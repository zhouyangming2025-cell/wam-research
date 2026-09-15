# NEXT_TASK

## 唯一下一任务

> **Deep-read DynFlowDrive under the WAM reading skill stack + Ontology V1/V1.1/V1.2, as the next core-WAM stress test.**

## Completed normalization / stress tests

```text
P0048 LAW          COMPLETE v2
P0045 WoTE         COMPLETE v2
P0001 Epona        COMPLETE v2
P0042 WorldDrive   COMPLETE v2
P0046 World4Drive  COMPLETE v2
P0061 SeerDrive    COMPLETE v2 first pass
P0049 Drive-JEPA   COMPLETE v2 first pass
P0062 Metis        COMPLETE v2 first pass
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
```

Current comparison layer:

```text
landscape/WAM_COMPARISON_MATRIX_V1.md
landscape/WAM_COMPARISON_MATRIX_V1_1_SEERDRIVE_EXTENSION.md
landscape/WAM_COMPARISON_MATRIX_V1_2_DRIVEJEPA_EXTENSION.md
landscape/WAM_COMPARISON_MATRIX_V1_2_METIS_EXTENSION.md
```

Metis artifacts:

```text
papers/deep_analysis/P0062_METIS_DEEP_ANALYSIS_V2.md
audits/literature/PHASE_C5_METIS_AUDIT.md
landscape/P0062_METIS_ONTOLOGY_PROJECTION.md
```

## Why DynFlowDrive is next

DynFlowDrive claims that ordinary latent world models use static endpoint regression, while its rectified-flow dynamics model represents the **continuous transition process** of the latent world under candidate trajectories.

Its initial paper-level graph is:

```text
current multi-view observation
→ scene representation
→ multi-mode trajectory proposals

current latent world state + candidate trajectory
→ rectified-flow velocity field
→ progressive latent-state transition

flow/reconstruction/stability information
→ stability-aware multi-mode selection/supervision
→ final trajectory
```

This directly stress-tests several ontology distinctions that Metis did not:

```text
flow denoising time vs physical future time
endpoint state vs transition path
candidate-specific future vs true alternative-action future
world dynamics vs selector/scorer contribution
prediction stability vs planning utility
```

## Primary scientific question

> **Does DynFlowDrive obtain its planning gain because rectified-flow world dynamics genuinely capture trajectory-conditioned scene evolution, or because the learned flow field provides a useful stability/selection regularizer over trajectory modes?**

The paper must not be allowed to answer this question with architecture language alone.

## Mandatory audit targets

Resolve at minimum:

```text
1. observation/history representation and sensor inputs
2. planner scene representation vs world-model latent representation
3. provenance/freeze status of the foundation encoder used for world features
4. candidate trajectory construction and number of modes
5. exact action representation entering the world model
6. exact future latent target and ground-truth lineage
7. rectified-flow state, flow-time variable and velocity target
8. what one integration/flow step means scientifically
9. whether flow time corresponds to physical scene time or only transport/denoising time
10. whether future scene time is one endpoint, multiple timestamps, or progressive latent path
11. F07 prediction temporal/observability geometry
12. whether each candidate gets its own action-conditioned latent transition
13. whether candidate branches have alternative-action factual supervision
14. how `stability` is mathematically defined from the flow field
15. what latent reconstruction discrepancy contributes
16. how ground-truth trajectory error enters stability-aware selection/training
17. whether the selector is training-only supervision or remains online at inference
18. whether claimed “no additional inference overhead” means WM is removed, distilled, or reused only during training
19. J08 iteration semantics: flow integration vs physical-time rollout vs planner refinement
20. J09 planner→world carrier
21. L07 supervision coverage across flow/integration states
22. strongest matched ablation: static regression vs flow dynamics vs stability selector
23. direct evidence that better flow/world prediction yields better planning
24. source-code/repo status and version lock
25. evaluation regime on nuScenes vs NAVSIM
26. relation to LAW / WoTE / World4Drive / SeerDrive / Metis
```

## Required semantic attack: `flow` is overloaded

Do not accept wording such as `progressive world evolution` until the following are separated:

```text
physical time τ
= future scene timestamp

flow / ODE transport time s
= interpolation/integration variable used to transform latent/noise/state

planner iteration k
= candidate-query refinement or selection iteration
```

A continuous path in flow-time does **not automatically mean** the model has supervised every physical intermediate future state.

The audit must trace exact tensor targets and timestamps.

## Required selector attack

DynFlowDrive explicitly introduces a stability-aware multi-mode selector. Therefore every planning gain must be decomposed into at least:

```text
base multi-mode planner
→ + static/endpoint latent world prediction if available
→ + rectified-flow dynamics
→ + stability criterion
→ + reconstruction criterion
→ + final mode supervision/selection
```

If ablations do not isolate these pieces cleanly, record the unresolved bundle rather than assigning all gain to the dynamic world model.

## Required counterfactual attack

Candidate-conditioned latent transitions must be checked against:

```text
candidate-specific output?
YES/NO

candidate-specific observed future truth?
YES/NO

reactive surrounding-agent responses under each candidate?
YES/NO

external intervention-validity test?
YES/NO
```

Do not infer counterfactual correctness from candidate-conditioned flow generation.

## Required workflow

```text
official paper / RAW_MD / supplement / official repo
→ mechanism + formula reconstruction
→ source/version gate
→ claim–evidence extraction
→ full Ontology V1 + V1.1 + V1.2 projection
→ immediate horizontal comparison
→ residue test
→ back-project any proposed dimension before ontology extension
```

## Required comparisons

Especially compare with:

```text
LAW
= action-aware future endpoint latent, auxiliary training signal

WoTE
= candidate-conditioned recurrent BEV transition → explicit utility

World4Drive
= candidate/intention-conditioned endpoint latent → ScoreNet

SeerDrive
= endpoint future BEV ↔ planner hidden feature co-refinement

Metis
= rectified/flow formulation used for action/video generation,
but future-video branch removed from action inference
```

The key question is whether DynFlowDrive creates a genuinely different **world dynamics object**, a different **decision criterion**, or both.

## Required output

```text
papers/deep_analysis/P0063_DYNFLOWDRIVE_DEEP_ANALYSIS_V2.md
audits/literature/PHASE_C5_DYNFLOWDRIVE_AUDIT.md
landscape/P0063_DYNFLOWDRIVE_ONTOLOGY_PROJECTION.md
comparison matrix extension/update
```

Add a new ontology dimension only if a residue cannot be represented by the existing axes and survives back-projection.

## Stop condition

Do not move to Discrete-WAM until we can state without ambiguity:

```text
what physical future object DynFlowDrive predicts;
what the rectified-flow variable actually represents;
whether progressive flow states correspond to physical intermediate futures;
how candidate trajectory conditions world evolution;
what truth supervises candidate-conditioned futures;
what stability means mathematically;
whether WM/stability logic remains online;
which ablation isolates flow dynamics from selector design;
what is proven vs author framing.
```

## After DynFlowDrive

```text
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
