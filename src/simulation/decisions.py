"""Health flags, recommended action, capability output and explanation facts. Rule tables: INVENTORY_OPTIMISATION_METHODOLOGY section 5, blueprint section 12.2 (D-25).

Deterministic rules. Thresholds are analyst-selected and live in settings. Every action is a candidate needing human review. No action comes from a cost saving.
Wording rule (D-21): recorded non-movement is never an obsolescence determination, and low consumption alone is never excess.
"""
import json

import numpy as np
import pandas as pd

from src.simulation import settings as cfg

LIMITATIONS_ALL = ["stock_undated", "issues_not_proven_demand", "synthetic_dataset"]
ACTION_LABEL = {"REORDER": "Reorder", "HOLD": "Maintain", "REDUCE": "Reduce", "MONITOR": "Monitor", "NO_ACTION_EVIDENCE": "No action: insufficient evidence"}
VIEW_NAME = {"OR": "original_rows", "ED": "exact_distinct_rows"}


def plan_locations(conformed_dir=None) -> set:
    path = (conformed_dir or (cfg.PROCESSED_DIR.parent / "interim" / "conformed")) / "fact_plan_item.csv"
    return set(pd.read_csv(path, usecols=["functional_location"], dtype="string").functional_location.dropna())


def material_plan_link(plan_fl: set, conformed_dir=None) -> pd.Series:
    """True when any BoM location of the material has a recorded maintenance plan. Plans do not state their parts, so this is only a location link."""
    path = (conformed_dir or (cfg.PROCESSED_DIR.parent / "interim" / "conformed")) / "bridge_fl_material.csv"
    bridge = pd.read_csv(path, usecols=["functional_location", "material_no"], dtype="string")
    bridge["linked"] = bridge.functional_location.isin(plan_fl)
    return bridge.groupby("material_no").linked.any()


def build_health_flags(inputs, tier: pd.DataFrame, mc_r1: pd.DataFrame, r0: pd.DataFrame, proposed: pd.DataFrame, plan_link: pd.Series, run_id: str) -> pd.DataFrame:
    inv = inputs.inventory.loc[tier.index]
    f = pd.DataFrame(index=tier.index)
    f["run_id"] = run_id
    f["tier"], f["policy_grade"], f["demand_class"], f["unit"], f["active_months"] = tier.tier, tier.policy_grade, tier.demand_class, tier.unit, tier.active_months
    f["recorded_stock_undated"], f["recorded_min"], f["recorded_max"] = inv.stock, inv.min_qty, inv.max_qty
    f["first_issue_date"], f["last_issue_date"] = inv.first_issue_date, inv.last_issue_date
    last = pd.to_datetime(inv.last_issue_date)
    f["days_since_last_issue_at_window_end"] = (pd.Timestamp(cfg.HORIZON[1]) - last).dt.days
    held = inv.stock > 0
    f["flag_stock_held"] = held
    f["flag_stock_at_or_below_recorded_min"] = (inv.stock <= inv.min_qty) & (inv.min_qty > 0)
    f["flag_stock_above_recorded_max"] = (inv.stock > inv.max_qty) & (inv.max_qty > 0)
    f["flag_stock_held_with_zero_max"] = held & (inv.max_qty == 0)

    active = tier.active_months
    few_months = (active >= 1) & (active <= cfg.SLOW_MAX_ACTIVE_MONTHS)
    quiet = (active >= 1) & (last < pd.Timestamp(cfg.SLOW_LAST_ISSUE_BEFORE))
    f["flag_slow_moving_by_recorded_issues"] = held & (few_months | quiet)
    f["slow_moving_basis"] = np.select([held & few_months & quiet, held & few_months, held & quiet], ["few_active_months;no_issue_last_6_months", "few_active_months", "no_issue_last_6_months"], "")
    f["slow_moving_basis"] = f.slow_moving_basis.replace("", pd.NA)
    f["flag_non_moving_by_recorded_issues"] = held & (active == 0)
    linked = plan_link.reindex(tier.index)
    f["has_plan_link_at_bom_locations"] = linked.astype("boolean")
    f["n_bom_locations"] = inv.n_bom_locations
    f["flag_potentially_obsolete_candidate"] = held & (active == 0) & (linked.fillna(False) == False)  # noqa: E712. Hypothesis wording only (D-21).
    f["flag_outlier_review"] = tier.flag_outlier_review

    grouped = mc_r1.groupby("material_no")
    f["shortfall_probability_min"] = grouped.shortfall_probability.min().reindex(tier.index)
    f["shortfall_probability_max"] = grouped.shortfall_probability.max().reindex(tier.index)
    f["shortfall_probability_after_first_arrival_max"] = grouped.shortfall_probability_after_first_arrival.max().reindex(tier.index)
    f["replay_any_shortfall"] = r0.groupby("material_no").any_shortfall.any().reindex(tier.index).astype("boolean")
    worst = f.shortfall_probability_max
    f["stockout_risk_level"] = np.select([worst >= cfg.RISK_HIGH, worst >= cfg.RISK_MEDIUM, worst.notna()], ["High", "Medium", "Low"], "Not assessed")
    f["stockout_risk_basis"] = np.select([worst.notna(), f.replay_any_shortfall.fillna(False).astype(bool) | (tier.tier == "T3")], ["simulated_mc_d_policy_r1_worst_of_four_scenarios", "deterministic_replay_only_grade_b"], "not_assessed_outside_simulation_population")

    x2 = proposed[proposed.policy == cfg.REFERENCE_SERVICE_POLICY]
    above = x2.assign(above=x2.recorded_stock_undated > x2.proposed_S).groupby("material_no").above.agg(["sum", "count"]).reindex(tier.index)
    share = (grouped.days_above_recorded_max.max() / cfg.HORIZON_DAYS).reindex(tier.index)
    f["days_above_recorded_max_share_max"] = share.round(6)
    f["stock_above_proposed_S_scenarios"] = above["sum"]
    f["overstock_risk_level"] = np.select([above["sum"] == above["count"], (above["sum"] > 0) | (share > cfg.REDUCE_DAYS_ABOVE_MAX_SHARE), above["count"].notna()], ["High", "Medium", "Low"], "Not assessed")
    f.loc[above["count"].isna(), "overstock_risk_level"] = "Not assessed"
    f["overstock_risk_basis"] = np.where(above["count"].notna(), "simulated_and_proposed_S_grade_a", np.where(f.flag_stock_above_recorded_max, "recorded_stock_above_recorded_max_descriptive_only", "not_assessed"))
    f["wording_note"] = "Flags describe recorded issues and undated recorded stock. Non-movement is not an obsolescence determination. Obsolete candidate is a hypothesis needing lifecycle data."
    f["output_class"] = "rule_derived"
    return f.reset_index()


def _risk_from_probability(p) -> str:
    if p is None or pd.isna(p):
        return "Not assessed"
    return "High" if p >= cfg.RISK_HIGH else "Medium" if p >= cfg.RISK_MEDIUM else "Low"


def action_for_grade_a(stock: float, s: int, S: int, shortfall: float, days_above_share: float) -> tuple[str, str, str]:
    """Rows 1 to 3 of the rule table. Returns action, reason codes, trigger text."""
    if stock <= s and shortfall > cfg.REORDER_SHORTFALL_THRESHOLD:
        return "REORDER", "stock_at_or_below_proposed_s;shortfall_probability_above_threshold", f"recorded stock {stock:g} <= proposed s {s:g} and simulated shortfall probability {shortfall:.3f} > {cfg.REORDER_SHORTFALL_THRESHOLD}"
    if stock > S or days_above_share > cfg.REDUCE_DAYS_ABOVE_MAX_SHARE:
        codes = ";".join(c for c, on in (("stock_above_proposed_S", stock > S), ("days_above_recorded_max_above_threshold", days_above_share > cfg.REDUCE_DAYS_ABOVE_MAX_SHARE)) if on)
        return "REDUCE", codes, f"recorded stock {stock:g} vs proposed S {S:g}; simulated share of days above recorded Max {days_above_share:.3f} vs threshold {cfg.REDUCE_DAYS_ABOVE_MAX_SHARE}"
    return "HOLD", "within_proposed_range_or_low_simulated_shortfall", f"recorded stock {stock:g}, proposed s {s:g}, proposed S {S:g}, simulated shortfall probability {shortfall:.3f}"


def build_recommendations(inputs, tier, flags, mc_r1, proposed, quantile_accepted: bool, held_out: pd.DataFrame, run_id: str) -> pd.DataFrame:
    """Grain: material and scenario. Grade A has one row per demand scenario and view. Every other material has one scenario-independent row."""
    flags_i = flags.set_index("material_no")
    pop = inputs.population
    rows = []
    key_mc = mc_r1.set_index(["material_no", "demand_scenario", "pr_view"])
    key_p = proposed.set_index(["material_no", "demand_scenario", "pr_view", "policy"])
    ho = held_out[(held_out.config_id == "K30") & (held_out.policy.isin(["R0", cfg.REFERENCE_SERVICE_POLICY]))]
    key_ho = {(r.material_no, r.demand_scenario, r.pr_view, r.policy): r.any_shortfall for r in ho.itertuples()}
    for material, f in flags_i.iterrows():
        base_lim = list(LIMITATIONS_ALL)
        if pd.notna(f.policy_grade) and f.policy_grade == "A":
            popr = pop.loc[material]
            for demand in cfg.DEMAND_SCENARIOS:
                for view in cfg.PR_VIEWS:
                    mc = key_mc.loc[(material, demand, view)]
                    stock = float(f.recorded_stock_undated)
                    share = float(mc.days_above_recorded_max) / cfg.HORIZON_DAYS
                    by_level = {}
                    for code in cfg.SERVICE_LEVELS:
                        p = key_p.loc[(material, demand, view, code)]
                        by_level[code] = (*action_for_grade_a(stock, int(p.proposed_s), int(p.proposed_S), float(mc.shortfall_probability), share), p)
                    action, codes, trigger, p = by_level[cfg.REFERENCE_SERVICE_POLICY]
                    lim = base_lim + ["min_max_meaning_unverified", "promised_interval_not_goods_receipt_lead_time"]
                    if not quantile_accepted:
                        lim.append("quantile_method_failed_preregistered_pinball_rule")
                    if popr.single_line_exceeds_max or popr.median_pr_quantity_exceeds_max or popr.stock_above_max:
                        lim.append("recorded_values_conflict_with_order_up_to_reading")
                    if popr.at_or_below_min_at_start:
                        lim.append("early_shortfall_driven_by_assumed_opening_stock")
                    if f.flag_outlier_review:
                        lim.append("outlier_review_required")
                    if popr.demand_materially_affected:
                        lim.append("scenario_a_b_materially_different")
                    metrics = {"recorded_stock_undated": stock, "recorded_min": float(f.recorded_min), "recorded_max": float(f.recorded_max), "proposed_s": int(p.proposed_s), "proposed_S": int(p.proposed_S), "proposed_Q": int(p.proposed_Q), "safety_stock": float(p.safety_stock),
                               "lead_time_demand_mean": float(p.lead_time_demand_mean), "shortfall_probability_policy_r1": float(mc.shortfall_probability), "shortfall_probability_after_first_arrival": float(mc.shortfall_probability_after_first_arrival),
                               "days_above_recorded_max_share": round(share, 6), "held_out_r0_any_shortfall": _opt(key_ho.get((material, demand, view, "R0"))), "held_out_x2_any_shortfall": _opt(key_ho.get((material, demand, view, cfg.REFERENCE_SERVICE_POLICY)))}
                    rows.append({"run_id": run_id, "material_no": material, "scenario_id": cfg.scenario_id(demand, view, cfg.REFERENCE_SERVICE_POLICY, "BO", "K20"), "demand_scenario": demand, "pr_view": view, "service_level_reference": cfg.SERVICE_LEVELS[cfg.REFERENCE_SERVICE_POLICY],
                                 "recommended_action": action, "action_label": ACTION_LABEL[action], "action_at_90": by_level["X1"][0], "action_at_98": by_level["X3"][0], "risk_level": _risk_from_probability(mc.shortfall_probability) if action != "REDUCE" else f.overstock_risk_level,
                                 "evidence_class": tier.loc[material, "evidence_subtier"], "confidence": tier.loc[material, "confidence"], "reason_codes": codes, "reason": _reason(action), "trigger_condition": trigger, "supporting_metrics": json.dumps(metrics, sort_keys=True),
                                 "proposed_s": int(p.proposed_s), "proposed_S": int(p.proposed_S), "proposed_Q": int(p.proposed_Q), "safety_stock": float(p.safety_stock), "recorded_min": f.recorded_min, "recorded_max": f.recorded_max, "recorded_stock_undated": stock, "unit": f.unit,
                                 "limitations": ";".join(lim), "requires_review": True, "method_class": "deterministic_rule_on_simulation", "output_class": "rule_derived"})
        else:
            codes = [c for c, on in (("slow_moving_by_recorded_issues", f.flag_slow_moving_by_recorded_issues), ("non_moving_by_recorded_issues", f.flag_non_moving_by_recorded_issues), ("potentially_obsolete_candidate", f.flag_potentially_obsolete_candidate), ("outlier_review", f.flag_outlier_review)) if on]
            action = "MONITOR" if codes else "NO_ACTION_EVIDENCE"
            reason_code = ";".join(codes) if codes else (f"{tier.loc[material, 'abstain_reason']}" if pd.notna(tier.loc[material, "abstain_reason"]) else "grade_b_or_not_simulated_no_flag")
            metrics = {"recorded_stock_undated": _opt(f.recorded_stock_undated), "recorded_min": _opt(f.recorded_min), "recorded_max": _opt(f.recorded_max), "active_months": int(f.active_months), "days_since_last_issue_at_window_end": _opt(f.days_since_last_issue_at_window_end), "replay_any_shortfall": _opt(f.replay_any_shortfall)}
            rows.append({"run_id": run_id, "material_no": material, "scenario_id": "SC-ALL-NA-NA-NA-K0", "demand_scenario": "ALL", "pr_view": "ALL", "service_level_reference": None, "recommended_action": action, "action_label": ACTION_LABEL[action], "action_at_90": None, "action_at_98": None,
                         "risk_level": "Not assessed", "evidence_class": tier.loc[material, "evidence_subtier"], "confidence": tier.loc[material, "confidence"], "reason_codes": reason_code, "reason": _reason(action), "trigger_condition": "; ".join(codes) if codes else "no flag raised and evidence below the minimum for a parameter", "supporting_metrics": json.dumps(metrics, sort_keys=True),
                         "proposed_s": None, "proposed_S": None, "proposed_Q": None, "safety_stock": None, "recorded_min": f.recorded_min, "recorded_max": f.recorded_max, "recorded_stock_undated": f.recorded_stock_undated, "unit": f.unit,
                         "limitations": ";".join(base_lim + ["no_proposed_parameter_d24"]), "requires_review": action == "MONITOR", "method_class": "deterministic_rule", "output_class": "rule_derived"})
    frame = pd.DataFrame(rows)
    groups = frame.groupby("material_no").recommended_action
    unique = groups.nunique()
    first = groups.first()
    frame["consensus_status"] = frame.material_no.map(unique).map(lambda n: "all_scenarios_agree" if n == 1 else "scenario_dependent")
    frame["consensus_action"] = frame.material_no.map(first.where(unique == 1))
    return frame


def _opt(value):
    if value is None or value is pd.NA or (isinstance(value, float) and np.isnan(value)):
        return None
    if isinstance(value, (bool, np.bool_)):
        return bool(value)
    return float(value)


def _reason(action: str) -> str:
    return {
        "REORDER": "Candidate: recorded stock sits at or below the proposed reorder point, and resampled history under the recorded Min-Max reading shows shortfalls above the configured threshold.",
        "REDUCE": "Candidate for review: recorded stock is above the proposed order-up-to level, or stays above recorded Max for most of the simulated horizon. Review replenishment before any disposal decision.",
        "HOLD": "Candidate: maintain current levels. Recorded stock does not meet the reorder or reduce rule under this scenario.",
        "MONITOR": "No parameter is proposed because evidence is thin or absent. A recorded-issue flag was raised, so a planner should review it. Non-movement is not an obsolescence determination.",
        "NO_ACTION_EVIDENCE": "The system abstains. Evidence is below the minimum for a recommendation and no flag was raised.",
    }[action]


def build_capability_output(tier, flags, recommendations, proposed, mc_r1, r0, run_id) -> pd.DataFrame:
    rows = []
    f = flags.set_index("material_no")
    for r in mc_r1.itertuples():
        rows.append(dict(material_no=r.material_no, capability="stockout_risk", scenario_id=r.scenario_id, flag=_risk_from_probability(r.shortfall_probability), value_num=r.shortfall_probability, value_kind="shortfall_probability_simulated", unit="probability", confidence=tier.confidence[r.material_no], requires_review=True, reason_codes="simulated_mc_d_policy_r1", method_class="simulation", recommended_action=None))
    grade_b = r0[r0.policy_grade == "B"]
    for r in grade_b.itertuples():
        rows.append(dict(material_no=r.material_no, capability="stockout_risk", scenario_id=r.scenario_id, flag="replay_shortfall" if r.any_shortfall else "no_replay_shortfall", value_num=r.expected_unmet_qty, value_kind="replay_unmet_qty", unit=r.unit, confidence="Low", requires_review=bool(r.any_shortfall), reason_codes="deterministic_replay_only_grade_b", method_class="simulation", recommended_action=None))
    for material, x in f.iterrows():
        rows.append(dict(material_no=material, capability="overstock_risk", scenario_id="SC-ALL-NA-NA-NA-K0", flag=x.overstock_risk_level, value_num=x.recorded_stock_undated - x.recorded_max if x.flag_stock_above_recorded_max else None, value_kind="recorded_stock_minus_recorded_max", unit=x.unit, confidence=tier.confidence[material], requires_review=bool(x.flag_stock_above_recorded_max), reason_codes=x.overstock_risk_basis, method_class="deterministic_rule", recommended_action=None))
        code = "non_moving_by_recorded_issues" if x.flag_non_moving_by_recorded_issues else ("slow_moving_by_recorded_issues" if x.flag_slow_moving_by_recorded_issues else "not_flagged")
        rows.append(dict(material_no=material, capability="slow_moving", scenario_id="SC-ALL-NA-NA-NA-K0", flag=code, value_num=x.days_since_last_issue_at_window_end, value_kind="days_since_last_issue_at_window_end", unit="days", confidence=tier.confidence[material], requires_review=code != "not_flagged", reason_codes="potentially_obsolete_candidate" if x.flag_potentially_obsolete_candidate else code, method_class="deterministic_rule", recommended_action=None))
    for r in recommendations.itertuples():
        rows.append(dict(material_no=r.material_no, capability="reorder", scenario_id=r.scenario_id, flag=r.recommended_action, value_num=r.proposed_s, value_kind="proposed_s", unit=r.unit, confidence=r.confidence, requires_review=r.requires_review, reason_codes=r.reason_codes, method_class=r.method_class, recommended_action=r.recommended_action))
    for r in proposed.itertuples():
        rows.append(dict(material_no=r.material_no, capability="dynamic_parameters", scenario_id=r.scenario_id, flag=r.parameter_status, value_num=r.proposed_s, value_kind="proposed_s", unit=r.unit, confidence=tier.confidence[r.material_no], requires_review=True, reason_codes=f"service_level_scenario_{r.service_level}", method_class="simulation_grid", recommended_action=None))
    for material in tier.index[tier.policy_grade == "A"]:
        rows.append(dict(material_no=material, capability="cost_risk", scenario_id="SC-ALL-NA-NA-NA-K0", flag="not_computed_d09_d10", value_num=None, value_kind=None, unit=None, confidence="Abstain", requires_review=False, reason_codes="no_approved_cost_set", method_class="arithmetic_blocked", recommended_action=None))
    frame = pd.DataFrame(rows)
    frame.insert(0, "run_id", run_id)
    frame["output_class"] = np.where(frame.method_class.isin(["simulation", "simulation_grid"]), "stochastic_simulation", "rule_derived")
    frame.loc[frame.value_kind == "replay_unmet_qty", "output_class"] = "deterministic_simulation"
    return frame


def build_explanation_facts(tier, flags, recommendations, proposed, run_id) -> pd.DataFrame:
    rows = []
    f = flags.set_index("material_no")

    def add(material, capability, key, value, unit, scenario, source_file, source_column):
        if value is None or (isinstance(value, float) and np.isnan(value)) or value is pd.NA:
            return
        rows.append({"run_id": run_id, "material_no": material, "fact_id": f"{material}-{len(rows)}", "capability": capability, "fact_key": key, "value": value, "unit": unit, "scenario_id": scenario, "source_file": source_file, "source_column": source_column})

    for material, x in f.iterrows():
        add(material, "all", "tier", x.tier, None, "SC-ALL-NA-NA-NA-K0", "eng_material_tier.csv", "tier")
        add(material, "all", "demand_class", x.demand_class, None, "SC-ALL-NA-NA-NA-K0", "eng_material_tier.csv", "demand_class")
        add(material, "all", "active_months", int(x.active_months), "months of 17", "SC-ALL-NA-NA-NA-K0", "eng_material_tier.csv", "active_months")
        add(material, "all", "recorded_stock_undated", x.recorded_stock_undated, x.unit, "SC-ALL-NA-NA-NA-K0", "mart_material_inventory.csv", "stock")
        add(material, "all", "recorded_min", x.recorded_min, x.unit, "SC-ALL-NA-NA-NA-K0", "mart_material_inventory.csv", "min_qty")
        add(material, "all", "recorded_max", x.recorded_max, x.unit, "SC-ALL-NA-NA-NA-K0", "mart_material_inventory.csv", "max_qty")
    for r in recommendations.itertuples():
        add(r.material_no, "reorder", "recommended_action", r.recommended_action, None, r.scenario_id, "eng_recommendation.csv", "recommended_action")
        add(r.material_no, "reorder", "trigger_condition", r.trigger_condition, None, r.scenario_id, "eng_recommendation.csv", "trigger_condition")
        add(r.material_no, "reorder", "limitations", r.limitations, None, r.scenario_id, "eng_recommendation.csv", "limitations")
    for r in proposed.itertuples():
        for key in ("proposed_s", "proposed_S", "proposed_Q", "safety_stock", "lead_time_demand_mean"):
            add(r.material_no, "dynamic_parameters", key, getattr(r, key), r.unit, r.scenario_id, "eng_proposed_parameters.csv", key)
    return pd.DataFrame(rows)


def build_supply_context(inputs, run_id) -> pd.DataFrame:
    """Thin export of procurement evidence per material and view (D-14, D-16). Promised intervals only, never goods-receipt or transport time."""
    rows = []
    cutoff = pd.Timestamp(cfg.HORIZON[1])
    for code, view in cfg.PR_VIEWS.items():
        lines = inputs.procurement[view]
        supplier = inputs.supplier[view].set_index("material_no")
        grouped = lines.groupby("material_no")
        extra = pd.DataFrame({
            "promise_gap_days_median": grouped.promise_gap_days.median(), "promised_interval_days_std": grouped.promised_interval_days.std(ddof=1).round(6),
            "n_lines_promised_before_pr": grouped.flag_promise_before_pr.sum(), "n_lines_promised_after_data_cutoff": grouped.po_delivery_date.apply(lambda s: int((s > cutoff).sum())),
            "first_pr_date": grouped.pr_date.min().dt.strftime("%Y-%m-%d"), "last_pr_date": grouped.pr_date.max().dt.strftime("%Y-%m-%d"), "pr_quantity_median": grouped.pr_quantity.median()})
        supplier_lines = grouped.supplier_code.agg(lambda s: s.value_counts(normalize=True).iloc[0]).round(6)
        for material, s in supplier.iterrows():
            e = extra.loc[material]
            p25, p75 = s.promised_interval_days_p25, s.promised_interval_days_p75
            rows.append({"run_id": run_id, "material_no": material, "pr_view": code, "supplier_code": s.supplier_code, "supplier_name": s.supplier_name, "currency": s.currency, "unit": s.unit, "n_lines": s.n_lines, "n_purchase_orders": s.n_purchase_orders, "first_pr_date": e.first_pr_date, "last_pr_date": e.last_pr_date, "pr_quantity_median": e.pr_quantity_median,
                         "promised_interval_days_min": s.promised_interval_days_min, "promised_interval_days_median": s.promised_interval_days_median, "promised_interval_days_p75": p75, "promised_interval_days_p25": p25, "promised_interval_days_p90": s.promised_interval_days_p90, "promised_interval_days_max": s.promised_interval_days_max, "promised_interval_days_iqr": round(p75 - p25, 6), "promised_interval_days_std": e.promised_interval_days_std,
                         "n_lines_used_for_promised_interval": s.n_lines_used_for_promised_interval, "requested_interval_days_median": s.requested_interval_days_median, "requested_vs_promised_gap_days_median": e.promise_gap_days_median, "n_lines_promised_after_data_cutoff": int(e.n_lines_promised_after_data_cutoff), "n_lines_promised_before_pr": int(e.n_lines_promised_before_pr), "supplier_share_of_lines": supplier_lines[material], "source_file": f"mart_supplier_material__{view}.csv; mart_procurement_line__{view}.csv", "label": "promised procurement interval, not transport or goods-receipt time", "output_class": "historical_descriptive"})
    return pd.DataFrame(rows)
