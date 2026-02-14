# Migration Status

Current phase: M4 (Packet harness + cutover enablement)
Last updated: 2026-02-14

Next 3 actions:
1. Run `tools/migration/xtrlv2.py run-golden-packet` with a production packet pre-contract and archive evidence artifacts (issue `#5`).
2. Execute cutover sequence from `docs/migration/cutover.md` against a real migrated state root (issue `#6`).
3. Promote `migration-final-guards` to required check after one stable release cycle (issue `#7`).

Blockers:
- no code blockers; production cutover evidence artifacts are still pending.
