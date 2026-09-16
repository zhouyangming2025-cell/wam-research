# Ontology-Free Mechanism Record Template

Use this template before assigning any project ontology codes.

## A. Identity

```text
paper:
version/date:
artifact/mode:
implementation boundary:
reading depth: RD0/RD1/RD2/RD3/RD4
sources:
```

## B. Declared task

What is the terminal task in this artifact?

```text
action / control
trajectory
candidate selection
policy learning
world generation
simulation
value / reward prediction
representation pretraining
other
```

State the terminal output exactly.

## C. Online inputs

List only information available in the scoped runtime route.

```text
current observation
history
current explicit state
route / command / goal
ego state
candidate action / trajectory
previous-cycle state/action
external control
other
```

## D. Explicit computational objects

For every independently traceable object, record:

```text
object id / notation:
semantic referent:
current / future / timeless / unknown:
physical-time index if any:
entity structure if any:
action/control indexed? how?
learned or supplied?
runtime lifecycle: train-only / runtime / both
```

Do not call an object a world state merely because it is a feature tensor.

## E. Dynamics / transformation operators

For each edge/operator:

```text
input objects
control/action inputs
output objects
operator role:
  encoding
  filtering / belief update
  transition
  temporal prediction
  generation
  relational update
  rollout
  reward/value prediction
  scoring
  policy/action generation
  search/optimization
physical-time advance? yes/no
repeated online? yes/no
```

## F. Future construction

Does the artifact construct a future object online?

```text
none
internal predictive hidden state only
single future endpoint
multi-step sequence
branching/tree future
joint future world-action object
unknown
```

For each future object:

```text
what time does it refer to?
does candidate identity survive into it?
is it factual, sampled, predicted, counterfactual or surrogate?
does the planner/action module consume it?
```

## G. Action formation

Describe exactly how an action/trajectory is formed.

```text
direct decode
hierarchical semantic decision → action
sampling without final common resolver
candidate proposal bank
continuous action-sequence optimization
planning/search tree
policy distribution
joint world-action generation
external action/control supplied
```

Do not infer commitment from the existence of multiple outputs.

## H. Commitment / search / optimization

If one action is eventually executed, record:

```text
what alternatives exist?
where are identities preserved?
what operation compares/optimizes them?
is comparison explicit or implicit?
what determines the final action?
is there resampling/refinement after selection?
is there replanning/search before commitment?
```

## I. Decision criterion

Record target semantics separately from measure and implementation.

```text
semantic target:
  expert/factual compatibility
  reward / return
  value
  task utility
  safety / collision
  comfort / progress / rules
  future fidelity
  physical/dynamics validity
  model likelihood/confidence
  goal achievement
  other
  unknown

compared objects:
target provenance:
measure/loss:
composition / weighting / lexicographic order:
```

## J. Training program

Write stages in causal order.

For each stage:

```text
inputs
predicted objects
targets
losses
which parameters receive gradient
frozen / stop-gradient components
teacher / target networks
data source: logged / simulation / generated / preference / RL
```

Then record:

```text
retain at deployment:
drop at deployment:
bypass in this mode:
distilled into:
```

## K. Online clocks

Record separately:

```text
numerical solver/edit iterations
world↔policy reciprocal iterations within one decision
modeled physical-future horizon
search-tree depth / branching
cross-control-cycle dependency
real environment interaction loop
```

Counts are evidence attributes, not automatically mechanism categories.

## L. Uncertainty / branching

```text
deterministic vs stochastic state transition
single mode vs multimodal future
aleatoric uncertainty explicit?
epistemic/model uncertainty explicit?
branching used by decision or only generation?
```

This field is intentionally recorded before deciding whether uncertainty deserves its own ontology axis.

## M. Evidence boundary

Separate:

### PRIMARY FACT

### CODE FACT

### AUTHOR CLAIM

### OUR INFERENCE

### UNKNOWN

## N. Minimal causal graph

Write the artifact as a typed DAG / loop without ontology codes.

Example syntax:

```text
O_t → state_t
state_t, A{k} → future{k}
future{k} → score{k}
argmax_k score{k} → A*
```

or

```text
O_t → s_t
search:
  (s,a) → (r,s') repeated in tree
  leaf value + backed-up return → root action
```

## O. Deletion / substitution tests

Test the artifact by removing or replacing one component:

```text
remove future object: does action mechanism change?
replace RGB with latent/BEV: does mechanism change?
replace heavy generator with semantic-equivalent surrogate: does mechanism change?
remove resolver: is final commitment still defined?
remove online model but keep trained policy: what mechanism remains?
change solver step count: mechanism or parameter only?
```

## P. Candidate ontology projection — AFTER FREEZE ONLY

This section is intentionally last.

For every candidate ontology version:

```text
projection:
information lost:
ambiguous boundary:
collision with another artifact:
category pressure / proposed revision:
```

Never edit the ontology-free sections merely to make a projection cleaner.
