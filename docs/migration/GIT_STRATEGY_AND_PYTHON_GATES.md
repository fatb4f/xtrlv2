# Git Strategy And Python Gates

## Purpose
Record what is implemented vs missing for migration-grade git governance, and define Python file gates required to close the drift surface.

## Current status (2026-02-14)

### Implemented
- Commit history mostly follows Conventional Commit style (`feat(...)`, `docs(...)`).
- Migration gate policy docs exist under `docs/migration/gates/`.
- `schema-ssot-gate` workflow exists at `.github/workflows/schema-ssot-gate.yml`.
- `python-quality-gate` workflow exists at `.github/workflows/python-quality-gate.yml`.
- Refactoring policy contract exists at `docs/migration/QUALITY_REFACTORING_CONTRACT.md` (Refactoring Guru pattern baseline + feedback loop).

### Partial
- `schema-ssot-gate` now runs on `pull_request` + `push` to `main` using Python-native commands.
- `python-quality-gate` baseline is green locally; CI evidence links still need to be captured in issue `#2`.
- Branch protection is active with required checks, but run-evidence links for failing/passing PR cases are still pending.
- Trailer usage policy is optional and independent from xtrl runtime conventions.

### Missing
- Conventional commit enforcement gate (no `commitlint`/equivalent check).
- Changelog policy and generation path (`CHANGELOG.md` + CI/release update flow).
- Explicit trailer enforcement gate (required keys, scope, and validation).

## Python file gate plan

### Gate set (minimum)
1. `py-lint`: `ruff check .`
2. `py-format`: `ruff format --check .`
3. `py-tests`: `pytest -q`
4. `py-schema-gates`: `python tools/migration/migrate_check.py` + focused SSOT schema tests

### Optional hardening
- `py-type`: `mypy` on selected modules once type baselines exist.
- `py-security`: `bandit -q -r tools src tests` with explicit excludes.

## Refactoring workflow policy
- Pattern selection should reference Refactoring Guru taxonomy for non-trivial structural changes.
- `ast-grep-mcp` should be used for structural hotspot search and policy-preflight before edits.
- `lsp-mcp` should be used for symbol-level safety checks (references/rename/diagnostics) during edits.
- CI remains source of truth via deterministic command gates; MCP tools assist local quality and refactor speed.

### Enforcement policy
- Required on `main`: `schema-ssot-gate`, `py-lint`, `py-format`, `py-tests`.
- Keep stable workflow/job names once bound in branch protection.
- Fail-fast in CI; no soft-fail for required checks.

## Execution sequence
1. Verify `schema-ssot-gate` runs green on `pull_request` + `push` to `main`.
2. Verify `python-quality-gate` runs green with `ruff` + `pytest`.
3. Enable required checks in branch protection.
4. Add negative test evidence for each gate in `docs/migration/gates/GATE_MATRIX.md`.
5. Add changelog/trailer gates after core Python gates are green.

## Evidence to collect
- Workflow run links for first green PR and first blocked PR.
- Branch protection screenshot/config export.
- One intentional failure per required gate with remediation note.
