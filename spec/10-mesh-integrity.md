# Mesh Integrity (v2.0, new)

Added in response to the 2026-07-04 thesis review finding: Indra's Mesh is the architecture's highest-bandwidth contamination channel. The same identity-filtered broadcast that compounds learning super-linearly compounds poisoned principles super-linearly. QIP without Mesh Integrity is nonconformant (spec/14).

## Threat model

| Threat | Vector | Consequence without integrity |
|---|---|---|
| Memory poisoning | Prompt injection into any low-privilege agent that then broadcasts | System-wide adoption of attacker-authored principles |
| Provenance spoofing | Unsigned principle claiming a trusted source | Trust laundering |
| Context manipulation | Poisoned patterns entering Decision Contexts | Systematically skewed decisions (spec/09) |
| Drift amplification | Honest but wrong principle adopted widely before validation | Compounded error at learning speed |

## Mechanisms

### Provenance (mandatory)
Every broadcast carries `agent_id`, `parent_ids` (chain to originating task/lesson), `timestamp`, and discovery context. A principle with no reconstructable chain MUST be rejected at write time.

### Signing (mandatory)
Broadcasts are HMAC-SHA256 signed over `(topic, full_text, timestamp, agent_id)` with the emitting agent's key. Agent keys are registered in `qip_agents`. Verification failure MUST reject the point, fail-closed, same as embedding failure.

### Quarantine (mandatory)
New principles enter `status=quarantined` with initial `trust=0.30`. Quarantined principles are excluded from Decision Context construction and from adoption. They are visible only to Guardian review (`python -m qip review`).

### Trust-weighted adoption (mandatory)
Promotion to `status=active` requires either explicit Guardian approval or the auto-promotion rule: N independent validations (default 2) by agents other than the author, each recorded as a validation capture. Adoption by receiving agents requires `status=active` AND `trust ≥ QIP_TRUST_THRESHOLD` (default 0.60). Trust rises with validated reuse, falls with contradiction, and a principle contradicted by an inversion result (spec/06) is demoted to `status=deprecated`, never silently deleted; the contradiction is part of system memory.

### Blast-radius accounting
Because `adopted_by` chains are recorded, a poisoned or deprecated principle's downstream adopters are enumerable. Deprecation MUST cascade a review flag to every adopter's derived patterns. This turns the worst-case scenario from "unknowable contamination" into a bounded, auditable recall.

## Interaction with compounding

Integrity is not friction on compounding; it is what makes claimed compounding real. Unverified amplification amplifies noise, and the metrics (spec/12) would report it as capability. Quarantine throughput and rejection rate are therefore first-class metrics, not ops trivia.
