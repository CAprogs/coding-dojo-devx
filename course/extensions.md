# Extensions (optional)

For learners who finish a lab early. None of them is needed for the next lab.

## E1: a reproducible "today" ([DN-4](backlog/DN-4.md))

Replace `current_date` and `current_localtimestamp()` in `silver/agenda.sql` and `silver/agenda_enriched.sql`
with a `run_date` variable, for example `{{ var('run_date', modules.datetime.date.today().isoformat()) }}`.
Then write a unit test that sets it:

```yaml
    overrides:
      vars:
        run_date: "2030-06-15"
```

## E2: planner, implementer and reviewer

- Write a `planner.agent.md` with read-only tools and a `handoffs` entry that passes its plan to the default agent for implementation.
- Let the planner call your `reviewer` as a subagent: add `agent` to its tools and `agents: ['reviewer']` to its front matter.
- Enable the `runSubagent` tool in Configure Tools if needed.
- Remember: a subagent cannot use a more expensive model than the agent that calls it.

## E3: untrusted HTML ([DN-5](backlog/DN-5.md))

Replace `unsafe_allow_html=True` in `src/exposition/main.py` with a small sanitising function, tested with pytest.

## E4: a hook (Preview)

If your organisation allows preview features, add a `PostToolUse` hook in `.github/hooks/` that runs `uv run just lint-sql`
after SQL edits. Hooks run with your permissions: review them like code.

## E5: MCP on your machine

If the organisation policy allows it, reproduce the [MCP demo](07-mcp-demo.md) with your own read-only token.
Never commit a token; the configuration uses an input prompt.
