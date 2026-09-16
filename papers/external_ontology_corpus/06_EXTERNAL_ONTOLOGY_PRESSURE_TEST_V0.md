# External Ontology Pressure Test V0

Status: **provisional external verdict, not a replacement ontology**.

Evidence base in this pass:

- existing repository field census and RD3/RD4 driving mechanism evidence;
- external foundational mechanisms including Dyna, VPN, TreeQN, World Models, PlaNet, Dreamer, MuZero and TD-MPC/TD-MPC2;
- recent survey/index evidence spanning general world models, Physical AI, robotics and autonomous driving;
- strong non-WM planning controls.

The frozen 12-paper ontology is not modified by this document.

---

# 1. Executive result

The broad-literature pass changes the confidence distribution across the current human axes.

| candidate axis | V0 external verdict | main reason |
|---|---|---|
| `R` output formation / commitment | **MODIFY / likely SPLIT or expand** | online MPC, MCTS, differentiable lookahead and iterative trajectory optimization are major mechanism families missing from the current driving-derived R codebook |
| `W` online world role | **KEEP + MODIFY** | deployment-time model/world use is strongly validated from Dyna→PlaNet/MuZero; categories need cleaner mechanism definitions and joint `W5` should be removed from human layer |
| `E` semantic criterion | **KEEP + BROADEN** | criterion/objective matters across candidate resolution and search, but `resolver criterion` is too narrow for return/value/Q-based online planning |
| `L` learning route | **KEEP + strengthen ordered-program requirement** | Dyna, Dreamer, predictive pretraining and distillation independently validate learning/deployment-route distinctions |

The external evidence also raises two possible missing questions:

```text
I? = interaction / intervention / reactivity semantics
U? = uncertainty / branching semantics
```

Neither is promoted yet. They require independence tests against W, X/control binding, T/clocks, evaluation regime and R/search topology.

---

# 2. W axis — strongest surviving human axis after external pressure

## 2.1 Necessary question

The externally stable question is:

> **During deployment, what explicit predictive/model-side world object, if any, lies on the causal path of the scoped output/decision?**

This is more robust than the project-specific phrase `world carrier`.

Dyna proves that model knowledge may shape learning while execution remains reactive. PlaNet/MuZero/TD-MPC2 prove that learned model objects may instead be actively used in online deliberation.

Therefore the top split is stable:

```text
no online model/world object
vs
online model/world object used
```

## 2.2 Proposed human W revision

```text
W0  no explicit online predictive/model world object
W1  current dynamical model state / belief-like state
W2  predictive/generative internal state directly consumed before explicit future materialization
W3  explicit single future consequence / endpoint
W4  explicit multi-step or branching future rollout structure
WU  unresolved
```

### W0

World knowledge may exist in parameters, encoder, scorer, value or policy; train-time world models may have been used. The scoped runtime decision route does not materialize an explicit predictive/model world object.

External support: Dyna execution.
Driving support: LAW runtime, Drive-JEPA, DynFlowDrive, Epona planning mode.

### W1

An explicit current model state represents the system's current belief/dynamical state and is maintained/grounded by temporal or dynamical operations.

External support: recurrent state-space / belief-state lineages, Dreamer current model state.
Driving support: GraphWorld.

Important revision: delete the word `structured` from the essential definition. Graph structure is one realization, not the category.

### W2

The policy consumes an internal state of a predictive/generative process that already carries anticipatory dynamics, but the runtime route does not explicitly materialize a time-indexed future endpoint/horizon before action formation.

External support: Ha & Schmidhuber predictive RNN hidden state.
Driving support: DriveLaW Video-DiT hidden state.

This category survives an external non-driving exemplar and is therefore not merely DriveLaW-specific.

### W3

A separately identifiable future consequence corresponding to a specific future time/endpoint is materialized and used/returned.

Driving exemplars: World4Drive, WorldDrive surrogate, SeerDrive future endpoint.
Potential external analogues: one-step model-state consequence interfaces.

### W4

A multi-step, horizon, tree or branching future structure is explicitly constructed online.

External exemplars: VPN rollout, TreeQN tree, PlaNet latent horizon, MuZero MCTS, TD-MPC2 trajectory rollout.
Driving exemplars: WoTE horizon, Epona world rollout, Drive-WM imagined future video sequence.

Revision: `sequence` is too narrow; tree/branching rollout must fit.

## 2.3 Delete human W5

Current `W5 = joint world-action carrier` should not remain a primary W class if `R/D` already encode joint world-action coupling.

Reason:

```text
jointness = relation/coupling between action and world variables
future temporal role = what the W question should encode
```

A joint future world-action sequence can therefore be:

```text
R_joint + W4
```

rather than duplicating `joint` in both axes.

Keep `C5` or equivalent detailed graph type in the audit backend if useful; delete its mechanical one-to-one projection into human W.

## 2.4 Revised admission gate

A runtime object should count as W1–W4 only if all are supported:

```text
G1 identity
  independently traceable object/state exists

G2 predictive/dynamical role
  beyond ordinary encoding, it participates in filtering/belief update,
  transition, temporal prediction, relational dynamics, generation,
  reward/value-predictive dynamics or world-state transport

G3 decision-relevant predictive grounding
  training/teacher evidence constrains temporally indexed consequences
  or planning-relevant dynamics; full observation reconstruction is NOT required

G4 scoped runtime interface
  the object lies on the runtime route to the declared decision/output
```

This revised gate admits VPN/MuZero/TD-MPC2 while still rejecting generic CNN/BEV features.

## 2.5 W verdict

```text
W = KEEP + MODIFY
confidence after V0 = medium-high
```

Main unresolved issue: W1 versus W2 boundary requires more recurrent-state / hidden-state / JEPA / robotics anchors before freeze.

---

# 3. R axis — major external failure discovered

## 3.1 Current R question remains useful

> How is the action/output formed and, where alternatives exist, committed?

This question is independently important.

## 3.2 Current category set is incomplete

The current R set was induced from a driving sample dominated by direct policies, candidate banks and joint generation. External canonical methods expose at least one missing family:

```text
ONLINE SEARCH / OPTIMIZATION OVER A LEARNED MODEL
```

Examples:

- PlaNet: iterative CEM optimization of action-sequence distribution using latent rollouts;
- MuZero: MCTS with recursive latent model expansion and backup;
- TreeQN: differentiable recursive lookahead tree;
- TD-MPC2: local trajectory optimization in latent world model;
- VPN: multi-step abstract rollout and lookahead evaluation.

These should not be forced into current `RB` because:

- alternatives may be generated/resampled iteratively rather than born as a stable explicit bank;
- tree nodes/actions have search semantics rather than final proposal identity;
- continuous optimization need not preserve finite candidate identities;
- backup/optimization may repeatedly change search support before root commitment.

They should not be forced into `R0` because doing so would erase the central online deliberation mechanism.

## 3.3 Candidate repair hypotheses

Do not freeze yet. Test at least two designs.

### Hypothesis R-A — add one search/optimization class

```text
RO = online model-based search / optimization before commitment
```

Admission examples:

```text
CEM/MPC
MCTS
learned differentiable tree backup
iterative action-sequence optimization
```

Potential weakness: MCTS and continuous MPC may still be too different to compress into one human class.

### Hypothesis R-B — factor R into two subquestions

```text
R_form = direct / semantic hierarchy / generative policy / joint world-action ...
R_commit = none / finite-bank resolver / iterative optimization / tree search / reciprocal revision ...
```

Potential strength: cleaner compositionality.
Potential weakness: human signature grows and may duplicate D/P backend fields.

External corpus should decide rather than guessing now.

## 3.4 R verdict

```text
R = NECESSARY QUESTION
current codebook = INCOMPLETE
status = MODIFY, possibly SPLIT
severity = HIGH
```

---

# 4. E axis — useful semantics, wrong scope wording

## 4.1 What survives

There is clearly an independent question:

> **What semantic objective makes an action/search branch preferable?**

Different systems optimize:

```text
expert compatibility
world/future fidelity
task utility / return
reward
value / Q
safety / collision
comfort / progress / rule compliance
physical validity
likelihood/confidence
goal achievement
preference
```

These differences matter even when the architecture/scalar-head shape is identical.

## 4.2 What fails

`resolver criterion` is too narrow.

PlaNet, MuZero, TreeQN, VPN and TD-MPC2 contain decision criteria inside online search/optimization without necessarily instantiating the driving-specific explicit resolver topology.

Therefore E should likely be reframed as:

> **decision objective / commitment criterion semantics**

rather than criterion of a separately typed resolver only.

## 4.3 Semantic representation proposal

Continue separating:

```text
semantic target
compared/optimized objects
target provenance
measure
composition / backup / weighting
```

Potential semantic atoms to test:

```text
expert/factual compatibility
world/predictive fidelity
holistic task utility / return
value / Q / expected return
factorized outcome terms: safety, rules, comfort, progress...
physical/dynamics validity
likelihood/confidence
goal/constraint satisfaction
preference
```

Question for further audit: `value/Q/return` may be implementation/composition of holistic utility rather than a new atom. Do not split prematurely.

## 4.4 E verdict

```text
E question = KEEP
scope/grammar = MODIFY
confidence = medium-high
```

---

# 5. L axis — strongly validated, but human representation must remain directed

Cross-domain evidence supports the necessity of distinguishing how world knowledge reaches deployed behavior:

```text
Dyna:
model → simulated planning updates → value/policy → reactive execution

Dreamer:
world model → imagined trajectories → actor/value learning → deployed actor/current state

predictive pretraining:
future objective → encoder transfer → deployed planner

LAW:
predicted action → future prediction loss → shared/planner updates → future branch dropped

WorldDrive:
world generator teacher → representation transfer + future-state surrogate distillation → online surrogate

DynFlowDrive:
train-time world criterion → scorer supervision → world model removed
```

An unordered label set would collapse materially different routes.

## L verdict

```text
L = KEEP
ordered directed program + retain/drop fate = mandatory
family macros = optional compression only
confidence = high
```

---

# 6. Interaction / reactivity — possible missing dimension

Recent driving work and older interactive-prediction literature expose another question:

> If ego action changes, does the modeled environment response change in a behaviorally/causally meaningful way?

Possible states include:

```text
factual replay / no reaction
open-loop conditional prediction
candidate-conditioned but independent/non-reactive response
influencer→reactor conditional response
joint interaction model
reactive simulator agents
learned closed-loop world agents
strategic/game-theoretic response
unknown
```

This distinction is not obviously reducible to W:

- two systems can both be W4 rollouts but one replays logged actors while another predicts reactions to ego deviations.

It is not obviously reducible to X/control either:

- action conditioning can exist without behaviorally correct intervention response.

However, it may partly belong to **world-model validity/evaluation**, not core planning mechanism.

### Status

```text
I-axis hypothesis = OPEN
promotion forbidden until independence test across M2I, GameFormer, Drive-WM,
reactive simulators, CausalDrive and non-reactive log replay
```

---

# 7. Uncertainty / stochastic branching — possible missing dimension

Questions:

```text
Does the model represent multiple possible futures?
Is uncertainty aleatoric, epistemic or merely sampling diversity?
Does the decision rule consume uncertainty, or only point predictions?
Does branching affect safety/utility commitment?
```

W4 can already represent a branching rollout structure, but it does not say whether probabilities/uncertainty semantics matter to decision.

Risk-sensitive MPC and probabilistic model-based control may force a separate dimension or criterion attribute.

### Status

```text
U-axis hypothesis = OPEN
needs PILCO / probabilistic ensembles / risk-sensitive MPC / stochastic world-model anchors
```

---

# 8. Relationship to detailed C–X–D–P–V–T–L backend

The external pass does not yet justify deleting the detailed backend. Instead it suggests:

- `C` should be reframed as model/world object semantics with a broader predictive-grounding gate;
- `D` remains useful for runtime world→decision causal route;
- `P` must be tested against search/MPC/MCTS rather than only semantic hierarchy and finite candidate banks;
- `V` needs the same broadening as E;
- `T` may need explicit search-tree depth/optimizer iteration as audit parameters, while keeping distinct physical horizon and control-cycle clocks;
- `L` is strongly supported.

The current backend remains a hypothesis until the external corpus grows.

---

# 9. Candidate human ontology V0.1 — for testing only

Do **not** promote this to normative files.

```text
Artifact = R? + W? + E? ⊕ L[...]
```

with:

```text
W0 no online predictive/model world object
W1 current dynamical model state
W2 predictive/generative internal state consumed directly
W3 explicit single future consequence
W4 explicit multi-step/branching rollout
WU unresolved
```

R and E are deliberately left unfrozen pending search/MPC pressure tests.

This asymmetry is intentional: do not freeze the whole signature because one axis currently looks stable.

---

# 10. Next decisive reading waves

## Wave F1 — R search/optimization adjudication

Deep read:

```text
PlaNet
MuZero
TreeQN
VPN
TD-MPC2
one classical MPC-with-learned-dynamics paper
one sampling-based model-predictive policy paper
```

Question: one `online deliberation` class or split tree-search versus iterative optimization?

## Wave F2 — W1/W2 boundary adjudication

Deep read:

```text
World Models
DreamerV1/V3
V-JEPA 2 action-conditioned variant
GraphWorld
DriveLaW
one belief-state/POMDP neural model
one robotics recurrent WM
```

Question: can current model state and predictive hidden state be mechanically separated without architecture-specific language?

## Wave F3 — interaction/reactivity independence

Deep read:

```text
M2I
GameFormer
BeTop
Drive-WM
ReactSim-Bench
CausalDrive
one non-reactive log-replay benchmark
```

Question: core mechanism axis, world-validity axis, or evaluation attribute?

## Wave F4 — uncertainty/risk independence

Deep read probabilistic/risk-sensitive model-based planners and recent safety WMs.

---

# 11. V0 conclusion

The broad-literature program is already scientifically useful because it produced a nontrivial result rather than merely validating the current ontology:

```text
W: survives but needs cleanup
R: current categories fail external completeness
E: semantics survive but scope is too resolver-specific
L: strongly survives
interaction/reactivity: plausible missing question
uncertainty: plausible missing question
```

This is exactly the behavior expected from an independent ontology audit.
