# WAM Comparison Matrix V1.2 — Metis Extension

Last updated: 2026-09-15

Status: **HISTORICAL PROJECTION SNAPSHOT — not current state or final route authority; retain only as a traceable comparison aid.**

Base coordinate system:

```text
landscape/WAM_DIMENSION_ONTOLOGY_V1.md
landscape/WAM_DIMENSION_ONTOLOGY_V1_1_AMENDMENT.md
landscape/WAM_DIMENSION_ONTOLOGY_V1_2_AMENDMENT.md
```

Existing matrices:

```text
landscape/WAM_COMPARISON_MATRIX_V1.md
landscape/WAM_COMPARISON_MATRIX_V1_1_SEERDRIVE_EXTENSION.md
landscape/WAM_COMPARISON_MATRIX_V1_2_DRIVEJEPA_EXTENSION.md
```

New full projection:

```text
landscape/P0062_METIS_ONTOLOGY_PROJECTION.md
```

Anchors considered here:

```text
LAW | WoTE | Epona | WorldDrive | World4Drive | SeerDrive | Drive-JEPA | Metis
```

---

# 1. Future knowledge: training role vs deployed role

| Paper | Future/world mechanism during training | Future object required during deployed action selection? | Deployed planning mechanism |
|---|---|---:|---|
| LAW | action-aware factual future-latent auxiliary loss | NO | direct waypoint policy |
| WoTE | recurrent candidate-conditioned future BEV + reward learning | **YES** | candidate future → utility → argmax |
| Epona | visual + trajectory generative losses shape shared history latent | visual future **NO** for planning mode | direct generative trajectory policy |
| WorldDrive | heavy generative WM teacher + future-feature distillation | **YES, distilled summary** | candidates → distilled future-aware ranking |
| World4Drive | intention/action-conditioned endpoint future latent | **YES** | future modes → ScoreNet → select |
| SeerDrive | future BEV + iterative world/planner feature co-refinement | **YES** | future-BEV planner branch + fusion |
| Drive-JEPA | masked-video JEPA pretraining → encoder transfer | NO | proposal/refinement/scorer policy |
| **Metis** | **action-conditioned future-video flow loss shapes AE through asymmetric co-training** | **NO** | **direct action-flow denoising** |

Metis reinforces that:

```text
world supervision useful during training
!=
world future required at deployment
```

---

# 2. Joint world-action modeling must be vector-valued

| Paper | Shared representation? | Shared parameters? | Shared/joint losses or gradients? | Forward action→world? | Forward world-future→action? | Both future/action branches required online? |
|---|---|---|---|---|---|---|
| LAW | upstream planner/world features partially shared | predictor separate | YES: future loss shapes planner representation | YES | NO | NO |
| Epona | **YES: shared F** | shared MST + separate DiTs | **YES** | action can condition VisDiT | NO same-step visual-future→planner | NO |
| WorldDrive | transferred/shared representation across stages | teacher/student/planner distinct | teacher/distillation gradients by stage | YES | YES via distilled future feature | lightweight future only |
| World4Drive | current physical latent shared across planner/WM | partial shared graph | YES | YES | YES via ScoreNet | YES |
| SeerDrive | current/future/planner features interact | partial | YES, all refinement stages | **YES planner→world** | **YES world→planner** | YES |
| Drive-JEPA | encoder transferred | JEPA predictor not shared with planner | stage-separated | NO deployed world | NO | NO |
| **Metis** | **shared interaction latent/current context; specialized expert states** | **NO full sharing; separate VGE/AE experts** | **YES: video loss can backprop into AE** | **YES during training** | **NO — masked by design** | **NO** |

Metis adds a particularly useful control:

```text
world→action gradient influence
!=
world→action forward information flow
```

---

# 3. Coupling direction by computational phase

| Paper | Training forward graph | Training backward influence | Inference graph |
|---|---|---|---|
| LAW | planner action → future predictor | future loss → planner representation | current → waypoint; future branch discarded |
| Epona | F → trajectory; F+action → visual future | L_traj + L_vis → shared F | F → trajectory; visual branch optional |
| WorldDrive | candidate → teacher future | teacher/distillation → lightweight surrogate/planner | candidate → surrogate future → ranking |
| World4Drive | candidate/action → future latent → score | joint losses through predictor/planner | same compact future path online |
| SeerDrive | planner feature ↔ future-BEV feature | losses across refinement iterations | repeated internal world↔planner refinement |
| Drive-JEPA | masked video → JEPA target | JEPA loss → encoder, in prior stage | encoder → planner; predictor absent |
| **Metis** | **AE action → VGE future video** | **L_video → VGE → AE through action dependence** | **current context → AE → action only** |

This phase-specific table should replace generic labels such as `bidirectional WAM` whenever possible.

---

# 4. F07 — prediction temporal / observability geometry

| Paper | F07 prediction obligation |
|---|---|
| LAW | current latent + predicted action → factual future endpoint latent |
| WoTE | recurrent current state-action → next/future BEV transition |
| Epona | historical context → chronologically unseen future visual generation |
| WorldDrive | history + trajectory → chronologically unseen future scene/video latent |
| World4Drive | current physical latent + intention/action → future endpoint latent |
| SeerDrive | current BEV + mode/planner feature → final-horizon future BEV |
| Drive-JEPA | **random-mask same-window spatiotemporal completion** |
| **Metis** | **current context + action → chronologically unseen future video latent chunk** |

Metis therefore validates F07 rather than requiring another temporal-prediction dimension.

---

# 5. Direct policy vs candidate evaluation

| Paper | Action interface | Explicit candidate bank? | Explicit scorer? | Future used for ranking? |
|---|---|---:|---:|---:|
| LAW | direct waypoint | NO | NO | NO |
| WoTE | candidate selector | YES | YES | YES |
| Epona | direct generative trajectory | NO scored bank | NO | NO |
| WorldDrive | candidate selector | YES | YES | YES |
| World4Drive | intention candidates | YES | ScoreNet | YES |
| SeerDrive | multimodal planner/fusion | modes | original core not future utility scorer | future feature refines planner |
| Drive-JEPA | 32 learned proposals | YES | YES | NO learned world future |
| **Metis** | **direct stochastic/flow action chunk** | **NO fixed bank** | **NO** | **NO** |

Metis final performance should therefore not be compared to WoTE/WorldDrive only as a “better world model”; their host planners solve different decision problems.

---

# 6. Strongest matched evidence for the world-related mechanism

| Paper | Strongest matched control | What it reasonably isolates | Main remaining confound |
|---|---|---|---|
| LAW | ± future-latent/action-aware auxiliary loss | predictive representation shaping | latent semantics/auxiliary regularization |
| WoTE | trajectory only → evaluator no future → +future | future consequence inside evaluator | reactive/counterfactual validity |
| Epona | trajectory-only → joint visual+trajectory | visual predictive auxiliary contribution to shared representation | exact visual property causing gain |
| WorldDrive | base/scorer → +distilled future feature | lightweight future feature beyond trajectory-only ranking | teacher dynamics vs ranking supervision |
| World4Drive | priors+intentions no WM → +WM | future-latent selector bundle | prediction vs mode matching/regularization |
| SeerDrive | 2×2 future-aware × iterative | future feature and co-refinement contributions | no causal/reactive truth proof |
| Drive-JEPA | generic V-JEPA2 → driving-domain JEPA; full module ladder | predictive representation transfer; proposal/selector contributions | extra domain data + planner modules |
| **Metis** | **w/o video co-train 87.9 → w/video co-train 89.5 EPDMS** | **future-video auxiliary co-training benefit to action policy** | **world-fidelity vs generic auxiliary regularization + imported prior** |

Metis also provides the matched 320×384 attention ablation:

```text
Joint       87.4 / 28.0
Isolated    88.3 / 29.4
Asymmetric  88.8 / 31.6
            navtest / navhard EPDMS
```

This isolates **interaction topology** better than the headline SOTA table.

---

# 7. Prediction quality vs planning quality

| Paper | Dedicated world/prediction-quality metric? | Direct evidence world fidelity tracks planning? |
|---|---|---|
| Epona | visual-generation metrics exist | not cleanly established as monotonic planning relation |
| WorldDrive | generative metrics + planner ablations | teacher quality not fully isolated from representation/ranking |
| Drive-JEPA | no deployed world fidelity metric | NO |
| **Metis** | **qualitative future-video outputs; no dedicated quantitative fidelity metric identified** | **NO** |

Metis therefore strengthens the existing control:

```text
benefit from a world-prediction task
!=
evidence that world-prediction fidelity is the causal planning variable
```

---

# 8. Future-knowledge lifecycle after Metis

```text
LAW
future latent target
→ auxiliary loss during planner training
→ no future object online

Drive-JEPA
masked predictive pretraining
→ encoder transfer
→ predictor removed before planner deployment

Epona
joint visual+trajectory generative training
→ shared F shaped
→ visual future branch optional in planning

Metis
action-conditioned future-video co-training
→ video loss gradient shapes action expert
→ future-video path bypassed at deployment
→ direct action-flow policy

WorldDrive
heavy future teacher
→ distillation
→ lightweight future surrogate remains online

World4Drive
compact action-conditioned endpoint future
→ remains online
→ factual-mode ScoreNet

WoTE
compact recurrent future transition
→ remains online
→ explicit utility selection

SeerDrive
compact future BEV
→ remains online
↔ planner feature co-refinement
```

Metis is therefore closest to a new *combination* of existing axes rather than a new ontology primitive:

```text
training-time action→world forward coupling
+
world-loss→policy gradient shaping
+
action-only deployment
```

---

# 9. Efficiency semantics

| Paper | World-related deployment compute | Important caveat |
|---|---|---|
| WoTE | many candidates × recurrent compact future | parallel/batched compact states |
| WorldDrive | lightweight distilled future surrogate | heavy teacher removed |
| World4Drive | six endpoint latent futures | compact online predictor |
| SeerDrive | repeated future-BEV/planner co-refinement | iteration != future-time rollout |
| Drive-JEPA | zero online predictive-world depth | proposal/refinement/scorer still costs compute |
| **Metis** | **zero explicit future-video generation in action-only mode** | **action flow still requires denoising; 0.17 s operating point also uses fewer steps than with-video row** |

Metis reports a useful action-only denoising curve:

```text
1 step   87.2 navtest / 30.4 navhard EPDMS
2        89.2         / 31.2
5        89.4         / 31.4
10       89.5         / 32.2
```

---

# 10. Counterfactuality vector

| Paper | Action-conditioned future? | Alternative-action factual supervision? | Reactive other-agent truth? | Intervention evidence? |
|---|---:|---:|---:|---:|
| LAW | YES | NO | NO | NO |
| WoTE | YES | simulator/semantic candidate targets | not in audited fixed-surrounding path | NO |
| Epona | controllable visual generation | NO K matched truths | not established | NO |
| WorldDrive | YES | generated/teacher alternatives | not established | NO |
| World4Drive | YES | one factual future assigns mode | not established | NO |
| SeerDrive | mode-conditioned | one factual WTA mode | not established | NO |
| Drive-JEPA | NO learned world branches | NO | NO | NO |
| **Metis** | **YES during video training** | **NO** | **NOT ESTABLISHED** | **NO** |

Again:

```text
action-conditioned video generation
!=
causally identified alternative future
```

---

# 11. Historical novelty boundary

Metis cites Fast-WAM and explicitly frames its decoupled inference formulation as inspired by that work.

Therefore:

```text
training with world/video objective
→ skip explicit future generation at inference
```

is prior art before Metis.

Metis's differentiating mechanism should instead be compared on:

```text
Mixture-of-Transformers expert separation
asymmetric attention direction
video-loss→AE gradient path
AD + urban-navigation transfer
quality/latency operating point
```

This prevents a lifecycle idea from being misclassified as a new WAM family simply because the application paper uses new architecture language.

---

# 12. Source/status warning

Unlike the recently audited Drive-JEPA source path, Metis has no public implementation source available in the official repository as of 2026-09-15.

Use:

```text
PAPER-VERIFIED
OFFICIAL-README-VERIFIED
SOURCE-UNVERIFIED
```

for decision-critical mechanism cells.

Do not infer exact module execution, parameter freezing or code-level latency scope beyond paper/README statements.

---

# 13. Ontology stress-test result

Candidate new concept:

```text
forward action→world
backward world-loss→action
without world-future→action forward dependency
```

Merge test:

```text
E01/E02 = forward action→world
J04     = computational causal direction
L04     = gradient coupling direction
M01-M03 = lifecycle / deployment transformation
```

Result:

```text
NO new dimension survives.
Ontology V1.2 remains active.
```

This is scientifically preferable to creating a Metis-specific axis.
