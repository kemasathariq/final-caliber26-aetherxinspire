"""Conformed layer (L2): flagged facts, dimensions, bridges and mapping tables.

Rules enforced here:
  - Fact tables keep every source row, in source order, with source values unchanged.
    Repeated rows are labelled with ``in_exact_distinct_rows``. They are never removed.
  - Bridges at a coarser grain record every source row they represent.
  - Values that depend on a population are calculated separately for each view, and
    the column name says which view. Rows outside a view hold a blank.
  - Undefined codes stay unordered codes. No ranking, score, stock status label,
    stockout label, FX conversion, imputation or date projection exists here.
  - Interval names say requested or promised. No actual receipt date exists.
"""
import pandas as pd

from src.config import DATA_CUTOFF, EXTREME_INTERVAL_PERCENTILE, RARE_CATEGORY_DISTINCT_ROWS
from src.data.schemas import BOM_MATERIAL_ATTRIBUTES
from src.preprocessing.cycle_map import build_map_cycle
from src.preprocessing.joins import audited_lookup
from src.preprocessing.outliers import robust_outlier_flags
from src.preprocessing.prpo_views import DISTINCT, ORIGINAL

ALL_ROWS = "all_rows"
COUNT_UNITS = ("EA", "SET", "ASS")
REF_CODE_PATTERN = r"^\s*(?:[A-Za-z0-9]+/)?\[([^\]]+)\]"
CRITICALITY_CODES = ("A", "B", "C", "S")


class ConformError(RuntimeError):
    """A rule the conformed tables depend on does not hold, so they would be wrong."""


class _Build:
    """Collects the audit trail of one conformed build."""

    def __init__(self):
        self.joins: list[dict] = []
        self.log: list[dict] = []
        self.outlier_rows: list[pd.DataFrame] = []
        self.outlier_summary: list[dict] = []

    def record(self, table: str, spec_ref: str, rule_class: str, rule: str, columns: str, rows_before: int, rows_after: int) -> None:
        self.log.append({"table": table, "step": len([e for e in self.log if e["table"] == table]) + 1, "spec_reference": spec_ref,
                         "class": rule_class, "rule": rule, "columns_added": columns, "rows_before": rows_before, "rows_after": rows_after})

    def flag_outliers(self, frame: pd.DataFrame, table: str, measure: str, name: str, views: dict[str, pd.Series], group: str, fallback: str | None) -> list[str]:
        """Add one flag column per view. Population statistics differ by view, so they are never shared."""
        added = []
        for view, mask in views.items():
            subset = frame.loc[mask]
            flags = robust_outlier_flags(subset[measure], subset[group], subset[fallback] if fallback else None)
            column = f"flag_outlier_{name}__{view}"
            frame[column] = pd.Series(pd.NA, index=frame.index, dtype="boolean")
            frame.loc[mask, column] = flags["flag"]
            added.append(column)
            for method, part in flags.dropna(subset="method").groupby("method"):
                self.outlier_summary.append({"table": table, "measure": name, "view": view, "method": method, "values_assessed": len(part),
                                             "flagged": int(part["flag"].sum())})
            hit = flags[flags["flag"].fillna(False).astype(bool)]
            if len(hit):
                self.outlier_rows.append(pd.DataFrame({
                    "table": table, "measure": name, "view": view, "source_row": subset.loc[hit.index, "source_row"].astype("Int64"),
                    "group_key": subset.loc[hit.index, group].astype("string"), "value": subset.loc[hit.index, measure].astype("Float64"),
                    "method": hit["method"], "score": hit["score"]}))
        return added


def _clean(series: pd.Series) -> pd.Series:
    return series.astype("string").str.strip()


def _text(series: pd.Series) -> pd.Series:
    return series.astype("string")


def _month_start(dates: pd.Series) -> pd.Series:
    return dates.dt.to_period("M").dt.to_timestamp().astype("datetime64[ns]")


def _extreme(values: pd.Series, mask: pd.Series) -> pd.Series:
    """True above the 99.5th percentile of the values inside ``mask``. Blank outside it."""
    result = pd.Series(pd.NA, index=values.index, dtype="boolean")
    inside = values[mask].astype("float64")
    result[mask] = (inside > inside.quantile(EXTREME_INTERVAL_PERCENTILE)).astype("boolean").where(inside.notna(), pd.NA)
    return result


def _days(later: pd.Series, earlier: pd.Series) -> pd.Series:
    return (later - earlier).dt.days.astype("Int64")


def _group_ids(keys: pd.Series, prefix: str) -> pd.Series:
    codes, _ = pd.factorize(keys, use_na_sentinel=True)
    return pd.array([f"{prefix}-{code + 1:06d}" if code >= 0 else pd.NA for code in codes], dtype="string")


def build_dim_functional_location(funcloc: pd.DataFrame, bom: pd.DataFrame, notif: pd.DataFrame, mitem: pd.DataFrame, build: _Build) -> pd.DataFrame:
    if funcloc["functional_location"].duplicated().any():
        raise ConformError("Functional location is not unique in the FuncLoc list")
    dim = funcloc.copy()
    code = dim["functional_location"]
    dim["fl_desc_clean"] = _clean(dim["fl_desc"])
    dim["fl_prefix"] = code.str.split("_", n=1).str[0]
    dim["fl_body"] = code.str.split("_", n=1).str[1]
    dim["is_system_level"] = code.str.startswith("SITE").astype("boolean")
    dim["criticality_missing"] = dim["criticality"].isna().astype("boolean")
    dim["criticality_missing_reason"] = pd.array(
        ["system_level_row" if missing and site else (pd.NA if not missing else "unexplained")
         for missing, site in zip(dim["criticality_missing"], dim["is_system_level"])], dtype="string")
    dim["fl_has_bom"] = code.isin(bom["functional_location"]).astype("boolean")
    dim["fl_has_notification"] = code.isin(notif["functional_location"]).astype("boolean")
    dim["fl_has_plan"] = code.isin(mitem["functional_location"]).astype("boolean")
    dim["fl_in_all_three"] = dim["fl_has_bom"] & dim["fl_has_notification"] & dim["fl_has_plan"]
    build.record("dim_functional_location", "Spec 3.6, F-02, F-04, F-05", "A/C", "One row per location. Blank criticality kept and flagged. Prefix and body are text labels only. No parent links inferred.",
                 "fl_desc_clean;fl_prefix;fl_body;is_system_level;criticality_missing;criticality_missing_reason;fl_has_bom;fl_has_notification;fl_has_plan;fl_in_all_three", len(funcloc), len(dim))
    return dim


def build_dim_material(bom_labelled: pd.DataFrame, movement: pd.DataFrame, prpo: pd.DataFrame, dim_fl: pd.DataFrame, build: _Build) -> pd.DataFrame:
    """One row per material. Allowed only because BoM attributes never differ within a material (Spec B-02, S05)."""
    conflicts = {a: int(n) for a, n in bom_labelled.groupby("material_no")[list(BOM_MATERIAL_ATTRIBUTES)].nunique(dropna=False).gt(1).sum().items() if n}
    if conflicts:
        raise ConformError(f"BoM attributes differ within a material, so dim_material would be wrong: {conflicts}")
    ordered = bom_labelled.sort_values("source_row", kind="stable")
    first = ordered.drop_duplicates("material_no")
    dim = first[["material_no", *BOM_MATERIAL_ATTRIBUTES, "source_file", "source_sheet", "source_row", "spec_version"]].rename(
        columns={"source_row": "first_source_row"}).reset_index(drop=True)
    dim["material_desc_clean"] = _clean(dim["material_desc"])
    dim["material_prefix"] = dim["material_no"].str[:4]
    pairs = ordered.drop_duplicates(["functional_location", "material_no"])[["functional_location", "material_no"]]
    pairs = audited_lookup(pairs, dim_fl[["functional_location", "criticality"]], "functional_location", "bridge_fl_material -> dim_functional_location (criticality count)",
                           build.joins, require_all_matched=True)
    critical = pairs["criticality"].astype("string").fillna("null")
    counts = pd.crosstab(pairs["material_no"], critical)
    for code in (*CRITICALITY_CODES, "null"):
        counts[code] = counts[code] if code in counts else 0
    dim["n_bom_rows"] = dim["material_no"].map(ordered.groupby("material_no").size()).astype("Int64")
    dim["n_bom_locations"] = dim["material_no"].map(pairs.groupby("material_no").size()).astype("Int64")
    for code in (*CRITICALITY_CODES, "null"):
        dim[f"n_fl_crit_{code}"] = dim["material_no"].map(counts[code]).astype("Int64")
    # Raw comparisons only. Min, Max and Stock are undefined and undated (DEF-02, DEF-12).
    dim["stock_eq_zero"] = (dim["stock"] == 0).astype("boolean")
    dim["stock_lt_min"] = (dim["stock"] < dim["min_qty"]).astype("boolean")
    dim["stock_gt_max"] = (dim["stock"] > dim["max_qty"]).astype("boolean")
    dim["min_eq_max"] = (dim["min_qty"] == dim["max_qty"]).astype("boolean")
    mrp = dim["mrp_type"].astype("string")
    dim["nonstock_with_stock"] = ((mrp == "Non Stock") & (dim["stock"] > 0)).astype("boolean")
    dim["stockitem_min_max_zero"] = ((mrp == "Stock Item") & (dim["min_qty"] == 0) & (dim["max_qty"] == 0)).astype("boolean")
    dim["flag_fraction_on_count_unit"] = ((dim["stock"] % 1 != 0) & dim["unit"].astype("string").isin(COUNT_UNITS)).astype("boolean")
    shared = dim.groupby("material_desc_clean")["material_no"].transform("nunique") > 1
    dim["desc_shared_group_id"] = _group_ids(dim["material_desc_clean"].where(shared), "DESC")
    dim["is_issued"] = dim["material_no"].isin(movement["material_no"]).astype("boolean")
    dim["is_procured"] = dim["material_no"].isin(prpo["material_no"]).astype("boolean")
    # One row per material, so the robust z never applies. The Spec's within-unit fence does.
    dim = dim.rename(columns={"first_source_row": "source_row"})
    added = build.flag_outliers(dim, "dim_material", "stock", "stock", {"one_row_per_material": pd.Series(True, index=dim.index)}, "material_no", "unit")
    dim = dim.rename(columns={"source_row": "first_source_row"})
    build.record("dim_material", "Spec 3.2 S05-S11, B-02, B-05 to B-08", "A/C", "One row per material, after confirming attributes never differ. Comparisons are raw, with no status label. Descriptions shared across codes are flagged, never merged.",
                 "material_desc_clean;material_prefix;n_bom_rows;n_bom_locations;n_fl_crit_*;stock_eq_zero;stock_lt_min;stock_gt_max;min_eq_max;nonstock_with_stock;stockitem_min_max_zero;flag_fraction_on_count_unit;desc_shared_group_id;is_issued;is_procured;" + ";".join(added),
                 len(bom_labelled), len(dim))
    return dim


def build_dim_supplier(prpo: pd.DataFrame, build: _Build) -> pd.DataFrame:
    grouped = prpo.astype({"currency": "string"}).groupby("supplier_code")
    for column, label in (("supplier_name", "name"), ("currency", "currency")):
        repeats = int((grouped[column].nunique() > 1).sum())
        if repeats:
            raise ConformError(f"{repeats} suppliers have more than one {label}")
    dim = prpo.astype({"currency": "string"}).sort_values("source_row", kind="stable").drop_duplicates("supplier_code")[["supplier_code", "supplier_name", "currency"]].reset_index(drop=True)
    dim["supplier_name_clean"] = _clean(dim["supplier_name"])
    dim["is_non_idr_currency"] = (dim["currency"] != "IDR").astype("boolean")
    build.record("dim_supplier", "Spec 3.1 S07, COR-02, P-12", "A", "One row per supplier code, after confirming one name and one currency per code. No amounts or rankings. Non-IDR currency is not treated as proof of a foreign supplier.",
                 "supplier_name_clean;is_non_idr_currency", len(prpo), len(dim))
    return dim


def build_bridge_fl_material(bom_labelled: pd.DataFrame, dim_material: pd.DataFrame, build: _Build) -> pd.DataFrame:
    keys = ["functional_location", "material_no"]
    first = bom_labelled[bom_labelled["occurrence_rank"] == 1]
    if first.duplicated(keys).any():
        raise ConformError("A BoM location and material pair has differing content, so a pair table would lose values")
    row_lists = bom_labelled.groupby("content_group_id")["source_row"].agg(lambda rows: ";".join(str(int(r)) for r in sorted(rows)))
    bridge = first[[*keys, "installed_qty", "unit", "content_group_id", "occurrence_count", "source_file", "source_sheet", "source_row", "row_hash", "spec_version"]].reset_index(drop=True)
    bridge["all_source_rows"] = pd.array(bridge["content_group_id"].map(row_lists).tolist(), dtype="string")
    bridge["flag_non_integer_installed_qty"] = (bridge["installed_qty"] % 1 != 0).astype("boolean")
    bridge["flag_fraction_on_count_unit"] = (bridge["flag_non_integer_installed_qty"] & bridge["unit"].astype("string").isin(COUNT_UNITS)).astype("boolean")
    bridge = audited_lookup(bridge, dim_material[["material_no"]], "material_no", "bridge_fl_material -> dim_material", build.joins, require_all_matched=True)
    added = build.flag_outliers(bridge, "bridge_fl_material", "installed_qty", "installed_qty", {"distinct_pairs": pd.Series(True, index=bridge.index)}, "material_no", "unit")
    build.record("bridge_fl_material", "Spec 3.2 S03-S04, S10, B-01, COR-07", "B", "One row per location and material pair. Exact copies are represented by all_source_rows and occurrence_count. Installed Qty is identical across copies.",
                 "all_source_rows;flag_non_integer_installed_qty;flag_fraction_on_count_unit;" + ";".join(added), len(bom_labelled), len(bridge))
    return bridge


def build_bridge_order_notification(notif: pd.DataFrame, movement: pd.DataFrame, build: _Build) -> pd.DataFrame:
    linked = notif[notif["order_no"].notna()]
    bridge = linked[["order_no", "notification", "functional_location", "notification_date", "source_row"]].reset_index(drop=True)
    per_order = bridge.groupby("order_no")
    bridge["n_notifications_for_order"] = per_order["notification"].transform("nunique").astype("Int64")
    bridge["n_locations_for_order"] = per_order["functional_location"].transform("nunique").astype("Int64")
    bridge["order_shared"] = (bridge["n_notifications_for_order"] > 1).astype("boolean")
    same = bridge["n_locations_for_order"] == 1
    bridge["shared_order_same_fl"] = same.astype("boolean").where(bridge["order_shared"], pd.NA)
    bridge["has_issue"] = bridge["order_no"].isin(movement["order_no"]).astype("boolean")
    build.record("bridge_order_notification", "Spec 3.4 S07, N-02", "A/C", "One row per order and notification, from notifications with an order. No allocation rule is applied to shared orders.",
                 "n_notifications_for_order;n_locations_for_order;order_shared;shared_order_same_fl;has_issue", len(notif), len(bridge))
    return bridge


def _check_against_material(fact: pd.DataFrame, dim_material: pd.DataFrame, name: str, build: _Build) -> pd.DataFrame:
    """Compare unit and trimmed description with the material dimension. Fact values are not replaced."""
    lookup = dim_material[["material_no", "unit", "material_desc_clean", "desc_shared_group_id"]].rename(
        columns={"unit": "_dim_unit", "material_desc_clean": "_dim_desc"}).astype({"_dim_unit": "string"})
    merged = audited_lookup(fact, lookup, "material_no", f"{name} -> dim_material", build.joins, require_all_matched=True)
    merged["flag_unit_mismatch"] = (merged["unit"].astype("string") != merged["_dim_unit"]).astype("boolean")
    merged["flag_desc_mismatch"] = (merged["material_desc_clean"] != merged["_dim_desc"]).astype("boolean")
    return merged.drop(columns=["_dim_unit", "_dim_desc"])


def build_fact_prpo_line(prpo_labelled: pd.DataFrame, dim_material: pd.DataFrame, dim_supplier: pd.DataFrame, build: _Build) -> pd.DataFrame:
    fact = prpo_labelled.sort_values("source_row", kind="stable").reset_index(drop=True)
    in_distinct = fact["occurrence_rank"] == 1
    views = {ORIGINAL: pd.Series(True, index=fact.index), DISTINCT: in_distinct}
    fact["in_exact_distinct_rows"] = in_distinct.astype("boolean")
    fact["is_repeat_occurrence"] = (~in_distinct).astype("boolean")
    fact["material_desc_clean"] = _clean(fact["material_desc"])
    fact = _check_against_material(fact, dim_material, "fact_prpo_line", build)
    supplier = audited_lookup(fact[["supplier_code"]], dim_supplier[["supplier_code", "is_non_idr_currency"]], "supplier_code", "fact_prpo_line -> dim_supplier", build.joins, require_all_matched=True)
    fact["requested_interval_days"] = _days(fact["pr_delivery_date"], fact["pr_date"])
    fact["promised_interval_days"] = _days(fact["po_delivery_date"], fact["pr_date"])
    fact["promise_gap_days"] = _days(fact["po_delivery_date"], fact["pr_delivery_date"])
    fact["flag_req_before_pr"] = (fact["requested_interval_days"] < 0).astype("boolean")
    fact["flag_promise_before_pr"] = (fact["promised_interval_days"] < 0).astype("boolean")
    cutoff = pd.Timestamp(DATA_CUTOFF)
    fact["flag_future_requested_date"] = (fact["pr_delivery_date"] > cutoff).astype("boolean")
    fact["flag_future_promised_date"] = (fact["po_delivery_date"] > cutoff).astype("boolean")
    fact["flag_future_date"] = fact["flag_future_requested_date"] | fact["flag_future_promised_date"]
    fact["in_idr_scope"] = (fact["currency"].astype("string") == "IDR").astype("boolean")
    fact["is_non_idr_supplier"] = supplier["is_non_idr_currency"].to_numpy()
    fact["pr_prefix"] = fact["purchase_requisition"].str[:2]
    fact["po_prefix"] = fact["purchase_order"].str[:2]
    fact["pr_month"] = _month_start(fact["pr_date"])
    distinct_rows = fact[in_distinct]
    for column, name in (("pr_type", "rare_pr_type"), ("purchasing_group", "rare_purchasing_group")):
        sizes = distinct_rows[column].astype("string").value_counts()
        fact[name] = fact[column].astype("string").map(sizes).lt(RARE_CATEGORY_DISTINCT_ROWS).astype("boolean")
    added = []
    for view, mask in views.items():
        column = f"flag_extreme_interval__{view}"
        fact[column] = _extreme(fact["requested_interval_days"], mask) | _extreme(fact["promised_interval_days"], mask)
        added.append(column)
    fact["_all"] = pd.array(["all"] * len(fact), dtype="string")
    added += build.flag_outliers(fact, "fact_prpo_line", "pr_quantity", "pr_quantity", views, "material_no", "unit")
    for measure, name in (("requested_interval_days", "requested_interval"), ("promised_interval_days", "promised_interval"), ("promise_gap_days", "promise_gap")):
        added += build.flag_outliers(fact, "fact_prpo_line", measure, name, views, "material_no", "_all")
    fact = fact.drop(columns="_all")
    build.record("fact_prpo_line", "Spec 3.1 S03-S04, S09-S15, COR-09", "A/C", "All source rows kept. in_exact_distinct_rows selects the sensitivity view. Population-based flags are held per view. No unit amount is derived (DEF-05).",
                 "in_exact_distinct_rows;is_repeat_occurrence;material_desc_clean;flag_unit_mismatch;flag_desc_mismatch;desc_shared_group_id;requested_interval_days;promised_interval_days;promise_gap_days;flag_req_before_pr;flag_promise_before_pr;flag_future_*;in_idr_scope;is_non_idr_supplier;pr_prefix;po_prefix;pr_month;rare_pr_type;rare_purchasing_group;" + ";".join(added),
                 len(prpo_labelled), len(fact))
    return fact


def _attribution(fact_rows: pd.DataFrame, bridge_order: pd.DataFrame, bridge_material: pd.DataFrame) -> pd.DataFrame:
    """Which functional location an issue row can be linked to through its order. Nothing is allocated."""
    candidates = fact_rows[["source_row", "order_no", "material_no"]].merge(
        bridge_order[["order_no", "functional_location"]], on="order_no", how="inner")
    pairs = set(zip(bridge_material["functional_location"], bridge_material["material_no"]))
    candidates["pair_in_bom"] = [pair in pairs for pair in zip(candidates["functional_location"], candidates["material_no"])]
    summary = candidates.groupby("source_row").agg(n_candidate_locations=("functional_location", "nunique"),
                                                   n_candidate_locations_with_material=("pair_in_bom", "sum"),
                                                   _location=("functional_location", "first"))
    return summary


def build_fact_issue(movement_labelled: pd.DataFrame, bridge_order: pd.DataFrame, bridge_material: pd.DataFrame, dim_material: pd.DataFrame, build: _Build) -> pd.DataFrame:
    fact = movement_labelled.sort_values("source_row", kind="stable").reset_index(drop=True)
    in_distinct = fact["occurrence_rank"] == 1
    views = {ALL_ROWS: pd.Series(True, index=fact.index), DISTINCT: in_distinct}
    fact["in_exact_distinct_rows"] = in_distinct.astype("boolean")
    fact["is_repeat_occurrence"] = (~in_distinct).astype("boolean")
    fact["material_desc_clean"] = _clean(fact["material_desc"])
    fact = _check_against_material(fact, dim_material, "fact_issue", build)
    keys = ["posting_date", "material_no", "order_no"]
    same_key = fact.groupby(keys)
    fact["same_key_group_size"] = same_key["source_row"].transform("size").astype("Int64")
    partial = same_key["quantity"].transform("nunique") > 1
    fact["is_partial_dup_group"] = partial.astype("boolean")
    fact["partial_dup_group_id"] = _group_ids(fact["posting_date"].dt.strftime("%Y%m%d").where(partial).astype("string") + "|" + fact["material_no"] + "|" + fact["order_no"], "MOVEPART")
    fact["order_prefix"] = fact["order_no"].str[:3]
    fact["posting_month"] = _month_start(fact["posting_date"])
    fact["posting_week"] = (fact["posting_date"] - pd.to_timedelta(fact["posting_date"].dt.weekday, unit="D")).astype("datetime64[ns]")
    fact["has_notification"] = fact["order_no"].isin(bridge_order["order_no"]).astype("boolean")
    shared_orders = set(bridge_order.loc[bridge_order["order_shared"].fillna(False).astype(bool), "order_no"])
    fact["order_shared"] = fact["order_no"].isin(shared_orders).astype("boolean")
    summary = _attribution(fact, bridge_order, bridge_material)
    locations = fact["source_row"].map(summary["n_candidate_locations"])
    fact["fl_attribution"] = pd.array(["none" if pd.isna(n) else ("unique" if n == 1 else "ambiguous") for n in locations], dtype="string")
    fact["attributed_functional_location"] = fact["source_row"].map(summary["_location"]).astype("string").where(fact["fl_attribution"] == "unique", pd.NA)
    fact["n_candidate_locations_with_material"] = fact["source_row"].map(summary["n_candidate_locations_with_material"]).astype("Int64")
    fact["issued_material_in_fl_bom"] = (fact["n_candidate_locations_with_material"] > 0).astype("boolean")
    added = build.flag_outliers(fact, "fact_issue", "quantity", "quantity", views, "material_no", "unit")
    build.record("fact_issue", "Spec 3.3 S02-S09, R7, R8, R10, A-05", "A/C", "All source rows kept. No duplicate policy is applied (A-05). Location is filled only when the order leads to exactly one location. Shared orders stay ambiguous and are never allocated.",
                 "in_exact_distinct_rows;is_repeat_occurrence;material_desc_clean;flag_unit_mismatch;flag_desc_mismatch;desc_shared_group_id;same_key_group_size;is_partial_dup_group;partial_dup_group_id;order_prefix;posting_month;posting_week;has_notification;order_shared;fl_attribution;attributed_functional_location;n_candidate_locations_with_material;issued_material_in_fl_bom;" + ";".join(added),
                 len(movement_labelled), len(fact))
    return fact


def build_fact_notification(notif: pd.DataFrame, bridge_order: pd.DataFrame, dim_fl: pd.DataFrame, movement: pd.DataFrame, build: _Build) -> pd.DataFrame:
    fact = notif.sort_values("source_row", kind="stable").reset_index(drop=True)
    status = fact["status"].astype("string")
    cutoff = pd.Timestamp(DATA_CUTOFF)
    fact["description_clean"] = _clean(fact["description"])
    fact["desc_ref_code"] = fact["description"].str.extract(REF_CODE_PATTERN, expand=False).astype("string")
    fact["desc_first_word"] = fact["description_clean"].str.split().str[0].str.upper().astype("string")
    fact["is_open"] = (status == "In Progress").astype("boolean")
    fact["is_censored"] = fact["is_open"]
    fact["order_missing"] = fact["order_no"].isna().astype("boolean")
    shared = bridge_order.drop_duplicates("order_no").set_index("order_no")
    fact["order_shared"] = fact["order_no"].map(shared["order_shared"]).astype("boolean").fillna(False)
    fact["shared_order_same_fl"] = fact["order_no"].map(shared["shared_order_same_fl"]).astype("boolean")
    fact["has_issue"] = fact["order_no"].isin(movement["order_no"]).astype("boolean")
    fact["flag_reqstart_before_notif"] = (fact["required_start"] < fact["notification_date"]).astype("boolean")
    fact["flag_created_differs"] = (fact["created_on"] != fact["notification_date"]).astype("boolean")
    fact["completed_late"] = (fact["completion_date"] > fact["required_end"]).astype("boolean").where(fact["completion_date"].notna(), pd.NA)
    fact["flag_future_date"] = ((fact["required_start"] > cutoff) | (fact["required_end"] > cutoff)).astype("boolean")
    fact["first_month_flag"] = (fact["notification_date"].dt.strftime("%Y-%m") == "2025-05").astype("boolean")
    fact["days_to_complete"] = _days(fact["completion_date"], fact["notification_date"])
    fact["days_open_at_cutoff"] = _days(pd.Series(cutoff, index=fact.index), fact["notification_date"]).where(fact["is_open"].fillna(False).astype(bool), pd.NA)
    fact["required_window_days"] = _days(fact["required_end"], fact["required_start"])
    fact["days_late_vs_required"] = _days(fact["completion_date"], fact["required_end"])
    fact["flag_extreme_interval"] = _extreme(fact["days_to_complete"], pd.Series(True, index=fact.index))
    keys = ["functional_location", "description", "notification_date"]
    repeat = fact.duplicated(keys, keep=False)
    fact["is_partial_dup_group"] = repeat.astype("boolean")
    fact["partial_dup_group_id"] = _group_ids(fact["functional_location"].where(repeat) + "|" + fact["description"] + "|" + fact["notification_date"].dt.strftime("%Y%m%d"), "NOTIFPART")
    attributes = dim_fl[["functional_location", "criticality", "fl_prefix", "is_system_level"]].rename(columns={"criticality": "fl_criticality"})
    fact = audited_lookup(fact, attributes, "functional_location", "fact_notification -> dim_functional_location", build.joins, require_all_matched=True)
    build.record("fact_notification", "Spec 3.4 S04-S11, N-01 to N-05, N-08 to N-10", "A/B/C", "All source rows kept. Blank completion dates and orders are never filled. Open records are censored at the assumed cutoff (A-01). Notifications are not treated as failures (DEF-09). No priority rank.",
                 "description_clean;desc_ref_code;desc_first_word;is_open;is_censored;order_missing;order_shared;shared_order_same_fl;has_issue;flag_reqstart_before_notif;flag_created_differs;completed_late;flag_future_date;first_month_flag;days_to_complete;days_open_at_cutoff;required_window_days;days_late_vs_required;flag_extreme_interval;is_partial_dup_group;partial_dup_group_id;fl_criticality;fl_prefix;is_system_level",
                 len(notif), len(fact))
    return fact


def build_fact_plan_item(mitem: pd.DataFrame, map_cycle: pd.DataFrame, dim_fl: pd.DataFrame, build: _Build) -> pd.DataFrame:
    fact = mitem.sort_values("source_row", kind="stable").reset_index(drop=True)
    fact["fl_desc_clean"] = _clean(fact["fl_desc"])
    fact["_cycle"] = fact["cycle_desc"].astype("string")
    lookup = map_cycle[["cycle_desc", "interval_value_proposed", "interval_unit_proposed", "interval_days_proposed", "mapping_basis"]].rename(columns={"cycle_desc": "_cycle"})
    fact = audited_lookup(fact, lookup, "_cycle", "fact_plan_item -> map_cycle", build.joins).drop(columns="_cycle")
    fact["flag_cycle_unmapped"] = fact["interval_unit_proposed"].isna().astype("boolean")
    fact["flag_future_cycle_start"] = (fact["start_of_cycle"] > pd.Timestamp(DATA_CUTOFF)).astype("boolean")
    fact["start_day_is_first"] = (fact["start_of_cycle"].dt.day == 1).astype("boolean")
    plans = fact.groupby("maintenance_plan")
    fact["n_items_in_plan"] = plans["maintenance_item"].transform("nunique").astype("Int64")
    fact["n_fl_in_plan"] = plans["functional_location"].transform("nunique").astype("Int64")
    fact["plan_multi_fl"] = (fact["n_fl_in_plan"] > 1).astype("boolean")
    attributes = dim_fl[["functional_location", "fl_prefix", "is_system_level"]]
    fact = audited_lookup(fact, attributes, "functional_location", "fact_plan_item -> dim_functional_location", build.joins, require_all_matched=True)
    build.record("fact_plan_item", "Spec 3.5 S03-S06, S09, I-01, I-02, COR-12", "A/B", "All source rows kept. Interval columns are proposed readings that need DEF-10. Future starts use the single cutoff. No due dates are projected (DEF-11).",
                 "fl_desc_clean;interval_value_proposed;interval_unit_proposed;interval_days_proposed;mapping_basis;flag_cycle_unmapped;flag_future_cycle_start;start_day_is_first;n_items_in_plan;n_fl_in_plan;plan_multi_fl;fl_prefix;is_system_level",
                 len(mitem), len(fact))
    return fact


GRAINS = {
    "dim_functional_location": "One functional location", "dim_material": "One material, from BoM attributes", "dim_supplier": "One supplier code",
    "map_cycle": "One cycle spelling. Proposed mapping, requires DEF-10", "bridge_fl_material": "One location and material pair",
    "bridge_order_notification": "One order and notification pair", "fact_prpo_line": "One PR PO source row, across both views",
    "fact_issue": "One Movement source row", "fact_notification": "One notification", "fact_plan_item": "One maintenance item",
}


def build_conformed(tables: dict[str, pd.DataFrame], labelled: dict[str, pd.DataFrame]) -> dict:
    """Build all conformed tables. Returns the tables and the audit trail of the build."""
    build = _Build()
    funcloc, bom, notif, mitem, movement, prpo = (tables[k] for k in ("funcloc", "bom", "notif", "mitem", "movement", "prpo"))
    map_cycle = build_map_cycle()
    build.record("map_cycle", "Spec Appendix A, I-01, DEF-10", "B", "Proposed readings of the 28 spellings. Not confirmed.", "all", 28, len(map_cycle))
    dim_fl = build_dim_functional_location(funcloc, bom, notif, mitem, build)
    dim_material = build_dim_material(labelled["bom"], movement, prpo, dim_fl, build)
    dim_supplier = build_dim_supplier(prpo, build)
    bridge_material = build_bridge_fl_material(labelled["bom"], dim_material, build)
    bridge_order = build_bridge_order_notification(notif, movement, build)
    conformed = {
        "dim_functional_location": dim_fl, "dim_material": dim_material, "dim_supplier": dim_supplier, "map_cycle": map_cycle,
        "bridge_fl_material": bridge_material, "bridge_order_notification": bridge_order,
        "fact_prpo_line": build_fact_prpo_line(labelled["prpo"], dim_material, dim_supplier, build),
        "fact_issue": build_fact_issue(labelled["movement"], bridge_order, bridge_material, dim_material, build),
        "fact_notification": build_fact_notification(notif, bridge_order, dim_fl, movement, build),
        "fact_plan_item": build_fact_plan_item(mitem, map_cycle, dim_fl, build),
    }
    outliers = pd.concat(build.outlier_rows, ignore_index=True) if build.outlier_rows else pd.DataFrame()
    return {"tables": {name: normalise_types(frame) for name, frame in conformed.items()},
            "join_audit": pd.DataFrame(build.joins), "transformation_log": pd.DataFrame(build.log),
            "outliers": outliers, "outlier_summary": pd.DataFrame(build.outlier_summary)}


def normalise_types(frame: pd.DataFrame) -> pd.DataFrame:
    """Use one nullable type per kind, so a table reloads from CSV to the same types."""
    result = frame.copy()
    for column in result.columns:
        kind = result[column].dtype
        if isinstance(kind, pd.CategoricalDtype) or str(kind) in ("string", "Int64", "Float64", "boolean", "datetime64[ns]"):
            continue
        if pd.api.types.is_bool_dtype(kind):
            result[column] = result[column].astype("boolean")
        elif pd.api.types.is_integer_dtype(kind):
            result[column] = result[column].astype("Int64")
        elif pd.api.types.is_float_dtype(kind):
            result[column] = result[column].astype("Float64")
        elif pd.api.types.is_datetime64_any_dtype(kind):
            result[column] = result[column].astype("datetime64[ns]")
        else:
            result[column] = result[column].astype("string")
    return result


def type_map(frame: pd.DataFrame) -> dict[str, str]:
    return {column: "category" if isinstance(frame[column].dtype, pd.CategoricalDtype) else str(frame[column].dtype) for column in frame.columns}


def read_conformed(path, types: dict[str, str]) -> pd.DataFrame:
    """Load a conformed CSV with its recorded types. A plain read_csv damages identifiers."""
    dates = [c for c, kind in types.items() if kind.startswith("datetime")]
    dtypes = {c: ("string" if kind == "category" else kind) for c, kind in types.items() if not kind.startswith("datetime")}
    frame = pd.read_csv(path, dtype=dtypes, keep_default_na=False, na_values=[""], parse_dates=dates, encoding="utf-8")
    for column, kind in types.items():
        if kind == "category":
            frame[column] = frame[column].astype("category")
        elif kind.startswith("datetime"):
            frame[column] = frame[column].astype("datetime64[ns]")
    return frame
