# M1-T02 Gate Bundle Decision

Date: 2026-02-11  
Status: accepted (local)

## Decision

Use the canonical gate bundle as:

- `gate_decision`
- `run_manifest`
- `evidence_capsule`

Do not introduce a separate `gate_worker` SSOT artifact in xtrlv2 for M1.

## Rationale

- The three artifacts already exist in SSOT (`registry.json`) and are schema-backed.
- This avoids duplicate gate semantics and keeps policy linkage centralized in `gate_decision`.
- It reduces migration scope and unblocks downstream M1 tasks without adding a parallel artifact family.

## Validation

- `gate_decision` example validates against schema.
- Missing `reason_codes` in `gate_decision` fails validation (negative test).
