# ONTOLOGY-FREE MECHANISM CARD V2

Use this template for RD2+ WAM + one-stage artifacts before any ontology projection.

The purpose is to reconstruct the mechanism without forcing it into R/W/E/L or C/X/D/P/V/T/L.

---

# 0. Identity

```text
Paper:
Version/date:
Venue/status:
Code repo/commit if audited:
Artifact ID:
Mode/task path:
Evidence tier: Tier 1 / Tier 2 / Tier 3
Reading depth: RD0 / RD1 / RD2 / RD3 / RD4
```

## Scope decision

```text
IN-DOMAIN / BOUNDARY / THEORY-SUPPORT / EXCLUDE
```

Reason in one paragraph.

---

# 1. Problem and deployed output

What deployed problem does this artifact solve?

```text
Input:
Terminal deployed output:
Planning/action output type:
Deployment environment/evaluation mode:
```

Do not describe training objectives yet.

---

# 2. Mechanism DAG

Draw the deployed causal route first.

Example syntax only:

```text
observation/history
  -> current representation/state
  -> optional future/world operation
  -> action/proposal/search process
  -> optional criterion/value
  -> terminal action/trajectory
```

Then draw the training route separately.

Never merge train-time-only branches into the runtime graph.

---

# 3. State/object ledger

For every separately traceable object:

| object | lifecycle | semantic role claimed by authors | how constructed | temporal referent | consumed by | evidence |
|---|---|---|---|---|---|---|

Possible lifecycle labels:

```text
TRAIN_ONLY
RUNTIME
BOTH
TARGET_ONLY
TEACHER_ONLY
```

Do not call something a world state merely because scene information can be decoded from it.

---

# 4. Dynamics / predictive operation

Record every operation that goes beyond ordinary encoding:

```text
action-conditioned transition
temporal prediction
future latent prediction
video/occupancy/BEV generation
state transport/update
relational temporal update
rollout
search-tree expansion
iterative world-policy update
other
```

For each:

```text
input objects:
conditioning variables:
output object:
number/type of time steps:
training/runtime/both:
```

---

# 5. Future construction

Does the artifact construct any future/consequence object?

If yes, record:

```text
explicit future time index?
single endpoint / sequence / branching tree / internal predictive hidden / other?
candidate-specific?
ego-action-conditioned?
other-agent response conditioned on ego action?
factual/teacher future or counterfactual/generated future?
materialized at deployment or training only?
```

If no, say explicitly `NO MATERIALIZED FUTURE OBJECT`.

---

# 6. Action formation

Describe how the terminal action/trajectory comes into existence without taxonomy labels.

Possible observed mechanisms include, but are not limited to:

```text
direct decoder/policy
semantic intent -> action
explicit proposal/candidate bank
iterative trajectory refinement
sampling without common resolver
search/tree expansion
MPC/trajectory optimization
world-policy reciprocal updates
joint/interleaved world-action generation
retrieval + ranking
other
```

For candidate/search systems record:

```text
candidate birth
identity preservation
prefiltering
scoring/evaluation
selection/commitment
post-selection refinement
whether refinement is rescored/re-enters search
```

---

# 7. Decision objective / criterion

What causes one action/path/search branch to be preferred over another?

Record semantics, not only scalar-head architecture.

```text
expert/factual compatibility
task utility
reward/return/value/Q
safety/collision/drivability
progress/comfort/rules
world/future agreement
physical/dynamics validity
likelihood/confidence
learned preference
hybrid composition
unknown
```

Also record:

```text
compared objects:
target/provenance:
measure/model:
weights/order/filter:
where in the decision process the criterion acts:
```

If no explicit decision objective is used at runtime, say so.

---

# 8. Learning-to-deployment program

Write the directed training program in chronological order.

Example grammar:

```text
stage A -> stage B -> joint(stage C, stage D)
=> retain{...}
=> drop{...}
=> bypass{...}
=> freeze{...}
```

For every important loss/teacher:

```text
source/target
what parameters receive gradient
stop-gradient/detach/frozen boundaries
whether the trained component survives deployment
```

---

# 9. Deployment residue

At runtime, list explicitly:

```text
RETAINED:
DROPPED:
BYPASSED:
FROZEN BUT ACTIVE:
DISTILLED INTO:
```

This section is mandatory because two methods can share training but differ completely at deployment.

---

# 10. Clock / iteration ledger

Record each independently meaningful repetition:

```text
physical future horizon
solver/diffusion/flow iterations
world<->policy reciprocal rounds
search depth/tree depth
MPC optimization rounds
previous-control-cycle reference
recurrent memory update
```

Do not confuse numerical step count with a topological mechanism class.

---

# 11. Uncertainty / branching

Record whether the method represents:

```text
single deterministic future
stochastic future distribution
multiple intention modes
candidate-indexed worlds
branching tree
ensemble/distributional value
uncertainty used for action choice
uncertainty predicted but ignored by planner
```

No ontology conclusion yet.

---

# 12. Interaction / intervention / reactivity

Record separately:

```text
Is future conditioned on ego action?
Do other agents/world variables respond to ego intervention?
Is the response factual/log replay, learned conditional response, rule response, or closed-loop simulation?
Does the decision mechanism actually consume that reactive response?
Is counterfactual validity empirically evaluated?
```

Do not infer behavioral causality from generic action conditioning.

---

# 13. Evidence ledger

For every decision-critical claim:

| claim | evidence type | source location | confidence | unresolved ambiguity |
|---|---|---|---|---|

Evidence type:

```text
PAPER FACT
CODE FACT
AUTHOR CLAIM
OUR INFERENCE
UNKNOWN
```

---

# 14. Counterfactual deletion tests

Ask what happens if each component is removed while preserving the rest:

```text
remove future/world branch
remove candidate scorer
remove future decoder but retain latent trunk
replace heavy generator with distilled surrogate
remove post-selection refinement
remove prefilter
remove world loss after pretraining
remove search and use policy prior directly
```

For each test state whether it changes:

```text
runtime causal topology
semantic decision objective
world/predictive role
action-formation mechanism
learning route only
implementation only
```

These may be analytical counterfactuals; mark them `OUR INFERENCE` unless experimentally tested.

---

# 15. Implementation-invariance probes

Would the core mechanism remain the same under:

```text
RGB <-> BEV <-> latent representation swap
Transformer <-> diffusion/flow implementation swap
5 -> 10 solver steps
heavy teacher -> compact surrogate with same semantic state/output
candidate count change
backbone scale change
```

Explain which changes are mechanistic versus implementation-level.

---

# 16. Closest contrast artifacts

List 2–5 papers/artifacts that are maximally useful for distinguishing this mechanism.

For each, state the exact edge/object difference.

---

# 17. Unknowns

List unresolved questions explicitly.

Unknown is preferred over ontology-forcing speculation.

---

# 18. Projection lock

Do not fill ontology labels here during initial extraction.

After the ontology-free card is reviewed, a separate projection record may map the artifact to candidate axes.
