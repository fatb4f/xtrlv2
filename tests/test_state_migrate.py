import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SSOT = ROOT / "control" / "ssot"
SCRIPT = ROOT / "tools" / "migration" / "state_migrate.py"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def run_state_migrate(*args: str) -> dict:
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout.strip())


def make_legacy_source(source_root: Path) -> None:
    (source_root / "out" / "run-001").mkdir(parents=True, exist_ok=True)
    (source_root / "out" / "run-001" / "result.txt").write_text(
        "ok\n", encoding="utf-8"
    )
    (source_root / "worktrees" / "wt-a").mkdir(parents=True, exist_ok=True)
    (source_root / "worktrees" / "wt-a" / "meta.txt").write_text(
        "worktree\n", encoding="utf-8"
    )
    (source_root / "state").mkdir(parents=True, exist_ok=True)
    latest = load(SSOT / "examples" / "latest_state.example.json")
    (source_root / "state" / "latest.json").write_text(
        json.dumps(latest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def test_state_migrate_dry_run_then_apply_is_idempotent(tmp_path: Path):
    source_root = tmp_path / "legacy_state"
    target_root = tmp_path / "xtrlv2_state"
    make_legacy_source(source_root)

    dry_report_json = tmp_path / "report_dry.json"
    dry_report_md = tmp_path / "report_dry.md"
    dry = run_state_migrate(
        "--source-root",
        str(source_root),
        "--target-root",
        str(target_root),
        "--report-json",
        str(dry_report_json),
        "--report-md",
        str(dry_report_md),
        "--dry-run",
    )
    dry_report = load(Path(dry["report_json"]))

    assert dry_report["mode"] == "dry-run"
    assert dry_report["summary"]["planned"] > 0
    assert not (target_root / "queue").exists()

    apply_report_json = tmp_path / "report_apply_1.json"
    apply_report_md = tmp_path / "report_apply_1.md"
    apply_1 = run_state_migrate(
        "--source-root",
        str(source_root),
        "--target-root",
        str(target_root),
        "--report-json",
        str(apply_report_json),
        "--report-md",
        str(apply_report_md),
    )
    report_1 = load(Path(apply_1["report_json"]))

    assert report_1["mode"] == "apply"
    assert report_1["summary"]["copied"] > 0
    assert (target_root / "out" / "run-001" / "result.txt").exists()
    assert (target_root / "worktrees" / "wt-a" / "meta.txt").exists()
    assert (target_root / "ledger" / "latest.json").exists()
    assert report_1["idempotent"] is False

    apply_report_json_2 = tmp_path / "report_apply_2.json"
    apply_report_md_2 = tmp_path / "report_apply_2.md"
    apply_2 = run_state_migrate(
        "--source-root",
        str(source_root),
        "--target-root",
        str(target_root),
        "--report-json",
        str(apply_report_json_2),
        "--report-md",
        str(apply_report_md_2),
    )
    report_2 = load(Path(apply_2["report_json"]))

    assert report_2["summary"]["created"] == 0
    assert report_2["summary"]["copied"] == 0
    assert report_2["summary"]["conflict"] == 0
    assert report_2["summary"]["error"] == 0
    assert report_2["idempotent"] is True
