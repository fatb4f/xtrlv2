"""Concurrent micro-loop worker.

This script claims a work item from a WorkQueue, runs codex-cli to produce a PatchProposal,
creates an EvidenceCapsule + worker-local gate decision, and appends the candidate to the
CandidateSet.

Design goals:
- deterministic file layout under state/
- patch-only primary output (unified diff)
- controller/linearizer remains the only promotion authority

NOTE: This repo stages the control plane. You must have `codex` installed for execution.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict

from _util import (
    AtomicLock,
    ensure_state_layout,
    load_json,
    now_iso,
    read_registry_schema,
    validate_artifact,
    write_json,
    state_root,
)


def run_codex(
    prompt: str,
    output_schema_path: Path,
    out_json: Path,
    out_events_jsonl: Path,
    cwd: Path,
) -> int:
    """Run codex non-interactive.

    Contract:
    - JSONL event stream -> out_events_jsonl
    - final structured output -> out_json (validated by output_schema_path)
    """
    cmd = [
        "codex",
        "exec",
        "--json",
        "--output-schema",
        str(output_schema_path),
        "-o",
        str(out_json),
        prompt,
    ]
    with out_events_jsonl.open("w", encoding="utf-8") as f:
        proc = subprocess.run(cmd, cwd=str(cwd), stdout=f, stderr=subprocess.STDOUT)
    return int(proc.returncode)


def make_evidence_stub(
    candidate_id: str, base_ref: str, work_item_id: str, codex_rc: int, out_dir: Path
) -> Dict[str, Any]:
    """Minimal evidence capsule; controller/linearizer can extend.

    Current schema is permissive; this is a placeholder that keeps the artifact graph intact.
    """
    return {
        "artifact_kind": "evidence_capsule",
        "run_id": candidate_id,
        "base_ref": base_ref,
        "checks": {
            "codex": {
                "ok": codex_rc == 0,
                "rc": codex_rc,
                "work_item_id": work_item_id,
            },
        },
        "diff": {"files": [], "lines_added": 0, "lines_removed": 0},
        "notes": [f"events_jsonl={str(out_dir / 'codex_events.jsonl')}"],
    }


def worker_gate_stub(candidate_id: str, base_ref: str, codex_rc: int) -> Dict[str, Any]:
    """Worker-local gate: admissibility filter (NOT promotion)."""
    if codex_rc != 0:
        decision = "DENY"
        reason_codes = ["CHECKS_FAILED"]
    else:
        decision = "ALLOW"
        reason_codes = []

    return {
        "artifact_kind": "gate_decision",
        "run_id": candidate_id,
        "decision": decision,
        "reason_codes": reason_codes,
        "base_ref": base_ref,
        "created_at": now_iso(),
        "notes": ["worker-local admissibility only"],
    }


def append_candidate(candidate_set_path: Path, entry: Dict[str, Any]) -> None:
    if candidate_set_path.exists():
        data = load_json(candidate_set_path)
    else:
        data = {
            "artifact_kind": "candidate_set",
            "queue_id": entry["queue_id"],
            "base_ref": entry["base_ref"],
            "candidates": [],
        }
    data["candidates"].append(entry["candidate"])
    write_json(candidate_set_path, data)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--queue", default=str(state_root() / "queue" / "work_queue.json")
    )
    parser.add_argument(
        "--rank-policy", default=str(state_root() / "queue" / "rank_policy.json")
    )
    parser.add_argument(
        "--candidate-set", default=str(state_root() / "queue" / "candidate_set.json")
    )
    parser.add_argument("--worker-id", default="worker-001")
    parser.add_argument(
        "--prompt",
        default="Implement the smallest change for the given objective slice. Output a unified diff.",
    )
    args = parser.parse_args()

    ensure_state_layout()

    queue_path = Path(args.queue)
    queue = load_json(queue_path)
    validate_artifact("work_queue", queue)

    # naive: take first work item (claim lock prevents duplication)
    wi = queue["work_items"][0]
    work_item_id = wi["work_item_id"]

    lock_path = state_root() / "locks" / f"claim_{work_item_id}.lock"
    try:
        with AtomicLock(lock_path):
            candidate_id = f"cand-{args.worker_id}-{int(Path('/proc/uptime').read_text().split()[0].split('.')[0])}"
            out_dir = state_root() / "out" / candidate_id
            out_dir.mkdir(parents=True, exist_ok=True)

            # Write run manifest (optional for now)
            run_manifest = {
                "artifact_kind": "run_manifest",
                "run_id": candidate_id,
                "repo_root": str(Path.cwd()),
                "base_ref": queue["base_ref"],
                "last_good_ref": queue["base_ref"],
                "desired_state_id": queue["desired_state_id"],
                "budgets": wi.get("budgets", {}),
                "policy": wi.get(
                    "policy",
                    {
                        "allowed_paths": [],
                        "forbidden_paths": [],
                        "allowed_commands": [],
                    },
                ),
                "output_root": str(out_dir),
            }
            write_json(out_dir / "run_manifest.json", run_manifest)

            # Run codex
            patch_schema = Path(read_registry_schema("patch_proposal"))
            patch_out = out_dir / "patch_proposal.json"
            events_out = out_dir / "codex_events.jsonl"
            rc = run_codex(
                prompt=f"Objective: {wi['objective_slice']}\n\n{args.prompt}",
                output_schema_path=patch_schema,
                out_json=patch_out,
                out_events_jsonl=events_out,
                cwd=Path.cwd(),
            )

            if patch_out.exists():
                validate_artifact("patch_proposal", load_json(patch_out))

            evidence = make_evidence_stub(
                candidate_id, queue["base_ref"], work_item_id, rc, out_dir
            )
            write_json(out_dir / "evidence.json", evidence)
            validate_artifact("evidence_capsule", evidence)

            gate = worker_gate_stub(candidate_id, queue["base_ref"], rc)
            write_json(out_dir / "gate_worker.json", gate)
            validate_artifact("gate_decision", gate)

            # CandidateSet entry
            entry = {
                "queue_id": queue["queue_id"],
                "base_ref": queue["base_ref"],
                "candidate": {
                    "candidate_id": candidate_id,
                    "work_item_id": work_item_id,
                    "patch_proposal_path": str(patch_out),
                    "evidence_path": str(out_dir / "evidence.json"),
                    "gate_worker_path": str(out_dir / "gate_worker.json"),
                    "created_at": now_iso(),
                    "metrics": {
                        "diff_lines_total": 0,
                        "files_touched": 0,
                        "checks_passed": 1 if rc == 0 else 0,
                        "checks_failed": 0 if rc == 0 else 1,
                        "policy_warnings": 0,
                    },
                },
            }

            append_candidate(Path(args.candidate_set), entry)
            return 0

    except FileExistsError:
        print(f"work item already claimed: {work_item_id}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
