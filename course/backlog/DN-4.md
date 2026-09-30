# DN-4: Make "today" reproducible (extension)

**As** a data engineer,
**I want** to rebuild "today's events" for a given date,
**so that** I can reproduce a bug report and test date logic deterministically.

## Acceptance criteria

- The models that use `current_date` or `current_localtimestamp()` read a `run_date` dbt variable,
  defaulting to the current date.
- A unit test sets `overrides: vars: {run_date: ...}` and checks `has_event_today`.

Lab: [extensions](../extensions.md), E1.
