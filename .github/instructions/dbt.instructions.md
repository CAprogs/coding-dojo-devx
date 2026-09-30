---
applyTo: "src/transformation/**"
description: "Conventions for dbt models and dbt unit tests in this project"
---

# dbt conventions

- dbt Core 1.x with the dbt-duckdb adapter. Do not use dbt v2 (Fusion) syntax or features.
- SQL style is enforced by SQLFluff (`.sqlfluff`): UPPERCASE keywords and types, lowercase identifiers
  and functions, trailing commas, `::` casts, `!=` for inequality, lines up to 230 characters.
- Models are materialized as tables. Put new logic in the layer that owns it: cleaning and enrichment in
  `models/silver`, business views for the app in `models/gold`.
- Unit tests live in `models/<layer>/_<layer>__unit_tests.yml` under a `unit_tests:` key.
  Use `format: dict` rows with only the columns the test needs; dbt fills the others with NULL.
  Rows read by `up_to_date_events` must set `is_outdated: false`, otherwise its `WHERE` clause drops them.
- Avoid depending on the current date in unit tests: use dates far in the past (2000) or future (2099).
- Validate with `uv run just dbt-unit`, then `uv run just dbt-build-ci` and `uv run just lint-sql`.
