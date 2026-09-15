# WAM Comparison Matrix V1.3 — DynFlowDrive Extension

Last updated: 2026-09-15

Status: **NINE-ANCHOR EXTENSION — ONTOLOGY V1.3 ACTIVE**

Coordinate system:

```text
WAM_DIMENSION_ONTOLOGY_V1.md
+ WAM_DIMENSION_ONTOLOGY_V1_1_AMENDMENT.md
+ WAM_DIMENSION_ONTOLOGY_V1_2_AMENDMENT.md
+ WAM_DIMENSION_ONTOLOGY_V1_3_AMENDMENT.md
```

Anchors:

```text
LAW | WoTE | Epona | WorldDrive | World4Drive | SeerDrive | Drive-JEPA | Metis | DynFlowDrive
```

---

# 1. Future/world knowledge lifecycle

| Paper | Training-time world mechanism | Future/world object required for deployed action selection? | Deployed decision mechanism |
|---|---|---:|---|
| LAW | action-aware factual future-latent auxiliary prediction | NO | direct waypoint policy |
| WoTE | recurrent candidate-conditioned future BEV + reward learning | YES | future BEV → explicit utility → argmax |
| Epona | shared-latent trajectory + visual generation | visual future NO for planning | direct generative trajectory policy |
| WorldDrive | heavy generative teacher + future-feature distillation | YES, lightweight distilled future | future-aware reranking |
| World4Drive | candidate/intention-conditioned endpoint future latent | YES | future mode → ScoreNet → select |
| SeerDrive | future-BEV ↔ planner-feature internal co-refinement | YES | iterative future-aware planner |
| Drive-JEPA | masked-video predictive pretraining | NO | proposal/refinement/scorer policy |
| Metis | action-conditioned future-video co-training | NO | direct action-flow policy |
| **DynFlowDrive** | **candidate-conditioned flow dynamics + world-derived positive-mode teacher** | **NO** | **candidate score head → argmax** |

DynFlowDrive adds a useful lifecycle combination:

```text
explicit candidate consequence model during training
→ consequence-derived ranking labels
→ consequence model fully removed
→ only learned score behavior survives
```

---

# 2. F08 — internal transition coordinate vs physical time

| Paper | Internal-step semantics | Is intermediate step physically time-identified? |
|---|---|---|
| LAW | direct endpoint prediction | N/A |
| WoTE | recurrent state transition | **YES: predicted future time advances** |
| Epona | outer frame-autoregressive future + inner denoising | outer YES; inner denoising NO |
| WorldDrive | physical future teacher + diffusion sampling coordinate | physical future YES; diffusion step NO |
| World4Drive | direct endpoint future latent | N/A |
| SeerDrive | repeated planner/world hidden-feature refinement | NO; same decision state is refined |
| Drive-JEPA | masked spatiotemporal completion, no deployed transition path | N/A |
| Metis | action/video flow-denoising coordinate | NO; flow step is not physical waypoint/video time |
| **DynFlowDrive** | **Euler integration along rectified-flow coordinate `s` between `t` and `t+1`** | **NO intermediate physical supervision** |

Binding control:

```text
more internal solver/refinement steps
!= more predicted physical future time
```

DynFlowDrive makes this distinction especially important because it assigns a `stability` interpretation to the vector field along `s`.

---

# 3. Candidate-conditioned consequence truth

| Paper | Candidate-specific future output? | Per-candidate observed/simulated consequence truth? | Reactive other-agent truth? |
|---|---:|---:|---:|
| LAW | single action only | one factual future | NO |
| WoTE | YES | simulator/pseudo targets, but audited NAVSIM surrounding tracks largely fixed | NO in audited target path |
| Epona | controllable action-conditioned visual future | no K observed alternatives | NO established intervention truth |
| WorldDrive | YES teacher-generated candidate futures | learned-teacher alternatives, not observed interventions | NO direct real intervention proof |
| World4Drive | YES, K endpoint futures | **NO: one factual future latent** | NO |
| SeerDrive | YES, mode-conditioned future BEV | **NO: one factual future / WTA supervision** | NO |
| Drive-JEPA | NO world branches | N/A | NO |
| Metis | action-conditioned future-video generation during training | one logged factual future | NO |
| **DynFlowDrive** | **YES: N trajectory-conditioned flow paths** | **NO: one factual `z_{t+1}`** | **NO / NOT ESTABLISHED** |

Thus:

```text
candidate-conditioned vector field
!= candidate-specific counterfactual truth
```

---

# 4. Consequence model vs decision model

| Paper | Consequence model | Decision/value model | Relation at deployment |
|---|---|---|---|
| WoTE | recurrent BEV dynamics | explicit reward heads | both online |
| WorldDrive | heavy teacher / lightweight future surrogate | preference/ranking model | lightweight consequence + decision online |
| World4Drive | endpoint future latent | factual-mode ScoreNet | both online |
| Drive-JEPA | no deployed consequence model | simulator-trained scorer | scorer online only |
| Metis | training future-video generator | no explicit scorer | direct policy online |
| **DynFlowDrive** | **training-only flow WM** | **planner score head** | **consequence model removed; score head online** |

DynFlowDrive therefore resembles a teacher→student decision lifecycle, but the distilled object is **not a future latent**. What survives is ranking behavior in the score head.

---

# 5. Scorer semantics

| Paper | What does a high deployed score mean? | Direct training target |
|---|---|---|
| WoTE | utility/driving quality | imitation + simulator NC/DAC/TTC/comfort/progress |
| WorldDrive | learned preference / PDMS-like ranking with future feature | preference/ranking targets |
| World4Drive | factual-future/mode consistency | nearest-to-one-factual-future mode |
| Drive-JEPA | simulator/PDM driving quality + temporal comfort correction | simulator-derived proposal targets |
| **DynFlowDrive** | **learned preference for a mode chosen by hybrid teacher** | **GT trajectory error + factual latent reconstruction + flow-path directional stability** |

DynFlowDrive score is therefore not a direct online `world stability` measurement. At inference the scorer does not see the predicted future or flow velocities.

---

# 6. Strongest matched world-related evidence

| Paper | Strongest matched control | Main boundary |
|---|---|---|
| LAW | ± future-latent auxiliary shaping | auxiliary temporal regularization vs world semantics |
| WoTE | evaluator without future → + future | counterfactual/reactive validity |
| Epona | trajectory-only → trajectory+visual joint training | which visual property drives gain |
| WorldDrive | trajectory rewarder → + distilled future feature | teacher dynamics vs ranking signal |
| World4Drive | priors/intentions no WM → + WM | future predictor vs mode matching |
| SeerDrive | 2×2 future-aware × iterative | internal refinement != reactive truth |
| Drive-JEPA | generic V-JEPA2 → driving-domain JEPA | extra driving data/domain exposure |
| Metis | without video co-train 87.9 → with 89.5 EPDMS | auxiliary regularization / video prior |
| **DynFlowDrive** | **Static WM 0.61/0.30 → Flow WM 0.59/0.26 (Avg L2/CR)** | **shows flow parameterization helps, not that internal path is physical time** |

DynFlowDrive representation control:

```text
Flow WM                    0.59 / 0.26
+ pretrained World Feature 0.57 / 0.22
```

So representation prior and dynamics formulation remain distinct contributions.

---

# 7. Selection / supervision attribution

DynFlowDrive Table 5b:

```text
none              0.61 L2 / 0.30 CR
L2 only           0.59    / 0.24
+ reconstruction  0.58    / 0.22
+ flow stability  0.57    / 0.22
```

Cross-paper implication:

```text
world-derived candidate supervision can be useful
without retaining the world model online
```

But the final flow-stability term itself has a modest incremental effect:

```text
0.58 → 0.57 L2
0.22 → 0.22 CR
```

Therefore do not compress the full mode-selection gain into `flow stability`.

---

# 8. Internal-step performance curves

| Paper | Step axis | What one step means | Performance implication |
|---|---|---|---|
| WoTE | recurrent rollout step | predicted physical future transition | deeper physical foresight |
| SeerDrive | co-refinement iteration | internal planner/world feature update | same planning instant refined |
| Metis | action denoising step | generative solver iteration | policy sample refinement |
| **DynFlowDrive** | **flow Euler step** | **transport discretization between same physical endpoints** | **teacher/solver quality; 5 best, 10 degrades** |

DynFlowDrive:

```text
1 step   0.60 / 0.28
3        0.59 / 0.23
5        0.57 / 0.22
10       0.59 / 0.24
```

This is not a world-horizon curve.

---

# 9. Prediction/path fidelity vs planning evidence

| Paper | Dedicated future/prediction metric? | Direct fidelity→planning link? |
|---|---|---|
| Epona | visual-generation metrics | not clean monotonic proof |
| WorldDrive | video-generation metrics + planner ablations | partially suggestive, confounded |
| Metis | qualitative future video only in audited paper | NO |
| **DynFlowDrive** | **no independent latent-trajectory physical-fidelity benchmark identified** | **NO** |

DynFlowDrive's downstream L2/CR ablations show the training formulation is useful, but they do not validate the intermediate latent path against intermediate physical states.

---

# 10. Evaluation regime

| Paper | Main planning regime relevant here | Important correction |
|---|---|---|
| LAW | nuScenes open-loop | future shaping ≠ closed loop |
| WoTE | NAVSIM non-reactive + other reactive benchmarks in broader work | training/eval reactivity must be separated |
| World4Drive | nuScenes open-loop + NAVSIM non-reactive | not reactive alternative-agent truth |
| Drive-JEPA | NAVSIM non-reactive + Bench2Drive reactive CARLA | reactive eval does not change JEPA training semantics |
| Metis | NAVSIM non-reactive; real robot navigation closed loop | robot navigation != real-car AD closed loop |
| **DynFlowDrive** | **nuScenes open-loop + NAVSIM v1 non-reactive pseudo-simulation** | **paper's label `closed-loop NAVSIM` must not be upgraded to reactive closed loop** |

Thus 88.7 PDMS supports planner quality under NAVSIM's regime, not reactive learned-world validity.

---

# 11. Headline-comparison audit

Paper-highlighted SSR trajectory error improvement:

```text
SSR*                   0.39 Avg L2 / 0.15 CR
DynFlowDrive headline  0.31        / 0.11
```

But Table 1 separates:

```text
SSR*                             0.39 / 0.15
DynFlowDrive(SSR)                0.35 / 0.14
DynFlowDrive(SSR) + ego status   0.31 / 0.11
```

Therefore:

```text
more matched WM delta = 0.39 → 0.35
headline 0.39 → 0.31 includes ego-status input change
```

Binding rule strengthened:

```text
headline improvement
!= matched mechanism attribution
```

---

# 12. Source/equation integrity

DynFlowDrive currently has no released implementation.

Two paper-level ambiguities remain:

```text
Eq.7:
x_s=(1-s)a+s z_{t+1}
→ derivative should be z_{t+1}-a

Eq.10 target:
(1-s)(z_{t+1}-a)

AND

training interpolation starts from stochastic anchor a
sampling prose says integration starts from z_t
```

Until code release:

```text
exact implemented flow target = UNKNOWN
exact integration initial state = UNKNOWN
```

This prevents overconfident tensor-level reconstruction beyond the paper.

---

# 13. Nine-anchor lifecycle map after DynFlowDrive

```text
LAW
factual future latent auxiliary target
→ representation shaping
→ no future online

Drive-JEPA
masked predictive pretraining
→ encoder transfer
→ no predictor online

Metis
action-conditioned future-video co-training
→ world-loss-shaped action expert
→ no future online

DynFlowDrive
candidate-conditioned flow consequence teacher
→ world-derived score/mode supervision
→ no future online

Epona
joint visual+trajectory generation
→ shared history representation
→ visual future optional online

WorldDrive
heavy future teacher
→ distilled lightweight future summary
→ future summary online

World4Drive
candidate-conditioned endpoint future
→ factual-mode scorer
→ future online

WoTE
candidate-conditioned recurrent future
→ explicit utility
→ future online

SeerDrive
future endpoint ↔ planner hidden-state co-refinement
→ future online
```

This map now distinguishes not only `online/offline`, but **what exactly survives from world learning into deployment**.

---

# 14. Stable controls strengthened after DynFlowDrive

```text
rectified-flow time != physical time
continuous latent transport != validated continuous physical dynamics
smooth dz/ds != smooth dz/dtau
candidate-conditioned dynamics != counterfactual truth
world-derived score supervision != online world evaluation
training-time consequence model can disappear entirely at deployment
foundation latent gain != flow-dynamics gain
selection-teacher gain != consequence-model gain
solver-step depth != future-horizon depth
NAVSIM non-reactive evaluation != reactive closed-loop evidence
matched internal control > headline SOTA delta
```

Ontology V1.3 is therefore justified by **one** new stable axis, F08, rather than paper-specific module proliferation.
