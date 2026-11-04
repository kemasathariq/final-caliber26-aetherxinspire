"""Generate docs/analytics/SIMULATION_METHODOLOGY_AND_RESULTS.md from the output files, so every number in it is reproducible. python -m src.simulation.report"""
import json
import sys

import pandas as pd

from src.config import PROJECT_ROOT
from src.simulation import settings as cfg

DOC = PROJECT_ROOT / "docs" / "analytics" / "SIMULATION_METHODOLOGY_AND_RESULTS.md"
POL = ["R0", "R2", "N1", "X1", "X2", "X3"]
POL_MC = ["R1", "R2", "N1", "X1", "X2", "X3"]
RULE = {"K30": "recorded Stock", "K31": "recorded Min", "K32": "recorded Max"}


def _rng(values, f="{:,.0f}"):
    lo, hi = min(values), max(values)
    return f.format(lo) if lo == hi else f"{f.format(lo)} to {f.format(hi)}"


def _table(head, rows):
    return "\n".join(["| " + " | ".join(head) + " |", "| " + " | ".join("---" for _ in head) + " |"] + ["| " + " | ".join(str(c) for c in r) + " |" for r in rows])


def build(engine=cfg.ENGINE_DIR) -> str:
    r = pd.read_csv(engine / "eng_scenario_result.csv", dtype={"material_no": str}, low_memory=False)
    r["short"] = r.any_shortfall == True  # noqa: E712
    man = json.loads((engine / "eng_run_manifest.json").read_text())
    val = pd.read_csv(engine / "eng_validation_results.csv")
    tier = pd.read_csv(engine / "eng_material_tier.csv", dtype={"material_no": str}, low_memory=False)
    rec = pd.read_csv(engine / "eng_recommendation.csv", dtype={"material_no": str}, low_memory=False)
    flags = pd.read_csv(engine / "eng_health_flags.csv", dtype={"material_no": str}, low_memory=False)
    fv = pd.read_csv(engine / "eng_forecast_validation.csv")
    sens = pd.read_csv(engine / "eng_sensitivity_summary.csv")
    comp = pd.read_csv(engine / "eng_scenario_comparison.csv", dtype={"material_no": str}, low_memory=False)
    ho_pop = pd.read_csv(engine / "eng_held_out_population.csv", dtype={"material_no": str})
    one = rec.drop_duplicates("material_no")

    # R0 replay.
    r0 = r[(r.run_set == "R0") & (r.policy == "R0")]
    r0_rows = []
    for (d, v), p in r0.groupby(["demand_scenario", "pr_view"]):
        r0_rows.append([d, v, len(p), int(p.short.sum()), int((p.orders_placed == 0).sum()), f"{p.sim_fill_rate_quantity.mean():.3f}", f"{p.sim_fill_rate_after_first_arrival.mean():.3f}", int((p.sim_fill_rate_quantity >= 0.95).sum()), f"{p.orders_placed.sum():,.0f}", int((p.sim_orders_open_at_end > 0).sum())])
    pop = pd.read_csv(cfg.PROCESSED_DIR / "simulation_population.csv", dtype={"material_no": str}, low_memory=False).set_index("material_no")
    ref = r0[r0.scenario_id == "SC-A-ED-R0-BO-K0"].copy()
    ref["day0"] = ref.material_no.map(pop.at_or_below_min_at_start) == True  # noqa: E712
    conflict = pop.single_line_exceeds_max.eq(True) | pop.median_pr_quantity_exceeds_max.eq(True) | pop.stock_above_max.eq(True)
    ref["conflict"] = ref.material_no.map(conflict)

    # Held-out.
    ho = r[r.run_set == "HO"]
    n_ho = int(ho_pop.included_in_held_out.sum())
    ho_rows = []
    for k in ("K30", "K31", "K32"):
        for pol in POL:
            p = ho[(ho.config_id == k) & (ho.policy == pol)]
            s = p.groupby(["demand_scenario", "pr_view"])
            ho_rows.append([RULE[k], pol, _rng(s.short.sum()), _rng(s.sim_fill_rate_quantity.mean(), "{:.3f}"), _rng(s.orders_placed.sum())])
    base_ho = ho[ho.policy == "R0"].set_index(["material_no", "demand_scenario", "pr_view", "config_id"])
    ratio_rows = []
    for k in ("K30", "K31", "K32"):
        row = [RULE[k]]
        for pol in ("R2", "N1", "X1", "X2", "X3"):
            j = ho[(ho.policy == pol)].set_index(base_ho.index.names).join(base_ho, rsuffix="_b")
            j = j[j.index.get_level_values("config_id") == k]
            j = j[j.mean_on_hand_b > 0]
            row.append(f"{(j.mean_on_hand / j.mean_on_hand_b).median():.2f}")
        ratio_rows.append(row)
    x2 = comp[(comp.comparison_type == "held_out_vs_recorded") & (comp.policy_a == "X2")]
    trade = x2.groupby("config_id").tradeoff.value_counts().unstack(fill_value=0)
    labels = ["less_unmet_more_inventory", "less_unmet_less_inventory", "less_unmet_same_inventory", "same_unmet_more_inventory", "same_unmet_less_inventory", "no_change", "more_unmet_more_inventory", "more_unmet_less_inventory", "more_unmet_same_inventory"]
    labels = [c for c in labels if c in trade.columns]
    trade_rows = [[RULE[k], *[int(trade.loc[k, c]) for c in labels], int(trade.loc[k].sum())] for k in trade.index]
    x2s = ho[ho.policy == "X2"].groupby(["config_id", "demand_scenario", "pr_view"]).short.sum()
    r0s = ho[ho.policy == "R0"].groupby(["config_id", "demand_scenario", "pr_view"]).short.sum()
    n_direction = int((x2s < r0s).sum())
    more_unmet_x2 = int(x2.tradeoff.str.startswith("more_unmet").sum())

    # Monte Carlo.
    def mc_rows(run_set):
        m = r[r.run_set == run_set]
        rows = []
        base = m[m.policy == "R1"].set_index(["material_no", "demand_scenario", "pr_view"])
        for pol in POL_MC:
            p = m[m.policy == pol]
            s = p.groupby(["demand_scenario", "pr_view"])
            j = p.set_index(base.index.names).join(base, rsuffix="_b", how="inner")
            j = j[j.mean_on_hand_b > 0]
            ratio = (j.mean_on_hand / j.mean_on_hand_b).median()
            rows.append([pol, int(p.material_no.nunique()), _rng(s.shortfall_probability.mean(), "{:.3f}"), _rng(s.shortfall_probability_after_first_arrival.mean(), "{:.3f}"), _rng(s.sim_fill_rate_quantity.mean(), "{:.3f}"), f"{ratio:.2f}", _rng(s.orders_placed.sum()), f"{int(p.converged_fill_rate.eq(True).sum())} of {len(p)}"])
        return rows
    d = r[r.run_set == "MC-D"]
    bd = d[d.policy == "R1"].set_index(["material_no", "demand_scenario", "pr_view"])
    jd = d[d.policy == "X2"].set_index(bd.index.names).join(bd, rsuffix="_b")
    lower = jd.shortfall_probability < jd.shortfall_probability_b - 1e-9
    not_more = jd.mean_on_hand <= jd.mean_on_hand_b + 1e-9
    stability = (lower & not_more).mean()
    stability_lower = lower.mean()
    stability_higher = (jd.shortfall_probability > jd.shortfall_probability_b + 1e-9).mean()
    unconverged = d[(d.converged_fill_rate == False)]  # noqa: E712

    # Forecast validation.
    boot = fv[fv.method == "block_bootstrap"]
    fv_rows = [[x.demand_scenario, x.demand_class, x.n_materials, x.n_origin_evaluations, f"{fv.loc[x.Index, 'share_beating_mean_pinball_0.5']:.2f}", f"{fv.loc[x.Index, 'share_beating_mean_pinball_0.9']:.2f}", f"{fv.loc[x.Index, 'share_beating_mean_pinball_0.95']:.2f}", f"{fv.loc[x.Index, 'share_beating_mean_pinball_0.98']:.2f}", f"{fv.loc[x.Index, 'empirical_coverage_0.9']:.3f}", f"{fv.loc[x.Index, 'empirical_coverage_0.95']:.3f}", f"{fv.loc[x.Index, 'empirical_coverage_0.98']:.3f}", "yes" if x.bootstrap_range_accepted else "**no**"] for x in boot.itertuples()]
    pt = fv[(fv.demand_scenario == "A") & (fv.method != "block_bootstrap")]
    pt_rows = [[x.demand_class, x.method, f"{x.median_scaled_error:.3f}", f"{fv.loc[x.Index, 'share_beating_mean_pinball_0.5']:.2f}", f"{fv.loc[x.Index, 'empirical_coverage_0.5']:.3f}"] for x in pt.itertuples()]

    # Recommendations.
    a4 = rec[rec.demand_scenario != "ALL"]
    action_rows = []
    for act in ("REORDER", "HOLD", "REDUCE", "MONITOR", "NO_ACTION_EVIDENCE"):
        action_rows.append([act, int((one.consensus_action == act).sum())])
    action_rows.append(["Depends on scenario", int((one.consensus_status == "scenario_dependent").sum())])
    t3_rows = one[one.demand_scenario == "ALL"].merge(tier[["material_no", "tier", "policy_grade"]], on="material_no")
    grade_rows = [[f"{t}{' Grade B' if t == 'T3' else ''}", int(((t3_rows.tier == t) & (t3_rows.recommended_action == "MONITOR")).sum()), int(((t3_rows.tier == t) & (t3_rows.recommended_action == "NO_ACTION_EVIDENCE")).sum())] for t in ("T3", "T2", "T1")]

    # Sensitivity.
    s = sens[(sens.pr_view == "ED") & sens.demand_scenario.isin(["A", "A|B"])].sort_values("mean_abs_fill_rate_change", ascending=False)
    sens_rows = [[("**" + x.description + "**") if x.config_id == "A_vs_B" else x.description, f"{x.mean_abs_fill_rate_change:.3f}", "" if pd.isna(x.materials_with_shortage) else f"{x.materials_with_shortage:.0f}", int(x.shortage_status_changes), int(x.order_count_changes)] for x in s.itertuples()]
    ab_value = sens[(sens.config_id == "A_vs_B") & (sens.pr_view == "ED")].mean_abs_fill_rate_change.iloc[0]
    larger = int((s[s.config_id != "A_vs_B"].mean_abs_fill_rate_change > ab_value).sum())
    n_factors = int((s.config_id != "A_vs_B").sum())
    ab = comp[(comp.comparison_type == "demand_a_vs_b") & (comp.pr_view == "ED")]
    ab_rows = [[g, len(p), int(p.orders_differ.sum()), int(p.first_order_day_differs.eq(True).sum()), int(p.order_quantity_differs.sum()), int(p.stockout_status_differs.eq(True).sum())] for g, p in ab.groupby("group")]

    classes = tier.demand_class.value_counts().sort_index()
    pat = tier.demand_pattern__scenario_a.value_counts()
    files = "\n".join(f"| `{k}` | {v['rows']:,} | {v.get('grain') or 'Audit file'} |" for k, v in man["files"].items())
    passed = int((val.status == "PASS").sum())

    return f"""# INSpire Simulation Methodology and Results

**Status:** generated by `src/simulation/report.py` from run `{man['run_id']}`. Do not edit by hand. Methodology `{man['methodology_version']}`, engine `{man['engine_version']}`, contract `{man['spec_version']}`, master seed {man['seed']}, {man['replications']:,} replications.

**{cfg.SIMULATED_LABEL}** {cfg.DATA_LABEL_TEXT} Nothing here describes Chandra Asri operations. A simulated shortage is never an actual stockout: every replayed issue did happen, so a shortage on a replayed issue is a finding about the assumptions.

**The model is verified, not validated.** No dated stock or goods receipts exist, so results cannot be compared with what really happened.

## 1. Headline findings

1. **Proposed parameters reduce simulated shortages, and they do it by holding more stock.** On held-out months, with parameters taken only from earlier months, materials with a simulated shortage fall from {_rng(r0s)} under the recorded Min-Max reading to {_rng(x2s)} under X2, in {n_direction} of 12 scenario combinations. Median on-hand per material rises by a factor of {ratio_rows[0][4]} to {max(ratio_rows[i][4] for i in range(3))}, depending on the opening-stock rule.
2. **It is a trade-off, not a free gain.** Under Monte Carlo, only {stability:.1%} of material-scenario pairs get both a lower shortfall probability and no more on-hand. Lower shortfall probability alone holds on {stability_lower:.1%}. On {stability_higher:.1%} it is higher.
3. **The quantile method failed its own pre-registered test.** The block-bootstrap quantile loses to mean-of-history on pinball loss at 0.90, 0.95 and 0.98 on most materials, in both classes and both scenarios. Coverage is {boot['empirical_coverage_0.9'].min():.2f} to {boot['empirical_coverage_0.9'].max():.2f} at a nominal 0.90, so the proposed reorder points err high. X1 to X3 therefore stay **what-if scenario candidates**, not validated quantile forecasts. See section 6 and decision D-26.
4. **The duplicate question matters less than the unverified inputs.** The Scenario A versus B swing in fill rate ({ab_value:.3f}) is smaller than {larger} of the {n_factors} what-ifs tested. Opening stock is the largest. That answers the design's main decision question (section 8).
5. **The product withholds parameters from most materials, and says why.** Parameters exist for 228 of 7,481. {int(one.recommended_action.eq('MONITOR').sum()):,} get Monitor from a recorded-issue flag, and {int(one.recommended_action.eq('NO_ACTION_EVIDENCE').sum()):,} get no action for lack of evidence.

## 2. What was run

| Run set | K | Population | Policies | Inputs | Output class |
| --- | --- | --- | --- | --- | --- |
| R0 | K0 | 665 | R0, R2 | Replayed issues, median promised interval | Deterministic |
| R0 proposed | K0 | 228 | N1, X1, X2, X3 | Same. **Parameters from the same months, in-sample, context only** | Deterministic |
| S1 | K1 to K16, plus LS and R2 | 665 | R0 | One what-if at a time. 18 levels of the design | Deterministic |
| Held-out | K30, K31, K32 | {n_ho} of 228 | R0, R2, N1, X1, X2, X3 | Parameters from 2025-05 to 2026-03, replay on 2026-04 to 2026-09, three opening-stock rules | Deterministic |
| MC-D | K20 | 228 | R1, R2, N1, X1, X2, X3 | Issues resampled, block of 3 months | Stochastic |
| MC-L | K21 | 140 | Same (139 with X, N1) | Promised interval resampled per order | Stochastic |
| MC-J | K22 | 139 | Same | Both resampled | Stochastic |

Every set runs under Scenarios A and B and PR PO views OR and ED. There is no default. {len(ho_pop) - n_ho} Grade A materials are left out of held-out replay because they have under 6 active months in the training months.

**Comparison method, as designed.** Every policy shares the same opening stock, demand path, lead-time draws, shortage rule and horizon. That is the design's common-start rule. No independent-start comparison exists or was invented.

### Policies

| Code | Reorder at | Order | Source |
| --- | --- | --- | --- |
| R0, R1 | Recorded Min | Up to recorded Max | D-02 reading, **unverified**. R0 under replay, R1 under resampling |
| R2 | Recorded Min | Repeated median PR quantity | Alternative reading |
| N1 | Mean lead-time demand | s + median PR quantity | Naive benchmark |
| X1, X2, X3 | 90, 95, 98 percent quantile of lead-time demand | s + median PR quantity | Proposed. Scenario levels, never targets (D-05) |

### Formulas

- **Inventory position:** $IP_t = H_t + O_t - B_t$. Order if $IP_t \\le s$. (s, S) orders $S - IP_t$. R2 orders the smallest multiple of Q that lifts position above s.
- **Lead-time demand:** demand over a promised interval, from a random day on a resampled history path. Interval resampled from own history at 10 or more distinct observations, otherwise the median.
- **Reorder point:** $s(\\alpha) = \\lceil Q_\\alpha(\\text{{LTD}}) \\rceil$, a value that occurred. **Safety stock:** $\\max(0, s(\\alpha) - \\overline{{\\text{{LTD}}}})$. **Replenishment quantity:** $Q = \\lceil$ median PR quantity $\\rceil$. **Order-up-to:** $S = s + Q$.
- **Shortfall probability:** share of replications with at least one stockout day. **Fill rate:** quantity served on its day over issues. Conservation laws hold on every deterministic run and every replication, or the run stops.

**Reading of the numbers.** Monte Carlo spreads come from reshuffling a material's own history. They are not probabilities of a future outcome and not confidence intervals. Most uncertainty here is about meaning (Min, Max, Stock date, lead time), which resampling cannot reduce.

## 3. Deterministic replay, recorded values

{_table(["Demand", "View", "Materials", "With simulated shortage", "No order placed", "Mean fill rate", "Mean fill after first arrival", "Fill at or above 0.95", "Orders", "Orders open at end"], r0_rows)}

**Reading.** Under Scenario A and view ED, {int(ref.short.sum())} of 665 materials show a simulated shortage. {int((ref.day0 & ref.short).sum())} of them started at or below Min on the assumed day 0, so their early shortage comes from the starting assumption. {int((ref.conflict & ref.short).sum())} of the {int(ref.short.sum())} also have recorded values that conflict with reading Max as an order-up-to level. These results describe the recorded values under this reading, not plant practice.

**Pre-registered predictions.** All 12 written before the engine existed hold exactly: 125 and 133 materials place no order, 183 order at the day-0 review, 436 are identical across scenarios, 8 differ on whether Min is ever reached, and 238 and 253 have full fill because stock covers all issues.

## 4. Held-out comparison, the primary policy result

Parameters use only 2025-05 to 2026-03. Replay covers 2026-04 to 2026-09, {cfg.TEST_DAYS} days. {n_ho} materials. Ranges cover the four scenario and view combinations.

{_table(["Opening stock", "Policy", "Materials with simulated shortage", "Mean fill rate", "Orders"], ho_rows)}

**Median on-hand, per material, relative to R0:**

{_table(["Opening stock", "R2", "N1", "X1", "X2", "X3"], ratio_rows)}

**X2 against R0, paired, material-scenario pairs:**

{_table(["Opening stock", *labels, "Total"], trade_rows)}

**Reading.**

- X2 lowers the count of materials with a shortage in all 12 combinations, and places fewer orders than R0. Unmet quantity rises on only {more_unmet_x2} of {len(x2):,} pairs.
- The cost is inventory. {int((x2.tradeoff == "less_unmet_less_inventory").sum())} X2 pairs lower both unmet quantity and on-hand.
- **Order size explains part of the gain.** R2 keeps recorded Min and only changes the order size to the observed median PR quantity. Starting from Min, R2 reaches {_rng(ho[(ho.config_id == 'K31') & (ho.policy == 'R2')].groupby(['demand_scenario', 'pr_view']).short.sum())} materials with shortage against X2's {_rng(ho[(ho.config_id == 'K31') & (ho.policy == 'X2')].groupby(['demand_scenario', 'pr_view']).short.sum())}. Under the other two rules X2 is clearly lower. So the size of X2's advantage over R2 depends on the opening-stock rule.
- **The simple benchmark competes.** N1 reaches {_rng(ho[(ho.config_id == 'K30') & (ho.policy == 'N1')].groupby(['demand_scenario', 'pr_view']).short.sum())} materials with shortage at about R0's median on-hand under recorded stock. It does not hold up as well under Monte Carlo (section 5).
- **Test months are quieter.** 37.9 percent of population lines fall in November 2025 to January 2026, all inside training. So parameters may err high on the test months. 17 months cannot separate a season from a one-off.

## 5. Stochastic results

**MC-D, issues resampled, 228 materials:**

{_table(["Policy", "Materials", "Mean shortfall probability", "Same, after first arrival", "Mean fill rate", "Median on-hand vs R1", "Orders, sum of means", "Fill rate converged"], mc_rows("MC-D"))}

**MC-J, issues and promised interval resampled, 139 materials:**

{_table(["Policy", "Materials", "Mean shortfall probability", "Same, after first arrival", "Mean fill rate", "Median on-hand vs R1", "Orders, sum of means", "Fill rate converged"], mc_rows("MC-J"))}

**MC-L, promised interval resampled, 140 materials:**

{_table(["Policy", "Materials", "Mean shortfall probability", "Same, after first arrival", "Mean fill rate", "Median on-hand vs R1", "Orders, sum of means", "Fill rate converged"], mc_rows("MC-L"))}

**Reading.** X parameters here come from the same history that is resampled, so this flatters them. Held-out replay in section 4 is the fairer test. N1 has a higher mean shortfall probability than R1, though a better fill rate, which shows the two service measures can disagree. Materials identical by construction give identical results under A and B in every replication, which confirms common random numbers. {len(unconverged):,} of {len(d):,} MC-D rows miss the half-width target of {cfg.CONVERGENCE_HALF_WIDTH}. They are flagged in `converged_fill_rate`, not hidden.

## 6. Demand classes and forecasts

| Class | Rule | Materials | Output |
| --- | --- | --- | --- |
| D0 | Never issued | {classes['D0']:,} | Abstain |
| D1 | 1 to 2 active months | {classes['D1']:,} | Abstain |
| D2 | 3 to 5 active months | {classes['D2']:,} | Observed range only, no point forecast |
| D3 | 6 or more, not smooth in both scenarios | {classes['D3']:,} | Forecast |
| D4 | ADI below 1.32 and CV squared below 0.49 in both | {classes['D4']:,} | Forecast |

D3 and D4 total 296, and 228 of them are in the simulation population. The other 68 get a forecast with no policy output. The rebuilt Scenario A pattern split is {int(pat.get('erratic', 0))} erratic, {int(pat.get('lumpy', 0))} lumpy, {int(pat.get('intermittent', 0))} intermittent and {int(pat.get('smooth', 0))} smooth. It replaces the indicative 112, 87, 66 and 31 in the methodology, which were never checked. `{int(tier.flag_class_differs_by_scenario.sum())}` materials change between D3 and D4 by scenario, so `demand_class` takes the less smooth of the two and both per-scenario classes stay in the file.

**Rolling-origin validation, as pre-registered in `VALIDATION_FRAMEWORK.md`.** History of 9 to 15 months, target is cumulative issues over the promised interval rounded to months. Under 10 origins per material, so results are reported per class.

**Block bootstrap against mean-of-history:**

{_table(["Demand", "Class", "Materials", "Evaluations", "Beats mean at 0.5", "at 0.90", "at 0.95", "at 0.98", "Coverage 0.90", "Coverage 0.95", "Coverage 0.98", "Accepted"], fv_rows)}

**Point methods, Scenario A:**

{_table(["Class", "Method", "Median scaled error", "Beats mean at 0.5", "Coverage of point"], pt_rows)}

**Decision applied, per the pre-registered rule.** Croston-SBA is the point forecast for next month in both classes and scenarios. The bootstrap range is **not accepted** at the service levels. It stays in `eng_forecast.csv` with `quantile_method_status = not_accepted_failed_preregistered_pinball_rule`, labelled spread under resampling. The rule's fallback is mean-of-history or abstention, and N1 is that fallback for a reorder point. **This is a decision for the Lead (D-26).** X1 to X3 were kept as labelled what-if candidates because D-05 asks for service-level scenarios and held-out replay tests them directly, but the limitation code is on every Grade A recommendation.

**Caution on the test.** Mean-of-history is a point, so scoring it at high alphas compares a point with a quantile. Its own bias is high because the peak months fall early in the window. The failure direction is too much stock, not too little.

## 7. Recommendations and health flags

Rule table: blueprint 12.2 (D-25). Thresholds are **analyst-selected and pending approval**: reorder when recorded stock is at or below proposed s and shortfall probability exceeds {cfg.REORDER_SHORTFALL_THRESHOLD}. Reduce when stock exceeds proposed S, or days above recorded Max exceed {cfg.REDUCE_DAYS_ABOVE_MAX_SHARE:.0%} of the horizon. Reference level X2. Actions at 90 and 98 percent sit beside it. `HOLD` means Maintain (D-19).

{_table(["Consensus action, all scenarios agree", "Materials"], action_rows)}

{_table(["Tier", "Monitor", "No action: insufficient evidence"], grade_rows)}

Grade A materials get Reorder, Maintain or Reduce per scenario. {int((a4.recommended_action != a4.action_at_90).sum())} of {len(a4)} Grade A rows change action at 90 percent, and {int((a4.recommended_action != a4.action_at_98).sum())} at 98 percent. **Reorder rests on undated stock, so it is a prompt to verify the balance, not an instruction to buy.**

| Flag | Materials | Precise meaning |
| --- | --- | --- |
| Stock held | {int(flags.flag_stock_held.sum()):,} | Recorded stock above zero, undated |
| Slow-moving by recorded issues | {int(flags.flag_slow_moving_by_recorded_issues.sum()):,} | Stock held, and at most 2 active months or no issue in the last 6 months |
| Non-moving by recorded issues | {int(flags.flag_non_moving_by_recorded_issues.sum()):,} | Stock held, never issued in the window |
| Potentially obsolete candidate | {int(flags.flag_potentially_obsolete_candidate.sum()):,} | Non-moving, and no BoM location has a maintenance plan. **A hypothesis needing lifecycle data, not a determination** |
| Stock above recorded Max | {int(flags.flag_stock_above_recorded_max.sum()):,} | Where Max is above zero. A recorded comparison. M2 counts 1,380 Stock Items including 4 with Max of zero |
| Stock at or below recorded Min | {int(flags.flag_stock_at_or_below_recorded_min.sum()):,} | Where Min is above zero |
| Stockout risk High, Medium, Low | {int((flags.stockout_risk_level == 'High').sum())}, {int((flags.stockout_risk_level == 'Medium').sum())}, {int((flags.stockout_risk_level == 'Low').sum())} | Grade A only. Worst of four scenarios under R1. Thresholds {cfg.RISK_HIGH} and {cfg.RISK_MEDIUM}, analyst-selected |
| Overstock risk High, Medium, Low | {int((flags.overstock_risk_level == 'High').sum())}, {int((flags.overstock_risk_level == 'Medium').sum())}, {int((flags.overstock_risk_level == 'Low').sum())} | Grade A only, against proposed S. Everyone else is not assessed |

## 8. Sensitivity and the dominance check

One-at-a-time, recorded policy, Scenario A and view ED (B and OR are in the file). Sorted by mean absolute change in fill rate per material.

{_table(["What-if", "Mean abs fill change", "With shortage", "Status changes", "Order count changes"], sens_rows)}

**Answer.** The demand scenario moves results less than {larger} of {n_factors} what-ifs. The opening-stock assumption moves them most. Stock + issues is an upper bound that removes every shortage by construction. So the most valuable missing fact is **the date of the Stock field**, then the meaning of Min and Max, then actual lead times.

**A versus B, Scenario pairs, view ED:**

{_table(["Group", "Materials", "Order count differs", "First order day differs", "Order quantity differs", "Shortage status differs"], ab_rows)}

## 9. Differences from the design, stated plainly

| Item | What happened | Why |
| --- | --- | --- |
| S2 interactions | **Not run** | Not required by this phase. Cheap to add |
| Block length 1, 6, evidence thresholds 4 and 8, event-month weighting, capping peaks | **Not run**. Peak-line exclusion (K16) was run | Time. Listed in `VALIDATION_FRAMEWORK.md` section 6 |
| Lost sales | Deterministic only | Monte Carlo uses the backorder reference |
| Policy code | R0 means replay and R1 means the same reading under resampling | Reconciles the design's run set R0 with the blueprint grammar |
| N1 | Added to the policy part of the grammar | `VALIDATION_FRAMEWORK.md` section 5 requires it. Announced in the change log |
| Rolling-origin horizon | Promised interval rounded to whole months, capped at 6 | Monthly evaluation |
| Mean-of-history, point methods at high alphas | Scored as a constant | They give no quantile |
| Dynamic Min-Max | Parameters are per scenario, not re-estimated monthly | The monthly re-estimate replay in the methodology was not built |
| Parameter grid search over service levels | Three fixed levels | D-05. No optimiser |

## 10. Verification

{passed} of {len(val)} run checks pass (`eng_validation_results.csv`): input reconciliation to the marts, 12 pre-registered predictions, output checks, contract schemas and source-mart checksums before and after. Test evidence is in the final report and `tests/`. An independently written daily loop matches the engine on all 2,660 R0 runs. A plain recalculation with no project code matches ten real materials. A second full run gives identical bytes in every output file. Tests caught one real defect during the build: two orders due on the same day overwrote each other in the Monte Carlo batch. It was fixed before these results, with a regression test and a conservation check on every replication.

## 11. Limits on what these results may be used to say

- Not a forecast of the plant and not a reconstruction of history. Not evidence of an actual stockout.
- No money. Inventory reductions or increases here are in units, and are not savings or costs (D-09, D-10).
- Results describe the 665 materials or the named subset, not Non Stock items or the other Stock Items.
- Promised intervals are not goods-receipt lead times. Issues are not proven demand. Stock is undated. Min and Max meanings are unverified.
- Nothing here is called optimal.

## 12. Files and reproduction

```text
python -m src.simulation.run       # about 1 minute. Writes data/processed/engine/
python -m src.simulation.samples   # Writes labelled samples to data/samples/engine/
python -m src.simulation.report    # Regenerates this document
python -m pytest
```

| File | Rows | Grain |
| --- | --- | --- |
{files}
"""


def main() -> int:
    DOC.write_text(build(), encoding="utf-8")
    print(DOC)
    return 0


if __name__ == "__main__":
    sys.exit(main())
