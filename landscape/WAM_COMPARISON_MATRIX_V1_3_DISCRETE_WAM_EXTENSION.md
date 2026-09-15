# WAM Comparison Matrix V1.3 — Discrete-WAM Extension

Last updated: 2026-09-15

Status: **TEN-ANCHOR EXTENSION — ONTOLOGY V1.3 RETAINED**

Coordinate system:

```text
WAM_DIMENSION_ONTOLOGY_V1.md
+ WAM_DIMENSION_ONTOLOGY_V1_1_AMENDMENT.md
+ WAM_DIMENSION_ONTOLOGY_V1_2_AMENDMENT.md
+ WAM_DIMENSION_ONTOLOGY_V1_3_AMENDMENT.md
```

Anchors:

```text
LAW | WoTE | Epona | WorldDrive | World4Drive
| SeerDrive | Drive-JEPA | Metis | DynFlowDrive | Discrete-WAM
```

Full Discrete-WAM projection:

```text
landscape/P0064_DISCRETE_WAM_ONTOLOGY_PROJECTION.md
```

---

# 1. Future/world knowledge lifecycle

| Paper | Training-time future/world mechanism | Future/world object required for deployed action selection? | Deployed decision mechanism |
|---|---|---:|---|
| LAW | factual future-latent auxiliary prediction | NO | direct waypoint policy |
| WoTE | candidate-conditioned recurrent future BEV + reward learning | **YES** | future consequence → explicit utility → argmax |
| Epona | shared-latent trajectory + visual generation | visual future NO for planning | direct generative trajectory policy |
| WorldDrive | heavy future teacher + representation inheritance/distillation | **YES, lightweight distilled future** | future-aware candidate ranking |
| World4Drive | candidate/intention-conditioned endpoint future latent | **YES** | future mode → ScoreNet → select |
| SeerDrive | future BEV ↔ planner feature co-refinement | **YES** | internal future-aware iterative planner |
| Drive-JEPA | masked predictive video pretraining | NO | proposal/refinement/scorer policy |
| Metis | action-conditioned future-video co-training | NO | direct action-flow policy |
| DynFlowDrive | candidate-conditioned flow WM → mode/score teaching | NO | learned score head → argmax |
| **Discrete-WAM** | **world / policy / interleaved world-policy discrete multitask pretraining** | **NO for primary planning; optional world-generation capability** | **decision token → parallel action-token editing → trajectory** |

Discrete-WAM therefore adds a strong control:

```text
more unified training / parameter sharing
!=
more online dependence on predicted future world
```

---

# 2. What does `unified world-action` actually mean?

| Paper | Shared representation | Shared parameters | Shared token/codebook | Joint losses/gradients | Both world/action active in primary planning inference? |
|---|---|---|---|---|---|
| LAW | partial/shared planner representation | predictor separate | N/A | YES future loss shapes planner | NO |
| Epona | **shared F** | shared MST + separate DiTs | N/A | YES | visual branch NO |
| Metis | interaction/shared latent interface | separate AE/VGE experts | N/A | YES, asymmetric | NO |
| DynFlowDrive | planner/world features interact | planner + flow WM separate | N/A | YES in training | NO |
| **Discrete-WAM** | **YES common Transformer hidden space** | **YES same decoder backbone** | **NO — separate visual/action vocabularies** | **YES during joint stage** | **NO for primary planner** |

Binding rule strengthened:

```text
shared codebook
shared hidden space
shared parameters
shared sequence
shared gradient
active together at inference
```

are six different properties.

---

# 3. Discrete representation topology

| Property | Discrete-WAM |
|---|---|
| Visual vocabulary | VQ-style, ~16,384 entries |
| Action vocabulary | 60×60 ≈ 3,600 acceleration prototypes |
| High-level decision vocabulary | ~400 structured decision candidates |
| One shared world/action codebook? | **NO** |
| Common hidden/Transformer interface? | **YES** |
| Common sequence possible? | **YES** |
| Common physical token semantics? | **NO evidence** |

This is kept as an ontology **residue watchlist**, not promoted to V1.4 yet because the prior anchor set is predominantly continuous-latent.

---

# 4. Action ↔ world forward coupling

| Paper | Action→world | World future→action | Phase where it occurs |
|---|---|---|---|
| LAW | predicted waypoint conditions future latent | NO same-step future→current action | training auxiliary |
| WoTE | candidate action conditions future transition | YES via future reward | online |
| Epona | action can condition visual branch | NO visual-future→trajectory in primary planning | joint training / optional simulation |
| WorldDrive | candidate conditions future teacher/surrogate | YES via distilled future ranking | train + online lightweight |
| World4Drive | candidate/action conditions future latent | YES via ScoreNet | online |
| SeerDrive | planner hidden/mode conditions future BEV | YES future BEV refines planner | online co-refinement |
| Drive-JEPA | no action-conditioned JEPA world model | NO | pretraining only |
| Metis | YES action→future-video | NO future-video→action forward; gradient only | training |
| DynFlowDrive | YES candidate→flow WM | NO online; world-derived label only | training |
| **Discrete-WAM** | **YES same-step action→future visual in world/world-policy task** | **YES prior world token can condition later action in joint sequence; NO mandatory future-world→action in primary planning** | **joint generation/training capability; planning path action-only** |

---

# 5. Planning interface

| Paper | Canonical planning interface |
|---|---|
| LAW | future-as-training-representation-teacher |
| WoTE | future-as-online-consequence + explicit utility |
| Epona | shared representation + direct generative policy |
| WorldDrive | representation inheritance + distilled online foresight |
| World4Drive | compact online future + factual-mode selector |
| SeerDrive | online future/planner internal co-refinement |
| Drive-JEPA | predictive representation pretraining + simulator-distilled proposal/scorer |
| Metis | world-loss-shaped direct policy, action-only deployment |
| DynFlowDrive | world-derived mode/score teacher, WM removed |
| **Discrete-WAM** | **shared discrete world-policy pretraining + hierarchical direct token policy; future visual generation optional** |

---

# 6. F07 — prediction temporal / observability geometry

| Paper | F07 |
|---|---|
| LAW | current + action → factual future endpoint |
| WoTE | recurrent next-state/autoregressive future |
| Epona | history → unseen future visual sequence |
| WorldDrive | history + trajectory → unseen future scene |
| World4Drive | current + intention/action → endpoint future latent |
| SeerDrive | current + mode/planner feature → final-horizon future BEV |
| Drive-JEPA | random-mask same-window spatiotemporal completion |
| Metis | current context + action → unseen future-video chunk |
| DynFlowDrive | current latent + candidate → factual next endpoint via flow objective |
| **Discrete-WAM** | **current/history + action → chronologically unseen future visual tokens; joint sequence can autoregress across future world/action pairs** |

---

# 7. F08 / J08 — physical time vs internal iteration

| Paper | Physical future axis | Internal step axis |
|---|---|---|
| WoTE | recurrent predicted future time | each rollout step advances scene time |
| Epona | autoregressive future frame time | inner diffusion/denoising step |
| WorldDrive | future video/latent time | teacher diffusion sampling step |
| SeerDrive | fixed future endpoint | world↔planner hidden co-refinement iteration |
| Metis | future action/video horizon | flow/denoising iteration |
| DynFlowDrive | t→t+1 endpoint | rectified-flow transport coordinate s |
| **Discrete-WAM** | **interleaved A_h / V_h physical future positions** | **token-edit/discrete-diffusion refinement round** |

Control:

```text
action token position / editing round
!=
physical world timestep
```

---

# 8. Counterfactuality vector

| Paper | Candidate/action-specific future output | Per-action observed/simulated consequence truth | Reactive other-agent truth | Intervention validity |
|---|---:|---:|---:|---:|
| LAW | limited/single | one factual future | NO | NO |
| WoTE | YES | pseudo/simulator candidate targets; fixed-surrounding limitation in audited path | NO in audited path | NO |
| Epona | controllable future | NO matched K truths | NOT ESTABLISHED | NO |
| WorldDrive | YES teacher-generated futures | learned-teacher alternatives | NOT ESTABLISHED | NO |
| World4Drive | YES | **NO: one factual future** | NO | NO |
| SeerDrive | YES mode-conditioned | **NO: one factual WTA target** | NO | NO |
| Drive-JEPA | no world branches | N/A | NO | NO |
| Metis | action-conditioned future video | one logged future | NOT ESTABLISHED | NO |
| DynFlowDrive | YES flow branches | **NO: one factual next latent** | NO | NO |
| **Discrete-WAM** | **YES action perturbations / alternative token sequences generate distinct futures** | **NO matched alternative factual futures** | **NOT ESTABLISHED** | **NO direct proof** |

Discrete-WAM surprise analysis is therefore a useful sensitivity/safety proxy, not ground-truth counterfactual validation.

---

# 9. Consequence model vs decision/value model

| Paper | Consequence representation | Decision/value mechanism at deployment |
|---|---|---|
| WoTE | recurrent BEV future | explicit utility heads |
| WorldDrive | distilled future latent | preference/ranking rewarder |
| World4Drive | endpoint future latent | factual-mode ScoreNet |
| SeerDrive | future BEV | planner-feature refinement/fusion |
| Drive-JEPA | none online | simulator-trained scorer |
| Metis | none online | direct flow policy |
| DynFlowDrive | none online | learned score head taught by world-derived label |
| **Discrete-WAM** | **none required online for planning** | **decision classifier + action token policy + RL/post-training reward** |

Thus Discrete-WAM's high planning score cannot be interpreted as evidence of an online consequence evaluator.

---

# 10. Strongest matched world-related evidence

| Paper | Strongest control | Main boundary |
|---|---|---|
| LAW | ± future-latent auxiliary | auxiliary regularization vs world semantics |
| WoTE | evaluator no future → + future | reactive/counterfactual validity |
| Epona | trajectory-only → joint visual+trajectory | which visual property causes gain |
| WorldDrive | rewarder → + distilled future feature | teacher dynamics vs ranking signal |
| World4Drive | priors/intentions no WM → + WM | dynamics vs mode matching |
| SeerDrive | future-aware × iterative 2×2 | internal loop != environmental reactivity |
| Drive-JEPA | generic V-JEPA → driving JEPA | domain-data confound |
| Metis | without video co-train → with video co-train | world fidelity vs auxiliary regularization |
| DynFlowDrive | Static WM → Flow WM | flow parameterization ≠ physical-time validation |
| **Discrete-WAM** | **From scratch 89.8 / FT 89.7 / vision-oriented pretrain+LoRA 90.0 EPDMS** | **does not isolate full joint world+action pretraining; adaptation regime changes** |

Decision modeling is more strongly isolated:

```text
Base       84.7
Base-D_t   87.2
```

and posttraining:

```text
SFT       89.1
SFT-D_t   90.0
RL        90.4
```

Therefore high-level decision prior/post-training are major independent contributors.

---

# 11. Prediction fidelity → planning evidence

| Paper | Dedicated future/world metric | Direct monotonic fidelity→planning evidence? |
|---|---|---|
| Epona | YES | NO clean proof |
| WorldDrive | YES | partial/confounded |
| Metis | qualitative only in audited paper | NO |
| DynFlowDrive | no independent physical latent-path fidelity | NO |
| **Discrete-WAM** | **YES: FID ~6.6, FVD ~80.0** | **NO matched causal link to EPDMS** |

Strong world-generation metrics and strong planning metrics coexist, but that is not sufficient to identify generation fidelity as the planning mechanism.

---

# 12. Safety / risk semantics

| Method | Where safety/risk primarily appears |
|---|---|
| WoTE | explicit reward heads / driving utility |
| WorldDrive | preference/PDMS-like ranking supervision |
| World4Drive | implicit in factual-mode selection; no explicit utility |
| Drive-JEPA | simulator/PDM scorer + temporal comfort correction |
| DynFlowDrive | hybrid world/trajectory positive-mode teacher |
| **Discrete-WAM** | **decision/reward target via EPDMS/PDM terms + world-model surprise diagnostic; no explicit risk-state representation** |

This is particularly relevant for later risk-aware synthesis: Discrete-WAM's surprise is an endogenous model-sensitivity signal, not a calibrated future-risk state.

---

# 13. Planning evaluation regime

| Paper | Relevant regime | Correction |
|---|---|---|
| LAW | nuScenes open-loop | no closed-loop proof |
| World4Drive | nuScenes + NAVSIM | NAVSIM non-reactive |
| Drive-JEPA | NAVSIM + Bench2Drive | reactive eval does not change JEPA training semantics |
| Metis | NAVSIM + robot navigation | robot navigation != real-car AD closed loop |
| DynFlowDrive | nuScenes + NAVSIM | paper `closed-loop` wording normalized to non-reactive |
| **Discrete-WAM** | **NAVSIM v1/v2 planning + offline future generation** | **NAVSIM remains non-reactive data-driven/pseudo-simulation** |

---

# 14. Ten-anchor lifecycle map

```text
LAW
factual future latent auxiliary
→ planner representation shaping
→ no future online

Drive-JEPA
masked predictive pretraining
→ encoder transfer
→ no predictor online

Metis
action-conditioned future-video co-training
→ world-loss-shaped policy
→ no future online

DynFlowDrive
candidate-conditioned flow consequence teacher
→ world-derived score supervision
→ no future online

Discrete-WAM
shared discrete world/policy multitask pretraining
→ shared backbone + hierarchical decision/action token policy
→ no future visual required in primary planning

Epona
joint visual/trajectory generation
→ shared F
→ visual future optional online

WorldDrive
heavy future teacher
→ distilled future summary
→ lightweight future online

World4Drive
candidate endpoint future
→ factual-mode scorer
→ future online

WoTE
candidate recurrent future
→ explicit utility
→ future online

SeerDrive
future endpoint ↔ planner hidden-state co-refinement
→ future online
```

This lifecycle map now demonstrates that **training unification and deployment model-basedness are largely orthogonal axes**.

---

# 15. Ontology stress-test result

Candidate residue:

```text
shared codebook
vs
separate modality vocabularies
vs
common hidden/sequence interface
```

The distinction is scientifically real but does not yet pass the cross-anchor back-projection threshold because prior core anchors are mostly non-discrete.

Decision:

```text
Ontology V1.3 RETAINED
NO V1.4 AMENDMENT
```

Add to residue watchlist and re-test with a second discrete-token anchor.

Generation order / interleaving is already represented by:

```text
F04 + E02 + J04 + F08
```

and does not justify another dimension.

---

# 16. Stable controls strengthened after Discrete-WAM

```text
shared discrete framework != shared codebook
shared Transformer != identical modality semantics
joint world-policy training != online world imagination
world-generation capability != world-generation-required planning
strong FID/FVD + strong EPDMS != fidelity→planning causality
action-conditioned alternative generation != counterfactual ground truth
high-level decision prior can dominate world-pretraining matched gains
token-edit round != physical future timestep
model capability graph != primary deployment graph
```
