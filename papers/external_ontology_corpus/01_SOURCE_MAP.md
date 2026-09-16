# External Source Map

Status: discovery map, not ontology authority.

## 1. High-value survey / index sources

These are used to expand coverage and identify historical lineages. Their taxonomies are treated as competing hypotheses.

### General world models / Physical AI

- **Awesome World Models** — maintained cross-domain index; 340+ papers as of 2026-07-13. Covers foundations, autonomous driving, robotics, interactive/gaming world models, 3D/4D, physics, memory and evaluation.
- **Understanding World or Predicting Future? A Comprehensive Survey of World Models** — broad taxonomy and historical synthesis.
- **A Survey on Model-based Reinforcement Learning** — foundational MBRL taxonomy and planning/model-learning context.
- **A survey of world models for physical AI with uncertainty representation and control** — useful because it explicitly separates state abstraction, temporal dynamics and decision coupling.
- **World Model for Robot Learning: A Comprehensive Survey** — robotics-oriented evidence for policy/world coupling outside driving.
- **From World Models to World Action Models: A Concise Tutorial for Robotics** — world-action boundary and policy coupling.
- **A Tutorial on World Models and Physical AI** — broad recent tutorial.

### Autonomous driving

- **The Role of World Models in Shaping Autonomous Driving: A Comprehensive Survey** — maintained AD-specific paper list and survey.
- **A Survey of World Models for Autonomous Driving** — 2025 survey.
- **World Models for Autonomous Driving: An Initial Survey** — early 2024 snapshot.
- **Exploring the Interplay Between Video Generation and World Models in Autonomous Driving** — video-generation / WM boundary.
- **Latent World Models for Automated Driving: A Unified Taxonomy** — recent latent-WM taxonomy; especially relevant to representation-vs-planning interfaces.
- Existing repository atlas: `landscape/FIELD_ATLAS.md` and census documents.

## 2. Foundational mechanism strata and canonical seeds

### A. Predictive / belief state foundations

- Predictive State Representations for Dynamical Systems
- POMDP / belief-state literature as background for `state sufficient for decision` versus generic features
- recurrent state-space models as a bridge to learned latent dynamics

### B. Dyna / model-assisted learning

- Dyna: integrated architecture for learning, planning and reacting
- successors where a learned model produces simulated experience but execution can remain reactive

Why required: falsifies any ontology that equates `uses a world model somewhere` with `uses a world model online at decision time`.

### C. Learned latent dynamics + online planning

- **World Models** (Ha & Schmidhuber, 2018)
- **PlaNet** (Hafner et al., 2019)
- **TD-MPC / TD-MPC2**

Why required: expose current latent state, predictive hidden state, explicit rollout and trajectory optimization as distinct uses of learned dynamics.

### D. Imagination-trained policies

- **Dreamer / DreamerV2 / DreamerV3 / Dreamer4**

Why required: world trajectories can be central to policy/value learning while not being re-planned at every deployed action.

### E. Search with learned models

- **Value Prediction Network**
- **TreeQN / ATreeC**
- **MuZero / EfficientZero / EfficientZero V2**

Why required: world/model states can be abstract and reward/value sufficient rather than observation-reconstructive; runtime topology can be a search tree rather than a single future sequence.

### F. JEPA / predictive representations

- I-JEPA / V-JEPA / V-JEPA 2
- action-conditioned V-JEPA variants / physical planning with JEPAs

Why required: tests whether `future/world state` requires generative reconstruction and where predictive representations become decision-coupled.

## 3. Autonomous-driving mechanism strata

### Generation / simulation lineage

- DriveGAN
- GAIA-1 / GAIA-2
- DriveDreamer / DriveDreamer-2 / DriveDreamer4D
- Vista
- GenAD
- UniSim
- DrivingWorld
- UniDriveDreamer

### Structured world-state lineage

- OccWorld
- Drive-OccWorld
- MUVO
- BEVWorld
- DynamicCity
- UniFuture
- HERMES / HERMES++

### Planning-coupled world models

- Drive-WM
- LAW
- Epona
- DrivingGPT
- World4Drive
- WoTE
- WorldDrive
- DriveLaW
- Drive-JEPA
- Auto-JEPA
- WorldRFT
- ReWorld
- WA-JEPA
- DA-WAM
- Policy World Model
- SafeDrive
- RiskWorld
- Think2Drive
- SimWAM
- WAM-Flow
- FutureSightDrive / FSDrive
- recent risk-aware WM-MPC methods

### Reactive / simulator / policy-training lineages

- SLEDGE
- DriveArena
- HUGSIM
- ReactSim-Bench
- CausalDrive
- CRAFT
- BridgeSim

### Strong controls without explicit online WM

- UniAD
- VAD
- DiffusionDrive
- Hydra-MDP
- DriveSuprim
- iPad
- DrivoR
- ORION / VLA planning controls

## 4. Robotics / embodied evidence strata

Required because a driving-only ontology can overfit driving implementation conventions.

Priority families:

- action-conditioned video world models for manipulation;
- latent dynamics for robot planning;
- model-predictive control with learned dynamics;
- world-model policy evaluation;
- joint world-action models;
- robot policies trained in imagined/generated worlds;
- language/world-action models where semantic plans mediate low-level action.

Representative discovery seeds include Ctrl-World, ST-WAM, robot-world-model surveys, WorldArena / RoboWM-Bench and V-JEPA 2 action-conditioned models.

## 5. What not to infer from source maps

The following are discovery hints only:

```text
paper is in a WM survey
paper calls itself a world model
paper predicts video
paper uses latent tokens
paper uses BEV / occupancy
paper has a reward head
paper is joint world-action
```

None of these facts by themselves determine the mechanism class.

## 6. Immediate evidence gaps to fill

1. predictive-state / belief-state theory is underrepresented in the current driving repo;
2. online tree search and MPC with learned models are underrepresented in the current R examples;
3. robotics world-action systems are underrepresented;
4. world models that predict reward/value but not observations need dedicated mechanism cards;
5. methods with model-generated training data but model-free runtime need explicit comparison against LAW/Drive-JEPA/DynFlowDrive-like routes;
6. joint generation must be separated from temporal depth of the world representation;
7. uncertainty / stochastic branching may deserve an independent audit dimension if it changes decision causality rather than merely distributional implementation.
