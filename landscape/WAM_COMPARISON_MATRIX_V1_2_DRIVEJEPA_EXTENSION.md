# WAM Comparison Matrix V1.2 — Drive-JEPA Extension

Last updated: 2026-09-15

Status: **HISTORICAL PROJECTION SNAPSHOT — not current state or final route authority; retain only as a traceable comparison aid.**

Use with:

```text
landscape/WAM_COMPARISON_MATRIX_V1.md
landscape/WAM_COMPARISON_MATRIX_V1_1_SEERDRIVE_EXTENSION.md
landscape/WAM_DIMENSION_ONTOLOGY_V1_2_AMENDMENT.md
landscape/P0049_DRIVEJEPA_ONTOLOGY_PROJECTION.md
```

Anchors:

```text
LAW | WoTE | Epona | WorldDrive | World4Drive | SeerDrive | Drive-JEPA
```

This extension focuses on dimensions materially sharpened by Drive-JEPA rather than reproducing the full 97+ dimension projection.

---

# 1. Where predictive/world knowledge enters planning

| Paper | Predictive/world mechanism | Future object consumed online? | Final action interface |
|---|---|---:|---|
| LAW | action-aware factual future-latent auxiliary task shapes shared representation | **NO** | direct waypoint/planner head |
| WoTE | candidate-conditioned recurrent BEV future consequences | **YES** | future→explicit utility→argmax |
| Epona | joint visual-predictive + trajectory generation shapes shared history latent | visual future **NO** for planning mode | direct generative trajectory policy |
| WorldDrive | generative-WM representation inheritance + heavy future teacher distilled to lightweight future feature | **YES, distilled surrogate** | candidate→future-aware preference/ranking |
| World4Drive | candidate/intention-conditioned compact future endpoint latent | **YES** | future latent→factual-mode ScoreNet→select |
| SeerDrive | endpoint future BEV + internal world↔planner co-refinement | **YES** | future-BEV-guided planner feature fusion/refinement |
| **Drive-JEPA** | **masked video latent predictive pretraining → encoder transfer** | **NO** | **32 proposals→utility scorer→temporal recalibration→argmax** |

Drive-JEPA therefore expands the `training-only predictive knowledge` side of the map rather than adding another online consequence interface.

---

# 2. F07 — prediction temporal / observability geometry

| Paper | What is visible when prediction is made? | F07 class | Action-conditioned? |
|---|---|---|---:|
| LAW | current representation + predicted ego waypoint/action; later factual latent withheld | **CURRENT→FUTURE ENDPOINT** | **YES** |
| WoTE | current predicted state + candidate action; next future state withheld | **RECURRENT NEXT-STATE / AUTOREGRESSIVE FUTURE** | **YES** |
| Epona | historical visual/world context; future visual frames withheld | **HISTORY→UNSEEN FUTURE** | visual branch can be action-conditioned |
| WorldDrive | history + ego trajectory; future scene withheld | **HISTORY+TRAJECTORY→UNSEEN FUTURE** | **YES** |
| World4Drive | current physical latent + intention/action; future endpoint latent withheld | **CURRENT→FUTURE ENDPOINT** | **YES** |
| SeerDrive | current BEV + ego/mode feature; final-horizon BEV withheld | **CURRENT→FUTURE ENDPOINT** | mode/ego-feature conditioned |
| **Drive-JEPA** | **random subset of spatiotemporal tokens hidden while remaining clip context is visible** | **RANDOM-MASK SAME-WINDOW SPATIOTEMPORAL COMPLETION** | **NO** |

This is the main scientific distinction Drive-JEPA adds to the ontology.

A common phrase such as `latent prediction` now decomposes into at least:

```text
completion
forecasting
transition modeling
endpoint prediction
recurrent rollout
```

---

# 3. Predictive-training lifecycle

| Paper | When predictive objective acts | What transfers/remains | Predictor online? |
|---|---|---|---:|
| LAW | during planner training | shared planner representation | NO |
| Epona | joint multimodal training | shared history latent + trajectory generator | visual predictor optional/not needed for planning |
| WorldDrive | pretrain + teacher/distill stages | encoders + lightweight future surrogate | heavy teacher NO; surrogate YES |
| **Drive-JEPA** | **separate self-supervised video pretraining before planner** | **visual encoder** | **NO** |

Drive-JEPA is more strongly staged than LAW:

```text
LAW
planner training contains future-prediction loss

Drive-JEPA
predictive pretraining ends before downstream planning graph;
predictor/EMA target branch are removed
```

---

# 4. Predictive-pretraining controls: Drive-JEPA vs ViDAR

| Axis | ViDAR | Drive-JEPA |
|---|---|---|
| Pretext input | historical visual sequence | partially masked video clip |
| Target | chronologically future point clouds / future BEV features | EMA video latent at masked spatiotemporal positions |
| Target observability | future withheld | remaining spatial/temporal clip context visible depending mask |
| Dynamics factorization | autoregressive future decoder | masked latent predictor |
| Action conditioning | NO | NO |
| What transfers | history/BEV encoder | video ViT encoder |
| Future decoder/predictor deployed | NO | NO |
| Primary scientific claim | future forecasting learns geometry+temporal representation | masked video JEPA learns transferable spatiotemporal representation |

This comparison shows why `predictive pretraining` cannot be one undifferentiated ontology label.

---

# 5. Drive-JEPA vs LAW

| Axis | LAW | Drive-JEPA |
|---|---|---|
| Prediction timing | planner training | pretraining stage |
| Target | later factual scene/planner latent | masked same-video EMA latent |
| Chronological future required? | **YES** | **NO by stated random-mask objective** |
| Ego action condition? | **YES** | **NO** |
| Target network | detached factual-future branch | EMA target encoder + stop-grad |
| Predictor affects downstream training directly? | **YES** | NO after transfer |
| Predictor deployed? | NO | NO |
| Main benefit channel | auxiliary future shaping | pretrained representation transfer |

They share `future/predictive knowledge not consumed online`, but almost every supervision detail differs.

---

# 6. Action candidate / scorer matrix

| Paper | Online candidate bank | Candidate supervision | Scorer semantics | Future consequence required for score? |
|---|---:|---|---|---:|
| WoTE | 256 | human + simulator/evaluator | explicit utility/risk/progress | **YES**, learned future BEV |
| WorldDrive | 256→top-K | imitation + teacher/ranking | PDMS preference | **YES**, distilled future feature |
| World4Drive | 6 intentions | human/factual-mode supervision | factual-future mode consistency | **YES**, compact future latent |
| SeerDrive | multimodal modes, original core not WoTE scorer | WTA trajectory/future mode | no core scalar future utility | **YES**, future BEV refines planner |
| **Drive-JEPA** | **32** | **human + simulator-qualified pseudo trajectories** | **PDM/EPDMS utility + temporal comfort** | **NO** |

Drive-JEPA is an important control showing that strong candidate scoring can operate without an online learned consequence model.

---

# 7. Candidate diversity vs selection quality

Drive-JEPA provides unusually clear evidence that candidate diversity and final planning quality are different axes.

NAVSIM-v2:

```text
driving pretrain only
D = 24%
EC = 69.7
EPDMS = 86.1

+ MTD
D = 40%
EC = 47.9
EPDMS = 84.5

+ momentum-aware selection
D = 40%
EC = 84.8
EPDMS = 87.8
```

Thus:

```text
better candidate coverage
can initially make deployed policy worse
if the selector cannot resolve the larger support robustly.
```

This strengthens the existing field control:

```text
candidate generation/support
!=
candidate ranking/selection
```

and adds a concrete temporal-consistency example.

---

# 8. Iteration semantics after Drive-JEPA

| Paper | J08 iteration semantics | Physical predicted time advances? |
|---|---|---:|
| WoTE | recurrent world-state transition | **YES** |
| Epona | diffusion denoising / visual autoregressive rollout | depends on task mode |
| SeerDrive | internal world↔planner feature co-refinement | NO |
| **Drive-JEPA** | **planner proposal/query refinement** | **NO** |

Drive-JEPA further validates V1.1 J08: even inside planning-centric WAM papers, `iteration` may mean a fourth distinct object—candidate refinement—rather than world time, generative denoising, or world↔planner co-refinement.

---

# 9. Strongest matched evidence and attribution boundary

| Paper | Strongest matched evidence | What it supports | Main alternative explanation / boundary |
|---|---|---|---|
| LAW | ± future-latent auxiliary prediction | predictive representation shaping | exact learned semantics |
| WoTE | no evaluator→current-only→future evaluator ladder | online future consequence adds utility signal | reactive counterfactual validity |
| Epona | trajectory-only→joint visual+trajectory | joint predictive shaping | visual property causing gain unclear |
| WorldDrive | base→traj scorer→distilled future scorer | future feature beyond extra scorer | teacher validity / preference target |
| World4Drive | no-WM intentions→WM+selector | future-latent selector bundle | prediction vs mode-matching regularization |
| SeerDrive | 2×2 future-aware × iterative | future BEV + co-refinement separately useful | no causal/reactive world proof |
| **Drive-JEPA** | **simple decoder: V-JEPA2 86.1→drive JEPA 89.0; full planner 84.1→85.8/86.1 pretrain ladder** | **transfer value of video predictive representation/domain adaptation** | **extra 330h driving-domain exposure; not online world dynamics** |

Drive-JEPA's full 87.8/93.3 result also depends on MTD and scoring, so it is not a JEPA-only causal estimate.

---

# 10. Evaluation / counterfactual boundary

| Paper | Main planning evaluation | Candidate-specific world consequences | Reactive intervention truth? |
|---|---|---|---|
| WoTE | NAVSIM + Bench2Drive | learned BEV rollout | NAVSIM training path NO; Bench2Drive evaluation reactive |
| WorldDrive | NAVSIM | teacher-generated alternatives | NOT ESTABLISHED |
| World4Drive | nuScenes/NAVSIM | six future latent hypotheses | NO K observed alternatives |
| SeerDrive | NAVSIM/nuScenes + later Bench2Drive paper evidence | multimodal future BEV | NOT ESTABLISHED |
| **Drive-JEPA** | **NAVSIM v1/v2 + Bench2Drive** | **NONE online; candidate-specific utility only** | **NAVSIM NO; Bench2Drive planner evaluation reactive** |

Reactive closed-loop planner success does not convert the JEPA pretraining objective or NAVSIM pseudo-teacher source into intervention-valid world dynamics.

---

# 11. Updated future-knowledge / prediction taxonomy

After Drive-JEPA, the field coordinate system should separate at least two orthogonal questions:

```text
A. What predictive obligation is learned?
   masked completion
   causal future forecasting
   action-conditioned transition
   endpoint prediction
   recurrent rollout

B. What happens to predictive knowledge at planning inference?
   predictor discarded; encoder transferred
   auxiliary predictor discarded after joint training
   future predictor stays online
   heavy teacher distilled to surrogate
   sibling simulator optional
   direct world/action joint generator
```

Drive-JEPA occupies:

```text
A = RANDOM-MASK SAME-WINDOW COMPLETION
B = PREDICTOR DISCARDED; ENCODER TRANSFERRED
```

This position is distinct from all six previous normalized anchors.

---

# 12. Seven-anchor mechanism map

```text
LAW
= action-aware chronological future-latent auxiliary shaping

WoTE
= action-conditioned recurrent future BEV → explicit utility → selection

Epona
= shared history latent → joint trajectory / visual generation

WorldDrive
= generative world pretraining + heavy future teacher
→ distilled online future surrogate → ranking

World4Drive
= action/intention-conditioned future endpoint latent
→ factual-mode selector

SeerDrive
= future BEV endpoint ↔ planner hidden-feature co-refinement

Drive-JEPA
= random-mask video predictive pretraining → encoder transfer
+ simulator-distilled multimodal proposals → utility/comfort selection
```

The main addition is therefore **not another future→action arrow**. It is a sharper distinction inside predictive representation learning itself.
