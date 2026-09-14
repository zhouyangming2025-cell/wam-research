# CORE_WAM_2_2_COVERAGE_AUDIT

Last updated: 2026-09-14

Status: **FIRST-PASS IDENTITY / SCOPE / CODE VERIFICATION COMPLETE — DEEP READS NEXT**

## Scope correction

The current core direction is:

```text
WAM + one-stage / end-to-end autonomous driving planning
```

This is the primary research line. `WAM + VLA` is temporarily secondary and should be used mainly as a control/neighboring family, not as the organizing literature axis.

The following papers were present in the external 2.2 WAM list but were missing from the current Research Brain census/index. They are now treated as mandatory core-coverage candidates.

---

## First-pass verified inventory

| Work | Primary source | Year | Official/public code status | First-pass placement | Core priority |
|---|---|---:|---|---|---|
| **WorldDrive** — *Bridging Scene Generation and Planning: Driving with World Model via Unifying Vision and Motion Representation* | arXiv:2603.14948 | 2026 | **YES** — `TabGuigui/WorldDrive`; training/eval/checkpoints released | trajectory-aware driving WM + shared vision/motion representation + multimodal planner + future-aware rewarder | **A — mandatory deep read** |
| **World4Drive** — *End-to-End Autonomous Driving via Intention-aware Physical Latent World Model* | arXiv:2507.00603; ICCV 2025 | 2025 | **YES** — `ucaszyp/World4Drive` | latent WM for multimodal trajectory generation + intention-conditioned future latent + world-model selector | **A — mandatory deep read** |
| **SeerDrive** — *Future-Aware End-to-End Driving: Bidirectional Modeling of Trajectory Planning and Scene Evolution* | arXiv:2510.11092; NeurIPS 2025 | 2025 | **YES** — `LogosRoboticsGroup/SeerDrive` | future BEV modeling ↔ trajectory planning iterative/bidirectional coupling | **A — mandatory deep read** |
| **Drive-JEPA** — *Video JEPA Meets Multimodal Trajectory Distillation for End-to-End Driving* | arXiv:2601.22032 | 2026 | **YES** — `linhanwang/Drive-JEPA`; NAVSIM v1/v2 code + checkpoints | predictive video representation pretraining + proposal-centric multimodal planning/distillation | **A/B boundary — deep read because it tests whether predictive WM value is mainly representation learning** |
| **Metis** — *A Generalizable and Efficient World-Action Model for Autonomous Driving and Urban Navigation* | arXiv:2606.15869 | 2026 | **PUBLIC REPO, CODE NOT YET RELEASED** as of 2026-09-14 — `LogosRoboticsGroup/Metis` currently contains README/assets/license only | decoupled Video Generation Expert + Action Expert; asymmetric attention; joint world/action training, action-only inference | **A — mandatory deep read** |
| **DynFlowDrive** — *Flow-Based Dynamic World Modeling for Autonomous Driving* | arXiv:2603.19675 | 2026 | **REPO EXISTS, IMPLEMENTATION NOT YET RELEASED** — `xiaolul2/DynFlowDrive` | rectified-flow latent dynamics conditioned on driving action + stability-aware multimode trajectory selection | **A — mandatory deep read** |
| **Discrete-WAM** — *Unified Discrete Vision-Action Token Editing for World-Policy Learning* | arXiv:2606.05645 | 2026 | **NO OFFICIAL CODE FOUND IN FIRST-PASS SEARCH** | aligned discrete vision/action tokens + shared discrete diffusion + world/world-action/policy generative tasks | **A — mandatory deep read** |
| **GraphWorld** — *Long-Horizon Planning with World Models for End-to-End Autonomous Driving* | arXiv:2606.16274 | 2026 | **NO OFFICIAL CODE FOUND IN FIRST-PASS SEARCH**; do not confuse with unrelated `google-research/graphworld` | ego-centric interaction graph + latent world-state-conditioned long-horizon planning | **A — mandatory deep read** |

---

## Why these eight materially matter

These are not random missing papers. Collectively they cover several mechanisms not yet represented strongly enough in the current atlas:

```text
WorldDrive
  generation pretraining → planner-shared visual/motion encoders
  + future-aware rewarder

World4Drive
  intention-aware latent futures
  + multimodal trajectory generation
  + WM-based selection

SeerDrive
  future scene → planning
  + planned trajectory → future scene
  iterative bidirectional refinement

Drive-JEPA
  predictive video representation
  + multimodal trajectory distillation
  tests representation-vs-online-WM boundary

Metis
  joint world/action training
  but explicit future-video generation removed at inference
  efficiency / training-inference decoupling

DynFlowDrive
  action-conditioned stochastic/flow latent dynamics
  + stability-based trajectory selection

Discrete-WAM
  discrete compositional vision-action world-policy space
  potential alternative to continuous latent WAMs

GraphWorld
  interaction graph + latent world state
  explicitly targets long-horizon planning
```

They directly pressure-test the current Phase-C seven-interface taxonomy and may require revisions.

---

## Immediate scientific questions for deep reading

For every paper, do not stop at the abstract. Trace:

```text
1. exact observation input and numerical representation
2. exact world/predictive state
3. exact action / trajectory representation
4. what is directly supervised
5. whether future supervision exists only for executed action or alternatives
6. exact training-time world↔action coupling
7. exact inference-time world→planning path
8. whether generated/predicted future is consumed online or only shapes representation
9. candidate generation / scorer / selector contribution
10. matched ablations isolating world-model contribution
11. NAVSIM / nuScenes / Bench2Drive protocol semantics
12. latency / candidate count / horizon / deployment branch
13. strongest evidence for the paper
14. strongest competing explanation
15. relation to Epona / WoTE / LAW / DriveLaW / Auto-JEPA / DA-WAM
```

---

## Provisional reading order

```text
1. WorldDrive
2. World4Drive
3. SeerDrive
4. Drive-JEPA
5. Metis
6. DynFlowDrive
7. Discrete-WAM
8. GraphWorld
```

Rationale:

- `WorldDrive` directly connects several already-audited anchors (Epona/WoTE-style future modeling, representation transfer, rewarder) and is likely the highest-value bridge paper.
- `World4Drive` and `SeerDrive` are 2025 core predecessors that may change the historical narrative before reading 2026 successors.
- `Drive-JEPA` tests whether WAM benefit is predictive representation + action modeling rather than explicit online simulation.
- `Metis` explicitly attacks inference-time world-generation necessity.
- `DynFlowDrive`, `Discrete-WAM`, and `GraphWorld` represent newer 2026 directions: flow dynamics, discrete world-action tokens, and long-horizon graph-world planning.

---

## Current decision

```text
Phase D problem discovery = PAUSED
Phase C.5 core-WAM coverage correction = ACTIVE
WAM+VLA broadening = DEFERRED
```

Do not reopen formal gap selection until these eight papers are placed and the WAM-only synthesis is updated.
