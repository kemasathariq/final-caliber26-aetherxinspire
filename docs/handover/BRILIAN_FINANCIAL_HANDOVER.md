# INSpire Financial Handover for Brilian

**Status:** DRAFT v0.1. **Owner of this document:** Lead. **Owner of financial calculations:** Brilian. Definitions: `docs/strategy/MASTER_SOLUTION_BLUEPRINT.md` section 6. **No monetary figure is published without Lead approval of its inputs (D-09, D-10).**

## 1. The four quantities, kept apart

| Quantity | Definition | Computable today? | Basis |
| --- | --- | --- | --- |
| Inventory exposure | Recorded stock times a reference unit amount, IDR, under a stated price assumption | **Yes, as an assumption-based range** | M2 `stock`, M1 `implied_unit_amount_scenario` (A-13) |
| Cash tied up in inventory | Book value of stock held | **No.** Needs verified unit price and a dated stock snapshot | DEF-12, DEF-05 |
| Procurement expenditure | Sum of PO-Item Amount per currency and PR PO view | **Yes, as observed amounts of unconfirmed meaning** | M1. IDR 168.84 billion on `original_rows`, 89.21 billion on `exact_distinct_rows` |
| Estimated savings | Difference in total cost between two policies under approved cost assumptions | **No.** Blocked by D-09 | No cost parameters exist |

Never use one of these names for another.

## 2. Financial questions to answer

1. How much inventory exposure do recorded stock levels represent, by tier and by position against recorded Min/Max?
2. How does simulated average on-hand under proposed parameters compare with recorded parameters, in exposure terms?
3. What does procurement spending look like by supplier and material, under both PR PO views?
4. For an approved cost set, how does total scenario cost compare between recorded and proposed policies, and how stable is the ranking?
5. Which assumptions move the answer most?

## 3. Available inputs

| Field | Where | Caveat |
| --- | --- | --- |
| `stock`, `unit`, `min_qty`, `max_qty` | `mart_material_inventory` | Undated, material-level |
| `po_item_amount`, `currency`, `pr_quantity`, `implied_unit_amount_scenario` | `mart_procurement_line__*` | Amount meaning unconfirmed. Implied unit amount is amount divided by PR quantity. The highest value within a material is typically 2.04 times the lowest |
| `implied_unit_amount_scenario_median__{view}` | `mart_material_inventory` | Median of the above, per view |
| `supplier_code`, `n_pr_lines__{view}` | M1, M2 | One supplier per material |
| Mean on-hand, units above Max, orders placed, unmet quantity | `eng_scenario_result.csv` (engine, not yet built) | Simulated or replay, in units |

## 4. Missing financial inputs

Holding cost rate, ordering cost per order, stockout or downtime penalty, confirmed unit price, price tax treatment, goods-receipt values, stock snapshot date, exchange rates with source and date, obsolescence write-down rules.

**Do not invent any of these.** Propose scenario values with a stated source or rationale. The Lead approves each set.

## 5. Scenario definitions

Engine scenario identifier `SC-<D>-<V>-<P>-<S>-<K>` is fixed. You add one part: a cost set `CS-<n>`.

| Cost set | Content |
| --- | --- |
| `CS-0` | No cost. Units only. Always present |
| `CS-1` to `CS-n` | Holding rate (percent of value per year), ordering cost per order, stockout penalty per unmet unit or per shortfall event, all IDR, each with source or rationale and approval status |
| Price assumption `U-` | `U-LOW`, `U-MED`, `U-HIGH` from line-level implied unit amounts per material and view (for example lower quartile, median, upper quartile). State the rule you choose |

Report every number under `SC` and `CS` and `U-` identifiers.

## 6. Calculations

All per material, per scenario ID, in IDR only.

- **Exposure at recorded stock:** `E_rec = stock x u`, with `u` for the chosen `U-` level. Only where the unit amount exists and currency is IDR.
- **Scenario average exposure:** `E_pol = mean_on_hand x u`, from the engine, by policy.
- **Scenario cost:** `holding + ordering + shortfall`, where holding is rate times `E_pol` over the horizon fraction, ordering is cost times `orders_placed`, shortfall is penalty times unmet quantity (or events). Use the approved cost set only.
- **Scenario cost difference:** `Cost_recorded minus Cost_proposed` within the same `SC` and `CS`. Call it "scenario cost difference under assumption set CS-n". It is not a saving.
- **Procurement expenditure:** sum of `po_item_amount` for `currency = IDR`, per view, by supplier, material and month.
- **Rank stability:** share of (scenario, cost set, price level) combinations where proposed cost is lower than recorded cost.

Do not multiply a quantity in one unit by a price of another unit. Do not total quantities across units. Totals of money across materials are acceptable in IDR.

## 7. Currency handling

IDR is the working currency (11,511 original and 6,138 distinct lines). Non-IDR lines (EUR, JPY, SGD, USD: 98 original, 51 distinct) stay in their own currencies and are excluded from IDR totals. A conversion needs a named rate source and date, approved by the Lead. Never present a mixed-currency total.

## 8. Price interpretation uncertainties

- Is PO-Item Amount a line total or a unit price? Net or gross? Tax? (DEF-05)
- Does PR quantity equal ordered quantity? Requests are 7.5 to 9 times issues in large units (A-15).
- Exact copies in PR PO change totals by a factor of 1.89 in IDR. Both views are reported, neither is default.
- The price spread within a material is wide, so any single price is an assumption.

## 9. Sensitivity analysis

At minimum vary: PR PO view, price level `U-`, cost set, demand scenario, opening-stock rule. Report ranges and rank stability. Identify the factor that moves the result most. Do not headline one combination.

## 10. Financial output format

| Output | Format |
| --- | --- |
| `fin_scenario_grid.csv` | Columns: `material_no`, `scenario_id`, `cost_set_id`, `price_level`, `currency` (IDR), `exposure_recorded`, `exposure_policy`, `holding_cost`, `ordering_cost`, `shortfall_cost`, `total_cost`, `cost_difference_vs_recorded`, `assumption_status`, `label` |
| Summary tables | By tier, class, cost set, with ranges |
| Method note | One page: formulas, parameter sources, approval status |
| Label on every table | "Assumption-based scenario result. Source data is synthetic. Not a forecast or a realised saving." |

## 11. Rules

0. No logistics saving, freight rate or transport cost estimate of any kind (section 13).
1. No saving, ROI or payback figure without an approved cost set. Even then, call it a scenario cost difference.
2. Never use unit amounts as comparable costs across materials without resolving DEF-05.
3. Keep `CS-0` rows so units-only results always exist.
4. Cash tied up stays blocked until a verified price and a stock date exist.
5. Anything you propose goes to the Lead as a numbered decision.

## 12. Dependencies

Needs the engine output (Lead) and the cost-set approval path (D-09, D-10). You can start now on procurement expenditure, exposure ranges and the method note, which need only M1 and M2.

## 13. Logistics-related financial information

Scope added by the transportation assessment (`analytics/TRANSPORTATION_AND_DISTRIBUTION_ASSESSMENT.md`). You evaluate; you do not invent.

1. **Review what exists.** Check whether `PO-Item Amount` could include freight or handling (part of D-10). Report only what the data can show: amount level by supplier and currency, non-IDR lines kept in their own currency. Foreign currency is not proof of import.
2. **List missing transportation cost inputs.** Freight and handling per shipment, incoterms, customs and duties, packaging, insurance, expedite surcharge, landed-cost breakdown, supplier and plant locations, vehicle and capacity cost. Return the list with the reason each matters.
3. **Define the future cost-risk requirement.** Describe how a logistics cost component would join the cost sets (`CS-n`) and the scenario grid, which fields it would need, and which approval step applies. Design only, no values.
4. **Rules.** Do not invent freight rates, logistics savings, route costs or transfer costs. Do not include logistics cost in any figure. Do not label procurement expenditure as logistics spend. Anything you propose goes to the Lead as a numbered decision (D-15 covers the data request).

## 14. Official brief inputs for the cost-risk view (2026-11-04)

The brief (p4, p6) names the cost-risk components: inventory carrying and holding cost, procurement cost and replenishment lead time, and **downtime and production loss caused by spare part unavailability**, balanced against inventory cost. The dataset holds none of the cost components except `PO-Item Amount`. Your task is unchanged: define each as a labelled scenario input with a stated source, and invent no value. Add **downtime or production-loss cost per day** to the missing-input list next to the stockout penalty. For the success-metric slide (brief p9), review the metric definitions in `strategy/PROBLEM_STATEMENT.md` section 6 and confirm the exposure metric wording.

## 15. Phase 1 baseline lock (2026-11-04)

Read first: `strategy/PHASE_2_EXECUTION_PLAN.md` (B1 to B4), `strategy/DECISION_REGISTER.md` (D-09, D-10, C-5).

**Start now:** B1 price and amount interpretation memo, B2 exposure ranges from M1 and M2, B4 missing freight input list, and cost-set proposals for B3. **Wait for engine output:** the scenario grid (needs `eng_scenario_result.csv`, which does not exist yet). Cost-risk applies to the 228 Grade A materials only (D-24).

**You may not:** change shared definitions, metric names or contract columns. Raise a change request to the Lead. Show any monetary comparison before D-09. Use PO-Item Amount as a cost until C-5 is answered. Combine currencies. Report savings.
