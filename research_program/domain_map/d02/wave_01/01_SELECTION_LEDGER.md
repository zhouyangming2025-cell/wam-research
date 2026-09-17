# D02-W1 Selection Ledger

Status: **sealed before selected-paper method inspection**

## 1. Selection boundary

The local corpus contained 65 paper directories at the base commit. The hard-exclusion set removes the 12-paper core, the 21 canonical artifacts, the D01 26-paper domain census, the D01.3 blind set, and duplicate/version entries already used in ontology design, regression, or blind testing. The remaining local pool contains 26 candidates.

Selection used only:

- paper identifier and exact local title;
- abstract when present;
- year/venue/source metadata available in the local corpus;
- official-code availability metadata;
- the declared research task and obvious scope relation.

No selected-paper method section, formula, mechanism diagram, code path, or existing R–W–E/C–X–D–P–V–T–L projection was used to select the 20 papers.

### Selection-barrier audit

Two local candidates were opened during task setup before this ledger was written: `P0023_iPad` (method text) and `P0066_SafeSim` (verified source note). They are therefore **permanently deferred from Wave 1**, even though both are plausible candidates. This conservative exclusion preserves the preregistration barrier.

## 2. Eligible pool after hard exclusions

| paper ID | exact local title | local source | preliminary reason for eligibility | Wave 1 decision |
|---|---|---|---|---|
| P0004 | Reasoning Multi-Agent Behavioral Topology for Interactive Autonomous Driving | raw MD; official code URL in abstract | interactive prediction/planning topology | SELECT |
| P0010 | Test-Time Trajectory Optimization for Autonomous Driving | raw MD | test-time proposal/optimization boundary | SELECT |
| P0011 | Sensitivity Shaping for Latent Modeling | raw MD; abstract unavailable locally | latent/world representation boundary; evidence probe | SELECT |
| P0013 | BridgeSim: Unveiling the OL-CL Gap in End-to-End Autonomous Driving | raw MD | simulator and deployment/evaluation boundary | SELECT |
| P0014 | ReactSim-Bench: Benchmarking Reactive Behavior World Model Simulation in Autonomous Driving | raw MD | reactive world-model simulation boundary | SELECT |
| P0016 | How Can Driving World Models Do Counterfactual Prediction? | raw MD | counterfactual world-model semantics | SELECT |
| P0017 | CRAFT: Counterfactual-to-Interactive Reinforcement Fine-Tuning for Driving Policies | raw MD | counterfactual training environment and policy learning | SELECT |
| P0019 | M2I: From Factored Marginal Trajectory Prediction to Interactive Prediction | raw MD | interactive multi-agent prediction boundary | SELECT |
| P0021 | Hydra-MDP: End-to-end Multimodal Planning with Multi-target Hydra-Distillation | raw MD; official code URL in abstract | candidate planning and teacher/scorer use | SELECT |
| P0023 | iPad: Iterative Proposal-centric End-to-End Autonomous Driving | raw MD; method inspected before ledger | candidate-centric planning; barrier violation | DEFER—pre-opened |
| P0024 | DRIVEVLM: The Convergence of Autonomous Driving and Large Vision-Language Models | raw MD | semantic reasoning to action boundary | SELECT |
| P0025 | OmniDrive: A Holistic Vision-Language Dataset for Autonomous Driving with Counterfactual Reasoning | raw MD | counterfactual reasoning and planning supervision | SELECT |
| P0026 | ORION: A Holistic End-to-End Autonomous Driving Framework by Vision-Language Instructed Action Generation | raw MD | semantic hierarchy/action generation | SELECT |
| P0029 | GenAD: Generative End-to-End Autonomous Driving | raw MD; official code URL in abstract | generative future/action modelling | SELECT |
| P0030 | nuScenes: A multimodal dataset for autonomous driving | raw MD | dataset rather than mechanism artifact | DEFER—benchmark/data |
| P0031 | nuPlan: A closed-loop ML-based planning benchmark for autonomous vehicles | raw MD | closed-loop benchmark rather than a model | DEFER—benchmark/data |
| P0032 | NAVSIM: Data-Driven Non-Reactive Autonomous Vehicle Simulation and Benchmarking | raw MD | evaluation simulator/benchmark | DEFER—benchmark/data |
| P0033 | Bench2Drive: Towards Multi-Ability Benchmarking of Closed-Loop End-to-End Autonomous Driving | raw MD | benchmark rather than a model mechanism | DEFER—benchmark/data |
| P0034 | HUGSIM: A Real-Time, Photo-Realistic and Closed-Loop Simulator for Autonomous Driving | raw MD; abstract unavailable locally | generative simulator boundary | SELECT |
| P0038 | Vista: A Generalizable Driving World Model with High Fidelity and Versatile Controllability | raw MD | controllable world generation and action evaluation | SELECT |
| P0039 | DriveDreamer-2: LLM-Enhanced World Models for Diverse Driving Video Generation | raw MD | generation-only world model boundary | SELECT |
| P0054 | What Truly Matters in Trajectory Prediction for Autonomous Driving? | raw MD | dynamics gap and interactive evaluation boundary | SELECT |
| P0055 | SLEDGE: Synthesizing Driving Environments with Generative Models and Rule-Based Trafic | raw MD; abstract unavailable locally | synthetic environment/world generation boundary | SELECT |
| P0057 | Planning-oriented Autonomous Driving | raw MD; official code status in abstract | strong end-to-end planning control case | SELECT |
| P0058 | VAD: Vectorized Scene Representation for Efficient Autonomous Driving | raw MD; official code URL in abstract | vectorized scene/planning boundary control | SELECT |
| P0066 | SAFE-SIM: Safety-Critical Closed-Loop Traffic Simulation with Diffusion-Controllable Adversaries | verified source note; source inspected before ledger | reactive simulation; barrier violation | DEFER—pre-opened |

## 3. Final selected 20

```text
P0004  BeTop
P0010  TOAD
P0011  Sensitivity Shaping
P0013  BridgeSim
P0014  ReactSim-Bench
P0016  Counterfactual Prediction
P0017  CRAFT
P0019  M2I
P0021  Hydra-MDP
P0024  DRIVEVLM
P0025  OmniDrive
P0026  ORION
P0029  GenAD
P0034  HUGSIM
P0038  Vista
P0039  DriveDreamer-2
P0054  What Truly Matters
P0055  SLEDGE
P0057  UniAD
P0058  VAD
```

The selection is intentionally not a claim that all 20 are in-domain. It is a breadth probe. Scope verdicts are assigned only after the shallow source pass.

## 4. Selection rationale

The set covers the required conceptual faces without using fixed mechanism quotas:

| coverage face | selected representatives |
|---|---|
| online future/interaction or world participation | BeTop, GenAD, Vista |
| training-only or representation/learning boundary | Sensitivity Shaping, CRAFT, UniAD, VAD |
| candidate/proposal/optimization boundary | TOAD, Hydra-MDP, VAD |
| counterfactual and interactive semantics | Counterfactual Prediction, CRAFT, M2I, OmniDrive |
| simulation and evaluation boundary | BridgeSim, ReactSim-Bench, HUGSIM, What Truly Matters, SLEDGE |
| semantic/action generation | DRIVEVLM, ORION |
| generation-only world model | DriveDreamer-2, Vista, SLEDGE |

These labels describe selection intent only. They are not mechanism classifications and must not be copied as final route labels without evidence.

## 5. Deferred pool

The four dataset/benchmark entries are held for a later boundary corpus because they do not themselves present a deployed mechanism artifact. The two pre-opened candidates are held to protect the blindness barrier. None is silently counted as an exclusion from the domain; their reasons are preserved for later waves.

