# INSpire Engine Output Contract v0.2

**Status:** generated from `src/simulation/contract.py`. Do not edit by hand. This is contract v0.1 plus Addenda A and B, extended. It does not replace them with a competing contract: every v0.1 column keeps its name and meaning, and v0.2 only adds columns, files and enum values. See the change log in `TEAM_INTEGRATION_PROTOCOL.md`.

**Paths.** Real output: `data/processed/engine/` (git-ignored, confidential, blocked from deployment by D-07). Labelled sample output: `data/samples/engine/` (invented material numbers, safe to deploy).

**Rules that apply to every file.** CSV, UTF-8. Blank means no value, never zero. Read `material_no` as text. `output_class` says what each row is, and `sample` rows are never results. Do not recalculate any value. Do not sum quantities across units or amounts across currencies. There is no default demand scenario or PR PO view.

**Manifest.** `eng_run_manifest.json` has `run_id`, `spec_version`, `engine_version`, `methodology_version`, `data_label`, `simulated_label`, `seed`, `replications`, `input_checksums`, `created_at`, `execution_status`, `assumptions`, `populations` and, for each file, rows, sha256, grain, output classes, seed, population and assumptions. A loader must reject a run with no manifest or no `data_label`.

**Scenario grammar.** `SC-<D>-<V>-<P>-<S>-<K>`. D: A, B. V: OR, ED. P: R0, R1, R2, N1, X1, X2, X3. S: BO, LS. K: `eng_config_registry.csv`. N1 is new in v0.2. `SC-ALL-NA-NA-NA-K0` marks a scenario-independent row. Forecast rows use `NA` inside `scenario_id` for the parts they do not depend on. Read every CSV with default null-string parsing off, or `SC-` values and units can be damaged.

## `eng_material_tier.csv`

- **Grain:** One row per material
- **Primary key:** `material_no`
- **Population:** All 7,481 materials
- **Scenario identification:** Both scenarios as separate columns. demand_class takes the less smooth of the two
- **Evidence:** rule_derived: rules on recorded issues

| Column | Type | Unit | Null allowed | Meaning |
| --- | --- | --- | --- | --- |
| `run_id` | string |  | no | Identifies the run. A number is only valid with its run_id |
| `material_no` | string |  | no | Material number as text. Never parse as a number |
| `unit` | string | text | yes | Material unit. Quantities are never summed across units |
| `mrp_type` | string |  | yes | Stock Item or Non Stock |
| `active_months` | int | months of 17 | no | Months with an issue. Same in A and B |
| `n_issue_lines__scenario_a` | int | lines | no |  |
| `n_issue_lines__scenario_b` | int | lines | no |  |
| `tier` | enum |  | no | T3 policy-simulatable, T2 demand-evidenced, T1 state-only |
| `adi` | float | months | yes | 17 / active months. Blank if never issued |
| `cv2__scenario_a` | float |  | yes | Squared coefficient of variation of active-month quantities, sample standard deviation. Blank with one active month |
| `demand_pattern__scenario_a` | string |  | yes | smooth, erratic, intermittent or lumpy. Only at 6 or more active months |
| `demand_class__scenario_a` | enum |  | no | D0 to D4 under Scenario A |
| `cv2__scenario_b` | float |  | yes |  |
| `demand_pattern__scenario_b` | string |  | yes |  |
| `demand_class__scenario_b` | enum |  | no | D0 to D4 under Scenario B |
| `demand_class` | enum |  | no | D0 none, D1 sparse, D2 thin, D3 intermittent, lumpy or erratic, D4 smooth |
| `flag_class_differs_by_scenario` | bool |  | no | D3 or D4 differs between A and B |
| `lead_observations_distinct` | float | lines | yes | Promised intervals on exact_distinct_rows. Blank outside procurement history |
| `forecast_eligibility` | enum |  | no | forecast_range at 6 or more active months, rate_range_only at 3 to 5, abstain otherwise |
| `policy_grade` | enum |  | yes | A: proposed parameters (228). B: replay and what-if only, no parameters (437). Blank outside T3 |
| `evidence_subtier` | string |  | no | Tier, grade and lead evidence |
| `flag_outlier_review` | bool |  | no | Robust z above 3.5 or a line at a repeated unit peak. Flag only, nothing is removed |
| `flag_scenario_divergent` | bool |  | no | Materially affected by the scenario choice (A-14) |
| `confidence` | enum |  | no | Medium, Low or Abstain. High is reserved |
| `abstain_reason` | string |  | yes | Why no forecast or parameter is given. Blank when eligible |
| `output_class` | enum |  | no | sample, historical_descriptive, rule_derived, statistical_forecast, deterministic_simulation, stochastic_simulation or not_computed |

## `eng_forecast.csv`

- **Grain:** One row per material, scenario and horizon basis. next_month_rate for all 7,481 under A and B. lead_time_demand for the 296 eligible under each scenario and view
- **Primary key:** `material_no`, `scenario_id`, `horizon_basis`
- **Population:** All 7,481 with abstention rows
- **Scenario identification:** Scenario A and B, and view OR and ED for lead-time demand
- **Evidence:** statistical_forecast where eligible. Issues are not proven demand

| Column | Type | Unit | Null allowed | Meaning |
| --- | --- | --- | --- | --- |
| `run_id` | string |  | no | Identifies the run. A number is only valid with its run_id |
| `material_no` | string |  | no | Material number as text. Never parse as a number |
| `demand_scenario` | enum |  | no | A or B. ALL if not scenario dependent. Neither is a default |
| `pr_view` | enum |  | no | OR original_rows, ED exact_distinct_rows, ALL if not view dependent. Neither is a default |
| `scenario_id` | string |  | no | SC-<D>-<V>-<P>-<S>-<K>. SC-ALL-NA-NA-NA-K0 means the row does not depend on scenario |
| `horizon_basis` | enum |  | no | next_month_rate or lead_time_demand |
| `forecast_period` | string |  | no | 2026-10, or the lead window after the data ends |
| `horizon_days` | float | days | yes | Median promised interval used for lead-time demand |
| `unit` | string | text | yes | Material unit. Quantities are never summed across units |
| `demand_class` | enum |  | no | Class under this scenario |
| `active_months` | int | months of 17 | no | Historical evidence |
| `n_issue_lines` | int | lines | no | Historical evidence count |
| `evidence_class` | string |  | no | Same as evidence_subtier |
| `forecast_eligible` | bool |  | no | False means no point forecast is given |
| `forecast_quantity` | float | own unit per month, or per lead window | yes | Point forecast or mean lead-time demand. Blank when not eligible |
| `forecast_method` | string |  | no | croston_sba, tsb, mean, naive, block_bootstrap_lead_time_demand, observed_active_month_range or abstain |
| `rate_low` | float | own unit per month | yes | Observed month p05 (D3, D4), or lowest active month (D2). Not a prediction interval |
| `rate_mid` | float | own unit per month | yes | Observed month median |
| `rate_high` | float | own unit per month | yes | Observed month p95, or highest active month (D2) |
| `uncertainty_kind` | string |  | yes | Names what the range is. Never a confidence interval |
| `confidence` | enum |  | no | Medium, Low or Abstain |
| `output_class` | enum |  | no | sample, historical_descriptive, rule_derived, statistical_forecast, deterministic_simulation, stochastic_simulation or not_computed |
| `abstain_reason` | string |  | yes | Reason where no forecast is given |
| `lead_time_demand_low` | float | own unit per lead window | yes | p05 under resampling |
| `lead_time_demand_mid` | float | own unit per lead window | yes | p50 under resampling |
| `lead_time_demand_high` | float | own unit per lead window | yes | p95 under resampling |
| `lead_mode` | string |  | yes | resampled_own_history or median_promised_interval |
| `quantile_method_status` | string |  | yes | accepted, or not_accepted_failed_preregistered_pinball_rule |

## `eng_forecast_validation.csv`

- **Grain:** One row per demand scenario, class and method
- **Primary key:** `demand_scenario`, `demand_class`, `method`
- **Population:** 296 forecast-eligible materials
- **Scenario identification:** A and B separately
- **Evidence:** Rolling origin on recorded issues

| Column | Type | Unit | Null allowed | Meaning |
| --- | --- | --- | --- | --- |
| `run_id` | string |  | no | Identifies the run. A number is only valid with its run_id |
| `demand_scenario` | enum |  | no | A or B |
| `demand_class` | enum |  | no | D3 or D4 |
| `method` | string |  | no | mean, naive, croston_sba, tsb or block_bootstrap |
| `n_materials` | int | materials | no |  |
| `n_origin_evaluations` | int | evaluations | no |  |
| `median_scaled_error` | float | ratio | yes |  |
| `mean_bias` | float | mixed own units | yes | Across units, so read only as sign |
| `share_beating_mean_pinball_0.5` | float | share of materials | yes |  |
| `mean_pinball_0.5` | float | mixed own units | yes |  |
| `empirical_coverage_0.5` | float | share | yes |  |
| `share_beating_mean_pinball_0.9` | float | share of materials | yes |  |
| `mean_pinball_0.9` | float | mixed own units | yes |  |
| `empirical_coverage_0.9` | float | share | yes |  |
| `share_beating_mean_pinball_0.95` | float | share of materials | yes |  |
| `mean_pinball_0.95` | float | mixed own units | yes |  |
| `empirical_coverage_0.95` | float | share | yes |  |
| `share_beating_mean_pinball_0.98` | float | share of materials | yes |  |
| `mean_pinball_0.98` | float | mixed own units | yes |  |
| `empirical_coverage_0.98` | float | share | yes |  |
| `selected_point_method` | string |  | no | Point method after the pre-registered rule |
| `bootstrap_range_accepted` | bool |  | no | Beat mean-of-history on most materials at 0.90, 0.95 and 0.98 |
| `output_class` | enum |  | no | sample, historical_descriptive, rule_derived, statistical_forecast, deterministic_simulation, stochastic_simulation or not_computed |

## `eng_scenario_result.csv`

- **Grain:** One row per material and scenario_id
- **Primary key:** `material_no`, `scenario_id`
- **Population:** R0, R2 665. N1, X 228. Held-out 197. MC-D 228, MC-L 140, MC-J 139
- **Scenario identification:** A and B, OR and ED, policy, shortage rule and K in scenario_id
- **Evidence:** deterministic_simulation or stochastic_simulation. SIMULATED under stated assumptions. Not observed. Never an actual stockout

| Column | Type | Unit | Null allowed | Meaning |
| --- | --- | --- | --- | --- |
| `run_id` | string |  | no | Identifies the run. A number is only valid with its run_id |
| `material_no` | string |  | no | Material number as text. Never parse as a number |
| `scenario_id` | string |  | no | SC-<D>-<V>-<P>-<S>-<K>. SC-ALL-NA-NA-NA-K0 means the row does not depend on scenario |
| `demand_scenario` | enum |  | no | A or B |
| `pr_view` | enum |  | no | OR or ED |
| `policy` | enum |  | no | R0 recorded replay, R1 recorded under resampling, R2 recorded Min with repeated PR median, N1 naive, X1-X3 proposed at 90, 95, 98 percent scenario levels |
| `unmet_rule` | enum |  | no | BO backorder |
| `config_id` | string |  | no | K part. See eng_config_registry.csv |
| `run_set` | string |  | no | R0, HO, MC-D, MC-L or MC-J |
| `result_type` | enum |  | no | replay, heldout_replay, simulation or sample |
| `output_class` | enum |  | no | sample, historical_descriptive, rule_derived, statistical_forecast, deterministic_simulation, stochastic_simulation or not_computed |
| `unit` | string | text | yes | Material unit. Quantities are never summed across units |
| `service_level` | float | share | yes | Scenario level, never a target. Blank for recorded policies |
| `parameter_source` | string |  | no | recorded_min_max_unverified, training_months_only, full_window_in_sample or full_window_same_history. Full-window values are in-sample |
| `s_used` | int | own unit | no | Reorder level |
| `S_used` | float | own unit | yes | Order-up-to level. Blank for R2 |
| `Q_used` | float | own unit | yes | Fixed quantity for R2, S minus s for proposed policies |
| `lead_days_used` | string |  | no | Whole days, or resampled_per_order. Promised interval, not a lead time |
| `initial_inventory_used` | int | own unit | no | Assumed opening stock |
| `total_issues` | float | own unit | yes | Input issues. Mean across replications when resampled |
| `n_issue_lines` | float | lines | yes |  |
| `shortfall_probability` | prob | probability | yes | Share of replications with a stockout day. Blank for deterministic rows |
| `any_shortfall` | bool |  | yes | Deterministic rows: at least one stockout day. Blank when resampled |
| `expected_unmet_qty` | float | own unit | no | Quantity not served on its day |
| `days_at_or_below_zero` | float | days | no | Days ending with zero on hand |
| `mean_on_hand` | float | own unit | no | Average inventory |
| `p95_on_hand` | float | own unit | no |  |
| `units_above_recorded_max` | float | own unit | no | Mean daily units above recorded Max |
| `days_above_recorded_max` | float | days | no |  |
| `orders_placed` | float | orders | no | Replenishment orders. Mean across replications when resampled |
| `sim_fill_rate_quantity` | prob | ratio | yes | Served on day / issues. Blank if no issues |
| `sim_fill_rate_lines` | prob | ratio | yes | Lines served in full on the day / lines. Deterministic only |
| `sim_ready_rate_days` | prob | ratio | yes | Days ending with stock / days. Deterministic only |
| `sim_average_backorder` | float | own unit | yes |  |
| `sim_stockout_days` | float | days | yes |  |
| `sim_stockout_periods` | float | periods | yes |  |
| `sim_longest_stockout_days` | float | days | yes |  |
| `sim_days_to_first_stockout` | float | day index | yes |  |
| `sim_orders_per_year` | float | orders per year | yes |  |
| `sim_order_quantity_mean` | float | own unit | yes |  |
| `sim_order_quantity_total` | float | own unit | yes |  |
| `sim_orders_open_at_end` | float | orders | yes |  |
| `sim_first_order_day` | float | day index | yes |  |
| `sim_first_arrival_day` | float | day index | yes |  |
| `sim_ending_on_hand` | float | own unit | yes |  |
| `sim_ending_backorder` | float | own unit | yes |  |
| `sim_ending_on_order` | float | own unit | yes |  |
| `sim_lost_quantity` | float | own unit | yes |  |
| `sim_fill_rate_after_first_arrival` | prob | ratio | yes | Fill rate from the first arrival onward, which removes most of the opening-stock transient |
| `sim_stockout_days_after_first_arrival` | float | days | yes |  |
| `shortfall_probability_after_first_arrival` | prob | probability | yes | Same as shortfall_probability, from the first arrival onward |
| `unmet_qty_p95` | float | own unit | yes | Spread under resampling |
| `mean_on_hand_p05` | float | own unit | yes | Spread under resampling |
| `mean_on_hand_p95` | float | own unit | yes | Spread under resampling |
| `fill_rate_p05` | prob | ratio | yes | Spread under resampling. Not a confidence interval |
| `fill_rate_p95` | prob | ratio | yes | Spread under resampling. Not a confidence interval |
| `fill_rate_half_width` | float | ratio | yes | Monte Carlo error, 1.96 x SE |
| `converged_fill_rate` | bool |  | yes | Half-width at or below 0.01 |
| `n_replications` | float | replications | yes |  |
| `seed` | float |  | yes | Master seed |
| `policy_grade` | enum |  | no | A or B |
| `data_label` | string |  | no | synthetic |

## `eng_proposed_parameters.csv`

- **Grain:** One row per material, scenario and service level
- **Primary key:** `material_no`, `scenario_id`
- **Population:** 228 Grade A materials only (D-24)
- **Scenario identification:** A and B, OR and ED, X1 to X3
- **Evidence:** stochastic_simulation. Candidate for review. Never called optimal

| Column | Type | Unit | Null allowed | Meaning |
| --- | --- | --- | --- | --- |
| `run_id` | string |  | no | Identifies the run. A number is only valid with its run_id |
| `material_no` | string |  | no | Material number as text. Never parse as a number |
| `scenario_id` | string |  | no | SC-<D>-<V>-<P>-<S>-<K>. SC-ALL-NA-NA-NA-K0 means the row does not depend on scenario |
| `demand_scenario` | enum |  | no | A or B |
| `pr_view` | enum |  | no | OR or ED |
| `policy` | enum |  | no | X1, X2 or X3 |
| `service_level` | float | share | no | 90, 95 or 98 percent. Scenario level, never a target |
| `proposed_s` | int | own unit | no | Reorder point: alpha quantile of lead-time demand |
| `proposed_S` | int | own unit | no | Order-up-to: s + Q |
| `proposed_Q` | int | own unit | no | Median PR quantity for the view |
| `safety_stock` | float | own unit | no | s minus mean lead-time demand, floored at zero |
| `flag_safety_stock_floored` | bool |  | no |  |
| `proposed_S_capped_at_recorded_max` | int | own unit | no | Comparison only |
| `lead_time_demand_mean` | float | own unit | no |  |
| `lead_time_demand_quantile` | float | own unit | no |  |
| `lead_mode` | string |  | no | resampled_own_history or median_promised_interval |
| `lead_days_median` | int | days | no | Promised interval, not a lead time |
| `n_draws` | int | draws | no |  |
| `recorded_min` | float | own unit | yes | BoM Min.Qty. Meaning unverified |
| `recorded_max` | float | own unit | yes | BoM Max.Qty. Meaning unverified |
| `recorded_stock_undated` | float | own unit | yes | BoM Stock. Undated, so not a verified current balance |
| `unit` | string | text | yes | Material unit. Quantities are never summed across units |
| `parameter_status` | string |  | no | candidate_for_review |
| `output_class` | enum |  | no | sample, historical_descriptive, rule_derived, statistical_forecast, deterministic_simulation, stochastic_simulation or not_computed |

## `eng_capability_output.csv`

- **Grain:** One row per material, capability and scenario
- **Primary key:** `material_no`, `capability`, `scenario_id`
- **Population:** All 7,481 for overstock, slow-moving and reorder. T3 for stockout. Grade A for dynamic parameters and cost risk
- **Scenario identification:** In scenario_id
- **Evidence:** See method_class and output_class

| Column | Type | Unit | Null allowed | Meaning |
| --- | --- | --- | --- | --- |
| `run_id` | string |  | no | Identifies the run. A number is only valid with its run_id |
| `material_no` | string |  | no | Material number as text. Never parse as a number |
| `capability` | enum |  | no | The six capabilities |
| `scenario_id` | string |  | no | SC-<D>-<V>-<P>-<S>-<K>. SC-ALL-NA-NA-NA-K0 means the row does not depend on scenario |
| `flag` | string |  | no | Level or code for the capability |
| `value_num` | float |  | yes | Blank when no number is supported |
| `value_kind` | string |  | yes | What value_num is |
| `unit` | string | text | yes | Material unit. Quantities are never summed across units |
| `confidence` | enum |  | no | Medium, Low or Abstain |
| `requires_review` | bool |  | no |  |
| `reason_codes` | string |  | no | Semicolon-separated |
| `method_class` | string |  | no | simulation, simulation_grid, deterministic_rule, deterministic_rule_on_simulation or arithmetic_blocked |
| `recommended_action` | enum |  | yes | Set on the reorder capability. HOLD stands for Maintain |
| `output_class` | enum |  | no | sample, historical_descriptive, rule_derived, statistical_forecast, deterministic_simulation, stochastic_simulation or not_computed |

## `eng_recommendation.csv`

- **Grain:** One row per material and scenario. Grade A: 4 rows. Everyone else: 1 row, SC-ALL
- **Primary key:** `material_no`, `scenario_id`
- **Population:** All 7,481
- **Scenario identification:** Grade A per A or B and OR or ED, at the X2 reference level. Actions at 90 and 98 percent alongside
- **Evidence:** rule_derived. Every action is a candidate needing review

| Column | Type | Unit | Null allowed | Meaning |
| --- | --- | --- | --- | --- |
| `run_id` | string |  | no | Identifies the run. A number is only valid with its run_id |
| `material_no` | string |  | no | Material number as text. Never parse as a number |
| `scenario_id` | string |  | no | SC-<D>-<V>-<P>-<S>-<K>. SC-ALL-NA-NA-NA-K0 means the row does not depend on scenario |
| `demand_scenario` | enum |  | no | A or B. ALL if not scenario dependent. Neither is a default |
| `pr_view` | enum |  | no | OR original_rows, ED exact_distinct_rows, ALL if not view dependent. Neither is a default |
| `service_level_reference` | float | share | yes | Analyst-selected reference level for the single action shown |
| `recommended_action` | enum |  | no | REORDER, HOLD (Maintain), REDUCE, MONITOR, NO_ACTION_EVIDENCE (abstention) |
| `action_label` | string |  | no | Display text |
| `action_at_90` | enum |  | yes | Action at the 90 percent scenario level |
| `action_at_98` | enum |  | yes | Action at the 98 percent scenario level |
| `risk_level` | enum |  | no | High, Medium, Low or Not assessed |
| `evidence_class` | string |  | no | Same as evidence_subtier |
| `confidence` | enum |  | no | Medium, Low or Abstain |
| `reason_codes` | string |  | no | Machine-readable reasons |
| `reason` | string |  | no | Plain text reason |
| `trigger_condition` | string |  | no | The condition that fired, with numbers |
| `supporting_metrics` | string |  | no | JSON object of the numbers used |
| `proposed_s` | float | own unit | yes |  |
| `proposed_S` | float | own unit | yes |  |
| `proposed_Q` | float | own unit | yes |  |
| `safety_stock` | float | own unit | yes |  |
| `recorded_min` | float | own unit | yes | BoM Min.Qty. Meaning unverified |
| `recorded_max` | float | own unit | yes | BoM Max.Qty. Meaning unverified |
| `recorded_stock_undated` | float | own unit | yes | BoM Stock. Undated, so not a verified current balance |
| `unit` | string | text | yes | Material unit. Quantities are never summed across units |
| `limitations` | string |  | no | Semicolon-separated limitation codes |
| `requires_review` | bool |  | no |  |
| `method_class` | string |  | no | deterministic_rule or deterministic_rule_on_simulation |
| `output_class` | enum |  | no | sample, historical_descriptive, rule_derived, statistical_forecast, deterministic_simulation, stochastic_simulation or not_computed |
| `consensus_status` | enum |  | no | all_scenarios_agree or scenario_dependent |
| `consensus_action` | enum |  | yes | Set only if every scenario agrees |

## `eng_health_flags.csv`

- **Grain:** One row per material
- **Primary key:** `material_no`
- **Population:** All 7,481
- **Scenario identification:** Scenario independent except simulated risk, which reports the worst of four
- **Evidence:** rule_derived on recorded values, simulated risk for Grade A

| Column | Type | Unit | Null allowed | Meaning |
| --- | --- | --- | --- | --- |
| `material_no` | string |  | no | Material number as text. Never parse as a number |
| `run_id` | string |  | no | Identifies the run. A number is only valid with its run_id |
| `tier` | enum |  | no | T1, T2 or T3 |
| `policy_grade` | enum |  | yes | A or B. Blank outside T3 |
| `demand_class` | enum |  | no | D0 to D4 |
| `unit` | string | text | yes | Material unit. Quantities are never summed across units |
| `active_months` | int | months of 17 | no |  |
| `recorded_stock_undated` | float | own unit | yes | BoM Stock. Undated, so not a verified current balance |
| `recorded_min` | float | own unit | yes | BoM Min.Qty. Meaning unverified |
| `recorded_max` | float | own unit | yes | BoM Max.Qty. Meaning unverified |
| `first_issue_date` | string |  | yes | Blank if never issued |
| `last_issue_date` | string |  | yes | Blank if never issued |
| `days_since_last_issue_at_window_end` | float | days | yes |  |
| `flag_stock_held` | bool |  | no | Recorded stock above zero |
| `flag_stock_at_or_below_recorded_min` | bool |  | no |  |
| `flag_stock_above_recorded_max` | bool |  | no | Only where Max is above zero. Recorded comparison, not a statement of excess |
| `flag_stock_held_with_zero_max` | bool |  | no |  |
| `flag_slow_moving_by_recorded_issues` | bool |  | no |  |
| `slow_moving_basis` | string |  | yes |  |
| `flag_non_moving_by_recorded_issues` | bool |  | no | Stock held, never issued in the window. Not an obsolescence determination |
| `has_plan_link_at_bom_locations` | bool |  | yes | A BoM location has a recorded maintenance plan. Blank if the material has no BoM location row |
| `n_bom_locations` | float | locations | yes |  |
| `flag_potentially_obsolete_candidate` | bool |  | no | Hypothesis only: stock held, no issue in the window, no plan link. Needs lifecycle data |
| `flag_outlier_review` | bool |  | no |  |
| `shortfall_probability_min` | prob | probability | yes | Lowest of four scenarios, policy R1 |
| `shortfall_probability_max` | prob | probability | yes | Highest of four scenarios, policy R1 |
| `shortfall_probability_after_first_arrival_max` | prob | probability | yes | Highest of four, from the first arrival onward |
| `replay_any_shortfall` | bool |  | yes | R0 replay, any scenario. Blank outside T3 |
| `stockout_risk_level` | enum |  | no | High, Medium, Low or Not assessed |
| `stockout_risk_basis` | string |  | no |  |
| `days_above_recorded_max_share_max` | float | share | yes |  |
| `stock_above_proposed_S_scenarios` | float | scenarios of 4 | yes |  |
| `overstock_risk_level` | enum |  | no | High, Medium, Low or Not assessed |
| `overstock_risk_basis` | string |  | no |  |
| `wording_note` | string |  | no |  |
| `output_class` | enum |  | no | sample, historical_descriptive, rule_derived, statistical_forecast, deterministic_simulation, stochastic_simulation or not_computed |

## `eng_explanation_facts.csv`

- **Grain:** One row per fact
- **Primary key:** `fact_id`
- **Population:** All 7,481
- **Scenario identification:** In scenario_id
- **Evidence:** Copies values from other files. The assistant may quote only these

| Column | Type | Unit | Null allowed | Meaning |
| --- | --- | --- | --- | --- |
| `run_id` | string |  | no | Identifies the run. A number is only valid with its run_id |
| `material_no` | string |  | no | Material number as text. Never parse as a number |
| `fact_id` | string |  | no | Unique |
| `capability` | string |  | no | Capability, or all |
| `fact_key` | string |  | no | Name of the fact |
| `value` | string |  | no | Value as text |
| `unit` | string |  | yes |  |
| `scenario_id` | string |  | no | SC-<D>-<V>-<P>-<S>-<K>. SC-ALL-NA-NA-NA-K0 means the row does not depend on scenario |
| `source_file` | string |  | no |  |
| `source_column` | string |  | no |  |

## `eng_supply_context.csv`

- **Grain:** One row per material and PR PO view
- **Primary key:** `material_no`, `pr_view`
- **Population:** 1,250 procured materials, 2 views
- **Scenario identification:** PR view OR and ED
- **Evidence:** historical_descriptive. Promised procurement interval, not transport or goods-receipt time. Currencies are never combined

| Column | Type | Unit | Null allowed | Meaning |
| --- | --- | --- | --- | --- |
| `run_id` | string |  | no | Identifies the run. A number is only valid with its run_id |
| `material_no` | string |  | no | Material number as text. Never parse as a number |
| `pr_view` | enum |  | no | OR or ED |
| `supplier_code` | string |  | no |  |
| `supplier_name` | string |  | yes |  |
| `currency` | string |  | no | Own currency. Never converted |
| `unit` | string | text | yes | Material unit. Quantities are never summed across units |
| `n_lines` | int | lines | no |  |
| `n_purchase_orders` | int | orders | no |  |
| `first_pr_date` | string |  | no |  |
| `last_pr_date` | string |  | no |  |
| `pr_quantity_median` | float | own unit | yes |  |
| `promised_interval_days_min` | float | days | yes |  |
| `promised_interval_days_median` | float | days | yes |  |
| `promised_interval_days_p75` | float | days | yes |  |
| `promised_interval_days_p25` | float | days | yes |  |
| `promised_interval_days_p90` | float | days | yes |  |
| `promised_interval_days_max` | float | days | yes |  |
| `promised_interval_days_iqr` | float | days | yes | Interval variability |
| `promised_interval_days_std` | float | days | yes | Interval variability. Blank with one line |
| `n_lines_used_for_promised_interval` | int | lines | no |  |
| `requested_interval_days_median` | float | days | yes |  |
| `requested_vs_promised_gap_days_median` | float | days | yes |  |
| `n_lines_promised_after_data_cutoff` | int | lines | no | Promised after 2026-09-30. Not verified as open: no receipts exist |
| `n_lines_promised_before_pr` | int | lines | no | Date anomaly, left out of intervals |
| `supplier_share_of_lines` | float | share | yes |  |
| `source_file` | string |  | no |  |
| `label` | string |  | no |  |
| `output_class` | enum |  | no | sample, historical_descriptive, rule_derived, statistical_forecast, deterministic_simulation, stochastic_simulation or not_computed |

## `eng_kpi_summary.csv`

- **Grain:** One row per KPI, population and scenario
- **Primary key:** `kpi_id`, `kpi_name`, `population`, `scenario`, `result_type`
- **Population:** Named in each row
- **Scenario identification:** Named in each row
- **Evidence:** Named in each row. No composite score

| Column | Type | Unit | Null allowed | Meaning |
| --- | --- | --- | --- | --- |
| `run_id` | string |  | no | Identifies the run. A number is only valid with its run_id |
| `kpi_id` | string |  | no |  |
| `dimension` | string |  | no | availability, inventory_efficiency, procurement_efficiency, decision_quality, policy_comparison or financial_impact |
| `kpi_name` | string |  | no |  |
| `formula` | string |  | no |  |
| `numerator` | float |  | yes |  |
| `denominator` | float |  | yes |  |
| `value` | float |  | yes | Blank when NOT_COMPUTED |
| `unit` | string |  | yes |  |
| `population` | string |  | no |  |
| `population_n` | float |  | yes |  |
| `scenario` | string |  | no |  |
| `demand_scenario` | string |  | yes |  |
| `pr_view` | string |  | yes |  |
| `policy` | string |  | yes |  |
| `run_set` | string |  | yes |  |
| `result_type` | string |  | yes |  |
| `source` | string |  | no |  |
| `interpretation` | string |  | no |  |
| `limitations` | string |  | no |  |
| `status` | enum |  | no | COMPUTED or NOT_COMPUTED |
| `output_class` | enum |  | no | sample, historical_descriptive, rule_derived, statistical_forecast, deterministic_simulation, stochastic_simulation or not_computed |

## `eng_scenario_comparison.csv`

- **Grain:** One row per comparison type, material, view, demand scenario, policy pair and configuration
- **Primary key:** `comparison_type`, `material_no`, `pr_view`, `demand_scenario`, `policy_a`, `config_id`
- **Population:** A vs B 665. Held-out 197. MC-D 228. MC-J 139
- **Scenario identification:** scenario_a and scenario_b
- **Evidence:** Paired, so inputs are shared. Delta is arithmetic, and neither Scenario A nor B is a baseline

| Column | Type | Unit | Null allowed | Meaning |
| --- | --- | --- | --- | --- |
| `run_id` | string |  | no | Identifies the run. A number is only valid with its run_id |
| `comparison_type` | enum |  | no | demand_a_vs_b, held_out_vs_recorded, mc_d_vs_recorded or mc_j_vs_recorded |
| `material_no` | string |  | no | Material number as text. Never parse as a number |
| `pr_view` | enum |  | no | OR or ED |
| `demand_scenario` | enum |  | no | A or B. ALL if not scenario dependent. Neither is a default |
| `scenario_a` | string |  | no |  |
| `scenario_b` | string |  | no |  |
| `policy_a` | string |  | no |  |
| `policy_b` | string |  | no |  |
| `config_id` | string |  | no |  |
| `group` | string |  | no |  |
| `unit` | string | text | yes | Material unit. Quantities are never summed across units |
| `metric_a_fill_rate` | prob | ratio | yes | Fill rate of side a |
| `metric_b_fill_rate` | prob | ratio | yes | Fill rate of side b |
| `delta_unmet_qty` | float | own unit | no | a minus b |
| `delta_mean_on_hand` | float | own unit | no | a minus b |
| `delta_orders` | float | orders | no | a minus b |
| `orders_differ` | bool |  | no |  |
| `first_order_day_differs` | bool |  | yes | A vs B only |
| `order_quantity_differs` | bool |  | no |  |
| `stockout_status_differs` | bool |  | yes | Deterministic comparisons only |
| `tradeoff` | string |  | yes | Availability and inventory outcome, kept apart. Policy comparisons only |
| `output_class` | enum |  | no | sample, historical_descriptive, rule_derived, statistical_forecast, deterministic_simulation, stochastic_simulation or not_computed |

## `eng_sensitivity_summary.csv`

- **Grain:** One row per what-if, shortage rule, policy, demand scenario and view
- **Primary key:** `config_id`, `unmet_rule`, `policy`, `demand_scenario`, `pr_view`
- **Population:** 665 T3
- **Scenario identification:** Against K0 in the same scenario. A_vs_B row is the dominance check
- **Evidence:** deterministic_simulation

| Column | Type | Unit | Null allowed | Meaning |
| --- | --- | --- | --- | --- |
| `run_id` | string |  | no | Identifies the run. A number is only valid with its run_id |
| `config_id` | string |  | no |  |
| `unmet_rule` | enum |  | no | BO or LS |
| `policy` | string |  | no |  |
| `demand_scenario` | string |  | no |  |
| `pr_view` | enum |  | no | OR or ED |
| `n_materials` | int | materials | no |  |
| `materials_with_shortage` | float | materials | yes |  |
| `materials_with_shortage_base` | float | materials | yes |  |
| `shortage_status_changes` | int | materials | no |  |
| `order_count_changes` | int | materials | no |  |
| `median_abs_fill_rate_change` | float | ratio | yes |  |
| `mean_abs_fill_rate_change` | float | ratio | yes |  |
| `p90_abs_fill_rate_change` | float | ratio | yes |  |
| `median_fill_rate` | float | ratio | yes |  |
| `output_class` | enum |  | no | sample, historical_descriptive, rule_derived, statistical_forecast, deterministic_simulation, stochastic_simulation or not_computed |
| `description` | string |  | no |  |

## `eng_config_registry.csv`

- **Grain:** One row per configuration K
- **Primary key:** `config_id`
- **Population:** n/a
- **Scenario identification:** K part of scenario_id
- **Evidence:** CONFIGURED values, not estimates

| Column | Type | Unit | Null allowed | Meaning |
| --- | --- | --- | --- | --- |
| `run_id` | string |  | no | Identifies the run. A number is only valid with its run_id |
| `config_id` | string |  | no |  |
| `run_set` | string |  | no |  |
| `output_kind` | string |  | no |  |
| `description` | string |  | no |  |

## `eng_held_out_population.csv`

- **Grain:** One row per Grade A material
- **Primary key:** `material_no`
- **Population:** 228 Grade A
- **Scenario identification:** Training months only
- **Evidence:** rule_derived

| Column | Type | Unit | Null allowed | Meaning |
| --- | --- | --- | --- | --- |
| `run_id` | string |  | no | Identifies the run. A number is only valid with its run_id |
| `material_no` | string |  | no | Material number as text. Never parse as a number |
| `train_active_months` | int | months of 11 | no |  |
| `train_lead_observations` | int | lines | no |  |
| `included_in_held_out` | bool |  | no |  |
| `exclusion_reason` | string |  | yes |  |
| `output_class` | enum |  | no | sample, historical_descriptive, rule_derived, statistical_forecast, deterministic_simulation, stochastic_simulation or not_computed |

## `eng_validation_results.csv`

- **Grain:** One row per check
- **Primary key:** `stage`, `check_id`
- **Population:** n/a
- **Scenario identification:** n/a
- **Evidence:** Verification. The model cannot be validated against reality

| Column | Type | Unit | Null allowed | Meaning |
| --- | --- | --- | --- | --- |
| `run_id` | string |  | no | Identifies the run. A number is only valid with its run_id |
| `stage` | string |  | no |  |
| `check_id` | string |  | no |  |
| `expected` | string |  | no |  |
| `actual` | string |  | no |  |
| `status` | enum |  | no | PASS or FAIL |
