"""Structural checks for the harness files each lab asks for.

Usage: `uv run python course/checks/lab_check.py lab-2`

The checks are deliberately simple and fail closed. They verify the shape of the harness,
not its quality: the human review and the rubrics in course/rubrics.md cover the rest.
"""

from collections.abc import Callable
from pathlib import Path
from typing import Any
import subprocess  # noqa: S404
import json
import sys
import re
import yaml


DBT_MODELS = Path("src/transformation/dbt_paris_event_analyzer/models")
MAX_AGENTS_MD_LINES = 120

# Tools a read-only review agent may use. Re-verify against the VS Code docs before each session
# (course/sources.md). Anything not listed here fails the check.
READ_ONLY_TOOLS = {
    "search",
    "search/codebase",
    "search/fileSearch",
    "search/textSearch",
    "search/listDirectory",
    "search/usages",
    "search/changes",
    "read",
    "read/readFile",
    "read/problems",
}

EXACT_RECIPE_RULE = re.compile(r"/\^(uv run )?just [a-z0-9-]+\$/")

SECRET_PATTERNS = [
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
]


class Report:
    """Collects check results and prints them."""

    def __init__(self) -> None:
        """Starts with no failures."""
        self.failures: list[str] = []

    def check(self, condition: bool, message: str) -> None:
        """Records one check."""
        print(f"{'PASS' if condition else 'FAIL'}  {message}")  # noqa: T201
        if not condition:
            self.failures.append(message)


def front_matter(path: Path) -> dict[str, Any]:
    """Returns the YAML front matter of a Markdown file, or an empty dict."""
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", path.read_text(encoding="utf-8"), re.DOTALL)
    if not match:
        return {}
    data = yaml.safe_load(match.group(1))
    return data if isinstance(data, dict) else {}


def just_recipes() -> set[str]:
    """Returns the recipe names defined in the justfile."""
    output = subprocess.run(["just", "--summary"], capture_output=True, text=True, check=True)  # noqa: S603, S607
    return set(output.stdout.split())


def has_secret(text: str) -> bool:
    """Detects obvious credentials."""
    return any(pattern.search(text) for pattern in SECRET_PATTERNS)


def unit_test_count() -> int:
    """Counts dbt unit tests declared in YAML files under models/."""
    count = 0
    for path in DBT_MODELS.rglob("*.yml"):
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        count += len(data.get("unit_tests") or [])
    return count


def lab_1(report: Report) -> None:
    """Context: AGENTS.md and a scoped instructions file."""
    agents_md = Path("AGENTS.md")
    report.check(agents_md.is_file(), "AGENTS.md exists at the repository root")
    if agents_md.is_file():
        text = agents_md.read_text(encoding="utf-8")
        report.check(
            len(text.splitlines()) <= MAX_AGENTS_MD_LINES, f"AGENTS.md has at most {MAX_AGENTS_MD_LINES} lines"
        )
        report.check(
            re.search(r"^#+\s*Commands", text, re.MULTILINE | re.IGNORECASE) is not None,
            "AGENTS.md has a Commands section",
        )
        recipes = just_recipes()
        # Only commands written as code (`just <recipe>` or `uv run just <recipe>`), not prose such as "just to run"
        mentioned = set(re.findall(r"`(?:uv run )?just\s+([a-z][a-z0-9-]*)", text))
        unknown = sorted(mentioned - recipes)
        report.check(
            bool(mentioned) and not unknown, f"every `just <recipe>` in AGENTS.md exists (unknown: {unknown or 'none'})"
        )
        report.check(not has_secret(text), "AGENTS.md contains no credential-like string")
    instructions = sorted(Path(".github/instructions").glob("*.instructions.md"))
    scoped = [p for p in instructions if "src/transformation" in str(front_matter(p).get("applyTo", ""))]
    report.check(
        bool(scoped), "an .github/instructions/*.instructions.md file has applyTo scoped to src/transformation"
    )


def lab_2(report: Report) -> None:
    """Feedback loop: a narrow terminal allowlist and at least one dbt unit test."""
    settings = Path(".vscode/settings.json")
    report.check(settings.is_file(), ".vscode/settings.json exists")
    if settings.is_file():
        # Strip // comments: VS Code settings are JSON with comments
        raw = re.sub(r"^\s*//.*$", "", settings.read_text(encoding="utf-8"), flags=re.MULTILINE)
        # VS Code also tolerates trailing commas
        raw = re.sub(r",(\s*[}\]])", r"\1", raw)
        try:
            allowlist = json.loads(raw).get("chat.tools.terminal.autoApprove", {})
        except json.JSONDecodeError as error:
            print(f"FAIL  .vscode/settings.json is not valid JSON: {error}")  # noqa: T201
            allowlist = None
        report.check(
            isinstance(allowlist, dict) and bool(allowlist), "chat.tools.terminal.autoApprove is a non-empty object"
        )
        approved = [
            key
            for key, value in (allowlist or {}).items()
            if value is True or (isinstance(value, dict) and value.get("approve") is True)
        ]
        # A plain string key matches the start of a command ("just dbt-unit" also approves "just dbt-unit-x"),
        # so only anchored regular expressions of one exact recipe are accepted.
        too_broad = [key for key in approved if not EXACT_RECIPE_RULE.fullmatch(key)]
        report.check(
            bool(approved) and not too_broad,
            f"auto-approved commands are anchored regexes of exact recipes, like /^uv run just dbt-unit$/ "
            f"(too broad: {too_broad or 'none'})",
        )
    report.check(unit_test_count() >= 1, "at least one dbt unit test is declared under models/")


def lab_3(report: Report) -> None:
    """Skill: a SKILL.md whose name matches its folder, with a specific description."""
    skills = sorted(Path(".github/skills").glob("*/SKILL.md"))
    report.check(bool(skills), "a skill exists in .github/skills/<name>/SKILL.md")
    for skill in skills:
        meta = front_matter(skill)
        report.check(meta.get("name") == skill.parent.name, f"{skill}: `name` matches the folder name")
        description = str(meta.get("description", ""))
        report.check(40 <= len(description) <= 1024, f"{skill}: `description` is specific (40 to 1024 characters)")
    report.check(unit_test_count() >= 2, "at least two dbt unit tests are declared under models/ (DN-2 and DN-3)")


def lab_4(report: Report) -> None:
    """Review agent: a custom agent restricted to read-only tools."""
    agents = sorted(Path(".github/agents").glob("*.agent.md"))
    report.check(bool(agents), "a custom agent exists in .github/agents/*.agent.md")
    for agent in agents:
        meta = front_matter(agent)
        tools = meta.get("tools")
        report.check(isinstance(tools, list) and bool(tools), f"{agent}: `tools` is an explicit, non-empty list")
        unknown = sorted(set(map(str, tools or [])) - READ_ONLY_TOOLS)
        report.check(not unknown, f"{agent}: only read-only tools (not allowed: {unknown or 'none'})")
        report.check(not meta.get("handoffs") and not meta.get("agents"), f"{agent}: no handoffs and no subagents")
        body = agent.read_text(encoding="utf-8").lower()
        report.check(
            "data" in body and "instruction" in body, f"{agent}: body tells the agent to treat reviewed content as data"
        )


CHECKS: dict[str, list[Callable[[Report], None]]] = {
    "lab-1": [lab_1],
    "lab-2": [lab_2],
    "lab-3": [lab_3],
    "lab-4": [lab_4],
}


def main(base_ref: str) -> int:
    """Runs the checks of the lab targeted by the pull request."""
    checks = CHECKS.get(base_ref)
    if checks is None:
        print(f"No lab checks for '{base_ref}'.")  # noqa: T201
        return 0
    report = Report()
    for check in checks:
        check(report)
    return 1 if report.failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else ""))
