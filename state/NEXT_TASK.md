# NEXT_TASK

## 唯一下一任务

> **Deep-read Metis under the WAM reading skill stack + Ontology V1/V1.1/V1.2, as the next core-WAM stress test.**

## Completed normalization / stress tests

```text
P0048 LAW          COMPLETE v2
P0045 WoTE         COMPLETE v2
P0001 Epona        COMPLETE v2
P0042 WorldDrive   COMPLETE v2
P0046 World4Drive  COMPLETE v2
P0061 SeerDrive    COMPLETE v2 first pass
P0049 Drive-JEPA   COMPLETE v2 first pass
```

Canonical method stack:

```text
landscape/WAM_READING_SKILL_STACK.md
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

Drive-JEPA artifacts:

```text
papers/deep_analysis/P0049_DRIVEJEPA_DEEP_ANALYSIS_V2.md
audits/literature/PHASE_C5_DRIVEJEPA_AUDIT.md
landscape/P0049_DRIVEJEPA_ONTOLOGY_PROJECTION.md
```

## Why Metis is next

Metis is currently placed as:

```text
joint world/action training
→ action-only inference
```

That placement is decision-relevant but still too coarse. The main task is to reconstruct whether world generation is:

```text
a shared generative process with action,
a training-only auxiliary target,
a representation-shaping teacher,
or an online decision mechanism.
```

The key scientific question is:

> **Does Metis genuinely unify world and action modeling at the mechanism level, or does it train them jointly while deployment collapses to an action-only policy whose world branch no longer participates in action selection?**

## Mandatory audit targets

Resolve at minimum:

```text
1. observation/history representation
2. world-state / future-world substrate
3. action representation
4. exact world target and target truth source
5. exact action target / policy supervision
6. whether world and action tokens share backbone, latent space, parameters or only training schedule
7. whether losses jointly update the same representation
8. action→world and world→action arrows during training
9. action→world and world→action arrows during inference
10. whether future/world tokens are generated at action-only deployment
11. whether action-only inference still internally consumes world hidden states
12. training-stage topology and any freeze/distillation stages
13. F07 prediction temporal/observability geometry
14. autoregressive / diffusion / flow / token-generation factorization
15. candidate vs direct policy interface
16. source/version status, especially if code remains unavailable
17. matched ablations isolating world/action jointness
18. strongest alternative explanation for gains
19. planning evaluation regime and world-generation evaluation regime
20. relation to Epona / DriveLaW / LAW / Drive-JEPA / WorldDrive
```

## Required comparison attacks

Do not accept `joint world-action model` as one binary label. Explicitly distinguish:

```text
shared representation?
shared parameters?
shared latent/token space?
shared generative process?
shared gradients?
world→action online feedback?
action→world online conditioning?
world branch required at action inference?
```

Compare especially with:

```text
Epona
= shared historical latent + separate trajectory/visual generative branches;
visual future optional for planning

Drive-JEPA
= predictive pretraining transferred to encoder;
predictor absent from action inference

LAW
= future prediction shapes planner representation during training;
future output not consumed online

WorldDrive
= heavy world teacher transformed into lightweight online future surrogate

DriveLaW
= online learned world hidden state participates directly in action generation
```

## Mandatory workflow

```text
official paper / RAW_MD / supplement / official repo if available
→ mechanism reconstruction
→ source/version gate
→ claim–evidence extraction
→ fill all Ontology dimensions including J08/J09/L07/F07
→ immediate horizontal comparison
→ residue test
→ back-project any proposed new dimension before ontology extension
```

If source code is still unavailable, record exact claims as `paper-verified / source-unverified`; do not invent implementation details.

## Required output

```text
papers/deep_analysis/<METIS>_DEEP_ANALYSIS_V2.md
audits/literature/PHASE_C5_METIS_AUDIT.md
landscape/<METIS>_ONTOLOGY_PROJECTION.md
comparison matrix extension/update
```

## Stop condition

Do not move to DynFlowDrive until we can state without ambiguity:

```text
what “joint world-action” actually means in tensors/gradients;
what world information survives into action deployment;
whether action-only inference still uses an implicit world hidden state;
what F07 prediction obligation is learned;
which matched evidence isolates joint world/action training;
what is proven vs only author framing.
```

## After Metis

```text
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
