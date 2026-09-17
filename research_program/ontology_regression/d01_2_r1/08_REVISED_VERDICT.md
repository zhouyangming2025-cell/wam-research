# D01.2-R1 Revised Verdict

## Verdict

**HOLD-STRUCTURAL-PRESSURE**

## Why this is not FAIL-ABSTRACTION

The abstraction still explains the 23 artifacts and preserves the core-12 route map. The observed collisions are mostly desirable functional equivalence classes. No new axis is needed, and no existing axis is shown to be fundamentally misguided.

## Why this is not PASS-STABLE

A16 cannot be accepted as a fully legal canonical projection under the frozen global constraint if it is represented faithfully:

    one candidate-indexed C5 joint consequence
    → common resolver
    → final selected action

The current specification admits D4 for joint generation and D2 for candidate consequence selection, but does not explicitly admit their composition when the same C5 carrier is the scored consequence. The first-round workaround (C3+C5) is not acceptable because it duplicates the semantic object.

## Why this is not yet PASS-MINOR-PATCH

The proposed repair is small and introduces no axis, but it changes a global type constraint. Per protocol, that structural patch must wait for human approval rather than being auto-applied in the regression run.

## Findings summary

    23 artifacts projected
    9 PASS
    9 TYPE_CONSTRAINT_ERROR (correctable projection values)
    4 EVIDENCE_REQUIRED
    1 POSSIBLE_COMPOSITION_GAP (A16)
    0 new axes
    0 deleted axes
    0 canonical headline changes

The nine type errors are primarily lifecycle/binding corrections (X=N/A → X=∅ or a stage-qualified binding, and A19 Th=P → Th=A). They do not constitute ontology failure.

## Required next gate

Human review should approve or reject the minimal A16 composition clarification in 06_MINIMAL_AMENDMENT_PROPOSAL.md. If approved, a narrowly scoped normative wording patch can be applied and the A16 projection re-run. If rejected, the ontology must explain why joint candidate consequences are outside D2 rather than silently assigning a false C3 carrier.

No commit or push was performed in this task. Protected paths and the previous D01.2 audit history remain untouched.
