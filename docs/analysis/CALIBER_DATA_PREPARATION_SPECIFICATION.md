# CALIBER 2026 Data Preparation Specification

**Version:** 0.1 (draft for approval)
**Date:** 2026-11-04
**Companion document:** CALIBER_DATA_DICTIONARY.md (column-level definitions; Section 1 of this specification)
**Inputs:** PR PO.xlsx, Movement Material.xlsx, Notif History.xlsx, Mitem & Mplan.xlsx, BoM.xlsx, FuncLoc list.xlsx
**Status:** Specification only. Nothing in this document has been executed. All counts quoted come from read-only inspection of the raw files on 2026-11-04 and serve as expected values for validation tests.

**Data status.** The case document "Data Context & Relationship Diagram.pdf" states that all six workbooks are synthetic (dummy) data generated for the Caliber 2026 Hackathon. Every output of this pipeline must carry that label. No prepared table may be presented as verified operational performance.

---

## Contents

0. Principles and architecture
1. Data dictionary (reference)
2. Data quality treatment by issue type
3. Dataset-specific cleaning strategy
4. Data integration design
5. Analytical data mart design
6. Cleaning decision register
7. Validation test suite
8. Approval checklist
Appendix A. Cycle description mapping
Appendix B. Flag catalogue
Appendix C. Output files and naming
Appendix D. Correction to the Analytical Discovery Report

---

## 0. Principles and architecture

### 0.1 Ten rules that every step must obey

1. **Raw is immutable.** Source workbooks are never edited. A SHA-256 checksum of each file is recorded at load and re-checked at every run.
2. **No row is deleted.** Rows are only flagged. "Distinct" views are filters over flagged tables, never physical deletions.
3. **Every row is traceable.** Each staged row carries `source_file`, `source_row` (Excel row number) and `row_hash`.
4. **Originals are kept beside derived values.** A trimmed description is a new column; the original column stays.
5. **No fabricated values.** No imputation of nulls, no invented dates, no default criticality, no assumed exchange rate.
6. **No unit mixing.** Quantities are added only within one material, or within one unit when materials differ.
7. **No currency mixing.** Amounts are added only within one currency unless a sourced exchange-rate table is supplied.
8. **Promised is not actual.** Dates from PR PO are requested or promised dates. Derived intervals are named `promised_*` or `requested_*`.
9. **Undefined codes stay codes.** Categories without a business definition are stored as unordered codes. No ranking is applied until approved.
10. **Every rule is versioned.** Each derived table records the specification version and the policy parameters used.

### 0.2 Layered architecture

| Layer | Name | Content | Rows removed? | Typical operations |
| --- | --- | --- | --- | --- |
| L0 | Raw | Original workbooks, read-only, with checksums | Never | None |
| L1 | Staged | One table per workbook. Standard column names, recommended types, lineage columns, trimmed text copies | Never | Type casting, renaming, whitespace trimming into new columns, lineage |
| L2 | Conformed | Flagged tables, duplicate groups, derived fields, dimension tables, bridge tables | Never (distinct views are filters) | Flags, duplicate grouping, derived intervals, mapping tables, referential checks |
| L3 | Marts | Analysis-ready datasets at declared grains | Filtered by documented policy only | Aggregation, policy-based filtering, joins at matching grain |

### 0.3 Lineage columns added in L1

| Column | Content |
| --- | --- |
| `source_file` | Original file name |
| `source_sheet` | Sheet name ("Data") |
| `source_row` | Excel row number (pandas index + 2, because row 1 is the header) |
| `row_hash` | SHA-256 of all original cell values, joined as text in source column order |
| `load_ts` | Load timestamp |
| `spec_version` | Version of this specification |

### 0.4 Global parameters

| Parameter | Proposed value | Status | Reason |
| --- | --- | --- | --- |
| `DATA_CUTOFF` | 2026-09-30 | ASSUMPTION, needs approval | Latest Posting Date and latest Notification Date in the files (OBSERVED). Used to flag "future" dates and to censor open notifications. |
| `PRPO_DUP_POLICY` | `distinct` | Needs approval (DEF-01) | See Section 3.1. Alternative: `raw`. |
| `MOVE_DUP_POLICY` | `raw` | Needs approval | See Section 3.3. Alternative: `distinct`. |
| `BOM_DUP_POLICY` | `distinct` | Needs approval | See Section 3.2. |
| `IDR_ONLY_SPEND` | `true` | Safe default | No exchange rates supplied. |
| `FX_TABLE` | none | Optional input | Only used if a sourced rate table is supplied (schema in Section 2.7). |
| `OUTLIER_METHOD` | robust z (MAD) within material, threshold 3.5; IQR fence 3.0 within unit for materials with fewer than 5 records | Needs approval | Flag only; nothing removed. |

Every mart records the parameter values it was built with in a metadata file.

---

## 1. Data dictionary (reference)

The full column-level dictionary (58 columns, business meaning with evidence label, current and recommended type, class, role, observed profile, issues and treatment) is in **CALIBER_DATA_DICTIONARY.md**. This specification refers to columns by their standard names (dictionary Section 7).

---

## 2. Data quality treatment by issue type

Each issue type below lists: how to detect it, how to investigate it, whether it can be corrected automatically, whether it is preserved and flagged, and whether a business definition is required. Expected counts are raw observations from 2026-11-04 and become test values in Section 7.

### 2.1 Exact duplicates

| Item | Specification |
| --- | --- |
| Detect | Group on all original columns (exclude lineage columns). `dup_count` = group size; `dup_rank` = order by `source_row` within the group; `is_dup_extra` = `dup_rank > 1`. |
| Expected | PR PO 5,420 extra rows (6,189 groups: 2,589 x1, 2,300 x2, 780 x3, 520 x4). BoM 230. Movement 863. Notif, Mitem, FuncLoc 0. |
| Investigate | (a) Does the business key become unique among `dup_rank = 1` rows? (b) Do duplicates cluster by date, supplier, PR-Type or purchasing group? (c) Is copy count related to any other table (for example BoM rows per material; already tested for PR PO: not related, match 10%, correlation -0.008)? |
| Automatic correction | No. Distinct views are produced automatically, but which view a mart uses is a policy decision. |
| Preserve and flag | Yes. All rows kept in L1 and L2. |
| Business definition | Yes for PR PO (DEF-01). Movement: no material document number exists, so the question cannot be settled from the data. |

### 2.2 Partial duplicates

| Item | Specification |
| --- | --- |
| Detect | Repeated business keys with differing non-key values. PR PO: (PR, PR-Item) and (PO, PO-Item) among distinct rows. BoM: (functional_location, material_no) among distinct rows. Movement: (posting_date, material_no, order_no) groups. Notif: (functional_location, description, notification_date). Mitem: (maintenance_plan, functional_location, item_text). |
| Expected | PR PO 0 key conflicts after exact duplicates. BoM 0. Movement 1,074 groups with more than one row, 297 of them with different quantities. Notif 8 rows repeat location, description and date; 1,200 rows repeat location and description on other dates. Mitem 0. |
| Investigate | For Movement, compare quantities within groups; for Notif, compare order numbers and status within repeated pairs. |
| Automatic correction | No. Different quantities on the same day and order can be real separate issues. Repeated notification texts on one location are expected for recurring work. |
| Preserve and flag | Yes: `is_partial_dup_group`, `partial_dup_group_id`. |
| Business definition | No for flagging; yes if a merge rule is ever proposed. |

### 2.3 Missing values

| Item | Specification |
| --- | --- |
| Detect | Null count per column. |
| Expected | Only three columns contain nulls: Notif Order 553 (all on In Progress notifications); Notif Completion by Date 1,305 (exactly the In Progress notifications); FuncLoc Criticallity 33 (exactly the SITE rows). All other columns: 0 nulls. |
| Investigate | Confirm each null set coincides with its structural explanation (status, SITE prefix). Any null outside these patterns is a new issue. |
| Automatic correction | Never impute. |
| Preserve and flag | Yes: `order_missing`, `is_open` (status In Progress), `criticality_missing` with `criticality_missing_reason = 'system_level_row'`. |
| Business definition | Not for these three cases (structural meaning is observed). Required if new nulls appear. |

### 2.4 Invalid or inconsistent dates

| Check | Rule | Expected raw count | Treatment |
| --- | --- | --- | --- |
| D1 | PR-Delivery Date < PR-Date | 630 | Flag `flag_req_before_pr`. Keep. Exclude from requested-interval statistics by default, report separately. |
| D2 | PO-Delivery Date < PR-Date | 6 | Flag `flag_promise_before_pr`. Keep. Exclude from promised-interval statistics by default. |
| D3 | PO-Delivery Date < PR-Delivery Date | 4,232 | Not invalid (promise earlier than request). Derive `promise_gap_days`; no flag. |
| D4 | PR-Delivery or PO-Delivery > DATA_CUTOFF | Count at build | Flag `flag_future_date`. These are open promises; the interval is still valid as a promise. |
| D5 | Required Start < Notification Date | 370 | Flag `flag_reqstart_before_notif`. Keep. |
| D6 | Required End < Required Start | 0 | Test must stay 0. |
| D7 | Completion by Date < Notification Date | 0 | Test must stay 0. |
| D8 | Completion by Date > Required End | 2,028 | Not invalid. Derive `completed_late` (boolean). |
| D9 | Created On ≠ Notification Date | about 61 (1.1% of 5,795) | Flag `flag_created_differs`. Keep both. |
| D10 | Start of cycle > report date (2026-11-04) | 344 | Flag `flag_future_cycle_start`. |
| D11 | Any date with a time component | 0 | Test must stay 0. |
| D12 | Extreme intervals | Intervals beyond the 99.5th percentile of their distribution | Flag `flag_extreme_interval`. Keep. |

Automatic correction: none. Business definition: needed to decide whether D1 and D5 rows are data errors (DEF-06, DEF-14).

### 2.5 Inconsistent categorical values

| Item | Specification |
| --- | --- |
| Detect | Distinct values per categorical column; case-insensitive and whitespace-insensitive comparison; known synonym lists. |
| Expected | Cycle Descriptions: 28 spellings, of which "YEARLY", "Yearly", "1 YEARLY" and possibly "12 MONTHLY" describe the same interval; "Monthly"/"1 MONTHLY"; "Weekly"/"1 WEEKLY"; "2 WEEK"/"2 WEEKLY". Maint. item text: near-synonyms such as "Final Element Inspection; Control Valve" and "Final Element Inspection; CV". No case or whitespace variants in PR-Type, Purchasing Group, Notification Type, Priority, Status, MRP Type, Unit, Currency, criticality. |
| Investigate | Produce a value-frequency table per column for review. |
| Automatic correction | Case and whitespace normalisation into a new column: yes. Synonym mapping: no, only through an approved mapping table (Appendix A for cycles; a proposed synonym map for item texts). |
| Preserve and flag | Original values always kept. |
| Business definition | Yes for cycle mapping (DEF-10) and for item-text synonyms. |

### 2.6 Inconsistent units

| Item | Specification |
| --- | --- |
| Detect | Per material, count distinct units across PR PO, Movement and BoM. |
| Expected | 0 materials with more than one unit within or across tables (OBSERVED). 10 unit codes overall. |
| Investigate | If any material shows two units in future data, stop and raise. |
| Automatic correction | None; no conversion factors exist. |
| Preserve and flag | Unit stored on every quantity row. A material-level `unit` in `dim_material` is the reference; any mismatch sets `flag_unit_mismatch`. |
| Business definition | Required for meanings of LG, RL, ASS, SHT (DEF-15), not for preparation. |
| Aggregation rule | Quantity measures are summed only when grouped by `material_no`. Cross-material totals use counts (issue lines, PR lines, orders) or are grouped by `unit`. |

### 2.7 Currency differences

| Item | Specification |
| --- | --- |
| Detect | Distinct PO-Currency values; currency per supplier. |
| Expected | IDR 11,511, JPY 41, USD 35, EUR 20, SGD 2 raw rows. Distinct rows: IDR 6,138, JPY 21, USD 17, EUR 11, SGD 2. Each non-IDR currency belongs to exactly one foreign supplier. |
| Investigate | Confirm one currency per supplier and per material. |
| Automatic correction | None. |
| Preserve and flag | `amount` stays in `currency`. Spend marts default to IDR rows only (`IDR_ONLY_SPEND = true`), with non-IDR rows reported in a separate table. |
| Optional conversion | Only if a rate table is supplied with columns `currency`, `rate_date`, `rate_to_idr`, `source_title`, `source_url`, `retrieved_on`. Converted values go to `amount_idr_scenario`, labelled as converted with the source named. Rates are never typed from memory. |
| Business definition | Required for whether amounts include tax (DEF-05). |

### 2.8 Numerical outliers

| Item | Specification |
| --- | --- |
| Detect | Within each material (unit is constant): robust z = 0.6745 x (value - median) / MAD; flag if absolute value > 3.5 (Iglewicz and Hoaglin rule). For materials with fewer than 5 records or MAD = 0: within unit, flag values above Q3 + 3 x IQR. Apply to PR-Quantity, implied unit amount (per material and currency), Movement Quantity, BoM Stock, Installed Qty, and each derived interval. |
| Expected | Heavy right tails observed (PR-Quantity up to 77,913 KG; Movement Quantity up to 23,135 KG; Stock up to 95,432). Exact flag counts are produced at build. |
| Investigate | Review the top 20 flagged values per measure against unit and description (for example bulk KG materials versus EA items). |
| Automatic correction | Never. No capping, no winsorising in preparation. |
| Preserve and flag | `flag_outlier_<measure>` plus `outlier_method`. EDA decides whether to use robust statistics. |
| Business definition | No for flagging. |

Special numeric anomalies: BoM Stock = 0.5 on a material in unit EA (material 4300057364) and 89 non-integer Installed Qty values. Flag `flag_fraction_on_count_unit` where unit is EA, SET or ASS and the value is not a whole number.

### 2.9 Invalid identifiers

| Identifier | Rule | Expected failures |
| --- | --- | --- |
| Purchase Requisition, Purchase Order, PR-Material, Material Number, Material No | 10 digits | 0 |
| PO-Supplier Code | 6 digits | 0 |
| Order (Movement, Notif), Notification, Maintenance Plan | 12 digits | 0 |
| Maintenance Item | 5 or 6 digits | 0 |
| PR-Item, PO-Item | Multiple of 10 | 0 |
| Notification prefix to type | 101=N1, 102=N2, 103=N3, 106=N6 | 0 |
| PR prefix to PR-Type | 10=PR01, 12=PR03, 13=PR04, 14=PR05, 15=PR06, 18=PR09, 19=PR10 | 0 |
| Functional Location | Non-empty, no leading or trailing spaces | 0 |

Treatment: cast all identifiers to string (A). Notif Order is stored as float with nulls; convert with integer conversion first so that "201000000108.0" never appears (A). Failures, if any, are flagged `flag_invalid_id` and kept.

### 2.10 Inconsistent descriptions

| Check | Expected | Treatment |
| --- | --- | --- |
| Leading or trailing spaces | PR PO 191 rows, Movement 128, BoM 438 | Trim into `*_desc_clean` (A). Keep original. |
| Same material, different description | 0 within and across tables | Test must stay 0. |
| Same description, different material numbers | PR PO 39 descriptions (36 bought from different suppliers); BoM 133 descriptions over 597 materials (counts to be re-run after trimming) | Flag `desc_shared_group_id`. Never merge material numbers (C). Equivalence needs engineering confirmation. |
| Free-text notification descriptions | 4.8% start with a bracketed reference code | Extract into `desc_ref_code` (B: pattern-based, verify on a sample). |

### 2.11 Referential integrity

| FK check | Expected child keys missing in parent | Expected parent keys unused | Treatment |
| --- | --- | --- | --- |
| BoM.functional_location → FuncLoc | 0 of 4,516 | 9,968 of 14,484 | Test. Flag `fl_has_bom` on FuncLoc. |
| Notif.functional_location → FuncLoc | 0 of 2,219 | 12,265 | Test. |
| Mitem.functional_location → FuncLoc | 0 of 5,785 | 8,699 | Test. |
| Movement.material_no → dim_material (BoM) | 0 of 1,930 | 5,551 materials never issued | Test. Flag `is_issued`. |
| PR PO.material_no → dim_material (BoM) | 0 of 1,250 | 6,231 materials never procured | Test. Flag `is_procured`. |
| Movement.order_no → Notif.order_no | 3,881 of 4,884 movement orders have no notification | 4,187 of 5,190 notification orders have no movement | Keep all. Flags `has_notification`, `has_issue`. |
| Mitem.criticality = FuncLoc.criticality | 0 mismatches | | Test (redundancy). |
| Mitem.fl_desc = FuncLoc.fl_desc | 0 mismatches | | Test (redundancy). |

Orphans are never dropped. Each unmatched record carries a flag so that analyses can report coverage.

---

## 3. Dataset-specific cleaning strategy

Each subsection lists ordered steps. Step numbers become function names in the Python implementation (for example `prpo_s03_flag_duplicates`).

### 3.1 PR PO

**Business key:** (purchase_requisition, pr_item). Secondary key: (purchase_order, po_item).

| Step | Action | Class |
| --- | --- | --- |
| S01 | Load raw, record checksum, add lineage columns. | A |
| S02 | Rename to standard names; cast identifiers to string, quantities to `Int64`, amounts to `Float64`, codes to `category`. | A |
| S03 | Add `material_desc_clean` (trimmed). | A |
| S04 | Exact duplicate grouping: `dup_group_id`, `dup_count`, `dup_rank`, `is_dup_extra`. Expected 5,420 extra rows. | A (flagging) |
| S05 | Test that (purchase_requisition, pr_item) and (purchase_order, po_item) are unique among `dup_rank = 1` rows. Expected: both unique, 6,189 rows. If this fails, stop: the distinct policy is no longer justified. | A (test) |
| S06 | Apply `PRPO_DUP_POLICY` to create `prpo_line` (distinct: `dup_rank = 1`; raw: all rows). Default `distinct`. Keep `dup_count` as a column so the raw total can always be recovered. | B |
| S07 | Validate supplier mapping: one name per supplier code (expected 124 to 124); one supplier per PO (expected max 1); one supplier per material (expected 1,250 materials, all with one supplier). Build `dim_supplier` (supplier_code, supplier_name, currency set, is_foreign = currency not IDR). | A |
| S08 | Validate material mapping: FK to dim_material (expected 0 missing); unit equals dim_material unit (expected 0 mismatches); description equals after trimming (expected 0 mismatches). | A (test) |
| S09 | Derive intervals in days: `requested_lead_days` = pr_delivery_date - pr_date; `promised_lead_days` = po_delivery_date - pr_date; `promise_gap_days` = po_delivery_date - pr_delivery_date. | A (arithmetic); naming fixed by rule 8 |
| S10 | Date flags D1, D2, D4, D12 (Section 2.4). Recount on distinct rows and record both raw and distinct counts. | A (flagging) |
| S11 | Currency: keep `amount` with `currency`; set `in_idr_scope` = currency is IDR. No conversion. | A |
| S12 | Derive `implied_unit_amount` = amount / pr_quantity with metadata note "assumes PO-Item Amount is the line total for PR-Quantity" (DEF-05). | B |
| S13 | Outlier flags on pr_quantity (within material), implied_unit_amount (within material and currency) and the three intervals. | A (flagging) |
| S14 | Derive labels: `pr_prefix`, `po_prefix`, `pr_month`. Test PR prefix to PR-Type rule. | A |
| S15 | Flag singleton or rare categories (PR09: 1 row; purchasing groups with fewer than 30 distinct rows) as `rare_category`. | A |

**Why the distinct policy is proposed for PR PO but not for Movement.** In PR PO each repeated row repeats a business key that should identify one document line: a requisition item cannot legitimately exist twice with identical content. After removing exact copies, both the PR item key and the PO item key become unique. Movement has no document key, so two identical issue lines cannot be shown to be the same event.

**Risk.** If the repeated rows are real repeat lines (DEF-01 answered "real"), the distinct policy understates quantity and spend by roughly half. Mitigation: every mart keeps `dup_count`, and a sensitivity output reports key totals under both policies.

**Quantity and amount interpretation.** PR PO has no PO quantity. Any per-unit figure assumes the PO line buys the PR quantity. This is an assumption (B) and must be stated wherever unit amounts appear.

### 3.2 BoM

**Grain separation.** BoM mixes two grains. The conformed layer splits it into two tables and never sums material-level values from the original rows.

| Table | Grain | Columns |
| --- | --- | --- |
| `bridge_fl_material` | One functional location and material pair | functional_location, material_no, installed_qty, lineage, flags |
| `dim_material` | One material | material_no, material_desc, material_desc_clean, unit, min_qty, max_qty, stock, mrp_type, material_prefix, n_bom_locations, flags |

| Step | Action | Class |
| --- | --- | --- |
| S01 | Load, lineage, rename `Functional Loc.` to `functional_location`, cast types. | A |
| S02 | Trim descriptions into `material_desc_clean`. | A |
| S03 | Exact duplicate grouping. Expected 230 extra rows. Test that (functional_location, material_no) is unique among `dup_rank = 1`. | A |
| S04 | Apply `BOM_DUP_POLICY = distinct` to build `bridge_fl_material` (expected 20,423 rows). Exact duplicates carry identical installed_qty, so the choice affects only pair counts, not material attributes. | B (low risk) |
| S05 | Test that material_desc, unit, min_qty, max_qty, stock and mrp_type have exactly one value per material. Expected 0 materials violating. If any violate, stop and raise: the material-level interpretation would be wrong. | A (test) |
| S06 | Build `dim_material` from one row per material (expected 7,481 rows; 3,656 Stock Item, 3,825 Non Stock). | A, conditional on S05 passing |
| S07 | Derive `n_bom_locations` and counts of locations per criticality code (`n_fl_crit_A`, `n_fl_crit_B`, `n_fl_crit_C`, `n_fl_crit_S`, `n_fl_crit_null`). No "highest criticality" field, because no ranking is approved (DEF-03). | A |
| S08 | Stock status, kept as raw comparisons, not judgements: `stock_eq_zero`, `stock_lt_min`, `stock_gt_max`, `min_eq_max`. A combined `stock_status` label is created only after DEF-02. | A for comparisons; D for the label |
| S09 | MRP flags: `nonstock_with_stock` (expected 1,683 materials), `stockitem_min_max_zero` (expected 29). | A (flagging) |
| S10 | Numeric anomalies: `flag_fraction_on_count_unit` for stock and installed_qty; outlier flags on stock within unit. | A (flagging) |
| S11 | Flag `desc_shared_group_id` for descriptions shared by several material numbers (after trimming). | A (flagging); merging is C |

**What Min.Qty and Max.Qty are not.** They are planning parameters. They are not warehouse or storage capacity and must not be used as capacity constraints.

**Zero stock is not a stockout.** A material with zero stock is reported as `stock_eq_zero`. Calling it a stockout requires a business rule (for example, a Stock Item with open demand), which is not available.

### 3.3 Movement Material

| Step | Action | Class |
| --- | --- | --- |
| S01 | Load, lineage, rename, cast types (order_no and material_no to string). | A |
| S02 | Trim descriptions. | A |
| S03 | Validate Movement Type is the single value "Issue". If other values appear, stop: sign conventions would need definition. | A (test) |
| S04 | Exact duplicate grouping (expected 863 extra rows) and partial duplicate grouping on (posting_date, material_no, order_no) (expected 1,074 groups; 297 with different quantities). | A (flagging) |
| S05 | Apply `MOVE_DUP_POLICY = raw` (all rows count as issues). Produce a sensitivity version with `distinct`. | C (preserve and flag) |
| S06 | Validate FK to dim_material (expected 0 missing) and unit equality (expected 0 mismatches). | A (test) |
| S07 | Derive `order_prefix`, `posting_month` (first day of month), `posting_week`. | A |
| S08 | Flag `has_notification` by joining to the distinct set of Notif order numbers (expected 1,003 of 4,884 orders; 2,791 of 17,518 rows). | A |
| S09 | Outlier flags on quantity within material. | A (flagging) |

**Demand aggregation rules**

1. Quantity is summed only within one material (its unit is fixed).
2. The base demand table is material by calendar month, covering every month from 2025-05 to 2026-09 for every issued material, with zeros where no issue occurred. Zero-filling is valid only inside this observed window and only under the assumption that the Movement file is the complete issue log for the period (B).
3. Materials never issued (5,551 in dim_material) are not zero-filled into the demand table; their status is carried in `dim_material.is_issued = false`, so the demand table does not swell with 5,551 x 17 zero rows of uncertain meaning.
4. Each demand row stores: `qty_issued`, `n_issue_lines`, `n_orders`, `n_orders_with_notification`, and the duplicate policy used.
5. Cross-material totals use `n_issue_lines` or `n_orders`, never quantity.
6. Issues are demand events, not receipts: the table cannot be used to rebuild stock balances.

### 3.4 Notif History

| Step | Action | Class |
| --- | --- | --- |
| S01 | Load, lineage, rename, cast types. Convert Order from float to nullable integer, then to string. | A |
| S02 | Validate Notification uniqueness (expected 5,795) and prefix-to-type rule (expected 0 failures). | A (test) |
| S03 | Validate status consistency: Complete ⇔ completion date present (expected 4,490); In Progress ⇔ completion date null (expected 1,305). | A (test) |
| S04 | Flags: `order_missing` (expected 553, all In Progress), `is_open`, `flag_reqstart_before_notif` (370), `flag_created_differs`, `completed_late` (2,028), `flag_future_date` for required dates after DATA_CUTOFF. | A (flagging) |
| S05 | Derived durations: `days_to_complete` = completion - notification_date for completed rows; `days_open_at_cutoff` = DATA_CUTOFF - notification_date for open rows; `is_censored` = is_open. Never fill completion dates. | A (arithmetic); censoring rule B (depends on DATA_CUTOFF) |
| S06 | Required window: `required_window_days` = required_end - required_start; `days_late_vs_required` = completion - required_end for completed rows. | A |
| S07 | Order relationships: build `bridge_order_notification` (order_no, notification) from non-null orders (expected 5,242 rows, 5,190 distinct orders); flag `order_shared` for the 52 orders on two or more notifications; record whether shared orders point to the same functional location (`shared_order_same_fl`). | A |
| S08 | Join FuncLoc attributes: criticality, fl_prefix, `is_system_level` (expected 394 notifications on SITE rows). | A |
| S09 | Priority stored as unordered category. A `priority_rank` column (Low 1, Medium 2, High 3, Emergency 4) is created only after approval. | D until approved |
| S10 | Text fields: `description_clean` (trimmed), `desc_ref_code` (bracketed prefix), `desc_first_word` (upper-cased first word) as a raw feature. Classification into failure or routine work belongs to EDA. | B |
| S11 | `first_month_flag` for notifications in 2025-05 (1,463 records), to allow sensitivity checks on a possible backlog load. | A (flagging) |

### 3.5 Mitem & Mplan

| Step | Action | Class |
| --- | --- | --- |
| S01 | Load, lineage, rename, cast types (maintenance_item and maintenance_plan to string; plan_priority to category). | A |
| S02 | Validate Maintenance Item uniqueness (expected 10,153). | A (test) |
| S03 | Validate redundancy: ABC Indicator equals FuncLoc criticality and FunctLocDescrip. equals FuncLoc description (expected 0 mismatches each). Marts use the FuncLoc master values. | A (test) |
| S04 | Cycle mapping: join `cycle_desc` to the approved mapping table (Appendix A) to obtain `interval_value` and `interval_unit` (WEEK, MONTH, YEAR). Unmapped values set `flag_cycle_unmapped` and stop the build. | B (needs DEF-10) |
| S05 | Derived comparison field `interval_days_approx` = value x 7, 30.4375 or 365.25. Used only for sorting and comparing intervals, never for date projection. | B |
| S06 | Start of cycle: flag `flag_future_cycle_start` (expected 344 after 2026-11-04); flag `start_day_is_first` (expected 7,718). | A (flagging) |
| S07 | Planning horizon: due-date projection (calendar offsets of interval_value interval_unit from start_of_cycle, using calendar arithmetic, not approximate days) is specified but **not executed** until DEF-11 confirms what Start of cycle means. Without completion history, projected dates are planned dates, not performed work. | D |
| S08 | Item text: keep `item_text`; add `item_text_group` through a reviewed synonym map (for example "CV" = "Control Valve"). | B |
| S09 | Plan structure: `n_items_in_plan`, `n_fl_in_plan`, `plan_multi_fl` (expected 710 plans). | A |

**Temporal interpretation.** Start of cycle runs from 2015-09-01 to 2029-12-12, far beyond the 17-month event window. Plan data describes intended work; it is not evidence that work or part consumption happened.

### 3.6 FuncLoc list

| Step | Action | Class |
| --- | --- | --- |
| S01 | Load, lineage, rename, cast. | A |
| S02 | Validate uniqueness (expected 14,484) and no leading or trailing spaces in the code. | A (test) |
| S03 | Criticality: store as unordered category with codes A, B, C, S. Keep 33 nulls. Add `criticality_missing` and `criticality_missing_reason = 'system_level_row'` where the code starts with SITE. No ranking, no default value. | C for nulls; D for ranking |
| S04 | `fl_desc_clean` (trimmed). Generic descriptions such as TEMPERATURE (826 rows) stay as they are; descriptions are labels, not identifiers. | A |
| S05 | Hierarchy candidates, as labels only: `fl_prefix` (text before the first underscore: PX, PY, UT, SITE); `is_system_level` (prefix SITE); `fl_body` (text after the first underscore); `tag_class_candidate` (letters at the start of fl_body, for example HE, PP, TEL, LCV, PGI); `is_line_pattern` (fl_body starts with a pipe size such as 1-1/2-, 3/4-, 20-). | B (pattern rules must be checked on samples) |
| S06 | Parent links are **not** inferred. The SITE rows (for example SITE_PX_S01 "CRACKED GAS COMPRESSION SYSTEM") have no stored link to the equipment below them. | D |
| S07 | Usage flags: `fl_has_bom`, `fl_has_notification`, `fl_has_plan`, and `fl_in_all_three` (expected 894). | A |

---

## 4. Data integration design

### 4.1 Integration principles

1. Join only at matching grain. Aggregate the many side first when the other side is a different grain.
2. Material-level attributes come from `dim_material` only (one row per material), never from BoM rows.
3. Every join records match counts and row counts before and after. A join that changes the row count of the left table unexpectedly fails the build.
4. A shared column name is not a reason to join. Each relationship below is justified by the diagram or by observed key behaviour.

### 4.2 Relationship register

| ID | Source (parent) | Destination (child) | Join keys | Expected cardinality | Expected unmatched | Row multiplication risk | Validation rule | Safe for analysis? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R1 | dim_functional_location | bridge_fl_material | functional_location | 1 : N | Child 0; parent unused 9,968 | None when looking up parent attributes onto child rows | Child row count unchanged after lookup; 0 unmatched | Yes |
| R2 | dim_functional_location | fact_notification | functional_location | 1 : N | Child 0; parent unused 12,265 | None as a lookup | Row count unchanged; 0 unmatched | Yes |
| R3 | dim_functional_location | fact_plan_item | functional_location | 1 : N | Child 0; parent unused 8,699 | None as a lookup | Row count unchanged; 0 unmatched | Yes |
| R4 | dim_material | fact_issue (Movement) | material_no | 1 : N | Child 0; materials never issued 5,551 | None if dim_material is one row per material. A naive join of raw BoM rows to Movement produces 615,146 rows from 17,518 issues (about 35 times). | Assert dim_material key unique before join; fact row count unchanged | Yes, through dim_material only |
| R5 | dim_material | prpo_line | material_no | 1 : N | Child 0; materials never procured 6,231 | Naive raw BoM to PR PO join produces 293,658 rows from 11,609 (about 25 times). | Same as R4 | Yes, through dim_material only |
| R6 | dim_supplier | prpo_line | supplier_code | 1 : N | 0 | None | Row count unchanged | Yes |
| R7 | fact_notification (via bridge_order_notification) | fact_issue | order_no | Mostly 1 : N; 52 orders link to 2 or more notifications | 3,881 of 4,884 movement orders unmatched (2,791 of 17,518 issue rows matched); 4,187 of 5,190 notification orders without issues | Joining issues to notifications adds 60 rows (2,851 joined rows from 2,791 issue rows) because of shared orders | Join issues to the bridge at order level; flag issue rows whose order is shared; never sum issue quantities after a join that multiplied rows | Conditional: safe for "which orders consumed what" at order level; for notification-level attribution, shared orders must be flagged or allocated by an approved rule |
| R8 | fact_issue to dim_functional_location (derived through R7) | | order_no → notification → functional_location | N : 1 for orders on one notification | Only the 2,791 linked issue rows can be attributed | Shared orders may point to two locations | Flag `fl_attribution = 'unique'`, `'ambiguous'` or `'none'` | Conditional: valid for the linked 16% of issue rows only; report coverage |
| R9 | Movement material aggregate | PR PO material aggregate | material_no | 1 : 1 after aggregation to material (or material and month) | 900 issued but not procured; 220 procured but not issued; 1,030 both | High if joined at row level | Aggregate both sides to material or material-month first; assert 1 : 1 | Yes after aggregation |
| R10 | bridge_fl_material | fact_issue (via R8) | functional_location + material_no | Pair lookup | Expected match about 23% of attributed rows (22.6% measured on 2,851 joined rows; recount on 2,791 distinct rows) | None as a lookup | Produces flag `issued_material_in_fl_bom` | Yes as a data-quality measure (BoM completeness); not as proof of where parts were used |
| R11 | fact_plan_item | bridge_fl_material | functional_location | N : M | Locations with plans but no BoM, and the reverse | Naive join creates 30,245 rows (every plan item times every material on the location) | Allowed only into a separate `candidate_kit` table labelled HYPOTHESIS | No for demand or requirement analysis; yes for exploration only |
| R12 | fact_plan_item | fact_notification | functional_location | N : M | Many | High | Aggregate both to location first | Yes at location grain only |
| R13 | dim_functional_location | fact_plan_item | criticality, fl_desc (redundant) | Equality check | 0 mismatches expected | n/a | Test only | Not a join; a consistency test |

### 4.3 Integration diagram (text)

```text
                      dim_functional_location (14,484)
                     /            |                 \
          R1 (1:N)  /     R3 (1:N)|          R2 (1:N)\
                   /              |                   \
 bridge_fl_material (20,423)  fact_plan_item (10,153)  fact_notification (5,795)
          |    \                 (R11 N:M, hypothesis only)     |
          |     \                                               | bridge_order_notification (5,242)
   R4/R5  |      dim_material (7,481)                           | R7 (order)
          |      /            \                                 |
   prpo_line (6,189 distinct)   fact_issue (17,518) <-----------+
          |  R6                       R9 (material aggregate) <-> prpo material aggregate
   dim_supplier (124)
```

---

## 5. Analytical data mart design

Each mart lists grain, columns, dimensions, measures and relationships. Marts are built only from conformed (L2) tables. Every mart ships with a metadata file: spec version, policy parameters, row count, source checksums, synthetic-data label.

### 5.1 M1. Procurement intelligence: `mart_procurement_line`

| Item | Specification |
| --- | --- |
| Grain | One PR item (purchase_requisition, pr_item) under `PRPO_DUP_POLICY` (default distinct: expected 6,189 rows) |
| Keys | purchase_requisition + pr_item (PK); purchase_order + po_item (unique alternate key); material_no (FK); supplier_code (FK) |
| Dimensions | pr_type, pr_prefix, po_prefix, purchasing_group, currency, supplier_code, is_foreign_supplier, material_no, material_prefix, unit, mrp_type (from dim_material), pr_month |
| Measures | pr_quantity (material unit), amount (original currency), implied_unit_amount (B), requested_lead_days, promised_lead_days, promise_gap_days, dup_count |
| Flags | flag_req_before_pr, flag_promise_before_pr, flag_future_date, flag_extreme_interval, flag_outlier_* , in_idr_scope, rare_category |
| Relationships | dim_material (N:1), dim_supplier (N:1) |
| Companion aggregates | `mart_supplier_material` (grain supplier, material, currency: n_lines, total quantity, total amount, median promised lead days, first and last PR date); `mart_procurement_nonidr` (non-IDR rows reported separately) |
| Not allowed | Cross-currency totals; cross-material quantity totals; calling promised lead time "actual lead time" |

### 5.2 M2. Material inventory: `mart_material_inventory`

| Item | Specification |
| --- | --- |
| Grain | One material (expected 7,481 rows) |
| Keys | material_no (PK) |
| Dimensions | mrp_type, unit, material_prefix, desc_shared_group_id, is_issued, is_procured |
| Measures (state) | stock, min_qty, max_qty (planning parameters), n_bom_locations, n_fl_crit_A, n_fl_crit_B, n_fl_crit_C, n_fl_crit_S, n_fl_crit_null |
| Derived comparisons | stock_eq_zero, stock_lt_min, stock_gt_max, min_eq_max, nonstock_with_stock, stockitem_min_max_zero |
| Joined summaries | From M3: n_issue_lines_total, qty_issued_total, months_with_issue, last_issue_date. From M1: n_pr_lines, median_promised_lead_days, supplier_code (single), currency |
| Relationships | 1 : N to bridge_fl_material, fact_issue, prpo_line |
| Not allowed | Summing stock across materials of different units; using min_qty or max_qty as capacity; a stock value total without unit prices |

### 5.3 M3. Material consumption and demand: `mart_material_demand_month`

| Item | Specification |
| --- | --- |
| Grain | One issued material by calendar month, 2025-05 to 2026-09, zero-filled within the window (expected 1,930 materials x 17 months = 32,810 rows) |
| Keys | material_no + month (PK) |
| Dimensions | month, unit, mrp_type, material_prefix |
| Measures | qty_issued (material unit), n_issue_lines, n_orders, n_orders_with_notification, n_issue_lines_dup_extra |
| Companion | `mart_material_demand_summary` (grain material): first_issue_date, last_issue_date, total qty, total lines, months_with_issue, mean and standard deviation of monthly qty, number of non-zero months. Intermittency classification (ADI, CV squared) is computed in EDA, not here. |
| Policy | MOVE_DUP_POLICY recorded per build; sensitivity build with distinct policy |
| Not allowed | Cross-material quantity sums; extending zeros outside the observed window; treating issues as receipts |

### 5.4 M4. Equipment and maintenance reliability

| Table | Grain | Columns and measures |
| --- | --- | --- |
| `fact_notification` | One notification (5,795) | notification, notification_type, notif_priority, status, is_open, is_censored, functional_location, criticality, fl_prefix, is_system_level, order_no, order_missing, order_shared, notification_date, required_start, required_end, completion_date, days_to_complete, days_open_at_cutoff, required_window_days, days_late_vs_required, completed_late, desc_ref_code, desc_first_word, first_month_flag, date flags |
| `mart_fl_reliability` | One functional location (14,484, including locations with no activity) | criticality, fl_prefix, tag_class_candidate, is_system_level, n_notifications by type and priority, n_open, median days_to_complete, n_plan_items, n_plans, n_bom_materials, n_issue_lines_attributed, fl_in_all_three |
| `fact_plan_item` | One maintenance item (10,153) | maintenance_item, maintenance_plan, functional_location, criticality (from FuncLoc), item_text, item_text_group, plan_priority, cycle_desc, interval_value, interval_unit, interval_days_approx, start_of_cycle, flags |

Relationships: fact_notification and fact_plan_item are N : 1 to dim_functional_location. They relate to each other only at location grain (R12).

Not allowed: treating every notification as a failure; averaging plan_priority; ranking criticality before approval.

### 5.5 M5. Maintenance-to-material relationships

| Table | Grain | Purpose | Columns | Evidence class |
| --- | --- | --- | --- | --- |
| `bridge_order_material` | One order and material | What each order consumed | order_no, material_no, order_prefix, qty_issued, n_issue_lines, first_posting_date, has_notification | OBSERVED consumption |
| `bridge_issue_attribution` | One issue row linked to a notification | Where linked consumption happened | issue row id, order_no, notification(s), functional_location, fl_attribution (unique, ambiguous, none), issued_material_in_fl_bom, posting_lag_days (posting minus notification date) | OBSERVED for 2,791 rows only |
| `candidate_kit` | One plan item and BoM material on the same location | Exploration of possible parts for planned work | maintenance_item, functional_location, material_no, installed_qty, stock, mrp_type | HYPOTHESIS: the diagram states plans do not list spare parts |

Coverage metrics shipped with M5: share of issue rows attributable to a location (expected about 16%), share of attributed issues whose material is in the location's BoM (expected about 23%), share of notification orders with any issue (expected about 19%).

### 5.6 M6. Integrated critical spare-part intelligence: `mart_critical_spare_part`

| Item | Specification |
| --- | --- |
| Grain | One material (7,481 rows); analyses may filter to Stock Items or to issued materials |
| Keys | material_no (PK) |
| Inventory components | stock, min_qty, max_qty, mrp_type, stock comparisons (from M2) |
| Equipment exposure components | n_bom_locations, n_fl_crit_A, n_fl_crit_B, n_fl_crit_C, n_fl_crit_S; notifications on locations where the material is in the BoM (n_notif_on_bom_fl, n_open_notif_on_bom_fl) |
| Demand components | qty_issued_total, n_issue_lines_total, months_with_issue, last_issue_date (from M3) |
| Supply components | n_pr_lines, median_promised_lead_days, supplier_code, currency, is_foreign_supplier (from M1) |
| Linkage-quality components | n_attributed_issues, share_issued_in_fl_bom (from M5) |
| Not included | Any composite risk score. A score needs weights and a criticality ranking, which are EDA and modelling decisions after DEF-03. This mart only supplies the components. |
| Relationships | 1 : 1 with M2; 1 : N to M3, M1, M5 |

---

## 6. Cleaning decision register

Classification: **A** safe automatic transformation; **B** transformation requiring validation; **C** preserve and flag; **D** business definition unavailable.

| Issue ID | Dataset | Column or field | Problem | Proposed treatment | Reason | Risk of incorrect treatment | Required validation | Class |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| G-01 | All | Source files | Accidental modification | Read-only load, SHA-256 checksum | Reproducibility | None | Checksum matches at every run | A |
| G-02 | All | Identifiers | Stored as numbers | Cast to string | Prevent arithmetic and float artefacts | None | Pattern tests (Section 2.9) | A |
| G-03 | All | Column names | Same concept, different names | Rename to standard names (dictionary Section 7) | Consistent joins | Confusing two Priority systems | Keep notif_priority and plan_priority separate | A |
| G-04 | All | Lineage | No row traceability | Add source_file, source_row, row_hash | Audit | None | Row counts equal raw counts | A |
| G-05 | All | Dates | Need consistent type | Cast to datetime; confirm no time component | Correct interval maths | None | 0 non-midnight values | A |
| G-06 | All | DATA_CUTOFF | Needed for "future" flags and censoring | Set to 2026-09-30 | Latest event date in files | Wrong cutoff mislabels open items | Case owner confirms extraction date | B |
| P-01 | PR PO | All columns | 5,420 exact duplicate rows | Flag groups; marts use distinct rows by default; keep dup_count | Business keys unique after removing copies | Spend and quantity halved if copies are real | DEF-01; report totals under both policies | B |
| P-02 | PR PO | PR + PR-Item, PO + PO-Item | Keys unique only after duplicates | Test uniqueness on distinct rows | Justifies P-01 | If test fails, P-01 is invalid | Expected 6,189 unique on both keys | A |
| P-03 | PR PO | PO-Currency, PO-Item Amount | Five currencies, no FX | Keep original currency; IDR-only spend marts; optional sourced FX scenario | Avoid invented rates | Non-IDR spend hidden from totals | Report non-IDR rows separately | A |
| P-04 | PR PO | PO-Item Amount | Meaning undefined | Derive implied_unit_amount with stated assumption | Needed for price analysis and value proxies | Wrong if amount is not a line total | DEF-05 | B |
| P-05 | PR PO | PR-Quantity | No PO quantity | Treat PR quantity as ordered quantity, labelled assumption | Only quantity available | Wrong if PO quantity differs | DEF-05 | B |
| P-06 | PR PO | PR-Delivery Date | 630 raw rows before PR-Date | Flag; exclude from requested-interval statistics by default | Illogical interval | Excluding real data if the rule differs | DEF-06; recount on distinct rows | C |
| P-07 | PR PO | PO-Delivery Date | 6 raw rows before PR-Date | Flag; exclude from promised-interval statistics by default | Illogical interval | Small | Recount on distinct rows | C |
| P-08 | PR PO | PO-Delivery Date | Promised, not actual | Name intervals promised_*; never "lead time actual" | No receipt date | Overstated precision | Naming review | A |
| P-09 | PR PO | Delivery dates | Dates after DATA_CUTOFF | Flag flag_future_date | Open promises | Depends on G-06 | G-06 | C |
| P-10 | PR PO | PR-Material Desc | 191 rows with spaces | Trim into new column | Clean labels | None | Original kept | A |
| P-11 | PR PO | PR-Type, PO prefix, Purchasing Group | Codes undefined | Keep as codes; flag rare categories | Avoid invented labels | Misread groups | DEF-08 | D |
| P-12 | PR PO | PO-Supplier Name | Likely synthetic names | Keep as label only; no geocoding | Data is synthetic | False entity matching | None for preparation | C |
| P-13 | PR PO | Supplier and material mapping | One supplier per material | Validate and record as a structural fact | Affects sourcing analyses | None | Expected 1,250 materials with 1 supplier | A |
| P-14 | PR PO | Quantities, unit amounts | Heavy tails | Robust outlier flags within material | Protect statistics without deleting | Threshold choice | Review top 20 per measure | C |
| B-01 | BoM | All columns | 230 exact duplicates | Flag; bridge uses distinct pairs | Pair key unique after removal; values identical | Very low | Expected 20,423 pairs | B |
| B-02 | BoM | Stock, Min.Qty, Max.Qty, MRP Type, Unit, Desc | Material-level values repeated per row | Split into dim_material (one row per material) | Prevent double counting | Wrong if values ever differ by location | Test 0 materials with conflicting values | A (conditional on test) |
| B-03 | BoM | Min.Qty, Max.Qty | Meaning undefined | Keep as planning parameters; no capacity use | Avoid wrong constraint | Wrong policy analysis | DEF-02 | D |
| B-04 | BoM | Stock | Undated snapshot | Keep; no time series from Stock | No date | Misaligned with demand window | DEF-12 | D |
| B-05 | BoM | MRP Type | 1,683 Non Stock materials hold stock | Flag nonstock_with_stock | Unexplained pattern | Misclassifying excess | DEF-04 | C |
| B-06 | BoM | Stock | Zero stock | Flag stock_eq_zero; no "stockout" label | No business rule | Overstated shortages | Business rule for stockout | C |
| B-07 | BoM | Stock, Installed Qty | Fractions on count units (0.5 EA; 89 Installed Qty) | Flag | Possible unit error | None (flag only) | Review list | C |
| B-08 | BoM | Material Desc. | 438 rows with spaces; 133 shared descriptions | Trim; flag shared groups; never merge codes | Clean labels; avoid false merges | Merging distinct parts | Engineering review of shared groups | A (trim), C (shared) |
| B-09 | BoM | Unit | Ten codes, no conversion | No conversion; aggregate within material only | Units not comparable | None | 0 unit mismatches across tables | A |
| M-01 | Movement | All columns | 863 exact duplicate rows | Keep all (raw policy); flag; sensitivity with distinct | No document key to prove repetition | Demand overstated if copies are errors | Compare demand under both policies | C |
| M-02 | Movement | Date, material, order | 297 groups with same key and different quantities | Keep; flag partial groups | Plausible separate issues | Minor | None | C |
| M-03 | Movement | Movement Type | Single value "Issue" | Validate constant | Sign convention depends on it | New types would break sums | Test single value | A |
| M-04 | Movement | Order | 79.5% of orders lack a notification | Flag has_notification; keep all | Order types undefined | Wrong attribution | DEF-07 | C |
| M-05 | Movement | Quantity | Monthly demand needs zeros | Zero-fill within 2025-05 to 2026-09 for issued materials only | Correct intermittency measurement | Wrong if issue log incomplete | Confirm completeness of issue log | B |
| M-06 | Movement | Quantity | Heavy tail | Outlier flags within material | Protect statistics | Threshold choice | Review | C |
| N-01 | Notif | Order | 553 nulls, float storage | Convert to string; keep nulls; flag | Structural (all In Progress) | None | 553 nulls, all In Progress | A |
| N-02 | Notif | Order | 52 orders on 2 or more notifications | Bridge table; flag order_shared | Prevent double counting of issues | Wrong attribution | Check same-location share | C |
| N-03 | Notif | Status, Completion by Date | Null completion for open items | Keep null; censor in duration analysis | Not missing data | Biased durations if imputed | Status consistency test | A |
| N-04 | Notif | Required Start | 370 before notification date | Flag | Illogical order | Unknown rule | DEF-14 | C |
| N-05 | Notif | Completion vs Required End | 2,028 completed late | Derive completed_late | Analysis feature | None | None | A |
| N-06 | Notif | Priority | Order not documented | Unordered category; rank only after approval | Avoid assumed ranking | Wrong severity weighting | Case owner approval | D |
| N-07 | Notif | Notification Type | Meanings undefined | Keep codes | Avoid invented labels | Misread failure share | DEF-09 | D |
| N-08 | Notif | Description | Free text, bracket codes | Trim; extract desc_ref_code; classification deferred to EDA | Preparation should not interpret | Pattern misses | Sample check of 50 rows | B |
| N-09 | Notif | Notification Date | 1,463 records in first month | first_month_flag | Possible backlog load | None (flag only) | Sensitivity in EDA | C |
| N-10 | Notif | Functional Location | 394 on SITE rows | Flag is_system_level | Different level of detail | None | None | A |
| I-01 | Mitem | Cycle Descriptions | 28 spellings | Approved mapping to value and unit (Appendix A) | Needed for intervals | Wrong interval for ambiguous spellings | DEF-10 | B |
| I-02 | Mitem | Start of cycle | Meaning undefined; 2015 to 2029 | Keep; flag future starts; no projection until defined | Projection depends on meaning | Fabricated schedule | DEF-11 | D |
| I-03 | Mitem | ABC Indicator, FunctLocDescrip. | Redundant with FuncLoc | Test equality; use FuncLoc values in marts | Single source of truth | None | 0 mismatches | A |
| I-04 | Mitem | Priority | Numeric code | Cast to category | Not a quantity | None | None | A |
| I-05 | Mitem | Maint. item text | Synonyms | Reviewed synonym map into item_text_group | Fair task counts | Over-merging tasks | Review of map | B |
| I-06 | Mitem | Plans vs BoM | Plans list no parts | candidate_kit table labelled hypothesis only | Diagram states no part link | Treating candidates as requirements | Label check | C |
| F-01 | FuncLoc | Functional Location | Uniqueness | Test | PK | None | 14,484 unique | A |
| F-02 | FuncLoc | FuncLoc Criticallity | 33 nulls (SITE rows) | Keep null; flag with reason | No fabricated class | None | 33 nulls, all SITE | C |
| F-03 | FuncLoc | FuncLoc Criticallity | Ranking undefined | Unordered category | Avoid assumed order | Wrong weighting | DEF-03 | D |
| F-04 | FuncLoc | Functional Location | Hierarchy not stored | Derive prefix and tag-pattern labels only; no parent links | Pattern evidence only | Wrong grouping if patterns misread | Sample check of 100 codes per pattern | B |
| F-05 | FuncLoc | FunctLocDescrip. | Generic repeated texts | Trim only | Labels, not keys | None | None | A |
| X-01 | BoM to Movement, PR PO | Material joins | Row explosion (615,146 and 293,658 rows) | Join through dim_material only | Grain safety | Inflated totals | Row-count assertions | A |
| X-02 | Movement to Notif | Order join | 60 extra rows from shared orders | Join at order level; flag shared | Avoid double counting | Inflated attributed demand | Row-count assertion | B |
| X-03 | Mitem to BoM | Location join | 30,245 candidate pairs | Separate hypothesis table only | No requirement evidence | False demand | Label check | C |
| X-04 | Same description, different materials | Material equivalence | 36 PR pairs with different suppliers | Flag only; no merging, no alternative-source assumption | Equivalence unconfirmed | False multi-sourcing | Engineering confirmation | C |

---

## 7. Validation test suite

Each test returns pass or fail with the observed value. Expected values come from the raw inspection of 2026-11-04. A failed test stops the build unless marked "warn".

| Test ID | Table | Assertion | Expected |
| --- | --- | --- | --- |
| T01 | All | Raw row counts | PR PO 11,609; Movement 17,518; Notif 5,795; Mitem 10,153; BoM 20,653; FuncLoc 14,484 |
| T02 | All | Column counts | 18; 7; 12; 9; 9; 3 |
| T03 | All | Checksums unchanged between runs | Equal |
| T04 | PR PO | Exact duplicate extra rows | 5,420 |
| T05 | PR PO | Distinct rows; unique (PR, PR-Item); unique (PO, PO-Item) | 6,189; true; true |
| T06 | PR PO | Supplier codes; names per code | 124; 1 |
| T07 | PR PO | Suppliers per material (max) | 1 |
| T08 | PR PO | Plant values | {1000} |
| T09 | PR PO | Currency row counts (raw) | IDR 11,511; JPY 41; USD 35; EUR 20; SGD 2 |
| T10 | PR PO | Requested before PR (raw); promised before PR (raw) | 630; 6 (warn if changed) |
| T11 | BoM | Exact duplicate extra rows; distinct pairs | 230; 20,423 |
| T12 | BoM | Materials with conflicting material-level values | 0 |
| T13 | BoM | Materials; Stock Item; Non Stock | 7,481; 3,656; 3,825 |
| T14 | BoM | Non Stock with stock above zero | 1,683 (warn) |
| T15 | Movement | Movement Type values | {Issue} |
| T16 | Movement | Exact duplicate extra rows | 863 |
| T17 | Movement | Materials; orders | 1,930; 4,884 |
| T18 | Notif | Unique notifications | 5,795 |
| T19 | Notif | Status Complete with date; In Progress without date | 4,490; 1,305 |
| T20 | Notif | Null orders; all In Progress | 553; true |
| T21 | Notif | Orders on 2 or more notifications | 52 |
| T22 | Notif | Required End before Required Start; completion before notification | 0; 0 |
| T23 | Mitem | Unique maintenance items | 10,153 |
| T24 | Mitem | Unmapped cycle descriptions after mapping | 0 |
| T25 | Mitem | ABC Indicator mismatches with FuncLoc; description mismatches | 0; 0 |
| T26 | FuncLoc | Unique locations; null criticality; nulls all SITE | 14,484; 33; true |
| T27 | Cross | FK misses: BoM FL, Notif FL, Mitem FL, Movement material, PR material | 0 each |
| T28 | Cross | Units per material across tables (max) | 1 |
| T29 | Cross | Descriptions per material after trimming (max) | 1 |
| T30 | Cross | Movement orders found in Notif; issue rows matched | 1,003; 2,791 |
| T31 | Cross | Materials issued and procured; issued only; procured only | 1,030; 900; 220 |
| T32 | Marts | Row count of fact tables unchanged after dimension lookups | Equal |
| T33 | Marts | mart_material_demand_month rows | 32,810 |
| T34 | Marts | No mart sums quantity across materials or amount across currencies | Code review and column test |

---

## 8. Approval checklist

### 8.1 Safe to implement now (Class A)

- [ ] G-01 to G-05: read-only load, checksums, string identifiers, standard names, lineage, date types.
- [ ] Whitespace trimming into new description columns (P-10, B-08 trim part, F-05).
- [ ] All flag columns that describe observed facts (duplicate groups, date flags, orphan flags, structural nulls, SITE rows, redundancy tests).
- [ ] P-02, P-13, B-09, M-03, N-01, N-03, N-05, N-10, I-03, I-04, F-01: validation tests and type fixes.
- [ ] B-02: split BoM into dim_material and bridge_fl_material, **only if** test T12 passes.
- [ ] P-03: keep original currency, IDR-only spend scope, no conversion.
- [ ] P-08: promised and requested naming for all PR PO intervals.
- [ ] X-01: material joins only through dim_material, with row-count assertions.
- [ ] The full validation suite in Section 7.

### 8.2 Implement with an assumption, then validate (Class B)

- [ ] G-06: DATA_CUTOFF = 2026-09-30. Validate: extraction date from case owner.
- [ ] P-01: PR PO distinct policy as default. Validate: DEF-01; always publish both totals.
- [ ] P-04, P-05: implied unit amount and PR quantity as ordered quantity. Validate: DEF-05.
- [ ] B-01: BoM distinct pairs. Validate: pair-key uniqueness test.
- [ ] M-05: zero-filled monthly demand inside the observed window. Validate: completeness of the issue log.
- [ ] N-08: bracket-code extraction. Validate: sample of 50 rows.
- [ ] I-01: cycle mapping (Appendix A). Validate: DEF-10.
- [ ] I-05: item-text synonym map. Validate: review by a maintenance planner or the team.
- [ ] F-04: prefix and tag-pattern labels. Validate: sample of 100 codes per pattern.
- [ ] X-02: order-level join with shared-order flags.
- [ ] Outlier method and thresholds (Section 2.8).

### 8.3 Preserve and flag; approve the approach (Class C)

- [ ] P-06, P-07, P-09: illogical or future procurement dates kept and flagged.
- [ ] P-12: supplier names kept as labels only.
- [ ] P-14, M-06: outliers flagged, never removed.
- [ ] B-05, B-06, B-07: Non Stock with stock, zero stock, fractional counts flagged.
- [ ] M-01, M-02: Movement duplicates kept (raw policy) with a distinct-policy sensitivity run.
- [ ] M-04, N-02: unlinked and shared orders flagged.
- [ ] N-04, N-09: required-date anomalies and first-month volume flagged.
- [ ] F-02: SITE-level criticality nulls kept.
- [ ] I-06, X-03: candidate kits labelled hypothesis.
- [ ] X-04: shared descriptions flagged; no merging and no assumed alternative sources.

### 8.4 Blocked until a business definition is supplied (Class D)

- [ ] DEF-01 duplicate meaning in PR PO (affects P-01).
- [ ] DEF-02 Min.Qty and Max.Qty meaning (B-03; blocks a combined stock-status label).
- [ ] DEF-03 criticality codes and ranking (F-03; blocks any criticality weighting or score).
- [ ] DEF-04 Non Stock meaning (B-05 interpretation).
- [ ] DEF-05 PO-Item Amount meaning (P-04, P-05).
- [ ] DEF-06 PO-Delivery Date meaning and receipt dates (P-06, P-08).
- [ ] DEF-07 order prefixes (M-04).
- [ ] DEF-08 PR-Type, PO prefix, purchasing groups (P-11).
- [ ] DEF-09 notification types (N-07).
- [ ] DEF-10 cycle mapping confirmation (I-01).
- [ ] DEF-11 Start of cycle meaning (I-02; blocks due-date projection).
- [ ] DEF-12 stock snapshot date (B-04).
- [ ] DEF-13 plant, material prefixes, location prefixes.
- [ ] DEF-14 Notification Date versus Created On (N-04).
- [ ] DEF-15 unit codes.
- [ ] Priority ranking approval (N-06).

If definitions do not arrive before the EDA deadline, each blocked item proceeds only as a declared ASSUMPTION, recorded in an assumptions register with a sensitivity check, and labelled as such in every chart and table that depends on it.

---

## Appendix A. Cycle description mapping (proposed, requires DEF-10)

| Source value | Rows | interval_value | interval_unit | interval_days_approx | Mapping status |
| --- | --- | --- | --- | --- | --- |
| 1 WEEKLY | 26 | 1 | WEEK | 7 | Direct |
| Weekly | 15 | 1 | WEEK | 7 | Assumed same as 1 WEEKLY |
| 2 WEEK | 14 | 2 | WEEK | 14 | Direct |
| 2 WEEKLY | 96 | 2 | WEEK | 14 | Direct (read as every 2 weeks, not twice a week) |
| 4 WEEKLY | 92 | 4 | WEEK | 28 | Direct |
| 8 WEEKLY | 3 | 8 | WEEK | 56 | Direct |
| 12 WEEK | 76 | 12 | WEEK | 84 | Direct |
| 16 WEEKLY | 3 | 16 | WEEK | 112 | Direct |
| 24 WEEK | 39 | 24 | WEEK | 168 | Direct |
| 26 WEEKLY | 31 | 26 | WEEK | 182 | Direct |
| 48 WEEK | 26 | 48 | WEEK | 336 | Direct |
| 1 MONTHLY | 49 | 1 | MONTH | 30.4375 | Direct |
| Monthly | 160 | 1 | MONTH | 30.4375 | Assumed same as 1 MONTHLY |
| 2 MONTHLY | 3 | 2 | MONTH | 60.875 | Direct |
| 3 MONTHLY | 267 | 3 | MONTH | 91.3125 | Direct |
| 4 MONTH | 83 | 4 | MONTH | 121.75 | Direct |
| 6 MONTHLY | 788 | 6 | MONTH | 182.625 | Direct |
| 12 MONTHLY | 229 | 12 | MONTH | 365.25 | Direct; kept distinct from 1 YEARLY in the original column |
| 18 MONTHLY | 1,132 | 18 | MONTH | 547.875 | Direct |
| 30 MONTHLY | 4 | 30 | MONTH | 913.125 | Direct |
| 1 YEARLY | 1,254 | 1 | YEAR | 365.25 | Direct |
| YEARLY | 465 | 1 | YEAR | 365.25 | Assumed same as 1 YEARLY |
| Yearly | 305 | 1 | YEAR | 365.25 | Assumed same as 1 YEARLY |
| 2 YEARLY | 376 | 2 | YEAR | 730.5 | Direct |
| 3 YEARLY | 202 | 3 | YEAR | 1,095.75 | Direct |
| 5 YEARLY | 3,767 | 5 | YEAR | 1,826.25 | Direct |
| 8 YEARLY | 27 | 8 | YEAR | 2,922 | Direct |
| 10 YEARLY | 621 | 10 | YEAR | 3,652.5 | Direct |

Total rows: 10,153. The "x WEEKLY" and "x MONTHLY" spellings are read as "every x weeks or months". If the case owner reads "2 WEEKLY" as twice a week, the 96 rows with that spelling, and any other "x WEEKLY" or "x MONTHLY" rows read the same way, must be remapped.

---

## Appendix B. Flag catalogue

| Flag | Table | Meaning |
| --- | --- | --- |
| is_dup_extra, dup_group_id, dup_count, dup_rank | PR PO, BoM, Movement | Exact duplicate structure |
| is_partial_dup_group, partial_dup_group_id | Movement, Notif | Same business key, different values |
| flag_req_before_pr | PR PO | Requested delivery before PR date |
| flag_promise_before_pr | PR PO | Promised delivery before PR date |
| flag_future_date | PR PO, Notif | Date after DATA_CUTOFF |
| flag_extreme_interval | PR PO, Notif | Interval beyond 99.5th percentile |
| flag_outlier_<measure>, outlier_method | PR PO, Movement, BoM | Robust outlier flag |
| in_idr_scope | PR PO | Currency is IDR |
| rare_category | PR PO | Category with fewer than 30 distinct rows |
| stock_eq_zero, stock_lt_min, stock_gt_max, min_eq_max | dim_material | Raw stock comparisons |
| nonstock_with_stock, stockitem_min_max_zero | dim_material | MRP pattern flags |
| flag_fraction_on_count_unit | BoM | Non-integer value on EA, SET or ASS |
| desc_shared_group_id | dim_material, PR PO | Same description on several material numbers |
| is_issued, is_procured | dim_material | Material appears in Movement or PR PO |
| has_notification | Movement | Order exists in Notif History |
| order_missing, order_shared, shared_order_same_fl | Notif | Order linkage state |
| is_open, is_censored | Notif | Open at DATA_CUTOFF |
| completed_late | Notif | Completed after Required End |
| flag_reqstart_before_notif, flag_created_differs | Notif | Date anomalies |
| first_month_flag | Notif | Notification in 2025-05 |
| is_system_level | FuncLoc, Notif | SITE-level location |
| criticality_missing, criticality_missing_reason | FuncLoc | Structural null criticality |
| flag_cycle_unmapped, flag_future_cycle_start, start_day_is_first | Mitem | Cycle data checks |
| plan_multi_fl | Mitem | Plan covering several locations |
| fl_has_bom, fl_has_notification, fl_has_plan, fl_in_all_three | FuncLoc | Usage across tables |
| fl_attribution | Issue attribution | unique, ambiguous or none |
| issued_material_in_fl_bom | Issue attribution | Issued material appears in that location's BoM |
| flag_invalid_id, flag_unit_mismatch | Any | Identifier or unit rule broken |

---

## Appendix C. Output files and naming (for the implementation phase)

```text
caliber_supply_chain/
  data/
    raw/                      L0: original workbooks + checksums.json
    staged/                   L1: one parquet per workbook (stg_prpo, stg_movement, stg_notif, stg_mitem, stg_bom, stg_funcloc)
    conformed/                L2: dim_material, dim_functional_location, dim_supplier,
                                  bridge_fl_material, bridge_order_notification,
                                  prpo_line, fact_issue, fact_notification, fact_plan_item,
                                  map_cycle (Appendix A), map_item_text
    marts/                    L3: mart_procurement_line, mart_supplier_material, mart_procurement_nonidr,
                                  mart_material_inventory, mart_material_demand_month,
                                  mart_material_demand_summary, mart_fl_reliability,
                                  bridge_order_material, bridge_issue_attribution, candidate_kit,
                                  mart_critical_spare_part  (+ one metadata JSON per mart)
  docs/
    CALIBER_DATA_DICTIONARY.md
    CALIBER_DATA_PREPARATION_SPECIFICATION.md
    assumptions_register.md   (created when Class B or D items proceed on assumptions)
    validation_report.md      (output of Section 7 at each build)
```

Naming rules: snake_case column names; `stg_` staged, `dim_` dimension, `fact_` event table, `bridge_` many-to-many or pair table, `map_` mapping table, `mart_` analysis dataset.

---

## Appendix D. Correction to the Analytical Discovery Report

The discovery report states that 2,851 movement lines link to a notification. The precise figures are: 2,791 distinct issue rows have an order found in Notif History; joining them to notifications yields 2,851 rows because 52 orders sit on more than one notification (60 extra rows). The 22.6% BoM-match share was measured on the 2,851 joined rows and must be recomputed on the 2,791 distinct rows during implementation (test T30 and relationship R10).
