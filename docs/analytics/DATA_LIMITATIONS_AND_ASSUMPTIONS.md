# INSpire Data Limitations and Assumptions

**Status:** DRAFT v0.1. A consolidated view for the three workstreams. The full registers are `docs/analysis/ASSUMPTIONS_REGISTER.md` (A-xx, DEF-xx) and `docs/analysis/SIMULATION_INPUT_ASSUMPTION_REGISTER.md` (P-xx, S-xx). This file maps them to capabilities and adds blueprint-level assumptions (B-xx). It does not replace them.

## 1. Limitations and which capability they limit

| Limitation | Register ID | Stockout | Overstock | Reorder | Slow-moving | Dynamic params | Cost-risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Stock is undated, no receipts | DEF-12 | Limits (opening is assumption) | Limits (recorded only) | Limits | Limits | Limits | Blocks cash tied up |
| Min.Qty and Max.Qty undefined | DEF-02 | Limits (policy reading) | Limits | Limits | none | Limits | Limits |
| Promised dates only, no receipts | DEF-06 | Limits | none | Limits | none | Limits | Limits |
| PR PO exact copies, cause open | DEF-01 | Limits | none | Limits | none | Limits | Limits |
| PR quantity and amount meaning | DEF-05, A-15 | Limits | none | Limits | none | Limits | Blocks price use |
| Movement copies, log completeness | A-05, A-06 | Limits | none | Limits | Limits | Limits | Limits |
| Repeated maximum values | A-11 | Limits tails | none | Limits | none | Limits | Limits |
| Criticality unranked | DEF-03 | Blocks weighting | Blocks weighting | Blocks weighting | none | Blocks | Blocks |
| Non Stock holds stock | DEF-04 | none | Limits | none | Limits | none | none |
| Notifications not failures, order types unknown | DEF-07, DEF-09 | none | none | none | none | none | none (context only) |
| 17 months of history | A-08 | Limits (no seasonality) | none | Limits | Limits | Limits | Limits |
| One plant, one supplier per material, no freight | Discovery report | none | none | none | none | none | Rules out network optimisation |
| No holding, ordering or stockout cost | Not in data | none | none | none | none | none | **Blocks** |
| Data is synthetic | A-02 | Limits every claim | | | | | |
| Official brief missing | A-03, C-01 | Limits framing of every capability | | | | | |

## 2. Blueprint-level assumptions

| ID | Assumption | Basis | Impact | Owner | Resolves with |
| --- | --- | --- | --- | --- | --- |
| B-01 | The six capabilities, MVP, SQLite and Vercel are binding | USER-STATED, brief absent | High | Lead | D-01 |
| B-02 | Evidence thresholds 6 active months, 10 lead observations | Design S-16 | High | Lead | D-03 |
| B-03 | Slow-moving default: 2 or fewer active months, or no issue in last 6 months, with stock above zero | Analyst choice | Medium | Lead | D-03 |
| B-04 | Service-level scenario set 90, 95, 98 percent | Convention, no data | Medium | Lead | D-05 |
| B-05 | Syntetos-Boylan cut-offs 1.32 and 0.49 for classes | Published convention | Low | Lead | D-06 |
| B-06 | Replay split months 1 to 11 and 12 to 17 | Analyst choice | Medium | Lead | Configurable |
| B-07 | Order quantity Q from median PR quantity or months of cover, no EOQ | No cost data | High | Lead | D-09 |
| B-08 | Review period monthly | Analyst choice | Low | Lead | Configurable |
| B-09 | Engine built and run by the Lead, consumed through a file contract | Team design | Medium | Lead | D-13 |
| B-10 | UI shows no default scenario or view | Project rule, see D-11 | Medium | Lead | D-11 |
| B-11 | Opening stock is an assumption, in three rules | DEF-12 | High | Lead | Snapshot date |

## 3. Unresolved questions for the case owner (priority)

1. Official Case 3 brief and scoring criteria.
2. What are Min.Qty and Max.Qty, per plant or per location?
3. Meaning of criticality A, B, C, S and their order.
4. Snapshot date of Stock. Are receipts available?
5. Meaning of PO-Item Amount and PR-Quantity. Goods-receipt dates?
6. Are PR PO and Movement exact copies errors?
7. Is Movement a complete issue log?
8. Order type prefixes 201 to 209, notification types N1, N2, N3, N6.
9. Are cost parameters (holding, ordering, stockout) available or should scenarios be used?
10. Explanation of the May 2025 notification backlog and December 2025 issue peak.
11. Logistics: supplier and storage-location master, goods-receipt dates, shipment and transfer history, freight costs, definitions of PR-Type and notification types, emergency handling (transportation assessment section 7).
