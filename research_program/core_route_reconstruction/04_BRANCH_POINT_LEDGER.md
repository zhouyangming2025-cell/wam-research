# Branch-Point Ledger for WAM + One-Stage Research Genealogy

Status: **PRE-ONTOLOGY ADJUDICATION LEDGER**  
Branch: `research/core-route-reconstruction`  
Date: 2026-09-17

## Decision vocabulary

Each candidate distinction receives one current status:

- `PROMOTE-CANDIDATE` — recurrent scientific fork with enough independent evidence to be tested as a possible CoreRoute boundary;
- `PROFILE` — recurrent and important, but cross-cutting; does not by itself define the world-to-planning route;
- `PARADIGM` — representation/task formulation that cuts across routes;
- `SINGLETON` — scientifically meaningful but not independently replicated enough for route promotion;
- `REJECT` — distinction fails mechanism-level tests or tracks replaceable implementation detail.

No entry below is a final ontology class.

---

## BP-01 — Does planning consume world-model computation directly, or only knowledge compiled during learning?

### Common ancestor thesis

World-model capability should improve the deployed planner.

### Side A — direct online world participation

Representative evidence:

- WoTE — candidate-specific recurrent future BEV rollout -> reward -> selection;
- Drive-WM — ego candidate -> generated future views -> planning cost -> selection;
- DA-WAM — candidate -> predicted future latent -> scorer;
- SafeDrive — proposal -> sparse future world -> safety reasoning;
- RaWMPC — candidate action sequence -> world rollout -> risk/progress cost;
- Policy World Model — online future tokens -> trajectory decoder;
- OccWorld / Drive-OccWorld — predicted future occupancy retained in planning path.

### Side B — world capability compiled into another deployed component

Representative evidence:

- LAW — future-latent prediction shapes planner/representation during training;
- Drive-JEPA — predictive pretraining transfers encoder;
- DynFlowDrive — world dynamics supervise scorer; world model removed online;
- Think2Drive — imagined transitions/returns train actor/critic;
- CRAFT — counterfactual advantages train policy;
- CausalDrive policy post-training — simulator rollout/reward trains policy;
- SimWAM — future-video branch trains action expert but is bypassed online;
- Metis — future-video generation can be bypassed for deployed action inference.

### Deletion / collapse behavior

Removing online world computation from Side A generally destroys or fundamentally changes the deployed mechanism.

Removing the training-world branch from Side B destroys how knowledge is acquired but may leave the deployment topology unchanged.

### Negative control

DrivoR / TOAD / Hydra-MDP: candidate selection exists without a qualifying world-consequence object.

### Current judgment

`PROFILE`

### Reason

The distinction is fundamental for lifecycle and causal interpretation, but Side B itself contains many different causal programs. “Online vs compiled” is too coarse to define route identity.

---

## BP-02 — How are world generation / prediction and action generation coupled?

### Common ancestor thesis

A world model and an action generator coexist within one WAM-oriented planning system.

### Observed scientifically distinct answers

#### Parallel/shared-state coupling

- Epona — shared temporal latent, specialized video and trajectory diffusion heads.

#### Chained world-representation -> planner

- DriveLaW — internal video-generator latent directly conditions Action DiT.
- DriveDreamer action path — predicted structural evolution / world features feed action decoder.

#### Explicit future-state -> planner

- Policy World Model — autoregressive future tokens remain online and feed trajectory decoder.

#### Deliberately asymmetric / decoupled coupling

- Metis — future video can attend to future action while action cannot depend on future video tokens; video generation bypassed online.
- SimWAM — isolated attention / action-only deployment after joint world-action training.

#### Joint generative coupling

- DrivingGPT — world/action objectives share autoregressive generative backbone.
- GenAD — ego and other-agent trajectories jointly emitted.
- Gen-Drive — joint ego/agent future-scene generator.
- Discrete-WAM joint mode — world/action tokens jointly modeled in one discrete process.

#### Solver-internal foresight coupling

- DriveFuture — provisional action conditions future latent, which guides diffusion planning during solving.

### Within-paper deletion evidence

- DriveLaW without generator-latent -> planner conditioning loses its claimed chained unification.
- Metis without asymmetric isolation loses the claimed solution to interference/latency.
- Epona without shared temporal world structure reduces toward independent generation/planning heads.

### Between-paper collapse examples

- DriveLaW minus chained latent bridge moves toward parallel/shared-latent designs.
- Metis minus action-side isolation moves toward tightly coupled joint world/action training.
- DriveFuture minus foresight guidance moves toward ordinary diffusion trajectory generation.

### Negative control

LAW / Drive-JEPA predictive-pretraining paths: world learning can improve planning without any such online coupling topology.

### Cross-implementation stability

The distinction appears across autoregressive tokens, diffusion, flow matching, latent representations, video generation, structured futures, and joint trajectory generation.

### Current judgment

`PROMOTE-CANDIDATE`

### Reason

This fork is recurrent, author-motivated, deletion-sensitive, and implementation-invariant. It is currently one of the strongest candidates for a genuine CoreRoute boundary or major internal branch.

---

## BP-03 — Does action choice depend on explicit/provisional action consequences?

### Common ancestor thesis

The planner should reason about what follows from alternative or provisional ego behaviors, rather than mapping only current observation to action.

### Positive evidence

- World4Drive — intention-specific predicted future latent / plausibility-based mode selection;
- WoTE — candidate-specific recurrent world rollout -> reward;
- WorldDrive — candidate-specific distilled future surrogate -> reward;
- Drive-WM — candidate-conditioned generated future views -> cost;
- DA-WAM — candidate-specific future latent -> score;
- SafeDrive — proposal-conditioned sparse world -> safety reasoning;
- RaWMPC — candidate action sequence -> horizon rollout -> cost;
- Gen-Drive multi-sample — sampled joint futures -> learned scene reward;
- DriveFuture — provisional action -> future latent -> diffusion-plan guidance.

### Negative controls

- DrivoR — proposals -> direct scorer; no separately predicted future consequence object.
- TOAD — CEM proposals -> trajectory reward; no qualifying world future.
- Hydra-MDP — multimodal heads / teacher-derived scores; no online world consequence carrier.
- Drive-JEPA PB — proposal scoring can exist without online future prediction.

### Internal forks observed

1. full explicit rollout/generation;
2. compact future surrogate;
3. sparse structured future;
4. factual-future plausibility matching;
5. learned downstream utility/reward;
6. joint future-scene generation and ranking;
7. future prediction embedded inside solver/refinement.

### Deletion / collapse behavior

Removing consequence construction from WoTE / Drive-WM / DA-WAM / SafeDrive / RaWMPC turns them toward ordinary candidate scoring or direct planning.

### Current judgment

`PROMOTE-CANDIDATE`

### Reason

The shared ancestor is strongly replicated and has clean negative controls. However, this is almost certainly a **large lineage with sub-branches**, not one final route class.

---

## BP-04 — Is the consequence evaluated by explicit rollout, surrogate future state, or only compiled score?

### Common ancestor thesis

Alternative actions are evaluated using world-model-derived information.

### Observed positions

- WoTE / Drive-WM / RaWMPC — explicit online rollout/generation;
- WorldDrive / DA-WAM — candidate-specific future surrogate retained online;
- DynFlowDrive — world-derived target/scoring supervision, world model removed at inference;
- Gen-Drive single-sample — preference compiled into generator parameters;
- Think2Drive / CRAFT / CausalDrive policy — world/simulator reasoning compiled into policy learning.

### Current judgment

`PROFILE`

### Reason

This is a robust spectrum of deployment residue, but changing position on the spectrum does not uniquely determine the scientific bridge. Different routes can occupy the same residue level.

---

## BP-05 — Predictive representation learning vs online world reasoning

### Common ancestor thesis

Future/world prediction can improve planning.

### Predictive-representation branch

- LAW — action-conditioned future latent as end-to-end self-supervision;
- Drive-JEPA — scalable V-JEPA pretraining -> transferred encoder;
- ViDAR — future geometry prediction pretraining -> downstream planner;
- DriveWorld — predictive world representation pretraining -> planning adaptation;
- ReWorld — predictive representation -> action generation;
- WA-JEPA — future/action predictive targets -> shared deployed representation.

### Online-reasoning branch

- WoTE / Drive-WM / DA-WAM / SafeDrive / RaWMPC etc. retain a future/consequence mechanism in the action decision process.

### Deletion evidence

Removing predictive pretraining from Drive-JEPA / ViDAR primarily degrades the learned representation, not the planner's runtime decision topology.

Removing online consequence computation from WoTE / Drive-WM removes the decision-time foresight mechanism itself.

### Current judgment

Predictive representation: `PROFILE` for now.

### Reason

The lineage is real and strong, but the stable shared mechanism is currently a learning-transfer program. It has not yet earned standalone CoreRoute status.

---

## BP-06 — One-way future-aware planning vs reciprocal world↔planning refinement

### Common ancestor thesis

Future scene information should influence action generation.

### One-way evidence

- World4Drive / WoTE / WorldDrive;
- Policy World Model;
- OccWorld / Drive-OccWorld;
- UniAD / BeTop / VAD;
- GraphAD blind case, on current evidence.

### Reciprocal evidence

- SeerDrive paper — world prediction revises planning; updated ego/planning state feeds back into world modeling; repeated refinement.

### Near-neighbors that do not yet qualify

- DriveFuture — future latent guides action solver, but full alternating world/action update not established;
- GraphAD — iterative graph/prediction refinement, but ego plan -> changed world -> revised ego plan loop not established;
- joint generators — simultaneous world/action generation is not reciprocal refinement.

### Between-paper collapse

SeerDrive minus feedback loop collapses toward one-shot future-aware planning.

### Current judgment

`SINGLETON`

### Reason

Strong scientific distinction, insufficient independent replication.

---

## BP-07 — Direct future-aware structured state -> planning vs candidate-specific consequence evaluation

### Common ancestor thesis

Planning should use future-relevant environment structure.

### Direct-state branch

- GraphWorld — compact interaction-aware world state conditions planning;
- OccWorld — future occupancy horizon informs planning;
- Drive-OccWorld — 4D occupancy forecast -> planning;
- UniAD — predicted agent motion / occupancy through unified queries -> planner;
- BeTop — future behavioral topology -> direct trajectory generator;
- VAD — vectorized predicted motion -> direct planning;
- GraphAD — future-prediction-informed interaction graph -> direct ego planning.

### Candidate-consequence branch

- WoTE / Drive-WM / DA-WAM / SafeDrive / RaWMPC: each alternative/provisional ego action indexes a distinct consequence used in commitment.

### Negative control

Plain current-state perception features without stateful future/dynamic operation should not qualify for the direct-state branch.

### Current judgment

`PROMOTE-CANDIDATE`

### Reason

This distinction appears stable across BEV, occupancy, graph, vectorized, latent and image-based implementations: either future/world structure conditions one planning computation, or the planner explicitly branches consequences by ego alternative.

Still unresolved whether the direct-state side is one CoreRoute or a higher-order parent of several routes.

---

## BP-08 — Joint world/action representation or token space

### Common ancestor thesis

World and action should be aligned strongly enough to support mutual modeling.

### Evidence

- Discrete-WAM — shared discrete visual/decision/action token space and unified task interface;
- DrivingGPT — common autoregressive world/action backbone;
- GenAD — common latent future generative process for ego/agents;
- Gen-Drive — joint ego/agent future scenes;
- Epona / DriveLaW — shared latent world representation, though not identical token semantics.

### Negative control

Two modules trained together do not automatically constitute a unified representation paradigm.

### Current judgment

`PARADIGM`

### Reason

Shared representational language strongly affects what mechanisms are convenient, but it does not uniquely determine final action formation or world-to-planning bridge.

---

## BP-09 — Semantic high-level decision before low-level action

### Evidence

- Discrete-WAM policy — high-level decision token -> low-level action editing;
- DRIVEVLM — semantic scene analysis / meta-action -> waypoints;
- ORION — VLM reasoning / planning token -> generative trajectory planner.

### Relation to world modeling

These mechanisms organize policy hierarchy, but a semantic decision token can exist with or without a qualifying world-model bridge.

### Current judgment

`PROFILE`

### Reason

Important policy-organization feature, not yet a WAM route boundary.

---

## BP-10 — Explicit visual/BEV/occupancy/latent/graph representation choice

### Evidence

The same higher-order scientific bridge is repeatedly instantiated with:

- video/image futures;
- BEV states;
- occupancy;
- sparse worlds;
- continuous latent states;
- relational graphs;
- discrete tokens.

### Current judgment

`REJECT`

### Reason

Representation substrate by itself fails implementation-invariance and deletion tests as a top-level route distinction.

It remains an important Representation Profile.

---

## BP-11 — Diffusion vs autoregression vs flow matching vs deterministic regression

### Evidence

Each solver family appears across mechanisms that otherwise belong to different research relationships.

Examples:

- diffusion can be video generation, trajectory generation, joint generation, or solver-internal foresight;
- autoregression can be world generation, joint world/action modeling, or sequential action generation;
- flow matching can model action generation, future dynamics, or joint training.

### Current judgment

`REJECT`

### Reason

Solver family is implementation unless it changes the causal program in a mechanism-specific way.

---

## BP-12 — Resolver objective semantics

### Evidence

Candidate mechanisms may score:

- factual-future agreement;
- imitation similarity;
- safety / collision / drivability;
- comfort / progress;
- holistic learned utility;
- physical/dynamic stability;
- confidence or likelihood.

### Current judgment

`PROFILE`

### Reason

Changing what the resolver prefers often leaves the same world-to-planning bridge intact. Objective semantics should remain a conditional resolver profile unless deletion produces a cross-paper branch collapse.

---

## Current promotion queue

The strongest candidates for the next stage are:

1. `BP-02` — world/action coupling topology;
2. `BP-03` — action-consequence reasoning vs non-consequence planning;
3. `BP-07` — direct future-aware world state conditioning vs candidate-indexed consequence branching.

These are **not three accepted routes**. They are three branch questions that currently satisfy the best combination of recurrence, author-framing, deletion sensitivity, negative controls, and implementation invariance.

The most important non-route findings are:

- `BP-01/BP-04`: deployment residue is cross-cutting;
- `BP-05`: predictive representation is currently a learning-transfer lineage;
- `BP-08`: unified world/action representation is currently a paradigm;
- `BP-06`: reciprocal refinement remains singleton;
- `BP-10/BP-11`: representation substrate and solver family are rejected as top-level route distinctions.

## Next gate

Before naming CoreRoutes, run a **minimal-branch reconstruction** using only `BP-02`, `BP-03`, and `BP-07` as candidate branch questions.

The reconstruction must test whether these three questions:

- are independent or hierarchical;
- generate false splits inside coherent paper families;
- erase synthesis nodes such as WorldDrive, Drive-JEPA, Gen-Drive, and Discrete-WAM;
- explain the canonical 12 and broader target-domain cases with fewer assumptions than the old R/W/E/L layer.

If a candidate branch cannot survive that test, demote it before any taxonomy naming.
