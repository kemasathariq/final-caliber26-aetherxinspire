# CALIBER 2026 Data Engineering Implementation Plan and Initial Audit

**Audit date:** 2026-11-04
**Status:** Phase 0 and Phase 1 implemented on 2026-11-04. See the status update below. Phases beyond Phase 1 await approval.
**Scope:** Read-only audit of the `final_caliber26` directory, the six Excel workbooks and the project documents.

**Changes made during the audit:** This report was the only project file created during the audit. No source file or workbook was changed, nothing was installed, and no Git command changed anything. The folder is not a Git repository. Audit scripts ran from a session scratchpad outside the project. The AETHER repository was not opened.

---

## Status update: through Step 5, M1 to M3 (2026-11-04)

The audit below is preserved as written. These points supersede it. Steps 2, 3 and 4 of Section 13 are complete, and so is M1 to M3 of Step 5. M4 to M6 and EDA have not started. Simulation has a design and feasibility assessment only: no engine exists, and none has been run. Implementation waits for review against the official Case 3 brief. See `DATA_QUALITY_REPORT.md`, `DATA_INTEGRATION_REPORT.md`, `DATA_MART_REPORT.md` and the three `SIMULATION_*` documents.

| Plan section | Update |
| --- | --- |
| Section 1 item 1, Section 3.3, Decision 1 | The project is confirmed as **Case 3, Spare Part Intelligence**. The Case 3 casebook is still not in the repository (A-03) |
| Section 1 item 5 | Refined. The Dictionary's type column records what default `read_excel` infers, not how the files store values. See COR-01 |
| Section 7.4, Decision 4 | **Dual views adopted.** The distinct view is a sensitivity scenario, not a default for marts. See COR-09 |
| Section 2.2 | Environment created at `~/.venvs/caliber26`. `read_excel` tested and matches an independent read in every cell |
| Section 11 | `BoM.xlsx` is now in `data/raw/`. Duplicate analysis is in `src/validation/`. Conformed tables are built by `src/preprocessing/conform.py`. `src/analysis/` is still empty |
| Section 13 | Steps 0 to 4 are complete. The Section 7 duplicate evidence is now reproduced by tested code |
| Section 14.1 | `requirements.txt` holds only what Phases 0 to 3 use, now including scipy. matplotlib, seaborn, notebook and nbconvert are added when a later phase needs them |
| Section 15 | Using this plan's numbering: Decisions 1 to 4 are settled. Decisions 5 and 6 proceed under the approved technical direction, with the cutoff held as assumption A-01. In Decision 7, the environment is created and Git initialisation is declined for this stage. Decisions 8 and 9 remain open |

### Git and data protection recommendation

Before the first commit:

| Item | Commit? | Reason |
| --- | --- | --- |
| `src/`, `tests/`, `requirements.txt`, `pytest.ini`, `README.md` | Yes | Source code and setup |
| `docs/analysis/*.md` | Yes, in a private repository | Reports quote counts and some source values |
| `data/reference/*.json` | Yes | Holds hashes and counts, no records |
| `data/raw/*.xlsx` | **No** | Competition-provided data. Redistribution terms are unconfirmed |
| `data/interim/`, `data/processed/`, `outputs/` | No | Generated, and contains source records |
| `docs/case/`, `docs/research/` | Decide first | Competition and third-party material. The article PDF may be copyrighted |

**Update:** the project owner created a `.git` folder for a new repository, so these rules are now in `.gitignore`. Nothing has been committed. `docs/case/` and `docs/research/` are not excluded, so decide on them before the first commit. Rules added:

```gitignore
data/raw/
*.xlsx
.pytest_cache/
```

Also use a **private** repository. The case document notes that submissions may become corporate property, so confirm the official terms before publishing anything. The AETHER repository should be checked for the same files before integration.

**Evidence labels used in this report**

| Label | Meaning |
| --- | --- |
| VERIFIED | Measured directly from the workbooks or read directly from a source document during this audit. |
| DOCUMENTED | Stated in a project document. Not independently provable from the data. |
| HYPOTHESIS | A possible explanation that has not been established. |
| UNCONFIRMED | "Cannot be confirmed from the available data or documentation." |

---

## 1. Findings that change the work

1. **The six workbooks do not belong to the case document in the repository.** The only case document covers Case 2, Intelligent Manufacturing Dashboard. The workbooks' only documentation is a diagram titled Case 3, Spare Part Intelligence. No case-level brief for the workbooks is in the repository.
2. **The data is documented as synthetic.** The diagram says so explicitly (Section 3). Findings describe this dataset, not plant performance.
3. **`BoM.xlsx` is not in `data/raw/`.** It is at the repository root. The other five workbooks are in `data/raw/`.
4. **The Data Preparation Specification is not approved.** It is labelled "Version 0.1 (draft for approval)", and every box on its approval checklist is unticked. Its default PR PO rule also conflicts with your instruction not to deduplicate automatically.
5. **The Data Dictionary's "current type" column is wrong for identifiers.** Identifiers are stored as text in the files, not as `int64` or `float64`. The float-repair step in the specification is therefore unnecessary.
6. **All PR PO row counts and totals depend on one unresolved duplicate decision.** The IDR amount is 168.84 billion on raw rows and 89.21 billion on distinct rows. Medians and concentration shares barely change (Section 7).
7. **No code exists yet.** `src/`, `tests/` and `notebooks/` contain only empty folders.

---

## 2. Repository and environment inventory

### 2.1 Repository

| Path | Status | Note |
| --- | --- | --- |
| `BoM.xlsx` | Present, misplaced | Expected under `data/raw/`. |
| `data/raw/` | 5 workbooks | FuncLoc list, Mitem & Mplan, Movement Material, Notif History, PR PO. |
| `data/interim/`, `data/processed/`, `data/external_research/` | Empty | |
| `docs/analysis/` | 5 documents, plus this report | Section 2.3. |
| `docs/case/` | 2 documents | Section 2.3. |
| `docs/research/` | 2 documents | Section 2.3. |
| `notebooks/`, `tests/` | Empty | |
| `src/analysis/`, `src/data/`, `src/preprocessing/`, `src/validation/` | Empty | No `.py` files anywhere. These folders are reused in the proposed design. |
| `outputs/figures/`, `outputs/reports/`, `outputs/tables/` | Empty | |
| `.gitignore` | Present | Ignores `data/interim/`, `data/processed/` and `outputs/`. |
| `README`, `requirements.txt`, config files | Absent | |
| `.git` | Absent | Not a Git repository. |

### 2.2 Environment

| Item | Finding |
| --- | --- |
| Python | 3.14.3 (system framework install) |
| Available | pandas 3.0.2, numpy 2.4.4, matplotlib 3.10.8, seaborn 0.13.2, scipy 1.17.1, scikit-learn 1.8.0, nbformat 5.10.4, notebook 7.5.5 |
| Missing | **openpyxl**, **pytest**, pyarrow |
| Consequence | `pandas.read_excel` cannot run yet. For this audit the workbook XML was parsed with the Python standard library. Phase 1 must confirm that `read_excel` returns identical values. **This has not been tested.** |
| Location risk | The repository is inside iCloud Drive. A virtual environment there would sync thousands of files, and iCloud can offload source files or create conflict copies. |

### 2.3 Documentation

| Document | Purpose | How this plan uses it |
| --- | --- | --- |
| `docs/analysis/CALIBER_DATA_DICTIONARY.md` (v0.1 draft) | Field definitions for 58 columns | Primary field reference, with the corrections in Section 6 |
| `docs/analysis/CALIBER_DATA_PREPARATION_SPECIFICATION.md` (v0.1 draft) | Layers, rules, relationships, marts, tests | Primary transformation reference once approved |
| `docs/analysis/CALIBER 2026 Analytical Discovery Report.md` | Preliminary observations and hypotheses | Investigation priorities only, not validated findings |
| `docs/analysis/consolidated_root_cause_analysis_reports.md` | Five RCA reports for Case 2 hero assets | Context only. No key links it to the workbooks (Section 3.3) |
| `docs/analysis/Caliber 2026 BCC _ Hackathon Analysis.md` | Case 2 strategic analysis | Context only |
| `docs/case/CALIBER_2026_Case_2_Complete_Final_Case.md` | Case 2 reference. Its appendices hold the strategic analysis, RCA reports, an equipment and incident dataset, and research notes | Case framing. It never mentions the six workbooks |
| `docs/case/Data Context & Relationship Diagram.pdf` | 2 pages: diagram, join keys, table grains | The only document that describes the workbooks directly |
| `docs/research/Chandra Asri Group_ ... Assessment.md` | Public-source company research | Business context only. It states "I could not access the four uploaded CALIBER documents", so it says nothing about these workbooks |
| `docs/research/Contoh process simulation petrokim.pdf` | 2017 journal article on naphtha cracking furnace simulation | Not relevant to this workstream |

---

## 3. Documentation discrepancy: synthetic data and case number

### 3.1 Exact source wording (VERIFIED)

From `docs/case/Data Context & Relationship Diagram.pdf`:

| Location | Exact text |
| --- | --- |
| PDF metadata, Title | `Caliber 2026 Hackathon - Case 3 - Data Relationship Diagram (Rev.1)` |
| Page 1, heading | `Case 3 - Spare Part Intelligence: Data Relationship Diagram` |
| Page 1, subheading | `Caliber 2026 Hackathon Day | Baseline dataset (dummy) | 6 Excel files, 1 sheet "Data" each` |
| Page 2, footnote | `All data is synthetic (dummy) and generated for the Caliber 2026 Hackathon. It mirrors the structure and relationships of the original system data, not its actual values.` |

The PDF metadata lists its author as `anonymous` and its creation time as 2026-11-03 01:48 UTC.

### 3.2 Is the data synthetic?

| Evidence | Finding | Label |
| --- | --- | --- |
| Diagram describes these workbooks | Column names and order match the diagram for all six files | VERIFIED |
| Diagram states the data is synthetic | Quoted above | DOCUMENTED |
| Workbook metadata | All six were written by `openpyxl` 3.1.5 (`Application: Microsoft Excel Compatible / Openpyxl 3.1.5`), with internal creation times between 2026-11-03 01:53:56 and 01:54:15 UTC | VERIFIED |
| Supplier names | 118 of 124 follow a four-word name ending in "PT" | VERIFIED |
| Second confirming document | None in the repository | VERIFIED absence |

**Conclusion.** The evidence supports treating the data as demonstration data. The metadata and name patterns are consistent with that, but they would not alone prove it, because a real export could also be re-saved by a script. Whether any specific value or pattern derives from real operations, and how closely patterns resemble real behaviour: **Cannot be confirmed from the available data or documentation.**

**How this affects interpretation**

- Findings describe this dataset. They must not be presented as actual Chandra Asri operations, spend, reliability or stock.
- A pattern may reflect how the data was generated rather than business behaviour. This applies especially to anomalies, duplicates and price dispersion.
- The data can demonstrate that a method and pipeline work. It cannot support a claim of realised or expected savings at the plant.
- Supplier names are not treated as real companies, and no external matching is proposed.
- Every generated output will carry the label: `Source data documented as synthetic (dummy); not operational performance.`

### 3.3 Which case does the data belong to?

| Item | Finding | Label |
| --- | --- | --- |
| Project instructions and case document | Case 2, Intelligent Manufacturing Dashboard | VERIFIED |
| Diagram | Case 3, Spare Part Intelligence | VERIFIED |
| Diagram's "Casebook data source" column | Refers to numbered casebook sections, such as "1. Spare Part Master Data". That casebook is not in the repository | VERIFIED absence |
| Case 2 document search | No reference to BoM, PR PO, Movement Material, Notif History, Mitem or FuncLoc | VERIFIED |
| Case 2 hero tags (PU-2101B, KO-3201, PM-4405B, HE-3301, BL-5702) | 0 matches in FuncLoc codes, FuncLoc descriptions or notification text | VERIFIED |
| Case 2 plant codes (ZCU, ARP, OPP and 9 others) | 0 matches in FuncLoc codes or descriptions. One incidental hit: "TKX" inside a reference code in one notification text | VERIFIED |
| About 800 tag-like codes in the Case 2 equipment and incident appendix | 0 exact matches to FuncLoc codes (a pattern-based check, indicative only) | VERIFIED |

**Conclusion.** The Case 2 materials and the six workbooks are two separate data universes with no shared key. Joining them, or attributing RCA findings to workbook records, is not supported.

Whether the final round expects Case 2 teams to use this dataset, and what business questions the Case 3 casebook asks: **Cannot be confirmed from the available data or documentation.** Decision 1 in Section 15 addresses this. The data engineering foundation is valid either way. The answer mainly affects how Phase 6 opportunities are framed.

---

## 4. Dataset inventory and integrity

All six workbooks opened and parsed without error. Each has one visible sheet named `Data`, with the header on row 1 and contiguous data rows. None has hidden rows or columns, formulas, merged cells, external links or tables. Each has an autofilter. (VERIFIED)

| Workbook | Path | Data rows x cols | Excel rows | SHA-256 baseline |
| --- | --- | --- | --- | --- |
| BoM | `BoM.xlsx` | 20,653 x 9 | 2 to 20654 | `e87f47d69a24ad81c232d7aaec820006ffd6f945b8529e97468c731583065e86` |
| FuncLoc list | `data/raw/FuncLoc list.xlsx` | 14,484 x 3 | 2 to 14485 | `9f6d306cef6952084a209993e4e8e7742f345cacfd207b556039412953165a82` |
| Mitem & Mplan | `data/raw/Mitem & Mplan.xlsx` | 10,153 x 9 | 2 to 10154 | `23e0b11894614c3aef8dfab6cd8c0d1369e67b11766c445555089fad00ed96c8` |
| Movement Material | `data/raw/Movement Material.xlsx` | 17,518 x 7 | 2 to 17519 | `3384208dda09d3a8c05d21d4fac9b38e77797bcf11b8d917964556386ca1ee3a` |
| Notif History | `data/raw/Notif History.xlsx` | 5,795 x 12 | 2 to 5796 | `7369419815352942613647692378cb6be64c251be92ce2125c12fdf684c3105e` |
| PR PO | `data/raw/PR PO.xlsx` | 11,609 x 18 | 2 to 11610 | `3f986b91d2ccc7e920486a6b15eb810d0676198b0b49fc674a3f7b817aec8f1a` |

**Limit of this check.** These hashes are a baseline from today. No reference checksum from the organisers exists, so whether these are the files as originally issued is unconfirmed.

### 4.1 Storage types in the files (VERIFIED)

| Stored as | Columns |
| --- | --- |
| Inline text | All identifiers and codes, including PR, PO, material, supplier, order, notification, plan, item numbers, plant and Mitem Priority |
| Numeric | PR-Quantity, PO-Item Amount, Quantity, Installed Qty, Min.Qty, Max.Qty, Stock |
| Date serial with no time part | All 10 date columns |

- No identifier has leading zeros, a decimal point, surrounding spaces or a non-digit character. Identifier tests are still needed to protect against future files and accidental casting.
- Blanks occur in only three columns: Notif `Order` (553), Notif `Completion by Date` (1,305) and FuncLoc `FuncLoc Criticallity` (33).

### 4.2 Temporal coverage (VERIFIED)

| Table | Event column | Range | Note |
| --- | --- | --- | --- |
| PR PO | PR-Date | 2025-05-04 to 2026-09-22 | September 2026 has 493 raw rows, against 605 to 773 in other months. The month may be incomplete |
| Movement | Posting Date | 2025-05-06 to 2026-09-30 | Peak November 2025 to January 2026 (1,860, 2,580 and 2,184 rows) |
| Notif History | Notification Date | 2025-05-02 to 2026-09-30 | 1,463 in May 2025, then 132 to 388 per month |
| Mitem & Mplan | Start of cycle | 2015-09-01 to 2029-12-12 | Not an event log |
| BoM, FuncLoc | None | | `Stock` is undated |

About 17 months of history cannot support a test of annual seasonality.

---

## 5. Data relationships and candidate keys

### 5.1 Candidate primary keys (VERIFIED)

| Table | Candidate key | Raw result | After setting aside exact copies | Diagram claim |
| --- | --- | --- | --- | --- |
| FuncLoc list | Functional Location | Unique | Same | Holds |
| Notif History | Notification | Unique | Same | Holds |
| Mitem & Mplan | Maintenance Item | Unique | Same | Holds |
| BoM | Functional Loc. + Material No | 230 repeats | Unique, 20,423 rows | Holds only after exact copies are set aside |
| PR PO | Purchase Requisition + PR-Item | 5,420 repeats | Unique, 6,189 rows | Holds only after exact copies are set aside |
| PR PO | Purchase Order + PO-Item | 5,420 repeats | Unique, 6,189 rows | Not stated as PK. Observed unique after setting aside copies |
| Movement | None | Identical rows exist in all 7 columns | No natural key is possible | Diagram lists keys, not a PK |

`source_row` serves as the row identity for every table. Movement has no other option.

### 5.2 Observed relationships (VERIFIED)

| # | Source to destination | Keys | Grain | Observed cardinality | Coverage | Row multiplication |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | FuncLoc to BoM | Functional Location = Functional Loc. | Location to pair | 1:N | 4,516 of 4,516 child keys match. 9,968 parents unused | None as a parent lookup |
| 2 | FuncLoc to Notif | Functional Location | Location to notification | 1:N, up to 114 per location | 2,219 of 2,219 match. 12,265 parents unused | None as a parent lookup |
| 3 | FuncLoc to Mitem | Functional Location | Location to item | 1:N, up to 8 per location | 5,785 of 5,785 match. 8,699 parents unused | None as a parent lookup |
| 4 | BoM to Movement | Material No = Material Number | Pair to issue | M:N on raw rows. 1:N only through a one-row-per-material table | 1,930 of 1,930 match. 5,551 BoM materials never issued | **615,146 rows** from 17,518 on a raw join |
| 5 | BoM to PR PO | Material No = PR-Material | Pair to PR line | M:N on raw rows. 1:N only through a one-row-per-material table | 1,250 of 1,250 match. 6,231 BoM materials never procured | **293,658 rows** from 11,609 on a raw join |
| 6 | Notif to Movement | Order | Notification to issue | **M:N, not 1:N as the diagram states.** 5,138 orders have 1 notification and 52 have exactly 2 | 1,003 of 4,884 movement orders (20.5%). 2,791 of 17,518 issue rows (15.9%). 1,003 of 5,190 notification orders (19.3%) | 2,851 rows from 2,791 (60 extra) |
| 7 | Mitem to BoM | Via Functional Location | Item to pair | M:N and indirect | 894 locations appear in BoM, Notif and Mitem together | 29,913 rows on distinct BoM pairs, 30,245 on raw. The diagram says plans do not include required parts |
| 8 | Movement and PR PO | Material, after aggregation | Material to material | 1:1 after aggregation | 1,030 both, 900 issued only, 220 procured only. 5,331 BoM materials in neither | High if joined at row level |
| 9 | PR item to PO item | Within PR PO | Line to line | 1:1 on distinct rows | 6,189 of 6,189 | Not applicable |
| 10 | Purchase Order to supplier | Within PR PO | Document to supplier | N:1 | Max 1 supplier per PO | Not applicable |
| 11 | Material to supplier | Within PR PO | Material to supplier | N:1 in this dataset | All 1,250 procured materials have one observed supplier | Not applicable. **Not proof of exclusive sourcing** |

**Keys that do not exist.** No key connects PR PO directly to Order, Notification, Functional Location or Maintenance Plan, or Movement to Maintenance Plan. Links between those tables can only go through material or location, at a declared aggregate grain.

### 5.3 Consistency that was confirmed (VERIFIED)

- Each material has one unit and one trimmed description across BoM, Movement and PR PO.
- BoM description, unit, Min.Qty, Max.Qty, Stock and MRP Type have no conflicting values within any material. They behave as material-level values repeated on each row, so summing them across BoM rows double counts.
- Mitem `ABC Indicator` and `FunctLocDescrip.` match FuncLoc in 100% of rows.
- PR-Type maps one to one to the PR number prefix, and notification prefix maps one to one to type.

### 5.4 Findings not in the existing documents (VERIFIED)

| Finding | Why it matters |
| --- | --- |
| Of the 52 shared orders, **all 52 sit on two different functional locations** and only 2 have the same notification date | Location attribution is ambiguous for every shared order. 16 of these orders reach Movement, affecting 60 issue rows |
| Order prefix 202 maps exactly to notification type N2 (135 notifications). N1 and N3 use prefix 201 only | A structural rule to test. Business meaning remains undefined |
| Movement orders with prefixes 203 to 209 have 0 rows linked to Notif History. Linked rows are 2,772 with prefix 201 and 19 with prefix 202 | Unlinked issue rows are not necessarily data gaps. They may be order types that never have notifications (HYPOTHESIS, DEF-07) |
| On the 2,851 joined rows, 234 were posted after the notification's completion date and 567 before Required Start | Timing can be profiled, but it does not establish why a part was issued |
| 22.59% of joined rows have the material in that location's BoM. 23.07% of the 2,791 issue rows have at least one match | Resolves Appendix D of the specification. The BoM link is weak evidence of where parts are used |
| 1,220 of 1,930 issued materials have issues in only one calendar month, and 985 have only one issue line. 229 are active in 9 or more months, and 47 in all 17 | Most materials cannot support meaningful CV, XYZ or forecasting results |
| 181 notifications from May 2025 are still In Progress | A long-open group that needs sensitivity analysis alongside the May 2025 volume spike |

---

## 6. Documentation compared with the data

**Reproduced.** Every expected value I could test now matched the workbooks: specification tests T01, T02, T04 to T23, and T25 to T31, plus all 28 cycle-description counts in Appendix A. T03, T24 and T32 to T34 apply to artefacts that do not exist yet. This shows the earlier counts are consistent with the data, not that any interpretation is correct.

**Conflicts to record.** Nothing below has been edited. I propose an addendum to the documents after approval.

| ID | Document | Stated | Observed | Impact and proposed action |
| --- | --- | --- | --- | --- |
| DOC-01 | Dictionary, "Current type". Spec Sections 2.9 and 3.4 | Identifiers are `int64`. Notif Order is `float64` with a risk of `201000000108.0` | All stored as inline text. No decimal points | Read identifiers as strings directly. Drop the float repair. Keep a test that no `.0` appears |
| DOC-02 | Dictionary row 17. Spec Section 2.7 | Each non-IDR currency belongs to exactly one foreign supplier | **JPY has 3 suppliers** (108763, 110155, 113914). Each supplier has one currency, which is the correct rule | Change the validation rule |
| DOC-03 | Discovery Section 2.4 | Descriptions starting with Replace: 1,009 | **882** | Do not reuse the discovery figure |
| DOC-04 | Discovery Section 3 | 20 lines posted before the notification | **10** on joined rows (13 when compared with Created On) | Do not reuse the discovery figure |
| DOC-05 | Discovery Section 2.2. Dictionary | One material sits on 308 locations | 308 raw rows, **307 distinct locations** | Report the distinct count |
| DOC-06 | Spec R11, X-03 | Plan to BoM join gives 30,245 rows | 30,245 uses raw BoM. **29,913** on `bridge_fl_material` | Correct the expected test value |
| DOC-07 | Spec Section 2.8, B-07 | 89 non-integer Installed Qty values listed as fractions on count units | **All 89 are in unit M**, a length unit. Only the 0.5 EA Stock value is on a count unit | The flag catches 1 material, not 90 rows. Correct the wording |
| DOC-08 | Spec header and Section 8 | Draft for approval, unticked checklist | Your brief refers to the "approved" specification | Needs explicit approval (Decision 3) |
| DOC-09 | Spec P-01, Section 0.4 | `PRPO_DUP_POLICY = distinct` by default | Conflicts with your instruction to present evidence first | Treat as blocked until Decision 4 |
| DOC-10 | Spec Appendix C | `caliber_supply_chain/`, `data/staged`, `data/conformed`, `data/marts`, Parquet, checksums inside `data/raw/` | Repo uses `final_caliber26/`, `data/interim`, `data/processed`. pyarrow is absent. Your brief keeps raw files immutable | Use the mapping in Section 11 |
| DOC-11 | Spec Section 0.3 | `load_ts` on every row | Makes every build differ, which breaks reproducibility testing | Move run time to metadata files. Keep row data deterministic |
| DOC-12 | Spec Section 2.4 | D4 uses DATA_CUTOFF (2026-09-30). D10 uses a fixed report date (2026-11-04) | Future cycle starts are 487 against the cutoff and 344 against the report date | Use one configured reference date, and report both counts (Decision 5) |
| DOC-13 | Discovery E04, E18, Opportunity J | "Highest criticality" and weighted exposure score | Spec S07 and Section 5.6 forbid ranking or scoring until DEF-03 | Follow the specification. Any scenario score must be labelled and tested for sensitivity |
| DOC-14 | Diagram | PR PO and BoM grains. Notif to Movement is 1:N | Grains fail on raw rows. Order is M:N for 52 orders | Record as findings. The observed data decides |

---

## 7. PR PO duplicate investigation: preliminary evidence

This investigation was read-only. **No rule has been applied.** Phase 2 will reproduce it in tested code and save the row-level evidence.

### 7.1 Results (VERIFIED)

| Question | Result |
| --- | --- |
| Exact duplicate rows | 11,609 rows form 6,189 distinct rows, leaving 5,420 extra copies (46.7%) |
| Copy distribution | 2,589 rows appear once, 2,300 twice, 780 three times, 520 four times |
| Repeated business keys | (PR, PR-Item) and (PO, PO-Item) each repeat 5,420 times on raw rows and 0 times on distinct rows |
| Same key with different values | **0**. Every repeated key is a completely identical row |
| PR item to PO item | Exactly 1:1 on distinct rows |
| Potentially valid repeat transactions (different keys, similar content) | Same date, material, quantity, amount and PO: 0 rows. Same date, material and quantity: 2 rows, which are not exact copies and stay separate |
| Position in the file | Copies are far apart. Only 1 of 5,420 successive-copy gaps is adjacent, the median gap is 2,627 rows, and the file follows no sort order on PR, PO, date or material |
| Copy count within a document | Same-copy share within multi-line documents matches random shuffling. PR: 0.255 observed, 0.265 shuffled. PO: 0.125 against 0.142. Material: 0.144 against 0.151 (200 permutations, seed 42) |
| Copy count against numeric fields | Spearman \|rho\| is at most 0.021 for lines per PR or PO, item number, quantity, amount, lead times, date, Movement rows per material and BoM locations |
| Copy count against categories | PR-Type, currency, unit, month and supplier show no significant association. Purchasing group: p = 0.026, Cramer's V = 0.064. This is weak, uncorrected for multiple tests and includes rare codes |

### 7.2 What this means

- **Compatible with row copying.** Copy count depends on nothing measured. That is compatible with either row-level replication during data generation, or an export joined to an unseen child table (such as receipt or schedule lines) whose columns were later dropped.
- **Less compatible with document-level export.** A document-level repeat would give consistent copy counts within a PR or PO. It does not.
- **Against real repeat transactions.** Identical key, identical content and the diagram's stated grain, "One PR item linked to one PO item", all argue against it.
- **Actual cause: Cannot be confirmed from the available data or documentation.** Only the case owner can answer (DEF-01).

### 7.3 Downstream impact (VERIFIED)

| Measure | Raw rows | Distinct rows | Sensitivity |
| --- | --- | --- | --- |
| IDR amount | 168,836,490,165 | 89,210,784,211 | **High, 1.89 times** |
| USD amount | 310,714.71 | 139,557.65 | **High** |
| JPY amount | 17,669,735 | 7,623,969 | **High** |
| EUR amount | 161,470.86 | 99,266.04 | **High** |
| SGD amount | 9,569.36 | 9,569.36 | None |
| Quantity, KG | 13,370,209 | 7,180,009 | **High** |
| Quantity, EA | 13,056,739 | 6,925,149 | **High** |
| Median lines per material | 4 | 2 | **High** |
| Promised interval median (mean), days | 42 (70.65) | 42 (70.51) | Low |
| Requested interval median (mean), days | 37 (71.36) | 37 (72.94) | Low |
| Top 10 IDR supplier share | 62.34% | 62.63% | Low |
| Supplier HHI, IDR | 0.0616 | 0.0601 | Low |
| Top 5 IDR suppliers | | | 4 of 5 unchanged |
| Top 50 IDR materials | | | 42 of 50 overlap (Spearman across all 1,229 materials: 0.990) |
| Materials reaching 80% of IDR amount | 200 of 1,229 | 210 of 1,229 | Moderate |
| Requested date before PR date | 630 | 324 | Scales with duplicates |
| Promised date before PR date | 6 | 2 | Scales with duplicates |

### 7.4 Recommended handling (Decision 4)

1. Keep all 11,609 rows through the raw, staged and conformed layers, with `dup_group_id`, `dup_count`, `dup_rank` and `is_dup_extra`.
2. Use a distinct-row **view** for line-level marts. Rows are filtered, never deleted, and `dup_count` stays available.
3. Publish every total under both policies wherever it is reported.
4. Label the decision as an assumption until DEF-01 is answered.

**Why distinct.** It gives the right answer whether the copies come from replication or an export join. Raw rows are right only if identical keyed lines are separate real transactions, which the evidence and the diagram argue against.

**Risk.** If the case owner confirms the copies are real, totals on the distinct policy are understated by nearly half. Keeping `dup_count` means the raw total can be restored at once.

### 7.5 Other duplicates differ (VERIFIED)

| Table | Extra copies | Pattern | Proposed handling |
| --- | --- | --- | --- |
| Movement | 863 of 17,518 | Close together: 429 of 863 gaps are adjacent, median gap 2 rows. 1,074 (date, material, order) groups have more than one row, and 297 of those have differing quantities | No document number exists to show whether identical rows are one event. Keep raw as the base, flag copies, and run a distinct-policy sensitivity check |
| BoM | 230 of 20,653 | Median gap 3 rows. Each copy pair is identical | Distinct pairs in `bridge_fl_material`. Installed Qty is unaffected per pair |

---

## 8. Known data quality concerns

| Area | Concern | Treatment |
| --- | --- | --- |
| Definitions | 15 open definitions (DEF-01 to DEF-15) | Keep codes as codes. Use declared assumptions only |
| PR PO | Requested date before PR date: 630 raw, 324 distinct. Promised date before PR date: 6 raw, 2 distinct | Flag, keep, report separately |
| PR PO | Delivery dates up to 2029. After 2026-09-30 on distinct rows: 891 requested, 766 promised | Flag. Dates are requested or promised, never actual |
| PR PO | No goods-receipt date, PO date, PO quantity or unit price | No actual lead time can be calculated. `PR-Quantity` as ordered quantity and amount as line total are assumptions |
| PR PO | Five currencies and no exchange rates | Report per currency only |
| BoM | Mixed grain | Split into `dim_material` and `bridge_fl_material`, gated on the conflict test |
| BoM | `Stock` is undated. No plant or storage location | Report as an undated snapshot, not a verified current stock position |
| BoM | 1,683 Non Stock materials hold stock. Stock of 0.5 on one EA material | Flag only |
| BoM | 133 descriptions cover 597 material numbers | Flag. Never merge |
| Movement | Only "Issue". No receipts, returns or transfers | **Stock balance and inflow analysis are not supported** |
| Movement | Issues are not proven demand | Call them observed issues. Demand is a labelled assumption |
| Notif | 1,463 notifications in May 2025 | First-month flag and sensitivity check |
| Notif | Required Start before notification date: 370 rows | Flag |
| Notif | No failure code, downtime or breakdown flag | **Notification counts are not failures or downtime** |
| Notif | 1,305 open records | Treat as censored. Do not impute |
| Mitem | 28 cycle spellings, and Start of cycle undefined | Approved mapping needed. Due-date projection stays blocked (DEF-11) |
| FuncLoc | 33 SITE rows have no criticality. A, B, C and S have no documented order | Keep nulls. Unordered category |
| FuncLoc | No parent column | Prefixes are labels only. Parent links are not inferred |
| Naming | `ABC Indicator` is an existing criticality code and differs from value-based ABC analysis | Use distinct names such as `abc_value_class` to avoid confusion |

---

## 9. Unresolved analytical questions

### 9.1 Scope questions for you or the organisers

| ID | Question | Status |
| --- | --- | --- |
| Q1 | Is this dataset the final-round data for Case 2, or does it belong to Case 3? | UNCONFIRMED |
| Q2 | Is the Case 3 casebook available? It appears to define the business questions | Not in repository |
| Q3 | Can the organisers confirm the "synthetic" statement and that it covers all fields? | One document only |

### 9.2 Business definitions

Dictionary Section 8 lists DEF-01 to DEF-15. These most affect results:

| ID | Question | Blocks |
| --- | --- | --- |
| DEF-01 | Meaning of PR PO exact duplicates | Final PR PO totals |
| DEF-02 | Meaning of Min.Qty and Max.Qty | Stock status labels |
| DEF-03 | Meaning and rank of criticality A, B, C, S | Criticality weighting and scoring |
| DEF-05 | Meaning of PO-Item Amount | Unit amount and value-based ABC |
| DEF-06 | Meaning of PO-Delivery Date, and receipt date availability | Any lead-time interpretation |
| DEF-07 | Meaning of order prefixes 201 to 209 | Interpreting unlinked issue rows |
| DEF-09 | Meaning of notification types | Any failure-related analysis |
| DEF-11 | Meaning of Start of cycle | Planned-work projection |
| DEF-12 | Date of the Stock snapshot | Stock against consumption |

New questions from this audit: the meaning of shared orders across two locations, and whether the Movement file is the complete issue log for the window. The monthly zero-filling in the demand mart depends on that second point.

---

## 10. Transportation optimisation readiness (no model proposed)

| Required element | Available? | Evidence |
| --- | --- | --- |
| Supply nodes | **Partial, identity only** | 124 supplier codes and names. No address or site. Each material has one observed supplier |
| Demand nodes | **No** | `PR-Plant` is 1000 on every row, so there is one destination |
| Supply quantities | **No** | No supplier capacity or availability |
| Demand quantities | **Partial** | Issues per material for one site. Issues are not confirmed demand |
| Transportation costs | **No** | No freight, mode or route cost. No field defines whether `PO-Item Amount` includes freight |
| Route or network | **No** | None. No text in Notif descriptions refers to transport, freight or shipping |
| Capacity constraints | **No** | Min.Qty and Max.Qty are undefined planning parameters, not capacity |

`SITE_PY_2200 WAREHOUSE` is one functional location, with 6 notifications, no BoM rows and no plan items. It does not establish a storage network. Prefixes PX, PY, UT and SITE cannot be read as physical sites.

**Conclusion.** A transportation model is not supported by the available data. Required additions would be supplier sites, at least two validated destinations, per-route unit freight costs, supplier capacity, confirmed demand per destination, and rules on which materials are interchangeable. Warehouse allocation has a similar gap, with no storage location or capacity data. The Phase 6 report will document this and will not build a model.

---

## 11. Proposed directory structure

Only additions and one file move. Existing folders are reused.

```text
final_caliber26/
├── README.md                     NEW, after implementation
├── requirements.txt              NEW
├── pytest.ini                    NEW
├── data/
│   ├── raw/                      L0, immutable. BoM.xlsx moves here (Decision 2)
│   ├── reference/                NEW: source_manifest.json, map_cycle.csv, map_item_text.csv, expected_values.json
│   ├── interim/
│   │   ├── staged/               L1: one table per workbook, with lineage
│   │   └── conformed/            L2: flags, dimensions, bridges, facts
│   └── processed/                L3: analytical marts, plus one metadata JSON each
├── docs/analysis/                Plan and reports, plus ASSUMPTIONS_REGISTER.md
├── notebooks/                    01 to 05, one per EDA area
├── outputs/{reports,tables,figures}/
├── src/
│   ├── config.py                 Relative paths, file registry, parameters
│   ├── pipeline.py               Command-line stage runner
│   ├── reporting.py              Writes tables, Markdown and metadata
│   ├── data/
│   │   ├── schemas.py            Expected columns, types, standard names
│   │   ├── ingest.py             Read, checksum, lineage
│   │   └── profiling.py          Phase 1 profiles
│   ├── validation/
│   │   ├── checks.py             Specification Section 7 tests
│   │   └── relationships.py      Join audit: cardinality, coverage, multiplication
│   ├── preprocessing/
│   │   ├── common.py             Duplicate grouping, date and outlier flags, transformation log
│   │   ├── prpo.py, bom.py, movement.py, notifications.py, maintenance_plan.py, funcloc.py
│   └── analysis/
│       ├── marts.py              Mart construction
│       ├── metrics.py            Pareto, ABC, XYZ, ADI and CV², HHI, outliers
│       └── plots.py              Shared figure helpers
└── tests/
    ├── conftest.py               Fixtures
    ├── unit/                     Small hand-checkable fixtures
    └── data_contract/            Real-workbook checks
```

**Specification layers mapped to repository folders**

| Specification | Repository |
| --- | --- |
| `caliber_supply_chain/` | `final_caliber26/` |
| `data/staged` | `data/interim/staged` |
| `data/conformed` | `data/interim/conformed` |
| `data/marts` | `data/processed` |
| `data/raw/checksums.json` | `data/reference/source_manifest.json` |
| `docs/validation_report.md` | `outputs/reports/validation_report.md` |

Mapping tables go in `data/reference/` because they are hand-reviewed inputs. They must not sit in a folder that gets regenerated or ignored by Git.

---

## 12. Proposed Python architecture

**Style:** plain functions with one job each, and no classes unless one is clearly needed. Notebooks load marts and call `src/` functions, and contain no hidden cleaning.

**Data flow**

```text
Workbooks → ingest → staged tables (types, names, lineage)
                       ↓
                  profiling → outputs/reports, outputs/tables
                       ↓
              preprocessing → conformed tables + transformation_log.csv + exception lists
                       ↓
              relationships → join audit tables (must pass before marts are built)
                       ↓
                      marts → data/processed + metadata JSON
                       ↓
             notebooks and reports
```

**Key rules**

| Concern | Rule |
| --- | --- |
| Paths | All derive from `Path(__file__).resolve().parents[1]`. No absolute paths |
| Read types | Identifiers read as strings by name. Types are asserted after reading, not inferred |
| Lineage | `source_file`, `source_sheet`, `source_row`, `row_hash` and `spec_version` on every staged row |
| Determinism | No timestamps in data files. Run time goes only in metadata. Stable sorts, fixed seeds |
| Joins | One `audited_merge` helper records rows before and after, and match rates. It fails on unexpected row growth |
| Row preservation | L1 and L2 row counts must equal raw counts. Filtering happens only in marts and is named in metadata |
| Transformation log | Dataset, field, record reference, transformation, reason, validation method, affected count |
| Failures | Checks are marked `fail` (stops the build) or `warn` (reported). Results are written even when a check fails |
| Logging | Standard `logging`, to console and `outputs/reports/pipeline.log` |
| Storage format | Recommended: CSV, read back only through one schema-aware function (Decision 6). Data files of this size are manageable and reviewable. Opening them in Excel may corrupt long identifiers |

**Commands**

```bash
python -m src.pipeline --stage ingest
python -m src.pipeline --stage all
pytest
```

---

## 13. Implementation sequence

| Step | Work | Output | Gate before continuing |
| --- | --- | --- | --- |
| 0 | Apply approved decisions, create the environment, confirm `read_excel` matches this audit | `requirements.txt`, manifest | Hashes and values match |
| 1 | Ingestion and profiling | Staged tables, workbook and column profiles, key assessment | Tests pass. You review results |
| 2 | Data quality and PR PO duplicate evidence | `DATA_QUALITY_REPORT.md`, exception lists | **Duplicate decision confirmed** |
| 3 | Cleaning and conformed tables | Conformed tables, transformation log | No rows lost, all flags tested |
| 4 | Relationship validation | `DATA_INTEGRATION_REPORT.md` | All joins audited |
| 5 | Marts M1 to M3, then M4 to M6 | `data/processed/`, metadata | Row-count and aggregation tests pass |
| 6 | EDA notebooks A to E | `notebooks/`, figures, `EXPLORATORY_DATA_ANALYSIS_REPORT.md` | Notebooks re-run clean from a fresh kernel |
| 7 | Business opportunities | `BUSINESS_OPPORTUNITY_REPORT.md` | Every claim is traceable to an output |
| 8 | README and full rebuild | README, validation report | Two clean rebuilds match |

After each major step I will run the code and tests, inspect outputs, document findings and report unresolved issues, including failed checks.

**Timing.** The Case 2 document states the Final Stage is on 4 to 5 November 2026, and the audit date is 2026-11-04. If the deadline is that close, the priority order is Steps 0 to 5 (through M3), Notebooks B and D, and then the rest. Please confirm your actual deadline (Decision 8).

### 13.1 Method feasibility, based on this audit

| Method | Feasibility | Limitation |
| --- | --- | --- |
| Descriptive, temporal analysis | Supported | 17 months, no seasonality test |
| Pareto by issue lines or orders | Supported | Never sum quantities across materials |
| Value-based ABC | Partial | 1,015 of 1,930 issued materials have an IDR amount. Requires DEF-05 and duplicate decision |
| XYZ, CV | Partial | 1,220 materials are active in a single month. Report only for materials above a declared activity threshold |
| Intermittency (ADI, CV²) | Partial | Needs repeated issues. Describes issue patterns, not confirmed demand |
| Supplier concentration (HHI, top N) | Supported per currency | Observed single-supplier materials do not prove exclusive contracts |
| Outlier investigation | Supported | Flag only. Robust z within material, with a fallback for sparse materials |
| Survival analysis of notification closure | Supported with scipy | Measures closure of records, not repair duration or downtime |
| Correlation | Limited | Used only at a compatible grain. Association, not cause |
| Machine learning, forecasting models | **Not proposed now** | No justified need given short, sparse history. scikit-learn stays out of requirements |
| Stock balance, stockout analysis | **Not supported** | No receipts, no dated stock, no stockout rule |
| Downtime or failure rate | **Not supported** | No such fields |
| Savings estimates | **Not supported at this stage** | Synthetic data, no cost rates. Only stated if inputs and assumptions are documented |

Each method used will be documented with its business question, required fields, grain, formula, assumptions, limitations, validation and interpretation.

---

## 14. Dependencies and testing strategy

### 14.1 Dependencies

Proposed `requirements.txt`, with pinned versions: pandas, numpy, openpyxl, matplotlib, seaborn, scipy, notebook, nbconvert, pytest.

- **scipy** is an addition to your listed stack. It is needed for chi-square, Kruskal-Wallis, Spearman and censored survival estimates.
- **scikit-learn** and **pyarrow** are excluded unless a need emerges.
- The virtual environment should sit outside iCloud, for example `~/.venvs/caliber26`.

### 14.2 Testing

| Layer | Purpose | Examples |
| --- | --- | --- |
| Data contract | Confirm the source files match expectations, using values kept in `expected_values.json` | Accessibility, checksums, sheets, columns, row counts, specification T01 to T31 |
| Unit | Confirm logic on small hand-checkable data | Duplicate grouping, flags, `audited_merge`, Pareto, ADI, HHI, robust z, cycle mapping |
| Identifier preservation | Prevent silent type damage | Leading zeros survive a round trip, no `.0`, no scientific notation |
| Pipeline integrity | Confirm rows and grains survive | L1 and L2 row counts match raw, mart keys are unique, fact tables unchanged after lookups |
| Relationships | Confirm cardinality and integrity | Foreign key misses, shared order count of 52, 2,851 joined rows from 2,791 |
| Aggregation safety | Prevent invalid totals | No cross-currency amount, no cross-material quantity, no BoM stock sum |
| Reproducibility | Confirm rebuild stability | Two builds give identical hashes for all data files |

**Limit of these tests.** A data-contract test passing means the data has not drifted from an earlier count. It does not show the count's interpretation is correct. The validation report will separate "matches expected value" from "logic verified on hand-calculated fixture". A phase is complete only when results have been inspected and failed checks are reported.

### 14.3 Deliverable check

| Deliverable | Plan |
| --- | --- |
| `DATA_ENGINEERING_IMPLEMENTATION_PLAN.md` | This document |
| `DATA_QUALITY_REPORT.md`, `DATA_INTEGRATION_REPORT.md` | Steps 2 and 4 |
| `EXPLORATORY_DATA_ANALYSIS_REPORT.md`, `BUSINESS_OPPORTUNITY_REPORT.md` | Steps 6 and 7 |
| Source modules, notebooks, tests | Sections 11 and 12 |
| Interim and processed datasets, outputs | Rebuilt by the pipeline |
| README | Step 8 |

---

## 15. Decisions requiring approval

| # | Decision | Recommendation | If there is no answer |
| --- | --- | --- | --- |
| 1 | **Case scope.** Are the six workbooks the correct final-round data for Case 2? | Build the foundation now, since it is valid either way. Please check with the organisers, and share the Case 3 casebook if available | Opportunities are framed as spare-part analytics, with the case-number discrepancy stated openly |
| 2 | **Move `BoM.xlsx` to `data/raw/`.** | Move it, confirming the SHA-256 is unchanged | Register its root path in config |
| 3 | **Approve the specification** with corrections DOC-01 to DOC-14, Class A now and Class B and C as declared assumptions. | Approve. Add corrections as an addendum rather than rewriting your documents | Implementation cannot start |
| 4 | **PR PO duplicates:** see Section 7.4. Options: A, keep all rows and use a distinct view with both totals published; B, raw; C, report no totals until the case owner answers. | **Option A** | Rows are flagged only, and no totals are finalised |
| 5 | **Reference dates:** `DATA_CUTOFF = 2026-09-30`, used for all "future" flags. | Approve, labelled as an assumption | Same as recommendation, labelled unconfirmed |
| 6 | **Storage format:** CSV with a schema-aware reader, or Parquet with pyarrow added. | CSV | CSV |
| 7 | **Environment and version control:** create a virtual environment outside iCloud and install `requirements.txt`. Should I also run `git init`? If so, should `outputs/` and processed data stay ignored as `.gitignore` currently specifies? | Create the environment. Initialise Git, keeping generated data ignored and committing code, documents and mapping tables | Environment is required. Git is skipped |
| 8 | **Deadline and depth:** the actual deadline, and whether the priority order in Section 13 should apply. | Confirm the deadline | Full sequence, in order |
| 9 | **Case-owner definitions:** can DEF-01 to DEF-15 be sent to the organisers? Unanswered ones proceed as labelled assumptions in `ASSUMPTIONS_REGISTER.md`. Rankings for criticality and priority stay unapplied until defined. | Send the 9 definitions in Section 9.2 first | Proceed on labelled assumptions |

**Implementation has not started. The next step is your approval or changes to the decisions above.**
