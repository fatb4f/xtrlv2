#!/usr/bin/env python
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MIGRATION_TOOLS = Path(__file__).resolve().parent


def run_py(script_name: str, passthrough_args: list[str]) -> int:
    script = MIGRATION_TOOLS / script_name
    cmd = [sys.executable, str(script), *passthrough_args]
    return subprocess.call(cmd, cwd=ROOT)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Canonical xtrlv2 migration and validation entrypoint."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("state-migrate", help="run state_migrate tool").add_argument(
        "args", nargs=argparse.REMAINDER
    )
    sub.add_parser("state-doctor", help="run state_doctor tool").add_argument(
        "args", nargs=argparse.REMAINDER
    )
    sub.add_parser("run-golden-packet", help="run golden packet harness").add_argument(
        "args", nargs=argparse.REMAINDER
    )
    sub.add_parser(
        "final-validate", help="run migration final validation checks"
    ).add_argument("args", nargs=argparse.REMAINDER)

    args = parser.parse_args()
    command_args = getattr(args, "args", [])

    if args.command == "state-migrate":
        return run_py("state_migrate.py", command_args)
    if args.command == "state-doctor":
        return run_py("state_doctor.py", command_args)
    if args.command == "run-golden-packet":
        return run_py("run_golden_packet.py", command_args)
    if args.command == "final-validate":
        return run_py("final_validate.py", command_args)

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
