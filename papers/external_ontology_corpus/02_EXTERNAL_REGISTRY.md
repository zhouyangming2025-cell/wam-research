# External Ontology Literature Registry

Status: **seed registry for breadth coverage**. This is not a deep-read claim.

Legend:

```text
C = census candidate
A = anchor candidate
D = decision-critical candidate
H = reserved holdout
RD0/RD1/RD2/RD3/RD4 = reading depth
```

The initial registry intentionally exceeds the original 12-paper derivation set and spans multiple research traditions. Entries discovered from maintained paper lists or surveys remain RD0/RD1 until checked against primary sources.

## 1. Foundational state / predictive-state / MBRL

| work | year | stratum | tier | depth | mechanism reason |
|---|---:|---|---|---|---|
| Dyna: Integrated Architecture for Learning, Planning, and Reacting | 1991 | model-assisted learning/planning | D | RD2 | separates model-generated planning updates from reactive execution |
| Predictive State Representations for Dynamical Systems | 2001 | predictive state | A | RD1 | state as predictions of future observables rather than hidden physical reconstruction |
| PILCO | 2011 | probabilistic model-based control | A | RD1 | uncertainty-aware learned dynamics + policy optimization |
| Value Prediction Network | 2017 | abstract dynamics / value rollout | D | RD2 | predicts reward/value-relevant abstract futures without observation reconstruction |
| TreeQN / ATreeC | 2018 | differentiable tree planning | D | RD2 | learned abstract transition + online lookahead tree |
| World Models | 2018 | latent recurrent world model | D | RD2 | controller consumes VAE latent + predictive RNN hidden state |
| PlaNet | 2019 | latent online planning | D | RD2 | RSSM latent dynamics + online action-sequence planning |
| Dreamer | 2020 | imagination-trained actor/value | D | RD2 | imagined latent trajectories train actor/value; runtime actor need not optimize fresh rollouts |
| MuZero | 2020 | learned-model tree search | D | RD2 | representation/dynamics/prediction functions + MCTS without observation reconstruction |
| DreamerV2 | 2021 | discrete latent imagination | A | RD1 | discrete RSSM + actor/value learning in imagination |
| EfficientZero | 2021 | sample-efficient MuZero lineage | A | RD1 | search with learned latent model + consistency losses |
| TD-MPC | 2022 | latent MPC | D | RD2 | short-horizon latent trajectory optimization + terminal value |
| DayDreamer | 2022 | physical robot world model | A | RD1 | Dreamer-style world-model policy learning on real robots |
| DreamerV3 | 2023/25 | scalable imagination policy learning | D | RD2 | broad-domain world-model RL, important deployment/training distinction |
| TD-MPC2 | 2024 | scalable latent MPC | D | RD2 | implicit latent world model + trajectory optimization / policy prior |
| EfficientZero V2 | 2024 | search/control | A | RD1 | discrete+continuous learned-model planning |
| Dreamer4 | 2025 | scalable WM agent training | A | RD1 | newer world-model policy-training regime |
| V-JEPA 2 | 2025 | predictive representation + action-conditioned WM | D | RD2 | predictive latent state and embodied planning without pixel-generation requirement |
| JEPA-WM physical-planning studies | 2025/26 | JEPA planning | A | RD1 | stress test for generative-reconstruction assumptions |

## 2. General / embodied world-model theory and surveys

| work | year | tier | depth | role |
|---|---:|---|---|---|
| A Survey on Model-based Reinforcement Learning | 2022/24 | A | RD1 | MBRL taxonomy / planning-model roles |
| Understanding World or Predicting Future? A Comprehensive Survey of World Models | 2024/25 | A | RD1 | broad WM taxonomy |
| Is Sora a World Simulator? | 2024 | C | RD1 | general-WM boundary / generative simulation |
| A Comprehensive Survey on World Models for Embodied AI | 2025 | A | RD1 | embodiment / planning / simulation scope |
| Critiques of World Models | 2025 | A | RD1 | negative/counterexample source |
| A survey of world models for physical AI with uncertainty representation and control | 2026 | D | RD2 | separates state abstraction, dynamics and decision coupling |
| World Model for Robot Learning: A Comprehensive Survey | 2026 | A | RD1 | robot-learning WM map |
| From World Models to World Action Models: A Concise Tutorial for Robotics | 2026 | A | RD1 | world-action coupling map |
| A Tutorial on World Models and Physical AI | 2026 | C | RD1 | recent tutorial / terminology |
| Research on World Models Is Not Merely Injecting World Knowledge into Specific Tasks | 2026 | A | RD1 | conceptual boundary between knowledge injection and world modeling |
| A Mechanistic View on Video Generation as World Models: State and Dynamics | 2026 | D | RD1 | state/dynamics mechanistic pressure test |
| Latent World Models for Automated Driving: A Unified Taxonomy | 2026 | D | RD1 | driving latent-WM taxonomy competitor |

## 3. Generative / simulator autonomous-driving world models

| work | year | tier | depth | role |
|---|---:|---|---|---|
| DriveGAN | 2021 | C | RD1 | controllable neural simulation precursor |
| GAIA-1 | 2023 | A | RD2 | generative driving WM, multimodal tokens/action conditioning |
| UniSim | 2023 | A | RD1 | neural closed-loop sensor simulator |
| DriveDreamer | 2023/24 | A | RD1 | real-world diffusion WM + control |
| Panacea | 2023/24 | C | RD1 | panoramic controllable driving video generation |
| MagicDrive | 2023/24 | C | RD1 | geometry-controlled multiview generation |
| Vista | 2024 | A | RD1 | generalizable controllable driving WM / action evaluator role |
| GenAD | 2024 | A | RD1 | generalized predictive driving model |
| DriveDreamer-2 | 2024/25 | C | RD1 | language-customized scenario generation |
| DriveDreamer4D | 2024 | C | RD1 | 4D data generation |
| DrivingWorld | 2024 | C | RD1 | long driving-video autoregressive world model |
| GAIA-2 | 2025 | A | RD1 | controllable multiview flow-based WM |
| UniDriveDreamer | 2026 | C | RD0 | single-stage multimodal world model |
| RAYNOVA | 2026 | C | RD0 | ray-space autoregressive world modeling |

## 4. Structured / occupancy / geometric driving world models

| work | year | tier | depth | role |
|---|---:|---|---|---|
| OccWorld | 2023/24 | D | RD2 | discrete 3D occupancy world evolution + ego motion |
| Copilot4D | 2023/24 | A | RD1 | unsupervised discrete LiDAR WM |
| MUVO | 2023 | A | RD1 | multimodal generative WM with voxel geometry |
| Drive-OccWorld | 2024/25 | A | RD1 | occupancy WM integrated toward planning/control |
| BEVWorld | 2024 | A | RD1 | scene-level BEV-latent simulator |
| DynamicCity | 2024/25 | C | RD1 | large-scale 4D occupancy generation |
| UniFuture | 2025/26 | A | RD1 | 4D future generation + perception |
| HERMES | 2025 | A | RD1 | unified 3D understanding + generation |
| HERMES++ | 2026 | A | RD0 | extended unified driving WM |
| GraphWorld | 2026 | D | RD3 existing repo | current relational model state for planning |

## 5. Planning-coupled driving world models

| work | year | tier | depth | role |
|---|---:|---|---|---|
| Drive-WM | 2023/24 | D | RD2 | maneuver-conditioned imagined futures used for planning evaluation |
| Think2Drive | 2024 | D | RD2 target | Dreamer-style latent WM used for RL policy improvement |
| DriveWorld | 2024 | A | RD1 existing atlas | world-model pretraining / downstream transfer |
| LAW | 2024/25 | D | RD3 existing repo | action-mediated future-latent supervision, runtime direct policy |
| Epona | 2025 | D | RD3/RD4 existing repo | direct planning plus world-rollout modes |
| DrivingGPT | 2024/25 | D | RD2 target | interleaved multimodal autoregressive world/action modeling |
| WoTE | 2025 | D | RD3 existing repo | candidate-specific future BEV rollout + evaluation |
| World4Drive | 2025 | D | RD3/RD4 existing repo | candidate future endpoint + selector |
| Policy World Model | 2025 | A | RD1 | collaborative state-action prediction / planning |
| FutureSightDrive / FSDrive | 2025 | A | RD1 | visual spatiotemporal chain-of-thought planning |
| DriveLaW | 2026 | D | RD3/RD4 existing repo | planner consumes video-generator internal state |
| Drive-JEPA | 2026 | D | RD3 existing repo | predictive representation transfer + multimodal proposal/scoring |
| WorldDrive | 2026 | D | RD3/RD4 existing repo | representation inheritance + future-latent surrogate rewarder |
| Auto-JEPA | 2026 | D | RD2 existing atlas | future compressed toward planning intent |
| WorldRFT | 2026 | A | RD1 existing atlas | planning-aligned latent + reinforcement fine-tuning |
| ReWorld | 2026 | A | RD1 existing atlas | representation shaping for world-action model |
| WA-JEPA | 2026 | A | RD1 existing atlas | joint future/action latent modeling |
| DA-WAM | 2026 | D | RD3 existing repo | candidate-specific future latent + factorized scorer |
| SafeDrive | 2026 | A | RD3 existing repo | candidate-conditioned sparse future/safety reasoning |
| RiskWorld | 2026 | A | RD3 existing repo | object-centric future rollout → risk monitor |
| SimWAM | 2026 | H | RD0 | reserve as post-freeze world-action holdout |
| WAM-Flow | 2026 | H | RD0 | reserve as post-freeze planning holdout |
| Risk-Aware WM Predictive Control | 2026 | H | RD0 | reserve as MPC-style driving holdout |

## 6. Reactive simulation / policy-training / evaluation

| work | year | tier | depth | role |
|---|---:|---|---|---|
| nuPlan | 2022/23 | A | RD2 existing atlas | planning-evaluation regimes / reactive terminology |
| NAVSIM | 2024 | D | RD2 existing atlas | non-reactive pseudo-simulation dominating current planning scores |
| Bench2Drive | 2024 | A | RD2 target | interactive CARLA E2E benchmark |
| SLEDGE | 2024 | A | RD1 | generative scene model + rule-based traffic |
| DriveArena | 2024/25 | A | RD1 | generative closed-loop simulation |
| HUGSIM | 2025/26 | A | RD1 | reconstructed photorealistic closed-loop simulation |
| ReactSim-Bench | 2026 | D | RD1 | behavioral validity of reactive world agents |
| CausalDrive | 2026 | D | RD1 | ego-conditioned reactive/causal driving WM |
| BridgeSim | 2026 | A | RD1 | open-loop/closed-loop diagnostic bridge |
| CRAFT | 2026 | A | RD1 | counterfactual proxy + interactive correction |

## 7. Strong non-WM / boundary controls

| work | year | tier | depth | purpose |
|---|---:|---|---|---|
| UniAD | 2023 | D | RD2 target | unified E2E without explicit WM control |
| VAD | 2023 | A | RD1 | structured vector E2E control |
| M2I | 2022 | A | RD2 target | conditional interactive prediction predecessor |
| GameFormer | 2023 | D | RD2 target | game-theoretic prediction/planning predecessor |
| BeTop | 2024 | A | RD1 | behavioral topology / contingency planning |
| DiffusionDrive | 2025 | D | RD2 target | multimodal action generation without explicit WM |
| Hydra-MDP | 2025/26 | A | RD1 | candidate bank/scoring/distillation without online WM requirement |
| DriveSuprim | 2026 | D | RD2 target | strong modern candidate-selection control |
| iPad | 2025/26 | A | RD1 | proposal-centric planner control |
| DrivoR | 2026 | A | RD1 | compact representation + candidate planning control |
| ORION | 2026 | A | RD1 | VLA semantic reasoning → planning control |

## 8. Robotics / embodied holdout and expansion candidates

These are intentionally not yet projected into any project ontology.

| work/family | tier | depth | reason |
|---|---|---|---|
| Ctrl-World | H | RD0 | controllable generative robot WM |
| ST-WAM | H | RD0 | explicit world-action manipulation model |
| robot policy evaluation with video WMs | H | RD0 | tests generation-as-evaluator route |
| WorldArena / RoboWM-Bench | C | RD0 | functional-utility evaluation of embodied WMs |
| action-conditioned V-JEPA robotics variants | D | RD1 | predictive latent planning without reconstruction |
| latent robot MPC families | A | RD0 | cross-domain check of W4/search/optimization semantics |

## 9. Registry status

Initial seed contains **100+ named works/families across discovery, anchor, decision-critical and holdout tiers** when combined with the repository's existing Phase-A driving census. This file does not claim 100 full reads.

Immediate next depth goal:

```text
foundational RD2+ set: 12–20
external driving/robotics RD2+ set: 20–30
existing repo RD3/RD4 evidence: reuse with source boundaries intact
true holdout: >=15 kept untouched until candidate codebook freeze
```
