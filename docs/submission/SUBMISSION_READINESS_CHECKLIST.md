# INSpire Submission Readiness Checklist

**Status:** 2026-11-04. Each item has a state, evidence and an owner. States: DONE (verified), PARTIAL, OPEN, BLOCKED (names the blocker). Update this file as items change. Do not mark an item DONE because code ran. DONE needs the stated evidence.

## 1. Requirements (USER-STATED, unchecked against the brief)

| # | Item | State | Evidence or blocker | Owner |
| --- | --- | --- | --- | --- |
| 1 | Official Case 3 brief obtained and checked | PARTIAL | Brief inspected 2026-11-04, audit written. Lead acceptance D-18 open. Full alignment not claimed | Lead |
| 2 | Functional MVP | OPEN | Not started in this repository. AETHER not inspected | Atria |
| 3 | SQLite database | OPEN | Schema specified, not built | Atria |
| 4 | Vercel deployment | BLOCKED | D-07, D-08 | Atria, Lead |
| 5 | Stockout Risk demonstrated | OPEN | Needs engine | Lead, Atria |
| 6 | Overstock Risk demonstrated | OPEN | Needs engine (descriptive part possible from M2) | Lead, Atria |
| 7 | Reorder Recommendation demonstrated | OPEN | Needs engine | Lead, Atria |
| 8 | Slow-Moving Alert demonstrated | OPEN | Rule specified (B-03), needs approval and build | Lead, Atria |
| 9 | Dynamic Inventory Parameters demonstrated | OPEN | Needs engine | Lead, Atria |
| 10 | Cost-Risk Optimisation Scenarios demonstrated | BLOCKED | D-09, D-10 | Brilian |
| 11 | AI assistant explains, does not invent numbers | OPEN | Contract specified | Atria |
| 12 | Human approval workflow | OPEN | Specified | Atria |

## 0. Phase 1 status (2026-11-04)

| Item | State | Evidence |
| --- | --- | --- |
| Brief inspected and traced | DONE | `strategy/OFFICIAL_CASE_ALIGNMENT_AUDIT.md`, verified again in Phase 1 |
| Figures reconciled to source | DONE | `analytics/FIGURE_AND_METHOD_RECONCILIATION.md`. 750 of 750 checks and 354 tests re-confirmed |
| Decision register and Phase 2 plan | DONE (draft, awaiting Lead) | `strategy/DECISION_REGISTER.md`, `strategy/PHASE_2_EXECUTION_PLAN.md` |
| Blockers cleared | **NO** | Engine unbuilt, D-07 and C-1, no application or deployment |
| Phase 2 started | NO | Needs Lead approval |

## 1A. Official submission requirements (brief p8, p9, OFFICIAL)

Brief: "To be eligible for final presentation, you must submit these 2 materials." Non-compliance affects evaluation.

| # | Item | State | Evidence or blocker | Owner |
| --- | --- | --- | --- | --- |
| 1a | Deadline Thursday 2026-11-05 06:00 (time zone not stated). Submission link arrives by WhatsApp group and email | OPEN, about 12 hours left at audit time | Confirm link and time zone | Lead |
| 1b | Prototype is a working MVP, not static HTML | OPEN | Nothing built | Atria |
| 1c | Published on Vercel | BLOCKED | D-07, D-08 | Atria |
| 1d | Database is SQLite | OPEN | Schema only | Atria |
| 1e | One .zip with complete source code and the database. Raw workbooks excluded | OPEN | D-07 default in `DECISION_REGISTER.md` section 2 | Atria, Lead |
| 1f | Screenshot (.png, .jpg or .jpeg) with timestamp of the latest deployed Vercel version | OPEN | After final deploy | Atria |
| 1g | Deck follows the official format, six content slides plus optional Appendix | OPEN | `PRESENTATION_STRUCTURE.md` section A | Lead |
| 1h | Cover has team name and member names | OPEN | Names not in repository | Lead |
| 1i | Key Question 1 and Key Question 2 answered in the deck | OPEN | Slide 3 blocks drafted | Lead |
| 1j | Business Impact slide has success metrics and expected benefits | PARTIAL | Definitions in `PROBLEM_STATEMENT.md` section 6 | Lead, Brilian |
| 1k | Roadmap slide has timeline, outputs, stakeholders, risks and mitigations | PARTIAL | Content drafted, not built | Lead |
| 1l | Team profile table (Name, Major, Semester, Expertise, Contribution) and AI models and tools used | OPEN | Member details missing | Lead |
| 1m | Everything in English | PARTIAL | Documents are English | All |
| 1n | Forecast output visible (R-16) and `recommended_action` (R-17) | OPEN | D-23, D-19 | Lead, Atria |

## 2. Analytical foundation

| # | Item | State | Evidence |
| --- | --- | --- | --- |
| 13 | Six datasets staged and conformed, raw unchanged | DONE | Checksums, `outputs/tables/validation_results.csv` |
| 14 | Marts M1 to M3 validated | DONE | 750 of 750 checks pass, 354 tests pass |
| 15 | Simulation design and feasibility | DONE | `docs/analysis/SIMULATION_*` |
| 16 | Demand classification table | OPEN | D-06 |
| 17 | Tier table | OPEN | Specified in blueprint |
| 18 | Engine R0 run and Lead review | OPEN | D-02, D-04 |
| 19 | Engine stochastic runs and validation | OPEN | After 18 |
| 20 | Historical replay and rolling-origin validation | OPEN | After 18 |
| 21 | Sensitivity report | OPEN | After 19 |
| 21a | Transportation assessment and positioning approved | PARTIAL | Assessment written, D-14 open |
| 21b | Supply context panel (Level B) | OPEN | D-14, D-16, Atria |
| 21c | Logistics data request prepared | OPEN | D-15 |

## 3. Integrity and claims

| # | Item | State | How to check |
| --- | --- | --- | --- |
| 22 | Data label on every output and slide | OPEN | Text scan of app, slides, reports |
| 23 | No claim of actual stockout | OPEN | Text scan |
| 24 | No saving, ROI or "optimal" claim | OPEN | Text scan |
| 25 | Scenario ID on every engine number | OPEN | App test |
| 26 | Both demand scenarios and both PR PO views carried, no default | OPEN | App and report check (D-11) |
| 27 | Simulated and replay results labelled apart | OPEN | Review |
| 28 | Currencies and units never combined | OPEN | Test and review |
| 29 | No source data sent to an external service | OPEN | D-07, review of assistant and deploy configuration |
| 30a | No transportation result, route or cost shown | OPEN | Text scan, app review |
| 30 | AETHER not modified by this repository | DONE for this repository | No AETHER files present |

## 4. Team and documents

| # | Item | State | Evidence |
| --- | --- | --- | --- |
| 31 | Blueprint documents written | DONE (draft) | Twenty-one files (sixteen blueprint, the transportation assessment, `OFFICIAL_CASE_ALIGNMENT_AUDIT.md`, `DECISION_REGISTER.md`, `PHASE_2_EXECUTION_PLAN.md` and `FIGURE_AND_METHOD_RECONCILIATION.md`) under `docs/strategy`, `docs/analytics`, `docs/handover`, `docs/submission` |
| 32 | Blueprint approved by the Lead | OPEN | Review |
| 33 | Atria handover acknowledged | OPEN | Atria |
| 34 | Brilian handover acknowledged | OPEN | Brilian |
| 35 | Decisions D-01 to D-25 answered | OPEN | `strategy/DECISION_REGISTER.md` (D-01, D-14, D-18 closed) |
| 36 | Presentation built | OPEN | `PRESENTATION_STRUCTURE.md` |
| 37 | Rehearsal done, jury Q and A prepared | OPEN | `SOLUTION_NARRATIVE.md` section 5 |
| 38 | Repository committed with agreed scope | OPEN | Lead performs Git operations. Decide ignore rules for `docs/case` and `docs/research` first |

## 5. Minimum viable submission if time runs out

1. Official items 1a to 1m first. Without a working prototype, the zip, the screenshot and the deck, the team is not eligible (brief p8).
2. Data foundation, root cause analysis and methodology, all done in draft.
3. Engine R0 and R1 on the 665 materials with sensitivity under A and B.
4. Application with capabilities 1 to 5 on the real or sample files, labelled.
5. Capability 6 as exposure and expenditure only, with no cost comparison.
6. Honest limits slide.
