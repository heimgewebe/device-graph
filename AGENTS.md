# Agent Guidelines

**Reading Order:**
1. `README.md`
2. `AGENTS.md`
3. `docs/index.md`

**Canonical Paths:**
- `data/` is the sole source of truth for topology data.
- `schemas/` defines the structural bounds for `data/`.

**Generated Paths:**
- Do NOT manually edit anything in `docs/_generated/`.

**Assignment vs Relation Rule:**
- Use `data/assignments/` strictly for role-to-device mapping.
- Use `data/relations/` strictly for general graph edges. Never create `HAS_ROLE` relations here.

**Blueprint vs Plan Rule:**
- `docs/blueprints/`: Conceptual target architectures, ontology definitions.
- `docs/plans/`: Operative roadmaps, execution tasks.

**Required Validation:**
- Any modification to `data/` or `schemas/` REQUIRES running `make validate` before committing.
