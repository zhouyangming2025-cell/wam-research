# NEXT_TASK

## 唯一下一任务

> **Deep-read P0002 SafeDrive as the third paper in Wave C.6, using the existing WAM reading stack. Keep research-direction convergence paused.**

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
13 anchors complete
DriveLaW = COMPLETE
DA-WAM   = COMPLETE
SafeDrive = NEXT
```

---

# Why SafeDrive is next

SafeDrive is selected for coverage diversity, not because it supports a preferred research hypothesis.

It introduces a different world/planning interface:

```text
trajectory-conditioned sparse world representation
→ explicit agent/timestep future interaction states
→ fine-grained safety reasoning
→ planning decision
```

This is materially different from:

```text
WoTE       recurrent BEV consequence + utility
World4Drive compact candidate future + factual-mode score
GraphWorld  structured interaction state + direct policy
DA-WAM      candidate-specific latent + factorized utility scorer
RiskWorld   object-centric risk prediction boundary anchor
```

SafeDrive therefore pressure-tests whether explicit structured safety/world states add scientific distinctions not captured by implicit latent consequence features.

---

# Mandatory reconstruction

## 1. Source/version boundary

Resolve:

```text
canonical paper version
official repository / project page
code-release state
paper↔code version relation
```

Lock a commit if code exists.

## 2. Host planner first

Reconstruct before the world model:

```text
observation
→ planner representation
→ ego trajectory / candidate trajectories
```

Determine whether SafeDrive is:

```text
direct policy
candidate bank + scorer
trajectory refinement
or hybrid
```

## 3. Sparse world representation

Trace exactly what `sparse world` means:

```text
object / agent tokens?
map elements?
BEV points?
future occupancy?
interaction states?
```

Record:

```text
state granularity
agent identity persistence
map representation
future-time indexing
```

Do not use `world state` as a generic label.

## 4. Action / trajectory → world coupling

For every predicted future object, determine:

```text
what ego trajectory/action conditions the predictor?
how is the action injected?
are multiple candidate actions predicted separately?
are parameters shared across branches?
```

Mandatory counterfactual distinction:

```text
candidate-specific output?
candidate-specific factual future target?
reactive surrounding-agent truth?
```

## 5. Agent/timestep future prediction

Reconstruct:

```text
current agent state
+ ego trajectory
→ future agent/world states
```

Determine:

```text
prediction horizon
physical timestep
single endpoint vs sequence
which agents are modeled
whether future states are geometric, semantic, occupancy, latent, or mixed
```

Use F04/F05/F07/F08.

## 6. Explicit safety reasoning

Trace every safety variable separately:

```text
collision
road/drivable-area compliance
TTC / distance margin
agent interaction risk
other rule constraints
```

For each, answer:

```text
predicted world state?
hand-computed evaluator?
learned safety head?
reward/value target?
training-only label?
online decision variable?
```

Do not collapse all of these into `risk`.

## 7. World → planning interface

Determine whether SafeDrive uses future/world information to:

```text
condition a direct planner
score candidates
refine trajectories
reject unsafe proposals
or supervise training only
```

Draw separate training and inference graphs.

## 8. Supervision truth

For each future agent/world branch, identify:

```text
logged factual future
simulator future
pseudo-label
rule-derived target
expert trajectory
hard-negative target
```

If multiple ego candidates exist, explicitly test whether one factual environment future is reused across candidates.

## 9. Strongest matched ablations

Prioritize controls isolating:

```text
base planner
+ sparse world modeling
+ action conditioning
+ safety module
+ fine-grained agent/timestep reasoning
```

Separate representation gain from safety-evaluator gain.

## 10. Evaluation regime

Classify each result as:

```text
open-loop
NAVSIM non-reactive pseudo-simulation
reactive simulator closed-loop
real-car closed-loop
```

Do not use the paper's label without auditing benchmark semantics.

## 11. Full Ontology V1.3 projection

Force-fill A–P with explicit:

```text
ABSENT
NOT REPORTED
NOT EVALUATED
NOT APPLICABLE
SOURCE-UNVERIFIED
```

Any proposed new dimension must survive merge testing and back-projection across prior anchors.

---

# Required immediate cross-paper comparisons

```text
SafeDrive vs WoTE
SafeDrive vs DA-WAM
SafeDrive vs GraphWorld
SafeDrive vs World4Drive
SafeDrive vs RiskWorld
```

Key questions:

```text
Is SafeDrive's `safety` an explicit world variable, a value function, or a rule evaluator?
Does it model other-agent response or only factual/logged motion?
Does agent/timestep structure add more than an implicit latent future?
Is safety gain attributable to world prediction or to explicit metric supervision?
```

---

# Required artifacts

After the deep read create at minimum:

```text
papers/deep_analysis/P0002_SAFEDRIVE_DEEP_ANALYSIS_V2.md
audits/literature/PHASE_C6_SAFEDRIVE_AUDIT.md
landscape/P0002_SAFEDRIVE_ONTOLOGY_PROJECTION.md
landscape/WAM_COMPARISON_MATRIX_V1_3_SAFEDRIVE_EXTENSION.md
```

Update state/queue only after mechanism and evidence are stable.

---

# After SafeDrive

Current core queue:

```text
P0005 RiskWorld
P0007 DriveReward
```

Then proceed into simulation/reactivity/evaluation and WAM+VLA control waves.

---

# Guardrail

This remains literature expansion.

Do not turn SafeDrive/DA-WAM into a project research direction.

The question remains:

```text
What mechanisms actually exist in the field,
how are they supervised,
how are they deployed,
and what evidence isolates their contribution?
```
