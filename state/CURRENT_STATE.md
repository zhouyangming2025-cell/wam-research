# CURRENT_STATE

Last updated: **2026-09-15 — Dimension-first normalization ACTIVE; Ontology V1 COMPLETE; Comparison Matrix V1 NEXT**

## Research north star

```text
WAM / World Model + one-stage End-to-End + Planning-centric autonomous driving
```

Core 2.2 WAM is primary. WAM+VLA remains secondary/control until core-WAM coverage is stable. Risk/predictive-risk expertise is optional prior knowledge, not a required destination.

## Methodology in force

```text
FIELD UNDERSTANDING FIRST
→ complete core-WAM coverage
→ comparative anchor deep reads
→ DIMENSION-FIRST normalization
→ WAM-only synthesis
→ evidence QA
→ only then adversarial problem discovery
→ falsification
→ method design
```

Phase D problem discovery remains **PAUSED**.

## Completed foundation

```text
Phase A census     CLOSED
Wave 1             CLOSED
Wave 2             CLOSED
Wave 3             CLOSED
Research QA Gate   CLOSED
Wave 4             CLOSED
Phase-C synthesis  COMPLETE FIRST PASS
Phase C.5          ACTIVE
```

The prior field synthesis remains a useful provisional coordinate system, but the project now treats **uniform mechanism/evidence comparability** as a mandatory gate before problem discovery.

## Dimension-first anchor normalization

The first five ontology-discovery anchors are complete:

```text
P0048 LAW          COMPLETE v2
P0045 WoTE         COMPLETE v2
P0001 Epona        COMPLETE v2
P0042 WorldDrive   COMPLETE v2
P0046 World4Drive  COMPLETE v2
```

Canonical deep analyses:

```text
papers/deep_analysis/P0048_LAW_DEEP_ANALYSIS_V2.md
papers/deep_analysis/P0045_WOTE_DEEP_ANALYSIS_V2.md
papers/deep_analysis/P0001_EPONA_DEEP_ANALYSIS_V2.md
papers/deep_analysis/P0042_WORLDDRIVE_DEEP_ANALYSIS_V2.md
papers/deep_analysis/P0046_WORLD4DRIVE_DEEP_ANALYSIS_V2.md
```

Dimension-discovery sources:

```text
landscape/WAM_DIMENSION_DISCOVERY_LOG.md
landscape/WAM_DIMENSION_DISCOVERY_ADDENDUM_EPONA_WORLDDRIVE.md
landscape/WAM_DIMENSION_DISCOVERY_ADDENDUM_WORLD4DRIVE.md
```

## Ontology V1 status

Created:

```text
landscape/WAM_DIMENSION_ONTOLOGY_V1.md
```

Ontology V1 is a stable extensible baseline, not a closed universe. It organizes the comparison space into 16 families:

```text
A  problem / role of world knowledge
B  observation and current-state representation
C  representation provenance / imported priors
D  action / intention / candidate space
E  action → world coupling
F  dynamics / future temporal modeling
G  future supervision / truth sources
H  multimodal branch identity / assignment
I  counterfactuality / reactivity
J  world → planning interface
K  scorer / decision semantics
L  training topology / jointness / gradients
M  future-knowledge lifecycle / deployment path
N  compute / pruning / latency
O  evaluation regime / evidence attribution
P  safety / uncertainty / interaction / physical validity
```

Binding ontology corrections:

```text
action-conditioned != WM-based action selection
joint modeling != shared representation != shared gradients != online feedback
candidate-specific output != candidate-specific alternative-future supervision
future→score != necessarily utility/value
foundation-prior gain != WM-specific future-model gain
online/offline is too coarse; future knowledge has a lifecycle
consequence teacher != value teacher
prediction fidelity != decision relevance
```

Every anchor must fill every stable dimension with a value or explicit `ABSENT / NOT REPORTED / NOT EVALUATED / NOT APPLICABLE / UNCLEAR`.

## Five-anchor mechanism sanity map

```text
LAW
= action-aware future prediction as auxiliary representation shaping
→ future output not consumed by deployed action selection

WoTE
= multi-candidate recurrent future BEV
→ explicit imitation/simulator utility
→ online selection

Epona
= shared historical world representation
→ direct generative trajectory policy
+ sibling visual-future generator
→ visual future not required by planning inference

WorldDrive
= generative-WM representation inheritance
+ heavy future teacher
→ distilled lightweight future surrogate
→ online preference/ranking

World4Drive
= six intention-conditioned compact future latents online
→ factual-future/mode ScoreNet
→ trajectory selection
```

## Stable evidence controls retained

```text
world-prediction quality != planning evidence
future information is not automatically beneficial
candidate-specific output != candidate-specific observed counterfactual supervision
WM-assisted planning != full online generative rollout
world completeness != decision relevance
candidate ranking/scoring is an independent bottleneck
evaluation regime is part of the claim
reactive feasibility != counterfactual behavioral truth
matched controls > headline SOTA
conditional future != intervention
multimodal action generation != world modeling
```

## Current core-WAM coverage correction queue

New-paper reading is temporarily paused until the first comparison matrix is complete.

After normalization:

```text
SeerDrive       NEXT NEW ANCHOR
Drive-JEPA      PENDING
Metis           PENDING
DynFlowDrive    PENDING
Discrete-WAM    PENDING
GraphWorld      PENDING
```

## Immediate next task

See `state/NEXT_TASK.md`.

Build:

```text
landscape/WAM_COMPARISON_MATRIX_V1.md
```

Project LAW / WoTE / Epona / WorldDrive / World4Drive across the Ontology V1 dimensions, grouped by family rather than as one unreadable flat table.

## Still forbidden

```text
no problem/gap declaration
no method design
no broad VLA expansion
no forced risk-field insertion
no novelty conclusion from missing cells
```

GitHub remains the Research Knowledge Authority; official papers/repos remain primary evidence for decision-critical claims.
