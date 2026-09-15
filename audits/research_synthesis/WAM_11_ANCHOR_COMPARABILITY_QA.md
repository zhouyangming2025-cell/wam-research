# WAM 11-Anchor Comparability QA

Last updated: 2026-09-15

Status: **COMPARABILITY GATE — precondition for any research-gap declaration**

Anchors:

```text
LAW | WoTE | Epona | WorldDrive | World4Drive | SeerDrive
Drive-JEPA | Metis | DynFlowDrive | Discrete-WAM | GraphWorld
```

Purpose:

> Determine which apparent disagreements are genuine scientific contrasts and which are artifacts of different planning interfaces, target truth, deployment lifecycles, temporal semantics, or evaluation regimes.

---

# 1. Comparability rule

Two papers are directly comparable only if the claim being compared is aligned on at least these dimensions:

```text
A. planning role of world knowledge
B. predicted / learned world object
C. future-target provenance
D. deployment graph
E. temporal horizon semantics
F. evaluation regime
G. supervision/value source
```

If one or more differ materially, the result may still be informative, but must be labeled:

```text
CROSS-FAMILY CONTROL
```

rather than a clean head-to-head mechanism test.

---

# 2. High-confidence directly comparable groups

## Group 2.1 — Training-time future/world shaping without mandatory online future

Anchors:

```text
LAW
Drive-JEPA
Epona [future visual branch optional]
Metis
Discrete-WAM
```

Comparable question:

> Can predictive/world objectives improve planning even when predicted future output is not required at deployment?

Useful contrasts:

```text
LAW          auxiliary future latent loss
Drive-JEPA   predictive representation pretraining
Epona        shared world/trajectory representation
Metis        asymmetric action→world co-training
Discrete-WAM shared world/policy backbone
```

Not directly comparable on:

```text
future target geometry
parameter sharing
planning decoder
benchmark scale
```

So the valid synthesis is qualitative:

```text
multiple architectures support training-time future/world knowledge transfer without mandatory online future inference.
```

Invalid synthesis:

```text
method X proves auxiliary world loss is superior to method Y's joint world model
```

because the mechanisms and training budgets differ.

---

## Group 2.2 — Online future-aware candidate/mode selection

Anchors:

```text
WorldDrive
World4Drive
WoTE
```

Shared property:

```text
predicted/derived future information is on the deployed action-selection path
```

Comparable scientific questions:

```text
Does online future information improve ranking/selection?
How explicit is the decision/value layer?
How deep is the future model?
```

Key differences:

```text
WorldDrive   lightweight distilled future + ranking
World4Drive  compact future latent + factual-mode matching
WoTE         recurrent future sequence + explicit utility
```

Therefore they are directly comparable on:

```text
online future dependence
future depth
selection semantics
value explicitness
```

but not on raw benchmark score without matched data/model controls.

---

## Group 2.3 — Candidate-conditioned world model used only during training

Anchors:

```text
DynFlowDrive
[WorldDrive teacher stage as a partial control]
```

Comparable question:

> Can candidate-conditioned consequence knowledge be compressed into a cheaper deployed decision module?

Difference:

```text
DynFlowDrive removes WM entirely
WorldDrive retains a lightweight distilled future surrogate
```

This is a clean lifecycle contrast.

---

## Group 2.4 — Direct policy conditioning by world representation

Anchors:

```text
Epona
GraphWorld
```

Shared property:

```text
world/history representation directly feeds trajectory generation without explicit consequence utility
```

Difference:

```text
Epona      shared multimodal historical latent F
GraphWorld online structured/refined interaction state W
```

Comparable on:

```text
representation dependence
world→policy forward interface
shared-state semantics
```

Not directly comparable on:

```text
explicit future transition depth
representation substrate
long-horizon evaluation
```

---

## Group 2.5 — Internal world/planner interaction without environmental reactivity

Anchors:

```text
SeerDrive
GraphWorld [single/short latent refinement]
```

Comparable question:

> Does internal planner↔world feature interaction help planning?

But:

```text
SeerDrive = iterative hidden co-refinement
GraphWorld = flow-refined W then direct planner conditioning
```

Neither mechanism by itself establishes ego↔environment reactive closed-loop world dynamics.

---

# 3. Strong cross-family controls

These pairs are scientifically useful precisely because they differ in mechanism.

## WoTE vs GraphWorld

```text
WoTE:
candidate → recurrent consequence → explicit utility → select

GraphWorld:
interaction/history → refined W → direct policy
```

Use this pair to separate:

```text
explicit consequence modeling
vs
compact decision-relevant representation conditioning
```

Do not compare as a single `which world model is better` question.

---

## Epona vs Metis

```text
Epona:
shared F feeds trajectory + visual branches

Metis:
action representation conditions world generation;
world loss shapes action expert backward
```

Use this pair to separate:

```text
shared representation coupling
vs
asymmetric gradient coupling
```

---

## Metis vs Discrete-WAM

Both can deploy action-only despite world-policy co-training.

Use this pair to test:

```text
training-time jointness
vs
deployment-time world dependence
```

Do not infer that stronger parameter sharing implies stronger online model-based planning.

---

## DynFlowDrive vs World4Drive

Both involve candidate/mode-conditioned future latent reasoning.

Lifecycle contrast:

```text
DynFlowDrive: world machinery removed after score supervision
World4Drive: future predictor retained online
```

This is a strong control for:

```text
teacher-only consequence knowledge
vs
online future computation
```

---

## LAW vs GraphWorld

Both can be described as `future-aware representation` approaches, but the deployment role differs:

```text
LAW        future knowledge shapes representation during training only
GraphWorld compact W is actively consumed online
```

Useful for distinguishing:

```text
training-time future awareness
vs
online world-state dependence
```

---

# 4. Comparisons that are usually invalid or misleading

## Invalid 4.1 — Compare raw world fidelity across unlike substrates

Bad:

```text
FID/FVD of video model
vs
BEV error
vs
latent flow loss
vs
graph-state consistency
```

Reason:

```text
metrics do not measure the same world object.
```

Valid alternative:

```text
within-paper fidelity/representation ablation → planning change
```

if matched.

---

## Invalid 4.2 — Rank `counterfactuality` by number of predicted branches

Bad:

```text
K futures > 1 future therefore more counterfactual
```

Must separate:

```text
candidate-specific output
candidate-specific truth
reactive other-agent truth
intervention validation
```

World4Drive, SeerDrive, DynFlowDrive and Discrete-WAM all demonstrate why branch multiplicity is insufficient.

---

## Invalid 4.3 — Treat NAVSIM as reactive environmental closed loop

Correct project label:

```text
NAVSIM = non-reactive data-driven / pseudo-simulation planning
```

Therefore NAVSIM cannot establish:

```text
reactive other-agent causal response to ego interventions
```

even when authors use `closed-loop` informally.

---

## Invalid 4.4 — Treat visual autoregressive rollout as policy-environment closed loop

Epona long video rollout proves:

```text
self-conditioned generative temporal rollout
```

not necessarily:

```text
reactive driving policy competence
```

---

## Invalid 4.5 — Compare solver/edit/refinement steps as physical horizon

Examples:

```text
DynFlowDrive rectified-flow s
GraphWorld flow coordinate
Discrete-WAM token-edit rounds
SeerDrive planner/world refinement iterations
Epona diffusion steps
```

These are not physical scene time.

---

## Invalid 4.6 — Equate collision reduction with explicit risk modeling

GraphWorld is the clearest negative control:

```text
strong collision reduction
without explicit risk state / field / utility head
```

Therefore later risk-aware claims require explicit additional evidence.

---

# 5. Evaluation-regime comparability

## Level E0 — same benchmark, same split, closely matched implementation

Strongest practical comparison.

Examples include within-paper ablations and same-backbone module toggles.

Use for mechanism attribution when available.

## Level E1 — same benchmark, different implementation/model/training

Useful for broad capability context.

Examples:

```text
NAVSIM leaderboard-style comparisons
nuScenes planning tables
```

Do not use as primary causal evidence.

## Level E2 — different benchmark, same claimed mechanism

Useful for robustness/generalization evidence only.

Cannot identify which architectural element caused score differences.

## Level E3 — different evaluation regimes

Examples:

```text
nuScenes open loop
vs
NAVSIM pseudo-simulation
vs
Bench2Drive reactive CARLA
vs
visual rollout
```

These are not numerically comparable.

They support different classes of claims.

---

# 6. Strongest matched control per anchor

| Anchor | Strongest matched/internal control | What it supports | What it does not isolate |
|---|---|---|---|
| LAW | ± future-latent auxiliary | predictive auxiliary helps planning representation | specific physical meaning of latent future |
| WoTE | evaluator no future → + predicted future | future consequence improves online evaluation | reactive counterfactual validity |
| Epona | trajectory-only → joint visual+trajectory | visual/world auxiliary branch helps planning | which aspect of visual prediction causes gain |
| WorldDrive | trajectory-feature rewarder → + distilled future feature | online future feature adds ranking value | heavy teacher/foundation prior contribution completely |
| World4Drive | matched priors/intentions without WM → + WM | compact future latent helps selection | alternative-action truth validity |
| SeerDrive | future-aware × iterative 2×2 | future branch and internal refinement both contribute | environmental closed-loop reactivity |
| Drive-JEPA | representation pretraining / planner proposal-selection decompositions | predictive pretraining and selection design matter | pure causal dynamics learning |
| Metis | no video co-train→video co-train; joint/isolated/asymmetric | world co-training and information-flow design matter | future-video fidelity→planning relation |
| DynFlowDrive | static WM→flow WM; score-factor decomposition | flow teacher and selection factors help | physical-time latent dynamics correctness |
| Discrete-WAM | scratch/FT/pretrain + decision/RL controls | decision prior/post-training and world-oriented pretraining contribute | full joint world-policy gain as one clean factor |
| GraphWorld | baseline→ECIG→WSCP; Stage I→II; diffusion→flow; dense→ego-star | interaction structure + world-state conditioning bundle drives gain | independent world-state fidelity→planning causality |

---

# 7. Comparability verdict by major question

## Q1. Does future/world knowledge help planning at all?

```text
YES across multiple matched within-paper controls.
```

Evidence is broad but mechanism-heterogeneous.

## Q2. Must a future world be generated online?

```text
NO.
```

Controls:

```text
LAW, Drive-JEPA, Epona planning-only, Metis, DynFlowDrive, Discrete-WAM
```

## Q3. Is online future modeling sufficient to imply explicit model-based selection?

```text
NO.
```

Controls:

```text
GraphWorld, SeerDrive
```

## Q4. Do multiple future branches establish counterfactual truth?

```text
NO.
```

Current anchor set lacks strong reactive intervention-validity evidence.

## Q5. Does stronger world-generation fidelity imply better planning?

```text
NOT ESTABLISHED across the anchor set.
```

Most papers do not provide a clean monotonic matched fidelity→planning experiment.

## Q6. Does stronger training-time unification imply stronger online model-basedness?

```text
NO.
```

Metis / Discrete-WAM vs WoTE / World4Drive are decisive controls.

## Q7. Does long-horizon planning require long-horizon world rollout?

```text
NO.
```

GraphWorld is the key negative control.

---

# 8. QA stop condition result

The eleven-anchor set is now normalized enough to support **scientific tension extraction**, provided every later claim preserves:

```text
mechanism family
future truth
lifecycle
source certainty
evaluation regime
```

This QA does **not** by itself authorize final research-gap declaration or method design.
