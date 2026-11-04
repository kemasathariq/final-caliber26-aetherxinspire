"""Read-only inspection of .xlsx files using the standard library.

An .xlsx file is a zip of XML parts. Reading those parts directly gives a view
of the workbook that is independent of pandas and openpyxl: how each cell is
physically stored, and structure such as hidden rows or formulas. The pipeline
uses it to cross-check every cell returned by ``pandas.read_excel``.
"""
import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

_NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
       "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}
_M = "{%s}" % _NS["m"]
_R_ID = "{%s}id" % _NS["r"]


def _column_index(cell_ref: str) -> int:
    index = 0
    for char in re.match(r"[A-Z]+", cell_ref).group():
        index = index * 26 + ord(char) - 64
    return index - 1


def _shared_strings(archive: zipfile.ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in archive.namelist():
        return []
    root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
    return ["".join(t.text or "" for t in si.iter(_M + "t")) for si in root]


def _document_properties(archive: zipfile.ZipFile) -> dict[str, str]:
    properties = {}
    for part in ("docProps/core.xml", "docProps/app.xml"):
        if part in archive.namelist():
            for element in ET.fromstring(archive.read(part)):
                if element.text and element.text.strip():
                    properties[element.tag.split("}")[1]] = element.text.strip()
    return properties


def _read_sheet(archive: zipfile.ZipFile, target: str, shared: list[str]) -> dict:
    root = ET.fromstring(archive.read(target))
    rows, hidden_rows, formula_cells = [], 0, 0
    for row in root.find("m:sheetData", _NS):
        if row.attrib.get("hidden") in ("1", "true"):
            hidden_rows += 1
        cells = {}
        for cell in row:
            cell_type = cell.attrib.get("t", "n")
            value = cell.find("m:v", _NS)
            if cell.find("m:f", _NS) is not None:
                formula_cells += 1
            if cell_type == "inlineStr":
                text = "".join(t.text or "" for t in cell.iter(_M + "t"))
            elif value is None:
                continue
            elif cell_type == "s":
                text = shared[int(value.text)]
            else:
                text = value.text
            cells[_column_index(cell.attrib["r"])] = (text, cell_type)
        rows.append((int(row.attrib["r"]), cells))
    dimension = root.find("m:dimension", _NS)
    numbers = [number for number, _ in rows]
    return {
        "rows": rows,
        "dimension": dimension.attrib.get("ref") if dimension is not None else None,
        "row_gaps": sum(1 for a, b in zip(numbers, numbers[1:]) if b != a + 1),
        "hidden_rows": hidden_rows,
        "hidden_columns": sum(1 for c in root.iter(_M + "col")
                              if c.attrib.get("hidden") in ("1", "true")),
        "formula_cells": formula_cells,
        "merged_ranges": sum(1 for _ in root.iter(_M + "mergeCell")),
        "has_autofilter": root.find("m:autoFilter", _NS) is not None,
        "table_parts": sum(1 for _ in root.iter(_M + "tablePart")),
    }


def inspect_workbook(path: Path) -> dict:
    """Return workbook structure and all cell text, without pandas or openpyxl."""
    with zipfile.ZipFile(path, "r") as archive:
        workbook = ET.fromstring(archive.read("xl/workbook.xml"))
        rels = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
        targets = {r.attrib["Id"]: r.attrib["Target"] for r in rels}
        shared = _shared_strings(archive)
        properties = workbook.find("m:workbookPr", _NS)
        result = {
            "date1904": properties is not None and properties.attrib.get("date1904") in ("1", "true"),
            "document_properties": _document_properties(archive),
            "external_links": sum("externalLink" in n for n in archive.namelist()),
            "sheets": {},
        }
        for sheet in workbook.find("m:sheets", _NS):
            target = targets[sheet.attrib[_R_ID]].lstrip("/")
            target = target if target.startswith("xl/") else "xl/" + target
            info = _read_sheet(archive, target, shared)
            info["state"] = sheet.attrib.get("state", "visible")
            result["sheets"][sheet.attrib["name"]] = info
    return result


def sheet_header(sheet: dict) -> list[str]:
    """Return header text from the first row of an inspected sheet."""
    _, cells = sheet["rows"][0]
    return [cells[i][0] if i in cells else "" for i in range(max(cells) + 1)] if cells else []


def storage_types_by_column(sheet: dict) -> dict[str, dict[str, int]]:
    """Count physical cell storage per column, keyed by header text."""
    header = sheet_header(sheet)
    counts: dict[str, dict[str, int]] = {name: {} for name in header}
    for _, cells in sheet["rows"][1:]:
        for index, name in enumerate(header):
            cell_type = cells[index][1] if index in cells else "blank"
            counts[name][cell_type] = counts[name].get(cell_type, 0) + 1
    return counts
