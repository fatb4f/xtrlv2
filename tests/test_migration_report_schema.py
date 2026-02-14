import copy
import json
from pathlib import Path

import jsonschema
import pytest

ROOT = Path(__file__).resolve().parents[1]
SSOT = ROOT / "control" / "ssot"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_migration_report_example_passes():
    schema = load(SSOT / "schemas" / "migration_report.schema.json")
    example = load(SSOT / "examples" / "migration_report.example.json")
    jsonschema.Draft7Validator(schema).validate(example)


def test_migration_report_missing_summary_fails():
    schema = load(SSOT / "schemas" / "migration_report.schema.json")
    candidate = copy.deepcopy(load(SSOT / "examples" / "migration_report.example.json"))
    del candidate["summary"]

    with pytest.raises(jsonschema.ValidationError):
        jsonschema.Draft7Validator(schema).validate(candidate)
