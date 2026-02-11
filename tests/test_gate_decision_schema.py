import copy
import json
from pathlib import Path

import jsonschema
import pytest

ROOT = Path(__file__).resolve().parents[1]
SSOT = ROOT / "control" / "ssot"


def load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def test_gate_decision_example_passes():
    schema = load(SSOT / "schemas" / "gate_decision.schema.json")
    example = load(SSOT / "examples" / "gate_decision.example.json")
    jsonschema.Draft7Validator(schema).validate(example)


def test_gate_decision_missing_reason_codes_fails():
    schema = load(SSOT / "schemas" / "gate_decision.schema.json")
    candidate = copy.deepcopy(load(SSOT / "examples" / "gate_decision.example.json"))
    del candidate["reason_codes"]

    with pytest.raises(jsonschema.ValidationError):
        jsonschema.Draft7Validator(schema).validate(candidate)
