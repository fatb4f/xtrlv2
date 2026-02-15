import copy
import json
from pathlib import Path

import jsonschema
import pytest

ROOT = Path(__file__).resolve().parents[1]
SSOT = ROOT / "control" / "ssot"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_guardrails_bundle_example_passes():
    schema = load(SSOT / "schemas" / "guardrails_bundle.schema.json")
    example = load(SSOT / "examples" / "guardrails_bundle.example.json")
    jsonschema.Draft7Validator(schema).validate(example)


def test_guardrails_bundle_missing_unknowns_policy_fails():
    schema = load(SSOT / "schemas" / "guardrails_bundle.schema.json")
    candidate = copy.deepcopy(
        load(SSOT / "examples" / "guardrails_bundle.example.json")
    )
    del candidate["meta"]["requirements"]["unknowns_policy"]

    with pytest.raises(jsonschema.ValidationError):
        jsonschema.Draft7Validator(schema).validate(candidate)
