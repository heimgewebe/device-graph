#!/usr/bin/env python3
import sys
import yaml
import glob

errors = 0

# 1. Load roles and map them to layers
layer_to_roles = {'truth': set(), 'service': set(), 'interaction': set(), 'access': set()}
for file_path in glob.glob('data/roles/*.yaml'):
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)
        if data and data.get('layer') in layer_to_roles:
            layer_to_roles[data.get('layer')].add(data.get('id'))

# 2. Analyze assignments specifically in target.yaml
target_devices_by_layer = {'truth': set(), 'service': set(), 'interaction': set(), 'access': set()}
assigned_roles_in_target = set()

try:
    with open('data/assignments/target.yaml', 'r') as f:
        target_data = yaml.safe_load(f)
        if target_data and 'assignments' in target_data:
            for assignment in target_data['assignments']:
                role = assignment.get('role')
                device = assignment.get('device')
                assigned_roles_in_target.add(role)

                for layer, roles in layer_to_roles.items():
                    if role in roles:
                        target_devices_by_layer[layer].add(device)
except FileNotFoundError:
    print("✗ target.yaml missing, unable to validate target architecture completeness.")
    errors += 1

# Rule A: Exclusivity - Truth layer must have exactly one device in target
truth_devices = target_devices_by_layer['truth']
if len(truth_devices) != 1:
    print(f"✗ Architecture violation: Truth layer must be exclusive to exactly one device in target.yaml. Found: {len(truth_devices)} ({truth_devices})")
    errors += 1

# Rule B: Completeness - All four layers must be represented in target.yaml
for layer in ['truth', 'service', 'interaction', 'access']:
    if not target_devices_by_layer[layer]:
        print(f"✗ Architecture violation: No device assigned to '{layer}' layer in target.yaml.")
        errors += 1

# 3. Analyze Relations
access_devices = target_devices_by_layer['access']
for file_path in glob.glob('data/relations/*.yaml'):
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)
        if data and 'relations' in data:
            for relation in data['relations']:
                source = relation.get('source')
                target = relation.get('target')
                rel_type = relation.get('type')

                # Rule C: Trust targets must be Truth devices
                if rel_type == 'trusts':
                    if target not in truth_devices:
                        print(f"✗ Architecture violation in {file_path}: 'trusts' target '{target}' is not a 'truth' layer device.")
                        errors += 1
                    # Rule D: Truth devices cannot trust themselves
                    if source in truth_devices and target == source:
                        print(f"✗ Architecture violation in {file_path}: 'truth' layer device '{source}' cannot trust itself.")
                        errors += 1

                # Rule E: Access layer devices must depend on the overlay network
                # We will check this globally below by collecting all dependencies first.

# Check Rule E (Consistency of Access Layer)
# Collect all network dependencies for devices
device_network_deps = {dev: set() for dev in access_devices}
for file_path in glob.glob('data/relations/*.yaml'):
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)
        if data and 'relations' in data:
            for relation in data['relations']:
                source = relation.get('source')
                target = relation.get('target')
                if relation.get('type') == 'depends_on' and source in access_devices:
                    device_network_deps[source].add(target)

for dev in access_devices:
    if 'overlay' not in device_network_deps.get(dev, set()):
         print(f"✗ Architecture violation: Access layer device '{dev}' lacks a 'depends_on' relation to the 'overlay' network.")
         errors += 1

if errors > 0:
    sys.exit(1)
else:
    print("All architectural rules passed successfully.")
