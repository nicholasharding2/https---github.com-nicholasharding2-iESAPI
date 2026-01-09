import json
from pathlib import Path
from jsonschema import Draft202012Validator, ValidationError

SCHEMA_PATH = Path(__file__).parent / "schemas" / "automation_commands.schema.json"

def load_schema():
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)