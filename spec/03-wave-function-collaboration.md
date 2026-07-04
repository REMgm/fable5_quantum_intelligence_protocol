# Core 3: Wave Function Collaboration

Plain language: when several agents work one problem, keep their explorations independent for as long as possible, share raw observations rather than conclusions, and only then let positions form. This is anti-anchoring engineering; premature sharing of conclusions collapses the group onto whoever spoke first.

## Four phases

### Phase 1: Superposition
Each agent explores independently through its own Decision Context (spec/09). No conclusions cross agent boundaries. Agents MUST NOT read each other's working notes in this phase.

### Phase 2: Reflection
Agents share observations, not conclusions. An observation is evidence, data, or a pattern noticed; a conclusion is a recommendation or verdict. The distinction is enforced editorially: shared artifacts in this phase MUST NOT contain recommendation language.

### Phase 3: Collapse
Each agent independently commits to its own conclusion, informed by the shared observation pool. Divergence at this point is signal, not failure; it maps the genuine shape of the possibility space.

### Phase 4: Synthesis
Structured dialectic among collapsed positions produces the committed course of action. Synthesis is not majority voting and not seniority. The synthesis artifact MUST record the surviving minority objections; these become inversion triggers (spec/06) if the decision later drifts.

## Timing governance

Premature collapse loses exploration value; deferred collapse degrades coherence. The heartbeat (spec/11) carries a collapse deadline per task. When the deadline arrives, Phase 3 executes with whatever exploration exists.

## Requirements

- Two or more agents on one problem MUST use the four phases; skipping Phase 2 sharing discipline is the most common implementation error and defeats the core.
- Solo agents SHOULD simulate superposition via the Einstein Gateway's three-hypothesis rule (spec/01).
- Every synthesis MUST store a `decision` capture with `parent_ids` linking the collapsed positions, so decision reversal can be measured (spec/12).
