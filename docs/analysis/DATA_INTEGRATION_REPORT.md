# CALIBER 2026 Data Integration Report: Phase 3

**Date:** 2026-11-04. **Project:** Case 3, Spare Part Intelligence. **Specification version:** `0.1+corrections-3`.

**Data status:** Source data documented as synthetic (dummy) in the Data Context & Relationship Diagram; not operational performance.

## 1. Summary

The conformed layer is built, and all 13 specification relationships are audited. Every fact table keeps all its source rows with unchanged values, and tables at a coarser grain record the source rows they represent. No marts or analyses are built.

**What this establishes:** tables can be joined safely under the conditions in Section 4, and flags match separately calculated counts.

**What it does not establish:** what the flags mean. **Only 15.93% of issue rows link to a notification**, so location-level consumption analysis covers a minority of issues. Plans do not state which parts they use, so plan-to-BoM pairs are not requirements.

## 2. Conformed tables

Location: `data/interim/conformed/`. Load with `read_conformed`, using the column types in `conformed_metadata.json`.

| Table | Grain | Rows | Columns | Rows in source |
| --- | --- | --- | --- | --- |
| `dim_functional_location` | One functional location | 14,484 | 18 | 14,484 |
| `dim_material` | One material, from BoM attributes | 7,481 | 31 | 20,653 BoM rows |
| `dim_supplier` | One supplier code | 124 | 5 | 11,609 PR PO rows |
| `map_cycle` | One cycle spelling. **Proposed, requires DEF-10** | 28 | 7 | Spec Appendix A |
| `bridge_fl_material` | One location and material pair | 20,423 | 15 | 20,653 BoM rows |
| `bridge_order_notification` | One order and notification pair | 5,242 | 10 | 5,795 notifications, of which 553 have no order |
| `fact_prpo_line` | One PR PO source row, across both views | 11,609 | 57 | 11,609 |
| `fact_issue` | One Movement source row | 17,518 | 35 | 17,518 |
| `fact_notification` | One notification | 5,795 | 41 | 5,795 |
| `fact_plan_item` | One maintenance item | 10,153 | 27 | 10,153 |

**Row accounting.** `bridge_fl_material` holds 20,423 pairs. Its `all_source_rows` and `occurrence_count` account for all 20,653 BoM rows, and together they rebuild Installed Qty per unit exactly. `dim_material` is allowed only because attributes never differ within a material, and the build stops if that stops being true.

**PR PO views.** `fact_prpo_line` has both views. `in_exact_distinct_rows` selects the sensitivity view, and selects exactly the same rows and amounts as the Phase 1 view. Flags that depend on a population are stored per view, such as `flag_outlier_pr_quantity__original_rows`. No view is the default, and every metric must name its view.

The step-by-step record is in `outputs/tables/transformation_log.csv`.

## 3. Relationship audit

Counts come from key values. Joins that multiply rows are measured but never stored. Relationship IDs follow Spec Section 4.2.

| ID | Parent to child | Keys | Observed | Child keys missing | Parent keys unused | Child rows matched | Join rows | Rows added |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R1 | Location to pair | Location | 1:N | 0 | 9,968 | 20,423 of 20,423 | 20,423 | 0 |
| R2 | Location to notification | Location | 1:N | 0 | 12,265 | 5,795 of 5,795 | 5,795 | 0 |
| R3 | Location to plan item | Location | 1:N | 0 | 8,699 | 10,153 of 10,153 | 10,153 | 0 |
| R4 | Material to issue | Material | 1:N | 0 | 5,551 | 17,518 of 17,518 | 17,518 | 0 |
| R5 | Material to PR PO, `original_rows` | Material | 1:N | 0 | 6,231 | 11,609 of 11,609 | 11,609 | 0 |
| R5 | Material to PR PO, `exact_distinct_rows` | Material | 1:N | 0 | 6,231 | 6,189 of 6,189 | 6,189 | 0 |
| R6 | Supplier to PR PO, `original_rows` | Supplier | 1:N | 0 | 0 | 11,609 of 11,609 | 11,609 | 0 |
| R7 | Order bridge to issue | Order | **N:N** | **3,881** | 4,187 | **2,791 of 17,518** | 2,851 | **60** |
| R8 | Location to attributed issue | Through order | 1:N | 0 | 13,791 | 2,731 of 2,731 | 2,731 | 0 |
| R9 | Issued to procured materials | Material, aggregated | 1:1 | 220 | 900 | | 1,030 | |
| R10 | Pair to linked issue | Location + material | Lookup | | | 644 of 2,791 (23.07%) | | |
| R11 | Plan item to pair | Location | **N:N** | 1,663 | 2,932 | 13,231 of 20,423 | **29,913** | 16,682 |
| R12 | Plan item to notification | Location | **N:N** | 1,089 | 4,655 | 3,123 of 5,795 | 6,959 | 3,836 |
| R13 | Location to plan item | Criticality, description | Equality test | | | 0 mismatches | | |

Source: `outputs/tables/relationship_audit.csv`, `outputs/reports/relationship_audit.md`. These match the Specification's expected values, with 29,913 replacing 30,245 for R11, per COR-06.

**Joins avoided.** Using raw BoM rows would have created 615,146 rows from Movement (35 times) and 293,658 from PR PO (25 times). Joining through `dim_material` adds none.

**Lookups in the build.** All 8 audited lookups kept their row count and found every parent. `audited_lookup` stops the build on a repeated key, a column collision or a required parent that is missing.

## 4. Conditions for use

| Relationship | Safe? | Condition |
| --- | --- | --- |
| R1, R2, R3, R6 | Yes | As lookups. For R6, name the PR PO view |
| R4, R5 | Yes | Through `dim_material` only, never through BoM rows |
| R7 | **Conditional** | Safe at order level. **Do not sum quantities after this join**, because shared orders repeat rows. Use the flags on `fact_issue` |
| R8 | **Conditional** | Only 2,731 of 17,518 issue rows have one location. Report that coverage |
| R9 | Yes | Only after aggregating both sides to material. Name the view |
| R10 | As a data quality measure | A match does not prove where a part was used |
| R11 | **No** for demand or requirements | Exploration only, in a table labelled as a hypothesis. Plans do not state their parts |
| R12 | Yes | At location grain only, after aggregating both sides |
| R13 | Not a join | Consistency test |

## 5. Issue attribution

| `fl_attribution` | Issue rows | % | Meaning |
| --- | --- | --- | --- |
| `unique` | 2,731 | 15.59 | The order leads to one location |
| `ambiguous` | 60 | 0.34 | The order is on two notifications at different locations. **Never allocated** |
| `none` | 14,727 | 84.07 | The order is not in Notif History |

Only 644 of the 2,791 linked rows (23.07%) have the issued material on the BoM of a linked location. The cause cannot be confirmed from the available data or documentation. It could reflect incomplete BoMs, orders covering other equipment, or data generation. Order prefixes are undefined (DEF-07), so the unlinked 84% cannot be interpreted yet.

## 6. Rules enforced by checks

`CONF-*` and `JOIN.*` in `outputs/tables/validation_results.csv`. Each has a test that damages real data and confirms the failure.

| Rule | Check |
| --- | --- |
| Facts keep every row, in source order | `CONF-01`, `CONF-02` |
| Source values and blanks are unchanged | `CONF-03` |
| Dimension and bridge keys are unique | `CONF-04` |
| The pair table accounts for every BoM row and rebuilds Installed Qty | `CONF-05` |
| Material attributes equal the staged BoM, with no conflicts | `CONF-06` |
| The view filter equals the distinct view in rows and amounts | `CONF-07` |
| View-specific flags are blank outside their view | `CONF-08` |
| Flag counts equal separately calculated counts | `CONF-09` |
| Shared orders are not allocated, and open notifications have no duration | `CONF-10` |
| No column applies an undefined rule, such as a ranking, stock status, FX or due date | `CONF-11`, `CONF-12` |
| Cycle spellings match Appendix A, and the mapping stays labelled as proposed | `CONF-13` |
| Conformed CSV files reload to identical values | `CONF-14` |

**Limit of `CONF-11`.** It checks column names against a list of known unapproved rules. It cannot detect an unapproved rule under an innocent name.

## 7. Assumptions in the conformed layer

| Item | Applied as | Register |
| --- | --- | --- |
| Data cutoff 2026-09-30 | Future-date flags, and censoring of open notifications | A-01 |
| Cycle readings | `map_cycle` and `*_proposed` columns only | DEF-10 |
| Outlier method | Flags only | A-10 |
| Reference-code pattern | `desc_ref_code`, after reviewing a random 50 rows | COR-19 |
| BoM attributes are material-level | Basis for `dim_material`, enforced by test | A-09 |

Not applied, because the definition is open: unit amounts (DEF-05), priority and criticality ranks (DEF-03, DEF-16), stock status (DEF-02), due-date projection (DEF-11), item-text synonyms, tag patterns and FX conversion.

## 8. Limitations

- **Synthetic data.** Patterns may reflect how the data was generated (A-02).
- **No business validation.** Flags and joins are verified against data and documents, not against a domain expert.
- **Stock is undated (DEF-12).** The raw comparisons on `dim_material` are not shortage or excess findings, and zero stock is not a stockout.
- **Promised is not actual.** No receipt dates exist, so no delivery performance can be measured (DEF-06).
- **Notifications are not failures (DEF-09).**
- **Environment.** Verified on Python 3.14.3 on macOS only.
