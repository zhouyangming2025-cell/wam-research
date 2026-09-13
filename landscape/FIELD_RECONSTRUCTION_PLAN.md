# FIELD_RECONSTRUCTION_PLAN

Last updated: 2026-09-14

## 0. Why this phase exists

The project previously moved too quickly from a small set of papers to candidate gaps (P1/P2-R/P3). That created a structural risk: interpreting the field through a preselected hypothesis before understanding the field's full design space, historical evolution, benchmark structure, and already-established trade-offs.

New rule:

```text
UNDERSTAND THE FIELD FIRST
→ reconstruct the technical landscape
→ understand why major design families exist
→ understand what each family gains and loses
→ understand benchmark/evaluation effects
→ identify recurring tensions and unresolved questions
→ only then mine research problems / gaps
```

P1/P2-R/P3 are retained as historical probes, not as the search objective of this phase.

## 1. Scope boundary

Primary scope:

```text
World Model + End-to-End + Planning-centric autonomous driving
```

Include work when future/world modeling materially changes one or more of:

- trajectory generation;
- candidate ranking / scoring;
- planning representation;
- counterfactual action evaluation;
- interactive prediction-planning coupling;
- closed-loop policy learning;
- simulation used to train/evaluate planning;
- safety/value/reward signals consumed by planning.

Do not let the map become perception-centric or generic video-generation-centric. Pure generation/perception papers are included only when they establish a world-model representation, training paradigm, or simulator that later becomes important for planning.

Risk field / safety representations are one optional branch, not the organizing principle.

## 2. What must be understood before asking for a gap

### 2.1 What is the world state?

Map methods by predicted state space:

```text
RGB / video
BEV feature
occupancy / flow
point cloud / 3D / Gaussian / scene geometry
vector / object / relation state
trajectory / behavior state
latent predictive state
reward / value / cost / preference state
hybrid multimodal state
```

Question: what information becomes easy or hard to preserve in each state space, and what does the planner actually consume?

### 2.2 What role does the world model play?

Separate at least:

```text
future generator / simulator
representation pretraining
auxiliary future-prediction supervision
direct future latent for planning
action-conditioned candidate evaluator
MPC / rollout planner
reward / value / safety estimator
closed-loop RL environment / policy improver
world-action / unified generative policy
```

A method can occupy multiple roles.

### 2.3 How is the future conditioned?

Record exactly:

```text
history only
route / command
ego state
discrete action / control
ego trajectory candidate
intention / goal
multi-agent actions / relations
policy-conditioned rollout
```

Do not equate action conditioning with correct causal or reactive response.

### 2.4 How is planning coupled to prediction?

Map the interface:

```text
prediction is discarded at inference
future feature conditions direct trajectory decoder
future state enters candidate scorer
future occupancy enters hand-designed cost
world model is rolled out per action
planner optimizes through / over learned model
world model supplies reward/value
policy/world/action are jointly generated
```

This is a more important planning-centric axis than visual quality alone.

### 2.5 What supervision is actually available?

Separate:

```text
future observation reconstruction/prediction
self-supervised latent prediction
expert imitation
trajectory ranking / candidate labels
rule / metric supervision
preference supervision
safety labels
counterfactual proxy labels
closed-loop reward / RL
synthetic / simulator supervision
```

For counterfactual methods, always ask which candidate has a real observed future and which candidates are only inferred.

### 2.6 What kind of interaction is modeled?

Distinguish:

```text
independent marginal prediction
joint prediction
conditional influencer→reactor prediction
ego-conditioned response prediction
contingency / branching planning
game-theoretic interaction
reactive simulator agents
learned closed-loop world agents
```

### 2.7 What is the planning output?

```text
direct trajectory
trajectory distribution / diffusion
candidate set + score
continuous cost / optimization
control sequence
policy action
hierarchical intent + trajectory
```

### 2.8 How is it evaluated?

Never collapse:

```text
visual generation metric
motion-prediction metric
open-loop trajectory matching
NAVSIM / data-driven non-reactive evaluation
closed-loop non-reactive simulation
reactive closed-loop simulation
CARLA / Bench2Drive style simulation
real-vehicle closed loop
```

Also record data, horizon, candidate count, model size, latency/FPS, and whether comparisons share backbone/input/evaluation.

## 3. Reconstruction phases

### Phase A — Field census / breadth map

Goal: identify the actual families and historical transitions before deep interpretation.

Target: roughly **50–80 decision-relevant papers** at metadata/abstract/method-overview depth, not 50–80 full deep reads.

For each paper record only enough to place it in the taxonomy:

- year / venue;
- world-state representation;
- generative/predictive paradigm;
- planning role;
- action conditioning;
- interaction/reactivity level;
- supervision;
- planning output;
- evaluation regime;
- primary contribution;
- main stated limitation.

No gap score. No novelty score. No attempt to make it support P2-R.

### Phase B — Representative anchor deep reads

Select roughly **15–25 anchor papers** that explain the field, including:

- foundational generation/simulation WMs;
- occupancy/BEV world models;
- latent/JEPA world models;
- unified world/action models;
- candidate-conditioned planning WMs;
- interactive prediction-planning predecessors;
- strong end-to-end planners without explicit WM;
- reactive/closed-loop evaluation papers;
- important counterexamples.

Deep-read them using the full paper-card standard.

### Phase C — Field synthesis

Produce:

1. **historical evolution:** what problem caused each major paradigm shift;
2. **architecture map:** which representations/interfaces dominate and why;
3. **planning-coupling map:** where the world model actually enters the planner;
4. **supervision map:** what is observable vs inferred/counterfactual;
5. **evaluation map:** which claims are supported by which regime;
6. **trade-off matrix:** fidelity, decision relevance, reactivity, uncertainty, efficiency, interpretability, scalability;
7. **contradiction / counterexample map:** papers whose success falsifies broad claims;
8. **evidence gaps:** important properties that current benchmarks do not measure well.

Only after this synthesis do we discuss possible research problems.

### Phase D — Problem discovery / gap mining

Now ask:

```text
What recurrent planning difficulty survives across multiple method families?
What trade-off appears structural rather than implementation-specific?
What important planning property is weakly measured or unsupervised?
Where do strong papers disagree, and why?
What failure is repeatedly visible but not resolved?
```

A valid research problem should emerge from the landscape, not be chosen before it.

## 4. Reading depth policy

Not every census paper gets a full card.

```text
CENSUS       = enough to place accurately in field map
ANCHOR       = deep read; full scientific card
DECISION     = anchor + targeted source/code audit if necessary
BACKGROUND   = retained for context only
```

This prevents both extremes:

- blind gap hunting from too few papers;
- collecting hundreds of papers without digesting them.

## 5. Initial organizing families

This list is provisional and should be corrected by evidence rather than protected:

```text
F1  Visual/video generative driving world models
F2  BEV / occupancy / geometric predictive world models
F3  Latent / JEPA / representation-predictive world models
F4  World-model-assisted end-to-end planning
F5  Candidate-conditioned / action-conditioned future evaluation
F6  Unified world-action / trajectory-and-world generation
F7  Interactive prediction + planning / contingency / game-theoretic predecessors
F8  Reactive world simulation / closed-loop policy training
F9  Reward / value / safety / cost interfaces for planning
F10 Strong end-to-end planning baselines without an explicit WM
F11 Evaluation / benchmark / simulator papers that change interpretation of planning results
```

The map should reveal overlaps; this is not a mutually exclusive classification.

## 6. Current hypotheses during reconstruction

```text
P1 = historical retired hypothesis
P2-R = PARKED PROBE; useful lens, not active target
P3 = PARKED BACKUP PROBE
```

Do not optimize the reading list to prove or kill them. If the field reconstruction independently returns to one of them, that is useful evidence. If not, abandon them without cost.

## 7. Completion criteria for field reconstruction

Do not claim "we understand the field" until we can answer, without hand-waving:

1. What are the major planning-centric WAM families and why did each arise?
2. What exact information flows from observation → future model → planner in each family?
3. What supervision makes each interface learnable?
4. Which methods are truly action-conditioned, counterfactual, reactive, or closed-loop?
5. Which benchmark regimes support which claims?
6. What are the strongest non-WM end-to-end planning baselines and what do they show?
7. What trade-offs recur across independent papers?
8. Which widely repeated claims have strong counterexamples?
9. What capabilities are genuinely under-measured rather than merely under-architected?
10. Where does the evidence remain contradictory or incomplete?

Only then reopen formal gap selection.
