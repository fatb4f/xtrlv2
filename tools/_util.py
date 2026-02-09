from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

import jsonschema


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def ssot_root() -> Path:
    return repo_root() / "control" / "ssot"


def state_root() -> Path:
    """Default runtime state root.

    - If CODEX_STATE is set, use $CODEX_STATE/xtrl (aligned with your canonical XDG model).
    - Otherwise, use repo-local ./state
    """
    codex_state = os.environ.get("CODEX_STATE")
    if codex_state:
        return Path(codex_state).expanduser() / "xtrl"
    return repo_root() / "state"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def validate_artifact(kind: str, obj: Any) -> None:
    registry = load_json(ssot_root() / "registry.json")
    meta = registry["artifacts"][kind]
    schema = load_json(repo_root() / meta["schema"])
    jsonschema.Draft7Validator(schema).validate(obj)


@dataclass(frozen=True)
class Lock:
    path: Path


def acquire_lock(lock_path: Path, ttl_seconds: int = 3600) -> Lock:
    """Acquire a lock via atomic create.

    Creates the lock file with O_EXCL. If it exists, checks staleness by mtime.
    """
    lock_path.parent.mkdir(parents=True, exist_ok=True)

    now = time.time()
    if lock_path.exists():
        age = now - lock_path.stat().st_mtime
        if age > ttl_seconds:
            # stale lock: best-effort break
            lock_path.unlink(missing_ok=True)

    fd = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(f"pid={os.getpid()}\n")
        f.write(f"created_at={int(now)}\n")

    return Lock(lock_path)


def release_lock(lock: Lock) -> None:
    lock.path.unlink(missing_ok=True)


def append_candidate(candidate_set_path: Path, candidate_entry: dict) -> None:
    """Append candidate entry to candidate_set.json (create if missing)."""
    if candidate_set_path.exists():
        obj = load_json(candidate_set_path)
    else:
        obj = {
            "artifact_kind": "candidate_set",
            "queue_id": candidate_entry.get("queue_id", ""),
            "base_ref": candidate_entry.get("base_ref", ""),
            "candidates": [],
        }

    obj.setdefault("candidates", []).append(candidate_entry)
    write_json(candidate_set_path, obj)


def ensure_state_layout() -> None:
    """Create expected state subdirs."""
    for sub in ["out", "queue", "locks", "promote", "worktrees"]:
        (state_root() / sub).mkdir(parents=True, exist_ok=True)


def now_iso() -> str:
    # fixed format; caller can override
    return time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime())


def read_registry_schema(kind: str) -> str:
    registry = load_json(ssot_root() / "registry.json")
    return str(repo_root() / registry["artifacts"][kind]["schema"])


class AtomicLock:
    """Context-manager wrapper around acquire_lock/release_lock."""

    def __init__(self, path: Path, ttl_seconds: int = 3600):
        self.path = path
        self.ttl_seconds = ttl_seconds
        self._lock: Optional[Lock] = None

    def __enter__(self):
        self._lock = acquire_lock(self.path, ttl_seconds=self.ttl_seconds)
        return self

    def __exit__(self, exc_type, exc, tb):
        if self._lock:
            release_lock(self._lock)
        return False
