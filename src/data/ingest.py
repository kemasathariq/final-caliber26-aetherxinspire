"""Workbook ingestion: read, type, add lineage and store staged tables.

Rules enforced here:
  - Workbooks are opened read-only and never written.
  - Every source row is kept. Nothing is deduplicated, imputed or trimmed.
  - Types come from the schema. pandas type inference is switched off, because
    default ``read_excel`` turns text identifiers into int64 or float64.
  - Only truly empty cells become null. Text such as "NA" stays text.

Known pandas behaviour: an Excel error cell such as #N/A is read as null. The
storage check (TYP-01) and cell cross-check (ROW-03) expose this if it occurs.
The six supplied workbooks contain no error cells.
"""
import hashlib
import logging
from pathlib import Path

import pandas as pd

from src.config import SPEC_VERSION
from src.data.schemas import DATASETS, LINEAGE_COLUMNS, DatasetSpec

log = logging.getLogger(__name__)

_SEPARATOR = "\x1f"


class SourceDataError(RuntimeError):
    """The source file does not match its schema, so it cannot be safely read."""


def read_source_table(spec: DatasetSpec, path: Path) -> pd.DataFrame:
    """Read one worksheet with no type inference, using source column names."""
    if not Path(path).is_file():
        raise SourceDataError(f"{spec.name}: workbook not found at {path}")
    try:
        frame = pd.read_excel(path, sheet_name=spec.sheet, engine="openpyxl", dtype=object,
                              keep_default_na=False, na_values=[""])
    except ValueError as error:
        raise SourceDataError(f"{spec.name}: cannot read sheet {spec.sheet!r}: {error}") from error
    if list(frame.columns) != spec.source_columns:
        raise SourceDataError(
            f"{spec.name}: columns differ from schema. "
            f"Expected {spec.source_columns}, found {list(frame.columns)}")
    return frame


def _require_cell_types(values: pd.Series, allowed: tuple, label: str) -> None:
    present = values.dropna()
    wrong = present[[not isinstance(v, allowed) for v in present]]
    if len(wrong):
        raise SourceDataError(
            f"{label}: {len(wrong)} cells have an unexpected type, "
            f"for example {wrong.iloc[0]!r} ({type(wrong.iloc[0]).__name__})")


def _to_typed(values: pd.Series, kind: str, label: str) -> pd.Series:
    if kind in ("identifier", "text", "category"):
        _require_cell_types(values, (str,), label)
        typed = values.astype("string")
        return typed.astype("category") if kind == "category" else typed
    if kind in ("integer", "float"):
        _require_cell_types(values, (int, float), label)
        numeric = pd.to_numeric(values)
        try:
            return numeric.astype("Int64" if kind == "integer" else "Float64")
        except (TypeError, ValueError) as error:
            raise SourceDataError(f"{label}: not whole numbers: {error}") from error
    if kind == "date":
        present = values.dropna()
        if len(present) and not all(hasattr(v, "year") for v in present):
            raise SourceDataError(f"{label}: contains cells that are not dates")
        return pd.to_datetime(values).astype("datetime64[ns]")
    raise ValueError(f"Unknown column kind: {kind}")


def _canonical_text(values: pd.Series, kind: str) -> list[str]:
    """Stable text form of a typed column, used for hashing. Null becomes empty."""
    if kind == "date":
        text = values.dt.strftime("%Y-%m-%dT%H:%M:%S")
    elif kind == "integer":
        text = values.astype("string")
    elif kind == "float":
        return ["" if pd.isna(v) else repr(float(v)) for v in values]
    else:
        text = values.astype("string")
    return text.fillna("").tolist()


def compute_row_hashes(frame: pd.DataFrame, spec: DatasetSpec) -> list[str]:
    """SHA-256 of all source cell values in source column order."""
    parts = [_canonical_text(frame[c.standard], c.kind) for c in spec.columns]
    return [hashlib.sha256(_SEPARATOR.join(row).encode("utf-8")).hexdigest() for row in zip(*parts)]


def stage_table(source: pd.DataFrame, spec: DatasetSpec) -> pd.DataFrame:
    """Apply schema types and standard names, and add lineage. Row count is unchanged."""
    staged = pd.DataFrame(index=source.index)
    for column in spec.columns:
        label = f"{spec.name}.{column.source}"
        staged[column.standard] = _to_typed(source[column.source], column.kind, label)
    staged["source_file"] = pd.array([spec.file_name] * len(staged), dtype="string")
    staged["source_sheet"] = pd.array([spec.sheet] * len(staged), dtype="string")
    # read_excel index 0 is the first row under the header, which is Excel row 2.
    staged["source_row"] = pd.array(source.index + 2, dtype="Int64")
    staged["row_hash"] = pd.array(compute_row_hashes(staged, spec), dtype="string")
    staged["spec_version"] = pd.array([SPEC_VERSION] * len(staged), dtype="string")
    if len(staged) != len(source):
        raise SourceDataError(f"{spec.name}: staging changed the row count")
    return staged.reset_index(drop=True)


def ingest_dataset(spec: DatasetSpec, raw_dir: Path) -> pd.DataFrame:
    table = stage_table(read_source_table(spec, Path(raw_dir) / spec.file_name), spec)
    log.info("Ingested %s: %d rows, %d source columns", spec.name, len(table), len(spec.columns))
    return table


def ingest_all(raw_dir: Path) -> dict[str, pd.DataFrame]:
    return {key: ingest_dataset(spec, raw_dir) for key, spec in DATASETS.items()}


def write_csv(frame: pd.DataFrame, path: Path) -> None:
    """Write a table deterministically: UTF-8, LF line ends, ISO dates, empty for null."""
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=False, encoding="utf-8", lineterminator="\n",
                 date_format="%Y-%m-%d", na_rep="")


def _staged_dtypes(spec: DatasetSpec) -> tuple[dict[str, str], list[str]]:
    mapping = {"identifier": "string", "text": "string", "category": "string",
               "integer": "Int64", "float": "Float64"}
    dtypes = {c.standard: mapping[c.kind] for c in spec.columns if c.kind != "date"}
    dtypes.update({"source_file": "string", "source_sheet": "string", "source_row": "Int64",
                   "row_hash": "string", "spec_version": "string"})
    return dtypes, spec.by_kind("date")


def read_staged(spec: DatasetSpec, path: Path) -> pd.DataFrame:
    """Read a staged CSV back with schema types.

    This is the only supported way to load staged tables. A plain ``read_csv``
    would turn identifiers into numbers.
    """
    dtypes, dates = _staged_dtypes(spec)
    frame = pd.read_csv(path, dtype=dtypes, keep_default_na=False, na_values=[""],
                        parse_dates=dates, encoding="utf-8")
    for column in dates:
        frame[column] = frame[column].astype("datetime64[ns]")
    for column in spec.by_kind("category"):
        frame[column] = frame[column].astype("category")
    expected = spec.standard_columns + list(LINEAGE_COLUMNS)
    if list(frame.columns) != expected:
        raise SourceDataError(f"{spec.name}: staged columns differ from schema")
    return frame
