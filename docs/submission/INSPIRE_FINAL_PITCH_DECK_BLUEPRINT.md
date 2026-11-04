# INSpire Final Pitch Deck Blueprint

Run `RUN-277fc4b966e6`. Footer on every slide: "Synthetic hackathon data. Simulated under stated assumptions. Not Chandra Asri performance. No financial benefit computed."

**Format conflict:** brief p9 also mandates Cover and Team Profile pages, unfilled here. Mapping: slides 1-2 Background and Problem; 3-4 Solution; 5 Business Impact; 6 Roadmap and Risk.

**Source key** (`data/processed/engine/` unless noted): T `eng_material_tier`, H `eng_health_flags`, R `eng_scenario_result`, PP `eng_proposed_parameters`, A `eng_recommendation`, V `eng_forecast_validation`, C `eng_scenario_comparison`, S `eng_sensitivity_summary`, X `eng_supply_context`, K `eng_kpi_summary`, F `eng_forecast`, E `eng_explanation_facts`. In `data/processed/`: POP `simulation_population`, PL `mart_procurement_line__original_rows`, DS `mart_material_demand_summary__scenario_a/b`.

**Filters:** HO = R `config_id` K30, K31, K32 (197 materials). MC-D = R K20 (228). **Labels:** [Hist] historical, [Rule] derived, [HO] held-out, [MC] in-sample.

**Storyline:** Records cannot support one uniform rule (1). Evidence shows why (2). INSpire grades evidence before deciding (3). Candidates are calculated openly and tested twice (4). Shortages fall, stock rises (5). Facts, approvals and costs come before a pilot (6).

## Slide 1. Background and Problem

**Headline:** Uniform rules meet uneven evidence: only 228 of 7,481 parts support proposed parameters

**Message:** The brief's gap, no "integrated and predictable approach", appears here as parts with very different evidence under rule-like parameters.

**Evidence:**
- [Hist] Funnel: 7,481 → 1,930 issued → 665 simulatable → 228 Grade A (`T.active_months`, `T.tier`, `T.policy_grade`).
- [Hist] 3,527 hold stock with no recorded issue (`H.flag_non_moving_by_recorded_issues`).
- [Hist] Max is exactly 2× or 3× Min on 400 of 665 (`POP.max_parameter_unverified`/`min_parameter_unverified`).

**Root causes** (patterns supported, causes hypotheses, `docs/strategy/ROOT_CAUSE_ANALYSIS.md`): static Min-Max; sparse demand; promises without receipts; undefined master data.

**Visual:** Left funnel, right issue tree: central problem → four causes → one number each.

**Takeaway:** The first decision is whether a part has enough evidence.

**Speaker:** "The brief asks for predictable forecasting and inventory settings. In this synthetic dataset, most parts lack the evidence to support either. Yet recorded parameters look rule-like. So applying one method everywhere can create false precision."

## Slide 2. Evidence Analysis

**Headline:** Sparse demand, conflicting Min-Max and promised dates limit what can be claimed

**Message:** Three evidence gaps decide which methods are defensible.

**Evidence:**
- [Rule] Classes: D0 5,551, D1 1,475, D2 159, D3 272, D4 24 (`T.demand_class`). 1,220 issued in one month only (`T.active_months`).
- [Hist] 1,376 above recorded Max, 906 at or below Min, undated (`H.flag_stock_above_recorded_max`, `H.flag_stock_at_or_below_recorded_min`).
- [Hist] 398 of 665 conflict with Max as order-up-to: line 173, PR quantity 176, stock 256, overlapping (POP `single_line_exceeds_max`, `median_pr_quantity_exceeds_max`, `stock_above_max`).
- [Hist] Promised interval p10 15, median 42, p90 155 days, CV 1.23 (`PL.promised_interval_days`, 11,609 rows). Not goods receipts.
- [Hist] 46.7% of PR rows and 863 of 17,518 issue lines are exact copies, analysed both ways (PL versus exact-distinct; `DS.n_issue_lines`).

**Visual:** Class bar; 398 conflict tile; interval box plot; red data-quality strip.

**Takeaway:** Evidence quality must be an input to the decision.

**Speaker:** "Most issued parts appear in one or two months. Over half of simulated parts conflict with the usual Max reading. We hold promises, not receipts, and stock has no date. These gaps determine which methods we may use."

## Slide 3. INSpire Solution Architecture

**Headline:** INSpire turns records into reviewable decisions, and abstains when evidence is thin

**Message:** Each pillar has one named method class, so forecasts, simulations, rules and explanations are never blurred as "AI".

| Pillar | Method class | Executed output | Status |
|---|---|---|---|
| Data foundation | Validated marts | M1-M3 | Built |
| Evidence classification | Rule | T 7,481 | Built |
| Demand forecasting | Statistical, Croston-SBA | F: 296 forecast, 159 range, 7,026 abstain (`T.forecast_eligibility`) | Built |
| Parameter calculation | Resampling plus rule | PP 2,736 rows | Candidates |
| Simulation | Deterministic, stochastic | R 35,304 rows | Built |
| Recommendations, health | Rule | A 8,165; H 7,481 | Thresholds unapproved (D-25) |
| Supply context | Descriptive | X 1,250 materials | Built |
| Explanation | Template or LLM on stored facts | E 83,061 facts | LLM not built (D-07) |

**Evidence:** 103 of 103 run checks (`eng_validation_results.csv`). Independent daily loop matches 2,660 R0 runs. Verified, not validated. Application status is Atria's to confirm.

**Visual:** Central pipeline, supply context feeding from below, status chips per pillar.

**Takeaway:** Every output carries its method, evidence and limitation.

**Speaker:** "Materials enter with an evidence grade. Eligible parts receive forecasts and tested candidates. Others receive monitoring or a stated abstention. Any LLM would only explain stored facts, never calculate. That separation keeps every recommendation auditable."

## Slide 4. Analytical Strategy and Simulation

**Headline:** Candidates are derived openly, tested twice, and the failed method is disclosed

**Message:** Formulas produce what-if candidates, not validated optima, answering Key Questions 1 and 2.

**Formulas:**
- Point forecast: Croston-SBA, $\hat d=(1-\beta/2)\,\hat z/\hat p$; D2 range only, D0-D1 abstain
- Lead-time demand: resampled demand over the promised interval (median if under 10 distinct observations)
- Safety stock: $SS=\max(0,\,s-\overline{LTD})$
- Reorder: $s(\alpha)=\lceil Q_\alpha(LTD)\rceil$, $\alpha$ = 0.90, 0.95, 0.98
- Quantity: $Q=\lceil$median PR quantity$\rceil$; target: $S=s+Q$
- Rule: order when $H+O-B\le s$

**Evidence:**
- Reading: R0/R1 treats Min as reorder point, Max as order-up-to, the conventional reading the data cannot confirm (D-02). Alternative R2 keeps Min and orders median PR quantity; mean fill change 0.049-0.051 (`S.mean_abs_fill_rate_change`, K0, R2).
- Eligibility: 228 at 6+ active months; 140 have resampled intervals (POP `resampling_allowed_demand`, `resampling_allowed_lead`).
- **Failure:** bootstrap quantile beats mean-of-history on only 26-27%, 30-33%, 41-48% of materials at 0.90, 0.95, 0.98. Coverage 0.968-0.979 at nominal 0.90, so reorder points err high (V `share_beating_mean_pinball_*`, `empirical_coverage_0.9`). X1-X3 remain what-ifs (D-26).

| Test | Held-out replay [HO] | Monte Carlo [MC] |
|---|---|---|
| Parameters | 2025-05 to 2026-03 only | Same history resampled, flatters X |
| Demand | Recorded issues, 183 test days | 3-month blocks, 1,000 replications |
| Measure, recorded → X2 | Shortage materials 44-50 → 16-23 | Shortfall probability 0.564-0.582 → 0.247-0.256 |
| On-hand ratio | 1.56-2.58× | 1.75× |

Caveat: test months are quieter than the training peak.

**Worked example, material 4100029830** (EA, A/ED, lumpy, Low confidence; PP, R). Recorded Stock 3, Min 3, Max 5. In-sample X2: mean LTD 4.26, $Q_{0.95}$ 16, s 16, SS 11.74, Q 31, S 47. [HO, K30], training-only s 17, S 49, 16 units issued:

| Policy | Fill | Mean on-hand | Orders | Units ordered |
|---|---|---|---|---|
| R0 | 0.625 | 3.73 | 4 | 18 |
| R2 | 1.000 | 28.55 | 1 | 32 |
| X2 | 1.000 | 40.79 | 1 | 46 |

**Visual:** Formula-to-decision flow, method comparison, example strip.

**Takeaway:** R2 matches X2's fill with less stock here, so the choice remains a trade-off.

**Speaker:** "Our quantile method failed its pre-registered test and errs high, so we keep X policies as what-ifs. Held-out replay is our fairer test. Monte Carlo explores uncertainty but flatters X. This part shows it plainly: recorded settings run short in replay, while R2 needs less stock than X2."

## Slide 5. Business Impact and USP

**Headline:** Fewer simulated shortages and fewer orders, paid for with more stock

**Message:** INSpire exposes the trade-off; none is declared optimal (D-27).

**Held-out only, 197 materials, ranges across 12 combinations:**

| Policy | Shortage materials | Mean fill | Orders | On-hand vs R0 |
|---|---|---|---|---|
| R0 | 44-50 | 0.881-0.910 | 250-475 | 1.00× |
| R2 | 26-41 | 0.935-0.954 | 129-241 | 1.00-1.71× |
| N1 | 31-42 | 0.931-0.952 | 120-190 | 1.00-1.40× |
| X1 | 16-26 | 0.959-0.972 | 145-217 | 1.35-2.24× |
| X2 | 16-23 | 0.959-0.977 | 153-223 | 1.56-2.58× |
| X3 | 14-22 | 0.963-0.982 | 159-225 | 1.73-2.78× |

Source: R `any_shortfall`, `sim_fill_rate_quantity`, `orders_placed`, `mean_on_hand` (median per-material ratio). Metrics: count with any stockout day; served-on-day quantity ÷ issues.

**Evidence:**
1. **Availability:** X2 has fewer shortage materials than R0 in 12 of 12; unmet rises on 4 of 2,364 pairs (`C.tradeoff`).
2. **Inventory:** no X2 pair lowers both unmet and on-hand; 224 keep unmet equal with less stock. N1 is the low-stock alternative.
3. **Procurement:** fewer orders in 12 of 12, but X2 ordered quantity is higher on 63-81% of pairs, median 1.74-2.28× where R0 ordered (`sim_order_quantity_total`).
4. **Coverage:** Reorder 112, Maintain 44, Reduce 62, scenario-dependent 10, Monitor 4,595, No action 2,658 (`A.consensus_action`, `consensus_status`).
5. **Risk transparency:** Stockout risk High 139, Medium 33, Low 56; 7,253 not assessed (`H.stockout_risk_level`). 89 and 68 of 912 actions change at 90% and 98% (`A.action_at_90`, `action_at_98`).

**Visual:** Dominant scatter: shortage materials versus on-hand ratio, one panel per opening rule. Red "FI-1 to FI-4 NOT_COMPUTED" tile (`K.status`).

**Takeaway:** Better simulated availability requires an approved stock-and-cost decision.

**Speaker:** "On held-out months, simulated shortages fall sharply under X2. But median stock rises by 1.56 to 2.58 times, and ordered quantity also grows. We claim no savings. We show management the trade-off, material by material, for a costed decision."

## Slide 6. Implementation Roadmap and Risk Management

**Headline:** Confirm the data meanings first, then pilot under human approval

**Message:** Deployment depends on confirmed definitions, approved costs and governed release, with durations set after confirmation.

| Phase | Activities and outputs | Stakeholders |
|---|---|---|
| Done | Marts, engine, run manifest | Data team |
| 1 MVP | Application, SQLite, deck | Team |
| 2 Validate | Stock date, Min-Max meaning, receipts, costs | Planners, procurement, finance |
| 3 Pilot | Live data, review loop, measured baselines | Planners, reliability |
| 4 Extend | Monthly re-estimation, logistics data | Logistics, warehouse |

**Evidence:** Opening stock moves fill most: 0.212 upper bound, 0.073 at Min, against A-versus-B 0.016 (S, `C.metric_*_fill_rate`). All recommendations carry limitation codes (`A.limitations`). Governance: 5,507 of 8,165 recommendations require review (`A.requires_review`), plus fixed seed, hashed manifest and approved thresholds.

**Scoring (team judgement):** Severity 1 minor to 5 invalidates headline. Likelihood 1 remote to 5 already observed. Score = S×L: 15-25 Critical, 8-14 High, 1-7 Watch.

| Risk | S | L | Score | Mitigation | Owner | Trigger |
|---|---|---|---|---|---|---|
| Undated stock | 5 | 4 | 20 Critical | Three opening rules; obtain date | Lead | Date absent at Phase 2 |
| Reorder points err high | 4 | 5 | 20 Critical | Keep what-ifs; recalibrate | Lead | Coverage above nominal |
| Stock rises uncosted | 4 | 4 | 16 Critical | Approve cost sets (D-09) | Brilian | FI status NOT_COMPUTED |
| Min-Max reading wrong | 5 | 3 | 15 Critical | Run R2 alongside | Lead | Case-owner answer (C-2) |
| Promises differ from receipts | 4 | 3 | 12 High | Obtain receipts | Procurement | Receipt-promise gap |
| Unapproved data release | 5 | 2 | 10 High | Samples until D-07 | Lead, Atria | Real data in build |
| LLM exceeds facts | 4 | 2 | 8 High | Facts-only answers | Atria | Answer without fact ID |

**Visual:** Left timeline, right 5×5 heatmap, compact risk table.

**Takeaway:** The most valuable next step is the date of recorded stock.

**Speaker:** "Before any pilot, we confirm the stock date, Min-Max meaning, receipts and costs. Planners approve every candidate. Each risk has an owner and trigger. Better facts change inputs, while the governed architecture stays the same."

## Five Defensible USPs

1. Abstention: 7,026 materials receive no forecast, each with a stated reason (`T.abstain_reason`).
2. Material-level classes D0-D4, used to gate methods.
3. Six policies compared under common start and common random numbers.
4. Recommendations carry reason, trigger, limitation and scenario (A).
5. Promised-interval spread and supplier shown per material, labelled as promises (X).

## Five Critical Evidence Limitations

1. Stock is undated; opening stock is the largest sensitivity.
2. Min-Max meaning is unverified; 398 of 665 conflict.
3. No goods receipts; promised intervals only. Issues are not proven demand.
4. Quantile method failed validation; proposed parameters err high.
5. Synthetic data, no costs, no financial KPIs. Currencies stay separate (`X.currency`), with no conversion.
