"""Portfolio KPIs and paired comparisons. No composite score, no cross-unit quantity total, no money. Financial KPIs stay NOT_COMPUTED until D-09 and D-10 close."""
import numpy as np
import pandas as pd

from src.simulation import settings as cfg

MEASURES = ["orders_placed", "expected_unmet_qty", "mean_on_hand", "sim_fill_rate_quantity", "sim_stockout_days", "sim_order_quantity_total", "sim_ending_on_hand"]


def compare_demand_scenarios(r0: pd.DataFrame, inputs) -> pd.DataFrame:
    """Design 8.4. Arithmetic differences only. Neither scenario is a baseline."""
    rows = []
    pop = inputs.t3
    group = np.where(pop.scenarios_identical_by_construction, "identical_by_construction", np.where(pop.demand_materially_affected, "materially_affected", "other_differs"))
    group = dict(zip(pop.index, group))
    keep = r0[r0.policy == "R0"].set_index(["material_no", "pr_view", "demand_scenario"]).sort_index()
    for (material, view), part in keep.groupby(level=[0, 1]):
        a, b = part.xs("A", level="demand_scenario").iloc[0], part.xs("B", level="demand_scenario").iloc[0]
        rows.append({"comparison_type": "demand_a_vs_b", "material_no": material, "pr_view": view, "demand_scenario": "A|B", "scenario_a": a.scenario_id, "scenario_b": b.scenario_id, "policy_a": "R0", "policy_b": "R0", "config_id": "K0", "group": group[material], "unit": a.unit,
                     "metric_a_fill_rate": a.sim_fill_rate_quantity, "metric_b_fill_rate": b.sim_fill_rate_quantity, "delta_unmet_qty": a.expected_unmet_qty - b.expected_unmet_qty, "delta_mean_on_hand": round(a.mean_on_hand - b.mean_on_hand, 6), "delta_orders": a.orders_placed - b.orders_placed,
                     "orders_differ": a.orders_placed != b.orders_placed, "first_order_day_differs": (a.sim_first_order_day != b.sim_first_order_day) and not (pd.isna(a.sim_first_order_day) and pd.isna(b.sim_first_order_day)), "order_quantity_differs": a.sim_order_quantity_total != b.sim_order_quantity_total, "stockout_status_differs": a.any_shortfall != b.any_shortfall, "tradeoff": None})
    return pd.DataFrame(rows)


def tradeoff(delta_unmet: float, delta_on_hand: float) -> str:
    """Availability and inventory stay separate. Delta is proposed minus recorded. Tolerance avoids labelling rounding as change."""
    u = 0 if abs(delta_unmet) < 1e-9 else np.sign(delta_unmet)
    h = 0 if abs(delta_on_hand) < 1e-9 else np.sign(delta_on_hand)
    return {(-1, -1): "less_unmet_less_inventory", (-1, 0): "less_unmet_same_inventory", (-1, 1): "less_unmet_more_inventory", (0, -1): "same_unmet_less_inventory", (0, 0): "no_change", (0, 1): "same_unmet_more_inventory", (1, -1): "more_unmet_less_inventory", (1, 0): "more_unmet_same_inventory", (1, 1): "more_unmet_more_inventory"}[(int(u), int(h))]


def compare_policies(results: pd.DataFrame, base_policy: str, comparison_type: str, policies=("R2", "N1", "X1", "X2", "X3")) -> pd.DataFrame:
    """Paired, per material, within one scenario, view and configuration, so demand path, opening stock and lead draws are shared."""
    key = ["material_no", "demand_scenario", "pr_view", "config_id"]
    base = results[results.policy == base_policy].set_index(key)
    rows = []
    for policy in policies:
        part = results[results.policy == policy].set_index(key)
        joined = part.join(base, rsuffix="_base", how="inner")
        for idx, r in joined.iterrows():
            du, dh = r.expected_unmet_qty - r.expected_unmet_qty_base, r.mean_on_hand - r.mean_on_hand_base
            rows.append({"comparison_type": comparison_type, "material_no": idx[0], "pr_view": idx[2], "demand_scenario": idx[1], "scenario_a": r.scenario_id, "scenario_b": r.scenario_id_base, "policy_a": policy, "policy_b": base_policy, "config_id": idx[3], "group": r.run_set, "unit": r.unit,
                         "metric_a_fill_rate": r.sim_fill_rate_quantity, "metric_b_fill_rate": r.sim_fill_rate_quantity_base, "delta_unmet_qty": round(du, 6), "delta_mean_on_hand": round(dh, 6), "delta_orders": round(r.orders_placed - r.orders_placed_base, 6),
                         "orders_differ": r.orders_placed != r.orders_placed_base, "first_order_day_differs": None, "order_quantity_differs": r.sim_order_quantity_total != r.sim_order_quantity_total_base, "stockout_status_differs": (r.any_shortfall != r.any_shortfall_base) if "any_shortfall" in r and pd.notna(r.get("any_shortfall")) else None, "tradeoff": tradeoff(du, dh)})
    return pd.DataFrame(rows)


def sensitivity_summary(rows: pd.DataFrame, base: pd.DataFrame) -> pd.DataFrame:
    """Design section 10. Effect of each what-if on status against the same scenario in K0 and its swing, plus the A versus B swing as the dominance check."""
    base_i = base.set_index(["material_no", "demand_scenario", "pr_view"])
    out = []
    for (k, shortage, policy), part in rows.groupby(["config_id", "unmet_rule", "policy"]):
        for (demand, view), sub in part.groupby(["demand_scenario", "pr_view"]):
            j = sub.set_index(["material_no", "demand_scenario", "pr_view"]).join(base_i, rsuffix="_base", how="inner")
            fill_swing = (j.sim_fill_rate_quantity - j.sim_fill_rate_quantity_base).abs()
            out.append({"config_id": k, "unmet_rule": shortage, "policy": policy, "demand_scenario": demand, "pr_view": view, "n_materials": len(j), "materials_with_shortage": int(j.any_shortfall.sum()), "materials_with_shortage_base": int(j.any_shortfall_base.sum()), "shortage_status_changes": int((j.any_shortfall != j.any_shortfall_base).sum()), "order_count_changes": int((j.orders_placed != j.orders_placed_base).sum()),
                        "median_abs_fill_rate_change": round(float(fill_swing.median()), 6), "mean_abs_fill_rate_change": round(float(fill_swing.mean()), 6), "p90_abs_fill_rate_change": round(float(fill_swing.quantile(0.9)), 6), "median_fill_rate": round(float(j.sim_fill_rate_quantity.median()), 6)})
    return pd.DataFrame(out)


def _kpi(store, kpi_id, dimension, name, formula, numerator, denominator, value, unit, population, n, scenario, source, interpretation, limitations, status="COMPUTED", policy=None, demand=None, view=None, run_set=None, result_type=None):
    store.append({"kpi_id": kpi_id, "dimension": dimension, "kpi_name": name, "formula": formula, "numerator": numerator, "denominator": denominator, "value": value, "unit": unit, "population": population, "population_n": n, "scenario": scenario, "demand_scenario": demand, "pr_view": view, "policy": policy, "run_set": run_set, "result_type": result_type, "source": source, "interpretation": interpretation, "limitations": limitations, "status": status})


SIM_LIMITS = "Simulated under stated assumptions. Opening stock undated, Min-Max meaning unverified, promised interval is not a lead time, issues are not proven demand. Dataset is synthetic. Never an actual stockout."


def build_kpis(results: pd.DataFrame, comparisons: pd.DataFrame, recommendations: pd.DataFrame, tier: pd.DataFrame, supply: pd.DataFrame, flags: pd.DataFrame, base_policy_by_set: dict, run_id: str) -> pd.DataFrame:
    k = []
    for (run_set, config, demand, view, policy), part in results.groupby(["run_set", "config_id", "demand_scenario", "pr_view", "policy"]):
        n = len(part)
        scen = cfg.scenario_id(demand, view, policy, "BO", config)
        rt = part.result_type.iloc[0]
        args = dict(policy=policy, demand=demand, view=view, run_set=run_set, result_type=rt)
        pop = {"R0": "T3 665" if n == 665 else "Grade A 228", "HO": f"Held-out {n}", "MC-D": f"Grade A {n}", "MC-L": f"Lead eligible {n}", "MC-J": f"Joint eligible {n}"}.get(run_set, str(n))
        src = "eng_scenario_result.csv"
        if rt != "simulation":
            shortage = int(part.any_shortfall.sum())
            _kpi(k, "AV-1", "availability", "Materials with a simulated shortage", "count(material with at least one stockout day) / materials", shortage, n, round(shortage / n, 6), "share of materials", pop, n, scen, src, "How many materials would run short if these assumptions held", SIM_LIMITS, **args)
        else:
            _kpi(k, "AV-5", "availability", "Mean simulated shortfall probability", "mean(share of replications with a stockout day)", None, n, round(float(part.shortfall_probability.mean()), 6), "probability", pop, n, scen, src, "Spread under resampling of own history. Not a future probability", SIM_LIMITS, **args)
            high = int((part.shortfall_probability >= cfg.RISK_HIGH).sum())
            _kpi(k, "AV-6", "availability", "Materials with shortfall probability at or above 0.5", "count(shortfall_probability >= 0.5) / materials", high, n, round(high / n, 6), "share of materials", pop, n, scen, src, "Materials that run short in most resampled histories", SIM_LIMITS, **args)
        fill = part.sim_fill_rate_quantity.dropna()
        _kpi(k, "AV-2", "availability", "Median quantity fill rate", "median(served on day / issues)", None, len(fill), round(float(fill.median()), 6), "ratio", pop, n, scen, src, "Service indicator. Scenario measure, not an official target", SIM_LIMITS, **args)
        at95 = int((fill >= 0.95).sum())
        _kpi(k, "AV-3", "availability", "Materials with fill rate at or above 0.95", "count(fill rate >= 0.95) / materials with issues", at95, len(fill), round(at95 / max(len(fill), 1), 6), "share of materials", pop, n, scen, src, "Service indicator", SIM_LIMITS, **args)
        ea = part[part.unit == "EA"]
        _kpi(k, "AV-4", "availability", "Unmet quantity within unit EA", "sum(quantity not served on its day), unit EA only", round(float(ea.expected_unmet_qty.sum()), 6), None, round(float(ea.expected_unmet_qty.sum()), 6), "EA", f"{pop}, unit EA", len(ea), scen, src, "Shortage size within one unit. Never totalled across units", SIM_LIMITS, **args)
        _kpi(k, "IE-1", "inventory_efficiency", "Average on-hand within unit EA", "sum(mean on-hand), unit EA only", round(float(ea.mean_on_hand.sum()), 6), None, round(float(ea.mean_on_hand.sum()), 6), "EA", f"{pop}, unit EA", len(ea), scen, src, "Inventory level. Dominated by opening stock assumed on day 0", SIM_LIMITS, **args)
        _kpi(k, "IE-2", "inventory_efficiency", "Ending on-hand within unit EA", "sum(ending on-hand), unit EA only", round(float(ea.sim_ending_on_hand.sum()), 6), None, round(float(ea.sim_ending_on_hand.sum()), 6), "EA", f"{pop}, unit EA", len(ea), scen, src, "Inventory at end of horizon", SIM_LIMITS, **args)
        above = int((part.days_above_recorded_max > 0).sum())
        _kpi(k, "IE-3", "inventory_efficiency", "Materials above recorded Max on any simulated day", "count(days above recorded Max > 0) / materials", above, n, round(above / n, 6), "share of materials", pop, n, scen, src, "Simulated overstock exposure in units. Not a value", SIM_LIMITS, **args)
        orders = float(part.orders_placed.sum())
        _kpi(k, "PE-1", "procurement_efficiency", "Replenishment orders placed", "sum(orders placed)", round(orders, 6), None, round(orders, 6), "orders", pop, n, scen, src, "Replenishment frequency. Orders are countable across units", SIM_LIMITS, **args)
        _kpi(k, "PE-2", "procurement_efficiency", "Median total ordered quantity per material within unit EA", "median(total ordered per material in the horizon), unit EA only" if rt != "simulation" else "median(mean total ordered per replication), unit EA only", None, None, round(float(ea.sim_order_quantity_total.median()), 6), "EA", f"{pop}, unit EA", len(ea), scen, src, "Order volume per material. Read with PE-1 for frequency", SIM_LIMITS, **args)

    for (ctype, config, demand, view, policy), part in comparisons[comparisons.comparison_type != "demand_a_vs_b"].groupby(["comparison_type", "config_id", "demand_scenario", "pr_view", "policy_a"]):
        n = len(part)
        scen = cfg.scenario_id(demand, view, policy, "BO", config)
        for label in sorted(part.tradeoff.unique()):
            c = int((part.tradeoff == label).sum())
            _kpi(k, "CP-1", "policy_comparison", f"Paired outcome: {label}", "count(materials in outcome) / materials, proposed minus recorded", c, n, round(c / n, 6), "share of materials", f"{ctype} {n}", n, scen, "eng_scenario_comparison.csv", "Trade-off between availability and inventory, shown without a composite", SIM_LIMITS, policy=policy, demand=demand, view=view, run_set=part["group"].iloc[0], result_type=ctype)
        ratio = part[part.delta_mean_on_hand.notna()]
        _kpi(k, "CP-2", "policy_comparison", "Median change in mean on-hand", "median(policy minus recorded), per material in its own unit", None, n, round(float(ratio.delta_mean_on_hand.median()), 6), "own unit, median of per-material differences", f"{ctype} {n}", n, scen, "eng_scenario_comparison.csv", "Inventory cost of the policy in units, not money", SIM_LIMITS, policy=policy, demand=demand, view=view, run_set=part["group"].iloc[0], result_type=ctype)

    for view, part in supply.groupby("pr_view"):
        _kpi(k, "PE-3", "procurement_efficiency", "Median spread of promised interval", "median(p75 - p25 of promised interval per material)", None, len(part), round(float(part.promised_interval_days_iqr.median()), 6), "days", f"Procured materials {len(part)}", len(part), f"PR view {view}", "eng_supply_context.csv", "Variability of promises across materials", "Promised, not achieved. No goods-receipt data exists. Synthetic data.", view=view, result_type="historical_descriptive")
        _kpi(k, "PE-4", "procurement_efficiency", "Median requested versus promised gap", "median(per-material median of promise gap)", None, len(part), round(float(part.requested_vs_promised_gap_days_median.median()), 6), "days", f"Procured materials {len(part)}", len(part), f"PR view {view}", "eng_supply_context.csv", "Gap between requested and promised dates", "Promised, not achieved. Synthetic data.", view=view, result_type="historical_descriptive")

    one = recommendations.drop_duplicates("material_no")
    total = len(one)
    for action in ["REORDER", "HOLD", "REDUCE", "MONITOR", "NO_ACTION_EVIDENCE"]:
        c = int((one.consensus_action == action).sum())
        _kpi(k, "DQ-1", "decision_quality", f"Materials with consensus action {action}", "count(all scenarios agree on action) / all materials", c, total, round(c / total, 6), "share of materials", f"All materials {total}", total, "All scenarios", "eng_recommendation.csv", "Candidates needing review. Thresholds pending D-25", "Rule output. Thresholds analyst-selected. Not an order instruction.", result_type="rule_derived")
    dep = int((one.consensus_status == "scenario_dependent").sum())
    _kpi(k, "DQ-2", "decision_quality", "Materials where the action depends on the scenario", "count(scenario_dependent) / all materials", dep, total, round(dep / total, 6), "share of materials", f"All materials {total}", total, "All scenarios", "eng_recommendation.csv", "Decisions that change with duplicates or PR PO view", "Rule output", result_type="rule_derived")
    for code, count in tier.forecast_eligibility.value_counts().items():
        _kpi(k, "DQ-3", "decision_quality", f"Forecast eligibility: {code}", "count / all materials", int(count), len(tier), round(count / len(tier), 6), "share of materials", f"All materials {len(tier)}", len(tier), "A and B", "eng_material_tier.csv", "Coverage, including abstention, by evidence", "Thresholds pending D-03", result_type="rule_derived")
    for code, count in tier.demand_class.value_counts().sort_index().items():
        _kpi(k, "DQ-4", "decision_quality", f"Demand class {code}", "count / all materials", int(count), len(tier), round(count / len(tier), 6), "share of materials", f"All materials {len(tier)}", len(tier), "Less smooth of A and B", "eng_material_tier.csv", "Coverage by evidence class", "Classes describe recorded issues", result_type="rule_derived")
    for flag in ["flag_slow_moving_by_recorded_issues", "flag_non_moving_by_recorded_issues", "flag_potentially_obsolete_candidate", "flag_stock_above_recorded_max", "flag_stock_at_or_below_recorded_min"]:
        c = int(flags[flag].sum())
        _kpi(k, "DQ-5", "decision_quality", flag, "count(flag) / all materials", c, len(flags), round(c / len(flags), 6), "share of materials", f"All materials {len(flags)}", len(flags), "Scenario independent", "eng_health_flags.csv", "Recorded-data flag", "Undated stock. Non-movement is not an obsolescence determination", result_type="historical_descriptive")

    for fid, name, block in [("FI-1", "Inventory exposure", "D-10 and C-5: PO-Item Amount meaning unconfirmed. Brilian computes as an assumption-based range per currency"), ("FI-2", "Cash tied up", "No verified price and no dated stock"), ("FI-3", "Scenario cost difference", "D-09: no approved cost set"), ("FI-4", "Estimated savings", "D-09. Simulated inventory changes are not realised savings")]:
        _kpi(k, fid, "financial_impact", name, "Not computed", None, None, None, None, "Grade A", None, "None", "Blocked", "Not available. Currencies stay separate when computed", block, status="NOT_COMPUTED")
    frame = pd.DataFrame(k)
    frame.insert(0, "run_id", run_id)
    frame["output_class"] = frame.result_type.map(lambda t: "deterministic_simulation" if t in ("replay", "heldout_replay", "held_out_vs_recorded") else "stochastic_simulation" if t in ("simulation", "mc_d_vs_recorded", "mc_l_vs_recorded", "mc_j_vs_recorded") else "rule_derived" if t == "rule_derived" else "historical_descriptive" if t == "historical_descriptive" else "not_computed")
    return frame
