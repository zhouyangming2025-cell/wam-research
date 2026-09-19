# P0048 LAW — Dimension-first Deep Analysis v2

> Paper: **LAW: Enhancing End-to-End Autonomous Driving with Latent World Model**  
> Purpose: rebuild LAW from mechanism/evidence first principles and use every important design choice as an immediate cross-paper comparison trigger.  
> Sources inspected: `papers/raw_md/P0048_LAW/P0048_LAW.raw.md`; `audits/literature/PHASE_B_WAVE2_INTERFACE_CODE_AUDIT.md`; `landscape/PHASE_B_WAVE2_COMPARABILITY_AUDIT.md`.  
> Reading protocol: adapted from `skills/external/paper-deep-reader-skill/` + `skills/external/agent-paper-reader/`, extended with a WAM-specific **dimension-first cross-paper rule**.

---

## 0. Executive verdict

LAW is most accurately understood as **action-aware future-latent prediction used as an auxiliary self-supervised representation-shaping objective for an end-to-end planner**.

Its causal execution order matters:

```text
current images
→ visual encoder
→ current visual latents V_t
→ waypoint decoder
→ current predicted ego waypoints W_t
→ concatenate W_t into every visual latent
→ action-aware latents A_t
→ latent world model
→ predicted future visual latents V̂_{t+1}
→ match against future-frame visual latents V_{t+1}
```

The deployed trajectory is already produced **before** the future latent exists. Source-code audit further verifies that the future-latent output is discarded by the test-time planning path. Therefore LAW is not online model-based planning and is not a candidate-consequence evaluator.

This distinction immediately separates LAW from:

```text
World4Drive:
candidate trajectory → future latent → score → final selection

WoTE:
candidate trajectory → future BEV rollout → reward → final selection

WorldDrive:
WM representation inheritance + candidate-conditioned future-representation distillation → reward → selection

Epona:
shared world representation → trajectory generation + visual-future generation
```

LAW's main scientific contribution is therefore not simply “a latent world model.” Its contribution is the proposition that **predicting an action-conditioned future representation can improve the representation and policy that produced the action, even when future prediction is not used online**.

---

# 1. What problem does LAW actually solve?

## 1.1 Author framing

LAW starts from a specific view of end-to-end driving: raw sensor inputs contain richer information than pre-processed perception outputs, but end-to-end performance depends on whether the learned scene feature is actually useful for planning. The paper therefore asks how to learn better scene representations from video without requiring additional manual perception labels.

The paper's proposed answer is temporal self-supervision:

```text
current scene representation
+ ego action
→ predict future scene representation
```

The action term is emphasized because future driving scenes depend on what the ego vehicle does.

## 1.2 Deeper interpretation

The core bottleneck LAW attacks is not “future prediction” itself. It is:

```text
trajectory-only supervision
→ weak/underspecified pressure on the visual representation
```

A waypoint loss can be minimized without forcing the encoder to preserve all scene dynamics relevant to future motion. LAW adds a second training pressure:

```text
representation must also contain enough information
for action-conditioned temporal prediction
```

So LAW can be viewed as **representation regularization through predictive dynamics**.

## 1.3 Immediate cross-paper question

Whenever a paper adds a future-prediction task, ask two separate questions:

1. Is future prediction the final deployed reasoning mechanism?
2. Or is future prediction only a training signal shaping a representation/policy?

LAW answers:

```text
future prediction online decision mechanism = NO
future prediction training signal           = YES
```

This axis already separates LAW from WoTE and World4Drive.

---

# 2. Exact mechanism, step by step

Use one fixed driving example throughout:

> Ego sees a slower vehicle ahead; left lane may be available. The planner predicts a short future ego path that begins moving left.

## 2.1 Current visual state: `V_t`

The visual encoder transforms current multi-view images into a set of latent vectors:

```text
V_t = {v_t^1, ..., v_t^L}
v_t^i ∈ R^D
```

The paper deliberately keeps `V_t` generic. It may be:

- perspective-view planning latent in the perception-free framework;
- flattened BEV latent in the perception-based framework.

### Why this matters

LAW does not define “world state” as RGB/video. Its world state is the planner's **learned visual representation**.

### Cross-paper trigger: world-state substrate

Compare immediately:

- **LAW:** perspective-view or BEV latent already used by planner.
- **OccWorld:** discrete structured occupancy tokens.
- **WoTE:** compact BEV world state designed for rollout/evaluation.
- **World4Drive:** physical latent enriched with spatial/depth, semantic and temporal priors.
- **WorldDrive:** video-VAE latent / planning-transferred visual representation.
- **Epona:** shared multimodal latent used by visual and trajectory generation branches.

Therefore `latent vs RGB vs BEV` is too coarse. A stronger dimension is:

> **What information is the world state optimized to preserve, and for which downstream interface?**

LAW's latent is primarily planner-facing and only secondarily constrained by future prediction.

---

## 2.2 Current planner action: `W_t`

The waypoint decoder reads `V_t` and predicts ego waypoints:

```text
W_t = {w_t^1, ..., w_t^M}
w_t^i = (x_t^i, y_t^i)
```

In the perception-free branch, learnable waypoint queries cross-attend to perspective-view latents and an MLP predicts the waypoint sequence. The waypoint loss is standard imitation against ground-truth ego waypoints.

### Crucial ordering

The action is **not an externally supplied counterfactual candidate**. It is the planner's own current prediction.

Source-code audit verifies:

```text
image feature
→ spatial_view_feat
→ waypoint attention/head
→ cur_waypoint
→ wm_prediction(spatial_view_feat, cur_waypoint)
→ wm_next_latent
```

So the action enters the world model only after the current action has already been selected/generated.

### Cross-paper trigger: provenance of action condition

This exposes a new comparison dimension:

**Where does the action condition come from?**

Possible values include:

```text
none
logged/expert action
planner's single predicted action
predefined trajectory anchor
multimodal candidate set
policy action during imagination
high-level command
```

LAW = **planner's single predicted trajectory**.

Contrast:

- WoTE = many candidate trajectories/anchors, each rolled forward.
- World4Drive = K intention-conditioned candidate trajectories, each encoded as action token.
- WorldDrive = trajectory vocabulary / candidate trajectory embedding.
- GAIA-1 = controllable action inputs for generation, but no planner selection loop in the audited use.

This is more informative than the binary label `action-conditioned`.

---

## 2.3 Action-aware latent construction: `A_t`

LAW flattens the full waypoint sequence into one vector:

```text
W_t ∈ R^{M×2}
→ w̃_t ∈ R^{2M}
```

For every visual token `v_t^i`, the same trajectory vector is concatenated and projected by an MLP:

```text
a_t^i = MLP([v_t^i, w̃_t])
```

This produces:

```text
A_t = {a_t^1, ..., a_t^L}
```

### Intuition

Every scene token is told: “the ego currently intends to execute this trajectory.” The future predictor is therefore not asked to predict a generic next scene, but a next representation under the planner's own proposed motion.

### What this mechanism does *not* imply

It does not establish that `A_t` captures a true intervention on surrounding agents. Training only observes the factual future that followed the logged episode; no matched set of alternative-action real futures exists.

### Cross-paper trigger: action injection location and granularity

Do not merely record `action-conditioned = yes`.

Ask:

1. action type: command / control / waypoint sequence / candidate trajectory / policy;
2. action granularity: one action vs K candidates;
3. injection point: token concatenation / cross-attention / diffusion condition / recurrent transition;
4. whether action alters only ego state or is intended to alter the entire predicted world;
5. whether each alternative action has direct supervision.

LAW's profile:

```text
action type        = predicted waypoint sequence
action multiplicity= single planner output
action injection   = repeated concat to each visual token + MLP
predicted object   = future visual latent
alternative-action GT = absent
```

---

## 2.4 Latent world model: `A_t → V̂_{t+1}`

The world model is a stack of Transformer blocks with self-attention over latent feature vectors:

```text
V̂_{t+1} = LatentWorldModel(A_t)
```

### What dynamics model is being learned?

LAW learns a compact one-step mapping in feature space rather than decoding pixels or occupancy:

```text
(current planner representation, predicted ego trajectory)
→ future planner representation
```

This is a materially different object from:

- video diffusion dynamics (Drive-WM / WorldDrive Phase 1);
- recurrent BEV rollout (WoTE);
- intention-conditioned future latent cross-attention (World4Drive);
- joint future-world + ego generation (OccWorld / Epona-like joint modeling families).

### New comparison dimension: dynamics operator

Future-state representation and dynamics architecture must be separate dimensions.

Two papers may both predict “latent futures” yet use very different operators:

```text
single-step deterministic Transformer
recurrent/autoregressive transition
masked/JEPA predictor
diffusion/flow dynamics
discrete autoregressive tokens
joint generative decoder
```

LAW = **single-step deterministic Transformer latent predictor** in its core formulation.

---

## 2.5 Future target: `V_{t+1}`

At training time the actual future frame is passed through the visual encoder, producing future visual latent `V_{t+1}`. The prediction target is therefore not a human annotation but a representation extracted from future sensor data.

Loss:

```text
L_latent = (1/L) Σ_i || v̂_{t+1}^i - v_{t+1}^i ||_2
```

The released code path audited in the repo detaches the future target latent in the reconstruction loss.

### Why this is important

This is self-supervision in a precise sense:

```text
future sensor observation
→ encoder
→ training target
```

No future RGB reconstruction, 3D box, semantic occupancy or map label is required for the latent task itself.

### Cross-paper trigger: target provenance

Future supervision needs a richer taxonomy than `supervised/self-supervised`:

```text
future raw observation
future encoded representation
future semantic label
future occupancy
future simulator reward
teacher-generated latent
single factual future
alternative-action simulated future
alternative-action observed/reactive future
```

LAW = **single factual future encoded representation**.

This immediately exposes a shared limitation with many candidate-conditioned WAMs: having action-conditioned outputs is not equivalent to having action-specific factual counterfactual supervision.

---

# 3. Two host frameworks reveal another dimension: representation portability

LAW explicitly instantiates the same latent-prediction task in two architectures.

## 3.1 Perception-free LAW

Pipeline:

```text
multi-view images
→ image backbone + 3D positional embedding
→ per-view learnable query cross-attention
→ perspective-view planning latents
→ waypoint-query decoder
→ waypoints
→ LAW future-latent auxiliary objective
```

Supervision:

```text
L_pf = L_latent + L_waypoint
```

The important point is that future latent prediction becomes a substitute for adding many perception labels.

## 3.2 Perception-based LAW

Pipeline:

```text
multi-view images
→ BEV encoder
→ BEV latents
→ agent motion + map construction heads
→ waypoint decoder
→ LAW future-BEV-latent auxiliary objective
```

Supervision:

```text
L_pb = L_latent + L_waypoint + L_perception
```

## 3.3 Cross-paper trigger: world-model attachment depth

LAW can be attached to different planner representations without redefining the whole planner. This suggests another dimension:

> **Is the world model an auxiliary module attached to an existing planner, a shared backbone, a transferred pretraining stage, or the central generative policy architecture?**

Examples:

```text
LAW          = auxiliary predictive branch on shared planner representation
ViDAR        = predictive pretraining whose representation transfers downstream
WorldDrive   = WM pretraining + representation inheritance + future-feature distillation
World4Drive  = world latent prediction/selection embedded inside deployed planner
WoTE         = explicit online transition model + evaluator inside planner
Epona        = joint world/action generative architecture
```

This is a stronger axis than “training vs inference” alone because it captures parameter/interface ownership.

---

# 4. Training and inference must be treated as different computational graphs

## 4.1 Training graph

```text
I_t ─→ Encoder ─→ V_t ─→ Planner ─→ W_t ──────────────┐
                     │                                │
                     └──────────────┐                 │
                                    ↓                 ↓
                                  fusion ─→ LWM ─→ V̂_future
                                                     │
I_future ─→ Encoder ─→ V_future (stop-gradient target)┘

trajectory GT ─→ waypoint imitation loss
future frame   ─→ latent prediction loss
```

Thus the world-model loss can update parameters upstream that also affect trajectory prediction.

## 4.2 Inference graph

Audited source path:

```text
I_t
→ encoder
→ planner
→ W_t
→ deployed trajectory
```

Although the branch may still compute latent outputs inside forward, the test-time planning path discards them; no candidate is re-ranked or refined using `V̂_future`.

## 4.3 Scientific consequence

The following two statements are not equivalent:

```text
A. The planner was trained with a world-model objective.
B. The planner uses a world model to reason about futures when choosing an action.
```

LAW proves usefulness of A; it is not evidence for B.

### New mandatory dimensions

Every WAM paper should therefore answer separately:

```text
WM used during representation pretraining?     yes/no
WM loss jointly trains deployed planner?       yes/no
WM future explicitly computed at inference?    yes/no
WM future consumed by action selection?        yes/no
WM future used to rank multiple candidates?    yes/no
```

Collapsing these into one `online/offline` field loses important mechanism differences.

---

# 5. Evidence chain: what does LAW actually prove?

## Claim C1 — latent future prediction improves planning

**Evidence.** nuScenes ablation removes/adds latent prediction in both perception-free and perception-based settings. In the perception-free case, average L2/collision move approximately:

```text
no WM input / no latent task: 0.71 / 0.41
visual latent only:           0.68 / 0.37
visual + predicted trajectory:0.61 / 0.30
```

Perception-based shows a similar trend.

**Interpretation.** Predictive representation learning provides a matched within-framework gain; adding the predicted trajectory as the future-model condition improves further.

**What remains unproven.** The table does not show that the predicted future latent itself should be used online, nor that higher latent prediction accuracy monotonically causes better planning.

---

## Claim C2 — action conditioning matters

**Evidence.** Table 4 compares the latent-prediction setup with visual latent only versus visual latent + predicted trajectory; the latter improves planning metrics.

**Interpretation.** The ego-motion condition supplies useful information for the predictive training task.

**What remains unproven.** This does not establish interventionally correct world response under alternative ego actions. Only the factual future is observed.

---

## Claim C3 — the mechanism is not benchmark-specific

**Evidence.** Latent-prediction ablation is reported across nuScenes, NAVSIM and CARLA. NAVSIM PDMS rises from 77.5 to 84.6; CARLA Driving Score rises from 67.9 to 70.1 in the reported perception-free setup.

**Interpretation.** The auxiliary predictive task transfers across different planner backbones/evaluation regimes better than a nuScenes-only result would suggest.

**What remains unproven.** The size and nature of gains are not identical. NAVSIM is non-reactive data-driven evaluation; CARLA is reactive closed-loop simulation. The paper does not isolate which representation changes explain each metric component.

---

## Claim C4 — farther prediction is not automatically better

**Evidence.** Time-horizon ablation reports best planning around a 1.5 s latent-prediction horizon; 10 s prediction removes the gain and becomes worse than the shorter settings.

**Interpretation.** Predictive-task usefulness has a **difficulty/informativeness trade-off**:

```text
future too near  → little dynamic information
future too far   → target becomes too difficult/uncertain
intermediate     → useful representation pressure
```

**Cross-paper significance.** This is a direct warning against using “longer world-model horizon” as a universal proxy for better planning.

### New dimension

Record separately:

```text
prediction horizon
rollout horizon
planner horizon
supervision horizon
best evidence-supported horizon
```

They are not necessarily the same.

---

# 6. Strongest contribution vs strongest limitation

## Strongest contribution

LAW demonstrates a lightweight mechanism for turning ordinary driving video into an action-aware temporal self-supervision signal that improves planning without requiring pixel generation or extra perception labels.

Its most reusable idea is:

```text
future prediction need not be a deployment-time simulator;
it can serve as a representation-shaping objective for planning.
```

## Strongest limitation

LAW does not close the model-based decision loop:

```text
propose action
→ imagine consequence
→ evaluate consequence
→ revise/select action
```

Instead:

```text
propose action
→ predict factual-future representation for training loss
```

The future model therefore regularizes the action generator but does not adjudicate actions online.

## Hidden assumption

For latent MSE to be useful, the future feature target must preserve planning-relevant temporal structure. But the target itself is produced by the learned visual encoder; there is no independent guarantee that latent Euclidean similarity corresponds to decision relevance.

This opens a cross-paper question later exposed more sharply by OccWorld and WorldDrive:

> **What future information should be preserved because it matters for decision, rather than because it is easy to reconstruct?**

---

# 7. Module-by-module horizontal comparison triggers

This section is deliberately not a final comparison matrix; it records the questions LAW forces us to ask of every other anchor.

| LAW component / choice | What LAW does | Immediate comparison question for other papers |
|---|---|---|
| visual world state | planner latent, PV or BEV | Does the other paper model raw appearance, semantic structure, occupancy, objects, graph, or task-specific latent? |
| action source | planner's single predicted waypoint sequence | Is action logged, expert, candidate, sampled, policy-generated, command-level or low-level control? |
| action multiplicity | one | Does the method branch over multiple alternatives? |
| action injection | concat same trajectory vector into each scene token + MLP | concat, attention, diffusion conditioning, recurrent transition, token interleaving? |
| dynamics operator | Transformer latent predictor | deterministic, autoregressive, diffusion, flow, JEPA, discrete token model? |
| future target | one factual future visual latent | label, raw sensor, teacher latent, reward, simulator outcome, multiple counterfactuals? |
| target encoder | same learned representation; target detached in audited code | frozen target, EMA teacher, independently pretrained encoder, semantic labels? |
| prediction horizon | one selected future frame; ablated from 0.5 to 10 s | one-step, multi-step, rollout, variable horizon? |
| training role | auxiliary self-supervised loss jointly shapes planner | pretraining, joint loss, distillation, RL imagination? |
| inference role | predicted future not consumed by action selection | future generation/ranking online? |
| decision semantics | representation shaping | simulator, evaluator, value, reward, policy hidden state, joint generator? |
| candidate consequence | absent | does each candidate produce a separate predicted consequence? |
| counterfactual supervision | absent | are alternative consequences directly supervised, simulated, or merely model-generated? |
| world/planner coupling | planner output conditions auxiliary WM; WM only influences planner through gradients | uni-directional, bi-directional iterative, shared latent, recurrent loop? |
| manual labels required by WM task | none | occupancy/map/object annotations or foundation-model priors required? |
| evaluation | nuScenes open-loop; NAVSIM non-reactive; CARLA closed-loop | what feedback regime actually supports the claim? |
| deployment cost | no need to consume future prediction for trajectory selection | full rollout, compact latent, distilled future, recurrent world model? |

---

# 8. Dimensions discovered or sharpened by LAW

These are **provisional dimensions**, not route labels. They were consolidated into `landscape/WAM_DIMENSION_ONTOLOGY_V1.md`; the five-question review interface records the remaining deployment distinctions without creating a per-paper projection layer.

### A. World-state semantics
What does the latent/world state represent, and what information is it optimized to preserve?

### B. Action-condition provenance
Where does the action input come from?

### C. Action multiplicity
Single factual/planner action vs multiple candidate alternatives.

### D. Action injection mechanism
How is action fused with world state?

### E. Dynamics operator
What mathematical/model family maps state+action to future?

### F. Future-target substrate
Raw observation, planner latent, semantic/occupancy state, reward/value, teacher latent, etc.

### G. Future-target provenance
Observed factual future, simulated future, teacher-generated future, counterfactual/reactive target.

### H. Target-network treatment
Shared encoder, frozen encoder, EMA teacher, stop-gradient, independently pretrained target.

### I. Prediction horizon vs planning horizon
Do not collapse them.

### J. WM attachment depth
Auxiliary branch, pretraining stage, shared backbone, deployed transition model, central generator.

### K. Gradient coupling direction
Which modules are changed by the WM objective, and where are stop-gradients used?

### L. Inference-path consumption
Future computed? Future consumed? Future ranks candidates? These are separate fields.

### M. Decision semantics of the future
Representation teacher / simulator / evaluator / reward / value / policy state / generator.

### N. Counterfactual scope
Does the system merely condition on action, branch over candidate actions, or have evidence of alternative-world correctness?

### O. Label economy
What additional annotations/priors are needed to train the world state/dynamics?

### P. Predictive-task difficulty vs informativeness
LAW's horizon ablation shows a useful self-supervised future need not be the farthest future.

### Q. Evaluation feedback regime
Open-loop, non-reactive data-driven, reactive simulator, real closed-loop.

### R. Deployment imagination cost
Full rollout, latent prediction, distillation, no online WM consumption.

---

# 9. LAW's historical role in the WAM evolution

A useful evolutionary reading is:

```text
Traditional E2E
observation → representation → trajectory

LAW
observation → representation → trajectory
             ↓             ↓
         state + predicted action
             → future latent prediction
             → auxiliary training signal

WoTE / World4Drive family
observation → candidate actions
→ candidate-specific future prediction
→ evaluation/score
→ select action

WorldDrive family
world-model predictive representation pretraining
+ transfer/distillation of future knowledge into candidate ranking
```

The important transition after LAW is therefore not simply “better world model.” It is:

> **Future information moves from a training-time constraint on the planner into an inference-time decision variable.**

That transition will be tested directly when deep-reading WoTE next.

---

# 10. Claims ledger

| Claim | Evidence locator | Verdict | What remains unproven |
|---|---|---|---|
| LAW predicts future visual latents from current visual latents + ego waypoints | §4.1 Eq.1–3 | supported | latent semantics are not independently identified |
| future target comes from future frame encoder | §4.1 Future Latent Supervision | supported | target quality/decision relevance not guaranteed |
| action conditioning improves the auxiliary mechanism/planning | Table 4 | supported within reported ablation | no counterfactual behavioral correctness |
| latent prediction improves planning across datasets | Tables 4–5 | supported | exact causal source of each benchmark gain remains mixed |
| very long prediction horizon is not better | Table 6 | supported in LAW setup | does not imply all WAMs have same optimal horizon |
| future latent is used to select deployed trajectory | source-code audit | contradicted | branch may execute, but output is not consumed by selection |
| LAW is online model-based planning | source-code audit | contradicted | LAW is better classified as predictive auxiliary representation shaping |
| LAW provides alternative-action world supervision | paper + audit | not supported | only factual future is available |

---

# 11. Questions to carry into WoTE

LAW leaves a precise set of questions for the next anchor:

1. If future prediction is used **online**, does it add value beyond a strong learned evaluator?
2. How many candidate actions are actually branched and rolled out?
3. Does each candidate receive a separate future target, or only a separate model prediction?
4. Do surrounding agents react differently under each candidate in supervision/evaluation?
5. Is future-state quality measured directly, or only through planning score?
6. Is the reward/value head an independent bottleneck from the world model?
7. What additional inference cost is introduced when future states are consumed online?
8. Does multi-step rollout create compounding errors absent from LAW's auxiliary single-future prediction?

These questions will expand or split the provisional dimensions above before any ontology is frozen.
