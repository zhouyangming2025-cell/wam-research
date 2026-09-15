# WAM Dimension Discovery Addendum — Epona + WorldDrive

Last updated: 2026-09-15

Status: **ACTIVE ADDENDUM — merge into `WAM_DIMENSION_ONTOLOGY_V1.md` only after World4Drive re-projection**

This file supplements `landscape/WAM_DIMENSION_DISCOVERY_LOG.md`, whose LAW/WoTE sections remain canonical. It records dimensions exposed by the third and fourth ontology-discovery anchors without prematurely freezing IDs.

Sources:

```text
papers/deep_analysis/P0001_EPONA_DEEP_ANALYSIS_V2.md
papers/deep_analysis/P0042_WORLDDRIVE_DEEP_ANALYSIS_V2.md
audits/literature/PHASE_C5_WORLDDRIVE_AUDIT.md
```

---

# 1. Epona pressure test — dimensions LAW/WoTE did not expose cleanly

| ID | New/refined dimension | Epona position | Why it matters |
|---|---|---|---|
| EPONA-D01 | **Historical/current state vs predicted future state** | planner consumes shared historical latent `F`; visual future is a separate VisDiT output | A model may use a world representation online without consuming a predicted future world. |
| EPONA-D02 | **Temporal factorization by modality** | frame-autoregressive visual future; multi-step trajectory generated in one diffusion process | One system can use different temporal semantics for world and action. |
| EPONA-D03 | **Action-selection mechanism** | direct diffusion/flow generative policy | Separate direct policy generation from candidate→consequence→score selection. |
| EPONA-D04 | **Distributional trajectory generation vs explicit candidate bank** | stochastic TrajDiT, no WoTE-style scored candidate set | Multimodal policy output is not the same as candidate evaluation. |
| EPONA-D05 | **Representation jointness** | MST latent `F` shared by trajectory and visual branches | Shared representation should not be conflated with shared output path. |
| EPONA-D06 | **Parameter jointness** | branches share upstream MST, then separate DiTs | Need distinguish shared backbone from separate modality heads. |
| EPONA-D07 | **Gradient/loss jointness** | `L_traj + L_vis` jointly shape shared latent | Joint training can help planning even when future output is absent at inference. |
| EPONA-D08 | **Online causal coupling direction** | trajectory/action can condition VisDiT; visual future does not re-score same-step trajectory | `joint modeling` does not imply bidirectional online planning feedback. |
| EPONA-D09 | **Task-mode-dependent inference graph** | planning: MST→TrajDiT; simulation: MST→VisDiT with action | One model can have different deployed graphs for planning and simulation. |
| EPONA-D10 | **Rollout distribution-shift training** | Chain-of-Forward exposes model to self-predicted contexts | Autoregressive robustness is a separate design dimension from one-step accuracy. |
| EPONA-D11 | **Modality-specific auxiliary module relevance** | temporal-aware DCAE improves visual decoding but not planning-only inference | Every module must be tagged by scientific function, not just architecture. |
| EPONA-D12 | **Quality–latency operating curve** | DiT sampling steps alter speed; planning-quality retention at fastest setting not fully isolated | Diffusion planners require a curve, not one latency number. |
| EPONA-D13 | **Evidence capability separation** | video FID/FVD evidence vs NAVSIM planning evidence | World-generation evidence cannot stand in for planning evidence. |
| EPONA-D14 | **Cross-modal predictive shaping** | visual-future training improves planner through shared `F` | Future can help policy through representation learning without online consequence use. |

## Epona's strongest ontology correction

The phrase `joint world/action modeling` must be split into at least:

```text
shared representation?
shared parameters?
shared loss / gradient?
action → world coupling?
world future → action feedback?
active together at inference?
```

Epona is strong on the first four but does not demonstrate same-step visual-future→trajectory feedback in planning mode.

---

# 2. WorldDrive pressure test — dimensions added or split

| ID | New/refined dimension | WorldDrive position | Why it matters |
|---|---|---|---|
| WD-D01 | **Representation origin stack** | CogVideoX generic prior → TA-DWM specialization → planner transfer | Generic foundation effects must be separated from WM-specific future-model effects. |
| WD-D02 | **Visual vs motion representation inheritance** | both explicitly inherited | `unified representation` hides distinct transferable objects. |
| WD-D03 | **Transfer/freeze policy** | transferred encoders frozen in planner stage | Fine-tuned vs frozen transfer changes causal interpretation. |
| WD-D04 | **Cross-task representation identity** | trajectory encoder/motion space deliberately reused from generation to planning | Stronger than generic “pretraining.” |
| WD-D05 | **Optimization topology** | WM pretrain → planner training → frozen-teacher FAR distillation | End-to-end deployed interface does not imply end-to-end joint optimization. |
| WD-D06 | **First-stage vs second-stage decision architecture** | base planner scores/refines 256 anchors; FAR re-ranks top-K | Planning quality is produced by multiple decision layers. |
| WD-D07 | **Branch-pruning location** | 256 → top-K before future-aware reasoning | Determines candidate support × online imagination cost. |
| WD-D08 | **Candidate oracle ceiling / ranking gap** | best-of-6 oracle much higher than normal selection | Separates candidate generation bottleneck from ranking bottleneck. |
| WD-D09 | **Consequence teacher type** | frozen learned generative TA-DWM | Future target can come from another learned model rather than factual/simulator truth. |
| WD-D10 | **Value teacher type** | PDMS/oracle candidate preference | Consequence teacher and utility teacher can be different systems. |
| WD-D11 | **Teacher error inheritance** | FAR student imitates TA-DWM latent | Distillation transfers teacher bias/errors as well as useful dynamics. |
| WD-D12 | **Future-knowledge lifecycle** | heavy diffusion future → distilled compact future → online reward | `online/offline` is too coarse; predictive knowledge can change model form across stages. |
| WD-D13 | **Consequence explicitness / observability** | opaque distilled latent online; explicit video not generated | Structured/decoded and opaque future consequences have different verification properties. |
| WD-D14 | **Teacher/student model-class mismatch** | heavy diffusion teacher vs lightweight query-decoder student | Training and deployment can instantiate “the future model” differently. |
| WD-D15 | **Future information bottleneck** | learnable Future Scene Queries | Distillation can intentionally preserve planning-relevant future information rather than full visual detail. |
| WD-D16 | **World-model vs scorer attribution** | trajectory-only rewarder 86.9→87.0; future feature 87.0→88.1 | Strong matched evidence that future feature adds beyond an extra scorer. |
| WD-D17 | **Generic prior vs WM-specific attribution** | 31.4→84.9 generic VAE; 84.9→86.9 TA-DWM-specific | Prevents monolithic `WM gain` claims. |
| WD-D18 | **Offline/online compute allocation** | expensive teacher offline; FAR online | Real-time deployment can still depend on costly offline world modeling. |
| WD-D19 | **Distillation objective semantics** | latent alignment + Bradley-Terry ranking | Student jointly learns future representation and decision preference. |
| WD-D20 | **Future information as causal decision variable** | distilled candidate future directly affects final argmax | Unlike LAW/Epona, future representation survives into action selection. |
| WD-D21 | **Future fidelity→decision evidence** | not directly isolated | Generation quality and planning usefulness remain separate hypotheses. |
| WD-D22 | **Action-support extrapolation** | TA-DWM learned mainly from logged/expert trajectories, then queried with planner alternatives | Candidate-conditioned generation may operate out of supervised action support. |
| WD-D23 | **Counterfactual supervision gap** | candidate future targets are teacher-generated, not matched real alternative futures | Multi-branch imagination is not intervention ground truth. |
| WD-D24 | **Coarse-to-fine utility computation** | base imitation/simulation scores → future-aware re-ranking | Final utility can be composed across multiple stages. |
| WD-D25 | **Deployment future-object type** | distilled latent surrogate | Separate from BEV rollout, decoded video, direct policy state and training-only target. |

---

# 3. Future-knowledge lifecycle — emerging major axis

The four anchors now expose four qualitatively different lifecycle patterns:

```text
LAW
future predictor used for auxiliary training
→ predicted future not consumed by deployed selection

Epona
visual future branch jointly trains shared history latent
→ visual branch can be disabled for planning
→ direct TrajDiT policy remains

WoTE
compact candidate-conditioned world transition is trained
→ same learned consequence model remains online
→ recurrent future BEV → reward → selection

WorldDrive
heavy candidate-conditioned generative WM is trained
→ used as frozen future teacher
→ distilled into lightweight candidate-conditioned future surrogate
→ surrogate future → reward → selection online
```

This axis should almost certainly survive into ontology v1.

Candidate labels for the stable dimension:

```text
future knowledge lifecycle
predictive knowledge deployment path
teacher→student foresight transformation
```

Do not freeze the final name until World4Drive is projected.

---

# 4. Consequence teacher vs value teacher — emerging major split

WoTE already showed that state truth and value truth are different. WorldDrive makes the split sharper:

```text
WorldDrive consequence teacher = frozen TA-DWM
WorldDrive value teacher       = PDMS/oracle preference
```

Therefore a future-aware planner should be audited as two learned problems:

```text
1. What happens under candidate a?
2. How good is that consequence?
```

and two possibly different supervision systems:

```text
consequence supervision source
value supervision source
```

A method may have excellent consequence distillation but poor utility semantics, or vice versa.

---

# 5. Attribution ladder — emerging mandatory evidence format

For WAM planning claims, record incremental evidence in the actual causal chain rather than headline SOTA.

WorldDrive provides the clearest example so far:

```text
No pretrain                              31.4
+ generic CogVideoX 3D VAE              84.9
+ TA-DWM vision                          85.8
+ TA-DWM motion                          86.9
+ trajectory-only extra rewarder         87.0
+ distilled future feature               88.1
```

This motivates a mandatory ontology/evidence field:

> **What is the strongest matched control immediately before the claimed WAM mechanism is added?**

For WorldDrive, the relevant controls differ by claim:

```text
representation-learning claim:
84.9 → 85.8 → 86.9

future-aware ranking claim:
86.9 → 87.0 → 88.1
```

The `31.4 → 88.1` headline delta is not a valid single-mechanism effect size.

---

# 6. Four-anchor provisional mechanism map

| Axis | LAW | WoTE | Epona | WorldDrive |
|---|---|---|---|---|
| future's main role | auxiliary representation shaping | online consequence model | joint representation shaping; visual simulator sibling | representation inheritance + distilled online consequence |
| planner action mechanism | conventional waypoint head | candidate bank + reward selection | direct diffusion/flow policy | candidate bank + coarse score + FAR re-rank |
| explicit candidates | no | yes | no scored bank | yes, 256→top-K |
| deployed future object | none consumed | recurrent BEV futures | no visual future required for planning | distilled candidate future latent |
| heavy generative visual model online | no | no | optional/off in planning | no |
| consequence/value separation | N/A | explicit | N/A in planning path | explicit after distillation |
| representation transfer | no separate stage | not primary | joint shared latent | explicit frozen WM→planner transfer |
| consequence truth/teacher | factual future latent | simulated/semantic BEV targets | observed future visual target | learned TA-DWM teacher |
| value truth/teacher | N/A | imitation + simulator rules | trajectory data distribution | PDMS preference + base imitation/simulation |
| strongest matched evidence | ± latent task/action | evaluator ± future | trajectory-only vs joint training | pretrain ladder + rewarder ladder |
| main unresolved causal issue | representation semantics | reactive counterfactual validity | what visual task teaches planning | teacher feature usefulness vs physically correct dynamics |

---

# 7. What World4Drive must now test

World4Drive is the fifth anchor before ontology freeze. It should challenge the current system on at least:

```text
1. Does future prediction remain online directly, or is any part distilled/removed?
2. Are K candidate futures outputs of one shared predictor or independent branches?
3. How are candidate trajectories generated and how much of performance is candidate support?
4. What is the exact future target: one factual latent, K simulated futures, teacher futures, or something else?
5. Does ScoreNet value physical consequence or merely classify which predicted latent matches the factual future?
6. Is consequence truth separate from value truth?
7. Does its candidate-conditioned output exceed its counterfactual supervision level?
8. What is the representation origin stack: foundation priors vs WM-specific learning?
9. Is there explicit coarse-to-fine pruning?
10. How does its online compact latent foresight compare with WoTE's recurrent BEV and WorldDrive's distilled surrogate?
11. Which existing dimensions collapse/merge after five anchors?
12. Which dimensions remain orthogonal enough for ontology v1?
```

Stop condition after World4Drive:

```text
merge/split provisional dimensions
→ WAM_DIMENSION_ONTOLOGY_V1.md
→ WAM_COMPARISON_MATRIX_V1.md
```
