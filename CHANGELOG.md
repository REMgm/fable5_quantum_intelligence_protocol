# Changelog

## v2.0.0 — 2026-07-05 (Fable5 edition, this repo)

Consolidates thesis v1.0, framework v1.1, and the 2026-07-04 thesis review into one executable protocol.

Added
- `spec/10-mesh-integrity.md` + `impl/qip/mesh.py`: provenance chains, HMAC-signed principles, quarantine tier, trust-weighted adoption. Closes the memory-poisoning gap: the compounding channel was also the contamination channel.
- `spec/12-metrics.md` + `impl/qip/metrics.py`: operational compounding metrics (lesson reuse rate, principle adoption rate, decision reversal rate, quarantine rejection rate). Replaces unmeasurable Φ as the success metric. Makes the Compound Autonomy Thesis falsifiable.
- `spec/13-constitutional-layer.md` + `impl/qip/constitution.py`: runtime invariants (protection ceiling, secret redaction, external-action gate, fail-closed writes) and EU AI Act mapping (Articles 9, 12, 14, 15, 72).
- `spec/08-execution-intelligence.md`, `spec/09-decision-context.md`: cores 8 and 9 from Framework v1.1 promoted into the canonical spec.
- `spec/11-compound-autonomy-loop.md`: CAL v2 unifies the operational loop (Task → Heartbeat → Memory-Informed Execution → Lesson Stored) with the cognitive loop (PERCEIVE → DC → DECIDE → ACT/EI → LEARN → EVOLVE).
- Scalable EI routing (`impl/qip/routing.py`): novelty-scored Fast/Smart/Deep execution paths, hybrid metric, pluggable.
- Fail-closed ingest with schema normalization (`impl/qip/store.py`): required payload fields tier+type+project enforced and indexed; normalizes the `qip_capture_v1` drift (summary/memory_tier → topic/tier).

Changed
- Architecture is 9-core (7 QIP principles + EI + DC), per 8NTIC CEO Activation and Framework v1.1.
- Collection routing formalized: business → `qip_knowledge`, swarm/research → `qip_research`, session/tasks → `qip_memory`, registry → `qip_agents`, sources → `qip_documents` (per 2026-07-04 split).
- Quantum vocabulary retained as naming; every mechanism also stated in plain systems language. The isomorphism claim is dropped from normative text.

## v1.1 — 2026-04-03 (8NTIC Framework)
- Added Execution Intelligence (EI) and Decision Context (DC); Enhanced Compound Autonomy Loop; agent operational matrix.

## v1.0 — 2026-03-09 (Thesis)
- Seven principles: Einstein Gateway, Identity Core, Wave Function Collaboration, Indra's Mesh, Active Participation, Inversion Detection, Frequency Orchestration. MCP Synaptic Layer. Five-layer composable stack.
