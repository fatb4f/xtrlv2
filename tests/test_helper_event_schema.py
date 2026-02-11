import copy
import json
from pathlib import Path

import jsonschema
import pytest

ROOT = Path(__file__).resolve().parents[1]
SSOT = ROOT / "control" / "ssot"


def load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def test_helper_event_example_passes():
    schema = load(SSOT / "schemas" / "helper_event.schema.json")
    example = load(SSOT / "examples" / "helper_event.example.json")
    jsonschema.Draft7Validator(schema).validate(example)


def test_helper_event_missing_gate_ref_fails():
    schema = load(SSOT / "schemas" / "helper_event.schema.json")
    candidate = copy.deepcopy(load(SSOT / "examples" / "helper_event.example.json"))
    del candidate["gate_decision_ref"]

    with pytest.raises(jsonschema.ValidationError):
        jsonschema.Draft7Validator(schema).validate(candidate)
