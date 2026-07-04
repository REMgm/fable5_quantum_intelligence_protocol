# MAP.md — from the map to the repo

The "map" is the 8NTIC research corpus in the `qip_research` collection (404 points, 13 sources), plus the business mind_pins in `qip_knowledge`. This file is the traceability matrix: every learning extracted from the map, and where it is implemented here. If it is not in this table, it was deliberately deferred (see Open Decisions).

## Sources analyzed

| Source (qip_research) | Points | What it contributed |
|---|---|---|
| Master Coordination | 27 | Three research tracks, dependency matrix, risk register, program phases |
| QIP Framework v1.1 | 19 | EI + DC definitions, enhanced loop, operational matrix |
| 8NTIC CEO Activation | 20 | 9-core architecture, 3-2-4-1 activation, BRAIN tiers, protection ceiling |
| AGENTS.md | 16 | Heartbeat protocol, memory conventions, red lines, external-action gate |
| QIP Unified Schema | 44 | Payload schema vocabulary |
| Constitutional / Scalable EI / Embodied deep dives | 75 | Track designs (constitutional invariants, Fast/Smart/Deep routing, embodiment deferred) |
| Tracks (Phenomenology, Signal Systems, Neuro-Physics) | 162 | Research context; not normative for v2.0 |
| 8NTIC Daily Log | 17 | Activation sequence history |

Plus `qip_knowledge` mind_pins: infrastructure canonical state (2026-06-28), collection split (2026-07-04), thesis review findings (2026-07-04).

## Learning → implementation

| # | Learning from the map | Implemented in |
|---|---|---|
| 1 | QIP is 9-core, not 7: EI and DC were added in v1.1 and never merged into the thesis | `spec/08`, `spec/09`, canonical list in `spec/00` |
| 2 | Enhanced CAL: PERCEIVE → [Construct DC] → DECIDE → ACT with EI → LEARN → EVOLVE | `spec/11-compound-autonomy-loop.md`, `impl/qip/loop.py` |
| 3 | Operational CAL: Agent Creates Task → Heartbeat Picks Up → Memory Informs Execution → Lesson Stored | Same files; the two loops are formally unified in spec/11 |
| 4 | EI protocol: Predict/Tag before, Monitor/Adapt during, Imprint/Reflect/Broadcast after | `impl/qip/loop.py` (`ExecutionRecord`), spec/08 |
| 5 | DC construction: Identity Filter (LT_) → Pattern Scan (MT_) → Objectives (ST_) → Environment | `impl/qip/memory.py` (`build_decision_context`), spec/09 |
| 6 | BRAIN tier naming ST_/MT_/LT_ maps to tiers L3-active / L2-mid+L1-long / mind_pin | `spec/02-identity-core.md` |
| 7 | Constitutional QIP track: runtime invariant checking, formal constraints, SENTINEL role | `spec/13`, `impl/qip/constitution.py` (bounded runtime checks now; theorem proving deferred) |
| 8 | Scalable EI track: novelty-based routing to Fast/Smart/Deep execution tiers | `spec/07` §routing, `impl/qip/routing.py` |
| 9 | Heartbeat conventions: HEARTBEAT.md checklist, HEARTBEAT_OK, cron vs heartbeat split | `agents/HEARTBEAT.md`, `ops/runbook.md` |
| 10 | Red lines + external-vs-internal action gate + protection ceiling | `impl/qip/constitution.py`, `agents/AGENTS.md` |
| 11 | Canonical infra rule: every write MUST populate tier+type+project, and those fields MUST be indexed (strict mode broke tier retrieval when they weren't) | `impl/qip/store.py` (enforced), `python -m qip init` creates indexes |
| 12 | Collection routing: business → qip_knowledge, swarm/research → qip_research (2026-07-04 split rationale: research noise polluted business retrieval) | `impl/qip/config.py` (`COLLECTIONS`), `ops/ingest-contract.md` |
| 13 | Schema drift exists in the wild: `qip_capture_v1` writes summary/memory_tier/content, contract writes topic/tier/full_text | `impl/qip/store.py` (`normalize_payload`) reads both, writes contract form |
| 14 | Thesis review 2026-07-04: Mesh is also the poisoning channel → provenance, signing, quarantine, trust | `spec/10-mesh-integrity.md`, `impl/qip/mesh.py` |
| 15 | Thesis review: Φ is unmeasurable → operational compounding metrics or the thesis is unfalsifiable | `spec/12-metrics.md`, `impl/qip/metrics.py` |
| 16 | Thesis review: "governance" must meet the EU AI Act definition, not only the compounding definition | `spec/13-constitutional-layer.md` §AI-Act mapping |
| 17 | 404 migrated research points lack full_text (pre-contract); remediation pending | `python -m qip audit --strict` flags them; remediation runbook in `ops/runbook.md` |

## Open decisions from the map, and the v2.0 stance

| Decision (Master Coordination) | v2.0 stance |
|---|---|
| Theorem prover: Coq vs Isabelle vs TLA+ | Deferred. Runtime invariant checking ships now (`constitution.py`); formal proofs are a v2.x track. TLA+ recommended when it starts: the invariants are temporal, not type-theoretic |
| Novelty metric: novelty vs surprise vs hybrid | Hybrid implemented as default (embedding distance × pattern-hit-rate), pluggable via `routing.py` |
| Robotics platform (Embodied QIP) | Out of scope for this repo; embodiment SDK belongs in a separate repo once Constitutional guarantees exist |
| Commercial vertical | Not a protocol concern; lives in qip_knowledge business tier |

## Known debt carried forward

One open client-delivery reconciliation item from the mind_pins belongs in the task queue, not in documentation; it has been filed in `qip_memory` where the details live. Rule made explicit by this very line: public repo files never carry client names, engagement details, or internal dates. Constitutional invariant I3 (secret hygiene) extends to client-confidential context in any artifact that leaves the private memory system.
