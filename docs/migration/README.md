# Migration Docs

Entry points:
- `WORKPLAN.md` — milestone plan and required deliverables
- `TRACKER.md` — authoritative task list and status
- `STATUS.md` — current phase and next actions
- `DEPENDENCY_MATRIX.md` / `DAG.md` — dependency views
- `GIT_STRATEGY_AND_PYTHON_GATES.md` — git governance status and Python gate rollout plan
- `QUALITY_REFACTORING_CONTRACT.md` — repeatable pattern baseline + feedback loop contract
- `tools/migration/state_migrate.py` — one-time state migration tool (dry-run/apply + report outputs)
- `tools/migration/state_doctor.py` — state layout validator/repair helper
- `tools/migration/run_golden_packet.py` — deterministic packet harness for evidence-tree regression
- `tools/migration/xtrlv2.py` — canonical migration/cutover CLI entrypoint
- `tools/migration/final_validate.py` — post-migration artifact/guard validator
- `cutover.md` / `cli_changes.md` / `final_report.md` — cutover and closeout docs
- `gate/git/git_plant_plan_review.md` — review findings for the concise git-plant implementation plan

Usage
- Update `STATUS.md` whenever migration docs/tools change.
- Use `python tools/migration/migrate_check.py` to validate doc consistency.
