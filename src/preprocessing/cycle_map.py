"""Proposed maintenance interval mapping, from Spec Appendix A.

Status: PROPOSED, requires DEF-10. The readings below are the Specification's, not
confirmed definitions. In particular "2 WEEKLY" is read as every two weeks and could
mean twice a week. Originals stay in ``cycle_desc``, and mapped columns are named
``*_proposed``. ``interval_days_proposed`` is for sorting and comparing only, never
for projecting dates (Spec S05 and S07).
"""
import pandas as pd

DAYS_PER_UNIT = {"WEEK": 7.0, "MONTH": 30.4375, "YEAR": 365.25}

# source value, documented rows, value, unit, mapping status
_ROWS = (
    ("1 WEEKLY", 26, 1, "WEEK", "direct"), ("Weekly", 15, 1, "WEEK", "assumed_same_as_1_WEEKLY"),
    ("2 WEEK", 14, 2, "WEEK", "direct"), ("2 WEEKLY", 96, 2, "WEEK", "direct_ambiguous_reading"),
    ("4 WEEKLY", 92, 4, "WEEK", "direct"), ("8 WEEKLY", 3, 8, "WEEK", "direct"),
    ("12 WEEK", 76, 12, "WEEK", "direct"), ("16 WEEKLY", 3, 16, "WEEK", "direct"),
    ("24 WEEK", 39, 24, "WEEK", "direct"), ("26 WEEKLY", 31, 26, "WEEK", "direct"),
    ("48 WEEK", 26, 48, "WEEK", "direct"), ("1 MONTHLY", 49, 1, "MONTH", "direct"),
    ("Monthly", 160, 1, "MONTH", "assumed_same_as_1_MONTHLY"), ("2 MONTHLY", 3, 2, "MONTH", "direct"),
    ("3 MONTHLY", 267, 3, "MONTH", "direct"), ("4 MONTH", 83, 4, "MONTH", "direct"),
    ("6 MONTHLY", 788, 6, "MONTH", "direct"), ("12 MONTHLY", 229, 12, "MONTH", "direct"),
    ("18 MONTHLY", 1132, 18, "MONTH", "direct"), ("30 MONTHLY", 4, 30, "MONTH", "direct"),
    ("1 YEARLY", 1254, 1, "YEAR", "direct"), ("YEARLY", 465, 1, "YEAR", "assumed_same_as_1_YEARLY"),
    ("Yearly", 305, 1, "YEAR", "assumed_same_as_1_YEARLY"), ("2 YEARLY", 376, 2, "YEAR", "direct"),
    ("3 YEARLY", 202, 3, "YEAR", "direct"), ("5 YEARLY", 3767, 5, "YEAR", "direct"),
    ("8 YEARLY", 27, 8, "YEAR", "direct"), ("10 YEARLY", 621, 10, "YEAR", "direct"),
)


def build_map_cycle() -> pd.DataFrame:
    table = pd.DataFrame(_ROWS, columns=["cycle_desc", "rows_documented_in_spec", "interval_value_proposed",
                                         "interval_unit_proposed", "mapping_basis"])
    table["cycle_desc"] = table["cycle_desc"].astype("string")
    table["interval_unit_proposed"] = table["interval_unit_proposed"].astype("string")
    table["mapping_basis"] = table["mapping_basis"].astype("string")
    table["rows_documented_in_spec"] = table["rows_documented_in_spec"].astype("Int64")
    table["interval_value_proposed"] = table["interval_value_proposed"].astype("Int64")
    table["interval_days_proposed"] = (table["interval_value_proposed"].astype("float64")
                                       * table["interval_unit_proposed"].map(DAYS_PER_UNIT).astype("float64")).astype("Float64")
    table["mapping_status"] = pd.array(["proposed_requires_DEF-10"] * len(table), dtype="string")
    return table
