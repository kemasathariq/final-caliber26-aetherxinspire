# CALIBER 2026 Analytical Discovery Report

Six-workbook data understanding and analytical opportunity assessment · Nov 4, 2026 · @Thoriq

## How to read this report

Every statement carries one of five labels, so you can see what is proven and what is not.

| Label | Meaning |
| --- | --- |
| SOURCE FACT | Stated in a supplied case document, such as the Data Context and Relationship Diagram. |
| OBSERVATION | Counted directly from the raw workbooks during read-only inspection. Preliminary, because no cleaning rule has been agreed yet. |
| HYPOTHESIS | A possible explanation or finding that still needs a test. Not a result. |
| AMBIGUITY | A field or rule whose meaning the files do not establish. Needs clarification from the case owner. |
| RECOMMENDATION | My proposal. A judgement, not a fact. |

**How the evidence was produced.** I opened each workbook read-only and counted rows, distinct values, nulls, key uniqueness and join coverage. I did not clean, deduplicate, transform or save any file. Counts marked "raw" include duplicate rows. A count marked "distinct" ignores exact duplicate rows only for that one check; the source files are unchanged.

**Scope.** Internal data only. No external supplier research was done for this report.

## 1. Executive overview

The six workbooks support a strong spare-part inventory, demand and maintenance-linkage analysis. They do not support a classical transportation model without invented data.

**What the data is.** The case diagram states that all six files are synthetic (dummy) data built for the Caliber 2026 Hackathon. They mirror the structure of the real system but not its values. The diagram is titled "Case 3, Spare Part Intelligence". (SOURCE FACT)

**Five things that matter most** (OBSERVATION unless labelled)

1. **Links through Functional Location are clean.** Every Functional Location used in BoM, Notif History and Mitem & Mplan exists in the FuncLoc list.
2. **Links through Material run one way.** All 1,250 procured materials and all 1,930 issued materials exist in the BoM. But the BoM has 7,481 materials, so only 16.7% were procured and 25.8% were issued in the period.
3. **The Order link is weak.** Only 20.5% of the orders in Movement Material appear in Notif History. When the link exists, only 22.6% of the issued materials appear in the BoM of that notification's Functional Location.
4. **PR PO has heavy duplication.** 5,420 of 11,609 rows (46.7%) are exact copies of another row. After setting copies aside, PR plus PR-Item becomes a unique key. Whether the copies are errors is NOT ESTABLISHED.
5. **The supply network is degenerate.** There is one plant (1000), each of the 1,250 materials has exactly one supplier, and no file holds supplier location, capacity, freight cost, warehouse or storage location.

**What this means** (RECOMMENDATION)

- The best-supported directions are inventory policy against actual consumption, criticality-weighted stock exposure, intermittent-demand classification, and closing the gap between maintenance work and spare-part master data.
- Transportation optimization with CSM and MODI can only be shown as a clearly labelled scenario. The supplied data does not justify it as a finding.
- Confirm four business definitions with the case owner before any EDA (Section 4).

## 2. Six-workbook dataset assessment

All six files have one sheet named "Data", as the diagram states. Five of the six have a key that holds once exact duplicate rows are set aside.

| Workbook | Purpose (per diagram) | Rows x cols | Grain (one row is) | Key tested | Exact duplicate rows | Time column, range |
| --- | --- | --- | --- | --- | --- | --- |
| FuncLoc list | Equipment criticality master | 14,484 x 3 | One functional location | Functional Location, unique | 0 | None |
| BoM | Spare part master and current inventory | 20,653 x 9 | One material on one functional location | Functional Loc. + Material No, unique after duplicates | 230 | None (stock is an undated snapshot) |
| Movement Material | Spare part consumption history | 17,518 x 7 | One issue transaction | No natural key | 863 | Posting Date, 2025-05-06 to 2026-09-30 |
| Notif History | Maintenance notifications | 5,795 x 12 | One notification | Notification, unique | 0 | Notification Date, 2025-05-02 to 2026-09-30 |
| PR PO | Procurement and lead time | 11,609 x 18 | One PR item linked to one PO item | PR + PR-Item, unique only after duplicates | 5,420 | PR-Date, 2025-05-04 to 2026-09-22 |
| Mitem & Mplan | Maintenance plan items | 10,153 x 9 | One maintenance item in a plan | Maintenance Item, unique | 0 | Start of cycle, 2015-09-01 to 2029-12-12 |

All counts are OBSERVATION from read-only inspection.

### 2.1 FuncLoc list

- **Columns.** Functional Location (text key), FunctLocDescrip. (text), FuncLoc Criticallity (category A, B, C, S).
- **Hierarchy is implied, not stored.** Codes start with PX (12,983), PY (1,411), UT (57) or SITE (33). The 33 SITE rows are system-level areas such as "CRACKED GAS COMPRESSION SYSTEM", "TANK FARM", "JETTY" and "WAREHOUSE". There is no parent column, so a tree can only be guessed from code patterns. (OBSERVATION)
- **Criticality.** C 7,298, A 2,668, B 2,581, S 1,904. All 33 nulls are the SITE rows. (OBSERVATION)
- **Ambiguity.** The meaning of A, B, C and S is not documented. S is not an obvious step in an A to C scale.
- Descriptions repeat: 7,944 distinct texts for 14,484 locations, so description is not an identifier.

### 2.2 BoM

- **Columns.** Functional Loc., Material No, Material Desc., Installed Qty (number), Unit (10 codes), Min.Qty, Max.Qty, Stock (numbers), MRP Type (Stock Item, Non Stock).
- **Mixed grain.** Installed Qty belongs to the location and material pair. Stock, Min.Qty, Max.Qty, MRP Type, Unit and description are identical for every row of the same material. So they are material-level values repeated across rows. Summing Stock across BoM rows double counts. (OBSERVATION)
- **Material level, 7,481 materials.** 3,656 Stock Item and 3,825 Non Stock. Among Stock Items: 472 have zero stock, 504 are below Min, 1,380 are above Max, 29 have Min = Max = 0. Every Non Stock material has Min = Max = 0, yet 1,683 of them hold stock above zero. (OBSERVATION)
- 2,165 materials sit on more than one location; one material sits on 308.
- Material numbers start with 4300 (3,742), 4100 (3,420) or 4200 (319). The meaning of these prefixes is unknown.
- Three Stock values are not whole numbers. No negative stock.
- **Not present.** Price, value, storage location, warehouse, plant, stock date.

### 2.3 Movement Material

- **Columns.** Posting Date, Movement Type, Material Number, Material Descriptions, Quantity (whole numbers 1 to 23,135), Base Unit, Order.
- **Only issues.** Movement Type has one value, "Issue". There are no goods receipts, returns or transfers, so stock cannot be rebuilt from movements. (OBSERVATION)
- 863 rows duplicate another row in every column. Two identical issues on the same day and order are possible in real life, so these are not proven errors. (HYPOTHESIS to verify)
- Orders start with 201 to 209. The order types behind these prefixes are not documented.
- 4,884 orders, median 2 lines per order, maximum 128.

### 2.4 Notif History

- **Columns.** Notification Date, Notification (key), Notification Type (N1 3,871, N3 1,788, N2 135, N6 1), Order, Priority (Medium 3,581, Low 1,669, High 410, Emergency 135), Functional Location, Description (free text), Created On, Required Start, Required End, Completion by Date, Status (Complete 4,490, In Progress 1,305).
- **Consistent rules found.** Every N2 is Emergency, and Emergency appears only on N2. Every Complete row has a completion date, and no In Progress row has one. Notification prefixes map one to one to types (101 = N1, 102 = N2, 103 = N3, 106 = N6). (OBSERVATION)
- **Orders.** 553 notifications (9.5%) have no order. 52 orders sit on more than one notification.
- **Date issues.** 370 rows have Required Start before the notification date. 2,028 of 4,490 completed notifications (45.2%) finished after Required End. Days from notification to completion: median 41, maximum 490. Created On equals Notification Date in 98.9% of rows.
- 394 notifications sit on SITE-level locations rather than equipment.
- Description text starts mostly with Replace (1,009), Install (922), Leak (753), Overhaul (232). It could be classified into failure versus routine work. (HYPOTHESIS)

### 2.5 PR PO

- **Columns.** PR-Type (7 codes), Purchase Requisition, PR-Item, PR-Date, PR-Material, PR-Material Desc, PR-Quantity, PR-UoM, PR-Delivery Date, PR-Plant, PR-Purchasing Group (19 codes), Purchase Order, PO-Item, PO-Supplier Code, PO-Supplier Name, PO-Item Amount, PO-Currency, PO-Delivery Date.
- **Duplication.** Of 6,189 distinct rows, 2,589 appear once, 2,300 twice, 780 three times and 520 four times. After setting copies aside, PR + PR-Item and PO + PO-Item are both unique, which points to replicated rows rather than different transactions. (OBSERVATION) I tested one explanation, that the copy count equals the number of BoM locations per material. It does not hold (match in 10% of rows, correlation -0.008). (OBSERVATION)
- **Structure.** PR-Plant is 1000 on every row. Each PO has one supplier. A PO groups 1 to 27 PRs (mean 3.4). PR-Type maps one to one to the PR number prefix. PO numbers start with 43, 45, 80 or 86 across all PR types.
- **Suppliers.** 124 codes, one name each. 118 Indonesian names follow one four-word template; 6 foreign suppliers each use their own currency. Each of the 1,250 materials has exactly one supplier.
- **Currency.** IDR 11,511 rows, JPY 41, USD 35, EUR 20, SGD 2. No exchange rates are supplied.
- **Date logic, raw rows.** PO-Delivery minus PR-Date: median 42 days, 6 negative. PR-Delivery minus PR-Date: median 37 days, 630 negative (as low as -500). PO-Delivery is earlier than the requested PR-Delivery in 4,232 rows. Delivery dates run to 2028 and 2029.
- **Price.** For 877 material and currency pairs with two or more distinct lines, the highest amount per unit is a median 2.04 times the lowest (maximum 5.28). This assumes PO-Item Amount is the line total, which is not documented.
- **Not present.** PO creation date, goods receipt date, net price per unit, incoterms, supplier location.

### 2.6 Mitem & Mplan

- **Columns.** Functional Location, FunctLocDescrip., ABC Indicator, Maintenance Plan, Maintenance Item (key), Maint. item text (51 values), Priority (2 = 8,650, 3 = 1,503), Cycle Descriptions (28 values), Start of cycle.
- **Redundant columns.** ABC Indicator equals FuncLoc Criticallity, and FunctLocDescrip. equals the FuncLoc list description, in 100% of rows. (OBSERVATION)
- **Cycle text is not standardised.** The same interval appears as "1 YEARLY", "YEARLY", "Yearly" and "12 MONTHLY". Converting to days needs an agreed mapping.
- 710 plans cover more than one location (up to 30).
- Start of cycle runs from 2015 to 2029. 344 items start after today. 7,718 dates fall on day 1 of a month.
- **Not present.** Required materials per task, task duration, last or next due date, completion history. The diagram itself says plans do not include required spare parts. (SOURCE FACT)

## 3. Preliminary relationship map

The diagram's seven relationships all exist in the fields, but only the three Functional Location joins are complete. Material and Order joins leave most records unmatched.

| # | Join (parent to child) | Key | Diagram says | Observed cardinality | Child keys found in parent | Parent keys used by child | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | FuncLoc list to BoM | Functional Location = Functional Loc. | 1 : N | 1 : N, 4,516 locations | 100% | 31.2% | Supported |
| 2 | FuncLoc list to Notif History | Functional Location | 1 : N | 1 : N, 2,219 locations, up to 114 notifications each | 100% | 15.3% | Supported |
| 3 | FuncLoc list to Mitem & Mplan | Functional Location | 1 : N | 1 : N, 5,785 locations | 100% | 39.9% | Supported |
| 4 | BoM to Movement Material | Material No = Material Number | Material link | N : N at row level (material repeats in both) | 100% of 1,930 | 25.8% of 7,481 | Supported, aggregate first |
| 5 | BoM to PR PO | Material No = PR-Material | Material link | N : N at row level | 100% of 1,250 | 16.7% of 7,481 | Supported, aggregate first |
| 6 | Notif History to Movement Material | Order | 1 : N | Mostly 1 : N; 52 orders sit on 2 or more notifications | 20.5% of 4,884 movement orders | 19.3% of 5,190 notification orders | Weak |
| 7 | Mitem & Mplan to BoM | via Functional Location | Indirect, no spare-part link | Indirect N : N | n/a | 894 locations appear in BoM, Notif and Mitem together | Context only |

All figures are OBSERVATION.

**Not in the diagram, but supported by the fields** (OBSERVATION)

- **Movement Material to PR PO by material.** 1,030 materials are both issued and procured. 900 issued materials were never procured in the period, and 220 procured materials were never issued.
- **Material attributes agree everywhere.** For every material shared between tables, description and unit match exactly. This makes material number a trustworthy key.
- **Same description, different material numbers.** 39 PR descriptions map to more than one material number (36 of them bought from different suppliers). In the BoM, 133 descriptions map to 597 material numbers. These may be duplicate master records or true variants. (AMBIGUITY)

**Orphans and gaps** (OBSERVATION)

- No child key is orphaned on the Functional Location side.
- 3,881 movement orders have no notification. Notification orders start only with 201 or 202, while movement orders also start with 203 to 209. Those other order types are never in Notif History. (HYPOTHESIS: they are preventive or other order types raised without a notification.)
- 553 notifications have no order, so they can never link to consumption.
- For 2,851 movement lines that link to a notification, the issued material is in the BoM of that notification's location in only 22.6% of cases. Either the BoM is incomplete, or materials are issued to an order at a different level of the location tree. (HYPOTHESIS)
- Posting date minus notification date for linked lines: median 7 days; 20 lines were posted before the notification.

**Double-counting risks** (RECOMMENDATION: rules to adopt before any join)

1. Never sum BoM Stock, Min.Qty or Max.Qty across BoM rows. Take one row per material first.
2. Never join BoM to Movement or PR PO at row level and then sum quantities. Aggregate each side to material first, then join.
3. Decide the PR PO duplicate rule before any spend or quantity total. Raw totals and distinct-row totals differ by about half.
4. Joining Notif to Movement on Order duplicates movement lines for the 52 shared orders. Allocate or flag them.
5. Mitem & Mplan joined to BoM through location creates every plan item times every material on that location. It does not mean the plan needs those parts.

&#91;embedded content: six project workbooks, read-only inspection, 4 Nov 2026\]

Every location key resolves, but only one in four BoM materials was issued and only one in five movement orders reaches a notification.

## 4. Data limitations and ambiguities

Fourteen points need a decision or a definition before EDA. The first four change results the most.

| # | Item | Why it matters | Question for the case owner |
| --- | --- | --- | --- |
| 1 | PR PO exact duplicates (46.7% of rows) | Spend, quantity and lead-time statistics roughly double or shift | Are repeated rows real repeat lines, or a data-generation artifact to remove? |
| 2 | Synthetic data (SOURCE FACT) | Values such as prices, supplier names and dates may follow generator rules, not business behaviour | Which fields keep realistic patterns, and which are random? |
| 3 | BoM Stock is undated, Movement has only issues | No stock balance over time, no stockout history | What date is the Stock snapshot? Are receipts available? |
| 4 | Min.Qty and Max.Qty meaning | Defines below-minimum and excess stock | Are these reorder point and maximum stock level per plant, in the material's unit? |
| 5 | Criticality codes A, B, C, S | Drives every criticality-weighted analysis | What does each code mean, and how does S rank against A? |
| 6 | Non Stock with stock above zero (1,683 materials) | Could be leftovers, project stock or data error | What does Non Stock mean in this MRP setup? |
| 7 | PO-Item Amount | Unit price is only valid if this is the line total | Is it the net line value, in the PO currency, including or excluding tax? |
| 8 | PO-Delivery Date | It is a promised or planned date, not a receipt | Is a goods-receipt date available? |
| 9 | No PO creation date | PR-to-PO approval time cannot be measured | Can the PO date be supplied? |
| 10 | Order prefixes 201 to 209 | Only 201 and 202 appear in Notif History | What order type does each prefix stand for? |
| 11 | PR-Type, PO number prefix and Purchasing Group codes | Needed to separate routine, project and emergency buying | What do PR01 to PR10 and the 19 groups mean? |
| 12 | Notification types N1, N2, N3, N6 | N2 is always Emergency; others mix priorities | What does each type mean (for example, failure versus request)? |
| 13 | Cycle Descriptions in 28 spellings | Interval in days cannot be computed without a mapping | Confirm "YEARLY" = 12 months, "12 WEEK" = 84 days, and so on |
| 14 | Plant 1000, material prefixes 4100, 4200, 4300, location prefixes PX, PY, UT | Scope and grouping | Which site or plant section does each stand for? |

**Structural limits that no definition fixes** (OBSERVATION)

- One plant, one destination. No storage location or warehouse field in any table. The only "WAREHOUSE" is a functional location.
- One supplier per material. No observed alternative source for any material.
- No supplier location, capacity, freight cost or transport mode anywhere.
- About 17 months of history (May 2025 to September 2026). Annual seasonality cannot be tested with fewer than two full years.
- No cost of downtime, holding cost rate or ordering cost.

**Uneven time coverage.** The chart below shows records per month in the three dated tables. Two shapes stand out: Notif History has 1,463 records in May 2025 against about 260 in later months, and Movement Material peaks at 2,580 issues in December 2025. (OBSERVATION) The first may be a backlog loaded at system start; the second may be a turnaround or major maintenance event. (HYPOTHESIS, not tested)

&#91;embedded content: PR PO.xlsx (PR-Date), Movement Material.xlsx (Posting Date), Notif History.xlsx (Notification Date) · raw rows, May 2025 to Sep 2026\]

PR PO stays near 700 rows a month, so the two spikes come from the maintenance side, not from buying.

## 5. Analytical opportunity matrix

Four of the ten opportunities are well supported by the current data (B, C, J and A). Two are only possible as scenarios (G and H). Every "possible finding" below is a HYPOTHESIS, not a result. Feasibility ratings are RECOMMENDATION.

| Opportunity | Business problem | Datasets and key columns | Methods | Possible findings (HYPOTHESIS) | Extra data needed | Feasibility now |
| --- | --- | --- | --- | --- | --- | --- |
| A. Procurement intelligence | Slow or unpredictable buying for spare parts | PR PO: PR-Date, PR-Delivery Date, PO-Delivery Date, PR-Type, Purchasing Group, Amount, Currency | Interval distributions by type and group, spend Pareto per currency, promise-versus-request gap, price dispersion per material | A few purchasing groups carry most long promised lead times; emergency PR types get shorter promises | Goods-receipt date, PO date, exchange rates, duplicate rule | Partial to high |
| B. Inventory optimization | Stock that is too low for critical parts and too high for others | BoM (one row per material): Stock, Min.Qty, Max.Qty, MRP Type; Movement: Quantity, Posting Date | Months of cover, stock versus Min and Max, demand during lead time versus Min, slow and non-moving stock, ABC-XYZ | Many Stock Items sit above Max while some critical ones sit below Min; Min/Max is not aligned with observed issues | Unit cost for non-procured materials, stock date, receipts | High, after definitions |
| C. Demand and consumption | Planners cannot tell steady demand from rare spikes | Movement: Material Number, Quantity, Posting Date, Order | Monthly series, ADI and CV squared classification (Syntetos-Boylan), Pareto of issue lines, outlier detection | Most materials are intermittent or lumpy; a small set drives most issue lines | Longer history (2 years or more) | High |
| D. Maintenance-driven planning | Parts for planned work are not prepared in advance | Mitem: Cycle Descriptions, Start of cycle, Functional Location; BoM; Movement via Order | Project plan due dates from cycles, map plan locations to BoM materials as candidate kits, compare with issues on orders | Some plan-heavy locations have BoM parts at zero stock; but kits stay unconfirmed | Task lists or planned components per plan, last completion date | Partial |
| E. Reliability and failure patterns | Repeat problems on the same equipment | Notif: Functional Location, Type, Priority, Description, dates; FuncLoc: Criticallity | Notifications per location, repeat-notification intervals, text classification of Description, priority against criticality | A small number of locations generate most notifications; Leak and Replace texts cluster on certain equipment | Failure codes, downtime hours, breakdown flag | Partial |
| F. Supplier concentration and risk | Dependence on one supplier per part | PR PO: Supplier Code, Material, Amount | Spend share and HHI (a concentration index) per currency, category-level supplier counts, same-description-different-code pairs | Concentration is total at material level (already observed); categories have alternative suppliers (median 11) | Approved vendor list, material equivalence rules | Partial |
| G. Warehouse and material allocation | Parts not stored where work happens | BoM, FuncLoc (one SITE row named WAREHOUSE) | Criticality-based stocking classes only | Cannot be tested: no storage locations | Storage locations, bin capacity, stock per location | Low, scenario only |
| H. Transportation and distribution | High freight cost or slow delivery | PR PO: Supplier, Plant | Classical transportation model, CSM, MODI | Cannot be tested with supplied data (Section 9) | Supplier sites, more than one destination, capacities, unit freight costs | Not feasible as a finding |
| I. Forecasting and predictive maintenance | Demand and failures arrive unannounced | Movement (demand); Notif (events) | Croston, SBA, TSB against naive baselines with time-ordered holdout; time-between-notification models | Intermittent-demand methods beat naive averages for lumpy parts; condition prediction is not possible | Sensor or condition data linked to locations, longer history | Forecasting partial; predictive maintenance low |
| J. Integrated supply chain intelligence | No single view from equipment risk to part availability | All six, joined by location and material | Exposure score per material: criticality of locations served, stock versus Min, demand rate, promised lead time | A short list of materials on critical equipment with low stock and long lead time | Definitions in Section 4 | High, the most differentiated |

**Why J ranks highest.** It is the only direction that uses all six workbooks and turns the join gaps into findings in their own right. For example, materials issued to an order but missing from that location's BoM are a master-data quality signal. (RECOMMENDATION)

## 6. Proposed EDA methodology

The EDA should run in five stages, and no stage should start before the grain and duplicate rules of Stage 0 are agreed. All of this section is RECOMMENDATION. Nothing here has been run.

**Rules that apply to every analysis**

- Keep raw files untouched. Every derived table states its grain and the duplicate rule used, with row counts before and after.
- Do not add quantities across different units (EA, KG, L, RL and others). Compare within one unit or use counts of issue lines.
- Do not add amounts across currencies without a documented exchange rate.
- Treat dates as promised or planned unless the field proves otherwise.
- Report associations, not causes.

| ID | Objective | Dataset | Required variables | Visualization | Statistical method | Expected output | Business interpretation | Main limitation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **Stage 0. Foundation** |  |  |  |  |  |  |  |  |
| E01 | Confirm keys, grain and duplicate rule | All six | Candidate keys, all columns for exact duplicates | Bar of copy count per PR PO row | Uniqueness tests, before and after counts | Grain register, agreed duplicate rule | Every later total is trustworthy | Rule depends on case owner's answer |
| E02 | Measure join coverage both ways | All six | Functional Location, Material, Order | Material overlap diagram (BoM, Movement, PR PO) | Set coverage percentages | Join coverage table | Shows which questions the data can answer | Synthetic links may not reflect real gaps |
| **Stage 1. Inventory** |  |  |  |  |  |  |  |  |
| E03 | Stock position against policy | BoM, one row per material | Stock, Min.Qty, Max.Qty, MRP Type | Stacked bar of below Min, within, above Max by MRP Type | Proportions with confidence intervals | Stock status per material | Size of shortage and excess risk | Stock is undated |
| E04 | Criticality-weighted exposure | BoM, FuncLoc | Highest criticality of locations each material serves, stock status | Heatmap of criticality by stock status | Chi-square test, Cramer's V (strength of association) | Exposure counts per cell | Whether critical equipment is better protected | Criticality code meanings unconfirmed |
| E05 | Slow and non-moving stock | BoM, Movement | Stock, issue count in 17 months | Bar of stock-holding materials with zero issues, by criticality | Counts, share | Non-moving list | Candidate excess or insurance spares | 17 months is short for rare spares |
| **Stage 2. Demand** |  |  |  |  |  |  |  |  |
| E06 | Consumption trend and spikes | Movement | Posting Date, Quantity, Order | Monthly issue lines, line chart | Rolling median with MAD (median absolute deviation) outlier flags | Spike months and materials | Planned events versus unplanned demand | Spikes may be generator artifacts |
| E07 | ABC-XYZ segmentation | Movement, PR PO for price | Issue lines or value, monthly demand | 3 by 3 matrix of ABC by XYZ | Pareto cut-offs (80, 95%), CV of monthly demand | Segment per material | Different stocking policy per segment | Value only for 1,030 materials with a purchase price |
| E08 | Intermittency classes | Movement | Interval between issues, quantity per issue | Scatter of ADI against CV squared with 1.32 and 0.49 cut-offs | Syntetos-Boylan classification | Smooth, erratic, intermittent or lumpy label | Picks the right forecast method | Needs enough issues per material |
| E09 | Demand versus Min/Max | Movement, BoM, PR PO | Monthly demand, promised lead time, Min.Qty | Scatter of demand during lead time against Min, log scale | Spearman rank correlation | Over and under-set Min values | Where the reorder point does not match use | Lead time is a promise, not a receipt |
| **Stage 3. Procurement** |  |  |  |  |  |  |  |  |
| E10 | Lead-time proxy | PR PO (distinct rows) | PR-Date, PO-Delivery Date, PR-Type, Purchasing Group | Box plots by PR-Type and group | Kruskal-Wallis test (compares medians without assuming normal data) | Lead-time profile per type and group | Which buying channels are slow | No PO or receipt dates |
| E11 | Promise against request | PR PO | PR-Delivery Date, PO-Delivery Date | Histogram of PO minus PR delivery date | Share early, on time, late | Request compliance rate | How often suppliers promise later than needed | 630 rows with requested date before PR date |
| E12 | Spend and supplier concentration | PR PO | Supplier, Amount, Currency | Pareto and Lorenz curve per currency | HHI, top-N share | Concentration profile | Dependence and negotiation leverage | IDR only unless FX is supplied |
| E13 | Price dispersion | PR PO | Amount, Quantity, Material, date | Strip plot of unit price per material | CV, IQR outlier rule | Materials with unstable prices | Possible savings or data errors | Amount meaning unconfirmed |
| **Stage 4. Maintenance** |  |  |  |  |  |  |  |  |
| E14 | Notification concentration | Notif, FuncLoc | Functional Location, Type, Priority, Description | Pareto of notifications per location; heatmap priority by criticality | Chi-square, Cramer's V; keyword rules on Description | Bad-actor locations, work-type classes | Where repeat problems sit | Notifications are not all failures |
| E15 | Notification cycle time | Notif | Notification Date, Completion by Date, Status, Priority | Kaplan-Meier curves by priority | Survival analysis, treating In Progress as unfinished (censored) | Time-to-complete per priority | Backlog and response speed | Required dates look inconsistent |
| E16 | Planned workload ahead | Mitem | Cycle Descriptions, Start of cycle | Bar of plan items due per month ahead | Interval mapping, date projection | Monthly due calendar | When parts demand from planned work may rise | Last completion date is missing |
| E17 | Work order to consumption link | Notif, Movement, BoM | Order, Functional Location, Material | Bar of BoM match rate by location prefix and type | Match rates, posting lag distribution | Linkage quality profile | How complete the BoM is for real work | Only 20.5% of movement orders link |
| **Stage 5. Integrated** |  |  |  |  |  |  |  |  |
| E18 | Material exposure score | All six | Outputs of E03, E04, E08, E10, E14 | Ranked bar of top materials, with score parts | Weighted score with weight sensitivity test | Ranked critical-part watch list | Where to act first | Weights are a judgement; show sensitivity |

## 7. Visualization roadmap

Ten figures are enough to carry the story from data trust to a critical-part watch list. Each one answers one business question. (RECOMMENDATION)

| Order | Figure | Business question it answers | From | Use |
| --- | --- | --- | --- | --- |
| 1 | Data lineage map: six tables, keys and match rates | Can we trust one integrated view? | E01, E02 | Deck, data foundation slide |
| 2 | Material overlap across BoM, Movement and PR PO | How much of the spare-part master is really active? | E02 | Deck |
| 3 | Stock status by MRP Type and criticality (heatmap) | Are critical parts better protected than others? | E03, E04 | Deck, key finding |
| 4 | ADI against CV squared scatter | Which parts can be forecast, and how? | E08 | Analysis, appendix |
| 5 | ABC-XYZ matrix with material counts | Which stocking policy fits each part group? | E07 | Deck |
| 6 | Demand during lead time against Min.Qty | Are reorder points set to real use? | E09 | Deck, key finding |
| 7 | Lead-time proxy box plots by PR-Type and group | Which buying channels are slow? | E10 | Analysis |
| 8 | Pareto of notifications per location with criticality colour | Where do repeat problems sit? | E14 | Deck |
| 9 | Kaplan-Meier time to completion by priority | Does priority speed up the work? | E15 | Analysis |
| 10 | Ranked exposure score with score parts | What should the plant act on first? | E18 | Deck, recommendation slide |

**Standard for every figure**

- A title that states the finding, with its number.
- Units on every axis; sample size (n) and time period in the subtitle.
- Source workbook and the duplicate rule in a footnote.
- One sentence of reading and one caveat beside it.
- No decorative charts: a figure with no business question is dropped.

## 8. Missing data requirements

The items below are absent from all six workbooks. Each one names the analysis it would unlock, so the request to the case owner can be ranked. Priority is RECOMMENDATION.

| Priority | Missing data | Unlocks | Possible substitute if refused |
| --- | --- | --- | --- |
| 1 | Definitions in Section 4 (duplicates, Min/Max, criticality codes, order and PR types) | Every analysis | State each assumption and test sensitivity |
| 1 | Goods-receipt date per PO item | True supplier lead time and delivery reliability | PO-Delivery Date as a promised lead time, labelled PROXY |
| 1 | Unit cost or moving average price for all 7,481 materials | Inventory value, holding cost, value-based ABC | Median PR PO unit price for the 1,250 procured materials only |
| 2 | Stock snapshot date and goods receipts | Stock balance over time, stockout events | Treat Stock as the position at the end of the movement window, labelled ASSUMPTION |
| 2 | Planned components or task lists per maintenance plan | Maintenance-driven part demand (Opportunity D) | Plan location to BoM materials as candidate kits, labelled HYPOTHESIS |
| 2 | Failure codes, breakdown flag and downtime hours on notifications | Reliability analysis and cost of a stockout | Keyword classification of Description |
| 3 | PO creation date | PR-to-PO approval time | None |
| 3 | Exchange rates by date | One spend total across currencies | Analyse IDR only (11,511 of 11,609 raw rows) |
| 3 | Storage location and bin capacity | Warehouse allocation (Opportunity G) | None |
| 4 | Supplier sites, transport mode, freight cost, supplier capacity, more than one destination | Transportation model (Opportunity H) | Scenario data only, clearly labelled |
| 4 | Holding cost rate, ordering cost, service-level targets by criticality | Optimal Min/Max and service trade-offs | Published or stated assumptions with a sensitivity range |
| 4 | Two or more years of history | Seasonality and forecast validation | Short-horizon validation with a stated limit |

## 9. Potential solution directions

Three directions score well on both data availability and business relevance. Transportation optimization scores lowest on data availability. These are directions to test in EDA, not a chosen solution. All ratings are RECOMMENDATION.

| Direction | Opportunities used | Business impact | Data availability | Analytical feasibility | Technical feasibility | Operational relevance | Differentiation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S1. Critical spare-part exposure intelligence (equipment risk to part availability) | J, B, E, A | High | High | High | High | High | High |
| S2. Demand-aware Min/Max review using intermittency classes | B, C, I | High | High | High | High | High | Medium |
| S3. Maintenance-to-material linkage and BoM completeness | D, E, J | Medium to high | Medium | Medium | High | High | High |
| S4. Procurement lead-time and supplier dependence monitor | A, F | Medium | Medium | Medium | High | Medium | Medium |
| S5. Bad-actor equipment and notification analytics | E | Medium | Medium | Medium | High | Medium | Low (common in other entries) |
| S6. Transportation optimization with CSM and MODI | H | Unknown | Very low | Low | High | Low with current data | High, but only if defensible |

### 9.1 Can a classical transportation model be justified?

No, not from the supplied data. (RECOMMENDATION, based on the OBSERVATIONS below)

A classical transportation model needs every input in the formula below:

```latex
\min \sum_{i=1}^{m} \sum_{j=1}^{n} c_{ij} x_{ij} \quad \text{s.t.} \quad \sum_{j} x_{ij} \le s_i, \quad \sum_{i} x_{ij} \ge d_j, \quad x_{ij} \ge 0
```

Here x is the quantity shipped from source i to destination j, c is the unit transport cost, s is source supply and d is destination demand.

| Model input | What it needs | What the six workbooks hold | Status |
| --- | --- | --- | --- |
| Sources (m) | Several sources able to supply the same item | 124 suppliers, but each material has exactly one | NOT ESTABLISHED for any material |
| Destinations (n) | Two or more demand points | One plant (1000), no storage locations | Fails: n = 1 |
| Supply s(i) | Capacity per source | None | NOT ESTABLISHED |
| Demand d(j) | Demand per destination | Issues per material over 17 months | Available for one destination only |
| Unit cost c(i,j) | Transport cost per unit per route | No locations, no freight cost | NOT ESTABLISHED |
| One commodity or one unit | Shipments that can be added together | 10 units of measure, 1,250 different materials | Fails unless one material at a time |

**Why one destination breaks the method.** With n = 1, the best plan is simply to take each unit from the cheapest source that still has capacity. A starting-solution method such as CSM and an improvement method such as MODI have nothing to improve. The cost table has a single column, so there is no route trade-off to optimise. (Reasoning, standard transportation-model logic)

**About the CSM paper.** The CSM paper is not among the project files I can see, so I cannot state its exact algorithm or assumptions here. I will need it attached before describing CSM in detail.

**When it could become defensible.** Only if the case owner supplies, or we declare as SCENARIO, all of the following:

1. Two or more destinations, for example separate warehouses or plant areas. The location prefixes PX, PY and UT could be area candidates, but no file places stock or cost by area.
2. Groups of interchangeable materials so one item has several sources. The 36 same-description pairs bought from different suppliers are the only data-based starting point, and their equivalence is unconfirmed.
3. Supplier capacity and unit freight cost per route, verified or labelled as scenario values.

If CSM and MODI stay in the pitch, they should appear as a clearly labelled scenario module on top of S1 or S2. They should not be presented as a finding from the data. (RECOMMENDATION)

## 10. Recommended next steps

The next move is a definitions request to the case owner, not code. Everything below is RECOMMENDATION.

- [ ] Confirm which case this dataset belongs to: the diagram says Case 3, Spare Part Intelligence; the project page says Case 2.
- [ ] Send the 14 questions in Section 4 to the case owner, starting with the PR PO duplicate rule, Min/Max meaning, criticality codes and order types.
- [ ] Request the priority 1 and 2 items in Section 8 (receipt date, unit cost, stock date, plan components, failure codes).
- [ ] Attach the CSM paper so its method can be checked against the conditions in Section 9.1.
- [ ] Agree the grain register and duplicate rule as the Stage 0 gate, then approve moving to EDA.
- [ ] Choose two or three solution directions from Section 9 to test in EDA, based on the answers received.
- [ ] Decide whether a transportation scenario stays in scope, given that it would rest on declared assumptions.

The supplier-name screening done earlier in this project is on hold, as you asked. Its result so far (no exact-name matches in a 4-name pilot) is consistent with the case's statement that the data is synthetic.

## Sources

- Data Context & Relationship Diagram.pdf (project file): synthetic data statement, table grains and join keys.
- PR PO.xlsx, Movement Material.xlsx, Notif History.xlsx, Mitem & Mplan.xlsx, BoM.xlsx, FuncLoc list.xlsx (project files): all OBSERVATION counts, inspected read-only on 4 November 2026.
