# NEXT_TASK

## 唯一下一任务

> **Deep-read P0005 RiskWorld as the fourth paper in Wave C.6. Treat it as an explicit-risk/world-state boundary anchor; keep research-direction convergence paused.**

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
14 anchors complete
DriveLaW  = COMPLETE
DA-WAM    = COMPLETE
SafeDrive = COMPLETE
RiskWorld = NEXT
```

---

# Why RiskWorld is next

RiskWorld is selected for coverage diversity, not because it supports a preferred hypothesis.

It is expected to occupy a boundary position:

```text
object-centric latent world state
→ temporal rollout / future ego-object relation
→ explicit object-level risk identification
```

The key question is whether `risk` is itself a predicted world-state variable, a downstream evaluator, a handcrafted label, or a planning value proxy.

This is materially different from:

```text
SafeDrive   candidate-specific sparse world → learned safety evaluator
WoTE        recurrent future BEV → utility
DA-WAM      candidate future latent → factorized utility
GraphWorld  structured world state → direct policy
World4Drive future latent → factual-mode score
```

---

# Mandatory reconstruction

## 1. Source/version boundary

Resolve:

```text
canonical paper/version
official repository/project page
code-release state
paper↔code relation
```

Lock a commit if official implementation exists.

## 2. Problem boundary

Before calling it a planning WAM, determine:

```text
Is RiskWorld primarily:
- world model?
- risk prediction model?
- planning model?
- simulator?
- representation learner?
```

If no action-selection interface exists, keep it as a boundary anchor rather than forcing it into the core planner family.

## 3. Observation and object-centric state

Reconstruct:

```text
sensor/history input
→ object extraction / slots / tracks
→ latent object state
→ scene/world state
```

Determine exactly what one object state contains and whether identity persists across time.

## 4. Dynamics / rollout

Trace:

```text
current latent state
→ transition / RSSM / recurrent dynamics
→ future latent/object states
```

Lock:

```text
physical timestep
prediction horizon
teacher forcing vs free rollout
stochastic vs deterministic state
latent prior/posterior structure
```

Use F04/F05/F06/F07/F08.

## 5. Ego-action conditioning

Force explicit answers:

```text
Does ego trajectory/action condition future dynamics?
How is it represented/injected?
Does changing ego action create a different predicted world?
Are alternative actions supervised?
```

Do not infer counterfactual capability from recurrent prediction alone.

## 6. Risk representation

For each risk quantity identify:

```text
object-level or scene-level?
current or future?
probability / score / binary class / continuous field?
learned or rule-derived?
supervision source?
calibrated or only discriminative?
```

Separate:

```text
predicted risk state
vs safety/value evaluator
vs benchmark collision metric
```

## 7. Future ego-object relation

If RiskWorld derives risk from future relational states, reconstruct:

```text
predicted ego state
predicted object state
relative geometry / interaction
→ risk
```

Determine whether risk is decoded from latent state or analytically computed from predicted geometry.

## 8. Planning interface

Determine whether risk/world output is actually consumed by:

```text
trajectory generator
candidate scorer
MPC/search
policy conditioning
or no planner at all
```

If absent, write `PLANNING INTERFACE = ABSENT` rather than extrapolating a use case.

## 9. Supervision truth

Audit:

```text
factual logged future
risk labels
collision labels
near-miss/TTC/RSS-style labels
synthetic/simulator targets
alternative-action future truth
reactive surrounding-agent truth
```

## 10. Strongest matched ablations

Prioritize controls isolating:

```text
object-centric vs scene-global representation
dynamics rollout vs no rollout
risk decoder / risk supervision
prediction horizon
action conditioning if present
```

Do not use headline metric gains as a monolithic `world-model gain`.

## 11. Evaluation regime

Classify separately:

```text
risk prediction evaluation
future prediction evaluation
open-loop planning evaluation
NAVSIM pseudo-simulation
reactive closed loop
```

Do not treat risk-classification accuracy as planning validation.

## 12. Full Ontology V1.3 projection

Force-fill A–P with explicit absence/status values.

Any proposed V1.4 dimension must survive merge testing and back-projection.

---

# Required immediate comparisons

```text
RiskWorld vs SafeDrive
RiskWorld vs GraphWorld
RiskWorld vs WoTE
RiskWorld vs DA-WAM
RiskWorld vs LAW / World4Drive
```

Especially answer:

```text
SafeDrive: safety is evaluator semantics attached to candidate sparse worlds.
RiskWorld: is risk actually part of the predicted world state?

GraphWorld: structured interaction latent conditions policy.
RiskWorld: does structured/object latent instead decode risk?

WoTE/DA-WAM: future helps choose an ego candidate.
RiskWorld: is there any comparable decision interface at all?
```

---

# Required artifacts

Create at minimum:

```text
papers/deep_analysis/P0005_RISKWORLD_DEEP_ANALYSIS_V2.md
audits/literature/PHASE_C6_RISKWORLD_AUDIT.md
landscape/P0005_RISKWORLD_ONTOLOGY_PROJECTION.md
landscape/WAM_COMPARISON_MATRIX_V1_3_RISKWORLD_EXTENSION.md
```

Update state/queue/source completeness only after mechanism is stable.

---

# After RiskWorld

```text
P0007 DriveReward
```

Then proceed to simulation/reactivity/evaluation controls and WAM+VLA boundary controls.

---

# Guardrail

This remains field reconstruction / literature expansion.

Do not turn SafeDrive or RiskWorld into a project research direction.
