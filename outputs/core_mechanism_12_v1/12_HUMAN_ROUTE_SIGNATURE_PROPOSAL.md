# Core Mechanism 12 — Human Route Signature Proposal

Status: provisional compression layer for human review. It does not replace the normative audit ontology in `09_ONTOLOGY_SPEC_S1_PLUS.md`.

## 1. Purpose

The audit signature `C–X–D–P–V–T–L` is intentionally loss-aware, but it is too dense to serve as the first view of a paper's idea. This document defines a four-question human route signature:

```text
Artifact = R? + W? + E? ⊕ L[...]
```

It should let a reader recover, in one sentence:

```text
how the output is formed
+ what online world information is actually used
+ what semantic criterion commits the output
+ how world knowledge enters retained deployment computation
```

The layers have different jobs:

```text
human route layer: R–W–E ⊕ L
        ↓ mechanically projected from
audit ontology: C–X–D–P–V–T–L
        ↓ justified by
typed deployment/learning DAG + paper/code evidence
```

The human layer may merge implementation-different artifacts that perform the same semantic function. It must not invent distinctions that exist only because one paper uses RGB, BEV, latent tokens, Transformer, diffusion, or flow.

## 2. Classification unit and syntax

The classification unit remains an artifact rather than a paper title:

```text
Artifact = paper/code version × task mode × planning/generation path
```

Canonical syntax:

```text
Artifact@version/mode
  = R... + W... + E... ⊕ L[ordered learning route; deployment fate]
```

Example:

```text
WorldDrive@planning
= RB + W3 + EV
  ⊕ L[LP → joint(LT,LC) → retain{surrogate,scorer}/drop{heavy generator}]
```

`R`, `W`, and `E` each have one primary value. `E` may contain a typed composition. `L` may contain an ordered or parallel expression because learning routes are not generally reducible to one unordered label.

## 3. R — output formation and commitment route

Research question:

> How is the terminal output formed and, when alternatives exist, committed?

| Code | Human meaning | Required audited topology |
|---|---|---|
| `R0` | direct or implicit action | `P∅`, ending in one action path; `W` separately says whether an online carrier conditions it |
| `RH` | semantic decision/intent then action | `PH`: an independently meaningful intent/decision precedes action formation |
| `RB` | explicit candidate bank then resolver | `PB`: candidate birth → identity preservation → common resolver → `A*` |
| `RR` | world and policy revise one another before commitment | `D3` and `Tr=present` |
| `RJ` | one joint world–action process emits both | `D4`, `C5`, and `X4` |
| `RG` | world/consequence generation is the terminal mode output | `D5`; use modifier `control=self`, `external`, or `UNKNOWN` when it changes the mode |
| `RU` | final action commitment is unresolved | `PU` or equivalent evidence boundary |

Projection priority is causal:

```text
D4 → RJ
D5 → RG
D3 → RR
otherwise PB → RB
otherwise PH → RH
otherwise P∅ → R0
otherwise PU → RU
```

This intentionally merges audit distinctions that do not alter semantic commitment. A top-K prefilter or a post-selection refinement without rescore remains an audit attribute, not a new R class.

## 4. W — primary online world role

Research question:

> What qualifying world state or consequence is actually on the deployed causal path to the terminal output?

| Code | Human meaning | Audit source |
|---|---|---|
| `W0` | no qualifying online world carrier | no `C@R` ancestor of the terminal output |
| `W1` | current structured world state | runtime `C1` through `D1` or another declared output route |
| `W2` | internal future-generative state | runtime `C4`, normally through `D1` |
| `W3` | future endpoint consequence | runtime `C2` used by the output route |
| `W4` | future-horizon consequence sequence | runtime `C3`; `Th` normally present when it is a physical future sequence |
| `W5` | joint world–action carrier | runtime `C5` through `D4` |
| `WU` | online world role cannot be determined | runtime carrier identity or ancestry unresolved |

Only carriers that pass the four-part gate in `09_ONTOLOGY_SPEC_S1_PLUS.md` may enter W. Ordinary encoder features, BEV perception features, or map/detection states do not become `W1` merely because planning consumes them.

When several runtime carriers exist, W records the most downstream world object that explains the decision route:

```text
joint world–action carrier
> future horizon
> future endpoint
> future-generative internal state
> current structured world state
```

Earlier supporting carriers remain in the audit record. For example, World4Drive retains `C1+C2` below the compression layer but projects to `W3` because the candidate future endpoint is the decisive online consequence.

Training-only future carriers never enter W. They are represented through L, so:

```text
train-time future prediction + runtime direct policy = W0
```

Representation substrate and direct-versus-surrogate implementation are not W categories. Teacher/surrogate distinctions remain in L.

## 5. E — semantic decision criterion

Research question:

> If alternatives are resolved, what semantic target makes one preferable?

| Code | Human meaning | Audit source |
|---|---|---|
| `E0` | no resolver criterion in this route | `V=N/A` because no resolver/commitment task exists |
| `EF` | expert or factual behavior compatibility | `VM` |
| `EV` | holistic planning value, utility, or preference | `VU` |
| `ED` | decomposed driving outcomes or reward components | `VD` |
| `EW` | world/future fidelity or agreement | `VW` |
| `EY` | dynamics or physical validity | `VY` |
| `EP` | model confidence or likelihood | `VP` |
| `EØ` | resolver is known, but no evaluative criterion is evidenced | `V∅` |
| `E?` | resolver applicability or criterion remains unresolved | `UNKNOWN` or `VX`, with the exact boundary retained below |

Composition is preserved when it changes the idea:

```text
EF + ED       imitation plus decomposed driving outcomes
ED → EV       decomposed outcomes aggregated into holistic utility
weighted(EV,ED)
```

Measures and architectures are not E categories. Latent MSE, ADE, cross entropy, a scalar head, and vector dimensionality are evidence about implementation or measurement, not semantic target identity.

## 6. L — human-readable learning route

Research question:

> Through what directed learning program does world knowledge alter retained deployment computation?

The human layer reuses the audited L macros instead of inventing a second learning alphabet:

| Code | Plain-language role |
|---|---|
| `LA` | predicted action conditions a world/future branch whose loss reaches the action path |
| `LS` | sibling world and policy objectives share state or parameters |
| `LP` | predictive/generative pretraining transfers a representation or backbone |
| `LG` | generative-carrier pretraining is adapted while the carrier-producing trunk remains online |
| `LN` | factual next-state/temporal consistency uses an explicit stopped target |
| `LT` | a heavy consequence teacher trains a deployed surrogate |
| `LC` | a world/simulator-derived criterion trains a proposal, label, reward, or scorer |
| `LQ` | world and action are learned as one shared sequence/carrier |
| `LR` | reward-based policy optimization |
| `LU` | learning route unresolved |

Required grammar:

```text
sequence: A → B
parallel: joint(A,B)
deployment fate: retain{...}/drop{...}/bypass{...}
uncertain edge: ?
```

The expression should contain only distinctions needed to explain the route family. The full gradient scopes, detach boundaries, stage-specific targets, and parameter sets remain authoritative in the audit DAG.

## 7. Mechanical projection algorithm

For every artifact:

1. Freeze the same artifact/version/mode boundary used by the audit record.
2. Assign R using the D/P priority rule in §3.
3. Trace runtime `C` ancestors only; assign the primary W using §4 and retain supporting carriers as notes.
4. Map V semantic atoms and their composition to E; do not infer E from head shape or loss name.
5. Normalize the ordered L macro route and retain/drop fate; preserve `UNKNOWN` edges.
6. Apply the type constraints below.
7. Write one plain-language mechanism sentence from the signature.
8. Compare the sentence against the canonical deployment and learning DAG. If the sentence is materially false, the compression fails even if the code is syntactically legal.

The projection is one-way:

```text
C–X–D–P–V–T–L → R–W–E ⊕ L
```

The human signature is not expected to reconstruct every X binding or clock. Those are deliberate audit-layer losses.

## 8. Compression-layer type constraints

1. `RB` requires a common resolver and normally requires `E≠E0`; use `E?` rather than inventing a criterion.
2. `R0` and `RH` normally require `E0` because no separate resolver is present.
3. `RR` may coexist with `E?` when reciprocal refinement is known but final commitment is unresolved.
4. `RJ` requires `W5`.
5. `RG` requires an online world/consequence output and normally uses `E0`; record self/external control when mode identity depends on it.
6. `W3` or `W4` with `RB` requires candidate-preserving `X3` in the audit record.
7. `W0` does not forbid `RB`: a train-time world criterion may be compressed into a deployed scorer, as in Drive-JEPA PB or DynFlowDrive.
8. A training-only carrier cannot justify `W1–W5`.
9. Supporting `C1` states may be omitted from primary W only when a later consequence carrier dominates the same route; they remain mandatory below the compression layer.
10. Audit `UNKNOWN` may project only to an honest known coarse class or to `RU/WU/E?`; it may never become verified absence.
11. Solver, reciprocal, horizon, and cross-cycle clocks are not silently conflated. R/W preserve `Tr` and `Th` when route-defining; `Ts` and `Tc` remain audit fields unless they change R, W, or E semantics.
12. Identical human signatures assert only functional route-family equivalence, not code identity or full typed-DAG isomorphism.

## 9. Equivalence levels after compression

```text
human-runtime-equivalent
= equal R + W + E

human-mechanism-family-equivalent
= equal R + W + E + normalized L route/fate

audit-runtime-equivalent
= equal runtime C/X/D/P/V/T

core-mechanism-equivalent
= typed deployment and learning DAGs are isomorphic after implementation renaming
```

The human layer is allowed to declare LAW and Metis mechanism-family-equivalent at its chosen semantic granularity while the audit layer records their non-isomorphic latent/video-expert implementations and solver details.

## 10. First-six canonical human signatures

```text
LAW-PF
= R0 + W0 + E0
  ⊕ L[LA → retain{planner}/drop{future branch}]
```

Direct planning; a predicted action is regularized through a train-time future loss, and the future branch is removed at deployment.

```text
EPO-PLAN
= R0 + W0 + E0
  ⊕ L[LS + detached-chain curriculum → retain{planner}/bypass{visual generator}]
```

Direct planning; world and policy objectives share state during training, including detached chain curriculum, but planning does not consume an online future carrier.

```text
DLAW-PAPER/CODE
= R0 + W2 + E0
  ⊕ L[LG → retain{future-generative trunk,action head}/skip{full video decode}]
```

Direct planning conditioned by an online internal future-generative state.

```text
W4D-PLAN
= RB + W3 + EW
  ⊕ L[joint(LC[future agreement],LA?) → retain{candidate future path,scorer}]
```

Candidate endpoint futures are compared through factual-future world agreement and the resolver commits one candidate.

```text
WD-PLAN
= RB + W3 + EV
  ⊕ L[LP → joint(LT,LC) → retain{surrogate,scorer}/drop{heavy generator}]
```

A distilled endpoint surrogate evaluates candidates according to holistic planning preference.

```text
WOTE-PLAN
= RB + W4 + (EF+ED)
  ⊕ L[joint(LC,world losses) → retain{future rollout,reward,resolver}]
```

Each candidate receives a future-horizon rollout and is resolved by imitation plus decomposed planning outcomes.

## 11. Deliberate information loss

The human signature deliberately omits:

- exact X binding except where self/external generation control defines the mode;
- supporting carriers before the primary online world object;
- solver clock `Ts` and cross-cycle clock `Tc` unless they change route/criterion semantics;
- candidate count, solver steps, horizon length, and prefilter/post-refine attributes;
- representation substrate and neural architecture;
- full gradient scopes and detach/freeze details.

These omissions are acceptable only because every signature links back to the complete audit record. `R–W–E ⊕ L` must never be used as the sole evidence ledger.

## 12. Acceptance gate

The proposal may become the primary route map only if all of the following pass:

- all 21 frozen artifacts project without paper-specific categories;
- every row yields one accurate plain-language sentence;
- expected functional equivalents collide and genuinely different route families do not;
- the first six pass human inspection;
- implementation substitutions leave the signature invariant;
- a later unseen paper is classified without changing the codebook;
- the detailed audit remains the normative dispute resolver.

Until that gate closes, this document is a provisional presentation layer, not a replacement ontology and not evidence for S2 promotion.
