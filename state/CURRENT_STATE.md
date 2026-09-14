# CURRENT_STATE

Last updated: 2026-09-14 — Phase-B Wave-1 first comparative pass complete

## Research north star

```text
World Model + End-to-End + Planning-centric autonomous driving
```

Planning is the center of gravity. Risk/predictive-risk expertise is optional prior knowledge, not a required destination.

Canonical rules: `state/RESEARCH_PRINCIPLES.md`.

## Methodological rule in force

```text
FIELD UNDERSTANDING FIRST
→ comparative anchor deep reads
→ cross-family synthesis
→ only then research-problem / gap discovery
```

P1/P2-R/P3 remain parked historical probes and do not organize the reading program.

## Current active stage

```text
FIELD RECONSTRUCTION — PHASE B: WAVE 1 IN PROGRESS
```

Phase A is closed:

```text
P0001–P0060 registered
58 RAW_MD_READY
F1–F11 census coverage PASS
broad acquisition FROZEN
25 representative Phase-B anchors selected
```

Canonical Phase-A artifacts:

- `landscape/CENSUS_PHASE_A_ROUND1.md`
- `landscape/CENSUS_PHASE_A_ROUND2.md`
- `landscape/FIELD_ATLAS.md`
- `landscape/PHASE_B_ANCHORS.md`

## Phase-B Wave 1

Wave 1 anchors:

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

Current synthesis:

`landscape/PHASE_B_WAVE1_SYNTHESIS.md`

Status:

```text
comparative first pass = COMPLETE
historical/control structure = ESTABLISHED
quantitative comparability audit = PENDING
Wave-1 final gate = OPEN
```

## First-pass structural understanding

1. **Conditional/interacting futures predate modern WAMs.** M2I explicitly predicts reactor futures conditioned on influencer futures; GameFormer iteratively reasons over agents’ future trajectories and jointly plans ego motion.
2. **Conditional response is fragile to upstream future error.** M2I’s direct experiment improves substantially with ground-truth influencer future but can underperform marginal prediction when conditioned on a single erroneous predicted influencer future.
3. **Interaction-aware planning gains are not architecture-pure.** GameFormer’s explicit cost-based refinement contributes a large absolute closed-loop gain; learned interaction and downstream optimization must be separated.
4. **Prediction metrics can mis-rank downstream driving.** What Truly Matters identifies a dynamics gap and computation/latency effects; static ADE/minADE is not sufficient evidence of planner value.
5. **Planning-oriented representations existed before WAM framing.** UniAD coordinates tracking/map/motion/occupancy around planning and demonstrates collision-vs-imitation trade-offs.
6. **Generative planning is not synonymous with world modeling.** DiffusionDrive generates multimodal action trajectories directly; DriveSuprim scores/selects candidates precisely; neither requires an inference-time future world model.
7. **Evaluation regimes encode different compromises.** nuPlan formalizes OL/CL-NR/CL-R planning evaluation; NAVSIM intentionally removes reactivity to preserve real sensor inputs, scale and simulation-based metrics.

These are baseline facts/interpretations for later WAM comparison, not research gaps.

## Immediate next task

See `state/NEXT_TASK.md`.

Finish Wave-1 comparability audit:

- M2I conditional vs causal/intervention boundary;
- GameFormer raw learned interaction vs refinement contribution;
- UniAD exact MotionFormer/OccFormer→planner flow;
- DiffusionDrive vs DriveSuprim matched NAVSIM conditions;
- nuPlan vs NAVSIM protocol/version boundaries.

Then close Wave 1 and choose exact Wave-2 comparative reading order.

## Still forbidden

```text
no gap declaration
no method design
no broad paper accumulation
no P2-R/P3 rescue program
no forced risk-field insertion
```

## Research Brain architecture

GitHub raw MD + figures are the persistent GPT-readable primary-text layer; canonical PDFs remain source authority where archived/available. The local agent is now on-demand infrastructure support rather than a broad-ingestion worker.

A fresh session should read:

```text
START_HERE.md
state/CURRENT_STATE.md
state/NEXT_TASK.md
landscape/FIELD_ATLAS.md
landscape/PHASE_B_ANCHORS.md
landscape/PHASE_B_WAVE1_SYNTHESIS.md
```
