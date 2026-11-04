"""Demand forecasts where evidence supports them, abstention elsewhere. DEMAND_INTELLIGENCE_METHODOLOGY and VALIDATION_FRAMEWORK section 2.

Forecasts describe issue quantities, which are not proven demand. The acceptance rule was fixed before any result: a method is used for a
class only if it beats mean-of-history on pinball loss on most materials of that class, otherwise mean-of-history is used.
Low and high bounds are spread under resampling of the material's own history. They are not prediction intervals with a stated coverage;
coverage is measured and reported at class level.
"""
import math

import numpy as np
import pandas as pd

from src.simulation import parameters as params
from src.simulation import resampling as rs
from src.simulation import settings as cfg
from src.simulation.inputs import material_lines

POINT_METHODS = ("mean", "naive", "croston_sba", "tsb")


def croston_sba(series, alpha: float = cfg.SBA_ALPHA) -> float:
    """Croston with the Syntetos-Boylan correction. Per-period rate. Zero if the series has no demand."""
    series = np.asarray(series, dtype=float)
    positive = np.flatnonzero(series > 0)
    if positive.size == 0:
        return 0.0
    size, interval, gap = series[positive[0]], float(positive[0] + 1), 1
    for value in series[positive[0] + 1:]:
        if value > 0:
            size += alpha * (value - size)
            interval += alpha * (gap - interval)
            gap = 1
        else:
            gap += 1
    return (1 - alpha / 2) * size / interval


def tsb(series, alpha: float = cfg.TSB_ALPHA, beta: float = cfg.TSB_BETA) -> float:
    """Teunter-Syntetos-Babai. Per-period rate. Demand probability updates every period, so obsolescence pulls the rate down."""
    series = np.asarray(series, dtype=float)
    positive = np.flatnonzero(series > 0)
    if positive.size == 0:
        return 0.0
    prob, size = float(np.mean(series > 0)), series[positive[0]]
    for value in series:
        if value > 0:
            prob += beta * (1 - prob)
            size += alpha * (value - size)
        else:
            prob += beta * (0 - prob)
    return prob * size


def point_rate(method: str, history) -> float:
    history = np.asarray(history, dtype=float)
    if method == "mean":
        return float(history.mean())
    if method == "naive":
        return float(history[-1])
    if method == "croston_sba":
        return croston_sba(history)
    if method == "tsb":
        return tsb(history)
    raise ValueError(method)


def pinball(actual: float, predicted: float, alpha: float) -> float:
    gap = actual - predicted
    return alpha * gap if gap >= 0 else (alpha - 1) * gap


def horizon_months(lead_days: float | None) -> int:
    if lead_days is None or (isinstance(lead_days, float) and math.isnan(lead_days)):
        return 1
    return int(min(6, max(1, math.ceil(lead_days / 30.44))))


def rolling_origin(months: pd.DataFrame, lead_median: pd.Series, classes: pd.Series, demand: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Per-material losses, then class summary. Same origins and draws for every material. History of 9 to 15 months."""
    rows = []
    for origin in cfg.FORECAST_ORIGINS:
        rng = rs.generator(rs.STREAM_FORECAST, origin)
        for h in range(1, 7):
            if origin + h > 17:
                continue
            sources = rs.draw_month_sources(cfg.FORECAST_BOOTSTRAP_PATHS, h, origin, rng)
            for material in months.index[[horizon_months(lead_median.get(m)) == h for m in months.index]]:
                series = months.loc[material].to_numpy(dtype=float)
                history, actual = series[:origin], series[origin:origin + h].sum()
                draws = history[sources].sum(axis=1)
                quantiles = {a: float(np.quantile(draws, a, method="inverted_cdf")) for a in cfg.FORECAST_ALPHAS}
                for method in POINT_METHODS:
                    point = point_rate(method, history) * h
                    rows.append({"material_no": material, "origin": origin, "h": h, "method": method, "ae": abs(actual - point), "error": point - actual, "actual": actual,
                                 **{f"pl_{a}": pinball(actual, point, a) for a in cfg.FORECAST_ALPHAS}, **{f"cover_{a}": float(actual <= point) for a in cfg.FORECAST_ALPHAS}})
                rows.append({"material_no": material, "origin": origin, "h": h, "method": "block_bootstrap", "ae": abs(actual - quantiles[0.5]), "error": quantiles[0.5] - actual, "actual": actual,
                             **{f"pl_{a}": pinball(actual, quantiles[a], a) for a in cfg.FORECAST_ALPHAS}, **{f"cover_{a}": float(actual <= quantiles[a]) for a in cfg.FORECAST_ALPHAS}})
    detail = pd.DataFrame(rows)
    if detail.empty:
        return detail, detail
    # Scaled error: absolute error over the mean absolute one-month change in the whole window. A scale, not a forecast input.
    scale = months.apply(lambda s: np.abs(np.diff(s.to_numpy(dtype=float))).mean(), axis=1).replace(0, np.nan)
    material = detail.groupby(["material_no", "method"]).mean(numeric_only=True).reset_index()
    material["scaled_error"] = material.ae / material.material_no.map(scale)
    base = material[material.method == "mean"].set_index("material_no")
    summary = []
    material["demand_class"] = material.material_no.map(classes)
    for (cls, method), part in material.groupby(["demand_class", "method"]):
        row = {"demand_scenario": demand, "demand_class": cls, "method": method, "n_materials": len(part), "n_origin_evaluations": int(detail[(detail.method == method) & detail.material_no.isin(part.material_no)].shape[0]),
               "median_scaled_error": round(float(part.scaled_error.median()), 6), "mean_bias": round(float(part.error.mean()), 6)}
        for a in cfg.FORECAST_ALPHAS:
            joined = part.set_index("material_no")[f"pl_{a}"]
            row[f"share_beating_mean_pinball_{a}"] = round(float((joined < base.loc[joined.index, f"pl_{a}"]).mean()), 6)
            row[f"mean_pinball_{a}"] = round(float(joined.mean()), 6)
            row[f"empirical_coverage_{a}"] = round(float(part[f"cover_{a}"].mean()), 6)
        summary.append(row)
    return material, pd.DataFrame(summary)


def select_methods(summary: pd.DataFrame) -> pd.DataFrame:
    """Apply the pre-registered rule. Point method judged at alpha 0.5. Bootstrap range accepted only if it beats mean-of-history at all three service levels."""
    rows = []
    for (demand, cls), part in summary.groupby(["demand_scenario", "demand_class"]):
        candidates = part[part.method.isin(["naive", "croston_sba", "tsb"])]
        winners = candidates[candidates["share_beating_mean_pinball_0.5"] > 0.5]
        point = "mean" if winners.empty else winners.sort_values(["share_beating_mean_pinball_0.5", "method"], ascending=[False, True]).iloc[0].method
        boot = part[part.method == "block_bootstrap"].iloc[0]
        accepted = all(boot[f"share_beating_mean_pinball_{a}"] > 0.5 for a in (0.90, 0.95, 0.98))
        rows.append({"demand_scenario": demand, "demand_class": cls, "selected_point_method": point, "bootstrap_range_accepted": accepted})
    return pd.DataFrame(rows)


def _ltd_rows(inputs, tier, run_id, chosen):
    rows = []
    status_by_key = {(r.demand_scenario, r.demand_class): ("accepted" if r.bootstrap_range_accepted else "not_accepted_failed_preregistered_pinball_rule") for r in chosen.itertuples()}
    sources = rs.draw_month_sources(cfg.LTD_PATHS, 17, 17, rs.generator(rs.STREAM_ESTIMATE_BLOCKS, 17))
    for material in tier.index[tier.forecast_eligibility == "forecast_range"]:
        row = tier.loc[material]
        resample = (row.lead_observations_distinct >= cfg.MIN_LEAD_OBSERVATIONS) if pd.notna(row.lead_observations_distinct) else False
        for demand, name in cfg.DEMAND_SCENARIOS.items():
            lines = material_lines(inputs, demand, material)
            for code, view in cfg.PR_VIEWS.items():
                obs = inputs.lead_obs[view].get(material)
                base = {"run_id": run_id, "material_no": material, "demand_scenario": demand, "pr_view": code, "scenario_id": cfg.scenario_id(demand, code, "NA", "NA"), "horizon_basis": "lead_time_demand", "unit": row.unit,
                        "demand_class": row[f"demand_class__{name}"], "active_months": row.active_months, "n_issue_lines": row[f"n_issue_lines__{name}"], "evidence_class": row.evidence_subtier, "forecast_eligible": True, "output_class": "statistical_forecast"}
                if obs is None or len(obs) == 0:
                    rows.append({**base, "forecast_eligible": False, "confidence": "Abstain", "abstain_reason": "no_promised_interval_for_lead_time_demand", "forecast_method": "abstain", "forecast_period": "lead_window_after_2026-09"})
                    continue
                est = params.estimate_ltd(lines, obs, material, bool(resample), 17, sources)
                rows.append({**base, "forecast_period": "lead_window_after_2026-09", "horizon_days": est.lead_days_median, "forecast_quantity": round(est.mean, 6), "forecast_method": "block_bootstrap_lead_time_demand",
                             "lead_time_demand_low": est.p05, "lead_time_demand_mid": est.p50, "lead_time_demand_high": est.p95, "uncertainty_kind": "spread_under_resampling_p05_p95", "confidence": row.confidence, "lead_mode": est.lead_mode, "quantile_method_status": status_by_key[(demand, row[f"demand_class__{name}"])]})
    return rows


def build_forecast(inputs, tier: pd.DataFrame, run_id: str) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """eng_forecast.csv, eng_forecast_validation.csv and the method selection. Every one of the 7,481 materials gets a row per scenario, with a forecast or a reason."""
    summaries = []
    eligible = tier.index[tier.forecast_eligibility == "forecast_range"]
    lead = inputs.inventory.loc[eligible, "promised_interval_days_median__exact_distinct_rows"]
    for demand, name in cfg.DEMAND_SCENARIOS.items():
        _, summary = rolling_origin(inputs.months[demand].loc[eligible], lead, tier.loc[eligible, f"demand_class__{name}"], demand)
        summaries.append(summary)
    summary = pd.concat(summaries, ignore_index=True)
    chosen = select_methods(summary)
    choice = {(r.demand_scenario, r.demand_class): r for r in chosen.itertuples()}

    rows = []
    for demand, name in cfg.DEMAND_SCENARIOS.items():
        month_table = inputs.months[demand]
        for material, row in tier.iterrows():
            base = {"run_id": run_id, "material_no": material, "demand_scenario": demand, "pr_view": "ALL", "scenario_id": cfg.scenario_id(demand, "NA", "NA", "NA"), "horizon_basis": "next_month_rate", "forecast_period": "2026-10", "horizon_days": None, "unit": row.unit,
                    "demand_class": row[f"demand_class__{name}"], "active_months": row.active_months, "n_issue_lines": row[f"n_issue_lines__{name}"], "evidence_class": row.evidence_subtier}
            cls = row[f"demand_class__{name}"]
            if cls == "D0":
                rows.append({**base, "forecast_eligible": False, "forecast_method": "abstain", "confidence": "Abstain", "abstain_reason": "no_recorded_consumption_in_window", "output_class": "rule_derived"})
            elif cls == "D1":
                rows.append({**base, "forecast_eligible": False, "forecast_method": "abstain", "confidence": "Low", "abstain_reason": "fewer_than_3_active_months_no_forecast", "output_class": "rule_derived"})
            elif cls == "D2":
                series = month_table.loc[material].to_numpy(dtype=float)
                active = series[series > 0]
                rows.append({**base, "forecast_eligible": False, "forecast_method": "observed_active_month_range", "rate_low": float(active.min()), "rate_high": float(active.max()), "uncertainty_kind": "observed_min_max_of_active_months", "confidence": "Low", "abstain_reason": "fewer_than_6_active_months_rate_range_only", "output_class": "historical_descriptive"})
            else:
                series = month_table.loc[material].to_numpy(dtype=float)
                pick = choice[(demand, cls)]
                ordered = np.sort(series)
                rows.append({**base, "forecast_eligible": True, "forecast_quantity": round(point_rate(pick.selected_point_method, series), 6), "forecast_method": pick.selected_point_method, "rate_low": float(np.quantile(ordered, 0.05, method="inverted_cdf")),
                             "rate_mid": float(np.quantile(ordered, 0.5, method="inverted_cdf")), "rate_high": float(np.quantile(ordered, 0.95, method="inverted_cdf")), "uncertainty_kind": "observed_month_percentiles_p05_p95", "confidence": row.confidence, "output_class": "statistical_forecast"})
    rows += _ltd_rows(inputs, tier, run_id, chosen)
    frame = pd.DataFrame(rows)
    return frame, summary, chosen
