import copy
import json
from pathlib import Path

import jsonschema
import pytest

ROOT = Path(__file__).resolve().parents[1]
SSOT = ROOT / "control" / "ssot"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_packet_pre_contract_example_passes():
    schema = load(SSOT / "schemas" / "packet_pre_contract.schema.json")
    example = load(SSOT / "examples" / "packet_pre_contract.example.json")
    jsonschema.Draft7Validator(schema).validate(example)


def test_packet_pre_contract_missing_required_files_fails():
    schema = load(SSOT / "schemas" / "packet_pre_contract.schema.json")
    candidate = copy.deepcopy(
        load(SSOT / "examples" / "packet_pre_contract.example.json")
    )
    del candidate["evidence"]["required_files"]

    with pytest.raises(jsonschema.ValidationError):
        jsonschema.Draft7Validator(schema).validate(candidate)
