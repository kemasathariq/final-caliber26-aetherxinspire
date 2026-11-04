"""PR PO dual views (approved Decision 4).

Two parallel views of the same 11,609 source rows:

    original_rows        every source row, exactly as supplied
    exact_distinct_rows  the first occurrence of each exact-duplicate group

The distinct view is a sensitivity scenario. It is not a statement that repeated
rows are invalid, and neither view is the definitive business truth. Every metric
must state its view. Rows are labelled and filtered here, never deleted.
"""
import pandas as pd

from src.config import DATA_CUTOFF

ORIGINAL = "original_rows"
DISTINCT = "exact_distinct_rows"

VIEW_DEFINITIONS = {
    ORIGINAL: {
        "definition": "All PR PO source rows, unchanged.",
        "limitation": ("If repeated rows are copies of one document line, counts, quantities "
                       "and amounts are overstated."),
    },
    DISTINCT: {
        "definition": "First occurrence of each group of rows identical in all 18 source columns.",
        "limitation": ("If repeated rows are real separate transactions, counts, quantities and "
                       "amounts are understated. This is a sensitivity scenario, not a "
                       "correction of the data."),
    },
}


def build_prpo_views(labelled: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return (original_rows view, exact_distinct_rows view) from labelled PR PO rows."""
    original = labelled.copy()
    original["analysis_view"] = pd.array([ORIGINAL] * len(original), dtype="string")

    row_lists = (labelled.groupby("content_group_id")["source_row"]
                 .agg(lambda rows: ";".join(str(int(r)) for r in sorted(rows))))
    distinct = labelled[labelled["occurrence_rank"] == 1].copy()
    distinct["all_source_rows"] = pd.array(
        distinct["content_group_id"].map(row_lists).tolist(), dtype="string")
    distinct["analysis_view"] = pd.array([DISTINCT] * len(distinct), dtype="string")
    return original, distinct.reset_index(drop=True)


def _view_metrics(view: pd.DataFrame) -> dict[tuple[str, str, str], float]:
    """Metrics for one view, keyed by (metric, group_field, group)."""
    metrics: dict[tuple[str, str, str], float] = {
        ("row_count", "", ""): len(view),
        ("distinct_pr_items", "", ""): view[["purchase_requisition", "pr_item"]].drop_duplicates().shape[0],
        ("distinct_po_items", "", ""): view[["purchase_order", "po_item"]].drop_duplicates().shape[0],
        ("distinct_purchase_requisitions", "", ""): view["purchase_requisition"].nunique(),
        ("distinct_purchase_orders", "", ""): view["purchase_order"].nunique(),
    }
    for currency, value in view.groupby("currency", observed=True)["po_item_amount"].sum().items():
        metrics[("po_item_amount_sum", "currency", str(currency))] = float(value)
    for currency, value in view.groupby("currency", observed=True).size().items():
        metrics[("row_count", "currency", str(currency))] = int(value)
    for unit, value in view.groupby("unit", observed=True)["pr_quantity"].sum().items():
        metrics[("pr_quantity_sum", "unit", str(unit))] = float(value)

    # Requested and promised dates only. No actual receipt date exists.
    requested = (view["pr_delivery_date"] - view["pr_date"]).dt.days
    promised = (view["po_delivery_date"] - view["pr_date"]).dt.days
    metrics.update({
        ("requested_interval_days_median", "", ""): float(requested.median()),
        ("requested_interval_days_mean", "", ""): round(float(requested.mean()), 4),
        ("promised_interval_days_median", "", ""): float(promised.median()),
        ("promised_interval_days_mean", "", ""): round(float(promised.mean()), 4),
        ("requested_date_before_pr_date_rows", "", ""): int((requested < 0).sum()),
        ("promised_date_before_pr_date_rows", "", ""): int((promised < 0).sum()),
        ("promised_date_before_requested_date_rows", "", ""):
            int((view["po_delivery_date"] < view["pr_delivery_date"]).sum()),
        ("requested_date_after_cutoff_rows", "", ""):
            int((view["pr_delivery_date"] > pd.Timestamp(DATA_CUTOFF)).sum()),
        ("promised_date_after_cutoff_rows", "", ""):
            int((view["po_delivery_date"] > pd.Timestamp(DATA_CUTOFF)).sum()),
    })
    return metrics


def compare_views(original: pd.DataFrame, distinct: pd.DataFrame) -> pd.DataFrame:
    """Side-by-side metrics. Each value belongs to one named view and they are never combined."""
    first, second = _view_metrics(original), _view_metrics(distinct)
    rows = []
    for key in sorted(set(first) | set(second)):
        metric, group_field, group = key
        a, b = first.get(key), second.get(key)
        rows.append({
            "metric": metric,
            "group_field": group_field,
            "group": group,
            ORIGINAL: a,
            DISTINCT: b,
            "ratio_original_to_distinct": round(a / b, 4) if a is not None and b else None,
        })
    return pd.DataFrame(rows)
