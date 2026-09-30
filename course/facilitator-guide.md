# Facilitator guide

## Timeline before the session

| When | Action |
|---|---|
| D-10 | Re-verify every Copilot claim and setting name in [sources.md](sources.md) against the current VS Code release. Update `READ_ONLY_TOOLS` in `checks/lab_check.py` if tool names changed. Check the model names used in `templates/reviewer.agent.md`. |
| D-10 | Ask the Copilot administrator to confirm: Agent mode enabled, the credit budget per learner and its alert, and "MCP servers in Copilot" for the facilitator seat. |
| D-7 | Send [00-prerequisites.md](00-prerequisites.md). |
| D-1 | Collect `PREFLIGHT OK` screenshots and warm-up pull requests. Merge each warm-up pull request into `warmup`: after that, the learner is no longer a first-time contributor and their workflows run without approval. |
| D-1 | Rehearse the MCP demo and record it as the fallback. Prepare the Lab 4 review pairing list. |

## During the session

- **Pairs:** mix experience levels. Person A drives Labs 1 and 3, person B drives Labs 2 and 4.
- **Lab 1:** show the fork, branch, push and pull request commands once, live (5 minutes).
- **No live review during Labs 0 to 2.** Circulate, unblock, and point to fallbacks.
- **Breaks:** use break 1 to triage stuck learners, break 2 to prepare the spotlight reviews.
- **Lab 4 pairing:** pair *n* reviews the Lab 2 pull request of pair *n+1* (the last pair reviews the first).

## Cut order when late

1. Lab 3 down to 15 minutes: skill only, DN-3 as homework (-5).
2. MCP demo replaced by the recording (-5).
3. One spotlight review instead of two (-4).

The last 8 minutes of the agenda are a floating buffer.

## Review cadence

- About 20 pull requests: 5 pairs × 4 labs.
- While each lab runs, draft reviews with the private reviewer (instructor material, not in this repository). Read each draft, edit it, and post it yourself as a comment review. About one minute per pull request.
- In the debrief, review two pull requests live.
- Finish the others within 48 hours.
- Only a human approves or merges. Pull requests are never merged into `main`; exemplary ones may be merged into their `lab-N` branch after the session.

## Known issues

- The `sqlfluff-fix` pre-commit hook rewrites SQL files during `git commit`. The commit then stops: stage the changes and commit again.
- Commitizen rejects commit messages that are not Conventional Commits (`fix(dbt): ...`).
- `just dbt-unit` builds the parents empty first; a model that fails to compile fails there, before the unit tests run.
- The offline sample is regenerated with dates relative to today on every `just dbt-build-ci`. Do not commit `data/sample/*.parquet`.
- Workflow runs from a learner's first pull request wait for approval unless their warm-up pull request was merged.

## Credits

Ask learners to report, for Labs 2 and 3: the model, the number of requests and the context percentage.
Measure the credits per lab during the rehearsal and share the order of magnitude in the debrief.
