"""Engine outputs on the real marts. Independent recalculation without project code, predictions, tendencies, failure detection, reproducibility."""
import csv
import gzip
import hashlib
import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).parents[1] / "unit"))
from independent_engine import run_daily, same_as_engine  # noqa: E402

from src.simulation import checks, contract, deterministic as det, stochastic  # noqa: E402
from src.simulation import run as engine_run  # noqa: E402
from src.simulation import settings as cfg  # noqa: E402
from src.simulation.engine import Policy, simulate  # noqa: E402
from src.simulation.inputs import load_inputs, material_lines  # noqa: E402

pytestmark = pytest.mark.data_contract
E = cfg.ENGINE_DIR
needs_output = pytest.mark.skipif(not (E / "eng_run_manifest.json").exists(), reason="Engine output not generated. Run python -m src.simulation.run")


def _csv(name, base=None):
    with open((base or cfg.PROCESSED_DIR) / name, newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


@pytest.fixture(scope="module")
def inputs():
    return load_inputs()


@pytest.fixture(scope="module")
def results():
    return pd.read_csv(E / "eng_scenario_result.csv", dtype={"material_no": str}, low_memory=False)


def test_engine_stays_in_its_package_and_the_pipeline_never_runs_it(real_build):
    """Carries forward what still applies from the design-stage boundary test: the data pipeline neither contains nor runs the engine, and emits no result files."""
    import re
    source = cfg.PROJECT_ROOT / "src"
    outside = [p for p in source.rglob("*engine*") if "__pycache__" not in p.parts and "simulation" not in p.parts]
    assert outside == []
    pattern = re.compile(r"src\.simulation(?!_)\b|from src import simulation\b")
    for path in source.rglob("*.py"):
        if "simulation" in path.relative_to(source).parts:
            continue
        assert not pattern.search(path.read_text(encoding="utf-8")), path
    names = [p.name for folder in (real_build["paths"].processed, real_build["paths"].tables, real_build["paths"].exceptions) for p in folder.iterdir()]
    assert not [n for n in names if "sim_result" in n or "simulation_result" in n or "stockout" in n or n.startswith("eng_")]


def test_all_r0_equals_independent_implementation(inputs):
    """Design 12.1. Every material, both scenarios, both views, both shortage modes."""
    runs = 0
    for material, row in inputs.t3.iterrows():
        for demand in cfg.DEMAND_SCENARIOS:
            lines = material_lines(inputs, demand, material)
            for view in cfg.PR_VIEWS.values():
                lead = det.lead_days(row[f"lead_median__{view}"])
                s, S = int(row.min_parameter_unverified), max(int(row.max_parameter_unverified), int(row.min_parameter_unverified) + 1)
                a = simulate(lines, row.assumed_initial_inventory, Policy(s, S=S), lead, recorded_max=row.max_parameter_unverified)
                b = run_daily(lines, row.assumed_initial_inventory, s, S, None, lead, 518, False, row.max_parameter_unverified)
                assert same_as_engine(a, b) == [], (material, demand, view)
                runs += 1
    assert runs == 2660


@needs_output
def test_class_counts_recalculated_without_project_code():
    """Standard library only, from the mart, compared with the engine file."""
    months = {r["material_no"]: int(r["months_with_issue"]) for r in _csv("mart_material_demand_summary__scenario_a.csv")}
    assert len(months) == 1930
    assert sum(1 <= m <= 2 for m in months.values()) == 1475
    assert sum(3 <= m <= 5 for m in months.values()) == 159
    assert sum(m >= 6 for m in months.values()) == 296
    population = _csv("simulation_population.csv")
    t3 = {r["material_no"] for r in population if r["population_status"] == "in_population"}
    assert len(t3) == 665
    both = {m for m, n in months.items() if n >= 6 and m in t3}
    assert len(both) == 228 and len(t3 - both) == 437
    stored = {r["material_no"]: r for r in _csv("eng_material_tier.csv", E)}
    assert len(stored) == 7481
    for material, row in stored.items():
        count = months.get(material, 0)
        assert int(row["active_months"]) == count
        expected = "D0" if count == 0 else "D1" if count <= 2 else "D2" if count <= 5 else None
        if expected:
            assert row["demand_class"] == expected
        else:
            assert row["demand_class"] in ("D3", "D4")
    assert {m for m, r in stored.items() if r["policy_grade"] == "A"} == both


@needs_output
def test_class_split_recalculated_without_project_code():
    """D3 and D4 from monthly quantities with the statistics module."""
    months = defaultdict(list)
    for r in _csv("mart_material_demand_month__scenario_a.csv"):
        if float(r["qty_issued"]) > 0:
            months[r["material_no"]].append(float(r["qty_issued"]))
    smooth = {m for m, q in months.items() if len(q) >= 6 and 17 / len(q) < 1.32 and (statistics.stdev(q) / statistics.mean(q)) ** 2 < 0.49}
    stored = {r["material_no"] for r in _csv("eng_material_tier.csv", E) if r["demand_class__scenario_a"] == "D4"}
    assert smooth == stored and len(stored) == 27


@needs_output
def test_replay_recalculated_without_project_code_on_a_real_material(results, inputs):
    """A plain day loop over the source file, for ten materials with orders and shortages. No project function is called."""
    population = {r["material_no"]: r for r in _csv("simulation_population.csv")}
    movement = defaultdict(list)
    for r in _csv("movement_copy_classification.csv"):
        if r["in_scenario_a"] == "True":
            movement[r["material_no"]].append((r["posting_date"][:10], int(r["source_row"]), float(r["quantity"])))
    chosen = results[(results.scenario_id == "SC-A-ED-R0-BO-K0") & (results.orders_placed > 0) & (results.any_shortfall == True)].head(10)  # noqa: E712
    assert len(chosen) == 10
    for row in chosen.itertuples():
        pop = population[row.material_no]
        low, high, stock = float(pop["min_parameter_unverified"]), float(pop["max_parameter_unverified"]), float(pop["assumed_initial_inventory"])
        lead = max(1, int(np.ceil(float(pop["lead_proxy_median_days__exact_distinct_rows"]))))
        start = pd.Timestamp("2025-05-01")
        issues = defaultdict(float)
        for date, _, qty in movement[row.material_no]:
            issues[(pd.Timestamp(date) - start).days] += qty
        on_hand, back, pipeline, total_h, orders, unmet = stock, 0.0, defaultdict(float), 0.0, 0, 0.0
        if on_hand <= low:
            pipeline[lead] += max(high, low + 1) - on_hand
            orders += 1
        for day in range(518):
            on_hand += pipeline.pop(day, 0.0)
            pay = min(on_hand, back)
            on_hand, back = on_hand - pay, back - pay
            give = min(on_hand, issues[day])
            on_hand -= give
            unmet += issues[day] - give
            back += issues[day] - give
            position = on_hand + sum(pipeline.values()) - back
            if position <= low and issues[day] > 0:
                pipeline[day + lead] += max(high, low + 1) - position
                orders += 1
            total_h += on_hand
        assert row.orders_placed == orders, row.material_no
        assert row.expected_unmet_qty == pytest.approx(unmet), row.material_no
        assert row.mean_on_hand == pytest.approx(total_h / 518, abs=1e-5), row.material_no


@needs_output
def test_gate_and_every_check_passed():
    rows = _csv("eng_validation_results.csv", E)
    assert rows and all(r["status"] == "PASS" for r in rows)
    gate = [r for r in rows if r["stage"] == "deterministic_gate"]
    assert len(gate) == 12


@needs_output
def test_scenarios_are_separate_and_never_blended(results):
    assert set(results.demand_scenario) == {"A", "B"} and set(results.pr_view) == {"OR", "ED"}
    assert not any("blend" in c or "combined" in c for c in results.columns)
    a = results[results.scenario_id == "SC-A-ED-R0-BO-K0"].set_index("material_no")
    b = results[results.scenario_id == "SC-B-ED-R0-BO-K0"].set_index("material_no").loc[a.index]
    assert (a.total_issues != b.total_issues).sum() == 229
    assert (a.total_issues >= b.total_issues).all()


@needs_output
def test_duplicate_sensitivity_view_changes_inputs_and_is_kept(results):
    original = results[results.scenario_id == "SC-A-OR-R0-BO-K0"].set_index("material_no")
    distinct = results[results.scenario_id == "SC-A-ED-R0-BO-K0"].set_index("material_no").loc[original.index]
    assert (original.lead_days_used != distinct.lead_days_used).sum() > 0


@needs_output
def test_design_tendencies_hold_on_most_materials():
    """Design 12.3. Tendencies, not laws. Exceptions are counted, not hidden."""
    with gzip.open(E / "audit/eng_sensitivity_result.csv.gz", "rt") as handle:
        s1 = pd.read_csv(handle, dtype={"material_no": str}, low_memory=False)
    s1 = s1[(s1.demand_scenario == "A") & (s1.pr_view == "ED") & (s1.unmet_rule == "BO")].set_index("material_no")
    base = pd.read_csv(E / "eng_scenario_result.csv", dtype={"material_no": str}, low_memory=False)
    base = base[base.scenario_id == "SC-A-ED-R0-BO-K0"].set_index("material_no")

    def share_not_worse(k, higher_is_better):
        part = s1[s1.config_id == k].sim_fill_rate_quantity.dropna()
        ref = base.sim_fill_rate_quantity.loc[part.index]
        return ((part >= ref - 1e-9) if higher_is_better else (part <= ref + 1e-9)).mean()

    assert share_not_worse("K2", True) >= 0.9       # More opening stock.
    assert share_not_worse("K1", False) >= 0.9      # Less opening stock.
    assert share_not_worse("K8", False) >= 0.9      # Longer interval.
    assert share_not_worse("K6", True) >= 0.9       # Shorter interval.
    assert share_not_worse("K11", False) >= 0.9     # More issues.
    assert share_not_worse("K10", True) >= 0.9      # Fewer issues.


@needs_output
def test_upper_bound_opening_stock_means_no_shortage():
    with gzip.open(E / "audit/eng_sensitivity_result.csv.gz", "rt") as handle:
        s1 = pd.read_csv(handle, dtype={"material_no": str}, low_memory=False)
    assert s1[s1.config_id == "K5"].any_shortfall.sum() == 0


def test_stochastic_is_reproducible_and_common_across_scenarios(inputs):
    material = next(m for m in inputs.grade_a if inputs.t3.loc[m, "scenarios_identical_by_construction"])
    a, b = stochastic.run_material(material, 50, inputs), stochastic.run_material(material, 50, inputs)
    assert a == b
    frame = pd.DataFrame(a)
    left = frame[(frame.demand_scenario == "A") & (frame.run_set == "MC-D")].set_index(["pr_view", "policy"]).shortfall_probability
    right = frame[(frame.demand_scenario == "B") & (frame.run_set == "MC-D")].set_index(["pr_view", "policy"]).shortfall_probability
    assert (left == right.loc[left.index]).all()


def test_evidence_gate_blocks_thin_materials(inputs):
    thin = inputs.t3.index[(inputs.t3.active_months < 6) & (inputs.t3.lead_observations_distinct < 10)][0]
    assert stochastic.run_material(thin, 10, inputs) == []


@needs_output
def test_no_sampled_input_for_materials_below_threshold(results, inputs):
    mc = results[results.result_type == "simulation"]
    lead = inputs.t3.index[inputs.t3.lead_observations_distinct >= 10]
    assert set(mc[mc.run_set == "MC-D"].material_no) == set(inputs.grade_a)
    assert set(mc[mc.run_set == "MC-L"].material_no) == set(lead)
    assert set(mc[mc.run_set == "MC-J"].material_no) == set(inputs.grade_a) & set(lead)


@needs_output
def test_held_out_parameters_use_training_months_only(results, inputs):
    """Change every test-month line and confirm the training estimate cannot move: recompute s from training lines alone and match the stored value."""
    from src.simulation import parameters as pm
    from src.simulation import resampling as rs
    held = results[(results.run_set == "HO") & (results.policy == "X2") & (results.scenario_id.str.startswith("SC-A-ED")) & (results.config_id == "K30")]
    table = inputs.procurement["exact_distinct_rows"]
    sources = rs.draw_month_sources(cfg.LTD_PATHS, cfg.TRAIN_MONTHS, cfg.TRAIN_MONTHS, rs.generator(rs.STREAM_ESTIMATE_BLOCKS, cfg.TRAIN_MONTHS))
    for row in held.head(25).itertuples():
        all_lines = material_lines(inputs, "A", row.material_no)
        train = [(d, q) for d, q in all_lines if d < cfg.TEST_START_DAY]
        obs_table = table[(table.material_no == row.material_no) & (table.pr_date < pd.Timestamp(cfg.TEST_START_DATE)) & (table.promised_interval_days >= 0)]
        obs = np.sort(obs_table.promised_interval_days.to_numpy(dtype=float))
        est = pm.estimate_ltd(train, obs, row.material_no, len(obs) >= 10, cfg.TRAIN_MONTHS, sources)
        assert int(np.ceil(est.quantiles["X2"])) == row.s_used
        assert all(d < cfg.TEST_START_DAY for d, _ in train)


@needs_output
def test_held_out_shares_opening_stock_and_lead_across_policies(results):
    held = results[(results.run_set == "HO")]
    grouped = held.groupby(["material_no", "demand_scenario", "pr_view", "config_id"])
    assert (grouped.initial_inventory_used.nunique() == 1).all()
    assert (grouped.lead_days_used.nunique() == 1).all()
    assert (grouped.total_issues.nunique() == 1).all()
    assert (grouped.size() == 6).all()


@needs_output
def test_policy_comparison_shares_demand_in_monte_carlo(results):
    mc = results[results.run_set == "MC-D"]
    assert (mc.groupby(["material_no", "demand_scenario", "pr_view"]).total_issues.nunique() == 1).all()
    assert (mc.groupby(["material_no", "demand_scenario", "pr_view"]).initial_inventory_used.nunique() == 1).all()


@needs_output
def test_forecast_abstention_and_no_forecast_for_unsupported():
    rows = _csv("eng_forecast.csv", E)
    monthly = [r for r in rows if r["horizon_basis"] == "next_month_rate"]
    assert len(monthly) == 2 * 7481
    for r in monthly:
        if r["demand_class"] in ("D0", "D1"):
            assert r["forecast_quantity"] == "" and r["rate_low"] == "" and r["abstain_reason"]
        if r["demand_class"] == "D2":
            assert r["forecast_quantity"] == "" and r["rate_low"] != "" and r["abstain_reason"]
        if r["demand_class"] in ("D3", "D4"):
            assert r["forecast_quantity"] != "" and r["forecast_eligible"] == "True"


@needs_output
def test_grade_b_receives_no_parameter_and_no_reorder():
    tier = {r["material_no"]: r for r in _csv("eng_material_tier.csv", E)}
    assert not [r for r in _csv("eng_proposed_parameters.csv", E) if tier[r["material_no"]]["policy_grade"] != "A"]
    for r in _csv("eng_recommendation.csv", E):
        if tier[r["material_no"]]["policy_grade"] != "A":
            assert r["recommended_action"] in ("MONITOR", "NO_ACTION_EVIDENCE") and r["proposed_s"] == ""


@needs_output
def test_no_issue_history_is_not_called_obsolete_and_low_use_is_not_excess():
    flags = _csv("eng_health_flags.csv", E)
    never = [r for r in flags if r["active_months"] == "0"]
    assert len(never) == 5551
    assert all(r["overstock_risk_level"] == "Not assessed" for r in never)
    assert sum(r["flag_potentially_obsolete_candidate"] == "True" for r in never) < sum(r["flag_non_moving_by_recorded_issues"] == "True" for r in never)
    assert all("not an obsolescence determination" in r["wording_note"].lower() for r in flags)
    assert not any("obsolete" in c and "candidate" not in c for c in flags[0])
    slow = [r for r in flags if r["flag_slow_moving_by_recorded_issues"] == "True"]
    assert all(r["overstock_risk_level"] == "Not assessed" or r["policy_grade"] == "A" for r in slow)


@needs_output
def test_supply_context_equals_the_mart_and_keeps_currencies_apart():
    supply = pd.read_csv(E / "eng_supply_context.csv", dtype={"material_no": str, "supplier_code": str})
    for view, code in (("exact_distinct_rows", "ED"), ("original_rows", "OR")):
        mart = pd.read_csv(cfg.PROCESSED_DIR / f"mart_supplier_material__{view}.csv", dtype={"material_no": str, "supplier_code": str}, keep_default_na=False, na_values=[""]).set_index("material_no")
        part = supply[supply.pr_view == code].set_index("material_no")
        assert len(part) == 1250
        for column in ("promised_interval_days_median", "promised_interval_days_p75", "promised_interval_days_p90", "n_lines", "requested_interval_days_median"):
            assert np.allclose(part[column].astype(float), mart.loc[part.index, column].astype(float), equal_nan=True), column
        assert (part.supplier_code == mart.loc[part.index, "supplier_code"]).all()
        assert (part.currency == mart.loc[part.index, "currency"]).all()
    assert set(supply.currency) == {"IDR", "JPY", "USD", "EUR", "SGD"}
    assert (supply.label.str.contains("not transport")).all()


@needs_output
def test_kpi_recalculates_from_results(results):
    kpi = pd.read_csv(E / "eng_kpi_summary.csv", low_memory=False)
    row = kpi[(kpi.kpi_id == "AV-1") & (kpi.run_set == "HO") & (kpi.scenario == "SC-A-ED-X2-BO-K30")].iloc[0]
    part = results[results.scenario_id == "SC-A-ED-X2-BO-K30"]
    assert row.numerator == (part.any_shortfall == True).sum() and row.denominator == len(part)  # noqa: E712
    assert row.value == pytest.approx(row.numerator / row.denominator, abs=1e-6)
    required = ["formula", "numerator", "denominator", "unit", "population", "scenario", "source", "interpretation", "limitations"]
    assert all(c in kpi.columns for c in required)
    assert not kpi.dimension.str.contains("composite").any()


@needs_output
def test_outputs_fail_when_damaged():
    """Damage real outputs and confirm the checks catch it."""
    inputs = load_inputs()
    tier = pd.read_csv(E / "eng_material_tier.csv", dtype={"material_no": str}, low_memory=False)
    files = {n: pd.read_csv(E / n, dtype={"material_no": str, "supplier_code": str}, low_memory=False) for n in contract.SCHEMAS if n != "eng_validation_results.csv"}
    clean = checks.output_checks(files, inputs, tier, cfg.MC_REPLICATIONS)
    assert all(r["status"] == "PASS" for r in clean)

    def failed(modified):
        rows = checks.output_checks({**files, **modified}, inputs, tier, cfg.MC_REPLICATIONS)
        return {r["check_id"] for r in rows if r["status"] != "PASS"}

    grade_b = tier[tier.policy_grade == "B"].material_no.iloc[0]
    rec = files["eng_recommendation.csv"].copy()
    rec.loc[rec.material_no == grade_b, "recommended_action"] = "REORDER"
    assert "grade_b_never_reorder_reduce_hold" in failed({"eng_recommendation.csv": rec})
    fc = files["eng_forecast.csv"].copy()
    idx = fc[(fc.horizon_basis == "next_month_rate") & (fc.demand_class == "D1")].index[0]
    fc.loc[idx, "forecast_quantity"] = 5.0
    assert "forecast_quantity_only_where_eligible" in failed({"eng_forecast.csv": fc})
    par = files["eng_proposed_parameters.csv"].copy()
    par.loc[0, "material_no"] = grade_b
    assert "no_parameter_for_grade_b" in failed({"eng_proposed_parameters.csv": par})
    res = files["eng_scenario_result.csv"].copy().assign(estimated_savings=1.0)
    assert "no_money_or_actual_column_eng_scenario_result.csv" in failed({"eng_scenario_result.csv": res})
    kpi = files["eng_kpi_summary.csv"].copy()
    kpi.loc[kpi.dimension == "financial_impact", "value"] = 123.0
    assert "financial_kpis_have_no_value" in failed({"eng_kpi_summary.csv": kpi})


@needs_output
def test_every_file_has_manifest_entry_with_hash_and_required_metadata():
    manifest = json.loads((E / "eng_run_manifest.json").read_text())
    for key in ("run_id", "created_at", "input_checksums", "methodology_version", "seed", "populations", "assumptions", "execution_status", "data_label", "spec_version"):
        assert manifest[key], key
    assert manifest["execution_status"] == "complete"
    for name, entry in manifest["files"].items():
        assert hashlib.sha256((E / name).read_bytes()).hexdigest() == entry["sha256"], name
        assert entry["execution_status"] == "generated"
    for name, value in manifest["input_checksums"].items():
        assert hashlib.sha256((cfg.PROCESSED_DIR / name).read_bytes()).hexdigest() == value, name


@pytest.mark.slow
@needs_output
def test_a_second_full_run_gives_identical_bytes(tmp_path):
    assert engine_run.main(["--out", str(tmp_path)]) == 0
    stored = json.loads((E / "eng_run_manifest.json").read_text())["files"]
    fresh = json.loads((tmp_path / "eng_run_manifest.json").read_text())["files"]
    assert {k: v["sha256"] for k, v in stored.items()} == {k: v["sha256"] for k, v in fresh.items()}
