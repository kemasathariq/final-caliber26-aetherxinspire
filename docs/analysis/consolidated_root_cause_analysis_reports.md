# Consolidated Abnormality & Root Cause Analysis (RCA) Reports

---

## Executive Overview Summary

| AR Number | Tag / Plant | Equipment Name | Issue / Event | Severity | Pre-Risk | Downtime | Prod. Loss | Total Cost Loss | Primary Root Cause |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **AR-2026-ARP-0117** | `PU-2101B` / ARP | Feed Charge Pump | Mechanical Seal Leakage | Major | III (200) | 18.5 h | 251.6 ton | $226.44k | Intermittent dry-running from suction cavitation during feed swings & lack of interlock |
| **AR-2026-ZCU-0142** | `KO-3201` / ZCU | Cracked Gas Compressor | High Radial Vibration Trip | Catastrophic | II (4000) | 32.0 h | 1760.0 ton | $1,584.00k | Water ingress via leaking lube-oil cooler degrading oil film, leading to bearing babbitt distress |
| **AR-2026-NUP-0089** | `PM-4405B` / NUP | Cooling Water Pump (Motor) | Motor Bearing Overheating Trip | Moderate | III (200) | 8.0 h | 160.0 ton | $112.00k | Grease degradation from over-extended non-risk-based re-lubrication interval |
| **AR-2026-ZCU-0165** | `HE-3301` / ZCU | Feed/Effluent Heat Exchanger | Tube-side Fouling / Duty Loss | Moderate | III (400) | 12.0 h | 216.0 ton | $183.60k | Heavy-ends feed fouling allowed to progress without dP-based cleaning triggers/KPIs |
| **AR-2026-OPP-0203** | `BL-5702` / OPP | Product Blower | High Vibration Trip | Major | III (400) | 14.0 h | 532.0 ton | $478.80k | Coupling misalignment aggravated by soft-foot and aged elastomer coupling element |

---

## Document Index
1. [RCA 1: PU-2101B Mechanical Seal Leakage](#rca-1-pu-2101b-mechanical-seal-leakage)
2. [RCA 2: KO-3201 High Radial Vibration Trip](#rca-2-ko-3201-high-radial-vibration-trip)
3. [RCA 3: PM-4405B Motor Bearing Failure](#rca-3-pm-4405b-motor-bearing-failure)
4. [RCA 4: HE-3301 High Fouling — Duty Loss & High dP](#rca-4-he-3301-high-fouling--duty-loss--high-dp)
5. [RCA 5: BL-5702 High Vibration (Coupling Misalignment)](#rca-5-bl-5702-high-vibration-coupling-misalignment)

---

# RCA 1: PU-2101B Mechanical Seal Leakage

### 1. Document Header & Identification
* **AR Number:** AR-2026-ARP-0117
* **Title / Problem:** Feed Charge Pump PU-2101B — Mechanical Seal Leakage
* **Tag / Plant Unit:** PU-2101B | ARP (Aurora Resin Plant)
* **Equipment Class:** Class B
* **Discipline:** ROT (Rotating)
* **AR Type:** OPEDR (Operation) — Uptime
* **Date of Occurrence:** 12 Mar 2026
* **Date Reported:** 13 Mar 2026
* **Pre-Risk Level:** Level III (Score: 200)
* **Severity:** Major
* **PIC (RCA):** REL-05
* **Procedure No.:** RCA-P-0050-03 | **Form No.:** RCA-F-0075-02
* **Downtime:** 18.5 hours
* **Production Loss:** 251.6 ton
* **Estimated Loss:** $226.44k

#### Immediate Action
Isolate `PU-2101B`, swap to spare `PU-2101A`, replace mechanical seal cartridge.

#### Problem Statement
Mechanical seal of Feed Charge Pump `PU-2101B` failed on 12-Mar-2026, causing seal leakage and an unplanned feed reduction to the ARP reactor section.

---

### 2. Chronology of Events
* **11-Mar-2026:** ARP produced resin grade PR-5502 (Reactor Rate $\pm 13.6\text{ T/H}$). Field operator noted minor seal weep on `PU-2101B` during routine round.
* **12-Mar-2026 02:15:** Seal flush low-flow alarm annunciated; visible feed seal leak with low suction pressure. Pump auto-tripped on low discharge pressure.
* **12-Mar-2026 02:40:** Feed section reduced; charge to reactor curtailed pending seal repair. Rotating team mobilized.
* **12-Mar-2026 09:20:** Seal cartridge & shaft sleeve inspected — seal faces heat-checked / worn (dry-running signature).
* **12-Mar-2026 20:45:** New seal cartridge installed, pump commissioned, feed restored to $\pm 13.6\text{ T/H}$.

---

### 3. Historical Data & 4W Assessment

#### Historical Data & Evidence
`PU-2101B` seal MTBF trended down from 26 to 9 months over the last 3 cycles. Seal-flush flow had been intermittently below the $6\text{ L/min}$ design minimum during feed swings, indicating recurring dry-run exposure.

#### Impact Summary (4W)
* **What:** Mechanical seal of `PU-2101B` leaked / failed
* **When:** 12-Mar-2026 (02:15)
* **Scope:** Reduced charge feed to ARP reactor section
* **Uptime Loss:** $18.5\text{ hours} \longrightarrow 251.6\text{ ton} \longrightarrow \$226.44\text{k}$

---

### 4. Target Setting
* **Actual Condition (Before):** Feed reduction due to `PU-2101B` mechanical seal leak.
* **Target Condition (Project Y):** No unplanned feed reduction due to `PU-2101B` seal failure (seal MTBF $\ge 24\text{ months}$).
* **Target Metric:** Recurrence of equipment failure mode: Before = $1\text{ case} \longrightarrow$ Target = $0\text{ cases}$.

---

### 5. Parameter Verification (4P Analysis)

| # | Problem Phenomenon / Parameter | Result | Evidence / Finding |
|---|---|:---:|---|
| **P1** | Pump operated above rated flow | **G** | Operated at $13.1\text{--}13.7\text{ T/H}$ vs rated max $18\text{ T/H}$ — within limit. |
| **P2** | Suction pressure below NPSH margin | **NG** | Suction pressure dropped during feed swing; NPSH margin $< 0.5\text{ m}$ (spec $\ge 1.0\text{ m}$) — cavitation risk. |
| **P3** | Seal flush flow below minimum | **NG** | Seal-flush flow measured $3\text{--}4\text{ L/min}$ vs $6\text{ L/min}$ minimum — seal ran dry intermittently. |
| **P4** | Cooling water to seal cooler inadequate | **G** | Seal cooler outlet temp normal ($42\text{ }^\circ\text{C}$) — cooling adequate. |
| **P5** | Seal faces beyond service life | **G** | Seal in service 11 months, within 24-month design life. |

*(Legend: **G** = Meets Standard / Good, **NG** = Does Not Meet Standard / Problem)*

---

### 6. Root Cause Verification (4M + 1E)

| # | Factor | Result | Evidence / Finding |
|---|---|:---:|---|
| **X1** | No low-NPSH / flush-flow interlock in DCS | **NG** | No automatic trip or alarm on loss of seal-flush flow. |
| **X2** | Feed-swing SOP allows fast rate ramp | **NG** | SOP permits $> 2\text{ T/H per minute}$ ramp, driving suction transients. |
| **X3** | PM covers seal only, not flush system | **NG** | Seal-flush plan (Plan 11) not on the PM check-sheet. |
| **X4** | Operator competency on seal-flush monitoring | **G** | Operators trained; no competency gap identified. |

#### Verified Root Cause Statement
Premature mechanical seal failure caused by intermittent dry-running: suction cavitation during feed swings reduced NPSH and seal-flush flow dropped below the $6\text{ L/min}$ minimum, with no interlock to protect the seal.

#### Priority Matrix Summary
High-impact root causes prioritized for intervention: `P2`, `P3`, `X1`, `X2`, `X3`.

---

### 7. Corrective & Pro-Active Action Plan (CAPAA)

#### Corrective Actions
| RC | Action Description | Plan Date | PIC | Status |
|---|---|---|---|---|
| **P3** | Install seal-flush flow switch with DCS alarm on `PU-2101B` | 24-Apr-2026 | REL-05 | In Progress |
| **X1** | Add low-NPSH / loss-of-flush trip interlock in DCS | 24-May-2026 | REL-02 | Open |

#### Pro-Active Actions (Fleet / Unit Roll-out)
| RC | Action Description | Plan Date | PIC | Status |
|---|---|---|---|---|
| **P3** | Roll out flush-flow switch to `PU-2101A` spare | 24-May-2026 | REL-05 | Open |
| **X1** | Apply interlock standard to all API-682 seal pumps in ARP | 24-Jul-2026 | REL-02 | Open |

---

### 8. Preventive Actions, Risk Analysis & PM Schedule

#### Preventive Actions
| Item | Possible Root Cause | Preventive Action | Plan Date | PIC |
|---|---|---|---|---|
| **P2** | Suction cavitation | Revise feed-swing SOP to cap ramp at $1\text{ T/H per minute}$ | 24-Apr-2026 | ROT-01 |
| **X3** | Flush system not in PM | Add seal-flush system (Plan 11) to `PU-2101B` PM check-sheet | 24-Apr-2026 | REL-05 |

#### Risk Analysis of Corrective Actions
* **Corrective Action:** Install flow switch & interlock
* **Potential Risk:** Nuisance trips during commissioning
* **Countermeasure:** Stage commissioning with bypass timer & operator brief (Target Date: 24-May-2026 | PIC: REL-05)

#### Established PM Schedule
* **PM-1:** Weekly seal-flush flow & seal-pot level check on `PU-2101B` | **Group:** Rotating | **Interval:** Weekly
* **PM-2:** Quarterly seal condition & shaft run-out inspection | **Group:** Rotating | **Interval:** 3-monthly

---
---

# RCA 2: KO-3201 High Radial Vibration Trip

### 1. Document Header & Identification
* **AR Number:** AR-2026-ZCU-0142
* **Title / Problem:** Cracked Gas Compressor KO-3201 — High Radial Vibration Trip (Bearing Distress)
* **Tag / Plant Unit:** KO-3201 | ZCU (Zeta Cracker Unit)
* **Equipment Class:** Class A
* **Discipline:** ROT (Rotating)
* **AR Type:** OPEDR (Operation) — Uptime
* **Date of Occurrence:** 29 Apr 2026
* **Date Reported:** 30 Apr 2026
* **Pre-Risk Level:** Level II (Score: 4000)
* **Severity:** Catastrophic
* **PIC (RCA):** REL-05
* **Procedure No.:** RCA-P-0050-03 | **Form No.:** RCA-F-0075-02
* **Downtime:** 32.0 hours
* **Production Loss:** 1760.0 ton
* **Estimated Loss:** $1,584.00k

#### Immediate Action
Controlled shutdown of compression train, replace DE journal bearing, flush lube-oil system.

#### Problem Statement
Cracked Gas Compressor `KO-3201` tripped on high-high radial vibration on 29-Apr-2026 due to journal-bearing babbitt distress driven by water-contaminated lube oil.

---

### 2. Chronology of Events
* **27-Apr-2026:** ZCU compression train running normal; `KO-3201` drive-end (DE) radial vibration trending up (from $28\text{ to }52\text{ }\mu\text{m}$ over 5 days).
* **29-Apr-2026 06:40:** `KO-3201` DE vibration reached high-high setpoint ($75\text{ }\mu\text{m}$); machinery protection system tripped the compressor.
* **29-Apr-2026 08:10:** Plant rate cut to minimum; lube-oil sample taken — water content $1,800\text{ ppm}$ (spec $< 500\text{ ppm}$).
* **29-Apr-2026 18:00:** DE journal bearing removed — babbitt wiped/distressed. Lube-oil cooler tube leak confirmed.
* **30-Apr-2026 14:40:** New bearing installed, lube-oil system flushed, cooler tube plugged, train restarted to $55\text{ T/H}$.

---

### 3. Historical Data & 4W Assessment

#### Historical Data & Evidence
`KO-3201` DE vibration baseline is $25\text{--}30\text{ }\mu\text{m}$. Trend shows a steady rise over 5 days preceding the trip. Lube-oil water content had drifted above $500\text{ ppm}$ for $\sim 2\text{ weeks}$ without an online alarm.

#### Impact Summary (4W)
* **What:** `KO-3201` tripped on high-high radial vibration
* **When:** 29-Apr-2026 (06:40)
* **Scope:** ZCU compression train shutdown — full ethylene rate loss
* **Uptime Loss:** $32.0\text{ hours} \longrightarrow 1760.0\text{ ton} \longrightarrow \$1,584.00\text{k}$

---

### 4. Target Setting
* **Actual Condition (Before):** Compressor trip due to bearing distress from contaminated lube oil.
* **Target Condition (Project Y):** No compressor trip due to lube-oil contamination (water $< 500\text{ ppm}$, vibration $< 45\text{ }\mu\text{m}$).
* **Target Metric:** Recurrence of equipment failure mode: Before = $1\text{ case} \longrightarrow$ Target = $0\text{ cases}$.

---

### 5. Parameter Verification (4P Analysis)

| # | Problem Phenomenon / Parameter | Result | Evidence / Finding |
|---|---|:---:|---|
| **P1** | Radial vibration above alarm | **NG** | DE vibration rose to $75\text{ }\mu\text{m}$ vs $45\text{ }\mu\text{m}$ alarm — bearing distress. |
| **P2** | Lube-oil water content above spec | **NG** | Water content $1,800\text{ ppm}$ vs $< 500\text{ ppm}$ spec — film breakdown. |
| **P3** | Lube-oil supply pressure low | **G** | Header pressure $1.8\text{ barg}$ — within normal band. |
| **P4** | Bearing beyond service life | **G** | Bearing in service 3 years vs 6-year design — within life. |
| **P5** | Process surge / anti-surge margin | **G** | Anti-surge margin maintained; no surge event recorded. |

*(Legend: **G** = Meets Standard / Good, **NG** = Does Not Meet Standard / Problem)*

---

### 6. Root Cause Verification (4M + 1E)

| # | Factor | Result | Evidence / Finding |
|---|---|:---:|---|
| **X1** | No online water-in-oil monitoring | **NG** | Water content only checked by weekly grab sample — slow detection. |
| **X2** | Lube-oil cooler integrity not trended | **NG** | No routine cooler tube leak check between TAs. |
| **X3** | Vibration alert limits too wide | **NG** | Alert at $60\text{ }\mu\text{m}$ gave little lead time before $75\text{ }\mu\text{m}$ trip. |
| **X4** | Lube-oil purifier not in service | **G** | Purifier available and operational. |

#### Verified Root Cause Statement
Journal-bearing babbitt distress caused by degraded oil-film strength from water ingress via a leaking lube-oil cooler tube, undetected due to absence of online water-in-oil monitoring, leading to rising vibration and a high-high trip.

#### Priority Matrix Summary
High-impact root causes prioritized for intervention: `P1`, `P2`, `X1`, `X2`, `X3`.

---

### 7. Corrective & Pro-Active Action Plan (CAPAA)

#### Corrective Actions
| RC | Action Description | Plan Date | PIC | Status |
|---|---|---|---|---|
| **P2** | Repair leaking lube-oil cooler tube (plug + re-test) | 30-Apr-2026 | STA-02 | Closed |
| **X1** | Install online water-in-oil sensor on `KO-3201` lube system | 30-Jun-2026 | REL-05 | In Progress |

#### Pro-Active Actions (Fleet / Unit Roll-out)
| RC | Action Description | Plan Date | PIC | Status |
|---|---|---|---|---|
| **P2** | Retube lube-oil cooler at next TA | 31-Oct-2026 | STA-02 | Open |
| **X1** | Apply online water-in-oil monitoring to `KO-3202`/`3203` | 30-Sep-2026 | REL-05 | Open |

---

### 8. Preventive Actions, Risk Analysis & PM Schedule

#### Preventive Actions
| Item | Possible Root Cause | Preventive Action | Plan Date | PIC |
|---|---|---|---|---|
| **X3** | Vibration limits too wide | Tighten `KO-3201` vibration alert to $45\text{ }\mu\text{m}$ & shorten trend-review cadence | 30-May-2026 | REL-05 |
| **X2** | Cooler integrity not trended | Add lube-oil cooler dP & conductivity trend to reliability dashboard | 30-Jun-2026 | REL-02 |

#### Risk Analysis of Corrective Actions
* **Corrective Action:** Tighten vibration alert to $45\text{ }\mu\text{m}$
* **Potential Risk:** Nuisance alerts on start-up transients
* **Countermeasure:** Add start-up alarm suppression timer (Target Date: 30-May-2026 | PIC: REL-05)

#### Established PM Schedule
* **PM-1:** Weekly lube-oil water-content & particle count | **Group:** Reliability | **Interval:** Weekly
* **PM-2:** 6-monthly lube-oil cooler leak test | **Group:** Static | **Interval:** 6-monthly
* **PM-3:** Continuous vibration trend review `KO-3201` | **Group:** Reliability | **Interval:** Daily

---
---

# RCA 3: PM-4405B Motor Bearing Failure

### 1. Document Header & Identification
* **AR Number:** AR-2026-NUP-0089
* **Title / Problem:** Cooling Water Pump PM-4405B (Motor Driven) — Motor Bearing Failure (Overheating)
* **Tag / Plant Unit:** PM-4405B | NUP (Nova Utility Plant)
* **Equipment Class:** Class B
* **Discipline:** ELE (Electrical)
* **AR Type:** OPEDR (Operation) — Uptime
* **Date of Occurrence:** 08 Jul 2026
* **Date Reported:** 08 Jul 2026
* **Pre-Risk Level:** Level III (Score: 200)
* **Severity:** Moderate
* **PIC (RCA):** REL-02
* **Procedure No.:** RCA-P-0050-03 | **Form No.:** RCA-F-0075-02
* **Downtime:** 8.0 hours
* **Production Loss:** 160.0 ton
* **Estimated Loss:** $112.00k

#### Immediate Action
Start standby CW pump `PM-4405C`, isolate `PM-4405B`, replace motor DE & NDE bearings.

#### Problem Statement
Cooling Water Pump `PM-4405B` motor tripped on 08-Jul-2026 due to drive-end bearing failure from grease degradation and an over-extended re-lubrication interval.

---

### 2. Chronology of Events
* **06-Jul-2026:** Cooling-water system running on `PM-4405B`; motor DE bearing temperature trending up ($68 \longrightarrow 84\text{ }^\circ\text{C}$).
* **08-Jul-2026 13:20:** Motor bearing high-temperature alarm; motor tripped on winding/bearing over-temp.
* **08-Jul-2026 13:35:** Standby `PM-4405C` started; cooling-water supply maintained at reduced margin.
* **08-Jul-2026 16:00:** Motor DE bearing found seized; grease degraded/carbonized. NDE bearing marginal.
* **08-Jul-2026 21:20:** DE & NDE bearings replaced and re-greased; motor recommissioned.

---

### 3. Historical Data & 4W Assessment

#### Historical Data & Evidence
`PM-4405B` motor bearing temperature baseline is $60\text{--}68\text{ }^\circ\text{C}$. Re-lubrication was performed on a fixed 12-month interval regardless of duty/ambient. Bearing temperature was not trended in CMMS, so degradation went unnoticed.

#### Impact Summary (4W)
* **What:** `PM-4405B` motor DE bearing failed / overheated
* **When:** 08-Jul-2026 (13:20)
* **Scope:** Loss of one cooling-water pump; reduced CW margin (standby covered)
* **Uptime Loss:** $8.0\text{ hours} \longrightarrow 160.0\text{ ton} \longrightarrow \$112.00\text{k}$

---

### 4. Target Setting
* **Actual Condition (Before):** CW pump motor trip due to bearing overheating.
* **Target Condition (Project Y):** No motor bearing failure due to lubrication (bearing temp $< 75\text{ }^\circ\text{C}$, risk-based re-greasing).
* **Target Metric:** Recurrence of equipment failure mode: Before = $1\text{ case} \longrightarrow$ Target = $0\text{ cases}$.

---

### 5. Parameter Verification (4P Analysis)

| # | Problem Phenomenon / Parameter | Result | Evidence / Finding |
|---|---|:---:|---|
| **P1** | Motor bearing temperature above limit | **NG** | DE bearing reached $84\text{ }^\circ\text{C}$ vs $75\text{ }^\circ\text{C}$ alarm — grease breakdown. |
| **P2** | Motor over-loaded (high ampere) | **G** | Running current $132\text{ A}$ vs $150\text{ A}$ rated — within limit. |
| **P3** | Cooling-fan / ventilation blocked | **G** | Fan cowl clean; ambient ventilation adequate. |
| **P4** | Grease type incorrect | **G** | Correct high-temp lithium-complex grease used. |
| **P5** | Bearing beyond service life | **G** | Bearing in service 2 years vs 5-year design — within life. |

*(Legend: **G** = Meets Standard / Good, **NG** = Does Not Meet Standard / Problem)*

---

### 6. Root Cause Verification (4M + 1E)

| # | Factor | Result | Evidence / Finding |
|---|---|:---:|---|
| **X1** | Re-lubrication interval not risk-based | **NG** | Fixed 12-month interval too long for duty & ambient — grease degraded. |
| **X2** | Bearing temperature not trended in CMMS | **NG** | No condition-based trigger; only alarm at failure point. |
| **X3** | Vibration route excludes utility motors | **NG** | `PM-4405B` not on the monthly vibration route. |
| **X4** | Operator round frequency | **G** | Rounds performed per schedule; local gauge read. |

#### Verified Root Cause Statement
Motor drive-end bearing failure caused by grease degradation from an over-extended, non-risk-based re-lubrication interval, undetected due to absence of bearing-temperature trending, resulting in bearing overheating and motor trip.

#### Priority Matrix Summary
High-impact root causes prioritized for intervention: `P1`, `X1`, `X2`, `X3`.

---

### 7. Corrective & Pro-Active Action Plan (CAPAA)

#### Corrective Actions
| RC | Action Description | Plan Date | PIC | Status |
|---|---|---|---|---|
| **X1** | Revise `PM-4405B` re-lubrication interval to risk-based (4-monthly) | 31-Jul-2026 | REL-02 | In Progress |
| **X2** | Add motor bearing temperature trending & alert to CMMS | 31-Aug-2026 | REL-05 | Open |

#### Pro-Active Actions (Fleet / Unit Roll-out)
| RC | Action Description | Plan Date | PIC | Status |
|---|---|---|---|---|
| **X1** | Apply risk-based re-greasing to all CW pump motors | 31-Aug-2026 | REL-02 | Open |
| **X2** | Extend bearing-temp trending to utility motor fleet | 30-Sep-2026 | REL-05 | Open |

---

### 8. Preventive Actions, Risk Analysis & PM Schedule

#### Preventive Actions
| Item | Possible Root Cause | Preventive Action | Plan Date | PIC |
|---|---|---|---|---|
| **X3** | Motor not on vibration route | Add `PM-4405B/C` to monthly vibration & thermography route | 31-Jul-2026 | REL-02 |
| **P1** | Bearing over-temp | Verify motor cooling-fan & louvre condition each PM | 31-Jul-2026 | ELE-01 |

#### Risk Analysis of Corrective Actions
* **Corrective Action:** Shorten re-greasing interval
* **Potential Risk:** Over-greasing risk (churning / seal push-out)
* **Countermeasure:** Use metered re-greasing per bearing volume calc (Target Date: 31-Jul-2026 | PIC: REL-02)

#### Established PM Schedule
* **PM-1:** Risk-based motor bearing re-greasing `PM-4405B` | **Group:** Electrical | **Interval:** 4-monthly
* **PM-2:** Monthly motor bearing temperature & vibration reading | **Group:** Reliability | **Interval:** Monthly

---
---

# RCA 4: HE-3301 High Fouling — Duty Loss & High dP

### 1. Document Header & Identification
* **AR Number:** AR-2026-ZCU-0165
* **Title / Problem:** Feed/Effluent Heat Exchanger HE-3301 — High Fouling — Duty Loss & High dP
* **Tag / Plant Unit:** HE-3301 | ZCU (Zeta Cracker Unit)
* **Equipment Class:** Class B
* **Discipline:** STA (Static)
* **AR Type:** OPEDR (Operation) — Uptime
* **Date of Occurrence:** 21 May 2026
* **Date Reported:** 22 May 2026
* **Pre-Risk Level:** Level III (Score: 400)
* **Severity:** Moderate
* **PIC (RCA):** STA-02
* **Procedure No.:** RCA-P-0050-03 | **Form No.:** RCA-F-0075-02
* **Downtime:** 12.0 hours
* **Production Loss:** 216.0 ton
* **Estimated Loss:** $183.60k

#### Immediate Action
Isolate `HE-3301`, bypass via spare train, hydro-jet clean tube bundle.

#### Problem Statement
Feed/Effluent Heat Exchanger `HE-3301` suffered accelerated tube-side fouling reducing duty and raising dP, forcing an unplanned isolation, cleaning and partial rate cut on 21-May-2026.

---

### 2. Chronology of Events
* **18-May-2026:** Heat-recovery section running; `HE-3301` tube-side dP rising ($0.4 \longrightarrow 0.9\text{ bar}$) and cold-outlet temperature falling.
* **21-May-2026 09:00:** Preheat duty dropped $\sim 35\%$ below design; unit rate reduced to protect downstream. Exchanger isolated.
* **21-May-2026 11:30:** Tube bundle inspected — heavy coke/polymer deposition on tube side.
* **21-May-2026 21:00:** Bundle hydro-jet cleaned and returned to service; duty and dP restored, rate ramped back to $30\text{ T/H}$.

---

### 3. Historical Data & 4W Assessment

#### Historical Data & Evidence
`HE-3301` tube-side dP baseline is $0.3\text{--}0.4\text{ bar}$; heat duty design $100\%$. Over the run, dP climbed steadily while duty fell — a classic fouling curve. No dP-based cleaning trigger existed, so fouling was allowed to progress to a forced cut.

#### Impact Summary (4W)
* **What:** `HE-3301` duty loss & high dP from tube-side fouling
* **When:** 21-May-2026 (09:00)
* **Scope:** Partial rate cut of ZCU heat-recovery section
* **Uptime Loss:** $12.0\text{ hours} \longrightarrow 216.0\text{ ton} \longrightarrow \$183.60\text{k}$

---

### 4. Target Setting
* **Actual Condition (Before):** Rate cut due to `HE-3301` fouling (duty loss + high dP).
* **Target Condition (Project Y):** No unplanned rate cut due to `HE-3301` fouling ($\text{dP} < 0.6\text{ bar}$, $\text{duty} > 90\%$).
* **Target Metric:** Recurrence of equipment failure mode: Before = $1\text{ case} \longrightarrow$ Target = $0\text{ cases}$.

---

### 5. Parameter Verification (4P Analysis)

| # | Problem Phenomenon / Parameter | Result | Evidence / Finding |
|---|---|:---:|---|
| **P1** | Tube-side dP above limit | **NG** | dP reached $0.9\text{ bar}$ vs $0.6\text{ bar}$ limit — heavy fouling. |
| **P2** | Heat duty below design | **NG** | Duty fell to $\sim 65\%$ of design — loss of preheat. |
| **P3** | Feed heavy-ends above spec | **NG** | Heavy-ends $2.4\%$ vs $< 1.5\%$ design — increased fouling precursor. |
| **P4** | Tube velocity below design | **G** | Tube velocity $1.9\text{ m/s}$ vs $1.5\text{ m/s}$ min — adequate. |
| **P5** | Cooling/heating medium temperature off | **G** | Shell-side inlet temperature within normal band. |

*(Legend: **G** = Meets Standard / Good, **NG** = Does Not Meet Standard / Problem)*

---

### 6. Root Cause Verification (4M + 1E)

| # | Factor | Result | Evidence / Finding |
|---|---|:---:|---|
| **X1** | No dP-based cleaning trigger | **NG** | Cleaning was time-based only; no dP alarm to trigger action. |
| **X2** | Feed filtration performance not trended | **NG** | Upstream filter dP not monitored, allowing heavy-ends carry-over. |
| **X3** | Fouling KPI not on dashboard | **NG** | No fouling factor / duty KPI tracked between TAs. |
| **X4** | Bundle metallurgy inadequate | **G** | Bundle metallurgy suitable for service. |

#### Verified Root Cause Statement
Accelerated tube-side coke/polymer fouling driven by higher-than-design feed heavy-ends, allowed to progress by the absence of a dP-based cleaning trigger and fouling KPI, causing duty loss, high dP and a forced rate cut.

#### Priority Matrix Summary
High-impact root causes prioritized for intervention: `P1`, `P2`, `P3`, `X1`, `X2`, `X3`.

---

### 7. Corrective & Pro-Active Action Plan (CAPAA)

#### Corrective Actions
| RC | Action Description | Plan Date | PIC | Status |
|---|---|---|---|---|
| **X1** | Add dP-based cleaning trigger & alarm for `HE-3301` | 22-Jun-2026 | STA-02 | In Progress |
| **P3** | Tighten feed heavy-ends control & filtration | 30-Jun-2026 | ROT-01 | Open |

#### Pro-Active Actions (Fleet / Unit Roll-out)
| RC | Action Description | Plan Date | PIC | Status |
|---|---|---|---|---|
| **X1** | Apply dP-trigger logic to parallel exchangers `HE-3302`/`3303` | 22-Jul-2026 | STA-02 | Open |
| **P3** | Review upstream fractionation cut-point control | 31-Jul-2026 | ROT-01 | Open |

---

### 8. Preventive Actions, Risk Analysis & PM Schedule

#### Preventive Actions
| Item | Possible Root Cause | Preventive Action | Plan Date | PIC |
|---|---|---|---|---|
| **X3** | No fouling KPI | Add fouling factor & duty KPI to reliability dashboard | 22-Jun-2026 | STA-02 |
| **X2** | Filter not trended | Add upstream filter dP trend & replacement trigger | 30-Jun-2026 | ROT-01 |

#### Risk Analysis of Corrective Actions
* **Corrective Action:** Add dP cleaning trigger
* **Potential Risk:** Premature/over-frequent cleaning
* **Countermeasure:** Set trigger with hysteresis + engineering review before cleaning (Target Date: 22-Jun-2026 | PIC: STA-02)

#### Established PM Schedule
* **PM-1:** Daily `HE-3301` dP & duty trend review | **Group:** Process | **Interval:** Daily
* **PM-2:** Bundle inspection & cleaning at dP trigger / next TA | **Group:** Static | **Interval:** Condition / TA

---
---

# RCA 5: BL-5702 High Vibration (Coupling Misalignment)

### 1. Document Header & Identification
* **AR Number:** AR-2026-OPP-0203
* **Title / Problem:** Product Blower BL-5702 — High Vibration (Coupling Misalignment)
* **Tag / Plant Unit:** BL-5702 | OPP (Orion Polypropylene Plant)
* **Equipment Class:** Class A
* **Discipline:** ROT (Rotating)
* **AR Type:** OPEDR (Operation) — Uptime
* **Date of Occurrence:** 17 Jun 2026
* **Date Reported:** 18 Jun 2026
* **Pre-Risk Level:** Level III (Score: 400)
* **Severity:** Major
* **PIC (RCA):** ROT-01
* **Procedure No.:** RCA-P-0050-03 | **Form No.:** RCA-F-0075-02
* **Downtime:** 14.0 hours
* **Production Loss:** 532.0 ton
* **Estimated Loss:** $478.80k

#### Immediate Action
Stop `BL-5702`, re-align coupling, replace worn coupling element.

#### Problem Statement
Product Blower `BL-5702` tripped on high vibration on 17-Jun-2026 due to coupling misalignment and a worn coupling element, halting the OPP powder-handling section.

---

### 2. Chronology of Events
* **15-Jun-2026:** OPP running normal; `BL-5702` vibration trending up ($4.2 \longrightarrow 8.5\text{ mm/s}$) with $2\text{X}$ harmonic rising.
* **17-Jun-2026 04:30:** `BL-5702` vibration reached alarm ($11\text{ mm/s}$); blower stopped to prevent damage — powder handling section halted.
* **17-Jun-2026 07:00:** Coupling element found worn/cracked; laser alignment showed $0.35\text{ mm}$ offset (spec $< 0.05\text{ mm}$).
* **17-Jun-2026 18:30:** Coupling element replaced, unit re-aligned to $< 0.05\text{ mm}$, blower restarted to $38\text{ T/H}$.

---

### 3. Historical Data & 4W Assessment

#### Historical Data & Evidence
`BL-5702` vibration baseline is $3.5\text{--}4.5\text{ mm/s}$. A rising trend with dominant $2\text{X}$ harmonic over 2 days indicated developing misalignment. Alignment was last verified 14 months prior; no soft-foot / alignment check in the routine PM.

#### Impact Summary (4W)
* **What:** `BL-5702` high vibration from coupling misalignment
* **When:** 17-Jun-2026 (04:30)
* **Scope:** OPP powder-handling section stop
* **Uptime Loss:** $14.0\text{ hours} \longrightarrow 532.0\text{ ton} \longrightarrow \$478.80\text{k}$

---

### 4. Target Setting
* **Actual Condition (Before):** Blower stop due to high vibration (misalignment).
* **Target Condition (Project Y):** No blower stop due to misalignment (vibration $< 7\text{ mm/s}$, alignment $< 0.05\text{ mm}$).
* **Target Metric:** Recurrence of equipment failure mode: Before = $1\text{ case} \longrightarrow$ Target = $0\text{ cases}$.

---

### 5. Parameter Verification (4P Analysis)

| # | Problem Phenomenon / Parameter | Result | Evidence / Finding |
|---|---|:---:|---|
| **P1** | Overall vibration above alarm | **NG** | Vibration reached $11\text{ mm/s}$ vs $7\text{ mm/s}$ alarm — misalignment signature. |
| **P2** | Coupling alignment out of tolerance | **NG** | Offset $0.35\text{ mm}$ vs $< 0.05\text{ mm}$ spec — angular/parallel misalignment. |
| **P3** | Bearing condition degraded | **G** | Bearing envelope/shock-pulse normal — no bearing defect. |
| **P4** | Foundation / soft-foot | **NG** | Soft-foot $0.12\text{ mm}$ found on one foot — contributed to misalignment. |
| **P5** | Rotor unbalance | **G** | $1\text{X}$ component within balance grade — no unbalance. |

*(Legend: **G** = Meets Standard / Good, **NG** = Does Not Meet Standard / Problem)*

---

### 6. Root Cause Verification (4M + 1E)

| # | Factor | Result | Evidence / Finding |
|---|---|:---:|---|
| **X1** | Alignment check not in routine PM | **NG** | PM did not include periodic laser alignment / soft-foot check. |
| **X2** | Coupling element life not tracked | **NG** | Elastomer coupling element run beyond recommended 12-month life. |
| **X3** | Vibration route interval too long | **NG** | Monthly route missed the fast-rising 2-day trend. |
| **X4** | Alignment tools / competency | **G** | Laser alignment tool & trained technicians available. |

#### Verified Root Cause Statement
High vibration from coupling misalignment aggravated by soft-foot and an over-aged elastomer coupling element, undetected because periodic alignment/soft-foot checks were absent from the PM and the vibration route interval was too long.

#### Priority Matrix Summary
High-impact root causes prioritized for intervention: `P1`, `P2`, `P4`, `X1`, `X2`, `X3`.

---

### 7. Corrective & Pro-Active Action Plan (CAPAA)

#### Corrective Actions
| RC | Action Description | Plan Date | PIC | Status |
|---|---|---|---|---|
| **X1** | Add periodic laser alignment & soft-foot check to `BL-5702` PM | 18-Jul-2026 | ROT-01 | In Progress |
| **X2** | Track coupling element life & replace at 12 months | 18-Jul-2026 | REL-05 | Open |

#### Pro-Active Actions (Fleet / Unit Roll-out)
| RC | Action Description | Plan Date | PIC | Status |
|---|---|---|---|---|
| **X1** | Roll out alignment check to all Class-A blowers in OPP | 18-Aug-2026 | ROT-01 | Open |
| **X2** | Create coupling-element replacement register for OPP trains | 31-Aug-2026 | REL-05 | Open |

---

### 8. Preventive Actions, Risk Analysis & PM Schedule

#### Preventive Actions
| Item | Possible Root Cause | Preventive Action | Plan Date | PIC |
|---|---|---|---|---|
| **X3** | Route interval too long | Shorten `BL-5702` vibration route to weekly | 18-Jul-2026 | REL-05 |
| **P4** | Soft-foot | Correct soft-foot & re-shim baseplate `BL-5702` | 18-Jun-2026 | ROT-01 |

#### Risk Analysis of Corrective Actions
* **Corrective Action:** Shorten vibration route to weekly
* **Potential Risk:** Increased inspection workload
* **Countermeasure:** Use wireless vibration sensor for continuous trend (Target Date: 18-Jul-2026 | PIC: REL-05)

#### Established PM Schedule
* **PM-1:** 6-monthly laser alignment & soft-foot check `BL-5702` | **Group:** Rotating | **Interval:** 6-monthly
* **PM-2:** Coupling element inspection/replacement | **Group:** Rotating | **Interval:** 12-monthly
* **PM-3:** Weekly vibration trend review `BL-5702` | **Group:** Reliability | **Interval:** Weekly