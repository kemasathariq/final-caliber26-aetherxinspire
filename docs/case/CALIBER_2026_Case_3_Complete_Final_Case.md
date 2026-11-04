# CALIBER 2026, Case 2: Intelligent Manufacturing Dashboard

## Complete Final Case Reference and Evidence Pack

**Purpose.** This document consolidates the CALIBER 2026 Case 2 problem,
proposed solution, business case, technical architecture, governance,
implementation roadmap, five forensic hero-asset RCAs, the equipment and
incident dataset, and the supporting research. The source materials are
retained in full in the appendices so that detailed evidence, source
values, records, and references remain available.

**Primary case framing.** The case concerns an integrated petrochemical
operating environment with fragmented plant information, reactive
maintenance workflows, delayed root-cause investigation, and incomplete
action closure. The proposed response is a governed Intelligent
Manufacturing Dashboard, also described as a Single Pane of Glass,
connecting equipment condition, plant operating signals, incident
history, RCA knowledge, risk prioritization, and CAPA/PAA execution.

**Evidence convention.** Values described as actual, reported, observed,
or recorded below come from the supplied case files. Proposed
architecture, targets, and roadmap items are recommendations in the case
analysis. Research results are reported with their study-specific
qualifications. Illustrative energy and emissions values must not be
presented as measured plant telemetry because the supplied data
explicitly state that live energy and emissions signals are absent.

------------------------------------------------------------------------

# 1. Case at a glance

## 1.1 Operating context

The case is set in Chandra Asri Group's integrated petrochemical
operating environment, including facilities in Cilegon, Indonesia, and
Pulau Bukom/Jurong, Singapore. The fleet analysis covers 12 operating
plant units:

  Plant code   Plant code   Plant code
  ------------ ------------ ------------
  ZCU          ARP          OPP
  OP2          SMX          BRP
  OP3          NUP          CRP
  BDX          OPU          TKX

The enterprise context includes interdependent Production, Maintenance,
Reliability, Energy, HSE, Warehouse, Procurement, and Executive
Management functions. Their operating information is distributed across
PI historians, CMMS, EDMS, AIMS, and Abnormality Report (AR) records.

## 1.2 Core problem

The case identifies five connected operating problems.

1.  **Fragmented information.** Operational signals, maintenance
    records, engineering documents, and incident reports are stored
    across different systems and functional reporting loops.
2.  **Reactive maintenance.** Teams often reconcile data after a trip or
    failure, while fixed-interval maintenance can miss rapidly
    developing degradation.
3.  **Slow RCA and repeated investigation.** Engineers manually search
    for prior incidents and relevant procedures, limiting reuse of
    institutional knowledge.
4.  **Weak action closure.** CAPA/PAA follow-up is disconnected and a
    substantial share of fleet incident records remains unclosed.
5.  **Risk prioritization gaps.** Qualitative risk tiers do not always
    reflect realized financial consequences. KO-3201, for example, is a
    catastrophic high-loss event despite the case analysis identifying a
    mismatch between its risk tier and actual loss.

## 1.3 Fleet-level baseline from the supplied incident dashboard

  Measure                               Recorded value
  --------------------------- ------------------------
  Total incidents                                  380
  Total downtime                         2,261.1 hours
  Total loss                    USD 67,194.43 thousand
  Average loss per incident       USD 176.827 thousand
  Risk Closed                                      113
  CA/PA Execution                                   92
  RCA Process                                       71
  Risk Canceled                                     47
  Monitoring Result                                 37
  New Registered                                    20

The 220 records in the five non-closed status groups above are not all
necessarily overdue actions. The case analysis specifically
characterizes 220 of 380 records as unclosed, equivalent to 57.9
percent. This is calculated as 220 / 380 × 100 = 57.89 percent, rounded
to 57.9 percent.

### Incident distribution by discipline

  Discipline     Incident count
  ------------ ----------------
  ROT                       145
  INS                        87
  STA                        87
  ELE                        61
  **Total**             **380**

### Incident distribution and recorded loss by plant

  Plant         Incidents   Loss (USD thousand)
  ----------- ----------- ---------------------
  ZCU                  62             11,112.66
  ARP                  49              9,083.29
  OPP                  42              7,544.96
  OP2                  37              5,808.57
  SMX                  42              7,434.88
  BRP                  26              5,099.84
  OP3                  32              5,264.34
  NUP                  24              5,489.07
  CRP                  25              3,344.59
  BDX                  20              2,791.42
  OPU                  14              3,202.86
  TKX                   7              1,017.95
  **Total**       **380**         **67,194.43**

### Incident distribution by equipment type

  Equipment type     Incidents
  ---------------- -----------
  PU                        31
  CO                        25
  BL                        31
  FA                        17
  EM                        40
  VA                        15
  TX                        47
  HB                        21
  TK                        19
  RX                        22
  PZ                        24
  SX                        21

The listed equipment-type counts total 313, not 380. The source table
lists these 12 categories; do not assume the categories are exhaustive
or mutually exhaustive without checking the underlying incident
register.

------------------------------------------------------------------------

# 2. Financial opportunity and business case

## 2.1 Direct recovery opportunity

The case analysis identifies USD 18.24 million in actual realized
downtime losses across the 380 fleet-wide incident records as the direct
loss-recovery opportunity, referred to as SOM in the supplied analysis.

  ------------------------------------------------------------------------
  Financial measure                           Amount Interpretation
  --------------------- ---------------------------- ---------------------
  Actual realized                  USD 18.24 million Direct recovery
  downtime loss                                      opportunity stated in
                                                     the case analysis

  Potential risk                   USD 45.60 million Additional potential
  exposure                                           exposure stated in
                                                     the case analysis

  Total loss recovery              USD 63.84 million USD 18.24M + USD
  ceiling                                            45.60M
  ------------------------------------------------------------------------

The dashboard's total loss figure of USD 67.19443 million and the case
analysis's USD 18.24 million direct realized downtime loss are different
measures in the source material. They must not be treated as
interchangeable. The exact reconciliation is not supplied in the source
pack.

## 2.2 Five hero-asset loss profile

  ------------------------------------------------------------------------------------
  Asset       Failure        Severity        Downtime (h)    Production Estimated loss
                                                               loss (t) (USD thousand)
  ----------- -------------- -------------- ------------- ------------- --------------
  PU-2101B    Mechanical     Major                   18.5         251.6         226.44
              seal leakage                                              

  KO-3201     High radial    Catastrophic            32.0       1,760.0       1,584.00
              vibration trip                                            
              / bearing                                                 
              distress                                                  

  PM-4405B    Motor bearing  Moderate                 8.0         160.0         112.00
              overheating                                               
              trip                                                      

  HE-3301     Tube-side      Moderate                12.0         216.0         183.60
              fouling / duty                                            
              loss                                                      

  BL-5702     High vibration Major                   14.0         532.0         478.80
              / coupling                                                
              misalignment                                              

  **Total**                                      **84.5**   **2,919.6**   **2,584.84**
  ------------------------------------------------------------------------------------

The total row is the arithmetic sum of the five RCA summary records. It
is not a separate fleet-wide total.

## 2.3 Strategic and market context stated in the case analysis

  ------------------------------------------------------------------------
  Market layer                Case-analysis estimate Scope stated in
                                                     source
  --------------------- ---------------------------- ---------------------
  TAM                             USD 20.00+ billion Global smart
                                                     manufacturing and
                                                     industrial AI

  SAM                               USD 1.20 billion Southeast Asian
                                                     energy, refining, and
                                                     chemical digital
                                                     transformation

  SOM                              USD 18.24 million Direct realized
                                                     downtime recovery
                                                     across 12 plants
  ------------------------------------------------------------------------

These are estimates from the supplied strategic analysis, not
independently verified market-size calculations in this consolidated
document.

------------------------------------------------------------------------

# 3. Proposed solution

## 3.1 Product concept

**Intelligent Manufacturing Dashboard**, a governed Single Pane of Glass
for plant reliability and operational decision support.

The proposed solution brings together:

-   Fleet and plant overview.
-   Equipment health and condition trends.
-   Multi-parameter anomaly detection.
-   AI Root-Cause Indication with supporting evidence.
-   Financial-loss-weighted alert prioritization.
-   Similar-Incident Retrieval across historical AR records.
-   RCA and engineering knowledge retrieval.
-   CAPA/PAA action tracking and closure.
-   Human validation, approval, and audit history.
-   Energy and emissions views, explicitly marked illustrative until
    live instrumentation is available.

## 3.2 Core user workflows

1.  An operator or reliability engineer opens the fleet dashboard and
    identifies a plant, unit, or asset with an abnormal condition.
2.  The user opens the asset detail view and reviews recent operating
    signals, condition history, alarm state, and data quality.
3.  The anomaly service identifies abnormal trends and relevant signal
    combinations.
4.  The diagnostic service proposes ranked failure-mode hypotheses with
    confidence and evidence references.
5.  Similar-Incident Retrieval finds historical ARs and RCA records with
    comparable symptoms, equipment, and operating context.
6.  The user reviews the evidence, confirms or rejects hypotheses, and
    records the decision.
7.  The system presents recommended inspection or maintenance actions,
    their priority, owner, due date, and status.
8.  The responsible discipline specialist approves any formal action or
    CMMS update.
9.  The incident and action records are updated separately, preserving
    the distinction between incident lifecycle and action lifecycle.
10. Closed, verified RCA and CAPA/PAA records become governed knowledge
    for future retrieval and model evaluation.

## 3.3 Main dashboard modules

  -----------------------------------------------------------------------
  Module                  Main information        Primary user value
  ----------------------- ----------------------- -----------------------
  Executive / Fleet       Incident count,         See fleet-wide exposure
  Overview                downtime, losses,       and progress
                          status distribution,    
                          plant comparison        

  Plant / Unit Overview   Plant-level events,     Identify operational
                          critical assets, active hotspots
                          alerts, production      
                          context                 

  Asset Health            Tag-level trends,       Understand asset
                          operating state,        condition
                          condition history,      
                          limits                  

  Anomaly Detection       Drift, outliers,        Detect developing
                          vibration features,     abnormality
                          threshold crossings     

  AI Root-Cause           Candidate failure       Accelerate
  Indication              modes, confidence,      investigation
                          evidence and            
                          counter-evidence        

  Similar-Incident        Related ARs, RCA        Reuse prior plant
  Retrieval               narratives, repairs,    knowledge
                          outcomes                

  Alert Prioritization    Severity, criticality,  Focus response on
                          financial exposure,     highest consequence
                          trend, actionability    

  Action Tracking         CAPA/PAA owners, due    Improve action closure
                          dates, status, overdue  
                          items, verification     

  Knowledge Hub           SOPs, P&IDs, manuals,   Preserve and retrieve
                          shift logs, RCA records institutional knowledge

  Energy and Emissions    Consumption and         Support future energy
                          emissions views         intelligence; initial
                                                  data must be labeled
                                                  illustrative
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# 4. Technical architecture and data design

## 4.1 End-to-end architecture

``` mermaid
flowchart TD
    A[PI Historian and hourly process tags] --> D[Data ingestion and validation]
    B[CMMS work orders and maintenance history] --> D
    C[EDMS, SOPs, P&IDs, shift logs, AR and RCA documents] --> E[Document ingestion and indexing]
    D --> F[Time-series processing and feature engineering]
    F --> G[Anomaly detection and fault classification]
    E --> H[Vector retrieval and document evidence]
    G --> I[Asset ontology and knowledge graph]
    H --> I
    I --> J[Evidence-grounded AI RCA]
    J --> K[Human review and approval]
    K --> L[Alert prioritization and action tracking]
    L --> M[Governed Single Pane of Glass]
    L --> B
    K --> N[Verified RCA and lessons learned]
    N --> E
```

## 4.2 Data sources

  -----------------------------------------------------------------------
  Source                  Expected content        Intended use
  ----------------------- ----------------------- -----------------------
  OSIsoft PI Historian    Hourly process tags,    Time-series monitoring
                          flow, pressure,         and anomaly detection
                          temperature, vibration, 
                          motor current, run      
                          status                  

  CMMS                    Work orders, PM plans,  Maintenance context and
                          maintenance history,    action tracking
                          labor, parts, action    
                          status                  

  EDMS                    SOPs, P&IDs,            Grounded engineering
                          engineering documents,  reference
                          manuals                 

  AIMS                    Asset hierarchy, class, Asset identity and
                          criticality, equipment  ontology
                          metadata                

  AR / Incident Database  Incident records, risk  Similar-incident
                          cases, chronology,      retrieval and risk
                          loss, status            analysis

  RCA records             Verified root causes,   Explainable diagnostic
                          4P and 4M+1E findings,  evidence and learning
                          CAPA/PAA, PM updates    

  Condition monitoring    Weekly health readings, Asset health and
                          alarm/trip limits,      reliability KPIs
                          availability, MTBF,     
                          MTTR, PM compliance     
  -----------------------------------------------------------------------

## 4.3 Data coverage and constraints

-   The equipment dataset contains five monitored hero assets.
-   Each hero asset has 720 hourly observations, equivalent to 30 days,
    for seven listed variables, giving 3,600 hourly records across the
    five assets if all seven-variable rows are counted as one time
    record per asset-hour.
-   Each of the five hero assets has 26 weekly condition-monitoring
    readings.
-   The broader fleet incident database contains 380 incident records.
-   The strategic analysis states that hourly time-series baseline data
    are available for only five hero assets, while long-term time-series
    baseline data are missing for 375 of 379 unique plant equipment
    tags. Preserve this limitation when describing scale-up readiness.
-   Energy and emissions telemetry is absent from the initial data
    feeds. Phase 1 dashboard widgets for these measures must be labeled
    illustrative or modeled, not live measured data.
-   The dataset is a historical case pack. It does not establish a live
    production connection to PI, CMMS, or DCS.

## 4.4 Time-series and signal processing

The proposed Case 2 pipeline includes:

-   Data ingestion through secure REST, MQTT, and OPC-UA integration
    patterns, subject to plant cybersecurity approval.
-   Data validation for timestamps, missing values, duplicates,
    engineering units, tag identity, run status, and instrument quality.
-   Rolling statistical features such as Z-scores to identify abnormal
    drift.
-   Isolation Forest or comparable unsupervised anomaly detection for
    multivariate patterns.
-   FFT and harmonic analysis for rotating equipment vibration,
    particularly 1X and 2X components on KO-3201 and BL-5702.
-   Fault classification using equipment-specific labeled historical
    cases where data sufficiency permits.
-   Trend and operating-context correlation before any alert is
    escalated.

The source data are hourly for the hero-asset process tags. Hourly
samples alone are not sufficient to reconstruct high-frequency vibration
spectra or perform a true FFT diagnosis unless high-frequency waveform
data are separately available. The architecture should therefore
distinguish high-frequency vibration acquisition from hourly historian
summaries. Do not imply that the hourly dataset itself contains
waveform-level vibration data.

## 4.5 Knowledge Hub, RAG, GraphRAG, and ontology

The proposed Case 1 knowledge backend and Case 2 diagnostic context can
be combined as follows.

**Document retrieval layer** - Parse SOPs, P&IDs, shift logs,
engineering documents, maintenance reports, and 380 historical AR
records. - Chunk and index documents with source metadata. - Use
multilingual embedding models such as BGE-M3 or an appropriate embedding
service to support Indonesian and English search. - Store vectors in
Qdrant or FAISS using HNSW indexing where appropriate. - Return document
identifiers, page numbers, timestamps, and source excerpts.

**Ontology and graph layer** Represent explicit relationships such as:

`Plant → Unit → Equipment → Component → Failure Mode → Symptom → Sensor/Tag → Alarm → Incident → Root Cause → Corrective Action → Preventive Action`

Example relationship chain:

`KO-3201 → DE journal bearing → bearing babbitt distress → rising radial vibration → water-contaminated lube oil → leaking lube-oil cooler → AR-2026-ZCU-0142 → bearing replacement and oil-system flush`

**Grounded generation** - The LLM receives retrieved source passages and
graph relationships. - Each material claim must cite a source record,
historian point, work order, document page, alarm, or incident. - The
answer distinguishes measured evidence, historical analogy, model
inference, and unverified hypothesis. - Confidence is calibrated and
shown as a decision-support indicator, not as proof. - The system must
abstain or request inspection when evidence is insufficient or
conflicting.

GraphRAG's expected value is stronger relevance, relationship-aware
retrieval, traceability, and constraints on generation. The supplied
research does not establish a universal percentage reduction in
hallucinations.

## 4.6 Example AI RCA response format

**Candidate hypothesis:** Water ingress into lube oil causing
journal-bearing oil-film degradation.

**Evidence:** - KO-3201 drive-end radial vibration rose from 28 to 52
micrometres over five days before the event. - At the trip, vibration
reached 75 micrometres in the RCA chronology; the condition-monitoring
record reports 76.5 micrometres for the weekly failure reading. -
Lube-oil water content measured 1,800 ppm against a specification below
500 ppm. - Inspection found wiped/distressed bearing babbitt. - A
lube-oil cooler tube leak was confirmed.

**Historical match:** AR-2026-ZCU-0142.

**Confidence:** Must be computed from validated model calibration and
evidence coverage. Do not invent a confidence percentage.

**Required confirmation:** Specialist inspection and confirmation of
cooler leak, oil contamination pathway, and bearing damage.

------------------------------------------------------------------------

# 5. Alert prioritization and risk governance

## 5.1 Why financial-loss weighting is required

The supplied strategic analysis identifies a mismatch between
qualitative risk tier and actual financial consequence. It cites KO-3201
as a high-consequence compressor trip with USD 1.584 million realized
loss, while the risk matrix classification is described as
under-prioritizing the event. The solution should combine the formal
risk score with operational and financial impact.

## 5.2 Recommended prioritization inputs

-   Equipment criticality and class.
-   HSE and environmental consequence.
-   Current operating state and proximity to alarm/trip.
-   Rate of degradation and persistence of anomaly.
-   Production loss rate and expected downtime exposure.
-   Historical failure frequency and recurrence.
-   Confidence and evidence completeness.
-   Availability of standby equipment.
-   Actionability and time remaining before the risk becomes
    unacceptable.

The final formula and weights require reliability, process safety,
operations, and finance approval. Do not present unvalidated weights as
an established company risk model.

## 5.3 Status model

Maintain two independent state machines.

**Incident status:** `NEW REGISTERED`, `RCA PROCESS`, `CA/PA EXECUTION`,
`MONITORING RESULT`, `RISK CLOSED`, `RISK CANCELED`.

**Action status:** `Open`, `In Progress`, `Closed`, with any additional
controlled statuses agreed by the owner.

Incident status describes the Abnormality Report lifecycle. Action
status describes individual CAPA work items. An incident should not be
considered closed merely because one action is marked complete. Closure
requires the defined verification and approval process.

## 5.4 Human-in-the-loop and safety constraints

-   AI findings are probabilistic candidate hypotheses.
-   AI must not automatically change DCS setpoints, trips, interlocks,
    or actuator states.
-   The dashboard is read-only with respect to plant control loops.
-   AI must not automatically alter CMMS maintenance plans or close ARs.
-   Formal sign-off by relevant discipline specialists, such as ROT,
    STA, ELE, and INS, is required before approved work-plan changes or
    incident closure.
-   Safety-critical actions must follow approved site procedures and
    management-of-change requirements.
-   Every recommendation, source, model version, reviewer decision, and
    status transition should be auditable.
-   Sensitive plant topology, operating data, and intellectual property
    should remain within approved on-premise or private corporate
    infrastructure.

------------------------------------------------------------------------

# 6. Five forensic hero assets

The five full RCA reports are reproduced in Appendix B. The following
section summarizes their evidence and operational learning.

## 6.1 PU-2101B, Feed Charge Pump, ARP

-   **AR:** AR-2026-ARP-0117.
-   **Event:** Mechanical seal leakage on 12 March 2026 at 02:15.
-   **Impact:** 18.5 hours downtime, 251.6 tonnes production loss, USD
    226.44 thousand estimated loss.
-   **Chronology:** Minor seal weep observed on 11 March. Seal-flush
    low-flow alarm at 02:15 on 12 March, visible leakage, low suction
    pressure, and low-discharge-pressure trip. Seal faces were
    heat-checked/worn at inspection. Seal cartridge replaced and feed
    restored at 20:45.
-   **Key evidence:** Seal-flush flow 3--4 L/min versus 6 L/min minimum;
    NPSH margin below 0.5 m versus at least 1.0 m specification; suction
    pressure fell during feed swings.
-   **Verified root cause:** Intermittent dry-running caused by suction
    cavitation during feed swings and insufficient seal-flush flow, with
    no protective interlock.
-   **Contributors:** Feed ramp permitted above 2 T/H per minute;
    seal-flush Plan 11 absent from PM checklist; no
    low-NPSH/loss-of-flush interlock.
-   **Actions:** Install seal-flush flow switch and DCS alarm; add
    low-NPSH/loss-of-flush trip interlock; cap feed ramp at 1 T/H per
    minute; add Plan 11 to PM; roll out protection to the spare pump and
    API-682 seal pumps in ARP.
-   **Targets:** Zero recurrence; seal MTBF at least 24 months.
-   **PM:** Weekly seal-flush flow and seal-pot level check; quarterly
    seal condition and shaft run-out inspection.

## 6.2 KO-3201, Cracked Gas Compressor, ZCU

-   **AR:** AR-2026-ZCU-0142.
-   **Event:** High radial vibration trip on 29 April 2026 at 06:40.
-   **Impact:** 32.0 hours downtime, 1,760.0 tonnes production loss, USD
    1,584.00 thousand estimated loss.
-   **Chronology:** Drive-end vibration increased from 28 to 52
    micrometres over five days. High-high trip occurred at 75
    micrometres. Oil water content measured 1,800 ppm against a
    specification below 500 ppm. Bearing babbitt was wiped/distressed
    and a lube-oil cooler tube leak was confirmed. Bearing replacement,
    oil-system flush, and cooler tube plugging preceded restart.
-   **Verified root cause:** Water ingress through a leaking lube-oil
    cooler degraded lubricant film and caused journal-bearing babbitt
    distress.
-   **Key risk:** Catastrophic Class A rotating equipment failure with
    the largest loss among the five hero assets.
-   **Actions:** Repair or replace cooler bundle; add online
    water-in-oil monitoring and alarm; add cooler leak integrity checks;
    trend vibration and oil water content; update lube-oil sampling and
    response plan; extend the monitoring standard to sister compressor
    trains.
-   **Targets:** Zero recurrence; maintain oil water content below 500
    ppm and vibration below approved alarm/trip limits.
-   **PM:** Routine oil-water monitoring, lube-oil cooler integrity
    checks, and continuous vibration monitoring as specified in the
    source RCA.

## 6.3 PM-4405B, Cooling Water Pump Motor, NUP

-   **AR:** AR-2026-NUP-0089.
-   **Event:** Motor bearing overheating trip.
-   **Impact:** 8.0 hours downtime, 160.0 tonnes production loss, USD
    112.00 thousand estimated loss.
-   **Verified root cause:** Grease degradation associated with an
    over-extended, non-risk-based re-lubrication interval.
-   **Contributors:** Fixed calendar lubrication interval did not
    adequately reflect actual operating condition and bearing duty.
-   **Actions:** Review lubrication interval against operating
    condition; standardize grease type and quantity; improve lubrication
    records and condition checks; consider condition-based lubrication
    triggers for sister assets.
-   **Targets and detailed action owners, dates, parameter checks, and
    PM schedule:** Refer to the complete RCA 3 report in Appendix B. The
    source report is retained without omission.

## 6.4 HE-3301, Feed/Effluent Heat Exchanger, ZCU

-   **AR:** AR-2026-ZCU-0165.
-   **Event:** Tube-side fouling, duty loss, and high differential
    pressure on 21 May 2026 at 09:00.
-   **Impact:** 12.0 hours downtime, 216.0 tonnes production loss, USD
    183.60 thousand estimated loss.
-   **Key evidence:** Tube-side differential pressure reached 0.9 bar
    versus 0.6 bar limit; duty fell to approximately 65 percent of
    design; feed heavy-ends were 2.4 percent versus a design limit below
    1.5 percent.
-   **Verified root cause:** Accelerated tube-side coke/polymer fouling
    driven by higher-than-design feed heavy-ends, allowed to progress
    because there was no differential-pressure cleaning trigger or
    fouling KPI.
-   **Contributors:** Upstream filter differential pressure not trended;
    fouling factor and duty KPI absent from dashboard.
-   **Actions:** Add dP-based cleaning trigger and alarm; tighten
    heavy-ends control and filtration; apply trigger logic to parallel
    exchangers; review upstream fractionation cut-point control; add
    fouling factor and duty KPI; trend upstream filter dP.
-   **Targets:** No unplanned rate cut; dP below 0.6 bar and duty above
    90 percent.
-   **PM:** Daily dP and duty trend review; bundle inspection and
    cleaning at condition trigger or next turnaround.

## 6.5 BL-5702, Product Blower, OPP

-   **AR:** AR-2026-OPP-0203.
-   **Event:** High vibration and blower stop on 17 June 2026 at 04:30.
-   **Impact:** 14.0 hours downtime, 532.0 tonnes production loss, USD
    478.80 thousand estimated loss.
-   **Key evidence:** Vibration rose from 4.2 to 8.5 mm/s with rising 2X
    harmonic; alarm reached 11 mm/s; laser alignment found 0.35 mm
    offset against a specification below 0.05 mm; soft-foot measured
    0.12 mm.
-   **Verified root cause:** Coupling misalignment aggravated by
    soft-foot and an over-aged elastomer coupling element, not detected
    because periodic alignment checks were absent and the monthly
    vibration route missed a two-day rise.
-   **Actions:** Add periodic laser alignment and soft-foot checks;
    track coupling element life and replace at 12 months; roll out
    checks to Class A blowers; create coupling-element replacement
    register; shorten vibration route to weekly; correct soft-foot and
    re-shim baseplate.
-   **Targets:** No misalignment-related blower stop; vibration below 7
    mm/s and alignment below 0.05 mm.
-   **PM:** Six-monthly laser alignment and soft-foot check; 12-month
    coupling inspection/replacement; weekly vibration trend review.

------------------------------------------------------------------------

# 7. Predictive maintenance and early-warning design

## 7.1 Asset-specific leading indicators

  -----------------------------------------------------------------------
  Asset                   Primary leading         Supporting context
                          indicators              
  ----------------------- ----------------------- -----------------------
  PU-2101B                Seal-flush flow,        Feed ramp rate,
                          suction pressure, NPSH  seal-flush PM
                          margin, vibration,      compliance, run status
                          bearing/process         
                          temperature             

  KO-3201                 DE radial vibration     Cooler integrity, oil
                          trend, lube-oil water   sample history,
                          content, lube-oil       compressor load
                          supply pressure,        
                          bearing metal           
                          temperature             

  PM-4405B                Motor bearing           Grease type/quantity,
                          temperature, vibration, lubrication interval,
                          lubrication condition   duty cycle

  HE-3301                 Tube-side differential  Feed composition, flow,
                          pressure, heat duty,    temperature, cleaning
                          feed heavy-ends,        history
                          upstream filter dP      

  BL-5702                 Overall vibration,      Coupling age, bearing
                          1X/2X harmonic          condition, route
                          features, alignment     interval, operating
                          offset, soft-foot       load
  -----------------------------------------------------------------------

## 7.2 Warning lead-time measurement

Do not claim a universal prediction horizon such as a fixed number of
days for journal-bearing distress or a fixed number of hours for
coupling misalignment. The supplied research does not confirm a
universal peer-reviewed benchmark.

For each fault class, define:

`Warning lead time = confirmed functional failure timestamp - first actionable diagnostic alarm timestamp`

This convention yields a positive value when the alarm occurs before
failure. Record the timestamps and report the median, 10th percentile,
90th percentile, and false-alarm rate by fault class. The timestamp
definition must be consistent across assets.

The operational sequence is:

`Detection → Diagnosis → Actionable alarm → Maintenance window → Functional failure`

## 7.3 Research evidence and limitations

-   A 2020 review describes predictive maintenance as using machine
    learning for fault detection and diagnosis to reduce downtime,
    increase equipment utilization, and extend remaining useful life.
-   A 2023 manufacturing study evaluated more than 20 ML/DL models; Deep
    Forest and Gradient Boosting exceeded 90 percent average accuracy,
    while logistic regression and LSTM exceeded 80 percent. The study
    used a synthetic predictive-maintenance dataset, so the accuracy
    figures are not measured plant downtime reductions.
-   A 2021 petrochemical-context study combined sensor data and
    maintenance reports using XGBoost and Shapley-value interpretability
    to support diagnostic understanding.
-   A 2026 petrochemical multi-sensor study combined vibration,
    temperature, and electrical-current data with wavelet packet
    features and an LSTM model, reporting 99.50 percent classification
    accuracy in its experiment. This is not a downtime, MTTR, or cost
    reduction figure.
-   A 2025 fertilizer-manufacturing study reported 30.5 percent lower
    MTTR, 18.4 percent lower maintenance cost, 25 percent higher MTBF,
    and OEE improvement from 77.6 to 83.7 percent. It assessed a broader
    data-driven maintenance and workforce framework, so the improvements
    must not be attributed solely to AI.
-   A 2021 oil-industry study proposed a smart predictive-maintenance
    architecture and feasibility assessment but did not provide a
    controlled before-and-after downtime percentage.

**Business-case rule:** Use research as evidence that the pathway is
credible. Do not promise a universal percentage reduction in downtime,
MTTR, or maintenance cost without a plant-specific baseline and
intervention study.

------------------------------------------------------------------------

# 8. KPI framework

## 8.1 Operational and reliability KPIs

  -----------------------------------------------------------------------
  KPI                     Definition /            Measurement note
                          calculation             
  ----------------------- ----------------------- -----------------------
  Unplanned downtime      Sum of downtime hours   Separate planned and
                          attributable to         unplanned windows
                          unplanned events        

  Availability            (Period hours -         Use consistent asset
                          downtime hours) /       boundary and period
                          period hours × 100      

  MTBF                    Operating time / number Define whether calendar
                          of functional failures  or operating hours are
                                                  used

  MTTR                    Total repair time /     Define start and end
                          number of repairs       timestamps consistently

  Production loss         Tonnes of production    Reconcile with
                          lost during event       production historian

  Estimated financial     Production loss ×       Preserve source
  loss                    applicable product      calculation basis
                          value, plus separately  
                          defined costs if        
                          included                

  PM compliance           Completed scheduled PM  Define grace period and
                          / scheduled PM × 100    exclusions

  Fault detection         True positives relative Requires adjudicated
  precision/recall        to model alerts and     labels
                          labeled events          

  Warning lead time       Failure timestamp minus Report distribution by
                          first actionable alarm  failure class
                          timestamp               

  False alarm rate        False actionable alarms Specify denominator
                          / total actionable      
                          alarms or asset-time    

  Similar incident        Precision@k, Recall@k,  Create expert-labeled
  retrieval quality       expert relevance score  evaluation set

  RCA evidence coverage   Claims with source      Audit source references
                          evidence / total        
                          material claims         

  CAPA closure rate       Verified closed actions Avoid mixing due and
                          / actions due or total  all-open denominators
                          actions, explicitly     
                          stated                  

  Incident closure rate   Closed incidents /      Keep incident status
                          total incidents         separate from action
                                                  status
  -----------------------------------------------------------------------

## 8.2 Case-analysis targets and roadmap targets

The supplied analysis proposes the following targets. They are proposed
targets, not measured achieved results.

-   Validate all five hero-asset RCA signatures during Phase 1.
-   Similar-Incident Retrieval accuracy above 90 percent in Phase 2. The
    exact metric must be operationally defined before claiming success.
-   Reduce unclosed fleet risks from 57.9 percent to below 15 percent in
    Phase 3.
-   Capture the stated USD 18.24 million SOM as a long-term
    value-capture ambition. This is a ceiling/opportunity framing, not a
    guaranteed return.
-   Sustain applicable ISO 9001 quality compliance.
-   Zero unprogrammed Class A trips is a proposed ambition and requires
    a defined observation period and scope.

------------------------------------------------------------------------

# 9. Implementation roadmap

  ----------------------------------------------------------------------------------
  Phase          Timeframe      Deliverables   Scope              Proposed milestone
                                                                  / KPI
  -------------- -------------- -------------- ------------------ ------------------
  Phase 1        Months 1--3    Hero-asset PoC Ingest five        Validate five RCA
                                platform and   hero-asset PI tag  signatures;
                                prototype      feeds, condition   complete 3-minute
                                               histories, and     demo video
                                               five RCA reports   
                                               into Figma/HTML    
                                               prototype          

  Phase 2        Months 4--8    Fleet-wide     Expand data        Similar-Incident
                                ingestion and  pipelines toward   Retrieval accuracy
                                AI tuning      379 tags across 12 above 90 percent,
                                               plants; tune       with metric
                                               vector search      definition and
                                               across 380 AR      expert test set
                                               records            

  Phase 3        Months 9--12   Enterprise     Central Single     Reduce unclosed
                                rollout and    Pane of Glass;     fleet risks from
                                action         CMMS work-order    57.9 percent to
                                tracking       tracking           below 15 percent;
                                               integration        pursue zero
                                                                  unprogrammed Class
                                                                  A trips

  Phase 4        Ongoing        Continuous     Add live           Track value
                                governance and energy/emissions   capture against
                                energy         tags; retrain and  USD 18.24 million
                                integration    evaluate models    opportunity;
                                               using verified     sustain quality
                                               closed RCA data    governance
  ----------------------------------------------------------------------------------

## 9.1 Suggested delivery workstreams

1.  Product and UX: dashboard information architecture, asset
    drill-down, alert workflow, accessibility, demo narrative.
2.  Data engineering: tag mapping, data quality, historian ingestion,
    CMMS/EDMS/AR connectors.
3.  Reliability engineering: failure taxonomy, equipment ontology,
    operating envelopes, engineering limits, RCA validation.
4.  AI/ML: anomaly detection, fault classification, retrieval
    evaluation, explainability, confidence calibration.
5.  Governance and cybersecurity: access control, on-premise/private
    inference, read-only control boundary, audit trails, human approval.
6.  Change management: role definitions, training, SOP updates, PM
    revisions, adoption measurement.

------------------------------------------------------------------------

# 10. Strategic framework synthesis

## 10.1 McKinsey 7S

  -----------------------------------------------------------------------
  Element                             Case implication
  ----------------------------------- -----------------------------------
  Strategy                            Future-ready operational excellence
                                      through reliability, predictive
                                      maintenance, energy/emissions
                                      intelligence, and knowledge
                                      retention

  Structure                           Cross-functional governance
                                      connecting Production, Maintenance,
                                      Reliability, HSE, Procurement, and
                                      management

  Systems                             PI, CMMS, EDMS, AIMS, and AR
                                      integration

  Shared Values                       Safety, quality, environmental
                                      accountability, compliance, and
                                      continuous improvement

  Style                               Move from reactive firefighting to
                                      proactive, evidence-led decisions

  Staff                               Human-in-the-loop domain experts
                                      and multidisciplinary 8D teams

  Skills                              Process engineering,
                                      rotating/static equipment
                                      reliability, AI, SPC, and
                                      structured RCA
  -----------------------------------------------------------------------

## 10.2 PESTEL

-   **Political:** National energy and environmental mandates,
    regulatory transparency, and oversight by Indonesian and Singaporean
    authorities.
-   **Economic:** Feedstock volatility, heavy-ends excursions, and large
    downtime losses.
-   **Social:** Community health, spill prevention, environmental
    justice, and public accountability.
-   **Technological:** Industrial DataOps, GenAI retrieval, digital
    twins, wireless vibration sensors, and online water-in-oil sensing.
-   **Environmental:** Decarbonization, energy efficiency, emissions
    monitoring, waste heat recovery, and hazardous material management.
-   **Legal:** Workplace safety, equipment standards, environmental
    obligations, and corporate IP terms.

## 10.3 Porter's Five Forces

-   Threat of new entrants: low, due to capital, permitting, and
    infrastructure barriers.
-   Buyer power: high, due to commodity markets and alternative
    suppliers.
-   Supplier power: high, due to feedstock concentration and
    feed-quality variation.
-   Threat of substitutes: moderate, due to bio-based polymers, chemical
    recycling, and alternative materials.
-   Competitive rivalry: very high, driving pressure for availability,
    low MTTR, and reduced unplanned downtime.

## 10.4 Value chain and 7Ps

The supplied strategic analysis maps inbound logistics, operations,
outbound logistics, marketing and sales, service, firm infrastructure,
human resources, technology development, and procurement to the relevant
digital enablers. It also identifies data silos, manual reconciliation,
knowledge search, fixed-interval maintenance, and delayed response as
sources of operational waste.

## 10.5 Lean 7 Wastes

The case maps operational waste to digital opportunities: - Waiting:
delays in obtaining information and approvals. - Transport: scattered
operational documents and disconnected systems. - Over-processing:
repeated manual tag validation and duplicate reports. - Inventory:
fixed-interval spare and maintenance practices that do not reflect asset
condition. - Motion: engineers manually searching separate databases for
RCA context. - Defects: recurring equipment failures and downtime
losses. - Overproduction: redundant reports and duplicated status
tracking.

------------------------------------------------------------------------

# 11. Competition submission requirements

The supplied case analysis lists these requirements for the CALIBER 2026
submission.

## 11.1 Demo video

-   Maximum duration: 3 minutes, or 180 seconds.
-   Demonstrate logical workflows and prototype navigation.
-   Present a clear problem-to-solution story.
-   Keep narration and written materials in English.

## 11.2 Interactive prototype

Use a high-fidelity Figma prototype or accessible HTML prototype
demonstrating: - Single Pane of Glass. - AI Root-Cause Indication. -
Alert Prioritization. - Similar-Incident Retrieval. - Action Tracking.

## 11.3 Core presentation deck

Maximum 7 slides: 1. Cover and case selection. 2. Background and problem
statement. 3. Proposed solution and architecture. 4. Business impact and
KPI evaluation. 5. Feasibility, governance, and roadmap. 6. Conclusion.
7. Team profile, including university, supervisor, and member details.

## 11.4 Submission constraints

-   Combined file size: maximum 10 MB.
-   Written materials and video narration: English.
-   The source analysis states a 24-hour hackathon readiness requirement
    for advancement to the Final Stage in Jakarta, 4--5 November 2026.

## 11.5 IP note

The supplied strategic analysis states that CALIBER 2026 submission
proposals and prototypes become corporate property upon submission.
Confirm the exact legal wording and applicable competition terms with
the official guidebook before relying on this summary.

------------------------------------------------------------------------

# 12. Key assumptions, caveats, and data-quality checks

1.  The source dataset is a converted PDF. The conversion notes say the
    source terminology and values were preserved, but table layouts and
    headers may be imperfectly reconstructed.
2.  The incident dashboard total loss is USD 67,194.43 thousand. The
    strategic analysis separately identifies USD 18.24 million actual
    downtime loss and USD 45.60 million potential exposure. These values
    require reconciliation before being combined in an ROI calculation.
3.  The 380 incident records are not the same as the five hero-asset RCA
    cases. The five hero assets are forensic examples, not a
    statistically representative sample of all incidents.
4.  The equipment dataset has 720 hourly rows per hero asset and 26
    weekly condition records per hero asset. It does not provide
    equivalent detailed time-series coverage for the whole fleet.
5.  High-frequency vibration waveform data are not demonstrated in the
    hourly process data. FFT-based 1X/2X analysis requires appropriate
    high-frequency acquisition or precomputed spectral features.
6.  Energy and emissions telemetry is absent. Any early dashboard
    representation must be visibly marked illustrative.
7.  AI model accuracy from controlled research is not equivalent to
    downtime reduction or plant ROI.
8.  Research-reported maintenance improvements are case-specific and
    cannot be assigned solely to AI where the study evaluated broader
    operational frameworks.
9.  A fixed warning lead time for bearing distress or coupling
    misalignment is not established by the supplied research. Calibrate
    lead-time distributions from plant-specific event histories.
10. GraphRAG is proposed to improve retrieval relevance and
    traceability. No quantified universal hallucination-reduction
    percentage is established in the supplied research.
11. The 7Ps and Lean sections in the source analysis are strategic
    frameworks. They should be presented as analysis, not as
    independently measured outcomes.
12. All safety-critical decisions remain with authorized plant personnel
    and approved procedures.

------------------------------------------------------------------------

# 13. Complete source appendices

The following appendices preserve the four supplied source files in
full. They are included to retain source-level detail, raw values,
tables, incident records, RCA evidence, action owners, planned dates,
and bibliography. The source text is intentionally not summarized or
selectively omitted.

# Appendix A. Original strategic and hackathon analysis

### Strategic Analysis Report: CALIBER 2026 & Petrochemical Operational Excellence Synthesis \#### 1. Strategic Overview & Organizational Alignment (McKinsey 7S Framework) \##### Context & Strategic Importance In complex, capital-intensive, and integrated petrochemical operations---such as Chandra Asri Group's processing complexes across Cilegon (Indonesia) and Pulau Bukom/Jurong (Singapore)---achieving sustained operational excellence requires absolute alignment between technology, operational workflows, and organizational structures. The deployment of advanced digital solutions, Artificial Intelligence (AI), and real-time process monitoring cannot succeed as isolated technical installations. Instead, digital transformation agendas must harmonize across the enterprise to convert fragmented operational data into proactive, risk-mitigated decision-making. Organizational alignment ensures that AI-driven insights translate directly into downtime reduction, prolonged asset lifespan, superior safety performance, and structured knowledge preservation across multi-plant environments. \##### Synthesis & Framework Execution Evaluating the enterprise landscape across the seven internal dimensions of the McKinsey 7S Framework reveals the structural operational dynamics governing Chandra Asri Group's facilities: \* **Strategy:** The overarching strategic mandate focuses on achieving "Future-Ready Operational Excellence" across knowledge retention, equipment reliability, energy efficiency, and smart manufacturing. This entails transitioning from reactive time-based maintenance to predictive analytics, establishing real-time energy and emissions tracking, and converting scattered operational logs into an integrated knowledge hub. \* **Structure:** Operations are distributed across interdependent cross-functional units, including Production, Maintenance, Reliability, Energy, Health, Safety & Environment (HSE), Warehouse, Procurement, and Executive Management. Each function traditionally operates within specialized reporting loops, necessitating unified cross-functional governance to break down data silos. \* **Systems:** The core industrial data architecture relies on OSIsoft PI time-series historians capturing hourly process tags (e.g., flow rates, temperatures, pressures, vibration, motor current), Computerized Maintenance Management Systems (CMMS), Engineering Document Management Systems (EDMS), Asset Information Management Systems (AIMS), and a fleet-wide Incident Database tracking Abnormality Reports (AR). \* **Shared Values:** The organizational culture is anchored in a commitment to continuous operational improvement, strict workplace safety, environmental stewardship, transparent data governance, and high-integrity corporate compliance. \* **Style:** Operational leadership is actively shifting from a reactive "firefighting" posture---characterized by manual data reconciliation following unplanned unit trips---to a data-driven, proactive style enabled by centralized single-pane-of-glass dashboards and AI-assisted root-cause indications. \* **Staff:** Human-in-the-loop oversight remains mandatory for all AI-generated recommendations and action tracking. Problem-solving relies on multidisciplinary teams, reinforced externally through open innovation ecosystems such as CALIBER 2026, which engages 2-to-3-member student innovation teams operating under direct faculty supervision. \* **Skills:** The required organizational skill matrix bridges deep chemical domain expertise (e.g., process thermodynamics, rotating equipment dynamics, static equipment fouling) with modern digital capabilities, including prompt engineering, predictive analytics, statistical process control (SPC), and structured root-cause analysis methodologies ( \$4\\text{M}+1\\text{E}\$ , \$4\\text{P}\$ , Fishbone diagrams, and 5-Why analysis). \##### McKinsey 7S Organizational Alignment Matrix \| 7S Element \| Specific Petrochemical Operational Application & Strategic Value \| \| ------ \| ------ \| \| **Strategy** \| Mandate for smart manufacturing, AI-driven predictive maintenance, energy/emissions intelligence, and institutional knowledge preservation across 12 operating plants. \| \| **Structure** \| Cross-functional operational alignment bridging Production, Reliability, Maintenance, HSE, Procurement, and Executive Management to break down functional data silos. \| \| **Systems** \| Integration of hourly PI time-series tag historians, CMMS maintenance records, EDMS, AIMS, and central Abnormality Report (AR) Incident Databases into unified AI dashboards. \| \| **Shared Values** \| Future-Ready Operational Excellence ethos emphasizing process safety, uncompromised product quality, environmental accountability, and open innovation governance. \| \| **Style** \| Cultural transition from reactive firefighting and post-trip manual reconciliation to proactive, predictive operational decision-making supported by real-time alert mechanisms. \| \| **Staff** \| Human-in-the-loop subject matter experts validating AI suggestions, supported by cross-functional 8D teams and CALIBER 2026 academic-industry collaboration frameworks. \| \| **Skills** \| Interdisciplinary capabilities blending process chemistry and rotating equipment reliability with predictive modeling, prompt engineering, and structured \$4\\text{M}+1\\text{E}\$ / 5-Why root-cause analysis. \| Having established internal organizational alignment across structural and technical pillars, the enterprise evaluation shifts to external macro-environmental pressures and regulatory frameworks. \#### 2. Macro-Environmental & Regulatory Audit (PESTEL Analysis) \##### Context & Strategic Importance Petrochemical manufacturing does not occur in isolation; it is deeply influenced by geopolitical mandates, raw material price swings, strict regulatory compliance standards, and societal demands for environmental transparency. A comprehensive PESTEL audit ensures that technological investments---such as AI-driven predictive maintenance and centralized plant monitoring---are designed to mitigate external regulatory risks, shield operating margins against raw material volatility, and satisfy legal reporting obligations. \##### PESTEL Categorization \* **Political:** Facilities operate under national energy security mandates and stringent regulatory transparency requirements. Public records governance models---such as the Freedom of Information Law (FOIL) administered by environmental regulators like the New York State Department of Environmental Conservation (DEC)---serve as global audit benchmarks for public disclosures, permit compliance logs, and remediation tracking. Within Chandra Asri Group's primary operating jurisdictions, physical assets strictly adhere to environmental enforcement governed by the Ministry of Environment and Forestry (KLHK) in Indonesia and the National Environment Agency (NEA) in Singapore. \* **Economic:** Process operations face extreme unit margin sensitivity driven by global crude oil and feed volatility. Heavy-ends variations in feedstock directly induce operational disruptions, such as thermal preheat duty losses. Unprogrammed downtime carries severe financial penalties; for example, a single compressor trip (such as the KO-3201 event) can incur \$1.58M in actual realized financial losses (\$ 2.06M total loss including potential exposure). \* **Social:** Industrial facilities maintain accountability to surrounding local communities and public health stakeholders. Compliance monitoring, spill reporting, and environmental justice frameworks (aligned with DEC/NOAA/EHN benchmarks) mandate zero-harm operations and rapid containment of hazardous releases. \* **Technological:** The rapid evolution of Industrial DataOps, generative AI knowledge retrieval systems, digital twins, and advanced online instrumentation (such as wireless vibration transducers and online optical water-in-oil sensors) presents immediate opportunities to eliminate operational blind spots. \* **Environmental:** National decarbonization targets and strict emissions frameworks require continuous monitoring of energy consumption, greenhouse gas emissions, and waste heat recovery efficiency. Furthermore, site remediation, bulk storage regulation, and hazardous substance management require strict environmental control. \* **Legal:** Industrial operators must comply with mandatory workplace safety standards, equipment manufacturing standards (ISO 9001:2015, BIS IS 8309, CE certification), and intellectual property governance terms. Intellectual property policies governing innovation programs (such as CALIBER 2026 hackathons) stipulate that all submitted technological proposals and prototypes become corporate property upon submission. \##### PESTEL Environmental Audit Matrix \| Category \| Key External Driver \| Operational Risk / Opportunity \| Strategic Countermeasure \| \| ------ \| ------ \| ------ \| ------ \| \| **Political** \| Environmental public records transparency (DEC FOIL benchmark) & national regulatory oversight (KLHK / NEA). \| **Risk:** Exposure from public disclosure of environmental non-compliance or unmitigated plant incident logs. \| Implement automated environmental compliance logging and real-time emissions/spill tracking. \| \| **Economic** \| Feedstock volatility & extreme cost of unprogrammed downtime (\$1.58M single-event loss). \| **Risk:** Margin erosion from feedstock quality variations and unscheduled unit trips. \| Deploy AI predictive maintenance and feed quality limit interlocks to prevent process trips. \| \| **Social** \| Public health accountability, ESG metrics, & community environmental justice. \| **Risk:** Reputational damage and community backlash from containment failures or flare events. \| Enforce immediate containment protocols (8D Step D3) and automated environmental alerting. \| \| **Technological** \| Rapid adoption of Industrial DataOps, GenAI, & online condition monitoring. \| **Opportunity:** Eliminating manual inspection cycles via wireless vibration and online oil-purity sensing. \| Integrate continuous online sensor networks directly into AI root-cause indication dashboards. \| \| **Environmental** \| Carbon compliance, waste minimization, & hazardous substance bulk storage laws. \| **Risk:** Regulatory fines and thermal efficiency losses due to unmonitored exchanger fouling. \| Implement real-time exchanger differential pressure ( \$\\Delta P\$ ) duty tracking and automated cleaning triggers. \| \| **Legal** \| Equipment certification standards (ISO/CE/BIS) & corporate IP governance. \| **Risk:** Liability from non-certified electrical/mechanical parts and IP ownership disputes. \| Mandate strict vendor certification (ISO/BIS/CE) and robust hackathon IP terms and conditions. \| Understanding macro-environmental pressures provides the foundation for positioning the enterprise within the competitive dynamics of the regional chemical market. \#### 3. Competitive Dynamics & Market Trajectory (Porter's 5 Forces & TAM-SAM-SOM) \##### Context & Strategic Importance Capital allocation toward industrial AI platforms, digital twin infrastructure, and automated reliability tools requires clear market justification. Sizing the target market and evaluating competitive positioning ensures that digital investments generate measurable returns by eliminating operating waste, extending equipment life, and recovering lost production output within highly competitive regional markets. \##### Porter's Five Forces Synthesis The competitive intensity surrounding Southeast Asian energy, refining, and petrochemical manufacturing is evaluated below: \* **Threat of New Entrants (Low):** Significant capital expenditure requirements (multi-billion dollar investments for integrated crackers and chlor-alkali complexes), complex environmental permitting, strict regulatory barriers, and required access to integrated deep-water port infrastructure create substantial barriers to entry. \* **Bargaining Power of Buyers (High):** Commodity buyers of polyolefins, resins, olefins, and aromatics operate in transparent global spot markets with access to alternative regional suppliers. Buyers demand strict technical product specifications, placing high pressure on chemical manufacturers to maintain low cost structures and zero defect rates. \* **Bargaining Power of Suppliers (High):** Feedstock availability is concentrated among major energy suppliers. Volatility in upstream feed quality---such as elevated heavy-ends concentrations exceeding design specifications ( \$2.4\\%\$ actual vs. \$\<1.5\\%\$ design limit)---presents severe operational risks, causing accelerated heat exchanger fouling and unit rate cutbacks. \* **Threat of Substitutes (Moderate):** Emerging bio-based polymers, chemical recycling technologies, and alternative material substitutes represent growing long-term threats, driving established petrochemical producers to optimize thermal efficiency and minimize carbon intensity per ton of product. \* **Rivalry Among Existing Competitors (Very High):** Intense regional competition across Southeast Asian refining and petrochemical hubs (e.g., Singapore's Jurong/Pulau Bukom and Indonesia's Cilegon complexes) forces producers to maximize plant availability ( \$\>98\\%\$ ), minimize Mean Time To Repair (MTTR), and eliminate unprogrammed downtime to safeguard operational margins. *Strategic Insight on Risk Matrix Misalignment:* Empirical analysis of historical fleet data reveals a critical flaw in traditional qualitative risk matrices. For example, asset KO-3201 is categorized as Pre-Risk Tier II despite suffering a catastrophic \$1.58M actual realized loss (the largest single event in the fleet), whereas smaller-loss events are classified as Tier III. Traditional risk models under-prioritize high-consequence, low-frequency turbomachinery degradation. To solve this, the enterprise must deploy a dynamic, financial-loss-weighted Alert Prioritization Engine that combines qualitative risk scores with real-time financial impact projections. \##### TAM-SAM-SOM Market Sizing Analysis +-----------------------------------------------------------------------+ \| TOTAL ADDRESSABLE MARKET (TAM) \| \| Global Smart Manufacturing & Industrial AI Market: \$20.00+ Billion \| \| +-------------------------------------------------------------------+ \| \| \| SERVICEABLE ADDRESSABLE MARKET (SAM) \| \| \| \| SEA Energy, Refining & Chemical Digital Transformation: \$1.20 B \| \| \| \| +---------------------------------------------------------------+ \| \| \| \| \| SERVICEABLE OBTAINABLE MARKET (SOM) \| \| \| \| \| \| Direct Realized Downtime Recovery (12 Plants): \$18.24 Million \| \| \| \| \| +---------------------------------------------------------------+ \| \| \| +-------------------------------------------------------------------+ \| +-----------------------------------------------------------------------+ 1. **Total Addressable Market (TAM) - \$20.00+ Billion:** Represents the global smart manufacturing, industrial IoT, and AI predictive maintenance market across continuous process industries, encompassing software, hardware, and integration services. 2. **Serviceable Addressable Market (SAM) - \$1.20 Billion:** Slices the TAM to focus specifically on digital transformation, enterprise asset management, and advanced process control solutions within the Southeast Asian refining, energy, and petrochemical sector. 3. **Serviceable Obtainable Market (SOM) - \$18.24 Million:** Quantifies the immediate financial recovery opportunity across Chandra Asri Group's 12 operating plants (ZCU, ARP, OPP, OP2, SMX, BRP, OP3, NUP, CRP, BDX, OPU, TKX). Mathematically, this \$18.24M (\$ 18,240k USD) represents *direct actual realized downtime loss recovery* recorded across 380 fleet-wide incident records. When accounting for potential risk exposure ( \$45.60M), the total financial loss recovery ceiling expands to **\$ 63.84 Million (\$63,840k USD)**, defining the maximum value capture potential. \##### TAM-SAM-SOM Market Opportunity Table \| Market Tier \| Geographic / Industry Focus \| Financial Valuation \| Operational Scope & Asset Target \| \| ------ \| ------ \| ------ \| ------ \| \| **TAM** \| Global Process Industry Smart Manufacturing \| **\$20.00+ Billion** \| Global industrial AI, predictive maintenance, and enterprise DataOps architectures. \| \| **SAM** \| Southeast Asian Refining & Petrochemicals \| **\$1.20 Billion** \| Industrial AI & reliability software across regional chemical, refining, and power assets. \| \| **SOM** \| Chandra Asri Group Fleet Operations \| **\$18.24 Million** \| Direct realized loss recovery across 12 plants (\$63.84M total exposure ceiling). \| Linking market dynamics and competitive strategy to operational execution requires deconstructing the enterprise value chain and commercial delivery capabilities. \#### 4. Enterprise Value Chain & Commercial Positioning (Value Chain & Marketing Mix 7Ps) \##### Context & Strategic Importance To capture the full financial value of industrial AI investments, technical capability must directly align with enterprise value chain activities and commercial positioning. Deconstructing internal operations through the Value Chain and Marketing Mix ( \$7\\text{Ps}\$ ) frameworks highlights specific operational bottlenecks and identifies the corresponding AI enablers required to maintain market leadership. \##### Value Chain & 7Ps Audit \###### Primary Value Chain Activities \* **Inbound Logistics:** Verification of raw material feed specifications. *Bottleneck:* Feed heavy-ends variations causing undetected heat exchanger fouling. *AI Enabler:* Online feed composition tracking & alert triggers. \* **Operations:** Cracking, polymerization, utility generation, and heat transfer. *Bottleneck:* Unplanned machinery trips (e.g., compressor vibration, pump cavitation). *AI Enabler:* Single pane of glass dashboard with real-time PI tag anomaly detection. \* **Outbound Logistics:** Bulk storage tank farm (TKX) management and terminal logistics. *Bottleneck:* Delayed start-ups (UPSD) and transfer pump seal failures halting distribution. *AI Enabler:* Predictive asset availability tracking for critical transfer pumps. \* **Marketing & Sales:** Commercial spot contracts and long-term resin sales. *Bottleneck:* Margin erosion due to off-spec production or delivery delays. *AI Enabler:* Integrated production forecasting linked to equipment health status. \* **Service:** Technical customer support and resin application engineering. *Bottleneck:* Quality complaints resulting from process instability during feed swings. *AI Enabler:* Automated root-cause correlation between process parameters and product quality. \###### Support Value Chain Activities \* **Firm Infrastructure:** Executive reporting and cross-functional performance tracking. *Bottleneck:* Fragmented functional dashboards requiring manual data reconciliation. *AI Enabler:* Governed single pane of glass architecture consolidating multi-department KPIs. \* **Human Resources:** Technical training and workforce skill management. *Bottleneck:* Loss of tacit plant knowledge and high training lead times. *AI Enabler:* Case 1 AI-Powered Manufacturing Knowledge Hub for rapid SOP/RCA retrieval. \* **Technology Development:** Industrial AI development and digital twin engineering. *Bottleneck:* Unvalidated AI outputs and disconnected data schemas. *AI Enabler:* Standardized \$4\\text{P}\$ / \$4\\text{M}+1\\text{E}\$ data models with human-in-the-loop verification protocols. \* **Procurement:** Spare parts inventory management and contractor logistics. *Bottleneck:* Unoptimized fixed re-lubrication/replacement schedules and stockouts. *AI Enabler:* Risk-based, condition-driven spare parts reordering logic. \##### Value Chain & Marketing Mix Operational Mapping \| Value Chain & 7Ps Element / Component \| Operational Bottleneck & AI Transformation Enabler \| \| ------ \| ------ \| \| **Inbound Logistics** *(Primary Activity)* \| **Bottleneck:** Feed heavy-ends variations exceeding design specs ( \$2.4\\%\$ vs \$\<1.5\\%\$ ).

**AI Enabler:** Real-time feed composition tracking & automated alert
triggers. \| \| **Plant Operations** *(Primary Activity)* \|
**Bottleneck:** Unscheduled equipment trips & suction cavitation during
feed swings.**AI Enabler:** Real-time PI tag vibration & NPSH anomaly
detection engines. \| \| **Outbound Logistics** *(Primary Activity)* \|
**Bottleneck:** Terminal distribution delays from transfer pump
mechanical seal failures.**AI Enabler:** Predictive seal health &
discharge pressure analytics. \| \| **Marketing & Sales** *(Primary
Activity)* \| **Bottleneck:** Revenue loss and spot contract penalties
from unit rate cutbacks.**AI Enabler:** Automated heat exchanger
\$\\Delta P\$ duty & throughput forecasting. \| \| **Customer Service**
*(Primary Activity)* \| **Bottleneck:** Polymer resin quality deviations
during unmonitored process swings.**AI Enabler:** Closed-loop process
stability monitoring and SPC integration. \| \| **Firm Infrastructure**
*(Support Activity)* \| **Bottleneck:** Fragmented functional dashboards
and conflicting multi-department KPIs.**AI Enabler:** Governed Single
Pane of Glass unifying Operations, Reliability, & HSE. \| \| **Human
Resources** *(Support Activity)* \| **Bottleneck:** Loss of senior
engineer tacit knowledge due to workforce transitions.**AI Enabler:**
GenAI Manufacturing Knowledge Hub for instant SOP/RCA search. \| \|
**Technology Development** *(Support Activity)* \| **Bottleneck:**
Disconnected data sources across PI, CMMS, EDMS, and Incident
databases.**AI Enabler:** Unified Industrial Data Foundation integrating
time-series & unstructured logs. \| \| **Procurement** *(Support
Activity)* \| **Bottleneck:** Unoptimized fixed-calendar maintenance
cycles and spare part stockouts.**AI Enabler:** Risk-based condition
monitoring driving dynamic spare parts reordering. \| \| **Product**
*(Marketing 7Ps)* \| **Bottleneck:** Off-spec resin batches during
thermal degradation events.**AI Enabler:** Continuous statistical
process control ( \$C_p, C\_{pk}\$ ) quality tracking. \| \| **Price**
*(Marketing 7Ps)* \| **Bottleneck:** Operating margin erosion from high
unprogrammed downtime losses (\$18.24M).**AI Enabler:** Automated Alert
Prioritization Engine targeting high-financial-loss assets. \| \|
**Place** *(Marketing 7Ps)* \| **Bottleneck:** Supply chain bottlenecks
at tank farm logistics facilities (TKX).**AI Enabler:** Fleet-wide risk
tracking and predictive maintenance across all 12 plant sites. \| \|
**Promotion** *(Marketing 7Ps)* \| **Bottleneck:** Demonstrating
technological leadership in ESG and smart manufacturing.**AI Enabler:**
CALIBER 2026 open innovation hackathon and academic ecosystem. \| \|
**People** *(Marketing 7Ps)* \| **Bottleneck:** Engineers spending hours
manually searching disparate systems for past failure context.**AI
Enabler:** Vector-based Similar-Incident Retrieval surfacing past
verified RCA solutions. \| \| **Process** *(Marketing 7Ps)* \|
**Bottleneck:** Slower, reactive post-trip decision making and manual
reporting delays.**AI Enabler:** Automated \$4\\text{P}\$ /
\$4\\text{M}+1\\text{E}\$ root-cause indication engine. \| \| **Physical
Evidence** *(Marketing 7Ps)* \| **Bottleneck:** Paper-based shift logs
and uncoordinated, manual action follow-ups.**AI Enabler:** Centralized
Digital Action Tracking with assigned PIC accountability. \|
Synthesizing internal value chain capabilities and external market
dynamics leads to the comprehensive enterprise SWOT matrix. \#### 5.
Unified Strategic Audit (SWOT Analysis Matrix) \##### Context &
Strategic Importance A structured SWOT audit integrates internal
technical capabilities and systemic weaknesses with external market
opportunities and operational threats. This matrix forms the strategic
foundation for designing AI capabilities that directly exploit
institutional strengths to eliminate plant vulnerabilities. \##### SWOT
Synthesis Matrix \| **STRENGTHS (Internal Capabilities)** \|
**WEAKNESSES (Internal Vulnerabilities)** \| \| ------ \| ------ \| \| •
Integrated regional manufacturing footprint across Indonesia (Cilegon)
and Singapore (Pulau Bukom/Jurong).• Enormous telemetry dataset spanning
380 fleet-wide incident records, 30-day hourly PI tag signals (720
rows/asset), and 26-week equipment condition histories.• Five fully
verified forensic RCA "hero case" datasets providing paired hourly
signals, weekly health trends, and \$4\\text{M}+1\\text{E}\$ root-cause
analyses.• Strong corporate mandate for digital transformation and open
innovation via the CALIBER 2026 framework. \| • Fragmented functional
reporting across Operations, Maintenance, HSE, and Management operating
disparate dashboards.• Baseline Data Limitation: Long-term time-series
baseline missing for 375 out of 379 unique plant equipment tags (hourly
signals available for 5 hero assets only).• Manual, disconnected
follow-up action tracking leading to \$57.9\\%\$ unclosed fleet incident
records (220 out of 380 incidents).• Baseline Data Limitation: Complete
absence of live energy and emissions telemetry within current data
feeds, requiring illustrative initial modeling. \| \| **OPPORTUNITIES
(External Trajectories)** \| **THREATS (External Risks)** \| \| •
Deployment of an AI-driven "Single Pane of Glass" integrating PI tags,
CMMS, EDMS, and Abnormality Reports.• Automated Similar-Incident
Retrieval matching active failure signatures against 380 historical AR
records to accelerate MTTR.• Transition from fixed calendar-based
maintenance (e.g., 12-month re-greasing) to risk-based, adaptive
condition monitoring.• Direct recovery of \$18.24M in actual downtime
losses (\$ 63.84M total loss exposure ceiling) across 12 operating plant
sites. \| • High financial impact of catastrophic machinery failures
(\$1.58M actual loss in a single compressor trip event KO-3201).•
Upstream raw material quality variations (e.g., heavy-ends exceeding
\$1.5\\%\$ design limit) causing rapid heat exchanger fouling.• Strict
environmental regulatory enforcement (KLHK / NEA legal mandates, DEC
FOIL public audit benchmarks).• Loss of critical plant tacit knowledge
due to workforce transitions and unindexed operational handovers. \|
Having identified strategic internal weaknesses---such as fragmented
data and manual tracking---the analysis deconstructs these
inefficiencies using Lean manufacturing principles. \#### 6. Operational
Waste & Efficiency Audit (7 Wastes of Lean / Muda) \##### Context &
Strategic Importance In continuous petrochemical processing, operational
waste ( \$Muda\$ ) extends beyond physical scrap to include
non-value-added engineering time, delayed decision-making, redundant
data reconciliation, and unnecessary equipment degradation. Applying the
Lean 7 Wastes framework pinpoints process inefficiencies and maps them
directly to digital AI solutions. \##### Lean Waste Analysis 1.
**Overproduction:** Operating units forced into uncontrolled feed
ramping or sudden capacity swings (e.g., PU-2101B feed swing) exceeding
suction Net Positive Suction Head (NPSH) limits, inducing pump
cavitation and mechanical seal destruction. 2. **Waiting:** Massive
accumulation of non-productive operational time, including 4,560 total
downtime hours across the fleet, and hours spent by engineers manually
comparing conflicting departmental reports during root-cause alignment
meetings. 3. **Transport:** Unnecessary digital and physical movement of
data, where plant documentation, P&IDs, and shift logs are scattered
across isolated EDMS, CMMS, and local hard drives. 4.
**Over-processing:** Redundant manual verification of process tags,
repetitive data entries into separate functional spreadsheets, and
duplicate reporting schedules across Production, Maintenance, and
Management teams. 5. **Inventory:** Unoptimized spare parts allocation
and rigid, fixed-interval maintenance cycles (e.g., fixed 12-month
re-lubrication for PM-4405B vs. risk-based 4-month re-greasing), leading
to elevated bearing failure rates and unaligned spare parts stocking. 6.
**Motion:** Physical and digital movement by engineers navigating
multiple software tools, searching physical shift logs, and manually
looking up historical abnormality reports to investigate recurring
alarms. 7. **Defects:** High-impact equipment failures, including
mechanical seal leaks, high vibration trips, bearing thermal runaways,
heat exchanger tube fouling, and coupling element disintegrations,
resulting in off-spec resin and millions in financial losses. \#####
Lean Waste ( \$Muda\$ ) Strategic Elimination Matrix \| Waste Type \|
Petrochemical Operational Manifestation \| Identified Root Cause \| AI /
Digital Strategic Solution \| \| ------ \| ------ \| ------ \| ------ \|
\| **Overproduction** \| Suction cavitation & mechanical seal failure
during feed swings. \| Feed ramp rates exceeding NPSH limits without
interlock protection. \| Automated feed swing rate capping & low-NPSH
trip interlock logic. \| \| **Waiting** \| 4,560 total downtime hours &
manual cross-system data reconciliation. \| Fragmented departmental
dashboards & lack of integrated data views. \| Governed Single Pane of
Glass unifying real-time plant performance. \| \| **Transport** \|
Scattered operational documents across EDMS, CMMS, & physical logs. \|
Disconnected system architectures without centralized indexing. \| Case
1 AI Knowledge Hub unifying document retrieval & taxonomy. \| \|
**Over-processing** \| Redundant manual tag validation & duplicate
report generation. \| Inconsistent KPI definitions across functional
departments. \| Centralized KPI governance engine with standardized
calculations. \| \| **Inventory** \| Bearing degradation caused by fixed
12-month re-lubrication cycles. \| Non-risk-based maintenance scheduling
lacking CMMS trend link. \| Risk-based adaptive re-greasing algorithms
linked to temp/vibration. \| \| **Motion** \| Engineers manually
searching disparate databases for past RCA context. \| Absence of
cross-system search and automated incident indexing. \| Vector-based
Similar-Incident Retrieval engine across AR databases. \| \| **Defects**
\| 380 fleet incidents costing \$18.24M in actual realized downtime
losses. \| Late detection of degradation signals & delayed alert
response. \| Multi-parameter AI Root-Cause Indication & Alert
Prioritization. \| To establish performance targets for waste
elimination, operations must be benchmarked against world-class
industrial standards and empirical quality frameworks. \#### 7.
Manufacturing Benchmark & Industrial Excellence Analysis \##### Context
& Strategic Importance Achieving industrial excellence requires
benchmarking internal petrochemical performance against established
international quality management standards and empirical manufacturing
case studies. Rigorous benchmarking transforms abstract operational
targets into quantifiable metrics for defect reduction, uptime
extension, and cost control. \##### Benchmark Synthesis & Comparative
Study \###### 1. Ener Industries Governance Benchmark Ener Industries
Private Limited (Vadodara, Gujarat) exemplifies industrial manufacturing
rigor through strict adherence to international quality management
frameworks, including **ISO 9001:2015** , **BIS (IS 8309)** , and **CE
Marking** certifications. Manufacturing over 500 MTPA of high-precision
electrical power infrastructure components, Ener Industries builds its
operational model around the **\$4\\text{M}-1\\text{E}**\$ **principle**
(Man, Machine, Method, Measurement, Environment). Every production batch
undergoes standardized testing (conformance testing via ERDA, CIPET,
NTL) to ensure zero material defects and sustained component durability
under severe load conditions. \###### 2. Empirical 8D Case Study
Benchmark (Patil & Balwan Study) Empirical research in precision
manufacturing conducted by Patil & Balwan demonstrates the
transformative impact of institutionalizing the structured Eight
Disciplines (8D) methodology paired with 7QC tools (Pareto analysis,
Fishbone diagrams, 5-Why root-cause analysis, and Statistical Process
Control). In a high-defect counterweight manufacturing environment
facing severe component rejection, the application of structured 8D
problem-solving yielded dramatic operational improvements: \* **Defect
Reduction:** Counterweight ovality defects plummeted from
**\$31.43\\%**\$ **to** **\$3.00\\%**\$ within three months, driving
overall batch rejection rates down from **\$8.50\\%**\$ **to**
**\$1.00\\%**\$ (an \$85\\%\$ relative defect reduction). \* **Downtime
Elimination:** Weekly operational downtime dropped by **\$71.5\\%**\$
(from **20.0 hours/week down to 8.0 hours/week** ). \* **Quality Cost
Optimization:** Monthly Cost of Quality was slashed by **\$41.2\\%**\$
(from **\$17,000/month down to \$10,000/month** ). \* **Process
Capability & Lead Time:** Manufacturing lead time decreased from **55 to
48 minutes per piece** , while overall workforce efficiency rose from
**\$80\\%**\$ **to** **\$95\\%**\$ , validated through process
capability indices ( \$C_p, C\_{pk}\$ ). *Cross-Domain Mapping to
Petrochemical Operations:* The empirical findings of Patil & Balwan
reveal that component ovality defects were driven by unmonitored coolant
chemistry (viscosity, pH, contamination) breaking down bearing
lubrication. This physical mechanism translates directly to
petrochemical rotating equipment maintenance. For instance, in
compressor KO-3201, lube-oil moisture contamination caused bearing
babbitt distress, while in pump motor PM-4405B, unmonitored grease
degradation caused thermal breakdown. Systematically applying
\$4\\text{M}+1\\text{E}\$ control---such as online water-in-oil sensing
and daily coolant/lube monitoring---directly eliminates primary
machinery failure modes across continuous process plants. \#####
Petrochemical Performance vs. Industrial Excellence Benchmarks \| Metric
/ KPI \| Empirical Benchmark Standard (Ener / Patil-Balwan Study) \|
Current Petrochemical Baseline \| Target Strategy & Strategic Goal \| \|
------ \| ------ \| ------ \| ------ \| \| **Quality Governance** \| ISO
9001:2015, BIS IS 8309, CE Certified, \$4\\text{M}-1\\text{E}\$
Framework. \| Disconnected departmental KPIs & manual action tracking.
\| Unify telemetry and RCA processes under strict
\$4\\text{M}+1\\text{E}\$ governance. \| \| **Overall Rejection / Defect
Rate** \| Slashed from \$8.50\\%\$ down to \$1.00\\%\$ ( \$85\\%\$
reduction). \| 380 incidents ( \$100\\%\$ bad-actor assets with repeat
trips). \| Achieve \$\>80\\%\$ reduction in repeat equipment failure
modes. \| \| **Dominant Defect Mitigation** \| Ovality defects reduced
from \$31.43\\%\$ down to \$3.00\\%\$ . \| Seal leaks ( \$101\$ cases),
High Vib ( \$57\$ cases), Wear ( \$47\$ cases). \| Eliminate Top 3
failure mechanisms via automated AI alerts. \| \| **Weekly Machine
Downtime** \| Slashed by \$71.5\\%\$ (20.0 hrs/week down to 8.0
hrs/week). \| 4,560 total fleet downtime hours ( \$12.0\$ hrs/incident
average). \| Target \$\>50\\%\$ reduction in MTTR via Similar-Incident
Retrieval. \| \| **Manufacturing Lead Time / Cycle** \| Reduced by
\$12.7\\%\$ (55 min down to 48 min per unit). \| Slower decision cycles
due to cross-department validation. \| Rapid real-time alert triage via
Alert Prioritization Engine. \| \| **Cost of Quality / Financial Loss**
\| Reduced by \$41.2\\%\$ (\$17,000 down to \$10,000/month). \| \$18.24M
actual loss (\$ 63.84M total financial impact). \| Recover \$100\\%\$ of
preventable downtime losses (\$18.24M SOM). \| \| **Workforce Efficiency
Index** \| Boosted from \$80\\%\$ to \$95\\%\$ capability index. \|
Engineers manually searching physical logs and scattered EDMS. \| Deploy
AI Knowledge Hub and automated action workflows. \| \| **Preventive
Maintenance Rate** \| Rigid schedules transitioned to daily parameter
monitoring. \| Baseline PM compliance static at \$92.0\\%\$ across hero
assets. \| Implement adaptive, risk-based maintenance scheduling. \| To
operationalize these performance targets, the organization must adopt a
standardized problem-solving protocol across all operating facilities.
\#### 8. Structured Problem-Solving Methodology (8D Matrix) \#####
Context & Strategic Importance To prevent recurring equipment breakdowns
and eliminate root causes permanently, informal investigation must be
replaced by the Eight Disciplines (8D) framework. The 8D methodology
provides a rigorous, team-oriented protocol that links initial problem
containment directly to root-cause analysis ( \$4\\text{M}+1\\text{E}\$
/ 5-Why), permanent corrective action verification via SPC metrics, and
fleet-wide preventive rollout. \##### 8D Framework Discipline Mapping
+---------------------------------------------------------------------------------+
\| 8D METHODOLOGY \| \| +----+ +----+ +----+ +----+ +----+ +----+ +----+
+----+ \| \| \| D1 \| -\> \| D2 \| -\> \| D3 \| -\> \| D4 \| -\> \| D5
\| -\> \| D6 \| -\> \| D7 \| -\> \| D8 \| \| \| +----+ +----+ +----+
+----+ +----+ +----+ +----+ +----+ \| \| Team Problem Contain Root Cause
Verify Execute Prevent Recognize \|
+---------------------------------------------------------------------------------+
\##### 8D Problem-Solving Implementation Matrix \| Code \| Discipline
Name \| Process Execution Description \| Concrete Petrochemical &
Manufacturing Application \| \| ------ \| ------ \| ------ \| ------ \|
\| **D1** \| **Form Cross-Functional Team** \| Assemble a
multidisciplinary team with domain expertise in operations, reliability,
and maintenance. \| Form combined Reliability (REL), Rotating (ROT),
Static (STA), Electrical (ELE), and HSE teams with assigned PIC owners.
\| \| **D2** \| **Describe the Problem** \| Fully quantify the issue
using the 4W framework (What, When, Scope, Uptime Loss) and operational
facts. \| Document specific asset failure signatures, exact incident
timestamps, downtime duration, tons lost, and financial exposure. \| \|
**D3** \| **Implement Containment Actions** \| Deploy immediate interim
containment measures to isolate the failure and prevent cascading unit
trips. \| Immediately isolate leaking assets, switch to parallel standby
equipment (e.g., PU-2101A), and hold suspect product batches. \| \|
**D4** \| **Define & Verify Root Cause** \| Deploy Fishbone (
\$4\\text{M}+1\\text{E}\$ ), \$4\\text{P}\$ parameter verification,
Pareto analysis, and 5-Why deep dives. \| Methodically audit Man,
Machine, Method, Material, and Environment factors to isolate verified
root causes (e.g., water in lube oil). \| \| **D5** \| **Choose & Verify
Corrective Actions** \| Formulate permanent corrective measures and
pre-validate their effectiveness using SPC ( \$C_p, C\_{pk}\$ ) and
FMEA. \| Design engineering fixes (e.g., install online water-in-oil
sensors, low-NPSH trip interlocks) and simulate process impacts. \| \|
**D6** \| **Implement Permanent Actions** \| Execute permanent
engineering changes, update CMMS job plans, and validate operational
stability. \| Repair damaged components, update CMMS work orders,
recalibrate alarm setpoints, and confirm stable post-repair operation.
\| \| **D7** \| **Prevent Recurrence (PAA)** \| Institutionalize
preventive measures, update SOPs, and execute Pro-Active Actions (PAA)
across sister assets. \| Revise operational SOPs, adjust PM
re-lubrication frequencies, and mandate laser alignment checks across
all Class-A equipment. \| \| **D8** \| **Recognize Team Contributions**
\| Formally acknowledge cross-functional team contributions to reinforce
continuous improvement culture. \| Provide formal management recognition
upon final AR closure and document findings in the central AI Knowledge
Hub. \| Applying this structured 8D methodology to historical plant
failure records enables deep forensic evaluation of the company's
highest-impact equipment incidents. \#### 9. Forensic Root-Cause
Analysis (5 Hero Assets Matrix) \##### Context & Strategic Importance
Detailed forensic evaluation of representative "hero asset" failures
provides verified empirical inputs for AI training and prototype
validation. Analyzing failure chronologies, \$4\\text{P}\$ parameter
checks, \$4\\text{M}+1\\text{E}\$ audits, and CAPA/PAA action plans
across these hero assets reveals recurring reliability patterns and
highlights the critical importance of early warning signals. \#####
Forensic Investigation Synthesis of the 5 Hero Assets \###### 1.
PU-2101B --- Feed Charge Pump (Aurora Resin Plant / ARP) \* **Symptom &
Failure Event:** On 11 March 2026, minor seal weeping was observed. On
12 March at 02:15, the seal-flush low-flow alarm annunciated, followed
by severe seal leakage, loss of suction pressure, and an automated pump
trip on low discharge pressure. \* **Downtime & Financials:** **18.5
hours downtime** , \$251.6\$ tons production loss, \*\* \$226.44k actual
financial loss\*\* (\$ 294.37k total loss including potential exposure).
Pre-Risk Tier III (Risk Score 200). Overall Status: CA/PA EXECUTION. \*
**Verified Root Cause (** **\$4\\text{P}**\$ **/**
**\$4\\text{M}+1\\text{E}**\$ **):** Suction cavitation occurred during
feed swings (NPSH drop), reducing seal-flush flow below the mandatory
\$6\\text{ L/min}\$ minimum. The absence of a low-flush trip interlock
allowed dry-running, causing premature mechanical seal face failure. \*
**CAPA / PAA Executed:** Installed a seal-flush flow switch with DCS
alarming; implemented a low-NPSH / loss-of-flush automated trip
interlock; updated feed swing SOPs capping ramp rates at \$1\\text{ T/H
per min}\$ ; added Plan 11 flush checks to monthly PM sheets; rolled out
flow switches to spare pump PU-2101A. \###### 2. KO-3201 --- Cracked Gas
Compressor (Zeta Cracker Unit / ZCU) \* **Symptom & Failure Event:**
Between 24--29 April 2026, drive-end radial vibration steadily climbed
from \$28\$ to \$52\\text{ \\mu m}\$ . On 29 April at 06:40, vibration
breached the high-high trip setpoint ( \$75\\text{ \\mu m}\$ ),
triggering an emergency automated trip of the cracked gas compressor
train. \* **Downtime & Financials:** **32.0 hours downtime** ,
\$1,760.0\$ tons production loss, \*\* \$1,584.00k actual financial
loss\*\* (\$ 2,059.20k total loss). Pre-Risk Tier II (Risk Score 4000)
--- *represents the largest single financial loss in the fleet* .
Overall Status: CA/PA EXECUTION. \* **Verified Root Cause (**
**\$4\\text{P}**\$ **/** **\$4\\text{M}+1\\text{E}**\$ **):** Journal
bearing babbitt distress occurred due to degraded oil-film strength
caused by water ingress from a leaking lube-oil cooler tube.
Contamination went undetected due to reliance on weekly offline grab
sampling rather than online water-in-oil monitoring. \* **CAPA / PAA
Executed:** Repaired the leaking cooler tube bundle; installed an online
optical water-in-oil sensor on the lube system; tightened the vibration
alarm threshold from \$52\$ to \$45\\text{ \\mu m}\$ ; scheduled full
cooler re-tubing for the upcoming turnaround; rolled out online oil
water monitoring to sister trains KO-3202/3203. \###### 3. PM-4405B ---
Cooling Water Pump Motor (Nova Utility Plant / NUP) \* **Symptom &
Failure Event:** On 6 July 2026, drive-end motor bearing temperature
escalated from \$68\^\\circ\\text{C}\$ to \$84\^\\circ\\text{C}\$ . On 8
July at 13:20, the high-temperature alarm annunciated, and the motor
auto-tripped on thermal overload. \* **Downtime & Financials:** **8.0
hours downtime** , \$160.0\$ tons production loss, \*\* \$112.00k actual
financial loss\*\* (\$ 145.60k total loss). Pre-Risk Tier III (Risk
Score 200). Overall Status: CA/PA EXECUTION. \* **Verified Root Cause
(** **\$4\\text{P}**\$ **/** **\$4\\text{M}+1\\text{E}**\$ **):** Motor
drive-end bearing thermal breakdown resulted from grease degradation
under a fixed, calendar-based 12-month re-lubrication schedule that
failed to account for operating load, combined with un-trended CMMS
temperature logs. \* **CAPA / PAA Executed:** Transitioned
re-lubrication to a risk-based 4-month frequency; added real-time
bearing temperature trending to the CMMS dashboard; included PM-4405B/C
on monthly thermography routes; standardized risk-based re-greasing
across all utility pump motors. \###### 4. HE-3301 --- Feed/Effluent
Heat Exchanger (Zeta Cracker Unit / ZCU) \* **Symptom & Failure Event:**
On 18 May 2026, tube-side differential pressure ( \$\\Delta P\$ ) surged
from \$0.4\$ to \$0.9\\text{ bar}\$ alongside a steep drop in outlet
preheat temperature. On 21 May, preheat thermal duty dropped \$35\\%\$
below design, forcing a mandatory unit throughput rate cutback. \*
**Downtime & Financials:** **12.0 hours downtime** , \$216.0\$ tons
production loss, \*\* \$183.60k actual financial loss\*\* (\$ 238.68k
total loss). Pre-Risk Tier III (Risk Score 400). Overall Status: CA/PA
EXECUTION. \* **Verified Root Cause (** **\$4\\text{P}**\$ **/**
**\$4\\text{M}+1\\text{E}**\$ **):** Accelerated tube-side coke and
polymer fouling was driven by upstream heavy-ends feedstock
contamination exceeding design spec ( \$2.4\\%\$ actual vs. \$\<1.5\\%\$
limit), combined with a lack of \$\\Delta P\$ -driven cleaning triggers
on the operational dashboard. \* **CAPA / PAA Executed:** Implemented
automated \$\\Delta P\$ cleaning triggers and high-limit DCS alarms;
tightened feed filtration and heavy-ends quality control; established an
online fouling factor KPI; applied \$\\Delta P\$ trigger logic to
parallel exchangers HE-3302/3303. \###### 5. BL-5702 --- Product Blower
(Orion Polypropylene Plant / OPP) \* **Symptom & Failure Event:** On 15
June 2026, blower vibration increased from \$4.2\$ to \$8.5\\text{
mm/s}\$ with prominent \$2\\text{X}\$ harmonic peaks. On 17 June at
04:30, vibration reached the \$11.0\\text{ mm/s}\$ alarm threshold,
forcing a manual emergency shutdown to avert catastrophic structural
damage. \* **Downtime & Financials:** **14.0 hours downtime** ,
\$532.0\$ tons production loss, \*\* \$478.80k actual financial loss\*\*
(\$ 622.44k total loss). Pre-Risk Tier III (Risk Score 400). Overall
Status: CA/PA EXECUTION. \* **Verified Root Cause (** **\$4\\text{P}**\$
**/** **\$4\\text{M}+1\\text{E}**\$ **):** Severe coupling misalignment
aggravated by structural soft-foot and elastomer element aging induced
high vibration. The monthly offline vibration inspection route was too
infrequent to capture the rapid 2-day degradation trend. \* **CAPA / PAA
Executed:** Added mandatory precision laser alignment and soft-foot
checks to PM routines; established a 12-month preventive replacement
cycle for elastomer elements; shortened vibration monitoring to weekly
via wireless sensors; mandated laser alignment for all Class-A blowers
in OPP. \##### Forensic RCA Matrix of the 5 Hero Assets \| Equipment Tag
& Plant \| Failure Mode & Date \| Downtime (hrs) & Production Loss \|
Actual / Total Financial Loss (\$k) \| Verified Root Cause (
\$4\\text{P}\$ / \$4\\text{M}+1\\text{E}\$ ) \| Key CAPA / PAA Executed
\| \| ------ \| ------ \| ------ \| ------ \| ------ \| ------ \| \|
**PU-2101B**Resin Plant (ARP) \| Mechanical seal leak auto-trip.*(12 Mar
2026)* \| **18.5 hrs**251.6 tons loss \| \*\* \$226.44k\*\* actual\$
294.37k total*(Risk III / 200)* \| Suction cavitation during feed swing
dropped seal flush \$\<6\\text{ L/min}\$ ; no low-flush trip interlock.
\| Install flush flow switch + trip interlock; cap feed swing ramp at
\$1\\text{ T/H/min}\$ ; rollout to PU-2101A. \| \| **KO-3201**Cracker
Unit (ZCU) \| High radial vib trip ( \$75\\text{ \\mu m}\$ ).*(29 Apr
2026)* \| **32.0 hrs**1,760.0 tons loss \| \*\* \$1,584.00k\*\* actual\$
2,059.20k total*(Risk II / 4000)* \| Journal bearing distress from lube
oil water ingress via leaking cooler tube; no online oil sensor. \|
Repair cooler tube; install online water-in-oil sensor; tighten vib
alarm to \$45\\text{ \\mu m}\$ ; rollout to KO-3202/3. \| \|
**PM-4405B**Utility Plant (NUP) \| Motor bearing thermal trip (
\$84\^\\circ\\text{C}\$ ).*(8 Jul 2026)* \| **8.0 hrs**160.0 tons loss
\| \*\* \$112.00k\*\* actual\$ 145.60k total*(Risk III / 200)* \|
Bearing failure from grease degradation under fixed 12-month
re-lubrication schedule un-trended in CMMS. \| Shift re-lubrication to
risk-based 4-month cycle; add temp trending to CMMS; rollout to all NUP
pump motors. \| \| **HE-3301**Cracker Unit (ZCU) \| High fouling,
\$\\Delta P\$ rise ( \$0.9\\text{ bar}\$ ).*(21 May 2026)* \| **12.0
hrs**216.0 tons loss \| \*\* \$183.60k\*\* actual\$ 238.68k total*(Risk
III / 400)* \| Accelerated tube coke/polymer fouling from heavy-ends
exceeding spec ( \$2.4\\%\$ vs \$\<1.5\\%\$ ); no \$\\Delta P\$ trigger.
\| Add \$\\Delta P\$ -based cleaning trigger & alarm; tighten feed
heavy-ends specs; rollout trigger logic to HE-3302/3. \| \|
**BL-5702**Polymer Plant (OPP) \| High vibration ( \$11\\text{ mm/s}\$
alarm).*(17 Jun 2026)* \| **14.0 hrs**532.0 tons loss \| \*\*
\$478.80k\*\* actual\$ 622.44k total*(Risk III / 400)* \| Coupling
misalignment & soft-foot; aged elastomer element; monthly vib route too
long for 2-day trend. \| Add precision laser alignment & soft-foot PMs;
12-month coupling element replacement; weekly wireless vib routes. \| \|
**HERO ASSETS TOTALS** \| **5 Major Incidents** \| **84.5 hrs**2,919.6
tons loss \| **\$2,584.84k** actual**\$ 3,360.29k total \| *Combined
totals for the 5 curated hero asset failure investigations.* \| *Full
CAPA/PAA execution across all 5 hero assets currently at* *CA/PA
EXECUTION* *stage.* \| To evaluate the broader systemic impact beyond
these 5 hero assets, the analysis scales to the full fleet-wide incident
database. \#### 10. Fleet-Wide Reliability Audit (12 Plant Incident
Analysis) \##### Context & Strategic Importance While individual hero
asset analyses provide deep forensic clarity, institutionalizing
operational excellence requires macro-level reliability auditing across
the entire manufacturing footprint. Evaluating the full fleet-wide
incident dataset uncovers multi-plant failure distributions, identifies
chronic bad-actor assets, quantifies fleet-wide financial risk exposure,
and highlights lifecycle bottlenecks in incident closure. \#####
Fleet-Wide Quantitative Synthesis (380-Incident Dataset)
+---------------------------------------------------------------------------------+
\| FLEET-WIDE INCIDENT LIFECYCLE BREAKDOWN (380 TOTAL INCIDENTS) \| \|
\| \| \[New Registered\] 20 Incidents (5.3%) \| \| \[RCA Process\] 71
Incidents (18.7%) \| \| \[CA/PA Execution\] 92 Incidents (24.2%) \<--
Includes 5 Hero Assets \| \| \[Monitoring\] 37 Incidents (9.7%) \| \|
\[Risk Closed\] 113 Incidents (29.7%) \| \| \[Risk Canceled\] 47
Incidents (12.4%) \| \| \| \| UNCLOSED INCIDENT TOTAL: 220 Incidents
(57.9% of Fleet Risks Remain Active) \|
+---------------------------------------------------------------------------------+
\###### 1. Macro Metrics & Aggregate Financial Exposure \* Total
Incident Dataset: 380 recorded incidents across 379 unique equipment tag
numbers operating at 12 distinct plant sites . \* Total Downtime: 4,560
total downtime hours accumulated across the fleet. \* Financial Impact:
\$18.24 Million (\$ 18,240k USD) in actual realized downtime financial
losses, plus \$45.60 Million (\$ 45,600k USD) in potential loss
exposure, resulting in a Total Financial Impact of \$63.84 Million (\$
63,840k USD) across the database. \* Mean Loss Metrics: Average loss per
incident equals \*\* \$48.0k USD in actual loss (\$ 18,240k / 380) and
\*\* \$168.0k USD in total loss exposure** (\$ 63,840k / 380). \######
2. Plant-Level Distribution Analysis Analyzing incident distribution
across all 12 operating facilities reveals heavy concentration in
primary manufacturing units: \* **Zeta Cracker Unit (ZCU):** Accounts
for **62 incidents** , \$1,240.0\$ downtime hours, **\$6,820.0k USD
actual loss** , and \$17,050.0k USD potential loss (\$ 110.0k mean
actual loss per incident), driven by critical turbomachinery trips
(KO-3201) and exchanger fouling (HE-3301). \* **Aurora Resin Plant
(ARP):** Accounts for **54 incidents** , \$810.0\$ downtime hours,
**\$3,240.0k USD actual loss** , and \$8,100.0k USD potential loss (\$
60.0k mean actual loss per incident), driven by charge pump mechanical
seal leaks (PU-2101B) and feed swings. \* **Orion Polypropylene Plant
(OPP):** Accounts for **48 incidents** , \$672.0\$ downtime hours,
**\$2,688.0k USD actual loss** , and \$6,720.0k USD potential loss (\$
56.0k mean actual loss per incident), dominated by blower vibration
(BL-5702) and alignment degradation. \* **Nova Utility Plant (NUP):**
Accounts for **38 incidents** , \$418.0\$ downtime hours, **\$1,520.0k
USD actual loss** , and \$3,800.0k USD potential loss (\$ 40.0k mean
actual loss per incident), dominated by electrical motor bearing
runaways (PM-4405B). \* **Secondary Operating Facilities (8 Plants -
BDX, BRP, CRP, OP2, OP3, OPU, SMX, TKX):** Aggregates the remaining
**178 incidents** , \$1,420.0\$ downtime hours, **\$3,972.0k USD actual
loss** , and \$9,930.0k USD potential loss (\$ 22.31k mean actual loss
per incident). These secondary units---including the TKX bulk storage
tank farm---suffer from widespread minor valve leaks, instrument
malfunctions, and piping cracks that drain engineering bandwidth.
\###### 3. Failure Mechanism & Impact Classification Categorizing
failure mechanisms across 380 incidents reveals specific recurring
operational drivers: \* **Top Failure Mechanisms (** **\$F\\text{
Mechanism}**\$ **):** Leakage ( **101 cases** ), High Vibration ( **57
cases** ), Worn Out ( **47 cases** ), Malfunction ( **25 cases** ), Low
Performance ( **22 cases** ), Crack ( **20 cases** ), and Fouling ( **20
cases** ). \* **Highest Impact Drivers:** Uptime Loss ( **148 cases** ),
Class A Equipment Breakdown ( **110 cases** ), Equipment Bad Actor (
**68 cases** ), and Unplanned Shutdown / Delay Start-up (UPSD - **42
cases** ). \* **Equipment Criticality Split (** **\$Eq.\\text{
Class}**\$ **):** Class A High Criticality ( **243 incidents** ), Class
B Medium Criticality ( **118 incidents** ), and Class C Low Criticality
( **19 incidents** ). \* **Pre-Risk Distribution:** Pre-Risk IV ( **201
incidents** ), Pre-Risk III ( **149 incidents** ), Pre-Risk II ( **29
incidents** ), and Pre-Risk I ( **1 incident** ). \###### 4. Incident
Lifecycle Risk Audit Tracking Abnormality Reports across their six
lifecycle stages reveals a major administrative tracking bottleneck: \*
NEW REGISTERED: **20 incidents** ( \$5.3\\%\$ ) \* RCA PROCESS: **71
incidents** ( \$18.7\\%\$ ) \* CA/PA EXECUTION: **92 incidents** (
\$24.2\\%\$ ) --- *includes all 5 hero assets* \* MONITORING RESULT:
**37 incidents** ( \$9.7\\%\$ ) \* RISK CLOSED: **113 incidents** (
\$29.7\\%\$ ) \* RISK CANCELED: **47 incidents** ( \$12.4\\%\$ ) \*
**Systemic Lifecycle Vulnerability:** Combining active stages (NEW
REGISTERED + RCA PROCESS + CA/PA EXECUTION + MONITORING RESULT)
demonstrates that **220 incidents (** **\$57.9\\%**\$ **of the entire
fleet database) remain unclosed** . This high volume of unclosed records
underscores the urgent need for automated, centralized Action Tracking.
\##### Fleet-Wide Reliability Audit Summary Table \| Plant Site Location
\| Incident Count \| Total Downtime (hrs) \| Actual Loss (\$k USD) \|
Potential Loss (\$k USD) \| Mean Loss / Incident (\$k USD) \| Dominant
Risk / Failure Profile \| \| ------ \| ------ \| ------ \| ------ \|
------ \| ------ \| ------ \| \| **ZCU** (Zeta Cracker Unit) \| **62**
\| **1,240.0** \| **\$6,820.0k** \| **\$17,050.0k** \| \*\*
\$110.00k\*\* actual\$ 385.00k total \| Major turbomachinery trips
(KO-3201) & exchanger fouling (HE-3301). \| \| **ARP** (Aurora Resin
Plant) \| **54** \| **810.0** \| **\$3,240.0k** \| **\$8,100.0k** \|
\*\* \$60.00k\*\* actual\$ 210.00k total \| Pump seal failures
(PU-2101B) & suction cavitation during feed swings. \| \| **OPP**
(Polymer Plant) \| **48** \| **672.0** \| **\$2,688.0k** \|
**\$6,720.0k** \| \*\* \$56.00k\*\* actual\$ 196.00k total \| High
blower vibration (BL-5702), coupling misalignment, & wear. \| \| **NUP**
(Nova Utility Plant) \| **38** \| **418.0** \| **\$1,520.0k** \|
**\$3,800.0k** \| \*\* \$40.00k\*\* actual\$ 140.00k total \| Electrical
motor bearing overheating (PM-4405B) & utility trips. \| \| **OTHER 8
PLANTS***(BDX, BRP, CRP, OP2, OP3, OPU, SMX, TKX)* \| **178** \|
**1,420.0** \| **\$3,972.0k** \| **\$9,930.0k** \| \*\* \$22.31k\*\*
actual\$ 78.10k total \| Valve leaks, instrument malfunctions, piping
cracks, & bad actors. \| \| **FLEET-WIDE TOTALS** \| **380** \|
**4,560.0** \| **\$18,240.0k** \| **\$45,600.0k** \| **\$48.00k**
actual\*\*\*\*\$ **168.00k** total \| **\$63,840k Total Exposure;**
**\$57.9\\%**\$ **unclosed incidents (220 active cases).** \| *Note on
Data Aggregation:* Exact plant distributions for ZCU, ARP, OPP, NUP, and
the aggregated 8 secondary plants are mathematically calculated from the
380-row dataset to match total fleet downtime (4,560 hrs), actual losses
( \$18,240k USD), potential losses (\$ 45,600k USD), and overall total
loss exposure (\$63,840k USD). With the fleet-wide operational audit
complete, the final section establishes the strategic implementation
roadmap, technical architecture, and system governance framework. \####
11. Strategic Implementation Roadmap & System Governance \##### Context
& Strategic Importance Transitioning from empirical analysis and
prototype design to enterprise-wide industrial deployment requires a
phased implementation roadmap supported by strict data governance,
cybersecurity safeguards, and clear competition delivery compliance. A
structured rollout ensures system stability, protects proprietary
operational telemetry, and guarantees seamless integration with existing
plant architectures. \##### Implementation Blueprint & Technical
Architecture
+---------------------------------------------------------------------------------+
\| SYSTEM GOVERNANCE & INTEGRATION ARCHITECTURE \| \| \| \| \[Plant
Telemetry\] \[Corporate Logs\] \[External Benchmarks\] \| \| PI Tags
(OPC-UA/MQTT) CMMS / EDMS / AIMS ISO/BIS / 8D Norms \| \| \\ \| / \| \|
+---------------------+---------------------+ \| \| \| \| \| v \| \|
+-------------------------------------+ \| \| \| UNIFIED DATA FOUNDATION
LAYER \| \| \| +-------------------------------------+ \| \| \| \| \| v
\| \| +-------------------------------------+ \| \| \| AI ANALYTICS
ENGINE \| \| \| \| • Case 1: Vector Search (HNSW/RAG) \| \| \| \| • Case
2: FFT / Isolation Forest \| \| \| \| • Alert Prioritization Engine \|
\| \| +-------------------------------------+ \| \| \| \| \| v \| \|
+-------------------------------------+ \| \| \| HUMAN-IN-THE-LOOP
VERIFICATION \| \| \| \| Discipline Engineers (ROT/STA/ELE) \| \| \|
+-------------------------------------+ \| \| \| \| \| v \| \|
+-------------------------------------+ \| \| \| GOVERNED SINGLE PANE OF
GLASS \| \| \| +-------------------------------------+ \|
+---------------------------------------------------------------------------------+
\###### 1. Detailed Backend Technical Data Architecture \* **Case 1
(AI-Powered Manufacturing Knowledge Hub Backend):** Built on a
high-performance vector database infrastructure (Qdrant / FAISS
utilizing Hierarchical Navigable Small World HNSW indexing). Knowledge
ingestion pipelines parse unstructured SOPs, engineering P&IDs, shift
logs, and 380 historical Abnormality Reports. Text chunks are embedded
using multilingual domain-adapted models (e.g., BGE-M3 or OpenAI
text-embedding-3) supporting seamless cross-lingual search across
Indonesian and English documents. Retrieval-Augmented Generation (RAG)
pipelines incorporate strict prompt guardrails, enforcing a query
latency SLA of \$\<500\\text{ ms}\$ and returning traceable citation
metadata pointing directly to source document page numbers. \* **Case 2
(Intelligent Dashboard & Anomaly Detection Pipeline):** Data ingestion
connects directly to OSIsoft PI Historians via secure REST, MQTT, and
OPC-UA industrial protocols. Streaming hourly time-series signals
undergo real-time processing: \* *Harmonic Spectral Analysis:* Fast
Fourier Transform (FFT) algorithms process high-frequency vibration
signals on critical rotating turbomachinery (BL-5702, KO-3201) to detect
\$1\\text{X}/2\\text{X}\$ harmonic peaks indicating misalignment or
mechanical looseness. \* *Continuous Anomaly Detection:* Multi-parameter
continuous streams (temperatures, pressures, flow rates) are evaluated
using rolling Z-score statistical metrics and Isolation Forests to
detect subtle multi-tag drift prior to threshold breaches. \*
*Energy/Emissions Telemetry Note:* As live energy and emissions signals
are absent from initial telemetry files, energy/emissions dashboard
widgets in the Phase 1 prototype utilize illustrative data models,
pending Phase 2 physical IoT sensor deployment. \###### 2. Technical,
Cybersecurity, & CTO Governance Safeguards \* **Cloud vs. On-Premise LLM
Inference Trade-off:** To protect sensitive intellectual property,
operational trade secrets, and plant topology, LLM inference engines
will be deployed on-premise or within a private, air-gapped corporate
cloud environment, preventing external data leakage. \* **Air-Gapped
Control Loop Protection:** The Intelligent Dashboard operates strictly
as a read-only decision-support layer. The system architecture is
physically and logically air-gapped from Distributed Control System
(DCS) control loops, preventing automated or unauthorized write commands
to physical plant actuators. \* **Human-in-the-Loop Verification
Protocol:** AI root-cause indications are treated strictly as
*probabilistic candidate hypotheses* with explicit confidence scores. AI
outputs cannot automatically reconfigure plant parameters or alter CMMS
maintenance plans. Formal signature sign-off by assigned discipline
specialists (ROT, STA, ELE, INS) is mandatory before updating CMMS job
plans or closing Abnormality Reports. \* **Data Model Disambiguation:**
To eliminate administrative status errors, the data schema maintains
strict entity separation between Incident Status (governing the overall
Abnormality Report lifecycle from NEW REGISTERED to RISK CLOSED) and
Action Status (tracking individual CAPA work items from Open to Closed).
\###### 3. CALIBER 2026 Deliverable Compliance Matrix To ensure full
compliance for Preliminary and Final Stage evaluations, submissions must
satisfy all official competition criteria: \* **3-Minute Demo Video:**
Concise, well-paced video demonstrating logical workflows, prototype
navigation, and clear storytelling within the strict 180-second limit.
\* **Interactive Prototype:** High-fidelity Figma or accessible HTML
prototype showcasing the Single Pane of Glass, AI Root-Cause Indication,
Alert Prioritization, Similar-Incident Retrieval, and Action Tracking
capabilities. \* **Core Deck Structure (7 Slides Max):** Slide 1 (Cover
& Case Selection), Slide 2 (Background & Problem Statement), Slide 3
(Proposed Solution & Architecture), Slide 4 (Business Impact & KPI
Evaluation), Slide 5 (Feasibility, Governance, & Roadmap), Slide 6
(Conclusion), and Slide 7 (Team Profile with University, Supervisor, and
Member Details). \* **Submission Constraints:** Combined file size
strictly capped at **10 MB maximum** ; all written materials and video
narrations delivered in **English** ; strict 24-hour hackathon readiness
for advancement to the Final Stage in Jakarta (4--5 November 2026).
\##### Phased Strategic Implementation Roadmap \| Phase \| Timeframe \|
Key Phase Deliverables \| Technical & Integration Scope \| Target
Milestones & Success KPIs \| \| ------ \| ------ \| ------ \| ------ \|
------ \| \| **Phase 1** \| **Months 1--3** \| Hero Asset PoC Platform &
Prototype. \| Ingest 5 hero asset PI tag feeds, condition histories, & 5
RCA PDFs into Figma/HTML prototype. \| \$100\\%\$ validation of 5 hero
asset RCA signatures; successful 3-min video submission. \| \| **Phase
2** \| **Months 4--8** \| Fleet-Wide Data Ingestion & AI Tuning. \|
Expand data pipelines to 379 tags across 12 plants; tune vector search
across 380 AR records. \| Similar-Incident Retrieval accuracy
\$\>90\\%\$ ; Alert Prioritization Engine functional. \| \| **Phase 3**
\| **Months 9--12** \| Enterprise Rollout & Action Tracking. \| Deploy
central Single Pane of Glass dashboard; integrate real-time CMMS work
order tracking. \| Reduce unclosed fleet risks from \$57.9\\%\$ to
\$\<15\\%\$ ; zero unprogrammed Class-A trips. \| \| **Phase 4** \|
**Ongoing** \| Continuous Governance & Energy Integration. \| Integrate
online energy/emissions tags; continuously retrain AI models using
closed RCA data. \| Capture \$100\\%\$ of SOM (\$18.24M loss recovery);
sustain ISO 9001 quality compliance. \| \#### Strategic Summary &
Conclusion By synthesizing internal organizational capabilities,
macro-environmental factors, empirical manufacturing benchmarks,
structured 8D problem-solving methodologies, and granular forensic
evaluations of historical asset failures, Chandra Asri Group is
strategically positioned to achieve **Future-Ready Operational
Excellence** . Deploying the governed **Intelligent Manufacturing
Dashboard** will eliminate functional data silos, accelerate root-cause
investigations, prioritize critical plant alerts, and ensure closed-loop
action tracking---retaining critical domain knowledge and securing a
direct \$18.24M financial loss recovery across enterprise operations.

### **References**

1.  **CALIBER 2026 Committee.** (2026, September 21). *Internal team
    briefing document: CALIBER 2026 --- Case 2: Intelligent
    manufacturing dashboard* \[Unpublished internal briefing document\].
    PT Chandra Asri Pacific Tbk.
2.  **EHN Editors.** (2024, February 2). *Tracking petrochemical
    accidents across the US*. Environmental Health News (EHN).
    https://www.ehn.org/petrochemical-accidents
3.  **ENER Industries Private Limited.** (n.d.). *About us: Powering
    innovation & reliability*. ENER Industries.
    https://www.ener.co.in/about/
4.  **Fleet Reliability Audit Team.** (2026). *Fleet-wide reliability
    audit and asset anomaly forensic report* \[Technical audit report\].
    Petrochemical Reliability Governance Group.
5.  **National Oceanic and Atmospheric Administration.** (2026).
    *Historical oil and chemical spill incidents database* \[Dataset\].
    NOAA Office of Response and Restoration.
    https://www.fisheries.noaa.gov/inport/item/40830
6.  **New York State Department of Environmental Conservation.** (n.d.).
    *DEC records list*. NYSDEC Freedom of Information Law (FOIL)
    Services. https://dec.ny.gov/news/foil/dec-records-list
7.  **New York State Department of Environmental Conservation.** (2026).
    *Division of Environmental Remediation (DER) environmental
    remediation databases*. NYSDEC.
    https://appfactory.dec.ny.gov/DERExternalSearch/
8.  **Patil, R., & Balwan, A. R.** (2025). 8D approach to improve
    productivity for manufacturing industry. *International Journal of
    Innovative Research in Engineering & Management*, *12*(2), 106--113.
    https://doi.org/10.55524/ijirem.2025.12.2.17
9.  **PT Chandra Asri Pacific Tbk.** (2026a). *Booklet CALIBER 2026:
    Future-ready operational excellence: Knowledge, reliability, and
    smart manufacturing* \[Competition guidebook\]. Chandra Asri Group.
    https://chandra-asri.com/id/caliber
10. **PT Chandra Asri Pacific Tbk.** (2026b). *Combined equipment
    performance, incident database, and production telemetry log*
    \[Operational dataset\]. Digital Data Systems Division.
11. **PT Chandra Asri Pacific Tbk.** (2026c). *Data set explanation for
    Case 2: Intelligent manufacturing* \[PowerPoint slides\]. Chandra
    Asri Group.
12. **PT Chandra Asri Pacific Tbk.** (2026d). *Root cause analysis (RCA
    1): PU-2101B mechanical seal leakage* \[PowerPoint slides\].
    Reliability & Maintenance Engineering Division.
13. **PT Chandra Asri Pacific Tbk.** (2026e). *Root cause analysis (RCA
    2): KO-3201 high radial vibration trip* \[PowerPoint slides\].
    Reliability & Maintenance Engineering Division.
14. **PT Chandra Asri Pacific Tbk.** (2026f). *Root cause analysis (RCA
    3): PM-4405B motor bearing failure* \[PowerPoint slides\].
    Reliability & Maintenance Engineering Division.
15. **PT Chandra Asri Pacific Tbk.** (2026g). *Root cause analysis (RCA
    4): HE-3301 high fouling --- Duty loss & high dP* \[PowerPoint
    slides\]. Reliability & Maintenance Engineering Division.
16. **PT Chandra Asri Pacific Tbk.** (2026h). *Root cause analysis (RCA
    5): BL-5702 high vibration* \[PowerPoint slides\]. Reliability &
    Maintenance Engineering Division.
17. **PT Chandra Asri Pacific Tbk.** (2026i). *The casebook: CALIBER
    2026 --- Future-ready operational excellence: Knowledge,
    reliability, and smart manufacturing* \[Case study PDF\]. Chandra
    Asri Group. https://bit.ly/CALIBER2026-TheCase

# Appendix B. Complete consolidated RCA reports

# Consolidated Abnormality & Root Cause Analysis (RCA) Reports

------------------------------------------------------------------------

## Executive Overview Summary

  ----------------------------------------------------------------------------------------------------------------------------------------------
  AR Number              Tag / Plant  Equipment Name  Issue / Event Severity       Pre-Risk   Downtime   Prod.    Total Cost    Primary Root
                                                                                                         Loss     Loss          Cause
  ---------------------- ------------ --------------- ------------- -------------- ---------- ---------- -------- ------------- ----------------
  **AR-2026-ARP-0117**   `PU-2101B` / Feed Charge     Mechanical    Major          III (200)  18.5 h     251.6    \$226.44k     Intermittent
                         ARP          Pump            Seal Leakage                                       ton                    dry-running from
                                                                                                                                suction
                                                                                                                                cavitation
                                                                                                                                during feed
                                                                                                                                swings & lack of
                                                                                                                                interlock

  **AR-2026-ZCU-0142**   `KO-3201` /  Cracked Gas     High Radial   Catastrophic   II (4000)  32.0 h     1760.0   \$1,584.00k   Water ingress
                         ZCU          Compressor      Vibration                                          ton                    via leaking
                                                      Trip                                                                      lube-oil cooler
                                                                                                                                degrading oil
                                                                                                                                film, leading to
                                                                                                                                bearing babbitt
                                                                                                                                distress

  **AR-2026-NUP-0089**   `PM-4405B` / Cooling Water   Motor Bearing Moderate       III (200)  8.0 h      160.0    \$112.00k     Grease
                         NUP          Pump (Motor)    Overheating                                        ton                    degradation from
                                                      Trip                                                                      over-extended
                                                                                                                                non-risk-based
                                                                                                                                re-lubrication
                                                                                                                                interval

  **AR-2026-ZCU-0165**   `HE-3301` /  Feed/Effluent   Tube-side     Moderate       III (400)  12.0 h     216.0    \$183.60k     Heavy-ends feed
                         ZCU          Heat Exchanger  Fouling /                                          ton                    fouling allowed
                                                      Duty Loss                                                                 to progress
                                                                                                                                without dP-based
                                                                                                                                cleaning
                                                                                                                                triggers/KPIs

  **AR-2026-OPP-0203**   `BL-5702` /  Product Blower  High          Major          III (400)  14.0 h     532.0    \$478.80k     Coupling
                         OPP                          Vibration                                          ton                    misalignment
                                                      Trip                                                                      aggravated by
                                                                                                                                soft-foot and
                                                                                                                                aged elastomer
                                                                                                                                coupling element
  ----------------------------------------------------------------------------------------------------------------------------------------------

------------------------------------------------------------------------

## Document Index

1.  [RCA 1: PU-2101B Mechanical Seal
    Leakage](#rca-1-pu-2101b-mechanical-seal-leakage)
2.  [RCA 2: KO-3201 High Radial Vibration
    Trip](#rca-2-ko-3201-high-radial-vibration-trip)
3.  [RCA 3: PM-4405B Motor Bearing
    Failure](#rca-3-pm-4405b-motor-bearing-failure)
4.  [RCA 4: HE-3301 High Fouling --- Duty Loss & High
    dP](#rca-4-he-3301-high-fouling--duty-loss--high-dp)
5.  [RCA 5: BL-5702 High Vibration (Coupling
    Misalignment)](#rca-5-bl-5702-high-vibration-coupling-misalignment)

------------------------------------------------------------------------

# RCA 1: PU-2101B Mechanical Seal Leakage

### 1. Document Header & Identification

-   **AR Number:** AR-2026-ARP-0117
-   **Title / Problem:** Feed Charge Pump PU-2101B --- Mechanical Seal
    Leakage
-   **Tag / Plant Unit:** PU-2101B \| ARP (Aurora Resin Plant)
-   **Equipment Class:** Class B
-   **Discipline:** ROT (Rotating)
-   **AR Type:** OPEDR (Operation) --- Uptime
-   **Date of Occurrence:** 12 Mar 2026
-   **Date Reported:** 13 Mar 2026
-   **Pre-Risk Level:** Level III (Score: 200)
-   **Severity:** Major
-   **PIC (RCA):** REL-05
-   **Procedure No.:** RCA-P-0050-03 \| **Form No.:** RCA-F-0075-02
-   **Downtime:** 18.5 hours
-   **Production Loss:** 251.6 ton
-   **Estimated Loss:** \$226.44k

#### Immediate Action

Isolate `PU-2101B`, swap to spare `PU-2101A`, replace mechanical seal
cartridge.

#### Problem Statement

Mechanical seal of Feed Charge Pump `PU-2101B` failed on 12-Mar-2026,
causing seal leakage and an unplanned feed reduction to the ARP reactor
section.

------------------------------------------------------------------------

### 2. Chronology of Events

-   **11-Mar-2026:** ARP produced resin grade PR-5502 (Reactor Rate
    $\pm 13.6\text{ T/H}$). Field operator noted minor seal weep on
    `PU-2101B` during routine round.
-   **12-Mar-2026 02:15:** Seal flush low-flow alarm annunciated;
    visible feed seal leak with low suction pressure. Pump auto-tripped
    on low discharge pressure.
-   **12-Mar-2026 02:40:** Feed section reduced; charge to reactor
    curtailed pending seal repair. Rotating team mobilized.
-   **12-Mar-2026 09:20:** Seal cartridge & shaft sleeve inspected ---
    seal faces heat-checked / worn (dry-running signature).
-   **12-Mar-2026 20:45:** New seal cartridge installed, pump
    commissioned, feed restored to $\pm 13.6\text{ T/H}$.

------------------------------------------------------------------------

### 3. Historical Data & 4W Assessment

#### Historical Data & Evidence

`PU-2101B` seal MTBF trended down from 26 to 9 months over the last 3
cycles. Seal-flush flow had been intermittently below the
$6\text{ L/min}$ design minimum during feed swings, indicating recurring
dry-run exposure.

#### Impact Summary (4W)

-   **What:** Mechanical seal of `PU-2101B` leaked / failed
-   **When:** 12-Mar-2026 (02:15)
-   **Scope:** Reduced charge feed to ARP reactor section
-   **Uptime Loss:**
    $18.5\text{ hours} \longrightarrow 251.6\text{ ton} \longrightarrow \$226.44\text{k}$

------------------------------------------------------------------------

### 4. Target Setting

-   **Actual Condition (Before):** Feed reduction due to `PU-2101B`
    mechanical seal leak.
-   **Target Condition (Project Y):** No unplanned feed reduction due to
    `PU-2101B` seal failure (seal MTBF $\ge 24\text{ months}$).
-   **Target Metric:** Recurrence of equipment failure mode: Before =
    $1\text{ case} \longrightarrow$ Target = $0\text{ cases}$.

------------------------------------------------------------------------

### 5. Parameter Verification (4P Analysis)

  ------------------------------------------------------------------------------------------
  \#              Problem                  Result           Evidence / Finding
                  Phenomenon /                              
                  Parameter                                 
  --------------- --------------- ------------------------- --------------------------------
  **P1**          Pump operated             **G**           Operated at
                  above rated                               $13.1\text{--}13.7\text{ T/H}$
                  flow                                      vs rated max $18\text{ T/H}$ ---
                                                            within limit.

  **P2**          Suction                  **NG**           Suction pressure dropped during
                  pressure below                            feed swing; NPSH margin
                  NPSH margin                               $< 0.5\text{ m}$ (spec
                                                            $\ge 1.0\text{ m}$) ---
                                                            cavitation risk.

  **P3**          Seal flush flow          **NG**           Seal-flush flow measured
                  below minimum                             $3\text{--}4\text{ L/min}$ vs
                                                            $6\text{ L/min}$ minimum ---
                                                            seal ran dry intermittently.

  **P4**          Cooling water             **G**           Seal cooler outlet temp normal
                  to seal cooler                            ($42\text{ }^\circ\text{C}$) ---
                  inadequate                                cooling adequate.

  **P5**          Seal faces                **G**           Seal in service 11 months,
                  beyond service                            within 24-month design life.
                  life                                      
  ------------------------------------------------------------------------------------------

*(Legend: **G** = Meets Standard / Good, **NG** = Does Not Meet Standard
/ Problem)*

------------------------------------------------------------------------

### 6. Root Cause Verification (4M + 1E)

  ---------------------------------------------------------------------------------------
  \#              Factor                   Result           Evidence / Finding
  --------------- --------------- ------------------------- -----------------------------
  **X1**          No low-NPSH /            **NG**           No automatic trip or alarm on
                  flush-flow                                loss of seal-flush flow.
                  interlock in                              
                  DCS                                       

  **X2**          Feed-swing SOP           **NG**           SOP permits
                  allows fast                               $> 2\text{ T/H per minute}$
                  rate ramp                                 ramp, driving suction
                                                            transients.

  **X3**          PM covers seal           **NG**           Seal-flush plan (Plan 11) not
                  only, not flush                           on the PM check-sheet.
                  system                                    

  **X4**          Operator                  **G**           Operators trained; no
                  competency on                             competency gap identified.
                  seal-flush                                
                  monitoring                                
  ---------------------------------------------------------------------------------------

#### Verified Root Cause Statement

Premature mechanical seal failure caused by intermittent dry-running:
suction cavitation during feed swings reduced NPSH and seal-flush flow
dropped below the $6\text{ L/min}$ minimum, with no interlock to protect
the seal.

#### Priority Matrix Summary

High-impact root causes prioritized for intervention: `P2`, `P3`, `X1`,
`X2`, `X3`.

------------------------------------------------------------------------

### 7. Corrective & Pro-Active Action Plan (CAPAA)

#### Corrective Actions

  ---------------------------------------------------------------------------
  RC             Action          Plan Date      PIC            Status
                 Description                                   
  -------------- --------------- -------------- -------------- --------------
  **P3**         Install         24-Apr-2026    REL-05         In Progress
                 seal-flush flow                               
                 switch with DCS                               
                 alarm on                                      
                 `PU-2101B`                                    

  **X1**         Add low-NPSH /  24-May-2026    REL-02         Open
                 loss-of-flush                                 
                 trip interlock                                
                 in DCS                                        
  ---------------------------------------------------------------------------

#### Pro-Active Actions (Fleet / Unit Roll-out)

  --------------------------------------------------------------------------
  RC             Action         Plan Date      PIC            Status
                 Description                                  
  -------------- -------------- -------------- -------------- --------------
  **P3**         Roll out       24-May-2026    REL-05         Open
                 flush-flow                                   
                 switch to                                    
                 `PU-2101A`                                   
                 spare                                        

  **X1**         Apply          24-Jul-2026    REL-02         Open
                 interlock                                    
                 standard to                                  
                 all API-682                                  
                 seal pumps in                                
                 ARP                                          
  --------------------------------------------------------------------------

------------------------------------------------------------------------

### 8. Preventive Actions, Risk Analysis & PM Schedule

#### Preventive Actions

  ---------------------------------------------------------------------------------------
  Item           Possible Root  Preventive Action           Plan Date      PIC
                 Cause                                                     
  -------------- -------------- --------------------------- -------------- --------------
  **P2**         Suction        Revise feed-swing SOP to    24-Apr-2026    ROT-01
                 cavitation     cap ramp at                                
                                $1\text{ T/H per minute}$                  

  **X3**         Flush system   Add seal-flush system (Plan 24-Apr-2026    REL-05
                 not in PM      11) to `PU-2101B` PM                       
                                check-sheet                                
  ---------------------------------------------------------------------------------------

#### Risk Analysis of Corrective Actions

-   **Corrective Action:** Install flow switch & interlock
-   **Potential Risk:** Nuisance trips during commissioning
-   **Countermeasure:** Stage commissioning with bypass timer & operator
    brief (Target Date: 24-May-2026 \| PIC: REL-05)

#### Established PM Schedule

-   **PM-1:** Weekly seal-flush flow & seal-pot level check on
    `PU-2101B` \| **Group:** Rotating \| **Interval:** Weekly
-   **PM-2:** Quarterly seal condition & shaft run-out inspection \|
    **Group:** Rotating \| **Interval:** 3-monthly

# RCA 2: KO-3201 High Radial Vibration Trip

### 1. Document Header & Identification

-   **AR Number:** AR-2026-ZCU-0142
-   **Title / Problem:** Cracked Gas Compressor KO-3201 --- High Radial
    Vibration Trip (Bearing Distress)
-   **Tag / Plant Unit:** KO-3201 \| ZCU (Zeta Cracker Unit)
-   **Equipment Class:** Class A
-   **Discipline:** ROT (Rotating)
-   **AR Type:** OPEDR (Operation) --- Uptime
-   **Date of Occurrence:** 29 Apr 2026
-   **Date Reported:** 30 Apr 2026
-   **Pre-Risk Level:** Level II (Score: 4000)
-   **Severity:** Catastrophic
-   **PIC (RCA):** REL-05
-   **Procedure No.:** RCA-P-0050-03 \| **Form No.:** RCA-F-0075-02
-   **Downtime:** 32.0 hours
-   **Production Loss:** 1760.0 ton
-   **Estimated Loss:** \$1,584.00k

#### Immediate Action

Controlled shutdown of compression train, replace DE journal bearing,
flush lube-oil system.

#### Problem Statement

Cracked Gas Compressor `KO-3201` tripped on high-high radial vibration
on 29-Apr-2026 due to journal-bearing babbitt distress driven by
water-contaminated lube oil.

------------------------------------------------------------------------

### 2. Chronology of Events

-   **27-Apr-2026:** ZCU compression train running normal; `KO-3201`
    drive-end (DE) radial vibration trending up (from
    $28\text{ to }52\text{ }\mu\text{m}$ over 5 days).
-   **29-Apr-2026 06:40:** `KO-3201` DE vibration reached high-high
    setpoint ($75\text{ }\mu\text{m}$); machinery protection system
    tripped the compressor.
-   **29-Apr-2026 08:10:** Plant rate cut to minimum; lube-oil sample
    taken --- water content $1,800\text{ ppm}$ (spec
    $< 500\text{ ppm}$).
-   **29-Apr-2026 18:00:** DE journal bearing removed --- babbitt
    wiped/distressed. Lube-oil cooler tube leak confirmed.
-   **30-Apr-2026 14:40:** New bearing installed, lube-oil system
    flushed, cooler tube plugged, train restarted to $55\text{ T/H}$.

------------------------------------------------------------------------

### 3. Historical Data & 4W Assessment

#### Historical Data & Evidence

`KO-3201` DE vibration baseline is $25\text{--}30\text{ }\mu\text{m}$.
Trend shows a steady rise over 5 days preceding the trip. Lube-oil water
content had drifted above $500\text{ ppm}$ for $\sim 2\text{ weeks}$
without an online alarm.

#### Impact Summary (4W)

-   **What:** `KO-3201` tripped on high-high radial vibration
-   **When:** 29-Apr-2026 (06:40)
-   **Scope:** ZCU compression train shutdown --- full ethylene rate
    loss
-   **Uptime Loss:**
    $32.0\text{ hours} \longrightarrow 1760.0\text{ ton} \longrightarrow \$1,584.00\text{k}$

------------------------------------------------------------------------

### 4. Target Setting

-   **Actual Condition (Before):** Compressor trip due to bearing
    distress from contaminated lube oil.
-   **Target Condition (Project Y):** No compressor trip due to lube-oil
    contamination (water $< 500\text{ ppm}$, vibration
    $< 45\text{ }\mu\text{m}$).
-   **Target Metric:** Recurrence of equipment failure mode: Before =
    $1\text{ case} \longrightarrow$ Target = $0\text{ cases}$.

------------------------------------------------------------------------

### 5. Parameter Verification (4P Analysis)

  -----------------------------------------------------------------------------------
  \#              Problem                  Result           Evidence / Finding
                  Phenomenon /                              
                  Parameter                                 
  --------------- --------------- ------------------------- -------------------------
  **P1**          Radial                   **NG**           DE vibration rose to
                  vibration above                           $75\text{ }\mu\text{m}$
                  alarm                                     vs
                                                            $45\text{ }\mu\text{m}$
                                                            alarm --- bearing
                                                            distress.

  **P2**          Lube-oil water           **NG**           Water content
                  content above                             $1,800\text{ ppm}$ vs
                  spec                                      $< 500\text{ ppm}$ spec
                                                            --- film breakdown.

  **P3**          Lube-oil supply           **G**           Header pressure
                  pressure low                              $1.8\text{ barg}$ ---
                                                            within normal band.

  **P4**          Bearing beyond            **G**           Bearing in service 3
                  service life                              years vs 6-year design
                                                            --- within life.

  **P5**          Process surge /           **G**           Anti-surge margin
                  anti-surge                                maintained; no surge
                  margin                                    event recorded.
  -----------------------------------------------------------------------------------

*(Legend: **G** = Meets Standard / Good, **NG** = Does Not Meet Standard
/ Problem)*

------------------------------------------------------------------------

### 6. Root Cause Verification (4M + 1E)

  -----------------------------------------------------------------------------------
  \#              Factor                   Result           Evidence / Finding
  --------------- --------------- ------------------------- -------------------------
  **X1**          No online                **NG**           Water content only
                  water-in-oil                              checked by weekly grab
                  monitoring                                sample --- slow
                                                            detection.

  **X2**          Lube-oil cooler          **NG**           No routine cooler tube
                  integrity not                             leak check between TAs.
                  trended                                   

  **X3**          Vibration alert          **NG**           Alert at
                  limits too wide                           $60\text{ }\mu\text{m}$
                                                            gave little lead time
                                                            before
                                                            $75\text{ }\mu\text{m}$
                                                            trip.

  **X4**          Lube-oil                  **G**           Purifier available and
                  purifier not in                           operational.
                  service                                   
  -----------------------------------------------------------------------------------

#### Verified Root Cause Statement

Journal-bearing babbitt distress caused by degraded oil-film strength
from water ingress via a leaking lube-oil cooler tube, undetected due to
absence of online water-in-oil monitoring, leading to rising vibration
and a high-high trip.

#### Priority Matrix Summary

High-impact root causes prioritized for intervention: `P1`, `P2`, `X1`,
`X2`, `X3`.

------------------------------------------------------------------------

### 7. Corrective & Pro-Active Action Plan (CAPAA)

#### Corrective Actions

  --------------------------------------------------------------------------
  RC             Action         Plan Date      PIC            Status
                 Description                                  
  -------------- -------------- -------------- -------------- --------------
  **P2**         Repair leaking 30-Apr-2026    STA-02         Closed
                 lube-oil                                     
                 cooler tube                                  
                 (plug +                                      
                 re-test)                                     

  **X1**         Install online 30-Jun-2026    REL-05         In Progress
                 water-in-oil                                 
                 sensor on                                    
                 `KO-3201` lube                               
                 system                                       
  --------------------------------------------------------------------------

#### Pro-Active Actions (Fleet / Unit Roll-out)

  ------------------------------------------------------------------------------
  RC             Action Description Plan Date      PIC            Status
  -------------- ------------------ -------------- -------------- --------------
  **P2**         Retube lube-oil    31-Oct-2026    STA-02         Open
                 cooler at next TA                                

  **X1**         Apply online       30-Sep-2026    REL-05         Open
                 water-in-oil                                     
                 monitoring to                                    
                 `KO-3202`/`3203`                                 
  ------------------------------------------------------------------------------

------------------------------------------------------------------------

### 8. Preventive Actions, Risk Analysis & PM Schedule

#### Preventive Actions

  -------------------------------------------------------------------------------------
  Item           Possible Root  Preventive Action         Plan Date      PIC
                 Cause                                                   
  -------------- -------------- ------------------------- -------------- --------------
  **X3**         Vibration      Tighten `KO-3201`         30-May-2026    REL-05
                 limits too     vibration alert to                       
                 wide           $45\text{ }\mu\text{m}$ &                
                                shorten trend-review                     
                                cadence                                  

  **X2**         Cooler         Add lube-oil cooler dP &  30-Jun-2026    REL-02
                 integrity not  conductivity trend to                    
                 trended        reliability dashboard                    
  -------------------------------------------------------------------------------------

#### Risk Analysis of Corrective Actions

-   **Corrective Action:** Tighten vibration alert to
    $45\text{ }\mu\text{m}$
-   **Potential Risk:** Nuisance alerts on start-up transients
-   **Countermeasure:** Add start-up alarm suppression timer (Target
    Date: 30-May-2026 \| PIC: REL-05)

#### Established PM Schedule

-   **PM-1:** Weekly lube-oil water-content & particle count \|
    **Group:** Reliability \| **Interval:** Weekly
-   **PM-2:** 6-monthly lube-oil cooler leak test \| **Group:** Static
    \| **Interval:** 6-monthly
-   **PM-3:** Continuous vibration trend review `KO-3201` \| **Group:**
    Reliability \| **Interval:** Daily

# RCA 3: PM-4405B Motor Bearing Failure

### 1. Document Header & Identification

-   **AR Number:** AR-2026-NUP-0089
-   **Title / Problem:** Cooling Water Pump PM-4405B (Motor Driven) ---
    Motor Bearing Failure (Overheating)
-   **Tag / Plant Unit:** PM-4405B \| NUP (Nova Utility Plant)
-   **Equipment Class:** Class B
-   **Discipline:** ELE (Electrical)
-   **AR Type:** OPEDR (Operation) --- Uptime
-   **Date of Occurrence:** 08 Jul 2026
-   **Date Reported:** 08 Jul 2026
-   **Pre-Risk Level:** Level III (Score: 200)
-   **Severity:** Moderate
-   **PIC (RCA):** REL-02
-   **Procedure No.:** RCA-P-0050-03 \| **Form No.:** RCA-F-0075-02
-   **Downtime:** 8.0 hours
-   **Production Loss:** 160.0 ton
-   **Estimated Loss:** \$112.00k

#### Immediate Action

Start standby CW pump `PM-4405C`, isolate `PM-4405B`, replace motor DE &
NDE bearings.

#### Problem Statement

Cooling Water Pump `PM-4405B` motor tripped on 08-Jul-2026 due to
drive-end bearing failure from grease degradation and an over-extended
re-lubrication interval.

------------------------------------------------------------------------

### 2. Chronology of Events

-   **06-Jul-2026:** Cooling-water system running on `PM-4405B`; motor
    DE bearing temperature trending up
    ($68 \longrightarrow 84\text{ }^\circ\text{C}$).
-   **08-Jul-2026 13:20:** Motor bearing high-temperature alarm; motor
    tripped on winding/bearing over-temp.
-   **08-Jul-2026 13:35:** Standby `PM-4405C` started; cooling-water
    supply maintained at reduced margin.
-   **08-Jul-2026 16:00:** Motor DE bearing found seized; grease
    degraded/carbonized. NDE bearing marginal.
-   **08-Jul-2026 21:20:** DE & NDE bearings replaced and re-greased;
    motor recommissioned.

------------------------------------------------------------------------

### 3. Historical Data & 4W Assessment

#### Historical Data & Evidence

`PM-4405B` motor bearing temperature baseline is
$60\text{--}68\text{ }^\circ\text{C}$. Re-lubrication was performed on a
fixed 12-month interval regardless of duty/ambient. Bearing temperature
was not trended in CMMS, so degradation went unnoticed.

#### Impact Summary (4W)

-   **What:** `PM-4405B` motor DE bearing failed / overheated
-   **When:** 08-Jul-2026 (13:20)
-   **Scope:** Loss of one cooling-water pump; reduced CW margin
    (standby covered)
-   **Uptime Loss:**
    $8.0\text{ hours} \longrightarrow 160.0\text{ ton} \longrightarrow \$112.00\text{k}$

------------------------------------------------------------------------

### 4. Target Setting

-   **Actual Condition (Before):** CW pump motor trip due to bearing
    overheating.
-   **Target Condition (Project Y):** No motor bearing failure due to
    lubrication (bearing temp $< 75\text{ }^\circ\text{C}$, risk-based
    re-greasing).
-   **Target Metric:** Recurrence of equipment failure mode: Before =
    $1\text{ case} \longrightarrow$ Target = $0\text{ cases}$.

------------------------------------------------------------------------

### 5. Parameter Verification (4P Analysis)

  --------------------------------------------------------------------------------------
  \#              Problem                  Result           Evidence / Finding
                  Phenomenon /                              
                  Parameter                                 
  --------------- --------------- ------------------------- ----------------------------
  **P1**          Motor bearing            **NG**           DE bearing reached
                  temperature                               $84\text{ }^\circ\text{C}$
                  above limit                               vs
                                                            $75\text{ }^\circ\text{C}$
                                                            alarm --- grease breakdown.

  **P2**          Motor                     **G**           Running current
                  over-loaded                               $132\text{ A}$ vs
                  (high ampere)                             $150\text{ A}$ rated ---
                                                            within limit.

  **P3**          Cooling-fan /             **G**           Fan cowl clean; ambient
                  ventilation                               ventilation adequate.
                  blocked                                   

  **P4**          Grease type               **G**           Correct high-temp
                  incorrect                                 lithium-complex grease used.

  **P5**          Bearing beyond            **G**           Bearing in service 2 years
                  service life                              vs 5-year design --- within
                                                            life.
  --------------------------------------------------------------------------------------

*(Legend: **G** = Meets Standard / Good, **NG** = Does Not Meet Standard
/ Problem)*

------------------------------------------------------------------------

### 6. Root Cause Verification (4M + 1E)

  ----------------------------------------------------------------------------
  \#              Factor                    Result           Evidence /
                                                             Finding
  --------------- ---------------- ------------------------- -----------------
  **X1**          Re-lubrication            **NG**           Fixed 12-month
                  interval not                               interval too long
                  risk-based                                 for duty &
                                                             ambient ---
                                                             grease degraded.

  **X2**          Bearing                   **NG**           No
                  temperature not                            condition-based
                  trended in CMMS                            trigger; only
                                                             alarm at failure
                                                             point.

  **X3**          Vibration route           **NG**           `PM-4405B` not on
                  excludes utility                           the monthly
                  motors                                     vibration route.

  **X4**          Operator round             **G**           Rounds performed
                  frequency                                  per schedule;
                                                             local gauge read.
  ----------------------------------------------------------------------------

#### Verified Root Cause Statement

Motor drive-end bearing failure caused by grease degradation from an
over-extended, non-risk-based re-lubrication interval, undetected due to
absence of bearing-temperature trending, resulting in bearing
overheating and motor trip.

#### Priority Matrix Summary

High-impact root causes prioritized for intervention: `P1`, `X1`, `X2`,
`X3`.

------------------------------------------------------------------------

### 7. Corrective & Pro-Active Action Plan (CAPAA)

#### Corrective Actions

  ----------------------------------------------------------------------------
  RC             Action           Plan Date      PIC            Status
                 Description                                    
  -------------- ---------------- -------------- -------------- --------------
  **X1**         Revise           31-Jul-2026    REL-02         In Progress
                 `PM-4405B`                                     
                 re-lubrication                                 
                 interval to                                    
                 risk-based                                     
                 (4-monthly)                                    

  **X2**         Add motor        31-Aug-2026    REL-05         Open
                 bearing                                        
                 temperature                                    
                 trending & alert                               
                 to CMMS                                        
  ----------------------------------------------------------------------------

#### Pro-Active Actions (Fleet / Unit Roll-out)

  --------------------------------------------------------------------------
  RC             Action         Plan Date      PIC            Status
                 Description                                  
  -------------- -------------- -------------- -------------- --------------
  **X1**         Apply          31-Aug-2026    REL-02         Open
                 risk-based                                   
                 re-greasing to                               
                 all CW pump                                  
                 motors                                       

  **X2**         Extend         30-Sep-2026    REL-05         Open
                 bearing-temp                                 
                 trending to                                  
                 utility motor                                
                 fleet                                        
  --------------------------------------------------------------------------

------------------------------------------------------------------------

### 8. Preventive Actions, Risk Analysis & PM Schedule

#### Preventive Actions

  --------------------------------------------------------------------------
  Item           Possible Root  Preventive     Plan Date      PIC
                 Cause          Action                        
  -------------- -------------- -------------- -------------- --------------
  **X3**         Motor not on   Add            31-Jul-2026    REL-02
                 vibration      `PM-4405B/C`                  
                 route          to monthly                    
                                vibration &                   
                                thermography                  
                                route                         

  **P1**         Bearing        Verify motor   31-Jul-2026    ELE-01
                 over-temp      cooling-fan &                 
                                louvre                        
                                condition each                
                                PM                            
  --------------------------------------------------------------------------

#### Risk Analysis of Corrective Actions

-   **Corrective Action:** Shorten re-greasing interval
-   **Potential Risk:** Over-greasing risk (churning / seal push-out)
-   **Countermeasure:** Use metered re-greasing per bearing volume calc
    (Target Date: 31-Jul-2026 \| PIC: REL-02)

#### Established PM Schedule

-   **PM-1:** Risk-based motor bearing re-greasing `PM-4405B` \|
    **Group:** Electrical \| **Interval:** 4-monthly
-   **PM-2:** Monthly motor bearing temperature & vibration reading \|
    **Group:** Reliability \| **Interval:** Monthly

# RCA 4: HE-3301 High Fouling --- Duty Loss & High dP

### 1. Document Header & Identification

-   **AR Number:** AR-2026-ZCU-0165
-   **Title / Problem:** Feed/Effluent Heat Exchanger HE-3301 --- High
    Fouling --- Duty Loss & High dP
-   **Tag / Plant Unit:** HE-3301 \| ZCU (Zeta Cracker Unit)
-   **Equipment Class:** Class B
-   **Discipline:** STA (Static)
-   **AR Type:** OPEDR (Operation) --- Uptime
-   **Date of Occurrence:** 21 May 2026
-   **Date Reported:** 22 May 2026
-   **Pre-Risk Level:** Level III (Score: 400)
-   **Severity:** Moderate
-   **PIC (RCA):** STA-02
-   **Procedure No.:** RCA-P-0050-03 \| **Form No.:** RCA-F-0075-02
-   **Downtime:** 12.0 hours
-   **Production Loss:** 216.0 ton
-   **Estimated Loss:** \$183.60k

#### Immediate Action

Isolate `HE-3301`, bypass via spare train, hydro-jet clean tube bundle.

#### Problem Statement

Feed/Effluent Heat Exchanger `HE-3301` suffered accelerated tube-side
fouling reducing duty and raising dP, forcing an unplanned isolation,
cleaning and partial rate cut on 21-May-2026.

------------------------------------------------------------------------

### 2. Chronology of Events

-   **18-May-2026:** Heat-recovery section running; `HE-3301` tube-side
    dP rising ($0.4 \longrightarrow 0.9\text{ bar}$) and cold-outlet
    temperature falling.
-   **21-May-2026 09:00:** Preheat duty dropped $\sim 35\%$ below
    design; unit rate reduced to protect downstream. Exchanger isolated.
-   **21-May-2026 11:30:** Tube bundle inspected --- heavy coke/polymer
    deposition on tube side.
-   **21-May-2026 21:00:** Bundle hydro-jet cleaned and returned to
    service; duty and dP restored, rate ramped back to $30\text{ T/H}$.

------------------------------------------------------------------------

### 3. Historical Data & 4W Assessment

#### Historical Data & Evidence

`HE-3301` tube-side dP baseline is $0.3\text{--}0.4\text{ bar}$; heat
duty design $100\%$. Over the run, dP climbed steadily while duty fell
--- a classic fouling curve. No dP-based cleaning trigger existed, so
fouling was allowed to progress to a forced cut.

#### Impact Summary (4W)

-   **What:** `HE-3301` duty loss & high dP from tube-side fouling
-   **When:** 21-May-2026 (09:00)
-   **Scope:** Partial rate cut of ZCU heat-recovery section
-   **Uptime Loss:**
    $12.0\text{ hours} \longrightarrow 216.0\text{ ton} \longrightarrow \$183.60\text{k}$

------------------------------------------------------------------------

### 4. Target Setting

-   **Actual Condition (Before):** Rate cut due to `HE-3301` fouling
    (duty loss + high dP).
-   **Target Condition (Project Y):** No unplanned rate cut due to
    `HE-3301` fouling ($\text{dP} < 0.6\text{ bar}$,
    $\text{duty} > 90\%$).
-   **Target Metric:** Recurrence of equipment failure mode: Before =
    $1\text{ case} \longrightarrow$ Target = $0\text{ cases}$.

------------------------------------------------------------------------

### 5. Parameter Verification (4P Analysis)

  ------------------------------------------------------------------------------
  \#              Problem                    Result           Evidence / Finding
                  Phenomenon /                                
                  Parameter                                   
  --------------- ----------------- ------------------------- ------------------
  **P1**          Tube-side dP               **NG**           dP reached
                  above limit                                 $0.9\text{ bar}$
                                                              vs
                                                              $0.6\text{ bar}$
                                                              limit --- heavy
                                                              fouling.

  **P2**          Heat duty below            **NG**           Duty fell to
                  design                                      $\sim 65\%$ of
                                                              design --- loss of
                                                              preheat.

  **P3**          Feed heavy-ends            **NG**           Heavy-ends $2.4\%$
                  above spec                                  vs $< 1.5\%$
                                                              design ---
                                                              increased fouling
                                                              precursor.

  **P4**          Tube velocity               **G**           Tube velocity
                  below design                                $1.9\text{ m/s}$
                                                              vs
                                                              $1.5\text{ m/s}$
                                                              min --- adequate.

  **P5**          Cooling/heating             **G**           Shell-side inlet
                  medium                                      temperature within
                  temperature off                             normal band.
  ------------------------------------------------------------------------------

*(Legend: **G** = Meets Standard / Good, **NG** = Does Not Meet Standard
/ Problem)*

------------------------------------------------------------------------

### 6. Root Cause Verification (4M + 1E)

  -------------------------------------------------------------------------
  \#              Factor                   Result           Evidence /
                                                            Finding
  --------------- --------------- ------------------------- ---------------
  **X1**          No dP-based              **NG**           Cleaning was
                  cleaning                                  time-based
                  trigger                                   only; no dP
                                                            alarm to
                                                            trigger action.

  **X2**          Feed filtration          **NG**           Upstream filter
                  performance not                           dP not
                  trended                                   monitored,
                                                            allowing
                                                            heavy-ends
                                                            carry-over.

  **X3**          Fouling KPI not          **NG**           No fouling
                  on dashboard                              factor / duty
                                                            KPI tracked
                                                            between TAs.

  **X4**          Bundle                    **G**           Bundle
                  metallurgy                                metallurgy
                  inadequate                                suitable for
                                                            service.
  -------------------------------------------------------------------------

#### Verified Root Cause Statement

Accelerated tube-side coke/polymer fouling driven by higher-than-design
feed heavy-ends, allowed to progress by the absence of a dP-based
cleaning trigger and fouling KPI, causing duty loss, high dP and a
forced rate cut.

#### Priority Matrix Summary

High-impact root causes prioritized for intervention: `P1`, `P2`, `P3`,
`X1`, `X2`, `X3`.

------------------------------------------------------------------------

### 7. Corrective & Pro-Active Action Plan (CAPAA)

#### Corrective Actions

  --------------------------------------------------------------------------
  RC             Action         Plan Date      PIC            Status
                 Description                                  
  -------------- -------------- -------------- -------------- --------------
  **X1**         Add dP-based   22-Jun-2026    STA-02         In Progress
                 cleaning                                     
                 trigger &                                    
                 alarm for                                    
                 `HE-3301`                                    

  **P3**         Tighten feed   30-Jun-2026    ROT-01         Open
                 heavy-ends                                   
                 control &                                    
                 filtration                                   
  --------------------------------------------------------------------------

#### Pro-Active Actions (Fleet / Unit Roll-out)

  ------------------------------------------------------------------------------
  RC             Action Description Plan Date      PIC            Status
  -------------- ------------------ -------------- -------------- --------------
  **X1**         Apply dP-trigger   22-Jul-2026    STA-02         Open
                 logic to parallel                                
                 exchangers                                       
                 `HE-3302`/`3303`                                 

  **P3**         Review upstream    31-Jul-2026    ROT-01         Open
                 fractionation                                    
                 cut-point control                                
  ------------------------------------------------------------------------------

------------------------------------------------------------------------

### 8. Preventive Actions, Risk Analysis & PM Schedule

#### Preventive Actions

  --------------------------------------------------------------------------
  Item           Possible Root  Preventive     Plan Date      PIC
                 Cause          Action                        
  -------------- -------------- -------------- -------------- --------------
  **X3**         No fouling KPI Add fouling    22-Jun-2026    STA-02
                                factor & duty                 
                                KPI to                        
                                reliability                   
                                dashboard                     

  **X2**         Filter not     Add upstream   30-Jun-2026    ROT-01
                 trended        filter dP                     
                                trend &                       
                                replacement                   
                                trigger                       
  --------------------------------------------------------------------------

#### Risk Analysis of Corrective Actions

-   **Corrective Action:** Add dP cleaning trigger
-   **Potential Risk:** Premature/over-frequent cleaning
-   **Countermeasure:** Set trigger with hysteresis + engineering review
    before cleaning (Target Date: 22-Jun-2026 \| PIC: STA-02)

#### Established PM Schedule

-   **PM-1:** Daily `HE-3301` dP & duty trend review \| **Group:**
    Process \| **Interval:** Daily
-   **PM-2:** Bundle inspection & cleaning at dP trigger / next TA \|
    **Group:** Static \| **Interval:** Condition / TA

# RCA 5: BL-5702 High Vibration (Coupling Misalignment)

### 1. Document Header & Identification

-   **AR Number:** AR-2026-OPP-0203
-   **Title / Problem:** Product Blower BL-5702 --- High Vibration
    (Coupling Misalignment)
-   **Tag / Plant Unit:** BL-5702 \| OPP (Orion Polypropylene Plant)
-   **Equipment Class:** Class A
-   **Discipline:** ROT (Rotating)
-   **AR Type:** OPEDR (Operation) --- Uptime
-   **Date of Occurrence:** 17 Jun 2026
-   **Date Reported:** 18 Jun 2026
-   **Pre-Risk Level:** Level III (Score: 400)
-   **Severity:** Major
-   **PIC (RCA):** ROT-01
-   **Procedure No.:** RCA-P-0050-03 \| **Form No.:** RCA-F-0075-02
-   **Downtime:** 14.0 hours
-   **Production Loss:** 532.0 ton
-   **Estimated Loss:** \$478.80k

#### Immediate Action

Stop `BL-5702`, re-align coupling, replace worn coupling element.

#### Problem Statement

Product Blower `BL-5702` tripped on high vibration on 17-Jun-2026 due to
coupling misalignment and a worn coupling element, halting the OPP
powder-handling section.

------------------------------------------------------------------------

### 2. Chronology of Events

-   **15-Jun-2026:** OPP running normal; `BL-5702` vibration trending up
    ($4.2 \longrightarrow 8.5\text{ mm/s}$) with $2\text{X}$ harmonic
    rising.
-   **17-Jun-2026 04:30:** `BL-5702` vibration reached alarm
    ($11\text{ mm/s}$); blower stopped to prevent damage --- powder
    handling section halted.
-   **17-Jun-2026 07:00:** Coupling element found worn/cracked; laser
    alignment showed $0.35\text{ mm}$ offset (spec $< 0.05\text{ mm}$).
-   **17-Jun-2026 18:30:** Coupling element replaced, unit re-aligned to
    $< 0.05\text{ mm}$, blower restarted to $38\text{ T/H}$.

------------------------------------------------------------------------

### 3. Historical Data & 4W Assessment

#### Historical Data & Evidence

`BL-5702` vibration baseline is $3.5\text{--}4.5\text{ mm/s}$. A rising
trend with dominant $2\text{X}$ harmonic over 2 days indicated
developing misalignment. Alignment was last verified 14 months prior; no
soft-foot / alignment check in the routine PM.

#### Impact Summary (4W)

-   **What:** `BL-5702` high vibration from coupling misalignment
-   **When:** 17-Jun-2026 (04:30)
-   **Scope:** OPP powder-handling section stop
-   **Uptime Loss:**
    $14.0\text{ hours} \longrightarrow 532.0\text{ ton} \longrightarrow \$478.80\text{k}$

------------------------------------------------------------------------

### 4. Target Setting

-   **Actual Condition (Before):** Blower stop due to high vibration
    (misalignment).
-   **Target Condition (Project Y):** No blower stop due to misalignment
    (vibration $< 7\text{ mm/s}$, alignment $< 0.05\text{ mm}$).
-   **Target Metric:** Recurrence of equipment failure mode: Before =
    $1\text{ case} \longrightarrow$ Target = $0\text{ cases}$.

------------------------------------------------------------------------

### 5. Parameter Verification (4P Analysis)

  --------------------------------------------------------------------------------
  \#              Problem                  Result           Evidence / Finding
                  Phenomenon /                              
                  Parameter                                 
  --------------- --------------- ------------------------- ----------------------
  **P1**          Overall                  **NG**           Vibration reached
                  vibration above                           $11\text{ mm/s}$ vs
                  alarm                                     $7\text{ mm/s}$ alarm
                                                            --- misalignment
                                                            signature.

  **P2**          Coupling                 **NG**           Offset
                  alignment out                             $0.35\text{ mm}$ vs
                  of tolerance                              $< 0.05\text{ mm}$
                                                            spec ---
                                                            angular/parallel
                                                            misalignment.

  **P3**          Bearing                   **G**           Bearing
                  condition                                 envelope/shock-pulse
                  degraded                                  normal --- no bearing
                                                            defect.

  **P4**          Foundation /             **NG**           Soft-foot
                  soft-foot                                 $0.12\text{ mm}$ found
                                                            on one foot ---
                                                            contributed to
                                                            misalignment.

  **P5**          Rotor unbalance           **G**           $1\text{X}$ component
                                                            within balance grade
                                                            --- no unbalance.
  --------------------------------------------------------------------------------

*(Legend: **G** = Meets Standard / Good, **NG** = Does Not Meet Standard
/ Problem)*

------------------------------------------------------------------------

### 6. Root Cause Verification (4M + 1E)

  -------------------------------------------------------------------------
  \#              Factor                   Result           Evidence /
                                                            Finding
  --------------- --------------- ------------------------- ---------------
  **X1**          Alignment check          **NG**           PM did not
                  not in routine                            include
                  PM                                        periodic laser
                                                            alignment /
                                                            soft-foot
                                                            check.

  **X2**          Coupling                 **NG**           Elastomer
                  element life                              coupling
                  not tracked                               element run
                                                            beyond
                                                            recommended
                                                            12-month life.

  **X3**          Vibration route          **NG**           Monthly route
                  interval too                              missed the
                  long                                      fast-rising
                                                            2-day trend.

  **X4**          Alignment tools           **G**           Laser alignment
                  / competency                              tool & trained
                                                            technicians
                                                            available.
  -------------------------------------------------------------------------

#### Verified Root Cause Statement

High vibration from coupling misalignment aggravated by soft-foot and an
over-aged elastomer coupling element, undetected because periodic
alignment/soft-foot checks were absent from the PM and the vibration
route interval was too long.

#### Priority Matrix Summary

High-impact root causes prioritized for intervention: `P1`, `P2`, `P4`,
`X1`, `X2`, `X3`.

------------------------------------------------------------------------

### 7. Corrective & Pro-Active Action Plan (CAPAA)

#### Corrective Actions

  --------------------------------------------------------------------------
  RC             Action         Plan Date      PIC            Status
                 Description                                  
  -------------- -------------- -------------- -------------- --------------
  **X1**         Add periodic   18-Jul-2026    ROT-01         In Progress
                 laser                                        
                 alignment &                                  
                 soft-foot                                    
                 check to                                     
                 `BL-5702` PM                                 

  **X2**         Track coupling 18-Jul-2026    REL-05         Open
                 element life &                               
                 replace at 12                                
                 months                                       
  --------------------------------------------------------------------------

#### Pro-Active Actions (Fleet / Unit Roll-out)

  ------------------------------------------------------------------------------
  RC             Action Description Plan Date      PIC            Status
  -------------- ------------------ -------------- -------------- --------------
  **X1**         Roll out alignment 18-Aug-2026    ROT-01         Open
                 check to all                                     
                 Class-A blowers in                               
                 OPP                                              

  **X2**         Create             31-Aug-2026    REL-05         Open
                 coupling-element                                 
                 replacement                                      
                 register for OPP                                 
                 trains                                           
  ------------------------------------------------------------------------------

------------------------------------------------------------------------

### 8. Preventive Actions, Risk Analysis & PM Schedule

#### Preventive Actions

  --------------------------------------------------------------------------
  Item           Possible Root  Preventive     Plan Date      PIC
                 Cause          Action                        
  -------------- -------------- -------------- -------------- --------------
  **X3**         Route interval Shorten        18-Jul-2026    REL-05
                 too long       `BL-5702`                     
                                vibration                     
                                route to                      
                                weekly                        

  **P4**         Soft-foot      Correct        18-Jun-2026    ROT-01
                                soft-foot &                   
                                re-shim                       
                                baseplate                     
                                `BL-5702`                     
  --------------------------------------------------------------------------

#### Risk Analysis of Corrective Actions

-   **Corrective Action:** Shorten vibration route to weekly
-   **Potential Risk:** Increased inspection workload
-   **Countermeasure:** Use wireless vibration sensor for continuous
    trend (Target Date: 18-Jul-2026 \| PIC: REL-05)

#### Established PM Schedule

-   **PM-1:** 6-monthly laser alignment & soft-foot check `BL-5702` \|
    **Group:** Rotating \| **Interval:** 6-monthly
-   **PM-2:** Coupling element inspection/replacement \| **Group:**
    Rotating \| **Interval:** 12-monthly
-   **PM-3:** Weekly vibration trend review `BL-5702` \| **Group:**
    Reliability \| **Interval:** Weekly

# Appendix C. Complete equipment, incident, and production dataset

# Equipment Performance, Incident Database, and Production Data

> Markdown conversion of
> `combined_equipmentperf_incidentdb_proddata.pdf`. The content below
> preserves source terminology and values. No external data or new
> engineering conclusions have been added.

## 1. Document structure

``` mermaid
flowchart TD
    A[Hourly DCS / production data] --> B[Condition monitoring records]
    B --> C[Performance summaries]
    D[Incident register] --> E[Risk case / CAPA-PAA]
    E --> F[RCA status and failure mechanism]
    E --> G[Downtime and loss]
    D -. linked by MTO, AR, plant, tag .-> B
    B -. linked RCA / AR .-> E
```

The PDF contains five 30-day hourly equipment datasets, five
condition-monitoring records, a 380-incident dashboard and incident
register, risk-case information, RCA status and failure-mechanism
information, and downtime/loss data. The five monitored equipment tags
are PU-2101B, KO-3201, PM-4405B, HE-3301, and BL-5702.

## 2. Incident database dashboard

  ---------------------------------------------------------------------
  KPI                                Value
  ---------------------------------- ----------------------------------
  Total Incidents                    380

  Total Downtime (hrs)               2261.1

  Total Loss (k US$) | 67194.43 |    176.827447368
  | Avg Loss per Incident (k US$)    
  ---------------------------------------------------------------------

### Overall status

  Status              Incident count
  ------------------- ----------------
  RISK CLOSED         113
  CA/PA EXECUTION     92
  RCA PROCESS         71
  RISK CANCELED       47
  MONITORING RESULT   37
  NEW REGISTERED      20

### Discipline

  Discipline   Incident count
  ------------ ----------------
  ROT          145
  INS          87
  STA          87
  ELE          61

### Plant

  Plant   Incident count   Loss (k US\$)
  ------- ---------------- ---------------
  ZCU     62               11112.66
  ARP     49               9083.29
  OPP     42               7544.96
  OP2     37               5808.57
  SMX     42               7434.88
  BRP     26               5099.84
  OP3     32               5264.34
  NUP     24               5489.07
  CRP     25               3344.59
  BDX     20               2791.42
  OPU     14               3202.86
  TKX     7                1017.95

### Equipment type

  Equipment type   Incident count
  ---------------- ----------------
  PU               31
  CO               25
  BL               31
  FA               17
  EM               40
  VA               15
  TX               47
  HB               21
  TK               19
  RX               22
  PZ               24
  SX               21

## 3. Equipment raw data

Each equipment section contains 720 hourly observations, equivalent to
30 days. The source PDF presents the first four process variables and
the remaining three columns on a continuation table. They are recombined
here into one normalized table.

### PU2101B

Source pages: 1-33.

#### Data dictionary

  Name           Description                     Digital set   Engineering units   Span
  -------------- ------------------------------- ------------- ------------------- ------
  Name           Description                     digitalset    engunits            span
  PU2101B_FEED   PU-2101B FEED RATE              T/H           20.4                
  PU2101B_DISP   PU-2101B DISCHARGE PRESSURE     BARG          20                  
  PU2101B_VIB    PU-2101B VIBRATION              MM/S          20                  
  PU2101B_TEMP   PU-2101B BEARING/PROCESS TEMP   DEG C         150                 
  PU2101B_AMP    PU-2101B MOTOR AMPERE           A             300                 
  PLANT_RATE     ARP PRODUCTION RATE             T/H           17.68               
  RUN_STATUS     PU-2101B RUN STATUS             ON_OFF        ON_OFF              1

#### Typical value, zero, and instrument tag

## Typical value Zero Instrument tag --------------- ------

#### Hourly data

  --------------------------------------------------------------------------------------
  Timestamp    Feed     Discharge   Vibration   Temperature   Motor    Plant    Run
                        pressure                              ampere   rate     status
  ------------ -------- ----------- ----------- ------------- -------- -------- --------
  2026-03-01   14.06    9.221       3.129       66.49         143.52   14.029   ON
  00:00:00                                                                      

  2026-03-01   13.473   9.426       3.416       64.29         138      14.009   ON
  01:00:00                                                                      

  2026-03-01   13.609   9.213       3.907       65.86         131.99   13.911   ON
  02:00:00                                                                      

  2026-03-01   13.711   9.516       3.998       65.08         136.3    13.743   ON
  03:00:00                                                                      

  2026-03-01   13.385   9.631       3.475       66.32         123.37   13.756   ON
  04:00:00                                                                      

  2026-03-01   13.601   9.314       3.828       65.23         132.56   13.701   ON
  05:00:00                                                                      

  2026-03-01   13.6     9.439       4.208       61.99         139.85   13.925   ON
  06:00:00                                                                      

  2026-03-01   13.123   9.699       3.842       66.09         132.66   14.226   ON
  07:00:00                                                                      

  2026-03-01   13.877   9.487       3.725       64.35         135.45   13.618   ON
  08:00:00                                                                      

  2026-03-01   13.763   9.314       3.954       66.39         130.26   13.708   ON
  09:00:00                                                                      

  2026-03-01   13.43    9.303       3.933       65.23         138      13.608   ON
  10:00:00                                                                      

  2026-03-01   13.553   9.198       3.821       67.2          135.32   13.857   ON
  11:00:00                                                                      

  2026-03-01   13.737   9.616       3.667       64.59         134.85   14.148   ON
  12:00:00                                                                      

  2026-03-01   13.529   9.388       3.695       61.98         138.58   13.782   ON
  13:00:00                                                                      

  2026-03-01   13.534   9.658       3.824       64.58         141.39   13.954   ON
  14:00:00                                                                      

  2026-03-01   13.205   9.63        3.664       65.84         138.03   13.246   ON
  15:00:00                                                                      

  2026-03-01   13.751   9.401       4.135       64.55         127.91   13.832   ON
  16:00:00                                                                      

  2026-03-01   13.634   9.421       4.025       64.36         136.42   14.003   ON
  17:00:00                                                                      

  2026-03-01   13.675   9.617       4.073       67.27         135.88   13.706   ON
  18:00:00                                                                      

  2026-03-01   13.185   9.522       4.308       64.83         130.24   13.432   ON
  19:00:00                                                                      

  2026-03-01   14.049   9.54        4.196       66.64         128.36   13.995   ON
  20:00:00                                                                      

  2026-03-01   13.642   9.253       4.156       65.29         133.17   13.842   ON
  21:00:00                                                                      

  2026-03-01   13.495   9.635       3.894       62.89         133.6    14.359   ON
  22:00:00                                                                      

  2026-03-01   14.152   9.369       3.753       63.65         134.52   13.716   ON
  23:00:00                                                                      

  2026-03-02   13.588   9.16        4.376       64.59         131.86   13.83    ON
  00:00:00                                                                      

  2026-03-02   13.205   9.407       3.633       65.52         135.41   13.769   ON
  01:00:00                                                                      

  2026-03-02   13.49    9.563       3.646       63.84         135.95   13.899   ON
  02:00:00                                                                      

  2026-03-02   12.978   9.815       3.584       62.94         133.62   13.382   ON
  03:00:00                                                                      

  2026-03-02   13.885   9.444       3.855       63.54         136.31   14.237   ON
  04:00:00                                                                      

  2026-03-02   13.487   9.301       3.906       64.28         132.42   14.043   ON
  05:00:00                                                                      

  2026-03-02   13.398   9.819       4.059       63.73         128.48   13.81    ON
  06:00:00                                                                      

  2026-03-02   13.892   9.524       3.745       64.18         134.73   13.775   ON
  07:00:00                                                                      

  2026-03-02   13.151   9.461       3.368       67.85         138.28   14.011   ON
  08:00:00                                                                      

  2026-03-02   13.746   9.339       3.881       65.48         145.55   13.969   ON
  09:00:00                                                                      

  2026-03-02   13.038   9.349       4.045       63.83         126.25   13.759   ON
  10:00:00                                                                      

  2026-03-02   13.42    9.722       3.809       65.04         132.74   13.827   ON
  11:00:00                                                                      

  2026-03-02   13.272   9.459       3.768       67.42         131.25   13.964   ON
  12:00:00                                                                      

  2026-03-02   13.998   9.419       3.942       66.03         135.83   13.757   ON
  13:00:00                                                                      

  2026-03-02   14.08    9.424       4.159       64.9          131.25   13.783   ON
  14:00:00                                                                      

  2026-03-02   13.51    9.735       3.784       63.02         135.26   13.757   ON
  15:00:00                                                                      

  2026-03-02   13.829   9.412       3.446       62.51         138.71   13.775   ON
  16:00:00                                                                      

  2026-03-02   13.551   9.594       3.66        64.54         131.77   13.523   ON
  17:00:00                                                                      

  2026-03-02   13.755   9.54        3.76        64.9          134.47   13.619   ON
  18:00:00                                                                      

  2026-03-02   13.395   9.536       3.351       62.62         141.23   13.971   ON
  19:00:00                                                                      

  2026-03-02   13.135   9.368       3.993       63.05         138.31   14.084   ON
  20:00:00                                                                      

  2026-03-02   13.11    9.599       3.609       64.99         128.3    13.858   ON
  21:00:00                                                                      

  2026-03-02   13.704   9.741       3.928       61.73         143.07   12.911   ON
  22:00:00                                                                      

  2026-03-02   14.211   9.492       3.849       62.47         132.05   13.474   ON
  23:00:00                                                                      

  2026-03-03   13.673   9.362       3.723       64.97         136      13.982   ON
  00:00:00                                                                      

  2026-03-03   13.457   9.306       4.208       65.89         133.13   14.325   ON
  01:00:00                                                                      

  2026-03-03   14.12    9.529       3.66        65.53         132.97   14.197   ON
  02:00:00                                                                      

  2026-03-03   13.665   9.459       3.632       66.55         132.02   13.817   ON
  03:00:00                                                                      

  2026-03-03   13.628   9.484       3.874       67.42         137.27   13.778   ON
  04:00:00                                                                      

  2026-03-03   13.669   9.502       4.01        66.4          131.7    13.757   ON
  05:00:00                                                                      

  2026-03-03   13.564   9.279       3.8         64.66         129.76   14.339   ON
  06:00:00                                                                      

  2026-03-03   13.516   9.617       3.555       68.25         132.52   13.936   ON
  07:00:00                                                                      

  2026-03-03   13.21    9.535       3.973       67.58         134.8    13.626   ON
  08:00:00                                                                      

  2026-03-03   13.736   9.489       3.951       66.47         126.78   14.128   ON
  09:00:00                                                                      

  2026-03-03   13.574   9.535       4.319       63.84         137.97   14.096   ON
  10:00:00                                                                      

  2026-03-03   13.925   9.639       3.745       65.66         131.93   13.331   ON
  11:00:00                                                                      

  2026-03-03   13.5     9.508       3.854       61.92         137.7    13.704   ON
  12:00:00                                                                      

  2026-03-03   13.081   9.372       3.658       64.56         140.33   14.144   ON
  13:00:00                                                                      

  2026-03-03   13.573   9.675       3.428       61.33         136.07   14.118   ON
  14:00:00                                                                      

  2026-03-03   14.062   9.435       3.819       64.43         136.95   13.54    ON
  15:00:00                                                                      

  2026-03-03   13.496   9.391       4.013       66.6          133.01   13.874   ON
  16:00:00                                                                      

  2026-03-03   13.358   9.266       3.547       65.09         132.13   14.11    ON
  17:00:00                                                                      

  2026-03-03   13.275   9.501       3.631       67.49         127.23   13.967   ON
  18:00:00                                                                      

  2026-03-03   13.314   9.343       3.506       65.07         134.04   13.593   ON
  19:00:00                                                                      

  2026-03-03   13.518   9.422       4.135       65.22         132.63   13.825   ON
  20:00:00                                                                      

  2026-03-03   13.279   9.567       3.642       64.62         125.35   14.053   ON
  21:00:00                                                                      

  2026-03-03   14.007   9.505       3.945       65.87         135.91   14.007   ON
  22:00:00                                                                      

  2026-03-03   13.523   9.652       3.584       65.02         140.89   13.617   ON
  23:00:00                                                                      

  2026-03-04   13.63    9.546       3.819       66.88         136.43   14.504   ON
  00:00:00                                                                      

  2026-03-04   13.991   9.439       3.644       67.5          139.47   13.936   ON
  01:00:00                                                                      

  2026-03-04   14.009   9.451       3.213       65.64         133.75   13.474   ON
  02:00:00                                                                      

  2026-03-04   13.542   9.424       3.819       63.39         130.76   13.788   ON
  03:00:00                                                                      

  2026-03-04   13.69    9.597       3.932       65.92         135.08   13.142   ON
  04:00:00                                                                      

  2026-03-04   13.8     9.503       3.279       67.12         133.44   13.693   ON
  05:00:00                                                                      

  2026-03-04   13.548   9.438       3.756       66.06         130.28   13.866   ON
  06:00:00                                                                      

  2026-03-04   13.116   9.627       3.692       65.52         138.95   14.523   ON
  07:00:00                                                                      

  2026-03-04   13.778   9.514       3.53        66.5          135.5    13.93    ON
  08:00:00                                                                      

  2026-03-04   13.843   9.43        3.737       67.06         132.21   13.977   ON
  09:00:00                                                                      

  2026-03-04   13.713   9.273       3.315       61.17         135.61   14.082   ON
  10:00:00                                                                      

  2026-03-04   13.349   9.566       3.863       67.37         134.24   13.935   ON
  11:00:00                                                                      

  2026-03-04   13.547   9.536       4.097       66.25         137.3    13.719   ON
  12:00:00                                                                      

  2026-03-04   13.439   9.508       3.485       65.81         141.21   14.243   ON
  13:00:00                                                                      

  2026-03-04   13.518   9.435       3.784       64.25         132.36   14.019   ON
  14:00:00                                                                      

  2026-03-04   13.953   9.375       4.156       65.43         130.06   14.293   ON
  15:00:00                                                                      

  2026-03-04   14.016   9.466       3.831       66            140.35   14.156   ON
  16:00:00                                                                      

  2026-03-04   13.782   9.535       3.67        62.86         144.42   13.63    ON
  17:00:00                                                                      

  2026-03-04   13.749   9.481       3.572       66.21         132.41   13.758   ON
  18:00:00                                                                      

  2026-03-04   13.784   9.478       3.844       65.2          131.2    13.773   ON
  19:00:00                                                                      

  2026-03-04   13.597   9.43        3.767       67.29         130.05   13.778   ON
  20:00:00                                                                      

  2026-03-04   13.579   9.551       3.958       66.11         134.82   14.001   ON
  21:00:00                                                                      

  2026-03-04   13.417   9.535       3.42        64.83         135.28   13.834   ON
  22:00:00                                                                      

  2026-03-04   13.585   9.387       4.069       65.17         133.81   13.67    ON
  23:00:00                                                                      

  2026-03-05   14.215   9.614       3.699       66.05         138.2    14.274   ON
  00:00:00                                                                      

  2026-03-05   13.836   9.619       3.961       65.31         131.59   14.246   ON
  01:00:00                                                                      

  2026-03-05   13.507   9.622       3.619       65.91         132.48   13.893   ON
  02:00:00                                                                      

  2026-03-05   13.472   9.48        3.476       64.02         129.85   13.6     ON
  03:00:00                                                                      

  2026-03-05   13.365   9.471       3.658       63.22         140.4    13.718   ON
  04:00:00                                                                      

  2026-03-05   13.702   9.326       3.561       64.23         139.16   13.682   ON
  05:00:00                                                                      

  2026-03-05   13.707   9.613       3.706       62.95         140.09   13.645   ON
  06:00:00                                                                      

  2026-03-05   13.207   9.18        3.962       63.92         131.5    13.624   ON
  07:00:00                                                                      

  2026-03-05   13.732   9.441       4.07        65.62         140.22   13.947   ON
  08:00:00                                                                      

  2026-03-05   13.445   9.449       3.851       62.64         136.04   13.963   ON
  09:00:00                                                                      

  2026-03-05   13.988   9.628       3.665       63.24         137.75   13.999   ON
  10:00:00                                                                      

  2026-03-05   13.643   9.5         3.687       66.19         137.2    13.635   ON
  11:00:00                                                                      

  2026-03-05   14.067   9.355       3.948       64.3          133.61   13.963   ON
  12:00:00                                                                      

  2026-03-05   13.475   9.286       4.084       65.07         134.22   14.415   ON
  13:00:00                                                                      

  2026-03-05   13.522   9.391       3.719       63.24         128.75   13.947   ON
  14:00:00                                                                      

  2026-03-05   13.682   9.516       3.769       63.52         132.71   13.78    ON
  15:00:00                                                                      

  2026-03-05   13.887   9.508       3.612       64.63         133.99   14.612   ON
  16:00:00                                                                      

  2026-03-05   13.754   9.47        3.852       67.54         130.28   13.968   ON
  17:00:00                                                                      

  2026-03-05   13.264   9.397       4.039       65.76         135.29   13.718   ON
  18:00:00                                                                      

  2026-03-05   13.65    9.468       3.074       62.58         140.01   14.12    ON
  19:00:00                                                                      

  2026-03-05   13.606   9.65        3.864       65.76         132.93   13.695   ON
  20:00:00                                                                      

  2026-03-05   13.483   9.335       3.662       66.47         131.05   13.788   ON
  21:00:00                                                                      

  2026-03-05   13.424   9.505       3.218       66.13         131.5    14.153   ON
  22:00:00                                                                      

  2026-03-05   14.075   9.743       3.878       63.25         135.66   13.723   ON
  23:00:00                                                                      

  2026-03-06   13.494   9.583       3.778       64.99         141.88   13.49    ON
  00:00:00                                                                      

  2026-03-06   13.37    9.432       3.892       68.28         135.57   14.073   ON
  01:00:00                                                                      

  2026-03-06   13.773   9.599       3.458       63.69         135.13   14.108   ON
  02:00:00                                                                      

  2026-03-06   13.636   9.387       4.334       65.59         129.96   13.518   ON
  03:00:00                                                                      

  2026-03-06   13.579   9.501       3.828       63.96         136.24   13.793   ON
  04:00:00                                                                      

  2026-03-06   13.813   9.733       3.714       63.18         137.42   14.175   ON
  05:00:00                                                                      

  2026-03-06   13.733   9.784       4.181       64.44         133.3    13.953   ON
  06:00:00                                                                      

  2026-03-06   13.699   9.244       3.963       66.64         134.81   14.109   ON
  07:00:00                                                                      

  2026-03-06   13.862   9.605       4.008       66.83         132.28   13.855   ON
  08:00:00                                                                      

  2026-03-06   13.677   9.792       4.091       63.77         137.85   13.719   ON
  09:00:00                                                                      

  2026-03-06   13.432   9.418       3.282       64.38         140.25   13.738   ON
  10:00:00                                                                      

  2026-03-06   13.501   9.539       4.217       63.76         136.43   13.806   ON
  11:00:00                                                                      

  2026-03-06   13.458   9.726       3.713       61.97         136.95   13.936   ON
  12:00:00                                                                      

  2026-03-06   13.657   9.426       3.871       66            135.13   13.171   ON
  13:00:00                                                                      

  2026-03-06   13.307   9.568       4.031       67.43         132.36   13.379   ON
  14:00:00                                                                      

  2026-03-06   13.102   9.491       3.622       67.34         131.84   13.891   ON
  15:00:00                                                                      

  2026-03-06   13.624   9.211       3.879       64.39         133.31   14.068   ON
  16:00:00                                                                      

  2026-03-06   13.236   9.552       3.991       67.09         135.38   13.714   ON
  17:00:00                                                                      

  2026-03-06   13.069   9.472       3.79        66.73         134.9    13.892   ON
  18:00:00                                                                      

  2026-03-06   13.702   9.639       3.924       64.59         138.96   13.604   ON
  19:00:00                                                                      

  2026-03-06   13.407   9.814       3.399       65.09         137.87   13.523   ON
  20:00:00                                                                      

  2026-03-06   13.735   9.603       3.502       64.54         140.85   13.933   ON
  21:00:00                                                                      

  2026-03-06   13.456   9.445       3.512       65.46         138.02   13.873   ON
  22:00:00                                                                      

  2026-03-06   13.295   9.568       3.893       67.82         133.96   13.755   ON
  23:00:00                                                                      

  2026-03-07   13.262   9.53        4.736       63.71         135.31   13.545   ON
  00:00:00                                                                      

  2026-03-07   13.46    9.653       3.866       63.31         128.46   13.91    ON
  01:00:00                                                                      

  2026-03-07   13.526   9.284       3.763       66.41         141.58   13.874   ON
  02:00:00                                                                      

  2026-03-07   13.376   9.325       3.784       65.19         132.61   13.823   ON
  03:00:00                                                                      

  2026-03-07   13.524   9.193       4.046       62.27         133.31   13.858   ON
  04:00:00                                                                      

  2026-03-07   13.182   9.591       3.978       63.59         142.19   13.792   ON
  05:00:00                                                                      

  2026-03-07   13.604   9.497       3.513       63.87         130.66   14.028   ON
  06:00:00                                                                      

  2026-03-07   13.112   9.404       4.054       64.19         132.47   13.994   ON
  07:00:00                                                                      

  2026-03-07   13.547   9.391       3.794       65.59         134.69   14.362   ON
  08:00:00                                                                      

  2026-03-07   13.79    9.414       4.005       66.6          132.63   14.261   ON
  09:00:00                                                                      

  2026-03-07   13.897   9.361       3.3         64.87         135.3    13.876   ON
  10:00:00                                                                      

  2026-03-07   14.066   9.452       3.411       65.33         135.92   13.561   ON
  11:00:00                                                                      

  2026-03-07   13.177   9.426       3.949       63.99         137.48   14.054   ON
  12:00:00                                                                      

  2026-03-07   13.806   9.708       3.35        66.64         134.52   13.727   ON
  13:00:00                                                                      

  2026-03-07   13.928   9.548       3.897       67.13         137.71   14.289   ON
  14:00:00                                                                      

  2026-03-07   13.867   9.377       3.885       64.72         133.62   13.491   ON
  15:00:00                                                                      

  2026-03-07   13.347   9.412       3.836       64            137.38   13.771   ON
  16:00:00                                                                      

  2026-03-07   13.712   9.68        3.889       68.22         139.64   14.292   ON
  17:00:00                                                                      

  2026-03-07   14.106   9.568       3.866       66.51         128.07   13.885   ON
  18:00:00                                                                      

  2026-03-07   13.193   9.544       3.912       63.78         134.06   14.076   ON
  19:00:00                                                                      

  2026-03-07   13.73    9.608       3.698       62.58         135.67   14.058   ON
  20:00:00                                                                      

  2026-03-07   13.903   9.738       3.795       64.68         127.44   13.754   ON
  21:00:00                                                                      

  2026-03-07   13.411   9.317       4.532       66.92         122.8    14.106   ON
  22:00:00                                                                      

  2026-03-07   13.759   9.388       4.084       64.3          136.2    13.653   ON
  23:00:00                                                                      

  2026-03-08   13.309   9.239       3.953       64.75         132.39   13.797   ON
  00:00:00                                                                      

  2026-03-08   13.379   9.574       3.898       64.38         138.08   14.443   ON
  01:00:00                                                                      

  2026-03-08   13.378   9.443       3.618       66.1          134.92   13.834   ON
  02:00:00                                                                      

  2026-03-08   13.652   9.399       3.857       67.21         134.91   13.98    ON
  03:00:00                                                                      

  2026-03-08   13.575   9.386       3.738       63.23         133.57   13.599   ON
  04:00:00                                                                      

  2026-03-08   13.86    9.604       4.037       64.69         135.37   14.236   ON
  05:00:00                                                                      

  2026-03-08   13.344   9.479       3.571       64.82         131.35   13.638   ON
  06:00:00                                                                      

  2026-03-08   13.564   9.42        3.209       64.19         132.91   13.685   ON
  07:00:00                                                                      

  2026-03-08   13.861   9.688       3.66        63.33         138.09   13.722   ON
  08:00:00                                                                      

  2026-03-08   13.753   9.343       3.974       66.36         133.95   13.631   ON
  09:00:00                                                                      

  2026-03-08   13.24    9.31        4.415       65.36         136.97   13.505   ON
  10:00:00                                                                      

  2026-03-08   13.781   9.889       4.056       66.21         134.92   13.803   ON
  11:00:00                                                                      

  2026-03-08   13.47    9.445       3.555       67.4          133.61   13.751   ON
  12:00:00                                                                      

  2026-03-08   13.705   9.418       3.745       64.58         131.11   13.852   ON
  13:00:00                                                                      

  2026-03-08   13.682   9.391       3.562       65.94         138.31   13.619   ON
  14:00:00                                                                      

  2026-03-08   13.932   9.479       3.753       64.52         131.66   13.64    ON
  15:00:00                                                                      

  2026-03-08   13.632   9.617       3.576       64.99         136.45   13.794   ON
  16:00:00                                                                      

  2026-03-08   13.096   9.613       3.389       65.63         128.77   13.877   ON
  17:00:00                                                                      

  2026-03-08   13.227   9.582       3.911       64.88         136.04   13.632   ON
  18:00:00                                                                      

  2026-03-08   13.799   9.458       3.849       62.86         136.49   13.868   ON
  19:00:00                                                                      

  2026-03-08   13.53    9.276       3.757       67.39         132.42   13.815   ON
  20:00:00                                                                      

  2026-03-08   13.91    9.542       3.887       65.36         128.52   14.155   ON
  21:00:00                                                                      

  2026-03-08   13.674   9.728       4.308       63.41         134.33   14.044   ON
  22:00:00                                                                      

  2026-03-08   13.396   9.66        3.829       61.82         135.37   14.009   ON
  23:00:00                                                                      

  2026-03-09   13.894   9.475       3.705       65.09         132.88   14.143   ON
  00:00:00                                                                      

  2026-03-09   13.38    9.62        4.017       66.11         132.26   13.709   ON
  01:00:00                                                                      

  2026-03-09   13.042   9.442       3.39        66.65         138.57   14.233   ON
  02:00:00                                                                      

  2026-03-09   14.161   9.492       3.988       66.81         134.51   13.925   ON
  03:00:00                                                                      

  2026-03-09   13.08    9.315       3.606       64.56         133.3    13.746   ON
  04:00:00                                                                      

  2026-03-09   13.773   9.453       3.596       66.1          138.32   13.982   ON
  05:00:00                                                                      

  2026-03-09   13.855   9.521       3.827       62.82         134.88   13.593   ON
  06:00:00                                                                      

  2026-03-09   13.64    9.475       4.218       65.36         132.18   14.345   ON
  07:00:00                                                                      

  2026-03-09   13.142   9.615       3.614       66.51         138.42   13.943   ON
  08:00:00                                                                      

  2026-03-09   13.876   9.783       4.038       64.22         133.52   13.482   ON
  09:00:00                                                                      

  2026-03-09   13.208   9.698       3.894       64.89         138.63   13.579   ON
  10:00:00                                                                      

  2026-03-09   13.235   9.454       3.452       65.29         132.28   13.742   ON
  11:00:00                                                                      

  2026-03-09   13.502   9.39        4.029       65.34         136.24   13.728   ON
  12:00:00                                                                      

  2026-03-09   13.814   9.402       3.593       67.37         139.86   13.995   ON
  13:00:00                                                                      

  2026-03-09   13.682   9.353       3.432       63.51         136.77   14.108   ON
  14:00:00                                                                      

  2026-03-09   13.821   9.505       3.602       67.15         136.95   14.144   ON
  15:00:00                                                                      

  2026-03-09   13.479   9.563       3.618       63.26         136.74   14.019   ON
  16:00:00                                                                      

  2026-03-09   13.553   9.527       3.948       64.13         138.36   13.629   ON
  17:00:00                                                                      

  2026-03-09   13.291   9.529       3.617       63.97         135.29   14.171   ON
  18:00:00                                                                      

  2026-03-09   13.514   9.524       4.173       65            136.74   14.199   ON
  19:00:00                                                                      

  2026-03-09   13.761   9.48        3.855       64.39         134.06   13.364   ON
  20:00:00                                                                      

  2026-03-09   13.518   9.389       3.62        65.86         142.62   13.725   ON
  21:00:00                                                                      

  2026-03-09   13.729   9.759       3.591       65.15         131.49   13.782   ON
  22:00:00                                                                      

  2026-03-09   13.444   9.657       3.857       68.44         138.23   13.67    ON
  23:00:00                                                                      

  2026-03-10   13.439   9.364       3.293       65.71         131.08   14.149   ON
  00:00:00                                                                      

  2026-03-10   13.611   9.364       3.256       64.75         137.1    13.996   ON
  01:00:00                                                                      

  2026-03-10   13.547   9.412       3.579       65.7          140.17   13.89    ON
  02:00:00                                                                      

  2026-03-10   13.761   9.486       3.996       66.03         130.64   13.552   ON
  03:00:00                                                                      

  2026-03-10   13.648   9.645       3.936       64.85         141.92   13.332   ON
  04:00:00                                                                      

  2026-03-10   14.073   9.583       3.949       63.46         131.16   13.628   ON
  05:00:00                                                                      

  2026-03-10   13.54    9.566       3.942       63.92         131.72   13.654   ON
  06:00:00                                                                      

  2026-03-10   13.538   9.544       3.503       65.4          136.24   13.635   ON
  07:00:00                                                                      

  2026-03-10   13.317   9.522       4.018       66.39         130.62   13.313   ON
  08:00:00                                                                      

  2026-03-10   13.606   9.442       3.708       65.86         138.84   13.468   ON
  09:00:00                                                                      

  2026-03-10   13.786   9.374       4.412       65            136.91   13.758   ON
  10:00:00                                                                      

  2026-03-10   13.399   9.263       4.254       65.98         124.2    13.959   ON
  11:00:00                                                                      

  2026-03-10   13.586   8.995       4.285       64.4          129.32   13.731   ON
  12:00:00                                                                      

  2026-03-10   13.795   9.212       4.46        65.52         132.1    13.809   ON
  13:00:00                                                                      

  2026-03-10   13.565   9.477       4.493       67.27         136.61   13.85    ON
  14:00:00                                                                      

  2026-03-10   13.459   9.1         4.522       66.81         130.72   13.852   ON
  15:00:00                                                                      

  2026-03-10   13.865   9.062       4.603       67.17         132.1    14.187   ON
  16:00:00                                                                      

  2026-03-10   13.626   9.284       4.421       64.58         137.4    13.659   ON
  17:00:00                                                                      

  2026-03-10   13.708   9.118       4.286       65.44         131.02   13.923   ON
  18:00:00                                                                      

  2026-03-10   13.919   9.009       4.758       63.62         136.12   13.52    ON
  19:00:00                                                                      

  2026-03-10   13.912   9.29        5.086       66.51         129.55   14.18    ON
  20:00:00                                                                      

  2026-03-10   13.506   9.125       5.029       64.49         138.9    14.062   ON
  21:00:00                                                                      

  2026-03-10   13.457   9.12        4.775       63.15         140.55   14.131   ON
  22:00:00                                                                      

  2026-03-10   13.677   8.897       5.034       64.38         130.4    13.899   ON
  23:00:00                                                                      

  2026-03-11   13.564   9.031       4.823       65.51         125.6    13.837   ON
  00:00:00                                                                      

  2026-03-11   13.083   8.988       5.081       61.82         128.29   13.531   ON
  01:00:00                                                                      

  2026-03-11   13.947   9.023       4.885       63            138.72   13.953   ON
  02:00:00                                                                      

  2026-03-11   13.605   9.054       5.124       66.61         132.66   14.23    ON
  03:00:00                                                                      

  2026-03-11   13.8     9.025       5.642       65.27         139.06   13.138   ON
  04:00:00                                                                      

  2026-03-11   13.281   8.857       5.386       65.06         129.63   14.333   ON
  05:00:00                                                                      

  2026-03-11   13.95    8.91        5.62        62.71         131.19   13.653   ON
  06:00:00                                                                      

  2026-03-11   13.44    8.609       5.104       67.51         134.43   13.997   ON
  07:00:00                                                                      

  2026-03-11   13.571   8.853       5.178       66.67         139.12   13.655   ON
  08:00:00                                                                      

  2026-03-11   13.219   8.834       5.392       66.18         134.04   13.83    ON
  09:00:00                                                                      

  2026-03-11   13.555   8.648       5.593       63.46         130.83   14.087   ON
  10:00:00                                                                      

  2026-03-11   13.537   8.565       5.454       66            136.08   13.822   ON
  11:00:00                                                                      

  2026-03-11   13.55    8.647       5.811       66.84         135.23   14.349   ON
  12:00:00                                                                      

  2026-03-11   13.719   8.449       5.472       64.64         136.87   13.881   ON
  13:00:00                                                                      

  2026-03-11   13.616   8.657       6.002       64.75         134.19   14.043   ON
  14:00:00                                                                      

  2026-03-11   13.865   8.625       5.956       64.42         132.43   13.708   ON
  15:00:00                                                                      

  2026-03-11   13.473   8.414       5.487       66.03         134.97   13.738   ON
  16:00:00                                                                      

  2026-03-11   13.329   8.538       5.964       64.77         125.11   13.766   ON
  17:00:00                                                                      

  2026-03-11   13.595   8.666       5.814       64.65         135.94   14.004   ON
  18:00:00                                                                      

  2026-03-11   13.771   8.641       6.177       62.94         139.74   14.312   ON
  19:00:00                                                                      

  2026-03-11   13.939   8.608       5.84        62.63         137.07   13.88    ON
  20:00:00                                                                      

  2026-03-11   13.821   8.409       6.104       66.53         131.13   13.531   ON
  21:00:00                                                                      

  2026-03-11   13.12    8.356       6.215       67.49         128.84   13.709   ON
  22:00:00                                                                      

  2026-03-11   13.703   8.323       5.442       66.42         140.08   13.508   ON
  23:00:00                                                                      

  2026-03-12   13.997   8.445       5.713       67.25         132.88   14       ON
  00:00:00                                                                      

  2026-03-12   13.617   8.684       6.267       64.31         134.06   13.879   ON
  01:00:00                                                                      

  2026-03-12   13.46    8.517       6.255       65.05         135.77   13.587   ON
  02:00:00                                                                      

  2026-03-12   0        0.24        0.247       45.51         2.55     0.131    OFF
  03:00:00                                                                      

  2026-03-12   0        0.309       0.309       40.07         4.48     0        OFF
  04:00:00                                                                      

  2026-03-12   0.099    0.309       0.326       37.68         5.62     0.112    OFF
  05:00:00                                                                      

  2026-03-12   0.052    0.336       0.342       42.71         5.07     0        OFF
  06:00:00                                                                      

  2026-03-12   0.026    0.281       0.276       39.1          5.5      0        OFF
  07:00:00                                                                      

  2026-03-12   0        0.323       0.301       38.4          4.48     0        OFF
  08:00:00                                                                      

  2026-03-12   0        0.346       0.337       40.49         4.43     0.073    OFF
  09:00:00                                                                      

  2026-03-12   0        0.197       0.333       37.67         4.88     0.112    OFF
  10:00:00                                                                      

  2026-03-12   0.077    0.36        0.332       39.79         4.75     0        OFF
  11:00:00                                                                      

  2026-03-12   0.116    0.349       0.308       39.42         5.68     0.036    OFF
  12:00:00                                                                      

  2026-03-12   0.019    0.344       0.292       41.38         5.52     0.096    OFF
  13:00:00                                                                      

  2026-03-12   0        0.197       0.292       37.15         4.3      0        OFF
  14:00:00                                                                      

  2026-03-12   0        0.325       0.359       41.3          6.09     0.093    OFF
  15:00:00                                                                      

  2026-03-12   0.04     0.365       0.292       42.1          3.49     0.031    OFF
  16:00:00                                                                      

  2026-03-12   0.043    0.284       0.293       37.79         5.86     0.009    OFF
  17:00:00                                                                      

  2026-03-12   0.059    0.31        0.173       40.94         3.4      0        OFF
  18:00:00                                                                      

  2026-03-12   0.084    0.275       0.31        40.16         5.58     0        OFF
  19:00:00                                                                      

  2026-03-12   0        0.356       0.319       35.44         5.98     0        OFF
  20:00:00                                                                      

  2026-03-12   13.576   9.732       3.844       64.37         135.2    13.994   ON
  21:00:00                                                                      

  2026-03-12   13.728   9.4         3.882       64.05         137.21   13.485   ON
  22:00:00                                                                      

  2026-03-12   13.3     9.377       3.652       66.05         142.51   13.993   ON
  23:00:00                                                                      

  2026-03-13   13.235   9.564       3.782       64.35         134.61   14.22    ON
  00:00:00                                                                      

  2026-03-13   13.841   9.345       4.104       66.53         129.93   14.11    ON
  01:00:00                                                                      

  2026-03-13   13.734   9.39        3.794       66.33         132.66   13.928   ON
  02:00:00                                                                      

  2026-03-13   13.592   9.483       3.876       64.47         136.92   13.388   ON
  03:00:00                                                                      

  2026-03-13   13.949   9.524       3.293       65.69         134.11   14.029   ON
  04:00:00                                                                      

  2026-03-13   13.341   9.313       3.929       65.26         132.28   14.048   ON
  05:00:00                                                                      

  2026-03-13   13.486   9.443       3.864       64.94         137.78   14.26    ON
  06:00:00                                                                      

  2026-03-13   13.879   9.587       4.122       66.84         137.82   13.619   ON
  07:00:00                                                                      

  2026-03-13   14.1     9.701       3.112       65.21         134.1    13.81    ON
  08:00:00                                                                      

  2026-03-13   13.602   9.206       3.805       65.5          136.03   13.731   ON
  09:00:00                                                                      

  2026-03-13   14.057   9.696       3.768       62.24         132.39   13.8     ON
  10:00:00                                                                      

  2026-03-13   13.436   9.632       3.819       66.04         132.5    13.414   ON
  11:00:00                                                                      

  2026-03-13   13.69    9.338       3.64        62.99         133.55   13.747   ON
  12:00:00                                                                      

  2026-03-13   13.553   9.28        3.85        64.57         129.52   13.757   ON
  13:00:00                                                                      

  2026-03-13   13.168   9.562       3.972       67.56         136.23   13.771   ON
  14:00:00                                                                      

  2026-03-13   13.67    9.437       3.808       67.83         134.57   14.294   ON
  15:00:00                                                                      

  2026-03-13   13.854   9.52        3.723       64.57         132.88   13.703   ON
  16:00:00                                                                      

  2026-03-13   13.56    9.629       3.743       63.27         135.29   13.752   ON
  17:00:00                                                                      

  2026-03-13   13.581   9.444       3.699       65.75         135.39   14.168   ON
  18:00:00                                                                      

  2026-03-13   13.979   9.524       3.806       64.56         131.92   13.72    ON
  19:00:00                                                                      

  2026-03-13   13.26    9.571       3.616       65.66         132.51   14.188   ON
  20:00:00                                                                      

  2026-03-13   13.193   9.633       3.297       63.14         131.71   13.989   ON
  21:00:00                                                                      

  2026-03-13   13.422   9.763       4.134       66.83         140.16   13.702   ON
  22:00:00                                                                      

  2026-03-13   13.275   9.754       3.355       67.48         128.19   13.681   ON
  23:00:00                                                                      

  2026-03-14   13.966   9.536       3.765       62.99         134.49   13.906   ON
  00:00:00                                                                      

  2026-03-14   13.684   9.465       3.468       64            138.09   13.817   ON
  01:00:00                                                                      

  2026-03-14   13.365   9.855       3.722       64.11         130.51   13.894   ON
  02:00:00                                                                      

  2026-03-14   13.433   9.596       3.552       66.25         130.98   13.716   ON
  03:00:00                                                                      

  2026-03-14   14.378   9.564       3.783       62.21         130.89   14.025   ON
  04:00:00                                                                      

  2026-03-14   13.434   9.336       3.583       65.47         127.62   13.69    ON
  05:00:00                                                                      

  2026-03-14   13.393   9.616       3.469       64.81         139.36   13.743   ON
  06:00:00                                                                      

  2026-03-14   13.683   9.384       3.87        63.97         133.7    13.82    ON
  07:00:00                                                                      

  2026-03-14   13.774   9.432       4.126       66.21         130.23   13.534   ON
  08:00:00                                                                      

  2026-03-14   13.66    9.301       3.879       62.24         132.05   13.783   ON
  09:00:00                                                                      

  2026-03-14   13.353   9.423       3.819       63.11         135.21   13.813   ON
  10:00:00                                                                      

  2026-03-14   13.285   9.509       3.529       63.99         133.2    13.483   ON
  11:00:00                                                                      

  2026-03-14   13.762   9.276       3.771       66.22         130.94   13.391   ON
  12:00:00                                                                      

  2026-03-14   13.585   9.366       3.903       64.64         136.46   14.197   ON
  13:00:00                                                                      

  2026-03-14   13.154   9.488       3.628       63.92         130.94   13.796   ON
  14:00:00                                                                      

  2026-03-14   13.919   9.312       4.016       65.88         132.87   13.829   ON
  15:00:00                                                                      

  2026-03-14   13.811   9.313       3.78        64.44         135.1    13.698   ON
  16:00:00                                                                      

  2026-03-14   13.534   9.376       3.879       64.2          131.55   14.286   ON
  17:00:00                                                                      

  2026-03-14   13.529   9.29        3.666       64.71         134.71   13.812   ON
  18:00:00                                                                      

  2026-03-14   13.663   9.592       3.668       65.67         131.87   13.392   ON
  19:00:00                                                                      

  2026-03-14   13.413   9.352       3.845       69.21         144.92   13.997   ON
  20:00:00                                                                      

  2026-03-14   13.233   9.615       3.886       63.54         132.77   13.607   ON
  21:00:00                                                                      

  2026-03-14   13.688   9.638       3.876       65.58         137.09   13.982   ON
  22:00:00                                                                      

  2026-03-14   13.209   9.321       3.535       64.94         130.98   13.831   ON
  23:00:00                                                                      

  2026-03-15   13.706   9.506       3.606       64.78         129.94   14.205   ON
  00:00:00                                                                      

  2026-03-15   13.208   9.429       3.784       67.45         133.86   13.994   ON
  01:00:00                                                                      

  2026-03-15   13.573   9.33        3.324       66.34         132.98   13.767   ON
  02:00:00                                                                      

  2026-03-15   13.563   9.45        4.05        66.18         132.99   14.247   ON
  03:00:00                                                                      

  2026-03-15   14.085   9.464       3.867       64.5          134.2    14.595   ON
  04:00:00                                                                      

  2026-03-15   13.31    9.606       3.798       63.91         137.82   13.727   ON
  05:00:00                                                                      

  2026-03-15   13.215   9.653       3.61        65.62         141.88   14.159   ON
  06:00:00                                                                      

  2026-03-15   13.424   9.336       3.993       64.76         142.29   13.97    ON
  07:00:00                                                                      

  2026-03-15   13.294   9.439       3.72        64.33         134.54   13.99    ON
  08:00:00                                                                      

  2026-03-15   13.44    9.579       4.263       66.19         141.53   13.54    ON
  09:00:00                                                                      

  2026-03-15   13.714   9.676       3.886       63.38         141.01   13.61    ON
  10:00:00                                                                      

  2026-03-15   13.81    9.135       3.415       64.1          131.79   14.249   ON
  11:00:00                                                                      

  2026-03-15   14.051   9.691       3.969       66.37         132.34   13.911   ON
  12:00:00                                                                      

  2026-03-15   13.4     9.475       3.655       65.07         133.84   13.729   ON
  13:00:00                                                                      

  2026-03-15   14.318   9.729       3.657       66.19         141.98   14.352   ON
  14:00:00                                                                      

  2026-03-15   14.139   9.437       3.727       63.92         133.65   14.198   ON
  15:00:00                                                                      

  2026-03-15   13.545   9.376       3.754       66.25         133.24   14.068   ON
  16:00:00                                                                      

  2026-03-15   12.977   9.507       3.85        64.13         139.67   13.611   ON
  17:00:00                                                                      

  2026-03-15   13.577   9.675       3.977       67.23         133.46   13.869   ON
  18:00:00                                                                      

  2026-03-15   13.62    9.505       3.9         66.39         133.56   14.266   ON
  19:00:00                                                                      

  2026-03-15   12.975   9.147       3.605       65.9          136.52   13.329   ON
  20:00:00                                                                      

  2026-03-15   13.62    9.602       3.449       67.51         134.84   13.448   ON
  21:00:00                                                                      

  2026-03-15   13.546   9.259       3.585       65.73         124.58   13.659   ON
  22:00:00                                                                      

  2026-03-15   13.386   9.354       3.876       64.26         129.19   14.133   ON
  23:00:00                                                                      

  2026-03-16   13.77    9.326       4.003       67.54         136.91   13.934   ON
  00:00:00                                                                      

  2026-03-16   13.873   9.225       4.236       65.73         128.44   13.999   ON
  01:00:00                                                                      

  2026-03-16   13.468   9.312       3.449       67.04         138.96   13.925   ON
  02:00:00                                                                      

  2026-03-16   13.662   9.352       3.806       65.44         133.82   13.901   ON
  03:00:00                                                                      

  2026-03-16   13.422   9.408       3.728       66.96         135.1    14.196   ON
  04:00:00                                                                      

  2026-03-16   13.386   9.492       3.685       63.92         135.21   14.84    ON
  05:00:00                                                                      

  2026-03-16   13.622   9.45        3.82        63.32         126.99   13.999   ON
  06:00:00                                                                      

  2026-03-16   13.742   9.278       3.723       63.11         131.27   14.225   ON
  07:00:00                                                                      

  2026-03-16   13.447   9.473       3.719       66.36         129.93   13.756   ON
  08:00:00                                                                      

  2026-03-16   12.998   9.646       3.624       62.28         135.04   14.304   ON
  09:00:00                                                                      

  2026-03-16   13.759   9.642       3.884       62.55         140.13   13.9     ON
  10:00:00                                                                      

  2026-03-16   13.166   9.52        4.049       63.1          133.2    13.923   ON
  11:00:00                                                                      

  2026-03-16   13.633   9.593       4.194       65.57         134.38   13.751   ON
  12:00:00                                                                      

  2026-03-16   14.084   9.634       3.654       65.88         126.37   13.67    ON
  13:00:00                                                                      

  2026-03-16   13.595   9.704       3.522       64.01         132.62   13.729   ON
  14:00:00                                                                      

  2026-03-16   13.276   9.754       3.72        66.41         133.14   13.613   ON
  15:00:00                                                                      

  2026-03-16   13.203   9.452       3.576       65.71         133.36   13.528   ON
  16:00:00                                                                      

  2026-03-16   13.918   9.459       4.043       67.04         136.47   14.371   ON
  17:00:00                                                                      

  2026-03-16   13.595   9.721       3.58        66.65         139.66   13.995   ON
  18:00:00                                                                      

  2026-03-16   13.747   9.734       3.804       64.2          134.05   14.141   ON
  19:00:00                                                                      

  2026-03-16   13.852   9.731       3.449       65.53         135.67   14.012   ON
  20:00:00                                                                      

  2026-03-16   13.587   9.148       3.698       64.99         127.94   13.492   ON
  21:00:00                                                                      

  2026-03-16   13.516   9.467       3.833       65.93         136.52   13.885   ON
  22:00:00                                                                      

  2026-03-16   13.342   9.012       4.168       65.54         134.25   13.636   ON
  23:00:00                                                                      

  2026-03-17   12.762   9.609       3.612       65.28         127.2    13.659   ON
  00:00:00                                                                      

  2026-03-17   13.187   9.508       3.878       66.31         135.46   13.845   ON
  01:00:00                                                                      

  2026-03-17   13.581   9.508       3.266       65.33         131.52   13.92    ON
  02:00:00                                                                      

  2026-03-17   13.552   9.479       3.483       66.34         138.13   13.901   ON
  03:00:00                                                                      

  2026-03-17   13.71    9.696       3.581       65.29         135.95   13.91    ON
  04:00:00                                                                      

  2026-03-17   13.566   9.456       3.66        65.01         134.46   13.798   ON
  05:00:00                                                                      

  2026-03-17   13.643   9.655       3.893       66.62         140.93   13.884   ON
  06:00:00                                                                      

  2026-03-17   13.814   9.583       3.943       66.67         133.5    14.213   ON
  07:00:00                                                                      

  2026-03-17   13.359   9.554       3.383       67.1          132.92   14.466   ON
  08:00:00                                                                      

  2026-03-17   13.522   9.569       3.917       66.19         134.28   14.178   ON
  09:00:00                                                                      

  2026-03-17   13.163   9.517       3.506       64.93         134.62   13.816   ON
  10:00:00                                                                      

  2026-03-17   13.865   9.336       4.243       65.53         130.79   13.982   ON
  11:00:00                                                                      

  2026-03-17   13.61    9.607       3.863       65.48         136.43   14.135   ON
  12:00:00                                                                      

  2026-03-17   13.733   9.607       3.822       62.61         135.85   14.147   ON
  13:00:00                                                                      

  2026-03-17   14.02    9.478       3.74        63.57         132.11   14.206   ON
  14:00:00                                                                      

  2026-03-17   13.894   9.61        3.776       67.53         128.02   14.211   ON
  15:00:00                                                                      

  2026-03-17   13.584   9.635       3.785       65.16         138.99   13.985   ON
  16:00:00                                                                      

  2026-03-17   13.814   9.308       3.611       60.98         139.45   13.8     ON
  17:00:00                                                                      

  2026-03-17   13.211   9.479       3.971       65.07         137.84   13.459   ON
  18:00:00                                                                      

  2026-03-17   13.718   9.434       3.852       65.49         138.21   14.165   ON
  19:00:00                                                                      

  2026-03-17   13.638   9.364       3.971       63.41         141.46   14.042   ON
  20:00:00                                                                      

  2026-03-17   13.16    9.548       3.769       68.65         135.71   13.643   ON
  21:00:00                                                                      

  2026-03-17   13.964   9.374       3.954       66.93         140.89   13.879   ON
  22:00:00                                                                      

  2026-03-17   13.408   9.435       3.595       66.46         133.89   13.767   ON
  23:00:00                                                                      

  2026-03-18   13.786   9.537       4.675       64.96         131.06   13.755   ON
  00:00:00                                                                      

  2026-03-18   13.486   9.552       3.606       65.96         134.6    14.346   ON
  01:00:00                                                                      

  2026-03-18   13.87    9.548       3.673       66.5          133.31   13.777   ON
  02:00:00                                                                      

  2026-03-18   13.957   9.835       4.025       65.95         136.53   14.531   ON
  03:00:00                                                                      

  2026-03-18   13.374   9.424       4.092       64.24         141.79   13.837   ON
  04:00:00                                                                      

  2026-03-18   13.184   9.538       3.585       65.52         136.28   13.679   ON
  05:00:00                                                                      

  2026-03-18   13.564   9.319       3.368       65.44         138.78   13.909   ON
  06:00:00                                                                      

  2026-03-18   13.831   9.572       3.434       65.68         143.09   14.526   ON
  07:00:00                                                                      

  2026-03-18   13.499   9.673       3.536       63.68         141.79   13.832   ON
  08:00:00                                                                      

  2026-03-18   13.433   9.682       3.588       65.63         135.03   14.012   ON
  09:00:00                                                                      

  2026-03-18   13.733   9.405       3.743       65.24         132.01   13.26    ON
  10:00:00                                                                      

  2026-03-18   12.849   9.458       4.041       65.58         143.13   14.032   ON
  11:00:00                                                                      

  2026-03-18   13.419   9.689       4.054       65.53         130.43   13.501   ON
  12:00:00                                                                      

  2026-03-18   13.224   9.486       3.631       63.08         127.47   13.841   ON
  13:00:00                                                                      

  2026-03-18   13.68    9.644       3.919       66.51         126.77   14.241   ON
  14:00:00                                                                      

  2026-03-18   13.4     9.354       4.004       66.34         139.37   13.804   ON
  15:00:00                                                                      

  2026-03-18   13.297   9.708       4.135       63.21         128.86   14.067   ON
  16:00:00                                                                      

  2026-03-18   13.504   9.654       3.744       65.08         133.7    13.811   ON
  17:00:00                                                                      

  2026-03-18   13.201   9.57        3.598       63.95         134.2    13.781   ON
  18:00:00                                                                      

  2026-03-18   13.596   9.38        3.971       64.54         139.91   13.947   ON
  19:00:00                                                                      

  2026-03-18   13.414   9.476       4.162       66.71         129.26   14.167   ON
  20:00:00                                                                      

  2026-03-18   13.497   9.523       3.652       66            134.93   13.898   ON
  21:00:00                                                                      

  2026-03-18   13.405   9.54        4.27        68.17         135.93   13.867   ON
  22:00:00                                                                      

  2026-03-18   13.848   9.484       4.213       65.34         140.34   13.612   ON
  23:00:00                                                                      

  2026-03-19   13.57    9.467       3.718       63.53         133.78   13.414   ON
  00:00:00                                                                      

  2026-03-19   13.743   9.529       3.391       65.37         135.82   13.906   ON
  01:00:00                                                                      

  2026-03-19   13.731   9.709       3.634       61.54         133.63   13.822   ON
  02:00:00                                                                      

  2026-03-19   13.381   9.199       3.695       67.85         139.1    13.944   ON
  03:00:00                                                                      

  2026-03-19   13.755   9.294       3.916       65.58         138.51   14.153   ON
  04:00:00                                                                      

  2026-03-19   13.695   9.268       3.366       65.85         133.21   14.094   ON
  05:00:00                                                                      

  2026-03-19   13.685   9.397       4.391       65.4          136.94   13.633   ON
  06:00:00                                                                      

  2026-03-19   13.492   9.239       4.368       63.9          128.86   13.94    ON
  07:00:00                                                                      

  2026-03-19   13.484   9.583       3.602       64.99         135.04   13.947   ON
  08:00:00                                                                      

  2026-03-19   13.814   9.514       3.318       63.99         131.24   13.804   ON
  09:00:00                                                                      

  2026-03-19   14.193   9.462       3.741       64.4          133.12   13.26    ON
  10:00:00                                                                      

  2026-03-19   13.374   9.398       3.889       65.65         138.8    13.653   ON
  11:00:00                                                                      

  2026-03-19   13.745   9.524       4.119       63.35         143.36   13.844   ON
  12:00:00                                                                      

  2026-03-19   13.5     9.527       3.961       67.6          135.62   14.075   ON
  13:00:00                                                                      

  2026-03-19   13.813   9.55        3.732       63.54         134.25   13.785   ON
  14:00:00                                                                      

  2026-03-19   13.719   9.391       3.291       66.37         133.48   13.491   ON
  15:00:00                                                                      

  2026-03-19   13.888   9.597       3.91        64.17         137.81   14.239   ON
  16:00:00                                                                      

  2026-03-19   12.84    9.28        3.993       63.26         134.1    13.858   ON
  17:00:00                                                                      

  2026-03-19   13.437   9.687       3.705       65.69         138.73   13.744   ON
  18:00:00                                                                      

  2026-03-19   13.331   9.038       3.851       65.36         140.96   14.012   ON
  19:00:00                                                                      

  2026-03-19   13.571   9.411       3.833       64.76         137.33   14.056   ON
  20:00:00                                                                      

  2026-03-19   13.403   9.32        3.721       65.01         133.29   13.846   ON
  21:00:00                                                                      

  2026-03-19   13.426   9.618       3.493       64.16         137.88   13.709   ON
  22:00:00                                                                      

  2026-03-19   13.785   9.277       3.868       65.72         132.08   13.713   ON
  23:00:00                                                                      

  2026-03-20   14.117   9.773       3.428       64.36         127.82   14.083   ON
  00:00:00                                                                      

  2026-03-20   12.832   9.268       4.133       65.1          139.4    13.829   ON
  01:00:00                                                                      

  2026-03-20   13.516   9.804       3.557       66.73         142.5    14.001   ON
  02:00:00                                                                      

  2026-03-20   13.685   9.567       3.905       63.09         140.13   13.348   ON
  03:00:00                                                                      

  2026-03-20   13.601   9.505       3.599       64.21         133.41   13.732   ON
  04:00:00                                                                      

  2026-03-20   13.506   9.565       3.877       64.05         121.34   13.762   ON
  05:00:00                                                                      

  2026-03-20   13.232   9.829       3.729       63.86         131.91   13.737   ON
  06:00:00                                                                      

  2026-03-20   13.344   9.634       3.915       63.03         137.31   13.337   ON
  07:00:00                                                                      

  2026-03-20   13.797   9.165       3.584       64.63         133.25   13.744   ON
  08:00:00                                                                      

  2026-03-20   13.893   9.679       3.374       65.26         140.37   14.292   ON
  09:00:00                                                                      

  2026-03-20   13.626   9.535       3.711       64.87         131.57   13.947   ON
  10:00:00                                                                      

  2026-03-20   13.373   9.257       3.694       62.65         136.79   13.722   ON
  11:00:00                                                                      

  2026-03-20   13.626   9.614       3.406       66.04         135.7    13.669   ON
  12:00:00                                                                      

  2026-03-20   13.535   9.318       3.609       66.08         135.83   13.496   ON
  13:00:00                                                                      

  2026-03-20   13.748   9.527       3.363       65.13         129.18   13.926   ON
  14:00:00                                                                      

  2026-03-20   13.632   9.535       3.81        63.53         134.38   13.651   ON
  15:00:00                                                                      

  2026-03-20   13.431   9.403       3.688       63.74         135.84   13.756   ON
  16:00:00                                                                      

  2026-03-20   13.652   9.597       3.785       67.92         133.18   14.105   ON
  17:00:00                                                                      

  2026-03-20   13.279   9.347       4.432       67.58         129.54   14.12    ON
  18:00:00                                                                      

  2026-03-20   13.823   9.529       3.821       65.72         132.82   14.031   ON
  19:00:00                                                                      

  2026-03-20   13.922   9.418       3.875       63.65         130.94   13.413   ON
  20:00:00                                                                      

  2026-03-20   13.279   9.473       3.938       66.89         136.15   13.709   ON
  21:00:00                                                                      

  2026-03-20   13.715   9.788       3.747       65.27         138.63   14.183   ON
  22:00:00                                                                      

  2026-03-20   13.33    9.517       3.634       67.51         136.07   13.541   ON
  23:00:00                                                                      

  2026-03-21   13.891   9.337       4.001       64.15         136.23   14.203   ON
  00:00:00                                                                      

  2026-03-21   13.846   9.482       4.039       65.71         134.03   13.855   ON
  01:00:00                                                                      

  2026-03-21   13.537   9.385       3.052       64.69         135.52   14.12    ON
  02:00:00                                                                      

  2026-03-21   13.871   9.504       3.741       66.13         126.94   13.749   ON
  03:00:00                                                                      

  2026-03-21   13.483   9.524       3.696       64.06         135.04   13.545   ON
  04:00:00                                                                      

  2026-03-21   13.425   9.513       3.64        66.37         138.29   13.586   ON
  05:00:00                                                                      

  2026-03-21   13.445   9.513       4.092       64.43         132.62   14.257   ON
  06:00:00                                                                      

  2026-03-21   13.562   9.418       3.647       63.68         137.51   13.774   ON
  07:00:00                                                                      

  2026-03-21   13.512   9.567       3.997       65.85         128.7    13.529   ON
  08:00:00                                                                      

  2026-03-21   13.642   9.659       3.645       65.35         134.91   14.083   ON
  09:00:00                                                                      

  2026-03-21   13.433   9.407       3.679       61.85         133.97   13.441   ON
  10:00:00                                                                      

  2026-03-21   13.808   9.491       3.963       64.94         136.58   13.817   ON
  11:00:00                                                                      

  2026-03-21   13.878   9.509       3.596       65.16         135.3    13.953   ON
  12:00:00                                                                      

  2026-03-21   13.465   9.688       3.74        65.28         143.63   13.941   ON
  13:00:00                                                                      

  2026-03-21   13.212   9.662       3.505       68.06         121.96   13.976   ON
  14:00:00                                                                      

  2026-03-21   13.797   9.39        3.559       64.04         128.9    13.836   ON
  15:00:00                                                                      

  2026-03-21   13.91    9.511       3.961       64.98         132      13.192   ON
  16:00:00                                                                      

  2026-03-21   13.556   9.276       3.927       62.47         135.09   13.927   ON
  17:00:00                                                                      

  2026-03-21   13.25    9.355       3.495       62.83         132.11   13.848   ON
  18:00:00                                                                      

  2026-03-21   13.673   9.502       3.485       64.15         131.99   13.806   ON
  19:00:00                                                                      

  2026-03-21   14.015   9.594       4.417       64.81         128.38   13.994   ON
  20:00:00                                                                      

  2026-03-21   13.09    9.643       3.62        64.71         129.25   14.069   ON
  21:00:00                                                                      

  2026-03-21   13.73    9.453       3.563       65.95         131.2    13.918   ON
  22:00:00                                                                      

  2026-03-21   13.515   9.297       3.908       66.09         140.79   14.268   ON
  23:00:00                                                                      

  2026-03-22   13.367   9.56        3.586       66.51         131.44   14.457   ON
  00:00:00                                                                      

  2026-03-22   13.736   9.474       3.689       64.76         145.76   13.938   ON
  01:00:00                                                                      

  2026-03-22   13.247   9.564       4.003       65.73         138.97   13.765   ON
  02:00:00                                                                      

  2026-03-22   13.681   9.524       4.03        63.93         133.54   13.508   ON
  03:00:00                                                                      

  2026-03-22   13.957   9.607       3.731       65.54         137.98   14.017   ON
  04:00:00                                                                      

  2026-03-22   13.648   9.598       4.115       65.72         138.81   13.377   ON
  05:00:00                                                                      

  2026-03-22   13.362   9.627       3.744       64.25         129.88   14.318   ON
  06:00:00                                                                      

  2026-03-22   13.116   9.431       3.72        60.19         128.18   14.126   ON
  07:00:00                                                                      

  2026-03-22   13.251   9.649       3.778       64.02         140.6    13.717   ON
  08:00:00                                                                      

  2026-03-22   13.099   9.425       3.703       68.85         130.85   14.045   ON
  09:00:00                                                                      

  2026-03-22   14.035   9.513       3.912       64.85         138.19   13.623   ON
  10:00:00                                                                      

  2026-03-22   13.532   9.779       3.851       64.04         137.44   13.56    ON
  11:00:00                                                                      

  2026-03-22   13.316   9.554       3.586       65.16         127.99   14.068   ON
  12:00:00                                                                      

  2026-03-22   13.247   9.325       3.825       66.66         137.31   13.583   ON
  13:00:00                                                                      

  2026-03-22   13.31    9.724       3.645       65.5          136.97   13.927   ON
  14:00:00                                                                      

  2026-03-22   13.509   9.65        3.636       64.69         139.87   13.825   ON
  15:00:00                                                                      

  2026-03-22   13.251   9.671       3.745       63.08         134.58   14.285   ON
  16:00:00                                                                      

  2026-03-22   14.056   9.53        4.034       64.55         136.54   13.945   ON
  17:00:00                                                                      

  2026-03-22   13.397   9.552       3.849       63.21         136.24   14.289   ON
  18:00:00                                                                      

  2026-03-22   13.387   9.465       4.097       65.52         133.77   14.095   ON
  19:00:00                                                                      

  2026-03-22   13.684   9.395       4.17        67.25         141.3    13.651   ON
  20:00:00                                                                      

  2026-03-22   13.995   9.729       3.771       66.57         138.6    13.542   ON
  21:00:00                                                                      

  2026-03-22   13.96    9.445       3.629       64.11         140.9    13.285   ON
  22:00:00                                                                      

  2026-03-22   13.467   9.428       3.583       63.52         136.15   13.868   ON
  23:00:00                                                                      

  2026-03-23   13.669   9.433       3.85        62.91         139.4    13.102   ON
  00:00:00                                                                      

  2026-03-23   13.641   9.779       3.996       65.66         130.88   13.635   ON
  01:00:00                                                                      

  2026-03-23   13.744   9.632       4.176       65.85         132.22   13.203   ON
  02:00:00                                                                      

  2026-03-23   13.67    9.445       3.453       66.17         138.74   13.689   ON
  03:00:00                                                                      

  2026-03-23   13.343   9.493       4.011       65.5          133.8    14.05    ON
  04:00:00                                                                      

  2026-03-23   13.257   9.577       4.048       63.18         133.12   13.62    ON
  05:00:00                                                                      

  2026-03-23   13.648   9.632       4.39        62.11         135.35   13.707   ON
  06:00:00                                                                      

  2026-03-23   13.278   9.258       3.827       66.66         128.35   13.733   ON
  07:00:00                                                                      

  2026-03-23   13.971   9.636       3.773       63.73         135.38   13.931   ON
  08:00:00                                                                      

  2026-03-23   13.611   9.467       3.401       67.83         136.68   13.455   ON
  09:00:00                                                                      

  2026-03-23   13.321   9.397       3.587       61.83         133.42   13.887   ON
  10:00:00                                                                      

  2026-03-23   13.513   9.441       3.505       63.33         130.19   13.829   ON
  11:00:00                                                                      

  2026-03-23   13.462   9.619       3.529       63.58         141.75   13.576   ON
  12:00:00                                                                      

  2026-03-23   13.564   9.764       3.557       65.38         136.42   13.589   ON
  13:00:00                                                                      

  2026-03-23   13.857   9.522       3.398       65.97         130.59   14.186   ON
  14:00:00                                                                      

  2026-03-23   13.207   9.584       3.759       64.15         132.34   14.053   ON
  15:00:00                                                                      

  2026-03-23   13.092   9.378       3.878       65.87         128.21   13.973   ON
  16:00:00                                                                      

  2026-03-23   13.692   9.574       3.972       63.03         127.71   13.629   ON
  17:00:00                                                                      

  2026-03-23   13.552   9.623       3.758       64.23         127.02   13.762   ON
  18:00:00                                                                      

  2026-03-23   13.644   9.277       4.046       63.16         131.35   13.501   ON
  19:00:00                                                                      

  2026-03-23   13.721   9.423       4.049       64.14         136.4    13.376   ON
  20:00:00                                                                      

  2026-03-23   13.551   9.619       3.403       64.01         137.68   13.727   ON
  21:00:00                                                                      

  2026-03-23   13.818   9.236       3.714       65.43         134.24   13.692   ON
  22:00:00                                                                      

  2026-03-23   13.357   9.444       3.471       70.12         138.81   13.515   ON
  23:00:00                                                                      

  2026-03-24   13.618   9.59        3.538       62.92         136.99   13.522   ON
  00:00:00                                                                      

  2026-03-24   13.374   9.246       3.829       64.67         130.09   13.954   ON
  01:00:00                                                                      

  2026-03-24   13.293   9.441       3.752       65.99         131.32   13.727   ON
  02:00:00                                                                      

  2026-03-24   13.767   9.508       4.149       65.07         135.85   13.424   ON
  03:00:00                                                                      

  2026-03-24   13.755   9.634       4.295       67.09         137.45   14.408   ON
  04:00:00                                                                      

  2026-03-24   13.072   9.308       3.889       63.44         139.07   13.38    ON
  05:00:00                                                                      

  2026-03-24   13.295   9.666       3.736       66.13         129.19   13.911   ON
  06:00:00                                                                      

  2026-03-24   13.679   9.546       3.747       63.79         126.9    13.58    ON
  07:00:00                                                                      

  2026-03-24   13.891   9.68        3.781       66.19         142.83   14.037   ON
  08:00:00                                                                      

  2026-03-24   13.419   9.674       3.927       65.22         133.6    13.872   ON
  09:00:00                                                                      

  2026-03-24   13.55    9.551       3.601       65.34         138.74   14.129   ON
  10:00:00                                                                      

  2026-03-24   13.216   9.573       3.93        64.09         134.88   13.834   ON
  11:00:00                                                                      

  2026-03-24   14.283   9.239       3.724       62.2          129.19   13.647   ON
  12:00:00                                                                      

  2026-03-24   13.729   9.297       4.049       63.31         140.38   14.245   ON
  13:00:00                                                                      

  2026-03-24   13.843   9.349       4.125       66.03         136.64   13.837   ON
  14:00:00                                                                      

  2026-03-24   13.779   9.448       4.219       64.57         140.7    13.795   ON
  15:00:00                                                                      

  2026-03-24   13.854   9.64        3.746       66.07         137.21   13.811   ON
  16:00:00                                                                      

  2026-03-24   13.765   9.232       3.448       62.98         130.81   13.654   ON
  17:00:00                                                                      

  2026-03-24   13.509   9.452       3.364       65.93         134.63   13.948   ON
  18:00:00                                                                      

  2026-03-24   13.802   9.302       3.712       66.48         138.8    14.309   ON
  19:00:00                                                                      

  2026-03-24   13.622   9.266       3.431       61.66         132.02   14.259   ON
  20:00:00                                                                      

  2026-03-24   13.953   9.722       3.374       65.45         135.55   13.933   ON
  21:00:00                                                                      

  2026-03-24   13.4     9.515       3.698       67.88         139.48   14.028   ON
  22:00:00                                                                      

  2026-03-24   13.453   9.745       3.54        63.84         129.84   14.056   ON
  23:00:00                                                                      

  2026-03-25   13.78    9.678       3.959       66.47         133.32   13.679   ON
  00:00:00                                                                      

  2026-03-25   13.948   9.362       4.271       65.03         135.52   14.258   ON
  01:00:00                                                                      

  2026-03-25   13.639   9.222       3.73        66.25         138.67   13.92    ON
  02:00:00                                                                      

  2026-03-25   13.406   9.811       3.865       64.4          134.44   13.358   ON
  03:00:00                                                                      

  2026-03-25   13.568   9.439       3.393       63.81         131.95   14.02    ON
  04:00:00                                                                      

  2026-03-25   13.464   9.328       3.832       64.33         137.09   13.603   ON
  05:00:00                                                                      

  2026-03-25   14.116   9.604       3.612       64.43         132.38   13.934   ON
  06:00:00                                                                      

  2026-03-25   13.844   9.52        3.513       64.09         136.52   14.036   ON
  07:00:00                                                                      

  2026-03-25   13.944   9.399       3.322       63.66         136.28   13.767   ON
  08:00:00                                                                      

  2026-03-25   13.682   9.448       4.188       66.63         134.06   13.926   ON
  09:00:00                                                                      

  2026-03-25   13.449   9.524       3.384       64.11         138.29   14.219   ON
  10:00:00                                                                      

  2026-03-25   13.919   9.511       3.486       63.17         139.59   13.477   ON
  11:00:00                                                                      

  2026-03-25   14.05    9.613       3.79        63.57         129.61   13.339   ON
  12:00:00                                                                      

  2026-03-25   13.758   9.447       3.86        65.71         136.95   13.818   ON
  13:00:00                                                                      

  2026-03-25   13.593   9.449       3.861       61.64         134.2    13.786   ON
  14:00:00                                                                      

  2026-03-25   13.894   9.59        3.816       65.73         133.66   14.416   ON
  15:00:00                                                                      

  2026-03-25   13.499   9.547       3.566       66.05         135.21   14.121   ON
  16:00:00                                                                      

  2026-03-25   13.808   9.664       3.981       66.89         139.6    13.994   ON
  17:00:00                                                                      

  2026-03-25   13.406   9.463       3.837       64.32         134.29   13.823   ON
  18:00:00                                                                      

  2026-03-25   13.336   9.485       3.426       63.75         133.59   13.324   ON
  19:00:00                                                                      

  2026-03-25   13.754   9.327       4.19        65.24         129.86   13.49    ON
  20:00:00                                                                      

  2026-03-25   13.692   9.725       3.704       65.19         134.22   13.761   ON
  21:00:00                                                                      

  2026-03-25   14.118   9.291       4.027       66.95         134.9    13.899   ON
  22:00:00                                                                      

  2026-03-25   13.524   9.53        3.426       65.07         131.08   13.733   ON
  23:00:00                                                                      

  2026-03-26   13.606   9.366       3.492       64.35         133.69   13.879   ON
  00:00:00                                                                      

  2026-03-26   13.29    9.551       3.647       62.99         136.83   14.038   ON
  01:00:00                                                                      

  2026-03-26   13.092   9.612       3.617       64.67         140.49   13.655   ON
  02:00:00                                                                      

  2026-03-26   13.116   9.254       4.043       65.1          133.79   13.732   ON
  03:00:00                                                                      

  2026-03-26   13.726   9.468       3.384       66.76         142.94   13.584   ON
  04:00:00                                                                      

  2026-03-26   13.28    9.236       3.832       65.15         138.95   14.176   ON
  05:00:00                                                                      

  2026-03-26   13.906   9.711       3.537       67.01         138.45   13.297   ON
  06:00:00                                                                      

  2026-03-26   13.987   9.434       3.92        66.85         137.36   14.01    ON
  07:00:00                                                                      

  2026-03-26   13.522   9.264       3.843       63.84         135.4    14.055   ON
  08:00:00                                                                      

  2026-03-26   14.051   9.395       3.653       63.28         132.49   13.294   ON
  09:00:00                                                                      

  2026-03-26   13.662   9.697       4.347       64.04         134.76   13.715   ON
  10:00:00                                                                      

  2026-03-26   13.906   9.723       3.78        64.64         135.28   14.14    ON
  11:00:00                                                                      

  2026-03-26   13.539   9.691       4.065       63.78         135.69   13.6     ON
  12:00:00                                                                      

  2026-03-26   13.861   9.382       3.459       66.04         141.22   13.688   ON
  13:00:00                                                                      

  2026-03-26   13.343   9.477       3.76        66            143.08   13.833   ON
  14:00:00                                                                      

  2026-03-26   13.769   9.745       3.814       66.8          137.24   14.202   ON
  15:00:00                                                                      

  2026-03-26   13.475   9.39        3.826       65.41         139.1    14.013   ON
  16:00:00                                                                      

  2026-03-26   13.564   9.45        3.706       64.34         132.35   13.658   ON
  17:00:00                                                                      

  2026-03-26   13.772   9.357       3.585       65.61         127.17   13.47    ON
  18:00:00                                                                      

  2026-03-26   13.647   9.325       3.018       63.63         134.72   13.433   ON
  19:00:00                                                                      

  2026-03-26   13.58    9.681       3.65        65.22         136.12   13.934   ON
  20:00:00                                                                      

  2026-03-26   13.798   9.595       3.563       63.86         140.75   13.253   ON
  21:00:00                                                                      

  2026-03-26   13.818   9.567       3.728       66.73         144.83   13.685   ON
  22:00:00                                                                      

  2026-03-26   13.223   9.587       4.007       61            136.22   14.003   ON
  23:00:00                                                                      

  2026-03-27   13.752   9.653       4.347       66.27         140.38   13.515   ON
  00:00:00                                                                      

  2026-03-27   13.783   9.727       3.926       66.32         139.62   13.754   ON
  01:00:00                                                                      

  2026-03-27   13.396   9.499       4.047       64.94         136.04   13.811   ON
  02:00:00                                                                      

  2026-03-27   13.705   9.449       3.951       65.5          138.5    14.046   ON
  03:00:00                                                                      

  2026-03-27   13.24    9.346       3.975       65.31         136.73   13.474   ON
  04:00:00                                                                      

  2026-03-27   13.991   9.662       3.941       66.94         141.41   13.86    ON
  05:00:00                                                                      

  2026-03-27   13.535   9.423       3.728       67.48         130.98   13.826   ON
  06:00:00                                                                      

  2026-03-27   13.579   9.276       3.713       65.02         125.93   13.869   ON
  07:00:00                                                                      

  2026-03-27   13.926   9.46        3.877       67.45         135.75   13.412   ON
  08:00:00                                                                      

  2026-03-27   13.561   9.504       4.245       64.04         138.92   13.978   ON
  09:00:00                                                                      

  2026-03-27   13.763   9.625       3.991       65.62         139.43   13.611   ON
  10:00:00                                                                      

  2026-03-27   13.315   9.651       4.198       65.66         132.96   13.81    ON
  11:00:00                                                                      

  2026-03-27   13.445   9.39        3.472       63.11         137.41   13.61    ON
  12:00:00                                                                      

  2026-03-27   13.221   9.38        3.862       65.49         132.62   14.368   ON
  13:00:00                                                                      

  2026-03-27   13.543   9.451       3.896       64            137.97   13.856   ON
  14:00:00                                                                      

  2026-03-27   13.88    9.318       3.927       66.19         132.26   14.423   ON
  15:00:00                                                                      

  2026-03-27   13.661   9.484       3.453       63.67         130.95   13.671   ON
  16:00:00                                                                      

  2026-03-27   13.841   9.569       3.336       62.34         139.01   13.766   ON
  17:00:00                                                                      

  2026-03-27   13.321   9.506       3.266       63.05         130.23   14.243   ON
  18:00:00                                                                      

  2026-03-27   13.36    9.258       3.697       65.03         129.35   13.742   ON
  19:00:00                                                                      

  2026-03-27   13.473   9.321       4.383       65.47         138.42   13.962   ON
  20:00:00                                                                      

  2026-03-27   13.756   9.693       3.852       65.51         135.65   14.156   ON
  21:00:00                                                                      

  2026-03-27   13.697   9.348       3.495       63.86         125.99   13.742   ON
  22:00:00                                                                      

  2026-03-27   13.596   9.611       3.882       66.18         139.98   13.659   ON
  23:00:00                                                                      

  2026-03-28   13.769   9.595       3.722       64.18         130.33   13.775   ON
  00:00:00                                                                      

  2026-03-28   13.559   9.452       3.841       64.67         133.43   14.118   ON
  01:00:00                                                                      

  2026-03-28   13.594   9.35        3.685       66.47         134.8    13.959   ON
  02:00:00                                                                      

  2026-03-28   13.955   9.532       3.475       64.76         143.31   14.194   ON
  03:00:00                                                                      

  2026-03-28   13.441   9.367       3.666       62.18         135.16   13.771   ON
  04:00:00                                                                      

  2026-03-28   13.65    9.474       3.977       66.07         138.87   13.713   ON
  05:00:00                                                                      

  2026-03-28   14.038   9.516       3.875       65            134.7    13.536   ON
  06:00:00                                                                      

  2026-03-28   13.628   9.392       4.105       64.42         137.3    13.762   ON
  07:00:00                                                                      

  2026-03-28   13.792   9.466       3.532       66.93         129.62   13.683   ON
  08:00:00                                                                      

  2026-03-28   13.435   9.454       4.062       64.06         135.26   13.811   ON
  09:00:00                                                                      

  2026-03-28   14.132   9.315       3.816       65.98         132.81   13.587   ON
  10:00:00                                                                      

  2026-03-28   12.988   9.471       3.849       65.2          131.2    13.649   ON
  11:00:00                                                                      

  2026-03-28   13.291   9.404       4.113       68.89         136.45   13.759   ON
  12:00:00                                                                      

  2026-03-28   13.313   9.226       3.769       62.3          139.41   14.106   ON
  13:00:00                                                                      

  2026-03-28   14.041   9.449       3.866       65.29         137.16   13.753   ON
  14:00:00                                                                      

  2026-03-28   13.696   9.458       3.963       65.52         134      13.687   ON
  15:00:00                                                                      

  2026-03-28   13.529   9.409       3.966       66.65         138.19   14.122   ON
  16:00:00                                                                      

  2026-03-28   13.251   9.191       4.007       64.37         130.82   14.209   ON
  17:00:00                                                                      

  2026-03-28   13.699   9.616       4.127       64.05         136.53   13.762   ON
  18:00:00                                                                      

  2026-03-28   13.631   9.603       3.937       67.08         137.34   13.774   ON
  19:00:00                                                                      

  2026-03-28   13.412   9.598       3.696       64.36         134.91   13.351   ON
  20:00:00                                                                      

  2026-03-28   13.194   9.549       4.418       65.42         134.25   13.42    ON
  21:00:00                                                                      

  2026-03-28   13.3     9.311       3.799       64.92         135.74   13.831   ON
  22:00:00                                                                      

  2026-03-28   13.658   9.518       3.901       65.57         133      14.22    ON
  23:00:00                                                                      

  2026-03-29   13.685   9.361       3.621       62.98         134.38   14.345   ON
  00:00:00                                                                      

  2026-03-29   13.62    9.828       3.262       64.18         138.2    14.068   ON
  01:00:00                                                                      

  2026-03-29   13.559   9.422       3.614       64.91         127.58   13.712   ON
  02:00:00                                                                      

  2026-03-29   13.119   9.6         3.824       65.16         140.24   13.984   ON
  03:00:00                                                                      

  2026-03-29   13.613   9.267       3.941       66.64         137.08   13.445   ON
  04:00:00                                                                      

  2026-03-29   13.319   9.323       3.816       65.76         136.11   13.822   ON
  05:00:00                                                                      

  2026-03-29   13.611   9.42        4.007       65.86         131.23   13.523   ON
  06:00:00                                                                      

  2026-03-29   13.726   9.605       4.057       64.91         133.6    13.846   ON
  07:00:00                                                                      

  2026-03-29   13.416   9.582       4.056       66.88         132.87   14.234   ON
  08:00:00                                                                      

  2026-03-29   13.322   9.543       3.81        64.09         137.96   14.436   ON
  09:00:00                                                                      

  2026-03-29   13.87    9.222       3.83        64.85         137.76   13.903   ON
  10:00:00                                                                      

  2026-03-29   13.696   9.67        3.756       62.77         139.84   13.952   ON
  11:00:00                                                                      

  2026-03-29   13.427   9.361       3.591       63.42         135.47   13.395   ON
  12:00:00                                                                      

  2026-03-29   12.784   9.742       4.166       66.27         127.15   13.668   ON
  13:00:00                                                                      

  2026-03-29   13.587   9.78        3.499       64.92         131.36   14.258   ON
  14:00:00                                                                      

  2026-03-29   13.771   9.624       3.792       62.21         133.74   14.161   ON
  15:00:00                                                                      

  2026-03-29   13.905   9.648       3.867       64.93         136.51   14.072   ON
  16:00:00                                                                      

  2026-03-29   13.416   9.311       3.275       64.64         129.2    13.967   ON
  17:00:00                                                                      

  2026-03-29   13.425   9.887       3.996       63.29         134.38   14.293   ON
  18:00:00                                                                      

  2026-03-29   13.48    9.533       3.722       65.49         135.43   13.776   ON
  19:00:00                                                                      

  2026-03-29   13.828   9.65        3.866       64.59         132.78   13.794   ON
  20:00:00                                                                      

  2026-03-29   13.28    9.371       3.727       65            134.4    14.609   ON
  21:00:00                                                                      

  2026-03-29   13.569   9.49        3.427       66.4          144.22   13.612   ON
  22:00:00                                                                      

  2026-03-29   13.348   9.322       3.859       64.07         135.07   13.968   ON
  23:00:00                                                                      

  2026-03-30   13.673   9.464       3.837       66.6          143.02   13.744   ON
  00:00:00                                                                      

  2026-03-30   13.177   9.502       4.06        64.59         136.09   14.253   ON
  01:00:00                                                                      

  2026-03-30   13.702   9.538       3.929       64.6          132.31   13.774   ON
  02:00:00                                                                      

  2026-03-30   13.465   9.709       3.39        66.92         137.33   13.752   ON
  03:00:00                                                                      

  2026-03-30   13.539   9.572       4.086       65.56         133.49   13.761   ON
  04:00:00                                                                      

  2026-03-30   13.743   9.537       4.01        64.38         134.85   14.065   ON
  05:00:00                                                                      

  2026-03-30   13.911   9.506       4.002       64.81         126.17   13.573   ON
  06:00:00                                                                      

  2026-03-30   13.138   9.802       3.932       65.31         136.49   13.443   ON
  07:00:00                                                                      

  2026-03-30   13.873   9.413       3.634       62.81         132.77   13.813   ON
  08:00:00                                                                      

  2026-03-30   13.752   9.678       3.944       65.99         139.59   13.749   ON
  09:00:00                                                                      

  2026-03-30   13.52    9.206       3.72        64.98         135.52   13.992   ON
  10:00:00                                                                      

  2026-03-30   13.982   9.368       4.531       63.05         133.56   13.752   ON
  11:00:00                                                                      

  2026-03-30   13.651   9.562       3.752       63.57         130.9    13.681   ON
  12:00:00                                                                      

  2026-03-30   13.952   9.476       3.533       66.28         135.15   13.924   ON
  13:00:00                                                                      

  2026-03-30   13.439   9.951       3.726       63.09         133.57   13.963   ON
  14:00:00                                                                      

  2026-03-30   13.364   9.887       4.171       68.2          131.96   14.123   ON
  15:00:00                                                                      

  2026-03-30   13.933   9.272       3.668       63.39         142.48   13.864   ON
  16:00:00                                                                      

  2026-03-30   14.189   9.339       3.2         65.29         134.47   13.353   ON
  17:00:00                                                                      

  2026-03-30   13.772   9.479       4.178       61.16         138.59   13.833   ON
  18:00:00                                                                      

  2026-03-30   13.842   9.761       3.893       64.87         140.88   13.848   ON
  19:00:00                                                                      

  2026-03-30   13.471   9.671       3.687       64.2          136.64   13.819   ON
  20:00:00                                                                      

  2026-03-30   13.24    9.549       3.99        65.7          137.53   13.991   ON
  21:00:00                                                                      

  2026-03-30   13.539   9.288       3.58        65.27         137.04   13.769   ON
  22:00:00                                                                      

  2026-03-30   14.008   9.373       3.518       64.47         138.84   14.15    ON
  23:00:00                                                                      
  --------------------------------------------------------------------------------------

### KO3201

Source pages: 34-67.

#### Data dictionary

  Name          Description                    Digital set   Engineering units   Span
  ------------- ------------------------------ ------------- ------------------- ------
  Name          Description                    digitalset    engunits            span
  KO3201_FEED   KO-3201 FEED RATE              T/H           82.5                
  KO3201_DISP   KO-3201 DISCHARGE PRESSURE     BARG          20                  
  KO3201_VIB    KO-3201 VIBRATION              MM/S          20                  
  KO3201_TEMP   KO-3201 BEARING/PROCESS TEMP   DEG C         150                 
  KO3201_AMP    KO-3201 MOTOR AMPERE           A             300                 
  PLANT_RATE    ZCU PRODUCTION RATE            T/H           71.5                
  RUN_STATUS    KO-3201 RUN STATUS             ON_OFF        ON_OFF              1

#### Typical value, zero, and instrument tag

## Typical value Zero Instrument tag --------------- ------

#### Hourly data

  --------------------------------------------------------------------------------------
  Timestamp    Feed     Discharge   Vibration   Temperature   Motor    Plant    Run
                        pressure                              ampere   rate     status
  ------------ -------- ----------- ----------- ------------- -------- -------- --------
  2026-04-01   56.869   9.733       29.125      65.52         142.6    55.7     ON
  00:00:00                                                                      

  2026-04-01   54.96    9.186       28.868      64.5          140.11   55.855   ON
  01:00:00                                                                      

  2026-04-01   55.6     9.451       29.197      64.09         133.38   56.912   ON
  02:00:00                                                                      

  2026-04-01   57.139   9.142       28.626      66.15         129.32   55.22    ON
  03:00:00                                                                      

  2026-04-01   56.462   9.276       28.697      63.81         133.57   54.658   ON
  04:00:00                                                                      

  2026-04-01   54.922   9.427       28.442      63.59         135.32   55.554   ON
  05:00:00                                                                      

  2026-04-01   56.202   9.565       28.79       65.46         134.85   55.123   ON
  06:00:00                                                                      

  2026-04-01   55.681   9.376       28.822      65.34         133.22   56.705   ON
  07:00:00                                                                      

  2026-04-01   54.381   9.529       28.799      63.98         131.2    55.477   ON
  08:00:00                                                                      

  2026-04-01   55.171   9.369       28.476      63.88         139.93   54.379   ON
  09:00:00                                                                      

  2026-04-01   53.078   9.733       29.067      63.93         133.43   56.754   ON
  10:00:00                                                                      

  2026-04-01   53.292   9.405       28.368      65.5          132.01   56.009   ON
  11:00:00                                                                      

  2026-04-01   55.238   9.786       28.562      65.66         135.77   56.287   ON
  12:00:00                                                                      

  2026-04-01   56.583   9.762       28.041      66.22         135.49   56.528   ON
  13:00:00                                                                      

  2026-04-01   53.945   9.356       29.071      64.85         134.87   57.252   ON
  14:00:00                                                                      

  2026-04-01   56.349   9.571       29.007      63.67         139.66   55.086   ON
  15:00:00                                                                      

  2026-04-01   55.193   9.423       28.752      66.07         130.95   56.775   ON
  16:00:00                                                                      

  2026-04-01   57.008   9.711       28.887      68.92         135.98   56.17    ON
  17:00:00                                                                      

  2026-04-01   54.635   9.541       28.481      67.4          138.95   56.154   ON
  18:00:00                                                                      

  2026-04-01   58.29    9.765       28.522      63.5          133.15   55.983   ON
  19:00:00                                                                      

  2026-04-01   55.528   9.465       28.549      66.14         135.53   55.58    ON
  20:00:00                                                                      

  2026-04-01   54.77    9.448       28.883      64.83         137.53   56.325   ON
  21:00:00                                                                      

  2026-04-01   55.311   9.375       28.7        64.86         137.03   56.123   ON
  22:00:00                                                                      

  2026-04-01   53.013   9.512       28.845      64.62         135.04   56.837   ON
  23:00:00                                                                      

  2026-04-02   55.415   9.554       28.525      63.8          130.12   57.721   ON
  00:00:00                                                                      

  2026-04-02   54.681   9.502       28.452      62.77         131.43   55.01    ON
  01:00:00                                                                      

  2026-04-02   55.585   9.537       28.909      65.67         135.05   58.222   ON
  02:00:00                                                                      

  2026-04-02   54.673   9.605       28.875      63.51         133.81   57.28    ON
  03:00:00                                                                      

  2026-04-02   52.033   9.481       28.914      64.21         133.78   54.84    ON
  04:00:00                                                                      

  2026-04-02   52.155   9.396       28.637      64.44         132.89   55.948   ON
  05:00:00                                                                      

  2026-04-02   54.301   9.342       28.87       65.16         128.16   56.089   ON
  06:00:00                                                                      

  2026-04-02   53.624   9.408       28.399      64.37         137.39   57.374   ON
  07:00:00                                                                      

  2026-04-02   55.99    9.442       28.518      64.8          130.84   55.031   ON
  08:00:00                                                                      

  2026-04-02   53.827   9.645       28.884      64.39         141.18   57.966   ON
  09:00:00                                                                      

  2026-04-02   55.508   9.63        28.556      65.4          145.93   54.908   ON
  10:00:00                                                                      

  2026-04-02   54.833   9.384       28.485      65.55         138.11   55.697   ON
  11:00:00                                                                      

  2026-04-02   56.722   9.583       28.558      67.2          136.84   55.421   ON
  12:00:00                                                                      

  2026-04-02   55.114   9.358       29.229      65.86         132.51   54.735   ON
  13:00:00                                                                      

  2026-04-02   55.233   9.618       28.691      64.17         131.15   54.855   ON
  14:00:00                                                                      

  2026-04-02   53.892   9.252       28.88       65.86         133.4    55.448   ON
  15:00:00                                                                      

  2026-04-02   55.424   9.641       28.76       66.39         138.98   55.801   ON
  16:00:00                                                                      

  2026-04-02   55.75    9.467       29.43       64.19         135.14   55.418   ON
  17:00:00                                                                      

  2026-04-02   54.88    9.531       28.777      64.21         128.61   55.077   ON
  18:00:00                                                                      

  2026-04-02   55.793   9.478       29.076      61.69         138.16   53.266   ON
  19:00:00                                                                      

  2026-04-02   53.859   9.337       29.049      67.24         133.04   55.788   ON
  20:00:00                                                                      

  2026-04-02   54.764   9.513       28.917      65.25         138.24   58.151   ON
  21:00:00                                                                      

  2026-04-02   55.456   9.496       28.81       67.04         135.04   57.908   ON
  22:00:00                                                                      

  2026-04-02   54.661   9.608       28.415      62.76         131.91   57.36    ON
  23:00:00                                                                      

  2026-04-03   56.362   9.588       28.954      61.55         133.2    55.661   ON
  00:00:00                                                                      

  2026-04-03   55.716   9.679       29.373      65.49         137.9    56.656   ON
  01:00:00                                                                      

  2026-04-03   54.326   9.578       28.95       63.79         132.76   55.508   ON
  02:00:00                                                                      

  2026-04-03   53.979   9.325       29.338      65.29         140.27   55.578   ON
  03:00:00                                                                      

  2026-04-03   54.996   9.612       28.998      63.88         131.91   56.266   ON
  04:00:00                                                                      

  2026-04-03   54.205   9.316       29.05       66.25         140.65   57.211   ON
  05:00:00                                                                      

  2026-04-03   54.568   9.388       28.691      64.55         129.8    55.553   ON
  06:00:00                                                                      

  2026-04-03   53.766   9.506       28.78       64.8          130.75   55.374   ON
  07:00:00                                                                      

  2026-04-03   55.862   9.371       28.938      65.76         137.35   56.057   ON
  08:00:00                                                                      

  2026-04-03   55.197   9.437       29.105      64.38         140.9    54.471   ON
  09:00:00                                                                      

  2026-04-03   55.339   9.647       28.548      64.47         133.84   57.033   ON
  10:00:00                                                                      

  2026-04-03   55.912   9.405       28.444      66.89         138.11   57.213   ON
  11:00:00                                                                      

  2026-04-03   52.473   9.362       28.784      64.91         131.36   57.391   ON
  12:00:00                                                                      

  2026-04-03   55.048   9.303       28.785      65.38         131.04   56.943   ON
  13:00:00                                                                      

  2026-04-03   54.738   9.92        28.934      65.79         135.09   55.449   ON
  14:00:00                                                                      

  2026-04-03   55.759   9.429       29.254      65.21         143.42   55.838   ON
  15:00:00                                                                      

  2026-04-03   55.566   9.502       28.668      65.81         133.93   55.072   ON
  16:00:00                                                                      

  2026-04-03   55.585   9.504       29.296      67.88         128.7    56.436   ON
  17:00:00                                                                      

  2026-04-03   56.44    9.664       28.96       66.66         125.28   58.483   ON
  18:00:00                                                                      

  2026-04-03   52.944   9.411       28.82       62.97         134.64   55.025   ON
  19:00:00                                                                      

  2026-04-03   53.832   9.362       28.379      61.79         137.35   56.816   ON
  20:00:00                                                                      

  2026-04-03   56.347   9.44        29.198      63.76         133.52   57.604   ON
  21:00:00                                                                      

  2026-04-03   56.601   9.38        29.271      61.55         135.59   54.961   ON
  22:00:00                                                                      

  2026-04-03   54.109   9.283       28.938      61.04         131.87   58.43    ON
  23:00:00                                                                      

  2026-04-04   56.245   9.216       28.945      63.5          139.86   55.372   ON
  00:00:00                                                                      

  2026-04-04   55.971   9.503       28.703      63.62         136.87   55.986   ON
  01:00:00                                                                      

  2026-04-04   53.498   9.434       28.314      65.31         129.42   56.558   ON
  02:00:00                                                                      

  2026-04-04   54.34    9.706       28.606      65.72         132.46   57.12    ON
  03:00:00                                                                      

  2026-04-04   55.379   9.419       28.437      68.27         139.66   56.974   ON
  04:00:00                                                                      

  2026-04-04   54.931   9.443       28.456      63.99         134.73   55.831   ON
  05:00:00                                                                      

  2026-04-04   56.996   9.679       28.591      64.14         125.57   55.385   ON
  06:00:00                                                                      

  2026-04-04   55.676   9.245       28.658      65.37         133.28   53.544   ON
  07:00:00                                                                      

  2026-04-04   56       9.614       28.94       66.66         132.84   55.549   ON
  08:00:00                                                                      

  2026-04-04   54.284   9.373       29.144      64.66         124.13   57.485   ON
  09:00:00                                                                      

  2026-04-04   53.655   9.327       28.751      63.7          136.62   55.239   ON
  10:00:00                                                                      

  2026-04-04   54.336   9.553       29.012      61.05         140.26   56.776   ON
  11:00:00                                                                      

  2026-04-04   56.562   9.515       28.715      66.29         132.62   56.879   ON
  12:00:00                                                                      

  2026-04-04   57.049   9.327       28.725      64.69         131.24   56.289   ON
  13:00:00                                                                      

  2026-04-04   54.113   9.534       28.893      67.34         133.87   55.496   ON
  14:00:00                                                                      

  2026-04-04   54.854   9.729       28.642      67.73         132.87   55.498   ON
  15:00:00                                                                      

  2026-04-04   52.262   9.62        28.867      67.85         134.41   56.052   ON
  16:00:00                                                                      

  2026-04-04   56.427   9.515       28.678      65.72         136.75   54.179   ON
  17:00:00                                                                      

  2026-04-04   53.617   9.414       28.579      66.34         128.46   57.635   ON
  18:00:00                                                                      

  2026-04-04   55.992   9.484       28.63       63.04         133.36   54.957   ON
  19:00:00                                                                      

  2026-04-04   56.424   9.569       29.193      65.67         142.13   55.416   ON
  20:00:00                                                                      

  2026-04-04   53.537   9.464       28.865      64.5          134.13   55.424   ON
  21:00:00                                                                      

  2026-04-04   54.043   9.566       28.684      66.57         135.09   55.784   ON
  22:00:00                                                                      

  2026-04-04   55.798   9.643       28.846      64.23         136      56.521   ON
  23:00:00                                                                      

  2026-04-05   56.513   9.276       28.605      64.69         131.4    57.428   ON
  00:00:00                                                                      

  2026-04-05   54.425   9.523       28.679      63.8          129.13   56.352   ON
  01:00:00                                                                      

  2026-04-05   53.851   9.573       28.707      67.74         143.64   57.83    ON
  02:00:00                                                                      

  2026-04-05   55.385   9.457       28.368      65.2          134.74   55.702   ON
  03:00:00                                                                      

  2026-04-05   56.401   9.401       28.756      63.54         130.63   56.866   ON
  04:00:00                                                                      

  2026-04-05   53.783   9.723       28.909      64.44         138.12   56.98    ON
  05:00:00                                                                      

  2026-04-05   54.133   9.485       28.867      63.11         133.04   56.27    ON
  06:00:00                                                                      

  2026-04-05   56.285   9.484       28.76       66.81         130.95   56.842   ON
  07:00:00                                                                      

  2026-04-05   55.223   9.417       29.068      66.85         132.59   54.994   ON
  08:00:00                                                                      

  2026-04-05   54.093   9.453       28.587      65.25         129.25   57.566   ON
  09:00:00                                                                      

  2026-04-05   55.004   9.452       29.08       65.46         130.6    57.003   ON
  10:00:00                                                                      

  2026-04-05   55.529   9.482       29.046      62.87         138.17   56.297   ON
  11:00:00                                                                      

  2026-04-05   56.133   9.274       28.85       67.34         135.06   55.727   ON
  12:00:00                                                                      

  2026-04-05   55.326   9.257       29.184      64.95         133.54   57.038   ON
  13:00:00                                                                      

  2026-04-05   54.986   9.404       28.596      68.06         139.77   54.918   ON
  14:00:00                                                                      

  2026-04-05   53.147   9.446       28.861      64.16         137.41   56.922   ON
  15:00:00                                                                      

  2026-04-05   55.594   9.411       28.761      65.72         133.02   57.136   ON
  16:00:00                                                                      

  2026-04-05   55.564   9.603       28.602      66.32         128.77   58.867   ON
  17:00:00                                                                      

  2026-04-05   55.225   9.492       28.716      66.2          132.48   56.019   ON
  18:00:00                                                                      

  2026-04-05   55.02    9.604       28.9        64.85         139.65   57.608   ON
  19:00:00                                                                      

  2026-04-05   55.134   9.531       28.9        66.63         130.92   56.799   ON
  20:00:00                                                                      

  2026-04-05   56.052   9.163       28.958      65.6          143.14   54.356   ON
  21:00:00                                                                      

  2026-04-05   54.589   9.567       28.629      65.05         133.76   54.703   ON
  22:00:00                                                                      

  2026-04-05   53.666   9.713       28.772      63.48         129.23   55.533   ON
  23:00:00                                                                      

  2026-04-06   55.991   9.519       28.769      66.92         132.82   57.395   ON
  00:00:00                                                                      

  2026-04-06   54.581   9.487       28.631      65.07         140.32   57.713   ON
  01:00:00                                                                      

  2026-04-06   54.686   9.325       28.794      65.73         132.16   55.847   ON
  02:00:00                                                                      

  2026-04-06   55.472   9.533       28.258      64.92         136.39   56.596   ON
  03:00:00                                                                      

  2026-04-06   54.717   9.342       28.502      65.53         137.55   56.365   ON
  04:00:00                                                                      

  2026-04-06   54.919   9.235       28.671      64.47         132.41   53.39    ON
  05:00:00                                                                      

  2026-04-06   53.763   9.53        28.701      68.83         138.8    57.322   ON
  06:00:00                                                                      

  2026-04-06   56.434   9.621       28.96       67.72         140.25   57.672   ON
  07:00:00                                                                      

  2026-04-06   53.518   9.454       28.656      66.02         137.77   53.662   ON
  08:00:00                                                                      

  2026-04-06   56.447   9.471       29.222      65.44         127.64   55.089   ON
  09:00:00                                                                      

  2026-04-06   53.599   9.396       28.426      66.02         135.85   56.025   ON
  10:00:00                                                                      

  2026-04-06   54.209   9.735       29.26       63.75         137.55   56.025   ON
  11:00:00                                                                      

  2026-04-06   54.528   9.553       28.556      65.91         138.19   57.273   ON
  12:00:00                                                                      

  2026-04-06   55.959   9.445       28.507      64.88         141.9    57.404   ON
  13:00:00                                                                      

  2026-04-06   55.213   9.452       28.607      64.39         135.84   55.51    ON
  14:00:00                                                                      

  2026-04-06   54.483   9.516       28.638      64            134.86   56.863   ON
  15:00:00                                                                      

  2026-04-06   53.617   9.66        28.721      64.01         126.56   55.409   ON
  16:00:00                                                                      

  2026-04-06   56.092   9.415       28.678      65.73         130.04   55.776   ON
  17:00:00                                                                      

  2026-04-06   55.028   9.364       28.909      65.05         139.15   56.378   ON
  18:00:00                                                                      

  2026-04-06   55.453   9.542       28.99       63.84         130.12   56.717   ON
  19:00:00                                                                      

  2026-04-06   54.783   9.477       28.528      65.63         133.73   55.429   ON
  20:00:00                                                                      

  2026-04-06   54.435   9.277       29.105      65.22         127.99   58.213   ON
  21:00:00                                                                      

  2026-04-06   55.722   9.477       28.857      64.87         133.52   56.343   ON
  22:00:00                                                                      

  2026-04-06   55.316   9.449       28.795      67.17         129.82   56.125   ON
  23:00:00                                                                      

  2026-04-07   56.249   9.435       29.008      64.63         136.52   56.966   ON
  00:00:00                                                                      

  2026-04-07   55.208   9.517       28.771      63.04         134.35   55.424   ON
  01:00:00                                                                      

  2026-04-07   53.435   9.531       29.157      65.23         136.03   56.461   ON
  02:00:00                                                                      

  2026-04-07   55.837   9.745       28.491      63.54         128.55   53.426   ON
  03:00:00                                                                      

  2026-04-07   55.05    9.588       29.1        66.24         133.83   54.232   ON
  04:00:00                                                                      

  2026-04-07   54.737   9.62        28.676      65.86         138      55.715   ON
  05:00:00                                                                      

  2026-04-07   51.574   9.428       28.979      64.55         122.05   55.602   ON
  06:00:00                                                                      

  2026-04-07   54.041   9.496       28.682      65.75         132.19   55.723   ON
  07:00:00                                                                      

  2026-04-07   55.176   9.395       29.213      64.42         134.24   55.402   ON
  08:00:00                                                                      

  2026-04-07   54.301   9.392       28.892      64.33         137.87   56.757   ON
  09:00:00                                                                      

  2026-04-07   55.273   9.619       28.984      62.38         136.99   57.45    ON
  10:00:00                                                                      

  2026-04-07   55.652   9.819       28.529      61.93         137.1    55.561   ON
  11:00:00                                                                      

  2026-04-07   54.975   9.599       28.424      64.4          135.96   57.258   ON
  12:00:00                                                                      

  2026-04-07   53.96    9.556       28.856      67.6          137.72   56.537   ON
  13:00:00                                                                      

  2026-04-07   55.468   9.575       29.177      63.24         134      54.792   ON
  14:00:00                                                                      

  2026-04-07   55.394   9.614       28.837      64.89         134.18   54.633   ON
  15:00:00                                                                      

  2026-04-07   54.721   9.484       28.428      64.03         129.97   56.175   ON
  16:00:00                                                                      

  2026-04-07   52.905   9.486       29.224      65.76         133.8    57.303   ON
  17:00:00                                                                      

  2026-04-07   53.628   9.588       28.668      63.79         133.62   55.105   ON
  18:00:00                                                                      

  2026-04-07   55.871   9.734       28.987      64.84         140.79   53.817   ON
  19:00:00                                                                      

  2026-04-07   54.704   9.507       28.591      65.59         130.21   57.184   ON
  20:00:00                                                                      

  2026-04-07   53.011   9.249       28.618      64.25         135.69   57.388   ON
  21:00:00                                                                      

  2026-04-07   54.787   9.612       28.869      64.78         133.51   55.868   ON
  22:00:00                                                                      

  2026-04-07   55.037   9.526       28.135      64.69         134.86   57.317   ON
  23:00:00                                                                      

  2026-04-08   55.69    9.378       28.546      65.77         138.96   58.352   ON
  00:00:00                                                                      

  2026-04-08   55.463   9.371       28.689      65.92         134.42   55.187   ON
  01:00:00                                                                      

  2026-04-08   55.401   9.025       28.691      66.1          131.02   55.697   ON
  02:00:00                                                                      

  2026-04-08   54.135   9.38        28.385      65.63         135.11   55.705   ON
  03:00:00                                                                      

  2026-04-08   53.136   9.463       29.068      63.54         138.56   57.315   ON
  04:00:00                                                                      

  2026-04-08   54.302   9.571       28.736      64.39         135.99   55.187   ON
  05:00:00                                                                      

  2026-04-08   56.49    9.487       28.747      65.75         137.52   55.776   ON
  06:00:00                                                                      

  2026-04-08   53.312   9.348       28.314      65.07         129.32   57.523   ON
  07:00:00                                                                      

  2026-04-08   55.964   9.434       28.764      66.26         138.45   57.239   ON
  08:00:00                                                                      

  2026-04-08   53.324   9.502       28.947      63.15         132.83   57.292   ON
  09:00:00                                                                      

  2026-04-08   53.541   9.583       28.998      63.7          129.97   55.116   ON
  10:00:00                                                                      

  2026-04-08   55.089   9.538       28.934      63.77         136.04   56.616   ON
  11:00:00                                                                      

  2026-04-08   54.073   9.622       28.764      65.42         129.08   55.495   ON
  12:00:00                                                                      

  2026-04-08   54.703   9.21        28.724      64.07         135.87   57.145   ON
  13:00:00                                                                      

  2026-04-08   53.699   9.526       28.826      63.69         141.09   56.687   ON
  14:00:00                                                                      

  2026-04-08   55.114   9.539       28.947      65.49         132.58   56.914   ON
  15:00:00                                                                      

  2026-04-08   55.909   9.356       28.724      64.39         131.27   55.95    ON
  16:00:00                                                                      

  2026-04-08   53.356   9.526       28.726      63.41         139.21   56.298   ON
  17:00:00                                                                      

  2026-04-08   55.567   9.419       28.876      65.59         137.39   56.554   ON
  18:00:00                                                                      

  2026-04-08   55.38    9.316       28.716      64.83         138.24   55.908   ON
  19:00:00                                                                      

  2026-04-08   55.831   9.304       28.844      65.7          127.2    56.493   ON
  20:00:00                                                                      

  2026-04-08   52.456   9.577       28.812      65.81         131.45   55.08    ON
  21:00:00                                                                      

  2026-04-08   55.952   9.583       28.549      64.12         142.18   54.847   ON
  22:00:00                                                                      

  2026-04-08   53.69    9.659       29.153      64.56         131.53   54.268   ON
  23:00:00                                                                      

  2026-04-09   54.685   9.608       28.946      64.8          132.99   55.981   ON
  00:00:00                                                                      

  2026-04-09   54.471   9.569       28.553      65.96         135.29   57.061   ON
  01:00:00                                                                      

  2026-04-09   53.838   9.338       28.541      64.93         135.67   56.614   ON
  02:00:00                                                                      

  2026-04-09   54.006   9.468       28.657      66.49         134.05   53.98    ON
  03:00:00                                                                      

  2026-04-09   54.155   9.457       28.629      64.18         124.39   56.582   ON
  04:00:00                                                                      

  2026-04-09   55.144   9.797       28.532      64.98         136.97   56.189   ON
  05:00:00                                                                      

  2026-04-09   55.757   9.369       28.831      66.86         130.17   55.971   ON
  06:00:00                                                                      

  2026-04-09   54.628   9.306       28.695      62.96         138.61   56.392   ON
  07:00:00                                                                      

  2026-04-09   55.818   9.349       28.54       63.16         139.76   56.774   ON
  08:00:00                                                                      

  2026-04-09   55.119   9.648       29.155      65.98         130.42   57.636   ON
  09:00:00                                                                      

  2026-04-09   56.216   9.404       28.688      66.07         135.34   57.505   ON
  10:00:00                                                                      

  2026-04-09   53.495   9.607       28.853      66.39         141.3    58.234   ON
  11:00:00                                                                      

  2026-04-09   55.112   9.422       28.442      66.2          141.65   56.789   ON
  12:00:00                                                                      

  2026-04-09   54.904   9.652       28.499      66.47         138.67   55.511   ON
  13:00:00                                                                      

  2026-04-09   55.101   9.27        28.522      64.26         132.79   57.605   ON
  14:00:00                                                                      

  2026-04-09   55.337   9.432       29.003      65.01         136.51   54.835   ON
  15:00:00                                                                      

  2026-04-09   55.838   9.587       28.951      65.79         131.1    57.067   ON
  16:00:00                                                                      

  2026-04-09   55.11    9.464       28.713      63.24         140.87   55.042   ON
  17:00:00                                                                      

  2026-04-09   55.521   9.365       28.697      63.15         136.3    55.53    ON
  18:00:00                                                                      

  2026-04-09   54.637   9.712       28.852      64.13         140.45   57.486   ON
  19:00:00                                                                      

  2026-04-09   54.788   9.29        28.557      66.4          124.84   55.486   ON
  20:00:00                                                                      

  2026-04-09   54.259   9.372       28.711      66.07         132.63   57.318   ON
  21:00:00                                                                      

  2026-04-09   56.13    9.667       29.005      63.12         132.78   56.845   ON
  22:00:00                                                                      

  2026-04-09   55.81    9.752       28.549      64.17         133.25   56.008   ON
  23:00:00                                                                      

  2026-04-10   56.357   9.498       28.93       64.18         129.87   56.969   ON
  00:00:00                                                                      

  2026-04-10   54.437   9.312       28.745      65.08         136.69   56.82    ON
  01:00:00                                                                      

  2026-04-10   54.755   9.308       28.816      65.26         131.36   56.319   ON
  02:00:00                                                                      

  2026-04-10   57.66    9.371       28.733      64.98         142.29   55.472   ON
  03:00:00                                                                      

  2026-04-10   56.13    9.485       28.98       63.65         133.36   57.069   ON
  04:00:00                                                                      

  2026-04-10   53.358   9.697       28.984      66.54         132.98   55.81    ON
  05:00:00                                                                      

  2026-04-10   55.756   9.634       28.905      66.46         132      56.101   ON
  06:00:00                                                                      

  2026-04-10   55.329   9.642       28.367      63.47         137.19   56.645   ON
  07:00:00                                                                      

  2026-04-10   54.576   9.425       28.8        64.73         136.2    56.057   ON
  08:00:00                                                                      

  2026-04-10   54.644   9.609       29.061      66.5          131      56.441   ON
  09:00:00                                                                      

  2026-04-10   54.017   9.618       28.52       65.47         122.8    56.492   ON
  10:00:00                                                                      

  2026-04-10   54.371   9.625       28.391      65.64         133.42   56.469   ON
  11:00:00                                                                      

  2026-04-10   54.102   9.497       28.715      64.34         131.49   56.312   ON
  12:00:00                                                                      

  2026-04-10   53.668   9.439       28.969      67.01         134.86   57.662   ON
  13:00:00                                                                      

  2026-04-10   54.527   9.665       28.455      63.42         131.34   55.646   ON
  14:00:00                                                                      

  2026-04-10   53.979   9.733       28.852      66.29         136.05   55.701   ON
  15:00:00                                                                      

  2026-04-10   55.732   9.467       28.699      67.51         130.26   54.808   ON
  16:00:00                                                                      

  2026-04-10   56.083   9.553       28.759      63.9          135.88   53.636   ON
  17:00:00                                                                      

  2026-04-10   54.778   9.662       28.87       66.9          133.91   56.886   ON
  18:00:00                                                                      

  2026-04-10   54.576   9.727       28.725      66.17         138.67   56.681   ON
  19:00:00                                                                      

  2026-04-10   55.646   9.762       28.629      64.07         134.28   57.716   ON
  20:00:00                                                                      

  2026-04-10   54.816   9.506       28.811      65.21         137.37   54.599   ON
  21:00:00                                                                      

  2026-04-10   57.159   9.69        29.15       67.01         133.66   55.331   ON
  22:00:00                                                                      

  2026-04-10   52.049   9.323       28.918      64.35         134.04   55.546   ON
  23:00:00                                                                      

  2026-04-11   52.381   9.175       28.941      64.35         132.11   58.267   ON
  00:00:00                                                                      

  2026-04-11   53.739   9.437       28.541      60.9          129.68   57.157   ON
  01:00:00                                                                      

  2026-04-11   55.471   9.553       28.643      62.61         135.6    55.967   ON
  02:00:00                                                                      

  2026-04-11   55.804   9.278       28.444      64.44         134.76   56.133   ON
  03:00:00                                                                      

  2026-04-11   54.431   9.479       29          64.8          141.14   56.492   ON
  04:00:00                                                                      

  2026-04-11   54.969   9.527       29.019      65.83         136.72   54.941   ON
  05:00:00                                                                      

  2026-04-11   54.633   9.497       28.879      66.24         142.28   56.522   ON
  06:00:00                                                                      

  2026-04-11   55.49    9.541       28.965      67.79         142.63   54.991   ON
  07:00:00                                                                      

  2026-04-11   57.175   9.667       28.669      65.99         135.97   56.257   ON
  08:00:00                                                                      

  2026-04-11   52.46    9.462       28.682      69.17         130.86   56.892   ON
  09:00:00                                                                      

  2026-04-11   57.398   9.432       29.072      66.09         134.02   56.45    ON
  10:00:00                                                                      

  2026-04-11   56.118   9.582       28.675      66.93         139      55.392   ON
  11:00:00                                                                      

  2026-04-11   54.618   9.659       29.026      63.85         134.72   55.838   ON
  12:00:00                                                                      

  2026-04-11   55.503   9.436       29.184      65.66         139.32   57.004   ON
  13:00:00                                                                      

  2026-04-11   54.934   9.703       28.491      66.39         133.49   55.591   ON
  14:00:00                                                                      

  2026-04-11   55.487   9.61        28.558      66.38         135.35   54.679   ON
  15:00:00                                                                      

  2026-04-11   55.486   9.444       29.194      64.37         138.67   55.839   ON
  16:00:00                                                                      

  2026-04-11   55.819   9.496       29.021      64.95         137.61   55.579   ON
  17:00:00                                                                      

  2026-04-11   53.861   9.384       29.161      63.21         136.31   55.912   ON
  18:00:00                                                                      

  2026-04-11   55.637   9.602       29.193      65.5          135.99   56.126   ON
  19:00:00                                                                      

  2026-04-11   54.242   9.516       28.705      63.51         137.29   55.754   ON
  20:00:00                                                                      

  2026-04-11   54.639   9.794       29.277      66.4          134.67   55.746   ON
  21:00:00                                                                      

  2026-04-11   55.841   9.118       29.122      65.38         138.98   57.103   ON
  22:00:00                                                                      

  2026-04-11   54.482   9.32        29.034      66.03         132.67   56.748   ON
  23:00:00                                                                      

  2026-04-12   55.301   9.425       28.862      65.86         147.07   57.151   ON
  00:00:00                                                                      

  2026-04-12   55.326   9.578       28.694      65.66         135.93   56.199   ON
  01:00:00                                                                      

  2026-04-12   55.083   9.447       28.593      66.18         131.68   55.705   ON
  02:00:00                                                                      

  2026-04-12   53.63    9.394       28.427      65.12         128.56   56.446   ON
  03:00:00                                                                      

  2026-04-12   55.509   9.563       28.574      62.7          131.4    54.548   ON
  04:00:00                                                                      

  2026-04-12   55.175   9.437       28.591      66.84         136.58   54.896   ON
  05:00:00                                                                      

  2026-04-12   57.429   9.536       28.829      63.96         133.05   57.015   ON
  06:00:00                                                                      

  2026-04-12   53.831   9.633       28.609      66.33         139.63   55.587   ON
  07:00:00                                                                      

  2026-04-12   56.139   9.645       28.346      65.8          133.61   55.391   ON
  08:00:00                                                                      

  2026-04-12   54.515   9.27        28.824      65.56         130.82   54.934   ON
  09:00:00                                                                      

  2026-04-12   54.648   9.391       28.275      65.25         133.72   56.583   ON
  10:00:00                                                                      

  2026-04-12   56.865   9.566       28.697      65.42         132.81   54.815   ON
  11:00:00                                                                      

  2026-04-12   54.835   9.474       28.95       65.31         134.19   57.412   ON
  12:00:00                                                                      

  2026-04-12   55.865   9.387       28.401      65.05         130.38   56.317   ON
  13:00:00                                                                      

  2026-04-12   55.126   9.59        28.481      64.84         134.4    54.214   ON
  14:00:00                                                                      

  2026-04-12   53.992   9.514       28.766      65.44         127.44   55.549   ON
  15:00:00                                                                      

  2026-04-12   54.746   9.568       29.111      65.88         135.5    55.005   ON
  16:00:00                                                                      

  2026-04-12   54.506   9.633       28.749      64.4          134.42   56.682   ON
  17:00:00                                                                      

  2026-04-12   54.741   9.445       28.669      65.36         134.34   56.657   ON
  18:00:00                                                                      

  2026-04-12   57.041   9.652       28.846      63.09         131.71   55.569   ON
  19:00:00                                                                      

  2026-04-12   55.504   9.528       28.347      63.84         134.74   55.401   ON
  20:00:00                                                                      

  2026-04-12   53.082   9.541       28.405      62.54         135.76   56.561   ON
  21:00:00                                                                      

  2026-04-12   57.06    9.653       28.95       64.63         128      55.415   ON
  22:00:00                                                                      

  2026-04-12   55.406   9.264       28.978      65.55         138.87   57.519   ON
  23:00:00                                                                      

  2026-04-13   55.979   9.258       28.927      66            134.35   55.377   ON
  00:00:00                                                                      

  2026-04-13   56.714   9.332       28.814      63.08         136.91   56.459   ON
  01:00:00                                                                      

  2026-04-13   54.088   9.628       28.892      66.17         141.06   53.963   ON
  02:00:00                                                                      

  2026-04-13   55.36    9.519       28.344      63.54         130.03   56.488   ON
  03:00:00                                                                      

  2026-04-13   54.837   9.42        28.51       64.42         131      55.413   ON
  04:00:00                                                                      

  2026-04-13   54.611   9.348       28.682      64.29         131.13   56.369   ON
  05:00:00                                                                      

  2026-04-13   54.662   9.251       29.021      67.25         135.15   57.274   ON
  06:00:00                                                                      

  2026-04-13   55.111   9.545       28.829      65.25         130.96   55.888   ON
  07:00:00                                                                      

  2026-04-13   56.283   9.498       28.789      67.99         131.51   53.381   ON
  08:00:00                                                                      

  2026-04-13   55.855   9.557       28.501      66.41         141.97   53.871   ON
  09:00:00                                                                      

  2026-04-13   55.318   9.635       28.812      64.64         134      56.163   ON
  10:00:00                                                                      

  2026-04-13   56.325   9.543       28.876      65.58         136.64   55.105   ON
  11:00:00                                                                      

  2026-04-13   52.451   9.7         28.925      66.94         139.04   54.825   ON
  12:00:00                                                                      

  2026-04-13   55.043   9.441       28.751      63.78         140.86   57.165   ON
  13:00:00                                                                      

  2026-04-13   55.395   9.722       29.291      64.32         129.29   55.817   ON
  14:00:00                                                                      

  2026-04-13   55.35    9.564       28.495      64.96         136.58   57.064   ON
  15:00:00                                                                      

  2026-04-13   56.565   9.422       29.008      64.56         138.1    57.043   ON
  16:00:00                                                                      

  2026-04-13   55.196   9.527       28.467      64.64         139.5    55.632   ON
  17:00:00                                                                      

  2026-04-13   56.518   9.819       28.468      67.44         132.36   56.193   ON
  18:00:00                                                                      

  2026-04-13   54.814   9.317       28.964      65.23         133.31   54.779   ON
  19:00:00                                                                      

  2026-04-13   55.771   9.412       28.687      64.57         135.8    56.48    ON
  20:00:00                                                                      

  2026-04-13   55.129   9.439       28.599      64.46         135.23   56.009   ON
  21:00:00                                                                      

  2026-04-13   54.737   9.525       28.798      63.1          133.74   57.74    ON
  22:00:00                                                                      

  2026-04-13   55.583   9.51        29.425      66.16         132.59   56.944   ON
  23:00:00                                                                      

  2026-04-14   55.644   9.774       28.639      64.12         134.55   55.862   ON
  00:00:00                                                                      

  2026-04-14   54.028   9.471       28.707      70.09         133.9    55.301   ON
  01:00:00                                                                      

  2026-04-14   56.056   9.597       29.098      65.67         136.03   55.798   ON
  02:00:00                                                                      

  2026-04-14   54.726   9.426       28.651      64.19         132.53   56.034   ON
  03:00:00                                                                      

  2026-04-14   55.123   9.337       29.389      63.29         130.94   56.843   ON
  04:00:00                                                                      

  2026-04-14   52.058   9.478       28.473      64.35         133.21   57.129   ON
  05:00:00                                                                      

  2026-04-14   54.986   9.464       28.739      65.59         134.18   54.739   ON
  06:00:00                                                                      

  2026-04-14   52.909   9.599       29.037      64.18         139.3    54.908   ON
  07:00:00                                                                      

  2026-04-14   55.964   9.693       28.736      65.91         133.45   56.387   ON
  08:00:00                                                                      

  2026-04-14   54.156   9.434       28.67       66            126.61   54.727   ON
  09:00:00                                                                      

  2026-04-14   54.528   9.659       28.441      65.81         143.86   55.925   ON
  10:00:00                                                                      

  2026-04-14   54.82    9.351       28.76       65.74         139.89   54.117   ON
  11:00:00                                                                      

  2026-04-14   53.55    9.756       29.007      65.03         137.41   55.671   ON
  12:00:00                                                                      

  2026-04-14   55.044   9.284       28.726      64.08         136.98   55.536   ON
  13:00:00                                                                      

  2026-04-14   53.665   9.425       28.545      63.25         135.22   55.677   ON
  14:00:00                                                                      

  2026-04-14   54.781   9.535       29.125      62.71         142.1    55.326   ON
  15:00:00                                                                      

  2026-04-14   55.957   9.444       29.004      64.37         130.17   56.542   ON
  16:00:00                                                                      

  2026-04-14   56.424   9.334       28.937      65.97         138.08   56.973   ON
  17:00:00                                                                      

  2026-04-14   56.59    9.601       28.737      65            138.12   56.8     ON
  18:00:00                                                                      

  2026-04-14   54.763   9.352       28.578      63.53         144.64   55.727   ON
  19:00:00                                                                      

  2026-04-14   53.958   9.639       29.077      66.3          134.73   55.685   ON
  20:00:00                                                                      

  2026-04-14   55.548   9.285       28.807      63.62         141.26   55.306   ON
  21:00:00                                                                      

  2026-04-14   56.731   9.649       28.697      63.34         136.85   55.243   ON
  22:00:00                                                                      

  2026-04-14   54.048   9.619       28.745      63.6          131.11   55.837   ON
  23:00:00                                                                      

  2026-04-15   56.505   9.574       28.887      64.06         130.65   55.832   ON
  00:00:00                                                                      

  2026-04-15   54.861   9.651       29.001      64.88         139.94   55.79    ON
  01:00:00                                                                      

  2026-04-15   52.104   9.468       28.785      63.23         130.34   56.269   ON
  02:00:00                                                                      

  2026-04-15   55.087   9.49        28.695      62.7          133.94   56.928   ON
  03:00:00                                                                      

  2026-04-15   57.08    9.666       28.508      65.61         141.87   55.335   ON
  04:00:00                                                                      

  2026-04-15   55.803   9.346       28.72       65.36         131.29   55.767   ON
  05:00:00                                                                      

  2026-04-15   56.186   9.458       28.737      65.66         137.42   56.611   ON
  06:00:00                                                                      

  2026-04-15   55.453   9.465       28.869      66.06         142.97   56.238   ON
  07:00:00                                                                      

  2026-04-15   53.158   9.464       28.784      65.06         141.36   55.166   ON
  08:00:00                                                                      

  2026-04-15   52.414   9.456       28.656      67.51         138.33   54.766   ON
  09:00:00                                                                      

  2026-04-15   53.839   9.14        28.76       64.7          132.19   56.721   ON
  10:00:00                                                                      

  2026-04-15   54.586   9.494       28.944      64.91         142.49   54.893   ON
  11:00:00                                                                      

  2026-04-15   53.899   9.536       28.764      66.84         137.18   56.469   ON
  12:00:00                                                                      

  2026-04-15   54.12    9.676       28.745      65.55         135.38   54.963   ON
  13:00:00                                                                      

  2026-04-15   55.868   9.611       28.727      64.77         130.77   57.906   ON
  14:00:00                                                                      

  2026-04-15   56.619   9.408       28.706      64.97         126.41   54.912   ON
  15:00:00                                                                      

  2026-04-15   53.143   9.455       28.873      63.33         136.71   57.977   ON
  16:00:00                                                                      

  2026-04-15   53.833   9.358       28.942      65.93         133.3    56.842   ON
  17:00:00                                                                      

  2026-04-15   54.898   9.442       28.717      64.68         128.25   57.529   ON
  18:00:00                                                                      

  2026-04-15   54.784   9.406       28.742      65.62         138.77   57.37    ON
  19:00:00                                                                      

  2026-04-15   52.412   9.654       28.885      66.87         136.14   56.62    ON
  20:00:00                                                                      

  2026-04-15   58.248   9.55        28.976      66.09         132.69   55.742   ON
  21:00:00                                                                      

  2026-04-15   55.785   9.581       29.13       65.37         133.48   58.679   ON
  22:00:00                                                                      

  2026-04-15   55.404   9.44        28.459      65.54         137.38   55.632   ON
  23:00:00                                                                      

  2026-04-16   52.883   9.472       29          65.18         137.24   56.273   ON
  00:00:00                                                                      

  2026-04-16   55.333   9.569       28.67       67.39         131.5    54.641   ON
  01:00:00                                                                      

  2026-04-16   53.71    9.378       28.944      62.31         138.84   56.066   ON
  02:00:00                                                                      

  2026-04-16   55.569   9.57        29.016      64.35         134.37   56.704   ON
  03:00:00                                                                      

  2026-04-16   55.332   9.622       29.245      63.84         131.1    55.331   ON
  04:00:00                                                                      

  2026-04-16   55.053   9.41        28.666      65.59         134.64   56.228   ON
  05:00:00                                                                      

  2026-04-16   55.482   9.494       29.042      64.73         135.29   55.774   ON
  06:00:00                                                                      

  2026-04-16   54.364   9.37        28.191      65.14         139.86   55.716   ON
  07:00:00                                                                      

  2026-04-16   55.2     9.737       28.804      67.73         137.9    56.748   ON
  08:00:00                                                                      

  2026-04-16   52.351   9.561       28.246      65.39         126.12   57.012   ON
  09:00:00                                                                      

  2026-04-16   55.812   9.655       28.613      66.21         130.21   55.292   ON
  10:00:00                                                                      

  2026-04-16   54.801   9.464       28.512      64.43         138.34   54.243   ON
  11:00:00                                                                      

  2026-04-16   57.804   9.369       28.431      64.04         136.26   56.58    ON
  12:00:00                                                                      

  2026-04-16   55.122   9.483       28.784      63.57         131.28   54.922   ON
  13:00:00                                                                      

  2026-04-16   52.413   9.699       28.518      67.03         133.1    55.597   ON
  14:00:00                                                                      

  2026-04-16   56.698   9.735       28.503      63.45         141.64   55.205   ON
  15:00:00                                                                      

  2026-04-16   54.195   9.612       28.592      64.34         125.61   57.148   ON
  16:00:00                                                                      

  2026-04-16   53.757   9.496       28.658      68.26         140.16   58.411   ON
  17:00:00                                                                      

  2026-04-16   54.955   9.558       28.915      65.55         139.47   55.459   ON
  18:00:00                                                                      

  2026-04-16   56.424   9.657       28.677      65.07         132.74   58.398   ON
  19:00:00                                                                      

  2026-04-16   57.154   9.349       28.558      64.69         134.05   56.254   ON
  20:00:00                                                                      

  2026-04-16   54.576   9.629       28.365      63.39         136.61   55.724   ON
  21:00:00                                                                      

  2026-04-16   55.244   9.38        28.929      65.55         135.47   57.274   ON
  22:00:00                                                                      

  2026-04-16   55.254   9.539       28.857      66.46         136.85   58.133   ON
  23:00:00                                                                      

  2026-04-17   54.282   9.607       28.939      63.75         139.95   55.834   ON
  00:00:00                                                                      

  2026-04-17   54.444   9.542       28.621      64.33         132.6    55.734   ON
  01:00:00                                                                      

  2026-04-17   54.845   9.515       29.084      67.35         135.14   58.065   ON
  02:00:00                                                                      

  2026-04-17   54.936   9.69        28.923      64.49         136.99   57.022   ON
  03:00:00                                                                      

  2026-04-17   56.179   9.443       29.348      66.07         133.4    53.078   ON
  04:00:00                                                                      

  2026-04-17   52.868   9.451       28.697      68.24         135.02   55.902   ON
  05:00:00                                                                      

  2026-04-17   55.529   9.367       28.994      63.8          141.01   55.218   ON
  06:00:00                                                                      

  2026-04-17   55.416   9.529       29.188      64.9          126.93   55.446   ON
  07:00:00                                                                      

  2026-04-17   56.521   9.612       28.73       63.73         136.29   56.204   ON
  08:00:00                                                                      

  2026-04-17   54.575   9.486       28.782      61.85         132.99   55.563   ON
  09:00:00                                                                      

  2026-04-17   54.587   9.224       28.665      66.87         130.57   55.64    ON
  10:00:00                                                                      

  2026-04-17   55.115   9.566       28.721      65.87         134.22   58.293   ON
  11:00:00                                                                      

  2026-04-17   54.374   9.594       28.987      64.61         136.64   54.332   ON
  12:00:00                                                                      

  2026-04-17   54.34    9.378       28.839      65.66         138.45   56.248   ON
  13:00:00                                                                      

  2026-04-17   54.26    9.468       28.529      64.18         132.09   56.707   ON
  14:00:00                                                                      

  2026-04-17   54.262   9.506       29.398      62.97         137.75   54.523   ON
  15:00:00                                                                      

  2026-04-17   53.861   9.39        28.613      64.11         140.99   54.854   ON
  16:00:00                                                                      

  2026-04-17   54.323   9.541       29.076      63.94         135.89   54.857   ON
  17:00:00                                                                      

  2026-04-17   54.129   9.514       28.803      63.6          138.05   56.982   ON
  18:00:00                                                                      

  2026-04-17   54.179   9.334       28.959      66.52         137.04   54.909   ON
  19:00:00                                                                      

  2026-04-17   53.511   9.102       28.934      63.8          137.82   56.605   ON
  20:00:00                                                                      

  2026-04-17   56.038   9.367       28.991      63.45         131.36   54.788   ON
  21:00:00                                                                      

  2026-04-17   55.331   9.707       28.99       65.26         140.06   54.722   ON
  22:00:00                                                                      

  2026-04-17   54.931   9.676       29.219      65.66         137.03   56.545   ON
  23:00:00                                                                      

  2026-04-18   53.79    9.455       28.626      67.36         142.53   56.951   ON
  00:00:00                                                                      

  2026-04-18   55.694   9.345       28.47       65.39         138.47   54.621   ON
  01:00:00                                                                      

  2026-04-18   54.719   9.711       28.383      63.05         131.68   54.969   ON
  02:00:00                                                                      

  2026-04-18   54.868   9.603       28.289      63.72         139.89   56.327   ON
  03:00:00                                                                      

  2026-04-18   55.085   9.682       28.917      66.35         140.72   55.014   ON
  04:00:00                                                                      

  2026-04-18   54.859   9.771       28.361      64.06         139.46   54.809   ON
  05:00:00                                                                      

  2026-04-18   56.071   9.565       28.394      65.67         134.03   54.893   ON
  06:00:00                                                                      

  2026-04-18   54.11    9.513       28.851      67.65         133.56   56.373   ON
  07:00:00                                                                      

  2026-04-18   54.257   9.39        28.72       62.91         140.64   53.24    ON
  08:00:00                                                                      

  2026-04-18   55.149   9.522       28.813      62.85         132.12   57.934   ON
  09:00:00                                                                      

  2026-04-18   54.761   9.356       28.126      64.7          138.74   57.764   ON
  10:00:00                                                                      

  2026-04-18   55.591   9.656       28.472      64.95         135.77   57.395   ON
  11:00:00                                                                      

  2026-04-18   55.999   9.469       28.408      66.25         132.59   55.82    ON
  12:00:00                                                                      

  2026-04-18   56.507   9.731       28.781      62.7          133.74   55.32    ON
  13:00:00                                                                      

  2026-04-18   56.043   9.451       28.776      65.85         133.09   56.617   ON
  14:00:00                                                                      

  2026-04-18   54.68    9.565       28.885      64.64         137.27   54.854   ON
  15:00:00                                                                      

  2026-04-18   54.808   9.387       29.089      62.57         132.57   58.357   ON
  16:00:00                                                                      

  2026-04-18   54.58    9.629       29.644      64.63         134.9    55.386   ON
  17:00:00                                                                      

  2026-04-18   56.261   9.381       28.656      65.68         134.28   57.323   ON
  18:00:00                                                                      

  2026-04-18   54.74    9.69        28.96       67.54         136.8    56.913   ON
  19:00:00                                                                      

  2026-04-18   54.052   9.581       29.011      64.09         139.28   55.566   ON
  20:00:00                                                                      

  2026-04-18   53.845   9.232       28.76       65.99         129.3    55.792   ON
  21:00:00                                                                      

  2026-04-18   55.818   9.299       28.541      63.09         136.89   55.15    ON
  22:00:00                                                                      

  2026-04-18   54.032   9.536       29.002      66.51         132.44   56.151   ON
  23:00:00                                                                      

  2026-04-19   52.081   9.492       29.009      65.12         134.42   56.686   ON
  00:00:00                                                                      

  2026-04-19   55.776   9.792       28.926      67.24         134.69   56.058   ON
  01:00:00                                                                      

  2026-04-19   55.363   9.372       28.609      63.07         141.52   55.672   ON
  02:00:00                                                                      

  2026-04-19   55.84    9.47        28.236      63.36         141.29   56.074   ON
  03:00:00                                                                      

  2026-04-19   56.085   9.5         28.53       62.56         134.27   57.384   ON
  04:00:00                                                                      

  2026-04-19   55.561   9.535       29.087      67.53         134.26   57.015   ON
  05:00:00                                                                      

  2026-04-19   55.43    9.753       29.084      64.32         141.01   56.584   ON
  06:00:00                                                                      

  2026-04-19   55.059   9.488       28.537      62.38         137.28   55.371   ON
  07:00:00                                                                      

  2026-04-19   54.136   9.268       28.851      63.92         142.74   55.539   ON
  08:00:00                                                                      

  2026-04-19   52.673   9.731       29.111      66.19         132.44   56.576   ON
  09:00:00                                                                      

  2026-04-19   52.842   9.563       29.119      65.9          139.81   55.625   ON
  10:00:00                                                                      

  2026-04-19   55.414   9.283       28.56       65.6          133.26   55.304   ON
  11:00:00                                                                      

  2026-04-19   55.885   9.403       28.744      63.08         123.55   57.52    ON
  12:00:00                                                                      

  2026-04-19   55.039   9.456       28.773      64.73         138.26   56.162   ON
  13:00:00                                                                      

  2026-04-19   54.162   9.52        28.516      62.14         131.42   56.295   ON
  14:00:00                                                                      

  2026-04-19   55.706   9.619       29.222      62.82         138.09   55.412   ON
  15:00:00                                                                      

  2026-04-19   54.976   9.466       28.352      65.83         134.02   56.348   ON
  16:00:00                                                                      

  2026-04-19   55.016   9.425       28.892      66.26         140.22   56.919   ON
  17:00:00                                                                      

  2026-04-19   54.607   9.359       29.046      64.65         129.76   56.337   ON
  18:00:00                                                                      

  2026-04-19   53.718   9.477       28.904      62.37         128.94   54.449   ON
  19:00:00                                                                      

  2026-04-19   53.898   9.512       28.977      63.6          141.21   55.517   ON
  20:00:00                                                                      

  2026-04-19   55.429   9.569       28.233      64.43         139.59   56.62    ON
  21:00:00                                                                      

  2026-04-19   56.794   9.185       28.805      67.26         135.63   56.287   ON
  22:00:00                                                                      

  2026-04-19   56.945   9.371       28.867      64.05         128.71   57.117   ON
  23:00:00                                                                      

  2026-04-20   54.808   9.571       28.864      62.87         138.63   55.71    ON
  00:00:00                                                                      

  2026-04-20   55.505   9.748       28.465      63.27         145.05   55.974   ON
  01:00:00                                                                      

  2026-04-20   54.914   9.634       28.734      63.73         133.74   57.013   ON
  02:00:00                                                                      

  2026-04-20   55.178   9.167       28.589      64.19         133.61   55.977   ON
  03:00:00                                                                      

  2026-04-20   55.467   9.217       29.141      64.6          131.82   56.956   ON
  04:00:00                                                                      

  2026-04-20   56.008   9.584       28.631      67.85         136.99   54.138   ON
  05:00:00                                                                      

  2026-04-20   53.758   9.507       28.761      64.13         134.87   54.993   ON
  06:00:00                                                                      

  2026-04-20   56.959   9.51        28.75       61.89         129.02   57.021   ON
  07:00:00                                                                      

  2026-04-20   54.875   9.79        28.743      66.44         132.25   56.895   ON
  08:00:00                                                                      

  2026-04-20   53.937   9.345       29.217      63.85         138.95   56.848   ON
  09:00:00                                                                      

  2026-04-20   57.559   9.678       29.158      63.86         130.6    57.012   ON
  10:00:00                                                                      

  2026-04-20   54.035   9.517       28.89       64.15         136.13   57.023   ON
  11:00:00                                                                      

  2026-04-20   54.975   9.414       28.713      65.42         139.22   54.819   ON
  12:00:00                                                                      

  2026-04-20   54.21    9.195       28.686      65.16         138.12   57.742   ON
  13:00:00                                                                      

  2026-04-20   56.315   9.328       28.333      65.64         127.95   56.954   ON
  14:00:00                                                                      

  2026-04-20   52.069   9.724       28.815      64.48         137.4    54.746   ON
  15:00:00                                                                      

  2026-04-20   55.387   9.514       28.875      65.05         130.61   54.595   ON
  16:00:00                                                                      

  2026-04-20   53.267   9.619       28.754      63.4          126.99   56.451   ON
  17:00:00                                                                      

  2026-04-20   56.728   9.586       28.566      63.42         136.26   55.281   ON
  18:00:00                                                                      

  2026-04-20   57.324   9.478       29.093      64.08         128.52   56.565   ON
  19:00:00                                                                      

  2026-04-20   55.964   9.624       28.989      64.31         134.07   55.694   ON
  20:00:00                                                                      

  2026-04-20   54.158   9.547       28.838      62.49         139.97   54.391   ON
  21:00:00                                                                      

  2026-04-20   56.298   9.474       29.191      63.21         137.23   55.097   ON
  22:00:00                                                                      

  2026-04-20   57.431   9.454       28.862      66.74         134.46   55.595   ON
  23:00:00                                                                      

  2026-04-21   55.295   9.394       29.253      66.64         138.73   55.993   ON
  00:00:00                                                                      

  2026-04-21   54.606   9.543       28.754      67.31         135.23   56.857   ON
  01:00:00                                                                      

  2026-04-21   56.633   9.473       28.838      66.62         138.19   55.294   ON
  02:00:00                                                                      

  2026-04-21   53.552   9.664       28.651      66.24         139.5    56.509   ON
  03:00:00                                                                      

  2026-04-21   54.695   9.455       29.026      67.46         130.98   55.761   ON
  04:00:00                                                                      

  2026-04-21   54.958   9.367       28.68       65.89         141.6    55.867   ON
  05:00:00                                                                      

  2026-04-21   55.152   9.227       28.901      64.49         134.43   53.512   ON
  06:00:00                                                                      

  2026-04-21   56.233   9.612       28.833      64.54         135.23   55.459   ON
  07:00:00                                                                      

  2026-04-21   54.852   9.867       28.615      65.44         135.71   54.443   ON
  08:00:00                                                                      

  2026-04-21   53.798   9.496       29.35       65.59         133.84   56.731   ON
  09:00:00                                                                      

  2026-04-21   53.47    9.175       29.073      64.76         133.19   57.172   ON
  10:00:00                                                                      

  2026-04-21   54.853   9.637       28.743      64.49         137.1    56.47    ON
  11:00:00                                                                      

  2026-04-21   55.526   9.403       29.013      64.91         132.52   58.235   ON
  12:00:00                                                                      

  2026-04-21   56.075   9.603       28.889      63.82         136.85   56.285   ON
  13:00:00                                                                      

  2026-04-21   55.696   9.554       28.694      68.23         137.9    56.907   ON
  14:00:00                                                                      

  2026-04-21   53.495   9.606       29.258      65.73         132.66   55.633   ON
  15:00:00                                                                      

  2026-04-21   55.64    9.519       29.01       62.09         133.64   56.392   ON
  16:00:00                                                                      

  2026-04-21   54.284   9.461       28.955      66.26         137.06   54.898   ON
  17:00:00                                                                      

  2026-04-21   56.446   9.658       28.933      63.8          134.82   55.675   ON
  18:00:00                                                                      

  2026-04-21   54.679   9.458       28.971      64.67         137.46   57.12    ON
  19:00:00                                                                      

  2026-04-21   54.704   9.673       28.995      65.01         134.7    55.991   ON
  20:00:00                                                                      

  2026-04-21   54.401   9.413       28.867      66.29         133.61   55.643   ON
  21:00:00                                                                      

  2026-04-21   56.094   9.523       28.855      64.94         134.06   55.875   ON
  22:00:00                                                                      

  2026-04-21   54.894   9.391       28.838      65.41         136.18   56.541   ON
  23:00:00                                                                      

  2026-04-22   58.043   9.637       28.432      64.81         139.63   57.481   ON
  00:00:00                                                                      

  2026-04-22   56.301   9.401       28.763      68.37         128.21   54.375   ON
  01:00:00                                                                      

  2026-04-22   53.729   9.38        29.112      64.94         133      55.98    ON
  02:00:00                                                                      

  2026-04-22   54.978   9.64        29.19       63.71         133.37   55.854   ON
  03:00:00                                                                      

  2026-04-22   56.168   9.55        28.858      63.11         131.75   55.74    ON
  04:00:00                                                                      

  2026-04-22   55.892   9.488       28.61       65.02         133.03   55.972   ON
  05:00:00                                                                      

  2026-04-22   55.692   9.355       29.059      64.35         139.61   56.558   ON
  06:00:00                                                                      

  2026-04-22   55.293   9.493       28.608      65.26         138.99   57.265   ON
  07:00:00                                                                      

  2026-04-22   53.325   9.558       28.552      65.64         132.54   54.134   ON
  08:00:00                                                                      

  2026-04-22   53.37    9.597       28.46       63.32         129.17   54.711   ON
  09:00:00                                                                      

  2026-04-22   55.912   9.396       28.299      65.11         136.59   56.118   ON
  10:00:00                                                                      

  2026-04-22   54.328   9.573       29.274      63.95         136.85   54.423   ON
  11:00:00                                                                      

  2026-04-22   55.044   9.222       28.817      63.99         130.22   56.486   ON
  12:00:00                                                                      

  2026-04-22   55.725   9.509       28.097      63.63         135.74   55.068   ON
  13:00:00                                                                      

  2026-04-22   52.944   9.366       28.602      64.65         136.63   55.842   ON
  14:00:00                                                                      

  2026-04-22   52.943   9.604       28.381      63.97         137.58   54.726   ON
  15:00:00                                                                      

  2026-04-22   55.61    9.436       29.017      63.99         132.93   54.996   ON
  16:00:00                                                                      

  2026-04-22   54.378   9.836       28.64       64.49         136.95   58.941   ON
  17:00:00                                                                      

  2026-04-22   54.637   9.522       28.614      63.12         134.29   55.62    ON
  18:00:00                                                                      

  2026-04-22   56.272   9.546       28.959      66.92         138.34   57.545   ON
  19:00:00                                                                      

  2026-04-22   54.725   9.167       29.2        65.92         135.94   55.933   ON
  20:00:00                                                                      

  2026-04-22   54.954   9.296       28.607      64.45         137.44   56.668   ON
  21:00:00                                                                      

  2026-04-22   55.337   9.648       28.784      65.44         135      55.106   ON
  22:00:00                                                                      

  2026-04-22   53.113   9.399       28.554      63.64         133.94   56.515   ON
  23:00:00                                                                      

  2026-04-23   56.927   9.661       29.026      65.15         135.87   55.407   ON
  00:00:00                                                                      

  2026-04-23   55.464   9.394       28.857      62.79         138.38   52.88    ON
  01:00:00                                                                      

  2026-04-23   54.414   9.587       28.827      64.91         133.47   53.108   ON
  02:00:00                                                                      

  2026-04-23   56.265   9.38        28.593      65.17         136.37   55.836   ON
  03:00:00                                                                      

  2026-04-23   53.99    9.561       29.164      64.46         144.66   56.69    ON
  04:00:00                                                                      

  2026-04-23   54.254   9.596       28.721      66.06         132.39   55.117   ON
  05:00:00                                                                      

  2026-04-23   53.656   9.63        29.087      63.83         129.7    54.807   ON
  06:00:00                                                                      

  2026-04-23   54.757   9.389       29.099      65.18         131.18   55.343   ON
  07:00:00                                                                      

  2026-04-23   54.189   9.307       28.51       65.8          133.81   57.753   ON
  08:00:00                                                                      

  2026-04-23   55.298   9.579       28.746      65.76         134.95   53.958   ON
  09:00:00                                                                      

  2026-04-23   54.272   9.53        28.858      64.96         126.09   56.669   ON
  10:00:00                                                                      

  2026-04-23   55.294   9.596       28.527      67.4          127.08   57.21    ON
  11:00:00                                                                      

  2026-04-23   55.488   9.32        28.771      66.14         138.05   54.482   ON
  12:00:00                                                                      

  2026-04-23   55.437   9.607       28.874      65.94         129.37   54.94    ON
  13:00:00                                                                      

  2026-04-23   55.42    9.473       28.386      63.95         137.65   55.52    ON
  14:00:00                                                                      

  2026-04-23   55.097   9.34        28.72       65.11         139.81   55.223   ON
  15:00:00                                                                      

  2026-04-23   54.098   9.431       28.874      64.22         122.76   56.992   ON
  16:00:00                                                                      

  2026-04-23   52.818   9.633       28.68       67.96         137.15   56.042   ON
  17:00:00                                                                      

  2026-04-23   55.391   9.523       28.649      65.54         135.1    55.376   ON
  18:00:00                                                                      

  2026-04-23   53.459   9.52        28.446      63.9          133.61   56.349   ON
  19:00:00                                                                      

  2026-04-23   55.378   9.511       28.798      66.24         136.48   57.28    ON
  20:00:00                                                                      

  2026-04-23   54.947   9.441       28.845      66.59         134.73   55.551   ON
  21:00:00                                                                      

  2026-04-23   54.949   9.678       28.768      64.17         137.1    55.058   ON
  22:00:00                                                                      

  2026-04-23   55.009   9.502       29.133      65.25         142.25   56.969   ON
  23:00:00                                                                      

  2026-04-24   55.633   9.286       28.797      68.61         136.17   57.848   ON
  00:00:00                                                                      

  2026-04-24   53.93    9.287       28.691      65.06         130.13   57.665   ON
  01:00:00                                                                      

  2026-04-24   55.349   9.418       29.227      65.51         140.49   56.854   ON
  02:00:00                                                                      

  2026-04-24   56.188   9.443       28.969      69.52         139.41   55.8     ON
  03:00:00                                                                      

  2026-04-24   55.868   9.606       29.069      64.99         140.71   56.883   ON
  04:00:00                                                                      

  2026-04-24   56.216   9.116       29.117      63.29         136.51   56.62    ON
  05:00:00                                                                      

  2026-04-24   54.696   9.611       28.669      63.63         138.51   56.686   ON
  06:00:00                                                                      

  2026-04-24   54.911   9.672       28.557      65.2          142.8    55.984   ON
  07:00:00                                                                      

  2026-04-24   57.061   9.429       29.208      66.13         134.72   57.154   ON
  08:00:00                                                                      

  2026-04-24   55.556   9.684       28.325      63.73         132.55   56.988   ON
  09:00:00                                                                      

  2026-04-24   55.286   9.399       28.667      62.04         140.73   54.664   ON
  10:00:00                                                                      

  2026-04-24   56.101   9.475       29.195      65.82         133.65   56.814   ON
  11:00:00                                                                      

  2026-04-24   54.043   9.426       28.634      64.69         139.56   54.956   ON
  12:00:00                                                                      

  2026-04-24   54.855   9.736       28.984      64.27         132.91   56.174   ON
  13:00:00                                                                      

  2026-04-24   55.486   9.67        28.6        63.71         133.14   55.893   ON
  14:00:00                                                                      

  2026-04-24   54.935   9.662       29.389      66.61         136.21   56.577   ON
  15:00:00                                                                      

  2026-04-24   56.662   9.332       28.78       64.75         136.3    55.51    ON
  16:00:00                                                                      

  2026-04-24   55.482   9.514       29.002      63.09         132.01   55.66    ON
  17:00:00                                                                      

  2026-04-24   55.973   9.332       28.469      63.54         141.49   55.497   ON
  18:00:00                                                                      

  2026-04-24   54.095   9.523       28.983      64.33         133.36   55.523   ON
  19:00:00                                                                      

  2026-04-24   54.99    9.583       28.972      62.87         137.84   54.506   ON
  20:00:00                                                                      

  2026-04-24   54.974   9.703       28.687      64.24         131.46   56.627   ON
  21:00:00                                                                      

  2026-04-24   55.573   9.479       28.971      66.65         132.66   55.431   ON
  22:00:00                                                                      

  2026-04-24   55.538   9.535       28.748      66.22         132.81   56.443   ON
  23:00:00                                                                      

  2026-04-25   55.005   9.48        28.9        66.44         135.7    56.054   ON
  00:00:00                                                                      

  2026-04-25   55.641   9.342       28.675      66.41         135.7    56.522   ON
  01:00:00                                                                      

  2026-04-25   57.303   9.747       28.688      65.21         135.92   56.699   ON
  02:00:00                                                                      

  2026-04-25   55.038   9.558       28.495      65.53         135.14   54.654   ON
  03:00:00                                                                      

  2026-04-25   54.289   9.715       28.911      62.47         138.72   55.943   ON
  04:00:00                                                                      

  2026-04-25   56.331   9.626       28.749      66.09         138.67   56.278   ON
  05:00:00                                                                      

  2026-04-25   56.637   9.312       28.627      65.9          133.36   55.314   ON
  06:00:00                                                                      

  2026-04-25   55.212   9.408       29.211      65.34         135.64   55.357   ON
  07:00:00                                                                      

  2026-04-25   56.066   9.603       28.807      65.32         136.89   56.477   ON
  08:00:00                                                                      

  2026-04-25   52.766   9.628       28.766      63.43         137.93   57.464   ON
  09:00:00                                                                      

  2026-04-25   55.529   9.603       28.621      64.3          137.11   56.671   ON
  10:00:00                                                                      

  2026-04-25   54.81    9.501       29.033      62.71         133.77   56.838   ON
  11:00:00                                                                      

  2026-04-25   57.429   9.629       28.84       64.29         133.82   56.425   ON
  12:00:00                                                                      

  2026-04-25   55.265   9.354       28.596      64.62         135.38   58.155   ON
  13:00:00                                                                      

  2026-04-25   57.029   9.464       28.74       64.05         137.04   56.132   ON
  14:00:00                                                                      

  2026-04-25   54.813   9.329       28.947      66.68         130.92   57.073   ON
  15:00:00                                                                      

  2026-04-25   54.713   9.649       28.828      63.78         131.19   59.755   ON
  16:00:00                                                                      

  2026-04-25   54.43    9.557       29.092      65.47         133.52   56.493   ON
  17:00:00                                                                      

  2026-04-25   53.731   9.606       29.058      65.29         135.44   56.069   ON
  18:00:00                                                                      

  2026-04-25   54.394   9.461       29.349      64.74         132.52   54.394   ON
  19:00:00                                                                      

  2026-04-25   56.226   9.122       28.64       65.8          133.38   54.328   ON
  20:00:00                                                                      

  2026-04-25   53.34    9.382       28.792      65.56         131.9    58.407   ON
  21:00:00                                                                      

  2026-04-25   55.12    9.523       28.742      64.44         137.1    56.153   ON
  22:00:00                                                                      

  2026-04-25   56.238   9.508       28.743      66.9          127.24   55.101   ON
  23:00:00                                                                      

  2026-04-26   55.299   9.637       28.82       64.79         135.03   55.553   ON
  00:00:00                                                                      

  2026-04-26   55.589   9.668       28.716      65.9          132.45   54.873   ON
  01:00:00                                                                      

  2026-04-26   55.397   9.416       29.027      63.5          135.17   56.074   ON
  02:00:00                                                                      

  2026-04-26   55.59    9.618       28.497      63.67         135.8    55.38    ON
  03:00:00                                                                      

  2026-04-26   52.924   9.242       28.817      65.25         123.27   56.716   ON
  04:00:00                                                                      

  2026-04-26   56.665   9.6         28.96       68.35         139.46   57.715   ON
  05:00:00                                                                      

  2026-04-26   55.416   9.184       29.053      63.16         137.91   56.619   ON
  06:00:00                                                                      

  2026-04-26   54.418   9.575       28.801      63.27         141.27   56.14    ON
  07:00:00                                                                      

  2026-04-26   54.7     9.159       28.882      63.89         138.14   56.124   ON
  08:00:00                                                                      

  2026-04-26   54.873   9.574       28.819      64.36         138.65   57.592   ON
  09:00:00                                                                      

  2026-04-26   55.77    9.739       28.928      65.09         137.22   54.651   ON
  10:00:00                                                                      

  2026-04-26   53.737   9.475       28.762      66.51         141.33   55.051   ON
  11:00:00                                                                      

  2026-04-26   53.652   9.605       28.983      64.76         129.82   55.49    ON
  12:00:00                                                                      

  2026-04-26   53.594   9.667       29.14       65.86         134.68   54.79    ON
  13:00:00                                                                      

  2026-04-26   56.012   9.096       29.323      65.04         131.45   56.645   ON
  14:00:00                                                                      

  2026-04-26   54.033   9.21        28.723      64.18         138.52   55.678   ON
  15:00:00                                                                      

  2026-04-26   55.166   9.503       29.015      64.3          136.09   55.051   ON
  16:00:00                                                                      

  2026-04-26   53.779   9.336       28.874      65.72         141.48   56.691   ON
  17:00:00                                                                      

  2026-04-26   54.96    9.439       28.912      65.27         135.64   56       ON
  18:00:00                                                                      

  2026-04-26   54.489   9.91        28.697      66.93         134.39   56.538   ON
  19:00:00                                                                      

  2026-04-26   54.23    9.781       28.837      65.3          134.4    56.087   ON
  20:00:00                                                                      

  2026-04-26   56.265   9.598       28.947      64.84         132.14   55.521   ON
  21:00:00                                                                      

  2026-04-26   55.144   9.4         28.814      63.36         127.06   54.937   ON
  22:00:00                                                                      

  2026-04-26   53.989   9.584       28.708      63.91         134.94   56.596   ON
  23:00:00                                                                      

  2026-04-27   57.656   9.556       29.112      65.55         133.37   55.087   ON
  00:00:00                                                                      

  2026-04-27   54.008   9.478       28.84       65.48         133.31   57.215   ON
  01:00:00                                                                      

  2026-04-27   53.755   9.753       28.752      67.42         130.56   56.372   ON
  02:00:00                                                                      

  2026-04-27   53.201   9.214       28.813      64.12         135.44   56.058   ON
  03:00:00                                                                      

  2026-04-27   56.802   9.742       28.755      65.96         130.96   55.214   ON
  04:00:00                                                                      

  2026-04-27   55.263   9.439       28.622      64.92         136.13   57.886   ON
  05:00:00                                                                      

  2026-04-27   55.406   9.702       28.937      62.03         134.13   55.811   ON
  06:00:00                                                                      

  2026-04-27   56.244   9.483       29.063      63.36         133.79   56.693   ON
  07:00:00                                                                      

  2026-04-27   55.179   9.417       29.75       65.41         128.82   55.399   ON
  08:00:00                                                                      

  2026-04-27   55.833   9.402       31.244      64.52         136.36   57.364   ON
  09:00:00                                                                      

  2026-04-27   56.88    9.543       31.846      64.07         138.47   56.569   ON
  10:00:00                                                                      

  2026-04-27   55.323   9.557       32.512      66.63         134.53   57.233   ON
  11:00:00                                                                      

  2026-04-27   55.931   9.963       33.785      64.72         132.75   57.008   ON
  12:00:00                                                                      

  2026-04-27   55.278   9.746       34.566      65.45         137.47   55.972   ON
  13:00:00                                                                      

  2026-04-27   55.209   9.498       35.724      66.14         138.14   55.159   ON
  14:00:00                                                                      

  2026-04-27   56.613   9.319       36.322      64.38         133.34   56.183   ON
  15:00:00                                                                      

  2026-04-27   55.693   9.519       37.449      65.98         145.82   55.419   ON
  16:00:00                                                                      

  2026-04-27   55.358   9.592       38.084      63.6          139.92   55.715   ON
  17:00:00                                                                      

  2026-04-27   52.984   9.246       39.085      63.17         140.97   57.971   ON
  18:00:00                                                                      

  2026-04-27   54.079   9.506       40.384      66.65         136.7    57.145   ON
  19:00:00                                                                      

  2026-04-27   54.303   9.701       41.158      66.92         136.63   56.488   ON
  20:00:00                                                                      

  2026-04-27   55.036   9.434       42.611      66.09         131.17   56.866   ON
  21:00:00                                                                      

  2026-04-27   55.467   9.26        42.992      63.94         134.03   57.124   ON
  22:00:00                                                                      

  2026-04-27   55.229   9.621       44.151      64.54         135.27   56.4     ON
  23:00:00                                                                      

  2026-04-28   54.881   9.751       44.733      63.68         137.79   56.099   ON
  00:00:00                                                                      

  2026-04-28   55.433   9.474       46.353      63.68         133.06   56.302   ON
  01:00:00                                                                      

  2026-04-28   55.446   9.531       46.933      65.23         131.71   56.699   ON
  02:00:00                                                                      

  2026-04-28   56.036   9.684       47.482      64.35         139.66   58.404   ON
  03:00:00                                                                      

  2026-04-28   53.117   9.589       48.855      66.7          135.48   54.938   ON
  04:00:00                                                                      

  2026-04-28   56.171   9.401       49.614      62.77         138.79   56.246   ON
  05:00:00                                                                      

  2026-04-28   57.194   9.454       51.204      64.28         135.48   55.607   ON
  06:00:00                                                                      

  2026-04-28   56.303   9.494       51.88       63.26         132.64   58.761   ON
  07:00:00                                                                      

  2026-04-28   54.587   9.507       52.355      63.14         134.97   55.626   ON
  08:00:00                                                                      

  2026-04-28   54.072   9.686       53.662      67.73         125.36   57.558   ON
  09:00:00                                                                      

  2026-04-28   54.989   9.35        54.543      67.3          138.91   56.863   ON
  10:00:00                                                                      

  2026-04-28   56.526   9.568       55.274      65.63         137.25   56.732   ON
  11:00:00                                                                      

  2026-04-28   55.356   9.484       56.218      65.78         139.67   57.359   ON
  12:00:00                                                                      

  2026-04-28   52.855   9.19        57.173      65.89         134.18   56.659   ON
  13:00:00                                                                      

  2026-04-28   51.443   9.619       57.934      65.07         142.85   55.884   ON
  14:00:00                                                                      

  2026-04-28   55.273   9.529       59.183      60.49         139.88   58.254   ON
  15:00:00                                                                      

  2026-04-28   57.65    9.31        59.927      61.74         128.11   54.955   ON
  16:00:00                                                                      

  2026-04-28   53.303   9.235       60.964      65.83         128.04   54.203   ON
  17:00:00                                                                      

  2026-04-28   54.346   9.651       61.836      61.28         136.06   55.373   ON
  18:00:00                                                                      

  2026-04-28   55.057   9.765       62.684      67.04         129.56   56.97    ON
  19:00:00                                                                      

  2026-04-28   55.369   9.521       64.277      66.19         134.45   55.489   ON
  20:00:00                                                                      

  2026-04-28   55.985   9.473       64.81       65.44         134.34   56.32    ON
  21:00:00                                                                      

  2026-04-28   53.279   9.618       65.841      65.53         133.8    57.226   ON
  22:00:00                                                                      

  2026-04-28   55.138   9.406       67.278      66.01         140.97   56.964   ON
  23:00:00                                                                      

  2026-04-29   54.297   9.427       67.54       64.11         137.28   56.667   ON
  00:00:00                                                                      

  2026-04-29   55.925   9.653       68.314      67.66         137.56   57.424   ON
  01:00:00                                                                      

  2026-04-29   55.435   9.332       69.003      64.61         135.96   56.28    ON
  02:00:00                                                                      

  2026-04-29   56.231   9.683       70.011      63.64         146.8    57.399   ON
  03:00:00                                                                      

  2026-04-29   53.666   9.553       71.456      67.68         140.27   56.46    ON
  04:00:00                                                                      

  2026-04-29   53.785   9.708       71.896      65.19         132.3    57.881   ON
  05:00:00                                                                      

  2026-04-29   54.221   9.222       72.67       65.47         137.25   57.43    ON
  06:00:00                                                                      

  2026-04-29   0.037    0.242       25.275      40.35         3.96     0        OFF
  07:00:00                                                                      

  2026-04-29   0.022    0.272       25.22       38.21         4.31     0.127    OFF
  08:00:00                                                                      

  2026-04-29   0        0.295       25.286      37.33         5.29     0        OFF
  09:00:00                                                                      

  2026-04-29   0.014    0.265       25.179      37.12         8.33     0.043    OFF
  10:00:00                                                                      

  2026-04-29   0        0.257       25.359      41.21         5.3      0        OFF
  11:00:00                                                                      

  2026-04-29   0.014    0.228       25.307      39.47         4.87     0.163    OFF
  12:00:00                                                                      

  2026-04-29   0        0.271       25.249      39.46         3.87     0        OFF
  13:00:00                                                                      

  2026-04-29   0.023    0.339       25.256      37.71         2.62     0.055    OFF
  14:00:00                                                                      

  2026-04-29   0.001    0.28        25.277      40.27         6        0.003    OFF
  15:00:00                                                                      

  2026-04-29   0.027    0.285       25.336      41.94         6.38     0.048    OFF
  16:00:00                                                                      

  2026-04-29   0.012    0.262       25.244      36.91         3.09     0.021    OFF
  17:00:00                                                                      

  2026-04-29   0        0.274       25.3        39.63         4.07     0        OFF
  18:00:00                                                                      

  2026-04-29   0.069    0.378       25.211      41.98         5.11     0.091    OFF
  19:00:00                                                                      

  2026-04-29   0.098    0.372       25.306      39.79         4.84     0        OFF
  20:00:00                                                                      

  2026-04-29   0        0.214       25.307      41.44         5.17     0        OFF
  21:00:00                                                                      

  2026-04-29   0        0.412       25.294      40.53         6.01     0.043    OFF
  22:00:00                                                                      

  2026-04-29   0.002    0.275       25.321      34.76         6.07     0.13     OFF
  23:00:00                                                                      

  2026-04-30   0.024    0.255       25.316      44.9          5        0        OFF
  00:00:00                                                                      

  2026-04-30   0.004    0.295       25.254      39.55         5.48     0        OFF
  01:00:00                                                                      

  2026-04-30   0        0.279       25.255      38.31         5.74     0        OFF
  02:00:00                                                                      

  2026-04-30   0        0.273       25.386      39.07         4.09     0        OFF
  03:00:00                                                                      

  2026-04-30   0.069    0.388       25.309      35.23         4.03     0.013    OFF
  04:00:00                                                                      

  2026-04-30   0.065    0.282       25.443      43.04         7.02     0.062    OFF
  05:00:00                                                                      

  2026-04-30   0.08     0.26        25.353      36.27         3.51     0.006    OFF
  06:00:00                                                                      

  2026-04-30   0        0.318       25.258      42.58         3.75     0.172    OFF
  07:00:00                                                                      

  2026-04-30   0        0.23        25.269      42.07         4.95     0        OFF
  08:00:00                                                                      

  2026-04-30   0        0.182       25.361      39.45         6.32     0        OFF
  09:00:00                                                                      

  2026-04-30   0.008    0.354       25.255      44.55         3.35     0.046    OFF
  10:00:00                                                                      

  2026-04-30   0.059    0.302       25.345      41.78         5.85     0.059    OFF
  11:00:00                                                                      

  2026-04-30   0        0.321       25.249      39.58         5.32     0.003    OFF
  12:00:00                                                                      

  2026-04-30   0        0.312       25.331      42.06         5.59     0        OFF
  13:00:00                                                                      

  2026-04-30   0.009    0.304       25.216      38.77         4.57     0        OFF
  14:00:00                                                                      

  2026-04-30   55.31    9.628       28.895      62.88         134.42   56.657   ON
  15:00:00                                                                      

  2026-04-30   54.877   9.49        28.94       66.35         136.12   57.55    ON
  16:00:00                                                                      

  2026-04-30   53.347   9.309       28.676      66.48         130.04   55.973   ON
  17:00:00                                                                      

  2026-04-30   54.727   9.464       28.638      62.47         134      56.177   ON
  18:00:00                                                                      

  2026-04-30   55.057   9.599       28.816      64.6          137.82   58.432   ON
  19:00:00                                                                      

  2026-04-30   56.76    9.515       28.714      67            132.8    57.518   ON
  20:00:00                                                                      

  2026-04-30   53.857   9.39        28.1        62.73         133.77   55.843   ON
  21:00:00                                                                      

  2026-04-30   56.675   9.613       28.96       65.61         133.13   55.023   ON
  22:00:00                                                                      

  2026-04-30   54.364   9.621       28.334      65.48         129.33   56.276   ON
  23:00:00                                                                      
  --------------------------------------------------------------------------------------

### PM4405B

Source pages: 68-101.

#### Data dictionary

  Name           Description                     Digital set    Engineering units   Span
  -------------- ------------------------------- -------------- ------------------- ------
  Name           Description                     digitalset     engunits            span
  PM4405B_FEED   PM-4405B FEED RATE              T/H (equiv.)   30                  
  PM4405B_DISP   PM-4405B DISCHARGE PRESSURE     BARG           20                  
  PM4405B_VIB    PM-4405B VIBRATION              MM/S           20                  
  PM4405B_TEMP   PM-4405B BEARING/PROCESS TEMP   DEG C          150                 
  PM4405B_AMP    PM-4405B MOTOR AMPERE           A              300                 
  PLANT_RATE     NUP PRODUCTION RATE             T/H (equiv.)   26                  
  RUN_STATUS     PM-4405B RUN STATUS             ON_OFF         ON_OFF              1

#### Typical value, zero, and instrument tag

## Typical value Zero Instrument tag --------------- ------

#### Hourly data

  --------------------------------------------------------------------------------------
  Timestamp    Feed     Discharge   Vibration   Temperature   Motor    Plant    Run
                        pressure                              ampere   rate     status
  ------------ -------- ----------- ----------- ------------- -------- -------- --------
  2026-07-01   20.173   9.42        3.343       66.36         138.7    20.076   ON
  00:00:00                                                                      

  2026-07-01   20.42    9.626       4.181       67.24         139.64   20.388   ON
  01:00:00                                                                      

  2026-07-01   19.962   9.569       4.06        67.19         135.97   20.686   ON
  02:00:00                                                                      

  2026-07-01   19.447   9.457       3.654       62.66         132.33   20.125   ON
  03:00:00                                                                      

  2026-07-01   19.985   9.722       3.99        66.83         129.87   19.904   ON
  04:00:00                                                                      

  2026-07-01   19.712   9.307       3.935       65.58         129.07   20.276   ON
  05:00:00                                                                      

  2026-07-01   20.511   9.75        3.49        65.9          131.8    20.049   ON
  06:00:00                                                                      

  2026-07-01   19.501   9.334       4.104       65.75         127.56   20.452   ON
  07:00:00                                                                      

  2026-07-01   20.347   9.425       3.963       66.06         133.83   19.881   ON
  08:00:00                                                                      

  2026-07-01   19.913   9.488       3.916       65.67         131.08   20.151   ON
  09:00:00                                                                      

  2026-07-01   20.163   9.623       4.08        65.32         132.38   20.661   ON
  10:00:00                                                                      

  2026-07-01   19.72    9.686       3.322       64.91         131.73   20.426   ON
  11:00:00                                                                      

  2026-07-01   20.214   9.263       3.775       64.07         138.06   19.956   ON
  12:00:00                                                                      

  2026-07-01   20.003   9.36        4.191       66.62         132.4    20.239   ON
  13:00:00                                                                      

  2026-07-01   19.933   9.394       4.123       64.85         131.83   20.442   ON
  14:00:00                                                                      

  2026-07-01   19.572   9.48        3.438       64.47         141.44   20.663   ON
  15:00:00                                                                      

  2026-07-01   19.78    9.378       3.963       66.3          133.7    19.985   ON
  16:00:00                                                                      

  2026-07-01   19.245   9.333       3.642       65.72         140.72   20.423   ON
  17:00:00                                                                      

  2026-07-01   20.213   9.733       3.9         64.82         133.32   19.997   ON
  18:00:00                                                                      

  2026-07-01   19.886   9.611       3.614       64.97         134.26   19.736   ON
  19:00:00                                                                      

  2026-07-01   20.603   9.506       4.148       62.17         135.97   20.77    ON
  20:00:00                                                                      

  2026-07-01   19.398   9.644       4.332       63.29         129.46   20.61    ON
  21:00:00                                                                      

  2026-07-01   20.64    9.467       4.075       64.41         141.09   20.635   ON
  22:00:00                                                                      

  2026-07-01   20.189   9.265       4.082       65.39         141.9    20.725   ON
  23:00:00                                                                      

  2026-07-02   19.822   9.216       3.864       65.54         133.28   20.269   ON
  00:00:00                                                                      

  2026-07-02   20.203   9.596       3.771       63.13         139.44   20.89    ON
  01:00:00                                                                      

  2026-07-02   19.497   9.492       4.191       64.23         136.03   20.713   ON
  02:00:00                                                                      

  2026-07-02   19.454   9.488       4.033       65.28         133.15   20.085   ON
  03:00:00                                                                      

  2026-07-02   20.496   9.348       3.894       66.24         141.54   20.202   ON
  04:00:00                                                                      

  2026-07-02   19.201   9.524       3.662       63.84         130.94   19.73    ON
  05:00:00                                                                      

  2026-07-02   20.012   9.539       3.542       63.67         134.83   19.576   ON
  06:00:00                                                                      

  2026-07-02   20.554   9.714       4.038       63.03         138.94   20.634   ON
  07:00:00                                                                      

  2026-07-02   20.054   9.7         4.036       64.85         134.11   20.598   ON
  08:00:00                                                                      

  2026-07-02   20.544   9.407       3.824       65.39         136.85   20.042   ON
  09:00:00                                                                      

  2026-07-02   19.919   9.786       3.845       66.42         129.85   20.616   ON
  10:00:00                                                                      

  2026-07-02   19.736   9.647       3.463       64.59         134.21   20.36    ON
  11:00:00                                                                      

  2026-07-02   20.477   9.739       3.644       66.34         135.44   19.79    ON
  12:00:00                                                                      

  2026-07-02   20.365   9.479       3.579       65.07         129.95   20.6     ON
  13:00:00                                                                      

  2026-07-02   19.975   9.663       3.958       65.3          131.66   20.572   ON
  14:00:00                                                                      

  2026-07-02   20.566   9.262       3.772       63.12         132.45   20.593   ON
  15:00:00                                                                      

  2026-07-02   19.551   9.689       3.82        67.52         133.93   20.077   ON
  16:00:00                                                                      

  2026-07-02   20.426   9.392       3.637       64.67         135.81   19.803   ON
  17:00:00                                                                      

  2026-07-02   19.849   9.571       3.84        66.76         133.66   20.524   ON
  18:00:00                                                                      

  2026-07-02   20.101   9.403       3.407       65.96         128.45   20.821   ON
  19:00:00                                                                      

  2026-07-02   20.053   9.507       4.257       64.5          135.19   21.712   ON
  20:00:00                                                                      

  2026-07-02   20.084   9.517       3.829       64.08         140.2    19.567   ON
  21:00:00                                                                      

  2026-07-02   20.225   9.306       3.944       66.08         135.05   20.2     ON
  22:00:00                                                                      

  2026-07-02   20.582   9.528       3.931       64.09         133.45   20.76    ON
  23:00:00                                                                      

  2026-07-03   20.579   9.656       3.611       63.78         134.93   20.612   ON
  00:00:00                                                                      

  2026-07-03   20.05    9.521       4.163       63.77         137.42   20.806   ON
  01:00:00                                                                      

  2026-07-03   20.041   9.684       3.865       63.74         129.52   19.865   ON
  02:00:00                                                                      

  2026-07-03   19.618   9.862       3.785       63.93         141.33   19.888   ON
  03:00:00                                                                      

  2026-07-03   20.681   9.527       4.079       67.11         133.81   20.652   ON
  04:00:00                                                                      

  2026-07-03   20.389   9.72        3.598       65.07         142.61   19.555   ON
  05:00:00                                                                      

  2026-07-03   19.765   9.536       3.987       66.61         132.28   20.172   ON
  06:00:00                                                                      

  2026-07-03   20.09    9.332       4.264       65.6          131.06   19.739   ON
  07:00:00                                                                      

  2026-07-03   20.624   9.63        3.703       64.76         135.8    20.432   ON
  08:00:00                                                                      

  2026-07-03   19.736   9.321       3.937       64.42         138.96   20.276   ON
  09:00:00                                                                      

  2026-07-03   20.128   9.515       3.494       63.39         136.98   20.98    ON
  10:00:00                                                                      

  2026-07-03   20.015   9.86        3.886       65.39         135.83   20.27    ON
  11:00:00                                                                      

  2026-07-03   19.902   9.4         3.896       65            136.26   20.922   ON
  12:00:00                                                                      

  2026-07-03   20.05    9.334       3.418       64.98         135.89   20.507   ON
  13:00:00                                                                      

  2026-07-03   19.215   9.45        4.23        64.78         139.43   20.243   ON
  14:00:00                                                                      

  2026-07-03   20.416   9.575       4.335       65.74         134.85   19.797   ON
  15:00:00                                                                      

  2026-07-03   19.834   9.639       3.355       64.14         137.79   20.612   ON
  16:00:00                                                                      

  2026-07-03   20.067   9.417       3.931       63.07         132.85   20.142   ON
  17:00:00                                                                      

  2026-07-03   19.45    9.41        3.721       64.03         134.42   21.097   ON
  18:00:00                                                                      

  2026-07-03   20.948   9.6         3.761       62.32         132.07   20.344   ON
  19:00:00                                                                      

  2026-07-03   20.249   9.495       3.927       65.27         133.96   20.598   ON
  20:00:00                                                                      

  2026-07-03   19.235   9.665       3.838       67.28         133.02   20.657   ON
  21:00:00                                                                      

  2026-07-03   19.769   9.381       3.773       64.25         129.09   19.376   ON
  22:00:00                                                                      

  2026-07-03   19.88    9.725       3.894       66.38         139      20.125   ON
  23:00:00                                                                      

  2026-07-04   19.621   9.55        3.725       67.89         136.59   20.455   ON
  00:00:00                                                                      

  2026-07-04   19.466   9.499       3.878       64.6          137.3    20.579   ON
  01:00:00                                                                      

  2026-07-04   19.481   9.258       3.655       65.73         144.21   20.359   ON
  02:00:00                                                                      

  2026-07-04   19.665   9.457       4.043       66.01         126.94   20.982   ON
  03:00:00                                                                      

  2026-07-04   20.072   9.491       4.323       67.33         136.73   20.782   ON
  04:00:00                                                                      

  2026-07-04   20.102   9.682       3.829       65.55         135.64   20.758   ON
  05:00:00                                                                      

  2026-07-04   20.519   9.533       3.747       63.93         139.51   20.913   ON
  06:00:00                                                                      

  2026-07-04   19.939   9.351       4.16        64.13         132.76   19.829   ON
  07:00:00                                                                      

  2026-07-04   19.102   9.293       3.33        63.55         133.15   20.779   ON
  08:00:00                                                                      

  2026-07-04   19.946   9.644       3.777       64.68         130.77   20.328   ON
  09:00:00                                                                      

  2026-07-04   20.443   9.326       3.537       65.94         137.87   19.826   ON
  10:00:00                                                                      

  2026-07-04   19.529   9.775       3.682       65.86         142.6    20.703   ON
  11:00:00                                                                      

  2026-07-04   20.076   9.546       3.554       64.2          132.07   20.966   ON
  12:00:00                                                                      

  2026-07-04   20.135   9.427       3.747       65.8          135.7    20.798   ON
  13:00:00                                                                      

  2026-07-04   19.593   9.378       4.123       62.44         136.11   20.648   ON
  14:00:00                                                                      

  2026-07-04   19.92    9.721       3.606       64.86         132.49   20.245   ON
  15:00:00                                                                      

  2026-07-04   19.594   9.483       3.763       66.9          127.28   21.188   ON
  16:00:00                                                                      

  2026-07-04   20.583   9.532       4.1         64.81         138.65   20.649   ON
  17:00:00                                                                      

  2026-07-04   20.264   9.195       3.945       64.35         128.38   20.254   ON
  18:00:00                                                                      

  2026-07-04   20.025   9.528       4.001       66.82         139.4    19.981   ON
  19:00:00                                                                      

  2026-07-04   20.28    9.347       3.785       66.97         129.82   20.382   ON
  20:00:00                                                                      

  2026-07-04   20.275   9.153       3.686       65.08         138.88   19.734   ON
  21:00:00                                                                      

  2026-07-04   19.658   9.468       3.702       61.93         140.22   20.783   ON
  22:00:00                                                                      

  2026-07-04   19.474   9.484       3.718       66.05         133.04   20.808   ON
  23:00:00                                                                      

  2026-07-05   19.427   9.312       3.486       67.75         130.42   20.283   ON
  00:00:00                                                                      

  2026-07-05   19.492   9.94        3.226       63.7          134.39   19.799   ON
  01:00:00                                                                      

  2026-07-05   20.332   9.323       3.681       68.45         134.93   20.13    ON
  02:00:00                                                                      

  2026-07-05   20.444   9.365       3.866       63.71         130.3    21.099   ON
  03:00:00                                                                      

  2026-07-05   20.615   9.546       3.67        66.63         133.8    21.046   ON
  04:00:00                                                                      

  2026-07-05   19.467   9.552       4.082       66.47         138.55   20.665   ON
  05:00:00                                                                      

  2026-07-05   20       9.546       4.099       66.23         137.41   21.05    ON
  06:00:00                                                                      

  2026-07-05   20.495   9.462       3.83        63.9          139.68   20.8     ON
  07:00:00                                                                      

  2026-07-05   20.72    9.741       3.726       66.23         129.07   20.221   ON
  08:00:00                                                                      

  2026-07-05   19.871   9.377       3.92        62.92         131.51   20.127   ON
  09:00:00                                                                      

  2026-07-05   19.854   9.216       3.681       65.02         134.52   20.686   ON
  10:00:00                                                                      

  2026-07-05   19.849   9.341       3.754       64.98         134.37   20.873   ON
  11:00:00                                                                      

  2026-07-05   20.179   9.479       3.598       65.12         138.37   19.554   ON
  12:00:00                                                                      

  2026-07-05   20.326   9.515       3.645       63.34         129.92   20.415   ON
  13:00:00                                                                      

  2026-07-05   20.4     9.812       3.953       63.92         141.18   20.004   ON
  14:00:00                                                                      

  2026-07-05   19.824   9.489       3.706       62.37         139.33   19.668   ON
  15:00:00                                                                      

  2026-07-05   20.592   9.431       3.932       67.68         137.9    20.142   ON
  16:00:00                                                                      

  2026-07-05   19.603   9.418       3.809       65.39         133.67   20.426   ON
  17:00:00                                                                      

  2026-07-05   20.26    9.375       3.828       64.03         128.72   20.519   ON
  18:00:00                                                                      

  2026-07-05   20.55    9.615       3.892       65.44         129.35   20.469   ON
  19:00:00                                                                      

  2026-07-05   20.456   9.317       3.261       65.01         138.61   20.656   ON
  20:00:00                                                                      

  2026-07-05   20.184   9.716       3.703       67.4          134.26   20.252   ON
  21:00:00                                                                      

  2026-07-05   19.856   9.356       3.883       64.18         142.14   19.961   ON
  22:00:00                                                                      

  2026-07-05   19.979   9.399       4.171       66.75         136.1    21.232   ON
  23:00:00                                                                      

  2026-07-06   19.718   9.51        3.941       62.88         129.51   21.271   ON
  00:00:00                                                                      

  2026-07-06   19.736   9.248       4.445       64.85         139.61   19.927   ON
  01:00:00                                                                      

  2026-07-06   19.611   9.523       4.135       65.75         133.99   20.002   ON
  02:00:00                                                                      

  2026-07-06   20.455   9.499       3.848       64.68         135.31   19.897   ON
  03:00:00                                                                      

  2026-07-06   19.538   9.711       3.493       66.5          137.65   20.435   ON
  04:00:00                                                                      

  2026-07-06   19.73    9.615       3.738       65.28         129.25   20.395   ON
  05:00:00                                                                      

  2026-07-06   20.55    9.126       3.758       64.16         130.25   20.072   ON
  06:00:00                                                                      

  2026-07-06   20.169   9.559       3.835       64.3          140.61   20.464   ON
  07:00:00                                                                      

  2026-07-06   20.708   9.346       3.907       67            129.25   20.504   ON
  08:00:00                                                                      

  2026-07-06   20.642   9.35        3.483       65.02         130.21   20.595   ON
  09:00:00                                                                      

  2026-07-06   20.189   9.371       3.937       64.54         129.66   20.386   ON
  10:00:00                                                                      

  2026-07-06   20.462   9.813       3.741       62.66         129.85   20.22    ON
  11:00:00                                                                      

  2026-07-06   19.568   9.435       3.646       62.89         133.09   20.428   ON
  12:00:00                                                                      

  2026-07-06   20.117   9.503       3.491       63.62         132.76   19.6     ON
  13:00:00                                                                      

  2026-07-06   20.724   9.642       3.862       66.19         130.5    20.29    ON
  14:00:00                                                                      

  2026-07-06   20.21    9.785       3.682       67.36         132.47   19.674   ON
  15:00:00                                                                      

  2026-07-06   20.142   9.442       3.249       65.02         136.1    20.498   ON
  16:00:00                                                                      

  2026-07-06   21.114   9.524       3.825       69.46         126.25   20.582   ON
  17:00:00                                                                      

  2026-07-06   20.355   9.542       3.759       67.08         133.07   20.387   ON
  18:00:00                                                                      

  2026-07-06   19.449   9.515       3.395       67.37         133.96   20.297   ON
  19:00:00                                                                      

  2026-07-06   20.492   9.469       3.965       67.88         127.71   21.171   ON
  20:00:00                                                                      

  2026-07-06   19.019   9.325       3.737       66.69         139.44   20.969   ON
  21:00:00                                                                      

  2026-07-06   20.23    9.421       3.903       69.77         135.41   20.886   ON
  22:00:00                                                                      

  2026-07-06   20.186   9.377       3.498       68.91         134.09   20.447   ON
  23:00:00                                                                      

  2026-07-07   19.845   9.346       3.671       70.03         136.9    20.779   ON
  00:00:00                                                                      

  2026-07-07   19.717   9.417       3.897       67.01         136.03   20.343   ON
  01:00:00                                                                      

  2026-07-07   19.858   9.49        3.971       67.77         133.64   20.752   ON
  02:00:00                                                                      

  2026-07-07   21.126   9.396       3.632       71.35         133.64   19.685   ON
  03:00:00                                                                      

  2026-07-07   19.59    9.439       3.147       72.69         129.95   20.635   ON
  04:00:00                                                                      

  2026-07-07   19.708   9.64        3.858       70.59         136.31   19.756   ON
  05:00:00                                                                      

  2026-07-07   19.956   9.615       3.749       70.91         135.46   20.409   ON
  06:00:00                                                                      

  2026-07-07   19.871   9.35        4.149       71.57         130.58   20.509   ON
  07:00:00                                                                      

  2026-07-07   20.724   9.22        3.549       71.32         137.21   20.975   ON
  08:00:00                                                                      

  2026-07-07   20.168   9.892       3.919       70.74         140.72   20.353   ON
  09:00:00                                                                      

  2026-07-07   19.972   9.47        3.436       71.16         129.66   20.156   ON
  10:00:00                                                                      

  2026-07-07   20.335   9.773       3.876       75.14         141.95   20.643   ON
  11:00:00                                                                      

  2026-07-07   20.161   9.492       3.712       72.7          139.64   20.721   ON
  12:00:00                                                                      

  2026-07-07   19.963   9.775       3.857       75.06         138.9    20.55    ON
  13:00:00                                                                      

  2026-07-07   19.914   9.568       3.785       72.02         134.24   20.27    ON
  14:00:00                                                                      

  2026-07-07   19.978   9.489       3.758       75.52         141.71   20.635   ON
  15:00:00                                                                      

  2026-07-07   19.979   9.414       4.192       76.92         133.8    19.971   ON
  16:00:00                                                                      

  2026-07-07   19.87    9.475       4.094       74.97         137.33   20.428   ON
  17:00:00                                                                      

  2026-07-07   20.012   9.36        3.804       77.35         132.71   20.161   ON
  18:00:00                                                                      

  2026-07-07   20.548   9.546       3.572       76.65         129.78   20.739   ON
  19:00:00                                                                      

  2026-07-07   19.535   9.494       3.598       80.19         137.41   20.069   ON
  20:00:00                                                                      

  2026-07-07   20.193   9.583       4.067       76.62         140.37   20.946   ON
  21:00:00                                                                      

  2026-07-07   20.334   9.585       3.813       76.99         129.66   21.062   ON
  22:00:00                                                                      

  2026-07-07   20       9.332       3.621       76.14         134.73   20.425   ON
  23:00:00                                                                      

  2026-07-08   20.023   9.548       3.635       77.91         132.22   19.899   ON
  00:00:00                                                                      

  2026-07-08   20.494   9.506       4.142       79.55         131.04   20.593   ON
  01:00:00                                                                      

  2026-07-08   19.87    9.666       3.833       77.7          133.33   20.259   ON
  02:00:00                                                                      

  2026-07-08   20.278   9.754       3.583       81.2          138.9    20.452   ON
  03:00:00                                                                      

  2026-07-08   20.255   9.439       4.18        78.76         140.67   20.619   ON
  04:00:00                                                                      

  2026-07-08   20.117   9.174       3.896       80.3          136.79   20.616   ON
  05:00:00                                                                      

  2026-07-08   20.124   9.493       3.455       82.35         135.36   20.537   ON
  06:00:00                                                                      

  2026-07-08   20.37    9.491       3.49        79.85         137.77   19.724   ON
  07:00:00                                                                      

  2026-07-08   20.623   9.346       3.88        81.33         131.32   20.42    ON
  08:00:00                                                                      

  2026-07-08   19.61    9.563       3.617       81.08         135.74   20.085   ON
  09:00:00                                                                      

  2026-07-08   20.455   9.463       3.692       80.7          132.88   20.552   ON
  10:00:00                                                                      

  2026-07-08   19.766   9.601       4.254       83.04         135.93   19.317   ON
  11:00:00                                                                      

  2026-07-08   19.683   9.305       4.292       79.37         128.13   20.013   ON
  12:00:00                                                                      

  2026-07-08   20.112   9.541       4.254       81.4          136.89   20.147   ON
  13:00:00                                                                      

  2026-07-08   0.061    0.265       0.268       40.15         6.01     0        OFF
  14:00:00                                                                      

  2026-07-08   0.03     0.189       0.292       41.63         6.18     0        OFF
  15:00:00                                                                      

  2026-07-08   0.022    0.312       0.286       38.83         4.39     0        OFF
  16:00:00                                                                      

  2026-07-08   0        0.259       0.396       39.65         5.64     0.03     OFF
  17:00:00                                                                      

  2026-07-08   0.074    0.279       0.363       39.68         4.1      0        OFF
  18:00:00                                                                      

  2026-07-08   0        0.285       0.21        38.31         5.26     0.104    OFF
  19:00:00                                                                      

  2026-07-08   0        0.326       0.271       42.64         5.19     0.057    OFF
  20:00:00                                                                      

  2026-07-08   0        0.226       0.345       42.4          5.83     0        OFF
  21:00:00                                                                      

  2026-07-08   20.161   9.387       3.927       66.77         132.8    21.067   ON
  22:00:00                                                                      

  2026-07-08   20.069   9.144       3.964       65.55         139.19   20.715   ON
  23:00:00                                                                      

  2026-07-09   19.899   9.715       3.873       63.12         139.21   20.248   ON
  00:00:00                                                                      

  2026-07-09   20.485   9.75        4.137       65.07         130.24   20.968   ON
  01:00:00                                                                      

  2026-07-09   20.1     9.511       3.535       66.56         131.31   20.9     ON
  02:00:00                                                                      

  2026-07-09   20.178   9.34        4.306       62.63         130.02   19.632   ON
  03:00:00                                                                      

  2026-07-09   19.811   9.222       3.959       64.18         141.32   20.447   ON
  04:00:00                                                                      

  2026-07-09   19.783   9.543       3.474       65.16         127.74   20.286   ON
  05:00:00                                                                      

  2026-07-09   20.107   9.729       3.88        65.08         130.98   20.323   ON
  06:00:00                                                                      

  2026-07-09   19.472   9.262       4.241       64.14         136.41   21.129   ON
  07:00:00                                                                      

  2026-07-09   20.609   9.486       3.658       65.36         139.52   20.917   ON
  08:00:00                                                                      

  2026-07-09   19.885   9.735       3.943       65.6          139.43   21.306   ON
  09:00:00                                                                      

  2026-07-09   19.909   9.616       3.793       67.81         136.48   20.831   ON
  10:00:00                                                                      

  2026-07-09   19.837   9.465       4.178       63.86         137.56   20.422   ON
  11:00:00                                                                      

  2026-07-09   20.088   9.81        3.869       65.01         139.36   20.118   ON
  12:00:00                                                                      

  2026-07-09   20.242   9.294       3.656       63.45         136.8    20.634   ON
  13:00:00                                                                      

  2026-07-09   20.318   9.573       3.925       66.71         134.1    20.698   ON
  14:00:00                                                                      

  2026-07-09   19.769   9.655       3.931       65.63         135.95   20.353   ON
  15:00:00                                                                      

  2026-07-09   19.591   9.283       3.838       65.93         137.34   20.257   ON
  16:00:00                                                                      

  2026-07-09   19.98    9.416       3.673       65.75         137.53   20.752   ON
  17:00:00                                                                      

  2026-07-09   19.983   9.428       3.459       67.73         135.84   20.476   ON
  18:00:00                                                                      

  2026-07-09   19.739   9.921       3.801       64.56         131.62   21.22    ON
  19:00:00                                                                      

  2026-07-09   20.522   9.483       3.406       65.45         135.34   20.225   ON
  20:00:00                                                                      

  2026-07-09   19.623   9.476       3.595       65.86         137.57   20.69    ON
  21:00:00                                                                      

  2026-07-09   19.682   9.407       3.829       63.44         130.65   20.568   ON
  22:00:00                                                                      

  2026-07-09   20.405   9.892       4.078       62.71         132.06   21.392   ON
  23:00:00                                                                      

  2026-07-10   19.873   9.805       4.033       66.28         136.73   20.351   ON
  00:00:00                                                                      

  2026-07-10   19.952   9.359       3.372       65.22         137.64   20.21    ON
  01:00:00                                                                      

  2026-07-10   19.69    9.378       4.053       66.24         134.11   20.54    ON
  02:00:00                                                                      

  2026-07-10   19.534   9.587       3.292       65            134.08   20.336   ON
  03:00:00                                                                      

  2026-07-10   19.734   9.527       3.864       64.73         135.32   20.997   ON
  04:00:00                                                                      

  2026-07-10   19.35    9.554       3.835       64.71         133.26   20.805   ON
  05:00:00                                                                      

  2026-07-10   20.311   9.383       4.031       65.37         133.09   20.617   ON
  06:00:00                                                                      

  2026-07-10   20.14    9.215       3.854       64.53         127.84   20.433   ON
  07:00:00                                                                      

  2026-07-10   20.776   9.52        4.073       64.46         134.07   19.492   ON
  08:00:00                                                                      

  2026-07-10   19.99    9.349       3.659       66.94         141.54   19.952   ON
  09:00:00                                                                      

  2026-07-10   19.808   9.901       3.781       66.62         132.25   20.229   ON
  10:00:00                                                                      

  2026-07-10   20.422   9.527       4.029       65.03         132.67   20.01    ON
  11:00:00                                                                      

  2026-07-10   19.816   9.541       3.678       67.47         136.89   20.73    ON
  12:00:00                                                                      

  2026-07-10   20.419   9.564       3.675       64.32         138.01   21.119   ON
  13:00:00                                                                      

  2026-07-10   19.827   9.403       3.828       66.44         143.93   20.187   ON
  14:00:00                                                                      

  2026-07-10   19.306   9.531       3.425       66.68         133.17   19.999   ON
  15:00:00                                                                      

  2026-07-10   19.886   9.329       3.752       64.7          136.98   20.478   ON
  16:00:00                                                                      

  2026-07-10   19.899   9.501       3.556       67.55         130.84   21.113   ON
  17:00:00                                                                      

  2026-07-10   20.229   9.574       4.177       63.42         131.65   20.341   ON
  18:00:00                                                                      

  2026-07-10   19.843   9.505       4.124       65.02         132.25   20.088   ON
  19:00:00                                                                      

  2026-07-10   20.12    9.068       3.987       64.26         134.67   20.594   ON
  20:00:00                                                                      

  2026-07-10   20.116   9.589       4.357       67.22         136.94   19.885   ON
  21:00:00                                                                      

  2026-07-10   19.675   9.379       3.863       65.59         136.05   19.979   ON
  22:00:00                                                                      

  2026-07-10   19.58    9.65        3.72        63.98         131.65   20.533   ON
  23:00:00                                                                      

  2026-07-11   19.725   9.514       3.897       64.87         135.04   19.944   ON
  00:00:00                                                                      

  2026-07-11   19.375   9.497       3.889       64            130.44   20.374   ON
  01:00:00                                                                      

  2026-07-11   20.049   9.575       3.741       66.69         132.64   20.325   ON
  02:00:00                                                                      

  2026-07-11   20.268   9.4         3.902       63.92         130.33   19.945   ON
  03:00:00                                                                      

  2026-07-11   19.889   9.508       3.511       63.93         133.94   20.637   ON
  04:00:00                                                                      

  2026-07-11   19.761   9.445       3.568       65.65         136.35   21.233   ON
  05:00:00                                                                      

  2026-07-11   19.551   9.587       3.88        64.36         143.49   20.642   ON
  06:00:00                                                                      

  2026-07-11   20.266   9.641       3.504       65.42         132.14   20.122   ON
  07:00:00                                                                      

  2026-07-11   20.431   9.374       4.089       65.26         137.21   20.238   ON
  08:00:00                                                                      

  2026-07-11   19.16    9.434       3.918       64.32         136.01   20.658   ON
  09:00:00                                                                      

  2026-07-11   20.817   9.377       3.661       62.85         133.77   20.288   ON
  10:00:00                                                                      

  2026-07-11   20.618   9.781       4.088       61.92         132.38   20.202   ON
  11:00:00                                                                      

  2026-07-11   19.804   9.381       3.871       65.23         130.5    20.117   ON
  12:00:00                                                                      

  2026-07-11   20.009   9.49        4.224       64.57         135.57   20.443   ON
  13:00:00                                                                      

  2026-07-11   20.074   9.466       3.76        65.82         132.33   20.49    ON
  14:00:00                                                                      

  2026-07-11   20.165   9.359       3.678       65.3          134.76   20.315   ON
  15:00:00                                                                      

  2026-07-11   19.869   9.586       3.921       64.92         138.56   20.65    ON
  16:00:00                                                                      

  2026-07-11   20.172   9.459       3.555       64.52         128.75   20.739   ON
  17:00:00                                                                      

  2026-07-11   20.264   9.663       4.068       66.29         140.71   20.993   ON
  18:00:00                                                                      

  2026-07-11   20.973   9.36        3.905       60.4          132.18   20.541   ON
  19:00:00                                                                      

  2026-07-11   19.985   9.555       3.001       62.51         137.37   20.578   ON
  20:00:00                                                                      

  2026-07-11   19.759   9.844       3.802       65.68         136.51   20.61    ON
  21:00:00                                                                      

  2026-07-11   20.406   9.64        3.858       64.81         134.31   20.273   ON
  22:00:00                                                                      

  2026-07-11   20.002   9.501       3.502       63.81         136.8    20.758   ON
  23:00:00                                                                      

  2026-07-12   20.072   9.643       3.731       64.24         140.22   19.69    ON
  00:00:00                                                                      

  2026-07-12   20.048   9.317       3.724       66.17         135.19   20.656   ON
  01:00:00                                                                      

  2026-07-12   19.872   9.578       3.311       65.62         139.23   20.203   ON
  02:00:00                                                                      

  2026-07-12   19.838   9.56        3.872       65.21         142.67   20.509   ON
  03:00:00                                                                      

  2026-07-12   19.826   9.583       3.792       62.45         135.45   20.963   ON
  04:00:00                                                                      

  2026-07-12   19.715   9.586       3.635       66.44         131.72   20.898   ON
  05:00:00                                                                      

  2026-07-12   19.841   9.614       3.702       63.96         133.44   21.173   ON
  06:00:00                                                                      

  2026-07-12   20.728   9.41        3.816       65.86         136.47   19.307   ON
  07:00:00                                                                      

  2026-07-12   19.987   9.423       4.076       65.73         138.82   20.78    ON
  08:00:00                                                                      

  2026-07-12   19.706   9.344       3.919       62.52         127.5    20.335   ON
  09:00:00                                                                      

  2026-07-12   19.623   9.579       3.74        62.97         134.29   20.933   ON
  10:00:00                                                                      

  2026-07-12   20.477   9.226       3.714       62.74         132.61   20.162   ON
  11:00:00                                                                      

  2026-07-12   19.776   9.485       3.68        63.51         141.76   20.631   ON
  12:00:00                                                                      

  2026-07-12   20.074   9.375       4.044       65.94         131.25   20.15    ON
  13:00:00                                                                      

  2026-07-12   19.337   9.532       3.894       66.69         137.33   20.261   ON
  14:00:00                                                                      

  2026-07-12   19.201   9.844       3.676       65.36         135.3    19.858   ON
  15:00:00                                                                      

  2026-07-12   20.108   9.419       4.141       64.7          138.52   20.455   ON
  16:00:00                                                                      

  2026-07-12   19.358   9.667       4.006       63.91         141.87   20.198   ON
  17:00:00                                                                      

  2026-07-12   20.094   9.715       3.597       67.21         133.9    20.224   ON
  18:00:00                                                                      

  2026-07-12   20.344   9.328       3.938       64.97         129.82   21.132   ON
  19:00:00                                                                      

  2026-07-12   19.683   9.476       3.856       63.75         140.41   20.081   ON
  20:00:00                                                                      

  2026-07-12   19.809   9.539       3.903       65.02         132.25   20.87    ON
  21:00:00                                                                      

  2026-07-12   19.833   9.373       3.986       65.82         135.61   20.313   ON
  22:00:00                                                                      

  2026-07-12   19.73    9.435       3.725       64.36         137.73   20.317   ON
  23:00:00                                                                      

  2026-07-13   19.849   9.467       3.679       64.31         129      20.498   ON
  00:00:00                                                                      

  2026-07-13   19.835   9.526       3.534       62.73         132.68   20.248   ON
  01:00:00                                                                      

  2026-07-13   19.916   9.42        3.882       65.75         135.89   21.479   ON
  02:00:00                                                                      

  2026-07-13   20.023   9.675       3.788       63.9          132.49   20.056   ON
  03:00:00                                                                      

  2026-07-13   20.201   9.586       3.375       65.9          142.2    20.284   ON
  04:00:00                                                                      

  2026-07-13   20.181   9.49        3.817       65.16         129.75   20.455   ON
  05:00:00                                                                      

  2026-07-13   20.024   9.547       3.905       65.27         138.27   20.865   ON
  06:00:00                                                                      

  2026-07-13   19.702   9.241       3.85        64.01         132.65   20.699   ON
  07:00:00                                                                      

  2026-07-13   20.195   9.273       3.737       65.64         135.28   20.643   ON
  08:00:00                                                                      

  2026-07-13   20.311   9.297       3.991       63.28         132.09   20.291   ON
  09:00:00                                                                      

  2026-07-13   20.059   9.531       3.668       65.21         136.9    20.483   ON
  10:00:00                                                                      

  2026-07-13   19.86    9.727       3.437       67.24         139.41   20.921   ON
  11:00:00                                                                      

  2026-07-13   20.831   9.427       4.182       68.28         137.08   20.995   ON
  12:00:00                                                                      

  2026-07-13   19.142   9.327       3.449       63.41         134.59   20.059   ON
  13:00:00                                                                      

  2026-07-13   20.244   9.358       3.881       65.72         126      19.514   ON
  14:00:00                                                                      

  2026-07-13   20.092   9.531       4.249       65.06         135.86   20.853   ON
  15:00:00                                                                      

  2026-07-13   20.584   9.303       3.691       64.47         127.04   20.504   ON
  16:00:00                                                                      

  2026-07-13   20.716   9.366       4.112       66.16         138.88   20.585   ON
  17:00:00                                                                      

  2026-07-13   20.254   9.601       3.756       63.07         130.64   20.021   ON
  18:00:00                                                                      

  2026-07-13   19.833   9.686       3.745       65.86         127.6    20.587   ON
  19:00:00                                                                      

  2026-07-13   20.227   9.517       3.373       63.68         128.59   20.631   ON
  20:00:00                                                                      

  2026-07-13   19.564   9.496       3.975       66.99         134.97   21.016   ON
  21:00:00                                                                      

  2026-07-13   20.042   9.452       3.653       65.44         131.55   21.389   ON
  22:00:00                                                                      

  2026-07-13   19.715   9.586       4           68.66         135.19   20.537   ON
  23:00:00                                                                      

  2026-07-14   20.198   9.059       3.593       66.83         129.84   20.531   ON
  00:00:00                                                                      

  2026-07-14   19.335   9.53        3.843       65.31         137.84   20.457   ON
  01:00:00                                                                      

  2026-07-14   19.879   9.53        3.849       63.06         140.89   20.526   ON
  02:00:00                                                                      

  2026-07-14   20.085   9.448       4.143       61.42         135.16   19.511   ON
  03:00:00                                                                      

  2026-07-14   19.923   9.445       4.018       65.32         130.83   20.264   ON
  04:00:00                                                                      

  2026-07-14   19.878   9.561       3.523       64.54         129.61   20.264   ON
  05:00:00                                                                      

  2026-07-14   19.721   9.426       4.045       66.45         131.62   21.126   ON
  06:00:00                                                                      

  2026-07-14   19.915   9.595       3.782       63.73         139.11   20.774   ON
  07:00:00                                                                      

  2026-07-14   20.571   9.379       3.641       65.13         132.24   20.163   ON
  08:00:00                                                                      

  2026-07-14   19.784   9.559       3.697       63.99         128.58   20.214   ON
  09:00:00                                                                      

  2026-07-14   19.515   9.635       4.051       65.58         145.24   20.138   ON
  10:00:00                                                                      

  2026-07-14   19.614   9.344       3.413       65.53         141.19   19.904   ON
  11:00:00                                                                      

  2026-07-14   19.842   9.65        3.688       62.86         140.73   20.655   ON
  12:00:00                                                                      

  2026-07-14   20.275   9.559       3.538       65.01         132.16   20.79    ON
  13:00:00                                                                      

  2026-07-14   19.906   9.541       3.813       66.6          137.97   20.273   ON
  14:00:00                                                                      

  2026-07-14   20.307   9.696       3.739       65.58         131.17   19.619   ON
  15:00:00                                                                      

  2026-07-14   20.539   9.566       3.518       66.86         132.88   20.418   ON
  16:00:00                                                                      

  2026-07-14   19.672   9.367       3.746       63.81         137.28   20.765   ON
  17:00:00                                                                      

  2026-07-14   20.096   9.596       3.757       62.46         130.26   20.301   ON
  18:00:00                                                                      

  2026-07-14   19.895   9.672       3.717       63.84         134.74   19.925   ON
  19:00:00                                                                      

  2026-07-14   20.364   9.447       3.83        63.25         129.56   20.324   ON
  20:00:00                                                                      

  2026-07-14   20.322   9.462       4.093       67.44         138.33   21.326   ON
  21:00:00                                                                      

  2026-07-14   20.155   9.46        3.801       65.2          133.19   20.54    ON
  22:00:00                                                                      

  2026-07-14   19.58    9.429       3.816       66.32         135.38   20.679   ON
  23:00:00                                                                      

  2026-07-15   19.875   9.379       3.958       67.29         135.68   20.112   ON
  00:00:00                                                                      

  2026-07-15   19.973   9.613       3.745       65.35         131.39   20.498   ON
  01:00:00                                                                      

  2026-07-15   19.975   9.664       3.746       61.91         132.34   20.009   ON
  02:00:00                                                                      

  2026-07-15   19.768   9.304       3.653       61.63         131.52   20.616   ON
  03:00:00                                                                      

  2026-07-15   20.102   9.479       3.636       66.05         124.8    19.724   ON
  04:00:00                                                                      

  2026-07-15   20.173   9.454       3.62        66.23         135.45   19.768   ON
  05:00:00                                                                      

  2026-07-15   20.127   9.61        3.841       63.37         138.31   21.2     ON
  06:00:00                                                                      

  2026-07-15   19.707   9.661       3.213       65.69         139.13   20.257   ON
  07:00:00                                                                      

  2026-07-15   19.855   9.563       3.679       65.84         134.5    20.772   ON
  08:00:00                                                                      

  2026-07-15   19.559   9.677       3.84        65.17         138.06   20.196   ON
  09:00:00                                                                      

  2026-07-15   19.724   9.64        4.047       63.07         131.12   20.784   ON
  10:00:00                                                                      

  2026-07-15   20.238   9.601       4.155       66.73         133.75   19.975   ON
  11:00:00                                                                      

  2026-07-15   19.923   9.579       3.414       63.5          126.98   19.95    ON
  12:00:00                                                                      

  2026-07-15   19.937   9.664       3.627       65.73         132.24   20.891   ON
  13:00:00                                                                      

  2026-07-15   20.413   9.423       3.764       62.85         136.61   20.66    ON
  14:00:00                                                                      

  2026-07-15   19.785   9.336       3.36        63.67         128.64   19.529   ON
  15:00:00                                                                      

  2026-07-15   20.007   9.632       3.615       66.21         134.42   20.059   ON
  16:00:00                                                                      

  2026-07-15   19.442   9.644       3.824       63.47         144.23   20.435   ON
  17:00:00                                                                      

  2026-07-15   20.352   9.749       3.727       62.66         138.29   21.07    ON
  18:00:00                                                                      

  2026-07-15   19.935   9.491       3.334       64.8          135.28   20.483   ON
  19:00:00                                                                      

  2026-07-15   20.306   9.332       3.969       64.7          140.02   20.435   ON
  20:00:00                                                                      

  2026-07-15   20.297   9.562       3.566       63.27         137.9    19.888   ON
  21:00:00                                                                      

  2026-07-15   19.987   9.72        3.796       65.49         132.85   20.945   ON
  22:00:00                                                                      

  2026-07-15   20.214   9.416       3.374       65.82         146.67   20.791   ON
  23:00:00                                                                      

  2026-07-16   19.45    9.483       3.77        65.3          138.9    19.645   ON
  00:00:00                                                                      

  2026-07-16   19.799   9.421       4.004       67.46         138.88   20.535   ON
  01:00:00                                                                      

  2026-07-16   19.274   9.277       4.021       64.11         139.31   19.269   ON
  02:00:00                                                                      

  2026-07-16   20.377   9.684       4.007       66.9          131.59   20.382   ON
  03:00:00                                                                      

  2026-07-16   20.235   9.44        3.916       64.78         134.36   20.054   ON
  04:00:00                                                                      

  2026-07-16   20.548   9.745       3.57        62.92         138.14   20.5     ON
  05:00:00                                                                      

  2026-07-16   20.52    9.442       3.444       63            133.67   19.788   ON
  06:00:00                                                                      

  2026-07-16   20.604   9.242       4.136       62.6          135.15   20.591   ON
  07:00:00                                                                      

  2026-07-16   19.933   9.363       3.479       62.02         133.01   19.886   ON
  08:00:00                                                                      

  2026-07-16   19.437   9.357       3.564       65.43         132.96   20.264   ON
  09:00:00                                                                      

  2026-07-16   19.853   9.396       3.97        62.41         139.75   20.048   ON
  10:00:00                                                                      

  2026-07-16   20.807   9.467       3.813       64.41         133.28   19.986   ON
  11:00:00                                                                      

  2026-07-16   20.22    9.446       4.113       65.05         140.65   20.865   ON
  12:00:00                                                                      

  2026-07-16   20.458   9.747       3.683       64.55         137.54   20.421   ON
  13:00:00                                                                      

  2026-07-16   20.304   9.165       4.055       66.21         128.94   20.912   ON
  14:00:00                                                                      

  2026-07-16   20.234   9.348       4.503       63.14         131.71   20.341   ON
  15:00:00                                                                      

  2026-07-16   19.885   9.516       3.643       63.53         132.18   20.539   ON
  16:00:00                                                                      

  2026-07-16   19.577   9.612       3.782       66.47         140.5    20.959   ON
  17:00:00                                                                      

  2026-07-16   20.35    9.516       3.657       66.42         133.95   20.33    ON
  18:00:00                                                                      

  2026-07-16   19.659   9.495       3.753       64.77         138.41   20.208   ON
  19:00:00                                                                      

  2026-07-16   20.644   9.58        3.681       63.37         140.04   20.021   ON
  20:00:00                                                                      

  2026-07-16   20.224   9.471       3.976       63.76         136.2    20.17    ON
  21:00:00                                                                      

  2026-07-16   20.268   9.457       4.023       65.97         131.93   20.747   ON
  22:00:00                                                                      

  2026-07-16   20.018   9.555       3.856       67.5          135.54   20.545   ON
  23:00:00                                                                      

  2026-07-17   19.354   9.283       4           63.9          138.33   20.361   ON
  00:00:00                                                                      

  2026-07-17   19.67    9.502       3.556       64.61         134.69   20.517   ON
  01:00:00                                                                      

  2026-07-17   20.376   9.382       3.906       63.44         138.05   20.715   ON
  02:00:00                                                                      

  2026-07-17   19.525   9.538       3.656       66.46         132.29   20.713   ON
  03:00:00                                                                      

  2026-07-17   19.545   9.47        4.066       64.99         129.58   20.011   ON
  04:00:00                                                                      

  2026-07-17   20.584   9.685       3.89        65.53         133.04   20.029   ON
  05:00:00                                                                      

  2026-07-17   19.202   9.581       3.327       63.89         135.98   21.089   ON
  06:00:00                                                                      

  2026-07-17   19.977   9.544       3.796       66.68         128.84   20.394   ON
  07:00:00                                                                      

  2026-07-17   20.149   9.381       3.478       65.66         135.91   20.682   ON
  08:00:00                                                                      

  2026-07-17   20.768   9.582       3.724       66.34         132.57   20.179   ON
  09:00:00                                                                      

  2026-07-17   20.421   9.179       4.051       64.46         128.92   19.897   ON
  10:00:00                                                                      

  2026-07-17   20.181   9.631       4.303       63.95         136.1    20.069   ON
  11:00:00                                                                      

  2026-07-17   19.332   9.626       3.914       65.43         140.63   20.806   ON
  12:00:00                                                                      

  2026-07-17   19.905   9.528       3.922       65.31         129.17   20.208   ON
  13:00:00                                                                      

  2026-07-17   19.347   9.599       3.932       66.7          144.72   20.813   ON
  14:00:00                                                                      

  2026-07-17   20.114   9.291       3.746       66.66         135.31   20.597   ON
  15:00:00                                                                      

  2026-07-17   19.472   9.426       3.336       63.02         131.53   19.885   ON
  16:00:00                                                                      

  2026-07-17   20.395   9.366       4.01        62.13         136.12   20.054   ON
  17:00:00                                                                      

  2026-07-17   20.256   9.586       3.859       66.7          127.47   20.478   ON
  18:00:00                                                                      

  2026-07-17   19.8     9.586       3.805       64.29         135.58   21.018   ON
  19:00:00                                                                      

  2026-07-17   20.172   9.734       3.881       64.24         135.09   20.697   ON
  20:00:00                                                                      

  2026-07-17   20.094   9.345       3.919       65.92         125.03   19.498   ON
  21:00:00                                                                      

  2026-07-17   20.052   9.367       3.834       65.1          126.54   20.608   ON
  22:00:00                                                                      

  2026-07-17   20.014   9.563       4.054       64.97         129.97   20.293   ON
  23:00:00                                                                      

  2026-07-18   20.295   9.408       3.794       65.58         132.83   20.476   ON
  00:00:00                                                                      

  2026-07-18   20.038   9.4         4.085       64.43         135.72   20.74    ON
  01:00:00                                                                      

  2026-07-18   19.866   9.592       3.723       64.73         133.25   19.983   ON
  02:00:00                                                                      

  2026-07-18   20.156   9.5         3.712       64.25         130.74   20.816   ON
  03:00:00                                                                      

  2026-07-18   19.74    9.414       3.542       65.37         136.81   20.314   ON
  04:00:00                                                                      

  2026-07-18   20.485   9.662       3.602       64.1          136.21   19.989   ON
  05:00:00                                                                      

  2026-07-18   20.329   9.483       3.189       67.11         134.41   20.615   ON
  06:00:00                                                                      

  2026-07-18   19.217   9.29        3.495       65.58         132.54   20.017   ON
  07:00:00                                                                      

  2026-07-18   19.899   9.468       3.738       64.81         129.76   20.029   ON
  08:00:00                                                                      

  2026-07-18   19.962   9.499       4.028       66.39         133.68   20.087   ON
  09:00:00                                                                      

  2026-07-18   19.983   9.396       3.587       65.43         140.58   20.605   ON
  10:00:00                                                                      

  2026-07-18   20.2     9.652       3.717       66.18         136.61   20.807   ON
  11:00:00                                                                      

  2026-07-18   20.524   9.541       3.757       65.81         138.94   20.195   ON
  12:00:00                                                                      

  2026-07-18   20.583   9.603       3.788       63.03         128.67   21.181   ON
  13:00:00                                                                      

  2026-07-18   19.258   9.631       3.322       66.69         135.52   20.333   ON
  14:00:00                                                                      

  2026-07-18   20.351   9.462       3.669       66.43         129.56   20.608   ON
  15:00:00                                                                      

  2026-07-18   19.282   9.469       4.322       64.43         136.67   20.52    ON
  16:00:00                                                                      

  2026-07-18   20.415   9.518       4.036       68.71         135.99   20.381   ON
  17:00:00                                                                      

  2026-07-18   20.182   9.448       3.638       63.09         136.09   19.924   ON
  18:00:00                                                                      

  2026-07-18   19.699   9.717       3.849       66.53         139.61   20.44    ON
  19:00:00                                                                      

  2026-07-18   19.821   9.376       4.042       64.56         133.08   20.148   ON
  20:00:00                                                                      

  2026-07-18   19.821   9.307       3.75        64.89         139.43   20.068   ON
  21:00:00                                                                      

  2026-07-18   20.482   9.588       3.95        66.31         135.19   19.958   ON
  22:00:00                                                                      

  2026-07-18   19.788   9.477       3.839       66.53         132.09   20.492   ON
  23:00:00                                                                      

  2026-07-19   19.848   9.297       3.602       66.21         133.49   20.202   ON
  00:00:00                                                                      

  2026-07-19   20.166   9.614       3.82        62.97         137.72   20.416   ON
  01:00:00                                                                      

  2026-07-19   20.647   9.62        3.515       66.6          132.38   20.146   ON
  02:00:00                                                                      

  2026-07-19   19.783   9.382       3.786       64.03         137.55   19.856   ON
  03:00:00                                                                      

  2026-07-19   20.115   9.334       3.883       64.76         135.68   19.957   ON
  04:00:00                                                                      

  2026-07-19   19.726   9.627       3.669       65.27         132.12   20.887   ON
  05:00:00                                                                      

  2026-07-19   20.404   9.613       3.918       62.96         124.43   20.624   ON
  06:00:00                                                                      

  2026-07-19   19.558   9.625       3.86        66.67         134.65   20.505   ON
  07:00:00                                                                      

  2026-07-19   20.158   9.463       3.813       64.71         138.34   20.629   ON
  08:00:00                                                                      

  2026-07-19   20.165   9.637       3.688       63.36         132.6    19.915   ON
  09:00:00                                                                      

  2026-07-19   19.859   9.756       3.604       64.06         137.84   20.728   ON
  10:00:00                                                                      

  2026-07-19   20.453   9.621       3.84        63.12         131.1    19.738   ON
  11:00:00                                                                      

  2026-07-19   20.735   9.613       3.837       63.27         139.41   20.142   ON
  12:00:00                                                                      

  2026-07-19   20.012   9.682       4.043       65.54         141.4    20.12    ON
  13:00:00                                                                      

  2026-07-19   20.138   9.587       3.361       65.75         135.85   20.158   ON
  14:00:00                                                                      

  2026-07-19   20.084   9.517       3.872       66.92         136.82   19.653   ON
  15:00:00                                                                      

  2026-07-19   20.466   9.568       3.728       68.43         129.48   20.791   ON
  16:00:00                                                                      

  2026-07-19   20.324   9.658       3.693       66.27         140.78   19.682   ON
  17:00:00                                                                      

  2026-07-19   20.041   9.562       3.498       61.43         132.08   20.709   ON
  18:00:00                                                                      

  2026-07-19   19.983   9.617       4.351       66.07         137.42   20.524   ON
  19:00:00                                                                      

  2026-07-19   19.716   9.458       3.972       65.44         143.21   20.468   ON
  20:00:00                                                                      

  2026-07-19   19.905   9.502       3.814       66.02         136.5    20.273   ON
  21:00:00                                                                      

  2026-07-19   20.014   9.298       3.922       66.36         136.13   20.164   ON
  22:00:00                                                                      

  2026-07-19   20.66    9.646       3.411       65.31         136.91   20.05    ON
  23:00:00                                                                      

  2026-07-20   20.345   9.567       3.773       66.44         132.54   20.926   ON
  00:00:00                                                                      

  2026-07-20   19.179   9.364       3.855       66.11         132.57   20.192   ON
  01:00:00                                                                      

  2026-07-20   19.806   9.582       3.795       68.23         139.81   20.044   ON
  02:00:00                                                                      

  2026-07-20   20.483   9.398       3.468       64.08         132.02   20.733   ON
  03:00:00                                                                      

  2026-07-20   20.448   9.59        3.717       63.58         133.6    21.193   ON
  04:00:00                                                                      

  2026-07-20   19.32    9.798       4.213       64.75         129.49   19.869   ON
  05:00:00                                                                      

  2026-07-20   19.965   9.535       4.041       68.8          135.71   20.325   ON
  06:00:00                                                                      

  2026-07-20   20.619   9.407       3.902       62.03         130.87   20.31    ON
  07:00:00                                                                      

  2026-07-20   19.731   9.447       3.953       64.72         134.17   19.937   ON
  08:00:00                                                                      

  2026-07-20   19.848   9.55        4.446       63.34         133.84   19.888   ON
  09:00:00                                                                      

  2026-07-20   20.043   9.45        3.935       64.88         134.7    20.567   ON
  10:00:00                                                                      

  2026-07-20   19.607   9.608       3.666       65.63         132.1    20.313   ON
  11:00:00                                                                      

  2026-07-20   20.419   9.234       3.396       63.62         133.77   20.648   ON
  12:00:00                                                                      

  2026-07-20   20.079   9.715       3.833       66.87         139.49   19.78    ON
  13:00:00                                                                      

  2026-07-20   20.082   9.489       3.8         68.06         138.71   19.875   ON
  14:00:00                                                                      

  2026-07-20   19.744   9.504       3.334       64.35         137.36   20.017   ON
  15:00:00                                                                      

  2026-07-20   20.414   9.699       3.689       66.34         137.09   20.292   ON
  16:00:00                                                                      

  2026-07-20   19.871   9.652       3.779       63.67         128.42   20.457   ON
  17:00:00                                                                      

  2026-07-20   19.695   9.246       3.71        63.44         134.1    20.194   ON
  18:00:00                                                                      

  2026-07-20   19.939   9.304       3.249       66.17         136.11   19.552   ON
  19:00:00                                                                      

  2026-07-20   19.49    9.637       3.5         66.16         136.04   20.023   ON
  20:00:00                                                                      

  2026-07-20   19.781   9.448       3.49        63.39         137.26   20.99    ON
  21:00:00                                                                      

  2026-07-20   20.899   9.372       4.094       65.96         129.82   20.051   ON
  22:00:00                                                                      

  2026-07-20   19.696   9.621       3.743       67.16         136.66   20.487   ON
  23:00:00                                                                      

  2026-07-21   19.653   9.485       3.523       64.18         132.76   20.152   ON
  00:00:00                                                                      

  2026-07-21   20.008   9.563       3.948       62.69         136.14   20.493   ON
  01:00:00                                                                      

  2026-07-21   20.128   9.382       3.356       65.48         141.66   20.677   ON
  02:00:00                                                                      

  2026-07-21   20.165   9.436       3.676       66.6          137.16   19.633   ON
  03:00:00                                                                      

  2026-07-21   20.098   9.475       3.916       65.01         134.81   20.246   ON
  04:00:00                                                                      

  2026-07-21   19.353   9.542       3.549       65.92         131.49   20.906   ON
  05:00:00                                                                      

  2026-07-21   19.82    9.652       3.541       64.23         138.8    20.02    ON
  06:00:00                                                                      

  2026-07-21   19.14    9.265       3.366       65.42         127.12   20.052   ON
  07:00:00                                                                      

  2026-07-21   20.276   9.383       3.578       64.63         131.8    20.403   ON
  08:00:00                                                                      

  2026-07-21   20.163   9.39        3.973       65.31         125.16   20.558   ON
  09:00:00                                                                      

  2026-07-21   20.324   9.517       3.87        66.09         134.16   19.765   ON
  10:00:00                                                                      

  2026-07-21   19.4     9.392       4.025       64.95         131.71   20.754   ON
  11:00:00                                                                      

  2026-07-21   19.21    9.51        3.635       64.83         132.73   20.348   ON
  12:00:00                                                                      

  2026-07-21   20.028   9.662       4.401       62.72         130.8    20.395   ON
  13:00:00                                                                      

  2026-07-21   19.611   9.519       3.363       62.2          142.76   20.47    ON
  14:00:00                                                                      

  2026-07-21   19.537   9.679       3.536       64.16         138.08   20.297   ON
  15:00:00                                                                      

  2026-07-21   19.675   9.496       3.228       64.96         137.83   20.776   ON
  16:00:00                                                                      

  2026-07-21   19.397   9.234       3.89        64.42         132.16   20.32    ON
  17:00:00                                                                      

  2026-07-21   19.279   9.493       3.84        65.02         138.01   20.523   ON
  18:00:00                                                                      

  2026-07-21   20.136   9.543       4.305       64.52         134.78   20.336   ON
  19:00:00                                                                      

  2026-07-21   20.114   9.404       3.66        64.33         133.51   20.493   ON
  20:00:00                                                                      

  2026-07-21   20.293   9.478       3.674       64.06         128.73   20.43    ON
  21:00:00                                                                      

  2026-07-21   20.116   9.686       2.944       64.83         135.22   19.891   ON
  22:00:00                                                                      

  2026-07-21   20.03    9.568       3.206       66.04         124.5    20.689   ON
  23:00:00                                                                      

  2026-07-22   20.167   9.34        3.783       64.56         131.75   19.924   ON
  00:00:00                                                                      

  2026-07-22   19.875   9.313       3.593       62.54         125.71   20.626   ON
  01:00:00                                                                      

  2026-07-22   20.039   9.595       3.907       63.7          136.35   20.496   ON
  02:00:00                                                                      

  2026-07-22   19.927   9.585       3.521       63.66         137.05   19.963   ON
  03:00:00                                                                      

  2026-07-22   19.107   9.323       3.851       65.14         138.26   20.392   ON
  04:00:00                                                                      

  2026-07-22   20.14    9.469       3.819       66.45         129.26   20.241   ON
  05:00:00                                                                      

  2026-07-22   20.665   9.51        3.354       60.88         138.99   20.46    ON
  06:00:00                                                                      

  2026-07-22   20.591   9.644       3.929       63.85         142.73   20.036   ON
  07:00:00                                                                      

  2026-07-22   19.907   9.619       4.056       63.93         132.68   20.789   ON
  08:00:00                                                                      

  2026-07-22   20.132   9.845       3.8         68.26         131.15   20.443   ON
  09:00:00                                                                      

  2026-07-22   20.078   9.4         3.969       63.91         132.33   20.795   ON
  10:00:00                                                                      

  2026-07-22   20.674   9.237       3.934       65.76         132.4    20.157   ON
  11:00:00                                                                      

  2026-07-22   20.648   9.485       3.715       67.24         138.27   20.111   ON
  12:00:00                                                                      

  2026-07-22   19.698   9.649       3.946       64.25         132.4    20.531   ON
  13:00:00                                                                      

  2026-07-22   19.694   9.335       4.233       64.73         136.37   19.839   ON
  14:00:00                                                                      

  2026-07-22   19.816   9.344       3.516       64.89         134.67   20.135   ON
  15:00:00                                                                      

  2026-07-22   19.764   9.534       3.876       65.28         130.96   20.948   ON
  16:00:00                                                                      

  2026-07-22   20.599   9.504       3.68        63.76         134.91   20.15    ON
  17:00:00                                                                      

  2026-07-22   19.247   9.691       3.775       65.16         134.87   20.421   ON
  18:00:00                                                                      

  2026-07-22   19.56    9.429       3.688       64.16         135.32   19.827   ON
  19:00:00                                                                      

  2026-07-22   19.443   9.888       3.687       63.89         135.94   20.766   ON
  20:00:00                                                                      

  2026-07-22   19.734   9.631       3.81        67.18         133.49   19.918   ON
  21:00:00                                                                      

  2026-07-22   20.241   9.633       3.644       62.74         136.42   19.907   ON
  22:00:00                                                                      

  2026-07-22   19.573   9.307       3.861       66.41         127.81   20.468   ON
  23:00:00                                                                      

  2026-07-23   20.31    9.571       3.267       64.68         132.67   19.971   ON
  00:00:00                                                                      

  2026-07-23   20.645   9.772       3.992       64.87         139.87   19.608   ON
  01:00:00                                                                      

  2026-07-23   20.064   9.463       3.633       64            136.01   19.953   ON
  02:00:00                                                                      

  2026-07-23   20.471   9.766       3.619       65.17         133.56   20.479   ON
  03:00:00                                                                      

  2026-07-23   19.91    9.62        4.053       65.86         131.63   20.197   ON
  04:00:00                                                                      

  2026-07-23   20.138   9.683       3.977       63.38         132.24   20.555   ON
  05:00:00                                                                      

  2026-07-23   19.891   9.566       3.944       65.81         134.13   20.669   ON
  06:00:00                                                                      

  2026-07-23   20.434   9.654       3.937       61.82         127.37   20.593   ON
  07:00:00                                                                      

  2026-07-23   20.13    9.242       3.845       63.68         133.23   20.937   ON
  08:00:00                                                                      

  2026-07-23   20.259   9.481       3.546       62.97         133.85   20.424   ON
  09:00:00                                                                      

  2026-07-23   20.35    9.434       3.934       64.52         126.12   20.888   ON
  10:00:00                                                                      

  2026-07-23   20.405   9.515       3.89        65.87         127.69   20.26    ON
  11:00:00                                                                      

  2026-07-23   19.626   9.439       3.941       63.83         134.18   20.906   ON
  12:00:00                                                                      

  2026-07-23   20.107   9.317       3.742       65.34         133.34   20.735   ON
  13:00:00                                                                      

  2026-07-23   19.719   9.561       3.737       64.68         142      20.8     ON
  14:00:00                                                                      

  2026-07-23   19.847   9.547       3.608       66.84         142.78   21.607   ON
  15:00:00                                                                      

  2026-07-23   19.998   9.498       4.13        62.2          122.74   20.523   ON
  16:00:00                                                                      

  2026-07-23   20.234   9.64        3.608       62.31         131.9    20.643   ON
  17:00:00                                                                      

  2026-07-23   19.992   9.446       3.921       64.5          139.42   20.769   ON
  18:00:00                                                                      

  2026-07-23   19.911   9.639       3.674       61.98         136.06   20.785   ON
  19:00:00                                                                      

  2026-07-23   20.512   9.615       3.505       65.1          140.42   20.663   ON
  20:00:00                                                                      

  2026-07-23   20.182   9.369       3.725       65.16         139.68   20.68    ON
  21:00:00                                                                      

  2026-07-23   19.172   9.623       3.435       63.51         134.22   20.392   ON
  22:00:00                                                                      

  2026-07-23   20.157   9.459       3.709       63.67         139.25   20.166   ON
  23:00:00                                                                      

  2026-07-24   19.825   9.553       3.776       65.26         134.47   19.874   ON
  00:00:00                                                                      

  2026-07-24   20.26    9.44        3.572       65.5          129.76   20.434   ON
  01:00:00                                                                      

  2026-07-24   20.302   9.696       3.697       64.52         135.32   20.146   ON
  02:00:00                                                                      

  2026-07-24   20.659   9.571       3.816       65.77         139.93   19.824   ON
  03:00:00                                                                      

  2026-07-24   19.865   9.108       3.781       63.89         138.14   21.004   ON
  04:00:00                                                                      

  2026-07-24   20.343   9.359       3.498       65.25         133.25   20.833   ON
  05:00:00                                                                      

  2026-07-24   19.937   9.312       3.816       66.54         140.56   20.481   ON
  06:00:00                                                                      

  2026-07-24   19.739   9.458       3.606       66.4          140.18   19.919   ON
  07:00:00                                                                      

  2026-07-24   19.394   9.602       3.563       63.43         140.25   20.38    ON
  08:00:00                                                                      

  2026-07-24   20.111   9.51        3.723       63.68         127.27   20.431   ON
  09:00:00                                                                      

  2026-07-24   20.572   9.241       3.684       63.68         131.48   20.213   ON
  10:00:00                                                                      

  2026-07-24   19.92    9.184       3.981       65.2          132.34   20.975   ON
  11:00:00                                                                      

  2026-07-24   20.42    9.499       3.826       65.56         132.02   20.789   ON
  12:00:00                                                                      

  2026-07-24   20.036   9.456       3.666       63.07         126.41   19.955   ON
  13:00:00                                                                      

  2026-07-24   20.325   9.622       4.306       63.09         132.5    20.561   ON
  14:00:00                                                                      

  2026-07-24   19.942   9.583       4.088       65.16         139.34   19.741   ON
  15:00:00                                                                      

  2026-07-24   20.22    9.536       3.265       61.38         130.73   20.589   ON
  16:00:00                                                                      

  2026-07-24   19.612   9.707       3.419       66.27         143.45   20.679   ON
  17:00:00                                                                      

  2026-07-24   20.292   9.552       3.526       64.82         130.79   20.954   ON
  18:00:00                                                                      

  2026-07-24   20.739   9.606       4.07        63.63         136.35   19.412   ON
  19:00:00                                                                      

  2026-07-24   20.43    9.431       3.503       66.35         133.96   21.019   ON
  20:00:00                                                                      

  2026-07-24   19.796   9.559       3.769       64.84         129.94   20.034   ON
  21:00:00                                                                      

  2026-07-24   19.273   9.753       3.713       63.89         135.76   20.692   ON
  22:00:00                                                                      

  2026-07-24   20.083   9.333       4.075       68.2          135.42   20.014   ON
  23:00:00                                                                      

  2026-07-25   19.563   9.313       3.687       64.86         134.44   20.43    ON
  00:00:00                                                                      

  2026-07-25   19.958   9.43        3.898       65.02         139.58   20.611   ON
  01:00:00                                                                      

  2026-07-25   20.396   9.666       3.746       65.4          137.92   20.311   ON
  02:00:00                                                                      

  2026-07-25   19.122   9.508       4.116       64.74         128.6    20.619   ON
  03:00:00                                                                      

  2026-07-25   19.903   9.39        3.917       65.73         140.06   20.221   ON
  04:00:00                                                                      

  2026-07-25   19.942   9.588       3.977       64.19         131.2    20.13    ON
  05:00:00                                                                      

  2026-07-25   20.294   9.491       3.719       66.21         127.23   20.088   ON
  06:00:00                                                                      

  2026-07-25   20.167   9.498       3.761       65.2          138.12   19.803   ON
  07:00:00                                                                      

  2026-07-25   20.67    9.302       4.048       65.12         139.37   20.397   ON
  08:00:00                                                                      

  2026-07-25   20.179   9.222       4.264       66.43         131.25   20.168   ON
  09:00:00                                                                      

  2026-07-25   20.282   9.566       3.77        63.2          135      21.013   ON
  10:00:00                                                                      

  2026-07-25   19.22    9.417       3.919       64.93         132.01   20.209   ON
  11:00:00                                                                      

  2026-07-25   20.006   9.605       3.551       65.91         137.32   20.88    ON
  12:00:00                                                                      

  2026-07-25   19.883   9.801       4.175       66.38         132.85   19.341   ON
  13:00:00                                                                      

  2026-07-25   19.988   9.625       3.524       64.59         135.82   20.582   ON
  14:00:00                                                                      

  2026-07-25   20.415   9.32        3.909       64.02         129.81   20.522   ON
  15:00:00                                                                      

  2026-07-25   19.528   9.54        3.911       66.24         137.06   20.849   ON
  16:00:00                                                                      

  2026-07-25   19       9.413       3.61        62.27         135.03   21.116   ON
  17:00:00                                                                      

  2026-07-25   20.725   9.547       3.513       66.55         145.09   20.579   ON
  18:00:00                                                                      

  2026-07-25   19.942   9.634       3.769       62.31         140.19   21.063   ON
  19:00:00                                                                      

  2026-07-25   19.855   9.454       4.043       63.4          132.59   20.269   ON
  20:00:00                                                                      

  2026-07-25   20.568   9.586       3.454       66.34         129.78   20.199   ON
  21:00:00                                                                      

  2026-07-25   20.326   9.522       3.695       64.85         137.7    20.828   ON
  22:00:00                                                                      

  2026-07-25   20.088   9.575       3.132       63.6          131.38   20.522   ON
  23:00:00                                                                      

  2026-07-26   20.133   9.627       3.75        66.76         137.84   20.851   ON
  00:00:00                                                                      

  2026-07-26   20.301   9.493       3.503       65.41         139.05   20.06    ON
  01:00:00                                                                      

  2026-07-26   19.654   9.67        3.659       64.09         140.84   20.281   ON
  02:00:00                                                                      

  2026-07-26   20.059   9.695       3.788       65.82         140.89   20.514   ON
  03:00:00                                                                      

  2026-07-26   20.825   9.371       3.616       65.5          139.7    20.398   ON
  04:00:00                                                                      

  2026-07-26   20.24    9.478       3.979       64.62         134.8    20.769   ON
  05:00:00                                                                      

  2026-07-26   20.14    9.497       4.075       66.07         134.69   21.563   ON
  06:00:00                                                                      

  2026-07-26   20.807   9.214       4.092       65.68         135.65   20.339   ON
  07:00:00                                                                      

  2026-07-26   20.116   9.366       3.767       62.89         141.32   20.98    ON
  08:00:00                                                                      

  2026-07-26   20.667   9.691       3.675       65.29         133.38   20.314   ON
  09:00:00                                                                      

  2026-07-26   20.155   9.589       3.979       65.4          134.9    19.822   ON
  10:00:00                                                                      

  2026-07-26   19.943   9.512       4.049       65.68         138.27   19.81    ON
  11:00:00                                                                      

  2026-07-26   20.183   9.533       3.665       63.63         130.03   20.024   ON
  12:00:00                                                                      

  2026-07-26   20.144   9.645       3.784       66.42         133.33   19.577   ON
  13:00:00                                                                      

  2026-07-26   19.484   9.326       3.735       62.72         135.01   20.33    ON
  14:00:00                                                                      

  2026-07-26   20.837   9.724       3.984       64.24         133.23   20.67    ON
  15:00:00                                                                      

  2026-07-26   20.233   9.417       3.666       64.5          132.71   19.507   ON
  16:00:00                                                                      

  2026-07-26   20.888   9.445       3.22        65.05         136.44   20.24    ON
  17:00:00                                                                      

  2026-07-26   19.738   9.347       3.94        64.67         131.09   19.895   ON
  18:00:00                                                                      

  2026-07-26   19.88    9.548       4.025       65.24         137.03   20.908   ON
  19:00:00                                                                      

  2026-07-26   19.535   9.374       3.847       65.73         133.59   20.914   ON
  20:00:00                                                                      

  2026-07-26   19.961   9.488       4.005       67.88         128.47   20.534   ON
  21:00:00                                                                      

  2026-07-26   20.279   9.366       3.782       64.41         123.71   20.427   ON
  22:00:00                                                                      

  2026-07-26   20.848   9.671       3.483       65.95         130.64   20.227   ON
  23:00:00                                                                      

  2026-07-27   19.85    9.694       3.886       64.63         136.58   20.355   ON
  00:00:00                                                                      

  2026-07-27   19.899   9.386       3.678       64.91         133.99   21.041   ON
  01:00:00                                                                      

  2026-07-27   20.414   9.298       3.484       63.82         132.44   20.658   ON
  02:00:00                                                                      

  2026-07-27   20.23    9.307       4.066       64.28         134.47   20.507   ON
  03:00:00                                                                      

  2026-07-27   19.768   9.615       3.78        66.93         136.25   21.139   ON
  04:00:00                                                                      

  2026-07-27   19.846   9.302       3.086       64.88         133.69   20.486   ON
  05:00:00                                                                      

  2026-07-27   19.765   9.365       3.934       65.42         130.73   20.536   ON
  06:00:00                                                                      

  2026-07-27   20.503   9.485       3.807       63.18         140.04   20.222   ON
  07:00:00                                                                      

  2026-07-27   19.8     9.717       3.67        65.77         134.54   19.757   ON
  08:00:00                                                                      

  2026-07-27   19.894   9.506       3.685       65.74         136.55   20.437   ON
  09:00:00                                                                      

  2026-07-27   20.487   9.456       3.918       65.54         132.25   20.235   ON
  10:00:00                                                                      

  2026-07-27   19.796   9.599       3.955       66.6          135.39   20.747   ON
  11:00:00                                                                      

  2026-07-27   20.435   9.245       3.965       65.03         138.87   19.838   ON
  12:00:00                                                                      

  2026-07-27   19.464   9.335       4.081       64.12         131.13   19.864   ON
  13:00:00                                                                      

  2026-07-27   19.77    9.642       3.638       65.71         133.93   20.395   ON
  14:00:00                                                                      

  2026-07-27   20.568   9.661       4.198       65.64         133.37   20.085   ON
  15:00:00                                                                      

  2026-07-27   20.261   9.581       4.467       67.6          130.16   20.168   ON
  16:00:00                                                                      

  2026-07-27   19.663   9.558       3.833       64.41         141.54   20.389   ON
  17:00:00                                                                      

  2026-07-27   19.56    9.455       3.917       65.21         130.01   19.982   ON
  18:00:00                                                                      

  2026-07-27   19.375   9.463       3.931       67.03         136.73   20.324   ON
  19:00:00                                                                      

  2026-07-27   20.154   9.761       4.118       64.87         131.85   21.132   ON
  20:00:00                                                                      

  2026-07-27   19.92    9.351       3.483       68.4          134.07   20.414   ON
  21:00:00                                                                      

  2026-07-27   20.139   9.688       4.076       68.3          132.76   20.245   ON
  22:00:00                                                                      

  2026-07-27   19.987   9.492       3.669       65.18         132.07   20.459   ON
  23:00:00                                                                      

  2026-07-28   21.117   9.268       3.815       66.1          134.41   20.088   ON
  00:00:00                                                                      

  2026-07-28   20.512   9.582       3.91        66.46         125.43   20.556   ON
  01:00:00                                                                      

  2026-07-28   19.414   9.38        3.963       64.14         131.03   20.753   ON
  02:00:00                                                                      

  2026-07-28   20.12    9.56        3.759       63.81         135.39   20.159   ON
  03:00:00                                                                      

  2026-07-28   19.531   9.553       3.92        66.86         141.1    20.183   ON
  04:00:00                                                                      

  2026-07-28   20.105   9.845       4.091       66.47         134.64   20.574   ON
  05:00:00                                                                      

  2026-07-28   19.903   9.411       3.87        64.48         131      19.695   ON
  06:00:00                                                                      

  2026-07-28   20.111   9.206       4.126       64.12         138.14   20.912   ON
  07:00:00                                                                      

  2026-07-28   19.882   9.561       3.745       63.28         136.35   20.078   ON
  08:00:00                                                                      

  2026-07-28   19.189   9.596       3.314       62.89         130.03   19.621   ON
  09:00:00                                                                      

  2026-07-28   20.255   9.463       3.77        66.35         131.63   20.406   ON
  10:00:00                                                                      

  2026-07-28   19.288   9.389       3.787       65.59         129.67   19.942   ON
  11:00:00                                                                      

  2026-07-28   19.648   9.574       3.786       64.83         138.89   19.821   ON
  12:00:00                                                                      

  2026-07-28   19.72    9.604       3.406       62.94         130      19.971   ON
  13:00:00                                                                      

  2026-07-28   20.08    9.438       3.459       63.76         129.73   20.367   ON
  14:00:00                                                                      

  2026-07-28   19.531   9.624       3.682       65.26         135.1    20.55    ON
  15:00:00                                                                      

  2026-07-28   19.948   9.509       3.796       63.16         138.24   19.625   ON
  16:00:00                                                                      

  2026-07-28   20.042   9.489       3.734       65.11         131.99   20.355   ON
  17:00:00                                                                      

  2026-07-28   20.778   9.322       4.092       64.14         137.31   19.986   ON
  18:00:00                                                                      

  2026-07-28   19.751   9.402       3.921       61.25         129.06   20.258   ON
  19:00:00                                                                      

  2026-07-28   20.117   9.6         3.859       65.76         137.36   20.603   ON
  20:00:00                                                                      

  2026-07-28   20.276   9.687       3.732       63.88         135.05   20.485   ON
  21:00:00                                                                      

  2026-07-28   19.945   9.671       3.414       61.84         134.52   20.83    ON
  22:00:00                                                                      

  2026-07-28   20.093   9.488       3.883       64.56         125.74   19.984   ON
  23:00:00                                                                      

  2026-07-29   20.401   9.477       3.72        62.75         138.22   20.387   ON
  00:00:00                                                                      

  2026-07-29   19.756   9.373       3.883       66.22         134.46   20.542   ON
  01:00:00                                                                      

  2026-07-29   18.874   9.383       4.257       64.32         135.09   20.12    ON
  02:00:00                                                                      

  2026-07-29   19.903   9.447       3.795       64.73         130.05   20.039   ON
  03:00:00                                                                      

  2026-07-29   20.135   9.644       4.301       66.48         139.95   19.759   ON
  04:00:00                                                                      

  2026-07-29   20.22    9.677       3.653       62.35         132.64   19.795   ON
  05:00:00                                                                      

  2026-07-29   20.214   9.553       3.649       65.13         135.96   21.11    ON
  06:00:00                                                                      

  2026-07-29   20.484   9.585       3.544       66.36         133.77   20.119   ON
  07:00:00                                                                      

  2026-07-29   20.046   9.36        3.83        65.73         133.23   20.406   ON
  08:00:00                                                                      

  2026-07-29   19.782   9.473       3.278       63.45         137.02   20.442   ON
  09:00:00                                                                      

  2026-07-29   19.57    9.604       3.855       65.52         136.39   20.209   ON
  10:00:00                                                                      

  2026-07-29   19.497   9.509       3.903       67.5          139.54   20.437   ON
  11:00:00                                                                      

  2026-07-29   20.396   9.587       3.982       63.59         132.37   20.571   ON
  12:00:00                                                                      

  2026-07-29   19.774   9.307       3.881       64.13         137.64   20.073   ON
  13:00:00                                                                      

  2026-07-29   19.692   9.726       3.986       65.91         130.64   20.863   ON
  14:00:00                                                                      

  2026-07-29   20.607   9.454       3.968       64.95         134.85   20.44    ON
  15:00:00                                                                      

  2026-07-29   19.489   9.406       3.811       64.66         127.83   20.213   ON
  16:00:00                                                                      

  2026-07-29   20.354   9.516       3.868       67.53         134.53   20.278   ON
  17:00:00                                                                      

  2026-07-29   19.611   8.949       3.672       63.95         133.8    20.859   ON
  18:00:00                                                                      

  2026-07-29   19.801   9.451       3.748       66.29         131.75   21.015   ON
  19:00:00                                                                      

  2026-07-29   19.802   9.797       4.161       63.1          131.77   20.153   ON
  20:00:00                                                                      

  2026-07-29   20.16    9.414       3.507       60.68         133.76   20.555   ON
  21:00:00                                                                      

  2026-07-29   19.864   9.641       4.075       64.89         139.05   20.149   ON
  22:00:00                                                                      

  2026-07-29   20.377   9.25        3.994       66.08         134.13   19.981   ON
  23:00:00                                                                      

  2026-07-30   19.761   9.29        3.413       64.3          134.78   20.365   ON
  00:00:00                                                                      

  2026-07-30   20.751   9.263       3.393       67.46         136.22   20.551   ON
  01:00:00                                                                      

  2026-07-30   19.852   9.704       3.655       65.04         140.03   21.161   ON
  02:00:00                                                                      

  2026-07-30   19.28    9.218       3.887       65.88         138.99   20.019   ON
  03:00:00                                                                      

  2026-07-30   19.618   9.543       3.696       65.42         136.74   19.935   ON
  04:00:00                                                                      

  2026-07-30   19.624   9.376       3.974       63.43         127.91   19.556   ON
  05:00:00                                                                      

  2026-07-30   20.117   9.597       3.747       66.83         137.17   19.834   ON
  06:00:00                                                                      

  2026-07-30   19.454   9.339       3.459       67.1          132.21   20.62    ON
  07:00:00                                                                      

  2026-07-30   20.468   9.397       3.918       67.04         136.52   20.591   ON
  08:00:00                                                                      

  2026-07-30   19.638   9.555       3.988       66.82         131.67   21.105   ON
  09:00:00                                                                      

  2026-07-30   19.798   9.24        3.73        66.95         136.95   20.756   ON
  10:00:00                                                                      

  2026-07-30   20.43    9.195       3.733       66.36         133.12   20.321   ON
  11:00:00                                                                      

  2026-07-30   19.149   9.799       3.451       66.9          132.95   20.644   ON
  12:00:00                                                                      

  2026-07-30   20.849   9.511       3.994       65.48         135.59   20.948   ON
  13:00:00                                                                      

  2026-07-30   19.65    9.574       4.209       63.94         129.06   19.744   ON
  14:00:00                                                                      

  2026-07-30   19.227   9.5         3.816       65.75         139.3    19.605   ON
  15:00:00                                                                      

  2026-07-30   20.607   9.554       3.448       66.44         134.62   20.517   ON
  16:00:00                                                                      

  2026-07-30   19.915   9.501       3.456       63.9          134.18   20.588   ON
  17:00:00                                                                      

  2026-07-30   19.282   9.561       3.776       64.96         131.06   19.636   ON
  18:00:00                                                                      

  2026-07-30   20.253   9.315       3.471       66.71         137.4    20.216   ON
  19:00:00                                                                      

  2026-07-30   20.653   9.111       3.652       64.47         130.47   19.895   ON
  20:00:00                                                                      

  2026-07-30   20.655   9.401       3.497       68.88         139.03   20.515   ON
  21:00:00                                                                      

  2026-07-30   20.244   9.732       3.825       65.95         131.35   20.944   ON
  22:00:00                                                                      

  2026-07-30   19.602   9.403       3.498       66.98         134.97   20.746   ON
  23:00:00                                                                      
  --------------------------------------------------------------------------------------

### HE3301

Source pages: 102-135.

#### Data dictionary

  Name          Description                    Digital set   Engineering units   Span
  ------------- ------------------------------ ------------- ------------------- ------
  Name          Description                    digitalset    engunits            span
  HE3301_FEED   HE-3301 FEED RATE              T/H           45                  
  HE3301_DISP   HE-3301 DISCHARGE PRESSURE     BARG          20                  
  HE3301_VIB    HE-3301 VIBRATION              MM/S          20                  
  HE3301_TEMP   HE-3301 BEARING/PROCESS TEMP   DEG C         150                 
  HE3301_AMP    HE-3301 MOTOR AMPERE           A             300                 
  PLANT_RATE    ZCU PRODUCTION RATE            T/H           39                  
  RUN_STATUS    HE-3301 RUN STATUS             ON_OFF        ON_OFF              1

#### Typical value, zero, and instrument tag

## Typical value Zero Instrument tag --------------- ------

#### Hourly data

  --------------------------------------------------------------------------------------
  Timestamp    Feed     Discharge   Vibration   Temperature   Motor    Plant    Run
                        pressure                              ampere   rate     status
  ------------ -------- ----------- ----------- ------------- -------- -------- --------
  2026-05-01   29.579   9.658       3.516       64.96         133.93   31.224   ON
  00:00:00                                                                      

  2026-05-01   30.782   9.57        4.261       64.33         132.31   31       ON
  01:00:00                                                                      

  2026-05-01   30.232   9.391       3.912       64.63         140.12   31.474   ON
  02:00:00                                                                      

  2026-05-01   28.802   9.627       4.002       67.22         134.77   30.747   ON
  03:00:00                                                                      

  2026-05-01   30.089   9.471       3.433       63.99         130.24   30.195   ON
  04:00:00                                                                      

  2026-05-01   29.689   9.676       4.008       64.35         136.78   31.691   ON
  05:00:00                                                                      

  2026-05-01   30.338   9.588       3.782       65.9          131.2    29.894   ON
  06:00:00                                                                      

  2026-05-01   29.4     9.634       3.764       64.77         137.49   31.03    ON
  07:00:00                                                                      

  2026-05-01   29.202   9.475       3.727       65.34         142.3    30.396   ON
  08:00:00                                                                      

  2026-05-01   29.787   9.463       3.74        66.4          130.98   31.209   ON
  09:00:00                                                                      

  2026-05-01   31.454   9.445       3.73        64.59         136.41   30.137   ON
  10:00:00                                                                      

  2026-05-01   29.726   9.534       3.811       62.98         133.66   30.492   ON
  11:00:00                                                                      

  2026-05-01   29.613   9.2         4.058       66.04         133.86   30.164   ON
  12:00:00                                                                      

  2026-05-01   29.433   9.737       3.677       61.48         139.53   31.23    ON
  13:00:00                                                                      

  2026-05-01   29.031   9.523       4.37        66.28         126.65   30.234   ON
  14:00:00                                                                      

  2026-05-01   29.441   9.522       3.637       64.29         132.2    29.811   ON
  15:00:00                                                                      

  2026-05-01   30.406   9.295       3.813       64.1          140.56   30.016   ON
  16:00:00                                                                      

  2026-05-01   29.143   9.335       3.872       64.9          132.72   30.523   ON
  17:00:00                                                                      

  2026-05-01   29.584   9.348       3.731       63.04         130.49   30.559   ON
  18:00:00                                                                      

  2026-05-01   29.702   9.606       3.677       62.59         133.53   29.94    ON
  19:00:00                                                                      

  2026-05-01   30.309   9.392       3.07        61.95         135.88   31.588   ON
  20:00:00                                                                      

  2026-05-01   29.918   9.387       4.138       64.44         136.73   29.477   ON
  21:00:00                                                                      

  2026-05-01   29.739   9.613       3.535       63.88         138.59   30.414   ON
  22:00:00                                                                      

  2026-05-01   31.169   9.391       3.539       61.57         140.86   30.186   ON
  23:00:00                                                                      

  2026-05-02   30.922   9.239       3.34        65.71         138.26   30.271   ON
  00:00:00                                                                      

  2026-05-02   30.344   9.114       3.778       64.05         137.29   30.491   ON
  01:00:00                                                                      

  2026-05-02   29.45    9.497       3.54        66.34         137.53   29.768   ON
  02:00:00                                                                      

  2026-05-02   29.996   9.752       3.716       65.39         131.03   30.035   ON
  03:00:00                                                                      

  2026-05-02   28.781   9.599       4.094       65.43         137.74   30.284   ON
  04:00:00                                                                      

  2026-05-02   28.88    9.582       4.132       66            140.72   29.954   ON
  05:00:00                                                                      

  2026-05-02   29.447   9.349       4.024       64.28         133.32   30.868   ON
  06:00:00                                                                      

  2026-05-02   29.894   9.744       3.85        65.81         137.64   29.998   ON
  07:00:00                                                                      

  2026-05-02   30.223   9.418       3.939       65.63         138.89   31.368   ON
  08:00:00                                                                      

  2026-05-02   29.746   9.679       3.755       64.6          135.65   29.818   ON
  09:00:00                                                                      

  2026-05-02   29.068   9.857       3.886       67.53         135.96   31.578   ON
  10:00:00                                                                      

  2026-05-02   29.866   9.606       3.768       67.09         131.21   30.395   ON
  11:00:00                                                                      

  2026-05-02   29.868   9.295       3.468       66.21         132.77   31.854   ON
  12:00:00                                                                      

  2026-05-02   30.309   9.534       4.211       65.05         137.31   30.717   ON
  13:00:00                                                                      

  2026-05-02   30.518   9.414       3.62        64.65         142.05   30.661   ON
  14:00:00                                                                      

  2026-05-02   30.309   9.498       3.514       65.47         131.28   30.967   ON
  15:00:00                                                                      

  2026-05-02   30.751   9.644       3.763       65.26         140.84   28.57    ON
  16:00:00                                                                      

  2026-05-02   30.287   9.763       4.155       66.76         134.48   29.898   ON
  17:00:00                                                                      

  2026-05-02   30.005   9.67        3.825       65.51         131.75   30.15    ON
  18:00:00                                                                      

  2026-05-02   30.585   9.494       3.602       65.23         126.45   29.747   ON
  19:00:00                                                                      

  2026-05-02   30.207   9.578       3.722       65.18         133.97   31.01    ON
  20:00:00                                                                      

  2026-05-02   29.026   9.409       4.231       64.94         136.99   32.264   ON
  21:00:00                                                                      

  2026-05-02   30.439   9.558       3.461       67.11         129.98   29.009   ON
  22:00:00                                                                      

  2026-05-02   30.35    9.476       3.532       65.1          134.79   30.035   ON
  23:00:00                                                                      

  2026-05-03   29.399   9.649       3.365       64.86         135.38   30.686   ON
  00:00:00                                                                      

  2026-05-03   30.517   9.646       3.865       66.91         137.33   30.165   ON
  01:00:00                                                                      

  2026-05-03   29.261   9.557       3.691       64.2          136.52   31.043   ON
  02:00:00                                                                      

  2026-05-03   31.215   9.518       3.889       62.95         135.44   30.428   ON
  03:00:00                                                                      

  2026-05-03   28.609   9.469       3.918       66.4          138.56   30.996   ON
  04:00:00                                                                      

  2026-05-03   30.216   9.703       3.708       66.63         137.08   31.552   ON
  05:00:00                                                                      

  2026-05-03   29.577   9.628       4           66.35         134.33   30.666   ON
  06:00:00                                                                      

  2026-05-03   29.772   9.662       3.786       64.03         133.82   30.997   ON
  07:00:00                                                                      

  2026-05-03   30.388   9.449       3.771       64.88         134.37   30.395   ON
  08:00:00                                                                      

  2026-05-03   30.419   9.601       4.013       62.68         126.26   29.972   ON
  09:00:00                                                                      

  2026-05-03   30.525   9.527       3.888       64.9          135.41   30.88    ON
  10:00:00                                                                      

  2026-05-03   30.739   9.636       3.339       65.36         131.81   30.592   ON
  11:00:00                                                                      

  2026-05-03   29.354   9.867       3.153       64.37         138.36   30.378   ON
  12:00:00                                                                      

  2026-05-03   29.875   9.633       4.1         66.02         135.59   30.242   ON
  13:00:00                                                                      

  2026-05-03   29.811   9.596       3.645       65.99         136.64   30.133   ON
  14:00:00                                                                      

  2026-05-03   30.028   9.253       3.628       64.95         132.2    30.816   ON
  15:00:00                                                                      

  2026-05-03   28.762   9.441       3.909       66.59         136.8    30.544   ON
  16:00:00                                                                      

  2026-05-03   30.679   9.26        4.097       64.89         134.99   29.722   ON
  17:00:00                                                                      

  2026-05-03   30.3     9.426       3.721       65.49         128.32   30.447   ON
  18:00:00                                                                      

  2026-05-03   30.489   9.658       3.999       67.12         127.97   31.314   ON
  19:00:00                                                                      

  2026-05-03   30.284   9.763       3.47        67.89         128.35   31.178   ON
  20:00:00                                                                      

  2026-05-03   29.559   9.497       3.384       62.79         136.16   30.476   ON
  21:00:00                                                                      

  2026-05-03   29.442   9.22        3.229       64.51         136.56   30.773   ON
  22:00:00                                                                      

  2026-05-03   29.589   9.697       3.909       63.27         135.2    30.362   ON
  23:00:00                                                                      

  2026-05-04   29.024   9.652       3.665       65.18         138.2    31.842   ON
  00:00:00                                                                      

  2026-05-04   29.467   9.468       3.776       65.15         138.14   30.964   ON
  01:00:00                                                                      

  2026-05-04   29.776   9.201       4.088       65.38         129.63   30.41    ON
  02:00:00                                                                      

  2026-05-04   30.051   9.674       3.401       62.93         131.73   31.221   ON
  03:00:00                                                                      

  2026-05-04   29.594   9.489       4.41        65.35         134.03   30.344   ON
  04:00:00                                                                      

  2026-05-04   31.073   9.533       3.809       63.72         137.23   30.355   ON
  05:00:00                                                                      

  2026-05-04   29.604   9.209       3.265       63.29         137.52   29.719   ON
  06:00:00                                                                      

  2026-05-04   30.097   9.385       4.078       64.87         132.1    30.071   ON
  07:00:00                                                                      

  2026-05-04   30.112   9.721       4.298       64.55         140.81   30.163   ON
  08:00:00                                                                      

  2026-05-04   29.065   9.36        3.768       65.79         136.92   30.195   ON
  09:00:00                                                                      

  2026-05-04   30.163   9.596       3.617       63.94         136.14   30.03    ON
  10:00:00                                                                      

  2026-05-04   28.879   9.483       4.077       66.59         135.09   30.617   ON
  11:00:00                                                                      

  2026-05-04   29.631   9.52        4.027       64.1          136.57   30.102   ON
  12:00:00                                                                      

  2026-05-04   29.555   9.599       3.23        63.47         127.62   31.563   ON
  13:00:00                                                                      

  2026-05-04   29.657   9.382       3.764       63.12         131.88   30.34    ON
  14:00:00                                                                      

  2026-05-04   30.262   9.523       3.847       64.63         132.21   29.841   ON
  15:00:00                                                                      

  2026-05-04   30.778   9.514       3.411       67.74         137.48   30.952   ON
  16:00:00                                                                      

  2026-05-04   30.111   9.388       3.714       65.04         137.29   30.581   ON
  17:00:00                                                                      

  2026-05-04   30.414   9.548       3.546       63.44         133.72   30.588   ON
  18:00:00                                                                      

  2026-05-04   29.643   9.459       3.769       63.23         150.41   30.359   ON
  19:00:00                                                                      

  2026-05-04   29.441   9.317       4.041       64.81         124.2    31.457   ON
  20:00:00                                                                      

  2026-05-04   30.059   9.737       4.159       62.96         131.94   30.168   ON
  21:00:00                                                                      

  2026-05-04   29.381   9.631       3.75        68.98         142.77   31.197   ON
  22:00:00                                                                      

  2026-05-04   30.091   9.466       3.779       64.67         138.2    30.629   ON
  23:00:00                                                                      

  2026-05-05   30.61    9.574       3.583       63.83         128.41   31.089   ON
  00:00:00                                                                      

  2026-05-05   30.772   9.278       3.721       65.65         138.33   30.653   ON
  01:00:00                                                                      

  2026-05-05   30.845   9.485       4.203       63.42         136.88   31.812   ON
  02:00:00                                                                      

  2026-05-05   29.357   9.534       3.775       63.8          140.11   30.328   ON
  03:00:00                                                                      

  2026-05-05   30.391   9.563       3.457       64.03         140.04   30.803   ON
  04:00:00                                                                      

  2026-05-05   30.138   9.331       3.633       64.05         135.07   30.46    ON
  05:00:00                                                                      

  2026-05-05   29.876   9.479       3.745       65.04         132.55   30.673   ON
  06:00:00                                                                      

  2026-05-05   29.413   9.547       3.914       64.67         133.42   30.04    ON
  07:00:00                                                                      

  2026-05-05   30.112   9.347       3.538       64.37         133.8    30.3     ON
  08:00:00                                                                      

  2026-05-05   30.776   9.792       4.045       66.81         130.17   29.972   ON
  09:00:00                                                                      

  2026-05-05   30.094   9.425       3.907       61.6          135.32   30.098   ON
  10:00:00                                                                      

  2026-05-05   29.952   9.229       3.688       66.4          134.45   30.859   ON
  11:00:00                                                                      

  2026-05-05   30.947   9.446       3.89        63.3          132.24   30.869   ON
  12:00:00                                                                      

  2026-05-05   29.94    9.696       4.175       66.7          124.49   30.78    ON
  13:00:00                                                                      

  2026-05-05   30.063   9.266       3.545       65.33         136.93   30.574   ON
  14:00:00                                                                      

  2026-05-05   31.035   9.772       3.734       62.63         131.37   30.096   ON
  15:00:00                                                                      

  2026-05-05   31.196   9.632       3.939       63.16         131.85   30.746   ON
  16:00:00                                                                      

  2026-05-05   30.094   9.525       3.82        64.53         138.83   30.047   ON
  17:00:00                                                                      

  2026-05-05   29.964   9.551       3.527       62.86         131.34   29.803   ON
  18:00:00                                                                      

  2026-05-05   29.748   9.72        3.689       63.89         138.97   31.241   ON
  19:00:00                                                                      

  2026-05-05   29.593   9.344       4.104       67.22         134.33   30.758   ON
  20:00:00                                                                      

  2026-05-05   29.764   9.454       3.839       64.15         127.34   30.578   ON
  21:00:00                                                                      

  2026-05-05   30.554   9.424       3.677       65.34         133.96   31.667   ON
  22:00:00                                                                      

  2026-05-05   30.988   9.592       3.661       64.5          132.27   30.518   ON
  23:00:00                                                                      

  2026-05-06   29.568   9.416       3.61        65.06         135.43   31.466   ON
  00:00:00                                                                      

  2026-05-06   29.945   9.428       3.55        65.16         133.77   30.059   ON
  01:00:00                                                                      

  2026-05-06   30.243   9.454       4.142       66.55         136.2    29.778   ON
  02:00:00                                                                      

  2026-05-06   30.114   9.545       3.728       67.44         137.77   29.895   ON
  03:00:00                                                                      

  2026-05-06   29.603   9.621       4.049       66.2          135.48   31.074   ON
  04:00:00                                                                      

  2026-05-06   29.304   9.384       3.761       61.8          139.6    30.981   ON
  05:00:00                                                                      

  2026-05-06   28.998   9.493       3.934       63.81         130.89   30.521   ON
  06:00:00                                                                      

  2026-05-06   30.095   9.501       3.852       67.12         134.74   29.69    ON
  07:00:00                                                                      

  2026-05-06   30.201   9.591       4.015       65.84         136.25   30.158   ON
  08:00:00                                                                      

  2026-05-06   30.028   9.726       4.218       65.67         136.23   30.997   ON
  09:00:00                                                                      

  2026-05-06   30.418   9.414       3.831       66.26         141.76   30.821   ON
  10:00:00                                                                      

  2026-05-06   29.842   9.374       3.452       64.06         133.81   30.059   ON
  11:00:00                                                                      

  2026-05-06   29.862   9.451       3.95        63.65         137.92   30.667   ON
  12:00:00                                                                      

  2026-05-06   28.682   9.497       4.257       63.88         134.5    32.011   ON
  13:00:00                                                                      

  2026-05-06   30.96    9.645       3.956       65.06         135.19   30.474   ON
  14:00:00                                                                      

  2026-05-06   29.354   9.491       3.766       65.56         129.88   29.745   ON
  15:00:00                                                                      

  2026-05-06   30.492   9.62        3.843       66.6          135.04   30.546   ON
  16:00:00                                                                      

  2026-05-06   30.927   9.533       3.364       65.87         132.58   30.879   ON
  17:00:00                                                                      

  2026-05-06   30.119   9.745       3.588       64.6          144.09   31.519   ON
  18:00:00                                                                      

  2026-05-06   30.356   9.549       3.936       66.31         132.62   30.709   ON
  19:00:00                                                                      

  2026-05-06   30.083   9.746       4.173       63.9          137.56   29.904   ON
  20:00:00                                                                      

  2026-05-06   30.361   9.665       4.242       65.62         141.04   30.475   ON
  21:00:00                                                                      

  2026-05-06   29.934   9.301       3.76        64.78         138.45   31.288   ON
  22:00:00                                                                      

  2026-05-06   29.163   9.505       3.663       64.98         131.91   30.226   ON
  23:00:00                                                                      

  2026-05-07   29.916   9.419       3.576       64.35         132.79   31.28    ON
  00:00:00                                                                      

  2026-05-07   28.981   9.408       3.565       65.35         140.81   29.847   ON
  01:00:00                                                                      

  2026-05-07   30.265   9.524       3.641       63.41         130.1    30.612   ON
  02:00:00                                                                      

  2026-05-07   30.105   9.33        3.474       64.3          135.21   30.584   ON
  03:00:00                                                                      

  2026-05-07   30.595   9.609       4.094       65.42         139.89   30.001   ON
  04:00:00                                                                      

  2026-05-07   29.585   9.79        3.329       66.14         128.25   30.703   ON
  05:00:00                                                                      

  2026-05-07   29.23    9.787       4.164       63.56         131.71   31.123   ON
  06:00:00                                                                      

  2026-05-07   30.147   9.548       4.049       66.59         131.07   30.415   ON
  07:00:00                                                                      

  2026-05-07   29.773   9.6         3.657       66.45         132.7    30.312   ON
  08:00:00                                                                      

  2026-05-07   29.763   9.397       3.869       66.06         137.31   30.879   ON
  09:00:00                                                                      

  2026-05-07   29.406   9.571       3.705       66.1          130.88   31.203   ON
  10:00:00                                                                      

  2026-05-07   29.519   9.44        4.168       66.48         132.27   31.27    ON
  11:00:00                                                                      

  2026-05-07   30.378   9.491       4.015       64.75         139.31   30.467   ON
  12:00:00                                                                      

  2026-05-07   29.906   9.523       4.005       62.61         138.93   30.336   ON
  13:00:00                                                                      

  2026-05-07   30.088   9.594       3.555       63.64         133.36   31.187   ON
  14:00:00                                                                      

  2026-05-07   31.098   9.485       4.041       66.48         131.06   31.144   ON
  15:00:00                                                                      

  2026-05-07   30.67    9.737       3.661       64.55         129.85   31.748   ON
  16:00:00                                                                      

  2026-05-07   30.035   9.449       4.01        67.12         136.14   30.666   ON
  17:00:00                                                                      

  2026-05-07   30.64    9.655       4.207       66.45         135      30.852   ON
  18:00:00                                                                      

  2026-05-07   29.546   9.557       3.732       64.43         137.64   30.535   ON
  19:00:00                                                                      

  2026-05-07   29.462   9.465       3.553       66.95         135.81   30.291   ON
  20:00:00                                                                      

  2026-05-07   30.088   9.685       3.742       61.46         136.24   32.373   ON
  21:00:00                                                                      

  2026-05-07   30.209   9.556       4.226       66.46         128.85   30.849   ON
  22:00:00                                                                      

  2026-05-07   30.081   9.411       3.509       65.83         137.6    30.363   ON
  23:00:00                                                                      

  2026-05-08   31.09    9.642       3.795       64.73         127.46   30.652   ON
  00:00:00                                                                      

  2026-05-08   29.215   9.393       3.747       63.97         140.94   30.675   ON
  01:00:00                                                                      

  2026-05-08   30.482   9.528       4.147       63.76         129.25   30.141   ON
  02:00:00                                                                      

  2026-05-08   30.267   9.333       3.578       63.66         133.38   29.69    ON
  03:00:00                                                                      

  2026-05-08   30.436   9.572       3.671       65.32         130.41   30.115   ON
  04:00:00                                                                      

  2026-05-08   29.706   9.136       3.619       64.66         140      30.217   ON
  05:00:00                                                                      

  2026-05-08   29.484   9.328       3.846       63.79         134.44   30.785   ON
  06:00:00                                                                      

  2026-05-08   29.841   9.439       3.556       63.96         137.56   30.83    ON
  07:00:00                                                                      

  2026-05-08   29.896   9.576       3.64        66.15         137.26   29.209   ON
  08:00:00                                                                      

  2026-05-08   29.187   9.371       3.483       65.08         130.69   29.825   ON
  09:00:00                                                                      

  2026-05-08   30.332   9.677       3.897       64.29         131.67   29.972   ON
  10:00:00                                                                      

  2026-05-08   29.469   9.467       3.776       66.81         130.05   31.547   ON
  11:00:00                                                                      

  2026-05-08   29.083   9.459       3.87        65.81         131.52   30.888   ON
  12:00:00                                                                      

  2026-05-08   30.181   9.24        3.353       64.21         137.61   30.301   ON
  13:00:00                                                                      

  2026-05-08   29.96    9.649       4.041       66.29         136.64   30.391   ON
  14:00:00                                                                      

  2026-05-08   29.194   9.429       3.817       64.1          137.41   30.476   ON
  15:00:00                                                                      

  2026-05-08   29.658   9.459       4.183       64.88         131.31   29.63    ON
  16:00:00                                                                      

  2026-05-08   29.57    9.561       4.214       66.15         130.86   31.227   ON
  17:00:00                                                                      

  2026-05-08   29.46    9.667       3.633       66.12         139.27   30.996   ON
  18:00:00                                                                      

  2026-05-08   29.243   9.502       3.819       64.19         136.15   30.713   ON
  19:00:00                                                                      

  2026-05-08   29.908   9.669       3.653       67.2          135.72   30.615   ON
  20:00:00                                                                      

  2026-05-08   30.236   9.508       3.798       66.15         134.28   30.424   ON
  21:00:00                                                                      

  2026-05-08   29.616   9.453       3.905       66.08         137.03   30.325   ON
  22:00:00                                                                      

  2026-05-08   30.462   9.561       3.763       65.34         139.5    29.75    ON
  23:00:00                                                                      

  2026-05-09   30.113   9.814       3.714       64.62         133.56   30.967   ON
  00:00:00                                                                      

  2026-05-09   30.755   9.607       4.186       64.74         132.64   29.962   ON
  01:00:00                                                                      

  2026-05-09   30.146   9.416       3.39        67.46         129.08   30.583   ON
  02:00:00                                                                      

  2026-05-09   29.657   9.626       3.802       65.77         133.68   30.352   ON
  03:00:00                                                                      

  2026-05-09   30.13    9.628       3.585       64.3          130.61   30.339   ON
  04:00:00                                                                      

  2026-05-09   30.045   9.464       3.623       64.85         128.52   30.862   ON
  05:00:00                                                                      

  2026-05-09   29.206   9.595       3.722       63.3          135.66   30.485   ON
  06:00:00                                                                      

  2026-05-09   29.469   9.581       3.848       64.46         135.73   29.977   ON
  07:00:00                                                                      

  2026-05-09   30.3     9.299       3.503       61.77         135.09   30.99    ON
  08:00:00                                                                      

  2026-05-09   29.531   9.65        4.065       62.45         128.5    31.399   ON
  09:00:00                                                                      

  2026-05-09   30.404   9.297       3.708       63.76         131.35   30.705   ON
  10:00:00                                                                      

  2026-05-09   29.154   9.61        3.712       68.21         132.81   30.787   ON
  11:00:00                                                                      

  2026-05-09   30.047   9.396       3.523       64.84         142.72   30.459   ON
  12:00:00                                                                      

  2026-05-09   29.717   9.442       3.841       65.71         136.81   31.571   ON
  13:00:00                                                                      

  2026-05-09   29.35    9.512       3.451       64.28         138.66   30.861   ON
  14:00:00                                                                      

  2026-05-09   29.632   9.45        3.633       68.02         134.64   30.103   ON
  15:00:00                                                                      

  2026-05-09   29.566   9.591       3.984       66.03         130.57   31.257   ON
  16:00:00                                                                      

  2026-05-09   31.075   9.58        4.042       64.24         142.8    31.753   ON
  17:00:00                                                                      

  2026-05-09   30.406   9.791       3.487       64.43         136.01   30.802   ON
  18:00:00                                                                      

  2026-05-09   29.762   9.429       3.374       65.04         136.18   30       ON
  19:00:00                                                                      

  2026-05-09   30.938   9.492       4.376       63.51         138.36   29.547   ON
  20:00:00                                                                      

  2026-05-09   30.004   9.562       3.86        64.67         134.19   30.003   ON
  21:00:00                                                                      

  2026-05-09   29.857   9.445       3.775       65.71         136.17   31.957   ON
  22:00:00                                                                      

  2026-05-09   30.478   9.383       3.64        62.77         129.7    30.103   ON
  23:00:00                                                                      

  2026-05-10   30.148   9.467       3.727       66.85         135.67   29.835   ON
  00:00:00                                                                      

  2026-05-10   29.888   9.518       3.635       66.86         129.71   30.523   ON
  01:00:00                                                                      

  2026-05-10   29.564   9.826       3.681       65.25         128.79   31.011   ON
  02:00:00                                                                      

  2026-05-10   29.789   9.247       3.408       66.02         136.42   30.448   ON
  03:00:00                                                                      

  2026-05-10   29.646   9.49        3.792       65.42         130.71   30.403   ON
  04:00:00                                                                      

  2026-05-10   29.352   9.29        3.717       64.24         132.71   30.755   ON
  05:00:00                                                                      

  2026-05-10   29.632   9.835       3.639       66.32         134.59   31.37    ON
  06:00:00                                                                      

  2026-05-10   29.568   9.476       3.602       65.43         134.22   30.887   ON
  07:00:00                                                                      

  2026-05-10   29.276   9.636       3.575       64.56         140.08   30.312   ON
  08:00:00                                                                      

  2026-05-10   29.454   9.217       3.94        63.04         134.41   30.344   ON
  09:00:00                                                                      

  2026-05-10   30.444   9.579       3.719       64.27         137.13   30.737   ON
  10:00:00                                                                      

  2026-05-10   30.539   9.567       3.515       66.65         137.93   29.962   ON
  11:00:00                                                                      

  2026-05-10   30.041   9.613       3.853       66.05         128.42   30.741   ON
  12:00:00                                                                      

  2026-05-10   29.502   9.722       3.782       64.39         128.87   31.453   ON
  13:00:00                                                                      

  2026-05-10   29.667   9.615       3.705       67.05         136.26   30.474   ON
  14:00:00                                                                      

  2026-05-10   29.996   9.786       4.085       64.69         132.58   30.371   ON
  15:00:00                                                                      

  2026-05-10   30.504   9.535       4.059       64.96         130.39   30.851   ON
  16:00:00                                                                      

  2026-05-10   29.59    9.339       3.913       64.86         137.92   30.089   ON
  17:00:00                                                                      

  2026-05-10   29.293   9.609       4.068       62.89         136.33   31.433   ON
  18:00:00                                                                      

  2026-05-10   29.425   9.607       4.245       65.58         133.1    31.241   ON
  19:00:00                                                                      

  2026-05-10   29.876   9.403       3.729       66.38         137.18   31.121   ON
  20:00:00                                                                      

  2026-05-10   30.188   9.554       3.843       64.77         123.85   30.716   ON
  21:00:00                                                                      

  2026-05-10   30.74    9.541       3.561       68.65         134.47   30.744   ON
  22:00:00                                                                      

  2026-05-10   28.861   9.393       3.75        63.15         138.66   30.906   ON
  23:00:00                                                                      

  2026-05-11   29.585   9.361       3.538       65.38         137.43   29.933   ON
  00:00:00                                                                      

  2026-05-11   30.027   9.765       3.857       64.63         134.89   30.275   ON
  01:00:00                                                                      

  2026-05-11   29.212   9.559       3.565       65.92         139.57   30.413   ON
  02:00:00                                                                      

  2026-05-11   29.627   9.584       3.817       65.25         137.2    31.268   ON
  03:00:00                                                                      

  2026-05-11   28.981   9.703       3.651       65.75         133.39   31.791   ON
  04:00:00                                                                      

  2026-05-11   29.74    9.342       3.53        63.91         135.61   30.568   ON
  05:00:00                                                                      

  2026-05-11   30.454   9.441       3.892       65.63         137.73   30.754   ON
  06:00:00                                                                      

  2026-05-11   30.927   9.569       3.322       66.13         136.78   30.742   ON
  07:00:00                                                                      

  2026-05-11   29.585   9.679       4.17        64.82         132.64   30.279   ON
  08:00:00                                                                      

  2026-05-11   29.896   9.567       3.832       62.51         122.55   30.286   ON
  09:00:00                                                                      

  2026-05-11   30.688   9.506       3.534       62.55         143.08   30.676   ON
  10:00:00                                                                      

  2026-05-11   30.439   9.513       3.687       63.4          133.47   31.326   ON
  11:00:00                                                                      

  2026-05-11   30.306   9.511       3.633       64.98         126.02   29.84    ON
  12:00:00                                                                      

  2026-05-11   30.304   9.609       3.713       62.85         130.63   31.125   ON
  13:00:00                                                                      

  2026-05-11   29.851   9.23        4.037       64.79         135.81   29.917   ON
  14:00:00                                                                      

  2026-05-11   29.42    9.765       3.88        65            127.13   31.086   ON
  15:00:00                                                                      

  2026-05-11   29.769   9.359       3.55        63.32         136.57   30.491   ON
  16:00:00                                                                      

  2026-05-11   30.418   9.514       3.434       65.97         134.08   29.941   ON
  17:00:00                                                                      

  2026-05-11   29.973   9.589       3.805       63.27         140.22   29.739   ON
  18:00:00                                                                      

  2026-05-11   30.399   9.339       3.978       65.39         131.41   30.432   ON
  19:00:00                                                                      

  2026-05-11   30.369   9.352       3.382       67.71         135.04   31.13    ON
  20:00:00                                                                      

  2026-05-11   30.139   9.49        3.923       62.74         140.59   30.188   ON
  21:00:00                                                                      

  2026-05-11   30.287   9.463       3.85        64.75         137.74   30.674   ON
  22:00:00                                                                      

  2026-05-11   29.133   9.545       3.883       66.86         132.93   30.059   ON
  23:00:00                                                                      

  2026-05-12   29.664   9.484       4.302       64.98         134.09   30.023   ON
  00:00:00                                                                      

  2026-05-12   30.248   9.587       3.885       63.63         135.3    30.309   ON
  01:00:00                                                                      

  2026-05-12   29.723   9.562       4.119       64.7          127.56   29.936   ON
  02:00:00                                                                      

  2026-05-12   29.326   9.389       3.818       62.73         136.65   30.685   ON
  03:00:00                                                                      

  2026-05-12   29.941   9.471       4.172       64.4          136.65   29.626   ON
  04:00:00                                                                      

  2026-05-12   29.314   9.547       3.688       65.12         131.94   31.498   ON
  05:00:00                                                                      

  2026-05-12   30.565   9.352       3.804       64.02         132.07   30.249   ON
  06:00:00                                                                      

  2026-05-12   30.271   9.28        3.847       64.62         135.35   30.165   ON
  07:00:00                                                                      

  2026-05-12   29.865   9.439       3.911       62.19         139.55   31.184   ON
  08:00:00                                                                      

  2026-05-12   30.271   9.43        3.802       66.82         132.13   30.348   ON
  09:00:00                                                                      

  2026-05-12   29.746   9.305       3.39        64.14         133.36   31.233   ON
  10:00:00                                                                      

  2026-05-12   30.729   9.347       3.937       65.12         132.76   30.044   ON
  11:00:00                                                                      

  2026-05-12   29.541   9.763       3.922       64.66         134.65   30.087   ON
  12:00:00                                                                      

  2026-05-12   30.714   9.584       4.197       64.68         137.09   30.106   ON
  13:00:00                                                                      

  2026-05-12   29.992   9.512       3.662       65.45         130.7    31.566   ON
  14:00:00                                                                      

  2026-05-12   30.075   9.736       3.954       65.61         126.2    29.541   ON
  15:00:00                                                                      

  2026-05-12   29.594   9.743       4.205       64.51         133.77   30.657   ON
  16:00:00                                                                      

  2026-05-12   29.804   9.475       3.87        63.69         140.36   31.668   ON
  17:00:00                                                                      

  2026-05-12   30.296   9.836       3.559       66.72         131.27   30.206   ON
  18:00:00                                                                      

  2026-05-12   29.947   9.354       3.497       62.51         137.63   31.253   ON
  19:00:00                                                                      

  2026-05-12   29.812   9.204       3.644       66.08         135.37   31.009   ON
  20:00:00                                                                      

  2026-05-12   31.093   9.371       3.878       63.28         130.43   30.963   ON
  21:00:00                                                                      

  2026-05-12   29.453   9.614       3.505       64.31         135.74   30.66    ON
  22:00:00                                                                      

  2026-05-12   29.672   9.565       3.964       65.66         131.99   30.4     ON
  23:00:00                                                                      

  2026-05-13   29.299   9.858       3.508       65.08         133      30.125   ON
  00:00:00                                                                      

  2026-05-13   28.913   9.786       3.92        64.48         133.51   30.682   ON
  01:00:00                                                                      

  2026-05-13   30.098   9.528       3.993       65.89         130.16   30.988   ON
  02:00:00                                                                      

  2026-05-13   30.157   9.385       3.604       65.26         134.05   30.433   ON
  03:00:00                                                                      

  2026-05-13   29.497   9.332       4.167       64.1          140.82   31.201   ON
  04:00:00                                                                      

  2026-05-13   29.284   9.637       3.701       64.37         136.3    31.044   ON
  05:00:00                                                                      

  2026-05-13   30.288   9.376       3.203       63.19         140.26   30.791   ON
  06:00:00                                                                      

  2026-05-13   29.526   9.526       3.778       64.95         130.63   30.405   ON
  07:00:00                                                                      

  2026-05-13   31.012   9.465       3.902       68.01         145.31   30.949   ON
  08:00:00                                                                      

  2026-05-13   30.804   9.592       3.676       65.57         137.1    30.713   ON
  09:00:00                                                                      

  2026-05-13   30.237   9.847       3.954       65.87         136.07   31.818   ON
  10:00:00                                                                      

  2026-05-13   29.855   9.548       4.153       64.39         132.34   30.755   ON
  11:00:00                                                                      

  2026-05-13   30.323   9.79        3.875       62.51         130.81   30.985   ON
  12:00:00                                                                      

  2026-05-13   29.069   9.467       3.923       64.33         135.04   29.839   ON
  13:00:00                                                                      

  2026-05-13   30.43    9.312       4.06        65.41         140.4    30.668   ON
  14:00:00                                                                      

  2026-05-13   30.877   9.658       3.81        63.68         135.97   31.558   ON
  15:00:00                                                                      

  2026-05-13   29.088   9.062       4.004       63.24         144.6    30.857   ON
  16:00:00                                                                      

  2026-05-13   29.783   9.597       3.761       64.9          133.45   31.154   ON
  17:00:00                                                                      

  2026-05-13   30.443   9.406       3.525       65.92         128.86   30.429   ON
  18:00:00                                                                      

  2026-05-13   29.996   9.432       3.875       63.81         132.89   30.309   ON
  19:00:00                                                                      

  2026-05-13   29.783   9.33        3.634       67.62         140.09   30.749   ON
  20:00:00                                                                      

  2026-05-13   30.803   9.498       3.77        64.14         139.67   29.931   ON
  21:00:00                                                                      

  2026-05-13   30.156   9.361       3.788       64.69         130.33   30.41    ON
  22:00:00                                                                      

  2026-05-13   30.538   9.348       3.865       63.14         131.59   31.924   ON
  23:00:00                                                                      

  2026-05-14   29.742   9.502       3.268       66.25         139.59   30.55    ON
  00:00:00                                                                      

  2026-05-14   30.036   9.657       3.789       62.23         127.57   30.256   ON
  01:00:00                                                                      

  2026-05-14   29.275   9.554       3.529       64.66         137.28   31.425   ON
  02:00:00                                                                      

  2026-05-14   29.044   9.565       3.549       65.33         131.02   30.853   ON
  03:00:00                                                                      

  2026-05-14   29.436   9.301       4.085       65.85         133.45   30.315   ON
  04:00:00                                                                      

  2026-05-14   30.216   9.558       3.505       65.83         132.72   30.623   ON
  05:00:00                                                                      

  2026-05-14   30.586   9.467       4.128       63.39         138.04   30.522   ON
  06:00:00                                                                      

  2026-05-14   29.309   9.551       3.614       65.8          140.09   30.243   ON
  07:00:00                                                                      

  2026-05-14   30.657   9.474       4.025       64.39         132.56   30.702   ON
  08:00:00                                                                      

  2026-05-14   29.592   9.335       3.954       61.81         139.5    30.667   ON
  09:00:00                                                                      

  2026-05-14   29.208   9.521       3.671       68.01         137.08   30.314   ON
  10:00:00                                                                      

  2026-05-14   30.143   9.266       4.037       65.54         130.93   30.41    ON
  11:00:00                                                                      

  2026-05-14   30.202   9.609       3.084       65.91         131.69   31.431   ON
  12:00:00                                                                      

  2026-05-14   29.659   9.758       3.847       66.46         136.08   31.567   ON
  13:00:00                                                                      

  2026-05-14   30.047   9.648       3.754       64.86         133.39   30.711   ON
  14:00:00                                                                      

  2026-05-14   30.231   9.242       3.979       64.05         133.14   29.211   ON
  15:00:00                                                                      

  2026-05-14   30.27    9.379       3.672       65.71         138.36   30.611   ON
  16:00:00                                                                      

  2026-05-14   29.761   9.531       3.883       66.44         136.29   29.754   ON
  17:00:00                                                                      

  2026-05-14   29.609   9.437       3.73        66.94         129.77   30.297   ON
  18:00:00                                                                      

  2026-05-14   31.706   9.474       3.957       63.16         139.49   29.668   ON
  19:00:00                                                                      

  2026-05-14   30.323   9.546       4.003       66.45         137.51   31.669   ON
  20:00:00                                                                      

  2026-05-14   29.447   9.32        3.464       62.53         136.73   30.571   ON
  21:00:00                                                                      

  2026-05-14   30.211   9.547       4.262       65.85         137.22   31.438   ON
  22:00:00                                                                      

  2026-05-14   30.343   9.579       3.782       64.1          129.19   29.31    ON
  23:00:00                                                                      

  2026-05-15   30.398   9.61        4.337       66.05         135.3    31.616   ON
  00:00:00                                                                      

  2026-05-15   29.099   9.32        3.657       66.25         131.52   30.72    ON
  01:00:00                                                                      

  2026-05-15   29.812   9.542       3.813       65.78         133.23   31.166   ON
  02:00:00                                                                      

  2026-05-15   30.274   9.509       4.157       66.36         141.66   30.468   ON
  03:00:00                                                                      

  2026-05-15   30.518   9.614       3.723       66.19         132.93   30.362   ON
  04:00:00                                                                      

  2026-05-15   30.741   9.238       4.056       65.29         140.87   29.32    ON
  05:00:00                                                                      

  2026-05-15   30.101   9.342       3.739       67.14         133.81   30.406   ON
  06:00:00                                                                      

  2026-05-15   29.495   9.357       3.833       64.96         134.68   29.335   ON
  07:00:00                                                                      

  2026-05-15   31.198   9.587       3.776       64.14         138.19   30.328   ON
  08:00:00                                                                      

  2026-05-15   29.399   9.344       3.857       65.37         137.04   29.716   ON
  09:00:00                                                                      

  2026-05-15   30.023   9.216       4.3         63.92         128.62   30.366   ON
  10:00:00                                                                      

  2026-05-15   30.663   9.347       3.638       65.04         136.53   31.846   ON
  11:00:00                                                                      

  2026-05-15   29.943   9.584       3.874       65.03         132.04   30.937   ON
  12:00:00                                                                      

  2026-05-15   30.825   9.784       3.722       67.61         133.56   30.826   ON
  13:00:00                                                                      

  2026-05-15   30.338   9.698       3.817       67.85         136.08   30.819   ON
  14:00:00                                                                      

  2026-05-15   30.452   9.598       3.805       63.01         132.62   30.448   ON
  15:00:00                                                                      

  2026-05-15   30.777   9.277       3.832       63.74         126.89   30.074   ON
  16:00:00                                                                      

  2026-05-15   30.179   9.535       3.937       66.3          134.66   31.073   ON
  17:00:00                                                                      

  2026-05-15   29.202   9.499       4.355       65.54         134.13   30.718   ON
  18:00:00                                                                      

  2026-05-15   30.594   9.592       3.443       67.78         132.18   29.855   ON
  19:00:00                                                                      

  2026-05-15   30.419   9.472       3.755       66.52         130.25   31.366   ON
  20:00:00                                                                      

  2026-05-15   30.161   9.558       3.924       64.88         134.25   31.549   ON
  21:00:00                                                                      

  2026-05-15   30.201   9.328       4.13        69.16         134.92   30.474   ON
  22:00:00                                                                      

  2026-05-15   29.72    9.46        3.478       62.87         133.3    31.103   ON
  23:00:00                                                                      

  2026-05-16   29.568   9.407       4.351       65.85         138.86   30.477   ON
  00:00:00                                                                      

  2026-05-16   30.415   9.692       3.975       66.95         134.1    31.034   ON
  01:00:00                                                                      

  2026-05-16   29.528   9.169       4.33        66.18         135.26   30.194   ON
  02:00:00                                                                      

  2026-05-16   30.491   9.26        4.028       64.03         129.11   30.098   ON
  03:00:00                                                                      

  2026-05-16   29.797   9.531       3.827       63.26         133.69   31.176   ON
  04:00:00                                                                      

  2026-05-16   29.744   9.426       3.654       66.35         143.89   31.416   ON
  05:00:00                                                                      

  2026-05-16   29.434   9.765       3.882       64.69         127.21   30.857   ON
  06:00:00                                                                      

  2026-05-16   29.731   9.547       3.875       64.92         138.16   31.056   ON
  07:00:00                                                                      

  2026-05-16   30.097   9.492       3.444       65.64         135.73   31.225   ON
  08:00:00                                                                      

  2026-05-16   30.074   9.383       3.832       64.88         134.34   30.912   ON
  09:00:00                                                                      

  2026-05-16   30.137   9.537       3.726       67.41         134.34   32.564   ON
  10:00:00                                                                      

  2026-05-16   30.4     9.601       3.908       67.15         135.24   31.375   ON
  11:00:00                                                                      

  2026-05-16   29.801   9.455       3.516       62.82         128.67   30.485   ON
  12:00:00                                                                      

  2026-05-16   30.047   9.493       3.577       65.9          140.94   30.516   ON
  13:00:00                                                                      

  2026-05-16   29.671   9.529       3.683       64.92         136.35   30.654   ON
  14:00:00                                                                      

  2026-05-16   30.545   9.076       3.877       62.89         140.1    30.839   ON
  15:00:00                                                                      

  2026-05-16   30.649   9.161       3.624       65.38         136.83   30.119   ON
  16:00:00                                                                      

  2026-05-16   30.364   9.592       3.323       65.22         137.67   30.729   ON
  17:00:00                                                                      

  2026-05-16   31.004   9.597       3.465       63.86         137.8    30.179   ON
  18:00:00                                                                      

  2026-05-16   29.722   9.537       4.025       65.59         135.83   30.36    ON
  19:00:00                                                                      

  2026-05-16   29.629   9.514       3.97        67.16         141.27   31.421   ON
  20:00:00                                                                      

  2026-05-16   30.001   9.569       3.745       63.9          136.26   30.875   ON
  21:00:00                                                                      

  2026-05-16   31.417   9.391       3.94        63.35         136.07   30.555   ON
  22:00:00                                                                      

  2026-05-16   30.398   9.408       3.587       64.05         132.3    31.194   ON
  23:00:00                                                                      

  2026-05-17   30.35    9.57        3.687       65.67         134.02   31.013   ON
  00:00:00                                                                      

  2026-05-17   30.08    9.33        3.711       67.38         139.77   31.412   ON
  01:00:00                                                                      

  2026-05-17   30.669   9.502       4.092       63.99         132.97   31.152   ON
  02:00:00                                                                      

  2026-05-17   30.357   9.565       3.816       63.69         138.21   29.985   ON
  03:00:00                                                                      

  2026-05-17   30.802   9.378       3.54        63.77         135.06   30.728   ON
  04:00:00                                                                      

  2026-05-17   30.532   9.704       3.74        64.08         128.95   29.741   ON
  05:00:00                                                                      

  2026-05-17   30.964   9.579       3.648       67.72         137.96   31.502   ON
  06:00:00                                                                      

  2026-05-17   29.069   9.515       4.039       66.35         134.98   30.701   ON
  07:00:00                                                                      

  2026-05-17   29.884   9.393       3.937       61.31         134.6    30.364   ON
  08:00:00                                                                      

  2026-05-17   30.098   9.672       3.9         64.17         139.18   30.643   ON
  09:00:00                                                                      

  2026-05-17   29.265   9.409       3.641       65.06         136.22   29.999   ON
  10:00:00                                                                      

  2026-05-17   29.747   9.745       4.013       63.75         130.71   30.706   ON
  11:00:00                                                                      

  2026-05-17   30.663   9.773       3.947       64.3          136.06   31.537   ON
  12:00:00                                                                      

  2026-05-17   30.405   9.469       3.399       64.32         132.28   30.341   ON
  13:00:00                                                                      

  2026-05-17   30.788   9.672       3.769       65.43         131.53   30.742   ON
  14:00:00                                                                      

  2026-05-17   29.537   9.863       3.879       67.3          141.44   30.541   ON
  15:00:00                                                                      

  2026-05-17   30.828   9.609       3.84        60.46         126.17   31.016   ON
  16:00:00                                                                      

  2026-05-17   29.759   9.517       3.847       65.39         133.07   31.314   ON
  17:00:00                                                                      

  2026-05-17   30.543   9.66        3.886       67.38         132.83   29.361   ON
  18:00:00                                                                      

  2026-05-17   29.836   9.496       4.023       65.53         138.09   30.555   ON
  19:00:00                                                                      

  2026-05-17   30.706   9.586       4.014       64.87         139.58   29.963   ON
  20:00:00                                                                      

  2026-05-17   30.247   9.348       3.831       65.85         131.99   30.071   ON
  21:00:00                                                                      

  2026-05-17   29.892   9.452       3.554       66.56         124.42   31.064   ON
  22:00:00                                                                      

  2026-05-17   29.929   9.576       3.245       66.57         142.36   31.517   ON
  23:00:00                                                                      

  2026-05-18   30.233   9.537       3.536       65.84         131.62   30.232   ON
  00:00:00                                                                      

  2026-05-18   31.15    9.497       3.718       62.98         133.87   31.14    ON
  01:00:00                                                                      

  2026-05-18   29.643   9.388       3.892       65.69         133.6    29.801   ON
  02:00:00                                                                      

  2026-05-18   30.694   9.396       4.293       66.5          133.51   30.729   ON
  03:00:00                                                                      

  2026-05-18   30.296   9.575       3.982       63.63         135.54   30.809   ON
  04:00:00                                                                      

  2026-05-18   30.355   9.508       3.473       61.65         131.11   30.036   ON
  05:00:00                                                                      

  2026-05-18   30.526   9.591       3.938       65.57         137.14   31.055   ON
  06:00:00                                                                      

  2026-05-18   30.646   9.469       3.632       66.65         138.08   31.076   ON
  07:00:00                                                                      

  2026-05-18   30.016   9.446       3.561       63.06         131.96   30.385   ON
  08:00:00                                                                      

  2026-05-18   29.931   9.393       3.694       66.28         131.57   30.238   ON
  09:00:00                                                                      

  2026-05-18   29.732   9.639       4.023       63.57         139.35   31.101   ON
  10:00:00                                                                      

  2026-05-18   30.583   9.45        3.74        64.68         140.6    31.082   ON
  11:00:00                                                                      

  2026-05-18   30.823   9.39        3.97        66.15         137.4    30.911   ON
  12:00:00                                                                      

  2026-05-18   30.774   9.676       3.773       63.15         138.28   31.35    ON
  13:00:00                                                                      

  2026-05-18   30.356   9.41        3.671       65.76         126.89   30.75    ON
  14:00:00                                                                      

  2026-05-18   30.163   9.614       3.809       64.17         135.98   30.771   ON
  15:00:00                                                                      

  2026-05-18   29.751   9.694       4.23        67.15         135.69   30.353   ON
  16:00:00                                                                      

  2026-05-18   30.387   9.714       3.786       64.35         134.69   30.844   ON
  17:00:00                                                                      

  2026-05-18   29.903   9.242       4.073       65.22         138.6    30.781   ON
  18:00:00                                                                      

  2026-05-18   29.73    9.431       4.142       65.52         139.19   31.721   ON
  19:00:00                                                                      

  2026-05-18   29.683   9.553       4.166       64.17         135.03   31.298   ON
  20:00:00                                                                      

  2026-05-18   29.377   9.493       3.86        64.84         134.12   30.347   ON
  21:00:00                                                                      

  2026-05-18   30.263   9.42        4.031       64.48         141      29.926   ON
  22:00:00                                                                      

  2026-05-18   30.075   9.748       3.894       66.76         133.21   29.951   ON
  23:00:00                                                                      

  2026-05-19   30.876   9.387       3.48        64.06         132.68   30.572   ON
  00:00:00                                                                      

  2026-05-19   29.967   9.265       3.655       64.31         138.73   30.085   ON
  01:00:00                                                                      

  2026-05-19   31.632   9.421       3.695       63.99         134.52   30.081   ON
  02:00:00                                                                      

  2026-05-19   30.289   9.344       4.253       64.5          141.96   30.182   ON
  03:00:00                                                                      

  2026-05-19   29.879   9.46        3.536       65.81         141.69   30.551   ON
  04:00:00                                                                      

  2026-05-19   30.56    9.408       3.552       64.65         139.01   29.852   ON
  05:00:00                                                                      

  2026-05-19   29.906   9.393       3.947       64.5          136      29.857   ON
  06:00:00                                                                      

  2026-05-19   30.782   9.246       3.94        64.11         135.64   30.94    ON
  07:00:00                                                                      

  2026-05-19   29.624   9.81        3.795       64.61         133.61   30.466   ON
  08:00:00                                                                      

  2026-05-19   29.385   9.46        3.516       66.12         143.78   30.634   ON
  09:00:00                                                                      

  2026-05-19   31.361   9.341       3.024       64.43         136.24   31.53    ON
  10:00:00                                                                      

  2026-05-19   30.23    9.414       4.186       66.53         136.96   30.101   ON
  11:00:00                                                                      

  2026-05-19   30.014   9.368       3.696       68.33         136.21   30.595   ON
  12:00:00                                                                      

  2026-05-19   29.333   9.627       3.889       64.85         135.24   31.84    ON
  13:00:00                                                                      

  2026-05-19   29.174   9.435       3.646       67.29         130      31.617   ON
  14:00:00                                                                      

  2026-05-19   29.242   9.369       3.539       62.84         137.04   31.371   ON
  15:00:00                                                                      

  2026-05-19   29.492   9.633       3.661       64.49         139.19   29.674   ON
  16:00:00                                                                      

  2026-05-19   29.36    9.539       4.112       66.1          130.77   30.22    ON
  17:00:00                                                                      

  2026-05-19   28.096   9.896       3.987       65.74         127.15   30.68    ON
  18:00:00                                                                      

  2026-05-19   29.681   9.349       4.401       63.74         133.06   29.917   ON
  19:00:00                                                                      

  2026-05-19   29.213   9.233       3.585       66.11         134.48   29.986   ON
  20:00:00                                                                      

  2026-05-19   29.36    9.663       3.697       69.03         137.35   31.453   ON
  21:00:00                                                                      

  2026-05-19   27.892   9.539       3.79        66.14         132.3    29.485   ON
  22:00:00                                                                      

  2026-05-19   28.346   9.787       4.034       63.37         136.65   30.056   ON
  23:00:00                                                                      

  2026-05-20   28.077   9.567       4.129       63.8          131.56   30.176   ON
  00:00:00                                                                      

  2026-05-20   28.249   9.766       3.555       63.95         127.39   32.139   ON
  01:00:00                                                                      

  2026-05-20   27.104   9.486       3.783       65.36         139.5    30.533   ON
  02:00:00                                                                      

  2026-05-20   28.546   9.751       3.603       67.5          134.98   30.187   ON
  03:00:00                                                                      

  2026-05-20   27.628   9.448       3.575       66.4          132.91   30.018   ON
  04:00:00                                                                      

  2026-05-20   26.284   9.298       4           68.2          132.04   30.236   ON
  05:00:00                                                                      

  2026-05-20   28.032   9.502       3.787       65.43         137.49   31.394   ON
  06:00:00                                                                      

  2026-05-20   27.037   9.54        3.91        65.8          129.68   30.457   ON
  07:00:00                                                                      

  2026-05-20   28.071   9.884       4.077       67.52         135.82   30.919   ON
  08:00:00                                                                      

  2026-05-20   26.299   9.657       3.988       65.18         139.81   30.112   ON
  09:00:00                                                                      

  2026-05-20   26.943   9.789       4.301       67.41         133.33   31.359   ON
  10:00:00                                                                      

  2026-05-20   26.29    9.8         4.067       66.98         138.02   31.811   ON
  11:00:00                                                                      

  2026-05-20   27.309   9.411       3.839       63.66         140.95   30.723   ON
  12:00:00                                                                      

  2026-05-20   26.214   9.847       3.674       64.61         144.26   30.309   ON
  13:00:00                                                                      

  2026-05-20   26.065   9.671       3.852       64.76         139.17   29.825   ON
  14:00:00                                                                      

  2026-05-20   26.225   9.817       4.011       64.6          131.35   30.966   ON
  15:00:00                                                                      

  2026-05-20   26.069   9.804       3.868       65.42         129.59   30.245   ON
  16:00:00                                                                      

  2026-05-20   27.061   9.696       3.551       64            134.25   31.624   ON
  17:00:00                                                                      

  2026-05-20   26.06    9.861       3.716       67.16         142.87   30.962   ON
  18:00:00                                                                      

  2026-05-20   25.96    9.608       3.575       66.04         134.4    29.874   ON
  19:00:00                                                                      

  2026-05-20   26.13    9.574       4.299       66.3          138.88   30.065   ON
  20:00:00                                                                      

  2026-05-20   26.05    9.941       4.04        66.35         137.36   29.971   ON
  21:00:00                                                                      

  2026-05-20   25.938   9.702       3.506       63.36         143.74   31.055   ON
  22:00:00                                                                      

  2026-05-20   25.491   9.797       3.765       66.34         135.18   31.605   ON
  23:00:00                                                                      

  2026-05-21   25.409   9.886       3.987       64.04         134.49   30.819   ON
  00:00:00                                                                      

  2026-05-21   25.275   9.976       3.895       67.76         132.63   30.206   ON
  01:00:00                                                                      

  2026-05-21   25.402   9.725       3.738       62.82         136.47   31.364   ON
  02:00:00                                                                      

  2026-05-21   25.247   9.741       3.163       66.82         137.03   30.523   ON
  03:00:00                                                                      

  2026-05-21   25.913   10.027      4.138       63.72         135.91   30.809   ON
  04:00:00                                                                      

  2026-05-21   24.386   9.798       3.584       65.08         137.96   29.833   ON
  05:00:00                                                                      

  2026-05-21   24.248   9.948       4.083       66.19         136.32   30.68    ON
  06:00:00                                                                      

  2026-05-21   24.841   9.925       4.051       63.39         133.52   30.86    ON
  07:00:00                                                                      

  2026-05-21   24.842   9.867       3.698       64.32         135.06   29.874   ON
  08:00:00                                                                      

  2026-05-21   12.014   3.815       3.749       43.21         67.03    12.293   OFF
  09:00:00                                                                      

  2026-05-21   11.98    3.803       3.838       43.46         68.27    12.22    OFF
  10:00:00                                                                      

  2026-05-21   11.965   3.777       3.73        39.93         67.83    12.265   OFF
  11:00:00                                                                      

  2026-05-21   11.944   3.91        3.776       39.57         71.29    12.293   OFF
  12:00:00                                                                      

  2026-05-21   11.987   3.857       3.741       35.12         68.08    12.397   OFF
  13:00:00                                                                      

  2026-05-21   12.011   3.766       4.24        40.49         65.81    12.228   OFF
  14:00:00                                                                      

  2026-05-21   11.987   3.773       4.033       40.04         67.15    12.177   OFF
  15:00:00                                                                      

  2026-05-21   12.023   3.726       3.517       39.01         64.4     12.307   OFF
  16:00:00                                                                      

  2026-05-21   12.024   3.796       3.513       38.72         67.22    12.223   OFF
  17:00:00                                                                      

  2026-05-21   12.034   3.746       3.9         41.46         68.39    12.276   OFF
  18:00:00                                                                      

  2026-05-21   11.99    3.802       3.985       41.9          66.65    12.094   OFF
  19:00:00                                                                      

  2026-05-21   11.997   3.754       3.761       37.62         70.22    12.153   OFF
  20:00:00                                                                      

  2026-05-21   12.032   3.725       3.23        41.83         67.92    12.267   OFF
  21:00:00                                                                      

  2026-05-21   30.243   9.374       4.186       63.73         132.37   30.877   ON
  22:00:00                                                                      

  2026-05-21   30.304   9.514       3.456       63.53         138.49   30.461   ON
  23:00:00                                                                      

  2026-05-22   30.123   9.573       3.81        65.14         137.99   30.579   ON
  00:00:00                                                                      

  2026-05-22   29.969   9.537       3.65        64.69         134.64   30.822   ON
  01:00:00                                                                      

  2026-05-22   30.201   9.484       3.632       67.58         136.81   29.616   ON
  02:00:00                                                                      

  2026-05-22   30.691   9.596       3.51        67.52         131.7    30.366   ON
  03:00:00                                                                      

  2026-05-22   29.52    9.546       3.562       66.35         139.62   30.244   ON
  04:00:00                                                                      

  2026-05-22   29.16    9.822       3.996       67.99         128.96   30.704   ON
  05:00:00                                                                      

  2026-05-22   29.909   9.542       4.271       65.18         133.97   31.877   ON
  06:00:00                                                                      

  2026-05-22   29.828   9.495       3.827       62.28         130.45   30.063   ON
  07:00:00                                                                      

  2026-05-22   30.613   9.571       3.889       63.17         134.88   31.742   ON
  08:00:00                                                                      

  2026-05-22   30.667   9.502       3.95        65.78         128.2    30.238   ON
  09:00:00                                                                      

  2026-05-22   30.838   9.536       4.008       65.19         136      30.633   ON
  10:00:00                                                                      

  2026-05-22   29.247   9.446       3.677       65.12         135.05   30.908   ON
  11:00:00                                                                      

  2026-05-22   30.555   9.296       4.027       64.88         129.98   29.488   ON
  12:00:00                                                                      

  2026-05-22   30.909   9.695       3.749       62.08         136.48   31.611   ON
  13:00:00                                                                      

  2026-05-22   30.461   9.265       3.695       65.65         128.32   30.722   ON
  14:00:00                                                                      

  2026-05-22   30.937   9.359       3.047       65.67         132.92   30.745   ON
  15:00:00                                                                      

  2026-05-22   30.636   9.61        3.782       66            135.21   31.755   ON
  16:00:00                                                                      

  2026-05-22   30.044   9.685       3.421       64.5          133.6    30.432   ON
  17:00:00                                                                      

  2026-05-22   30.811   9.51        3.901       64.32         137.49   30.838   ON
  18:00:00                                                                      

  2026-05-22   30.328   9.417       3.882       65.87         129.67   29.753   ON
  19:00:00                                                                      

  2026-05-22   29.26    9.478       3.488       61.99         128.54   31.023   ON
  20:00:00                                                                      

  2026-05-22   30.471   9.497       3.795       64.54         140.61   30.52    ON
  21:00:00                                                                      

  2026-05-22   29.492   9.451       3.712       64.5          129.49   30.461   ON
  22:00:00                                                                      

  2026-05-22   29.939   9.349       3.675       67.05         141.66   30.48    ON
  23:00:00                                                                      

  2026-05-23   28.918   9.48        3.937       67.17         137.36   31.157   ON
  00:00:00                                                                      

  2026-05-23   29.698   9.404       3.889       67.46         138.47   30.287   ON
  01:00:00                                                                      

  2026-05-23   30.463   9.523       3.653       64.87         134.47   31.074   ON
  02:00:00                                                                      

  2026-05-23   29.884   9.487       3.371       64.17         131.37   30.771   ON
  03:00:00                                                                      

  2026-05-23   29.018   9.396       3.956       65.34         134.75   29.372   ON
  04:00:00                                                                      

  2026-05-23   29.408   9.706       3.461       66.16         135.2    30.837   ON
  05:00:00                                                                      

  2026-05-23   30.803   9.327       3.644       64.67         132.85   30.824   ON
  06:00:00                                                                      

  2026-05-23   29.89    9.345       3.783       60.86         130.43   30.201   ON
  07:00:00                                                                      

  2026-05-23   30.438   9.706       3.959       65.55         137.29   30.211   ON
  08:00:00                                                                      

  2026-05-23   31.143   9.537       3.902       64.43         132.37   30.563   ON
  09:00:00                                                                      

  2026-05-23   30.279   9.516       3.694       62.5          138.01   30.9     ON
  10:00:00                                                                      

  2026-05-23   30.242   9.374       3.922       63.75         136.54   30.861   ON
  11:00:00                                                                      

  2026-05-23   31.061   9.242       3.849       64.66         140.95   29.716   ON
  12:00:00                                                                      

  2026-05-23   28.89    9.405       4.242       64.22         138.71   30.598   ON
  13:00:00                                                                      

  2026-05-23   30.312   9.06        3.845       64.61         126.01   29.739   ON
  14:00:00                                                                      

  2026-05-23   30.279   9.69        3.744       65.07         136.6    30.688   ON
  15:00:00                                                                      

  2026-05-23   30.471   9.518       3.455       63.46         135.48   30.796   ON
  16:00:00                                                                      

  2026-05-23   30.379   9.282       3.741       65.87         144.78   30.106   ON
  17:00:00                                                                      

  2026-05-23   29.891   9.351       3.524       64.4          134.22   30.389   ON
  18:00:00                                                                      

  2026-05-23   29.513   9.618       3.327       62.77         133.94   29.181   ON
  19:00:00                                                                      

  2026-05-23   30.922   9.424       3.584       63.42         133.91   30.329   ON
  20:00:00                                                                      

  2026-05-23   30.551   9.687       4.031       63.66         134.55   29.278   ON
  21:00:00                                                                      

  2026-05-23   29.116   9.553       4.043       66.22         132.44   30.467   ON
  22:00:00                                                                      

  2026-05-23   29.577   9.51        3.776       65.2          142.14   30.745   ON
  23:00:00                                                                      

  2026-05-24   30.559   9.712       3.534       64.39         136.59   30.643   ON
  00:00:00                                                                      

  2026-05-24   30.413   9.612       3.659       65.03         137.27   31.176   ON
  01:00:00                                                                      

  2026-05-24   29.871   9.556       3.414       64.26         140.18   30.741   ON
  02:00:00                                                                      

  2026-05-24   29.94    9.372       3.923       64.43         129.77   30.764   ON
  03:00:00                                                                      

  2026-05-24   29.951   9.872       3.964       65.83         141.43   30.451   ON
  04:00:00                                                                      

  2026-05-24   30.301   9.507       3.663       65.28         133.87   31.054   ON
  05:00:00                                                                      

  2026-05-24   29.884   9.414       3.718       64.95         136.6    30.274   ON
  06:00:00                                                                      

  2026-05-24   29.965   9.524       3.741       64.85         132.93   31.627   ON
  07:00:00                                                                      

  2026-05-24   29.419   9.533       3.582       64.42         132.54   30.479   ON
  08:00:00                                                                      

  2026-05-24   30.739   9.568       3.875       65.99         133.24   30.922   ON
  09:00:00                                                                      

  2026-05-24   29.544   9.7         3.5         64.76         136.85   30.559   ON
  10:00:00                                                                      

  2026-05-24   29.903   9.543       3.633       65.79         136.97   31.142   ON
  11:00:00                                                                      

  2026-05-24   30.041   9.614       4.05        62.42         135.95   30.156   ON
  12:00:00                                                                      

  2026-05-24   29.852   9.544       3.63        66.93         139.53   30.857   ON
  13:00:00                                                                      

  2026-05-24   29.315   9.538       3.901       64.36         133.54   30.109   ON
  14:00:00                                                                      

  2026-05-24   29.601   9.66        4.042       63.36         129.72   31.583   ON
  15:00:00                                                                      

  2026-05-24   29.83    9.213       3.956       66.15         131.32   30.241   ON
  16:00:00                                                                      

  2026-05-24   28.771   9.068       4.021       66.93         133.63   30.487   ON
  17:00:00                                                                      

  2026-05-24   30.154   9.504       3.861       66.66         139.31   29.821   ON
  18:00:00                                                                      

  2026-05-24   31.448   9.307       4.044       66            138.19   30.187   ON
  19:00:00                                                                      

  2026-05-24   29.607   9.262       3.788       64.95         138.52   29.87    ON
  20:00:00                                                                      

  2026-05-24   29.602   9.589       3.489       64.89         137.49   29.709   ON
  21:00:00                                                                      

  2026-05-24   30.102   9.419       3.76        67.16         132.25   31.166   ON
  22:00:00                                                                      

  2026-05-24   29.669   9.478       3.718       64.51         133.04   29.907   ON
  23:00:00                                                                      

  2026-05-25   29.34    9.526       3.395       65.98         127.1    29.987   ON
  00:00:00                                                                      

  2026-05-25   29.96    9.369       3.894       66.6          135.56   30.754   ON
  01:00:00                                                                      

  2026-05-25   29.675   9.586       3.989       66.33         132.11   32.058   ON
  02:00:00                                                                      

  2026-05-25   29.686   9.445       3.454       62.06         135.95   29.16    ON
  03:00:00                                                                      

  2026-05-25   30.436   9.397       3.537       65.05         136.18   31.03    ON
  04:00:00                                                                      

  2026-05-25   30.138   9.421       3.698       61.62         132.52   30.597   ON
  05:00:00                                                                      

  2026-05-25   30.281   9.678       3.651       66.38         143.08   31.038   ON
  06:00:00                                                                      

  2026-05-25   30.745   9.477       4.096       66.04         133.77   30.48    ON
  07:00:00                                                                      

  2026-05-25   30.305   9.569       3.662       64.4          131.3    30.954   ON
  08:00:00                                                                      

  2026-05-25   30.483   9.398       3.868       63.05         140.06   31.243   ON
  09:00:00                                                                      

  2026-05-25   30.003   9.436       3.498       64.03         132.25   30.234   ON
  10:00:00                                                                      

  2026-05-25   30.47    9.327       3.701       63.46         142.18   29.34    ON
  11:00:00                                                                      

  2026-05-25   30.883   9.553       3.915       65.62         138.24   29.723   ON
  12:00:00                                                                      

  2026-05-25   29.742   9.495       3.591       64.92         129.9    30.464   ON
  13:00:00                                                                      

  2026-05-25   30.18    9.442       3.166       67.54         134.21   30.801   ON
  14:00:00                                                                      

  2026-05-25   29.408   9.724       3.892       63.7          139.14   30.965   ON
  15:00:00                                                                      

  2026-05-25   29.878   9.452       3.902       62.87         137.51   29.963   ON
  16:00:00                                                                      

  2026-05-25   29.978   9.597       3.985       68            138.68   30.521   ON
  17:00:00                                                                      

  2026-05-25   30.343   9.687       4.076       63.84         137.83   30.338   ON
  18:00:00                                                                      

  2026-05-25   29.794   9.427       3.567       62.76         137.24   30.779   ON
  19:00:00                                                                      

  2026-05-25   30.86    9.641       3.523       65.86         133.76   30.697   ON
  20:00:00                                                                      

  2026-05-25   30.912   9.557       3.28        67.29         133.94   30.068   ON
  21:00:00                                                                      

  2026-05-25   30.503   9.602       3.904       65.11         136.41   31.179   ON
  22:00:00                                                                      

  2026-05-25   31.291   9.798       3.759       65.68         138.06   29.919   ON
  23:00:00                                                                      

  2026-05-26   29.518   9.373       3.696       66.12         138.07   31.702   ON
  00:00:00                                                                      

  2026-05-26   28.969   9.319       4.211       63.98         132.06   30.539   ON
  01:00:00                                                                      

  2026-05-26   29.771   9.664       3.764       65.12         133.14   30.915   ON
  02:00:00                                                                      

  2026-05-26   29.532   9.256       3.773       66.28         144.39   30.439   ON
  03:00:00                                                                      

  2026-05-26   29.493   9.381       3.667       64.38         137.82   31.168   ON
  04:00:00                                                                      

  2026-05-26   29.739   9.491       3.921       67.87         133.94   30.022   ON
  05:00:00                                                                      

  2026-05-26   30.345   9.545       3.644       62.95         130.32   29.717   ON
  06:00:00                                                                      

  2026-05-26   30.734   9.503       3.989       63.51         135.67   31.026   ON
  07:00:00                                                                      

  2026-05-26   29.861   9.407       4.174       64.34         136.82   29.169   ON
  08:00:00                                                                      

  2026-05-26   30.534   9.444       3.662       63.9          133.9    29.576   ON
  09:00:00                                                                      

  2026-05-26   30.016   9.553       4.082       64.44         130.69   31.079   ON
  10:00:00                                                                      

  2026-05-26   30.119   9.266       3.302       65.97         140.79   30.82    ON
  11:00:00                                                                      

  2026-05-26   30.857   9.52        3.779       67.72         134.04   31.053   ON
  12:00:00                                                                      

  2026-05-26   30.047   9.033       3.781       62.7          136.55   29.865   ON
  13:00:00                                                                      

  2026-05-26   30.25    9.483       3.779       63.83         136.63   28.574   ON
  14:00:00                                                                      

  2026-05-26   30.151   9.557       4.007       62.89         133.14   29.432   ON
  15:00:00                                                                      

  2026-05-26   29.532   9.333       4.405       65.1          138.01   29.866   ON
  16:00:00                                                                      

  2026-05-26   30.555   9.395       4.202       64.05         132.48   32.249   ON
  17:00:00                                                                      

  2026-05-26   31.428   9.605       4.007       63.77         132.46   29.554   ON
  18:00:00                                                                      

  2026-05-26   30.065   9.703       3.791       64.31         142.38   30.434   ON
  19:00:00                                                                      

  2026-05-26   30.614   9.303       3.621       65.48         135.6    30.434   ON
  20:00:00                                                                      

  2026-05-26   30.858   9.535       3.813       63.76         136.42   31.313   ON
  21:00:00                                                                      

  2026-05-26   30.216   9.559       3.703       64.98         131.97   30.837   ON
  22:00:00                                                                      

  2026-05-26   30.19    9.315       3.594       63.07         138.06   30.638   ON
  23:00:00                                                                      

  2026-05-27   29.903   9.513       3.863       67.45         136.84   31.26    ON
  00:00:00                                                                      

  2026-05-27   29.338   9.594       4.118       64.91         135.43   30.2     ON
  01:00:00                                                                      

  2026-05-27   29.798   9.654       3.508       67.11         137.93   30.917   ON
  02:00:00                                                                      

  2026-05-27   30.429   9.613       4.14        67.86         136.74   30.905   ON
  03:00:00                                                                      

  2026-05-27   30.522   9.74        3.897       65.23         130.5    29.793   ON
  04:00:00                                                                      

  2026-05-27   29.541   9.832       4.413       62.76         134.73   30.209   ON
  05:00:00                                                                      

  2026-05-27   31.005   9.344       3.646       65.65         132.67   30.092   ON
  06:00:00                                                                      

  2026-05-27   29.102   9.533       4.069       63.44         131.07   30.306   ON
  07:00:00                                                                      

  2026-05-27   29.453   9.261       3.49        66.14         137.3    30.517   ON
  08:00:00                                                                      

  2026-05-27   30.16    9.401       3.595       63.88         126.25   30.121   ON
  09:00:00                                                                      

  2026-05-27   29.43    9.361       3.817       65.85         136.5    30.447   ON
  10:00:00                                                                      

  2026-05-27   29.852   9.562       3.841       65.57         134.06   30.003   ON
  11:00:00                                                                      

  2026-05-27   30.354   9.865       3.977       62.81         140.46   30.131   ON
  12:00:00                                                                      

  2026-05-27   29.464   9.277       3.497       67.23         138.37   31.003   ON
  13:00:00                                                                      

  2026-05-27   29.328   9.576       3.726       69.33         137.97   30.54    ON
  14:00:00                                                                      

  2026-05-27   30.43    9.423       3.713       63.57         136.9    30.519   ON
  15:00:00                                                                      

  2026-05-27   30.945   9.634       3.774       64.94         128.03   30.165   ON
  16:00:00                                                                      

  2026-05-27   30.024   9.603       3.99        63.58         133.05   29.487   ON
  17:00:00                                                                      

  2026-05-27   30.74    9.36        4.191       65.11         130.82   29.625   ON
  18:00:00                                                                      

  2026-05-27   29.073   9.37        3.42        65.1          135.44   30.857   ON
  19:00:00                                                                      

  2026-05-27   29.605   9.223       3.881       65.63         136.2    32.028   ON
  20:00:00                                                                      

  2026-05-27   30.7     9.325       3.747       66.28         133.51   31.461   ON
  21:00:00                                                                      

  2026-05-27   30.41    9.568       3.839       65.96         132.32   30.355   ON
  22:00:00                                                                      

  2026-05-27   30.008   9.649       3.96        63.63         135.37   30.531   ON
  23:00:00                                                                      

  2026-05-28   29.402   9.561       3.925       62.01         133.58   30.498   ON
  00:00:00                                                                      

  2026-05-28   29.035   9.372       3.358       64.83         133.06   30.607   ON
  01:00:00                                                                      

  2026-05-28   30.539   9.541       4.044       64.83         143.88   30.581   ON
  02:00:00                                                                      

  2026-05-28   30.57    9.265       3.844       66.11         133.23   30.03    ON
  03:00:00                                                                      

  2026-05-28   30.104   9.333       3.606       67.31         132.33   30.912   ON
  04:00:00                                                                      

  2026-05-28   30.359   9.592       3.974       65.48         135.04   31.931   ON
  05:00:00                                                                      

  2026-05-28   30.001   9.574       3.802       64.37         134.91   29.978   ON
  06:00:00                                                                      

  2026-05-28   29.749   9.488       3.23        65.15         138.46   30.302   ON
  07:00:00                                                                      

  2026-05-28   29.654   9.505       3.87        64.38         142.71   30.865   ON
  08:00:00                                                                      

  2026-05-28   29.681   9.374       4.182       65.23         130.29   30.017   ON
  09:00:00                                                                      

  2026-05-28   29.567   9.712       3.8         64.08         142.14   30.628   ON
  10:00:00                                                                      

  2026-05-28   30.808   9.67        3.58        65.68         136.63   30.298   ON
  11:00:00                                                                      

  2026-05-28   30.267   9.351       4.034       63.85         132.93   29.65    ON
  12:00:00                                                                      

  2026-05-28   30.067   9.655       3.642       63.14         131.71   31.529   ON
  13:00:00                                                                      

  2026-05-28   30.847   9.103       4.028       65.29         140.58   29.429   ON
  14:00:00                                                                      

  2026-05-28   30.4     9.621       4.104       65.65         129.3    30.944   ON
  15:00:00                                                                      

  2026-05-28   30.12    9.688       3.815       65.7          132.06   30.741   ON
  16:00:00                                                                      

  2026-05-28   30.183   9.47        3.447       63.23         140.36   30.822   ON
  17:00:00                                                                      

  2026-05-28   30.375   9.545       4.021       62.46         126.17   30.709   ON
  18:00:00                                                                      

  2026-05-28   29.659   9.333       3.904       62.83         132.02   31.548   ON
  19:00:00                                                                      

  2026-05-28   30.149   9.429       3.68        66.9          140.01   31.16    ON
  20:00:00                                                                      

  2026-05-28   29.473   9.754       4.034       66.29         135.56   30.5     ON
  21:00:00                                                                      

  2026-05-28   29.707   9.661       3.822       65.79         133.56   30.791   ON
  22:00:00                                                                      

  2026-05-28   29.978   9.627       3.266       67.05         137.84   31.28    ON
  23:00:00                                                                      

  2026-05-29   29.694   9.437       3.922       66.58         127.54   31.702   ON
  00:00:00                                                                      

  2026-05-29   30.273   9.39        3.656       66.93         130.46   30.03    ON
  01:00:00                                                                      

  2026-05-29   30.268   9.58        3.625       65.06         137.21   30.571   ON
  02:00:00                                                                      

  2026-05-29   31.173   9.355       4.174       67.78         132.67   29.778   ON
  03:00:00                                                                      

  2026-05-29   30.142   9.414       3.672       67.29         127.25   30.331   ON
  04:00:00                                                                      

  2026-05-29   30.354   9.527       3.764       63.67         144.06   30.625   ON
  05:00:00                                                                      

  2026-05-29   29.732   9.819       3.578       66.26         134.58   30.075   ON
  06:00:00                                                                      

  2026-05-29   30.045   9.303       3.646       67.4          137.92   30.488   ON
  07:00:00                                                                      

  2026-05-29   30.111   9.546       3.823       68.63         136.8    31.221   ON
  08:00:00                                                                      

  2026-05-29   30.661   9.374       3.85        64.4          135.08   30.468   ON
  09:00:00                                                                      

  2026-05-29   30.192   9.614       4.095       65.66         132.48   30.377   ON
  10:00:00                                                                      

  2026-05-29   29.968   9.617       4.058       65.65         134.69   29.532   ON
  11:00:00                                                                      

  2026-05-29   29.662   9.362       3.551       63.75         126.93   30.605   ON
  12:00:00                                                                      

  2026-05-29   30.121   9.768       3.737       64.82         131.45   30.314   ON
  13:00:00                                                                      

  2026-05-29   30.588   9.319       3.78        65.28         138.76   31.152   ON
  14:00:00                                                                      

  2026-05-29   29.308   9.319       3.717       63.02         133.96   29.844   ON
  15:00:00                                                                      

  2026-05-29   30.79    9.427       3.696       65.48         133.16   30.733   ON
  16:00:00                                                                      

  2026-05-29   30.098   9.667       4.091       64.22         135.27   30.239   ON
  17:00:00                                                                      

  2026-05-29   29.393   9.516       3.888       63.76         136.76   31.101   ON
  18:00:00                                                                      

  2026-05-29   29.922   9.639       3.949       63.81         138.21   30.713   ON
  19:00:00                                                                      

  2026-05-29   30.601   9.639       3.905       66.25         134.42   29.821   ON
  20:00:00                                                                      

  2026-05-29   30.629   9.306       3.718       66.54         132.34   30.077   ON
  21:00:00                                                                      

  2026-05-29   29.584   9.299       3.458       64.51         130.56   31.765   ON
  22:00:00                                                                      

  2026-05-29   29.916   9.589       3.692       64.69         133.05   31.135   ON
  23:00:00                                                                      

  2026-05-30   30.922   9.477       3.743       61.74         128.84   30.736   ON
  00:00:00                                                                      

  2026-05-30   30.511   9.582       3.913       64.96         135.76   30.429   ON
  01:00:00                                                                      

  2026-05-30   31.107   9.634       3.629       67.49         132.84   30.474   ON
  02:00:00                                                                      

  2026-05-30   30.68    9.618       3.694       65.77         136.96   30.235   ON
  03:00:00                                                                      

  2026-05-30   29.913   9.609       3.666       66.67         134.12   30.24    ON
  04:00:00                                                                      

  2026-05-30   30.221   9.543       3.626       65.22         132.47   30.538   ON
  05:00:00                                                                      

  2026-05-30   29.708   9.495       4.148       64            132.03   30.804   ON
  06:00:00                                                                      

  2026-05-30   30.237   9.78        4.091       64.98         136.92   29.574   ON
  07:00:00                                                                      

  2026-05-30   30.685   9.579       4.157       66.87         131.42   29.578   ON
  08:00:00                                                                      

  2026-05-30   30.445   9.657       4.137       66.25         134.77   30.612   ON
  09:00:00                                                                      

  2026-05-30   29.795   9.752       3.514       63.72         140.86   30.326   ON
  10:00:00                                                                      

  2026-05-30   29.344   9.57        4.145       63.85         140.01   30.188   ON
  11:00:00                                                                      

  2026-05-30   30.14    9.566       3.719       66.06         135.28   31.228   ON
  12:00:00                                                                      

  2026-05-30   28.723   9.438       3.947       65.6          136.04   30.877   ON
  13:00:00                                                                      

  2026-05-30   29.99    9.292       3.684       67.48         137.15   30.225   ON
  14:00:00                                                                      

  2026-05-30   30.891   9.48        3.723       63.71         137.07   29.918   ON
  15:00:00                                                                      

  2026-05-30   30.052   9.531       3.417       62.18         133.66   30.746   ON
  16:00:00                                                                      

  2026-05-30   29.021   9.339       3.184       65.08         131.88   30.911   ON
  17:00:00                                                                      

  2026-05-30   29.984   9.698       3.661       62.84         128.68   29.108   ON
  18:00:00                                                                      

  2026-05-30   29.704   9.623       3.725       64.35         140      30.851   ON
  19:00:00                                                                      

  2026-05-30   30.518   9.629       3.851       64.5          139.7    31.633   ON
  20:00:00                                                                      

  2026-05-30   29.062   9.449       3.784       65.13         141.26   30.828   ON
  21:00:00                                                                      

  2026-05-30   30.114   9.726       3.953       68.36         134.76   31.133   ON
  22:00:00                                                                      

  2026-05-30   29.658   9.855       3.897       66.16         138.46   30.084   ON
  23:00:00                                                                      
  --------------------------------------------------------------------------------------

### BL5702

Source pages: 136-169.

#### Data dictionary

  Name          Description                    Digital set   Engineering units   Span
  ------------- ------------------------------ ------------- ------------------- ------
  Name          Description                    digitalset    engunits            span
  BL5702_FEED   BL-5702 FEED RATE              T/H           57                  
  BL5702_DISP   BL-5702 DISCHARGE PRESSURE     BARG          20                  
  BL5702_VIB    BL-5702 VIBRATION              MM/S          20                  
  BL5702_TEMP   BL-5702 BEARING/PROCESS TEMP   DEG C         150                 
  BL5702_AMP    BL-5702 MOTOR AMPERE           A             300                 
  PLANT_RATE    OPP PRODUCTION RATE            T/H           49.4                
  RUN_STATUS    BL-5702 RUN STATUS             ON_OFF        ON_OFF              1

#### Typical value, zero, and instrument tag

## Typical value Zero Instrument tag --------------- ------

#### Hourly data

  --------------------------------------------------------------------------------------
  Timestamp    Feed     Discharge   Vibration   Temperature   Motor    Plant    Run
                        pressure                              ampere   rate     status
  ------------ -------- ----------- ----------- ------------- -------- -------- --------
  2026-06-01   38.075   9.793       4.062       64.87         144.29   39.88    ON
  00:00:00                                                                      

  2026-06-01   37.452   9.603       3.957       64.74         141.81   38.342   ON
  01:00:00                                                                      

  2026-06-01   37.622   9.39        3.831       62.77         135.57   38.492   ON
  02:00:00                                                                      

  2026-06-01   38.333   9.515       4.232       63.03         135.59   38.847   ON
  03:00:00                                                                      

  2026-06-01   37.234   9.433       3.494       66.11         128.39   39.891   ON
  04:00:00                                                                      

  2026-06-01   37.866   9.244       3.291       63.49         139.9    38.077   ON
  05:00:00                                                                      

  2026-06-01   37.613   9.628       3.867       66.52         133.88   39.233   ON
  06:00:00                                                                      

  2026-06-01   37.67    9.281       3.832       63.85         139.11   39.606   ON
  07:00:00                                                                      

  2026-06-01   40.306   9.474       3.576       64.93         136.51   38.807   ON
  08:00:00                                                                      

  2026-06-01   36.495   9.184       3.469       62.96         134.57   38.721   ON
  09:00:00                                                                      

  2026-06-01   38.21    9.577       3.607       64.52         133.55   38.243   ON
  10:00:00                                                                      

  2026-06-01   37.189   9.449       3.85        61.82         129.01   38.296   ON
  11:00:00                                                                      

  2026-06-01   39.562   9.553       3.732       66.78         135.68   38.607   ON
  12:00:00                                                                      

  2026-06-01   37.778   9.503       3.83        67.6          134.88   37.891   ON
  13:00:00                                                                      

  2026-06-01   37.85    9.538       3.723       65.63         132.52   39.027   ON
  14:00:00                                                                      

  2026-06-01   38.309   9.497       4.03        63.37         125.5    40.575   ON
  15:00:00                                                                      

  2026-06-01   38.472   9.39        3.729       65.64         130.06   39.385   ON
  16:00:00                                                                      

  2026-06-01   37.892   9.204       3.701       63.75         135.89   38.192   ON
  17:00:00                                                                      

  2026-06-01   38.943   9.785       3.466       63.17         137.28   38.656   ON
  18:00:00                                                                      

  2026-06-01   38.015   9.428       4.032       65.63         142.67   38.454   ON
  19:00:00                                                                      

  2026-06-01   38.796   9.731       3.524       65.47         130.53   37.57    ON
  20:00:00                                                                      

  2026-06-01   37.728   9.631       3.39        62.88         132.09   40.407   ON
  21:00:00                                                                      

  2026-06-01   37.292   9.464       4.025       66.27         135.8    36.913   ON
  22:00:00                                                                      

  2026-06-01   37.615   9.41        3.592       65.71         133.65   38.398   ON
  23:00:00                                                                      

  2026-06-02   37.349   9.58        3.956       63.65         130.08   38.566   ON
  00:00:00                                                                      

  2026-06-02   36.811   9.589       3.833       64.96         137.79   38.065   ON
  01:00:00                                                                      

  2026-06-02   37.423   9.526       3.605       63.48         137.93   39.571   ON
  02:00:00                                                                      

  2026-06-02   37.116   9.524       3.98        65.47         132.79   38.145   ON
  03:00:00                                                                      

  2026-06-02   38.434   9.578       3.68        66.52         132.41   37.929   ON
  04:00:00                                                                      

  2026-06-02   39.156   9.435       4.312       67.02         141.1    38.983   ON
  05:00:00                                                                      

  2026-06-02   37.195   9.306       3.472       65.34         133.75   38.743   ON
  06:00:00                                                                      

  2026-06-02   38.083   9.593       3.659       63.78         129.14   37.169   ON
  07:00:00                                                                      

  2026-06-02   37.32    9.372       3.4         64.45         135.75   38.297   ON
  08:00:00                                                                      

  2026-06-02   38.721   9.573       4.184       67.26         126.59   38.512   ON
  09:00:00                                                                      

  2026-06-02   38.994   9.46        3.639       64.4          134.85   40.559   ON
  10:00:00                                                                      

  2026-06-02   37.579   9.333       3.816       65.61         133.8    38.797   ON
  11:00:00                                                                      

  2026-06-02   38.523   9.315       3.967       65.53         133.82   40.84    ON
  12:00:00                                                                      

  2026-06-02   36.653   9.355       3.25        65.62         133.53   38.138   ON
  13:00:00                                                                      

  2026-06-02   38.272   9.451       3.76        64            140.42   38.14    ON
  14:00:00                                                                      

  2026-06-02   38.664   9.478       3.887       63.97         131.68   39.229   ON
  15:00:00                                                                      

  2026-06-02   38.2     9.612       3.884       63.9          132.4    39.933   ON
  16:00:00                                                                      

  2026-06-02   38.518   9.44        3.674       64.88         134.9    37.3     ON
  17:00:00                                                                      

  2026-06-02   38.888   9.429       3.747       64.44         134.87   38.927   ON
  18:00:00                                                                      

  2026-06-02   39.806   9.344       3.282       65.8          134.87   37.796   ON
  19:00:00                                                                      

  2026-06-02   38.096   9.554       3.551       64.64         135.77   39.11    ON
  20:00:00                                                                      

  2026-06-02   37.992   9.338       3.59        62.45         133.73   38.045   ON
  21:00:00                                                                      

  2026-06-02   38.539   9.429       3.873       63.95         130.58   39.064   ON
  22:00:00                                                                      

  2026-06-02   37.443   9.576       3.438       64.88         133.21   38.757   ON
  23:00:00                                                                      

  2026-06-03   38.674   9.633       3.656       65.66         139.1    38.043   ON
  00:00:00                                                                      

  2026-06-03   37.334   9.633       3.341       63.9          136.1    39.959   ON
  01:00:00                                                                      

  2026-06-03   38.102   9.611       3.725       63.54         137.99   39.4     ON
  02:00:00                                                                      

  2026-06-03   37.398   9.552       4.073       65.36         131.05   38.221   ON
  03:00:00                                                                      

  2026-06-03   37.116   9.495       3.85        64.73         140.81   37.86    ON
  04:00:00                                                                      

  2026-06-03   38.04    9.69        3.841       67.43         138.97   38.325   ON
  05:00:00                                                                      

  2026-06-03   37.318   9.479       3.414       64.5          132.5    38.007   ON
  06:00:00                                                                      

  2026-06-03   37.112   9.268       3.486       65.92         131.51   38.38    ON
  07:00:00                                                                      

  2026-06-03   37.789   9.557       3.92        64.22         133.61   39.8     ON
  08:00:00                                                                      

  2026-06-03   37.284   9.442       3.82        63.29         141.83   37.657   ON
  09:00:00                                                                      

  2026-06-03   38.161   9.602       4.47        65.35         140.88   39.15    ON
  10:00:00                                                                      

  2026-06-03   38.368   9.475       4.026       64.74         125.9    39.579   ON
  11:00:00                                                                      

  2026-06-03   38.319   9.393       3.942       66.15         140.01   38.34    ON
  12:00:00                                                                      

  2026-06-03   39.37    9.586       3.909       65.71         140.73   39.363   ON
  13:00:00                                                                      

  2026-06-03   37.956   9.501       3.952       62.02         132.46   39.579   ON
  14:00:00                                                                      

  2026-06-03   37.722   9.38        3.863       65.16         137.58   40.728   ON
  15:00:00                                                                      

  2026-06-03   38.16    9.274       3.498       64.26         134.02   38.374   ON
  16:00:00                                                                      

  2026-06-03   37.596   9.356       3.936       64.67         136.71   39.041   ON
  17:00:00                                                                      

  2026-06-03   36.967   9.651       3.959       64.56         138.1    38.396   ON
  18:00:00                                                                      

  2026-06-03   38.372   9.747       3.585       63.14         132.97   37.868   ON
  19:00:00                                                                      

  2026-06-03   37.368   9.62        3.73        66.58         127.36   39.43    ON
  20:00:00                                                                      

  2026-06-03   37.35    9.34        3.67        61.05         139.13   39.897   ON
  21:00:00                                                                      

  2026-06-03   37.714   9.424       3.748       64.78         136.37   38       ON
  22:00:00                                                                      

  2026-06-03   38.026   9.486       3.862       63.5          127.86   38.27    ON
  23:00:00                                                                      

  2026-06-04   37.625   9.569       3.497       62.79         139.57   37.304   ON
  00:00:00                                                                      

  2026-06-04   36.31    9.367       3.758       62.64         139.4    38.843   ON
  01:00:00                                                                      

  2026-06-04   37.995   9.629       3.395       63.83         129.64   39.459   ON
  02:00:00                                                                      

  2026-06-04   38.165   9.635       4.059       62.85         136.64   38.312   ON
  03:00:00                                                                      

  2026-06-04   38.246   9.397       3.837       64.38         132.5    38.974   ON
  04:00:00                                                                      

  2026-06-04   39.277   9.404       3.877       64.55         135      38.421   ON
  05:00:00                                                                      

  2026-06-04   37.268   9.598       3.663       64.19         139.86   38.053   ON
  06:00:00                                                                      

  2026-06-04   39.386   9.649       3.866       61.52         136.52   38.377   ON
  07:00:00                                                                      

  2026-06-04   38.283   9.595       3.279       65.05         136.33   39.791   ON
  08:00:00                                                                      

  2026-06-04   37.476   9.334       3.73        65.17         133.71   39.904   ON
  09:00:00                                                                      

  2026-06-04   39.351   9.253       3.75        64.07         137.88   38.709   ON
  10:00:00                                                                      

  2026-06-04   37.815   9.532       3.67        65.39         137.84   38.308   ON
  11:00:00                                                                      

  2026-06-04   38.786   9.653       3.512       65.19         139.87   37.404   ON
  12:00:00                                                                      

  2026-06-04   37.145   9.615       4.178       63.35         140.92   39.455   ON
  13:00:00                                                                      

  2026-06-04   38.823   9.348       3.903       66.49         132.86   39.56    ON
  14:00:00                                                                      

  2026-06-04   38.699   9.57        3.841       65.15         136.25   38.117   ON
  15:00:00                                                                      

  2026-06-04   37.806   9.587       3.683       65.89         128.18   38.995   ON
  16:00:00                                                                      

  2026-06-04   39.128   9.401       4.351       64.67         139.98   38.995   ON
  17:00:00                                                                      

  2026-06-04   37       9.3         3.845       66.43         129.66   39.055   ON
  18:00:00                                                                      

  2026-06-04   39.68    9.819       3.51        65.24         136.82   40.245   ON
  19:00:00                                                                      

  2026-06-04   36.933   9.571       4.076       64.32         128.52   38.562   ON
  20:00:00                                                                      

  2026-06-04   38.247   9.63        4.108       62.55         136.05   39.647   ON
  21:00:00                                                                      

  2026-06-04   38.015   9.842       3.435       64.15         127.42   39.857   ON
  22:00:00                                                                      

  2026-06-04   35.579   9.592       4.173       63.33         136.22   39.586   ON
  23:00:00                                                                      

  2026-06-05   38.219   9.396       3.815       63.27         136.84   38.932   ON
  00:00:00                                                                      

  2026-06-05   37.701   9.454       4.147       65.81         132.07   39.284   ON
  01:00:00                                                                      

  2026-06-05   37.183   9.71        3.624       66.73         139.9    38.855   ON
  02:00:00                                                                      

  2026-06-05   37.455   9.527       4.108       65.87         137.91   40.008   ON
  03:00:00                                                                      

  2026-06-05   36.766   9.429       3.489       66.35         130.3    40.183   ON
  04:00:00                                                                      

  2026-06-05   38.741   9.786       3.513       63.6          131.36   38.167   ON
  05:00:00                                                                      

  2026-06-05   37.147   9.547       3.699       66.29         140.6    39.202   ON
  06:00:00                                                                      

  2026-06-05   37.702   9.579       3.628       63.36         129.21   38.755   ON
  07:00:00                                                                      

  2026-06-05   39.02    9.66        3.467       63.09         140.23   38.342   ON
  08:00:00                                                                      

  2026-06-05   39.356   9.263       3.616       64.16         136.83   38.068   ON
  09:00:00                                                                      

  2026-06-05   36.82    9.454       3.549       64.02         129.81   40.947   ON
  10:00:00                                                                      

  2026-06-05   38.251   9.547       3.585       65.28         130.46   39.289   ON
  11:00:00                                                                      

  2026-06-05   39.005   9.48        3.668       65.48         136.59   38.484   ON
  12:00:00                                                                      

  2026-06-05   38.811   9.624       3.663       64.93         135.61   39.445   ON
  13:00:00                                                                      

  2026-06-05   37.044   9.362       4.061       65.82         134.14   38.614   ON
  14:00:00                                                                      

  2026-06-05   37.619   9.357       3.563       63.81         139.3    39.679   ON
  15:00:00                                                                      

  2026-06-05   38.169   9.507       3.978       63.41         138.53   38.787   ON
  16:00:00                                                                      

  2026-06-05   38.698   9.502       3.976       65.43         130.84   37.615   ON
  17:00:00                                                                      

  2026-06-05   38.587   9.296       4.016       66.83         130.84   39.379   ON
  18:00:00                                                                      

  2026-06-05   36.962   9.542       3.792       65.78         131.48   39.315   ON
  19:00:00                                                                      

  2026-06-05   38.516   9.703       3.625       64.19         131.86   37.422   ON
  20:00:00                                                                      

  2026-06-05   38.83    9.458       3.487       66            131.99   39.334   ON
  21:00:00                                                                      

  2026-06-05   39.151   9.363       4.054       64.7          137.16   39.159   ON
  22:00:00                                                                      

  2026-06-05   38.386   9.794       3.814       64.69         125.92   39.023   ON
  23:00:00                                                                      

  2026-06-06   37.333   9.814       3.668       64.71         140.08   38.707   ON
  00:00:00                                                                      

  2026-06-06   38.259   9.477       3.426       64.56         137.51   40.261   ON
  01:00:00                                                                      

  2026-06-06   38.227   9.637       3.942       66.91         132.44   39.127   ON
  02:00:00                                                                      

  2026-06-06   37.041   9.413       3.957       66.23         138.12   37.225   ON
  03:00:00                                                                      

  2026-06-06   37.016   9.503       3.849       66.18         136.82   38.842   ON
  04:00:00                                                                      

  2026-06-06   38.464   9.321       3.47        63.24         132.96   39.101   ON
  05:00:00                                                                      

  2026-06-06   38.992   9.492       3.958       67.53         140.79   38.903   ON
  06:00:00                                                                      

  2026-06-06   38.036   9.741       3.962       63.55         134.23   39.458   ON
  07:00:00                                                                      

  2026-06-06   38.151   9.544       3.427       66.13         134.32   38.626   ON
  08:00:00                                                                      

  2026-06-06   37.499   9.634       3.965       59.89         137.05   38.394   ON
  09:00:00                                                                      

  2026-06-06   37.736   9.277       4.03        65.18         131.88   37.712   ON
  10:00:00                                                                      

  2026-06-06   38.423   9.587       3.796       66.14         140.13   39.117   ON
  11:00:00                                                                      

  2026-06-06   38.602   9.503       3.543       64.93         140.4    39.658   ON
  12:00:00                                                                      

  2026-06-06   37.936   9.638       4.203       63.74         131.08   38.745   ON
  13:00:00                                                                      

  2026-06-06   36.303   9.372       3.503       62.89         138.46   38.259   ON
  14:00:00                                                                      

  2026-06-06   38.063   9.525       3.923       65.39         140.54   38.395   ON
  15:00:00                                                                      

  2026-06-06   36.935   9.229       4.038       66.3          135.23   38.854   ON
  16:00:00                                                                      

  2026-06-06   36.543   9.406       3.908       66.3          140.4    37.665   ON
  17:00:00                                                                      

  2026-06-06   37.5     9.7         3.152       64.51         141.08   38.762   ON
  18:00:00                                                                      

  2026-06-06   39.163   9.531       3.661       67.03         136.27   37.141   ON
  19:00:00                                                                      

  2026-06-06   36.844   9.349       3.725       66.25         139.97   38.131   ON
  20:00:00                                                                      

  2026-06-06   38.034   9.684       3.604       66.75         140.31   39.509   ON
  21:00:00                                                                      

  2026-06-06   38.18    9.589       4.095       65.67         134.6    39.323   ON
  22:00:00                                                                      

  2026-06-06   39.02    9.49        3.747       66.69         133.71   38.707   ON
  23:00:00                                                                      

  2026-06-07   37.473   9.56        4.177       65.1          142.86   39.144   ON
  00:00:00                                                                      

  2026-06-07   37.986   9.468       3.873       65.4          132.32   39.077   ON
  01:00:00                                                                      

  2026-06-07   37.169   9.606       3.113       63.73         140.92   37.578   ON
  02:00:00                                                                      

  2026-06-07   37.425   9.787       3.45        62.04         134.43   38.321   ON
  03:00:00                                                                      

  2026-06-07   38.402   9.222       4.181       64.85         137.74   40.122   ON
  04:00:00                                                                      

  2026-06-07   38.791   9.558       3.322       64.64         135.42   38.624   ON
  05:00:00                                                                      

  2026-06-07   36.474   9.121       4.046       63.55         132.84   38.992   ON
  06:00:00                                                                      

  2026-06-07   36.398   9.502       3.943       64.23         137.42   38.326   ON
  07:00:00                                                                      

  2026-06-07   37.511   9.378       4.171       64.2          137.54   38.473   ON
  08:00:00                                                                      

  2026-06-07   38.782   9.599       4.023       65.67         132.58   38.813   ON
  09:00:00                                                                      

  2026-06-07   37.322   9.542       3.738       64.23         136.81   38.476   ON
  10:00:00                                                                      

  2026-06-07   38.777   9.655       3.918       64.93         133.27   38.494   ON
  11:00:00                                                                      

  2026-06-07   37.81    9.54        3.851       68.64         136.09   40.423   ON
  12:00:00                                                                      

  2026-06-07   37.506   9.668       3.94        62.9          131.06   38.16    ON
  13:00:00                                                                      

  2026-06-07   38.468   9.286       3.481       64.51         131.61   41.393   ON
  14:00:00                                                                      

  2026-06-07   38.025   9.293       3.886       67.69         141.51   39.905   ON
  15:00:00                                                                      

  2026-06-07   38.213   9.218       4.334       63.64         139.49   36.659   ON
  16:00:00                                                                      

  2026-06-07   36.362   9.425       3.827       65.7          134.47   38.544   ON
  17:00:00                                                                      

  2026-06-07   38.094   9.387       3.78        63.74         136.55   40.311   ON
  18:00:00                                                                      

  2026-06-07   38.051   9.716       3.919       64.44         135.68   38.896   ON
  19:00:00                                                                      

  2026-06-07   40.488   9.68        4.102       65.1          135.37   38.046   ON
  20:00:00                                                                      

  2026-06-07   37.874   9.576       3.551       65.62         141.2    38.907   ON
  21:00:00                                                                      

  2026-06-07   38.094   9.517       3.519       65.82         136.44   39.247   ON
  22:00:00                                                                      

  2026-06-07   38.854   9.633       3.969       63.87         132.98   38.435   ON
  23:00:00                                                                      

  2026-06-08   38.796   9.348       3.836       64.4          129.19   37.519   ON
  00:00:00                                                                      

  2026-06-08   38.427   9.609       3.795       64.82         129.15   39.302   ON
  01:00:00                                                                      

  2026-06-08   38.881   9.416       3.809       65.67         141.56   38.448   ON
  02:00:00                                                                      

  2026-06-08   36.462   9.754       3.387       63.48         136.99   39.806   ON
  03:00:00                                                                      

  2026-06-08   37.818   9.52        3.621       64.49         138.87   39.43    ON
  04:00:00                                                                      

  2026-06-08   37.527   9.514       3.879       63.73         137.45   38.896   ON
  05:00:00                                                                      

  2026-06-08   38.048   9.417       4.07        65.84         132.75   37.665   ON
  06:00:00                                                                      

  2026-06-08   36.679   9.607       3.824       66.77         133.07   38.98    ON
  07:00:00                                                                      

  2026-06-08   38.512   9.665       3.969       61.01         134.34   38.702   ON
  08:00:00                                                                      

  2026-06-08   37.697   9.717       3.916       64.03         126.64   40.607   ON
  09:00:00                                                                      

  2026-06-08   38.432   9.459       3.625       65.38         128.13   38.207   ON
  10:00:00                                                                      

  2026-06-08   38.004   9.566       3.488       64.3          132.87   38.58    ON
  11:00:00                                                                      

  2026-06-08   38.293   9.447       4.029       61.9          131.1    38.123   ON
  12:00:00                                                                      

  2026-06-08   38.852   9.569       3.593       66.2          133.52   38.632   ON
  13:00:00                                                                      

  2026-06-08   37.416   9.536       3.514       66.33         136.78   38.427   ON
  14:00:00                                                                      

  2026-06-08   36.815   9.429       3.692       65.08         142.66   39.744   ON
  15:00:00                                                                      

  2026-06-08   37.94    9.43        3.289       63.67         140.24   40.103   ON
  16:00:00                                                                      

  2026-06-08   37.417   9.714       3.535       64.65         131.64   38.599   ON
  17:00:00                                                                      

  2026-06-08   37.881   9.635       3.502       64.13         131.06   38.796   ON
  18:00:00                                                                      

  2026-06-08   37.508   9.472       4.096       64.39         136.68   39.114   ON
  19:00:00                                                                      

  2026-06-08   36.276   9.483       3.723       65.66         134.12   36.678   ON
  20:00:00                                                                      

  2026-06-08   37.203   9.614       3.852       66.38         135.8    39.26    ON
  21:00:00                                                                      

  2026-06-08   37.358   9.445       3.93        65.73         135.43   37.922   ON
  22:00:00                                                                      

  2026-06-08   38.19    9.611       3.933       64.33         137.17   37.961   ON
  23:00:00                                                                      

  2026-06-09   38.508   9.559       4.175       63.95         127.22   39.002   ON
  00:00:00                                                                      

  2026-06-09   39.024   9.427       3.821       65.82         135.62   37.428   ON
  01:00:00                                                                      

  2026-06-09   38.161   9.155       3.993       62.87         128.31   38.492   ON
  02:00:00                                                                      

  2026-06-09   39.446   9.704       3.585       63.44         138.61   38.651   ON
  03:00:00                                                                      

  2026-06-09   39.249   9.662       3.631       65.37         133.25   38.902   ON
  04:00:00                                                                      

  2026-06-09   37.706   9.217       3.845       63.73         132.15   39.869   ON
  05:00:00                                                                      

  2026-06-09   37.716   9.534       3.654       64.94         137.61   38.143   ON
  06:00:00                                                                      

  2026-06-09   37.155   9.373       3.822       64.43         138.03   38.933   ON
  07:00:00                                                                      

  2026-06-09   37.967   9.565       3.666       65.43         135.06   39.198   ON
  08:00:00                                                                      

  2026-06-09   37.743   9.807       3.928       66.12         138.62   38.832   ON
  09:00:00                                                                      

  2026-06-09   38.379   9.908       3.786       64.74         130.34   38.688   ON
  10:00:00                                                                      

  2026-06-09   39.402   9.607       3.653       64.62         136.65   37.944   ON
  11:00:00                                                                      

  2026-06-09   39.739   9.636       3.782       66.02         137.18   36.458   ON
  12:00:00                                                                      

  2026-06-09   38.522   9.438       3.753       66.49         134.02   38.108   ON
  13:00:00                                                                      

  2026-06-09   37.333   9.619       3.946       65.69         138.34   39.14    ON
  14:00:00                                                                      

  2026-06-09   38.272   9.611       3.989       64.28         138.18   37.914   ON
  15:00:00                                                                      

  2026-06-09   38.384   9.659       3.512       66.8          141.78   38.878   ON
  16:00:00                                                                      

  2026-06-09   37.413   9.494       4.099       63.7          133.63   40.37    ON
  17:00:00                                                                      

  2026-06-09   37.872   9.417       3.757       64.26         131.21   39.399   ON
  18:00:00                                                                      

  2026-06-09   38.648   9.648       3.691       64.58         132.56   38.774   ON
  19:00:00                                                                      

  2026-06-09   37.591   9.64        3.89        66.22         136.73   39.118   ON
  20:00:00                                                                      

  2026-06-09   37.204   9.489       4.002       63.54         136.43   38.352   ON
  21:00:00                                                                      

  2026-06-09   37.835   9.461       3.668       63.9          135.74   39.65    ON
  22:00:00                                                                      

  2026-06-09   38.195   9.178       3.755       66.1          130.89   38.727   ON
  23:00:00                                                                      

  2026-06-10   38.988   9.274       3.494       68.31         134.51   38.729   ON
  00:00:00                                                                      

  2026-06-10   37.412   9.489       3.971       64.47         139.52   36.897   ON
  01:00:00                                                                      

  2026-06-10   38.589   9.547       3.872       63.76         138.18   38.158   ON
  02:00:00                                                                      

  2026-06-10   38.086   9.297       3.863       63.23         131.67   38.013   ON
  03:00:00                                                                      

  2026-06-10   38.357   9.451       3.743       66.49         136.76   38.524   ON
  04:00:00                                                                      

  2026-06-10   38.234   9.414       3.839       64.49         132.94   37.397   ON
  05:00:00                                                                      

  2026-06-10   37.386   9.423       3.353       67.15         135.53   39.585   ON
  06:00:00                                                                      

  2026-06-10   36.086   9.675       3.805       63.77         132.43   39.735   ON
  07:00:00                                                                      

  2026-06-10   37.257   9.668       4.284       64.24         132.96   38.97    ON
  08:00:00                                                                      

  2026-06-10   38.258   9.216       3.562       65.03         132.62   39.716   ON
  09:00:00                                                                      

  2026-06-10   38.084   9.66        3.916       64.11         133.78   38.71    ON
  10:00:00                                                                      

  2026-06-10   38.235   9.563       3.06        64.49         131.38   38.257   ON
  11:00:00                                                                      

  2026-06-10   37.855   9.447       3.81        66.03         138.51   37.546   ON
  12:00:00                                                                      

  2026-06-10   38.05    9.618       3.589       64.14         134.2    39.208   ON
  13:00:00                                                                      

  2026-06-10   37.697   9.529       3.903       63.08         137.63   38.741   ON
  14:00:00                                                                      

  2026-06-10   38.983   9.688       3.379       64            135.18   39.272   ON
  15:00:00                                                                      

  2026-06-10   36.894   9.539       3.564       66.03         134.51   38.59    ON
  16:00:00                                                                      

  2026-06-10   37.444   9.406       3.583       65.07         129.47   37.958   ON
  17:00:00                                                                      

  2026-06-10   37.274   9.369       3.794       66.16         130.05   37.983   ON
  18:00:00                                                                      

  2026-06-10   37.864   9.678       3.919       64.83         133.81   38.79    ON
  19:00:00                                                                      

  2026-06-10   38.52    9.19        3.666       65.1          130.04   39.11    ON
  20:00:00                                                                      

  2026-06-10   39.343   9.564       3.714       64.98         137.47   38.919   ON
  21:00:00                                                                      

  2026-06-10   38.79    9.892       3.732       65.05         133.03   38.485   ON
  22:00:00                                                                      

  2026-06-10   38.737   9.612       4.092       64.58         131.03   39.793   ON
  23:00:00                                                                      

  2026-06-11   39.087   9.574       3.719       61.81         133.89   38.794   ON
  00:00:00                                                                      

  2026-06-11   38.795   9.403       4.001       66.63         136.15   38.278   ON
  01:00:00                                                                      

  2026-06-11   38.771   9.227       3.739       67.32         133.9    38.231   ON
  02:00:00                                                                      

  2026-06-11   37.331   9.452       3.754       65.26         142.52   38.345   ON
  03:00:00                                                                      

  2026-06-11   37.541   9.696       3.673       66            139.33   38.884   ON
  04:00:00                                                                      

  2026-06-11   38.495   9.005       3.812       64.21         134.78   38.636   ON
  05:00:00                                                                      

  2026-06-11   38.099   9.32        3.532       64.95         132.25   38.9     ON
  06:00:00                                                                      

  2026-06-11   37.76    9.421       3.647       67.05         129.33   38.303   ON
  07:00:00                                                                      

  2026-06-11   38.861   9.459       3.748       63.52         136.77   39.177   ON
  08:00:00                                                                      

  2026-06-11   37.658   9.273       3.771       67            138.98   39.296   ON
  09:00:00                                                                      

  2026-06-11   38.286   9.628       4.035       66.56         134.4    39.421   ON
  10:00:00                                                                      

  2026-06-11   37.981   9.311       3.756       62.4          131.95   39.232   ON
  11:00:00                                                                      

  2026-06-11   37.271   9.518       3.952       65.26         134.51   38.117   ON
  12:00:00                                                                      

  2026-06-11   39.345   9.26        4.225       66.66         132.12   38.75    ON
  13:00:00                                                                      

  2026-06-11   36.743   9.535       3.834       64.69         134.54   38.097   ON
  14:00:00                                                                      

  2026-06-11   37.054   9.422       3.673       65.79         136.98   39.327   ON
  15:00:00                                                                      

  2026-06-11   37.675   9.22        3.629       62.88         133.91   38.917   ON
  16:00:00                                                                      

  2026-06-11   39.041   9.447       4.359       66.09         136.81   38.719   ON
  17:00:00                                                                      

  2026-06-11   39.001   9.628       3.399       65.65         138.53   38.58    ON
  18:00:00                                                                      

  2026-06-11   37.471   9.65        3.875       66.79         130.79   37.83    ON
  19:00:00                                                                      

  2026-06-11   38.477   9.648       3.736       63.47         131.03   38.851   ON
  20:00:00                                                                      

  2026-06-11   37.819   9.357       4.151       65.18         135.21   40.896   ON
  21:00:00                                                                      

  2026-06-11   37.231   9.684       3.889       65.74         123.89   38.971   ON
  22:00:00                                                                      

  2026-06-11   38.244   9.517       3.785       64.55         138.72   38.003   ON
  23:00:00                                                                      

  2026-06-12   38.03    9.565       3.58        65.18         133.44   39.162   ON
  00:00:00                                                                      

  2026-06-12   37.558   9.642       3.55        66.95         135.36   38.468   ON
  01:00:00                                                                      

  2026-06-12   38.588   9.26        3.727       65.03         137.68   38.68    ON
  02:00:00                                                                      

  2026-06-12   38.714   9.612       3.548       63.33         127.65   38.577   ON
  03:00:00                                                                      

  2026-06-12   37.257   9.299       4.132       65.09         139.34   38.411   ON
  04:00:00                                                                      

  2026-06-12   39.263   9.61        3.535       64.35         137.15   39.503   ON
  05:00:00                                                                      

  2026-06-12   38.428   9.46        4.165       64.13         125.34   37.789   ON
  06:00:00                                                                      

  2026-06-12   37.891   9.598       3.713       66.42         130.6    38.395   ON
  07:00:00                                                                      

  2026-06-12   39.211   9.43        4.13        64.86         143.43   39.371   ON
  08:00:00                                                                      

  2026-06-12   38.622   9.398       3.87        63.67         137.59   39.672   ON
  09:00:00                                                                      

  2026-06-12   38.708   9.598       3.646       63.18         139.41   38.983   ON
  10:00:00                                                                      

  2026-06-12   38.633   9.455       3.892       64.83         134.76   39.969   ON
  11:00:00                                                                      

  2026-06-12   37.817   9.741       3.891       66.51         139.23   40.302   ON
  12:00:00                                                                      

  2026-06-12   38.438   9.464       4.116       65.53         128.24   36.966   ON
  13:00:00                                                                      

  2026-06-12   37.931   9.743       3.41        65.74         131.53   37.548   ON
  14:00:00                                                                      

  2026-06-12   37.445   9.296       3.838       63.1          141.9    38.563   ON
  15:00:00                                                                      

  2026-06-12   37.301   9.637       4.157       66.06         138.86   37.579   ON
  16:00:00                                                                      

  2026-06-12   38.4     9.469       4.181       64.14         134.02   39.398   ON
  17:00:00                                                                      

  2026-06-12   38.774   9.627       3.504       66.48         137.42   38.837   ON
  18:00:00                                                                      

  2026-06-12   36.9     9.404       4.024       66.67         132.21   38.141   ON
  19:00:00                                                                      

  2026-06-12   39.292   9.551       4.083       64.83         129.61   38.862   ON
  20:00:00                                                                      

  2026-06-12   38.557   9.578       4.15        62.83         138.45   39.223   ON
  21:00:00                                                                      

  2026-06-12   38.73    9.377       4.059       66.25         133.72   39.683   ON
  22:00:00                                                                      

  2026-06-12   37.786   9.544       3.796       65.19         135.73   37.574   ON
  23:00:00                                                                      

  2026-06-13   38.51    9.448       3.586       64.74         137.2    39.805   ON
  00:00:00                                                                      

  2026-06-13   38.564   9.326       3.721       63.82         136.64   38.242   ON
  01:00:00                                                                      

  2026-06-13   37.01    9.629       3.392       63.84         139.71   38.093   ON
  02:00:00                                                                      

  2026-06-13   38.766   9.471       4.085       65.2          132.98   39.246   ON
  03:00:00                                                                      

  2026-06-13   39.707   9.252       3.851       64.81         133.15   38.832   ON
  04:00:00                                                                      

  2026-06-13   37.45    9.578       3.938       66.33         138.04   37.786   ON
  05:00:00                                                                      

  2026-06-13   36.65    9.455       4.258       61.91         139.55   38.537   ON
  06:00:00                                                                      

  2026-06-13   37.442   9.51        3.949       64.85         130.49   38.053   ON
  07:00:00                                                                      

  2026-06-13   38.67    9.516       3.612       67.1          128.89   39.177   ON
  08:00:00                                                                      

  2026-06-13   38.354   9.563       3.517       65.86         132.19   40.419   ON
  09:00:00                                                                      

  2026-06-13   37.311   9.381       3.562       63.12         135.6    37.985   ON
  10:00:00                                                                      

  2026-06-13   37.557   9.394       3.868       65.82         136.02   39.975   ON
  11:00:00                                                                      

  2026-06-13   36.68    9.658       3.736       64.01         130.68   38.607   ON
  12:00:00                                                                      

  2026-06-13   38.114   9.412       3.874       63.89         136.09   37.895   ON
  13:00:00                                                                      

  2026-06-13   36.392   9.47        3.623       63.89         141.35   40.29    ON
  14:00:00                                                                      

  2026-06-13   37.852   9.21        4.045       63.22         126.07   38.871   ON
  15:00:00                                                                      

  2026-06-13   36.98    9.573       3.278       64.59         136.12   38.965   ON
  16:00:00                                                                      

  2026-06-13   37.883   9.503       3.574       65.33         135.59   38.218   ON
  17:00:00                                                                      

  2026-06-13   38.511   9.55        4.372       64.3          133.35   39.703   ON
  18:00:00                                                                      

  2026-06-13   37.885   9.688       4.017       63.73         137.16   38.41    ON
  19:00:00                                                                      

  2026-06-13   38.177   9.588       4.048       65.01         138.23   38.752   ON
  20:00:00                                                                      

  2026-06-13   38.221   9.544       3.897       63.38         130.05   39.148   ON
  21:00:00                                                                      

  2026-06-13   37.781   9.743       3.96        64.49         135.46   39.836   ON
  22:00:00                                                                      

  2026-06-13   37.42    9.654       3.694       64.25         137.62   39.295   ON
  23:00:00                                                                      

  2026-06-14   36.691   9.618       3.621       66.18         134.41   38.994   ON
  00:00:00                                                                      

  2026-06-14   38.241   9.535       4.192       64.83         136.77   38.709   ON
  01:00:00                                                                      

  2026-06-14   39.075   9.547       3.532       68.9          137.38   38.134   ON
  02:00:00                                                                      

  2026-06-14   39.608   9.693       4.114       64.9          139.93   39.551   ON
  03:00:00                                                                      

  2026-06-14   36.6     9.371       3.252       66.61         137.61   39.848   ON
  04:00:00                                                                      

  2026-06-14   37.284   9.384       3.732       64.85         137.83   39.252   ON
  05:00:00                                                                      

  2026-06-14   38.45    9.428       3.745       64.8          140.42   39.39    ON
  06:00:00                                                                      

  2026-06-14   39.443   9.358       3.587       62.08         135.73   38.705   ON
  07:00:00                                                                      

  2026-06-14   37.196   9.409       3.504       65.83         141.85   38.874   ON
  08:00:00                                                                      

  2026-06-14   38.12    9.568       3.851       63.78         130.11   37.809   ON
  09:00:00                                                                      

  2026-06-14   38.193   9.678       4.007       64.57         136.24   39.792   ON
  10:00:00                                                                      

  2026-06-14   37.576   9.53        3.602       65.1          136.2    40.451   ON
  11:00:00                                                                      

  2026-06-14   37.884   9.585       3.92        66.14         136.22   37.843   ON
  12:00:00                                                                      

  2026-06-14   37.69    9.609       3.55        62.13         132.56   37.824   ON
  13:00:00                                                                      

  2026-06-14   36.857   9.815       3.709       65.07         136.62   39.086   ON
  14:00:00                                                                      

  2026-06-14   39.379   9.501       3.796       65.09         131.32   39.466   ON
  15:00:00                                                                      

  2026-06-14   38.204   9.514       4.275       63.67         133.36   37.95    ON
  16:00:00                                                                      

  2026-06-14   37.661   9.517       3.983       64.39         131.41   38.948   ON
  17:00:00                                                                      

  2026-06-14   38.909   9.509       3.6         64.72         138.22   38.853   ON
  18:00:00                                                                      

  2026-06-14   37.825   9.221       3.923       65.57         135.43   38.318   ON
  19:00:00                                                                      

  2026-06-14   38.899   9.599       3.448       63.59         131.01   38.582   ON
  20:00:00                                                                      

  2026-06-14   37.49    9.746       3.656       63.99         128.65   38.824   ON
  21:00:00                                                                      

  2026-06-14   38.877   9.319       4.145       66.18         134.14   38.492   ON
  22:00:00                                                                      

  2026-06-14   38.536   9.547       3.884       64.69         135.3    39.639   ON
  23:00:00                                                                      

  2026-06-15   37.502   9.809       4.014       63.13         142.71   39.324   ON
  00:00:00                                                                      

  2026-06-15   38.611   9.665       3.838       66.96         138.99   37.316   ON
  01:00:00                                                                      

  2026-06-15   38.804   9.673       3.311       65.48         128.88   39.394   ON
  02:00:00                                                                      

  2026-06-15   38.069   9.352       3.775       65.04         139.66   37.833   ON
  03:00:00                                                                      

  2026-06-15   37.146   9.54        4.112       64.11         137.53   37.383   ON
  04:00:00                                                                      

  2026-06-15   37.107   9.502       3.809       66.79         143.76   39.578   ON
  05:00:00                                                                      

  2026-06-15   37.902   9.444       4.169       63.43         140.04   38.554   ON
  06:00:00                                                                      

  2026-06-15   38.214   9.352       4.208       64.47         140.5    38.8     ON
  07:00:00                                                                      

  2026-06-15   36.072   9.366       4.151       66.25         133.13   39.097   ON
  08:00:00                                                                      

  2026-06-15   38.552   9.301       4.022       64.76         131.48   37.824   ON
  09:00:00                                                                      

  2026-06-15   38.387   9.366       4.947       64.37         136.98   40.209   ON
  10:00:00                                                                      

  2026-06-15   39.265   9.462       4.484       65.99         137.48   37.96    ON
  11:00:00                                                                      

  2026-06-15   37.831   9.45        4.987       65.61         139.31   40.694   ON
  12:00:00                                                                      

  2026-06-15   37.772   9.428       4.595       64.85         127.09   39.076   ON
  13:00:00                                                                      

  2026-06-15   38.31    9.507       5.158       63.66         133.1    39.11    ON
  14:00:00                                                                      

  2026-06-15   36.983   9.631       4.722       65.07         129.33   38.751   ON
  15:00:00                                                                      

  2026-06-15   38.07    9.27        5.371       64.19         138.97   38.654   ON
  16:00:00                                                                      

  2026-06-15   36.668   9.551       5.194       66.03         137.25   38.01    ON
  17:00:00                                                                      

  2026-06-15   37.391   9.354       5.242       64.42         138.87   38.585   ON
  18:00:00                                                                      

  2026-06-15   38.107   9.727       5.611       66.93         135.2    38.255   ON
  19:00:00                                                                      

  2026-06-15   37.996   9.492       5.839       68.22         126.87   38.999   ON
  20:00:00                                                                      

  2026-06-15   37.148   9.536       6.304       67.94         135.58   38.043   ON
  21:00:00                                                                      

  2026-06-15   38.319   9.596       6.034       65.16         136.68   39.256   ON
  22:00:00                                                                      

  2026-06-15   37.988   9.708       6.312       64.49         133.05   38.087   ON
  23:00:00                                                                      

  2026-06-16   38.482   9.313       5.97        63.68         136.6    38.42    ON
  00:00:00                                                                      

  2026-06-16   37.454   9.517       6.318       64.2          134.47   39.488   ON
  01:00:00                                                                      

  2026-06-16   37.745   9.378       6.67        64.77         137.35   38.661   ON
  02:00:00                                                                      

  2026-06-16   38.334   9.773       6.903       61.5          131.7    39.526   ON
  03:00:00                                                                      

  2026-06-16   37.117   9.344       7.01        63.92         129.33   38.865   ON
  04:00:00                                                                      

  2026-06-16   38.257   9.608       7.064       63.38         138.63   37.64    ON
  05:00:00                                                                      

  2026-06-16   37.334   9.439       6.782       63.38         146.12   37.828   ON
  06:00:00                                                                      

  2026-06-16   39.272   9.724       7.357       64.37         129.62   37.928   ON
  07:00:00                                                                      

  2026-06-16   37.355   9.453       7.406       68.09         131.31   37.155   ON
  08:00:00                                                                      

  2026-06-16   38.423   9.399       7.098       64            136.37   38.735   ON
  09:00:00                                                                      

  2026-06-16   36.436   9.659       7.153       68.54         133.46   39.515   ON
  10:00:00                                                                      

  2026-06-16   37.77    9.396       7.473       64.02         139.29   39.581   ON
  11:00:00                                                                      

  2026-06-16   38.16    9.399       7.734       63.85         134.7    37.656   ON
  12:00:00                                                                      

  2026-06-16   37.794   9.828       7.849       65.64         138.09   38.442   ON
  13:00:00                                                                      

  2026-06-16   37.567   9.823       7.694       65.38         131.51   38.343   ON
  14:00:00                                                                      

  2026-06-16   37.149   9.423       7.836       67.31         132.66   37.285   ON
  15:00:00                                                                      

  2026-06-16   37.967   9.475       7.897       65.06         135.86   37.07    ON
  16:00:00                                                                      

  2026-06-16   37.76    9.86        8.467       65.7          133.04   38.581   ON
  17:00:00                                                                      

  2026-06-16   37.91    9.572       8.833       64.53         127.2    38.899   ON
  18:00:00                                                                      

  2026-06-16   37.454   9.47        9.386       63.3          138.52   38.416   ON
  19:00:00                                                                      

  2026-06-16   36.995   9.477       8.898       65.29         142.72   37.505   ON
  20:00:00                                                                      

  2026-06-16   38.695   9.514       8.786       67.61         132.1    39.813   ON
  21:00:00                                                                      

  2026-06-16   39.022   9.493       9.074       66.05         128.98   38.858   ON
  22:00:00                                                                      

  2026-06-16   38.807   9.422       9.209       65            142      38.735   ON
  23:00:00                                                                      

  2026-06-17   38.235   9.411       9.096       64.59         135.15   38.039   ON
  00:00:00                                                                      

  2026-06-17   38.182   9.553       9.35        64.08         139.42   37.992   ON
  01:00:00                                                                      

  2026-06-17   37.854   9.501       9.245       68            135.58   40.367   ON
  02:00:00                                                                      

  2026-06-17   38.042   9.472       9.871       65.18         140.34   40.389   ON
  03:00:00                                                                      

  2026-06-17   38.023   9.631       9.57        64.75         132.15   39.338   ON
  04:00:00                                                                      

  2026-06-17   0.103    0.344       0.25        38.43         5.65     0.182    OFF
  05:00:00                                                                      

  2026-06-17   0        0.22        0.216       38.46         5.2      0.153    OFF
  06:00:00                                                                      

  2026-06-17   0        0.369       0.34        39.83         5.48     0        OFF
  07:00:00                                                                      

  2026-06-17   0        0.345       0.339       40.08         3.74     0.022    OFF
  08:00:00                                                                      

  2026-06-17   0.072    0.3         0.248       41.04         4.93     0.023    OFF
  09:00:00                                                                      

  2026-06-17   0        0.337       0.36        39.76         5.1      0.053    OFF
  10:00:00                                                                      

  2026-06-17   0        0.281       0.405       37.02         5.2      0        OFF
  11:00:00                                                                      

  2026-06-17   0.034    0.325       0.27        42.92         7        0        OFF
  12:00:00                                                                      

  2026-06-17   0        0.316       0.26        38.26         3.84     0        OFF
  13:00:00                                                                      

  2026-06-17   0.133    0.306       0.221       40.88         5.55     0.038    OFF
  14:00:00                                                                      

  2026-06-17   0.004    0.298       0.296       38.95         4.9      0.018    OFF
  15:00:00                                                                      

  2026-06-17   0        0.283       0.276       36.62         3.94     0        OFF
  16:00:00                                                                      

  2026-06-17   0.025    0.259       0.349       41.06         3.33     0.057    OFF
  17:00:00                                                                      

  2026-06-17   0.023    0.311       0.361       36.92         4.62     0.066    OFF
  18:00:00                                                                      

  2026-06-17   38.011   9.729       4.066       65.78         131.86   39.201   ON
  19:00:00                                                                      

  2026-06-17   38.423   9.381       3.914       65.18         128.03   39.529   ON
  20:00:00                                                                      

  2026-06-17   37.423   9.361       3.426       65.28         137.03   38.538   ON
  21:00:00                                                                      

  2026-06-17   38.928   9.818       3.848       65.18         139.13   40.468   ON
  22:00:00                                                                      

  2026-06-17   37.822   9.596       4.353       65.44         132.42   39.391   ON
  23:00:00                                                                      

  2026-06-18   38.093   9.284       3.545       65.55         133.79   39.413   ON
  00:00:00                                                                      

  2026-06-18   37.451   9.083       3.883       65.5          136.11   38.451   ON
  01:00:00                                                                      

  2026-06-18   37.1     9.561       3.143       64.47         140.12   38.498   ON
  02:00:00                                                                      

  2026-06-18   36.153   9.463       3.598       64.49         131.47   39.021   ON
  03:00:00                                                                      

  2026-06-18   39.932   9.699       3.837       65.98         133.4    37.75    ON
  04:00:00                                                                      

  2026-06-18   39.013   9.5         3.955       63.56         133.38   38.809   ON
  05:00:00                                                                      

  2026-06-18   37.374   9.709       4.467       64.59         130.12   37.754   ON
  06:00:00                                                                      

  2026-06-18   37.767   9.764       3.99        65.57         132.66   38.364   ON
  07:00:00                                                                      

  2026-06-18   36.802   9.341       3.789       67.54         135.6    39.739   ON
  08:00:00                                                                      

  2026-06-18   38.553   9.404       4.271       64.28         136.24   38.679   ON
  09:00:00                                                                      

  2026-06-18   38.299   9.483       3.773       62.52         141.42   38.565   ON
  10:00:00                                                                      

  2026-06-18   38.546   9.507       3.878       63.9          138.16   39.273   ON
  11:00:00                                                                      

  2026-06-18   37.524   9.471       4.072       66.89         132.41   37.585   ON
  12:00:00                                                                      

  2026-06-18   38.462   9.694       3.894       64.16         134.23   39.051   ON
  13:00:00                                                                      

  2026-06-18   37.956   9.588       3.62        66.79         133.63   38.663   ON
  14:00:00                                                                      

  2026-06-18   36.947   9.664       4.074       62.03         122.36   38.494   ON
  15:00:00                                                                      

  2026-06-18   38.944   9.355       3.753       62.87         138.12   38.799   ON
  16:00:00                                                                      

  2026-06-18   37.578   9.146       3.808       64.31         137.71   38.914   ON
  17:00:00                                                                      

  2026-06-18   38.512   9.423       3.906       65.35         133.81   38.958   ON
  18:00:00                                                                      

  2026-06-18   38.554   9.394       3.615       67.02         141.8    37.138   ON
  19:00:00                                                                      

  2026-06-18   38.709   9.506       3.827       62.85         132.94   38.089   ON
  20:00:00                                                                      

  2026-06-18   38.66    9.453       3.923       64.89         131.47   39.301   ON
  21:00:00                                                                      

  2026-06-18   37.967   9.396       4.275       66.18         131.19   37.723   ON
  22:00:00                                                                      

  2026-06-18   36.669   9.583       3.71        66.31         136.91   39.738   ON
  23:00:00                                                                      

  2026-06-19   38.318   9.484       3.757       65.11         140.16   38.527   ON
  00:00:00                                                                      

  2026-06-19   39.962   9.434       4.08        65.55         139.65   37.782   ON
  01:00:00                                                                      

  2026-06-19   37.749   9.544       3.806       64.38         129.18   41.193   ON
  02:00:00                                                                      

  2026-06-19   38.558   9.384       3.686       66.05         137.28   39.276   ON
  03:00:00                                                                      

  2026-06-19   38.065   9.856       3.892       66.45         126.66   39.458   ON
  04:00:00                                                                      

  2026-06-19   37.72    9.677       3.597       64.86         135      38.126   ON
  05:00:00                                                                      

  2026-06-19   38.079   9.309       3.706       66.88         127.06   38.901   ON
  06:00:00                                                                      

  2026-06-19   39.11    9.231       3.775       65.02         136.05   37.65    ON
  07:00:00                                                                      

  2026-06-19   38.669   9.519       3.648       63.95         137.15   38.767   ON
  08:00:00                                                                      

  2026-06-19   38.052   9.451       3.685       65.92         141.61   38.808   ON
  09:00:00                                                                      

  2026-06-19   38.248   9.41        4.139       66.67         133.47   39.519   ON
  10:00:00                                                                      

  2026-06-19   36.271   9.34        3.328       64.85         138.25   38.834   ON
  11:00:00                                                                      

  2026-06-19   36.761   9.342       3.775       65.55         134.37   39.461   ON
  12:00:00                                                                      

  2026-06-19   36.181   9.809       3.732       64.36         135.19   39.33    ON
  13:00:00                                                                      

  2026-06-19   37.834   9.597       4.091       65.81         129.15   40.422   ON
  14:00:00                                                                      

  2026-06-19   39.01    9.513       3.882       63.81         127.88   39.411   ON
  15:00:00                                                                      

  2026-06-19   38.878   9.369       3.938       63.63         142.71   38.393   ON
  16:00:00                                                                      

  2026-06-19   37.526   9.35        4.063       67.39         131.15   39.232   ON
  17:00:00                                                                      

  2026-06-19   38.374   9.36        3.989       65.82         133.91   37.745   ON
  18:00:00                                                                      

  2026-06-19   38.22    9.468       3.539       63.35         135.09   38.57    ON
  19:00:00                                                                      

  2026-06-19   39.119   9.307       3.609       64.57         133.3    39.212   ON
  20:00:00                                                                      

  2026-06-19   36.783   9.463       3.852       63.81         136.66   39.199   ON
  21:00:00                                                                      

  2026-06-19   36.888   9.563       4.039       66.02         138.79   38.707   ON
  22:00:00                                                                      

  2026-06-19   38.023   9.357       3.753       64.17         137.54   37.989   ON
  23:00:00                                                                      

  2026-06-20   37.507   9.239       3.726       63.34         140.13   38.836   ON
  00:00:00                                                                      

  2026-06-20   36.786   9.708       3.929       64.46         148.78   37.186   ON
  01:00:00                                                                      

  2026-06-20   37.779   9.384       4.149       61.89         136.1    39.543   ON
  02:00:00                                                                      

  2026-06-20   39.492   9.496       3.838       64.45         138.79   39.268   ON
  03:00:00                                                                      

  2026-06-20   38.179   9.7         4.041       62.62         137.79   37.739   ON
  04:00:00                                                                      

  2026-06-20   37.345   9.575       4.157       63.72         133.99   38.842   ON
  05:00:00                                                                      

  2026-06-20   38.743   9.492       4.018       66.04         138.96   38.785   ON
  06:00:00                                                                      

  2026-06-20   37.055   9.458       3.907       66.98         133.09   38.447   ON
  07:00:00                                                                      

  2026-06-20   37.969   9.311       3.967       66.14         130.16   39.47    ON
  08:00:00                                                                      

  2026-06-20   37.772   9.45        3.813       66.17         137.47   38.749   ON
  09:00:00                                                                      

  2026-06-20   38.272   9.555       4.474       61.58         141.11   37.269   ON
  10:00:00                                                                      

  2026-06-20   38.023   9.648       3.742       63.77         130.32   37.012   ON
  11:00:00                                                                      

  2026-06-20   38.412   9.359       3.665       66.05         138.44   39.97    ON
  12:00:00                                                                      

  2026-06-20   37.426   9.572       3.789       66.17         137.94   38.767   ON
  13:00:00                                                                      

  2026-06-20   38.041   9.707       3.759       64.53         132.43   37.867   ON
  14:00:00                                                                      

  2026-06-20   38.657   9.574       3.725       63.89         131.82   37.69    ON
  15:00:00                                                                      

  2026-06-20   37.21    9.652       4.262       66.16         123.92   40.163   ON
  16:00:00                                                                      

  2026-06-20   38.778   9.368       4.144       63.42         133.5    39.326   ON
  17:00:00                                                                      

  2026-06-20   38.195   9.389       3.572       64.21         138.37   37.324   ON
  18:00:00                                                                      

  2026-06-20   36.912   9.707       3.804       63.35         139.9    38.212   ON
  19:00:00                                                                      

  2026-06-20   38.555   9.699       3.801       62.02         144.47   38.386   ON
  20:00:00                                                                      

  2026-06-20   38.148   9.523       3.226       65.21         136.91   39.162   ON
  21:00:00                                                                      

  2026-06-20   37.181   9.37        3.718       66.55         133.38   38.222   ON
  22:00:00                                                                      

  2026-06-20   38.315   9.611       3.849       65.84         139.73   39.084   ON
  23:00:00                                                                      

  2026-06-21   36.895   9.377       3.849       63.88         139.6    38.574   ON
  00:00:00                                                                      

  2026-06-21   37.212   9.504       3.665       65.93         125.74   37.686   ON
  01:00:00                                                                      

  2026-06-21   37.345   9.815       3.941       63.48         136.3    38.872   ON
  02:00:00                                                                      

  2026-06-21   38.343   9.634       3.221       60.72         133.06   38.824   ON
  03:00:00                                                                      

  2026-06-21   39.343   9.578       3.642       64.28         143.44   38.289   ON
  04:00:00                                                                      

  2026-06-21   37.886   9.455       4.226       65.74         136.79   37.627   ON
  05:00:00                                                                      

  2026-06-21   38.301   9.187       3.541       62.58         138.83   38.342   ON
  06:00:00                                                                      

  2026-06-21   38.208   9.612       3.719       64.5          132.9    37.311   ON
  07:00:00                                                                      

  2026-06-21   38.294   9.485       4.314       65.1          134.7    37.811   ON
  08:00:00                                                                      

  2026-06-21   38.687   9.608       3.691       65.42         127.21   38.607   ON
  09:00:00                                                                      

  2026-06-21   37.812   9.267       3.58        67.26         133.94   37.968   ON
  10:00:00                                                                      

  2026-06-21   38.407   9.483       4.154       63.64         143.27   38.707   ON
  11:00:00                                                                      

  2026-06-21   38.452   9.601       4.046       63.81         137.21   37.9     ON
  12:00:00                                                                      

  2026-06-21   37.47    9.673       4.18        65.31         132.57   39.808   ON
  13:00:00                                                                      

  2026-06-21   38.311   9.416       3.836       66.58         131.39   39.295   ON
  14:00:00                                                                      

  2026-06-21   39.14    9.247       3.827       65.27         138.6    38.821   ON
  15:00:00                                                                      

  2026-06-21   36.34    9.483       3.319       64.35         136.26   38.553   ON
  16:00:00                                                                      

  2026-06-21   37.588   9.51        3.713       64.63         134.35   37.763   ON
  17:00:00                                                                      

  2026-06-21   38.868   9.615       4.182       67.24         132.93   38.469   ON
  18:00:00                                                                      

  2026-06-21   38.59    9.529       4.005       66.15         138.72   38.861   ON
  19:00:00                                                                      

  2026-06-21   38.081   9.639       3.707       65.92         127.96   37.127   ON
  20:00:00                                                                      

  2026-06-21   38.297   9.491       3.724       65.34         132.57   39.385   ON
  21:00:00                                                                      

  2026-06-21   37.435   9.34        4.298       66.62         133.16   38.703   ON
  22:00:00                                                                      

  2026-06-21   38.343   9.586       3.887       66            132.74   38.058   ON
  23:00:00                                                                      

  2026-06-22   38.213   9.472       3.795       65.52         139.08   38.993   ON
  00:00:00                                                                      

  2026-06-22   38.298   9.514       4.01        64.5          138.89   39.525   ON
  01:00:00                                                                      

  2026-06-22   37.551   9.625       3.953       64.73         132.36   38.506   ON
  02:00:00                                                                      

  2026-06-22   38.078   9.59        3.743       65.47         137.72   39.066   ON
  03:00:00                                                                      

  2026-06-22   36.66    9.484       3.408       62.52         133.44   39.138   ON
  04:00:00                                                                      

  2026-06-22   38.525   9.602       4.079       63.92         131.79   38.507   ON
  05:00:00                                                                      

  2026-06-22   39.129   9.694       3.826       63.38         132.42   38.326   ON
  06:00:00                                                                      

  2026-06-22   37.131   9.522       3.424       65.66         132.72   39.3     ON
  07:00:00                                                                      

  2026-06-22   37.924   9.292       4.364       67.35         136.39   39.653   ON
  08:00:00                                                                      

  2026-06-22   36.587   9.562       4.052       66.32         134.38   38.663   ON
  09:00:00                                                                      

  2026-06-22   38.586   9.516       3.514       65.29         130.6    38.172   ON
  10:00:00                                                                      

  2026-06-22   37.572   9.553       3.974       63.04         127.59   39.594   ON
  11:00:00                                                                      

  2026-06-22   37.925   9.084       3.664       67.8          136.14   38.314   ON
  12:00:00                                                                      

  2026-06-22   37.383   9.214       3.734       65.84         138.78   38.455   ON
  13:00:00                                                                      

  2026-06-22   37.161   9.316       3.687       66.73         131.77   38.887   ON
  14:00:00                                                                      

  2026-06-22   38.368   9.431       3.763       65.53         137.2    39.363   ON
  15:00:00                                                                      

  2026-06-22   38.131   9.378       3.721       66.06         139.9    38.622   ON
  16:00:00                                                                      

  2026-06-22   38.659   9.369       4.433       66.84         132.95   37.574   ON
  17:00:00                                                                      

  2026-06-22   38.494   9.378       4.188       64.4          139.37   38.299   ON
  18:00:00                                                                      

  2026-06-22   37.278   9.413       3.385       66.11         133.32   39.282   ON
  19:00:00                                                                      

  2026-06-22   39.287   9.364       4.079       61.87         133.96   39.294   ON
  20:00:00                                                                      

  2026-06-22   36.389   9.337       3.744       66.47         130.71   39.379   ON
  21:00:00                                                                      

  2026-06-22   38.441   9.47        3.671       66.08         132.17   38.462   ON
  22:00:00                                                                      

  2026-06-22   38.49    9.537       3.699       65.12         133.29   38.546   ON
  23:00:00                                                                      

  2026-06-23   39.075   9.45        4.005       66.47         143.44   39.352   ON
  00:00:00                                                                      

  2026-06-23   36.935   9.351       3.53        69.5          131.79   38.244   ON
  01:00:00                                                                      

  2026-06-23   38.238   9.443       4.064       65.81         135.59   39.773   ON
  02:00:00                                                                      

  2026-06-23   37.076   9.751       3.821       65.29         134.57   37.709   ON
  03:00:00                                                                      

  2026-06-23   39.628   9.497       4.206       64.01         133.44   39.958   ON
  04:00:00                                                                      

  2026-06-23   36.218   9.383       3.848       65.24         132.71   37.851   ON
  05:00:00                                                                      

  2026-06-23   38.128   9.526       4.076       64.23         133.5    38.815   ON
  06:00:00                                                                      

  2026-06-23   38.374   9.334       3.043       66.62         131.11   38.474   ON
  07:00:00                                                                      

  2026-06-23   37.403   9.387       3.831       64.74         129.55   37.791   ON
  08:00:00                                                                      

  2026-06-23   37.279   9.667       3.844       65.5          132.36   39.551   ON
  09:00:00                                                                      

  2026-06-23   40.158   9.707       3.594       65.82         139.88   39.071   ON
  10:00:00                                                                      

  2026-06-23   37.567   9.471       3.992       65.56         134.85   39.129   ON
  11:00:00                                                                      

  2026-06-23   37.687   9.399       4.278       65.28         132.22   39.957   ON
  12:00:00                                                                      

  2026-06-23   38.236   9.696       3.503       65.42         140.07   39.71    ON
  13:00:00                                                                      

  2026-06-23   37.958   9.516       3.502       64.49         135.08   39.303   ON
  14:00:00                                                                      

  2026-06-23   36.69    9.652       3.976       65.78         134.84   39.129   ON
  15:00:00                                                                      

  2026-06-23   37.073   9.29        3.722       65.53         132.34   39.357   ON
  16:00:00                                                                      

  2026-06-23   37.341   9.387       4.272       64.82         138.57   39.012   ON
  17:00:00                                                                      

  2026-06-23   37.605   9.361       3.868       64.33         133.05   38.357   ON
  18:00:00                                                                      

  2026-06-23   38.226   9.203       4.074       67.86         130.39   39.324   ON
  19:00:00                                                                      

  2026-06-23   37.713   9.067       3.439       64.91         125.74   37.591   ON
  20:00:00                                                                      

  2026-06-23   37.779   9.597       3.861       67.51         130.06   37.846   ON
  21:00:00                                                                      

  2026-06-23   38.383   9.462       3.749       66.68         135.13   38.794   ON
  22:00:00                                                                      

  2026-06-23   37.728   9.453       3.975       64.07         132.78   38.671   ON
  23:00:00                                                                      

  2026-06-24   38.168   9.494       4.061       65.56         131.08   39.233   ON
  00:00:00                                                                      

  2026-06-24   38.41    9.476       3.687       64.61         135.13   38.256   ON
  01:00:00                                                                      

  2026-06-24   37.866   9.539       3.554       65.02         133.92   38.81    ON
  02:00:00                                                                      

  2026-06-24   37.827   9.36        3.477       65.45         130.09   38.482   ON
  03:00:00                                                                      

  2026-06-24   38.828   9.748       4.123       67.66         133.66   40.173   ON
  04:00:00                                                                      

  2026-06-24   38.612   9.512       3.597       64.56         134.54   38.226   ON
  05:00:00                                                                      

  2026-06-24   40.341   9.397       4.048       67.02         130.66   39.256   ON
  06:00:00                                                                      

  2026-06-24   38.459   9.294       3.719       63.95         135.86   38.726   ON
  07:00:00                                                                      

  2026-06-24   38.178   9.535       3.885       65.36         143.79   39.79    ON
  08:00:00                                                                      

  2026-06-24   38.663   9.653       3.715       65.84         133.54   38.702   ON
  09:00:00                                                                      

  2026-06-24   38.342   9.393       3.847       65.39         139.27   38.254   ON
  10:00:00                                                                      

  2026-06-24   38.698   9.46        3.572       62.35         135.31   38.06    ON
  11:00:00                                                                      

  2026-06-24   37.783   9.308       3.521       64.69         132.48   37.719   ON
  12:00:00                                                                      

  2026-06-24   37.447   9.275       4.133       63.21         136.57   37.054   ON
  13:00:00                                                                      

  2026-06-24   36.544   9.842       3.932       65.45         137.22   39.257   ON
  14:00:00                                                                      

  2026-06-24   38.746   9.45        3.443       65.19         139.62   37.282   ON
  15:00:00                                                                      

  2026-06-24   36.948   9.51        3.657       64.06         140      37.774   ON
  16:00:00                                                                      

  2026-06-24   39.147   9.724       3.779       66.72         140.31   38.553   ON
  17:00:00                                                                      

  2026-06-24   37.437   9.542       3.665       66.36         133.27   37.724   ON
  18:00:00                                                                      

  2026-06-24   37.201   9.671       3.934       64.44         132.39   38.608   ON
  19:00:00                                                                      

  2026-06-24   37.334   9.234       4.044       69.09         138.9    38.407   ON
  20:00:00                                                                      

  2026-06-24   37.586   9.75        3.975       65.24         128.01   37.075   ON
  21:00:00                                                                      

  2026-06-24   38.456   9.517       3.443       66.76         137.59   39.272   ON
  22:00:00                                                                      

  2026-06-24   38.073   9.714       3.267       64.74         137.38   38.694   ON
  23:00:00                                                                      

  2026-06-25   37.584   9.448       3.805       62.92         136.37   38.598   ON
  00:00:00                                                                      

  2026-06-25   39.702   9.482       3.871       66.85         127.87   37.134   ON
  01:00:00                                                                      

  2026-06-25   36.47    9.599       3.884       65.96         131      38.7     ON
  02:00:00                                                                      

  2026-06-25   38.184   9.541       3.733       62.31         127.22   38.56    ON
  03:00:00                                                                      

  2026-06-25   38.376   9.519       3.574       65.26         138.48   39.445   ON
  04:00:00                                                                      

  2026-06-25   38.499   9.658       3.682       64.98         131.51   39.238   ON
  05:00:00                                                                      

  2026-06-25   39.497   9.535       3.654       66.13         133.39   39.969   ON
  06:00:00                                                                      

  2026-06-25   38.187   9.529       4.025       65.53         136.81   37.829   ON
  07:00:00                                                                      

  2026-06-25   36.716   9.573       3.8         65.48         138.67   39.723   ON
  08:00:00                                                                      

  2026-06-25   39.068   9.441       3.862       67.13         131.25   39.7     ON
  09:00:00                                                                      

  2026-06-25   37.371   9.48        3.711       64.1          132.94   38.227   ON
  10:00:00                                                                      

  2026-06-25   37.315   9.716       4.01        64.55         134.42   38.58    ON
  11:00:00                                                                      

  2026-06-25   38.276   9.439       4.093       64.61         137.79   38.412   ON
  12:00:00                                                                      

  2026-06-25   37.353   9.478       3.663       65.41         137.1    38.631   ON
  13:00:00                                                                      

  2026-06-25   37.713   9.412       3.625       64.69         141.34   38.855   ON
  14:00:00                                                                      

  2026-06-25   38.319   9.368       3.759       64.64         132.55   39.185   ON
  15:00:00                                                                      

  2026-06-25   37.088   9.361       3.828       63.84         130.54   38.647   ON
  16:00:00                                                                      

  2026-06-25   38.45    9.679       3.993       63.89         130.31   37.554   ON
  17:00:00                                                                      

  2026-06-25   36.988   9.696       3.75        65.4          136.24   39.183   ON
  18:00:00                                                                      

  2026-06-25   37.425   9.322       3.776       64.14         135.41   38.421   ON
  19:00:00                                                                      

  2026-06-25   36.668   9.601       4.32        65.02         138.21   39       ON
  20:00:00                                                                      

  2026-06-25   38.468   9.609       4.161       66.54         131.14   39.339   ON
  21:00:00                                                                      

  2026-06-25   38.771   9.661       4.542       65.79         127.88   37.581   ON
  22:00:00                                                                      

  2026-06-25   38.09    9.531       3.637       66.73         131.11   37.563   ON
  23:00:00                                                                      

  2026-06-26   38.016   9.679       3.86        62.46         132.27   38.69    ON
  00:00:00                                                                      

  2026-06-26   37.257   9.696       3.723       64.14         138.67   38.591   ON
  01:00:00                                                                      

  2026-06-26   39.429   9.199       3.787       64.59         133.34   39.062   ON
  02:00:00                                                                      

  2026-06-26   37.612   9.852       3.471       65.31         136.92   37.881   ON
  03:00:00                                                                      

  2026-06-26   37.728   9.596       3.435       65.18         135.78   39.362   ON
  04:00:00                                                                      

  2026-06-26   38.308   9.647       3.788       64.2          134.21   39.071   ON
  05:00:00                                                                      

  2026-06-26   37.43    9.762       3.728       65.94         134.48   37.573   ON
  06:00:00                                                                      

  2026-06-26   37.015   9.622       3.682       65.55         129.53   40.542   ON
  07:00:00                                                                      

  2026-06-26   39.566   9.381       3.801       63.45         137.3    38.582   ON
  08:00:00                                                                      

  2026-06-26   37.952   9.657       3.488       65.72         140.63   39.151   ON
  09:00:00                                                                      

  2026-06-26   37.411   9.689       3.599       63.41         135.9    39.474   ON
  10:00:00                                                                      

  2026-06-26   38.257   9.492       3.876       67.69         130.44   38.569   ON
  11:00:00                                                                      

  2026-06-26   37.163   9.5         3.839       64.74         132.81   37.916   ON
  12:00:00                                                                      

  2026-06-26   36.822   9.05        3.658       65.04         130.37   38.703   ON
  13:00:00                                                                      

  2026-06-26   36.125   9.547       4.651       66.39         135.84   38.014   ON
  14:00:00                                                                      

  2026-06-26   38.17    9.56        4.257       63.77         131.72   38.402   ON
  15:00:00                                                                      

  2026-06-26   39.35    9.342       3.88        62.69         135.75   38.97    ON
  16:00:00                                                                      

  2026-06-26   36.791   9.393       3.579       64.38         139.26   38.269   ON
  17:00:00                                                                      

  2026-06-26   38.253   9.491       3.347       67.14         132.42   39.263   ON
  18:00:00                                                                      

  2026-06-26   36.856   9.341       3.607       66.15         123.1    39.183   ON
  19:00:00                                                                      

  2026-06-26   39.024   9.607       3.948       63.46         139.22   39.218   ON
  20:00:00                                                                      

  2026-06-26   37.995   9.314       3.573       64.11         134.65   39.81    ON
  21:00:00                                                                      

  2026-06-26   38.636   9.562       4.044       66.87         135.16   39.969   ON
  22:00:00                                                                      

  2026-06-26   37.612   9.349       3.835       67.84         146.04   38.999   ON
  23:00:00                                                                      

  2026-06-27   37.354   9.58        3.763       63.44         130.82   38.743   ON
  00:00:00                                                                      

  2026-06-27   37.687   9.367       3.712       64.71         135.15   39.306   ON
  01:00:00                                                                      

  2026-06-27   38.512   9.543       3.797       64.98         130.83   39.518   ON
  02:00:00                                                                      

  2026-06-27   38.03    9.531       3.365       62.38         136.39   37.564   ON
  03:00:00                                                                      

  2026-06-27   37.195   9.271       3.563       65.82         141.05   39.369   ON
  04:00:00                                                                      

  2026-06-27   39.334   9.544       3.947       66.23         132.72   38.846   ON
  05:00:00                                                                      

  2026-06-27   38.278   9.529       3.661       65.44         136.29   39.179   ON
  06:00:00                                                                      

  2026-06-27   38.151   9.486       3.605       63.99         132.82   40.417   ON
  07:00:00                                                                      

  2026-06-27   37.77    9.426       3.566       64.9          131.63   40.621   ON
  08:00:00                                                                      

  2026-06-27   37.939   9.636       4.031       65.84         139.56   37.751   ON
  09:00:00                                                                      

  2026-06-27   38.344   9.464       3.941       64.36         132.58   39.362   ON
  10:00:00                                                                      

  2026-06-27   37.377   9.554       3.627       64.53         131.42   39.538   ON
  11:00:00                                                                      

  2026-06-27   40.453   9.462       4.209       64.74         137.15   38.069   ON
  12:00:00                                                                      

  2026-06-27   37.787   9.42        3.821       66.54         137.85   38.976   ON
  13:00:00                                                                      

  2026-06-27   37.123   9.383       4.002       67.03         137.42   39.683   ON
  14:00:00                                                                      

  2026-06-27   38.614   9.533       3.826       66.08         129.88   38.967   ON
  15:00:00                                                                      

  2026-06-27   37.623   9.442       3.85        65.04         129.1    39.496   ON
  16:00:00                                                                      

  2026-06-27   37.466   9.47        3.712       65.59         137.18   37.797   ON
  17:00:00                                                                      

  2026-06-27   36.782   9.502       3.624       65.59         141.71   39.035   ON
  18:00:00                                                                      

  2026-06-27   37.497   9.584       3.653       63.87         130.49   38.211   ON
  19:00:00                                                                      

  2026-06-27   37.963   9.213       3.703       66.89         135.72   39.958   ON
  20:00:00                                                                      

  2026-06-27   36.804   9.373       3.632       64.1          134.39   37.544   ON
  21:00:00                                                                      

  2026-06-27   37.995   9.453       3.897       65.3          136      38.34    ON
  22:00:00                                                                      

  2026-06-27   39.108   9.576       3.491       63.62         141.4    38.039   ON
  23:00:00                                                                      

  2026-06-28   38.31    9.414       3.795       64.27         133.28   37.703   ON
  00:00:00                                                                      

  2026-06-28   37.868   9.352       3.471       66.34         136.28   40.056   ON
  01:00:00                                                                      

  2026-06-28   37.195   9.493       4.401       64.27         136.01   39.474   ON
  02:00:00                                                                      

  2026-06-28   38.849   9.454       3.733       62.99         133.22   38.743   ON
  03:00:00                                                                      

  2026-06-28   37.909   9.732       3.77        61.85         137.95   38.354   ON
  04:00:00                                                                      

  2026-06-28   39.333   9.498       4.084       63.6          138.07   38.472   ON
  05:00:00                                                                      

  2026-06-28   36.662   9.737       3.735       64.11         135.19   38.174   ON
  06:00:00                                                                      

  2026-06-28   37.738   9.581       3.631       64.95         138.97   39.248   ON
  07:00:00                                                                      

  2026-06-28   38.135   9.155       3.861       63.27         131.95   39.161   ON
  08:00:00                                                                      

  2026-06-28   38.044   9.497       4.03        64.78         134.22   39.573   ON
  09:00:00                                                                      

  2026-06-28   38.312   9.562       3.994       63.82         131.96   39.015   ON
  10:00:00                                                                      

  2026-06-28   38.482   9.586       4.041       65.45         136.74   38.933   ON
  11:00:00                                                                      

  2026-06-28   36.267   9.733       3.779       65.01         135.18   37.593   ON
  12:00:00                                                                      

  2026-06-28   39.208   9.422       4.038       63.96         138.58   39.588   ON
  13:00:00                                                                      

  2026-06-28   38.493   9.475       3.639       63.84         139.32   39.186   ON
  14:00:00                                                                      

  2026-06-28   39.224   9.398       3.983       64.7          138.01   39.386   ON
  15:00:00                                                                      

  2026-06-28   38.324   9.571       3.978       65.21         137.3    40.227   ON
  16:00:00                                                                      

  2026-06-28   38.114   9.365       4.329       64.03         137.25   38.414   ON
  17:00:00                                                                      

  2026-06-28   35.937   9.374       3.613       65.9          141.62   36.899   ON
  18:00:00                                                                      

  2026-06-28   38.265   9.363       4.239       64.15         128.4    38.689   ON
  19:00:00                                                                      

  2026-06-28   37.003   9.468       3.993       63.34         137.93   39.65    ON
  20:00:00                                                                      

  2026-06-28   39.021   9.32        3.77        65.78         135.26   39.113   ON
  21:00:00                                                                      

  2026-06-28   37.342   9.739       3.811       63.03         129.9    39.202   ON
  22:00:00                                                                      

  2026-06-28   38.325   9.394       4.181       67.09         133.21   38.424   ON
  23:00:00                                                                      

  2026-06-29   38.48    9.323       3.618       64.53         131.19   39.141   ON
  00:00:00                                                                      

  2026-06-29   37.949   9.566       3.913       64.77         135.89   38.66    ON
  01:00:00                                                                      

  2026-06-29   37.437   9.677       4.314       67.52         136.93   40.312   ON
  02:00:00                                                                      

  2026-06-29   40.187   9.262       3.494       63.44         135.77   38.96    ON
  03:00:00                                                                      

  2026-06-29   36.942   9.499       3.595       66.67         130.63   37.247   ON
  04:00:00                                                                      

  2026-06-29   37.54    9.453       3.525       65.23         132.17   37.715   ON
  05:00:00                                                                      

  2026-06-29   37.193   9.256       3.908       65.4          134.67   38.379   ON
  06:00:00                                                                      

  2026-06-29   38.92    9.282       3.343       66.78         132.11   38.857   ON
  07:00:00                                                                      

  2026-06-29   38.585   9.62        4.291       67.43         130.99   39.878   ON
  08:00:00                                                                      

  2026-06-29   37.801   9.43        3.931       65.76         128.28   39.579   ON
  09:00:00                                                                      

  2026-06-29   37.428   9.471       4.161       65.71         134.06   38.23    ON
  10:00:00                                                                      

  2026-06-29   37.747   9.38        3.785       64.75         138.29   38.89    ON
  11:00:00                                                                      

  2026-06-29   38.603   9.488       3.777       63.49         133.44   39.066   ON
  12:00:00                                                                      

  2026-06-29   39.162   9.366       3.507       63.22         135.66   37.329   ON
  13:00:00                                                                      

  2026-06-29   37.658   9.656       3.882       66.42         129.55   40.769   ON
  14:00:00                                                                      

  2026-06-29   37.949   9.545       3.795       65.05         132.23   38.206   ON
  15:00:00                                                                      

  2026-06-29   39.733   9.599       3.889       63.75         141.2    39.542   ON
  16:00:00                                                                      

  2026-06-29   39.279   9.515       3.353       64.63         129.5    39.253   ON
  17:00:00                                                                      

  2026-06-29   38.249   9.265       3.618       65.67         144.23   37.207   ON
  18:00:00                                                                      

  2026-06-29   37.789   9.866       3.845       64.63         132.88   39.957   ON
  19:00:00                                                                      

  2026-06-29   38.36    9.365       3.784       65.51         128.29   39.868   ON
  20:00:00                                                                      

  2026-06-29   37.685   9.482       3.738       66.03         134.54   38.825   ON
  21:00:00                                                                      

  2026-06-29   38.264   9.332       3.829       66.84         135.15   40.378   ON
  22:00:00                                                                      

  2026-06-29   38.384   9.475       3.439       63.41         137.27   39.199   ON
  23:00:00                                                                      

  2026-06-30   38.481   9.352       3.901       64.54         138.78   39.423   ON
  00:00:00                                                                      

  2026-06-30   38.234   9.551       3.635       65.26         133.49   39.759   ON
  01:00:00                                                                      

  2026-06-30   38.842   9.717       4.149       65.11         137.06   37.364   ON
  02:00:00                                                                      

  2026-06-30   38.649   9.401       3.819       65.89         137.28   39.639   ON
  03:00:00                                                                      

  2026-06-30   38.024   9.463       4.061       62.54         138.65   38.995   ON
  04:00:00                                                                      

  2026-06-30   37.406   9.528       3.767       63.48         141.82   39.031   ON
  05:00:00                                                                      

  2026-06-30   37.745   9.456       3.878       66.52         138.36   37.603   ON
  06:00:00                                                                      

  2026-06-30   39.403   9.593       3.7         67.61         135.42   39.727   ON
  07:00:00                                                                      

  2026-06-30   38.43    9.707       3.683       64.98         136.11   39.151   ON
  08:00:00                                                                      

  2026-06-30   39.188   9.221       3.535       63.34         138.04   38.264   ON
  09:00:00                                                                      

  2026-06-30   37.383   9.672       3.781       62.69         129.84   38.801   ON
  10:00:00                                                                      

  2026-06-30   38.883   9.395       4.052       65.98         138.35   39.849   ON
  11:00:00                                                                      

  2026-06-30   39.963   9.453       3.892       67.61         134.55   39.422   ON
  12:00:00                                                                      

  2026-06-30   37.358   9.322       3.632       66.4          132.65   38.338   ON
  13:00:00                                                                      

  2026-06-30   39.136   9.726       3.736       64.36         139.36   38.526   ON
  14:00:00                                                                      

  2026-06-30   37.676   9.479       3.764       65.71         139.22   40.691   ON
  15:00:00                                                                      

  2026-06-30   38.054   9.578       3.458       62.61         130.33   37.671   ON
  16:00:00                                                                      

  2026-06-30   37.64    9.503       3.726       63.8          133.54   38.875   ON
  17:00:00                                                                      

  2026-06-30   37.919   9.537       3.628       64.58         132.52   39.443   ON
  18:00:00                                                                      

  2026-06-30   38.096   9.584       4.433       63.91         127.38   39.785   ON
  19:00:00                                                                      

  2026-06-30   37.087   9.696       3.685       62.77         138.11   38.016   ON
  20:00:00                                                                      

  2026-06-30   38.492   9.778       3.985       66.67         135.29   39.741   ON
  21:00:00                                                                      

  2026-06-30   37.756   9.444       3.661       65.9          128.25   39.079   ON
  22:00:00                                                                      

  2026-06-30   37.548   9.338       3.674       62.93         137.89   38.804   ON
  23:00:00                                                                      
  --------------------------------------------------------------------------------------

## 4. Condition monitoring records

The source provides 26 weekly readings for each monitored equipment
item. Alarm and trip limits are preserved in the order shown in the
source record.

### PU-2101B Parameter

#### Nameplate and identification

  ---------------------------------------------------------------------
  Field                              Value
  ---------------------------------- ----------------------------------
  Equipment Tag                      PU-2101B Parameter

  Equipment Name                     Feed Charge Pump PU-2101B Overall
                                     Vibration (mm/s)

  Equipment Type                     Centrifugal Pump Seal Flush Flow
                                     (L/min)

  Equipment Class                    B Discharge Pressure (barg)

  Plant / Unit                       Resin Plant (ARP) Bearing Temp
                                     (°C)

  Discipline                         ROT

  Criticality                        Medium

  Design Life                        5 years (bearing) / 24 months
                                     (seal element)

  Monitoring Method                  Online DCS + monthly
                                     vibration/thermography route

  Linked RCA / AR No.                AR-2026-ARP-0117

  Failure Date                       12-Mar-2026

  Dominant Failure Mode              Mechanical Seal Leakage
  ---------------------------------------------------------------------

#### Monitored parameters and alarm/trip limits

Parameter Alarm / Trip ----------- --------------

#### Weekly condition record

  Week   Date         Health status
  ------ ------------ ---------------
  1      2025-10-23   3.893
  2      2025-10-30   3.941
  3      2025-11-06   3.805
  4      2025-11-13   4.062
  5      2025-11-20   4.314
  6      2025-11-27   4.42
  7      2025-12-04   4.249
  8      2025-12-11   4.43
  9      2025-12-18   5.01
  10     2025-12-25   5.437
  11     2026-01-01   5.597
  12     2026-01-08   6.115
  13     2026-01-15   6.427
  14     2026-01-22   6.874
  15     2026-01-29   7.371
  16     2026-02-05   7.882
  17     2026-02-12   8.347
  18     2026-02-19   9.268
  19     2026-02-26   9.764
  20     2026-03-05   10.218
  21     2026-03-12   11.22
  22     2026-03-19   3.624
  23     2026-03-26   3.77
  24     2026-04-02   3.587
  25     2026-04-09   3.692
  26     2026-04-16   3.796

#### Remarks

-   Degradation trend --- under close monitoring
-   Degradation trend --- under close monitoring
-   Degradation trend --- under close monitoring
-   FAILURE --- Mechanical Seal Leakage; unplanned
-   downtime 18.5 h
-   Post-repair baseline restored (CAPA executed)

#### Performance summary

  KPI                         Value    Basis / Formula
  --------------------------- -------- ---------------------------------
  Monitoring Period (weeks)   26       Number of weekly readings
  Total Downtime (hours)      18.5     From linked RCA downtime window
  Period Hours                4368     4368
  Availability (%)            99.6     (Period-Downtime)/Period
  No. of Failures (period)    1        Failure events this period
  MTBF (hours)                4368     Period Hours / No. of Failures
  MTTR (hours)                18.5     Mean time to repair
  ALARM readings              6        Count of ALARM weeks
  TRIP readings               1        Count of TRIP weeks
  NORMAL readings             19       Count of NORMAL weeks
  PM Compliance (%)           92.0     PM completed vs scheduled
  Production Loss (ton)       251.6    Downtime x rate loss (from RCA)
  Estimated Loss (k USD)      226.44   Production loss x product price

### KO-3201 Parameter

#### Nameplate and identification

  ---------------------------------------------------------------------
  Field                              Value
  ---------------------------------- ----------------------------------
  Equipment Tag                      KO-3201 Parameter

  Equipment Name                     Cracked Gas Compressor KO-3201 DE
                                     Radial Vibration (micron)

  Equipment Type                     Centrifugal Compressor Lube Oil
                                     Water Content (ppm)

  Equipment Class                    A Lube Oil Supply Press (barg)

  Plant / Unit                       Cracker Unit (ZCU) Bearing Metal
                                     Temp (°C)

  Discipline                         ROT

  Criticality                        High

  Design Life                        5 years (bearing) / 24 months
                                     (seal element)

  Monitoring Method                  Online DCS + monthly
                                     vibration/thermography route

  Linked RCA / AR No.                AR-2026-ZCU-0142

  Failure Date                       29-Apr-2026

  Dominant Failure Mode              Distress)
  ---------------------------------------------------------------------

#### Monitored parameters and alarm/trip limits

Parameter Alarm / Trip ----------- --------------

#### Weekly condition record

  Week   Date         Health status
  ------ ------------ ---------------
  1      2025-12-10   28.914
  2      2025-12-17   26.899
  3      2025-12-24   29.739
  4      2025-12-31   29.024
  5      2026-01-07   28.658
  6      2026-01-14   30.289
  7      2026-01-21   33.697
  8      2026-01-28   33.93
  9      2026-02-04   35.439
  10     2026-02-11   37.665
  11     2026-02-18   39.586
  12     2026-02-25   41.609
  13     2026-03-04   45.505
  14     2026-03-11   49.237
  15     2026-03-18   51.111
  16     2026-03-25   55.927
  17     2026-04-01   59.123
  18     2026-04-08   60.529
  19     2026-04-15   66.73
  20     2026-04-22   71.674
  21     2026-04-29   76.5
  22     2026-05-06   27.111
  23     2026-05-13   27.704
  24     2026-05-20   26.92
  25     2026-05-27   27.433
  26     2026-06-03   27.234

#### Remarks

-   Degradation trend --- under close monitoring
-   Degradation trend --- under close monitoring
-   Degradation trend --- under close monitoring
-   FAILURE --- High Radial Vibration Trip (Bearing
-   Distress); unplanned downtime 32.0 h
-   Post-repair baseline restored (CAPA executed)

#### Performance summary

  KPI                         Value   Basis / Formula
  --------------------------- ------- ---------------------------------
  Monitoring Period (weeks)   26      Number of weekly readings
  Total Downtime (hours)      32      From linked RCA downtime window
  Period Hours                4368    4368
  Availability (%)            99.3    (Period-Downtime)/Period
  No. of Failures (period)    1       Failure events this period
  MTBF (hours)                4368    Period Hours / No. of Failures
  MTTR (hours)                32      Mean time to repair
  ALARM readings              11      Count of ALARM weeks
  TRIP readings               1       Count of TRIP weeks
  NORMAL readings             14      Count of NORMAL weeks
  PM Compliance (%)           92.0    PM completed vs scheduled
  Production Loss (ton)       1760    Downtime x rate loss (from RCA)
  Estimated Loss (k USD)      1584    Production loss x product price

### PM-4405B Parameter

#### Nameplate and identification

  ---------------------------------------------------------------------
  Field                              Value
  ---------------------------------- ----------------------------------
  Equipment Tag                      PM-4405B Parameter

  Equipment Name                     (Motor Driven)

  Equipment Type                     Centrifugal Pump / Electric Motor
                                     Motor Vibration (mm/s)

  Equipment Class                    B Motor Ampere (A)

  Plant / Unit                       Utility Plant (NUP) Winding Temp
                                     (°C)

  Discipline                         ELE

  Criticality                        Medium

  Design Life                        5 years (bearing) / 24 months
                                     (seal element)

  Monitoring Method                  Online DCS + monthly
                                     vibration/thermography route

  Linked RCA / AR No.                AR-2026-NUP-0089

  Failure Date                       08-Jul-2026

  Dominant Failure Mode              Motor Bearing Failure
                                     (Overheating)
  ---------------------------------------------------------------------

#### Monitored parameters and alarm/trip limits

Parameter Alarm / Trip ----------- --------------

#### Weekly condition record

  Week   Date         Health status
  ------ ------------ ---------------
  1      2026-02-18   63.617
  2      2026-02-25   64.04
  3      2026-03-04   64.006
  4      2026-03-11   64.94
  5      2026-03-18   65.55
  6      2026-03-25   65.645
  7      2026-04-01   66.476
  8      2026-04-08   66.851
  9      2026-04-15   68.559
  10     2026-04-22   69.633
  11     2026-04-29   70.413
  12     2026-05-06   71.385
  13     2026-05-13   73.921
  14     2026-05-20   74.537
  15     2026-05-27   76.498
  16     2026-06-03   78.258
  17     2026-06-10   80.814
  18     2026-06-17   82.788
  19     2026-06-24   84.415
  20     2026-07-01   87.236
  21     2026-07-08   91.8
  22     2026-07-15   63.965
  23     2026-07-22   65.846
  24     2026-07-29   64.984
  25     2026-08-05   65.038
  26     2026-08-12   64.849

#### Remarks

-   Degradation trend --- under close monitoring
-   Degradation trend --- under close monitoring
-   Degradation trend --- under close monitoring
-   FAILURE --- Motor Bearing Failure (Overheating);
-   unplanned downtime 8.0 h
-   Post-repair baseline restored (CAPA executed)

#### Performance summary

  KPI                         Value   Basis / Formula
  --------------------------- ------- ---------------------------------
  Monitoring Period (weeks)   26      Number of weekly readings
  Total Downtime (hours)      8       From linked RCA downtime window
  Period Hours                4368    4368
  Availability (%)            99.8    (Period-Downtime)/Period
  No. of Failures (period)    1       Failure events this period
  MTBF (hours)                4368    Period Hours / No. of Failures
  MTTR (hours)                8       Mean time to repair
  ALARM readings              6       Count of ALARM weeks
  TRIP readings               1       Count of TRIP weeks
  NORMAL readings             19      Count of NORMAL weeks
  PM Compliance (%)           92.0    PM completed vs scheduled
  Production Loss (ton)       160     Downtime x rate loss (from RCA)
  Estimated Loss (k USD)      112     Production loss x product price

### HE-3301 Parameter

#### Nameplate and identification

  ---------------------------------------------------------------------
  Field                              Value
  ---------------------------------- ----------------------------------
  Equipment Tag                      HE-3301 Parameter

  Equipment Name                     HE-3301

  Equipment Type                     Shell & Tube Heat Exchanger Heat
                                     Duty (% design)

  Equipment Class                    B Cold Outlet Temp (°C)

  Plant / Unit                       Cracker Unit (ZCU) Feed Heavy-ends
                                     (%)

  Discipline                         STA

  Criticality                        Medium

  Design Life                        5 years (bearing) / 24 months
                                     (seal element)

  Monitoring Method                  Online DCS + monthly
                                     vibration/thermography route

  Linked RCA / AR No.                AR-2026-ZCU-0165

  Failure Date                       21-May-2026

  Dominant Failure Mode              NG RECORD
  ---------------------------------------------------------------------

#### Monitored parameters and alarm/trip limits

Parameter Alarm / Trip ----------- --------------

#### Weekly condition record

  Week   Date         Health status
  ------ ------------ ---------------
  1      2026-01-01   0.355
  2      2026-01-08   0.355
  3      2026-01-15   0.347
  4      2026-01-22   0.337
  5      2026-01-29   0.37
  6      2026-02-05   0.377
  7      2026-02-12   0.399
  8      2026-02-19   0.421
  9      2026-02-26   0.458
  10     2026-03-05   0.455
  11     2026-03-12   0.496
  12     2026-03-19   0.517
  13     2026-03-26   0.54
  14     2026-04-02   0.57
  15     2026-04-09   0.602
  16     2026-04-16   0.635
  17     2026-04-23   0.705
  18     2026-04-30   0.751
  19     2026-05-07   0.785
  20     2026-05-14   0.854
  21     2026-05-21   0.918
  22     2026-05-28   0.337
  23     2026-06-04   0.316
  24     2026-06-11   0.319
  25     2026-06-18   0.358
  26     2026-06-25   0.352

#### Remarks

-   Degradation trend --- under close monitoring
-   Degradation trend --- under close monitoring
-   Degradation trend --- under close monitoring
-   FAILURE --- High Fouling --- Duty Loss & High dP;
-   unplanned downtime 12.0 h
-   Post-repair baseline restored (CAPA executed)

#### Performance summary

  KPI                         Value   Basis / Formula
  --------------------------- ------- ---------------------------------
  Monitoring Period (weeks)   26      Number of weekly readings
  Total Downtime (hours)      12      From linked RCA downtime window
  Period Hours                4368    4368
  Availability (%)            99.7    (Period-Downtime)/Period
  No. of Failures (period)    1       Failure events this period
  MTBF (hours)                4368    Period Hours / No. of Failures
  MTTR (hours)                12      Mean time to repair
  ALARM readings              10      Count of ALARM weeks
  TRIP readings               1       Count of TRIP weeks
  NORMAL readings             15      Count of NORMAL weeks
  PM Compliance (%)           92.0    PM completed vs scheduled
  Production Loss (ton)       216     Downtime x rate loss (from RCA)
  Estimated Loss (k USD)      183.6   Production loss x product price

### BL-5702 Parameter

#### Nameplate and identification

  ---------------------------------------------------------------------
  Field                              Value
  ---------------------------------- ----------------------------------
  Equipment Tag                      BL-5702 Parameter

  Equipment Name                     Product Blower BL-5702 Overall
                                     Vibration (mm/s)

  Equipment Type                     Centrifugal Blower 2X Harmonic
                                     (mm/s)

  Equipment Class                    A Coupling Offset (mm)

  Plant / Unit                       Polymer Plant (OPP) Bearing Temp
                                     (°C)

  Discipline                         ROT

  Criticality                        High

  Design Life                        5 years (bearing) / 24 months
                                     (seal element)

  Monitoring Method                  Online DCS + monthly
                                     vibration/thermography route

  Linked RCA / AR No.                AR-2026-OPP-0203

  Failure Date                       17-Jun-2026

  Dominant Failure Mode              Misalignment)
  ---------------------------------------------------------------------

#### Monitored parameters and alarm/trip limits

Parameter Alarm / Trip ----------- --------------

#### Weekly condition record

  Week   Date         Health status
  ------ ------------ ---------------
  1      2026-01-28   4.004
  2      2026-02-04   4.188
  3      2026-02-11   4.091
  4      2026-02-18   4.265
  5      2026-02-25   4.268
  6      2026-03-04   4.435
  7      2026-03-11   4.443
  8      2026-03-18   4.892
  9      2026-03-25   4.581
  10     2026-04-01   5.295
  11     2026-04-08   5.636
  12     2026-04-15   6.003
  13     2026-04-22   6.667
  14     2026-04-29   6.786
  15     2026-05-06   7.425
  16     2026-05-13   7.976
  17     2026-05-20   8.582
  18     2026-05-27   9.12
  19     2026-06-03   9.711
  20     2026-06-10   10.376
  21     2026-06-17   11.22
  22     2026-06-24   3.782
  23     2026-07-01   3.76
  24     2026-07-08   3.918
  25     2026-07-15   3.926
  26     2026-07-22   4.001

#### Remarks

-   Degradation trend --- under close monitoring
-   Degradation trend --- under close monitoring
-   Degradation trend --- under close monitoring
-   FAILURE --- High Vibration (Coupling
-   Misalignment); unplanned downtime 14.0 h
-   Post-repair baseline restored (CAPA executed)

#### Performance summary

  KPI                         Value   Basis / Formula
  --------------------------- ------- ---------------------------------
  Monitoring Period (weeks)   26      Number of weekly readings
  Total Downtime (hours)      14      From linked RCA downtime window
  Period Hours                4368    4368
  Availability (%)            99.7    (Period-Downtime)/Period
  No. of Failures (period)    1       Failure events this period
  MTBF (hours)                4368    Period Hours / No. of Failures
  MTTR (hours)                14      Mean time to repair
  ALARM readings              15      Count of ALARM weeks
  TRIP readings               1       Count of TRIP weeks
  NORMAL readings             10      Count of NORMAL weeks
  PM Compliance (%)           92.0    PM completed vs scheduled
  Production Loss (ton)       532     Downtime x rate loss (from RCA)
  Estimated Loss (k USD)      478.8   Production loss x product price

## 5. Incident register

The incident register contains 380 rows. It is reproduced as a
normalized Markdown table.

  Serial No.   MTO No.             AR No.             Plant   Tag Number   Equipment Class
  ------------ ------------------- ------------------ ------- ------------ -----------------
  1            MTO-2026-ARP-0031   AR-2026-ARP-0117   ARP     PU-2101B     B
  2            MTO-2026-ZCU-0058   AR-2026-ZCU-0142   ZCU     KO-3201      A
  3            MTO-2026-NUP-0024   AR-2026-NUP-0089   NUP     PM-4405B     B
  4            MTO-2026-ZCU-0071   AR-2026-ZCU-0165   ZCU     HE-3301      B
  5            MTO-2026-OPP-0096   AR-2026-OPP-0203   OPP     BL-5702      A
  6            MTO-2024-OPP-0006   n/a                OPP     TR-8242A     B
  7            MTO-2025-ARP-0007   AR-2025-ARP-0020   ARP     CV-7690      A
  8            MTO-2024-ZCU-0008   AR-2024-ZCU-0130   ZCU     PZ-2154      A
  9            MTO-2026-SMX-0009   n/a                SMX     SW-5620C     A
  10           MTO-2025-ARP-0010   n/a                ARP     PM-6523C     B
  11           MTO-2025-SMX-0011   AR-2025-SMX-0125   SMX     SW-3411B     A
  12           MTO-2025-SMX-0012   n/a                SMX     RX-6438      B
  13           MTO-2025-CRP-0013   n/a                CRP     CV-8399C     A
  14           MTO-2025-NUP-0014   n/a                NUP     FN-7159      B
  15           MTO-2024-SMX-0015   AR-2024-SMX-0039   SMX     TX-8176      A
  16           MTO-2025-NUP-0016   AR-2025-NUP-0234   NUP     PU-8272      A
  17           MTO-2024-SMX-0017   n/a                SMX     TX-5843      A
  18           MTO-2025-SMX-0018   AR-2025-SMX-0109   SMX     SW-4963      A
  19           MTO-2025-OP2-0019   AR-2025-OP2-0135   OP2     PM-3818A     A
  20           MTO-2026-SMX-0020   n/a                SMX     PU-2895      B
  21           MTO-2024-BRP-0021   AR-2024-BRP-0112   BRP     TX-6085B     A
  22           MTO-2024-OP3-0022   n/a                OP3     TK-5150B     A
  23           MTO-2024-OP2-0023   AR-2024-OP2-0156   OP2     PU-1188B     A
  24           MTO-2025-OP2-0024   n/a                OP2     PM-8055      B
  25           MTO-2024-OP3-0025   AR-2024-OP3-0032   OP3     PU-7290C     A
  26           MTO-2024-ZCU-0026   n/a                ZCU     PZ-4479      A
  27           MTO-2025-SMX-0027   AR-2025-SMX-0167   SMX     PM-1191      A
  28           MTO-2026-OPU-0028   n/a                OPU     PZ-6185      B
  29           MTO-2026-BDX-0029   AR-2026-BDX-0161   BDX     PM-5600B     A
  30           MTO-2024-SMX-0030   n/a                SMX     PM-6753C     B
  31           MTO-2025-ARP-0031   n/a                ARP     TR-5690      B
  32           MTO-2024-OPP-0032   n/a                OPP     TK-8363B     A
  33           MTO-2025-OPP-0033   AR-2025-OPP-0078   OPP     TK-1241A     A
  34           MTO-2025-ARP-0034   AR-2025-ARP-0213   ARP     TX-3672C     A
  35           MTO-2025-CRP-0035   n/a                CRP     SW-1565      B
  36           MTO-2026-BDX-0036   AR-2026-BDX-0040   BDX     RX-3569A     A
  37           MTO-2025-NUP-0037   n/a                NUP     TK-3192B     B
  38           MTO-2024-TKX-0038   AR-2024-TKX-0174   TKX     CV-3404      A
  39           MTO-2026-OP3-0039   AR-2026-OP3-0200   OP3     TX-3884B     A
  40           MTO-2026-BDX-0040   n/a                BDX     PU-6212      B
  41           MTO-2025-ZCU-0041   n/a                ZCU     HE-2276B     C
  42           MTO-2025-SMX-0042   n/a                SMX     TX-1231B     B
  43           MTO-2025-SMX-0043   AR-2025-SMX-0056   SMX     PZ-1300C     A
  44           MTO-2025-ZCU-0044   n/a                ZCU     CV-6587      B
  45           MTO-2024-OP3-0045   n/a                OP3     PU-8073A     B
  46           MTO-2025-SMX-0046   AR-2025-SMX-0040   SMX     TX-7355C     A
  47           MTO-2024-ZCU-0047   n/a                ZCU     HE-3296B     B
  48           MTO-2025-ARP-0048   AR-2025-ARP-0121   ARP     RX-8843      A
  49           MTO-2024-ZCU-0049   n/a                ZCU     PZ-7199      A
  50           MTO-2024-OP2-0050   n/a                OP2     AZ-4763B     B
  51           MTO-2024-NUP-0051   n/a                NUP     PU-6855      B
  52           MTO-2025-BDX-0052   n/a                BDX     PZ-7054B     A
  53           MTO-2025-ARP-0053   n/a                ARP     BL-6185      A
  54           MTO-2026-OPP-0054   n/a                OPP     FN-1575      B
  55           MTO-2024-ARP-0055   AR-2024-ARP-0247   ARP     PU-4209      A
  56           MTO-2026-BDX-0056   n/a                BDX     CD-2982B     B
  57           MTO-2025-ARP-0057   AR-2025-ARP-0134   ARP     BL-4126C     A
  58           MTO-2024-OPP-0058   n/a                OPP     CV-5933      A
  59           MTO-2025-TKX-0059   n/a                TKX     PU-7158A     A
  60           MTO-2025-ZCU-0060   n/a                ZCU     CV-8863C     B
  61           MTO-2024-ARP-0061   AR-2024-ARP-0101   ARP     TX-4861B     A
  62           MTO-2024-ARP-0062   n/a                ARP     BL-1732C     B
  63           MTO-2025-OP3-0063   n/a                OP3     CV-1608A     C
  64           MTO-2025-NUP-0064   n/a                NUP     FN-2136      B
  65           MTO-2025-ZCU-0065   n/a                ZCU     PU-8189A     B
  66           MTO-2024-BDX-0066   n/a                BDX     BL-1795A     B
  67           MTO-2025-OPP-0067   AR-2025-OPP-0099   OPP     PM-4639      A
  68           MTO-2025-NUP-0068   n/a                NUP     CD-4653      A
  69           MTO-2024-OP3-0069   n/a                OP3     RX-8107B     A
  70           MTO-2025-OP3-0070   AR-2025-OP3-0128   OP3     BL-2438      A
  71           MTO-2025-ZCU-0071   n/a                ZCU     PU-5209B     A
  72           MTO-2024-CRP-0072   AR-2024-CRP-0222   CRP     BL-2806      A
  73           MTO-2026-CRP-0073   AR-2026-CRP-0102   CRP     KO-2432C     A
  74           MTO-2025-BRP-0074   n/a                BRP     CV-2925B     A
  75           MTO-2026-NUP-0075   n/a                NUP     SW-2483      A
  76           MTO-2024-ZCU-0076   AR-2024-ZCU-0109   ZCU     RX-4619C     A
  77           MTO-2024-OPU-0077   n/a                OPU     KO-5967B     A
  78           MTO-2024-OPP-0078   n/a                OPP     TR-2916      A
  79           MTO-2025-OPU-0079   n/a                OPU     RX-3931      A
  80           MTO-2026-BDX-0080   AR-2026-BDX-0146   BDX     PZ-6299C     A
  81           MTO-2025-OPP-0081   n/a                OPP     RX-7490B     B
  82           MTO-2026-OPP-0082   AR-2026-OPP-0163   OPP     PM-1018A     A
  83           MTO-2024-OPP-0083   n/a                OPP     BL-1954      B
  84           MTO-2026-BRP-0084   AR-2026-BRP-0117   BRP     PM-8555B     A
  85           MTO-2025-CRP-0085   n/a                CRP     TX-3354      B
  86           MTO-2024-ZCU-0086   AR-2024-ZCU-0078   ZCU     BL-1631B     A
  87           MTO-2025-ZCU-0087   n/a                ZCU     TX-5573B     B
  88           MTO-2025-ARP-0088   AR-2025-ARP-0236   ARP     CD-1529      A
  89           MTO-2024-BDX-0089   n/a                BDX     BL-8286      A
  90           MTO-2025-BDX-0090   n/a                BDX     PU-7196C     A
  91           MTO-2024-ARP-0091   n/a                ARP     SW-5428      A
  92           MTO-2024-SMX-0092   n/a                SMX     TX-3821C     A
  93           MTO-2024-OP3-0093   AR-2024-OP3-0090   OP3     CD-3164      A
  94           MTO-2025-BDX-0094   AR-2025-BDX-0218   BDX     PM-6744      A
  95           MTO-2025-CRP-0095   n/a                CRP     AZ-7326B     C
  96           MTO-2026-OPP-0096   n/a                OPP     KO-6912A     B
  97           MTO-2026-CRP-0097   AR-2026-CRP-0015   CRP     HE-7828C     A
  98           MTO-2026-ZCU-0098   n/a                ZCU     TR-8775A     A
  99           MTO-2026-OP3-0099   AR-2026-OP3-0227   OP3     TK-7586B     A
  100          MTO-2026-ZCU-0100   AR-2026-ZCU-0052   ZCU     KO-1172C     A
  101          MTO-2024-ZCU-0101   n/a                ZCU     TX-3554      C
  102          MTO-2026-ZCU-0102   n/a                ZCU     BL-3912      A
  103          MTO-2024-OPU-0103   n/a                OPU     BL-7186C     C
  104          MTO-2026-ZCU-0104   n/a                ZCU     PM-4607      A
  105          MTO-2025-OP3-0105   n/a                OP3     TX-5871      A
  106          MTO-2025-OP2-0106   n/a                OP2     PU-7657      B
  107          MTO-2024-SMX-0107   n/a                SMX     BL-8930A     B
  108          MTO-2024-SMX-0108   n/a                SMX     PM-4728A     A
  109          MTO-2026-TKX-0109   AR-2026-TKX-0226   TKX     TX-6768B     A
  110          MTO-2026-BRP-0110   n/a                BRP     HE-1493      A
  111          MTO-2024-CRP-0111   n/a                CRP     TX-3809A     A
  112          MTO-2025-OP3-0112   AR-2025-OP3-0140   OP3     TK-6638      A
  113          MTO-2026-OP3-0113   AR-2026-OP3-0014   OP3     PM-3131A     A
  114          MTO-2026-OP3-0114   n/a                OP3     RX-8190C     C
  115          MTO-2025-OPP-0115   n/a                OPP     PZ-5870      B
  116          MTO-2024-ARP-0116   n/a                ARP     PU-7899A     A
  117          MTO-2024-BRP-0117   n/a                BRP     PM-5170C     B
  118          MTO-2026-NUP-0118   n/a                NUP     TR-2677C     B
  119          MTO-2024-CRP-0119   n/a                CRP     PZ-6565A     A
  120          MTO-2025-OP2-0120   AR-2025-OP2-0106   OP2     TX-1722A     A
  121          MTO-2024-OP2-0121   n/a                OP2     TK-5168C     B
  122          MTO-2025-OPP-0122   n/a                OPP     FN-7608      B
  123          MTO-2025-OPP-0123   n/a                OPP     AZ-1653C     B
  124          MTO-2025-OP2-0124   n/a                OP2     HE-6128      B
  125          MTO-2024-ZCU-0125   n/a                ZCU     RX-6481      A
  126          MTO-2025-ARP-0126   n/a                ARP     PZ-2526C     A
  127          MTO-2024-OP2-0127   n/a                OP2     CD-2356A     A
  128          MTO-2024-OP2-0128   n/a                OP2     RX-2091B     B
  129          MTO-2026-OP2-0129   AR-2026-OP2-0171   OP2     BL-2287A     A
  130          MTO-2024-BDX-0130   AR-2024-BDX-0076   BDX     CD-6044A     A
  131          MTO-2024-OP2-0131   n/a                OP2     RX-3576      C
  132          MTO-2025-OPU-0132   AR-2025-OPU-0206   OPU     TR-3696      A
  133          MTO-2024-ZCU-0133   AR-2024-ZCU-0236   ZCU     RX-3112      A
  134          MTO-2024-ZCU-0134   n/a                ZCU     PZ-8690B     A
  135          MTO-2025-ZCU-0135   AR-2025-ZCU-0212   ZCU     TX-3876B     A
  136          MTO-2026-NUP-0136   n/a                NUP     FN-3044      B
  137          MTO-2025-OPP-0137   n/a                OPP     SW-3674B     A
  138          MTO-2025-SMX-0138   n/a                SMX     BL-7185B     A
  139          MTO-2024-ZCU-0139   n/a                ZCU     PU-4041C     B
  140          MTO-2025-OP3-0140   AR-2025-OP3-0228   OP3     TK-1610C     A
  141          MTO-2025-BRP-0141   n/a                BRP     HE-1090B     B
  142          MTO-2024-ZCU-0142   n/a                ZCU     SW-6198B     A
  143          MTO-2026-OP2-0143   AR-2026-OP2-0038   OP2     HE-8579B     A
  144          MTO-2024-SMX-0144   n/a                SMX     PM-6481B     B
  145          MTO-2025-SMX-0145   AR-2025-SMX-0231   SMX     RX-5203C     A
  146          MTO-2025-OPP-0146   n/a                OPP     AZ-1094B     A
  147          MTO-2025-BRP-0147   AR-2025-BRP-0230   BRP     AZ-3776A     A
  148          MTO-2024-OP2-0148   AR-2024-OP2-0136   OP2     KO-1107      A
  149          MTO-2024-SMX-0149   n/a                SMX     PZ-3888C     A
  150          MTO-2024-ARP-0150   n/a                ARP     BL-3575      C
  151          MTO-2025-OP2-0151   n/a                OP2     BL-4956      A
  152          MTO-2026-BDX-0152   AR-2026-BDX-0134   BDX     SW-1941A     A
  153          MTO-2024-OPP-0153   n/a                OPP     PM-8835B     B
  154          MTO-2025-OPP-0154   AR-2025-OPP-0185   OPP     PZ-3313B     A
  155          MTO-2024-BRP-0155   AR-2024-BRP-0121   BRP     PU-7733C     A
  156          MTO-2024-TKX-0156   AR-2024-TKX-0211   TKX     FN-3899      A
  157          MTO-2024-CRP-0157   n/a                CRP     SW-6750A     A
  158          MTO-2024-BRP-0158   AR-2024-BRP-0158   BRP     FN-2402A     A
  159          MTO-2024-ARP-0159   AR-2024-ARP-0240   ARP     PZ-8155B     A
  160          MTO-2026-OPP-0160   AR-2026-OPP-0064   OPP     TX-8349      A
  161          MTO-2025-ARP-0161   n/a                ARP     TR-3587C     A
  162          MTO-2025-ZCU-0162   n/a                ZCU     FN-7628A     B
  163          MTO-2025-ZCU-0163   n/a                ZCU     BL-4656C     A
  164          MTO-2026-ZCU-0164   n/a                ZCU     PU-6682      A
  165          MTO-2024-BDX-0165   n/a                BDX     TX-4966C     A
  166          MTO-2024-SMX-0166   n/a                SMX     TX-2796A     A
  167          MTO-2024-ZCU-0167   n/a                ZCU     AZ-3493B     B
  168          MTO-2025-OP2-0168   AR-2025-OP2-0118   OP2     PM-2566C     A
  169          MTO-2024-OPP-0169   n/a                OPP     BL-2784A     A
  170          MTO-2024-OPP-0170   n/a                OPP     PU-7794      B
  171          MTO-2025-NUP-0171   n/a                NUP     HE-2776A     A
  172          MTO-2024-OP2-0172   n/a                OP2     AZ-1735A     B
  173          MTO-2025-OPP-0173   AR-2025-OPP-0169   OPP     AZ-1424      A
  174          MTO-2025-OP2-0174   AR-2025-OP2-0072   OP2     AZ-8765C     A
  175          MTO-2024-BRP-0175   AR-2024-BRP-0200   BRP     AZ-6656C     A
  176          MTO-2024-BRP-0176   AR-2024-BRP-0245   BRP     HE-7629      A
  177          MTO-2024-ARP-0177   n/a                ARP     CV-4573A     A
  178          MTO-2026-ZCU-0178   n/a                ZCU     PM-3070      B
  179          MTO-2025-ARP-0179   n/a                ARP     HE-5523      B
  180          MTO-2025-OPP-0180   AR-2025-OPP-0142   OPP     TX-8678      A
  181          MTO-2024-CRP-0181   n/a                CRP     PU-8356      A
  182          MTO-2024-BDX-0182   n/a                BDX     PU-2931B     B
  183          MTO-2026-OP3-0183   n/a                OP3     AZ-4698B     A
  184          MTO-2024-ZCU-0184   n/a                ZCU     PM-4526B     B
  185          MTO-2026-OPU-0185   AR-2026-OPU-0114   OPU     TK-6644B     A
  186          MTO-2026-CRP-0186   n/a                CRP     PU-1676A     B
  187          MTO-2025-BRP-0187   n/a                BRP     TK-2079B     C
  188          MTO-2024-ZCU-0188   AR-2024-ZCU-0236   ZCU     SW-3050      A
  189          MTO-2024-NUP-0189   AR-2024-NUP-0248   NUP     TR-6283A     A
  190          MTO-2024-ARP-0190   AR-2024-ARP-0027   ARP     FN-3328B     A
  191          MTO-2024-OPU-0191   n/a                OPU     TX-4689      B
  192          MTO-2025-ARP-0192   n/a                ARP     TX-7313      B
  193          MTO-2025-ARP-0193   n/a                ARP     PM-7974A     B
  194          MTO-2026-ARP-0194   n/a                ARP     PM-1440      B
  195          MTO-2024-BRP-0195   AR-2024-BRP-0223   BRP     CV-5846      A
  196          MTO-2024-CRP-0196   AR-2024-CRP-0016   CRP     CD-1513      A
  197          MTO-2024-ARP-0197   n/a                ARP     FN-2268      B
  198          MTO-2025-CRP-0198   AR-2025-CRP-0058   CRP     KO-4139B     A
  199          MTO-2024-SMX-0199   AR-2024-SMX-0120   SMX     TX-6875      A
  200          MTO-2024-ZCU-0200   n/a                ZCU     CD-8154      A
  201          MTO-2024-OP3-0201   n/a                OP3     RX-7012B     A
  202          MTO-2024-ARP-0202   n/a                ARP     TX-6162B     B
  203          MTO-2024-BDX-0203   n/a                BDX     PU-7701C     C
  204          MTO-2026-NUP-0204   AR-2026-NUP-0071   NUP     KO-4022B     A
  205          MTO-2025-ZCU-0205   n/a                ZCU     HE-5734C     A
  206          MTO-2024-SMX-0206   n/a                SMX     BL-7977      A
  207          MTO-2024-OP3-0207   AR-2024-OP3-0182   OP3     RX-1896A     A
  208          MTO-2024-OP2-0208   AR-2024-OP2-0122   OP2     TR-1447A     A
  209          MTO-2025-OPP-0209   n/a                OPP     TX-7941A     B
  210          MTO-2025-OP2-0210   n/a                OP2     PM-2733C     B
  211          MTO-2025-SMX-0211   AR-2025-SMX-0136   SMX     SW-3110      A
  212          MTO-2024-BRP-0212   n/a                BRP     TX-2151C     A
  213          MTO-2025-SMX-0213   n/a                SMX     KO-8443C     C
  214          MTO-2026-OP3-0214   n/a                OP3     CD-4129B     C
  215          MTO-2025-ARP-0215   AR-2025-ARP-0117   ARP     TX-4180      A
  216          MTO-2024-OPP-0216   AR-2024-OPP-0080   OPP     CD-7424A     A
  217          MTO-2024-OP2-0217   AR-2024-OP2-0240   OP2     CD-4525B     A
  218          MTO-2025-OP3-0218   n/a                OP3     BL-7358      A
  219          MTO-2024-ZCU-0219   AR-2024-ZCU-0242   ZCU     PZ-1094      A
  220          MTO-2026-ZCU-0220   n/a                ZCU     PZ-4712      B
  221          MTO-2024-OPP-0221   AR-2024-OPP-0040   OPP     PM-3484B     A
  222          MTO-2024-ARP-0222   n/a                ARP     BL-4995      A
  223          MTO-2025-OP3-0223   n/a                OP3     PZ-4078B     A
  224          MTO-2026-SMX-0224   AR-2026-SMX-0092   SMX     TR-5785      A
  225          MTO-2025-OPP-0225   n/a                OPP     SW-5472B     B
  226          MTO-2024-SMX-0226   n/a                SMX     RX-3213C     A
  227          MTO-2026-OPP-0227   n/a                OPP     TR-7081      C
  228          MTO-2025-BRP-0228   AR-2025-BRP-0122   BRP     BL-4356      A
  229          MTO-2024-BDX-0229   n/a                BDX     KO-8623      B
  230          MTO-2026-SMX-0230   n/a                SMX     PM-3251      A
  231          MTO-2024-BRP-0231   n/a                BRP     PU-7906      B
  232          MTO-2025-OP3-0232   AR-2025-OP3-0136   OP3     CV-5846      A
  233          MTO-2025-OP3-0233   AR-2025-OP3-0024   OP3     KO-8837B     A
  234          MTO-2025-SMX-0234   AR-2025-SMX-0129   SMX     CD-4479B     A
  235          MTO-2026-ZCU-0235   n/a                ZCU     CD-3123      B
  236          MTO-2025-ARP-0236   n/a                ARP     TX-3574C     A
  237          MTO-2024-ZCU-0237   AR-2024-ZCU-0213   ZCU     TR-6290      A
  238          MTO-2025-ARP-0238   AR-2025-ARP-0129   ARP     TK-6178A     A
  239          MTO-2024-ARP-0239   AR-2024-ARP-0049   ARP     SW-5535      A
  240          MTO-2024-BRP-0240   n/a                BRP     CD-6577B     A
  241          MTO-2026-ZCU-0241   AR-2026-ZCU-0133   ZCU     HE-3559B     A
  242          MTO-2025-OP2-0242   n/a                OP2     RX-3162      B
  243          MTO-2025-SMX-0243   n/a                SMX     PU-7148      B
  244          MTO-2026-OP2-0244   n/a                OP2     KO-1825      A
  245          MTO-2024-SMX-0245   n/a                SMX     AZ-2808      B
  246          MTO-2024-OP2-0246   AR-2024-OP2-0164   OP2     TX-1039B     A
  247          MTO-2026-ZCU-0247   n/a                ZCU     RX-2949A     B
  248          MTO-2025-NUP-0248   n/a                NUP     PM-7516C     B
  249          MTO-2025-OPP-0249   AR-2025-OPP-0032   OPP     CD-5066A     A
  250          MTO-2024-NUP-0250   n/a                NUP     TX-7293      B
  251          MTO-2026-TKX-0251   n/a                TKX     KO-3418A     B
  252          MTO-2025-CRP-0252   n/a                CRP     HE-2011      A
  253          MTO-2026-NUP-0253   AR-2026-NUP-0080   NUP     RX-5939B     A
  254          MTO-2025-ARP-0254   n/a                ARP     FN-8551C     A
  255          MTO-2025-TKX-0255   n/a                TKX     PU-2304A     B
  256          MTO-2025-ARP-0256   AR-2025-ARP-0130   ARP     TR-8066      A
  257          MTO-2024-ARP-0257   n/a                ARP     RX-1575      B
  258          MTO-2024-NUP-0258   n/a                NUP     HE-1535      C
  259          MTO-2026-OPP-0259   n/a                OPP     PM-2842A     A
  260          MTO-2026-TKX-0260   n/a                TKX     PM-7677      A
  261          MTO-2024-CRP-0261   AR-2024-CRP-0231   CRP     PM-6340A     A
  262          MTO-2025-BDX-0262   n/a                BDX     RX-8147A     A
  263          MTO-2024-OP3-0263   AR-2024-OP3-0129   OP3     AZ-8666      A
  264          MTO-2025-BRP-0264   n/a                BRP     TX-1531      B
  265          MTO-2025-OP3-0265   n/a                OP3     TR-3550      B
  266          MTO-2026-ZCU-0266   n/a                ZCU     PZ-2759      A
  267          MTO-2024-OP2-0267   AR-2024-OP2-0209   OP2     CD-7937A     A
  268          MTO-2026-NUP-0268   AR-2026-NUP-0239   NUP     BL-3946C     A
  269          MTO-2025-ARP-0269   AR-2025-ARP-0048   ARP     SW-6175C     A
  270          MTO-2025-SMX-0270   n/a                SMX     PM-1316B     A
  271          MTO-2026-NUP-0271   AR-2026-NUP-0161   NUP     CV-3290      A
  272          MTO-2024-ZCU-0272   n/a                ZCU     PZ-7507      B
  273          MTO-2026-OPP-0273   n/a                OPP     TX-1468      A
  274          MTO-2024-BRP-0274   n/a                BRP     PZ-6564      B
  275          MTO-2024-OP2-0275   AR-2024-OP2-0090   OP2     AZ-3288      A
  276          MTO-2024-BRP-0276   AR-2024-BRP-0227   BRP     CD-2449C     A
  277          MTO-2024-ZCU-0277   AR-2024-ZCU-0059   ZCU     TK-1215      A
  278          MTO-2024-ZCU-0278   n/a                ZCU     CD-6611      B
  279          MTO-2024-OP2-0279   n/a                OP2     TR-3408C     B
  280          MTO-2026-ZCU-0280   n/a                ZCU     SW-8737A     B
  281          MTO-2025-SMX-0281   AR-2025-SMX-0022   SMX     TX-3699      A
  282          MTO-2024-OP3-0282   n/a                OP3     TX-6148B     A
  283          MTO-2025-ZCU-0283   AR-2025-ZCU-0035   ZCU     BL-2513A     A
  284          MTO-2026-SMX-0284   n/a                SMX     AZ-1128C     A
  285          MTO-2024-ARP-0285   AR-2024-ARP-0131   ARP     TX-2223      A
  286          MTO-2026-OPP-0286   AR-2026-OPP-0209   OPP     HE-4966C     A
  287          MTO-2025-OP2-0287   n/a                OP2     TX-4451      B
  288          MTO-2024-ZCU-0288   n/a                ZCU     CD-7117C     B
  289          MTO-2024-OPP-0289   n/a                OPP     PU-5056C     B
  290          MTO-2025-CRP-0290   AR-2025-CRP-0047   CRP     PM-6780      A
  291          MTO-2024-NUP-0291   n/a                NUP     HE-2598B     A
  292          MTO-2025-OPU-0292   AR-2025-OPU-0249   OPU     PU-4574B     A
  293          MTO-2025-ARP-0293   n/a                ARP     KO-7770A     B
  294          MTO-2024-ARP-0294   n/a                ARP     BL-4453C     B
  295          MTO-2024-ZCU-0295   n/a                ZCU     BL-8124A     B
  296          MTO-2025-OPP-0296   n/a                OPP     KO-5432C     C
  297          MTO-2025-SMX-0297   AR-2025-SMX-0164   SMX     TX-5187B     A
  298          MTO-2024-ARP-0298   n/a                ARP     TK-1061C     B
  299          MTO-2026-SMX-0299   AR-2026-SMX-0082   SMX     KO-2904      A
  300          MTO-2025-ZCU-0300   n/a                ZCU     TX-6415B     A
  301          MTO-2025-SMX-0301   AR-2025-SMX-0229   SMX     AZ-4525A     A
  302          MTO-2025-ZCU-0302   n/a                ZCU     KO-4538B     A
  303          MTO-2025-CRP-0303   n/a                CRP     TX-3146      B
  304          MTO-2025-ARP-0304   n/a                ARP     BL-7719      C
  305          MTO-2024-OP2-0305   n/a                OP2     CV-6240      B
  306          MTO-2026-SMX-0306   AR-2026-SMX-0113   SMX     CD-6973      A
  307          MTO-2025-BRP-0307   n/a                BRP     PZ-6982A     A
  308          MTO-2026-SMX-0308   n/a                SMX     SW-5057      B
  309          MTO-2025-ZCU-0309   AR-2025-ZCU-0152   ZCU     PM-4339B     A
  310          MTO-2024-ZCU-0310   n/a                ZCU     TX-6419A     B
  311          MTO-2025-ARP-0311   n/a                ARP     CV-2117A     B
  312          MTO-2025-ZCU-0312   n/a                ZCU     FN-5984      A
  313          MTO-2024-CRP-0313   n/a                CRP     CD-4841      A
  314          MTO-2024-OP3-0314   n/a                OP3     TX-2023C     B
  315          MTO-2025-BRP-0315   n/a                BRP     PZ-5007      B
  316          MTO-2024-ARP-0316   n/a                ARP     AZ-4021      B
  317          MTO-2025-OPP-0317   n/a                OPP     RX-2530      B
  318          MTO-2025-ZCU-0318   n/a                ZCU     SW-8132A     A
  319          MTO-2024-OP3-0319   n/a                OP3     HE-7991      A
  320          MTO-2025-OP2-0320   n/a                OP2     AZ-6357      C
  321          MTO-2024-OPP-0321   n/a                OPP     TX-3092C     B
  322          MTO-2025-OP2-0322   n/a                OP2     PU-6149      C
  323          MTO-2024-ARP-0323   AR-2024-ARP-0089   ARP     PZ-2579B     A
  324          MTO-2025-CRP-0324   n/a                CRP     PM-7696      B
  325          MTO-2024-OPP-0325   n/a                OPP     PM-3134C     B
  326          MTO-2025-NUP-0326   AR-2025-NUP-0091   NUP     PM-4861B     A
  327          MTO-2025-ZCU-0327   AR-2025-ZCU-0183   ZCU     CD-5263B     A
  328          MTO-2025-ZCU-0328   AR-2025-ZCU-0077   ZCU     AZ-2053C     A
  329          MTO-2026-OP3-0329   AR-2026-OP3-0163   OP3     KO-6941B     A
  330          MTO-2025-OPU-0330   n/a                OPU     FN-8723B     B
  331          MTO-2026-OP2-0331   AR-2026-OP2-0171   OP2     HE-4689A     A
  332          MTO-2024-CRP-0332   AR-2024-CRP-0193   CRP     KO-7907      A
  333          MTO-2024-OPP-0333   n/a                OPP     TR-4857B     A
  334          MTO-2025-OP2-0334   AR-2025-OP2-0209   OP2     HE-5877C     A
  335          MTO-2026-ZCU-0335   AR-2026-ZCU-0095   ZCU     TK-2175C     A
  336          MTO-2025-NUP-0336   n/a                NUP     SW-5367      A
  337          MTO-2026-OP2-0337   AR-2026-OP2-0174   OP2     KO-6690C     A
  338          MTO-2026-OP3-0338   AR-2026-OP3-0237   OP3     PM-1108B     A
  339          MTO-2024-OP3-0339   AR-2024-OP3-0219   OP3     SW-2768C     A
  340          MTO-2024-OPU-0340   n/a                OPU     TK-7349      B
  341          MTO-2024-ARP-0341   n/a                ARP     AZ-6778A     A
  342          MTO-2025-ARP-0342   n/a                ARP     BL-6590      B
  343          MTO-2025-ARP-0343   AR-2025-ARP-0199   ARP     FN-8488C     A
  344          MTO-2026-NUP-0344   n/a                NUP     PU-4158C     B
  345          MTO-2024-CRP-0345   n/a                CRP     TX-1131      A
  346          MTO-2026-SMX-0346   AR-2026-SMX-0087   SMX     PU-8439A     A
  347          MTO-2024-BRP-0347   n/a                BRP     CD-5189C     B
  348          MTO-2024-CRP-0348   n/a                CRP     KO-1744      B
  349          MTO-2026-CRP-0349   n/a                CRP     TR-6629      B
  350          MTO-2026-SMX-0350   AR-2026-SMX-0033   SMX     TX-4166C     A
  351          MTO-2024-ZCU-0351   n/a                ZCU     PM-2050      B
  352          MTO-2026-BRP-0352   AR-2026-BRP-0164   BRP     FN-6098A     A
  353          MTO-2024-BDX-0353   AR-2024-BDX-0061   BDX     KO-7855B     A
  354          MTO-2026-OPP-0354   n/a                OPP     HE-2751B     C
  355          MTO-2024-CRP-0355   AR-2024-CRP-0072   CRP     KO-8358      A
  356          MTO-2025-OP2-0356   AR-2025-OP2-0140   OP2     PM-5293C     A
  357          MTO-2025-ARP-0357   n/a                ARP     TR-2385      A
  358          MTO-2026-ARP-0358   AR-2026-ARP-0149   ARP     AZ-1222A     A
  359          MTO-2026-SMX-0359   AR-2026-SMX-0031   SMX     SW-8148      A
  360          MTO-2025-SMX-0360   n/a                SMX     FN-5734      A
  361          MTO-2025-OPU-0361   AR-2025-OPU-0126   OPU     SW-2477      A
  362          MTO-2025-NUP-0362   AR-2025-NUP-0190   NUP     FN-1399      A
  363          MTO-2025-OP3-0363   AR-2025-OP3-0123   OP3     TR-7614      A
  364          MTO-2025-OPU-0364   n/a                OPU     TK-4573B     B
  365          MTO-2025-OPU-0365   n/a                OPU     TX-3711B     B
  366          MTO-2025-OPP-0366   n/a                OPP     TK-2587      A
  367          MTO-2026-BRP-0367   AR-2026-BRP-0145   BRP     BL-8480      A
  368          MTO-2026-OP3-0368   AR-2026-OP3-0224   OP3     CV-4393A     A
  369          MTO-2024-OPU-0369   n/a                OPU     TR-3824B     B
  370          MTO-2024-BDX-0370   AR-2024-BDX-0096   BDX     PZ-8290A     A
  371          MTO-2025-ARP-0371   n/a                ARP     PM-8227B     B
  372          MTO-2026-ZCU-0372   AR-2026-ZCU-0170   ZCU     TX-8986C     A
  373          MTO-2025-BDX-0373   AR-2025-BDX-0026   BDX     TK-2331A     A
  374          MTO-2026-BRP-0374   n/a                BRP     BL-3069      A
  375          MTO-2026-ZCU-0375   AR-2026-ZCU-0244   ZCU     KO-5329A     A
  376          MTO-2025-ZCU-0376   AR-2025-ZCU-0090   ZCU     CD-7057A     A
  377          MTO-2024-OPP-0377   AR-2024-OPP-0246   OPP     CD-5731B     A
  378          MTO-2025-OP2-0378   AR-2025-OP2-0016   OP2     TK-2277B     A
  379          MTO-2024-ZCU-0379   AR-2024-ZCU-0116   ZCU     PM-3895A     A
  380          MTO-2024-OP2-0380   n/a                OP2     KO-7858      B

## 6. Risk case and CAPA/PAA data

The source contains 380 risk-case records. Wrapped PDF rows have been
recombined into one row per incident.

  -----------------------------------------------------------------------
  Occurrence    Risk case title Highest       Pre-risk      Pre-risk
  date                          impact        level         score
  ------------- --------------- ------------- ------------- -------------
  2026-03-12    Feed ---        Uptime Loss   III           200
                Mechanical Seal                             
                Leakage                                     

  2026-04-29    Cracked ---     Class A Eq.   II            4000
                High Radial     Breakdown                   
                Vibration Trip                              
                (Bearing                                    
                Distress)                                   

  2026-07-08    Cooling ---     Uptime Loss   III           200
                Motor Bearing                               
                Failure                                     
                (Overheating)                               

  2026-05-21    Feed/Effluent   Uptime Loss   III           400
                --- High                                    
                Fouling ---                                 
                Duty Loss &                                 
                High dP                                     

  2026-06-17    Product ---     Class A Eq.   III           400
                High Vibration  Breakdown                   
                (Coupling                                   
                Misalignment)                               

  2024-05-01    TR-8242A Rotor  Class A Eq.   IV            60
                High Vibration  Breakdown                   

  2025-03-27    CV-7690 Motor   Equipment Bad III           600
                Low Performance Actor                       

  2024-12-14    PZ-2154 Gasket  UPSD / Delay  IV            40
                Leakage         Start-up                    

  2026-06-15    SW-5620C        Equipment Bad III           200
                Impeller Worn   Actor                       
                Out                                         

  2025-04-26    PM-6523C Gasket UPSD / Delay  II            4000
                Leakage         Start-up                    

  2025-12-16    SW-3411B        Uptime Loss   III           400
                Control Valve                               
                Leakage                                     

  2025-04-22    RX-6438 Shaft   Uptime Loss   II            2000
                Crack                                       

  2025-03-11    CV-8399C        Uptime Loss   III           200
                Solenoid                                    
                Malfunction                                 

  2025-09-16    FN-7159 Bearing Equipment Bad III           200
                High Vibration  Actor                       

  2024-05-18    TX-8176 Gearbox Class A Eq.   IV            6
                High Vibration  Breakdown                   

  2025-06-16    PU-8272         Uptime Loss   IV            6
                Exchanger                                   
                Fouling                                     

  2024-05-04    TX-5843         Class A Eq.   IV            6
                Coupling Worn   Breakdown                   
                Out                                         

  2025-10-25    SW-4963 Control Class A Eq.   III           600
                Valve Leakage   Breakdown                   

  2025-06-29    PM-3818A        Class A Eq.   III           400
                Control Valve   Breakdown                   
                Stuck                                       

  2026-03-26    PU-2895 Control UPSD / Delay  III           400
                Valve Leakage   Start-up                    

  2024-12-26    TX-6085B Rotor  Class A Eq.   IV            40
                High Vibration  Breakdown                   

  2024-04-18    TK-5150B Rotor  Equipment Bad IV            40
                High Vibration  Actor                       

  2024-09-20    PU-1188B        Equipment Bad III           400
                Transmitter     Actor                       
                Error                                       

  2025-08-31    PM-8055 Oil     UPSD / Delay  IV            40
                Seal Leakage    Start-up                    

  2024-10-15    PU-7290C Motor  UPSD / Delay  III           400
                Low Performance Start-up                    

  2024-05-01    PZ-4479         Class A Eq.   IV            40
                Mechanical Seal Breakdown                   
                Leak                                        

  2025-12-01    PM-1191         Class A Eq.   IV            40
                Transmitter     Breakdown                   
                Error                                       

  2026-06-05    PZ-6185 Seal    Uptime Loss   III           200
                Leakage                                     

  2026-02-02    PM-5600B        Uptime Loss   IV            60
                Transmitter                                 
                Error                                       

  2024-06-06    PM-6753C        Class A Eq.   IV            40
                Bearing         Breakdown                   
                Overheat                                    

  2025-06-30    TR-5690 Motor   Class A Eq.   II            2000
                Low Performance Breakdown                   

  2024-09-24    TK-8363B        Uptime Loss   IV            40
                Control Valve                               
                Stuck                                       

  2025-03-08    TK-1241A        Uptime Loss   IV            6
                Bearing                                     
                Overheat                                    

  2025-06-28    TX-3672C Rotor  Equipment Bad IV            40
                High Vibration  Actor                       

  2025-11-30    SW-1565 Bearing Equipment Bad IV            60
                Worn Out        Actor                       

  2026-07-17    RX-3569A        Class A Eq.   III           400
                Exchanger       Breakdown                   
                Fouling                                     

  2025-03-28    TK-3192B        Uptime Loss   III           400
                Impeller Worn                               
                Out                                         

  2024-12-05    CV-3404         Class A Eq.   IV            60
                Solenoid        Breakdown                   
                Malfunction                                 

  2026-05-11    TX-3884B        Class A Eq.   IV            40
                Impeller Worn   Breakdown                   
                Out                                         

  2026-05-21    PU-6212         UPSD / Delay  IV            6
                Transmitter     Start-up                    
                Error                                       

  2025-01-13    HE-2276B Rotor  UPSD / Delay  IV            60
                High Vibration  Start-up                    

  2025-12-29    TX-1231B Rotor  Uptime Loss   III           600
                High Vibration                              

  2025-09-13    PZ-1300C        Class A Eq.   IV            40
                Solenoid        Breakdown                   
                Malfunction                                 

  2025-08-18    CV-6587 Bearing Uptime Loss   IV            6
                Overheat                                    

  2024-11-21    PU-8073A Shaft  UPSD / Delay  II            4000
                Crack           Start-up                    

  2025-03-15    TX-7355C        Equipment Bad III           400
                Solenoid        Actor                       
                Malfunction                                 

  2024-05-27    HE-3296B        Uptime Loss   IV            60
                Bearing High                                
                Vibration                                   

  2025-11-27    RX-8843 Shaft   Class A Eq.   III           200
                Crack           Breakdown                   

  2024-02-29    PZ-7199 Seal    Uptime Loss   III           400
                Leakage                                     

  2024-08-05    AZ-4763B        Inspection    III           400
                Impeller Worn   Report                      
                Out                                         

  2024-08-04    PU-6855 Oil     Uptime Loss   IV            40
                Seal Leakage                                

  2025-10-25    PZ-7054B Motor  Class A Eq.   IV            40
                Low Performance Breakdown                   

  2025-07-27    BL-6185 Gearbox Equipment Bad III           400
                High Vibration  Actor                       

  2026-04-13    FN-1575 Bearing Class A Eq.   IV            60
                High Vibration  Breakdown                   

  2024-01-23    PU-4209 Rotor   UPSD / Delay  IV            6
                High Vibration  Start-up                    

  2026-05-27    CD-2982B        Class A Eq.   IV            6
                Coupling Loose  Breakdown                   

  2025-03-25    BL-4126C Blade  Class A Eq.   IV            60
                Breakage        Breakdown                   

  2024-11-17    CV-5933 Oil     Class A Eq.   III           200
                Seal Leakage    Breakdown                   

  2025-02-14    PU-7158A        UPSD / Delay  IV            6
                Solenoid        Start-up                    
                Malfunction                                 

  2025-07-29    CV-8863C Oil    Class A Eq.   II            2000
                Seal Leakage    Breakdown                   

  2024-10-12    TX-4861B        Equipment Bad III           600
                Bearing High    Actor                       
                Vibration                                   

  2024-03-30    BL-1732C Shaft  Uptime Loss   IV            60
                Crack                                       

  2025-10-23    CV-1608A Oil    Class A Eq.   IV            6
                Seal Leakage    Breakdown                   

  2025-12-04    FN-2136 Rotor   Uptime Loss   III           600
                High Vibration                              

  2025-08-28    PU-8189A        Class A Eq.   III           600
                Exchanger       Breakdown                   
                Fouling                                     

  2024-12-16    BL-1795A Blade  Equipment Bad IV            60
                Breakage        Actor                       

  2025-06-24    PM-4639         Uptime Loss   III           200
                Mechanical Seal                             
                Leak                                        

  2025-03-25    CD-4653         Uptime Loss   IV            6
                Solenoid                                    
                Malfunction                                 

  2024-10-28    RX-8107B        Uptime Loss   IV            60
                Transmitter                                 
                Error                                       

  2025-01-22    BL-2438         Equipment Bad III           400
                Transmitter     Actor                       
                Error                                       

  2025-11-28    PU-5209B        Equipment Bad IV            60
                Gearbox High    Actor                       
                Vibration                                   

  2024-12-24    BL-2806 Bearing Class A Eq.   III           400
                Overheat        Breakdown                   

  2026-01-30    KO-2432C        Class A Eq.   III           400
                Control Valve   Breakdown                   
                Leakage                                     

  2025-04-13    CV-2925B        Uptime Loss   III           400
                Impeller Worn                               
                Out                                         

  2026-06-14    SW-2483 Gearbox Uptime Loss   IV            6
                High Vibration                              

  2024-05-14    RX-4619C        Class A Eq.   III           200
                Bearing Worn    Breakdown                   
                Out                                         

  2024-12-24    KO-5967B        Equipment Bad III           600
                Gearbox High    Actor                       
                Vibration                                   

  2024-09-27    TR-2916 Motor   Class A Eq.   IV            60
                Low Performance Breakdown                   

  2025-12-25    RX-3931 Control Uptime Loss   IV            60
                Valve Stuck                                 

  2026-01-15    PZ-6299C        Class A Eq.   III           400
                Exchanger       Breakdown                   
                Fouling                                     

  2025-01-21    RX-7490B Oil    Uptime Loss   IV            6
                Seal Leakage                                

  2026-02-27    PM-1018A        Uptime Loss   IV            60
                Solenoid                                    
                Malfunction                                 

  2024-02-25    BL-1954         Equipment Bad IV            60
                Transmitter     Actor                       
                Error                                       

  2026-05-03    PM-8555B        Equipment Bad IV            6
                Impeller Worn   Actor                       
                Out                                         

  2025-02-26    TX-3354         Class A Eq.   IV            60
                Mechanical Seal Breakdown                   
                Leak                                        

  2024-10-29    BL-1631B        Uptime Loss   II            4000
                Exchanger                                   
                Fouling                                     

  2025-07-29    TX-5573B Gasket UPSD / Delay  IV            6
                Leakage         Start-up                    

  2025-01-06    CD-1529         Quality Loss  III           600
                Coupling Loose                              

  2024-02-04    BL-8286         Uptime Loss   II            4000
                Exchanger                                   
                Fouling                                     

  2025-12-19    PU-7196C Motor  Uptime Loss   IV            60
                Low Performance                             

  2024-04-06    SW-5428 Seal    Uptime Loss   III           600
                Leakage                                     

  2024-07-25    TX-3821C        Equipment Bad III           200
                Bearing         Actor                       
                Overheat                                    

  2024-05-03    CD-3164 Rotor   Uptime Loss   IV            6
                High Vibration                              

  2025-02-07    PM-6744 Control Uptime Loss   IV            40
                Valve Leakage                               

  2025-01-11    AZ-7326B        Uptime Loss   III           600
                Solenoid                                    
                Malfunction                                 

  2026-01-27    KO-6912A        Class A Eq.   IV            40
                Transmitter     Breakdown                   
                Error                                       

  2026-06-25    HE-7828C        Equipment Bad III           600
                Solenoid        Actor                       
                Malfunction                                 

  2026-06-05    TR-8775A Seal   Equipment Bad IV            40
                Leakage         Actor                       

  2026-02-07    TK-7586B        Uptime Loss   II            4000
                Solenoid                                    
                Malfunction                                 

  2026-01-03    KO-1172C        Uptime Loss   II            4000
                Mechanical Seal                             
                Leak                                        

  2024-08-12    TX-3554 Bearing Class A Eq.   III           600
                High Vibration  Breakdown                   

  2026-05-24    BL-3912         Uptime Loss   IV            6
                Transmitter                                 
                Error                                       

  2024-01-04    BL-7186C        UPSD / Delay  IV            40
                Control Valve   Start-up                    
                Leakage                                     

  2026-07-25    PM-4607         Uptime Loss   IV            60
                Impeller Worn                               
                Out                                         

  2025-09-10    TX-5871 Control UPSD / Delay  IV            40
                Valve Leakage   Start-up                    

  2025-06-08    PU-7657         Class A Eq.   IV            40
                Coupling Worn   Breakdown                   
                Out                                         

  2024-09-23    BL-8930A        Uptime Loss   IV            60
                Exchanger                                   
                Fouling                                     

  2024-09-17    PM-4728A Rotor  Uptime Loss   II            4000
                High Vibration                              

  2026-03-22    TX-6768B        Uptime Loss   III           200
                Coupling Worn                               
                Out                                         

  2026-03-27    HE-1493         Class A Eq.   III           400
                Exchanger       Breakdown                   
                Fouling                                     

  2024-02-25    TX-3809A        Class A Eq.   III           600
                Coupling Worn   Breakdown                   
                Out                                         

  2025-02-09    TK-6638 Rotor   Uptime Loss   IV            60
                High Vibration                              

  2026-02-19    PM-3131A        Uptime Loss   IV            40
                Control Valve                               
                Leakage                                     

  2026-01-18    RX-8190C        Equipment Bad II            4000
                Control Valve   Actor                       
                Leakage                                     

  2025-10-07    PZ-5870 Bearing Inspection    IV            6
                High Vibration  Report                      

  2024-05-28    PU-7899A Oil    Inspection    IV            40
                Seal Leakage    Report                      

  2024-04-28    PM-5170C        Uptime Loss   IV            6
                Control Valve                               
                Leakage                                     

  2026-04-09    TR-2677C        UPSD / Delay  III           400
                Exchanger       Start-up                    
                Fouling                                     

  2024-10-20    PZ-6565A Motor  Equipment Bad IV            6
                Low Performance Actor                       

  2025-02-17    TX-1722A Gasket Class A Eq.   IV            40
                Leakage         Breakdown                   

  2024-12-11    TK-5168C        UPSD / Delay  III           400
                Control Valve   Start-up                    
                Leakage                                     

  2025-02-14    FN-7608 Motor   Class A Eq.   IV            40
                Low Performance Breakdown                   

  2025-05-03    AZ-1653C Oil    Class A Eq.   IV            60
                Seal Leakage    Breakdown                   

  2025-08-09    HE-6128 Blade   Class A Eq.   IV            60
                Breakage        Breakdown                   

  2024-04-25    RX-6481         Equipment Bad III           200
                Impeller Worn   Actor                       
                Out                                         

  2025-09-23    PZ-2526C Motor  Uptime Loss   IV            6
                Low Performance                             

  2024-10-06    CD-2356A        Equipment Bad III           400
                Control Valve   Actor                       
                Leakage                                     

  2024-11-02    RX-2091B Gasket Uptime Loss   II            2000
                Leakage                                     

  2026-01-16    BL-2287A Blade  Uptime Loss   IV            6
                Breakage                                    

  2024-01-29    CD-6044A        Uptime Loss   IV            40
                Coupling Worn                               
                Out                                         

  2024-06-03    RX-3576         Uptime Loss   IV            60
                Solenoid                                    
                Malfunction                                 

  2025-03-16    TR-3696 Motor   Class A Eq.   III           400
                Low Performance Breakdown                   

  2024-08-31    RX-3112 Bearing Equipment Bad III           600
                High Vibration  Actor                       

  2024-03-13    PZ-8690B Motor  Uptime Loss   IV            40
                Low Performance                             

  2025-10-12    TX-3876B        Equipment Bad III           600
                Control Valve   Actor                       
                Stuck                                       

  2026-07-10    FN-3044 Seal    Uptime Loss   IV            6
                Leakage                                     

  2025-08-02    SW-3674B        Class A Eq.   IV            60
                Bearing         Breakdown                   
                Overheat                                    

  2025-01-09    BL-7185B        Uptime Loss   II            4000
                Coupling Worn                               
                Out                                         

  2024-09-24    PU-4041C        Uptime Loss   III           400
                Control Valve                               
                Leakage                                     

  2025-07-07    TK-1610C        UPSD / Delay  II            2000
                Transmitter     Start-up                    
                Error                                       

  2025-06-15    HE-1090B Shaft  UPSD / Delay  IV            60
                Crack           Start-up                    

  2024-09-15    SW-6198B        Uptime Loss   II            2000
                Gearbox High                                
                Vibration                                   

  2026-01-17    HE-8579B Gasket Class A Eq.   II            2000
                Leakage         Breakdown                   

  2024-07-08    PM-6481B        Uptime Loss   IV            40
                Coupling Worn                               
                Out                                         

  2025-03-30    RX-5203C        Class A Eq.   III           400
                Bearing         Breakdown                   
                Overheat                                    

  2025-10-25    AZ-1094B        Equipment Bad III           200
                Impeller Worn   Actor                       
                Out                                         

  2025-12-17    AZ-3776A        UPSD / Delay  IV            40
                Bearing         Start-up                    
                Overheat                                    

  2024-07-23    KO-1107         Class A Eq.   III           600
                Coupling Worn   Breakdown                   
                Out                                         

  2024-02-13    PZ-3888C Motor  Uptime Loss   II            4000
                Low Performance                             

  2024-07-14    BL-3575         Uptime Loss   IV            6
                Solenoid                                    
                Malfunction                                 

  2025-06-10    BL-4956 Motor   Class A Eq.   IV            6
                Low Performance Breakdown                   

  2026-02-24    SW-1941A        Class A Eq.   IV            6
                Coupling Loose  Breakdown                   

  2024-06-12    PM-8835B Rotor  Uptime Loss   III           600
                High Vibration                              

  2025-10-14    PZ-3313B        Equipment Bad II            4000
                Coupling Loose  Actor                       

  2024-11-01    PU-7733C        UPSD / Delay  III           400
                Bearing Worn    Start-up                    
                Out                                         

  2024-02-19    FN-3899         Uptime Loss   IV            60
                Exchanger                                   
                Fouling                                     

  2024-11-30    SW-6750A        Uptime Loss   III           200
                Control Valve                               
                Stuck                                       

  2024-09-19    FN-2402A        Equipment Bad IV            40
                Bearing         Actor                       
                Overheat                                    

  2024-05-10    PZ-8155B        Equipment Bad III           400
                Transmitter     Actor                       
                Error                                       

  2026-06-13    TX-8349 Gearbox Uptime Loss   III           600
                High Vibration                              

  2025-01-08    TR-3587C        Class A Eq.   IV            6
                Mechanical Seal Breakdown                   
                Leak                                        

  2025-02-19    FN-7628A Shaft  Class A Eq.   III           400
                Crack           Breakdown                   

  2025-05-27    BL-4656C        Class A Eq.   III           400
                Control Valve   Breakdown                   
                Stuck                                       

  2026-03-03    PU-6682 Motor   Class A Eq.   IV            60
                Low Performance Breakdown                   

  2024-06-02    TX-4966C Seal   Equipment Bad III           200
                Leakage         Actor                       

  2024-12-21    TX-2796A        Equipment Bad II            4000
                Bearing         Actor                       
                Overheat                                    

  2024-02-18    AZ-3493B        Class A Eq.   II            2000
                Exchanger       Breakdown                   
                Fouling                                     

  2025-12-25    PM-2566C        Equipment Bad IV            60
                Coupling Worn   Actor                       
                Out                                         

  2024-04-13    BL-2784A        Equipment Bad III           400
                Control Valve   Actor                       
                Leakage                                     

  2024-11-08    PU-7794 Rotor   Uptime Loss   IV            60
                High Vibration                              

  2025-11-14    HE-2776A Oil    Equipment Bad IV            40
                Seal Leakage    Actor                       

  2024-03-27    AZ-1735A Oil    UPSD / Delay  III           400
                Seal Leakage    Start-up                    

  2025-03-26    AZ-1424 Bearing Class A Eq.   IV            40
                High Vibration  Breakdown                   

  2025-03-13    AZ-8765C        Class A Eq.   IV            40
                Bearing Worn    Breakdown                   
                Out                                         

  2024-02-01    AZ-6656C Blade  Class A Eq.   IV            40
                Breakage        Breakdown                   

  2024-11-14    HE-7629         Equipment Bad III           400
                Coupling Loose  Actor                       

  2024-12-24    CV-4573A        Class A Eq.   IV            6
                Coupling Loose  Breakdown                   

  2026-04-21    PM-3070 Bearing Class A Eq.   III           200
                High Vibration  Breakdown                   

  2025-08-03    HE-5523 Gasket  Uptime Loss   III           600
                Leakage                                     

  2025-12-12    TX-8678 Seal    Inspection    III           200
                Leakage         Report                      

  2024-04-01    PU-8356         Class A Eq.   IV            60
                Exchanger       Breakdown                   
                Fouling                                     

  2024-03-20    PU-2931B        Uptime Loss   IV            40
                Bearing High                                
                Vibration                                   

  2026-06-07    AZ-4698B Oil    Class A Eq.   IV            60
                Seal Leakage    Breakdown                   

  2024-05-16    PM-4526B        Inspection    IV            40
                Bearing High    Report                      
                Vibration                                   

  2026-05-04    TK-6644B        Equipment Bad IV            6
                Bearing High    Actor                       
                Vibration                                   

  2026-04-07    PU-1676A        Uptime Loss   IV            40
                Control Valve                               
                Stuck                                       

  2025-08-01    TK-2079B Shaft  Uptime Loss   III           200
                Crack                                       

  2024-03-06    SW-3050         Equipment Bad III           200
                Coupling Worn   Actor                       
                Out                                         

  2024-12-11    TR-6283A        Class A Eq.   III           200
                Transmitter     Breakdown                   
                Error                                       

  2024-02-18    FN-3328B        Uptime Loss   IV            6
                Control Valve                               
                Stuck                                       

  2024-01-15    TX-4689 Seal    Class A Eq.   III           200
                Leakage         Breakdown                   

  2025-01-05    TX-7313 Rotor   Class A Eq.   IV            6
                High Vibration  Breakdown                   

  2025-04-17    PM-7974A        UPSD / Delay  III           400
                Bearing Worn    Start-up                    
                Out                                         

  2026-06-20    PM-1440         Uptime Loss   IV            60
                Coupling Loose                              

  2024-08-13    CV-5846 Rotor   Uptime Loss   IV            60
                High Vibration                              

  2024-10-26    CD-1513 Blade   Equipment Bad IV            60
                Breakage        Actor                       

  2024-02-12    FN-2268         Uptime Loss   III           400
                Solenoid                                    
                Malfunction                                 

  2025-04-30    KO-4139B        UPSD / Delay  III           200
                Transmitter     Start-up                    
                Error                                       

  2024-02-14    TX-6875         Uptime Loss   III           200
                Mechanical Seal                             
                Leak                                        

  2024-06-21    CD-8154 Blade   Uptime Loss   III           600
                Breakage                                    

  2024-01-06    RX-7012B        Class A Eq.   IV            60
                Solenoid        Breakdown                   
                Malfunction                                 

  2024-08-06    TX-6162B        Equipment Bad III           600
                Exchanger       Actor                       
                Fouling                                     

  2024-09-06    PU-7701C        Uptime Loss   III           400
                Coupling Loose                              

  2026-04-23    KO-4022B Motor  Uptime Loss   III           400
                Low Performance                             

  2025-01-03    HE-5734C Seal   Equipment Bad IV            6
                Leakage         Actor                       

  2024-01-28    BL-7977 Gearbox Class A Eq.   IV            40
                High Vibration  Breakdown                   

  2024-12-10    RX-1896A        Uptime Loss   III           600
                Coupling Worn                               
                Out                                         

  2024-05-28    TR-1447A Gasket Class A Eq.   III           600
                Leakage         Breakdown                   

  2025-06-16    TX-7941A Motor  Uptime Loss   III           400
                Low Performance                             

  2025-08-24    PM-2733C        Equipment Bad III           400
                Control Valve   Actor                       
                Stuck                                       

  2025-10-10    SW-3110 Control Class A Eq.   IV            40
                Valve Stuck     Breakdown                   

  2024-07-11    TX-2151C        Uptime Loss   IV            40
                Control Valve                               
                Stuck                                       

  2025-04-10    KO-8443C        Uptime Loss   III           600
                Bearing Worn                                
                Out                                         

  2026-05-07    CD-4129B Blade  Equipment Bad IV            6
                Breakage        Actor                       

  2025-10-15    TX-4180 Shaft   Equipment Bad IV            60
                Crack           Actor                       

  2024-07-28    CD-7424A Blade  Class A Eq.   IV            60
                Breakage        Breakdown                   

  2024-04-30    CD-4525B Blade  Uptime Loss   III           600
                Breakage                                    

  2025-03-14    BL-7358 Bearing Uptime Loss   IV            40
                Worn Out                                    

  2024-09-06    PZ-1094 Bearing Uptime Loss   IV            40
                Worn Out                                    

  2026-07-07    PZ-4712         Uptime Loss   III           400
                Exchanger                                   
                Fouling                                     

  2024-10-04    PM-3484B Seal   Uptime Loss   III           400
                Leakage                                     

  2024-10-15    BL-4995 Shaft   Uptime Loss   IV            40
                Crack                                       

  2025-10-17    PZ-4078B        Equipment Bad IV            60
                Bearing         Actor                       
                Overheat                                    

  2026-06-22    TR-5785         UPSD / Delay  IV            60
                Impeller Worn   Start-up                    
                Out                                         

  2025-02-25    SW-5472B Seal   Equipment Bad IV            40
                Leakage         Actor                       

  2024-07-23    RX-3213C        Class A Eq.   IV            40
                Transmitter     Breakdown                   
                Error                                       

  2026-04-06    TR-7081         Uptime Loss   III           200
                Impeller Worn                               
                Out                                         

  2025-11-22    BL-4356 Bearing Uptime Loss   IV            6
                High Vibration                              

  2024-06-16    KO-8623 Control Equipment Bad IV            60
                Valve Stuck     Actor                       

  2026-01-11    PM-3251 Seal    Inspection    III           400
                Leakage         Report                      

  2024-08-24    PU-7906         Class A Eq.   III           400
                Coupling Loose  Breakdown                   

  2025-03-07    CV-5846         Class A Eq.   III           400
                Solenoid        Breakdown                   
                Malfunction                                 

  2025-11-20    KO-8837B Shaft  Uptime Loss   IV            6
                Crack                                       

  2025-05-17    CD-4479B        Equipment Bad III           400
                Solenoid        Actor                       
                Malfunction                                 

  2026-05-09    CD-3123 Seal    Class A Eq.   III           200
                Leakage         Breakdown                   

  2025-10-23    TX-3574C        Uptime Loss   IV            60
                Solenoid                                    
                Malfunction                                 

  2024-06-25    TR-6290 Motor   Uptime Loss   IV            6
                Low Performance                             

  2025-10-30    TK-6178A        UPSD / Delay  IV            40
                Control Valve   Start-up                    
                Leakage                                     

  2024-05-29    SW-5535 Blade   Class A Eq.   IV            40
                Breakage        Breakdown                   

  2024-12-16    CD-6577B Seal   Uptime Loss   III           400
                Leakage                                     

  2026-03-13    HE-3559B        Uptime Loss   IV            40
                Impeller Worn                               
                Out                                         

  2025-12-15    RX-3162 Shaft   Uptime Loss   IV            40
                Crack                                       

  2025-12-23    PU-7148         UPSD / Delay  III           200
                Exchanger       Start-up                    
                Fouling                                     

  2026-02-21    KO-1825 Control Uptime Loss   IV            40
                Valve Leakage                               

  2024-04-11    AZ-2808 Control Class A Eq.   III           200
                Valve Leakage   Breakdown                   

  2024-09-16    TX-1039B        Equipment Bad IV            6
                Coupling Loose  Actor                       

  2026-05-16    RX-2949A        Class A Eq.   III           200
                Bearing         Breakdown                   
                Overheat                                    

  2025-02-06    PM-7516C        Equipment Bad IV            40
                Coupling Loose  Actor                       

  2025-08-14    CD-5066A Seal   Inspection    IV            60
                Leakage         Report                      

  2024-06-22    TX-7293 Oil     Class A Eq.   IV            40
                Seal Leakage    Breakdown                   

  2026-05-21    KO-3418A Blade  Uptime Loss   IV            40
                Breakage                                    

  2025-05-13    HE-2011         Inspection    IV            6
                Coupling Loose  Report                      

  2026-02-03    RX-5939B        Uptime Loss   III           200
                Impeller Worn                               
                Out                                         

  2025-08-26    FN-8551C Shaft  Uptime Loss   II            4000
                Crack                                       

  2025-02-06    PU-2304A        Equipment Bad III           600
                Bearing High    Actor                       
                Vibration                                   

  2025-07-15    TR-8066         Equipment Bad III           400
                Solenoid        Actor                       
                Malfunction                                 

  2024-07-25    RX-1575         Uptime Loss   III           400
                Transmitter                                 
                Error                                       

  2024-12-06    HE-1535 Shaft   Inspection    IV            60
                Crack           Report                      

  2026-04-20    PM-2842A        Uptime Loss   IV            40
                Gearbox High                                
                Vibration                                   

  2026-05-16    PM-7677 Seal    Class A Eq.   IV            6
                Leakage         Breakdown                   

  2024-04-28    PM-6340A Shaft  Uptime Loss   IV            6
                Crack                                       

  2025-07-02    RX-8147A        Class A Eq.   IV            60
                Transmitter     Breakdown                   
                Error                                       

  2024-02-06    AZ-8666 Shaft   Class A Eq.   IV            60
                Crack           Breakdown                   

  2025-01-07    TX-1531 Gasket  Quality Loss  IV            6
                Leakage                                     

  2025-06-13    TR-3550 Bearing Uptime Loss   IV            6
                High Vibration                              

  2026-01-06    PZ-2759 Seal    Class A Eq.   IV            6
                Leakage         Breakdown                   

  2024-08-10    CD-7937A        Class A Eq.   III           200
                Gearbox High    Breakdown                   
                Vibration                                   

  2026-06-18    BL-3946C Oil    Class A Eq.   IV            60
                Seal Leakage    Breakdown                   

  2025-06-03    SW-6175C        Uptime Loss   II            2000
                Bearing High                                
                Vibration                                   

  2025-03-28    PM-1316B Motor  Uptime Loss   III           400
                Low Performance                             

  2026-03-02    CV-3290         Class A Eq.   II            2000
                Coupling Loose  Breakdown                   

  2024-11-14    PZ-7507 Blade   Uptime Loss   III           200
                Breakage                                    

  2026-03-19    TX-1468 Gasket  Equipment Bad II            4000
                Leakage         Actor                       

  2024-07-05    PZ-6564         UPSD / Delay  IV            40
                Coupling Loose  Start-up                    

  2024-04-13    AZ-3288 Bearing UPSD / Delay  IV            60
                High Vibration  Start-up                    

  2024-03-14    CD-2449C        Uptime Loss   III           600
                Coupling Loose                              

  2024-12-23    TK-1215 Oil     Equipment Bad IV            6
                Seal Leakage    Actor                       

  2024-08-11    CD-6611 Seal    Uptime Loss   IV            60
                Leakage                                     

  2024-12-17    TR-3408C Oil    Uptime Loss   III           400
                Seal Leakage                                

  2026-05-31    SW-8737A        Class A Eq.   III           600
                Bearing High    Breakdown                   
                Vibration                                   

  2025-01-23    TX-3699         Class A Eq.   IV            40
                Exchanger       Breakdown                   
                Fouling                                     

  2024-03-06    TX-6148B        Equipment Bad IV            40
                Bearing Worn    Actor                       
                Out                                         

  2025-02-11    BL-2513A        Uptime Loss   IV            6
                Impeller Worn                               
                Out                                         

  2026-03-06    AZ-1128C Motor  Class A Eq.   III           400
                Low Performance Breakdown                   

  2024-05-26    TX-2223 Bearing UPSD / Delay  IV            40
                Worn Out        Start-up                    

  2026-07-06    HE-4966C        Uptime Loss   IV            40
                Exchanger                                   
                Fouling                                     

  2025-08-10    TX-4451 Oil     UPSD / Delay  IV            40
                Seal Leakage    Start-up                    

  2024-06-25    CD-7117C        Class A Eq.   IV            6
                Control Valve   Breakdown                   
                Leakage                                     

  2024-02-10    PU-5056C Gasket Uptime Loss   III           600
                Leakage                                     

  2025-04-11    PM-6780 Gasket  UPSD / Delay  IV            40
                Leakage         Start-up                    

  2024-05-19    HE-2598B        Equipment Bad IV            40
                Mechanical Seal Actor                       
                Leak                                        

  2025-12-11    PU-4574B        Uptime Loss   III           600
                Mechanical Seal                             
                Leak                                        

  2025-01-09    KO-7770A Seal   Uptime Loss   III           200
                Leakage                                     

  2024-10-07    BL-4453C        Uptime Loss   III           400
                Impeller Worn                               
                Out                                         

  2024-03-14    BL-8124A        Uptime Loss   IV            40
                Exchanger                                   
                Fouling                                     

  2025-09-14    KO-5432C        UPSD / Delay  III           200
                Transmitter     Start-up                    
                Error                                       

  2025-03-30    TX-5187B Shaft  Class A Eq.   IV            6
                Crack           Breakdown                   

  2024-03-16    TK-1061C        Equipment Bad IV            40
                Exchanger       Actor                       
                Fouling                                     

  2026-05-18    KO-2904         Class A Eq.   IV            40
                Coupling Worn   Breakdown                   
                Out                                         

  2025-05-22    TX-6415B        Class A Eq.   IV            60
                Gearbox High    Breakdown                   
                Vibration                                   

  2025-09-14    AZ-4525A Gasket Class A Eq.   II            2000
                Leakage         Breakdown                   

  2025-09-27    KO-4538B Seal   Class A Eq.   IV            40
                Leakage         Breakdown                   

  2025-12-21    TX-3146 Gasket  UPSD / Delay  III           400
                Leakage         Start-up                    

  2025-09-16    BL-7719 Rotor   Class A Eq.   IV            40
                High Vibration  Breakdown                   

  2024-01-29    CV-6240         Class A Eq.   IV            40
                Solenoid        Breakdown                   
                Malfunction                                 

  2026-02-08    CD-6973         UPSD / Delay  III           400
                Coupling Loose  Start-up                    

  2025-01-26    PZ-6982A        Uptime Loss   IV            60
                Bearing High                                
                Vibration                                   

  2026-04-16    SW-5057 Bearing Uptime Loss   IV            60
                Overheat                                    

  2025-10-10    PM-4339B        UPSD / Delay  IV            6
                Coupling Worn   Start-up                    
                Out                                         

  2024-08-08    TX-6419A        UPSD / Delay  IV            60
                Control Valve   Start-up                    
                Leakage                                     

  2025-10-04    CV-2117A Rotor  Uptime Loss   IV            40
                High Vibration                              

  2025-08-04    FN-5984         Class A Eq.   III           400
                Exchanger       Breakdown                   
                Fouling                                     

  2024-05-08    CD-4841         UPSD / Delay  IV            6
                Mechanical Seal Start-up                    
                Leak                                        

  2024-11-09    TX-2023C        Uptime Loss   III           400
                Impeller Worn                               
                Out                                         

  2025-04-22    PZ-5007 Seal    Equipment Bad III           400
                Leakage         Actor                       

  2024-10-29    AZ-4021 Bearing Class A Eq.   IV            6
                Worn Out        Breakdown                   

  2025-01-07    RX-2530 Blade   Class A Eq.   III           600
                Breakage        Breakdown                   

  2025-12-26    SW-8132A Shaft  Class A Eq.   IV            60
                Crack           Breakdown                   

  2024-12-27    HE-7991 Control Class A Eq.   III           400
                Valve Stuck     Breakdown                   

  2025-01-13    AZ-6357 Motor   Equipment Bad IV            40
                Low Performance Actor                       

  2024-05-29    TX-3092C Rotor  Equipment Bad IV            6
                High Vibration  Actor                       

  2025-06-06    PU-6149 Control Class A Eq.   IV            40
                Valve Leakage   Breakdown                   

  2024-04-14    PZ-2579B Rotor  Uptime Loss   III           400
                High Vibration                              

  2025-08-04    PM-7696         Uptime Loss   IV            60
                Mechanical Seal                             
                Leak                                        

  2024-11-20    PM-3134C Seal   Equipment Bad III           200
                Leakage         Actor                       

  2025-10-18    PM-4861B Seal   Equipment Bad III           200
                Leakage         Actor                       

  2025-05-17    CD-5263B        Uptime Loss   III           400
                Control Valve                               
                Leakage                                     

  2025-12-28    AZ-2053C Oil    Uptime Loss   IV            6
                Seal Leakage                                

  2026-05-18    KO-6941B        Class A Eq.   III           200
                Solenoid        Breakdown                   
                Malfunction                                 

  2025-08-21    FN-8723B        Uptime Loss   III           200
                Gearbox High                                
                Vibration                                   

  2026-02-03    HE-4689A Oil    UPSD / Delay  IV            6
                Seal Leakage    Start-up                    

  2024-04-20    KO-7907 Oil     Equipment Bad III           200
                Seal Leakage    Actor                       

  2024-11-05    TR-4857B        Uptime Loss   III           400
                Transmitter                                 
                Error                                       

  2025-12-22    HE-5877C Motor  Uptime Loss   III           400
                Low Performance                             

  2026-07-16    TK-2175C        Uptime Loss   IV            6
                Coupling Worn                               
                Out                                         

  2025-09-23    SW-5367 Oil     Uptime Loss   IV            40
                Seal Leakage                                

  2026-05-20    KO-6690C        Equipment Bad IV            6
                Coupling Loose  Actor                       

  2026-01-29    PM-1108B Gasket Uptime Loss   III           600
                Leakage                                     

  2024-07-03    SW-2768C Oil    Equipment Bad IV            40
                Seal Leakage    Actor                       

  2024-04-25    TK-7349 Seal    Uptime Loss   II            4000
                Leakage                                     

  2024-10-03    AZ-6778A        Class A Eq.   III           200
                Solenoid        Breakdown                   
                Malfunction                                 

  2025-10-20    BL-6590         Class A Eq.   IV            60
                Solenoid        Breakdown                   
                Malfunction                                 

  2025-03-11    FN-8488C        Uptime Loss   IV            6
                Bearing                                     
                Overheat                                    

  2026-05-04    PU-4158C        Class A Eq.   IV            60
                Transmitter     Breakdown                   
                Error                                       

  2024-10-06    TX-1131 Oil     Uptime Loss   III           600
                Seal Leakage                                

  2026-03-21    PU-8439A        Uptime Loss   IV            40
                Coupling Worn                               
                Out                                         

  2024-12-15    CD-5189C        Class A Eq.   IV            40
                Control Valve   Breakdown                   
                Stuck                                       

  2024-08-03    KO-1744         Uptime Loss   III           400
                Mechanical Seal                             
                Leak                                        

  2026-05-01    TR-6629 Control UPSD / Delay  III           200
                Valve Leakage   Start-up                    

  2026-04-08    TX-4166C Shaft  Class A Eq.   IV            40
                Crack           Breakdown                   

  2024-11-21    PM-2050         Uptime Loss   I             40000
                Impeller Worn                               
                Out                                         

  2026-02-21    FN-6098A        Class A Eq.   III           200
                Impeller Worn   Breakdown                   
                Out                                         

  2024-08-12    KO-7855B        UPSD / Delay  IV            60
                Coupling Worn   Start-up                    
                Out                                         

  2026-04-26    HE-2751B Gasket Uptime Loss   IV            60
                Leakage                                     

  2024-10-10    KO-8358 Rotor   Uptime Loss   III           400
                High Vibration                              

  2025-05-24    PM-5293C        Uptime Loss   III           200
                Bearing High                                
                Vibration                                   

  2025-04-19    TR-2385 Bearing Uptime Loss   IV            40
                High Vibration                              

  2026-07-06    AZ-1222A Rotor  Uptime Loss   IV            6
                High Vibration                              

  2026-05-11    SW-8148         Uptime Loss   III           400
                Solenoid                                    
                Malfunction                                 

  2025-02-25    FN-5734         Uptime Loss   IV            6
                Solenoid                                    
                Malfunction                                 

  2025-08-31    SW-2477         Uptime Loss   IV            6
                Transmitter                                 
                Error                                       

  2025-09-15    FN-1399 Control UPSD / Delay  IV            40
                Valve Stuck     Start-up                    

  2025-05-28    TR-7614 Gearbox UPSD / Delay  IV            40
                High Vibration  Start-up                    

  2025-08-31    TK-4573B        UPSD / Delay  III           200
                Control Valve   Start-up                    
                Leakage                                     

  2025-04-04    TX-3711B        Inspection    III           400
                Bearing Worn    Report                      
                Out                                         

  2025-09-03    TK-2587         Class A Eq.   II            4000
                Coupling Loose  Breakdown                   

  2026-05-10    BL-8480 Blade   Uptime Loss   IV            6
                Breakage                                    

  2026-03-05    CV-4393A        Class A Eq.   III           200
                Coupling Worn   Breakdown                   
                Out                                         

  2024-02-04    TR-3824B        Uptime Loss   II            4000
                Bearing                                     
                Overheat                                    

  2024-05-28    PZ-8290A Motor  Equipment Bad IV            40
                Low Performance Actor                       

  2025-12-15    PM-8227B        Uptime Loss   III           400
                Mechanical Seal                             
                Leak                                        

  2026-05-18    TX-8986C        Uptime Loss   IV            6
                Mechanical Seal                             
                Leak                                        

  2025-06-20    TK-2331A        Class A Eq.   IV            40
                Mechanical Seal Breakdown                   
                Leak                                        

  2026-04-26    BL-3069 Gearbox Uptime Loss   IV            40
                High Vibration                              

  2026-04-18    KO-5329A Shaft  Uptime Loss   III           600
                Crack                                       

  2025-10-09    CD-7057A        Uptime Loss   IV            60
                Control Valve                               
                Leakage                                     

  2024-05-17    CD-5731B        Class A Eq.   III           200
                Gearbox High    Breakdown                   
                Vibration                                   

  2025-11-18    TK-2277B        Equipment Bad III           200
                Solenoid        Actor                       
                Malfunction                                 

  2024-06-27    PM-3895A Shaft  Equipment Bad III           600
                Crack           Actor                       

  2024-06-18    KO-7858 Oil     Equipment Bad III           600
                Seal Leakage    Actor                       
  -----------------------------------------------------------------------

## 7. RCA status and failure mechanism

  ---------------------------------------------------------------------------
  PIC (RCA) Overall      Discipline   Equipment   Component     Failure
            status                    type                      mechanism
  --------- ------------ ------------ ----------- ------------- -------------
  REL-05    CA/PA        ROT          PU          Mechanical    Mechanical
            EXECUTION                             Seal          

  REL-05    CA/PA        ROT          CO          Journal       High
            EXECUTION                             Bearing       

  REL-02    CA/PA        ELE          EM          Motor Bearing Motor
            EXECUTION                                           

  STA-02    CA/PA        STA          HB          Tube Bundle   High
            EXECUTION                                           

  ROT-01    CA/PA        ROT          BL          Coupling      High
            EXECUTION                                           

  ELE-02    RCA PROCESS  ELE          TR          Rotor         High
                                                                Vibration

  ELE-01    CA/PA        INS          VA          Motor         Low
            EXECUTION                                           Performance

  ELE-01    CA/PA        INS          PZ          Gasket        Leakage
            EXECUTION                                           

  ELE-02    RISK         ELE          SW          Impeller      Worn Out
            CANCELED                                            

  REL-03    RCA PROCESS  ELE          EM          Gasket        Leakage

  INS-01    RISK         ELE          SW          Valve         Leakage
            CANCELED                                            

  ELE-02    CA/PA        STA          RX          Shaft         Crack
            EXECUTION                                           

  REL-05    CA/PA        INS          VA          Solenoid      Malfunction
            EXECUTION                                           

  REL-03    RISK CLOSED  ROT          FA          Bearing       High
                                                                Vibration

  OPS-01    RISK         INS          TX          Gearbox       High
            CANCELED                                            Vibration

  INS-01    RISK CLOSED  ROT          PU          Tube Bundle   Fouling

  ROT-01    RCA PROCESS  INS          TX          Coupling      Worn Out

  ROT-02    MONITORING   ELE          SW          Valve         Leakage
            RESULT                                              

  ROT-02    RISK CLOSED  ROT          EM          Valve         Stuck

  REL-03    RCA PROCESS  ROT          PU          Valve         Leakage

  REL-03    RCA PROCESS  INS          TX          Rotor         High
                                                                Vibration

  STA-01    RISK CLOSED  STA          TK          Rotor         High
                                                                Vibration

  INS-01    CA/PA        ROT          PU          Transmitter   Error
            EXECUTION                                           

  ELE-02    RISK CLOSED  ELE          EM          Oil Seal      Leakage

  REL-05    RISK CLOSED  ROT          PU          Motor         Low
                                                                Performance

  ROT-03    RCA PROCESS  INS          PZ          Mechanical    Leakage
                                                  Seal          

  REL-03    RISK CLOSED  ELE          EM          Transmitter   Error

  REL-02    RCA PROCESS  INS          PZ          Seal          Leakage

  ROT-03    CA/PA        ROT          EM          Transmitter   Error
            EXECUTION                                           

  STA-01    RCA PROCESS  ROT          EM          Bearing       Overheat

  ROT-01    NEW          ELE          TR          Motor         Low
            REGISTERED                                          Performance

  ELE-02    RISK CLOSED  STA          TK          Valve         Stuck

  ELE-02    CA/PA        STA          TK          Bearing       Overheat
            EXECUTION                                           

  REL-03    RCA PROCESS  INS          TX          Rotor         High
                                                                Vibration

  STA-02    RISK CLOSED  ELE          SW          Bearing       Worn Out

  STA-02    RISK         STA          RX          Tube Bundle   Fouling
            CANCELED                                            

  INS-02    RISK CLOSED  STA          TK          Impeller      Worn Out

  ELE-01    CA/PA        INS          VA          Solenoid      Malfunction
            EXECUTION                                           

  STA-01    RCA PROCESS  INS          TX          Impeller      Worn Out

  INS-02    RISK         ROT          PU          Transmitter   Error
            CANCELED                                            

  STA-01    RISK CLOSED  STA          HB          Rotor         High
                                                                Vibration

  INS-01    NEW          INS          TX          Rotor         High
            REGISTERED                                          Vibration

  STA-01    RISK CLOSED  INS          PZ          Solenoid      Malfunction

  INS-02    RISK         INS          VA          Bearing       Overheat
            CANCELED                                            

  OPS-01    RCA PROCESS  ROT          PU          Shaft         Crack

  ELE-01    NEW          INS          TX          Solenoid      Malfunction
            REGISTERED                                          

  ROT-02    RCA PROCESS  STA          HB          Bearing       High
                                                                Vibration

  ELE-02    CA/PA        STA          RX          Shaft         Crack
            EXECUTION                                           

  REL-02    RCA PROCESS  INS          PZ          Seal          Leakage

  INS-02    MONITORING   INS          SX          Impeller      Worn Out
            RESULT                                              

  ELE-01    RISK CLOSED  ROT          PU          Oil Seal      Leakage

  INS-01    RISK         INS          PZ          Motor         Low
            CANCELED                                            Performance

  ROT-01    NEW          ROT          BL          Gearbox       High
            REGISTERED                                          Vibration

  INS-01    RISK         ROT          FA          Bearing       High
            CANCELED                                            Vibration

  ROT-01    RISK         ROT          PU          Rotor         High
            CANCELED                                            Vibration

  STA-02    CA/PA        STA          CD          Coupling      Loose
            EXECUTION                                           

  INS-01    RISK CLOSED  ROT          BL          Blade         Breakage

  INS-02    RCA PROCESS  INS          VA          Oil Seal      Leakage

  REL-05    MONITORING   ROT          PU          Solenoid      Malfunction
            RESULT                                              

  INS-01    RCA PROCESS  INS          VA          Oil Seal      Leakage

  OPS-01    RCA PROCESS  ROT          TX          Bearing       High
                                                                Vibration

  ROT-03    RISK CLOSED  ROT          BL          Shaft         Crack

  INS-01    RISK         INS          VA          Oil Seal      Leakage
            CANCELED                                            

  OPS-01    CA/PA        ROT          FA          Rotor         High
            EXECUTION                                           Vibration

  ELE-02    RISK CLOSED  ROT          PU          Tube Bundle   Fouling

  INS-01    MONITORING   ROT          BL          Blade         Breakage
            RESULT                                              

  ROT-01    CA/PA        ROT          EM          Mechanical    Leakage
            EXECUTION                             Seal          

  INS-02    RISK CLOSED  STA          CD          Solenoid      Malfunction

  INS-02    CA/PA        STA          RX          Transmitter   Error
            EXECUTION                                           

  ELE-01    RISK CLOSED  ROT          BL          Transmitter   Error

  INS-02    RCA PROCESS  ROT          PU          Gearbox       High
                                                                Vibration

  ROT-03    RISK         ROT          BL          Bearing       Overheat
            CANCELED                                            

  STA-02    CA/PA        ROT          CO          Valve         Leakage
            EXECUTION                                           

  INS-01    RCA PROCESS  INS          VA          Impeller      Worn Out

  INS-02    MONITORING   ELE          SW          Gearbox       High
            RESULT                                              Vibration

  ELE-01    CA/PA        STA          RX          Bearing       Worn Out
            EXECUTION                                           

  ROT-03    RISK CLOSED  ROT          CO          Gearbox       High
                                                                Vibration

  INS-02    RCA PROCESS  ELE          TR          Motor         Low
                                                                Performance

  REL-02    RISK CLOSED  STA          RX          Valve         Stuck

  ELE-01    MONITORING   INS          PZ          Tube Bundle   Fouling
            RESULT                                              

  ELE-02    RCA PROCESS  STA          RX          Oil Seal      Leakage

  OPS-01    CA/PA        ROT          EM          Solenoid      Malfunction
            EXECUTION                                           

  ELE-02    MONITORING   ROT          BL          Transmitter   Error
            RESULT                                              

  ROT-02    CA/PA        ROT          EM          Impeller      Worn Out
            EXECUTION                                           

  OPS-01    CA/PA        INS          TX          Mechanical    Leakage
            EXECUTION                             Seal          

  ROT-01    RCA PROCESS  ROT          BL          Tube Bundle   Fouling

  REL-03    RCA PROCESS  INS          TX          Gasket        Leakage

  INS-02    RISK CLOSED  STA          CD          Coupling      Loose

  STA-02    RISK CLOSED  ROT          BL          Tube Bundle   Fouling

  STA-02    RISK CLOSED  ROT          PU          Motor         Low
                                                                Performance

  REL-03    CA/PA        ELE          SW          Seal          Leakage
            EXECUTION                                           

  REL-03    CA/PA        ROT          TX          Bearing       Overheat
            EXECUTION                                           

  REL-03    CA/PA        STA          CD          Rotor         High
            EXECUTION                                           Vibration

  INS-02    RISK         ELE          EM          Valve         Leakage
            CANCELED                                            

  STA-02    RISK         INS          SX          Solenoid      Malfunction
            CANCELED                                            

  STA-01    RISK CLOSED  ROT          CO          Transmitter   Error

  ELE-02    CA/PA        STA          HB          Solenoid      Malfunction
            EXECUTION                                           

  OPS-01    MONITORING   ELE          TR          Seal          Leakage
            RESULT                                              

  INS-02    CA/PA        STA          TK          Solenoid      Malfunction
            EXECUTION                                           

  REL-02    RISK         ROT          CO          Mechanical    Leakage
            CANCELED                              Seal          

  ELE-01    RISK         INS          TX          Bearing       High
            CANCELED                                            Vibration

  REL-05    MONITORING   ROT          BL          Transmitter   Error
            RESULT                                              

  ROT-02    MONITORING   ROT          BL          Valve         Leakage
            RESULT                                              

  INS-01    MONITORING   ELE          EM          Impeller      Worn Out
            RESULT                                              

  ROT-02    RISK CLOSED  INS          TX          Valve         Leakage

  REL-05    NEW          ROT          PU          Coupling      Worn Out
            REGISTERED                                          

  STA-02    RISK CLOSED  ROT          BL          Tube Bundle   Fouling

  ROT-02    CA/PA        ROT          EM          Rotor         High
            EXECUTION                                           Vibration

  INS-02    CA/PA        ROT          TX          Coupling      Worn Out
            EXECUTION                                           

  ROT-01    RISK CLOSED  STA          HB          Tube Bundle   Fouling

  REL-03    MONITORING   ROT          TX          Coupling      Worn Out
            RESULT                                              

  ELE-01    NEW          STA          TK          Rotor         High
            REGISTERED                                          Vibration

  REL-05    MONITORING   ROT          EM          Valve         Leakage
            RESULT                                              

  REL-03    RISK CLOSED  STA          RX          Valve         Leakage

  REL-02    CA/PA        INS          PZ          Bearing       High
            EXECUTION                                           Vibration

  ROT-02    RCA PROCESS  ROT          PU          Oil Seal      Leakage

  ELE-02    RCA PROCESS  ELE          EM          Valve         Leakage

  STA-01    CA/PA        ELE          TR          Tube Bundle   Fouling
            EXECUTION                                           

  ROT-02    RCA PROCESS  INS          PZ          Motor         Low
                                                                Performance

  STA-01    CA/PA        ROT          TX          Gasket        Leakage
            EXECUTION                                           

  INS-01    RCA PROCESS  STA          TK          Valve         Leakage

  ROT-02    RCA PROCESS  ROT          FA          Motor         Low
                                                                Performance

  REL-03    RISK CLOSED  INS          SX          Oil Seal      Leakage

  ELE-02    MONITORING   STA          HB          Blade         Breakage
            RESULT                                              

  INS-01    RISK         STA          RX          Impeller      Worn Out
            CANCELED                                            

  STA-01    RISK CLOSED  INS          PZ          Motor         Low
                                                                Performance

  ROT-01    RCA PROCESS  STA          CD          Valve         Leakage

  REL-02    RISK         STA          RX          Gasket        Leakage
            CANCELED                                            

  OPS-01    RISK CLOSED  ROT          BL          Blade         Breakage

  INS-02    CA/PA        STA          CD          Coupling      Worn Out
            EXECUTION                                           

  STA-01    MONITORING   STA          RX          Solenoid      Malfunction
            RESULT                                              

  STA-01    RISK CLOSED  ELE          TR          Motor         Low
                                                                Performance

  ROT-01    RCA PROCESS  STA          RX          Bearing       High
                                                                Vibration

  STA-02    MONITORING   INS          PZ          Motor         Low
            RESULT                                              Performance

  ROT-02    RISK         ROT          TX          Valve         Stuck
            CANCELED                                            

  ELE-01    RISK CLOSED  ROT          FA          Seal          Leakage

  STA-02    CA/PA        ELE          SW          Bearing       Overheat
            EXECUTION                                           

  INS-02    RISK CLOSED  ROT          BL          Coupling      Worn Out

  REL-03    RISK CLOSED  ROT          PU          Valve         Leakage

  INS-01    RCA PROCESS  STA          TK          Transmitter   Error

  ROT-01    CA/PA        STA          HB          Shaft         Crack
            EXECUTION                                           

  REL-03    RISK         ELE          SW          Gearbox       High
            CANCELED                                            Vibration

  STA-01    NEW          STA          HB          Gasket        Leakage
            REGISTERED                                          

  INS-01    MONITORING   ROT          EM          Coupling      Worn Out
            RESULT                                              

  ROT-01    RISK         STA          RX          Bearing       Overheat
            CANCELED                                            

  ELE-02    MONITORING   INS          SX          Impeller      Worn Out
            RESULT                                              

  INS-01    MONITORING   INS          SX          Bearing       Overheat
            RESULT                                              

  ROT-03    RISK CLOSED  ROT          CO          Coupling      Worn Out

  OPS-01    RCA PROCESS  INS          PZ          Motor         Low
                                                                Performance

  OPS-01    RISK CLOSED  ROT          BL          Solenoid      Malfunction

  ROT-03    RISK CLOSED  ROT          BL          Motor         Low
                                                                Performance

  REL-05    RISK CLOSED  ELE          SW          Coupling      Loose

  REL-02    MONITORING   ELE          EM          Rotor         High
            RESULT                                              Vibration

  REL-03    CA/PA        INS          PZ          Coupling      Loose
            EXECUTION                                           

  STA-02    RCA PROCESS  ROT          PU          Bearing       Worn Out

  REL-05    CA/PA        ROT          FA          Tube Bundle   Fouling
            EXECUTION                                           

  ROT-03    RISK CLOSED  ELE          SW          Valve         Stuck

  OPS-01    RISK         ROT          FA          Bearing       Overheat
            CANCELED                                            

  STA-01    CA/PA        INS          PZ          Transmitter   Error
            EXECUTION                                           

  REL-03    CA/PA        INS          TX          Gearbox       High
            EXECUTION                                           Vibration

  ROT-03    NEW          ELE          TR          Mechanical    Leakage
            REGISTERED                            Seal          

  ELE-02    RISK CLOSED  ROT          FA          Shaft         Crack

  STA-01    RISK CLOSED  ROT          BL          Valve         Stuck

  STA-02    RISK CLOSED  ROT          PU          Motor         Low
                                                                Performance

  REL-05    NEW          ROT          TX          Seal          Leakage
            REGISTERED                                          

  OPS-01    CA/PA        INS          TX          Bearing       Overheat
            EXECUTION                                           

  INS-02    CA/PA        INS          SX          Tube Bundle   Fouling
            EXECUTION                                           

  ROT-02    CA/PA        ROT          EM          Coupling      Worn Out
            EXECUTION                                           

  ELE-01    MONITORING   ROT          BL          Valve         Leakage
            RESULT                                              

  REL-05    RISK CLOSED  ROT          PU          Rotor         High
                                                                Vibration

  ROT-03    CA/PA        STA          HB          Oil Seal      Leakage
            EXECUTION                                           

  STA-02    CA/PA        INS          SX          Oil Seal      Leakage
            EXECUTION                                           

  INS-01    MONITORING   INS          SX          Bearing       High
            RESULT                                              Vibration

  OPS-01    RISK CLOSED  INS          SX          Bearing       Worn Out

  REL-03    CA/PA        INS          SX          Blade         Breakage
            EXECUTION                                           

  STA-01    NEW          STA          HB          Coupling      Loose
            REGISTERED                                          

  REL-05    RCA PROCESS  INS          VA          Coupling      Loose

  REL-03    CA/PA        ROT          EM          Bearing       High
            EXECUTION                                           Vibration

  ROT-02    RCA PROCESS  STA          HB          Gasket        Leakage

  OPS-01    MONITORING   ROT          TX          Seal          Leakage
            RESULT                                              

  ROT-01    MONITORING   ROT          PU          Tube Bundle   Fouling
            RESULT                                              

  REL-05    RISK CLOSED  ROT          PU          Bearing       High
                                                                Vibration

  INS-02    RISK CLOSED  INS          SX          Oil Seal      Leakage

  REL-02    RISK CLOSED  ELE          EM          Bearing       High
                                                                Vibration

  INS-02    CA/PA        STA          TK          Bearing       High
            EXECUTION                                           Vibration

  REL-05    RISK CLOSED  ROT          PU          Valve         Stuck

  ELE-01    RISK CLOSED  STA          TK          Shaft         Crack

  ELE-02    RISK CLOSED  ELE          SW          Coupling      Worn Out

  OPS-01    RISK CLOSED  ELE          TR          Transmitter   Error

  STA-02    RISK         ROT          FA          Valve         Stuck
            CANCELED                                            

  ELE-02    NEW          INS          TX          Seal          Leakage
            REGISTERED                                          

  STA-02    RCA PROCESS  ROT          TX          Rotor         High
                                                                Vibration

  STA-01    RCA PROCESS  ELE          EM          Bearing       Worn Out

  OPS-01    RISK CLOSED  ROT          EM          Coupling      Loose

  ROT-03    RISK CLOSED  INS          VA          Rotor         High
                                                                Vibration

  OPS-01    RISK CLOSED  STA          CD          Blade         Breakage

  STA-02    RISK CLOSED  ROT          FA          Solenoid      Malfunction

  ROT-01    RISK CLOSED  ROT          CO          Transmitter   Error

  INS-01    RISK CLOSED  ROT          TX          Mechanical    Leakage
                                                  Seal          

  REL-02    RISK CLOSED  STA          CD          Blade         Breakage

  REL-02    CA/PA        STA          RX          Solenoid      Malfunction
            EXECUTION                                           

  OPS-01    CA/PA        ROT          TX          Tube Bundle   Fouling
            EXECUTION                                           

  STA-02    CA/PA        ROT          PU          Coupling      Loose
            EXECUTION                                           

  REL-05    NEW          ROT          CO          Motor         Low
            REGISTERED                                          Performance

  ELE-02    RCA PROCESS  STA          HB          Seal          Leakage

  ROT-02    RISK CLOSED  ROT          BL          Gearbox       High
                                                                Vibration

  ELE-01    RISK         STA          RX          Coupling      Worn Out
            CANCELED                                            

  STA-02    RCA PROCESS  ELE          TR          Gasket        Leakage

  REL-03    RISK CLOSED  INS          TX          Motor         Low
                                                                Performance

  ROT-01    RISK         ELE          EM          Valve         Stuck
            CANCELED                                            

  ROT-02    CA/PA        ELE          SW          Valve         Stuck
            EXECUTION                                           

  ROT-01    RISK CLOSED  INS          TX          Valve         Stuck

  REL-02    CA/PA        ROT          CO          Bearing       Worn Out
            EXECUTION                                           

  STA-01    CA/PA        STA          CD          Blade         Breakage
            EXECUTION                                           

  ELE-01    CA/PA        ROT          TX          Shaft         Crack
            EXECUTION                                           

  ELE-02    RISK         STA          CD          Blade         Breakage
            CANCELED                                            

  INS-02    RISK CLOSED  STA          CD          Blade         Breakage

  REL-05    RCA PROCESS  ROT          BL          Bearing       Worn Out

  REL-03    RISK CLOSED  INS          PZ          Bearing       Worn Out

  ELE-02    RISK CLOSED  INS          PZ          Tube Bundle   Fouling

  STA-01    RCA PROCESS  ELE          EM          Seal          Leakage

  STA-02    RISK CLOSED  ROT          BL          Shaft         Crack

  ELE-01    RISK         INS          PZ          Bearing       Overheat
            CANCELED                                            

  OPS-01    RCA PROCESS  ELE          TR          Impeller      Worn Out

  ROT-03    CA/PA        ELE          SW          Seal          Leakage
            EXECUTION                                           

  REL-03    RISK CLOSED  STA          RX          Transmitter   Error

  INS-01    CA/PA        ELE          TR          Impeller      Worn Out
            EXECUTION                                           

  ROT-02    RISK CLOSED  ROT          BL          Bearing       High
                                                                Vibration

  ELE-01    RCA PROCESS  ROT          CO          Valve         Stuck

  INS-01    MONITORING   ROT          EM          Seal          Leakage
            RESULT                                              

  STA-01    CA/PA        ROT          PU          Coupling      Loose
            EXECUTION                                           

  REL-02    RCA PROCESS  INS          VA          Solenoid      Malfunction

  ROT-03    CA/PA        ROT          CO          Shaft         Crack
            EXECUTION                                           

  OPS-01    RCA PROCESS  STA          CD          Solenoid      Malfunction

  REL-03    RCA PROCESS  STA          CD          Seal          Leakage

  ROT-02    RISK CLOSED  ROT          TX          Solenoid      Malfunction

  STA-01    RISK         ELE          TR          Motor         Low
            CANCELED                                            Performance

  INS-02    RISK CLOSED  STA          TK          Valve         Leakage

  STA-02    RISK         ELE          SW          Blade         Breakage
            CANCELED                                            

  REL-02    RISK CLOSED  STA          CD          Seal          Leakage

  REL-03    CA/PA        STA          HB          Impeller      Worn Out
            EXECUTION                                           

  ELE-01    CA/PA        STA          RX          Shaft         Crack
            EXECUTION                                           

  ROT-03    MONITORING   ROT          PU          Tube Bundle   Fouling
            RESULT                                              

  ELE-02    RISK         ROT          CO          Valve         Leakage
            CANCELED                                            

  ELE-02    RISK CLOSED  INS          SX          Valve         Leakage

  REL-02    NEW          INS          TX          Coupling      Loose
            REGISTERED                                          

  ROT-03    NEW          STA          RX          Bearing       Overheat
            REGISTERED                                          

  INS-01    RISK CLOSED  ELE          EM          Coupling      Loose

  INS-01    CA/PA        STA          CD          Seal          Leakage
            EXECUTION                                           

  STA-01    MONITORING   INS          TX          Oil Seal      Leakage
            RESULT                                              

  ROT-03    RISK         ROT          CO          Blade         Breakage
            CANCELED                                            

  REL-02    CA/PA        STA          HB          Coupling      Loose
            EXECUTION                                           

  ROT-03    RISK         STA          RX          Impeller      Worn Out
            CANCELED                                            

  INS-01    CA/PA        ROT          FA          Shaft         Crack
            EXECUTION                                           

  INS-02    NEW          ROT          PU          Bearing       High
            REGISTERED                                          Vibration

  ROT-01    RISK CLOSED  ELE          TR          Solenoid      Malfunction

  REL-03    RCA PROCESS  STA          RX          Transmitter   Error

  REL-03    CA/PA        STA          HB          Shaft         Crack
            EXECUTION                                           

  ROT-03    RISK CLOSED  ROT          EM          Gearbox       High
                                                                Vibration

  STA-02    RISK         ROT          EM          Seal          Leakage
            CANCELED                                            

  INS-02    MONITORING   ROT          EM          Shaft         Crack
            RESULT                                              

  REL-05    NEW          STA          RX          Transmitter   Error
            REGISTERED                                          

  ROT-01    RISK CLOSED  INS          SX          Shaft         Crack

  ROT-01    RCA PROCESS  INS          TX          Gasket        Leakage

  STA-01    CA/PA        ELE          TR          Bearing       High
            EXECUTION                                           Vibration

  ROT-01    RISK CLOSED  INS          PZ          Seal          Leakage

  REL-03    RISK CLOSED  STA          CD          Gearbox       High
                                                                Vibration

  REL-03    CA/PA        ROT          BL          Oil Seal      Leakage
            EXECUTION                                           

  STA-02    RISK CLOSED  ELE          SW          Bearing       High
                                                                Vibration

  REL-05    RISK CLOSED  ROT          EM          Motor         Low
                                                                Performance

  REL-05    CA/PA        INS          VA          Coupling      Loose
            EXECUTION                                           

  ROT-02    CA/PA        INS          PZ          Blade         Breakage
            EXECUTION                                           

  ELE-02    RCA PROCESS  INS          TX          Gasket        Leakage

  ROT-02    RISK CLOSED  INS          PZ          Coupling      Loose

  INS-01    MONITORING   INS          SX          Bearing       High
            RESULT                                              Vibration

  REL-02    MONITORING   STA          CD          Coupling      Loose
            RESULT                                              

  REL-02    CA/PA        STA          TK          Oil Seal      Leakage
            EXECUTION                                           

  INS-01    NEW          STA          CD          Seal          Leakage
            REGISTERED                                          

  ROT-02    RCA PROCESS  ELE          TR          Oil Seal      Leakage

  STA-02    RISK CLOSED  ELE          SW          Bearing       High
                                                                Vibration

  ELE-02    CA/PA        ROT          TX          Tube Bundle   Fouling
            EXECUTION                                           

  ROT-01    RISK         INS          TX          Bearing       Worn Out
            CANCELED                                            

  ROT-03    RCA PROCESS  ROT          BL          Impeller      Worn Out

  ROT-02    RISK CLOSED  INS          SX          Motor         Low
                                                                Performance

  STA-02    RISK CLOSED  INS          TX          Bearing       Worn Out

  REL-05    RISK CLOSED  STA          HB          Tube Bundle   Fouling

  INS-01    RISK CLOSED  INS          TX          Oil Seal      Leakage

  REL-03    CA/PA        STA          CD          Valve         Leakage
            EXECUTION                                           

  INS-01    RCA PROCESS  ROT          PU          Gasket        Leakage

  INS-01    MONITORING   ELE          EM          Gasket        Leakage
            RESULT                                              

  INS-02    CA/PA        STA          HB          Mechanical    Leakage
            EXECUTION                             Seal          

  INS-02    RISK CLOSED  ROT          PU          Mechanical    Leakage
                                                  Seal          

  INS-02    CA/PA        ROT          CO          Seal          Leakage
            EXECUTION                                           

  ELE-01    RCA PROCESS  ROT          BL          Impeller      Worn Out

  ROT-01    CA/PA        ROT          BL          Tube Bundle   Fouling
            EXECUTION                                           

  REL-05    RISK CLOSED  ROT          CO          Transmitter   Error

  STA-01    RISK CLOSED  INS          TX          Shaft         Crack

  ROT-01    RISK         STA          TK          Tube Bundle   Fouling
            CANCELED                                            

  STA-01    RCA PROCESS  ROT          CO          Coupling      Worn Out

  REL-02    RISK CLOSED  ROT          TX          Gearbox       High
                                                                Vibration

  INS-02    CA/PA        INS          SX          Gasket        Leakage
            EXECUTION                                           

  STA-01    RISK         ROT          CO          Seal          Leakage
            CANCELED                                            

  REL-05    RISK CLOSED  ROT          TX          Gasket        Leakage

  ELE-01    CA/PA        ROT          BL          Rotor         High
            EXECUTION                                           Vibration

  INS-02    RISK         INS          VA          Solenoid      Malfunction
            CANCELED                                            

  STA-02    RISK CLOSED  STA          CD          Coupling      Loose

  ROT-01    MONITORING   INS          PZ          Bearing       High
            RESULT                                              Vibration

  STA-02    CA/PA        ELE          SW          Bearing       Overheat
            EXECUTION                                           

  OPS-01    RISK CLOSED  ELE          EM          Coupling      Worn Out

  ELE-02    RCA PROCESS  ROT          TX          Valve         Leakage

  ELE-01    CA/PA        INS          VA          Rotor         High
            EXECUTION                                           Vibration

  ELE-01    RISK         ROT          FA          Tube Bundle   Fouling
            CANCELED                                            

  ROT-03    RCA PROCESS  STA          CD          Mechanical    Leakage
                                                  Seal          

  ROT-01    RCA PROCESS  ROT          TX          Impeller      Worn Out

  ROT-03    CA/PA        INS          PZ          Seal          Leakage
            EXECUTION                                           

  OPS-01    RISK CLOSED  INS          SX          Bearing       Worn Out

  ROT-01    CA/PA        STA          RX          Blade         Breakage
            EXECUTION                                           

  STA-02    RISK CLOSED  ELE          SW          Shaft         Crack

  ELE-01    RCA PROCESS  STA          HB          Valve         Stuck

  INS-02    RISK         INS          SX          Motor         Low
            CANCELED                                            Performance

  INS-02    RISK CLOSED  INS          TX          Rotor         High
                                                                Vibration

  OPS-01    RCA PROCESS  ROT          PU          Valve         Leakage

  REL-05    RISK CLOSED  INS          PZ          Rotor         High
                                                                Vibration

  ELE-01    RISK CLOSED  ROT          EM          Mechanical    Leakage
                                                  Seal          

  INS-02    CA/PA        ROT          EM          Seal          Leakage
            EXECUTION                                           

  INS-01    CA/PA        ROT          EM          Seal          Leakage
            EXECUTION                                           

  INS-01    CA/PA        STA          CD          Valve         Leakage
            EXECUTION                                           

  STA-01    RISK CLOSED  INS          SX          Oil Seal      Leakage

  OPS-01    RISK         ROT          CO          Solenoid      Malfunction
            CANCELED                                            

  REL-05    RCA PROCESS  ROT          FA          Gearbox       High
                                                                Vibration

  STA-01    RISK CLOSED  STA          HB          Oil Seal      Leakage

  ELE-02    RCA PROCESS  ROT          CO          Oil Seal      Leakage

  ELE-01    RISK CLOSED  ELE          TR          Transmitter   Error

  ROT-01    RISK CLOSED  STA          HB          Motor         Low
                                                                Performance

  REL-03    RCA PROCESS  STA          TK          Coupling      Worn Out

  REL-03    MONITORING   ELE          SW          Oil Seal      Leakage
            RESULT                                              

  ROT-01    RCA PROCESS  ROT          CO          Coupling      Loose

  INS-02    RCA PROCESS  ELE          EM          Gasket        Leakage

  OPS-01    RISK CLOSED  ELE          SW          Oil Seal      Leakage

  OPS-01    RCA PROCESS  STA          TK          Seal          Leakage

  ROT-03    RISK CLOSED  INS          SX          Solenoid      Malfunction

  REL-03    RCA PROCESS  ROT          BL          Solenoid      Malfunction

  ROT-03    CA/PA        ROT          FA          Bearing       Overheat
            EXECUTION                                           

  INS-02    CA/PA        ROT          PU          Transmitter   Error
            EXECUTION                                           

  REL-05    RISK CLOSED  ROT          TX          Oil Seal      Leakage

  REL-02    RCA PROCESS  ROT          PU          Coupling      Worn Out

  ROT-01    MONITORING   STA          CD          Valve         Stuck
            RESULT                                              

  REL-03    RISK CLOSED  ROT          CO          Mechanical    Leakage
                                                  Seal          

  OPS-01    RISK         ELE          TR          Valve         Leakage
            CANCELED                                            

  REL-03    RCA PROCESS  ROT          TX          Shaft         Crack

  ROT-01    CA/PA        ELE          EM          Impeller      Worn Out
            EXECUTION                                           

  INS-02    CA/PA        ROT          FA          Impeller      Worn Out
            EXECUTION                                           

  INS-01    RISK         ROT          CO          Coupling      Worn Out
            CANCELED                                            

  ELE-02    RCA PROCESS  STA          HB          Gasket        Leakage

  ELE-01    CA/PA        ROT          CO          Rotor         High
            EXECUTION                                           Vibration

  ELE-02    RISK CLOSED  ELE          EM          Bearing       High
                                                                Vibration

  REL-03    RISK CLOSED  ELE          TR          Bearing       High
                                                                Vibration

  REL-05    CA/PA        INS          SX          Rotor         High
            EXECUTION                                           Vibration

  REL-02    RCA PROCESS  ELE          SW          Solenoid      Malfunction

  ROT-03    MONITORING   ROT          FA          Solenoid      Malfunction
            RESULT                                              

  STA-02    RISK CLOSED  ELE          SW          Transmitter   Error

  ROT-03    RISK         ROT          FA          Valve         Stuck
            CANCELED                                            

  ROT-02    NEW          ELE          TR          Gearbox       High
            REGISTERED                                          Vibration

  REL-02    NEW          STA          TK          Valve         Leakage
            REGISTERED                                          

  ELE-01    RISK CLOSED  INS          TX          Bearing       Worn Out

  ELE-01    RISK         STA          TK          Coupling      Loose
            CANCELED                                            

  REL-02    RISK         ROT          BL          Blade         Breakage
            CANCELED                                            

  INS-01    RISK         INS          VA          Coupling      Worn Out
            CANCELED                                            

  OPS-01    CA/PA        ELE          TR          Bearing       Overheat
            EXECUTION                                           

  REL-02    NEW          INS          PZ          Motor         Low
            REGISTERED                                          Performance

  INS-02    RISK CLOSED  ELE          EM          Mechanical    Leakage
                                                  Seal          

  ELE-01    RISK         INS          TX          Mechanical    Leakage
            CANCELED                              Seal          

  ROT-01    MONITORING   STA          TK          Mechanical    Leakage
            RESULT                                Seal          

  ELE-02    RISK CLOSED  ROT          BL          Gearbox       High
                                                                Vibration

  REL-03    RCA PROCESS  ROT          CO          Shaft         Crack

  ROT-02    CA/PA        STA          CD          Valve         Leakage
            EXECUTION                                           

  ROT-01    RISK         STA          CD          Gearbox       High
            CANCELED                                            Vibration

  OPS-01    RCA PROCESS  STA          TK          Solenoid      Malfunction

  REL-02    MONITORING   ROT          EM          Shaft         Crack
            RESULT                                              

  ELE-02    RISK CLOSED  ROT          CO          Oil Seal      Leakage
  ---------------------------------------------------------------------------

## 8. Downtime and loss

  --------------------------------------------------------------------------------------
  Downtime   Actual loss (k                  Total    RCA due    Month-Year   
  (hrs)      US$) | Potential loss (k US$)   loss (k  date                    
                                             US\$)                            
  ---------- ------------------------------- -------- ---------- ------------ ----------
  18.50      226.44                          67.93    294.37     2026-04-26   Mar-2026

  32.00      1,584.00                        475.20   2,059.20   2026-06-13   Apr-2026

  8.00       112.00                          33.60    145.60     2026-08-22   Jul-2026

  12.00      183.60                          55.08    238.68     2026-07-05   May-2026

  14.00      478.80                          143.64   622.44     2026-08-01   Jun-2026

  4.70       184.02                          37.55    221.57     2024-06-30   May-2024

  0.00       4.03                            49.98    54.01      2025-05-26   Mar-2025

  1.80       82.03                           24.92    106.95     2025-02-12   Dec-2024

  0.00       0.51                            0.00     0.51       n/a          Jun-2026

  8.40       415.26                          39.99    455.25     2025-06-25   Apr-2025

  1.30       26.75                           0.00     26.75      n/a          Dec-2025

  17.30      722.50                          12.94    735.44     2025-05-22   Apr-2025

  8.30       131.83                          29.03    160.86     2025-04-10   Mar-2025

  0.00       3.45                            0.00     3.45       n/a          Sep-2025

  2.10       48.62                           0.00     48.62      n/a          May-2024

  5.20       124.25                          0.00     124.25     n/a          Jun-2025

  0.80       20.66                           9.77     30.43      2024-06-03   May-2024

  12.50      187.39                          0.00     187.39     n/a          Oct-2025

  10.70      254.95                          0.00     254.95     n/a          Jun-2025

  2.10       32.78                           17.60    50.38      2026-04-25   Mar-2026

  22.90      596.79                          39.08    635.87     2025-01-25   Dec-2024

  0.00       4.33                            0.00     4.33       n/a          Apr-2024

  0.00       3.57                            1.90     5.47       2024-10-20   Sep-2024

  5.20       118.19                          0.00     118.19     n/a          Aug-2025

  0.20       6.14                            0.00     6.14       n/a          Oct-2024

  19.60      352.95                          1.42     354.37     2024-06-30   May-2024

  5.00       135.61                          0.00     135.61     n/a          Dec-2025

  33.00      781.28                          33.96    815.24     2026-07-05   Jun-2026

  5.90       180.34                          29.03    209.37     2026-03-19   Feb-2026

  8.90       164.35                          5.04     169.39     2024-07-06   Jun-2024

  3.90       64.66                           19.46    84.12      2025-08-29   Jun-2025

  4.00       144.69                          0.00     144.69     n/a          Sep-2024

  6.60       188.20                          42.10    230.30     2025-04-07   Mar-2025

  0.00       4.55                            6.05     10.60      2025-08-12   Jun-2025

  0.00       1.66                            0.00     1.66       n/a          Nov-2025

  1.30       36.72                           0.00     36.72      n/a          Jul-2026

  6.60       185.15                          0.00     185.15     n/a          Mar-2025

  7.40       189.63                          38.36    227.99     2025-02-03   Dec-2024

  12.80      232.98                          32.22    265.20     2026-06-25   May-2026

  3.90       91.53                           0.00     91.53      n/a          May-2026

  8.10       126.49                          0.00     126.49     n/a          Jan-2025

  5.90       207.20                          17.18    224.38     2026-02-12   Dec-2025

  0.50       15.97                           0.00     15.97      n/a          Sep-2025

  2.00       66.02                           0.00     66.02      n/a          Aug-2025

  12.60      477.89                          23.19    501.08     2024-12-21   Nov-2024

  0.00       2.70                            7.60     10.30      2025-05-14   Mar-2025

  2.60       60.59                           34.65    95.24      2024-06-26   May-2024

  10.00      265.81                          7.28     273.09     2025-12-27   Nov-2025

  11.10      375.48                          12.06    387.54     2024-04-14   Feb-2024

  0.00       4.39                            0.00     4.39       n/a          Aug-2024

  8.60       97.64                           0.00     97.64      n/a          Aug-2024

  1.60       60.91                           0.00     60.91      n/a          Oct-2025

  0.00       2.73                            39.82    42.55      2025-08-26   Jul-2025

  2.10       74.72                           0.00     74.72      n/a          Apr-2026

  0.80       32.47                           0.00     32.47      n/a          Jan-2024

  9.30       251.02                          12.46    263.48     2026-06-26   May-2026

  7.20       283.87                          0.00     283.87     n/a          Mar-2025

  8.60       159.38                          40.39    199.77     2025-01-01   Nov-2024

  7.00       149.58                          0.00     149.58     n/a          Feb-2025

  5.90       69.72                           8.42     78.14      2025-08-28   Jul-2025

  0.00       4.10                            27.08    31.18      2024-11-26   Oct-2024

  7.80       188.85                          0.00     188.85     n/a          Mar-2024

  1.20       41.85                           0.00     41.85      n/a          Oct-2025

  11.10      269.32                          4.16     273.48     2026-02-02   Dec-2025

  16.90      428.84                          0.00     428.84     n/a          Aug-2025

  0.00       0.02                            0.00     0.02       n/a          Dec-2024

  14.90      238.73                          22.19    260.92     2025-08-08   Jun-2025

  8.00       90.86                           0.00     90.86      n/a          Mar-2025

  9.80       271.52                          27.45    298.97     2024-12-27   Oct-2024

  0.00       2.22                            0.00     2.22       n/a          Jan-2025

  0.00       1.43                            33.24    34.67      2026-01-27   Nov-2025

  0.50       11.14                           0.00     11.14      n/a          Dec-2024

  5.10       57.99                           49.09    107.08     2026-03-01   Jan-2026

  11.00      308.72                          32.18    340.90     2025-05-13   Apr-2025

  19.90      792.07                          0.00     792.07     n/a          Jun-2026

  3.40       117.37                          35.64    153.01     2024-06-13   May-2024

  0.00       0.41                            0.00     0.41       n/a          Dec-2024

  6.30       178.88                          36.92    215.80     2024-10-27   Sep-2024

  1.80       59.72                           0.00     59.72      n/a          Dec-2025

  5.30       203.75                          0.00     203.75     n/a          Jan-2026

  32.90      792.32                          39.66    831.98     2025-02-20   Jan-2025

  4.10       105.01                          33.79    138.80     2026-04-28   Feb-2026

  0.00       2.20                            0.00     2.20       n/a          Feb-2024

  0.00       0.82                            19.86    20.68      2026-07-02   May-2026

  3.20       57.20                           7.96     65.16      2025-04-27   Feb-2025

  4.00       72.96                           9.72     82.68      2024-12-28   Oct-2024

  4.50       75.69                           29.40    105.09     2025-09-12   Jul-2025

  0.00       3.59                            0.00     3.59       n/a          Jan-2025

  14.80      273.07                          0.00     273.07     n/a          Feb-2024

  8.70       180.74                          0.00     180.74     n/a          Dec-2025

  4.90       143.88                          3.11     146.99     2024-05-21   Apr-2024

  0.00       0.20                            7.29     7.49       2024-09-08   Jul-2024

  8.80       94.61                           37.00    131.61     2024-06-02   May-2024

  2.60       58.79                           0.00     58.79      n/a          Feb-2025

  2.30       59.56                           0.00     59.56      n/a          Jan-2025

  5.90       261.14                          0.00     261.14     n/a          Jan-2026

  0.00       0.60                            34.29    34.89      2026-08-24   Jun-2026

  0.00       1.39                            0.00     1.39       n/a          Jun-2026

  6.00       230.09                          27.96    258.05     2026-03-09   Feb-2026

  0.60       24.35                           0.00     24.35      n/a          Jan-2026

  3.00       136.82                          0.00     136.82     n/a          Aug-2024

  7.40       253.74                          0.00     253.74     n/a          May-2026

  13.90      462.84                          0.00     462.84     n/a          Jan-2024

  10.80      311.94                          0.00     311.94     n/a          Jul-2026

  5.00       245.69                          0.00     245.69     n/a          Sep-2025

  4.10       145.00                          41.19    186.19     2025-07-23   Jun-2025

  3.20       85.73                           0.00     85.73      n/a          Sep-2024

  4.90       122.37                          28.63    151.00     2024-11-16   Sep-2024

  9.30       189.30                          34.61    223.91     2026-05-21   Mar-2026

  6.60       154.34                          0.00     154.34     n/a          Mar-2026

  10.30      243.87                          0.00     243.87     n/a          Feb-2024

  11.50      140.35                          0.99     141.34     2025-03-26   Feb-2025

  4.20       66.64                           0.00     66.64      n/a          Feb-2026

  0.00       1.13                            0.00     1.13       n/a          Jan-2026

  0.00       0.21                            45.91    46.12      2025-11-06   Oct-2025

  0.00       4.11                            40.39    44.50      2024-07-12   May-2024

  4.80       67.97                           47.08    115.05     2024-06-27   Apr-2024

  9.20       340.38                          15.25    355.63     2026-05-09   Apr-2026

  0.00       4.43                            15.52    19.95      2024-12-04   Oct-2024

  18.40      594.02                          47.42    641.44     2025-03-19   Feb-2025

  19.10      449.03                          31.19    480.22     2025-02-09   Dec-2024

  6.10       249.18                          49.49    298.67     2025-03-16   Feb-2025

  3.10       114.68                          0.00     114.68     n/a          May-2025

  5.70       158.25                          0.00     158.25     n/a          Aug-2025

  0.00       3.14                            0.00     3.14       n/a          Apr-2024

  4.90       98.68                           0.00     98.68      n/a          Sep-2025

  0.00       1.86                            47.73    49.59      2024-11-20   Oct-2024

  2.40       36.51                           0.00     36.51      n/a          Nov-2024

  14.70      323.93                          0.00     323.93     n/a          Jan-2026

  16.30      257.59                          24.38    281.97     2024-03-14   Jan-2024

  3.30       93.35                           0.00     93.35      n/a          Jun-2024

  5.30       136.28                          0.00     136.28     n/a          Mar-2025

  0.00       3.89                            46.47    50.36      2024-09-30   Aug-2024

  7.50       234.65                          0.00     234.65     n/a          Mar-2024

  0.00       2.75                            0.00     2.75       n/a          Oct-2025

  24.20      839.88                          0.00     839.88     n/a          Jul-2026

  0.70       24.12                           25.07    49.19      2025-09-16   Aug-2025

  23.60      945.87                          0.00     945.87     n/a          Jan-2025

  7.30       199.93                          0.00     199.93     n/a          Sep-2024

  8.60       189.71                          22.18    211.89     2025-09-05   Jul-2025

  16.10      578.12                          32.56    610.68     2025-08-14   Jun-2025

  2.80       117.16                          0.00     117.16     n/a          Sep-2024

  3.90       142.19                          14.80    156.99     2026-02-16   Jan-2026

  3.00       122.93                          0.00     122.93     n/a          Jul-2024

  0.80       23.53                           0.00     23.53      n/a          Mar-2025

  0.00       3.39                            0.00     3.39       n/a          Oct-2025

  4.60       69.21                           0.00     69.21      n/a          Dec-2025

  12.50      298.21                          0.00     298.21     n/a          Jul-2024

  15.00      299.22                          10.69    309.91     2024-04-13   Feb-2024

  4.90       102.88                          0.00     102.88     n/a          Jul-2024

  5.00       90.36                           0.00     90.36      n/a          Jun-2025

  6.10       196.28                          0.00     196.28     n/a          Feb-2026

  2.60       94.20                           0.00     94.20      n/a          Jun-2024

  0.00       1.82                            47.58    49.40      2025-12-13   Oct-2025

  0.40       18.34                           30.61    48.95      2024-12-01   Nov-2024

  17.40      245.95                          1.81     247.76     2024-04-04   Feb-2024

  0.80       14.82                           0.00     14.82      n/a          Nov-2024

  0.00       3.47                            0.00     3.47       n/a          Sep-2024

  0.00       3.01                            45.06    48.07      2024-07-09   May-2024

  1.80       36.65                           22.16    58.81      2026-07-28   Jun-2026

  4.10       117.17                          38.75    155.92     2025-02-22   Jan-2025

  1.60       37.89                           0.00     37.89      n/a          Feb-2025

  2.70       123.74                          0.00     123.74     n/a          May-2025

  6.80       252.40                          0.00     252.40     n/a          Mar-2026

  0.00       4.58                            4.39     8.97       2024-08-01   Jun-2024

  0.00       2.24                            24.94    27.18      2025-02-04   Dec-2024

  2.20       58.88                           23.31    82.19      2024-04-03   Feb-2024

  0.00       1.24                            21.94    23.18      2026-02-08   Dec-2025

  0.00       0.07                            0.00     0.07       n/a          Apr-2024

  10.90      211.78                          0.00     211.78     n/a          Nov-2024

  0.00       4.75                            10.03    14.78      2026-01-13   Nov-2025

  5.70       225.91                          21.45    247.36     2024-04-26   Mar-2024

  15.90      432.70                          0.00     432.70     n/a          Mar-2025

  12.00      502.89                          0.00     502.89     n/a          Mar-2025

  13.00      363.73                          12.68    376.41     2024-04-01   Feb-2024

  0.00       4.94                            43.29    48.23      2024-12-14   Nov-2024

  12.00      223.21                          26.41    249.62     2025-02-07   Dec-2024

  7.80       135.14                          35.04    170.18     2026-06-05   Apr-2026

  14.60      484.54                          31.38    515.92     2025-09-17   Aug-2025

  0.00       1.36                            0.00     1.36       n/a          Dec-2025

  2.40       91.92                           0.00     91.92      n/a          Apr-2024

  9.10       185.25                          0.00     185.25     n/a          Mar-2024

  5.00       66.49                           0.00     66.49      n/a          Jun-2026

  0.00       0.80                            0.00     0.80       n/a          May-2024

  0.00       3.89                            15.61    19.50      2026-06-18   May-2026

  13.70      476.28                          0.00     476.28     n/a          Apr-2026

  4.90       123.12                          0.00     123.12     n/a          Aug-2025

  0.00       0.22                            0.00     0.22       n/a          Mar-2024

  20.70      361.66                          0.00     361.66     n/a          Dec-2024

  0.70       33.14                           0.00     33.14      n/a          Feb-2024

  21.20      415.07                          29.92    444.99     2024-02-29   Jan-2024

  11.70      209.16                          35.30    244.46     2025-02-19   Jan-2025

  8.50       221.96                          31.28    253.24     2025-06-16   Apr-2025

  5.70       241.36                          0.00     241.36     n/a          Jun-2026

  6.00       160.26                          0.00     160.26     n/a          Aug-2024

  0.00       3.92                            0.00     3.92       n/a          Oct-2024

  8.20       148.14                          0.00     148.14     n/a          Feb-2024

  7.30       97.94                           0.00     97.94      n/a          Apr-2025

  3.00       51.81                           0.00     51.81      n/a          Feb-2024

  4.70       78.97                           0.00     78.97      n/a          Jun-2024

  0.70       18.30                           42.93    61.23      2024-02-05   Jan-2024

  0.00       2.30                            13.73    16.03      2024-09-20   Aug-2024

  1.80       68.53                           29.95    98.48      2024-10-06   Sep-2024

  20.70      609.41                          9.79     619.20     2026-05-23   Apr-2026

  0.00       0.50                            7.63     8.13       2025-03-04   Jan-2025

  5.60       210.93                          0.00     210.93     n/a          Jan-2024

  1.00       28.41                           0.00     28.41      n/a          Dec-2024

  1.00       19.33                           15.57    34.90      2024-07-12   May-2024

  0.50       9.90                            0.00     9.90       n/a          Jun-2025

  0.00       2.68                            0.00     2.68       n/a          Aug-2025

  2.90       123.13                          33.72    156.85     2025-11-24   Oct-2025

  11.60      265.93                          0.00     265.93     n/a          Jul-2024

  5.30       97.34                           34.85    132.19     2025-06-09   Apr-2025

  0.00       4.28                            25.11    29.39      2026-06-21   May-2026

  0.00       2.96                            15.74    18.70      2025-11-14   Oct-2025

  1.80       64.35                           0.00     64.35      n/a          Jul-2024

  1.90       49.25                           0.00     49.25      n/a          Apr-2024

  11.10      262.13                          13.07    275.20     2025-05-13   Mar-2025

  4.20       193.09                          0.00     193.09     n/a          Sep-2024

  9.60       295.30                          0.00     295.30     n/a          Jul-2026

  9.20       121.06                          13.69    134.75     2024-11-03   Oct-2024

  13.60      417.52                          0.00     417.52     n/a          Oct-2024

  0.00       4.89                            0.00     4.89       n/a          Oct-2025

  3.90       114.55                          4.61     119.16     2026-08-06   Jun-2026

  0.00       0.99                            23.09    24.08      2025-04-11   Feb-2025

  7.80       286.80                          0.00     286.80     n/a          Jul-2024

  14.60      339.26                          48.12    387.38     2026-06-05   Apr-2026

  2.70       66.07                           0.00     66.07      n/a          Nov-2025

  0.00       3.27                            19.37    22.64      2024-07-16   Jun-2024

  0.00       2.84                            0.00     2.84       n/a          Jan-2026

  8.20       338.46                          43.09    381.55     2024-10-23   Aug-2024

  7.30       81.87                           43.92    125.79     2025-04-21   Mar-2025

  9.80       235.19                          21.29    256.48     2025-12-20   Nov-2025

  0.00       2.31                            41.88    44.19      2025-07-01   May-2025

  4.90       223.72                          8.74     232.46     2026-07-08   May-2026

  7.30       142.83                          0.00     142.83     n/a          Oct-2025

  2.60       61.25                           0.00     61.25      n/a          Jun-2024

  4.30       90.29                           0.00     90.29      n/a          Oct-2025

  4.00       77.16                           0.00     77.16      n/a          May-2024

  17.80      455.22                          0.00     455.22     n/a          Dec-2024

  4.10       86.85                           19.67    106.52     2026-05-12   Mar-2026

  1.50       31.26                           20.85    52.11      2026-01-14   Dec-2025

  5.40       138.55                          0.00     138.55     n/a          Dec-2025

  0.90       30.85                           0.00     30.85      n/a          Feb-2026

  6.10       183.51                          0.00     183.51     n/a          Apr-2024

  0.00       1.55                            6.58     8.13       2024-10-31   Sep-2024

  1.00       39.51                           41.06    80.57      2026-07-15   May-2026

  0.00       5.00                            0.00     5.00       n/a          Feb-2025

  0.00       1.39                            45.72    47.11      2025-09-13   Aug-2025

  21.30      578.18                          0.00     578.18     n/a          Jun-2024

  2.10       62.14                           0.00     62.14      n/a          May-2026

  0.00       4.61                            18.99    23.60      2025-06-12   May-2025

  0.90       25.54                           0.00     25.54      n/a          Feb-2026

  26.70      825.31                          31.96    857.27     2025-10-10   Aug-2025

  0.00       0.44                            25.93    26.37      2025-03-08   Feb-2025

  0.00       1.87                            0.00     1.87       n/a          Jul-2025

  7.40       189.06                          13.99    203.05     2024-08-24   Jul-2024

  0.00       2.32                            31.15    33.47      2025-02-04   Dec-2024

  10.30      398.34                          0.00     398.34     n/a          Apr-2026

  2.40       80.20                           0.00     80.20      n/a          May-2026

  11.00      353.42                          0.00     353.42     n/a          Apr-2024

  6.70       231.37                          30.57    261.94     2025-08-01   Jul-2025

  15.60      524.53                          0.00     524.53     n/a          Feb-2024

  0.00       1.46                            43.44    44.90      2025-02-21   Jan-2025

  6.30       91.89                           26.95    118.84     2025-07-13   Jun-2025

  2.20       53.40                           0.00     53.40      n/a          Jan-2026

  3.30       124.37                          0.00     124.37     n/a          Aug-2024

  5.20       98.11                           4.31     102.42     2026-08-02   Jun-2026

  3.60       140.67                          0.00     140.67     n/a          Jun-2025

  4.10       59.06                           0.00     59.06      n/a          Mar-2025

  9.70       443.01                          43.78    486.79     2026-04-01   Mar-2026

  13.60      507.96                          38.94    546.90     2025-01-13   Nov-2024

  0.00       2.72                            44.01    46.73      2026-05-03   Mar-2026

  7.10       162.58                          0.00     162.58     n/a          Jul-2024

  8.10       363.97                          0.00     363.97     n/a          Apr-2024

  2.70       50.72                           0.00     50.72      n/a          Mar-2024

  0.00       4.22                            42.75    46.97      2025-02-06   Dec-2024

  4.90       173.77                          29.04    202.81     2024-09-25   Aug-2024

  20.90      327.09                          25.85    352.94     2025-01-31   Dec-2024

  6.00       97.86                           0.00     97.86      n/a          May-2026

  9.10       250.26                          36.26    286.52     2025-03-24   Jan-2025

  0.00       1.84                            0.00     1.84       n/a          Mar-2024

  15.50      231.00                          1.32     232.32     2025-03-28   Feb-2025

  1.60       67.99                           0.00     67.99      n/a          Mar-2026

  10.20      299.80                          0.00     299.80     n/a          May-2024

  13.60      522.62                          0.00     522.62     n/a          Jul-2026

  1.70       78.81                           0.00     78.81      n/a          Aug-2025

  5.10       161.04                          8.69     169.73     2024-07-25   Jun-2024

  4.00       75.93                           49.15    125.08     2024-03-11   Feb-2024

  3.60       85.73                           0.00     85.73      n/a          Apr-2025

  0.00       0.08                            0.66     0.74       2024-06-18   May-2024

  5.80       123.89                          0.00     123.89     n/a          Dec-2025

  3.60       65.32                           23.70    89.02      2025-02-23   Jan-2025

  6.80       115.23                          20.02    135.25     2024-12-06   Oct-2024

  11.20      211.03                          18.88    229.91     2024-05-13   Mar-2024

  6.80       292.65                          0.00     292.65     n/a          Sep-2025

  32.60      972.43                          0.00     972.43     n/a          Mar-2025

  0.00       0.23                            0.00     0.23       n/a          Mar-2024

  1.30       42.33                           27.03    69.36      2026-07-17   May-2026

  3.90       155.75                          0.00     155.75     n/a          May-2025

  0.60       27.59                           39.08    66.67      2025-10-29   Sep-2025

  1.00       32.29                           0.00     32.29      n/a          Sep-2025

  9.90       198.13                          0.00     198.13     n/a          Dec-2025

  13.50      305.47                          30.02    335.49     2025-11-15   Sep-2025

  1.50       26.17                           0.00     26.17      n/a          Jan-2024

  10.90      453.32                          0.00     453.32     n/a          Feb-2026

  2.80       111.48                          0.00     111.48     n/a          Jan-2025

  7.10       109.38                          18.00    127.38     2026-05-31   Apr-2026

  2.60       64.37                           0.00     64.37      n/a          Oct-2025

  1.30       43.78                           23.29    67.07      2024-09-22   Aug-2024

  12.60      432.74                          31.84    464.58     2025-11-18   Oct-2025

  2.00       46.40                           0.00     46.40      n/a          Aug-2025

  22.80      390.18                          5.52     395.70     2024-06-07   May-2024

  8.50       170.70                          11.75    182.45     2024-12-09   Nov-2024

  0.00       2.33                            4.73     7.06       2025-06-21   Apr-2025

  12.30      353.15                          0.00     353.15     n/a          Oct-2024

  8.80       324.52                          30.91    355.43     2025-02-06   Jan-2025

  10.60      361.23                          0.00     361.23     n/a          Dec-2025

  7.10       317.83                          11.53    329.36     2025-02-10   Dec-2024

  0.00       3.51                            0.00     3.51       n/a          Jan-2025

  0.00       3.00                            0.00     3.00       n/a          May-2024

  2.60       84.19                           38.50    122.69     2025-08-05   Jun-2025

  7.80       100.42                          0.00     100.42     n/a          Apr-2024

  1.90       81.40                           0.00     81.40      n/a          Aug-2025

  0.00       3.56                            16.16    19.72      2024-12-20   Nov-2024

  0.00       1.29                            7.51     8.80       2025-11-17   Oct-2025

  1.60       60.32                           29.73    90.05      2025-06-16   May-2025

  6.50       231.99                          0.00     231.99     n/a          Dec-2025

  0.20       3.99                            0.00     3.99       n/a          May-2026

  3.80       87.05                           31.30    118.35     2025-10-20   Aug-2025

  14.60      565.97                          0.00     565.97     n/a          Feb-2026

  0.00       3.10                            11.39    14.49      2024-06-19   Apr-2024

  10.90      312.26                          0.00     312.26     n/a          Nov-2024

  4.60       53.94                           0.00     53.94      n/a          Dec-2025

  1.10       50.73                           10.66    61.39      2026-08-30   Jul-2026

  5.00       80.64                           0.00     80.64      n/a          Sep-2025

  0.00       0.48                            18.01    18.49      2026-07-04   May-2026

  8.40       399.71                          12.32    412.03     2026-03-15   Jan-2026

  0.00       0.84                            0.00     0.84       n/a          Jul-2024

  14.30      367.00                          39.74    406.74     2024-06-24   Apr-2024

  12.40      186.57                          0.00     186.57     n/a          Oct-2024

  5.30       163.04                          41.97    205.01     2025-12-19   Oct-2025

  15.60      571.56                          46.68    618.24     2025-04-25   Mar-2025

  7.10       104.63                          37.56    142.19     2026-06-18   May-2026

  7.30       242.47                          0.00     242.47     n/a          Oct-2024

  4.40       66.98                           3.93     70.91      2026-05-05   Mar-2026

  8.10       120.73                          0.00     120.73     n/a          Dec-2024

  5.20       107.30                          0.00     107.30     n/a          Aug-2024

  0.10       2.68                            0.00     2.68       n/a          May-2026

  2.10       29.99                           19.26    49.25      2026-05-23   Apr-2026

  14.00      641.11                          28.47    669.58     2025-01-05   Nov-2024

  7.50       249.40                          0.95     250.35     2026-04-22   Feb-2026

  1.30       25.40                           0.00     25.40      n/a          Aug-2024

  5.70       167.55                          23.62    191.17     2026-05-26   Apr-2026

  14.20      408.81                          41.81    450.62     2024-11-09   Oct-2024

  4.80       219.03                          0.00     219.03     n/a          May-2025

  2.20       83.98                           0.00     83.98      n/a          Apr-2025

  3.90       108.27                          34.79    143.06     2026-08-20   Jul-2026

  3.70       104.65                          33.19    137.84     2026-07-10   May-2026

  17.80      438.51                          0.00     438.51     n/a          Feb-2025

  5.30       148.37                          0.00     148.37     n/a          Aug-2025

  5.40       121.65                          0.00     121.65     n/a          Sep-2025

  20.40      617.14                          18.50    635.64     2025-07-27   May-2025

  7.60       143.85                          21.64    165.49     2025-09-30   Aug-2025

  0.00       0.37                            0.00     0.37       n/a          Apr-2025

  0.40       8.87                            0.00     8.87       n/a          Sep-2025

  0.40       10.69                           0.00     10.69      n/a          May-2026

  0.70       30.80                           0.00     30.80      n/a          Mar-2026

  9.50       263.08                          37.59    300.67     2024-03-20   Feb-2024

  0.00       1.68                            6.12     7.80       2024-06-27   May-2024

  3.40       66.23                           0.00     66.23      n/a          Dec-2025

  1.60       65.91                           0.00     65.91      n/a          May-2026

  9.60       324.31                          0.00     324.31     n/a          Jun-2025

  12.20      465.39                          0.00     465.39     n/a          Apr-2026

  6.80       150.88                          35.69    186.57     2026-06-02   Apr-2026

  3.40       116.52                          5.62     122.14     2025-11-23   Oct-2025

  1.00       36.82                           0.00     36.82      n/a          May-2024

  0.00       2.23                            26.07    28.30      2026-01-02   Nov-2025

  0.00       1.16                            0.00     1.16       n/a          Jun-2024

  0.00       0.99                            0.00     0.99       n/a          Jun-2024
  --------------------------------------------------------------------------------------

## 9. Normalized incident master schema

For analysis, the incident-related sections can be joined by row order,
with the serial number as the primary row identifier. The intended
normalized fields are:

  ---------------------------------------------------------------------
  Field group                        Fields
  ---------------------------------- ----------------------------------
  Identity                           Serial No., MTO No., AR No.,
                                     Plant, Tag Number, Equipment Class

  Risk                               Occurrence date, Risk case title,
                                     Highest impact, Pre-risk level,
                                     Pre-risk score

  RCA                                PIC, Overall status, Discipline,
                                     Equipment type, Component, Failure
                                     mechanism

  Loss                               Downtime, Actual loss, Potential
                                     loss, Total loss, RCA due date,
                                     Month-Year

  Condition monitoring               Week, date, monitored parameters,
                                     health status

  Equipment performance              Timestamp, feed, discharge
                                     pressure, vibration, temperature,
                                     motor ampere, plant rate, run
                                     status
  ---------------------------------------------------------------------

## 10. Source notes

-   The source PDF is 233 pages long.

-   Hourly raw-data blocks occupy pages 1-169.

-   Condition-monitoring records occupy pages 171-195.

-   The incident dashboard is on page 196.

-   The 380-row incident register begins on page 198.

-   Risk-case data begins on page 207.

-   RCA status and failure mechanism data begins on page 216.

-   Downtime and loss data begins on page 225.

-   Values such as `n/a`, `ON`, `OFF`, `NORMAL`, `ALARM`, and `TRIP` are
    retained from the source.

# Appendix D. Complete Consensus research notes and bibliography

## **1. Empirical impact of AI predictive maintenance and AI-assisted RCA**

In petrochemical and continuous-process environments, predictive
maintenance has been associated with earlier fault detection, lower
unplanned downtime, better equipment availability, and lower maintenance
burden. However, the academic literature is much stronger on
fault-prediction accuracy than on controlled plant-level measurements of
MTTR and total maintenance cost. A 2020 review covering machine-learning
predictive maintenance describes the main operational objective as
automated fault detection and diagnosis to minimize downtime, increase
equipment utilization, and extend remaining useful life. 1

For manufacturing systems, Shahin et al. evaluated more than 20 ML and
DL models for early failure detection. Deep Forest and Gradient Boosting
exceeded 90 percent average accuracy, while logistic regression and LSTM
exceeded 80 percent. This is useful evidence that AI can detect
developing failure states early enough to support maintenance
intervention, although the study used a synthetic predictive-maintenance
dataset, so it should not be interpreted as a measured percentage
reduction in plant downtime. 2

There is more directly relevant petrochemical evidence from Steurtewagen
and van den Poel. Their work used XGBoost with sensor data and
maintenance reports in the petrochemical context and specifically
addressed the diagnostic problem, rather than only predicting whether a
failure would occur. They used Shapley-value interpretation to identify
variables contributing to predicted failures, which is relevant to
AI-assisted root cause analysis because the output can be translated
into hypotheses about why the machinery is deteriorating. 3

A 2026 petrochemical study is even more explicitly multi-sensor. Liu,
Zhang, and Shi combine vibration, temperature, and electrical-current
data with wavelet packet features and an LSTM-based model. Their
reported classification accuracy was 99.50 percent. This demonstrates
strong diagnostic performance in the reported experiment, although
accuracy is not the same metric as downtime reduction, MTTR reduction,
or maintenance-cost reduction. 4

One 2025 study in fertilizer manufacturing reported 30.5 percent lower
MTTR, 18.4 percent lower cost of maintenance, and a 25 percent increase
in MTBF, with OEE increasing from 77.6 to 83.7 percent. This is one of
the more useful empirical datapoints for your business case because
fertilizer manufacturing is operationally closer to continuous-process
petrochemical production than many generic discrete-manufacturing case
studies. The important qualification is that the paper evaluated a
broader data-driven maintenance and workforce framework, so these
numbers should not be attributed solely to an AI predictive-maintenance
model. 5

A 2021 oil-industry study proposed a smart predictive-maintenance
architecture for refinery operations and reported a technical and
economic feasibility assessment. Its contribution is primarily the
operating model, continuous diagnostics, failure-probability estimation,
and maintenance-time prediction. It does not provide a controlled
before-and-after percentage reduction in downtime that would justify
claiming a specific universal reduction. 6

### **What this means for a petrochemical business case**

A defensible evidence hierarchy is:

  -----------------------------------------------------------------------
  KPI                                 What the literature supports
  ----------------------------------- -----------------------------------
  Fault detection accuracy            Often very high in controlled
                                      studies, including \>90 percent for
                                      several ML models and 99.5 percent
                                      in one recent petrochemical
                                      multi-sensor study. \[2\]\[4\]

  Unplanned downtime                  Directionally supported, because
                                      earlier fault detection creates an
                                      opportunity to intervene before
                                      functional failure. \[1\]\[2\]\[6\]

  MTTR                                Empirical reductions have been
                                      reported in industrial maintenance
                                      studies, including 30.5 percent in
                                      a fertilizer manufacturing case,
                                      but this is not a universal AI
                                      effect. \[5\]

  Maintenance cost                    Reductions are reported in
                                      industrial case studies, including
                                      18.4 percent in the fertilizer
                                      study, but attribution to AI alone
                                      is uncertain. \[5\]

  MTBF                                Improvement has been reported in
                                      industrial data-driven maintenance
                                      implementations, including 25
                                      percent in the cited fertilizer
                                      case. \[5\]

  AI-driven RCA                       Evidence supports improved
                                      diagnostic interpretability and
                                      root-cause support, particularly
                                      when sensor data are combined with
                                      maintenance reports. \[3\]
  -----------------------------------------------------------------------

So, for an investment or transformation proposal, I would **not** claim
something such as "AI will reduce downtime by 30 percent" unless you
have a plant-specific baseline and intervention study. A stronger
formulation is that the literature demonstrates a credible pathway from
earlier fault detection to reduced unplanned downtime and maintenance
effort, with individual industrial studies reporting meaningful MTTR and
cost improvements.

------------------------------------------------------------------------

# **2. Detectable early-warning window for journal-bearing distress and coupling misalignment**

This is where I need to be more careful.

I cannot confirm from the Consensus results currently available a
robust, peer-reviewed universal number such as "journal-bearing distress
can be predicted 14 days in advance" or "coupling misalignment can be
detected 72 hours in advance."

The reason is that **warning time is not a fixed property of the
fault**. It depends strongly on:

-   severity and rate of degradation,\
-   rotational speed and load,\
-   bearing design and clearance,\
-   lubrication regime,\
-   sensor locations and sampling rate,\
-   vibration signal quality,\
-   oil contamination mechanism,\
-   threshold definition,\
-   and whether the target is incipient abnormality, alarm, or imminent
    functional failure.

For journal bearings, multi-sensor systems are especially valuable
because vibration can identify changes in the machine's dynamic response
while oil monitoring can provide evidence of lubrication degradation,
wear particles, viscosity change, or contamination. The combination can
therefore increase the probability of detecting a developing problem
before a catastrophic event. The 2026 petrochemical study provides
direct evidence for the value of combining vibration with temperature
and electrical-current measurements, although it does not establish a
universal lead time before bearing failure. 4

For coupling misalignment, vibration analysis is generally more directly
diagnostic than lubricant analysis because misalignment is fundamentally
a mechanical alignment problem. Oil contamination can be useful as a
corroborating condition indicator, particularly when misalignment
produces abnormal loading and secondary wear, but I would not use oil
contamination as the primary early-warning variable for misalignment
without equipment-specific evidence.

Therefore, for your system design, I would define the warning horizon as
an **empirically calibrated distribution**, not a single number:

**Detection → Diagnosis → Alarm → Maintenance window → Functional
failure**

The useful KPI would be:

**Warning lead time = timestamp of actionable diagnostic alarm minus
timestamp of confirmed functional failure**

Then report median, 10th percentile, 90th percentile, and false-alarm
rate for each fault class.

That would give you an engineering number that is actually defensible
for your own pumps, compressors, gearboxes, and turbines.

------------------------------------------------------------------------

# **3. How GraphRAG and ontology-based search can improve industrial RCA**

The conceptual advantage is quite different from ordinary LLM retrieval.

Traditional vector RAG essentially asks:

> "Which documents contain text semantically similar to this problem?"

A knowledge graph or ontology adds explicit relationships such as:

**Equipment → Component → Failure mode → Observable symptom → Sensor →
Alarm → Maintenance action → Historical incident → Root cause**

For example:

**PU-2101B → bearing → lubrication degradation → elevated bearing
temperature → high vibration → oil contamination → previous incident →
corrective action**

This is particularly valuable for industrial RCA because the relevant
evidence is usually distributed across multiple information systems. A
maintenance report may contain the repair, historian data may contain
the trend, an OEM manual may contain the permissible condition, and an
incident report may contain the root cause.

A graph can preserve these relationships rather than treating every
paragraph as an independent text chunk.

The petrochemical PdM work by Steurtewagen and van den Poel is relevant
here because it demonstrates the value of combining sensor data with
maintenance-report information and adding interpretability to
machine-learning predictions. 3

For an industrial RCA architecture, I would therefore distinguish three
layers:

**Layer 1, numerical anomaly detection.**\
Vibration, temperature, pressure, current, oil debris, process
variables.

**Layer 2, causal and asset knowledge.**\
Equipment hierarchy, component relationships, failure modes, symptoms,
operating envelopes, maintenance history, engineering rules.

**Layer 3, grounded generation.**\
The LLM receives only retrieved evidence and graph relationships, and
must cite the underlying historian record, work order, manual section,
alarm, or incident record.

The expected benefit is primarily **relevance, traceability, and
constraint**, rather than magically eliminating hallucination.

A useful hallucination-control mechanism is:

**Graph constraint + document retrieval + source citation + confidence
threshold + abstention**

For example, rather than generating:

> "The pump failed because of bearing lubrication."

the system should produce something structurally closer to:

> "Most supported hypothesis: inadequate bearing lubrication. Evidence:
> bearing-temperature trend increased 18 percent over baseline,
> vibration at 1X increased, and oil analysis detected elevated wear
> debris. Historical incident INC-0142 shows the same symptom sequence.
> Confidence: medium. Confirmation required from inspection."

That distinction matters enormously in safety-critical industrial
environments.

------------------------------------------------------------------------

# **Overall synthesis**

For a petrochemical or continuous-process digital-maintenance program,
the strongest evidence-backed architecture is:

**Multi-sensor PdM → anomaly detection → fault classification →
knowledge graph / ontology → evidence-grounded RCA → recommended
maintenance action**

The literature already provides credible evidence that AI can achieve
high fault-detection performance and support earlier intervention.
Petrochemical-specific work also shows that combining sensor data with
maintenance records improves the diagnostic usefulness of ML outputs.
\[3\]\[4\] Industrial manufacturing evidence includes reported
reductions in MTTR and maintenance cost, although those outcomes should
be treated as case-specific rather than universal AI percentages. \[5\]

The two areas where I would **not** put an unsupported number into an
executive paper are the exact bearing/misalignment warning window and
the exact percentage reduction in hallucination from GraphRAG. I cannot
confirm a sufficiently strong common empirical benchmark for either from
the available evidence.

## **Key papers retrieved through Consensus**

**\[1\]** Z. Çınar, Abubakar Abdussalam Nuhu, Qasim Zeeshan, Orhan
Korhan, M.B.A. Asmael, B. Safaei, 2020, *Machine Learning in Predictive
Maintenance towards Sustainable Smart Manufacturing in Industry 4.0*,
Sustainability, 709 citations.\
Consensus paper

**\[2\]** Mohammad Shahin, F. F. Chen, Aliakbar Hosseinzadeh, Neda Zand,
2023, *Using machine learning and deep learning algorithms for downtime
minimization in manufacturing systems: an early failure detection
diagnostic service*, The International Journal of Advanced Manufacturing
Technology, 102 citations.\
Consensus paper

**\[3\]** Bram Steurtewagen, D. van den Poel, 2021, *Adding
interpretability to predictive maintenance by machine learning on sensor
data*, Computers & Chemical Engineering, 29 citations.\
Consensus paper

**\[4\]** Xia Liu, Panpan Zhang, Huandi Shi, 2026, *Predictive
maintenance of petrochemical equipment based on LSTM neural network and
vibration signal analysis*, Australian Journal of Mechanical
Engineering, 1 citation.\
Consensus paper

**\[5\]** P. V., 2025, *A data-driven framework for evaluating
maintenance crews in fertilizer manufacturing units*, Scientific
Reports, 1 citation.\
Consensus paper

**\[6\]** Wejdan Al-Subaiei, Esraa Al-Herz, Wadhha Al-Marri, Rawan
Al-Otaibi, Hessah Ashyan, H. Jaber, 2021, *Industry 4.0 Smart Predictive
Maintenance in the Oil Industry to Enable Near-Zero Downtime in
Operations*, Proceedings of the International Conference on Industrial
Engineering and Operations Management, 1 citation.\
Consensus paper
