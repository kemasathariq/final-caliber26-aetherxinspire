"""Parameters, resampling, forecasts, classes, abstention, rules, wording, contract and money boundaries, on small hand-calculated data."""
import json
import os
import subprocess
import sys

import numpy as np
import pandas as pd
import pytest

from src.config import PROJECT_ROOT
from src.simulation import checks, classification as cl, contract, decisions, forecast as fc, kpis, mc, parameters as pm, resampling as rs, samples
from src.simulation import settings as cfg


# Lead-time demand, reorder point and safety stock.
def test_lead_time_demand_by_hand():
    paths = np.array([[1.0, 2.0, 3.0, 4.0]])
    assert rs.lead_time_demand(paths, np.array([[2]]), np.array([[1]])).tolist() == [[5.0]]      # Days 1, 2.
    assert rs.lead_time_demand(paths, np.array([[3]]), np.array([[2]])).tolist() == [[8.0]]      # Days 2, 3, wrap to 0.
    assert rs.lead_time_demand(paths, np.array([[4]]), np.array([[0]])).tolist() == [[10.0]]     # Whole path once.
    assert rs.lead_time_demand(paths, np.array([[9]]), np.array([[1]])).tolist() == [[22.0]]     # Twice round, plus day 1.


def _estimate(mean=5.0, q=(8.0, 10.0, 12.0)):
    return pm.LtdEstimate(mean, 1.0, 5.0, 11.0, dict(zip(("X1", "X2", "X3"), q)), "median_promised_interval", 30, 5000)


def test_reorder_point_safety_stock_and_quantity_by_hand():
    levels = pm.proposed_levels(_estimate(), 6.5, 12)
    assert levels["X2"] == {"service_level": 0.95, "s": 10, "S": 17, "Q": 7, "safety_stock": 5.0, "flag_safety_stock_floored": False, "lead_time_demand_mean": 5.0, "lead_time_demand_quantile": 10.0, "S_capped_at_recorded_max": 12}
    assert levels["X1"]["s"] == 8 and levels["X3"]["s"] == 12
    assert levels["N1"]["s"] == 5 and levels["N1"]["S"] == 12 and levels["N1"]["service_level"] is None


def test_safety_stock_floors_at_zero_and_flags():
    level = pm.proposed_levels(_estimate(mean=9.0, q=(2.0, 3.0, 4.0)), 2, 5)["X1"]
    assert level["safety_stock"] == 0.0 and level["flag_safety_stock_floored"] is True
    assert level["s"] == 2


def test_recorded_levels_and_observed_order_size():
    levels = pm.recorded_policy_levels(5, 9, 3.5)
    assert levels["R1"] == {"s": 5, "S": 9, "Q": None}
    assert levels["R2"] == {"s": 5, "S": None, "Q": 4}


def test_estimate_quantiles_are_values_that_occur():
    lines = [(d, float(d % 7 + 1)) for d in range(0, 500, 11)]
    est = pm.estimate_ltd(lines, np.array([30.0]), "123", False)
    assert est.lead_days_median == 30 and est.n_draws == cfg.LTD_PATHS * cfg.LTD_WINDOWS_PER_PATH
    assert all(q == int(q) for q in est.quantiles.values())
    assert est.quantiles["X1"] <= est.quantiles["X2"] <= est.quantiles["X3"]


# Resampling boundaries.
def test_day_of_month_folds_past_the_end_of_a_short_month():
    table = np.zeros((2, 31))
    table[0, 30] = 7   # Day 31 of a 31-day source month.
    paths = rs.build_daily_paths(table, np.array([[0]]), [30])
    assert paths[0, 29] == 7 and paths.sum() == 7


def test_no_invented_values_every_resampled_line_comes_from_own_history():
    lines = [(10, 3.0), (40, 8.0), (100, 5.0), (250, 2.0), (400, 11.0)]
    table = rs.day_of_month_table(lines, cfg.MONTH_LENGTHS)
    sources = rs.draw_month_sources(200, 17, 17, rs.generator(rs.STREAM_BLOCKS, 99))
    paths = rs.build_daily_paths(table, sources, cfg.MONTH_LENGTHS)
    assert set(np.unique(paths)) <= {0.0, 3.0, 8.0, 5.0, 2.0, 11.0}


def test_lead_draws_stay_in_own_history_and_round_up():
    obs = np.array([10.0, 20.5, 30.0])
    draws = rs.lead_draws(obs, np.random.default_rng(1).random(1000))
    assert set(np.unique(draws)) == {10, 21, 30}


def test_block_draws_are_consecutive_months_with_wrap():
    sources = rs.draw_month_sources(50, 17, 17, rs.generator(rs.STREAM_BLOCKS, 1), block=3)
    assert sources.shape == (50, 17)
    for row in sources:
        for i in range(0, 15, 3):
            assert (row[i + 1] - row[i]) % 17 == 1 and (row[i + 2] - row[i + 1]) % 17 == 1


def test_fixed_seed_reproduces_and_a_different_seed_differs():
    a = rs.draw_month_sources(100, 17, 17, rs.generator(rs.STREAM_BLOCKS, 0))
    b = rs.draw_month_sources(100, 17, 17, rs.generator(rs.STREAM_BLOCKS, 0))
    c = rs.draw_month_sources(100, 17, 17, rs.generator(rs.STREAM_BLOCKS, 0, seed=7))
    assert (a == b).all() and not (a == c).all()


@pytest.mark.parametrize("hash_seed", ["1", "999"])
def test_reproducible_across_processes_and_hash_seeds(hash_seed):
    code = "from src.simulation import resampling as r; import hashlib; print(hashlib.sha256(r.draw_month_sources(50,17,17,r.generator(1,0)).tobytes()).hexdigest())"
    env = {**os.environ, "PYTHONHASHSEED": hash_seed}
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, env=env, cwd=PROJECT_ROOT, check=True).stdout.strip()
    import hashlib
    assert out == hashlib.sha256(rs.draw_month_sources(50, 17, 17, rs.generator(1, 0)).tobytes()).hexdigest()


def test_common_random_numbers_give_policies_the_same_demand():
    path = np.zeros((4, 30))
    path[:, 5] = 3
    path[:, 12] = [1, 2, 3, 4]
    a, b = mc.simulate_batch(path, 2, 1, 4, None, 3), mc.simulate_batch(path, 2, 2, 8, None, 3)
    assert (a["total"] == b["total"]).all()


def test_batch_with_per_order_lead_uses_the_draw_for_that_day():
    path = np.zeros((2, 10))
    path[:, 0] = 2
    leads = np.full((2, 10), 3)
    leads[1, 0] = 6
    out = mc.simulate_batch(path, 2, 0, 4, None, leads)
    assert out["end_on_hand"].tolist() == [4, 4]
    assert out["mean_on_hand"][0] > out["mean_on_hand"][1]


def test_lead_past_the_horizon_stays_on_order_in_batch():
    path = np.zeros((1, 5))
    out = mc.simulate_batch(path, 0, 0, 3, None, 100)
    assert out["end_on_order"][0] == 3 and out["end_on_hand"][0] == 0


# Forecast methods by hand.
def test_croston_sba_by_hand():
    # Positive at index 1 (size 2, interval 2) and 3 (size 4, gap 2). alpha 0.5: size 3, interval 2. SBA 0.75 x 3 / 2.
    assert fc.croston_sba([0, 2, 0, 4], alpha=0.5) == pytest.approx(0.75 * 3 / 2)
    assert fc.croston_sba([0, 0, 0]) == 0


def test_tsb_by_hand():
    # Start p = 0.5, size 2. Then 0: p .25. 2: p .625, size 2. 0: .3125. 4: .65625, size 3.
    assert fc.tsb([0, 2, 0, 4], alpha=0.5, beta=0.5) == pytest.approx(0.65625 * 3)
    assert fc.tsb([0, 0]) == 0


def test_pinball_by_hand():
    assert fc.pinball(10, 8, 0.9) == pytest.approx(1.8)
    assert fc.pinball(8, 10, 0.9) == pytest.approx(0.2)


def test_horizon_months_handles_missing_lead():
    assert fc.horizon_months(None) == 1 and fc.horizon_months(float("nan")) == 1 and fc.horizon_months(42) == 2 and fc.horizon_months(900) == 6


def test_preregistered_rule_rejects_bootstrap_that_loses_to_mean():
    row = lambda method, p5, p9: {"demand_scenario": "A", "demand_class": "D3", "method": method, "share_beating_mean_pinball_0.5": p5, "share_beating_mean_pinball_0.9": p9, "share_beating_mean_pinball_0.95": p9, "share_beating_mean_pinball_0.98": p9}  # noqa: E731
    chosen = fc.select_methods(pd.DataFrame([row("naive", 0.4, 0.1), row("croston_sba", 0.6, 0.4), row("tsb", 0.7, 0.4), row("mean", 0, 0), row("block_bootstrap", 0.8, 0.3)])).iloc[0]
    assert chosen.selected_point_method == "tsb" and not chosen.bootstrap_range_accepted
    fallback = fc.select_methods(pd.DataFrame([row("naive", 0.4, 0.1), row("croston_sba", 0.5, 0.4), row("tsb", 0.3, 0.4), row("mean", 0, 0), row("block_bootstrap", 0.8, 0.9)])).iloc[0]
    assert fallback.selected_point_method == "mean" and fallback.bootstrap_range_accepted


# Classification and abstention.
def test_demand_class_rules_by_hand():
    active = pd.Series([0, 1, 2, 3, 5, 6, 15, 15])
    pat = pd.Series([pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, "lumpy", "smooth", "erratic"], dtype="string")
    assert cl.demand_class(active, pat).tolist() == ["D0", "D1", "D1", "D2", "D2", "D3", "D4", "D3"]


def test_pattern_cutoffs_by_hand():
    adi = pd.Series([1.0, 1.0, 2.0, 2.0, 1.32])
    cv2 = pd.Series([0.1, 0.49, 0.1, 0.9, 0.1])
    assert cl.pattern(adi, cv2).tolist() == ["smooth", "erratic", "intermittent", "lumpy", "intermittent"]


# Recommendation rules.
def test_action_rule_table_by_hand():
    assert decisions.action_for_grade_a(5, 10, 20, 0.3, 0.0)[0] == "REORDER"
    assert decisions.action_for_grade_a(5, 10, 20, 0.05, 0.0)[0] == "HOLD"         # At s, but shortfall below threshold.
    assert decisions.action_for_grade_a(10, 10, 20, 0.11, 0.0)[0] == "REORDER"     # Boundary on s.
    assert decisions.action_for_grade_a(21, 10, 20, 0.3, 0.0)[0] == "REDUCE"
    assert decisions.action_for_grade_a(15, 10, 20, 0.3, 0.6)[0] == "REDUCE"
    assert decisions.action_for_grade_a(15, 10, 20, 0.3, 0.5)[0] == "HOLD"


def test_action_reason_wording_is_precise():
    for action in ("REORDER", "REDUCE", "HOLD", "MONITOR", "NO_ACTION_EVIDENCE"):
        assert not checks.FORBIDDEN_TEXT.search(decisions._reason(action))
    assert "not an obsolescence determination" in decisions._reason("MONITOR")
    assert decisions.ACTION_LABEL["HOLD"] == "Maintain"


def test_tradeoff_keeps_availability_and_inventory_apart():
    assert kpis.tradeoff(-1, 1) == "less_unmet_more_inventory"
    assert kpis.tradeoff(1, -1) == "more_unmet_less_inventory"
    assert kpis.tradeoff(0, 0) == "no_change"


# Scenario grammar and contract.
def test_scenario_identifier_grammar():
    assert cfg.scenario_id("A", "ED", "R0") == "SC-A-ED-R0-BO-K0"
    assert cfg.scenario_id("B", "OR", "X2", "BO", "K20") == "SC-B-OR-X2-BO-K20"


def test_held_out_window_lengths():
    assert cfg.TEST_START_DAY == 335 and cfg.TEST_DAYS == 183 and cfg.TRAIN_MONTHS == 11


def test_every_v01_column_survives_in_v02():
    for name, columns in contract.V01_REQUIRED.items():
        names = [c[0] for c in contract.SCHEMAS[name]["columns"]]
        assert set(columns) <= set(names), name


def test_samples_match_the_contract_and_are_labelled(tmp_path):
    assert samples.main([str(tmp_path)]) == 0
    manifest = json.loads((tmp_path / "eng_run_manifest.json").read_text())
    assert "SAMPLE" in manifest["data_label"]
    for path in tmp_path.glob("*.csv"):
        frame = pd.read_csv(path, dtype={"material_no": str})
        assert contract.validate_frame(path.name, frame) == [], path.name
        assert (frame.output_class == "sample").all() if "output_class" in frame else True
        assert frame.material_no.str.startswith("SAMPLE-").all() if "material_no" in frame else True
        assert (frame.run_id == "RUN-SAMPLE").all()
    results = pd.read_csv(tmp_path / "eng_scenario_result.csv")
    assert (results.result_type == "sample").all()


def _sample(name):
    return samples.build()[name].copy()


def test_contract_rejects_a_missing_column():
    frame = _sample("eng_material_tier.csv").drop(columns="tier")
    assert any("missing columns" in e for e in contract.validate_frame("eng_material_tier.csv", frame))


def test_contract_rejects_an_unknown_column():
    frame = _sample("eng_material_tier.csv").assign(extra=1)
    assert any("unknown columns" in e for e in contract.validate_frame("eng_material_tier.csv", frame))


def test_contract_rejects_a_bad_enum_a_null_a_repeat_and_a_bad_probability():
    frame = _sample("eng_recommendation.csv")
    frame.loc[0, "recommended_action"] = "BUY"
    assert any("outside the enum" in e for e in contract.validate_frame("eng_recommendation.csv", frame))
    frame = _sample("eng_material_tier.csv")
    frame.loc[0, "run_id"] = None
    assert any("nulls" in e for e in contract.validate_frame("eng_material_tier.csv", frame))
    frame = _sample("eng_material_tier.csv")
    frame.loc[1, "material_no"] = frame.loc[0, "material_no"]
    assert any("primary key" in e for e in contract.validate_frame("eng_material_tier.csv", frame))
    frame = _sample("eng_scenario_result.csv")
    frame.loc[0, "sim_fill_rate_quantity"] = 1.5
    assert any("outside 0 to 1" in e for e in contract.validate_frame("eng_scenario_result.csv", frame))


def test_contract_document_is_generated_and_current():
    path = PROJECT_ROOT / "docs/handover/ENGINE_OUTPUT_CONTRACT.md"
    assert path.read_text(encoding="utf-8") == contract.render_markdown()


# Money and wording boundaries.
@pytest.mark.parametrize("name", ["estimated_savings", "cost_total", "unit_price", "po_item_amount", "actual_stockout", "optimal_s", "best_policy", "value_idr"])
def test_money_and_claim_columns_are_caught(name):
    assert checks.FORBIDDEN_COLUMN.search(name)


@pytest.mark.parametrize("text", ["This is the optimal level", "avoids an actual stockout", "Savings of 10", "dead stock"])
def test_forbidden_text_is_caught(text):
    assert checks.FORBIDDEN_TEXT.search(text)


def test_contract_has_no_money_column_outside_currency_label():
    for name, spec in contract.SCHEMAS.items():
        if name == "eng_validation_results.csv":  # Its "actual" column holds a check result, not a business value.
            continue
        for column in spec["columns"]:
            assert not checks.FORBIDDEN_COLUMN.search(column[0]), (name, column[0])


def test_kpi_financial_rows_are_blocked_with_no_value():
    empty = pd.DataFrame(columns=["run_set", "config_id", "demand_scenario", "pr_view", "policy", "result_type", "any_shortfall", "sim_fill_rate_quantity", "unit", "expected_unmet_qty", "mean_on_hand", "sim_ending_on_hand", "days_above_recorded_max", "orders_placed", "sim_order_quantity_total", "shortfall_probability"])
    comparison = pd.DataFrame(columns=["comparison_type", "config_id", "demand_scenario", "pr_view", "policy_a", "tradeoff", "group", "delta_mean_on_hand"])
    supply = pd.DataFrame(columns=["pr_view", "promised_interval_days_iqr", "requested_vs_promised_gap_days_median"])
    rec = pd.DataFrame({"material_no": ["1"], "consensus_action": ["HOLD"], "consensus_status": ["all_scenarios_agree"]})
    tier = pd.DataFrame({"forecast_eligibility": ["abstain"], "demand_class": ["D0"]})
    flags = pd.DataFrame({k: [False] for k in ["flag_slow_moving_by_recorded_issues", "flag_non_moving_by_recorded_issues", "flag_potentially_obsolete_candidate", "flag_stock_above_recorded_max", "flag_stock_at_or_below_recorded_min"]})
    out = kpis.build_kpis(empty, comparison, rec, tier, supply, flags, {}, "RUN")
    money = out[out.dimension == "financial_impact"]
    assert len(money) == 4 and (money.status == "NOT_COMPUTED").all() and money.value.isna().all()


def test_results_report_is_generated_and_current():
    if not (cfg.ENGINE_DIR / "eng_run_manifest.json").exists():
        pytest.skip("Engine output not generated")
    from src.simulation import report
    assert report.DOC.read_text(encoding="utf-8") == report.build()
