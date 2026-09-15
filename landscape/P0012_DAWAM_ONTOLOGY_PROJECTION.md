# P0012 DA-WAM — Ontology V1 + V1.1 + V1.2 + V1.3 Projection

Last updated: 2026-09-15

Status: **FULL DIMENSION-FIRST PROJECTION — COMPLETE FIRST PASS**

Canonical analysis:

```text
papers/deep_analysis/P0012_DAWAM_DEEP_ANALYSIS_V2.md
audits/literature/PHASE_C6_DAWAM_AUDIT.md
```

Coordinate system:

```text
WAM_DIMENSION_ONTOLOGY_V1.md
+ V1.1
+ V1.2
+ V1.3
```

Method-version scope:

```text
arXiv:2608.19085v2
official repo LeapWM/da-wam
latest observed commit 1edbe555146a2d1fe9484f5c11f120860b8a4858
implementation unavailable as of 2026-09-15
```

Core warning:

```text
candidate-specific future latent
!= candidate-specific factual/counterfactual future truth
```

---

# A. Problem and role of world knowledge

| ID | DA-WAM value | Evidence / interpretation |
|---|---|---|
| A01 | **candidate discrimination / prediction–action alignment** | Targets the mismatch between one/shared future representation and multiple action candidates. |
| A02 | **online candidate-specific consequence feature + explicit utility support** | Predicted future latent directly enters candidate scorer online. |
| A03 | **candidate proposal + factorized scorer + argmax** | 32 trajectories are proposed before future modeling. |
| A04 | **JEPA predictive representation + action-conditioned latent consequence + learned trajectory scoring** | Closest historical lineages: Drive-JEPA/LAW predictive representation, WoTE/World4Drive future-aware selection, GTRS/ZTRS trajectory scoring. |

---

# B. Observation and current-state representation

| ID | DA-WAM value | Evidence / interpretation |
|---|---|---|
| B01 | **front-camera visual input** | Reported NAVSIM setup is camera-only. |
| B02 | **two historical front-camera frames** | Distinct from single-frame current state and long autoregressive histories. |
| B03 | **V-JEPA 2.1 spatial scene tokens Z_t** | M tokens × D features. |
| B04 | **semantic/spatiotemporal predictive representation adapted for planning** | No explicit decoded objects/occupancy/risk field. |
| B05 | **planner consumes both current Z_t and predicted future Zhat_i** | Future latent is explicitly online in scorer. |

---

# C. Representation provenance and imported priors

| ID | DA-WAM value | Evidence / interpretation |
|---|---|---|
| C01 | **pretrained V-JEPA 2.1** | Strong imported video self-supervised prior. |
| C02 | **initialization + dense JEPA future target + LoRA adaptation** | Prior is adapted rather than used only frozen. |
| C03 | **base encoder frozen; selected LoRA parameters trainable; EMA target updated from online encoder** | Paper-level architecture; exact source implementation unavailable. |
| C04 | **PARTIALLY ISOLATED** | Table 4 separates frozen/LoRA/full-FT, dense/non-dense, and target policies; final system still bundles these with scorer/future predictor. |

---

# D. Action, intention and candidate space

| ID | DA-WAM value | Evidence / interpretation |
|---|---|---|
| D01 | **proposal-module-generated trajectory candidates** | 32 candidates before world prediction. |
| D02 | **8 future ego poses → trajectory encoder E_tau → action embedding a_i** | Position/heading sequence. |
| D03 | **no central semantic intention-mode variable reported** | Candidate diversity comes from proposal module, not explicit left/right intent branches. |
| D04 | **explicit multimodal proposal bank** | N=32 final configuration. |
| D05 | **1/8/16/32/64 ablation; saturation around 32** | Candidate breadth materially affects PDMS. |
| D06 | **candidate generation is separate from world predictor; hard negatives are appended during training** | No world-based online candidate pruning described. |

---

# E. Action → world coupling

| ID | DA-WAM value | Evidence / interpretation |
|---|---|---|
| E01 | **PRESENT online: every candidate action conditions its own future latent** | Core mechanism. |
| E02 | **trajectory embedding is query; current scene tokens are key/value in shared predictor** | Explicit cross-attention-style action→world injection. |
| E03 | **shared predictor parameters across all candidates** | Branch difference comes from a_i, not independent models. |
| E04 | **endpoint-only branch persistence** | One 0.5s latent per candidate; no recurrent branch rollout. |
| E05 | **non-expert candidate actions are outside direct future-supervision support** | Their latent futures receive no observed alternative consequence target. |

---

# F. Dynamics and future temporal modeling

| ID | DA-WAM value | Evidence / interpretation |
|---|---|---|
| F01 | **compact V-JEPA future latent tokens** | No RGB reconstruction needed. |
| F02 | **planning-relevant scene consequence representation; physical semantics implicit** | Future latent is intended to encode action-specific scene evolution. |
| F03 | **shared attention-based predictor P_phi** | Exact depth/source architecture unavailable. |
| F04 | **single short-horizon endpoint** | No recurrent or autoregressive physical world rollout. |
| F05 | **0.5s future endpoint** | Planner trajectory itself contains eight future poses; world prediction horizon is shorter and must be kept separate. |
| F06 | **candidate multimodality, not calibrated world uncertainty** | 32 ego branches do not establish stochastic environment uncertainty. |
| F07 | **history/current observation + candidate trajectory → unseen factual future endpoint for expert branch** | Chronological future prediction, unlike same-window random-mask JEPA pretraining. |
| F08 | **no internal solver-time world path central to core predictor** | N/A for physical-time/solver-time confusion beyond ordinary network computation. |

---

# G. Future supervision and truth sources

| ID | DA-WAM value | Evidence / interpretation |
|---|---|---|
| G01 | **one factual observed future latent Z_{t+Δ}** | Derived from actual future frame via EMA target encoder. |
| G02 | **EMA target encoder + stop-gradient** | Slowly evolving target network. |
| G03 | **logged observed future only for executed expert trajectory** | Directly acknowledged by paper. |
| G04 | **simulation/rule-based planning-factor + utility targets for all candidates** | NC/DAC/EP/TTC/Comfort and scalar utility. |
| G05 | **expert trajectory used for branch matching; proposal planning supervision inherited from host planner** | Dense future target branch is chosen by ADE to expert. |
| G06 | **expert-matched candidate i_exp selected by minimum ADE** | Not best-future matching. |
| G07 | **dense future supervision on exactly one branch; factor/score/rank on all branches** | Core supervision-coverage asymmetry. |
| G08 | **reactive alternative-agent future truth NOT ESTABLISHED** | Candidate metric labels do not supply actual alternative visual/world trajectories. |

---

# H. Multimodal branch identity and assignment

| ID | DA-WAM value | Evidence / interpretation |
|---|---|---|
| H01 | **ego trajectory candidate** | Each branch is an action hypothesis. |
| H02 | **proposal-generated trajectory geometry** | No separate world-mode identity. |
| H03 | **factual branch assignment by minimum ADE to expert trajectory** | Important distinction from World4Drive future-latent nearest-mode matching. |
| H04 | **candidate-count saturation reported; oracle best-of-N ceiling not isolated** | Support vs ranking headroom remains partly unresolved. |

---

# I. Counterfactuality and reactivity

| ID | DA-WAM value | Evidence / interpretation |
|---|---|---|
| I01 | **YES candidate-specific future outputs** | 32 predicted latent futures. |
| I02 | **NO direct alternative-action future supervision** | Only expert-matched branch sees factual future latent. |
| I03 | **NO observed/simulated intervention world-state GT for each branch** | Metric targets are not full future-state targets. |
| I04 | **NO / NOT ESTABLISHED reactive other-agent response truth** | NAVSIM/logged setting does not provide branch-specific reactive future agents. |
| I05 | **ABSENT external intervention-validity validation** | Candidate-specific latent differentiation is not causal identification. |

---

# J. World → planning interface

| ID | DA-WAM value | Evidence / interpretation |
|---|---|---|
| J01 | **online candidate-specific future latent conditions utility scorer** | Future is directly decision-informative. |
| J02 | **YES online future computation** | Predictor runs for every candidate at inference. |
| J03 | **YES online future consumption** | Scorer receives Zhat_i. |
| J04 | **forward: action→future latent→score; backward: planning losses jointly shape predictor/online LoRA per paper** | Exact detach implementation SOURCE-UNVERIFIED. |
| J05 | **factorized utility score → argmax** | Explicit selection mechanism. |
| J06 | **consequence feature and decision model are distinct but jointly trained** | Predictor ≠ scorer. |
| J07 | **training removes target/hard-negative machinery at inference but retains future predictor** | Lifecycle change is partial, not removal of WM. |
| J08 | **no iterative world↔planner co-refinement reported** | Candidate predictor/scorer are feed-forward endpoint operations. |
| J09 | **candidate trajectory embedding a_i is planner→world carrier** | Direct candidate→future interface. |

---

# K. Scorer and decision semantics

| ID | DA-WAM value | Evidence / interpretation |
|---|---|---|
| K01 | **explicit shared factorized scorer** | One scorer applied across candidates. |
| K02 | **utility / safety / compliance / progress semantics** | NC, DAC, EP, TTC, Comfort. |
| K03 | **scorer sees current state + trajectory embedding + candidate-specific predicted future** | Future is not merely training-only. |
| K04 | **factor heads + learned utility head** | Explicit decomposition. |
| K05 | **external metric-derived factor/utility targets + pairwise ranking** | Hard negatives are oversampled/upweighted around safety boundary. |

---

# L. Training topology, jointness and gradient coupling

| ID | DA-WAM value | Evidence / interpretation |
|---|---|---|
| L01 | **joint end-to-end planner/world/scorer optimization on composite loss** | Predictive and planning objectives coexist. |
| L02 | **shared online scene representation across proposal/future/scoring pipeline** | Z_t feeds predictor and scorer. |
| L03 | **separate online encoder, EMA target, predictor, trajectory encoder and scorer modules** | Not monolithic parameter sharing. |
| L04 | **paper states LoRA jointly updated by future prediction + planning gradients; other predictor/scorer gradient routes implied by composite objective** | Exact implementation detach boundaries unavailable. |
| L05 | **EMA target removed; online predictor/scorer retained** | Partial lifecycle pruning. |
| L06 | **L_pred + L_factor + L_score + L_rank** | Final gains are multi-objective. |
| L07 | **NOT APPLICABLE to iterative world state supervision** | One endpoint future target, not repeated refinement states. |

---

# M. Future-knowledge lifecycle and deployment path

| ID | DA-WAM value | Evidence / interpretation |
|---|---|---|
| M01 | **pretrained JEPA prior → joint predictive/planning adaptation → online future predictor retained** | Distinct from training-only predictive branches. |
| M02 | **candidate-specific compact future latent online** | No RGB/video generation. |
| M03 | **EMA target/prior-supervision machinery removed; online encoder/predictor/scorer retained** | Model class remains explicitly future-aware. |
| M04 | **no separate distillation/compression stage reported** | Future object is already compact. |
| M05 | **inspectable per-candidate future latent exists online, though semantics are not fully identifiable** | Stronger auditability than pure policy-weight distillation. |
| M06 | **single deployed candidate-evaluation mode** | No optional simulation sibling described. |

---

# N. Compute, pruning and latency

| ID | DA-WAM value | Evidence / interpretation |
|---|---|---|
| N01 | **32 online candidates × one 0.5s future latent each** | Main deployed branching cost. |
| N02 | **V-JEPA encoder + shared predictor + scorer; target branch absent** | No video decoder/generative rollout. |
| N03 | **EMA target and hard-negative machinery pruned at deployment** | Future predictor is not pruned. |
| N04 | **candidate computation likely batchable; exact source implementation unavailable** | Do not invent parallelization details. |
| N05 | **runtime/FPS not established in audited text** | NOT REPORTED here. |
| N06 | **candidate count 32 chosen after saturation at 32/64** | Compute/quality trade-off indirectly visible. |

---

# O. Evaluation regime and evidence attribution

| ID | DA-WAM value | Evidence / interpretation |
|---|---|---|
| O01 | **NAVSIM-v1/v2 non-reactive data-driven pseudo-simulation planning** | Not reactive closed-loop world validation. |
| O02 | **no independent quantitative future-latent physical fidelity metric identified** | Planning score is main evidence. |
| O03 | **one factual logged future target + metric-derived candidate labels** | Alternative branch future truth remains missing. |
| O04 | **No Future 93.31 → Action-conditioned 93.46** | Strongest matched incremental world/future control. |
| O05 | **Shared Global 92.81 → Action-conditioned 93.46** | Strong evidence that proposal-invariant future can hurt. |
| O06 | **Hard-negative 93.46 → 93.68** | Value/safety supervision contributes materially. |
| O07 | **Table 4 separates dense objective / adaptation / target policy** | Representation attribution relatively strong. |
| O08 | **official repo exists but implementation not released** | Source certainty lower than paper certainty. |

---

# P. Safety, uncertainty, interaction and physical validity

| ID | DA-WAM value | Evidence / interpretation |
|---|---|---|
| P01 | **NO explicit risk field/state** | Future latent remains implicit. |
| P02 | **YES explicit safety/value factors** | NC/DAC/TTC plus utility scorer. |
| P03 | **NO calibrated uncertainty distribution** | Candidate multiplicity ≠ calibrated world uncertainty. |
| P04 | **implicit scene interaction in visual latent; no validated reactive candidate-conditioned agent dynamics** | Safety labels do not identify response trajectories. |
| P05 | **trajectory-conditioned short future latent; no explicit causal/kinematic dynamics law** | Physical validity not independently measured. |
| P06 | **no recursive world rollout drift evaluated** | Endpoint prediction only. |
| P07 | **rule/compliance semantics explicitly enter factor supervision** | Stronger explicit decision semantics than purely latent scorers. |

---

# Final normalized identity

```text
DA-WAM
=
2-frame front-camera input
→ V-JEPA 2.1 online encoder + LoRA
→ current scene tokens
→ 32 proposal trajectories
→ per-trajectory action query
→ shared 0.5s future-latent predictor
→ one future latent per candidate
→ current/action/future factorized scorer
→ NC/DAC/EP/TTC/Comfort + utility
→ argmax

TRAINING TRUTH:
only expert-matched branch receives direct factual future-latent supervision;
all candidates receive factor/value/ranking targets;
hard negatives are value/safety labels, not observed future worlds.
```

Primary ontology identity:

```text
E01 candidate action→future coupling YES
F04 endpoint-only future
G01 one factual future
G07 one-branch direct future supervision / all-branch decision supervision
I01 candidate-specific outputs YES
I02 candidate-specific factual alternatives NO
J02/J03 online future computation + consumption YES
K02 explicit factorized utility semantics
M02 compact per-candidate future latent online
O04 no-future→action-future matched gain +0.15 PDMS
```

Ontology decision:

```text
V1.3 RETAINED
NO V1.4
```
