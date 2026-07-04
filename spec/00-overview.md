# QIP v2.0 Overview and Conventions

## Status

Normative. The key words MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY are to be interpreted as in RFC 2119.

## What QIP is

The Quantum Intelligence Protocol governs how a system of autonomous agents remembers, decides, learns, and stays safe, so that capability compounds across interaction cycles instead of resetting with each session. It sits above orchestration frameworks and below the human interface. Orchestration moves tasks; QIP moves intelligence.

Quantum vocabulary is a naming layer. Every mechanism in this spec is also stated in plain systems language, and the plain statement is the normative one. QIP claims no quantum-mechanical behavior in agents and requires no quantum hardware.

## The 9 cores

Seven principles from thesis v1.0 plus two operational components from Framework v1.1:

1. Einstein Gateway: hypothesis-first processing (spec/01)
2. Identity Core: three-tier memory as identity engine (spec/02)
3. Wave Function Collaboration: parallel decision architecture (spec/03)
4. Indra's Mesh: reflective intelligence compounding (spec/04)
5. Active Participation: reality construction awareness (spec/05)
6. Inversion Detection: adversarial validation (spec/06)
7. Frequency Orchestration: multi-speed agent ecosystem (spec/07)
8. Execution Intelligence: action as intelligence generation (spec/08)
9. Decision Context: identity-filtered meaning construction (spec/09)

v2.0 adds three cross-cutting layers that the first nine depend on: Mesh Integrity (spec/10), Metrics (spec/12), and the Constitutional Layer (spec/13). The Compound Autonomy Loop (spec/11) is the master cycle that binds all of them.

## Terminology

| Term | Meaning |
|---|---|
| Agent | Any reasoning process with an identity: Fable5, Claude Code, Kimi, codex, a swarm role |
| Principal | The human the system serves. Protection of the principal is inviolable |
| Capture | A durable write to vector memory under the ingest contract |
| Lesson | A capture produced by executing a task |
| Principle | A transferable generalization broadcast through Indra's Mesh |
| Tier | Memory stratum: `mind_pin`, `L1-long`, `L2-mid`, `L3-active` |
| Heartbeat | Scheduled wake-up that drives the operational loop |
| Guardian | Agent (or human) that reviews quarantined principles and system drift |

## Layer stack (from thesis v1.0, unchanged)

1. Infrastructure (cloud, compute, storage)
2. Connectivity (MCP synaptic layer, Qdrant collections)
3. Agent ecosystem (multi-frequency agents)
4. Intelligence (this protocol)
5. Interface (human-AI cognitive bridge)

## Collections (canonical since the 2026-07-04 split)

| Collection | Content | Writers |
|---|---|---|
| `qip_knowledge` | Business and strategy knowledge, mind_pins | All agents, business captures only |
| `qip_research` | Swarm and research corpus (8NTIC tracks) | Research agents only |
| `qip_memory` | Session state, task queue, experience buffer | The loop (spec/11) |
| `qip_agents` | Agent registry, identities, public keys | Guardian |
| `qip_documents` | Source document chunks | Ingest pipelines |

Routing is normative: business knowledge MUST NOT be written to `qip_research`, and research/swarm output MUST NOT be written to `qip_knowledge`. Rationale: retrieval quality; the 2026-07-04 split removed 97% research noise from business reads.
