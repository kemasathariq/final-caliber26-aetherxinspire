"""Checks on generated outputs. Counts are recomputed from the output files and compared with the reconciled figures."""
import re

import pandas as pd

from src.simulation import settings as cfg

FORBIDDEN_COLUMN = re.compile(r"(?:saving|cost|price|amount|idr|usd|revenue|profit|roi|actual|optimal|best_)", re.I)
FORBIDDEN_TEXT = re.compile(r"\b(?:optimal|actual stockout|savings?|dead stock)\b", re.I)


def output_checks(files: dict, inputs, tier: pd.DataFrame, reps: int) -> list[dict]:
    rows = []

    def add(check, expected, actual):
        rows.append({"check_id": check, "expected": str(expected), "actual": str(actual), "status": "PASS" if expected == actual else "FAIL"})

    t = files["eng_material_tier.csv"]
    add("tier_t1", 5551, int((t.tier == "T1").sum()))
    add("tier_t2", 1265, int((t.tier == "T2").sum()))
    add("tier_t3", 665, int((t.tier == "T3").sum()))
    add("issued_materials", 1930, int((t.active_months > 0).sum()))
    add("class_d0", 5551, int((t.demand_class == "D0").sum()))
    add("class_d1", 1475, int((t.demand_class == "D1").sum()))
    add("class_d2", 159, int((t.demand_class == "D2").sum()))
    add("class_d3_d4", 296, int(t.demand_class.isin(["D3", "D4"]).sum()))
    add("grade_a_in_t3", 228, int(((t.tier == "T3") & (t.active_months >= 6)).sum()))
    add("forecast_eligible_outside_t3", 68, int(((t.tier != "T3") & (t.active_months >= 6)).sum()))
    add("grade_b", 437, int((t.policy_grade == "B").sum()))

    f = files["eng_forecast.csv"]
    monthly = f[f.horizon_basis == "next_month_rate"]
    add("forecast_every_material_each_scenario", 7481 * 2, len(monthly))
    add("forecast_quantity_only_where_eligible", 0, int((monthly.forecast_quantity.notna() & ~monthly.forecast_eligible).sum()))
    add("forecast_eligible_materials", 296, monthly[monthly.forecast_eligible].material_no.nunique())
    add("abstaining_rows_have_reason", 0, int((~monthly.forecast_eligible & monthly.abstain_reason.isna()).sum()))
    add("d0_d1_have_no_number", 0, int(monthly[monthly.demand_class.isin(["D0", "D1"])][["forecast_quantity", "rate_low", "rate_high"]].notna().any(axis=1).sum()))

    p = files["eng_proposed_parameters.csv"]
    add("proposed_parameter_materials", 228, p.material_no.nunique())
    add("proposed_parameter_rows", 228 * 4 * 3, len(p))
    add("no_parameter_for_grade_b", 0, int(p.material_no.isin(t[t.policy_grade == "B"].material_no).sum()))
    add("proposed_S_above_s", 0, int((p.proposed_S <= p.proposed_s).sum()))
    add("safety_stock_not_negative", 0, int((p.safety_stock < 0).sum()))

    r = files["eng_scenario_result.csv"]
    add("r0_rows", 2660, int(((r.run_set == "R0") & (r.policy == "R0")).sum()))
    add("every_result_has_label", 0, int(r[["run_id", "output_class", "result_type", "scenario_id"]].isna().any(axis=1).sum()))
    mc = r[r.result_type == "simulation"]
    add("mc_d_only_grade_a", 0, int((~mc[mc.run_set == "MC-D"].material_no.isin(inputs.grade_a)).sum()))
    lead_ok = inputs.t3.index[inputs.t3.lead_observations_distinct >= cfg.MIN_LEAD_OBSERVATIONS]
    add("mc_l_only_lead_eligible", 0, int((~mc[mc.run_set == "MC-L"].material_no.isin(lead_ok)).sum()))
    add("mc_j_materials", 139, mc[mc.run_set == "MC-J"].material_no.nunique())
    add("mc_d_materials", 228, mc[mc.run_set == "MC-D"].material_no.nunique())
    add("mc_l_materials", 140, mc[mc.run_set == "MC-L"].material_no.nunique())
    add("mc_replications_recorded", 0, int((mc.n_replications != reps).sum()))
    identical = inputs.t3.index[inputs.t3.scenarios_identical_by_construction]
    d = mc[(mc.run_set == "MC-D") & mc.material_no.isin(identical)]
    a = d[d.demand_scenario == "A"].set_index(["material_no", "pr_view", "policy"]).sort_index()[["shortfall_probability", "mean_on_hand", "expected_unmet_qty"]]
    b = d[d.demand_scenario == "B"].set_index(["material_no", "pr_view", "policy"]).sort_index()[["shortfall_probability", "mean_on_hand", "expected_unmet_qty"]]
    add("common_random_numbers_identical_materials", 0, int((a != b).any(axis=1).sum()))

    rec = files["eng_recommendation.csv"]
    add("recommendation_every_material", 7481, rec.material_no.nunique())
    add("grade_a_four_scenarios", 228 * 4, int((rec.demand_scenario != "ALL").sum()))
    add("recommended_action_enum", 0, int((~rec.recommended_action.isin(["REORDER", "HOLD", "REDUCE", "MONITOR", "NO_ACTION_EVIDENCE"])).sum()))
    add("grade_b_never_reorder_reduce_hold", 0, int((rec.material_no.isin(t[t.policy_grade != "A"].material_no) & rec.recommended_action.isin(["REORDER", "REDUCE", "HOLD"])).sum()))
    add("recommendation_has_reason_and_limits", 0, int(rec[["reason", "reason_codes", "limitations", "trigger_condition", "supporting_metrics"]].isna().any(axis=1).sum()))

    flags = files["eng_health_flags.csv"]
    add("flags_every_material", 7481, len(flags))
    add("obsolete_candidate_implies_non_moving", 0, int((flags.flag_potentially_obsolete_candidate & ~flags.flag_non_moving_by_recorded_issues).sum()))
    add("no_stock_never_flagged_slow", 0, int((~flags.flag_stock_held & flags.flag_slow_moving_by_recorded_issues).sum()))

    for name, frame in files.items():
        if name == "eng_supply_context.csv":
            bad = [c for c in frame.columns if FORBIDDEN_COLUMN.search(c) and c not in ("currency",)]
        else:
            bad = [c for c in frame.columns if FORBIDDEN_COLUMN.search(c)]
        add(f"no_money_or_actual_column_{name}", "[]", str(bad))
    for name in ("eng_recommendation.csv", "eng_health_flags.csv"):
        frame = files[name]
        hits = 0
        for column in frame.select_dtypes(include=["object", "string"]).columns:
            hits += int(frame[column].dropna().astype(str).str.contains(FORBIDDEN_TEXT).sum())
        add(f"forbidden_wording_{name}", 0, hits)
    supply = files["eng_supply_context.csv"]
    add("supply_context_views", 2500, len(supply))
    add("supply_context_never_totals_currency", 0, int(supply.currency.isna().sum()))
    k = files["eng_kpi_summary.csv"]
    add("financial_kpis_not_computed", 4, int(((k.dimension == "financial_impact") & (k.status == "NOT_COMPUTED")).sum()))
    add("financial_kpis_have_no_value", 0, int(k[k.dimension == "financial_impact"].value.notna().sum()))
    add("kpi_formula_and_population_present", 0, int(k[["formula", "population", "source", "interpretation", "limitations"]].isna().any(axis=1).sum()))
    return rows
