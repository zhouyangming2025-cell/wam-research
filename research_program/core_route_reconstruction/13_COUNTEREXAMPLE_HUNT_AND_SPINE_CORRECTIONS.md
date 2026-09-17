# Counterexample Hunt and Causal-Spine Corrections

Status: **ADVERSARIAL COUNTEREXAMPLE AUDIT — NOT AN ONTOLOGY SPEC**  
Branch: `research/core-route-reconstruction`  
Date: 2026-09-17  
Targets: Auto-JEPA, WorldRFT, Drive-OccWorld, plus correction pressure from OccWorld.

## 0. Purpose

The revised spine in `12_REVISED_MINIMAL_CAUSAL_SPINE_SYNTHESIS.md` looked suspiciously clean. This audit deliberately selects papers likely to fall between categories.

A valid counterexample should show a qualifying WAM planning program whose implemented world-action dependency cannot be faithfully represented as:

- compiled world knowledge (`M0`);
- world-first mediation (`M1`);
- action-conditioned consequence (`M2`);
- joint world-action generation (`M3`);
- reciprocal world-action refinement (`M4`);
- or a composition of the above.

Important: a paper can instead expose a **domain-gate failure**. That does not require a new route.

---

## 1. Auto-JEPA — route counterexample or world-state gate challenge?

Primary source: `papers/raw_md/P0051_AutoJEPA/P0051_AutoJEPA.raw.md`.

### 1.1 Mechanism

Auto-JEPA predicts a continuous latent representation of the **future ego trajectory** from current visual context, ego-motion history, and route command.

At inference:

- predict future ego-motion intent latent;
- use that latent as retrieval key into a fixed trajectory memory;
- rank retrieved trajectories with a scene-conditioned scorer;
- apply a drivable-area gate;
- select final trajectory.

The paper explicitly contrasts itself with dense future-world prediction and argues that planning need only predict scene information through its implication for future ego action.

### 1.2 Why it is dangerous for the ontology

If every future action/trajectory latent is admitted as a “world state”, then nearly any sophisticated action predictor can be promoted into WAM.

Auto-JEPA's predicted object is not clearly:

- future environment state;
- transition state;
- consequence of a candidate ego action;
- joint world/action future.

It is primarily a **future ego-motion/action representation**.

### 1.3 Does it require a new route?

No.

The problem occurs **before** route projection.

Auto-JEPA pressures the world-carrier/domain gate:

> Can an action-oriented latent that contains only the future ego trajectory count as world modeling merely because current scene dynamics are compressed into the predicted action intent?

Current answer: **do not assume yes**.

### 1.4 Current status

`WORLD-GATE-PRESSURE / ACTION-LATENT PREDICTIVE PLANNER`.

If future ego-action latent alone is judged insufficient to qualify as a world state, Auto-JEPA moves to an adjacent predictive-planning family rather than creating a new WAM route.

If later evidence establishes that its latent contains a separately identifiable predictive environment/dynamics state beyond ego action semantics, re-open projection.

### Lesson

> Route completeness and domain membership are orthogonal. A paper outside the world-state gate is not a missing route.

---

## 2. WorldRFT — apparent “latent world state” does not automatically create M1

Primary source: `papers/raw_md/P0050_WorldRFT/P0050_WorldRFT.raw.md`.

### 2.1 Mechanism layers

WorldRFT combines:

- spatial-aware current latent representation using visual/geometric priors;
- hierarchical planning decomposition;
- local-aware iterative trajectory refinement;
- future latent prediction as a self-supervised world-modeling training objective;
- GRPO-based safety reinforcement fine-tuning.

The future world decoder predicts `W_latent^(t+1)` from current latent representation and trajectory during training.

The online planner principally consumes the current spatial-aware latent representation and performs hierarchical/local refinement.

### 2.2 Why it could be misclassified

The paper calls its feature `W_latent`, and the planner reads that feature online.

A superficial state-name rule would assign M1.

But the strict M1 gate asks whether a separately traceable **runtime world/dynamics operation** produces the mediator, beyond ordinary/current representation encoding.

Current evidence supports future prediction primarily as a training loss. The online planning state is a current representation constructed from image features + geometry priors.

### 2.3 Current projection

Primary WAM bridge:

`M0-R predictive/world representation shaping`.

The hierarchical planner and GRPO fine-tuning are additional planning/training innovations. GRPO should not be labeled M0-P unless the reward/return itself is generated through the qualifying world model; ordinary collision-aware planning reward is insufficient.

### 2.4 Does it require a new route?

No.

It reinforces the rule:

> A tensor named “world latent” is not automatically an online world mediator.

WorldRFT therefore does not break the factorisation spine.

---

## 3. Drive-OccWorld — major correction: independent M4 replication

Primary source: `papers/raw_md/P0044_DriveOccWorld/P0044_DriveOccWorld.raw.md`.

### 3.1 Previous shallow interpretation

D01 neutral skeleton compressed the method to roughly:

`occupancy forecast -> planning`.

That suggested M1.

### 3.2 Full-paper implemented program

Drive-OccWorld explicitly defines continuous forecasting and planning.

At a future step:

1. world model forecasts future occupancy/flow state using historical observations and action conditions;
2. occupancy-based planner evaluates/selects the next trajectory using that predicted state;
3. the selected/predicted trajectory becomes the action condition fed back into the world model;
4. the world model forecasts the subsequent state;
5. planning repeats.

The paper states that the predicted trajectory at `t+1` serves as action condition for forecasting `s_(t+2)`, “leading to a continuous rollout of forecasting and planning.”

Computationally:

```text
state/world^(1)
    -> plan/action^(1)
    -> state/world^(2)
    -> plan/action^(2)
    -> ...
```

### 3.3 Relationship to SeerDrive

SeerDrive:

- future BEV and ego planning mutually refine each other in an iterative loop within the planning framework.

Drive-OccWorld:

- occupancy world rollout and trajectory planning alternate autoregressively across future steps.

The internal state representation and update schedule differ, but both instantiate the deeper dependency:

`world -> action -> revised/further world -> action ...`.

### 3.4 M4 status correction

Previous status:

`M4 = scientifically meaningful singleton extension`.

New status:

**M4 has at least two independent strong anchors: SeerDrive and Drive-OccWorld.**

Therefore it should be upgraded from singleton to **major branch candidate**, while preserving sublineage differences.

Potential M4 sublineages:

- iterative mutual refinement of a fixed future representation/planning state — SeerDrive;
- autoregressive continuous world-rollout / planning alternation — Drive-OccWorld.

Do not yet split these into separate CoreRoutes.

### 3.5 Why Drive-OccWorld is not just M2

M2 can evaluate candidate consequences once and commit.

Drive-OccWorld feeds the resulting action back into the world process to create the next world state and continues alternating.

Thus the repeated world/action state update is not incidental; it is the declared continuous planning mechanism.

M4 is the more faithful higher-order motif.

---

## 4. OccWorld vs Drive-OccWorld — a useful lineage fork

OccWorld full-paper reading supports:

`joint future scene + ego generation` -> M3-like.

Drive-OccWorld instead explicitly integrates:

`world forecast -> planner -> action condition -> next world forecast` -> M4-like.

These papers share occupancy-world intellectual ancestry but implement different world-action factorisations.

This is a powerful example of why:

- representation substrate (occupancy) must not define route;
- genealogy proximity must not force route equality;
- route is better captured by world/action dependency structure.

---

## 5. Does the counterexample hunt break the five-way spine?

Current result: **NO**.

Instead it produces two corrections:

1. Auto-JEPA is primarily a **world/domain-gate pressure case**, not evidence for a sixth route;
2. Drive-OccWorld independently replicates `M4`, upgrading reciprocal/alternating world-action planning from singleton to serious branch candidate.

WorldRFT fits `M0-R` once current representation is distinguished from an online predictive world mediator.

---

## 6. Revised branch maturity after counterexample hunt

| Motif | Current maturity | Key anchors | Main unresolved issue |
|---|---|---|---|
| `M0` compiled | HIGH as ancestor | LAW, Drive-JEPA, Think2Drive, Metis, DynFlowDrive, etc. | leaf structure / M0-S replication |
| `M1` world-first | HIGH as ancestor | DriveLaW, GraphWorld, Policy World Model, Epona-probable | explicit forecast vs internal state leaf split |
| `M2` action-consequence | VERY HIGH as ancestor | WoTE, DA-WAM, World4Drive, WorldDrive, Drive-WM, SafeDrive, RaWMPC | evaluator vs solver-refinement subbranch |
| `M3` joint generation | HIGH | DrivingGPT, GenAD, Gen-Drive, Discrete-WAM-joint, OccWorld | strict world/action co-generation gate |
| `M4` reciprocal/alternating | MEDIUM-HIGH, upgraded | SeerDrive, Drive-OccWorld | unify/refine two alternating styles; more independent anchors desirable |

---

## 7. New pre-route gate forced by Auto-JEPA

Before M0-M4 projection, ask:

### World-object gate

Does the method contain a separately traceable object/process with semantics of:

- environment/world state;
- transition/dynamics state;
- predicted world consequence;
- joint ego-environment future;
- generative world/model process state;

rather than only:

- ego action;
- future ego trajectory/intention;
- generic visual feature;
- semantic decision token;
- scalar reward/score?

Future action information can condition a world model, but action semantics alone should not automatically qualify as the world object.

This gate restores the earlier useful insight of the formal C-carrier audit without restoring the old R-W-E-L route ontology.

### Important caveat

A predictive state need not resemble pixels or BEV. A latent can qualify if its learned/operational role is genuinely world/dynamics predictive rather than merely action encoding.

---

## 8. Corrections to prior files

The following statements are now superseded:

### `07_MINIMAL_CAUSAL_SPINE_PROJECTION.md`

- OccWorld=M1 -> **SUPERSEDED; full paper supports M3-like joint scene/ego generation**.
- Drive-OccWorld=M1 -> **SUPERSEDED; full paper supports M4 alternating forecasting/planning**.

### `12_REVISED_MINIMAL_CAUSAL_SPINE_SYNTHESIS.md`

- M4 described as singleton -> **SUPERSEDED; Drive-OccWorld provides independent replication**.

Historical files remain untouched to preserve reasoning evolution.

---

## 9. Current verdict

High confidence:

- the five-way causal factorisation spine survives this counterexample hunt;
- strict world-object/domain gate is necessary before route projection;
- Auto-JEPA currently pressures domain membership rather than route completeness;
- WorldRFT is better explained as compiled predictive representation + planner innovations than as a new world-action factorisation;
- Drive-OccWorld is strong independent M4 evidence;
- OccWorld and Drive-OccWorld demonstrate that the same occupancy substrate can instantiate different routes.

Medium/high confidence:

- M4 should now be retained as a real major branch candidate, not merely a SeerDrive-specific extension.

Next step:

> construct a corrected factorisation decision tree + route evidence table using full-paper adjudications where available, then test a small held-out set chosen specifically to distinguish M0/M1/M2/M3/M4 and world-gate failures. Do not expand broadly; choose adversarial papers.
