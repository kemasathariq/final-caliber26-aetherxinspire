# INSpire Solution Architecture

**Status:** Phase 1 BASELINE v1.0 (transportation integrated, official brief audit applied, SQLite and Vercel constraints in section 9). Everything below is PROPOSED except the data foundation (layer 1), which is IMPLEMENTED. Shared definitions are in `MASTER_SOLUTION_BLUEPRINT.md` section 6.

## 1. Six layers as one workflow

```
 L1 Data foundation ──► L2 Context ──► L3 Demand intelligence ──► L4 Inventory optimisation
 (M1-M3, tiers)        (criticality,     (class, abstain,          (R0/R1/R2 vs X policies,
                        notifications,    resample)                 scenarios A/B, views OR/ED)
                        plans)                                           │
                                                                         ▼
        L6 Recommendations + cost-risk scenarios  ◄──  L5 Health and risk monitoring
        (assistant explains, planner decides)          (six capability outputs per material)
```

A material enters at L1 with a tier. L2 attaches context. L3 gives it a demand class and a confidence. L4 simulates. L5 turns results into the six capability outputs. L6 presents them with explanation and a human decision. Each layer writes files the next layer reads, so any number can be traced back.

## 2. Layer responsibilities

| Layer | Purpose | Input | Output | Owner | Status |
| --- | --- | --- | --- | --- | --- |
| L1 | Governed, validated base | Six workbooks | M1, M2, M3 marts, tier table | Lead | IMPLEMENTED (tier table PROPOSED) |
| L2 | Context for explanation, not demand. Includes equipment and maintenance context and **supply context** (supplier, currency, promised interval, spread) | FuncLoc, Notif History, Mitem and Mplan, BoM, PR PO via M1 | Per-material counts of locations by criticality, linked notification counts, plan counts, promised-interval profile | Lead | Criticality counts IMPLEMENTED in M2. Supplier-material interval stats IMPLEMENTED in M1 (display PROPOSED, D-14). Others PROPOSED |
| L3 | Know what kind of demand it is | M3 | Demand class, active months, confidence, eligibility flag | Lead | PROPOSED (D-06) |
| L4 | Compare policies under identical conditions | M1, M2, M3 | Scenario results by `SC-` identifier | Lead | Design IMPLEMENTED, engine PROPOSED |
| L5 | Monitor health and risk | L3, L4, M2 | `rec_capability_output` rows | Lead | PROPOSED |
| L6 | Explain, price scenarios, approve | L5, cost sets | Recommendation records, approvals, explanations | Atria (app), Brilian (cost), Lead (rules) | PROPOSED |

## 3. Data flow and storage

| Stage | Location | Format | Notes |
| --- | --- | --- | --- |
| Raw | `data/raw/` | xlsx | Immutable, git-ignored |
| Conformed and marts | `data/interim/`, `data/processed/` | CSV with metadata JSON | Git-ignored. Confidential competition data |
| Engine output | `data/processed/engine/` (PROPOSED) | CSV plus `run_manifest.json` | Contract in `ATRIA_TECHNICAL_HANDOVER.md` |
| Application database | SQLite file built from engine output | SQLite | Read-only reference tables plus review tables (D-08) |

The application never reads raw workbooks and never recalculates results.

## 4. Capability map

| Capability | Layer | Eligible tiers | Output type | Evidence rule |
| --- | --- | --- | --- | --- |
| Stockout Risk | L4, L5 | T3 | Simulated share of runs with a shortfall, per scenario | Resampling only above thresholds, else deterministic or configurable |
| Overstock Risk | L5 | T3 simulated, T2 and T1 descriptive | Position against recorded Max, simulated days above Max | Descriptive wording outside T3 |
| Reorder Recommendation | L4, L5 | T3 | Reorder point and quantity candidates, trigger state at snapshot | Candidate, needs approval |
| Slow-Moving Alert | L3, L5 | T2, T3 (T1 labelled "no recorded consumption") | Rule-based flag with months since last issue | Descriptive, no cost claim |
| Dynamic Inventory Parameters | L4 | T3 | Proposed s and S by service-level scenario next to recorded Min/Max | Scenario level, not target |
| Cost-Risk Optimisation Scenarios | L4, L6 | T3 | Grid of exposure and shortfall by cost set | Monetary only with approved cost sets (D-09) |

## 5. Technical architecture summary

- **Analytical engine:** Python, single-item daily recursion, no external simulation framework (`SIMULATION_DESIGN_SPECIFICATION.md`). Run offline by the Lead. Output files are versioned and checksummed.
- **Application:** web front end, SQLite, serverless deployment. Specified in `ATRIA_TECHNICAL_HANDOVER.md`.
- **Assistant:** explanation layer over stored records. Specified in the same document.
- **Financial layer:** Brilian's scenario sets applied to engine output, specified in `BRILIAN_FINANCIAL_HANDOVER.md`.

## 6. Why this architecture

- It keeps the unconfirmed parts (Min/Max meaning, lead proxy, costs) as visible scenario inputs, so approval of the brief later changes inputs, not structure.
- It lets Atria build against a fixed file contract before the engine exists.
- It keeps three people from recomputing the same quantity in three places.

## 7. Risks

| Risk | Effect | Mitigation |
| --- | --- | --- |
| Reference policy reading is wrong (C-08) | Results describe a policy nobody uses | Stop gate after R0, R2 alternative, wording |
| Brief differs from assumed requirements (C-01) | Rework in capabilities | Contract is capability-agnostic. Check D-01 first |
| Vercel and confidentiality (C-07) | Cannot deploy real data | Decide D-07. Fallback: deploy with the mock contract data and label it |
| Transportation expectation by the jury | The brief does not mention transportation. The risk is the reverse: the jury sees a solution that drifts from forecasting and inventory | Lead with the brief's four capabilities. Show Level B supply context as "procurement lead time and supply variability" (brief p5, p7) and Level C as one roadmap row |
| Forecasting and recommended action not visible | Brief capabilities 1 and 4 (p4) look unmet | R-16 forecast output and R-17 `recommended_action` (audit X-01, X-03) |
| Thin history | Most output descriptive | Tiers and abstention, stated up front |

## 8. Integrated supply-chain scope and logistics extension points

INSpire is Integrated Spare Part Supply Chain Intelligence (USER-STATED, not OFFICIAL). The architecture covers demand, inventory, procurement and equipment context today. Logistics is an extension, not an MVP module.

| Supply-chain stage | In the architecture now | Evidence level |
| --- | --- | --- |
| Demand | L3 | MVP |
| Stock and policy | L4, L5 | MVP |
| Procurement lead time and supplier context | L2 supply context, L4 lead-time input | Level B, promised dates only |
| Supplier-to-warehouse transport | Not modelled | Level C |
| Warehouse positioning, transfers, emergency distribution | Not modelled | Level C |
| Route and vehicle | Not modelled | Level C |

**Extension points (design only, no logic):**

1. Optional nullable fields `location_id` on stock and engine result rows. An empty value means unknown, never "central store".
2. Reference tables `ref_location`, `ref_supplier_site`, `ref_transfer` created empty so a later data load needs no schema change.
3. A future layer L7 (logistics) would read the same marts plus the new tables, and write files under the same contract with new `capability` values. It would not change L1 to L6 outputs.
4. Contract versioning follows `TEAM_INTEGRATION_PROTOCOL.md`.

**Boundary.** L7 is not built, not stubbed with fake data, and not shown in the demo as a result. Details, data needs and the roadmap: `analytics/TRANSPORTATION_AND_DISTRIBUTION_ASSESSMENT.md`.

## 9. SQLite and Vercel constraints (Phase 1 baseline)

| Constraint | Rule | Basis |
| --- | --- | --- |
| Database | SQLite, one file, built from engine output by Atria's loaders | OFFICIAL, brief p8 |
| Deployment | Working MVP, not static HTML, published to Vercel | OFFICIAL, brief p8 |
| Contents | Derived tables only. No raw workbook rows. No full line-level procurement dump. Sample-labelled rows until D-07 is approved | TEAM default (D-07) |
| Write behaviour | Treat the deployed database as **read-only**. Review actions are kept in the browser session and labelled "not persisted" unless the smoke test proves persistence (D-08) | TEAM default. Vercel documentation retrieved did not confirm filesystem behaviour |
| Size | Bundle limit stated by Vercel for Python functions is 500 MB. The derived database is expected to be far smaller. Check after the build | Vercel docs search, 2026-11-04 |
| Secrets | Environment variables only, none in the zip | Standing rule |
| Assistant | Templated explanation, no external model unless D-07 allows | TEAM default |
| Zip | Complete source and the SQLite file. Excludes `data/raw/`, `.venv`, and anything not approved | OFFICIAL (p8) plus TEAM default |
| Screenshot | After the final deploy, png or jpg with timestamp visible | OFFICIAL, p8 |

Method classes per capability: `MASTER_SOLUTION_BLUEPRINT.md` section 12.2 and 12.3.
