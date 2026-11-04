# CALIBER 2026 Final Round: Case 3, Spare Part Intelligence

Data engineering and analysis foundation for the six supplied Excel workbooks.

**Current status:** Phases 0 to 3 and marts M1 to M3 are implemented: environment and sources, ingestion and profiling, data quality evidence, conformed tables with an audited relationship layer, and procurement, inventory and demand marts. Simulation has a design and feasibility assessment only: **no engine exists, and none has been run**. The official Case 3 brief (`docs/case/CALIBER 2026 - Final Case Brief.pdf`) has been inspected and traced in `docs/strategy/OFFICIAL_CASE_ALIGNMENT_AUDIT.md`. The Phase 1 execution baseline is in `docs/strategy/MASTER_SOLUTION_BLUEPRINT.md` section 12. No engine, application or deployment exists yet. Phase 2 awaits Lead approval. EDA awaits approval.

**Data status:** The source data is documented as synthetic (dummy) in the Data Context & Relationship Diagram. Results describe this dataset, not operational performance.

## Environment setup

Requires Python 3.14 (verified on 3.14.3, macOS). Create the virtual environment **outside iCloud Drive**, because syncing it causes problems.

```bash
python3 -m venv ~/.venvs/caliber26
source ~/.venvs/caliber26/bin/activate
```

## Dependency installation

Run from the repository root:

```bash
python -m pip install -r requirements.txt
python -m pip check
```

Versions are pinned. Direct dependencies are pandas, openpyxl, pytest, numpy and scipy.

## Pipeline execution

Run from the repository root:

```bash
python -m src.pipeline                  # everything
python -m src.pipeline --stage sources  # checksums and source manifest only
python -m src.pipeline --stage ingest   # also staged tables and PR PO views
python -m src.pipeline --stage conform  # also conformed tables
python -m src.pipeline --stage marts    # also marts M1 to M3
```

- Exit code `0` means no critical check failed. Exit code `1` means at least one did, and reports are still written.
- The pipeline only reads `data/raw/`. It never writes there.
- Rerunning overwrites generated files with byte-identical content, except `run_metadata.json` and `pipeline.log`.

## Test execution

```bash
python -m pytest                    # all tests, about 1 minute
python -m pytest tests/unit         # logic and failure-detection tests
python -m pytest -m "not slow"      # skip the full rebuild comparison
```

Tests write only to temporary folders. To keep Python cache folders out of iCloud, set `export PYTHONDONTWRITEBYTECODE=1` first.

## Output locations

| Location | Content | Committed? |
| --- | --- | --- |
| `data/raw/` | The six original workbooks. **Immutable** | No, see below |
| `data/reference/` | Audit baseline checksums, source manifest, expected values, BoM move record | Yes |
| `data/interim/staged/` | One typed table per workbook, with lineage | No, regenerated |
| `data/interim/prpo_views/` | PR PO `original_rows` and `exact_distinct_rows` views | No, regenerated |
| `data/interim/duplicates/` | Duplicate-group metadata with source row references | No, regenerated |
| `data/interim/conformed/` | Flagged facts, dimensions, bridges, `map_cycle` and metadata | No, regenerated |
| `data/processed/` | Marts M1 to M3 and `mart_metadata.json` | No, regenerated |
| `outputs/reports/` | Profiles, validation, duplicate evidence, conformed summary, relationship audit | No, regenerated |
| `outputs/exceptions/` | Row-level exception lists for review | No, regenerated |
| `outputs/tables/` | Machine-readable profiling and validation results | No, regenerated |
| `docs/analysis/` | Plan, corrections, assumptions and data quality report | Yes |

## Working with the data

- **Load staged tables with `src.data.ingest.read_staged`, and conformed tables with `src.preprocessing.conform.read_conformed`** using the types in `conformed_metadata.json`. A plain `pandas.read_csv` turns identifiers into numbers.
- **Do not open data files in Excel and save them.** Excel can damage long identifiers.
- **PR PO has two views, and neither is definitive.** Every financial or procurement metric must name the view it uses.
- **Select the PR PO sensitivity view with `in_exact_distinct_rows`.** Flags ending in `__<view>` belong to that view and are blank outside it.
- **Join materials through `dim_material`, never through BoM rows.** A raw BoM join creates 615,146 rows from 17,518 Movement rows.
- **Do not sum quantities after joining issues to notifications.** 52 shared orders repeat rows. Use `fl_attribution` and report its coverage.
- **Marts come in parallel files.** Use one view or one scenario at a time, and report results under each. No view or scenario is the default.
- **Columns named `*_proposed` or `*_scenario` are unconfirmed readings.** A flag means review, not error.
- **Never add amounts across currencies, or quantities across units.**

## Project layout

```text
src/config.py                Paths and parameters
src/pipeline.py              Command-line runner
src/reporting.py             Markdown and JSON writers
src/data/                    Schemas, workbook inspection, ingestion, profiling
src/validation/              Source checks, duplicates and their evidence, measures, exceptions, relationships, validation checks
src/marts/                    M1 to M3, the Movement copy classification and the column dictionary
src/simulation_design/       Population and feasibility evidence. Not a simulation engine
src/preprocessing/           PR PO views, conformed tables, audited joins, outlier flags, cycle mapping
tests/unit/                  Logic on small hand-checkable data, and failure detection
tests/data_contract/         Checks on the real workbooks and full pipeline
```

## Key documents

| Document | Purpose |
| --- | --- |
| `docs/analysis/DATA_ENGINEERING_IMPLEMENTATION_PLAN.md` | Audit, plan, status and Git recommendation |
| `docs/analysis/DATA_QUALITY_REPORT.md` | Validation and data quality evidence, Phases 0 to 3 |
| `docs/analysis/DATA_INTEGRATION_REPORT.md` | Conformed tables, relationships and conditions for use |
| `docs/analysis/DATA_MART_REPORT.md` | M1 to M3: purpose, grain, schema, validation, limitations, simulation readiness |
| `docs/analysis/SIMULATION_DESIGN_SPECIFICATION.md` | Method evaluation, event flow, formulas, measures, scenarios and tests. Design only |
| `docs/analysis/SIMULATION_INPUT_ASSUMPTION_REGISTER.md` | Every simulation parameter, source, assumption and uncertainty |
| `docs/analysis/SIMULATION_FEASIBILITY_ASSESSMENT.md` | What the current data can and cannot support |
| `docs/analysis/DATA_SPECIFICATION_CORRECTIONS.md` | Corrections to the Dictionary and Specification. Takes precedence over them |
| `docs/analysis/ASSUMPTIONS_REGISTER.md` | Open definitions and assumptions |
| `docs/analysis/CALIBER_DATA_DICTIONARY.md` | Field definitions (original) |
| `docs/analysis/CALIBER_DATA_PREPARATION_SPECIFICATION.md` | Transformation rules (original) |
