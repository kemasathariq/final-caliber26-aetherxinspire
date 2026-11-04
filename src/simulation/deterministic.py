"""Deterministic run sets: R0 replay of 665 materials, R2, proposed policies, one-at-a-time sensitivity S1, and held-out replay."""
import math

import numpy as np
import pandas as pd

from src.simulation import parameters as params
from src.simulation import resampling as rs
from src.simulation import settings as cfg
from src.simulation.engine import BACKORDER, LOST_SALES, Policy, lead_days, scale_lines, simulate
from src.simulation.inputs import material_lines

VIEW_CODES = {v: k for k, v in cfg.PR_VIEWS.items()}


def result_row(material, row, demand, view_code, policy_code, shortage, k, run_set, result_type, output_class, r, s, S, Q, lead, initial, parameter_source, service_level=None) -> dict:
    """One row of eng_scenario_result.csv from a deterministic run."""
    return {
        "material_no": material, "scenario_id": cfg.scenario_id(demand, view_code, policy_code, shortage, k), "demand_scenario": demand, "pr_view": view_code, "policy": policy_code, "unmet_rule": shortage, "config_id": k,
        "run_set": run_set, "result_type": result_type, "output_class": output_class, "unit": row["unit"], "service_level": service_level, "parameter_source": parameter_source,
        "s_used": s, "S_used": S, "Q_used": Q, "lead_days_used": lead, "initial_inventory_used": initial, "total_issues": r.total_issues, "n_issue_lines": r.n_lines,
        "shortfall_probability": None, "any_shortfall": r.stockout_days > 0, "expected_unmet_qty": r.shortage_quantity, "days_at_or_below_zero": r.zero_on_hand_days, "mean_on_hand": round(r.avg_on_hand, 6), "p95_on_hand": r.p95_on_hand,
        "units_above_recorded_max": round(r.mean_units_above_max, 6), "days_above_recorded_max": r.days_above_max, "orders_placed": r.orders_placed,
        "sim_fill_rate_quantity": _round(r.fill_rate_quantity), "sim_fill_rate_lines": _round(r.fill_rate_lines), "sim_ready_rate_days": _round(r.ready_rate), "sim_average_backorder": round(r.avg_backorder, 6),
        "sim_stockout_days": r.stockout_days, "sim_stockout_periods": r.stockout_periods, "sim_longest_stockout_days": r.longest_stockout, "sim_days_to_first_stockout": r.first_stockout_day,
        "sim_orders_per_year": round(r.orders_per_year, 6), "sim_order_quantity_mean": _round(r.order_quantity_mean), "sim_order_quantity_total": r.order_quantity_total, "sim_orders_open_at_end": r.orders_open_at_end,
        "sim_first_order_day": r.first_order_day, "sim_first_arrival_day": r.first_arrival_day, "sim_ending_on_hand": r.end_on_hand, "sim_ending_backorder": r.end_backorder, "sim_ending_on_order": r.end_on_order, "sim_lost_quantity": r.lost,
        "sim_fill_rate_after_first_arrival": _round(r.fill_rate_after_first_arrival), "sim_stockout_days_after_first_arrival": r.stockout_days_after_first_arrival,
    }


def _round(value, digits=6):
    return None if value is None else round(value, digits)


def initial_inventory(rule: str, factor: float, row, total_issues: float) -> float:
    base = {"stock": row["assumed_initial_inventory"], "min": row["min_parameter_unverified"], "max": row["max_parameter_unverified"], "stock_plus_issues": row["assumed_initial_inventory"] + total_issues}[rule]
    return math.ceil(base * factor)


def run_recorded(inputs, policy_code="R0", ksets=None, shortage=BACKORDER, keep_trace=False, materials=None):
    """Replay recorded Min and Max under Scenarios A and B and both views. Returns rows, and traces if asked."""
    rows, traces = [], []
    t3 = inputs.t3 if materials is None else inputs.t3.loc[materials]
    for kset in ksets or [cfg.K0]:
        for material, row in t3.iterrows():
            for demand in cfg.DEMAND_SCENARIOS:
                lines = material_lines(inputs, demand, material, kset.peak_lines)
                unscaled_total = sum(q for _, q in lines)
                run_lines = scale_lines(lines, kset.demand_factor)
                initial = initial_inventory(kset.i0_rule, kset.i0_factor, row, unscaled_total)
                for code, view in cfg.PR_VIEWS.items():
                    base_lead = row[f"lead_p90__{view}"] if kset.lead_rule == "p90" else row[f"lead_median__{view}"]
                    lead = lead_days(base_lead, kset.lead_factor)
                    levels = params.recorded_policy_levels(row["min_parameter_unverified"], row["max_parameter_unverified"], row[f"pr_qty_median__{view}"], kset.min_factor, kset.max_factor)
                    lv = levels["R2"] if policy_code == "R2" else levels["R1"]
                    policy = Policy(lv["s"], S=lv["S"], Q=lv["Q"])
                    r = simulate(run_lines, initial, policy, lead, shortage=shortage, recorded_max=row["max_parameter_unverified"], keep_trace=keep_trace)
                    rows.append(result_row(material, row, demand, code, policy_code, shortage, kset.k, kset.run_set, "replay", "deterministic_simulation", r, lv["s"], lv["S"], lv["Q"], lead, initial, "recorded_min_max_unverified"))
                    if keep_trace:
                        for t in r.trace:
                            traces.append({"material_no": material, "scenario_id": rows[-1]["scenario_id"], **t})
    return rows, traces


def estimate_all_parameters(inputs) -> dict:
    """Full-window estimates per Grade A material, demand scenario and view. Common block draws across materials and scenarios."""
    sources = rs.draw_month_sources(cfg.LTD_PATHS, 17, 17, rs.generator(rs.STREAM_ESTIMATE_BLOCKS, 17))
    out = {}
    for material in inputs.grade_a:
        row = inputs.t3.loc[material]
        resample = row["lead_observations_distinct"] >= cfg.MIN_LEAD_OBSERVATIONS
        for demand in cfg.DEMAND_SCENARIOS:
            lines = material_lines(inputs, demand, material)
            for code, view in cfg.PR_VIEWS.items():
                est = params.estimate_ltd(lines, inputs.lead_obs[view][material], material, bool(resample), 17, sources)
                out[(material, demand, code)] = {"estimate": est, "levels": params.proposed_levels(est, row[f"pr_qty_median__{view}"], row["max_parameter_unverified"])}
    return out


def proposed_parameter_rows(inputs, estimates, run_id) -> list[dict]:
    rows = []
    for (material, demand, view), item in estimates.items():
        row = inputs.t3.loc[material]
        est = item["estimate"]
        for code in cfg.SERVICE_LEVELS:
            lv = item["levels"][code]
            rows.append({"run_id": run_id, "material_no": material, "scenario_id": cfg.scenario_id(demand, view, code), "demand_scenario": demand, "pr_view": view, "policy": code, "service_level": lv["service_level"],
                         "proposed_s": lv["s"], "proposed_S": lv["S"], "proposed_Q": lv["Q"], "safety_stock": lv["safety_stock"], "flag_safety_stock_floored": lv["flag_safety_stock_floored"], "proposed_S_capped_at_recorded_max": lv["S_capped_at_recorded_max"],
                         "lead_time_demand_mean": lv["lead_time_demand_mean"], "lead_time_demand_quantile": lv["lead_time_demand_quantile"], "lead_mode": est.lead_mode, "lead_days_median": est.lead_days_median, "n_draws": est.n_draws,
                         "recorded_min": row["min_parameter_unverified"], "recorded_max": row["max_parameter_unverified"], "recorded_stock_undated": row["assumed_initial_inventory"], "unit": row["unit"],
                         "parameter_status": "candidate_for_review", "output_class": "stochastic_simulation"})
    return rows


def run_policy_replay(inputs, estimates) -> list[dict]:
    """Full-window replay of N1 and X1 to X3. Parameters use the same months they are replayed on, so this is in-sample and labelled that way."""
    rows = []
    for (material, demand, view_code), item in estimates.items():
        row = inputs.t3.loc[material]
        view = cfg.PR_VIEWS[view_code]
        lines = material_lines(inputs, demand, material)
        lead = lead_days(row[f"lead_median__{view}"])
        initial = math.ceil(row["assumed_initial_inventory"])
        for code, lv in item["levels"].items():
            r = simulate(lines, initial, Policy(lv["s"], S=lv["S"]), lead, recorded_max=row["max_parameter_unverified"])
            rows.append(result_row(material, row, demand, view_code, code, BACKORDER, "K0", "R0", "replay", "deterministic_simulation", r, lv["s"], lv["S"], lv["Q"], lead, initial, "full_window_in_sample", lv["service_level"]))
    return rows


def training_material_status(inputs) -> dict:
    """Which Grade A materials hold enough evidence in the training months alone. The thresholds do not change for training."""
    out = {}
    for material in inputs.grade_a:
        active = (inputs.months["A"].loc[material, cfg.MONTHS[:cfg.TRAIN_MONTHS]] > 0).sum()
        out[material] = {"train_active_months": int(active)}
    return out


def run_held_out(inputs) -> tuple[list[dict], pd.DataFrame]:
    """VALIDATION_FRAMEWORK section 3. Parameters from months 1 to 11, replay on months 12 to 17, common opening stock per rule, same lead proxy for all policies."""
    rows, status = [], []
    sources = rs.draw_month_sources(cfg.LTD_PATHS, cfg.TRAIN_MONTHS, cfg.TRAIN_MONTHS, rs.generator(rs.STREAM_ESTIMATE_BLOCKS, cfg.TRAIN_MONTHS))
    test_start = pd.Timestamp(cfg.TEST_START_DATE)
    train_lines_by_view = {}
    for view, table in inputs.procurement.items():
        usable = table[(table.pr_date < test_start) & (table.promised_interval_days >= 0)]
        train_lines_by_view[view] = {m: g for m, g in usable.groupby("material_no")}
    distinct_train = {m: len(g) for m, g in train_lines_by_view["exact_distinct_rows"].items()}

    for material in inputs.grade_a:
        row = inputs.t3.loc[material]
        active = int((inputs.months["A"].loc[material, cfg.MONTHS[:cfg.TRAIN_MONTHS]] > 0).sum())
        has_lead = material in train_lines_by_view["exact_distinct_rows"]
        included = active >= cfg.MIN_ACTIVE_MONTHS and has_lead
        status.append({"material_no": material, "train_active_months": active, "train_lead_observations": distinct_train.get(material, 0), "included_in_held_out": included,
                       "exclusion_reason": None if included else ("fewer_than_6_active_training_months" if active < cfg.MIN_ACTIVE_MONTHS else "no_pr_line_in_training_months")})
        if not included:
            continue
        resample = distinct_train[material] >= cfg.MIN_LEAD_OBSERVATIONS
        for demand in cfg.DEMAND_SCENARIOS:
            all_lines = material_lines(inputs, demand, material)
            train = [(d, q) for d, q in all_lines if d < cfg.TEST_START_DAY]
            test = [(d - cfg.TEST_START_DAY, q) for d, q in all_lines if d >= cfg.TEST_START_DAY]
            for view_code, view in cfg.PR_VIEWS.items():
                train_table = train_lines_by_view[view][material]
                obs = np.sort(train_table.promised_interval_days.to_numpy(dtype=float))
                q_train = float(train_table.pr_quantity.median())
                est = params.estimate_ltd(train, obs, material, bool(resample), cfg.TRAIN_MONTHS, sources)
                levels = params.proposed_levels(est, q_train, row["max_parameter_unverified"])
                recorded = params.recorded_policy_levels(row["min_parameter_unverified"], row["max_parameter_unverified"], q_train)
                lead = lead_days(row[f"lead_median__{view}"])  # Same for every policy. Part of the test conditions, not of any policy.
                for rule, k in cfg.HELD_OUT_KSETS.items():
                    initial = initial_inventory(rule, 1.0, row, 0)
                    runs = [("R0", recorded["R1"], "recorded_min_max_unverified", None), ("R2", recorded["R2"], "recorded_min_training_pr_median", None)]
                    runs += [(code, levels[code], "training_months_only", levels[code]["service_level"]) for code in ("N1", "X1", "X2", "X3")]
                    for code, lv, source, level in runs:
                        policy = Policy(lv["s"], S=lv["S"]) if code != "R2" else Policy(lv["s"], Q=lv["Q"])
                        r = simulate(test, initial, policy, lead, horizon=cfg.TEST_DAYS, recorded_max=row["max_parameter_unverified"])
                        rows.append(result_row(material, row, demand, view_code, code, BACKORDER, k, "HO", "heldout_replay", "deterministic_simulation", r, lv["s"], lv["S"], lv["Q"], lead, initial, source, level))
    return rows, pd.DataFrame(status)


def gate_checks(r0: pd.DataFrame, inputs) -> list[dict]:
    """Design section 12.2 predictions, written before the engine existed. All must hold before stochastic runs start."""
    rows = []

    def add(check, expected, actual):
        rows.append({"check_id": check, "expected": str(expected), "actual": str(actual), "status": "PASS" if expected == actual else "FAIL"})

    pop = inputs.t3
    for demand, expected in (("A", 125), ("B", 133)):
        chosen = r0[(r0.demand_scenario == demand)]
        for view in cfg.PR_VIEWS:
            part = chosen[chosen.pr_view == view]
            add(f"r0_no_order_{demand}_{view}", expected, int((part.orders_placed == 0).sum()))
    for view in cfg.PR_VIEWS:
        part = r0[(r0.demand_scenario == "A") & (r0.pr_view == view)]
        add(f"r0_order_at_day0_review_{view}", 183, int(((part.sim_first_order_day == 0) & part.material_no.isin(pop.index[pop.at_or_below_min_at_start])).sum()))
    measures = ["orders_placed", "expected_unmet_qty", "mean_on_hand", "sim_fill_rate_quantity", "sim_stockout_days", "sim_order_quantity_total", "sim_ending_on_hand"]
    for view in cfg.PR_VIEWS:
        a = r0[(r0.demand_scenario == "A") & (r0.pr_view == view)].set_index("material_no")[measures]
        b = r0[(r0.demand_scenario == "B") & (r0.pr_view == view)].set_index("material_no")[measures]
        same = (a.fillna(-1) == b.fillna(-1).loc[a.index]).all(axis=1)
        identical = pop.index[pop.scenarios_identical_by_construction]
        add(f"r0_identical_by_construction_{view}", 436, int(same.loc[identical].sum()))
        add(f"r0_whether_min_reached_differs_{view}", 8, int(((a.orders_placed == 0) != (b.orders_placed.loc[a.index] == 0)).sum()))
    for demand, expected, column in (("A", 238, "initial_inventory_covers_all_issues__scenario_a"), ("B", 253, "initial_inventory_covers_all_issues__scenario_b")):
        part = r0[(r0.demand_scenario == demand) & (r0.pr_view == "ED")].set_index("material_no")
        covered = pop.index[pop[column]]
        add(f"r0_covered_materials_full_fill_{demand}", expected, int(((part.loc[covered].sim_fill_rate_quantity == 1) & (part.loc[covered].sim_stockout_days == 0)).sum()))
    return rows
