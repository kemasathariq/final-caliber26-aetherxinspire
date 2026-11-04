# INSpire Problem Statement

**Status:** DRAFT v0.1. **Data label:** findings describe the supplied synthetic dataset, not Chandra Asri operations. The official brief (`docs/case/CALIBER 2026 - Final Case Brief.pdf`) was inspected on 2026-11-04. The framing below is ours and rests on the data. The brief's own problem sentence (p3): the company "lacks an integrated and predictable approach to forecasting spare part demand and inventory level setting". Use it verbatim on the deck.

## 1. Core problem

Planners who stock spare parts must decide, for thousands of materials, what needs attention, how much to hold, and when to reorder. In the supplied dataset, the records they would use for that decision do not support it directly:

- Recorded Min and Max values sit away from recorded consumption.
- Most parts are issued in only one or two months of seventeen.
- Maintenance work is rarely linked to the parts issued for it.
- Procurement records hold promised dates, not receipts, and half of the PR PO rows are exact copies.
- Stock has no date.

INSpire's job is to turn these records into a transparent, reviewable decision aid, and to say plainly where the records are too thin to decide.

## 2. Decision questions

| # | Question a planner asks | Data basis | Answerable today? |
| --- | --- | --- | --- |
| 1 | Which parts need attention first? | M2, M3, FuncLoc criticality (unranked) | Partly. Ranking by criticality is blocked (DEF-03) |
| 2 | Which parts have irregular or sparse demand? | M3 | Yes, descriptively |
| 3 | How much should be held? | M2, M3, M1 | Only as scenario candidates for 665 materials |
| 4 | When should replenishment start? | M1 lead proxy, M3 | Only as scenario candidates for 665 materials |
| 5 | Which parts carry stockout, overstock or slow-moving risk? | M2, M3 | Overstock and slow-moving: descriptive. Stockout: simulated only |
| 6 | How to balance availability, exposure and risk? | Engine plus cost scenarios | Not until D-09 |
| 7 | Which recommendations need human review? | Evidence tiers | Yes, by rule |

## 3. Business impact and consequences

The dataset holds no downtime, production loss, cost of stockout, holding cost or ordering cost. **No business impact can be measured from it.** Impact statements are limited to:

- RESEARCH or HYPOTHESIS: unplanned maintenance with missing spares prolongs downtime. (The company assessment in `docs/research/` scores spare parts intelligence 2.85, a qualitative score, not a measurement.)
- OBSERVATION: 1,380 of 3,656 Stock Items hold stock above recorded Max (37.7 percent), and 504 sit below recorded Min. These are raw comparisons against values whose meaning is unconfirmed. They are not excess or shortage findings.

## 4. Scope

**In scope:** 7,481 materials in the BoM, with depth depending on evidence tier (T1 state only, T2 demand-evidenced, T3 policy-simulatable). One plant (1000). Seventeen months, 2025-05 to 2026-09.

**Transportation and distribution (investigated, not optimised):** INSpire is positioned as Integrated Spare Part Supply Chain Intelligence. Inbound procurement lead time and supplier context are in scope as supporting intelligence (Level B). Transportation, allocation, transfer and routing optimisation are future enhancements (Level C) because the data has one plant, one supplier per material and no location, receipt or freight data. See `analytics/TRANSPORTATION_AND_DISTRIBUTION_ASSESSMENT.md`.

**Out of scope:** supplier selection (one supplier per material in the data), equipment failure prediction, and any financial claim without approved assumptions.

## 5. Success criteria

1. Every recommendation shows its evidence tier, scenario identifier and data label.
2. A planner can reproduce any number from stored inputs.
3. The product abstains where evidence is insufficient, and says why.
4. No output claims a historical stockout or a monetary saving.
5. All six capabilities are visibly demonstrated on at least one T3 material and one abstention case.

## 6. Success metrics and expected benefits (brief p9 slide 4)

The brief requires success metrics ("how success will be measured") and expected benefits. The dataset cannot support any measured benefit. These are therefore **metric definitions**. Targets and baselines are left to the case owner, and no value is claimed.

| Metric | How measured | Baseline from the data? | Target |
| --- | --- | --- | --- |
| Recommendation coverage | Materials with a recommendation or a stated abstention reason, divided by 7,481 | Yes, computable from the tier table | Not set |
| Share of materials with evidence tier shown | Same | Yes | 100 percent (design rule) |
| Forecast error on held-out months | Rolling-origin error versus a naive baseline, D3 and D4 only | No, needs the engine | Not set |
| Replay stock-position gap | Days at or below zero and units above recorded Max, recorded versus proposed, same replay | No, needs the engine | Not set |
| Inventory exposure at risk | Stock times reference unit amount, under an approved price rule, per currency | No, D-10 open | Not set |
| Planner decision time and review rate | Approved, rejected, deferred counts | Only after use | Not set |

**Expected benefits (qualitative, from the brief's impact list, p3):** earlier sight of parts at risk, fewer parts reviewed blind, clearer separation of slow-moving from active parts, a documented reason for each stock level. These are intended benefits, not results.
