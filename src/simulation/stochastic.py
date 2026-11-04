"""Run sets MC-D, MC-L and MC-J (design 9.2). Own-history resampling only, with common random numbers across policies, scenarios and views.

Reporting wording: spread under resampling. Never a confidence interval for a true value, and never a forecast of the plant.
"""
import math
from concurrent.futures import ProcessPoolExecutor

import numpy as np

from src.simulation import deterministic as det
from src.simulation import mc, parameters as params, resampling as rs
from src.simulation import settings as cfg
from src.simulation.inputs import load_inputs, material_lines

_STATE = {}


def _worker_init():
    _STATE["inputs"] = load_inputs()


def block_sources(reps: int) -> np.ndarray:
    return rs.draw_month_sources(reps, 17, 17, rs.generator(rs.STREAM_BLOCKS, 0))


def _row(material, row, demand, view, policy, k, run_set, out, reps, lv, lead_desc, initial, service_level) -> dict:
    fill = out["fill_rate"]
    n_fill = int(np.sum(~np.isnan(fill)))
    half = 1.96 * np.nanstd(fill, ddof=1) / math.sqrt(n_fill) if n_fill > 1 else None
    return {
        "material_no": material, "scenario_id": cfg.scenario_id(demand, view, policy, "BO", k), "demand_scenario": demand, "pr_view": view, "policy": policy, "unmet_rule": "BO", "config_id": k, "run_set": run_set,
        "result_type": "simulation", "output_class": "stochastic_simulation", "unit": row["unit"], "service_level": service_level, "parameter_source": "recorded_min_max_unverified" if policy in ("R1", "R2") else "full_window_same_history",
        "s_used": lv["s"], "S_used": lv.get("S"), "Q_used": lv.get("Q"), "lead_days_used": lead_desc, "initial_inventory_used": initial, "total_issues": round(float(out["total"].mean()), 6),
        "shortfall_probability": round(float(out["any_shortfall"].mean()), 6), "shortfall_probability_after_first_arrival": round(float(out["any_shortfall_after_first_arrival"].mean()), 6),
        "expected_unmet_qty": round(float(out["shortage_quantity"].mean()), 6), "unmet_qty_p95": float(np.quantile(out["shortage_quantity"], 0.95, method="inverted_cdf")),
        "days_at_or_below_zero": round(float(out["zero_on_hand_days"].mean()), 6), "mean_on_hand": round(float(out["mean_on_hand"].mean()), 6), "mean_on_hand_p05": round(float(np.quantile(out["mean_on_hand"], 0.05)), 6), "mean_on_hand_p95": round(float(np.quantile(out["mean_on_hand"], 0.95)), 6),
        "p95_on_hand": out["p95_on_hand_pooled"], "units_above_recorded_max": round(float(out["units_above_max"].mean()), 6), "days_above_recorded_max": round(float(out["days_above_max"].mean()), 6), "orders_placed": round(float(out["orders"].mean()), 6),
        "sim_fill_rate_quantity": None if n_fill == 0 else round(float(np.nanmean(fill)), 6), "fill_rate_p05": None if n_fill == 0 else round(float(np.nanquantile(fill, 0.05)), 6), "fill_rate_p95": None if n_fill == 0 else round(float(np.nanquantile(fill, 0.95)), 6),
        "fill_rate_half_width": None if half is None else round(float(half), 6), "converged_fill_rate": None if half is None else bool(half <= cfg.CONVERGENCE_HALF_WIDTH), "sim_stockout_days": round(float(out["stockout_days"].mean()), 6),
        "sim_average_backorder": round(float(out["mean_backorder"].mean()), 6), "sim_order_quantity_total": round(float(out["ordered"].mean()), 6), "sim_orders_per_year": round(float(out["orders"].mean()) * 365 / 518, 6),
        "sim_ending_on_hand": round(float(out["end_on_hand"].mean()), 6), "n_replications": reps, "seed": cfg.MASTER_SEED,
    }


def run_material(material: str, reps: int = cfg.MC_REPLICATIONS, inputs=None) -> list[dict]:
    """Every run set the material qualifies for. Independent of the order materials run in."""
    inputs = inputs or _STATE["inputs"]
    row = inputs.t3.loc[material]
    grade_a = row["active_months"] >= cfg.MIN_ACTIVE_MONTHS
    lead_ok = row["lead_observations_distinct"] >= cfg.MIN_LEAD_OBSERVATIONS
    if not (grade_a or lead_ok):
        return []
    sets = []
    if grade_a:
        sets.append("MC-D")
    if lead_ok:
        sets.append("MC-L")
    if grade_a and lead_ok:
        sets.append("MC-J")
    sources = block_sources(reps)
    estimate_sources = rs.draw_month_sources(cfg.LTD_PATHS, 17, 17, rs.generator(rs.STREAM_ESTIMATE_BLOCKS, 17))
    uniform = rs.generator(rs.STREAM_LEADS, rs.material_key(material)).random((reps, cfg.HORIZON_DAYS)) if lead_ok else None
    initial = math.ceil(row["assumed_initial_inventory"])
    recorded_max = row["max_parameter_unverified"]
    rows = []
    for demand in cfg.DEMAND_SCENARIOS:
        lines = material_lines(inputs, demand, material)
        table = rs.day_of_month_table(lines, cfg.MONTH_LENGTHS)
        resampled_paths = rs.build_daily_paths(table, sources, cfg.MONTH_LENGTHS) if grade_a else None
        replay_path = np.zeros((reps, cfg.HORIZON_DAYS))
        for day, qty in lines:
            replay_path[:, day] += qty
        for view_code, view in cfg.PR_VIEWS.items():
            obs = inputs.lead_obs[view][material]
            median_lead = det.lead_days(row[f"lead_median__{view}"])
            drawn = rs.lead_draws(obs, uniform) if lead_ok else None
            recorded = params.recorded_policy_levels(row["min_parameter_unverified"], recorded_max, row[f"pr_qty_median__{view}"])
            policies = [("R1", recorded["R1"], None), ("R2", recorded["R2"], None)]
            if grade_a:
                est = params.estimate_ltd(lines, obs, material, bool(lead_ok), 17, estimate_sources)
                levels = params.proposed_levels(est, row[f"pr_qty_median__{view}"], recorded_max)
                policies += [(code, levels[code], levels[code]["service_level"]) for code in ("N1", "X1", "X2", "X3")]
            for run_set in sets:
                k = cfg.MC_KSETS[run_set]
                paths = resampled_paths if run_set in ("MC-D", "MC-J") else replay_path
                leads = drawn if run_set in ("MC-L", "MC-J") else median_lead
                lead_desc = "resampled_per_order" if run_set in ("MC-L", "MC-J") else median_lead
                for code, lv, level in policies:
                    if run_set == "MC-L" and code not in ("R1", "R2") and not grade_a:
                        continue
                    out = mc.simulate_batch(paths, initial, lv["s"], lv.get("S"), lv.get("Q"), leads, recorded_max)
                    rows.append(_row(material, row, demand, view_code, code, k, run_set, out, reps, lv, lead_desc, initial, level))
    return rows


def run_all(materials: list[str], reps: int = cfg.MC_REPLICATIONS, workers: int = 8) -> list[dict]:
    rows = []
    with ProcessPoolExecutor(max_workers=workers, initializer=_worker_init) as pool:
        for part in pool.map(_run_one, [(m, reps) for m in materials], chunksize=4):
            rows.extend(part)
    return rows


def _run_one(args):
    return run_material(args[0], args[1])
