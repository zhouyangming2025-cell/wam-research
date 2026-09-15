# P0049 Drive-JEPA — Ontology V1 + V1.1 + V1.2 Projection

Last updated: 2026-09-15

Status: **FULL DIMENSION-FIRST PROJECTION — COMPLETE FIRST PASS**

Canonical analysis:

```text
papers/deep_analysis/P0049_DRIVEJEPA_DEEP_ANALYSIS_V2.md
audits/literature/PHASE_C5_DRIVEJEPA_AUDIT.md
```

Coordinate system:

```text
WAM_DIMENSION_ONTOLOGY_V1.md
+ WAM_DIMENSION_ONTOLOGY_V1_1_AMENDMENT.md
+ WAM_DIMENSION_ONTOLOGY_V1_2_AMENDMENT.md
```

Method-version scope:

```text
paper + official source linhanwang/Drive-JEPA@e21f47410b4d26b61f05f9bd23e169c0390cae2a
```

Core warning:

```text
JEPA predictive pretraining
!= deployed online world model
```

---

# A. Problem and role of world knowledge

| ID | Drive-JEPA value | Evidence / interpretation |
|---|---|---|
| A01 | **representation quality + candidate coverage + candidate selection/temporal consistency** | The paper has two distinct bottlenecks: predictive video representation learning and proposal/scorer planning. |
| A02 | **training-stage predictive representation prior** | JEPA prediction shapes/transfers the visual encoder; no JEPA future object is consumed online. |
| A03 | **proposal-centric candidate planner** in full model; **direct waypoint decoder** in perception-free probe | Full system generates 32 proposals and scores them. |
| A04 | **predictive pretraining + multimodal imitation/pseudo-teacher planning + learned utility scoring** | Historically closer to ViDAR/predictive pretraining for JEPA part and candidate-scoring E2E planning for full planner. |

---

# B. Observation and current-state representation

| ID | Drive-JEPA value | Evidence / interpretation |
|---|---|---|
| B01 | **front RGB camera + ego status/command; no LiDAR in reported Drive-JEPA setup** | Paper appendix uses front camera at 512×256. |
| B02 | **two front frames for downstream planner** | Current + previous front image; JEPA pretraining uses 8-frame clips. |
| B03 | **ViT video/image latent tokens; perception-based planner further maps them into proposal/BEV-query features** | Current-state substrate is learned visual representation, not explicit future world state. |
| B04 | **spatiotemporal visual semantics learned self-supervised; downstream proposal features additionally planning-oriented** | Exact physical semantics are not explicitly decoded by JEPA pretext task. |
| B05 | **current/history representation only at deployment; no predicted future-state object** | Distinguish pretraining predictive target from deployed planner state. |

---

# C. Representation provenance and imported priors

| ID | Drive-JEPA value | Evidence / interpretation |
|---|---|---|
| C01 | **V-JEPA 2 ViT-L prior → driving-video JEPA adaptation/pretraining** | Core representation origin stack. |
| C02 | **checkpoint initialization + continued self-supervised video latent prediction** | No explicit perception labels required for JEPA pretraining. |
| C03 | **perception-free: frozen by default; perception-based: fine-tuned at reduced LR** | Source verifies frozen encoder in simple probe and 0.1× backbone LR in full planner. |
| C04 | **partially isolated** | Table 5: generic V-JEPA2 86.1 → drive-domain JEPA 89.0 under simple decoder; still confounded by extra driving-domain data/exposure. |

---

# D. Action, intention and candidate space

| ID | Drive-JEPA value | Evidence / interpretation |
|---|---|---|
| D01 | **online proposals learned/refined from scene features; supervision from logged human + simulator-qualified pseudo teachers** | JEPA pretraining itself has no ego-action condition. |
| D02 | **8-pose trajectory / waypoint sequence, (x,y,heading), 4 s horizon** | Source config: 8 poses, 0.5 s interval. |
| D03 | **route/driving command included in ego status** | Paper task formulation includes left/forward/right-style command. |
| D04 | **32 online proposals; separate 8192-trajectory offline teacher vocabulary** | Do not confuse teacher vocabulary size with deployed proposal count. |
| D05 | **32 deployed alternatives; offline teacher vocabulary 8192** | MTD expands supervision/support rather than directly evaluating all 8192 at inference. |
| D06 | **4 shared-weight proposal-refinement passes; simulator filters pseudo teachers before training** | Proposal refinement is an independent planner mechanism. |

---

# E. Action → world coupling

| ID | Drive-JEPA value | Evidence / interpretation |
|---|---|---|
| E01 | **ABSENT for JEPA world/predictive pretraining** | V-JEPA masked latent objective is not conditioned on ego action. Candidate trajectories later enter planner/scorer, not an online future-world predictor. |
| E02 | **NOT APPLICABLE** | No deployed action→world transition module. |
| E03 | **NOT APPLICABLE** | No candidate-conditioned world branches. |
| E04 | **NOT APPLICABLE** | No branched temporal world rollout. |
| E05 | **NOT APPLICABLE to world prediction** | Planner candidate support can extend beyond logged human future via pseudo teachers, but no world model is queried on those actions. |

---

# F. Dynamics and future temporal modeling

| ID | Drive-JEPA value | Evidence / interpretation |
|---|---|---|
| F01 | **pretraining target = masked video latent feature; deployed future object = NONE** | Predictor targets EMA encoder embeddings, not pixels/BEV future states. |
| F02 | **spatiotemporal predictive representation** | Target semantics are whatever information the EMA video encoder preserves; not explicitly a planning consequence state. |
| F03 | **ViT encoder + JEPA Transformer predictor during pretraining; predictor removed downstream** | Full planner uses proposal refiners/scorer, not a dynamics operator. |
| F04 | **random masked spatiotemporal latent completion during JEPA pretraining** | Not chronological autoregressive rollout. |
| F05 | **no explicit deployed future-world horizon; pretraining uses 8-frame clips; planner horizon 4 s is an action horizon** | Do not treat 4 s trajectory horizon as a JEPA world-prediction horizon. |
| F06 | **deterministic latent regression; no calibrated future uncertainty** | Multimodal trajectories belong to planner, not JEPA world uncertainty. |
| **F07** | **RANDOM-MASK SAME-WINDOW SPATIOTEMPORAL COMPLETION** | Key V1.2 result: visible context can include non-causal same-window information; not history-only→future by construction. |

---

# G. Future supervision and truth sources

| ID | Drive-JEPA value | Evidence / interpretation |
|---|---|---|
| G01 | **observed-video target latent at masked spatiotemporal positions** | Factual source is the target view of the same video sample, not alternative-action future outcome. |
| G02 | **EMA target encoder + stop-gradient** | Canonical JEPA anti-collapse/target-network design. |
| G03 | **target encoder on observed video; no candidate-consequence teacher** | Separate from simulator utility labels. |
| G04 | **NAVSIM/PDM/EPDMS simulation/rule targets for proposal quality** | Utility teacher belongs to downstream planner, not JEPA target. |
| G05 | **logged human imitation + simulator-selected pseudo-teacher trajectory matching** | Multimodal Trajectory Distillation changes policy supervision. |
| G06 | **min-over-proposals matching to human and pseudo teachers; simulator threshold/ranking defines pseudo-teacher set** | Branch assignment is trajectory matching, not future-world latent matching. |
| G07 | **all proposals can receive score targets; trajectory regression selects nearest proposal(s) to human/pseudo targets** | Different supervision coverage for generation vs scoring. |
| G08 | **NAVSIM logged/replayed surrounding-agent context for training utility; reactive alternative-agent truth NOT ESTABLISHED** | Bench2Drive is evaluation, not pseudo-teacher truth source. |

---

# H. Multimodal branch identity and assignment

| ID | Drive-JEPA value | Evidence / interpretation |
|---|---|---|
| H01 | **trajectory proposal mode / feasible ego action hypothesis** | Modes are actions, not separate predicted worlds. |
| H02 | **learned proposal/query features shaped by human + simulator pseudo teachers** | Offline 8192 trajectory vocabulary supplies multimodal targets. |
| H03 | **nearest/min-over-proposal matching + simulator-quality filtering** | Positive proposal supervision is target-trajectory based. |
| H04 | **diversity measured; explicit deployed oracle ceiling NOT REPORTED** | Table 6 reports diversity 24→40%; source computes best scores internally but paper does not establish a canonical best-of-32 oracle gap. |

---

# I. Counterfactuality and reactivity

| ID | Drive-JEPA value | Evidence / interpretation |
|---|---|---|
| I01 | **NO candidate-specific world-output branching** | There are 32 action proposals, but no corresponding predicted world futures. |
| I02 | **NO learned candidate-specific consequence target; utility labels only** | Simulator/rule scores are candidate-specific decision targets, not learned world-state targets. |
| I03 | **simulated/rule-evaluated ego alternatives exist; no observed alternative-action world ground truth** | Candidate feasibility/utility is evaluated offline. |
| I04 | **NO / NOT ESTABLISHED for training supervision** | Other-agent responses under each ego candidate are not established as reactive causal truths. |
| I05 | **NO direct intervention-validity evidence for a world model** | Bench2Drive supports closed-loop planner performance, not counterfactual dynamics identification. |

---

# J. World → planning interface

| ID | Drive-JEPA value | Evidence / interpretation |
|---|---|---|
| J01 | **representation learning / encoder transfer** | Predictive world knowledge enters planning only through encoder weights/features. |
| J02 | **NO online predicted future representation** | Source-verified. |
| J03 | **NO online future consumption** | JEPA predictor absent from planner inference. |
| J04 | **no online world→action or action→world dynamics coupling** | Training-stage predictive representation → later planner is a staged lifecycle. |
| J05 | **full model: proposal scorer/argmax; perception-free probe: direct waypoint decoder** | Final deployed mechanism depends on evaluation mode. |
| J06 | **no consequence model; utility scorer separate from visual representation** | Important distinction: learned score is not output of a future-world model. |
| J07 | **multiple task/evaluation graphs** | Perception-free representation probe vs perception-based proposal planner; NAVSIM-v1/v2 source differences also matter. |
| **J08** | **PLANNER PROPOSAL/QUERY REFINEMENT ITERATION** | Four shared-weight passes refine candidate features; physical future time does not advance. |
| **J09** | **NONE / NOT APPLICABLE** | No planner→world feedback carrier because no online world predictor exists. |

---

# K. Scorer and decision semantics

| ID | Drive-JEPA value | Evidence / interpretation |
|---|---|---|
| K01 | **explicit scorer after proposal refinement** | Full model only; perception-free probe has no proposal scorer. |
| K02 | **utility / driving-quality score + temporal comfort correction** | High score means simulator/PDM-like candidate quality, not factual-future probability. |
| K03 | **proposal feature / trajectory-conditioned feature; momentum path also sees previous simulated ego states** | No predicted future-world sequence is required. |
| K04 | **PDM/EPDMS multi-criterion utility learned in score targets; final NAVSIM-v2 recalibration adds two-frame extended comfort** | Utility composition itself explains part of planning behavior. |
| K05 | **NAVSIM simulator/rule metric targets** | Source computes proposal target scores offline during training. |

---

# L. Training topology, jointness and gradient coupling

| ID | Drive-JEPA value | Evidence / interpretation |
|---|---|---|
| L01 | **staged: V-JEPA2 initialization → driving-video JEPA pretraining → downstream planner training** | Not one joint world-action training graph. |
| L02 | **representation identity transfer through visual encoder** | Downstream planner consumes encoder learned by predictive pretraining. |
| L03 | **encoder transferred; JEPA predictor/EMA target modules not shared with planner** | Full planner adds separate proposal/scorer modules. |
| L04 | **no downstream planner gradient through JEPA predictor; perception-based planner can fine-tune visual backbone** | Predictive and planning losses are temporally/stage separated. |
| L05 | **perception-free frozen encoder; perception-based reduced-LR fine-tuning; predictor discarded** | Important lifecycle distinction. |
| L06 | **planner combines trajectory, score, auxiliary agent/area/map objectives depending configuration** | Full gain cannot be assigned to predictive objective alone. |
| **L07** | **ALL proposal-refinement stages receive trajectory supervision, with previous-stage weighting** | Source loops over `proposal_list`; not a world-state refinement loss. |

---

# M. Future-knowledge lifecycle and deployment path

| ID | Drive-JEPA value | Evidence / interpretation |
|---|---|---|
| M01 | **predictive pretraining → transferred representation; predictive head discarded** | Distinct from LAW's auxiliary loss during planner training. |
| M02 | **NONE** | No future object exists on deployed action-selection path. |
| M03 | **encoder retained; JEPA predictor + EMA target encoder removed** | Model class changes from predictive pretraining system to feature encoder + planner. |
| M04 | **implicit representation bottleneck only; no deployed future-summary distillation** | Do not confuse encoder representation with a predicted future summary. |
| M05 | **opaque transferred visual latent; no inspectable future consequence** | Predictor output not deployed. |
| M06 | **NO optional deployed future-generation sibling branch in audited planner** | JEPA training machinery is a prior stage, not a task-mode sibling. |

---

# N. Compute, pruning and latency

| ID | Drive-JEPA value | Evidence / interpretation |
|---|---|---|
| N01 | **32 action proposals × 4 proposal-refinement passes; future-world depth = 0** | Candidate breadth should not be described as 32 world rollouts. |
| N02 | **ViT-L-scale visual representation + proposal query features; no online dynamics state** | Pretraining is compute-heavy but deployment avoids predictive head. |
| N03 | **no major future-model pruning stage; all 32 final proposals scored** | Offline 8192 teacher vocabulary is not deployed online. |
| N04 | **proposal branches represented in batched tensors / parallel neural processing** | No sequential search tree. |
| N05 | **end-to-end inference latency NOT REPORTED sufficiently for matched cross-paper comparison** | Paper reports training compute and input resolution more clearly than sensor-to-action runtime. |
| N06 | **no canonical quality–latency operating curve for proposal count/refinement depth reported in audited paper** | Module ablations are quality attribution, not latency frontier. |

---

# O. Evaluation regime and evidence attribution

| ID | Drive-JEPA value | Evidence / interpretation |
|---|---|---|
| O01 | **NAVSIM v1/v2 non-reactive data-driven planning + Bench2Drive reactive CARLA closed loop** | Evaluation regime must be named per result. |
| O02 | **no dedicated world-generation/future-prediction fidelity evaluation tied to planning** | Main JEPA evidence is downstream planning transfer. |
| O03 | **training pseudo-teacher/score regime NAVSIM-style non-reactive; Bench2Drive evaluates deployed planner reactively** | Reactive evaluation does not retroactively make training supervision counterfactual/reactive. |
| O04 | **JEPA-specific: V-JEPA2 ViT/L 86.1 → drive-domain JEPA ViT/L 89.0 with same simple-decoder family; full planner: baseline 84.1 → drive-pretrain 86.1** | Strongest available representation control, though extra domain data remains a confound. |
| O05 | **84.1 baseline → 85.8 generic V-JEPA2 / 86.1 driving pretrain → 84.5 +MTD → 87.8 +momentum** | Canonical attribution ladder; shows MTD alone harms final score while increasing diversity. |
| O06 | **cross-paper SOTA heterogeneous; within-paper module rows stronger** | Epona/LAW/World4Drive differ in backbone/data/model scale and should not be causal controls. |
| O07 | **ABSENT** | No matched evidence that lower JEPA latent-prediction error itself yields better planning. |
| O08 | **paper + official source audited at e21f474...; perception-free and v1/v2 planner paths checked** | Momentum path source-verified in NAVSIM-v2; v1 differs. |
| O09 | **NOT REPORTED as canonical deployed best-of-32 gap** | Source can compute best proposal score, but no stable paper-level oracle ceiling established here. |
| O10 | **see evidence boundary below** | Predictive representation transfer is supported; online world dynamics/counterfactual response is not. |

### O10 compact boundary

```text
PROVES / strongly supports:
predictive video pretraining transfers useful planning representation;
simulator pseudo teachers increase proposal diversity;
selection quality is necessary to exploit that diversity.

DOES NOT PROVE:
JEPA predictor is an online world model;
random-mask completion equals causal future forecasting;
full planning gain is a world-model gain;
simulator pseudo teachers are reactive counterfactual truth.

STRONGEST ALTERNATIVE EXPLANATION:
large-scale video representation + richer action supervision + stronger candidate scorer/temporal selector.
```

---

# P. Safety, uncertainty, interaction and physical validity

| ID | Drive-JEPA value | Evidence / interpretation |
|---|---|---|
| P01 | **ABSENT explicit risk/safety future state** | JEPA latent is not explicitly safety-structured. |
| P02 | **YES in decision value** | PDM/EPDMS targets encode collision/compliance/progress/comfort-related criteria; momentum adds temporal comfort. |
| P03 | **no calibrated predictive uncertainty** | Multiple proposals express policy diversity, not calibrated world uncertainty. |
| P04 | **implicit visual interaction + optional agent auxiliary supervision; no learned reactive candidate-conditioned world response** | Keep action diversity separate from interaction dynamics. |
| P05 | **trajectory vocabulary + simulator/rule scoring + feasible human/pseudo targets provide kinematic/road constraints** | Physical validity comes mostly through candidate supervision/scoring, not JEPA dynamics. |
| P06 | **no recursive deployed world prediction; proposal refinement only** | No world-model drift accumulation at inference. |
| P07 | **rules/compliance represented mainly in PDM/EPDMS utility/evaluation** | Includes traffic/compliance/comfort metrics in NAVSIM-v2; this does not prove visual latent explicitly encodes rules. |

---

# Final normalized identity

```text
Drive-JEPA
=
V-JEPA random-mask spatiotemporal latent pretraining
→ driving-domain visual encoder transfer
→ JEPA predictor removed

+

32 proposal policy
→ 4 shared-weight proposal refinements
→ human + simulator pseudo-teacher multimodal supervision
→ simulator-trained utility scorer
→ NAVSIM-v2 temporal comfort recalibration
→ argmax
```

Primary ontology identity:

```text
A02  training-stage predictive representation prior
F07  RANDOM-MASK SAME-WINDOW SPATIOTEMPORAL COMPLETION
J02  online future computation = NO
J03  online future consumption = NO
J08  planner proposal refinement, not temporal rollout
K02  utility / driving-quality scorer
L01  staged predictive pretraining → planner training
M01  predictive pretraining → encoder transfer, predictor discarded
O05  full attribution ladder mandatory
```

Cross-paper position:

```text
ViDAR       causal future-forecasting pretrain → encoder transfer
LAW         action-aware future-latent auxiliary shaping during planner training
Drive-JEPA  masked-video predictive pretrain → encoder transfer
Auto-JEPA   future ego-intent latent remains online as action retrieval key
WA-JEPA     future-directed JEPA + joint world/action prediction
```
