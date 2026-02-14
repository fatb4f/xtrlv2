# CLI Changes (v1 -> v2)

This document tracks migration-time CLI mapping while `xtrlv2` becomes the standalone default.

## Canonical v2 entrypoint

Use:

```bash
python tools/migration/xtrlv2.py <command> [args...]
```

Supported commands:
- `state-migrate`
- `state-doctor`
- `run-golden-packet`
- `final-validate`

## Compatibility mapping

| Legacy pattern | v2 command |
|---|---|
| state migration scripts (ad-hoc) | `python tools/migration/xtrlv2.py state-migrate ...` |
| state layout checks | `python tools/migration/xtrlv2.py state-doctor ...` |
| packet harness smoke run | `python tools/migration/xtrlv2.py run-golden-packet ...` |
| post-migration validation checks | `python tools/migration/xtrlv2.py final-validate` |

## Notes

- `xtrlv2` is standalone and should not depend on `xtrl` actuator scripts.
- `xtrl` may still be referenced as a legacy source-state input for one-time migration.
- Direct operational invocation of `tools/migration/state_migrate.py`, `state_doctor.py`, `run_golden_packet.py`, and `final_validate.py` is deprecated in runbooks; use `tools/migration/xtrlv2.py` subcommands.
