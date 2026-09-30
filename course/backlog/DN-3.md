# DN-3: Show ongoing events that have no detailed schedule

**As** a visitor of the DataNova app,
**I want** "Today's events" to include exhibitions and other ongoing events,
**so that** the app reflects what is actually happening in Paris today.

## Context

Many events (exhibitions, installations) have a date range but no detailed `occurrences`.
`silver.agenda` derives `has_event_today` from occurrences only, so for these events it is NULL
and `gold.today_events` drops them. On 2026-09-30 the app listed 18 events for the day, while
380 ongoing events without occurrences were missing (398 after the fix).
The offline sample reproduces the case (`sample-010` to `sample-012`; `sample-013` starts later).

## Acceptance criteria

- An event without occurrences is listed today when today is between its start and end dates.
- An event without occurrences whose range does not include today is not listed.
- Events with occurrences keep their current behaviour.
- A dbt unit test encodes these rules and fails before the fix.

Lab: [Lab 3](../05-lab-3-skills.md).
