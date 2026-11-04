# CALIBER 2026 Data Quality Report: Phases 0 to 3, marts M1 to M3 and simulation feasibility evidence

**Date:** 2026-11-04. **Project:** Case 3, Spare Part Intelligence. **Specification version:** `0.1+corrections-3`.

**Data status:** Source data documented as synthetic (dummy) in the Data Context & Relationship Diagram; not operational performance.

## 1. Summary

The six workbooks were ingested with all 80,212 rows intact, and every cell was confirmed against an independent read of the file. All 750 validation checks and 354 automated tests pass. No source file changed. Sections 12 to 15 add the Phase 2 evidence. Conformed tables are covered in `DATA_INTEGRATION_REPORT.md`, marts in `DATA_MART_REPORT.md`, and simulation feasibility in `SIMULATION_FEASIBILITY_ASSESSMENT.md`. No simulation has been run.

**What this establishes:** the data arrives in the pipeline exactly as supplied, can be rebuilt identically, and is internally consistent on the rules tested.

**What it does not establish:** that the data is correct, or what its unusual patterns mean. Passing means the data matches earlier counts and structural rules. 16 business definitions remain open (`ASSUMPTIONS_REGISTER.md`), and a repeated-maximum pattern is unexplained (Section 15).

## 2. Validation results

| Group | Checks | Pass | Fail | Warn | What it covers |
| --- | --- | --- | --- | --- | --- |
| Accessibility | 6 | 6 | 0 | 0 | Each workbook exists in `data/raw/` |
| Checksum | 6 | 6 | 0 | 0 | SHA-256 matches the audit baseline |
| Worksheets | 12 | 12 | 0 | 0 | Sheet name. No hidden content, formulas, merged cells or row gaps |
| Columns | 6 | 6 | 0 | 0 | Header names and order |
| Data types | 24 | 24 | 0 | 0 | Cell storage, staged types, no time parts, unordered categories |
| Identifier integrity | 54 | 54 | 0 | 0 | Patterns, no float damage, no stray spaces |
| Row preservation | 18 | 18 | 0 | 0 | Row counts, source row numbers, **every cell against the file's XML** |
| Lineage | 12 | 12 | 0 | 0 | Source file, sheet and row hash |
| Missing values | 15 | 15 | 0 | 0 | Blanks only where documented and structurally explained |
| Duplicates | 24 | 24 | 0 | 0 | Labelling removes nothing and matches direct comparison |
| PR PO views | 11 | 11 | 0 | 0 | Both views preserve and trace all source rows |
| Round trip | 12 | 12 | 0 | 0 | Staged CSV reloads to identical values |
| Expected values | 272 | 272 | 0 | 0 | Counts match documented values: 135 from Phase 1, 94 from Phases 2 and 3, 30 from marts, 13 from simulation feasibility |
| Conformed tables | 101 | 101 | 0 | 0 | Facts keep every row and value, keys are unique, flags match separate counts, no unapproved rule applied |
| Relationships | 39 | 39 | 0 | 0 | Every lookup keeps its row count and finds its parent |
| Marts | 126 | 126 | 0 | 0 | Keys, reconciliation to conformed tables, scenario and view separation, no undefined rule applied |
| Simulation design | 12 | 12 | 0 | 0 | Population rules, arithmetic, and no simulated result or money figure at this stage |
| **Total** | **750** | **750** | **0** | **0** | |

Source: `outputs/tables/validation_results.csv`, `outputs/reports/validation_report.md`.

### Automated tests

354 tests pass, both in the project environment and in a new environment installed from `requirements.txt`. They include:

- **Failure detection (85 tests).** These damage a copy of the data and confirm the checks catch it. Examples are one changed cell, one lost row, a trimmed description, a damaged identifier and a modified workbook. One runs end to end, confirming a changed workbook makes the pipeline report the failure and exit with code 1.
- **Logic on hand-checkable data.** Leading zeros, text such as "NA", blanks, duplicate labelling, view totals and key assessment.
- **Recalculation without project code.** Key conformed flags are recalculated from the CSV files using only the Python standard library: the distinct view, requested-before-PR, location attribution, the BoM pair match, and the robust z on all 10,645 assessed Movement rows.
- **Reproducibility.** Two full rebuilds in separate processes with different hash seeds produce byte-identical files.

### Failures during development

Four tests failed on their first run. None involved the real data. The first two were in Phase 1 and the others in Phases 2 and 3. No mart test failed on its first run, which is why 31 mart tests deliberately damage data to confirm the checks can fail.

| Test | Cause | Resolution |
| --- | --- | --- |
| `test_text_that_looks_null_stays_text[#N/A]` | A real pandas behaviour: an Excel error cell is read as null without warning | The six workbooks have no error cells. The case was replaced with a test proving the independent checks would catch one. Recorded in `DATA_SPECIFICATION_CORRECTIONS.md` |
| `test_date_combination_is_marked_coincidental` | A mistake in the test's data. The date column alone was already unique | Test data corrected. Code unchanged |
| `test_threshold_is_strictly_above_3_5` | My hand calculation was wrong. Six values have a median of 11, not 10 | Test rewritten with seven values, and recalculated. Code unchanged |
| `test_holm_correction_by_hand` | My expected value was wrong. Holm caps 0.9 x 2 at 1.0 | Expected value corrected. Code unchanged |

## 3. Source integrity

| Workbook | Data rows | Columns | Size (bytes) | Worksheets | Status |
| --- | --- | --- | --- | --- | --- |
| PR PO | 11,609 | 18 | 1,375,240 | Data | Consistent with audit baseline |
| Movement Material | 17,518 | 7 | 708,571 | Data | Consistent with audit baseline |
| Notif History | 5,795 | 12 | 378,378 | Data | Consistent with audit baseline |
| Mitem & Mplan | 10,153 | 9 | 638,417 | Data | Consistent with audit baseline |
| BoM | 20,653 | 9 | 987,174 | Data | Consistent with audit baseline |
| FuncLoc list | 14,484 | 3 | 373,573 | Data | Consistent with audit baseline |

Source: `data/reference/source_manifest.json`.

**Checksum scope.** These checksums establish consistency with the audit baseline of 2026-11-04, not authenticity against organiser-issued checksums. None were supplied.

**BoM move.** `BoM.xlsx` moved from the project root to `data/raw/`. Its SHA-256 (`e87f47d6...3065e86`), size and modification time were identical before and after. Record: `data/reference/bom_relocation_record.json`.

**Provenance signal.** All six files were written by openpyxl 3.1.5 between 2026-11-03 01:53:56 and 01:54:15 UTC. This is consistent with the diagram's synthetic-data statement but does not prove it.

## 4. Data types

Default `pandas.read_excel` is **not safe** for these files. It converts text identifiers to numbers.

| Column | Stored in file as | Default `read_excel` gives | Pipeline gives |
| --- | --- | --- | --- |
| Purchase Requisition, Purchase Order, material numbers | Text | `int64` | `string` |
| Notif Order (553 blanks) | Text | `float64` | `string` with nulls |
| Mitem Priority | Text | `int64` | Unordered `category` |
| PR-Plant | Text | `int64` | `string` |

No identifier in the current files has a leading zero, so no value would be visibly damaged today. The approach protects against future files and accidental arithmetic.

## 5. Missing values

Blanks occur in only three columns. All three coincide exactly with a structural rule, so they are kept as null. Nothing is imputed.

| Column | Blanks | Rule that explains them |
| --- | --- | --- |
| Notif History, Completion by Date | 1,305 | Exactly the In Progress rows |
| Notif History, Order | 553 | All on In Progress rows |
| FuncLoc list, FuncLoc Criticallity | 33 | Exactly the SITE rows |

## 6. Duplicates

Duplicates are detected and labelled. **No source record is removed.**

| Dataset | Rows | Distinct | Extra copies | % | Occurrence pattern (times: rows) | Adjacent gaps | Median gap (rows) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PR PO | 11,609 | 6,189 | 5,420 | 46.69 | 1: 2,589; 2: 2,300; 3: 780; 4: 520 | 1 of 5,420 | 2,627 |
| Movement Material | 17,518 | 16,655 | 863 | 4.93 | 1: 15,835; 2: 788; 3: 23; 4: 7; 5: 2 | 429 of 863 | 2 |
| BoM | 20,653 | 20,423 | 230 | 1.11 | 1: 20,193; 2: 230 | 51 of 230 | 3 |
| Notif, Mitem, FuncLoc | | | 0 | 0 | | | |

The very different gaps suggest PR PO copies arise differently from those in Movement and BoM. The cause of any of them cannot be confirmed from the available data or documentation.

### PR PO dual views

Per Decision 4, both views exist side by side.

| View | Rows | Status | Limitation |
| --- | --- | --- | --- |
| `original_rows` | 11,609 | All source rows, unchanged | If repeated rows are copies of one document line, counts, quantities and amounts are overstated |
| `exact_distinct_rows` | 6,189 | First occurrence per group. **Sensitivity scenario, not the definitive business truth** | If repeated rows are real separate transactions, counts, quantities and amounts are understated |

Group metadata covers 3,600 groups with source row references, occurrence counts and per-group totals. All 3,600 are confirmed identical in every source column, and no business key is shared with different content.

| Metric | Group | `original_rows` | `exact_distinct_rows` | Ratio |
| --- | --- | --- | --- | --- |
| Rows | | 11,609 | 6,189 | 1.88 |
| PO-Item Amount | IDR | 168,836,490,165 | 89,210,784,211 | 1.89 |
| PO-Item Amount | USD | 310,714.71 | 139,557.65 | 2.23 |
| PO-Item Amount | EUR | 161,470.86 | 99,266.04 | 1.63 |
| PO-Item Amount | JPY | 17,669,735 | 7,623,969 | 2.32 |
| PO-Item Amount | SGD | 9,569.36 | 9,569.36 | 1.00 |
| PR-Quantity | EA | 13,056,739 | 6,925,149 | 1.89 |
| PR-Quantity | KG | 13,370,209 | 7,180,009 | 1.86 |
| Requested interval, median days | | 37 | 37 | 1.00 |
| Promised interval, median days | | 42 | 42 | 1.00 |
| Requested date before PR date, rows | | 630 | 324 | 1.94 |
| Promised date before PR date, rows | | 6 | 2 | 3.00 |

Totals depend heavily on the view. Median intervals do not. The full table is in `outputs/tables/prpo_view_comparison.csv`. Amounts are never added across currencies, and quantities are never added across units. Intervals use requested or promised dates, because no actual receipt date exists.

## 7. Candidate keys

Keys were tested on identifier and date columns, alone and combined up to three columns, on all rows and on distinct rows.

| Dataset | Candidate | Repeats, all rows | Repeats, distinct rows | Assessment |
| --- | --- | --- | --- | --- |
| FuncLoc list | Functional Location | 0 | 0 | Unique |
| Notif History | Notification | 0 | 0 | Unique |
| Mitem & Mplan | Maintenance Item | 0 | 0 | Unique |
| BoM | Functional Location + Material | 230 | 0 | Unique only after setting aside exact copies |
| PR PO | PR + PR-Item | 5,420 | 0 | Unique only after setting aside exact copies |
| PR PO | PO + PO-Item | 5,420 | 0 | Unique only after setting aside exact copies |
| Movement | Date + Material + Order | 1,171 | 308 | Not unique. **Movement has no natural key** |

**Uniqueness alone does not make a business key.** The search also found `purchase_requisition + material_no + po_item`, which adds nothing to the simpler PR key. Two combinations that include a date are unique by chance. Those are labelled coincidental.

## 8. Candidate foreign keys

Pairs were discovered from overlapping values. **No tables were joined.** Join sizes are calculated from key frequencies. Full relationship validation is in `DATA_INTEGRATION_REPORT.md`.

| Column A | Column B | Shared | A covered | B covered | Observed | Raw join rows | In diagram |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BoM location | FuncLoc location | 4,516 | 100% | 31.18% | N:1 | 20,653 | 1:N |
| Notif location | FuncLoc location | 2,219 | 100% | 15.32% | N:1 | 5,795 | 1:N |
| Mitem location | FuncLoc location | 5,785 | 100% | 39.94% | N:1 | 10,153 | 1:N |
| Movement material | BoM material | 1,930 | 100% | 25.80% | N:N | **615,146** | Unspecified |
| PR PO material | BoM material | 1,250 | 100% | 16.71% | N:N | **293,658** | Unspecified |
| Movement order | Notif order | 1,003 | 20.54% | 19.33% | N:N | 2,851 | 1:N |
| Mitem location | BoM location | 2,853 | 49.32% | 63.18% | N:N | 30,245 | Indirect |
| PR PO material | Movement material | 1,030 | 82.40% | 53.37% | N:N | 759,280 | No |
| Notif location | BoM location | 1,380 | 62.19% | 30.56% | N:N | 88,510 | No |
| Notif location | Mitem location | 1,130 | 50.92% | 19.53% | N:N | 6,959 | No |

**New finding: identifiers overlap by coincidence across different domains.**

| Column A | Column B | Shared values |
| --- | --- | --- |
| PR PO, Purchase Order | BoM, Material No | 58 |
| PR PO, Purchase Order | Movement, Material Number | 9 |
| PR PO, Supplier Code | Mitem, Maintenance Item | 33 |

These have different meanings and no documented relationship. Joining on value alone would produce false matches. They are labelled `value_overlap_only_not_supported_by_name_or_diagram`.

## 9. Potential data quality issues

All are flagged only. Source values are unchanged. Full list: `outputs/tables/data_quality_findings.csv`.

| Dataset | Finding | Count | View or grain | Related item |
| --- | --- | --- | --- | --- |
| PR PO | Rows repeating an earlier row in all 18 columns | 5,420 | original rows | DEF-01 |
| PR PO | Requested date before PR date | 630 / 324 | original / distinct | DEF-06 |
| PR PO | Promised date before PR date | 6 / 2 | original / distinct | DEF-06 |
| PR PO | Requested date after assumed cutoff | 1,682 / 891 | original / distinct | A-01 |
| PR PO | Promised date after assumed cutoff | 1,467 / 766 | original / distinct | A-01 |
| PR PO | Description with surrounding spaces | 191 rows | original rows | |
| BoM | Rows repeating an earlier row | 230 | all rows | |
| BoM | Non Stock materials holding stock | 1,683 | one row per material | DEF-04 |
| BoM | Stock Item materials at zero stock | 472 | one row per material | DEF-02 |
| BoM | Stock Item materials below Min.Qty | 504 | one row per material | DEF-02 |
| BoM | Stock Item materials above Max.Qty | 1,380 | one row per material | DEF-02 |
| BoM | Non-integer Stock rows, including 0.5 EA | 3 | all rows | |
| BoM | Non-integer Installed Qty, all in unit M | 89 | all rows | DEF-15 |
| BoM | Trimmed descriptions shared across material numbers | 133 | one row per material | |
| Movement | Rows repeating an earlier row. No document number exists | 863 | all rows | A-05 |
| Movement | Same date, material and order with differing quantities | 297 groups | all rows | |
| Movement | Orders with no matching notification order | 3,881 | distinct orders | DEF-07 |
| Notif | Orders on two notifications at different locations | 52 | distinct orders | A-07 |
| Notif | Required Start before notification date | 370 | all rows | DEF-14 |
| Notif | Created On differs from Notification Date | 61 | all rows | DEF-14 |
| Notif | Notifications in May 2025, far above later months | 1,463 | all rows | A-08 |
| Mitem | Distinct spellings of the maintenance interval | 28 | all rows | DEF-10 |
| Mitem | Start of cycle after assumed cutoff | 487 | all rows | DEF-11 |
| FuncLoc | Null criticality on SITE rows | 33 | all rows | DEF-03 |

Stock comparisons are raw counts. They are not findings about shortage or excess, because Min.Qty and Max.Qty are undefined and Stock is undated. Zero stock is not called a stockout.

## 10. Known limitations

- **Expected-value checks confirm consistency, not correctness.** Several expected values come from the same earlier inspection. Seven were recorded at a build, because the documents quoted only percentages or other forms of the count. They are marked in `data/reference/expected_values.json`.
- **The independent XML reader was written for this project.** It shares no code with pandas or openpyxl, but it is not itself an external authority.
- **CSV stores no types.** Staged tables must be loaded with `read_staged`. Opening them in Excel may damage long identifiers.
- **Environment.** Verified on Python 3.14.3 on macOS only.
- **Tests of association cannot show a cause.** Finding no association with measured fields says nothing about fields the data does not contain.
- **Items not built.** Item-text groups, tag patterns and marts M4 to M6. See the implementation notes in `DATA_SPECIFICATION_CORRECTIONS.md`.

## 11. Output locations

| Output | Location |
| --- | --- |
| Per-dataset profiles | `outputs/reports/profile_*.md` |
| Cross-dataset summary | `outputs/reports/profiling_summary.md`, `profiling_summary.json` |
| Validation | `outputs/reports/validation_report.md`, `outputs/tables/validation_results.csv` |
| Profiling tables | `outputs/tables/` |
| Staged tables | `data/interim/staged/` |
| PR PO views and metadata | `data/interim/prpo_views/` |
| Duplicate-group metadata | `data/interim/duplicates/` |
| Duplicate evidence | `outputs/reports/duplicate_evidence.md`, `outputs/tables/prpo_copy_*.csv`, `movement_duplicate_sensitivity.csv` |
| Exception lists | `outputs/exceptions/`, `outputs/tables/exception_summary.csv` |
| Outlier flags | `outputs/exceptions/outliers.csv`, `outputs/tables/outlier_summary.csv` |
| Repeated maximum values | `outputs/tables/repeated_maximum_values.csv` |

## 12. Phase 2: PR PO duplicate evidence

The audit's tests now run in tested pipeline code, and the results match the audit. **Cause: Cannot be confirmed from the available data or documentation.** This evidence chooses no policy, and both views remain.

**Key structure.** Business keys repeat 5,420 times on `original_rows` and 0 times on `exact_distinct_rows`. No key carries different content. PR item to PO item is exactly 1:1 on distinct rows. No two rows with different keys match on date, material, quantity, amount and PO. Two rows match on date, material and quantity alone.

**Is a copy count shared within a document?** If whole documents were repeated, the observed share would sit far above the shuffled range. It sits inside the range. Calculated on `exact_distinct_rows`, 200 shuffles, seed 42.

| Grouping | Documents with several lines | Observed share | Shuffled mean | Shuffled range | One-sided p |
| --- | --- | --- | --- | --- | --- |
| Purchase Requisition | 987 | 0.255 | 0.265 | 0.232 to 0.306 | 0.76 |
| Purchase Order | 1,151 | 0.125 | 0.142 | 0.118 to 0.166 | 0.96 |
| Material | 877 | 0.144 | 0.151 | 0.123 to 0.184 | 0.76 |

A test on constructed data confirms this test can detect document-level repetition when it exists.

**Copy count against other fields.**

- **Numeric fields.** The largest |Spearman rho| across 11 tests is 0.021, and the smallest p is 0.099. Amount is tested within IDR, and quantity within EA and KG.
- **Categories.** Purchasing group is the only result below 0.05 (p = 0.026, Cramer's V = 0.064). After a Holm correction across the seven tests it is p = 0.18, so **no category shows an association after correction**. In some tests many cells have a low expected count (60% for currency), so those p-values are approximate.

**What this means.** Copy counts relate to nothing measured here. This is compatible with row-level replication, or with an export joined to an unseen child table. It is less compatible with whole documents being repeated. It cannot separate those explanations, or rule out a cause involving fields not supplied.

## 13. Phase 2: Movement duplicates

No document number exists, so copies cannot be shown to be one event. **No policy is applied.** All rows are kept and both populations are compared.

| Measure | All rows | Exact-distinct rows | Change |
| --- | --- | --- | --- |
| Issue lines | 17,518 | 16,655 | -4.93% |
| Orders | 4,884 | 4,884 | None |
| Materials | 1,930 | 1,930 | None |
| Quantity, EA | 949,729 | 922,363 | -2.88% |
| Quantity, KG | 805,820 | 793,670 | -1.51% |
| Monthly issue lines | | | -2.85% to -6.41% |

**Totals are stable, but individual materials are not.** 400 materials lose at least one line in the distinct population. 220 change by more than 10% in quantity, 135 by more than 25%, and the largest by 80%. Rank order across materials stays similar (Spearman 0.963 on lines, 0.982 on quantity). Any per-material demand result should be checked under both populations.

Separately, 297 groups share a date, material and order but differ in quantity, covering 657 rows. These can be separate issues, so they are flagged and never merged.

## 14. Phase 2: exception lists and outlier flags

Each list holds the rows behind a count, for review. Rows remain in the tables. Where a list spans PR PO views, it says how many rows are in each.

| List | Rows | Distinct view | Related item |
| --- | --- | --- | --- |
| PR PO requested date before PR date | 630 | 324 | DEF-06 |
| PR PO promised date before PR date | 6 | 2 | DEF-06 |
| PR PO requested or promised date after cutoff | 1,953 | 1,034 | A-01 |
| Movement same key, different quantity | 657 | | A-05 |
| Notif Required Start before notification | 370 | | DEF-14 |
| Notif Created On differs | 61 | | DEF-14 |
| Notif same location, description and date | 16 | | |
| Plan Start of cycle after cutoff | 487 | | DEF-11 |
| Material Non Stock holding stock | 1,683 | | DEF-04 |
| Material fraction on a count unit | 1 | | DEF-15 |
| BoM non-integer Installed Qty, distinct pairs | 88 | | DEF-15 |
| Materials sharing a description | 597 | | X-04 |
| Orders on two notifications | 52 | | A-07 |

**Outlier flags** (assumption A-10) describe values and remove nothing.

| Measure | Population | Assessed | Flagged | % |
| --- | --- | --- | --- | --- |
| PR-Quantity | `original_rows` | 11,609 | 113 | 1.0 |
| PR-Quantity | `exact_distinct_rows` | 6,189 | 21 | 0.3 |
| Requested interval | `original_rows` | 11,609 | 1,499 | 12.9 |
| Requested interval | `exact_distinct_rows` | 6,189 | 766 | 12.4 |
| Promised interval | `original_rows` | 11,609 | 784 | 6.8 |
| Promised interval | `exact_distinct_rows` | 6,189 | 357 | 5.8 |
| Movement quantity | all rows | 17,518 | 1,404 | 8.0 |
| Movement quantity | exact-distinct rows | 16,655 | 1,341 | 8.1 |
| Stock | one row per material | 7,481 | 746 | 10.0 |
| Installed Qty | distinct pairs | 20,423 | 76 | 0.4 |

**Two cautions.** Rates near 10% are too high to treat a flag as an anomaly, so a flag means review. Results also depend on the population: PR-Quantity flags fall five-fold in the distinct view, while rows fall less than two-fold, so flags are held per view (COR-17).

## 15. Phase 2: repeated maximum values

Reviewing the top 20 flagged values for five measures found a pattern the counts did not show. Spec Section 2.8 asks for this review on every measure. Quantity, Stock, Installed Qty and promised interval were reviewed, and the remaining intervals are covered only by the table below. Exact copies are set aside first, so repeated rows do not cause it.

| Measure | Unit | Maximum | Rows at maximum | Materials at maximum | Next value |
| --- | --- | --- | --- | --- | --- |
| Movement quantity | KG | 23,135 | 7 | 7 | 5,000 |
| Movement quantity | EA | 5,700 | 23 | 9 | 5,000 |
| Movement quantity | L | 200 | 125 | 16 | 20 |
| Installed Qty | EA | 5,037 | 80 | 55 | 1,500 |
| Installed Qty | KG | 3,000 | 42 | 29 | 1,200 |
| Max.Qty | EA | 3,344 | 9 | 9 | 3,335 |
| Max.Qty | KG | 3,344 | 10 | 10 | 3,296 |
| Max.Qty | L | 3,344 | 1 | 1 | 1,614 |
| Promised interval, days | | 829 | 9 | 8 | 827 |

The 23,135 KG value appears on grease and on refractory castable alike. The value 3,344 is the Max.Qty peak in three different units. By contrast, Stock and PR-Quantity peaks each sit on one material (with one exception, on 6 materials in unit ASS at a value of 2).

**What this could mean.** A cap in a source system or in data generation is one possibility. Some values may be ordinary, such as 200 L, which could be a standard container size. **Cause: Cannot be confirmed from the available data or documentation** (A-11). Nothing is changed. Maximums, tail statistics and totals on Movement quantity, Installed Qty and Max.Qty should be read with this in mind.
