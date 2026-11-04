# INSpire Master Solution Blueprint

**Project:** CALIBER 2026 Final Round, Case 3 (Spare Part Intelligence). **Product:** INSpire, a spare part intelligence and decision-support workbench.
**Date:** 2026-11-04. **Status:** Phase 1 BASELINE v1.0 (2026-11-04), awaiting Lead approval. Section 12 is the execution baseline. Nothing is implemented except the data foundation (M1 to M3 marts, simulation population file, checks and tests). **The simulation engine, application, database, deployment and deck do not exist.** Decisions live in `DECISION_REGISTER.md`. Phase 2 plan: `PHASE_2_EXECUTION_PLAN.md`.
**Data label (use in every output):** Source data documented as synthetic (dummy) in the Data Context & Relationship Diagram. Findings describe the supplied dataset, not Chandra Asri operational performance.

**Strategic positioning (USER-STATED, confirmed by the Lead, 2026-11-04):** INSpire is an **Integrated Spare Part Supply Chain Intelligence** solution. Transportation and distribution are investigated explicitly (`analytics/TRANSPORTATION_AND_DISTRIBUTION_ASSESSMENT.md`). The official brief does not mention transportation, so this positioning is a TEAM choice, framed as supply context and a roadmap (audit section 5). **Official brief inspected 2026-11-04** (`docs/case/CALIBER 2026 - Final Case Brief.pdf`). Result: see `OFFICIAL_CASE_ALIGNMENT_AUDIT.md`. **The blueprint is only partly aligned**: 6 of 39 traced requirements are fully covered in plan, 25 partly, 4 not at all, and nothing but the data foundation is implemented. Full alignment is not claimed.

This is the single source of truth for strategy. The other documents in `docs/strategy`, `docs/analytics`, `docs/handover` and `docs/submission` implement it. Where they disagree with this file, this file wins until the Solution Lead decides otherwise.

## 1. Evidence labels

Every claim in the blueprint documents carries one of these labels, in words or by context.

| Label | Meaning |
| --- | --- |
| OFFICIAL | Stated by the official Case 3 brief, `CALIBER 2026 - Final Case Brief.pdf`, with a page number in the audit. Confirmed so far: the four capabilities and six named outputs (p4), the two key questions (p5, p6), MVP not static HTML, Vercel, SQLite, zip, screenshot, deadline (p8), deck format (p9). Everything else stays TEAM or USER-STATED |
| USER-STATED | Stated by the Solution Lead in the blueprint assignment. Treated as binding, but not yet checked against the brief. |
| OBSERVATION | Measured in the supplied data. It describes the dataset. |
| RESEARCH | Supported by a cited research document or published method. |
| ASSUMPTION | An analyst choice that data cannot settle. It is configurable and listed in the assumption registers. |
| PROPOSED | A capability or method specified here and not built. |
| IMPLEMENTED | Exists in the repository and passed its checks. Today this means only the pipeline, marts M1 to M3 and the simulation feasibility evidence. |

## 2. Source hierarchy and what actually exists

| Rank | Source | Present in repository? | Use in this blueprint |
| --- | --- | --- | --- |
| 1 | Official Case 3 brief | **Yes**, `docs/case/CALIBER 2026 - Final Case Brief.pdf` (10 pages) | Inspected. Requirements traced in `OFFICIAL_CASE_ALIGNMENT_AUDIT.md`. The Case 3 named `.md` file is still Case 2 content (C-01) |
| 2 | Six Excel workbooks | Yes, `data/raw/` (git-ignored, immutable) | Authoritative for values |
| 3 | Validated marts and data specifications | Yes. M1 to M3 accepted by the Solution Lead; 750 of 750 checks pass | Preserved. Not modified by this blueprint |
| 4 | Analytical discovery and root cause analysis | Discovery report: yes (Case 3 data). `consolidated_root_cause_analysis_reports.md`: yes, but it is Case 2 equipment RCA, not spare-part RCA | Discovery report used. Case 2 RCAs are context only (C-02) |
| 5 | Research and benchmark | Yes, `docs/research/` (company-level assessment, one spare-parts scoring row). The petrochemical process-simulation PDF is not about inventory | Context only |
| 6 | Existing INSpire proposals and simulation specifications | Simulation design, assumption register and feasibility assessment: yes. No earlier INSpire proposal found | Reused, see `docs/analysis/SIMULATION_*` |
| 7 | Application code and AETHER | **AETHER is not in this repository** (maintained separately by Atria). Not inspected | Atria must supply an inventory (D-12) |

## 3. Source conflicts, stated explicitly

| ID | Conflict | How this blueprint treats it |
| --- | --- | --- |
| C-01 | **Resolved 2026-11-04:** the official brief is `docs/case/CALIBER 2026 - Final Case Brief.pdf`. `CALIBER_2026_Case_3_Complete_Final_Case.md` (about 990 KB) remains Case 2 content under a Case 3 name and is not used | The six outputs, MVP, SQLite and Vercel are now OFFICIAL. Section 11 lists what the audit changed. Lead to confirm via D-18 |
| C-02 | The consolidated RCA reports, the "BCC Hackathon Analysis" and the Case 2 reference describe equipment reliability (seals, vibration, bearings). They are not spare-part analysis | Not used as evidence for any Case 3 root cause. Root causes come from the six datasets |
| C-03 | The assignment asks for recommended Min-Max and safety stock. The data cannot define what recorded Min.Qty and Max.Qty mean (DEF-02), has no service target and no holding, ordering or stockout cost | Recorded values are shown as "recorded, unverified". Recommended values are scenario outputs under configurable service levels, never "optimal" |
| C-04 | The assignment asks for stockout risk. Stock has no date (DEF-12) and no receipts exist | Stockout risk means **simulated** shortfall probability under stated assumptions. It is never called a historical stockout |
| C-05 | The assignment asks for cost-risk optimisation. No cost parameters exist | Delivered as scenario comparison with explicit, labelled cost inputs from Brilian. No saving is reported until approved (D-09) |
| C-06 | Earlier accepted work scopes simulation to 665 Stock Items. The six capabilities need to cover more materials | Three eligibility tiers (Section 6.3). Capabilities degrade to descriptive output outside the top tier |
| C-07 | The Vercel requirement conflicts with two project rules: no upload of competition data to external services, and SQLite writes do not persist on Vercel serverless | Flagged as decisions D-07 and D-08. Blocks deployment, not analytics |
| C-08 | The simulation design reads Min/Max as a reorder point and order-up-to level (R1), unverified | Kept as one reference policy with an alternative (R2). Decision D-02 |

## 4. Requirements traceability

Status of each row after the audit (section 11): R-01 to R-09 are OFFICIAL by name (brief p4 and p8). R-10 to R-15 are TEAM additions, not in the brief. R-16 is new. "Component" points to where the requirement is met. No row is IMPLEMENTED except R-13.

| ID | Requirement | Component | Document | Status |
| --- | --- | --- | --- | --- |
| R-01 | Functional MVP | Application modules | `handover/ATRIA_TECHNICAL_HANDOVER.md` | PROPOSED |
| R-02 | SQLite database | Entities and loaders | `handover/ATRIA_TECHNICAL_HANDOVER.md` | PROPOSED, with C-07 risk |
| R-03 | Vercel deployment | Deployment requirements | `handover/ATRIA_TECHNICAL_HANDOVER.md` | PROPOSED, blocked by D-07, D-08 |
| R-04 | AI capability 1, Stockout Risk | Simulated shortfall probability (engine output `risk_stockout`) | `analytics/INVENTORY_OPTIMISATION_METHODOLOGY.md` | PROPOSED |
| R-05 | AI capability 2, Overstock Risk | Position against recorded Max, simulated excess, cover | same | PROPOSED |
| R-06 | AI capability 3, Reorder Recommendation | Reorder point and quantity candidates, trigger state | same | PROPOSED |
| R-07 | AI capability 4, Slow-Moving Alert | Descriptive activity rule on M2 and M3 | `analytics/DEMAND_INTELLIGENCE_METHODOLOGY.md` | PROPOSED |
| R-08 | AI capability 5, Dynamic Inventory Parameters | Proposed s, S under scenario service levels versus recorded | `analytics/INVENTORY_OPTIMISATION_METHODOLOGY.md` | PROPOSED |
| R-09 | AI capability 6, Cost-Risk Optimisation Scenarios | Scenario grid joining engine outputs and Brilian cost sets | `handover/BRILIAN_FINANCIAL_HANDOVER.md` | PROPOSED, blocked by D-09 |
| R-10 | AI assistant explains, never invents numbers | Assistant contract | `handover/ATRIA_TECHNICAL_HANDOVER.md` section 7 | PROPOSED |
| R-11 | Human review of recommendations | Approval workflow | same, section 8 | PROPOSED |
| R-12 | Six data layers connected into one workflow | Architecture | `strategy/SOLUTION_ARCHITECTURE.md` | PROPOSED |
| R-13 | Preserve validated M1 to M3, no silent deduplication | Data foundation | `analytics/DATA_INTELLIGENCE_SPECIFICATION.md` | IMPLEMENTED |
| R-15 | Integrated supply-chain positioning, transportation investigated explicitly | Supply context (Level B) and logistics extension points (Level C) | `analytics/TRANSPORTATION_AND_DISTRIBUTION_ASSESSMENT.md`, `strategy/SOLUTION_ARCHITECTURE.md` section 8 | PROPOSED, USER-STATED direction, D-14 |
| R-16 | OFFICIAL (p4 capability 1, p5 key question 1): Demand Forecasting output, a visible forward-demand range or lead-time demand for D2 to D4 materials, abstention reason for the rest | Forecast fields in engine output | `analytics/DEMAND_INTELLIGENCE_METHODOLOGY.md` | PROPOSED, new (D-23) |
| R-17 | OFFICIAL (p4 capability 4): recommended action per part, reorder, hold, reduce or monitor | `recommended_action` field | `handover/ATRIA_TECHNICAL_HANDOVER.md` Addendum B | PROPOSED (D-19) |
| R-14 | No unsupported savings or performance claim | Claim rules | `analytics/VALIDATION_FRAMEWORK.md` section 7 | Enforced by checklist |

## 5. The solution in one page

**Problem (OBSERVATION-based).** In the supplied dataset, recorded Min/Max values do not line up with recorded consumption, demand for most parts is sparse, maintenance work cannot be tied to parts for most issues, and procurement data cannot tell achieved lead time or true order quantity. A planner cannot tell, from these records, which part needs attention.

**Answer.** INSpire turns the validated marts into a decision workflow of six connected layers (detail in `SOLUTION_ARCHITECTURE.md`):

1. **Data foundation and governance:** M1 to M3, eligibility tiers, evidence metadata.
2. **Equipment and maintenance context:** functional location criticality, notifications and plans as context only, never as demand without a material link.
3. **Demand intelligence:** classify each issued material, then abstain, resample, or use a method suited to its evidence.
4. **Dynamic inventory optimisation:** simulate recorded and proposed Min-Max under identical conditions, under both demand scenarios.
5. **Inventory health and risk monitoring:** six capability outputs per material with a confidence tier.
6. **AI recommendations and cost-risk scenarios:** the assistant explains stored results. Brilian's scenario sets add the cost view. A planner approves, rejects or defers.

**Principles that never change**

- A recommendation without an evidence tier is not shown.
- Demand Scenario A and B, and PR PO views `original_rows` and `exact_distinct_rows`, are carried side by side. No default is chosen. The UI must show which one a number uses.
- A simulated number is labelled simulated. Simulation never produces "actual stockouts" or money saved.
- The assistant explains and never calculates a recommendation.

## 5A. Integrated supply-chain scope and transportation positioning

INSpire connects **demand, inventory policy, procurement lead time and (in future) logistics** in one workflow. Transportation was assessed as seven problem areas and six optimisation methods. Result (OBSERVATION, details in the assessment):

- The six workbooks hold no supplier location, storage location, movement origin or destination, goods receipt, transfer, shipment or freight cost. One plant, one movement type (`Issue`), one supplier per material.
- **No transportation problem is a confirmed operational fact.** Each is a labelled HYPOTHESIS with data required.

| Level | Content | Status |
| --- | --- | --- |
| A. Core MVP | No transportation-specific capability. Promised procurement interval already feeds the inventory engine as lead-time proxy | Unchanged |
| B. Supporting intelligence | Supply context panel: supplier, currency, promised interval and spread, requested-versus-promised gap, supplier concentration, labelled "promised, not transport time" | PROPOSED (D-14), from existing M1 and M2 columns |
| C. Future enhancement | Allocation, transfers, emergency distribution, supplier-to-warehouse optimisation, cost and route optimisation | Needs the data list in assessment section 7 |

No unsupported transportation algorithm is in the MVP. Capabilities 1 to 6, tiers, scenario grammar and the R0 stop gate are unchanged.

## 6. Shared definitions (normative for all three workstreams)

### 6.1 Scenario identifiers

`SC-<D>-<V>-<P>-<S>-<K>`, for example `SC-A-ED-R1-BO-K0`.

| Part | Values | Meaning |
| --- | --- | --- |
| D | `A`, `B` | Demand Scenario A (all 17,518 eligible Movement lines) or B (16,655 lines, excluding rule C1 copies) |
| V | `OR`, `ED` | PR PO `original_rows` (11,609) or `exact_distinct_rows` (6,189), used for lead-time proxy and order quantity |
| P | `R0`, `R1`, `R2`, `X1`, `X2`, `X3` | Policy. `R0` deterministic replay of recorded values. `R1`, `R2` are the reference readings of recorded Min/Max (SIMULATION_DESIGN_SPECIFICATION). `X1` to `X3` are proposed parameter sets at service-level scenarios |
| S | `BO`, `LS` | Unmet demand is backordered, or lost. `BO` is the reference |
| K | `K0`, `K1`, ... | Configuration set: opening-stock rule, bootstrap block size, horizon, seed. `K0` is the documented default |

An `X` policy carries a service-level scenario value (for example 90, 95, 98 percent). Those are scenario levels, not targets (D-05).

### 6.2 Terms

| Term | Definition |
| --- | --- |
| Recorded Min/Max | BoM `Min.Qty` and `Max.Qty`, material-level, meaning unconfirmed (DEF-02). Never called "current policy" without that caveat |
| Proposed parameters | Reorder point and order-up-to level produced by the engine under a scenario. A candidate for review |
| Lead-time proxy | Promised interval, from PR date to PO delivery date. Promised, not achieved (DEF-06) |
| Inventory exposure | Stock quantity times a reference unit amount, in IDR, under an explicit price assumption. Not a book value |
| Cash tied up | Needs verified unit price and a dated stock snapshot. **Not computable today** |
| Procurement expenditure | Sum of PO-Item Amount, per currency and per PR PO view. Observed in the dataset, meaning of the amount unconfirmed (DEF-05) |
| Estimated saving | Difference between two policies in cost under approved assumptions. **Not computed. Blocked by D-09** |
| Simulated shortfall | A day in the model where demand exceeds available stock. Never an actual stockout |

### 6.3 Eligibility tiers (OBSERVATION counts, from M2 and the simulation design)

| Tier | Rule | Materials | What the product may show |
| --- | --- | --- | --- |
| T3, policy-simulatable | Stock Item with demand history, promised interval, unit amount and non-zero Min or Max | 665 | Grade A (228, at least 6 active months): all six capabilities with proposed parameters. Grade B (437): R0 replay and configured what-if, **no proposed s, S, Q** (D-24). Lead-proxy resampling on 140, joint on 139 |
| T2, demand-evidenced | Issued in the window, not T3 | 1,265 | Demand class, slow-moving alert, descriptive position against recorded Min/Max. No policy comparison |
| T1, state-only | Never issued in the window | 5,551 | Recorded state, overstock flag against recorded Max, no demand-based output. "No recorded consumption", not "dead stock" |

Sub-tiers inside T3 use the thresholds of 6 active months and 10 distinct lead observations (S-16, pending D-03).

## 7. Decisions requiring approval

**The authoritative register is `DECISION_REGISTER.md` (D-01 to D-25, clarifications C-1 to C-7, classification and state).** The table below is the original list and is kept for history. Where they differ, the register wins.

| ID | Decision | Proposed by | Approver | Blocks |
| --- | --- | --- | --- | --- |
| D-01 | Provide the official Case 3 brief, and confirm R-01 to R-14 against it | Lead | Lead | Every OFFICIAL label |
| D-02 | Reference policy: R1 (Min as reorder point, Max as order-up-to), with R2 as alternative | Lead | Lead | Engine build |
| D-03 | Evidence thresholds, 6 active months and 10 lead observations | Lead | Lead | Tier labels |
| D-04 | Build the engine in stages, stop after deterministic R0 for review | Lead | Lead | R1 and later runs |
| D-05 | Service-level scenario set (default 90, 95, 98 percent) as scenario levels, not targets | Lead | Lead | `X` policies |
| D-06 | Add a demand classification mart (M4) so classes are validated, not computed ad hoc | Lead | Lead | Demand class display |
| D-07 | Whether derived competition data may be bundled into a Vercel deployment and whether any content may go to an external LLM service | Atria | Lead | Deployment, assistant |
| D-08 | Persistence design on Vercel (bundled read-only SQLite, with approvals held elsewhere) | Atria | Lead | Approval workflow |
| D-09 | Cost scenario sets: holding rate, ordering cost, stockout penalty, currency scope | Brilian | Lead | Capability 6, any monetary output |
| D-10 | Meaning of PO-Item Amount, and how to derive a reference unit amount (A-13) | Brilian | Lead | Exposure |
| D-11 | UI rule: no default demand scenario or PR PO view. Show both, or force an explicit choice with a divergence flag | Atria | Lead | UX |
| D-12 | Inventory of AETHER components to reuse | Atria | Lead | Architecture |
| D-14 | Transportation positioning: supply context Level B, all transport optimisation Level C | Lead | Lead | Atria module M-J, narrative |
| D-15 | Logistics data request to the case owner (assessment section 7) | Lead | Lead | Moving any method from C to B |
| D-16 | Checked mart M5 for promised lead-time profile and supplier concentration | Lead | Lead | Showing supply context as validated |
| D-17 | Whether a hypothetical network scenario may appear in the narrative. Recommendation: no | Lead | Lead | None |
| D-13 | Analytical engine is built by the Lead and exposed as files and a contract. Atria consumes it | Lead | Lead | Plan |
| D-18 | Close D-01: accept the official brief file and the audit's status changes | Lead | Lead | OFFICIAL labels |
| D-19 | Add `recommended_action` (REORDER, HOLD, REDUCE, MONITOR) to the contract | Lead | Lead | R-17 |
| D-20 | Deck numbering: brief lists slides 1 to 5 and 7. Six slides in order, or ask organisers | Lead | Lead | Deck |
| D-21 | Allow "potentially obsolete candidate" and "non-moving by recorded issues" wording | Lead | Lead | Capability 3 |
| D-22 | How the deck describes "AI" (statistical forecasting and simulation plus an explanation assistant) | Lead | Lead | Deck slide 3 and 6 |
| D-23 | Add forecast output (R-16) and stock-level what-if scenarios to engine scope | Lead | Lead | R-16, OB-20 |

## 8. Requirements that cannot yet be fulfilled

| Requirement | Why not | What unblocks it |
| --- | --- | --- |
| Full alignment with the official brief | Brief inspected, 29 of 39 rows partial or not covered, nothing built | Audit section 7 |
| Zip, SQLite file, Vercel deployment, screenshot, deck | None exist. Deadline 2026-11-05 06:00 | Atria, Lead |
| Any monetary saving or cost-optimal setting | No holding, ordering, stockout cost; weak unit amount | D-09, D-10 |
| Actual stockout history or service level | No dated stock, no receipts | Snapshot date and receipts |
| Cash tied up in inventory | No verified price, undated stock | D-10 and snapshot date |
| Criticality-weighted service levels | A, B, C, S unranked (DEF-03) | Ranking from case owner |
| Seasonality | 17 months only | Longer history |
| Deployed application | AETHER not inspected, D-07 and D-08 open | Decisions plus Atria inventory |
| Engine outputs | Engine not built | D-02, D-04 |
| Any transportation, allocation, transfer or routing result | No location, receipt, transfer or freight data | D-15 and the data in the assessment |
| Actual (achieved) lead time or supplier reliability | Promised dates only, no receipts | Goods-receipt dates |

## 9. Document map

| Folder | Files |
| --- | --- |
| `docs/strategy` | this file, `OFFICIAL_CASE_ALIGNMENT_AUDIT`, `PROBLEM_STATEMENT`, `ROOT_CAUSE_ANALYSIS`, `SOLUTION_ARCHITECTURE`, `TEAM_RESPONSIBILITY_MATRIX` |
| `docs/analytics` | `TRANSPORTATION_AND_DISTRIBUTION_ASSESSMENT`, `DATA_INTELLIGENCE_SPECIFICATION`, `DEMAND_INTELLIGENCE_METHODOLOGY`, `INVENTORY_OPTIMISATION_METHODOLOGY`, `VALIDATION_FRAMEWORK`, `DATA_LIMITATIONS_AND_ASSUMPTIONS` |
| `docs/handover` | `ATRIA_TECHNICAL_HANDOVER`, `BRILIAN_FINANCIAL_HANDOVER`, `TEAM_INTEGRATION_PROTOCOL` |
| `docs/submission` | `SOLUTION_NARRATIVE`, `PRESENTATION_STRUCTURE`, `SUBMISSION_READINESS_CHECKLIST` |
| `docs/analysis` (existing, unchanged) | Data specification, dictionary, quality, integration and mart reports, assumption registers, simulation design and feasibility |

## 10. Documents that depend on the official Case 3 brief

The brief was inspected on 2026-11-04. The table below lists the dependency. The outcome per document is in `OFFICIAL_CASE_ALIGNMENT_AUDIT.md` section 6. **No document is declared fully aligned**, because most requirements are only planned.

| Document | What depends on the brief |
| --- | --- |
| `strategy/MASTER_SOLUTION_BLUEPRINT.md` | Requirements R-01 to R-15, strategic positioning, the six capability names |
| `strategy/PROBLEM_STATEMENT.md` | Problem framing, scope, success criteria |
| `strategy/ROOT_CAUSE_ANALYSIS.md` | Whether the brief expects other cause categories. The causes themselves rest on the data |
| `strategy/SOLUTION_ARCHITECTURE.md` | Layers and capability map against required deliverables |
| `strategy/TEAM_RESPONSIBILITY_MATRIX.md` | Any deliverable the brief requires that is not listed |
| `analytics/TRANSPORTATION_AND_DISTRIBUTION_ASSESSMENT.md` | Whether the brief requires or defines transportation scope. Positioning is USER-STATED |
| `analytics/DATA_INTELLIGENCE_SPECIFICATION.md` | Brief data definitions, if any, that override assumptions |
| `analytics/DEMAND_INTELLIGENCE_METHODOLOGY.md` | Required methods or evaluation criteria |
| `analytics/INVENTORY_OPTIMISATION_METHODOLOGY.md` | Meaning of Min/Max, required policy, service-level targets (D-02, D-05) |
| `analytics/VALIDATION_FRAMEWORK.md` | Evaluation criteria and accepted evidence |
| `analytics/DATA_LIMITATIONS_AND_ASSUMPTIONS.md` | Questions the brief may already answer |
| `handover/ATRIA_TECHNICAL_HANDOVER.md` | MVP definition, SQLite, Vercel, AI assistant requirements |
| `handover/BRILIAN_FINANCIAL_HANDOVER.md` | Whether cost parameters are provided or scenarios expected |
| `handover/TEAM_INTEGRATION_PROTOCOL.md` | Submission rules and deadlines |
| `submission/SOLUTION_NARRATIVE.md` | Required narrative content and format |
| `submission/PRESENTATION_STRUCTURE.md` | Format, length and scoring weights |
| `submission/SUBMISSION_READINESS_CHECKLIST.md` | Mandatory deliverables and format |

Differences are recorded in the audit as X-01 to X-13.

## 11. Changes caused by the official brief (2026-11-04)

| Topic | Before | After |
| --- | --- | --- |
| Requirement source | Assignment text | Brief for R-01 to R-09, assignment or team for R-10 to R-15 |
| Forecasting | No requirement row | R-16 (OFFICIAL, p4, p5) |
| Recommended action | Review actions only | R-17, REORDER, HOLD, REDUCE, MONITOR |
| Obsolete and dead stock | Never claimed | "Potentially obsolete candidate" allowed as hypothesis (D-21). Unqualified claims still forbidden |
| Deck | 16 slides, own order | Official six content slides plus Appendix |
| Submission | Not itemised | Zip, SQLite, Vercel, screenshot, deadline in checklist |
| Transportation | USER-STATED direction | Still the Lead's direction. Not in the brief. Framed as supply context (brief p5, p7) plus roadmap |

Established analytical results, tiers, scenario grammar and the R0 gate are unchanged.

## 12. Phase 1 execution baseline (normative for Phase 2)

### 12.1 Product scope and proposition

INSpire is Spare Part Intelligence and Inventory Optimization (the brief's title), built as an integrated spare-part supply-chain tool. It helps a planner decide which parts need attention by forecasting where evidence supports it, testing stock rules under identical conditions, recommending an action per part, and stating where records are too thin. Supply context (promised lead time, supplier, currency) is in scope. Transportation, allocation, transfer and routing optimisation are future enhancements (Level C) and are not in the MVP.

### 12.2 MVP outputs, method class and status

Status words: IMPLEMENTED means exists and tested. Everything else here is PROPOSED and not built.

| Output (brief p4) | Method class | Grade and population | Contract field | Status |
| --- | --- | --- | --- | --- |
| Demand classification | Deterministic rules (active months, ADI, CV squared) | 1,930 issued, D0 for 5,551 | `eng_material_tier.csv` | PROPOSED |
| Demand forecast | Statistical: block bootstrap of lead-time demand, Croston-SBA and TSB as baselines | 296 forecast range, 159 rate range, 1,475 abstain | `eng_forecast.csv` | PROPOSED |
| Dynamic Min-Max, safety stock, reorder point, replenishment quantity | Simulation-based parameter search over scenario service levels (a grid, not a mathematical optimiser) | 228 (Grade A) | `eng_proposed_parameters.csv` (`proposed_s`, `proposed_S`, `safety_stock`, `proposed_Q`) | PROPOSED |
| Stockout risk | Simulation. R0 replay is deterministic, Monte Carlo for 228 | 665 replay, 228 stochastic | `eng_scenario_result.csv`, `eng_capability_output.csv` | PROPOSED |
| Overstock risk | Deterministic comparison against recorded Max, plus simulated days above Max | All tiers descriptive, T3 simulated | same | PROPOSED |
| Slow-moving and non-moving alert | Deterministic rules on M2, M3 | T2, T3, T1 | `eng_capability_output.csv` | PROPOSED |
| Potentially obsolete candidate | Deterministic hypothesis rule (D-21) | T1 and T2 | same | PROPOSED |
| Recommended action | Deterministic decision table over the outputs above (below) | All 7,481 | `recommended_action` | PROPOSED (D-25) |
| Cost-risk scenarios | Arithmetic scenario grid on engine output and approved cost sets. No optimiser | Grade A | `fin_scenario_grid.csv` | PROPOSED, blocked by D-09 |
| Supply context | Descriptive statistics from M1 | Materials with supplier rows | `eng_supply_context.csv` | PROPOSED |
| Explanations | Templated text from stored facts. An LLM only if D-07 allows it | All | `eng_explanation_facts.csv` | PROPOSED |

**Provisional `recommended_action` decision table (D-25, thresholds unset and configurable):**

| Order | Condition | Action |
| --- | --- | --- |
| 1 | Grade A, trigger state at or below proposed s, shortfall probability above a threshold | REORDER |
| 2 | Grade A, stock above proposed S, or simulated days above Max above a threshold | REDUCE (candidate) |
| 3 | Grade A, neither | HOLD |
| 4 | Grade B, T2, T1 with slow-moving, non-moving, potentially obsolete or outlier flag | MONITOR |
| 5 | Everything else | NO_ACTION_EVIDENCE |

Every action is a candidate needing human review. No action is derived from a cost saving.

### 12.3 What is AI and what is not (use in the deck, D-22)

| Category | Where it applies |
| --- | --- |
| Statistical forecasting | Demand forecast, lead-time demand (bootstrap, Croston-SBA, TSB) |
| Simulation | Policy comparison, stockout and overstock risk |
| Deterministic business rules | Demand classes, tiers, slow-moving, non-moving, obsolete candidate, recommended action, abstention |
| Optimisation | None in the MVP. Parameter selection is a scenario grid. No transportation optimisation |
| LLM or template generation | Explanations only. Never calculates or recommends |

The deck must not describe rules or simulation as machine learning.

### 12.4 Data sources and limits

Six workbooks, documented as synthetic. Limits (see `DATA_LIMITATIONS_AND_ASSUMPTIONS.md`): Min/Max meaning unknown, stock undated, promised dates only, no costs, criticality unranked, notifications are not failures, plans carry no parts, 17 months. Authoritative figures and population definitions: `analytics/FIGURE_AND_METHOD_RECONCILIATION.md`.

### 12.5 SQLite and Vercel constraints

Specified in `SOLUTION_ARCHITECTURE.md` section 9. Summary: SQLite database inside the app bundle, read-only by default, derived tables only, labelled sample data until D-07 is approved, persistence proven by smoke test (D-08).

### 12.6 Integration contracts

Contract v0.1 plus Addendum A (supply context) and Addendum B (`recommended_action`, `eng_forecast.csv`). Definitions in `handover/ATRIA_TECHNICAL_HANDOVER.md` section 5 and addenda. Change control in `handover/TEAM_INTEGRATION_PROTOCOL.md`.

### 12.7 Ownership and boundaries

`strategy/TEAM_RESPONSIBILITY_MATRIX.md`. Lead owns direction, RCA, data interpretation, methodology, business logic, analytical validation, architecture, shared assumptions and integration decisions. Atria owns application, frontend, backend, SQLite, implementation, testing, deployment. Brilian owns financial analysis, price interpretation, exposure, cost-risk scenarios, financial assumptions. Nobody redefines a shared term, contract column or metric.

### 12.8 Acceptance and submission

Acceptance per workstream: `strategy/PHASE_2_EXECUTION_PLAN.md`. Official submission items: `submission/SUBMISSION_READINESS_CHECKLIST.md` section 1A.

### 12.9 Blockers

| Rank | Blocker | Severity |
| --- | --- | --- |
| 1 | Engine not built, about 12 hours left. No simulated output exists | Critical |
| 2 | D-07 and C-1: permission to publish derived data and zip content | Critical for real-data deploy |
| 3 | Application, SQLite database, Vercel deployment do not exist | Critical |
| 4 | Team names, majors, semesters missing. Deadline time zone and link unknown | High |
| 5 | D-02, C-2: Min/Max meaning unknown | High (credibility of parameters) |
| 6 | D-09, D-10: no cost basis | High for capability 6, none for the rest |
| 7 | D-08: Vercel write persistence unconfirmed | Medium |
| 8 | D-24, D-25, D-23: scope decisions | Medium |
