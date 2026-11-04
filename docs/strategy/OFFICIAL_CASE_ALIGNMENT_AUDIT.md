# INSpire Official Case 3 Alignment Audit

**Status:** DRAFT v0.1 for Lead review. **Date:** 2026-11-04 (about 12 hours before the deadline, see OB-26).
**Official source:** `docs/case/CALIBER 2026 - Final Case Brief.pdf`, 10 pages, all pages read as extracted text (pypdf). Page 1 is a cover, page 10 is "Good Luck!". Pages 2 to 9 carry all content. Layout, icons and any image-only content were not inspected visually, so a visual check by the Lead is advised.
**Companion source:** `docs/case/Data Context & Relationship Diagram.pdf` (2 pages). Documents the six files, joins and grain. Labelled synthetic (dummy). Not part of the brief, but part of the case pack.
**Not official:** `docs/case/CALIBER_2026_Case_3_Complete_Final_Case.md` (Case 2 content under a Case 3 name, C-01) and `CALIBER_2026_Master_Reference_Case_2.md`. Neither was used for any requirement.

**Labels.** OFFICIAL = stated in the brief (page given). TEAM = our assumption or addition. FINDING = measured or concluded in our analysis. PROPOSED = specified, not built. IMPLEMENTED = exists and passed checks. Today IMPLEMENTED means only marts M1 to M3 and simulation design evidence. **No application, engine or deck exists yet**, so no capability is "covered" in an implementation sense. "Covered" below means the plan addresses the requirement, and the Implementation column says whether anything exists.

**Rule on mandatory status.** The brief gives no scoring weights and no slide limit. Words "must" and "required" appear only on p5 (key questions), p8 (submission) and p9 (deck format). Everything else is "expected" or "should consider". This audit uses only those words.

## 1. Summary of the official brief

| Topic | What the brief says | Page |
| --- | --- | --- |
| Title | Spare Part Intelligence & Inventory Optimization, AI-Powered Forecasting & Dynamic Optimization | 1, 2 |
| Objective | AI-powered solution to improve forecasting, enable dynamic inventory decisions, reduce excess inventory and working capital, maintain critical spare part availability | 2 |
| Trigger, cause, dilemma | Right items unavailable at shutdown while slow-moving items sit on shelf. Planning is reactive. Cost versus risk trade-off | 2 |
| Problem | No integrated, predictable approach to forecasting demand and setting inventory levels. Static planning (historical consumption, static Min-Max). Suboptimal balancing (criticality and lead time not consistently considered) | 3 |
| Impact | Emergency procurement, higher purchasing and carrying costs, excess working capital, prolonged downtime and production losses | 3 |
| Expected solution | Four capabilities: Demand Forecasting, Dynamic Inventory Optimization, Inventory Health Monitoring, AI Recommendation and Cost-Risk Optimization. Must move beyond forecasting to six named outputs | 4 |
| Key questions | Two, to be answered in the deck | 5, 6 |
| Data | Six workbooks, mapped to six data sources. Extra data allowed with clear business justification. Quality architecture preferred over more data | 7 |
| Submission | Prototype (MVP, not static HTML, on Vercel, SQLite, zip of source and database, screenshot with timestamp) and a deck. Deadline Thursday 5 November 2026, 06.00. English. Strict compliance | 8 |
| Deck | Cover, Background and Problem, Solution, Business Impact, Roadmap and Risk, Team Profile, optional Appendix | 9 |

**What the brief does not contain:** any mention of transportation, logistics, warehouses, routing, supplier location or freight (full text searched). No scoring weights. No slide limit. No service-level target. No definition of Min-Max. No cost parameters. No mention of an AI assistant or human approval workflow.

## 2. Requirements traceability matrix

Coverage: **Full** = plan addresses it completely with no data conflict. **Partial** = addressed with a gap, a wording conflict or a limit. **None** = not in the plan. **Unclear** = depends on a fact not available. Implementation: **None** unless stated.

### 2.1 Context and framing

| ID | Requirement (faithful summary) | Page | Status | INSpire document | Coverage | Evidence | Correction or action | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OB-01 | Objective: improve forecasting, enable dynamic inventory decisions, reduce excess inventory and working capital, keep critical parts available | 2 | Stated (objective) | `PROBLEM_STATEMENT.md`, blueprint section 5 | Partial | Plan addresses all four verbs. "Reduce working capital" cannot be measured: no price, undated stock, cash tied up not computable | State the objective in the brief's words. Say working capital is shown as exposure under assumptions, never as realised reduction | Lead |
| OB-02 | Trigger, cause, dilemma (shutdown stockout versus idle slow movers, reactive planning, cost versus risk) | 2 | Context | `PROBLEM_STATEMENT.md`, `ROOT_CAUSE_ANALYSIS.md` | Partial | Root causes come from the data (RC1 to RC7). The brief's "shutdown" trigger has no shutdown calendar behind it (A-08 is a hypothesis) | Quote the brief's trigger on the problem slide as the case owner's framing, then show what the dataset can and cannot show about it | Lead |
| OB-03 | Problem: no integrated, predictable approach to demand forecasting and inventory level setting | 3 | Context | `PROBLEM_STATEMENT.md` | Full | Core problem statement matches in substance | Use the brief's sentence verbatim in the deck | Lead |
| OB-04 | Why: static planning (historical consumption, static Min-Max) | 3 | Context | `ROOT_CAUSE_ANALYSIS.md` RC1 | Partial | RC1 shows recorded Min/Max sit away from consumption. "Static" is not provable: Min/Max has no history, one snapshot | Say "recorded Min/Max is a single undated snapshot", do not assert it is static over time | Lead |
| OB-05 | Why: criticality and lead time not consistently considered | 3 | Context | RC for criticality, lead proxy | Partial | Criticality is unranked in data (DEF-03). Lead time is promised only (DEF-06) | Keep as stated. Note both as data limits | Lead |
| OB-06 | Impact: emergency procurement, higher costs, excess capital, downtime | 3 | Context | `PROBLEM_STATEMENT.md` section 3 | Partial | Dataset holds no downtime, loss, or cost. Only 135 Emergency notifications (type N2) exist, and they are not procurement | Present as the case owner's stated impact. Do not quantify from this data | Lead |

### 2.2 Expected solution and capabilities (p4)

| ID | Requirement | Page | Status | INSpire document | Coverage | Evidence | Correction or action | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OB-07 | Capability 1, Demand Forecasting: predict future requirements from consumption, failures, maintenance activities, operating conditions | 4 | Expected capability | `DEMAND_INTELLIGENCE_METHODOLOGY.md` | **Partial** | Method abstains for 1,475 of 1,930 issued materials (D1), gives a rate range for 159 (D2) and forecasts "demand during lead time" for 296 (D3, D4). No forward forecast shown for most. Failures, maintenance and operating conditions are context only (DEF-09, DEF-10, DEF-11). Blueprint has **no requirement row for forecasting itself** | Add requirement R-16 (Demand Forecasting) with a visible forward-demand output: lead-time demand distribution or range for D2 to D4, abstention reason for the rest. Name it "forecast" in the product | Lead |
| OB-08 | Capability 2, Dynamic Inventory Optimization: recommend Min-Max, Safety Stock, Reorder Points, replenishment quantities, based on changing demand and lead times | 4 | Expected capability | `INVENTORY_OPTIMISATION_METHODOLOGY.md`, contract `eng_proposed_parameters.csv` | Partial | Contract has `proposed_s`, `proposed_S`, `proposed_Q`, `safety_stock`, recorded min/max. Covers 665 materials only (T3). "Dynamic" is a replay of re-estimation, not proven (17 months) | Map names explicitly: Min = proposed s, Max = proposed S, as candidates. State that 6,816 materials get no parameters and why | Lead |
| OB-09 | Capability 3, Inventory Health Monitoring: detect excess, slow-moving, non-moving, potentially obsolete parts | 4 | Expected capability | `INVENTORY_OPTIMISATION_METHODOLOGY.md` section 5 | **Partial, wording conflict** | Slow-moving and "no recorded consumption" defined. **Obsolete is "never claimed"**, and "dead stock" is avoided. The brief asks for "potentially obsolete" and (p6) "dead stock" | Add a "potentially obsolete candidate" flag as a labelled HYPOTHESIS (stock above zero, no issue in window, no plan link). Allow "non-moving by recorded issues". Keep "obsolete" and "dead stock" as claims forbidden. See section 4, X-02 | Lead |
| OB-10 | Capability 4, AI Recommendation and Cost-Risk Optimization: recommend which parts to **reorder, maintain, reduce or monitor**, balancing inventory cost against stockout, downtime, production-loss risk | 4 | Expected capability | Contract `eng_capability_output.csv`, `BRILIAN_FINANCIAL_HANDOVER.md` | **Partial** | Contract has six capability flags and review actions (approve, reject, defer). It has **no recommended-action field** with the four brief actions. Downtime and production-loss cost are not in the data, Brilian lists "stockout or downtime penalty" as a missing input | Add `recommended_action` (REORDER, HOLD, REDUCE, MONITOR) as an additive contract field (PROPOSED, D-19). "Maintain" is read as hold current level (TEAM reading, confirm). Cost-risk stays scenario only | Lead, Atria |
| OB-11 | Move beyond forecasting to actionable outputs: Stockout Risk | 4 | Expected output | R-04 | Partial | Simulated shortfall probability for T3 only. Never a historical stockout | OFFICIAL status now confirmed for the name. Keep simulated wording | Lead |
| OB-12 | Overstock Risk | 4 | Expected output | R-05 | Partial | Simulated for T3, descriptive for others | Same | Lead |
| OB-13 | Reorder Recommendation | 4 | Expected output | R-06 | Partial | T3 candidates only, needs approval | Same | Lead |
| OB-14 | Slow-Moving Alert | 4 | Expected output | R-07 | Full (plan) | Rule on M2 and M3 for T2, T3, and T1 labelled | None beyond OB-09 wording | Lead |
| OB-15 | Dynamic Inventory Parameters | 4 | Expected output | R-08 | Partial | Same as OB-08 | Same | Lead |
| OB-16 | Cost-Risk Optimization Scenarios | 4 | Expected output | R-09 | Partial, blocked | No cost data, D-09 open | Scenario comparison with labelled inputs. No saving | Brilian |

### 2.3 Key questions (p5, p6)

| ID | Requirement | Page | Status | INSpire document | Coverage | Evidence | Correction or action | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OB-17 | Deck **must** address Key Question 1: improve demand predictability for irregular, uncertain consumption, inside Proposed Solution or Business Impact | 5 | **Mandatory** ("must") | `DEMAND_INTELLIGENCE_METHODOLOGY.md` | Partial | Content exists (classes, abstention, bootstrap). **No slide in `PRESENTATION_STRUCTURE.md` is designated to answer it by name** | Add an explicit "Key Question 1" block to the Solution slide, using the brief's wording | Lead |
| OB-18 | Key Question 1 "should consider": consumption patterns, failure frequency, planned maintenance, preventive schedules, shutdowns and turnarounds, installed population, seasonal and operating conditions, abnormal consumption, procurement lead time and supply variability | 5 | Optional ("should consider") | Demand methodology section 2 | Partial | Addressed: consumption, abnormal (flagged), installed qty in M2, lead time and variability (promised). Limited: failures (notifications only), PM (no spare-part link), shutdown (no calendar), seasonality (17 months, abstain) | Show a one-row-per-factor table in the deck: used, context only, or not supported, with reason | Lead |
| OB-19 | Deck **must** address Key Question 2: dynamically optimise inventory balancing cost, availability, operational risk | 6 | **Mandatory** ("must") | `INVENTORY_OPTIMISATION_METHODOLOGY.md` | Partial | Same gap as OB-17 | Explicit "Key Question 2" block on Solution or Business Impact slide | Lead |
| OB-20 | Key Question 2 "should consider": stockout risk, overstock, reorder when, reorder quantity and dynamic Min-Max, slow or dead stock, carrying and holding cost, procurement cost and lead time, criticality, downtime and production loss, cost-versus-risk trade-off, **scenario simulation of increasing or reducing inventory levels** | 6 | Optional ("should consider") | Inventory methodology | Partial | Covered by capabilities 1 to 6 and policy simulation. Holding cost, downtime and production loss: no data. **"Increase or reduce inventory levels" what-if is not an explicit scenario**: policies X1 to X3 vary service level, not a stock-level multiplier | Add an explicit stock-level what-if (recorded Min/Max scaled by configurable factors) to the scenario set. Data gaps stated | Lead |

### 2.4 Data (p7)

| ID | Requirement | Page | Status | INSpire document | Coverage | Evidence | Correction or action | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OB-21 | Use baseline data: six files mapped to six sources (BoM for master and inventory, Movement for consumption, Notif and FuncLoc for criticality and failures, PR PO for procurement, Mitem and Mplan for plans) | 7 | Expected | Data specification, M1 to M3 | Full (IMPLEMENTED data foundation) | All six staged, 750 of 750 checks, marts M1 to M3 accepted | None | Lead |
| OB-22 | Brief says Mitem and Mplan give "visibility of known future spare part demand" | 7 | Brief statement | Demand methodology | **Contradiction** | The case pack's own diagram says Mitem and Mplan "do not include the spare parts required to perform the PM work". Our data check agrees | Do not forecast demand from plans. Say so on the slide, citing the Data Context diagram. See X-04 | Lead |
| OB-23 | Additional data sources may be proposed, each with clear business justification. High-quality data architecture preferred over simply integrating more data | 7 | Optional | Transportation assessment section 7, blueprint section 5A | Full (as framed) | Level C data list is each justified by a named method. No extra source is integrated | Keep additional sources to the justified list. Do not add any source to the MVP | Lead |

### 2.5 Submission (p8)

| ID | Requirement | Page | Status | INSpire document | Coverage | Evidence | Correction or action | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OB-24 | Must submit two materials: prototype and deck, to be eligible for the final presentation | 8 | **Mandatory** | Checklist | Not implemented | Neither exists | Track as the two critical-path items | Lead |
| OB-25 | Prototype: MVP, **not static HTML**, published to Vercel | 8 | **Mandatory** | `ATRIA_TECHNICAL_HANDOVER.md`, R-01, R-03 | Partial (plan) | Plan exists. AETHER not inspected. Nothing deployed. D-07, D-08 open | Elevate R-01 and R-03 to OFFICIAL. A bundled read-only page with sample data must still be a functional app, not static HTML | Atria |
| OB-26 | Deadline: Thursday 5 November 2026, 06.00 AM | 8 | **Mandatory** | Checklist | **Critical** | Now is 2026-11-04 evening. About 12 hours remain. Time zone is not stated in the brief | Freeze scope. Use the minimum viable submission (checklist section 5). Confirm time zone and submission link | Lead |
| OB-27 | Database using SQLite | 8 | **Mandatory** | R-02, Atria handover | Partial (plan) | Schema specified, not built | Elevate R-02 to OFFICIAL | Atria |
| OB-28 | Complete source code and database in a .zip | 8 | **Mandatory** | Checklist | **None** | No checklist item names the zip, and the project rule not to bundle competition data (C-07, D-07) conflicts with shipping the database | New checklist items. Lead decides D-07 against this official requirement (X-05). Confirm data may be bundled given it is documented as dummy | Lead, Atria |
| OB-29 | Screenshot (.png, .jpg, .jpeg) with timestamp of the latest deployed Vercel version | 8 | **Mandatory** | Checklist | **None** | Not listed anywhere | New checklist item. Take after final deploy | Atria |
| OB-30 | All materials in English. Proposal must strictly follow guidelines. Non-compliance directly affects evaluation | 8 | **Mandatory** | Checklist | Partial | Docs are in English. Deck format not yet followed (OB-31) | Add compliance gate to checklist | Lead |

### 2.6 Deck format (p9)

| ID | Requirement | Page | Status | INSpire document | Coverage | Evidence | Correction or action | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OB-31 | Deck follows the stated slide list. Page title says "Presentation Deck Format", content column "Slide Required Content" | 9 | **Mandatory** (strict compliance, p8) | `PRESENTATION_STRUCTURE.md` | **Not covered** | The plan has 16 slides in our own order. It does not follow the official list | Rewrite to the official six content slides plus Appendix. Move our extra material to the Appendix or into the required slides | Lead |
| OB-32 | Slide 1 Cover: team name and member names | 9 | Mandatory | Presentation structure slide 1 | Partial | Our slide 1 is a title and data label. Team name and members not recorded anywhere | Add team name and member names. Input needed from the Lead | Lead |
| OB-33 | Slide 2 Background and Problem Statement: current challenges, supporting facts, why important | 9 | Mandatory | Problem Statement, RCA | Full (plan) | Content exists | Fit within one slide | Lead |
| OB-34 | Slide 3 Solution: proposed solution, key technologies and features that make it unique | 9 | Mandatory | Architecture, narrative | Partial | Technologies not listed as a set. "AI" is not described (see X-06) | Add a technology and uniqueness block and the two key-question answers | Lead |
| OB-35 | Slide 4 Business Impact: success metrics (how measured) and expected benefits | 9 | Mandatory | Problem Statement success criteria | **Partial** | Existing criteria are product-quality rules. **No success-metric definition for the business**, and benefits cannot be quantified from the data | Add a KPI definition table (what, how measured, baseline status, target left to the case owner) and qualitative expected benefits. No numbers invented. Done in `PROBLEM_STATEMENT.md` section 6 | Lead, Brilian |
| OB-36 | Slide 5 Roadmap and Risk: high-level timeline with activities, outputs and **stakeholders** per phase. Key risks and mitigations | 9 | Mandatory | Transportation assessment section 8 (data roadmap only), architecture risks | **Partial** | The existing roadmap F0 to F5 is a data-enablement roadmap for logistics, not a delivery timeline with stakeholders. Risks exist | Add a delivery roadmap (phase, activity, output, stakeholder) in `PRESENTATION_STRUCTURE.md`. Keep F0 to F5 as one phase of it | Lead |
| OB-37 | Slide 7 Team Profile and Key Technologies: table (No, Name, Major, Semester, Area of expertise, Contribution), plus AI models and tools used | 9 | Mandatory | None | **None** | No team table. No list of AI models or tools. Atria, Brilian and Lead roles exist, but not major or semester | Lead supplies names, majors, semesters. Tools list drafted in the presentation structure from facts in this repository only | Lead |
| OB-38 | Appendix optional: supporting references | 9 | Optional | n/a | Full | Our extra slides fit here | Move evidence tiers, methodology detail, validation, financial detail, limitations and transportation assessment here | Lead |
| OB-39 | Slide numbering lists 1, 2, 3, 4, 5, 7 with **no slide 6** | 9 | Brief ambiguity | n/a | Unclear | Either a numbering slip or a missing row | Decision D-20: follow content order as six slides, flagged, or ask the organisers | Lead |

## 3. Coverage summary

Counts are of OB-01 to OB-39 (39 rows). A row is counted once, by its coverage word.

| Coverage | Rows |
| --- | --- |
| Full (plan or implemented data) | OB-03, OB-14, OB-21, OB-23, OB-33, OB-38 (6) |
| Partial | OB-01, OB-02, OB-04, OB-05, OB-06, OB-07, OB-08, OB-09, OB-10, OB-11, OB-12, OB-13, OB-15, OB-16, OB-17, OB-18, OB-19, OB-20, OB-25, OB-27, OB-30, OB-32, OB-34, OB-35, OB-36 (25) |
| Not covered | OB-28, OB-29, OB-31, OB-37 (4) |
| Unclear | OB-39, OB-26 (critical, time) (2) |
| Contradiction between brief and data | OB-22 (1) |
| Not implemented (all) | OB-24 |

**No requirement has implementation evidence except OB-21 (data foundation).** All other "Full" and "Partial" ratings describe the plan only.

## 4. Gaps, contradictions and claims beyond the data

| ID | Finding | Type | Resolution |
| --- | --- | --- | --- |
| X-01 | **The brief asks for forecasting as capability 1. The blueprint has no forecast requirement, only the six outputs.** Our method forecasts for 296 of 1,930 issued materials and abstains elsewhere | Gap | R-16 added. Say honestly: forecast where evidence supports, abstain where not. Abstention answers Key Question 1 (OB-17) but must be shown as an answer, not an omission |
| X-02 | **Wording conflict on obsolete and dead stock.** Brief: "potentially obsolete" (p4), "dead stock" (p6). Our methodology: never claimed, avoided | Contradiction | Allow "potentially obsolete candidate" (labelled hypothesis) and "non-moving by recorded issues". Keep "obsolete" and "dead stock" as unqualified claims forbidden. Needs Lead approval (D-21) |
| X-03 | **Four action verbs (reorder, maintain, reduce, monitor) are not in the contract** | Gap | `recommended_action` PROPOSED (D-19) |
| X-04 | **Brief says Mitem and Mplan show known future spare part demand. The case pack diagram and our data say they hold no spare parts** | Brief versus data contradiction | Cite the diagram. Do not forecast from plans. Raise with organisers if possible |
| X-05 | **Official requirement to ship the database in a zip and deploy to Vercel conflicts with our project rule against uploading competition data externally (C-07, D-07)** | Conflict between official requirement and team rule | The official requirement is mandatory for eligibility. The data is documented as synthetic. Lead must decide D-07 now. Fallback: ship derived tables only, which is still a SQLite database |
| X-06 | **"AI-powered" and "AI models and tools used" (p2, p9). Our methods are statistical (bootstrap, Croston-SBA, TSB, simulation) plus an LLM assistant** | Positioning risk | Describe honestly: statistical forecasting and simulation, plus an explanation assistant. Do not call simple rules "machine learning". Lead decides how to present (D-22) |
| X-07 | **Transportation is not in the brief.** Our integrated positioning is a TEAM choice | Positioning | See section 5 |
| X-08 | **The deck plan does not follow the official format (16 slides versus six content slides)** | Gap, mandatory | `PRESENTATION_STRUCTURE.md` rewritten |
| X-09 | **No checklist item for zip, screenshot, SQLite file in the zip, or deadline** | Gap, mandatory | Checklist updated |
| X-10 | **Scenario "increase or reduce inventory levels" not explicit** | Gap | Add stock-level multiplier scenarios (OB-20) |
| X-11 | The blueprint called R-01 to R-03 and the six capability names USER-STATED | Status change | Now OFFICIAL (p4, p8). R-10 (assistant), R-11 (human review), R-12 to R-15 stay TEAM |
| X-12 | The blueprint says no business impact is measurable. The brief requires success metrics and benefits on slide 4 | Tension, not contradiction | Define metrics without values or claims (OB-35) |
| X-13 | Claims in the blueprint that exceed what the data can validate | Check | See below |

**Claims that exceed what the supplied data can validate (and how they are already handled).**

| Claim area | Why the data cannot validate it | Current handling |
| --- | --- | --- |
| Dynamic Min-Max "based on changing demand" | One undated stock snapshot, 17 months, no history of Min/Max | Replay only, never proven benefit |
| Working capital reduction | No verified price, undated stock | Exposure under assumption only |
| Failure probability and downtime exposure (p7 item 4) | Notifications are not failures (DEF-09), no downtime field, criticality unranked | Context only. Do not present a failure model |
| Known future demand from plans (p7 item 6) | Plans carry no parts | Not used |
| Emergency procurement impact (p2, p3) | Emergency notifications exist, emergency purchases do not | Not quantified |
| Shutdown driven demand | No shutdown calendar | Event-month hypothesis only |
| Transportation problems | No location or freight data | Hypotheses, Level B and C |

## 5. Strategic positioning review

- **Direction confirmed by the Lead:** Integrated Spare Part Supply Chain Intelligence. Transportation stays in the overall strategy.
- **What the brief says:** the case is Spare Part Intelligence and Inventory Optimization. Supply appears only as "procurement lead time and supply variability" (p5), "replenishment lead time" and "procurement cost" (p6), and PR PO as "lead time, cost, and supply reliability" (p7).
- **Alignment.** The Level B supply context panel is justified by those official phrases, not by transportation. It should be described that way. The word "transportation" does not appear in the brief, so the deck must not suggest the jury asked for it.
- **Brief caution (p7):** "A well-justified and high-quality data architecture is preferred over simply integrating more data." This supports the existing evidence-based decision to keep transportation optimisation out of the MVP (Level C) and to add no source without justification.
- **Wording rule.** Lead with the brief's title in the deck. Use "integrated supply-chain" as the umbrella that explains why supply context and the logistics roadmap exist. Give transportation at most one roadmap row and one appendix slide, so that the jury's attention stays on the four official capabilities and the two key questions.
- **Unchanged:** Level A none, Level B supply context, Level C all optimisation. No unsupported transportation optimisation enters the MVP.

## 6. Documents depending on the brief, after inspection

| Document | Result of the inspection | Action taken |
| --- | --- | --- |
| `MASTER_SOLUTION_BLUEPRINT.md` | R-01 to R-03, R-04 to R-09 now OFFICIAL by name. Forecasting missing. Alignment statement outdated | Updated (section 1, 2, 4, 7, 8, 10, new section 11) |
| `PROBLEM_STATEMENT.md` | Success criteria were product rules, no business metrics | Section 6 added |
| `ROOT_CAUSE_ANALYSIS.md` | Brief gives its own cause list (reactive planning, static Min-Max, criticality and lead time ignored). Our causes come from the data and are compatible | No change needed. Mapping recorded in this audit (OB-02 to OB-06) |
| `SOLUTION_ARCHITECTURE.md` | Risk row on jury expectation reworded | Updated |
| `TEAM_RESPONSIBILITY_MATRIX.md` | Missing deliverables: deck, team table, zip, screenshot | Updated |
| `TRANSPORTATION_AND_DISTRIBUTION_ASSESSMENT.md` | Brief does not define transportation scope, which confirms positioning is TEAM | Header note |
| `DEMAND_INTELLIGENCE_METHODOLOGY.md` | Needs forecast output | Flagged here (R-16), not edited, because methods are unchanged |
| `INVENTORY_OPTIMISATION_METHODOLOGY.md` | Obsolete wording conflict | Section 5 note added |
| `VALIDATION_FRAMEWORK.md`, `DATA_INTELLIGENCE_SPECIFICATION.md`, `DATA_LIMITATIONS_AND_ASSUMPTIONS.md` | The brief supplies no evaluation weights and no definitions that override assumptions | No change |
| `ATRIA_TECHNICAL_HANDOVER.md`, `BRILIAN_FINANCIAL_HANDOVER.md`, `TEAM_INTEGRATION_PROTOCOL.md` | `recommended_action` proposed. Brilian: downtime and production-loss cost inputs named by the brief | Short addenda (PROPOSED) |
| `SOLUTION_NARRATIVE.md` | Story must lead with the brief's title. Key-question answers needed | Updated |
| `PRESENTATION_STRUCTURE.md` | Did not follow the official format | Rewritten |
| `SUBMISSION_READINESS_CHECKLIST.md` | Zip, screenshot, deadline, deck compliance missing | Updated |

## 7. Unresolved requirements (all)

| Item | Why open | Owner |
| --- | --- | --- |
| OB-07 forecast output | Needs R-16 approved and built | Lead |
| OB-09 potentially obsolete flag | D-21 | Lead |
| OB-10 recommended action field | D-19 | Lead, Atria |
| OB-16 cost-risk scenarios | D-09, D-10 | Brilian |
| OB-17, OB-19 key-question answers in deck | Deck not built | Lead |
| OB-20 stock-level what-if | Needs engine configuration | Lead |
| OB-24 to OB-30 prototype, database, zip, screenshot | Nothing built or deployed. D-07, D-08 | Atria, Lead |
| OB-31 to OB-37 deck | Not built. Team names, majors, semesters missing | Lead |
| OB-39 missing slide 6 | D-20 | Lead |
| OB-26 deadline | About 12 hours | Lead |

## 8. New decisions

| ID | Decision | Recommendation |
| --- | --- | --- |
| D-18 | Close D-01: accept `CALIBER 2026 - Final Case Brief.pdf` as the official brief, and accept the status changes in this audit | Accept |
| D-19 | Add `recommended_action` (REORDER, HOLD, REDUCE, MONITOR) to the contract | Accept, additive |
| D-20 | Deck numbering: six content slides in order, or ask organisers about the missing slide 6 | Six slides in order, and a note |
| D-21 | Allow "potentially obsolete candidate" and "non-moving by recorded issues" wording | Accept, hypothesis label |
| D-22 | How the deck describes "AI" | Statistical forecasting and simulation plus an explanation assistant, no overstatement |
| D-23 | Add stock-level what-if scenarios and a forecast output (R-16) to the engine scope | Accept if time permits, else show as designed |
| D-07 (restated) | Bundling the database is now an official requirement | Decide immediately |

## 8A. Phase 1 verification note (2026-11-04)

The audit was checked against the PDF again. The requirement rows and page references hold. Two omissions were found and are now recorded in `DECISION_REGISTER.md` section 4: the 228 versus 665 parameter-eligibility contradiction (D-24) and the name collision between demand classes D1 to D4 and the `demand_evidence_tier` labels. Decision classes and states for D-18 to D-23 are in the register, which supersedes section 8 above.

## 9. Change history

| Date | Change |
| --- | --- |
| 2026-11-04 | First audit against the official brief. Documents in section 6 updated. No data, mart or source change |
