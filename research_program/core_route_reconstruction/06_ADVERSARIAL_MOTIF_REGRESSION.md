# Adversarial Regression of the Provisional Causal Bridge Motifs

Status: **PRE-ONTOLOGY ADVERSARIAL AUDIT — NOT A ROUTE SPEC**  
Branch: `research/core-route-reconstruction`  
Date: 2026-09-17  
Parent reconstruction: `05_MINIMAL_BRANCH_RECONSTRUCTION.md`

## 0. Purpose

`05_MINIMAL_BRANCH_RECONSTRUCTION.md` introduced a provisional causal grammar:

- `M0` — world knowledge is compiled into deployed components during learning;
- `M1` — an online world/future state is formed before and directly conditions planning;
- `M2` — a provisional/candidate ego action indexes a world consequence which then changes action commitment/refinement;
- `M3` — world and action variables are generated inside one joint generative process;
- `M4` — world and action repeatedly revise each other before commitment.

These symbols are **reconstruction motifs only**. This audit tries to break them.

The goal is not to maximize fit. The goal is to identify false splits, false merges, multi-motif papers, and abstraction-level mistakes before any CoreRoute naming.

Hard cases:

1. Drive-JEPA PF vs PB;
2. Epona vs DriveLaW vs Metis;
3. GraphWorld / occupancy / prediction-conditioned planners vs WoTE / Drive-WM / SafeDrive;
4. World4Drive vs WoTE vs WorldDrive vs DA-WAM;
5. DrivingGPT vs GenAD vs Gen-Drive vs Discrete-WAM;
6. SeerDrive vs DriveFuture / GraphAD;
7. LAW / Drive-JEPA / ViDAR / DynFlowDrive / Think2Drive / CRAFT / SimWAM / Metis inside `M0`.

---

## 1. Three graph objects must be separated

The previous ontology repeatedly mixed three different mathematical objects.

### G1 — Research genealogy graph

Nodes are papers / method programs. Edges mean intellectual relations such as:

- extends;
- criticizes;
- tightens coupling;
- decouples;
- distills;
- compiles;
- synthesizes.

Question:

> Which scientific problem did this paper inherit, and what answer did it change?

### G2 — Mechanism-route graph

Nodes are recurrent causal bridge motifs. Edges mean refinement / specialization / composition.

Question:

> Through what indispensable causal path does world-model capability change planning?

### G3 — Paper-composition graph

A paper may instantiate more than one bridge motif.

Question:

> Which independent mechanism programs are actually combined in this paper?

Examples:

- WorldDrive = representation inheritance + online candidate-specific future evaluation;
- Drive-JEPA = predictive representation program + an orthogonal multimodal proposal/distillation program;
- Discrete-WAM = representation unification + world-policy joint modeling + hierarchical policy generation.

**Critical rule:** proximity in G1 does not imply equality in G2, and one paper node in G1 does not imply one motif in G3.

This distinction is now considered foundational for the reconstruction program.

---

## 2. Hard pair A — Drive-JEPA PF vs PB

Primary source: `papers/raw_md/P0049_DriveJEPA/P0049_DriveJEPA.raw.md`

### 2.1 Author framing

Drive-JEPA explicitly presents two bottlenecks:

1. planning representations learned from world/video pretraining have shown limited gains and are expensive / poorly scalable;
2. one human trajectory per scene under-supervises multimodal planning.

The paper calls the second direction *orthogonal* to the first. The complete framework combines:

- Driving Video Pretraining via V-JEPA;
- Multimodal Trajectory Distillation;
- Momentum-aware Trajectory Selection.

PF demonstrates the value of the first program with a simple trajectory decoder.

PB adds a richer proposal-centric downstream planner and simulator-distilled supervision.

### 2.2 Adversarial question

Does PB become `M2` merely because it has proposals and a resolver?

No.

For `M2`, the defining bridge is:

`candidate action -> candidate-specific predicted world consequence -> changed commitment`.

Drive-JEPA PB instead has:

`pretrained predictive representation -> candidate generator/scorer -> selection`.

The candidate scorer predicts collision risk, traffic-rule compliance and comfort, but the world-model branch does not instantiate a distinct online future world for each candidate.

### 2.3 Deletion test

Delete proposal generation / selection from PB.

The V-JEPA predictive-pretraining thesis remains and is directly tested by PF.

Delete V-JEPA predictive pretraining.

The WAM-specific thesis of Drive-JEPA is substantially weakened even though the proposal planner can still exist as an ordinary E2E planner.

### Verdict

- PF: `M0-predictive-representation`.
- PB: same `M0-predictive-representation` WAM bridge + non-WM multimodal planner specialization.
- **PF/PB should not be split into different WAM CoreRoutes solely because PB has a candidate resolver.**

This is a major success of the causal-bridge framing over the old R-like commitment topology.

---

## 3. Hard triangle B — Epona vs DriveLaW vs Metis

Primary sources:

- `papers/raw_md/P0001_Epona/P0001_Epona.raw.md`
- `papers/raw_md/P0009_DriveLaW/P0009_DriveLaW.raw.md`
- `papers/raw_md/P0062_Metis/P0062_Metis.raw.md`

This is the strongest test that genealogy and route identity must remain separate.

### 3.1 Epona

Epona's design:

- causal temporal transformer learns temporal dynamics in compressed latent space;
- specialized diffusion heads generate future video and trajectory;
- both are conditioned on the same temporal latent;
- trajectory planning can run while video prediction/rendering is deactivated.

The action path therefore still depends on the shared temporal world representation even when expensive visual output is bypassed.

Provisional bridge:

`history -> shared temporal world latent -> trajectory generator`.

This is closest to `M1`.

### 3.2 DriveLaW

DriveLaW explicitly argues that existing approaches—including Epona-like parallel generation/planning—do not exploit the generator's internal world representation strongly enough.

Its defining bridge is:

`history -> Video DiT internal latent -> Action DiT -> trajectory`.

Deleting the latent-to-planner chain destroys the paper's stated contribution.

This is also `M1`, but a **chained generator-latent realization** inside `M1`.

### 3.3 Metis

Metis explicitly attacks:

- the latency of generating future observations before action;
- interference caused by tightly coupled high-dimensional video and low-dimensional action modeling.

Its asymmetric mask enforces:

- future video tokens can attend to future action tokens;
- action tokens cannot attend to future video tokens.

The paper formalizes deployed action inference as:

`a ~ p(a | z(o_t, l))`,

with future observations used during training and explicit future generation bypassed at inference.

This means the learned world/video program can influence action representation through joint training, but a future-video state is not a required online mediator on the deployed action path.

Provisional bridge:

`world/video learning -> shared/regulated training -> action model parameters/representation -> action`.

This is closest to `M0`, specifically a joint-training-with-future-bypass subtype.

### 3.4 Why this split is not a contradiction

Genealogically:

`Epona <-> DriveLaW <-> Metis`

are close because they debate the same question.

Mechanistically:

- Epona / DriveLaW keep a world-derived state on the action path (`M1`);
- Metis deliberately removes future-world dependence from action inference (`M0`).

Therefore **genealogical closeness can generate a real route split** when the scientific disagreement is exactly about the causal bridge.

### Verdict

- Do not create a top-level “Epona/DriveLaW/Metis family” merely because they are intellectual siblings.
- Preserve their coupling debate in G1.
- In G2, Epona and DriveLaW currently support `M1`; Metis currently supports an `M0` subtype.
- Inside `M1`, “parallel shared temporal state” vs “generator latent chained into planner” is scientifically meaningful but not yet proven to require separate top-level routes.

---

## 4. Hard split C — World-first state mediation vs action-conditioned consequence mediation

The most important current route fork is not “does a future exist?” It is **which variable comes first in the causal chain**.

### 4.1 World-first / state-conditioned side (`M1`)

General form:

`O -> Z -> A`

The future/world representation is formed as a state for planning; an ego alternative is not required to instantiate a distinct world consequence branch.

Independent evidence includes:

- GraphWorld: relational ego-centric world state -> planning queries;
- OccWorld / Drive-OccWorld: future occupancy -> planning;
- UniAD / BeTop / VAD: structured predicted future motion/occupancy/topology -> direct planner;
- GraphAD: future motion-informed interaction graph -> direct ego planning;
- Policy World Model: autoregressive future state tokens -> trajectory decoder;
- DriveLaW: video-generator latent -> Action DiT.

### 4.2 Action-indexed consequence side (`M2`)

General form:

`O -> Ã_k -> Z(Ã_k) -> A*`.

Independent evidence includes:

- WoTE;
- Drive-WM;
- DA-WAM;
- SafeDrive;
- RaWMPC;
- World4Drive;
- WorldDrive;
- DriveFuture.

### 4.3 DA-WAM as unusually strong confirming evidence

Primary source: `papers/raw_md/P0012_DAWAM/P0012_DAWAM.raw.md`.

DA-WAM explicitly frames the scientific issue as *prediction–action alignment*:

- a future representation shared across candidates is inadequate;
- each candidate must have a distinct predicted future latent;
- that candidate-specific latent must directly condition the scorer.

Its deployed chain is explicitly:

`candidate tau_i -> action representation a_i -> future latent Z_i -> scorer(current, a_i, Z_i) -> utility -> select`.

This is nearly a direct statement of the `M2` causal motif.

### 4.4 Negative controls

- DrivoR: `candidate -> scorer -> select`, no candidate-specific future world;
- TOAD: `proposal distribution -> learned reward -> search`, no candidate-specific world consequence;
- Hydra-MDP: multimodal candidate heads + teacher-derived scores, no online predicted world consequence;
- Drive-JEPA PB: proposal/scorer system on predictive pretrained features, no candidate-specific future world branch.

These negative controls prove that **candidate selection is not the defining feature**.

### 4.5 Deletion/collapse test

For WoTE / Drive-WM / DA-WAM / SafeDrive / RaWMPC:

remove `candidate -> consequence`.

The method collapses toward ordinary candidate scoring or world-first/direct planning.

For GraphWorld / OccWorld / UniAD:

adding multiple output trajectories does not automatically turn them into `M2`; only action-indexed world branching would.

### Verdict

`M1` vs `M2` survives the strongest current adversarial test.

Confidence: **HIGH** that this is a real field-level mechanism fork.

---

## 5. Hard family D — World4Drive vs WoTE vs WorldDrive vs DA-WAM

These papers share `M2` ancestry, but the shared ancestry is not the whole scientific story.

### 5.1 World4Drive

Primary source: `papers/raw_md/P0046_World4Drive/P0046_World4Drive.raw.md`.

Author thesis:

- unimodal latent future is insufficient for multimodal driving intention;
- model multiple intention-conditioned futures;
- evaluate/rank planning trajectories with the latent world model.

Core bridge:

`intention / candidate -> intention-specific future latent -> learned selector -> trajectory`.

Its distinctive mechanism is **future plausibility / mode agreement** tied to intention-conditioned latent futures.

### 5.2 WoTE

Core bridge:

`trajectory candidate -> recurrent future BEV rollout -> driving reward -> select`.

Distinctive mechanism:

**explicit online model-based rollout evaluation** over a future horizon.

### 5.3 WorldDrive

WorldDrive is a synthesis node.

Bridge A:

`trajectory-aware world generation -> shared/frozen visual + motion representation -> planner` (`M0`-like representation inheritance).

Bridge B:

`candidate -> distilled future latent -> future-aware reward -> select` (`M2`).

Distinctive mechanism:

retain the planning value of expensive world foresight through a lightweight distilled online surrogate.

### 5.4 DA-WAM

Core bridge:

`candidate -> one-to-one candidate future latent -> factorized scorer -> select`.

Distinctive mechanism:

**decision-aligned future representation**: predictive representation continues to co-adapt with planner optimization and every candidate has its own future latent.

### 5.5 Are these one route?

At a high level: yes, they share one indispensable ancestor:

> the ego alternative must index a future/consequence representation that changes commitment.

At a lower level: no, their distinctive bridge realization is not interchangeable:

- factual-future plausibility / intention selection;
- recurrent environment rollout + reward;
- distilled surrogate foresight + reward;
- one-to-one decision-aligned future latent + scorer.

### Verdict

Treat `M2` as a **major ancestor motif**, not a finished leaf class.

Do not prematurely decide whether the four realizations require two, three, or four subroutes. That requires another deletion/collapse pass focused only inside `M2`.

---

## 6. Hard family E — strict joint-generation gate for `M3`

`M3` risks becoming a junk drawer for every architecture that shares a latent or trains world/action together. A strict gate is required.

### 6.1 Proposed M3 gate

A planning mode qualifies as `M3` only if all hold:

1. **common generative program:** world/future variables and ego-action variables are prediction targets / generated variables of one generative program, rather than one being only an external condition for the other;
2. **co-defined sample/process:** the generated world/action outputs belong to the same sampled/generated future process or interleaved generative sequence;
3. **planning relevance:** the action output is an actual planning output in the scoped mode, not merely a conditioning signal used to render a world;
4. **not merely shared representation:** shared encoder, shared temporal latent, multitask loss, or parallel heads are insufficient by themselves;
5. **not merely reciprocal:** repeated world->action->world refinement belongs to `M4`, not `M3`, unless a distinct joint-generation mode also exists.

### 6.2 DrivingGPT

Primary source: `papers/raw_md/P0040_DrivingGPT/P0040_DrivingGPT.raw.md`.

DrivingGPT constructs a single interleaved discrete visual/action “driving language” and trains one autoregressive next-token model to predict both modalities.

It passes the M3 gate strongly.

### 6.3 GenAD

Primary source: `papers/raw_md/P0029_GenAD/P0029_GenAD.raw.md`.

GenAD explicitly critiques serial motion-prediction-before-planning and instead models the future ego and surrounding-agent trajectories together in a structural latent trajectory space.

It passes the joint-future gate at the trajectory/world-agent level.

### 6.4 Gen-Drive

D01 evidence supports sampled joint ego/agent future scenes. In multi-sample mode, a learned reward can rank joint futures downstream.

The ranking stage does not erase the joint birth of world/agent and ego trajectories.

It passes M3 in the relevant joint-generation mode and may compose `M3 + downstream resolver`.

### 6.5 Discrete-WAM

The joint world-policy modeling mode predicts action and future visual tokens in the same unified token-editing process.

It passes M3 **for that mode**.

The deployed policy mode should not automatically inherit M3 if its actual action path is decision-token -> action-token generation without joint future visual generation.

### 6.6 Epona negative control

Epona shares a temporal latent and has specialized trajectory/video diffusion heads, but the heads are parallel specialized outputs rather than one necessarily joint world-action sample.

Therefore shared latent + parallel outputs is **not sufficient** for M3.

Current best reading places Epona's planning bridge under M1, with a joint-training/shared-state profile.

### 6.7 Metis negative control

Metis jointly trains video/action experts, but action inference is explicitly masked from future-video tokens and future generation is bypassed.

Thus joint training is **not sufficient** for M3.

### Verdict

`M3` survives if defined by strict **co-generation / co-birth**, not by generic “jointness.”

Confidence: **MEDIUM-HIGH**.

---

## 7. Hard family F — SeerDrive vs DriveFuture vs GraphAD

### 7.1 SeerDrive

SeerDrive's paper-level thesis is explicit bidirectionality:

`future world -> plan -> changed ego state/plan -> revised future world -> ...`.

The reciprocal loop is the claimed paradigm shift.

### 7.2 DriveFuture

D01 evidence supports:

`provisional action/trajectory -> predicted future latent -> guidance inside diffusion planning -> final trajectory`.

This is naturally explained by M2 with **solver-internal consequence feedback**.

What is not yet established is repeated alternation in which the revised action regenerates a new world state multiple times before commitment.

### 7.3 GraphAD

GraphAD iteratively refines future motion / graph representations, but current evidence does not establish:

`ego plan -> changed world prediction -> revised ego plan -> changed world prediction`.

Internal iterative predictive feature refinement is not enough.

### Verdict

`M4` remains a scientifically strong **singleton extension** anchored by SeerDrive.

Do not collapse every iterative solver/refiner into M4.

Do not yet promote M4 to a mature family without independent replication.

---

## 8. Hard family G — `M0` is not one leaf route

The “compiled world knowledge” ancestor survives, but it is internally heterogeneous enough that treating it as one final route would recreate the old W0 failure.

### M0-A — predictive representation shaping / transfer

Examples:

- LAW;
- Drive-JEPA;
- ViDAR;
- DriveWorld;
- ReWorld;
- WA-JEPA.

Shared thesis:

> predictive/world learning improves the representation consumed by a deployed planner, while explicit future computation need not remain online.

Important internal distinction:

- LAW: action-conditioned future prediction tightly coupled to E2E learning;
- Drive-JEPA / ViDAR / DriveWorld: larger pretraining/transfer separation;
- ReWorld / WA-JEPA: shared predictive representations with action alignment.

Whether these require multiple leaf routes remains open.

### M0-B — world-derived evaluator/scorer supervision

Anchor:

- DynFlowDrive.

World dynamics determine which candidate should be scored as stable/safe; the world model is then removed and the scorer performs deployment selection.

This is not the same learning transfer as predictive representation pretraining.

### M0-C — imagined/simulator world -> policy optimization

Examples:

- Think2Drive;
- CRAFT;
- CausalDrive policy post-training.

World/simulator consequences are consumed during policy optimization, and preference/return is compiled into policy parameters.

Again, this is not equivalent to representation pretraining.

### M0-D — joint world/action training with future branch bypass

Examples:

- Metis;
- SimWAM.

Future prediction participates in joint training, but action deployment is intentionally made independent of explicit future generation.

### Important correction to earlier `BP-01 = PROFILE`

The previous judgment that online-vs-compiled is merely a profile was correct **at the leaf level** but incomplete **at the hierarchy level**.

“Compiled world knowledge” may be a useful high-level ancestor branch, provided it is immediately subdivided by *what is compiled and through which learning mechanism*.

Thus:

- `compiled vs online` is too coarse to be a final route;
- but it can still be a meaningful first-level structural split in a hierarchical map.

This is a level-dependent distinction, not a contradiction.

---

## 9. Does the provisional causal spine survive?

After the adversarial tests, the current minimal causal spine is:

### Spine A — compiled world knowledge

World capability changes planning through learning/parameter transfer; no required online world/future mediator remains.

**Status:** strong ancestor, unresolved leaves.

### Spine B — online world-first mediation

`O -> Z -> A`.

A world/future state is formed online, then conditions action.

**Status:** strong recurrent motif.

### Spine C — action-conditioned consequence mediation

`O -> Ã -> Z(Ã) -> A*`.

A provisional/candidate ego behavior instantiates a distinct consequence which changes selection/refinement.

**Status:** strongest recurrent motif with clean negative controls.

### Spine D — joint world-action generation

`O -> G -> (Z, A)` under a strict co-generation gate.

**Status:** strong candidate, exact mode scope required.

### Spine E — reciprocal refinement

`A^0 -> Z^1 -> A^1 -> Z^2 -> ...`.

**Status:** scientifically meaningful but currently singleton/immature.

These are **not accepted CoreRoutes**. They are the minimal causal spine that survived this regression.

---

## 10. What the spine explains that R-W-E-L did not

### Drive-JEPA PF/PB

Both preserve the same WAM bridge ancestry under predictive representation transfer; PB's candidate planner does not falsely promote it into action-consequence reasoning.

### World4Drive / WoTE / WorldDrive

Their shared action-conditioned consequence ancestry is preserved, while their internal future-evaluation realization remains available for sub-branch analysis.

### Epona / DriveLaW / Metis

Their intellectual debate is preserved without forcing all three into one route: Epona/DriveLaW keep world-derived state on the planning path; Metis deliberately compiles/bypasses future generation at inference.

### DrivoR / TOAD / Hydra-MDP

Candidate selection without a world-consequence branch remains an explicit negative control rather than being mistaken for a WAM consequence route.

### SeerDrive

Its reciprocal innovation remains visible rather than being flattened into “future state + planner”.

### Discrete-WAM

Its joint world-policy mode can qualify under strict M3 while its representation paradigm and policy mode remain distinct conceptual contributions.

---

## 11. Remaining failure modes

The causal spine is still vulnerable to at least six errors:

1. `M1` may be too broad: generator latent, occupancy future, relational state, and autoregressive future tokens may require real subroutes.
2. `M2` may be too broad: plausibility matching, explicit rollout/reward, surrogate future scoring, and solver-internal foresight may be genuinely different branch points.
3. `M0` definitely requires subdivision; current four subfamilies are only hypotheses.
4. `M3` jointness must be checked mode-by-mode, especially when paper claims “unified” but inference uses a separate action path.
5. `M4` lacks independent replication.
6. Hybrid/synthesis papers may not fit a tree; the final representation may need a route DAG with compositional membership.

---

## 12. Next gate

The next step should **not** invent names.

Build a full provisional projection of canonical + broader in-domain papers onto the minimal causal spine, allowing:

- one primary motif;
- optional secondary motif(s);
- explicit `NOT-WAM-BRIDGE` for ordinary downstream planner components;
- unresolved / ambiguous status;
- sub-branch notes without promoting them.

Then run four audits:

1. **family coherence:** Drive-JEPA, WorldDrive, Discrete-WAM modes;
2. **false merge:** within M0 / M1 / M2;
3. **false split:** papers with different implementations but same bridge;
4. **held-out prediction:** can the spine describe a new target-domain paper before creating another motif?

Only after that projection should provisional route names be considered.
