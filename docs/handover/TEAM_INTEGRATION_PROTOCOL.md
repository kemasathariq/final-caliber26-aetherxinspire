# INSpire Team Integration Protocol

**Status:** DRAFT v0.1. Rules for how the Lead, Atria and Brilian exchange work. Responsibilities: `docs/strategy/TEAM_RESPONSIBILITY_MATRIX.md`. Definitions: `docs/strategy/MASTER_SOLUTION_BLUEPRINT.md`.

## 1. Interfaces

| From | To | Artifact | Format | Gate |
| --- | --- | --- | --- | --- |
| Lead | Atria | Engine output files, `eng_*` | CSV and manifest, contract v0.1 | Lead validation passed |
| Lead | Atria | Sample files in contract format | CSV | Before Atria's first load (to be produced) |
| Lead | Brilian | `eng_scenario_result.csv`, `eng_proposed_parameters.csv`, marts M1 and M2 | CSV | Same |
| Brilian | Lead | Cost set proposals, price assumption rule | One page per set | Lead approval |
| Brilian | Atria | `fin_scenario_grid.csv` | CSV | Lead approval of the cost sets used |
| Atria | Lead | AETHER inventory, persistence proposal, external-service proposal | Short memo | Lead decision D-07, D-08, D-12 |
| Atria | Lead | Build for acceptance walk-through | Deployed or local | Acceptance, `ATRIA_TECHNICAL_HANDOVER.md` section 12 |

## 2. Versioning

- Contract version in `eng_run_manifest.json` (`spec_version`). Current: `0.1`.
- A change to a column name, meaning or enum raises the version and is announced in the change log below before it ships.
- Adding a column is backward compatible. Removing or renaming is not.
- Every run has a `run_id`. The application and the financial grid both record the `run_id` they used. A number is only valid with its `run_id`.

## 3. Change log

| Date | Version | Change | Announced by |
| --- | --- | --- | --- |
| 2026-11-04 | 0.1 | Initial contract | Lead |
| 2026-11-04 | 0.1-A (PROPOSED) | Addendum A: optional `eng_supply_context.csv`, empty `ref_location`, `ref_supplier_site`, `ref_transfer` tables and nullable `location_id`. Not active until D-14 and D-16 are approved | Lead |
| 2026-11-04 | 0.1-B (PROPOSED) | Addendum B: `recommended_action` in `eng_capability_output.csv`, optional `eng_forecast.csv`. Additive. Not active until D-19 and D-23 | Lead |
| 2026-11-04 | Phase 1 lock | Contract v0.1 plus Addenda A and B adopted as the Phase 2 baseline. Additions still PROPOSED until D-19, D-23 and D-16 are signed. Shared definitions frozen. Changes need a Lead entry here | Lead |

## 4. Shared definitions

Single source: `MASTER_SOLUTION_BLUEPRINT.md` section 6 (scenario identifier, terms, tiers). If one workstream needs a new term, it goes to the Lead as a decision. Nobody redefines a term locally.

## 5. Decision flow

1. The proposer writes the decision with ID, options, recommendation and what it blocks.
2. The approver in the decision table (blueprint section 7) answers in one line.
3. The answer is added to `docs/strategy/DECISION_REGISTER.md`, with date. Until then the open state applies.
4. **Shared assumptions, contract columns and metric definitions change only by a Lead entry in the change log above.** Atria and Brilian may propose, never edit.

## 6. Order of work and dependencies

```
Lead: D-01, D-02, D-03 ──► engine R0 ──► stop gate ──► R1/R2, S1/S2, MC runs ──► validation
Atria: schema, loaders, UI shell, assistant (sample files) ──► real load ──► acceptance
Brilian: expenditure, exposure ranges, method note, cost proposals ──► scenario grid ──► evidence
```

Parallel from now: Atria on sample files, Brilian on M1 and M2 only. Serial: real engine output must exist before Atria's real load and Brilian's scenario grid.

## 7. Data handling

- Raw workbooks, marts and engine output are confidential competition data derived from it. They stay out of the public repository.
- No source data or mart goes to an external service, including a language model, without an explicit decision (D-07).
- The repository is shared. Do not reset, clean, or force-push. Commits go through the Lead's review.

## 8. Git

Recommended branches are decided by the Lead. Documentation is committed separately from code. See the commit scope in the final report of this blueprint task.

## 9. Acceptance and sign-off

| Output | Validated by | Evidence |
| --- | --- | --- |
| Engine output | Lead | `VALIDATION_FRAMEWORK.md` section 8 |
| Application | Lead, with Atria's test log | Section 12 of the Atria handover |
| Financial grid | Lead, with Brilian's reconciliation | Section 11 of the Brilian handover |
| Presentation claims | Lead | `SUBMISSION_READINESS_CHECKLIST.md` |

## 10. Defect and conflict handling

A discrepancy between two workstreams' numbers is a defect, not a debate. The two owners compare against the `run_id` and the stored file. If the file is right, the other side fixes. If the definition is unclear, it becomes a new decision ID.
