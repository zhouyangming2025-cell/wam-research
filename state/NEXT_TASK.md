# NEXT_TASK

## 唯一下一任务

> **Deep-read P0007 DriveReward as the fifth paper in Wave C.6. Treat it as a value/reward control anchor; keep research-direction convergence paused.**

Canonical expansion plan:

```text
landscape/WAM_DEEP_READ_EXPANSION_QUEUE_V1.md
```

Current phase:

```text
broad WAM literature expansion     ACTIVE
research-direction convergence     PAUSED
candidate-problem promotion        PAUSED
method design                      FORBIDDEN
```

Current normalized count:

```text
15 anchors complete
DriveLaW  = COMPLETE
DA-WAM    = COMPLETE
SafeDrive = COMPLETE
RiskWorld = COMPLETE
DriveReward = NEXT
```

---

# Why DriveReward is next

DriveReward is selected for coverage diversity. It is a control anchor for the hypothesis-independent question:

```text
Can planning quality improve through learned semantic reward/value
without predicting an explicit future world state?
```

This is needed to prevent the WAM atlas from conflating:

```text
future-world modeling
with
trajectory valuation / reward modeling
```

Immediate comparisons:

```text
DriveReward vs WoTE
DriveReward vs DA-WAM
DriveReward vs SafeDrive
DriveReward vs RiskWorld
DriveReward vs Drive-JEPA / WorldDrive
```

---

# Mandatory reconstruction

## 1. Source/version boundary

Resolve canonical paper, project/repository, code-release state and audited commit if implementation exists.

## 2. Input and trajectory representation

Reconstruct exactly:

```text
visual/current context
+ ego trajectory / action proposal
→ reward/value model input
```

Determine whether future world state is generated at all.

## 3. Reward semantics

For every reward component identify:

```text
safety
progress
comfort
rule compliance
human preference
semantic quality
planning score
```

and its target provenance.

## 4. Training graph

Separate:

```text
supervised reward learning
preference learning
VLM/generative reasoning
RL/post-training
planner/policy training
```

Track which modules receive which gradients.

## 5. Inference graph

Determine whether reward is used for:

```text
candidate ranking
trajectory reranking
RL policy only
search / optimization
training-only supervision
```

## 6. World-model boundary

Force explicit answers:

```text
Is any future environment state predicted?
Is the reward model a consequence model or a value model?
Does it consume predicted future or only current context + trajectory?
```

## 7. Supervision truth

Audit reward labels / preference labels / simulator metrics / human or VLM teacher signals separately.

## 8. Strongest matched ablations

Prioritize controls isolating:

```text
base planner
+ reward model
+ semantic/VLM reasoning
+ RL/post-training
+ test-time reranking if present
```

## 9. Evaluation regime

Separate open-loop, NAVSIM pseudo-simulation, reactive closed loop and real-car evidence.

## 10. Full Ontology V1.3 projection

Force-fill A–P. Do not add V1.4 unless a genuinely irreducible dimension survives back-projection.

---

# Required artifacts

```text
papers/deep_analysis/P0007_DRIVEREWARD_DEEP_ANALYSIS_V2.md
audits/literature/PHASE_C6_DRIVEREWARD_AUDIT.md
landscape/P0007_DRIVEREWARD_ONTOLOGY_PROJECTION.md
landscape/WAM_COMPARISON_MATRIX_V1_3_DRIVEREWARD_EXTENSION.md
```

---

# Guardrail

This remains field reconstruction / literature expansion.

Do not reopen research-direction convergence after RiskWorld or DriveReward.
