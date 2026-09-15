# CURRENT_STATE

Last updated: **2026-09-15 — SeerDrive ontology stress test COMPLETE; V1.1 amendment ACTIVE; Drive-JEPA NEXT**

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

The external skills added in `cd4b2ac` have now been converted into a WAM-native stack:

```text
paper-deep-reader
→ single-paper mechanism / formula / figure reconstruction

academic-research-agent source/claim gate
→ source/version discipline + claim/evidence separation

literature-reading-and-synthesis
→ claim-evidence extraction + immediate cross-paper synthesis

WAM Ontology
→ full A–P projection + residue gate
```

Authority:

```text
landscape/WAM_READING_SKILL_STACK.md
```

Research-strategy / peer-review / publication skills are not active by default during field reconstruction.

## Dimension-first normalization

Original five ontology anchors:

```text
P0048 LAW          COMPLETE v2
P0045 WoTE         COMPLETE v2
P0001 Epona        COMPLETE v2
P0042 WorldDrive   COMPLETE v2
P0046 World4Drive  COMPLETE v2
```

First post-ontology stress-test anchor:

```text
P0061 SeerDrive    COMPLETE v2 first pass + source/version audit + full ontology projection
```

Canonical coordinate system:

```text
landscape/WAM_DIMENSION_ONTOLOGY_V1.md
landscape/WAM_DIMENSION_ONTOLOGY_V1_1_AMENDMENT.md
landscape/WAM_COMPARISON_MATRIX_V1.md
landscape/WAM_COMPARISON_MATRIX_V1_1_SEERDRIVE_EXTENSION.md
```

SeerDrive full projection:

```text
landscape/P0061_SEERDRIVE_ONTOLOGY_V1_PROJECTION.md
```

## SeerDrive stable result

Original NeurIPS paper mechanism:

```text
current BEV + multimodal ego/mode features
→ mode-conditioned future BEV endpoint
→ current-side planner branch + future-side planner branch
→ MLN feature fusion
→ final trajectory
→ refined ego/planner feature feeds back into BEV world model
→ update future BEV
→ repeat internal refinement
```

Scientific subtype:

```text
ONLINE BIDIRECTIONAL FEATURE CO-REFINEMENT
```

Important semantic boundary:

```text
internal world↔planner refinement iteration
!= physical-time rollout
!= environment execution-feedback closed loop
```

Default paper design predicts the final-horizon future BEV only. NAVSIM ablation:

```text
1s-2s-3s-4s future BEVs  88.8 PDMS
2s-4s future BEVs         88.9
4s endpoint only           88.9
```

Thus richer temporal future prediction did not add meaningful planning value in this setup.

Strongest matched component evidence:

```text
future-aware OFF + iterative OFF   87.1
future-aware OFF + iterative ON    87.9
future-aware ON  + iterative OFF   88.1
future-aware ON  + iterative ON    88.9
```

This supports both future-BEV consumption and internal co-refinement as useful within the architecture, without proving causal/reactive alternative-world correctness.

## SeerDrive source/version boundary

Official README states the public release was updated by integrating WoTE's online trajectory evaluation/selection and reports ~88.88 PDMS **without the iterative interaction between planning and scene modeling**.

The official repo `initial release` commit:

```text
1cfb7ecdbdbbe52fd598949efe4edf8f6fb12b69
```

already contains WoTE-style `RewardConvNet`, reward heads and candidate evaluation machinery.

Therefore:

```text
original paper mechanism
→ paper is primary authority

released code mechanism
→ post-paper WoTE-integrated variant

DO NOT merge them into one undocumented method
```

Canonical audit:

```text
audits/literature/PHASE_C5_SEERDRIVE_AUDIT.md
```

## Ontology V1.1 amendment from SeerDrive

After residue/merge testing, only three new dimensions survived:

```text
J08  Inference iteration semantics
J09  Planner→world feedback carrier
L07  Iterative-state supervision coverage
```

Two initial candidates were NOT added because existing V1 dimensions already cover them:

```text
mutual-refinement topology → J04
refinement-depth performance curve → N06
```

This is the active rule for ontology growth: **new paper first fills V1, residue must survive back-projection before a new axis is accepted.**

## Six-anchor mechanism map

```text
LAW
= future prediction as auxiliary representation shaping

WoTE
= temporal candidate future BEV rollout → explicit utility → selection

Epona
= shared history latent → direct generative trajectory policy
+ sibling visual future generator

WorldDrive
= generative-WM representation inheritance
+ heavy future teacher → distilled lightweight future surrogate → ranking

World4Drive
= online candidate endpoint latent → factual-future/mode ScoreNet → selection

SeerDrive
= online endpoint future BEV → planner feature refinement
→ refined planner feature feeds back into WM
→ internal world↔planner co-refinement
```

## Stable controls retained

```text
world-prediction quality != planning evidence
world completeness != decision relevance
future information is not automatically beneficial
candidate-specific output != candidate-specific observed counterfactual supervision
conditional future != intervention
internal iterative refinement != temporal rollout != external closed loop
candidate ranking/scoring is an independent bottleneck
foundation-prior gain != WM-specific dynamics gain
consequence teacher != value teacher
evaluation regime is part of the claim
matched controls > headline SOTA
```

## Phase C.5 coverage queue

```text
WorldDrive      COMPLETE
World4Drive     COMPLETE
SeerDrive       COMPLETE
Drive-JEPA      NEXT
Metis           PENDING
DynFlowDrive    PENDING
Discrete-WAM    PENDING
GraphWorld      PENDING
```

## Immediate next task

See `state/NEXT_TASK.md`.

Deep-read **Drive-JEPA** using the WAM reading skill stack + Ontology V1/V1.1, specifically testing whether JEPA-style predictive representation introduces a genuinely distinct future/planning interface or mainly changes the dynamics-learning objective/target-network semantics.

## Still forbidden

```text
no research-gap declaration
no method design
no broad VLA expansion
no forced risk-field insertion
no novelty conclusion from missing ontology cells
```

GitHub remains the Research Knowledge Authority; official papers/repos are primary evidence for decision-critical claims.
