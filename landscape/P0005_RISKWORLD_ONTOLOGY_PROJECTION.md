# P0005 RiskWorld — Ontology V1 + V1.1 + V1.2 + V1.3 Projection

Last updated: 2026-09-15

Status: **FULL DIMENSION-FIRST PROJECTION — COMPLETE FIRST PASS**

Canonical analysis:

```text
papers/deep_analysis/P0005_RISKWORLD_DEEP_ANALYSIS_V2.md
audits/literature/PHASE_C6_RISKWORLD_AUDIT.md
```

Source scope:

```text
paper: arXiv:2608.21414v1
raw MD: PRESENT
official implementation: NOT IDENTIFIED
source status: PAPER-COMPLETE / SOURCE-BLOCKED
```

Core warning:

```text
object-specific future rollout
!=
action-candidate-specific counterfactual future
```

---

# A. Problem / role

| ID | RiskWorld value |
|---|---|
| A01 | object-level risk-source identification / anticipation |
| A02 | predictive object-centric risk monitor; world knowledge supports risk identification, not direct planning |
| A03 | observed object set → per-object future rollout → risk score / threshold-rank |
| A04 | combines predictive video representation, relation attention, RSSM-style latent dynamics and supervised risk identification |

# B. Current-state representation

| ID | RiskWorld value |
|---|---|
| B01 | front-view RGB + tracked object states + ego motion |
| B02 | K=16 observed frames/history |
| B03 | frozen V-JEPA2 global scene + box-pooled object visual token + structured track state |
| B04 | explicit object/ego-relative geometry, appearance, motion and relational semantics |
| B05 | current relation-aware object tokens initialize online future rollout |

# C. Representation provenance

| ID | RiskWorld value |
|---|---|
| C01 | pretrained V-JEPA2 ViT-L predictive-video prior |
| C02 | frozen imported encoder + task-specific object/relation/dynamics/risk modules |
| C03 | V-JEPA2 frozen according to paper; downstream RiskWorld modules trained |
| C04 | prior contribution partly isolated via w/o world features/object token; final result still bundles foundation representation with RiskWorld dynamics |

# D. Action / candidate space

| ID | RiskWorld value |
|---|---|
| D01 | NO ego action-candidate bank; `candidate` means observed object |
| D02 | observed ego-motion history only; no future ego action representation |
| D03 | no intention hypotheses |
| D04 | up to 64 object candidates, not multimodal ego trajectories |
| D05 | candidate-count planning breadth NOT APPLICABLE |
| D06 | object validity masking; no world-based action pruning |

# E. Action → world coupling

| ID | RiskWorld value |
|---|---|
| E01 | ABSENT for hypothetical action; world rollout is conditioned on observed history only |
| E02 | past/current ego motion is part of state, but no future action injection carrier exists |
| E03 | RSSM dynamics parameters shared across object branches |
| E04 | object branch persists over H physical future steps |
| E05 | alternative ego actions are outside model support/evaluation |

# F. Dynamics / future time

| ID | RiskWorld value |
|---|---|
| F01 | compact object-centric deterministic + stochastic latent states |
| F02 | future ego-relative position/distance plus learned temporal-risk semantics |
| F03 | RSSM-style prior/posterior + GRU recurrent dynamics |
| F04 | recurrent explicit multi-step physical future rollout |
| F05 | H=60 steps = 3 s at 20 FPS |
| F06 | stochastic latent during training; inference uses means; no calibrated multi-modal future distribution reported |
| F07 | observed-history → unseen physical future relation sequence |
| F08 | rollout index k corresponds to physical future time; posterior/prior sampling mechanics are not a separate physical clock |

# G. Future supervision / truth

| ID | RiskWorld value |
|---|---|
| G01 | logged factual future ego/object tracks provide position/distance truth |
| G02 | direct supervised future relation labels + event-derived risk labels; no EMA target network central to method |
| G03 | future tracks correspond to the executed/logged episode only |
| G04 | event annotation defines object risk and shaped temporal-risk target; no candidate utility teacher |
| G05 | no expert trajectory imitation role |
| G06 | no action-branch factual assignment |
| G07 | all valid object branches with available logged future steps receive relation supervision; object risk label coverage follows RiskBench annotations |
| G08 | reactive alternative-agent intervention truth ABSENT |

# H. Branch identity / assignment

| ID | RiskWorld value |
|---|---|
| H01 | observed object identity |
| H02 | tracked object token identity persists through rollout |
| H03 | no factual action-mode assignment; risk source annotation is object-level supervision |
| H04 | object support/validity, not best-of-N ego planning support |

# I. Counterfactuality / reactivity

| ID | RiskWorld value |
|---|---|
| I01 | NO action-candidate-specific future outputs; YES object-specific future outputs |
| I02 | NO alternative-action future supervision |
| I03 | NO intervention world-state GT |
| I04 | NO validated reactive other-agent response to changed ego action |
| I05 | intervention validity NOT EVALUATED; paper lists planner-conditioned counterfactual rollout as future work |

# J. World → planning interface

| ID | RiskWorld value |
|---|---|
| J01 | no direct planner conditioning/scoring path; world rollout feeds risk identification |
| J02 | YES future/world computation online inside risk monitor |
| J03 | consumed online by risk heads, NOT by planner |
| J04 | forward: current object world → future relation rollout → risk; backward: risk/relation losses shape dynamics; no planning gradient |
| J05 | object risk threshold/ranking, not action selection |
| J06 | consequence representation + risk classifier; no decision/planning value model |
| J07 | future annotations training-only; latent rollout/risk head remain online |
| J08 | recurrent rollout steps advance physical future time, not iterative planner refinement |
| J09 | planner→world feedback carrier ABSENT |

# K. Scorer semantics

| ID | RiskWorld value |
|---|---|
| K01 | explicit object-risk classifier and temporal-risk head, not trajectory scorer |
| K02 | risk-source probability / event-timing semantics, not utility/reward |
| K03 | risk heads consume object latent future sequence/pooled state |
| K04 | final object risk + time-indexed temporal risk + physical relation heads |
| K05 | object/event annotations + logged future geometry; not PDM/value labels |

# L. Training topology

| ID | RiskWorld value |
|---|---|
| L01 | joint downstream training with composite risk/relation/KL objective; V-JEPA2 frozen |
| L02 | relation-aware object state shared by latent dynamics and risk/relation decoders |
| L03 | pretrained encoder, structured encoder, relation attention, RSSM dynamics and heads are functionally distinct modules |
| L04 | L_obj/L_curve/L_xy/L_dist/L_min shape downstream world/risk modules; no planner gradient path |
| L05 | frozen foundation encoder; no reported stage-wise deployment distillation |
| L06 | L_obj + L_xy + L_dist + L_min + L_curve + βL_KL |
| L07 | all recurrent future states are decoded/supervised where logged targets are valid; exact source implementation unavailable |

# M. Future-knowledge lifecycle

| ID | RiskWorld value |
|---|---|
| M01 | frozen predictive-video prior → supervised relation/risk world model → online risk monitor |
| M02 | online object-wise 3 s latent rollout |
| M03 | logged futures are training-only; rollout and risk decoder retained at inference |
| M04 | no separate future-model distillation/compression stage |
| M05 | highly inspectable outputs: object score, position, distance, temporal-risk curve, min distance, time-to-risk |
| M06 | single history-only risk-monitor mode; no planner-candidate sibling mode reported |

# N. Compute / pruning

| ID | RiskWorld value |
|---|---|
| N01 | up to 64 object branches × 60 recurrent future steps |
| N02 | frozen ViT-L encoder + relation attention + object-wise RSSM + heads online |
| N03 | no deployment pruning/distillation reported |
| N04 | object-wise shared dynamics are structurally parallelizable but implementation behavior SOURCE-UNVERIFIED |
| N05 | runtime/latency NOT REPORTED in audited text |
| N06 | no compute-vs-object-count or horizon trade-off study central to paper |

# O. Evaluation / attribution

| ID | RiskWorld value |
|---|---|
| O01 | RiskBench CARLA simulation dataset; primary task is frame-wise risk identification, not closed-loop planning |
| O02 | future-risk Brier analysis directly evaluates temporal-risk prediction; future physical relation fidelity not comprehensively benchmarked as a standalone dynamics task |
| O03 | factual logged future relation + object/event annotations |
| O04 | strongest dynamics control: w/o future rollout 60.2 → full 63.0 overall F1 |
| O05 | future supervision control: 61.6 → 63.0; stochastic vs deterministic: 62.0 → 63.0 overall |
| O06 | largest overall gaps arise from representation/world-feature/object-token/relation-attention ablations, so final gain is not pure dynamics gain |
| O07 | planning-aware LBC masking evaluates relevance of selected objects, not planner improvement |
| O08 | paper evidence available; official source NOT IDENTIFIED |

# P. Safety / uncertainty / interaction / physical validity

| ID | RiskWorld value |
|---|---|
| P01 | YES explicit object-level risk and time-indexed risk state; NO continuous spatial risk field |
| P02 | explicit risk monitor, but NOT an online trajectory safety/value evaluator |
| P03 | stochastic latent exists but no calibrated uncertainty/risk interval claim |
| P04 | explicit object–ego and object–object relational context; no intervention-reactive dynamics validation |
| P05 | future relative position/distance gives geometric physical grounding; no formal dynamics-law constraint |
| P06 | 60-step recurrent rollout is evaluated through future-risk Brier and task performance, but long-horizon state-drift calibration is not independently established |
| P07 | event/risk semantics explicitly enter supervision through annotated risk source and temporal event curve |

---

# Final normalized identity

```text
RiskWorld
=
16-frame front RGB + tracks + ego motion
→ frozen V-JEPA2 global/object visual features
→ structured object/ego state
→ relation attention
→ object-indexed current world tokens
→ RSSM-style stochastic/deterministic 60-step rollout
→ future relative position / distance / temporal-risk sequence
→ pooled object-risk probability
→ identify risk source

SUPERVISION:
logged factual ego/object future relation   YES
object risk annotation                      YES
event-timing risk curve                     YES
alternative ego-action future truth         NO
reactive intervention truth                 NO

PLANNING:
direct online planning interface            ABSENT
filtered-observation planning relevance     EVALUATED
```

Ontology decision:

```text
V1.3 RETAINED
NO V1.4
```

RiskWorld primarily strengthens already-existing distinctions:

```text
P01 explicit risk state
J02/J03 future computation vs planner consumption
I01–I05 counterfactual/reactivity vector
F04/F05 physical multi-step rollout
G03/G08 factual vs intervention truth
```
