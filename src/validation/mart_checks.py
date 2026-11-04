"""Validation of M1, M2 and M3: reconciliation to conformed tables, grain, and scenario separation."""
from pathlib import Path

import pandas as pd

from src.config import DEMAND_IMPACT_HIGH_PCT, DEMAND_IMPACT_MATERIAL_PCT
from src.marts.build import PRIMARY_KEYS
from src.marts.dictionary import describe
from src.marts.movement_copies import SCENARIO_A, SCENARIO_B, demand_months
from src.marts.procurement import VIEWS
from src.preprocessing.conform import read_conformed, type_map
from src.preprocessing.prpo_views import DISTINCT, ORIGINAL
from src.validation.checks import result
from src.validation.conformed_checks import _same

GROUP = "marts"
SCENARIOS = (SCENARIO_A, SCENARIO_B)
# Names that would mean a rule without a definition, or a later phase's output, had entered a mart.
FORBIDDEN_NAME_PARTS = ("stockout", "stock_status", "stock_cover", "cover_months", "reorder", "safety_stock", "eoq", "forecast", "abc_class", "xyz_class", "priority_rank", "criticality_rank", "highest_criticality",
                        "supplier_rank", "actual", "lead_time", "lead_days", "amount_idr", "fx_", "due_date", "optimal", "is_foreign", "true_demand", "best_scenario", "default_view")


def _flag(series: pd.Series) -> pd.Series:
    return series.fillna(False).astype(bool)


def check_grain_and_dictionary(tables: dict[str, pd.DataFrame]) -> list[dict]:
    rows = []
    for name, keys in PRIMARY_KEYS.items():
        frame = tables[name]
        rows.append(result(f"MART-01.{name}", GROUP, name, f"Key {'+'.join(keys)} is unique and complete", 0, int(frame.duplicated(keys).sum() + frame[keys].isna().any(axis=1).sum())))
        rows.append(result(f"MART-02.{name}", GROUP, name, "Every column has a description", [], [c for c in frame.columns if describe(c) is None]))
        bad = sorted(c for c in frame.columns if any(part in c.lower() for part in FORBIDDEN_NAME_PARTS) or ("unit_amount" in c and "scenario" not in c))
        rows.append(result(f"MART-03.{name}", GROUP, name, "No column applies an undefined rule or a later phase's output", [], bad))
    for name in [n for n in tables if n.endswith(SCENARIOS)]:
        rows.append(result(f"MART-04.{name}", GROUP, name, "File holds exactly one scenario", [name.rsplit("__", 1)[1]], tables[name]["demand_scenario"].unique().tolist()))
    for name in [n for n in tables if n.endswith(VIEWS)]:
        rows.append(result(f"MART-04.{name}", GROUP, name, "File holds exactly one view", [name.rsplit("__", 1)[1]], tables[name]["analysis_view"].unique().tolist()))
    return rows


def check_classification(tables: dict[str, pd.DataFrame], conformed: dict[str, pd.DataFrame]) -> list[dict]:
    frame, fact = tables["movement_copy_classification"], conformed["fact_issue"].sort_values("source_row", kind="stable")
    name = "movement_copy_classification"
    rows = [result("MART-10.rows", GROUP, name, "Every Movement source row is present, in order", fact["source_row"].astype("int64").tolist(), frame["source_row"].astype("int64").tolist())]
    changed = [c for c in ("posting_date", "movement_type", "material_no", "quantity", "unit", "order_no", "row_hash") if not _same(fact[c], frame[c])]
    rows.append(result("MART-10.values", GROUP, name, "Source values and row hashes are unchanged", [], changed))
    rows.append(result("MART-11", GROUP, name, "Every row has a copy class and a reason", 0, int(frame[["copy_class", "copy_classification_reason"]].isna().any(axis=1).sum())))
    # Recalculated by walking the rows, separately from the labelling code.
    seen: dict[str, int] = {}
    expected_copy, expected_first = [], []
    for row_hash, source_row in zip(frame["row_hash"], frame["source_row"].astype("int64")):
        expected_copy.append(row_hash in seen)
        seen.setdefault(row_hash, source_row)
        expected_first.append(seen[row_hash])
    rows.append(result("MART-12.rule", GROUP, name, "A row is a C1 copy only if an identical row appears earlier", expected_copy, _flag(frame["is_copy_c1"]).tolist()))
    rows.append(result("MART-12.first", GROUP, name, "Each row points to its earliest identical row", expected_first, frame["first_source_row_of_group"].astype("int64").tolist()))
    eligible = _flag(frame["is_eligible_demand"])
    rows.append(result("MART-13.a", GROUP, name, "Scenario A holds exactly the eligible rows", eligible.tolist(), _flag(frame["in_scenario_a"]).tolist()))
    rows.append(result("MART-13.b", GROUP, name, "Scenario B holds exactly the eligible rows that are not C1 copies", (eligible & ~_flag(frame["is_copy_c1"])).tolist(), _flag(frame["in_scenario_b"]).tolist()))
    partial_only = _flag(frame["is_partial_dup_group"]) & (frame["occurrence_count"] == 1)
    rows.append(result("MART-14", GROUP, name, "Same key with a different quantity alone never counts as a copy", 0, int(_flag(frame["is_copy_c1"])[partial_only].sum())))
    return rows


def check_demand(tables: dict[str, pd.DataFrame], conformed: dict[str, pd.DataFrame]) -> list[dict]:
    rows = []
    fact = conformed["fact_issue"]
    # Direct sums from the conformed table, bypassing the mart's own membership columns.
    direct = {SCENARIO_A: fact, SCENARIO_B: fact[_flag(fact["in_exact_distinct_rows"])]}
    window = [m.strftime("%Y-%m-%d") for m in demand_months()]
    for scenario in SCENARIOS:
        month, summary = tables[f"mart_material_demand_month__{scenario}"], tables[f"mart_material_demand_summary__{scenario}"]
        name = f"mart_material_demand_month__{scenario}"
        rows.append(result(f"MART-20.rows.{scenario}", GROUP, name, "Rows equal materials x months", len(summary) * len(window), len(month)))
        rows.append(result(f"MART-20.window.{scenario}", GROUP, name, "Months are exactly the demand window", window, sorted(month["month"].dt.strftime("%Y-%m-%d").unique().tolist())))
        expected = direct[scenario].groupby("material_no")["quantity"].sum().astype("int64").sort_index()
        rows.append(result(f"MART-21.{scenario}", GROUP, name, "Material totals equal a direct sum of its records", {k: int(v) for k, v in expected.items()},
                           {k: int(v) for k, v in month.groupby("material_no")["qty_issued"].sum().astype("int64").sort_index().items()}))
        lines = direct[scenario].groupby(["material_no", "posting_month"]).size().sort_index()
        active = month[month["n_issue_lines"] > 0].set_index(["material_no", "month"])["n_issue_lines"].astype("int64").sort_index()
        rows.append(result(f"MART-22.{scenario}", GROUP, name, "Monthly line counts equal a direct count", lines.tolist(), active.tolist()))
        filled = _flag(month["is_zero_filled"])
        rows.append(result(f"MART-23.{scenario}", GROUP, name, "Zero-filled rows hold zeros, and other rows hold issues", 0, int((month.loc[filled, "qty_issued"] != 0).sum() + (month.loc[~filled, "n_issue_lines"] == 0).sum())))
        collapsed = month.groupby("material_no").agg(q=("qty_issued", "sum"), l=("n_issue_lines", "sum")).astype("int64").sort_index()
        ordered = summary.set_index("material_no").sort_index()
        rows.append(result(f"MART-24.{scenario}", GROUP, name, "Summary totals equal the monthly table", [collapsed["q"].tolist(), collapsed["l"].tolist()], [ordered["qty_issued_total"].astype("int64").tolist(), ordered["n_issue_lines"].astype("int64").tolist()]))
    repeats = tables[f"mart_material_demand_month__{SCENARIO_B}"]["n_repeat_lines_included"].sum()
    rows.append(result("MART-25", GROUP, "mart_material_demand_month", "Scenario B counts no C1 line", 0, int(repeats)))

    compare = tables["mart_material_demand_comparison"].set_index("material_no").sort_index()
    copies = fact[_flag(fact["is_repeat_occurrence"])].groupby("material_no")["quantity"].sum().reindex(compare.index).fillna(0).astype("int64")
    name = "mart_material_demand_comparison"
    rows.append(result("MART-26.diff", GROUP, name, "Quantity difference equals the C1 quantity of each material", copies.tolist(), compare["qty_diff_abs"].astype("int64").tolist()))
    classes = compare[["qty_copy_class_adjacent", "qty_copy_class_near", "qty_copy_class_far"]].sum(axis=1).astype("int64")
    rows.append(result("MART-26.classes", GROUP, name, "Copy classes add up to the quantity difference", copies.tolist(), classes.tolist()))
    a, b = compare["qty_scenario_a"].astype("float64"), compare["qty_scenario_b"].astype("float64")
    rows.append(result("MART-27", GROUP, name, "Percentage differences recalculate", 0, int((((a - b) / a * 100).round(4) != compare["qty_diff_pct_of_a"].astype("float64")).sum() + (((a - b) / b * 100).round(4) != compare["qty_diff_pct_of_b"].astype("float64")).sum())))
    pct = compare["qty_diff_pct_of_a"].astype("float64")
    tiers = pct.map(lambda v: "no_change" if v == 0 else "high" if v >= DEMAND_IMPACT_HIGH_PCT else "material" if v >= DEMAND_IMPACT_MATERIAL_PCT else "below_threshold")
    rows.append(result("MART-28", GROUP, name, "Impact tiers follow the stated thresholds", tiers.tolist(), compare["impact_tier"].astype("string").tolist()))
    rows.append(result("MART-29", GROUP, name, "Removing copies never changes which months are active", compare["months_with_issue"].astype("int64").tolist(), compare["months_with_issue_scenario_b"].astype("int64").tolist()))
    return rows


def check_procurement(tables: dict[str, pd.DataFrame], conformed: dict[str, pd.DataFrame]) -> list[dict]:
    rows = []
    fact = conformed["fact_prpo_line"]
    selected = {ORIGINAL: fact, DISTINCT: fact[_flag(fact["in_exact_distinct_rows"])]}
    for view in VIEWS:
        line, supplier = tables[f"mart_procurement_line__{view}"], tables[f"mart_supplier_material__{view}"]
        source = selected[view].reset_index(drop=True)
        name = f"mart_procurement_line__{view}"
        rows.append(result(f"MART-30.{view}", GROUP, name, "Lines are the same source rows as the conformed view", source["source_row"].astype("int64").tolist(), line["source_row"].astype("int64").tolist()))
        changed = [c for c in ("material_no", "pr_quantity", "po_item_amount", "currency", "pr_date", "po_delivery_date", "row_hash") if not _same(source[c], line[c])]
        rows.append(result(f"MART-31.{view}", GROUP, name, "Source values are unchanged", [], changed))
        flag = f"flag_outlier_pr_quantity__{view}"
        rows.append(result(f"MART-32.{view}", GROUP, name, "View-specific flags come from this view", source[flag].fillna(False).astype(bool).tolist(), _flag(line["flag_outlier_pr_quantity"]).tolist()))
        recalculated = (line["po_item_amount"].astype("float64") / line["pr_quantity"].astype("float64")).round(6)
        rows.append(result(f"MART-33.{view}", GROUP, name, "Implied unit amount recalculates", 0, int(((recalculated - line["implied_unit_amount_scenario"].astype("float64")).abs() > 1e-6).sum())))
        for currency, part in line.astype({"currency": "string"}).groupby("currency"):
            inside = supplier[supplier["currency"].astype("string") == currency]
            rows.append(result(f"MART-34.{view}.{currency}", GROUP, f"mart_supplier_material__{view}", f"Supplier-material amounts rebuild the line total ({currency})", round(float(part["po_item_amount"].sum()), 2), round(float(inside["po_item_amount_total"].sum()), 2)))
        rows.append(result(f"MART-35.{view}", GROUP, f"mart_supplier_material__{view}", "Supplier-material lines rebuild the line count", len(line), int(supplier["n_lines"].sum())))
        per_material = line.groupby("material_no")["pr_quantity"].sum().astype("int64").sort_index()
        rows.append(result(f"MART-36.{view}", GROUP, f"mart_supplier_material__{view}", "Quantity totals equal a direct sum within each material", per_material.tolist(), supplier.sort_values("material_no")["pr_quantity_total"].astype("int64").tolist()))
        rows.append(result(f"MART-37.{view}", GROUP, f"mart_supplier_material__{view}", "Each material has one supplier row, which lookups depend on", 0, int(supplier["material_no"].duplicated().sum())))
        before_pr = line[_flag(line["flag_promise_before_pr"])]
        used = int(supplier["n_lines_used_for_promised_interval"].sum())
        rows.append(result(f"MART-38.{view}", GROUP, f"mart_supplier_material__{view}", "Interval statistics set aside only rows promised before the PR date", len(line) - len(before_pr), used))
    return rows


def check_inventory(tables: dict[str, pd.DataFrame], conformed: dict[str, pd.DataFrame]) -> list[dict]:
    name = "mart_material_inventory"
    frame, dim = tables[name].set_index("material_no"), conformed["dim_material"].set_index("material_no")
    rows = [result("MART-40", GROUP, name, "One row for every material in dim_material", sorted(dim.index.tolist()), sorted(frame.index.tolist()))]
    aligned = frame.loc[dim.index]
    state = ("stock", "min_qty", "max_qty", "unit", "mrp_type", "n_bom_locations", "stock_eq_zero", "stock_lt_min", "stock_gt_max", "nonstock_with_stock")
    rows.append(result("MART-41", GROUP, name, "State values equal dim_material", [], [c for c in state if not _same(dim[c], aligned[c])]))
    for scenario in SCENARIOS:
        summary = tables[f"mart_material_demand_summary__{scenario}"].set_index("material_no")
        for column in ("qty_issued_total", "mean_monthly_qty", "std_monthly_qty"):
            rows.append(result(f"MART-42.{scenario}.{column}", GROUP, name, f"{column} equals the {scenario} summary", 0, int((aligned.loc[summary.index, f"{column}__{scenario}"].astype("float64") != summary[column].astype("float64")).sum())))
    for view in VIEWS:
        supplier = tables[f"mart_supplier_material__{view}"].set_index("material_no")
        rows.append(result(f"MART-43.{view}", GROUP, name, f"Procurement lines equal the {view} summary", supplier["n_lines"].astype("int64").sort_index().tolist(), aligned.loc[supplier.index, f"n_pr_lines__{view}"].astype("int64").sort_index().tolist()))
    never_issued, never_procured = ~_flag(aligned["is_issued"]), ~_flag(aligned["is_procured"])
    rows.append(result("MART-44.issued", GROUP, name, "Never-issued materials hold blanks, not zeros", 0, int(aligned.loc[never_issued, f"qty_issued_total__{SCENARIO_A}"].notna().sum() + aligned.loc[never_issued, f"qty_issued_total__{SCENARIO_B}"].notna().sum())))
    rows.append(result("MART-44.procured", GROUP, name, "Never-procured materials hold blanks, not zeros", 0, int(aligned.loc[never_procured, f"n_pr_lines__{ORIGINAL}"].notna().sum() + aligned.loc[never_procured, "supplier_code"].notna().sum())))
    return rows


def check_mart_joins(join_audit: pd.DataFrame, tables: dict[str, pd.DataFrame]) -> list[dict]:
    rows = []
    for _, entry in join_audit.iterrows():
        rows.append(result(f"JOIN.{entry['join']}.rows", "relationships", entry["join"], "Lookup keeps the left row count", int(entry["left_rows"]), int(entry["result_rows"])))
        if "mart_material_inventory" not in entry["join"]:
            rows.append(result(f"JOIN.{entry['join']}.unmatched", "relationships", entry["join"], "Every lookup key finds its parent", 0, int(entry["unmatched_rows"])))
    return rows


def check_mart_round_trip(tables: dict[str, pd.DataFrame], folder: Path) -> list[dict]:
    rows = []
    for name, frame in tables.items():
        reloaded = read_conformed(Path(folder) / f"{name}.csv", type_map(frame))
        different = [c for c in frame.columns if not _same(frame[c], reloaded[c])] if list(frame.columns) == list(reloaded.columns) else ["column list"]
        rows.append(result(f"MART-50.{name}", GROUP, name, "CSV reloads to identical values and identifiers", [], different))
    return rows


def mart_measures(tables: dict[str, pd.DataFrame]) -> dict:
    """Named measures compared with data/reference/expected_values_marts.json."""
    classification = tables["movement_copy_classification"]
    compare = tables["mart_material_demand_comparison"]
    inventory = tables["mart_material_inventory"]
    pct = compare["qty_diff_pct_of_a"].astype("float64")
    measures: dict = {f"mart.rows.{name}": len(frame) for name, frame in tables.items()}
    measures.update({
        "classification.copy_class": {k: int(v) for k, v in classification["copy_class"].value_counts().sort_index().items()},
        "classification.ineligible_rows": int((~_flag(classification["is_eligible_demand"])).sum()),
        "classification.in_scenario_a": int(_flag(classification["in_scenario_a"]).sum()), "classification.in_scenario_b": int(_flag(classification["in_scenario_b"]).sum()),
        "comparison.materials_with_any_difference": int((compare["lines_diff_abs"] > 0).sum()), "comparison.materials_above_10pct_strict": int((pct > 10).sum()), "comparison.materials_above_25pct_strict": int((pct > 25).sum()),
        "comparison.max_diff_pct": round(float(pct.max()), 2), "comparison.impact_tier": {k: int(v) for k, v in compare["impact_tier"].value_counts().sort_index().items()},
        "inventory.never_issued": int((~_flag(inventory["is_issued"])).sum()), "inventory.never_procured": int((~_flag(inventory["is_procured"])).sum()), "inventory.issued_and_procured": int((_flag(inventory["is_issued"]) & _flag(inventory["is_procured"])).sum()),
        "inventory.simulation_inputs_complete": int(inventory["simulation_inputs_missing"].isna().sum()),
    })
    for scenario in SCENARIOS:
        summary = tables[f"mart_material_demand_summary__{scenario}"].astype({"unit": "string"})
        measures[f"demand.qty_by_unit.{scenario}"] = {k: int(v) for k, v in summary.groupby("unit")["qty_issued_total"].sum().sort_index().items()}
        measures[f"demand.lines.{scenario}"] = int(summary["n_issue_lines"].sum())
    return measures
