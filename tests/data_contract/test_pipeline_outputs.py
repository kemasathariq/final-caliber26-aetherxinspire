"""The complete pipeline: outputs exist, rerun is reproducible, sources are untouched."""
import json
import os
import shutil
import subprocess
import sys

import pandas as pd
import pytest

from src import pipeline
from src.config import PROJECT_ROOT, get_paths
from src.validation.source_checks import sha256_file

pytestmark = pytest.mark.data_contract

TABLES = ["workbook_inventory", "column_profile", "numeric_summary", "categorical_distribution", "date_summary",
          "date_monthly_counts", "candidate_primary_keys", "candidate_foreign_keys", "duplicate_summary",
          "prpo_view_comparison", "data_quality_findings", "validation_results", "transformation_log", "join_audit", "outlier_summary",
          "prpo_copy_permutation_tests", "prpo_copy_numeric_associations", "prpo_copy_categorical_associations", "movement_duplicate_sensitivity",
          "exception_summary", "repeated_maximum_values", "relationship_audit", "mart_join_audit", "procurement_currency_summary",
          "demand_scenario_unit_summary", "demand_impact_sensitivity", "procurement_issue_reconciliation", "sim_population_funnel", "sim_single_reason_candidates", "sim_evidence_tiers",
          "sim_resampling_threshold_sensitivity", "sim_pre_analysis", "sim_demand_coverage", "sim_monthly_demand_shape", "sim_parameter_plausibility", "sim_lead_proxy_associations", "sim_demand_timing"]
REPORTS = ["profile_prpo", "profile_movement", "profile_notif", "profile_mitem", "profile_bom", "profile_funcloc",
           "profiling_summary", "validation_report", "duplicate_evidence", "conformed_summary", "relationship_audit", "mart_summary", "simulation_feasibility_evidence"]


def test_no_critical_check_failed(real_build):
    results = real_build["results"]
    failed = results[results["status"] == "FAIL"]
    assert failed.empty, failed[["check_id", "expected", "observed"]].to_string()


def test_validation_covers_every_required_group(real_build):
    assert {"accessibility", "checksum", "worksheets", "columns", "data types", "identifier integrity", "missing values",
            "duplicates", "row preservation", "lineage", "round trip", "PR PO views", "expected values", "conformed tables", "relationships", "marts", "simulation design"} <= set(real_build["results"]["group"])


@pytest.mark.parametrize("name", TABLES)
def test_table_output_exists_and_has_rows(real_build, name):
    assert len(pd.read_csv(real_build["paths"].tables / f"{name}.csv")) > 0


@pytest.mark.parametrize("name", REPORTS)
def test_report_exists_with_the_data_label(real_build, name):
    assert "documented as synthetic" in (real_build["paths"].reports / f"{name}.md").read_text()


def test_machine_readable_summaries_parse(real_build):
    summary = json.loads((real_build["paths"].reports / "profiling_summary.json").read_text())
    assert summary["datasets"]["PR PO"]["rows"] == 11609
    assert summary["prpo_views"] == {"original_rows": 11609, "exact_distinct_rows": 6189}
    assert json.loads((real_build["paths"].tables / "quality_measures.json").read_text())["rows.bom"] == 20653


def test_supplier_and_material_frequency_lists_are_not_published(real_build):
    """Rankings are out of scope for this phase."""
    columns = set(pd.read_csv(real_build["paths"].tables / "categorical_distribution.csv")["column"])
    assert not columns & {"supplier_name", "supplier_code", "material_no", "material_desc"}


def _run_in_new_process(root, hash_seed):
    env = dict(os.environ, PYTHONHASHSEED=str(hash_seed), PYTHONDONTWRITEBYTECODE="1")
    return subprocess.run([sys.executable, "-m", "src.pipeline", "--build-root", str(root)], cwd=PROJECT_ROOT,
                          env=env, capture_output=True, text=True, timeout=300)


@pytest.mark.slow
def test_rebuilds_in_new_processes_produce_identical_files(tmp_path, real_build):
    first, second = tmp_path / "one", tmp_path / "two"
    for root, seed in ((first, 1), (second, 2)):
        done = _run_in_new_process(root, seed)
        assert done.returncode == 0, done.stdout + done.stderr
    a = json.loads((first / "outputs/reports/output_checksums.json").read_text())
    b = json.loads((second / "outputs/reports/output_checksums.json").read_text())
    assert a == b
    assert len(a) >= 30
    # Actual bytes, in case the hash map itself were wrong.
    for relative in a:
        assert (first / relative).read_bytes() == (second / relative).read_bytes(), relative
    # The in-process session build matches too.
    assert a == json.loads((real_build["root"] / "outputs/reports/output_checksums.json").read_text())


def test_generated_data_has_no_absolute_paths(real_build):
    home = os.path.expanduser("~")
    manifest = real_build["paths"].manifest.read_text()
    assert home not in manifest and "Mobile Documents" not in manifest
    assert home not in (real_build["paths"].reports / "validation_report.md").read_text()


def test_source_workbooks_are_unchanged_after_all_runs(real_build, raw_checksums_before):
    raw = get_paths().raw
    assert {p.name: sha256_file(p) for p in sorted(raw.glob("*.xlsx"))} == raw_checksums_before


def test_pipeline_reports_and_exits_nonzero_when_a_source_changes(tmp_path, monkeypatch):
    """End to end: a changed workbook copy must fail visibly, with reports still written."""
    raw = tmp_path / "raw"
    raw.mkdir()
    for workbook in get_paths().raw.glob("*.xlsx"):
        shutil.copy(workbook, raw / workbook.name)
    with open(raw / "BoM.xlsx", "ab") as handle:
        handle.write(b"\0")
    paths = get_paths(build_root=tmp_path / "build", raw_dir=raw)
    monkeypatch.setattr(pipeline, "get_paths", lambda build_root=None: paths)
    monkeypatch.setattr(sys, "argv", ["pipeline"])
    assert pipeline.main() == 1
    results = pd.read_csv(paths.tables / "validation_results.csv")
    assert results.loc[results["check_id"] == "SRC-02.bom", "status"].item() == "FAIL"
    assert "SRC-02.bom" in (paths.reports / "validation_report.md").read_text()
    manifest = json.loads(paths.manifest.read_text())
    status = {e["file_name"]: e["verification_status"] for e in manifest["files"]}
    assert status["BoM.xlsx"] == "checksum_mismatch"
    assert status["PR PO.xlsx"] == "consistent_with_audit_baseline"
