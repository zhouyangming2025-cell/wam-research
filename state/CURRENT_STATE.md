# CURRENT_STATE

Last updated: 2026-09-14 — Phase C.5 ACTIVE; WorldDrive + World4Drive COMPLETE; SeerDrive NEXT

## Research north star

```text
WAM / World Model + one-stage End-to-End + Planning-centric autonomous driving
```

Core 2.2 WAM is primary. WAM+VLA remains secondary/control until core-WAM coverage is stable. Risk/predictive-risk expertise is optional prior knowledge, not a required destination.

## Methodology in force

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

Phase D problem discovery remains **PAUSED**.

## Completed foundation

```text
Phase A census     CLOSED
Wave 1             CLOSED
Wave 2             CLOSED
Wave 3             CLOSED
Research QA Gate   CLOSED
Wave 4             CLOSED
Phase-C synthesis  COMPLETE FIRST PASS
```

The prior synthesis remains a provisional coordinate system, not final core-WAM coverage.

## Phase C.5 core-WAM correction progress

```text
WorldDrive      COMPLETE
World4Drive     COMPLETE
SeerDrive       NEXT
Drive-JEPA      PENDING
Metis           PENDING
DynFlowDrive    PENDING
Discrete-WAM    PENDING
GraphWorld      PENDING
```

Canonical coverage:

```text
landscape/CORE_WAM_2_2_COVERAGE_AUDIT.md
```

Canonical new audits:

```text
audits/literature/PHASE_C5_WORLDDRIVE_AUDIT.md
audits/literature/PHASE_C5_WORLD4DRIVE_AUDIT.md
```

## WorldDrive stable result

Official source audit:

```text
TabGuigui/WorldDrive@c375ee1e1fe86ace175609db1ed90fd6db89673b
```

Mechanism:

```text
TA-DWM trajectory-conditioned generative pretraining
→ transfer/freeze vision + motion representations
→ multimodal candidate planner
→ frozen TA-DWM candidate-future latent as FAR training teacher
→ lightweight distilled future feature + ranking at inference
→ no full diffusion rollout online
```

Subtype:

```text
DISTILLED WORLD-MODEL FORESIGHT
```

Strongest matched evidence:

```text
31.4 no pretrain
84.9 generic CogVideoX VAE
85.8 + TA-DWM vision
86.9 + TA-DWM motion

86.9 base planner
87.0 trajectory-only rewarder
88.1 + distilled future feature
```

Important boundary: the huge representation jump is dominated by generic video/VAE pretraining; FAR also receives PDMS ranking supervision; alternative-action real future GT is unavailable.

## World4Drive stable result

Official source audit:

```text
ucaszyp/World4Drive@cffb51adeb1f7d02b49c4b74d7262ded62a33ac8
```

Mechanism:

```text
current physical latent L_t
+ 6 intention queries
→ 6 ego trajectories T^k
→ action tokens A^k
→ 6 intention-conditioned future world latents L_{t+n}^k
→ ScoreNet
→ select trajectory with highest future-latent score at inference
```

Subtype:

```text
ONLINE LATENT FORESIGHT
```

Training observes only one actual future latent and chooses the predicted mode nearest to it as the target class. Therefore:

```text
K candidate/intention future outputs
!=
K real alternative-action future labels
```

Strongest matched component evidence:

```text
physical priors + intentions, no WM   0.61 L2 / 0.36 collision
physical priors + intentions + WM     0.50    / 0.16
```

This supports the whole future-latent predictor + world-model-selector mechanism beyond multimodal intentions alone.

Evaluation:

```text
nuScenes = open-loop planning
NAVSIM   = non-reactive data-driven planning evaluation under project taxonomy
```

The released repo source audit verifies the core W4D architecture. A separate clearly identifiable NAVSIM implementation path was not established, so paper-level NAVSIM evidence is kept distinct from source-verified implementation details.

## Emerging core-WAM interface axis

```text
LAW
training-only future shaping

WorldDrive
distilled future foresight

World4Drive
online compact latent foresight

DriveLaW
online generative hidden state → action

WoTE
online future BEV → reward

DA-WAM
candidate → future latent → scorer
```

This strengthens the view that the useful planning taxonomy is **where and how future/world information enters action selection**, not simply RGB-vs-BEV-vs-latent.

## Existing stable field controls retained

```text
world-prediction quality != planning evidence
future information is not automatically beneficial
candidate-specific output != candidate-specific observed counterfactual supervision
WM-assisted planning != full online generative rollout
world completeness != decision relevance
candidate ranking/scoring is an independent bottleneck
evaluation regime is part of the claim
reactive feasibility != counterfactual behavioral truth
```

## Immediate next task

See `state/NEXT_TASK.md`.

Deep-read **SeerDrive**, specifically testing whether its claimed bidirectional scene↔planning iteration introduces a genuinely distinct WAM planning interface or mainly re-instantiates older iterative prediction-planning refinement in a future-scene latent space.

## Still forbidden

```text
no problem/gap declaration
no method design
no broad VLA expansion
no forced risk-field insertion
```

GitHub remains the Research Knowledge Authority; public official papers/repos are primary evidence for decision-critical claims.
