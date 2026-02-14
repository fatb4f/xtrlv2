import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "tools" / "migration" / "xtrlv2.py"


def run_ok(*args: str):
    proc = subprocess.run(
        [sys.executable, str(CLI), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr


def test_xtrlv2_cli_help_commands():
    run_ok("--help")
    run_ok("state-migrate", "--help")
    run_ok("state-doctor", "--help")
    run_ok("run-golden-packet", "--help")
    run_ok("final-validate", "--help")


def test_xtrlv2_cli_passthrough_arguments(tmp_path: Path):
    state_root = tmp_path / "state"
    proc = subprocess.run(
        [
            sys.executable,
            str(CLI),
            "state-doctor",
            "--state-root",
            str(state_root),
            "--create-missing",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
