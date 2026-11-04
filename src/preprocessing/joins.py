"""Audited joins (Spec Section 4.1). Every join records counts and checks its cardinality.

A shared column name is not a reason to join. A lookup must keep the left table's
row count, so a join that multiplies rows fails here instead of inflating totals.
"""
import pandas as pd


class JoinAuditError(RuntimeError):
    """A join broke its declared key or row-count contract."""


def audited_lookup(left: pd.DataFrame, right: pd.DataFrame, on: str | list[str], name: str,
                   audit_log: list[dict] | None = None, require_all_matched: bool = False) -> pd.DataFrame:
    """Left join onto a table with a unique key. The left row count and order never change."""
    keys = [on] if isinstance(on, str) else list(on)
    if right.duplicated(keys).any():
        raise JoinAuditError(f"{name}: right key {keys} is not unique ({int(right.duplicated(keys).sum())} repeats)")
    overlap = (set(left.columns) & set(right.columns)) - set(keys)
    if overlap:
        raise JoinAuditError(f"{name}: columns would collide: {sorted(overlap)}")
    merged = left.merge(right, on=keys, how="left", validate="many_to_one", indicator="_match", sort=False)
    if len(merged) != len(left):
        raise JoinAuditError(f"{name}: row count changed from {len(left)} to {len(merged)}")
    # A blank key never matches a real parent; pandas would pair blanks with blanks.
    has_key = left[keys].notna().all(axis=1).to_numpy()
    matched = (merged["_match"] == "both").to_numpy() & has_key
    if require_all_matched and not matched[has_key].all():
        raise JoinAuditError(f"{name}: {int((~matched[has_key]).sum())} rows found no parent")
    if audit_log is not None:
        audit_log.append({"join": name, "keys": ";".join(keys), "left_rows": len(left), "right_rows": len(right),
                          "result_rows": len(merged), "matched_rows": int(matched.sum()),
                          "unmatched_rows": int((~matched[has_key]).sum()),
                          "left_rows_with_blank_key": int((~has_key).sum())})
    return merged.drop(columns="_match")


def join_row_count(left_keys: pd.Series, right_keys: pd.Series) -> int:
    """Rows an inner join would create, without building it."""
    a, b = left_keys.dropna().value_counts(), right_keys.dropna().value_counts()
    shared = a.index.intersection(b.index)
    return int((a[shared] * b[shared]).sum())


def observed_cardinality(left_keys: pd.Series, right_keys: pd.Series) -> str:
    """Cardinality among keys present on both sides."""
    a, b = left_keys.dropna().value_counts(), right_keys.dropna().value_counts()
    shared = a.index.intersection(b.index)
    if shared.empty:
        return "no shared keys"
    return f"{'N' if (a[shared] > 1).any() else '1'}:{'N' if (b[shared] > 1).any() else '1'}"
