"""Outlier and join logic on small data with hand-calculated answers."""
import pandas as pd
import pytest

from src.preprocessing.joins import JoinAuditError, audited_lookup, join_row_count, observed_cardinality
from src.preprocessing.outliers import IQR_FENCE, NOT_ASSESSED, ROBUST_Z, robust_outlier_flags


def _flags(values, groups=None, fallback=None):
    series = pd.Series(values, dtype="Float64")
    group = pd.Series(groups if groups else ["a"] * len(values))
    return robust_outlier_flags(series, group, pd.Series(fallback) if fallback else None)


def test_robust_z_matches_a_hand_calculation():
    # Median 11, deviations 1, 1, 0, 1, 89, so MAD is 1. z for 100 = 0.6745 x 89 = 60.0305.
    result = _flags([10, 10, 11, 12, 100])
    assert result["method"].tolist() == [ROBUST_Z] * 5
    assert result["flag"].tolist() == [False, False, False, False, True]
    assert result["score"].iloc[4] == pytest.approx(60.0305)


def test_threshold_is_strictly_above_3_5():
    # Sorted 8, 8, 10, 10, 12, 12, x: median 10, MAD 2. z for 20 = 3.3725 (kept); for 21 = 3.70975 (flagged).
    assert _flags([8, 8, 10, 10, 12, 12, 20])["flag"].iloc[6] == False  # noqa: E712
    assert _flags([8, 8, 10, 10, 12, 12, 21])["flag"].iloc[6] == True  # noqa: E712


def test_blank_values_stay_blank_and_are_not_flagged():
    result = _flags([10, 10, 11, 12, 100, None])
    assert pd.isna(result["flag"].iloc[5]) and pd.isna(result["method"].iloc[5])


def test_small_group_falls_back_to_the_iqr_fence_of_the_wider_group():
    # Wider group 1 to 8 and 100. Q1 = 3, Q3 = 7, IQR = 4, fence = 7 + 3 x 4 = 19.
    values = [1, 2, 3, 4, 5, 6, 7, 8, 100]
    groups = [f"g{i}" for i in range(9)]
    result = _flags(values, groups, ["unit"] * 9)
    assert set(result["method"]) == {IQR_FENCE}
    assert result["flag"].tolist() == [False] * 8 + [True]
    assert result["score"].iloc[8] == pytest.approx((100 - 7) / 4)


def test_zero_mad_also_uses_the_fence():
    assert _flags([5, 5, 5, 5, 5, 9, 1, 2], ["m"] * 6 + ["x", "y"], ["u"] * 8)["method"].iloc[0] == IQR_FENCE


def test_the_fence_is_upper_side_only():
    values = [-1000, 2, 3, 4, 5, 6, 7, 8, 9]
    assert not _flags(values, [f"g{i}" for i in range(9)], ["u"] * 9)["flag"].iloc[0]


def test_no_spread_is_reported_as_not_assessed_rather_than_flagged():
    result = _flags([1, 1, 1, 1, 1, 50], ["m"] * 6, ["u"] * 6)
    # MAD is 0 and the wider group's IQR is 0, so no threshold can be defined.
    assert set(result["method"]) == {NOT_ASSESSED}
    assert result["flag"].sum() == 0


def _left():
    return pd.DataFrame({"k": ["a", "b", "a", None], "x": [1, 2, 3, 4]}).astype({"k": "string"})


def test_lookup_keeps_rows_and_order_and_records_counts():
    audit = []
    right = pd.DataFrame({"k": ["a", "b"], "y": [10, 20]}).astype({"k": "string"})
    merged = audited_lookup(_left(), right, "k", "demo", audit)
    assert merged["x"].tolist() == [1, 2, 3, 4]
    assert merged["y"].tolist()[:3] == [10, 20, 10]
    assert audit[0] == {"join": "demo", "keys": "k", "left_rows": 4, "right_rows": 2, "result_rows": 4, "matched_rows": 3, "unmatched_rows": 0, "left_rows_with_blank_key": 1}


def test_repeated_right_key_stops_the_join_before_it_multiplies_rows():
    right = pd.DataFrame({"k": ["a", "a"], "y": [1, 2]}).astype({"k": "string"})
    with pytest.raises(JoinAuditError, match="not unique"):
        audited_lookup(_left(), right, "k", "demo")


def test_colliding_columns_stop_the_join():
    right = pd.DataFrame({"k": ["a"], "x": [9]}).astype({"k": "string"})
    with pytest.raises(JoinAuditError, match="collide"):
        audited_lookup(_left(), right, "k", "demo")


def test_missing_parent_stops_a_join_that_requires_one():
    right = pd.DataFrame({"k": ["a"], "y": [1]}).astype({"k": "string"})
    with pytest.raises(JoinAuditError, match="no parent"):
        audited_lookup(_left(), right, "k", "demo", require_all_matched=True)


def test_blank_keys_never_match_a_blank_parent():
    audit = []
    right = pd.DataFrame({"k": ["a", None], "y": [1, 99]}).astype({"k": "string"})
    audited_lookup(_left(), right, "k", "demo", audit)
    assert audit[0]["matched_rows"] == 2 and audit[0]["left_rows_with_blank_key"] == 1


def test_join_row_count_and_cardinality_by_hand():
    left, right = pd.Series(["a", "a", "b", "c"]), pd.Series(["a", "a", "a", "b", None])
    assert join_row_count(left, right) == 2 * 3 + 1
    assert observed_cardinality(left, right) == "N:N"
    assert observed_cardinality(pd.Series(["a", "b"]), pd.Series(["a", "a"])) == "1:N"
    assert observed_cardinality(pd.Series(["a", "a"]), pd.Series(["a", "b"])) == "N:1"
    assert observed_cardinality(pd.Series(["a"]), pd.Series(["a"])) == "1:1"
    assert observed_cardinality(pd.Series(["a"]), pd.Series(["b"])) == "no shared keys"
