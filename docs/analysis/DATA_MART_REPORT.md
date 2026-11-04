# CALIBER 2026 Data Mart Report: M1 to M3

**Date:** 2026-11-04. **Project:** Case 3, Spare Part Intelligence. **Specification version:** `0.1+corrections-3`.

**Data status:** Source data documented as synthetic (dummy) in the Data Context & Relationship Diagram; not operational performance.

## 1. Summary

M1 (procurement), M2 (inventory) and M3 (material demand) are built from the conformed tables and reconcile to them. No source record is changed or removed. Movement copies are handled through two parallel demand scenarios, and every Movement row keeps its classification and reason.

**No view or scenario is the default, and none is the true value.** PR PO has `original_rows` and `exact_distinct_rows`. Demand has Scenario A and Scenario B. They sit in separate files, so they can't be added together by accident.

**Main results:**

- **The scenario choice barely moves totals, but it does move some materials.** 863 of 17,518 lines (4.93%) differ. 400 of 1,930 materials change, and 222 change by 10% or more in quantity.
- **Most of those 222 have little history.** 135 have fewer than five lines, where removing one line produces a large percentage. 87 have five or more lines.
- **Simulation inputs are complete for only 665 of 7,481 materials**, all Stock Items, and 88 of those are materially affected by the scenario choice.

**What this does not establish:** which scenario or view is right, or that issues are demand. Open definitions and the limitations in Section 8 still apply.

Location: `data/processed/`. Load with `read_conformed`, using the column types in `mart_metadata.json`.

| Mart | File | Grain | Key | Rows |
| --- | --- | --- | --- | --- |
| M1 | `mart_procurement_line__original_rows` | One PR PO source row | `source_row` | 11,609 |
| M1 | `mart_procurement_line__exact_distinct_rows` | One PR item and PO item | `purchase_requisition` + `pr_item` | 6,189 |
| M1 | `mart_supplier_material__original_rows` | One supplier, material and currency | `supplier_code` + `material_no` + `currency` | 1,250 |
| M1 | `mart_supplier_material__exact_distinct_rows` | One supplier, material and currency | `supplier_code` + `material_no` + `currency` | 1,250 |
| M1 | `mart_procurement_nonidr__original_rows` | One non-IDR source row | `source_row` | 98 |
| M1 | `mart_procurement_nonidr__exact_distinct_rows` | One non-IDR PR item and PO item | `purchase_requisition` + `pr_item` | 51 |
| M2 | `mart_material_inventory` | One material | `material_no` | 7,481 |
| M3 | `movement_copy_classification` | One Movement source row | `source_row` | 17,518 |
| M3 | `mart_material_demand_month__scenario_a` | One issued material by month | `material_no` + `month` | 32,810 |
| M3 | `mart_material_demand_month__scenario_b` | One issued material by month | `material_no` + `month` | 32,810 |
| M3 | `mart_material_demand_summary__scenario_a` | One issued material | `material_no` | 1,930 |
| M3 | `mart_material_demand_summary__scenario_b` | One issued material | `material_no` | 1,930 |
| M3 | `mart_material_demand_comparison` | One issued material | `material_no` | 1,930 |

## 2. Movement copy classification

This table drives both demand scenarios. It holds **every Movement source row**, including those excluded from Scenario B.

**Eligibility, for both scenarios.** A row counts as demand only if it passes all five rules. All 17,518 rows currently pass. A failing row would stay in the table, with the failed rule named.

| Rule | Condition |
| --- | --- |
| E1 | Movement Type is Issue |
| E2 | Posting Date is within 2025-05 to 2026-09 |
| E3 | Quantity is above zero |
| E4 | Material exists in `dim_material` |
| E5 | Unit equals the material's unit in `dim_material` |

**Copy rule, for Scenario B only.**

| Rule | Condition | Effect |
| --- | --- | --- |
| C1 | Identical to an earlier row in all 7 source columns | In Scenario A. Excluded from Scenario B |

The earliest occurrence stays in Scenario B. Because occurrences are identical, the choice of which to keep changes no quantity. Rows that share a date, material and order but differ in quantity are **not** copies: 657 such rows stay in both scenarios unless they separately meet C1.

**Classes.** The gap to the previous identical row describes the evidence, and does not change membership.

| `copy_class` | Meaning | Rows | Scenario A | Scenario B |
| --- | --- | --- | --- | --- |
| `unique_record` | No identical row exists | 15,835 | Yes | Yes |
| `first_occurrence_of_repeated_record` | Earliest of several identical rows | 820 | Yes | Yes |
| `repeat_adjacent` | C1, gap of 1 row | 429 | Yes | **No** |
| `repeat_near` | C1, gap of 2 to 10 rows | 415 | Yes | **No** |
| `repeat_far` | C1, gap above 10 rows (largest gap 32) | 19 | Yes | **No** |

Each row also has `copy_classification_reason`, for example: *"Rule C1: identical in all 7 source columns to source row 17, which is the earliest of 2 occurrences. 1 row after the previous occurrence. Included in Scenario A, excluded from Scenario B. Not proven to be an error."*

**Limitations of the classification:**

- **No document number exists.** Rule C1 cannot separate an accidental copy from two real issues of the same quantity, for the same order, on the same day. This is the central limit, and only the case owner or a document number can settle it (A-05).
- **It can miss copies.** A duplicate posted on another date, or with a different quantity, is not identical, so C1 does not catch it.
- **It can overcount copies.** Small repeated issues, such as one unit twice in a day, are plausible real events.
- **Closeness is suggestive, not proof.** All copies sit within 32 rows of each other, unlike PR PO copies (median gap 2,627). That points to a different origin, but the file order itself has no documented meaning.
- **Adjacent rows are not a stronger class by any rule.** All three repeat classes are excluded together. Quantities per class are kept in the comparison, so a narrower rule can be tested later without rebuilding.

## 3. M1: Procurement mart

**Purpose.** Line-level procurement data with intervals and flags, plus per-material procurement parameters such as promised intervals and order sizes for later replenishment work.

**Source tables.** `fact_prpo_line`, `dim_material`.

**Grain and keys.** See Section 1. `material_no` and `supplier_code` are foreign keys, with no unmatched rows.

**Transformation logic.**

1. Select rows for one view. `original_rows` takes all rows, and `exact_distinct_rows` takes `in_exact_distinct_rows`.
2. Take flags calculated within that view, and drop the view suffix, since each file holds one view.
3. Derive `implied_unit_amount_scenario` as amount divided by PR quantity, assuming the amount is the line total for that quantity (DEF-05, A-13).
4. Add `mrp_type` and `material_prefix` by audited lookup. The row count cannot change.
5. Aggregate to supplier and material. Quantities sum within one material, and amounts within one currency.
6. Calculate interval statistics after setting aside rows promised or requested before the PR date (Spec P-06, P-07). Those rows stay counted in `n_lines`.
7. Report non-IDR lines separately, without conversion. No exchange rate was supplied.

**Amounts by currency.** Each currency stands alone. The two views are alternatives.

| Currency | Lines, `original_rows` | Lines, `exact_distinct_rows` | Amount, `original_rows` | Amount, `exact_distinct_rows` | Ratio |
| --- | --- | --- | --- | --- | --- |
| IDR | 11,511 | 6,138 | 168,836,490,165 | 89,210,784,211 | 1.89 |
| USD | 35 | 17 | 310,714.71 | 139,557.65 | 2.23 |
| EUR | 20 | 11 | 161,470.86 | 99,266.04 | 1.63 |
| JPY | 41 | 21 | 17,669,735 | 7,623,969 | 2.32 |
| SGD | 2 | 2 | 9,569.36 | 9,569.36 | 1.00 |

**Validation.** `MART-30` to `MART-38`: same source rows as the conformed view, unchanged values, flags from the right view, unit amounts recalculate, supplier totals rebuild line totals per currency, line counts and per-material quantity, and one supplier row per material.

**Known limitations.**

- **Promised is not actual.** No receipt date exists, so no interval here is an achieved lead time (DEF-06). There's also no PO date, so the interval starts at the PR date and includes any approval time.
- **Unit amounts are weak.** Within a material, the highest implied unit amount is typically twice the lowest (median 2.04 times, up to 5.28 times, on `exact_distinct_rows` materials with more than one line). The assumption may be wrong, or prices may vary.
- **Thin history.** 373 materials have one line in `exact_distinct_rows`, and 682 have fewer than three lines behind their promised interval.
- **One supplier per material is observed, not proven exclusive.** Supplier names are labels only, and no ranking exists.
- **Non-IDR spend sits outside IDR totals.** 98 lines in `original_rows`, 51 in `exact_distinct_rows`.

### Schema: `mart_procurement_line__*`, and `mart_procurement_nonidr__*` (same columns)

| Column | Type | Description |
| --- | --- | --- |
| `analysis_view` | string | PR PO view this row belongs to. Neither view is the business truth |
| `purchase_requisition` | string | Purchase requisition number, text |
| `pr_item` | string | PR item number, text |
| `purchase_order` | string | Purchase order number, text |
| `po_item` | string | PO item number, text |
| `material_no` | string | Material number, text |
| `material_desc_clean` | string | Material description with surrounding spaces trimmed |
| `unit` | category | Material unit. Quantities are comparable only within it |
| `pr_quantity` | Int64 | PR quantity, in the material unit. Treated as the ordered quantity only in implied_unit_amount_scenario |
| `supplier_code` | string | Supplier code, text |
| `supplier_name` | string | Supplier name, label only. Likely synthetic |
| `po_item_amount` | Float64 | PO item amount, in its own currency. Meaning undefined (DEF-05) |
| `currency` | category | Currency of the amount |
| `pr_type` | category | PR type code. Undefined (DEF-08) |
| `pr_prefix` | string | First 2 digits of the PR number |
| `po_prefix` | string | First 2 digits of the PO number |
| `purchasing_group` | category | Purchasing group code. Undefined (DEF-08) |
| `plant` | string | Plant code. Undefined (DEF-13) |
| `pr_date` | datetime64[ns] | PR date |
| `pr_month` | datetime64[ns] | First day of the PR date's month |
| `pr_delivery_date` | datetime64[ns] | Requested delivery date |
| `po_delivery_date` | datetime64[ns] | Promised delivery date. Not a receipt date (DEF-06) |
| `requested_interval_days` | Int64 | Requested delivery date minus PR date |
| `promised_interval_days` | Int64 | Promised delivery date minus PR date. Not an achieved lead time |
| `promise_gap_days` | Int64 | Promised date minus requested date |
| `occurrence_count` | Int64 | Rows identical in all source columns, including this one |
| `occurrence_rank` | Int64 | Position among identical rows, in source order |
| `content_group_id` | string | Identifier of the group of identical rows |
| `in_idr_scope` | boolean | Currency is IDR |
| `is_non_idr_supplier` | boolean | Supplier's currency is not IDR. Does not establish a foreign supplier |
| `flag_req_before_pr` | boolean | Requested date is before the PR date |
| `flag_promise_before_pr` | boolean | Promised date is before the PR date |
| `flag_future_requested_date` | boolean | Requested date is after the assumed cutoff (A-01) |
| `flag_future_promised_date` | boolean | Promised date is after the assumed cutoff (A-01) |
| `flag_future_date` | boolean | Either delivery date is after the assumed cutoff (A-01) |
| `rare_pr_type` | boolean | PR type has under 30 distinct rows |
| `rare_purchasing_group` | boolean | Purchasing group has under 30 distinct rows |
| `desc_shared_group_id` | string | Same trimmed description on several material numbers. Never merged |
| `source_row` | Int64 | Excel row number in the source workbook |
| `row_hash` | string | SHA-256 of all source values in the row |
| `flag_extreme_interval` | boolean | Requested or promised interval is above this view's 99.5th percentile |
| `flag_outlier_pr_quantity` | boolean | Review flag calculated within this view (A-10) |
| `flag_outlier_requested_interval` | boolean | Review flag calculated within this view (A-10) |
| `flag_outlier_promised_interval` | boolean | Review flag calculated within this view (A-10) |
| `flag_outlier_promise_gap` | boolean | Review flag calculated within this view (A-10) |
| `implied_unit_amount_scenario` | Float64 | PO item amount divided by PR quantity, in its currency. ASSUMES the amount is the line total for that quantity (DEF-05, A-13) |
| `flag_outlier_implied_unit_amount_scenario` | boolean | Review flag within material and currency, in this view (A-10) |
| `mrp_type` | category | MRP type code from BoM. Meaning of Non Stock is undefined (DEF-04) |
| `material_prefix` | string | First 4 digits of the material number. Undefined (DEF-13) |

### Schema: `mart_supplier_material__*`

| Column | Type | Description |
| --- | --- | --- |
| `analysis_view` | string | PR PO view this row belongs to. Neither view is the business truth |
| `supplier_code` | string | Supplier code, text |
| `material_no` | string | Material number, text |
| `currency` | string | Currency of the amount |
| `supplier_name` | string | Supplier name, label only. Likely synthetic |
| `unit` | string | Material unit. Quantities are comparable only within it |
| `n_lines` | Int64 | Lines in this view |
| `n_purchase_orders` | Int64 | Distinct purchase orders in this view |
| `pr_quantity_total` | Int64 | PR quantity summed within one material |
| `pr_quantity_median` | Float64 | Median PR quantity per line |
| `po_item_amount_total` | Float64 | Amount summed within one currency |
| `implied_unit_amount_scenario_min` | Float64 | Lowest implied unit amount (A-13) |
| `implied_unit_amount_scenario_median` | Float64 | Median implied unit amount (A-13) |
| `implied_unit_amount_scenario_max` | Float64 | Highest implied unit amount (A-13) |
| `first_pr_date` | datetime64[ns] | Earliest PR date |
| `last_pr_date` | datetime64[ns] | Latest PR date |
| `n_lines_used_for_promised_interval` | Int64 | Lines left after setting aside promised dates before the PR date |
| `promised_interval_days_min` | Float64 | Lowest promised interval |
| `promised_interval_days_p25` | Float64 | 25th percentile of the promised interval |
| `promised_interval_days_median` | Float64 | Median promised interval |
| `promised_interval_days_p75` | Float64 | 75th percentile of the promised interval |
| `promised_interval_days_p90` | Float64 | 90th percentile of the promised interval |
| `promised_interval_days_max` | Float64 | Highest promised interval |
| `n_lines_used_for_requested_interval` | Int64 | Lines left after setting aside requested dates before the PR date |
| `requested_interval_days_median` | Float64 | Median requested interval |

## 4. M3: Material demand mart

**Purpose.** Monthly and per-material issue history under two parallel scenarios, with a material-level comparison, as the demand input for later simulation.

**Source tables.** `fact_issue`, `dim_material`.

**Grain and keys.** See Section 1. Each month table has 1,930 materials x 17 months.

**Transformation logic.**

1. Classify every Movement row (Section 2).
2. **For each scenario separately**, select its rows and aggregate to material and month. Neither scenario is derived from the other.
3. Fill zeros only inside 2025-05 to 2026-09, and only for materials with an eligible issue. The 5,551 never-issued materials are not zero-filled (A-06).
4. Summarise per material, with monthly statistics over all 17 months. Intermittency classes such as ADI and CV² are left for EDA, per the Specification, but `months_with_issue` and the statistics needed to calculate them are stored.
5. Compare the two sets of results per material.

**Scenarios by unit.** Quantities stay within one unit.

| Unit | Materials | Scenario A | Scenario B | Absolute difference | % of A |
| --- | --- | --- | --- | --- | --- |
| EA | 1,384 | 949,729 | 922,363 | 27,366 | 2.88 |
| KG | 33 | 805,820 | 793,670 | 12,150 | 1.51 |
| L | 23 | 29,807 | 29,068 | 739 | 2.48 |
| LG | 29 | 3,133 | 3,050 | 83 | 2.65 |
| RL | 30 | 2,961 | 2,860 | 101 | 3.41 |
| M | 27 | 2,350 | 2,320 | 30 | 1.28 |
| CAN | 13 | 2,260 | 2,184 | 76 | 3.36 |
| SET | 374 | 1,025 | 958 | 67 | 6.54 |
| SHT | 9 | 38 | 30 | 8 | 21.05 |
| ASS | 8 | 12 | 11 | 1 | 8.33 |

**Materials materially affected.** Tiers apply to the change in total quantity, as a percentage of Scenario A. **These thresholds are analyst choices, not business rules (A-14).** Scenario A is the denominator for arithmetic only, and `qty_diff_pct_of_b` is stored too.

| `impact_tier` | Rule | Materials | Under 5 lines | 5 lines or more |
| --- | --- | --- | --- | --- |
| `no_change` | 0% | 1,530 | 1,372 | 158 |
| `below_threshold` | Under 10% | 178 | 2 | 176 |
| `material` | 10% to under 25% | 70 | 9 | 61 |
| `high` | 25% or more | 152 | 126 | 26 |

Sensitivity to the threshold:

| Threshold | Materials at or above | Under 5 lines | 5 lines or more |
| --- | --- | --- | --- |
| 1% | 376 | 137 | 239 |
| 5% | 280 | 135 | 145 |
| 10% | 222 | 135 | 87 |
| 25% | 152 | 126 | 26 |
| 50% | 81 | 78 | 3 |

**Start with the 87 materials with enough lines.** For the other 135, one line decides the percentage. The full list, with `impact_reason`, is in `outputs/exceptions/demand_materially_affected.csv`. Examples of the largest absolute differences:

| Material | Unit | Scenario A | Scenario B | Difference | % of A | Lines A to B | Under 5 lines |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4200000228 | EA | 15,170 | 10,170 | 5,000 | 32.96 | 49 to 48 | No |
| 4200000566 | EA | 1,020 | 520 | 500 | 49.02 | 3 to 2 | Yes |
| 4100079353 | EA | 1,000 | 500 | 500 | 50.00 | 2 to 1 | Yes |
| 4100024279 | EA | 2,352 | 2,080 | 272 | 11.56 | 54 to 51 | No |
| 4100107050 | L | 1,863 | 1,663 | 200 | 10.74 | 43 to 42 | No |

**Other effects on simulation inputs.** Monthly standard deviation differs on 398 materials, and peak monthly quantity on 260. **The months with an issue never differ**, because a copy shares its date with the row kept, so measures based only on active months' timing are unaffected.

**Validation.** `MART-10` to `MART-14` cover the classification. Every row is present with unchanged values. The copy rule is recalculated separately by walking the rows. Scenario membership follows the rules. `MART-20` to `MART-29` cover demand. Rows equal materials x months, and the window is exact. Totals and monthly counts equal direct sums from the conformed table. Zero-filled rows hold zeros. Summaries equal the monthly tables. Differences equal each material's C1 quantity. Percentages and tiers recalculate. Tests also recalculate scenario totals, monthly values and the affected list from CSV files, using only the Python standard library.

**Known limitations.**

- **Issues are observed movements, not proven demand** (A-06). Zero-filling assumes the Movement file is the complete issue log, which isn't documented. A zero month may be a missing record.
- **Short history.** 17 months is too short for a seasonality test. 1,220 of 1,930 materials are active in a single month, and 1,475 have `flag_sparse_history`, so their monthly standard deviations are weak.
- **Repeated peak values (A-11).** 42 materials have lines at a unit peak shared by at least five materials: 23,135 KG, 5,700 EA, 200 L and 100 M. Where present, these lines typically make up about 35% of a material's total in EA and KG, and over 85% in L and M. See `n_lines_at_repeated_unit_maximum`.
- **Monthly grain.** Simulation at a finer grain can aggregate `movement_copy_classification`, which keeps `posting_date`.
- **Location coverage is thin.** Only 2,731 of 17,518 lines link to one location, 60 are ambiguous, and 14,727 have no link. Demand here is per material, not per location.

### Schema: `movement_copy_classification`

| Column | Type | Description |
| --- | --- | --- |
| `source_row` | Int64 | Excel row number in the source workbook |
| `row_hash` | string | SHA-256 of all source values in the row |
| `posting_date` | datetime64[ns] | Issue posting date |
| `movement_type` | category | Movement type as supplied |
| `material_no` | string | Material number, text |
| `material_desc_clean` | string | Material description with surrounding spaces trimmed |
| `quantity` | Int64 | Issued quantity, in the material unit |
| `unit` | category | Material unit. Quantities are comparable only within it |
| `order_no` | string | Order number, text |
| `posting_month` | datetime64[ns] | First day of the posting date's month |
| `order_prefix` | string | First 3 digits of the order number. Undefined (DEF-07) |
| `has_notification` | boolean | The order appears in Notif History |
| `order_shared` | boolean | The order is on more than one notification |
| `fl_attribution` | string | Link from order to location: unique, ambiguous or none. Ambiguous rows are never allocated |
| `attributed_functional_location` | string | Location, filled only when the order leads to exactly one |
| `issued_material_in_fl_bom` | boolean | Material is on the BoM of a location linked through the order. Blank when no link exists |
| `content_group_id` | string | Identifier of the group of identical rows |
| `occurrence_count` | Int64 | Rows identical in all source columns, including this one |
| `occurrence_rank` | Int64 | Position among identical rows, in source order |
| `same_key_group_size` | Int64 | Rows sharing date, material and order |
| `is_partial_dup_group` | boolean | Same date, material and order with differing quantities. Not a copy under rule C1 |
| `partial_dup_group_id` | string | Identifier of that group |
| `first_source_row_of_group` | Int64 | Source row of the earliest identical row |
| `copy_gap_rows` | Int64 | Rows since the previous identical row. Blank on the earliest |
| `is_copy_c1` | boolean | Rule C1: identical in all 7 source columns to an earlier row. Not proven to be an error |
| `copy_class` | string | unique_record, first_occurrence_of_repeated_record, repeat_adjacent, repeat_near or repeat_far |
| `copy_classification_reason` | string | Plain-language reason for this row's classification |
| `is_eligible_demand` | boolean | Passes eligibility rules E1 to E5 |
| `eligibility_rules_failed` | string | Eligibility rules this row fails. Blank if none |
| `in_scenario_a` | boolean | Counted in Scenario A |
| `in_scenario_b` | boolean | Counted in Scenario B |
| `flag_at_repeated_unit_maximum` | boolean | Quantity equals its unit's peak, and at least 5 materials share that peak (A-11) |

### Schema: `mart_material_demand_month__*`

| Column | Type | Description |
| --- | --- | --- |
| `demand_scenario` | string | Demand scenario this row belongs to. Neither scenario is the true demand |
| `material_no` | string | Material number, text |
| `month` | datetime64[ns] | First day of the calendar month |
| `unit` | category | Material unit. Quantities are comparable only within it |
| `mrp_type` | category | MRP type code from BoM. Meaning of Non Stock is undefined (DEF-04) |
| `material_prefix` | string | First 4 digits of the material number. Undefined (DEF-13) |
| `qty_issued` | Int64 | Issued quantity, within one material |
| `n_issue_lines` | Int64 | Issue lines |
| `n_orders` | Int64 | Distinct orders. Not additive across months |
| `n_orders_with_notification` | Int64 | Distinct orders found in Notif History. Not additive across months |
| `n_repeat_lines_included` | Int64 | Rule C1 lines counted here. Always 0 in Scenario B |
| `is_zero_filled` | boolean | No issue that month, so the zeros were filled in (A-06) |

### Schema: `mart_material_demand_summary__*`

| Column | Type | Description |
| --- | --- | --- |
| `demand_scenario` | string | Demand scenario this row belongs to. Neither scenario is the true demand |
| `material_no` | string | Material number, text |
| `months_in_window` | Int64 | Months in the demand window |
| `qty_issued_total` | Int64 | Issued quantity across the window, within one material |
| `n_issue_lines` | Int64 | Issue lines |
| `n_orders` | Int64 | Distinct orders. Not additive across months |
| `months_with_issue` | Int64 | Months with at least one issue |
| `mean_monthly_qty` | Float64 | Mean over all window months, including zero months |
| `std_monthly_qty` | Float64 | Sample standard deviation over all window months |
| `max_monthly_qty` | Float64 | Highest monthly quantity |
| `mean_active_month_qty` | Float64 | Mean over months with an issue |
| `std_active_month_qty` | Float64 | Sample standard deviation over months with an issue. Blank with one such month |
| `max_line_qty` | Float64 | Highest single line quantity |
| `first_issue_date` | datetime64[ns] | Earliest posting date |
| `last_issue_date` | datetime64[ns] | Latest posting date |
| `n_lines_with_unique_location` | Int64 | Lines whose order leads to one location |
| `n_lines_with_ambiguous_location` | Int64 | Lines on orders shared across locations |
| `n_lines_at_repeated_unit_maximum` | Int64 | Lines at a repeated unit peak (A-11) |
| `flag_sparse_history` | boolean | Fewer than 3 months with an issue. Monthly statistics are weak |
| `unit` | category | Material unit. Quantities are comparable only within it |
| `mrp_type` | category | MRP type code from BoM. Meaning of Non Stock is undefined (DEF-04) |
| `material_prefix` | string | First 4 digits of the material number. Undefined (DEF-13) |

### Schema: `mart_material_demand_comparison`

| Column | Type | Description |
| --- | --- | --- |
| `material_no` | string | Material number, text |
| `unit` | category | Material unit. Quantities are comparable only within it |
| `mrp_type` | category | MRP type code from BoM. Meaning of Non Stock is undefined (DEF-04) |
| `material_prefix` | string | First 4 digits of the material number. Undefined (DEF-13) |
| `qty_scenario_a` | Int64 | Total quantity in Scenario A |
| `qty_scenario_b` | Int64 | Total quantity in Scenario B |
| `qty_diff_abs` | Int64 | Absolute difference in total quantity |
| `qty_diff_pct_of_a` | Float64 | Difference as a percentage of Scenario A |
| `qty_diff_pct_of_b` | Float64 | Difference as a percentage of Scenario B |
| `lines_scenario_a` | Int64 | Lines in Scenario A |
| `lines_scenario_b` | Int64 | Lines in Scenario B |
| `lines_diff_abs` | Int64 | Absolute difference in lines |
| `lines_diff_pct_of_a` | Float64 | Line difference as a percentage of Scenario A |
| `lines_diff_pct_of_b` | Float64 | Line difference as a percentage of Scenario B |
| `mean_monthly_qty_scenario_a` | Float64 | Mean monthly quantity in Scenario A |
| `mean_monthly_qty_scenario_b` | Float64 | Mean monthly quantity in Scenario B |
| `mean_monthly_qty_diff_abs` | Float64 | Absolute difference |
| `std_monthly_qty_scenario_a` | Float64 | Monthly standard deviation in Scenario A |
| `std_monthly_qty_scenario_b` | Float64 | Monthly standard deviation in Scenario B |
| `std_monthly_qty_diff_abs` | Float64 | Absolute difference |
| `max_monthly_qty_scenario_a` | Float64 | Highest monthly quantity in Scenario A |
| `max_monthly_qty_scenario_b` | Float64 | Highest monthly quantity in Scenario B |
| `max_monthly_qty_diff_abs` | Float64 | Absolute difference |
| `months_with_issue` | Int64 | Months with at least one issue |
| `months_with_issue_scenario_b` | Int64 | Months with an issue in Scenario B. Equals Scenario A, because copies share a date with the row kept |
| `months_with_difference` | Int64 | Months where the scenarios differ |
| `max_month_qty_diff_abs` | Int64 | Largest difference in any one month |
| `qty_copy_class_adjacent` | Int64 | Rule C1 quantity with a gap of 1 row |
| `qty_copy_class_near` | Int64 | Rule C1 quantity with a gap of 2 to 10 rows |
| `qty_copy_class_far` | Int64 | Rule C1 quantity with a gap above 10 rows |
| `impact_tier` | string | no_change, below_threshold, material (10% or more of Scenario A) or high (25% or more). Analyst thresholds (A-14) |
| `is_materially_affected` | boolean | impact_tier is material or high |
| `flag_low_line_count` | boolean | Under 5 lines in Scenario A, so the percentage is sensitive |
| `impact_reason` | string | Plain-language statement of the difference |

## 5. M2: Inventory mart

**Purpose.** One row per material, combining stock and planning values with demand and procurement summaries, as the base table for later inventory and replenishment simulation.

**Source tables.** `dim_material`, plus the M3 summaries and comparison and the M1 supplier-material tables.

**Grain and keys.** One material, keyed on `material_no`. State values come from `dim_material`, never from BoM rows.

**Transformation logic.**

1. Start from `dim_material`.
2. Add demand summaries for each scenario, and procurement summaries for each view, as separate columns with `__scenario_a`, `__scenario_b`, `__original_rows` or `__exact_distinct_rows` suffixes. Every lookup is audited and cannot add rows.
3. Add the demand impact tier.
4. Add `simulation_inputs_missing`, which names what each material lacks.

**Blanks mean no record.** Materials never issued (5,551) or never procured (6,231) hold blanks in those summaries. A blank is not a recorded zero, and a check fails if zeros appear.

**Validation.** `MART-40` to `MART-44`: one row for every material, state values equal `dim_material`, demand and procurement columns equal their sources, and blanks stay blank.

**Known limitations.**

- **Stock is undated (DEF-12).** It has no snapshot date, plant or storage location. So **no stock cover, days of supply, stockout or excess measure is built**, because each would compare an undated value with a dated flow. The raw comparisons are not shortage or excess findings, and zero stock is not a stockout.
- **Min.Qty and Max.Qty are undefined (DEF-02).** They aren't treated as reorder points or capacity.
- **Criticality is unranked (DEF-03).** Location counts per code are stored, with no score.
- **Stock can't be totalled.** It's never summed across units, and no stock value exists without confirmed prices.

### Schema: `mart_material_inventory`

| Column | Type | Description |
| --- | --- | --- |
| `material_no` | string | Material number, text |
| `material_desc_clean` | string | Material description with surrounding spaces trimmed |
| `unit` | category | Material unit. Quantities are comparable only within it |
| `mrp_type` | category | MRP type code from BoM. Meaning of Non Stock is undefined (DEF-04) |
| `material_prefix` | string | First 4 digits of the material number. Undefined (DEF-13) |
| `desc_shared_group_id` | string | Same trimmed description on several material numbers. Never merged |
| `stock` | Float64 | Stock as supplied. Undated (DEF-12) |
| `min_qty` | Int64 | Min.Qty. Undefined planning value, not capacity (DEF-02) |
| `max_qty` | Int64 | Max.Qty. Undefined planning value, not capacity (DEF-02) |
| `n_bom_rows` | Int64 | BoM source rows |
| `n_bom_locations` | Int64 | Distinct BoM locations |
| `n_fl_crit_A` | Int64 | Distinct locations with code A. No ranking applied (DEF-03) |
| `n_fl_crit_B` | Int64 | Distinct locations with code B |
| `n_fl_crit_C` | Int64 | Distinct locations with code C |
| `n_fl_crit_S` | Int64 | Distinct locations with code S |
| `n_fl_crit_null` | Int64 | Distinct locations with no code |
| `is_issued` | boolean | Appears in Movement |
| `is_procured` | boolean | Appears in PR PO |
| `stock_eq_zero` | boolean | Stock is 0. Not a stockout |
| `stock_lt_min` | boolean | Stock is below Min.Qty. Raw comparison |
| `stock_gt_max` | boolean | Stock is above Max.Qty. Raw comparison |
| `min_eq_max` | boolean | Min.Qty equals Max.Qty |
| `nonstock_with_stock` | boolean | Non Stock material holding stock (DEF-04) |
| `stockitem_min_max_zero` | boolean | Stock Item with Min.Qty and Max.Qty both 0 |
| `flag_fraction_on_count_unit` | boolean | Non-integer stock on EA, SET or ASS |
| `flag_outlier_stock` | boolean | Review flag within unit (A-10) |
| `months_with_issue` | Int64 | Months with at least one issue |
| `first_issue_date` | datetime64[ns] | Earliest posting date |
| `last_issue_date` | datetime64[ns] | Latest posting date |
| `flag_sparse_history` | boolean | Fewer than 3 months with an issue. Monthly statistics are weak |
| `n_lines_at_repeated_unit_maximum` | Int64 | Lines at a repeated unit peak (A-11) |
| `qty_issued_total__scenario_a` | Int64 | Issued quantity across the window, within one material (Scenario A) |
| `n_issue_lines__scenario_a` | Int64 | Issue lines (Scenario A) |
| `mean_monthly_qty__scenario_a` | Float64 | Mean over all window months, including zero months (Scenario A) |
| `std_monthly_qty__scenario_a` | Float64 | Sample standard deviation over all window months (Scenario A) |
| `max_monthly_qty__scenario_a` | Float64 | Highest monthly quantity (Scenario A) |
| `mean_active_month_qty__scenario_a` | Float64 | Mean over months with an issue (Scenario A) |
| `std_active_month_qty__scenario_a` | Float64 | Sample standard deviation over months with an issue. Blank with one such month (Scenario A) |
| `qty_issued_total__scenario_b` | Int64 | Issued quantity across the window, within one material (Scenario B) |
| `n_issue_lines__scenario_b` | Int64 | Issue lines (Scenario B) |
| `mean_monthly_qty__scenario_b` | Float64 | Mean over all window months, including zero months (Scenario B) |
| `std_monthly_qty__scenario_b` | Float64 | Sample standard deviation over all window months (Scenario B) |
| `max_monthly_qty__scenario_b` | Float64 | Highest monthly quantity (Scenario B) |
| `mean_active_month_qty__scenario_b` | Float64 | Mean over months with an issue (Scenario B) |
| `std_active_month_qty__scenario_b` | Float64 | Sample standard deviation over months with an issue. Blank with one such month (Scenario B) |
| `demand_qty_diff_abs` | Int64 | Absolute difference between demand scenarios |
| `demand_qty_diff_pct_of_a` | Float64 | That difference as a percentage of Scenario A |
| `demand_impact_tier` | string | Impact tier from the demand comparison |
| `demand_materially_affected` | boolean | Materially affected by the scenario choice |
| `supplier_code` | string | Supplier code, text |
| `currency` | string | Currency of the amount |
| `n_pr_lines__original_rows` | Int64 | Lines in this view (original_rows view) |
| `pr_quantity_total__original_rows` | Int64 | PR quantity summed within one material (original_rows view) |
| `pr_quantity_median__original_rows` | Float64 | Median PR quantity per line (original_rows view) |
| `promised_interval_days_median__original_rows` | Float64 | Median promised interval (original_rows view) |
| `promised_interval_days_p90__original_rows` | Float64 | 90th percentile of the promised interval (original_rows view) |
| `requested_interval_days_median__original_rows` | Float64 | Median requested interval (original_rows view) |
| `implied_unit_amount_scenario_median__original_rows` | Float64 | Median implied unit amount (A-13) (original_rows view) |
| `n_pr_lines__exact_distinct_rows` | Int64 | Lines in this view (exact_distinct_rows view) |
| `pr_quantity_total__exact_distinct_rows` | Int64 | PR quantity summed within one material (exact_distinct_rows view) |
| `pr_quantity_median__exact_distinct_rows` | Float64 | Median PR quantity per line (exact_distinct_rows view) |
| `promised_interval_days_median__exact_distinct_rows` | Float64 | Median promised interval (exact_distinct_rows view) |
| `promised_interval_days_p90__exact_distinct_rows` | Float64 | 90th percentile of the promised interval (exact_distinct_rows view) |
| `requested_interval_days_median__exact_distinct_rows` | Float64 | Median requested interval (exact_distinct_rows view) |
| `implied_unit_amount_scenario_median__exact_distinct_rows` | Float64 | Median implied unit amount (A-13) (exact_distinct_rows view) |
| `simulation_inputs_missing` | string | Inputs a later simulation lacks: demand_history, promised_interval, unit_amount, min_or_max. Blank if none. Having a value does not confirm its meaning |

## 6. Requested against issued quantity

For replenishment work, requested and issued quantities need to be broadly comparable. **On the materials in both datasets, they aren't.** The table uses `exact_distinct_rows` and Scenario A, the pairing that gives the smallest ratio.

| Unit | Materials in both | PR quantity, `exact_distinct_rows` | Issued, Scenario A | Ratio of totals | Median material ratio |
| --- | --- | --- | --- | --- | --- |
| EA | 754 | 6,924,907 | 917,658 | 7.55 | 1.67 |
| SET | 167 | 1,348 | 586 | 2.30 | 1.50 |
| KG | 22 | 7,180,004 | 792,245 | 9.06 | 3.01 |
| RL | 21 | 27,016 | 2,939 | 9.19 | 3.31 |
| LG | 19 | 26,942 | 3,023 | 8.91 | 3.09 |
| L | 18 | 234,770 | 29,255 | 8.03 | 2.77 |
| M | 10 | 1,561 | 1,290 | 1.21 | 0.59 |
| CAN | 9 | 19,427 | 2,241 | 8.67 | 3.83 |
| SHT | 6 | 24 | 33 | 0.73 | 0.74 |
| ASS | 4 | 13 | 7 | 1.86 | 1.50 |

Requests exceed issues in total by seven to nine times in most large units. On `original_rows` the gap is nearly twice that. The cause can't be confirmed from the available data or documentation (A-15). Possibilities include PR quantity not being the ordered quantity (DEF-05), stock build-up, an incomplete issue log (A-06), or how the synthetic data was generated. **A simulation that uses both flows must address this first**, because the two don't balance. No receipts or dated stock exist to reconcile them.

## 7. Readiness for simulation

**These marts are inputs. No simulation, optimisation, reorder point or safety stock has been calculated.** The approved next stage is design only: see the three `SIMULATION_*` documents.

| Simulation input | Where | Status |
| --- | --- | --- |
| Demand series, per scenario | `mart_material_demand_month__*` | Available for 1,930 materials. Issues, not proven demand |
| Demand variability | `mart_material_demand_summary__*` | Available. Weak for 1,475 sparse materials |
| Finer-grain issue events | `movement_copy_classification` | Available, with `posting_date` and scenario flags |
| Lead time | `mart_supplier_material__*`, `promised_interval_days_*` | **Proxy only.** Promised, not achieved, for 1,250 materials |
| Order size | `pr_quantity_median__*` | Available. May not be the ordered quantity (DEF-05) |
| Unit cost | `implied_unit_amount_scenario_*` | **Assumption.** Weak (Section 3) |
| Opening stock | `stock` | **Undated** (DEF-12) |
| Reorder point and maximum | `min_qty`, `max_qty` | **Undefined** (DEF-02) |
| Criticality or service level | `n_fl_crit_*` | **Unranked** (DEF-03). No service target exists |
| Holding, ordering and stockout costs | None | **Not in the data** |
| Receipts | None | **Not in the data** |

**Materials with all four checked inputs** (demand history, promised interval, unit amount, and a non-zero Min or Max):

| MRP type | Complete | Incomplete |
| --- | --- | --- |
| Stock Item | 665 | 2,991 |
| Non Stock | 0 | 3,825 |

"Complete" means the columns have values, not that their meaning is confirmed. 88 of the 665 are materially affected by the scenario choice. Each simulation result should be reported under both demand scenarios, and both PR PO views where procurement inputs are used.

## 8. Unresolved data limitations

| Item | Effect on later work | Needed |
| --- | --- | --- |
| A-05: cause of Movement copies | Two demand scenarios must be carried forward | Case owner confirmation, or a document number |
| DEF-01: cause of PR PO copies | Two procurement views must be carried forward | Case owner confirmation |
| A-06: issue log completeness | Zero months and demand levels may be wrong | Case owner confirmation |
| A-11: repeated peak values | Tails and totals may be capped or artificial | Case owner explanation |
| A-15: requests far above issues | The two flows don't balance | Definition of PR quantity, plus receipts |
| DEF-12: stock is undated | Opening stock for simulation is an assumption | Snapshot date |
| DEF-02: Min and Max undefined | Current policy can't be stated as a baseline | Definition |
| DEF-05, DEF-06: amount and promised date | Unit cost and lead time are proxies | Definitions, and receipt dates |
| DEF-03: criticality unranked | Service levels can't be set by criticality | Definition and ranking |
| A-02: data is synthetic | Findings describe this dataset, not plant performance | Organiser confirmation |
| A-03: Case 3 casebook missing | Business questions are unconfirmed. `docs/case/CALIBER_2026_Case_3_Complete_Final_Case.md` is misnamed, and its content is the Case 2 dashboard case | The real casebook |

**Also not validated:** no domain expert has reviewed the outputs. Checks show that marts reconcile to their sources and documents, not that their interpretation is right. Tested on Python 3.14.3 on macOS only.

## 9. Validation results

All 721 checks across the pipeline pass, 126 of them specific to marts, and 309 automated tests pass in both the project environment and a clean install. Of those tests, 31 damage mart data to confirm the checks catch it: a deleted record, a copy kept in Scenario B, Scenario A reused as B, zeros outside the window, and a multiplied join, for example. No mart test failed on its first run. All results are in `outputs/tables/validation_results.csv`. Expected values for marts are in `data/reference/expected_values_marts.json`. Each entry names its source, and two (tier counts and the 665) were recorded at this build because no document states them.

**Limit of `MART-03`.** It checks column names against a list. It can't detect an unapproved rule under an innocent name.
