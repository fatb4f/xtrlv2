# Quality Refactoring Contract

Purpose: ensure repeatable Python design patterns across tooling and enforce continuous feedback during refactors.

## Scope
- Applies to Python tooling under `tools/`, schema/gate helpers, and migration automation code.
- Applies to local development and CI validation.

## Functional Requirements
1. Refactors must map to an explicit design pattern choice (Refactoring Guru taxonomy), with rationale in PR notes.
2. Behavior must remain covered by `pytest` and schema conformance tests.
3. Style and consistency must pass `ruff check .` and `ruff format --check .`.
4. Migration policy drift must be blocked by `ast-grep` rules.
5. Every refactor must produce machine-verifiable feedback (lint, format, tests, policy scan).

## Pattern Baseline (Refactoring Guru-aligned)
- `Strategy`: interchangeable ranking/scoring or decision policies.
- `Adapter`: compatibility bridges between external artifacts and xtrlv2 SSOT.
- `Factory Method`: deterministic construction of run workers/executors.
- `Template Method`: shared migration/gate execution skeletons with constrained extension points.

Non-goal: introducing patterns where simpler structure is sufficient.

## Feedback System
1. Syntax/Style feedback:
   - `ruff check .`
   - `ruff format --check .`
2. Structural/policy feedback:
   - `ast-grep scan --config sgconfig.yml`
   - backed by `.ast-grep/rules/*.yml`
3. Behavioral feedback:
   - `pytest -q`
   - focused schema gate tests in `schema-ssot-gate`
4. Documentation consistency feedback:
   - `python tools/migration/migrate_check.py`

## MCP-assisted Refactor Workflow
- `ast-grep-mcp`:
  - query structural hotspots before editing
  - validate no legacy actuator patterns re-enter workflow code
- `lsp-mcp`:
  - inspect symbol-level impacts (references, diagnostics, rename safety)
  - confirm post-refactor API and call graph consistency

MCP tools are developer-assist layers. CI enforcement remains command-based and deterministic.

## Environment + Config
- Python: 3.11
- Primary runner: `uv run`
- Required tools: `ruff`, `pytest`, `jsonschema`, `@ast-grep/cli`
- Gate workflows:
  - `.github/workflows/schema-ssot-gate.yml`
  - `.github/workflows/python-quality-gate.yml`

## Exit Criteria
- No lint findings.
- No format drift.
- Tests green.
- Ast-grep policy scan green.
- Migration docs remain consistent.
