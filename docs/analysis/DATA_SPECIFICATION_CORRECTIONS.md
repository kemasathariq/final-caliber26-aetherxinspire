# CALIBER 2026 Data Specification Corrections

**Version:** corrections-3, applied as pipeline specification version `0.1+corrections-3`
**Date:** 2026-11-04
**Applies to:** `CALIBER_DATA_DICTIONARY.md` v0.1, `CALIBER_DATA_PREPARATION_SPECIFICATION.md` v0.1 and, where stated, `CALIBER 2026 Analytical Discovery Report.md` and the Data Context & Relationship Diagram.

The original documents are preserved unchanged. **Where this document and an original disagree, this document takes precedence for implementation.**

Check IDs refer to `outputs/tables/validation_results.csv`. Test names refer to `tests/`. All check results below are from the Step 5 build.

## How corrections are classified

| Class | Meaning |
| --- | --- |
| Confirmed by data | Measured directly from the workbooks. The original statement does not match the data. |
| Approved decision | Set by the project owner's authorisation of Phases 0 and 1, or of continuing to Phases 2 and 3. |
| Technical design | An engineering change with no effect on business meaning. |
| Unresolved | The correction states a rule to follow, but the underlying business question stays open. See `ASSUMPTIONS_REGISTER.md`. |

## Summary

| ID | Topic | Class | Validation result |
| --- | --- | --- | --- |
| COR-01 | Identifier storage and read types | Confirmed by data | PASS |
| COR-02 | Suppliers per foreign currency | Confirmed by data | PASS |
| COR-03 | Descriptions starting with Replace | Confirmed by data | PASS |
| COR-04 | Issues posted before notification | Confirmed by data | PASS |
| COR-05 | Maximum locations per material | Confirmed by data | PASS |
| COR-06 | Plan-to-BoM join size | Confirmed by data | PASS |
| COR-07 | Non-integer Installed Qty | Confirmed by data | PASS |
| COR-08 | Specification approval status | Approved decision | Not a data check |
| COR-09 | PR PO duplicate policy | Approved decision, cause unresolved | PASS |
| COR-10 | Directory layout and storage format | Approved decision | PASS |
| COR-11 | Run timestamp on rows | Technical design | PASS |
| COR-12 | Reference dates | Confirmed by data, cutoff unresolved | PASS |
| COR-13 | Criticality ranking and scoring | Unresolved | PASS for the rule; meaning open |
| COR-14 | Diagram grains and cardinality | Confirmed by data | PASS |
| COR-15 | Case designation | Approved decision | Not a data check |
| COR-16 | Conformed PR PO table and flag names | Technical design, follows COR-09 | PASS |
| COR-17 | Population-based flags per view | Technical design, follows COR-09 | PASS |
| COR-18 | Non-IDR suppliers | Unresolved | PASS for the rule; meaning open |
| COR-19 | Notification repeats and reference codes | Confirmed by data | PASS |
| COR-20 | Outliers where no threshold exists | Technical design, assumption A-10 | PASS |
| COR-21 | Movement policy replaced by two scenarios | Approved decision | PASS |
| COR-22 | M1 in two parallel views | Approved decision, follows COR-09 | PASS |
| COR-23 | Unit amount as a labelled scenario | Unresolved (DEF-05) | PASS for the label; meaning open |
| COR-24 | Mart storage and metadata | Technical design | PASS |

---

## Corrections

### COR-01. Identifier storage and read types

| Item | Detail |
| --- | --- |
| Class | Confirmed by data |
| Source | Dictionary, "Current type" column. Spec Sections 2.9 and 3.4 (S01), and decision N-01 |
| Stated | Identifiers are `int64`. Notif Order is `float64`, with a risk of text such as `201000000108.0`. Order must be converted from float to integer to string |
| Observed | All identifiers are stored in the files as inline text. No value contains a decimal point. Default `pandas.read_excel` then infers `int64` or `float64` for them, including `float64` for Notif Order |
| Explanation | The Dictionary recorded the types pandas infers by default, not how the files store the values. This also refines the audit plan, which described the column simply as wrong. The risk it warns about is real, but only under a default read |
| Rationale | Reading text as text needs no conversion. Inference followed by conversion would be the step that creates risk, because it could drop leading zeros in any future file |
| Implementation impact | `read_source_table` reads with `dtype=object`, `keep_default_na=False` and `na_values=[""]`, then applies types from `src/data/schemas.py`. The float repair step is dropped |
| Validation | `TYP-01.*`, `TYP-02.*`, `ID-02.*`, `ROW-03.*`. Tests `test_default_read_excel_would_damage_identifiers`, `test_leading_zeros_are_preserved`, `test_nullable_order_is_never_stored_as_a_float` |

### COR-02. Suppliers per foreign currency

| Item | Detail |
| --- | --- |
| Class | Confirmed by data |
| Source | Dictionary (PO-Currency). Spec Section 2.7 |
| Stated | Each non-IDR currency belongs to exactly one foreign supplier |
| Observed | JPY has 3 suppliers (108763, 110155, 113914). EUR, SGD and USD have 1 each. IDR has 118. Each supplier uses exactly one currency, which is the rule that holds |
| Rationale | The stated rule would fail against the data |
| Implementation impact | Validate "one currency per supplier", not "one supplier per currency" |
| Validation | `EXP.prpo.max_currencies_per_supplier` = 1, `EXP.prpo.suppliers_per_currency` |

### COR-03. Descriptions starting with Replace

| Item | Detail |
| --- | --- |
| Class | Confirmed by data |
| Source | Discovery Report Section 2.4 |
| Stated | 1,009 descriptions start with Replace |
| Observed | 882, compared case-insensitively on the first word after trimming |
| Rationale | The source of the 1,009 figure cannot be reproduced |
| Implementation impact | Do not reuse the discovery figure |
| Validation | `EXP.notif.description_starts_with_replace` |

### COR-04. Issues posted before notification

| Item | Detail |
| --- | --- |
| Class | Confirmed by data |
| Source | Discovery Report Section 3 |
| Stated | 20 lines were posted before the notification |
| Observed | 10 of the 2,851 joined rows, using Notification Date. The audit measured 13 using Created On |
| Rationale | The source of the 20 figure cannot be reproduced |
| Implementation impact | Do not reuse the discovery figure. Name the date used in any later analysis |
| Validation | `EXP.cross.joined_rows_posted_before_notification` |

### COR-05. Maximum locations per material

| Item | Detail |
| --- | --- |
| Class | Confirmed by data |
| Source | Discovery Report Section 2.2. Dictionary (Material No) |
| Stated | One material sits on 308 locations |
| Observed | 308 raw BoM rows, which is 307 distinct locations after setting aside an exact copy |
| Rationale | A location count must not include repeated rows |
| Implementation impact | Report distinct locations |
| Validation | `EXP.bom.max_rows_per_material` = 308, `EXP.bom.max_locations_per_material` = 307 |

### COR-06. Plan-to-BoM join size

| Item | Detail |
| --- | --- |
| Class | Confirmed by data |
| Source | Spec R11 and X-03 |
| Stated | The join creates 30,245 rows, in a relationship defined on `bridge_fl_material` |
| Observed | 30,245 applies to raw BoM rows. It is 29,913 on distinct BoM rows, which is the grain `bridge_fl_material` will have |
| Rationale | The expected value must match the table actually joined |
| Implementation impact | Use 29,913 as the expected size in Phase 3 |
| Validation | `EXP.cross.raw_join_rows_mitem_bom_all_rows`, `EXP.cross.raw_join_rows_mitem_bom_distinct` |

### COR-07. Non-integer Installed Qty

| Item | Detail |
| --- | --- |
| Class | Confirmed by data |
| Source | Spec Section 2.8 and B-07 |
| Stated | 89 non-integer Installed Qty values are listed among fractions on count units |
| Observed | All 89 are in unit M. Whether M means metre is undefined (DEF-15). The only fraction on a count unit is Stock of 0.5 on material 4300057364, unit EA |
| Rationale | `flag_fraction_on_count_unit` will catch 1 material, not 90 rows |
| Implementation impact | Correct the expected count for that flag in Phase 3 |
| Validation | `EXP.bom.non_integer_installed_by_unit`, `EXP.bom.non_integer_stock_on_count_unit_materials` |

### COR-08. Specification approval status

| Item | Detail |
| --- | --- |
| Class | Approved decision |
| Source | Spec header and Section 8, labelled "Version 0.1 (draft for approval)" |
| Correction | The project owner has approved the recommended technical direction, with the Dictionary and Specification as foundational references, as corrected here |
| Limit | Phases 0 to 3 and marts M1 to M3 are authorised. Marts M4 to M6, EDA, simulation and later steps have not been applied. Checklist items in Spec Section 8 are not individually signed off |
| Implementation impact | Staged rows carry `spec_version = 0.1+corrections-3` |
| Validation | Document review. `ROW-05` confirms lineage is present |

### COR-09. PR PO duplicate policy

| Item | Detail |
| --- | --- |
| Class | Approved decision. The cause of the copies stays unresolved (DEF-01) |
| Source | Spec Section 0.4 and decision P-01, `PRPO_DUP_POLICY = distinct` by default. Audit plan Section 7.4 proposed the distinct view for line-level marts |
| Correction | **Both supersede.** No default policy exists and `PRPO_DUP_POLICY` is retired. There are two parallel views: `original_rows` (11,609) and `exact_distinct_rows` (6,189), plus duplicate-group metadata |
| Status of the views | The distinct view is a sensitivity scenario, not the definitive business truth. Exact duplicate rows are not assumed to be invalid. Every financial or procurement metric must name its view |
| Limitation of `original_rows` | If repeated rows are copies of one document line, counts, quantities and amounts are overstated |
| Limitation of `exact_distinct_rows` | If repeated rows are real separate transactions, counts, quantities and amounts are understated |
| Implementation impact | `src/preprocessing/prpo_views.py`, `data/interim/prpo_views/`, `data/interim/duplicates/prpo_duplicate_groups.csv`. Every view row has an `analysis_view` label |
| Validation | `VIEW-01` to `VIEW-07`, `DUP-*.prpo`. Test `test_prpo_views_preserve_and_separate_records` |

### COR-10. Directory layout and storage format

| Item | Detail |
| --- | --- |
| Class | Approved decision |
| Source | Spec Appendix C |
| Stated | `caliber_supply_chain/`, `data/staged`, `data/conformed`, `data/marts`, Parquet, and checksums inside `data/raw/` |
| Correction | `final_caliber26/`. `data/interim/staged`, `data/interim/conformed`, `data/processed`. CSV read back through `read_staged`. Checksums in `data/reference/`, so `data/raw/` holds only the six workbooks |
| Rationale | Reuses the existing repository, avoids adding pyarrow, and keeps files reviewable |
| Limit | CSV stores no types. Staged tables must be loaded with `read_staged`. A plain `read_csv` or opening in Excel can damage long identifiers |
| Validation | `CSV-01.*`, `CSV-02.*`. Tests `test_csv_round_trip_preserves_values`, `test_exactly_six_workbooks_are_in_data_raw` |

### COR-11. Run timestamp on rows

| Item | Detail |
| --- | --- |
| Class | Technical design |
| Source | Spec Section 0.3, `load_ts` on every row |
| Correction | Removed from rows. Run times appear only in `outputs/reports/run_metadata.json` and `pipeline.log` |
| Rationale | A timestamp on each row makes every build differ, which would defeat reproducibility checks |
| Validation | Test `test_rebuilds_in_new_processes_produce_identical_files` compares every generated byte across two processes |

### COR-12. Reference dates

| Item | Detail |
| --- | --- |
| Class | The counts are confirmed by data. The cutoff itself is an unresolved assumption (A-01) |
| Source | Spec Section 2.4: D4 uses DATA_CUTOFF, D10 uses a fixed report date |
| Observed | Start of cycle is after 2026-09-30 on 487 rows and after 2026-11-04 on 344 rows |
| Correction | `DATA_CUTOFF` (2026-09-30) is the single reference for future-date flags. The 344 count is kept only to reproduce Spec D10 |
| Validation | `EXP.mitem.start_after_cutoff`, `EXP.mitem.start_after_audit_date` |

### COR-13. Criticality ranking and scoring

| Item | Detail |
| --- | --- |
| Class | Unresolved (DEF-03) |
| Source | Discovery Report E04, E18 and Opportunity J use "highest criticality" and a weighted score. Spec S07 and Section 5.6 forbid ranking or scoring before DEF-03 |
| Correction | The Specification's rule applies. Criticality and priority are stored as unordered categories. No ranking or score exists |
| Implementation impact | Any later score must be labelled a scenario, with its assumptions and a sensitivity test |
| Validation | `TYP-04.*` confirms category columns are unordered |

### COR-14. Diagram grains and cardinality

| Item | Detail |
| --- | --- |
| Class | Confirmed by data |
| Source | Data Context & Relationship Diagram, Join Keys and Table summary |
| Stated | PR PO: "One PR item linked to one PO item". BoM: "One material assigned to one FuncLoc". Notif History to Movement Material on Order: 1 : N |
| Observed | PR PO keys repeat 5,420 times on all rows and 0 on distinct rows. BoM pairs repeat 230 times on all rows and 0 on distinct rows. On Order, 52 orders each sit on 2 notifications, all at different functional locations, so the observed relationship is N:N |
| Rationale | Observed data decides. The diagram remains the source of intended meaning |
| Implementation impact | No join may assume the diagram's cardinality. Phase 3 will audit each join. `candidate_foreign_keys.csv` records the observed values |
| Validation | `EXP.prpo.pr_key_repeats.*`, `EXP.bom.pair_repeats.*`, `EXP.notif.orders_on_multiple_notifications`, `EXP.notif.shared_orders_on_same_location` |

### COR-15. Case designation

| Item | Detail |
| --- | --- |
| Class | Approved decision |
| Source | Audit plan Sections 1 and 3.3 raised a discrepancy between the Case 2 document and the Case 3 diagram |
| Correction | The project owner confirms this is the CALIBER 2026 final-round **Case 3, Spare Part Intelligence**. The Case 2 document, RCA reports and research are context only |
| Still open | The Case 3 casebook is not in the repository (A-03). No key links the workbooks to the Case 2 incident data |
| Validation | Document review |

### COR-16. Conformed PR PO table and flag names

| Item | Detail |
| --- | --- |
| Class | Technical design, follows COR-09 |
| Source | Spec Sections 2.1, 3.1 S06 and S09, and Appendices B and C: `prpo_line` filtered by policy, `dup_group_id`, `dup_count`, `dup_rank`, `is_dup_extra`, `requested_lead_days`, `promised_lead_days` |
| Correction | `fact_prpo_line` keeps all 11,609 rows, and `in_exact_distinct_rows` selects the sensitivity view. Duplicate columns stay `content_group_id`, `occurrence_count` and `occurrence_rank`. `is_repeat_occurrence` replaces `is_dup_extra`. Intervals are `requested_interval_days` and `promised_interval_days` |
| Rationale | A table filtered by policy would restore the default view COR-09 retired. "Extra" implies the row is wrong, which is not established. "Lead" invites reading a promise as an achieved lead time |
| Validation | `CONF-01`, `CONF-02`, `CONF-03`, `CONF-07`, `CONF-11` |

### COR-17. Population-based flags per view

| Item | Detail |
| --- | --- |
| Class | Technical design, follows COR-09 |
| Source | Spec Appendix B lists one `flag_outlier_<measure>` and one `flag_extreme_interval` |
| Observed | The two PR PO views give different results, because copies change a material's median and spread. `pr_quantity` flags 113 rows in `original_rows` and 21 in `exact_distinct_rows`, not simply in proportion to rows |
| Correction | These flags are stored once per view, for example `flag_outlier_pr_quantity__original_rows`. A row outside a view holds a blank. Movement follows the same pattern, because no Movement policy is confirmed (A-05) |
| Validation | `CONF-08.*`. Test `test_outlier_populations_differ_by_view_so_flags_are_held_per_view` |

### COR-18. Non-IDR suppliers

| Item | Detail |
| --- | --- |
| Class | Unresolved |
| Source | Spec 3.1 S07: `is_foreign` = currency not IDR |
| Correction | The column is `is_non_idr_currency`. An invoice currency does not establish that a supplier is foreign, and supplier names are likely synthetic (P-12) |
| Validation | `CONF-11.dim_supplier` |

### COR-19. Notification repeats and reference codes

| Item | Detail |
| --- | --- |
| Class | Confirmed by data |
| Source | Spec Section 2.2: "8 rows repeat location, description and date". Spec Section 2.10: 4.8% of descriptions start with a bracketed code |
| Observed | 8 is the count of extra rows. They form 8 groups covering 16 rows. 279 descriptions start with a code (4.8%), and 9 more use the form `PSM25/[...]`, so `desc_ref_code` is filled on 288 rows |
| Implementation impact | `is_partial_dup_group` is true on all 16 rows. A review of a random 50 of the 279 found the pattern consistent. Extraction is pattern-based and does not interpret the code |
| Validation | `EXP.flag.fact_notification.partial_dup_extra_rows`, `EXP.flag.fact_notification.desc_ref_code_rows` |

### COR-20. Outliers where no threshold exists

| Item | Detail |
| --- | --- |
| Class | Technical design, assumption A-10 |
| Source | Spec Section 2.8 gives a robust z, then an IQR fence |
| Gap | Neither is defined when the wider group has IQR = 0 or too few records |
| Correction | Those values are reported as `not_assessed` and not flagged. Under a literal fence of Q3 + 3 x 0, any value above Q3 would be flagged. This affects 17,971 of 20,423 Installed Qty pairs, and 768 Movement rows on `all_rows` (9 on distinct rows) |
| Validation | Test `test_no_spread_is_reported_as_not_assessed_rather_than_flagged` |

### COR-21. Movement policy replaced by two scenarios

| Item | Detail |
| --- | --- |
| Class | Approved decision |
| Source | Spec Section 0.4 `MOVE_DUP_POLICY = raw`, with a distinct sensitivity build. Spec M-01 |
| Correction | `MOVE_DUP_POLICY` is retired. Scenario A (all eligible records) and Scenario B (excluding rule C1 copies) are parallel, and neither is the base case. Each is calculated from its own records, with a material-level comparison |
| Implementation impact | `movement_copy_classification` holds every row with flags and reasons. Spec's `n_issue_lines_dup_extra` becomes `n_repeat_lines_included` |
| Validation | `MART-10` to `MART-29` |

### COR-22. M1 in two parallel views

| Item | Detail |
| --- | --- |
| Class | Approved decision, follows COR-09 |
| Source | Spec Section 5.1: grain one PR item under a default distinct policy, expected 6,189 rows |
| Correction | Each M1 table exists once per view, in separate files. The `original_rows` line table has 11,609 rows keyed on `source_row`, and the `exact_distinct_rows` table has 6,189 keyed on the PR item |
| Validation | `MART-04`, `MART-30` to `MART-38` |

### COR-23. Unit amount as a labelled scenario

| Item | Detail |
| --- | --- |
| Class | Unresolved (DEF-05, A-13) |
| Source | Spec P-04, S12: `implied_unit_amount` |
| Correction | Named `implied_unit_amount_scenario`, and built only in M1 and M2. A check fails if a unit amount column lacks the word scenario. It was left out of the conformed layer on purpose |
| Observed | Within a material, the highest value is typically 2.04 times the lowest |
| Validation | `MART-03`, `MART-33` |

### COR-24. Mart storage and metadata

| Item | Detail |
| --- | --- |
| Class | Technical design |
| Source | Spec Appendix C: `data/marts/`, Parquet, one metadata file per mart |
| Correction | `data/processed/`, CSV, and a single `mart_metadata.json` with an entry per table: grain, key, types, column descriptions, parameters, policies and source checksums |
| Validation | `MART-01`, `MART-02`, `MART-50` |

---

## Implementation notes

These do not contradict the Specification. They record what has deliberately been left out so far.

| Item | Spec reference | Status |
| --- | --- | --- |
| `implied_unit_amount` in the conformed layer | P-04, S12 | Not derived there. See COR-23 for the labelled column in M1 and M2 |
| `item_text_group` | I-05 | Not built. The Specification requires a reviewed synonym map, and none exists |
| `tag_class_candidate`, `is_line_pattern` | F-04 | Not built. They need a sample review, and nothing yet uses them |
| `candidate_kit` | I-06, X-03 | Not built. It belongs to M5, which is not approved. R11 sizes it at 29,913 rows |
| Stock cover and days of supply | Not in the Specification | Not built. They would compare undated stock with dated flows (DEF-12) |
| `priority_rank`, `stock_status`, criticality ranking | N-06, B-03, F-03 | Not built. Definitions are open. `CONF-11` fails if such a column appears |
| Due-date projection | I-02, S07 | Not run (DEF-11) |
| Cycle mapping | I-01, Appendix A | Built as `map_cycle`, with `*_proposed` columns, pending DEF-10 |
| Trimmed text copies | Section 0.2 lists these under L1 | In the conformed layer. Staged text stays verbatim |

## New rule from Phase 1

**Excel error cells.** `pandas.read_excel` reads a cell such as `#N/A` as null without warning. None exist in the six workbooks. `TYP-01` and `ROW-03` would expose one in a future file, shown by test `test_excel_error_cell_is_caught_by_the_independent_checks`.
