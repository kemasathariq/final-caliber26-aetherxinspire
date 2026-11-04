# INSpire Phase 2 Execution Plan

**Status:** Phase 2 started on the Lead's instruction, 2026-11-04. Lead workstreams L1 to L6 are **executed**, run `RUN-277fc4b966e6`. See section 7. Deadline: Thursday 2026-11-05 06:00 (time zone unconfirmed, C-7). Shared definitions: `MASTER_SOLUTION_BLUEPRINT.md` sections 6 and 12. Decisions: `DECISION_REGISTER.md`.

**Change control.** A workstream may not change a shared definition (scenario grammar, tiers, terms), a contract column, or a metric. It raises a change request to the Lead, who records it in `handover/TEAM_INTEGRATION_PROTOCOL.md` section 3. Until then the old definition applies.

## 1. Workstreams

| WS | Owner | Deliverable | Starts now? | Depends on | Acceptance |
| --- | --- | --- | --- | --- | --- |
| L1 Contract samples | Lead | Sample files in contract v0.1 + 0.1-B format for about 10 materials, **clearly labelled sample, not results**, plus `eng_run_manifest.json` | Yes, first | none | Files load without error. Every row has `result_type = sample`. No value presented as a result |
| L2 Engine R0 | Lead | Deterministic replay for the 665 under A and B, both views. Output files `eng_*` | Yes, after L1 | D-02 (default R1 usable), D-04 | Reproduces the spec's worked example. Independent second loop agrees. `result_type = replay`. Checks pass. Existing tests still pass |
| L3 Tier and forecast files | Lead | `eng_material_tier.csv` (7,481 rows), `eng_forecast.csv` for 296 | Yes, parallel with L2 | D-06, D-23 | Counts match reconciliation (5,551, 1,265, 665; 1,475, 159, 296). Abstain reason for each D0 and D1 |
| L4 Stochastic and policy runs | Lead | R1, R2, X policies, Monte Carlo for 228, 140, 139 | After L2 review | D-02, D-03, D-05, D-24 | Common random numbers. Same seed gives identical bytes. Sensitivity report. Labelled simulation |
| L5 Recommended action and flags | Lead | `recommended_action`, slow-moving, non-moving, potentially obsolete candidate | After L3 | D-19, D-21, D-25 | Rule table implemented as specified. Each row has `reason_codes` |
| L6 Supply context file | Lead | `eng_supply_context.csv` | Yes | D-14 (closed), D-16 | Equals M1 columns. Labelled promised, not transport time |
| A1 Schema and loaders | Atria | SQLite schema from the contract. Loaders with validation. Empty `ref_location`, `ref_supplier_site`, `ref_transfer` | **Yes, now** (spec exists) | none | Loads L1 samples. Rejects a file with a missing or unknown column. Unit tests pass |
| A2 UI and modules M-A to M-J | Atria | Overview, material detail, capability views, review queue, supply context | Yes, on L1 samples | A1, L1 | Handover section 12 acceptance. Scenario ID and data label on every number. No default scenario |
| A3 Assistant | Atria | Templated explanation over `eng_explanation_facts` | Yes | A1 | Never returns a number absent from stored facts. Says "not enough evidence" when facts are missing |
| A4 Vercel smoke deploy | Atria | Deploy a **sample-data** build. Test write persistence on a cold function | **Yes, now** | none (sample data only) | Public URL works, not static HTML. Persistence result recorded (D-08) |
| A5 Real-data load and final deploy | Atria | Load real derived files, final deploy, screenshot with timestamp, zip | **No** | L2 output, **D-07 approval**, L1 to L5 as available | Zip holds source and SQLite. Screenshot png or jpg shows deployed version and timestamp |
| B1 Price and amount interpretation | Brilian | Review of PO-Item Amount, reference unit amount rule, currency handling | Yes, on M1 and M2 | none | One-page memo with options. No figure presented as fact. C-5 listed |
| B2 Exposure | Brilian | Inventory exposure as ranges per currency and per PR PO view | Yes | B1 | Reproducible from M1 and M2. Currencies never combined. Labelled assumption |
| B3 Cost sets and grid | Brilian | Cost set proposals, `fin_scenario_grid.csv` | Cost sets: yes. Grid: **after L2 output** | D-09, L2 | Every input labelled with source or "assumption". No saving, no optimal claim |
| B4 Logistics cost requirements | Brilian | Missing freight input list (handover section 13) | Yes | none | List only, no values |
| D1 Deck | Lead | Deck in the official format | **No, not in Phase 2 start** | Phase 2 results | Official six slides plus Appendix, two key-question blocks |

## 2. Critical path

1. L1 samples, so Atria can integrate.
2. L2 engine R0, so a real number exists anywhere.
3. D-07 answer, so real derived data can be deployed.
4. A5 final deploy, zip and screenshot.
5. Deck.

Fallback if L2 slips: ship the sample-labelled app plus descriptive outputs from the existing marts (slow-moving, non-moving, overstock against recorded Max, demand classes, supply context). These need no engine. State "design stage, not simulated" on every simulated view.

## 3. What may start immediately

L1, L3, L6 (Lead). A1, A2, A3, A4 (Atria). B1, B2, B4, and B3 cost sets (Brilian). L2 starts once L1 is handed over.

## 4. Blocked

| Work | Blocked by |
| --- | --- |
| Real-data deploy, zip content decision (A5) | D-07, C-1 |
| Any monetary comparison (B3 grid) | D-09, L2 |
| Proposed parameters beyond 228 | D-24 |
| Recommended action thresholds | D-25 |
| Deck | Phase 2 results, team details |

## 5. Interfaces (frozen by this plan)

| From | To | Artifact | Gate |
| --- | --- | --- | --- |
| Lead | Atria | `eng_*` files, contract v0.1 plus 0.1-A and 0.1-B | Lead validation |
| Lead | Brilian | `eng_scenario_result.csv`, `eng_proposed_parameters.csv`, M1, M2 | Lead validation |
| Brilian | Lead | Cost set proposals | Lead approval |
| Brilian | Atria | `fin_scenario_grid.csv` | Approved cost sets only |
| Atria | Lead | Persistence result, AETHER inventory, deploy status | Lead decision |

## 6. Phase 2 exit criteria

All official items 1a to 1m in `submission/SUBMISSION_READINESS_CHECKLIST.md` section 1A have evidence, or a stated reason with the Lead's agreement. No claim in the "must not make" list. Tests still pass and no mart or raw data changed.

## 7. Lead workstream status (2026-11-04)

| WS | State | Evidence |
| --- | --- | --- |
| L1 Contract samples | **Done** | `data/samples/engine/`, `handover/ENGINE_OUTPUT_CONTRACT.md` |
| L2 Engine R0 | **Done** | `src/simulation/engine.py`. Gate 12 of 12. Independent loop matches 2,660 runs |
| L3 Tier and forecast | **Done** | `eng_material_tier.csv`, `eng_forecast.csv`, `eng_forecast_validation.csv` |
| L4 Stochastic | **Done** for MC-D, MC-L, MC-J. S2 not run | `eng_scenario_result.csv` |
| L5 Action and flags | **Done**, thresholds pending D-25 | `eng_recommendation.csv`, `eng_health_flags.csv` |
| L6 Supply context | **Done** | `eng_supply_context.csv` |
| Business impact layer | **Done in units**. Financial KPIs blocked | `eng_kpi_summary.csv` |
| Report | **Done** | `analytics/SIMULATION_METHODOLOGY_AND_RESULTS.md` |
