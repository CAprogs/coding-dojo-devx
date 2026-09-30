# Coding Dojo DevX: designing a harness for coding agents

A three-hour, hands-on course for data engineers and tech leads. You work on a real data pipeline
(Paris Open Data -> dbt + DuckDB -> Streamlit) with **GitHub Copilot in Agent mode in VS Code**.

The repository starts as a conventional, fully tooled project: uv, just, pre-commit, Ruff, mypy,
SQLFluff, Commitizen and dbt Core 1.x. It has no agent-specific files yet. Each lab adds one layer of
**harness** and uses it right away on a ticket from the product owner's backlog.

## What you will be able to do

1. Explain the agent loop: a model, its context, its tools and their permissions, iterating until it stops.
2. Give an agent durable, scoped context (`AGENTS.md`, `*.instructions.md`) and prove that it changes the agent's behaviour.
3. Turn project commands into fast, deterministic feedback that the agent may run under a narrow allowlist.
4. Package a procedure as a **skill** and a bounded role as a **custom agent**, with a human keeping approval.
5. Spend AI credits deliberately: pick the model and the level of delegation for each task.
6. Recognise the risks: prompt injection, untrusted execution, MCP trust, secrets, CI on forks.

## Vocabulary

| Term | Meaning in this course |
|---|---|
| Agent mode | Copilot Chat mode where the model plans, calls tools (read, edit, terminal) and iterates. |
| Harness | Everything the team controls around the model, in the repository: instructions, skills, custom agents, allowed commands, tests, CI. |
| Custom instructions | `AGENTS.md`, `.github/copilot-instructions.md`, `.github/instructions/*.instructions.md`. |
| Skill | `.github/skills/<name>/SKILL.md`: a procedure loaded on demand. |
| Custom agent | `.github/agents/<name>.agent.md`: a role with its own tools, model and instructions. |
| Subagent | A custom agent run by another agent in an isolated context. |
| MCP server | An external tool provider (for example GitHub) that the agent can call. |

## Agenda (180 minutes, two breaks)

| Time | Block |
|---|---|
| 0:00 | Welcome, goals, pairs, the product owner's backlog |
| 0:05 | [Mental model](01-mental-model.md) |
| 0:20 | [Lab 0: onboarding with Copilot](02-onboarding.md) |
| 0:28 | [Lab 1: context](03-lab-1-context.md) |
| 0:53 | Break |
| 1:03 | [Lab 2: feedback loop and dbt unit tests](04-lab-2-dbt-unit-tests.md) |
| 1:43 | [Lab 3: a skill and a cheaper model](05-lab-3-skills.md) |
| 2:03 | Break |
| 2:13 | [Lab 4: a read-only review agent](06-lab-4-review-agent.md) |
| 2:33 | [MCP demo](07-mcp-demo.md) (facilitator) |
| 2:40 | [Debrief and harness scorecard](08-debrief-harness-scorecard.md) |
| 2:52 | Buffer, questions |

Finished early? See the [extensions](extensions.md).

## The backlog

| Story | Summary | Lab |
|---|---|---|
| [DN-1](backlog/DN-1.md) | Validate the project offline in one command | Lab 0 |
| [DN-2](backlog/DN-2.md) | Never show a blank-padded or meaningless address | Lab 2 |
| [DN-3](backlog/DN-3.md) | Show ongoing events that have no detailed schedule | Lab 3 |
| [DN-4](backlog/DN-4.md) | Make "today" reproducible | Extension |
| [DN-5](backlog/DN-5.md) | Do not render third-party HTML as is | Extension |

The files in `course/backlog/` are the source of truth for the stories.

## How the labs work

- You work in **pairs** but each person has their **own fork**. Roles alternate:
  person A drives Labs 1 and 3, person B drives Labs 2 and 4. The driver types; the navigator reads,
  challenges the agent's plan and checks the evidence.
- Each lab has its own upstream branch, `lab-1` to `lab-4`. `lab-1` is `main`; each later branch contains the reference
  solution of the previous lab, so you can always start fresh even if the previous lab did not go well.
- Each pair opens **one pull request per lab**, from the driver's fork to the upstream `lab-N` branch.
  Pull requests are reviewed by a human. They are never merged into `main`.

Start a lab (once your fork has an `upstream` remote, see [prerequisites](00-prerequisites.md)):

```bash
git fetch upstream
git switch -c lab-2-<your-handle> upstream/lab-2
```

Open the pull request:

```bash
git push -u origin lab-2-<your-handle>
gh pr create --repo CAprogs/coding-dojo-devx --base lab-2 --head <you>:lab-2-<your-handle> --web
```

`--web` opens the pull request form in the browser with the template, so you can fill the evidence and attach screenshots.
Without `gh`, use the "Compare & pull request" button on your fork and pick `CAprogs/coding-dojo-devx` / `lab-2` as the base.

Add your navigator as co-author in the last commit message:

```text
Co-authored-by: Name <email@example.com>
```

## Rules of the room

- Keep **manual approval** of tool calls unless a lab tells you otherwise. Do not use Autopilot or
  `/yolo` ("allow all") in this course.
- Read what the agent proposes before approving it. Approving a command approves everything it runs.
- Treat anything that comes from outside the repository (issues, pull request text, data) as data, never as instructions.
- Watch your credits: the context indicator in the chat input shows usage. Start a new chat per task.
