# Set C relational + core-mechanism deletion audit

Status: evidence audit only. **No route naming, no ontology update, no R/W/E/L projection, no M0–M4 assignment.**

Branch context: `research/core-route-reconstruction`

Primary reconstruction: `18_PAPER_FIRST_RECONSTRUCTION_SET_C.md`

Papers:

- LAW — *Enhancing End-to-End Autonomous Driving with Latent World Model*
- Drive-JEPA — *Video JEPA Meets Multimodal Trajectory Distillation for End-to-End Driving*
- ViDAR — *Visual Point Cloud Forecasting enables Scalable Autonomous Driving*
- Latent-WAM — *Latent World Action Modeling for End-to-End Autonomous Driving*
- Auto-JEPA — *A Latent World Model of Continuous Intent for End-to-End Autonomous Driving*

Additional evidence checked after the first reconstruction:

- official Drive-JEPA repository, including the separate perception-free and perception-based agents;
- official Latent-WAM arXiv full text (`arXiv:2603.24581`), especially Sec. 3.3–3.5;
- official LAW repository/project description where useful for lifecycle confirmation.

The goal of this note is deliberately narrower than classification. It asks two questions:

1. If the paper's predictive/world mechanism is deleted, what scientific claim and what computation disappear?
2. When two papers look similar, is the commonality actually the paper's core idea, or only one replaceable implementation property?

---

## 1. Why deletion is useful here

The phrase

```text
predict the future -> improve planning
```

is too weak to reconstruct research routes. All five papers can be described this way, but the prediction occupies a different place in each system.

The deletion test therefore removes the predictive/world component conceptually and asks:

- does the deployed planner still have a valid forward path?
- does only training supervision disappear?
- does the representation entering the planner change?
- does the final action-selection procedure become impossible?
- does the paper lose its main scientific claim, or only one auxiliary enhancement?

This test is not a new axis. It is a guard against classifying papers from nouns such as `world model`, `JEPA`, `future latent`, or `pretraining`.

---

# 2. LAW deletion test

LAW training is approximately:

```text
current image
-> current visual latent V_t
-> planner
-> predicted ego trajectory W_t

(V_t, W_t)
-> action-aware latent
-> latent world model
-> predicted factual future scene latent V_hat_{t+1}
-> latent prediction loss against V_{t+1}
```

Deployment is reconstructed conservatively as:

```text
image
-> current visual/BEV representation
-> planning decoder
-> trajectory
```

The predicted future latent is not an online input to the described planning decoder.

### Delete the latent-world branch

The deployed sensor-to-trajectory path still exists.

What disappears is the **action-conditioned temporal self-supervision** that jointly shapes scene representation and the trajectory predictor.

This matters because LAW's ablation separates:

```text
no future-latent prediction
< action-agnostic future-latent prediction
< future-latent prediction conditioned on predicted trajectory
```

So the paper's world-model contribution is not merely "future supervision". The planner's own predicted trajectory participates in the training-time dynamics-prediction problem.

### Provisional factual statement

LAW's predictive component is **causally essential to the learning program but not evidenced as an online future-state mediator at deployment**.

Do not convert that sentence into a route label yet.

---

# 3. Drive-JEPA deletion test

Drive-JEPA must be tested compositionally because the paper explicitly attacks two bottlenecks.

Program A:

```text
large driving-video corpus
-> V-JEPA masked latent prediction
-> predictive visual encoder
-> downstream planning representation
```

Program B:

```text
current representation
-> online proposal generation/refinement
-> simulator-distilled multimodal proposal supervision
-> learned proposal scorer
-> momentum correction
-> final trajectory
```

## 3.1 Delete V-JEPA driving-video pretraining

Both the simple perception-free decoder and the proposal-centric planner remain architecturally possible.

What disappears is the paper's first scientific claim: scalable predictive video representation acquisition aligned with driving planning.

The full planner therefore does **not** depend on running a V-JEPA predictor online. It depends on the encoder representation produced by the predictive pretraining program.

## 3.2 Delete proposal/distillation/selection program

The simple perception-free planning experiment still exists:

```text
pretrained ViT features
-> simple Transformer waypoint decoder
-> trajectory
```

What disappears is the second scientific program: multimodal proposal generation beyond a single logged human future, plus simulator-derived ranking and temporal stabilization.

Thus the complete Drive-JEPA paper is not one indivisible mechanism.

---

# 4. Drive-JEPA PF/PB re-audit

This is the most important pressure case in Set C because the previous ontology treated the PF and PB artifacts as strongly separated planning routes.

## 4.1 What is genuinely different

The official code confirms two distinct downstream agents.

Perception-free agent:

- reads camera/history features and ego status;
- feeds them to the Drive-JEPA model;
- outputs one trajectory;
- is trained directly with trajectory loss;
- does not perform online candidate scoring/resolution.

Perception-based/full agent:

- generates trajectory proposals;
- obtains simulator-derived proposal targets during training;
- trains proposal score heads and proposal-centric auxiliary predictions;
- selects from the proposal set at deployment.

So the downstream **actionization / commitment computation really is different**.

## 4.2 What is shared

Both are presented by the authors under the same Drive-JEPA framework and inherit the same central predictive-representation program: driving-domain V-JEPA pretraining produces the visual encoder representation used by planning.

The paper itself treats the simple decoder as evidence for the representation-learning claim, then builds the complete proposal-centric planner as an additional solution to multimodal action supervision.

A faithful reconstruction is therefore:

```text
                V-JEPA driving representation
                          |
             ---------------------------
             |                         |
      simple trajectory decoder   proposal-centric planner
                                  + simulator distillation
                                  + learned selection
```

## 4.3 What this means for the old split

The old split is **valid as an artifact-level deployment distinction**.

It is not automatically valid as evidence for two different **world-model research routes**.

If a taxonomy asks "how does the final action get committed?", PF and PB should differ.

If the scientific question is "what role does predictive world/video learning play in this paper?", the two settings share the same upstream world-learning program and differ mainly in the downstream planner added on top.

This is exactly the type of case where forcing one paper into one leaf, or treating every task mode as a different research lineage, can distort the paper's actual contribution.

No ontology change is made here. This is a warning about the level of abstraction.

---

# 5. ViDAR deletion test

ViDAR pretraining is approximately:

```text
historical images
-> History Encoder
-> geometry-aware Latent Rendering
-> Future Decoder
-> future occupancy / point cloud
-> forecasting supervision
```

The History Encoder is then transferred into downstream perception/prediction/planning systems.

### Delete forecasting pretraining

The downstream BEVFormer / OccNet / UniAD architecture still exists.

What disappears is the predictive pretraining signal used to organize the encoder representation.

Crucially, ViDAR contains a negative result:

```text
no forecasting pretrain                    44.11 NDS
naive forecasting with ray-casting         40.20 NDS
forecasting with Latent Rendering           47.58 NDS
```

Therefore even within "future-prediction pretraining", the way the predictive task constrains the transferable representation is scientifically important.

This prevents the following invalid inference:

```text
future prediction exists
=> predictive representation is useful
=> same mechanism as every other predictive-pretraining paper
```

The middle implication is empirically false in ViDAR's own ablation.

---

# 6. Latent-WAM deletion test

Official full-text verification clarifies the lifecycle very strongly.

Training:

```text
multi-view images
-> SCWE
-> compressed scene tokens

scene tokens + command/velocity/acceleration
-> frame-wise S_world

historical S_world
-> DLWM causal prediction
-> future scene+ego world-status target
-> world-model + ego-status losses

current S_world^t
-> trajectory decoder
-> candidate trajectories conditioned on command
```

The paper explicitly states that at inference **only the Spatial-Aware Compressive Encoder and Trajectory Decoder are required**. DLWM and the geometric foundation teacher do not add inference computation.

## 6.1 Delete DLWM

The deployed path remains structurally valid:

```text
images
-> SCWE
-> current S_world^t
-> trajectory decoder
-> trajectory
```

What disappears is the temporal-dynamics learning program that shapes the online representation.

## 6.2 Delete SCWE

This is more destructive. SCWE is not merely a training teacher; it is the online representation producer consumed by the trajectory decoder.

So Latent-WAM itself already contains components with different lifecycle roles:

- geometric foundation model: training teacher;
- DLWM: training-time dynamics shaper;
- SCWE/world-status representation: deployment state;
- trajectory decoder: deployment action generator.

Treating the whole paper as one atomic world-model mechanism would erase this internal composition.

## 6.3 Difference from LAW that should not be erased

LAW's predictive branch is conditioned on the **planner's predicted trajectory**.

Latent-WAM's DLWM predicts future scene+ego world status from **historical world status**, where ego status is command/velocity/acceleration; the future planner trajectory is not used as the transition condition in the same way.

Both improve deployed planning through training-time predictive learning, but the causal learning problem is different.

This difference may or may not eventually define a scientific branch. Set C does not promote it.

---

# 7. Auto-JEPA deletion test

Auto-JEPA is the strongest counterexample to treating every JEPA/predictive-latent paper as a representation-pretraining paper.

Training constructs a latent space from future ego trajectories and learns:

```text
current visual context + ego-motion history + route command
-> predicted future ego-motion intent latent
```

At deployment the predicted intent is not discarded. It is the retrieval key:

```text
predicted intent
-> retrieve Top-K trajectories from trajectory memory
-> scene-conditioned scorer
-> drivable-area gate
-> final trajectory
```

### Delete the intent predictor

The deployment pipeline loses the mechanism that retrieves scene-appropriate trajectories. The paper's component ablation supports this: replacing scene-conditioned predicted intent with a fixed codebook medoid severely degrades planning.

Therefore Auto-JEPA's predictive object is not merely a training regularizer or transferred representation. It is an **online decision variable**.

But there is an equally important semantic warning: its prediction target is the representation of the **future ego trajectory itself**, not a dense or structured future environment state.

This makes Auto-JEPA a pressure case for the definition of "world model", not evidence that every future-action latent should automatically be admitted as a world state.

---

# 8. Pairwise observations that survived the full-text reconstruction

These are relations, not classes.

## LAW vs Latent-WAM

Shared observation:

- predictive temporal learning can shape the representation used by a planner while the explicit future predictor is unnecessary at inference.

Important difference:

- LAW: planner-predicted trajectory conditions future scene-latent prediction;
- Latent-WAM: historical scene+ego-status states drive autoregressive future-status prediction.

Do not collapse them into "training-only latent WM" without preserving this difference.

## Drive-JEPA vs ViDAR

Shared observation:

- a predictive pretext program produces an encoder that is then reused by downstream planning;
- the explicit predictor/decoder is not the online planning mechanism.

Important difference:

- Drive-JEPA uses masked video joint-embedding prediction and emphasizes scalable driving-video representation learning;
- ViDAR predicts future 3D point clouds through a geometry-enforcing representation bottleneck and is a general pretraining method for multiple downstream tasks.

The common lifecycle is real; whether it defines a target-domain WAM route remains unresolved because ViDAR itself may be adjacent rather than a WAM+one-stage method.

## Drive-JEPA vs LAW

Both can be casually described as "predictive latent learning for planning", but the learning program differs:

- Drive-JEPA predictive learning is an upstream video pretraining stage independent of the downstream planned trajectory;
- LAW attaches the future-prediction loss to planner training and explicitly conditions the prediction on the planner's predicted trajectory.

This is a scientifically meaningful distinction even though both deploy without an explicit future rollout.

## Drive-JEPA vs Auto-JEPA

The shared word `JEPA` is misleading if used for taxonomy.

- Drive-JEPA: JEPA prediction is primarily representation acquisition; downstream planner consumes the encoder representation.
- Auto-JEPA: JEPA prediction outputs the future-ego intent latent that directly determines which trajectories are retrieved online.

Same learning family name, different operational role.

## LAW vs Auto-JEPA

- LAW predicts a future **scene representation** during training; the planner consumes current representation at deployment.
- Auto-JEPA predicts a future **ego-motion representation** at deployment; that prediction directly structures the candidate set.

Their predictive targets and lifecycle roles are both different.

---

# 9. What Set C currently supports — and what it does not

Set C supports several methodological statements.

### Supported observation 1: "future prediction" is not a mechanism identity

The same phrase covers:

- planner-conditioned scene-latent supervision;
- masked-video representation pretraining;
- future point-cloud pretraining;
- autoregressive world-status supervision;
- online future-ego-intent prediction.

These cannot be treated as one route solely because each predicts something future-related.

### Supported observation 2: deployment role matters, but deployment topology alone is also insufficient

The deployment graph reveals whether a predictive object directly mediates action.

However, Drive-JEPA shows that two downstream deployment topologies can share the same upstream world-learning contribution. Therefore final action topology alone can over-separate one paper's scientific program.

### Supported observation 3: papers are compositions

At least Drive-JEPA and Latent-WAM are naturally reconstructed as combinations of mechanisms with different lifecycle roles.

A future ontology may need to represent a paper as a composition rather than force one paper/task mode into one mutually exclusive leaf.

This is a hypothesis about representation format, not yet a proposed ontology design.

### Supported observation 4: target semantics cannot be ignored

Auto-JEPA exposes a boundary problem. Predicting a future ego-trajectory latent is operationally predictive and decision-relevant, but it may not satisfy a strict definition of modeling the external world/dynamics.

The WAM domain gate must eventually resolve this without relying on paper branding.

### Not supported

Set C does **not** establish:

- a new route family;
- a new primary axis;
- that training-only predictive methods form one class;
- that action-conditioned learning must be a separate class;
- that Auto-JEPA is definitively IN-DOMAIN or OUT-OF-DOMAIN;
- that Drive-JEPA PF/PB should be merged in all analyses;
- that the earlier R/W/E/L or M0–M4 structures have been repaired.

---

# 10. Strongest correction to the previous research process

The unit of scientific comparison cannot be assumed in advance.

Three different units are all legitimate for different questions:

```text
paper
component / scientific program
runtime artifact / task mode
```

Drive-JEPA demonstrates why confusing them is dangerous:

- paper level: one framework with two explicit bottlenecks;
- program level: predictive representation acquisition + multimodal action supervision/selection;
- runtime artifact level: direct-decoder PF path vs candidate-resolved PB/full path.

The old ontology often promoted runtime-artifact differences into headline research-route differences. Set C shows this can be scientifically misleading.

The corrective rule for the next paper-first sets is therefore:

> First reconstruct the paper's scientific programs and their training/deployment graphs. Only afterward decide which comparison unit is appropriate for the question being asked.

Do not assume that `paper`, `mode`, `artifact`, or `module` is always the correct classification unit.

---

# 11. Next pressure target

The most valuable next set is not another predictive-representation set. It should attack the previous assumption that "joint world-action generation" is naturally one route.

Recommended Set D for independent reconstruction:

- OccWorld
- DrivingGPT
- GenAD
- Gen-Drive
- Discrete-WAM

The pre-registration question is deliberately weak:

> These papers all appear to entangle future scene/world variables with ego action variables. Are they actually solving the same scientific problem and using the same causal program, or have we again grouped together methods that merely share one visible architectural property?

No `joint-generation` class should be assumed before the five full reconstructions are complete.
