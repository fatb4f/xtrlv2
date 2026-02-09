#!/usr/bin/env python3
"""Contract codegen runner (deterministic).

Inputs:
  - tools/contracts/codegen_manifest.json (schema -> output mapping)

Outputs:
  - generated python modules (default under src/xtrl_contracts/...)
  - tools/contracts/codegen_hashes.json (schema + output sha256)

Notes:
  - never hand-edit generated outputs; regen-and-compare in CI
  - this runner is deliberately repo-agnostic; only paths in the manifest matter
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Entry:
    schema: Path
    output: Path


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_manifest(path: Path) -> tuple[dict[str, Any], list[Entry]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    entries: list[Entry] = []
    for e in data.get("entries", []):
        entries.append(Entry(schema=Path(e["schema"]), output=Path(e["output"])))
    if not entries:
        raise ValueError("manifest has no entries")
    return data, entries


def ensure_pkg_dirs(repo_root: Path, outputs: list[Path]) -> None:
    """Ensure generated outputs are importable packages (create __init__.py)."""
    for out in outputs:
        out_abs = (repo_root / out).resolve()
        pkg = out_abs.parent
        while True:
            # stop at repo root or at 'src'
            if pkg == repo_root or pkg.name == "src":
                break
            init = pkg / "__init__.py"
            if not init.exists():
                init.write_text("# generated package marker\n", encoding="utf-8")
            pkg = pkg.parent


def run_codegen(
    *,
    repo_root: Path,
    schema: Path,
    output: Path,
    input_file_type: str,
    output_model_type: str,
    disable_timestamp: bool,
) -> None:
    schema_abs = (repo_root / schema).resolve()
    output_abs = (repo_root / output).resolve()
    output_abs.parent.mkdir(parents=True, exist_ok=True)

    # Use module invocation to respect the active venv.
    cmd = [
        sys.executable,
        "-m",
        "datamodel_code_generator",
        "--input-file-type",
        input_file_type,
        "--output-model-type",
        output_model_type,
        "--input",
        str(schema_abs),
        "--output",
        str(output_abs),
    ]
    if disable_timestamp:
        cmd.append("--disable-timestamp")

    subprocess.run(cmd, check=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--manifest",
        default="tools/contracts/codegen_manifest.json",
        help="Path to manifest JSON (default: tools/contracts/codegen_manifest.json)",
    )
    ap.add_argument(
        "--repo-root",
        default=".",
        help="Repo root (default: current directory)",
    )
    ap.add_argument(
        "--hashes-out",
        default="tools/contracts/codegen_hashes.json",
        help="Where to write schema/output hashes",
    )
    ap.add_argument(
        "--strict",
        action="store_true",
        help="Fail if any schema/output path is missing",
    )
    args = ap.parse_args()

    repo_root = Path(args.repo_root).resolve()
    manifest_path = (repo_root / args.manifest).resolve()

    manifest, entries = load_manifest(manifest_path)

    input_file_type = manifest.get("input_file_type", "jsonschema")
    output_model_type = manifest.get("output_model_type", "pydantic_v2.BaseModel")
    disable_timestamp = bool(manifest.get("disable_timestamp", True))

    if args.strict:
        for e in entries:
            if not (repo_root / e.schema).exists():
                raise FileNotFoundError(f"missing schema: {e.schema}")

    outputs = [e.output for e in entries]
    ensure_pkg_dirs(repo_root, outputs)

    for e in entries:
        run_codegen(
            repo_root=repo_root,
            schema=e.schema,
            output=e.output,
            input_file_type=input_file_type,
            output_model_type=output_model_type,
            disable_timestamp=disable_timestamp,
        )

    hashes: dict[str, Any] = {
        "version": manifest.get("version", "0.1.0"),
        "tool": {
            "python": sys.version.split()[0],
            "generator": "datamodel-code-generator",
        },
        "entries": [],
    }

    for e in entries:
        schema_abs = (repo_root / e.schema).resolve()
        out_abs = (repo_root / e.output).resolve()

        if args.strict and not out_abs.exists():
            raise FileNotFoundError(f"missing output after codegen: {e.output}")

        hashes["entries"].append(
            {
                "schema": str(e.schema),
                "schema_sha256": sha256_file(schema_abs) if schema_abs.exists() else None,
                "output": str(e.output),
                "output_sha256": sha256_file(out_abs) if out_abs.exists() else None,
            }
        )

    hashes_out = (repo_root / args.hashes_out).resolve()
    hashes_out.parent.mkdir(parents=True, exist_ok=True)
    hashes_out.write_text(
        json.dumps(hashes, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
