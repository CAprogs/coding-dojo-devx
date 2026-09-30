# DN-1: Validate the project offline in one command

**As** a new developer on the DataNova team,
**I want** a single command that tells me my machine is ready,
**so that** I can start contributing without chasing setup issues.

## Acceptance criteria

- `uv run just preflight` ends with `PREFLIGHT OK` on a fresh clone.
- It needs no Docker, no credentials and no `.env` file.
- It builds every dbt model on the offline sample and runs every dbt test.

Status: delivered in the baseline. Used in Lab 0 to discover the repository with Copilot.
