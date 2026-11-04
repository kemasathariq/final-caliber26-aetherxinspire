"""Evidence about repeated rows (Spec Section 2.1, plan Section 7). It tests. It decides nothing.

Results here can show whether copy counts relate to measured fields. They cannot show
why rows repeat: "Cannot be confirmed from the available data or documentation."
Only the case owner can answer that (DEF-01, A-05).
"""
import numpy as np
import pandas as pd
from scipy import stats

from src.config import PERMUTATION_ROUNDS, PERMUTATION_SEED
from src.preprocessing.prpo_views import DISTINCT, ORIGINAL


def same_copy_share(keys: pd.Series, copies: pd.Series) -> float:
    """Share of multi-line documents where every line has the same copy count."""
    frame = pd.DataFrame({"key": keys.to_numpy(), "copies": copies.to_numpy()})
    return float((frame.groupby("key", sort=False)["copies"].nunique() == 1).mean())


def document_permutation_test(distinct: pd.DataFrame, key: str, rng: np.random.Generator, rounds: int = PERMUTATION_ROUNDS) -> dict:
    """Would a document's lines share a copy count more often than random assignment gives?

    A document-level repeat would push the observed share well above the shuffled range.
    """
    sizes = distinct.groupby(key, sort=False)[key].transform("size")
    multi = distinct[sizes > 1]
    keys = multi[key].to_numpy()
    copies = multi["occurrence_count"].astype("int64").to_numpy()
    observed = same_copy_share(multi[key], multi["occurrence_count"])
    shuffled = [same_copy_share(pd.Series(keys), pd.Series(rng.permutation(copies))) for _ in range(rounds)]
    return {"grouping": key, "documents_with_multiple_lines": int(multi[key].nunique()), "observed_same_copy_share": round(observed, 4),
            "shuffled_mean": round(float(np.mean(shuffled)), 4), "shuffled_min": round(float(np.min(shuffled)), 4), "shuffled_max": round(float(np.max(shuffled)), 4),
            "permutation_rounds": rounds, "seed": PERMUTATION_SEED,
            # One-sided, with the standard +1 correction so a p-value is never reported as 0.
            "p_observed_at_or_above_shuffled": round((sum(s >= observed for s in shuffled) + 1) / (rounds + 1), 4)}


def _spearman(name: str, scope: str, copies: pd.Series, values: pd.Series) -> dict:
    pair = pd.DataFrame({"c": copies.astype("float64").to_numpy(), "v": values.astype("float64").to_numpy()}).dropna()
    test = stats.spearmanr(pair["c"], pair["v"])
    return {"field": name, "scope": scope, "rows": len(pair), "spearman_rho": round(float(test.statistic), 4), "p_value": float(f"{test.pvalue:.4g}")}


def numeric_associations(distinct: pd.DataFrame, movement: pd.DataFrame, bom: pd.DataFrame) -> pd.DataFrame:
    """Copy count against numeric fields, keeping amounts within one currency and quantities within one unit."""
    frame = distinct.copy()
    copies = frame["occurrence_count"]
    frame["lines_per_pr"] = frame.groupby("purchase_requisition")["pr_item"].transform("size")
    frame["lines_per_po"] = frame.groupby("purchase_order")["po_item"].transform("size")
    frame["pr_item_number"] = frame["pr_item"].astype("int64")
    frame["requested_interval_days"] = (frame["pr_delivery_date"] - frame["pr_date"]).dt.days
    frame["promised_interval_days"] = (frame["po_delivery_date"] - frame["pr_date"]).dt.days
    frame["pr_date_ordinal"] = frame["pr_date"].map(pd.Timestamp.toordinal)
    frame["movement_rows_for_material"] = frame["material_no"].map(movement.groupby("material_no").size()).fillna(0)
    frame["bom_locations_for_material"] = frame["material_no"].map(
        bom.drop_duplicates(["functional_location", "material_no"]).groupby("material_no").size())
    rows = [_spearman(c, "exact_distinct_rows", copies, frame[c]) for c in (
        "lines_per_pr", "lines_per_po", "pr_item_number", "requested_interval_days", "promised_interval_days",
        "pr_date_ordinal", "movement_rows_for_material", "bom_locations_for_material")]
    idr = frame["currency"].astype("string") == "IDR"
    rows.append(_spearman("po_item_amount", "exact_distinct_rows, IDR only", copies[idr], frame.loc[idr, "po_item_amount"]))
    for unit in ("EA", "KG"):
        inside = frame["unit"].astype("string") == unit
        rows.append(_spearman("pr_quantity", f"exact_distinct_rows, unit {unit} only", copies[inside], frame.loc[inside, "pr_quantity"]))
    return pd.DataFrame(rows)


def _chi_square(name: str, values: pd.Series, copies: pd.Series, note: str = "") -> dict:
    table = pd.crosstab(values.astype("string"), copies.astype("int64"))
    table = table.loc[table.sum(axis=1) > 0, table.sum(axis=0) > 0]
    chi, p, dof, expected = stats.chi2_contingency(table)
    return {"field": name, "levels": table.shape[0], "rows": int(table.to_numpy().sum()), "chi_square": round(float(chi), 3), "dof": int(dof),
            "p_value": float(f"{p:.4g}"), "cramers_v": round(float(np.sqrt(chi / (table.to_numpy().sum() * (min(table.shape) - 1)))), 4),
            "cells_expected_below_5_pct": round(float((expected < 5).mean() * 100), 1), "note": note}


def holm_adjust(p_values: pd.Series) -> pd.Series:
    """Holm step-down correction: conservative, and valid without assuming independent tests."""
    ordered = p_values.sort_values(kind="stable")
    adjusted, running = {}, 0.0
    for position, (index, p) in enumerate(ordered.items()):
        running = max(running, min(1.0, p * (len(ordered) - position)))
        adjusted[index] = float(f"{running:.4g}")
    return pd.Series(adjusted).reindex(p_values.index)


def categorical_associations(distinct: pd.DataFrame, minimum_supplier_rows: int = 30) -> pd.DataFrame:
    """Chi-square against copy count, with a Holm correction because several fields are tested together."""
    copies = distinct["occurrence_count"]
    rows = [_chi_square(c, distinct[c], copies) for c in ("pr_type", "purchasing_group", "currency", "unit")]
    rows.append(_chi_square("pr_month", distinct["pr_date"].dt.strftime("%Y-%m"), copies))
    rows.append(_chi_square("po_prefix", distinct["purchase_order"].str[:2], copies))
    sizes = distinct["supplier_code"].map(distinct["supplier_code"].value_counts())
    common = sizes >= minimum_supplier_rows
    rows.append(_chi_square("supplier_code", distinct.loc[common, "supplier_code"], copies[common], f"Suppliers with at least {minimum_supplier_rows} rows"))
    result = pd.DataFrame(rows)
    result["p_value_holm"] = holm_adjust(result["p_value"])
    return result


def key_structure(original: pd.DataFrame, distinct: pd.DataFrame) -> dict:
    """Do keys repeat only as complete copies, and could any repeat be a separate transaction?"""
    pr_key, po_key = ["purchase_requisition", "pr_item"], ["purchase_order", "po_item"]
    near_all = ["pr_date", "material_no", "pr_quantity", "po_item_amount", "purchase_order"]
    near_some = ["pr_date", "material_no", "pr_quantity"]
    return {
        "pr_key_repeats_original_rows": int(original.duplicated(pr_key).sum()), "pr_key_repeats_distinct_rows": int(distinct.duplicated(pr_key).sum()),
        "po_key_repeats_original_rows": int(original.duplicated(po_key).sum()), "po_key_repeats_distinct_rows": int(distinct.duplicated(po_key).sum()),
        "same_pr_key_with_different_content": int((original.groupby(pr_key)["row_hash"].nunique() > 1).sum()),
        "same_po_key_with_different_content": int((original.groupby(po_key)["row_hash"].nunique() > 1).sum()),
        "max_po_items_per_pr_item_distinct_rows": int(distinct.groupby(pr_key)[po_key].nunique().max().max()),
        "max_pr_items_per_po_item_distinct_rows": int(distinct.assign(_k=distinct["purchase_requisition"] + "|" + distinct["pr_item"]).groupby(po_key)["_k"].nunique().max()),
        "different_key_same_date_material_quantity_amount_po_rows": int(distinct.duplicated(near_all, keep=False).sum()),
        "different_key_same_date_material_quantity_rows": int(distinct.duplicated(near_some, keep=False).sum()),
    }


def prpo_duplicate_evidence(views: dict[str, pd.DataFrame], movement: pd.DataFrame, bom: pd.DataFrame) -> dict:
    original, distinct = views[ORIGINAL], views[DISTINCT]
    rng = np.random.default_rng(PERMUTATION_SEED)
    # Evaluated in this order so the seeded sequence stays stable.
    permutations = pd.DataFrame([document_permutation_test(distinct, key, rng) for key in ("purchase_requisition", "purchase_order", "material_no")])
    return {"keys": key_structure(original, distinct), "permutations": permutations,
            "numeric": numeric_associations(distinct, movement, bom), "categorical": categorical_associations(distinct)}


def movement_sensitivity(movement_labelled: pd.DataFrame) -> pd.DataFrame:
    """Compare all rows with exact-distinct rows. Quantities stay within one material or one unit."""
    distinct = movement_labelled[movement_labelled["occurrence_rank"] == 1]
    rows = []

    def add(metric: str, all_rows, distinct_rows, group: str = "") -> None:
        rows.append({"metric": metric, "group": group, "all_rows": all_rows, "exact_distinct_rows": distinct_rows,
                     "change_pct": round(100 * (distinct_rows - all_rows) / all_rows, 3) if all_rows else None})

    add("issue_lines", len(movement_labelled), len(distinct))
    add("distinct_orders", int(movement_labelled["order_no"].nunique()), int(distinct["order_no"].nunique()))
    add("distinct_materials", int(movement_labelled["material_no"].nunique()), int(distinct["material_no"].nunique()))
    for unit, part in movement_labelled.astype({"unit": "string"}).groupby("unit"):
        inside = distinct[distinct["unit"].astype("string") == unit]
        add("quantity_sum_within_unit", int(part["quantity"].sum()), int(inside["quantity"].sum()), unit)

    lines_all, lines_distinct = movement_labelled.groupby("material_no").size(), distinct.groupby("material_no").size()
    quantity_all = movement_labelled.groupby("material_no")["quantity"].sum().astype("float64")
    quantity_distinct = distinct.groupby("material_no")["quantity"].sum().astype("float64")
    drop = 1 - quantity_distinct / quantity_all
    per_material = [("materials_with_any_line_removed_in_distinct_view", int((lines_all != lines_distinct).sum())),
                    ("materials_with_quantity_change_above_10pct", int((drop > 0.10).sum())),
                    ("materials_with_quantity_change_above_25pct", int((drop > 0.25).sum())),
                    ("max_quantity_change_pct_within_a_material", round(float(drop.max() * 100), 2)),
                    ("spearman_material_line_counts_between_views", round(float(stats.spearmanr(lines_all, lines_distinct).statistic), 4)),
                    ("spearman_material_quantity_between_views", round(float(stats.spearmanr(quantity_all, quantity_distinct).statistic), 4))]
    for metric, value in per_material:
        rows.append({"metric": metric, "group": "per material", "all_rows": None, "exact_distinct_rows": None, "change_pct": None, "value": value})
    months_all = movement_labelled["posting_date"].dt.strftime("%Y-%m").value_counts().sort_index()
    months_distinct = distinct["posting_date"].dt.strftime("%Y-%m").value_counts().sort_index()
    for month in months_all.index:
        add("issue_lines_in_month", int(months_all[month]), int(months_distinct.get(month, 0)), month)
    return pd.DataFrame(rows)


def shared_order_review(bridge_order: pd.DataFrame, fact_issue: pd.DataFrame, bridge_material: pd.DataFrame) -> pd.DataFrame:
    """One row per order on several notifications. Reported for the case owner. Nothing is allocated."""
    shared = bridge_order[bridge_order["order_shared"].fillna(False).astype(bool)].sort_values(["order_no", "notification"])
    pairs = set(zip(bridge_material["functional_location"], bridge_material["material_no"]))
    rows = []
    for order, part in shared.groupby("order_no", sort=True):
        issues = fact_issue[fact_issue["order_no"] == order]
        materials = issues["material_no"].tolist()
        locations = part["functional_location"].tolist()
        matches = [sum((location, material) in pairs for location in locations) for material in materials]
        rows.append({"order_no": order, "notifications": ";".join(part["notification"]), "functional_locations": ";".join(locations),
                     "notification_dates": ";".join(part["notification_date"].dt.strftime("%Y-%m-%d")),
                     "same_notification_date": part["notification_date"].nunique() == 1, "same_location_prefix": len({l.split("_")[0] for l in locations}) == 1,
                     "issue_rows": len(issues), "issue_rows_material_in_exactly_one_location_bom": sum(m == 1 for m in matches),
                     "issue_rows_material_in_more_than_one_location_bom": sum(m > 1 for m in matches), "issue_rows_material_in_no_location_bom": sum(m == 0 for m in matches)})
    return pd.DataFrame(rows)
