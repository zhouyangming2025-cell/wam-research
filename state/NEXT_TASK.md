# NEXT_TASK

## 唯一下一任务

> Deep-read **World4Drive** as the second anchor in **Phase C.5 — Core-WAM Coverage Correction**.

Canonical coverage audit:

```text
landscape/CORE_WAM_2_2_COVERAGE_AUDIT.md
```

WorldDrive deep read:

```text
audits/literature/PHASE_C5_WORLDDRIVE_AUDIT.md
```

## Status

```text
Wave 1            CLOSED
Wave 2            CLOSED
Wave 3            CLOSED
Research QA Gate  CLOSED
Wave 4            CLOSED
Phase-C synthesis COMPLETE FIRST PASS
Phase D           PAUSED
Phase C.5         ACTIVE
WorldDrive        COMPLETE
World4Drive       NEXT
```

## Scope

Primary direction:

```text
WAM + one-stage / end-to-end autonomous-driving planning
```

Secondary/control direction:

```text
WAM+VLA / VLA-centric planning
```

Do not broaden into VLA before core WAM coverage is stable.

## WorldDrive result carried forward

WorldDrive is now source-audited as:

```text
TA-DWM trajectory-conditioned generative pretraining
→ inherited/frozen vision + motion representation
→ multimodal candidate planner
→ TA-DWM candidate-future latent teacher during FAR training
→ lightweight distilled candidate-future feature at inference
→ scalar future-aware reward / trajectory selection
```

Important distinction:

```text
full TA-DiT diffusion future rollout = training teacher only
full diffusion rollout at planner inference = NO
```

This introduced a new core subtype:

```text
DISTILLED WORLD-MODEL FORESIGHT
```

## Current deep-read order

```text
1. WorldDrive      COMPLETE
2. World4Drive     NEXT
3. SeerDrive
4. Drive-JEPA
5. Metis
6. DynFlowDrive
7. Discrete-WAM
8. GraphWorld
```

## World4Drive audit requirements

Trace from primary paper + official code:

```text
1. exact visual/BEV/latent input and history representation
2. what “physical latent world model” actually predicts numerically
3. intention/action conditioning form
4. multimodal trajectory proposal mechanism
5. whether trajectory is generated before future latent, after future latent, or jointly
6. exact world-model selector / evaluator path
7. which future branch remains at inference
8. factual vs alternative-action supervision
9. frozen/trainable components and training stages
10. matched ablations isolating latent-world contribution
11. NAVSIM / nuScenes evaluation semantics
12. latency / candidate count / planning horizon
13. strongest evidence and strongest alternative explanation
14. exact relation to LAW / WorldDrive / WoTE / Epona / DA-WAM
```

Required classification:

```text
predictive representation shaping?
online latent future?
candidate consequence evaluation?
joint world-action generation?
intent-conditioned future planning?
hybrid?
```

## Stop condition for World4Drive

Do not move to SeerDrive until we can state without ambiguity:

```text
observation/history
→ world/latent model
→ intention / candidate trajectories
→ future latent(s)
→ selector / planner
→ final trajectory
```

and identify which quantities are observed targets, model-generated alternatives, frozen representations and inference-time inputs.

## Phase C.5 stop condition

Do not reopen Phase D until:

```text
all eight 2.2 WAM papers are verified/placed;
all decision-relevant mechanisms are deep-read;
existing Phase-C conclusions are rechecked against them;
a WAM-only historical/interface synthesis is stable.
```

## Still forbidden

```text
no problem/gap selection yet
no method design
no broad VLA expansion
no forced risk-field insertion
no treating similar paper names as the same work
```
