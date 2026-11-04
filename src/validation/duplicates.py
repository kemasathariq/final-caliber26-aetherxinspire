"""Exact-duplicate detection and metadata. Rows are labelled, never removed."""
import json

import pandas as pd


def add_duplicate_columns(table: pd.DataFrame, id_prefix: str) -> pd.DataFrame:
    """Label each row with its content group. Returns the same rows in source order.

    Rows are exact duplicates when every source column matches, which is what
    ``row_hash`` encodes. Group numbers follow first appearance in the file.
    """
    labelled = table.sort_values("source_row", kind="stable").reset_index(drop=True)
    groups = labelled.groupby("row_hash", sort=False)
    codes, _ = pd.factorize(labelled["row_hash"])
    labelled["content_group_id"] = pd.array(
        [f"{id_prefix}-{code + 1:06d}" for code in codes], dtype="string")
    labelled["occurrence_count"] = groups["source_row"].transform("size").astype("Int64")
    labelled["occurrence_rank"] = (groups.cumcount() + 1).astype("Int64")
    if len(labelled) != len(table):
        raise AssertionError("Duplicate labelling changed the row count")
    return labelled


def duplicate_summary(labelled: pd.DataFrame, dataset_key: str) -> dict:
    """Counts of exact duplicates and how far apart copies sit in the file."""
    first_rows = labelled[labelled["occurrence_rank"] == 1]
    extra = labelled[labelled["occurrence_rank"] > 1]
    distribution = first_rows["occurrence_count"].value_counts().sort_index()
    ordered = labelled[labelled["occurrence_count"] > 1].sort_values(
        ["content_group_id", "source_row"])
    gaps = ordered.groupby("content_group_id")["source_row"].diff().dropna().astype("int64")
    return {
        "dataset": dataset_key,
        "total_rows": len(labelled),
        "distinct_rows": len(first_rows),
        "extra_copies": len(extra),
        "extra_copies_pct": round(100 * len(extra) / len(labelled), 3) if len(labelled) else 0.0,
        "groups_with_copies": int((first_rows["occurrence_count"] > 1).sum()),
        "occurrence_distribution": json.dumps({str(k): int(v) for k, v in distribution.items()}),
        "adjacent_copy_gaps": int((gaps == 1).sum()),
        "copy_gaps": len(gaps),
        "median_copy_gap_rows": float(gaps.median()) if len(gaps) else None,
        "max_copy_gap_rows": int(gaps.max()) if len(gaps) else None,
    }


def duplicate_group_metadata(labelled: pd.DataFrame, source_columns: list[str],
                             key_sets: tuple, measures: tuple, context: tuple) -> pd.DataFrame:
    """One row per content group that occurs more than once.

    Includes source row references, occurrences, how far apart copies sit, whether
    all source columns really match, and how often the group's business keys
    appear under different content. Measures show the single-row value and the
    total across occurrences, so both views can be compared per group.
    """
    copies = labelled[labelled["occurrence_count"] > 1].sort_values(
        ["content_group_id", "source_row"])
    columns = ["content_group_id", "occurrence_count", "source_rows", "first_source_row",
               "last_source_row", "source_row_span", "adjacent_pairs",
               "all_source_columns_identical"]
    if copies.empty:
        return pd.DataFrame(columns=columns)

    grouped = copies.groupby("content_group_id", sort=True)
    row_lists = grouped["source_row"].agg(lambda rows: [int(r) for r in rows])
    metadata = pd.DataFrame({
        "occurrence_count": grouped["occurrence_count"].first(),
        "source_rows": row_lists.map(lambda rows: ";".join(map(str, rows))),
        "first_source_row": row_lists.map(lambda rows: rows[0]),
        "last_source_row": row_lists.map(lambda rows: rows[-1]),
        "source_row_span": row_lists.map(lambda rows: rows[-1] - rows[0]),
        "adjacent_pairs": row_lists.map(lambda rows: sum(b - a == 1 for a, b in zip(rows, rows[1:]))),
    })
    distinct_values = grouped[source_columns].nunique(dropna=False)
    metadata["all_source_columns_identical"] = distinct_values.max(axis=1) == 1

    first = grouped.first()
    for key_set in key_sets:
        for column in key_set:
            metadata[column] = first[column]
        # How many different content groups share this key across the whole table.
        name = "groups_sharing_" + "__".join(key_set)
        per_key = (labelled.groupby(list(key_set), dropna=False, observed=True)["content_group_id"]
                   .nunique().rename(name).reset_index())
        merged = metadata[list(key_set)].reset_index().merge(
            per_key, on=list(key_set), how="left", validate="many_to_one")
        metadata[name] = merged.set_index("content_group_id")[name]
    for column in context:
        metadata[column] = first[column]
    for column in measures:
        metadata[column] = first[column]
        metadata[f"{column}_sum_all_occurrences"] = grouped[column].sum()
    return metadata.reset_index()
