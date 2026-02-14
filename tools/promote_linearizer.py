"""Promotion linearizer (single-writer).

Consumes CandidateSet, filters+ranks candidates deterministically via RankPolicy, then
selects a candidate for replay/promotion.

This skeleton stages the SSOT + selection logic. The authoritative replay (clean checkout,
apply patch, run full checks, commit/push) is intentionally left as a TODO because it
depends on your chosen git plant (patch-based promotion vs CI-only).\n
Invariants:
- single writer to promotion state (promote.lock)
- workers never promote
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Dict, List

from _util import (
    AtomicLock,
    ensure_state_layout,
    load_json,
    now_iso,
    validate_artifact,
    write_json,
    state_root,
)
from rank import build_rank_key, passes_hard_filters


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--queue", default=str(state_root() / "queue" / "work_queue.json"))
    ap.add_argument(
        "--candidate-set", default=str(state_root() / "queue" / "candidate_set.json")
    )
    ap.add_argument(
        "--rank-policy", default=str(state_root() / "queue" / "rank_policy.json")
    )
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    ensure_state_layout()

    queue_path = Path(args.queue)
    cand_path = Path(args.candidate_set)
    rp_path = Path(args.rank_policy)

    if not queue_path.exists() or not cand_path.exists() or not rp_path.exists():
        print(
            "Missing queue/candidate-set/rank-policy under state/queue", file=sys.stderr
        )
        return 2

    work_queue = load_json(queue_path)
    validate_artifact("work_queue", work_queue)

    cand_set = load_json(cand_path)
    validate_artifact("candidate_set", cand_set)

    rank_policy = load_json(rp_path)
    validate_artifact("rank_policy", rank_policy)

    if cand_set["base_ref"] != work_queue["base_ref"]:
        print("candidate_set.base_ref != work_queue.base_ref", file=sys.stderr)
        return 3

    candidates: List[Dict[str, Any]] = list(cand_set.get("candidates", []))
    candidates = [c for c in candidates if passes_hard_filters(rank_policy, c)]
    if not candidates:
        print("No candidates after hard filters", file=sys.stderr)
        return 0

    key_fn = build_rank_key(rank_policy)
    candidates.sort(key=key_fn)
    chosen = candidates[0]

    promote_lock = state_root() / "locks" / "promote.lock"
    with AtomicLock(promote_lock):
        out_dir = state_root() / "promote"
        out_dir.mkdir(parents=True, exist_ok=True)

        selection = {
            "artifact_kind": "promotion_selection",
            "selected_at": now_iso(),
            "dry_run": bool(args.dry_run),
            "queue_id": work_queue["queue_id"],
            "base_ref": work_queue["base_ref"],
            "candidate": {
                "candidate_id": chosen["candidate_id"],
                "work_item_id": chosen["work_item_id"],
                "patch_proposal_path": chosen["patch_proposal_path"],
                "evidence_path": chosen["evidence_path"],
                "gate_worker_path": chosen["gate_worker_path"],
                "metrics": chosen.get("metrics", {}),
            },
            "todo": [
                "Replay candidate patch on clean base_ref",
                "Run authoritative checks",
                "Emit authoritative gate_decision + next_iter_plan",
                "Promote commit/patch according to git plant",
            ],
        }

        write_json(out_dir / "selection.json", selection)

    print(f"Selected candidate: {chosen['candidate_id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
