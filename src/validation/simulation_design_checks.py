"""Validation of the feasibility evidence: population rules, arithmetic and scope boundaries."""
import pandas as pd

from src.config import SIM_MIN_ACTIVE_MONTHS_TO_RESAMPLE_DEMAND, SIM_MIN_LINES_TO_RESAMPLE_LEAD
from src.marts.movement_copies import SCENARIO_A, SCENARIO_B
from src.simulation_design.feasibility import DESCRIPTIONS, IN_POPULATION
from src.validation.checks import result

GROUP = "simulation design"
NAME = "simulation_population"
# Names that would mean an engine, a claim about history, or a money figure had entered this stage.
FORBIDDEN_NAME_PARTS = ("simulated", "stockout", "fill_rate", "service_level", "average_inventory", "saving", "cost", "benefit", "unit_amount", "amount", "value_idr", "reorder_point", "safety_stock", "optimal", "best_scenario", "true_demand", "actual")


def check_population(population: pd.DataFrame, inventory: pd.DataFrame) -> list[dict]:
    rows = [result("SIM-01", GROUP, NAME, "One row per material in M2", sorted(inventory["material_no"].tolist()), sorted(population["material_no"].tolist()))]
    rule = (inventory.set_index("material_no")["mrp_type"].astype("string") == "Stock Item") & inventory.set_index("material_no")["simulation_inputs_missing"].isna()
    members = population.set_index("material_no")["population_status"] == IN_POPULATION
    rows.append(result("SIM-02", GROUP, NAME, "Population equals Stock Items with no missing input, recalculated from M2", sorted(rule[rule].index.tolist()), sorted(members[members].index.tolist())))
    excluded = population[population["population_status"] != IN_POPULATION]
    rows.append(result("SIM-03", GROUP, NAME, "Every excluded material states a reason, and no member does", [0, 0], [int(excluded["exclusion_reasons"].isna().sum()), int(population.loc[population["population_status"] == IN_POPULATION, "exclusion_reasons"].notna().sum())]))
    bad = sorted(c for c in population.columns if any(part in c.lower() for part in FORBIDDEN_NAME_PARTS))
    rows.append(result("SIM-04", GROUP, NAME, "No simulated result, historical stockout claim or money figure exists at this stage", [], bad))
    rows.append(result("SIM-05", GROUP, NAME, "Every column has a description", [], [c for c in population.columns if c not in DESCRIPTIONS]))
    return rows


def check_arithmetic(population: pd.DataFrame, inventory: pd.DataFrame) -> list[dict]:
    frame = population[population["population_status"] == IN_POPULATION].set_index("material_no").sort_index()
    source = inventory.set_index("material_no").loc[frame.index]
    stock, low, high = source["stock"].astype("float64"), source["min_qty"].astype("float64"), source["max_qty"].astype("float64")
    rows = [result("SIM-10", GROUP, NAME, "Initial inventory and parameters equal M2, unchanged", [stock.tolist(), low.tolist(), high.tolist()],
                   [frame["assumed_initial_inventory"].astype("float64").tolist(), frame["min_parameter_unverified"].astype("float64").tolist(), frame["max_parameter_unverified"].astype("float64").tolist()])]
    for scenario in (SCENARIO_A, SCENARIO_B):
        total = source[f"qty_issued_total__{scenario}"].astype("float64")
        rows.append(result(f"SIM-11.{scenario}", GROUP, NAME, f"Never-reaches-Min flag recalculates ({scenario})", ((stock - total) > low).tolist(), frame[f"stays_above_min__{scenario}"].astype(bool).tolist()))
    active = source["months_with_issue"].astype("int64")
    rows.append(result("SIM-12.demand", GROUP, NAME, "Demand resampling is allowed only with enough active months", (active >= SIM_MIN_ACTIVE_MONTHS_TO_RESAMPLE_DEMAND).tolist(), frame["resampling_allowed_demand"].astype(bool).tolist()))
    lead = frame["lead_observations_distinct"].astype("int64")
    rows.append(result("SIM-12.lead", GROUP, NAME, "Lead resampling is allowed only with enough distinct observations", (lead >= SIM_MIN_LINES_TO_RESAMPLE_LEAD).tolist(), frame["resampling_allowed_lead"].astype(bool).tolist()))
    rows.append(result("SIM-13", GROUP, NAME, "Every member has an evidence tier and a lead proxy", 0, int(frame[["demand_evidence_tier", "lead_evidence_tier", "lead_proxy_median_days__exact_distinct_rows", "lead_proxy_median_days__original_rows"]].isna().any(axis=1).sum())))
    rows.append(result("SIM-14", GROUP, NAME, "Dropping the unit amount condition would not change the population, so no decision rests on unit amounts", 0,
                       int((inventory["mrp_type"].astype("string").eq("Stock Item") & inventory["promised_interval_days_median__original_rows"].notna() & inventory["implied_unit_amount_scenario_median__original_rows"].isna()).sum())))
    return rows


def simulation_design_measures(population: pd.DataFrame, summary: pd.DataFrame) -> dict:
    measures = {f"sim_design.{row.condition}": int(row.materials) for row in summary.itertuples()}
    measures["sim_design.rows"] = len(population)
    measures["sim_design.excluded"] = int((population["population_status"] != IN_POPULATION).sum())
    return measures
