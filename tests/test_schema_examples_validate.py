import json
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
SSOT = ROOT / "control" / "ssot"


def load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def test_examples_validate_against_registry():
    registry = load(SSOT / "registry.json")
    artifacts = registry["artifacts"]

    for kind, meta in artifacts.items():
        schema_path = ROOT / meta["schema"]
        example_path = SSOT / "examples" / f"{kind}.example.json"

        schema = load(schema_path)
        example = load(example_path)

        # Schemas in this repo target Draft-07 for maximum tool compatibility.
        jsonschema.Draft7Validator(schema).validate(example)
