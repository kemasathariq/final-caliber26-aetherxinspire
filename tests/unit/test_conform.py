"""Conformed-layer logic on small hand-checkable tables, passed through the real staging code."""
from datetime import datetime as D

import pandas as pd
import pytest

from src.data.ingest import stage_table
from src.data.schemas import BOM, FUNCLOC, MITEM, MOVEMENT, NOTIF, PRPO
from src.preprocessing.conform import (ConformError, _Build, build_bridge_fl_material, build_bridge_order_notification, build_dim_functional_location,
                                       build_dim_material, build_dim_supplier, build_fact_issue, build_fact_notification, build_fact_plan_item, build_fact_prpo_line,
                                       normalise_types, read_conformed, type_map)
from src.data.ingest import write_csv
from src.preprocessing.cycle_map import build_map_cycle
from src.validation.duplicates import add_duplicate_columns

M1, M2, M3 = "4100000001", "4100000002", "4300000003"
O1, O2, O3 = "201000000001", "201000000002", "202000000003"


def _stage(spec, rows):
    return stage_table(pd.DataFrame(rows, columns=spec.source_columns, dtype=object), spec)


def _label(table, prefix="X"):
    return add_duplicate_columns(table, prefix)


@pytest.fixture
def small():
    bom = _stage(BOM, [
        ["PX_A", M1, " Bolt ", 2.0, "EA", 1, 5, 0.0, "Stock Item"],
        ["PX_A", M1, " Bolt ", 2.0, "EA", 1, 5, 0.0, "Stock Item"],
        ["PX_B", M1, " Bolt ", 1.5, "EA", 1, 5, 0.0, "Stock Item"],
        ["PX_B", M2, "Bolt", 1.0, "EA", 0, 0, 3.5, "Non Stock"],
        ["SITE_C", M3, "Pipe", 2.5, "M", 0, 0, 7.0, "Stock Item"],
    ])
    funcloc = _stage(FUNCLOC, [["PX_A", " Pump ", "A"], ["PX_B", "Valve", "S"], ["SITE_C", "System", None], ["PX_D", "Unused", "B"]])
    movement = _stage(MOVEMENT, [
        [D(2026, 1, 7), "Issue", M1, " Bolt ", 2, "EA", O1],
        [D(2026, 1, 7), "Issue", M1, " Bolt ", 2, "EA", O1],
        [D(2026, 1, 7), "Issue", M1, " Bolt ", 5, "EA", O1],
        [D(2026, 2, 3), "Issue", M2, "Bolt", 1, "EA", O2],
        [D(2026, 2, 3), "Issue", M1, " Bolt ", 1, "EA", O3],
    ])
    notif = _stage(NOTIF, [
        [D(2026, 1, 1), "101000000001", "N1", O1, "High", "PX_A", " [MSI-B-1] Permanent repair", D(2026, 1, 1), D(2026, 1, 2), D(2026, 1, 5), D(2026, 1, 9), "Complete"],
        [D(2026, 1, 2), "101000000002", "N1", O2, "Low", "PX_A", "PSM25/[MSI-B-2/M] Replace line", D(2026, 1, 3), D(2026, 1, 1), D(2026, 1, 5), D(2026, 1, 4), "Complete"],
        [D(2026, 1, 3), "101000000003", "N1", O2, "Low", "PX_B", "Check", D(2026, 1, 3), D(2026, 1, 4), D(2026, 12, 5), None, "In Progress"],
        [D(2025, 5, 3), "101000000004", "N1", None, "Low", "SITE_C", "Check", D(2025, 5, 3), D(2025, 5, 4), D(2025, 5, 5), None, "In Progress"],
    ])
    mitem = _stage(MITEM, [
        ["PX_A", "Pump", "A", "300000000001", "10001", "Inspect", "1", "2 WEEKLY", D(2027, 1, 1)],
        ["PX_B", "Valve", "S", "300000000001", "10002", "Inspect", "1", "5 YEARLY", D(2025, 3, 5)],
        ["PX_B", "Valve", "S", "300000000002", "10003", "Inspect", "1", "UNKNOWN SPELLING", D(2025, 3, 1)],
    ])
    prpo_row = lambda pr, item, qty, delivery, promised, currency="IDR", desc=" Bolt ", pr_type="PR01": [pr_type, pr, item, D(2026, 1, 10), M1, desc, qty, "EA", delivery, "1000", "G1", "4500000001", item, "100001", "Acme", 100.0, currency, promised]
    prpo = _stage(PRPO, [
        prpo_row("1000000001", "10", 4, D(2026, 1, 5), D(2026, 1, 20)),
        prpo_row("1000000001", "10", 4, D(2026, 1, 5), D(2026, 1, 20)),
        prpo_row("1000000001", "20", 4, D(2026, 1, 15), D(2026, 1, 8)),
        prpo_row("1000000001", "30", 4, D(2026, 12, 15), D(2026, 12, 20)),
    ])
    build = _Build()
    labelled = {"bom": _label(bom), "movement": _label(movement), "prpo": _label(prpo)}
    dim_fl = build_dim_functional_location(funcloc, bom, notif, mitem, build)
    dim_material = build_dim_material(labelled["bom"], movement, prpo, dim_fl, build)
    dim_supplier = build_dim_supplier(prpo, build)
    bridge_material = build_bridge_fl_material(labelled["bom"], dim_material, build)
    bridge_order = build_bridge_order_notification(notif, movement, build)
    return dict(bom=bom, funcloc=funcloc, movement=movement, notif=notif, mitem=mitem, prpo=prpo, build=build, labelled=labelled, dim_fl=dim_fl, dim_material=dim_material,
                dim_supplier=dim_supplier, bridge_material=bridge_material, bridge_order=bridge_order)


def test_dim_material_is_one_row_per_material_and_does_not_count_copies(small):
    dim = small["dim_material"].set_index("material_no")
    assert list(dim.index) == [M1, M2, M3]
    assert dim.loc[M1, "n_bom_rows"] == 3 and dim.loc[M1, "n_bom_locations"] == 2
    assert dim.loc[M1, "n_fl_crit_A"] == 1 and dim.loc[M1, "n_fl_crit_S"] == 1
    assert dim.loc[M3, "n_fl_crit_null"] == 1


def test_material_flags_are_raw_comparisons(small):
    dim = small["dim_material"].set_index("material_no")
    assert dim.loc[M1, "stock_eq_zero"] and dim.loc[M1, "stock_lt_min"] and not dim.loc[M1, "stock_gt_max"]
    assert dim.loc[M2, "nonstock_with_stock"] and dim.loc[M2, "flag_fraction_on_count_unit"]
    assert dim.loc[M3, "stockitem_min_max_zero"] and not dim.loc[M3, "flag_fraction_on_count_unit"]
    assert dim.loc[M1, "is_issued"] and not dim.loc[M3, "is_issued"]
    assert dim.loc[M1, "is_procured"] and not dim.loc[M2, "is_procured"]


def test_shared_description_is_flagged_and_materials_stay_separate(small):
    dim = small["dim_material"].set_index("material_no")
    assert dim.loc[M1, "material_desc"] == " Bolt " and dim.loc[M1, "material_desc_clean"] == "Bolt"
    assert dim.loc[M1, "desc_shared_group_id"] == dim.loc[M2, "desc_shared_group_id"]
    assert pd.isna(dim.loc[M3, "desc_shared_group_id"])
    assert dim.index.is_unique and len(dim) == 3


def test_conflicting_material_attributes_stop_dim_material(small):
    bad = small["labelled"]["bom"].copy()
    bad.loc[0, "stock"] = 99.0
    with pytest.raises(ConformError, match="differ within a material"):
        build_dim_material(bad, small["movement"], small["prpo"], small["dim_fl"], _Build())


def test_bridge_records_every_source_row_it_represents(small):
    bridge = small["bridge_material"].set_index(["functional_location", "material_no"])
    assert len(bridge) == 4
    assert bridge.loc[("PX_A", M1), "occurrence_count"] == 2
    assert bridge.loc[("PX_A", M1), "all_source_rows"] == "2;3"
    assert bridge.loc[("PX_B", M1), "flag_non_integer_installed_qty"]
    assert bridge.loc[("PX_B", M1), "flag_fraction_on_count_unit"]
    assert not bridge.loc[("SITE_C", M3), "flag_fraction_on_count_unit"]


def test_pair_with_differing_content_stops_the_bridge(small):
    bom = small["bom"].copy()
    bom.loc[1, "installed_qty"] = 9.0
    bom.loc[1, "row_hash"] = "changed"
    with pytest.raises(ConformError, match="differing content"):
        build_bridge_fl_material(_label(bom), small["dim_material"], _Build())


def test_supplier_with_two_names_stops_dim_supplier(small):
    prpo = small["prpo"].copy()
    prpo.loc[0, "supplier_name"] = "Other"
    with pytest.raises(ConformError, match="more than one name"):
        build_dim_supplier(prpo, _Build())


def test_blank_criticality_is_kept_with_its_reason(small):
    dim = small["dim_fl"].set_index("functional_location")
    assert pd.isna(dim.loc["SITE_C", "criticality"])
    assert dim.loc["SITE_C", "criticality_missing_reason"] == "system_level_row"
    assert dim.loc["PX_D", "fl_has_bom"] == False  # noqa: E712
    assert dim.loc["PX_A", "fl_in_all_three"] == True  # noqa: E712
    assert dim.loc["PX_A", "fl_desc"] == " Pump " and dim.loc["PX_A", "fl_desc_clean"] == "Pump"


def test_prpo_keeps_all_rows_and_flags_dates(small):
    fact = build_fact_prpo_line(small["labelled"]["prpo"], small["dim_material"], small["dim_supplier"], small["build"])
    assert len(fact) == 4 and fact["source_row"].tolist() == [2, 3, 4, 5]
    assert fact["in_exact_distinct_rows"].tolist() == [True, False, True, True]
    assert fact["material_desc"].iloc[0] == " Bolt " and fact["material_desc_clean"].iloc[0] == "Bolt"
    assert fact["requested_interval_days"].tolist() == [-5, -5, 5, 339]
    assert fact["promised_interval_days"].tolist() == [10, 10, -2, 344]
    assert fact["promise_gap_days"].tolist() == [15, 15, -7, 5]
    assert fact["flag_req_before_pr"].tolist() == [True, True, False, False]
    assert fact["flag_promise_before_pr"].tolist() == [False, False, True, False]
    assert fact["flag_future_date"].tolist() == [False, False, False, True]
    assert fact["pr_prefix"].iloc[0] == "10" and fact["pr_month"].iloc[0] == pd.Timestamp("2026-01-01")


def test_view_specific_flags_are_blank_outside_their_view(small):
    fact = build_fact_prpo_line(small["labelled"]["prpo"], small["dim_material"], small["dim_supplier"], small["build"])
    for column in ("flag_outlier_pr_quantity__exact_distinct_rows", "flag_extreme_interval__exact_distinct_rows"):
        assert pd.isna(fact[column].iloc[1]) and pd.notna(fact[column].iloc[0])
    assert fact["flag_outlier_pr_quantity__original_rows"].notna().all()


def test_rare_categories_count_distinct_rows(small):
    fact = build_fact_prpo_line(small["labelled"]["prpo"], small["dim_material"], small["dim_supplier"], small["build"])
    assert fact["rare_pr_type"].all()


def test_no_unit_amount_or_fx_columns_are_derived(small):
    fact = build_fact_prpo_line(small["labelled"]["prpo"], small["dim_material"], small["dim_supplier"], small["build"])
    assert not [c for c in fact.columns if "unit_amount" in c or "amount_idr" in c or c.endswith("_lead_days")]


def test_issue_attribution_never_allocates_a_shared_order(small):
    fact = build_fact_issue(small["labelled"]["movement"], small["bridge_order"], small["bridge_material"], small["dim_material"], small["build"])
    assert fact["fl_attribution"].tolist() == ["unique", "unique", "unique", "ambiguous", "none"]
    assert fact["attributed_functional_location"].iloc[0] == "PX_A"
    assert pd.isna(fact["attributed_functional_location"].iloc[3]) and pd.isna(fact["attributed_functional_location"].iloc[4])
    assert fact["order_shared"].tolist() == [False, False, False, True, False]
    # M2 is on the BoM of PX_B, one of the shared order's two locations.
    assert fact["n_candidate_locations_with_material"].iloc[3] == 1
    assert fact["issued_material_in_fl_bom"].iloc[0] == True  # noqa: E712
    assert pd.isna(fact["issued_material_in_fl_bom"].iloc[4])


def test_issue_labels_copies_and_partial_groups_without_removing_rows(small):
    fact = build_fact_issue(small["labelled"]["movement"], small["bridge_order"], small["bridge_material"], small["dim_material"], small["build"])
    assert len(fact) == 5
    assert fact["in_exact_distinct_rows"].tolist() == [True, False, True, True, True]
    assert fact["is_partial_dup_group"].tolist() == [True, True, True, False, False]
    assert fact["partial_dup_group_id"].nunique() == 1 and fact["same_key_group_size"].iloc[0] == 3
    assert fact["posting_month"].iloc[3] == pd.Timestamp("2026-02-01")
    assert fact["posting_week"].iloc[3] == pd.Timestamp("2026-02-02")  # 2026-02-03 is a Tuesday


def test_bridge_order_marks_shared_orders_and_leaves_blank_orders_out(small):
    bridge = small["bridge_order"]
    assert len(bridge) == 3
    assert bridge["order_shared"].tolist() == [False, True, True]
    assert pd.isna(bridge["shared_order_same_fl"].iloc[0]) and bridge["shared_order_same_fl"].iloc[1] == False  # noqa: E712


def test_notification_blanks_stay_blank_and_open_records_are_censored(small):
    fact = build_fact_notification(small["notif"], small["bridge_order"], small["dim_fl"], small["movement"], small["build"]).set_index("notification")
    done, late_row, open_row, blank_order = ("101000000001", "101000000002", "101000000003", "101000000004")
    assert pd.isna(fact.loc[open_row, "completion_date"]) and pd.isna(fact.loc[open_row, "days_to_complete"])
    assert fact.loc[open_row, "is_censored"] and fact.loc[open_row, "days_open_at_cutoff"] == (pd.Timestamp("2026-09-30") - pd.Timestamp("2026-01-03")).days
    assert pd.isna(fact.loc[done, "days_open_at_cutoff"]) and fact.loc[done, "days_to_complete"] == 8
    assert fact.loc[done, "completed_late"] == True and fact.loc[late_row, "completed_late"] == False  # noqa: E712
    assert pd.isna(fact.loc[open_row, "completed_late"])
    assert fact.loc[blank_order, "order_missing"] and pd.isna(fact.loc[blank_order, "order_no"])
    assert fact.loc[blank_order, "first_month_flag"] and fact.loc[blank_order, "is_system_level"]
    assert fact.loc[open_row, "flag_future_date"]
    assert fact.loc[late_row, "flag_reqstart_before_notif"] and fact.loc[late_row, "flag_created_differs"]


def test_reference_codes_are_found_in_both_observed_forms(small):
    fact = build_fact_notification(small["notif"], small["bridge_order"], small["dim_fl"], small["movement"], small["build"])
    assert fact["desc_ref_code"].tolist()[:2] == ["MSI-B-1", "MSI-B-2/M"]
    assert pd.isna(fact["desc_ref_code"].iloc[2])
    assert fact["description"].iloc[0] == " [MSI-B-1] Permanent repair"


def test_plan_items_use_proposed_names_and_flag_unmapped_spellings(small):
    fact = build_fact_plan_item(small["mitem"], build_map_cycle(), small["dim_fl"], small["build"])
    assert fact["interval_value_proposed"].tolist()[:2] == [2, 5]
    assert fact["interval_unit_proposed"].tolist()[:2] == ["WEEK", "YEAR"]
    assert fact["flag_cycle_unmapped"].tolist() == [False, False, True]
    assert fact["cycle_desc"].astype("string").iloc[2] == "UNKNOWN SPELLING"
    assert fact["flag_future_cycle_start"].tolist() == [True, False, False]
    assert fact["start_day_is_first"].tolist() == [True, False, True]
    assert fact["plan_multi_fl"].tolist() == [True, True, False]
    assert not [c for c in fact.columns if "due" in c]


def test_cycle_map_covers_all_documented_rows_and_days():
    table = build_map_cycle().set_index("cycle_desc")
    assert len(table) == 28 and table["rows_documented_in_spec"].sum() == 10153
    assert table.loc["2 WEEKLY", "interval_days_proposed"] == 14
    assert table.loc["18 MONTHLY", "interval_days_proposed"] == 547.875
    assert table.loc["10 YEARLY", "interval_days_proposed"] == 3652.5
    assert table.loc["2 WEEKLY", "mapping_basis"] == "direct_ambiguous_reading"
    assert set(table["mapping_status"]) == {"proposed_requires_DEF-10"}


def test_conformed_csv_round_trip_keeps_identifiers_blanks_and_types(tmp_path, small):
    frame = normalise_types(pd.DataFrame({
        "code": pd.array(["0012", None], dtype="string"), "n": pd.array([1, None], dtype="Int64"), "x": pd.array([1.5, None], dtype="Float64"),
        "flag": pd.array([True, None], dtype="boolean"), "day": pd.to_datetime(["2026-01-01", None]).astype("datetime64[ns]"), "cat": pd.Categorical(["A", None])}))
    write_csv(frame, tmp_path / "t.csv")
    back = read_conformed(tmp_path / "t.csv", type_map(frame))
    assert back["code"].iloc[0] == "0012"
    assert type_map(back) == type_map(frame)
    assert back.isna().sum().tolist() == [1] * 6
