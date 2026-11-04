"""Evidence for the simulation design and feasibility assessment. NOT a simulation engine.

This module simulates nothing. No events run, no stock is depleted over time, and no order is
generated. It records which materials enter the proposed population and why others do not, how much
evidence each input has, and simple arithmetic on the inputs. Every value is observed or arithmetic
on observed values and stated assumptions. No value here is a simulated result, or a historical
stockout, or a cost. Unit amounts are deliberately not read.
"""
import pandas as pd

from src.config import SIM_HORIZON_END, SIM_HORIZON_START, SIM_MIN_ACTIVE_MONTHS_TO_RESAMPLE_DEMAND, SIM_MIN_LINES_TO_RESAMPLE_LEAD
from src.marts.movement_copies import SCENARIO_A, SCENARIO_B
from src.preprocessing.joins import audited_lookup
from src.preprocessing.prpo_views import DISTINCT, ORIGINAL

IN_POPULATION, EXCLUDED = "in_population", "excluded"
# Reason names map to the inventory mart's simulation_inputs_missing, plus the Stock Item condition.
_REASONS = {"demand_history": "no_demand_history", "promised_interval": "no_promised_interval", "unit_amount": "no_unit_amount_record", "min_or_max": "min_and_max_both_zero"}
HORIZON_DAYS = (pd.Timestamp(SIM_HORIZON_END) - pd.Timestamp(SIM_HORIZON_START)).days + 1

DEMAND_RESAMPLE, DEMAND_FEW, DEMAND_SINGLE = "d1_resampling_allowed", "d2_replay_and_configured_only", "d3_single_active_month"
LEAD_RESAMPLE, LEAD_FEW, LEAD_THIN = "l1_resampling_allowed", "l2_point_and_configured_only", "l3_one_or_two_lines"

DESCRIPTIONS = {
    "material_no": "Material number, text", "unit": "Material unit", "mrp_type": "MRP type code from BoM", "population_status": "in_population or excluded, under the approved eligibility criteria",
    "exclusion_reasons": "Why the material is excluded. Blank if in the population", "n_exclusion_reasons": "Number of exclusion reasons",
    "assumed_initial_inventory": "Stock as supplied, ASSUMED to be inventory at the start of the horizon. Undated (DEF-12)", "min_parameter_unverified": "Min.Qty. Unverified parameter (DEF-02)", "max_parameter_unverified": "Max.Qty. Unverified parameter (DEF-02)",
    "lead_proxy_median_days__original_rows": "Median promised interval in this view. Proxy, not an actual lead time (DEF-06)", "lead_proxy_median_days__exact_distinct_rows": "Median promised interval in this view. Proxy, not an actual lead time (DEF-06)",
    "lead_proxy_p90_days__exact_distinct_rows": "90th percentile of the promised interval in this view. Proxy only", "lead_observations_distinct": "Promised intervals available on exact_distinct_rows. Copies are not independent observations",
    "pr_quantity_median__exact_distinct_rows": "Median PR quantity per line. May not be the ordered quantity (DEF-05)", "active_months": "Months with an issue, of 17. The same in both scenarios",
    "lines__scenario_a": "Issue lines in Scenario A", "lines__scenario_b": "Issue lines in Scenario B", "qty_total__scenario_a": "Issued quantity in Scenario A", "qty_total__scenario_b": "Issued quantity in Scenario B",
    "max_line_qty__scenario_a": "Largest single issue line. The same in both scenarios, since copies repeat a kept value", "demand_evidence_tier": "How much demand evidence exists, and what it allows (assumption S-16)", "lead_evidence_tier": "How much lead-proxy evidence exists, and what it allows (assumption S-16)",
    "resampling_allowed_demand": "Own-history resampling of demand is allowed", "resampling_allowed_lead": "Own-history resampling of the lead proxy is allowed", "resampling_allowed_both": "Both are allowed",
    "scenarios_identical_by_construction": "No rule C1 rows, so Scenarios A and B hold the same records and must give identical results", "demand_materially_affected": "Materially affected by the scenario choice (A-14)", "has_line_at_repeated_unit_peak": "Has a line at a repeated unit peak (A-11)",
    "at_or_below_min_at_start": "ARITHMETIC. Assumed initial inventory is at or below Min, so an order would be triggered on day 0 under the reference reading",
    "stays_above_min__scenario_a": "ARITHMETIC. Initial inventory minus all issues stays above Min, so no order would ever be triggered under the reference reading", "stays_above_min__scenario_b": "ARITHMETIC. As above, for Scenario B",
    "initial_inventory_covers_all_issues__scenario_a": "ARITHMETIC. Initial inventory is at least all issues in the window", "initial_inventory_covers_all_issues__scenario_b": "ARITHMETIC. As above, for Scenario B",
    "single_line_exceeds_max": "OBSERVED. One issue line is larger than Max, which conflicts with reading Max as an order-up-to level", "median_pr_quantity_exceeds_max": "OBSERVED. Median PR quantity is larger than Max, which conflicts with reading Max as an order-up-to level", "stock_above_max": "OBSERVED. Stock is above Max",
    "lead_proxy_exceeds_horizon": f"ARITHMETIC. Median lead proxy is longer than the {HORIZON_DAYS}-day horizon, so an order may never arrive inside it",
}


def _tier_demand(active: pd.Series) -> pd.Series:
    tier = pd.Series(pd.NA, index=active.index, dtype="string")
    tier[active == 1] = DEMAND_SINGLE
    tier[(active >= 2) & (active < SIM_MIN_ACTIVE_MONTHS_TO_RESAMPLE_DEMAND)] = DEMAND_FEW
    tier[active >= SIM_MIN_ACTIVE_MONTHS_TO_RESAMPLE_DEMAND] = DEMAND_RESAMPLE
    return tier


def _tier_lead(lines: pd.Series) -> pd.Series:
    tier = pd.Series(pd.NA, index=lines.index, dtype="string")
    tier[(lines >= 1) & (lines <= 2)] = LEAD_THIN
    tier[(lines >= 3) & (lines < SIM_MIN_LINES_TO_RESAMPLE_LEAD)] = LEAD_FEW
    tier[lines >= SIM_MIN_LINES_TO_RESAMPLE_LEAD] = LEAD_RESAMPLE
    return tier


def build_simulation_population(inventory: pd.DataFrame, summary_b: pd.DataFrame, supplier_distinct: pd.DataFrame, audit_log: list | None = None) -> pd.DataFrame:
    """One row per material in M2, including every excluded material and its reasons."""
    frame = inventory[["material_no", "unit", "mrp_type"]].copy()
    not_stock = inventory["mrp_type"].astype("string") != "Stock Item"
    missing = inventory["simulation_inputs_missing"].astype("string")
    reasons = []
    for excluded_type, gaps in zip(not_stock, missing):
        items = ["mrp_type_not_stock_item"] if excluded_type else []
        if pd.notna(gaps):
            items += [_REASONS[g] for g in gaps.split(";")]
        reasons.append(";".join(items) if items else pd.NA)
    frame["exclusion_reasons"] = pd.array(reasons, dtype="string")
    frame["population_status"] = pd.array([EXCLUDED if pd.notna(r) else IN_POPULATION for r in reasons], dtype="string")
    frame["n_exclusion_reasons"] = pd.array([len(r.split(";")) if pd.notna(r) else 0 for r in reasons], dtype="Int64")

    frame["assumed_initial_inventory"] = inventory["stock"]
    frame["min_parameter_unverified"] = inventory["min_qty"]
    frame["max_parameter_unverified"] = inventory["max_qty"]
    frame["lead_proxy_median_days__original_rows"] = inventory[f"promised_interval_days_median__{ORIGINAL}"]
    frame["lead_proxy_median_days__exact_distinct_rows"] = inventory[f"promised_interval_days_median__{DISTINCT}"]
    frame["pr_quantity_median__exact_distinct_rows"] = inventory[f"pr_quantity_median__{DISTINCT}"]
    frame["active_months"] = inventory["months_with_issue"]
    frame["lines__scenario_a"] = inventory[f"n_issue_lines__{SCENARIO_A}"]
    frame["lines__scenario_b"] = inventory[f"n_issue_lines__{SCENARIO_B}"]
    frame["qty_total__scenario_a"] = inventory[f"qty_issued_total__{SCENARIO_A}"]
    frame["qty_total__scenario_b"] = inventory[f"qty_issued_total__{SCENARIO_B}"]
    frame["demand_materially_affected"] = inventory["demand_materially_affected"]
    frame["has_line_at_repeated_unit_peak"] = inventory["n_lines_at_repeated_unit_maximum"] > 0

    lead = supplier_distinct[["material_no", "n_lines_used_for_promised_interval", "promised_interval_days_p90"]].rename(
        columns={"n_lines_used_for_promised_interval": "lead_observations_distinct", "promised_interval_days_p90": "lead_proxy_p90_days__exact_distinct_rows"})
    frame = audited_lookup(frame, lead, "material_no", "simulation_population -> supplier material", audit_log)
    line_peak = summary_b[["material_no", "max_line_qty"]].rename(columns={"max_line_qty": "max_line_qty__scenario_a"})
    frame = audited_lookup(frame, line_peak, "material_no", "simulation_population -> demand summary", audit_log)

    frame["demand_evidence_tier"] = _tier_demand(frame["active_months"])
    frame["lead_evidence_tier"] = _tier_lead(frame["lead_observations_distinct"])
    frame["resampling_allowed_demand"] = (frame["demand_evidence_tier"] == DEMAND_RESAMPLE).astype("boolean")
    frame["resampling_allowed_lead"] = (frame["lead_evidence_tier"] == LEAD_RESAMPLE).astype("boolean")
    frame["resampling_allowed_both"] = frame["resampling_allowed_demand"] & frame["resampling_allowed_lead"]
    frame["scenarios_identical_by_construction"] = (frame["qty_total__scenario_a"] == frame["qty_total__scenario_b"]) & (frame["lines__scenario_a"] == frame["lines__scenario_b"])

    initial, low, high = (frame[c].astype("Float64") for c in ("assumed_initial_inventory", "min_parameter_unverified", "max_parameter_unverified"))
    frame["at_or_below_min_at_start"] = initial <= low
    for scenario in (SCENARIO_A, SCENARIO_B):
        total = frame[f"qty_total__{scenario}"].astype("Float64")
        frame[f"stays_above_min__{scenario}"] = (initial - total) > low
        frame[f"initial_inventory_covers_all_issues__{scenario}"] = initial >= total
    frame["single_line_exceeds_max"] = frame["max_line_qty__scenario_a"].astype("Float64") > high
    frame["median_pr_quantity_exceeds_max"] = frame["pr_quantity_median__exact_distinct_rows"].astype("Float64") > high
    frame["stock_above_max"] = initial > high
    frame["lead_proxy_exceeds_horizon"] = frame["lead_proxy_median_days__exact_distinct_rows"].astype("Float64") > HORIZON_DAYS
    return frame[list(DESCRIPTIONS)]


def population_funnel(population: pd.DataFrame) -> pd.DataFrame:
    """Exclusion combinations by MRP type. Every material appears in exactly one row."""
    frame = population.assign(reasons=population["exclusion_reasons"].fillna("none, in population"), mrp=population["mrp_type"].astype("string"))
    table = frame.groupby(["mrp", "reasons"]).size().reset_index(name="materials")
    return table.sort_values(["mrp", "materials"], ascending=[False, False]).reset_index(drop=True)


def single_reason_candidates(population: pd.DataFrame) -> pd.DataFrame:
    """Stock Items excluded for one reason only. These could join later if that input were supplied."""
    frame = population[(population["mrp_type"].astype("string") == "Stock Item") & (population["n_exclusion_reasons"] == 1)]
    return frame.groupby("exclusion_reasons").size().reset_index(name="materials")


def evidence_tiers(population: pd.DataFrame) -> pd.DataFrame:
    frame = population[population["population_status"] == IN_POPULATION]
    return pd.crosstab(frame["demand_evidence_tier"], frame["lead_evidence_tier"], margins=True, margins_name="total").reset_index()


def threshold_sensitivity(population: pd.DataFrame) -> pd.DataFrame:
    """Materials allowed to resample demand and lead together, under other evidence thresholds."""
    frame = population[population["population_status"] == IN_POPULATION]
    rows = []
    for months in (3, 6, 9, 12):
        for lines in (5, 10, 20):
            rows.append({"min_active_months": months, "min_lead_observations": lines, "materials": int(((frame["active_months"] >= months) & (frame["lead_observations_distinct"] >= lines)).sum())})
    return pd.DataFrame(rows)


def pre_analysis_summary(population: pd.DataFrame) -> pd.DataFrame:
    """Counts of arithmetic and observed conditions in the population. None is a simulated result."""
    frame = population[population["population_status"] == IN_POPULATION]
    def count(mask) -> int:
        return int(mask.fillna(False).astype(bool).sum())
    can_trigger_a = ~frame[f"stays_above_min__{SCENARIO_A}"].fillna(False).astype(bool)
    differs = ~frame["scenarios_identical_by_construction"].fillna(False).astype(bool)
    affected = frame["demand_materially_affected"].fillna(False).astype(bool)
    rows = [
        ("population", "Materials in the population", len(frame)),
        ("scenario", "Scenarios A and B identical by construction", count(frame["scenarios_identical_by_construction"])),
        ("scenario", "Scenarios A and B differ", int(differs.sum())),
        ("scenario", "Materially affected by the scenario choice", int(affected.sum())),
        ("scenario", "Scenarios differ, and an order could be triggered in Scenario A", int((differs & can_trigger_a).sum())),
        ("scenario", "Materially affected, and an order could be triggered in Scenario A", int((affected & can_trigger_a).sum())),
        ("scenario", "Scenario choice changes whether Min is ever reached", int((frame[f"stays_above_min__{SCENARIO_A}"] != frame[f"stays_above_min__{SCENARIO_B}"]).sum())),
        ("reference reading", "At or below Min on day 0, so an order is triggered at once", count(frame["at_or_below_min_at_start"])),
        ("reference reading", "Never reaches Min in Scenario A, so no order is ever triggered", count(frame[f"stays_above_min__{SCENARIO_A}"])),
        ("reference reading", "Never reaches Min in Scenario B, so no order is ever triggered", count(frame[f"stays_above_min__{SCENARIO_B}"])),
        ("reference reading", "Initial inventory covers all issues in Scenario A", count(frame[f"initial_inventory_covers_all_issues__{SCENARIO_A}"])),
        ("reference reading", "Initial inventory covers all issues in Scenario B", count(frame[f"initial_inventory_covers_all_issues__{SCENARIO_B}"])),
        ("parameter conflict", "One issue line larger than Max", count(frame["single_line_exceeds_max"])),
        ("parameter conflict", "Median PR quantity larger than Max", count(frame["median_pr_quantity_exceeds_max"])),
        ("parameter conflict", "Stock above Max", count(frame["stock_above_max"])),
        ("parameter conflict", "Any of the three conflicts above", int((frame["single_line_exceeds_max"].fillna(False) | frame["median_pr_quantity_exceeds_max"].fillna(False) | frame["stock_above_max"].fillna(False)).sum())),
        ("initial inventory", "Stock of zero, so scaling the initial inventory has no effect", int((frame["assumed_initial_inventory"] == 0).sum())),
        ("lead proxy", f"Median lead proxy longer than the {HORIZON_DAYS}-day horizon", count(frame["lead_proxy_exceeds_horizon"])),
        ("demand evidence", "Resampling allowed for demand", count(frame["resampling_allowed_demand"])),
        ("demand evidence", "One active month only", int((frame["active_months"] == 1).sum())),
        ("demand evidence", "One issue line only, in Scenario A", int((frame["lines__scenario_a"] == 1).sum())),
        ("lead evidence", "Resampling allowed for the lead proxy", count(frame["resampling_allowed_lead"])),
        ("combined", "Resampling allowed for both", count(frame["resampling_allowed_both"])),
        ("combined", "Resampling allowed for both, and an order could be triggered in Scenario A", int((frame["resampling_allowed_both"].fillna(False).astype(bool) & can_trigger_a).sum())),
        ("other", "Has a line at a repeated unit peak", count(frame["has_line_at_repeated_unit_peak"])),
    ]
    return pd.DataFrame(rows, columns=["topic", "condition", "materials"])


def demand_coverage(classification: pd.DataFrame, population: pd.DataFrame) -> pd.DataFrame:
    """Share of issues the population covers, within each unit, in Scenario A."""
    members = set(population.loc[population["population_status"] == IN_POPULATION, "material_no"])
    rows = classification[classification["in_scenario_a"].fillna(False).astype(bool)].astype({"unit": "string"})
    inside = rows["material_no"].isin(members)
    table = pd.DataFrame({"lines_total": rows.groupby("unit").size(), "lines_in_population": rows[inside].groupby("unit").size(), "qty_total": rows.groupby("unit")["quantity"].sum(), "qty_in_population": rows[inside].groupby("unit")["quantity"].sum()}).fillna(0)
    table["qty_share_pct"] = (100 * table["qty_in_population"].astype("float64") / table["qty_total"].astype("float64")).round(2)
    return table.astype({"lines_total": "Int64", "lines_in_population": "Int64", "qty_total": "Int64", "qty_in_population": "Int64"}).reset_index()


def monthly_demand_shape(classification: pd.DataFrame, population: pd.DataFrame) -> pd.DataFrame:
    """Issue lines per month in the population, to judge whether months can be treated as interchangeable."""
    members = set(population.loc[population["population_status"] == IN_POPULATION, "material_no"])
    rows = classification[classification["material_no"].isin(members)]
    a = rows[rows["in_scenario_a"].fillna(False).astype(bool)].groupby("posting_month").size()
    b = rows[rows["in_scenario_b"].fillna(False).astype(bool)].groupby("posting_month").size()
    return pd.DataFrame({"lines__scenario_a": a, "lines__scenario_b": b}).reset_index().rename(columns={"posting_month": "month"})


def parameter_plausibility(inventory: pd.DataFrame, population: pd.DataFrame, supplier_distinct: pd.DataFrame) -> pd.DataFrame:
    """Observed evidence on whether Min and Max behave like a reorder level and an order-up-to level."""
    members = population.loc[population["population_status"] == IN_POPULATION, "material_no"]
    frame = inventory[inventory["material_no"].isin(members)].set_index("material_no").sort_index()
    supplier = supplier_distinct.set_index("material_no").loc[frame.index]
    low, high = frame["min_qty"].astype("float64"), frame["max_qty"].astype("float64")
    mean_month, lead = frame[f"mean_monthly_qty__{SCENARIO_A}"].astype("float64"), frame[f"promised_interval_days_median__{DISTINCT}"].astype("float64")
    lead_demand = mean_month * lead / 30.4375
    issued = frame[f"qty_issued_total__{SCENARIO_A}"].astype("float64")
    pr_ratio = supplier["pr_quantity_total"].astype("float64") / issued
    ratio = (high / low).round(6)
    rows = [("Max is exactly 2 times Min", int((ratio == 2).sum())), ("Max is exactly 3 times Min", int((ratio == 3).sum())), ("Min is at or above mean Scenario A demand during the median lead proxy", int((low >= lead_demand).sum())),
            ("PR quantity on exact_distinct_rows exceeds Scenario A issues", int((pr_ratio > 1).sum())), ("Median ratio of PR quantity to Scenario A issues, as a value", round(float(pr_ratio.median()), 3)),
            ("Median of Min", float(low.median())), ("Median of Max", float(high.median()))]
    return pd.DataFrame(rows, columns=["measure", "value"])


def lead_proxy_associations(line_distinct: pd.DataFrame, population: pd.DataFrame) -> pd.DataFrame:
    """Does the promised interval relate to order size or date? Independence would otherwise be assumed."""
    from scipy import stats
    members = set(population.loc[population["population_status"] == IN_POPULATION, "material_no"])
    rows = line_distinct[line_distinct["material_no"].isin(members) & ~line_distinct["flag_promise_before_pr"].fillna(False).astype(bool)]
    results = []
    for label, part, other in (("PR quantity, unit EA", rows[rows["unit"].astype("string") == "EA"], "pr_quantity"), ("PR date, all units", rows.assign(_date=rows["pr_date"].map(pd.Timestamp.toordinal)), "_date")):
        test = stats.spearmanr(part["promised_interval_days"].astype("float64"), part[other].astype("float64"))
        results.append({"promised_interval_against": label, "lines": len(part), "spearman_rho": round(float(test.statistic), 4), "p_value": float(f"{test.pvalue:.4g}")})
    return pd.DataFrame(results)


def demand_timing(classification: pd.DataFrame, population: pd.DataFrame) -> pd.DataFrame:
    """Timing facts that decide the time step and whether months are interchangeable."""
    members = set(population.loc[population["population_status"] == IN_POPULATION, "material_no"])
    rows = classification[classification["material_no"].isin(members) & classification["in_scenario_a"].fillna(False).astype(bool)]
    months = rows.groupby("posting_month").size()
    peak_months = rows["posting_month"].isin(pd.to_datetime(["2025-11-01", "2025-12-01", "2026-01-01"]))
    weekdays = rows["posting_date"].dt.dayofweek.value_counts()
    same_day = rows.groupby(["material_no", "posting_date"]).size()
    entries = [("Issue lines, Scenario A", len(rows)), ("Lowest monthly lines", int(months.min())), ("Highest monthly lines", int(months.max())), ("Share of lines in 2025-11 to 2026-01, percent", round(100 * float(peak_months.mean()), 2)),
               ("Fewest lines on one weekday", int(weekdays.min())), ("Most lines on one weekday", int(weekdays.max())), ("Lines on Saturday and Sunday", int(rows["posting_date"].dt.dayofweek.isin([5, 6]).sum())),
               ("Material-days with more than one line", int((same_day > 1).sum())), ("Material-days with an issue", len(same_day))]
    return pd.DataFrame(entries, columns=["measure", "value"])
