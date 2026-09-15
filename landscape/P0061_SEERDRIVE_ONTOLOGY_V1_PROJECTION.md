# P0061 SeerDrive — Ontology V1 Projection

Last updated: 2026-09-15

Status: **COMPLETE FIRST PROJECTION — one genuine ontology residue identified**

Authority:

```text
landscape/WAM_DIMENSION_ONTOLOGY_V1.md
papers/deep_analysis/P0061_SEERDRIVE_DEEP_ANALYSIS_V2.md
audits/literature/PHASE_C5_SEERDRIVE_AUDIT.md
```

Evidence notation:

```text
[DP] direct paper evidence
[SV] official source/version evidence
[INF] project interpretation
[NR] not reported
[NE] not evaluated
[NA] not applicable
```

---

# A. Problem and role of world knowledge

| ID | SeerDrive position |
|---|---|
| A01 | one-shot current-scene planning underuses future scene evolution and mutual world/planning dependence [DP] |
| A02 | online future BEV as planner refinement context + internal iterative world/planner co-refinement [DP][INF] |
| A03 | anchored multimodal E2E planner with trajectory refinement/fusion; original paper is not primarily a scalar future-reward selector [DP] |
| A04 | closest historical mechanism = iterative prediction/planning refinement + multimodal planning, instantiated with learned future BEV representation [INF] |

# B. Observation and current state

| ID | SeerDrive position |
|---|---|
| B01 | NAVSIM: multi-view RGB + LiDAR + ego status; nuScenes: vision-oriented setup [DP] |
| B02 | primarily current observation encoding; not a long historical rollout model [DP] |
| B03 | TransFuser BEV feature `F_bev^curr` + M mode-specific ego features `F_ego^curr` [DP] |
| B04 | BEV spatial/semantic planning representation; ego feature encodes anchored trajectory mode + status [DP] |
| B05 | explicit current BEV and predicted future BEV; planner consumes both through decoupled branches [DP] |

# C. Representation provenance / priors

| ID | SeerDrive position |
|---|---|
| C01 | TransFuser-style sensor backbone + trajectory anchors; no foundation-model prior analogous to W4D/WorldDrive central to claimed mechanism [DP] |
| C02 | standard learned BEV/anchor encoding, auxiliary BEV semantics [DP] |
| C03 | jointly trained E2E paper graph; dedicated imported-prior freeze policy not central [DP] |
| C04 | no generic-prior→WM-specific attribution ladder reported [NE] |

# D. Action / intention / candidate space

| ID | SeerDrive position |
|---|---|
| D01 | K-means/anchored trajectory modes + ego status create current ego/mode feature [DP] |
| D02 | trajectory anchor / endpoint embedded as ego-mode representation; not low-level control [DP] |
| D03 | no explicit semantic command/intention module central to original method; supplement failure suggests missing high-level intention can hurt right turns [DP] |
| D04 | explicit anchored multimodal candidate/mode bank [DP] |
| D05 | NAVSIM M=256; nuScenes M=6 [DP] |
| D06 | planning network refines/decodes trajectories; supplement identifies candidate support and classification as remaining bottlenecks [DP] |

# E. Action → world coupling

| ID | SeerDrive position |
|---|---|
| E01 | future BEV depends on mode-specific ego feature derived from anchor trajectory/status [DP] |
| E02 | current BEV repeated per mode + mode ego token concatenated into scene token sequence → shared Transformer WM [DP] |
| E03 | M branches produced by one shared BEV world model conditioned on different ego/mode features [DP] |
| E04 | branches persist across **internal refinement iterations**, but original best configuration predicts endpoint future rather than recurrent physical-time sequence [DP][INF] |
| E05 | alternative modes arise from anchor support; intervention-valid OOD action generalization not established [NE] |

# F. Dynamics / future temporal modeling

| ID | SeerDrive position |
|---|---|
| F01 | mode-specific future BEV feature + decodable semantic BEV map [DP] |
| F02 | future scene context used to refine ego planning representation [DP] |
| F03 | Transformer encoder BEV world model [DP] |
| F04 | default = final-horizon endpoint future; not recurrent temporal rollout [DP] |
| F05 | NAVSIM final horizon 4s; nuScenes 3s. Intermediate temporal predictions do not improve PDMS: 88.8/88.9/88.9 [DP] |
| F06 | multimodal modes, but no calibrated uncertainty claim; WTA supervision. Internal refinement robustness distinct from temporal rollout robustness [DP][INF] |

# G. Future supervision / truth sources

| ID | SeerDrive position |
|---|---|
| G01 | factual future semantic BEV / scene target from logged future [DP] |
| G02 | explicit semantic BEV target/decoder; no EMA/teacher-network mechanism central to original paper [DP] |
| G03 | factual logged future supervision for selected branch; no separate reactive simulator consequence teacher [DP] |
| G04 | original core future-aware branch has no explicit utility teacher; NAVSIM metric supervises/evaluates planning externally, not future-BEV truth [DP] |
| G05 | trajectory branches supervised with GT trajectory under multimodal/WTA setup [DP] |
| G06 | shared trajectory/mode probability determines winning trajectory and corresponding future-BEV branch [DP] |
| G07 | selected/winning mode receives WTA future/trajectory supervision; not K observed alternative futures [DP] |
| G08 | candidate-specific reactive surrounding-agent truth NOT ESTABLISHED [NE] |

# H. Multimodal branch identity

| ID | SeerDrive position |
|---|---|
| H01 | branch = anchored ego trajectory mode coupled to a future-BEV hypothesis [DP] |
| H02 | K-means/anchor-derived trajectory modes [DP] |
| H03 | same current-ego mode probability selects best trajectory and its future-BEV supervision [DP] |
| H04 | supplement reports candidate/ranking failure examples; no clean best-of-N oracle table equivalent to WorldDrive [DP/NE] |

# I. Counterfactuality / reactivity

| ID | SeerDrive position |
|---|---|
| I01 | YES: M mode-specific future-BEV outputs [DP] |
| I02 | positive/winning branch factual supervision; no K distinct intervention consequence labels [DP] |
| I03 | NO matched K-way observed real alternative outcomes; reactive simulator alternatives not used for original future-BEV supervision [DP/NE] |
| I04 | candidate-specific surrounding-agent reaction truth NOT ESTABLISHED [NE] |
| I05 | intervention-validity of imagined per-mode futures NOT ESTABLISHED [NE] |

# J. World → planning interface

| ID | SeerDrive position |
|---|---|
| J01 | predicted future BEV enters **trajectory feature refinement/fusion**, not merely representation pretraining or scalar reward [DP] |
| J02 | YES: compact future BEV feature computed online in original paper inference graph [DP] |
| J03 | YES: removing future BEV lowers PDMS; future representation causally participates in planner computation [DP] |
| J04 | **bidirectional internal feature coupling**: future BEV→planner; refined ego/planner feature→world model; repeated N times [DP][INF] |
| J05 | multimodal trajectory generation/refinement and final feature-fused trajectory; not WoTE-style explicit utility argmax as original paper's defining interface [DP] |
| J06 | consequence/world predictor and planner are separate modules but no separate explicit utility model in original core method [DP] |
| J07 | original paper graph vs public WoTE-integrated release differ materially; source/version must be recorded separately [SV] |

# K. Scorer / decision semantics

| ID | SeerDrive position |
|---|---|
| K01 | multimodal mode/classification scores exist for candidate selection/WTA; no original dedicated future-utility scorer central to contribution [DP] |
| K02 | mode/candidate probability / expert trajectory selection semantics, not explicit safety utility [DP][INF] |
| K03 | score primarily tied to ego/mode planning feature, while future BEV affects trajectory features [DP] |
| K04 | explicit NC/DAC/TTC reward aggregation is absent from original paper core graph; present in later WoTE-integrated code variant [SV] |
| K05 | expert/mode trajectory target in original paper; later public code adds PDM/WoTE-style reward supervision [DP][SV] |

# L. Training topology / jointness

| ID | SeerDrive position |
|---|---|
| L01 | original paper trained end-to-end with iterative world/planner passes [DP] |
| L02 | current BEV, future BEV and ego features interact in common computational graph; distinct representation objects [DP] |
| L03 | world model and planner are separate modules; iterative features pass between them [DP] |
| L04 | future-map and trajectory losses supervise all iterations, allowing gradients through shared iterative computation [DP] |
| L05 | no teacher/student distillation in original mechanism [NA] |
| L06 | `L_map + L_traj`, applied across iterative outputs; possible multi-task coupling [DP] |

# M. Future-knowledge lifecycle

| ID | SeerDrive position |
|---|---|
| M01 | direct online endpoint future BEV + iterative co-refinement remains in original deployed paper graph [DP] |
| M02 | explicit/decodable future BEV feature at final planning horizon [DP] |
| M03 | no heavy→light lifecycle transformation in original paper [NA] |
| M04 | strong planning compression: endpoint future BEV only is sufficient; sequence predictions add complexity without PDMS gain [DP] |
| M05 | relatively inspectable semantic BEV (decoder supervised) [DP] |
| M06 | NO: future BEV is required by original future-aware planning mechanism; not merely sibling simulation branch [DP] |

# N. Compute / pruning / latency

| ID | SeerDrive position |
|---|---|
| N01 | M modes × one endpoint future by default × N=2 internal refinement iterations in best setup [DP] |
| N02 | BEV Transformer world state, far lighter than visual diffusion; 66M model reported in supplement [DP] |
| N03 | no WorldDrive-style explicit top-K pruning before future reasoning described in original paper core mechanism [DP] |
| N04 | multimodal branches are tensorized/shared-model computation; exact parallelization detail not the scientific claim [DP] |
| N05 | ~24 ms average inference, NAVSIM configuration, supplement [DP] |
| N06 | iteration curve 1/2/3 = 88.1/88.9/88.7; temporal future richness 4-step/2-step/endpoint ≈ equal [DP] |

# O. Evaluation / evidence attribution

| ID | SeerDrive position |
|---|---|
| O01 | nuScenes open-loop; NAVSIM non-reactive data-driven; supplement Bench2Drive reactive closed-loop simulator [DP] |
| O02 | future semantic-BEV mIoU reported separately; no evidence that higher mIoU monotonically predicts PDMS [DP/NE] |
| O03 | factual/non-reactive future supervision differs from Bench2Drive reactive policy evaluation; do not transfer causal semantics across them [INF] |
| O04 | strongest matched control = Table 3 2×2: 87.1 baseline, 87.9 iterative only, 88.1 future-aware only, 88.9 both [DP] |
| O05 | attribution must separate candidate/mode bank, future BEV, fusion design, refinement iterations, classification/ranking [DP] |
| O06 | SOTA cross-paper comparisons have sensor/backbone/training differences; internal ablations are stronger [DP/INF] |
| O07 | richer intermediate future prediction gives no planning gain; prediction richness ≠ decision relevance [DP] |
| O08 | paper mechanism = paper verified; current public code = later WoTE-integrated release verified at initial release commit [SV] |
| O09 | failure cases show ranking/support gap qualitatively; no clean oracle ceiling table [DP/NE] |
| O10 | proves future-BEV feature + iterative co-refinement improve reported planning; does not prove intervention-correct ego↔traffic causal dynamics [DP][INF] |

# P. Safety / uncertainty / interaction / physical validity

| ID | SeerDrive position |
|---|---|
| P01 | safety/risk not explicit as dedicated world-state variable; encoded implicitly in BEV/scene representation [DP] |
| P02 | original paper does not use explicit NC/TTC utility heads; later WoTE-integrated code does [DP][SV] |
| P03 | multimodal branch probabilities exist, but calibrated epistemic/aleatoric uncertainty NOT ESTABLISHED [NE] |
| P04 | other-agent/world dynamics encoded in BEV; explicit reactive behavioral response to each ego intervention NOT ESTABLISHED [NE] |
| P05 | anchor ego motion and semantic BEV provide geometric/motion structure; no direct causal interaction constraint [DP] |
| P06 | no long recurrent temporal rollout in best paper design; drift accumulation is therefore not the same deployment issue as Epona/WoTE [DP] |
| P07 | safety/compliance primarily evaluated through planning benchmarks, not explicitly represented as original WM reward semantics [DP] |

---

# Ontology residue / proposed V1.1 amendment

SeerDrive can be expressed under V1, but five scientifically meaningful details are awkwardly compressed. Proposed additions:

```text
J08  inference iteration semantics
     physical-time rollout / search depth / denoising / internal world↔planner refinement / environment feedback

J09  planner→world feedback carrier
     executed action / candidate trajectory / planner hidden feature / ego-mode feature / environment observation

J10  mutual-refinement topology
     one-shot / one-way / alternating internal co-refinement / external feedback closed loop

L07  per-iteration supervision
     final-only / all iterations / selected iterations / self-consistency

N07  refinement-depth saturation curve
     quality and latency as internal refinement iterations increase
```

SeerDrive values:

```text
J08 = internal world↔planner refinement
J09 = refined ego/planning feature
J10 = alternating internal co-refinement
L07 = all iterations supervised
N07 = 1→2 helps, 2→3 slightly regresses
```

These dimensions pass the Ontology extension rule because they change mechanism interpretation and prevent a major scientific error:

```text
internal neural refinement iteration
!=
physical-time world rollout
!=
external reactive closed loop
```

Before canonical V1.1, backfill the five original anchors.
