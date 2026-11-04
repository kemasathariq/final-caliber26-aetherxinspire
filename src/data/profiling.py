"""Dataset profiling. Describes the data as supplied and changes nothing.

Numeric summaries stay within a single unit or currency. PR PO results are
produced for both approved views and labelled with the view used.
"""
from itertools import combinations

import pandas as pd

from src.config import DATA_CUTOFF
from src.data.schemas import (BOM_MATERIAL_ATTRIBUTES, DATASETS, DIAGRAM_RELATIONS,
                              NUMERIC_GROUP_BY, DatasetSpec)
from src.data.workbook_inspect import storage_types_by_column

ALL_ROWS = "all_rows"
LOW_CARDINALITY = 30
# Frequency lists of these would be supplier or material rankings, which are out
# of scope for this phase. Their uniqueness is still profiled in the column profile.
NO_VALUE_LISTS = {"supplier_name", "supplier_code", "material_no", "material_desc"}


def workbook_inventory(inspections: dict[str, dict]) -> pd.DataFrame:
    rows = []
    for key, spec in DATASETS.items():
        inspection = inspections[key]
        for name, sheet in inspection["sheets"].items():
            properties = inspection["document_properties"]
            rows.append({
                "dataset": spec.name, "file_name": spec.file_name, "worksheet": name,
                "state": sheet["state"], "dimension": sheet["dimension"],
                "excel_rows": len(sheet["rows"]), "data_rows": len(sheet["rows"]) - 1,
                "row_number_gaps": sheet["row_gaps"], "hidden_rows": sheet["hidden_rows"],
                "hidden_columns": sheet["hidden_columns"], "formula_cells": sheet["formula_cells"],
                "merged_ranges": sheet["merged_ranges"], "has_autofilter": sheet["has_autofilter"],
                "table_parts": sheet["table_parts"], "external_links": inspection["external_links"],
                "date1904": inspection["date1904"], "creator": properties.get("creator"),
                "application": properties.get("Application"), "created_utc": properties.get("created"),
            })
    return pd.DataFrame(rows)


def column_profile(table: pd.DataFrame, spec: DatasetSpec, sheet: dict) -> pd.DataFrame:
    storage = storage_types_by_column(sheet)
    rows = []
    for position, column in enumerate(spec.columns, start=1):
        values = table[column.standard]
        present = values.dropna()
        row = {
            "dataset": spec.name, "position": position, "source_column": column.source,
            "standard_name": column.standard, "kind": column.kind,
            "xlsx_cell_storage": "; ".join(f"{k}={v}" for k, v in sorted(storage[column.source].items())),
            "pandas_dtype": str(values.dtype).split("(")[0], "rows": len(values),
            "non_null": len(present), "missing": int(values.isna().sum()),
            "missing_pct": round(100 * values.isna().mean(), 3),
            "unique_values": int(present.nunique()),
            "unique_pct_of_non_null": round(100 * present.nunique() / len(present), 3) if len(present) else 0.0,
        }
        if column.kind in ("identifier", "text", "category"):
            text = present.astype("string")
            lengths = text.str.len()
            row.update({
                "min_length": int(lengths.min()), "max_length": int(lengths.max()),
                "leading_trailing_space_rows": int((text != text.str.strip()).sum()),
                "empty_string_rows": int((text == "").sum()),
            })
        rows.append(row)
    return pd.DataFrame(rows)


def _numeric_stats(values: pd.Series) -> dict:
    present = values.dropna().astype("float64")
    return {
        "count": len(present), "missing": int(values.isna().sum()),
        "min": float(present.min()), "p25": float(present.quantile(.25)),
        "median": float(present.median()), "p75": float(present.quantile(.75)),
        "p95": float(present.quantile(.95)), "p99": float(present.quantile(.99)),
        "max": float(present.max()), "mean": round(float(present.mean()), 4),
        "std": round(float(present.std()), 4) if len(present) > 1 else None,
        "zero_count": int((present == 0).sum()), "negative_count": int((present < 0).sum()),
        "non_integer_count": int((present % 1 != 0).sum()),
    }


def numeric_summary(views: dict[str, dict[str, pd.DataFrame]]) -> pd.DataFrame:
    """Numeric statistics inside each unit or currency, labelled by view and grain."""
    rows = []
    for key, column_groups in NUMERIC_GROUP_BY.items():
        for view_name, table in views[key].items():
            grains = [("source_rows", table)]
            if key == "bom":
                grains.append(("one_row_per_material", table.drop_duplicates("material_no")))
            for grain, frame in grains:
                for column, group_by in column_groups.items():
                    if grain == "one_row_per_material" and column not in BOM_MATERIAL_ATTRIBUTES:
                        continue
                    for group, part in frame.groupby(group_by, observed=True):
                        rows.append({"dataset": DATASETS[key].name, "view": view_name, "grain": grain,
                                     "column": column, "group_field": group_by, "group": str(group),
                                     **_numeric_stats(part[column])})
    return pd.DataFrame(rows)


def categorical_distribution(views: dict[str, dict[str, pd.DataFrame]]) -> pd.DataFrame:
    """Value counts for category columns and other low-cardinality code columns."""
    rows = []
    for key, spec in DATASETS.items():
        for view_name, table in views[key].items():
            for column in spec.columns:
                values = table[column.standard]
                include = column.kind == "category" or (
                    column.kind in ("identifier", "text")
                    and column.standard not in NO_VALUE_LISTS
                    and values.nunique() <= LOW_CARDINALITY)
                if not include:
                    continue
                counts = values.astype("string").fillna("<NULL>").value_counts()
                # Sort by count then value, so ties always list in the same order.
                ordered = counts.rename("count").reset_index().sort_values(
                    ["count", column.standard], ascending=[False, True], kind="stable")
                for rank, (value, count) in enumerate(zip(ordered[column.standard], ordered["count"]), start=1):
                    rows.append({"dataset": spec.name, "view": view_name, "column": column.standard,
                                 "rank": rank, "value": value, "count": int(count),
                                 "pct": round(100 * count / len(values), 3)})
    return pd.DataFrame(rows)


def date_summary(views: dict[str, dict[str, pd.DataFrame]]) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Date ranges and monthly row counts per date column."""
    summary, monthly = [], []
    cutoff = pd.Timestamp(DATA_CUTOFF)
    for key, spec in DATASETS.items():
        for view_name, table in views[key].items():
            for column in spec.by_kind("date"):
                values = table[column]
                present = values.dropna()
                summary.append({
                    "dataset": spec.name, "view": view_name, "column": column,
                    "non_null": len(present), "missing": int(values.isna().sum()),
                    "distinct_dates": int(present.nunique()),
                    "min_date": present.min().date().isoformat(),
                    "max_date": present.max().date().isoformat(),
                    "with_time_component": int((present != present.dt.normalize()).sum()),
                    "after_data_cutoff": int((present > cutoff).sum()),
                })
                months = present.dt.strftime("%Y-%m").value_counts().sort_index()
                for month, count in months.items():
                    monthly.append({"dataset": spec.name, "view": view_name, "column": column,
                                    "month": month, "rows": int(count)})
    return pd.DataFrame(summary), pd.DataFrame(monthly)


def _key_candidates(spec: DatasetSpec) -> list[str]:
    excluded = {"plant"}  # constant value, cannot contribute to a key
    return [c.standard for c in spec.columns
            if c.kind in ("identifier", "date") and c.standard not in excluded]


def candidate_primary_keys(table: pd.DataFrame, spec: DatasetSpec, max_columns: int = 3,
                           documented_keys: tuple = ()) -> pd.DataFrame:
    """Test identifier and date columns, alone and combined, on all and distinct rows.

    A combination is reported if it is a single column, a documented key, or unique
    on distinct rows with no smaller subset already unique. Combinations with dates
    can be unique by chance, so they are marked as coincidental, not business keys.
    Uniqueness alone does not make a combination a meaningful business key.
    """
    documented = {frozenset(key) for key in documented_keys}
    distinct = table.drop_duplicates("row_hash")
    date_columns = set(spec.by_kind("date"))
    unique_sets: list[frozenset] = []
    rows = []
    for size in range(1, max_columns + 1):
        for combo in combinations(_key_candidates(spec), size):
            combo_list = list(combo)
            repeats_all = int(table.duplicated(combo_list).sum())
            repeats_distinct = int(distinct.duplicated(combo_list).sum())
            has_nulls = bool(table[combo_list].isna().any(axis=None))
            unique_on_distinct = repeats_distinct == 0
            minimal = not any(s < frozenset(combo) for s in unique_sets)
            if unique_on_distinct and minimal and not has_nulls:
                unique_sets.append(frozenset(combo))
            is_new_key = unique_on_distinct and minimal and not has_nulls
            if size > 1 and not is_new_key and frozenset(combo) not in documented:
                continue
            uses_date = bool(set(combo) & date_columns)
            if has_nulls:
                assessment = "not_a_key_contains_nulls"
            elif not unique_on_distinct:
                assessment = "not_unique"
            elif uses_date and frozenset(combo) not in documented:
                assessment = "coincidental_unique_includes_date"
            elif repeats_all == 0:
                assessment = "unique_on_all_rows"
            else:
                assessment = "unique_only_after_setting_aside_exact_copies"
            rows.append({"dataset": spec.name, "columns": " + ".join(combo), "column_count": size,
                         "rows": len(table), "repeats_on_all_rows": repeats_all,
                         "distinct_rows": len(distinct), "repeats_on_distinct_rows": repeats_distinct,
                         "contains_nulls": has_nulls, "includes_date": uses_date,
                         "assessment": assessment})
    # Whole-row uniqueness shows whether any natural key could exist at all.
    whole_row_repeats = int(table.duplicated("row_hash").sum())
    rows.append({"dataset": spec.name, "columns": "(all source columns)",
                 "column_count": len(spec.columns), "rows": len(table),
                 "repeats_on_all_rows": whole_row_repeats, "distinct_rows": len(distinct),
                 "repeats_on_distinct_rows": 0, "contains_nulls": False, "includes_date": False,
                 "assessment": "no_natural_key_possible_on_all_rows" if whole_row_repeats else "whole_row_unique"})
    return pd.DataFrame(rows)


def _cardinality(max_a: int, max_b: int) -> str:
    return f"{'1' if max_a == 1 else 'N'}:{'1' if max_b == 1 else 'N'}"


def _foreign_key_assessment(same_name: bool, in_diagram: bool, shared: int, distinct_a: int, distinct_b: int) -> str:
    if not same_name and not in_diagram:
        return "value_overlap_only_not_supported_by_name_or_diagram"
    if shared in (distinct_a, distinct_b):
        return "candidate_foreign_key_one_side_fully_contained"
    return "shared_key_partial_overlap"


def candidate_foreign_keys(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Compare identifier value sets across datasets. No tables are joined.

    Pairs are discovered from overlapping values, not assumed from column names.
    A pair sharing values but with different meanings is reported as value overlap
    only. Row counts for a raw inner join are computed from key frequencies.
    """
    diagram = {frozenset((a, b)): cardinality for a, b, cardinality in DIAGRAM_RELATIONS}
    columns = [(key, column) for key, spec in DATASETS.items() for column in spec.by_kind("identifier")]
    rows = []
    for (key_a, col_a), (key_b, col_b) in combinations(columns, 2):
        if key_a == key_b:
            continue
        counts_a = tables[key_a][col_a].dropna().value_counts()
        counts_b = tables[key_b][col_b].dropna().value_counts()
        shared = counts_a.index.intersection(counts_b.index)
        if len(shared) == 0:
            continue
        name_a, name_b = f"{key_a}.{col_a}", f"{key_b}.{col_b}"
        drawn = diagram.get(frozenset((name_a, name_b)))
        rows.append({
            "column_a": name_a, "column_b": name_b,
            "distinct_a": len(counts_a), "distinct_b": len(counts_b), "shared_values": len(shared),
            "coverage_of_a_pct": round(100 * len(shared) / len(counts_a), 2),
            "coverage_of_b_pct": round(100 * len(shared) / len(counts_b), 2),
            "unmatched_a": len(counts_a) - len(shared), "unmatched_b": len(counts_b) - len(shared),
            "rows_a": int(counts_a.sum()), "rows_b": int(counts_b.sum()),
            "max_rows_per_shared_key_a": int(counts_a[shared].max()),
            "max_rows_per_shared_key_b": int(counts_b[shared].max()),
            "observed_cardinality_a_to_b": _cardinality(int(counts_a[shared].max()), int(counts_b[shared].max())),
            "raw_inner_join_rows": int((counts_a[shared] * counts_b[shared]).sum()),
            "same_standard_name": col_a == col_b,
            "diagram_relation": drawn if drawn else "not in diagram",
            "assessment": _foreign_key_assessment(col_a == col_b, bool(drawn), len(shared),
                                                  len(counts_a), len(counts_b)),
        })
    return pd.DataFrame(rows)
