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

Runtime role:
runtime decision / training improvement / representation transfer / simulation / generation only

World dependency type:
none / training-only predictive / online predictive state / online rollout / candidate-conditioned consequence / joint generation

Action commitment relation:
before world / after world / through world / independent / unknown
```

## D01.1 field semantics

The three fields in the identity block are mandatory for every artifact or mode at RD2+. They are artifact-level descriptors, not paper-level adjectives. If one paper contains multiple terminal products or lifecycle roles, create separate artifact records before assigning these fields.

`Runtime role` answers what the artifact is doing in the system being audited:

| value | use when |
|---|---|
| `runtime decision` | the artifact's predictive/world operation is part of the deployed action, trajectory, candidate resolver, or policy decision path |
| `training improvement` | the predictive/world operation primarily supplies imagined experience, reward/return, policy updates, or action-learning supervision and is not required by the final deployed action path |
| `representation transfer` | a predictive objective or model produces parameters/features transferred into a planner, while the predictive operation itself is not required at deployment |
| `simulation` | the artifact's terminal product is an environment/world response used to evaluate or train another policy, rather than the policy's own final action |
| `generation only` | the artifact generates future scenes, frames, states, or trajectories as its terminal product, without an evidenced final action commitment in that mode |

`World dependency type` records the strongest separately traceable predictive/world operation on the artifact path:

| value | use when |
|---|---|
| `none` | no separately traceable predictive/world operation affects the artifact; ordinary encoding or direct action denoising is insufficient |
| `training-only predictive` | future/state prediction exists only as a pretraining, auxiliary, target, or co-training operation and is removed/bypassed before deployment |
| `online predictive state` | a predicted or updated world/state object is retained online and conditions action formation without explicit candidate-specific consequence branches |
| `online rollout` | a runtime or training-time action-conditioned transition is iterated over a horizon to obtain imagined states, rewards, or policy-learning returns |
| `candidate-conditioned consequence` | separately identified candidate actions/trajectories index predicted consequences that are consumed by a common evaluation, optimization, or commitment step |
| `joint generation` | ego action/trajectory and other world entities are generated in one coupled future object, with the generated joint object itself serving as the artifact's operative world interface |

Use the first value that describes the artifact's decisive world dependency. Do not upgrade `training-only predictive` to an online value because a decoder or target branch exists in the training graph. Do not use `joint generation` for an ordinary action distribution unless other world entities or future scene variables are jointly generated.

`Action commitment relation` records where the terminal action becomes committed relative to the world operation named above:

| value | use when |
|---|---|
| `before world` | the terminal action/trajectory is committed before the predictive/world operation begins; the later world output is diagnostic, auxiliary, or post-hoc |
| `after world` | a world/state/future or candidate consequence is materialized first and the final action/trajectory is then selected, decoded, or optimized from it |
| `through world` | action and world are jointly or iteratively updated, or the action/policy is learned through world-mediated transitions/returns such that neither side is a simple preceding auxiliary |
| `independent` | the final action path does not depend on the separately described world operation, including a deployment action path after a training-only predictive branch is removed |
| `unknown` | the source does not resolve the order or causal dependence |

For `training improvement`, interpret this field at the operative training mechanism and add the deployment residue in Sections 8–9. For `representation transfer`, the default deployment relation is usually `independent`; use `through world` only when the transferred representation is still updated jointly with the action path in the audited artifact. For `simulation` and `generation only`, write `not applicable` in the terminal-action sentence and use `unknown` only if the artifact also claims an action path whose relation is unresolved.

These fields do not replace the detailed DAG, lifecycle, future-construction, action-formation, learning, deployment-residue, or evidence sections below. They are a compact routing layer that prevents training-time prediction, representation transfer, online world use, simulation, and generation-only outputs from being counted as the same mechanism.

### D01.1 recording rule

Record exactly one controlled value for each field per artifact. If two values appear necessary, the artifact split is probably too coarse. Preserve the tension in `Unknowns` or the evidence ledger rather than inventing a compound value. A paper-level summary may list several artifact records, but must not collapse them into one paper-level value.

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
