# INSpire Transportation and Distribution Assessment

**Status:** DRAFT v0.1 for Solution Lead approval. **Date:** 2026-11-04. **Owner:** Lead. **Companion to:** `strategy/MASTER_SOLUTION_BLUEPRINT.md` (section 5A), `strategy/ROOT_CAUSE_ANALYSIS.md` (RC8 to RC10), `strategy/SOLUTION_ARCHITECTURE.md` (section 8).

**Official brief check (2026-11-04):** the brief (`CALIBER 2026 - Final Case Brief.pdf`) does not mention transportation, logistics or warehouses. The integrated positioning is the Lead's choice. Supply context is justified by the brief's "procurement lead time and supply variability" (p5) and PR PO "lead time, cost, and supply reliability" (p7). The brief also prefers a justified data architecture over more data (p7), which supports keeping optimisation at Level C. See `strategy/OFFICIAL_CASE_ALIGNMENT_AUDIT.md`.
**Data label:** Source data documented as synthetic. Findings describe the supplied dataset, not Chandra Asri operations.
**Official brief:** Not inspected (D-01). Nothing here is OFFICIAL. The strategic direction (Integrated Spare Part Supply Chain Intelligence, transportation investigated explicitly) is USER-STATED, confirmed by the Lead.

## 1. Summary

1. Transportation was investigated across seven problem areas. **None can be confirmed as an operational fact from the six workbooks.** The files hold no supplier location, no storage location, no origin or destination of any movement, no goods receipt, no transfer, no shipment and no freight cost.
2. The supply network in the data is degenerate: one plant (`1000`), one movement type (`Issue`), one supplier per material (1,250 of 1,250), and a single destination for all purchasing. A transportation or allocation model has nothing to optimise on this structure without invented data.
3. What the data does support is **supply-side context**: promised procurement lead time, its spread, supplier and currency concentration, and the gap between requested and promised dates. This is already in mart M1 (`mart_supplier_material__*`). It is inbound delivery *timing as promised*, not transport.
4. **Recommended positioning:** inbound lead-time variability and supplier context are **Level B, supporting supply-chain intelligence** (descriptive, shown beside the inventory result). Every transportation optimisation method is **Level C, future enhancement**. No transportation optimisation enters the MVP. The MVP stays realistic and the strategic direction stays integrated.
5. The inventory engine already uses procurement lead time as an input (lead-time-proxy demand), so transport-related variability reaches the product through the inventory logic, labelled as promised lead time.

## 2. Evidence labels and rules

OBSERVATION (counted in the supplied files), HYPOTHESIS (plausible, not testable now), ASSUMPTION, PROPOSED. Numbers marked **read-only** were computed for this assessment from the raw workbooks with no file written. They are not validated marts. Rebuilding them as a checked table is proposed as D-16.

## 3. Field-by-field assessment of the six datasets

| Dataset | Field | Business meaning (verified status) | Transport relevance |
| --- | --- | --- | --- |
| PR PO | `PR-Plant` | Single value `1000` on all 11,609 rows (OBSERVATION). Meaning: purchasing plant. Not a storage location | One destination. No inter-plant or inter-warehouse flow is visible |
| PR PO | `PR-Purchasing Group` | 19 groups, MR1 holds 4,980 rows. Meaning of codes unconfirmed (DEF) | Organisational, not geographic |
| PR PO | `PR-Type` | PR01, PR03 to PR06, PR09, PR10. Meaning unconfirmed. Promised intervals differ by type (median PR01 111 days, PR03 37, PR06 40, PR05 90; read-only) | Cannot be called "emergency" or "standard" without definitions |
| PR PO | `PO-Supplier Code`, `PO-Supplier Name` | 124 suppliers. Exactly one supplier per material. Median 6 materials per supplier | Supplier identity only. No address, country or coordinates |
| PR PO | `PR-Date` | Requisition date (2025-05-04 to 2026-09-22) | Start of the procurement clock |
| PR PO | `PR-Delivery Date` | Requested delivery date (meaning per data specification). 630 rows precede the PR date. 764 fall after 2027-01-01. Range 2023-12-21 to 2029-03-09 | Not an actual delivery. Implausible values exist |
| PR PO | `PO-Delivery Date` | Promised delivery date. 6 rows precede the PR date, 429 fall after 2027-01-01 | Promised only. This is the only supply-side time signal |
| PR PO | `PO-Currency` | IDR on 11,511 rows. JPY 41, USD 35, EUR 20, SGD 2 across 6 suppliers | Currency hints at foreign billing, not at origin or route. Do not infer location |
| PR PO | `PO-Item Amount` | Amount of unconfirmed meaning (D-10) | No freight component is identifiable |
| Movement Material | `Movement Type` | Only `Issue` (17,518 of 17,518) | No receipt, no transfer, no return. Not a physical route |
| Movement Material | `Posting Date`, `Order` | Issue date and work order | Consumption timing only |
| Movement Material | Origin, destination, storage location | **Absent** | No route can be derived |
| FuncLoc list | `Functional Location` | Technical hierarchy, 14,484 rows. Codes start PX, PY, UT, SITE | Equipment structure, not a logistics network |
| FuncLoc list | `SITE_PY_2200` "WAREHOUSE", `SITE_PY_2000` "JETTY", `SITE_PY_1900` "TANK FARM", `SITE_PY_0900` "OFFSITE & TANKAGE" | Area-level functional locations. Nothing links stock or movements to them. Whether the WAREHOUSE row is a store is unconfirmed | Possible candidates for a future location master. Not a storage location today |
| BoM | `Functional Loc.` | 4,516 locations, all found in FuncLoc list | Where a part is installed. It identifies demand points for context, not delivery destinations |
| BoM | `Stock`, `MRP Type` | One stock figure per material (repeated on each location row), undated, no storage location | Stock cannot be split by location |
| Notif History | `Functional Location`, `Priority` (Emergency 135, all type N2), `Order` | Where work was requested and its urgency. Only 20.5 percent of Movement orders match | Weak link from work location to a material issue |
| Mitem & Mplan | Maintenance plan and item | Planned maintenance by location | Possible future demand-timing input, not logistics |

**Rule recorded for all teams:** a `Movement Material` row is a stock issue to a work order. It is **not** a physical transport leg. A goods issue does not tell where a part was stored or where it was taken. No document may draw a route from movement data.

## 4. Problem-by-problem assessment

Columns: **C** = confirmed evidence (OBSERVATION), **PRC** = potential root cause, **H** = hypothesis requiring validation, **D** = additional data required.

### 4.1 Supplier-to-warehouse delivery

- **C.** Promised interval from PR date to PO delivery date, on 11,603 rows with a non-negative value (read-only): p10 15 days, median 42, p90 155, p99 464, coefficient of variation 1.23. Median supplier-level CV is 0.66 over 114 suppliers with at least 10 lines. Foreign-currency lines have a median of 151.5 days against 42 for IDR (98 rows, 6 suppliers). Top five suppliers hold 27.1 percent of rows. 46.7 percent of rows are exact copies (DEF-01), so volumes depend on the PR PO view.
- **PRC.** Long and widely spread promised intervals are consistent with supplier lead time, approval or processing time, or shipping time. The data cannot separate them.
- **H.** Foreign sourcing lengthens inbound lead time. Supported only as a pattern on 98 rows from six suppliers. Currency is not origin.
- **D.** Actual goods-receipt date, PO creation date, shipment date, supplier country and address, incoterms.

### 4.2 Warehouse-to-warehouse transfers

- **C.** None. One plant, one issue movement type, no transfer movement, no storage location.
- **PRC.** Not assessable.
- **H.** Parts may be held in more than one store and balanced by transfers. Nothing in the files supports or contradicts this.
- **D.** Warehouse and storage-location master, stock by location with date, transfer movements with origin and destination.

### 4.3 Warehouse-to-maintenance-location distribution

- **C.** BoM links materials to functional locations (4,516 locations). Notifications and orders link some issues to locations (20.5 percent of orders). No delivery time from store to work site exists.
- **PRC.** Weak linkage (RC3) limits any location-level demand picture.
- **H.** Distance or handling time from the store to the work site contributes to delay. Untestable.
- **D.** Coordinates or zone of store and work sites, delivery or pick timestamps, request-to-issue timing.

### 4.4 Emergency spare part transfers

- **C.** 135 Emergency notifications, all type N2 (134 distinct orders). Only 8 of these orders have any material issue. Where linked, the issue posted a median of 1 day after the notification date against 6 to 7 days for Low, Medium and High (19 Emergency issue lines, read-only, very small sample).
- **PRC.** Emergency work may draw on parts that are not recorded as issued, or emergency work may be recorded without parts.
- **H.** Emergency demand is served by faster or alternative routes. The data has no transfer or expedite field. PR-Type differences (section 3) cannot be labelled as emergency without definitions.
- **D.** Definition of PR types and notification types, expedite flag, emergency transfer log, requested-versus-actual delivery time for urgent items.

### 4.5 Transportation lead-time variability

- **C.** As in 4.1, only as promised procurement interval. The gap between promised and requested delivery date has a median of 3 days and a 25 to 75 percent range of -4 to 14 days (read-only), but 630 rows have a requested date before the PR date, so the requested date is itself unreliable.
- **PRC.** Variability may come from supplier performance, order approval, or transit. Not separable.
- **H.** Transit is a material share of the variability. Untestable.
- **D.** Actual receipt dates, shipment dates, carrier and mode.
- **Use in product (Level B):** the inventory engine uses promised interval as lead-time proxy and shows its spread. Label it **promised procurement interval, not transport time**.

### 4.6 Logistics cost and delivery constraints

- **C.** None. No freight, handling, customs, packaging or insurance field. No capacity, vehicle or delivery-window constraint.
- **PRC.** Not assessable. `PO-Item Amount` may or may not include freight (D-10).
- **H.** Freight is a relevant part of total landed cost for foreign items. Untestable.
- **D.** Freight and handling cost per shipment, incoterms, landed-cost breakdown.

### 4.7 Inventory positioning and multi-location allocation

- **C.** None for allocation. Stock is one undated figure per material, 1,683 Non Stock materials hold stock, no location split.
- **PRC.** Not assessable.
- **H.** Positioning parts closer to high-criticality locations would reduce delay. The data has no location of stock and no delivery time.
- **D.** Stock by storage location with date, location master, criticality ranking (DEF-03), delivery time between locations.
- **Note:** the existing criticality counts per material (M2) are context for *where a part is used*. They do not say where it is stored.

## 5. Optimisation feasibility matrix

Level: A core MVP, B supporting intelligence, C future. "MVP feasibility" is the recommended answer.

| Method | Business objective | Required inputs | Available inputs | Missing inputs | Assumptions needed | Validation requirement | MVP feasibility | Future potential |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Transportation cost optimisation | Lower total freight cost for given demand | Unit freight cost per route, sources, destinations, capacities | Supplier codes, single destination | Everything except supplier code | Would require invented costs | Back-test against actual freight invoices | **Not feasible (C)** | High once freight and location data exist |
| Multi-warehouse inventory allocation | Place stock where service is needed at lowest cost | Stock by location, demand by location, location costs, delivery times | Material-level stock, BoM locations (installation only) | Storage locations, stock per location, demand per location | Would require invented split | Held-out replay by location | **Not feasible (C)** | High; extends inventory engine to multi-echelon |
| Inter-warehouse transfer optimisation | Rebalance stock to avoid shortage and excess | Two or more stocked locations, transfer times, costs | None | Locations, transfer history, costs | Would require invented network | Replay of historical transfers | **Not feasible (C)** | Medium to high |
| Emergency spare part distribution | Shortest response for urgent need | Emergency definition, stock by location, routes, response times | Emergency notification flag (135), PR types (undefined) | Definitions, expedite log, locations, response times | Emergency means N2 priority only if confirmed | Compare with logged response | **Descriptive context only (B)**: count emergency notifications and linked issues, with small-sample warning. No optimisation | Medium |
| Supplier-to-warehouse delivery optimisation | Shorter or more reliable inbound delivery | Supplier alternatives, actual lead times, cost, location | Promised lead time per supplier-material, one supplier per material | Alternatives, actual receipts, cost | Promised equals expected actual (weak) | Actual versus promised back-test | **Supporting intelligence (B)**: promised interval and spread, supplier concentration. No supplier selection, because each material has one supplier | High once receipts exist |
| Route and vehicle optimisation | Efficient routing | Coordinates, distances, vehicle capacity, time windows, load | None | All | Would require invented routes and distances | Compare with operations | **Not feasible (C)** | Low priority; only if the owner runs own fleet |

## 6. Recommended positioning

| Level | Capability | Content | Status |
| --- | --- | --- | --- |
| **A. Core MVP** | None specific to transportation | Inbound lead time already enters the inventory engine as a stated input with its uncertainty | Existing design, no new scope |
| **B. Supporting intelligence** | **Supply context** panel and **inbound lead-time variability** view | Per material: supplier, currency, promised interval (median, p75, p90), requested-versus-promised gap, line counts under both PR PO views. Shown beside the reorder recommendation. Optional descriptive emergency-notification count | PROPOSED, built only from existing M1 and M2 columns |
| **C. Future enhancement** | All transportation, allocation, transfer, emergency routing and vehicle methods | Roadmap in section 8 | Requires data in section 7 |

**Positioning sentence for the narrative:** "INSpire is an integrated spare-part supply-chain tool. Today it links demand, inventory policy and procurement lead time. It is built so that storage-location, receipt and freight data can extend it to allocation and transfer decisions. We did not model transportation because the supplied data cannot support it, and we state what is missing."

**What this does not change.** Capabilities 1 to 6, the engine, tiers, scenario grammar and the staged stop after R0 are unchanged. No contradiction with `INVENTORY_OPTIMISATION_METHODOLOGY.md` or `DEMAND_INTELLIGENCE_METHODOLOGY.md`: promised interval was already the lead-time proxy (the limits are in `VALIDATION_FRAMEWORK.md`).

## 7. Additional data required

| Data source | Why it matters | Enables |
| --- | --- | --- |
| Warehouse and storage-location master with coordinates | Defines nodes and stock positions | Allocation, transfers, positioning |
| Supplier master with address, country and coordinates | Separates domestic from foreign and gives distance | Inbound analysis, route cost, supplier risk |
| Plant and maintenance-location coordinates or zones | Defines destinations and response distance | Distribution, emergency response |
| Actual goods-receipt timestamps | Turns promised into achieved lead time. The most valuable single addition | Lead-time variability, service-level validation, supplier performance |
| Shipment and delivery history (ship date, mode, carrier) | Splits supplier time from transit time | Transit variability, supplier-to-warehouse optimisation |
| Inter-location transfer history | Shows actual rebalancing | Transfer optimisation, replay validation |
| Transportation and landed costs | Gives c(i,j) for a cost model | Cost optimisation, cost-risk scenarios |
| Vehicle and capacity constraints | Gives feasibility limits | Route and vehicle optimisation |
| Service-level and emergency delivery requirements | Defines targets and urgency | Emergency distribution, criticality-weighted service |
| Dated stock by storage location | Gives starting position per node | All allocation methods, cash tied up |
| Definitions of PR-Type, Purchasing Group, notification types | Gives meaning to urgency and process | Emergency labelling, procurement intelligence |

## 8. Future enhancement roadmap

| Phase | Trigger | Content | Owner |
| --- | --- | --- | --- |
| F0 (now, MVP) | None | Supply context panel and promised-interval view (Level B). Extension points in the schema | Atria builds, Lead defines |
| F1 | Goods-receipt dates supplied | Replace promised with actual lead time. Re-run validation. Supplier reliability view | Lead, Atria |
| F2 | Location master and dated stock by location | Multi-location stock view and allocation scenarios. Engine gains a location dimension | Lead, Atria |
| F3 | Transfer history and transfer times | Transfer recommendations validated by replay | Lead |
| F4 | Freight and landed costs | Cost-risk scenarios include logistics. Brilian extends cost sets | Brilian, Lead |
| F5 | Fleet, capacity, coordinates | Route and vehicle optimisation, only if the case owner needs it | Lead |

## 9. Ownership

| Role | Responsibility for transportation |
| --- | --- |
| Lead | Frames transport inside the overall problem. Approves positioning (D-14). Defines future requirements and the data request (D-15). Owns validation |
| Atria | Builds the supply context panel from existing mart fields if D-14 is approved. Defines extension points (optional `location_id` fields, empty tables). **Builds no routing or transport optimisation** |
| Brilian | Reviews available procurement and logistics-related financial information. Lists missing freight inputs. Defines how logistics cost would join the cost sets. **Invents no logistics savings and no freight rate** |

## 10. Decisions for the Lead

| ID | Decision | Approver | Blocks |
| --- | --- | --- | --- |
| D-14 | Approve positioning: supply context Level B, all transport optimisation Level C | Lead | Atria module M-J, narrative wording |
| D-15 | Send the logistics data request (section 7) to the case owner and decide whether answers can arrive before submission | Lead | Any move of a method from C to B or A |
| D-16 | Build a checked mart (M5) for promised lead-time profile, requested-versus-promised gap and supplier concentration, replacing the read-only numbers here | Lead | Showing these figures in the product as validated |
| D-17 | Whether a clearly labelled hypothetical network scenario is allowed in the narrative at all. Recommendation: **no**, because it would require invented routes and costs | Lead | None |

## 11. What cannot be claimed

- That transportation, delivery or distribution is a confirmed cause of any stock problem.
- Any transport lead time, cost, route, distance or saving.
- That any movement, plant or functional-location field represents a route or a warehouse.
- That foreign-currency lines are imports.
- That a supplier is unreliable. Only promised dates exist.
- That emergency demand is served differently from other demand.
