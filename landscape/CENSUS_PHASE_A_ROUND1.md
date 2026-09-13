# FIELD CENSUS — Phase A Round 1

Last updated: 2026-09-14

Status: **BREADTH CENSUS, NOT GAP ANALYSIS**

Purpose: build the first neutral map of the planning-centric driving world-model field. Placement is provisional and will be revised after anchor deep reads. This file deliberately avoids research-gap verdicts.

## 0. Reading rule

Round 1 asks only:

```text
What family is this work in?
What future/world state does it model?
What role does that model play for planning?
How directly does future information reach the planner?
What evaluation regime supports the planning claim?
Why is the work historically useful for understanding the field?
```

It does **not** ask whether a paper exposes our next innovation.

Confidence labels:

- `HIGH`: placement checked against a primary paper/project source or repo-hosted primary text.
- `MEDIUM`: placement supported by abstract/project source; details still need paper-level verification.
- `LOW`: discovery only; do not use for synthesis until verified.

---

# 1. Visual / video generative world-model lineage

| work | year | provisional role in field | planning connection | confidence |
|---|---:|---|---|---|
| **GAIA-1: A Generative World Model for Autonomous Driving** | 2023 | Early large generative driving WM; multimodal video/text/action token sequence modeling | Mainly world generation / autonomy representation; planning value is prospective rather than a modern planner-interface proof | HIGH |
| **DriveDreamer: Towards Real-world-driven World Models for Autonomous Driving** | 2023/24 | Diffusion WM trained on real-world driving; structured constraints + future video/action capability | Demonstrates action interaction and driving-policy prediction, but its historical importance is primarily real-world controllable WM generation | HIGH |
| **Drive-WM: Driving into the Future: Multiview Visual Forecasting and Planning with World Model for Autonomous Driving** | 2023/24 | Important bridge from controllable multiview video WM to explicit planning over imagined futures | Different maneuvers produce different futures; image-based rewards support trajectory choice | HIGH |
| **Vista: A Generalizable Driving World Model with High Fidelity and Versatile Controllability** | 2024 | Generalizable high-fidelity driving video WM with controls ranging from command/goal to trajectory/speed/angle | Explores using the WM itself as a generalized action evaluator/reward; important bridge between generation and decision evaluation | HIGH |
| **DriveDreamer-2: LLM-Enhanced World Models for Diverse Driving Video Generation** | 2024/25 | Customized rare-scenario generation using language → trajectories → HD map → video | Planning connection is indirect; useful as a data-generation/simulation branch, not as a core planner architecture | HIGH |
| **Epona: Autoregressive Diffusion World Model for Autonomous Driving** | 2025 | Long-horizon autoregressive video WM unified with trajectory planning | Joint trajectory/video branches and real-time motion planning; major anchor for unified generation+planning | HIGH |
| **DrivingGPT: Unifying Driving World Modeling and Planning with Multi-modal Autoregressive Transformers** | 2025 | Interleaved image/action token language; replaces diffusion-only view with multimodal autoregressive modeling | World modeling and planning are cast as one sequence-prediction problem | HIGH |
| **Policy World Model: From Forecasting to Planning via Collaborative State-Action Prediction** | 2025 | Video/world forecasting explicitly inserted as a planning rationale | Action-free future forecasting is consumed before action prediction; useful counterpoint to action-conditioned WMs | MEDIUM |
| **WorldDrive: Bridging Scene Generation and Planning via Unifying Vision and Motion Representation** | 2026 | Explicit attempt to make video-WM representations planner-inheritable | Transfers vision/motion encoders to planner and adds a future-aware rewarder from frozen WM latent | HIGH |

**Round-1 observation:** visual-generation work evolves through at least three roles that must not be conflated: `generation/data engine → controllable imagined future → planner-consumed representation/evaluator → unified world-action model`.

---

# 2. Occupancy / BEV / geometric world-model lineage

| work | year | provisional role in field | planning connection | confidence |
|---|---:|---|---|---|
| **OccWorld: Learning a 3D Occupancy World Model for Autonomous Driving** | 2023/24 | Jointly models future 3D occupancy and ego movement in discrete scene-token space | Produces ego trajectory jointly with occupancy evolution; important structured alternative to RGB world modeling | HIGH |
| **Drive-OccWorld: Driving in the Occupancy World** | 2024/25 | Extends occupancy forecasting toward action-controllable continuous forecasting/planning | Observation + trajectory conditioning; explicitly integrates occupancy WM with planner | HIGH |
| **WoTE: End-to-End Driving with Online Trajectory Evaluation via BEV World Model** | 2025 | Latency-oriented BEV future model designed specifically for online trajectory evaluation | Predicted future BEV states are used to evaluate/select trajectories; evaluated on NAVSIM and Bench2Drive | HIGH |
| **World4Drive: End-to-End Autonomous Driving via Intention-aware Physical Latent World Model** | 2025 | Hybrid latent/physical representation with multiple intention-driven future states | Generates multimodal trajectories, predicts intention-conditioned future latents, then uses a WM selector | HIGH |
| **GraphAD: Interaction Scene Graph for End-to-End Autonomous Driving** | 2024/25 | Not a canonical WM paper, but explicit future-trajectory graph reasoning is an important structured-state predecessor/boundary | Future motion geometry refines interaction edges; final plan uses graph-processed ego feature; occupancy post-optimization materially contributes to safety | HIGH |

**Round-1 observation:** geometric/BEV families trade pixel-level richness for structured state that can enter planning more directly. This is a field-design choice to understand, not a priori evidence that one representation is superior.

---

# 3. Latent / predictive-representation / JEPA lineage

| work | year | provisional role in field | planning connection | confidence |
|---|---:|---|---|---|
| **DriveWorld: 4D Pre-trained Scene Understanding via World Models for Autonomous Driving** | 2024 | WM as spatiotemporal self-supervised pretraining for a broad autonomous-driving stack | Planning improvement is downstream representation transfer, not necessarily inference-time future rollout | HIGH |
| **LAW: Enhancing End-to-End Autonomous Driving with Latent World Model** | 2024/25 | Early planning-centric latent WM using future-feature prediction as self-supervision | Predicts future latent features from current features + ego trajectory; self-supervision improves planner representation | HIGH |
| **DriveLaW** | 2026 | Video/world latent directly coupled to action generation; strong world-action style planning anchor | Planner consumes hidden Video-DiT features during action denoising rather than requiring explicit completed visual rollout | HIGH (repo reverified previously) |
| **Drive-JEPA: Video JEPA Meets Multimodal Trajectory Distillation for End-to-End Driving** | 2026 | Predictive video representation + proposal-centric multimodal trajectory distillation | Uses V-JEPA representation as planning feature; adds simulator-generated multimodal trajectory supervision | HIGH |
| **WorldRFT: Latent World Model Planning with Reinforcement Fine-Tuning** | 2026 | Planning-oriented latent representation + hierarchical planning + RL fine-tuning | Explicitly aligns latent representation learning with planning and adds collision-aware GRPO-style RFT | HIGH |
| **Auto-JEPA: A Latent World Model of Continuous Intent for End-to-End Autonomous Driving** | 2026 | Deliberately compresses future into planning-relevant intent rather than reconstructing dense world state | Predicts continuous intent embedding aligned with future ego trajectory; retrieves/ranks trajectories from memory | HIGH |
| **ReWorld: Learning Better Representations for World Action Models** | 2026 | Intermediate-representation supervision specifically for WAMs | Shapes Video-DiT and Action-DiT internal representations with future prediction, cross-modal alignment, and hard negatives | HIGH |
| **WA-JEPA: Rethinking the Video JEPA Paradigm for World-Action Modeling in Autonomous Driving** | 2026 | Future-masked JEPA + flow-based latent future + joint world/action denoising | Future scene tokens and ego trajectory are jointly modeled in one latent space; includes NAVSIM and HUGSIM evidence | HIGH |
| **DA-WAM: Decision-Aligned Future Latents for Driving World Models** | 2026 | Candidate-specific future latent as explicit decision interface | Distinct latent per candidate enters factorized scorer; expert-matched future gets direct latent supervision | HIGH |

**Round-1 observation:** the latent family is not one idea. At least four distinct roles already appear: `pretraining-only representation`, `auxiliary future supervision`, `future latent retained at inference`, and `world-action joint latent used directly for action selection`.

---

# 4. Interactive prediction / planning lineage before and beside modern WAMs

| work | year | provisional role in field | why it matters for field understanding | confidence |
|---|---:|---|---|---|
| **M2I: From Factored Marginal Trajectory Prediction to Interactive Prediction** | 2022 | Influencer→reactor conditional interaction prediction | Shows conditional response modeling predates current WAM terminology | HIGH |
| **GameFormer: Game-theoretic Modeling and Learning of Transformer-based Interactive Prediction and Planning** | 2023 | Hierarchical game-theoretic response reasoning + joint prediction/planning | Important bridge from interactive prediction to planner-level closed-loop evaluation | HIGH |
| **What Truly Matters in Trajectory Prediction for Autonomous Driving?** | 2023 | Evaluation study exposing mismatch between static prediction metrics and downstream driving | Establishes a "dynamics gap": ego policy changes surrounding-agent behavior; benchmark design can hide this | HIGH |
| **BeTop: Reasoning Multi-Agent Behavioral Topology for Interactive Autonomous Driving** | 2024 | Explicit future behavioral topology + contingency planning | Demonstrates OL / closed-loop non-reactive / reactive evaluation and explicit interaction structure | HIGH (repo reverified) |
| **GraphAD** | 2024/25 | Future-geometry-driven interaction graph in E2E stack | Useful structured interaction bridge, although not a reactive per-action world simulator | HIGH |

**Round-1 observation:** a substantial fraction of what modern WAM papers call interaction, conditional response, contingency, or reactive reasoning has intellectual predecessors in integrated prediction/planning. The atlas must track conceptual inheritance, not only paper names.

---

# 5. Reactive simulation / world-model environment lineage

| work | year | provisional role | planning/evaluation role | confidence |
|---|---:|---|---|---|
| **nuPlan** | 2022/23 | Large-scale planning dataset + lightweight closed-loop simulator | Historical benchmark anchor for moving beyond ego L2 open-loop evaluation | HIGH |
| **SLEDGE: Synthesizing Driving Environments with Generative Models and Rule-Based Traffic** | 2024 | Generative planning simulator from real logs; learned scene generation + rule traffic | Creates hard controllable planning environments; simulation/data-generation branch rather than policy WM | HIGH |
| **NAVSIM** | 2024 | Scalable real-log **non-reactive** pseudo-simulation / planning benchmark | Central to 2024–26 planning-WM claims; its non-reactivity must always be remembered | HIGH |
| **Bench2Drive** | 2024 | Multi-ability CARLA closed-loop E2E benchmark | Important interactive closed-loop evidence source; different domain from real-log NAVSIM | HIGH |
| **HUGSIM** | 2025/26 | Photorealistic real-time closed-loop simulator using reconstructed real scenes | Adds closed-loop visual realism; increasingly used by 2026 planners/WAMs | HIGH |
| **DriveArena** | 2024/25 | Closed-loop generative simulation platform for vision-based driving agents | Important generative-simulator branch; dynamically updates ego/actor states | MEDIUM |
| **BridgeSim** | 2026 | Studies open-loop→closed-loop gap in E2E planning | Evaluation/causal-diagnosis branch; currently parked from prior P2-R program but retained in atlas | MEDIUM until full paper deep read |
| **ReactSim-Bench** | 2026 | Benchmarks reactive behavior of world-agent simulation under AV deviations | Directly relevant to behavioral validity of learned reactive worlds | MEDIUM until full paper deep read |
| **CausalDrive** | 2026 | Reactive/causal driving WM conditioned on ego trajectory | Represents newer attempt to replace oracle/logged NPC future with generated reaction | MEDIUM until full paper deep read |
| **CRAFT** | 2026 | Counterfactual proxy training + interactive correction for policy improvement | Bridges offline counterfactual supervision and grounded closed-loop learning | MEDIUM until full paper deep read |

**Round-1 observation:** "closed-loop" is not one regime. The atlas must keep apart `non-reactive log-based pseudo-simulation`, `rule-based reactive simulation`, `learned reactive world agents`, `photorealistic reconstructed simulation`, and `real-vehicle closed loop`.

---

# 6. Reward / value / safety / trajectory-evaluation interfaces

| work | year | provisional role | field value | confidence |
|---|---:|---|---|---|
| **SafeDrive** | 2026 | Candidate-conditioned sparse world + pairwise collision / drivability reasoning | Strong example of explicit fine-grained safety interface inside E2E planning | HIGH |
| **Gen-Drive** | 2026 | Learned reward from generated future scenes + rules / preference supervision | Demonstrates learned world knowledge can be turned into policy reward; also raises optimization-stability questions | HIGH (repo prior deep read) |
| **DriveReward** | 2026 | Candidate-conditioned learned multidimensional reward/evaluator | Useful evidence that candidate quality and candidate ranking are separable bottlenecks | HIGH (repo prior deep read) |
| **RiskWorld** | 2026 | Object-centric latent rollout → object-level risk monitor | Boundary case: planning-relevant future relations without being a planner itself | HIGH |
| **NPPC** | 2026 | Continuous learned planning cost + dense candidate supervision/refinement | Important non-WM/explicit-cost counterexample for understanding value interfaces | MEDIUM until source is re-obtained |
| **TOAD / DrivoR context** | 2026 | Learned candidate scorer + test-time trajectory search/optimization | Strong planning-scoring baseline and robustness context; not inherently a world model | HIGH (repo source audit / CVPR DrivoR source) |

**Round-1 observation:** "world model for planning" sometimes means the future model itself is the planner, but sometimes means the WM feeds an evaluator, reward, safety model, or search procedure. Those are scientifically different interfaces.

---

# 7. Strong non-WM end-to-end planning controls

| work | year | role as control | why required in atlas | confidence |
|---|---:|---|---|---|
| **UniAD: Planning-Oriented Autonomous Driving** | 2023 | Unified full-stack perception→prediction→planning E2E baseline | Establishes strong planning-oriented architecture before modern WAM wave | HIGH |
| **VAD: Vectorized Scene Representation for Efficient Autonomous Driving** | 2023 | Efficient vectorized scene representation + planning constraints | Shows planning gains can come from representation/interface design without a future world model | HIGH |
| **DiffusionDrive** | 2025 | Fast multimodal diffusion trajectory policy | Demonstrates strong NAVSIM planning from action-distribution modeling, no explicit WM needed | HIGH |
| **DrivoR: Driving on Registers** | 2026 | Compact register representation + candidate generation/scoring | Strong modern non-WM candidate planner; important control against attributing gains to WM alone | HIGH |

Additional modern controls (Hydra-MDP, DriveSuprim, iPad, VLA planners) should be added in Round 2 after primary-source verification.

---

# 8. First historical skeleton

This is a **provisional chronology**, not a causal conclusion:

```text
2010s–2022: modular prediction/planning + conditional / game-theoretic interaction
        ↓
2022–2023: planning benchmarks + planning-oriented E2E stacks
        ↓
2023–2024: real-world generative driving WMs + occupancy WMs + WM pretraining
        ↓
2024–2025: planning explicitly consumes future BEV/latent/video information
        ↓
2025: unified video/action sequence models and stronger candidate evaluators
        ↓
2026: planning-oriented latent representations, JEPA/WAM representation learning,
      candidate-specific future latents, world-action joint models,
      reactive/counterfactual simulators, RL/post-training
```

The key task for later anchor deep reads is to verify **why each transition happened** and which limitations were genuinely resolved versus merely reframed.

---

# 9. Preliminary anchor-deep-read candidates

Not final. Chosen because together they expose different design choices rather than because they support any hypothesis.

### Historical / interaction controls

1. M2I
2. GameFormer
3. What Truly Matters
4. UniAD
5. NAVSIM

### Generative / visual WM anchors

6. GAIA-1
7. Drive-WM
8. Vista
9. Epona
10. DrivingGPT

### Structured / geometric anchors

11. OccWorld
12. Drive-OccWorld
13. WoTE
14. World4Drive

### Latent / representation / WAM anchors

15. LAW
16. DriveLaW
17. Drive-JEPA
18. WorldRFT
19. Auto-JEPA
20. ReWorld or WA-JEPA (one or both after comparative screening)
21. DA-WAM
22. WorldDrive

### Evaluation / reactive-world anchors

23. Bench2Drive
24. HUGSIM
25. ReactSim-Bench or CausalDrive (after full-paper verification)

This currently yields ~25 possible anchors; the final deep-read set should be reduced after Phase-A census reaches 50–80 works.

---

# 10. Missing coverage after Round 1

Round 1 is intentionally incomplete. Next census work should add and verify:

- more 2023–25 video-WM/data-engine papers (e.g. ViDAR / GenAD / DriveDreamer4D where planning relevance warrants inclusion);
- more occupancy/geometric WMs and their planning interfaces;
- strong 2025–26 non-WM E2E controls (Hydra-MDP family, iPad, DriveSuprim, VLA planners);
- world-model RL / Think2Drive lineage;
- real-vehicle closed-loop evidence, if any, rather than assuming benchmark gains transfer;
- efficiency/deployment comparisons;
- uncertainty / multimodal world-state modeling;
- dataset and benchmark lineage (nuScenes → nuPlan → NAVSIM → NAVSIM-v2 → Bench2Drive/HUGSIM);
- more explicit distinction between `pretraining world model`, `inference-time world model`, and `joint world-action policy`.

## Current census size

This round places **~45 unique works/benchmarks/control systems** across the atlas, with roughly 25 provisional anchors for later deep reading.

No research gap is claimed from this census.