"""Confirms validation checks actually fail when data is wrong.

Each test damages a copy of real data in memory or a temporary file. Source
workbooks are never altered.
"""
import json
import shutil

import pandas as pd
import pytest

from src.data.ingest import write_csv
from src.data.schemas import DATASETS, NOTIF, PRPO
from src.preprocessing.prpo_views import DISTINCT, ORIGINAL
from src.validation import checks
from src.validation.source_checks import checksum_status, compare_cells_with_workbook, load_audit_baseline

pytestmark = pytest.mark.data_contract


def statuses(rows, prefix):
    return [r["status"] for r in rows if r["check_id"].startswith(prefix)]


def test_changed_file_fails_the_checksum(real_build, tmp_path):
    copy = tmp_path / "BoM.xlsx"
    shutil.copy(real_build["paths"].raw / "BoM.xlsx", copy)
    assert checksum_status(copy, load_audit_baseline())["status"] == "consistent_with_audit_baseline"
    with open(copy, "ab") as handle:
        handle.write(b"\0")
    assert checksum_status(copy, load_audit_baseline())["status"] == "checksum_mismatch"


def test_missing_file_is_reported_as_missing(tmp_path):
    assert checksum_status(tmp_path / "BoM.xlsx", load_audit_baseline())["status"] == "missing"


def test_check_sources_fails_on_a_changed_workbook(real_build, real_state, tmp_path):
    for spec in DATASETS.values():
        shutil.copy(real_build["paths"].raw / spec.file_name, tmp_path / spec.file_name)
    with open(tmp_path / "FuncLoc list.xlsx", "ab") as handle:
        handle.write(b"\0")
    rows = checks.check_sources(tmp_path, real_state["inspections"])
    assert statuses(rows, "SRC-02.funcloc") == [checks.FAIL]
    assert statuses(rows, "SRC-02.bom") == [checks.PASS]


@pytest.mark.parametrize("column, new_value", [
    ("order_no", "201000000108"),      # identifier changed
    ("description", "changed text"),   # text changed
    ("notification_date", pd.Timestamp("2020-01-01")),  # date changed
])
def test_cell_comparison_detects_a_single_changed_cell(real_state, column, new_value):
    damaged = real_state["tables"]["notif"].copy()
    damaged.loc[0, column] = new_value
    sheet = real_state["inspections"]["notif"]["sheets"]["Data"]
    assert compare_cells_with_workbook(damaged, NOTIF, sheet) == {column: 1}


def test_cell_comparison_detects_a_changed_number_and_a_new_null(real_state):
    damaged = real_state["tables"]["prpo"].copy()
    damaged.loc[5, "po_item_amount"] = damaged.loc[5, "po_item_amount"] + 0.01
    damaged.loc[6, "material_desc"] = pd.NA
    sheet = real_state["inspections"]["prpo"]["sheets"]["Data"]
    assert compare_cells_with_workbook(damaged, PRPO, sheet) == {"material_desc": 1, "po_item_amount": 1}


def test_cell_comparison_detects_a_trimmed_description(real_state):
    table = real_state["tables"]["prpo"]
    damaged = table.copy()
    spaced = table.index[table["material_desc"] != table["material_desc"].str.strip()][0]
    damaged.loc[spaced, "material_desc"] = table.loc[spaced, "material_desc"].strip()
    sheet = real_state["inspections"]["prpo"]["sheets"]["Data"]
    assert compare_cells_with_workbook(damaged, PRPO, sheet) == {"material_desc": 1}


def test_row_check_fails_when_a_row_is_lost(real_state):
    tables = dict(real_state["tables"])
    tables["bom"] = tables["bom"].iloc[:-1]
    rows = checks.check_rows_and_cells(tables, real_state["inspections"])
    assert statuses(rows, "ROW-01.bom") == [checks.FAIL]
    assert statuses(rows, "ROW-03.bom") == [checks.FAIL]


def test_identifier_checks_fail_on_float_damage(real_state):
    tables = dict(real_state["tables"])
    damaged = tables["notif"].copy()
    damaged.loc[0, "order_no"] = "201000026481.0"
    tables["notif"] = damaged
    rows = checks.check_identifiers(tables)
    assert statuses(rows, "ID-01.notif.order_no") == [checks.FAIL]
    assert statuses(rows, "ID-02.notif.order_no") == [checks.FAIL]


def test_identifier_check_fails_on_lost_leading_digits(real_state):
    tables = dict(real_state["tables"])
    damaged = tables["bom"].copy()
    damaged.loc[0, "material_no"] = "100033923"
    tables["bom"] = damaged
    assert statuses(checks.check_identifiers(tables), "ID-01.bom.material_no") == [checks.FAIL]


def test_missing_value_check_fails_on_an_unexpected_blank(real_state):
    tables = dict(real_state["tables"])
    damaged = tables["movement"].copy()
    damaged.loc[0, "quantity"] = pd.NA
    tables["movement"] = damaged
    assert statuses(checks.check_missing_values(tables), "NUL-01.movement") == [checks.FAIL]


def test_missing_value_check_fails_when_status_rule_breaks(real_state):
    tables = dict(real_state["tables"])
    damaged = tables["notif"].copy()
    complete = damaged.index[damaged["status"] == "Complete"][0]
    damaged.loc[complete, "completion_date"] = pd.NaT
    tables["notif"] = damaged
    assert statuses(checks.check_missing_values(tables), "NUL-03") == [checks.FAIL]


def test_view_checks_fail_when_a_source_row_is_removed(real_state):
    views = dict(real_state["views"])
    views[ORIGINAL] = views[ORIGINAL].iloc[1:]
    rows = checks.check_duplicate_handling(real_state["tables"], real_state["labelled"], real_state["groups"], views)
    assert statuses(rows, "VIEW-01") == [checks.FAIL]
    assert statuses(rows, "VIEW-02") == [checks.FAIL]


def test_view_checks_fail_when_distinct_loses_a_row(real_state):
    views = dict(real_state["views"])
    views[DISTINCT] = views[DISTINCT].iloc[1:]
    rows = checks.check_duplicate_handling(real_state["tables"], real_state["labelled"], real_state["groups"], views)
    assert statuses(rows, "VIEW-03") == [checks.FAIL]
    assert statuses(rows, "VIEW-04") == [checks.FAIL]


def test_duplicate_check_fails_when_labelling_drops_a_row(real_state):
    labelled = dict(real_state["labelled"])
    labelled["bom"] = labelled["bom"].iloc[1:]
    rows = checks.check_duplicate_handling(real_state["tables"], labelled, real_state["groups"], real_state["views"])
    assert statuses(rows, "DUP-01.bom") == [checks.FAIL]


def test_round_trip_check_fails_on_a_changed_csv(real_build, real_state, tmp_path):
    for spec_key in DATASETS:
        shutil.copy(real_build["paths"].staged / f"stg_{spec_key}.csv", tmp_path / f"stg_{spec_key}.csv")
    damaged = real_state["tables"]["funcloc"].copy()
    damaged.loc[0, "functional_location"] = "CHANGED"
    write_csv(damaged, tmp_path / "stg_funcloc.csv")
    rows = checks.check_staged_round_trip(real_state["tables"], tmp_path)
    assert statuses(rows, "CSV-01.funcloc") == [checks.FAIL]
    assert statuses(rows, "CSV-01.bom") == [checks.PASS]


def test_expected_value_drift_fails_or_warns_by_severity(tmp_path):
    expected = tmp_path / "expected.json"
    expected.write_text(json.dumps({"measures": {
        "a.critical": {"expected": 1, "source": "t", "severity": "critical"},
        "a.warning": {"expected": 1, "source": "t", "severity": "warning"},
        "a.same": {"expected": {"x": 1}, "source": "t", "severity": "critical"},
        "a.absent": {"expected": 1, "source": "t", "severity": "warning"},
    }}))
    rows = checks.check_expected_values({"a.critical": 2, "a.warning": 2, "a.same": {"x": 1}}, expected)
    by_id = {r["check_id"]: r["status"] for r in rows}
    assert by_id == {"EXP.a.critical": checks.FAIL, "EXP.a.warning": checks.WARN, "EXP.a.same": checks.PASS, "EXP.a.absent": checks.FAIL}
