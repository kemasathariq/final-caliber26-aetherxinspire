"""Exception lists: the rows behind each data quality count, for review. Rows are kept in the tables."""
import pandas as pd

# name, table, flag column, columns to list, related item, note
_LISTS = (
    ("prpo_requested_before_pr", "fact_prpo_line", "flag_req_before_pr", ("source_row", "purchase_requisition", "pr_item", "pr_date", "pr_delivery_date", "requested_interval_days", "in_exact_distinct_rows", "occurrence_count"), "DEF-06", "Requested date before PR date"),
    ("prpo_promised_before_pr", "fact_prpo_line", "flag_promise_before_pr", ("source_row", "purchase_order", "po_item", "pr_date", "po_delivery_date", "promised_interval_days", "in_exact_distinct_rows", "occurrence_count"), "DEF-06", "Promised date before PR date"),
    ("prpo_future_dates", "fact_prpo_line", "flag_future_date", ("source_row", "purchase_order", "po_item", "pr_delivery_date", "po_delivery_date", "flag_future_requested_date", "flag_future_promised_date", "in_exact_distinct_rows"), "A-01", "Requested or promised date after the assumed cutoff"),
    ("movement_same_key_different_quantity", "fact_issue", "is_partial_dup_group", ("source_row", "partial_dup_group_id", "posting_date", "material_no", "order_no", "quantity", "unit", "occurrence_count"), "A-05", "Same date, material and order with differing quantities"),
    ("notif_required_start_before_notification", "fact_notification", "flag_reqstart_before_notif", ("source_row", "notification", "notification_date", "required_start", "status"), "DEF-14", "Required Start before Notification Date"),
    ("notif_created_on_differs", "fact_notification", "flag_created_differs", ("source_row", "notification", "notification_date", "created_on"), "DEF-14", "Created On differs from Notification Date"),
    ("notif_same_location_description_date", "fact_notification", "is_partial_dup_group", ("source_row", "partial_dup_group_id", "notification", "functional_location", "description", "notification_date", "status"), "", "Same location, description and date on different notifications"),
    ("plan_future_cycle_start", "fact_plan_item", "flag_future_cycle_start", ("source_row", "maintenance_item", "maintenance_plan", "start_of_cycle", "cycle_desc"), "DEF-11", "Start of cycle after the assumed cutoff"),
    ("material_nonstock_with_stock", "dim_material", "nonstock_with_stock", ("material_no", "material_desc_clean", "unit", "stock", "min_qty", "max_qty", "mrp_type"), "DEF-04", "Non Stock material holding stock"),
    ("material_fraction_on_count_unit", "dim_material", "flag_fraction_on_count_unit", ("material_no", "material_desc_clean", "unit", "stock"), "DEF-15", "Non-integer Stock on EA, SET or ASS"),
    ("bom_non_integer_installed_qty", "bridge_fl_material", "flag_non_integer_installed_qty", ("source_row", "functional_location", "material_no", "installed_qty", "unit"), "DEF-15", "Non-integer Installed Qty"),
)


def build_exception_lists(conformed: dict[str, pd.DataFrame]) -> tuple[dict[str, pd.DataFrame], pd.DataFrame]:
    lists, summary = {}, []
    for name, table, flag, columns, related, description in _LISTS:
        frame = conformed[table]
        rows = frame.loc[frame[flag].fillna(False).astype(bool), list(columns)].reset_index(drop=True)
        lists[name] = rows
        entry = {"exception_list": name, "table": table, "flag": flag, "description": description, "rows": len(rows), "related_item": related}
        if "in_exact_distinct_rows" in rows:
            entry["rows_in_exact_distinct_view"] = int(rows["in_exact_distinct_rows"].sum())
        summary.append(entry)
    shared = conformed["dim_material"].loc[conformed["dim_material"]["desc_shared_group_id"].notna(), ["desc_shared_group_id", "material_desc_clean", "material_no", "unit", "mrp_type", "is_issued", "is_procured"]]
    lists["material_shared_descriptions"] = shared.sort_values(["desc_shared_group_id", "material_no"]).reset_index(drop=True)
    summary.append({"exception_list": "material_shared_descriptions", "table": "dim_material", "flag": "desc_shared_group_id", "description": "Same trimmed description on several material numbers. Never merged", "rows": len(shared), "related_item": "X-04"})
    return lists, pd.DataFrame(summary)


def repeated_maximum_values(conformed: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Is a measure's maximum shared by many unrelated rows? A natural heavy tail rarely repeats its peak exactly.

    Exact copies are set aside first, so repeated rows cannot create the pattern. A repeated
    maximum can suggest a cap in a system or in data generation, but this cannot confirm one.
    """
    prpo, issue = conformed["fact_prpo_line"], conformed["fact_issue"]
    prpo_distinct, issue_distinct = prpo[prpo["in_exact_distinct_rows"]], issue[issue["in_exact_distinct_rows"]]
    specs = (("Movement quantity", issue_distinct, "quantity", "unit", "exact_distinct_rows"), ("BoM Installed Qty", conformed["bridge_fl_material"], "installed_qty", "unit", "distinct_pairs"),
             ("BoM Stock", conformed["dim_material"], "stock", "unit", "one_row_per_material"), ("BoM Max.Qty", conformed["dim_material"], "max_qty", "unit", "one_row_per_material"),
             ("PR-Quantity", prpo_distinct, "pr_quantity", "unit", "exact_distinct_rows"), ("Requested interval, days", prpo_distinct, "requested_interval_days", None, "exact_distinct_rows"),
             ("Promised interval, days", prpo_distinct, "promised_interval_days", None, "exact_distinct_rows"), ("Days to complete notification", conformed["fact_notification"], "days_to_complete", None, "all_rows"))
    rows = []
    for label, frame, column, group, view in specs:
        groups = frame.astype({group: "string"}).groupby(group) if group else [("", frame)]
        for name, part in groups:
            values = part[column].dropna().astype("float64")
            if values.empty:
                continue
            peak = values.max()
            at_peak = part.loc[values[values == peak].index]
            below = values[values < peak]
            rows.append({"measure": label, "unit": name, "view": view, "values": len(values), "maximum": peak, "rows_at_maximum": len(at_peak),
                         "materials_at_maximum": int(at_peak["material_no"].nunique()) if "material_no" in at_peak else None,
                         "next_highest_value": below.max() if len(below) else None})
    return pd.DataFrame(rows)
