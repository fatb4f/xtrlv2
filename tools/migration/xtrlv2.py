#!/usr/bin/env python
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MIGRATION_TOOLS = Path(__file__).resolve().parent
COMMAND_MAP = {
    "state-migrate": "state_migrate.py",
    "state-doctor": "state_doctor.py",
    "run-golden-packet": "run_golden_packet.py",
    "final-validate": "final_validate.py",
}


def run_py(script_name: str, passthrough_args: list[str]) -> int:
    script = MIGRATION_TOOLS / script_name
    cmd = [sys.executable, str(script), *passthrough_args]
    return subprocess.call(cmd, cwd=ROOT)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Canonical xtrlv2 migration and validation entrypoint."
    )
    parser.add_argument(
        "command",
        choices=sorted(COMMAND_MAP.keys()),
        help="migration command to execute",
    )

    args, passthrough_args = parser.parse_known_args()
    return run_py(COMMAND_MAP[args.command], passthrough_args)


if __name__ == "__main__":
    raise SystemExit(main())
