# M2 Action-Conditioned Consequence Sub-Branch Audit

Status: **SUB-BRANCH RECONSTRUCTION — NOT AN ONTOLOGY SPEC**  
Branch: `research/core-route-reconstruction`  
Date: 2026-09-17  
Target: resolve false-merge pressure inside provisional `M2`.

## 0. Starting question

`M2` currently contains methods with the causal ancestor:

`O -> A~ -> Z(A~) -> A*`

where a provisional/candidate ego behavior indexes a distinct predicted future/consequence which then changes final planning.

Current members include:

- World4Drive;
- WoTE;
- WorldDrive;
- DA-WAM;
- Drive-WM;
- SafeDrive;
- RaWMPC;
- DriveFuture.

This shared ancestor is strongly supported. But it is still too broad to assume all are one final route.

The main audit question is:

> **Does the predicted consequence only evaluate/choose among already formed alternatives, or does it participate inside the action-generation/optimization process to create the final action?**

---

## 1. Mature branch candidate — consequence-based alternative evaluation

### Core program

```text
observation
    -> candidate / intention / action alternatives A~_k
    -> candidate-specific consequences Z_k
    -> evaluator / cost / reward / plausibility
    -> choose A*
```

The world model is used as an **evaluator of alternatives**.

The candidate may be an explicit trajectory, intention, action sequence, or proposal. The consequence may be video, BEV, sparse world, occupancy-like state, or latent. Those differences are not sufficient by themselves to split the causal route.

### Strong independent anchors

#### WoTE

Primary source: `papers/raw_md/P0045_WoTE/P0045_WoTE.raw.md`.

The paper's central thesis is exactly online trajectory evaluation with a world model:

- propose multiple trajectories;
- form a state-action pair for each;
- recurrently predict each trajectory's future BEV states;
- predict reward from those future states;
- choose the highest-reward trajectory.

This is the clearest explicit rollout form.

#### DA-WAM

Primary source: `papers/raw_md/P0012_DAWAM/P0012_DAWAM.raw.md`.

DA-WAM makes the one-to-one action-consequence relation itself the scientific contribution:

- each candidate obtains a distinct future latent;
- the scorer consumes current state + candidate + its own future latent;
- the candidate with highest utility is selected.

The paper explicitly argues that shared/pooled futures weaken decision alignment.

#### World4Drive

Primary source: `papers/raw_md/P0046_World4Drive/P0046_World4Drive.raw.md`.

World4Drive:

- forms multimodal driving intentions / trajectories;
- predicts intention-specific future latent worlds;
- uses a world-model selector to evaluate/rank trajectories.

The distinctive idea is intention-aware future plausibility / mode agreement, but the causal bridge remains alternative -> consequence -> commitment.

#### WorldDrive

WorldDrive retains a lightweight candidate-specific future surrogate at inference:

- planner proposes top-K trajectories;
- FAR predicts/distills planning-relevant future latent per candidate;
- future-aware reward ranks candidates.

WorldDrive also has an independent representation-inheritance bridge (`M0-R`), making it a synthesis paper.

#### Drive-WM

D01 skeleton:

`ego-candidate-conditioned future views -> planning cost per candidate -> minimum-cost trajectory`.

This is a high-fidelity visual consequence realization of the same evaluation bridge.

#### SafeDrive

D01 skeleton:

`ego proposals -> proposal-conditioned sparse worlds -> collision/drivable-area reasoning -> selected/refined trajectory`.

The world representation is sparse and explicitly safety-oriented, but alternatives still receive proposal-specific consequences before commitment.

#### RaWMPC

D01 skeleton:

`candidate action sequences -> horizon rollouts -> semantic/risk/ego-state predictions -> cost -> minimum-cost sequence`.

This is closest to classical model-predictive candidate evaluation.

### Negative controls

- DrivoR: candidate -> scorer, no predicted consequence;
- TOAD: CEM candidate search -> learned reward, no world consequence;
- Hydra-MDP: teacher-trained candidate scoring, no online world consequence;
- Drive-JEPA PB: proposal/scorer, but predictive pretraining does not instantiate candidate-specific future worlds.

These controls strongly isolate the bridge.

### Current verdict

This is a **mature M2 sub-branch candidate**.

Working description:

> `M2-EVAL`: candidate/intention-specific world consequence used to evaluate and commit among alternatives.

---

## 2. Emerging branch candidate — consequence-guided action refinement / solving

### Core program

```text
provisional action A^(i)
    -> predicted consequence Z(A^(i))
    -> guidance / update
    -> revised action A^(i+1)
    -> ...
    -> committed action A*
```

Here consequence reasoning is not merely an external judge after proposals exist. It enters the **solver that constructs/refines the action**.

### Strong anchor: DriveFuture

D01 mechanism evidence:

`current latent + provisional ego trajectory -> predicted future latent -> progressive foresight guidance within diffusion planning -> final trajectory`.

The future latent is retained online and interacts with planning denoising/guidance.

This differs from WoTE-style ranking if the future signal changes the trajectory-generation trajectory itself rather than only scoring finished alternatives.

### Possible near-neighbors

- SafeDrive may refine as well as select, but the current evidence is not sufficiently precise to treat it as an independent refinement anchor.
- MPC/search methods may repeatedly generate/evaluate proposals, but repeated optimizer search is not enough unless a world consequence enters each action-update step.
- SeerDrive alternates world and planning updates, but its explicit reciprocal world<->planning loop is currently kept at the higher-order `M4` motif.

### Boundary with M4

`M2-REFINE`:

- consequence prediction is subordinate to the action solver;
- the world state need not be a persistent independently refined object;
- the key loop is action proposal -> consequence guidance -> action update.

`M4`:

- world state itself is revised using updated plan/action information;
- revised world again updates planning;
- both sides participate as alternating stateful processes.

Thus not every iterative consequence-guided planner is reciprocal world-action refinement.

### Current verdict

Scientifically plausible but **under-replicated**.

Working description:

> `M2-REFINE`: action-conditioned consequence used inside action optimization/refinement rather than only post-hoc selection.

Status: **early/singleton sub-branch candidate** pending independent target-domain replication.

---

## 3. Rejected top-level split — endpoint future vs horizon rollout

Tempting distinction:

- World4Drive / DA-WAM: compact endpoint/future latent;
- WoTE / RaWMPC: multi-step horizon rollout.

Current judgment: **PROFILE, not route boundary**.

Reason:

Replacing a one-step/endpoint consequence with a horizon rollout changes fidelity, temporal depth, and computational cost, but the bridge can remain:

`candidate -> consequence -> evaluator -> select`.

Deletion test:

- WoTE with a shorter learned consequence predictor would still instantiate model-based consequence evaluation;
- DA-WAM with a longer rollout would remain candidate-specific consequence scoring.

This may become a scientifically important subprofile such as `ConsequenceDepth`, but current evidence does not justify a separate CoreRoute.

---

## 4. Rejected top-level split — explicit world rollout vs latent/surrogate future

Tempting distinction:

- Drive-WM: generated visual future;
- WoTE: explicit BEV future;
- WorldDrive: distilled future surrogate;
- DA-WAM: direct latent future;
- SafeDrive: sparse world.

Current judgment: **Consequence Realization Profile**.

The representation/substrate and compression level change efficiency and interpretability, but not necessarily the causal bridge.

Important scientific sublineage:

`full world rollout -> compact future latent -> distilled future surrogate`.

This is worth preserving in the genealogy, especially WoTE -> WorldDrive-like efficiency progression, but should not automatically define different top-level planning routes.

---

## 5. Rejected top-level split — plausibility vs utility/reward vs safety

Examples:

- World4Drive: future plausibility / mode agreement;
- WoTE: imitation + simulator driving rewards;
- WorldDrive: planning preference/future-aware reward;
- DA-WAM: factorized outcomes + overall utility;
- SafeDrive: collision/drivable-area safety reasoning;
- RaWMPC: risk/progress cost.

Current judgment: **Resolver / Consequence-Evaluation Profile**.

This is the same correction previously discovered for E.

If the candidate-consequence bridge remains fixed, changing the criterion semantics does not by itself create a different route.

Exception:

If criterion structure changes the solver topology—for example, hard feasibility constraints that prune/repair actions rather than score them—then the mechanism should be re-audited at the bridge level rather than promoted merely because its semantic label differs.

---

## 6. World4Drive vs WoTE vs WorldDrive vs DA-WAM — commonality and real difference

This set is the key protection against both over-merge and over-split.

### Common ancestor

All make the action/intention-specific future **decision-relevant online**.

### World4Drive unique residue

- multimodal intention representation;
- intention-specific future latent;
- factual-future alignment trains the selector;
- future plausibility/mode agreement is central.

Deleting the multimodal intention-conditioned future mechanism pushes it toward LAW-like unimodal latent self-supervision / ordinary multimodal planner.

### WoTE unique residue

- explicit recurrent future BEV rollout for each trajectory;
- reward prediction from imagined future states;
- online model-based trajectory evaluation is the declared paper problem.

Deleting future rollout collapses it toward ordinary current-state trajectory evaluation.

### WorldDrive unique residue

- generative world model learns unified visual/motion representation;
- planner inherits those representations;
- heavy candidate-wise generation is distilled into FAR;
- online candidate-specific future surrogate remains.

Deleting FAR leaves the representation-inheritance bridge (`M0-R`) but removes its M2 contribution. This is unusually strong evidence that WorldDrive is a synthesis paper rather than a single-route exemplar.

### DA-WAM unique residue

- predictive representation remains adaptive during planner optimization;
- every candidate receives an explicit one-to-one future latent;
- scorer is explicitly future-latent-conditioned;
- paper is framed around prediction-action alignment.

Deleting one-to-one candidate-future alignment collapses it toward weak/shared-future latent planning.

### Audit conclusion

The four papers **should share an M2-EVAL ancestor**, but their paper identities are preserved by lower-level sublineages and secondary motifs.

This is exactly the desired behavior of a hierarchical route map.

---

## 7. Decision-alignment strength is a profile, not automatically a route

DA-WAM introduces a useful concept: how strongly future prediction is aligned with each candidate and with planner optimization.

Possible spectrum:

- one shared future state for all planning;
- intention-conditioned multiple futures;
- distinct future per candidate;
- distinct future per candidate + scorer explicitly conditioned on it;
- future representation co-adapts with planning objective.

This is scientifically meaningful.

But it cuts across representation and training design and does not automatically change the major causal motif once the action-indexed consequence branch already exists.

Working status: `DecisionAlignmentProfile` until broader evidence shows a stable route split.

---

## 8. Counterfactual fidelity / reactivity is also orthogonal

An action-conditioned world model can be structurally M2 while still using weak counterfactual supervision:

- logged future may only correspond to expert action;
- other-agent futures may be reused across counterfactual ego branches;
- simulator supervision may or may not model reaction to ego intervention.

Therefore:

> `candidate-conditioned consequence` does not imply causal correctness of that consequence.

Reactivity/counterfactual validity should remain an audit/profile dimension, not be inferred from route membership.

This prevents the route taxonomy from accidentally making epistemic-quality claims.

---

## 9. Proposed M2 internal hierarchy

```text
Action-conditioned consequence mediation (M2 ancestor)
|
|-- M2-EVAL  consequence used to compare/commit among alternatives  [MATURE]
|     |-- explicit rollout / cost-reward evaluation      (WoTE, Drive-WM, RaWMPC)
|     |-- compact candidate-future latent + scorer       (DA-WAM)
|     |-- intention/future plausibility selection        (World4Drive)
|     |-- distilled future-surrogate evaluation          (WorldDrive)
|     |-- sparse safety-world evaluation                 (SafeDrive)
|     [lower rows are current sublineages/profiles, NOT accepted routes]
|
|-- M2-REFINE consequence used inside action solver/refinement       [EARLY]
      |-- progressive foresight-guided diffusion planning (DriveFuture)
```

The strongest supported route-level split inside M2 is currently:

**evaluate alternatives** vs **use consequence inside the action solver**.

Even this split is asymmetric in evidence: M2-EVAL is mature; M2-REFINE is under-replicated.

---

## 10. Current verdict

High confidence:

- `M2-EVAL` is a mature repeated scientific route candidate.
- World4Drive, WoTE, WorldDrive, DA-WAM, Drive-WM, SafeDrive, and RaWMPC share this major ancestor despite large implementation differences.
- consequence representation (video/BEV/latent/sparse/surrogate) should not currently define top-level routes.
- resolver objective semantics should remain profile-level.
- consequence horizon depth should remain profile-level.

Medium confidence:

- consequence-guided action refinement is a real separate sub-branch mechanism.

Low/medium confidence:

- `M2-REFINE` has enough independent target-domain replication to become a stable route family.

Next priority:

> audit `M1` internal structure and test whether Epona / DriveLaW / GraphWorld / occupancy-future planners really share one world-first route, or whether generator-state mediation and structured-prediction mediation are genuinely separate scientific branches.
