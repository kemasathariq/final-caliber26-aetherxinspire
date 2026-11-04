"""Named data quality measures, and findings built from them.

Each measure is calculated once here. Validation compares measures with
data/reference/expected_values.json, and the findings table describes them.
Findings flag issues only. No source value is changed.
"""
import pandas as pd

from src.config import AUDIT_REPORT_DATE, DATA_CUTOFF
from src.preprocessing.prpo_views import DISTINCT, ORIGINAL


def _counts(series: pd.Series) -> dict[str, int]:
    return {str(k): int(v) for k, v in sorted(series.astype("string").value_counts().items())}


def _space_rows(series: pd.Series) -> int:
    text = series.dropna().astype("string")
    return int((text != text.str.strip()).sum())


def _prpo(views: dict[str, pd.DataFrame]) -> dict:
    original, distinct = views[ORIGINAL], views[DISTINCT]
    first = distinct
    result = {
        "prpo.distinct_rows": len(distinct),
        "prpo.occurrence_distribution": _counts(first["occurrence_count"]),
        "prpo.pr_key_repeats.original_rows": int(original.duplicated(["purchase_requisition", "pr_item"]).sum()),
        "prpo.pr_key_repeats.exact_distinct_rows": int(distinct.duplicated(["purchase_requisition", "pr_item"]).sum()),
        "prpo.po_key_repeats.original_rows": int(original.duplicated(["purchase_order", "po_item"]).sum()),
        "prpo.po_key_repeats.exact_distinct_rows": int(distinct.duplicated(["purchase_order", "po_item"]).sum()),
        "prpo.distinct_purchase_requisitions": int(original["purchase_requisition"].nunique()),
        "prpo.distinct_purchase_orders": int(original["purchase_order"].nunique()),
        "prpo.distinct_materials": int(original["material_no"].nunique()),
        "prpo.distinct_suppliers": int(original["supplier_code"].nunique()),
        "prpo.max_names_per_supplier": int(original.groupby("supplier_code")["supplier_name"].nunique().max()),
        "prpo.max_suppliers_per_po": int(original.groupby("purchase_order")["supplier_code"].nunique().max()),
        "prpo.max_suppliers_per_material": int(original.groupby("material_no")["supplier_code"].nunique().max()),
        "prpo.plant_values": sorted(original["plant"].unique().tolist()),
        "prpo.currency_rows.original_rows": _counts(original["currency"]),
        "prpo.currency_rows.exact_distinct_rows": _counts(distinct["currency"]),
        "prpo.max_currencies_per_supplier": int(original.groupby("supplier_code")["currency"].nunique().max()),
        "prpo.suppliers_per_currency": {str(k): int(v) for k, v in original.astype({"currency": "string"})
                                        .groupby("currency")["supplier_code"].nunique().items()},
        "prpo.pr_prefix_type_violations": int(
            (original.groupby("pr_type", observed=True)["purchase_requisition"]
             .apply(lambda s: s.str[:2].nunique()) != 1).sum()),
        "prpo.material_desc_space_rows": _space_rows(original["material_desc"]),
    }
    for name, view in views.items():
        result[f"prpo.requested_before_pr.{name}"] = int((view["pr_delivery_date"] < view["pr_date"]).sum())
        result[f"prpo.promised_before_pr.{name}"] = int((view["po_delivery_date"] < view["pr_date"]).sum())
        result[f"prpo.promised_before_requested.{name}"] = int((view["po_delivery_date"] < view["pr_delivery_date"]).sum())
        result[f"prpo.requested_after_cutoff.{name}"] = int((view["pr_delivery_date"] > pd.Timestamp(DATA_CUTOFF)).sum())
        result[f"prpo.promised_after_cutoff.{name}"] = int((view["po_delivery_date"] > pd.Timestamp(DATA_CUTOFF)).sum())
    return result


def _bom(bom: pd.DataFrame) -> dict:
    distinct = bom.drop_duplicates("row_hash")
    attributes = ["material_desc", "unit", "min_qty", "max_qty", "stock", "mrp_type"]
    per_material = distinct.groupby("material_no")
    material = distinct.drop_duplicates("material_no")
    mrp = material["mrp_type"].astype("string")
    stock_items, non_stock = material[mrp == "Stock Item"], material[mrp == "Non Stock"]
    fractions = bom[bom["installed_qty"] % 1 != 0]
    fraction_stock = material[material["stock"] % 1 != 0]
    count_units = {"EA", "SET", "ASS"}
    trimmed = material.assign(desc=material["material_desc"].str.strip())
    shared = trimmed.groupby("desc")["material_no"].nunique()
    return {
        "bom.distinct_rows": len(distinct),
        "bom.pair_repeats.all_rows": int(bom.duplicated(["functional_location", "material_no"]).sum()),
        "bom.pair_repeats.distinct_rows": int(distinct.duplicated(["functional_location", "material_no"]).sum()),
        "bom.materials_with_conflicting_attributes": {
            a: int((per_material[a].nunique() > 1).sum()) for a in attributes},
        "bom.distinct_materials": int(bom["material_no"].nunique()),
        "bom.distinct_locations": int(bom["functional_location"].nunique()),
        "bom.mrp_materials": _counts(material["mrp_type"]),
        "bom.non_stock_with_stock": int((non_stock["stock"] > 0).sum()),
        "bom.non_stock_with_min_or_max": int(((non_stock["min_qty"] != 0) | (non_stock["max_qty"] != 0)).sum()),
        "bom.stock_item_zero_stock": int((stock_items["stock"] == 0).sum()),
        "bom.stock_item_below_min": int((stock_items["stock"] < stock_items["min_qty"]).sum()),
        "bom.stock_item_above_max": int((stock_items["stock"] > stock_items["max_qty"]).sum()),
        "bom.stock_item_min_max_zero": int(((stock_items["min_qty"] == 0) & (stock_items["max_qty"] == 0)).sum()),
        "bom.min_greater_than_max": int((material["min_qty"] > material["max_qty"]).sum()),
        "bom.non_integer_stock_rows": int((bom["stock"] % 1 != 0).sum()),
        "bom.non_integer_stock_on_count_unit_materials": int(fraction_stock["unit"].astype("string").isin(count_units).sum()),
        "bom.non_integer_installed_rows": len(fractions),
        "bom.non_integer_installed_by_unit": _counts(fractions["unit"]),
        "bom.max_rows_per_material": int(bom.groupby("material_no").size().max()),
        "bom.max_locations_per_material": int(distinct.groupby("material_no")["functional_location"].nunique().max()),
        "bom.material_desc_space_rows": _space_rows(bom["material_desc"]),
        "bom.descriptions_on_multiple_materials": int((shared > 1).sum()),
        "bom.materials_with_shared_description": int(shared[shared > 1].sum()),
    }


def _movement(movement: pd.DataFrame) -> dict:
    keys = movement.groupby(["posting_date", "material_no", "order_no"])["quantity"]
    sizes, varied = keys.size(), keys.nunique()
    months = movement["posting_date"].dt.strftime("%Y-%m").value_counts()
    active = movement.assign(m=movement["posting_date"].dt.strftime("%Y-%m")).groupby("material_no")["m"].nunique()
    return {
        "movement.distinct_rows": int(movement["row_hash"].nunique()),
        "movement.movement_types": sorted(movement["movement_type"].astype("string").unique().tolist()),
        "movement.distinct_materials": int(movement["material_no"].nunique()),
        "movement.distinct_orders": int(movement["order_no"].nunique()),
        "movement.same_date_material_order_groups": int((sizes > 1).sum()),
        "movement.same_key_groups_with_different_quantity": int((varied > 1).sum()),
        "movement.material_desc_space_rows": _space_rows(movement["material_desc"]),
        "movement.peak_month_rows": int(months.max()),
        "movement.materials_active_in_one_month": int((active == 1).sum()),
    }


def _notif(notif: pd.DataFrame) -> dict:
    status = notif["status"].astype("string")
    has_order = notif["order_no"].notna()
    has_completion = notif["completion_date"].notna()
    per_order = notif[has_order].groupby("order_no")
    locations = per_order["functional_location"].nunique()
    shared = locations[per_order.size() > 1]
    notif_prefix = notif["notification"].str[:3]
    prefix_by_type = pd.crosstab(notif["notification_type"].astype("string"), notif["order_no"].str[:3])
    first_word = notif["description"].str.strip().str.split().str[0].str.lower()
    return {
        "notif.distinct_notifications": int(notif["notification"].nunique()),
        "notif.status_rows": _counts(status),
        "notif.complete_with_completion_date": int(((status == "Complete") & has_completion).sum()),
        "notif.complete_without_completion_date": int(((status == "Complete") & ~has_completion).sum()),
        "notif.in_progress_with_completion_date": int(((status == "In Progress") & has_completion).sum()),
        "notif.in_progress_without_completion_date": int(((status == "In Progress") & ~has_completion).sum()),
        "notif.null_orders": int((~has_order).sum()),
        "notif.null_orders_not_in_progress": int(((~has_order) & (status != "In Progress")).sum()),
        "notif.distinct_orders": int(notif["order_no"].nunique()),
        "notif.orders_on_multiple_notifications": len(shared),
        "notif.max_notifications_per_order": int(per_order.size().max()),
        "notif.shared_orders_on_same_location": int((shared == 1).sum()),
        "notif.prefix_type_violations": int(
            (notif.groupby("notification_type", observed=True)["notification"]
             .apply(lambda s: s.str[:3].nunique()) != 1).sum() + (notif_prefix.nunique() != 4)),
        "notif.order_prefix_202_rows_by_type": {str(k): int(v) for k, v in prefix_by_type["202"].items() if v},
        "notif.required_end_before_start": int((notif["required_end"] < notif["required_start"]).sum()),
        "notif.completion_before_notification": int((notif["completion_date"] < notif["notification_date"]).sum()),
        "notif.required_start_before_notification": int((notif["required_start"] < notif["notification_date"]).sum()),
        "notif.completed_after_required_end": int((notif["completion_date"] > notif["required_end"]).sum()),
        "notif.created_on_differs": int((notif["created_on"] != notif["notification_date"]).sum()),
        "notif.first_month_rows": int((notif["notification_date"].dt.strftime("%Y-%m") == "2025-05").sum()),
        "notif.on_site_level_locations": int(notif["functional_location"].str.startswith("SITE").sum()),
        "notif.description_starts_with_replace": int((first_word == "replace").sum()),
        "notif.bracket_prefix_rows": int(notif["description"].str.match(r"\s*\[").sum()),
    }


def _mitem(mitem: pd.DataFrame, funcloc: pd.DataFrame) -> dict:
    joined = mitem[["functional_location", "criticality", "fl_desc"]].merge(
        funcloc[["functional_location", "criticality", "fl_desc"]],
        on="functional_location", how="left", suffixes=("", "_master"), validate="many_to_one")
    critical = joined["criticality"].astype("string")
    master = joined["criticality_master"].astype("string")
    plans = mitem.groupby("maintenance_plan")["functional_location"].nunique()
    start = mitem["start_of_cycle"]
    return {
        "mitem.distinct_items": int(mitem["maintenance_item"].nunique()),
        "mitem.distinct_plans": int(mitem["maintenance_plan"].nunique()),
        "mitem.distinct_locations": int(mitem["functional_location"].nunique()),
        "mitem.cycle_description_rows": _counts(mitem["cycle_desc"]),
        "mitem.criticality_differs_from_master": int((critical != master).fillna(True).sum()),
        "mitem.description_differs_from_master": int((joined["fl_desc"] != joined["fl_desc_master"]).fillna(True).sum()),
        "mitem.start_after_cutoff": int((start > pd.Timestamp(DATA_CUTOFF)).sum()),
        "mitem.start_after_audit_date": int((start > pd.Timestamp(AUDIT_REPORT_DATE)).sum()),
        "mitem.start_on_first_of_month": int((start.dt.day == 1).sum()),
        "mitem.plans_on_multiple_locations": int((plans > 1).sum()),
    }


def _funcloc(funcloc: pd.DataFrame) -> dict:
    is_site = funcloc["functional_location"].str.startswith("SITE")
    missing = funcloc["criticality"].isna()
    return {
        "funcloc.distinct_locations": int(funcloc["functional_location"].nunique()),
        "funcloc.null_criticality": int(missing.sum()),
        "funcloc.null_criticality_not_site": int((missing & ~is_site).sum()),
        "funcloc.site_rows": int(is_site.sum()),
        "funcloc.criticality_rows": _counts(funcloc["criticality"]),
        "funcloc.prefix_rows": _counts(funcloc["functional_location"].str.split("_").str[0]),
    }


def _cross(t: dict[str, pd.DataFrame]) -> dict:
    funcloc = set(t["funcloc"]["functional_location"])
    bom, movement, prpo, notif, mitem = t["bom"], t["movement"], t["prpo"], t["notif"], t["mitem"]
    materials = set(bom["material_no"])
    issued, procured = set(movement["material_no"]), set(prpo["material_no"])
    move_orders, notif_orders = set(movement["order_no"]), set(notif["order_no"].dropna())

    per_material_units: dict[str, set] = {}
    per_material_desc: dict[str, set] = {}
    for table in (bom, movement, prpo):
        pairs = table[["material_no", "unit", "material_desc"]].astype("string")
        for material, unit, description in pairs.drop_duplicates().itertuples(index=False):
            per_material_units.setdefault(material, set()).add(unit)
            per_material_desc.setdefault(material, set()).add(description.strip())

    linked = movement.merge(notif.loc[notif["order_no"].notna(),
                                      ["order_no", "notification_date", "functional_location",
                                       "completion_date", "required_start", "created_on"]],
                            on="order_no", how="inner")
    bom_distinct = bom.drop_duplicates("row_hash")
    bom_pairs = set(zip(bom_distinct["functional_location"], bom_distinct["material_no"]))
    in_bom = [pair in bom_pairs for pair in zip(linked["functional_location"], linked["material_no"])]
    linked = linked.assign(in_bom=in_bom)

    def raw_join_rows(left: pd.Series, right: pd.Series) -> int:
        a, b = left.value_counts(), right.value_counts()
        shared = a.index.intersection(b.index)
        return int((a[shared] * b[shared]).sum())

    return {
        "cross.bom_locations_missing_from_funcloc": len(set(bom["functional_location"]) - funcloc),
        "cross.notif_locations_missing_from_funcloc": len(set(notif["functional_location"]) - funcloc),
        "cross.mitem_locations_missing_from_funcloc": len(set(mitem["functional_location"]) - funcloc),
        "cross.movement_materials_missing_from_bom": len(issued - materials),
        "cross.prpo_materials_missing_from_bom": len(procured - materials),
        "cross.materials_issued_and_procured": len(issued & procured),
        "cross.materials_issued_only": len(issued - procured),
        "cross.materials_procured_only": len(procured - issued),
        "cross.bom_materials_neither": len(materials - issued - procured),
        "cross.max_units_per_material": max(len(v) for v in per_material_units.values()),
        "cross.max_descriptions_per_material": max(len(v) for v in per_material_desc.values()),
        "cross.movement_orders_found_in_notif": len(move_orders & notif_orders),
        "cross.movement_rows_with_notif_order": int(movement["order_no"].isin(notif_orders).sum()),
        "cross.movement_notif_joined_rows": len(linked),
        "cross.joined_rows_posted_before_notification": int((linked["posting_date"] < linked["notification_date"]).sum()),
        "cross.joined_rows_material_in_location_bom": int(linked["in_bom"].sum()),
        "cross.movement_rows_in_bom_for_any_linked_notification": int(linked.groupby("source_row")["in_bom"].any().sum()),
        "cross.raw_join_rows_bom_movement": raw_join_rows(bom["material_no"], movement["material_no"]),
        "cross.raw_join_rows_bom_prpo": raw_join_rows(bom["material_no"], prpo["material_no"]),
        "cross.raw_join_rows_mitem_bom_all_rows": raw_join_rows(mitem["functional_location"], bom["functional_location"]),
        "cross.raw_join_rows_mitem_bom_distinct": raw_join_rows(mitem["functional_location"], bom_distinct["functional_location"]),
        "cross.locations_in_bom_notif_and_mitem": len(set(bom["functional_location"]) & set(notif["functional_location"]) & set(mitem["functional_location"])),
    }


def compute_measures(tables: dict[str, pd.DataFrame], prpo_views: dict[str, pd.DataFrame]) -> dict:
    measures: dict = {f"rows.{key}": len(table) for key, table in tables.items()}
    measures.update({f"exact_duplicate_extras.{key}": int(table.duplicated("row_hash").sum())
                     for key, table in tables.items()})
    measures.update(_prpo(prpo_views))
    measures.update(_bom(tables["bom"]))
    measures.update(_movement(tables["movement"]))
    measures.update(_notif(tables["notif"]))
    measures.update(_mitem(tables["mitem"], tables["funcloc"]))
    measures.update(_funcloc(tables["funcloc"]))
    measures.update(_cross(tables))
    return measures


# id, dataset, field, finding, measure name, view, treatment, related definition
_FINDINGS = (
    ("DQ-01", "PR PO", "all columns", "Rows repeating an earlier row in all 18 columns", "exact_duplicate_extras.prpo", ORIGINAL, "Kept. Dual views maintained. No view is declared definitive", "DEF-01"),
    ("DQ-02", "PR PO", "PR-Delivery Date", "Requested date before PR date", "prpo.requested_before_pr.original_rows", ORIGINAL, "Flag only", "DEF-06"),
    ("DQ-03", "PR PO", "PR-Delivery Date", "Requested date before PR date", "prpo.requested_before_pr.exact_distinct_rows", DISTINCT, "Flag only", "DEF-06"),
    ("DQ-04", "PR PO", "PO-Delivery Date", "Promised date before PR date", "prpo.promised_before_pr.original_rows", ORIGINAL, "Flag only", "DEF-06"),
    ("DQ-05", "PR PO", "PO-Delivery Date", "Promised date before PR date", "prpo.promised_before_pr.exact_distinct_rows", DISTINCT, "Flag only", "DEF-06"),
    ("DQ-06", "PR PO", "PO-Delivery Date", "Promised date after the assumed data cutoff", "prpo.promised_after_cutoff.original_rows", ORIGINAL, "Flag only. Cutoff is an assumption", "A-01"),
    ("DQ-07", "PR PO", "PR-Material Desc", "Rows with leading or trailing spaces", "prpo.material_desc_space_rows", ORIGINAL, "Original text kept verbatim", ""),
    ("DQ-08", "BoM", "all columns", "Rows repeating an earlier row in all 9 columns", "exact_duplicate_extras.bom", "all_rows", "Kept and labelled", ""),
    ("DQ-09", "BoM", "Stock, Min.Qty, Max.Qty, MRP Type", "Non Stock materials holding stock above zero", "bom.non_stock_with_stock", "one_row_per_material", "Flag only", "DEF-04"),
    ("DQ-10", "BoM", "Stock", "Stock Item materials with zero stock. Not a stockout without a business rule", "bom.stock_item_zero_stock", "one_row_per_material", "Comparison only", "DEF-02"),
    ("DQ-11", "BoM", "Stock", "Stock Item materials below Min.Qty. Min.Qty meaning is undefined", "bom.stock_item_below_min", "one_row_per_material", "Comparison only", "DEF-02"),
    ("DQ-12", "BoM", "Stock", "Stock Item materials above Max.Qty. Max.Qty meaning is undefined", "bom.stock_item_above_max", "one_row_per_material", "Comparison only", "DEF-02"),
    ("DQ-13", "BoM", "Stock", "Rows with non-integer stock. One material holds 0.5 in unit EA", "bom.non_integer_stock_rows", "all_rows", "Flag only", ""),
    ("DQ-14", "BoM", "Installed Qty", "Rows with non-integer Installed Qty. All are in unit M", "bom.non_integer_installed_rows", "all_rows", "Flag only", "DEF-15"),
    ("DQ-15", "BoM", "Material Desc.", "Rows with leading or trailing spaces", "bom.material_desc_space_rows", "all_rows", "Original text kept verbatim", ""),
    ("DQ-16", "BoM", "Material Desc.", "Trimmed descriptions shared by more than one material number", "bom.descriptions_on_multiple_materials", "one_row_per_material", "Flag only. Never merge material numbers", ""),
    ("DQ-17", "Movement Material", "all columns", "Rows repeating an earlier row in all 7 columns. No document number exists to test them", "exact_duplicate_extras.movement", "all_rows", "Kept and labelled", ""),
    ("DQ-18", "Movement Material", "Posting Date, Material, Order", "Same date, material and order, with differing quantities", "movement.same_key_groups_with_different_quantity", "all_rows", "Kept", ""),
    ("DQ-19", "Movement Material", "Material Descriptions", "Rows with leading or trailing spaces", "movement.material_desc_space_rows", "all_rows", "Original text kept verbatim", ""),
    ("DQ-20", "Notif History", "Order", "Notifications with no order. All are In Progress", "notif.null_orders", "all_rows", "Null kept. Not imputed", ""),
    ("DQ-21", "Notif History", "Order", "Orders on two notifications at different functional locations", "notif.orders_on_multiple_notifications", "all_rows", "Flag only", "A-07"),
    ("DQ-22", "Notif History", "Completion by Date", "Null completion dates. Exactly the In Progress rows", "notif.in_progress_without_completion_date", "all_rows", "Null kept. Not imputed", ""),
    ("DQ-23", "Notif History", "Required Start", "Required start before notification date", "notif.required_start_before_notification", "all_rows", "Flag only", "DEF-14"),
    ("DQ-24", "Notif History", "Created On", "Created On differs from Notification Date", "notif.created_on_differs", "all_rows", "Both kept", "DEF-14"),
    ("DQ-25", "Notif History", "Notification Date", "Notifications in May 2025, far above later months. Cause unknown", "notif.first_month_rows", "all_rows", "Flag only", ""),
    ("DQ-26", "Mitem & Mplan", "Cycle Descriptions", "Distinct spellings of the maintenance interval", "mitem.distinct_cycle_spellings", "all_rows", "Originals kept. Mapping awaits confirmation", "DEF-10"),
    ("DQ-27", "Mitem & Mplan", "Start of cycle", "Start of cycle after the assumed data cutoff", "mitem.start_after_cutoff", "all_rows", "Flag only", "DEF-11"),
    ("DQ-28", "FuncLoc list", "FuncLoc Criticallity", "Null criticality. Exactly the SITE rows", "funcloc.null_criticality", "all_rows", "Null kept. Not imputed", "DEF-03"),
    ("DQ-30", "PR PO", "PO-Delivery Date", "Promised date after the assumed data cutoff", "prpo.promised_after_cutoff.exact_distinct_rows", DISTINCT, "Flag only. Cutoff is an assumption", "A-01"),
    ("DQ-31", "PR PO", "PR-Delivery Date", "Requested date after the assumed data cutoff", "prpo.requested_after_cutoff.original_rows", ORIGINAL, "Flag only. Cutoff is an assumption", "A-01"),
    ("DQ-32", "PR PO", "PR-Delivery Date", "Requested date after the assumed data cutoff", "prpo.requested_after_cutoff.exact_distinct_rows", DISTINCT, "Flag only. Cutoff is an assumption", "A-01"),
    ("DQ-29", "Movement Material, Notif History", "Order", "Movement orders with no matching notification order", "cross.movement_orders_not_in_notif", "all_rows", "Kept. Order prefix meaning is undefined", "DEF-07"),
)


def build_findings(measures: dict) -> pd.DataFrame:
    """Potential data quality issues with counts. Describes the data; changes nothing."""
    extended = dict(measures)
    extended["mitem.distinct_cycle_spellings"] = len(measures["mitem.cycle_description_rows"])
    extended["cross.movement_orders_not_in_notif"] = (
        measures["movement.distinct_orders"] - measures["cross.movement_orders_found_in_notif"])
    rows = [{"finding_id": f[0], "dataset": f[1], "field": f[2], "finding": f[3], "count": extended[f[4]],
             "view_or_grain": f[5], "measure": f[4], "treatment": f[6], "related_definition": f[7]}
            for f in _FINDINGS]
    return pd.DataFrame(rows)
