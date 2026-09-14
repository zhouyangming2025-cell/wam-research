# PHASE_B_WAVE2_SYNTHESIS — From World Prediction to Planning Interface

Last updated: 2026-09-14

Status: **COMPARATIVE FIRST PASS COMPLETE — mechanism/interface audit included**

Wave 2:

```text
GAIA-1
Drive-WM
OccWorld
WoTE
ViDAR
LAW
```

Purpose: explain what changed when autonomous-driving research moved from planning-oriented prediction/E2E systems into explicit driving world models, while refusing to treat all uses of future prediction as one paradigm.

Source-code supplement:

`audits/literature/PHASE_B_WAVE2_INTERFACE_CODE_AUDIT.md`

Wave-1 controls remain binding:

```text
future prediction accuracy != planning evidence
conditional future != causal response
final planner score must be decomposed
matched controls > headline SOTA
candidate ranking is an independent bottleneck
evaluation regime is part of the claim
```

---

## 1. Executive result: “world model helps planning” splits into at least five different mechanisms

Across these six anchors, world/future modeling enters planning through fundamentally different interfaces:

```text
GAIA-1:
world generation capability only
(no operational planner interface)

Drive-WM:
candidate action → generated future video → detector/map reward → select action

OccWorld:
shared latent dynamics jointly generate future occupancy + ego motion
(no alternative-action evaluator)

WoTE:
candidate action → candidate-specific future BEV → learned reward → select action

ViDAR:
future geometry prediction pretrains the representation
(future branch not needed as deployed planner interface)

LAW:
predicted ego trajectory conditions future-latent auxiliary prediction during training
(source audit: predicted future latent is ignored by test-time action selection)
```

Therefore:

```text
“uses a world model”
```

is scientifically too coarse. The planning-relevant taxonomy must ask **what the future is used for**.

---

## 2. GAIA-1 — controllable world generation before a planning interface

### Exact role

GAIA-1 autoregressively models driving video/world evolution using image tokens together with language and vehicle actions such as speed/curvature. It can roll out futures conditioned on changed actions and qualitatively displays resulting ego motion and scene evolution.

### What it establishes

**AUTHOR CLAIM.** Large-scale generative models can learn high-level rules and scene dynamics from driving data and support controllable imagination.

**DIRECT EVIDENCE.** The paper demonstrates long, coherent, action-conditioned video generation qualitatively and through generation-focused evaluation. It shows plausible changes when action/text conditions are modified.

### What it does not establish

There is no operational planning loop of the form:

```text
candidate action
→ generated future
→ decision score
→ selected ego plan
```

and no planning benchmark showing that using the generated future improves an ego planner.

The visible response of other agents under changed conditions is also qualitative rather than a behavioral counterfactual benchmark.

### Historical role

GAIA-1 is best treated as the **capability precursor**:

```text
Can a large generative model represent and controllably imagine a driving world?
```

It does not yet answer:

```text
How should a planner consume that imagination, and does doing so improve decisions?
```

This distinction is the starting point of Wave 2.

---

## 3. Drive-WM — the key transition from controllable generation to explicit future-based action evaluation

Drive-WM creates the clearest early visual-WM planning interface in this wave.

### Data flow

At planning time:

```text
current observations
→ candidate ego trajectories/actions
→ one generated future video per candidate
→ 3D object detector + online HD-map perception on generated future
→ object/map reward
→ choose highest-reward candidate
```

It can recursively expand this process into a tree.

This is qualitatively different from GAIA-1: the imagined world becomes a **decision variable**, not merely a generated artifact.

### Direct planning evidence

In the reported nuScenes planning experiment using VAD-derived commands/candidates:

```text
VAD with GT command         L2 0.72 / collision 0.22
VAD with random command     L2 1.02 / collision 0.93
sampled candidate           L2 0.87 / collision 0.47
Drive-WM selection          L2 0.80 / collision 0.26
```

The paper also reports that combining object and map rewards performs better than either alone.

This is direct evidence that candidate-specific imagined futures can be operationally used to improve selection relative to weaker candidate-choice strategies in that setup.

### Strongest competing explanations / boundaries

The planner interface contains several mechanisms simultaneously:

```text
generated future quality
+ detector performance on generated imagery
+ map estimator performance
+ hand-designed reward formulation
+ candidate set quality
```

The experiment does not cleanly isolate “world-model fidelity” from these downstream perception/reward choices.

The reported planning evaluation is also nuScenes/open-loop-style rather than a reactive closed-loop environment. Candidate branches are generated by the learned model, but no reactive oracle supplies the true surrounding-agent response for every alternative candidate.

### Historical role

Drive-WM establishes a major transition:

```text
controllable generative WM
→ explicit imagined-future evaluator for planning
```

but not yet behaviorally validated counterfactual planning.

---

## 4. OccWorld — structured world state and joint world-action generation are different from candidate evaluation

OccWorld changes both the state representation and the world/action relationship.

### Data flow

```text
past 3D semantic occupancy
→ scene tokenizer / discrete tokens
→ spatial-temporal autoregressive transformer
→ future scene tokens + ego token
→ decode future occupancy + ego trajectory
```

The ego future is co-modeled with the future world. This is an early structured form of joint world-action generation.

### Critical distinction

OccWorld does **not** implement:

```text
candidate a1 → future world 1 → score
candidate a2 → future world 2 → score
...
```

Instead, the ego future is itself one of the model outputs. Therefore:

```text
jointly generating world + ego future
!=
candidate-conditioned consequence evaluation
```

This distinction matters because both are often loosely called “action-aware world modeling.”

### Planning evidence and supervision

OccWorld uses future semantic occupancy plus ego-motion supervision and reports downstream ego-planning metrics. Its stronger oracle/structured-input variants outperform camera-only degraded variants, but the comparisons mix input quality and model configuration.

The cleanest Wave-2 evidence from OccWorld is not the headline planning table; it is the internal representation ablation.

### Strong counterexample: better reconstruction can yield worse forecasting/planning

The paper's tokenizer-resolution experiment reports a higher-resolution tokenizer with much better reconstruction:

```text
reconstruction mIoU / IoU:
78.12 / 71.63
```

versus the default:

```text
66.38 / 62.29
```

Yet downstream forecasting/planning are worse:

```text
future forecasting mIoU:
12.38 vs 17.14

planning L2:
1.36 vs 1.17
```

This is one of the strongest direct pieces of evidence in the current atlas against the assumption:

```text
higher world reconstruction fidelity
→ better world forecasting
→ better planning
```

A representation can reconstruct current/future scene details more accurately while being **less useful as a predictable planning state**.

### Temporal-dynamics evidence

Removing temporal interaction hurts both future prediction and planning. The paper also identifies degradation for longer rollout and failure when previously unseen vehicles enter the field of view.

### Historical role

OccWorld is important not because occupancy is automatically superior to RGB, but because it exposes two enduring questions:

1. What information should a “world state” preserve for planning?
2. Should the ego action be an external intervention, or a jointly generated modality?

---

## 5. WoTE — the cleanest Wave-2 case where future state is explicitly consumed online

WoTE is architecturally closer to classic model-based decision making than LAW/ViDAR.

### Data flow

```text
camera + LiDAR
→ compact current BEV state B_t

256 ego trajectory anchors
→ anchor refinement
→ candidate actions a_i

for each candidate i:
(B_t, a_i)
→ world model
→ predicted future BEV states
→ recurrent future rollout

(current/future BEV + action)
→ learned reward heads
→ candidate score
→ argmax trajectory
```

The model parallelizes candidate branches.

### Direct mechanism decomposition

The validation ablation is unusually useful:

```text
trajectory prediction only                  81.0 PDMS
+ learned trajectory evaluation, no future  83.2 PDMS
+ future world states                        85.6 PDMS
```

This decomposes two independent gains:

```text
better evaluator/scorer alone: +2.2
future-state input on top:      +2.4
```

Therefore WoTE provides stronger evidence than many WAM papers that **the predicted future state itself adds value beyond a learned evaluator that sees no future state**.

Additional ablations:

```text
imitation reward only  83.5
simulation reward only 83.6
both                   85.6

single 0→4 s rollout   84.0
0→2→4 s rollout        85.6

64 / 128 / 256 candidates:
84.5 / 85.4 / 85.6 PDMS
```

Reported latency for the 256-candidate setting is approximately `18.7 ms` in the table, showing that per-candidate world modeling need not imply serial rollout cost if branches are batched/parallelized.

### Supervision audit: candidate-specific does not mean reactively supervised

The source-code audit resolves an important ambiguity.

WoTE's target-generation script evaluates many predefined ego trajectories with `pdm_score_multi_trajs`. Each candidate ego trajectory is simulated, but all are scored against the same `metric_cache.observation`.

`MetricCacheProcessor._interpolate_gt_observation` creates that observation from:

```text
scenario.get_tracked_objects_at_iteration(...)
```

and interpolates the logged/GT future tracks. Candidate ego action is not an input to this construction.

Thus in this target path:

```text
candidate-specific ego future: YES
candidate-specific reward: YES
candidate-dependent logged other-agent future: NO
```

The supervision follows NAVSIM-style non-reactive semantics.

### Scientific interpretation

WoTE remains a genuine **online candidate-conditioned world-model planner** because different candidate actions are passed through the learned WM and future states are consumed by the rewarder.

But the evidence does not establish:

```text
each candidate's predicted surrounding-agent response
=
behaviorally correct response to that ego intervention
```

The learned candidate branches are richer than their available reactive oracle supervision.

### Strongest Wave-1 competing explanation

DriveSuprim showed that candidate ranking alone can create large gains. WoTE's future-state-on/off ablation is therefore particularly important: it survives that specific alternative explanation better than a plain SOTA comparison, although richer simulator/reward supervision still remains a confound.

---

## 6. ViDAR — world prediction can help planning even when the world model disappears from inference

ViDAR is the clean counterexample to the assumption that “WM-assisted planning” means online imagination.

### Role

```text
historical camera images
→ BEV representation
→ latent rendering
→ autoregressive future occupancy / point-cloud forecasting
```

This task is used to pretrain the representation. The downstream autonomous-driving models reuse the pretrained encoder; the forecasting decoder is not the deployed planning interface.

### Planning evidence

For a UniAD downstream setup, the reported planning comparison is approximately:

```text
UniAD baseline          avg L2 1.12 / collision 0.27
ViDAR-pretrained UniAD  avg L2 0.91 / collision 0.23
```

This supports the claim that future-prediction pretraining can improve a downstream planner.

### Crucial matched negative control

A naïve differentiable ray-casting pretraining implementation degrades downstream detection (`NDS 44.11 → 40.20` in the reported comparison), whereas the proposed latent rendering pretraining improves it (`47.58`).

Therefore:

```text
“add a future prediction task”
```

is not sufficient. The representation and rendering/prediction interface determine whether the pretext task improves downstream features.

### What it proves and does not prove

It proves:

```text
future geometry prediction can be a useful representation-learning objective
```

It does not prove:

```text
online imagined future is necessary for planning
```

or that the downstream planner's gain comes from counterfactual reasoning.

Historical role: ViDAR establishes the `WM-as-pretraining` branch that must be kept separate from `WM-as-online-evaluator`.

---

## 7. LAW — action-aware future latent prediction as planner regularization, not online rollout

LAW is particularly important because its paper language can easily be read too broadly if architecture and inference are not separated.

### Paper-level data flow

```text
current images
→ visual/spatial latent V_t
→ waypoint decoder
→ predicted ego waypoints W_t

(V_t, W_t)
→ action-aware encoder + Transformer world model
→ predicted next latent Vhat_{t+1}

future real observation
→ target future latent V_{t+1}

MSE(Vhat_{t+1}, V_{t+1})
+ waypoint loss
```

Thus the planner's **own predicted trajectory** conditions the future-latent prediction task.

### Direct ablation

Perception-free branch:

```text
no WM                      L2 0.71 / collision 0.41
visual latent prediction       0.68 / 0.37
+ ego trajectory condition     0.61 / 0.30
```

Perception-based branch:

```text
0.54 / 0.25
→ 0.52 / 0.21
→ 0.49 / 0.19
```

The action-aware latent objective therefore adds planning-side gains beyond a visual-latent-only future objective in the authors' ablation.

On the paper's perception-free NAVSIM/CARLA comparison:

```text
without latent prediction  PDMS 77.5 / CARLA DS 67.9±2.1
with latent prediction     PDMS 84.6 / CARLA DS 70.1±2.6
```

This is stronger evidence than nuScenes L2 alone that the auxiliary objective can improve driving policy quality under multiple evaluation regimes.

### Source-code audit resolves the inference ambiguity

At public commit:

```text
BraveGroup/LAW
b2f6a784247072923c477ab92324d3aa5a9759bf
```

`WaypointHead.forward` computes `cur_waypoint` **before** calling `wm_prediction(...)`.

Training uses the returned future latent in `loss_reconstruction(...)`.

Testing calls:

```python
preds_ego_future_traj, _, _ = self.pts_bbox_head(...)
```

and discards the current/future latent outputs for plan selection.

Therefore the audited implementation supports the stronger architectural conclusion:

```text
LAW's future-latent branch is an auxiliary representation-shaping objective.
The predicted future latent is not fed back into the current trajectory selection/refinement path at inference.
```

The branch can still execute at inference in the code, but its returned future prediction is ignored by the planner output path.

### Horizon counterexample

The future target horizon is not monotonic:

```text
0.5 s   L2 0.61 / collision 0.30
1.5 s      0.58 / 0.25   ← best among shown horizons
3.0 s      0.63 / 0.27
10.0 s     0.72 / 0.43
```

This is direct evidence against the generic claim:

```text
longer predictive horizon → better planning representation
```

At least in LAW, a moderately short future provides stronger useful supervision than very long-horizon latent matching.

### Historical role

LAW creates a crucial bridge:

```text
world modeling
→ not necessarily a simulator/evaluator
→ can instead be a self-supervised constraint that shapes planning features
```

---

## 8. Cross-paper interface matrix

| paper | future state | ego action relation | alternative-action supervision | future used at inference? | planning interface | planning evidence | biggest confound / boundary |
|---|---|---|---|---|---|---|---|
| GAIA-1 | visual/video tokens | action-conditioned generation | logged factual data; alternatives inferred | generation yes, planner no | none operational | no direct planner evidence | qualitative controllability ≠ decision utility |
| Drive-WM | multiview future video | one future per candidate | alternative branches learned/generalized, no reactive oracle | **yes** | generated video → detector/map reward → select | nuScenes planning selection | reward/perception heads + small candidate set + E2 evaluation |
| OccWorld | future semantic occupancy tokens | ego future jointly generated | no candidate intervention set | **yes**, in joint generation | shared latent → ego decoder | nuScenes planning | joint generation ≠ candidate consequence evaluation; metric variants mixed |
| WoTE | compact future BEV states | **one branch per candidate** | candidate ego/reward labels; other-agent future fixed/logged in audited PDM path | **yes** | future BEV → learned reward → select | NAVSIM + additional benchmark results | non-reactive target semantics + rich reward supervision |
| ViDAR | future geometry / latent rendering | none | none | **no deployed planning interface** | pretrain encoder → downstream planner | downstream UniAD improvement | representation pretraining, not online imagination |
| LAW | future visual latent | planner-predicted ego trajectory conditions latent predictor | factual future latent target only | WM output **not consumed by plan** | auxiliary loss shapes shared planner features | nuScenes/NAVSIM/CARLA ablations | action-aware auxiliary training ≠ candidate rollout |

---

## 9. The most important Wave-2 distinctions

### 9.1 Action conditioning has at least three non-equivalent meanings

```text
A. controllable generation
   GAIA-1
   action changes generated future
   but future is not used by a planner

B. inference-time candidate consequence branching
   Drive-WM / WoTE
   each candidate gets its own imagined future used for selection

C. action-aware training objective
   LAW
   predicted ego trajectory conditions future-latent learning
   but predicted future latent is not used to choose the action online
```

A paper saying “action-conditioned world model” is therefore incomplete without this role distinction.

### 9.2 Joint world-action generation is a fourth pattern

OccWorld generates world evolution and ego motion together. The action is neither merely an external condition nor necessarily an evaluated intervention.

This gives four separate axes:

```text
control the future
co-generate the future/action
branch the future by candidate for evaluation
use action only to shape training supervision
```

---

## 10. Supervision map — the counterfactual supervision problem becomes visible

The six papers reveal a recurring asymmetry:

```text
GAIA-1 / Drive-WM:
real data supplies the one factual future that actually happened;
alternative action futures come from generalization of the model.

OccWorld:
factual future occupancy + factual/expert ego future.

WoTE:
can generate many candidate-specific labels and rewards through NAVSIM/PDM,
but surrounding-agent future remains the same logged future across candidate ego actions in the audited path.

ViDAR:
future LiDAR/geometry target, no action branching.

LAW:
factual future latent is the target; current predicted ego trajectory conditions the predictor.
```

Thus:

```text
candidate-specific prediction
!=
candidate-specific ground-truth supervision
!=
reactive counterfactual supervision
```

This distinction should be carried into every later WAM paper.

---

## 11. Strong cross-family counterexamples established by Wave 2

### Counterexample A — visual/world fidelity is not monotonically planning-relevant

OccWorld directly shows higher tokenizer reconstruction fidelity with worse future forecasting and planning.

Therefore the field hypothesis:

```text
higher world fidelity → better planning
```

already has an internal counterexample.

Current status:

```text
COUNTEREXAMPLE EXISTS / claim is context-dependent
```

### Counterexample B — longer future horizon is not monotonically better

LAW's 1.5 s latent target outperforms 3 s and 10 s variants.

Thus:

```text
longer predictive horizon → better planner
```

is also false as a general rule.

### Counterexample C — online rollout is not necessary for a WM objective to improve planning

ViDAR and LAW both improve planning without a future-state rollout being the deployed decision interface.

Thus:

```text
WM helps planning
```

cannot be interpreted as:

```text
planner must imagine futures online and choose among them
```

### Counterexample D — a candidate-specific future is not automatically reactive

WoTE has candidate-specific learned future branches, while its audited candidate supervision evaluates ego alternatives against fixed logged other-agent futures.

Thus:

```text
action-conditioned/candidate-specific WM
```

does not by itself establish correct intervention-dependent social response.

---

## 12. What did the WAM wave actually add beyond Wave 1?

Wave 1 had interaction prediction, future occupancy, planning-oriented representations, multimodal action policies and candidate scoring already.

Wave 2 adds several genuinely distinct capabilities/interfaces:

### Addition 1 — learned future state becomes a reusable decision object

Drive-WM and WoTE make the candidate's predicted future an explicit intermediate object used in action evaluation.

### Addition 2 — world state can be optimized for predictability rather than direct perception semantics

OccWorld, ViDAR and LAW explore occupancy/discrete/latent predictive representations instead of treating RGB reconstruction as the only world state.

### Addition 3 — future prediction becomes a scalable training signal

ViDAR and LAW use future observations themselves to shape planning features, reducing dependence on manually specified perception labels for the world-model branch.

### Addition 4 — world and action modeling become structurally entangled

OccWorld jointly generates ego/world evolution; WoTE and Drive-WM branch future states by action; LAW conditions latent dynamics on the planner output.

These are real transitions. But none of them alone proves behaviorally correct counterfactual reasoning or reactive closed-loop superiority.

---

## 13. Updated interpretation of “planning-centric world model”

After Waves 1–2, the field should no longer be organized by the binary question:

```text
Does the model have a world model?
```

A more informative planning-centric description is:

```text
Observation
→ World state representation
→ Future-model role
→ Action relationship
→ Supervision source
→ Planner interface
→ Evaluation regime
```

For example:

```text
LAW
camera → latent → auxiliary future latent conditioned on predicted ego trajectory
→ factual future-latent supervision
→ shared-feature regularization
→ direct waypoint output

WoTE
camera/LiDAR → compact BEV
→ candidate-conditioned future BEV rollout
→ NAVSIM/PDM multi-candidate non-reactive supervision
→ learned reward
→ candidate selection
```

Both are “world models,” but they solve very different computational problems.

---

## 14. Questions that remain open after Wave 2

Wave 2 is strong enough to close several broad claims but not yet to choose a research gap. The next waves must determine:

1. **Decision compression:** how much world detail can be discarded while preserving action quality? Auto-JEPA/DriveLaW become important here.
2. **Unified world-action generation:** does tighter joint modeling outperform separate future-model + planner interfaces for reasons beyond shared capacity/supervision? Epona/DrivingGPT become key.
3. **Candidate-specific latent futures:** can DA-WAM-type models retain the decision benefits of WoTE/Drive-WM without expensive visual/BEV reconstruction?
4. **Reactive validity:** when later papers claim reactive/causal futures, do alternative ego actions produce behaviorally correct surrounding-agent responses under matched oracle evaluation?
5. **Evaluation transfer:** do gains established on E2/E3 survive E5/E6 interactive closed loop?

These questions organize Wave 3/4; they are not yet gap verdicts.

---

## 15. Wave-2 gate decision

The first comparative deep read and two decision-critical source audits support the following field-level conclusions:

```text
CONTROLLABLE GENERATION != PLANNING INTERFACE
JOINT WORLD-ACTION GENERATION != CANDIDATE CONSEQUENCE EVALUATION
ACTION-CONDITIONED != REACTIVELY SUPERVISED
WM-ASSISTED PLANNING != ONLINE MODEL-BASED PLANNING
WORLD FIDELITY != DECISION UTILITY
LONGER HORIZON != BETTER PLANNING
```

Wave 2 is therefore sufficiently mature to serve as the **world-representation / future-role coordinate system** for later anchors.

Before formally closing Wave 2, the remaining task is a short comparability closeout on:

```text
Drive-WM: isolate world-generation vs reward/perception confounds as far as paper evidence allows
OccWorld: normalize which planning metric/table variants are actually comparable
ViDAR: pin down what downstream components are retained/discarded and matched-pretraining controls
WoTE: integrate the now-resolved non-reactive target-generation audit into the final evidence-strength rating
```

No new paper acquisition is required.