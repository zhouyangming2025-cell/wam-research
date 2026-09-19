# P0045 WoTE — Dimension-first Deep Analysis v2

> Paper: **End-to-End Driving with Online Trajectory Evaluation via BEV World Model**  
> Purpose: pressure-test the LAW-derived dimensions and discover decision-level WAM dimensions that only become visible once future prediction is consumed online.  
> Sources inspected: `papers/raw_md/P0045_WoTE/P0045_WoTE.raw.md`; `audits/literature/PHASE_B_WAVE2_INTERFACE_CODE_AUDIT.md`; `landscape/PHASE_B_WAVE2_COMPARABILITY_AUDIT.md`.  
> Reading protocol: `paper-deep-reader` + evidence-gate ideas from `agent-paper-reader`, extended by the project's dimension-first cross-paper rule.

---

# 0. Executive verdict

WoTE is best understood as a **candidate-conditioned online model-based trajectory evaluator** rather than merely “a BEV world model for planning.”

Its deployed causal loop is:

```text
camera + LiDAR
→ current compact BEV state B_t
→ N trajectory anchors
→ state-conditioned trajectory refinement
→ N candidate ego trajectories τ̂_i
→ encode each candidate as action a_t^i
→ N state-action pairs (B_t, a_t^i)
→ recurrent BEV world model
→ candidate-specific future BEV sequence B_{t+1:t+K}^i
→ learned reward model over current+future BEV and action sequence
→ imitation reward + simulator-style safety/progress rewards
→ weighted final reward
→ argmax candidate
```

This is a structural break from LAW:

```text
LAW:
one planner action → future latent prediction → training loss
future does not select action

WoTE:
many candidate actions → many future-state branches → reward → select action
future directly changes deployed action
```

However, WoTE's strongest scientific boundary is equally important:

```text
candidate-specific ego future supervision       = YES
candidate-specific model future output           = YES
candidate-specific reactive other-agent GT       = NO in audited NAVSIM/PDM target path
```

The audited simulator target pipeline evaluates each ego proposal against the same cached logged surrounding-agent future. Therefore WoTE demonstrates **candidate-conditioned online foresight under non-reactive multi-agent target semantics**, not behaviorally verified counterfactual traffic simulation.

---

# 1. What problem does WoTE actually solve?

## 1.1 Author framing

WoTE begins where multi-modal end-to-end planners create a new bottleneck:

```text
one trajectory prediction
→ trajectory quality bottleneck

multiple plausible trajectories
→ candidate selection bottleneck
```

The authors argue that evaluating a candidate using only the current state is insufficient because trajectory quality depends on what may happen after executing that trajectory.

Therefore the core problem is:

> **How can an end-to-end planner evaluate multiple ego trajectory candidates using their predicted consequences, while remaining real-time and trainable?**

This differs from LAW's problem:

> How can future prediction improve the representation learned by a planner?

The scientific object has shifted from **representation quality** to **decision ranking quality**.

## 1.2 Deeper decomposition

WoTE actually solves four coupled subproblems:

1. **Candidate production:** generate a diverse but manageable action set.
2. **Consequence prediction:** map each candidate to future world states.
3. **Consequence valuation:** turn state/action futures into scores.
4. **Supervision generation:** obtain future-state and reward targets for many candidates although logs contain one factual ego future.

This decomposition matters because a final planning gain can originate from any of the four, not only the world model.

### Immediate cross-paper rule

For every WAM candidate evaluator, never report only:

```text
candidate → future → score
```

Also isolate:

```text
who generated candidate?
how broad is candidate support?
what predicts consequence?
what scores consequence?
where do score labels come from?
which component contributes the gain?
```

This becomes a permanent comparison family.

---

# 2. Candidate generation is an independent subsystem

## 2.1 Trajectory anchors

WoTE clusters expert trajectories with K-Means to obtain `N` trajectory anchors. In the NAVSIM setup:

```text
N = 256
```

Each anchor is not directly executed. It is first refined using current BEV context.

## 2.2 State-conditioned refinement

Each anchor is encoded by an MLP trajectory encoder `TE`, used as a query over current BEV state `B`:

```text
τ̂ = τ + MLP(CrossAttention(TE(τ), B, B))
```

Thus the final candidate set combines:

```text
data-derived motion modes
+ current-scene-dependent residual refinement
```

### Why this cannot be attributed to the world model

Even before future prediction, WoTE has already changed the planner from a single-trajectory predictor into a multimodal candidate generator/refiner. Candidate coverage can independently improve planning because the evaluator cannot choose a safe maneuver that is absent from the candidate set.

### New dimension family: candidate-set geometry

LAW had no meaningful candidate set. WoTE forces us to record:

- candidate source: learned / clustered / sampled / hand-designed / diffusion-generated;
- candidate count;
- anchor vs free-form generation;
- candidate refinement mechanism;
- diversity/mode coverage;
- train/test candidate distribution;
- whether candidate quality is evaluated independently of scorer quality.

This dimension is central for comparison with WorldDrive and World4Drive, both of which also use trajectory vocabularies/intention modes but in different ways.

---

# 3. Current world state: compact BEV as a decision substrate

WoTE fuses multi-view RGB and LiDAR through a TransFuser-style encoder into:

```text
B_t ∈ R^{h×w×c}
```

The paper calls this the BEV state. The world model uses a very compact grid, e.g. `h=w=8` in the described implementation.

## 3.1 Why BEV is chosen

The authors' choice is not merely representational preference. It is explicitly an **inference-cost decision**:

```text
image/video WM
→ expensive multi-step diffusion generation

compact BEV latent/state
→ feed-forward Transformer transition
→ parallel candidate rollout
```

### Cross-paper implication

World-state representation must be compared together with its **operational role and cost constraint**.

For WoTE, BEV is valuable because it supports hundreds of online candidate branches. A high-fidelity RGB world state that cannot be rolled out for 256 candidates would serve a different planning interface.

This sharpens LAW-D01 and LAW-D26 into a joint question:

> **What is the minimum world state sufficient for the decision operation the planner needs to perform under latency constraints?**

---

# 4. Action representation: one candidate = one branch

Each refined trajectory is encoded using the same trajectory encoder into an action embedding:

```text
A_t = {a_t^1, ..., a_t^N}
```

Each candidate creates an explicit state-action pair:

```text
(B_t, a_t^i)
```

This is fundamentally different from LAW's single planner trajectory being repeated into the latent tokens.

## 4.1 LAW vs WoTE

```text
LAW
single predicted W_t
→ one action-aware future prediction
→ auxiliary training loss

WoTE
N refined τ̂_i
→ N state-action pairs
→ N candidate futures
→ N rewards
→ argmax
```

So the meaningful distinction is not merely `action-conditioned = yes`.

We now need at least:

```text
action provenance
action multiplicity
candidate branching point
branch persistence through rollout
branch-specific valuation
branch-specific supervision semantics
```

---

# 5. BEV World Model: recurrent candidate-specific foresight

## 5.1 One transition

For candidate `i`, WoTE flattens BEV state tokens, appends the action embedding, and passes the sequence through a Transformer encoder:

```text
(B_{t+1}^i, a_{t+1}^i) = WM(B_t, a_t^i)
```

The model predicts **both** a future BEV state and an updated future action embedding.

This is already a dimension LAW did not expose clearly:

> Does the dynamics model transition only the environment state, only ego/action state, or a coupled state-action latent?

WoTE evolves both representation streams jointly inside the recurrent transition.

## 5.2 Recurrent rollout

The predicted pair is fed back into the same world model:

```text
(B_{t+k}^i, a_{t+k}^i)
= WM(B_{t+k-1}^i, a_{t+k-1}^i)
```

NAVSIM configuration predicts futures at approximately 2 s and 4 s.

### New dimensions

A single `prediction horizon` field is now insufficient. Record:

- one-step transition interval;
- number of recurrent transitions;
- total rollout horizon;
- whether action evolves during rollout;
- whether the same transition parameters are reused;
- teacher-forced vs free-running recurrence;
- error accumulation exposure;
- whether intermediate states are consumed by the evaluator.

LAW predicts a selected future target for auxiliary training; WoTE produces a **sequence consumed online**.

## 5.3 Evidence for recurrence

The paper compares:

```text
0s → 4s              PDMS 84.0
0s → 2s → 4s         PDMS 85.6
```

The authors interpret this as richer temporal information from finer recurrent prediction.

### Evidence boundary

This supports the usefulness of intermediate future states in WoTE's evaluator. It does **not** by itself establish that the recurrent transition is more accurate as a world model, nor whether the gain comes from state accuracy, temporal features available to the reward network, or optimization differences.

---

# 6. Reward Model: the world model does not make the decision by itself

This is one of WoTE's most important lessons for cross-paper comparison.

The predicted future is not directly the decision. A separate learned value/evaluation mechanism consumes it.

For candidate `i`:

```text
B_all^i = concat(B_t, B_{t+1}^i, ..., B_{t+K}^i)
a_all^i = MLP(concat(a_t^i, ..., a_{t+K}^i))

(B_all^i → Conv2D → global pooling)
+ a_all^i
→ MLP
→ multiple reward heads r_i
```

The final trajectory is:

```text
argmax_i r_final^i
```

## 6.1 Reward semantics

WoTE predicts two reward families:

### Imitation reward

How close a trajectory mode is to human/expert motion.

### Simulation rewards

Five NAVSIM-style criteria:

```text
NC   no collision
DAC  drivable-area compliance
TTC  time-to-collision
Comf comfort
EP   ego progress
```

The final score is a hand-weighted combination of learned reward outputs.

## 6.2 New dimension family: valuation architecture

This is independent of world-state prediction and must be compared separately:

- evaluator input: current only / future only / current+future;
- evaluator form: learned scalar / multi-head metrics / rule-based / cost function / value network;
- value semantics: imitation / safety / legality / comfort / progress / composite utility;
- aggregation: learned / fixed weights / multiplicative / hierarchical constraints;
- reward supervision source;
- calibration/ranking quality;
- whether the evaluator generalizes to unseen candidate distributions.

World-model quality and value-model quality are two separate bottlenecks.

## 6.3 Direct evidence that future adds value beyond scorer

The strongest WoTE ablation is:

```text
trajectory prediction only                  81.0 PDMS
+ learned trajectory evaluation, no future  83.2 PDMS
+ predicted future states                   85.6 PDMS
```

This decomposes roughly:

```text
scorer/evaluator gain beyond generator: +2.2
future-state gain beyond current-state scorer: +2.4
```

This is much stronger planning-interface evidence than a headline SOTA table because it isolates future-state consumption on top of an existing learned evaluator.

### Cross-paper importance

Any future WAM paper claiming “world model helps planning” should ideally provide this kind of control:

```text
same candidate generator
same scorer capacity
with vs without predicted future
```

WorldDrive and World4Drive should be judged against this evidence standard.

---

# 7. BEV-space supervision: simulator as label generator

WoTE identifies a real offline-data problem:

```text
model predicts many candidate-conditioned futures
but logged data contains only one factual future
```

Its solution is to use a traffic simulator to generate labels in BEV space.

## 7.1 Future-state labels

For each simulated candidate scenario, a semantic BEV map is decoded/supervised with focal loss. Classes include road, walkway, centerline, static objects, vehicles, pedestrians, etc.

This introduces a mechanism absent in LAW:

```text
external simulator
→ dense future-state supervisory labels
→ learned world model
```

The simulator is not the deployed planner. It functions as a **training-time supervision oracle/teacher**.

## 7.2 Reward labels

The simulator/rule evaluator also produces trajectory metric targets (collision, DAC, TTC, comfort, progress), used to supervise the learned reward heads.

Thus simulator knowledge enters WoTE twice:

```text
simulator → future semantic-state target
simulator → decision/reward target
```

### New dimension: source of world truth vs source of value truth

These must be separate fields.

A paper can learn world dynamics from logged observations while learning value from rules, or vice versa.

WoTE:

```text
state target source  = BEV simulator / logged scenario construction
value target source  = simulator rule metrics + expert imitation
```

---

# 8. Critical source audit: “multi-future supervision” is not full reactive counterfactual supervision

The paper motivation states that BEV traffic simulators alleviate the scarcity of multiple future labels. That statement is operationally true in the sense that many ego trajectories receive separate simulated ego states/rewards and semantic supervision.

But the exact semantics matter.

The audited NAVSIM/PDM target generation does:

```text
for every candidate ego trajectory:
    simulate ego proposal
    score against metric_cache.observation
```

`metric_cache.observation` is constructed once from recorded/logged future surrounding-agent tracks and shared across candidates.

Therefore:

```text
candidate-specific ego intervention             YES
candidate-specific reward                       YES
candidate-specific BEV target around ego path   YES in generated target pipeline
other-agent future re-planned per candidate      NO in audited NAVSIM/PDM path
reactive traffic counterfactual oracle            NO
```

## 8.1 Why this distinction matters

Suppose ego candidate A merges left and candidate B stays in lane. A fully reactive counterfactual simulator would allow a neighboring car to brake/yield differently under A vs B.

The audited NAVSIM/PDM path instead keeps the surrounding logged trajectories fixed while ego alternatives change.

So WoTE's world model may *output* different surrounding futures by candidate, but the supervision does not directly certify those differences as correct responses to intervention.

### Counterfactual ontology must therefore have levels

A binary `counterfactual = yes/no` is inadequate. At minimum distinguish:

```text
L0: no action condition
L1: single action-conditioned factual prediction
L2: multiple candidate-conditioned model outputs
L3: candidate-specific ego simulation / scores under fixed-agent future
L4: candidate-specific reactive simulator targets
L5: behaviorally validated intervention response / real counterfactual evidence
```

LAW ≈ L1.
WoTE audited NAVSIM path ≈ L3, despite producing L2-style multiple model branches.
World4Drive must be positioned separately because it has K latent outputs but only one factual future latent.

---

# 9. Train-time candidate distribution vs test-time candidate distribution

A subtle but important implementation detail appears in WoTE:

```text
training:
precompute simulator labels on predefined trajectory anchors
feed anchors to trajectory-evaluation module

testing:
evaluate refined trajectories conditioned on live sensor state
```

The paper additionally tests unseen trajectory sets:

```text
trained with 256 anchors
→ test with 1024 unseen anchors
→ reported PDMS increases
```

and reports refined trajectories performing better than raw anchors.

## 9.1 New dimension: evaluator/world-model action-space generalization

Candidate evaluators should be judged on whether they learn:

```text
memorized score for a fixed vocabulary
vs
function over continuous/unseen action space
```

Record:

- train candidate support;
- test candidate support;
- whether simulator labels cover refined candidates exactly;
- interpolation/extrapolation beyond anchors;
- unseen-action generalization evidence.

This becomes highly relevant for WorldDrive's trajectory vocabulary and World4Drive's intention vocabulary.

### Evidence boundary

WoTE's unseen-anchor result is encouraging for action-space generalization, but higher final PDMS with 1024 candidates can also arise from better candidate coverage, not solely better generalization of world dynamics. Candidate-set quality and evaluator generalization remain partially entangled.

---

# 10. Candidate count and compute scaling

WoTE reports:

```text
64 candidates   PDMS 84.5   latency 17.2 ms
128 candidates  PDMS 85.4   latency 17.9 ms
256 candidates  PDMS 85.6   latency 18.7 ms
```

The GPU parallelizes state-action branches.

## 10.1 New dimension: decision breadth vs compute

For candidate-based WAM planning, planning capability depends on both:

```text
breadth of imagined actions
×
depth/fidelity of imagined future
```

under a latency budget.

This suggests a planning compute frontier:

```text
# candidates × rollout steps × state size × evaluator cost
```

Different WAMs trade these factors differently:

- WoTE: many compact BEV branches, recurrent rollout.
- World4Drive: small K intention-conditioned compact latent futures.
- WorldDrive: many candidate trajectories but distills expensive generative futures into a lightweight evaluator.
- Drive-WM: visually rich generated futures, substantially heavier generation path.
- LAW: no online candidate imagination cost.

This is more useful than reporting model latency alone.

---

# 11. Reward composition exposes “what is good driving?” as a model-design choice

WoTE combines imitation and simulation rewards. The ablation reports:

```text
imitation only   PDMS 83.5
simulation only  PDMS 83.6
both             PDMS 85.6
```

and the components trade off differently: imitation helps some collision/TTC aspects; simulation metrics help DAC/progress.

## 11.1 Scientific interpretation

The world model answers:

> what future might follow this candidate?

The reward model answers:

> how desirable is that future?

These are fundamentally different questions.

A better world model cannot compensate for a misspecified utility function, and a better scorer cannot recover consequences that were never modeled.

### New mandatory separation

Future WAM comparison must distinguish:

```text
world accuracy problem
value/reward specification problem
candidate support problem
```

Do not call the entire stack “world-model planning” and attribute the result to one block.

---

# 12. Training graph vs inference graph

## Training

```text
sensor input
→ BEV encoder
→ anchors/refinement
→ candidate action embeddings
→ recurrent WM futures
→ semantic BEV decoder losses
→ reward predictor
→ simulator reward losses + imitation reward loss
→ trajectory refinement loss
```

External simulator-generated targets inject privileged structural knowledge into the learned evaluator/world model.

## Inference

```text
sensor input
→ BEV state
→ refined candidates
→ parallel recurrent future prediction for every candidate
→ learned reward prediction
→ weighted reward aggregation
→ argmax trajectory
```

Unlike LAW, future states are explicitly part of the deployed decision path.

---

# 13. Evidence chain

## Claim C1 — trajectory evaluation itself helps

**Evidence:** Table 3 baseline trajectory prediction only = 81.0 PDMS; learned trajectory evaluation with current state but no future = 83.2.

**Interpretation:** candidate scoring is an independent planning mechanism.

**Unproven:** whether the exact reward formulation is optimal; how much gain comes from candidate diversity versus ranking.

## Claim C2 — future states add value beyond current-state evaluation

**Evidence:** current-state evaluator 83.2 → evaluator with predicted future states 85.6 PDMS.

**Interpretation:** strongest direct evidence that imagined future state is decision-relevant in this architecture.

**Unproven:** the gain does not identify which future-state components matter, nor establish behavioral counterfactual correctness.

## Claim C3 — recurrent intermediate futures help

**Evidence:** direct 0→4 s setup 84.0 vs 0→2→4 s 85.6 PDMS.

**Interpretation:** temporal sequence available to evaluator is useful.

**Unproven:** whether improvement is caused by more accurate dynamics, richer reward features, or optimization.

## Claim C4 — imitation and simulator value signals are complementary

**Evidence:** 83.5 imitation-only / 83.6 simulator-only / 85.6 combined.

**Interpretation:** desired driving behavior is multi-objective; human-likeness and rule/safety/progress signals encode different preferences.

**Unproven:** the hand-weighted aggregate is not shown to be uniquely correct or calibrated.

## Claim C5 — evaluator generalizes beyond training anchor set

**Evidence:** paper evaluates 1024 unseen anchors after training with 256 and reports improved PDMS; refined trajectories also work.

**Interpretation:** scorer/WM is not restricted to exact memorized anchor identities.

**Unproven:** improvement conflates evaluator generalization with expanded candidate coverage.

## Claim C6 — online model-based selection is real-time feasible in this representation

**Evidence:** reported 256-trajectory latency about 18.7 ms on NVIDIA L20.

**Interpretation:** compact BEV + branch parallelism make online candidate foresight practical in reported hardware/setup.

**Unproven:** end-to-end system latency, memory scaling and portability to different hardware/state sizes need separate accounting.

---

# 14. LAW → WoTE dimension changes

WoTE confirms some LAW dimensions but forces several splits.

## Confirmed dimensions

- world-state semantics;
- action provenance;
- action multiplicity;
- action representation/injection;
- dynamics operator;
- prediction/rollout horizon;
- inference future consumption;
- counterfactual scope;
- evaluation feedback regime;
- deployment imagination cost.

## LAW dimensions that must be split/refined

### `Action multiplicity`
Split into:

```text
candidate count
candidate generation source
candidate refinement
candidate coverage/diversity
branch persistence through rollout
```

### `Future target provenance`
Split into:

```text
state-truth source
value/reward-truth source
other-agent response source
```

### `Decision semantics`
Split into:

```text
future consequence representation
future valuation/evaluator
final utility aggregation
```

### `Deployment imagination cost`
Split into a compute frontier:

```text
candidate breadth
× rollout depth
× state resolution
× transition cost
× scorer cost
```

## New dimensions first exposed strongly by WoTE

1. **Candidate-set construction and coverage**
2. **Candidate refinement vs fixed anchors**
3. **World-model action-space generalization**
4. **State-truth oracle vs value-truth oracle**
5. **Simulator teacher semantics**
6. **Other-agent reactivity of supervision**
7. **Reward/value head architecture**
8. **Utility/reward decomposition**
9. **Reward aggregation rule and weights**
10. **World-model vs evaluator attribution**
11. **Recurrent rollout depth / intermediate-state use**
12. **Free-running rollout error exposure**
13. **Candidate breadth × rollout depth compute frontier**
14. **Train/test candidate distribution shift**
15. **Action-space generalization evidence**
16. **World-state semantic decoder supervision**
17. **Ego dynamics vs environment dynamics coupling**
18. **Surrounding-agent behavioral response validity**

---

# 15. Immediate horizontal comparison: LAW vs WoTE

| Question | LAW | WoTE | Scientific difference |
|---|---|---|---|
| Why use future? | shape representation/policy during training | rank multiple actions online | training teacher vs deployed decision variable |
| Action source | one planner-predicted waypoint sequence | 256 anchor-derived/refined candidates | single factual proposal vs branching action set |
| Candidate set | none | clustered + refined | adds independent action-coverage bottleneck |
| Future state | planner visual latent | compact BEV state | state substrate follows interface need |
| Dynamics | one selected future latent Transformer | recurrent Transformer transition | auxiliary target vs multi-step rollout |
| Future consumed at inference? | no | yes | decisive taxonomy split |
| Scorer/value model | absent | learned multi-reward model | consequence prediction separated from valuation |
| Future supervision | one observed future encoded latent | simulator-derived semantic BEV targets across ego candidates | factual SSL vs simulator teacher |
| Alternative ego actions supervised? | no | yes, through candidate simulations/scores | stronger action branching |
| Other agents react per candidate? | no evidence | no in audited NAVSIM/PDM path | still not full reactive counterfactual supervision |
| Main direct evidence | latent task/action-condition ablations | evaluator-with/without-future ablation | WoTE more directly isolates online future value |
| Deployment compute | WM prediction not consumed | 256 parallel candidate rollouts, ~18.7ms reported | foresight depth/breadth becomes compute design problem |

---

# 16. Questions to carry into Epona / WorldDrive / World4Drive

1. Does the method separate **consequence prediction** from **value estimation**, or collapse them into one latent score?
2. Where do candidate trajectories come from and how much of the gain may be candidate coverage rather than WM reasoning?
3. Does a candidate-specific predicted future have candidate-specific *supervision*, and are surrounding agents reactive under that supervision?
4. Is the world state explicitly supervised semantically, self-supervised latently, or inherited from a foundation/generative model?
5. What is the compute allocation between candidate breadth, rollout depth and world-state richness?
6. Are expensive world futures used directly online or distilled/compressed?
7. Does the model learn one factual future, multimodal futures, or explicit action branches?
8. Is the scorer trained from human imitation, rules, simulator metrics, learned preference/value, or a mixture?
9. Can the evaluator handle actions outside its training vocabulary?
10. Does planning improvement survive a matched `same generator + same scorer ± future` control comparable to WoTE Table 3?

These questions should be used to re-project WorldDrive and World4Drive and to guide the first true Epona deep read.
