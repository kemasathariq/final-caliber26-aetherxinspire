"""Real workbooks: accessibility, location, checksums, worksheets, columns, manifest."""
import json

import pandas as pd
import pytest

from src.config import BOM_RELOCATION_FILE, PROJECT_ROOT
from src.data.schemas import DATASETS
from src.validation.source_checks import load_audit_baseline, sha256_file

pytestmark = pytest.mark.data_contract

SPECS = list(DATASETS.values())
IDS = [s.key for s in SPECS]


def test_exactly_six_workbooks_are_in_data_raw(raw_checksums_before):
    assert sorted(raw_checksums_before) == sorted(s.file_name for s in SPECS)


def test_bom_is_no_longer_in_the_project_root():
    assert not (PROJECT_ROOT / "BoM.xlsx").exists()


def test_bom_relocation_record_shows_matching_checksums():
    record = json.loads(BOM_RELOCATION_FILE.read_text())
    baseline = load_audit_baseline()["BoM.xlsx"]
    assert record["original_relative_path"] == "BoM.xlsx"
    assert record["new_relative_path"] == "data/raw/BoM.xlsx"
    assert record["sha256_before_move"] == record["sha256_after_move"] == baseline
    assert sha256_file(PROJECT_ROOT / record["new_relative_path"]) == baseline


@pytest.mark.parametrize("spec", SPECS, ids=IDS)
def test_checksum_matches_audit_baseline(spec, raw_checksums_before):
    assert raw_checksums_before[spec.file_name] == load_audit_baseline()[spec.file_name]


@pytest.mark.parametrize("spec", SPECS, ids=IDS)
def test_worksheet_and_columns_via_openpyxl(spec, real_build):
    with pd.ExcelFile(real_build["paths"].raw / spec.file_name, engine="openpyxl") as book:
        assert book.sheet_names == [spec.sheet]
        assert list(book.parse(spec.sheet, nrows=0).columns) == spec.source_columns


def test_manifest_has_every_required_field(real_build):
    manifest = json.loads(real_build["paths"].manifest.read_text())
    assert "not authenticity against organiser-issued checksums" in manifest["note"]
    assert len(manifest["files"]) == 6
    required = {"dataset", "file_name", "relative_path", "sha256", "file_size_bytes", "worksheets",
                "data_rows", "columns", "verification_status"}
    for entry in manifest["files"]:
        assert required <= set(entry)
        assert entry["verification_status"] == "consistent_with_audit_baseline"
        assert entry["relative_path"] == f"data/raw/{entry['file_name']}"
        assert entry["worksheets"] == ["Data"]
        assert not entry["relative_path"].startswith("/")
