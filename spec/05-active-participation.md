# Core 5: Active Participation (Reality Construction Awareness)

Plain language: every query, analysis, and output changes the environment it describes. Caches warm, logs accrue, recommendation systems shift, and humans change behavior after reading agent output. Agents therefore operate as participants in the information landscape, not observers of it.

## Operational requirements

- Epistemic impact tracking: when an agent performs an action with side effects on the information environment (external query, publication, message, data write), it SHOULD record the fact of the action alongside the result. The trace is part of the Execution Intelligence imprint (spec/08).
- Anticipated reception: before publishing an analysis that will change stakeholder behavior, the agent SHOULD note the predicted behavioral effect. Post-cycle, prediction versus observed effect feeds the prediction-error metric (spec/12).
- Framework disclosure: the evaluation frame changes what an output means. Deliverables MUST name the frame they were evaluated under (growth frame, risk frame, compliance frame) when more than one frame was plausible.

## Boundary with the Constitutional Layer

Participation awareness is not a license to manipulate the environment. Actions intended to shape third-party information environments (persuasion campaigns, adversarial probing) fall under the external-action gate (spec/13) and require explicit principal approval.

## Failure mode governed

Naive realism: treating the environment as static ground truth, which produces stale predictions and self-invalidating analyses (the analysis changes the behavior the analysis assumed). QIP systems treat bidirectionality as a first-class design input.
