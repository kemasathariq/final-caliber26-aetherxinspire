# INSpire Data Intelligence Specification

**Status:** DRAFT v0.1. The foundation is IMPLEMENTED and accepted (M1 to M3, 750 of 750 checks pass, 354 tests pass). This document states how INSpire uses it. It adds no transformation. Full detail: `docs/analysis/CALIBER_DATA_PREPARATION_SPECIFICATION.md`, `DATA_MART_REPORT.md`, `DATA_QUALITY_REPORT.md`, `ASSUMPTIONS_REGISTER.md`.

## 1. Six datasets

| Dataset | Rows | Grain | Role in INSpire | Key caveat |
| --- | --- | --- | --- | --- |
| BoM | 20,653 | Material on a functional location | Material master, stock, recorded Min/Max, location links | Stock, Min, Max are material-level and repeat across rows. Never sum across rows. Stock undated |
| Movement Material | 17,518 | Issue line | Observed consumption (demand proxy) | 863 exact copy lines. Two scenarios. No document number |
| Notif History | 5,795 | Notification | Maintenance context | Not failures (DEF-09). May 2025 backlog of 1,463 |
| FuncLoc list | 14,484 | Functional location | Criticality context | A, B, C, S unranked |
| PR PO | 11,609 | PR item and PO item | Lead-time proxy, order quantity, supplier, spend | 5,420 exact copies, two views. Promised dates only |
| Mitem and Mplan | 10,153 | Maintenance item | Planned work context | Cycle meaning and start anchor unconfirmed |

## 2. Relationships

- Functional Location links are clean. Every location in BoM, Notif History and Mitem and Mplan exists in the FuncLoc list.
- Material links run one way. All 1,250 procured and all 1,930 issued materials exist in the BoM. BoM has 7,481 materials.
- Order links are weak: 20.5 percent of Movement orders appear in Notif History, and 22.6 percent of linked issued materials are on that location's BoM.
- 52 orders sit on two notifications. Location attribution is `ambiguous` and never allocated.

## 3. Material-level information model

One row per material (`mart_material_inventory`, 7,481 rows). Groups of fields:

| Group | Fields | Source |
| --- | --- | --- |
| Identity and state | `material_no`, `unit`, `mrp_type`, `stock`, `min_qty`, `max_qty`, state flags | BoM via `dim_material` |
| Equipment context | `n_bom_locations`, `n_fl_crit_A/B/C/S/null` | BoM, FuncLoc |
| Demand, per scenario | `qty_issued_total`, `n_issue_lines`, monthly mean, std, max, `months_with_issue`, `flag_sparse_history` | M3, suffixes `__scenario_a`, `__scenario_b` |
| Scenario sensitivity | `demand_qty_diff_pct_of_a`, `demand_impact_tier`, `demand_materially_affected` | M3 comparison |
| Procurement, per view | supplier, currency, PR line count, PR quantity median, promised interval median and p90, implied unit amount | M1, suffixes `__original_rows`, `__exact_distinct_rows` |
| Readiness | `simulation_inputs_missing` | M2 |

Blank means no record. A blank is never a recorded zero.

## 4. Equipment, maintenance and procurement context

| Context | Use | Never |
| --- | --- | --- |
| Equipment (criticality, location count) | Show with each recommendation, group in views | Rank or weight by A, B, C, S (DEF-03) |
| Maintenance (notifications, plans) | Explain where an issue linked to work, show planned-work density per location | Convert a notification or plan into material demand without a material relationship |
| Procurement | Lead-time proxy, order quantity reference, supplier, spend per currency and view | Call a promised interval an actual lead time, or sum across currencies |

## 5. Data-quality controls (IMPLEMENTED)

Raw workbooks are checksummed and immutable. Every join is audited and cannot multiply rows. Check functions return PASS, FAIL or WARN, with expected-value files in `data/reference/`. 85 failure-detection tests damage data to prove checks can fail. Rebuilds are byte-identical across 110 tracked files. Results: `outputs/tables/validation_results.csv`.

## 6. Missing information

Receipts, stock date, storage location, order quantity and unit price, criticality meaning, Min/Max meaning, failure codes and downtime, cost parameters, supplier alternatives. Full list in `DATA_LIMITATIONS_AND_ASSUMPTIONS.md`.

## 7. Confidence and eligibility rules

| Rule | Condition | Effect |
| --- | --- | --- |
| Tier T3 | Stock Item, demand history, promised interval, unit amount, non-zero Min or Max | Policy simulation allowed |
| Tier T2 | Issued in window, not T3 | Demand-based descriptive output |
| Tier T1 | Never issued | State-only output |
| Resampling gate | At least 6 active months for demand, 10 distinct lead observations (pending D-03) | Below gate: deterministic or configurable scenario only |
| Scenario sensitivity | `demand_materially_affected` true (88 of 665) | Confidence one level lower and a visible divergence flag |
| Unit | Per material | Quantities are never combined across units |
| Currency | Per currency | Never combined without a verified rate. Non-IDR rows: 98 original, 51 distinct |

## 8. Preservation commitments

M1 to M3 are not modified. New analytical tables (tier table, demand classification, engine output) are added beside them, validated the same way, and never overwrite a mart. No silent deduplication anywhere.
