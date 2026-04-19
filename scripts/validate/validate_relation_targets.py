#!/usr/bin/env python3
import sys
import yaml
import glob

# Sammle alle existierenden IDs
known_ids = set()

# Lade Devices
for fp in glob.glob('data/devices/**/*.yaml', recursive=True):
    with open(fp, 'r') as f:
        data = yaml.safe_load(f)
        if 'id' in data:
            known_ids.add(data['id'])

# Lade Networks
for fp in glob.glob('data/networks/*.yaml'):
    with open(fp, 'r') as f:
        data = yaml.safe_load(f)
        if 'id' in data:
            known_ids.add(data['id'])

# Lade Roles
for fp in glob.glob('data/roles/*.yaml'):
    with open(fp, 'r') as f:
        data = yaml.safe_load(f)
        if 'id' in data:
            known_ids.add(data['id'])

# Prüfe Relations
errors = 0
for fp in glob.glob('data/relations/*.yaml'):
    with open(fp, 'r') as f:
        data = yaml.safe_load(f)
        if 'relations' in data:
            for i, rel in enumerate(data['relations']):
                src = rel.get('source')
                tgt = rel.get('target')
                if src not in known_ids:
                    print(f"✗ {fp} (Relation {i}): Source ID '{src}' does not exist.")
                    errors += 1
                if tgt not in known_ids:
                    print(f"✗ {fp} (Relation {i}): Target ID '{tgt}' does not exist.")
                    errors += 1

if errors > 0:
    sys.exit(1)
else:
    print("All relation targets are valid (exist as nodes).")
