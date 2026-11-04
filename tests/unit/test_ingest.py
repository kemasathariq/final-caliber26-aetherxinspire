"""Ingestion logic on small hand-checkable workbooks."""
import datetime as dt

import pandas as pd
import pytest

from src.data.ingest import (SourceDataError, compute_row_hashes, read_source_table, read_staged,
                             stage_table, write_csv)
from src.data.schemas import ColumnSpec, DatasetSpec, LINEAGE_COLUMNS
from src.data.workbook_inspect import inspect_workbook, storage_types_by_column
from src.validation.source_checks import compare_cells_with_workbook

DAY = dt.datetime(2026, 1, 15)
ROW = ["0012345678", "note", "A", 3, 1.5, DAY]


def _staged(spec, path):
    return stage_table(read_source_table(spec, path), spec)


def test_leading_zeros_are_preserved(sample_spec, make_workbook):
    table = _staged(sample_spec, make_workbook([ROW]))
    assert table.loc[0, "doc_no"] == "0012345678"


def test_default_read_excel_would_damage_identifiers(sample_spec, make_workbook):
    """Documents why inference is off: default read_excel turns this text into a number."""
    path = make_workbook([ROW])
    assert pd.read_excel(path)["Doc No"].iloc[0] == 12345678
    assert read_source_table(sample_spec, path)["Doc No"].iloc[0] == "0012345678"


@pytest.mark.parametrize("text", ["NA", "N/A", "null", "None", "nan"])
def test_text_that_looks_null_stays_text(sample_spec, make_workbook, text):
    row = ["0012345678", text, "A", 3, 1.5, DAY]
    assert _staged(sample_spec, make_workbook([row])).loc[0, "note"] == text


def test_excel_error_cell_is_caught_by_the_independent_checks(sample_spec, make_workbook):
    """pandas reads an Excel error cell such as #N/A as null, silently.

    The XML cross-check and the storage check must both expose that. The real
    workbooks contain no error cells.
    """
    path = make_workbook([["0012345678", "#N/A", "A", 3, 1.5, DAY]])
    table = _staged(sample_spec, path)
    assert pd.isna(table.loc[0, "note"])
    sheet = inspect_workbook(path)["sheets"]["Data"]
    assert compare_cells_with_workbook(table, sample_spec, sheet) == {"note": 1}
    assert "e" in storage_types_by_column(sheet)["Note"]


def test_blank_cells_become_null_and_are_not_imputed(sample_spec, make_workbook):
    table = _staged(sample_spec, make_workbook([["0012345678", None, None, None, None, None]]))
    assert table[["note", "code", "qty", "amount", "doc_date"]].isna().all(axis=None)


def test_surrounding_spaces_are_kept_verbatim(sample_spec, make_workbook):
    row = ["0012345678", "  padded text ", "A", 3, 1.5, DAY]
    assert _staged(sample_spec, make_workbook([row])).loc[0, "note"] == "  padded text "


def test_source_row_is_the_excel_row_number(sample_spec, make_workbook):
    table = _staged(sample_spec, make_workbook([ROW, ROW, ROW]))
    assert table["source_row"].tolist() == [2, 3, 4]


def test_duplicate_rows_are_not_dropped(sample_spec, make_workbook):
    assert len(_staged(sample_spec, make_workbook([ROW] * 5))) == 5


def test_lineage_columns_are_added(sample_spec, make_workbook):
    table = _staged(sample_spec, make_workbook([ROW]))
    assert set(LINEAGE_COLUMNS) <= set(table.columns)
    assert table.loc[0, "source_file"] == "sample.xlsx"
    assert table.loc[0, "source_sheet"] == "Data"


def test_schema_types_are_applied(sample_spec, make_workbook):
    table = _staged(sample_spec, make_workbook([ROW]))
    assert table["doc_no"].dtype == "string"
    assert table["code"].dtype == "category" and not table["code"].cat.ordered
    assert table["qty"].dtype == "Int64"
    assert table["amount"].dtype == "Float64"
    assert table["doc_date"].dtype == "datetime64[ns]"


def test_missing_file_is_reported(sample_spec, tmp_path):
    with pytest.raises(SourceDataError, match="not found"):
        read_source_table(sample_spec, tmp_path / "absent.xlsx")


def test_missing_sheet_is_reported(sample_spec, make_workbook):
    with pytest.raises(SourceDataError, match="cannot read sheet"):
        read_source_table(sample_spec, make_workbook([ROW], sheet="Other"))


def test_changed_columns_are_reported(sample_spec, make_workbook):
    headers = list(sample_spec.source_columns)
    headers[1] = "Renamed"
    with pytest.raises(SourceDataError, match="columns differ"):
        read_source_table(sample_spec, make_workbook([ROW], headers=headers))


def test_numeric_identifier_cell_is_rejected_not_coerced(sample_spec, make_workbook):
    row = [12345678, "note", "A", 3, 1.5, DAY]
    with pytest.raises(SourceDataError, match="unexpected type"):
        _staged(sample_spec, make_workbook([row]))


def test_fraction_in_integer_column_is_rejected_not_rounded(sample_spec, make_workbook):
    row = ["0012345678", "note", "A", 3.5, 1.5, DAY]
    with pytest.raises(SourceDataError, match="not whole numbers"):
        _staged(sample_spec, make_workbook([row]))


def test_text_in_date_column_is_rejected(sample_spec, make_workbook):
    row = ["0012345678", "note", "A", 3, 1.5, "not a date"]
    with pytest.raises(SourceDataError, match="not dates"):
        _staged(sample_spec, make_workbook([row]))


def test_row_hash_depends_on_every_cell(sample_spec, make_workbook):
    other = ["0012345678", "note", "A", 3, 1.6, DAY]
    table = _staged(sample_spec, make_workbook([ROW, ROW, other]))
    assert table.loc[0, "row_hash"] == table.loc[1, "row_hash"]
    assert table.loc[0, "row_hash"] != table.loc[2, "row_hash"]


def test_row_hash_does_not_confuse_cell_boundaries():
    spec = DatasetSpec("x", "x", "x.xlsx", "Data", (ColumnSpec("A", "a", "text"), ColumnSpec("B", "b", "text")), "")
    frame = pd.DataFrame({"a": pd.array(["ab", "a"], dtype="string"), "b": pd.array(["c", "bc"], dtype="string")})
    first, second = compute_row_hashes(frame, spec)
    assert first != second


def test_csv_round_trip_preserves_values(sample_spec, make_workbook, tmp_path):
    rows = [["0012345678", "  NA ", "A", 3, 1.5, DAY],
            ["0000000001", None, None, None, None, None],
            ["0012345679", 'with "quotes", commas\nand a line break', "B", 7, 36.91, DAY]]
    table = _staged(sample_spec, make_workbook(rows))
    path = tmp_path / "stg.csv"
    write_csv(table, path)
    back = read_staged(sample_spec, path)
    assert back["doc_no"].tolist() == ["0012345678", "0000000001", "0012345679"]
    assert back.loc[0, "note"] == "  NA "
    assert pd.isna(back.loc[1, "note"]) and pd.isna(back.loc[1, "qty"]) and pd.isna(back.loc[1, "doc_date"])
    assert back.loc[2, "note"] == 'with "quotes", commas\nand a line break'
    assert back.loc[2, "amount"] == 36.91
    assert back["row_hash"].tolist() == table["row_hash"].tolist()
