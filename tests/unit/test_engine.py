"""Deterministic engine against hand calculations, including design section 11, plus failure cases."""
import random
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).parent))
from independent_engine import run_daily, same_as_engine  # noqa: E402

from src.simulation.engine import BACKORDER, LOST_SALES, ConservationError, Policy, check_conservation, lead_days, reference_levels, scale_lines, simulate  # noqa: E402
from src.simulation.mc import simulate_batch  # noqa: E402

EXAMPLE = [(0, 1), (1, 2), (2, 5), (4, 1)]


def test_worked_example_backorder_every_number():
    r = simulate(EXAMPLE, 3, Policy(2, S=6), 2, horizon=6, keep_trace=True)
    assert r.fill_rate_quantity == pytest.approx(8 / 9)
    assert r.fill_rate_lines == 0.75
    assert r.ready_rate == 0.5
    assert r.avg_on_hand == 2
    assert (r.stockout_periods, r.stockout_days, r.zero_on_hand_days, r.orders_placed) == (1, 2, 3, 2)
    assert [(d, q, due) for d, q, due in r.orders] == [(0, 4, 2), (2, 7, 4)]
    assert (r.end_on_hand, r.end_backorder, r.end_on_order) == (5, 0, 0)
    assert 3 + r.arrived_total == 14 == r.end_on_hand + r.served_on_day + r.backfilled
    assert r.total_issues == 9 == r.served_on_day + r.backfilled + r.end_backorder
    by_day = {t["day"]: t for t in r.trace}
    assert [by_day[d]["on_hand"] for d in (0, 1, 2, 4)] == [2, 0, 0, 5]
    assert by_day[2]["position"] == 6 and by_day[2]["backorder"] == 1


def test_worked_example_lost_sales_every_number():
    r = simulate(EXAMPLE, 3, Policy(2, S=6), 2, horizon=6, shortage=LOST_SALES)
    assert r.fill_rate_quantity == pytest.approx(8 / 9)
    assert r.lost == 1 and r.stockout_days == 1 and r.end_backorder == 0
    assert [(d, q, due) for d, q, due in r.orders] == [(0, 4, 2), (2, 6, 4)]
    assert r.avg_on_hand == pytest.approx(12 / 6)
    assert 3 + r.arrived_total == 13 == r.end_on_hand + r.served_on_day


def test_same_day_arrival_serves_that_days_issue():
    r = simulate([(2, 4)], 0, Policy(0, S=4), 2, horizon=4)  # Day-0 order of 4 arrives on day 2, the same day as the issue.
    assert r.fill_rate_quantity == 1 and r.stockout_days == 0


def test_backorders_are_served_before_new_issues():
    r = simulate([(0, 3), (2, 2)], 0, Policy(0, S=2), 2, horizon=5)
    # Day 0: initial review orders 2, due day 2. Short 3, B=3, IP=-1, order 3, due day 2.
    # Day 2: 5 arrive, repay 3, serve 2, H=0, IP=0, order 2, due day 4. Day 4: H=2.
    assert r.served_on_day == 2 and r.backfilled == 3 and r.end_backorder == 0
    assert [o[1] for o in r.orders] == [2, 3, 2] and r.end_on_hand == 2


def test_crossing_orders_later_order_arrives_first():
    leads = {0: 6, 1: 1}
    r = simulate([(0, 3), (1, 3)], 3, Policy(0, S=3), lambda i, _d: leads[i], horizon=9)
    # Day 0: H=0, IP=0 -> order 3 due day 6. Day 1: short 3, B=3, IP=0 -> order 3 due day 2.
    assert [o[2] for o in r.orders] == [6, 2]
    assert r.first_arrival_day == 2
    assert r.end_on_hand == 3 and r.end_backorder == 0


def test_issue_larger_than_order_up_to_level():
    r = simulate([(0, 20)], 5, Policy(2, S=6), 3, horizon=10)
    # Served 5. B=15, IP=-15 -> order 21. Arrives day 3, repays 15, H=6.
    assert r.served_on_day == 5 and r.orders[0][1] == 21 and r.end_on_hand == 6 and r.stockout_days == 3


def test_zero_stock_on_day_zero_orders_at_initial_review():
    r = simulate([], 0, Policy(1, S=5), 2, horizon=5)
    assert r.first_order_day == 0 and r.orders_placed == 1 and r.end_on_hand == 5 and r.fill_rate_quantity is None
    assert r.zero_on_hand_days == 2


def test_lead_longer_than_horizon_never_arrives():
    r = simulate([(0, 5)], 0, Policy(0, S=5), 600, horizon=10)
    # Initial review orders 5. The issue then takes position to 0, so a second order of 5 is placed. Neither arrives.
    assert r.arrived_total == 0 and r.orders_open_at_end == 2 and r.end_on_order == 10 and r.first_arrival_day is None


def test_no_demand_no_order_above_s():
    r = simulate([], 10, Policy(2, S=6), 2, horizon=10)
    assert r.orders_placed == 0 and r.avg_on_hand == 10 and r.stockout_days == 0


def test_very_large_stock_gives_full_fill_and_no_order():
    r = simulate(EXAMPLE, 1000, Policy(2, S=6), 2, horizon=6)
    assert r.fill_rate_quantity == 1 and r.orders_placed == 0


def test_r2_repeats_fixed_quantity_until_above_s():
    r = simulate([(0, 9)], 2, Policy(3, Q=4), 2, horizon=6)
    # Initial review: IP=2, one step of 4 brings it to 6. Then served 2, B=7, IP=4+0-7=-3: two steps of 4 bring it to 5.
    assert [o[1] for o in r.orders] == [4, 8]


def test_several_stockout_periods_and_longest_run():
    r = simulate([(1, 3), (6, 3)], 0, Policy(0, S=3), 2, horizon=10)
    # Day 0 order 3 due 2. Day 1 short 3. IP stays 0 -> order 3 due 3.
    assert r.stockout_periods == 1 and r.stockout_days == 1 and r.longest_stockout == 1
    s = simulate([(1, 1), (5, 1)], 0, Policy(-1, S=1), 2, horizon=10)
    # s=-1: order only once position falls to -1. Day 1 short, IP=-1, order 2 due 3. Day 5 served from stock on hand.
    assert s.stockout_periods == 1 and s.stockout_days == 2


def test_after_first_arrival_measures_remove_the_opening_transient():
    r = simulate([(0, 3), (4, 3)], 0, Policy(0, S=3), 3, horizon=8)
    assert r.fill_rate_quantity == pytest.approx(0.5)
    assert r.first_arrival_day == 3
    assert r.fill_rate_after_first_arrival == 1


def test_reference_levels_lead_rounding_and_scaling_by_hand():
    assert reference_levels(5, 9) == (5, 9)
    assert reference_levels(5, 5) == (5, 6)
    assert reference_levels(3, 9, 0.5, 0.5) == (2, 5)
    assert reference_levels(0, 0) == (0, 1)
    assert lead_days(42.5) == 43 and lead_days(0) == 1 and lead_days(10, 0.5) == 5
    assert scale_lines([(0, 1), (1, 1), (2, 1), (3, 1)], 0.75) == [(0, 1), (1, 1), (3, 1)]
    assert sum(q for _, q in scale_lines([(d, 3) for d in range(10)], 1.25)) == 38


@pytest.mark.parametrize("bad", [dict(S=None, Q=None), dict(S=3, Q=3), dict(S=2), dict(Q=0)])
def test_policy_rejects_impossible_settings(bad):
    with pytest.raises(ValueError):
        Policy(2, **bad)


def test_engine_rejects_bad_inputs():
    with pytest.raises(ValueError):
        simulate([(0, 1)], -1, Policy(1, S=2), 1)
    with pytest.raises(ValueError):
        simulate([(0, -1)], 1, Policy(1, S=2), 1)
    with pytest.raises(ValueError):
        simulate([(600, 1)], 1, Policy(1, S=2), 1, horizon=10)


def test_conservation_check_catches_damage():
    r = simulate(EXAMPLE, 3, Policy(2, S=6), 2, horizon=6)
    r.end_on_hand += 1
    with pytest.raises(ConservationError):
        check_conservation(r, 3, BACKORDER)
    r2 = simulate(EXAMPLE, 3, Policy(2, S=6), 2, horizon=6)
    r2.order_quantity_total += 1
    with pytest.raises(ConservationError):
        check_conservation(r2, 3, BACKORDER)


def _random_case(rng):
    horizon = rng.randint(5, 60)
    lines = sorted((rng.randrange(horizon), rng.randint(1, 15)) for _ in range(rng.randint(0, 25)))
    s = rng.randint(0, 12)
    return horizon, lines, s, rng.randint(0, 30), rng.randint(1, 15), rng.randint(1, 20)


@pytest.mark.parametrize("seed", range(150))
def test_event_engine_equals_independent_daily_loop(seed):
    rng = random.Random(seed)
    horizon, lines, s, initial, step, lead = _random_case(rng)
    for shortage, lost in ((BACKORDER, False), (LOST_SALES, True)):
        for policy, S, Q in ((Policy(s, S=s + step), s + step, None), (Policy(s, Q=step), None, step)):
            cap = s + step
            a = simulate(lines, initial, policy, lead, horizon=horizon, shortage=shortage, recorded_max=cap)
            b = run_daily(lines, initial, s, S, Q, lead, horizon, lost, cap)
            assert same_as_engine(a, b) == [], (seed, shortage, S, Q)


@pytest.mark.parametrize("seed", range(40))
def test_state_bounds_hold(seed):
    rng = random.Random(1000 + seed)
    horizon, lines, s, initial, step, lead = _random_case(rng)
    r = simulate(lines, initial, Policy(s, S=s + step), lead, horizon=horizon, keep_trace=True)
    assert all(t["on_hand"] >= 0 and t["backorder"] >= 0 and t["on_order"] >= 0 for t in r.trace)
    assert all(t["position"] == t["on_hand"] + t["on_order"] - t["backorder"] for t in r.trace)


@pytest.mark.parametrize("seed", range(40))
def test_vector_batch_equals_scalar_engine(seed):
    rng = random.Random(2000 + seed)
    horizon, lines, s, initial, step, lead = _random_case(rng)
    path = np.zeros((3, horizon))
    for day, qty in lines:
        path[:, day] += qty
    for policy, S, Q in ((Policy(s, S=s + step), s + step, None), (Policy(s, Q=step), None, step)):
        a = simulate(lines, initial, policy, lead, horizon=horizon, recorded_max=s + step)
        b = simulate_batch(path, initial, s, S, Q, lead, s + step)
        assert b["orders"][0] == a.orders_placed and b["stockout_days"][0] == a.stockout_days and b["zero_on_hand_days"][0] == a.zero_on_hand_days
        assert b["mean_on_hand"][0] == pytest.approx(a.avg_on_hand) and b["mean_backorder"][0] == pytest.approx(a.avg_backorder)
        assert b["shortage_quantity"][0] == pytest.approx(a.shortage_quantity) and b["ordered"][0] == pytest.approx(a.order_quantity_total)
        assert b["days_above_max"][0] == a.days_above_max and b["units_above_max"][0] == pytest.approx(a.mean_units_above_max)
        assert b["any_shortfall"][0] == (a.stockout_days > 0)
        assert b["end_on_hand"][0] == a.end_on_hand and b["end_on_order"][0] == a.end_on_order
        assert b["backfilled"][0] == pytest.approx(a.backfilled) and b["arrived"][0] == pytest.approx(a.arrived_total)


def test_batch_keeps_two_orders_due_on_the_same_day():
    """Regression: the initial review and the day-0 review share a due day. The second must not overwrite the first."""
    path = np.zeros((1, 6))
    path[0, 0] = 5
    a = simulate([(0, 5)], 3, Policy(4, S=8), 2, horizon=6)
    b = simulate_batch(path, 3, 4, 8, None, 2)
    assert len(a.orders) == 2 and a.orders[0][2] == a.orders[1][2]
    # Initial review orders 5. Issue: served 3, B=2, IP=3, order 5. Day 2: 10 arrive, repay 2, H=8. With the bug, 5 arrive and H=3.
    assert b["end_on_hand"][0] == a.end_on_hand == 8
    assert b["arrived"][0] == a.arrived_total == 10
