# CALIBER 2026 Simulation Design Specification

**Date:** 2026-11-04. **Status:** design for review. **No simulation engine exists, and no simulation has been run.**

**Data status:** Source data documented as synthetic (dummy) in the Data Context & Relationship Diagram; not operational performance.

**Companion documents:** `SIMULATION_INPUT_ASSUMPTION_REGISTER.md` and `SIMULATION_FEASIBILITY_ASSESSMENT.md`. All figures come from `outputs/reports/simulation_feasibility_evidence.md`, which the pipeline rebuilds.

## 1. Case 3 limitation

**The complete Case 3 problem statement is not confirmed in the available project documents.**

- The diagram identifies these workbooks as Case 3, Spare Part Intelligence.
- The only case document, `docs/case/CALIBER_2026_Case_3_Complete_Final_Case.md`, is misnamed. Its content is Case 2, the Intelligent Manufacturing Dashboard.
- The Case 2 reference and RCA reports are context only.

**So this design invents no competition requirement.** Its objectives, measures and boundaries come only from the project owner's approval of this stage. Nothing here should be read as what the competition asks for. **This design must be reviewed against the official Case 3 brief before implementation is approved.** Section 14 lists what the brief could change.

## 2. Purpose and questions

The purpose is a **what-if tool**. It shows how simulated inventory behaves under stated assumptions, and how much the results depend on those assumptions. It doesn't predict the future or reconstruct the past.

| ID | Question, from the project owner's approval | Answered by |
| --- | --- | --- |
| Q1 | How do inventory measures behave under the assumed starting stock and parameters? | Reference set R0 |
| Q2 | How do Scenarios A and B differ in their effect on simulated inventory decisions? | Paired comparison, Section 9.4 |
| Q3 | How sensitive are the results to initial inventory, lead time, demand and replenishment parameters? | Sets S1 and S2 |
| Q4 | How much do the results vary when demand and lead proxies are resampled, where evidence allows? | Set MC |

**Out of scope, per the approval:** claims of actual historical stockouts, monetary savings or financial benefits, and optimisation. Parameters are varied to test sensitivity. They aren't searched for a best value.

## 3. Method evaluation

### 3.1 Discrete-event simulation

**Finding: event logic is appropriate. A general simulation framework is not needed.**

| Consideration | Evidence | Implication |
| --- | --- | --- |
| Events are discrete and dated | Issues, order placements and arrivals each happen on a date | Supports event logic |
| Monthly steps would hide what matters | Median lead proxy is 42 days, and the shortest is 8. 10,568 material-days have an issue | A monthly model can't show a stockout inside a month. **Rejected** |
| Materials don't interact | No shared warehouse, budget, supplier capacity or transport limit exists in the data. Min and Max aren't capacity | Each material can run alone. No queues or shared resources are needed |
| Resolution | Dates have no time of day, and 1,682 material-days have several lines | Daily resolution, with a fixed order of events inside a day |
| No working calendar | Issue lines are nearly even across all seven days (1,743 to 1,895), including 3,538 on weekends | All days are treated alike. No calendar is assumed |

**Recommendation.** A single-item, event-driven inventory recursion per material, with daily resolution, written in plain Python and NumPy. A framework such as SimPy adds no modelling power here, and would add a dependency. Section 11 includes a worked example, and Section 12 requires a second implementation to confirm the result.

### 3.2 Monte Carlo

**Finding: appropriate only as bounded resampling, for a minority of materials.** No parametric distribution is proposed, because most materials lack the history to support one.

| Input | Evidence in the population | Treatment |
| --- | --- | --- |
| Demand | 282 materials have one active month, 201 have one issue line, and 228 have 6 or more active months of 17 | Own-history resampling for 228. Replay and configured what-ifs for the other 437 |
| Lead proxy | 267 materials have 1 or 2 observations, 258 have 3 to 9, and 140 have 10 or more | Own-history resampling for 140. Point value and configured what-ifs for the other 525 |
| Both | 139 materials pass both thresholds | Joint resampling for these only |

**The thresholds of 6 months and 10 observations are analyst choices (S-16).** From 3 to 12 months, the joint count at 10 observations stays between 118 and 140. At 20 observations it falls to 47. It's the lead observations that limit this.

**What a Monte Carlo result means here.** It shows the spread from reshuffling a material's own history. It's not a probability of a future outcome, and it can't produce a demand size or interval that never occurred.

### 3.3 Alternatives considered

| Alternative | Decision | Reason |
| --- | --- | --- |
| Closed-form inventory formulas | Rejected as the main method | They need stationary demand distributions, which the evidence doesn't support |
| Fitted distributions (Poisson, gamma, normal) | **Rejected** | The project owner's rule. Median active months is 2 |
| Pooling across materials to fit a distribution | Rejected | Materials differ in unit and scale, and no definition supports grouping them |
| Time-series forecasting | Rejected | 17 months, no seasonality test possible, and out of scope |

## 4. Population

The population is the **665 Stock Items** with demand history, a promised interval, a unit amount record and a non-zero Min or Max. `data/processed/simulation_population.csv` keeps all 7,481 materials with their status and reasons.

**The unit amount condition changes nothing.** Every Stock Item with a promised interval also has a unit amount record, so the population would still be 665 without it. No model calculation reads a unit amount.

**Coverage, in Scenario A.** The population holds 12,684 of 17,518 issue lines. Within units its quantity share ranges widely: 99% in CAN, 87% in KG, 57% in EA and 21% in SET. **Results describe these 665 materials only.** They don't generalise to Non Stock items or to Stock Items without procurement records.

## 5. Model structure

| Item | Design |
| --- | --- |
| Entity | One material at a time. No interaction between materials |
| Time horizon | 2025-05-01 to 2026-09-30, or 518 days, which is the observed demand window. **Not extended**, because nothing supports extrapolating |
| Time step | Daily resolution, event-driven |
| Initial inventory | The undated Stock value is **assumed** to apply on day 0 (S-01) |
| Initial on-order and backorders | Zero (S-02). Historical purchase orders are **not** replayed as arrivals, because the flows don't balance (A-15) |
| Warm-up | None. The run starts from an assumed state, so early days are a transient, and measures are also reported without it (Section 8.5) |
| End of horizon | Orders still open are counted and reported. Nothing is measured after day 517 |
| Replenishment | Policy-generated only. Reference reading: Min as reorder level, Max as order-up-to level (S-03). **This reading is unverified, and Section 7 of the feasibility assessment records evidence against it** |
| Shortage handling | Partial fill with backorders in the reference set. Lost sales as an alternative (S-05). The data doesn't say which applies |
| Quantities | Within one material and its unit. Never totalled across units |
| Costs | None. No cost, price or value enters the model |

## 6. Event-flow description

Each day is processed in this fixed order. The order matters, because a same-day arrival must be able to serve that day's issue.

```text
Day 0 only:   INITIALISE   H = I0, B = 0, O = 0
              INITIAL REVIEW  if IP <= s, place an order

Each day t:
  1. ARRIVAL     Every order due on day t arrives, in order placed.  H += Q, O -= Q
  2. BACKFILL    Oldest backorders first.  F = min(H, B).  H -= F, B -= F
  3. ISSUES      Each line in source_row order:
                   served = min(H, line quantity)     H -= served
                   short  = line quantity - served
                   Backorder mode: B += short
                   Lost-sales mode: short is recorded as lost
  4. REVIEW      IP = H + O - B
                   if IP <= s and S - IP > 0:
                     Q = S - IP, draw or set L, schedule arrival on day t + L, O += Q
  5. RECORD      End-of-day H, B, O, and any order placed
```

**Rules that follow from this:**

- **One review a day at most**, after issues. A material can place at most one order per day, plus the day-0 initial review.
- **Orders may cross.** Under varying lead times, a later order can arrive first. That's allowed and recorded.
- **Backorders are served before new issues**, oldest first (S-06).
- **Order size uses inventory position**, which includes open orders and backorders. This prevents ordering again for stock already on the way.
- **A shortage doesn't mean the historical issue failed.** Observed issues did happen. See Section 13.

## 7. Mathematical model and formulas

**Indices.** One material. Days $t = 0, \dots, T-1$, with $T = 518$. Demand scenario $k \in \{A, B\}$. Issue lines $\ell$ on day $t$, in `source_row` order.

**Inputs.**

| Symbol | Meaning | Reference value |
| --- | --- | --- |
| $I_0$ | Initial inventory | `assumed_initial_inventory` x $\phi_I$ |
| $s$ | Reorder level | $\lceil \phi_s \cdot \text{Min} \rceil$ |
| $S$ | Order-up-to level | $\max(\lceil \phi_S \cdot \text{Max} \rceil,\ s+1)$ |
| $L_j$ | Lead proxy for order $j$, in whole days | $\lceil \phi_L \cdot \tilde{L} \rceil$, at least 1, where $\tilde{L}$ is the median promised interval for the view |
| $q_{\ell}^{k}$ | Quantity of line $\ell$, in scenario $k$ | Observed quantity x $\phi_D$. Under $\phi_D \ne 1$, cumulative demand is rounded so totals stay accurate |
| $\phi$ | Configurable multipliers | 1 in the reference set |

**State at end of day $t$.** On hand $H_t \ge 0$, backorders $B_t \ge 0$, on order $O_t \ge 0$, and inventory position $IP_t = H_t + O_t - B_t$.

**Recursion, backorder mode.** With arrivals $A_t = \sum_{j:\, t_j + L_j = t} Q_j$:

$$H_t' = H_{t-1} + A_t, \qquad F_t = \min(H_t', B_{t-1})$$

Lines are then served in sequence from $H_t' - F_t$, giving immediate service $w_{\ell} = \min(\text{available}, q_{\ell}^{k})$. With $d_t = \sum_{\ell} q_{\ell}^{k}$ and $w_t = \sum_{\ell} w_{\ell}$:

$$H_t = H_t' - F_t - w_t, \qquad B_t = B_{t-1} - F_t + d_t - w_t$$

**Order rule.** For the review on day $t$:

$$Q_t = \begin{cases} S - IP_t & \text{if } IP_t \le s \text{ and } S - IP_t > 0 \\ 0 & \text{otherwise} \end{cases} \qquad O_t = O_{t-1} - A_t + Q_t$$

**Lost-sales mode.** $B_t = 0$ and $F_t = 0$ for all $t$. Unmet quantity $u_t = d_t - w_t$ is recorded as lost.

**Conservation laws, which must hold in every run.**

$$I_0 + \sum_t A_t = H_{T-1} + \sum_t w_t + \sum_t F_t$$

$$\sum_t d_t = \sum_t w_t + \sum_t F_t + B_{T-1} \quad \text{(backorder mode)}, \qquad \sum_t d_t = \sum_t w_t + \sum_t u_t \quad \text{(lost-sales mode)}$$

$$\sum_t Q_t = \sum_t A_t + O_{T-1}$$

**Alternative policy reading (R2).** Order a fixed $Q = $ `pr_quantity_median` when $IP_t \le s$, repeated until $IP_t > s$. This tests the reference reading against an observed order size, and carries the DEF-05 caveat.

## 8. Performance measures

All are **simulated**, per material, per configuration. None is an observed value.

### 8.1 Stockout periods

| Measure | Formula |
| --- | --- |
| Stockout day | Backorder mode: $B_t > 0$. Lost-sales mode: $u_t > 0$ |
| Stockout period | A maximal run of consecutive stockout days |
| `sim_stockout_periods`, `sim_stockout_days`, `sim_longest_stockout_days` | Count of periods, total days, longest run |
| `sim_days_to_first_stockout` | First stockout day. Blank if none |
| `sim_zero_on_hand_days` | Days with $H_t = 0$, **reported separately**. Zero stock with no unmet issue isn't a stockout |

### 8.2 Service level

Three definitions are reported, because they answer different questions. The approval doesn't choose one, and neither does the data.

| Measure | Formula | Reads as |
| --- | --- | --- |
| `sim_fill_rate_quantity` | $\sum_t w_t \,/\, \sum_t d_t$ | Share of quantity served on its day |
| `sim_fill_rate_lines` | Lines with $w_\ell = q_\ell$, divided by all lines | Share of lines served in full on their day |
| `sim_ready_rate_days` | $\frac{1}{T}\sum_t \mathbb{1}[H_t > 0]$ | Share of days ending with stock on hand |

### 8.3 Inventory and replenishment

| Measure | Formula |
| --- | --- |
| `sim_average_on_hand` | $\frac{1}{T}\sum_t H_t$, in the material's unit |
| `sim_average_backorder` | $\frac{1}{T}\sum_t B_t$ |
| `sim_orders_placed` | Count of $Q_t > 0$ |
| `sim_orders_per_year` | `sim_orders_placed` x 365 / $T$ |
| `sim_order_quantity_mean`, `sim_order_quantity_total` | Within one material |
| `sim_orders_open_at_end` | Orders not arrived by day 517 |
| `sim_first_order_day` | First day with $Q_t > 0$ |

**No cross-material total of quantity exists.** Across materials, results are reported as counts, shares and percentiles of per-material measures, or within one unit.

### 8.4 Demand variability, and differences between scenarios

**Demand variability is observed input, not simulated,** per scenario, from M3: mean and standard deviation of monthly quantity, CV = standard deviation / mean, active months, ADI = 17 / active months, and CV² over active months. No intermittency class is assigned.

**Scenario differences are paired, per material:** $\Delta M = M^{A} - M^{B}$, plus these decision indicators:

| Indicator | Meaning |
| --- | --- |
| `orders_differ` | $\text{orders}^A \ne \text{orders}^B$ |
| `first_order_day_differs` | First order falls on a different day, or occurs in only one scenario |
| `order_quantity_differs` | Total ordered quantity differs |
| `stockout_status_differs` | Any stockout in one scenario and none in the other |

**Neither scenario is a baseline.** The sign of $\Delta M$ is arithmetic only. Results stay in separate columns, and no blended value is reported. For 436 materials the two scenarios are identical by construction, so they're reported apart from the 229 that can differ.

### 8.5 Early-horizon transient

183 materials sit at or below Min on day 0, including 85 with zero stock. Their early stockouts come from the starting assumption, not from demand. So stockout and service measures are reported **over the full horizon and from the first arrival onward**.

## 9. Scenario design

### 9.1 Factors

**Levels are configurable what-if values, not estimates.** Each lives in a configuration file (Section 9.5). "Reference" means the unadjusted input, not a true or preferred value.

| Factor | Reference | What-if levels | Why |
| --- | --- | --- | --- |
| Demand records | **Both A and B, always** | | Approved |
| PR PO view for the lead proxy | **Both views, always** | | No default view (COR-09). Medians differ on 323 materials |
| $\phi_I$, initial inventory | x1 | x0.5, x1.5, = Min, = Max, Stock + window issues | Stock is undated. The last level is an upper bound if the snapshot was taken at the end of the window with no receipts. Absolute levels matter because scaling zero stock changes nothing (85 materials) |
| $\phi_L$, lead proxy | x1 | x0.5, x1.5, x2, 90th percentile | Promised, not achieved. Actual delay is unknown in either direction |
| $\phi_D$, demand | x1 | x0.75, x1.25 | Issues aren't proven demand, and may be censored by availability |
| $\phi_s$, Min | x1 | x0.5, x1.5 | Unverified |
| $\phi_S$, Max | x1 | x0.5, x1.5 | Unverified |
| Policy reading | R1 (s,S) | R2 (s, fixed Q) | Evidence conflicts with R1 |
| Shortage handling | Backorder | Lost sales | Undefined |
| Repeated peak lines | Kept | Excluded, for 29 materials | May be a cap in the data (A-11) |

### 9.2 Run sets

Every set runs under all four combinations of Scenario A or B with each PR PO view.

| Set | Purpose | Design | Runs |
| --- | --- | --- | --- |
| **R0** | Reference | All reference levels | 4 x 665 = 2,660 |
| **S1** | One-at-a-time sensitivity | Each what-if level alone: 5 + 4 + 2 + 2 + 2 + 1 + 1 + 1 = 18 | 18 x 2,660 = 47,880, or fewer since the peak-line level only affects 29 materials |
| **S2** | Interactions | $\phi_I$ {0.5, 1, 1.5} x $\phi_L$ {0.5, 1, 2} x $\phi_D$ {0.75, 1, 1.25} x $\phi_s$ and $\phi_S$ together {0.5, 1, 1.5} = 81 | 81 x 2,660 = 215,460 |
| **MC-D** | Demand resampled | 228 materials, 1,000 replications | 912,000 |
| **MC-L** | Lead proxy resampled | 140 materials, 1,000 replications | 560,000 |
| **MC-J** | Both resampled | 139 materials, 1,000 replications | 556,000 |

**Run time.** R0, S1 and S2 are deterministic and small. The MC sets total about 2 million runs and an estimated 130 million line events. That's an unmeasured estimate, likely minutes rather than hours. A timing pilot comes first, and replications can be reduced if the convergence rule below is met earlier.

### 9.3 Resampling rules

**No distribution is fitted. Resampling draws only from a material's own observed values.**

**Demand, for 228 materials: circular block bootstrap of calendar months.**

1. Draw blocks of 3 consecutive months, wrapping at the end, until 17 months are filled. Block length is configurable (1 or 3).
2. Use the **same draw for every material in a replication**, and the **same draw for Scenarios A and B**.
3. Place each source month's lines on the same day of the month in the target month. Days beyond the month's end move to its last day.

*Why blocks:* months aren't interchangeable. 37.9% of population lines fall in November 2025 to January 2026, and monthly lines range from 284 to 1,861. Blocks keep some of that clustering, but **17 months can't separate a seasonal effect from a one-off**, so results stay what-if only (S-17).

**Lead proxy, for 140 materials: draw per order, with replacement, from the material's own promised intervals**, leaving out those before the PR date. The `exact_distinct_rows` view draws from distinct lines. The `original_rows` view is the same set weighted by copies.

*Known weakness:* drawing per order assumes the interval doesn't depend on order size. In EA the observed Spearman correlation with PR quantity is -0.28, so independence is an approximation (S-18). No relationship with PR date is visible (rho 0.003).

**All other materials:** deterministic replay and configured what-ifs only. They never receive a sampled input.

### 9.4 Monte Carlo reporting and convergence

- **Common random numbers.** Scenarios A and B and both views use identical draws, so their differences come from the inputs and not from sampling noise.
- **Reproducible seeds.** `numpy.random.SeedSequence` from a configured master seed and the configuration, independent of `PYTHONHASHSEED`.
- **Reporting.** Mean, median, and 5th and 95th percentiles of each measure across replications, labelled "spread under resampling" and never "confidence interval for the true value".
- **Convergence.** Monte Carlo error is $SE = \hat\sigma / \sqrt{R}$. For fill rate, target a half-width $1.96 \cdot SE \le 0.01$ on each material. Materials that miss it are listed.

### 9.5 Configuration

Every run is defined by a configuration, stored beside its results. Draft shape, for review:

```json
{
  "configuration_id": "S1_lead_x2",
  "demand_scenario": "scenario_a",
  "prpo_view": "exact_distinct_rows",
  "initial_inventory": {"mode": "multiply_stock", "factor": 1.0},
  "lead_proxy": {"mode": "median", "factor": 2.0},
  "demand_factor": 1.0,
  "min_factor": 1.0,
  "max_factor": 1.0,
  "policy_reading": "R1_min_max",
  "shortage_handling": "backorder",
  "repeated_peak_lines": "keep",
  "resampling": null,
  "seed": null,
  "label": "SIMULATED what-if. Not observed. Inputs unverified."
}
```

## 10. Comparison and sensitivity outputs

| Output | Content |
| --- | --- |
| Scenario difference | $\Delta M$ and decision indicators per material, split by identical-by-construction, materially affected and other |
| One-at-a-time sensitivity | Swing per factor: $\max M - \min M$ across levels, per material, and the median across materials |
| Status changes | Materials whose stockout status, or order count, changes at each level |
| Factor ranking | Which factor moves each measure most, within R0 and S1 |
| Interaction | From S2, whether a factor's effect depends on another's level |
| Dominance check | Whether the scenario choice matters more or less than the unverified inputs. **This is the main decision question** |

## 11. Worked example

A hand-calculated case. The future engine must reproduce it exactly as a test. Both modes use $I_0 = 3$, $s = 2$, $S = 6$, $L = 2$, $T = 6$, with lines of 1 (day 0), 2 (day 1), 5 (day 2) and 1 (day 4).

**Backorder mode.**

| Day | Arrive | Backfill | Issue | Served | End H | End B | IP at review | Order | End O |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | | | 1 | 1 | 2 | 0 | 2 | **4**, due day 2 | 4 |
| 1 | | | 2 | 2 | 0 | 0 | 4 | | 4 |
| 2 | 4 | | 5 | 4 | 0 | 1 | -1 | **7**, due day 4 | 7 |
| 3 | | | | | 0 | 1 | 6 | | 7 |
| 4 | 7 | 1 | 1 | 1 | 5 | 0 | 5 | | 0 |
| 5 | | | | | 5 | 0 | 5 | | 0 |

Day 0's initial review sees $IP = 3 > 2$, so no order is placed until the end of that day.

| Measure | Value | Check |
| --- | --- | --- |
| `sim_fill_rate_quantity` | 8 / 9 = 0.8889 | Served on the day: 1 + 2 + 4 + 1 |
| `sim_fill_rate_lines` | 3 / 4 = 0.75 | Day 2's line is short |
| `sim_ready_rate_days` | 3 / 6 = 0.5 | Days 0, 4 and 5 end with stock |
| `sim_average_on_hand` | 12 / 6 = 2 | 2 + 0 + 0 + 0 + 5 + 5 |
| `sim_stockout_periods` / `sim_stockout_days` | 1 / 2 | Days 2 and 3 |
| `sim_zero_on_hand_days` | 3 | Days 1, 2 and 3. Day 1 isn't a stockout |
| `sim_orders_placed` | 2 | Quantities 4 and 7 |
| Conservation of stock | 3 + 11 = 5 + 8 + 1 | Both sides 14 |
| Conservation of demand | 9 = 8 + 1 + 0 | |
| Conservation of orders | 11 = 11 + 0 | |

**Lost-sales mode.** Day 2 loses 1 unit, so IP at review is 0 and the order is 6, due on day 4. End-of-day H is 2, 0, 0, 0, 5, 5. Fill rate on quantity stays 8/9, and lost quantity is 1. There is 1 stockout day. Conservation: 3 + 10 = 5 + 8, both 13.

## 12. Validation and testing strategy

**The model can be verified, but it can't be validated against reality.** Verification asks whether the code does what this design says. Validation would ask whether the results match what happened, and that needs dated stock and receipts, which don't exist. Results must say so.

### 12.1 Verification

| Level | Test | Passes when |
| --- | --- | --- |
| Inputs | Engine inputs reconcile to M1, M2 and M3 | Every line, parameter and lead proxy matches |
| Worked example | Section 11, in both modes | Every number matches exactly |
| More hand cases | Same-day arrival and issue, crossing orders, an issue larger than S, zero stock on day 0, a lead proxy longer than the horizon | Match hand calculation |
| Conservation | Section 7 laws, on every material in every deterministic run | Exact |
| State bounds | $H_t \ge 0$, $B_t \ge 0$, $O_t \ge 0$, and $B_t = 0$ in lost-sales mode | Always |
| Independent implementation | A second, separately written daily loop, compared on all of R0 | Identical results |

### 12.2 Predictions the engine must meet

These come from the feasibility evidence, calculated before any engine exists, so they're real tests.

| Prediction, in R0 | Materials |
| --- | --- |
| No order is placed in Scenario A | Exactly 125 |
| No order is placed in Scenario B | Exactly 133 |
| An order is placed at the day-0 review | Exactly 183 |
| Scenarios A and B give identical results | All 436 identical by construction |
| Whether Min is ever reached differs between scenarios | Exactly 8 |
| Materials whose initial inventory covers all issues have fill rate 1 and no stockout | 238 in A, 253 in B |

### 12.3 Degenerate and relationship tests

**Must hold exactly:**

| Case | Expected |
| --- | --- |
| No demand | No stockout, and no order unless $I_0 \le s$. On hand changes only if that order arrives |
| Very large $I_0$ | Fill rate 1, no order |
| Lead proxy of 1 day, with large $S$ | Stockouts limited to the first days |
| Scenario with no copies | Same as its pair |

**Expected tendencies, not laws.** Under (s,S) with discrete lines, these can fail on single materials, because a shift can change order timing. A test requires them to hold across most materials, and each exception must be explained, not hidden.

| Change | Expected direction |
| --- | --- |
| Higher $\phi_I$ | Fill rate not lower |
| Higher $\phi_L$ | Fill rate not higher |
| Higher $\phi_D$ | Fill rate not higher, orders not fewer |
| Scenario B compared with A | Less demand, so usually fewer orders. Not guaranteed per material |

### 12.4 Monte Carlo tests

| Test | Passes when |
| --- | --- |
| Reproducibility | Same seed gives identical bytes, across processes and hash seeds |
| Different seeds | Results differ, within the reported spread |
| No invented values | Every sampled line quantity and interval exists in that material's history |
| Evidence gate | A material below a threshold never receives a sampled input |
| Common random numbers | A and B use identical draws, and materials identical by construction give identical results in every replication |
| Convergence | Rule in Section 9.4 is reported |

### 12.5 Failure detection and boundaries

As in earlier stages, tests must damage inputs and confirm the checks catch it. Boundary checks must fail if a result lacks the simulated label, or if an output adds any money, cost or saving column, an "actual" column, a blended A and B value, a quantity total across units, or a best-scenario or optimal-value column.

### 12.6 Plausibility checks, not validation

Reported as context, with no pass or fail, because the comparison isn't like for like: simulated order counts against observed PR lines, and simulated order sizes against observed PR quantities.

## 13. Reporting rules

| Rule | Detail |
| --- | --- |
| Label | Every output: **"SIMULATED under stated assumptions. Not observed. Inputs unverified."**, plus the synthetic data label |
| Names | Simulated columns start with `sim_`. Observed values never carry that prefix |
| No historical claim | A simulated stockout is **never** described as one that happened. Observed issues did happen, so a simulated shortage on a replayed issue shows the assumptions disagree with history. It's a finding about the assumptions |
| No money | No cost, saving or benefit, in any currency |
| Both scenarios, both views | Reported side by side, with no blend and no default |
| Evidence tier | Shown beside each material's result |
| Language | "If these assumptions held, the model shows...". Never "the plant will..." |

## 14. Items for review against the official Case 3 brief

Implementation waits for this review. The brief could change:

| Design item | What the brief could change |
| --- | --- |
| Questions in Section 2 | Whether these are the questions being asked |
| Population of 665 | Whether Non Stock items, criticality-based subsets or other materials are required |
| Measures | Whether a specific service definition or target is required |
| Horizon | Whether a forward-looking horizon is required. This design has none, because the data doesn't support one |
| Costs | Whether official cost data or rates are provided. Financial analysis stays out unless they are |
| Definitions | Whether the brief defines Min, Max, Stock date, criticality or PO-Delivery Date. That would replace assumptions here |
| Method | Whether a method is required or excluded |

## 15. Implementation outline, not built

Proposed once approved: `src/simulation/engine.py`, `inputs.py`, `measures.py`, `resampling.py` and `checks.py`, plus configuration files, the second implementation under `tests/`, and a report. Order of work: inputs, deterministic engine, worked example and conservation tests, R0 predictions, second implementation, S1 and S2, timing pilot, then Monte Carlo. A stop gate follows R0, because R0 will show whether the reference reading is usable at all.
