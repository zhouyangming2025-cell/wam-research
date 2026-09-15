# CORE_WAM_2_2_COVERAGE_AUDIT

Last updated: 2026-09-15

Status: **CORE DEEP READS ACTIVE — WorldDrive / World4Drive / SeerDrive / Drive-JEPA COMPLETE; Metis NEXT**

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
| **SeerDrive** | 2025 NeurIPS | official repo audited; public release is a WoTE-integrated variant distinct from original paper mechanism | **online bidirectional feature co-refinement**: future BEV ↔ planner hidden feature | **COMPLETE — CORE ANCHOR** |
| **Drive-JEPA** | 2026 | official NAVSIM-v1/v2 code audited at `linhanwang/Drive-JEPA@e21f474...` | **predictive representation pretraining → encoder transfer** + simulator-distilled proposal/scorer policy | **COMPLETE — BOUNDARY/CORE CONTROL ANCHOR** |
| **Metis** | 2026 | public repo; source-code availability must be rechecked during audit | joint world/action training, reported action-only inference | **NEXT** |
| **DynFlowDrive** | 2026 | repo exists; implementation status must be rechecked | action-conditioned rectified-flow latent dynamics + stability selection | PENDING |
| **Discrete-WAM** | 2026 | official-code status needs current recheck | unified discrete vision-action world-policy learning | PENDING |
| **GraphWorld** | 2026 | official-code status needs current recheck | interaction graph + latent world state + long-horizon planning | PENDING |

Canonical Phase C.5 audits:

```text
audits/literature/PHASE_C5_WORLDDRIVE_AUDIT.md
audits/literature/PHASE_C5_WORLD4DRIVE_AUDIT.md
audits/literature/PHASE_C5_SEERDRIVE_AUDIT.md
audits/literature/PHASE_C5_DRIVEJEPA_AUDIT.md
```

Canonical normalized deep reads:

```text
papers/deep_analysis/P0042_WORLDDRIVE_DEEP_ANALYSIS_V2.md
papers/deep_analysis/P0046_WORLD4DRIVE_DEEP_ANALYSIS_V2.md
papers/deep_analysis/P0061_SEERDRIVE_DEEP_ANALYSIS_V2.md
papers/deep_analysis/P0049_DRIVEJEPA_DEEP_ANALYSIS_V2.md
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

Important deployment fact:

```text
full TA-DiT diffusion rollout at planner inference = NO
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
current physical world latent
+ six intention queries
→ six ego trajectories
→ action tokens
→ six intention-conditioned future world latents
→ ScoreNet
→ select final trajectory
```

Training sees one factual future latent; multiple predicted branches are not multiple observed alternative-action truths.

Strongest component evidence:

```text
physical priors + intentions, no WM   0.61 L2 / 0.36 collision
physical priors + intentions + WM     0.50    / 0.16
```

---

## SeerDrive — ONLINE BIDIRECTIONAL FEATURE CO-REFINEMENT

Original paper:

```text
current BEV + ego/mode features
→ future BEV endpoint
→ future-aware planner
→ refined ego/planner feature
→ feed feature back into BEV world model
→ updated future BEV
→ repeat internal refinement
```

Important semantic boundary:

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

Paper predicts the final-horizon future BEV by default; richer intermediate future-BEV sequences do not improve PDMS materially.

Public source/README is a later WoTE-integrated variant and must not be silently merged with the original paper graph.

---

## Drive-JEPA — PREDICTIVE REPRESENTATION PRETRAINING + SIMULATOR-DISTILLED PROPOSAL POLICY

Predictive side:

```text
V-JEPA random spatiotemporal mask completion
→ online encoder + predictor
→ EMA/stop-gradient latent target
→ driving-domain video adaptation
→ transfer visual encoder into planner
→ discard JEPA predictor / target branch
```

Deployment side:

```text
2 front frames + ego/status
→ transferred visual representation
→ 32 proposals
→ 4 shared-weight proposal-refinement passes
→ learned PDM/EPDMS utility scorer
→ NAVSIM-v2 two-frame comfort calibration
→ argmax
```

MTD:

```text
8192 offline trajectory vocabulary
→ NAVSIM simulator/rule quality evaluation
→ high-quality pseudo teachers
→ multimodal proposal supervision
```

Key evidence:

```text
simple decoder:
V-JEPA2             86.1 PDMS
Drive-domain JEPA   89.0

full NAVSIM-v2 ladder:
baseline                       84.1 EPDMS / 25% D / 68.2 EC
driving pretrain               86.1       / 24%   / 69.7
+ MTD                          84.5       / 40%   / 47.9
+ momentum selection           87.8       / 40%   / 84.8
```

This demonstrates:

```text
predictive representation can help without online future rollout;
candidate diversity can hurt until selection quality catches up.
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

F07 prevents collapsing:

```text
random-mask same-window completion
past/history-only → unseen future
current → future endpoint
recurrent next-state rollout
hybrid future masking
```

into one generic `predictive` label.

---

# Updated interface / lifecycle map

```text
LAW
training-time action-aware future-latent shaping
→ future output absent from deployed action selection

Drive-JEPA
separate masked-video predictive pretraining
→ predictor discarded
→ encoder transferred

Epona
joint visual/trajectory predictive training
→ shared history representation
→ visual future optional for planning

WoTE
compact learned recurrent future transition
→ stays online
→ explicit utility selection

WorldDrive
heavy generative future teacher
→ distilled lightweight surrogate online
→ preference/ranking

World4Drive
compact candidate future endpoint predictor
→ stays online
→ factual-mode selector

SeerDrive
compact future BEV endpoint online
↔ planner hidden feature internal co-refinement
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
action→world conditioning
world→planning interface
future target / truth lineage
target encoder / stop-gradient / teacher semantics
training-stage topology
shared representation / parameters / gradients
what predictive/world machinery survives deployment
candidate/scorer contribution
J08 iteration semantics
J09 feedback carrier when applicable
L07 iterative supervision when applicable
matched controls isolating world/predictive contribution
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
5. Metis           NEXT
6. DynFlowDrive
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
