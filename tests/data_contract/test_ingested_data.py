"""Real workbooks: rows, values, identifiers, types, missing patterns and duplicates."""
import pandas as pd
import pytest

from src.data.schemas import DATASETS, LINEAGE_COLUMNS
from src.preprocessing.prpo_views import DISTINCT, ORIGINAL

pytestmark = pytest.mark.data_contract

ROWS = {"prpo": 11609, "movement": 17518, "notif": 5795, "mitem": 10153, "bom": 20653, "funcloc": 14484}
COLUMNS = {"prpo": 18, "movement": 7, "notif": 12, "mitem": 9, "bom": 9, "funcloc": 3}


@pytest.mark.parametrize("key", ROWS)
def test_all_source_rows_are_preserved(real_state, key):
    table = real_state["tables"][key]
    assert len(table) == ROWS[key]
    assert table["source_row"].tolist() == list(range(2, ROWS[key] + 2))
    assert len(DATASETS[key].columns) == COLUMNS[key]
    assert list(table.columns) == DATASETS[key].standard_columns + list(LINEAGE_COLUMNS)


def test_representative_values_match_the_workbooks(real_state):
    t = real_state["tables"]
    first = t["prpo"].iloc[0]
    assert (first["purchase_requisition"], first["pr_item"], first["purchase_order"], first["po_item"]) == ("1200009275", "10", "4300005365", "20")
    assert (first["pr_quantity"], first["po_item_amount"], first["supplier_code"]) == (17, 15378989.0, "101872")
    assert first["pr_date"] == pd.Timestamp("2025-10-05")
    assert t["movement"].iloc[0]["order_no"] == "201000002982"
    assert t["notif"].iloc[0]["description"] == "[MSI-B-25-PTP-346/M] Replace line"
    assert t["mitem"].iloc[0]["plan_priority"] == "2"
    assert t["bom"].iloc[0]["functional_location"] == "PX_1-1/2-BF-1913-A21A"
    site = t["funcloc"].iloc[0]
    assert site["functional_location"] == "SITE_PX_S01" and pd.isna(site["criticality"])


@pytest.mark.parametrize("key", ROWS)
def test_identifiers_stay_strings_after_csv_round_trip(real_state, key):
    for name, table in (("memory", real_state["tables"][key]), ("csv", real_state["reloaded"][key])):
        for column in DATASETS[key].by_kind("identifier"):
            assert table[column].dtype == "string", f"{name}: {column}"


def test_nullable_order_is_never_stored_as_a_float(real_state):
    orders = real_state["reloaded"]["notif"]["order_no"].dropna()
    assert orders.str.fullmatch(r"\d{12}").all()
    assert not orders.str.contains(".", regex=False).any()


def test_two_priority_code_systems_stay_separate(real_state):
    t = real_state["tables"]
    assert set(t["notif"]["notif_priority"].astype("string")) == {"Low", "Medium", "High", "Emergency"}
    assert set(t["mitem"]["plan_priority"].astype("string")) == {"2", "3"}
    assert "priority" not in t["notif"].columns and "priority" not in t["mitem"].columns


def test_missing_values_are_structural_and_unimputed(real_state):
    notif, funcloc = real_state["tables"]["notif"], real_state["tables"]["funcloc"]
    in_progress = notif["status"] == "In Progress"
    assert notif["order_no"].isna().sum() == 553 and notif.loc[notif["order_no"].isna(), "status"].eq("In Progress").all()
    assert notif["completion_date"].isna().equals(in_progress.astype(bool))
    assert funcloc["criticality"].isna().sum() == 33
    assert funcloc.loc[funcloc["criticality"].isna(), "functional_location"].str.startswith("SITE").all()


def test_description_whitespace_is_not_altered(real_state):
    t = real_state["tables"]
    assert {k: int((t[k]["material_desc"] != t[k]["material_desc"].str.strip()).sum()) for k in ("prpo", "movement", "bom")} == {"prpo": 191, "movement": 128, "bom": 438}


@pytest.mark.parametrize("key, extras, distinct", [("prpo", 5420, 6189), ("movement", 863, 16655), ("bom", 230, 20423),
                                                   ("notif", 0, 5795), ("mitem", 0, 10153), ("funcloc", 0, 14484)])
def test_duplicates_are_detected_but_not_removed(real_state, key, extras, distinct):
    labelled = real_state["labelled"][key]
    assert len(labelled) == ROWS[key]
    assert int((labelled["occurrence_rank"] > 1).sum()) == extras
    assert int((labelled["occurrence_rank"] == 1).sum()) == distinct
    assert len(real_state["tables"][key]) == ROWS[key]


def test_prpo_views_preserve_and_separate_records(real_state):
    original, distinct = real_state["views"][ORIGINAL], real_state["views"][DISTINCT]
    groups = real_state["groups"]["prpo"]
    assert len(original) == 11609 and len(distinct) == 6189 and len(groups) == 3600
    assert set(original["analysis_view"]) == {ORIGINAL} and set(distinct["analysis_view"]) == {DISTINCT}
    assert groups["occurrence_count"].sum() + (distinct["occurrence_count"] == 1).sum() == 11609
    assert groups["all_source_columns_identical"].all()
    assert (groups["groups_sharing_purchase_requisition__pr_item"] == 1).all()


def test_every_prpo_row_can_be_traced_through_the_distinct_view(real_state):
    distinct = real_state["views"][DISTINCT]
    rows = sorted(int(r) for text in distinct["all_source_rows"] for r in text.split(";"))
    assert rows == list(range(2, 11611))


def test_view_totals_stay_in_their_own_currency_and_view(real_build):
    comparison = pd.read_csv(real_build["paths"].tables / "prpo_view_comparison.csv")
    amounts = comparison[comparison["metric"] == "po_item_amount_sum"].set_index("group")
    assert set(amounts.index) == {"IDR", "USD", "EUR", "JPY", "SGD"}
    assert amounts.loc["IDR", ORIGINAL] == 168836490165.0
    assert amounts.loc["IDR", DISTINCT] == 89210784211.0
    assert amounts.loc["SGD", ORIGINAL] == amounts.loc["SGD", DISTINCT]
    assert not comparison["metric"].str.contains("actual|lead_time").any()
