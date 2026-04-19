# Agent Guidelines

Welcome, AI Agent. This repository models the infrastructure, network, roles, and migration paths of devices.
When operating within this repository, adhere strictly to the following rules:

1. **Separation of Concerns**:
   - Exclusively use `data/assignments/` for role assignments.
   - Never use `data/relations/` for role assignments; keep it restricted to general graph edges (`connected_to`, `depends_on`, `managed_by`, `trusts`, `exposed_to`).
2. **Heterogeneity**:
   - Devices must include fields for heterogeneity (e.g., `category`, `visibility`, `management_model`, `trust_zone`).
   - Networks are not strictly IPv4. Always use `transport` and `scope` to model the full network context.
3. **Epistemic State**:
   - Assignments must model target states conservatively. Use the `confidence` field (`confirmed`, `planned`, `speculative`) to denote the reality of an assignment. Do not treat future architectures as facts unless confirmed.
4. **Validation**:
   - Always validate any modifications to `data/` against `schemas/`.
