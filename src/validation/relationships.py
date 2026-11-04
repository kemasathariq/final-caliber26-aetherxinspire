"""Relationship audit against Spec Section 4.2, on conformed tables.

Counts come from the key values. Row-multiplying joins are measured, never stored.
``safe_for_analysis`` restates the conditions under which each join may be used.
"""
import pandas as pd

from src.preprocessing.joins import join_row_count, observed_cardinality
from src.preprocessing.prpo_views import DISTINCT, ORIGINAL


def _row(relationship: str, parent: str, child: str, keys: str, parent_keys: pd.Series, child_keys: pd.Series, spec_cardinality: str, safe: str, note: str = "", naive_rows: int | None = None) -> dict:
    parent_set, child_set = set(parent_keys.dropna()), set(child_keys.dropna())
    joined = join_row_count(parent_keys, child_keys)
    return {
        "relationship": relationship, "parent": parent, "child": child, "keys": keys, "spec_cardinality": spec_cardinality,
        "observed_cardinality": observed_cardinality(parent_keys, child_keys),
        "parent_rows": len(parent_keys), "child_rows": len(child_keys), "child_blank_keys": int(child_keys.isna().sum()),
        "distinct_parent_keys": len(parent_set), "distinct_child_keys": len(child_set),
        "child_keys_missing_in_parent": len(child_set - parent_set), "parent_keys_unused_by_child": len(parent_set - child_set),
        "child_rows_matched": int(child_keys.isin(parent_set).sum()),
        "child_coverage_pct": round(100 * float(child_keys.isin(parent_set).sum()) / len(child_keys), 2) if len(child_keys) else None,
        "inner_join_rows": joined, "rows_added_over_child": joined - int(child_keys.isin(parent_set).sum()),
        "naive_raw_join_rows_avoided": naive_rows, "safe_for_analysis": safe, "note": note,
    }


def relationship_audit(conformed: dict[str, pd.DataFrame], tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    dim_fl, dim_material, dim_supplier = conformed["dim_functional_location"], conformed["dim_material"], conformed["dim_supplier"]
    bridge_material, bridge_order = conformed["bridge_fl_material"], conformed["bridge_order_notification"]
    prpo, issue, notif, plan = conformed["fact_prpo_line"], conformed["fact_issue"], conformed["fact_notification"], conformed["fact_plan_item"]
    fl, material = dim_fl["functional_location"], dim_material["material_no"]
    distinct_prpo = prpo[prpo["in_exact_distinct_rows"]]
    rows = [
        _row("R1", "dim_functional_location", "bridge_fl_material", "functional_location", fl, bridge_material["functional_location"], "1:N", "Yes, as a lookup"),
        _row("R2", "dim_functional_location", "fact_notification", "functional_location", fl, notif["functional_location"], "1:N", "Yes, as a lookup"),
        _row("R3", "dim_functional_location", "fact_plan_item", "functional_location", fl, plan["functional_location"], "1:N", "Yes, as a lookup"),
        _row("R4", "dim_material", "fact_issue", "material_no", material, issue["material_no"], "1:N", "Yes, through dim_material only", naive_rows=join_row_count(tables["bom"]["material_no"], issue["material_no"])),
        _row(f"R5.{ORIGINAL}", "dim_material", "fact_prpo_line", "material_no", material, prpo["material_no"], "1:N", "Yes, through dim_material only. Name the view", naive_rows=join_row_count(tables["bom"]["material_no"], prpo["material_no"])),
        _row(f"R5.{DISTINCT}", "dim_material", "fact_prpo_line where in_exact_distinct_rows", "material_no", material, distinct_prpo["material_no"], "1:N", "Yes, through dim_material only. Name the view"),
        _row(f"R6.{ORIGINAL}", "dim_supplier", "fact_prpo_line", "supplier_code", dim_supplier["supplier_code"], prpo["supplier_code"], "1:N", "Yes, as a lookup. Name the view"),
        _row("R7", "bridge_order_notification", "fact_issue", "order_no", bridge_order["order_no"], issue["order_no"], "Mostly 1:N, shared orders N:N",
             "Conditional. Safe at order level. Quantities must not be summed after this join, because shared orders repeat rows", "Shared orders add rows. Use the flags on fact_issue instead of joining"),
        _row("R11", "fact_plan_item", "bridge_fl_material", "functional_location", plan["functional_location"], bridge_material["functional_location"], "N:M",
             "No for demand or requirements. Exploration only, in a table labelled as a hypothesis", "Lists every material on a location for every plan item. Plans do not state which parts they use"),
        _row("R12", "fact_plan_item", "fact_notification", "functional_location", plan["functional_location"], notif["functional_location"], "N:M", "Yes at location grain only, after aggregating both sides"),
    ]
    attributed = issue[issue["fl_attribution"] == "unique"]
    ambiguous = issue[issue["fl_attribution"] == "ambiguous"]
    rows.append(_row("R8", "dim_functional_location", "fact_issue attributed through its order", "attributed_functional_location", fl, attributed["attributed_functional_location"], "N:1 where the order has one notification",
                     "Conditional. Valid only for attributed rows, and coverage must be reported", f"{len(attributed):,} unique, {len(ambiguous):,} ambiguous and {int((issue['fl_attribution'] == 'none').sum()):,} with no link, of {len(issue):,} issue rows"))
    pair_rows = int(issue["issued_material_in_fl_bom"].notna().sum())
    rows.append({"relationship": "R10", "parent": "bridge_fl_material", "child": "fact_issue, linked rows", "keys": "functional_location + material_no", "spec_cardinality": "Pair lookup",
                 "observed_cardinality": "lookup", "parent_rows": len(bridge_material), "child_rows": pair_rows, "child_rows_matched": int(issue["issued_material_in_fl_bom"].fillna(False).sum()),
                 "child_coverage_pct": round(100 * float(issue["issued_material_in_fl_bom"].fillna(False).sum()) / pair_rows, 2) if pair_rows else None,
                 "safe_for_analysis": "Yes as a data quality measure. Not proof of where parts were used", "note": "A match means the issued material is on the BoM of a location linked through the order"})
    issued, procured = set(issue["material_no"]), set(prpo["material_no"])
    rows.append({"relationship": "R9", "parent": "Movement material aggregate", "child": "PR PO material aggregate", "keys": "material_no", "spec_cardinality": "1:1 after aggregation", "observed_cardinality": "1:1 after aggregation",
                 "distinct_parent_keys": len(issued), "distinct_child_keys": len(procured), "child_keys_missing_in_parent": len(procured - issued), "parent_keys_unused_by_child": len(issued - procured), "inner_join_rows": len(issued & procured),
                 "safe_for_analysis": "Yes, only after aggregating both sides. Name the PR PO view", "note": "Row-level joining is not allowed"})
    critical = plan[["functional_location", "criticality", "fl_desc"]].merge(dim_fl[["functional_location", "criticality", "fl_desc"]], on="functional_location", suffixes=("", "_master"), validate="many_to_one")
    mismatch = int((critical["criticality"].astype("string") != critical["criticality_master"].astype("string")).fillna(True).sum() + (critical["fl_desc"] != critical["fl_desc_master"]).fillna(True).sum())
    rows.append({"relationship": "R13", "parent": "dim_functional_location", "child": "fact_plan_item", "keys": "criticality, fl_desc", "spec_cardinality": "Equality check", "observed_cardinality": "equality check",
                 "child_rows": len(plan), "child_rows_matched": len(plan) - mismatch, "safe_for_analysis": "Not a join. Consistency test only", "note": f"{mismatch} mismatches"})
    order = ["R1", "R2", "R3", "R4", f"R5.{ORIGINAL}", f"R5.{DISTINCT}", f"R6.{ORIGINAL}", "R7", "R8", "R9", "R10", "R11", "R12", "R13"]
    frame = pd.DataFrame(rows)
    return frame.set_index("relationship").loc[order].reset_index()


def conformed_measures(conformed: dict[str, pd.DataFrame], audit: pd.DataFrame, evidence: dict, movement: pd.DataFrame) -> dict:
    """Named measures compared with data/reference/expected_values_conformed.json."""
    def true_count(table: str, column: str) -> int:
        return int(conformed[table][column].fillna(False).astype(bool).sum())

    prpo, issue, notif = conformed["fact_prpo_line"], conformed["fact_issue"], conformed["fact_notification"]
    distinct = prpo[prpo["in_exact_distinct_rows"]]
    measures: dict = {f"conformed.rows.{name}": len(frame) for name, frame in conformed.items()}
    for table, columns in {
        "fact_prpo_line": ("flag_req_before_pr", "flag_promise_before_pr", "flag_future_requested_date", "flag_future_promised_date", "in_idr_scope", "flag_unit_mismatch", "flag_desc_mismatch"),
        "fact_issue": ("has_notification", "order_shared", "flag_unit_mismatch", "flag_desc_mismatch"),
        "fact_notification": ("is_open", "order_missing", "flag_reqstart_before_notif", "flag_created_differs", "completed_late", "first_month_flag", "is_system_level"),
        "fact_plan_item": ("flag_cycle_unmapped", "flag_future_cycle_start", "start_day_is_first"),
        "dim_material": ("nonstock_with_stock", "stockitem_min_max_zero", "flag_fraction_on_count_unit", "is_issued", "is_procured"),
        "dim_functional_location": ("fl_has_bom", "fl_has_notification", "fl_has_plan", "fl_in_all_three", "criticality_missing"),
        "bridge_order_notification": ("order_shared",),
        "bridge_fl_material": ("flag_non_integer_installed_qty", "flag_fraction_on_count_unit"),
    }.items():
        for column in columns:
            measures[f"flag.{table}.{column}"] = true_count(table, column)
    measures.update({
        "flag.fact_prpo_line.flag_req_before_pr.exact_distinct_rows": int(distinct["flag_req_before_pr"].sum()),
        "flag.fact_prpo_line.flag_promise_before_pr.exact_distinct_rows": int(distinct["flag_promise_before_pr"].sum()),
        "flag.fact_issue.partial_dup_groups": int(issue["partial_dup_group_id"].nunique()),
        "flag.fact_issue.fl_attribution": {k: int(v) for k, v in issue["fl_attribution"].value_counts().sort_index().items()},
        "flag.fact_issue.issued_material_in_fl_bom": true_count("fact_issue", "issued_material_in_fl_bom"),
        "flag.fact_notification.partial_dup_extra_rows": int(notif.duplicated(["functional_location", "description", "notification_date"]).sum()),
        "flag.fact_notification.desc_ref_code_rows": int(notif["desc_ref_code"].notna().sum()),
        "flag.bridge_order_notification.shared_orders": int(conformed["bridge_order_notification"].loc[conformed["bridge_order_notification"]["order_shared"], "order_no"].nunique()),
        "flag.bridge_order_notification.shared_orders_same_location": true_count("bridge_order_notification", "shared_order_same_fl"),
        "flag.dim_material.mrp_type": {str(k): int(v) for k, v in conformed["dim_material"]["mrp_type"].astype("string").value_counts().sort_index().items()},
        "flag.dim_material.desc_shared_groups": int(conformed["dim_material"]["desc_shared_group_id"].nunique()),
        "flag.dim_material.desc_shared_materials": int(conformed["dim_material"]["desc_shared_group_id"].notna().sum()),
        "flag.fact_plan_item.plans_on_multiple_locations": int(conformed["fact_plan_item"].loc[conformed["fact_plan_item"]["plan_multi_fl"], "maintenance_plan"].nunique()),
    })
    for _, row in audit.iterrows():
        name = row["relationship"]
        for column in ("child_keys_missing_in_parent", "parent_keys_unused_by_child", "inner_join_rows", "child_rows_matched", "rows_added_over_child", "naive_raw_join_rows_avoided"):
            if pd.notna(row.get(column)):
                measures[f"relationship.{name}.{column}"] = int(row[column])
    keys = evidence["keys"]
    measures.update({f"evidence.keys.{k}": v for k, v in keys.items()})
    for _, row in evidence["permutations"].iterrows():
        measures[f"evidence.observed_same_copy_share.{row['grouping']}"] = round(float(row["observed_same_copy_share"]), 3)
    return measures
