# P0063 DynFlowDrive — Ontology V1 + V1.1 + V1.2 + V1.3 Projection

Last updated: 2026-09-15

Status: **FULL DIMENSION-FIRST PROJECTION — COMPLETE FIRST PASS**

Canonical analysis:

```text
papers/deep_analysis/P0063_DYNFLOWDRIVE_DEEP_ANALYSIS_V2.md
audits/literature/PHASE_C5_DYNFLOWDRIVE_AUDIT.md
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
arXiv:2603.19675v2
official repo xiaolul2/DynFlowDrive
latest observed public commit c665dc577a0939543fa7abe64d28eadaec28283c
implementation code unavailable as of 2026-09-15
```

Core warning:

```text
rectified-flow transport path
!= physically time-supervised continuous world evolution

training-time candidate-conditioned WM
!= online candidate-future evaluator
```

---

# A. Problem and role of world knowledge

| ID | DynFlowDrive value | Evidence / interpretation |
|---|---|---|
| A01 | **latent-dynamics modeling + multimodal candidate supervision/selection reliability** | The paper targets limitations of static next-latent regression and geometric-only candidate selection. |
| A02 | **training-time consequence model + mode-label/ranking teacher + predictive regularizer** | World dynamics create reconstruction/flow signals and help define the positive candidate during training; the WM is removed at deployment. |
| A03 | **multimodal candidate planner + learned score head** | Host planner proposes trajectories before world modeling; final deployed action is highest learned score. |
| A04 | **LAW/SSR predictive-latent lineage + World4Drive-like mode assignment + flow-matching dynamics + training-time teacher distillation into scorer** | New terminology must be read against predictive auxiliary training and multimodal positive-mode selection predecessors. |

---

# B. Observation and current-state representation

| ID | DynFlowDrive value | Evidence / interpretation |
|---|---|---|
| B01 | **nuScenes: multi-view cameras + command; NAVSIM: combined front/front-left/front-right camera + LiDAR + command/context** | Sensor setting differs across benchmarks; this is a comparability confound. |
| B02 | **primarily current observation for the audited world-transition formulation** | The paper defines current `I_t` and next factual `I_{t+1}`; no long observation history is central to the flow formulation. |
| B03 | **planner scene queries + separate pretrained-VAE-derived world latent** | Planner representation and WM representation are related through cross-attention but not simply identical. |
| B04 | **implicit visual/spatial/context latent intended to be dynamics-aligned** | Geometry/interaction are not explicitly decoded as objects/occupancy in the core flow state. |
| B05 | **future latent exists during training only; deployment consumes current planner state only** | Critical lifecycle boundary. |

---

# C. Representation provenance and imported priors

| ID | DynFlowDrive value | Evidence / interpretation |
|---|---|---|
| C01 | **host planner backbone + pretrained VAE/foundation world encoder** | Flow dynamics do not operate on a representation learned from scratch. |
| C02 | **pretrained VAE latent → lightweight MLP → cross-attention with scene queries** | Imported prior is explicitly reprojected into a world latent. |
| C03 | **figure suggests frozen world/VAE encoder; exact trainability SOURCE-UNVERIFIED** | Public code is unavailable; snowflake icon is not enough for layer-level ownership claims. |
| C04 | **PARTIALLY ISOLATED** | Table 4: Static WM 0.61/0.30 → Flow WM 0.59/0.26 → + World Feat 0.57/0.22, separating dynamics parameterization from representation prior better than headline rows. |

---

# D. Action, intention and candidate space

| ID | DynFlowDrive value | Evidence / interpretation |
|---|---|---|
| D01 | **planner-generated/refined candidate trajectories; NAVSIM uses 256 anchors/modes** | World model does not generate the action space. |
| D02 | **BEV waypoint trajectory sequence → TrajEmb** | Full candidate trajectory is embedded as the dynamics condition. |
| D03 | **left / right / go-straight navigation commands in nuScenes setup** | Command provides high-level maneuver structure independently of world modeling. |
| D04 | **query-based multimodal trajectory proposals; NAVSIM N=256 anchors** | Candidate bank exists before flow WM. |
| D05 | **256 deployed candidates on NAVSIM; exact nuScenes mode count not clearly established in audited text** | Do not generalize 256 across datasets without evidence. |
| D06 | **trajectory-query refinement in host planner; no world-model-based online pruning** | Candidate support/refinement is a separate planner mechanism. |

---

# E. Action → world coupling

| ID | DynFlowDrive value | Evidence / interpretation |
|---|---|---|
| E01 | **PRESENT during training: candidate trajectory conditions future latent dynamics; ABSENT deployed WM coupling** | Training-only action-conditioned consequence model. |
| E02 | **Concat(current world latent, TrajEmb(candidate)) → flow condition `h_t^n`** | Direct trajectory-conditioning path. |
| E03 | **shared flow model with candidate-specific conditions** | N candidates do not mean N separately parameterized WMs. |
| E04 | **one physical `t→t+1` endpoint per candidate condition; internal flow path persists only in solver coordinate `s`** | Not a persistent multi-step physical rollout. |
| E05 | **alternative planner candidates extend beyond the one executed/logged action; consequence truth outside factual support is unobserved** | Candidate-conditioning does not establish intervention validity. |

---

# F. Dynamics and future temporal modeling

| ID | DynFlowDrive value | Evidence / interpretation |
|---|---|---|
| F01 | **VAE-derived compact latent world state** | Future prediction remains latent; no RGB reconstruction required for planner use. |
| F02 | **intended scene dynamics / transition representation; exact physical semantics implicit** | Supervision constrains a factual next latent, not explicit objects/risk/occupancy. |
| F03 | **Transformer-based rectified-flow velocity field** | Dynamics operator predicts `v_theta(x_s,s,h_t^n)`. |
| F04 | **one physical next-step endpoint + internal Euler/flow integration path** | Solver path should not be described as a sequence of observed future scenes. |
| F05 | **physical target = next factual timestep; default useful solver depth 5 in ablation; exact dataset physical Δt for WM transition not cleanly isolated in audited text** | Keep physical horizon and solver depth separate. |
| F06 | **stochastic noised anchor / flow process; no calibrated future uncertainty** | Candidate multimodality is policy/action diversity, not calibrated world uncertainty. |
| **F07** | **CURRENT WORLD STATE + CANDIDATE ACTION → FACTUAL NEXT-FUTURE ENDPOINT under flow-matching training** | Chronological next-future target, unlike same-window JEPA completion. |
| **F08** | **RECTIFIED-FLOW TRANSPORT COORDINATE; INTERMEDIATE `s` STATES ARE NOT PHYSICALLY TIME-SUPERVISED** | `dz/ds` must not be equated to `dz/dτ`; core V1.3 result. |

---

# G. Future supervision and truth sources

| ID | DynFlowDrive value | Evidence / interpretation |
|---|---|---|
| G01 | **one factual next-frame world latent `z_{t+1}^w`** | Extracted from the actually observed next frame. |
| G02 | **pretrained VAE/foundation target path; no EMA target network described; exact detach/freeze SOURCE-UNVERIFIED** | Code is required to settle gradient ownership. |
| G03 | **logged factual next observation** | No per-candidate reactive simulator or teacher provides true alternative consequences. |
| G04 | **NO external utility teacher; hybrid positive-mode teacher uses GT trajectory error + factual latent reconstruction + flow-direction stability** | This is ranking/classification supervision, not a learned return/PDMS teacher. |
| G05 | **ground-truth trajectory L1/imitation loss** | Planner trajectory supervision remains a major direct signal. |
| G06 | **`n* = argmin_n [λ_rec L_rec^n + λ_traj L_traj^n + λ_θ S_θ^n]`** | Positive mode is defined by a hand-weighted hybrid criterion. |
| G07 | **score head receives the selected mode `n*`; paper implies candidate-conditioned world evaluation, exact per-candidate loss/detach coverage SOURCE-UNVERIFIED** | Multi-candidate architecture still shares one factual world endpoint. |
| G08 | **logged factual surrounding-world future; reactive responses under unexecuted ego alternatives NOT ESTABLISHED** | Core counterfactual boundary. |

---

# H. Multimodal branch identity and assignment

| ID | DynFlowDrive value | Evidence / interpretation |
|---|---|---|
| H01 | **ego trajectory candidate / policy mode** | Each branch represents an action hypothesis, not a separately observed world. |
| H02 | **learned trajectory queries / anchors structured by command and host planner** | Branch identity originates in planner candidate construction. |
| H03 | **hybrid trajectory + reconstruction + flow-stability criterion defines positive mode** | World model changes training assignment rather than online selection. |
| H04 | **no canonical best-of-N/oracle candidate ceiling reported** | Candidate support vs scorer headroom remains unresolved. |

---

# I. Counterfactuality and reactivity

| ID | DynFlowDrive value | Evidence / interpretation |
|---|---|---|
| I01 | **YES candidate-specific world-output/velocity branching** | Different trajectory conditions produce distinct learned flow fields. |
| I02 | **NO observed per-candidate alternative consequence targets** | All branches ultimately reference the one factual next latent. |
| I03 | **NO real/simulated intervention ground truth for all alternative ego candidates** | Planner candidates are hypothetical. |
| I04 | **NO / NOT ESTABLISHED reactive other-agent response truth** | NAVSIM does not supply fully reactive actor responses for each candidate. |
| I05 | **ABSENT external intervention-validity evidence** | Action-conditioned latent differentiation is architectural, not causal identification. |

---

# J. World → planning interface

| ID | DynFlowDrive value | Evidence / interpretation |
|---|---|---|
| J01 | **training-time candidate assignment / score-label teaching + auxiliary representation shaping** | World information changes how the planner learns, not which future it evaluates online. |
| J02 | **NO online future computation** | Paper explicitly says world model is not involved at inference. |
| J03 | **NO online future consumption** | Final selector uses learned score head only. |
| J04 | **training forward: candidate action→world; training backward: world/score losses may shape planner; inference: current state→candidates/scores** | Exact gradient detach boundaries await code. |
| J05 | **candidate score head → argmax** | Deployed mechanism is a learned model-free-style candidate selector. |
| J06 | **consequence model and decision model are separate during training; consequence model removed at inference** | Strong contrast to WoTE/World4Drive where future object remains online. |
| J07 | **training graph includes WM; inference graph excludes WM** | Explicit lifecycle graph switch. |
| **J08** | **DEPLOYED WORLD ITERATION = NONE; host planner may iteratively refine trajectory queries** | Flow Euler steps are training-time transport steps, not deployed planning iterations. |
| **J09** | **TRAINING: predicted/candidate trajectory; DEPLOYMENT: NOT APPLICABLE** | Candidate trajectory is the planner→world carrier only during training. |

---

# K. Scorer and decision semantics

| ID | DynFlowDrive value | Evidence / interpretation |
|---|---|---|
| K01 | **explicit planner score head; world model defines its training target indirectly** | Scorer remains after WM removal. |
| K02 | **hybrid mode-preference / imitation-consistency / factual-reconstruction / latent-transport-stability semantics** | A high deployed score is not directly a calibrated utility or risk probability. |
| K03 | **inference scorer sees planner/candidate features, not predicted future world; training target sees world-derived criterion** | Critical teacher/student information asymmetry. |
| K04 | **hand-weighted criterion: trajectory error + future-latent reconstruction + flow-direction stability** | Utility decomposition itself is a scientific design choice. |
| K05 | **`n*` from hybrid criterion supervises score-class selection** | Score target is a training-time world-derived oracle label, not PDMS/return. |

---

# L. Training topology, jointness and gradient coupling

| ID | DynFlowDrive value | Evidence / interpretation |
|---|---|---|
| L01 | **joint planner + score + reconstruction + flow training** | Not a separate pretraining stage in the audited formulation. |
| L02 | **partial representation interaction: planner scene queries participate in world-latent aggregation** | World/planner states are not fully identical. |
| L03 | **separate host planner, pretrained world encoder/VAE path, and flow Transformer** | No single monolithic shared parameter set. |
| L04 | **paper graph/objective suggest world/reconstruction/flow losses can shape planner; exact detach direction SOURCE-UNVERIFIED** | Code release is required before layer-level gradient claims. |
| L05 | **world model discarded at deployment; only planner/score weights retain training influence** | No future latent/student surrogate remains. |
| L06 | **`L_traj + λ_score L_score + λ_rec L_rec + λ_flow L_flow`** | Final gain is a bundle of policy, ranking and dynamics supervision. |
| **L07** | **NOT APPLICABLE to world↔planner refinement; internal flow states receive flow-field supervision but not physical intermediate-state labels** | Do not reinterpret solver supervision as intermediate physical future supervision. |

---

# M. Future-knowledge lifecycle and deployment path

| ID | DynFlowDrive value | Evidence / interpretation |
|---|---|---|
| M01 | **training-only consequence model → score/policy shaping / world-derived candidate-label distillation** | Canonical lifecycle. |
| M02 | **NONE at deployment** | No future world object is computed by the deployed selector. |
| M03 | **explicit flow dynamics system removed; learned score/policy parameters retained** | Model class changes from world-assisted training graph to planner-only deployment graph. |
| M04 | **implicit compression into score-head/policy weights; no explicit future-summary latent** | Unlike WorldDrive's online distilled future summary. |
| M05 | **no inspectable deployed consequence object** | Future consequences cannot be audited online because they are not produced. |
| M06 | **training-only world branch, not an online sibling planning mode** | Stronger removal than optional Epona simulation branch. |

---

# N. Compute, pruning and latency

| ID | DynFlowDrive value | Evidence / interpretation |
|---|---|---|
| N01 | **NAVSIM: 256 online action candidates × deployed future-world depth 0** | Training evaluates flow dynamics, deployment does not. |
| N02 | **training-time VAE latent + flow Transformer; deployment retains ordinary planner/scorer only** | World-state richness has no online dynamics cost. |
| N03 | **world model completely pruned before deployment** | Score head is the compressed decision artifact. |
| N04 | **candidate scoring likely batched/parallel in host planner; source-level implementation not available** | Do not invent execution details. |
| N05 | **Table 3 reports 13.8 FPS baseline/WM-only vs 13.6 FPS MS-containing rows on RTX 4090** | Supports near-zero world-model inference cost because WM is absent; small scorer/multimodal overhead remains. |
| N06 | **training-time flow integration curve: 1/3/5/10 → 0.60/0.28, 0.59/0.23, 0.57/0.22, 0.59/0.24** | This is solver/teacher resolution, not deployed world rollout or physical horizon. |

---

# O. Evaluation regime and evidence attribution

| ID | DynFlowDrive value | Evidence / interpretation |
|---|---|---|
| O01 | **nuScenes open-loop planning + NAVSIM v1 NON-REACTIVE data-driven/pseudo-simulation planning** | Paper's `closed-loop NAVSIM` wording is not adopted as reactive closed-loop evidence. |
| O02 | **no standalone future-latent fidelity metric tied to world modeling identified** | Main evidence is downstream planning ablation, not prediction benchmark. |
| O03 | **one factual logged next-world supervision; NAVSIM evaluation remains non-reactive** | Evaluation does not upgrade training to counterfactual/reactive truth. |
| O04 | **Static WM 0.61/0.30 → Flow WM 0.59/0.26 (Avg L2/CR)** | Strongest matched world-dynamics control. |
| O05 | **baseline 0.69/0.37 → Static WM 0.61/0.30 → Flow WM 0.59/0.26 → Flow+MS 0.57/0.22; separate World Feat 0.59/0.26→0.57/0.22** | Attribution must separate static predictive loss, flow formulation, feature prior and selection supervision. |
| O06 | **headline SSR 0.39→0.31 is confounded by ego-status input; more matched row is 0.39→0.35** | Headline SOTA delta is weaker causal evidence. |
| O07 | **ABSENT direct world-prediction/path-fidelity → planning-relevance evidence** | Better planning after flow objective does not establish calibrated world fidelity as causal variable. |
| O08 | **paper + official repo state audited; implementation unavailable; Eq.7/Eq.10 and sampling-start ambiguities unresolved** | Do not repair mathematical ambiguity without source. |
| O09 | **NOT REPORTED canonical candidate oracle ceiling** | Ranking vs candidate-support headroom remains unknown. |
| O10 | **see symmetric evidence boundary below** | Required. |

O10 normalized evidence boundary:

```text
PROVES REASONABLY WELL:
- rectified-flow WM improves downstream planning over the matched static-WM baseline;
- foundation world features add further gain;
- richer training-time mode-assignment/score supervision improves planning;
- the world model can be removed from deployment.

DOES NOT PROVE:
- flow coordinate s is physical time;
- intermediate flow states are real intermediate scenes;
- angular flow stability is calibrated physical stability;
- 256 candidate branches have 256 true intervention futures;
- surrounding agents react correctly to each candidate;
- NAVSIM validates reactive closed-loop dynamics.

STRONGEST ALTERNATIVE EXPLANATION:
pretrained latent quality + extra future-state regularization + multimodal positive-mode assignment + scorer distillation + generic flow regularization explain much of the gain without identifying true continuous physical dynamics.
```

---

# P. Safety, uncertainty, interaction and physical validity

| ID | DynFlowDrive value | Evidence / interpretation |
|---|---|---|
| P01 | **ABSENT explicit safety/risk state** | World latent is not a decoded risk field or safety state. |
| P02 | **NO explicit deployed safety utility; training criterion contains trajectory error/reconstruction/stability rather than collision/TTC reward** | Safety emerges through imitation/training/evaluation, not an explicit online risk head. |
| P03 | **no calibrated uncertainty** | Stochastic anchor and multiple ego modes do not establish calibrated world uncertainty. |
| P04 | **implicit multi-agent information in visual/latent state; no validated reactive candidate-conditioned agent response** | Interaction appearance is not intervention response truth. |
| P05 | **trajectory conditioning + latent flow regularization; no explicit kinematic/causal law; flow angular smoothness is not validated physical consistency** | Core F08/P05 boundary. |
| P06 | **no recursive deployed world prediction/drift; training solver depth shows non-monotonic 1/3/5/10 behavior** | Online robustness is mostly planner/scorer robustness rather than WM rollout stability. |
| P07 | **rules/compliance represented mainly through dataset/benchmark and expert trajectories; no explicit rule world state** | NAVSIM PDMS does not prove world latent encodes rules. |

---

# Final normalized identity

```text
DynFlowDrive
=
multimodal trajectory planner
→ candidate trajectories + learned score head

TRAINING ONLY:
current factual world latent
+ candidate trajectory
→ rectified-flow latent transport toward one factual next latent
→ reconstruction + flow objectives
→ flow-path directional consistency
+ GT trajectory error
→ hybrid n* positive-mode label
→ score-head / policy supervision

DEPLOYMENT:
current observation
→ candidate trajectories + learned scores
→ argmax

world model / future latent / flow integration / flow stability = ABSENT
```

Primary ontology identity:

```text
A02  training-time consequence + ranking teacher
E01  trajectory-conditioned world prediction during training
F04  physical endpoint + internal flow path
F07  current/action → factual next-future target
F08  transport coordinate != physically supervised time
G01  one factual next latent
I01  candidate-specific outputs YES
I02  candidate-specific factual alternative consequences NO
J02  online future computation NO
J03  online future consumption NO
J05  deployed candidate scorer
K02  hybrid teacher-preference semantics
K05  hybrid world-derived positive-mode label
M01  training-only world teacher → score/policy weights
O01  nuScenes open-loop + NAVSIM non-reactive planning
O08  paper-only implementation; source release blocked
```

Canonical subtype:

```text
TRAINING-ONLY FLOW-DYNAMICS MODE-SUPERVISION WAM
```
