# CALIBER 2026 Data Dictionary

**Version:** 0.1 (draft for approval)
**Date:** 2026-11-04
**Scope:** The six supplied workbooks: PR PO.xlsx, Movement Material.xlsx, Notif History.xlsx, Mitem & Mplan.xlsx, BoM.xlsx, FuncLoc list.xlsx.
**Companion document:** CALIBER_DATA_PREPARATION_SPECIFICATION.md
**Status of the data:** The case document "Data Context & Relationship Diagram.pdf" states that all six files are synthetic (dummy) data built for the Caliber 2026 Hackathon. They mirror the structure of the original system, not its values. Nothing in this dictionary describes verified operational performance.

---

## 0. How to read this dictionary

### 0.1 Evidence labels for business meaning

| Label | Meaning |
| --- | --- |
| DIAGRAM | Meaning stated or implied by the supplied Data Context & Relationship Diagram. |
| OBSERVED | Behaviour counted in the raw workbook (read-only inspection, 4 November 2026). It describes the data, not the business rule. |
| UNDEFINED | No supplied document defines this field or its codes. A business definition from the case owner is required. Analysis may proceed only with a declared assumption. |

Common SAP meanings are deliberately **not** used as definitions. Where a field name resembles an SAP field, the dictionary says so only as a question for the case owner.

### 0.2 Variable classes

| Class | Meaning |
| --- | --- |
| Identifier | A code that identifies a record or links tables. Never used in arithmetic. |
| Categorical | A closed set of codes or labels. |
| Numerical | A measured quantity or amount. |
| Temporal | A date. |
| Descriptive | Free or semi-structured text. |

### 0.3 Analytical roles

| Role | Meaning |
| --- | --- |
| Primary key (PK) | Uniquely identifies a row (after the documented duplicate rule, where stated). |
| Foreign key (FK) | Links to another table. |
| Dimension | Used to group, filter or segment. |
| Measure | Aggregated or compared numerically. |
| Event date | Places a record in time. |
| Label | Read by people; not used for joins. |

### 0.4 Recommended data types (pandas)

| Notation | Meaning |
| --- | --- |
| `string` | pandas `StringDtype`. All identifiers are stored as strings so they are never summed, averaged or rounded. |
| `category` | pandas categorical, unordered unless an order is approved. |
| `Int64` | Nullable integer. |
| `Float64` | Nullable float. |
| `datetime64[ns]` | Date (all source dates have no time component, OBSERVED). |

### 0.5 Profile conventions

"Rows" counts are raw rows, including exact duplicates. "Distinct" counts are distinct values in the raw column. Ranges are raw minimum and maximum.

---

## 1. PR PO.xlsx

**Diagram purpose:** Purchase requisition and order; "Procurement & Lead-Time Data".
**Diagram grain:** One PR item linked to one PO item.
**Raw shape:** 11,609 rows x 18 columns, sheet "Data".
**Exact duplicate rows:** 5,420 (46.7%). 6,189 distinct rows.
**Key status:** (Purchase Requisition, PR-Item) and (Purchase Order, PO-Item) are each unique only after exact duplicates are set aside (OBSERVED).

| # | Column | Business meaning | Current type | Recommended type | Class | Role | Observed profile | Potential issues | Recommended treatment |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | PR-Type | Purchase requisition type. Code meanings UNDEFINED. | str | `category` | Categorical | Dimension | 7 codes: PR01 392, PR03 5,776, PR04 494, PR05 779, PR06 4,080, PR09 1, PR10 87 rows. Maps one to one to the first 2 digits of Purchase Requisition (PR01=10, PR03=12, PR04=13, PR05=14, PR06=15, PR09=18, PR10=19). | Meaning unknown (routine, project, emergency?). PR09 has a single row. | Keep codes as is. Validate the one-to-one prefix rule. Do not label codes until defined. Flag PR09 as a singleton category for any statistics. |
| 2 | Purchase Requisition | PR document number. DIAGRAM: part of the PR item key. | int64 | `string` | Identifier | PK part, FK candidate | 4,805 distinct; all 10 digits. | Stored as a number. | Cast to string. Validate 10-digit pattern. |
| 3 | PR-Item | Line number within the PR. DIAGRAM: part of the PR item key. | int64 | `string` | Identifier | PK part | Values 10 to 70 in steps of 10. | None found. | Cast to string. Validate values are multiples of 10. |
| 4 | PR-Date | Date the PR was created. Meaning inferred from the name only; confirm. | datetime | `datetime64[ns]` | Temporal | Event date | 2025-05-04 to 2026-09-22; 507 distinct; no time component. | Whether it is creation or approval date is UNDEFINED. | Keep. Use as the start of all procurement intervals. |
| 5 | PR-Material | Material number requested. DIAGRAM: FK to BoM Material No. | int64 | `string` | Identifier | FK | 1,250 distinct; all 10 digits; 100% found in BoM. Each material has exactly one supplier, one UoM and one description. | None found. | Cast to string. Validate 10-digit pattern and FK to BoM. |
| 6 | PR-Material Desc | Material description. | str | `string` | Descriptive | Label | 1,182 distinct; 191 rows with leading or trailing spaces; all upper case; 39 descriptions map to more than one material number. | Whitespace; same text on different material numbers. | Keep original. Add trimmed copy `material_desc_clean`. Flag same-description-different-material groups. Do not merge material numbers. |
| 7 | PR-Quantity | Quantity requested on the PR item, in PR-UoM. | int64 | `Int64` | Numerical | Measure | 1 to 77,913; median 26 (raw). By unit (distinct rows): KG median 15,670, max 77,913; EA median 20, max 61,128; SET max 31. | Whether PR quantity equals PO quantity is UNDEFINED (no PO quantity column). Heavy right tail. | Keep. Never sum across units. Flag outliers within material or unit (see specification). |
| 8 | PR-UoM | Unit of measure of PR-Quantity. | str | `category` | Categorical | Dimension | 10 units: EA, SET, KG, RL, LG, L, CAN, M, ASS, SHT. Matches BoM Unit for every material. | Unit code meanings (LG, RL, ASS, SHT) UNDEFINED. | Keep. Use only to group or validate. No unit conversion. |
| 9 | PR-Delivery Date | Delivery date requested on the PR. Meaning inferred from the name; confirm. | datetime | `datetime64[ns]` | Temporal | Requested date | 2023-12-21 to 2029-03-09; 630 raw rows are before PR-Date (as low as -500 days). | Requested date before PR creation is illogical; far-future dates. | Keep. Flag negative and extreme intervals. Never treat as an actual date. |
| 10 | PR-Plant | Plant code. Site identity UNDEFINED. | int64 | `string` | Identifier | Dimension | Single value 1000 on every row. | No variation; plant identity not documented. | Cast to string. Keep as constant. Exclude from grouping (no information). |
| 11 | PR-Purchasing Group | Purchasing group code. Meanings UNDEFINED. | str | `category` | Categorical | Dimension | 19 codes; MR1 4,980 rows; PMP 1 row. | Rare codes. | Keep. Flag groups with fewer than 30 distinct rows for statistics. |
| 12 | Purchase Order | PO document number. | int64 | `string` | Identifier | PK part | 1,792 distinct; 10 digits; prefixes 43, 45, 80, 86 (meaning UNDEFINED). One supplier per PO. A PO groups 1 to 27 PRs. | Prefix meaning unknown. | Cast to string. Derive `po_prefix` (2 digits) as a label only. |
| 13 | PO-Item | Line number within the PO. | int64 | `string` | Identifier | PK part | Values 10 to 270 in steps of 10. | None found. | Cast to string. |
| 14 | PO-Supplier Code | Supplier identifier. | int64 | `string` | Identifier | FK to supplier dimension | 124 distinct; 6 digits; one name per code. | Synthetic; not a verified entity. | Cast to string. Build supplier dimension from this table only. |
| 15 | PO-Supplier Name | Supplier name. | str | `string` | Descriptive | Label | 124 distinct; 118 follow a four-word Indonesian template ending "PT"; 6 foreign names. | Names are likely generated (synthetic data). No location information. | Keep as label. Do not geocode or match to real companies in preparation. |
| 16 | PO-Item Amount | Amount on the PO item, in PO-Currency. Whether it is a line total, net or gross, with or without tax is UNDEFINED. | float64 | `Float64` | Numerical | Measure | All positive; no zeros. | Meaning of amount; implied unit amount varies up to 5.28 times within a material. | Keep in original currency. Derive `implied_unit_amount` = amount / PR-Quantity only with the label "implied, assumes line total". |
| 17 | PO-Currency | Currency of the amount. | str | `category` | Categorical | Dimension | IDR 11,511, JPY 41, USD 35, EUR 20, SGD 2 rows. Each foreign currency belongs to exactly one foreign supplier. | No exchange rates supplied. | Keep. Never add amounts across currencies without a sourced rate table. |
| 18 | PO-Delivery Date | Delivery date on the PO. Promised or planned; not a goods receipt. | datetime | `datetime64[ns]` | Temporal | Promised date | 2025-04-20 to 2028-10-09; 6 raw rows before PR-Date; 4,232 raw rows earlier than PR-Delivery Date. | Not an actual receipt date. Future dates beyond the data window. | Keep. Name derived intervals "promised". Flag negatives and dates after the data cutoff. |

**Columns absent from PR PO that analyses might wrongly assume exist:** PO creation date, goods-receipt date, PO quantity, net unit price, price unit, incoterms, storage location, supplier address.

---

## 2. Movement Material.xlsx

**Diagram purpose:** Spare part issue (consumption); "Spare Part Consumption History".
**Diagram grain:** One material issue transaction.
**Raw shape:** 17,518 rows x 7 columns.
**Exact duplicate rows:** 863 (rows that repeat an earlier row in all 7 columns). 1,074 (Posting Date, Material, Order) groups have more than one row; 297 of those groups contain different quantities.
**Key status:** No natural key. No material document number is supplied.

| # | Column | Business meaning | Current type | Recommended type | Class | Role | Observed profile | Potential issues | Recommended treatment |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Posting Date | Date the issue was posted. | datetime | `datetime64[ns]` | Temporal | Event date | 2025-05-06 to 2026-09-30; 513 distinct; no time component. | Monthly volume uneven (peak 2,580 rows in Dec 2025). | Keep. Derive month and ISO week. |
| 2 | Movement Type | Type of goods movement. | str | `category` | Categorical | Dimension | Single value "Issue". | No receipts, returns or transfers; the label is text, not an SAP movement code. | Keep. Validate it stays constant. Note: stock cannot be rebuilt from this table. |
| 3 | Material Number | Material issued. DIAGRAM: FK to BoM Material No. | int64 | `string` | Identifier | FK | 1,930 distinct; 10 digits; 100% found in BoM; one unit and one description per material. | None found. | Cast to string. Validate FK. |
| 4 | Material Descriptions | Material description. | str | `string` | Descriptive | Label | 1,795 distinct; 128 rows with leading or trailing spaces. | Whitespace. | Keep original. Add trimmed copy. |
| 5 | Quantity | Quantity issued, in Base Unit. Sign convention: all values positive. | int64 | `Int64` | Numerical | Measure | 1 to 23,135; median 2. By unit: KG max 23,135; EA max 5,700. | Heavy tail; mixed units. | Keep. Aggregate only within one material (single unit per material verified). Flag outliers within material. |
| 6 | Base Unit | Unit of Quantity. | str | `category` | Categorical | Dimension | Same 10 units as PR PO. Matches BoM Unit for every material. | Unit code meanings UNDEFINED. | Keep. No conversion. |
| 7 | Order | Maintenance order receiving the issue. DIAGRAM: FK to Notif History Order. | int64 | `string` | Identifier | FK | 4,884 distinct; 12 digits; prefixes 201 (13,180 rows), 203, 209, 204, 205, 206, 202. 20.5% of these orders appear in Notif History. | Order type per prefix UNDEFINED; most orders have no notification. | Cast to string. Derive `order_prefix` (3 digits) as a label. Flag `has_notification`. |

---

## 3. Notif History.xlsx

**Diagram purpose:** Maintenance notification; "Equipment Criticality & Failure History".
**Diagram grain:** One maintenance notification.
**Raw shape:** 5,795 rows x 12 columns. No exact duplicates.
**Key status:** Notification is unique (OBSERVED).

| # | Column | Business meaning | Current type | Recommended type | Class | Role | Observed profile | Potential issues | Recommended treatment |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Notification Date | Date of the notification. Difference from Created On UNDEFINED. | datetime | `datetime64[ns]` | Temporal | Event date | 2025-05-02 to 2026-09-30; 1,463 records in May 2025 against about 260 per later month. | Possible backlog load in the first month (HYPOTHESIS). | Keep. Flag first-month records for sensitivity checks. |
| 2 | Notification | Notification number. | int64 | `string` | Identifier | PK | 5,795 distinct; 12 digits; prefix 101 = N1, 102 = N2, 103 = N3, 106 = N6 (one to one). | None found. | Cast to string. Validate prefix-to-type rule. |
| 3 | Notification Type | Notification category. Code meanings UNDEFINED. | str | `category` | Categorical | Dimension | N1 3,871, N3 1,788, N2 135, N6 1. | N6 is a singleton. | Keep codes. Do not label as failure or request until defined. |
| 4 | Order | Maintenance order created from the notification. DIAGRAM: FK to Movement Order. | float64 | `string` (nullable) | Identifier | FK | 553 nulls (9.5%), all on In Progress notifications; 5,242 non-null, 5,190 distinct; 52 orders on two or more notifications; prefixes 201 and 202 only. | Stored as float (risk of "201000000108.0" text). | Convert float to integer then string; keep nulls as `<NA>`. Flag shared orders. |
| 5 | Priority | Priority of the notification. | str | `category` (unordered until approved) | Categorical | Dimension | Medium 3,581, Low 1,669, High 410, Emergency 135. Emergency occurs only on N2, and every N2 is Emergency. | The obvious order Low < Medium < High < Emergency is plausible but not documented. | Keep labels. Store as unordered category. Apply an order only after approval. |
| 6 | Functional Location | Location the notification is raised on. DIAGRAM: FK to FuncLoc list. | str | `string` | Identifier | FK | 2,219 distinct; 100% found in FuncLoc list; 394 rows on SITE-level locations; up to 114 notifications per location. | System-level versus equipment-level mix. | Keep. Flag `is_system_level` from FuncLoc. |
| 7 | Description | Short text of the notification. | str | `string` | Descriptive | Label, text feature | 3,122 distinct; mixed case; 4.8% start with a bracketed code such as "[MSI-B-25-PTP-346/M]"; common first words Replace, Install, Leak, Overhaul. | Free text; repeated texts on the same location (1,200 rows repeat a location and description pair). | Keep original. Extract bracketed prefix into `desc_ref_code`. Text classification belongs to EDA, not preparation. |
| 8 | Created On | Record creation date. Difference from Notification Date UNDEFINED. | datetime | `datetime64[ns]` | Temporal | Audit date | Equals Notification Date in 98.9% of rows. | Unknown which date is authoritative. | Keep both. Flag rows where they differ. |
| 9 | Required Start | Required start of the work. | datetime | `datetime64[ns]` | Temporal | Planned date | 2024-03-28 to 2029-03-18; 370 rows before Notification Date. | Required start before the notification exists. | Keep. Flag. Do not correct. |
| 10 | Required End | Required end of the work. | datetime | `datetime64[ns]` | Temporal | Planned date | Up to 2029-05-31; never before Required Start. | Far-future dates. | Keep. Flag dates after the data cutoff. |
| 11 | Completion by Date | Date the notification was completed. Meaning inferred from the name; confirm. | datetime | `datetime64[ns]` | Temporal | Event date | 1,305 nulls, exactly the In Progress rows; 2025-05-02 to 2026-09-29; never before Notification Date; 2,028 of 4,490 completions are after Required End. | Null is meaningful (not missing data). | Keep nulls. Never impute. Treat as censored in duration analysis. |
| 12 | Status | Notification status. | str | `category` | Categorical | Dimension | Complete 4,490, In Progress 1,305. Fully consistent with Completion by Date. | Snapshot date of status UNDEFINED. | Keep. Validate status to completion-date consistency. |

---

## 4. Mitem & Mplan.xlsx

**Diagram purpose:** Maintenance plan and item; "Maintenance Plan".
**Diagram grain:** One maintenance item within a maintenance plan.
**Diagram note:** Maintenance plans and items do not include the spare parts required to perform the work.
**Raw shape:** 10,153 rows x 9 columns. No exact duplicates.
**Key status:** Maintenance Item is unique (OBSERVED).

| # | Column | Business meaning | Current type | Recommended type | Class | Role | Observed profile | Potential issues | Recommended treatment |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Functional Location | Location the maintenance item applies to. DIAGRAM: FK to FuncLoc list. | str | `string` | Identifier | FK | 5,785 distinct; 100% found in FuncLoc list; up to 8 items per location. | None found. | Keep. Validate FK. |
| 2 | FunctLocDescrip. | Location description, copied from the location master. | str | `string` | Descriptive | Label | Identical to FuncLoc list description in 100% of rows. | Redundant. | Keep in staged layer; drop from marts (take from FuncLoc list). Validate equality. |
| 3 | ABC Indicator | Criticality code on the item. | str | `category` | Categorical | Dimension | A 2,529, B 2,034, C 4,258, S 1,332; equal to FuncLoc Criticallity in 100% of rows; one value per location. | Redundant with the location master; meaning UNDEFINED. | Keep in staged layer; validate equality; use FuncLoc Criticallity in marts. |
| 4 | Maintenance Plan | Plan number. | int64 | `string` | Identifier | Group key | 3,823 distinct; 12 digits; 1 to 30 items per plan; 710 plans cover more than one location. | None found. | Cast to string. |
| 5 | Maintenance Item | Maintenance item number. | int64 | `string` | Identifier | PK | 10,153 distinct; 5 or 6 digits. | Variable length. | Cast to string without padding. |
| 6 | Maint. item text | Task description. | str | `category` | Categorical (short text) | Dimension | 51 distinct values, such as Calibration (779), Thickness Measurement (703); near-duplicate wording exists ("Final Element Inspection; Control Valve" and "Final Element Inspection; CV"). | Synonymous texts counted as different tasks. | Keep original. Propose a reviewed synonym map (requires validation). |
| 7 | Priority | Plan item priority. Meaning UNDEFINED. | int64 | `category` | Categorical | Dimension | Values 2 (8,650) and 3 (1,503). | Numeric code, not a quantity; direction of urgency unknown. | Cast to category. Never average. |
| 8 | Cycle Descriptions | Maintenance interval as text. | str | `category` | Categorical | Dimension, source of derived interval | 28 spellings, including 1 YEARLY, YEARLY, Yearly, 12 MONTHLY, 4 MONTH, 12 WEEK, Monthly, Weekly. | Same interval written several ways; mixed case. | Keep original. Map to (interval_value, interval_unit) through an approved mapping table. |
| 9 | Start of cycle | Cycle start date. Whether it is the anchor date, the first due date, or the last completion is UNDEFINED. | datetime | `datetime64[ns]` | Temporal | Anchor date | 2015-09-01 to 2029-12-12; 7,718 of 10,153 on day 1 of a month; 344 after 2026-11-04. | Meaning decides every projected due date. | Keep. Flag future starts. Due-date projection requires an approved definition. |

---

## 5. BoM.xlsx

**Diagram purpose:** Spare part per functional location plus inventory; "Spare Part Master Data" and "Current Inventory Position".
**Diagram grain:** One material assigned to one functional location.
**Raw shape:** 20,653 rows x 9 columns.
**Exact duplicate rows:** 230. After setting them aside, (Functional Loc., Material No) is unique.
**Mixed grain (OBSERVED):** Installed Qty belongs to the location and material pair. Material Desc., Unit, Min.Qty, Max.Qty, Stock and MRP Type are identical on every row of the same material, so they are material-level attributes repeated across rows.

| # | Column | Business meaning | Current type | Recommended type | Class | Role | Grain level | Observed profile | Potential issues | Recommended treatment |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Functional Loc. | Location the material is assigned to. DIAGRAM: FK to FuncLoc list. | str | `string` | Identifier | PK part, FK | Pair | 4,516 distinct; 100% found in FuncLoc list; up to 227 materials per location. | Column name differs from other tables ("Functional Loc." versus "Functional Location"). | Rename to `functional_location` in staged layer. Validate FK. |
| 2 | Material No | Material number. DIAGRAM: FK to Movement and PR PO. | int64 | `string` | Identifier | PK part, FK | Pair | 7,481 distinct; 10 digits; prefixes 4300 (3,742), 4100 (3,420), 4200 (319), meaning UNDEFINED; 2,165 materials on more than one location (one on 308). | None found. | Cast to string. Derive `material_prefix` (4 digits) as a label. |
| 3 | Material Desc. | Material description. | str | `string` | Descriptive | Label | Material | 7,017 distinct; 438 rows with leading or trailing spaces; 133 descriptions map to 597 material numbers. | Whitespace; same text on different material numbers. | Keep original; add trimmed copy; flag same-description groups; never merge material numbers. |
| 4 | Installed Qty | Quantity of the material installed on the location. Meaning inferred from the name; confirm. | float64 | `Float64` | Numerical | Measure | Pair | 25 distinct values; 1.0 on 15,882 rows; large values 1,500 and 5,037 occur; 89 rows are not whole numbers. | Large values may be bulk materials (KG, L, M); unit is the material's Unit. | Keep. Never sum across materials. Flag non-integer values on count units (EA, SET, ASS). |
| 5 | Unit | Unit of measure of the material. | str | `category` | Categorical | Dimension | Material | 10 units; one per material; matches PR PO and Movement units. | Unit code meanings UNDEFINED. | Keep. No conversion. |
| 6 | Min.Qty | Minimum quantity planning parameter. Whether it is a reorder point, safety stock or minimum level is UNDEFINED. | int64 | `Int64` | Numerical | Planning parameter | Material | 0 to 2,000; 0 for every Non Stock material. | Not physical warehouse capacity. Meaning unknown. | Keep. Analyse at material level only. Never treat as capacity. |
| 7 | Max.Qty | Maximum quantity planning parameter. Meaning UNDEFINED. | int64 | `Int64` | Numerical | Planning parameter | Material | 0 to 3,344; Min never exceeds Max; 0 for every Non Stock material. | Not warehouse capacity. | Keep. Material level only. |
| 8 | Stock | Stock on hand. Snapshot date, plant and storage location UNDEFINED. | float64 | `Float64` | Numerical | Measure (state) | Material | 0 to 95,432; 5,687 rows at zero; 3 non-integer rows (0.5 EA on material 4300057364; 4.5 KG on 4100092523). | Repeated per location row; summing across BoM rows double counts. Undated. | Keep. Analyse at one row per material. Flag 0.5 EA as a unit anomaly. |
| 9 | MRP Type | Planning class. | str | `category` | Categorical | Dimension | Material | Stock Item 3,656 materials, Non Stock 3,825 materials; 1,683 Non Stock materials have stock above zero. | Meaning of Non Stock with stock UNDEFINED. | Keep. Flag `nonstock_with_stock`. Do not call zero stock a stockout without a business rule. |

**Columns absent from BoM:** price or valuation, storage location, warehouse, plant, stock date, lead time, safety stock, criticality of the material itself.

---

## 6. FuncLoc list.xlsx

**Diagram purpose:** Functional location master; "Equipment Criticality & Failure History".
**Diagram grain:** One functional location (location, sub-location or system).
**Raw shape:** 14,484 rows x 3 columns. No exact duplicates.
**Key status:** Functional Location is unique (OBSERVED).

| # | Column | Business meaning | Current type | Recommended type | Class | Role | Observed profile | Potential issues | Recommended treatment |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Functional Location | Functional location code. | str | `string` | Identifier | PK | 14,484 distinct. Prefixes before the first underscore: PX 12,983, PY 1,411, UT 57, SITE 33. SITE rows look like SITE_PX_S01 or SITE_PY_0100. | Prefix meaning UNDEFINED. No parent column, so the hierarchy is not stored. | Keep. Derive `fl_prefix`. Derive tag-pattern candidates as labels only (see specification). Do not infer parents. |
| 2 | FunctLocDescrip. | Location description. | str | `string` | Descriptive | Label | 7,944 distinct; generic texts repeat (TEMPERATURE 826, PRESSURE GAUGE 270). SITE rows name systems (for example CRACKED GAS COMPRESSION SYSTEM, TANK FARM, JETTY, WAREHOUSE). | Not an identifier. | Keep original; add trimmed copy. |
| 3 | FuncLoc Criticallity | Criticality class (spelling as in source). Code meanings and ranking UNDEFINED. | str | `category` (unordered) | Categorical | Dimension | C 7,298, A 2,668, B 2,581, S 1,904, null 33. All nulls are the 33 SITE rows. | No documented order; S does not fit an A to C sequence. | Keep codes as an unordered category. Keep nulls; flag `criticality_missing` with reason "system-level row". No ranking until approved. |

---

## 7. Cross-table naming map

The same business concept appears under different column names. The staged layer uses one standard name.

| Standard name | PR PO | Movement Material | Notif History | Mitem & Mplan | BoM | FuncLoc list |
| --- | --- | --- | --- | --- | --- | --- |
| `material_no` | PR-Material | Material Number | | | Material No | |
| `material_desc` | PR-Material Desc | Material Descriptions | | | Material Desc. | |
| `unit` | PR-UoM | Base Unit | | | Unit | |
| `functional_location` | | | Functional Location | Functional Location | Functional Loc. | Functional Location |
| `fl_desc` | | | | FunctLocDescrip. | | FunctLocDescrip. |
| `order_no` | | Order | Order | | | |
| `criticality` | | | | ABC Indicator | | FuncLoc Criticallity |
| `priority` | | | Priority (text) | Priority (number) | | |

**Warning:** The two Priority columns are different code systems (text levels in Notif History, numbers 2 and 3 in Mitem & Mplan). They must keep separate standard names: `notif_priority` and `plan_priority`.

---

## 8. Open definitions required from the case owner

| ID | Field or code | Question |
| --- | --- | --- |
| DEF-01 | PR PO exact duplicates | Are repeated identical rows the same document line recorded more than once, or real repeated lines? |
| DEF-02 | Min.Qty, Max.Qty | Reorder point and maximum level, or other parameters? Per plant or per storage location? |
| DEF-03 | FuncLoc Criticallity A, B, C, S | Meaning of each code and their rank order. |
| DEF-04 | MRP Type Non Stock | Why do 1,683 Non Stock materials hold stock? |
| DEF-05 | PO-Item Amount | Line total or unit price? Net or gross? Tax included? |
| DEF-06 | PO-Delivery Date | Promised date? Is a goods-receipt date available? |
| DEF-07 | Order prefixes 201 to 209 | Order type for each prefix. |
| DEF-08 | PR-Type, PO prefix, Purchasing Group | Meaning of each code. |
| DEF-09 | Notification Type N1, N2, N3, N6 | Meaning of each type. |
| DEF-10 | Cycle Descriptions | Confirm the interval mapping table (specification Section 3.5). |
| DEF-11 | Start of cycle | Anchor date, first due date or last completion? |
| DEF-12 | Stock snapshot | Date of the Stock value. |
| DEF-13 | Plant 1000, material prefixes, location prefixes PX, PY, UT | What each stands for. |
| DEF-14 | Notification Date versus Created On | Which date is authoritative? |
| DEF-15 | Unit codes LG, RL, ASS, SHT | Meaning of each unit. |
