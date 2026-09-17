# Core Mechanism 12 — Normative Ontology Specification S1+

Status: current normative specification after 21-artifact projection, counterexample audit, and first-six human review.

This file supersedes `02_ONTOLOGY_SPEC.md` for new classifications. The Phase 2 file remains unchanged as an evolution record.

## 1. Classification unit

Classify an artifact, not a paper title:

```text
Artifact = paper/code version × task mode × planning/generation path
```

Examples that must remain separate include SeerDrive paper/code, DriveLaW paper/code, Epona planning/self-rollout/external-control, and Drive-JEPA PF/PB modes.

Normative signature:

```text
Artifact@version/mode
  C = carrier records
  X = control interface bound to each carrier, lifecycle, and when needed training stage
  D = runtime carrier-to-output causal route
  P = action formation and commitment topology
  V = resolver criterion record
  T = online clock topology
  L = ordered and directed learning-to-deployment program
```

The compact signature is an index. The evidence boundary and canonical DAG are part of the mechanism record.

## 2. Evidence values

Use three distinct states:

```text
∅        verified absence inside the scoped artifact
N/A      field is inapplicable by task/type
UNKNOWN  available evidence cannot determine the value or applicability
```

Do not convert missing evidence into ∅. Do not use N/A merely because implementation details are unavailable.

## 3. Common world-carrier gate

A state qualifies as C only if all four conditions hold:

1. Localizable identity: a separately traceable state exists.
2. Stateful world operation: it participates in transition, temporal prediction/consistency, temporally identified relational update, generative dynamics, or world-state transport beyond ordinary encoding.
3. Carrier-level grounding: supervision or teacher evidence targets the state's world/temporal semantics; a loss merely attached to a shared feature is insufficient.
4. Mechanism interface: the state reaches planning/output, or its loss/criterion updates a deployed planning component.

Hard negative:

```text
detection/map supervision + planner consumption
without a stateful world operation
= ordinary perception state, not C1
```

## 4. C — world/consequence carrier semantics

Research question: what qualifying world/consequence object exists, and in which lifecycle?

| Code | Meaning |
|---|---|
| C1 | current structured world state |
| C2 | future endpoint consequence |
| C3 | future-horizon consequence sequence |
| C4 | internal future-generative process state |
| C5 | joint world–action sequence/carrier |
| C∅ | no qualifying carrier in the scoped lifecycle |
| CU | carrier type unknown |

Modifiers:

```text
life        = @T train-only | @R runtime-only | @B both | @U unknown
realization = direct | surrogate | generative_internal | unknown
```

`C5` may be candidate-indexed as `C5[k]` when each jointly born world–action sample retains its candidate identity through a downstream resolver. The key identifies the joint carrier; it does not by itself imply an action-conditioned input.

Multiple semantically distinct carriers require multiple records. Representation substrate—RGB, BEV, latent, token, hidden state—does not change C.

## 5. X — carrier control/branching interface

Research question: what action/control variable indexes each consequence or joint carrier?

| Code | Meaning |
|---|---|
| X∅ | no action/control conditions this applicable carrier |
| X1 | factual, supplied, or external control |
| X2 | one policy-predicted control |
| X3 | candidate-preserving control keyed by k |
| X4 | joint/interleaved world–action variables |
| XU | control edge unknown |
| N/A | carrier type is not action/control-indexable in this lifecycle |

Normative syntax:

```text
X(carrier-id@life{realization}, stage?) = value
```

Lifecycle shorthand is allowed only when it identifies exactly one carrier. If C1 and C2 are both `@B`, `@B:X3` is invalid because it does not identify which carrier is candidate-controlled.

Stage may be omitted only when the incoming control type is constant throughout that lifecycle. If a teacher uses factual control in pretraining and candidate control during scorer/distillation training, both edges must be recorded.

A route command that conditions only the policy is not X.

## 6. D — deployment carrier-to-output causal route

Research question: how does a runtime carrier causally affect the declared terminal output?

| Code | Required route |
|---|---|
| D∅ | no runtime C carrier influences A* |
| D1 | runtime carrier → one policy/action path → A* |
| D2 | candidate consequence → resolver → A*; see the two admissible forms below |
| D3 | action → consequence → revised action, repeated within one decision before commitment |
| D4 | one joint world–action generation/editing process directly emits the committed world/action output |
| D5 | consequence generation is the terminal mode output; A* may be N/A |
| DU | route unknown |

Internal network depth, denoising iterations, and physical-time rollout do not by themselves create D3.

For candidate resolution, D2 has two legal forms:

```text
A{k} → C2/C3{k} → V{k} → resolver → A*

C5{k} = (world{k}, action{k}) → V{k} → resolver → A*
```

The first form is an action-conditioned consequence and normally uses `X3` on the candidate consequence. The second form is a jointly born candidate and uses `X4` on `C5{k}`. If multiple joint candidates enter a common resolver, the final route is `D2`, not `D4`. `D4` is reserved for direct joint emission without a downstream common resolver. No additional D code is introduced.

## 7. P — action formation and commitment topology

Research question: how is action semantically formed and, if alternatives exist, committed?

| Code | Required topology |
|---|---|
| P∅ | direct/implicit action formation; no independently semantic intermediate and no explicit bank/resolver |
| PH | context → independently semantic decision/intent → action |
| PB | identity-preserving candidate bank → common resolver → A* |
| PU | multimodal/action outputs exist but final commitment topology is unresolved |
| N/A | generation-only/external-control mode has no action-commitment task |

PB admission requires all four:

```text
candidate birth
→ identity preservation
→ common resolver
→ resolver determines A*
```

Random samples, solver states, token-edit iterations, hidden queries, or WTA training labels are not PB without this chain.

Attributes such as `prefilter`, `postselect_refine`, `rescore`, and `candidate_count` remain non-core unless they introduce another commitment stage or change resolver semantics.

## 8. V — resolver criterion semantics

Research question: when a resolver exists, what semantic target determines preference among alternatives?

Semantic atoms:

| Code | Meaning |
|---|---|
| VM | expert/factual behavior compatibility |
| VU | holistic planning utility or preference |
| VD | decomposed driving outcomes such as safety, comfort, progress, or rule compliance |
| VW | world/future fidelity or predictive agreement |
| VY | dynamics or physical validity |
| VP | model confidence or likelihood |
| VX | resolver is known to exist, but criterion semantics are unknown |
| V∅ | resolver exists, but no evaluative criterion is evidenced |
| N/A | no resolver by task/topology |
| UNKNOWN | resolver applicability and/or criterion cannot be established |

Every nontrivial V record contains:

```text
composition(
  semantic atoms;
  compared objects;
  target provenance;
  measure;
  weights/order/filter
)
```

Geometric distance is a measure, not a semantic atom. Previous-cycle reference is temporal provenance and may also imply Tc; it is not a semantic atom.

Example:

```text
World4Drive V = single(VW;
  compared=predicted F{k}, factual F_hat;
  measure=latent MSE;
  target=j=argmin distance)
```

## 9. T — online clock topology

Research question: which kinds of online progression exist?

```text
T = (Ts, Tr, Th, Tc)
each value ∈ {absent, present, UNKNOWN}
```

| Field | Meaning |
|---|---|
| Ts | numerical solver, denoising, flow, or token-edit coordinate |
| Tr | reciprocal world↔policy update within one decision |
| Th | modelled physical-future horizon progression |
| Tc | dependency across real control cycles |

Counts are audit parameters:

```text
solver_steps
refinement_rounds
model_horizon_steps
previous_cycle_lag
```

Changing 5 to 10 solver steps does not change core T. Changing endpoint prediction to a recurrent physical horizon changes C and Th.

## 10. L — directed learning-to-deployment program

Research question: through what staged, directed program does world information alter retained deployed computation?

Normative operators:

```text
stage sequence     A → B
parallel objectives A || B
directed edge      source → operation/loss → parameter scope
boundary           stopgrad | detach | freeze | EMA | UNKNOWN
deployment         retain{...} / drop{...} / bypass{...}
```

Reusable family macros:

| Code | Meaning |
|---|---|
| LP | predictive/generative representation pretraining followed by encoder/backbone transfer |
| LS | sibling world and policy objectives coupled through shared state/parameters |
| LA | predicted action conditions a future/world branch whose loss reaches the action-producing path |
| LG | generative-carrier pretraining followed by retained online trunk adaptation |
| LN | factual next-state/temporal consistency with explicit stopped target |
| LT | heavy teacher consequence → deployed surrogate distillation |
| LC | world/simulator criterion → proposal, label, reward, or runtime scorer supervision |
| LQ | shared world–action sequence learning |
| LR | reward-based policy optimization |
| LU | learning route unresolved |

Macros are indices, not substitutes for the canonical program.

Example:

```text
WorldDrive:
pretrain TA-DWM
→ transfer/freeze visual+motion encoders and train planner (LP)
→ joint FAR train [teacher alignment (LT) || PDMS ranking (LC)]
→ retain{encoders,planner,surrogate,reward}/drop{heavy generator}
```

## 11. Global type constraints

1. D2 requires either (a) a runtime C2/C3 candidate consequence with X3 on that carrier, or (b) a candidate-indexed runtime C5 joint consequence with X4 on that carrier; both forms require identity preservation, PB, a non-N/A V, and a declared A*.
2. D3 requires action→carrier and carrier→action edges plus Tr=present.
3. D4 requires C5 and X4 when one joint process directly emits the committed world/action output; if multiple C5 candidates enter a common resolver, use D2 instead.
4. D5 permits A*=N/A and normally uses P=N/A for generation-only modes.
5. A train-only carrier cannot support D1–D4.
6. PB may exist without a runtime world carrier; then D may be D∅ and V still applies.
7. P∅, PH, or N/A implies V=N/A unless a separate explicit resolver is represented.
8. PU implies V=UNKNOWN when resolver applicability is unresolved; VX requires a known resolver.
9. X must be bound to carrier, lifecycle, and when needed training stage; C1 current state normally has X=N/A.
10. Th does not imply Tr or Tc.
11. Ts does not imply physical-future rollout.
12. L cannot be inferred from D.
13. A dropped/bypassed node cannot appear in the runtime causal path.
14. D1 requires a C@R ancestor of A* and excludes the D2 candidate-consequence pattern.
15. PB requires a declared A*.
16. Every ∅ requires positive scoped absence evidence; otherwise use UNKNOWN.

## 12. Classification algorithm

For each artifact:

1. Freeze paper/code commit, mode, terminal output, and evidence boundary.
2. Draw separate deployment and learning DAGs.
3. Apply the four-part carrier gate to every candidate state.
4. Create all C records with lifecycle and realization.
5. Bind X separately to every applicable carrier record and split by stage when control provenance changes within one lifecycle.
6. Trace only runtime C ancestors to assign D.
7. Determine action formation/commitment and apply the PB gate to assign P.
8. If a resolver exists, reconstruct V from supervision provenance and compared objects—not from the scalar head's shape or paper terminology.
9. Separate Ts, Tr, Th, and Tc; move numerical counts to attributes.
10. Write the full staged L program with directed gradients and retain/drop boundaries.
11. Apply all type constraints.
12. Compare the resulting DAG against nearest artifacts and run implementation-invariance substitutions.

## 13. Equivalence relations

```text
runtime-equivalent
= equal runtime C/X/D/P/V/T after erasing noncausal audit parameters

mechanism-family-equivalent
= runtime-equivalent + same ordered/parallel L macro structure

core-mechanism-equivalent
= typed deployment and learning DAGs are isomorphic after implementation renaming
   and removal of noncausal numerical parameters
```

A compact-signature collision establishes at most the first two levels. Full core equivalence requires DAG comparison.

## 14. Corrected first-six canonical planning signatures

These are teaching compressions; the detailed artifact records remain authoritative.

```text
LAW-PF
C[C2@T] · X[C2@T:X2] · D∅ · P∅ · V[N/A]
· T[all absent] · L[LA; future branch dropped]

EPO-PLAN
C[C2@T base,C3@T chain]
· X[C2@T,base:X1; C3@T,chain:X2] · D∅ · P∅ · V[N/A]
· T[Ts] · L[LS+detached-chain; visual branch bypassed]

DLAW-PAPER/CODE
C[C4@B internal] · X[C4@T:X∅; C4@R:X∅] · D1 · P∅ · V[N/A]
· T[Ts] · L[LG; generative trunk retained]

W4D-PLAN
C[C1@B,C2@B] · X[C1:N/A,C2:X3] · D2 · PB
· V[VW factual-future latent agreement] · T[all absent]
· L[retained joint graph; LA reach partly UNKNOWN]

WD-PLAN
C[C2@T direct,C2@R surrogate]
· X[C2@T,pretrain:X1; C2@T,FAR:X3; C2@R:X3] · D2 · PB{prefilter}
· V[VU PDMS preference] · T[all absent]
· L[LP→joint(LT,LC); heavy generator dropped]

WOTE-PLAN
C[C1@B,C3@B] · X[C1:N/A,C3:X3] · D2 · PB
· V[fusion(VM,VD)] · T[Th]
· L[retained joint world/reward graph + LC]
```

## 15. Stability boundary

Current level: provisional S1+.

Not S2 because:

- SEER-PAPER and GW-PLAN final commitment remain UNKNOWN;
- four recent papers lack executable source verification;
- several detach/gradient edges remain unresolved;
- no blind independent-reader classification of a new external paper has yet passed.

The next paper must be classified from this file without consulting paper-specific categories. If it forces a new category, first test whether the current research question is malformed before extending the code list.
