# INSpire Presentation Structure

**Status:** DRAFT v0.2 (2026-11-04). **Rewritten to the official deck format** (`CALIBER 2026 - Final Case Brief.pdf`, p9). The brief says the proposal "must strictly follow the guidelines" and non-compliance "will directly affect the evaluation outcome" (p8). The brief gives no slide limit and no scoring weights. No slide is built. The earlier 16-slide plan is kept below as the Appendix plan (history preserved).

## A. Official structure (OFFICIAL, p9)

The brief lists slides 1, 2, 3, 4, 5 and 7. Slide 6 is absent (D-20). This plan uses six content slides in the order given, then the optional Appendix. Label the last content slide "Team Profile and Key Technologies".

| Slide | Official required content | INSpire content (TEAM) | Owner | Source | Ready? |
| --- | --- | --- | --- | --- | --- |
| 1 Cover | Team name and team members' names | Product INSpire, team name and members. Data label line | Lead | **Team name and member names not in the repository** | Needs input |
| 2 Background and Problem Statement | Current challenges, supporting facts, why important | Brief's problem sentence (p3), trigger and dilemma (p2), then four observations from the data (undated stock, sparse demand, 20.5 percent order link, promised dates only). Root causes RC1 to RC7 as supporting facts | Lead | `PROBLEM_STATEMENT.md`, `ROOT_CAUSE_ANALYSIS.md` | Yes |
| 3 Solution | Proposed solutions, key technologies and features that make it unique | Four official capabilities (forecasting, dynamic optimisation, health monitoring, AI recommendation and cost-risk) mapped to six outputs. Evidence tiers and abstention as the unique feature. Integrated supply context (promised lead time and supplier). **Key Question 1 and Key Question 2 answered here**, in the brief's wording, one block each (p5, p6) | Lead | Architecture, methodology documents | Needs engine results to show numbers |
| 4 Business Impact | Success metrics (how measured), expected benefits | Metric definitions and qualitative benefits from `PROBLEM_STATEMENT.md` section 6. No savings, no percentages. Cost-risk scenario shown only with an approved cost set | Lead, Brilian | Problem statement section 6, financial handover | Yes for definitions |
| 5 Roadmap and Risk Management | High-level timeline with activities, outputs and stakeholders per phase. Key risks and mitigations | See roadmap table below. Risks from `SOLUTION_ARCHITECTURE.md` section 7 and blueprint section 8 | Lead | This file, architecture | Yes |
| 6 (brief slide 7) Team Profile and Key Technologies | Table: No, Name, Major, Semester, Area of expertise, Contribution. AI models and tools used | Roles Lead, Atria, Brilian. **Major, semester, names not in the repository.** Tools list below | Lead | Lead input | Needs input |
| Appendix (optional) | Supporting references | Slides in section C | Lead | | Yes |

**Slide 3 must contain the two key-question blocks** (brief p5 and p6 say participants "must address" them in the Proposed Solution or Business Impact section). Draft wording:

- **Key Question 1, demand predictability:** classify every issued part by demand pattern, forecast lead-time demand where evidence supports it (296 materials), give a rate range where it is thin (159), and abstain with a stated reason where it is sparse (1,475). Show the factor table (used, context only, not supported) for the brief's "should consider" list.
- **Key Question 2, dynamic optimisation:** replay recorded and proposed Min-Max candidates under identical conditions, in two demand views and two procurement views, with stock-level what-if scenarios. Show cost-risk comparison as scenarios.

## B. Roadmap content for slide 5 (PROPOSED, labelled)

| Phase | Activities | Outputs | Stakeholders (roles, not named people) |
| --- | --- | --- | --- |
| 0. Data foundation (done) | Stage six workbooks, validate marts M1 to M3 | Validated marts, data specification | Data owner |
| 1. Hackathon MVP | Engine R0 and R1, application, SQLite, Vercel deployment | Working prototype, deck | Team, jury |
| 2. Validate with the case owner | Confirm Min/Max meaning, stock date, receipts, cost parameters. Approve cost sets | Definitions, validated parameters | Planners, procurement, finance, maintenance |
| 3. Pilot | Run on live data, human review loop, measure the success metrics | Measured baselines and targets | Planners, procurement, reliability |
| 4. Supply-chain extension | Logistics data F1 to F5 from the transportation assessment, only as data arrives | Actual lead time, location-aware allocation, transfer and cost models | Logistics, warehouse, procurement, finance |

## C. Appendix plan (the earlier 16-slide plan, kept)

| # | Slide | Content | Owner | Source | Ready? |
| --- | --- | --- | --- | --- | --- |
| 1 | Title and data label | INSpire, Case 3, "synthetic data" line | Lead | n/a | Yes |
| 2 | Problem | Planner's decision problem, six questions | Lead | `PROBLEM_STATEMENT.md` | Yes |
| 3 | What the data shows | Dataset scale, four headline observations | Lead | Discovery report, M2, M3 | Yes |
| 4 | Root causes | RC1 to RC7 with evidence and status | Lead | `ROOT_CAUSE_ANALYSIS.md` | Yes |
| 5 | Why a careful answer is hard | Sparse demand chart, undated stock, copies | Lead | M3, quality report | Needs chart |
| 6 | Solution overview | Integrated supply-chain intelligence: six layers as one workflow, supply context shown | Lead | `SOLUTION_ARCHITECTURE.md` | Yes |
| 7 | Evidence tiers | 665, 1,265, 5,551, what each tier allows | Lead | Blueprint section 6.3 | Yes |
| 8 | Methodology | Demand classes, abstention, simulation of policies | Lead | Methodology documents | Yes |
| 9 | Demo: capabilities 1 to 5 | Live walk-through on one T3 material and one abstention | Atria | Application | Needs build |
| 10 | Demo: AI assistant | Explain a recommendation from stored facts | Atria | Application | Needs build |
| 11 | Demo: cost-risk scenarios | Approved cost set, exposure and shortfall | Brilian, Atria | Financial grid | Needs D-09 |
| 12 | Human approval | Review queue, evidence, log | Atria | Application | Needs build |
| 13 | Validation and honesty | Verification versus validation, sensitivity, rank stability | Lead | `VALIDATION_FRAMEWORK.md`, engine results | Needs engine |
| 14 | Financial view | Exposure ranges, expenditure, scenario cost differences, labelled | Brilian | Financial handover | Needs inputs |
| 15 | Limitations and future roadmap | What the case owner can confirm, what it unlocks. Transportation assessment: what the data cannot support, the data needed, phases F1 to F5 | Lead | `DATA_LIMITATIONS_AND_ASSUMPTIONS.md`, transportation assessment section 8 | Yes |
| 16 | Close | One sentence story, ask | Lead | Narrative | Yes |

Transportation appears only in Appendix slide 15 and in roadmap phase 4. Optional supply context panel (M-J) on a demo screen, only if D-14 is approved and built. Never a route map or transport result. The live demo is not a required deck element (the brief requires a prototype and a deck separately, p8).

## D. Technologies and tools for the team slide (facts in this repository only)

| Item | Use | Status |
| --- | --- | --- |
| Python, pandas, pytest | Data pipeline and validated marts | IMPLEMENTED |
| Bootstrap resampling, Croston-SBA, TSB | Forecast and simulation methods | IMPLEMENTED. Croston-SBA selected for point forecasts. Bootstrap quantile failed its pre-registered test (D-26), so say so |
| SQLite, web front end, Vercel | Prototype | PROPOSED, not built |
| LLM assistant | Explains stored results only | PROPOSED. Model and provider not chosen (D-07, D-22) |
| Claude Code | Used by the Lead for analysis and documentation | Fact, this project. Confirm wording with the Lead |

Add only tools that were actually used. Do not name a forecasting model that was not built.

## Rules for every slide

- Data label in the footer.
- Scenario ID on any engine number.
- No claim from the "must not make" list in `SOLUTION_NARRATIVE.md`.
- A slide is dropped, not faked, if its source is not ready.

## Fallbacks

| If missing | Then |
| --- | --- |
| Engine results | Use feasibility evidence (pre-analysis arithmetic) and say "design stage, not simulated" |
| Deployed app | Run locally, or deploy with sample data, labelled |
| Cost sets | Show exposure and expenditure only, no cost comparison |
