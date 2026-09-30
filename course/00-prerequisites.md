# Prerequisites (complete before the session)

Plan about 30 minutes. Do this **at least one day before** the session: installing the hook
environments and DuckDB extensions downloads several hundred megabytes, and the course has no time for it.

Send the facilitator a screenshot of `PREFLIGHT OK` and the link to your warm-up pull request **by D-1**.
If your preflight is not green, you will work on your partner's machine.

## 1. Accounts and editor

- A GitHub account that is a member of the organisation that provides your Copilot seat.
- [VS Code](https://code.visualstudio.com/), latest stable release.
- GitHub Copilot enabled in VS Code: open the Chat view, sign in with that account, and check that
  the mode picker offers **Agent**.
- Optional: the [GitHub CLI](https://cli.github.com/) (`gh auth login`). Without it, open pull requests from the GitHub web UI.

If Agent mode is missing, ask your Copilot administrator. Organisation policies can disable it.

## 2. Tools

- git
- [uv](https://docs.astral.sh/uv/getting-started/installation/). uv installs Python 3.12 and `just` for the project; you do not need to install them yourself.

No Docker, credentials or `.env` file are needed.

## 3. Fork and clone

1. Fork `https://github.com/CAprogs/coding-dojo-devx` to your account. Uncheck "Copy the main branch only": you need the `lab-*` branches.
2. Clone your fork and add the course repository as `upstream`:

```bash
git clone https://github.com/<you>/coding-dojo-devx.git
cd coding-dojo-devx
git remote add upstream https://github.com/CAprogs/coding-dojo-devx.git
git fetch upstream
```

## 4. Preflight

```bash
uv sync --locked --all-groups
uv run just preflight
```

Expected end of output: `PREFLIGHT OK`.

Then open the folder in VS Code and trust the workspace when asked.

## 5. Warm-up pull request

On a public repository, GitHub asks a maintainer to approve workflow runs for first-time contributors.
The warm-up pull request gets that approval out of the way before the session.

```bash
git switch -c warmup-<you> upstream/warmup
git commit --allow-empty -m "chore: warm-up for <you>"
git push -u origin warmup-<you>
gh pr create --repo CAprogs/coding-dojo-devx --base warmup --title "chore: warm-up <you>" --body "Warm-up"
```

The facilitator merges warm-up pull requests into the `warmup` branch, which exists only for this purpose.

## Manual fallback

If `just preflight` fails, run the steps one by one and send the facilitator the first failing output:

```bash
uv sync --locked --all-groups
uv pip install -e .
uv run pre-commit install --install-hooks
uv run python -c "import duckdb; duckdb.sql('INSTALL parquet; INSTALL spatial;')"
uv run just dbt-build-ci
```

Common causes: a corporate proxy blocking `extensions.duckdb.org` or PyPI, or an old uv (`uv self update`).
