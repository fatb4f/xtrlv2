set quiet := true

migrate-check:
    @python tools/migration/migrate_check.py

migrate-dry:
    @python tools/migration/migrate.py --dry-run

inventory-xtrl:
    @python tools/migration/inventory_xtrl.py --xtrl-root ../xtrl --out-dir docs/migration

# Usage: just loop-tick <run_id> <PRECHECK|PLAN|EXEC|CHECK|GATE>
loop-tick RUN_ID PHASE:
    @python tools/migration/loop_tick.py --run-id {{RUN_ID}} --phase {{PHASE}}
