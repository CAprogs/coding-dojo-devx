# Review rubrics

A human reviews every pull request. CI checks the shape of the harness files; this rubric covers what CI cannot judge.
Each criterion is **met** or **not met**. Two minutes per pull request is the target; Lab 2 allows three.

## Lab 1: context

| # | Criterion | Met when |
|---|---|---|
| 1.1 | Commands are real | Every command in `AGENTS.md` runs as written from the repository root. |
| 1.2 | Rules are verifiable | "Run `just dbt-unit`" rather than "write good tests". |
| 1.3 | Scope is right | dbt conventions live in the scoped `*.instructions.md`, not in `AGENTS.md`. |
| 1.4 | No duplication | `AGENTS.md` does not copy the README. |
| 1.5 | Evidence | Before/after screenshots show the command chosen and `AGENTS.md` in the references. |

## Lab 2: feedback loop and dbt unit test

| # | Criterion | Met when |
|---|---|---|
| 2.1 | Red first | The PR includes the failing test output from before the fix. |
| 2.2 | Rule encoded | Cases cover a missing street with a postal code, and a complete address. |
| 2.3 | Minimal fixtures | Only the columns the rule needs; `is_outdated: false` is set. |
| 2.4 | Right layer | The fix is in `models/silver`, not patched in `gold` or in the app. |
| 2.5 | Narrow allowlist | Auto-approved rules are anchored regexes of exact recipes (`/^uv run just dbt-unit$/`): no wildcard, no bare `uv` or `git` rule. |

## Lab 3: skill and model choice

| # | Criterion | Met when |
|---|---|---|
| 3.1 | Selectable | The `description` says what the skill does and when to use it, in this repository's terms. |
| 3.2 | Executable steps | The steps can be followed without guessing, and include "check that the test fails first". |
| 3.3 | No repetition | The skill does not restate `AGENTS.md`. |
| 3.4 | It worked | The skill produced a failing DN-3 unit test (the fix is a stretch goal); the PR states the model, number of requests and context use. |
| 3.5 | Right tests | The two unit tests cover DN-2 and DN-3 (CI only counts them). |

## Lab 4: review agent

| # | Criterion | Met when |
|---|---|---|
| 4.1 | Least privilege | `tools` lists read-only tools only; no terminal, edit, web or MCP tools. |
| 4.2 | Concrete rubric | The agent body contains the review criteria, not "review the code". |
| 4.3 | Injection clause | The body says reviewed content is data, never instructions. |
| 4.4 | Human authority | The agent reports findings; it never approves or merges. |
| 4.5 | Useful output | Findings posted on the reviewed PR cite `path:line`; one spot-checked finding is real. |

## Harness scorecard (debrief)

Score the set of pull requests of each pair, from 0 (absent) to 2 (solid).

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Context | None | Generic or long | Short, verifiable, scoped |
| Feedback | Manual checks | Commands exist | Fast, deterministic, used by the agent |
| Permissions | Allow all | Broad allowlist | Exact commands, manual for the rest |
| Procedures | None | Prompt pasted each time | Skill with a selectable description |
| Roles | None | Agent with broad tools | Read-only role, human decides |
| Cost awareness | Not tracked | Tracked | Model chosen per task, fresh chats |
