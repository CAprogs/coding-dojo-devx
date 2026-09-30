[private]
default:
    @just --list --list-prefix " ➫ " --unsorted

set dotenv-load

export DBT_PROJECT_DIR := "src/transformation/dbt_paris_event_analyzer/"
export DBT_PROFILES_DIR := "src/transformation/dbt_paris_event_analyzer/profiles/"

PROD_DATABASE := "warehouse/prod.duckdb"
CI_DATABASE := "warehouse/ci.duckdb"
INGESTION_ENTRYPOINT := "src/ingestion/main.py"
WEB_APP_ENTRYPOINT := "app.py"
SAMPLE_GENERATOR := "data/sample/generate_sample.py"

# Check that this machine can run the whole offline workflow
[group("setup")]
preflight:
    @echo "\n[1/4] Syncing dependencies from uv.lock ..\n"
    @uv sync --locked --all-groups
    @uv pip install -e . --quiet
    @echo "\n[2/4] Installing git hooks and hook environments ..\n"
    @uv run pre-commit install --install-hooks
    @echo "\n[3/4] Installing DuckDB extensions ..\n"
    @uv run python -c "import duckdb; duckdb.sql('INSTALL parquet; INSTALL spatial;')"
    @echo "\n[4/4] Building the offline warehouse and running all dbt tests ..\n"
    @just dbt-build-ci
    @echo "\nPREFLIGHT OK\n"

[group("test")]
quality:
	@echo "Checking pre-commit config consistency"
	@uv run pre-commit validate-config
	@echo "\nInstalling pre-commit hooks\n"
	@uv run pre-commit install --install-hooks

[group("test")]
quality-default: quality
	@echo "\nRunning pre-commit on staged files\n"
	@uv run pre-commit run

[group("test")]
quality-all: quality
	@echo "\nRunning pre-commit on all files\n"
	@uv run pre-commit run --all-files

# Lint all dbt SQL models with SQLFluff (no database needed)
[group("test")]
lint-sql:
    @uv run pre-commit run sqlfluff-lint --all-files

# Regenerate the synthetic offline sample (dates relative to today)
[group("dbt")]
sample:
    @uv run python {{SAMPLE_GENERATOR}}

# Build every model on the offline sample and run unit + data tests
[group("dbt")]
dbt-build-ci: sample
    @uv run dbt build --target ci

# Run dbt unit tests only (parents are built empty first)
[group("dbt")]
dbt-unit: sample
    @uv run dbt run --target ci --empty --quiet
    @uv run dbt test --target ci --select "test_type:unit"

[group("dbt")]
dbt-debug:
    @echo "\nDebugging profile config .."
    @uv run dbt debug --config-dir
    @uv run dbt debug

[group("dbt")]
dbt-catalog: dbt-debug
    @echo "\nBuilding catalog .."
    @uv run dbt docs generate
    @echo "\nOpening DBT documentation .."
    @uv run dbt docs serve --port 3000

# Build the models on today's real snapshot (run `just ingest` first)
[group("dbt")]
dbt-run: dbt-debug
    @echo "\nRunning dbt models .."
    @uv run dbt run

[group("dbt")]
dbt-clean:
    @echo "\nCleaning dbt project .."
    @uv run dbt clean --no-clean-project-files-only

# Open the DuckDB UI on the real warehouse (needs the DuckDB CLI)
[group("dbt")]
duckdb-ui: dbt-run
    @echo "\nStarting DuckDB UI .."
    @duckdb -ui {{PROD_DATABASE}}

# Download today's events from Paris Open Data into datalake/
[group("workflow")]
ingest:
		@uv run python {{INGESTION_ENTRYPOINT}}

[group("workflow")]
expose:
		@WAREHOUSE_PATH={{PROD_DATABASE}} uv run streamlit run {{WEB_APP_ENTRYPOINT}}

# Start the app on the offline warehouse
[group("workflow")]
expose-ci: dbt-build-ci
		@WAREHOUSE_PATH={{CI_DATABASE}} uv run streamlit run {{WEB_APP_ENTRYPOINT}}

[group("workflow")]
final-workflow: ingest dbt-run expose
