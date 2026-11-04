# INSpire Figure and Method Reconciliation

**Status:** Phase 1, 2026-11-04. Every figure below was recomputed read-only from `data/processed/*.csv` (python `-I`, no files written) and compared with the document that states it. No mart, result or source was changed. **No simulation engine exists and no simulation has been run.** Figures in `docs/analysis/SIMULATION_*` are pre-analysis arithmetic on inputs, not simulated outputs.

## 1. Population hierarchy

| Population | Count | Definition | Source file and column | Used for |
| --- | --- | --- | --- | --- |
| All materials | 7,481 | BoM materials | `simulation_population.csv` (7,481 rows) | Tier table |
| Issued materials | 1,930 | At least one issue line, Scenario A and B alike | `mart_material_demand_summary__scenario_a.csv` (`months_with_issue` at least 1) | Demand classes D1 to D4 |
| Never issued | 5,551 | 7,481 minus 1,930 | same | D0, tier T1 |
| Simulation population (T3) | 665 | `population_status = in_population`: Stock Item, demand history, promised interval, unit amount, non-zero Min or Max | `simulation_population.csv` | Policy comparison, all six outputs at some grade |
| Excluded from simulation | 6,816 | `population_status = excluded` | same | No policy output |

## 2. Forecast and resampling counts: one table, three populations

All counts reproduced exactly. The same numbers had been mixed in conversation because they describe **different populations and different questions**.

| Figure | Population | Question answered | Rule | Source (reproduced) | Authoritative for |
| --- | --- | --- | --- | --- | --- |
| **1,475** | 1,930 issued | Sparse demand | `months_with_issue` 1 or 2 (`flag_sparse_history`) | demand summary A and B (identical) | Demand class D1, abstain from forecast |
| **159** | 1,930 issued | Thin demand | `months_with_issue` 3 to 5 | same | Class D2, rate range only |
| **296** | 1,930 issued | Demand forecast eligible | `months_with_issue` at least 6 (classes D3 plus D4) | same. 1,475 + 159 + 296 = 1,930 | **Forecast output (R-16)** |
| **228** | 665 in T3 | Demand-resampling eligible inside the simulation | at least 6 active months, within T3 (`resampling_allowed_demand`) | `simulation_population.csv` | **Stochastic demand simulation** |
| **68** | 296 minus 228 | Forecast-eligible but not in T3 | `population_status = excluded` | computed | Forecast shown, no policy output |
| **140** | 665 in T3 | Lead-time resampling eligible | at least 10 distinct lead observations (`resampling_allowed_lead`) | same | Lead-time resampling |
| **139** | 665 in T3 | Both resampled | 6 months and 10 lead observations | `resampling_allowed_both` | Joint resampling |
| 166 | 7,481 all | Lead tier `l1_resampling_allowed` across all materials | same threshold, all materials | `lead_evidence_tier` | Not used. Context only |

**Reading:** 228 is a subset of 296 (the forecast-eligible set restricted to the simulation population). 139 is a subset of 228 and of 140. These are consistent, not contradictory. The earlier blueprint wording "forecast eligible 296" and the simulation wording "228" differ only in population.

**Name collision (corrected here).** `simulation_population.csv` uses lowercase tier labels `d1_resampling_allowed` (296), `d2_replay_and_configured_only` (414), `d3_single_active_month` (1,220) for **demand evidence**, ordered best first. The blueprint's demand classes D0 to D4 (uppercase) are ordered by sparseness, and **D1 means sparse**. They are different scales. Rule: always write "demand class D3" for the blueprint scale and `demand_evidence_tier = d1_resampling_allowed` for the file column. The two scales map as: file `d1_resampling_allowed` = classes D3 plus D4 (296); file `d3_single_active_month` = class D1 subset (1,220 single-month); file `d2_replay_and_configured_only` (414) = remaining issued materials with 2 to 5 months (1,930 − 296 − 1,220 = 414, consistent with D1 two-month plus D2).

## 3. Contradiction found and resolved: which materials get parameters

| Document | Said | Problem |
| --- | --- | --- |
| Blueprint section 6.3 (v0.1) | T3 (665) gets "all six capabilities" with an evidence sub-tier | Implies proposed Min-Max for 665 |
| `DEMAND_INTELLIGENCE_METHODOLOGY.md` section 3 | Only classes D3 and D4 within T3 get Reorder and Dynamic Parameters. D1, D2 abstain | Implies parameters for 228 |

Inside T3, 437 materials (665 − 228) have fewer than 6 active months. **Safe default adopted in the baseline (D-24, needs your approval):** the demand methodology governs. Grade A, 228 materials, get stochastic outputs and proposed parameters. Grade B, 437 materials, get R0 replay and configured what-if only, and **no proposed s, S or Q** (the recommended action is MONITOR or NO_ACTION_EVIDENCE). Reason: no distribution from thin history (standing rule). Cost: dynamic Min-Max covers 228 materials, not 665. If you prefer 665, the configured-demand parameters must be labelled "scenario-configured, low confidence" and cannot be called forecasts.

## 4. Scenario and view definitions (restated, unchanged)

| Item | Definition | Source |
| --- | --- | --- |
| Demand Scenario A | All 17,518 eligible Movement lines | Demand marts, design spec |
| Demand Scenario B | 16,655 lines, excluding 863 exact-copy lines (rule C1) | same |
| Identical by construction | 436 of 665 T3 materials have the same demand under A and B. 88 are materially affected | `scenarios_identical_by_construction`, `demand_materially_affected` |
| PR PO `original_rows` | 11,609 rows | PR PO views |
| PR PO `exact_distinct_rows` | 6,189 rows | same |
| No default | Neither scenario nor view is the baseline | Standing rule |

## 5. "Common-start" versus "independent-start"

**These two terms do not appear in any repository document.** The nearest concepts in `SIMULATION_DESIGN_SPECIFICATION.md` are:

- **Common start (the design rule).** All policies and both scenarios start from the same assumed day-0 stock, the undated BoM `Stock` value (S-01, `assumed_initial_inventory`), with no on-order and no backorders (S-02). They also share random draws (common random numbers, spec lines 277 and 404), so differences come from inputs, not sampling noise.
- **Alternative start (sensitivity only).** The initial-inventory factor φ_I may be set to Min, Max, or stock plus window issues (spec line 233). That is a sensitivity run, not a separate comparison method.

If "independent-start" refers to a comparison in which each policy starts from its own level, it is **not in the design**. Ask the Lead (clarification C-3 in the Decision Register). The design warns that 183 materials sit at or below Min on day 0, so their early shortfalls come from the starting assumption and are reported separately.

## 6. Check counts

| Statement | Where | Verified now |
| --- | --- | --- |
| 750 of 750 validation checks pass | Blueprint, checklist | `outputs/tables/validation_results.csv`: 750 rows, all PASS |
| 354 tests pass | Blueprint, checklist | `pytest` run today: 354 passed |
| 721 checks and 309 tests | `docs/analysis/DATA_MART_REPORT.md` section 11 | **Historical** at the M1 to M3 build. Superseded by the simulation-design checks (+29 checks, +45 tests). Left unchanged because it is a dated stage report |

## 7. Simulation status

**Superseded on 2026-11-04.** The engine is built and has run: `SIMULATION_METHODOLOGY_AND_RESULTS.md`, run `RUN-277fc4b966e6`. The population counts in sections 1 and 2 were recomputed from the marts in the run and hold. The indicative pattern split changed: Scenario A is 116 erratic, 100 lumpy, 53 intermittent and 27 smooth, where the methodology had 112, 87, 66 and 31. The table below is the Phase 1 record.

| Item | Status |
| --- | --- |
| Design specification, assumption register, feasibility assessment | IMPLEMENTED as documents, checks and tests exist |
| Simulation population file | IMPLEMENTED (`simulation_population.csv`, 7,481 rows) |
| Simulation engine (R0 replay, R1, R2, X policies, Monte Carlo) | **Not built. Not run.** |
| Any shortfall probability, service level, saving | **Do not exist.** Anything shown before the engine runs is a placeholder and must be labelled sample |
| Figures in the feasibility assessment (for example 398 of 665 conflict with Max as order-up-to level, 183 at or below Min on day 0) | Pre-analysis observation, not model output |
