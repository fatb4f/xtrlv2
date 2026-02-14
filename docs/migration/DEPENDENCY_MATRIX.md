# Migration Dependency Matrix

Legend: X depends on Y.

| Work Item | Depends On |
| --- | --- |
| M1-T01 ReasonCodes schema (SSOT) | none |
| M1-T02 Gate decision bundle (SSOT) | M1-T01 |
| M1-T03 helper_created schema | M1-T01 |
| M1-T04 Ledger/latest schemas | M1-T01 |
| M1-T05 Phase E snapshot schemas | M1-T01 |
| M2-T01 external compatibility bridge validation | M1-T01, M1-T02, M1-T03, M1-T04, M1-T05 |
| M2-T02 required branch gates on `main` | M2-T01 |
| M2-T03 Python quality gates (`ruff` + `pytest`) | M2-T02 |
| M2-T04 refactoring quality contract | M2-T03 |
| M3-T01 migration report schema (`migration_report`) | M2-T03 |
| M3-T02 state migration tool (`state_migrate.py`) | M3-T01 |
| M3-T03 state doctor validator (`state_doctor.py`) | M3-T02 |
| M4-T01 packet pre-contract schema (`packet_pre_contract`) | M3-T03 |
| M4-T02 golden packet execution harness (`run_golden_packet.py`) | M4-T01 |
| M4-T03 golden packet regression tests | M4-T02 |
| M5-T01 canonical migration CLI (`xtrlv2.py`) | M4-T02 |
| M5-T02 cutover documentation (`cutover.md`, `cli_changes.md`) | M5-T01 |
| M6-T01 final validation tool (`final_validate.py`) | M5-T02 |
| M6-T02 final guard workflow (`migration-final-guards`) | M6-T01 |
| M6-T03 final report draft (`final_report.md`) | M6-T01 |

## Rationale (short)
- `reason_codes` is foundational and referenced by multiple downstream schemas/artifacts.
- Compatibility validation should happen only after SSOT contracts are stable.
- Branch protection must be active before quality gates are fully enforceable.
- Refactoring policy is operationally meaningful only once core quality gates are in place.
- Migration tool outputs should be schema-bound before applying state changes.
- State doctor should validate post-migration layout before M4 runtime harness work.
- Golden packet harness requires a stable packet contract shape.
- Cutover docs should point to a canonical v2 entrypoint rather than individual scripts.
- Final validation and guard workflows should land after core migration tooling exists.
