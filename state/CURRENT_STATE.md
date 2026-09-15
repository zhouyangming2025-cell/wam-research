# CURRENT_STATE

Last updated: **2026-09-15 — Metis stress test COMPLETE; Ontology V1.2 RETAINED; DynFlowDrive NEXT**

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
P0049 Drive-JEPA   COMPLETE v2 first pass + source audit
P0062 Metis        COMPLETE v2 first pass + paper/official-repo audit
```

Canonical coordinate system remains:

```text
landscape/WAM_DIMENSION_ONTOLOGY_V1.md
landscape/WAM_DIMENSION_ONTOLOGY_V1_1_AMENDMENT.md
landscape/WAM_DIMENSION_ONTOLOGY_V1_2_AMENDMENT.md
```

Comparison layer:

```text
landscape/WAM_COMPARISON_MATRIX_V1.md
landscape/WAM_COMPARISON_MATRIX_V1_1_SEERDRIVE_EXTENSION.md
landscape/WAM_COMPARISON_MATRIX_V1_2_DRIVEJEPA_EXTENSION.md
landscape/WAM_COMPARISON_MATRIX_V1_2_METIS_EXTENSION.md
```

New Metis artifacts:

```text
papers/deep_analysis/P0062_METIS_DEEP_ANALYSIS_V2.md
audits/literature/PHASE_C5_METIS_AUDIT.md
landscape/P0062_METIS_ONTOLOGY_PROJECTION.md
```

---

# Metis stable result

## Source/version boundary

Paper:

```text
arXiv:2606.15869 v1
submitted 2026-06-14
```

Official repository:

```text
LogosRoboticsGroup/Metis
latest observed public commit:
7677b62d786cff8bb2044b489bd41f3d59514b43
```

As of 2026-09-15, training/inference/evaluation implementation remains unreleased despite an earlier August release plan.

Therefore:

```text
paper mechanism         PAPER-VERIFIED
official README claims  VERIFIED
implementation details  SOURCE-UNVERIFIED
```

Unresolved reporting inconsistency retained:

```text
main method/README VGE: Wan2.2-5B
capacity-ablation label: Wan2.2-14B
```

Do not silently reconcile until source/configs are released.

---

# Metis mechanism

Canonical subtype:

```text
TRAINING-ONLY ASYMMETRIC WORLD-ACTION CO-TRAINING
→ WORLD-LOSS-SHAPED ACTION EXPERT
→ ACTION-ONLY FLOW POLICY
```

Training graph:

```text
current observation + language + ego state
→ Action Expert (AE)
→ future action representation
          ↓
          conditions
          ↓
Video Generation Expert (VGE)
→ factual future-video flow loss
          ↓ backward gradient
          └──────────────→ shapes AE
```

The asymmetric mask enforces:

```text
FORWARD:
action tokens → future-video tokens     YES
future-video tokens → action tokens     NO

BACKWARD:
video-generation loss → action expert   YES
```

This is the key scientific distinction:

```text
world→action gradient influence
!=
world→action forward information flow
```

Deployment graph:

```text
current observation + language + ego state
→ action expert flow denoising
→ trajectory
```

Explicit deployed future object:

```text
NONE
```

Thus Metis is not an online `imagine future → inspect future → choose action` planner.

---

# Metis future supervision

Future-world target:

```text
logged factual future video latent
```

Action target:

```text
logged factual trajectory/action chunk
```

F07:

```text
CURRENT-CONTEXT + ACTION
→ CHRONOLOGICALLY UNSEEN FUTURE VIDEO
(flow-matched fixed-window generation)
```

Important boundary:

```text
one logged action + one factual future
!=
multiple observed alternative-action futures
```

No intervention-valid/reactive alternative-agent future truth is established.

---

# Metis strongest evidence

## World-task co-training on/off

```text
without video co-training   87.4 PDMS / 87.9 EPDMS
with video co-training      89.1 PDMS / 89.5 EPDMS
```

Supports:

```text
future-video co-training benefits the reported action-policy family
```

Does not isolate:

```text
future-video fidelity
causal dynamics accuracy
generic auxiliary regularization
imported video prior
AE capacity / resolution effects
```

## Attention topology — matched 320×384

```text
Joint       87.4 navtest / 28.0 navhard EPDMS
Isolated    88.3         / 29.4
Asymmetric  88.8         / 31.6
```

This establishes:

```text
tighter/symmetric coupling is not automatically better
asymmetric training coupling > full isolation in this architecture
```

Because AE cannot attend future-video tokens, the gain is not evidence of direct future-video→action reasoning.

## Action denoising quality–compute curve

```text
steps   navtest EPDMS   navhard EPDMS
1       87.2            30.4
2       89.2            31.2
5       89.4            31.4
10      89.5            32.2
```

Paper latency operating points on RTX 4090:

```text
with video        1.38 s
action-only       ~0.17 s
```

But video uses 10 denoising steps while the efficient action-only point uses 2, so the ~8× number is not a pure matched branch-removal ablation.

---

# Metis world-quality evidence boundary

No dedicated quantitative future-video fidelity metric such as FVD/PSNR/SSIM was identified in the audited paper text; world-generation evidence is mainly qualitative.

Therefore:

```text
video co-training helps planning
!=
better video prediction fidelity causes better planning
```

O07 remains:

```text
ABSENT direct prediction-fidelity → planning evidence
```

---

# Metis historical boundary

Metis cites Fast-WAM and explicitly says its decoupled inference paradigm is inspired by it.

Therefore the broad lifecycle:

```text
world/video co-training during training
→ skip explicit future generation at inference
```

is not unique to Metis.

Metis-specific scientific contribution is better described as:

```text
Mixture-of-Transformers expert separation
+ asymmetric attention
+ action-conditioned future-video task
+ video-loss→AE gradient shaping
+ action-only flow deployment
```

---

# Ontology stress-test result

Potential residue:

```text
forward action→world
backward world-loss→action
without world-future→action forward dependency
```

Existing dimensions already represent it:

```text
E01/E02  forward action→world
J04      coupling direction
L04      gradient coupling direction
M01-M03  training→deployment lifecycle
```

Decision:

```text
NO V1.3 amendment.
Ontology V1.2 remains active.
```

This is a positive stability result for the coordinate system.

---

# Eight-anchor mechanism map

```text
LAW
= action-aware future-latent auxiliary representation shaping

WoTE
= candidate-conditioned recurrent future BEV → explicit utility → selection

Epona
= shared history latent → trajectory + visual generative branches

WorldDrive
= heavy generative future teacher → distilled online future surrogate → ranking

World4Drive
= candidate/intention-conditioned endpoint future latent → factual-mode selector

SeerDrive
= future-BEV endpoint ↔ planner-hidden-feature internal co-refinement

Drive-JEPA
= masked-video predictive pretraining → encoder transfer
+ simulator-distilled multimodal proposals → utility/comfort selection

Metis
= action-conditioned future-video co-training
→ video-loss gradient shapes action expert
→ future-video branch bypassed
→ direct action-flow policy
```

---

# Stable controls retained / strengthened

```text
joint training != shared representation != shared parameters
joint training != symmetric forward coupling
world→action gradient influence != world→action inference flow
world-task benefit != online future consumption
world co-training != test-time imagination
prediction quality != planning evidence
action-conditioned future != intervention-valid future
foundation-prior gain != WM-specific dynamics gain
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
Metis           COMPLETE
DynFlowDrive    NEXT
Discrete-WAM    PENDING
GraphWorld      PENDING
```

## Immediate next task

See `state/NEXT_TASK.md`.

Deep-read **DynFlowDrive** next. Primary stress-test question:

```text
Does rectified-flow latent dynamics provide a genuinely decision-relevant trajectory-conditioned transition process,
or is the gain primarily generated by its stability-aware selection/supervision criterion?
```

Particular care is required to separate:

```text
flow denoising time
physical future time
candidate trajectory modes
latent reconstruction
flow-field stability score
final action selection
```

## Still forbidden

```text
no research-gap declaration
no method design
no broad VLA expansion
no forced risk-field insertion
no novelty conclusion from missing ontology cells
```

GitHub remains the Research Knowledge Authority; official papers/repos are primary evidence for decision-critical claims.
