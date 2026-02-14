# Gate matrix

One row per gate. Keep entries short, auditable, and enforceable.

**Legend**
- **Layer**: precheck | schema-pin | conformance | tests | promote | branch-protection
- **Enforced in main**: `yes` means required status checks / protected branch behavior blocks merge.

| gate_id | layer | owner | trigger_path | command | failure_reason_codes | evidence_artifact | enforced_in_main |
|---|---|---|---|---|---|---|---|
| G-PRE-001-clean-repo | precheck | Migration Maintainers | CI + local tooling | `git status --porcelain` must be empty | `REPO_DIRTY` | CI log + runner stderr | no |
| G-POL-001-ast-grep-policy | precheck | Migration Maintainers | GitHub Actions (`schema-ssot-gate`) on PR + push main | `ast-grep scan --config sgconfig.yml` | `POLICY_VIOLATION` | ast-grep output in CI logs | yes |
| G-SSOT-001-migration-doc-consistency | schema-pin | Migration Maintainers | GitHub Actions (`schema-ssot-gate`) on PR + push main | `python tools/migration/migrate_check.py` | `MIGRATION_DOC_DRIFT` | command stdout/stderr | yes |
| G-CONF-001-schema-conformance | conformance | Migration Maintainers | GitHub Actions (`schema-ssot-gate`) on PR + push main | `pytest -q tests/test_reason_codes_schema.py tests/test_gate_decision_schema.py tests/test_helper_event_schema.py tests/test_ledger_latest_schema.py tests/test_src_snapshot_schemas.py tests/test_schema_examples_validate.py` | `SCHEMA_NONCONFORMANT`, `ARTIFACT_OUT_OF_DATE` | pytest output (+ junit if configured) | yes |
| G-PY-001-ruff-lint | tests | Migration Maintainers | GitHub Actions (`python-quality-gate`) on PR + push main | `ruff check .` | `LINT_FAILED` | CI logs (+ junit if configured) | yes |
| G-PY-002-ruff-format | tests | Migration Maintainers | GitHub Actions (`python-quality-gate`) on PR + push main | `ruff format --check .` | `FORMAT_FAILED` | CI logs | yes |
| G-PY-003-pytest-suite | tests | Migration Maintainers | GitHub Actions (`python-quality-gate`) on PR + push main | `pytest -q` | `TEST_FAILURE` | pytest output (+ junit) | yes |
| G-PROM-001-release-tag | promote | Release Maintainers | release workflow | release command (TBD) | `RELEASE_BLOCKED` | release notes + tag | no |
| G-BP-001-main-required-checks | branch-protection | Repo Admins | GitHub branch protection | require `schema-ssot-gate` + `python-quality-gate` checks | `STATUS_CHECK_REQUIRED` | GitHub settings + merge UI | yes |

## Notes
- Replace `Migration Maintainers` with concrete team/person as part of issue `#2` closeout.
- Expand `failure_reason_codes` to match the repo's canonical taxonomy.
- If a gate writes explicit evidence files, link them here and standardize locations.

## Negative test checklist (one per gate)
- G-SSOT-001: intentionally break migration tracker/doc linkage -> `python tools/migration/migrate_check.py` fails.
- G-CONF-001: break a schema example or schema file -> schema conformance test suite fails.
- G-BP-001: verify merge is blocked when checks are failing.
