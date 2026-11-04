# INSpire Technical Handover for Atria

**Status:** DRAFT v0.1. **Owner of this document:** Lead. **Owner of implementation:** Atria. Definitions: `docs/strategy/MASTER_SOLUTION_BLUEPRINT.md` section 6. Requirements R-01 to R-14 are USER-STATED until the brief is checked (D-01).

## 1. What exists today, and what does not

| Item | State |
| --- | --- |
| Validated marts M1 to M3 (CSV, git-ignored, confidential) | **Exists** in `data/processed/` with `mart_metadata.json` |
| Simulation design and feasibility evidence | **Exists**. Engine **does not exist** |
| Engine output files in Section 5 | **Do not exist yet.** Build against the contract. The Lead will supply sample files in the contract format before the first real run (not yet created) |
| AETHER | Not in this repository, not inspected. You must provide the inventory in Section 11 |
| Cost scenario file from Brilian | Does not exist yet |

Start now with the schema, loaders, UI shell and assistant on sample data. Do not wait for the engine.

## 2. Product architecture

Static or server-rendered web app, a SQLite file built offline from engine output, a template-first assistant, and a review log. The application reads files and displays them. It never recalculates a recommendation, a parameter or a risk number.

## 3. Application modules

| Module | Function | Capability |
| --- | --- | --- |
| M-A Overview | Counts by tier, class and capability flag. Data label and scenario selector visible | All |
| M-B Material list | Filter by tier, class, flag, unit, criticality counts | All |
| M-C Material detail | Recorded state, demand history by month under A and B, procurement summary under OR and ED, context, recommendations | All |
| M-D Policy comparison | Recorded (R1, R2) versus proposed (X1 to X3) with shortfall probability and on-hand | 1, 2, 3, 5 |
| M-E Alerts | Slow-moving and stockout, overstock flags with wording rules | 1, 2, 4 |
| M-F Cost-risk scenarios | Grid by cost set, only approved sets | 6 |
| M-G Assistant | Explain a recommendation from stored facts | 1 to 6 |
| M-H Review queue | Approve, reject, defer with reason | All |
| M-I Data and method | Data label, limitations, definitions, evidence tiers | n/a |
| M-J Supply context (PROPOSED, D-14) | Per material: supplier, currency, promised interval (median, p75, p90), requested-versus-promised gap, line counts under both PR PO views. Label: "promised procurement interval, not transport time" | Supports 3, 5 |

## 4. User journeys

1. **Planner triage:** Overview, filter T3 with flag "requires review", open detail, read recommendation and evidence, approve or defer.
2. **Understand why:** from a recommendation, ask the assistant "why this reorder point", get an answer quoting stored facts and the scenario ID.
3. **Compare policies:** open policy comparison, switch demand scenario and PR PO view, see the divergence flag.
4. **Slow-moving review:** list by months since last issue, open material, see "slow-moving by recorded issues".
5. **Cost-risk view:** choose an approved cost set, see assumption-labelled exposure next to simulated shortfall.
6. **Abstention:** open a D1 material, see "insufficient evidence" with reason, no number.

## 5. Analytical input contract (v0.1)

Files under `data/processed/engine/`, CSV, UTF-8, one `eng_run_manifest.json` per run. Every row carries `run_id`. Blank means no value, never zero.

| File | Grain | Key columns |
| --- | --- | --- |
| `eng_run_manifest.json` | One run | `run_id`, `spec_version`, `engine_version`, `data_label`, `config_id`, `seed`, `input_checksums`, `created_at` |
| `eng_material_tier.csv` | Material | `material_no`, `tier` (T1, T2, T3), `demand_class` (D0 to D4), `evidence_subtier`, `confidence` (Low, Medium, Abstain), `abstain_reason`, `flag_scenario_divergent`, `flag_outlier_review` |
| `eng_scenario_result.csv` | Material and scenario | `material_no`, `scenario_id`, `demand_scenario`, `pr_view`, `policy`, `unmet_rule`, `config_id`, `shortfall_probability`, `expected_unmet_qty`, `days_at_or_below_zero`, `mean_on_hand`, `p95_on_hand`, `units_above_recorded_max`, `orders_placed`, `unit`, `result_type` (`replay` or `simulation`) |
| `eng_proposed_parameters.csv` | Material, scenario and service level | `material_no`, `scenario_id`, `service_level`, `proposed_s`, `proposed_S`, `proposed_Q`, `safety_stock`, `recorded_min`, `recorded_max`, `unit` |
| `eng_capability_output.csv` | Material, capability and scenario | `material_no`, `capability` (stockout_risk, overstock_risk, reorder, slow_moving, dynamic_parameters, cost_risk), `scenario_id`, `flag`, `value_num`, `unit`, `confidence`, `requires_review`, `reason_codes` |
| `eng_explanation_facts.csv` | Fact | `material_no`, `fact_id`, `capability`, `fact_key`, `value`, `unit`, `scenario_id`, `source_file`, `source_column` |
| `fin_scenario_grid.csv` (from Brilian) | Material, scenario and cost set | Defined in `BRILIAN_FINANCIAL_HANDOVER.md` |

**Addendum A (PROPOSED, pending D-14 and D-16): `eng_supply_context.csv`.** Grain: material and PR PO view. Columns: `material_no`, `pr_view`, `supplier_code`, `supplier_name`, `currency`, `n_lines`, `promised_interval_days_median`, `promised_interval_days_p75`, `promised_interval_days_p90`, `n_lines_used_for_promised_interval`, `requested_interval_days_median`, `supplier_share_of_lines`, `source_file`. The Lead writes it as a thin export of M1 columns. Atria does not compute these values. Until it exists, use sample rows.

`scenario_id` follows `SC-<D>-<V>-<P>-<S>-<K>`. Column names may gain fields in v0.2. Existing names will not change without notice in `TEAM_INTEGRATION_PROTOCOL.md`.

## 6. Database entities (SQLite)

| Table | Content | Writable at runtime |
| --- | --- | --- |
| `material` | M2 state fields, tier, class | No |
| `demand_month` | M3 monthly demand per scenario | No |
| `procurement_summary` | M1 summary per view | No |
| `scenario_result`, `proposed_parameters`, `capability_output` | From engine files | No |
| `explanation_fact` | From engine facts | No |
| `cost_scenario_grid` | From Brilian | No |
| `recommendation` | One per material, capability and scenario, built from `capability_output` | No |
| `review_action` | `rec_id`, `action`, `reviewer`, `reason`, `timestamp`, `run_id` | **Yes** (see D-08) |
| `assistant_log` | Question, facts quoted, answer, timestamp | **Yes** |
| `run_manifest` | One row per loaded run | No |

Foreign keys on `material_no` and `run_id`. Reject load if the manifest checksum or `data_label` is missing.

**Logistics extension points (design only).** Create `ref_location`, `ref_supplier_site` and `ref_transfer` as **empty** tables, and nullable `location_id` on stock and result rows. Do not populate them. Do not add routing, distance, freight or transfer logic, screens or placeholder charts with invented values. A Level C screen, if shown, is a static "data required" list from `analytics/TRANSPORTATION_AND_DISTRIBUTION_ASSESSMENT.md` section 7.

## 7. AI assistant contract

| Rule | Detail |
| --- | --- |
| Source of numbers | Only rows of `explanation_fact` and `capability_output` for the selected material and scenario |
| Allowed | Explain, summarise, compare two stored scenarios, list limitations and review reasons, say "not enough evidence" |
| Not allowed | Compute or alter any quantity, state a number not in the facts, recommend outside the stored candidates, claim a historical stockout, claim a saving, use "optimal" |
| Required in every answer | Scenario ID, evidence tier, confidence, data label |
| Failure mode | If asked something the facts do not hold, say so and point to the missing input |
| Test | Every number in an answer must match a stored fact. Fail the build if not |
| Baseline implementation | Template text from fact keys, no external model. An external language model is optional and only after D-07 is closed. If allowed, send stored facts only, never raw rows or marts |

## 8. Human approval workflow

States: `GENERATED` to `UNDER_REVIEW` to `APPROVED`, `REJECTED` or `DEFERRED`. Rules:

1. Only a human changes state. The assistant cannot.
2. `requires_review` items cannot be approved without a reason text.
3. Approval means "accept this candidate for the planner's own use", not that anything changes in an ERP.
4. Every action is logged with run ID. A new run does not erase earlier actions.
5. A recommendation from a superseded run is shown as superseded.

## 9. Display rules (acceptance-critical)

- Data label on every page.
- Scenario ID, demand scenario and PR PO view on every number from the engine. No default scenario. Either show A and B together, or require an explicit pick and show a divergence flag (D-11).
- "Recorded" for BoM values, "proposed" or "candidate" for engine values, "simulated" for simulation results, "replay" for replay results.
- Never: "actual stockout", "savings", "optimal", "lead time" without "promised".
- Quantities in their own unit. No sum across units. No sum across currencies.

## 10. Capability demonstration workflows

| Capability | Demo flow | Must show |
| --- | --- | --- |
| 1 Stockout Risk | Open a T3 material, view shortfall probability for R1 and X2 under A and B | Word "simulated", scenario ID, abstention for a D1 material |
| 2 Overstock Risk | Material with recorded stock above recorded Max, show recorded and simulated excess | "Recorded" versus "simulated" |
| 3 Reorder Recommendation | Candidate s and Q with trigger state | Candidate wording, approval buttons |
| 4 Slow-Moving Alert | List sorted by months since last issue | "Slow-moving by recorded issues", D0 shown as "no recorded consumption" |
| 5 Dynamic Inventory Parameters | Recorded Min/Max beside proposed s and S at service-level scenarios, plus the change history from replay | "Service-level scenario, not target" |
| 6 Cost-Risk Optimisation Scenarios | Pick an approved cost set, see assumption-labelled exposure and simulated shortfall | Cost set ID, no saving claim |

## 11. Integration with AETHER

AETHER is maintained separately and was not inspected. Before design is final, deliver to the Lead:

1. List of AETHER components, with what each does and whether it works.
2. Which components you propose to reuse for M-A to M-I, and why.
3. Anything in AETHER that stores or sends data externally.

Do not replace working AETHER components without a stated reason. Do not copy files from the AETHER repository into this repository. Integrate through the file contract.

## 12. Testing and acceptance

| Test | Pass condition |
| --- | --- |
| Contract load | Loads the sample files, rejects a file with a missing column or missing label |
| No recalculation | Displayed values equal stored values, byte for byte |
| Labels | Every page has the data label. Every engine number has a scenario ID |
| Wording | A text scan finds no "optimal", "actual stockout", "saving" outside the permitted context |
| Assistant | All six capabilities answered from facts, one abstention answered correctly, numbers match |
| Workflow | A review action is logged and survives a reload (as far as D-08 allows) |
| Scenario switch | Switching A and B changes numbers and shows the divergence flag |
| Accessibility and mobile | Basic checks on the main views |

Acceptance of the MVP by the Lead is a walk through the six capability flows on real engine output.

## 13. Deployment requirements and open conflicts

- SQLite and Vercel are USER-STATED requirements (R-02, R-03).
- **Conflict 1 (D-07).** The project rule is not to upload competition-provided data to external services. A Vercel deployment publishes derived data. Decide before deploying real output. Fallback: deploy with the sample files, labelled "illustrative sample".
- **Conflict 2 (D-08).** Vercel serverless storage is not persistent for writes. Options: bundled read-only SQLite with review actions held in the browser session, or a Vercel-compatible persistent store. Propose one with consequences.
- Secrets in environment variables only. No data in the public repository.
- Build is reproducible from a tagged run ID.

## 14. Work order if time is short

1. Contract loader and SQLite schema on sample files.
2. Overview, material detail, label and scenario display.
3. Capabilities 1 to 5 views, review queue.
4. Template assistant.
4a. Supply context panel M-J (only after D-14, small effort, from sample rows first).
5. Capability 6 view, deployment, polish.

## 15. What you must not do

Implement or mock transportation, routing, allocation or transfer optimisation. Present a movement, plant or functional-location field as a route or warehouse. Describe promised interval as transport or delivery time. Recalculate any recommendation. Choose a default scenario. Drop the data label. Sum across units or currencies. Send source data or marts to an external service. Change engine files. Change `docs/analysis` or any mart.

## Addendum B (PROPOSED, pending D-19 and D-23): official brief alignment, 2026-11-04

OFFICIAL facts from `CALIBER 2026 - Final Case Brief.pdf` that affect the build (p8): the prototype must be a **working MVP, not static HTML**, published to **Vercel**, with a **SQLite** database, delivered with complete source code and the database in one **.zip**, plus a **timestamped screenshot** of the latest Vercel deployment. Deadline 2026-11-05 06:00.

Proposed additive contract fields (contract v0.1 columns do not change, adding is backward compatible):

| File | Added column | Values | Meaning |
| --- | --- | --- | --- |
| `eng_capability_output.csv` | `recommended_action` | `REORDER`, `HOLD`, `REDUCE`, `MONITOR`, `NO_ACTION_EVIDENCE` | The brief's four actions (p4). `HOLD` stands for "maintain" (TEAM reading, confirm). `NO_ACTION_EVIDENCE` is an abstention |
| `eng_forecast.csv` (new, optional) | `material_no`, `demand_class`, `horizon_basis`, `lead_time_demand_low`, `lead_time_demand_mid`, `lead_time_demand_high`, `unit`, `scenario_id`, `confidence`, `abstain_reason` | | Forecast output for R-16. Empty range with an abstain reason for D0 and D1 |

Rules: show `recommended_action` as a candidate needing review. Do not compute it in the application. Wording on non-moving and obsolete follows D-21. The zip must contain only what the Lead approves for bundling (D-07). Take the screenshot after the last deploy.

## Addendum C: Phase 1 baseline lock (2026-11-04)

Read first: `strategy/MASTER_SOLUTION_BLUEPRINT.md` section 12, `strategy/PHASE_2_EXECUTION_PLAN.md` (A1 to A5), `strategy/DECISION_REGISTER.md`.

**Start now (no blocker):** A1 schema and loaders, A2 UI on sample files, A3 templated assistant, A4 Vercel smoke deploy with sample data and a persistence test. Report the persistence result to the Lead (D-08).

**Do not start:** real-data load and final deploy (A5) until the Lead records D-07. Do not put raw workbook rows, `data/raw/` or full line-level procurement tables in the database or zip. Do not call an external language model with project data.

**Authoritative counts for display and tests:** tiers 5,551 / 1,265 / 665. Forecast eligible 296, rate range 159, abstain 1,475. Parameters for 228 only (D-24). See `analytics/FIGURE_AND_METHOD_RECONCILIATION.md`. Do not reuse the uppercase class names D1 to D4 for the file column `demand_evidence_tier`.

**Display rules added:** show the method class (statistical, simulation, rule) beside each output. Show `recommended_action` as a candidate. Show "sample data" on every page until real data is approved. Persist nothing unless the smoke test proves it.

**Acceptance for the baseline** is in the execution plan. A feature is "done" only with a test or screenshot as evidence.
