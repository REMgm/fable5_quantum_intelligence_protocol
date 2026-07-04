# Core 9: Decision Context (DC)

Origin: Framework v1.1 operational addendum (2026-04-03), promoted to canonical core in v2.0.

Plain language: no decision runs on raw data. Every decision runs on meaning, and meaning is constructed by passing raw inputs through accumulated identity, recognized patterns, current objectives, and a live read of the environment. Two agents with different identities will, correctly, decide differently on identical inputs. There is no context-independent right answer; the protocol therefore governs context construction explicitly instead of pretending it away.

## Construction pipeline (normative order)

```
RAW INPUTS
   ↓  [Identity Filter]      ← mind_pin tier (values, priorities, risk tolerance)
   ↓  [Pattern Layer Scan]   ← L1/L2 tiers ("this resembles X we have seen")
   ↓  [Current Objectives]   ← L3-active tier (what we are trying to achieve now)
   ↓  [Environmental Read]   ← live signals from high-frequency agents
DECISION CONTEXT  →  feeds Wave Function Collapse (spec/03) or solo decision
```

This is the retrieval order of spec/02 turned into a data structure. `impl/qip/memory.py::build_decision_context` is the reference implementation.

## DC components

| Component | Source | Function |
|---|---|---|
| Identity bias | mind_pin | Values, priorities, risk tolerance |
| Pattern recognition | L1-long / L2-mid | Precedent and analogy |
| Current objectives | L3-active | Immediate goals and constraints |
| Environmental read | Live sensors/scouts | Real-time state |

## Requirements

- A DC MUST be constructed before every non-trivial decision, and MUST be constructed fresh when entering a new problem domain; stale DCs are the operational form of paradigm lock.
- Conflicting contexts (identity says one thing, objectives another) MUST be surfaced to the Guardian role rather than silently resolved; context conflicts are inversion triggers (spec/06).
- DC construction is where context manipulation attacks land (poisoned patterns produce poisoned meaning). The pattern-scan step therefore reads only `status=active` points that satisfy the trust threshold (spec/10). Quarantined material MUST NOT enter a DC.
- The DC used for a committed decision SHOULD be summarized into the decision capture, so that audits can reconstruct why the decision made sense at the time (spec/13, Article 12).
