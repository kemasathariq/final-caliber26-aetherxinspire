"""Execute the analytical engine and write contract files to data/processed/engine/. Read-only on raw data and marts.

    python -m src.simulation.run                 full run, 1,000 replications
    python -m src.simulation.run --reps 100      smaller Monte Carlo
    python -m src.simulation.run --out PATH      write elsewhere (tests use this)

Exit code 1 means the deterministic gate or an output check failed. The stochastic stage never starts if the gate fails.
"""
import argparse
import hashlib
import json
import platform
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from src.simulation import checks, classification, contract, decisions, deterministic as det, forecast, kpis, stochastic
from src.simulation import settings as cfg
from src.simulation.engine import LOST_SALES
from src.simulation.inputs import input_checksums, load_inputs, reconcile, sha256


def make_run_id(checksums: dict, reps: int) -> str:
    """Deterministic, so a repeat run on the same inputs gives byte-identical files."""
    text = json.dumps({"inputs": checksums, "engine": cfg.ENGINE_VERSION, "contract": cfg.CONTRACT_VERSION, "method": cfg.METHODOLOGY_VERSION, "seed": cfg.MASTER_SEED, "reps": reps}, sort_keys=True)
    return "RUN-" + hashlib.sha256(text.encode()).hexdigest()[:12]


def write(frame: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix == ".gz":
        frame.to_csv(path, index=False, lineterminator="\n", encoding="utf-8", compression={"method": "gzip", "mtime": 0})
    else:
        frame.to_csv(path, index=False, lineterminator="\n", encoding="utf-8")


def main(argv=None) -> int:
    args = argparse.ArgumentParser()
    args.add_argument("--reps", type=int, default=cfg.MC_REPLICATIONS)
    args.add_argument("--out", type=Path, default=cfg.ENGINE_DIR)
    args.add_argument("--workers", type=int, default=8)
    opts = args.parse_args(argv)
    out: Path = opts.out
    started = time.time()

    def log(message):
        print(f"[{time.time() - started:7.1f}s] {message}", flush=True)

    before = input_checksums()
    inputs = load_inputs()
    run_id = make_run_id(inputs.checksums, opts.reps)
    validation = [{"stage": "inputs", **row} for row in reconcile(inputs)]
    log(f"{run_id}: inputs loaded, {sum(r['status'] == 'PASS' for r in validation)} of {len(validation)} reconciliation checks pass")

    # L2. Deterministic baseline, then the gate.
    r0_rows, trace = det.run_recorded(inputs, "R0", keep_trace=True)
    r0 = pd.DataFrame(r0_rows)
    gate = [{"stage": "deterministic_gate", **row} for row in det.gate_checks(r0, inputs)]
    validation += gate
    failed = [g for g in validation if g["status"] != "PASS"]
    log(f"R0 replay: {len(r0)} runs. Gate: {len(gate) - sum(g['status'] != 'PASS' for g in gate)} of {len(gate)} pass")
    if failed:
        print(json.dumps(failed, indent=1))
        log("Deterministic gate failed. Stochastic stage not started.")
        return 1
    r2, trace_r2 = det.run_recorded(inputs, "R2", keep_trace=True)
    estimates = det.estimate_all_parameters(inputs)
    proposed = pd.DataFrame(det.proposed_parameter_rows(inputs, estimates, run_id))
    replay_x = det.run_policy_replay(inputs, estimates)
    s1_rows, _ = det.run_recorded(inputs, "R0", ksets=cfg.S1_KSETS)
    ls_rows, _ = det.run_recorded(inputs, "R0", shortage=LOST_SALES)
    held_out_rows, held_out_status = det.run_held_out(inputs)
    log(f"R2 {len(r2)}, proposed-policy replay {len(replay_x)}, S1 {len(s1_rows)}, lost sales {len(ls_rows)}, held-out {len(held_out_rows)} on {int(held_out_status.included_in_held_out.sum())} materials")

    # L3. Classes and forecasts.
    tier = classification.build_material_tier(inputs)
    fc, fc_validation, fc_choice = forecast.build_forecast(inputs, tier, run_id)
    log(f"Classes {tier.demand_class.value_counts().sort_index().to_dict()}. Forecast rows {len(fc)}. Choices {fc_choice.to_dict('records')}")
    quantile_accepted = bool(fc_choice.bootstrap_range_accepted.all())

    # L4. Stochastic, only reached if the gate passed.
    eligible = sorted(inputs.t3.index[(inputs.t3.active_months >= cfg.MIN_ACTIVE_MONTHS) | (inputs.t3.lead_observations_distinct >= cfg.MIN_LEAD_OBSERVATIONS)])
    mc_rows = stochastic.run_all(eligible, opts.reps, opts.workers)
    log(f"Monte Carlo: {len(mc_rows)} result rows, {len(eligible)} materials, {opts.reps} replications")

    results = pd.DataFrame(r0_rows + r2 + replay_x + held_out_rows + mc_rows)
    results.insert(0, "run_id", run_id)
    results["policy_grade"] = results.material_no.map(tier.policy_grade)
    results["data_label"] = "synthetic"
    results = results.sort_values(["run_set", "scenario_id", "material_no"], kind="stable").reset_index(drop=True)
    for column in ("any_shortfall", "converged_fill_rate"):
        results[column] = results[column].astype("boolean")

    # L5, L6.
    mc_d_r1 = results[(results.run_set == "MC-D") & (results.policy == "R1")]
    r0_frame = results[(results.run_set == "R0") & (results.policy == "R0")]
    plan_link = decisions.material_plan_link(decisions.plan_locations())
    flags = decisions.build_health_flags(inputs, tier, mc_d_r1, r0_frame, proposed, plan_link, run_id)
    held_out = results[results.run_set == "HO"]
    recommendations = decisions.build_recommendations(inputs, tier, flags, mc_d_r1, proposed, quantile_accepted, held_out, run_id)
    capability = decisions.build_capability_output(tier, flags, recommendations, proposed, mc_d_r1, r0_frame, run_id)
    facts = decisions.build_explanation_facts(tier, flags, recommendations, proposed, run_id)
    supply = decisions.build_supply_context(inputs, run_id)
    log(f"Recommendations {len(recommendations)} rows; flags {len(flags)}; supply context {len(supply)}")

    # Comparisons and KPIs.
    comparisons = pd.concat([
        kpis.compare_demand_scenarios(r0_frame, inputs),
        kpis.compare_policies(held_out, "R0", "held_out_vs_recorded"),
        kpis.compare_policies(results[results.run_set == "MC-D"], "R1", "mc_d_vs_recorded"),
        kpis.compare_policies(results[results.run_set == "MC-J"], "R1", "mc_j_vs_recorded"),
    ], ignore_index=True)
    comparisons.insert(0, "run_id", run_id)
    comparisons["output_class"] = comparisons.comparison_type.map({"demand_a_vs_b": "deterministic_simulation", "held_out_vs_recorded": "deterministic_simulation", "mc_d_vs_recorded": "stochastic_simulation", "mc_j_vs_recorded": "stochastic_simulation"})
    s1 = pd.DataFrame(s1_rows + ls_rows)
    sensitivity = kpis.sensitivity_summary(s1, r0_frame)
    r2_sens = kpis.sensitivity_summary(results[(results.run_set == "R0") & (results.policy == "R2")], r0_frame)
    sensitivity = pd.concat([sensitivity, r2_sens], ignore_index=True)
    ab = r0_frame.pivot_table(index=["material_no", "pr_view"], columns="demand_scenario", values="sim_fill_rate_quantity").dropna()
    ab_rows = []
    for view, part in ab.groupby(level="pr_view"):
        diff = (part["A"] - part["B"]).abs()
        ab_rows.append({"config_id": "A_vs_B", "unmet_rule": "BO", "policy": "R0", "demand_scenario": "A|B", "pr_view": view, "n_materials": len(part), "shortage_status_changes": int(comparisons[(comparisons.comparison_type == "demand_a_vs_b") & (comparisons.pr_view == view)].stockout_status_differs.sum()), "order_count_changes": int(comparisons[(comparisons.comparison_type == "demand_a_vs_b") & (comparisons.pr_view == view)].orders_differ.sum()), "median_abs_fill_rate_change": round(float(diff.median()), 6), "mean_abs_fill_rate_change": round(float(diff.mean()), 6), "p90_abs_fill_rate_change": round(float(diff.quantile(0.9)), 6)})
    sensitivity = pd.concat([sensitivity, pd.DataFrame(ab_rows)], ignore_index=True)
    sensitivity.insert(0, "run_id", run_id)
    sensitivity["output_class"] = "deterministic_simulation"
    sensitivity["description"] = sensitivity.config_id.map({k[0]: k[3] for k in cfg.CONFIG_REGISTRY}).fillna("")
    sensitivity.loc[sensitivity.config_id == "A_vs_B", "description"] = "Demand Scenario A against B, paired"
    sensitivity.loc[sensitivity.unmet_rule == "LS", "description"] = "Unmet quantity lost, not backordered"
    sensitivity.loc[sensitivity.policy == "R2", "description"] = "Policy R2: Min as reorder level, repeated median PR quantity"
    kpi = kpis.build_kpis(results[results.policy_grade.notna()], comparisons, recommendations, tier, supply, flags, {}, run_id)
    log(f"Comparisons {len(comparisons)}; KPI rows {len(kpi)}; sensitivity rows {len(sensitivity)}")

    registry = pd.DataFrame(cfg.CONFIG_REGISTRY, columns=["config_id", "run_set", "output_kind", "description"])
    registry.insert(0, "run_id", run_id)

    tier_out = tier.reset_index()
    tier_out.insert(0, "run_id", run_id)
    fc_validation.insert(0, "run_id", run_id)
    fc_choice.insert(0, "run_id", run_id)
    fc_validation = fc_validation.merge(fc_choice, on=["run_id", "demand_scenario", "demand_class"])
    fc_validation["output_class"] = "statistical_forecast"
    held_out_status.insert(0, "run_id", run_id)
    held_out_status["output_class"] = "rule_derived"
    audit_s1 = s1[["material_no", "scenario_id", "demand_scenario", "pr_view", "policy", "unmet_rule", "config_id", "any_shortfall", "expected_unmet_qty", "mean_on_hand", "orders_placed", "sim_fill_rate_quantity", "sim_stockout_days", "unit"]].copy()
    audit_s1.insert(0, "run_id", run_id)
    trace_frame = pd.DataFrame(trace + trace_r2)
    trace_frame.insert(0, "run_id", run_id)
    trace_frame["output_class"] = "deterministic_simulation"

    files = {
        "eng_material_tier.csv": tier_out, "eng_forecast.csv": fc, "eng_forecast_validation.csv": fc_validation, "eng_scenario_result.csv": results, "eng_proposed_parameters.csv": proposed,
        "eng_capability_output.csv": capability, "eng_recommendation.csv": recommendations, "eng_health_flags.csv": flags, "eng_explanation_facts.csv": facts, "eng_supply_context.csv": supply,
        "eng_kpi_summary.csv": kpi, "eng_scenario_comparison.csv": comparisons, "eng_sensitivity_summary.csv": sensitivity, "eng_config_registry.csv": registry, "eng_held_out_population.csv": held_out_status,
    }
    audit_files = {"audit/eng_sensitivity_result.csv.gz": audit_s1, "audit/eng_replay_event_trace.csv.gz": trace_frame}

    validation += [{"stage": "outputs", **row} for row in checks.output_checks(files, inputs, tier, opts.reps)]
    validation += [{"stage": "contract", **row} for row in contract.validate_all(files)]
    after = input_checksums()
    validation.append({"stage": "protection", "check_id": "source_marts_unchanged", "expected": "0", "actual": str(sum(before[k] != after[k] for k in before)), "status": "PASS" if before == after else "FAIL"})
    validation_frame = pd.DataFrame(validation)
    validation_frame.insert(0, "run_id", run_id)
    files["eng_validation_results.csv"] = validation_frame

    out.mkdir(parents=True, exist_ok=True)
    entries = {}
    for name, frame in {**files, **audit_files}.items():
        write(frame, out / name)
        meta = contract.FILE_META.get(name, {})
        entries[name] = {"rows": len(frame), "sha256": sha256(out / name), "grain": meta.get("grain"), "output_classes": sorted(frame.output_class.dropna().unique().tolist()) if "output_class" in frame else [], "execution_status": "generated", "seed": cfg.MASTER_SEED if name in contract.SEEDED_FILES else None, "population": meta.get("population"), "scenario": meta.get("scenario"), "methodology_version": cfg.METHODOLOGY_VERSION, "assumptions": cfg.ASSUMPTIONS if name in contract.SIMULATED_FILES else None}
    manifest = {
        "run_id": run_id, "spec_version": cfg.CONTRACT_VERSION, "engine_version": cfg.ENGINE_VERSION, "methodology_version": cfg.METHODOLOGY_VERSION, "data_label": cfg.DATA_LABEL_TEXT, "simulated_label": cfg.SIMULATED_LABEL, "config_id": "K0 plus registry", "seed": cfg.MASTER_SEED, "replications": opts.reps,
        "block_months": cfg.BLOCK_MONTHS, "input_checksums": inputs.checksums, "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "execution_status": "complete" if (validation_frame.status == "PASS").all() else "complete_with_failed_checks", "assumptions": cfg.ASSUMPTIONS,
        "decisions_applied_as_defaults": {"D-02": "R1 reading with R2 alternative", "D-03": "6 active months, 10 lead observations", "D-05": "90, 95, 98 percent as scenario levels", "D-24": "parameters for 228 Grade A only", "D-25": f"reorder threshold {cfg.REORDER_SHORTFALL_THRESHOLD}, reduce threshold {cfg.REDUCE_DAYS_ABOVE_MAX_SHARE}, analyst-selected"},
        "populations": {"all_materials": len(tier), "t3": int((tier.tier == "T3").sum()), "grade_a": len(inputs.grade_a), "held_out": int(held_out_status.included_in_held_out.sum())}, "files": entries, "environment": {"python": platform.python_version(), "numpy": np.__version__, "pandas": pd.__version__},
        "validation": {"checks": len(validation_frame), "passed": int((validation_frame.status == "PASS").sum())},
    }
    (out / "eng_run_manifest.json").write_text(json.dumps(manifest, indent=1, default=str) + "\n", encoding="utf-8")
    bad = validation_frame[validation_frame.status != "PASS"]
    log(f"Validation: {manifest['validation']['passed']} of {manifest['validation']['checks']} pass. Files in {out}")
    if len(bad):
        print(bad.to_string())
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
