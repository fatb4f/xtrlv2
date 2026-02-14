# Migration Status

Current phase: M3 (State layout + one-time migration tool)
Last updated: 2026-02-14

Next 3 actions:
1. Run `tools/migration/state_migrate.py` against a real legacy state root and attach the generated report artifacts.
2. Wire `tools/migration/state_doctor.py` into CI for periodic state-layout health checks.
3. Open M4 packet-contract migration tasks after first production migration report lands.

Blockers:
- no code blockers; production migration evidence run still pending.
