# Paper-first reconstruction — Set C

Status: evidence reconstruction only; **no route naming, no ontology update, no M0–M4 assignment**.

Branch context: `research/core-route-reconstruction`

Papers in this set:

1. LAW — *Enhancing End-to-End Autonomous Driving with Latent World Model*
2. Drive-JEPA — *Video JEPA Meets Multimodal Trajectory Distillation for End-to-End Driving*
3. ViDAR — *Visual Point Cloud Forecasting enables Scalable Autonomous Driving*
4. Latent-WAM — *Latent World Action Modeling for End-to-End Autonomous Driving*
5. Auto-JEPA — *A Latent World Model of Continuous Intent for End-to-End Autonomous Driving*

Primary evidence:

- `papers/raw_md/P0048_LAW/P0048_LAW.raw.md`
- `papers/raw_md/P0049_DriveJEPA/P0049_DriveJEPA.raw.md`
- `papers/raw_md/P0028_ViDAR/P0028_ViDAR.raw.md`
- `papers/raw_md/P0051_AutoJEPA/P0051_AutoJEPA.raw.md`
- Latent-WAM official arXiv full text: `https://arxiv.org/html/2603.24581v1` (no matching local raw-paper artifact was found on this branch at audit time)

This document follows the paper-first reset in `00C_LIVING_FIRST_PRINCIPLES_AUDIT_PAPER_FIRST_RESET.md` and the same discipline used in Sets A and B.

---

## 0. Audit contract

The apparent commonality in this set is deliberately treated as a hypothesis rather than a classification:

```text
predict some future representation
→ obtain a better planner
```

That sentence is too weak to establish mechanism sameness.

For each paper we reconstruct independently:

- what the prediction target actually means;
- what information conditions that prediction;
- whether prediction is a standalone pretraining task or is attached to planner training;
- whether an ego action/proposed trajectory enters the prediction computation;
- which gradients can reach the deployed planning path;
- which predictive modules remain at deployment;
- whether the predicted future object itself is consumed online;
- how the learned representation is converted into a final trajectory;
- what ablations say would disappear if the predictive component were removed.

Only after those facts are reconstructed do we compare the papers.

---

# 1. LAW

## 1.1 Author-stated scientific problem

LAW starts from a representation-learning question rather than an online planning-through-imagination question:

> end-to-end planners consume raw sensor data, so how can the internal scene representation be improved without relying on expensive perception annotations?

The proposed answer is temporal self-supervision. Instead of reconstructing pixels, LAW predicts a future **scene latent** from the current scene latent and the ego trajectory predicted by the planner.

The paper explicitly presents the latent world model as a self-supervised task that can be attached to both perception-free and perception-based end-to-end planners.

## 1.2 Training computation

The current visual encoder produces latent scene features `V_t`.

The ordinary planning decoder first predicts ego waypoints:

```text
current images
→ visual encoder
→ V_t
→ waypoint/planning decoder
→ W_t
```

LAW then makes the planning output part of the predictive-learning branch. The predicted waypoint sequence is flattened and fused into every current visual latent:

```text
(v_t^i, W_t)
→ MLP
→ action-aware latent a_t^i
```

The latent world model predicts the next-frame scene representation:

```text
A_t = {a_t^i}
→ LatentWorldModel
→ V_hat_{t+1}
```

The target `V_{t+1}` is extracted from the factual future frame and the latent prediction receives an MSE loss.

Thus the important causal ordering during training is:

```text
current representation
→ predicted ego trajectory
→ action-aware latent
→ predicted future scene latent
→ future-latent loss
```

This is stronger than generic predictive pretraining. The planner's own predicted trajectory lies on the path to the future-prediction loss. In the paper equations there is no stop-gradient inserted between the predicted waypoints and the latent world model, so the predictive loss is positioned to shape both scene representation and trajectory prediction.

## 1.3 Perception-free and perception-based variants

LAW demonstrates the same self-supervised mechanism in two planner substrates.

Perception-free:

```text
perspective-view visual latents
→ waypoint queries / cross-attention
→ trajectory
```

with total training objective:

```text
L_pf = L_latent + L_waypoint
```

Perception-based:

```text
BEV latents
→ motion/map intermediate heads
→ waypoint decoder
→ trajectory
```

with:

```text
L_pb = L_latent + L_waypoint + L_perception
```

The substrate and auxiliary labels differ, but the LAW-specific intervention remains the same: use the planner-produced action together with the current scene representation to predict the factual future latent.

## 1.4 Deployment graph

The planning decoder itself consumes the **current** scene representation. The predicted `V_hat_{t+1}` is not used by either described planning decoder.

The paper does not provide a separate sentence saying “drop the latent world model at inference,” but its method graph and decoder equations place the latent world model in the training objective rather than on the final sensor-to-waypoint forward path.

The conservative deployment reconstruction is therefore:

```text
images
→ deployable visual/BEV representation
→ planning decoder
→ trajectory
```

not:

```text
images
→ predicted future latent
→ planning decoder
```

## 1.5 What the ablation actually establishes

LAW removes the latent-prediction branch and also tests whether the world model sees current visual latent only or current visual latent plus predicted trajectory.

For the perception-free nuScenes setting:

```text
no latent world model                 avg L2 0.71 / collision 0.41
visual latent only                    avg L2 0.68 / collision 0.37
visual latent + predicted trajectory  avg L2 0.61 / collision 0.30
```

The same ordering appears in the perception-based setting.

This is unusually useful evidence: it does not merely show that temporal supervision helps. It shows that conditioning the future prediction on the planner's own predicted action adds value beyond action-agnostic future-latent prediction.

## 1.6 What LAW is not

LAW is not an online counterfactual evaluator. It does not generate candidate-specific future states and score them at inference.

It is also not merely pretraining followed by transfer. The future-prediction loss is attached while the planner is being optimized, and the predicted action is part of the predictive task.

---

# 2. Drive-JEPA

## 2.1 Author-stated scientific problem is explicitly two-part

Drive-JEPA does not present one monolithic mechanism. It attacks two different bottlenecks:

1. driving representation learning from large-scale video has not scaled effectively into planning;
2. one logged human trajectory per scene gives poor supervision for multimodal driving behavior.

The paper therefore combines two scientific programs:

```text
A. scalable V-JEPA driving-video pretraining
B. simulator-distilled multimodal proposal generation + selection
```

These should not be collapsed into one “world-model route.”

## 2.2 Driving-video pretraining

The pretraining stage adapts V-JEPA to 330 hours of driving video.

The JEPA task predicts masked spatiotemporal target representations using an online encoder/predictor and an EMA target encoder with stop-gradient.

Critically, this pretraining objective is **not ego-action-conditioned world transition learning**. The prediction target is a masked video representation; no proposed driving action is required to define the transition.

The product that transfers is the visual encoder.

## 2.3 Simple perception-free planner

The paper deliberately attaches a minimal decoder to the pretrained encoder to test whether the representation itself is useful for planning:

```text
front-view video/history
→ pretrained ViT encoder
→ spatiotemporal features F_t
→ simple Transformer waypoint decoder
→ trajectory
```

The downstream planner is trained with trajectory MSE. Implementation details assign the ViT encoder a smaller but non-zero learning rate than the planner, so the transferred encoder is further adapted rather than being strictly frozen.

This simple planner is scientifically important because it isolates the value of driving-video pretraining. The paper reports 89.0 PDMS for its driving-domain V-JEPA representation with the simple decoder, versus 86.1 for the original V-JEPA 2 checkpoint in the same comparison.

## 2.4 Full proposal-centric planner is a second mechanism layered on top

The complete Drive-JEPA planner uses the same visual representation as input to an online proposal generator.

It iteratively refines trajectory proposals around explicit waypoint anchors using WADA / feature sampling:

```text
F_t + ego status
→ proposal queries
→ waypoint proposals
→ iterative proposal refinement
```

The multimodality problem is addressed not by a future-world predictor but by offline simulator distillation.

A large trajectory vocabulary is scored with a rule-based simulator. Multiple high-quality trajectories become pseudo-teachers. The proposal generator is trained toward both the logged human trajectory and those simulator-approved alternatives.

The final proposals are then scored by a learned proposal scorer supervised by simulator-derived driving-quality labels, with an additional momentum/comfort correction from the previously selected trajectory.

Deployment is therefore approximately:

```text
current visual representation
→ online trajectory proposals
→ learned proposal scores + temporal comfort correction
→ argmax trajectory
```

There is no online V-JEPA future-prediction operation in this final path.

## 2.5 Ablations separate the contributions rather than merging them

The paper's NAVSIM-v2 component ablation distinguishes:

- M1: generic V-JEPA 2 initialization;
- M2: driving-domain video pretraining;
- M3: multimodal trajectory distillation;
- M4: momentum-aware trajectory selection.

The driving-domain pretraining alone improves the planner over the generic V-JEPA representation. The trajectory-distillation module changes proposal diversity but can damage comfort; the momentum selector repairs that temporal-instability cost.

This confirms that representation pretraining and proposal/selection are separable interventions with different failure modes.

## 2.6 Pressure on the old PF/PB split

Earlier project artifacts separated Drive-JEPA's simple direct-decoder setting and proposal/selection settings into distinct planning artifacts because their final commitment topologies differ.

That difference is real at the **action-commitment** level.

But Set C shows that treating them as entirely separate **predictive-world mechanisms** overstates the distinction.

Both inherit the same core V-JEPA driving representation program. The full planner then adds a second, simulator-distilled proposal/selection program on top.

A more faithful paper reconstruction is therefore compositional:

```text
shared predictive-representation acquisition
    ├─ simple direct waypoint decoder        [representation probe / usable planner]
    └─ proposal generator + distillation + selector   [full planning program]
```

This is a correction to how strongly the prior PF/PB artifact split should be interpreted, not an ontology amendment.

---

# 3. ViDAR

## 3.1 Author-stated problem

ViDAR predates the recent WAM framing and asks a broader question:

> what scalable pretext task can make a visual driving encoder simultaneously learn semantics, 3D geometry, and temporal dynamics for downstream perception, prediction, and planning?

Its answer is **visual point-cloud forecasting**.

## 3.2 Pretraining computation

Historical multi-view images are encoded into BEV features by a History Encoder. A Latent Rendering operator reshapes those features into a geometry-aware latent space. An autoregressive Future Decoder predicts future BEV/occupancy states, from which future point clouds are rendered and supervised against LiDAR-derived targets.

Simplified:

```text
historical images
→ History Encoder
→ BEV representation
→ Latent Rendering
→ autoregressive Future Decoder
→ future occupancy / point cloud
→ forecasting loss
```

The History Encoder is explicitly the structure intended to transfer downstream.

## 3.3 Deployment/downstream lifecycle

After pretraining, the encoder initializes ordinary downstream systems such as BEVFormer, OccNet, and UniAD.

The point-cloud forecasting decoder is not the mechanism through which UniAD chooses a trajectory online. Planning improvement comes through the transferred encoder representation.

Thus ViDAR is much closer to:

```text
predictive pretext task
→ representation acquisition
→ downstream fine-tuning
```

than to an online world-model planner.

This makes it a useful adjacent pressure case even if one later decides it is outside the narrow WAM + one-stage domain boundary.

## 3.4 The most important negative result

ViDAR contains an ablation that directly warns against equating “future prediction” with “better predictive representation.”

A straightforward forecasting setup using differentiable ray-casting actually hurts downstream detection:

```text
baseline without forecasting pretrain     44.11 NDS
naive forecasting + ray-casting            40.20 NDS
forecasting + Latent Rendering              47.58 NDS
```

So the future-prediction objective by itself is not sufficient.

The representation interface created by the pretext task matters. ViDAR's scientific contribution is not simply “forecast the future”; it is that the Latent Rendering bottleneck forces the transferable encoder to organize geometry in a downstream-useful way.

This is strong evidence against a coarse category based only on the existence of future prediction.

## 3.5 Planning evidence

When transferred into UniAD, ViDAR improves the reported planning displacement error and average collision rate (roughly 15% collision reduction), together with perception and motion-prediction metrics.

That demonstrates transfer utility, but the planning computation itself remains UniAD's downstream computation rather than ViDAR's Future Decoder.

---

# 4. Latent-WAM

## 4.1 Author-stated problem

Latent-WAM argues that previous latent world-model planners underuse three things:

- compression;
- spatial/geometric understanding;
- historical/longer-range dynamics.

It therefore combines two representation-shaping programs before trajectory decoding:

1. Spatial-Aware Compressive World Encoder (SCWE): compress scene tokens and distill geometry from a frozen foundation model;
2. Dynamic Latent World Model (DLWM): predict future world-status representations causally from historical scene + ego-status representations.

## 4.2 Current world status

SCWE compresses image patch tokens into a small set of learnable scene tokens.

Scene tokens from different cameras are aggregated and concatenated with ego-status embeddings containing command, velocity, and acceleration:

```text
multi-view images
→ SCWE
→ compressed scene tokens

command + velocity + acceleration
→ ego-status embedding

scene tokens + ego status
→ S_world^t
```

This `S_world^t` is used both as the substrate for future-world training and as the representation read by the trajectory decoder.

## 4.3 Dynamic latent prediction is a training-time representation-shaping program

DLWM is a causal Transformer that predicts future world-status blocks from historical factual world-status blocks.

Targets are produced by an EMA copy of the SCWE. Teacher forcing supplies factual historical world-status context during training.

Unlike LAW, the planner's **predicted future trajectory is not the conditioning action** for DLWM. The dynamics input includes historical scene and ego-status information, but the trajectory decoder's proposed future path does not feed into the world transition equation described by the paper.

This difference is mechanistic, not merely architectural:

```text
LAW:
current state + planner-predicted trajectory
→ future latent loss

Latent-WAM:
historical scene/ego-status blocks
→ future world-status loss
```

## 4.4 Trajectory planning and deployment

The trajectory decoder reads the **current** world status `S_world^t` and trajectory queries, then emits command-conditioned trajectory candidates.

The paper is explicit about inference:

```text
inference = SCWE + Trajectory Decoder only
```

DLWM, EMA target encoder, geometric foundation teacher, and future-status decoders are not required online.

So Latent-WAM should not be reconstructed as runtime latent rollout planning.

Its predictive world model shapes the representation during joint end-to-end training; the deployable product is the current compact world representation plus trajectory decoder.

## 4.5 Ablations show that “world modeling” is only one part of the gain

Progressive NAVSIM-v2 ablations report approximately:

```text
base image-patch planner                          87.9 EPDMS
compression only                                 87.7
compression + world model                        88.0
compression + world model + ego supervision      88.3
compression + geometry                           88.6
compression + geometry + world model             89.0
full                                              89.3
```

Two lessons follow.

First, geometry distillation contributes at least as strongly as the dynamic prediction branch in these matched ablations. The paper is genuinely compositional; “future prediction” does not explain the whole method.

Second, more temporal prediction targets are not monotonically better. Predicting a moderate multi-step history/future sequence reaches 89.3, while a denser stride-2 sequence gives 89.1. The authors attribute this partly to adjacent-frame redundancy and optimization cost.

Again, the useful question is not simply whether future prediction exists, but what prediction schedule and representation bottleneck shape the deployable state.

---

# 5. Auto-JEPA

## 5.1 Author-stated scientific proposition

Auto-JEPA attacks the definition of the prediction target itself.

Its claim is that planning does not need a dense model of the complete future environment. The predictive target should instead retain only scene information that matters for the ego vehicle's future action.

It operationalizes that idea by predicting the latent representation of the **future ego trajectory**.

This is a major semantic departure from the other four papers in the set.

## 5.2 Stage 1: define the future-ego target space

A trajectory autoencoder is trained on factual future ego trajectories.

The trajectory encoder maps eight future waypoints into eight latent tokens. After this stage:

- the decoder is discarded;
- the trajectory encoder is frozen;
- the same encoder is used both to produce intent targets and to embed every trajectory in a retrieval memory.

Thus the target space is intentionally executable-action geometry, not a scene/world-state representation.

## 5.3 Stage 2: predict future intent from current context

A frozen V-JEPA 2 visual encoder extracts visual tokens from current/history frames. Ego-motion history and route command are separately encoded.

A JEPA predictor produces an eight-token future-intent latent:

```text
visual context + ego history + route command
→ predicted future ego-motion latent Z_hat
```

Training aligns `Z_hat` with the frozen trajectory-encoder representation of the factual future ego trajectory using feature, cosine, and contrastive objectives.

## 5.4 Runtime: the predicted future latent is directly actionized

This is the critical distinction from LAW, ViDAR, Drive-JEPA pretraining, and Latent-WAM.

At inference, `Z_hat` is not discarded after representation learning. It is the retrieval key into a fixed memory of 110k+ executable recorded trajectories:

```text
current scene/context
→ predicted future intent Z_hat
→ cosine retrieval from trajectory memory
→ Top-300 candidates
→ scene-conditioned scorer + drivable-area gate
→ final trajectory
```

The predicted future object is therefore on the live causal path to final action commitment.

## 5.5 Forward coupling and learning coupling are different

Auto-JEPA is a useful continuation of the Set B lesson.

Forward/deployment dependence is strong:

```text
predicted intent
→ candidate identity set
→ final action
```

But the final scorer is trained separately. The paper states that scorer training propagates no gradients into the visual encoder, JEPA predictor, or trajectory memory.

So selection quality does not end-to-end reshape the intent predictor through the final utility loss.

This gives a concrete example where runtime causal dependence is strong while backward/learning coupling from final selection is deliberately weak.

## 5.6 Component ablation

Replacing scene-conditioned predicted intent with a fixed codebook medoid collapses PDMS from 91.3 to 52.6.

Intent-based retrieval plus feasibility gate, even without the learned utility scorer, reaches 87.6. Adding the scorer contributes another 3.7 PDMS points; the gate has a smaller but measurable effect on DAC.

This is unusually direct evidence that the predicted future-intent latent is not decorative representation supervision. It is a necessary actionization variable in the deployed planner.

## 5.7 Scope ambiguity that must remain open

Auto-JEPA calls this an action-oriented latent world model.

Mechanistically, however, its prediction target is the ego's future action/motion representation, not a state describing environment evolution.

That makes it a high-value boundary case for the project:

> how much of “world modeling” may be compressed away before the predictive object becomes an action model rather than a world model?

Set C does not answer that scope question. It only establishes the causal facts needed to answer it later.

---

# 6. Side-by-side comparison after independent reconstruction

The five papers all exploit future-related prediction, but the phrase `predictive representation` hides several independent facts.

| Paper | Prediction target | Prediction conditioning | Training attachment | Predictor/output at deployment | How world/future knowledge reaches action |
|---|---|---|---|---|---|
| LAW | next factual scene latent | current latent + **planner-predicted ego trajectory** | joint with planner | future predictor not on stated planning path | predictive loss shapes current representation and planner through action-aware branch |
| Drive-JEPA | masked spatiotemporal video representation | masked driving video context | standalone large-scale pretraining, then downstream adaptation | JEPA predictor absent; encoder retained | pretrained/adapted visual representation feeds direct or proposal planner |
| ViDAR | future point cloud via future BEV/occupancy | historical multi-view images | standalone pretraining before downstream fine-tuning | forecasting decoder absent downstream | pretrained History Encoder initializes downstream stack |
| Latent-WAM | future scene+ego world-status representation | historical factual scene + ego status | joint end-to-end auxiliary dynamics objective | DLWM absent; current SCWE state retained | future-loss + geometry distillation shape current compact world state used by planner |
| Auto-JEPA | future **ego-trajectory latent** | visual context + ego-motion history + route command | task-specific intent-predictor training | predicted latent remains online | predicted intent directly retrieves candidate trajectories |

This table is descriptive, not a taxonomy.

---

# 7. Main Set C corrections

## 7.1 “Future prediction” is not a sufficient mechanism description

At minimum, a faithful reconstruction needs to answer:

```text
1. target semantics: what future object is predicted?
2. conditioning: what variables define the prediction?
3. optimization attachment: pretraining, joint planner loss, or separate task stage?
4. backward reach: which deployed planner parameters can the predictive loss change?
5. deployment fate: is the predictor/output retained online?
6. actionization: if retained, how does it alter the final trajectory?
```

These are audit questions only. They are not promoted as ontology axes.

## 7.2 Pretraining transfer and joint planner-coupled prediction should not be conflated

ViDAR and Drive-JEPA use future/predictive objectives primarily to acquire an encoder that is later transferred or adapted downstream.

LAW and Latent-WAM attach predictive losses directly to the representation being optimized together with planning.

That lifecycle difference changes the learning graph even when all four papers can be described verbally as “future prediction improves planning representation.”

## 7.3 LAW adds a further dependency that Latent-WAM does not

LAW makes the planner's own predicted trajectory an input to future-latent prediction. Its world loss therefore evaluates whether the current representation and predicted action jointly explain the factual future representation.

Latent-WAM predicts future world-status from historical scene and ego-status blocks but does not condition the stated transition on the planner's proposed future trajectory.

This distinction survives full-paper reading and LAW's action-conditioning ablation.

## 7.4 ViDAR is a negative control against objective-only reasoning

ViDAR demonstrates that adding a future-forecasting objective can worsen downstream representation quality if the representation interface is wrong.

Therefore no future taxonomy should infer “world/predictive representation mechanism” solely from the presence of a forecasting loss.

The architecture of the learning bottleneck and the representation actually transferred downstream matter causally.

## 7.5 Auto-JEPA reverses the lifecycle

In LAW, Drive-JEPA, ViDAR, and Latent-WAM, the explicit future-prediction machinery is principally a learning device; deployment action uses the learned current representation.

In Auto-JEPA, the predicted future latent itself remains online and determines which trajectory candidates even enter the final scorer.

That is a genuine causal difference, but Set C does not yet decide whether it deserves an ontology category, modifier, or simply a graph-level descriptor.

## 7.6 Drive-JEPA PF/PB should not be treated as proof of separate predictive-world routes

The simple direct decoder and the full proposal-selection planner have different final commitment structures.

But the paper's predictive-representation program is shared: both consume features acquired through the same driving-domain V-JEPA pretraining.

The full planner adds multimodal simulator distillation and candidate selection as an additional mechanism.

Therefore the old artifact split remains useful for action-path regression, but it should no longer be read as evidence that Drive-JEPA contains multiple different ways of acquiring world/predictive knowledge.

---

# 8. Questions intentionally left unresolved

1. **Auto-JEPA scope:** is a predictor whose target is only future ego motion still a world model for this project's domain, or is it a planning/action predictive model using a JEPA learning principle?
2. **Predictive-target granularity:** do scene-state, geometry, masked-video, and future-action targets form meaningful mechanism families, or are they better treated as target semantics attached to deeper causal programs?
3. **Pretraining vs joint optimization:** is lifecycle itself field-defining, or merely one coordinate needed to reconstruct learning graphs?
4. **Action-conditioned prediction:** LAW gives strong evidence that this relation matters locally. More papers are needed before judging whether it generalizes.
5. **Forward vs backward dependency:** Auto-JEPA and Set B jointly show these can diverge sharply. More target-domain examples are needed before formal promotion.

No answer is forced in this set.

---

# 9. Provisional reading discipline after Set C

For future paper-first batches, whenever a paper claims that prediction/world modeling “improves the planner,” record two graphs plus a target statement:

```text
A. Prediction target statement
   What exactly is being predicted?

B. Learning / backward graph
   Which future/world loss can modify which deployable parameters?

C. Forward / deployment graph
   Which learned or predicted object is actually read before final action commitment?
```

This is an audit protocol, not a replacement ontology.

Set C strengthens the same methodological conclusion reached in Sets A and B:

> do not classify from nouns such as `world model`, `JEPA`, `future latent`, `predictive representation`, or `pretraining`.
>
> Reconstruct the causal program first, then ask whether a recurring distinction survives across papers.
