"""Builds M1, M2 and M3 from conformed tables, in dependency order: M1 and M3 feed M2."""
import pandas as pd

from src.marts.demand import build_demand_month, build_demand_summary, compare_scenarios, impact_sensitivity, unit_scenario_summary
from src.marts.inventory import build_inventory, procurement_issue_reconciliation
from src.marts.movement_copies import SCENARIO_A, SCENARIO_B, classify_movement_copies
from src.marts.procurement import VIEWS, build_nonidr, build_procurement_line, build_supplier_material, currency_summary
from src.preprocessing.conform import normalise_types
from src.preprocessing.prpo_views import DISTINCT, ORIGINAL

GRAINS = {
    f"mart_procurement_line__{ORIGINAL}": "One PR PO source row", f"mart_procurement_line__{DISTINCT}": "One PR item and one PO item, after setting aside exact copies",
    f"mart_supplier_material__{ORIGINAL}": "One supplier, material and currency", f"mart_supplier_material__{DISTINCT}": "One supplier, material and currency",
    f"mart_procurement_nonidr__{ORIGINAL}": "One non-IDR PR PO source row", f"mart_procurement_nonidr__{DISTINCT}": "One non-IDR PR item and PO item",
    "mart_material_inventory": "One material", "movement_copy_classification": "One Movement source row",
    f"mart_material_demand_month__{SCENARIO_A}": "One issued material by calendar month", f"mart_material_demand_month__{SCENARIO_B}": "One issued material by calendar month",
    f"mart_material_demand_summary__{SCENARIO_A}": "One issued material", f"mart_material_demand_summary__{SCENARIO_B}": "One issued material",
    "mart_material_demand_comparison": "One issued material",
}
PRIMARY_KEYS = {
    f"mart_procurement_line__{ORIGINAL}": ["source_row"], f"mart_procurement_line__{DISTINCT}": ["purchase_requisition", "pr_item"],
    f"mart_supplier_material__{ORIGINAL}": ["supplier_code", "material_no", "currency"], f"mart_supplier_material__{DISTINCT}": ["supplier_code", "material_no", "currency"],
    f"mart_procurement_nonidr__{ORIGINAL}": ["source_row"], f"mart_procurement_nonidr__{DISTINCT}": ["purchase_requisition", "pr_item"],
    "mart_material_inventory": ["material_no"], "movement_copy_classification": ["source_row"],
    f"mart_material_demand_month__{SCENARIO_A}": ["material_no", "month"], f"mart_material_demand_month__{SCENARIO_B}": ["material_no", "month"],
    f"mart_material_demand_summary__{SCENARIO_A}": ["material_no"], f"mart_material_demand_summary__{SCENARIO_B}": ["material_no"],
    "mart_material_demand_comparison": ["material_no"],
}


def build_marts(conformed: dict[str, pd.DataFrame]) -> dict:
    audit: list[dict] = []
    dim_material, fact_prpo, fact_issue = conformed["dim_material"], conformed["fact_prpo_line"], conformed["fact_issue"]
    lines = {view: build_procurement_line(fact_prpo, dim_material, view, audit) for view in VIEWS}
    supplier_material = {view: build_supplier_material(lines[view], view) for view in VIEWS}
    classification = classify_movement_copies(fact_issue, dim_material)
    months = {s: build_demand_month(classification, s, dim_material, audit) for s in (SCENARIO_A, SCENARIO_B)}
    summaries = {s: build_demand_summary(months[s], classification, s, audit) for s in (SCENARIO_A, SCENARIO_B)}
    comparison = compare_scenarios(summaries[SCENARIO_A], summaries[SCENARIO_B], months[SCENARIO_A], months[SCENARIO_B], classification)
    inventory = build_inventory(dim_material, summaries, comparison, supplier_material, audit)
    tables = {"movement_copy_classification": classification, "mart_material_demand_comparison": comparison, "mart_material_inventory": inventory}
    for view in VIEWS:
        tables[f"mart_procurement_line__{view}"] = lines[view]
        tables[f"mart_supplier_material__{view}"] = supplier_material[view]
        tables[f"mart_procurement_nonidr__{view}"] = build_nonidr(lines[view])
    for scenario in (SCENARIO_A, SCENARIO_B):
        tables[f"mart_material_demand_month__{scenario}"] = months[scenario]
        tables[f"mart_material_demand_summary__{scenario}"] = summaries[scenario]
    tables = {name: normalise_types(tables[name]) for name in GRAINS}
    return {"tables": tables, "join_audit": pd.DataFrame(audit), "currency_summary": currency_summary(lines),
            "unit_scenario_summary": unit_scenario_summary(summaries[SCENARIO_A], summaries[SCENARIO_B]), "impact_sensitivity": impact_sensitivity(tables["mart_material_demand_comparison"]),
            "procurement_issue_reconciliation": procurement_issue_reconciliation(tables["mart_material_inventory"])}
