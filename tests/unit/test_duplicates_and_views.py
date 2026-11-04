"""Duplicate labelling and PR PO views on hand-checkable data."""
import datetime as dt

import pandas as pd
import pytest

from src.data.ingest import stage_table
from src.data.schemas import DUPLICATE_SETTINGS, PRPO
from src.preprocessing.prpo_views import DISTINCT, ORIGINAL, build_prpo_views, compare_views
from src.validation.duplicates import add_duplicate_columns, duplicate_group_metadata, duplicate_summary


def prpo_row(pr, item, po, po_item, qty, amount, currency="IDR", unit="EA"):
    day = dt.datetime(2026, 1, 1)
    return {"PR-Type": "PR03", "Purchase Requisition": pr, "PR-Item": item, "PR-Date": day, "PR-Material": "4100000001",
            "PR-Material Desc": "PART", "PR-Quantity": qty, "PR-UoM": unit, "PR-Delivery Date": day + dt.timedelta(days=10),
            "PR-Plant": "1000", "PR-Purchasing Group": "MR1", "Purchase Order": po, "PO-Item": po_item,
            "PO-Supplier Code": "100001", "PO-Supplier Name": "S PT", "PO-Item Amount": amount,
            "PO-Currency": currency, "PO-Delivery Date": day + dt.timedelta(days=20)}


@pytest.fixture
def labelled():
    """Rows 2, 4 and 7 are copies. Rows 3 and 6 are copies. Row 5 is single. Row 8 reuses a key with new content."""
    a = prpo_row("1200000001", "10", "4300000001", "10", 2, 100.0)
    b = prpo_row("1200000002", "10", "4300000002", "10", 5, 50.0, currency="USD")
    c = prpo_row("1200000003", "10", "4300000003", "10", 1, 10.0)
    d = prpo_row("1200000001", "10", "4300000009", "10", 9, 999.0)
    source = pd.DataFrame([a, b, a, c, b, a, d], dtype=object)
    return add_duplicate_columns(stage_table(source, PRPO), "PRPO")


def test_labelling_keeps_every_row(labelled):
    assert labelled["source_row"].tolist() == [2, 3, 4, 5, 6, 7, 8]


def test_occurrence_counts_and_ranks(labelled):
    assert labelled["occurrence_count"].tolist() == [3, 2, 3, 1, 2, 3, 1]
    assert labelled["occurrence_rank"].tolist() == [1, 1, 2, 1, 2, 3, 1]
    assert labelled["content_group_id"].tolist() == [
        "PRPO-000001", "PRPO-000002", "PRPO-000001", "PRPO-000003", "PRPO-000002", "PRPO-000001", "PRPO-000004"]


def test_summary_counts(labelled):
    summary = duplicate_summary(labelled, "prpo")
    assert (summary["total_rows"], summary["distinct_rows"], summary["extra_copies"], summary["groups_with_copies"]) == (7, 4, 3, 2)
    assert summary["occurrence_distribution"] == '{"1": 2, "2": 1, "3": 1}'


def test_group_metadata_references_source_rows(labelled):
    s = DUPLICATE_SETTINGS["prpo"]
    groups = duplicate_group_metadata(labelled, PRPO.standard_columns, s["key_sets"], s["measures"], s["context"]).set_index("content_group_id")
    assert list(groups.index) == ["PRPO-000001", "PRPO-000002"]
    first = groups.loc["PRPO-000001"]
    assert first["source_rows"] == "2;4;7"
    assert first["occurrence_count"] == 3
    assert first["source_row_span"] == 5
    assert bool(first["all_source_columns_identical"])
    assert first["po_item_amount"] == 100.0
    assert first["po_item_amount_sum_all_occurrences"] == 300.0
    assert first["pr_quantity_sum_all_occurrences"] == 6


def test_metadata_flags_a_key_shared_with_different_content(labelled):
    s = DUPLICATE_SETTINGS["prpo"]
    groups = duplicate_group_metadata(labelled, PRPO.standard_columns, s["key_sets"], s["measures"], s["context"]).set_index("content_group_id")
    assert groups.loc["PRPO-000001", "groups_sharing_purchase_requisition__pr_item"] == 2
    assert groups.loc["PRPO-000002", "groups_sharing_purchase_requisition__pr_item"] == 1


def test_views_hold_all_rows_and_first_occurrences(labelled):
    original, distinct = build_prpo_views(labelled)
    assert len(original) == 7 and len(distinct) == 4
    assert set(original["analysis_view"]) == {ORIGINAL}
    assert set(distinct["analysis_view"]) == {DISTINCT}
    assert distinct["source_row"].tolist() == [2, 3, 5, 8]
    assert distinct["all_source_rows"].tolist() == ["2;4;7", "3;6", "5", "8"]


def test_view_building_does_not_change_its_input(labelled):
    before = labelled.copy()
    build_prpo_views(labelled)
    pd.testing.assert_frame_equal(labelled, before)


def test_comparison_keeps_currencies_and_views_separate(labelled):
    table = compare_views(*build_prpo_views(labelled))
    amounts = table[table["metric"] == "po_item_amount_sum"].set_index("group")
    assert set(amounts.index) == {"IDR", "USD"}  # no cross-currency total exists
    assert amounts.loc["IDR", ORIGINAL] == 100 * 3 + 10 + 999
    assert amounts.loc["IDR", DISTINCT] == 100 + 10 + 999
    assert amounts.loc["USD", ORIGINAL] == 100.0
    assert amounts.loc["USD", DISTINCT] == 50.0
    assert amounts.loc["USD", "ratio_original_to_distinct"] == 2.0
    assert table.loc[table["metric"] == "promised_interval_days_median", ORIGINAL].iloc[0] == 20


def test_comparison_uses_requested_and_promised_names_only(labelled):
    metrics = set(compare_views(*build_prpo_views(labelled))["metric"])
    assert not {m for m in metrics if "actual" in m or "lead_time" in m}
