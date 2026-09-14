# NEXT_TASK

## 唯一下一任务

> Deep-read **WorldDrive** as the first anchor in **Phase C.5 — Core-WAM Coverage Correction**.

Canonical first-pass audit:

```text
landscape/CORE_WAM_2_2_COVERAGE_AUDIT.md
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
missing 2.2 identities / code status FIRST-PASS VERIFIED
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

## First-pass verified missing core set

```text
WorldDrive      ANCHOR — official code released
World4Drive     ANCHOR — official code released
SeerDrive       ANCHOR — official code released
Drive-JEPA      ANCHOR/BOUNDARY — official code released
Metis           ANCHOR — official repo exists; source code still absent as of 2026-09-14
DynFlowDrive    ANCHOR — official repo exists; implementation still unreleased
Discrete-WAM    ANCHOR — no official code found in first-pass search
GraphWorld      ANCHOR — no official code found in first-pass search
```

Anti-alias rules remain binding:

```text
Auto-JEPA != Drive-JEPA
Drive-WM  != WorldDrive
DA-WAM    != Discrete-WAM
```

## Current deep-read order

```text
1. WorldDrive      NEXT
2. World4Drive
3. SeerDrive
4. Drive-JEPA
5. Metis
6. DynFlowDrive
7. Discrete-WAM
8. GraphWorld
```

## WorldDrive audit requirements

Trace from primary paper + official code:

```text
1. TA-DWM observation/action/future representation
2. trajectory vocabulary numerical form
3. what visual encoder and motion encoder learn during world-model pretraining
4. exactly which encoders/weights are transferred into the downstream planner
5. Multi-modal Planner candidate/proposal generation
6. Future-aware Rewarder input, target and inference path
7. whether FAR consumes an actually rolled-out future at inference or a distilled/current representation
8. planner/FAR training stages and frozen/trainable components
9. NAVSIM / NAVSIM-v2 / nuScenes evaluation semantics
10. matched ablations: planner without WM pretraining, without motion representation, without FAR, etc.
11. latency / candidate count / planning frequency
12. strongest evidence that world modeling itself helps planning
13. strongest alternative explanation (representation pretraining, candidate set, rewarder/scorer, data scale)
14. exact relation to Epona, WoTE, DriveLaW and LAW
```

Required classification after deep read:

```text
training-only predictive shaping?
online predictive state?
joint world-action representation?
candidate consequence evaluation?
reward/value distillation?
hybrid of several interfaces?
```

## Stop condition for WorldDrive

Do not move to World4Drive until we can state, without ambiguity:

```text
observation → world model → transferred representation → planner → candidate set → FAR → selected trajectory
```

and identify which links are directly supervised, which are generated, which are frozen, and which survive at inference.

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
