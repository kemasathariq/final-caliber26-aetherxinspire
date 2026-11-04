# CALIBER 2026, Master Reference, Case 2, Intelligent Manufacturing Dashboard

**Prepared from the three uploaded CALIBER 2026 source documents.**

- `CALIBER2026_Case2_TeamBriefing.docx`
- `The Case - CALIBER 2026.pdf`
- `Booklet CALIBER 2026 - Registration Extended.pdf`

## Purpose

This Markdown is a comprehensive, structured reference for the CALIBER 2026 Case 2 work. It preserves the substantive information contained in the uploaded documents, including competition requirements, Case 1 and Case 2 descriptions, Case 2 key questions, submission requirements, evaluation criteria, timelines, dataset architecture, dataset glossaries, coded-field legends, five hero cases, quantitative insights, limitations, team work plan, rules, FAQ, prizes, registration information, contacts, and source-file inventory.

Where the uploaded material distinguishes **facts** from **interpretations or hypotheses**, that distinction is preserved. Where a source does not provide enough information, this document does not fill the gap with assumptions.

---

## 1. Quick Reference

### Competition

- Competition: **CALIBER, Chandra Asri Limitless Innovation and Business Strategy Challenge 2026**.
- Organizer: **Chandra Asri Group, PT Chandra Asri Pacific Tbk**.
- Grand theme: **“Future-Ready Operational Excellence: Knowledge, Reliability, and Smart Manufacturing.”**
- Eligible participants: active undergraduate, S1, or vocational, diploma, students during the competition period, subject to the booklet rules.
- Competition stages:
  1. Preliminary Stage, Business Proposal Submission.
  2. Final Stage, 2-day Hackathon.
- Preliminary Stage: select exactly one of the two use cases.
- Final Stage: the top 10 Preliminary Stage teams receive a new and entirely different use case and have 24 hours to develop a solution before pitching the following day.
- Final event: **4–5 November 2026, Jakarta**.
- Preliminary proposal deadline: **4 October 2026, 23:59 WIB**.
- All submitted materials and pitching must be in English.
- Preliminary Stage has three required deliverables, with a combined maximum size of **10 MB**.

### Team-selected use case

**Case 2, Manufacturing Intelligence, Intelligent Manufacturing Dashboard**

Scope wording used across the documents:
- Unified Dashboard.
- AI Insight.
- Root Cause Analysis support.
- Follow-up Action Recommendation.
- Single Pane of Glass.
- Alert Prioritization.
- Similar-Incident Retrieval.
- Action Tracking.

### Case 2 core problem

Manufacturing performance information is fragmented across multiple dashboards, systems, reports, KPI definitions, data formats, and reporting schedules. This makes it harder to:
- monitor plant performance,
- identify probable root causes,
- prioritize alerts,
- recommend corrective actions,
- track follow-up actions and ownership,
- make decisions quickly and proactively.

### Committee-envisioned solution

The expected direction is one governed platform that:
1. Connects manufacturing data.
2. Provides a Single Pane of Glass.
3. Displays critical KPIs.
4. Detects or highlights operational problems.
5. Provides AI Root-Cause Indication.
6. Prioritizes alerts according to impact and urgency.
7. Retrieves similar historical incidents.
8. Converts recommendations into owned, trackable actions.

### Five Case 2 data groups and design layer

1. **Incident Database**, fleet-wide incident history.
2. **Equipment Performance**, weekly equipment condition and reliability KPIs for five hero assets.
3. **Production Data**, hourly operational and sensor signals for five hero assets.
4. **RCA & CAPA/PAA**, five verified incident investigations and action plans.
5. **Alert & Action Tracking**, a solution layer to be designed by combining the preceding data sources.

### Five hero assets

- PU-2101B, Mechanical Seal Leakage.
- KO-3201, High Radial Vibration Trip, bearing distress.
- PM-4405B, Motor Bearing Failure, overheating.
- HE-3301, High Fouling, duty loss and high dP.
- BL-5702, High Vibration, coupling misalignment.

### Important data boundary

The project contains detailed, granular time-series and weekly condition data for the five hero assets. The Incident Database covers **380 incidents across 12 plants**, but at summary level. The uploaded Team Briefing explicitly states that no energy or emissions dataset was found in the project, and that the five hero assets should therefore be treated as the prototype proof of concept unless additional justified data is introduced.

---

## 2. Case 2 Mandatory Questions

The official Case Book requires all three questions to be addressed in the proposed solution or business impact section.

### Question 1, governed data foundation

**How can the Company rationalize fragmented dashboards and map manufacturing data sources into one governed data foundation?**

Main focus:
- Reduce dashboard redundancy.
- Create consistent KPI and data mapping across functions.

Key capability:
- Data Source Mapping.

### Question 2, executive visibility

**How can the Company build a single pane of glass that provides executive visibility of manufacturing performance?**

Main focus:
- Provide one integrated dashboard to monitor operational performance.

Key capability:
- Executive Level Dashboard.

Use cases explicitly listed:
- Energy Forecasting.
- Similar-Incident Retrieval.
- AI-based Root Cause Indication.

### Question 3, AI-to-action workflow

**How can AI help identify probable root causes behind operational problems and translate insights into prioritized follow-up actions with clear ownership and tracking?**

Main focus:
- Support faster problem-solving by connecting issue detection, prioritized alerts, and recommended actions.

Key capabilities:
- Problem Tank.
- Root Cause Indication.
- Alert Prioritization Engine.
- Action Tracking.
- Action Guidance.

---

## 3. Preliminary Stage Deliverables

The Registration Booklet requires three materials:

1. **Solution mock-up or prototype**
   - May be provided through Figma.
   - May be accessible HTML.
   - May use another equivalent format that lets the Committee understand and navigate the proposed result.

2. **3-minute demo video**
   - Explains and demonstrates how the proposed solution works.

3. **Presentation deck in PDF**
   - Maximum 7 slides.
   - Cover slide is included in the seven.
   - Appendix slides are excluded from the seven-slide limit.
   - Must follow the required deck structure.

All three materials must be in English.

For the Preliminary Stage, the three materials combined must not exceed **10 MB**.

Non-compliance with the stated submission guidelines directly affects the evaluation outcome.

---

## 4. Mandatory Seven-Slide Deck Structure

### Slide 1, Cover
Identify:
- Team name.
- Chosen use case.

### Slide 2, Background & Problem Statement
Explain:
- Current challenges.
- Supporting facts.
- Why the problem is important to solve.

### Slide 3, Solution
Present:
- High-level objective.
- Workflow.
- Key technologies.

### Slide 4, Business Impact
Demonstrate:
- Expected evaluation or effect.
- Measurable benefits.
- KPIs.
- Success metrics.

### Slide 5, Feasibility & Roadmap
Cover:
- Technical feasibility.
- Operational feasibility.
- Legal considerations.
- Cybersecurity.
- Data governance.
- Organizational readiness.
- Implementation roadmap.
- Timeline.

### Slide 6, Conclusion
Summarize:
- Proposed solution.
- Key value.
- Expected outcomes.

### Slide 7, Team Profile
Provide:
- Team name.
- University.
- Supervisor's name.
- Each member's study program or major.
- Semester enrolled.
- Area of expertise.
- Contribution to the proposal.

The booklet's example table uses:
`No. | Name | Major | Semester | Area of expertise | Contribution`.

### Appendix
- Unlimited appendix slides.
- Include only highly relevant supporting material that strengthens the proposal and provides additional evidence.

---

## 5. Evaluation Criteria

### 5.1 Problem Understanding & Business Impact
The Committee considers:
- Clarity of problem understanding.
- Identification of impacted users.
- Articulation of pain points.
- Expected benefits.
- KPIs.
- Success metrics.
- Measurable business value supported by data or evidence.

### 5.2 Solution Design & Prototype Quality
The Committee considers:
- Logical workflow.
- User journey.
- Expected output.
- UX clarity.
- Prototype completeness.
- Relevance, strength, and novelty of technology use, if applicable.

### 5.3 Presentation Quality
The Committee considers:
- Presentation structure.
- Visual clarity.
- Storytelling flow.
- Demo-video pacing.
- Narration.
- Ability to communicate the solution effectively within 3 minutes.

### 5.4 Feasibility & Roadmap
The Committee considers:
- Realistic implementation plan.
- Technical considerations.
- Operational considerations.
- Legal considerations.
- Cybersecurity.
- Organizational readiness.

### 5.5 Chemical Domain Relevance
The proposal should fit:
- Real chemical-industry needs.
- The selected case context.

---

## 6. Official Competition Timeline

| Event | Date |
|---|---|
| Open Registration | 10 August 2026 |
| Registration closing, extended | 17 September 2026 |
| Preliminary Proposal Submission | 4 October 2026, 23:59 WIB |
| Best Proposal Announcement | 23 October 2026 |
| Final Presentation and Winner Announcement | 4–5 November 2026, Jakarta |

The Team Briefing separately records the same operational milestones and states that internal team and supervisor review should be completed before the proposal deadline.

---

## 7. Company and Theme Context

The Case Book describes PT Chandra Asri Pacific Tbk, Chandra Asri Group, as an energy, chemical, and infrastructure solutions company in Southeast Asia operating complex, asset-intensive petrochemical facilities.

The documents emphasize reliance on:
- technical knowledge,
- equipment reliability,
- supply-chain readiness,
- efficient resource utilization,
- safe and continuous operations.

The digital-transformation direction is described as integrating:
- data,
- analytics,
- artificial intelligence,
into manufacturing processes.

The stated purposes include:
- faster decision-making,
- improved operational visibility,
- preservation of critical plant knowledge,
- stronger collaboration across functions.

The Registration Booklet describes Chandra Asri Group as operating integrated regional platforms based in Indonesia and Singapore. It states that Indonesian assets include the first and largest integrated petrochemical complex in Indonesia, the upcoming Chlor-Alkali and Ethylene Dichloride plant, and infrastructure solutions covering electricity, water, logistics, ports, and storage. Facilities on Pulau Bukom and Pulau Jurong serve as integrated petrochemical and refining production hubs in Singapore.

---

## 8. Case 1, Reference Only

The competition permits only one selected use case. The team-selected case is Case 2, so Case 1 should not be combined into the proposed solution.

### Case 1 title

**Manufacturing Knowledge Hub, AI-Powered Knowledge Integration**

### Case 1 topic

The case focuses on reducing improper execution risk caused by:
- scattered knowledge sources,
- missing tacit knowledge,
- difficulty finding trusted information,
- disconnected operational data.

### Case 1 background

Engineers need quick and accurate decisions during:
- start-up,
- troubleshooting,
- maintenance,
- abnormal operating conditions.

Relevant information can be spread across:
- SOPs,
- datasheets,
- P&IDs,
- maintenance logs,
- real-time operating data.

Because the sources are disconnected, engineers may spend time searching for trusted information or asking experienced personnel for confirmation. Missing tacit knowledge, outdated documents, or incomplete context can cause procedure misinterpretation or incorrect execution steps.

Potential consequences described in the Case Book include:
- longer troubleshooting time,
- repeated engineering rework,
- higher safety risk,
- delayed start-up,
- inconsistent decision-making across Process, Maintenance, Engineering, Operation, and HSE.

### Case 1 expected solution components

- Industrial Data Ops.
- AI Document Ingestion.
- Q&A Assistant & Semantic Search.
- Traceable Answer with Source.
- EDMS, AIMS, and Digital Twin Integration.
- Failure Memory System and Recommendation.

### Case 1 mandatory questions

1. How can the Company build a structured Industrial Data Ops foundation to connect scattered plant knowledge sources?
   - Main focus: Build connected knowledge foundation.

2. How can AI help engineers find trusted technical information faster and reduce the risk of improper execution?
   - Main focus: Improve search, Q&A, and answer verification.

3. How can the Manufacturing Knowledge Hub be integrated with operational systems to support reliability, troubleshooting, and continuous improvement?
   - Main focus: Active knowledge for operational decision support.

### Case 1 baseline data

| Data source | Purpose |
|---|---|
| SOP & Technical Document, Datasheets | Provides procedures and technical reference |
| P&IDs Data | Understand as-built equipment, piping systems, and instrumentation |
| Maintenance History | Capture incidents, root causes, and corrective actions |
| Tacit Knowledge | Capture SME experience and OPL data |

The Case Book says additional data sources may be proposed, but each must have clear business justification. A well-justified, high-quality data architecture is preferred over simply integrating more data.

---

## 9. Case 2, Official Case Definition

### Topic

Manufacturing performance data is fragmented across multiple dashboards, systems, and reports. This makes it difficult to:
- monitor plant performance,
- identify root causes,
- prioritize alerts,
- track follow-up actions.

### Background

Teams from:
- Operations,
- Production,
- Energy,
- Maintenance,
- HSE,
- Management,

use multiple dashboards and reports.

Each function may rely on different:
- systems,
- KPI definitions,
- data formats,
- reporting timelines.

When an issue occurs, examples include:
- abnormal energy consumption,
- production loss,
- emission deviation,
- equipment downtime.

Teams may need significant time to:
- validate data,
- compare reports,
- align interpretations,
before deciding the next action.

The stated result is slower and more reactive decision-making, together with difficulty:
- identifying root causes,
- prioritizing critical alerts,
- recommending corrective actions,
- tracking whether follow-up actions have been completed.

Potential optimization opportunities may be missed, and operational reliability can be affected.

---

## 10. Case 2 Problem Statement and Expected Solution

### Problem statement

Participants are challenged to design an Intelligent Manufacturing Dashboard that integrates fragmented manufacturing data into a **single pane of glass** for decision-making.

The solution should:
- connect data sources,
- display critical KPIs,
- identify operational problems,
- indicate possible root causes,
- prioritize alerts,
- guide follow-up actions.

The objective is to:
- reduce time spent on data validation,
- accelerate problem-solving,
- improve operational efficiency,
- reduce downtime,
- strengthen reliability and safety across functions.

### Expected solution components

#### Rationalize & Integrate Dashboard
Consolidate redundant dashboards and connect key manufacturing data sources into one governed view.

#### Single Pane of Glass
Provide one integrated dashboard to monitor:
- energy,
- production,
- emissions,
- downtime,
- operational performance.

#### Root Cause Analysis Support
Help identify probable causes using:
- problem history,
- KPI deviations,
- data patterns.

#### Follow-up Action Recommendation
Convert alerts and insights into:
- prioritized actions,
- owner,
- guidance,
- progress tracking.

---

## 11. Committee-Envisioned Five Core Elements

### 11.1 Single Pane of Glass
One integrated dashboard consolidates redundant dashboards and connects key manufacturing data sources into one governed view. It monitors energy, production, emissions, downtime, and operational performance and provides executive-level visibility.

### 11.2 AI Root-Cause Indication
AI helps identify a probable root cause using:
- problem history,
- KPI deviations,
- data patterns.

The source explicitly states this is an **indication supporting investigation**, not a replacement for the formal RCA process.

### 11.3 Alert Prioritization
An Alert Prioritization Engine converts alerts and insights into prioritized actions. It weighs:
- impact,
- urgency,
rather than simply counting alert volume.

### 11.4 Similar-Incident Retrieval
The solution should surface similar past incidents when a new problem is detected, allowing teams to leverage previously verified knowledge and solutions.

### 11.5 Action Tracking
The solution should convert alerts and recommendations into concrete actions with:
- owner,
- action guidance,
- progress tracking.

The intended result is visible and accountable follow-up status.

The Team Briefing summarizes the Committee's direction as:

> “One governed platform connects data → delivers insights → explains root causes → drives accountable actions for faster and safer decision-making.”

---

## 12. Dataset Architecture

The Team Briefing explicitly states that the Case 2 datasets are **not a one-way chain**.

They form two complementary source groups:

### Group A, condition and anomaly signals
- Production Data.
- Equipment Performance.

### Group B, incident history, root causes, and actions
- Incident Database.
- RCA & CAPA/PAA.

Both groups flow into an **Integrated Data Foundation**, which supports:
- Alert Prioritization.
- AI Root-Cause Indication.
- Similar-Incident Retrieval.
- Action Tracking.

The fifth layer, Alert & Action Tracking, is a solution layer designed by the team rather than a standalone raw data file.

---

## 13. Recommended Dataset Study Order

| Order | Dataset | Reason |
|---|---|---|
| 1 | Incident Database.xlsx | Widest view, 380 incidents across 12 plants. Introduces plant codes, risk tiers, failure mechanisms, and status stages. |
| 2 | Equipment Performance, 5 files | Establishes how the five hero assets were monitored weekly and how Availability, MTBF, and MTTR were computed. |
| 3 | Production Data, 5 files | Most granular raw layer, hourly sensor signals. Best interpreted after understanding alarm and trip thresholds. |
| 4 | RCA & CAPA/PAA, 5 PDFs | The “answer key” connecting incident record, weekly condition trend, hourly anomaly, verified root cause, and action plan. |
| 5 | Alert & Action Tracking | Not a source file. It is a designed layer combining fields from the preceding datasets. |

---

## 14. Production Data

### Function
Raw operational and sensor signals, PI tags, recording equipment and process conditions hour by hour before an incident. This is the rawest and most granular layer.

### Grain and files
- 1 row = 1 hour per asset.
- 5 files.
- Hero assets:
  - PU-2101B.
  - KO-3201.
  - PM-4405B.
  - HE-3301.
  - BL-5702.

### Period
- 720 hours, 30 days, per asset.
- KO-3201: 1–30 April 2026.
- PU-2101B: March 2026.
- HE-3301: May 2026.
- BL-5702: June 2026.
- PM-4405B: July 2026.

### Can be concluded
- Operational trends and anomalies leading to failure.
- Correlation between equipment condition and production output.
- Equipment run/stop profile.

### Cannot be concluded
- Conditions outside the 30-day window.
- A long historical baseline.
- Condition of the other 374 assets outside the five hero assets.
- Energy data.
- Emissions data.

### PI Tag sheet glossary

| Field | Meaning |
|---|---|
| Name | Short internal code used as the tag's column header, e.g. `KO3201_VIB`. This is a simplified dataset label, not the live DCS tag itself. |
| Description | Plain-language description of the measurement, e.g. “KO-3201 VIBRATION”. |
| digitalset | Filled only for binary/discrete tags and defines the on/off state set, e.g. `ON_OFF`. Blank for continuous analog tags. |
| engunits | Engineering unit, such as T/H, BARG, MM/S, DEG C, A, or ON_OFF. |
| span | Full measurement range, maximum readable value. |
| typicalvalue | Expected or typical operating value, used as a reference midpoint, roughly half of span in this dataset. |
| zero | Zero point or minimum of the instrument range. It is 0 for every tag in this dataset. |
| instrumenttag | Corresponding DCS/PI-historian point name, e.g. `KO3201V.PV`. `.PV` is standard DCS notation for Process Value. |

### Hourly data sheet glossary

| Field | Meaning |
|---|---|
| Timestamp | Date and hour of the reading, hourly resolution, 720 rows per 30 days. |
| `[Asset]_FEED` | Feed or throughput rate through the asset, T/H. |
| `[Asset]_DISP` | Downstream discharge pressure, barg. |
| `[Asset]_VIB` | Asset vibration reading, in the relevant unit, mm/s or micron depending on the asset. |
| `[Asset]_TEMP` | Relevant bearing or process temperature. |
| `[Asset]_AMP` | Motor current draw, A, an indirect indicator of mechanical loading. |
| `PLANT_RATE` | Overall plant/unit production rate, T/H. Shared plant-level context, not specific to one asset. |
| `RUN_STATUS` | Asset ON/OFF operating status. |

---

## 15. Equipment Performance

### Function
Weekly condition-monitoring records per asset plus reliability KPI summaries. It sits between hourly Production Data and verified RCA narrative.

### Grain and files
- 1 row = 1 week per asset.
- 5 files.
- Each file has three sheets:
  - Equipment Info.
  - Condition History.
  - Performance Summary.

### Period
- 26 weeks, approximately 6 months, per asset.
- Example given: KO-3201, 10 December 2025 to 3 June 2026.

### Can be concluded
- Weekly degradation trend.
- Transition from NORMAL to ALARM to TRIP.
- Availability.
- MTBF.
- MTTR.

### Cannot be concluded
- Hourly-level detail.
- Continuous time-series behavior.
- Conditions of non-hero assets.
- Maintenance cost.
- Spare-part availability.

### Equipment Info sheet

| Field | Meaning |
|---|---|
| Equipment Tag | Unique asset ID, matching Incident Database `Tag Number`. |
| Equipment Name | Full asset name. |
| Equipment Type | Plain-language equipment category. |
| Equipment Class | A/B/C criticality class, matching Incident Database. |
| Plant / Unit | Plant name plus short code. |
| Discipline | ROT, STA, ELE, or INS. |
| Criticality | Plain-language criticality label. Class A assets are “High” and Class B assets are “Medium” in this dataset. |
| Design Life | Expected service life of key wear components, e.g. bearing or seal element. |
| Monitoring Method | Normal monitoring method, such as online DCS plus monthly vibration/thermography route. |
| Linked RCA / AR No. | Link to Incident Database AR Number and matching RCA report. |
| Failure Date | Incident date. |
| Dominant Failure Mode | Short failure-mode label matching the RCA report title. |
| Monitored Parameters & Limits | Tracked parameters and Alarm/Trip thresholds. Direction matters because most parameters worsen upward, while some, such as seal-flush flow and lube-oil supply pressure, worsen downward. |

### Condition History sheet

| Field | Meaning |
|---|---|
| Week | Week number 1–26. |
| Date | Calendar date for that weekly reading. |
| Parameter columns | Four tracked parameters, varying by asset. |
| Health Status | NORMAL, ALARM, or TRIP, derived from threshold breaches. |
| Remark | Free-text note, usually blank except around key events or maintenance actions. |

### Performance Summary sheet

| Field | Meaning |
|---|---|
| Monitoring Period | 26 weeks for each asset. |
| Total Downtime | Pulled from the linked RCA report. |
| Period Hours | `26 × 168 = 4,368` hours. |
| Availability | `(Period Hours − Downtime) ÷ Period Hours × 100`. |
| No. of Failures | Distinct failure/trip events, one for each hero case file. |
| MTBF | `Period Hours ÷ No. of Failures`. |
| MTTR | Downtime for the failure event. |
| ALARM / TRIP / NORMAL readings | Count of weekly readings by status out of 26. |
| PM Compliance | Share of scheduled preventive maintenance completed. It is 92% for all five assets, so the briefing flags it as a shared baseline rather than an asset-specific differentiator. |
| Production Loss | Tons of lost production. |
| Estimated Loss | Financial value of production loss, in thousands of US dollars. |

---

## 16. Incident Database

### Function
Fleet-wide catalog of equipment-risk incidents. It is the widest-scope dataset and supports reliability analytics and cross-plant failure-pattern analysis.

### Grain and coverage
- 1 row = 1 incident, Abnormality Report.
- One file.
- `Incident Database` sheet plus `Dashboard` summary sheet.
- Period: 4 January 2024 to 25 July 2026, approximately 2.5 years.
- 380 incidents.
- 379 unique tags.
- 12 plants.

### Can be concluded
- Failure-frequency patterns.
- Bad-actor assets.
- Risk distribution by plant.
- Risk distribution by discipline.
- Risk distribution by failure mechanism.
- Incident resolution stage.

### Cannot be concluded
- Sensor or time-series behavior.
- Verified root causes for all 380 incidents.
- Full RCA evidence exists only for the five hero cases.

### Incident Database, 23-column glossary

| Field | Meaning |
|---|---|
| Serial No | Sequential row number, not a business ID. |
| MTO No. | Internal repair work-order reference, formatted `MTO-[year]-[plant]-[sequence]`. The full expansion of MTO is not stated in the provided files. |
| AR No. | Abnormality Report unique incident ID, formatted `AR-[year]-[plant]-[sequence]`. It links to the RCA report where available. |
| Plant | Three-letter plant/unit code. |
| Tag Number | Specific equipment tag. |
| Eq. Class | Equipment criticality class A, B, or C. |
| Date of Occur. | Incident date. |
| Risk Case Title | Short descriptive incident title. |
| Highest Impact | Main consequence category. |
| Pre-Risk | Pre-mitigation risk tier, I highest through IV lowest. |
| Risk Score | Numeric score underlying the risk tier, described as a Severity × Likelihood-style risk-matrix score. |
| PIC (RCA) | Person or role responsible for RCA, using discipline prefix and number. |
| Overall Status | Incident lifecycle stage. |
| Discipline | ROT, STA, ELE, or INS. |
| Eq. Type | Two-letter equipment-type code. |
| Component | Failed component. |
| F Mechanism | Failure mechanism category. |
| Downtime (hrs) | Production downtime caused by incident. |
| Act. Loss (k US$) | Actual realized loss. |
| Pot. Loss (k US$) | Potential/additional loss, risk exposure, or near-miss potential. It is not a fixed percentage across the full database. |
| Total Loss (k US$) | `Act. Loss + Pot. Loss`. |
| RCA Due Date | RCA completion deadline. |
| Month - Year | Month-year reporting bucket. |

### Plant legend

| Code | Meaning |
|---|---|
| ARP | Aurora Resin Plant, confirmed through RCA1, PU-2101B. |
| ZCU | Zeta Cracker Unit, confirmed through KO-3201 and HE-3301. |
| NUP | Nova Utility Plant, confirmed through PM-4405B. |
| OPP | Orion Polypropylene Plant, confirmed through BL-5702. |
| BDX, BRP, CRP, OP2, OP3, OPU, SMX, TKX | Present in the database, but full names are not stated in the provided files. Confirm with the data owner if needed. |

### Equipment class distribution

| Class | Meaning | Incidents |
|---|---|---:|
| A | Most critical, High criticality | 243 |
| B | Medium criticality | 118 |
| C | Least critical in this scheme | 19 |

### Pre-Risk distribution

| Tier | Meaning | Incidents |
|---|---|---:|
| I | Highest risk tier observed | 1 |
| II | High risk | 29 |
| III | Medium risk | 149 |
| IV | Lowest risk | 201 |

The Team Briefing notes that KO-3201 is Pre-Risk II, Risk Score 4000, with RCA Severity “Catastrophic”, and has the largest loss among the five hero cases. The other four hero cases are Pre-Risk III.

### Highest Impact distribution

| Category | Count | Meaning |
|---|---:|---|
| Uptime Loss | 148 | Main consequence was lost operating time or downtime. |
| Class A Eq. Breakdown | 110 | Breakdown of Class A equipment. |
| Equipment Bad Actor | 68 | Chronic or repeat-failure equipment. |
| UPSD / Delay Start-up | 42 | Unplanned Shutdown or delayed plant start-up. |
| Inspection Report | 10 | Issue identified through inspection. |
| Quality Loss | 2 | Product-quality impact. |

### Overall incident status

| Status | Count | Meaning |
|---|---:|---|
| NEW REGISTERED | 20 | Incident logged, RCA not yet started. |
| RCA PROCESS | 71 | Root-cause investigation underway. |
| CA/PA EXECUTION | 92 | Root cause verified, corrective/pro-active actions underway. |
| MONITORING RESULT | 37 | Actions completed, effectiveness being monitored before closure. |
| RISK CLOSED | 113 | Resolved, confirmed effective, and closed. |
| RISK CANCELED | 47 | Closed without full resolution, for example found invalid or not reportable on review. |

All five hero cases are at `CA/PA EXECUTION` status in the Incident Database.

### Equipment type legend

Confirmed from the five hero cases:

| Code | Equipment type |
|---|---|
| PU | Pump |
| CO | Compressor |
| EM | Electric Motor |
| HB | Heat-exchanger Bundle |
| BL | Blower |

Other codes include TX, CD, PZ, SW, RX, SX, TR, TK, FA, VA, and others. Their meanings are not stated in the provided files. The briefing gives examples of occurrence counts such as TX 47, EM 40, CD 25, PZ 24, SW 22, RX 22. The team should confirm other codes directly with the data owner if needed.

### Discipline and PIC

| Code | Meaning |
|---|---|
| ROT | Rotating Equipment, including pumps, compressors, blowers. |
| STA | Static Equipment, including heat exchangers, vessels, piping. |
| ELE | Electrical, including motors and switchgear. |
| INS | Instrument discipline. |

PIC examples include `REL-05`, `ROT-01`, `STA-02`, and `ELE-01`. The prefixes can represent Reliability, Rotating, Static, Electrical, Instrument, and Operations, followed by a person or role number.

### Potential-loss note

For the five curated hero cases, Potential Loss is exactly 30% of Actual Loss in each case. For example, KO-3201 has $1,584.00k Actual Loss and $475.20k Potential Loss.

This 30% ratio **does not hold across the full 380-row database**. Many rows have zero Potential Loss, and others have ratios above or below 30%. Therefore, 30% must not be treated as a documented general formula for the whole database.

---

## 17. RCA & CAPA/PAA

### Function
Verified Root Cause Analysis reports plus Corrective and Pro-Active Action plans. This is the narrative layer that connects the other datasets.

### Coverage
- 1 PDF per incident.
- 5 reports.
- Assets:
  - PU-2101B.
  - KO-3201.
  - PM-4405B.
  - HE-3301.
  - BL-5702.

### Can be concluded
- Verified root causes from structured investigation.
- Specific actions.
- Action owners.
- Action status.

### Cannot be concluded
The five RCA reports cannot be automatically generalized to all 380 incidents. Each incident has its own context and root cause.

### Recurring RCA fields

| Field | Meaning |
|---|---|
| AR Number | Same incident key as Incident Database `AR No.` |
| Tag / Plant | Equipment tag and plant code. |
| Date Occurrence | Failure date. |
| Pre-Risk | Same risk tier and score as Incident Database. |
| PIC (RCA) | Person/role responsible for RCA. |
| AR Type | All five hero reports show `OPEDR (Operation) — Uptime`, meaning Operations-related report with uptime loss as the primary impact. |
| Severity | Qualitative severity label such as Major, Catastrophic, Moderate. It is a qualitative counterpart, not identical to the numeric Pre-Risk tier. |
| Downtime / Loss | Same definitions as Incident Database. |
| Problem Statement | One or two sentences describing what happened. |
| Chronology of Events | Timestamped sequence from first symptom to restoration. |
| Impact Summary, 4W | What, When, Scope, Uptime Loss. |
| Parameter Verification, 4P | Up to five process parameters, P1–P5, checked against design specifications and marked G or NG. |
| 4M+1E Verification | Man, Machine, Method, Material, Environment checks, labeled X1–X4, marked G or NG. |
| Root Cause | Final verified root-cause statement synthesizing 4P and 4M+1E findings. |
| RCA Matrix Priority | Impact-versus-control 2×2 prioritization of root-cause codes. |
| Corrective & Pro-Active Action, CAPAA | Root-cause code, action, plan date, PIC, status. |
| Pro-Active Action | Similar table for rollout to sister or similar equipment. |
| Preventive & Risk Analysis | Preventive actions plus risk introduced by the corrective action and countermeasure. |
| PM Schedule Established | New or revised PM task and interval created from the RCA. |

---

## 18. Alert and Action Tracking Layer

Alert and Action Tracking is **not** a raw dataset available as a standalone file.

It is designed by combining information from the other datasets.

### Potential alert trigger
Equipment Performance `Health Status`:
- NORMAL.
- ALARM.
- TRIP.

### Individual action tracking
RCA CAPA/PAA status:
- Open.
- In Progress.
- Closed.

### Incident lifecycle tracking
Incident Database `Overall Status`:
- NEW REGISTERED.
- RCA PROCESS.
- CA/PA EXECUTION.
- MONITORING RESULT.
- RISK CLOSED.
- RISK CANCELED.

### Important distinction
`Overall Status` is an **incident-level lifecycle status**.

CAPA/PAA `Status` is an **individual action-level status**.

One incident in `CA/PA EXECUTION` can have several actions with different Open, In Progress, or Closed statuses.

The dashboard data model should therefore keep:
- **Incident Status**
- **Action Status**

as separate entities or fields.

---

## 19. Downtime Data Note

The Case Book lists “Downtime Data” as a baseline source for Case 2.

The Team Briefing states that no standalone downtime time-series dataset is available in the project.

Downtime information is available through:
1. Incident Database.
2. Equipment Performance, Performance Summary.
3. Five RCA & CAPA/PAA reports.

Those sources also contain production-loss and estimated-loss information.

If the deck refers to “Downtime Data,” it should explain that downtime is derived from those sources rather than from a standalone downtime dataset file.

---

## 20. Five Hero Cases

The five hero cases have:
- hourly Production Data,
- weekly Equipment Performance,
- verified RCA & CAPA/PAA reports.

They are therefore the strongest working examples for:
- AI Root-Cause Indication.
- Similar-Incident Retrieval.

### 20.1 Comparison

| Asset | Incident | Date | Downtime | Actual Loss | Total Loss | Pre-Risk |
|---|---|---|---:|---:|---:|---|
| PU-2101B | Mechanical seal leakage | 12 Mar 2026 | 18.5 h | $226.44k | $294.37k | III, 200 |
| KO-3201 | High radial vibration trip, bearing distress | 29 Apr 2026 | 32.0 h | $1,584.00k | $2,059.20k | II, 4000 |
| PM-4405B | Motor bearing failure, overheating | 8 Jul 2026 | 8.0 h | $112.00k | $145.60k | III, 200 |
| HE-3301 | High fouling, duty loss and high dP | 21 May 2026 | 12.0 h | $183.60k | $238.68k | III, 400 |
| BL-5702 | High vibration, coupling misalignment | 17 Jun 2026 | 14.0 h | $478.80k | $622.44k | III, 400 |

### Aggregate five-case figures

- Total downtime: **84.5 hours**.
- This is approximately **3.7%** of total downtime across all 380 incidents.
- Total Actual Loss: approximately **$2.58 million**.
- This is approximately **4.2%** of total Actual Loss across all incidents.
- Total Loss including Potential Loss: approximately **$3.36 million**.
- This is approximately **5.0%** of the **$67.19 million** Total Loss across all incidents.
- All five hero incidents have `CA/PA EXECUTION` status, so their corrective actions are not yet fully closed.

---

## 21. Hero Case 1, PU-2101B

### Asset
Feed Charge Pump, Resin Plant, ARP.

### Initial symptoms
- 11 March: field operator observed a minor seal weep during a routine round.
- 12 March, 02:15: seal-flush low-flow alarm annunciated.
- Visible feed-seal leak appeared with low suction pressure.
- Pump auto-tripped on low discharge pressure.

### Verified root cause
Premature mechanical seal failure caused by intermittent dry-running:
- suction cavitation during feed swings reduced NPSH,
- seal-flush flow fell below the 6 L/min minimum,
- no interlock existed to protect the seal.

### Downtime and losses
- 18.5 hours downtime.
- 251.6 tons production loss.
- $226.44k Actual Loss.
- $294.37k Total Loss.
- Pre-Risk III, score 200.

### Corrective and preventive actions
- Install seal-flush flow switch with DCS alarm.
- Add low-NPSH/loss-of-flush trip interlock.
- Revise feed-swing SOP, limiting ramp rate to 1 T/H per minute.
- Add seal-flush system, Plan 11, to PM checklist.
- Roll out flow switch to spare pump PU-2101A.

### Dashboard lesson
Monitor a leading indicator, seal-flush flow versus minimum specification, in real time rather than waiting for the final alarm.

The worsening seal MTBF trend, 26 to 9 months over three cycles, is also identified as a long-term degradation signal worth displaying.

---

## 22. Hero Case 2, KO-3201

### Asset
Cracked Gas Compressor, Cracker Unit, ZCU.

### Initial symptoms
- 27 April: drive-end radial vibration increased from 28 to 52 microns over five days.
- 29 April, 06:40: vibration reached the high-high setpoint of 75 microns.
- Machinery protection system tripped the compressor.

### Verified root cause
Journal-bearing babbitt distress caused by degraded oil-film strength due to water ingress through a leaking lube-oil cooler tube.

Detection weakness:
- no online water-in-oil monitoring,
- only a weekly grab sample.

### Downtime and losses
- 32.0 hours downtime.
- 1,760 tons production loss.
- $1,584.00k Actual Loss.
- $2,059.20k Total Loss.
- Pre-Risk II, score 4000.
- Largest loss among the five hero cases.

### Corrective and preventive actions
- Repair leaking lube-oil cooler tube.
- Install online water-in-oil sensor.
- Tighten vibration alert to 45 microns.
- Shorten trend-review cycle.
- Retube cooler at next turnaround.
- Roll out water-in-oil monitoring to KO-3202 and KO-3203.

### Dashboard lesson
The combination of:
- vibration trend,
- contaminant parameter, water-in-oil,
is described as a strong early-warning pattern.

The Team Briefing identifies KO-3201 as a suitable main hero case for the prototype because it has High criticality and the largest loss among the five cases.

---

## 23. Hero Case 3, PM-4405B

### Asset
Cooling Water Pump, Motor Driven, Utility Plant, NUP.

### Initial symptoms
- 6 July: motor drive-end bearing temperature increased from 68°C to 84°C.
- 8 July, 13:20: high-bearing-temperature alarm annunciated.
- Motor tripped on over-temperature.

### Verified root cause
Motor drive-end bearing failure caused by grease degradation from a fixed 12-month re-lubrication interval that was not risk-based.

Detection weakness:
- bearing temperature was not trended in CMMS.

### Downtime and losses
- 8.0 hours downtime.
- 160 tons production loss.
- $112.00k Actual Loss.
- Pre-Risk III, score 200.
- Smallest loss among the five hero cases.

### Corrective and preventive actions
- Change re-lubrication interval to risk-based, every four months.
- Add bearing-temperature trending and alerting to CMMS.
- Add PM-4405B/C to monthly vibration and thermography route.
- Apply risk-based re-greasing to all cooling-water pump motors.

### Dashboard lesson
Not every root cause originates from real-time sensors. Non-sensor maintenance parameters, such as PM and re-lubrication interval, should also be visualized and linked to failure risk.

---

## 24. Hero Case 4, HE-3301

### Asset
Feed/Effluent Heat Exchanger, Cracker Unit, ZCU.

### Initial symptoms
- 18 May: tube-side dP increased from 0.4 to 0.9 bar.
- Cold-outlet temperature fell over several days.
- 21 May: preheat duty dropped approximately 35% below design.
- Unit rate was reduced to protect the downstream section.

### Verified root cause
Accelerated tube-side coke/polymer fouling driven by feed heavy-ends above design:
- 2.4% measured,
- specification below 1.5%.

The condition progressed because:
- no dP-based cleaning trigger,
- no fouling KPI on the dashboard.

### Downtime and losses
- 12.0 hours downtime.
- 216 tons production loss.
- $183.60k Actual Loss.
- $238.68k Total Loss.
- Pre-Risk III, score 400.

### Corrective and preventive actions
- Add dP-based cleaning trigger and alarm.
- Tighten feed heavy-ends control and filtration.
- Add fouling factor and duty KPI to reliability dashboard.
- Apply dP-trigger logic to HE-3302 and HE-3303.

### Dashboard lesson
Unmonitored process KPIs such as dP and duty percentage can create blind spots. Automatic thresholds should trigger action instead of relying only on time-based schedules.

---

## 25. Hero Case 5, BL-5702

### Asset
Product Blower, Polymer Plant, OPP.

### Initial symptoms
- 15 June: vibration increased from 4.2 to 8.5 mm/s.
- A rising 2X harmonic appeared over two days.
- 17 June, 04:30: vibration reached the 11 mm/s alarm.
- Blower was stopped to prevent further damage.

### Verified root cause
High vibration caused by coupling misalignment, aggravated by:
- soft-foot,
- over-aged elastomer coupling element.

Detection weakness:
- periodic alignment and soft-foot checks were not part of routine PM,
- vibration route was monthly and too long to capture a fast two-day trend.

### Downtime and losses
- 14.0 hours downtime.
- 532 tons production loss.
- $478.80k Actual Loss.
- $622.44k Total Loss.
- Pre-Risk III, score 400.

### Corrective and preventive actions
- Add periodic laser alignment and soft-foot checks to PM.
- Track coupling-element age.
- Replace coupling element at 12 months.
- Shorten BL-5702 vibration route to weekly.
- Use wireless vibration sensor.
- Roll out alignment checks to all Class-A blowers in OPP.

### Dashboard lesson
An infrequent monitoring interval can miss a rapidly developing trend. The briefing proposes that the dashboard ideally support risk-based, adaptive monitoring frequency rather than a uniform interval for every asset.

---

## 26. Data-Driven Insights

The Team Briefing deliberately separates:
- **data facts**, directly supported by dataset numbers,
from
- **interpretations**, which are hypotheses requiring team validation.

### 26.1 Early Warning

#### Data facts
Equipment Performance shows ALARM-status readings before TRIP within the 26-week window:

| Asset | ALARM readings | Total weekly readings | TRIP |
|---|---:|---:|---:|
| PU-2101B | 6 | 26 | 1 |
| KO-3201 | 11 | 26 | 1 |
| PM-4405B | 6 | 26 | 1 |
| HE-3301 | 10 | 26 | 1 |
| BL-5702 | 15 | 26 | 1 |

All five RCA reports also record worsening parameter trends over 2 days to several days before the trip or shutdown.

#### Interpretation requiring validation
A threshold-based early-warning feature could potentially provide reaction time before failure.

The briefing explicitly says the actual reaction-time window must be calculated separately for each asset and must not be assumed to be identical.

### 26.2 Risk-Based Alerting

#### Data facts
Pre-Risk distribution across 380 incidents:
- IV: 201.
- III: 149.
- II: 29.
- I: 1.

Among the five hero cases:
- KO-3201 is Pre-Risk II.
- It has $1,584k Actual Loss and $2,059k Total Loss.
- It has larger loss than the four Pre-Risk III hero cases.

#### Interpretation requiring validation
The Pre-Risk label alone may not be proportional to actual loss in every case.

The proposed design implication in the briefing is that Alert Prioritization could consider:
- Pre-Risk,
- estimated impact,
- downtime,
- loss,
rather than risk score alone.

The briefing explicitly warns that this is an observation from five samples, not a statistical conclusion across all 380 incidents.

### 26.3 Similar-Incident Retrieval

#### Data facts
Recurring F Mechanism categories in the Incident Database include:

| Failure mechanism | Cases |
|---|---:|
| Leakage | 101 |
| High Vibration | 57 |
| Worn Out | 47 |
| Malfunction | 25 |
| Low Performance | 22 |
| Crack | 20 |
| Fouling | 20 |
| Error | 20 |
| Loose | 18 |
| Stuck | 15 |

#### Interpretation requiring validation
Grouping by:
- F Mechanism,
- Eq. Type,
- Component,
could provide a basis for similar-incident retrieval.

However, retrieval quality depends on consistency of those categories across the 380 rows, so data quality should be checked before relying on them in the prototype.

### 26.4 Action Tracking

#### Data facts
Incident `Overall Status`:
- NEW REGISTERED: 20.
- RCA PROCESS: 71.
- CA/PA EXECUTION: 92.
- MONITORING RESULT: 37.
- RISK CLOSED: 113.
- RISK CANCELED: 47.
- Total: 380.

Active handling stages:
`20 + 71 + 92 = 183 incidents`.

`183 / 380 × 100 ≈ 48.2%`.

If MONITORING RESULT is also treated as not final:
`20 + 71 + 92 + 37 = 220 incidents`.

`220 / 380 × 100 ≈ 57.9%`.

All five hero cases are included in the CA/PA EXECUTION group.

#### Interpretation requiring validation
The proportion of incidents still in progress supports the need for centralized Action Tracking.

However, the Team Briefing emphasizes that incident status is not the same as individual action status.

---

## 27. Data Limitations and Design Principles

### 27.1 Granular data exists for only five assets

**Limitation:** Production Data, hourly, and Equipment Performance, weekly, exist only for the five hero assets. Incident Database covers 380 incidents across 379 tags and 12 plants, but only at summary level.

**Design implication:** Prototype with the five hero assets as proof of concept and explicitly state that fleet-wide scaling requires additional data sources.

### 27.2 AI output is an indication, not a final decision

**Limitation:** AI Root-Cause Indication produces a probable root cause from patterns and historical data. It does not replace formal RCA using 4P and 4M+1E.

**Design implication:** Display AI output as:
- indication,
- candidate root cause,
- confidence level,
rather than an automatically executable final conclusion.

### 27.3 Actions require human verification

**Limitation:** CAPA/PAA action status, Open, In Progress, Closed, is managed manually by the PIC in the RCA reports.

**Design implication:** Action Tracking needs a human-in-the-loop approval or verification flow before an action is marked complete.

### 27.4 No energy or emissions dataset was found

The grand theme and Single Pane of Glass mention energy and emissions, but the project data does not contain an identified energy or emissions dataset.

**Design implication:** If the prototype displays energy/emissions:
- clearly label the information as dummy or illustrative data,
or
- label it as a future integration proposal.

Do not present it as existing project data.

### 27.5 Incident status and action status are different

Incident status:
- NEW REGISTERED.
- RCA PROCESS.
- CA/PA EXECUTION.
- MONITORING RESULT.
- RISK CLOSED.
- RISK CANCELED.

Action status:
- Open.
- In Progress.
- Closed.

**Design implication:** Keep separate Incident Status and Action Status fields/entities.

---

## 28. Three-Person Work Plan

The Team Briefing provides this as an initial allocation that can be adjusted according to member interests and strengths.

| Member | Focus | Main output |
|---|---|---|
| Member 1 | Business problem, business impact, KPIs, storytelling | Problem statement, KPI/success-metric list, Business Impact narrative, presentation storytelling flow |
| Member 2 | Data, AI logic, root-cause indication, alert prioritization | Data model from five datasets, AI Root-Cause Indication logic, Similar-Incident Retrieval logic, Alert Prioritization Engine |
| Member 3 | Prototype, user flow, dashboard design, demo video | Figma or HTML prototype, Single Pane of Glass user flow, Action Tracking user flow, 3-minute demo video |

### Collaboration rules

- Weekly sync-ups, or more frequently as the deadline approaches.
- Use the Team Briefing as the shared reference.
- Member 2 shares data-mapping and AI-logic results with Member 1 for evidence-backed Business Impact claims.
- Member 2 shares data constraints and AI logic with Member 3 so the prototype matches actual available data.
- Member 1 ensures every business-impact claim can be traced to the figures in Sections 5–6 of the Team Briefing rather than new, unverified numbers.
- Member 3 involves Members 1 and 2 when choosing prototype features so the prototype does not promise unsupported capabilities.
- Use one shared file or board, such as Figma, Google Slides, or a spreadsheet, to prevent version divergence.

### Outputs that must be agreed jointly

1. Main hero case for deck narrative and prototype.
2. Final wording of the three Case 2 Key Question answers.
3. Core prototype and demo-video features, respecting data limitations.
4. KPIs and success metrics for Business Impact, consistent with both the narrative and demonstrated technical capability.

### Section 9, Next Steps source limitation

The uploaded Team Briefing states that a practical work sequence should move the team from shared understanding toward the competition deck without jumping directly into design.

However, in the supplied DOCX content, the detailed numbered items after that introduction are not populated. The visible placeholders are `7.`, `8.`, `9.`, `10.`, `11.`, and `12.`. No descriptions for those numbered items are present in the extracted content. This Markdown therefore does not invent those missing steps.

---

## 29. Official Rules and Eligibility

### Eligibility and team formation

1. Active undergraduate, S1, or vocational, diploma, students are eligible throughout the competition period from August to October 2026.
2. Teams must have 2–3 members.
3. All members must come from the same university or college.
4. A participant may not be registered in more than one team.
5. Students involved in academic violations or under university sanctions during the competition period cannot participate.
6. Team members and team name cannot be changed once the competition begins.
7. Every team must have a faculty advisor or lecturer as supervisor.
8. Each team may submit only one proposal.
9. If selected for the Final Stage, all team members must attend the offline Final Stage in person on 4–5 November 2026.
10. Registration constitutes agreement to the CALIBER 2026 rules and guidelines.

### Rules and regulations

1. Proposed ideas must be relevant to the provided case.
2. Teams must follow the booklet regulations and submit all required documents.
3. All submitted materials must be in English.
4. Submitted materials become the property of Chandra Asri Group and will not be returned.
5. Plagiarism or other misconduct results in disqualification.
6. Jury and Chandra Asri Group CALIBER 2026 Committee decisions are final and cannot be appealed.
7. Participants will be notified of changes to rules and regulations.

---

## 30. FAQ

### General FAQ

**Can I register for more than one team?**  
No. Each participant can only be registered in one team.

**Can team members come from different faculties or majors?**  
Yes, provided all members are from the same university or college.

**Do we need to work on both use cases for Preliminary Stage?**  
No. Choose one case.

**Can we combine ideas from both cases?**  
No. Select one case. Extended solutions may be developed within that case, but attention must remain on that case.

**What file formats and size limits apply?**  
For Preliminary Stage, all three deliverables combined must not exceed 10 MB. Final Stage submission format will be provided during the event.

**What language should be used?**  
All materials and pitch delivery must be in English.

**Can generative AI tools be used during solution development?**  
Yes, provided they are used lawfully and according to applicable terms and conditions and privacy notices. AI-generated outputs must be validated, iterated, and evaluated for quality, accuracy, and reliability before use or implementation.

**Can a submission be updated or replaced after submission?**  
No. Only the first submitted version is accepted and evaluated.

**What happens if one required deliverable is missing?**  
The team is disqualified and cannot continue to the next stage.

### Case Book FAQ

The Case Book repeats and expands several of the same points:

- Only one use case is required.
- Ideas from the two cases must not be combined.
- All listed Key Questions are mandatory.
- Preliminary-stage datasets are included in the Case Book.
- Relevant dummy data may be generated or used.
- Publicly available data and reasonable assumptions may supplement the baseline.
- External data must have clear relevance and business-value justification.
- All three Preliminary Stage materials combined must be no larger than 10 MB.
- Final Stage format will be informed at the event.
- All materials must be in English.
- Generative AI use is permitted under lawful use, applicable terms, and privacy notices, with validation required.
- The first submission is final.
- Failure to submit any required deliverable causes disqualification.

---

## 31. Registration

The booklet's registration process:

1. Visit the CALIBER page on the Chandra Asri website.
2. Navigate to the CALIBER 2026 menu.
3. Fill out the registration form.
4. After registration, receive a confirmation email and Case Book.
5. If the confirmation email and case are not received within 48 hours, contact the CALIBER 2026 Committee at `caliber.2026@capcx.com`.

The booklet gives the website as:
`https://chandra-asri.com/id/caliber`

---

## 32. Contacts

### CALIBER 2026 Committee
Email:
`caliber.2026@capcx.com`

### Sherrish Tanudirdjo
Corporate Communications, Chandra Asri Group  
Email:
`Sherrish.Tanudirdjo@capcx.com`

### Alifa Shavira
Corporate Communications, Chandra Asri Group  
Email:
`Alifa.Shavira@capcx.com`

### Head Office
PT Chandra Asri Pacific Tbk  
Wisma Barito Pacific Tower A, 5th Floor  
Jl. Let. Jend. S. Parman Kav. 62–63  
Jakarta 11410, Indonesia

Phone:
`(62-21) 530 7950`

Fax:
`(62-21) 530 8930`

---

## 33. Grand Prizes

The booklet displays three prize amounts:

- **Rp15 million**
- **Rp10 million**
- **Rp7.5 million**

The supplied booklet page displays the amounts but does not assign additional labels in the extracted text.

---

## 34. Final Stage

The Final Stage is a 2-day hackathon.

- Top 10 teams from Preliminary Stage advance.
- Day 1 provides a new and entirely different use case.
- Teams have 24 hours to develop a solution.
- Teams pitch on the following day.
- Final Stage submission format is announced during the event.
- Pitching is in English.
- Scheduled Wednesday–Thursday, 4–5 November 2026, Jakarta.
- Finalists are notified later about event details.
- The booklet asks finalists to ensure availability in advance.
- All selected team members must attend in person.

---

## 35. Source-Supported Quantitative Calculations

### Performance monitoring period
`26 weeks × 168 hours/week = 4,368 hours`.

### Active incident-handling stages
`NEW REGISTERED + RCA PROCESS + CA/PA EXECUTION`

`20 + 71 + 92 = 183`

`183 ÷ 380 × 100 ≈ 48.2%`.

### Not-yet-final incidents including monitoring
`20 + 71 + 92 + 37 = 220`

`220 ÷ 380 × 100 ≈ 57.9%`.

### Five hero cases
Total downtime:
`18.5 + 32.0 + 8.0 + 12.0 + 14.0 = 84.5 hours`.

The Team Briefing reports this as approximately 3.7% of total downtime across 380 incidents.

Actual Loss:
`$226.44k + $1,584.00k + $112.00k + $183.60k + $478.80k ≈ $2.58 million`.

Total Loss:
`$294.37k + $2,059.20k + $145.60k + $238.68k + $622.44k ≈ $3.36 million`.

The briefing reports approximately:
- 4.2% of total Actual Loss for the five cases.
- 5.0% of the $67.19 million total loss across all 380 incidents.

---

## 36. Source File Inventory from the Team Briefing

The internal Team Briefing states that it was prepared from the following project files.

### Case and registration documents
- `The Case - CALIBER 2026 1.pdf`
- `Booklet CALIBER 2026 - Registration Extended.pdf`
- `Data Set Explanation for Case 2 Intelligence Manufacturing.pptx`

### RCA & CAPA/PAA reports
- `RCA1 - PU-2101B Mechanical Seal Leakage.pdf`
- `RCA2 - KO-3201 High Radial Vibration Trip.pdf`
- `RCA3 - PM-4405B Motor Bearing Failure.pdf`
- `RCA4 - HE-3301 High Fouling — Duty Loss & High dP.pdf`
- `RCA5 - BL-5702 High Vibration.pdf`

### Equipment Performance datasets
- `Equipment Performance - RCA1 PU-2101B.xlsx`
- `Equipment Performance - RCA2 KO-3201.xlsx`
- `Equipment Performance - RCA3 PM-4405B.xlsx`
- `Equipment Performance - RCA4 HE-3301.xlsx`
- `Equipment Performance - RCA5 BL-5702.xlsx`

### Production Data datasets
- `Production Data - RCA1 PU-2101B.xlsx`
- `Production Data - RCA2 KO-3201.xlsx`
- `Production Data - RCA3 PM-4405B.xlsx`
- `Production Data - RCA4 HE-3301.xlsx`
- `Production Data - RCA5 BL-5702.xlsx`

### Incident dataset
- `Incident Database.xlsx`

---

# Appendix A. Complete Source, Registration Booklet

The following pages preserve the complete substantive text of the uploaded registration booklet, organized by source page.


## Source A. Internal Team Briefing, CALIBER 2026 Case 2

> Source file: `CALIBER2026_Case2_TeamBriefing.docx`. Prepared for internal team use on 21 September 2026.

INTERNAL TEAM BRIEFING DOCUMENT

CALIBER 2026 — Case 2

Team Briefing: Intelligent Manufacturing Dashboard

Chandra Asri Limitless Innovation & Business Strategy Challenge 2026

| Team | [Team Name] |
| --- | --- |
| University | [University Name] |
| Member 1 | [Member 1 Name] |
| Member 2 | [Member 2 Name] |
| Member 3 | [Member 3 Name] |
| Date | 21 September 2026 |

#### Purpose of This Document

To align all three team members on the competition, the business problem, and the full Case 2 dataset before the team starts designing the solution and building the competition deck. This document is not the final proposal and not the competition deck.

### 1. Competition Overview

CALIBER (Chandra Asri Limitless Innovation and Business Strategy Challenge) 2026 is an annual competition organized by Chandra Asri Group (PT Chandra Asri Pacific Tbk), open to active undergraduate (S1) or vocational (diploma) students to showcase analytical ability, strategic thinking, and problem-solving through an AI-based business proposal.

This year's grand theme: “Future-Ready Operational Excellence: Knowledge, Reliability, and Smart Manufacturing” — participants apply Artificial Intelligence to address critical manufacturing challenges in a petrochemical environment, with solutions that integrate plant and enterprise data, provide transparent and traceable recommendations, and consider human oversight, data security, system reliability, and measurable business impact.

#### Competition Structure

The competition consists of two stages:

Preliminary Stage — participants select one of two use cases and develop a business proposal.

Final Stage (Hackathon) — the top 10 teams from the Preliminary Stage work on a new, different use case within 24 hours, then present the following day. Scheduled Wednesday–Thursday, 4–5 November 2026 in Jakarta.

#### Case 2 Focus Chosen by the Team

The team has chosen Case 2: Intelligent Manufacturing (Unified Dashboard, AI Insight, Root Cause Analysis, Follow-up Action Recommendation). This case focuses on manufacturing performance data that is fragmented across dashboards, systems, and reports, making it difficult to monitor plant performance, identify root causes, prioritize alerts, and track follow-up actions.

| Important notes / • Only one case may be worked on — ideas from Case 1 and Case 2 must not be combined. / • The dataset provided in the Case Book may be supplemented with dummy data, public data, or reasonable assumptions, as long as their relevance is explained in the deck. / • All materials (prototype, video, deck) must be in English. |
| --- |

#### Preliminary Stage Deliverables

To pass the Preliminary Stage review, the team must submit the following 3 materials (combined total no larger than 10 MB):

#### Three Mandatory Key Questions for Case 2

All three must be answered in the Solution or Business Impact section of the deck:

#### Key Timeline

| Stage | Date |
| --- | --- |
| Registration closes (extended) | 17 September 2026 |
| Proposal submission deadline | 4 October 2026, 23:59 WIB |
| Best Proposal announcement (advancing to the Final) | 23 October 2026 |
| Final Presentation & winner announcement | 4–5 November 2026, Jakarta |

#### Evaluation Criteria

Problem Understanding & Business Impact — clarity of problem understanding, impacted users, KPIs, and evidence of business impact.

Solution Design & Prototype Quality — logical workflow, user journey, UX clarity, prototype completeness, and technology relevance.

Presentation Quality — presentation structure, visual clarity, storytelling flow, and demo video quality within the 3-minute limit.

Feasibility & Roadmap — realistic technical, operational, legal, cybersecurity, and organizational-readiness implementation plan.

Chemical Domain Relevance — fit with real chemical industry needs and the selected case context.

### 2. The Case 2 Business Problem

At a chemical manufacturing plant, the Operations, Production, Energy, Maintenance, HSE, and Management teams each monitor plant performance through different dashboards and reports. Every function runs its own system, its own KPI definitions, its own data format, and its own reporting schedule. This condition is the root of the four problems below.

### 1. Fragmented Dashboards

Because each function uses a different dashboard, system, and KPI definition, whenever an anomaly occurs — abnormal energy consumption, production loss, emission deviation, or equipment downtime — teams must spend significant time validating data, comparing reports across systems, and aligning interpretations before they can decide on the next action. The result is slower, more reactive decision-making.

### 2. Difficulty Finding Root Causes

Without one integrated view of the data, teams struggle to connect symptoms (KPI deviations, alarms) to the history of similar problems and historical data patterns. Root-cause investigation becomes time-consuming because the information needed is scattered across different, unconnected systems.

### 3. Alert Prioritization Problems

When many alerts appear from various systems without a consistent prioritization mechanism, teams find it hard to determine which ones are truly critical and need to be handled first. This risks delaying the handling of high-impact issues while minor issues receive disproportionate attention.

### 4. Weak Follow-up Action Tracking

Data fragmentation also makes it difficult to track whether a follow-up action has actually been completed, who is responsible for it, and how far its progress has gone. Without centralized tracking, optimization opportunities can potentially be missed, and operational reliability may be affected.

| Overall impact (per the Case Book) / • Decision-making becomes slower and more reactive rather than proactive. / • Difficult to identify root causes, prioritize critical alerts, recommend corrective actions, and track the completion of follow-up actions. / • Optimization opportunities can potentially be missed, and operational reliability and safety may be affected. |
| --- |

### 3. The Solution Envisioned by the Committee

The Committee expects an Intelligent Manufacturing Dashboard that integrates fragmented manufacturing data into a single pane of glass for decision-making. This solution connects data sources, displays critical KPIs, identifies operational problems, indicates possible root causes, prioritizes alerts, and guides follow-up actions. The five core elements expected are:

### 1. Single Pane of Glass

One integrated dashboard that consolidates redundant dashboards and connects key manufacturing data sources into one governed view. This dashboard monitors energy, production, emissions, downtime, and operational performance comprehensively — providing executive-level visibility of manufacturing performance.

### 2. AI Root-Cause Indication

AI capability to help identify the probable root cause of an operational issue, using problem history, KPI deviations, and data patterns. This is meant as an indication that supports investigation, not a replacement for the formal RCA process (see Section 7).

### 3. Alert Prioritization

A mechanism (Alert Prioritization Engine) that converts alerts and insights into prioritized actions — weighing the level of impact and urgency, not merely alert volume — so teams can focus on the most critical issues first.

### 4. Similar-Incident Retrieval

The ability to search and surface similar past incidents when a new problem is detected, so teams can leverage previously verified knowledge and solutions to speed up resolution.

### 5. Action Tracking

A feature that converts alerts and recommendations into concrete actions with an owner, action guidance, and progress tracking — so the completion status of every follow-up action is always visible and accountable.

A concise summary from the Committee's material: “One governed platform connects data → delivers insights → explains root causes → drives accountable actions for faster and safer decision-making.”

### 4. Dataset Map

This section maps all datasets available in the Project for Case 2. The five dataset groups below are not a one-way chain; instead, they fall into two complementary source groups: (1) Production Data and Equipment Performance as sources of condition & anomaly signals, and (2) Incident Database and RCA & CAPA/PAA as sources of incident history, root causes, and actions. Together, these two groups form the foundation for four dashboard capabilities — Alert Prioritization, AI Root-Cause Indication, Similar-Incident Retrieval, and Action Tracking — as shown in Figure 1. To help the team read each file with confidence, this section also gives the recommended study order and a full column-by-column glossary for every dataset.

Figure 1. Two groups of data sources (condition & anomaly signals; incident history, root causes, and actions) both flow into one integrated data foundation, which then supports four AI capabilities — not a one-way flow.

#### Recommended Order to Study the Datasets

Read the five dataset groups in this order — from broad context to raw signal, ending with the narrative that ties everything together:

| Order | Dataset | Why this order |
| --- | --- | --- |
| 1 | Incident Database.xlsx | Start here. It is the widest view — all 380 incidents across 12 plants — and works like a table of contents. It introduces the vocabulary (plant codes, risk tiers, failure mechanisms, status stages) used everywhere else. |
| 2 | Equipment Performance (5 files) | Once you know which 5 assets are the hero cases, learn how each one's condition was tracked week by week and how its reliability KPIs (Availability, MTBF, MTTR) were computed. |
| 3 | Production Data (5 files) | The most granular, rawest layer (hourly sensor signals). Best understood after you already know each asset's alarm/trip thresholds from Equipment Performance, so the hourly numbers have context. |
| 4 | RCA & CAPA/PAA (5 PDFs) | Read last, as the “answer key” — it ties the incident record, the weekly condition trend, and the hourly signal anomaly together into one verified root cause and action plan. |
| 5 | Alert & Action Tracking | Not a file to read — a layer the team designs by combining fields from the four datasets above (see Section 4.5). |

### 1. Production Data

| Function | Raw operational/sensor signals (PI tags) recording equipment and process conditions hour by hour, prior to an incident. This is the rawest, most granular layer in the whole dataset map. |
| --- | --- |
| Grain & number of files | 1 row = 1 hour, per asset. Available as 5 separate files — one per hero-case asset (PU-2101B, KO-3201, PM-4405B, HE-3301, BL-5702). |
| Period | 720 hours (30 days) per asset, covering the month in which the incident occurred for that asset (e.g., KO-3201: 1–30 April 2026; PU-2101B: March 2026; HE-3301: May 2026; BL-5702: June 2026; PM-4405B: July 2026). |
| Can be concluded | Operational trends and anomalies leading up to a failure; correlation between equipment condition and production output; equipment run/stop profile. |
| Cannot be concluded | Conditions outside that 30-day window (no long historical baseline in this file); the condition of the other 374 assets outside the 5 hero-case assets; no energy or emissions data. |

Column Glossary — “PI Tag” sheet (one row per instrument)

| Field | Meaning |
| --- | --- |
| Name | The short internal code used as that tag's column header in the hourly data sheet (e.g., KO3201_VIB). This is a simplified dataset label, not the live DCS tag itself. |
| Description | Plain-language description of what the tag measures (e.g., “KO-3201 VIBRATION”). |
| digitalset | Only filled in for binary/discrete tags — defines the on/off state set (e.g., “ON_OFF” for RUN_STATUS). Left blank for continuous analog tags such as pressure or vibration. |
| engunits | The engineering unit of measurement: T/H (tons/hour), BARG (bar gauge), MM/S (millimetres/second), DEG C (Celsius), A (Ampere), or ON_OFF (binary state). |
| span | The instrument's full measurement range — the maximum value it can read. |
| typicalvalue | The expected/typical operating value, used as a reference midpoint (in this dataset, roughly half of span). |
| zero | The zero point / minimum of the instrument's range (0 for every tag in this dataset). |
| instrumenttag | The corresponding DCS/PI-historian point name (e.g., KO3201V.PV). The “.PV” suffix is standard DCS notation for “Process Value” — the live measured value at that point. |

Column Glossary — hourly data sheet

| Field | Meaning |
| --- | --- |
| Timestamp | Date and hour of the reading (hourly resolution; 720 rows = 30 days). |
| [Asset]_FEED | Feed / throughput rate through the asset, in T/H (e.g., KO3201_FEED, PU2101B_FEED). |
| [Asset]_DISP | Discharge pressure downstream of the asset, in barg. |
| [Asset]_VIB | Vibration reading for the asset, in the unit shown for that tag in the “PI Tag” sheet (mm/s or micron, depending on the asset). |
| [Asset]_TEMP | Temperature reading relevant to that asset — bearing or process temperature depending on the equipment type. |
| [Asset]_AMP | Motor current draw, in Ampere — an indirect indicator of mechanical loading. |
| PLANT_RATE | The overall plant/unit production rate (T/H) at that hour. This is shared plant-wide context, not specific to the one asset. |
| RUN_STATUS | ON/OFF operating status of the asset during that hour. |

### 2. Equipment Performance

| Function | Weekly condition-monitoring records per asset, along with a summary of reliability KPIs (Availability, MTBF, MTTR, etc.). Sits between the raw hourly signal (Production Data) and the verified narrative (RCA). |
| --- | --- |
| Grain & number of files | 1 row = 1 week, per asset. Available as 5 files — one per hero-case asset, each with 3 sheets: Equipment Info, Condition History, and Performance Summary. |
| Period | 26 weeks (≈ 6 months) per asset, covering the incident date (e.g., KO-3201: 10 Dec 2025 – 3 Jun 2026). |
| Can be concluded | Weekly degradation trend leading to failure; the point at which status shifts from NORMAL → ALARM → TRIP; per-asset reliability metrics (availability, MTBF, MTTR). |
| Cannot be concluded | Hourly-level detail (this data is weekly, not continuous time-series); the condition of assets outside the 5 hero-case assets; maintenance cost or spare-part availability. |

Column Glossary — “Equipment Info” sheet

| Field | Meaning |
| --- | --- |
| Equipment Tag | The asset's unique ID (matches “Tag Number” in the Incident Database). |
| Equipment Name | Full descriptive name of the asset. |
| Equipment Type | Plain-language equipment category (e.g., “Centrifugal Compressor”). |
| Equipment Class | Criticality class — A / B / C — the same scale used in the Incident Database's “Eq. Class” column. |
| Plant / Unit | Plant name plus its short code (e.g., “Cracker Unit (ZCU)”). |
| Discipline | Engineering discipline responsible: ROT (Rotating), STA (Static), ELE (Electrical), INS (Instrument). |
| Criticality | Plain-language criticality label. In this dataset, Class A assets are labeled “High” and Class B assets “Medium”. |
| Design Life | Expected service life of the key wear components (e.g., “5 years (bearing) / 24 months (seal element)”). |
| Monitoring Method | How the asset is normally monitored, e.g. “Online DCS + monthly vibration/thermography route”. |
| Linked RCA / AR No. | Cross-reference to the AR Number in the Incident Database and the matching RCA & CAPA/PAA PDF. |
| Failure Date | Date of the incident this file profiles. |
| Dominant Failure Mode | Short label of the failure mode, matching the RCA report's title. |
| Monitored Parameters & Limits (side table) | Lists each tracked parameter with its Alarm and Trip threshold, shown as “Alarm / Trip” (e.g., “45 / 75”). Read the direction carefully per parameter: for most parameters a higher reading is worse, but for a few (e.g., seal-flush flow, lube-oil supply pressure) a lower reading is worse, so the alarm/trip pair are lower bounds instead. |

Column Glossary — “Condition History” sheet

| Field | Meaning |
| --- | --- |
| Week | Sequential week number within the 26-week monitoring window (1–26). |
| Date | Calendar date of that week's reading. |
| [4 parameter columns] | The same parameters listed in “Monitored Parameters & Limits” above (different per asset, e.g. vibration, seal-flush flow, discharge pressure, bearing temperature for PU-2101B), one weekly reading each. |
| Health Status | NORMAL / ALARM / TRIP — the week's classification, derived from whether the readings breach that parameter's Alarm/Trip threshold. |
| Remark | Free-text note; blank most weeks, filled in around the key weeks (e.g., noting the failure event or a maintenance action). |

Column Glossary — “Performance Summary” sheet (computed KPIs)

| Field | Meaning |
| --- | --- |
| Monitoring Period (weeks) | 26 for every asset — the length of the Condition History window. |
| Total Downtime (hours) | Pulled directly from the linked RCA report's downtime figure. |
| Period Hours | Total hours in the monitoring window: 26 weeks × 168 hours/week = 4,368. |
| Availability (%) | (Period Hours − Downtime) ÷ Period Hours × 100. |
| No. of Failures (period) | Count of distinct failure/trip events in the window — equal to 1 for every hero-case file, since each file is built around one incident. |
| MTBF (hours) | Mean Time Between Failures = Period Hours ÷ No. of Failures. |
| MTTR (hours) | Mean Time To Repair = the downtime of that one failure event. |
| ALARM / TRIP / NORMAL readings | Count of weekly readings that fell into each Health Status category, out of 26. |
| PM Compliance (%) | Share of scheduled preventive maintenance actually completed. This is 92% for all 5 assets in this dataset — worth flagging to the team as a possible shared baseline figure rather than a truly asset-specific measurement, since it does not vary. |
| Production Loss (ton) | Tons of product lost as a result of the downtime. |
| Estimated Loss (k USD) | Financial value of that production loss, in thousands of US dollars. |

### 3. Incident Database

| Function | A catalog of equipment risk incidents across the entire fleet (not only the 5 hero-case assets) — the widest-scope dataset, and the source for reliability analytics and cross-plant failure patterns. |
| --- | --- |
| Grain & number of files | 1 row = 1 incident (Abnormality Report). 1 file, “Incident Database” sheet (plus a “Dashboard” summary sheet). |
| Period | 4 January 2024 – 25 July 2026 (≈ 2.5 years); 380 incidents across 379 unique tags at 12 plants. |
| Can be concluded | Failure-frequency patterns and bad-actor assets; risk distribution by plant, discipline, and failure mechanism; the resolution stage (status) of each incident. |
| Cannot be concluded | Sensor/time-series data (not present here); verified root causes for all 380 incidents — full RCA reports are only available for the 5 hero-case incidents covered in Section 5. |

Column Glossary — “Incident Database” sheet (23 columns)

| Field | Meaning |
| --- | --- |
| Serial No | Sequential row number in the database — a row identifier, not a business ID. |
| MTO No. | Internal work-order reference number for the repair job, formatted “MTO-[year]-[plant]-[sequence]” (e.g., MTO-2026-ARP-0031). The full expansion of “MTO” is not stated in the provided files — treat it as an internal work-order ID and confirm with the data owner if the proposal needs the exact term. |
| AR No. | Abnormality Report number, the incident's unique ID, formatted “AR-[year]-[plant]-[sequence]”. This is the key that links a row here to its RCA & CAPA/PAA PDF report, where one exists. |
| Plant | The 3-letter plant/unit code where the incident occurred. See the Plant legend below. |
| Tag Number | The specific equipment's unique tag ID (e.g., PU-2101B). |
| Eq. Class | Equipment criticality class: A (most critical) / B / C (least critical). See the Eq. Class legend below. |
| Date of Occur. | The date the failure/incident occurred. |
| Risk Case Title | A short descriptive title combining the equipment and the symptom. |
| Highest Impact | The category of the incident's single most significant consequence. See the Highest Impact legend below. |
| Pre-Risk | The pre-mitigation risk tier, I (highest) through IV (lowest). See the Pre-Risk legend below. |
| Risk Score | The numeric score underlying the Pre-Risk tier — a Severity × Likelihood-style risk-matrix score. |
| PIC (RCA) | Code identifying who is responsible for conducting the RCA: a discipline prefix plus a number (e.g., REL-05 = Reliability engineer #5). See the PIC legend below. |
| Overall Status | The incident's current lifecycle stage. See the Overall Status legend below. |
| Discipline | Engineering discipline that owns the equipment: ROT / STA / ELE / INS. See the Discipline legend below. |
| Eq. Type | 2-letter equipment-type code. See the Eq. Type legend below. |
| Component | The specific part that failed (e.g., Bearing, Valve, Coupling, Mechanical Seal). |
| F Mechanism | The failure-mechanism category (e.g., Leakage, High [vibration], Worn Out, Crack, Fouling, Malfunction). |
| Downtime (hrs) | Hours of production downtime caused by the incident. |
| Act. Loss (k US$) | Actual realized financial loss, in thousands of US dollars. |
| Pot. Loss (k US$) | Potential / additional loss beyond the realized amount (e.g., risk exposure or near-miss potential), in k US$. See the note below the legends — this is not a fixed percentage of Act. Loss across the full database. |
| Total Loss (k US$) | Act. Loss + Pot. Loss. |
| RCA Due Date | The deadline by which the RCA must be completed. |
| Month - Year | The month-year bucket of the incident, used for monthly/trend reporting. |

Legends for the coded fields

Plant — 12 codes appear in the database; only the 4 used by the hero cases are confirmed by name in the provided files:

| Field | Meaning |
| --- | --- |
| ARP | Aurora Resin Plant (confirmed — RCA1, PU-2101B). |
| ZCU | Zeta Cracker Unit (confirmed — RCA2 KO-3201 and RCA4 HE-3301). |
| NUP | Nova Utility Plant (confirmed — RCA3, PM-4405B). |
| OPP | Orion Polypropylene Plant (confirmed — RCA5, BL-5702). |
| BDX, BRP, CRP, OP2, OP3, OPU, SMX, TKX | Other plant codes present in the Incident Database. Their full names are not stated anywhere in the provided files — confirm with the data owner/committee if the proposal needs to name them. |

Eq. Class — criticality tier (cross-checked against Equipment Performance's “Criticality” field for the 5 hero cases):

| Field | Meaning |
| --- | --- |
| A | Most critical equipment — “High” criticality (243 of 380 incidents). |
| B | Medium criticality (118 of 380 incidents). |
| C | Least critical equipment in this scheme (19 of 380 incidents). |

Pre-Risk — pre-mitigation risk tier (I = highest risk, IV = lowest); cross-checked against the RCA reports' qualitative “Severity” label:

| Field | Meaning |
| --- | --- |
| I | Highest risk tier observed (1 of 380 incidents). |
| II | High risk tier (29 of 380 incidents). Example: KO-3201, Risk Score 4000, RCA Severity label “Catastrophic” — the largest-loss hero case despite not being tier I. |
| III | Medium risk tier (149 of 380 incidents) — all four other hero cases (PU-2101B, PM-4405B, HE-3301, BL-5702) sit here, with RCA Severity labels ranging from “Moderate” to “Major”. |
| IV | Lowest risk tier (201 of 380 incidents) — the most common tier in the database. |

Highest Impact — category of the incident's single largest consequence:

| Field | Meaning |
| --- | --- |
| Uptime Loss (148) | The incident's main consequence was lost operating time / downtime. |
| Class A Eq. Breakdown (110) | Breakdown of a Class A (most critical) piece of equipment. |
| Equipment Bad Actor (68) | The equipment is flagged as a chronic, repeat-failure item. |
| UPSD / Delay Start-up (42) | Unplanned Shutdown, or a delayed plant start-up. |
| Inspection Report (10) | Issue found through inspection, not necessarily causing downtime by itself. |
| Quality Loss (2) | The incident affected product quality. |

Overall Status — the incident's lifecycle stage, sequential from left to right:

| Field | Meaning |
| --- | --- |
| NEW REGISTERED (20) | Incident just logged; RCA not yet started. |
| RCA PROCESS (71) | Root-cause investigation is underway. |
| CA/PA EXECUTION (92) | Root cause verified; corrective/pro-active actions are being carried out. (All 5 hero cases are currently at this stage.) |
| MONITORING RESULT (37) | Actions completed; their effectiveness is being monitored before final closure. |
| RISK CLOSED (113) | Resolved, confirmed effective, and closed. |
| RISK CANCELED (47) | Closed without going through full resolution — e.g., found not to be a valid or reportable case on review. |

Eq. Type — 2-letter equipment-type code; only 5 are confirmed by the hero cases, the rest appear elsewhere in the fleet-wide data:

| Field | Meaning |
| --- | --- |
| PU | Pump (confirmed — PU-2101B). |
| CO | Compressor (confirmed — KO-3201). |
| EM | Electric Motor (confirmed — PM-4405B). |
| HB | Heat-exchanger Bundle (confirmed — HE-3301). |
| BL | Blower (confirmed — BL-5702). |
| TX, CD, PZ, SW, RX, SX, TR, TK, FA, VA, … | Other equipment-type codes present in the fleet-wide database (e.g., TX appears 47 times, EM 40, CD 25, PZ 24, SW 22, RX 22). Their meanings are not stated in the provided files and are not covered by the 5 hero cases — confirm directly with the data owner if the team needs to reference them. |

Discipline and PIC (RCA) — who is responsible:

| Field | Meaning |
| --- | --- |
| ROT | Rotating Equipment discipline (pumps, compressors, blowers). |
| STA | Static Equipment discipline (heat exchangers, vessels, piping). |
| ELE | Electrical discipline (motors, switchgear). |
| INS | Instrument discipline. |
| PIC (RCA) codes (e.g., REL-05, ROT-01, STA-02, ELE-01) | Each is a discipline prefix — REL (Reliability), ROT, STA, ELE, INS, OPS (Operations) — plus a person/role number, identifying who owns the RCA for that incident. |

| Note on Pot. Loss / • For the 5 hero cases specifically, Pot. Loss is exactly 30% of Act. Loss in every case (e.g., KO-3201: $1,584.00k Act. Loss → $475.20k Pot. Loss). Across the full 380-row database, however, this ratio does not hold — many rows have Pot. Loss = 0, and others have ratios far above or below 30%. Treat the 30% pattern as specific to these 5 curated hero cases, not as a documented formula for the whole dataset. |
| --- |

### 4. RCA & CAPA/PAA

| Function | Verified root-cause investigation reports (Root Cause Analysis) together with corrective and pro-active action plans (Corrective & Pro-Active Action). The narrative layer that ties the other three datasets together. |
| --- | --- |
| Grain & number of files | 1 PDF report per incident. 5 reports are available — one per hero-case asset (PU-2101B, KO-3201, PM-4405B, HE-3301, BL-5702). |
| Period | Specific to each asset's incident date. |
| Can be concluded | Root causes that have been verified in a structured way (not initial guesses); specific actions with an owner and status. |
| Cannot be concluded | Automatic generalization to all 380 incidents in the Incident Database — full RCA reports are only available for these 5 cases; every incident has its own unique context and root cause. |

Field Glossary — recurring sections of each report

| Field | Meaning |
| --- | --- |
| AR Number | Same unique ID as the Incident Database's “AR No.” column — the key that links the two datasets. |
| Tag / Plant | Equipment tag and plant code, matching the Incident Database. |
| Date Occurrence | Date of the failure event. |
| Pre-Risk (Roman numeral + score) | Same risk tier and score as the Incident Database's Pre-Risk / Risk Score columns. |
| PIC (RCA) | The person/role responsible for conducting this RCA — same code scheme as the Incident Database. |
| AR Type | Classification of the report. All 5 hero-case reports share the same observed value: “OPEDR (Operation) — Uptime”, i.e., an Operations-related report whose primary impact is uptime loss. |
| Severity | A qualitative severity label (e.g., Major, Catastrophic, Moderate) — a qualitative counterpart to the numeric Pre-Risk score, not identical to the Pre-Risk tier itself. |
| Downtime / Loss | Same definitions as the Incident Database's Downtime (hrs) and Act. Loss (k US$) columns. |
| Problem Statement | A 1–2 sentence description of what happened. |
| Chronology of Events | A timestamped sequence of events, from the first symptom to restoration of normal operation. |
| Impact Summary (4W) | A structured What / When / Scope / Uptime Loss summary framework. |
| Parameter Verification (4P) | Checks up to 5 process parameters (labeled P1–P5) against their design spec; each is flagged G (meets standard) or NG (Not Good — a problem). |
| 4M+1E Verification | Checks Man / Machine / Method / Material / Environment root-cause categories (labeled X1–X4); flagged G/NG the same way as 4P. |
| Root Cause | The final, verified root-cause statement, synthesizing the 4P and 4M+1E findings into one sentence. |
| RCA Matrix Priority | An impact-vs-control 2×2 chart used to decide which root-cause codes (e.g., X1, P2) get addressed first — high-impact, low-control items are prioritized. |
| Corrective & Pro-Active Action (CAPAA) table | Columns: RC (which root-cause code this action addresses) \| Action description \| Plan Date \| PIC \| Status (Open / In Progress / Closed). |
| Pro-Active Action | Same table structure as CAPAA, but for rolling the fix out to similar or sister equipment (e.g., applying a KO-3201 fix to KO-3202/3203). |
| Preventive & Risk Analysis | Additional preventive actions, plus a risk analysis of the corrective action itself — what new risk it could introduce, and the countermeasure for that new risk. |
| PM Schedule Established | The new or revised preventive-maintenance tasks and their interval, created as a direct result of this RCA. |

### 5. Alert and Action Tracking

Unlike the four groups above, Alert and Action Tracking is not a raw dataset directly available in the Project — it is a layer the team needs to design and build by combining signals from the other datasets. Some of the raw material already available to build it:

Health Status (NORMAL/ALARM/TRIP) in Equipment Performance can serve as a condition-based alert trigger.

The status field in the CAPA/PAA table of each RCA report (Open/In Progress/Closed) can serve as the basis for tracking the progress of individual actions.

Overall Status in the Incident Database (NEW REGISTERED → RCA PROCESS → CA/PA EXECUTION → MONITORING RESULT → RISK CLOSED / RISK CANCELED) can serve as the basis for tracking the overall incident lifecycle.

| Note on “Downtime Data” / • The Case Book for Case 2 mentions “Downtime Data” as one of the baseline data sources. No separate downtime time-series dataset is available. Downtime information is available in the Incident Database, in the Performance Summary of Equipment Performance, and in the five RCA & CAPA/PAA reports, which also record production loss and estimated loss. / • If the team wants to cite this source in the deck, it should be explained that downtime is derived from these three sources above, not from a single standalone downtime dataset file. |
| --- |

### 5. Explanation of the Five RCA Cases

The five cases below are the incidents with complete granular data (hourly Production Data + weekly Equipment Performance + verified RCA & CAPA/PAA reports). All five become the “hero cases” best suited as working examples of AI Root-Cause Indication and Similar-Incident Retrieval in the prototype, because only these five assets have this complete a data trail.

#### Comparison Summary

| Asset | Incident | Date | Downtime | Act. Loss | Total Loss | Pre-Risk |
| --- | --- | --- | --- | --- | --- | --- |
| PU-2101B | Mechanical seal leakage | 12 Mar 2026 | 18.5 h | $226.44k | $294.37k | III (200) |
| KO-3201 | High radial vibration trip (bearing distress) | 29 Apr 2026 | 32.0 h | $1,584.00k | $2,059.20k | II (4000) |
| PM-4405B | Motor bearing failure (overheating) | 8 Jul 2026 | 8.0 h | $112.00k | $145.60k | III (200) |
| HE-3301 | High fouling — duty loss & high dP | 21 May 2026 | 12.0 h | $183.60k | $238.68k | III (400) |
| BL-5702 | High vibration (coupling misalignment) | 17 Jun 2026 | 14.0 h | $478.80k | $622.44k | III (400) |

Act. Loss = actual loss (from the RCA report); Total Loss = Act. Loss + Pot. Loss (potential loss), per the Incident Database. Total downtime across these five cases is 84.5 hours (≈ 3.7% of the total downtime across all 380 incidents). Total Act. Loss across the five is ≈ $2.58 million (≈ 4.2% of total Act. Loss across all incidents); if Pot. Loss is included, the Total Loss across the five is ≈ $3.36 million (≈ 5.0% of the $67.19 million Total Loss across all incidents). All five incidents also share the same “CA/PA EXECUTION” status in the Incident Database — their corrective actions are not yet fully closed.

PU-2101B — Feed Charge Pump (Resin Plant / ARP)

| Initial symptoms | 11 Mar: the field operator noticed a minor seal weep on PU-2101B during a routine round. 12 Mar 02:15: the seal-flush low-flow alarm annunciated, a visible feed seal leak appeared with low suction pressure; the pump auto-tripped on low discharge pressure. |
| --- | --- |
| Verified root cause | Premature mechanical seal failure caused by intermittent dry-running: suction cavitation during feed swings reduced NPSH, and seal-flush flow dropped below the 6 L/min minimum, with no interlock to protect the seal. |
| Downtime & losses | 18.5 hours downtime → 251.6 tons of production loss → $226.44k (Total Loss $294.37k). Pre-Risk III (score 200). |
| Corrective/preventive actions | Install a seal-flush flow switch with a DCS alarm; add a low-NPSH/loss-of-flush trip interlock; revise the feed-swing SOP (cap the ramp rate at 1 T/H per minute); add the seal-flush system (Plan 11) to the PM check-sheet; roll out the flow switch to the spare pump PU-2101A. |
| Lesson for dashboard design | A leading-indicator parameter (seal-flush flow vs. the minimum spec) should be monitored in real time on the dashboard, not only reacted to when the final alarm fires — the worsening seal MTBF trend (26 → 9 months over 3 cycles) is also worth displaying as a long-term degradation signal. |

KO-3201 — Cracked Gas Compressor (Cracker Unit / ZCU)

| Initial symptoms | 27 Apr: drive-end (DE) radial vibration rose from 28 to 52 microns over 5 days. 29 Apr 06:40: vibration reached the high-high setpoint (75 microns) and the machinery protection system tripped the compressor. |
| --- | --- |
| Verified root cause | Journal-bearing babbitt distress caused by degraded oil-film strength from water ingress via a leaking lube-oil cooler tube, undetected due to the absence of online water-in-oil monitoring (only a weekly grab sample was taken). |
| Downtime & losses | 32.0 hours downtime → 1,760 tons of production loss → $1,584.00k (Total Loss $2,059.20k). Pre-Risk II (score 4000) — the largest loss among the five cases. |
| Corrective/preventive actions | Repair the leaking lube-oil cooler tube; install an online water-in-oil sensor on the KO-3201 lube system; tighten the vibration alert to 45 microns and shorten the trend-review cycle; retube the cooler at the next turnaround; roll out water-in-oil monitoring to KO-3202/3203. |
| Lesson for dashboard design | The combination of a vibration trend plus a contaminant parameter (water-in-oil) is a strong early-warning pattern. An asset with “High” criticality and the largest loss like this one is well suited as the main hero case for the prototype (see Section 9). |

PM-4405B — Cooling Water Pump, Motor Driven (Utility Plant / NUP)

| Initial symptoms | 6 Jul: motor DE bearing temperature rose from 68 to 84°C. 8 Jul 13:20: the high-bearing-temperature alarm annunciated, and the motor tripped on over-temperature. |
| --- | --- |
| Verified root cause | Motor drive-end bearing failure caused by grease degradation from a fixed 12-month re-lubrication interval that was not risk-based, undetected because bearing temperature was not trended in the CMMS. |
| Downtime & losses | 8.0 hours downtime → 160 tons of production loss → $112.00k. Pre-Risk III (score 200) — the smallest loss among the five cases. |
| Corrective/preventive actions | Change the re-lubrication interval to risk-based (every 4 months); add bearing-temperature trending and alerting to the CMMS; add PM-4405B/C to the monthly vibration & thermography route; apply risk-based re-greasing to all cooling-water pump motors. |
| Lesson for dashboard design | Not every root cause originates from a real-time sensor — non-sensor maintenance parameters such as the PM/re-lubrication interval also need to be visualized and linked to failure risk on the dashboard. |

HE-3301 — Feed/Effluent Heat Exchanger (Cracker Unit / ZCU)

| Initial symptoms | 18 May: tube-side dP rose from 0.4 to 0.9 bar and the cold-outlet temperature fell over several days. 21 May: preheat duty dropped ≈ 35% below design, and the unit rate was cut to protect the downstream section. |
| --- | --- |
| Verified root cause | Accelerated tube-side coke/polymer fouling driven by feed heavy-ends above design (2.4% vs. the < 1.5% spec), allowed to progress because there was no dP-based cleaning trigger and no fouling KPI on the dashboard. |
| Downtime & losses | 12.0 hours downtime → 216 tons of production loss → $183.60k. Pre-Risk III (score 400). |
| Corrective/preventive actions | Add a dP-based cleaning trigger and alarm for HE-3301; tighten feed heavy-ends control and filtration; add a fouling factor & duty KPI to the reliability dashboard; apply the dP-trigger logic to the parallel exchangers HE-3302/3303. |
| Lesson for dashboard design | Unmonitored process KPIs (dP, duty %) can become a blind spot. The dashboard needs automatic thresholds to trigger action, not only a time-based schedule. |

BL-5702 — Product Blower (Polymer Plant / OPP)

| Initial symptoms | 15 Jun: vibration rose from 4.2 to 8.5 mm/s with a rising 2X harmonic over 2 days. 17 Jun 04:30: vibration reached the 11 mm/s alarm, and the blower was stopped to prevent further damage. |
| --- | --- |
| Verified root cause | High vibration from coupling misalignment, aggravated by soft-foot and an over-aged elastomer coupling element, undetected because periodic alignment/soft-foot checks were not part of the routine PM and the vibration route interval (monthly) was too long to catch the fast 2-day trend. |
| Downtime & losses | 14.0 hours downtime → 532 tons of production loss → $478.80k. Pre-Risk III (score 400). |
| Corrective/preventive actions | Add periodic laser alignment & soft-foot checks to the PM; track coupling-element age and replace at 12 months; shorten the BL-5702 vibration route to weekly (using a wireless vibration sensor); roll out alignment checks to all Class-A blowers in OPP. |
| Lesson for dashboard design | A monitoring interval that is too infrequent can miss a fast-developing trend. The dashboard should ideally support risk-based, adaptive monitoring frequency, not a uniform interval for every asset. |

### 6. Key Data-Driven Insights

This section clearly separates the insights that are genuinely supported by numbers from the dataset (data facts) from the ones that are pattern readings / possible-cause interpretations that still need to be validated by the team (assumptions/interpretations).

A. Early Warning — supported by data

Fact: across all five RCA cases, Equipment Performance shows a number of ALARM-status readings before the TRIP occurred within the 26-week window — PU-2101B 6 ALARMs, KO-3201 11 ALARMs, PM-4405B 6 ALARMs, HE-3301 10 ALARMs, BL-5702 15 ALARMs (each out of 26 weekly readings, with 1 TRIP).

Fact: in all 5 RCA reports, the event chronology records a measurably worsening parameter trend (vibration, bearing temperature, dP, water content) over a range of 2 days to several days before the trip/shutdown.

Interpretation (needs team validation): this ALARM-before-TRIP pattern suggests that a threshold-based early-warning feature on the dashboard could potentially give reaction time before a failure — but the realistic size of that “reaction time” needs to be calculated by the team per asset, not assumed to be the same across all cases.

B. Risk-Based Alert — supported by data

Fact: the Pre-Risk distribution in the Incident Database (380 incidents) is IV = 201, III = 149, II = 29, I = 1.

Fact: of the 5 hero cases, KO-3201 is labeled Pre-Risk II yet has the largest loss ($1,584k Act. Loss / $2,059k Total Loss) compared with the three cases labeled Pre-Risk III.

Interpretation (needs team validation): the Pre-Risk label alone is not necessarily proportional to the actual loss in every case, so the Alert Prioritization Engine should consider a combination of Pre-Risk and estimated impact (downtime/loss), not the risk score alone. This is an observation from 5 samples, not a statistical conclusion across all 380 incidents.

C. Similar-Incident Retrieval — supported by data

Fact: the F Mechanism column in the Incident Database shows failure mechanisms that recur across plants — Leakage 101 cases, High Vibration 57, Worn Out 47, Malfunction 25, Low Performance 22, Crack 20, Fouling 20, Error 20, Loose 18, Stuck 15 (out of 380 incidents).

Interpretation (needs team validation): grouping by F Mechanism, Eq. Type, and Component could potentially serve as the basis for similar-incident search, but retrieval quality depends on how consistently these categories are filled in across the 380 rows — the data quality should be checked before use in the prototype.

D. Action Tracking — supported by data

Fact: Overall Status in the Incident Database is split into 6 stages — NEW REGISTERED 20, RCA PROCESS 71, CA/PA EXECUTION 92, MONITORING RESULT 37, RISK CLOSED 113, RISK CANCELED 47 (total 380).

Fact: NEW REGISTERED (20) + RCA PROCESS (71) + CA/PA EXECUTION (92) = 183 incidents (≈ 48.2% of 380) are still at an active handling stage — not yet at the monitoring or closure stage.

Fact: if MONITORING RESULT (37) is also counted as not yet final (since it is still awaiting confirmation of action effectiveness), the total becomes 220 incidents (≈ 57.9% of 380) that are not yet RISK CLOSED or RISK CANCELED — including all five hero cases, which are all still at CA/PA EXECUTION status.

Interpretation (needs team validation): the proportion of incidents still “in progress” reinforces the real need for centralized Action Tracking on the dashboard — but the team should keep in mind that this status is an incident status, not the status of each individual action (see Section 7).

| Principles the team is holding to / • All the figures above can be re-verified directly from the Incident Database.xlsx file and the five paired Equipment Performance / Production Data / RCA PDF files. / • Sections marked “Interpretation” are the team's reading, not numbers from the dataset — they should be presented as working hypotheses in the deck, not as absolute facts. / • For any claim covering all 380 incidents, the team should compute it directly from the Incident Database rather than extrapolating from the 5 hero cases alone. |
| --- |

### 7. Data Limitations and Design Principles

To keep the team's proposal realistic and free of overclaiming, the data limitations below should be stated openly, along with their design implications.

| Limitation | Explanation | Design implication |
| --- | --- | --- |
| Granular data is available for only 5 assets | Production Data (hourly) and Equipment Performance (weekly) are only available for the 5 hero-case assets. The Incident Database covers 380 incidents across 379 tags/12 plants, but only at a summary level (no time-series). | The prototype should be demonstrated with these 5 assets as a proof of concept, with an explicit statement that scaling up to the whole fleet requires additional data sources. |
| AI provides an indication, not a final decision | AI Root-Cause Indication is designed to produce a probable root cause based on patterns and historical data — it is not a substitute for the formal RCA process (4P and 4M+1E) carried out by the reliability team, as seen in the five RCA reports in Section 5. | Present the AI output as an “indication/candidate root cause” with a confidence level, not as a final conclusion that gets executed automatically. |
| Actions require human verification | The action status on the CAPA/PAA table (Open/In Progress/Closed) in each RCA report is managed manually by the PIC (person in charge), not updated automatically by a system. | Action Tracking on the dashboard needs a human-in-the-loop approval/verification flow before an action is marked complete, not just an automatic recommendation. |
| No energy or emissions data yet | Although CALIBER 2026's grand theme and the Single Pane of Glass use case mention energy and emissions, no energy or emissions dataset was found in this Project. | If an energy/emissions module is shown in the prototype, state explicitly that it is dummy/illustrative data or a proposal for future integration — do not present it as if it came from an available dataset. |
| Incident status ≠ action status | Overall Status in the Incident Database (NEW REGISTERED → RCA PROCESS → CA/PA EXECUTION → MONITORING RESULT → RISK CLOSED / RISK CANCELED) describes the overall lifecycle stage of one incident. The status on the CAPA/PAA table in each RCA report (Open/In Progress/Closed) describes the progress of one individual action. One incident at “CA/PA EXECUTION” status can have several actions with different statuses. | Design two separate entities/status fields in the dashboard data model: Incident Status and Action Status — do not merge them into a single field. |

### 8. Work Plan for the Three-Person Team

The initial work division below is a starting point that the team can adjust to fit each member's interests and strengths. Name placeholders can be replaced once the team agrees on the final split.

| Member | Focus Area | Main Output |
| --- | --- | --- |
| Member 1 / [Member 1 Name] | Business problem, business impact, KPIs, and storytelling | Business problem statement (Section 2), list of KPIs/success metrics, Business Impact narrative for the deck, presentation storytelling flow. |
| Member 2 / [Member 2 Name] | Data, AI logic, root-cause indication, and alert prioritization | Data model from the five datasets (Section 4), AI Root-Cause Indication & Similar-Incident Retrieval logic, Alert Prioritization Engine design. |
| Member 3 / [Member 3 Name] | Prototype, user flow, dashboard design, and demo video | Wireframe/prototype (Figma or HTML), user flow for Single Pane of Glass & Action Tracking, production of the 3-minute demo video. |

#### How the Team Collaborates

Weekly sync-ups (or more frequently as the deadline nears) to align progress across all three areas, using this document as the shared reference.

Member 2 shares the data-mapping and AI-logic results with Member 1 (for data-based Business Impact claims, per Section 6) and with Member 3 (for a prototype design that is consistent with the data actually available).

Member 1 makes sure every business-impact claim in the deck can be traced back to the figures in Sections 5–6 of this document, not new, unverified numbers.

Member 3 involves Members 1 and 2 when deciding which features appear in the prototype, so the prototype does not promise capabilities the data does not support (see Section 7).

Use one shared file/board (e.g., Figma, Google Slides, or a spreadsheet) to track design decisions, so no member ends up working from a different version of the solution.

#### Outputs That Must Be Agreed Together

Selection of the main hero case for the deck narrative and prototype (see the recommendation in Section 9).

Final wording of the three answers to the Case 2 Key Questions (Section 1) — since the answers involve both the data/AI side (Member 2) and the business side (Member 1).

The list of core features that actually go into the prototype and demo video, with honest data limitations (Section 7).

The KPIs/success metrics used in the Business Impact slide, so they stay consistent between the narrative (Member 1) and the technical capability demonstrated (Members 2 & 3).

### 9. Next Steps

The practical work sequence below helps the team move from a shared understanding (this document) toward the competition deck, without jumping straight into design before the fundamentals are clear.

| Reminder / • This document is a shared-understanding resource, not the final proposal or the competition deck — the proposal and deck are prepared separately after the steps above are complete. / • Preliminary Stage proposal submission deadline: 4 October 2026, 23:59 WIB. Allow time for internal team and supervisor review before the deadline. |
| --- |

### List of Source Files

The entire content of this document was prepared based on the following files in the “Caliber 2026” Project:

Case & Registration Documents

The Case - CALIBER 2026 1.pdf

Booklet CALIBER 2026 - Registration Extended.pdf

Data Set Explanation for Case 2 Intelligence Manufacturing.pptx

RCA & CAPA/PAA Reports

RCA1 - PU-2101B Mechanical Seal Leakage.pdf

RCA2 - KO-3201 High Radial Vibration Trip.pdf

RCA3 - PM-4405B Motor Bearing Failure.pdf

RCA4 - HE-3301 High Fouling — Duty Loss & High dP.pdf

RCA5 - BL-5702 High Vibration.pdf

Equipment Performance Dataset

Equipment Performance - RCA1 PU-2101B.xlsx

Equipment Performance - RCA2 KO-3201.xlsx

Equipment Performance - RCA3 PM-4405B.xlsx

Equipment Performance - RCA4 HE-3301.xlsx

Equipment Performance - RCA5 BL-5702.xlsx

Production Data Dataset

Production Data - RCA1 PU-2101B.xlsx

Production Data - RCA2 KO-3201.xlsx

Production Data - RCA3 PM-4405B.xlsx

Production Data - RCA4 HE-3301.xlsx

Production Data - RCA5 BL-5702.xlsx

Incident Dataset

Incident Database.xlsx

This briefing document was prepared for internal team use on 21 September 2026, as a shared foundation of understanding before the team designs the solution and builds the CALIBER 2026 competition deck.

> **Source fidelity note:** In the uploaded Team Briefing, Section 9, “Next Steps,” contains the introductory explanation followed by numbered placeholders `7.` through `12.` but the corresponding step descriptions are not present in the extracted document content. They are therefore not reconstructed or guessed here.

---

# Appendix C. Complete Source, The Case, CALIBER 2026

## Source B. The Case, CALIBER 2026

> Source file: `The Case - CALIBER 2026.pdf`. The section below preserves the substantive text page by page.

### Page 1

CALIBER 2026
Future -
Ready Operational Excellence:
Knowledge, Reliability, and Smart Manufacturing
Company Background
PT Chandra Asri Pacific Tbk (Chandra Asri Group) is an energy,
chemical, and infrastructure solutions company in Southeast
Asia . Operating complex and asset
-
intensive petrochemical
facilities,
the
Company
relies
on
technical
knowledge,
equipment
reliability, supply -
chain readiness, and efficient resource
utilization
to
maintain
safe
and
continuous
operations .
As its plants, systems, and operational data continue to grow,
the Company is strengthening its digital transformation agenda
by integrating data, analytics, and artificial intelligence into
manufacturing processes . This transformation is intended to
support faster decision -
making, improve operational visibility,
preserve critical plant knowledge, and enhance collaboration
across Production, Maintenance, Reliability, Warehouse,
Procurement, Energy, and Health, Safety, Environment (HSE)
functions .
For eligibility, registration, key dates, and contact information, please refer to the
official CALIBER 2026 Booklet. This casebook covers case content and submission only.

### Page 2

Executive
Summary
Future -
Ready Operational Excellence : Knowledge,
Reliability, and Smart Manufacturing grand theme focuses
on applying artificial intelligence to address critical
manufacturing
challenges
within
a
petrochemical
environment .
Participants are expected to propose practical and scalable AI
solutions that transform fragmented operational data into
actionable insight . The proposed solutions may support
technical knowledge retention, predictive maintenance, spare -
part inventory optimization, energy and emissions monitoring,
production forecasting, anomaly detection, and cross -
functional
decision -
making .
The solutions should integrate relevant plant and enterprise
data, provide transparent and traceable recommendations, and
consider human oversight, data security, system reliability, and
measurable business impact
. Through this grand theme, the
Company aims to accelerate the development of safer, more
reliable,
efficient,
and
intelligent
manufacturing
operations .

### Page 3

Please choose only one of the two use cases provided in the
following section and build your solution based on it.

### Page 4

Manufacturing Knowledge Hub
(AI - Powered Knowledge Integration)
CASE 1
Topic
This case focuses on reducing improper execution risk caused by
scattered knowledge source, missing tacit knowledge, difficulty in
finding trusted information, and disconnected operational data.
Background
In a chemical manufacturing plant, engineers need to make quick and
accurate decisions during start -
up, troubleshooting, maintenance
activities, and abnormal operating conditions. However, the
information they need is often spread across different sources: SOPs
are stored in one system, datasheets in another, P&IDs in document
folders, maintenance logs in separate records, and real -
time operating
data in plant systems.
Because these knowledge sources are not connected, engineers may
spend too much time searching for trusted information or asking
experienced personnel for confirmation. In some cases, missing tacit
knowledge, outdated documents, or incomplete context may cause
teams to misinterpret procedures or fail to follow the correct execution
steps.
As a result, plant operations may face longer troubleshooting time,
repeated engineering rework, higher safety risk, delayed start -
up, and
inconsistent decision -
making across Process, Maintenance,
Engineering, Operation, and HSE functions.

### Page 5

Problem Statement
Participants are challenged to design an AI -
enabled Manufacturing
Knowledge Hub that scattered plant knowledge from SOPs,
datasheets, P&IDs, EDMS, AIMS, maintenance logs, incident reports,
and real -
time operational data into one trusted, structured, and
traceable knowledge ecosystem. The solution should help engineers
find verified information faster, reduce improper execution, support
troubleshooting, and improve reliability, safety, and cross -
functional
decision -
making.
Expected Solution
• Industrial Data Ops: Builds a structured data and metadata
foundation to connect SOPs, P&IDs, datasheets, maintenance logs,
and asset data.
• AI Document Ingestion: Converts scattered technical documents
into a structured, searchable, and AI -
ready knowledge base.
• Q&A Assistant & Semantic Search: Develops an AI assistant that
helps engineers find trusted technical information through natural -
language questions and context -
based search.
• Traceable Answer with Source: Provides AI -
generated answers with
clear document sources, version references, approval status, and
confidence indicators.
• EDMS, AIMS, and Digital Twin Integration: Connects to knowledge
hub with EDMS, AIMS, and Digital Twin to provide technical
information based on asset and operational context.
• Failure Memory System and Recommendation: Retrieves past
failures, RCA, lessons learned, and recommended actions to
support faster troubleshooting and more reliable execution.

### Page 6

Key Questions (Scope of Work)
Participants must address the following question in the deck , either
within the proposed solution or business impact section.
1. How can the Company build a structured Industrial Data Ops
foundation to connect scattered plant knowledge sources?
• Main Focus: Build connected knowledge foundation.
2. How can AI help engineers find trusted technical information
faster and reduce the risk of improper execution?
• Main Focus: Improve search, Q&A, and answer verification.
3. How can the Manufacturing Knowledge Hub be integrated with
operational systems to support reliability, troubleshooting, and
continuous improvement?
• Main Focus: Active knowledge for operational decision
support.

### Page 7

Baseline Data
You can retrieve the baseline data from this link:
https://bit.ly/ CALIBER2026 -
TheCase
Besides the baseline data, participants may propose additional
knowledge of data sources beyond the provided baseline. However,
every additional data source should be supported by a clear business
justification. A well -
justified, high -
quality data architecture is preferred
over simply integrating more data.
Data Source Purpose
SOP & Technical
Document (Datasheets)
Provides procedures and technical
reference
P&IDs Data Understand as -
built equipment, pipping
systems, and instrumentation
Maintenance History Capture incidents, root causes, and
corrective actions
Tacit Knowledge Capture SME experience and OPL data

### Page 8

Topic
Manufacturing performance data is fragmented across multiple
dashboards, systems, and reports, making it difficult to monitor plant
performance, identify root causes, prioritize alerts, and track follow -
up
actions.
Background
In a chemical manufacturing plant, teams from Operations, Production,
Energy, Maintenance, HSE, and Management use multiple dashboards
and reports to monitor plant performance. However, each function
often relies on different systems, KPI definitions, data formats, and
reporting timelines. When an issues occurs, such as abnormal energy
consumption, production loss, emission deviation, or equipment
downtime, teams may spend significant time validating data,
comparing reports, and aligning interpretations before deciding the
next action.
This fragmented condition results in slower, more reactive decision -
making. It also creates difficulties in identifying root causes, prioritizing
critical alerts, recommending corrective actions, and tracking whether
follow
-
up actions have been completed. As a result, potential
optimization opportunities may be missed, and operational reliability
can be affected.
CASE 2
Intelligence Manufacturing (Unified Dashboard, AI Insight,
Root Cause Analysis, Follow - up Action Recommendation)

### Page 9

Problem Statement
Participants are challenged to design an Intelligent Manufacturing
Dashboard that integrates fragmented manufacturing data into a single
pane of glass for decision -
making.
The solution should connect data sources, display critical KPIs, identify
operational problems, indicate possible root cause, prioritize alerts,
and guide follow -
up actions. The objective is to reduce time spent on
data validation, accelerate problem -
solving, improve operational
efficiency, reduce downtime, and strengthen reliability and safety
across functions.
Expected Solution
• Rationalize & Integrate Dashboard: Consolidates redundant
dashboards and connects key manufacturing data sources into one
governed view.
• Single Pane of Glass: Provides one integrated dashboard to monitor
energy, production, emission, downtime, and operational
performance.
• Root Cause Analysis Support: Helps identify probable causes of
operational issues using problem history, KPI deviations, and data
patterns.
• Follow
-
up Action Recommendation: Converts alerts and insights
into prioritized actions with owner, guidance, and progress tracking.

### Page 10

Key Questions (Scope of Work)
Participants must address the following questions in the deck ,
either within the proposed solution or business impact section.
1. How can the Company rationalize fragmented dashboards and
map manufacturing data sources into one governed data
foundation?
• Main Focus : Reduce dashboard redundancy and create
consistent KPI/data mapping across functions.
• Key Capabilities: Data Source Mapping.
2. How can the Company build a single pane of glass
that provides executive visibility of manufacturing performance?
• Main Focus : Provide one integrated dashboard to
monitor operational performance.
• Key Capabilities: Executive Level Dashboard.
• Use Cases: Energy Forecasting, Similar -
incident Retrieval, AI -
based Root Cause Indication.
3. How can AI help identify probable root causes behind
operational problems and translate insights into prioritized
follow - up actions with clear ownership and tracking?
• Main Focus : Support faster problem -
solving by connecting
issue detection, prioritized alerts, recommended actions.
• Key Capabilities: Problem Tank, Root Cause Indication, Alert
Prioritization Engine, Action Tracking, and Action Guidance.

### Page 11

Baseline Data
You can retrieve the baseline data from this link:
https://bit.ly/ CALIBER2026 -
TheCase
Besides the baseline data, participants may propose additional
knowledge of data sources beyond the provided baseline. However,
every additional data source should be supported by a clear business
justification. A well -
justified, high -
quality data architecture is preferred
over simply integrating more data.
Data Source Purpose
Production Data Monitor production output and
performance
Incident Database Trace and analyze past incidents
Equipment Performance Monitor equipment condition and
performance trends
Downtime Data Track downtime causes and duration

### Page 12

1. Do we need to work on both use cases?
No, please choose only one case to solve.
2. Can we combine ideas from both cases?
No. Select just one of the two cases; while extended solutions to the problem may be
developed for whichever case you pick, your attention should remain on that particular case.
3. Are the "Key Questions" listed under each case mandatory to answer individually?
Yes, you are required to answer all the key questions in the proposed solution or business
impact section.
4. Will we be provided with real datasets, or should we use assumed data?
All datasets required for the Preliminary Stage are included in this Case Book. You can use
ot generate dummy data that are relevant to your solution or with the provided all dataset.
You may also supplement your analysis with publicly available data or reasonable
assumptions where necessary.
5. Can we use external or publicly available datasets in addition to the baseline data
provided?
Yes. You may use additional external or publicly available data sources beyond the baseline
data provided, provided that the relevance and business value of each data source are
clearly justified in the presentation deck.
6. What file formats and size limits apply to the prototype, video, and presentation deck?
For the Preliminary Stage, all 3 (three) materials combined should be no bigger than 10 MB.
Submission format for Final Stage will be informed during the event.
7. What language should be used for the presentation deck and pitch?
All materials should be written and delivered in English.
8. Can we use generative AI tools as part of our solution development process?
The use of AI tools is permitted, provided they are used lawfully and in accordance with
their applicable terms and conditions and privacy notices. All AI -
generated outputs must be
validated, iterated, and evaluated to ensure the quality, accuracy, and reliability of the
resulting technology solutions before use or implementation.
9. Can we update or replace our submission after it has been submitted?
No. Only the first submission submitted by your team will be accepted and evaluated.
10. What happens if we fail to submit one of the required deliverables?
Your team will be disqualified and cannot continue to the next stage.
FAQ (Case Book)

### Page 13

Chandra Asri Group
CALIBER 2026
Committee
E
-
mail : caliber. 2026 @capcx.com
PT Chandra Asri Pacific Tbk
Head Office
Wisma Barito Pacific Tower A, 5th Floor
Jl. Let. Jend
. S. Parman Kav. 62 -
63
Jakarta 11410, Indonesia
Phone: (62 -
21) 530 7950
Fax: (62 -
21) 530 8930

## Source C. Booklet, CALIBER 2026, Registration Extended

> Source file: `Booklet CALIBER 2026 - Registration Extended.pdf`. The section below preserves the substantive text page by page.

### Page 1

“Future-Ready Operational Excellence:
Knowledge, Reliability, and Smart Manufacturing”
CHANDRA ASRI LIMITLESS INNOVATION &
BUSINESS STRATEGY CHALLENGE 2026

### Page 2

Table of Contents
Introduction
Background
07
03
05
Table of Contents 02
Submission Format
07
09
Business Proposal Competition 07
Evaluation Criteria
Rules & Regulations
10
11
14
FAQ 15
Grand Prizes 16
Timeline 17
6
Contact Person 12
Terms & Conditions 13
How to Register 12

### Page 3

INTRODUCTION
PT Chandra Asri Pacific Tbk (Chandra Asri Group) is a
Southeast Asia’s leading energy, chemical, and infrastructure
solutions company, operating integrated regional platforms
based
in
Indonesia
and
Singapore .
Our Indonesian assets include the first and largest integrated
petrochemical complex in Indonesia, the upcoming Chlor -
Alkali and Ethylene Dichloride plant, and infrastructure
solutions which cover electricity, water, logistics, and ports &
storage ;
affirming
our
contribution
as
one
of
the
pillars
of
the
national industry . Meanwhile, our facilities on Pulau Bukom
and Pulau Jurong serve as integrated petrochemical and
refining
production
hubs
in
Singapore .
We are dedicated to sustainable collaboration and
innovation,
serving
as
Indonesia’s
Growth
Partner
.
Chandra Asri Group
Find out more about Chandra Asri Group
on
www.chandra -
asri.
com.

### Page 4

INTRODUCTION
CALIBER (Chandra Asri Limitless Innovation and Business
Strategy Challenge) is the annual competition hosted by
Chandra Asri Group, designed to provide a platform for
emerging talents, particularly students, to showcase their
analytical prowess, strategic thinking, and problem -
solving
abilities
.
This year’s theme, “Future
-
Ready Operational Excellence :
Knowledge, Reliability, and Smart Manufacturing,” challenges
participants to develop a business proposal that leverages
Artificial Intelligence (AI) to tackle critical manufacturing
challenges
across
Chandra
Asri
Group’s
chemical
facilities
.
CALIBER 2026

### Page 5

BACKGROUND
PT Chandra Asri Pacific Tbk (Chandra Asri Group) as an
energy, chemical, and infrastructure solutions company in
Southeast Asia has been continuously improved its
operations
to
respond
to
the
industry’s
dynamic .
Operating complex and asset
-
intensive petrochemical
facilities in Indonesia, the Company relies on technical
knowledge, equipment reliability, supply -
chain readiness,
and efficient resource utilization to maintain safe and
continuous
operations .
As its plants, systems, and operational data continue to
grow, the Company is strengthening its digital
transformation agenda by integrating data, analytics, and
artificial intelligence into manufacturing processes . This
transformation is intended to support faster decision -
making, improve operational visibility, preserve critical
plant knowledge, and enhance collaboration across
functions
within
the
Company .

### Page 6

Future
-
Ready Manufacturing Operations : Knowledge,
Reliability, and Energy Intelligence is our grand theme,
focusing
on
applying
artificial
intelligence
to
address
critical
manufacturing
challenges
in
a
petrochemical
environment .
Participants are expected to design scalable, technology -
driven solutions, including AI, that transform fragmented
data or process into actionable insights . The proposed
solutions may support technical knowledge retention,
predictive maintenance, spare -
part inventory optimization,
energy and emissions monitoring, production forecasting,
anomaly
detection,
and
cross -
functional
decision -
making .
The
solutions should
integrate
relevant
plant and
enterprise
data, provide transparent and traceable recommendations,
and consider human oversight, data security, system
reliability, and measurable business impact . Through this
grand theme, the Company aims to accelerate the
development of safer, more reliable, efficient, and
intelligent
manufacturing
operations .

### Page 7

BUSINESS CASE
COMPETITION
The
competition
consists
of
two
stages :
the
Preliminary
Stage
and
the
Final
Stage .
Preliminary Stage : Business
Proposal
Submission
Participants are required to select one of the two available use cases
and
develop
a
business
proposal
outlining
their
proposed
solution
.
Detailed submission requirements and formatting guidelines are
provided
in
the
following
section
(see
pg .
9
-
10
)
.
Proposal must be submitted by 4 October 2026 at 23.59 WIB at the
latest. Link to upload the proposal will be sent by e -
mail to all
registrants.
Case 1: Manufacturing Knowledge Hub (AI - Powered Knowledge
Integration)
This use case focuses on reducing improper execution risk caused by
scattered knowledge sources, missing tacit knowledge, difficulty in
finding trusted information, and disconnected operational data.
Case 2: Manufacturing Intelligence (Unified Dashboard, AI
Insight, Root Cause Analysis, Follow - up Action Recommendation)
This use case focuses on addressing the challenges of fragmented
manufacturing performance data across multiple dashboards,
systems, and reports, making it difficult to monitor plant
performance, identify root causes, prioritize alerts, and track follow -
up actions

### Page 8

Final
Stage : Hackathon Event
The top 10 teams from the Preliminary Stage will be selected to
advance to the 2
-
day Final Stage, which will be conducted in a
hackathon
format
.
During
the
first
day
of
the
Final
Stage,
finalists
will
be
presented
with
a new and entirely different use case and will have 24 hours to
develop their solution
. Each team will then present its proposed
solution
in
a
pitching
session
held
on
the
following
day .
Submission format for the Final Stage will be informed during the
event
.
Pitching
session
will
be
conducted
in
English .
The event is scheduled on Wed -
Thu, 4
-
5 November 2026 in Jakarta
.
The finalists will be notified later on the details
. Please ensure your
availability
in
advance .

### Page 9

Preliminary Stage (Business Proposal Submission)
Please submit a clear representation of your proposed solution to
demonstrate the concept, user flow, and expected output. To be
eligible for preliminary stage review, you must submit these 3
materials:
1. A solution mock -
up or prototype, which may be provided
through Figma, accessible HTML, or other equivalent formats that
allow Committee to understand and navigate the proposed
result.
2. A 3 -
minute demo video that explains and demonstrates how the
proposed solution works.
3. A presentation deck in PDF format consisting of a maximum of 7
slides, including the cover slide and excluding any appendix
slides, following the required deck structure provided in the next
section of this booklet (see pg. 10).
All materials should be delivered in English.
Proposal must strictly follow the guidelines provided. Non -
compliance will directly affect the evaluation outcome.
SUBMISSION FORMAT

### Page 10

For Preliminary & Final Stage
Mandatory presentation deck structure:
Slide Required Content
1 Cover
Identify your team's name and the chosen use case .
2 Background & Problem Statement
Explain the current challenges, supporting facts, and why the problem is important to
solve.
3 Solution
Present the proposed solution, including the high -
level objective, workflow, and key
technologies.
4 Business Impact
Demonstrate the expected evaluation, measurable benefits, key performance
indicators (KPIs), and success metrics.
5 Feasibility & Roadmap
Explain the implementation feasibility, including technical, operational, legal,
cybersecurity, data governance, and organizational readiness considerations. Provide
an implementation roadmap and timeline.
6 Conclusion
Summarize the proposed solution, key value, and expected outcomes.
7 Team Profile
Provide team name, university, supervisor’s name, and details of team members
including study program, semester enrolled, area of expertise, and contributions to
the proposal. Please use the table below to present the information.
Appendix
Appendix slides are unlimited. Include only highly relevant supporting materials that
strengthen the proposal and provide additional evidence for evaluation.
No. Name Major Semester Area of expertise Contribution
1 [Example -
1] Computer
Science 6 Formulate the idea, etc.
2 [Example -
2] Chemical
Engineering 7 Elaborate background and
problem statement, etc.
3 … … … … …

### Page 11

1. Problem Understanding & Business Impact
• Clarity of problem understanding, identification of impacted
users, and articulation of pain points.
• Expected benefits, KPIs, success metrics, and measurable
business value with supporting data or evidence.
2. Solution Design & Prototype Quality
• Logical workflow, user journey, expected output, UX clarity, and
prototype completeness.
• If any: Relevance, strength, and novelty of technology use in the
proposed solution.
3. Presentation Quality (Technical)
• Presentation structure, visual clarity, and storytelling flow.
• Quality of demo video: pacing, narration, and ability to convey
the solution effectively within the 3 -
minute limit.
4. Feasibility & Roadmap
• Realistic implementation plan covering technical,
operational/legal/cybersecurity/etc. and organizational
readiness.
5. Chemical Domain Relevance
• Fit with real chemical industry needs and selected case context.
EVALUATION CRITERIA

### Page 12

1. Visit the website https://chandra - asri.com/id/caliber.
2. Navigate to the CALIBER 2026 menu.
3. Fill out the registration form.
4. Upon completing registration form, registrants will receive a
confirmation e -
mail and the Case Book as reference for the
business proposal.
5. If you do not receive the confirmation e -
mail and the case within
48 hours, please contact the 2026 CALIBER Committee at
caliber.2026@capcx.com.
HOW TO REGISTER
CONTACT PERSON
CALIBER 2026 Committee
caliber.2026@capcx.com
Sherrish
Tanudirdjo
Corporate Communications Chandra Asri Group
Sherrish.Tanudirdjo@capcx.com
Alifa Shavira
Corporate Communications Chandra Asri Group
Alifa.Shavira@capcx.com

### Page 13

1. Active undergraduate (S1) or vocational program (diploma)
students are eligible to participate throughout the competition
period from August to October 2026.
2. Participants must form teams consisting of 2 to 3 members
from the same university or college.
3. Each participant (member) are not allowed to be registered in
more than 1 team.
4. Students who are involved in academic violations or under
university sanctions during the competition period are not
allowed to participate.
5. There can be no changes to team members and team’s name
once the competition begins.
6. Each team must have a faculty advisor or lecturer as a
supervisor.
7. Each team is permitted to submit only 1 proposal.
8. Upon selection, all team members of are required to attend
the offline Final Stage in -
person. Please ensure your
availability on 4
-
5
November
2026.
9. By registering, participants agree to adhere to the rules and
guidelines of CALIBER 2026.
TERMS & CONDITIONS

### Page 14

1. Proposed ideas must be relevant to the provided case.
2. Every team must adhere to the regulations outlined in
this booklet and submit all necessary documents.
3. All submitted materials should be in English.
4. All submissions become the property of Chandra Asri
Group and will not be returned.
5. Plagiarism or any other misconduct will result in
disqualification.
6. Decisions made by the juries and the Chandra Asri
Group 2026 CALIBER Committee are final and cannot
be appealed.
7. Participants will be notified of any changes to the rules
and regulations.
RULES & REGULATIONS

### Page 15

1. Can I register for more than one team?
No. Each participant can only be registered in one team.
2. Can team members come from different faculties/majors?
Yes, you can form team with student(s) from other faculties/majors as long as you are all
from the same university/college.
3. Do we need to work on both use cases for Preliminary Stage?
No, please choose only one case to solve.
4. Can we combine ideas from both cases for Preliminary Stage?
No. Select just one of the two cases; while extended solutions to the problem may be
developed for whichever case you pick, your attention should remain on that particular case.
5. What file formats and size limits apply to the prototype, video, and presentation deck?
For the Preliminary Stage, all 3 (three) deliverables combined should be no bigger than 10
MB. Submission format for Final Stage will be informed during the event.
6. What language should be used for the presentation deck and pitch?
All materials should be written and delivered in English.
7. Can we use generative AI tools as part of our solution development process?
The use of AI tools is permitted, provided they are used lawfully and in accordance with
their applicable terms and conditions and privacy notices. All AI -
generated outputs must be
validated, iterated, and evaluated to ensure the quality, accuracy, and reliability of the
resulting technology solutions before use or implementation.
8. Can we update or replace our submission after it has been submitted?
No. Only the first submission submitted by your team will be accepted and evaluated.
9. What happens if we fail to submit one of the required deliverables?
Your team will be disqualified and cannot continue to the next stage.
FAQ (General)

### Page 16

GRAND PRIZE
Rp15 million
Rp10 million Rp7,5 million

### Page 17

TIMELINE
10 August 2026 Open Registration
EXTENDED : 17 September
2026
Proposal Submission
Close Registration
Best Proposal
Announcement
4 October 2026
23 October 2026
4
-
5 November 2026 Final Presentation and
Winner Announcement

### Page 18

Chandra Asri Group
CALIBER 2026
Committee
E
-
mail : caliber. 2026 @capcx.com
PT Chandra Asri Pacific Tbk
Head Office
Wisma Barito Pacific Tower A, 5th Floor
Jl. Let. Jend
. S. Parman Kav. 62 -
63
Jakarta 11410, Indonesia
Phone: (62 -
21) 530 7950
Fax: (62 -
21) 530 8930


---

# Appendix B. Source Integrity and Scope

## Uploaded source inventory

| Source | Format | Pages / structure |
|---|---|---|
| CALIBER2026_Case2_TeamBriefing.docx | DOCX | 20 pages in the source document |
| The Case - CALIBER 2026.pdf | PDF | 13 pages |
| Booklet CALIBER 2026 - Registration Extended.pdf | PDF | 18 pages |

## Interpretation policy used in this Markdown

- Source wording has been normalized for spacing and line-break artifacts caused by PDF/DOCX extraction.
- Substantive numbers, dates, dataset names, field names, thresholds, statuses, and case facts are retained.
- Where the source distinguishes a **Fact** from an **Interpretation**, that distinction is retained.
- Where a source says information is not stated, this Markdown does not invent the missing information.
- Where the Team Briefing contains an unpopulated numbered placeholder, the placeholder is preserved and its missing description is explicitly noted.
- No external data was added to the substantive case analysis.
