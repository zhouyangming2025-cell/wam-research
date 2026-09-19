# FIELD_ATLAS — Planning-centric WAM

Last updated: 2026-09-14

Status: **HISTORICAL FIELD ATLAS — phase status superseded by current state; retain family map and evidence boundaries.**

This document is not a gap list. It maps the field: major method families, historical transitions, planning interfaces, supervision/evaluation regimes, strong controls and recurring comparison questions.

Detailed census passes:

- `landscape/CENSUS_PHASE_A_ROUND1.md`
- `landscape/CENSUS_PHASE_A_ROUND2.md`

Final Phase-B anchor set:

- `landscape/PHASE_B_ANCHORS.md`

## 1. Field boundary

Primary question:

> How do autonomous-driving world models represent future evolution, couple that future to end-to-end planning, and demonstrate that the coupling improves decisions?

Planning is the center of gravity. Pure perception, VLA, generation and simulation work enters the atlas only when it materially explains planning capability, planner supervision, evaluation, or a historical transition.

## 2. Working field families after Phase A

### F1 — Visual / video generative driving world models

Representative works:

- GAIA-1
- DriveDreamer / DriveDreamer-2
- Drive-WM
- Vista
- Epona
- DrivingGPT
- Policy World Model
- WorldDrive

Core distinction:

```text
generation/data engine
!= controllable imagined future
!= future used as evaluator
!= future representation inherited by planner
!= unified world-action sequence model
```

Visual fidelity and planning usefulness therefore need separate evidence.

### F2 — BEV / occupancy / geometric world models

Representative works:

- OccWorld
- Drive-OccWorld
- WoTE
- World4Drive
- GraphAD as structured-interaction boundary

These methods use future geometry/occupancy/BEV state as a more planning-aligned alternative to RGB. Phase B must separate gains from **predicting the future** from gains due simply to a more structured state representation.

### F3 — Latent / JEPA / predictive-representation world models

Representative works:

- ViDAR
- DriveWorld
- LAW
- DriveLaW
- Drive-JEPA
- WorldRFT
- Auto-JEPA
- ReWorld
- WA-JEPA
- DA-WAM
- Think2Drive as a distinct latent-dynamics RL branch

Role taxonomy is more informative than the generic label “latent WM”:

```text
L1  predictive pretraining only                — ViDAR / DriveWorld
L2  auxiliary future prediction for planning  — LAW-like
L3  future/WM latent consumed at inference     — DriveLaW and related
L4  candidate-specific future latent           — DA-WAM
L5  joint world-action latent/generation        — WA-JEPA / DrivingGPT-like lineage
L6  latent dynamics as policy-training world   — Think2Drive
```

These roles must never be treated as interchangeable.

### F4 — World-model-assisted direct end-to-end planning

Representative works:

- LAW
- Epona
- DriveLaW
- WorldDrive
- Drive-JEPA
- WorldRFT

Central question: **where does future modeling enter the planner?** During pretraining only, as an auxiliary loss, as an inference-time feature, as direct rollout, or as post-training/reward supervision?

### F5 — Candidate-conditioned / action-conditioned future evaluation

Representative works:

- Drive-WM
- Drive-OccWorld
- WoTE
- World4Drive
- SafeDrive
- DA-WAM

Keep separate:

```text
action-conditioned generation
!= candidate-specific latent
!= explicit future-based trajectory evaluator
!= learned candidate score without a future model
!= behaviorally correct intervention response
```

Hydra-MDP / DriveSuprim are especially important **non-WM controls** here because they score many actions effectively without predicting a future world.

### F6 — Unified world-action / trajectory-and-world generation

Representative works / precursors:

- GenAD as trajectory-level ego+agent joint-generation precursor
- OccWorld as structured occupancy+ego joint modeling
- Epona
- DrivingGPT
- DriveLaW
- ReWorld / WA-JEPA lineage

Historical transition:

```text
action as external condition
→ ego and environment futures jointly represented
→ action becomes a co-modeled modality
```

Joint modeling itself is not evidence of correct counterfactual response; that remains an empirical question.

### F7 — Interactive prediction + planning predecessors

Representative works:

- M2I
- GameFormer
- What Truly Matters in Trajectory Prediction
- BeTop
- GraphAD
- Bahram et al. 2016 (metadata/abstract only; lawful open full text unavailable)
- GenAD as later joint-trajectory bridge

Purpose: prevent modern WAM language (“reactive”, “conditional”, “counterfactual”, “interactive”) from obscuring older prediction/planning concepts.

### F8 — Reactive simulation / closed-loop policy learning

Representative works:

- Think2Drive — latent WM as RL training simulator
- SLEDGE
- DriveArena
- HUGSIM
- BridgeSim
- ReactSim-Bench
- CausalDrive
- CRAFT

Keep apart:

```text
WM used to train a policy
rule-based reactive traffic
learned reactive world agents
generative visual simulator
reconstructed photorealistic simulator
counterfactual proxy + interactive correction
```

“Reactive” describes a mechanism/evaluation regime; it does not guarantee behavioral correctness.

### F9 — Reward / value / safety / cost interfaces

Representative works:

- Vista as WM-as-action-evaluator example
- SafeDrive
- Gen-Drive
- DriveReward
- RiskWorld boundary case
- NPPC control
- TOAD / DrivoR context
- WorldDrive rewarder
- Hydra-MDP / DriveSuprim as strong metric-score distillation/scoring controls

Explicit risk/value is one decision interface among several. It is not the default endpoint of world modeling.

### F10 — Strong end-to-end planning without an explicit world model

Representative controls now include:

- UniAD
- VAD
- DiffusionDrive
- DrivoR
- Hydra-MDP
- DriveSuprim
- iPad
- DriveVLM / DriveVLM-Dual
- OmniDrive agent/data branch
- ORION

This family is mandatory for causal interpretation of WAM gains. Strong planning can come from:

```text
better representation
better multimodal action modeling
candidate generation/scoring
metric distillation
proposal-centric feature extraction
language/world-knowledge priors
stronger supervision
```

without an inference-time future world model.

### F11 — Evaluation / benchmark / simulator lineage

The atlas now distinguishes the benchmark history explicitly:

**nuScenes (2020).** Original paper is a multimodal perception/scene-understanding dataset and detection/tracking benchmark. Later E2E literature retrofitted open-loop planning/L2 protocols onto its logs; that planning protocol is not native to the original paper.

**nuPlan (2021+).** Planning-specific dataset/metrics and explicit open-loop, closed-loop non-reactive, and closed-loop reactive protocols. It is a key conceptual transition from prediction-style metrics to planner evaluation.

**NAVSIM (2024).** Real sensor data + short-horizon **non-reactive** pseudo-simulation. Policy is queried once; other-agent behavior does not respond. PDMS adds planning-relevant safety/progress/comfort metrics at scalable cost.

**Bench2Drive (2024).** CARLA-v2 interactive sensor closed loop with standardized expert data and granular multi-ability scenarios.

**HUGSIM (2024/25).** Reconstructed real-scene photorealistic sensor closed loop using 3D Gaussian Splatting plus explicit actor dynamics.

**ReactSim-Bench / related 2026 work.** Moves evaluation toward behavioral validity of learned reactive world agents.

Central rule:

```text
E2  open-loop trajectory matching
E3  NAVSIM non-reactive pseudo-simulation
E4  closed-loop non-reactive data-driven simulation
E5  reactive/reconstructed closed-loop simulation
E6  CARLA / Bench2Drive interactive simulation
E7  standardized real-vehicle closed loop
```

must not be collapsed into a single “closed-loop” category.

## 3. Historical skeleton after Phase-A closeout

This remains a chronology to verify by deep reading, not a causal conclusion:

```text
conditional / game-theoretic interaction prediction
        ↓
planning-oriented unified E2E stacks + planning benchmarks
        ↓
real-world video WMs / occupancy WMs / predictive pretraining
        ↓
future representation explicitly coupled to planning
        ↓
latent planning-oriented prediction / JEPA-style representation shaping
        ↓
multimodal world-action joint modeling + candidate-specific futures
        ↓
WM-based RL/post-training + reactive/counterfactual world simulation
        ↓
stronger evaluation pressure: non-reactive → interactive → photorealistic/reactive worlds
```

Phase B must verify, for every arrow:

1. what concrete limitation motivated the change;
2. whether that limitation was experimentally demonstrated or only argued;
3. what new supervision/data/benchmark enabled the change;
4. whether planning gains came from world prediction, representation, action modeling, evaluator/scoring, RL, or benchmark changes;
5. what older ideas were reintroduced under new terminology.

## 4. Phase-A coverage audit

| family | coverage status | evidence that coverage is sufficient for anchor selection |
|---|---|---|
| F1 visual/video WM | **PASS** | generation-only, controllable, evaluator, planner-inherited and unified world-action variants represented |
| F2 BEV/occupancy/geometric WM | **PASS** | occupancy joint modeling, action-conditioned forecasting, online BEV evaluation and physical-latent variants represented |
| F3 latent/JEPA/predictive | **PASS** | pretraining-only, auxiliary, inference-time, candidate-specific, joint and RL-dynamics roles represented |
| F4 WM-assisted direct planning | **PASS** | multiple interfaces from latent self-supervision to inference features and post-training represented |
| F5 candidate/action-conditioned future | **PASS** | visual, BEV, sparse-world and latent candidates represented, plus non-WM scoring controls |
| F6 unified world-action | **PASS** | trajectory-level precursor, structured occupancy, video/action token and latent joint models represented |
| F7 interaction predecessors | **PASS** | conditional prediction, game-theoretic planning, topology/graph interaction and evaluation critique represented |
| F8 reactive simulation / WM-RL | **PASS** | latent policy-training WM, generative/reconstructed simulators, reactive-agent benchmark and causal-WM branch represented |
| F9 reward/value/safety/cost | **PASS** | explicit safety, reward, learned cost, scorer/search and monitor boundary cases represented |
| F10 strong non-WM controls | **PASS** | unified E2E, diffusion action models, candidate scoring, proposal-centric and VLA planners represented |
| F11 evaluation / benchmarks | **PASS** | nuScenes legacy, nuPlan, NAVSIM, Bench2Drive, HUGSIM and reactive-world benchmark evolution represented |

### Residual coverage weaknesses — tracked, not blockers

1. **Standardized real-vehicle closed-loop evidence remains sparse.** DriveVLM reports production-vehicle deployment, but there is no common E7 benchmark in the current map that supports clean method comparison.
2. **Uncertainty/multimodality consumption remains heterogeneous.** Multiple trajectories/futures are common, but probability calibration, branch selection and whether uncertainty actually changes the final action are not standardized. This requires comparative deep reading, not more breadth accumulation.
3. **Behavioral realism of reactive agents is not solved by simulator realism.** HUGSIM improves visual realism; ReactSim-Bench/CausalDrive address behavior from another direction. Their relationship must be analyzed in Phase B.

`Hydra-MDP++` and `NAVSIM-v2` are optional follow-ups. They are not required to explain the current field skeleton and therefore do not block Phase A.

## 5. Cross-family claims reserved for Phase B/C

The following remain **questions**, not conclusions:

```text
Higher world fidelity improves planning.
A future model adds value beyond better representation learning.
Action conditioning improves planning because it models consequences.
Joint world-action modeling outperforms simply sharing a backbone.
Latent predictive states are more decision-efficient than visual reconstruction.
Explicit interaction modeling improves reactive behavior.
Candidate-specific futures help because of counterfactual modeling rather than stronger scoring supervision.
Long-horizon prediction matters for action quality.
Explicit value/risk interfaces improve safety beyond implicit action modeling.
Closed-loop simulation changes model ranking relative to open-loop/non-reactive metrics.
```

Each claim will later be assigned `SUPPORTED / MIXED / WEAK / COUNTEREXAMPLE / INSUFFICIENT` only after matched anchor evidence.

## 6. Phase-A closeout

```text
Corpus breadth: 60 registered records, 58 RAW_MD_READY
Scientific census: sufficient cross-family coverage
F1–F11 audit: PASS
Broad paper acquisition: FROZEN
Gap/novelty search: CLOSED
Method design: CLOSED
Phase B anchor deep reads: AUTHORIZED
```

Final anchor set and redundancy rationale:

`landscape/PHASE_B_ANCHORS.md`

## 7. Phase-B entry point

Start with **Wave 1**:

```text
M2I
GameFormer
What Truly Matters in Trajectory Prediction?
UniAD
nuPlan
NAVSIM
DiffusionDrive
DriveSuprim
```

The first synthesis should establish the pre-WAM planning/evaluation baseline before interpreting any modern WM gain.