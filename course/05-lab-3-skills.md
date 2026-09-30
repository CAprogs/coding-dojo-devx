# Lab 3: a skill and a cheaper model (20 minutes)

**Driver:** person A. **Branch:** `upstream/lab-3` (contains the Lab 2 reference solution). **Pull request to:** `lab-3`.
**Story:** [DN-3](backlog/DN-3.md): show ongoing events that have no detailed schedule.

## Goal

Turn the Lab 2 procedure into a reusable **skill**, then let a lighter model follow it on a new story.

## Skills in two minutes

- A skill is a folder `.github/skills/<name>/` with a `SKILL.md` file and, optionally, templates or scripts.
- Only its `name` and `description` are loaded at first. The agent loads the body when the description matches the task, so the description decides whether the skill is used.
- You can also call it explicitly by typing `/` followed by its name in the chat.
- Procedures belong in skills. `AGENTS.md` stays short and lists facts.

## Steps

1. Create `.github/skills/dbt-unit-test/SKILL.md` (start from [templates/SKILL.md](templates/SKILL.md)):
   - `name: dbt-unit-test` (it must match the folder name);
   - a `description` that says what it does and when to use it, in this repository's terms;
   - the steps: find the model and its direct parents, write the failing test, run `uv run just dbt-unit`,
     check it fails for the right reason, change the SQL, run again, lint;
   - a YAML template and the pitfalls you met in Lab 2.

2. Open a **new chat**, pick **Auto** or a lightweight model, and ask:

   ```text
   Implement course/backlog/DN-3.md test-first.
   ```

   Do not name the skill. Check under **References** whether it was picked up. If not, improve its description, or call it with `/dbt-unit-test`.

   Hint for your review: the fix belongs where `has_event_today` is derived for events without occurrences.
   `agenda_enriched` joins `filtered_rows` with `agenda`, so its unit test needs **two** `given` inputs.

3. Compare with Lab 2: number of requests, context percentage, and how much you had to steer.

4. Commit (`feat(dbt): list ongoing events without occurrences`), push, and open the pull request to `lab-3`
   with the model used, the number of requests and the context percentage.

## You are done when

- CI `lab-checks` passes: the skill's `name` matches its folder, its description is specific, and at least two unit tests exist.
- The informational `acceptance` job, which checks DN-2 and DN-3 on the offline sample, passes.

## Short on time?

Keep the skill and leave DN-3 for later: open the pull request with the skill only (15 minutes).
`lab-checks` will then report the missing second unit test; that is expected.

## Review (2 minutes)

See [rubrics.md](rubrics.md#lab-3-skill-and-model-choice).
