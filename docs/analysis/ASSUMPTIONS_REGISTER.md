# CALIBER 2026 Assumptions Register

**Date:** 2026-11-04. **Status:** all items below are open unless marked otherwise.

This register records definitions and assumptions the supplied data and documents cannot settle. Nothing here is a business definition. An item closes only when the case owner, or a named document, answers it.

"Current treatment" describes what the pipeline does today. Through marts M1 to M3, no item changes a source value or removes a row.

**Impact scale**

| Level | Meaning |
| --- | --- |
| High | The answer could materially change analytical results or their interpretation. |
| Medium | Affects a specific analysis or label. |
| Low | Affects wording or minor grouping. |

---

## 1. Project and data assumptions

| ID | Item | Evidence | Impact | Current treatment | Needed to resolve |
| --- | --- | --- | --- | --- | --- |
| A-01 | `DATA_CUTOFF = 2026-09-30` | Latest Posting Date and Notification Date in the files. No extraction date is documented | Medium. Decides "future date" flags (1,467 promised and 1,682 requested on original rows; 766 and 891 on distinct rows) and later censoring of open notifications | Single configured value in `src/config.py`. Used for counts only | Extraction date from the case owner |
| A-02 | The data is synthetic | The diagram states "All data is synthetic (dummy)". All six files were written by openpyxl within 19 seconds. Only one document says so | High. Findings describe this dataset, not plant performance. Patterns may reflect data generation | Every report carries the data label. No operational or savings claims | Organiser confirmation, including which fields keep realistic patterns |
| A-03 | Case 3 business questions | The project is confirmed as Case 3. The diagram cites a casebook whose sections are not in the repository. `docs/case/CALIBER_2026_Case_3_Complete_Final_Case.md` is misnamed: its content is the Case 2 dashboard case | High for simulation and all later framing. The complete Case 3 problem statement is not confirmed, and no competition requirement is assumed | Foundation built from the diagram and workbooks. Simulation design must be reviewed against the official brief before implementation | The official Case 3 brief |
| A-04 | File authenticity | Checksums match the audit baseline of 2026-11-04. No organiser checksums were supplied | Low | Manifest states the limit | Organiser checksums, if available |
| A-05 | Movement exact duplicates (863 extra rows) | No document number exists. Copies sit close together (429 of 863 gaps are adjacent, median gap 2 rows). 297 same-key groups have differing quantities | Medium. Totals move little (lines 4.93%, quantity within a unit 1.28% to 21.05%), but 220 materials change by over 10% in quantity, up to 80% | Two parallel demand scenarios (project owner's decision): A includes all eligible records, B excludes rule C1 copies. Neither is treated as true. 222 materials change by 10% or more | Case owner confirmation, or a document number |
| A-06 | Movement is a complete issue log, and issues represent demand | Movement Type is only "Issue". Completeness is not documented. Issues are observed movements, not proven demand | High for demand and simulation. Monthly zero-filling depends on completeness | Zero-filled only inside 2025-05 to 2026-09, only for issued materials, with `is_zero_filled` on every row. Described as observed issues | Case owner confirmation |
| A-07 | Orders on two notifications | 52 orders each sit on 2 notifications. All 52 pair different functional locations, and only 2 share a date. 16 reach Movement, covering 60 issue rows | Medium. Location attribution is ambiguous for those rows | `fl_attribution = ambiguous`, never allocated. On 19 of the 60 rows the material is on the BoM of exactly one of the two locations, and on 41 it is on neither. See `outputs/exceptions/shared_orders.csv` | Whether one order may legitimately cover several locations |
| A-08 | Cause of volume patterns | Notif History has 1,463 rows in May 2025, then 132 to 388 a month. Movement peaks at 2,580 in December 2025. PR-Date ends 2026-09-22 with 493 rows that month | Medium. May be a backlog load, a major maintenance event or data generation | Reported only. No cause is claimed | Case owner explanation |
| A-09 | BoM attributes are material-level | Description, unit, Min.Qty, Max.Qty, Stock and MRP Type show no conflict within any material. This is observed behaviour, not a documented rule | Medium. Basis for `dim_material` | The build stops if any attribute differs within a material. 0 conflicts found (`CONF-06.conflicts`) | Case owner confirmation |
| A-10 | Outlier method and thresholds | Spec Section 2.8, marked as needing approval. Flag rates reach 13% on some intervals, and 10% on Stock | Low for results, because flags remove nothing. Medium for interpretation: a flag means review, not error | Robust z 3.5 within material, IQR fence 3.0 within the wider group, and `not_assessed` where neither applies (COR-20) | Approval of the method, or a preferred alternative |
| A-11 | Repeated maximum values | Exact copies set aside. Movement KG peaks at 23,135 on 7 materials, including both grease and castable, next value 5,000. Movement EA peaks at 5,700 on 9 materials, next 5,000. Installed Qty EA peaks at 5,037 on 55 materials, next 1,500. Max.Qty peaks at 3,344 in three different units. Stock and PR-Quantity show no such pattern | Medium. May be a cap in a system or in data generation. Maximums, totals and tails on these measures may not reflect real extremes | Reported in `repeated_maximum_values.csv`. Values unchanged. No cause claimed | Case owner explanation |
| A-13 | Unit amount is amount divided by PR quantity | The Specification's proposal. Assumes the amount is the line total for that quantity. Within a material the highest value is typically 2.04 times the lowest | High for any cost-based simulation | `implied_unit_amount_scenario`, in M1 and M2 only | DEF-05 |
| A-14 | Demand impact thresholds of 10% and 25% | Analyst choice, not a business rule. Sensitivity is shown from 1% to 50% | Medium. Decides which materials are called materially affected | `DEMAND_IMPACT_MATERIAL_PCT`, `DEMAND_IMPACT_HIGH_PCT` in `src/config.py` | Project owner's preferred thresholds |
| A-15 | Requested quantity far exceeds issued quantity | On materials in both datasets, `exact_distinct_rows` against Scenario A: 7.55 times in EA, 9.06 in KG. Median material ratio 1.67 in EA | High for replenishment simulation. The flows don't balance | Reported in `procurement_issue_reconciliation.csv`. No adjustment | Definition of PR quantity, and receipts |
| A-12 | `DEF-` items proceeding as labelled assumptions | The project owner approved continuing, and the plan's recommendation was to proceed with labels | Medium | Only Class B items that are labelled in their column names or metadata were applied: cycle mapping, censoring at the cutoff, and the unit amount scenario | Project owner may overrule |

---

## 2. Business definitions

IDs follow `CALIBER_DATA_DICTIONARY.md` Section 8. "Blocks" lists work that cannot be finalised without an answer or a labelled assumption.

| ID | Question | Evidence | Impact | Current treatment | Blocks | Information needed |
| --- | --- | --- | --- | --- | --- | --- |
| DEF-01 | What do PR PO exact duplicates mean? | 5,420 extra rows. Keys are unique on distinct rows. Copies sit far apart (median gap 2,627 rows). The cause cannot be confirmed | High. IDR amount is 168.84 billion on original rows and 89.21 billion on distinct rows. Copy counts show no association with any tested field after correction for multiple tests (`duplicate_evidence.md`), which still does not establish the cause | Dual views. Neither is definitive | Any single headline total | Whether repeats are real lines, export artefacts or generated copies |
| DEF-02 | What are Min.Qty and Max.Qty? | Planning-style values. Min never exceeds Max. Both are 0 on every Non Stock material | High | Compared with Stock only, as raw counts | Stock status labels and policy analysis | Reorder point, maximum level, or other? Per plant or per location? |
| DEF-03 | What do criticality A, B, C and S mean, and how do they rank? | 33 SITE rows are blank. S does not fit an A to C order | High | Unordered category. No ranking | Any weighting or score | Definition and rank of each code |
| DEF-04 | Why do Non Stock materials hold stock? | 1,683 materials | Medium | Counted only | Interpreting them as excess | Meaning of Non Stock |
| DEF-05 | What is PO-Item Amount? Does PR-Quantity equal the ordered quantity? | No PO quantity or unit price exists. Implied unit amount varies within materials | High | Amounts kept in original currency. Unit amount exists only as `implied_unit_amount_scenario` (A-13) | Confirmed unit amount, value-based ABC | Line total or unit price, net or gross, tax treatment |
| DEF-06 | What is PO-Delivery Date? Is a receipt date available? | Earlier than PR date on 6 original rows and 2 distinct rows. No receipt date exists | High | Called "promised". Never "actual" | Actual lead time or delivery reliability | Definition, plus goods-receipt dates |
| DEF-07 | What do order prefixes 201 to 209 mean? | Only 201 and 202 appear in Notif History. 202 maps exactly to N2. Movement rows with prefixes 203 to 209 never link | High for attribution | Counted only | Interpreting unlinked issues | Order type per prefix |
| DEF-08 | What do PR-Type, PO prefix and Purchasing Group mean? | 7 types, 4 PO prefixes, 19 groups | Medium | Kept as codes | Routine versus emergency analysis | Code meanings |
| DEF-09 | What do notification types N1, N2, N3 and N6 mean? | N2 is always Emergency. N6 has one row | High | Kept as codes. **Notifications are not treated as failures** | Failure analysis | Type meanings, failure codes, downtime |
| DEF-10 | Is the cycle mapping in Spec Appendix A correct? | 28 spellings. "2 WEEKLY" could be read two ways | Medium | Originals kept. `map_cycle` holds the Spec's reading, in `*_proposed` columns only | Final interval analysis | Confirmation of the mapping |
| DEF-11 | What is Start of cycle? | 2015 to 2029. 7,718 fall on the first of a month | High for planning | Kept as supplied | Due-date projection | Anchor, first due date or last completion |
| DEF-12 | When was Stock measured? | No date, plant or storage location | High | Treated as an undated snapshot, not current stock | Stock against consumption | Snapshot date, and receipts if available |
| DEF-13 | What do plant 1000, material prefixes and location prefixes mean? | One plant. Prefixes 4100, 4200, 4300. PX, PY, UT, SITE | Medium | Labels only. Not treated as physical sites | Site-level grouping and any network analysis | Meaning of each |
| DEF-14 | Which notification date is authoritative? | Created On differs on 61 rows. Required Start is before notification on 370 rows | Low to medium | Both kept | Interval analysis choice | Definition |
| DEF-15 | What do units LG, RL, ASS, SHT and M mean? | 10 codes. No unit conversions supplied | Low | Kept as codes. Never converted or added across units | None if kept within a unit | Definitions |
| DEF-16 | How do notification priorities rank? (Added from Spec N-06) | Low, Medium, High, Emergency look ordered, but this is not documented | Medium | Unordered category | Any severity weighting | Confirmation of the order |

---

## 3. Closed items

| Item | Resolution | Source |
| --- | --- | --- |
| Which case this data belongs to | Case 3, Spare Part Intelligence | Project owner, Phase 0 and Phase 1 authorisation |
| PR PO working policy | Dual views. The cause of the duplicates remains open as DEF-01 | Project owner, Decision 4 |
| BoM.xlsx location | Moved to `data/raw/` with matching checksums | Project owner, Decision 2. See `data/reference/bom_relocation_record.json` |

---

## 4. Priority questions for the case owner

Asking these first would resolve the most analytical risk: **DEF-01, DEF-02, DEF-03, DEF-05, DEF-06, DEF-07, DEF-09, DEF-11, DEF-12**, plus A-03 (the Case 3 casebook), A-05 (Movement copies), A-06 (issue log completeness), A-11 (repeated maximum values) and A-15 (requests above issues).
