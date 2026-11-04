"""Record-level Movement classification for the two demand scenarios.

Nothing is deleted. Every Movement source row appears once, with its flags and reason.

Eligibility (both scenarios). A row counts as demand only if all of these hold:
    E1  Movement Type is Issue
    E2  Posting Date is inside the demand window
    E3  Quantity is above zero
    E4  Material exists in dim_material
    E5  Unit equals the material's unit in dim_material

Copy rule (Scenario B only).
    C1  The row is identical to an earlier row in all 7 source columns.
The earliest occurrence stays in Scenario B. Later occurrences are excluded. Because
occurrences are identical, the choice of which to keep changes no quantity.

Rows with the same date, material and order but a different quantity are NOT copies.

Limits. Movement has no document number, so C1 cannot separate an accidental copy from
two real issues of the same quantity, for the same order, on the same day. Neither
scenario is the true demand. Gap classes describe evidence and do not change membership.
"""
import pandas as pd

from src.config import COPY_NEAR_GAP_ROWS, DEMAND_WINDOW_END, DEMAND_WINDOW_START, REPEATED_MAXIMUM_MIN_MATERIALS

SCENARIO_A, SCENARIO_B = "scenario_a", "scenario_b"
UNIQUE, FIRST, ADJACENT, NEAR, FAR = ("unique_record", "first_occurrence_of_repeated_record", "repeat_adjacent", "repeat_near", "repeat_far")
SCENARIOS = {
    SCENARIO_A: {"definition": "All eligible Movement records.",
                 "limitation": "If identical rows are accidental copies of one event, demand is overstated."},
    SCENARIO_B: {"definition": "Eligible Movement records, excluding later occurrences of rows identical in all 7 source columns (rule C1).",
                 "limitation": "If identical rows are real separate issues, demand is understated."},
}
COPY_RULES = {
    "E1": "Movement Type is Issue", "E2": f"Posting Date is within {DEMAND_WINDOW_START} to {DEMAND_WINDOW_END}", "E3": "Quantity is above zero",
    "E4": "Material exists in dim_material", "E5": "Unit equals the material's unit in dim_material",
    "C1": "Identical to an earlier row in all 7 source columns. Earliest occurrence stays in Scenario B",
    "gap classes": f"{ADJACENT}: gap of 1 row. {NEAR}: gap of 2 to {COPY_NEAR_GAP_ROWS} rows. {FAR}: gap above {COPY_NEAR_GAP_ROWS} rows. Descriptive only",
}


def demand_months() -> pd.DatetimeIndex:
    return pd.date_range(f"{DEMAND_WINDOW_START}-01", f"{DEMAND_WINDOW_END}-01", freq="MS").astype("datetime64[ns]")


def _eligibility(fact: pd.DataFrame, dim_material: pd.DataFrame) -> pd.DataFrame:
    units = dim_material.set_index("material_no")["unit"].astype("string")
    months = demand_months()
    window_end = months[-1] + pd.offsets.MonthEnd(0)
    tests = pd.DataFrame({
        "E1": fact["movement_type"].astype("string") == "Issue",
        "E2": fact["posting_date"].between(months[0], window_end),
        "E3": fact["quantity"] > 0,
        "E4": fact["material_no"].isin(units.index),
        "E5": fact["unit"].astype("string") == fact["material_no"].map(units).astype("string"),
    }).fillna(False).astype(bool)
    failed = [";".join(rule for rule, ok in zip(tests.columns, row) if not ok) for row in tests.itertuples(index=False)]
    return pd.DataFrame({"is_eligible_demand": tests.all(axis=1).astype("boolean"),
                         "eligibility_rules_failed": pd.array([f if f else pd.NA for f in failed], dtype="string")}, index=fact.index)


def _reason(row_class: str, first_row: int, gap, count: int) -> str:
    if row_class == UNIQUE:
        return "No identical row exists. Included in both scenarios."
    if row_class == FIRST:
        return f"Earliest of {count} rows identical in all 7 source columns. Included in both scenarios."
    return (f"Rule C1: identical in all 7 source columns to source row {first_row}, which is the earliest of {count} occurrences. "
            f"{int(gap)} {'row' if gap == 1 else 'rows'} after the previous occurrence. Included in Scenario A, excluded from Scenario B. Not proven to be an error.")


def classify_movement_copies(fact_issue: pd.DataFrame, dim_material: pd.DataFrame) -> pd.DataFrame:
    """One row per Movement source row, in source order. Row count always equals the input."""
    columns = ["source_row", "row_hash", "posting_date", "movement_type", "material_no", "material_desc_clean", "quantity", "unit", "order_no", "posting_month", "order_prefix",
               "has_notification", "order_shared", "fl_attribution", "attributed_functional_location", "issued_material_in_fl_bom",
               "content_group_id", "occurrence_count", "occurrence_rank", "same_key_group_size", "is_partial_dup_group", "partial_dup_group_id"]
    rows = fact_issue.sort_values("source_row", kind="stable")[columns].reset_index(drop=True)
    grouped = rows.groupby("content_group_id", sort=False)["source_row"]
    rows["first_source_row_of_group"] = grouped.transform("min").astype("Int64")
    rows["copy_gap_rows"] = grouped.diff().astype("Int64")
    is_repeat = rows["occurrence_rank"] > 1
    rows["is_copy_c1"] = is_repeat.astype("boolean")
    copy_class = pd.Series(UNIQUE, index=rows.index, dtype="string")
    copy_class[(rows["occurrence_count"] > 1) & ~is_repeat] = FIRST
    copy_class[is_repeat & (rows["copy_gap_rows"] == 1)] = ADJACENT
    copy_class[is_repeat & (rows["copy_gap_rows"] > 1) & (rows["copy_gap_rows"] <= COPY_NEAR_GAP_ROWS)] = NEAR
    copy_class[is_repeat & (rows["copy_gap_rows"] > COPY_NEAR_GAP_ROWS)] = FAR
    rows["copy_class"] = copy_class
    rows["copy_classification_reason"] = pd.array(
        [_reason(c, f, g, n) for c, f, g, n in zip(rows["copy_class"], rows["first_source_row_of_group"], rows["copy_gap_rows"], rows["occurrence_count"])], dtype="string")
    rows = pd.concat([rows, _eligibility(rows, dim_material)], axis=1)
    rows["in_scenario_a"] = rows["is_eligible_demand"]
    rows["in_scenario_b"] = rows["is_eligible_demand"] & ~rows["is_copy_c1"]
    # The peak of a unit, when shared by several materials, may be a cap rather than a real extreme (A-11).
    distinct = rows[rows["in_scenario_b"]]
    peaks = distinct.astype({"unit": "string"}).groupby("unit")["quantity"].max()
    at_peak = distinct[distinct["quantity"] == distinct["unit"].astype("string").map(peaks)]
    shared = at_peak.astype({"unit": "string"}).groupby("unit")["material_no"].nunique()
    repeated = peaks[shared[shared >= REPEATED_MAXIMUM_MIN_MATERIALS].index]
    rows["flag_at_repeated_unit_maximum"] = (rows["quantity"] == rows["unit"].astype("string").map(repeated)).fillna(False).astype("boolean")
    if len(rows) != len(fact_issue):
        raise AssertionError("Classification changed the Movement row count")
    return rows
