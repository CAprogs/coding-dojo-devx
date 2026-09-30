# Lab 2: feedback loop and dbt unit tests (40 minutes)

**Driver:** person B. **Branch:** `upstream/lab-2` (contains the Lab 1 reference solution). **Pull request to:** `lab-2`.
**Story:** [DN-2](backlog/DN-2.md): never show a blank-padded or meaningless address.

## Goal

Give the agent a fast, deterministic signal, let it run that signal without asking you each time,
and use it to fix a real data bug test-first.

## dbt unit tests in three minutes (dbt Core 1.x)

- A unit test runs **one model's SQL** on rows you provide (`given`) and compares the result with rows you expect (`expect`).
- It is declared in YAML under `unit_tests:`, next to the models. It needs no real data.
- With `format: dict` (the default) you only list the columns the test needs; the other columns are NULL.
- dbt needs to know the columns of each input, so the parent models must exist in the warehouse. `just dbt-unit` builds them empty first (`dbt run --empty`), then runs `dbt test --select "test_type:unit"`.
- `dbt build` runs a model's unit tests before building it.

Reference: [dbt unit tests](https://docs.getdbt.com/docs/build/unit-tests).

## Steps

### 1. Allowlist first (5 minutes)

Create `.vscode/settings.json`:

```jsonc
{
  "chat.tools.terminal.autoApprove": {
    "/^uv run just dbt-unit$/": true,
    "/^uv run just dbt-build-ci$/": true,
    "/^uv run just lint-sql$/": true
  }
}
```

Why regular expressions? A plain string key matches the **start** of a command: `"uv run just dbt-unit"` would also
approve `uv run just dbt-unit-anything`. The anchored form `/^...$/` approves exactly one command line.

Discuss with your navigator: approving `just dbt-unit` approves **whatever the `dbt-unit` recipe runs**, and dbt runs
whatever SQL the models contain. The allowlist is only as safe as the `justfile` and the models:
approving `just X` means approving any code the agent may have written that `X` runs. The `justfile` also loads a `.env`
file if one exists, which could change the environment of every approved recipe.

Recommended in your **user** settings (it is ignored in workspace settings): keep edits to the files your allowlisted
commands execute under manual approval. The last matching pattern wins, so `"**/*": true` comes first.
If you already have this setting, add the lines instead of replacing it.

```jsonc
"chat.tools.edits.autoApprove": {
  "**/*": true,
  "**/justfile": false,
  "**/.pre-commit-config.yaml": false,
  "**/.github/workflows/**": false,
  "**/profiles.yml": false,
  "**/data/sample/*.py": false,
  "**/pyproject.toml": false,
  "**/uv.lock": false,
  "**/.env*": false,
  "**/macros/**": false,
  "**/models/**/*.py": false
}
```

### 2. Write the failing test (15 minutes)

Ask the agent, in a new chat:

```text
Read course/backlog/DN-2.md. Do not change any model yet. Write a dbt unit test for up_to_date_events
in src/transformation/dbt_paris_event_analyzer/models/silver/_silver__unit_tests.yml that encodes the acceptance criteria, then run uv run just dbt-unit
and show me that it fails.
```

Check the test yourself before going on:

- the rows given for `ref('agenda_enriched')` set `is_outdated: false` (otherwise the model's `WHERE` clause drops them);
- at least one case with a postal code and no street, and a complete address;
- optional teaching case: a venue name only (no street, no postal code).
  A naive fix with `concat_ws` returns `''` here, not NULL.
- `expect` rows with `full_address`, `latitude` and `longitude`.

Paste the red output in the pull request.

### 3. Fix (10 minutes)

```text
Now fix up_to_date_events so that the test passes. Change as little SQL as possible.
Validate with uv run just dbt-unit, then uv run just dbt-build-ci and uv run just lint-sql.
```

The three commands now run without asking you. Watch the loop: failure, change, run again.

### 4. Pull request (5 minutes)

Commit (`fix(dbt): hide incomplete addresses`), push, and open the pull request to `lab-2`.
Include the red and green outputs, the model used and the context percentage.

## You are done when

- `uv run just dbt-unit` is green.
- CI passes: `quality`, `dbt-ci` and `lab-checks` (allowlist rules are anchored regexes of exact recipes; at least one unit test exists).
- The informational `acceptance` job, which checks DN-2 on the offline sample, passes.

## Fallback

Stuck on the test? Copy [fallbacks/lab-2/_silver__unit_tests.yml](fallbacks/lab-2/_silver__unit_tests.yml)
into `src/transformation/dbt_paris_event_analyzer/models/silver/` and continue at step 3.

## Review (3 minutes)

See [rubrics.md](rubrics.md#lab-2-feedback-loop-and-dbt-unit-test).
