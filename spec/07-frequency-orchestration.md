# Core 7: Frequency Orchestration (Multi-Speed Agent Ecosystem)

Plain language: different problems live at different speeds. The ecosystem runs agents at four frequencies, and signals cascade between them: fast observations aggregate into patterns, patterns inform strategy, strategy recalibrates everything, and rare systemic reviews keep the whole cascade honest.

## Frequency tiers

| Tier | Roles | Cadence | Function |
|---|---|---|---|
| High | Scouts, Monitors | Continuous / minutes | Sensory input: streams, anomalies, signals |
| Mid | Executors, Optimizers | Task cycle / hours | Convert strategy into outcomes |
| Low | Architects, Strategists | Days / weeks | Pattern review, strategy refinement, model updates |
| Ultra-low | Guardians, Evaluators | Weeks / months | System self-evaluation: bias, drift, blind spots, inversion of mind_pins |

Requisite variety rationale (Ashby): the governance layer MUST match the temporal variety of its environment. A single-speed system either thrashes (all fast) or fossilizes (all slow).

## v2.0 addition: novelty-routed execution (Scalable EI track)

Within the mid tier, tasks route by novelty score to one of three execution paths:

| Path | Novelty | Behavior |
|---|---|---|
| `fast` | low (pattern hit) | Apply the cached pattern; minimal reasoning; log reuse |
| `smart` | medium | Standard reasoning informed by pattern layer |
| `deep` | high (no precedent) | Einstein Gateway mandatory; WFC if multi-agent; full EI protocol |

Default novelty metric is hybrid: embedding distance to nearest pattern-layer neighbors, weighted by historical pattern hit rate for the task family. The metric is pluggable (`impl/qip/routing.py`); the Master Coordination open decision (novelty vs surprise vs hybrid) is resolved as hybrid-by-default, replaceable by evidence.

Routing exists for economics as much as intelligence: fast-path reuse is the visible dividend of compounding, and its rate is a first-class metric (spec/12). A system where everything routes `deep` forever is, measurably, not compounding.

## Requirements

- Heartbeats (spec/11) MUST carry the frequency tier of the tasks they wake, so slow work is never starved by fast noise.
- Ultra-low cycles MUST run even when everything seems fine; that is when drift is cheapest to catch.
