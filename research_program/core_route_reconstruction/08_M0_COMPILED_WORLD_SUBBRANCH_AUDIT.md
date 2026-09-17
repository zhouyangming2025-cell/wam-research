# M0 Compiled-World Sub-Branch Audit

Status: **SUB-BRANCH RECONSTRUCTION — NOT AN ONTOLOGY SPEC**  
Branch: `research/core-route-reconstruction`  
Date: 2026-09-17  
Target: resolve the largest false-merge risk inside provisional `M0`.

## 0. Starting problem

`M0` currently means:

> world/predictive/simulation computation changes the deployed planner/policy/scorer through learning, but the relevant future/world computation is not required as an online mediator at action time.

This ancestor includes LAW, Drive-JEPA, ViDAR, DriveWorld, ReWorld, WA-JEPA, Metis, SimWAM, DynFlowDrive, Think2Drive, CRAFT, and CausalDrive policy post-training.

If all of these remain one route, `M0` simply recreates the old `W0` collapse.

The real question is:

> **What exactly is compiled from world modeling into the deployed decision system, and through which causal learning bridge?**

---

## 1. Candidate split 1 — predictive representation / policy-feature shaping

### Core program

```text
observations / video
    -> predictive/world objective
    -> representation or shared action-model state
    -> deployed planner/action model
```

The world task primarily teaches **what representation the planner should use**.

The deployed planner consumes a representation/parameter state shaped by predictive learning, not a stored action ranking or imagined return.

### Strong anchors

#### LAW

Primary source: `papers/raw_md/P0048_LAW/P0048_LAW.raw.md`.

LAW explicitly asks how to learn better scene feature representations for E2E driving.

Its action-aware latent world model predicts future scene features from current latents + predicted ego trajectory. The future-latent loss jointly improves current scene representation and trajectory prediction.

Deleting the future-prediction objective collapses LAW toward the underlying ordinary E2E planner.

#### Drive-JEPA

Primary source: `papers/raw_md/P0049_DriveJEPA/P0049_DriveJEPA.raw.md`.

Drive-JEPA makes scalable predictive representation learning the first of two orthogonal bottlenecks. V-JEPA pretraining produces an encoder transferred to both PF and PB planning settings.

Deleting the proposal planner still leaves the predictive-representation thesis directly testable in PF.

#### ViDAR / DriveWorld / ReWorld / WA-JEPA

D01 neutral skeletons independently show:

- future geometry / predictive world objectives during pretraining;
- transfer/adaptation of the learned encoder/representation;
- prediction targets or target encoders removed/bypassed online.

These strongly replicate the same broad learning bridge across different predictive substrates.

### Does joint-training-with-future-bypass form a separate branch?

Previously Metis and SimWAM were tentatively separated as `M0-D`.

This audit weakens that split.

#### Metis

Primary source: `papers/raw_md/P0062_Metis/P0062_Metis.raw.md`.

Metis uses future video generation as a jointly optimized predictive task but imposes asymmetric visibility so the action expert does not depend on future video tokens at inference.

The WAM contribution still reaches the deployed action model mainly through **representational/shared-training effects**.

The special contribution is the coupling realization:

- separate experts;
- shared latent interaction;
- asymmetric mask;
- explicit future bypass.

Those facts distinguish Metis scientifically from LAW/Drive-JEPA, but the high-level causal learning bridge remains predictive/world training -> deployed action representation/model.

#### SimWAM

D01 evidence similarly shows joint video/action flow-matching training with future video isolated/dropped at deployment.

### Deletion/collapse test

- LAW minus predictive loss -> ordinary planner;
- Drive-JEPA minus V-JEPA pretraining -> ordinary planner/proposal system without WAM representation benefit;
- Metis minus future-video learning -> action expert without WAM training benefit;
- ViDAR minus future geometry pretraining -> standard downstream encoder/planner.

All collapse along the same **representation/policy-feature shaping** dimension, although their training organization differs.

### Current verdict

This is a **mature M0 sub-branch candidate**.

Working description only:

> `M0-R`: predictive/world learning compiled into deployed representation / action-model features.

Do not yet split auxiliary co-training vs stage-separated pretraining into separate CoreRoutes. Treat that as a Learning/Coupling Profile unless broader evidence shows route-level consequences.

---

## 2. Candidate split 2 — imagination / simulator consequences compiled into policy preference

### Core program

```text
policy action
    -> learned/simulated world rollout
    -> reward / return / advantage
    -> policy optimization
    -> deployed policy parameters
```

The world model does not primarily teach a generic representation. It provides an **interaction environment in which policy preference is optimized**.

### Strong anchors

#### Think2Drive

Primary source: `papers/raw_md/P0027_Think2Drive/P0027_Think2Drive.raw.md`.

The paper explicitly describes the learned latent world model as a neural simulator. The planner acts in latent imagined rollouts; the world model predicts next latent state, reward, and termination; actor/critic are trained through those imagined trajectories.

Deleting imagined world rollouts does not merely weaken scene representation—it removes the model-based policy-optimization mechanism.

#### CRAFT

D02 mechanism evidence supports a counterfactual-to-interactive reinforcement-fine-tuning program in which counterfactual group advantages and closed-loop residuals create policy-gradient supervision, while the counterfactual/world machinery is absent at deployment.

#### CausalDrive policy post-training

D01 evidence supports:

`policy action -> CausalDrive world rollout -> reward -> reinforcement update -> deployed policy`,

with simulator dropped online.

### Why this is not M0-R

Substitute a predictive representation objective for imagined return optimization:

- actor/critic learning disappears;
- the role of action-conditioned counterfactual consequences changes;
- the learned object is no longer policy preference under return.

Conversely, adding a better visual representation does not reproduce imagined policy optimization.

The distinction survives representation, model architecture, and simulator implementation changes.

### Deletion/collapse test

- Think2Drive minus imagination -> model-free or externally simulated RL, not the same method;
- CausalDrive-policy minus simulator reward -> no simulator-driven policy post-training;
- CRAFT minus counterfactual/interactive advantage construction -> ordinary policy fine-tuning.

### Current verdict

This is a second **mature M0 sub-branch candidate**.

Working description:

> `M0-P`: world/simulator consequences compiled into policy preference through return/advantage optimization.

---

## 3. Candidate split 3 — world-derived decision supervision distilled into a scorer/evaluator

### Core program

```text
candidate action
    -> world model / world-dynamics analysis during training
    -> target score / preferred-mode label
    -> deployed scorer
    -> candidate selection
```

The world process is compiled not into a generic representation and not directly into a policy return, but into a **decision evaluator**.

### Strong anchor: DynFlowDrive

Primary source: `papers/raw_md/P0063_DynFlowDrive/...` and D01 skeleton.

DynFlowDrive's flow-based world model models trajectory-conditioned latent transitions and derives reconstruction/stability criteria for multi-mode supervision. The deployed planner/scorer remains, while the world model is explicitly absent at inference.

Deleting the world-derived stability/reconstruction supervision collapses the method toward ordinary multimodal trajectory scoring.

### Why it differs from M0-R

The primary thing transmitted is **which candidate should be preferred / how it should be scored**, not merely a world-aware representation of the observation.

### Why it differs from M0-P

The deployment artifact retains a scorer approximating a world-derived candidate-evaluation relation. The policy itself is not principally optimized through imagined multi-step return/advantage.

### Replication problem

Current target-domain evidence has a strong DynFlowDrive anchor, but independent exact replicas are sparse.

Possible near-neighbors:

- world/simulator-derived candidate labels in other planning distillation systems;
- teacher->surrogate evaluators;
- some simulator-derived scoring branches.

However, these often lack a qualifying WAM of their own or retain an online future surrogate (e.g. WorldDrive, which remains M2 rather than pure M0).

### Current verdict

Scientifically coherent but **under-replicated**.

Working description:

> `M0-S`: world-derived decision supervision compiled into deployed scorer/evaluator.

Status: **singleton/early sub-branch candidate**, not mature route.

---

## 4. Rejected split — joint world/action training with future bypass as a separate M0 route

Previous hypothesis:

`M0-D = joint world/action training with future branch bypass`.

Current audit result: **DEGRADE TO COUPLING/LEARNING PROFILE**.

Reason:

Metis and SimWAM are distinctive because of how they prevent future-generation computation from becoming an inference dependency. But the world knowledge reaches action mainly by shaping a shared/action representation under predictive joint training.

This fits the higher-order `M0-R` bridge.

What remains valuable is a profile such as:

- separate predictive pretraining then transfer;
- end-to-end auxiliary prediction;
- shared multi-task latent;
- asymmetric expert coupling;
- isolated future branch;
- future-output bypass at deployment.

These are scientifically meaningful implementations of the same high-level compiled-representation bridge until proven otherwise.

---

## 5. LAW vs Drive-JEPA — same branch, real sublineage difference

This pair is useful because it shows how to preserve scientific novelty without over-promoting it.

### Shared bridge

Both use predictive learning to produce a planning-useful representation that remains after explicit prediction machinery is no longer needed for decision making.

### LAW-specific program

`planner-predicted ego trajectory + current latent -> future latent prediction -> joint E2E self-supervised optimization`.

Prediction is action-conditioned and tightly integrated into planner training.

### Drive-JEPA-specific program

`large-scale video -> V-JEPA masked latent prediction pretraining -> transferred encoder -> planner`.

The paper's novelty is scalability, collapse-resistant JEPA pretraining, and separation of representation learning from a second multimodal-planning bottleneck.

### Branch judgment

The distinction is currently best represented as **learning-program sublineage**, not a different world-to-planning CoreRoute.

Deleting the detailed learning organization from either paper still leaves the same causal bridge class:

`predictive world objective -> deployed representation -> planning`.

---

## 6. Metis as a crucial boundary case

Metis initially looked route-distinct from LAW/Drive-JEPA because its paper is framed around WAM coupling and inference efficiency rather than generic representation learning.

The causal audit gives a subtler answer:

- genealogy: Metis belongs near Epona/DriveLaW because it directly debates world/action coupling;
- route bridge: Metis belongs on the compiled-representation side because future video is not an online mediator;
- coupling profile: Metis is special because it achieves this through asymmetric dual-expert training.

Thus one paper can be:

- genealogically adjacent to `M1` siblings;
- mechanistically located under `M0-R`;
- scientifically novel through a coupling-profile fork.

This is precisely why one graph cannot represent all relationships.

---

## 7. Proposed M0 internal structure after adversarial audit

```text
Compiled world knowledge (M0 ancestor)
|
|-- M0-R  predictive/world learning -> deployed representation/action-model features
|     |-- end-to-end action-conditioned auxiliary prediction (LAW)
|     |-- scalable pretraining -> transfer (Drive-JEPA, ViDAR, DriveWorld, ...)
|     |-- joint predictive/action training + future bypass (Metis, SimWAM)
|
|-- M0-P  imagined/simulated consequences -> return/advantage -> deployed policy
|     |-- learned latent imagination (Think2Drive)
|     |-- counterfactual/interative fine-tuning (CRAFT)
|     |-- external/distilled world simulator post-training (CausalDrive-policy)
|
|-- M0-S  world-derived decision supervision -> deployed scorer/evaluator
      |-- DynFlowDrive [strong anchor; independent replication still weak]
```

This is a **working hierarchy**, not accepted ontology.

---

## 8. Why these splits are more fundamental than “training-only world model”

All three branches can delete the world computation before deployment, but what survives is different:

### M0-R survivor

A world-aware **representation / action-model feature geometry**.

### M0-P survivor

A world/simulator-optimized **policy preference encoded in policy parameters**.

### M0-S survivor

A world-derived **candidate evaluator / score approximation**.

This is exactly the user's earlier `a + b/c + unique` intuition at work:

- common ancestor: world-model knowledge is compiled rather than explicitly queried online;
- main fork: what decision object receives that compiled knowledge;
- local innovation: JEPA vs latent prediction vs dual-expert masking vs flow dynamics vs Dreamer-style imagination.

---

## 9. Counterarguments and unresolved pressure

### 9.1 Could M0-R and M0-S be merged as “distillation/transfer”?

Too coarse at present.

Representation shaping changes the state/features from which arbitrary planning computations operate. Scorer distillation approximates a much narrower action-evaluation relation. Swapping one for the other changes the deployed causal object.

### 9.2 Could M0-S be only a profile because it has one anchor?

Yes. Current status remains early/singleton. It should not be promoted to mature route without independent target-domain replication.

### 9.3 Could M0-P be considered ordinary model-based RL rather than WAM one-stage route?

This is a domain-scope question rather than a mechanism question. Think2Drive is in the target census because a learned world model causally trains the deployed driving policy. If final scope later excludes training-only world-model policy learning, M0-P may move outside the target map. Do not resolve scope by changing mechanism semantics.

### 9.4 Does Metis really belong with representation shaping?

Current answer: medium/high confidence. Its asymmetric training is designed so future prediction influences action learning without becoming a future-token dependency. Exact gradient/parameter-sharing paths remain worth code-level verification if this becomes normative.

---

## 10. Current verdict

High confidence:

- `M0` cannot remain one final route.
- predictive representation shaping/transfer (`M0-R`) is a mature repeated lineage.
- imagination/simulator-driven policy optimization (`M0-P`) is a distinct mature learning bridge.
- Metis/SimWAM-style future bypass is better treated as a realization within `M0-R` than as a separate top-level route.

Medium confidence:

- world-derived scorer supervision (`M0-S`) is genuinely distinct in mechanism.

Low/medium confidence:

- `M0-S` has enough independent replication to deserve a stable branch.
- exact leaf split inside `M0-R`.

Next priority:

> perform the same sub-branch reconstruction inside `M2`, where the false-merge pressure is now the largest remaining threat to a minimal route hierarchy.
