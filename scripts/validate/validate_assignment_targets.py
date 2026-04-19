#!/usr/bin/env python3
import sys
import yaml
import glob

# Sammle alle existierenden IDs
known_devices = set()
known_roles = set()

# Lade Devices
for fp in sorted(glob.glob('data/devices/**/*.yaml', recursive=True)):
    with open(fp, 'r') as f:
        data = yaml.safe_load(f)
        if data and 'id' in data:
            known_devices.add(data['id'])

# Lade Roles
for fp in sorted(glob.glob('data/roles/*.yaml')):
    with open(fp, 'r') as f:
        data = yaml.safe_load(f)
        if data and 'id' in data:
            known_roles.add(data['id'])

# Prüfe Assignments
errors = 0
for fp in sorted(glob.glob('data/assignments/*.yaml')):
    with open(fp, 'r') as f:
        data = yaml.safe_load(f)
        if data and isinstance(data.get('assignments'), list):
            for i, assign in enumerate(data['assignments']):
                role = assign.get('role')
                device = assign.get('device')
                if role not in known_roles:
                    print(f"✗ {fp} (Assignment {i}): Role ID '{role}' does not exist in data/roles/.")
                    errors += 1
                if device not in known_devices:
                    print(f"✗ {fp} (Assignment {i}): Device ID '{device}' does not exist in data/devices/.")
                    errors += 1

if errors > 0:
    sys.exit(1)
else:
    print("All assignment targets are valid (exist as nodes).")
