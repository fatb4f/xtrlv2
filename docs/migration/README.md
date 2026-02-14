# Migration Docs

Entry points:
- `WORKPLAN.md` — milestone plan and required deliverables
- `TRACKER.md` — authoritative task list and status
- `STATUS.md` — current phase and next actions
- `DEPENDENCY_MATRIX.md` / `DAG.md` — dependency views
- `GIT_STRATEGY_AND_PYTHON_GATES.md` — git governance status and Python gate rollout plan
- `QUALITY_REFACTORING_CONTRACT.md` — repeatable pattern baseline + feedback loop contract
- `gate/git/git_plant_plan_review.md` — review findings for the concise git-plant implementation plan

Usage
- Update `STATUS.md` whenever migration docs/tools change.
- Use `python tools/migration/migrate_check.py` to validate doc consistency.
