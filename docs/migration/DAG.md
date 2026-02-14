# Migration DAG

```
ReasonCodes (SSOT)
  ├─ Gate decision bundle (SSOT)
  ├─ helper_created schema
  ├─ Ledger/latest schemas
  └─ Phase E snapshot schemas
        └─ external compatibility bridge validation (depends on all SSOT)
```

Notes:
- Gate decision bundle unlocks Phase B/C/D correctness.
- helper_created / ledger / snapshots can proceed once reason codes are fixed.
- External compatibility validation is last to avoid churn in SSOT definitions.
