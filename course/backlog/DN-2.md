# DN-2: Never show a blank-padded or meaningless address

**As** a visitor of the DataNova app,
**I want** an event address to be either complete or absent,
**so that** I never see an address like `" 75010"` or a map pin without an address.

## Context

On 2026-09-30, 13 of the 3,745 events published by Paris Open Data had a postal code but no street
and no venue name. `silver.up_to_date_events` builds `full_address` with `concat`, which skips NULLs,
so these events show `" 75010"` and still get a map pin. The offline sample reproduces the case
(`sample-007`, and `sample-008` for a venue name without street or postal code).

## Acceptance criteria

- `full_address` is `<street> <postal code>` only when both are present and not blank.
- Otherwise `full_address`, `latitude` and `longitude` are NULL.
- A dbt unit test encodes these rules and fails before the fix.

Lab: [Lab 2](../04-lab-2-dbt-unit-tests.md).
