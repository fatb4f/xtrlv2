# Contract codegen

This directory provides a deterministic runner to generate Pydantic v2 contract models from SSOT JSON Schemas.

## Inputs (SSOT)
- `control/ssot/schemas/*.schema.json`

## Manifest
- `tools/contracts/codegen_manifest.json`

## Outputs (generated)
- `src/xtrl_contracts/...` (never hand-edit)

## Run
```bash
python tools/contracts/gen.py
```

## Regen-and-compare gate (CI)
```bash
python tools/contracts/gen.py
git diff --exit-code
```

## Notes
- This runner invokes `python -m datamodel_code_generator` to respect the active venv.
- `--disable-timestamp` is enabled for deterministic output.
