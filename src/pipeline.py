"""Command-line runner, through marts M1 to M3 and the simulation feasibility evidence. It runs no simulation.

    python -m src.pipeline                  run everything
    python -m src.pipeline --stage sources  checksums and source manifest only
    python -m src.pipeline --stage ingest   also write staged tables and PR PO views
    python -m src.pipeline --stage conform  also write conformed tables
    python -m src.pipeline --stage marts    also write marts M1 to M3

Exit code 1 means a critical check failed. Reports are still written.
"""
import argparse
import json
import logging
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy
import openpyxl
import pandas as pd
import scipy

from src import reporting
from src.config import (EXPECTED_SIM_DESIGN_FILE, BASELINE_NOTE, COPY_NEAR_GAP_ROWS, DATA_CUTOFF, DATA_LABEL, DEMAND_IMPACT_HIGH_PCT, DEMAND_IMPACT_MATERIAL_PCT, DEMAND_WINDOW_END, DEMAND_WINDOW_START,
                        EXPECTED_CONFORMED_FILE, EXPECTED_MARTS_FILE, EXTREME_INTERVAL_PERCENTILE, LOW_LINE_COUNT, OUTLIER_PARAMETERS, PERMUTATION_ROUNDS, PERMUTATION_SEED,
                        RARE_CATEGORY_DISTINCT_ROWS, REPEATED_MAXIMUM_MIN_MATERIALS, SPARSE_HISTORY_MONTHS, SPEC_VERSION, Paths, get_paths)
from src.data import profiling
from src.data.ingest import ingest_all, write_csv
from src.data.schemas import DATASETS, DUPLICATE_SETTINGS
from src.data.workbook_inspect import inspect_workbook
from src.marts.build import GRAINS as MART_GRAINS
from src.marts.build import PRIMARY_KEYS, build_marts
from src.marts.dictionary import describe
from src.marts.movement_copies import COPY_RULES, SCENARIOS
from src.preprocessing.conform import GRAINS, build_conformed, type_map
from src.preprocessing.prpo_views import DISTINCT, ORIGINAL, VIEW_DEFINITIONS, build_prpo_views, compare_views
from src.simulation_design import feasibility
from src.validation import checks, conformed_checks, mart_checks, simulation_design_checks
from src.validation.duplicate_evidence import movement_sensitivity, prpo_duplicate_evidence, shared_order_review
from src.validation.duplicates import add_duplicate_columns, duplicate_group_metadata, duplicate_summary
from src.validation.exceptions import build_exception_lists, repeated_maximum_values
from src.validation.quality_measures import build_findings, compute_measures
from src.validation.relationships import conformed_measures, relationship_audit
from src.validation.source_checks import build_source_manifest, sha256_file

log = logging.getLogger("pipeline")

# Generated files whose content legitimately differs between runs.
_RUN_SPECIFIC_FILES = {"run_metadata.json", "pipeline.log", "output_checksums.json"}


def _configure_logging(log_file: Path) -> None:
    log_file.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(level=logging.INFO, force=True, format="%(asctime)s %(levelname)s %(name)s: %(message)s",
                        handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler(log_file, mode="w", encoding="utf-8")])


def run_sources(paths: Paths) -> tuple[dict, dict]:
    """Inspect each workbook read-only and write the source manifest."""
    inspections = {}
    for key, spec in DATASETS.items():
        path = paths.raw / spec.file_name
        if not path.is_file():
            raise FileNotFoundError(f"Source workbook missing: {path}")
        inspections[key] = inspect_workbook(path)
    manifest = build_source_manifest(paths.raw, inspections)
    reporting.write_json(manifest, paths.manifest)
    for entry in manifest["files"]:
        log.info("%s: %s, %s data rows", entry["file_name"], entry["verification_status"], entry["data_rows"])
    return inspections, manifest


def run_ingest(paths: Paths) -> dict:
    """Read all workbooks, then write staged tables, duplicate metadata and PR PO views."""
    tables = ingest_all(paths.raw)
    for key, table in tables.items():
        write_csv(table, paths.staged / f"stg_{key}.csv")

    labelled, groups, summaries = {}, {}, []
    for key, spec in DATASETS.items():
        settings = DUPLICATE_SETTINGS[key]
        labelled[key] = add_duplicate_columns(tables[key], settings["id_prefix"])
        summaries.append(duplicate_summary(labelled[key], key))
        groups[key] = duplicate_group_metadata(labelled[key], spec.standard_columns, settings["key_sets"],
                                               settings["measures"], settings["context"])
        if len(groups[key]):
            write_csv(groups[key], paths.duplicates / f"{key}_duplicate_groups.csv")

    original, distinct = build_prpo_views(labelled["prpo"])
    views = {ORIGINAL: original, DISTINCT: distinct}
    write_csv(original, paths.prpo_views / "prpo_original_rows.csv")
    write_csv(distinct, paths.prpo_views / "prpo_exact_distinct_rows.csv")
    reporting.write_json({
        "status": "Approved Decision 4. Neither view is the definitive business truth. "
                  "The distinct view is a sensitivity scenario.",
        "views": VIEW_DEFINITIONS,
        "row_counts": {ORIGINAL: len(original), DISTINCT: len(distinct)},
        "duplicate_groups_file": "data/interim/duplicates/prpo_duplicate_groups.csv",
        "data_label": DATA_LABEL,
    }, paths.prpo_views / "prpo_views_metadata.json")
    log.info("PR PO views: %d original rows, %d exact distinct rows, %d duplicate groups",
             len(original), len(distinct), len(groups["prpo"]))
    return {"tables": tables, "labelled": labelled, "groups": groups, "views": views,
            "duplicate_summary": pd.DataFrame(summaries)}


def run_profiling(paths: Paths, state: dict, inspections: dict) -> dict:
    """Generate all profiling tables, and return them for the reports."""
    tables = state["tables"]
    view_sets = {key: {profiling.ALL_ROWS: table} for key, table in tables.items()}
    view_sets["prpo"] = state["views"]

    numeric = profiling.numeric_summary(view_sets)
    categories = profiling.categorical_distribution(view_sets)
    dates, monthly = profiling.date_summary(view_sets)
    columns = pd.concat([profiling.column_profile(tables[k], s, inspections[k]["sheets"][s.sheet]) for k, s in DATASETS.items()], ignore_index=True)
    primary_keys = pd.concat([profiling.candidate_primary_keys(tables[k], s, documented_keys=DUPLICATE_SETTINGS[k]["key_sets"]) for k, s in DATASETS.items()], ignore_index=True)
    foreign_keys = profiling.candidate_foreign_keys(tables)
    comparison = compare_views(state["views"][ORIGINAL], state["views"][DISTINCT])

    measures = compute_measures(tables, state["views"])
    findings = build_findings(measures)

    outputs = {
        "workbook_inventory": profiling.workbook_inventory(inspections), "column_profile": columns,
        "numeric_summary": numeric, "categorical_distribution": categories, "date_summary": dates,
        "date_monthly_counts": monthly, "candidate_primary_keys": primary_keys,
        "candidate_foreign_keys": foreign_keys, "duplicate_summary": state["duplicate_summary"],
        "prpo_view_comparison": comparison, "data_quality_findings": findings,
    }
    for name, frame in outputs.items():
        write_csv(frame, paths.tables / f"{name}.csv")
    reporting.write_json(measures, paths.tables / "quality_measures.json")

    profile = {"tables": tables, "columns": columns, "numeric": numeric, "categories": categories, "dates": dates,
               "primary_keys": primary_keys, "foreign_keys": foreign_keys, "duplicates": state["duplicate_summary"],
               "view_comparison": comparison, "findings": findings}
    for key in DATASETS:
        reporting.write_dataset_profile(key, profile, paths.reports / f"profile_{key}.md")
    reporting.write_profiling_summary(outputs, paths.reports / "profiling_summary.md")
    reporting.write_json({
        "data_label": DATA_LABEL,
        "datasets": {spec.name: {
            "file_name": spec.file_name, "worksheet": spec.sheet, "rows": len(tables[key]), "columns": len(spec.columns),
            "exact_duplicate_extras": measures[f"exact_duplicate_extras.{key}"],
            "columns_with_missing_values": {c: int(tables[key][c].isna().sum()) for c in spec.standard_columns if tables[key][c].isna().any()},
            "business_keys_unique_on_all_rows": primary_keys[(primary_keys["dataset"] == spec.name) & (primary_keys["assessment"] == "unique_on_all_rows")]["columns"].tolist(),
            "business_keys_unique_only_after_setting_aside_exact_copies": primary_keys[(primary_keys["dataset"] == spec.name) & (primary_keys["assessment"] == "unique_only_after_setting_aside_exact_copies")]["columns"].tolist(),
        } for key, spec in DATASETS.items()},
        "prpo_views": {ORIGINAL: len(state["views"][ORIGINAL]), DISTINCT: len(state["views"][DISTINCT])},
    }, paths.reports / "profiling_summary.json")
    return {"measures": measures}


def run_conform(paths: Paths, state: dict) -> dict:
    """Build and write the conformed tables with their metadata, log and audit tables."""
    built = build_conformed(state["tables"], state["labelled"])
    for name, frame in built["tables"].items():
        write_csv(frame, paths.conformed / f"{name}.csv")
    metadata = {
        "spec_version": SPEC_VERSION, "data_label": DATA_LABEL,
        "parameters": {"data_cutoff_assumption": DATA_CUTOFF, "outliers": OUTLIER_PARAMETERS, "extreme_interval_percentile": EXTREME_INTERVAL_PERCENTILE,
                       "rare_category_distinct_rows": RARE_CATEGORY_DISTINCT_ROWS},
        "policies": {"prpo": "Dual views. Select with in_exact_distinct_rows. Neither is definitive (COR-09).", "movement": "No policy applied. All rows kept and labelled (A-05).",
                     "bom": "Pair table holds distinct pairs, with occurrence_count and all_source_rows."},
        "load_with": "src.preprocessing.conform.read_conformed, using the column types below",
        "tables": {name: {"grain": GRAINS[name], "rows": len(frame), "columns": type_map(frame)} for name, frame in built["tables"].items()},
    }
    reporting.write_json(metadata, paths.conformed / "conformed_metadata.json")
    write_csv(built["transformation_log"], paths.tables / "transformation_log.csv")
    write_csv(built["join_audit"], paths.tables / "join_audit.csv")
    write_csv(built["outlier_summary"], paths.tables / "outlier_summary.csv")
    write_csv(built["outliers"], paths.exceptions / "outliers.csv")
    built["metadata"] = metadata
    log.info("Conformed tables: %s", json.dumps({name: len(frame) for name, frame in built["tables"].items()}))
    return built


def run_marts(paths: Paths, built: dict, manifest: dict) -> dict:
    """Build and write M1, M2 and M3 with their metadata."""
    marts = build_marts(built["tables"])
    for name, frame in marts["tables"].items():
        write_csv(frame, paths.processed / f"{name}.csv")
    metadata = {
        "spec_version": SPEC_VERSION, "data_label": DATA_LABEL, "checksum_scope": BASELINE_NOTE,
        "source_checksums": {entry["file_name"]: entry["sha256"] for entry in manifest["files"]},
        "parameters": {"data_cutoff_assumption": DATA_CUTOFF, "demand_window": [DEMAND_WINDOW_START, DEMAND_WINDOW_END], "copy_near_gap_rows": COPY_NEAR_GAP_ROWS,
                       "impact_material_pct": DEMAND_IMPACT_MATERIAL_PCT, "impact_high_pct": DEMAND_IMPACT_HIGH_PCT, "low_line_count": LOW_LINE_COUNT, "sparse_history_months": SPARSE_HISTORY_MONTHS,
                       "repeated_maximum_min_materials": REPEATED_MAXIMUM_MIN_MATERIALS, "outliers": OUTLIER_PARAMETERS},
        "policies": {"prpo_views": VIEW_DEFINITIONS, "demand_scenarios": SCENARIOS, "copy_rules": COPY_RULES, "no_default": "No view or scenario is the default, and none is the true value."},
        "load_with": "src.preprocessing.conform.read_conformed, using the column types below",
        "tables": {name: {"grain": MART_GRAINS[name], "primary_key": PRIMARY_KEYS[name], "rows": len(frame),
                          "columns": type_map(frame), "descriptions": {c: describe(c) for c in frame.columns}} for name, frame in marts["tables"].items()},
    }
    reporting.write_json(metadata, paths.processed / "mart_metadata.json")
    write_csv(marts["join_audit"], paths.tables / "mart_join_audit.csv")
    write_csv(marts["currency_summary"], paths.tables / "procurement_currency_summary.csv")
    write_csv(marts["unit_scenario_summary"], paths.tables / "demand_scenario_unit_summary.csv")
    write_csv(marts["impact_sensitivity"], paths.tables / "demand_impact_sensitivity.csv")
    write_csv(marts["procurement_issue_reconciliation"], paths.tables / "procurement_issue_reconciliation.csv")
    comparison = marts["tables"]["mart_material_demand_comparison"]
    affected = comparison[comparison["is_materially_affected"]].sort_values(["qty_diff_pct_of_a", "material_no"], ascending=[False, True])
    write_csv(affected, paths.exceptions / "demand_materially_affected.csv")
    measures = mart_checks.mart_measures(marts["tables"])
    reporting.write_json(measures, paths.tables / "mart_measures.json")
    reporting.write_mart_summary(metadata, marts, measures, paths.reports / "mart_summary.md")
    marts["measures"] = measures
    log.info("Marts: %s", json.dumps({name: len(frame) for name, frame in marts["tables"].items()}))
    return marts


def run_simulation_feasibility(paths: Paths, marts: dict) -> dict:
    """Feasibility evidence for the simulation design. No events run and no results are simulated."""
    tables = marts["tables"]
    audit: list[dict] = []
    population = feasibility.build_simulation_population(tables["mart_material_inventory"], tables["mart_material_demand_summary__scenario_b"], tables["mart_supplier_material__exact_distinct_rows"], audit)
    write_csv(population, paths.processed / "simulation_population.csv")
    summary = feasibility.pre_analysis_summary(population)
    outputs = {"sim_population_funnel": feasibility.population_funnel(population), "sim_single_reason_candidates": feasibility.single_reason_candidates(population), "sim_evidence_tiers": feasibility.evidence_tiers(population),
               "sim_resampling_threshold_sensitivity": feasibility.threshold_sensitivity(population), "sim_pre_analysis": summary, "sim_demand_coverage": feasibility.demand_coverage(tables["movement_copy_classification"], population),
               "sim_monthly_demand_shape": feasibility.monthly_demand_shape(tables["movement_copy_classification"], population),
               "sim_parameter_plausibility": feasibility.parameter_plausibility(tables["mart_material_inventory"], population, tables["mart_supplier_material__exact_distinct_rows"]),
               "sim_lead_proxy_associations": feasibility.lead_proxy_associations(tables["mart_procurement_line__exact_distinct_rows"], population),
               "sim_demand_timing": feasibility.demand_timing(tables["movement_copy_classification"], population)}
    for name, frame in outputs.items():
        write_csv(frame, paths.tables / f"{name}.csv")
    reporting.write_json({"status": "Feasibility evidence only. No simulation has been run. Nothing here is a simulated result, a historical stockout or a cost.", "data_label": DATA_LABEL, "spec_version": SPEC_VERSION,
                          "columns": type_map(population), "descriptions": feasibility.DESCRIPTIONS, "load_with": "src.preprocessing.conform.read_conformed, using the column types above"}, paths.processed / "simulation_population_metadata.json")
    reporting.write_simulation_feasibility_summary(outputs, paths.reports / "simulation_feasibility_evidence.md")
    return {"population": population, "summary": summary, "join_audit": pd.DataFrame(audit), "measures": simulation_design_checks.simulation_design_measures(population, summary)}


def run_quality_evidence(paths: Paths, state: dict, built: dict) -> dict:
    """Duplicate evidence, exception lists and the relationship audit."""
    conformed = built["tables"]
    evidence = prpo_duplicate_evidence(state["views"], state["tables"]["movement"], state["tables"]["bom"])
    sensitivity = movement_sensitivity(state["labelled"]["movement"])
    shared = shared_order_review(conformed["bridge_order_notification"], conformed["fact_issue"], conformed["bridge_fl_material"])
    write_csv(evidence["permutations"], paths.tables / "prpo_copy_permutation_tests.csv")
    write_csv(evidence["numeric"], paths.tables / "prpo_copy_numeric_associations.csv")
    write_csv(evidence["categorical"], paths.tables / "prpo_copy_categorical_associations.csv")
    reporting.write_json(evidence["keys"], paths.tables / "prpo_key_structure.json")
    write_csv(sensitivity, paths.tables / "movement_duplicate_sensitivity.csv")
    write_csv(shared, paths.exceptions / "shared_orders.csv")
    reporting.write_duplicate_evidence_report(evidence, sensitivity, shared, state["duplicate_summary"], paths.reports / "duplicate_evidence.md")

    lists, summary = build_exception_lists(conformed)
    for name, frame in lists.items():
        write_csv(frame, paths.exceptions / f"{name}.csv")
    write_csv(summary, paths.tables / "exception_summary.csv")
    repeated = repeated_maximum_values(conformed)
    write_csv(repeated, paths.tables / "repeated_maximum_values.csv")
    audit = relationship_audit(conformed, state["tables"])
    write_csv(audit, paths.tables / "relationship_audit.csv")
    reporting.write_relationship_report(audit, paths.reports / "relationship_audit.md")
    reporting.write_conformed_report(built["metadata"], built["transformation_log"], built["join_audit"], built["outlier_summary"], summary, repeated, paths.reports / "conformed_summary.md")
    measures = conformed_measures(conformed, audit, evidence, state["tables"]["movement"])
    reporting.write_json(measures, paths.tables / "conformed_measures.json")
    return {"evidence": evidence, "measures": measures, "audit": audit}


def run_validation(paths: Paths, state: dict, inspections: dict, measures: dict, built: dict, evidence_measures: dict, marts: dict, feasible: dict) -> pd.DataFrame:
    tables = state["tables"]
    conformed = built["tables"]
    rows = (checks.check_sources(paths.raw, inspections)
            + checks.check_storage_and_types(tables, inspections)
            + checks.check_rows_and_cells(tables, inspections)
            + checks.check_identifiers(tables)
            + checks.check_missing_values(tables)
            + checks.check_duplicate_handling(tables, state["labelled"], state["groups"], state["views"])
            + checks.check_staged_round_trip(tables, paths.staged)
            + checks.check_expected_values(measures)
            + conformed_checks.check_facts_preserve_sources(conformed, tables)
            + conformed_checks.check_keys_and_coarser_tables(conformed, tables)
            + conformed_checks.check_views_and_flags(conformed, state["views"], measures)
            + conformed_checks.check_no_unapproved_rules(conformed)
            + conformed_checks.check_cycle_map(conformed)
            + conformed_checks.check_join_audit(built["join_audit"])
            + conformed_checks.check_conformed_round_trip(conformed, paths.conformed)
            + checks.check_expected_values(evidence_measures, EXPECTED_CONFORMED_FILE)
            + mart_checks.check_grain_and_dictionary(marts["tables"])
            + mart_checks.check_classification(marts["tables"], conformed)
            + mart_checks.check_demand(marts["tables"], conformed)
            + mart_checks.check_procurement(marts["tables"], conformed)
            + mart_checks.check_inventory(marts["tables"], conformed)
            + mart_checks.check_mart_joins(marts["join_audit"], marts["tables"])
            + mart_checks.check_mart_round_trip(marts["tables"], paths.processed)
            + checks.check_expected_values(marts["measures"], EXPECTED_MARTS_FILE)
            + simulation_design_checks.check_population(feasible["population"], marts["tables"]["mart_material_inventory"])
            + simulation_design_checks.check_arithmetic(feasible["population"], marts["tables"]["mart_material_inventory"])
            + mart_checks.check_mart_joins(feasible["join_audit"].assign(unmatched_rows=0), marts["tables"])
            + checks.check_expected_values(feasible["measures"], EXPECTED_SIM_DESIGN_FILE))
    results = pd.DataFrame(rows)
    write_csv(results, paths.tables / "validation_results.csv")
    reporting.write_validation_report(results, paths.reports / "validation_report.md")
    return results


def _generated_files(build_root: Path, paths: Paths) -> list[Path]:
    folders = (paths.staged, paths.prpo_views, paths.duplicates, paths.conformed, paths.processed, paths.exceptions, paths.tables, paths.reports)
    files = [paths.manifest] + [f for folder in folders for f in sorted(folder.glob("*")) if f.is_file()]
    return [f for f in files if f.name not in _RUN_SPECIFIC_FILES and f.name != ".DS_Store"]


def write_output_checksums(paths: Paths) -> dict[str, str]:
    """Hash deterministic outputs. Two clean builds must produce equal maps."""
    root = paths.reports.parents[1]
    hashes = {f.relative_to(root).as_posix(): sha256_file(f) for f in _generated_files(root, paths)}
    reporting.write_json(hashes, paths.reports / "output_checksums.json")
    return hashes


def run_pipeline(paths: Paths, stage: str = "all") -> pd.DataFrame | None:
    """Run the requested stage and everything before it."""
    paths.create_output_dirs()
    started = datetime.now(timezone.utc)
    log.info("Stage 1: source inspection and manifest")
    inspections, manifest = run_sources(paths)
    if stage == "sources":
        return None
    log.info("Stage 2: ingestion, staged tables, duplicate metadata and PR PO views")
    state = run_ingest(paths)
    if stage == "ingest":
        return None
    log.info("Stage 3: conformed tables")
    built = run_conform(paths, state)
    if stage == "conform":
        return None
    log.info("Stage 4: marts M1 to M3")
    marts = run_marts(paths, built, manifest)
    if stage == "marts":
        return None
    log.info("Stage 5: simulation feasibility evidence. No simulation is run")
    feasible = run_simulation_feasibility(paths, marts)
    log.info("Stage 6: profiling")
    measures = run_profiling(paths, state, inspections)["measures"]
    log.info("Stage 7: duplicate evidence, exception lists and relationship audit")
    quality = run_quality_evidence(paths, state, built)
    log.info("Stage 8: validation")
    results = run_validation(paths, state, inspections, measures, built, quality["measures"], marts, feasible)
    write_output_checksums(paths)

    counts = results["status"].value_counts().to_dict()
    packages = {"pandas": pd.__version__, "numpy": numpy.__version__, "openpyxl": openpyxl.__version__, "scipy": scipy.__version__}
    reporting.write_json({
        "started_utc": started.isoformat(timespec="seconds"),
        "finished_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "python": platform.python_version(), "packages": packages, "spec_version": SPEC_VERSION,
        "data_cutoff_assumption": DATA_CUTOFF, "permutation_seed": PERMUTATION_SEED, "permutation_rounds": PERMUTATION_ROUNDS, "check_status_counts": counts,
    }, paths.reports / "run_metadata.json")
    log.info("Validation: %s", json.dumps(counts, sort_keys=True))
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--stage", choices=("sources", "ingest", "conform", "marts", "all"), default="all")
    parser.add_argument("--build-root", type=Path, default=None,
                        help="Write generated files here instead of the project folders. Used by tests.")
    args = parser.parse_args()
    paths = get_paths(build_root=args.build_root)
    _configure_logging(paths.reports / "pipeline.log")
    results = run_pipeline(paths, args.stage)
    if results is None:
        return 0
    failures = results[results["status"] == checks.FAIL]
    for _, row in failures.iterrows():
        log.error("FAILED %s: %s. Expected %s, observed %s", row["check_id"], row["description"], row["expected"], row["observed"])
    return 1 if len(failures) else 0


if __name__ == "__main__":
    sys.exit(main())
