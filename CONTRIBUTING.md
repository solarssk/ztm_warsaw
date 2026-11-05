# Contributing to ztm_warsaw

Thanks for your interest in contributing. This document covers the practical steps for proposing a
change. The rules the checks enforce, and the list of identifiers that must not change, are in
[AGENTS.md](AGENTS.md).

## Before you start

- For anything beyond a small fix, start a discussion or open an issue first, so we agree on the
  approach before you spend time on it.
- Search the existing issues and discussions first; someone may already be on it.
- Found a security vulnerability? Do **not** open a public issue. Follow [SECURITY.md](SECURITY.md).

## Ways to contribute

| Type | Where to start |
|---|---|
| Bug report | Use the [issue form](https://github.com/solarssk/ztm_warsaw/issues/new?template=bug.yml) ("Bug report / feature request") with Type: Bug. Say which Home Assistant and integration versions you run and what you expected. Remove your API key from every log and screenshot first. |
| Question or help with setup | Ask in [Discussions](https://github.com/solarssk/ztm_warsaw/discussions), for example how to find a stop ID or a pole number, or why a sensor shows "No service". |
| Feature request | Start a [Discussion](https://github.com/solarssk/ztm_warsaw/discussions) describing the goal and what "done" looks like, or, for a small and well-defined one, use the same issue form with Type: Feature request. |
| Code change | Branch, then open a pull request (see below). |
| Documentation | The front page is [README.md](README.md); the user manual is the wiki, published from [docs/wiki/](docs/wiki) (edit the files there, in a pull request). Release notes are written in [CHANGELOG.md](CHANGELOG.md). How the tests are organised is in [tests/README.md](tests/README.md). |

## Development setup

You need Python 3.14.2 or newer. The tests run a real Home Assistant, whose release and minimum Python are
pinned by `pytest-homeassistant-custom-component` in `requirements_test.txt`.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --require-hashes -r .github/locks/test.txt
```

CI installs from the hash-locked files in `.github/locks/` (Scorecard's Pinned-Dependencies check, and a changed package on PyPI cannot slip in). `requirements_test.txt` and `.github/compat/min-ha.txt` stay the files you edit; after changing a pin, copy it to the matching `.in` file and regenerate the lock, for example
`uv pip compile --generate-hashes --python-platform linux --python-version 3.14.2 .github/locks/test.in -o .github/locks/test.txt` (the minimum-Home-Assistant lock uses `--python-version 3.13.2`). `tests/test_locks.py` fails when they disagree.

The additional `Compat smoke (current Home Assistant)` job boots Core 2026.11.0 directly, configures a line against the local fake City, checks its sensor and unloads the entry. It uses `.github/locks/ha-current.in` and its complete hash lock, independently of the pytest plugin, which still pins Core 2026.10.4. Run it with `python -m tests.compat.native_smoke` in an environment installed from that lock. Regenerate the lock with the same compile command above, replacing `test.in` and `test.txt` with `ha-current.in` and `ha-current.txt`. This smoke check does not replace the full pytest suite.

The integration itself must stay valid for Home Assistant 2026.1 and Python 3.13, even though CI
runs newer versions.

## Translations

The texts of the integration are in `custom_components/ztm_warsaw/translations/`: `en.json` is the source, and `pl`, `uk`, `ru`, `de`, `es`, `fr` and `it` are translated (all but Polish by machine, so a correction from a native speaker is a welcome pull request). The standard for how the texts are written, and for the words of the transport vocabulary, is [docs/LOCALIZATION.md](docs/LOCALIZATION.md). A new language is a copy of `en.json` with every text translated; `tests/test_translations.py` checks that a file has exactly the keys of `en.json` and keeps every `{placeholder}`, paragraph break and link. When you add or change a text in `en.json`, add it to every language file in the same pull request. The README is in the same eight languages (`README.md` is English, the others are `README.<code>.md`); `tests/test_readmes.py` checks that they have the same sections and that every link in them works. When you change the English README, change the others too.

## Running the checks

CI runs these on every pull request; run them before you open one.

```bash
ruff check .
python scripts/check_mypy_baseline.py
pytest
```

- `pytest` takes about ten seconds. It runs the integration inside a real Home Assistant against a
  fake City of Warsaw server on your own machine, so it needs no network and no API key. Add
  `--cov` for a coverage report.
- `scripts/check_mypy_baseline.py` runs `mypy custom_components/ztm_warsaw` in strict mode (`strict = true` in
  `pyproject.toml`: every function is annotated) and compares its diagnostics with
  `.github/mypy-baseline.txt`, the same way CI does. The list is empty: any diagnostic fails the check,
  so annotate what you add. `python scripts/check_mypy_baseline.py --update` rewrites the entries if a
  diagnostic must be accepted for a while (say why in the pull request).
- A test against the real API exists (`tests/live/`) but is opt-in. It makes a handful of requests,
  never prints the key, and never runs in CI:

  ```bash
  ZTM_LIVE_API_KEY=<your key> pytest -m live tests/live
  ```

- CI also runs hassfest and the HACS validation, a dependency audit of the pinned tooling,
  gitleaks, and actionlint and zizmor on the workflow files. One repository check is cheap to run
  yourself: `python scripts/release_check.py` (the `manifest.json` version has notes in
  `CHANGELOG.md`). The Documentation impact declaration is checked only in CI, against the
  description of your pull request (see below).
- A user-visible change gets a `CHANGELOG.md` entry under `[Unreleased]`. The changelog is the release notes that
  Home Assistant users read, so write it for them: one line with a bold title and one short, friendly sentence about what
  they get, for example `- **A calendar of departures**: switch it on to see the whole day in Home Assistant's calendar.`
  Leave the technical details to the pull request; `tests/test_changelog_style.py` checks the form.

## Making a change

1. Branch from `main` with a prefix and a short slug:

   | Prefix | Use for |
   |---|---|
   | `feature/<slug>` | New functionality |
   | `fix/<slug>` | Bug fixes |
   | `chore/<slug>` | Maintenance, dependencies, tooling |
   | `docs/<slug>` | Documentation only |
   | `ci/<slug>` | Workflows and CI configuration |
   | `test/<slug>` | Tests only |
   | `release/vX.Y.Z` | A release commit |

2. Write Conventional Commit messages and pull request titles: `feat:`, `fix:`, `docs:`, `chore:`,
   `test:`, `ci(scope):`, and `release: vX.Y.Z` for a release commit.

3. **Changes to what the integration does come with tests.** A bug fix adds a test that fails
   without the fix, or, if the bug is already pinned by a `@known_bug(...)` test in `tests/e2e/`,
   removes that mark (strict mode turns a fix that forgets to red). A new feature is not done
   without a test of its behaviour. Documentation, CI and test-only changes need none.

4. Do not change an entity ID, a `unique_id`, a device identifier, an attribute name or a config
   entry key without a migration: see "The public contract is frozen" in [AGENTS.md](AGENTS.md).

5. Match the style of the file you are editing, and keep the diff to what the change needs.

6. **Every module, class and function has a docstring** (private and nested ones too; `test_*` functions are the
   exception) that says what it is for and what it promises. Someone returns to this code after months and has none
   of today's context. `python scripts/check_docstrings.py` (also run by pytest) tells you what is missing.

## Using AI coding tools

AI-assisted contributions are welcome. The same bar applies as to any other contribution: you are
responsible for what you submit, not the tool that helped write it.

- Read and understand every line before you submit it.
- Run it: build, type-check and run the real test suite. "Looks correct" is not a result.
- Keep the diff scoped to the issue; do not let an agent "improve" adjacent code.
- Do not invent: no made-up APIs, no confident claims about behaviour you have not checked.

## Opening a pull request

Use the repository's [pull request template](.github/pull_request_template.md) and keep its
headings. Fill in "Documentation impact": a check compares your declaration with the files you
changed, and the pull request cannot merge while they disagree.

`main` is protected. A pull request needs these checks to pass, and its branch to be up to date
with `main` (use the "Update branch" button). The repository administrator can bypass the rule, so
that a broken CI can still be repaired; by habit, nothing is pushed to `main` directly.

The required checks:

- `Lint (ruff)`
- `Type check (mypy)`
- `Tests (pytest)`
- `Hassfest`
- `Dependency audit (pip-audit)`
- `Secret scan (gitleaks)`
- `Lint workflows (actionlint, zizmor)`
- `Release bookkeeping`
- `Documentation impact declaration`

`HACS validation` is not required to merge, because it depends on the network, but it must pass
before a release. So must `Compat smoke (minimum Home Assistant)`: it runs the whole test suite on the
oldest Home Assistant the integration claims (2026.1, Python 3.13; the pin is in `.github/compat/`),
because every other job runs the newest. To run it locally, build a Python 3.13 environment and
install `.github/compat/min-ha.txt`, then `python -m pytest tests`. The Codecov, SonarCloud and Scorecard results are signals, not gates.

This is a single-maintainer project. [@solarssk](https://github.com/solarssk) reviews and merges
every pull request, including their own, once the required checks are green, and sets the `type:`
label, the milestone of the release it lands in and the assignee. Automated reviewers (Codex, and
CodeRabbit on request) may comment on your pull request; their findings are input, not verdicts.

## Releases and maintenance

- A release is a version in `manifest.json`, its notes in `CHANGELOG.md`, and a tag; the procedure
  is in the header of [`.github/workflows/release.yml`](.github/workflows/release.yml). The
  workflow prepares a draft GitHub Release, and publishing it by hand is what makes HACS offer it.
- Once a month, run `gh workflow list --all` and check that no workflow shows as
  `disabled_inactivity`. GitHub disables a workflow that has a `schedule:` trigger after 60 days
  without repository activity, and a disabled workflow stops running on pull requests too; this is
  what happened to the old HACS and hassfest workflows. `ci.yml` has no `schedule:` for that reason,
  so today only `scorecard.yml` (and CodeQL's weekly run) can be hit.
- At every minor release, look at the triggers in [AGENTS.md](AGENTS.md) that would call for a
  review of the repository's tier, and run the playbook's checks including the repository
  settings, which the `Verify standard` workflow cannot read without an admin token (it runs on
  every pull request and reports only):

  ```bash
  [ -d ../playbook ] || git clone https://github.com/solarssk/playbook.git ../playbook
  git -C ../playbook fetch --tags origin
  git -C ../playbook checkout "$(gh release view --repo solarssk/playbook --json tagName --jq .tagName)"
  GITHUB_REPOSITORY=solarssk/ztm_warsaw GH_TOKEN="$(gh auth token)" ADMIN_TOKEN="$(gh auth token)" \
    node ../playbook/scripts/verify-tier.mjs
  ```

  The two middle lines move the checkout to the playbook's latest release on every run, so a check
  that a newer release added is not missed by a clone that was made a year ago. Expected: no
  failures, and the two warnings listed in AGENTS.md (`sast`, `readme-opens-well`).

## Questions

Open a [discussion](https://github.com/solarssk/ztm_warsaw/discussions), or reach [@solarssk](https://github.com/solarssk).
