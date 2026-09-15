# NEXT_TASK

## 唯一下一任务

> **Deep-read Drive-JEPA under the WAM reading skill stack + Ontology V1/V1.1, as the second post-ontology stress test.**

## Completed normalization / stress tests

```text
P0048 LAW          COMPLETE v2
P0045 WoTE         COMPLETE v2
P0001 Epona        COMPLETE v2
P0042 WorldDrive   COMPLETE v2
P0046 World4Drive  COMPLETE v2
P0061 SeerDrive    COMPLETE v2 first pass
```

Canonical method stack:

```text
landscape/WAM_READING_SKILL_STACK.md
```

Canonical coordinate system:

```text
landscape/WAM_DIMENSION_ONTOLOGY_V1.md
landscape/WAM_DIMENSION_ONTOLOGY_V1_1_AMENDMENT.md
landscape/WAM_COMPARISON_MATRIX_V1.md
landscape/WAM_COMPARISON_MATRIX_V1_1_SEERDRIVE_EXTENSION.md
```

SeerDrive artifacts:

```text
papers/deep_analysis/P0061_SEERDRIVE_DEEP_ANALYSIS_V2.md
audits/literature/PHASE_C5_SEERDRIVE_AUDIT.md
landscape/P0061_SEERDRIVE_ONTOLOGY_V1_PROJECTION.md
```

## Why Drive-JEPA is next

Drive-JEPA is the next core-WAM coverage item and should stress a different part of the ontology than SeerDrive.

Main questions:

```text
1. What exactly is the JEPA target representation?
2. Is there an online/EMA/frozen target encoder?
3. Does future prediction shape representation only, or remain in deployed planning?
4. What is the action/trajectory condition, if any?
5. What information is deliberately omitted from prediction versus reconstructed?
6. How does JEPA differ scientifically from LAW latent prediction?
7. How does it differ from ViDAR / Auto-JEPA / WA-JEPA predictive pretraining?
8. Is the planner direct, candidate-based, or future-evaluator based?
9. Which gains come from predictive objective vs backbone/pretraining/data?
10. Does JEPA prediction quality correlate with planning quality?
11. What target-network / stop-gradient / collapse-avoidance mechanism is used?
12. What future horizon/object gives the strongest planning signal?
13. Is the model learning world dynamics, representation invariance, or both?
14. What remains at inference?
15. What matched control isolates the JEPA-specific mechanism?
```

## Mandatory workflow

```text
official paper / RAW_MD / supplement / version-locked source if needed
→ paper-deep-reader mechanism reconstruction
→ source/claim gate
→ claim–evidence extraction
→ fill all Ontology V1 + V1.1 dimensions
→ compare every important mechanism immediately with LAW / WoTE / Epona / WorldDrive / World4Drive / SeerDrive
→ identify ontology residue
→ back-project any proposed new dimension before acceptance
```

Do not assume `JEPA = world model` merely from naming. Establish:

```text
predicted object
future semantics
supervision
planning interface
deployment role
```

## Required output

```text
papers/deep_analysis/P0049_DRIVEJEPA_DEEP_ANALYSIS_V2.md
audits/literature/PHASE_C5_DRIVEJEPA_AUDIT.md
landscape/P0049_DRIVEJEPA_ONTOLOGY_PROJECTION.md
comparison matrix extension/update
```

## Stop condition

Do not move to Metis until we can state without ambiguity:

```text
what JEPA predicts
where its target comes from
why this is different from LAW-style future-latent regression
what action/planning information conditions prediction
whether predictive knowledge remains online
what evidence isolates JEPA-specific planning value
whether a new ontology dimension is genuinely needed
```

## After Drive-JEPA

```text
Metis
DynFlowDrive
Discrete-WAM
GraphWorld
```

## Still forbidden

```text
no research-gap declaration
no method design
no broad VLA expansion
no forced risk-field insertion
no novelty conclusion from empty ontology cells
```
