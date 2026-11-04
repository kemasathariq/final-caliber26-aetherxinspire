"""Source file checks: checksums, the source manifest and the cell-level cross-check."""
import hashlib
import json
from pathlib import Path

import pandas as pd

from src.config import AUDIT_BASELINE_FILE, BASELINE_NOTE, BOM_RELOCATION_FILE, PROJECT_ROOT
from src.data.schemas import DATASETS, DatasetSpec
from src.data.workbook_inspect import sheet_header

_EXCEL_EPOCH = pd.Timestamp("1899-12-30")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_audit_baseline() -> dict[str, str]:
    return json.loads(AUDIT_BASELINE_FILE.read_text(encoding="utf-8"))["sha256_by_file"]


def checksum_status(path: Path, baseline: dict[str, str]) -> dict:
    """Compare one file with the audit baseline."""
    if not path.is_file():
        return {"exists": False, "sha256": None, "status": "missing"}
    observed = sha256_file(path)
    expected = baseline.get(path.name)
    status = "consistent_with_audit_baseline" if observed == expected else "checksum_mismatch"
    return {"exists": True, "sha256": observed, "status": status}


def _relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(PROJECT_ROOT).as_posix()
    except ValueError:
        return path.name  # fixture files in tests live outside the project


def build_source_manifest(raw_dir: Path, inspections: dict[str, dict]) -> dict:
    """Describe each source file. The manifest holds counts and hashes, no records."""
    baseline = load_audit_baseline()
    entries = []
    for key, spec in DATASETS.items():
        path = Path(raw_dir) / spec.file_name
        check = checksum_status(path, baseline)
        sheets = inspections[key]["sheets"]
        main = sheets.get(spec.sheet)
        header = sheet_header(main) if main else []
        entries.append({
            "dataset": spec.name,
            "dataset_key": key,
            "file_name": spec.file_name,
            "relative_path": _relative(path),
            "sha256": check["sha256"],
            "audit_baseline_sha256": baseline.get(spec.file_name),
            "file_size_bytes": path.stat().st_size if path.is_file() else None,
            "worksheets": list(sheets),
            "data_rows": len(main["rows"]) - 1 if main else None,
            "columns": len(header),
            "verification_status": check["status"],
        })
    return {
        "note": BASELINE_NOTE,
        "bom_relocation_record": _relative(BOM_RELOCATION_FILE),
        "files": entries,
    }


def compare_cells_with_workbook(table: pd.DataFrame, spec: DatasetSpec, sheet: dict) -> dict[str, int]:
    """Compare every staged cell with the workbook XML. Returns mismatches per column.

    Text must match exactly, including spaces. Numbers must be equal. Dates must
    equal the Excel day serial. Blank cells must be null and nothing else may be.
    """
    data_rows = sheet["rows"][1:]
    mismatches = {}
    row_numbers = table["source_row"].astype("int64").tolist()
    if row_numbers != [number for number, _ in data_rows]:
        return {"source_row": len(data_rows)}
    for index, column in enumerate(spec.columns):
        staged = table[column.standard]
        nulls = staged.isna().tolist()
        if column.kind == "date":
            serials = ((staged - _EXCEL_EPOCH) / pd.Timedelta(days=1)).tolist()
            values = serials
        elif column.kind in ("integer", "float"):
            values = [None if n else float(v) for v, n in zip(staged, nulls)]
        else:
            values = staged.astype("string").tolist()
        bad = 0
        for (_, cells), value, is_null in zip(data_rows, values, nulls):
            cell = cells.get(index)
            if cell is None:
                bad += 0 if is_null else 1
            elif is_null:
                bad += 1
            elif column.kind in ("date", "integer", "float"):
                bad += 0 if float(cell[0]) == value else 1
            else:
                bad += 0 if cell[0] == value else 1
        if bad:
            mismatches[column.standard] = bad
    return mismatches
