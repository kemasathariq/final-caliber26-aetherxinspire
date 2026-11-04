# CALIBER 2026 Simulation Feasibility Assessment

**Date:** 2026-11-04. **Status:** for review. **No simulation has been run.** Every figure is observed, or arithmetic on observed values and stated assumptions, rebuilt by `src/simulation_design/feasibility.py` and listed in `outputs/reports/simulation_feasibility_evidence.md`.

**Data status:** Source data documented as synthetic (dummy) in the Data Context & Relationship Diagram; not operational performance.

## 1. Conclusion

**A simulation is feasible as a what-if stress test of stated assumptions. It is not feasible as a prediction, a reconstruction of history or a financial case.**

- **Supported:** a verified single-item model on 665 materials, comparing Scenarios A and B, and showing sensitivity to each unverified input.
- **Only partly supported:** Monte Carlo, on 139 materials for demand and lead proxy together.
- **Not supported:** validating the model against what happened, stating actual stockouts, or any monetary result.
- **The main risk is the reference policy.** On 398 of 665 materials, observed values conflict with reading Max as an order-up-to level. So a reference run may describe a policy the plant doesn't use.

**Recommendation.** Proceed to implementation only after review against the official Case 3 brief. Stop after the deterministic reference set to judge whether the policy reading is usable before building the rest.

## 2. Case 3 limitation

**The complete Case 3 problem statement is not confirmed in the available project documents.** The diagram identifies the workbooks as Case 3, Spare Part Intelligence, while the available case document, despite its Case 3 filename, is Case 2 content. **This assessment doesn't state what the competition requires, and can't judge whether the design answers it.** That review is the next gate.

## 3. What can and cannot be supported

| Capability | Verdict | Evidence | Condition or reason |
| --- | --- | --- | --- |
| Event-driven model, daily, per material | **Supported** | Dated events. No shared constraints | Verification only |
| Replay of issues under Scenarios A and B | **Supported** | All 665 have issue lines | Issues aren't proven demand |
| Comparing A and B on simulated decisions | **Supported, on 229** | 436 are identical by construction | 202 of the 229 can trigger an order in Scenario A, and only 8 change whether Min is ever reached |
| Sensitivity to each input | **Supported** | Configured levels | Shows dependence. Doesn't say which level is right |
| Simulated stockout periods | **Supported, as simulated only** | Follows from the model | Never a historical claim |
| Service level | **Supported, as simulated only** | Three definitions | No official target is known |
| Average inventory | **Supported, per material or unit** | Follows from the model | Depends heavily on undated stock. No value in money |
| Replenishment frequency | **Partly supported** | 125 to 133 materials would never order | Reflects the reference reading, not plant practice |
| Demand variability | **Supported, as observed** | M3 | Weak for 358 materials with under 3 active months |
| Monte Carlo on demand | **Partly supported** | 228 of 665 | Own-history blocks only |
| Monte Carlo on lead proxy | **Partly supported** | 140 of 665 | Spread of promises, not deliveries |
| Monte Carlo on both | **Partly supported** | 139 of 665, of which 124 can trigger an order | |
| Fitted probability distributions | **Not supported** | Median active months is 2 | Excluded |
| Forward forecast or future horizon | **Not supported** | 17 months, 37.9% of lines in three months | Excluded |
| Validation against history | **Not supported** | No dated stock, receipts or stockout record | The largest limit. See Section 6 |
| Actual lead times or delivery reliability | **Not supported** | No receipt dates | Proxy only |
| Actual historical stockouts | **Not supported** | No record, and all observed issues happened | Excluded |
| Monetary savings, cost or value | **Not supported** | No cost data, unreliable unit amounts | Excluded |
| Optimal Min, Max or stock levels | **Not supported** | No cost or service target. Out of scope | Excluded |
| Criticality-based service targets | **Not supported** | Codes are unranked | Needs DEF-03 |
| Location-level or network results | **Not supported** | 84% of issue lines have no location link | Per material only |
| Generalising beyond the 665 | **Not supported** | They exclude all Non Stock items, and hold 21% to 99% of quantity by unit | |

## 4. Population

| Group | Materials | Note |
| --- | --- | --- |
| **In population** | **665** | Stock Items with all inputs |
| Stock Items, excluded | 2,991 | |
| - No demand, no promised interval | 2,381 | Nothing to simulate |
| - No promised interval, and so no unit amount record | 486 | **Have demand and Min or Max. Could join with a configured lead time, if approved** |
| - No demand history only | 95 | Have parameters but no issues |
| - Min and Max both zero only | 7 | Have demand and lead proxy, but no policy to test |
| - Other combinations | 22 | |
| Non Stock, excluded | 3,825 | Meaning of Non Stock undefined (DEF-04) |
| **Total** | **7,481** | Each material's status and reasons are in `simulation_population.csv` |

## 5. Evidence by input

**Evidence tiers.** Materials in the population, by demand and lead-proxy evidence.

| Demand evidence | Lead: 10+ observations | Lead: 3 to 9 | Lead: 1 or 2 | Total |
| --- | --- | --- | --- | --- |
| 6+ active months | **139** | 84 | 5 | 228 |
| 2 to 5 active months | 1 | 94 | 60 | 155 |
| 1 active month | 0 | 80 | 202 | 282 |
| **Total** | 140 | 258 | 267 | 665 |

**Only 21% can resample both inputs.** For the other 79%, the design uses replay and configured what-ifs, as the approval requires.

| Input | Finding | Consequence |
| --- | --- | --- |
| Demand history | Median 2 active months and 3 lines. 201 materials have a single issue line | Demand variability can't be estimated for most |
| Demand over time | Monthly lines range from 284 to 1,861. 37.9% fall in November 2025 to January 2026 | Months aren't interchangeable, and no seasonal claim is possible |
| Lead proxy | Median 42 days, range 8 to 829. 4 materials exceed the 518-day horizon | Those 4 may never receive an order inside the horizon |
| Lead against order size | Spearman -0.28 in EA | Independent draws are an approximation |
| Initial stock | 85 at zero, and 183 at or below Min | Multiplying has no effect on 85. Early stockouts come from the assumption |
| Unit amounts | 4 materials aren't in IDR. Within a material, typically 2.11 times from lowest to highest | Not used in any calculation |

## 6. Why the model can't be validated

Validation would compare simulated stock with recorded stock over time. **The data holds one undated stock value and no receipts,** so there's nothing to compare against.

There's a further conflict to report plainly. **Every replayed issue did happen.** So when the model shows a shortage on a replayed issue, the assumed stock, parameters or lead proxies must disagree with whatever really occurred. A simulated stockout is a finding about the assumptions, never evidence of a real stockout. Issues may also be understated, because an unavailable part may never have been recorded.

**Results can therefore be verified, compared and tested for sensitivity, but not called accurate.**

## 7. Is Min/Max a reorder policy? Evidence for and against

Pre-analysis on the 665 materials. This is arithmetic and observation, not simulated output.

| Observation | Materials | Reads as |
| --- | --- | --- |
| One issue line larger than Max | 173 | **Against.** Once stock has been replenished up to Max, it can't serve a single issue that large |
| Median PR quantity larger than Max | 176 | **Against.** Observed requests exceed the supposed ceiling |
| Stock above Max | 256 | **Against**, or Stock isn't governed by Max |
| **Any of those three** | **398 of 665** | **Against** |
| Max is exactly 2 or 3 times Min | 400 | Suggests a rule or generated values, rather than per-part planning |
| Min at or above mean demand during the median lead proxy | 540 | **For.** Consistent with a reorder level |

**Effect on results under the reference reading:**

| Condition | Materials | Consequence |
| --- | --- | --- |
| At or below Min on day 0 | 183 | An order is placed at once. Early results reflect the assumption |
| Never reach Min, Scenario A | 125 | **No orders.** Replenishment frequency is 0 by arithmetic |
| Never reach Min, Scenario B | 133 | **No orders** |
| Initial inventory covers all issues, Scenario A / B | 238 / 253 | No shortage possible |

So **the reading is plausible for some materials and contradicted for others, and the data can't settle it.** This is why the design adds policy R2, and why it stops after R0.

## 8. How much the scenario choice can matter

| Group | Materials | What to expect |
| --- | --- | --- |
| Scenarios identical by construction | 436 | No difference, by definition |
| Scenarios differ | 229 | Differences possible |
| - Can trigger an order in Scenario A | 202 | Decisions could change |
| - Materially affected on quantity | 88 | Larger changes possible. 36 of these have under 5 lines |
| - Materially affected and can trigger an order | 73 | **The most informative group** |
| Scenario choice changes whether Min is ever reached | 8 | Direct change to the order decision |

**Expectation to test, not a finding:** the scenario choice is likely to matter less than the unverified inputs, because many materials don't differ at all. The design's dominance check tests this.

## 9. Requested against issued quantity

On the 665 materials, PR quantity on `exact_distinct_rows` exceeds Scenario A issues on 431 materials, with a median ratio of 1.70. Historical orders therefore can't be replayed as arrivals, and they can't validate simulated replenishment. See A-15 in `ASSUMPTIONS_REGISTER.md`.

## 10. Risks

| Risk | Effect | Mitigation in the design |
| --- | --- | --- |
| Results read as real stockouts or forecasts | False conclusions | Labels, `sim_` prefix, boundary tests and language rules |
| A narrow Monte Carlo spread read as reliable | False confidence | Reported as spread under resampling. Meaning-based uncertainty is stated separately |
| The reference reading is wrong | Results describe a policy that doesn't exist | Policy R2, parameter what-ifs and the stop gate after R0 |
| Early stockouts read as demand-driven | Overstated shortage | Measures reported from the first arrival onward too |
| Averages across materials hide extremes | Misleading summaries | Percentiles and counts, and no quantity totals across units |
| The official brief differs from this design | Wrong questions answered | Review gate before implementation |
| Time pressure | Dropped checks | Staged build with the worked example first |

## 11. What would improve feasibility

| If supplied | Then |
| --- | --- |
| Official Case 3 brief | Questions, population and measures can be confirmed |
| Definition of Min and Max | Policy reading is confirmed or replaced |
| Stock snapshot date | Initial inventory can be anchored properly |
| Goods-receipt dates | Actual lead times, real validation of arrivals, and stock reconstruction |
| Dated stock history | **True validation becomes possible** |
| Confirmation of Movement copies | One demand scenario could be retired |
| Cost basis and prices | Financial analysis could be considered |
| Lead-time assumption approved for 486 Stock Items | Population could grow |

## 12. Decisions for review

| Decision | Recommendation |
| --- | --- |
| Is the design consistent with the official Case 3 brief? | Required before implementation |
| Daily event-driven model, without a framework | Accept |
| Reference reading R1, with R2 as the alternative | Accept as labelled, pending a definition of Min and Max |
| Backorder as the reference, lost sales as the alternative | Accept |
| Evidence thresholds of 6 months and 10 observations | Accept, or set preferred values |
| Stop gate after R0 | Accept |
| Add the 486 Stock Items later, with configured lead times | Hold until after R0 |
