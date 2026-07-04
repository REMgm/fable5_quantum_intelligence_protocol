# QIP Ingest Contract (fail-closed)

The write contract every agent obeys, on every collection, with no exceptions. Codified from the 2026-06-14 protocol change, hardened by the 2026-06-28 canonical-state findings and the 2026-07-04 split. `impl/qip/store.py` is the reference enforcement.

## Embedding rules

- Provider: OpenAI. Model: `text-embedding-3-small`. Dimensions: 1536. Distance: Cosine
- Embed the full source text or full chunk text, never the preview
- Forbidden, write MUST fail if attempted: placeholder vectors, hash vectors, lexical pseudo-embeddings, preview-only embeddings, points missing `embedding_model`, points missing `embedding_status`
- After ingest, run the audit (`python -m qip audit`). Audit failure means the write failed, remove or remediate; there is no "mostly ingested"

## Required payload (every point, every collection)

```
source              writer identity or pipeline name
topic               kebab/snake summary key (normalized from `summary` if legacy)
type                decision | insight | research_finding | code_pattern | user_preference |
                    protocol_change | operational_rule | failed_assumption | accepted_architecture |
                    task | lesson | principle | execution_trace | inversion_result | hypothesis_result
tier                mind_pin | L1-long | L2-mid | L3-active
project             project stamp (QIP-CORE if none)
timestamp           ISO-8601 UTC
embedding_model     text-embedding-3-small
embedding_status    embedded
content_preview     display string, ≤ 200 chars
full_text           the embedded text itself
agent_id            emitting agent
signature           HMAC-SHA256 (spec/10); principles MUST, other types SHOULD
status              active | quarantined | deprecated  (principles start quarantined)
trust               float 0..1 (principles start 0.30)
parent_ids          provenance chain, [] allowed for roots
access_count        int, maintained by readers
adopted_by          agent list, principles only
```

`tier`, `type`, `project`, `status` MUST have payload indexes (strict-mode clusters return nothing on unindexed filters; this outage happened, 2026-06-28).

## Collection routing

Business/strategy → `qip_knowledge`. Swarm/research → `qip_research`. Session state and tasks → `qip_memory`. Agent registry → `qip_agents`. Source chunks → `qip_documents`. Wrong-collection writes are contract violations even when otherwise valid.

## Capture triggers

Write when any occurs: decision, insight, research finding, code pattern, user preference, protocol change, operational rule, failed assumption, accepted architecture. Write durable knowledge, not transient narration. When in doubt whether it is durable: would an agent six weeks from now act differently for knowing it? No → not a capture.

## Legacy compatibility

Readers MUST accept `qip_capture_v1` drift fields (`summary`→topic, `memory_tier`/`decay_class`→tier, `content`→full_text, `knowledge_type`→type) and SHOULD rewrite to contract form on touch. Writers MUST emit contract form only. The 404 migrated research points lacking `full_text` are flagged by `audit --strict` and queued for remediation (MAP.md).
