"""L1. Sample files in the contract format, so the application can integrate without real output. python -m src.simulation.samples

Material numbers and every value are invented. Each row has output_class = sample. Nothing here is a result, and none of it derives from the competition data.
"""
import json
import sys
from pathlib import Path

import pandas as pd

from src.simulation import contract
from src.simulation import settings as cfg

RUN_ID = "RUN-SAMPLE"
MATERIALS = [("SAMPLE-0001", "T3", "A", "D3"), ("SAMPLE-0002", "T3", "A", "D4"), ("SAMPLE-0003", "T3", "A", "D3"), ("SAMPLE-0004", "T3", "B", "D2"), ("SAMPLE-0005", "T3", "B", "D1"), ("SAMPLE-0006", "T2", None, "D3"), ("SAMPLE-0007", "T2", None, "D1"), ("SAMPLE-0008", "T1", None, "D0"), ("SAMPLE-0009", "T1", None, "D0"), ("SAMPLE-0010", "T2", None, "D2")]
SAMPLE_NOTE = "ILLUSTRATIVE SAMPLE. Invented values. Not a result."


def _fill(name: str, base: dict, i: int) -> dict:
    """Complete a row from the schema. Explicit values in base win."""
    row = {}
    for column in contract.SCHEMAS[name]["columns"]:
        key, kind, _, nullable = column[:4]
        if key in base:
            row[key] = base[key]
        elif key == "run_id":
            row[key] = RUN_ID
        elif key == "output_class":
            row[key] = "sample"
        elif kind == "enum":
            row[key] = None if nullable else column[5][i % len(column[5])]
        elif nullable:
            row[key] = None
        elif kind == "bool":
            row[key] = i % 2 == 0
        elif kind == "int":
            row[key] = i + 1
        elif kind == "float":
            row[key] = round(1.5 * (i + 1), 3)
        elif kind == "prob":
            row[key] = round(0.1 * (i % 10), 3)
        else:
            row[key] = f"sample_{key}"
    return row


def build() -> dict:
    files = {}
    tier, fc, res, par, cap, rec, flags, facts, sup = [], [], [], [], [], [], [], [], []
    for i, (m, t, grade, cls) in enumerate(MATERIALS):
        active = {"D0": 0, "D1": 2, "D2": 4, "D3": 9, "D4": 15}[cls]
        abstain = {"D0": "no_recorded_consumption_in_window", "D1": "fewer_than_3_active_months_no_forecast", "D2": "fewer_than_6_active_months_rate_range_only"}.get(cls)
        conf = {"D0": "Abstain"}.get(cls, "Medium" if grade == "A" and i == 0 else "Low")
        elig = "forecast_range" if active >= 6 else "rate_range_only" if active >= 3 else "abstain"
        tier.append(_fill("eng_material_tier.csv", {"material_no": m, "unit": "EA", "mrp_type": "Stock Item", "active_months": active, "n_issue_lines__scenario_a": active * 3, "n_issue_lines__scenario_b": active * 2, "tier": t, "adi": round(17 / active, 3) if active else None, "demand_class__scenario_a": cls, "demand_class__scenario_b": cls, "demand_class": cls, "forecast_eligibility": elig, "policy_grade": grade, "evidence_subtier": f"{t}_grade_{grade}" if grade else f"{t}__no_lead_proxy", "flag_class_differs_by_scenario": False, "flag_outlier_review": i == 1, "flag_scenario_divergent": i == 2, "confidence": conf, "abstain_reason": abstain}, i))
        for d in ("A", "B"):
            eligible = active >= 6
            fc.append(_fill("eng_forecast.csv", {"material_no": m, "demand_scenario": d, "pr_view": "ALL", "scenario_id": f"SC-{d}-NA-NA-NA-K0", "horizon_basis": "next_month_rate", "forecast_period": "2026-10", "unit": "EA", "demand_class": cls, "active_months": active, "n_issue_lines": active * 3, "evidence_class": "sample", "forecast_eligible": eligible, "forecast_quantity": round(4.2 + i, 3) if eligible else None, "forecast_method": "croston_sba" if eligible else ("observed_active_month_range" if cls == "D2" else "abstain"), "rate_low": 1.0 if active >= 3 else None, "rate_high": 9.0 if active >= 3 else None, "uncertainty_kind": "observed_month_percentiles_p05_p95" if eligible else None, "confidence": conf, "abstain_reason": abstain}, i))
            if eligible:
                fc.append(_fill("eng_forecast.csv", {"material_no": m, "demand_scenario": d, "pr_view": "ED", "scenario_id": f"SC-{d}-ED-NA-NA-K0", "horizon_basis": "lead_time_demand", "forecast_period": "lead_window_after_2026-09", "horizon_days": 42, "unit": "EA", "demand_class": cls, "active_months": active, "n_issue_lines": active * 3, "evidence_class": "sample", "forecast_eligible": True, "forecast_quantity": 12.5, "forecast_method": "block_bootstrap_lead_time_demand", "lead_time_demand_low": 2.0, "lead_time_demand_mid": 11.0, "lead_time_demand_high": 30.0, "uncertainty_kind": "spread_under_resampling_p05_p95", "confidence": conf, "lead_mode": "median_promised_interval", "quantile_method_status": "not_accepted_failed_preregistered_pinball_rule"}, i))
        if t == "T3":
            for d in ("A", "B"):
                for v in ("OR", "ED"):
                    r0 = {"material_no": m, "scenario_id": cfg.scenario_id(d, v, "R0"), "demand_scenario": d, "pr_view": v, "policy": "R0", "unmet_rule": "BO", "config_id": "K0", "run_set": "R0", "result_type": "sample", "unit": "EA", "parameter_source": "recorded_min_max_unverified", "s_used": 5, "S_used": 12, "lead_days_used": "42", "initial_inventory_used": 8, "total_issues": 30.0, "any_shortfall": i % 2 == 0, "expected_unmet_qty": 4.0 + i, "days_at_or_below_zero": 10.0, "mean_on_hand": 6.5, "p95_on_hand": 12.0, "units_above_recorded_max": 0.0, "days_above_recorded_max": 0.0, "orders_placed": 3.0, "sim_fill_rate_quantity": 0.87, "policy_grade": grade, "data_label": "sample"}
                    res.append(_fill("eng_scenario_result.csv", r0, i))
                    if grade == "A":
                        for code, level in cfg.SERVICE_LEVELS.items():
                            s = 7 + int(level * 10) - 9
                            res.append(_fill("eng_scenario_result.csv", {**r0, "scenario_id": cfg.scenario_id(d, v, code, "BO", "K20"), "policy": code, "config_id": "K20", "run_set": "MC-D", "service_level": level, "parameter_source": "full_window_same_history", "s_used": s, "S_used": s + 8, "Q_used": 8, "shortfall_probability": round(0.3 - (level - 0.9), 3), "any_shortfall": None, "n_replications": 1000, "seed": cfg.MASTER_SEED, "sim_fill_rate_quantity": round(level - 0.02, 3), "fill_rate_p05": 0.7, "fill_rate_p95": 1.0}, i))
                            par.append(_fill("eng_proposed_parameters.csv", {"material_no": m, "scenario_id": cfg.scenario_id(d, v, code), "demand_scenario": d, "pr_view": v, "policy": code, "service_level": level, "proposed_s": s, "proposed_S": s + 8, "proposed_Q": 8, "safety_stock": 2.5, "flag_safety_stock_floored": False, "proposed_S_capped_at_recorded_max": 12, "lead_time_demand_mean": 5.5, "lead_time_demand_quantile": float(s), "lead_mode": "median_promised_interval", "lead_days_median": 42, "n_draws": 5000, "recorded_min": 5, "recorded_max": 12, "recorded_stock_undated": 8, "unit": "EA", "parameter_status": "candidate_for_review"}, i))
                        res.append(_fill("eng_scenario_result.csv", {**r0, "scenario_id": cfg.scenario_id(d, v, "R1", "BO", "K20"), "policy": "R1", "config_id": "K20", "run_set": "MC-D", "shortfall_probability": 0.42, "any_shortfall": None, "n_replications": 1000, "seed": cfg.MASTER_SEED}, i))
                        action = ["REORDER", "HOLD", "REDUCE"][i % 3]
                        rec.append(_fill("eng_recommendation.csv", {"material_no": m, "scenario_id": cfg.scenario_id(d, v, "X2", "BO", "K20"), "demand_scenario": d, "pr_view": v, "service_level_reference": 0.95, "recommended_action": action, "action_label": {"REORDER": "Reorder", "HOLD": "Maintain", "REDUCE": "Reduce"}[action], "action_at_90": action, "action_at_98": action, "risk_level": ["High", "Low", "Medium"][i % 3], "evidence_class": "sample", "confidence": conf, "reason_codes": "sample_reason", "reason": SAMPLE_NOTE, "trigger_condition": "sample trigger: recorded stock 8 <= proposed s 9", "supporting_metrics": json.dumps({"recorded_stock_undated": 8, "proposed_s": 9}), "proposed_s": 9, "proposed_S": 17, "proposed_Q": 8, "safety_stock": 2.5, "recorded_min": 5, "recorded_max": 12, "recorded_stock_undated": 8, "unit": "EA", "limitations": "stock_undated;sample", "requires_review": True, "method_class": "deterministic_rule_on_simulation", "consensus_status": "all_scenarios_agree", "consensus_action": action}, i))
                        cap.append(_fill("eng_capability_output.csv", {"material_no": m, "capability": "reorder", "scenario_id": cfg.scenario_id(d, v, "X2", "BO", "K20"), "flag": action, "value_num": 9, "value_kind": "proposed_s", "unit": "EA", "confidence": conf, "requires_review": True, "reason_codes": "sample_reason", "method_class": "deterministic_rule_on_simulation", "recommended_action": action}, i))
                        cap.append(_fill("eng_capability_output.csv", {"material_no": m, "capability": "stockout_risk", "scenario_id": cfg.scenario_id(d, v, "R1", "BO", "K20"), "flag": "Medium", "value_num": 0.42, "value_kind": "shortfall_probability_simulated", "unit": "probability", "confidence": conf, "requires_review": True, "reason_codes": "sample_reason", "method_class": "simulation"}, i))
        if grade != "A":
            action = "MONITOR" if cls != "D0" or i % 2 == 0 else "NO_ACTION_EVIDENCE"
            rec.append(_fill("eng_recommendation.csv", {"material_no": m, "scenario_id": "SC-ALL-NA-NA-NA-K0", "demand_scenario": "ALL", "pr_view": "ALL", "recommended_action": action, "action_label": "Monitor" if action == "MONITOR" else "No action: insufficient evidence", "risk_level": "Not assessed", "evidence_class": "sample", "confidence": conf, "reason_codes": "sample_reason", "reason": SAMPLE_NOTE, "trigger_condition": "sample trigger", "supporting_metrics": "{}", "recorded_min": 0, "recorded_max": 0, "recorded_stock_undated": 3, "unit": "EA", "limitations": "stock_undated;sample", "requires_review": action == "MONITOR", "method_class": "deterministic_rule", "consensus_status": "all_scenarios_agree", "consensus_action": action}, i))
            cap.append(_fill("eng_capability_output.csv", {"material_no": m, "capability": "reorder", "scenario_id": "SC-ALL-NA-NA-NA-K0", "flag": action, "value_kind": None, "unit": "EA", "confidence": conf, "requires_review": action == "MONITOR", "reason_codes": "sample_reason", "method_class": "deterministic_rule", "recommended_action": action}, i))
        cap.append(_fill("eng_capability_output.csv", {"material_no": m, "capability": "slow_moving", "scenario_id": "SC-ALL-NA-NA-NA-K0", "flag": "non_moving_by_recorded_issues" if cls == "D0" else "not_flagged", "unit": "days", "confidence": conf, "requires_review": cls == "D0", "reason_codes": "sample_reason", "method_class": "deterministic_rule"}, i))
        cap.append(_fill("eng_capability_output.csv", {"material_no": m, "capability": "overstock_risk", "scenario_id": "SC-ALL-NA-NA-NA-K0", "flag": "Not assessed", "unit": "EA", "confidence": conf, "requires_review": False, "reason_codes": "sample_reason", "method_class": "deterministic_rule"}, i))
        flags.append(_fill("eng_health_flags.csv", {"material_no": m, "tier": t, "policy_grade": grade, "demand_class": cls, "unit": "EA", "active_months": active, "recorded_stock_undated": 3.0 + i, "recorded_min": 2, "recorded_max": 6, "flag_stock_held": True, "flag_stock_at_or_below_recorded_min": i == 0, "flag_stock_above_recorded_max": i == 3, "flag_stock_held_with_zero_max": False, "flag_slow_moving_by_recorded_issues": cls == "D1", "flag_non_moving_by_recorded_issues": cls == "D0", "flag_potentially_obsolete_candidate": i == 7, "flag_outlier_review": i == 1, "stockout_risk_level": "Medium" if grade == "A" else "Not assessed", "stockout_risk_basis": "sample", "overstock_risk_level": "Low" if grade == "A" else "Not assessed", "overstock_risk_basis": "sample", "wording_note": SAMPLE_NOTE}, i))
        facts.append(_fill("eng_explanation_facts.csv", {"material_no": m, "fact_id": f"{m}-1", "capability": "all", "fact_key": "demand_class", "value": cls, "scenario_id": "SC-ALL-NA-NA-NA-K0", "source_file": "eng_material_tier.csv", "source_column": "demand_class"}, i))
        if active:
            for v in ("OR", "ED"):
                sup.append(_fill("eng_supply_context.csv", {"material_no": m, "pr_view": v, "supplier_code": f"S{i:03d}", "supplier_name": "Sample Supplier", "currency": "IDR" if i != 2 else "USD", "unit": "EA", "n_lines": 8 + i, "n_purchase_orders": 6, "first_pr_date": "2025-06-01", "last_pr_date": "2026-08-01", "promised_interval_days_median": 42.0, "promised_interval_days_p25": 30.0, "promised_interval_days_p75": 60.0, "promised_interval_days_p90": 90.0, "promised_interval_days_iqr": 30.0, "n_lines_used_for_promised_interval": 8 + i, "requested_interval_days_median": 35.0, "requested_vs_promised_gap_days_median": 7.0, "n_lines_promised_after_data_cutoff": 0, "n_lines_promised_before_pr": 0, "supplier_share_of_lines": 1.0, "source_file": "sample", "label": "promised procurement interval, not transport or goods-receipt time"}, i))
    files["eng_material_tier.csv"] = pd.DataFrame(tier)
    files["eng_forecast.csv"] = pd.DataFrame(fc)
    files["eng_scenario_result.csv"] = pd.DataFrame(res)
    files["eng_proposed_parameters.csv"] = pd.DataFrame(par)
    files["eng_capability_output.csv"] = pd.DataFrame(cap)
    files["eng_recommendation.csv"] = pd.DataFrame(rec)
    files["eng_health_flags.csv"] = pd.DataFrame(flags)
    files["eng_explanation_facts.csv"] = pd.DataFrame(facts)
    files["eng_supply_context.csv"] = pd.DataFrame(sup)
    files["eng_kpi_summary.csv"] = pd.DataFrame([_fill("eng_kpi_summary.csv", {"kpi_id": "AV-1", "dimension": "availability", "kpi_name": "Materials with a simulated shortage (sample)", "formula": "count / materials", "numerator": 2, "denominator": 5, "value": 0.4, "unit": "share of materials", "population": "Sample 5", "population_n": 5, "scenario": cfg.scenario_id("A", "ED", "R0"), "source": "sample", "interpretation": SAMPLE_NOTE, "limitations": SAMPLE_NOTE, "status": "COMPUTED", "result_type": "sample"}, 0)])
    return files


def main(argv=None) -> int:
    out = Path(argv[0]) if argv else cfg.SAMPLES_DIR
    out.mkdir(parents=True, exist_ok=True)
    files = build()
    problems = {n: contract.validate_frame(n, f) for n, f in files.items()}
    problems = {n: e for n, e in problems.items() if e}
    if problems:
        print(json.dumps(problems, indent=1))
        return 1
    for name, frame in files.items():
        frame.to_csv(out / name, index=False, lineterminator="\n", encoding="utf-8")
    manifest = {"run_id": RUN_ID, "spec_version": cfg.CONTRACT_VERSION, "engine_version": "sample", "methodology_version": cfg.METHODOLOGY_VERSION, "data_label": "ILLUSTRATIVE SAMPLE. Invented values with invented material numbers. Not derived from the dataset. Not a result.", "config_id": "sample", "seed": None, "input_checksums": {}, "created_at": "sample", "execution_status": "sample", "files": {n: {"rows": len(f)} for n, f in files.items()}}
    (out / "eng_run_manifest.json").write_text(json.dumps(manifest, indent=1) + "\n", encoding="utf-8")
    print({n: len(f) for n, f in files.items()})
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
