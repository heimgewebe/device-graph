#!/usr/bin/env python3
import sys
import yaml
import glob

errors = 0

# Load roles to identify the truth layer role
truth_layer_roles = set()
for file_path in glob.glob('data/roles/*.yaml'):
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)
        if data and data.get('layer') == 'truth':
            truth_layer_roles.add(data.get('id'))

# Load assignments to find which devices hold the truth layer role
truth_devices = set()
for file_path in glob.glob('data/assignments/*.yaml'):
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)
        if data and 'assignments' in data:
            for assignment in data['assignments']:
                if assignment.get('role') in truth_layer_roles:
                    truth_devices.add(assignment.get('device'))

# Check that truth devices are exclusive if role demands it
# For now, just a simple rule: trusts relations MUST point to a truth device.
for file_path in glob.glob('data/relations/*.yaml'):
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)
        if data and 'relations' in data:
            for relation in data['relations']:
                if relation.get('type') == 'trusts':
                    target = relation.get('target')
                    if target not in truth_devices:
                        print(f"✗ Architecture violation in {file_path}: 'trusts' relation target '{target}' is not assigned a 'truth' layer role.")
                        errors += 1

if errors > 0:
    sys.exit(1)
else:
    print("All architectural rules passed successfully.")
