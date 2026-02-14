import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SSOT = ROOT / "control" / "ssot"
SCRIPT = ROOT / "tools" / "migration" / "state_doctor.py"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def run_state_doctor(*args: str) -> tuple[int, dict]:
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    payload = json.loads(proc.stdout.strip())
    return proc.returncode, payload


def test_state_doctor_reports_missing_then_create_then_validate(tmp_path: Path):
    state_root = tmp_path / "state_root"

    rc_missing, missing_payload = run_state_doctor("--state-root", str(state_root))
    assert rc_missing == 1
    assert "queue" in missing_payload["missing_dirs"]

    rc_create, create_payload = run_state_doctor(
        "--state-root", str(state_root), "--create-missing"
    )
    assert rc_create == 0
    assert create_payload["missing_dirs"] == []

    invalid_work_queue = state_root / "queue" / "work_queue.json"
    invalid_work_queue.write_text('{"artifact_kind": "work_queue"}\n', encoding="utf-8")
    rc_invalid, invalid_payload = run_state_doctor("--state-root", str(state_root))
    assert rc_invalid == 1
    assert invalid_payload["invalid_artifacts"]

    valid_work_queue = load(SSOT / "examples" / "work_queue.example.json")
    invalid_work_queue.write_text(
        json.dumps(valid_work_queue, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    rc_valid, valid_payload = run_state_doctor("--state-root", str(state_root))
    assert rc_valid == 0
    assert valid_payload["invalid_artifacts"] == []
