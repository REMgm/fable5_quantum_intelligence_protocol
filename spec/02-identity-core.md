# Core 2: Identity Core (Three-Tier Memory as Identity Engine)

Plain language: memory is not storage, it is the filter that decides what the system notices, keeps, and becomes. Two agents with different accumulated memory process identical input differently, and that difference is the system's identity.

## Tiers

| Tier label | BRAIN name (v1.1) | Cognitive analog | Content | Decay |
|---|---|---|---|---|
| `L3-active` | ST_ (short-term) | Working / episodic | Session state, active projects, open loops | Weeks; demote or expire |
| `L2-mid` | MT_ (mid-term) | Semantic patterns | Validated patterns, heuristics, playbooks | Reinforced by reuse, fades unused |
| `L1-long` | MT_/LT_ boundary | Consolidated knowledge | Stable operational rules, code patterns | Slow decay |
| `mind_pin` | LT_ (long-term) | Autobiographical | Identity, values, canonical infrastructure state, accepted architectures | No decay; explicit supersession only |

## Retrieval order (normative)

Before informing any decision or write, an agent MUST retrieve in this order:

1. `mind_pin` (who we are, canonical state)
2. `L3-active` (what is live right now)
3. Semantic search across the routed collection (what do we know about this)

This order is the Identity Filter in operation: identity first, situation second, knowledge third.

## Payload contract (enforced fail-closed in impl/qip/store.py)

Every point MUST carry: `source`, `topic`, `type`, `tier`, `project`, `timestamp`, `embedding_model`, `embedding_status`, `content_preview`, `full_text`, and v2.0 provenance fields (`agent_id`, `signature`, `status`, `trust`, `parent_ids`). `tier`, `type`, `project`, and `status` MUST have payload indexes; the 2026-06-28 canonical-state finding showed that tiering stored only as convention (unindexed, null) silently breaks retrieval under strict mode.

Vectors MUST be real embeddings from the canonical model (`text-embedding-3-small`, 1536, cosine). Hash vectors, lexical pseudo-embeddings, placeholders, and preview-only embeddings are forbidden. A write that cannot embed MUST fail, not degrade.

## Identity evolution

Identity is written only through the loop (spec/11): lessons promote to patterns, patterns that repeatedly survive reuse and inversion (spec/06) MAY be promoted to `mind_pin` by a Guardian. Nothing writes directly to `mind_pin` mid-task. Demotion is allowed; deletion of `mind_pin` entries requires a superseding entry that names what it replaces (see the 2026-06-28 cluster-supersession precedent).

## Failure modes governed

Gap 1 (stateless processing) and Gap 3 (identity vacuum). v2.0 adds the guard against identity lock-in: because the loop is self-reinforcing (identity shapes what is stored, storage shapes identity), the Inversion Detection core MUST run against `mind_pin` content on the ultra-low frequency cycle (spec/07), and reproducibility of retrieval MUST be preserved for audit (spec/13, Article 12 mapping).
