"""Feasibility evidence on small data with hand-calculated answers. No simulation exists to test."""
import pandas as pd

from src.simulation_design import feasibility as f

M = [f"41000000{i:02d}" for i in range(1, 8)]


def _inventory():
    rows = [
        # material, mrp, stock, min, max, issued a, issued b, lines a, lines b, active, missing
        (M[0], "Stock Item", 10, 2, 6, 5, 5, 3, 3, 6, None),               # stock - 5 = 5 > 2. Never reaches Min. Above Max
        (M[1], "Stock Item", 2, 2, 6, 9, 7, 8, 7, 2, None),                # At Min on day 0. Scenarios differ
        (M[2], "Stock Item", 9, 2, 6, 7, 6, 4, 3, 1, None),                # A: 2 is not > 2, reaches Min. B: 3 > 2, never reaches it
        (M[3], "Non Stock", 3, 0, 0, 1, 1, 1, 1, 1, "min_or_max"),         # Not a Stock Item, and no Min or Max
        (M[4], "Stock Item", 3, 1, 2, None, None, None, None, None, "demand_history"),
        (M[5], "Stock Item", 3, 1, 2, 4, 4, 4, 4, 4, "promised_interval;unit_amount"),
        (M[6], "Non Stock", 1, 1, 2, None, None, None, None, None, "demand_history;promised_interval;unit_amount"),
    ]
    frame = pd.DataFrame(rows, columns=["material_no", "mrp_type", "stock", "min_qty", "max_qty", "qty_issued_total__scenario_a", "qty_issued_total__scenario_b", "n_issue_lines__scenario_a", "n_issue_lines__scenario_b", "months_with_issue", "simulation_inputs_missing"])
    frame = frame.astype({"material_no": "string", "mrp_type": "category", "simulation_inputs_missing": "string", "stock": "Float64", "min_qty": "Int64", "max_qty": "Int64", "qty_issued_total__scenario_a": "Int64", "qty_issued_total__scenario_b": "Int64",
                          "n_issue_lines__scenario_a": "Int64", "n_issue_lines__scenario_b": "Int64", "months_with_issue": "Int64"})
    frame["unit"] = pd.Categorical(["EA"] * len(frame))
    lead = pd.array([40.0, 700.0, 10.0, None, None, None, None], dtype="Float64")
    frame["promised_interval_days_median__original_rows"] = lead
    frame["promised_interval_days_median__exact_distinct_rows"] = lead
    frame["pr_quantity_median__exact_distinct_rows"] = pd.array([3.0, 7.0, 2.0, None, None, None, None], dtype="Float64")
    frame["demand_materially_affected"] = pd.array([False, True, True, False, None, False, None], dtype="boolean")
    frame["n_lines_at_repeated_unit_maximum"] = pd.array([0, 1, 0, 0, None, 0, None], dtype="Int64")
    return frame


def _build():
    supplier = pd.DataFrame({"material_no": M[:3], "n_lines_used_for_promised_interval": [12, 2, 3], "promised_interval_days_p90": [50.0, 800.0, 12.0]}).astype({"material_no": "string", "n_lines_used_for_promised_interval": "Int64", "promised_interval_days_p90": "Float64"})
    summary = pd.DataFrame({"material_no": M[:3] + [M[3], M[5]], "max_line_qty": [2.0, 9.0, 3.0, 1.0, 1.0]}).astype({"material_no": "string"})
    return f.build_simulation_population(_inventory(), summary, supplier).set_index("material_no")


def test_every_material_is_kept_with_its_status_and_reasons():
    frame = _build()
    assert len(frame) == 7
    assert frame["population_status"].tolist() == ["in_population"] * 3 + ["excluded"] * 4
    assert pd.isna(frame.loc[M[0], "exclusion_reasons"])
    assert frame.loc[M[3], "exclusion_reasons"] == "mrp_type_not_stock_item;min_and_max_both_zero"
    assert frame.loc[M[4], "exclusion_reasons"] == "no_demand_history"
    assert frame.loc[M[5], "exclusion_reasons"] == "no_promised_interval;no_unit_amount_record"
    assert frame.loc[M[6], "n_exclusion_reasons"] == 4


def test_never_reaches_min_uses_a_strict_comparison_and_each_scenario():
    frame = _build()
    assert frame.loc[M[0], "stays_above_min__scenario_a"] == True  # noqa: E712
    assert frame.loc[M[2], "stays_above_min__scenario_a"] == False  # noqa: E712  9 - 7 = 2, which is not above 2
    assert frame.loc[M[2], "stays_above_min__scenario_b"] == True  # noqa: E712  9 - 6 = 3


def test_day_zero_trigger_and_conflict_flags_by_hand():
    frame = _build()
    assert frame.loc[M[1], "at_or_below_min_at_start"] == True and frame.loc[M[0], "at_or_below_min_at_start"] == False  # noqa: E712
    assert frame.loc[M[0], "stock_above_max"] == True and frame.loc[M[1], "stock_above_max"] == False  # noqa: E712
    assert frame.loc[M[1], "single_line_exceeds_max"] == True and frame.loc[M[0], "single_line_exceeds_max"] == False  # noqa: E712
    assert frame.loc[M[1], "median_pr_quantity_exceeds_max"] == True and frame.loc[M[0], "median_pr_quantity_exceeds_max"] == False  # noqa: E712
    assert frame.loc[M[1], "lead_proxy_exceeds_horizon"] == True and frame.loc[M[0], "lead_proxy_exceeds_horizon"] == False  # noqa: E712


def test_identical_scenarios_are_identified():
    frame = _build()
    assert frame.loc[M[0], "scenarios_identical_by_construction"] == True and frame.loc[M[1], "scenarios_identical_by_construction"] == False  # noqa: E712


def test_evidence_tiers_follow_the_thresholds():
    frame = _build()
    assert frame.loc[M[0], "demand_evidence_tier"] == f.DEMAND_RESAMPLE and frame.loc[M[0], "lead_evidence_tier"] == f.LEAD_RESAMPLE and frame.loc[M[0], "resampling_allowed_both"]
    assert frame.loc[M[1], "demand_evidence_tier"] == f.DEMAND_FEW and frame.loc[M[1], "lead_evidence_tier"] == f.LEAD_THIN and not frame.loc[M[1], "resampling_allowed_both"]
    assert frame.loc[M[2], "demand_evidence_tier"] == f.DEMAND_SINGLE and frame.loc[M[2], "lead_evidence_tier"] == f.LEAD_FEW


def test_summary_counts_by_hand_and_ignores_excluded_materials():
    table = f.pre_analysis_summary(_build().reset_index()).set_index("condition")["materials"]
    assert table["Materials in the population"] == 3
    assert table["Scenarios A and B differ"] == 2 and table["Scenarios A and B identical by construction"] == 1
    assert table["Scenario choice changes whether Min is ever reached"] == 1
    assert table["Any of the three conflicts above"] == 3
    assert table["Resampling allowed for both"] == 1


def test_funnel_accounts_for_every_material_once():
    frame = _build().reset_index()
    funnel = f.population_funnel(frame)
    assert funnel["materials"].sum() == 7
    candidates = f.single_reason_candidates(frame).set_index("exclusion_reasons")["materials"]
    assert candidates["no_demand_history"] == 1


def test_this_module_reads_no_unit_amount_and_runs_no_engine():
    source = open(f.__file__).read()
    code = source.split('"""', 2)[2]
    assert "implied_unit_amount" not in code and "po_item_amount" not in code
    assert "heapq" not in code and "numpy" not in code and "default_rng" not in code
