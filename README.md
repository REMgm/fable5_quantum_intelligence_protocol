# Fable5 Quantum Intelligence Protocol (QIP v2.0)

Executable governance layer for autonomous agent systems. QIP is not an orchestration framework; it is the intelligence substrate that makes any orchestration framework (LangGraph, CrewAI, Claude Agent SDK, custom swarms) compound capability instead of resetting it.

This repo is the v2.0 consolidation of three sources: the Quantum Intelligence thesis (9 Mar 2026), the 8NTIC Framework v1.1 (EI/DC extension, Apr 2026), and the adversarial thesis review of 4 Jul 2026. The full source-to-implementation trace is in [MAP.md](MAP.md).

Plain language, one sentence: agents write every task, lesson, and decision into a tiered vector memory with signed provenance; a heartbeat wakes the executing agent, memory shapes the execution, the lesson goes back in, and measurable compounding is enforced rather than assumed.

## The loop

```
        AGENT CREATES TASK
               │                     (qip_memory, type=task)
               ▼
        HEARTBEAT PICKS UP
               │                     (cron/launchd → python -m qip heartbeat)
               ▼
   MEMORY INFORMS EXECUTION          (Decision Context: mind_pin → L3-active → semantic)
               │                     (Execution Intelligence: predict/monitor/adapt)
               ▼
         LESSON STORED               (Indra's Mesh broadcast, signed, quarantined,
               │                      trust-weighted adoption)
               └──────────► identity refined → next cycle starts smarter
```

Each cycle MUST increase future capability, not merely log activity. `python -m qip metrics` proves whether it does.

## The 9 cores

| # | Core | Function | Spec |
|---|------|----------|------|
| 1 | Einstein Gateway | Hypothesis-first processing | [spec/01](spec/01-einstein-gateway.md) |
| 2 | Identity Core | Three-tier memory as identity engine | [spec/02](spec/02-identity-core.md) |
| 3 | Wave Function Collaboration | Parallel decision architecture | [spec/03](spec/03-wave-function-collaboration.md) |
| 4 | Indra's Mesh | Reflective intelligence compounding | [spec/04](spec/04-indras-mesh.md) |
| 5 | Active Participation | Reality construction awareness | [spec/05](spec/05-active-participation.md) |
| 6 | Inversion Detection | Adversarial validation | [spec/06](spec/06-inversion-detection.md) |
| 7 | Frequency Orchestration | Multi-speed agent ecosystem | [spec/07](spec/07-frequency-orchestration.md) |
| 8 | Execution Intelligence | Action as intelligence generation | [spec/08](spec/08-execution-intelligence.md) |
| 9 | Decision Context | Identity-filtered meaning construction | [spec/09](spec/09-decision-context.md) |

v2.0 additions that make the protocol safe and falsifiable: [Mesh Integrity](spec/10-mesh-integrity.md), [CAL v2](spec/11-compound-autonomy-loop.md), [Metrics](spec/12-metrics.md), [Constitutional Layer](spec/13-constitutional-layer.md), [Conformance](spec/14-conformance.md).

## Quickstart

Requires Python 3.9+. Zero third-party dependencies (stdlib only, by design: the governance layer must not drag a framework with it).

```bash
git clone https://github.com/REMgm/fable5_quantum_intelligence_protocol.git
cd fable5_quantum_intelligence_protocol
cp .env.example .env            # fill in Qdrant + OpenAI keys. Never commit .env
cd impl

python3 -m qip init             # create collections + payload indexes (tier/type/project/status)
python3 -m qip audit            # fail-closed vector integrity audit
python3 -m qip task "Reconcile the open delivery-deadline conflict into the PM system" --project "CLIENT-X"
python3 -m qip heartbeat        # pick up open tasks, build Decision Context, emit execution brief
python3 -m qip lesson <task-id> "What was learned" --type insight
python3 -m qip retrieve "agentic commerce wedge"   # tiered retrieval
python3 -m qip review           # guardian queue: quarantined principles awaiting promotion
python3 -m qip metrics          # compounding metrics; the falsifiability gate
```

The harness is model-agnostic. Fable5 (or Claude Code, Kimi, codex) is the reasoning engine; the repo governs memory, provenance, routing, and safety around it. Agent operating instructions live in [agents/FABLE5.md](agents/FABLE5.md).

## Repository map

```
spec/     15 normative specs (RFC 2119 keywords)     ← what MUST happen
agents/   Fable5 system instructions, heartbeat,     ← who executes
          workspace conventions, role/frequency map
impl/     stdlib-only Python reference impl + CLI    ← how it executes
ops/      runbook (cron/launchd), ingest contract    ← how it stays alive
MAP.md    map → learning → implementation trace      ← why it is this way
```

## Non-negotiables (Constitutional Layer, enforced at runtime)

Fail-closed writes (embedding must be real, 1536-dim, canonical model, audited). Signed provenance on every Mesh broadcast; unsigned principles are never adopted. Quarantine before adoption. Secret redaction before capture. External actions gated. Protection ceiling is inviolable. See [spec/13](spec/13-constitutional-layer.md) for the EU AI Act mapping (Articles 9, 12, 14, 15, 72).

## Status

v2.0.0. Live against the production Qdrant cluster (five collections: qip_knowledge, qip_research, qip_memory, qip_agents, qip_documents). See [CHANGELOG.md](CHANGELOG.md).
