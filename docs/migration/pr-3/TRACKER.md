# PR #3 Tracker

Scope: Python actuator cutover for migration gates and standalone `xtrlv2` posture.

PR: https://github.com/fatb4f/xtrlv2/pull/3

## Work items

| ID | Item | Status | Evidence |
|---|---|---|---|
| PR3-T01 | Convert `schema-ssot-gate` to run on `pull_request` + `push` | Done | `.github/workflows/schema-ssot-gate.yml` |
| PR3-T02 | Replace `just` gate commands with Python-native commands | Done | `.github/workflows/schema-ssot-gate.yml`, `docs/migration/gates/*.md` |
| PR3-T03 | Add `python-quality-gate` workflow (`ruff` + `pytest`) | Done | `.github/workflows/python-quality-gate.yml` |
| PR3-T04 | Enable required checks on `main` branch protection | Done | required checks configured: `schema-ssot-gate / ssot-gate`, `python-quality-gate / python-quality` |
| PR3-T05 | Align migration docs with standalone `xtrlv2` intent | Done | `docs/migration/TRACKER.md`, `docs/migration/DEPENDENCY_MATRIX.md`, `docs/migration/DAG.md` |
| PR3-T08 | Add ast-grep policy gate to block legacy actuator drift | Done | `sgconfig.yml`, `.ast-grep/rules/*.yml`, `schema-ssot-gate` |
| PR3-T09 | Define refactoring pattern + feedback contract | Done | `docs/migration/QUALITY_REFACTORING_CONTRACT.md` |
| PR3-T06 | Capture failing and passing PR run links for Issue #2 audit | Done | `docs/migration/gates/ISSUE_2_IMPLEMENTATION_CHECKLIST.md` |
| PR3-T07 | Resolve `ruff` lint/format baseline debt to make quality gate green | Done | `ruff check .` and `ruff format --check .` pass locally |

## Validation snapshot

- `python tools/migration/migrate_check.py` -> pass
- schema suite (`tests/test_*schema*.py`) -> pass
- `pytest -q` -> pass
- `ruff check .` -> pass
- `ruff format --check .` -> pass

## Exit criteria for PR #3 closeout

1. Both required checks are green on the PR branch.
2. Issue #2 checklist includes failing + passing run evidence links.
3. M2-T02 and M2-T03 can be marked done in `docs/migration/TRACKER.md`.
