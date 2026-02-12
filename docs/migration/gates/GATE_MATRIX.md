# Gate matrix

One row per gate. Keep entries short, auditable, and enforceable.

**Legend**
- **Layer**: precheck | schema-pin | conformance | tests | promote | branch-protection
- **Enforced in main**: `yes` means required status checks / protected branch behavior blocks merge.

| gate_id | layer | owner | trigger_path | command | failure_reason_codes | evidence_artifact | enforced_in_main |
|---|---|---|---|---|---|---|---|
| G-PRE-001-clean-repo | precheck | TBD | CI + local tooling | `git status --porcelain` must be empty | `REPO_DIRTY` | CI log + runner stderr | no |
| G-SSOT-001-pin-check | schema-pin | TBD | GitHub Actions (PR + push main) | `just ssot-pin-check` | `SSOT_PIN_MISMATCH`, `SSOT_PIN_MISSING` | command stdout + `control/ssot_pin.json` | **yes** |
| G-CONF-001-schema-conformance | conformance | TBD | GitHub Actions (PR + push main) | `pytest -q tests/test_ssot_conformance.py` | `SCHEMA_NONCONFORMANT`, `ARTIFACT_OUT_OF_DATE` | pytest output (+ junit if configured) | **yes** |
| G-CONF-002-m2-t01-pin-test | conformance | TBD | GitHub Actions (PR + push main) | `pytest -q tests/test_ssot_pin_check_m2_t01.py` | `PIN_CHECK_FAILED` | pytest output (+ junit if configured) | **yes** |
| G-TEST-001-unit-suite | tests | TBD | CI (optional initially) | `pytest -q` (full suite) | `TEST_FAILURE` | pytest output (+ junit) | no |
| G-PROM-001-release-tag | promote | TBD | release workflow | `just release` (or equivalent) | `RELEASE_BLOCKED` | release notes + tag | no |
| G-BP-001-main-required-checks | branch-protection | Repo Admins | GitHub branch protection | require `schema-ssot-gate` checks | `STATUS_CHECK_REQUIRED` | GitHub settings + merge UI | **yes** |

## Notes
- Replace `owner` with a concrete team/person.
- Expand `failure_reason_codes` to match the repo’s canonical taxonomy (if present).
- If a gate writes explicit evidence files, link them here and standardize locations.

## Negative test checklist (one per gate)
- G-SSOT-001: intentionally change expected SSOT hash → `just ssot-pin-check` fails.
- G-CONF-001: break a conformance rule/fixture → conformance test fails.
- G-CONF-002: change pin schema target incorrectly → pin test fails.
- G-BP-001: verify merge is blocked when checks are failing.
