# CALIBER 2026 Simulation Input and Assumption Register

**Date:** 2026-11-04. **Status:** for review. **No simulation has been run.** Open items here don't close without the case owner or a named document.

**Data status:** Source data documented as synthetic (dummy) in the Data Context & Relationship Diagram; not operational performance.

**Case limitation.** The complete Case 3 problem statement is not confirmed in the available project documents. The only case document is Case 2 content under a Case 3 filename. No item here comes from a competition requirement. This register also continues `ASSUMPTIONS_REGISTER.md`, whose A- and DEF- items still apply.

**Evidence labels**

| Label | Meaning |
| --- | --- |
| OBSERVED | In the data as supplied |
| PROXY | An observed value standing in for something unobserved |
| ASSUMED | A choice the data doesn't support or contradict |
| CONFIGURED | A what-if value chosen to test sensitivity. Not an estimate |

## 1. Parameters

| ID | Parameter | Source | Label | Treatment | Uncertainty | Sensitivity | Open item |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P-01 | Issue lines, per scenario | `movement_copy_classification` | OBSERVED, as issues | Replayed by date and `source_row` | Scenario A may overstate, and B may understate. Completeness undocumented. Issues may be censored by availability | Both scenarios always, $\phi_D$ | A-05, A-06 |
| P-02 | Initial inventory $I_0$ | `mart_material_inventory.stock` | **ASSUMED** on timing | Undated Stock, applied on day 0 | Could be any date, and more naturally the extract's end than its start. Direction of error unknown | $\phi_I$ x0.5, x1.5, = Min, = Max, Stock + issues | DEF-12 |
| P-03 | Min | `mart_material_inventory.min_qty` | **Unverified** | Reorder level in the reference reading | Meaning undefined. Median 1. Max is exactly 2 or 3 times Min on 400 of 665, which suggests a rule or generated values | $\phi_s$ x0.5, x1.5 | DEF-02 |
| P-04 | Max | `mart_material_inventory.max_qty` | **Unverified** | Order-up-to level in the reference reading | Meaning undefined. Median 3. Conflicts with observed values on 398 of 665 | $\phi_S$ x0.5, x1.5, policy R2 | DEF-02 |
| P-05 | Lead proxy $\tilde{L}$ | `promised_interval_days_median`, both views | **PROXY** | Median promised date minus PR date, rounded up to whole days | **Not an actual lead time.** No receipts or PO date. Includes any approval time. Direction of error unknown | $\phi_L$ x0.5, x1.5, x2, p90 | DEF-06 |
| P-06 | Lead proxy spread | `promised_interval_days` on each line | PROXY | Resampled for 140 materials only | Spread of promises, not of deliveries. 267 materials have 1 or 2 observations | MC-L | DEF-06, S-18 |
| P-07 | Alternative order size | `pr_quantity_median` | PROXY | Policy R2 only | May not be the ordered quantity. Requests exceed issues overall | Policy R1 against R2 | DEF-05, A-15 |
| P-08 | Time horizon | 2025-05-01 to 2026-09-30, 518 days | OBSERVED window | Fixed | Window end is the assumed cutoff | Not varied | A-01 |
| P-09 | Evidence thresholds | `src/config.py`: 6 months, 10 observations | CONFIGURED | Gate on resampling | Analyst choices | Counts shown from 3 to 12 months and 5 to 20 observations | S-16 |
| P-10 | Multipliers $\phi$ | Configuration | CONFIGURED | What-ifs | Not estimates. No evidence selects them | Section 9 of the design | |
| P-11 | Replications, block length, seed | Configuration | CONFIGURED | Monte Carlo control | Convergence is checked | Block length 1 or 3 | S-17 |

## 2. Inputs deliberately not used

| Input | Reason |
| --- | --- |
| **Unit amounts** (`implied_unit_amount_scenario_*`, `po_item_amount`) | Not reliable or comparable. 661 of 665 materials are in IDR and 4 aren't (2 JPY, 1 EUR, 1 USD), with no exchange rate. Within a material the highest implied amount is typically 2.11 times the lowest, up to 5.28 times. Meaning undefined (DEF-05). They affect no calculation, and the eligibility condition that mentions them doesn't change the population |
| **Holding, ordering and stockout costs** | Not in the data. None are invented |
| **Historical PR PO arrivals** | Requests exceed issues overall (A-15), and no receipts exist. Replaying them wouldn't balance |
| **Criticality and priority** | Unranked (DEF-03, DEF-16). No service target is set by them |
| **Location data** | 84% of issue lines have no location link. The model is per material |
| **Plan items** | Plans don't state their parts |

## 3. Structural assumptions

| ID | Assumption | Why this choice | Risk if wrong | Treatment |
| --- | --- | --- | --- | --- |
| S-01 | Stock applies on day 0 | The approved treatment. A forward run needs a start | Early results are artefacts, and possibly all of them | $\phi_I$ levels, plus measures from the first arrival onward |
| S-02 | No open orders on day 0 | No dated open-order record exists | Early stockouts are overstated | Stated. Larger $\phi_I$ levels approximate it |
| S-03 | Reference reading: Min is the reorder level, and Max is the order-up-to level | The usual reading of such fields, but **only a reading**. Evidence against it is on 398 of 665 materials | The reference results describe a policy the plant may not use | Policy R2, $\phi_s$, $\phi_S$, and reported as unverified |
| S-04 | Daily review after issues, and reorder at IP at or below s | Simplest rule consistent with daily data | Timing shifts by a day | Rule is stated, and a test covers it |
| S-05 | Partial fill with backorders in the reference set | Data doesn't say. Observed issues did occur, so backorder loses less demand from a record known to have happened | Lost sales would give different levels | Lost-sales alternative |
| S-06 | Backorders first, then issues in `source_row` order | Fixed for reproducibility. File order has no documented meaning | Small effect on line fill rate | Stated |
| S-07 | Same-day arrivals serve that day's issues | Dates have no time of day | Slightly favourable | Stated |
| S-08 | Materials are independent, with no shared limits | No capacity, budget or supplier limit in the data | Real constraints would worsen results | Stated |
| S-09 | One supply source, unlimited quantity, no lot sizes | One observed supplier per material, and no supplier capacity or lot data | Actual orders may be constrained | Stated |
| S-10 | Lead proxy doesn't depend on who else is ordering | No capacity data | Delays under load are missed | $\phi_L$ |
| S-11 | Issues are demand | Only available signal. Movement Type is Issue only | Availability-limited demand is understated | $\phi_D$, reported as issues |
| S-12 | No returns, reversals or stock adjustments | Only Issue rows exist | Levels drift from reality | Stated |
| S-13 | All days alike, no calendar | Lines are even across all seven days | Lead proxies might mean working days | Stated |
| S-14 | Lead rounding up to whole days, at least 1 | Daily model, and medians can be half-days | Small effect | Stated |
| S-15 | Demand multipliers round so that cumulative totals stay accurate | Quantities are whole numbers in the reference set | Small effect on line timing | Stated |
| S-16 | Resampling needs 6 or more active months, or 10 or more distinct lead observations | Below these, a resample mostly repeats a few values. Analyst choice | Different thresholds change who is resampled, up to 233 and down to 47 | Counts shown, and configurable |
| S-17 | Blocks of 3 months preserve enough clustering | 37.9% of lines fall in three months. 17 months can't separate season from one-off | Spread is understated or misplaced | Block length 1 or 3, and labelled as what-if |
| S-18 | Lead draws are independent of order size | Needed for per-order draws. **Observed Spearman of -0.28 in EA contradicts strict independence** | Spread on large orders is misstated | Stated as an approximation |

## 4. Uncertainty by source

| Source | Reducible by | Handled in the design by |
| --- | --- | --- |
| Meaning of Min, Max and Stock | Case owner or brief | Configured what-ifs, not distributions |
| Actual lead times | Goods-receipt dates | $\phi_L$ levels |
| Movement copies | Document number | Scenarios A and B |
| Issue log completeness | Case owner | $\phi_D$ levels |
| Sampling variation | Longer history | Resampling, for materials that qualify |
| Data is synthetic | Organiser confirmation | Label on all outputs |

**Most of the uncertainty is about meaning, not sampling.** Monte Carlo addresses only the last-but-one row. It can't reduce the others, and a narrow Monte Carlo spread shouldn't be read as a reliable result.

## 5. Questions for the official brief or case owner

Priority order, by effect on the design: (1) What do Min and Max mean? (2) When was Stock measured? (3) Are goods-receipt dates available? (4) Is the Movement file a complete issue log, and are identical rows real? (5) What does PO-Item Amount include, and what are the prices? (6) What is the official service definition or target, if any? (7) Is a cost basis provided?

## 6. `simulation_population` columns

`data/processed/simulation_population.csv`, one row for each of 7,481 materials. Load with `read_conformed`, using `simulation_population_metadata.json`. **No column is a simulated result, a historical stockout or a cost.** Columns marked ARITHMETIC are calculations on inputs under the reference reading.

| Column | Description |
| --- | --- |
| `material_no` | Material number, text |
| `unit` | Material unit |
| `mrp_type` | MRP type code from BoM |
| `population_status` | `in_population` or `excluded`, under the approved eligibility criteria |
| `exclusion_reasons` | Why the material is excluded. Blank if in the population |
| `n_exclusion_reasons` | Number of exclusion reasons |
| `assumed_initial_inventory` | Stock as supplied, ASSUMED to be inventory at the start of the horizon |
| `min_parameter_unverified` | Min.Qty. Unverified |
| `max_parameter_unverified` | Max.Qty. Unverified |
| `lead_proxy_median_days__original_rows` | Median promised interval, `original_rows`. Proxy |
| `lead_proxy_median_days__exact_distinct_rows` | Median promised interval, `exact_distinct_rows`. Proxy |
| `lead_proxy_p90_days__exact_distinct_rows` | 90th percentile of the promised interval. Proxy |
| `lead_observations_distinct` | Promised intervals on `exact_distinct_rows`. Copies aren't independent observations |
| `pr_quantity_median__exact_distinct_rows` | Median PR quantity per line |
| `active_months` | Months with an issue, of 17. The same in both scenarios |
| `lines__scenario_a` | Issue lines in Scenario A |
| `lines__scenario_b` | Issue lines in Scenario B |
| `qty_total__scenario_a` | Issued quantity in Scenario A |
| `qty_total__scenario_b` | Issued quantity in Scenario B |
| `max_line_qty__scenario_a` | Largest single issue line. The same in both scenarios |
| `demand_evidence_tier` | `d1_resampling_allowed`, `d2_replay_and_configured_only` or `d3_single_active_month` |
| `lead_evidence_tier` | `l1_resampling_allowed`, `l2_point_and_configured_only` or `l3_one_or_two_lines` |
| `resampling_allowed_demand` | Own-history resampling of demand is allowed |
| `resampling_allowed_lead` | Own-history resampling of the lead proxy is allowed |
| `resampling_allowed_both` | Both are allowed |
| `scenarios_identical_by_construction` | No rule C1 rows, so A and B must give identical results |
| `demand_materially_affected` | Materially affected by the scenario choice (A-14) |
| `has_line_at_repeated_unit_peak` | Has a line at a repeated unit peak (A-11) |
| `at_or_below_min_at_start` | ARITHMETIC. An order is triggered on day 0 under the reference reading |
| `stays_above_min__scenario_a` | ARITHMETIC. No order is ever triggered in Scenario A under the reference reading |
| `stays_above_min__scenario_b` | ARITHMETIC. No order is ever triggered in Scenario B under the reference reading |
| `initial_inventory_covers_all_issues__scenario_a` | ARITHMETIC. Initial inventory is at least all Scenario A issues |
| `initial_inventory_covers_all_issues__scenario_b` | ARITHMETIC. Initial inventory is at least all Scenario B issues |
| `single_line_exceeds_max` | OBSERVED. One issue line is larger than Max |
| `median_pr_quantity_exceeds_max` | OBSERVED. Median PR quantity is larger than Max |
| `stock_above_max` | OBSERVED. Stock is above Max |
| `lead_proxy_exceeds_horizon` | ARITHMETIC. Median lead proxy is longer than the 518-day horizon |
