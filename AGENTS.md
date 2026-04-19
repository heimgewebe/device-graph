# Agent Guidelines

## Current Phase: Structure Only

This repository is currently in **structure-only mode**.

Your task is to maintain and improve the **repository structure**, not to populate it with substantive content.

## Read First

1. `README.md`
2. `AGENTS.md`
3. `docs/index.md`

## Core Rule

Do **not** add substantial content to:

* `docs/blueprints/`
* `docs/plans/`
* `docs/reference/`
* `data/`

At this stage, these paths exist to define future structure only.

## Allowed Work

You may:

* create directories and placeholder files
* improve navigation structure
* improve repository metadata
* improve validation tooling
* improve schema scaffolding
* improve Makefile / CI scaffolding
* improve path discipline and guardrails

## Forbidden Work

You must not:

* define final ontology content
* define final relation semantics in detail
* define concrete migration plans
* define operational next steps in detail
* add real device inventory entries
* add real network topology content
* add generated documentation manually

## Generated Files

Anything under `docs/_generated/` is generated-only and must never be manually edited.

## Data Model Discipline

* `data/assignments/` is reserved for role assignments
* `data/relations/` is reserved for general graph edges
* no `HAS_ROLE` relation may be introduced in `data/relations/`

## Validation Discipline

Changes to `schemas/`, `scripts/validate/`, `Makefile`, or repository structure must preserve `make validate`.

## If Unsure

Prefer placeholders over premature meaning.
Structure first. Content later.
