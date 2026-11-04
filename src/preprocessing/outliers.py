"""Outlier flags (Spec Section 2.8). Flags describe values. They remove or change nothing.

Primary rule, inside each group:
    robust z = 0.6745 x (value - median) / MAD, flagged if |z| > threshold.

Fallback, when a group has too few records or MAD = 0 (upper side only):
    flagged if value > Q3 + multiplier x IQR, using the wider fallback group.

Where the fallback group is too small or has IQR = 0, no fence can be defined, so
the value is reported as not assessed rather than flagged. The Specification does
not cover that case; see assumption A-10.
"""
import numpy as np
import pandas as pd

from src.config import OUTLIER_PARAMETERS

ROBUST_Z, IQR_FENCE, NOT_ASSESSED = "robust_z", "iqr_fence", "not_assessed"


def robust_outlier_flags(values: pd.Series, group: pd.Series, fallback_group: pd.Series | None = None,
                         parameters: dict = OUTLIER_PARAMETERS) -> pd.DataFrame:
    """Return ``flag``, ``method`` and ``score`` aligned to ``values``. Blank values stay blank."""
    fallback = fallback_group if fallback_group is not None else pd.Series("all", index=values.index)
    frame = pd.DataFrame({
        "value": pd.to_numeric(values, errors="coerce").astype("float64"),
        "group": group.astype("string"), "fallback": fallback.astype("string"),
    }, index=values.index)
    present = frame[frame["value"].notna()].copy()

    grouped = present.groupby("group")["value"]
    present["median"] = grouped.transform("median")
    present["mad"] = (present["value"] - present["median"]).abs().groupby(present["group"]).transform("median")
    present["records"] = grouped.transform("size")
    use_z = (present["records"] >= parameters["minimum_records_for_robust_z"]) & (present["mad"] > 0)

    wide = present.groupby("fallback")["value"]
    q1, q3 = wide.transform(lambda s: s.quantile(0.25)), wide.transform(lambda s: s.quantile(0.75))
    iqr = q3 - q1
    can_fence = (wide.transform("size") >= parameters["minimum_records_for_iqr_fence"]) & (iqr > 0)

    z = 0.6745 * (present["value"] - present["median"]) / present["mad"].where(present["mad"] > 0)
    fence_score = (present["value"] - q3) / iqr.where(iqr > 0)
    flag = np.where(use_z, z.abs() > parameters["robust_z_threshold"],
                    np.where(can_fence, fence_score > parameters["iqr_fence_multiplier"], False))
    method = np.where(use_z, ROBUST_Z, np.where(can_fence, IQR_FENCE, NOT_ASSESSED))
    score = np.where(use_z, z, np.where(can_fence, fence_score, np.nan))

    result = pd.DataFrame(index=values.index)
    result["flag"] = pd.Series(pd.NA, index=values.index, dtype="boolean")
    result["method"] = pd.Series(pd.NA, index=values.index, dtype="string")
    result["score"] = pd.Series(np.nan, index=values.index, dtype="float64")
    result.loc[present.index, "flag"] = pd.array(flag.astype(bool), dtype="boolean")
    result.loc[present.index, "method"] = pd.array(method, dtype="string")
    result.loc[present.index, "score"] = np.round(score.astype("float64"), 6)
    return result
