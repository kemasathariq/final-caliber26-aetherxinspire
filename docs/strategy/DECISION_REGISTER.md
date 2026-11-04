# INSpire Decision Register

**Status:** Phase 1 baseline, 2026-11-04. Single register for decisions D-01 to D-25 and external clarifications C-1 to C-6. It replaces the scattered tables; `MASTER_SOLUTION_BLUEPRINT.md` section 7 now points here. **Only the Lead closes a decision marked APPROVAL.** "Baseline default" means the Phase 2 documents assume it, and Phase 2 work that depends on it carries the risk of reversal.

Classes: **EVID** evidence-resolvable. **DEFAULT** safe default recommended. **APPROVAL** human approval required. **EXTERNAL** needs a clarification from the case owner or organisers.

| ID | Decision | Class | Resolution or baseline default | State | Blocks |
| --- | --- | --- | --- | --- | --- |
| D-01 | Official brief | EVID | Closed. `CALIBER 2026 - Final Case Brief.pdf`, 10 pages, inspected twice | CLOSED | none |
| D-02 | Reference policy R1 (Min as reorder point, Max as order-up-to), R2 as alternative | DEFAULT + EXTERNAL (C-2) | Data cannot settle it. 398 of 665 conflict with the R1 reading. Use R1 with R2 sensitivity and the label "reading, unverified" | APPROVAL | Engine |
| D-03 | Evidence thresholds, 6 active months, 10 lead observations | DEFAULT | Keep. Counts stable from 3 to 12 months (118 to 140 joint) | APPROVAL | Tier labels |
| D-04 | Staged engine, stop after R0 | APPROVAL | Time conflict: 12 hours remain. Default: keep the gate but make R0 review a 15-minute check, not a stage | APPROVAL | R1 and later |
| D-05 | Service-level scenarios 90, 95, 98 percent as scenario levels | DEFAULT | Scenario levels, never targets | APPROVAL | X policies |
| D-06 | Validated demand classification (M4) | DEFAULT | Produce as `eng_material_tier.csv` with checks, instead of a separate mart, to save time | APPROVAL | Class display |
| D-07 | Whether derived data may go into the zip and a Vercel deployment, and whether any content goes to an external LLM | APPROVAL + EXTERNAL (C-1) | See section 2 | **BLOCKER** | Real-data deploy, zip content, assistant |
| D-08 | Persistence on Vercel | EVID (requirement) + DEFAULT | Brief requires SQLite only (p8), not write persistence. Approval workflow persistence is a TEAM feature (R-11). Default: bundled read-only SQLite, review actions in browser session, labelled "not persisted". Vercel documentation retrieved today did not confirm filesystem behaviour. Atria proves it with a smoke deploy of sample data | DEFAULT | R-11 durability |
| D-09 | Cost scenario sets | APPROVAL (Brilian proposes) | No value until approved | APPROVAL | Any monetary output |
| D-10 | Meaning of PO-Item Amount, unit amount rule | EXTERNAL (C-5) + APPROVAL | Exposure labelled "reference unit amount, unverified" | APPROVAL | Exposure |
| D-11 | No default scenario or view in the UI | DEFAULT | Already a standing rule. Adopted | ADOPTED | UX |
| D-12 | AETHER component inventory | APPROVAL (Atria memo) | Not in this repository. Build standalone until supplied | OPEN | Reuse |
| D-13 | Engine built by the Lead, consumed by Atria through files | EVID | Matches the ownership boundaries in the Phase 1 instruction (Lead: methodology and validation, Atria: implementation) | ADOPTED | none |
| D-14 | Supply context Level B, all transport optimisation Level C | EVID | Phase 1 instruction: keep supplier and procurement context in scope, transport optimisation as future enhancement | CLOSED | none |
| D-15 | Logistics data request to case owner | EXTERNAL (C-6) | Non-blocking | OPEN | Level C only |
| D-16 | Checked mart M5 for promised lead-time profile | DEFAULT | Emit as `eng_supply_context.csv` with checks, not a new mart | APPROVAL | Showing supply context as validated |
| D-17 | Hypothetical network scenario in narrative | DEFAULT | No | ADOPTED | none |
| D-18 | Accept the official brief and audit status changes | EVID | Audit verified against the PDF in Phase 1. Audit errors corrected in section 4 | CLOSED | none |
| D-19 | `recommended_action` field | EVID (need, p4) + DEFAULT (encoding) | Adopt REORDER, HOLD, REDUCE, MONITOR, NO_ACTION_EVIDENCE. HOLD stands for "maintain" | ADOPTED, sign-off | Contract |
| D-20 | Deck numbering, slide 6 missing | DEFAULT + EXTERNAL (C-4) | Six content slides in order, with a one-line note. Ask organisers only if a channel exists | ADOPTED | Deck |
| D-21 | "Potentially obsolete candidate", "non-moving by recorded issues" wording | EVID (p4, p6) + DEFAULT | Adopt as hypothesis wording. "Obsolete" and "dead stock" stay forbidden as plain claims | ADOPTED, sign-off | Capability 3 |
| D-22 | How the deck describes AI | DEFAULT | Use the method classification in blueprint section 12.3 | APPROVAL (wording) | Deck |
| D-23 | Forecast output R-16 and stock-level what-if in engine scope | EVID (need, p4, p6) + APPROVAL (time) | Needed by the brief. Scope and time are your call. Minimum: forecast range for 296 materials, what-if as Min and Max scaled by 0.5 and 1.5 | APPROVAL | R-16, OB-20 |
| D-24 | Which materials get proposed parameters: 228 or 665 | DEFAULT | 228 (Grade A). Section 3 of `FIGURE_AND_METHOD_RECONCILIATION.md` | APPROVAL | Capability 2 scope |
| D-25 | Rule table for `recommended_action` | DEFAULT | Blueprint section 12.2. Thresholds configurable and unset | APPROVAL | R-17 |

## 2. D-07 and D-08 in detail

**What the official brief says (p7, p8):** baseline data comes from a link given to participants. Extra data allowed with justification. The submission must include "Complete source code and database in .zip file" and the MVP must be "published to Vercel". It says nothing on confidentiality, data publication, licence or intellectual property. The Data Context diagram (p1, p2) says the data is synthetic (dummy) and "mirrors the structure and relationships of the original system data, not its actual values". The "submissions become corporate property" text exists only in the Case 2 pack, which is not the Case 3 brief.

**What is established**

| Question | Answer | Evidence |
| --- | --- | --- |
| Must the zip contain the database? | Yes | Brief p8 |
| Must the zip contain the raw workbooks? | **Not stated.** "Complete source code and database" most plausibly means the SQLite database the app uses plus code. Raw `.xlsx` are not required by the wording | Brief p8 |
| Is publishing derived data to Vercel permitted? | **Not stated either way** | Brief silent |
| Does Vercel support the stack? | A bundled SQLite file read by a function is a normal pattern. Retrieved Vercel documentation covered function bundles (500 MB limit stated for Python) but **not** write persistence | Vercel docs search, today |
| Is private GitHub or Vercel approved for the data? | **Not established** | Nobody has approved it |

**Decision.** Blocker until you answer. **Safest viable alternative (baseline default):**

1. Raw workbooks never leave your machine and never enter the zip.
2. The SQLite database holds only tables derived by our pipeline and engine, and only fields the app displays. No raw row dumps (for example no full PR PO line table).
3. Before real data is approved, deploy and demo with **clearly labelled illustrative sample rows** in the same schema.
4. The assistant uses templated explanations from stored facts, with no external model (Atria handover section 7 baseline).
5. Add a banner "synthetic dataset" on every page, as the Data Context diagram states.
6. Switch to real derived data only after your written decision, recorded in this register.

Because the brief mandates the DB in the zip and a public prototype, refusing all derived data would make the team ineligible. The residual question is whether synthetic-data-derived tables may be public. The data is documented dummy, which lowers but does not remove the risk. Ask the organisers (C-1) if a channel exists.

**D-08 acceptance test for Atria:** deploy a sample-data build to Vercel, perform a write, reload on a cold function, and record whether it persisted. Keep the default if it does not.

## 3. External clarifications

| ID | Question | Why it matters | Blocks |
| --- | --- | --- | --- |
| C-1 | May tables derived from the supplied synthetic dataset be included in the zip, deployed to a public Vercel URL, and shown in the deck? Is any intellectual property or confidentiality term attached to the dataset or submissions? | The brief is silent. Determines D-07 | Real-data deploy |
| C-2 | What do BoM `Min.Qty` and `Max.Qty` mean (reorder level, order-up-to, safety stock)? Is the stock figure dated, and when? | Decides D-02 and every recommended parameter | Engine credibility |
| C-3 | Internal question: what is "independent-start" comparison? Not found in the repository | Possibly a design not documented | Engine design |
| C-4 | Brief p9 lists slides 1 to 5 and 7. Is slide 6 missing, or a numbering slip? | Deck compliance | Deck |
| C-5 | What does `PO-Item Amount` represent (line total, unit price, per base unit)? Currency basis? | Exposure, any financial scenario | Brilian |
| C-6 | Are warehouse, supplier location, receipt and freight data available? | Moves Level C methods | Level C |
| C-7 | Time zone of the 2026-11-05 06:00 deadline and the submission link | Eligibility | Submission |

## 4. Audit corrections found during verification

| Audit statement | Finding | Action |
| --- | --- | --- |
| "Forecasts for 296 of 1,930 materials" (X-01) | Correct for forecast. Parameters only for 228 in T3 under the demand methodology | D-24 |
| "Blueprint calls R-01 to R-03 USER-STATED, now OFFICIAL" (X-11) | Correct. R-03 says Vercel, R-02 SQLite (p8) | none |
| "Obsolete wording conflict" (X-02) | Correct | D-21 |
| "6 of 39 fully covered" | Count holds. OB-14 depends on D-24 for T3 grade B | footnote only |
| Audit omitted the 228 versus 665 contradiction | New finding | D-24 |
| Audit omitted the name collision of tier labels | New finding | Reconciliation section 2 |
| Audit said brief silent on confidentiality | Verified, brief has no such term | none |
