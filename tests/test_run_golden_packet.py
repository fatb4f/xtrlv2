import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "migration" / "run_golden_packet.py"
CONTRACT = ROOT / "control" / "ssot" / "examples" / "packet_pre_contract.example.json"


def test_run_golden_packet_materializes_required_files(tmp_path: Path):
    out_root = tmp_path / "golden"
    run_id = "golden-test-0001"
    proc = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--contract",
            str(CONTRACT),
            "--out-root",
            str(out_root),
            "--run-id",
            run_id,
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout.strip())

    packet_dir = Path(payload["output_dir"])
    assert packet_dir.exists()
    for rel_path in payload["required_files"]:
        assert (packet_dir / rel_path).exists()
    assert (packet_dir / "golden_report.json").exists()
