"""Shared fixtures. Tests never write to the project's data or output folders."""
from pathlib import Path

import openpyxl
import pytest

from src.config import get_paths
from src.data.schemas import ColumnSpec, DatasetSpec
from src.pipeline import run_pipeline
from src.validation.source_checks import sha256_file

SAMPLE_SPEC = DatasetSpec("sample", "Sample", "sample.xlsx", "Data", (
    ColumnSpec("Doc No", "doc_no", "identifier", r"\d{10}"),
    ColumnSpec("Note", "note", "text"),
    ColumnSpec("Code", "code", "category"),
    ColumnSpec("Qty", "qty", "integer"),
    ColumnSpec("Amount", "amount", "float"),
    ColumnSpec("Doc Date", "doc_date", "date"),
), "One sample row")


@pytest.fixture
def sample_spec():
    return SAMPLE_SPEC


@pytest.fixture
def make_workbook(tmp_path):
    """Create a small .xlsx file with the given rows."""
    def _make(rows, headers=None, sheet="Data", name="sample.xlsx"):
        book = openpyxl.Workbook()
        worksheet = book.active
        worksheet.title = sheet
        worksheet.append(headers or SAMPLE_SPEC.source_columns)
        for row in rows:
            worksheet.append(row)
        path = Path(tmp_path) / name
        book.save(path)
        return path
    return _make


@pytest.fixture(scope="session")
def raw_checksums_before():
    """Hash the real workbooks before any test builds run."""
    raw = get_paths().raw
    return {p.name: sha256_file(p) for p in sorted(raw.glob("*.xlsx"))}


@pytest.fixture(scope="session")
def real_build(tmp_path_factory, raw_checksums_before):
    """One complete pipeline run on the real workbooks, into a temporary folder."""
    root = tmp_path_factory.mktemp("build")
    paths = get_paths(build_root=root)
    results = run_pipeline(paths)
    return {"root": root, "paths": paths, "results": results}


@pytest.fixture(scope="session")
def real_state(real_build):
    """Real staged tables, duplicate labels, views and inspections, kept in memory."""
    from src.data.ingest import read_staged
    from src.data.schemas import DATASETS
    from src.data.workbook_inspect import inspect_workbook
    from src.pipeline import run_ingest
    paths = real_build["paths"]
    state = run_ingest(paths)
    state["inspections"] = {k: inspect_workbook(paths.raw / s.file_name) for k, s in DATASETS.items()}
    state["reloaded"] = {k: read_staged(s, paths.staged / f"stg_{k}.csv") for k, s in DATASETS.items()}
    return state


@pytest.fixture(scope="session")
def real_conformed(real_state):
    """Conformed tables built from the real workbooks, kept in memory."""
    from src.preprocessing.conform import build_conformed
    return build_conformed(real_state["tables"], real_state["labelled"])


@pytest.fixture(scope="session")
def real_marts(real_conformed):
    """Marts M1 to M3 built from the real conformed tables, kept in memory."""
    from src.marts.build import build_marts
    return build_marts(real_conformed["tables"])
