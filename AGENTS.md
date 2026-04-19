# Agent Guidelines

This repository models devices, networks, roles, relationships, trust zones, and migration states.

It is a **model-repo**, not an infrastructure repo.

Your responsibility is to **maintain correctness, consistency, and explicitness of the model**.

---

## 1. Read Order (Mandatory)

Before making any changes, read:

1. `README.md`
2. `repo.meta.yaml`
3. `docs/index.md`
4. `docs/reference/` (when populated, use as semantic reference)
5. relevant files in `data/` and `schemas/`

---

## 2. Core Principles

### 2.1 Explicit over implicit
All relevant information must be explicitly modeled.

- No hidden assumptions
- No inferred meaning without marking it
- No silent defaults

---

### 2.2 Separation of Concerns

| Concept | Location |
|--------|--------|
| Devices | `data/devices/` |
| Networks | `data/networks/` |
| Roles | `data/roles/` |
| Role assignments | `data/assignments/` |
| Relationships | `data/relations/` |

Strict rules:

- Role ↔ Device mapping ONLY in `data/assignments/`
- NEVER represent roles via relations (`HAS_ROLE` is forbidden)
- `data/relations/` is only for graph edges

---

### 2.3 Epistemic Discipline

All future or uncertain states must be explicitly marked.

Use:

- `status` → real-world existence
- `confidence` → assignment certainty
- `visibility` → observability
- optional future: `source_kind`, `evidence_level`

Never present speculative architecture as fact.

---

### 2.4 Heterogeneity is mandatory

Devices must reflect real-world diversity.

At minimum:

- `category`
- `visibility`

Recommended:

- `management_model`
- `trust_zone`

Do not assume:
- IP connectivity
- direct access
- uniform device capabilities

---

### 2.5 Graph Integrity

All graph edges must be valid and meaningful.

Rules:

- All `source` and `target` IDs must exist
- Relations must follow the active schema and the documented semantics in `docs/reference/relation-types.md` where defined
- Avoid redundant or duplicate edges
- Direction matters

---

## 3. Validation (Non-Negotiable)

Every change to `data/` or `schemas/` requires:

```bash
make validate
```

Validation includes:

* schema compliance
* relation integrity
* cross-entity consistency

No validation → no valid change.

---

## 4. Generated Content

* `docs/_generated/` is **read-only**
* Never manually edit generated files
* If inconsistent → fix source, not output

---

## 5. Blueprints vs Plans

| Type       | Location           | Purpose                 |
| ---------- | ------------------ | ----------------------- |
| Blueprints | `docs/blueprints/` | conceptual architecture |
| Plans      | `docs/plans/`      | execution and steps     |

Rules:

* Blueprints may be incomplete, speculative, or exploratory
* Plans must be actionable and grounded
* Do not mix both

---

## 6. What Good Contributions Look Like

A good change:

* improves clarity of the model
* reduces ambiguity
* respects schema constraints
* keeps epistemic states explicit
* maintains graph consistency

A bad change:

* introduces implicit assumptions
* mixes concepts (roles vs relations)
* hides uncertainty
* breaks validation
* duplicates information

---

## 7. If Unsure

Prefer:

* explicit fields over clever shortcuts
* simple structure over implicit logic
* marking uncertainty over guessing

The model should be **inspectable, explainable, and machine-readable**.

---

## 8. Mental Model

This repository is not a configuration.

It is a **map of reality and intention**.

Reality is messy.
Your job is not to simplify it —
your job is to **represent it faithfully**.
