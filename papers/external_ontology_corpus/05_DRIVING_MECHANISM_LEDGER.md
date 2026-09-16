# Driving / Embodied Mechanism Ledger

Status: cross-links the repository's existing driving evidence with the external ontology-audit track. It does not replace existing paper cards or deep analyses.

## 1. Why this ledger exists

The repository already contains substantial RD3/RD4 evidence for planning-centric driving world models. This file extracts only the mechanism facts needed for cross-domain ontology pressure testing.

## 2. Training-only / compiled-world routes

### LAW

```text
current visual latent
→ direct waypoint planner
→ predicted trajectory
→ train-time future-latent predictor
→ future-latent loss updates shared/planning path

runtime:
current latent → planner → trajectory
future predictor dropped
```

Pressure:

- world knowledge can improve a deployed policy without an online future object;
- current encoder feature should not automatically become a model/world state merely because it contains scene information;
- supports separation of runtime world role from learning route.

### Drive-JEPA PF / PB

```text
video predictive pretraining
→ encoder representation
→ downstream direct planner or proposal/scorer

runtime future predictor/target network absent
```

Pressure:

- predictive representation transfer and online predictive-state use are different;
- PB variants prove candidate resolution does not imply online world consequence.

### DynFlowDrive

```text
train-time candidate/world-flow criterion
→ winner / supervision for proposal-scorer
→ deploy proposal + scorer
world-flow module removed
```

Pressure:

- teacher/criterion distillation can delete the future state itself;
- contrasts directly with WorldDrive, where a surrogate future state remains online.

## 3. Current-state route

### GraphWorld

```text
history / perception
→ ego-centric interaction structure
→ explicit current latent world state
→ world-state-conditioned planning
→ multimodal plan
```

Pressure:

- useful example of a current dynamical/relational model state rather than ordinary BEV feature;
- `structured` is implementation-specific; the deeper role is current model state with temporal/relational grounding;
- final commitment remains evidence-bounded, proving world-state role and action-commitment topology are independent questions.

## 4. Predictive internal-state route

### DriveLaW

```text
historical observation
→ Video-DiT generative process
→ intermediate predictive/generative hidden states
→ Action-DiT
→ trajectory
```

Full future video decoding is unnecessary for planning.

Pressure:

- strong independent driving counterpart to Ha & Schmidhuber's predictive RNN-hidden-state controller interface;
- supports a distinct category for `predictive/generative internal state consumed directly by policy`;
- implementation is not the category: Video-DiT hidden versus RNN hidden can be mechanism-family analogous.

## 5. Single-future-consequence routes

### World4Drive

```text
current physical latent + candidate trajectory k
→ candidate future latent F{k}
→ selector / score
→ final trajectory
```

Pressure:

- candidate-preserving single future consequence is causally distinct from a generic current state;
- factual future alignment during training and online candidate future generation must not be conflated.

### WorldDrive

```text
heavy trajectory-aware DWM teacher
→ pretrain representations
→ distill candidate future latent into lightweight FAR surrogate

runtime:
trajectory candidate k
→ surrogate future latent F{k}
→ reward / preference score
→ final trajectory
```

Pressure:

- `heavy generator dropped` does **not** imply runtime world object absent;
- semantic-equivalent teacher→surrogate substitution should preserve the future-consequence class;
- realization must be an attribute, not a temporal world category.

### SeerDrive paper/code

Both use candidate-conditioned future endpoint state, but deployment topology differs:

```text
paper: action/world representations reciprocally revise before commitment
code: candidates → future endpoints → one score/select → selected-path refinement without rescore
```

Pressure:

- world-object type alone cannot explain policy coupling topology;
- validates independence of a world-role axis and an action/decision-route axis.

## 6. Multi-step future / rollout routes

### WoTE

```text
candidate trajectory k
→ candidate-specific future BEV horizon
→ reward/evaluation over future states/outcomes
→ candidate selection
```

Pressure:

- multi-step physical future is more than a single endpoint;
- candidate identity and horizon time are independent properties.

### Epona world-rollout modes

```text
history + self-predicted or external motion control
→ autoregressive future visual sequence
→ generated future world is terminal mode output
```

Planning-only mode bypasses the visual generator.

Pressure:

- same paper/model family can instantiate W0-like direct planning and future-rollout generation artifacts;
- artifact/mode boundary is mandatory;
- world rollout may be the terminal product rather than an intermediate used to choose an action.

### Discrete-WAM world mode

```text
context + supplied future actions
→ future visual-token sequence
```

Pressure:

- world generation and action commitment can be N/A in a scoped mode;
- action-conditioned future sequence does not by itself mean the system chose the action.

## 7. Joint world-action route

### Discrete-WAM joint mode

```text
interleaved/coupled action tokens + future visual tokens
→ shared generation/editing process
```

Pressure:

- `jointness` is a policy/world coupling property, not necessarily a distinct temporal type of world information;
- the world side still spans a future horizon;
- therefore a human W axis should not duplicate `joint` if R/D already encode joint generation.

### DrivingGPT / WA-JEPA / Policy-World-Model lineage

Census evidence indicates multiple modern systems model future state and action in coupled or interleaved representations.

Pressure:

- maintain a clear distinction between `what future object exists` and `how action and world variables are coupled`;
- do not let architecture-level shared Transformer/token space substitute for causal coupling evidence.

## 8. Imagined-future planning in driving

### Drive-WM

```text
candidate maneuver/action
→ corresponding imagined future video / visual future
→ image-based reward/evaluation
→ planning choice
```

Pressure:

- provides a visual, explicit counterpart to latent candidate-consequence planning;
- substrate should not change the core mechanism if temporal/candidate semantics match.

### Think2Drive

Known field position: Dreamer-style latent world model used as a neural simulator for RL policy improvement.

Pressure:

- critical cross-link between driving and foundational imagination-based policy learning;
- must distinguish world model used to **train** a deployed policy from online MPC over the model.

Promote to RD3 before using for final ontology revision.

## 9. Structured generation without direct planner use

### OccWorld / UniFuture / HERMES families

These works are retained because they clarify what counts as a learned world state/dynamics even when the terminal task is prediction, generation or perception rather than direct planning.

Pressure:

- planning-centric ontology must define scope rather than misclassify generation-only artifacts as action mechanisms;
- a general world ontology and a planning-route ontology may need separate layers.

## 10. Strong controls that prevent WM over-attribution

### UniAD / VAD

Strong structured perception-prediction-planning pipelines demonstrate that rich current scene features and prediction heads do not automatically justify a runtime world-model-state category.

### DiffusionDrive

Strong multimodal trajectory generation without explicit world consequence demonstrates that multimodal action generation is not equivalent to world imagination.

### Hydra-MDP / DriveSuprim / iPad / DrivoR

Candidate proposal and scoring can be strong without an online consequence predictor.

Pressure:

- action topology and world-object topology must be independent;
- multiple candidate trajectories do not imply model-based planning;
- world knowledge can reside in scorer parameters without materialized world consequences.

## 11. Reactive / closed-loop evidence

### NAVSIM

Non-reactive pseudo-simulation: useful planning metrics, but logged environment behavior does not respond to ego deviations.

### Bench2Drive / CARLA-style closed loop

Environment evolves under ego actions with simulator agents/rules; stronger evidence for closed-loop behavior but domain differs from real logs.

### HUGSIM / DriveArena / learned reactive WMs

Photorealistic/generative simulation and behavioral reactivity are separate properties.

### ReactSim-Bench / CausalDrive lineage

Pressure:

- `world model predicts a future` is weaker than `world model predicts behaviorally valid reactions to changed ego actions`;
- intervention/reactivity may be a missing audit dimension if it proves independent of state type, action control binding and evaluation regime.

## 12. Cross-domain collision pairs to preserve

These pairs are especially valuable for ontology testing:

```text
LAW vs DriveLaW
training-only future supervision vs runtime predictive internal state

Drive-JEPA PB vs World4Drive
candidate scorer without runtime future vs candidate-specific future consequence

DynFlowDrive vs WorldDrive
world-derived scorer vs distilled-but-explicit future-state surrogate

GraphWorld vs ordinary BEV planners
current dynamical world state vs scene feature consumed by planner

World4Drive vs WoTE
future endpoint vs future horizon

WoTE vs PlaNet
finite candidate-specific horizon evaluator vs iterative action-sequence optimization over model rollout

SeerDrive paper vs code
reciprocal world↔policy revision vs one-shot candidate consequence resolution

Discrete-WAM joint vs world mode
joint action-world generation vs externally controlled world generation

Think2Drive vs PlaNet
model-imagined policy learning vs model-based online MPC
```

Any final ontology should explain these pairs without relying on architecture names.
