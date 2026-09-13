# FIELD_ATLAS — Planning-centric WAM

Last updated: 2026-09-14

Status: **UNDER CONSTRUCTION — FIELD RECONSTRUCTION PHASE**

This document is not a gap list. It is a map of the field: major families, historical transitions, planning interfaces, evidence regimes, recurring trade-offs, and representative anchors.

## 1. Field boundary

Primary question:

> How do autonomous-driving world models represent future evolution, couple that future to end-to-end planning, and demonstrate that the coupling improves decisions?

The atlas is planning-centric. Pure perception or generation work is included only when it materially shapes later planning-oriented world models.

## 2. Provisional field families

### F1 — Visual / video generative driving world models

Core idea: predict or generate future visual observations/world evolution.

Questions to map:
- Is the model controllable by ego action/trajectory?
- Is visual generation used by the planner or only for simulation/data generation?
- Does high visual fidelity correlate with planning utility?

Current known anchors to place/reverify:
- DrivingWorld / Driving-World family
- Vista
- GAIA-1
- Drive-WM
- Epona

### F2 — BEV / occupancy / geometric world models

Core idea: forecast future scene geometry, occupancy, flow, or BEV state, often closer to planning constraints than RGB.

Questions:
- Is future geometry predicted under ego action?
- Is planning performed via learned head, explicit cost, or candidate selection?
- How much safety gain comes from occupancy/cost post-processing rather than learned interaction?

Known anchors:
- OccWorld / Drive-OccWorld
- WoTE
- World4Drive
- related occupancy/BEV world-model planners

### F3 — Latent / JEPA / predictive-representation world models

Core idea: predict future latent states rather than reconstruct pixels.

Questions:
- What information is preserved or discarded?
- Is the future branch retained at inference?
- Is latent prediction directly coupled to action selection or only used as pretraining?

Known anchors:
- LAW
- DriveLaW
- Auto-JEPA
- Drive-JEPA
- ReWorld / WA-JEPA / related 2026 representation work
- DA-WAM

### F4 — World-model-assisted direct end-to-end planning

Core idea: future modeling improves direct trajectory decoding or planning representation.

Questions:
- Is the planner truly using future information at inference?
- Does matched ablation isolate world-model contribution?
- How does it compare with equally strong non-WM planners?

Known anchors:
- Epona
- DriveLaW
- LAW
- WorldDrive

### F5 — Candidate-conditioned / action-conditioned future evaluation

Core idea: imagine a different future for different ego actions/candidates, then score/select.

Questions:
- Which candidate futures have direct supervision?
- Is candidate-specific future prediction causally meaningful or merely distinct latent conditioning?
- Is the ranking tested under interactive/reactive evaluation?

Known anchors:
- SafeDrive
- DA-WAM
- Drive-WM / Drive-OccWorld style controllable rollout where applicable

### F6 — Unified world-action / trajectory-and-world generation

Core idea: actions/trajectories and world evolution are generated in a unified model or shared latent dynamics.

Questions:
- Is action a predicted modality, a conditioning signal, or both?
- Does joint generation materially improve planning?
- What is the direction of information flow between world and action branches?

Known anchors:
- Epona
- DrivingGPT / related world-action token models
- newer WAM / unified policy-world models to identify

### F7 — Interactive prediction + planning predecessors

Core idea: prediction and planning are coupled around agent interaction, contingency, conditional response, or game structure, often predating current WAM terminology.

Questions:
- Which concepts now called “reactive/counterfactual world modeling” already existed here?
- What was difficult before modern generative models?
- Which old assumptions remain relevant?

Known anchors:
- GameFormer
- M2I
- BeTop
- Bahram et al. replanning-aware game-theoretic planning
- GraphAD as a later end-to-end interaction representation

### F8 — Reactive world simulation / closed-loop policy training

Core idea: learned world agents or world models respond to ego deviations and support realistic closed-loop evaluation/training.

Questions:
- Does reaction depend on ego intervention?
- Are reactions behaviorally correct, not merely plausible?
- Is the world model used to train the policy, evaluate it, or both?

Known anchors:
- BridgeSim
- ReactSim-Bench
- CausalDrive
- CRAFT
- other learned reactive simulation systems to identify

### F9 — Reward / value / safety / cost interfaces

Core idea: world/prediction features are compressed into decision scores, reward, cost, safety, or preference signals.

Questions:
- Is the interface explicit or implicit?
- How is it supervised?
- Does optimization exploit it?
- Is explicit risk/value actually necessary?

Known anchors:
- Gen-Drive
- DriveReward
- NPPC
- SafeDrive
- RiskWorld as a monitoring boundary case
- TOAD / DrivoR as planning-scoring robustness context

### F10 — Strong end-to-end planning baselines without explicit WM

Purpose: prevent attributing every planning gain to world modeling when strong E2E planners may achieve similar or better results through representation, imitation, candidate generation, or scoring.

Need representative anchors across:
- direct trajectory imitation;
- diffusion trajectory planning;
- candidate-based scoring;
- VLA planning.

The field map is incomplete until WM methods are compared against these baselines conceptually and under comparable evaluation.

### F11 — Evaluation / benchmark / simulator papers

Core idea: benchmarks define what “planning improvement” means.

Need to map:
- nuScenes open-loop trajectory metrics;
- nuPlan OL / CL-NR / CL-R;
- NAVSIM / NAVSIM-v2;
- Bench2Drive / CARLA;
- reactive world-model simulation benchmarks;
- counterfactual evaluation datasets;
- real-world/vehicle evidence where available.

## 3. Historical evolution — to be reconstructed

Provisional questions, not conclusions:

```text
scene prediction
→ structured future prediction
→ integrated prediction + planning
→ visual/generative driving world models
→ latent/occupancy planning-oriented world models
→ action-conditioned/candidate-specific futures
→ unified world/action models
→ reactive/counterfactual world models
```

For each transition, determine:

1. What limitation of the previous paradigm motivated the shift?
2. Which new supervision/data made the new paradigm possible?
3. Which planning capability actually improved?
4. Which old problem remained unresolved?

## 4. Cross-family trade-off matrix — placeholders

To be filled with evidence rather than intuition:

| family | future fidelity | planning directness | action specificity | interaction/reactivity | uncertainty | interpretability | efficiency | closed-loop evidence |
|---|---|---|---|---|---|---|---|---|
| visual/video | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| occupancy/BEV | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| latent/JEPA | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| candidate-conditioned | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| reactive simulator | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |

## 5. Evidence map — placeholders

For each major claim, record both supporting and contradicting papers.

Examples of claims to test rather than assume:

```text
Higher world fidelity improves planning.
Action conditioning improves planning because it models consequences.
Explicit interaction modeling improves reactive behavior.
Closed-loop simulation is necessary for meaningful planning evaluation.
Latent prediction is more decision-efficient than visual reconstruction.
Explicit value/risk interfaces improve safety.
Long-horizon prediction is important for planning.
World-model pretraining provides gains beyond stronger planner supervision.
```

Each claim should end in one of:

```text
SUPPORTED
MIXED / CONTEXT-DEPENDENT
WEAKLY SUPPORTED
COUNTEREXAMPLE EXISTS
INSUFFICIENT EVIDENCE
```

## 6. Current corpus placement

Existing Batch 0A papers are valuable but biased toward hypotheses we were testing. They are **not** a representative field sample.

Current papers should now be re-used as anchors inside the broader atlas rather than treated as the field itself.

## 7. Next atlas work

1. Read recent high-quality DWM surveys and planning-oriented E2E surveys to seed a census list.
2. Build a 50–80 paper census across F1–F11.
3. Mark 15–25 representative anchors for deep reading.
4. Reclassify current Batch 0A papers into the common taxonomy.
5. Only after the atlas stabilizes, reopen problem discovery.
