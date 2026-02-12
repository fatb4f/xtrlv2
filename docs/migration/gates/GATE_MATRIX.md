# Gate matrix

One row per gate. Keep entries short, auditable, and enforceable.

**Legend**
- **Layer**: precheck | schema-pin | conformance | tests | promote | branch-protection
- **Enforced in main**: `yes` means required status checks / protected branch behavior blocks merge.

| gate_id | layer | owner | trigger_path | command | failure_reason_codes | evidence_artifact | enforced_in_main |
|---|---|---|---|---|---|---|---|
| G-PRE-001-clean-repo | precheck | Migration Maintainers | CI + local tooling | `git status --porcelain` must be empty | `REPO_DIRTY` | CI log + runner stderr | no |
| G-SSOT-001-pin-check | schema-pin | Migration Maintainers | GitHub Actions (target: PR + push main) | `just ssot-pin-check` | `SSOT_PIN_MISMATCH`, `SSOT_PIN_MISSING` | command stdout + `control/ssot_pin.json` | no |
| G-CONF-001-schema-conformance | conformance | Migration Maintainers | GitHub Actions (target: PR + push main) | `pytest -q tests/test_ssot_conformance.py` | `SCHEMA_NONCONFORMANT`, `ARTIFACT_OUT_OF_DATE` | pytest output (+ junit if configured) | no |
| G-CONF-002-m2-t01-pin-test | conformance | Migration Maintainers | GitHub Actions (target: PR + push main) | `pytest -q tests/test_ssot_pin_check_m2_t01.py` | `PIN_CHECK_FAILED` | pytest output (+ junit if configured) | no |
| G-PY-001-ruff-lint | tests | Migration Maintainers | GitHub Actions (planned) | `ruff check .` | `LINT_FAILED` | CI logs (+ junit if configured) | no |
| G-PY-002-ruff-format | tests | Migration Maintainers | GitHub Actions (planned) | `ruff format --check .` | `FORMAT_FAILED` | CI logs | no |
| G-PY-003-pytest-suite | tests | Migration Maintainers | GitHub Actions (planned) | `pytest -q` | `TEST_FAILURE` | pytest output (+ junit) | no |
| G-PROM-001-release-tag | promote | Release Maintainers | release workflow | `just release` (or equivalent) | `RELEASE_BLOCKED` | release notes + tag | no |
| G-BP-001-main-required-checks | branch-protection | Repo Admins | GitHub branch protection | require `schema-ssot-gate` checks | `STATUS_CHECK_REQUIRED` | GitHub settings + merge UI | no |

## Notes
- Replace `Migration Maintainers` with concrete team/person as part of issue `#2` closeout.
- Expand `failure_reason_codes` to match the repo's canonical taxonomy.
- If a gate writes explicit evidence files, link them here and standardize locations.
- `enforced_in_main` is set to `no` until branch protection and required checks are actually configured.

## Negative test checklist (one per gate)
- G-SSOT-001: intentionally change expected SSOT hash -> `just ssot-pin-check` fails.
- G-CONF-001: break a conformance rule/fixture -> conformance test fails.
- G-CONF-002: change pin schema target incorrectly -> pin test fails.
- G-BP-001: verify merge is blocked when checks are failing.
