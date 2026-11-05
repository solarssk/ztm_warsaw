"""Checks that the commit being released is a mainline commit that passed the CI checks that matter.

Used by .github/workflows/release.yml after a version tag is pushed. The workflow
saves the first-parent history of main (``git rev-list --first-parent origin/main``,
one SHA per line) and the check runs of the tagged commit (``gh api
.../commits/<sha>/check-runs``, one JSON object per line: id, name, status, conclusion,
app, check suite), the ci.yml workflow runs for that commit (``gh api
.../actions/workflows/ci.yml/runs?head_sha=<sha>&event=push&branch=main``, one JSON
object per line: id, check_suite_id, event, head_branch, head_sha), and passes the
files and the tagged SHA here.

The tagged commit must be in the first-parent history of main: the merge commit of a
release pull request, or a fast-forwarded one. A commit of the merged branch is an
ancestor of main too, but it lacks the merge result and the other mainline changes,
and its pull-request CI runs would satisfy the name-based check below.

Every check in REQUIRED must have completed with ``success``, as reported by the
GitHub Actions app, inside a check suite of a ci.yml run that was a push to main for
this very commit. The checks API lists every check run of a commit, whatever started
it, and a fast-forwarded release commit already carries successful, same-named runs
of its pull request, so the suite is what proves that CI ran on main; for a check that ran more than once (a re-run) the newest run
counts. A check from any other app, with the same name, does not count.

REQUIRED is the set of jobs of ci.yml that run on a push to main. It is the branch
protection list minus "Documentation impact declaration" (that check only runs on
pull requests, so a merge commit never has it) plus "HACS validation" (not required
to merge, because it needs the network) and "Compat smoke (minimum Home Assistant)"
(not required to merge, because it installs an old Home Assistant), both required to
release. The names are the
``name:`` of the jobs in ci.yml; a test keeps the two in step.

Messages are built from constants only: the check names below, never text from the
API.
"""

from __future__ import annotations

import json
import sys
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any

REQUIRED = (
    "Lint (ruff)",
    "Type check (mypy)",
    "Tests (pytest)",
    "Hassfest",
    "Dependency audit (pip-audit)",
    "Secret scan (gitleaks)",
    "Lint workflows (actionlint, zizmor)",
    "Release bookkeeping",
    "HACS validation",
    "Compat smoke (minimum Home Assistant)",
    "Compat smoke (current Home Assistant)",
)
APP = "github-actions"

MSG_NOT_MAINLINE = "The tagged commit is not on the first-parent line of main (it is a commit of a merged branch, or not on main at all). Tag the merge commit on main."
MSG_NO_PUSH_RUN = "CI has not run on main for the tagged commit (checks from its pull request do not count). Wait for the push run of ci.yml on main, or re-run it."
MSG_MISSING = "The tagged commit has no '{name}' check from GitHub Actions. Wait for CI on main to finish, or push the tag on a commit that went through main."
MSG_RUNNING = "The '{name}' check on the tagged commit has not finished. Re-run this workflow when it has."
MSG_FAILED = "The '{name}' check on the tagged commit did not succeed. Fix it (or re-run it if it was a network error) before releasing."


def on_mainline(commit: str, mainline: Iterable[str]) -> bool:
    """True if ``commit`` (a full 40-character SHA) is one of the SHAs in ``mainline``."""
    wanted = commit.strip().lower()
    if len(wanted) != 40 or any(c not in "0123456789abcdef" for c in wanted):
        return False
    return any(line.strip().lower() == wanted for line in mainline)


def push_suites(workflow_runs: Iterable[Mapping[str, Any]], commit: str) -> set[int]:
    """The check suites of the ci.yml runs that were a push to main for ``commit``."""
    wanted = commit.strip().lower()
    suites: set[int] = set()
    for run in workflow_runs:
        suite = run.get("check_suite_id")
        head_sha = run.get("head_sha")
        if (
            run.get("event") == "push"
            and run.get("head_branch") == "main"
            and isinstance(head_sha, str)
            and head_sha.lower() == wanted
            and isinstance(suite, int)
        ):
            suites.add(suite)
    return suites


def newest_runs(runs: Iterable[Mapping[str, Any]], suites: set[int]) -> dict[str, Mapping[str, Any]]:
    """The newest GitHub Actions run of each check name (the highest id) inside one of ``suites``."""
    newest: dict[str, Mapping[str, Any]] = {}
    for run in runs:
        name = run.get("name")
        if run.get("app") != APP or run.get("check_suite") not in suites or not isinstance(name, str):
            continue
        run_id = run.get("id")
        if not isinstance(run_id, int):
            continue
        previous = newest.get(name)
        if previous is None or run_id > previous["id"]:
            newest[name] = run
    return newest


def problems(runs: Iterable[Mapping[str, Any]], suites: set[int]) -> list[str]:
    """Return what keeps the commit from being released; an empty list means it may be."""
    if not suites:
        return [MSG_NO_PUSH_RUN]
    newest = newest_runs(runs, suites)
    found: list[str] = []
    for name in REQUIRED:
        run = newest.get(name)
        if run is None:
            found.append(MSG_MISSING.format(name=name))
        elif run.get("status") != "completed":
            found.append(MSG_RUNNING.format(name=name))
        elif run.get("conclusion") != "success":
            found.append(MSG_FAILED.format(name=name))
    return found


def read_runs(path: Path) -> list[dict[str, Any]]:
    """Parse the JSON-lines file written by the workflow; a line that is not an object is an error."""
    runs = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        run = json.loads(line)
        if not isinstance(run, dict):
            raise ValueError("the check-runs file holds a line that is not a JSON object")
        runs.append(run)
    return runs


def main(argv: list[str] | None = None) -> int:
    """Check from the four files the workflow gives (check runs, workflow runs, the mainline commits, the commit being released) that the commit is on main and its required CI checks succeeded; 0 if so, 1 with the problems on stderr, 2 for a wrong usage."""
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 4:
        print(
            "usage: release_preflight.py <check-runs.jsonl> <workflow-runs.jsonl> <mainline.txt> <commit-sha>",
            file=sys.stderr,
        )
        return 2
    try:
        runs = read_runs(Path(args[0]))
        workflow_runs = read_runs(Path(args[1]))
        mainline = Path(args[2]).read_text(encoding="utf-8").splitlines()
    except (OSError, ValueError):
        print("release-preflight: an input file is missing or not valid.", file=sys.stderr)
        return 1
    commit = args[3]
    found = problems(runs, push_suites(workflow_runs, commit))
    if not on_mainline(commit, mainline):
        found.insert(0, MSG_NOT_MAINLINE)
    if found:
        for problem in found:
            print(f"release-preflight: {problem}", file=sys.stderr)
        return 1
    print("release-preflight: the tagged commit is on main and every required CI check on it succeeded.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
