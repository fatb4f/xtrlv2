# Cutover Plan

Goal: make `xtrlv2` the default operational path and deprecate v1 usage.

## Preconditions

1. M3 state migration tool and doctor validator are merged.
2. M4 packet harness regression (`run-golden-packet`) is green in CI.
3. Branch protection requires `ssot-gate`, `python-quality`, and `final-guards`.

## Cutover steps

1. Migrate legacy state into `xtrlv2` root:
   - `python tools/migration/xtrlv2.py state-migrate --source-root <legacy> --target-root <v2> --report-json <...> --report-md <...>`
2. Validate resulting state layout:
   - `python tools/migration/xtrlv2.py state-doctor --state-root <v2>`
3. Run deterministic packet harness regression:
   - `python tools/migration/xtrlv2.py run-golden-packet --contract control/ssot/examples/packet_pre_contract.example.json --out-root migration/runtime/golden_packet`
4. Run final validation gate:
   - `python tools/migration/xtrlv2.py final-validate`
5. Update operational docs to reference v2 command path only.

## v1 deprecation signoff

- Effective date: 2026-02-14
- Status: `xtrl` actuator/runbook commands are deprecated for operational usage.
- Approved command path: `python tools/migration/xtrlv2.py ...`
- Legacy `xtrl` state may still be referenced only as migration input (`--source-root`).

## Rollback

If cutover validation fails:
- Keep v1 as operational fallback.
- Preserve migration reports and doctor output.
- Fix failing gate and rerun cutover sequence.
