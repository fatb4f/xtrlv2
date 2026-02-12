# Issue #2 Implementation Checklist

Scope: make schema SSOT checks preventive on `main` (not advisory), then extend to Python quality gates.

## Baseline
- [ ] Confirm `.github/workflows/schema-ssot-gate.yml` runs on `pull_request` and `push` to `main`.
- [ ] Confirm workflow/job names are stable: `schema-ssot-gate` / `ssot-gate`.
- [ ] Confirm required commands are runnable in CI context.

## Branch protection
- [ ] Enable branch protection on `main`.
- [ ] Require status check: `schema-ssot-gate / ssot-gate`.
- [ ] Require branches to be up to date before merge.
- [ ] Include administrators.

## Verification evidence
- [ ] Open a PR with an intentional gate failure and confirm merge is blocked.
- [ ] Open/refresh a PR with passing checks and confirm merge is allowed.
- [ ] Capture evidence links:
  - failing run URL:
  - blocked merge screenshot/URL:
  - passing run URL:

## Python gates (follow-on)
- [ ] Add `python-quality-gate` workflow.
- [ ] Add `ruff check .` gate.
- [ ] Add `ruff format --check .` gate.
- [ ] Add `pytest -q` gate.
- [ ] Bind all required checks in branch protection.

## Closeout criteria
- [ ] `GATE_MATRIX.md` rows reflect real enforcement state.
- [ ] `TRACKER.md` M2-T02 and M2-T03 marked done with evidence.
- [ ] `STATUS.md` updated with completion date and next phase.
