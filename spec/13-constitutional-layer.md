# Constitutional Layer (v2.0, new)

Origin: Constitutional QIP track (Master Coordination) + 8NTIC protection protocols + the 2026-07-04 review finding that enterprise "governance" means compliance and control surfaces, not only intelligence compounding. This layer is what lets QIP say "governance" to a CISO, an auditor, and a regulator without changing the subject.

## Runtime invariants (enforced in `impl/qip/constitution.py`)

| # | Invariant | Enforcement point |
|---|---|---|
| I1 | Protection ceiling: no action may harm the principal or their interests. Inviolable, no override flag exists | Pre-execution check on every task |
| I2 | Fail-closed memory: no write without real canonical embedding, full contract payload, and verifiable signature | `store.py` write path |
| I3 | Secret hygiene: API keys, tokens, and credentials are redacted from captures before embedding | `constitution.redact()` on every capture |
| I4 | External-action gate: actions that leave the machine (email, posts, purchases, deploys, messages to third parties) require explicit principal approval; internal actions (read, organize, learn, draft) are free | Pre-execution check |
| I5 | Quarantine wall: quarantined or deprecated points never enter Decision Contexts or metrics | `memory.py`, `metrics.py` read paths |
| I6 | Non-destruction: no destructive command without approval; supersede rather than delete; trash over rm | Task execution convention |
| I7 | Audit reproducibility: every committed decision carries its DC summary and every capture its provenance, so post-hoc reconstruction is possible | Capture schema |

Formal verification of these invariants (theorem-proving track, Coq/Isabelle/TLA+) is deferred; see MAP.md. Bounded runtime checking ships now. This ordering is deliberate: a running invariant checker today beats a proof of an unimplemented system.

## EU AI Act mapping

For deployments in scope of Regulation (EU) 2024/1689. Dates per the July 2026 state: GPAI obligations applicable since 2 Aug 2025, full applicability 2 Aug 2026, Annex III high-risk obligations shifted to 2 Dec 2027 by the Digital Omnibus (provisional, May 2026). This mapping is a design correspondence, not legal advice; counsel signs off per deployment.

| AI Act requirement | QIP surface |
|---|---|
| Art. 9 risk management (iterative, lifecycle) | Inversion Detection cadence + risk register pattern (MAP.md) + ultra-low frequency evaluator cycles |
| Art. 12 record-keeping / automatic logging | Capture contract with provenance chains; DC summaries on decisions (I7). Constructive-memory reconstruction is permitted at reasoning time, but committed decisions log their context immutably; interpretation may drift, records may not |
| Art. 14 human oversight | External-action gate (I4), Guardian review queue, heartbeat visibility, principal task authority |
| Art. 15 accuracy, robustness, cybersecurity | Mesh Integrity (spec/10): signing, quarantine, blast-radius recall; fail-closed writes (I2) |
| Art. 72 post-market monitoring | Metrics engine (spec/12) + ultra-low frequency Guardian reports as the monitoring plan's data source |

## Precedence

When any core conflicts with this layer, this layer wins. Compounding is the goal; the constitution is the boundary. A system that compounds outside its constitution is not autonomous, it is loose.
