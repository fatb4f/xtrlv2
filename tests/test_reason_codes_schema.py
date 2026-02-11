import copy
import json
from pathlib import Path

import jsonschema
import pytest

ROOT = Path(__file__).resolve().parents[1]
SSOT = ROOT / "control" / "ssot"


def load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def test_reason_codes_canonical_passes():
    schema = load(SSOT / "schemas" / "reason_codes.schema.json")
    canonical = load(SSOT / "reason_codes.json")
    jsonschema.Draft7Validator(schema).validate(canonical)


def test_reason_codes_unknown_code_fails():
    schema = load(SSOT / "schemas" / "reason_codes.schema.json")
    candidate = load(SSOT / "reason_codes.json")
    candidate["codes"]["UNKNOWN_REASON_CODE"] = {"class": "structural"}

    with pytest.raises(jsonschema.ValidationError):
        jsonschema.Draft7Validator(schema).validate(candidate)


def test_reason_codes_malformed_record_fails():
    schema = load(SSOT / "schemas" / "reason_codes.schema.json")
    candidate = copy.deepcopy(load(SSOT / "reason_codes.json"))
    del candidate["codes"]["SCHEMA_INVALID"]["class"]

    with pytest.raises(jsonschema.ValidationError):
        jsonschema.Draft7Validator(schema).validate(candidate)
