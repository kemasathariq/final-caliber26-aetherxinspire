"""M3 demand marts. Each scenario is aggregated separately from its own record set.

Rules: quantity is summed within one material only. Zeros are filled only inside the
demand window, and only for materials with an eligible issue. Never-issued materials are
not zero-filled. Issues are observed movements. They are not proven demand or receipts.
"""
import pandas as pd

from src.config import DEMAND_IMPACT_HIGH_PCT, DEMAND_IMPACT_MATERIAL_PCT, LOW_LINE_COUNT, SPARSE_HISTORY_MONTHS
from src.marts.movement_copies import ADJACENT, FAR, NEAR, SCENARIO_A, SCENARIO_B, demand_months
from src.preprocessing.joins import audited_lookup

NO_CHANGE, BELOW, MATERIAL, HIGH = "no_change", "below_threshold", "material", "high"
_MEMBERSHIP = {SCENARIO_A: "in_scenario_a", SCENARIO_B: "in_scenario_b"}


def scenario_rows(classification: pd.DataFrame, scenario: str) -> pd.DataFrame:
    return classification[classification[_MEMBERSHIP[scenario]].fillna(False).astype(bool)]


def eligible_materials(classification: pd.DataFrame) -> pd.Series:
    """Both scenarios cover the same materials, so a material absent from B would appear as zero, not vanish."""
    return pd.Series(sorted(classification.loc[classification["is_eligible_demand"].fillna(False).astype(bool), "material_no"].unique()), dtype="string", name="material_no")


def build_demand_month(classification: pd.DataFrame, scenario: str, dim_material: pd.DataFrame, audit_log: list | None = None) -> pd.DataFrame:
    """Grain: one material by calendar month, zero-filled inside the window."""
    rows = scenario_rows(classification, scenario)
    keys = ["material_no", "posting_month"]
    grouped = rows.groupby(keys, sort=True)
    with_link = rows[rows["has_notification"].fillna(False).astype(bool)]
    aggregates = pd.DataFrame({
        "qty_issued": grouped["quantity"].sum(), "n_issue_lines": grouped.size(), "n_orders": grouped["order_no"].nunique(),
        "n_orders_with_notification": with_link.groupby(keys)["order_no"].nunique(), "n_repeat_lines_included": grouped["is_copy_c1"].sum(),
    })
    frame_index = pd.MultiIndex.from_product([eligible_materials(classification), demand_months()], names=keys)
    month = aggregates.reindex(frame_index)
    month["is_zero_filled"] = month["n_issue_lines"].isna().astype("boolean")
    month = month.fillna({c: 0 for c in aggregates.columns}).astype({c: "Int64" for c in aggregates.columns}).reset_index().rename(columns={"posting_month": "month"})
    month.insert(0, "demand_scenario", pd.array([scenario] * len(month), dtype="string"))
    attributes = dim_material[["material_no", "unit", "mrp_type", "material_prefix"]]
    month = audited_lookup(month, attributes, "material_no", f"mart_material_demand_month.{scenario} -> dim_material", audit_log, require_all_matched=True)
    order = ["demand_scenario", "material_no", "month", "unit", "mrp_type", "material_prefix", "qty_issued", "n_issue_lines", "n_orders", "n_orders_with_notification", "n_repeat_lines_included", "is_zero_filled"]
    return month[order]


def build_demand_summary(month: pd.DataFrame, classification: pd.DataFrame, scenario: str, audit_log: list | None = None) -> pd.DataFrame:
    """Grain: one material. Monthly statistics use the 17-month zero-filled series."""
    rows = scenario_rows(classification, scenario)
    series = month.assign(_q=month["qty_issued"].astype("float64"))
    per_material = series.groupby("material_no", sort=True)
    active = series[series["qty_issued"] > 0].groupby("material_no")["_q"]
    lines = rows.groupby("material_no")
    summary = pd.DataFrame({
        "months_in_window": per_material.size().astype("Int64"),
        "qty_issued_total": per_material["qty_issued"].sum().astype("Int64"),
        "n_issue_lines": per_material["n_issue_lines"].sum().astype("Int64"),
        "n_orders": lines["order_no"].nunique().astype("Int64"),
        "months_with_issue": active.size().astype("Int64"),
        "mean_monthly_qty": per_material["_q"].mean().round(6),
        "std_monthly_qty": per_material["_q"].std(ddof=1).round(6),
        "max_monthly_qty": per_material["_q"].max(),
        "mean_active_month_qty": active.mean().round(6),
        "std_active_month_qty": active.std(ddof=1).round(6),
        "max_line_qty": lines["quantity"].max().astype("float64"),
        "first_issue_date": lines["posting_date"].min(),
        "last_issue_date": lines["posting_date"].max(),
        "n_lines_with_unique_location": rows[rows["fl_attribution"] == "unique"].groupby("material_no").size(),
        "n_lines_with_ambiguous_location": rows[rows["fl_attribution"] == "ambiguous"].groupby("material_no").size(),
        "n_lines_at_repeated_unit_maximum": rows[rows["flag_at_repeated_unit_maximum"].fillna(False).astype(bool)].groupby("material_no").size(),
    })
    for column in ("n_lines_with_unique_location", "n_lines_with_ambiguous_location", "n_lines_at_repeated_unit_maximum"):
        summary[column] = summary[column].fillna(0).astype("Int64")
    summary["flag_sparse_history"] = (summary["months_with_issue"] < SPARSE_HISTORY_MONTHS).astype("boolean")
    summary = summary.reset_index()
    summary.insert(0, "demand_scenario", pd.array([scenario] * len(summary), dtype="string"))
    attributes = month.drop_duplicates("material_no")[["material_no", "unit", "mrp_type", "material_prefix"]]
    summary = audited_lookup(summary, attributes, "material_no", f"mart_material_demand_summary.{scenario} -> demand month", audit_log, require_all_matched=True)
    return summary


def _impact_tier(pct_magnitude: pd.Series) -> pd.Series:
    tier = pd.Series(BELOW, index=pct_magnitude.index, dtype="string")
    tier[pct_magnitude == 0] = NO_CHANGE
    tier[pct_magnitude >= DEMAND_IMPACT_MATERIAL_PCT] = MATERIAL
    tier[pct_magnitude >= DEMAND_IMPACT_HIGH_PCT] = HIGH
    return tier


def compare_scenarios(summary_a: pd.DataFrame, summary_b: pd.DataFrame, month_a: pd.DataFrame, month_b: pd.DataFrame, classification: pd.DataFrame) -> pd.DataFrame:
    """Grain: one material, comparing separately calculated results. Neither scenario is treated as correct."""
    a, b = summary_a.set_index("material_no"), summary_b.set_index("material_no")
    if not a.index.equals(b.index):
        raise AssertionError("Scenarios cover different materials")
    frame = pd.DataFrame({"unit": a["unit"], "mrp_type": a["mrp_type"], "material_prefix": a["material_prefix"]}, index=a.index)
    for measure, label in (("qty_issued_total", "qty"), ("n_issue_lines", "lines")):
        frame[f"{label}_scenario_a"], frame[f"{label}_scenario_b"] = a[measure], b[measure]
        difference = (a[measure] - b[measure]).astype("Int64")
        frame[f"{label}_diff_abs"] = difference.abs()
        frame[f"{label}_diff_pct_of_a"] = (100 * difference.astype("float64") / a[measure].astype("float64")).round(4)
        frame[f"{label}_diff_pct_of_b"] = (100 * difference.astype("float64") / b[measure].astype("float64")).round(4)
    for measure in ("mean_monthly_qty", "std_monthly_qty", "max_monthly_qty"):
        frame[f"{measure}_scenario_a"], frame[f"{measure}_scenario_b"] = a[measure], b[measure]
        frame[f"{measure}_diff_abs"] = (a[measure] - b[measure]).abs().round(6)
    frame["months_with_issue"] = a["months_with_issue"]
    frame["months_with_issue_scenario_b"] = b["months_with_issue"]
    keys = ["material_no", "month"]
    monthly = month_a[keys + ["qty_issued"]].merge(month_b[keys + ["qty_issued"]], on=keys, suffixes=("_a", "_b"), validate="one_to_one")
    monthly["_d"] = (monthly["qty_issued_a"] - monthly["qty_issued_b"]).abs()
    frame["months_with_difference"] = monthly[monthly["_d"] > 0].groupby("material_no").size().reindex(frame.index).fillna(0).astype("Int64")
    frame["max_month_qty_diff_abs"] = monthly.groupby("material_no")["_d"].max().reindex(frame.index).astype("Int64")
    removed = classification[classification["is_copy_c1"].fillna(False).astype(bool) & classification["is_eligible_demand"].fillna(False).astype(bool)]
    for name, label in ((ADJACENT, "adjacent"), (NEAR, "near"), (FAR, "far")):
        frame[f"qty_copy_class_{label}"] = removed[removed["copy_class"] == name].groupby("material_no")["quantity"].sum().reindex(frame.index).fillna(0).astype("Int64")
    frame["impact_tier"] = _impact_tier(frame["qty_diff_pct_of_a"])
    frame["is_materially_affected"] = frame["impact_tier"].isin([MATERIAL, HIGH]).astype("boolean")
    frame["flag_low_line_count"] = (frame["lines_scenario_a"] < LOW_LINE_COUNT).astype("boolean")
    frame["impact_reason"] = pd.array([
        f"Quantity falls {q:.2f}% ({int(d)} {u}) and lines fall from {la} to {lb} when rule C1 rows are excluded." + (" Few lines, so the percentage is sensitive." if low else "") if d else "No rule C1 rows, so both scenarios agree."
        for q, d, u, la, lb, low in zip(frame["qty_diff_pct_of_a"], frame["qty_diff_abs"], frame["unit"], frame["lines_scenario_a"], frame["lines_scenario_b"], frame["flag_low_line_count"])], dtype="string")
    return frame.reset_index()


def unit_scenario_summary(summary_a: pd.DataFrame, summary_b: pd.DataFrame) -> pd.DataFrame:
    """Within one unit only. No total exists across units."""
    a = summary_a.astype({"unit": "string"}).groupby("unit")[["qty_issued_total", "n_issue_lines"]].sum()
    b = summary_b.astype({"unit": "string"}).groupby("unit")[["qty_issued_total", "n_issue_lines"]].sum()
    frame = pd.DataFrame({"materials": summary_a.astype({"unit": "string"}).groupby("unit").size().astype("Int64"), "qty_scenario_a": a["qty_issued_total"], "qty_scenario_b": b["qty_issued_total"],
                          "qty_diff_abs": a["qty_issued_total"] - b["qty_issued_total"], "lines_scenario_a": a["n_issue_lines"], "lines_scenario_b": b["n_issue_lines"]})
    frame["qty_diff_pct_of_a"] = (100 * frame["qty_diff_abs"].astype("float64") / frame["qty_scenario_a"].astype("float64")).round(4)
    return frame.reset_index()


def impact_sensitivity(comparison: pd.DataFrame) -> pd.DataFrame:
    """How the affected count moves with the threshold, overall and for materials with enough lines."""
    rows = []
    enough = ~comparison["flag_low_line_count"]
    for threshold in (1.0, 5.0, 10.0, 25.0, 50.0):
        hit = comparison["qty_diff_pct_of_a"] >= threshold
        rows.append({"threshold_pct": threshold, "materials_at_or_above": int(hit.sum()), "of_which_low_line_count": int((hit & ~enough).sum()), "of_which_enough_lines": int((hit & enough).sum()), "materials_total": len(comparison)})
    return pd.DataFrame(rows)


