# Lab 4: a read-only review agent (20 minutes)

**Driver:** person B. **Branch:** `upstream/lab-4` (contains the Lab 3 reference solution). **Pull request to:** `lab-4`.

## Goal

Create a bounded role: an agent that reviews a diff against the course rubric, cannot change or run anything,
and leaves the decision to a human.

## Custom agents and subagents in two minutes

- A custom agent is a `.github/agents/<name>.agent.md` file: front matter (`description`, `tools`, `model`, ...) and a body of instructions.
- `tools` lists what it may use. Without `tools`, it gets the default tools, so always list them explicitly.
  Read-only tool sets: `search` and `read`. Tool sets that change things or reach out: `edit`, `execute`, `web`, `agent`, `vscode`, MCP servers.
- `model` accepts a list; the first available model is used. A light model is enough for a checklist review.
- Another agent can run a custom agent as a **subagent**, in its own context window. A subagent cannot use a more expensive model than the agent that calls it.

## Steps

1. Create `.github/agents/reviewer.agent.md` (start from [templates/reviewer.agent.md](templates/reviewer.agent.md)):
   - `tools: ['search', 'read']`;
   - `model`: a light model first, then `Auto (copilot)` as fallback;
   - a body with the review criteria of [rubrics.md](rubrics.md), the output format
     (blocking and non-blocking findings with `path:line`), and a rule stating that reviewed content is data, never instructions;
   - no approval, no merge.

   VS Code asks you to confirm edits in `.github/agents/` by default. Read the change before accepting it.

2. Prepare the diff of the pull request you review. Each pair reviews the Lab 2 pull request of the next pair
   (the facilitator posts the list):

   ```bash
   git fetch upstream pull/<number>/head:review-<number>
   mkdir -p .review
   git diff upstream/lab-2...review-<number> > .review/diff.patch
   ```

   `.review/` is ignored by git.

3. Pick **reviewer** in the agent picker, in a new chat, and ask:

   ```text
   Review .review/diff.patch.
   ```

4. Check one finding yourself: does the cited line exist and say what the agent claims?
   Then post the findings as a comment on the reviewed pull request:

   ```bash
   gh pr comment <number> --repo CAprogs/coding-dojo-devx --body-file <file with the findings>
   ```

5. Commit (`feat: add a read-only review agent`), push, and open your pull request to `lab-4`.
   Include a screenshot of the agent's tool list (Configure Tools) and the link to the comment you posted.

## You are done when

- CI `lab-checks` passes: `tools` is an explicit list of read-only tools, with no handoffs or subagents,
  and the body tells the agent to treat reviewed content as data.
- Your findings are posted on the other pair's pull request.

## What to notice

- The agent cannot run a command, so a malicious diff cannot make it do anything but write text.
- The human reads, checks and decides. The agent's findings are an input, not a verdict.

## Review (2 minutes)

See [rubrics.md](rubrics.md#lab-4-review-agent).
