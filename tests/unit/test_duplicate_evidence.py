"""Duplicate evidence logic on constructed data, where the right answer is known in advance."""
import numpy as np
import pandas as pd
import pytest

from src.validation.duplicate_evidence import document_permutation_test, holm_adjust, movement_sensitivity, same_copy_share
from src.validation.duplicates import add_duplicate_columns
from src.validation.exceptions import repeated_maximum_values


def test_same_copy_share_by_hand():
    keys = pd.Series(["a", "a", "b", "b", "c", "c"])
    copies = pd.Series([2, 2, 1, 3, 4, 4])
    assert same_copy_share(keys, copies) == pytest.approx(2 / 3)


def _documents(copy_for_line, documents=300):
    rng = np.random.default_rng(1)
    rows = []
    for doc in range(documents):
        document_copy = int(rng.integers(1, 5))
        for line in range(3):
            rows.append({"doc": f"D{doc}", "occurrence_count": copy_for_line(rng, document_copy)})
    return pd.DataFrame(rows)


def test_permutation_detects_document_level_repetition():
    """Lines inherit their document's copy count, as a document-level repeat would produce."""
    result = document_permutation_test(_documents(lambda rng, doc: doc), "doc", np.random.default_rng(42), rounds=50)
    assert result["observed_same_copy_share"] == 1.0
    assert result["shuffled_max"] < 0.2
    assert result["p_observed_at_or_above_shuffled"] == pytest.approx(1 / 51, abs=1e-3)


def test_permutation_does_not_detect_it_when_copies_are_row_level():
    result = document_permutation_test(_documents(lambda rng, doc: int(rng.integers(1, 5))), "doc", np.random.default_rng(42), rounds=50)
    assert result["shuffled_min"] <= result["observed_same_copy_share"] <= result["shuffled_max"]
    assert result["p_observed_at_or_above_shuffled"] > 0.05


def test_permutation_ignores_single_line_documents():
    table = pd.DataFrame({"doc": ["a", "a", "b"], "occurrence_count": [2, 2, 5]})
    assert document_permutation_test(table, "doc", np.random.default_rng(1), rounds=3)["documents_with_multiple_lines"] == 1


def test_holm_correction_by_hand():
    # Sorted 0.01, 0.02, 0.5: multiply by 3, 2, 1 and keep the running maximum.
    adjusted = holm_adjust(pd.Series([0.5, 0.01, 0.02], index=["c", "a", "b"]))
    assert adjusted.to_dict() == {"c": 0.5, "a": 0.03, "b": 0.04}
    # 0.9 x 2 caps at 1.0, and the running maximum keeps the second at 1.0 too.
    assert holm_adjust(pd.Series([0.9, 0.9])).tolist() == [1.0, 1.0]


@pytest.mark.filterwarnings("ignore::scipy.stats.ConstantInputWarning")
def test_movement_sensitivity_by_hand():
    table = pd.DataFrame({
        "posting_date": pd.to_datetime(["2026-01-01", "2026-01-01", "2026-02-01"]), "material_no": ["M1", "M1", "M2"], "order_no": ["O1", "O1", "O2"],
        "quantity": pd.array([3, 3, 5], dtype="Int64"), "unit": pd.Categorical(["EA", "EA", "KG"]), "row_hash": ["h1", "h1", "h2"], "source_row": pd.array([2, 3, 4], dtype="Int64")})
    frame = movement_sensitivity(add_duplicate_columns(table, "M"))
    get = lambda metric, group="": frame[(frame["metric"] == metric) & (frame["group"] == group)].iloc[0]
    assert get("issue_lines")["all_rows"] == 3 and get("issue_lines")["exact_distinct_rows"] == 2
    assert get("quantity_sum_within_unit", "EA")["all_rows"] == 6 and get("quantity_sum_within_unit", "EA")["exact_distinct_rows"] == 3
    assert get("quantity_sum_within_unit", "KG")["change_pct"] == 0
    assert get("materials_with_any_line_removed_in_distinct_view", "per material")["value"] == 1
    assert get("max_quantity_change_pct_within_a_material", "per material")["value"] == 50
    assert get("issue_lines_in_month", "2026-01")["change_pct"] == -50


def test_repeated_maximum_counts_materials_and_ignores_exact_copies():
    prpo = pd.DataFrame({"in_exact_distinct_rows": [True, True, False], "material_no": ["A", "B", "A"], "unit": pd.Categorical(["EA"] * 3), "pr_quantity": pd.array([9, 9, 9], dtype="Int64"),
                         "requested_interval_days": pd.array([1, 2, 2], dtype="Int64"), "promised_interval_days": pd.array([5, 5, 5], dtype="Int64")})
    issue = pd.DataFrame({"in_exact_distinct_rows": [True, True, False, True], "material_no": ["A", "B", "B", "C"], "unit": pd.Categorical(["KG"] * 4), "quantity": pd.array([7, 7, 7, 3], dtype="Int64")})
    bridge = pd.DataFrame({"material_no": ["A"], "unit": pd.Categorical(["EA"]), "installed_qty": pd.array([1.0], dtype="Float64")})
    dim = pd.DataFrame({"material_no": ["A"], "unit": pd.Categorical(["EA"]), "stock": pd.array([1.0], dtype="Float64"), "max_qty": pd.array([1], dtype="Int64")})
    notif = pd.DataFrame({"days_to_complete": pd.array([None, 4], dtype="Int64")})
    frame = repeated_maximum_values({"fact_prpo_line": prpo, "fact_issue": issue, "bridge_fl_material": bridge, "dim_material": dim, "fact_notification": notif})
    movement = frame[frame["measure"] == "Movement quantity"].iloc[0]
    assert movement["maximum"] == 7 and movement["rows_at_maximum"] == 2 and movement["materials_at_maximum"] == 2 and movement["next_highest_value"] == 3
    quantity = frame[frame["measure"] == "PR-Quantity"].iloc[0]
    assert quantity["rows_at_maximum"] == 2 and pd.isna(quantity["next_highest_value"])
