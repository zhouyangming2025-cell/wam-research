# P0002 SafeDrive — Ontology V1 + V1.1 + V1.2 + V1.3 Projection

Last updated: 2026-09-15

Status: **FULL DIMENSION-FIRST PROJECTION — COMPLETE FIRST PASS**

Canonical analysis:

```text
papers/deep_analysis/P0002_SAFEDRIVE_DEEP_ANALYSIS_V2.md
audits/literature/PHASE_C6_SAFEDRIVE_AUDIT.md
```

Source scope:

```text
paper: SafeDrive, CVPR 2026
repo: SPA-junghokim/SafeDrive
audited commit: ea7791d6c2ebdeedfb6ed514f080cdfa1675b76f
NAVSIM core implementation SOURCE-VERIFIED
Bench2Drive implementation SOURCE-PARTIAL
```

Core warning:

```text
candidate-specific safety consequence supervision
!=
candidate-specific reactive environment-future truth
```

---

# A. Problem / role

| ID | SafeDrive value |
|---|---|
| A01 | safety-critical candidate discrimination and interaction-aware planning |
| A02 | online candidate-specific sparse world + explicit safety evaluator |
| A03 | candidate bank → world refinement → safety scoring → selection |
| A04 | combines query-based multimodal planning, conditional motion prediction, learned PDM-like scoring and structured interaction modeling |

# B. Current-state representation

| ID | SafeDrive value |
|---|---|
| B01 | camera + LiDAR + ego/history inputs |
| B02 | temporal BEV/history context |
| B03 | dense temporal BEV plus sparse object/planning queries |
| B04 | explicit instance, motion, relational and road semantics |
| B05 | both current BEV/object state and predicted/refined future sparse-world state are used online |

# C. Representation provenance

| ID | SafeDrive value |
|---|---|
| C01 | BEVFormer-M / standard perception-planning priors; no large video-foundation prior central to claim |
| C02 | pretrained/checkpointed stage-wise pipeline + supervised perception/world/planning losses |
| C03 | Phase 2 freezes perception; Phase 3 full fine-tunes |
| C04 | generic prior vs WAM-specific gain only partially isolated; strongest clean control is representation × safety-granularity ablation |

# D. Action / candidate space

| ID | SafeDrive value |
|---|---|
| D01 | K-means trajectory anchors refined by ProposalNet |
| D02 | sequence of ego future poses / planning query |
| D03 | no primary semantic intention token; multimodality is anchor/candidate based |
| D04 | explicit candidate bank, released config starts from 256 anchors |
| D05 | broad candidate support followed by pruning |
| D06 | released config uses two-stage proposal path, top-128 before SWNet; later world/agent filtering further reduces compute |

# E. Action → world coupling

| ID | SafeDrive value |
|---|---|
| E01 | PRESENT: each ego candidate defines its own sparse world |
| E02 | candidate planning query is concatenated/combined with replicated surrounding-agent queries; later world self-attention + trajectory-guided attention |
| E03 | shared SWNet parameters across candidate worlds |
| E04 | branch persists across multi-layer future motion refinement; not a search tree |
| E05 | non-expert candidate actions receive simulator safety supervision but no distinct observed reactive-agent future |

# F. Dynamics / future time

| ID | SafeDrive value |
|---|---|
| F01 | sparse ego/agent future queries and explicit future trajectories/motion states |
| F02 | interaction, geometry, motion and safety-relevant semantics |
| F03 | Transformer-style world interaction / motion decoder |
| F04 | explicit multi-timestep trajectory prediction/refinement, not video autoregression |
| F05 | 4 s planning horizon in released config, 0.5 s model pose interval; internal PDM teacher resamples more finely |
| F06 | multiple ego candidate worlds; no calibrated stochastic environment distribution |
| F07 | history/current observations → unseen future ego/agent motion sequence |
| F08 | model pose timestep corresponds to physical future time; decoder layer/refinement depth does NOT correspond to extra physical time |

# G. Future supervision / truth

| ID | SafeDrive value |
|---|---|
| G01 | logged factual agent motion / BEV semantics for prediction; simulator-derived candidate safety labels |
| G02 | direct supervised targets; no EMA target core to SafeDrive |
| G03 | logged future scene/agent tracks are factual, not per-intervention alternatives |
| G04 | strong candidate-specific PDM safety/value teacher: NC/DAC/EP/TTC/comfort/DDC (+TLC/LK), pair collision and TwDAC |
| G05 | expert trajectory supports imitation classification/regression |
| G06 | closest anchor/mode to expert defines imitation-positive branch |
| G07 | safety labels cover all model proposals; environment motion truth is reused across ego branches |
| G08 | reactive alternative-agent truth ABSENT in audited NAVSIM training path |

# H. Branch identity / assignment

| ID | SafeDrive value |
|---|---|
| H01 | ego trajectory candidate |
| H02 | anchor/refined-plan identity persists into sparse world |
| H03 | expert-positive assignment by geometric distance for imitation; safety supervision independently scores all proposals |
| H04 | pruning/support handled by proposal stages; oracle best-of-N headroom not the main reported world ablation |

# I. Counterfactuality / reactivity

| ID | SafeDrive value |
|---|---|
| I01 | YES candidate-specific sparse-world outputs |
| I02 | NO candidate-specific observed alternative-agent future targets |
| I03 | YES candidate-specific simulated safety consequence labels under PDM/logged-world semantics, but NO full intervention world-state truth |
| I04 | NO reactive other-agent response truth in audited NAVSIM target path |
| I05 | Bench2Drive gives reactive final-policy evidence, NOT branch-level intervention-validity evidence |

# J. World → planning interface

| ID | SafeDrive value |
|---|---|
| J01 | online sparse world feeds explicit safety reasoning and final selection |
| J02 | YES world/future features computed online |
| J03 | YES consumed online by FRNet/scoring |
| J04 | forward: candidate→world→safety→selection; training gradients from safety/motion/planning losses update corresponding modules; Phase-3 end-to-end |
| J05 | weighted multi-factor safety score → selection |
| J06 | consequence/world representation and decision evaluator are distinct but jointly trained |
| J07 | external PDM teacher removed at deployment; learned world+safety path retained |
| J08 | decoder layers/refinement iterations are representation/motion refinement, not physical rollout steps |
| J09 | planner→world carrier = ego planning query / trajectory candidate |

# K. Scorer semantics

| ID | SafeDrive value |
|---|---|
| K01 | explicit scene-level + fine-grained safety scorer |
| K02 | safety/compliance/progress/imitation utility semantics |
| K03 | scorer sees sparse ego-agent interaction state and candidate trajectory/world features |
| K04 | factorized: scene NC/DAC/TTC/EP/etc + PwNC(agent×time) + TwDAC(time) |
| K05 | targets come from live PDM proposal scoring + pair-collision/off-road localization; imitation target from logged expert |

# L. Training topology

| ID | SafeDrive value |
|---|---|
| L01 | multi-stage training ending in end-to-end full fine-tuning |
| L02 | shared BEV/object/planning representations across proposal/world/safety modules |
| L03 | ProposalNet, SWNet and FRNet are parameter-distinct modules |
| L04 | Phase-3 gradients jointly couple planning/world/safety; external PDM labels are detached/non-differentiable teacher outputs |
| L05 | Phase 2 frozen perception → Phase 3 unfrozen/full train |
| L06 | perception + trajectory + motion + scene safety + PwNC + TwDAC composite supervision |
| L07 | multi-layer world states receive trajectory/motion losses; no claim of ground-truth world supervision at every refinement layer beyond configured losses |

# M. Future-knowledge lifecycle

| ID | SafeDrive value |
|---|---|
| M01 | supervised perception/planning → simulator-labeled world/safety training → online learned evaluator |
| M02 | online sparse structured future representation |
| M03 | PDM teacher is training/eval-time external machinery; not needed for deployment inference |
| M04 | no separate distillation into smaller future model reported |
| M05 | inspectable agent/time safety outputs remain online |
| M06 | single deployed planning/evaluation mode in audited NAVSIM path |

# N. Compute / pruning

| ID | SafeDrive value |
|---|---|
| N01 | 256 initial anchors; top-128 stage-2 proposal path in released Phase-3 config; agent filtering to 25 |
| N02 | BEV encoder + proposal decoder + 4-layer SWNet + FRNet online |
| N03 | aggressive candidate/agent pruning before expensive sparse-world reasoning |
| N04 | candidate worlds can be processed as batched query dimensions in implementation |
| N05 | paper/release reports deployment performance but no clean isolated latency attribution for each world/safety module in this audit |
| N06 | pruning is integral to deployment feasibility; no monotonic candidate-count study central to paper found in this pass |

# O. Evaluation / attribution

| ID | SafeDrive value |
|---|---|
| O01 | NAVSIM non-reactive pseudo-simulation + paper-level Bench2Drive reactive CARLA closed loop |
| O02 | motion/world outputs are supervised, but no independent calibration study proving future-motion fidelity→planning gain identified |
| O03 | factual logged motion + PDM candidate safety labels; no alternative reactive-world truth |
| O04 | strongest mechanism control: sparse+scene ≈ BEV+scene, sparse+fine-grained improves to 91.6 |
| O05 | fine-grained head ablation isolates PwNC and TwDAC contributions |
| O06 | final gains also bundle proposal/scoring/perception improvements; do not call headline delta pure WAM gain |
| O07 | released checkpoint/test path reproduces ~91.6 NAVSIM PDMS |
| O08 | NAVSIM source HIGH; Bench2Drive source PARTIAL |

# P. Safety / uncertainty / interaction / validity

| ID | SafeDrive value |
|---|---|
| P01 | no continuous risk field; explicit localized safety states/scores instead |
| P02 | YES explicit online safety evaluator: scene + agent×time + time-wise road compliance |
| P03 | no calibrated probabilistic multi-future uncertainty distribution; PwNC is learned probability-like output but not calibrated uncertainty evidence |
| P04 | explicit ego-agent interaction structure in sparse worlds |
| P05 | future motion physically parameterized as trajectories; no formal dynamics-law constraint |
| P06 | no recurrent long-horizon world-rollout drift benchmark; fixed-horizon multi-step prediction/refinement |
| P07 | strong explicit rule/safety semantics from PDM labels and drivable-area geometry |

---

# Final normalized identity

```text
SafeDrive
=
multimodal temporal BEV
→ 256 candidate anchors + detected agents
→ coarse candidate scoring/pruning
→ one structured sparse ego-agent world per candidate
→ joint future-motion refinement
→ explicit scene / agent×time / time-wise safety reasoning
→ weighted learned safety selection

SUPERVISION:
per-candidate PDM safety labels      YES
per-candidate pair collision labels YES
per-candidate TwDAC labels          YES
per-candidate reactive agent GT     NO
```

Ontology decision:

```text
V1.3 RETAINED
NO V1.4
```

Residue watchlist only:

```text
safety-localization granularity
```
