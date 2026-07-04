# Core 4: Indra's Mesh (Reflective Intelligence Compounding)

Plain language: when one agent learns something transferable, the generalized principle (not the local fix) is broadcast to shared memory, and every other agent interprets it through its own identity, producing applications the original agent could not have generated. This is the amplification mechanism; it is what makes the system multiplicative instead of additive.

## Broadcast protocol (five steps, v1.0, now integrity-wrapped)

1. Extract: the solving agent states the transferable principle, stripped of local specifics.
2. Encode: metadata attached: discovery context, confidence, applicability scope, decay class.
3. Sign and broadcast (v2.0): the principle is HMAC-signed by the emitting agent and written with full provenance, entering the Mesh in `status=quarantined` (spec/10). Unsigned or unattributed principles MUST NOT enter.
4. Filter: each receiving agent evaluates the principle through its own Decision Context and records applicability to its domain.
5. Integrate: agents that adopt the principle store it in their pattern layer with `parent_ids` pointing to the broadcast point. Adoption MUST respect the trust threshold (spec/10).

## Why integrity wrapping is not optional

The 2026-07-04 review finding is normative history: the Mesh's super-linear scaling applies equally to contamination. A poisoned principle broadcast without provenance would be identity-filtered into every agent's pattern layer, at the same compounding rate claimed for learning. Steps 3 and 5 exist so that the amplification math only runs on verified inputs. A Mesh implementation without quarantine and trust weighting is nonconformant (spec/14).

## Scaling property

Each adoption event multiplies rather than adds because the receiving identity generates novel combinations with its existing patterns. The measurable expression is the principle adoption rate and cross-domain reuse count (spec/12), which replace the unmeasurable Φ as the system's integration metric.

## Requirements

- Broadcasts MUST be principles, not solutions. A capture that names project-local entities in its normative sentence is a lesson (stays local), not a principle.
- Every adoption MUST increment the source principle's `access_count` and append the adopter to `adopted_by`; the metrics engine reads these.
- Principles that reach zero adoptions across a full ultra-low frequency cycle SHOULD decay to archive status.
