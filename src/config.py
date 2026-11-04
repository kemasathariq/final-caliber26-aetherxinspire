"""Central configuration: paths, file locations and analysis parameters.

All paths derive from this file's location, so the project runs from any
checkout without machine-specific paths. Tests pass a temporary ``build_root``
so they never touch the project's generated outputs.
"""
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

SPEC_VERSION = "0.1+corrections-3"
DATA_LABEL = (
    "Source data documented as synthetic (dummy) in the Data Context & "
    "Relationship Diagram; not operational performance."
)
BASELINE_NOTE = (
    "Checksums establish consistency with the audit baseline of 2026-11-04, "
    "not authenticity against organiser-issued checksums."
)

# Assumption A-01 in docs/analysis/ASSUMPTIONS_REGISTER.md. Latest event date
# in the Movement and Notif History files; the extraction date is unconfirmed.
DATA_CUTOFF = "2026-09-30"
# Audit date. Used only to reproduce the Spec D10 count (correction COR-12).
AUDIT_REPORT_DATE = "2026-11-04"

# Outlier flagging (Spec Section 2.8, assumption A-10). Flags only; nothing is removed.
OUTLIER_PARAMETERS = {
    "robust_z_threshold": 3.5,
    "minimum_records_for_robust_z": 5,
    "iqr_fence_multiplier": 3.0,
    "minimum_records_for_iqr_fence": 5,
}
EXTREME_INTERVAL_PERCENTILE = 0.995
RARE_CATEGORY_DISTINCT_ROWS = 30
PERMUTATION_SEED = 42
PERMUTATION_ROUNDS = 200

# Demand marts (M3). The window is the observed Movement range; zero-filling stays inside it.
DEMAND_WINDOW_START = "2025-05"
DEMAND_WINDOW_END = "2026-09"
# Rows between a repeat and the previous occurrence. Describes the evidence; every class is excluded from Scenario B.
COPY_NEAR_GAP_ROWS = 10
# Impact tiers on total material quantity. Analyst thresholds, not business rules (assumption A-14).
DEMAND_IMPACT_MATERIAL_PCT = 10.0
DEMAND_IMPACT_HIGH_PCT = 25.0
LOW_LINE_COUNT = 5
SPARSE_HISTORY_MONTHS = 3
REPEATED_MAXIMUM_MIN_MATERIALS = 5

# Simulation design only. Evidence thresholds decide where resampling would be allowed (assumption S-16).
SIM_MIN_ACTIVE_MONTHS_TO_RESAMPLE_DEMAND = 6
SIM_MIN_LINES_TO_RESAMPLE_LEAD = 10
SIM_HORIZON_START = "2025-05-01"
SIM_HORIZON_END = "2026-09-30"

REFERENCE_DIR = PROJECT_ROOT / "data" / "reference"
AUDIT_BASELINE_FILE = REFERENCE_DIR / "audit_baseline_checksums.json"
EXPECTED_VALUES_FILE = REFERENCE_DIR / "expected_values.json"
EXPECTED_CONFORMED_FILE = REFERENCE_DIR / "expected_values_conformed.json"
EXPECTED_MARTS_FILE = REFERENCE_DIR / "expected_values_marts.json"
EXPECTED_SIM_DESIGN_FILE = REFERENCE_DIR / "expected_values_simulation_design.json"
BOM_RELOCATION_FILE = REFERENCE_DIR / "bom_relocation_record.json"


@dataclass(frozen=True)
class Paths:
    """Locations used by one pipeline run."""

    raw: Path
    manifest: Path
    staged: Path
    prpo_views: Path
    duplicates: Path
    conformed: Path
    processed: Path
    exceptions: Path
    tables: Path
    reports: Path

    def create_output_dirs(self) -> None:
        for folder in (self.manifest.parent, self.staged, self.prpo_views,
                       self.duplicates, self.conformed, self.processed, self.exceptions, self.tables, self.reports):
            folder.mkdir(parents=True, exist_ok=True)


def get_paths(build_root: Path | None = None, raw_dir: Path | None = None) -> Paths:
    """Return run paths. Generated files go under ``build_root``."""
    root = Path(build_root) if build_root else PROJECT_ROOT
    return Paths(
        raw=Path(raw_dir) if raw_dir else PROJECT_ROOT / "data" / "raw",
        manifest=root / "data" / "reference" / "source_manifest.json",
        staged=root / "data" / "interim" / "staged",
        prpo_views=root / "data" / "interim" / "prpo_views",
        duplicates=root / "data" / "interim" / "duplicates",
        conformed=root / "data" / "interim" / "conformed",
        processed=root / "data" / "processed",
        exceptions=root / "outputs" / "exceptions",
        tables=root / "outputs" / "tables",
        reports=root / "outputs" / "reports",
    )
