# INSpire Inventory Optimisation Methodology

**Status:** DRAFT v0.1. **Built on 2026-11-04, see `SIMULATION_METHODOLOGY_AND_RESULTS.md`. Monthly re-estimation in section 3 was not built.** Builds on `docs/analysis/SIMULATION_DESIGN_SPECIFICATION.md` (event flow, mathematics, worked example) and does not repeat it. No output of this method is called optimal. No cost enters unless approved (D-09).

## 1. Recorded versus proposed

| Item | Source | Label in the product |
| --- | --- | --- |
| Recorded Min, Recorded Max | BoM `Min.Qty`, `Max.Qty` | "Recorded, meaning unconfirmed" |
| Reference policy R1 | Min as reorder point, Max as order-up-to level | "Reference reading, not verified plant practice" |
| Alternative R2 | Reorder point Min, fixed order quantity equal to the median PR quantity | Same |
| Proposed reorder point s | Engine, scenario level alpha | "Candidate for review" |
| Proposed order-up-to S | Engine | "Candidate for review" |

The two sets are always shown side by side. A proposed value never overwrites a recorded one.

## 2. Parameter definitions (PROPOSED)

All quantities are per material, in its own unit, per scenario ID.

- **Lead-time demand (LTD).** Simulated demand over a sampled lead time. Lead time per order is resampled from the material's promised intervals (at least 10 distinct values), else a configurable scenario value. Demand paths come from the block bootstrap of observed months (at least 6 active months), else deterministic or configurable.
- **Reorder point s(alpha).** The alpha quantile of LTD, for alpha in the service-level scenario set (default 90, 95, 98 percent, D-05). These are scenario levels, not targets.
- **Safety stock.** s(alpha) minus mean LTD, reported as a derived value. Floored at zero and flagged when negative.
- **Order quantity Q.** Candidate Q1 is the median PR quantity for the chosen view. Candidate Q2 is a configurable number of months of mean demand. EOQ is not used, because ordering and holding costs are unavailable (D-09).
- **Order-up-to S.** s(alpha) plus Q. Also reported with the cap at recorded Max when comparing with R1.
- **Target stock.** Equal to S, shown with units of cover, never as money.

## 3. Dynamic Min-Max (PROPOSED)

Parameters are re-estimated at each review period from a trailing window, only while evidence stays above threshold. Rules:

1. The review period and window length are configuration (default monthly, all available history, because history is short).
2. If evidence falls below threshold, hold the last approved parameters and show "held, insufficient evidence".
3. The product shows change versus the previous approved parameters and the scenario that produced it.
4. Nothing is applied automatically. A planner approves, rejects or defers.

With 17 months, dynamic behaviour can be shown as a replay of how estimates would have moved, not as a proven benefit.

## 4. Current versus proposed policy comparison

Compared inside one run set: same demand paths, same opening inventory, same lead-time draws (common random numbers), same unmet-demand rule, same horizon. Policies compared: R0 (replay of recorded values), R1, R2, X1 to X3 at the service-level scenarios, and a naive benchmark N1 (reorder at mean LTD, same Q).

Reported measures, in units, never money:

| Measure | Meaning |
| --- | --- |
| Shortfall probability | Share of runs with at least one simulated shortfall |
| Expected unmet quantity | Mean simulated unmet quantity |
| Days at or below zero | Simulated |
| Mean and p95 on-hand | Units |
| Days above recorded Max, units above Max | Simulated overstock |
| Orders placed, mean order size | Replenishment frequency |
| Policy ranking stability | Share of scenarios where the proposed policy has a lower shortfall probability and not more on-hand than recorded |

All appear under demand Scenario A and B, and PR PO views OR and ED. A result that differs between them is flagged, not averaged.

## 5. Slow-moving and obsolete monitoring (PROPOSED)

| Flag | Default rule (ASSUMPTION, configurable) | Wording |
| --- | --- | --- |
| Slow-moving | Stock above zero and at most 2 active months of 17, or no issue in the last 6 months of the window | "Slow-moving by recorded issues" |
| No recorded consumption | Stock above zero and never issued in the window | "No recorded consumption in 17 months" |
| Obsolete | Not assigned. Needs lifecycle, BoM status or equipment retirement data | Never claimed |

**Brief alignment (audit X-02, D-21 pending).** The brief asks for "non-moving" and "potentially obsolete" parts (p4) and "dead stock" (p6). Allowed wording if D-21 is approved: "non-moving by recorded issues" (never issued in the window) and "potentially obsolete candidate" (stock above zero, no issue in the window, no recorded plan link at its locations), always as a HYPOTHESIS needing lifecycle data. "Obsolete" and "dead stock" stay forbidden as plain claims.

Rules use recorded stock and recorded issues only. Stock is undated, so cover figures use the word "recorded".

## 6. Eligibility, abstention and review

| Condition | Result |
| --- | --- |
| Not T3 | No policy comparison. Descriptive only |
| T3 below evidence thresholds | Deterministic and configurable-scenario output only, labelled |
| Recorded Max conflicts with the reference reading (398 of 665) | Show R1 and R2 results, mark "recorded parameters may not follow this reading", require review |
| Never reaches recorded Min (125 and 133) | "No orders triggered by observed issues". Not an error |
| At or below Min on day 0 (183) | Early results flagged as opening-stock driven. Run alternate opening rules |
| Scenario divergence material (88) | Review required |
| Currency or unit mismatch | Excluded from any value statement |

## 7. What this method will not say

- That any parameter is optimal.
- That a policy saves money, or reduces actual stockouts.
- That recorded Min/Max is wrong.
- Anything about plant performance.

## 8. Dependencies

Needs D-02 (reference reading), D-03 (thresholds), D-04 (staging), D-05 (service levels). Cost-risk comparison needs D-09 and D-10, see `BRILIAN_FINANCIAL_HANDOVER.md`.
