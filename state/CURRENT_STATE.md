# CURRENT_STATE

Last updated: 2026-09-14 — Phase C.5 Core-WAM Coverage Correction ACTIVE; WorldDrive COMPLETE

## Research north star

```text
World Model / WAM + End-to-End + Planning-centric autonomous driving
```

Planning is the center of gravity. Risk/predictive-risk expertise is optional prior knowledge, not a required destination.

## Scope priority correction

The current project distinguishes:

```text
PRIMARY:
core WAM / World Model + one-stage end-to-end planning

SECONDARY CONTROL:
WAM+VLA / VLA-centric planning
```

VLA papers remain useful as controls, but they should not consume equal priority while the core WAM branch is incomplete.

Canonical correction:

```text
landscape/PURE_WAM_PRIORITY_CORRECTION.md
```

## Methodological rule in force

```text
FIELD UNDERSTANDING FIRST
→ complete core-WAM coverage
→ comparative anchor deep reads
→ WAM-only synthesis
→ evidence QA
→ only then adversarial problem discovery
→ falsification
→ method design
```

P1/P2-R/P3 remain historical probes and do not organize reading.

## Current active stage

```text
PHASE C.5 — CORE-WAM COVERAGE CORRECTION
```

Phase D problem discovery is **PAUSED**.

Completed foundation:

```text
Phase A census     CLOSED
Wave 1             CLOSED
Wave 2             CLOSED
Wave 3             CLOSED
Research QA Gate   CLOSED
Wave 4             CLOSED
Phase-C synthesis  COMPLETE FIRST PASS
```

The first-pass synthesis remains useful but is not final core-WAM coverage.

## Core-WAM correction set

User-provided 2.2 reading map identified:

```text
WorldDrive
World4Drive
SeerDrive
Drive-JEPA
Metis
DynFlowDrive
Discrete-WAM
GraphWorld
```

Current progress:

```text
WorldDrive      COMPLETE — primary paper + official code audit
World4Drive     NEXT
SeerDrive       PENDING
Drive-JEPA      PENDING
Metis           PENDING
DynFlowDrive    PENDING
Discrete-WAM    PENDING
GraphWorld      PENDING
```

Canonical coverage map:

```text
landscape/CORE_WAM_2_2_COVERAGE_AUDIT.md
```

## WorldDrive — stable result

Canonical audit:

```text
audits/literature/PHASE_C5_WORLDDRIVE_AUDIT.md
```

Official repo audited at:

```text
TabGuigui/WorldDrive@c375ee1e1fe86ace175609db1ed90fd6db89673b
```

Exact mechanism:

```text
TA-DWM trajectory-conditioned scene-generation pretraining
→ learn shared vision + motion representation
→ transfer/freeze visual + trajectory encoders into planner
→ multi-modal trajectory vocabulary planner creates candidates
→ frozen TA-DWM generates candidate-conditioned future-latent teachers during FAR training
→ FAR distills candidate future features + learns PDMS preference ranking
→ inference uses lightweight distilled future features to score/select trajectories
→ no full TA-DiT diffusion future rollout at inference
```

This introduces a core subtype not explicit enough in the previous taxonomy:

```text
DISTILLED WORLD-MODEL FORESIGHT
```

### Strongest matched evidence

Representation inheritance:

```text
31.4  no pretrain
84.9  CogVideoX VAE prior
85.8  + TA-DWM vision
86.9  + TA-DWM motion
```

Interpretation boundary:

```text
the dominant jump is generic VAE/video pretraining;
TA-DWM-specific vision+motion representation contributes the smaller 84.9→86.9 increment.
```

Future-aware rewarder:

```text
86.9  base planner
87.0  + trajectory-feature rewarder
88.1  + distilled future feature
```

This is meaningful evidence that candidate-conditioned future representation adds value beyond trajectory-feature-only scoring in the matched WorldDrive setup.

### Supervision / causal boundary

FAR uses both:

```text
TA-DWM latent alignment
+
PDMS preference/ranking supervision
```

and alternative candidate futures are model-generated; ordinary logged data does not provide real observed surrounding-world futures for every unexecuted ego trajectory.

Thus WorldDrive does not invalidate:

```text
candidate-specific output != candidate-specific observed counterfactual supervision
```

### Evaluation boundary

```text
NAVSIM / NAVSIM-v2 = planning evidence under their benchmark semantics
nuScenes            = open-loop trajectory/collision evaluation
real-vehicle closed loop = not established
```

## Existing stable field controls retained

```text
world-prediction quality != planning evidence
future information is not automatically beneficial
candidate-specific output != candidate-specific observed counterfactual supervision
WM-assisted planning != full online generative model-based planning
world completeness != decision relevance
generative action modeling != world modeling
candidate ranking/scoring is an independent bottleneck
closed-loop must be decomposed into feedback channels
sensor photorealism != behavioral realism
reactive feasibility != counterfactual behavioral truth
```

WorldDrive strengthens rather than overturns the importance of decomposing:

```text
representation pretraining
vs candidate generation
vs reward/scoring
vs future representation
vs online generation cost
```

## Immediate next task

See `state/NEXT_TASK.md`.

Deep-read **World4Drive** from its primary paper + official code, then continue the remaining core-WAM set.

## Still forbidden

```text
no problem/gap declaration
no method design
no broad VLA expansion
no forced risk-field insertion
no assuming similar paper names are identical
no treating first-pass Phase-C synthesis as final WAM coverage
```

## Research Brain architecture

GitHub is the Research Knowledge Authority. Raw MD + figures are the persistent GPT-readable primary-text layer; canonical PDFs / official public papers remain source authority for decision-critical claims.
