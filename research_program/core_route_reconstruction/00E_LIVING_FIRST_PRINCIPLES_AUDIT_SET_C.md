# Living first-principles audit — Set C continuation

Status: research reasoning log. This file records why our interpretation changed; it is **not** a normative ontology artifact.

Related evidence files:

- `18_PAPER_FIRST_RECONSTRUCTION_SET_C.md`
- `19_SET_C_RELATIONAL_DELETION_AUDIT.md`

---

## 1. Why Set C was selected

After Sets A and B, we still had an unresolved warning from Drive-JEPA: the existing ontology placed its perception-free and perception-based/full planning settings far apart, even though the authors clearly present them as one larger research program.

The danger was that we might once again be classifying the visible shape of the final planner rather than understanding the scientific idea of the paper.

Set C therefore grouped five papers that could all superficially be described as:

```text
future/predictive learning -> better planning
```

The purpose was to test whether that apparent family survived full reconstruction.

It did not survive in that simple form.

---

## 2. First correction: prediction target is not enough

LAW, Drive-JEPA, ViDAR, Latent-WAM and Auto-JEPA all predict something related to the future, yet the prediction has a different causal job in each paper.

LAW:

```text
planner predicts trajectory
-> trajectory conditions future-scene-latent prediction
-> prediction loss shapes planner/representation
```

Drive-JEPA:

```text
masked driving-video prediction during pretraining
-> learned encoder
-> downstream planner
```

ViDAR:

```text
future point-cloud forecasting during pretraining
-> geometry-aware encoder
-> downstream UniAD / other tasks
```

Latent-WAM:

```text
historical scene+ego world status
-> causal future world-status prediction during training
-> dynamics-informed current world representation
-> trajectory decoder
```

Auto-JEPA:

```text
current scene
-> future ego-motion intent prediction
-> trajectory retrieval at inference
-> scorer/gate
-> final trajectory
```

So "predictive latent" cannot be a route identity.

---

## 3. Second correction: deployment-only taxonomy can also fail

Earlier we correctly learned that training and deployment must be distinguished. But Set C exposes the opposite overcorrection: if we classify only from the final deployment graph, we may split one scientific program too aggressively.

Drive-JEPA is the cleanest example.

The perception-free experiment has a direct trajectory decoder. The complete/perception-based system has proposal generation and candidate selection. Their runtime commitment topology differs substantially.

However, the world/predictive contribution that motivates the paper is shared: both consume the representation learned by driving-domain V-JEPA pretraining.

Therefore:

```text
runtime artifact difference != automatically different world-model research idea
```

This is a major warning against treating final commitment topology as the universal headline taxonomy.

---

## 4. Third correction: the scientific unit is not fixed

We previously behaved as though the correct unit of classification were known:

```text
paper/code version × task mode × planning path
```

That unit was useful for regression because it prevents hidden mode changes. But it is not necessarily the right unit for discovering scientific routes.

Drive-JEPA naturally has at least three views:

```text
paper: one framework
scientific programs: predictive representation + multimodal action supervision/selection
runtime artifacts: direct PF decoder vs proposal-resolved PB/full planner
```

All three descriptions are true.

The mistake is promoting one level into the only ontology level.

For future reconstruction, we must determine the comparison unit *after* understanding the paper, not before.

---

## 5. Fourth correction: "training-only world model" is still too coarse

LAW, ViDAR and Latent-WAM all have predictive computations that are unnecessary as explicit future predictors at deployment, but they are not interchangeable.

LAW's planner-produced trajectory conditions the future prediction objective.

ViDAR is a standalone general pretraining program whose key contribution includes the geometry-shaping Latent Rendering interface.

Latent-WAM trains an autoregressive world-status model over historical scene and ego status while its deployed trajectory decoder reads current compressed world status.

So even after lifecycle is fixed, the learning bridge remains scientifically different.

This means the old temptation to make one large bucket such as

```text
world model used in training, removed at deployment
```

would simply recreate W0 under a new name.

---

## 6. Fifth correction: Auto-JEPA is a domain-definition pressure case

Auto-JEPA is especially useful because the authors call it an action-oriented latent world model, yet its prediction target is the latent representation of the future ego trajectory itself.

The predicted latent is genuinely causal at deployment: it retrieves the candidate trajectories.

But the target is not obviously an external future world state.

This creates two separate questions that must not be merged:

1. Is the predicted latent important to online planning? — clearly yes.
2. Does predicting future ego-motion intent qualify as world modeling for our WAM domain? — unresolved.

This is exactly why the WAM membership gate and the route taxonomy must be separate research problems.

---

## 7. The core-mechanism deletion test proved useful

The deletion test gave a more stable description than early route naming.

If the predictive component is removed:

- LAW still has a deployable planner, but loses action-conditioned temporal self-supervision.
- Drive-JEPA still has planner architectures, but loses the predictive representation acquisition program.
- ViDAR still has downstream systems, but loses its forecasting-based encoder pretraining.
- Latent-WAM still has an inference path if DLWM is removed, but loses the temporal-dynamics shaping of its deployed world representation.
- Auto-JEPA loses the online intent signal required for trajectory retrieval, so the deployment decision process itself breaks.

This does **not** define five classes. It reveals where each paper's scientific intervention sits.

That is exactly what we need before classification.

---

## 8. Current methodological stance

Do not ask first:

> which route is this paper?

Ask first:

```text
What scientific problem is the paper attacking?
What computation is introduced to solve it?
What is learned?
What remains online?
What does the final planner actually consume?
What changes if the proposed mechanism is deleted?
Which parts are one program and which are separate programs composed in the same paper?
```

Only when these answers have been reconstructed across enough papers should recurring structure be promoted.

---

## 9. Set C does not rescue any previous ontology

The new observations should not be used to patch R/W/E/L or M0–M4 immediately.

In particular, Set C does not justify inventing new axes such as:

- `PredictiveRole`;
- `LifecycleRole`;
- `ActionConditioning`;
- `RepresentationTransfer`;
- `OnlineMediator`.

Those concepts are useful audit questions right now. Prematurely turning them into axes would repeat the same failure mode we are trying to escape.

---

## 10. Next scientific pressure test

The next suspicious abstraction is our earlier idea of a "joint world-action generation" family.

That label looks elegant, which is exactly why it is dangerous.

Set D should independently reconstruct:

- OccWorld
- DrivingGPT
- GenAD
- Gen-Drive
- Discrete-WAM

without assuming they are related.

The only pre-registered question is:

> When world/scene future variables and ego-action variables appear in one generative computation, is that shared architectural fact actually the paper's core scientific mechanism, or are we once again grouping papers by one visible similarity while ignoring more important differences?

If the five papers do not naturally support a shared scientific program after full reconstruction, the old "joint generation" idea should be abandoned rather than repaired.
