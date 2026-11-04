"""Vectorised batch of the engine in engine.py, backorder mode, over replications of one material. tests confirm it equals engine.simulate.

Results are the spread from reshuffling a material's own history. They are not probabilities of a future outcome and not confidence intervals.
"""
import numpy as np


def simulate_batch(demand: np.ndarray, initial: float, s: int, S: int | None, Q: int | None, leads, recorded_max: float | None = None) -> dict:
    """demand: reps x days. leads: whole number, or reps x days array of whole numbers. Returns per-replication measures."""
    reps, days = demand.shape
    h = np.full(reps, float(initial))
    b = np.zeros(reps)
    o = np.zeros(reps)
    pipe = np.zeros((reps, days + 1))
    hist_h = np.empty((reps, days))
    hist_b = np.empty((reps, days))
    served = np.zeros(reps)
    backfilled = np.zeros(reps)
    arrived = np.zeros(reps)
    orders = np.zeros(reps, dtype=np.int64)
    ordered = np.zeros(reps)
    first_arrival = np.full(reps, days, dtype=np.int64)
    fixed_lead = np.isscalar(leads) or isinstance(leads, (int, np.integer))
    rows = np.arange(reps)
    active_day = demand.any(axis=0)

    def review(t: int) -> None:
        position = h + o - b
        mask = position <= s
        if not mask.any():
            return
        idx = rows[mask]
        if S is not None:
            qty = S - position[mask]
        else:
            qty = Q * (np.floor((s - position[mask]) / Q) + 1)
        lead = int(leads) if fixed_lead else leads[idx, t]
        due = t + lead
        keep = due < days if not fixed_lead else None
        if fixed_lead:
            if due < days:
                pipe[idx, due] += qty  # += because the day-0 initial review and the day-0 review can share a due day.
        else:
            pipe[idx[keep], due[keep]] += qty[keep]
        o[idx] += qty
        orders[idx] += 1
        ordered[idx] += qty

    review(0)
    for t in range(days):
        arrive = pipe[:, t]
        if arrive.any():
            got = arrive > 0
            h += arrive
            o -= arrive
            arrived += arrive
            first_arrival[got & (first_arrival == days)] = t
            fill = np.minimum(h, b)
            h -= fill
            b -= fill
            backfilled += fill
        if active_day[t]:
            d = demand[:, t]
            w = np.minimum(h, d)
            h -= w
            served += w
            b += d - w
            review(t)
        hist_h[:, t] = h
        hist_b[:, t] = b

    total = demand.sum(axis=1)
    # Design section 7, on every replication. A failure stops the run.
    if not (np.allclose(initial + arrived, h + served + backfilled) and np.allclose(total, served + backfilled + b) and np.allclose(ordered, arrived + o)):
        raise ArithmeticError("Conservation failed in the Monte Carlo batch")
    if (h < 0).any() or (b < 0).any() or (o < -1e-9).any():
        raise ArithmeticError("State bound failed in the Monte Carlo batch")
    stockout = hist_b > 0
    after = np.arange(days)[None, :] >= np.where(first_arrival == days, 0, first_arrival)[:, None]
    above = np.maximum(hist_h - recorded_max, 0) if recorded_max is not None else np.zeros_like(hist_h)
    with np.errstate(invalid="ignore", divide="ignore"):
        fill_rate = np.where(total > 0, served / total, np.nan)
    return {
        "any_shortfall": stockout.any(axis=1), "any_shortfall_after_first_arrival": (stockout & after).any(axis=1), "shortage_quantity": total - served, "stockout_days": stockout.sum(axis=1),
        "zero_on_hand_days": (hist_h == 0).sum(axis=1), "mean_on_hand": hist_h.mean(axis=1), "mean_backorder": hist_b.mean(axis=1), "p95_on_hand_pooled": float(np.quantile(hist_h, 0.95, method="inverted_cdf")),
        "days_above_max": (above > 0).sum(axis=1), "units_above_max": above.mean(axis=1), "orders": orders, "ordered": ordered, "fill_rate": fill_rate, "total": total, "served": served,
        "end_on_hand": h, "end_backorder": b, "end_on_order": o, "backfilled": backfilled, "arrived": arrived,
    }
