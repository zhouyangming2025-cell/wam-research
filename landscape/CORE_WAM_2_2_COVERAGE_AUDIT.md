# CORE_WAM_2_2_COVERAGE_AUDIT

Last updated: 2026-09-15

Status: **CORE DEEP READS ACTIVE — through Discrete-WAM COMPLETE; GraphWorld NEXT**

## Scope

Primary direction:

```text
WAM + one-stage / end-to-end autonomous driving planning
```

`WAM + VLA` remains secondary/control until the core branch is stable.

Phase D problem discovery remains **PAUSED**.

---

# Verified inventory and progress

| Work | Year | Code/source status | Current placement | Status |
|---|---:|---|---|---|
| **WorldDrive** | 2026 | official code + checkpoints audited | representation inheritance + distilled future foresight + future-aware rewarder | **COMPLETE — CORE ANCHOR** |
| **World4Drive** | 2025 ICCV | official code audited | online latent foresight: intentions → trajectories → future latents → ScoreNet | **COMPLETE — CORE ANCHOR** |
| **SeerDrive** | 2025 NeurIPS | official repo audited; released code differs from original paper mechanism | online bidirectional feature co-refinement | **COMPLETE — CORE ANCHOR** |
| **Drive-JEPA** | 2026 | official NAVSIM-v1/v2 code audited | predictive representation pretraining → encoder transfer + simulator-distilled proposal/scorer | **COMPLETE — BOUNDARY/CORE CONTROL** |
| **Metis** | 2026 | official repo audited; implementation unreleased as of 2026-09-15 | asymmetric world-action co-training → action-only policy | **COMPLETE — CORE/LIFECYCLE** |
| **DynFlowDrive** | 2026 | official repo `xiaolul2/DynFlowDrive`; implementation unreleased | training-only trajectory-conditioned flow WM → score supervision → model-free deployment | **COMPLETE — CORE/LIFECYCLE** |
| **Discrete-WAM** | 2026 | arXiv v2 audited; official implementation repo not identified | shared-backbone discrete world/policy pretraining → decision/action token policy → no mandatory future world online | **COMPLETE — CORE/DISCRETE-WAM** |
| **GraphWorld** | 2026 | official-code status requires current audit | interaction graph + latent world state + long-horizon planning | **NEXT** |

Canonical Phase C.5 audits:

```text
audits/literature/PHASE_C5_WORLDDRIVE_AUDIT.md
audits/literature/PHASE_C5_WORLD4DRIVE_AUDIT.md
audits/literature/PHASE_C5_SEERDRIVE_AUDIT.md
audits/literature/PHASE_C5_DRIVEJEPA_AUDIT.md
audits/literature/PHASE_C5_METIS_AUDIT.md
audits/literature/PHASE_C5_DYNFLOWDRIVE_AUDIT.md
audits/literature/PHASE_C5_DISCRETE_WAM_AUDIT.md
```

Canonical normalized deep reads:

```text
papers/deep_analysis/P0042_WORLDDRIVE_DEEP_ANALYSIS_V2.md
papers/deep_analysis/P0046_WORLD4DRIVE_DEEP_ANALYSIS_V2.md
papers/deep_analysis/P0061_SEERDRIVE_DEEP_ANALYSIS_V2.md
papers/deep_analysis/P0049_DRIVEJEPA_DEEP_ANALYSIS_V2.md
papers/deep_analysis/P0062_METIS_DEEP_ANALYSIS_V2.md
papers/deep_analysis/P0063_DYNFLOWDRIVE_DEEP_ANALYSIS_V2.md
papers/deep_analysis/P0064_DISCRETE_WAM_DEEP_ANALYSIS_V2.md
```

---

# Current mechanism map

## WorldDrive — DISTILLED WORLD-MODEL FORESIGHT

```text
generative WM pretraining / representation inheritance
→ multimodal planner
→ heavy candidate-conditioned future teacher
→ distilled lightweight future representation
→ online future-aware ranking
```

## World4Drive — ONLINE LATENT FORESIGHT

```text
current latent + intentions
→ candidate trajectories
→ candidate action tokens
→ endpoint future latents
→ factual-mode ScoreNet
→ online selection
```

One factual future supervises mode identity; K outputs are not K observed counterfactual truths.

## SeerDrive — ONLINE BIDIRECTIONAL FEATURE CO-REFINEMENT

```text
current state + mode
→ future BEV endpoint
→ planner refinement
→ planner hidden feature feeds back to WM
→ repeated same-decision co-refinement
```

```text
internal refinement != physical rollout != executed-environment loop
```

## Drive-JEPA — PREDICTIVE REPRESENTATION PRETRAINING + PROPOSAL POLICY

```text
random-mask V-JEPA video pretraining
→ encoder transfer
→ predictor removed

32 proposals
→ refinement
→ simulator/pseudo-teacher targets
→ utility scorer + temporal calibration
→ argmax
```

## Metis — TRAINING-ONLY ASYMMETRIC WORLD-ACTION CO-TRAINING

```text
forward training: action → future-video branch
backward training: video loss → action expert
inference: current context → action only
```

## DynFlowDrive — TRAINING-ONLY FLOW-DYNAMICS MODE-SUPERVISION

```text
candidate + current world latent
→ rectified-flow WM
→ reconstruction / flow / stability teacher signals
→ positive mode / score-head supervision

DEPLOYMENT:
candidates + learned scores → argmax
world model removed
```

## Discrete-WAM — SHARED-BACKBONE DISCRETE WORLD-POLICY PRETRAINING

Training/capability:

```text
separate visual VQ vocabulary
+
separate acceleration-token vocabulary
→ common decoder-only Transformer
→ world / policy / interleaved world-policy tasks
```

Primary planning:

```text
current context
→ high-level decision token
→ parallel/iterative action-token editing
→ trajectory

future visual-token generation = optional / not required
```

Critical correction:

```text
shared discrete framework != shared codebook
joint training != online world imagination
```

---

# Active ontology amendments

```text
V1.1 — SeerDrive
J08  Inference iteration semantics
J09  Planner→world feedback carrier
L07  Iterative-state supervision coverage

V1.2 — Drive-JEPA
F07  Prediction temporal / observability geometry

V1.3 — DynFlowDrive
F08  Internal transition-coordinate / physical-time alignment
```

Discrete-WAM did **not** authorize V1.4.

Residue watchlist:

```text
Discrete representation alignment topology:
shared codebook
vs separate modality vocabularies
vs common hidden/sequence interface
```

Reason for deferral: the current prior anchor set is mostly continuous-latent, so back-projection provides insufficient cross-paper discrimination. Re-test when another discrete-token anchor is normalized.

---

# Ten-anchor future-knowledge lifecycle map

```text
LAW
future target → representation shaping → no future online

Drive-JEPA
predictive pretraining → encoder transfer → no predictor online

Metis
future-video co-training → world-loss-shaped policy → no future online

DynFlowDrive
candidate flow consequence teacher → score/mode teaching → no future online

Discrete-WAM
shared world/policy token pretraining → policy weights/hidden state → no future visual required online

Epona
joint visual/trajectory training → shared representation → visual future optional online

WorldDrive
heavy future teacher → distilled future summary → lightweight future online

World4Drive
candidate endpoint future → factual-mode scorer → future online

WoTE
candidate recurrent future → explicit utility → future online

SeerDrive
future BEV ↔ planner hidden state → online co-refinement
```

Stable synthesis:

```text
training-time unification strength
and
deployment-time model-basedness
are orthogonal axes
```

---

# Discrete-WAM evidence decomposition

World/pretraining strategy:

```text
From scratch   89.8 EPDMS
FT             89.7
LoRA-SFT       90.0
```

The LoRA-SFT row uses vision-oriented pretraining with teacher-forced actions and vision loss before LoRA policy SFT; it is not a clean full-joint world+action pretraining ablation.

Decision modeling:

```text
Base       84.7
Base-D_t   87.2
```

Post-training:

```text
SFT       89.1
SFT-D_t   90.0
RL        90.4
```

Therefore final planning performance is a bundle of:

```text
world/vision-oriented pretraining
+ high-level decision prior
+ action discretization
+ token editing
+ LoRA adaptation
+ RL/post-training
+ shared model capacity
```

World generation is independently strong (reported FID ≈6.6, FVD ≈80.0), but no clean matched fidelity→planning causal relation is shown.

---

# Stable controls retained / strengthened

```text
action-conditioned != WM-based action selection
candidate-specific output != candidate-specific alternative-future truth
joint modeling != shared representation != shared parameters != shared gradients != online bidirectional feedback
shared discrete framework != shared codebook
training unification != deployment world dependence
world-generation capability != world-generation-required planning
future→score != necessarily value/utility
foundation-prior gain != WM-specific dynamics gain
prediction fidelity != decision relevance
token-edit / diffusion / flow step != physical future timestep
NAVSIM non-reactive != reactive closed loop
matched controls > headline SOTA
```

---

# Evaluation regime discipline

For all applicable anchors:

```text
NAVSIM v1/v2
= NON-REACTIVE DATA-DRIVEN / PSEUDO-SIMULATION PLANNING
```

Bench2Drive/CARLA reactive evaluation, when present, must be labeled separately and must not be back-projected into training-supervision semantics.

---

# Reading order / remaining Phase C.5 queue

```text
WorldDrive       COMPLETE
World4Drive      COMPLETE
SeerDrive        COMPLETE
Drive-JEPA       COMPLETE
Metis            COMPLETE
DynFlowDrive     COMPLETE
Discrete-WAM     COMPLETE
GraphWorld       NEXT
```

## Current decision

```text
Phase D problem discovery = PAUSED
Phase C.5 core-WAM correction = ACTIVE
broad WAM+VLA expansion = DEFERRED
```

Do not reopen Phase D until GraphWorld is normalized and a WAM-only comparability QA / design-space consolidation is completed.
