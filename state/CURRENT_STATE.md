# CURRENT_STATE

Last updated: 2026-09-14 — Phase-A closeout complete

## Research north star

```text
World Model + End-to-End + Planning-centric autonomous driving
```

Planning is the center of gravity. Perception, video generation, JEPA/latent prediction, VLA, safety/risk modeling and simulation are supporting means, not the project identity.

**Risk field is optional, not required.** Prior risk/predictive-risk expertise is an asset, not a destination.

Canonical rules: `state/RESEARCH_PRINCIPLES.md`.

## Methodological rule in force

```text
FIELD UNDERSTANDING FIRST
→ reconstruct the field
→ deep-read representative anchors comparatively
→ synthesize historical transitions / interfaces / supervision / evaluation / trade-offs
→ only then reopen problem/gap discovery
```

P1/P2-R/P3 remain parked historical probes and do not organize the reading program.

## Current active stage

```text
FIELD RECONSTRUCTION — PHASE B: ANCHOR DEEP READS
```

Phase A has passed its closeout gate.

## Phase-A closeout facts

Corpus:

```text
P0001–P0060 registered
58 RAW_MD_READY
2 lawful-source blockers:
  P0008 NPPC
  P0020 Bahram 2016
```

Scientific census:

- Round 1: `landscape/CENSUS_PHASE_A_ROUND1.md`
- Round 2: `landscape/CENSUS_PHASE_A_ROUND2.md`
- Common taxonomy: `landscape/PLANNING_WAM_TAXONOMY.md`
- Updated cross-family map: `landscape/FIELD_ATLAS.md`

The F1–F11 coverage audit now passes at census depth. Broad paper acquisition is **frozen**. `Hydra-MDP++` and `NAVSIM-v2` are optional follow-ups rather than blockers.

## Important field distinctions earned by Phase A

These are map structure, not research gaps:

1. **WM role matters more than the label alone.** Future prediction can be a pretraining task (ViDAR), auxiliary planner supervision (LAW-like), inference-time representation (DriveLaW), per-candidate future (DA-WAM), joint world-action model, or RL training simulator (Think2Drive).
2. **Strong planning does not require an explicit WM.** UniAD, DiffusionDrive, Hydra-MDP, DriveSuprim, iPad and VLA planners provide necessary controls for representation, action modeling, scoring and supervision effects.
3. **VLA/VLM planning is adjacent to WAM, not synonymous with it.** Semantic world knowledge and generative action can improve planning without an explicit environment transition model.
4. **Benchmark choice is part of the scientific result.** nuScenes open-loop legacy, nuPlan OL/CL-NR/CL-R, NAVSIM non-reactive pseudo-simulation, Bench2Drive CARLA interaction and HUGSIM photorealistic closed loop prove different things.
5. **The original nuScenes paper is not a planning benchmark.** Later planning papers retrofit open-loop trajectory protocols to its logs.
6. **Modern interaction/reactivity concepts have older prediction/planning roots.** M2I, GameFormer and related work must be understood before claiming WAM-specific conceptual novelty.

## Phase-B anchor set

Canonical file:

`landscape/PHASE_B_ANCHORS.md`

25 anchors are selected for explanatory coverage, not hypothesis support. Secondary papers remain available and can be promoted only when an anchor comparison exposes a concrete missing link.

## Immediate next task

See `state/NEXT_TASK.md`.

Phase-B Wave 1:

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

Goal: reconstruct the pre-/non-WAM planning, interaction and evaluation baseline before interpreting modern WM gains.

## What remains forbidden

```text
no gap declaration yet
no method design yet
no P2-R rescue/kill program
no broad paper accumulation
no forced risk-field insertion
```

Phase B should produce comparative scientific understanding, not eight isolated paper summaries.

## Research Brain architecture

- Canonical PDFs live on local/NAS when archived.
- GitHub raw MD + figures are the persistent GPT-readable primary-text layer.
- Paper Cards are curated after deep review.
- `landscape/` contains cross-paper field understanding.
- Local corpus agent handles acquisition/conversion/local code; GPT-5.6 Sol handles scientific reading/synthesis/state updates.

## New-session bootstrap

A fresh session should read:

```text
START_HERE.md
state/CURRENT_STATE.md
state/NEXT_TASK.md
landscape/FIELD_ATLAS.md
landscape/PHASE_B_ANCHORS.md
```

Then load only the Wave-1 primary texts needed for the active comparative read.