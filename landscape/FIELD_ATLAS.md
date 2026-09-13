# FIELD_ATLAS — Planning-centric WAM

Last updated: 2026-09-14

Status: **UNDER CONSTRUCTION — FIELD RECONSTRUCTION PHASE**

This document is not a gap list. It is a map of the field: major families, historical transitions, planning interfaces, evidence regimes, recurring trade-offs, and representative anchors.

Detailed first census pass:

`landscape/CENSUS_PHASE_A_ROUND1.md`

## 1. Field boundary

Primary question:

> How do autonomous-driving world models represent future evolution, couple that future to end-to-end planning, and demonstrate that the coupling improves decisions?

The atlas is planning-centric. Pure perception or generation work is included only when it materially shapes later planning-oriented world models.

## 2. Current working families

### F1 — Visual / video generative driving world models

Core idea: predict or generate future visual observations/world evolution.

Representative anchors now placed:
- GAIA-1
- DriveDreamer / DriveDreamer-2
- Drive-WM
- Vista
- Epona
- DrivingGPT
- Policy World Model
- WorldDrive

Key distinction discovered in census Round 1:

```text
generation/data engine
≠ controllable imagined future
≠ future used as evaluator
≠ future representation inherited by planner
≠ unified world-action sequence model
```

The visual-WM family therefore cannot be treated as a single planning paradigm.

### F2 — BEV / occupancy / geometric world models

Core idea: forecast future scene geometry, occupancy, flow, or BEV state, often closer to planning constraints than RGB.

Representative anchors:
- OccWorld
- Drive-OccWorld
- WoTE
- World4Drive (hybrid latent/physical)
- GraphAD as a structured interaction boundary case

Central field question: which benefits come from predicting a future, and which come from choosing a more planning-friendly state representation?

### F3 — Latent / JEPA / predictive-representation world models

Core idea: predict future latent states rather than reconstruct pixels.

Representative anchors:
- DriveWorld
- LAW
- DriveLaW
- Drive-JEPA
- WorldRFT
- Auto-JEPA
- ReWorld
- WA-JEPA
- DA-WAM

Round-1 refinement: split this family by **role**, not only representation:

```text
L1  world-model pretraining only
L2  auxiliary future-prediction supervision during planner training
L3  future latent retained and consumed at inference
L4  candidate-specific future latent for selection
L5  joint world-action latent generation
```

This role distinction is likely more informative for planning than simply saying "latent world model".

### F4 — World-model-assisted direct end-to-end planning

Core idea: future modeling improves direct trajectory decoding or planning representation.

Representative anchors:
- LAW
- Epona
- DriveLaW
- WorldDrive
- Drive-JEPA
- WorldRFT

Key census question: is the world model **still present at inference**, or did it only shape the representation during training?

### F5 — Candidate-conditioned / action-conditioned future evaluation

Core idea: imagine a different future for different ego actions/candidates, then score/select.

Representative anchors:
- Drive-WM
- Drive-OccWorld
- WoTE
- World4Drive
- SafeDrive
- DA-WAM

Important distinction:

```text
action-conditioned generation
≠ candidate-specific learned latent
≠ explicit future-based evaluator
≠ behaviorally correct counterfactual reaction
```

The atlas records these separately.

### F6 — Unified world-action / trajectory-and-world generation

Core idea: actions/trajectories and world evolution are generated jointly or in tightly shared latent dynamics.

Representative anchors:
- OccWorld (joint occupancy + ego movement, early structured form)
- Epona
- DrivingGPT
- DriveLaW
- ReWorld lineage
- WA-JEPA

This appears to be an important 2025–2026 transition: the action is no longer merely an external conditioning variable; it increasingly becomes a co-modeled modality.

### F7 — Interactive prediction + planning predecessors

Core idea: prediction and planning are coupled around agent interaction, contingency, conditional response, or game structure, often predating current WAM terminology.

Representative anchors:
- M2I
- GameFormer
- What Truly Matters in Trajectory Prediction
- BeTop
- GraphAD
- Bahram et al. replanning-aware game-theoretic planning (to ingest/verify)

Field-reconstruction role: identify which ideas now described as "reactive", "conditional", "counterfactual", or "interactive world modeling" have older prediction/planning roots.

### F8 — Reactive world simulation / closed-loop policy training

Core idea: learned/rule world agents or simulators respond to ego deviations and support closed-loop evaluation/training.

Representative anchors:
- SLEDGE
- DriveArena
- HUGSIM
- BridgeSim
- ReactSim-Bench
- CausalDrive
- CRAFT

Keep apart:

```text
rule-based reactive traffic
learned reactive traffic agents
generative visual simulator
reconstructed photorealistic simulator
counterfactual proxy training
policy-learning environment
```

### F9 — Reward / value / safety / cost interfaces

Core idea: future/prediction features are compressed into decision scores, reward, cost, safety, or preference signals.

Representative anchors:
- Vista (WM-as-action evaluator)
- SafeDrive
- Gen-Drive
- DriveReward
- RiskWorld (monitor boundary case)
- NPPC (learned planning cost control)
- TOAD / DrivoR context
- WorldDrive future-aware rewarder

Important atlas principle: explicit value/risk is one planning interface among several, not the default destination of a world model.

### F10 — Strong end-to-end planning baselines without explicit WM

Purpose: prevent attributing every planning gain to world modeling.

Placed controls:
- UniAD
- VAD
- DiffusionDrive
- DrivoR

Round 2 must add Hydra-MDP family, DriveSuprim, iPad and representative VLA planners after primary-source verification.

### F11 — Evaluation / benchmark / simulator papers

Core benchmark lineage currently placed:
- nuScenes open-loop planning legacy
- nuPlan closed-loop planning benchmark
- NAVSIM / NAVSIM-v2 non-reactive pseudo-simulation
- Bench2Drive CARLA closed-loop interactive evaluation
- HUGSIM photorealistic closed-loop simulation
- What Truly Matters as predictor→planner evaluation critique
- ReactSim-Bench as reactive-world-agent benchmark

Central atlas rule:

```text
E2 open-loop trajectory matching
E3 NAVSIM-style non-reactive pseudo-simulation
E4/5 closed-loop non-reactive/reactive simulation
E6 CARLA-style interactive simulation
E7 real-vehicle closed loop
```

must never be collapsed into a single "closed-loop" label.

## 3. Provisional historical evolution after Census Round 1

This is a chronology to verify by deep reading, not a gap claim:

```text
interaction-aware prediction / game-theoretic planning
        ↓
planning-oriented E2E stacks + planning benchmarks
        ↓
real-world generative video WMs / occupancy WMs / WM pretraining
        ↓
future state explicitly consumed by planning
        ↓
latent / self-supervised planning representations
        ↓
multimodal world-action joint modeling
        ↓
candidate-specific futures + planning-oriented representation shaping
        ↓
reactive / counterfactual WMs + RL/post-training + stronger closed-loop evaluation
```

Questions for Phase B anchor reads:

1. What concrete limitation motivated each transition?
2. Was that limitation shown experimentally or asserted conceptually?
3. Which new supervision/data/benchmark enabled the transition?
4. Did planning improve because of future modeling, stronger representation, stronger action supervision, stronger evaluator, or benchmark change?
5. Which pieces of older prediction/planning theory were reintroduced under new WAM language?

## 4. Cross-family trade-off matrix — evidence collection started

Do **not** fill this from intuition. Phase B will populate it with matched evidence.

| family | future fidelity | planning directness | action specificity | interaction/reactivity | uncertainty | interpretability | efficiency | closed-loop evidence |
|---|---|---|---|---|---|---|---|---|
| visual/video | EVIDENCE PENDING | mixed | mixed/high in controllable models | mixed | often generative | low-medium | often costly | mixed |
| occupancy/BEV | EVIDENCE PENDING | high | mixed/high | mixed | varies | medium-high | medium | mixed |
| latent/JEPA | EVIDENCE PENDING | medium-high | mixed/high | mixed | increasingly generative | low | often favorable | mixed |
| candidate-conditioned | EVIDENCE PENDING | high | high | not guaranteed | varies | medium | candidate-count dependent | mixed |
| reactive simulator | EVIDENCE PENDING | evaluator/training dependent | high | high by design | varies | medium | varies | high by construction |

Cells marked qualitatively above are only taxonomy-level tendencies; they are not final comparative claims.

## 5. Evidence map — claims to test, not assumptions

```text
Higher world fidelity improves planning.
Action conditioning improves planning because it models consequences.
Explicit interaction modeling improves reactive behavior.
Closed-loop simulation is necessary for meaningful planning evaluation.
Latent prediction is more decision-efficient than visual reconstruction.
Explicit value/risk interfaces improve safety.
Long-horizon prediction is important for planning.
World-model pretraining provides gains beyond stronger planner supervision.
Joint world-action modeling provides gains beyond shared backbone capacity.
Candidate-specific futures improve decisions because of better counterfactual modeling rather than stronger scoring supervision.
```

Each claim will eventually receive:

```text
SUPPORTED
MIXED / CONTEXT-DEPENDENT
WEAKLY SUPPORTED
COUNTEREXAMPLE EXISTS
INSUFFICIENT EVIDENCE
```

No claim is adjudicated during Phase A census.

## 6. Census progress

Phase-A Round 1 now places roughly **45 unique works/benchmarks/control systems** across the field. See:

`landscape/CENSUS_PHASE_A_ROUND1.md`

The current Batch 0A corpus remains useful but hypothesis-biased; it is being re-used as anchor evidence inside this broader map.

## 7. Provisional Phase-B anchor pool

Current pool is approximately 25 works, intentionally spanning conflicting design philosophies:

- M2I
- GameFormer
- What Truly Matters
- UniAD
- NAVSIM
- GAIA-1
- Drive-WM
- Vista
- Epona
- DrivingGPT
- OccWorld
- Drive-OccWorld
- WoTE
- World4Drive
- LAW
- DriveLaW
- Drive-JEPA
- WorldRFT
- Auto-JEPA
- ReWorld / WA-JEPA
- DA-WAM
- WorldDrive
- Bench2Drive
- HUGSIM
- ReactSim-Bench / CausalDrive

This pool will be reduced only after Round 2 fills known census gaps.

## 8. Next atlas work

Round 2 should **not** search for gaps. It should fill missing field coverage:

1. Verify and add Hydra-MDP, DriveSuprim, iPad and representative VLA planning controls.
2. Add Think2Drive / world-model RL lineage.
3. Add ViDAR / GenAD and other representation-pretraining WMs only if they materially explain the transition into planning-centric WMs.
4. Map nuScenes → nuPlan → NAVSIM → NAVSIM-v2 → Bench2Drive/HUGSIM benchmark evolution.
5. Add inference/deployment properties: future branch retained vs discarded, latency, candidate count, rollout horizon.
6. Identify any credible real-vehicle closed-loop evidence.
7. Reach 50–80 census works, then freeze Phase A and begin representative anchor deep reads.
