# CORE_WAM_2_2_COVERAGE_AUDIT

Last updated: 2026-09-15

Status: **CORE DEEP READS ACTIVE — WorldDrive / World4Drive / SeerDrive / Drive-JEPA / Metis / DynFlowDrive COMPLETE; Discrete-WAM NEXT**

## Scope

Primary direction:

```text
WAM + one-stage / end-to-end autonomous driving planning
```

`WAM + VLA` remains secondary/control until the core branch is stable.

Phase D problem discovery remains **PAUSED**.

---

# Verified inventory and progress

| Work | Year | Code status | Current placement | Status |
|---|---:|---|---|---|
| **WorldDrive** | 2026 | official code + checkpoints; audited `TabGuigui/WorldDrive@c375ee1e...` | representation inheritance + distilled future foresight + future-aware rewarder | **COMPLETE — CORE ANCHOR** |
| **World4Drive** | 2025 ICCV | official code audited | online latent foresight: intentions → trajectories → future latents → ScoreNet | **COMPLETE — CORE ANCHOR** |
| **SeerDrive** | 2025 NeurIPS | official repo audited; public release differs from original paper mechanism | online bidirectional feature co-refinement | **COMPLETE — CORE ANCHOR** |
| **Drive-JEPA** | 2026 | official NAVSIM-v1/v2 code audited | predictive representation pretraining → encoder transfer + simulator-distilled proposal/scorer policy | **COMPLETE — BOUNDARY/CORE CONTROL ANCHOR** |
| **Metis** | 2026 | official repo audited; implementation unreleased as of 2026-09-15 | training-only asymmetric world-action co-training → action-only flow policy | **COMPLETE — CORE/LIFECYCLE ANCHOR** |
| **DynFlowDrive** | 2026 | official repo audited; implementation unreleased as of 2026-09-15 | training-only trajectory-conditioned flow WM → world-derived score supervision → model-free deployment | **COMPLETE — CORE/LIFECYCLE ANCHOR** |
| **Discrete-WAM** | 2026 | official-code status to be rechecked | unified discrete vision-action world-policy learning | **NEXT** |
| **GraphWorld** | 2026 | official-code status needs current recheck | interaction graph + latent world state + long-horizon planning | PENDING |

Canonical Phase C.5 audits:

```text
audits/literature/PHASE_C5_WORLDDRIVE_AUDIT.md
audits/literature/PHASE_C5_WORLD4DRIVE_AUDIT.md
audits/literature/PHASE_C5_SEERDRIVE_AUDIT.md
audits/literature/PHASE_C5_DRIVEJEPA_AUDIT.md
audits/literature/PHASE_C5_METIS_AUDIT.md
audits/literature/PHASE_C5_DYNFLOWDRIVE_AUDIT.md
```

Canonical normalized deep reads:

```text
papers/deep_analysis/P0042_WORLDDRIVE_DEEP_ANALYSIS_V2.md
papers/deep_analysis/P0046_WORLD4DRIVE_DEEP_ANALYSIS_V2.md
papers/deep_analysis/P0061_SEERDRIVE_DEEP_ANALYSIS_V2.md
papers/deep_analysis/P0049_DRIVEJEPA_DEEP_ANALYSIS_V2.md
papers/deep_analysis/P0062_METIS_DEEP_ANALYSIS_V2.md
papers/deep_analysis/P0063_DYNFLOWDRIVE_DEEP_ANALYSIS_V2.md
```

---

# Current mechanism map

## WorldDrive — DISTILLED WORLD-MODEL FORESIGHT

```text
trajectory-aware generative WM pretraining
→ transfer/freeze visual + motion representations
→ multimodal candidate planner
→ heavy future teacher
→ distilled lightweight future representation
→ online future-aware ranking
```

## World4Drive — ONLINE LATENT FORESIGHT

```text
current physical latent + intentions
→ candidate trajectories
→ candidate action tokens
→ endpoint future latents
→ factual-mode ScoreNet
→ online selection
```

One factual future latent supervises branch identity; candidate-specific outputs are not candidate-specific observed counterfactual truths.

## SeerDrive — ONLINE BIDIRECTIONAL FEATURE CO-REFINEMENT

```text
current state + mode
→ future BEV endpoint
→ planner refinement
→ planner hidden feature feeds back to WM
→ updated future BEV
→ repeated same-decision co-refinement
```

```text
internal refinement != physical rollout != executed-environment closed loop
```

## Drive-JEPA — PREDICTIVE REPRESENTATION PRETRAINING + PROPOSAL POLICY

```text
random-mask V-JEPA video pretraining
→ encoder transfer
→ predictor removed

32 proposals
→ repeated refinement
→ simulator/pseudo-teacher supervision
→ utility scorer + temporal calibration
→ argmax
```

## Metis — TRAINING-ONLY ASYMMETRIC WORLD-ACTION CO-TRAINING

```text
training forward: action→future-video branch
training backward: future-video loss→action expert
inference: current context→action only
```

```text
world→action gradient influence != world→action forward information flow
```

## DynFlowDrive — TRAINING-ONLY FLOW-DYNAMICS MODE-SUPERVISION

Training:

```text
multimodal planner
→ candidate trajectories

current factual world latent + candidate trajectory
→ rectified-flow latent dynamics
→ reconstruction + flow objectives
→ transport-direction stability

GT trajectory error + reconstruction + stability
→ positive mode n*
→ planner score-head supervision
```

Deployment:

```text
current observation
→ candidates + learned scores
→ argmax

world model / flow / future latent = REMOVED
```

Critical boundary:

```text
N candidate-conditioned flow outputs
vs
ONE factual next-world latent target
```

Thus action-conditioned branching is not intervention-valid counterfactual supervision.

---

# DynFlowDrive evidence decomposition

Strongest matched dynamics control:

```text
Static WM   0.61 Avg L2 / 0.30 Avg CR
Flow WM     0.59        / 0.26
```

World-feature prior:

```text
Flow WM                    0.59 / 0.26
+ pretrained World Feature 0.57 / 0.22
```

Selection teacher:

```text
none              0.61 / 0.30
L2 only           0.59 / 0.24
+ reconstruction  0.58 / 0.22
+ flow stability  0.57 / 0.22
```

This shows that the final performance is a bundle of:

```text
predictive/world supervision
+ flow parameterization
+ imported/foundation representation
+ positive-mode assignment / score distillation
```

The angular flow-stability term itself is a modest incremental contributor in the reported ablation.

---

# DynFlowDrive temporal correction and Ontology V1.3

DynFlowDrive forces separation of:

```text
physical scene time τ
rectified-flow transport coordinate s
planner/query iteration k
```

Only physical endpoints are directly observed as world targets. Intermediate `s` states are not physically time-supervised.

New stable dimension:

```text
F08  Internal transition-coordinate / physical-time alignment
```

Binding rule:

```text
K flow/diffusion steps != K physical future timesteps
smooth latent transport != validated smooth physical evolution
dz/ds != dz/dτ unless time identity is established
```

Back-projection distinguishes:

```text
WoTE       physically indexed predicted future transitions
Epona      outer physical frame time + inner denoising time
WorldDrive physical future + diffusion sampling time
SeerDrive  internal representation refinement
Metis      generative flow/denoising coordinate vs physical action/video horizon
DynFlowDrive rectified-flow transport coordinate between t and t+1
```

Canonical amendment:

```text
landscape/WAM_DIMENSION_ONTOLOGY_V1_3_AMENDMENT.md
```

---

# DynFlowDrive source/equation boundary

Official repository:

```text
xiaolul2/DynFlowDrive
latest observed public commit:
c665dc577a0939543fa7abe64d28eadaec28283c
```

Implementation remains unreleased.

Paper v2 contains unresolved mathematical/procedure ambiguities:

```text
Eq.7 x_s=(1-s)a+s z_{t+1}
vs Eq.10 target (1-s)(z_{t+1}-a)

training path built from noised anchor a
vs sampling prose starting from z_t
```

These remain source-audit questions rather than silently corrected implementation facts.

---

# Evaluation regime correction

DynFlowDrive paper calls NAVSIM `closed-loop`.

Project-standard label:

```text
NAVSIM v1 = NON-REACTIVE DATA-DRIVEN / PSEUDO-SIMULATION PLANNING
```

Therefore 88.7 PDMS is planning evidence under NAVSIM, not proof of reactive alternative-agent dynamics.

Headline SSR delta also contains an input confound:

```text
SSR*                            0.39 / 0.15
DynFlowDrive(SSR)               0.35 / 0.14
DynFlowDrive(SSR)+ego status    0.31 / 0.11
```

The more matched dynamics comparison is the 0.39→0.35 row, not the full 0.39→0.31 headline.

---

# Active coordinate-system amendments

```text
V1 base

V1.1 — SeerDrive
J08  Inference iteration semantics
J09  Planner→world feedback carrier
L07  Iterative-state supervision coverage

V1.2 — Drive-JEPA
F07  Prediction temporal / observability geometry

V1.3 — DynFlowDrive
F08  Internal transition-coordinate / physical-time alignment
```

Metis did not require a new axis; its asymmetric forward/backward coupling is already represented by E/J/L/M.

---

# Updated future-knowledge lifecycle map

```text
LAW
training future target → representation shaping → no future online

Drive-JEPA
predictive pretraining → encoder transfer → no predictor online

Metis
future-video co-training → world-loss-shaped action expert → no future online

DynFlowDrive
candidate consequence teacher → score/mode supervision → no future online

Epona
joint visual/trajectory training → shared representation → visual future optional online

WorldDrive
heavy future teacher → distilled future summary → lightweight future online

World4Drive
candidate endpoint future → future-mode scorer → online future

WoTE
candidate recurrent future → utility → online future

SeerDrive
future endpoint ↔ planner hidden state → online co-refinement
```

---

# Binding comparison questions for remaining anchors

Every remaining paper must resolve:

```text
observation/history representation
current-state object and representation provenance
future/world target object
F07 prediction observability geometry
F08 internal-step / physical-time semantics
action/intention representation
action→world and world→action forward coupling
world-loss→action gradient coupling
future target / truth lineage
counterfactual vector I01–I05
training-stage topology
representation / parameter / loss sharing
what world machinery survives deployment
candidate/scorer/selector contribution
J08 iteration semantics
J09 feedback carrier
L07 iterative-state supervision when relevant
matched world-mechanism control
prediction fidelity→planning evidence
evaluation regime / reactivity
source/version status
proves / does-not-prove / strongest alternative explanation
```

---

# Reading order

```text
1. WorldDrive      COMPLETE
2. World4Drive     COMPLETE
3. SeerDrive       COMPLETE
4. Drive-JEPA      COMPLETE
5. Metis           COMPLETE
6. DynFlowDrive    COMPLETE
7. Discrete-WAM    NEXT
8. GraphWorld      PENDING
```

## Current decision

```text
Phase D problem discovery = PAUSED
Phase C.5 core-WAM correction = ACTIVE
broad WAM+VLA expansion = DEFERRED
```

Do not reopen Phase D until Discrete-WAM and GraphWorld are normalized and WAM-only comparability QA is rerun.
