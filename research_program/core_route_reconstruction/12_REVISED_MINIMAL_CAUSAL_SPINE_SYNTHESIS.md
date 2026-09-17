# Revised Minimal Causal Spine Synthesis

Status: **SYNTHESIS AFTER ADVERSARIAL AUDITS — NOT AN ACCEPTED ONTOLOGY**  
Branch: `research/core-route-reconstruction`  
Date: 2026-09-17  
Inputs: `00` through `11` in this directory.

## 0. What has changed

The project started from a flat human signature:

`R–W–E ⊕ L`.

After E-axis audit, deployment-DAG failure, canonical genealogy reconstruction, broader-corpus pressure, branch-point reduction, and M0/M1/M2/M3 adversarial audits, the central object has changed.

The strongest current hypothesis is:

> **A major WAM planning route is defined primarily by the implemented causal factorisation through which world-model computation changes action/planning.**

This is not the same as:

- what representation is used;
- whether trajectories are multimodal;
- which reward is used;
- which architecture is used;
- whether training is joint;
- whether the paper calls itself “unified”.

The decisive question is:

> **At the point where world knowledge causally changes driving behavior, who conditions whom and when?**

---

## 1. Four graph objects must remain separate

### 1.1 Route-factorisation graph

Describes recurrent causal bridge motifs.

Question:

> How does world-model computation reach final action?

This is the candidate object for the future route ontology.

### 1.2 Research-genealogy graph

Describes intellectual relations among papers:

- extends;
- criticizes;
- tightens;
- decouples;
- distills;
- compiles;
- synthesizes.

Epona / DriveLaW / Metis are close here even when their deployed bridge differs.

### 1.3 Profile / realization graph

Describes replaceable or cross-cutting choices:

- explicit vs latent future;
- endpoint vs horizon;
- reward semantics;
- action proposal mechanism;
- rollout fidelity;
- predictive pretraining vs end-to-end auxiliary loss;
- diffusion vs AR vs flow;
- BEV vs RGB vs occupancy vs graph.

A profile can later be promoted only if repeated evidence shows that changing it consistently changes the causal route.

### 1.4 Paper-composition graph

Allows one paper to instantiate multiple mechanisms.

Examples:

- WorldDrive = predictive/generative representation inheritance + online candidate-consequence evaluation;
- Discrete-WAM = representation unification + joint world-policy mode + separate hierarchical policy mode;
- Gen-Drive = joint future generation + downstream evaluation and optional reward fine-tuning.

**No single graph should be forced to encode all four roles.**

This is now a foundational program rule.

---

## 2. Revised minimal causal spine

The symbols below remain working labels. They are not final names.

### C0 / M0 — compiled world knowledge

World/predictive/simulation computation changes deployed decision components through learning, but no qualifying online world/future mediator is required at deployment.

Deployment skeleton:

`O -> A` using parameters/features learned through world-related training.

Important mature subbranches:

#### M0-R — predictive representation / action-feature shaping

World prediction teaches the representation/action model.

Anchors:

- LAW;
- Drive-JEPA;
- ViDAR;
- DriveWorld;
- ReWorld;
- WA-JEPA;
- Metis / SimWAM as joint-training + future-bypass realizations.

#### M0-P — imagined/simulated consequence policy optimization

World/simulator rollout provides return/advantage used to optimize policy preference.

Anchors:

- Think2Drive;
- CRAFT;
- CausalDrive policy post-training.

#### M0-S — world-derived decision supervision distilled into scorer

World consequence analysis creates target scores/labels learned by a deployed evaluator.

Anchor:

- DynFlowDrive.

Status: coherent but under-replicated.

### C1 / M1 — online world-first mediation

Implemented dependency:

`O -> Z -> A`.

A qualifying online world/model state is formed first and directly conditions planning.

Sublineages currently visible:

#### M1-F — explicit forecast as planning intermediate

Examples:

- Policy World Model;
- DriveDreamer action path;
- selected structured prediction->planning systems after domain qualification.

#### M1-S — internal online world/model state as planning state

Examples:

- DriveLaW;
- GraphWorld;
- Epona planning path (probable / medium-high confidence).

Critical gate:

> a world-pretrained current feature is not sufficient. A separately traceable online world/dynamics/generative state must remain on the causal path.

M1-F vs M1-S is currently a sublineage/profile split, not yet accepted as two CoreRoutes.

### C2 / M2 — action-conditioned consequence mediation

Implemented dependency:

`O -> A~ -> Z(A~) -> A*`.

An ego alternative must exist before its relevant consequence can be instantiated; that consequence then changes commitment/refinement.

#### M2-EVAL — consequence evaluates alternatives [mature]

Anchors:

- WoTE;
- World4Drive;
- WorldDrive;
- DA-WAM;
- Drive-WM;
- SafeDrive;
- RaWMPC.

Clean negative controls:

- DrivoR;
- TOAD;
- Hydra-MDP;
- Drive-JEPA PB.

#### M2-REFINE — consequence guides action solver/refinement [early]

Anchor:

- DriveFuture.

Potentially independent but under-replicated.

Current non-route profiles inside M2:

- endpoint vs horizon;
- explicit rollout vs latent vs distilled surrogate;
- plausibility vs utility vs safety/reward;
- counterfactual fidelity/reactivity;
- candidate generator type.

### C3 / M3 — joint world-action future generation

Implemented dependency:

`(Z, A) <- one coupled generative future process`.

The world and ego action are generated variables of one coherent future, rather than one serving only as a prior mediator or external condition for the other.

Strong anchors:

- DrivingGPT;
- GenAD;
- Gen-Drive;
- Discrete-WAM joint world-policy mode;
- OccWorld after full-paper correction.

Strict exclusions:

- Epona: shared temporal latent + parallel specialized heads is not automatically co-generation;
- Metis: joint training with future branch bypass is not joint deployed generation.

Visible realization sublineages:

- unified visual/action token process;
- joint structured ego/environment future generation.

Current status: one strong major branch; representation differences remain profile-level.

### C4 / M4 — reciprocal world-action refinement

Implemented dependency:

`A^0 -> Z^1 -> A^1 -> Z^2 -> ... -> A*`.

World and action states alternately revise each other before commitment.

Strong anchor:

- SeerDrive paper.

Rejected near-equivalents at current evidence depth:

- GraphAD iterative predictive graph;
- DriveFuture consequence-guided diffusion refinement.

Current status: scientifically meaningful **singleton extension**, not mature field family.

---

## 3. Why this spine is materially better than R-W-E-L

### 3.1 Drive-JEPA PF/PB no longer break family coherence

Both have the same world-to-planning bridge:

`predictive pretraining -> deployed representation`.

PB's proposal/scoring architecture is a downstream planner specialization, not a new WAM route unless the proposals themselves index world consequences.

### 3.2 Candidate planners are no longer automatically WAM relatives

DrivoR / TOAD / Hydra-MDP may look like WoTE at the final `candidate -> score -> select` layer.

But only WoTE has:

`candidate -> predicted world consequence -> score`.

This sharply separates planner profile from world-model route.

### 3.3 World4Drive / WoTE / WorldDrive share the right thing

They share the action-conditioned consequence ancestor without pretending their internal methods are identical.

Their real differences remain visible as sublineages:

- intention/future plausibility;
- recurrent rollout + reward;
- distilled future surrogate + reward;
- representation inheritance as an extra WorldDrive parent.

### 3.4 Epona / DriveLaW / Metis disagreement is preserved

Genealogically close:

all debate world/action coupling.

Mechanistically:

- Epona / DriveLaW retain an online world/model state that mediates planning;
- Metis deliberately removes future-world dependence from deployed action inference and compiles benefit through training.

The route graph is allowed to split intellectual siblings when the split is exactly their scientific disagreement.

### 3.5 OccWorld correction is naturally representable

Shallow skeleton suggested forecast->planning.

Full paper reveals joint generation of future scene and ego variables.

The factorisation spine can correct M1 -> M3 without inventing a new axis.

### 3.6 E disappears from headline route identity without losing information

Plausibility, imitation compatibility, safety, reward, comfort, etc. remain Resolver/Consequence-Evaluation Profiles.

They matter, but they do not define who conditions whom in the world-action causal program.

---

## 4. The first-principles route question can now be stated precisely

For every target-domain planning program, ask in this order:

### Gate 0 — Is there a qualifying world-model contribution?

Can a separately traceable predictive/dynamics/world program be causally connected to final one-stage planning?

If no:

`NOT-WAM-BRIDGE` / adjacent control.

### Gate 1 — Does the relevant world computation survive online?

If no:

enter M0 and ask what was compiled:

- representation/features;
- policy preference through imagined return;
- evaluator/scorer supervision;
- other yet-unseen transfer mechanism.

### Gate 2 — If online, what is the implemented conditioning order?

#### World first

`Z -> A` => M1.

#### Ego alternative first

`A~ -> Z(A~) -> A` => M2.

#### Joint future

`(Z,A)` co-generated => M3.

#### Repeated alternation

`A -> Z -> A -> Z ...` => M4.

This is the current minimal decision procedure.

---

## 5. Important warning: this is not simply a tree

Although Gate 1/2 looks tree-like, real papers can compose mechanisms.

WorldDrive:

- M0-R representation inheritance;
- M2-EVAL future surrogate selection.

Gen-Drive:

- M3 joint future generation;
- downstream resolver;
- optional reward-based parameter optimization.

Discrete-WAM:

- M3 joint mode;
- separate policy mode;
- representation paradigm spanning both.

Therefore the final artifact should likely contain:

1. a **minimal route spine**;
2. a **composition notation** for multi-bridge papers;
3. profiles for mediator, resolver, lifecycle and learning realization;
4. a separate paper genealogy DAG.

A single mutually exclusive paper label is unlikely to be sufficient.

---

## 6. What remains unresolved before naming CoreRoutes

### 6.1 M0-S replication

DynFlowDrive is a strong mechanism, but independent exact analogues are still sparse.

### 6.2 M1 leaf split

Explicit forecast vs internal world/model state is real but not yet shown to be route-level rather than mediator-level.

### 6.3 M2-REFINE replication

DriveFuture-like solver-internal foresight needs independent examples.

### 6.4 M3 semantic gate

Need confirm that “environment future” may include structured agent/occupancy futures without making the category so broad that any joint trajectory predictor qualifies.

### 6.5 M4 replication

SeerDrive remains the main strong anchor.

### 6.6 Domain boundary

UniAD/VAD/BeTop-like prediction-conditioned planners can instantiate an M1-shaped dependency while still being adjacent non-WAM controls depending on the strict world-model gate. Route shape and domain membership must remain separate.

---

## 7. Current confidence

### Very high / high

- route discovery should no longer use flat R-W-E-L axes as the primary engine;
- implemented world/action conditioning order is a better first-principles abstraction;
- M1 vs M2 vs M3 are genuinely different causal factorisations;
- M0 must be subdivided by what world learning compiles into;
- candidate resolver existence and resolver semantics are not top-level WAM route definitions;
- one paper may instantiate multiple motifs;
- paper genealogy and route hierarchy must remain separate.

### Medium/high

- M0-R and M0-P are mature subbranches;
- M2-EVAL is a mature subbranch;
- M3 is mature enough to remain a major branch;
- Epona is M1-like; Metis is M0-R-like.

### Medium / low-medium

- M0-S as stable field family;
- M1-F vs M1-S as final route split;
- M2-REFINE as stable field family;
- M4 as mature route.

---

## 8. Immediate next step

Do not name final routes yet.

The next highest-value audit is **counterexample hunting against the factorisation spine**:

Search existing D01/D02 corpus and then a deliberately chosen small number of additional target-domain papers for cases that cannot be faithfully represented as:

- compiled;
- world-first;
- action-conditioned consequence;
- joint future;
- reciprocal refinement;
- or a composition of these.

A new branch is justified only if a paper introduces a new implemented world-action dependency, not merely a new state representation, reward, solver, or training target.

Success criterion:

> The spine predicts where a previously unclassified WAM paper belongs and explains its nearest scientific relatives **before** any new code is created.

Only after this counterexample hunt should human-readable CoreRoute names be proposed.
