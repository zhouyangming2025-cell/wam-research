# P0007 DriveReward — Ontology V1 + V1.1 + V1.2 + V1.3 Projection

Last updated: 2026-09-16

Status: **FULL DIMENSION-FIRST PROJECTION — COMPLETE FIRST PASS**

Canonical analysis:

```text
papers/deep_analysis/P0007_DRIVEREWARD_DEEP_ANALYSIS_V2.md
audits/literature/PHASE_C6_DRIVEREWARD_AUDIT.md
```

Core warning:

```text
candidate-specific reward/value
!=
candidate-specific future-world prediction
```

---

# A. Problem / role

| ID | DriveReward value |
|---|---|
| A01 | multimodal trajectory valuation and scalable RL reward provision |
| A02 | direct semantic value/reward model; no explicit future-world mediator |
| A03 | candidate ranking / RL reward teacher; host planner can be multimodal policy or VLA/RL policy |
| A04 | learned cost/value + VLM semantic evaluator + RL reward modeling lineage |

# B. Current-state representation

| ID | DriveReward value |
|---|---|
| B01 | front-view RGB / short visual context + text-carried route, ego state and candidate trajectory |
| B02 | paper wording is ambiguous between current image and short historical video / 3-frame context |
| B03 | InternVL3 visual-language hidden representation |
| B04 | semantic scene context + geometric prior + route/action semantics |
| B05 | current/history representation only; no explicit predicted future state is consumed |

# C. Representation provenance

| ID | DriveReward value |
|---|---|
| C01 | InternVL3-1B foundation VLM + VGGT geometric foundation model |
| C02 | domain QA pretraining + geometry-latent alignment + task-specific reward SFT |
| C03 | paper states frozen visual backbone in experiment setup; appendix `full parameter fine-tuning` wording creates unresolved trainability ambiguity |
| C04 | w/o pretraining and w/o 3D adapter provide partial attribution; full reward quality remains bundled with VLM prior and task supervision |

# D. Action / candidate space

| ID | DriveReward value |
|---|---|
| D01 | candidate provenance: GT/logged + offline kinematic retrieval + planner-generated; test-time AdaThinkDrive uses 4 independently generated proposals |
| D02 | future ego trajectory encoded in textual/multimodal query; trajectory shape T×3 reported |
| D03 | navigation instruction explicitly present; command-following is also a reward dimension |
| D04 | explicit candidate pool exists in dataset and test-time scorer use; RL also evaluates policy-generated trajectories |
| D05 | dataset deliberately enriches suboptimal/diverse action support; exact global candidate count varies by use |
| D06 | direct value scoring / selection; no world-model-based pruning stage |

# E. Action → world coupling

| ID | DriveReward value |
|---|---|
| E01 | **ABSENT as explicit world prediction**; candidate affects reward prediction directly |
| E02 | candidate trajectory enters evaluator prompt/context, not a transition model |
| E03 | each candidate is evaluated by shared reward model; no candidate-specific world branch |
| E04 | NOT APPLICABLE — no temporal world rollout branch |
| E05 | candidate support includes non-expert/suboptimal proposals, but extrapolation validity is evaluated only through reward/planning metrics |

# F. Dynamics / future time

| ID | DriveReward value |
|---|---|
| F01 | no future-world substrate; output is reward/reasoning tokens |
| F02 | trajectory quality semantics: safety, drivable compliance, TTC, progress, comfort, command following, legality |
| F03 | autoregressive VLM evaluator, not a world dynamics operator |
| F04 | NOT APPLICABLE for world evolution |
| F05 | candidate trajectory has a future horizon, but no predicted intermediate environment states are produced |
| F06 | no explicit world uncertainty/multimodality model; reward uncertainty not calibrated |
| F07 | NOT APPLICABLE as future-world prediction; evaluator sees proposed trajectory and current/history context |
| F08 | NOT APPLICABLE — language-token generation steps are not claimed as physical world time |

# G. Future supervision / truth

| ID | DriveReward value |
|---|---|
| G01 | no direct future-world target; reward targets derive from simulator/rules/VLM teacher |
| G02 | VGGT latent alignment is geometric representation supervision, not future target encoding |
| G03 | no factual future scene target for each candidate |
| G04 | NC/DAC/TTC/EP/Comfort from PDM/NAVSIM-style metrics; CF deterministic rule; LG and reasoning from Qwen3.5 teacher |
| G05 | GT trajectory participates as candidate/source and CF reference; main target is value, not pure imitation |
| G06 | candidate-specific reward labels exist; no factual alternative-world assignment |
| G07 | candidate reward coverage intentionally spans optimal/suboptimal proposals; exact coverage varies by label pipeline |
| G08 | reactive alternative-agent intervention truth ABSENT |

# H. Branch identity / assignment

| ID | DriveReward value |
|---|---|
| H01 | ego trajectory candidate identity |
| H02 | candidate trajectory retained explicitly in evaluator input |
| H03 | no factual future-mode assignment; reward labels rank/evaluate candidate quality |
| H04 | Best-of-N oracle exposes selection headroom; reward model recovers only a small portion in reported N=4 experiment |

# I. Counterfactuality / reactivity

| ID | DriveReward value |
|---|---|
| I01 | candidate-specific output YES, but output is reward/value not future world |
| I02 | alternative-action reward supervision YES; alternative-action future-world supervision NO |
| I03 | intervention world-state GT ABSENT |
| I04 | reactive other-agent response truth ABSENT |
| I05 | intervention validity is evaluated indirectly through simulator/rule reward and downstream policy metrics, not through predicted world-state accuracy |

# J. World → planning interface

| ID | DriveReward value |
|---|---|
| J01 | no world predictor; learned reward connects current semantic context + candidate directly to decision utility |
| J02 | no online future/world computation |
| J03 | online reward model is consumed by planner only in test-time scoring mode; in RL mode it is a training-time teacher |
| J04 | training-time reward → policy update; no explicit world↔planner forward loop |
| J05 | candidate ranking at test time; scalar/factorized reward for RL training |
| J06 | explicit value/reward model |
| J07 | dual lifecycle: training-only teacher for RL OR retained online scorer for reranking |
| J08 | autoregressive reward-token generation is model decoding, not physical-time rollout/planner-world refinement |
| J09 | planner→world feedback NOT APPLICABLE; candidate trajectory is evaluator input, not a world-state feedback carrier |

# K. Scorer semantics

| ID | DriveReward value |
|---|---|
| K01 | explicit learned trajectory reward/scorer |
| K02 | hybrid value semantics: safety + progress + comfort + command compliance + legality |
| K03 | scorer consumes current/history visual-language representation + ego trajectory directly |
| K04 | factorized seven-dimensional reward plus reasoning; aggregate PDMS/hybrid reward composed downstream |
| K05 | heterogeneous teacher stack: simulator metrics, deterministic rules, VLM semantic labels/reasoning |

# L. Training topology

| ID | DriveReward value |
|---|---|
| L01 | stage-1 domain adaptation → stage-2 reward SFT; separate downstream policy RL experiments |
| L02 | shared VLM hidden representation supports reasoning and reward-token outputs; geometry auxiliary representation aligned to VGGT |
| L03 | InternVL vision encoder / LLM / geometry adapter functionally separable; exact trainability partially ambiguous without code |
| L04 | reward-model gradients train evaluator during SFT; downstream policy receives reward through RL objective; no evidence of policy gradient updating reward model |
| L05 | paper states vision backbone frozen in experimental setup; appendix wording leaves exact stage-wise trainability unresolved |
| L06 | next-token reasoning/reward supervision + geometry L2 alignment; policy RL uses predicted/hybrid scalar rewards |
| L07 | NOT APPLICABLE — no recurrent world/planner refinement states |

# M. Future-knowledge lifecycle

| ID | DriveReward value |
|---|---|
| M01 | semantic/geometric driving knowledge → reward evaluator → either distilled into policy through RL or retained as test-time scorer |
| M02 | no future-world model online |
| M03 | RL mode: reward evaluator can be absent at deployment; scorer mode: evaluator remains online |
| M04 | no world-model distillation; RL is value/reward-to-policy transfer |
| M05 | highly inspectable factorized reward + textual reasoning, though reasoning faithfulness is not independently established |
| M06 | two operational modes: training-time reward teacher / online trajectory scorer |

# N. Compute / pruning

| ID | DriveReward value |
|---|---|
| N01 | one VLM evaluation per candidate / policy sample; test-time N scales evaluator calls |
| N02 | InternVL3-1B reward model online only when scorer mode is used |
| N03 | RL mode removes reward-model inference from deployed policy; no separate scorer distillation reported |
| N04 | candidate evaluations can in principle batch; implementation unavailable |
| N05 | real-time latency / FPS for reward scoring NOT REPORTED in audited text |
| N06 | no systematic candidate-count/latency frontier; Best-of-4 only exposes selection headroom |

# O. Evaluation / attribution

| ID | DriveReward value |
|---|---|
| O01 | reward benchmark + NAVSIM-v1 non-reactive pseudo-simulation + Bench2Drive interactive CARLA closed loop + AdaThinkDrive test-time selection |
| O02 | reward prediction directly evaluated per dimension; no world-fidelity metric applicable |
| O03 | reward truth is teacher-derived heterogeneous target, not physical future observation |
| O04 | strongest evaluator ablation: removing reasoning CoT causes largest degradation |
| O05 | strongest planning evidence: RL reward improves multiple SFT policies; test-time scoring gain is only +0.2 PDMS vs +2.7 Best-of-N headroom |
| O06 | final planning gain bundles reward quality, RL algorithm, base policy, candidate support and teacher semantics |
| O07 | NAVSIM and Bench2Drive evidence kept distinct; no real-vehicle closed-loop evidence |
| O08 | paper verified; official implementation not identified; dataset-scale/trainability/input-temporal ambiguities preserved |

# P. Safety / uncertainty / interaction / physical validity

| ID | DriveReward value |
|---|---|
| P01 | explicit safety-related factors NC/DAC/TTC plus legality; no spatial risk field |
| P02 | explicit trajectory value/safety evaluator |
| P03 | reward uncertainty/calibration NOT REPORTED |
| P04 | semantic interaction understanding may be implicit in VLM context, but no explicit reactive agent model |
| P05 | geometry grounding through VGGT + rule/simulator labels; no explicit physical dynamics constraint |
| P06 | no world rollout drift question; reward generalization tested across benchmarks but long-horizon value calibration not isolated |
| P07 | traffic-rule and command semantics explicitly enter reward supervision |

---

# Final normalized identity

```text
DriveReward
=
visual context + route + ego state + candidate trajectory
→ VLM semantic / geometric evaluator
→ factorized reward + reasoning
→ RL policy supervision OR test-time candidate selection

explicit future-world state             NO
candidate-specific direct value          YES
candidate-specific future-world truth    NO
reactive intervention truth              NO
world model required at deployment       NO
```

Ontology decision:

```text
V1.3 RETAINED
NO V1.4
```

DriveReward primarily strengthens the existing distinction between:

```text
consequence/world prediction
and
value/reward approximation
```
