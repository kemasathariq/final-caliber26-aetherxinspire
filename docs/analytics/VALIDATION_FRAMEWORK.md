# INSpire Validation Framework

**Status:** DRAFT v0.1. Applied on 2026-11-04, results in `SIMULATION_METHODOLOGY_AND_RESULTS.md`. Defines how forecasts, policies and simulations are checked. Historical replay and future what-if simulation are kept apart throughout.

## 1. Verification versus validation

| Term | Question | How | Possible now |
| --- | --- | --- | --- |
| Verification | Does the code do what the specification says? | Hand-checked worked example (design section 11), pre-registered predictions, unit tests, failure-detection tests | Yes, once the engine exists |
| Validation | Does the model represent the real system? | Needs actual stock history, receipts, confirmed policy | **No.** The model can be verified, not validated |

Everything reported as validation below means empirical testing against recorded issues. It does not mean confirmed against plant behaviour.

## 2. Forecast validation (D3 and D4 materials only, 296 in Scenario A)

| Item | Specification |
| --- | --- |
| Target | Cumulative demand over the lead-time proxy, and the alpha quantile used for reorder points |
| Procedure | Rolling origin with an expanding window. First origin after month 9, last before month 16 |
| Candidates | Block bootstrap (primary), Croston-SBA, TSB, mean of history, last-period naive |
| Metrics | Pinball loss at each alpha. Empirical coverage of the alpha quantile. Scaled error on cumulative demand. Bias |
| Acceptance (pre-registered) | A method is used for a class only if it beats the mean-of-history baseline on pinball loss on most materials of that class. Otherwise the baseline is used, or the product abstains |
| Reporting | Per class, with the count of materials, both demand scenarios |

Coverage is judged with its sampling error stated. With under 10 origins per material, results are shown per class, not per material.

## 3. Historical held-out replay

| Item | Specification |
| --- | --- |
| Split | Parameters from months 1 to 11 (2025-05 to 2026-03). Test months 12 to 17 (2026-04 to 2026-09). Configurable |
| Demand in test | Recorded issues, as they are, under Scenario A and B |
| Lead time | Deterministic promised median per view |
| Policies | R0, R1, R2, X1 to X3 (parameters from the training months only), N1 |
| Opening inventory | **Common to all policies.** Rule set in the configuration: recorded Stock, or recorded Min, or recorded Max. Each rule is reported. Recorded Stock is undated, so it is an assumption |
| Output | Same measures as the simulation, with the word "replay" |
| Interpretation | A replay of recorded issues against an assumed starting stock. It is not a reconstruction of actual stock, and its shortfalls are not actual stockouts |

## 4. Future what-if and Monte Carlo (separate)

Run sets S1, S2, MC-D, MC-L, MC-J per the design. They answer "what could happen under stated assumptions". They are never compared with replay numbers as if they were the same quantity. Seeds, block sizes and run counts are stored in `run_manifest.json`. Common random numbers keep policy comparisons fair.

## 5. Fair baseline comparison rules

1. Same demand path, same opening inventory, same lead-time draw for every policy.
2. Same unmet-demand rule (backorder reference, lost sales alternative).
3. Same order quantity rule unless the policy defines its own. Differences are stated.
4. Recorded policy is compared in both readings, R1 and R2.
5. A naive benchmark (N1) is included to show whether added complexity helps.
6. Both demand scenarios and both PR PO views are run. A result is "robust" only if the direction holds in all. Otherwise it is reported as scenario-dependent.
7. The comparison covers T3 only.

## 6. Sensitivity analysis

| Factor | Variations (all configurable) |
| --- | --- |
| Demand scenario | A, B |
| PR PO view | OR, ED |
| Opening inventory | Recorded Stock, Min, Max |
| Lead-time proxy | Promised median, p90, a multiplier set |
| Reference reading | R1, R2 |
| Unmet demand | Backorder, lost sales |
| Bootstrap block size | 1, 3, 6 |
| Event month | Included, down-weighted |
| Repeated maximum lines | Included, capped |
| Evidence thresholds | 4, 6, 8 active months |

Report the share of scenarios where each conclusion holds, and the factor that moves it most. No single scenario is headlined.

## 7. Claim rules

| Allowed | Not allowed |
| --- | --- |
| "Under scenario SC-A-ED-R1-BO-K0, simulated shortfall probability is x" | "Stockouts would fall by x percent" as a prediction |
| "Recorded stock is above recorded Max for 1,380 Stock Items" | "1,380 items are overstocked" |
| "Proposed parameters are candidates for review" | "Optimal", "best", "guaranteed" |
| "In replay, with assumed opening stock, ..." | "Last year the plant would have avoided ..." |
| "Lead-time proxy, promised interval" | "Actual lead time" |
| Any monetary figure labelled assumption-based, with the approved cost set ID | Any monetary saving without approved assumptions |

## 8. Engine acceptance after build

1. Hand-checked worked example reproduced exactly.
2. Pre-registered predictions hold: 125 and 133 materials never reach Min (A and B), 183 at or below Min on day 0, 436 identical across scenarios, 8 with differing Min reached.
3. Conservation test: opening plus receipts minus issues plus backorders equals closing, for every material and day.
4. Same seed gives byte-identical output.
5. Failure-detection tests: a damaged input makes the check fail.
6. Stop gate after deterministic R0 for Lead review before stochastic runs (D-04).

## 9. Output validation owner

The Lead validates engine output. Atria validates that the application displays the files without altering values. Brilian validates that financial figures reconcile to engine units and approved cost sets.
