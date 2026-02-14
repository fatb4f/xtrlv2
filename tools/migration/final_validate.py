#!/usr/bin/env python
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

REQUIRED_DOCS = [
    "docs/migration/cutover.md",
    "docs/migration/cli_changes.md",
    "docs/migration/final_report.md",
]
REQUIRED_TOOLS = [
    "tools/migration/state_migrate.py",
    "tools/migration/state_doctor.py",
    "tools/migration/run_golden_packet.py",
    "tools/migration/xtrlv2.py",
]
REQUIRED_TESTS = [
    "tests/test_state_migrate.py",
    "tests/test_state_doctor.py",
    "tests/test_run_golden_packet.py",
]


def missing(paths: list[str]) -> list[str]:
    return [p for p in paths if not (ROOT / p).exists()]


def main() -> int:
    missing_docs = missing(REQUIRED_DOCS)
    missing_tools = missing(REQUIRED_TOOLS)
    missing_tests = missing(REQUIRED_TESTS)

    ok = not (missing_docs or missing_tools or missing_tests)
    payload = {
        "ok": ok,
        "missing_docs": missing_docs,
        "missing_tools": missing_tools,
        "missing_tests": missing_tests,
    }
    print(json.dumps(payload, sort_keys=True))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
