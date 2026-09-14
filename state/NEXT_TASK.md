# NEXT_TASK

## 唯一下一任务

> Execute **Phase D — Adversarial Problem Discovery** from the completed Waves 1–4 field synthesis.

Canonical field synthesis:

```text
landscape/PHASE_C_WAVES1_4_FIELD_SYNTHESIS.md
```

Status:

```text
Wave 1            CLOSED
Wave 2            CLOSED
Wave 3            CLOSED
Research QA Gate  CLOSED
Wave 4            CLOSED
Phase C synthesis COMPLETE FIRST PASS
Phase D           NEXT
```

Broad corpus acquisition remains frozen unless a specific candidate problem requires one tightly scoped prior-art check.

## Phase-D purpose

Do **not** choose a method or reuse a historical hypothesis first.

Start from recurrent tensions / under-measured planning properties discovered in Phase C and ask whether any of them correspond to a real, consequential, falsifiable planning problem.

Required chain:

```text
Observed / measurable planning difficulty
→ failure mechanism
→ missing capability or structural trade-off
→ why current approaches cannot easily handle it
→ strongest counterexample / simpler explanation
→ falsifiable test
→ only if it survives: research question
```

## Candidate evidence-gap pool — not preselected gaps

Phase C identified:

```text
E1  real alternative-action surrounding-agent ground truth
E2  reactive simulator quality → planner decision quality
E3  simultaneous sensor-realistic + behaviorally validated closed loop
E4  intervention-conditioned uncertainty calibration
E5  long-horizon compounding under ego/sensor/agent/model feedback
E6  compute-normalized planning benefit
E7  representation semantics vs scale/capacity
E8  real-vehicle closed-loop validation
E9  standardized feedback-semantic reporting
E10 planner robustness to world-model error
```

These are evidence gaps only. Most may fail as research problems.

## Adversarial screen for every candidate

For each candidate, create one row with:

```text
1. exact observed/plausibly measurable failure
2. why it matters to ego planning
3. strongest direct evidence from current corpus
4. strongest historical precedent
5. strongest 2025–2026 neighboring solution
6. strongest non-WM explanation / baseline
7. strongest counterexample
8. whether the problem is WAM-specific or generic ML/planning
9. whether the problem can be measured without unavailable counterfactual GT
10. realistic evaluation regime capable of falsifying it
11. minimum experiment that could kill the problem
12. verdict: SURVIVES / WEAK / KILLED / EVIDENCE INSUFFICIENT
```

## Binding anti-shortcut rules

Do not accept:

```text
“no one has module X”
“paper Y did not evaluate metric Z”
“counterfactual GT is unavailable, therefore this is automatically a gap”
“reactive world models are new, therefore reactivity is a gap”
“better planning needs risk, therefore add risk field”
```

A valid problem must show a planning consequence, not merely a missing benchmark or representation.

## Required strongest attacks

Every survivor must be attacked by at least:

```text
Historical interaction/planning:
M2I / GameFormer / What Truly Matters

Strong non-WM planning:
UniAD / DiffusionDrive / DriveSuprim / ORION

Predictive-representation counterexamples:
OccWorld / LAW / DriveLaW / Auto-JEPA

Candidate-world planning:
Drive-WM / WoTE / DA-WAM

Closed-loop / reactive simulation:
Bench2Drive / HUGSIM / ReactSim-Bench / CausalDrive

Policy-imagination control:
Think2Drive
```

No candidate needs every paper, but no candidate may ignore the strongest relevant control.

## First deliverable

Create:

```text
landscape/PHASE_D_PROBLEM_DISCOVERY_ROUND1.md
```

It should contain:

```text
- 5–8 candidate problem statements max;
- adversarial evidence table;
- kill criteria for each;
- no method proposals;
- no novelty claim;
- explicit NONE / EVIDENCE INSUFFICIENT option.
```

Do not generate ten vague “future work” topics. Prefer fewer candidates with stronger falsification logic.

## Stop condition

Round 1 stops when every candidate is labeled:

```text
SURVIVES
WEAK
KILLED
or EVIDENCE INSUFFICIENT
```

Only `SURVIVES` candidates proceed to targeted prior-art/failure verification.

## Still forbidden

```text
no method design
no forced risk-field insertion
no automatic P2-R/P3 revival
no broad literature accumulation
no gap declaration from missing modules
no conflation of reactive feasibility with true counterfactual response
no conflation of simulator quality with planner benefit
```
