# LATEST — Handoff

Session: 2026-09-14 — Phase A closed; Phase-B Wave 1 in progress.

## New-session fast path

```text
1. START_HERE.md
2. state/CURRENT_STATE.md
3. state/NEXT_TASK.md
4. landscape/FIELD_ATLAS.md
5. landscape/PHASE_B_ANCHORS.md
6. landscape/PHASE_B_WAVE1_SYNTHESIS.md
```

Do not default to P2-R. Do not reload the whole corpus or old chats by default.

## Research identity

```text
World Model + End-to-End + Planning-centric autonomous driving
```

Risk-field / predictive-risk expertise is optional prior knowledge, not a required destination.

## Phase-A status

```text
F1–F11 census coverage = PASS
P0001–P0060 = 60 registered
58 RAW_MD_READY
broad acquisition = FROZEN
25 Phase-B anchors = FIXED
```

Canonical closeout artifacts:

- `landscape/CENSUS_PHASE_A_ROUND2.md`
- `landscape/FIELD_ATLAS.md`
- `landscape/PHASE_B_ANCHORS.md`

## Phase-B Wave 1 has started

Wave 1:

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

Current status:

```text
comparative first pass = COMPLETE
historical/control structure = ESTABLISHED
quantitative comparability audit = PENDING
Wave-1 final gate = OPEN
```

## First-pass findings that should survive into later reading

1. M2I shows conditional influencer→reactor future modeling clearly predates modern WAM language, while also exposing conditioning-error propagation.
2. GameFormer already performs hierarchical future-interaction reasoning + ego planning; its final closed-loop result is materially helped by an explicit refinement planner, so learned interaction and downstream optimization must be separated.
3. What Truly Matters shows static prediction metrics can misrepresent downstream driving and quantifies a large dynamics-gap contribution in its simulator setup; runtime/compute also affects driving performance.
4. UniAD establishes planning-oriented representation/task coordination as a strong pre-WAM baseline; planning benefits cannot automatically be credited to future-world prediction.
5. DiffusionDrive shows strong multimodal **action** generation without a WM; DriveSuprim shows strong candidate scoring/selection without a WM.
6. nuPlan and NAVSIM represent different evaluation compromises: nuPlan formalizes planning closed loop; NAVSIM intentionally removes reactivity to retain real sensor data, scale and simulation-based metrics.

These are not gap claims.

## Immediate next task

Read `state/NEXT_TASK.md`.

Finish the Wave-1 comparability audit:

- M2I conditional vs intervention boundary;
- GameFormer raw model vs refinement contribution;
- UniAD MotionFormer/OccFormer→planner path;
- DiffusionDrive vs DriveSuprim NAVSIM comparability;
- nuPlan vs NAVSIM protocol/version boundaries.

Then close Wave 1 and only after that enter Wave 2.

## Still forbidden

```text
no gap declaration
no method design
no broad paper accumulation
no P2-R/P3 optimization
no forced risk-field insertion
```

The repo, not conversation memory, is the canonical research authority.