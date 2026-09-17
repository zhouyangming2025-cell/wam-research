# Minimal Amendment Proposal

Status: **HOLD — proposal only; no ontology text was modified**

The amendment budget remains:

    new axis = 0
    deleted axis = 0
    canonical headline changes = 0

## Amendment A — candidate-indexed C5 consequence composition

### Problem

The frozen D2 constraint admits C2/C3-like candidate consequences, while A16 provides a candidate-indexed joint world/action consequence C5{k} that is directly scored by a common resolver. Forcing A16 into C3+C5 duplicates one semantic object; forcing it into D4 loses the resolver topology.

### Proposed clarification

Amend D2’s admissibility sentence to:

    D2 accepts a candidate-indexed C2/C3-like consequence or a
    candidate-indexed C5 joint consequence when candidate identity reaches
    one common resolver.

Add the following composition note to the X/D interface:

    A joint-generation birth binding X4 may be followed by a resolver
    binding X3 on the same candidate-indexed carrier. X4 does not itself
    imply PB.

Add the following R/W composition note:

    W5 describes carrier semantics and may coexist with RB when multiple
    candidate-indexed joint futures are resolved before commitment.

### Why this is minimal

- no new code is added;
- no existing code is deleted;
- D4 remains the correct code for single-process world/action emission;
- PB remains the correct code for candidate identity/common resolver;
- D2 remains the correct code for candidate-consequence selection;
- only the admissible composition between existing values is clarified.

## Amendment B — stage-qualified X binding

The schema should state that X binds to a carrier, lifecycle, and stage. This makes the following legal without creating a new axis:

    X4@birth + X3@resolver

It also prevents the recurring error of calling an applicable but unconditioned carrier X=N/A; those cases use X=∅.

## Non-amendments

The following are deliberately not proposed:

- no D6 for “joint generation plus resolver”;
- no new W6 for joint candidates;
- no new P code for A16;
- no new paper-specific type;
- no promotion of C3 and C5 as independent simultaneous carriers in A16;
- no conversion of D01.1 diagnostic fields into a third signature.

## Approval gate

This proposal must remain HOLD until a human reviewer agrees that candidate-indexed C5 is semantically a consequence at the D2 interface. After approval, the proposal may be applied as a normative wording patch and the A16 projection can be promoted from held composition to canonical syntax. The present R1 run does not apply it automatically.
