"""The conformed layer on the real workbooks, including recalculations that share no project code."""
import csv
import json
import statistics
from collections import defaultdict

import pandas as pd
import pytest

from src.config import get_paths
from src.preprocessing.conform import read_conformed
from src.preprocessing.prpo_views import DISTINCT, ORIGINAL
from src.validation import conformed_checks as cc
from src.validation.checks import FAIL, PASS

pytestmark = pytest.mark.data_contract

CONFORMED = ["dim_functional_location", "dim_material", "dim_supplier", "map_cycle", "bridge_fl_material", "bridge_order_notification",
             "fact_prpo_line", "fact_issue", "fact_notification", "fact_plan_item"]
EXCEPTIONS = ["prpo_requested_before_pr", "prpo_promised_before_pr", "prpo_future_dates", "movement_same_key_different_quantity", "notif_required_start_before_notification",
              "notif_created_on_differs", "notif_same_location_description_date", "plan_future_cycle_start", "material_nonstock_with_stock", "material_fraction_on_count_unit",
              "bom_non_integer_installed_qty", "material_shared_descriptions", "shared_orders", "outliers"]


def _raw(real_build, folder, name):
    with open(real_build["root"] / folder / f"{name}.csv", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _staged(real_build, name):
    return _raw(real_build, "data/interim/staged", f"stg_{name}")


def _conformed(real_build, name):
    return _raw(real_build, "data/interim/conformed", name)


@pytest.mark.parametrize("name", CONFORMED)
def test_conformed_table_exists_with_metadata(real_build, name):
    metadata = json.loads((real_build["paths"].conformed / "conformed_metadata.json").read_text())
    frame = read_conformed(real_build["paths"].conformed / f"{name}.csv", metadata["tables"][name]["columns"])
    assert len(frame) == metadata["tables"][name]["rows"] > 0


def test_metadata_records_version_policies_and_parameters(real_build):
    metadata = json.loads((real_build["paths"].conformed / "conformed_metadata.json").read_text())
    assert metadata["spec_version"] == "0.1+corrections-3"
    assert metadata["parameters"]["data_cutoff_assumption"] == "2026-09-30"
    assert metadata["parameters"]["outliers"]["robust_z_threshold"] == 3.5
    assert "Neither is definitive" in metadata["policies"]["prpo"]
    assert "synthetic" in metadata["data_label"]


@pytest.mark.parametrize("name", EXCEPTIONS)
def test_exception_list_exists_with_rows(real_build, name):
    assert len(pd.read_csv(real_build["paths"].exceptions / f"{name}.csv", dtype=str)) > 0


def test_identifiers_in_the_stored_csv_have_no_numeric_damage(real_build):
    for table, column, length in (("fact_prpo_line", "purchase_order", 10), ("fact_issue", "order_no", 12), ("dim_material", "material_no", 10), ("bridge_order_notification", "order_no", 12)):
        values = [row[column] for row in _conformed(real_build, table)]
        assert all(value.isdigit() and len(value) == length for value in values), table
    assert any(row["order_no"] == "" for row in _conformed(real_build, "fact_notification"))


def test_requested_before_pr_recalculated_without_project_code(real_build):
    rows = _staged(real_build, "prpo")
    flagged = {r["source_row"] for r in rows if r["pr_delivery_date"] < r["pr_date"]}  # ISO dates sort as text
    assert len(flagged) == 630
    assert {r["source_row"] for r in _conformed(real_build, "fact_prpo_line") if r["flag_req_before_pr"] == "True"} == flagged


def test_exact_distinct_selection_recalculated_without_project_code(real_build):
    seen, first = set(), set()
    for row in _staged(real_build, "prpo"):
        if row["row_hash"] not in seen:
            seen.add(row["row_hash"])
            first.add(row["source_row"])
    assert len(first) == 6189
    assert {r["source_row"] for r in _conformed(real_build, "fact_prpo_line") if r["in_exact_distinct_rows"] == "True"} == first


def test_attribution_recalculated_without_project_code(real_build):
    locations = defaultdict(set)
    for row in _staged(real_build, "notif"):
        if row["order_no"]:
            locations[row["order_no"]].add(row["functional_location"])
    expected, attributed = {}, {}
    for row in _staged(real_build, "movement"):
        found = locations.get(row["order_no"], set())
        expected[row["source_row"]] = "none" if not found else ("unique" if len(found) == 1 else "ambiguous")
        attributed[row["source_row"]] = next(iter(found)) if len(found) == 1 else ""
    fact = _conformed(real_build, "fact_issue")
    assert {r["source_row"]: r["fl_attribution"] for r in fact} == expected
    assert {r["source_row"]: r["attributed_functional_location"] for r in fact} == attributed


def test_bom_pair_match_recalculated_without_project_code(real_build):
    pairs = {(r["functional_location"], r["material_no"]) for r in _staged(real_build, "bom")}
    linked = defaultdict(set)
    for row in _staged(real_build, "notif"):
        if row["order_no"]:
            linked[row["order_no"]].add(row["functional_location"])
    matched = {r["source_row"] for r in _staged(real_build, "movement") if any((fl, r["material_no"]) in pairs for fl in linked.get(r["order_no"], ()))}
    assert {r["source_row"] for r in _conformed(real_build, "fact_issue") if r["issued_material_in_fl_bom"] == "True"} == matched


def test_robust_z_recalculated_without_project_code_on_every_large_material(real_build):
    """The all-rows Movement quantity flag, recalculated with the statistics module."""
    by_material = defaultdict(list)
    for row in _staged(real_build, "movement"):
        by_material[row["material_no"]].append((row["source_row"], float(row["quantity"])))
    flags = {r["source_row"]: r["flag_outlier_quantity__all_rows"] for r in _conformed(real_build, "fact_issue")}
    checked = 0
    for rows in by_material.values():
        values = [v for _, v in rows]
        median = statistics.median(values)
        mad = statistics.median(abs(v - median) for v in values)
        if len(values) < 5 or mad == 0:
            continue
        for source_row, value in rows:
            assert (flags[source_row] == "True") == (abs(0.6745 * (value - median) / mad) > 3.5), source_row
            checked += 1
    assert checked == 10645


def test_outlier_populations_differ_by_view_so_flags_are_held_per_view(real_conformed):
    fact = real_conformed["tables"]["fact_prpo_line"]
    a, b = fact["flag_outlier_pr_quantity__original_rows"], fact["flag_outlier_pr_quantity__exact_distinct_rows"]
    inside = fact["in_exact_distinct_rows"]
    assert (a[inside] != b[inside]).sum() > 0


def test_exception_counts_equal_flag_counts(real_build, real_conformed):
    summary = pd.read_csv(real_build["paths"].tables / "exception_summary.csv")
    tables = real_conformed["tables"]
    for _, row in summary[summary["flag"] != "desc_shared_group_id"].iterrows():
        assert row["rows"] == int(tables[row["table"]][row["flag"]].fillna(False).astype(bool).sum()), row["exception_list"]


def test_transformation_log_shows_no_fact_lost_a_row(real_conformed):
    log = real_conformed["transformation_log"]
    facts = log[log["table"].str.startswith("fact_")]
    assert len(facts) == 4 and (facts["rows_before"] == facts["rows_after"]).all()


def test_duplicate_report_states_no_cause_and_no_default_view(real_build):
    text = (real_build["paths"].reports / "duplicate_evidence.md").read_text()
    assert "Cannot be confirmed from the available data or documentation" in text
    assert "documented as synthetic" in text


def test_permutation_results_match_the_audit_to_three_places(real_build):
    table = pd.read_csv(real_build["paths"].tables / "prpo_copy_permutation_tests.csv").set_index("grouping")
    assert table.loc["purchase_requisition", ["observed_same_copy_share", "shuffled_mean"]].round(3).tolist() == [0.255, 0.265]
    assert table.loc["purchase_order", ["observed_same_copy_share", "shuffled_mean"]].round(3).tolist() == [0.125, 0.142]
    assert table.loc["material_no", ["observed_same_copy_share", "shuffled_mean"]].round(3).tolist() == [0.144, 0.151]


def test_relationship_audit_covers_every_spec_relationship(real_build):
    audit = pd.read_csv(real_build["paths"].tables / "relationship_audit.csv")
    names = {r.split(".")[0] for r in audit["relationship"]}
    assert names == {f"R{i}" for i in range(1, 14)}
    assert audit["safe_for_analysis"].notna().all()


def test_no_table_combines_currencies_or_ranks_suppliers(real_build, real_conformed):
    for frame in real_conformed["tables"].values():
        assert not [c for c in frame.columns if "total_amount" in c or "spend" in c or "rank" in c and c not in ("occurrence_rank",)]
    assert set(real_conformed["tables"]["dim_supplier"].columns) == {"supplier_code", "supplier_name", "currency", "supplier_name_clean", "is_non_idr_currency"}


# Failure detection: each damages a copy of real conformed data and expects a failed check.

def _statuses(rows):
    return {row["check_id"]: row["status"] for row in rows}


def _tables(real_conformed):
    return {name: frame.copy() for name, frame in real_conformed["tables"].items()}


def test_detects_a_changed_source_value(real_state, real_conformed):
    tables = _tables(real_conformed)
    tables["fact_prpo_line"].loc[5, "po_item_amount"] = 1.0
    assert _statuses(cc.check_facts_preserve_sources(tables, real_state["tables"]))["CONF-03.fact_prpo_line"] == FAIL


def test_detects_a_lost_row(real_state, real_conformed):
    tables = _tables(real_conformed)
    tables["fact_issue"] = tables["fact_issue"].iloc[:-1]
    results = _statuses(cc.check_facts_preserve_sources(tables, real_state["tables"]))
    assert results["CONF-01.fact_issue"] == FAIL and results["CONF-02.fact_issue"] == FAIL


def test_detects_a_trimmed_source_description(real_state, real_conformed):
    tables = _tables(real_conformed)
    fact = tables["fact_prpo_line"]
    fact["material_desc"] = fact["material_desc"].str.strip()
    assert _statuses(cc.check_facts_preserve_sources(tables, real_state["tables"]))["CONF-03.fact_prpo_line"] == FAIL


def test_detects_a_filled_blank_completion_date(real_state, real_conformed):
    tables = _tables(real_conformed)
    fact = tables["fact_notification"]
    fact.loc[fact["completion_date"].isna(), "completion_date"] = pd.Timestamp("2026-09-30")
    assert _statuses(cc.check_facts_preserve_sources(tables, real_state["tables"]))["CONF-03.fact_notification"] == FAIL


def test_detects_a_changed_material_attribute(real_state, real_conformed):
    tables = _tables(real_conformed)
    tables["dim_material"].loc[0, "stock"] = 123456.0
    assert _statuses(cc.check_keys_and_coarser_tables(tables, real_state["tables"]))["CONF-06"] == FAIL


def test_detects_a_repeated_dimension_key(real_state, real_conformed):
    tables = _tables(real_conformed)
    tables["dim_supplier"] = pd.concat([tables["dim_supplier"], tables["dim_supplier"].iloc[[0]]], ignore_index=True)
    assert _statuses(cc.check_keys_and_coarser_tables(tables, real_state["tables"]))["CONF-04.dim_supplier"] == FAIL


def test_detects_a_bridge_that_lost_a_source_row(real_state, real_conformed):
    tables = _tables(real_conformed)
    tables["bridge_fl_material"] = tables["bridge_fl_material"].iloc[1:]
    assert _statuses(cc.check_keys_and_coarser_tables(tables, real_state["tables"]))["CONF-05.source_rows"] == FAIL


def _flag_checks(tables, real_state, real_build):
    measures = json.loads((real_build["paths"].tables / "quality_measures.json").read_text())
    return _statuses(cc.check_views_and_flags(tables, real_state["views"], measures))


def test_detects_a_wrong_flag(real_state, real_conformed, real_build):
    tables = _tables(real_conformed)
    tables["fact_prpo_line"].loc[0, "flag_req_before_pr"] = not tables["fact_prpo_line"].loc[0, "flag_req_before_pr"]
    assert _flag_checks(tables, real_state, real_build)["CONF-09.fact_prpo_line.flag_req_before_pr"] == FAIL


def test_detects_a_wrong_view_selection(real_state, real_conformed, real_build):
    tables = _tables(real_conformed)
    tables["fact_prpo_line"]["in_exact_distinct_rows"] = True
    results = _flag_checks(tables, real_state, real_build)
    assert results["CONF-07.rows"] == FAIL and results["CONF-07.amount.IDR"] == FAIL


def test_detects_a_view_flag_outside_its_view(real_state, real_conformed, real_build):
    tables = _tables(real_conformed)
    fact = tables["fact_issue"]
    fact["flag_outlier_quantity__exact_distinct_rows"] = fact["flag_outlier_quantity__all_rows"]
    assert _flag_checks(tables, real_state, real_build)["CONF-08.fact_issue.flag_outlier_quantity__exact_distinct_rows"] == FAIL


def test_detects_an_allocated_shared_order(real_state, real_conformed, real_build):
    tables = _tables(real_conformed)
    fact = tables["fact_issue"]
    fact.loc[fact["order_shared"], "attributed_functional_location"] = "PX_ALLOCATED"
    assert _flag_checks(tables, real_state, real_build)["CONF-10.ambiguous_not_allocated"] == FAIL


@pytest.mark.parametrize("column", ["priority_rank", "stock_status", "actual_lead_time", "amount_idr_scenario", "implied_unit_amount", "projected_due_date", "failure_flag"])
def test_detects_a_column_applying_an_unapproved_rule(real_conformed, column):
    tables = _tables(real_conformed)
    tables["fact_notification"][column] = 1
    assert _statuses(cc.check_no_unapproved_rules(tables))["CONF-11.fact_notification"] == FAIL


def test_detects_ranked_criticality(real_conformed):
    tables = _tables(real_conformed)
    fact = tables["dim_functional_location"]
    fact["criticality"] = fact["criticality"].cat.as_ordered()
    assert _statuses(cc.check_no_unapproved_rules(tables))["CONF-12.dim_functional_location"] == FAIL


def test_detects_an_unmapped_cycle_spelling(real_conformed):
    tables = _tables(real_conformed)
    tables["fact_plan_item"].loc[0, "flag_cycle_unmapped"] = True
    assert _statuses(cc.check_cycle_map(tables))["CONF-13.unmapped"] == FAIL


def test_detects_a_join_that_lost_or_multiplied_rows():
    audit = pd.DataFrame([{"join": "x", "left_rows": 10, "result_rows": 11, "unmatched_rows": 2}])
    results = _statuses(cc.check_join_audit(audit))
    assert results["JOIN.x.rows"] == FAIL and results["JOIN.x.unmatched"] == FAIL


def test_detects_a_conformed_csv_with_damaged_identifiers(tmp_path, real_conformed, real_build):
    from src.data.ingest import write_csv
    frame = real_conformed["tables"]["dim_supplier"]
    damaged = frame.astype({"supplier_code": "string"}).copy()
    damaged["supplier_code"] = damaged["supplier_code"] + ".0"
    write_csv(damaged, tmp_path / "dim_supplier.csv")
    assert _statuses(cc.check_conformed_round_trip({"dim_supplier": frame}, tmp_path))["CONF-14.dim_supplier"] == FAIL


def test_healthy_real_tables_pass_the_same_checks(real_state, real_conformed, real_build):
    """The damage tests above only mean something if undamaged data passes."""
    tables = _tables(real_conformed)
    rows = (cc.check_facts_preserve_sources(tables, real_state["tables"]) + cc.check_keys_and_coarser_tables(tables, real_state["tables"])
            + cc.check_no_unapproved_rules(tables) + cc.check_cycle_map(tables))
    assert {row["status"] for row in rows} == {PASS}
    assert set(_flag_checks(tables, real_state, real_build).values()) == {PASS}
