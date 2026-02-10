set quiet := true

migrate-check:
    @python tools/migration/migrate_check.py

migrate-dry:
    @python tools/migration/migrate.py --dry-run

inventory-xtrl:
    @python tools/migration/inventory_xtrl.py --xtrl-root /home/src404/src/xtrl --out-dir docs/migration
