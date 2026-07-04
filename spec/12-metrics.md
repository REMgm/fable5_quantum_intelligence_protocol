# Metrics and Falsifiability (v2.0, new)

The thesis claimed measurable compounding but named only Φ, which cannot be computed for systems of realistic size. v2.0 replaces aspiration with instrumentation. These metrics make the Compound Autonomy Thesis falsifiable; if they stay flat, the thesis is wrong for that deployment and the deployment must change or the claim must be retracted.

## Core metrics (computed by `python -m qip metrics`)

| Metric | Definition | Compounding signal |
|---|---|---|
| Lesson reuse rate | Fraction of executions whose DC contained at least one prior lesson that shaped the outcome | Rising |
| Principle adoption rate | Adoptions per broadcast principle, across identities | > 1 sustained |
| Cross-domain adoption share | Fraction of adoptions where adopter domain ≠ author domain | Nonzero and rising (this is the Mesh's actual multiplier) |
| Fast-path share | Fraction of tasks routed `fast` (pattern hit) per period | Rising for recurring task families |
| Decision reversal rate | Committed decisions later reversed per period | Falling |
| Prediction error trend | EI predicted-vs-observed divergence over time | Falling |
| Quarantine rejection rate | Principles rejected or deprecated in review | Nonzero (zero means review is theater) |
| Re-paid lesson count | Failed assumptions recurring after a prior identical failure capture | Approaching zero |

## The compounding coefficient

Headline number: `CC = (reuse events + adoption events) / new lessons stored`, per period. CC < 1: the system writes more than it learns (archive, not intelligence). CC ≈ 1: linear. CC > 1 sustained: compounding. Report CC with its trend, never as a point value.

## Falsifiability gate

Every deployment MUST pre-register, at activation: expected CC trajectory at 30/90/180 days, the task families expected to shift toward fast-path, and the review cadence. Pre-registration is the Einstein Gateway applied to the protocol itself: hypothesis first, then evidence, and the hypothesis on record before results exist.

## Honesty constraints

- Metrics read only integrity-passing points (spec/10); poisoned reuse must not count as capability.
- Empty heartbeats, "nothing durable" traces, and rejections are reported, not hidden; their absence is a red flag, not a green one.
- Numbers reported outside the system (decks, papers, client reports) MUST be reproducible from `python -m qip metrics --window <period>` output. The 3-5 year advantage claims of v1.0 are hypotheses awaiting this data, and MUST be labeled as such until it exists.
