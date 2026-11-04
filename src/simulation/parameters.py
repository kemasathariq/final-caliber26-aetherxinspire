"""Proposed reorder parameters. INVENTORY_OPTIMISATION_METHODOLOGY section 2. Candidates for review, never called optimal.

Lead-time demand is demand over a promised interval on a resampled history path. Proposed s(alpha) is the alpha quantile, using a
value that occurred. Service levels are scenario levels (D-05). The 437 Grade B materials never reach this module (D-24).
"""
import math
from dataclasses import dataclass

import numpy as np

from src.simulation import resampling as rs
from src.simulation import settings as cfg
from src.simulation.engine import reference_levels


@dataclass(frozen=True)
class LtdEstimate:
    mean: float
    p05: float
    p50: float
    p95: float
    quantiles: dict
    lead_mode: str
    lead_days_median: int
    n_draws: int


def _sources(n_months: int) -> np.ndarray:
    return rs.draw_month_sources(cfg.LTD_PATHS, n_months, n_months, rs.generator(rs.STREAM_ESTIMATE_BLOCKS, n_months))


def estimate_ltd(lines, observations: np.ndarray, material: str, resample_lead: bool, n_months: int = 17, sources: np.ndarray | None = None) -> LtdEstimate:
    """Own-history block bootstrap of months, with own-history lead draws where evidence allows, otherwise the median promised interval."""
    lengths = cfg.MONTH_LENGTHS[:n_months]
    table = rs.day_of_month_table(lines, lengths)
    paths = rs.build_daily_paths(table, _sources(n_months) if sources is None else sources, lengths)
    days = paths.shape[1]
    rng = rs.generator(rs.STREAM_ESTIMATE_WINDOWS, rs.material_key(material), n_months)
    starts = rng.integers(0, days, size=(cfg.LTD_PATHS, cfg.LTD_WINDOWS_PER_PATH))
    uniform = rng.random(size=(cfg.LTD_PATHS, cfg.LTD_WINDOWS_PER_PATH))
    median_lead = max(1, math.ceil(float(np.median(observations))))
    leads = rs.lead_draws(observations, uniform) if resample_lead else np.full(starts.shape, median_lead)
    ltd = rs.lead_time_demand(paths, leads, starts).ravel()
    quantiles = {code: float(np.quantile(ltd, a, method="inverted_cdf")) for code, a in cfg.SERVICE_LEVELS.items()}
    return LtdEstimate(float(ltd.mean()), float(np.quantile(ltd, 0.05, method="inverted_cdf")), float(np.quantile(ltd, 0.5, method="inverted_cdf")), float(np.quantile(ltd, 0.95, method="inverted_cdf")),
                       quantiles, "resampled_own_history" if resample_lead else "median_promised_interval", median_lead, ltd.size)


def proposed_levels(estimate: LtdEstimate, q_observed: float, recorded_max: float) -> dict:
    """Per policy: X1 to X3 at the service-level scenarios, and N1, the naive benchmark that reorders at mean lead-time demand."""
    q = max(1, math.ceil(q_observed))
    out = {}
    for code, alpha in cfg.SERVICE_LEVELS.items():
        s = math.ceil(estimate.quantiles[code])
        raw_safety = s - estimate.mean
        out[code] = {"service_level": alpha, "s": s, "S": s + q, "Q": q, "safety_stock": max(0.0, round(raw_safety, 6)), "flag_safety_stock_floored": raw_safety < 0,
                     "lead_time_demand_mean": round(estimate.mean, 6), "lead_time_demand_quantile": estimate.quantiles[code], "S_capped_at_recorded_max": min(s + q, max(math.ceil(recorded_max), s + 1))}
    s = math.ceil(estimate.mean)
    out["N1"] = {"service_level": None, "s": s, "S": s + q, "Q": q, "safety_stock": 0.0, "flag_safety_stock_floored": False, "lead_time_demand_mean": round(estimate.mean, 6), "lead_time_demand_quantile": None, "S_capped_at_recorded_max": None}
    return out


def recorded_policy_levels(min_qty: float, max_qty: float, q_observed: float, min_factor: float = 1.0, max_factor: float = 1.0) -> dict:
    """R0 and R1 are the same reading of recorded values: s, S. R2 is s with a repeated fixed quantity (design section 7)."""
    s, S = reference_levels(min_qty, max_qty, min_factor, max_factor)
    return {"R1": {"s": s, "S": S, "Q": None}, "R2": {"s": s, "S": None, "Q": max(1, math.ceil(q_observed))}}
