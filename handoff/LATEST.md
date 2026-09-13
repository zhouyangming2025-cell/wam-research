# LATEST — Handoff

Session: 2026-09-14 — Phase-A field census Round 1 completed.

## New-session fast path

```text
1. START_HERE.md
2. state/CURRENT_STATE.md
3. state/NEXT_TASK.md
4. landscape/FIELD_ATLAS.md
5. landscape/CENSUS_PHASE_A_ROUND1.md
6. state/RESEARCH_PRINCIPLES.md
```

Read `landscape/FIELD_RECONSTRUCTION_PLAN.md` when methodology detail is needed.

Do not default to P2-R. Do not reload the whole corpus or old chats by default.

## Research identity

```text
World Model + End-to-End + Planning-centric autonomous driving
```

Planning is the center of gravity. Risk-field / predictive-risk expertise is optional prior knowledge, not a required destination.

## Active methodology

```text
FIELD UNDERSTANDING FIRST
→ census the field
→ select representative anchors
→ deep-read anchors
→ synthesize historical transitions / interfaces / supervision / evaluation / trade-offs
→ only then reopen research-problem discovery
```

P1/P2-R/P3 are parked provenance probes, not active search targets.

## Phase-A Round 1 completed

New census file:

`landscape/CENSUS_PHASE_A_ROUND1.md`

Round 1 provisionally places roughly **45 unique works / benchmarks / control systems** across F1–F11.

Coverage now includes:

- visual/video generative WMs: GAIA-1, DriveDreamer, Drive-WM, Vista, Epona, DrivingGPT, Policy World Model, WorldDrive;
- occupancy/BEV/geometric WMs: OccWorld, Drive-OccWorld, WoTE, World4Drive;
- latent/JEPA/WAM representations: DriveWorld, LAW, DriveLaW, Drive-JEPA, WorldRFT, Auto-JEPA, ReWorld, WA-JEPA, DA-WAM;
- interactive prediction/planning: M2I, GameFormer, What Truly Matters, BeTop, GraphAD;
- reactive/evaluation environments: nuPlan, SLEDGE, NAVSIM, Bench2Drive, HUGSIM, DriveArena, BridgeSim, ReactSim-Bench, CausalDrive, CRAFT;
- reward/value/safety interfaces: SafeDrive, Gen-Drive, DriveReward, RiskWorld, NPPC, TOAD/DrivoR;
- strong non-WM controls: UniAD, VAD, DiffusionDrive, DrivoR.

This is census placement only. No new gap has been declared.

## Structural distinctions already visible

These are **map distinctions**, not innovation claims:

```text
WM as data generator
!= WM as representation pretraining
!= WM as auxiliary future objective
!= inference-time future model
!= candidate evaluator/reward model
!= simulator
!= joint world-action policy
```

Likewise:

```text
latent WM
!= one paradigm
```

because some future branches disappear after training, some directly condition trajectory decoding, some score candidates, and newer models jointly generate world/action latents.

Also:

```text
closed-loop
```

must remain split across NAVSIM-style non-reactive pseudo-simulation, CARLA interactive simulation, learned reactive world agents, reconstructed photorealistic simulation, and any real-vehicle evidence.

## Provisional historical skeleton

To be verified during anchor deep reads:

```text
interactive prediction / game-theoretic planning
→ planning-oriented E2E + planning benchmarks
→ generative video / occupancy WMs + world-model pretraining
→ future state explicitly consumed by planner
→ latent self-supervised planning representations
→ unified world-action modeling
→ candidate-specific future latents / planning-oriented representation shaping
→ reactive/counterfactual WMs + RL/post-training + stronger closed-loop evaluation
```

## Next task — Phase-A Round 2

Canonical next task:

`state/NEXT_TASK.md`

Fill the remaining census holes:

- Hydra-MDP family, DriveSuprim, iPad and representative VLA planning controls;
- Think2Drive / world-model RL lineage;
- ViDAR / GenAD only where they help explain planning-relevant representation pretraining;
- benchmark evolution and deployment/inference properties;
- uncertainty/multimodal future treatment;
- credible real-vehicle closed-loop evidence, if any.

Target Phase-A total remains roughly **50–80 works**, after which breadth expansion freezes and the ~15–25 anchor set is finalized.

## Current anchor pool

Approximately 25 provisional anchors are listed in `FIELD_ATLAS.md` / `CENSUS_PHASE_A_ROUND1.md`. They intentionally span conflicting design philosophies. Do not reduce the list based on whether a paper supports prior P2-R/P3 thinking.

## Scientific discipline

During census:

- no per-paper novelty/gap verdict;
- verify representative primary sources, surveys only seed navigation;
- every deep-read anchor later gets strongest evidence + strongest limitation;
- distinguish `AUTHOR CLAIM / DIRECT EXPERIMENTAL EVIDENCE / OUR INFERENCE`;
- trace exact observation → world/future representation → planner flow;
- record what gets direct future supervision and what is inferred;
- use strong non-WM planners as controls;
- keep evaluation regimes distinct.

## Corpus / infrastructure

- Batch 0A remains available but is hypothesis-biased, not representative.
- Public official PDFs/pages may be read directly during census/deep read; local archival can follow asynchronously.
- GitHub Research Brain is the cross-session scientific authority.
- Local corpus agent remains the bulk-ingestion / MinerU / local-code worker.

The repo, not conversation memory, is the canonical research authority.