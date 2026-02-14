#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

TOOLS_DIR = Path(__file__).resolve().parents[1]
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from _util import load_json, state_root, validate_artifact  # noqa: E402

REQUIRED_DIRS = ["queue", "out", "locks", "promote", "worktrees", "ledger"]
OPTIONAL_ARTIFACTS = [
    ("queue/work_queue.json", "work_queue"),
    ("queue/rank_policy.json", "rank_policy"),
    ("queue/candidate_set.json", "candidate_set"),
    ("ledger/latest.json", "latest_state"),
]


def check_or_create_dirs(
    root: Path, create_missing: bool
) -> tuple[list[str], list[str]]:
    created: list[str] = []
    missing: list[str] = []

    for rel_path in REQUIRED_DIRS:
        path = root / rel_path
        if path.exists():
            continue
        if create_missing:
            path.mkdir(parents=True, exist_ok=True)
            created.append(rel_path)
        else:
            missing.append(rel_path)

    return created, missing


def validate_optional_artifacts(root: Path) -> list[dict[str, str]]:
    invalid: list[dict[str, str]] = []

    for rel_path, kind in OPTIONAL_ARTIFACTS:
        path = root / rel_path
        if not path.exists():
            continue
        try:
            obj = load_json(path)
            validate_artifact(kind, obj)
        except Exception as exc:  # noqa: BLE001
            invalid.append(
                {"path": rel_path, "artifact_kind": kind, "error": str(exc).strip()}
            )

    return invalid


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate xtrlv2 runtime state layout and optional artifact schema health."
    )
    parser.add_argument(
        "--state-root",
        default=str(state_root()),
        help="state root to validate (default: resolved state_root)",
    )
    parser.add_argument(
        "--create-missing",
        action="store_true",
        help="create required directories if missing",
    )
    args = parser.parse_args()

    root = Path(args.state_root).resolve()
    created_dirs, missing_dirs = check_or_create_dirs(root, args.create_missing)
    invalid_artifacts = validate_optional_artifacts(root)

    ok = not missing_dirs and not invalid_artifacts
    result: dict[str, Any] = {
        "ok": ok,
        "state_root": str(root),
        "required_dirs": REQUIRED_DIRS,
        "created_dirs": created_dirs,
        "missing_dirs": missing_dirs,
        "invalid_artifacts": invalid_artifacts,
    }
    print(json.dumps(result, sort_keys=True))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
