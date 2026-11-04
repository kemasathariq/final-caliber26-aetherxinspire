"""Marts on the real workbooks: recalculation without project code, and failure detection."""
import csv
import json
from collections import defaultdict
from pathlib import Path

import pandas as pd
import pytest

from src.config import PROJECT_ROOT
from src.marts.movement_copies import SCENARIO_A, SCENARIO_B
from src.preprocessing.conform import read_conformed
from src.validation import mart_checks as mc
from src.validation.checks import FAIL, PASS

pytestmark = pytest.mark.data_contract


def _csv(path):
    with open(path, newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _statuses(rows):
    return {row["check_id"]: row["status"] for row in rows}


def _copy(real_marts):
    return {name: frame.copy() for name, frame in real_marts["tables"].items()}


def test_every_mart_loads_from_disk_with_its_metadata(real_build):
    metadata = json.loads((real_build["paths"].processed / "mart_metadata.json").read_text())
    assert len(metadata["tables"]) == 13
    for name, entry in metadata["tables"].items():
        frame = read_conformed(real_build["paths"].processed / f"{name}.csv", entry["columns"])
        assert len(frame) == entry["rows"] and not frame.duplicated(entry["primary_key"]).any(), name
        assert all(entry["descriptions"].values()), name


def test_metadata_records_policies_checksums_and_parameters(real_build):
    metadata = json.loads((real_build["paths"].processed / "mart_metadata.json").read_text())
    assert len(metadata["source_checksums"]) == 6 and all(len(v) == 64 for v in metadata["source_checksums"].values())
    assert metadata["parameters"]["demand_window"] == ["2025-05", "2026-09"]
    assert set(metadata["policies"]["demand_scenarios"]) == {SCENARIO_A, SCENARIO_B}
    assert "C1" in metadata["policies"]["copy_rules"] and "synthetic" in metadata["data_label"]


def test_scenario_totals_recalculated_without_project_code(real_build):
    """From the staged CSV only: one pass for all rows, one keeping the first of identical rows."""
    totals = {SCENARIO_A: defaultdict(int), SCENARIO_B: defaultdict(int)}
    lines = {SCENARIO_A: defaultdict(int), SCENARIO_B: defaultdict(int)}
    seen = set()
    for row in _csv(real_build["root"] / "data/interim/staged/stg_movement.csv"):
        key = (row["posting_date"], row["movement_type"], row["material_no"], row["material_desc"], row["quantity"], row["unit"], row["order_no"])
        totals[SCENARIO_A][row["material_no"]] += int(row["quantity"])
        lines[SCENARIO_A][row["material_no"]] += 1
        if key not in seen:
            seen.add(key)
            totals[SCENARIO_B][row["material_no"]] += int(row["quantity"])
            lines[SCENARIO_B][row["material_no"]] += 1
    assert len(seen) == 16655
    for scenario in (SCENARIO_A, SCENARIO_B):
        mart = _csv(real_build["paths"].processed / f"mart_material_demand_summary__{scenario}.csv")
        assert {r["material_no"]: int(r["qty_issued_total"]) for r in mart} == dict(totals[scenario])
        assert {r["material_no"]: int(r["n_issue_lines"]) for r in mart} == dict(lines[scenario])


def test_monthly_values_recalculated_without_project_code(real_build):
    expected = defaultdict(int)
    for row in _csv(real_build["root"] / "data/interim/staged/stg_movement.csv"):
        expected[(row["material_no"], row["posting_date"][:7])] += int(row["quantity"])
    mart = _csv(real_build["paths"].processed / f"mart_material_demand_month__{SCENARIO_A}.csv")
    assert len(mart) == 32810
    observed = {(r["material_no"], r["month"][:7]): int(r["qty_issued"]) for r in mart if int(r["qty_issued"])}
    assert observed == dict(expected)


def test_affected_materials_recalculated_without_project_code(real_build):
    mart = _csv(real_build["paths"].processed / "mart_material_demand_comparison.csv")
    affected = {r["material_no"] for r in mart if 100 * (int(r["qty_scenario_a"]) - int(r["qty_scenario_b"])) / int(r["qty_scenario_a"]) >= 10}
    assert affected == {r["material_no"] for r in _csv(real_build["paths"].exceptions / "demand_materially_affected.csv")}
    assert len(affected) == 222


def test_procurement_totals_recalculated_without_project_code(real_build):
    totals = defaultdict(float)
    for row in _csv(real_build["root"] / "data/interim/staged/stg_prpo.csv"):
        totals[row["currency"]] += float(row["po_item_amount"])
    mart = defaultdict(float)
    for row in _csv(real_build["paths"].processed / "mart_supplier_material__original_rows.csv"):
        mart[row["currency"]] += float(row["po_item_amount_total"])
    assert {k: round(v, 2) for k, v in mart.items()} == {k: round(v, 2) for k, v in totals.items()}


def test_identifiers_in_stored_marts_have_no_numeric_damage(real_build):
    processed = real_build["paths"].processed
    for name, column, length in (("mart_material_inventory", "material_no", 10), ("movement_copy_classification", "order_no", 12), (f"mart_material_demand_month__{SCENARIO_B}", "material_no", 10), ("mart_procurement_line__original_rows", "purchase_order", 10)):
        assert all(r[column].isdigit() and len(r[column]) == length for r in _csv(processed / f"{name}.csv")), name


def test_source_rows_and_values_stay_available_for_every_excluded_record(real_marts):
    frame = real_marts["tables"]["movement_copy_classification"]
    excluded = frame[frame["in_scenario_a"] & ~frame["in_scenario_b"]]
    assert len(excluded) == 863 and excluded["copy_classification_reason"].str.contains("Rule C1").all()


def test_no_table_totals_across_units_currencies_or_scenarios(real_marts):
    assert not [c for frame in real_marts["tables"].values() for c in frame.columns if "all_currencies" in c or "all_units" in c or "combined" in c]
    assert "unit" in real_marts["unit_scenario_summary"].columns and "currency" in real_marts["currency_summary"].columns


def test_every_mart_column_is_in_the_mart_report(real_marts):
    text = Path(PROJECT_ROOT / "docs/analysis/DATA_MART_REPORT.md").read_text()
    missing = {c for frame in real_marts["tables"].values() for c in frame.columns if f"`{c}`" not in text}
    assert not missing


# Failure detection: each damages a copy of real mart data and expects a failed check.

def test_healthy_real_marts_pass_the_same_checks(real_marts, real_conformed):
    tables = _copy(real_marts)
    conformed = real_conformed["tables"]
    rows = (mc.check_grain_and_dictionary(tables) + mc.check_classification(tables, conformed) + mc.check_demand(tables, conformed) + mc.check_procurement(tables, conformed) + mc.check_inventory(tables, conformed))
    assert {row["status"] for row in rows} == {PASS}


def test_detects_a_deleted_movement_record(real_marts, real_conformed):
    tables = _copy(real_marts)
    frame = tables["movement_copy_classification"]
    tables["movement_copy_classification"] = frame[frame["occurrence_rank"] == 1].reset_index(drop=True)
    assert _statuses(mc.check_classification(tables, real_conformed["tables"]))["MART-10.rows"] == FAIL


def test_detects_a_changed_movement_quantity(real_marts, real_conformed):
    tables = _copy(real_marts)
    tables["movement_copy_classification"].loc[0, "quantity"] = 999
    assert _statuses(mc.check_classification(tables, real_conformed["tables"]))["MART-10.values"] == FAIL


def test_detects_a_missing_classification_reason(real_marts, real_conformed):
    tables = _copy(real_marts)
    tables["movement_copy_classification"].loc[0, "copy_classification_reason"] = pd.NA
    assert _statuses(mc.check_classification(tables, real_conformed["tables"]))["MART-11"] == FAIL


def test_detects_a_copy_labelled_as_unique(real_marts, real_conformed):
    tables = _copy(real_marts)
    frame = tables["movement_copy_classification"]
    frame.loc[frame["is_copy_c1"].idxmax(), "is_copy_c1"] = False
    assert _statuses(mc.check_classification(tables, real_conformed["tables"]))["MART-12.rule"] == FAIL


def test_detects_a_copy_kept_in_scenario_b(real_marts, real_conformed):
    tables = _copy(real_marts)
    frame = tables["movement_copy_classification"]
    frame.loc[frame["is_copy_c1"].idxmax(), "in_scenario_b"] = True
    assert _statuses(mc.check_classification(tables, real_conformed["tables"]))["MART-13.b"] == FAIL


def test_detects_a_record_dropped_from_scenario_a(real_marts, real_conformed):
    tables = _copy(real_marts)
    tables["movement_copy_classification"].loc[0, "in_scenario_a"] = False
    assert _statuses(mc.check_classification(tables, real_conformed["tables"]))["MART-13.a"] == FAIL


def test_detects_a_lost_demand_month(real_marts, real_conformed):
    tables = _copy(real_marts)
    name = f"mart_material_demand_month__{SCENARIO_A}"
    tables[name] = tables[name].iloc[1:]
    assert _statuses(mc.check_demand(tables, real_conformed["tables"]))[f"MART-20.rows.{SCENARIO_A}"] == FAIL


def test_detects_a_wrong_monthly_quantity(real_marts, real_conformed):
    tables = _copy(real_marts)
    month = tables[f"mart_material_demand_month__{SCENARIO_B}"]
    month.loc[month["qty_issued"].idxmax(), "qty_issued"] = 1
    results = _statuses(mc.check_demand(tables, real_conformed["tables"]))
    assert results[f"MART-21.{SCENARIO_B}"] == FAIL and results[f"MART-24.{SCENARIO_B}"] == FAIL


def test_detects_scenario_a_results_reused_as_scenario_b(real_marts, real_conformed):
    """Guards against the scenarios not being calculated independently."""
    tables = _copy(real_marts)
    tables[f"mart_material_demand_month__{SCENARIO_B}"] = tables[f"mart_material_demand_month__{SCENARIO_A}"].assign(demand_scenario=SCENARIO_B)
    results = _statuses(mc.check_demand(tables, real_conformed["tables"]))
    assert results[f"MART-21.{SCENARIO_B}"] == FAIL and results["MART-25"] == FAIL


def test_detects_zeros_extended_outside_the_window(real_marts, real_conformed):
    tables = _copy(real_marts)
    name = f"mart_material_demand_month__{SCENARIO_A}"
    extra = tables[name].iloc[[0]].assign(month=pd.Timestamp("2026-10-01"))
    tables[name] = pd.concat([tables[name], extra], ignore_index=True)
    assert _statuses(mc.check_demand(tables, real_conformed["tables"]))[f"MART-20.window.{SCENARIO_A}"] == FAIL


def test_detects_a_wrong_difference_percentage_and_tier(real_marts, real_conformed):
    tables = _copy(real_marts)
    compare = tables["mart_material_demand_comparison"]
    index = compare["qty_diff_abs"].idxmax()
    compare.loc[index, ["qty_diff_abs", "qty_diff_pct_of_a"]] = [1, 0.01]
    compare.loc[index, "impact_tier"] = "no_change"
    results = _statuses(mc.check_demand(tables, real_conformed["tables"]))
    assert results["MART-26.diff"] == FAIL and results["MART-27"] == FAIL


def test_detects_a_tier_that_ignores_the_thresholds(real_marts, real_conformed):
    tables = _copy(real_marts)
    compare = tables["mart_material_demand_comparison"]
    compare.loc[compare["qty_diff_pct_of_a"].idxmax(), "impact_tier"] = "below_threshold"
    assert _statuses(mc.check_demand(tables, real_conformed["tables"]))["MART-28"] == FAIL


def test_detects_a_duplicated_mart_key(real_marts):
    tables = _copy(real_marts)
    tables["mart_material_inventory"] = pd.concat([tables["mart_material_inventory"], tables["mart_material_inventory"].iloc[[0]]], ignore_index=True)
    assert _statuses(mc.check_grain_and_dictionary(tables))["MART-01.mart_material_inventory"] == FAIL


@pytest.mark.parametrize("column", ["stockout_flag", "reorder_point", "safety_stock", "stock_cover_months", "actual_lead_time", "amount_idr", "forecast_qty", "abc_class", "best_scenario"])
def test_detects_a_column_from_an_undefined_rule_or_later_phase(real_marts, column):
    tables = _copy(real_marts)
    tables["mart_material_inventory"][column] = 1
    assert _statuses(mc.check_grain_and_dictionary(tables))["MART-03.mart_material_inventory"] == FAIL


def test_detects_an_undescribed_column(real_marts):
    tables = _copy(real_marts)
    tables["mart_material_inventory"]["mystery"] = 1
    assert _statuses(mc.check_grain_and_dictionary(tables))["MART-02.mart_material_inventory"] == FAIL


def test_detects_scenarios_mixed_in_one_file(real_marts):
    tables = _copy(real_marts)
    tables[f"mart_material_demand_month__{SCENARIO_A}"].loc[0, "demand_scenario"] = SCENARIO_B
    assert _statuses(mc.check_grain_and_dictionary(tables))[f"MART-04.mart_material_demand_month__{SCENARIO_A}"] == FAIL


def test_detects_procurement_view_confusion(real_marts, real_conformed):
    tables = _copy(real_marts)
    tables["mart_procurement_line__exact_distinct_rows"] = tables["mart_procurement_line__original_rows"].copy()
    results = _statuses(mc.check_procurement(tables, real_conformed["tables"]))
    assert results["MART-30.exact_distinct_rows"] == FAIL and results["MART-35.exact_distinct_rows"] == FAIL


def test_detects_a_changed_amount(real_marts, real_conformed):
    tables = _copy(real_marts)
    tables["mart_procurement_line__original_rows"].loc[0, "po_item_amount"] = 1.0
    assert _statuses(mc.check_procurement(tables, real_conformed["tables"]))["MART-31.original_rows"] == FAIL


def test_detects_a_supplier_total_that_does_not_rebuild(real_marts, real_conformed):
    tables = _copy(real_marts)
    frame = tables["mart_supplier_material__original_rows"]
    frame.loc[frame["currency"].astype("string") == "IDR", "po_item_amount_total"] *= 2
    assert _statuses(mc.check_procurement(tables, real_conformed["tables"]))["MART-34.original_rows.IDR"] == FAIL


def test_detects_a_changed_stock_value(real_marts, real_conformed):
    tables = _copy(real_marts)
    tables["mart_material_inventory"].loc[0, "stock"] = 123456.0
    assert _statuses(mc.check_inventory(tables, real_conformed["tables"]))["MART-41"] == FAIL


def test_detects_zero_filled_never_issued_materials(real_marts, real_conformed):
    tables = _copy(real_marts)
    frame = tables["mart_material_inventory"]
    frame.loc[~frame["is_issued"], f"qty_issued_total__{SCENARIO_A}"] = 0
    assert _statuses(mc.check_inventory(tables, real_conformed["tables"]))["MART-44.issued"] == FAIL


def test_detects_a_join_that_multiplied_rows(real_marts):
    audit = pd.DataFrame([{"join": "x", "left_rows": 10, "result_rows": 35, "unmatched_rows": 0}])
    assert _statuses(mc.check_mart_joins(audit, real_marts["tables"]))["JOIN.x.rows"] == FAIL


def test_detects_a_mart_csv_with_damaged_identifiers(tmp_path, real_marts):
    from src.data.ingest import write_csv
    frame = real_marts["tables"]["mart_material_demand_comparison"]
    write_csv(frame.assign(material_no=frame["material_no"] + ".0"), tmp_path / "mart_material_demand_comparison.csv")
    assert _statuses(mc.check_mart_round_trip({"mart_material_demand_comparison": frame}, tmp_path))["MART-50.mart_material_demand_comparison"] == FAIL
