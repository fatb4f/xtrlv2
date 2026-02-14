#!/usr/bin/env python
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from typing import Callable

TOOLS_DIR = Path(__file__).resolve().parents[1]
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from _util import validate_artifact  # noqa: E402
from _util import repo_root, state_root, write_json  # noqa: E402

REQUIRED_DIRS = ["queue", "out", "locks", "promote", "worktrees", "ledger"]
DIRECTORY_MAPPINGS = [
    ("out", "out"),
    ("worktrees", "worktrees"),
    ("queue", "queue"),
    ("promote", "promote"),
    ("locks", "locks"),
    ("ledger", "ledger"),
]
FILE_MAPPINGS = [
    {
        "target": "ledger/latest.json",
        "candidates": ["latest.json", "state/latest.json", "ledger/latest.json"],
    },
    {
        "target": "ledger/ledger.jsonl",
        "candidates": ["ledger/ledger.jsonl", "state/ledger.jsonl"],
    },
]
SUMMARY_KEYS = [
    "planned",
    "created",
    "copied",
    "skipped",
    "missing_source",
    "conflict",
    "error",
]


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def rel_to_root(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 64), b""):
            h.update(chunk)
    return h.hexdigest()


def make_summary() -> dict[str, int]:
    return {key: 0 for key in SUMMARY_KEYS}


def record_op(
    operations: list[dict[str, Any]],
    summary: dict[str, int],
    *,
    action: str,
    status: str,
    path: str,
    source: str | None = None,
    target: str | None = None,
    note: str | None = None,
) -> None:
    op: dict[str, Any] = {"action": action, "status": status, "path": path}
    if source is not None:
        op["source"] = source
    if target is not None:
        op["target"] = target
    if note is not None:
        op["note"] = note
    operations.append(op)
    summary[status] += 1


def ensure_target_dir(
    target_root: Path,
    rel_path: str,
    dry_run: bool,
    operations: list[dict[str, Any]],
    summary: dict[str, int],
) -> None:
    target = target_root / rel_path
    if target.exists():
        record_op(
            operations,
            summary,
            action="ensure_dir",
            status="skipped",
            path=rel_path,
            target=rel_path,
        )
        return
    if dry_run:
        record_op(
            operations,
            summary,
            action="ensure_dir",
            status="planned",
            path=rel_path,
            target=rel_path,
        )
        return
    target.mkdir(parents=True, exist_ok=True)
    record_op(
        operations,
        summary,
        action="ensure_dir",
        status="created",
        path=rel_path,
        target=rel_path,
    )


def migrate_file(
    source_root: Path,
    target_root: Path,
    source_file: Path,
    target_file: Path,
    dry_run: bool,
    operations: list[dict[str, Any]],
    summary: dict[str, int],
    content_transform: Callable[[Path, bytes], bytes] | None = None,
) -> None:
    source_rel = rel_to_root(source_file, source_root)
    target_rel = rel_to_root(target_file, target_root)
    transform = content_transform or (lambda _source, data: data)

    if not source_file.exists():
        record_op(
            operations,
            summary,
            action="migrate_file",
            status="missing_source",
            path=target_rel,
            source=source_rel,
            target=target_rel,
        )
        return

    source_bytes = source_file.read_bytes()
    migrated_bytes = transform(source_file, source_bytes)
    migrated_hash = hashlib.sha256(migrated_bytes).hexdigest()

    if target_file.exists():
        target_hash = sha256_file(target_file)
        if migrated_hash == target_hash:
            record_op(
                operations,
                summary,
                action="migrate_file",
                status="skipped",
                path=target_rel,
                source=source_rel,
                target=target_rel,
            )
        else:
            record_op(
                operations,
                summary,
                action="migrate_file",
                status="conflict",
                path=target_rel,
                source=source_rel,
                target=target_rel,
                note="target exists with different content",
            )
        return

    if dry_run:
        record_op(
            operations,
            summary,
            action="migrate_file",
            status="planned",
            path=target_rel,
            source=source_rel,
            target=target_rel,
        )
        return

    target_file.parent.mkdir(parents=True, exist_ok=True)
    target_file.write_bytes(migrated_bytes)
    record_op(
        operations,
        summary,
        action="migrate_file",
        status="copied",
        path=target_rel,
        source=source_rel,
        target=target_rel,
    )


def migrate_directory(
    source_root: Path,
    target_root: Path,
    source_rel: str,
    target_rel: str,
    dry_run: bool,
    operations: list[dict[str, Any]],
    summary: dict[str, int],
) -> None:
    source_dir = source_root / source_rel
    target_dir = target_root / target_rel

    if not source_dir.exists():
        record_op(
            operations,
            summary,
            action="migrate_dir",
            status="missing_source",
            path=target_rel,
            source=source_rel,
            target=target_rel,
        )
        return

    for source_file in sorted(p for p in source_dir.rglob("*") if p.is_file()):
        relative = source_file.relative_to(source_dir)
        migrate_file(
            source_root,
            target_root,
            source_file,
            target_dir / relative,
            dry_run,
            operations,
            summary,
        )


def migrate_first_available_file(
    source_root: Path,
    target_root: Path,
    candidates: list[str],
    target_rel: str,
    dry_run: bool,
    operations: list[dict[str, Any]],
    summary: dict[str, int],
    content_transform: Callable[[Path, bytes], bytes] | None = None,
) -> None:
    for candidate in candidates:
        source = source_root / candidate
        if source.exists():
            migrate_file(
                source_root,
                target_root,
                source,
                target_root / target_rel,
                dry_run,
                operations,
                summary,
                content_transform=content_transform,
            )
            return

    record_op(
        operations,
        summary,
        action="migrate_file",
        status="missing_source",
        path=target_rel,
        source=candidates[0],
        target=target_rel,
        note="no candidate source file found",
    )


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Migration Report",
        "",
        f"- run_id: `{report['run_id']}`",
        f"- generated_at: `{report['generated_at']}`",
        f"- mode: `{report['mode']}`",
        f"- source_root: `{report['source_root']}`",
        f"- target_root: `{report['target_root']}`",
        f"- idempotent: `{str(report['idempotent']).lower()}`",
        "",
        "## Summary",
        "",
        "| status | count |",
        "|---|---:|",
    ]
    for key in SUMMARY_KEYS:
        lines.append(f"| {key} | {report['summary'][key]} |")

    lines.extend(["", "## Operations"])
    if not report["operations"]:
        lines.extend(["", "- none"])
    else:
        for op in report["operations"]:
            source = f" src=`{op['source']}`" if "source" in op else ""
            target = f" dst=`{op['target']}`" if "target" in op else ""
            note = f" note={op['note']}" if "note" in op else ""
            lines.append(
                f"- `{op['status']}` `{op['action']}` `{op['path']}`{source}{target}{note}"
            )

    lines.append("")
    return "\n".join(lines)


def default_source_root() -> Path:
    codex_state = os.environ.get("CODEX_STATE")
    if codex_state:
        return Path(codex_state).expanduser() / "xtrl"
    return repo_root() / "state_legacy"


def normalize_latest_state(source: Path, raw: bytes) -> bytes:
    try:
        obj = json.loads(raw.decode("utf-8"))
    except Exception:  # noqa: BLE001
        return raw

    try:
        validate_artifact("latest_state", obj)
        return raw
    except Exception:  # noqa: BLE001
        pass

    ledger_ref_obj = (
        obj.get("ledger_ref") if isinstance(obj.get("ledger_ref"), dict) else {}
    )
    mapped = {
        "schema_version": "0.1",
        "artifact_kind": "latest_state",
        "updated_at": obj.get("updated_at") or obj.get("timestamp_utc") or now_utc(),
        "run_id": obj.get("run_id")
        or obj.get("packet_id")
        or source.stem
        or "legacy-run",
        "iteration_id": obj.get("iteration_id")
        or obj.get("packet_id")
        or "legacy-iter-0001",
        "last_decision": obj.get("last_decision") or obj.get("decision") or "SKIPPED",
        "out_dir": obj.get("out_dir") or "out/legacy",
        "base_ref": obj.get("base_ref") or "legacy/base_ref",
        "ledger_ref": {
            "path": ledger_ref_obj.get("path")
            or obj.get("ledger_path")
            or "ledger/ledger.jsonl"
        },
    }
    if obj.get("next_base_ref"):
        mapped["next_base_ref"] = obj["next_base_ref"]

    if mapped["last_decision"] not in {"ALLOW", "DENY", "STOP", "SKIPPED"}:
        mapped["last_decision"] = "SKIPPED"

    try:
        validate_artifact("latest_state", mapped)
    except Exception:  # noqa: BLE001
        return raw
    return (json.dumps(mapped, indent=2, sort_keys=True) + "\n").encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Migrate legacy state layout into standalone xtrlv2 state root."
    )
    parser.add_argument(
        "--source-root",
        default=str(default_source_root()),
        help="legacy state root (default: $CODEX_STATE/xtrl or ./state_legacy)",
    )
    parser.add_argument(
        "--target-root",
        default=str(state_root()),
        help="target xtrlv2 state root (default: resolved state_root)",
    )
    parser.add_argument(
        "--report-json",
        default=str(repo_root() / "migration" / "runtime" / "migration_report.json"),
        help="path for machine-readable report",
    )
    parser.add_argument(
        "--report-md",
        default=str(repo_root() / "migration" / "runtime" / "migration_report.md"),
        help="path for markdown report",
    )
    parser.add_argument("--run-id", default=None, help="override generated run id")
    parser.add_argument("--dry-run", action="store_true", help="plan only; no writes")
    args = parser.parse_args()

    source_root = Path(args.source_root).resolve()
    target_root = Path(args.target_root).resolve()
    report_json_path = Path(args.report_json).resolve()
    report_md_path = Path(args.report_md).resolve()

    operations: list[dict[str, Any]] = []
    summary = make_summary()
    dry_run = bool(args.dry_run)

    for rel_path in REQUIRED_DIRS:
        ensure_target_dir(target_root, rel_path, dry_run, operations, summary)

    for source_rel, target_rel in DIRECTORY_MAPPINGS:
        migrate_directory(
            source_root,
            target_root,
            source_rel,
            target_rel,
            dry_run,
            operations,
            summary,
        )

    for mapping in FILE_MAPPINGS:
        transform = (
            normalize_latest_state
            if mapping["target"] == "ledger/latest.json"
            else None
        )
        migrate_first_available_file(
            source_root,
            target_root,
            mapping["candidates"],
            mapping["target"],
            dry_run,
            operations,
            summary,
            content_transform=transform,
        )

    report = {
        "schema_version": "0.1",
        "artifact_kind": "migration_report",
        "run_id": args.run_id
        or f"migrate-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}",
        "generated_at": now_utc(),
        "mode": "dry-run" if dry_run else "apply",
        "source_root": str(source_root),
        "target_root": str(target_root),
        "layout": {
            "required_dirs": REQUIRED_DIRS,
            "directory_mappings": [
                {"source": src, "target": dst} for src, dst in DIRECTORY_MAPPINGS
            ],
            "file_mappings": FILE_MAPPINGS,
        },
        "operations": operations,
        "summary": summary,
    }
    report["idempotent"] = (
        report["summary"]["planned"] == 0
        and report["summary"]["created"] == 0
        and report["summary"]["copied"] == 0
        and report["summary"]["conflict"] == 0
        and report["summary"]["error"] == 0
    )

    validate_artifact("migration_report", report)

    write_json(report_json_path, report)
    report_md_path.parent.mkdir(parents=True, exist_ok=True)
    report_md_path.write_text(render_markdown(report), encoding="utf-8")

    print(
        json.dumps(
            {
                "run_id": report["run_id"],
                "mode": report["mode"],
                "source_root": report["source_root"],
                "target_root": report["target_root"],
                "summary": report["summary"],
                "idempotent": report["idempotent"],
                "report_json": str(report_json_path),
                "report_md": str(report_md_path),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
