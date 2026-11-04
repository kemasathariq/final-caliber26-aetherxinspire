"""Demand classification, D-06 delivered as eng_material_tier.csv. Rules: DEMAND_INTELLIGENCE_METHODOLOGY sections 1 and 4.

Classes are deterministic rules on recorded issues, which are not proven demand. D3 and D4 can differ between Scenarios A and
B because CV squared depends on the quantities. No scenario is a default, so `demand_class` takes the less smooth of the two
and both per-scenario classes stay in the file.
"""
import numpy as np
import pandas as pd

from src.simulation import settings as cfg


def pattern(adi: pd.Series, cv2: pd.Series) -> pd.Series:
    """Syntetos-Boylan labels on active months. Descriptive only."""
    out = pd.Series(pd.NA, index=adi.index, dtype="string")
    known = adi.notna() & cv2.notna()
    out[known & (adi < cfg.SMOOTH_ADI) & (cv2 < cfg.SMOOTH_CV2)] = "smooth"
    out[known & (adi < cfg.SMOOTH_ADI) & (cv2 >= cfg.SMOOTH_CV2)] = "erratic"
    out[known & (adi >= cfg.SMOOTH_ADI) & (cv2 < cfg.SMOOTH_CV2)] = "intermittent"
    out[known & (adi >= cfg.SMOOTH_ADI) & (cv2 >= cfg.SMOOTH_CV2)] = "lumpy"
    return out


def demand_class(active: pd.Series, pat: pd.Series) -> pd.Series:
    out = pd.Series("D0", index=active.index, dtype="string")
    out[(active >= 1) & (active <= 2)] = "D1"
    out[(active >= 3) & (active < cfg.MIN_ACTIVE_MONTHS)] = "D2"
    out[active >= cfg.MIN_ACTIVE_MONTHS] = "D3"
    out[(active >= cfg.MIN_ACTIVE_MONTHS) & (pat == "smooth")] = "D4"
    return out


def robust_outlier_materials(inputs) -> set:
    """Robust z above 3.5 within a material's own lines (A-10). Flags only; nothing is removed. Same result in A and B counted as union."""
    flagged = set()
    for (_demand, material), rows in inputs.lines.items():
        if len(rows) < cfg.ROBUST_Z_MIN_LINES:
            continue
        q = np.array([r[1] for r in rows], dtype=float)
        med = np.median(q)
        mad = np.median(np.abs(q - med))
        if mad > 0 and (0.6745 * np.abs(q - med) / mad).max() > cfg.ROBUST_Z:
            flagged.add(material)
    return flagged


def build_material_tier(inputs) -> pd.DataFrame:
    inv, pop = inputs.inventory, inputs.population
    frame = pd.DataFrame(index=inv.index)
    active = inv.months_with_issue.fillna(0).astype(int)
    frame["unit"] = inv.unit
    frame["mrp_type"] = inv.mrp_type
    frame["active_months"] = active
    frame["n_issue_lines__scenario_a"] = inv.n_issue_lines__scenario_a.fillna(0).astype(int)
    frame["n_issue_lines__scenario_b"] = inv.n_issue_lines__scenario_b.fillna(0).astype(int)
    frame["tier"] = np.where(pop.loc[inv.index, "population_status"] == "in_population", "T3", np.where(active > 0, "T2", "T1"))
    frame["adi"] = (17 / active.where(active > 0)).round(6)
    for demand, name in cfg.DEMAND_SCENARIOS.items():
        s = inputs.summary[demand].reindex(inv.index)
        # Sample standard deviation, as in M3. A single active month has no spread, so CV squared stays blank.
        cv2 = ((s.std_active_month_qty / s.mean_active_month_qty) ** 2).round(6)
        frame[f"cv2__{name}"] = cv2
        pat = pattern(frame["adi"], cv2).where(active >= cfg.MIN_ACTIVE_MONTHS)
        frame[f"demand_pattern__{name}"] = pat
        frame[f"demand_class__{name}"] = demand_class(active, pat)
    both_smooth = (frame.demand_class__scenario_a == "D4") & (frame.demand_class__scenario_b == "D4")
    frame["demand_class"] = frame.demand_class__scenario_a.where(~frame.demand_class__scenario_a.isin(["D3", "D4"]), np.where(both_smooth, "D4", "D3"))
    frame["flag_class_differs_by_scenario"] = frame.demand_class__scenario_a != frame.demand_class__scenario_b

    lead_obs = pop.loc[inv.index, "lead_observations_distinct"]
    frame["lead_observations_distinct"] = lead_obs
    frame["forecast_eligibility"] = np.select([active >= cfg.MIN_ACTIVE_MONTHS, active >= 3], ["forecast_range", "rate_range_only"], "abstain")
    grade = pd.Series(pd.NA, index=inv.index, dtype="string")
    grade[frame.tier == "T3"] = "B"
    grade[(frame.tier == "T3") & (active >= cfg.MIN_ACTIVE_MONTHS)] = "A"
    frame["policy_grade"] = grade
    lead_part = np.select([lead_obs >= cfg.MIN_LEAD_OBSERVATIONS, lead_obs >= 3, lead_obs >= 1], ["lead_resampled", "lead_point_value", "lead_one_or_two_lines"], "no_lead_proxy")
    frame["evidence_subtier"] = np.where(frame.tier == "T3", "T3_grade_" + grade.fillna("").astype(str) + "__" + lead_part, frame.tier + "__" + lead_part)

    outliers = robust_outlier_materials(inputs)
    frame["flag_outlier_review"] = frame.index.isin(outliers) | (inv.n_lines_at_repeated_unit_maximum.fillna(0) > 0)
    frame["flag_scenario_divergent"] = inv.demand_materially_affected.fillna(False).astype(bool)

    medium = frame.demand_class.isin(["D3", "D4"]) & (lead_obs >= cfg.MIN_LEAD_OBSERVATIONS) & ~frame.flag_scenario_divergent & ~frame.flag_outlier_review
    frame["confidence"] = np.select([active == 0, medium], ["Abstain", "Medium"], "Low")
    frame["abstain_reason"] = pd.Series(np.select(
        [active == 0, active <= 2, active < cfg.MIN_ACTIVE_MONTHS],
        ["no_recorded_consumption_in_window", "fewer_than_3_active_months_no_forecast", "fewer_than_6_active_months_rate_range_only"], ""), index=inv.index).replace("", pd.NA)
    frame["output_class"] = "rule_derived"
    return frame.sort_index()
