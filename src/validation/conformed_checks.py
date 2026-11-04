"""Validation of the conformed layer: nothing lost, nothing altered, nothing invented."""
from pathlib import Path

import pandas as pd

from src.data.schemas import BOM_MATERIAL_ATTRIBUTES, DATASETS
from src.preprocessing.conform import read_conformed, type_map
from src.preprocessing.cycle_map import build_map_cycle
from src.preprocessing.prpo_views import DISTINCT
from src.validation.checks import result

GROUP = "conformed tables"
FACTS = {"fact_prpo_line": "prpo", "fact_issue": "movement", "fact_notification": "notif", "fact_plan_item": "mitem"}
UNIQUE_KEYS = {
    "dim_functional_location": ["functional_location"], "dim_material": ["material_no"], "dim_supplier": ["supplier_code"], "map_cycle": ["cycle_desc"],
    "bridge_fl_material": ["functional_location", "material_no"], "bridge_order_notification": ["order_no", "notification"],
    "fact_notification": ["notification"], "fact_plan_item": ["maintenance_item"],
}
# Column names that would mean an undefined business rule had been applied without approval.
FORBIDDEN_NAME_PARTS = ("priority_rank", "criticality_rank", "highest_criticality", "stock_status", "stockout", "actual", "lead_time", "lead_days", "amount_idr",
                        "fx_", "implied_unit_amount", "due_date", "failure", "is_foreign", "imputed", "weighted", "abc_class", "xyz_class", "forecast", "supplier_rank")


def _same(left: pd.Series, right: pd.Series) -> bool:
    if pd.api.types.is_datetime64_any_dtype(left):
        return bool(left.reset_index(drop=True).equals(right.reset_index(drop=True)))
    if isinstance(left.dtype, pd.CategoricalDtype) or str(left.dtype) in ("string", "str"):
        return bool(left.astype("string").reset_index(drop=True).equals(right.astype("string").reset_index(drop=True)))
    return bool(left.reset_index(drop=True).equals(right.reset_index(drop=True)))


def check_facts_preserve_sources(conformed: dict[str, pd.DataFrame], tables: dict[str, pd.DataFrame]) -> list[dict]:
    rows = []
    for name, key in FACTS.items():
        fact, source, spec = conformed[name], tables[key].sort_values("source_row", kind="stable"), DATASETS[key]
        rows.append(result(f"CONF-01.{name}", GROUP, spec.name, "Fact keeps every source row", len(source), len(fact)))
        rows.append(result(f"CONF-02.{name}", GROUP, spec.name, "Fact holds exactly the same source rows, in source order", source["source_row"].astype("int64").tolist(), fact["source_row"].astype("int64").tolist()))
        changed = [c for c in [*spec.standard_columns, "row_hash"] if not _same(source[c], fact[c])]
        rows.append(result(f"CONF-03.{name}", GROUP, spec.name, "All source values and row hashes are unchanged, including blanks", [], changed))
    return rows


def check_keys_and_coarser_tables(conformed: dict[str, pd.DataFrame], tables: dict[str, pd.DataFrame]) -> list[dict]:
    rows = [result(f"CONF-04.{name}", GROUP, name, f"Key {'+'.join(keys)} is unique", 0, int(conformed[name].duplicated(keys).sum())) for name, keys in UNIQUE_KEYS.items()]
    bom, bridge, dim = tables["bom"], conformed["bridge_fl_material"], conformed["dim_material"]
    listed = sorted(int(v) for text in bridge["all_source_rows"] for v in text.split(";"))
    rows.append(result("CONF-05.source_rows", GROUP, "BoM", "Pair table references every BoM source row exactly once", sorted(bom["source_row"].astype("int64").tolist()), listed))
    rows.append(result("CONF-05.occurrences", GROUP, "BoM", "Occurrence counts rebuild the BoM row count", len(bom), int(bridge["occurrence_count"].sum())))
    for unit, part in bom.astype({"unit": "string"}).groupby("unit"):
        inside = bridge[bridge["unit"].astype("string") == unit]
        rows.append(result(f"CONF-05.installed.{unit}", GROUP, "BoM", f"Pair values x occurrences rebuild Installed Qty ({unit})",
                           round(float(part["installed_qty"].sum()), 6), round(float((inside["installed_qty"] * inside["occurrence_count"]).sum()), 6)))
    expected = bom.sort_values("source_row").drop_duplicates("material_no").set_index("material_no")
    actual = dim.set_index("material_no").loc[expected.index]
    different = [a for a in BOM_MATERIAL_ATTRIBUTES if not _same(expected[a], actual[a])]
    rows.append(result("CONF-06", GROUP, "BoM", "Material dimension attributes equal the staged BoM", [], different))
    conflict = int(bom.groupby("material_no")[list(BOM_MATERIAL_ATTRIBUTES)].nunique(dropna=False).gt(1).any(axis=1).sum())
    rows.append(result("CONF-06.conflicts", GROUP, "BoM", "No material has differing attributes (the condition for dim_material)", 0, conflict))
    return rows


def check_views_and_flags(conformed: dict[str, pd.DataFrame], views: dict[str, pd.DataFrame], measures: dict) -> list[dict]:
    fact, issue, notif = conformed["fact_prpo_line"], conformed["fact_issue"], conformed["fact_notification"]
    distinct = views[DISTINCT]
    selected = fact[fact["in_exact_distinct_rows"]]
    rows = [result("CONF-07.rows", GROUP, "PR PO", "Conformed filter selects the same rows as the distinct view", distinct["source_row"].astype("int64").tolist(), selected["source_row"].astype("int64").tolist())]
    for currency, part in distinct.astype({"currency": "string"}).groupby("currency"):
        inside = selected[selected["currency"].astype("string") == currency]
        rows.append(result(f"CONF-07.amount.{currency}", GROUP, "PR PO", f"Filtered amount equals the distinct view ({currency})", round(float(part["po_item_amount"].sum()), 2), round(float(inside["po_item_amount"].sum()), 2)))
    # Blank means the row is outside that view. A filled value there would reuse another population's statistics.
    for frame, name in ((fact, "fact_prpo_line"), (issue, "fact_issue")):
        for column in [c for c in frame.columns if c.endswith(f"__{DISTINCT}")]:
            outside = ~frame["in_exact_distinct_rows"].fillna(False).astype(bool)
            rows.append(result(f"CONF-08.{name}.{column}", GROUP, name, "View-specific flag is blank outside its view", 0, int(frame.loc[outside, column].notna().sum())))
    # Flags against measures calculated separately from the staged tables.
    pairs = (("fact_prpo_line", "flag_req_before_pr", "prpo.requested_before_pr.original_rows"), ("fact_prpo_line", "flag_promise_before_pr", "prpo.promised_before_pr.original_rows"),
             ("fact_prpo_line", "flag_future_requested_date", "prpo.requested_after_cutoff.original_rows"), ("fact_prpo_line", "flag_future_promised_date", "prpo.promised_after_cutoff.original_rows"),
             ("fact_notification", "flag_reqstart_before_notif", "notif.required_start_before_notification"), ("fact_notification", "flag_created_differs", "notif.created_on_differs"),
             ("fact_notification", "completed_late", "notif.completed_after_required_end"), ("fact_notification", "first_month_flag", "notif.first_month_rows"),
             ("fact_notification", "order_missing", "notif.null_orders"), ("fact_notification", "is_system_level", "notif.on_site_level_locations"),
             ("fact_plan_item", "flag_future_cycle_start", "mitem.start_after_cutoff"), ("fact_plan_item", "start_day_is_first", "mitem.start_on_first_of_month"),
             ("dim_material", "nonstock_with_stock", "bom.non_stock_with_stock"), ("dim_material", "stockitem_min_max_zero", "bom.stock_item_min_max_zero"),
             ("dim_material", "flag_fraction_on_count_unit", "bom.non_integer_stock_on_count_unit_materials"), ("dim_functional_location", "criticality_missing", "funcloc.null_criticality"),
             ("fact_issue", "has_notification", "cross.movement_rows_with_notif_order"), ("fact_issue", "issued_material_in_fl_bom", "cross.movement_rows_in_bom_for_any_linked_notification"))
    for table, column, measure in pairs:
        rows.append(result(f"CONF-09.{table}.{column}", GROUP, table, f"Flag count equals separately calculated {measure}", measures[measure], int(conformed[table][column].fillna(False).astype(bool).sum())))
    rows.append(result("CONF-09.partial_groups", GROUP, "Movement", "Partial duplicate groups equal the separately calculated count", measures["movement.same_key_groups_with_different_quantity"], int(issue["partial_dup_group_id"].nunique())))
    attributed = issue["attributed_functional_location"].notna()
    rows.append(result("CONF-10.attribution", GROUP, "Movement", "A location is filled only when the order leads to exactly one location", ((issue["fl_attribution"] == "unique")).tolist() == attributed.tolist(), True))
    rows.append(result("CONF-10.ambiguous_not_allocated", GROUP, "Movement", "Issue rows on shared orders are not allocated", 0, int(issue.loc[issue["order_shared"], "attributed_functional_location"].notna().sum())))
    completion_filled = int(notif.loc[notif["is_open"], "days_to_complete"].notna().sum())
    rows.append(result("CONF-10.open_not_completed", GROUP, "Notif History", "Open notifications have no completion duration", 0, completion_filled))
    return rows


def check_no_unapproved_rules(conformed: dict[str, pd.DataFrame]) -> list[dict]:
    rows = []
    for name, frame in conformed.items():
        bad = sorted(c for c in frame.columns if any(part in c.lower() for part in FORBIDDEN_NAME_PARTS))
        rows.append(result(f"CONF-11.{name}", GROUP, name, "No column applies a rule that lacks an approved definition", [], bad))
        code_columns = [c for c in frame.columns if c in ("criticality", "notif_priority", "plan_priority", "fl_criticality") and isinstance(frame[c].dtype, pd.CategoricalDtype)]
        rows.append(result(f"CONF-12.{name}", GROUP, name, "Criticality and priority stay unordered", [], [c for c in code_columns if frame[c].cat.ordered]))
    return rows


def check_cycle_map(conformed: dict[str, pd.DataFrame]) -> list[dict]:
    plan = conformed["fact_plan_item"]
    counts = plan["cycle_desc"].astype("string").value_counts()
    documented = build_map_cycle().set_index("cycle_desc")["rows_documented_in_spec"]
    return [
        result("CONF-13.unmapped", GROUP, "Mitem & Mplan", "Every cycle spelling has a proposed mapping", 0, int(plan["flag_cycle_unmapped"].sum())),
        result("CONF-13.rows", GROUP, "Mitem & Mplan", "Spelling counts equal Spec Appendix A", {k: int(v) for k, v in documented.sort_index().items()}, {k: int(v) for k, v in counts.sort_index().items()}),
        result("CONF-13.status", GROUP, "Mitem & Mplan", "Mapping stays labelled as proposed", ["proposed_requires_DEF-10"], conformed["map_cycle"]["mapping_status"].unique().tolist()),
    ]


def check_join_audit(join_audit: pd.DataFrame) -> list[dict]:
    rows = []
    for _, entry in join_audit.iterrows():
        rows.append(result(f"JOIN.{entry['join']}.rows", "relationships", entry["join"], "Lookup keeps the left row count", int(entry["left_rows"]), int(entry["result_rows"])))
        rows.append(result(f"JOIN.{entry['join']}.unmatched", "relationships", entry["join"], "Every lookup key finds its parent", 0, int(entry["unmatched_rows"])))
    return rows


def check_conformed_round_trip(conformed: dict[str, pd.DataFrame], folder: Path) -> list[dict]:
    rows = []
    for name, frame in conformed.items():
        reloaded = read_conformed(Path(folder) / f"{name}.csv", type_map(frame))
        different = [c for c in frame.columns if not _same(frame[c], reloaded[c])] if list(frame.columns) == list(reloaded.columns) else ["column list"]
        rows.append(result(f"CONF-14.{name}", GROUP, name, "CSV reloads to identical values and identifiers", [], different))
    return rows
