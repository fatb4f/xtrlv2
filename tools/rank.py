from __future__ import annotations

from typing import Any, Callable


def build_rank_key(rank_policy: dict) -> Callable[[dict], tuple]:
    """Return a key function producing a tuple per RankPolicy.tuple_order.

    Candidate format is the CandidateSet.candidates[i] object.
    """

    orders = rank_policy.get("tuple_order", [])

    def get_field(cand: dict, field: str):
        if field == "created_at":
            return cand.get("created_at", "")
        metrics = cand.get("metrics", {})
        return metrics.get(field, 0)

    def key(cand: dict) -> tuple:
        out = []
        for spec in orders:
            field = spec["field"]
            direction = spec["direction"]
            v = get_field(cand, field)
            # Convert desc into a sortable inverse.
            if direction == "desc":
                if isinstance(v, (int, float)):
                    out.append(-v)
                else:
                    # For strings (created_at), reverse lexicographic by prefix.
                    out.append("\uffff" + str(v))
            else:
                out.append(v)
        return tuple(out)

    return key


def passes_hard_filters(rank_policy: dict, cand: dict) -> bool:
    hf = rank_policy.get("hard_filters") or {}
    max_diff = hf.get("max_diff_lines_total")
    if max_diff is not None:
        if cand.get("metrics", {}).get("diff_lines_total", 0) > max_diff:
            return False

    forbidden = set(hf.get("forbidden_paths") or [])
    # If evidence is later expanded to include touched paths here, enforce it.
    # For now, treat this as a placeholder hook.
    _ = forbidden
    return True
