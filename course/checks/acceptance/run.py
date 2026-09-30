"""Run the product owner's acceptance tests that apply to a lab branch.

Usage: `uv run python course/checks/acceptance/run.py lab-3`

The tests are dbt singular data tests. They are copied into the dbt project temporarily, then the
offline build runs, so they check the behaviour on the sample wherever the fix is implemented.
"""

from pathlib import Path
import subprocess  # noqa: S404
import shutil
import sys
import re


HERE = Path(__file__).parent
DBT_TESTS = Path("src/transformation/dbt_paris_event_analyzer/tests/acceptance")


def lab_number(base_ref: str) -> int:
    """Returns N for `lab-N`, 0 for any other branch."""
    match = re.fullmatch(r"lab-(\d+)", base_ref)
    return int(match.group(1)) if match else 0


def main(base_ref: str) -> int:
    """Copies the acceptance tests of labs 1..N, runs the offline build and cleans up."""
    number = lab_number(base_ref)
    suites = [HERE / f"lab-{n}" for n in range(1, number + 1) if (HERE / f"lab-{n}").is_dir()]
    if not suites:
        print(f"No acceptance tests for '{base_ref}'.")  # noqa: T201
        return 0
    DBT_TESTS.mkdir(parents=True, exist_ok=True)
    try:
        for suite in suites:
            for test in suite.glob("*.sql"):
                shutil.copy(test, DBT_TESTS / test.name)
        return subprocess.call(["just", "dbt-build-ci"])  # noqa: S603, S607
    finally:
        shutil.rmtree(DBT_TESTS)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else ""))
