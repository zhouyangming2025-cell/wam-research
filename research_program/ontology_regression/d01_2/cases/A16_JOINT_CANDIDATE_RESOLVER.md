# Pressure Case A16 — Joint Futures with a Common Resolver

## Boundary question

Does generating joint ego/agent futures force the artifact into `D4` joint generation, even when multiple samples retain identity and are ranked by a common evaluator?

## Closed-set projection

```text
C={C3@R,C5@R}
X=X4
D=D2
P=PB
V=VU
RB+W4+EV{joint-generation modifier}
```

`C3` is the candidate consequence used by the resolver; `C5` records the joint realization. The common resolver, not the internal generative architecture, determines the primary decision topology.

## Result

Existing multi-carrier and composition rules express the case. `D4` would be wrong because the selected candidate is committed after a common resolver.

```text
disposition: CLARIFY
patch: wording only, not applied
```
