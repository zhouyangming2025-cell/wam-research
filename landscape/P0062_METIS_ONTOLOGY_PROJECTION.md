# P0062 Metis — Ontology V1 + V1.1 + V1.2 Projection

Last updated: 2026-09-15

Status: **FULL DIMENSION-FIRST PROJECTION — COMPLETE FIRST PASS**

Canonical analysis:

```text
papers/deep_analysis/P0062_METIS_DEEP_ANALYSIS_V2.md
audits/literature/PHASE_C5_METIS_AUDIT.md
```

Coordinate system:

```text
WAM_DIMENSION_ONTOLOGY_V1.md
+ WAM_DIMENSION_ONTOLOGY_V1_1_AMENDMENT.md
+ WAM_DIMENSION_ONTOLOGY_V1_2_AMENDMENT.md
```

Method-version scope:

```text
arXiv:2606.15869 v1
official repo LogosRoboticsGroup/Metis
latest observed public commit 7677b62d786cff8bb2044b489bd41f3d59514b43
implementation code unavailable as of 2026-09-15
```

Core warning:

```text
joint world-action training
!= online world→action future consumption
```

---

# A. Problem and role of world knowledge

| ID | Metis value | Evidence / interpretation |
|---|---|---|
| A01 | **inference efficiency + heterogeneous world/action representation interference + generalization** | Metis targets the cost/noise of explicit future generation while retaining world-task training benefits. |
| A02 | **training-time world-task gradient shaping / imported video-world prior** | Future-video generation serves as auxiliary world supervision; no explicit future is consumed by deployed planner. |
| A03 | **direct generative action-chunk policy** | AE performs flow/diffusion denoising directly to an action trajectory; no fixed candidate bank or future-based scorer. |
| A04 | **training-only WAM co-training / decoupled inference lineage** | Historically close to Fast-WAM-style “world training without test-time imagination”; Metis adds MoT + asymmetric attention. |

---

# B. Observation and current-state representation

| ID | Metis value | Evidence / interpretation |
|---|---|---|
| B01 | **single front RGB + language instruction + ego/agent state** | Reported AD setting uses front camera only; language and ego state condition planning. |
| B02 | **current observation in formal planning formulation** | Paper writes `o_t`; no deployed chronological future context. Do not confuse training future video with observation history. |
| B03 | **video/VAE current-observation latent + action-expert hidden tokens** | VGE provides pretrained visual substrate; AE has separate low-dimensional action representation. |
| B04 | **high-dimensional visual/spatiotemporal prior + planning-conditioned action latent** | Exact physical semantics are implicit rather than explicit BEV/object state. |
| B05 | **current/context representation only at deployment; future video only during training** | Central lifecycle distinction. |

---

# C. Representation provenance and imported priors

| ID | Metis value | Evidence / interpretation |
|---|---|---|
| C01 | **Wan2.2 pretrained video-generation prior + video VAE + T5 text encoder** | Large foundation prior is a major representation source before task-specific WAM training. |
| C02 | **pretrained initialization/components + joint task-specific flow training** | Imported visual/world prior is adapted through Metis co-training. |
| C03 | **paper says VGE and AE jointly optimized; exact freeze/train policy SOURCE-UNVERIFIED** | Code is unreleased; do not infer layer-level ownership. |
| C04 | **partially isolated only** | VGE/AE capacity ablation exists, but rows change model capacity and reported VGE labels are internally inconsistent (5B main text vs 14B ablation labels). |

---

# D. Action, intention and candidate space

| ID | Metis value | Evidence / interpretation |
|---|---|---|
| D01 | **online action chunk sampled/denoised by AE from current context** | Training target is logged factual trajectory; world branch is conditioned on predicted/future action representation. |
| D02 | **NAVSIM: 8 waypoints `(x,y,heading)`, 4 s, 0.5 s interval; CityWalker: 5 `(x,y)` waypoints** | Direct continuous trajectory representation. |
| D03 | **language instruction + ego state; no discrete intention bank required** | High-level route/instruction enters conditioning rather than defining K future modes. |
| D04 | **NO explicit finite candidate bank** | Flow policy can be sampled stochastically; best-of-6 is an evaluation/sampling strategy, not an architectural K-candidate bank. |
| D05 | **continuous/stochastic policy support; finite support not enumerated** | Multisample policy output != explicit candidate world branches. |
| D06 | **action denoising refinement via 1/2/5/10 steps; no candidate-pruning stage** | Iterative computation refines one sampled action representation rather than ranking a bank. |

---

# E. Action → world coupling

| ID | Metis value | Evidence / interpretation |
|---|---|---|
| E01 | **PRESENT during training; absent as deployed world transition** | Future-video prediction is conditioned on future/predicted action tokens. |
| E02 | **structured attention / token visibility: future-video tokens attend action tokens** | Action enters VGE through the asymmetric attention graph. |
| E03 | **shared VGE conditioned on action sequence; no K separately parameterized candidate worlds** | One factual training future per sample. |
| E04 | **fixed-window future-video/action chunk alignment; no deployed branch persistence** | Paper states 1:1 temporal alignment; future-video branch is bypassed online. |
| E05 | **trained on logged action/factual future support; alternative-action consequence extrapolation NOT VALIDATED** | Action-conditioning alone does not establish counterfactual validity. |

---

# F. Dynamics and future temporal modeling

| ID | Metis value | Evidence / interpretation |
|---|---|---|
| F01 | **future video latent / visual future** | VGE denoises future visual latents rather than explicit BEV/occupancy. |
| F02 | **appearance + learned spatiotemporal scene dynamics; interaction only implicitly represented** | Supervision is factual future video. |
| F03 | **pretrained video-generation Transformer under flow matching** | Future generation is generative latent denoising. |
| F04 | **fixed-window/chunk future latent generation via flow denoising** | Not a deployed autoregressive physical-time rollout. |
| F05 | **video and action chunks aligned 1:1; NAVSIM action horizon 4 s** | Exact visual future sampling granularity beyond the reported alignment should remain paper-scoped. |
| F06 | **stochastic/generative flow model; no calibrated predictive uncertainty** | Sampling diversity does not establish uncertainty calibration. |
| **F07** | **CURRENT-CONTEXT + ACTION → CHRONOLOGICALLY UNSEEN FUTURE VIDEO** | Unlike Drive-JEPA random-mask completion, the prediction obligation is future-directed. |

---

# G. Future supervision and truth sources

| ID | Metis value | Evidence / interpretation |
|---|---|---|
| G01 | **logged factual future video latent** | Future-world truth comes from the realized recorded sequence. |
| G02 | **VAE/video latent + flow-matching noise interpolation; no EMA target encoder described** | Distinct target-network semantics from JEPA. |
| G03 | **same-sequence factual future visual observation** | No learned teacher or alternative-action simulator truth. |
| G04 | **ABSENT explicit utility/value target** | No PDMS reward/scorer supervises planning inside model training. |
| G05 | **logged factual action chunk / imitation target** | AE flow matching learns direct policy trajectory. |
| G06 | **NOT APPLICABLE discrete branch assignment** | No WTA future-mode bank. |
| G07 | **dense joint action/video flow losses** | Both tasks receive direct training objectives; gradient routes differ because of mask. |
| G08 | **logged factual world evolution; reactive alternative-action truth NOT ESTABLISHED** | One realized future cannot validate many intervention futures. |

---

# H. Multimodal branch identity and assignment

| ID | Metis value | Evidence / interpretation |
|---|---|---|
| H01 | **continuous stochastic action sample, not named discrete future mode** | Flow policy can generate multiple samples but no fixed branch identity is defined. |
| H02 | **implicit through noise/sample trajectory** | No intention-query/world-mode bank. |
| H03 | **NOT APPLICABLE WTA/mode assignment** | Each training example has factual action/video targets. |
| H04 | **best-of-6 policy sampling reported; not a candidate-bank oracle decomposition** | Single-run vs best-of-6 gives a sampling ceiling, not scorer-selection headroom. |

---

# I. Counterfactuality and reactivity

| ID | Metis value | Evidence / interpretation |
|---|---|---|
| I01 | **action-conditioned future output exists during training/generation, but no K matched candidate-world bank** | The VGE can be conditioned on an action representation; paper does not establish exhaustive alternative branches. |
| I02 | **NO alternative-action factual consequence supervision** | Future target is one logged future. |
| I03 | **NO observed K-way counterfactual truth** | Generative controllability must not be upgraded to intervention evidence. |
| I04 | **reactive other-agent alternative truth NOT ESTABLISHED** | Pixels can encode interactions, but training does not provide observed responses to unexecuted ego alternatives. |
| I05 | **NO direct intervention-validity evidence** | Real-robot policy tests validate execution, not causal correctness of generated alternative futures. |

---

# J. World → planning interface

| ID | Metis value | Evidence / interpretation |
|---|---|---|
| J01 | **training-time world-loss/representation shaping** | World task affects planning through parameters/gradients rather than an explicit deployed consequence object. |
| J02 | **NO online predicted future object in action-only mode** | Core deployment design. |
| J03 | **NO online future consumption** | Action tokens are prevented from attending future-video tokens even during training. |
| J04 | **training forward: action→world; training backward: world-loss→action; inference: current context→action** | This directional decomposition is the central Metis mechanism. |
| J05 | **direct action-flow policy** | No future scorer, argmax, MPC or candidate evaluator. |
| J06 | **NO consequence→utility scorer** | Video generation is a training task, not a value model. |
| J07 | **joint training graph / action-only deployment graph; optional explicit video generation for analysis** | Task-mode/deployment graph changes across lifecycle. |
| **J08** | **GENERATIVE DENOISING ITERATION (action flow)** | More denoising steps refine action sample; physical future time does not advance one environment step per iteration. |
| **J09** | **TRAINING: action-token/action-chunk representation; DEPLOYMENT: NOT APPLICABLE** | Planner→world carrier exists only because action conditions VGE during co-training. |

---

# K. Scorer and decision semantics

| ID | Metis value | Evidence / interpretation |
|---|---|---|
| K01 | **ABSENT explicit scorer** | Direct action policy. |
| K02 | **NOT APPLICABLE** | No candidate utility/factual-mode score. |
| K03 | **NOT APPLICABLE** | No scorer input scope. |
| K04 | **NOT APPLICABLE** | Safety/progress/comfort are benchmark metrics, not internal reward decomposition. |
| K05 | **NOT APPLICABLE** | No learned ranking target. |

---

# L. Training topology, jointness and gradient coupling

| ID | Metis value | Evidence / interpretation |
|---|---|---|
| L01 | **joint co-training of VGE + AE under two flow losses** | Distinct from Drive-JEPA pretrain→planner staging. |
| L02 | **shared interaction latent/current-context representation, specialized expert states** | Paper explicitly says shared latent space while preserving task distributions. |
| L03 | **separate experts with expert-specific projections/FFNs/heads; no full parameter identity** | `joint` does not mean one monolithic Transformer. |
| L04 | **asymmetric gradients: action loss→AE; video loss→VGE and, through action-conditioned dependence, can shape AE** | Forward future-video→AE is masked; gradient coupling must be separated from attention direction. |
| L05 | **pretrained VGE prior → jointly task-trained; future-generation path bypassed at inference; exact freeze policy SOURCE-UNVERIFIED** | No teacher/student distillation. |
| L06 | **L_action + L_video, λ=1** | Joint-loss conflict/regularization remains a possible explanation for gains. |
| **L07** | **NOT APPLICABLE to internal world↔planner refinement** | Flow denoising is generative optimization, not SeerDrive-style iteration-indexed state supervision. |

---

# M. Future-knowledge lifecycle and deployment path

| ID | Metis value | Evidence / interpretation |
|---|---|---|
| M01 | **joint world/action co-training → training-only world-loss shaping → action-only deployment** | Canonical lifecycle class. |
| M02 | **NONE in primary action-only deployment** | No explicit future latent/video consumed online. |
| M03 | **video-generation computation active in training, bypassed for action deployment** | Knowledge changes from explicit future task to implicit policy parameters/current representation. |
| M04 | **implicit compression into weights/representation; no explicit distilled future summary** | Unlike WorldDrive. |
| M05 | **no inspectable deployed consequence object** | Future generation can be run separately, but not required for action path. |
| M06 | **YES — video-generation sibling/training branch is optional at action inference** | Similar broad optionality to Epona but different coupling direction. |

---

# N. Compute, pruning and latency

| ID | Metis value | Evidence / interpretation |
|---|---|---|
| N01 | **candidate breadth N/A; action denoising depth 1/2/5/10; deployed future-world depth = 0** | Denoising iterations must not be called world rollout horizon. |
| N02 | **large VGE training prior + ~1B AE; explicit video generation costly** | Exact deployed parameter execution needs released code. |
| N03 | **future-video path bypassed entirely before deployed action inference** | Strong deployment pruning at task-branch level. |
| N04 | **no K candidate parallelization; neural denoising over action chunk** | Best-of-N is external sampling/evaluation strategy. |
| N05 | **single RTX 4090 comparison: ~1.38 s with video vs ~0.17 s action-only operating point; README ~147 ms for 2-step action-only** | Video and action-only rows also differ in denoising steps, so not pure branch-removal timing. |
| N06 | **strong 1/2/5/10-step quality curve** | 2 steps recover most navtest quality; navhard benefits more from 10 steps. |

---

# O. Evaluation regime and evidence attribution

| ID | Metis value | Evidence / interpretation |
|---|---|---|
| O01 | **NAVSIM v1/v2 data-driven/non-reactive planning; CityWalker navigation; Unitree Go2 real-robot navigation closed loop** | Real robot is navigation, not real-car AD validation. |
| O02 | **qualitative future-video visualization; no dedicated quantitative world-fidelity metric identified** | Planning evidence cannot be converted into generation-fidelity evidence. |
| O03 | **logged factual future-video/action co-training vs NAVSIM planning evaluation; real robot evaluation separate** | Training supervision is not reactive counterfactual truth. |
| O04 | **w/o video co-train 87.9 EPDMS → w/co-train 89.5** | Strongest direct world-task planning control. |
| O05 | **co-training gain + matched attention topology + resolution + AE/VGE capacity + denoising-step ladder** | Mandatory decomposition; final 89.5 is not a monolithic “WM gain.” |
| O06 | **headline SOTA heterogeneous; input/model scale/training prior differ** | Use within-paper controls for causal claims. |
| O07 | **ABSENT direct future-video fidelity → planning relevance evidence** | No matched quantitative relation established. |
| O08 | **paper + official README audited; source implementation unavailable** | Latest public repo still lacks code/eval scripts as of 2026-09-15. |
| O09 | **single-sample vs best-of-6 sampling gap exists (e.g. navtest EPDMS 89.5→90.3), but not a fixed-candidate oracle-ranking gap** | Interpret as stochastic policy sampling headroom. |
| O10 | **see evidence boundary below** | Symmetric scientific conclusion required. |

O10 normalized evidence boundary:

```text
PROVES REASONABLY WELL:
future-video co-training + asymmetric coupling can improve the reported direct action policy while explicit video generation is unnecessary at deployment.

DOES NOT PROVE:
online imagination, future-video→action forward reasoning, better video fidelity→better planning, or intervention-valid alternative futures.

STRONGEST ALTERNATIVE EXPLANATION:
pretrained video prior + auxiliary generative regularization/gradient shaping + AE capacity + resolution + denoising compute explain a substantial portion of gains.
```

---

# P. Safety, uncertainty, interaction and physical validity

| ID | Metis value | Evidence / interpretation |
|---|---|---|
| P01 | **ABSENT explicit risk/safety future state** | Future video is not an explicit risk representation. |
| P02 | **ABSENT explicit internal safety/risk value head** | NAVSIM safety/compliance terms are evaluation metrics, not a learned scorer in Metis. |
| P03 | **stochastic flow samples; no calibrated uncertainty** | Sampling/best-of-N must not be called uncertainty calibration. |
| P04 | **implicit multi-agent interaction in video pixels/latents; action-conditioned VGE; no validated reactive alternative-agent model** | Rich visual dynamics != counterfactual behavior truth. |
| P05 | **video prior + factual action/video supervision; no explicit kinematic/world-physics constraint reported as core mechanism** | Plausibility comes largely from data/foundation model. |
| P06 | **no deployed recursive future-world consumption, hence no online world-rollout drift** | Action denoising iteration is not world temporal recursion. |
| P07 | **rules/compliance mainly visible through NAVSIM evaluation metrics** | High DAC/DDC does not prove explicit rule semantics in latent state. |

---

# Final normalized identity

```text
Metis
=
pretrained VGE + specialized AE

TRAINING:
current context → AE → future action representation
                    ↓ conditions
               future-video VGE
                    ↓ L_video
              gradient shapes AE

INFERENCE:
current context → AE flow denoising → trajectory
explicit future-video generation = NO
```

Primary ontology identity:

```text
A02  training-time world-loss shaping
E01  action-conditioned world prediction = YES during training
F07  current-context + action → unseen future video
J02  deployed future object = NONE
J03  online future consumption = NO
J04  forward action→world / backward world-loss→action
J05  direct action-flow policy
L04  asymmetric gradient coupling
M01  co-training → action-only deployment
M06  world-generation branch optional/bypassed at inference
O04  87.9→89.5 EPDMS co-training control
O07  future-fidelity→planning evidence ABSENT
```

Cross-paper position:

```text
Drive-JEPA  predictive pretrain → encoder transfer → predictor discarded
LAW         action-aware future latent auxiliary loss → planner shaping
Epona       shared F → trajectory + visual sibling generators
Metis       action→future-video forward / world-loss→AE backward → action-only deployment
WorldDrive  heavy future teacher → distilled online future surrogate
WoTE/W4D    predicted future remains online in action selection
```

---

# Ontology residue result

Metis does **not** require V1.3.

Its key directional asymmetry is already captured by the combination of:

```text
E01/E02
J04
L04
M01-M03
```

Therefore Ontology **V1.2 remains active** after the Metis stress test.
