# HEARTBEAT.md — Wake-Cycle Checklist Template

Read by every heartbeat run before task pickup. Keep this file short; it burns tokens on every wake. Edit freely; this is a template, not scripture.

## On every heartbeat

1. `python -m qip heartbeat` has already pulled your open tasks; read the briefs
2. Anything blocked longer than 2 cycles: escalate to principal or re-scope
3. Any `collapse_deadline` inside the next cycle: prioritize its Phase 3

## Periodic (roughly weekly, pick a quiet heartbeat)

- Run `python -m qip review`: clear the quarantine queue, reject at least honestly
- Run `python -m qip metrics --window 7d`: is CC trending, or are we logging activity?
- Scan L3-active for loops that should be closed, demoted, or turned into tasks

## Periodic (roughly monthly)

- Inversion pass on one mind_pin narrative (spec/06): pick the one that feels most certain
- Memory maintenance: distill lessons worth keeping, deprecate what aged out
- Re-read the falsifiability pre-registration: are we on the predicted trajectory?

## Rules

- Nothing needs attention: output `HEARTBEAT_OK` and stop. An empty heartbeat is a valid heartbeat; manufactured busywork poisons the metrics
- Never infer stale tasks from old chats; the task queue is the only source of truth
- Heartbeat for batchable drift-tolerant checks; cron for exact-time isolated jobs
