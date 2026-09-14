# PHASE_B_ANCHORS — Representative Deep-Read Set

Last updated: 2026-09-14

Status: **PHASE-A FROZEN / PHASE-B READY**

Purpose: define the minimum representative deep-read set needed to explain the planning-centric WAM field without returning to hypothesis-driven paper selection. These papers are selected for **historical/architectural explanatory value**, not because they support or attack P1/P2-R/P3.

## Selection principles

An anchor is included only if it contributes at least one of the following:

```text
establishes a historical transition
represents a major world-state / planner-interface family
provides a strong non-WM control
changes the interpretation of evaluation evidence
represents a distinct use of WM (pretraining / inference / scoring / RL simulator / unified action-world)
provides a necessary counterexample to over-general field claims
```

A census paper can be scientifically important without needing full deep-read treatment. Redundancy is intentional to remove.

## Final Phase-B set — 25 anchors

| # | anchor | why it is necessary to explain the field | deep-read redundancy it absorbs |
|---:|---|---|---|
| 1 | **M2I** | Establishes conditional influencer→reactor interaction prediction before modern WAM terminology. | Many marginal/conditional prediction papers need only census-level reference. |
| 2 | **GameFormer** | Represents explicit game-theoretic interactive prediction + ego planning in one architecture and connects prediction research to planning. | Covers much of the intermediate “joint prediction/planning” lineage at concept level. |
| 3 | **What Truly Matters in Trajectory Prediction?** | Makes downstream driving and dynamics/evaluation mismatch an explicit research object; essential for understanding why prediction metrics stopped being enough. | Avoids deep-reading many isolated prediction-metric critiques. |
| 4 | **UniAD** | Canonical planning-oriented unified E2E baseline before the current WAM wave; needed to know what WM methods actually add beyond a strong multitask planning stack. | VAD and other 2023 unified-stack variants remain secondary comparisons. |
| 5 | **DiffusionDrive** | Strong modern direct generative trajectory policy without explicit WM; controls for gains from action-distribution modeling alone. | Several diffusion/action-only planners can remain census depth. |
| 6 | **DriveSuprim** | Strong modern candidate-selection/scoring planner without explicit WM; exposes hard-negative discrimination and selection precision as independent planning axes. | Hydra-MDP remains an important precursor but does not need equal deep-read depth unless teacher-distillation details become central. |
| 7 | **GAIA-1** | Foundational large generative driving WM anchor; establishes the early “model the driving world” vision before planning interfaces became mature. | DriveDreamer/DriveDreamer-2 can remain supporting visual-WM references. |
| 8 | **Drive-WM** | Important bridge from controllable multiview visual forecasting to imagined-future planning/evaluation. | Vista can remain supporting evidence unless generalized action-evaluator behavior becomes central. |
| 9 | **Epona** | Major autoregressive diffusion WM + trajectory-planning anchor; useful for studying unified latent history, trajectory generation, visual generation and shared conditioning. | Some later video-WM variants become secondary once this interface is understood. |
| 10 | **DrivingGPT** | Represents the transition from separate visual generation/planning modules to an interleaved multimodal autoregressive world-action sequence model. | Reduces need to deep-read every tokenized world-action variant. |
| 11 | **OccWorld** | Canonical structured alternative to RGB: future 3D occupancy and ego movement modeled jointly. | Several pure occupancy-forecasting variants can remain census depth. |
| 12 | **WoTE** | Clean example of future BEV world prediction used online to evaluate/select ego trajectories. | Drive-OccWorld/World4Drive become targeted secondary comparisons for controllability/intention variants. |
| 13 | **ViDAR** | Clean example where future world prediction is a **pretraining objective**, not an inference-time planner; crucial to separate representation learning from deployment-time world modeling. | DriveWorld and other pretraining WMs can be compared selectively rather than all deep-read. |
| 14 | **LAW** | Early planning-centric latent WM where future latent prediction self-supervises planning representation; a key latent-WM bridge. | Some auxiliary-latent-prediction methods become secondary. |
| 15 | **DriveLaW** | Strong example where hidden world/video-model features are consumed directly by action generation, challenging the idea that explicit rollout/value interfaces are required. | Several video-latent planner variants become secondary controls. |
| 16 | **Auto-JEPA** | Represents deliberate compression of the future toward continuous planning intent rather than dense world reconstruction. | Drive-JEPA / ReWorld / WA-JEPA / WorldRFT remain a comparison cluster to promote only if representation-shaping differences require it. |
| 17 | **DA-WAM** | Strongest current candidate-specific future-latent → candidate-score interface in the corpus; separates per-action future modeling from direct decoding. | SafeDrive/World4Drive support neighboring interfaces; deep read only if needed for safety/physical-state contrast. |
| 18 | **Think2Drive** | Essential independent lineage where a latent WM is a Dreamer-style neural simulator for RL policy improvement, not a representation consumed by a deployed raw-sensor planner. | Other model-based driving RL papers become secondary unless they change this lineage. |
| 19 | **nuPlan** | Foundational planning benchmark defining OL, closed-loop non-reactive and reactive evaluation concepts on real-log planning data. | Avoids treating later evaluation terminology as if it originated in WAM papers. |
| 20 | **NAVSIM** | Defines the scalable real-data non-reactive pseudo-simulation regime that dominates many recent planning results and score-distillation methods. | NAVSIM-v2 can be added only if metric/protocol evolution becomes decision-critical. |
| 21 | **Bench2Drive** | Canonical modern interactive CARLA closed-loop E2E benchmark with standardized data and granular scenarios. | Many CARLA leaderboard papers can remain benchmark context. |
| 22 | **HUGSIM** | Represents reconstructed real-scene photorealistic closed-loop simulation, distinct from both CARLA and NAVSIM. | DriveArena/SLEDGE remain supporting simulator branches. |
| 23 | **ORION** | Strong VLA/VLM planning control: semantic reasoning → planning token → generative multimodal trajectory with Bench2Drive evidence, without an explicit future WM. | DriveVLM and OmniDrive remain important supporting VLA/data references; they need not both be full anchors initially. |
| 24 | **ReactSim-Bench** | Directly evaluates behavioral validity of reactive world agents under AV deviation; needed to understand what “reactive simulation” actually tests. | BridgeSim remains a targeted evaluation/cause-analysis reference. |
| 25 | **CausalDrive** | Represents the newer reactive/causal WM method family itself, complementing ReactSim-Bench’s benchmark perspective. | CRAFT remains a useful policy-training/counterfactual correction reference rather than core anchor initially. |

## Deliberately secondary but scientifically retained

These papers stay in the atlas/corpus and are promoted to full deep read only if an anchor exposes a concrete unresolved comparison:

```text
DriveDreamer / DriveDreamer-2 / Vista
Drive-OccWorld / World4Drive
DriveWorld
Drive-JEPA / ReWorld / WA-JEPA / WorldRFT
WorldDrive
Hydra-MDP / iPad
DriveVLM / OmniDrive
GenAD
SafeDrive / BeTop / GraphAD / RiskWorld
Gen-Drive / DriveReward / TOAD / NPPC
BridgeSim / CRAFT
SLEDGE / DriveArena
VAD / DrivoR
```

“Secondary” means redundant for the first explanatory pass, not weak or unimportant.

## Reading waves

Phase B should proceed by **comparative waves**, not 25 isolated summaries.

### Wave 1 — historical roots, strong controls, and evaluation foundations

```text
M2I
GameFormer
What Truly Matters
UniAD
nuPlan
NAVSIM
DiffusionDrive
DriveSuprim
```

Goal: establish what planning, interaction, multimodality, evaluation and strong non-WM performance already meant **before** interpreting WM gains.

Required output after Wave 1: one synthesis memo answering:

- what problems existed before the modern WAM wave;
- which were prediction problems vs planning problems vs evaluation problems;
- what a strong non-WM planner can already achieve;
- what NAVSIM/nuPlan metrics actually reward;
- which later WM claims would be meaningless without these controls.

### Wave 2 — world representation and future-state interfaces

```text
GAIA-1
Drive-WM
OccWorld
WoTE
ViDAR
LAW
```

Goal: compare video, occupancy/BEV, pretraining-only future prediction and latent future prediction using one common observation→future→planner description.

### Wave 3 — unified / compressed / candidate-specific / RL world-action modeling

```text
Epona
DrivingGPT
DriveLaW
Auto-JEPA
DA-WAM
Think2Drive
```

Goal: understand how “world model” changes role from generation to hidden feature, compressed predictive state, per-action latent, joint world-action model and RL simulator.

### Wave 4 — closed-loop, VLA, and reactive-world evidence

```text
Bench2Drive
HUGSIM
ORION
ReactSim-Bench
CausalDrive
```

Goal: separate semantic reasoning, simulator realism, traffic reactivity, world-agent behavioral validity and actual policy closed-loop evidence.

## Phase-B deep-read contract

Each anchor must eventually record:

```text
1. Exact problem in historical context
2. Observation/input representation
3. Exact future/world representation, if any
4. Training supervision: observed future vs proxy vs inferred/counterfactual
5. Inference-time data flow: observation → representation/future → planner/action
6. Whether the WM/future branch survives deployment
7. Planner interface: direct decode / score / optimize / rollout / RL
8. Multimodality/uncertainty representation and whether planning consumes it
9. Evaluation regime and what that regime can/cannot establish
10. Strongest direct experimental evidence
11. Strongest limitation / alternative explanation
12. What the paper proves and does NOT prove
13. Historical transition role
14. Closest supporting and contradicting/counterexample papers
```

Use `AUTHOR CLAIM / DIRECT EXPERIMENTAL EVIDENCE / OUR INFERENCE` separately.

## Phase-A closeout decision

```text
CENSUS BREADTH: SUFFICIENT
F1–F11 COVERAGE: SUFFICIENT FOR ANCHOR SELECTION
BROAD INGESTION: FROZEN
PHASE B: AUTHORIZED
GAP / METHOD DESIGN: NOT AUTHORIZED
```

New papers may still be added, but only because a Phase-B comparison exposes a named missing historical or technical link—not because the corpus has room for more papers.