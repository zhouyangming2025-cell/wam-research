# P0009 DriveLaW — Ontology V1 + V1.1 + V1.2 + V1.3 Projection

Last updated: 2026-09-15

Status: **FULL DIMENSION-FIRST PROJECTION — COMPLETE FIRST PASS**

Canonical analysis:

```text
papers/deep_analysis/P0009_DRIVELAW_DEEP_ANALYSIS_V2.md
audits/literature/PHASE_C6_DRIVELAW_AUDIT.md
```

Coordinate system:

```text
WAM_DIMENSION_ONTOLOGY_V1.md
+ WAM_DIMENSION_ONTOLOGY_V1_1_AMENDMENT.md
+ WAM_DIMENSION_ONTOLOGY_V1_2_AMENDMENT.md
+ WAM_DIMENSION_ONTOLOGY_V1_3_AMENDMENT.md
```

Method-version scope:

```text
arXiv:2512.23421v3 — 2026-04-17
CVPR 2026
official repo xiaomi-research/drivelaw
main commit audited 243e0e41148bdb1ae39ce1adf17d026e7cbd4348
```

Core warning:

```text
online Video-DiT internal representation
!= full online future-video rollout

predictive/generative representation conditioning
!= candidate-specific consequence evaluation
```

---

# A. Problem and role of world knowledge

| ID | DriveLaW value | Evidence / interpretation |
|---|---|---|
| A01 | **planning representation quality / stronger coupling between generative world prior and direct trajectory policy** | The paper targets the disconnect between video-generation knowledge and planner state. |
| A02 | **online generative/predictive representation provider + large-scale pretraining prior** | World knowledge is directly consumed by Action DiT at deployment. |
| A03 | **direct diffusion/flow trajectory policy** | No canonical candidate bank + reward/scorer selection is required. |
| A04 | **video-foundation representation transfer → online latent policy conditioning** | Historically closer to predictive/generative representation learning than model-based search. |

---

# B. Observation and current-state representation

| ID | DriveLaW value | Evidence / interpretation |
|---|---|---|
| B01 | **front-view camera history + ego velocity/acceleration + high-level route command; text prompt derived from motion/context** | Paper planning path is camera-centric; video pretraining also uses nuScenes/nuPlan videos. |
| B02 | **4 historical camera frames for planning task adaptation/inference** | Paper states past four camera frames and 4-s trajectory target. |
| B03 | **spatiotemporal VAE latent/noise canvas processed by Video DiT; planner consumes Video-DiT block hidden states** | Raw VAE latent and planning representation are not identical. |
| B04 | **implicit appearance/semantics/motion/physical-prior representation, spatial-temporal latent tokens** | No explicit object/occupancy/risk semantics are decoded for planning. |
| B05 | **history-conditioned generative state with unobserved future noise slots; no completed future required** | Sits between pure current-state encoding and explicit predicted-future consumption. |

---

# C. Representation provenance and imported priors

| ID | DriveLaW value | Evidence / interpretation |
|---|---|---|
| C01 | **LTX-Video foundation initialization + large-scale driving-video pretraining** | Strong imported video-generation prior. |
| C02 | **initialization + two-stage driving-video generative pretraining + online hidden-state reuse** | Prior enters through the Video DiT itself, not only pseudo labels. |
| C03 | **VAE/text encoder effectively feature providers; Video DiT task-adapted in stage 3 under `action_full`** | Source verifies all diffusion-model params trainable in action_full. |
| C04 | **PARTIALLY ISOLATED** | Video PT scale 0→76k→3.8M→7.6M gives 85.9→87.0→87.8→89.1 PDMS; still confounds representation quality with data exposure. |

---

# D. Action, intention and candidate space

| ID | DriveLaW value | Evidence / interpretation |
|---|---|---|
| D01 | **direct policy action initialized from Gaussian noise; supervised by expert/logged trajectory** | No planner proposal bank precedes world reasoning. |
| D02 | **continuous sequence of `(x,y,heading)` trajectory points, normalized, embedded as action tokens** | Source action input channels = 3. |
| D03 | **high-level command one-hot + ego velocity/acceleration condition action generation** | Command is separate from world hidden-state carrier. |
| D04 | **NO explicit canonical candidate bank** | Direct generative trajectory policy. |
| D05 | **NOT APPLICABLE as a scored candidate set** | Multiple stochastic samples are possible in principle but paper path reports direct policy, not explicit N-way support evaluation. |
| D06 | **iterative action-flow refinement; no candidate pruning stage** | Refinement occurs in solver space rather than proposal-selection pipeline. |

---

# E. Action → world coupling

| ID | DriveLaW value | Evidence / interpretation |
|---|---|---|
| E01 | **ABSENT in canonical planning path** | Video/world representation is computed before final trajectory and is not conditioned on the candidate action. |
| E02 | **NOT APPLICABLE for action→world; world→action uses blockwise cross-attention** | Avoid calling route/ego prompt an action-conditioned consequence model. |
| E03 | **single shared world/generative representation for direct action generation** | No per-candidate world branches. |
| E04 | **NO action-conditioned branch persistence** | No consequence tree/branch rollout. |
| E05 | **NOT APPLICABLE to candidate-world extrapolation** | There is no per-candidate consequence query. |

---

# F. Dynamics and future temporal modeling

| ID | DriveLaW value | Evidence / interpretation |
|---|---|---|
| F01 | **video latent / Video-DiT hidden-state substrate; RGB future available in video mode but not required in planning mode** | Planner taps internal generative state. |
| F02 | **implicit spatiotemporal/generative world prior rather than explicit metric future state** | Planning semantics are learned through video pretraining + action adaptation. |
| F03 | **spatiotemporal VAE + Video DiT / flow-style denoising; Action DiT flow policy** | Two generative operators coexist. |
| F04 | **video generation models a future clip jointly in latent space; deployed planner executes only first video denoise iteration, while action trajectory is refined in action solver** | Do not equate solver iterations with physical rollout. |
| F05 | **video training includes long-horizon clips; planning target = next 4 s at 2 Hz; planner does not consume a physical intermediate future sequence explicitly** | World horizon and action horizon should remain distinct. |
| F06 | **stochastic video/action generative noise; no calibrated world uncertainty or explicit multimodal future probabilities** | Generative stochasticity ≠ calibrated predictive uncertainty. |
| **F07** | **history-conditioned generation toward unseen future slots; chronological future generation rather than same-window JEPA masking** | Predictive geometry is history→future generative, although planning taps an early hidden state. |
| **F08** | **two solver coordinates: video denoising and action flow; neither equals physical future time** | Table-6 step 1/5/10 is solver depth, not future horizon. |

---

# G. Future supervision and truth sources

| ID | DriveLaW value | Evidence / interpretation |
|---|---|---|
| G01 | **video pretraining: factual driving-video clips; planning stage: expert trajectory target** | Stage-3 canonical action config does not require a separate factual future-video loss. |
| G02 | **VAE/text encoders provide representation; no EMA target encoder central to paper method** | EMA is optional in released planner training and not the core future target mechanism. |
| G03 | **logged factual videos for generative pretraining; logged expert trajectory for planner** | No per-action alternative future truth. |
| G04 | **NO utility/value teacher in canonical method** | Paper emphasizes no auxiliary scorer/post-training. |
| G05 | **expert trajectory flow-matching supervision** | Direct policy imitation remains the decision target. |
| G06 | **NO WTA/factual-mode assignment in canonical planner** | Unlike World4Drive/SeerDrive. |
| G07 | **NO candidate-specific consequence supervision** | One common world representation conditions direct action generation. |
| G08 | **reactive other-agent response truth NOT ESTABLISHED** | Video data and NAVSIM do not provide intervention truth for alternative ego actions. |

---

# H. Multimodal branch identity and assignment

| ID | DriveLaW value | Evidence / interpretation |
|---|---|---|
| H01 | **NOT APPLICABLE as explicit discrete action branches** | Action diffusion represents a continuous trajectory distribution. |
| H02 | **noise sample / route command can induce different policy samples, but no named branch identity in canonical evaluation** | Distinguish stochastic policy sampling from explicit intention modes. |
| H03 | **NO explicit branch assignment / WTA target** | Direct flow objective. |
| H04 | **NO best-of-N/oracle support ceiling reported for a candidate bank** | Candidate support is not the planning formulation. |

---

# I. Counterfactuality and reactivity

| ID | DriveLaW value | Evidence / interpretation |
|---|---|---|
| I01 | **NO candidate-specific world branching** | World hidden states are computed before trajectory output. |
| I02 | **NO alternative-action future targets** | Factual videos supervise generic video generation, not N action alternatives. |
| I03 | **NO intervention ground truth across hypothetical ego actions** | Not a counterfactual consequence model. |
| I04 | **NO validated reactive other-agent response under alternative ego actions** | NAVSIM remains non-reactive. |
| I05 | **ABSENT intervention-validity experiment** | High planning score does not establish causal world simulation. |

---

# J. World → planning interface

| ID | DriveLaW value | Evidence / interpretation |
|---|---|---|
| J01 | **online internal generative representation conditions direct trajectory generation** | Core paper mechanism. |
| J02 | **PARTIAL online future/generative computation: one Video-DiT denoising iteration; full future rollout absent** | Binary `future computed?` must be read with this nuance. |
| J03 | **YES: blockwise Video-DiT hidden states are consumed by Action-DiT cross-attention** | Source-verified direct online dependence. |
| J04 | **forward world→action; backward action-loss→world during `action_full`; no canonical action→world forward consequence path** | Source-verified gradient direction. |
| J05 | **direct generative trajectory policy** | No canonical scorer/argmax. |
| J06 | **world representation and policy are chained; consequence/value model distinction not applicable as explicit modules** | World state supports policy generation rather than explicit value prediction. |
| J07 | **training and inference both retain Video DiT + Action DiT, but objectives differ by stage** | Stage 1/2 video generation; stage 3/action inference direct policy. |
| **J08** | **video iteration 1 is a generative solver state; action iterations refine action at same decision instant** | Neither is ego/environment closed-loop iteration. |
| **J09** | **planner→world feedback carrier ABSENT** | No predicted trajectory is fed back into Video DiT in canonical path. |

---

# K. Scorer and decision semantics

| ID | DriveLaW value | Evidence / interpretation |
|---|---|---|
| K01 | **ABSENT canonical explicit scorer** | Source contains optional scorer code, but released paper/config path does not enable it. |
| K02 | **NOT APPLICABLE** | No scalar utility/risk/factual-mode score controls final selection. |
| K03 | **NOT APPLICABLE** | Action policy directly sees world hidden states rather than a scorer seeing future states. |
| K04 | **NO explicit decomposed utility objective** | Safety/compliance enter indirectly through demonstration distribution and benchmark. |
| K05 | **NO score-label teacher** | Direct action flow loss. |

---

# L. Training topology, jointness and gradient coupling

| ID | DriveLaW value | Evidence / interpretation |
|---|---|---|
| L01 | **three-stage progressive curriculum: video long-horizon → video high-resolution → trajectory task adaptation** | Sequential, not one joint multitask objective. |
| L02 | **planner directly consumes internal Video-DiT representations** | Representation interface is strong. |
| L03 | **separate Video-DiT blocks and Action-DiT blocks; no full parameter sharing between branches** | Chained ≠ same parameters. |
| L04 | **stage 3 `action_full`: action loss backpropagates through Action DiT into trainable Video DiT** | Forward world→action, backward action-loss→world. |
| L05 | **Video DiT retained at deployment; no distillation into planner-only weights** | Unlike Metis/DynFlowDrive removal. |
| L06 | **stage 3 action flow loss only in audited canonical training loop** | Video objective is not simultaneously optimized in stage 3. |
| **L07** | **NO world↔planner iterative-state supervision; action solver states supervised through flow objective, video hidden state tapped once** | Solver-state iteration is not physical-world supervision. |

---

# M. Future-knowledge lifecycle and deployment path

| ID | DriveLaW value | Evidence / interpretation |
|---|---|---|
| M01 | **video foundation prior → driving-video pretraining → action-task adaptation → online generative representation retained** | Canonical lifecycle. |
| M02 | **deployment object = internal Video-DiT hidden states from first denoising pass; not completed RGB future** | Important middle category between full rollout and no future object. |
| M03 | **heavy Video DiT retained online** | No teacher removal. |
| M04 | **no explicit distillation/compression into a lightweight future summary** | Cached hidden states amortize across action solver steps only. |
| M05 | **internal generative state inspectable only as latent/block activations; no explicit risk/value semantics** | Harder to interpret than explicit BEV/value models. |
| M06 | **planning mode skips full video rollout/decoder while keeping backbone active** | Distinct from Epona optional visual sibling and Metis action-only bypass. |

---

# N. Compute, pruning and latency

| ID | DriveLaW value | Evidence / interpretation |
|---|---|---|
| N01 | **~1 Video-DiT forward pass + K Action-DiT solver passes for planning** | Source caches video states after the first video iteration. |
| N02 | **2B Video DiT + 133M planner reported by paper** | Heavy generative backbone remains a deployment cost. |
| N03 | **full remaining video denoising and VAE RGB decode pruned in planning mode** | Large savings relative to actual video generation. |
| N04 | **blockwise cached video states reused across action iterations** | Compute sharing across action solver depth. |
| N05 | **paper does not provide a clean deployed latency decomposition isolating Video-DiT pass vs Action-DiT steps in the audited main text** | Avoid inventing real-time claims from PDMS alone. |
| N06 | **paper declares 5 action sampling steps; current main agent hard-codes 10 while config/validation say 5** | Reproduction/version mismatch. |

---

# O. Evaluation regime and evidence attribution

| ID | DriveLaW value | Evidence / interpretation |
|---|---|---|
| O01 | **nuScenes video generation + NAVSIM v1 non-reactive data-driven/pseudo-simulation planning + nuScenes open-loop trajectory metrics** | Do not accept paper's `closed-loop` NAVSIM wording as reactive closed loop. |
| O02 | **FID/FVD for video; PDMS and trajectory metrics for planning** | Two evaluation families remain distinct. |
| O03 | **no candidate-specific intervention evaluation** | Planning benchmark does not test counterfactual world reactions. |
| O04 | **strongest matched planning controls: video PT scaling; BEV/VLM/video representation; video denoise step** | More informative than headline SOTA comparisons. |
| O05 | **video fidelity→planning monotonicity NOT ESTABLISHED** | Step-10 denoising collapse actively warns against this assumption. |
| O06 | **cross-method headline comparisons confounded by sensors/backbones/pretraining/objectives** | Use matched internal ablations first. |
| O07 | **Noise Reinjection planning contribution NOT EVALUATED cleanly** | Video-quality mechanism should not be credited for PDMS without isolation. |
| O08 | **official source available and core inference/training path audited; exact paper benchmark commit not pinned** | High source confidence with a reproduction-version caveat. |

---

# P. Safety, uncertainty, interaction and physical validity

| ID | DriveLaW value | Evidence / interpretation |
|---|---|---|
| P01 | **ABSENT explicit risk/safety world state** | World hidden states are generic generative features. |
| P02 | **NO explicit safety utility/reward head** | Safety reflected indirectly in learned policy and PDMS. |
| P03 | **stochastic generation but NO calibrated uncertainty** | Noise sampling is not uncertainty calibration. |
| P04 | **multi-agent appearance/dynamics implicitly represented in video latent; no validated reactive action-conditioned agent response** | Representation richness ≠ causal interaction model. |
| P05 | **video generative prior encourages physical/temporal coherence, but no explicit kinematic/causal law in planner interface** | Do not call generative consistency verified physics. |
| P06 | **full world rollout drift is largely avoided at planning time because only one video denoise pass is used** | Planning robustness does not establish long-horizon world rollout robustness. |
| P07 | **traffic rules/legality implicit in data/prompt/representation; no explicit rule state or reward** | PDMS compliance metrics are evaluation, not world-state semantics. |

---

# Final normalized identity

```text
DriveLaW
=
video-generative foundation initialization
→ driving-video generative pretraining
→ online first-pass Video-DiT block hidden states
→ blockwise Action-DiT cross-attention
→ direct action-flow trajectory policy

STAGE-3 BACKWARD FLOW:
action loss → Action DiT → Video DiT

DEPLOYMENT:
Video DiT remains active for one pass
full video rollout / RGB decode absent
explicit candidate consequence scorer absent
```

Primary ontology identity:

```text
A02  online generative representation provider
E01  action→world absent
F08  dual solver clocks ≠ physical time
I01  no candidate-specific world branching
J02  partial online generative computation
J03  direct consumption of blockwise Video-DiT hidden states
J04  forward world→action / backward action-loss→world
J05  direct policy
L04  action_full task-adapts Video DiT
M02  early internal generative state survives as deployment object
N01  one Video pass + K Action passes
O04  matched evidence from PT scale / representation / tap step
```

Canonical subtype:

```text
ONLINE GENERATIVE-LATENT DIRECT-POLICY WAM
```

Ontology decision:

```text
V1.3 RETAINED
candidate residue: generative-state tap location / solver-depth of policy condition
no V1.4 amendment yet
```
