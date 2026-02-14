# Migration Report

- run_id: `migrate-20260214T054110Z`
- generated_at: `2026-02-14T05:41:10.390452Z`
- mode: `apply`
- source_root: `/tmp/xtrlv2_cutover_demo/legacy_xtrl_state`
- target_root: `/tmp/xtrlv2_cutover_demo/xtrlv2_state`
- idempotent: `false`

## Summary

| status | count |
|---|---:|
| planned | 0 |
| created | 6 |
| copied | 3 |
| skipped | 0 |
| missing_source | 5 |
| conflict | 0 |
| error | 0 |

## Operations
- `created` `ensure_dir` `queue` dst=`queue`
- `created` `ensure_dir` `out` dst=`out`
- `created` `ensure_dir` `locks` dst=`locks`
- `created` `ensure_dir` `promote` dst=`promote`
- `created` `ensure_dir` `worktrees` dst=`worktrees`
- `created` `ensure_dir` `ledger` dst=`ledger`
- `copied` `migrate_file` `out/run-001/result.txt` src=`out/run-001/result.txt` dst=`out/run-001/result.txt`
- `copied` `migrate_file` `worktrees/wt-a/meta.txt` src=`worktrees/wt-a/meta.txt` dst=`worktrees/wt-a/meta.txt`
- `missing_source` `migrate_dir` `queue` src=`queue` dst=`queue`
- `missing_source` `migrate_dir` `promote` src=`promote` dst=`promote`
- `missing_source` `migrate_dir` `locks` src=`locks` dst=`locks`
- `missing_source` `migrate_dir` `ledger` src=`ledger` dst=`ledger`
- `copied` `migrate_file` `ledger/latest.json` src=`state/latest.json` dst=`ledger/latest.json`
- `missing_source` `migrate_file` `ledger/ledger.jsonl` src=`ledger/ledger.jsonl` dst=`ledger/ledger.jsonl` note=no candidate source file found
