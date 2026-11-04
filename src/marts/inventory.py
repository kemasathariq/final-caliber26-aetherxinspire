"""M2 inventory mart. Grain: one material. State comes from dim_material only.

Stock is an undated value as supplied (DEF-12). Min.Qty and Max.Qty are undefined planning values
(DEF-02), and are not capacity. Comparisons are raw. No stockout, excess, cover or reorder measure
exists here, because those need definitions or a dated stock. Materials never issued or procured
hold blanks in those summaries, not zeros: no record is different from a recorded zero.
"""
import pandas as pd

from src.marts.movement_copies import SCENARIO_A, SCENARIO_B
from src.preprocessing.joins import audited_lookup
from src.preprocessing.prpo_views import DISTINCT, ORIGINAL

_STATE = ["material_no", "material_desc_clean", "unit", "mrp_type", "material_prefix", "desc_shared_group_id", "stock", "min_qty", "max_qty", "n_bom_rows", "n_bom_locations",
          "n_fl_crit_A", "n_fl_crit_B", "n_fl_crit_C", "n_fl_crit_S", "n_fl_crit_null", "is_issued", "is_procured", "stock_eq_zero", "stock_lt_min", "stock_gt_max", "min_eq_max",
          "nonstock_with_stock", "stockitem_min_max_zero", "flag_fraction_on_count_unit", "flag_outlier_stock__one_row_per_material"]
_DEMAND = ("qty_issued_total", "n_issue_lines", "mean_monthly_qty", "std_monthly_qty", "max_monthly_qty", "mean_active_month_qty", "std_active_month_qty")
_PROCUREMENT = ("n_lines", "pr_quantity_total", "pr_quantity_median", "promised_interval_days_median", "promised_interval_days_p90", "requested_interval_days_median", "implied_unit_amount_scenario_median")


def _simulation_gaps(frame: pd.DataFrame) -> pd.Series:
    """Which inputs a later simulation lacks for this material. Having a value does not confirm its meaning."""
    tests = {"demand_history": frame["is_issued"].fillna(False).astype(bool), "promised_interval": frame[f"promised_interval_days_median__{ORIGINAL}"].notna(),
             "unit_amount": frame[f"implied_unit_amount_scenario_median__{ORIGINAL}"].notna(), "min_or_max": (frame["min_qty"] > 0) | (frame["max_qty"] > 0)}
    names = [";".join(name for name, ok in zip(tests, row) if not ok) for row in zip(*tests.values())]
    return pd.Series(pd.array([n if n else pd.NA for n in names], dtype="string"), index=frame.index)


def build_inventory(dim_material: pd.DataFrame, summaries: dict[str, pd.DataFrame], comparison: pd.DataFrame, supplier_material: dict[str, pd.DataFrame], audit_log: list | None = None) -> pd.DataFrame:
    frame = dim_material[_STATE].rename(columns={"flag_outlier_stock__one_row_per_material": "flag_outlier_stock"}).reset_index(drop=True)
    common = summaries[SCENARIO_A][["material_no", "months_with_issue", "first_issue_date", "last_issue_date", "flag_sparse_history", "n_lines_at_repeated_unit_maximum"]]
    frame = audited_lookup(frame, common, "material_no", "mart_material_inventory -> demand summary (shared fields)", audit_log)
    for scenario in (SCENARIO_A, SCENARIO_B):
        part = summaries[scenario][["material_no", *_DEMAND]].rename(columns={c: f"{c}__{scenario}" for c in _DEMAND})
        frame = audited_lookup(frame, part, "material_no", f"mart_material_inventory -> demand summary {scenario}", audit_log)
    impact = comparison[["material_no", "qty_diff_abs", "qty_diff_pct_of_a", "impact_tier", "is_materially_affected"]].rename(
        columns={"qty_diff_abs": "demand_qty_diff_abs", "qty_diff_pct_of_a": "demand_qty_diff_pct_of_a", "impact_tier": "demand_impact_tier", "is_materially_affected": "demand_materially_affected"})
    frame = audited_lookup(frame, impact, "material_no", "mart_material_inventory -> demand comparison", audit_log)
    supplier = supplier_material[ORIGINAL][["material_no", "supplier_code", "currency"]]
    frame = audited_lookup(frame, supplier, "material_no", "mart_material_inventory -> supplier", audit_log)
    for view in (ORIGINAL, DISTINCT):
        part = supplier_material[view][["material_no", *_PROCUREMENT]].rename(columns={c: f"{c}__{view}" for c in _PROCUREMENT})
        frame = audited_lookup(frame, part, "material_no", f"mart_material_inventory -> supplier material {view}", audit_log)
    frame = frame.rename(columns={f"n_lines__{v}": f"n_pr_lines__{v}" for v in (ORIGINAL, DISTINCT)})
    frame["simulation_inputs_missing"] = _simulation_gaps(frame)
    return frame


def procurement_issue_reconciliation(inventory: pd.DataFrame) -> pd.DataFrame:
    """Requested against issued quantity, on materials present in both, within one unit.

    No receipts or dated stock exist, so this is a plausibility comparison and not a stock balance.
    """
    shared = inventory[inventory["is_issued"].fillna(False).astype(bool) & inventory["is_procured"].fillna(False).astype(bool)].astype({"unit": "string"})
    rows = []
    for unit, part in shared.groupby("unit"):
        entry = {"unit": unit, "materials_in_both": len(part)}
        for view in (ORIGINAL, DISTINCT):
            entry[f"pr_quantity__{view}"] = int(part[f"pr_quantity_total__{view}"].sum())
        for scenario in (SCENARIO_A, SCENARIO_B):
            entry[f"issued_quantity__{scenario}"] = int(part[f"qty_issued_total__{scenario}"].sum())
        entry["ratio_distinct_rows_to_scenario_a"] = round(entry[f"pr_quantity__{DISTINCT}"] / entry[f"issued_quantity__{SCENARIO_A}"], 3)
        per_material = part[f"pr_quantity_total__{DISTINCT}"].astype("float64") / part[f"qty_issued_total__{SCENARIO_A}"].astype("float64")
        entry["median_material_ratio_distinct_rows_to_scenario_a"] = round(float(per_material.median()), 3)
        rows.append(entry)
    return pd.DataFrame(rows)
