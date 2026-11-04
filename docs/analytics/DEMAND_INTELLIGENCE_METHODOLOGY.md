# INSpire Demand Intelligence Methodology

**Status:** DRAFT v0.1. **Built on 2026-11-04, see `SIMULATION_METHODOLOGY_AND_RESULTS.md`, which holds the checked counts. The pre-registered test rejected the bootstrap quantile (D-26).** The text below is the design as written. Counts are OBSERVATION from M3 (Scenario A), with the class split labelled indicative (read-only computation, not a validated mart, D-06). Terms: `MASTER_SOLUTION_BLUEPRINT.md` section 6.

**Governing rules.** Movement issues are observed consumption, not proven demand (A-06). No distribution is fitted from thin history. Where evidence is short, use a configurable scenario or abstain. Maintenance schedules and notifications become demand only through a defensible material relationship, which the data rarely gives (20.5 percent order link).

**Unit of forecast.** Demand during the lead-time proxy, not a monthly point forecast. Monthly point forecasts on 17 months of sparse data would look precise and mean little.

## 1. Demand classes

Active month means a month with at least one issue. The window is 17 months (2025-05 to 2026-09). Counts are Scenario A, issued materials only (1,930).

| Class | Rule | Materials | Evidence requirement | Methodology | Confidence | Forecast eligible | Validation | Abstain or review when |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| D0 No recorded consumption | Never issued | 5,551 | None | No demand statement. State-only output | n/a | No | n/a | Always abstain on demand. Wording: "no recorded consumption in the window" |
| D1 Sparse | 1 to 2 active months | 1,475 (1,220 with a single month) | Insufficient | Descriptive only. Optional configurable-demand scenario, labelled assumption | Low | No | None possible | Abstain from reorder and parameter recommendation. Review if the single issue is a repeated maximum or outlier |
| D2 Thin | 3 to 5 active months | 159 | Minimal | Observed rate and size only. No distribution, no interval | Low | Rate only, as a range from min to max of observed months | Retrospective sanity check | Abstain from parameter recommendation. Show range |
| D3 Intermittent, lumpy or erratic | 6 or more active months and not smooth | 265 (indicative: 112 erratic, 87 lumpy, 66 intermittent) | Meets threshold (pending D-03) | Empirical block bootstrap of months (block 3). Croston-SBA or TSB as comparison baseline | Medium, Low if Scenario A and B diverge materially | Yes, for lead-time demand | Rolling origin plus replay (`VALIDATION_FRAMEWORK.md`) | Abstain if bootstrap beats no baseline. Review on repeated-maximum values |
| D4 Smooth | ADI below 1.32 and CV squared below 0.49 | 31 (indicative) | Meets threshold | Mean and spread of monthly demand, bootstrap for tails | Medium | Yes | Same | Review if trend break is visible |

D2, D3 and D4 together hold 455 materials not flagged sparse. Of them, 296 meet 6 active months (D3 and D4). Indicative D3 and D4 splits came from monthly ADI and CV squared on non-zero months, Syntetos-Boylan cut-offs. They need to be rebuilt as a checked table (D-06).

## 2. Modifiers applied on top of the class

| Modifier | Rule | Effect |
| --- | --- | --- |
| Abnormal consumption | Robust z above 3.5 within material, or `n_lines_at_repeated_unit_maximum` above 0 (A-10, A-11) | Never removed. Flag, run a sensitivity with the lines capped at the next value, require review before a recommendation is approved |
| Scenario sensitivity | `demand_materially_affected` (88 of 665 T3) | Both scenarios shown, confidence lowered one level |
| Event month | A month above a configurable multiple of the median month (December 2025 holds 2,580 lines, A-08) | Sensitivity run with the month down-weighted. Cause is a HYPOTHESIS (turnaround or backlog) |
| Maintenance link | Share of issue lines whose order links to a notification and a BoM-listed location | Shown as context. Never used to scale demand |
| Equipment failure context | Notification counts at the BoM locations | Context only. Notifications are not failures (DEF-09) |
| Planned and preventive maintenance | Mitem and Mplan counts per location | Context only. No kit is inferred (cycle meaning open, DEF-10, DEF-11) |
| Shutdown or turnaround | No shutdown calendar exists | Not modelled. Event-month sensitivity only |
| Procurement uncertainty | Promised interval median and p90, two PR PO views | Lead proxy used as a range and per-order resample above 10 observations. Otherwise a configurable scenario |
| Seasonality | 17 months, under two years | Not estimated. Abstain. Statement shown in the UI |

**Phase 1 reconciliation.** "D3, D4 (T3)" below means the **228** materials of classes D3 and D4 that are also in the simulation population. The other 68 of the 296 forecast-eligible materials get a forecast but no policy output. Parameters for the 437 other T3 materials are not proposed (D-24). See `FIGURE_AND_METHOD_RECONCILIATION.md`.

## 3. Demand classes and the six capabilities

| Class | Stockout | Overstock | Reorder | Slow-moving | Dynamic parameters | Cost-risk |
| --- | --- | --- | --- | --- | --- | --- |
| D0 | No | Descriptive | No | "No recorded consumption" | No | No |
| D1 | No | Descriptive | No | Yes | No | No |
| D2 | No | Descriptive | No | Yes | No | No |
| D3, D4 (T3) | Simulated | Simulated and descriptive | Candidate | Yes | Candidate | Scenario only |
| D3, D4 not T3 | No | Descriptive | No | Yes | No | No |

## 4. Confidence levels

| Level | Condition |
| --- | --- |
| High | Not assigned in this dataset. Synthetic data, unconfirmed definitions, 17 months. Reserved for a later, validated state |
| Medium | D3 or D4, thresholds met, both scenarios agree, promised interval has at least 10 observations, no unresolved outlier flag |
| Low | D1, D2, or any condition above not met |
| Abstain | D0, or evidence below the minimum for the capability |

## 5. Method choices and why

- **Empirical bootstrap over fitted distributions.** With under 18 observations per material, a fitted distribution invents shape.
- **Croston-SBA and TSB as baselines only.** They give a comparison, the bootstrap is the primary lead-time demand source.
- **Abstention is a result.** The product reports how many materials it declines, and why.
