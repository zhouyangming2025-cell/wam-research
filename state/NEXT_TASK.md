# NEXT_TASK

## 唯一下一任务

> Finish the **Phase-B Wave-1 quantitative/comparability audit** before moving to visual/latent WAM anchors.

Phase A is closed and Wave 1 has started.

Current Wave-1 artifact:

`landscape/PHASE_B_WAVE1_SYNTHESIS.md`

Status inside that memo:

```text
comparative first pass = COMPLETE
historical/control structure = ESTABLISHED
quantitative comparability audit = PENDING
Wave-1 final synthesis gate = OPEN
```

## Wave-1 anchors

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

## What the first pass already established

The modern WAM wave did not invent the underlying planning problems. Before it, the field already contained:

```text
conditional / interactive future prediction
joint prediction + ego planning
prediction-metric vs driving-performance mismatch
planning-oriented full-stack representation/task coordination
multimodal direct action generation
candidate scoring / hard-negative selection
planning-specific closed-loop evaluation
scalable non-reactive simulation-based scoring
```

Strong non-WM planners therefore remain mandatory controls for any later claim that world modeling itself caused a planning gain.

## Remaining Wave-1 audit

Do **not** add papers. Tighten these five points from primary text / matched settings:

1. **M2I** — exact joint-sample selection and the boundary between conditional prediction and intervention/causality.
2. **GameFormer** — isolate raw learned planner vs cost-based refinement contribution; keep WOMD non-reactive replay separate from nuPlan CL-R.
3. **UniAD** — trace exactly how MotionFormer and OccFormer reach the planner and what the planner ablations isolate.
4. **DiffusionDrive vs DriveSuprim** — determine which NAVSIM split/version, sensors, data, backbone and metric definitions are actually comparable before treating their scores as controls.
5. **nuPlan vs NAVSIM** — lock protocol/evaluation differences that later WAM papers inherit; note version-specific metric changes rather than treating benchmark names as fixed semantics.

## Required closeout update

Revise `landscape/PHASE_B_WAVE1_SYNTHESIS.md` so the final Wave-1 state becomes:

```text
per-paper evidence audit = COMPLETE
comparability boundaries = EXPLICIT
historical/non-WM/evaluation baseline = STABLE
Wave 1 = CLOSED
```

Then update `FIELD_ATLAS.md` only with field-level conclusions that survive the audit and choose the exact Wave-2 comparison order from `landscape/PHASE_B_ANCHORS.md`.

## Stop condition

Wave 1 closes when later WAM papers can be judged against a stable baseline without falsely attributing gains to WM that could instead come from interaction prediction, representation/task coordination, multimodal action modeling, scorer training, or benchmark choice.

Do not declare a gap. Do not design a method. Do not broaden the corpus. Do not reactivate P2-R/P3. Do not force risk-field knowledge into the interpretation.