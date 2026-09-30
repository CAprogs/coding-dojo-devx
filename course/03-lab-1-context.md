# Lab 1: context engineering (25 minutes)

**Driver:** person A. **Branch:** `upstream/lab-1`. **Pull request to:** `lab-1`.

## Goal

Give the agent durable context about this repository, and prove that the context changes what it does.

## Why

Without instructions, the agent spends requests discovering the project, and guesses when it cannot.
In this repository, plain `dbt build` fails: the project and profiles directories are set by the `justfile`.
One short file removes that guess for every future request.

## Steps

1. **Before** (fresh chat, Agent mode). Ask exactly:

   ```text
   Which single command validates a dbt change in this repository? Run it.
   ```

   Note the command it ends up proposing, how many tool calls it made before that (files read, searches, failed
   commands), and the result. Deny anything that is not a validation command. Screenshot it.

2. Create **`AGENTS.md`** at the repository root (start from [templates/AGENTS.md](templates/AGENTS.md)), with:
   - a short project map;
   - a **Commands** section listing the `just` recipes to use (`uv run just --list` shows them);
   - a definition of done;
   - a "Never" list: hand edits of `uv.lock`, reading `.env` files, network commands unless asked.

   Keep it under 120 lines. Every line is sent with every request.

3. Create **`.github/instructions/dbt.instructions.md`** (start from [templates/dbt.instructions.md](templates/dbt.instructions.md))
   with `applyTo: "src/transformation/**"` in its front matter: SQL conventions, where unit tests live, which command validates them.

4. **After** (new chat, same prompt as step 1). Expand **References** under the response ("Used n references")
   and check that `AGENTS.md` is listed. Note the command and the number of tool calls again. Screenshot it.

5. **Scope check** (new chat). Ask a question about `src/ingestion/main.py`, for example "What does `ingest` return?".
   `dbt.instructions.md` should **not** be in the references: `applyTo` limits it to dbt files.

6. Commit (`docs: add agent instructions`), push, and open the pull request to `lab-1` with the three screenshots.
   The facilitator shows the git commands live once at the start of this lab.

## You are done when

- CI `lab-checks` passes: both files exist, `AGENTS.md` has at most 120 lines and a Commands section,
  every `just <recipe>` it mentions exists, and no credential-like string is present.
- Your screenshots show the command and the number of tool calls before and after. A capable model may find the right
  recipe without help; the difference then shows in the number of steps and credits it took.

## What to notice

- Always-on context (`AGENTS.md`) costs tokens on every request. Scoped context (`applyTo`) costs only when relevant.
- Verifiable rules ("run `uv run just dbt-unit`") beat aspirational ones ("write good tests").
- The References list is how you debug instructions: if a file is not listed, the agent did not use it.

## Review (2 minutes)

See [rubrics.md](rubrics.md#lab-1-context).
