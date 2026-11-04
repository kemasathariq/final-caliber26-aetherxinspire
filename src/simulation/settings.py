"""Engine configuration. Every value below is a CONFIGURED analyst choice unless a decision ID says otherwise.

Decision states are in docs/strategy/DECISION_REGISTER.md. Nothing here is an estimate of plant behaviour.
"""
import calendar
from dataclasses import dataclass, field

from src.config import (DATA_LABEL, DEMAND_WINDOW_END, DEMAND_WINDOW_START, PROJECT_ROOT, SIM_HORIZON_END, SIM_HORIZON_START,
                        SIM_MIN_ACTIVE_MONTHS_TO_RESAMPLE_DEMAND, SIM_MIN_LINES_TO_RESAMPLE_LEAD)

ENGINE_VERSION = "1.0.0"
CONTRACT_VERSION = "0.2"
METHODOLOGY_VERSION = "INSPIRE-M-2026-11-04.1"
SIMULATED_LABEL = "SIMULATED under stated assumptions. Not observed. Inputs unverified."

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
ENGINE_DIR = PROCESSED_DIR / "engine"
SAMPLES_DIR = PROJECT_ROOT / "data" / "samples" / "engine"

HORIZON_DAYS = 518
MONTHS = [f"{y}-{m:02d}" for y, m in [(2025, m) for m in range(5, 13)] + [(2026, m) for m in range(1, 10)]]
assert MONTHS[0] == DEMAND_WINDOW_START and MONTHS[-1] == DEMAND_WINDOW_END and len(MONTHS) == 17
MONTH_LENGTHS = [calendar.monthrange(int(m[:4]), int(m[5:]))[1] for m in MONTHS]
assert sum(MONTH_LENGTHS) == HORIZON_DAYS

DEMAND_SCENARIOS = {"A": "scenario_a", "B": "scenario_b"}
PR_VIEWS = {"OR": "original_rows", "ED": "exact_distinct_rows"}

# D-03, default pending approval. Thresholds come from src/config.py so there is one source.
MIN_ACTIVE_MONTHS = SIM_MIN_ACTIVE_MONTHS_TO_RESAMPLE_DEMAND
MIN_LEAD_OBSERVATIONS = SIM_MIN_LINES_TO_RESAMPLE_LEAD
# D-05, scenario levels, never targets.
SERVICE_LEVELS = {"X1": 0.90, "X2": 0.95, "X3": 0.98}
# Analyst-selected reference level for the single action shown per scenario. The other two levels are reported beside it.
REFERENCE_SERVICE_POLICY = "X2"

MASTER_SEED = 20261105
MC_REPLICATIONS = 1000
BLOCK_MONTHS = 3
LTD_PATHS = 1000
LTD_WINDOWS_PER_PATH = 5
CONVERGENCE_HALF_WIDTH = 0.01

# Held-out replay (VALIDATION_FRAMEWORK section 3). Parameters from months 1 to 11, test on months 12 to 17.
TRAIN_END_MONTH = "2026-03"
TRAIN_MONTHS = 11
TEST_START_DATE = "2026-04-01"
TEST_START_DAY = sum(MONTH_LENGTHS[:TRAIN_MONTHS])
TEST_DAYS = HORIZON_DAYS - TEST_START_DAY

# Forecast validation (VALIDATION_FRAMEWORK section 2). Pre-registered before any result was seen.
FORECAST_ORIGINS = list(range(9, 16))  # History of 9 to 15 months.
FORECAST_ALPHAS = (0.5, 0.90, 0.95, 0.98)
FORECAST_BOOTSTRAP_PATHS = 500
SBA_ALPHA = 0.1
TSB_ALPHA = 0.1
TSB_BETA = 0.1
SMOOTH_ADI = 1.32
SMOOTH_CV2 = 0.49

# Health flags (INVENTORY_OPTIMISATION_METHODOLOGY section 5). ASSUMPTION, configurable.
SLOW_MAX_ACTIVE_MONTHS = 2
SLOW_NO_ISSUE_MONTHS = 6
SLOW_LAST_ISSUE_BEFORE = "2026-04-01"
ROBUST_Z = 3.5
ROBUST_Z_MIN_LINES = 5

# D-25: the rule table leaves thresholds unset. These are analyst-selected, configurable and pending approval.
REORDER_SHORTFALL_THRESHOLD = 0.10
REDUCE_DAYS_ABOVE_MAX_SHARE = 0.50
RISK_HIGH = 0.50
RISK_MEDIUM = 0.10


@dataclass(frozen=True)
class KSet:
    """One configuration set in the K part of the scenario identifier."""

    k: str
    run_set: str
    description: str
    i0_factor: float = 1.0
    i0_rule: str = "stock"          # stock, min, max, stock_plus_issues
    lead_factor: float = 1.0
    lead_rule: str = "median"       # median, p90
    demand_factor: float = 1.0
    min_factor: float = 1.0
    max_factor: float = 1.0
    peak_lines: str = "keep"        # keep, exclude
    extra: dict = field(default_factory=dict, hash=False)


K0 = KSet("K0", "R0", "Reference. Opening stock is recorded Stock, undated (S-01). Median promised interval. No resampling")
S1_KSETS = [
    KSet("K1", "S1", "Opening stock x0.5", i0_factor=0.5),
    KSet("K2", "S1", "Opening stock x1.5", i0_factor=1.5),
    KSet("K3", "S1", "Opening stock = recorded Min", i0_rule="min"),
    KSet("K4", "S1", "Opening stock = recorded Max", i0_rule="max"),
    KSet("K5", "S1", "Opening stock = Stock + window issues (upper bound)", i0_rule="stock_plus_issues"),
    KSet("K6", "S1", "Promised interval x0.5", lead_factor=0.5),
    KSet("K7", "S1", "Promised interval x1.5", lead_factor=1.5),
    KSet("K8", "S1", "Promised interval x2", lead_factor=2.0),
    KSet("K9", "S1", "Promised interval p90", lead_rule="p90"),
    KSet("K10", "S1", "Issues x0.75", demand_factor=0.75),
    KSet("K11", "S1", "Issues x1.25", demand_factor=1.25),
    KSet("K12", "S1", "Stock-level what-if: Min x0.5", min_factor=0.5),
    KSet("K13", "S1", "Stock-level what-if: Min x1.5", min_factor=1.5),
    KSet("K14", "S1", "Stock-level what-if: Max x0.5", max_factor=0.5),
    KSet("K15", "S1", "Stock-level what-if: Max x1.5", max_factor=1.5),
    KSet("K16", "S1", "Lines at a repeated unit peak excluded (A-11)", peak_lines="exclude"),
]
MC_KSETS = {"MC-D": "K20", "MC-L": "K21", "MC-J": "K22"}
HELD_OUT_KSETS = {"stock": "K30", "min": "K31", "max": "K32"}
CONFIG_REGISTRY = [
    ("K0", "R0", "deterministic", K0.description),
    *[(k.k, k.run_set, "deterministic", k.description) for k in S1_KSETS],
    ("K20", "MC-D", "stochastic", f"Issues resampled: circular block bootstrap of months, block {BLOCK_MONTHS}, {MC_REPLICATIONS} replications, seed {MASTER_SEED}. Median promised interval"),
    ("K21", "MC-L", "stochastic", f"Promised interval resampled per order from own history, {MC_REPLICATIONS} replications, seed {MASTER_SEED}. Issues replayed"),
    ("K22", "MC-J", "stochastic", f"Issues and promised interval both resampled, {MC_REPLICATIONS} replications, seed {MASTER_SEED}"),
    ("K30", "HO", "deterministic", "Held-out replay on 2026-04 to 2026-09. Parameters from 2025-05 to 2026-03 only. Opening stock = recorded Stock, undated"),
    ("K31", "HO", "deterministic", "Held-out replay. Opening stock = recorded Min"),
    ("K32", "HO", "deterministic", "Held-out replay. Opening stock = recorded Max"),
]


def scenario_id(demand: str, view: str, policy: str, shortage: str = "BO", k: str = "K0") -> str:
    return f"SC-{demand}-{view}-{policy}-{shortage}-{k}"


ASSUMPTIONS = [
    "S-01 undated Stock assumed to apply on day 0", "S-02 no open orders or backorders on day 0", "S-03 Min and Max read as reorder level and order-up-to level, unverified (D-02)",
    "S-05 backorder reference, lost sales alternative", "S-11 issues stand in for demand; they are not proven demand", "P-05 promised interval stands in for lead time; it is not a goods-receipt lead time",
    "D-03 evidence thresholds 6 active months and 10 lead observations", "D-05 service levels 90, 95, 98 percent are scenario levels", "D-24 proposed parameters for the 228 Grade A materials only",
]
DATA_LABEL_TEXT = DATA_LABEL
HORIZON = (SIM_HORIZON_START, SIM_HORIZON_END)
