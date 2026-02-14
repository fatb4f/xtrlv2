# Migration Tracker (Authoritative)

Goal: establish xtrlv2 as a standalone SSOT + execution toolchain for post-pivot features.

## Source of Truth
- xtrlv2: SSOT schemas, gates, and runtime policies
- xtrl: external compatibility reference only (not an actuator dependency)

## Current State
- SSOT update landed in xtrlv2: commit `0fdb685`
- New SSOT schemas now include `control_strategy` and `guardrails_bundle` (registered)
- ReasonCodes schema is implemented in SSOT (`reason_codes` v0.1)
- M1/M2/M3 milestone implementations are merged to `main`
- Active milestone evidence tracking: issue `#5` (M4), issue `#6` (M5), issue `#7` (M6)

## Work Items (ordered, blocking-first)
1. **M1-T01** ReasonCodes schema (SSOT) — formalize `reason_codes.json` as a schema-bound artifact.
2. **M1-T02** Gate decision bundle — decide gate_worker vs gate_decision+run_manifest+evidence_capsule.
3. **M1-T03** helper_created event schema — JSONL envelope + payload.
4. **M1-T04** Ledger/latest pointer schemas — if required by runtime.
5. **M1-T05** Phase E snapshot schemas — dep_graph, api_surface, module_manifest.
6. **M2-T01** Validate external compatibility bridge (xtrl artifacts against xtrlv2 SSOT), without reusing xtrl actuators in xtrlv2.
7. **M2-T02** Activate required branch gates on `main`.
8. **M2-T03** Python quality gates (`ruff` + `pytest`).
9. **M2-T04** Refactoring quality contract — define repeatable design-pattern baseline + MCP-assisted feedback workflow.
10. **M3-T01** Add `migration_report` schema + example and register it in SSOT.
11. **M3-T02** Implement `tools/migration/state_migrate.py` (dry-run/apply + report emission + idempotence).
12. **M3-T03** Implement `tools/migration/state_doctor.py` (layout validator + optional repair).
13. **M4-T01** Add `packet_pre_contract` schema + example to SSOT.
14. **M4-T02** Implement deterministic golden packet execution harness (`run_golden_packet.py`).
15. **M4-T03** Add regression tests for golden packet evidence tree.
16. **M5-T01** Add canonical xtrlv2 migration CLI entrypoint (`tools/migration/xtrlv2.py`).
17. **M5-T02** Publish cutover docs (`cli_changes.md`, `cutover.md`).
18. **M6-T01** Add final validation tool (`tools/migration/final_validate.py`).
19. **M6-T02** Add CI final guard workflow (`migration-final-guards`).
20. **M6-T03** Publish final report draft (`docs/migration/final_report.md`).

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
- Status: Done
- Owner: TBD
- Links: `docs/migration/gates/MAIN_BRANCH_ENFORCEMENT.md`, issue `#2`
- DoD gate: required status checks active in branch protection
- Evidence:
  - Checklist: `docs/migration/gates/ISSUE_2_IMPLEMENTATION_CHECKLIST.md`
  - Branch protection update applied (2026-02-14):
    - required checks: `ssot-gate`, `python-quality`
    - strict/up-to-date: enabled
    - enforce admins: enabled
  - Intentional failure proof (2026-02-14):
    - failing required check: https://github.com/fatb4f/xtrlv2/actions/runs/22011677068/job/63606647917 (`python-quality` fail)
    - blocked merge proof: `gh pr merge 3 --merge --delete-branch` -> base branch policy prohibits merge
  - Passing proof after remediation (2026-02-14):
    - `python-quality`: https://github.com/fatb4f/xtrlv2/actions/runs/22011688947/job/63606678737 (pass)
    - `ssot-gate`: https://github.com/fatb4f/xtrlv2/actions/runs/22011688944/job/63606678711 (pass)
- Blockers: none

### M2-T03 — Python quality gates (`ruff` + `pytest`)
- Repo: xtrlv2
- Artifacts: `python-quality-gate` workflow, gate matrix rows, branch protection required checks
- Schema refs: n/a (quality gates)
- Tests: lint/format/test failures block merge
- Status: Done
- Owner: TBD
- Links: `docs/migration/GIT_STRATEGY_AND_PYTHON_GATES.md`
- DoD gate: required checks enforce Python quality on `main`
- Evidence:
  - Workflow added: `.github/workflows/python-quality-gate.yml`
  - Local validation snapshot (2026-02-14):
    - `UV_CACHE_DIR=/tmp/uv-cache uv run --with pytest --with jsonschema python -m pytest -q` -> `15 passed`
    - `UV_CACHE_DIR=/tmp/uv-cache uv run --with ruff ruff check .` -> `All checks passed!`
    - `UV_CACHE_DIR=/tmp/uv-cache uv run --with ruff ruff format --check .` -> `17 files already formatted`
  - PR #3 CI evidence (2026-02-14):
    - `python-quality`: https://github.com/fatb4f/xtrlv2/actions/runs/22011601104/job/63606437236 (pass)
    - `ssot-gate`: https://github.com/fatb4f/xtrlv2/actions/runs/22011601105/job/63606437156 (pass)
- Blockers: none

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

### M3-T01 — Migration report schema (`migration_report`)
- Repo: xtrlv2
- Artifacts: `control/ssot/schemas/migration_report.schema.json`, `control/ssot/examples/migration_report.example.json`, `control/ssot/registry.json`
- Schema refs: `migration_report` v0.1
- Tests: schema validation; example validates; negative case for missing summary
- Status: Done
- Owner: TBD
- Links: (PR/commit)
- DoD gate: report artifacts are schema-bound and included in registry-driven example validation
- Evidence:
  - Touched files: `control/ssot/schemas/migration_report.schema.json`, `control/ssot/examples/migration_report.example.json`, `control/ssot/registry.json`, `tests/test_migration_report_schema.py`
  - Validation: `UV_CACHE_DIR=/tmp/uv-cache uv run --with pytest --with jsonschema python -m pytest -q tests/test_migration_report_schema.py tests/test_schema_examples_validate.py`
    - Key output: `3 passed`
- Blockers: none

### M3-T02 — State migration tool (`state_migrate.py`)
- Repo: xtrlv2
- Artifacts: `tools/migration/state_migrate.py`, `migration/runtime/migration_report.json`, `migration/runtime/migration_report.md`
- Schema refs: `migration_report` v0.1
- Tests: dry-run leaves target untouched; apply copies data; second apply run is idempotent
- Status: Done
- Owner: TBD
- Links: (PR/commit)
- DoD gate: tool emits schema-valid report json + markdown summary and supports deterministic dry-run/apply modes
- Evidence:
  - Touched files: `tools/migration/state_migrate.py`, `tools/_util.py`, `tests/test_state_migrate.py`
  - Validation:
    - `UV_CACHE_DIR=/tmp/uv-cache uv run --with pytest --with jsonschema python -m pytest -q tests/test_state_migrate.py`
    - `UV_CACHE_DIR=/tmp/uv-cache uv run --with ruff ruff check tools/migration/state_migrate.py`
  - Key output: dry-run/apply/idempotence test passes
- Blockers: none

### M3-T03 — State doctor validator (`state_doctor.py`)
- Repo: xtrlv2
- Artifacts: `tools/migration/state_doctor.py`
- Schema refs: validates optional artifacts via SSOT (`work_queue`, `rank_policy`, `candidate_set`, `latest_state`)
- Tests: missing layout fails; `--create-missing` repairs; invalid optional artifact fails validation
- Status: Done
- Owner: TBD
- Links: (PR/commit)
- DoD gate: machine-readable validator output with non-zero exit on missing dirs or invalid artifacts
- Evidence:
  - Touched files: `tools/migration/state_doctor.py`, `tests/test_state_doctor.py`
  - Validation:
    - `UV_CACHE_DIR=/tmp/uv-cache uv run --with pytest --with jsonschema python -m pytest -q tests/test_state_doctor.py`
    - `UV_CACHE_DIR=/tmp/uv-cache uv run --with ruff ruff check tools/migration/state_doctor.py`
- Blockers: production migration run evidence pending (non-blocking for implementation)

### M4-T01 — Packet pre-contract schema (`packet_pre_contract`)
- Repo: xtrlv2
- Artifacts: `control/ssot/schemas/packet_pre_contract.schema.json`, `control/ssot/examples/packet_pre_contract.example.json`, `control/ssot/registry.json`
- Schema refs: `packet_pre_contract` v0.1
- Tests: schema validation; example validates; negative case for missing required evidence files
- Status: Done
- Owner: TBD
- Links: (PR/commit)
- DoD gate: packet pre-contract format is machine-validated in SSOT
- Evidence:
  - Touched files: `control/ssot/schemas/packet_pre_contract.schema.json`, `control/ssot/examples/packet_pre_contract.example.json`, `control/ssot/registry.json`, `tests/test_packet_pre_contract_schema.py`
  - Validation: `UV_CACHE_DIR=/tmp/uv-cache uv run --with pytest --with jsonschema python -m pytest -q tests/test_packet_pre_contract_schema.py tests/test_schema_examples_validate.py`
- Blockers: none

### M4-T02 — Golden packet execution harness (`run_golden_packet.py`)
- Repo: xtrlv2
- Artifacts: `tools/migration/run_golden_packet.py`
- Schema refs: consumes `packet_pre_contract` v0.1
- Tests: harness materializes required evidence files from contract
- Status: Done
- Owner: TBD
- Links: (PR/commit)
- DoD gate: deterministic harness emits complete evidence tree for one packet run
- Evidence:
  - Touched files: `tools/migration/run_golden_packet.py`, `tests/test_run_golden_packet.py`
  - Validation: `UV_CACHE_DIR=/tmp/uv-cache uv run --with pytest --with jsonschema python -m pytest -q tests/test_run_golden_packet.py`
  - Evidence run (2026-02-14):
    - `migration/runtime/evidence/2026-02-14/run_golden_packet.stdout.json`
    - `migration/runtime/evidence/2026-02-14/golden_packet_runs/pkt-v2-migrate-0002-runner-cutover/golden-m4-20260214/golden_report.json`
- Blockers: none

### M4-T03 — Golden packet regression tests
- Repo: xtrlv2
- Artifacts: `tests/test_run_golden_packet.py`, `tests/test_packet_pre_contract_schema.py`
- Schema refs: `packet_pre_contract` v0.1
- Tests: regression test ensures required evidence files exist in harness output tree
- Status: Done
- Owner: TBD
- Links: (PR/commit)
- DoD gate: regression test suite is runnable in CI
- Evidence:
  - Validation: `UV_CACHE_DIR=/tmp/uv-cache uv run --with pytest --with jsonschema python -m pytest -q tests/test_packet_pre_contract_schema.py tests/test_run_golden_packet.py`
- Blockers: none

### M5-T01 — Canonical migration CLI (`tools/migration/xtrlv2.py`)
- Repo: xtrlv2
- Artifacts: `tools/migration/xtrlv2.py`
- Schema refs: n/a (entrypoint wrapper)
- Tests: CLI help and subcommand wiring
- Status: Done
- Owner: TBD
- Links: (PR/commit)
- DoD gate: one canonical xtrlv2 command path for migrate/doctor/harness/final validation
- Evidence:
  - Touched files: `tools/migration/xtrlv2.py`, `tests/test_xtrlv2_cli.py`
  - Validation: `UV_CACHE_DIR=/tmp/uv-cache uv run --with pytest --with jsonschema python -m pytest -q tests/test_xtrlv2_cli.py`
- Blockers: none

### M5-T02 — Cutover docs (`cli_changes.md`, `cutover.md`)
- Repo: xtrlv2
- Artifacts: `docs/migration/cli_changes.md`, `docs/migration/cutover.md`
- Schema refs: n/a
- Tests: included in final validation checks
- Status: Done
- Owner: TBD
- Links: (PR/commit)
- DoD gate: operational cutover sequence is documented with canonical CLI commands
- Evidence:
  - Touched files: `docs/migration/cli_changes.md`, `docs/migration/cutover.md`
  - Validation: `python tools/migration/final_validate.py`
  - Cutover demo run (2026-02-14):
    - `migration/runtime/evidence/2026-02-14/migration_report.json`
    - `migration/runtime/evidence/2026-02-14/state_doctor.stdout.json`
- Blockers: production environment signoff pending

### M6-T01 — Final validation tool (`final_validate.py`)
- Repo: xtrlv2
- Artifacts: `tools/migration/final_validate.py`
- Schema refs: n/a
- Tests: verifies required docs/tools/tests for migration closeout baseline
- Status: Done
- Owner: TBD
- Links: (PR/commit)
- DoD gate: explicit pass/fail validator for migration closeout artifacts
- Evidence:
  - Touched files: `tools/migration/final_validate.py`, `tests/test_final_validate.py`
  - Validation: `UV_CACHE_DIR=/tmp/uv-cache uv run --with pytest --with jsonschema python -m pytest -q tests/test_final_validate.py`
- Blockers: none

### M6-T02 — Final guard workflow (`migration-final-guards`)
- Repo: xtrlv2
- Artifacts: `.github/workflows/migration-final-guards.yml`
- Schema refs: validates packet contract/harness/final validate tests
- Tests: workflow runs final validator + targeted migration regression tests
- Status: Done
- Owner: TBD
- Links: (PR/commit)
- DoD gate: CI job exists and is green on PR/main
- Evidence:
  - Touched files: `.github/workflows/migration-final-guards.yml`
  - Validation: workflow executes `python tools/migration/final_validate.py` + regression pytest slice
- Blockers: not yet configured as required branch-protection check

### M6-T03 — Final report draft (`final_report.md`)
- Repo: xtrlv2
- Artifacts: `docs/migration/final_report.md`
- Schema refs: n/a
- Tests: included in final validation checks
- Status: Done
- Owner: TBD
- Links: (PR/commit)
- DoD gate: written migration closeout summary with remaining production evidence gaps
- Evidence:
  - Touched files: `docs/migration/final_report.md`
  - Validation: `python tools/migration/final_validate.py`
  - Consolidated evidence index: `migration/runtime/evidence/2026-02-14/evidence_summary.json`
- Blockers: production cutover evidence + branch-protection promotion signoff pending

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
- M4 evidence tracking: https://github.com/fatb4f/xtrlv2/issues/5
- M5 cutover tracking: https://github.com/fatb4f/xtrlv2/issues/6
- M6 finalization tracking: https://github.com/fatb4f/xtrlv2/issues/7
- xtrl schema gap map: `reports/xtrl_vs_xtrlv2_schema_mapping.md`
- alignment checklist: `reports/xtrlv2-cross-repo-alignment-checklist.md`
- pivot report: `reports/xtrlv2-migration-pivot-report.md`
- git plant plan review: `docs/migration/gate/git/git_plant_plan_review.md`
