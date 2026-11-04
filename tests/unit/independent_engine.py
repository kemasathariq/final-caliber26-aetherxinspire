"""A second implementation of the inventory recursion, written separately from src/simulation/engine.py and importing nothing from it.

It walks every day, keeps open orders in a plain list and derives every measure afterwards from end-of-day arrays. Agreement with the event-driven engine on all of R0 is design section 12.1.
"""


def run_daily(lines, initial, s, S, Q, lead, horizon=518, lost_sales=False, cap=None):
    per_day = [[] for _ in range(horizon)]
    for day, qty in lines:
        per_day[day].append(qty)
    on_hand, back, open_orders = initial, 0, []
    end_h, end_b, end_o, day_lost, day_served, day_demand = [], [], [], [], [], []
    orders, arrived_days, full_lines = [], [], 0

    def maybe_order(day):
        position = on_hand + sum(q for _, q in open_orders) - back
        if position <= s:
            if S is not None:
                quantity = S - position
            else:
                quantity = 0
                while position + quantity <= s:
                    quantity += Q
            if quantity > 0:
                open_orders.append((day + lead, quantity))
                orders.append((day, quantity))

    maybe_order(0)
    for day in range(horizon):
        due = [o for o in open_orders if o[0] == day]
        open_orders = [o for o in open_orders if o[0] != day]
        for _, quantity in due:
            on_hand += quantity
            arrived_days.append(day)
        repaid = min(on_hand, back)
        on_hand, back = on_hand - repaid, back - repaid
        served_today, lost_today = 0, 0
        for quantity in per_day[day]:
            given = min(on_hand, quantity)
            on_hand -= given
            served_today += given
            full_lines += given == quantity
            if lost_sales:
                lost_today += quantity - given
            else:
                back += quantity - given
        maybe_order(day)
        end_h.append(on_hand)
        end_b.append(back)
        end_o.append(sum(q for _, q in open_orders))
        day_lost.append(lost_today)
        day_served.append(served_today)
        day_demand.append(sum(per_day[day]))

    out_day = [(l > 0) if lost_sales else (b > 0) for l, b in zip(day_lost, end_b)]
    runs, length, longest = 0, 0, 0
    for flag in out_day:
        if flag:
            runs += length == 0
            length += 1
            longest = max(longest, length)
        else:
            length = 0
    total = sum(day_demand)
    first_arrival = min(arrived_days) if arrived_days else None
    return {
        "fill": sum(day_served) / total if total else None, "lines": full_lines / len(lines) if lines else None, "ready": sum(h > 0 for h in end_h) / horizon, "avg_h": sum(end_h) / horizon, "avg_b": sum(end_b) / horizon,
        "stock_days": sum(out_day), "periods": runs, "longest": longest, "first_out": out_day.index(True) if any(out_day) else None, "zero": sum(h == 0 for h in end_h), "orders": len(orders), "ordered": sum(q for _, q in orders),
        "first_order": orders[0][0] if orders else None, "open_end": len(open_orders), "end_h": end_h[-1], "end_b": end_b[-1], "end_o": end_o[-1], "lost": sum(day_lost), "shortage": total - sum(day_served),
        "first_arrival": first_arrival, "above_days": 0 if cap is None else sum(h > cap for h in end_h), "above_units": 0 if cap is None else sum(max(h - cap, 0) for h in end_h) / horizon,
        "stock_after": sum(f for d, f in enumerate(out_day) if first_arrival is not None and d >= first_arrival),
    }


def same_as_engine(result, independent, tolerance=1e-9) -> list[str]:
    """Names of measures where the two implementations disagree."""
    pairs = {
        "fill": result.fill_rate_quantity, "lines": result.fill_rate_lines, "ready": result.ready_rate, "avg_h": result.avg_on_hand, "avg_b": result.avg_backorder, "stock_days": result.stockout_days, "periods": result.stockout_periods, "longest": result.longest_stockout, "first_out": result.first_stockout_day,
        "zero": result.zero_on_hand_days, "orders": result.orders_placed, "ordered": result.order_quantity_total, "first_order": result.first_order_day, "open_end": result.orders_open_at_end, "end_h": result.end_on_hand, "end_b": result.end_backorder, "end_o": result.end_on_order, "lost": result.lost, "shortage": result.shortage_quantity,
        "first_arrival": result.first_arrival_day, "above_days": result.days_above_max, "above_units": result.mean_units_above_max, "stock_after": result.stockout_days_after_first_arrival,
    }
    bad = []
    for key, value in pairs.items():
        other = independent[key]
        if value is None or other is None:
            if value is not other:
                bad.append(key)
        elif abs(value - other) > tolerance:
            bad.append(key)
    return bad
