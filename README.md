# Base Spec + SSOT Spine Repo

This repository is a minimal scaffold for **spec-first development** plus an **SSOT-governed state-machine artifact graph**.

## Structure
- `docs/` — spec-kit-derived templates (SPEC/PLAN/TASKS/CHECKLIST)
- `control/ssot/` — schemas + examples + registry + reason codes
- `tests/` — schema/example validation

## Quick check
```bash
python -m venv .venv && . .venv/bin/activate
pip install -U pip
pip install jsonschema pytest
pytest -q
```
