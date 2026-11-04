"""Single-material, event-driven inventory recursion. Specification: SIMULATION_DESIGN_SPECIFICATION sections 6 to 8.

Order inside a day: arrivals, backfill, issues in source_row order, review, record. State is only recalculated on days
with an event; inventory position changes only on issue days, and a review always leaves it above s, so days with no
event repeat the previous end-of-day state. The separate daily loop in tests/unit/test_engine_independent.py confirms this.

Everything returned is SIMULATED. A shortage on a replayed issue is a finding about the assumptions: the issue did happen.
"""
import heapq
import math
from collections import Counter
from dataclasses import dataclass
from typing import Callable, Sequence

BACKORDER, LOST_SALES = "BO", "LS"


class ConservationError(AssertionError):
    """A conservation law in design section 7 failed."""


@dataclass(frozen=True)
class Policy:
    """(s, S) when S is set, repeated fixed quantity (s, Q) when Q is set. Policy R2 is the second form."""

    s: int
    S: int | None = None
    Q: int | None = None

    def __post_init__(self):
        if (self.S is None) == (self.Q is None):
            raise ValueError("Set exactly one of S or Q")
        if self.S is not None and self.S <= self.s:
            raise ValueError(f"Order-up-to level {self.S} must exceed reorder level {self.s}")
        if self.Q is not None and self.Q < 1:
            raise ValueError("Fixed order quantity must be at least 1")

    def order_quantity(self, position: float) -> float:
        if position > self.s:
            return 0
        if self.S is not None:
            return self.S - position
        return self.Q * (math.floor((self.s - position) / self.Q) + 1)


def reference_levels(min_qty: float, max_qty: float, min_factor: float = 1.0, max_factor: float = 1.0) -> tuple[int, int]:
    """Design section 7. s = ceil(factor x Min), S = max(ceil(factor x Max), s + 1)."""
    s = math.ceil(min_factor * min_qty)
    return s, max(math.ceil(max_factor * max_qty), s + 1)


def lead_days(value: float, factor: float = 1.0) -> int:
    """Whole days, rounded up, at least 1 (S-14)."""
    return max(1, math.ceil(value * factor))


def scale_lines(lines: Sequence[tuple[int, float]], factor: float) -> list[tuple[int, float]]:
    """Scale issue quantities so cumulative totals stay accurate (S-15). A line can round to zero and is then dropped."""
    if factor == 1.0:
        return list(lines)
    out, total, placed = [], 0.0, 0
    for day, qty in lines:
        total += qty
        target = math.floor(total * factor + 0.5)
        if target > placed:
            out.append((day, target - placed))
            placed = target
    return out


@dataclass
class SimResult:
    horizon: int
    total_issues: float
    n_lines: int
    served_on_day: float
    lines_full: int
    backfilled: float
    lost: float
    avg_on_hand: float
    avg_backorder: float
    ready_days: int
    zero_on_hand_days: int
    stockout_days: int
    stockout_periods: int
    longest_stockout: int
    first_stockout_day: int | None
    orders_placed: int
    order_quantity_total: float
    orders_open_at_end: int
    first_order_day: int | None
    first_arrival_day: int | None
    arrived_total: float
    end_on_hand: float
    end_backorder: float
    end_on_order: float
    p95_on_hand: float
    days_above_max: int
    mean_units_above_max: float
    issues_after_first_arrival: float
    served_after_first_arrival: float
    stockout_days_after_first_arrival: int
    orders: list
    trace: list | None = None

    @property
    def fill_rate_quantity(self):
        return self.served_on_day / self.total_issues if self.total_issues else None

    @property
    def fill_rate_lines(self):
        return self.lines_full / self.n_lines if self.n_lines else None

    @property
    def ready_rate(self):
        return self.ready_days / self.horizon

    @property
    def shortage_quantity(self):
        """Quantity not served on the day it was issued. Backordered or lost."""
        return self.total_issues - self.served_on_day

    @property
    def fill_rate_after_first_arrival(self):
        if self.first_arrival_day is None:
            return self.fill_rate_quantity
        return self.served_after_first_arrival / self.issues_after_first_arrival if self.issues_after_first_arrival else None

    @property
    def orders_per_year(self):
        return self.orders_placed * 365 / self.horizon

    @property
    def order_quantity_mean(self):
        return self.order_quantity_total / self.orders_placed if self.orders_placed else None


def _percentile_from_hist(hist: Counter, q: float) -> float:
    """Inverted-CDF percentile, so the value always occurred."""
    total = sum(hist.values())
    target, running = q * total, 0
    for value in sorted(hist):
        running += hist[value]
        if running >= target:
            return value
    return max(hist)


def simulate(lines: Sequence[tuple[int, float]], initial: float, policy: Policy, lead: int | Callable[[int, int], int], horizon: int = 518,
             shortage: str = BACKORDER, recorded_max: float | None = None, keep_trace: bool = False) -> SimResult:
    """Run one material. ``lines`` are (day, quantity) in source_row order. ``lead`` is a whole number of days, or a function of (order index, day)."""
    if shortage not in (BACKORDER, LOST_SALES):
        raise ValueError(shortage)
    if initial < 0:
        raise ValueError("Initial inventory cannot be negative")
    if any(q <= 0 for _, q in lines) or any(not 0 <= d < horizon for d, _ in lines):
        raise ValueError("Issue lines need a positive quantity and a day inside the horizon")
    by_day: dict[int, list[float]] = {}
    for day, qty in lines:
        by_day.setdefault(day, []).append(qty)

    get_lead = lead if callable(lead) else (lambda _i, _d: lead)
    h, b, o = initial, 0.0, 0.0
    arrivals: list[tuple[int, int, float]] = []  # (day due, order index, quantity). Same-day arrivals come in order placed.
    orders: list[tuple[int, float, int]] = []
    hist: Counter = Counter()
    trace = [] if keep_trace else None

    def place(day: int) -> None:
        nonlocal o
        q = policy.order_quantity(h + o - b)
        if q > 0:
            index = len(orders)
            due = day + max(1, int(get_lead(index, day)))
            heapq.heappush(arrivals, (due, index, q))
            orders.append((day, q, due))
            o += q

    place(0)  # Initial review on day 0, before any event.

    served = lines_full = backfilled = lost = arrived = 0.0
    sum_h = sum_b = above_days = above_units = 0.0
    ready = zero = stock_days = periods = longest = run = 0
    first_stockout = first_arrival = None
    issues_after = served_after = 0.0
    stock_after = 0
    last_recorded = -1

    def carry(until: int) -> None:
        """Repeat the end-of-day state for days last_recorded + 1 to until - 1, which have no event."""
        nonlocal sum_h, sum_b, ready, zero, above_days, above_units, stock_days, run, longest, stock_after, last_recorded
        gap = until - last_recorded - 1
        if gap <= 0:
            return
        sum_h += h * gap
        sum_b += b * gap
        hist[h] += gap
        if h > 0:
            ready += gap
        else:
            zero += gap
        if recorded_max is not None and h > recorded_max:
            above_days += gap
            above_units += (h - recorded_max) * gap
        if shortage == BACKORDER and b > 0:
            stock_days += gap
            run += gap
            longest = max(longest, run)
            if first_arrival is not None:
                stock_after += gap
        elif shortage == LOST_SALES or b == 0:
            run = 0
        last_recorded = until - 1

    event_days = set(by_day)
    day = 0
    while True:
        candidates = [d for d in event_days if d >= day]
        next_line = min(candidates) if candidates else None
        next_arrival = arrivals[0][0] if arrivals else None
        options = [x for x in (next_line, next_arrival) if x is not None and x < horizon]
        if not options:
            break
        day = min(options)
        carry(day)

        while arrivals and arrivals[0][0] == day:
            _, _, q = heapq.heappop(arrivals)
            h += q
            o -= q
            arrived += q
            if first_arrival is None:
                first_arrival = day
        fill = min(h, b)
        h -= fill
        b -= fill
        backfilled += fill

        day_lost = 0.0
        for qty in by_day.get(day, []):
            w = min(h, qty)
            h -= w
            served += w
            lines_full += w == qty
            if first_arrival is not None:
                issues_after += qty
                served_after += w
            short = qty - w
            if shortage == BACKORDER:
                b += short
            else:
                day_lost += short
        lost += day_lost

        if day in by_day:
            place(day)
        is_stockout = b > 0 if shortage == BACKORDER else day_lost > 0
        if is_stockout:
            stock_days += 1
            if first_stockout is None:
                first_stockout = day
            if first_arrival is not None:
                stock_after += 1
            if run == 0:
                periods += 1
            run += 1
            longest = max(longest, run)
        else:
            run = 0
        sum_h += h
        sum_b += b
        hist[h] += 1
        if h > 0:
            ready += 1
        else:
            zero += 1
        if recorded_max is not None and h > recorded_max:
            above_days += 1
            above_units += h - recorded_max
        last_recorded = day
        if trace is not None:
            trace.append({"day": day, "on_hand": h, "backorder": b, "on_order": o, "position": h + o - b,
                          "issue_qty": sum(by_day.get(day, [])), "order_qty": orders[-1][1] if orders and orders[-1][0] == day else 0})
        day += 1
    carry(horizon)

    total = sum(q for _, q in lines)
    open_orders = sum(1 for due, _, _ in arrivals)
    ordered = sum(q for _, q, _ in orders)
    result = SimResult(
        horizon=horizon, total_issues=total, n_lines=len(lines), served_on_day=served, lines_full=int(lines_full), backfilled=backfilled, lost=lost,
        avg_on_hand=sum_h / horizon, avg_backorder=sum_b / horizon, ready_days=ready, zero_on_hand_days=zero, stockout_days=stock_days, stockout_periods=periods, longest_stockout=longest,
        first_stockout_day=first_stockout, orders_placed=len(orders), order_quantity_total=ordered, orders_open_at_end=open_orders, first_order_day=orders[0][0] if orders else None,
        first_arrival_day=first_arrival, arrived_total=arrived, end_on_hand=h, end_backorder=b, end_on_order=o, p95_on_hand=_percentile_from_hist(hist, 0.95),
        days_above_max=int(above_days), mean_units_above_max=above_units / horizon, issues_after_first_arrival=issues_after, served_after_first_arrival=served_after,
        stockout_days_after_first_arrival=stock_after, orders=orders, trace=trace)
    check_conservation(result, initial, shortage)
    return result


def check_conservation(r: SimResult, initial: float, shortage: str) -> None:
    """Design section 7. Raises if any law fails. Bounds on state are enforced by construction and tested separately."""
    if abs(initial + r.arrived_total - (r.end_on_hand + r.served_on_day + r.backfilled)) > 1e-9:
        raise ConservationError("stock")
    if shortage == BACKORDER and abs(r.total_issues - (r.served_on_day + r.backfilled + r.end_backorder)) > 1e-9:
        raise ConservationError("demand, backorder mode")
    if shortage == LOST_SALES and (abs(r.total_issues - (r.served_on_day + r.lost)) > 1e-9 or r.end_backorder != 0):
        raise ConservationError("demand, lost sales mode")
    if abs(r.order_quantity_total - (r.arrived_total + r.end_on_order)) > 1e-9:
        raise ConservationError("orders")
