.PHONY: validate validate-devices validate-networks validate-roles validate-assignments validate-relations validate-relation-targets

validate: validate-devices validate-networks validate-roles validate-assignments validate-relations validate-relation-targets
	@echo "All validations passed successfully!"

validate-devices:
	@./scripts/validate/validate_devices.py

validate-networks:
	@./scripts/validate/validate_networks.py

validate-roles:
	@./scripts/validate/validate_roles.py

validate-assignments:
	@./scripts/validate/validate_assignments.py

validate-relations:
	@./scripts/validate/validate_relations.py

validate-relation-targets:
	@./scripts/validate/validate_relation_targets.py
