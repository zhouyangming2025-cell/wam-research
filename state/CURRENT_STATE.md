# CURRENT_STATE

Last updated: **2026-09-15 — Drive-JEPA stress test COMPLETE; Ontology V1.2 ACTIVE; Metis NEXT**

## Research north star

```text
WAM / World Model + one-stage End-to-End + Planning-centric autonomous driving
```

Core 2.2 WAM is primary. WAM+VLA remains secondary/control. Risk/predictive-risk is optional prior knowledge, not a required destination.

## Methodology in force

```text
FIELD UNDERSTANDING FIRST
→ complete core-WAM coverage
→ comparative anchor deep reads
→ dimension-first normalization
→ evidence QA
→ only then adversarial problem discovery
→ falsification
→ method design
```

Phase D remains **PAUSED**.

## Canonical reading method

```text
paper-deep-reader
→ mechanism / formula / figure reconstruction

academic-research-agent source/claim gate
→ source/version discipline + claim/evidence separation

literature-reading-and-synthesis
→ claim-evidence extraction + immediate cross-paper comparison

WAM Ontology
→ full projection + residue/back-projection gate
```

Authority:

```text
landscape/WAM_READING_SKILL_STACK.md
```

## Dimension-first normalization status

```text
P0048 LAW          COMPLETE v2
P0045 WoTE         COMPLETE v2
P0001 Epona        COMPLETE v2
P0042 WorldDrive   COMPLETE v2
P0046 World4Drive  COMPLETE v2
P0061 SeerDrive    COMPLETE v2 first pass
P0049 Drive-JEPA   COMPLETE v2 first pass + official-source audit + full ontology projection
```

Canonical coordinate system:

```text
landscape/WAM_DIMENSION_ONTOLOGY_V1.md
landscape/WAM_DIMENSION_ONTOLOGY_V1_1_AMENDMENT.md
landscape/WAM_DIMENSION_ONTOLOGY_V1_2_AMENDMENT.md

landscape/WAM_COMPARISON_MATRIX_V1.md
landscape/WAM_COMPARISON_MATRIX_V1_1_SEERDRIVE_EXTENSION.md
landscape/WAM_COMPARISON_MATRIX_V1_2_DRIVEJEPA_EXTENSION.md
```

Full new projection:

```text
landscape/P0049_DRIVEJEPA_ONTOLOGY_PROJECTION.md
```

---

# Drive-JEPA stable result

## Predictive-pretraining mechanism

Drive-JEPA's V-JEPA objective is:

```text
video clip
→ random spatiotemporal masking
→ online ViT encoder
→ JEPA predictor
→ masked latent prediction

full target view
→ EMA target encoder
→ stop-gradient latent targets
```

Key scientific correction:

```text
random masked spatiotemporal latent completion
!=
causal history-only → unseen-future world prediction
```

The JEPA pretraining described in the paper is not ego-action conditioned.

## Deployment lifecycle

Official perception-free source verifies:

```text
2 front images
→ pretrained image encoder
→ ordinary Transformer waypoint decoder
→ trajectory
```

The deployed planner does **not** retain:

```text
JEPA predictor
EMA target encoder
masked-target objective
online predicted future latent
world rollout
```

Thus Drive-JEPA's JEPA mechanism is best classified as:

```text
PREDICTIVE REPRESENTATION PRETRAINING
→ ENCODER TRANSFER
```

rather than online world-model reasoning.

## Full planner mechanism

Official source verifies the perception-based planner:

```text
2 front frames + ego/status
→ visual backbone
→ 32 proposal features
→ 4 shared-weight proposal-refinement passes
→ 32 final trajectories
→ learned PDM/EPDMS utility scorer
→ NAVSIM-v2 temporal comfort recalibration
→ argmax trajectory
```

Multimodal Trajectory Distillation (MTD):

```text
8192 offline trajectory vocabulary
→ NAVSIM-v2 rule/simulator evaluation
→ high-quality alternatives (appendix threshold EPDMS > 0.95)
→ pseudo-teacher trajectories
→ human + pseudo-teacher proposal supervision
```

This is candidate/policy supervision, not an online learned consequence model.

---

# Drive-JEPA strongest evidence

## Representation ladder

Simple planning decoder, paper Table 5:

```text
ImageNet ResNet34        76.0 PDMS
DINOv2 ViT/L             76.1
SigLIP ViT/L             83.4
V-JEPA2 ViT/L            86.1
Drive-domain JEPA ViT/L  89.0
```

Interpretation:

```text
strong evidence for transferable predictive video representation
+
useful driving-domain adaptation

NOT direct evidence for online world dynamics
```

The 86.1→89.0 gain is still confounded with additional 330 h driving-domain exposure; it does not isolate a pure objective effect.

## Full planner attribution ladder — NAVSIM-v2

```text
baseline                              84.1 EPDMS / 25% diversity / 68.2 EC
generic V-JEPA2                       85.8       / 21%           / 74.6
driving video pretraining             86.1       / 24%           / 69.7
+ MTD                                 84.5       / 40%           / 47.9
+ momentum-aware selection            87.8       / 40%           / 84.8
```

Important finding:

```text
MTD increases candidate diversity
but initially makes final planning worse;
selection / temporal consistency must solve the larger candidate-support problem.
```

This strongly reinforces:

```text
candidate support != candidate selection quality
```

Pseudo-teacher count is also non-monotonic:

```text
N_pseudo  0    1    2    4    8
EPDMS    87.2 87.8 87.7 87.8 87.5
```

---

# Drive-JEPA source/version boundary

Official source audited:

```text
linhanwang/Drive-JEPA@e21f47410b4d26b61f05f9bd23e169c0390cae2a
```

NAVSIM-v2 source verifies momentum calibration:

```text
past ego simulated states + current candidate
→ two-frame extended comfort
→ (14 * PDM score + 2 * comfort) / 16
→ argmax
```

NAVSIM-v1 public planner file does not expose the same recalibration path. Source claims must therefore remain version-scoped.

Headline number correction:

```text
stale raw-paper abstract occurrence  93.7 PDMS
current official arXiv / README       93.3 PDMS
paper checklist                       93.3 PDMS
```

Use **93.3** as current canonical NAVSIM-v1 headline result.

---

# Ontology V1.2 amendment from Drive-JEPA

One new dimension survives merge/back-projection:

```text
F07  Prediction temporal / observability geometry
```

It distinguishes:

```text
random-mask same-window spatiotemporal completion
past/history-only → unseen future
current → future endpoint
recurrent next-state / autoregressive future
partial-future-context completion
hybrid future masking
```

Drive-JEPA value:

```text
RANDOM-MASK SAME-WINDOW SPATIOTEMPORAL COMPLETION
```

Back-projection examples:

```text
LAW         current/action → future endpoint
WoTE        recurrent next-state future rollout
Epona       history → unseen future generation
WorldDrive  history+trajectory → unseen future
World4Drive current/action → future endpoint
SeerDrive   current/mode → final-horizon future BEV
ViDAR       history → autoregressive future point cloud
```

No new dimensions were added for EMA targets, encoder freezing, proposal refinement, or predictor removal because G02, C03/L05, J08 and M01–M03 already cover them.

---

# Predictive-representation lineage sharpened

```text
ViDAR
history → true chronological future point clouds
→ encoder transfer

LAW
current latent + planner action → factual future latent
→ auxiliary loss during planner training

Drive-JEPA
random masked video latent completion
→ encoder transfer before planner

Auto-JEPA
history/current scene → future ego-trajectory intent latent
→ predicted intent remains online as retrieval key

WA-JEPA
hybrid future masking + future latent generation + joint world/action prediction
```

This lineage is now encoded by F07 + lifecycle dimensions rather than one generic `predictive latent WM` label.

---

# Seven-anchor mechanism map

```text
LAW
= action-aware future-latent auxiliary representation shaping

WoTE
= candidate-conditioned recurrent future BEV → explicit utility → selection

Epona
= shared history latent → joint trajectory + visual generation

WorldDrive
= generative-WM representation inheritance
+ heavy future teacher → distilled online future surrogate → ranking

World4Drive
= candidate/intention-conditioned endpoint latent
→ factual-mode selector

SeerDrive
= future-BEV endpoint ↔ planner-hidden-feature internal co-refinement

Drive-JEPA
= masked-video predictive pretraining → encoder transfer
+ simulator-distilled multimodal proposals → utility/comfort selection
```

---

# Stable controls retained / strengthened

```text
predictive objective != online dynamics model
masked temporal completion != causal future forecasting
world-model pretraining gain != deployed world-model reasoning
candidate diversity != planning quality
candidate support != candidate selection quality
world-prediction quality != planning evidence
future information is not automatically beneficial
conditional future != intervention
foundation-prior gain != WM-specific dynamics gain
consequence teacher != value teacher
evaluation regime is part of the claim
matched controls > headline SOTA
```

---

# Phase C.5 coverage queue

```text
WorldDrive      COMPLETE
World4Drive     COMPLETE
SeerDrive       COMPLETE
Drive-JEPA      COMPLETE
Metis           NEXT
DynFlowDrive    PENDING
Discrete-WAM    PENDING
GraphWorld      PENDING
```

## Immediate next task

See `state/NEXT_TASK.md`.

Deep-read **Metis** next, testing its claimed joint world/action training and especially whether world-generation machinery remains on the deployed action path or serves only as a training-time representation/supervision mechanism.

## Still forbidden

```text
no research-gap declaration
no method design
no broad VLA expansion
no forced risk-field insertion
no novelty conclusion from missing ontology cells
```

GitHub remains the Research Knowledge Authority; official papers/repos are primary evidence for decision-critical claims.
