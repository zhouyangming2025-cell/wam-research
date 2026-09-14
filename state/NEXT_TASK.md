# NEXT_TASK

## 唯一下一任务

> Execute **Phase-B Wave 1 comparative deep reads** to reconstruct the historical planning / interaction / evaluation baseline before interpreting modern WAM gains.

Phase A is closed:

```text
60 registered records
58 RAW_MD_READY
F1–F11 coverage audit PASS
broad ingestion FROZEN
25 Phase-B anchors selected
```

Canonical files:

- `landscape/FIELD_ATLAS.md`
- `landscape/CENSUS_PHASE_A_ROUND1.md`
- `landscape/CENSUS_PHASE_A_ROUND2.md`
- `landscape/PHASE_B_ANCHORS.md`

## Wave 1 papers

Read comparatively, not as eight independent summaries:

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

## Wave-1 scientific questions

The objective is to establish the **pre-/non-WAM baseline** for the field:

1. What did interaction modeling already mean before modern driving WMs?
2. How were prediction and planning coupled before current world-action models?
3. What weaknesses of open-loop trajectory matching were already known?
4. What does a strong planning-oriented E2E stack achieve without an explicit WM?
5. What does a strong direct multimodal action model achieve without an explicit WM?
6. What does a strong trajectory-selection/scoring planner achieve without an explicit WM?
7. How do nuPlan and NAVSIM differ in what their metrics/simulation can establish?
8. Which later WAM claims would be confounded by stronger representation, action modeling, scoring, or evaluation protocol if these controls were ignored?

## Per-anchor deep-read contract

For each anchor record:

```text
Exact problem in historical context
Input / numerical representation
Future/world representation, if any
Direct supervision vs proxy/inferred future
Inference-time data flow
Does any future/WM branch survive inference?
Planner interface
Planning output
Multimodality / uncertainty and how the planner consumes it
Evaluation regime and its evidentiary boundary
Strongest direct experimental evidence
Strongest limitation / alternative explanation
What the paper proves
What it does NOT prove
Historical transition role
Closest supporting / contradicting work
```

Separate:

```text
AUTHOR CLAIM
DIRECT EXPERIMENTAL EVIDENCE
OUR INFERENCE
```

## Required Wave-1 output

Create one comparative synthesis, not eight disconnected cards:

`landscape/PHASE_B_WAVE1_SYNTHESIS.md`

It must answer:

```text
What problems existed before the modern WAM wave?
Which were prediction problems, planning problems, supervision problems, or evaluation problems?
What capabilities were already obtainable without a WM?
What benchmark assumptions shaped the apparent progress?
What conceptual inheritance should later WAM papers be compared against?
```

Paper Cards may be updated alongside the synthesis where useful, but the synthesis is the gate artifact.

## Stop condition

Stop Wave 1 when the comparative synthesis can explain the historical/control baseline coherently. Then choose Wave-2 reading order from `PHASE_B_ANCHORS.md` based on what Wave 1 shows.

Do not add broad new papers. Do not declare a gap. Do not design a method. Do not reactivate P2-R/P3 as search targets. Do not force risk-field knowledge into the interpretation.