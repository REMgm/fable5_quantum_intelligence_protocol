# Compound Autonomy Loop (CAL v2)

The master cycle. Everything else in QIP exists so that this loop compounds instead of resets.

## Two loops, one cycle

The operational loop (how work moves) and the cognitive loop (how intelligence moves) are the same cycle observed at different layers:

| Operational (v1.0 short form) | Cognitive (v1.1 enhanced form) | Governed by |
|---|---|---|
| Agent creates task | PERCEIVE (signal becomes intent) | spec/05, spec/07 |
| Heartbeat picks up | Construct DECISION CONTEXT | spec/09, spec/02 |
| Memory informs execution | DECIDE (WFC / solo collapse) then ACT with EI | spec/03, spec/01, spec/08 |
| Lesson stored | LEARN (Mesh, integrity-wrapped) | spec/04, spec/10 |
| (next cycle starts smarter) | EVOLVE (identity refinement) | spec/02, spec/06 |

Normative statement: each full cycle MUST increase future capability, not merely log activity. The metrics layer (spec/12) is the enforcement mechanism; a deployment whose fast-path reuse and adoption rates stay flat across cycles is running a workflow engine, not CAL.

## Task lifecycle (reference implementation semantics)

```
open ──heartbeat──▶ in_progress ──execution──▶ done
                        │                        │
                        ▼                        ▼
                     blocked              lesson stored (mandatory)
                                                 │
                                          principle extracted? ──▶ Mesh (quarantined)
```

- Tasks live in `qip_memory` (`type=task`) with `status`, `project`, `frequency`, and optional `collapse_deadline`.
- A task completed without a lesson capture is nonconformant. "Nothing durable learned" is itself a recordable outcome (`type=execution_trace`), and its frequency is diagnostic.
- Task creation is open to all agents and to the system itself: EVOLVE SHOULD emit new tasks (gaps noticed, inversions due, remediations pending). Self-generated tasks are how autonomy compounds; principal-generated tasks are how it stays aimed.

## Heartbeat semantics

The heartbeat is the metronome of autonomy: a scheduled wake (cron, launchd, or platform scheduler) that runs `python -m qip heartbeat`.

1. Read HEARTBEAT.md checklist if present (agents/HEARTBEAT.md template)
2. Pull open tasks for this agent's frequency tier, oldest deadline first
3. For each task claimed: build Decision Context, emit an execution brief (task + DC + EI pre-execution block), mark `in_progress`
4. If nothing needs attention: reply `HEARTBEAT_OK` and exit quietly; an empty heartbeat is a valid heartbeat

The reasoning engine (Fable5 or peer agent) consumes the brief, does the work, then calls `python -m qip lesson` to close the cycle. The harness never fakes the reasoning; the model never bypasses the harness.

## Anti-reset rule

No state may live only in a chat session. If it matters beyond the current turn, it is a capture; if it is a capture, it obeys the ingest contract (ops/ingest-contract.md). Sessions are disposable; the loop is not.
