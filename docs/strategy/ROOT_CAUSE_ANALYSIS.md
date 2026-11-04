# INSpire Root Cause Analysis

**Status:** DRAFT v0.1. **Method:** symptom to cause chain (five whys) plus a fishbone grouping by Data, Process, Policy and Context. **Scope:** causes of why the supplied records cannot support spare-part decisions, and what the dataset shows about inventory, demand and procurement.

**Read this first.** The existing RCA reports in `docs/analysis/consolidated_root_cause_analysis_reports.md` are Case 2 equipment RCAs. They are not used here (C-02). Every cause below is labelled **SUPPORTED** (an OBSERVATION in the dataset supports it) or **HYPOTHESIS** (needs validation). A SUPPORTED label means the pattern exists in the dataset. It does not prove why. The data is synthetic, so some patterns may come from how it was generated (A-02).

## 1. Symptoms (what a planner sees)

| ID | Symptom | Evidence (OBSERVATION) |
| --- | --- | --- |
| S1 | Recorded stock sits far from recorded Min/Max | Of 3,656 Stock Items: 472 zero stock, 504 below Min, 1,380 above Max, 29 with Min = Max = 0 (M2) |
| S2 | Many recorded Max values cannot work as an order-up-to level | Among 665 T3 materials: 398 conflict with reading Max as an order-up-to level: a single issue line above Max (173), median PR quantity above Max (176), or stock above Max (256), any of the three (feasibility assessment, pre-analysis arithmetic) |
| S3 | Many parts never reach recorded Min | For 125 (Scenario A) and 133 (Scenario B) of 665, observed issues over the window never take stock from its opening level to Min (pre-analysis arithmetic, not simulated) |
| S4 | Demand is sparse | 1,220 of 1,930 issued materials are issued in a single month. 1,475 are flagged sparse. Only 296 have six or more active months |
| S5 | Stock without a stocking rule | 1,683 Non Stock materials hold stock, all with Min = Max = 0 |
| S6 | Requests far exceed issues | PR quantity is 7.5 to 9 times issued quantity in the large units (A-15) |

| S7 | Promised delivery dates are widely spread and partly implausible | Promised interval median 42 days, p90 155, CV 1.23. 630 requested dates precede the PR date. 429 promised dates fall after 2027 (read-only, transportation assessment) |

## 2. Root causes

| ID | Root cause | Status | Supporting evidence | Symptoms explained | Validation needed |
| --- | --- | --- | --- | --- | --- |
| RC1 | **Recorded Min/Max is static and not tied to observed demand or lead time** | SUPPORTED as a pattern, cause HYPOTHESIS | Max is exactly 2 times or 3 times Min on 400 of 665 T3 materials (rule-like, not demand-derived). Min covers mean lead-time demand on 540 of 665. 183 sit at or below Min on day 0 | S1, S2, S3 | Case owner explanation of how Min/Max is set (DEF-02) |
| RC2 | **Demand for most parts is too sparse for conventional forecasting** | SUPPORTED | S4 evidence. Indicative classification (computed read-only for this blueprint, see note): 1,634 intermittent, 153 lumpy, 112 erratic, 31 smooth of 1,930 | S2, S3 | Longer history, confirmation that Movement is complete (A-06) |
| RC3 | **Maintenance work is weakly linked to materials** | SUPPORTED | Only 20.5 percent of Movement orders appear in Notif History. When linked, 22.6 percent of issued materials are on the BoM of that notification's location. Only 25.8 percent of BoM materials were issued | Cannot explain demand by equipment | Order type definitions (DEF-07), task lists |
| RC4 | **Procurement records do not show what was actually ordered or received** | SUPPORTED | 46.7 percent of PR PO rows are exact copies (cause open, DEF-01). Lead time is promised only (DEF-06). No receipts. PR quantity may not equal order quantity (DEF-05) | S6, uncertain lead times | Receipt dates, PO quantity, definition of amount |
| RC5 | **Master data does not state its own meaning** | SUPPORTED | Stock is undated (DEF-12). Criticality A, B, C, S unranked (DEF-03). Non Stock holding stock (DEF-04). Units mixed, 10 codes, no conversion | S1, S5 | Definitions from case owner |
| RC6 | **No visible review cycle for parameters** | HYPOTHESIS | No history of Min/Max changes in any file. Rule-like multiples under RC1 | S1, S2 | Parameter change log, planner interviews |
| RC7 | **Issue log may not equal demand** | HYPOTHESIS | Movement Type is only "Issue". 863 exact copy lines (4.93 percent) handled as two scenarios. Repeated maximum values (A-11) | Distorted demand level | Confirmation from case owner (A-06, A-05) |

| RC8 | **Inbound lead time is long and highly variable, and its source cannot be separated into supplier, processing and transit time** | Pattern SUPPORTED (promised intervals only). Cause HYPOTHESIS | Promised interval p10 15, median 42, p90 155 days. Supplier-level CV median 0.66. Foreign-currency lines median 151.5 days against 42 (98 rows, six suppliers, currency is not origin) | S7, S3 (via lead-time demand) | Receipt dates, shipment dates, supplier country (assessment 4.1, 4.5) |
| RC9 | **There is no logistics visibility: no receipt, transfer, storage location, supplier location or freight record** | SUPPORTED as data absence | One plant, one movement type `Issue`, no origin or destination, one supplier per material, no cost field | S1, S6, blocks any transport analysis | Data list in assessment section 7 |
| RC10 | **Emergency needs and multi-location stock positioning may be handled outside the records** | HYPOTHESIS, no supporting or contradicting evidence | 135 Emergency notifications, 8 of 134 orders with any issue. PR-Type and notification types undefined | None explained | Emergency definitions, expedite and transfer logs, stock by location |

**Transportation-related causes are labelled as hypotheses wherever the data cannot separate them.** RC9 is a statement about the data, not about the business. Do not report any of RC8 to RC10 as a confirmed operational fact.

**Note on the demand classification.** The class counts use monthly buckets over the 17-month window, the Syntetos-Boylan cut-offs (ADI 1.32, CV squared 0.49) and Scenario A. They were computed read-only during this blueprint and are not a validated mart. They must be rebuilt as a checked table before use (D-06). Treat them as an indication of shape only.

## 3. Cause chains

- **S3 (parts never reach Min):** Min is high relative to observed issue rate (RC1), because demand is sparse (RC2), so even rare large issues rarely cross it. Whether this is excess protection or a data artefact is unknown.
- **S1 (stock above Max on 1,380 items):** Stock is undated (RC5) and receipts are missing (RC4), so it cannot be said whether stock was built by purchasing against Min/Max or is an old balance.
- **S6 (requests exceed issues):** PR quantity meaning unknown (RC4), issue log completeness unknown (RC7), or generator behaviour (A-02).

## 4. Fishbone grouping

| Category | Causes |
| --- | --- |
| Data | RC4, RC5, RC7 |
| Process | RC3, RC6 |
| Policy | RC1 |
| Context | RC2 (sparse operating history, 17 months) |
| Logistics (data and process) | RC8, RC9, RC10 |

## 5. What this analysis cannot say

- Which cause drives cost or downtime. No such data exists.
- That any recorded Min/Max is wrong. Their meaning is unconfirmed.
- That transportation, delivery or distribution drives any stock problem.
- That excess stock is waste. Unit cost is weak and stock is undated.

## 6. Implication for the solution

| Root cause | Design response |
| --- | --- |
| RC1 | Simulate recorded and proposed parameters under identical conditions (capability 5) |
| RC2 | Classify demand, abstain where evidence is thin, resample only above thresholds |
| RC3 | Use maintenance context only as context, flag unlinked issues |
| RC4 | Carry both PR PO views, label lead time as promised |
| RC5 | Show data confidence on every recommendation and keep a visible definitions list |
| RC6, RC7 | Human approval workflow and review log |
| RC8 | Show promised interval and spread as supply context, label it promised, carry its spread into the lead-time demand (Level B) |
| RC9 | Document missing data, build extension points, do not model transport (Level C roadmap) |
| RC10 | Descriptive count of emergency notifications only, with small-sample warning. No emergency optimisation |
