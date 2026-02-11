#!/usr/bin/env python
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PHASES = ["PRECHECK", "PLAN", "EXEC", "CHECK", "GATE"]
NEXT_PHASE = {
    "PRECHECK": "PLAN",
    "PLAN": "EXEC",
    "EXEC": "CHECK",
    "CHECK": "GATE",
    "GATE": "PRECHECK",
}


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def append_jsonl(path: Path, payload: dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, sort_keys=True) + "\n")


def validate_phase(phase: str) -> None:
    if phase not in PHASES:
        raise ValueError(f"invalid phase: {phase}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run one stateless migration loop tick")
    parser.add_argument("--state", default="migration/runtime/loop_state.json", help="State JSON path")
    parser.add_argument("--log", default="migration/runtime/loop_log.jsonl", help="Log JSONL path")
    parser.add_argument("--run-id", required=True, help="Run identifier")
    parser.add_argument("--phase", required=True, choices=PHASES, help="Phase to execute")
    parser.add_argument("--status", default="OK", help="Tick status")
    parser.add_argument("--artifact", action="append", default=[], help="Artifact path (repeatable)")
    args = parser.parse_args()

    state_path = Path(args.state)
    log_path = Path(args.log)
    state_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    validate_phase(args.phase)
    state = load_json(state_path)

    tick = {
        "ts": now_utc(),
        "run_id": args.run_id,
        "phase": args.phase,
        "status": args.status,
        "artifacts": sorted(set(args.artifact)),
        "next_phase": NEXT_PHASE[args.phase],
    }

    append_jsonl(log_path, tick)

    state.update(
        {
            "run_id": args.run_id,
            "current_phase": args.phase,
            "last_status": args.status,
            "next_phase": NEXT_PHASE[args.phase],
            "updated_at": tick["ts"],
            "last_artifacts": tick["artifacts"],
        }
    )
    save_json(state_path, state)

    # Machine-readable minimal response for ChatGPT orchestration.
    print(
        json.dumps(
            {
                "phase": args.phase,
                "status": args.status,
                "next_phase": NEXT_PHASE[args.phase],
                "artifacts": tick["artifacts"],
                "state": str(state_path),
                "log": str(log_path),
            },
            sort_keys=True,
        )
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
