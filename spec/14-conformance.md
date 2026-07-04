# Conformance (v2.0)

Three levels. Each level includes everything below it. "QIP-inspired" without meeting QIP-Core is a vocabulary choice, not a conformance claim.

## QIP-Core (the loop works)

- [ ] Tiered memory with the four tiers of spec/02, payload contract complete, tier/type/project/status indexed
- [ ] Fail-closed writes: canonical embeddings only, audit tool passes (`python -m qip audit`)
- [ ] Tiered retrieval order implemented (mind_pin → L3-active → semantic)
- [ ] Task lifecycle + heartbeat operational (spec/11); every completed task stores a lesson
- [ ] Decision Context construction before non-trivial decisions (spec/09)
- [ ] EI records with pre-registered predictions (spec/08)
- [ ] Collection routing enforced (spec/00)

## QIP-Gov (the loop is safe and auditable)

- [ ] Mesh Integrity complete: signing, provenance, quarantine, trust-weighted adoption, blast-radius recall (spec/10)
- [ ] Constitutional invariants I1-I7 enforced at runtime (spec/13)
- [ ] Guardian review queue active with nonzero rejection rate over time
- [ ] Inversion Detection scheduled against mind_pins and institutional narratives (spec/06)
- [ ] Decision captures carry DC summaries (audit reproducibility)
- [ ] Where in scope: AI Act mapping reviewed by counsel (spec/13)

## QIP-Full (the compounding is proven)

- [ ] Metrics engine live; CC and component metrics reported per period (spec/12)
- [ ] Falsifiability gate: pre-registered CC trajectory on record before results
- [ ] Wave Function Collaboration used for multi-agent decisions, synthesis artifacts with minority objections (spec/03)
- [ ] Frequency Orchestration with novelty routing; fast-path share rising for recurring families (spec/07)
- [ ] Ultra-low frequency self-evaluation cycles executed and captured
- [ ] External claims about compounding reproducible from the metrics tool

## Self-test

`python -m qip conformance` prints this checklist with live pass/fail where mechanically verifiable, and "manual" where human judgment is required. Mechanical passes are necessary, never sufficient.
