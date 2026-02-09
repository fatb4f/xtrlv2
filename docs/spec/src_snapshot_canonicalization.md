# src/ Snapshot Canonicalization (Python)

This spec defines deterministic ordering and normalization for src/ snapshots.

## Inputs
- Source tree: `src/`
- Python files: `**/*.py`
- Root mapping: `src/<pkg>/...` → module `pkg.*`

## Output files
- `evidence/dep_graph.json`
- `evidence/api_surface.json`
- `evidence/module_manifest.json`

## Canonicalization rules (apply to all JSON outputs)
1. **Stable ordering**
   - Sort all lists lexicographically.
   - Sort object keys alphabetically.
2. **Normalized paths**
   - Use POSIX paths (`/`).
   - Paths are repo-relative.
3. **Deterministic module names**
   - `src/pkg/mod.py` → `pkg.mod`
   - `src/pkg/__init__.py` → `pkg`
4. **No derived randomness**
   - No timestamps in snapshots.

## dep_graph.json (module → imports)
Schema (conceptual):
- `modules[]`: list of modules
- `edges[]`: `{from, to, kind}`
  - `kind` in `{import, from_import}`
- `unresolved[]`: imports that cannot be resolved to a module

Rules:
- Extract imports via `ast.parse` only.
- Ignore dynamic imports (e.g., `importlib`) unless statically resolvable.
- Sort `edges` by `from`, then `to`, then `kind`.

## api_surface.json (public API surface)
Rules:
- Public API is derived from `src/<pkg>/__init__.py` only.
- If `__all__` exists: public = entries in `__all__`.
- Else: public = top-level assigned names + imported names (stable heuristic).
- Sort exported names lexicographically.

## module_manifest.json (files/modules + inferred layer)
Rules:
- Each entry: `{path, module, layer}`
- `layer` inferred from `control/src_conventions.json` layer map.
- Sort entries by `module`.

## Determinism test
- Same tree → identical JSON outputs (byte-for-byte).
- Output must be diff-friendly (no timestamps, no volatile fields).
