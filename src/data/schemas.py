"""Schema definitions for the six source workbooks.

Standard names follow CALIBER_DATA_DICTIONARY.md Section 7. A ``kind`` controls
how a column is read and stored:

    identifier  text code, never used in arithmetic; read as a string
    category    closed set of codes, stored as an unordered category
    text        free or semi-structured text, kept verbatim
    integer     whole-number measure
    float       decimal measure
    date        date with no time part
"""
from typing import NamedTuple


class ColumnSpec(NamedTuple):
    source: str
    standard: str
    kind: str
    id_pattern: str | None = None  # full-match regex for identifier integrity


class DatasetSpec(NamedTuple):
    key: str
    name: str
    file_name: str
    sheet: str
    columns: tuple[ColumnSpec, ...]
    documented_grain: str

    @property
    def source_columns(self) -> list[str]:
        return [c.source for c in self.columns]

    @property
    def standard_columns(self) -> list[str]:
        return [c.standard for c in self.columns]

    def by_kind(self, *kinds: str) -> list[str]:
        return [c.standard for c in self.columns if c.kind in kinds]


LINEAGE_COLUMNS = ("source_file", "source_sheet", "source_row", "row_hash", "spec_version")

TEN = r"\d{10}"
TWELVE = r"\d{12}"
MULTIPLE_OF_10 = r"\d*0"
FUNC_LOC = r"\S(.*\S)?"

PRPO = DatasetSpec("prpo", "PR PO", "PR PO.xlsx", "Data", (
    ColumnSpec("PR-Type", "pr_type", "category"),
    ColumnSpec("Purchase Requisition", "purchase_requisition", "identifier", TEN),
    ColumnSpec("PR-Item", "pr_item", "identifier", MULTIPLE_OF_10),
    ColumnSpec("PR-Date", "pr_date", "date"),
    ColumnSpec("PR-Material", "material_no", "identifier", TEN),
    ColumnSpec("PR-Material Desc", "material_desc", "text"),
    ColumnSpec("PR-Quantity", "pr_quantity", "integer"),
    ColumnSpec("PR-UoM", "unit", "category"),
    ColumnSpec("PR-Delivery Date", "pr_delivery_date", "date"),
    ColumnSpec("PR-Plant", "plant", "identifier", r"\d{4}"),
    ColumnSpec("PR-Purchasing Group", "purchasing_group", "category"),
    ColumnSpec("Purchase Order", "purchase_order", "identifier", TEN),
    ColumnSpec("PO-Item", "po_item", "identifier", MULTIPLE_OF_10),
    ColumnSpec("PO-Supplier Code", "supplier_code", "identifier", r"\d{6}"),
    ColumnSpec("PO-Supplier Name", "supplier_name", "text"),
    ColumnSpec("PO-Item Amount", "po_item_amount", "float"),
    ColumnSpec("PO-Currency", "currency", "category"),
    ColumnSpec("PO-Delivery Date", "po_delivery_date", "date"),
), "One PR item linked to one PO item")

MOVEMENT = DatasetSpec("movement", "Movement Material", "Movement Material.xlsx", "Data", (
    ColumnSpec("Posting Date", "posting_date", "date"),
    ColumnSpec("Movement Type", "movement_type", "category"),
    ColumnSpec("Material Number", "material_no", "identifier", TEN),
    ColumnSpec("Material Descriptions", "material_desc", "text"),
    ColumnSpec("Quantity", "quantity", "integer"),
    ColumnSpec("Base Unit", "unit", "category"),
    ColumnSpec("Order", "order_no", "identifier", TWELVE),
), "One material issue transaction")

NOTIF = DatasetSpec("notif", "Notif History", "Notif History.xlsx", "Data", (
    ColumnSpec("Notification Date", "notification_date", "date"),
    ColumnSpec("Notification", "notification", "identifier", TWELVE),
    ColumnSpec("Notification Type", "notification_type", "category"),
    ColumnSpec("Order", "order_no", "identifier", TWELVE),
    ColumnSpec("Priority", "notif_priority", "category"),
    ColumnSpec("Functional Location", "functional_location", "identifier", FUNC_LOC),
    ColumnSpec("Description", "description", "text"),
    ColumnSpec("Created On", "created_on", "date"),
    ColumnSpec("Required Start", "required_start", "date"),
    ColumnSpec("Required End", "required_end", "date"),
    ColumnSpec("Completion by Date", "completion_date", "date"),
    ColumnSpec("Status", "status", "category"),
), "One maintenance notification")

MITEM = DatasetSpec("mitem", "Mitem & Mplan", "Mitem & Mplan.xlsx", "Data", (
    ColumnSpec("Functional Location", "functional_location", "identifier", FUNC_LOC),
    ColumnSpec("FunctLocDescrip.", "fl_desc", "text"),
    ColumnSpec("ABC Indicator", "criticality", "category"),
    ColumnSpec("Maintenance Plan", "maintenance_plan", "identifier", TWELVE),
    ColumnSpec("Maintenance Item", "maintenance_item", "identifier", r"\d{5,6}"),
    ColumnSpec("Maint. item text", "item_text", "category"),
    ColumnSpec("Priority", "plan_priority", "category"),
    ColumnSpec("Cycle Descriptions", "cycle_desc", "category"),
    ColumnSpec("Start of cycle", "start_of_cycle", "date"),
), "One maintenance item within a maintenance plan")

BOM = DatasetSpec("bom", "BoM", "BoM.xlsx", "Data", (
    ColumnSpec("Functional Loc.", "functional_location", "identifier", FUNC_LOC),
    ColumnSpec("Material No", "material_no", "identifier", TEN),
    ColumnSpec("Material Desc.", "material_desc", "text"),
    ColumnSpec("Installed Qty", "installed_qty", "float"),
    ColumnSpec("Unit", "unit", "category"),
    ColumnSpec("Min.Qty", "min_qty", "integer"),
    ColumnSpec("Max.Qty", "max_qty", "integer"),
    ColumnSpec("Stock", "stock", "float"),
    ColumnSpec("MRP Type", "mrp_type", "category"),
), "One material assigned to one FuncLoc")

FUNCLOC = DatasetSpec("funcloc", "FuncLoc list", "FuncLoc list.xlsx", "Data", (
    ColumnSpec("Functional Location", "functional_location", "identifier", FUNC_LOC),
    ColumnSpec("FunctLocDescrip.", "fl_desc", "text"),
    ColumnSpec("FuncLoc Criticallity", "criticality", "category"),
), "One functional location (FuncLoc / sub-FuncLoc / system)")

DATASETS: dict[str, DatasetSpec] = {s.key: s for s in (PRPO, MOVEMENT, NOTIF, MITEM, BOM, FUNCLOC)}

# Numeric columns are summarised within these groups only, because quantities in
# different units and amounts in different currencies cannot be compared.
NUMERIC_GROUP_BY = {
    "prpo": {"pr_quantity": "unit", "po_item_amount": "currency"},
    "movement": {"quantity": "unit"},
    "bom": {"installed_qty": "unit", "min_qty": "unit", "max_qty": "unit", "stock": "unit"},
}

# BoM values repeated on every row of a material; also profiled at one row per material.
BOM_MATERIAL_ATTRIBUTES = ("material_desc", "unit", "min_qty", "max_qty", "stock", "mrp_type")

# Exact-duplicate metadata settings. key_sets are the business keys compared
# between duplicate groups; measures are shown per occurrence and in total.
DUPLICATE_SETTINGS = {
    "prpo": {
        "id_prefix": "PRPO",
        "key_sets": (("purchase_requisition", "pr_item"), ("purchase_order", "po_item")),
        "measures": ("pr_quantity", "po_item_amount"),
        "context": ("material_no", "unit", "currency"),
    },
    "bom": {
        "id_prefix": "BOM",
        "key_sets": (("functional_location", "material_no"),),
        "measures": ("installed_qty",),
        "context": ("unit",),
    },
    "movement": {
        "id_prefix": "MOVE",
        "key_sets": (("posting_date", "material_no", "order_no"),),
        "measures": ("quantity",),
        "context": ("unit",),
    },
    "notif": {"id_prefix": "NOTIF", "key_sets": (("notification",),), "measures": (), "context": ()},
    "mitem": {"id_prefix": "MITEM", "key_sets": (("maintenance_item",),), "measures": (), "context": ()},
    "funcloc": {"id_prefix": "FL", "key_sets": (("functional_location",),), "measures": (), "context": ()},
}

# Relationships as drawn in the Data Context & Relationship Diagram. Used only to
# label candidate foreign keys; the observed values decide what is reported.
DIAGRAM_RELATIONS = (
    ("funcloc.functional_location", "bom.functional_location", "1:N"),
    ("funcloc.functional_location", "notif.functional_location", "1:N"),
    ("funcloc.functional_location", "mitem.functional_location", "1:N"),
    ("bom.material_no", "movement.material_no", "unspecified"),
    ("bom.material_no", "prpo.material_no", "unspecified"),
    ("notif.order_no", "movement.order_no", "1:N"),
    ("mitem.functional_location", "bom.functional_location", "indirect"),
)
