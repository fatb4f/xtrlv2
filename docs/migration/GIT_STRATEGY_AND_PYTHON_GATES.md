# Git Strategy And Python Gates

## Purpose
Record what is implemented vs missing for migration-grade git governance, and define Python file gates required to close the drift surface.

## Current status (2026-02-12)

### Implemented
- Commit history mostly follows Conventional Commit style (`feat(...)`, `docs(...)`).
- Migration gate policy docs exist under `docs/migration/gates/`.
- `schema-ssot-gate` workflow exists at `.github/workflows/schema-ssot-gate.yml`.

### Partial
- `schema-ssot-gate` is currently `workflow_dispatch` only, not yet enforcing PR/push checks.
- Branch protection policy is documented but not verified as active in repository settings.
- Trailer usage exists in runtime workflows (`Packet:`, `Evidence:`) in `xtrl`, but is not yet a formal CI gate in `xtrlv2`.

### Missing
- Conventional commit enforcement gate (no `commitlint`/equivalent check).
- Changelog policy and generation path (`CHANGELOG.md` + CI/release update flow).
- Explicit trailer enforcement gate (required keys, scope, and validation).

## Python file gate plan

### Gate set (minimum)
1. `py-lint`: `ruff check .`
2. `py-format`: `ruff format --check .`
3. `py-tests`: `pytest -q`
4. `py-schema-gates`: `just ssot-pin-check` + focused conformance tests

### Optional hardening
- `py-type`: `mypy` on selected modules once type baselines exist.
- `py-security`: `bandit -q -r tools src tests` with explicit excludes.

### Enforcement policy
- Required on `main`: `schema-ssot-gate`, `py-lint`, `py-format`, `py-tests`.
- Keep stable workflow/job names once bound in branch protection.
- Fail-fast in CI; no soft-fail for required checks.

## Execution sequence
1. Convert `schema-ssot-gate` from manual-only to `pull_request` + `push` on `main`.
2. Add `python-quality-gate` workflow with `ruff` + `pytest`.
3. Enable required checks in branch protection.
4. Add negative test evidence for each gate in `docs/migration/gates/GATE_MATRIX.md`.
5. Add changelog/trailer gates after core Python gates are green.

## Evidence to collect
- Workflow run links for first green PR and first blocked PR.
- Branch protection screenshot/config export.
- One intentional failure per required gate with remediation note.
