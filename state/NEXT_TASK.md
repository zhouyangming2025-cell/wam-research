# NEXT_TASK

## 唯一下一任务

> Deep-read **SeerDrive** as the third core anchor in **Phase C.5 — Core-WAM Coverage Correction**.

Canonical coverage audit:

```text
landscape/CORE_WAM_2_2_COVERAGE_AUDIT.md
```

Completed audits:

```text
audits/literature/PHASE_C5_WORLDDRIVE_AUDIT.md
audits/literature/PHASE_C5_WORLD4DRIVE_AUDIT.md
```

## Status

```text
Phase D           PAUSED
Phase C.5         ACTIVE
WorldDrive        COMPLETE
World4Drive       COMPLETE
SeerDrive         NEXT
Drive-JEPA        PENDING
Metis             PENDING
DynFlowDrive      PENDING
Discrete-WAM      PENDING
GraphWorld        PENDING
```

## Stable comparison carried forward

```text
LAW
= training-only future-latent shaping

WorldDrive
= DISTILLED FORESIGHT:
  full generative future teacher during training
  → lightweight candidate future surrogate at inference

World4Drive
= ONLINE LATENT FORESIGHT:
  six intentions → six trajectories → six future latents
  → ScoreNet → select

WoTE
= online future BEV rollout → reward

DriveLaW
= online world-generator hidden state → direct action generator

DA-WAM
= candidate → future latent → score
```

## SeerDrive audit target

The paper appears to introduce bidirectional coupling between future-scene modeling and planning. Trace exactly:

```text
1. scene representation: RGB/BEV/latent and temporal history
2. first planning trajectory/proposals
3. first future-scene prediction
4. direction future scene → trajectory refinement
5. direction planned trajectory → future scene refinement
6. number of iterative rounds and whether weights are shared
7. exact future supervision and whether it is factual or candidate-specific
8. inference-time loop: what remains online and how much computation it costs
9. trajectory multimodality / candidate selection mechanism
10. matched ablations for each coupling direction and iteration count
11. evaluation regime(s), horizon, latency
12. relation to PPAD/GameFormer iterative prediction-planning predecessors
13. relation to LAW/World4Drive/WoTE/DA-WAM
14. strongest evidence and strongest simpler explanation
```

Required classification:

```text
Is SeerDrive primarily:
A. iterative predictive representation refinement,
B. bidirectional online world↔planning co-refinement,
C. candidate consequence evaluation,
D. another mechanism?
```

Historical novelty must be separated from older iterative prediction-planning concepts such as PPAD/GameFormer.

## Stop condition

Do not move to Drive-JEPA until the full deployed SeerDrive loop can be stated without ambiguity and its world-model contribution is separated from generic iterative decoder/refinement gains.

## Still forbidden

```text
no gap/problem selection
no method design
no broad VLA expansion
no forced risk-field insertion
```
