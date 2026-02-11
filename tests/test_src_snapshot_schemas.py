import copy
import json
from pathlib import Path

import jsonschema
import pytest

ROOT = Path(__file__).resolve().parents[1]
SSOT = ROOT / "control" / "ssot"


def load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def test_dep_graph_example_passes():
    schema = load(SSOT / "schemas" / "dep_graph.schema.json")
    example = load(SSOT / "examples" / "dep_graph.example.json")
    jsonschema.Draft7Validator(schema).validate(example)


def test_api_surface_example_passes():
    schema = load(SSOT / "schemas" / "api_surface.schema.json")
    example = load(SSOT / "examples" / "api_surface.example.json")
    jsonschema.Draft7Validator(schema).validate(example)


def test_module_manifest_example_passes():
    schema = load(SSOT / "schemas" / "module_manifest.schema.json")
    example = load(SSOT / "examples" / "module_manifest.example.json")
    jsonschema.Draft7Validator(schema).validate(example)


def test_dep_graph_unstable_ordering_fails():
    schema = load(SSOT / "schemas" / "dep_graph.schema.json")
    candidate = copy.deepcopy(load(SSOT / "examples" / "dep_graph.example.json"))
    candidate["ordering"] = "unspecified"

    with pytest.raises(jsonschema.ValidationError):
        jsonschema.Draft7Validator(schema).validate(candidate)
