"""M1 procurement marts. Two parallel views, in separate files, so they cannot be added together by accident.

No view is the default, and neither is the business truth (COR-09). Amounts stay in their own currency.
Dates are requested or promised, because no receipt date exists. ``implied_unit_amount_scenario``
assumes PO-Item Amount is the line total for PR-Quantity (DEF-05, assumption A-13).
"""
import pandas as pd

from src.preprocessing.joins import audited_lookup
from src.preprocessing.outliers import robust_outlier_flags
from src.preprocessing.prpo_views import DISTINCT, ORIGINAL

VIEWS = (ORIGINAL, DISTINCT)
_LINE_COLUMNS = ["purchase_requisition", "pr_item", "purchase_order", "po_item", "material_no", "material_desc_clean", "unit", "pr_quantity", "supplier_code", "supplier_name", "po_item_amount", "currency",
                 "pr_type", "pr_prefix", "po_prefix", "purchasing_group", "plant", "pr_date", "pr_month", "pr_delivery_date", "po_delivery_date", "requested_interval_days", "promised_interval_days", "promise_gap_days",
                 "occurrence_count", "occurrence_rank", "content_group_id", "in_idr_scope", "is_non_idr_supplier", "flag_req_before_pr", "flag_promise_before_pr", "flag_future_requested_date",
                 "flag_future_promised_date", "flag_future_date", "rare_pr_type", "rare_purchasing_group", "desc_shared_group_id", "source_row", "row_hash"]
_VIEW_FLAGS = ("flag_extreme_interval", "flag_outlier_pr_quantity", "flag_outlier_requested_interval", "flag_outlier_promised_interval", "flag_outlier_promise_gap")


def build_procurement_line(fact: pd.DataFrame, dim_material: pd.DataFrame, view: str, audit_log: list | None = None) -> pd.DataFrame:
    """ORIGINAL grain: one PR PO source row. DISTINCT grain: one PR item and one PO item."""
    rows = fact if view == ORIGINAL else fact[fact["in_exact_distinct_rows"].fillna(False).astype(bool)]
    line = rows[_LINE_COLUMNS].reset_index(drop=True)
    line.insert(0, "analysis_view", pd.array([view] * len(line), dtype="string"))
    for flag in _VIEW_FLAGS:
        line[flag] = rows[f"{flag}__{view}"].reset_index(drop=True)
    line["implied_unit_amount_scenario"] = (line["po_item_amount"] / line["pr_quantity"].astype("Float64")).round(6)
    outliers = robust_outlier_flags(line["implied_unit_amount_scenario"], line["material_no"] + "|" + line["currency"].astype("string"), line["unit"].astype("string") + "|" + line["currency"].astype("string"))
    line["flag_outlier_implied_unit_amount_scenario"] = outliers["flag"]
    attributes = dim_material[["material_no", "mrp_type", "material_prefix"]]
    line = audited_lookup(line, attributes, "material_no", f"mart_procurement_line.{view} -> dim_material", audit_log, require_all_matched=True)
    return line



def build_supplier_material(line: pd.DataFrame, view: str) -> pd.DataFrame:
    """Grain: supplier, material and currency. Quantity sums stay within one material, amounts within one currency.

    Interval statistics leave out rows promised or requested before the PR date (Spec P-06, P-07).
    Those rows stay counted in ``n_lines``. No ranking is calculated.
    """
    keys = ["supplier_code", "material_no", "currency"]
    frame = line.astype({"currency": "string", "unit": "string"})
    grouped = frame.groupby(keys, sort=True)
    result = pd.DataFrame({
        "supplier_name": grouped["supplier_name"].first(), "unit": grouped["unit"].first(), "n_lines": grouped.size().astype("Int64"),
        "n_purchase_orders": grouped["purchase_order"].nunique().astype("Int64"), "pr_quantity_total": grouped["pr_quantity"].sum().astype("Int64"),
        "pr_quantity_median": grouped["pr_quantity"].median().astype("Float64"), "po_item_amount_total": grouped["po_item_amount"].sum().round(2).astype("Float64"),
        "implied_unit_amount_scenario_min": grouped["implied_unit_amount_scenario"].min(), "implied_unit_amount_scenario_median": grouped["implied_unit_amount_scenario"].median().round(6),
        "implied_unit_amount_scenario_max": grouped["implied_unit_amount_scenario"].max(), "first_pr_date": grouped["pr_date"].min(), "last_pr_date": grouped["pr_date"].max(),
    })
    promised = frame[~frame["flag_promise_before_pr"].fillna(False).astype(bool)].groupby(keys)["promised_interval_days"]
    requested = frame[~frame["flag_req_before_pr"].fillna(False).astype(bool)].groupby(keys)["requested_interval_days"]
    result["n_lines_used_for_promised_interval"] = promised.size().reindex(result.index).fillna(0).astype("Int64")
    result["promised_interval_days_min"] = promised.min().astype("Float64")
    for name, q in (("p25", 0.25), ("median", 0.5), ("p75", 0.75), ("p90", 0.9)):
        result[f"promised_interval_days_{name}"] = promised.quantile(q).round(6).astype("Float64")
    result["promised_interval_days_max"] = promised.max().astype("Float64")
    result["n_lines_used_for_requested_interval"] = requested.size().reindex(result.index).fillna(0).astype("Int64")
    result["requested_interval_days_median"] = requested.median().astype("Float64")
    result = result.reset_index()
    result.insert(0, "analysis_view", pd.array([view] * len(result), dtype="string"))
    return result


def build_nonidr(line: pd.DataFrame) -> pd.DataFrame:
    """Non-IDR lines, reported apart because no exchange rate is available."""
    return line[~line["in_idr_scope"].fillna(False).astype(bool)].reset_index(drop=True)


def currency_summary(lines: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """One row per currency, with the two views side by side as alternatives. No total exists across currencies."""
    frames = {view: line.astype({"currency": "string"}).groupby("currency").agg(lines=("po_item_amount", "size"), amount=("po_item_amount", "sum")) for view, line in lines.items()}
    a, b = frames[ORIGINAL], frames[DISTINCT]
    result = pd.DataFrame({f"lines__{ORIGINAL}": a["lines"], f"lines__{DISTINCT}": b["lines"], f"amount__{ORIGINAL}": a["amount"].round(2), f"amount__{DISTINCT}": b["amount"].round(2)})
    result["ratio_original_to_distinct"] = (result[f"amount__{ORIGINAL}"] / result[f"amount__{DISTINCT}"]).astype("float64").round(4)
    return result.reset_index()
