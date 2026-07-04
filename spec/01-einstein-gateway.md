# Core 1: Einstein Gateway

Hypothesis-first processing. Plain language: when data-grinding stalls, generate bold conjectures first and use data to attack them, instead of hoping conclusions precipitate out of more retrieval.

## Triggers

The Gateway MUST activate when any of the following is detected:

- Analysis paralysis: three or more consecutive retrieval/tool cycles with no new decision-relevant information
- Recursive search loops: the same query family issued twice without a changed hypothesis
- Diminishing returns: novelty score of retrieved material below 0.2 for two cycles (see spec/07 routing)
- Deep-path routing: any task the novelty router classifies as `deep`

## Protocol

1. STOP tool use. No further retrieval until a hypothesis exists.
2. Generate exactly three bold hypotheses from context already in hand. Bold means: falsifiable, non-obvious, and materially different from each other.
3. Select the most promising by expected information value, not by prior probability.
4. Work backward: what evidence would refute this? Gather only that evidence.
5. Collapse: accept, reject, or mutate the hypothesis. Record the outcome as a capture (`type=hypothesis_result`).

## Requirements

- Hypotheses MUST be recorded before validation begins, so that hindsight cannot rewrite them. This is the pre-registration rule; it feeds the falsifiability metrics (spec/12).
- A rejected hypothesis is a success condition, not a failure. Rejections MUST be stored with the same fidelity as confirmations; they are decay-resistant negative knowledge.
- The Gateway output feeds Wave Function Collaboration (spec/03) when more than one agent explores the same problem.

## Failure mode governed

Gap 4 of the thesis (premature consensus) and the competent-mediocrity trap: data-first grinding produces defensible, unremarkable conclusions. The Gateway trades defensibility during exploration for testability at collapse.
