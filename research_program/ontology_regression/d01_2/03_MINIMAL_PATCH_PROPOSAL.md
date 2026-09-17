# D01.2 Minimal Patch Proposal

## Decision

```text
structural patch status: HOLD
new axis: 0
deleted axis: 0
canonical headline signature changes: 0
automatic patch application: forbidden
```

The regression does not require a structural ontology patch. The items below are candidate wording clarifications for a later human-approved maintenance pass; they are not applied in D01.2 and do not change any signature.

## Candidate clarification 1 — joint carrier plus candidate resolver

When an artifact generates joint ego/agent futures and then evaluates multiple identity-preserving samples, the existing notation should be read as a composition:

```text
C={C3,C5}; X=X4; D=D2; P=PB; V=...
```

`C3` is the candidate consequence consumed by the resolver; `C5` records the joint world–action realization. This prevents A16 from being forced into either pure `D4` joint generation or a new “joint candidate” category.

Status: wording clarification only; no axis change.

## Candidate clarification 2 — reciprocal decision boundary

`D3/RR` requires a semantic action-hypothesis → world/consequence → revised-action edge within one decision. Solver steps, denoising steps, autoregressive tokens, or recurrent layers do not qualify by themselves. A19 qualifies because its provisional trajectory is used to predict a future latent that is fed back into the action denoising process.

Status: wording clarification only; no axis change.

## Candidate clarification 3 — training-only carrier and direct policy

The phrase “world model” in a paper title or method name must not create `C@R` or `W≠W0`. If the carrier is deleted, bypassed, or used only as a training environment before deployment, use `C@T`, `D∅`, `W0`, and place the mechanism in ordered `L`.

Status: wording clarification only; no axis change.

## Candidate clarification 4 — unresolved commitment

`PU`, `DU`, `WU`, and `UNKNOWN` are valid evidence boundaries. They must not be silently upgraded to `PB`, `D2`, `RB`, or a concrete resolver semantic merely because a paper says “planning”, “ranking”, or “future-aware”. A10 and A11 are retained as examples.

Status: evidence protocol clarification only; no axis change.

## Why no patch is applied

All four proposals are already expressible by the current ontology's lifecycle, modifier, composition, multi-carrier, ordered-L, and evidence-state rules. Applying them would alter documentation wording, not mechanism semantics. The requested change budget therefore supports a stable verdict, subject to human confirmation of these clarifications.
