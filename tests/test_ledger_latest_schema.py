import copy
import json
from pathlib import Path

import jsonschema
import pytest

ROOT = Path(__file__).resolve().parents[1]
SSOT = ROOT / "control" / "ssot"


def load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def test_ledger_entry_example_passes():
    schema = load(SSOT / "schemas" / "ledger_entry.schema.json")
    example = load(SSOT / "examples" / "ledger_entry.example.json")
    jsonschema.Draft7Validator(schema).validate(example)


def test_latest_state_example_passes():
    schema = load(SSOT / "schemas" / "latest_state.schema.json")
    example = load(SSOT / "examples" / "latest_state.example.json")
    jsonschema.Draft7Validator(schema).validate(example)


def test_latest_state_missing_run_id_fails():
    schema = load(SSOT / "schemas" / "latest_state.schema.json")
    candidate = copy.deepcopy(load(SSOT / "examples" / "latest_state.example.json"))
    del candidate["run_id"]

    with pytest.raises(jsonschema.ValidationError):
        jsonschema.Draft7Validator(schema).validate(candidate)
