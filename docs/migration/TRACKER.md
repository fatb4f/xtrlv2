# Migration Tracker (Authoritative)

Goal: establish xtrlv2 as a standalone SSOT + execution toolchain for post-pivot features.

## Source of Truth
- xtrlv2: SSOT schemas, gates, and runtime policies
- xtrl: external compatibility reference only (not an actuator dependency)

## Current State
- SSOT update landed in xtrlv2: commit `0fdb685`
- New SSOT schemas now include `control_strategy` and `guardrails_bundle` (registered)
- ReasonCodes schema is implemented in SSOT (`reason_codes` v0.1)
- xtrlv2 gap tracker: https://github.com/fatb4f/xtrlv2/issues/1

## Work Items (ordered, blocking-first)
1. **M1-T01** ReasonCodes schema (SSOT) — formalize `reason_codes.json` as a schema-bound artifact.
2. **M1-T02** Gate decision bundle — decide gate_worker vs gate_decision+run_manifest+evidence_capsule.
3. **M1-T03** helper_created event schema — JSONL envelope + payload.
4. **M1-T04** Ledger/latest pointer schemas — if required by runtime.
5. **M1-T05** Phase E snapshot schemas — dep_graph, api_surface, module_manifest.
6. **M2-T01** Validate external compatibility bridge (xtrl artifacts against xtrlv2 SSOT), without reusing xtrl actuators in xtrlv2.
7. **M2-T04** Refactoring quality contract — define repeatable design-pattern baseline + MCP-assisted feedback workflow.

## Work Item Details (executable checklist)
Format: keep entries short and auditable.

### M1-T01 — ReasonCodes schema (SSOT)
- Repo: xtrlv2
- Artifacts: `control/ssot/reason_codes.json`, `control/ssot/schemas/reason_codes.schema.json`
- Schema refs: `reason_codes` v0.1 (new)
- Tests: schema validation; example file validates; negative case for unknown code
- Status: Done (pushed)
- Owner: TBD
- Links: (PR/commit)
- DoD gate: schema validation + example + negative case
- Evidence:
  - Touched files: `control/ssot/reason_codes.json`, `control/ssot/schemas/reason_codes.schema.json`, `control/ssot/registry.json`, `control/ssot/examples/reason_codes.example.json`, `tests/test_reason_codes_schema.py`
  - Validation: `UV_CACHE_DIR=/tmp/uv-cache uv run --with jsonschema --with pytest python -m pytest -q tests/test_reason_codes_schema.py tests/test_schema_examples_validate.py`
    - Key output: `4 passed in 0.07s`
  - Commit: `328806e`
- Blockers: none

### M1-T02 — Gate decision bundle choice
- Repo: xtrlv2
- Artifacts: `control/ssot/schemas/gate_decision.schema.json`, `control/ssot/schemas/run_manifest.schema.json`, `control/ssot/schemas/evidence_capsule.schema.json`
- Schema refs: `gate_decision` v0.1 + `run_manifest` v0.1 + `evidence_capsule` v0.1 (canonical bundle)
- Tests: schema validation; golden example; negative case for missing reason code
- Status: Done (pushed)
- Owner: TBD
- Links: `docs/migration/decisions/M1-T02-gate-bundle.md`
- DoD gate: schema validation + example + negative case
- Evidence:
  - Touched files: `tests/test_gate_decision_schema.py`, `docs/migration/decisions/M1-T02-gate-bundle.md`, `docs/migration/TRACKER.md`, `docs/migration/STATUS.md`
  - Validation: `UV_CACHE_DIR=/tmp/uv-cache uv run --with jsonschema --with pytest python -m pytest -q tests/test_gate_decision_schema.py tests/test_schema_examples_validate.py`
    - Key output: `3 passed in 0.07s`
  - Commit: `328806e`
- Blockers: none

### M1-T03 — helper_created event schema
- Repo: xtrlv2
- Artifacts: `control/ssot/schemas/helper_event.schema.json`, `control/ssot/examples/helper_event.example.json`
- Schema refs: helper event v0.1
- Tests: schema validation; example JSONL line validates; negative case for missing required fields
- Status: Done (pushed)
- Owner: TBD
- Links: (PR/commit)
- DoD gate: schema validation + example + negative case
- Evidence:
  - Touched files: `control/ssot/schemas/helper_event.schema.json`, `control/ssot/examples/helper_event.example.json`, `control/ssot/registry.json`, `tests/test_helper_event_schema.py`, `docs/migration/TRACKER.md`
  - Validation: `UV_CACHE_DIR=/tmp/uv-cache uv run --with jsonschema --with pytest python -m pytest -q tests/test_reason_codes_schema.py tests/test_gate_decision_schema.py tests/test_helper_event_schema.py tests/test_ledger_latest_schema.py tests/test_src_snapshot_schemas.py tests/test_schema_examples_validate.py`
    - Key output: `15 passed in 0.10s`
  - Commit: `328806e`
- Blockers: none

### M1-T04 — Ledger/latest pointer schemas
- Repo: xtrlv2
- Artifacts: `control/ssot/schemas/ledger_entry.schema.json`, `control/ssot/schemas/latest_state.schema.json`, `control/ssot/examples/ledger_entry.example.json`, `control/ssot/examples/latest_state.example.json`
- Schema refs: ledger/latest v0.1
- Tests: schema validation; example validates; negative case for missing base_ref/run_id
- Status: Done (pushed)
- Owner: TBD
- Links: (PR/commit)
- DoD gate: schema validation + example + negative case
- Evidence:
  - Touched files: `control/ssot/schemas/ledger_entry.schema.json`, `control/ssot/schemas/latest_state.schema.json`, `control/ssot/examples/ledger_entry.example.json`, `control/ssot/examples/latest_state.example.json`, `control/ssot/registry.json`, `tests/test_ledger_latest_schema.py`, `docs/migration/TRACKER.md`
  - Validation: `UV_CACHE_DIR=/tmp/uv-cache uv run --with jsonschema --with pytest python -m pytest -q tests/test_reason_codes_schema.py tests/test_gate_decision_schema.py tests/test_helper_event_schema.py tests/test_ledger_latest_schema.py tests/test_src_snapshot_schemas.py tests/test_schema_examples_validate.py`
    - Key output: `15 passed in 0.10s`
  - Commit: `328806e`
- Blockers: none

### M1-T05 — Phase E snapshot schemas
- Repo: xtrlv2
- Artifacts: `control/ssot/schemas/dep_graph.schema.json`, `control/ssot/schemas/api_surface.schema.json`, `control/ssot/schemas/module_manifest.schema.json`, `control/ssot/examples/dep_graph.example.json`, `control/ssot/examples/api_surface.example.json`, `control/ssot/examples/module_manifest.example.json`
- Schema refs: snapshots v0.1
- Tests: schema validation; example validates; negative case for unstable ordering
- Status: Done (pushed)
- Owner: TBD
- Links: (PR/commit)
- DoD gate: schema validation + example + negative case
- Evidence:
  - Touched files: `control/ssot/schemas/dep_graph.schema.json`, `control/ssot/schemas/api_surface.schema.json`, `control/ssot/schemas/module_manifest.schema.json`, `control/ssot/examples/dep_graph.example.json`, `control/ssot/examples/api_surface.example.json`, `control/ssot/examples/module_manifest.example.json`, `control/ssot/registry.json`, `tests/test_src_snapshot_schemas.py`, `docs/migration/TRACKER.md`
  - Validation: `UV_CACHE_DIR=/tmp/uv-cache uv run --with jsonschema --with pytest python -m pytest -q tests/test_reason_codes_schema.py tests/test_gate_decision_schema.py tests/test_helper_event_schema.py tests/test_ledger_latest_schema.py tests/test_src_snapshot_schemas.py tests/test_schema_examples_validate.py`
    - Key output: `15 passed in 0.10s`
  - Commit: `328806e`
- Blockers: none

### M2-T01 — external compatibility bridge validation
- Repo: xtrl (external bridge evidence), tracked from xtrlv2
- Artifacts: pinned schema hash file, conformance validator, bridge evidence
- Schema refs: all SSOT items above
- Tests: schema pin gate; artifact conformance gate (B–E)
- Status: Done (pushed)
- Owner: TBD
- Links: `e329450`
- DoD gate: schema pin + artifact conformance
- Evidence:
  - Commit: `e329450`
  - Validation (external bridge run in `xtrl`): `python tools/ssot_gate.py pin --pin-file control/ssot_pin.json --ssot-root /home/src404/src/xtrlv2/control/ssot`; `pytest -q tests/test_ssot_pin_check_m2_t01.py tests/test_ssot_conformance.py`
  - Key output: `4 passed`
- Blockers: none

### M2-T02 — Activate required branch gates on `main`
- Repo: xtrlv2
- Artifacts: `.github/workflows/schema-ssot-gate.yml`, branch protection config evidence
- Schema refs: n/a (policy enforcement)
- Tests: failing PR cannot merge; passing PR can merge
- Status: In progress
- Owner: TBD
- Links: `docs/migration/gates/MAIN_BRANCH_ENFORCEMENT.md`, issue `#2`
- DoD gate: required status checks active in branch protection
- Evidence:
  - Checklist: `docs/migration/gates/ISSUE_2_IMPLEMENTATION_CHECKLIST.md`
  - Branch protection update applied (2026-02-14):
    - required checks: `schema-ssot-gate / ssot-gate`, `python-quality-gate / python-quality`
    - strict/up-to-date: enabled
    - enforce admins: enabled
- Blockers: capture failing/pass PR run links for audit evidence

### M2-T03 — Python quality gates (`ruff` + `pytest`)
- Repo: xtrlv2
- Artifacts: `python-quality-gate` workflow, gate matrix rows, branch protection required checks
- Schema refs: n/a (quality gates)
- Tests: lint/format/test failures block merge
- Status: In progress
- Owner: TBD
- Links: `docs/migration/GIT_STRATEGY_AND_PYTHON_GATES.md`
- DoD gate: required checks enforce Python quality on `main`
- Evidence:
  - Workflow added: `.github/workflows/python-quality-gate.yml`
  - Local validation snapshot (2026-02-14):
    - `UV_CACHE_DIR=/tmp/uv-cache uv run --with pytest --with jsonschema python -m pytest -q` -> `15 passed`
    - `UV_CACHE_DIR=/tmp/uv-cache uv run --with ruff ruff check .` -> `All checks passed!`
    - `UV_CACHE_DIR=/tmp/uv-cache uv run --with ruff ruff format --check .` -> `17 files already formatted`
- Blockers: pending CI run links in issue `#2` evidence checklist

### M2-T04 — Refactoring quality contract
- Repo: xtrlv2
- Artifacts: `docs/migration/QUALITY_REFACTORING_CONTRACT.md`
- Schema refs: n/a (engineering quality policy)
- Tests: policy referenced from migration docs; gate commands remain deterministic
- Status: Done (pushed)
- Owner: TBD
- Links: `docs/migration/QUALITY_REFACTORING_CONTRACT.md`
- DoD gate: explicit pattern baseline + feedback loop contract documented
- Evidence:
  - Touched files: `docs/migration/QUALITY_REFACTORING_CONTRACT.md`, `docs/migration/README.md`, `docs/migration/GIT_STRATEGY_AND_PYTHON_GATES.md`
  - Validation: `python tools/migration/migrate_check.py` (docs consistency remains green)
- Blockers: none

## Definition of Done
- SSOT covers all post-pivot artifacts.
- xtrlv2 emits and validates schema-valid artifacts for B–E.
- Drift checks prevent schema divergence.

## Operational Gates (stop rules)
- xtrlv2 cannot add new artifact shapes unless an xtrlv2 schema exists or an approved temporary extension is recorded.
- Schema pin gate must fail on mismatch between xtrl and xtrlv2 schema hash.
- Artifact conformance gate must fail when xtrlv2 artifacts violate SSOT schemas.

## Migration Health Signals
- % of emitted artifacts passing SSOT schema validation (CI).
- Count of remaining SSOT gaps (from Work Items 1–5).
- Schema hash pinned + verified (Yes/No).

## References
- xtrlv2 SSOT catch-up: https://github.com/fatb4f/xtrlv2/issues/1
- xtrl schema gap map: `reports/xtrl_vs_xtrlv2_schema_mapping.md`
- alignment checklist: `reports/xtrlv2-cross-repo-alignment-checklist.md`
- pivot report: `reports/xtrlv2-migration-pivot-report.md`
- git plant plan review: `docs/migration/gate/git/git_plant_plan_review.md`
