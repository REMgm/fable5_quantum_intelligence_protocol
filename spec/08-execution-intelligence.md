# Core 8: Execution Intelligence (EI)

Origin: Framework v1.1 operational addendum (2026-04-03), promoted to canonical core in v2.0.

Plain language: execution is bidirectional. Every action is simultaneously a work product and a training signal. A system that executes without imprinting learns nothing from its own operations; a QIP system treats execution traces as the primary raw material of compounding.

## The EI protocol

```
PRE-EXECUTION
  Predict : what will this action change in the environment?
  Tag     : what intelligence will this execution generate?

DURING EXECUTION
  Monitor : what unexpected patterns are emerging?
  Adapt   : where does reality diverge from the prediction?

POST-EXECUTION
  Imprint : store execution traces in the pattern layer
  Reflect : what did we learn about the environment?
  Broadcast : if a transferable principle emerged, hand it to Indra's Mesh (spec/04)
```

## EI versus conventional execution

| Conventional | Execution Intelligence |
|---|---|
| Execute task, mark complete | Execute task, generate insight |
| Success = output delivered | Success = output delivered + pattern recognized |
| Errors are failures | Errors are signal that refines the prediction model |
| Environment is static | Environment is shaped by execution (spec/05) |

## Requirements

- Every heartbeat-driven execution (spec/11) MUST produce an ExecutionRecord containing prediction, divergence notes, and imprint decision, even when the imprint decision is "nothing durable". The record is what makes prediction error measurable (spec/12).
- Predictions MUST be written before execution starts; the pre-registration rule from spec/01 applies to operations, not only research.
- Error captures (`type=failed_assumption`) are mandatory, not optional. Skipped error imprints are the single largest silent killer of compounding: the system re-pays for the same lesson.

## Role assignment

Executor-class agents lead EI; monitor-class agents watch divergence in real time; all agents carry EI awareness. In single-agent deployments (Fable5 solo), the one agent performs all three EI roles sequentially.
