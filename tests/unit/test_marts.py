"""Mart logic on small data with hand-calculated answers, through the real staging and conform code."""
import statistics
from datetime import datetime as D

import pandas as pd
import pytest

from src.data.ingest import stage_table
from src.data.schemas import BOM, FUNCLOC, MITEM, MOVEMENT, NOTIF, PRPO
from src.marts.build import build_marts
from src.marts.demand import build_demand_month, compare_scenarios, impact_sensitivity
from src.marts.movement_copies import ADJACENT, FAR, FIRST, NEAR, SCENARIO_A, SCENARIO_B, UNIQUE, classify_movement_copies, demand_months
from src.preprocessing.conform import build_conformed
from src.validation.duplicates import add_duplicate_columns

M1, M2, M3 = "4100000001", "4100000002", "4100000003"
JAN, FEB = D(2026, 1, 7), D(2026, 2, 3)


def _stage(spec, rows):
    return stage_table(pd.DataFrame(rows, columns=spec.source_columns, dtype=object), spec)


def _issue(day, material, quantity, order, unit="EA"):
    return [day, "Issue", material, "Part", quantity, unit, order]


MOVEMENT_ROWS = [
    _issue(JAN, M1, 10, "201000000001"),                 # row 2: earliest of three
    _issue(JAN, M1, 10, "201000000001"),                 # row 3: adjacent copy
    _issue(JAN, M1, 5, "201000000001"),                  # row 4: same key, different quantity. Not a copy
    _issue(FEB, M2, 7, "201000000002", "KG"),            # row 5: earliest of two
    _issue(D(2026, 3, 1), M1, 1, "201000000003"),        # row 6
    _issue(D(2026, 3, 2), M1, 2, "201000000003"),        # row 7
    _issue(FEB, M2, 7, "201000000002", "KG"),            # row 8: near copy, gap 3
    *[_issue(D(2026, 4, day), M1, 1, "201000000004") for day in range(1, 9)],  # rows 9 to 16
    _issue(JAN, M1, 10, "201000000001"),                 # row 17: far copy, gap 14 from row 3
    _issue(D(2027, 1, 1), M1, 99, "201000000005"),       # row 18: outside the window
    _issue(D(2026, 5, 1), M1, 0, "201000000006"),        # row 19: zero quantity
    _issue(D(2026, 5, 2), M1, 4, "201000000007", "KG"),  # row 20: wrong unit
]


def _pr(pr, item, quantity, amount, delivery, promised, material=M1, currency="IDR", supplier="100001"):
    return ["PR01", pr, item, D(2026, 1, 10), material, "Part", quantity, "EA", delivery, "1000", "G1", "4500000001", item, supplier, "Acme", amount, currency, promised]


@pytest.fixture(scope="module")
def tables():
    source = {
        "bom": _stage(BOM, [["PX_A", M1, "Part", 1.0, "EA", 1, 5, 2.0, "Stock Item"], ["PX_A", M2, "Part", 1.0, "KG", 0, 0, 3.0, "Non Stock"], ["PX_B", M3, "Part", 1.0, "EA", 0, 0, 0.0, "Stock Item"]]),
        "funcloc": _stage(FUNCLOC, [["PX_A", "Pump", "A"], ["PX_B", "Valve", "B"]]),
        "movement": _stage(MOVEMENT, MOVEMENT_ROWS),
        "notif": _stage(NOTIF, [[D(2026, 1, 1), "101000000001", "N1", "201000000001", "High", "PX_A", "Check", D(2026, 1, 1), D(2026, 1, 2), D(2026, 1, 5), D(2026, 1, 9), "Complete"]]),
        "mitem": _stage(MITEM, [["PX_A", "Pump", "A", "300000000001", "10001", "Inspect", "1", "2 WEEKLY", D(2025, 1, 1)]]),
        "prpo": _stage(PRPO, [
            _pr("1000000001", "10", 4, 100.0, D(2026, 1, 15), D(2026, 1, 20)),
            _pr("1000000001", "10", 4, 100.0, D(2026, 1, 15), D(2026, 1, 20)),
            _pr("1000000001", "20", 10, 500.0, D(2026, 1, 5), D(2026, 1, 8)),
            _pr("1000000001", "30", 2, 300.0, D(2026, 2, 1), D(2026, 2, 9)),
        ]),
    }
    labelled = {k: add_duplicate_columns(v, k[:3].upper()) for k, v in source.items()}
    return build_marts(build_conformed(source, labelled)["tables"])["tables"]


def _row(frame, **keys):
    for column, value in keys.items():
        frame = frame[frame[column] == value]
    assert len(frame) == 1
    return frame.iloc[0]


def test_classification_keeps_every_row_and_labels_each(tables):
    frame = tables["movement_copy_classification"]
    assert frame["source_row"].tolist() == list(range(2, 21))
    assert frame["copy_class"].tolist()[:7] == [FIRST, ADJACENT, UNIQUE, FIRST, UNIQUE, UNIQUE, NEAR]
    assert _row(frame, source_row=17)["copy_class"] == FAR
    assert _row(frame, source_row=17)["copy_gap_rows"] == 14
    assert frame["copy_classification_reason"].notna().all()


def test_reason_names_the_rule_and_the_earlier_row(tables):
    reason = _row(tables["movement_copy_classification"], source_row=3)["copy_classification_reason"]
    assert "Rule C1" in reason and "source row 2" in reason and "1 row after" in reason and "Not proven to be an error" in reason


def test_same_key_with_a_different_quantity_is_not_a_copy(tables):
    row = _row(tables["movement_copy_classification"], source_row=4)
    assert row["is_partial_dup_group"] and not row["is_copy_c1"] and row["in_scenario_b"]


def test_ineligible_rows_are_kept_labelled_and_in_neither_scenario(tables):
    frame = tables["movement_copy_classification"]
    assert _row(frame, source_row=18)["eligibility_rules_failed"] == "E2"
    assert _row(frame, source_row=19)["eligibility_rules_failed"] == "E3"
    assert _row(frame, source_row=20)["eligibility_rules_failed"] == "E5"
    for source_row in (18, 19, 20):
        row = _row(frame, source_row=source_row)
        assert not row["in_scenario_a"] and not row["in_scenario_b"]


def test_scenario_membership_by_hand(tables):
    frame = tables["movement_copy_classification"]
    assert frame.loc[frame["in_scenario_a"], "source_row"].tolist() == list(range(2, 18))
    assert frame.loc[frame["in_scenario_b"], "source_row"].tolist() == [2, 4, 5, 6, 7, *range(9, 17)]


def test_month_tables_are_zero_filled_only_inside_the_window_for_issued_materials(tables):
    for scenario in (SCENARIO_A, SCENARIO_B):
        month = tables[f"mart_material_demand_month__{scenario}"]
        assert len(month) == 2 * 17 and set(month["material_no"]) == {M1, M2}  # M3 was never issued
        assert month["month"].min() == pd.Timestamp("2025-05-01") and month["month"].max() == pd.Timestamp("2026-09-01")


def test_monthly_values_by_hand(tables):
    a, b = tables[f"mart_material_demand_month__{SCENARIO_A}"], tables[f"mart_material_demand_month__{SCENARIO_B}"]
    jan = pd.Timestamp("2026-01-01")
    row_a, row_b = _row(a, material_no=M1, month=jan), _row(b, material_no=M1, month=jan)
    assert (row_a["qty_issued"], row_a["n_issue_lines"], row_a["n_orders"], row_a["n_repeat_lines_included"]) == (35, 4, 1, 2)
    assert (row_b["qty_issued"], row_b["n_issue_lines"], row_b["n_orders"], row_b["n_repeat_lines_included"]) == (15, 2, 1, 0)
    assert row_a["n_orders_with_notification"] == 1
    empty = _row(a, material_no=M1, month=pd.Timestamp("2025-06-01"))
    assert empty["is_zero_filled"] and empty["qty_issued"] == 0 and empty["n_issue_lines"] == 0


def test_summary_statistics_by_hand(tables):
    a = _row(tables[f"mart_material_demand_summary__{SCENARIO_A}"], material_no=M1)
    series = [35, 3, 8] + [0] * 14
    assert a["qty_issued_total"] == 46 and a["n_issue_lines"] == 14 and a["months_with_issue"] == 3 and a["months_in_window"] == 17
    assert a["mean_monthly_qty"] == pytest.approx(statistics.mean(series), abs=1e-5)
    assert a["std_monthly_qty"] == pytest.approx(statistics.stdev(series), abs=1e-5)
    assert a["mean_active_month_qty"] == pytest.approx(46 / 3, abs=1e-5)
    assert a["max_monthly_qty"] == 35 and a["max_line_qty"] == 10
    assert a["first_issue_date"] == pd.Timestamp(JAN) and a["last_issue_date"] == pd.Timestamp("2026-04-08")
    assert not a["flag_sparse_history"]
    assert _row(tables[f"mart_material_demand_summary__{SCENARIO_B}"], material_no=M2)["flag_sparse_history"]


def test_comparison_by_hand(tables):
    frame = tables["mart_material_demand_comparison"]
    one = _row(frame, material_no=M1)
    assert (one["qty_scenario_a"], one["qty_scenario_b"], one["qty_diff_abs"]) == (46, 26, 20)
    assert one["qty_diff_pct_of_a"] == pytest.approx(43.4783) and one["qty_diff_pct_of_b"] == pytest.approx(76.9231)
    assert (one["lines_scenario_a"], one["lines_scenario_b"], one["lines_diff_abs"]) == (14, 12, 2)
    assert one["months_with_difference"] == 1 and one["max_month_qty_diff_abs"] == 20
    assert (one["qty_copy_class_adjacent"], one["qty_copy_class_near"], one["qty_copy_class_far"]) == (10, 0, 10)
    assert one["impact_tier"] == "high" and one["is_materially_affected"] and not one["flag_low_line_count"]
    two = _row(frame, material_no=M2)
    assert two["qty_diff_abs"] == 7 and two["qty_diff_pct_of_a"] == 50 and two["qty_diff_pct_of_b"] == 100 and two["flag_low_line_count"]
    assert two["qty_copy_class_near"] == 7
    assert "Few lines" in two["impact_reason"]


def test_impact_tier_boundaries():
    months = demand_months()
    cases = {"no": (100, 100), "low": (100, 91), "ten": (100, 90), "high": (100, 75)}
    def summary(index):
        rows = [{"material_no": k, "unit": "EA", "mrp_type": "Stock Item", "material_prefix": "4100", "qty_issued_total": v[index], "n_issue_lines": 10, "mean_monthly_qty": 1.0, "std_monthly_qty": 1.0, "max_monthly_qty": 1.0, "months_with_issue": 1} for k, v in cases.items()]
        return pd.DataFrame(rows).astype({"qty_issued_total": "Int64", "n_issue_lines": "Int64"})
    month = pd.DataFrame({"material_no": list(cases), "month": months[0], "qty_issued": pd.array([1] * 4, dtype="Int64")})
    classification = pd.DataFrame({"is_copy_c1": [False], "is_eligible_demand": [True], "copy_class": ["unique_record"], "material_no": ["no"], "quantity": pd.array([1], dtype="Int64")})
    frame = compare_scenarios(summary(0), summary(1), month, month, classification).set_index("material_no")
    assert frame["impact_tier"].to_dict() == {"high": "high", "low": "below_threshold", "no": "no_change", "ten": "material"}
    assert frame["is_materially_affected"].to_dict() == {"high": True, "low": False, "no": False, "ten": True}
    table = impact_sensitivity(frame.reset_index().assign(flag_low_line_count=False)).set_index("threshold_pct")
    assert table.loc[10.0, "materials_at_or_above"] == 2 and table.loc[25.0, "materials_at_or_above"] == 1 and table.loc[1.0, "materials_at_or_above"] == 3


def test_copies_never_change_which_months_are_active(tables):
    frame = tables["mart_material_demand_comparison"]
    assert frame["months_with_issue"].tolist() == frame["months_with_issue_scenario_b"].tolist()


def test_procurement_views_and_unit_amount_by_hand(tables):
    original, distinct = tables["mart_procurement_line__original_rows"], tables["mart_procurement_line__exact_distinct_rows"]
    assert len(original) == 4 and len(distinct) == 3
    assert set(original["analysis_view"]) == {"original_rows"} and set(distinct["analysis_view"]) == {"exact_distinct_rows"}
    assert _row(distinct, pr_item="30")["implied_unit_amount_scenario"] == 150
    assert _row(distinct, pr_item="10")["occurrence_count"] == 2


def test_supplier_material_by_hand_excludes_early_dates_from_intervals_only(tables):
    a = _row(tables["mart_supplier_material__original_rows"], material_no=M1)
    b = _row(tables["mart_supplier_material__exact_distinct_rows"], material_no=M1)
    assert (a["n_lines"], b["n_lines"]) == (4, 3)
    assert (a["pr_quantity_total"], b["pr_quantity_total"]) == (20, 16)
    assert (a["po_item_amount_total"], b["po_item_amount_total"]) == (1000, 900)
    # Promised intervals in days: 10, 10, -2, 30. The -2 is set aside, but its line stays counted.
    assert (a["n_lines_used_for_promised_interval"], b["n_lines_used_for_promised_interval"]) == (3, 2)
    assert a["promised_interval_days_median"] == 10 and b["promised_interval_days_median"] == 20
    assert a["promised_interval_days_min"] == 10 and a["promised_interval_days_max"] == 30
    # Requested intervals: 5, 5, -5, 22. The -5 is set aside.
    assert (a["requested_interval_days_median"], b["requested_interval_days_median"]) == (5, 13.5)


def test_inventory_holds_blanks_for_no_record_and_state_from_the_dimension(tables):
    frame = tables["mart_material_inventory"].set_index("material_no")
    assert len(frame) == 3
    assert frame.loc[M1, "stock"] == 2 and frame.loc[M1, "min_qty"] == 1
    assert frame.loc[M1, "qty_issued_total__scenario_a"] == 46 and frame.loc[M1, "qty_issued_total__scenario_b"] == 26
    assert frame.loc[M1, "n_pr_lines__original_rows"] == 4 and frame.loc[M1, "n_pr_lines__exact_distinct_rows"] == 3
    assert frame.loc[M1, "supplier_code"] == "100001"
    assert pd.isna(frame.loc[M3, "qty_issued_total__scenario_a"]) and pd.isna(frame.loc[M3, "n_pr_lines__original_rows"])
    assert frame.loc[M1, "demand_impact_tier"] == "high"


def test_simulation_gaps_name_what_is_missing(tables):
    frame = tables["mart_material_inventory"].set_index("material_no")
    assert pd.isna(frame.loc[M1, "simulation_inputs_missing"])
    assert frame.loc[M2, "simulation_inputs_missing"] == "promised_interval;unit_amount;min_or_max"
    assert frame.loc[M3, "simulation_inputs_missing"] == "demand_history;promised_interval;unit_amount;min_or_max"


def test_months_are_seventeen():
    assert len(demand_months()) == 17


def test_build_month_fails_loudly_for_an_unknown_scenario(tables):
    with pytest.raises(KeyError):
        build_demand_month(tables["movement_copy_classification"], "scenario_c", pd.DataFrame())
