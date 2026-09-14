# CORE_WAM_2_2_COVERAGE_AUDIT

Last updated: 2026-09-14

Status: **CORE DEEP READS ACTIVE — WorldDrive + World4Drive COMPLETE**

## Scope

Primary direction:

```text
WAM + one-stage / end-to-end autonomous driving planning
```

`WAM + VLA` is secondary/control until the core branch is stable.

---

## Verified inventory and progress

| Work | Year | Code status | Current placement | Status |
|---|---:|---|---|---|
| **WorldDrive** | 2026 | official code + checkpoints; audited `TabGuigui/WorldDrive@c375ee1e...` | TA-DWM representation inheritance + **distilled future foresight** + future-aware candidate rewarder | **COMPLETE — KEEP CORE ANCHOR** |
| **World4Drive** | 2025 ICCV | official code; audited `ucaszyp/World4Drive@cffb51ad...` | **online latent foresight**: 6 intention trajectories → 6 future latents → ScoreNet → select | **COMPLETE — KEEP CORE ANCHOR** |
| **SeerDrive** | 2025 NeurIPS | official code `LogosRoboticsGroup/SeerDrive` | future BEV ↔ trajectory planning iterative/bidirectional coupling | **NEXT** |
| **Drive-JEPA** | 2026 | official code `linhanwang/Drive-JEPA` | predictive video representation + multimodal trajectory distillation | PENDING |
| **Metis** | 2026 | public repo; source code not released as of 2026-09-14 | joint world/action training, action-only inference | PENDING |
| **DynFlowDrive** | 2026 | repo exists; implementation unreleased | action-conditioned rectified-flow latent dynamics + stability selection | PENDING |
| **Discrete-WAM** | 2026 | no official code found first pass | unified discrete vision-action world-policy learning | PENDING |
| **GraphWorld** | 2026 | no official code found first pass | interaction graph + latent world state + long-horizon planning | PENDING |

Canonical audits:

```text
audits/literature/PHASE_C5_WORLDDRIVE_AUDIT.md
audits/literature/PHASE_C5_WORLD4DRIVE_AUDIT.md
```

---

## Core mechanism map after first two deep reads

### WorldDrive — DISTILLED WORLD-MODEL FORESIGHT

```text
trajectory-aware generative WM pretraining
→ transfer/freeze vision + motion representations
→ multimodal candidate planner
→ frozen TA-DWM candidate-future latent as training teacher
→ lightweight distilled future representation
→ future-aware reward / trajectory selection at inference
```

Important deployment fact:

```text
full TA-DiT diffusion rollout at planner inference = NO
```

Strongest matched evidence:

```text
31.4 no pretrain
→ 84.9 generic CogVideoX VAE
→ 85.8 + TA-DWM vision
→ 86.9 + TA-DWM motion

86.9 base planner
→ 87.0 trajectory-feature rewarder
→ 88.1 + distilled future feature
```

### World4Drive — ONLINE LATENT FORESIGHT

```text
current physical world latent
+ six intention queries
→ six ego trajectories
→ action tokens
→ six intention-conditioned future world latents
→ ScoreNet over predicted future latents
→ select final trajectory
```

Training supervision uses one factual future latent to choose the closest predicted future mode and train the selector. Thus:

```text
K action-conditioned future outputs
!=
K real alternative-action future labels
```

Strongest component evidence:

```text
physical priors + intentions, no WM   0.61 L2 / 0.36 collision
physical priors + intentions + WM     0.50    / 0.16
```

This supports the full latent-WM selector beyond multimodal intentions alone.

---

## New comparison axis introduced

WorldDrive and World4Drive make a useful distinction:

```text
DISTILLED FORESIGHT
heavy/full WM future used as teacher; lightweight future surrogate at deployment

vs

ONLINE LATENT FORESIGHT
compact action-conditioned future predictor itself remains in the deployment path
```

Both differ from:

```text
LAW        training-only future-latent shaping
DriveLaW   online WM hidden state → direct action generator
WoTE       candidate → future BEV rollout → learned reward
DA-WAM     candidate → future latent → factor/ranking scorer
```

This axis should be preserved in the final WAM-only synthesis.

---

## Reading order

```text
1. WorldDrive      COMPLETE
2. World4Drive     COMPLETE
3. SeerDrive       NEXT
4. Drive-JEPA
5. Metis
6. DynFlowDrive
7. Discrete-WAM
8. GraphWorld
```

## Binding deep-read questions for remaining papers

Trace exactly:

```text
observation/history representation
world/predictive state
candidate/action representation
future supervision source
training-time world↔action coupling
inference-time world→planning path
whether future branch remains online
candidate/scorer/selector contribution
matched ablations isolating WM contribution
evaluation semantics + latency/horizon
strongest evidence + strongest competing explanation
```

## Current decision

```text
Phase D problem discovery = PAUSED
Phase C.5 core-WAM correction = ACTIVE
broad WAM+VLA expansion = DEFERRED
```

Do not reopen Phase D until all decision-relevant 2.2 mechanisms are placed and a WAM-only historical/interface synthesis is stable.
