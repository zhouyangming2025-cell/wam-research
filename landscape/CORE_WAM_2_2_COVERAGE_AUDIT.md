# CORE_WAM_2_2_COVERAGE_AUDIT

Last updated: 2026-09-15

Status: **CORE DEEP READS ACTIVE — WorldDrive / World4Drive / SeerDrive / Drive-JEPA / Metis COMPLETE; DynFlowDrive NEXT**

## Scope

Primary direction:

```text
WAM + one-stage / end-to-end autonomous driving planning
```

`WAM + VLA` is secondary/control until the core branch is stable.

Phase D problem discovery remains paused.

---

# Verified inventory and progress

| Work | Year | Code status | Current placement | Status |
|---|---:|---|---|---|
| **WorldDrive** | 2026 | official code + checkpoints; audited `TabGuigui/WorldDrive@c375ee1e...` | representation inheritance + **distilled future foresight** + future-aware rewarder | **COMPLETE — CORE ANCHOR** |
| **World4Drive** | 2025 ICCV | official code; audited `ucaszyp/World4Drive@cffb51ad...` | **online latent foresight**: intentions → trajectories → future latents → ScoreNet | **COMPLETE — CORE ANCHOR** |
| **SeerDrive** | 2025 NeurIPS | official repo audited; public release differs from original paper mechanism | **online bidirectional feature co-refinement**: future BEV ↔ planner hidden feature | **COMPLETE — CORE ANCHOR** |
| **Drive-JEPA** | 2026 | official NAVSIM-v1/v2 code audited at `linhanwang/Drive-JEPA@e21f474...` | **predictive representation pretraining → encoder transfer** + simulator-distilled proposal/scorer policy | **COMPLETE — BOUNDARY/CORE CONTROL ANCHOR** |
| **Metis** | 2026 | official repo audited; implementation still unreleased as of 2026-09-15 | **training-only asymmetric world-action co-training → action-only flow policy** | **COMPLETE — CORE/LIFECYCLE ANCHOR** |
| **DynFlowDrive** | 2026 | official repo/source status to be rechecked during audit | action-conditioned rectified-flow latent dynamics + stability-aware multi-mode selection | **NEXT** |
| **Discrete-WAM** | 2026 | official-code status needs current recheck | unified discrete vision-action world-policy learning | PENDING |
| **GraphWorld** | 2026 | official-code status needs current recheck | interaction graph + latent world state + long-horizon planning | PENDING |

Canonical Phase C.5 audits:

```text
audits/literature/PHASE_C5_WORLDDRIVE_AUDIT.md
audits/literature/PHASE_C5_WORLD4DRIVE_AUDIT.md
audits/literature/PHASE_C5_SEERDRIVE_AUDIT.md
audits/literature/PHASE_C5_DRIVEJEPA_AUDIT.md
audits/literature/PHASE_C5_METIS_AUDIT.md
```

Canonical normalized deep reads:

```text
papers/deep_analysis/P0042_WORLDDRIVE_DEEP_ANALYSIS_V2.md
papers/deep_analysis/P0046_WORLD4DRIVE_DEEP_ANALYSIS_V2.md
papers/deep_analysis/P0061_SEERDRIVE_DEEP_ANALYSIS_V2.md
papers/deep_analysis/P0049_DRIVEJEPA_DEEP_ANALYSIS_V2.md
papers/deep_analysis/P0062_METIS_DEEP_ANALYSIS_V2.md
```

---

# Current mechanism map

## WorldDrive — DISTILLED WORLD-MODEL FORESIGHT

```text
trajectory-aware generative WM pretraining
→ transfer/freeze vision + motion representations
→ multimodal candidate planner
→ frozen TA-DWM candidate-future latent as training teacher
→ lightweight distilled future representation
→ future-aware reward / trajectory selection at inference
```

Strongest attribution ladder:

```text
31.4 no pretrain
→ 84.9 generic CogVideoX VAE
→ 85.8 + TA-DWM vision
→ 86.9 + TA-DWM motion
→ 87.0 trajectory-feature rewarder
→ 88.1 + distilled future feature
```

---

## World4Drive — ONLINE LATENT FORESIGHT

```text
current physical latent
+ six intention queries
→ six trajectories
→ action tokens
→ six future latents
→ ScoreNet
→ select final trajectory
```

One factual future latent supervises mode assignment; multiple predicted branches are not multiple observed alternative-action truths.

Strongest component evidence:

```text
physical priors + intentions, no WM   0.61 L2 / 0.36 collision
physical priors + intentions + WM     0.50    / 0.16
```

---

## SeerDrive — ONLINE BIDIRECTIONAL FEATURE CO-REFINEMENT

```text
current BEV + ego/mode features
→ future BEV endpoint
→ future-aware planner
→ refined ego/planner feature
→ feed feature back into BEV WM
→ update future BEV
→ repeat internal refinement
```

Binding boundary:

```text
internal world↔planner refinement
!= physical-time rollout
!= environment execution-feedback closed loop
```

Strongest 2×2 evidence:

```text
future-aware OFF + iterative OFF  87.1
future-aware OFF + iterative ON   87.9
future-aware ON  + iterative OFF  88.1
future-aware ON  + iterative ON   88.9
```

---

## Drive-JEPA — PREDICTIVE REPRESENTATION PRETRAINING + SIMULATOR-DISTILLED PROPOSAL POLICY

Predictive side:

```text
V-JEPA random spatiotemporal mask completion
→ encoder + predictor + EMA target
→ driving-video adaptation
→ transfer encoder
→ predictor/target branch discarded
```

Deployment side:

```text
2 front frames + ego/status
→ 32 proposals
→ 4 proposal-refinement passes
→ learned PDM/EPDMS scorer
→ temporal comfort calibration
→ argmax
```

Key planning ladder:

```text
baseline             84.1 EPDMS / 25% diversity / 68.2 EC
driving pretrain     86.1       / 24%           / 69.7
+ MTD                84.5       / 40%           / 47.9
+ momentum selection 87.8       / 40%           / 84.8
```

Control strengthened:

```text
candidate diversity != planning quality
candidate support != candidate selection quality
```

---

## Metis — TRAINING-ONLY ASYMMETRIC WORLD-ACTION CO-TRAINING

Training:

```text
current observation → action expert → future action representation
                                      ↓
                               conditions VGE
                                      ↓
                           factual future video
                                      ↓ L_video
                         gradient shapes action expert
```

Asymmetric attention semantics:

```text
forward action→world              YES
forward future-world→action       NO
backward world-loss→action expert YES
```

Deployment:

```text
current observation + language + ego state
→ action expert flow denoising
→ trajectory
```

Explicit future-video generation at action deployment:

```text
NO
```

Strongest matched world-task evidence:

```text
w/o video co-training   87.9 EPDMS
w/  video co-training   89.5 EPDMS
```

Strongest interaction-topology evidence at matched 320×384:

```text
Joint       87.4 navtest / 28.0 navhard
Isolated    88.3         / 29.4
Asymmetric  88.8         / 31.6
```

This demonstrates that tighter/symmetric coupling is not automatically better and that `world→action gradient influence` is distinct from `world→action forward information flow`.

No dedicated quantitative future-video fidelity metric was identified; therefore:

```text
video co-training benefit
!=
world-fidelity→planning evidence
```

Official implementation remains unreleased as of 2026-09-15, so code-level details are source-unverified.

Historical control:

```text
Fast-WAM already explores world/video co-training with test-time future generation removed;
Metis's contribution is the specific MoT + asymmetric-attention mechanism, not the broad lifecycle idea alone.
```

---

# Active coordinate-system amendments

Base:

```text
landscape/WAM_DIMENSION_ONTOLOGY_V1.md
```

V1.1 from SeerDrive:

```text
J08  Inference iteration semantics
J09  Planner→world feedback carrier
L07  Iterative-state supervision coverage
```

V1.2 from Drive-JEPA:

```text
F07  Prediction temporal / observability geometry
```

Metis stress-test result:

```text
NO new dimension required.
Ontology V1.2 remains sufficient.
```

Its distinctive asymmetry is represented by:

```text
E01/E02  action→world forward coupling
J04      coupling direction
L04      gradient coupling direction
M01-M03  training→deployment lifecycle
```

---

# Updated future-knowledge lifecycle map

```text
LAW
auxiliary future latent during planner training
→ no future object online

Drive-JEPA
masked predictive pretraining
→ encoder transfer
→ predictor removed

Epona
joint visual/trajectory generative training
→ shared representation shaped
→ visual branch optional online

Metis
action-conditioned future-video co-training
→ world loss shapes action expert
→ explicit future branch bypassed online

WoTE
compact recurrent future transition
→ stays online
→ explicit utility selection

WorldDrive
heavy future teacher
→ distilled lightweight surrogate
→ stays online for ranking

World4Drive
candidate endpoint future
→ stays online
→ factual-mode selector

SeerDrive
future BEV endpoint online
↔ planner hidden feature co-refinement
```

---

# Binding comparison questions for remaining anchors

Every remaining paper must resolve:

```text
observation/history representation
current-state object
future/world target object
F07 prediction observability geometry
action/intention representation
action→world forward coupling
world→action forward coupling
world-loss→action gradient coupling
future target / truth lineage
training-stage topology
shared representation / parameters / gradients
what predictive/world machinery survives deployment
candidate/scorer/selector contribution
J08 iteration semantics
J09 feedback carrier
L07 iterative supervision where applicable
matched controls isolating world mechanism
prediction fidelity→planning evidence
evaluation regime / reactivity
source-version status
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
6. DynFlowDrive    NEXT
7. Discrete-WAM
8. GraphWorld
```

## Current decision

```text
Phase D problem discovery = PAUSED
Phase C.5 core-WAM correction = ACTIVE
broad WAM+VLA expansion = DEFERRED
```

Do not reopen Phase D until remaining core mechanisms are normalized and the WAM-only historical/interface synthesis passes comparability QA.
