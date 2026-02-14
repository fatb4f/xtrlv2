# Issue #2 Implementation Checklist

Scope: make schema SSOT checks preventive on `main` (not advisory), then extend to Python quality gates.

## Baseline
- [x] Confirm `.github/workflows/schema-ssot-gate.yml` runs on `pull_request` and `push` to `main`.
- [x] Confirm workflow/job names are stable: `schema-ssot-gate` / `ssot-gate`.
- [x] Confirm required commands are runnable in CI context.
- [x] Confirm migration policy checks run via `ast-grep scan --config sgconfig.yml`.

## Branch protection
- [x] Enable branch protection on `main`.
- [x] Require status check: `schema-ssot-gate / ssot-gate`.
- [x] Require branches to be up to date before merge.
- [x] Include administrators.

## Verification evidence
- [x] Open a PR with an intentional gate failure and confirm merge is blocked.
- [x] Open/refresh a PR with passing checks and confirm merge is allowed once branch policy requirements are met.
- [x] Capture evidence links:
  - failing run URL: https://github.com/fatb4f/xtrlv2/actions/runs/22011677068/job/63606647917
  - blocked merge proof URL: https://github.com/fatb4f/xtrlv2/pull/3 (CLI proof: `gh pr merge 3 --merge --delete-branch` -> "base branch policy prohibits the merge")
  - passing run URL: https://github.com/fatb4f/xtrlv2/actions/runs/22011688947/job/63606678737

## Python gates (follow-on)
- [x] Add `python-quality-gate` workflow.
- [x] Add `ruff check .` gate.
- [x] Add `ruff format --check .` gate.
- [x] Add `pytest -q` gate.
- [x] Bind all required checks in branch protection.

## Closeout criteria
- [x] `GATE_MATRIX.md` rows reflect real enforcement state.
- [x] `TRACKER.md` M2-T02 and M2-T03 marked done with evidence.
- [x] `STATUS.md` updated with completion date and next phase.
