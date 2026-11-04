"""Repeatable validation checks. Each returns result rows; none alters data.

A critical failure means the build's foundation cannot be trusted. A warning
means an observed count moved from its documented value and needs review.
Results are always written, including failures.
"""
import json

from pathlib import Path

import pandas as pd

from src.config import EXPECTED_VALUES_FILE
from src.data.ingest import read_staged
from src.data.schemas import DATASETS, LINEAGE_COLUMNS
from src.data.workbook_inspect import sheet_header, storage_types_by_column
from src.preprocessing.prpo_views import DISTINCT, ORIGINAL
from src.validation.source_checks import checksum_status, compare_cells_with_workbook, load_audit_baseline

PASS, FAIL, WARN = "PASS", "FAIL", "WARN"

# The only columns allowed to contain blanks, with the rule that explains them.
ALLOWED_NULLS = {
    ("notif", "order_no"): 553,
    ("notif", "completion_date"): 1305,
    ("funcloc", "criticality"): 33,
}


def _normalise(value):
    return json.loads(json.dumps(value, sort_keys=True, default=str))


def result(check_id: str, group: str, dataset: str, description: str, expected, observed,
           severity: str = "critical", source: str = "") -> dict:
    passed = _normalise(expected) == _normalise(observed)
    return {
        "check_id": check_id, "group": group, "dataset": dataset, "description": description,
        "expected": json.dumps(_normalise(expected), sort_keys=True),
        "observed": json.dumps(_normalise(observed), sort_keys=True),
        "severity": severity, "status": PASS if passed else (FAIL if severity == "critical" else WARN),
        "source": source,
    }


def check_sources(raw_dir: Path, inspections: dict[str, dict]) -> list[dict]:
    baseline = load_audit_baseline()
    rows = []
    for key, spec in DATASETS.items():
        path = Path(raw_dir) / spec.file_name
        status = checksum_status(path, baseline)
        rows.append(result(f"SRC-01.{key}", "accessibility", spec.name, "Workbook exists in data/raw", True, status["exists"]))
        rows.append(result(f"SRC-02.{key}", "checksum", spec.name, "SHA-256 matches the audit baseline",
                           baseline.get(spec.file_name), status["sha256"]))
        sheets = inspections[key]["sheets"]
        rows.append(result(f"SRC-03.{key}", "worksheets", spec.name, "Worksheet list is exactly ['Data']", [spec.sheet], list(sheets)))
        sheet = sheets[spec.sheet]
        structure = {"state": sheet["state"], "hidden_rows": sheet["hidden_rows"], "hidden_columns": sheet["hidden_columns"],
                     "formula_cells": sheet["formula_cells"], "merged_ranges": sheet["merged_ranges"],
                     "row_number_gaps": sheet["row_gaps"], "external_links": inspections[key]["external_links"],
                     "date1904": inspections[key]["date1904"]}
        rows.append(result(f"SRC-04.{key}", "worksheets", spec.name, "No hidden content, formulas, merged cells, row gaps or external links",
                           {"state": "visible", "hidden_rows": 0, "hidden_columns": 0, "formula_cells": 0, "merged_ranges": 0,
                            "row_number_gaps": 0, "external_links": 0, "date1904": False}, structure))
        rows.append(result(f"SCH-01.{key}", "columns", spec.name, "Header names and order match the schema",
                           spec.source_columns, sheet_header(sheet)))
    return rows


def check_storage_and_types(tables: dict[str, pd.DataFrame], inspections: dict[str, dict]) -> list[dict]:
    expected_dtype = {"identifier": "string", "text": "string", "category": "category",
                      "integer": "Int64", "float": "Float64", "date": "datetime64[ns]"}
    rows = []
    for key, spec in DATASETS.items():
        table = tables[key]
        storage = storage_types_by_column(inspections[key]["sheets"][spec.sheet])
        wrong_storage, wrong_dtype = {}, {}
        for column in spec.columns:
            allowed = {"inlineStr", "s"} if column.kind in ("identifier", "text", "category") else {"n"}
            kinds = set(storage[column.source]) - {"blank"}
            if not kinds <= allowed:
                wrong_storage[column.source] = sorted(kinds)
            if str(table[column.standard].dtype).split("(")[0] != expected_dtype[column.kind]:
                wrong_dtype[column.standard] = str(table[column.standard].dtype)
        rows.append(result(f"TYP-01.{key}", "data types", spec.name, "Physical cell storage matches the column kind", {}, wrong_storage))
        rows.append(result(f"TYP-02.{key}", "data types", spec.name, "Staged column types match the schema", {}, wrong_dtype))
        rows.append(result(f"TYP-03.{key}", "data types", spec.name, "Date columns have no time component", 0,
                           sum(int((table[c].dropna() != table[c].dropna().dt.normalize()).sum()) for c in spec.by_kind("date"))))
        rows.append(result(f"TYP-04.{key}", "data types", spec.name, "Category columns are unordered, so no ranking is implied", [],
                           [c for c in spec.by_kind("category") if table[c].cat.ordered]))
    return rows


def check_rows_and_cells(tables: dict[str, pd.DataFrame], inspections: dict[str, dict]) -> list[dict]:
    rows = []
    for key, spec in DATASETS.items():
        table = tables[key]
        sheet = inspections[key]["sheets"][spec.sheet]
        data_rows = sheet["rows"][1:]
        rows.append(result(f"ROW-01.{key}", "row preservation", spec.name, "Staged rows equal workbook data rows", len(data_rows), len(table)))
        rows.append(result(f"ROW-02.{key}", "row preservation", spec.name, "source_row equals the workbook's own row numbers",
                           [n for n, _ in data_rows], table["source_row"].astype("int64").tolist()) | {"expected": str(len(data_rows)) + " row numbers", "observed": str(len(table)) + " row numbers"})
        rows.append(result(f"ROW-03.{key}", "row preservation", spec.name, "Every staged cell equals the workbook XML (independent reader)", {},
                           compare_cells_with_workbook(table, spec, sheet)))
        lineage = {"source_file": sorted(table["source_file"].unique().tolist()), "source_sheet": sorted(table["source_sheet"].unique().tolist())}
        rows.append(result(f"ROW-04.{key}", "lineage", spec.name, "Lineage names the source workbook and worksheet",
                           {"source_file": [spec.file_name], "source_sheet": [spec.sheet]}, lineage))
        rows.append(result(f"ROW-05.{key}", "lineage", spec.name, "Every row has a 64-character row hash", 0,
                           int((~table["row_hash"].fillna("").str.fullmatch(r"[0-9a-f]{64}")).sum())))
    return rows


def check_identifiers(tables: dict[str, pd.DataFrame]) -> list[dict]:
    rows = []
    for key, spec in DATASETS.items():
        table = tables[key]
        for column in spec.columns:
            if column.kind != "identifier":
                continue
            values = table[column.standard].dropna().astype("string")
            name = f"{spec.name}.{column.source}"
            if column.id_pattern:
                bad = int((~values.str.fullmatch(column.id_pattern)).sum())
                rows.append(result(f"ID-01.{key}.{column.standard}", "identifier integrity", name, f"All values match pattern {column.id_pattern}", 0, bad))
            damaged = int(values.str.fullmatch(r"\d+\.\d*|\d+(\.\d+)?[eE][+-]?\d+").sum())
            rows.append(result(f"ID-02.{key}.{column.standard}", "identifier integrity", name, "No float or scientific-notation damage", 0, damaged))
            rows.append(result(f"ID-03.{key}.{column.standard}", "identifier integrity", name, "No leading or trailing spaces", 0, int((values != values.str.strip()).sum())))
    return rows


def check_missing_values(tables: dict[str, pd.DataFrame]) -> list[dict]:
    rows = []
    for key, spec in DATASETS.items():
        observed = {c: int(tables[key][c].isna().sum()) for c in spec.standard_columns if tables[key][c].isna().any()}
        expected = {c: n for (k, c), n in ALLOWED_NULLS.items() if k == key}
        rows.append(result(f"NUL-01.{key}", "missing values", spec.name, "Blanks occur only in the documented columns and counts", expected, observed))
        rows.append(result(f"NUL-02.{key}", "missing values", spec.name, "No lineage value is missing", 0, int(tables[key][list(LINEAGE_COLUMNS)].isna().sum().sum())))
    notif, funcloc = tables["notif"], tables["funcloc"]
    open_rows = notif["status"].astype("string") == "In Progress"
    rows.append(result("NUL-03", "missing values", "Notif History", "Completion date is blank exactly on In Progress rows", 0,
                       int((notif["completion_date"].isna() != open_rows).sum())))
    rows.append(result("NUL-04", "missing values", "Notif History", "Every blank Order is on an In Progress row", 0,
                       int((notif["order_no"].isna() & ~open_rows).sum())))
    rows.append(result("NUL-05", "missing values", "FuncLoc list", "Criticality is blank exactly on SITE rows", 0,
                       int((funcloc["criticality"].isna() != funcloc["functional_location"].str.startswith("SITE")).sum())))
    return rows


def check_duplicate_handling(tables: dict[str, pd.DataFrame], labelled: dict[str, pd.DataFrame],
                             groups: dict[str, pd.DataFrame], views: dict[str, pd.DataFrame]) -> list[dict]:
    rows = []
    for key, table in labelled.items():
        name = DATASETS[key].name
        rows.append(result(f"DUP-01.{key}", "duplicates", name, "Labelling keeps every source row", len(tables[key]), len(table)))
        rows.append(result(f"DUP-02.{key}", "duplicates", name, "Occurrence counts add back to total rows", len(tables[key]),
                           int(table[table["occurrence_rank"] == 1]["occurrence_count"].sum())))
        direct = int(tables[key].duplicated(DATASETS[key].standard_columns).sum())
        rows.append(result(f"DUP-03.{key}", "duplicates", name, "Hash-based extras equal a direct all-column comparison", direct,
                           int((table["occurrence_rank"] > 1).sum())))
        if key in groups and len(groups[key]):
            rows.append(result(f"DUP-04.{key}", "duplicates", name, "All metadata groups are truly identical in every source column", True,
                               bool(groups[key]["all_source_columns_identical"].all())))
            listed = sorted(int(r) for rows_text in groups[key]["source_rows"] for r in rows_text.split(";"))
            copied = table[table["occurrence_count"] > 1]["source_row"].astype("int64").sort_values().tolist()
            rows.append(result(f"DUP-05.{key}", "duplicates", name, "Metadata lists each duplicated source row exactly once", len(copied), len(listed)))
            rows[-1]["status"] = PASS if listed == copied else FAIL

    original, distinct = views[ORIGINAL], views[DISTINCT]
    prpo_rows = tables["prpo"]["source_row"].astype("int64").tolist()
    rows.append(result("VIEW-01", "PR PO views", "PR PO", "Original-row view has all 11,609 source rows", 11609, len(original)))
    same = sorted(original["source_row"].astype("int64").tolist()) == sorted(prpo_rows)
    rows.append(result("VIEW-02", "PR PO views", "PR PO", "Original-row view has the same source rows as staged PR PO", True, same))
    rows.append(result("VIEW-03", "PR PO views", "PR PO", "Distinct view has one row per content group", int(original["content_group_id"].nunique()), len(distinct)))
    listed = sorted(int(r) for text in distinct["all_source_rows"] for r in text.split(";"))
    rows.append(result("VIEW-04", "PR PO views", "PR PO", "Distinct view references every source row exactly once", True, listed == sorted(prpo_rows)))
    columns = DATASETS["prpo"].standard_columns
    rows.append(result("VIEW-05", "PR PO views", "PR PO", "Original-row source values equal staged PR PO", True,
                       bool(original[columns].astype("string").reset_index(drop=True).equals(tables["prpo"][columns].astype("string").reset_index(drop=True)))))
    for currency, part in original.groupby("currency", observed=True):
        total = round(float(part["po_item_amount"].sum()), 2)
        rebuilt = distinct[distinct["currency"] == currency]
        rows.append(result(f"VIEW-06.{currency}", "PR PO views", "PR PO", f"Distinct amount x occurrences rebuilds the original-row total ({currency})", total,
                           round(float((rebuilt["po_item_amount"] * rebuilt["occurrence_count"]).sum()), 2)))
    labels = {"original": original["analysis_view"].unique().tolist(), "distinct": distinct["analysis_view"].unique().tolist()}
    rows.append(result("VIEW-07", "PR PO views", "PR PO", "Every row states its analysis view", {"original": [ORIGINAL], "distinct": [DISTINCT]}, labels))
    return rows


def check_staged_round_trip(tables: dict[str, pd.DataFrame], staged_dir: Path) -> list[dict]:
    rows = []
    for key, spec in DATASETS.items():
        reloaded = read_staged(spec, Path(staged_dir) / f"stg_{key}.csv")
        same = True
        for column in spec.standard_columns:
            left, right = tables[key][column], reloaded[column]
            if pd.api.types.is_datetime64_any_dtype(left):
                same &= bool(left.equals(right))
            else:
                same &= bool(left.astype("string").equals(right.astype("string"))) if left.dtype.name in ("string", "category") else bool(left.equals(right))
        rows.append(result(f"CSV-01.{key}", "round trip", spec.name, "Staged CSV reloads to identical values and identifiers", True, same))
        rows.append(result(f"CSV-02.{key}", "round trip", spec.name, "Row hashes survive the round trip", True,
                           bool(tables[key]["row_hash"].equals(reloaded["row_hash"]))))
    return rows


def check_expected_values(measures: dict, expected_file: Path = EXPECTED_VALUES_FILE) -> list[dict]:
    """Compare measures with documented values. Passing shows no drift, not correct meaning."""
    expected = json.loads(Path(expected_file).read_text(encoding="utf-8"))["measures"]
    rows = []
    for name, entry in expected.items():
        if name not in measures:
            rows.append(result(f"EXP.{name}", "expected values", name.split(".")[0], "Measure exists", "present", "absent", source=entry["source"]))
            continue
        rows.append(result(f"EXP.{name}", "expected values", name.split(".")[0], f"Measure {name} equals its documented value",
                           entry["expected"], measures[name], entry["severity"], entry["source"]))
    return rows
