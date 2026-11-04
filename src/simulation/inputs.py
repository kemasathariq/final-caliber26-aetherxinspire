"""Load engine inputs from the validated marts, read-only. Nothing is written to data/processed outside data/processed/engine."""
import hashlib
from dataclasses import dataclass

import numpy as np
import pandas as pd

from src.simulation import settings as cfg

IDS = {"material_no": "string"}
HORIZON_START = pd.Timestamp(cfg.HORIZON[0])
SOURCE_FILES = ["simulation_population.csv", "movement_copy_classification.csv", "mart_material_inventory.csv", "mart_material_demand_summary__scenario_a.csv",
                "mart_material_demand_summary__scenario_b.csv", "mart_material_demand_month__scenario_a.csv", "mart_material_demand_month__scenario_b.csv",
                "mart_procurement_line__original_rows.csv", "mart_procurement_line__exact_distinct_rows.csv", "mart_supplier_material__original_rows.csv",
                "mart_supplier_material__exact_distinct_rows.csv", "mart_metadata.json", "simulation_population_metadata.json"]


def sha256(path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def input_checksums(processed=cfg.PROCESSED_DIR) -> dict:
    return {name: sha256(processed / name) for name in SOURCE_FILES}


@dataclass
class EngineInputs:
    inventory: pd.DataFrame            # All 7,481 materials, indexed by material_no.
    population: pd.DataFrame           # All 7,481 materials, indexed by material_no.
    t3: pd.DataFrame                   # The 665 materials with engine parameters.
    grade_a: list                      # 228 materials: T3 with at least 6 active months.
    lines: dict                        # (demand, material) -> [(day, qty, source_row, at_peak)] in date and source_row order.
    lead_obs: dict                     # view -> material -> sorted array of promised intervals, before-PR lines left out.
    procurement: dict                  # view -> line table.
    supplier: dict                     # view -> supplier mart.
    summary: dict                      # demand -> demand summary mart.
    months: dict                       # demand -> materials x 17 months array frame.
    checksums: dict


def load_inputs(processed=cfg.PROCESSED_DIR) -> EngineInputs:
    population = pd.read_csv(processed / "simulation_population.csv", dtype=IDS | {"exclusion_reasons": "string"}, keep_default_na=False, na_values=[""], low_memory=False).set_index("material_no")
    inventory = pd.read_csv(processed / "mart_material_inventory.csv", dtype=IDS, keep_default_na=False, na_values=[""], low_memory=False).set_index("material_no")
    t3 = population[population.population_status == "in_population"].copy()
    for view in cfg.PR_VIEWS.values():
        t3[f"lead_p90__{view}"] = inventory.loc[t3.index, f"promised_interval_days_p90__{view}"]
        t3[f"pr_qty_median__{view}"] = inventory.loc[t3.index, f"pr_quantity_median__{view}"]
        t3[f"lead_median__{view}"] = inventory.loc[t3.index, f"promised_interval_days_median__{view}"]
    grade_a = sorted(t3.index[t3.active_months >= cfg.MIN_ACTIVE_MONTHS])

    movement = pd.read_csv(processed / "movement_copy_classification.csv", dtype=IDS, usecols=["source_row", "posting_date", "material_no", "quantity", "in_scenario_a", "in_scenario_b", "flag_at_repeated_unit_maximum"], parse_dates=["posting_date"])
    movement = movement.sort_values(["posting_date", "source_row"], kind="stable")
    movement["day"] = (movement.posting_date - HORIZON_START).dt.days
    lines = {}
    for demand, flag in (("A", "in_scenario_a"), ("B", "in_scenario_b")):
        chosen = movement[movement[flag]]
        for material, group in chosen.groupby("material_no", sort=False):
            lines[(demand, material)] = list(zip(group.day.tolist(), group.quantity.tolist(), group.source_row.tolist(), group.flag_at_repeated_unit_maximum.tolist()))

    procurement, supplier, lead_obs = {}, {}, {}
    for view in cfg.PR_VIEWS.values():
        table = pd.read_csv(processed / f"mart_procurement_line__{view}.csv", dtype=IDS | {"supplier_code": "string"}, keep_default_na=False, na_values=[""], low_memory=False, parse_dates=["pr_date", "pr_delivery_date", "po_delivery_date"])
        procurement[view] = table
        supplier[view] = pd.read_csv(processed / f"mart_supplier_material__{view}.csv", dtype=IDS | {"supplier_code": "string"}, keep_default_na=False, na_values=[""], low_memory=False)
        usable = table[table.promised_interval_days >= 0]  # Design 9.3: lines promised before the PR date are left out.
        lead_obs[view] = {m: np.sort(g.to_numpy(dtype=float)) for m, g in usable.groupby("material_no").promised_interval_days}

    summary, months = {}, {}
    for demand, name in cfg.DEMAND_SCENARIOS.items():
        summary[demand] = pd.read_csv(processed / f"mart_material_demand_summary__{name}.csv", dtype=IDS, keep_default_na=False, na_values=[""], low_memory=False).set_index("material_no")
        table = pd.read_csv(processed / f"mart_material_demand_month__{name}.csv", dtype=IDS, usecols=["material_no", "month", "qty_issued"], parse_dates=["month"])
        table["month"] = table.month.dt.strftime("%Y-%m")
        months[demand] = table.pivot(index="material_no", columns="month", values="qty_issued")[cfg.MONTHS]
    return EngineInputs(inventory, population, t3, grade_a, lines, lead_obs, procurement, supplier, summary, months, input_checksums(processed))


def material_lines(inputs: EngineInputs, demand: str, material: str, peak_lines: str = "keep") -> list[tuple[int, float]]:
    rows = inputs.lines.get((demand, material), [])
    return [(d, float(q)) for d, q, _, at_peak in rows if peak_lines == "keep" or not at_peak]


def reconcile(inputs: EngineInputs) -> list[dict]:
    """Inputs against M1, M2 and M3. Design section 12.1. Returns check rows."""
    rows = []

    def add(check, expected, actual):
        rows.append({"check_id": check, "expected": str(expected), "actual": str(actual), "status": "PASS" if expected == actual else "FAIL"})

    add("population_all_materials", 7481, len(inputs.population))
    add("population_t3", 665, len(inputs.t3))
    add("grade_a_materials", 228, len(inputs.grade_a))
    add("lines_scenario_a", 17518, sum(len(v) for k, v in inputs.lines.items() if k[0] == "A"))
    add("lines_scenario_b", 16655, sum(len(v) for k, v in inputs.lines.items() if k[0] == "B"))
    add("prpo_original_rows", 11609, len(inputs.procurement["original_rows"]))
    add("prpo_exact_distinct_rows", 6189, len(inputs.procurement["exact_distinct_rows"]))
    for demand, column in (("A", "qty_total__scenario_a"), ("B", "qty_total__scenario_b")):
        bad = sum(1 for m, row in inputs.t3.iterrows() if sum(q for _, q, _, _ in inputs.lines.get((demand, m), [])) != row[column])
        add(f"t3_issue_quantity_matches_population_{demand}", 0, bad)
    for view in cfg.PR_VIEWS.values():
        bad = sum(1 for m, row in inputs.t3.iterrows() if not np.isclose(np.median(inputs.lead_obs[view][m]), row[f"lead_proxy_median_days__{view}"]))
        add(f"t3_lead_median_matches_population_{view}", 0, bad)
    add("lead_resampling_eligible", 140, int((inputs.t3.lead_observations_distinct >= cfg.MIN_LEAD_OBSERVATIONS).sum()))
    add("joint_resampling_eligible", 139, int(((inputs.t3.lead_observations_distinct >= cfg.MIN_LEAD_OBSERVATIONS) & (inputs.t3.active_months >= cfg.MIN_ACTIVE_MONTHS)).sum()))
    add("t3_integer_stock_and_issues", 0, int((inputs.t3.assumed_initial_inventory % 1 != 0).sum()))
    add("t3_positive_pr_median", 0, sum(int((inputs.t3[f"pr_qty_median__{v}"] <= 0).sum()) for v in cfg.PR_VIEWS.values()))
    return rows
