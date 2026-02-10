#!/usr/bin/env python
import argparse
import json
import os
from pathlib import Path
from typing import Dict, List

EXCLUDE_DIRS = {".git", "__pycache__", ".venv", ".mypy_cache", ".pytest_cache"}


def list_tree(root: Path) -> Dict[str, List[str]]:
    top_level_dirs = []
    top_level_files = []
    for entry in sorted(root.iterdir(), key=lambda p: p.name):
        if entry.name in EXCLUDE_DIRS:
            continue
        if entry.is_dir():
            top_level_dirs.append(entry.name)
        else:
            top_level_files.append(entry.name)

    # Shallow inventory of known roots
    categories = {
        "top_level_dirs": top_level_dirs,
        "top_level_files": top_level_files,
    }

    def list_files(rel_dir: str) -> List[str]:
        path = root / rel_dir
        if not path.exists() or not path.is_dir():
            return []
        results = []
        for p in sorted(path.rglob("*"), key=lambda p: p.as_posix()):
            if p.is_dir():
                continue
            if any(part in EXCLUDE_DIRS for part in p.parts):
                continue
            results.append(str(p.relative_to(root)))
        return results

    for rel in ["control", "packets", "schemas", "tools", "templates", "docs", "state", "ledger", "out", "skills", "skills-pack"]:
        categories[f"files::{rel}"] = list_files(rel)

    return categories


def build_mapping(root: Path) -> List[Dict[str, str]]:
    # Deterministic initial mapping (placeholder actions)
    # Action: PORT/REPLACE/DROP/DEFER
    mapping = []

    def add(src: str, dest: str, action: str, notes: str) -> None:
        mapping.append({
            "source": src,
            "target": dest,
            "action": action,
            "notes": notes,
        })

    add("control/", "control/ssot/", "PORT", "SSOT already exists in v2; align schemas and policies.")
    add("schemas/", "control/ssot/schemas/", "REPLACE", "v2 owns schemas; map/merge as needed.")
    add("tools/", "tools/", "PORT", "Runtime tooling to be ported selectively.")
    add("packets/", "packets/", "REPLACE", "v2 packet formats may differ; normalize then port.")
    add("templates/", "(tbd)", "DEFER", "Decide if templates live in v2 or tooling.")
    add("docs/", "docs/", "PORT", "Migration docs should move; keep as sources of truth.")
    add("state/", "(v2 state root)", "REPLACE", "State layout changes handled in migration tool.")
    add("ledger/", "(v2 state root)", "REPLACE", "Ledger schema and location to be finalized.")
    add("out/", "(v2 state root)", "REPLACE", "Out dir layout to be defined by v2 evidence capsule.")
    add("skills/", "(tbd)", "DEFER", "Decide: keep in v1 only or port.")
    add("skills-pack/", "(tbd)", "DEFER", "Decide: keep in v1 only or port.")
    add("worktrees/", "(v2 state root)", "REPLACE", "Worktree layout defined in v2 state model.")
    add("xtrl (entrypoint)", "xtrlv2 entrypoint", "REPLACE", "Define new canonical CLI and wrapper.")

    return mapping


def write_mapping(md_path: Path, mapping: List[Dict[str, str]]) -> None:
    lines = [
        "# xtrl -> xtrlv2 Mapping",
        "",
        "Classification: PORT / REPLACE / DROP / DEFER",
        "",
        "| Source | Target | Action | Notes |",
        "| --- | --- | --- | --- |",
    ]
    for row in mapping:
        lines.append(f"| `{row['source']}` | `{row['target']}` | **{row['action']}** | {row['notes']} |")
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Inventory xtrl repo and produce mapping")
    parser.add_argument("--xtrl-root", required=True, help="Path to xtrl repo root")
    parser.add_argument("--out-dir", required=True, help="Output dir for docs/migration")
    args = parser.parse_args()

    xtrl_root = Path(args.xtrl_root).resolve()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    inventory = list_tree(xtrl_root)
    inventory_path = out_dir / "inventory_xtrl.json"
    inventory_path.write_text(json.dumps(inventory, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    mapping = build_mapping(xtrl_root)
    mapping_path = out_dir / "mapping.md"
    write_mapping(mapping_path, mapping)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
