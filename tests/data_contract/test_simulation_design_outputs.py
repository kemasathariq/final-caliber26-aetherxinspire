"""Feasibility evidence on the real data: recalculation without project code, failure detection, boundaries."""
import csv
import json
from pathlib import Path

import pandas as pd
import pytest

from src.config import PROJECT_ROOT
from src.simulation_design.feasibility import build_simulation_population
from src.validation import simulation_design_checks as sc
from src.validation.checks import FAIL, PASS

pytestmark = pytest.mark.data_contract
DOCS = PROJECT_ROOT / "docs/analysis"


def _csv(path):
    with open(path, newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


@pytest.fixture(scope="module")
def population(real_marts):
    t = real_marts["tables"]
    return build_simulation_population(t["mart_material_inventory"], t["mart_material_demand_summary__scenario_b"], t["mart_supplier_material__exact_distinct_rows"])


def _statuses(rows):
    return {row["check_id"]: row["status"] for row in rows}


def test_population_recalculated_without_project_code(real_build):
    rows = _csv(real_build["paths"].processed / "mart_material_inventory.csv")
    expected = {r["material_no"] for r in rows if r["mrp_type"] == "Stock Item" and r["simulation_inputs_missing"] == ""}
    stored = _csv(real_build["paths"].processed / "simulation_population.csv")
    assert len(expected) == 665 and len(stored) == 7481
    assert {r["material_no"] for r in stored if r["population_status"] == "in_population"} == expected
    assert all(r["exclusion_reasons"] for r in stored if r["population_status"] == "excluded")


def test_arithmetic_recalculated_without_project_code(real_build):
    never_a = never_b = trigger = conflict = 0
    for r in _csv(real_build["paths"].processed / "simulation_population.csv"):
        if r["population_status"] != "in_population":
            continue
        stock, low, high = float(r["assumed_initial_inventory"]), float(r["min_parameter_unverified"]), float(r["max_parameter_unverified"])
        never_a += stock - float(r["qty_total__scenario_a"]) > low
        never_b += stock - float(r["qty_total__scenario_b"]) > low
        trigger += stock <= low
        conflict += float(r["max_line_qty__scenario_a"]) > high
    assert (never_a, never_b, trigger, conflict) == (125, 133, 183, 173)


def test_largest_line_is_the_same_in_both_scenarios(real_marts):
    t = real_marts["tables"]
    a = t["mart_material_demand_summary__scenario_a"].set_index("material_no")["max_line_qty"]
    b = t["mart_material_demand_summary__scenario_b"].set_index("material_no")["max_line_qty"]
    assert a.equals(b.loc[a.index])


def test_dropping_the_unit_amount_condition_leaves_the_population_unchanged(real_marts):
    inventory = real_marts["tables"]["mart_material_inventory"]
    missing = inventory["simulation_inputs_missing"].fillna("").str.replace("unit_amount", "").str.strip(";")
    without = (inventory["mrp_type"].astype("string") == "Stock Item") & (missing.str.replace(";;", ";") == "")
    assert int(without.sum()) == 665


def test_population_file_holds_no_money_or_simulated_result(real_build):
    header = list(_csv(real_build["paths"].processed / "simulation_population.csv")[0])
    assert not [c for c in header if "amount" in c or "cost" in c or "simulated" in c or "stockout" in c]


def test_metadata_states_that_nothing_is_simulated(real_build):
    metadata = json.loads((real_build["paths"].processed / "simulation_population_metadata.json").read_text())
    assert "No simulation has been run" in metadata["status"]
    assert set(metadata["columns"]) == set(metadata["descriptions"])


def test_no_simulation_engine_or_result_file_exists(real_build):
    assert not list(Path(PROJECT_ROOT / "src").rglob("*engine*"))
    names = [p.name for folder in (real_build["paths"].processed, real_build["paths"].tables, real_build["paths"].exceptions) for p in folder.iterdir()]
    assert not [n for n in names if "sim_result" in n or "simulation_result" in n or "stockout" in n]


@pytest.mark.parametrize("name", ["SIMULATION_DESIGN_SPECIFICATION.md", "SIMULATION_INPUT_ASSUMPTION_REGISTER.md", "SIMULATION_FEASIBILITY_ASSESSMENT.md"])
def test_design_documents_state_the_case_limit_and_the_synthetic_label(name):
    text = (DOCS / name).read_text()
    assert "Case 3" in text and "not confirmed" in text
    assert "synthetic" in text


def test_design_specification_has_every_required_part():
    text = (DOCS / "SIMULATION_DESIGN_SPECIFICATION.md").read_text()
    for heading in ("Event-flow description", "Mathematical model and formulas", "Scenario design", "Validation and testing strategy", "Method evaluation", "Performance measures", "Worked example"):
        assert heading in text, heading


def test_every_population_column_is_documented(population):
    text = (DOCS / "SIMULATION_INPUT_ASSUMPTION_REGISTER.md").read_text()
    assert not [c for c in population.columns if f"`{c}`" not in text]


# Failure detection

def test_healthy_population_passes(population, real_marts):
    inventory = real_marts["tables"]["mart_material_inventory"]
    assert {r["status"] for r in sc.check_population(population, inventory) + sc.check_arithmetic(population, inventory)} == {PASS}


def test_detects_a_material_dropped_from_the_status_table(population, real_marts):
    damaged = population[population["population_status"] == "in_population"]
    assert _statuses(sc.check_population(damaged, real_marts["tables"]["mart_material_inventory"]))["SIM-01"] == FAIL


def test_detects_an_excluded_material_placed_in_the_population(population, real_marts):
    damaged = population.copy()
    damaged.loc[damaged["population_status"] == "excluded", "population_status"] = "in_population"
    assert _statuses(sc.check_population(damaged, real_marts["tables"]["mart_material_inventory"]))["SIM-02"] == FAIL


def test_detects_an_exclusion_without_a_reason(population, real_marts):
    damaged = population.copy()
    damaged.loc[damaged["population_status"] == "excluded", "exclusion_reasons"] = pd.NA
    assert _statuses(sc.check_population(damaged, real_marts["tables"]["mart_material_inventory"]))["SIM-03"] == FAIL


@pytest.mark.parametrize("column", ["simulated_stockout_days", "fill_rate", "service_level", "cost_saving", "implied_unit_amount_scenario", "safety_stock", "true_demand"])
def test_detects_a_result_or_money_column_at_this_stage(population, real_marts, column):
    damaged = population.assign(**{column: 1})
    assert _statuses(sc.check_population(damaged, real_marts["tables"]["mart_material_inventory"]))["SIM-04"] == FAIL


def test_detects_a_changed_initial_inventory(population, real_marts):
    damaged = population.copy()
    index = damaged[damaged["population_status"] == "in_population"].index[0]
    damaged.loc[index, "assumed_initial_inventory"] = 99999.0
    assert _statuses(sc.check_arithmetic(damaged, real_marts["tables"]["mart_material_inventory"]))["SIM-10"] == FAIL


def test_detects_a_wrong_reorder_flag(population, real_marts):
    damaged = population.copy()
    damaged["stays_above_min__scenario_b"] = ~damaged["stays_above_min__scenario_b"].fillna(False)
    assert _statuses(sc.check_arithmetic(damaged, real_marts["tables"]["mart_material_inventory"]))["SIM-11.scenario_b"] == FAIL


def test_detects_resampling_allowed_without_evidence(population, real_marts):
    damaged = population.copy()
    damaged["resampling_allowed_demand"] = True
    assert _statuses(sc.check_arithmetic(damaged, real_marts["tables"]["mart_material_inventory"]))["SIM-12.demand"] == FAIL
