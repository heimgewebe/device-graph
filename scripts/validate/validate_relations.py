#!/usr/bin/env python3
import sys
import yaml
import json
import glob
from jsonschema import validate, ValidationError

schema_path = 'schemas/relation.schema.json'
with open(schema_path, 'r') as f:
    schema = json.load(f)

errors = 0
for file_path in sorted(glob.glob('data/relations/*.yaml')):
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)
        if data is None:
            print(f"✗ {file_path}: empty YAML document")
            errors += 1
            continue
        try:
            validate(instance=data, schema=schema)
            print(f"✓ {file_path}")
        except ValidationError as e:
            print(f"✗ {file_path}: {e.message}")
            errors += 1

if errors > 0:
    sys.exit(1)
else:
    print("All relations are valid.")
