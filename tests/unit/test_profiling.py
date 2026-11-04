"""Profiling logic on hand-checkable data."""
import pandas as pd

from src.data import profiling
from src.data.schemas import ColumnSpec, DATASETS, DatasetSpec, FUNCLOC

KEY_SPEC = DatasetSpec("k", "K", "k.xlsx", "Data", (
    ColumnSpec("A", "a", "identifier"), ColumnSpec("B", "b", "identifier"), ColumnSpec("D", "d", "date")), "")


def key_table(a, b, d, hashes=None):
    frame = pd.DataFrame({"a": pd.array(a, dtype="string"), "b": pd.array(b, dtype="string"), "d": pd.to_datetime(d)})
    frame["row_hash"] = hashes or [f"{x}|{y}|{z}" for x, y, z in zip(a, b, d)]
    return frame


def assessment(frame, columns, **kwargs):
    table = profiling.candidate_primary_keys(frame, KEY_SPEC, **kwargs)
    return table.set_index("columns").loc[columns, "assessment"]


def test_unique_column_is_found():
    frame = key_table(["1", "2"], ["x", "x"], ["2026-01-01", "2026-01-01"])
    assert assessment(frame, "a") == "unique_on_all_rows"
    assert assessment(frame, "b") == "not_unique"


def test_key_unique_only_after_exact_copies_is_labelled():
    frame = key_table(["1", "1", "2"], ["x", "x", "x"], ["2026-01-01"] * 3)
    assert assessment(frame, "a") == "unique_only_after_setting_aside_exact_copies"
    assert assessment(frame, "(all source columns)") == "no_natural_key_possible_on_all_rows"


def test_same_key_with_different_content_is_not_unique():
    frame = key_table(["1", "1"], ["x", "y"], ["2026-01-01"] * 2)
    assert assessment(frame, "a") == "not_unique"


def test_column_with_nulls_cannot_be_a_key():
    frame = key_table(["1", None], ["x", "y"], ["2026-01-01"] * 2, hashes=["p", "q"])
    assert assessment(frame, "a") == "not_a_key_contains_nulls"


def test_date_combination_is_marked_coincidental():
    frame = key_table(["1", "1", "2"], ["x", "x", "x"], ["2026-01-01", "2026-01-02", "2026-01-01"])
    assert assessment(frame, "a + d") == "coincidental_unique_includes_date"


def test_documented_composite_key_is_always_reported():
    frame = key_table(["1", "1", "2"], ["x", "x", "y"], ["2026-01-01", "2026-01-02", "2026-01-01"])
    assert assessment(frame, "a + b", documented_keys=(("a", "b"),)) == "not_unique"


def minimal_tables(**overrides):
    tables = {}
    for key, spec in DATASETS.items():
        tables[key] = pd.DataFrame({c: pd.array([], dtype="string") for c in spec.by_kind("identifier")})
    for name, values in overrides.items():
        key, column = name.split("__")
        tables[key] = pd.DataFrame({column: pd.array(values, dtype="string")})
        for other in DATASETS[key].by_kind("identifier"):
            if other != column:
                tables[key][other] = pd.array([None] * len(values), dtype="string")
    return tables


def test_foreign_key_cardinality_coverage_and_join_size():
    tables = minimal_tables(funcloc__functional_location=["L1", "L2", "L3"],
                            bom__functional_location=["L1", "L1", "L2"])
    row = profiling.candidate_foreign_keys(tables).iloc[0]
    assert row["column_a"] == "bom.functional_location" and row["column_b"] == "funcloc.functional_location"
    assert row["observed_cardinality_a_to_b"] == "N:1"
    assert row["coverage_of_a_pct"] == 100.0 and row["coverage_of_b_pct"] == 66.67
    assert row["raw_inner_join_rows"] == 3
    assert row["diagram_relation"] == "1:N"
    assert row["assessment"] == "candidate_foreign_key_one_side_fully_contained"


def test_many_to_many_row_multiplication_is_measured():
    tables = minimal_tables(bom__material_no=["M1", "M1", "M1"], movement__material_no=["M1", "M1"])
    row = profiling.candidate_foreign_keys(tables).iloc[0]
    assert row["observed_cardinality_a_to_b"] == "N:N" and row["raw_inner_join_rows"] == 6


def test_coincidental_value_overlap_is_not_called_a_foreign_key():
    tables = minimal_tables(prpo__purchase_order=["4300000001"], bom__material_no=["4300000001"])
    row = profiling.candidate_foreign_keys(tables).iloc[0]
    assert row["assessment"] == "value_overlap_only_not_supported_by_name_or_diagram"


def test_numeric_summary_never_crosses_currency_or_unit():
    view = pd.DataFrame({"currency": pd.Categorical(["IDR", "USD"]), "unit": pd.Categorical(["EA", "KG"]),
                         "po_item_amount": pd.array([1000.0, 5.0], dtype="Float64"), "pr_quantity": pd.array([1, 2], dtype="Int64")})
    empty = {k: pd.DataFrame(columns=["unit", "quantity", "installed_qty", "min_qty", "max_qty", "stock", "material_no"]).astype({"unit": "category"}) for k in ("movement", "bom")}
    views = {"prpo": {"original_rows": view}, "movement": {"all_rows": empty["movement"]}, "bom": {"all_rows": empty["bom"]}}
    table = profiling.numeric_summary(views)
    amounts = table[table["column"] == "po_item_amount"].set_index("group")
    assert set(amounts.index) == {"IDR", "USD"}
    assert amounts.loc["IDR", "max"] == 1000 and amounts.loc["USD", "max"] == 5
    assert set(table["view"]) == {"original_rows"}
