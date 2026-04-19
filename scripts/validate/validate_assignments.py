#!/usr/bin/env python3
import sys
import yaml
import json
import glob
from jsonschema import validate, ValidationError

schema_path = 'schemas/assignment.schema.json'
with open(schema_path, 'r') as f:
    schema = json.load(f)

errors = 0
for file_path in sorted(glob.glob('data/assignments/*.yaml')):
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)
        if data:
            try:
                validate(instance=data, schema=schema)
                print(f"✓ {file_path}")
            except ValidationError as e:
                print(f"✗ {file_path}: {e.message}")
                errors += 1

if errors > 0:
    sys.exit(1)
else:
    print("All assignments are valid.")
