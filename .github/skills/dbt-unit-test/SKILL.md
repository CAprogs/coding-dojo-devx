---
name: dbt-unit-test
description: "Fix or change the logic of a dbt model in this repository test-first: write a failing dbt Core 1.x unit test for the model, then change the SQL until `just dbt-unit` passes. Use for any bug or rule change in models/silver or models/gold."
---

# Test-first change to a dbt model

## Steps

1. **Locate the model** that owns the rule, under `src/transformation/dbt_paris_event_analyzer/models/`.
   Read its SQL and list its direct parents: every `ref(...)` it uses.
2. **Write the unit test first**, in `models/<layer>/_<layer>__unit_tests.yml` (append to the existing
   `unit_tests:` list if the file exists). Use the template below:
   - one `given` entry per direct parent, including parents that need no rows (`rows: []`);
   - only the columns the rule needs; dbt fills the others with NULL;
   - one row per case of the acceptance criteria, with readable `id` values that name the case;
   - no dependency on the current date: use 2000 for the past and 2099 for the future.
3. **Run `uv run just dbt-unit`** and check that the new test **fails** for the expected reason.
   If it passes before the fix, the test does not encode the rule: fix the test.
4. **Change the SQL** of the model, as little as possible.
5. **Run `uv run just dbt-unit`** until it passes, then `uv run just lint-sql`.
6. Report: the rule, the cases covered, the red and green test output, and the files changed.

## Template

```yaml
unit_tests:
  - name: <story_id>_<rule_in_snake_case>
    description: "<story id>: <the rule in one sentence>"
    model: <model_name>
    given:
      - input: ref('<parent_model>')
        rows:
          - {id: <case_name>, <column>: <value>}
      - input: ref('<other_parent>')
        rows: []
    expect:
      rows:
        - {id: <case_name>, <output_column>: <expected_value>}
```

## Pitfalls in this project

- `up_to_date_events` keeps only rows where `is_outdated` is false: set `is_outdated: false` in its inputs.
- `current_date` and `current_localtimestamp()` make results depend on the day; keep test dates far from today.
- Plain `dbt` commands fail here; always go through `just`.

Reference: https://docs.getdbt.com/docs/build/unit-tests
