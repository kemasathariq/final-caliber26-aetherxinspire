# INSpire Team Responsibility Matrix

**Status:** DRAFT v0.1. Each row has exactly one accountable owner (A). R means responsible for doing the work. C means must be consulted before the decision. I means informed. Owners are roles: Lead is the Overall Solution Lead, Atria is the AI, Frontend and Deployment Lead, Brilian is the Financial Analysis Lead.

## 1. Ownership by deliverable

| Deliverable or decision | Lead | Atria | Brilian |
| --- | --- | --- | --- |
| Business problem, root cause analysis | A, R | I | C |
| Interpretation of the six datasets, data marts M1 to M3 | A, R | I | C |
| Transportation problem framing, positioning and future logistics requirements | A, R | C | C |
| Supply context panel and logistics extension points in the application | C | A, R | I |
| Evaluation of logistics-related financial information, missing freight inputs, future logistics cost-risk requirements | C | I | A, R |
| Approval of transportation positioning (D-14) and data request (D-15) | A, R | I | I |
| Business rules, eligibility tiers, evidence thresholds | A, R | C | C |
| Demand intelligence methodology | A, R | I | I |
| Inventory optimisation methodology, simulation engine | A, R | C | C |
| Scenario identifier grammar and analytical output contract | A, R | C | C |
| Recommendation record format (fields, evidence metadata) | A | R | C |
| SQLite schema, loaders, application, UX | C | A, R | I |
| AI assistant behaviour and prompts | C | A, R | I |
| AETHER reuse inventory and integration | C | A, R | I |
| Vercel deployment, technical testing | I | A, R | I |
| Financial methodology, price interpretation proposal | C | I | A, R |
| Cost scenario sets, sensitivity analysis | C | I | A, R |
| Approval of any cost assumption used in a published number | A | I | R |
| Financial evidence for presentation | C | I | A, R |
| Validation of engine output | A, R | C | C |
| Final narrative and presentation | A, R | C | C |
| Git operations and merges | A | R | R |

Rule for the cost-assumption row: Brilian proposes and calculates, the Lead approves. No monetary figure is published without that approval.

## 2. Boundaries that must not blur

| Boundary | Rule |
| --- | --- |
| Transportation | The Lead frames and positions. Atria builds only supporting context and empty extension points. Brilian lists missing cost inputs. Nobody models routes, costs or savings without data |
| Business logic versus calculation | The Lead defines what a quantity means. Brilian calculates money from approved inputs. Atria displays and stores. Nobody recomputes another owner's quantity |
| Engine versus application | The engine writes files that follow the contract. The application reads them and never recalculates a recommendation |
| Assistant versus engine | The assistant quotes stored values and explains them. It does not produce or alter a number |
| Data versus presentation | No chart or sentence may drop the scenario ID or the data label |

## 3. Dependencies

| Needs | From | Blocks |
| --- | --- | --- |
| Official brief check (D-01) | Lead | All OFFICIAL labels |
| Engine output files | Lead | Atria's real data load, Brilian's scenario grid |
| Cost scenario proposal (D-09, D-10) | Brilian | Capability 6, exposure figures |
| Persistence and external-service decisions (D-07, D-08) | Atria proposes, Lead approves | Deployment and assistant |
| AETHER inventory (D-12) | Atria | Architecture finalisation |
| Transportation positioning (D-14) and data request (D-15) | Lead | Module M-J, narrative wording, any Level C move |
| Mock data in the contract format | Lead (schema), Atria (builds against it) | Atria can start now |

## 4. Escalation

If two owners disagree on a definition, the definition in `MASTER_SOLUTION_BLUEPRINT.md` section 6 stands and the question goes to the Lead as a new decision ID.

## Additions from the official brief audit (2026-11-04)

| Deliverable (brief page) | Owner | Support | Note |
| --- | --- | --- | --- |
| Deck in the official format, six content slides plus Appendix (p9) | Lead | Atria, Brilian | `submission/PRESENTATION_STRUCTURE.md` |
| Team profile table: names, major, semester, expertise, contribution, AI models and tools (p9) | Lead | All | Lead supplies member details |
| Zip of complete source and SQLite database (p8) | Atria | Lead | D-07 must be decided first |
| Vercel screenshot with timestamp of the latest deployment (p8) | Atria | Lead | After the final deploy |
| Forecast output R-16 and stock-level what-if (p4, p6) | Lead | Atria | D-23 |
| `recommended_action` field R-17 (p4) | Lead | Atria | D-19 |
| Success metric definitions (p9 slide 4) | Lead | Brilian | `PROBLEM_STATEMENT.md` section 6 |

## Phase 1 lock: parallel boundaries (2026-11-04)

| Area | Lead | Atria | Brilian |
| --- | --- | --- | --- |
| Shared definitions (scenario grammar, tiers, terms, metrics) | **Owns, sole editor** | Reads, requests change | Reads, requests change |
| Contract columns and enums | **Owns** | Implements, requests change | Consumes `eng_*`, owns `fin_*` columns |
| Engine, forecast, recommended action rules | **Owns** | Displays, never recomputes | Never recomputes |
| Recommended action thresholds (D-25) | **Owns** | none | Reviews cost wording only |
| SQLite schema, loaders, UI, backend, tests, deployment, zip, screenshot | Approves D-07 | **Owns** | none |
| Price interpretation, exposure, cost sets, `fin_scenario_grid.csv` | Approves cost sets (D-09) | Displays approved sets | **Owns** |
| Wording of AI and method claims (D-22) | **Owns** | Follows | Follows |
| Persistence and data-handling proposals (D-07, D-08) | Decides | Proposes, tests | none |

Execution plan, dependencies and acceptance: `PHASE_2_EXECUTION_PLAN.md`. Decisions: `DECISION_REGISTER.md`.
