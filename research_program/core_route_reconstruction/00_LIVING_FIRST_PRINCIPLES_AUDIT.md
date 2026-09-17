# WAM + One-Stage Autonomous Driving: Living First-Principles Core-Route Audit

Status: **LIVING AUDIT LOG — NOT AN ONTOLOGY SPEC**  
Branch origin: `codex/domain-map-d02-w1e-rerun`  
Baseline commit: `368c9a848e241bfb7bf2e2d61242269d5e438af6`  
Created: 2026-09-17  
Scope: WAM + one-stage / end-to-end autonomous driving  
Owner role of this file: preserve high-value ontology reasoning, reversals, evidence, and unresolved questions so that later work does not silently regress to earlier assumptions.

---

## 0. Why this file exists

The project originally attempted to explain WAM + one-stage autonomous-driving mechanisms through a human route layer such as:

`R–W–E ⊕ L`

This work produced useful formal discipline, but subsequent audits exposed a more fundamental risk:

> We may have designed axes first and then become increasingly good at projecting papers into them, instead of reconstructing the field's actual mechanism families from the papers themselves.

The real research objective is not to make a compact code system. It is:

> **Identify the genuinely different world-model-to-planning routes in WAM + one-stage autonomous driving, and distinguish genuine mechanism differences from implementation, representation, objective, or training-detail differences.**

This file therefore does **not** treat R/W/E/L as ground truth. It records the process of challenging them.

A central methodological rule is:

> **Routes must grow from papers; papers must not be forced into routes.**

---

## 1. Current target question

The first-principles target is:

> **“WAM + 一段式自动驾驶，究竟有哪些本质不同的世界模型规划路线？”**

A candidate route should explain a mechanism-level difference in how world-model capability changes planning or action generation.

A route distinction should not be promoted merely because two systems differ in:

- RGB vs BEV vs latent representation;
- Transformer vs diffusion vs flow matching;
- expert vs teacher vs simulator supervision;
- one scalar value vs several decomposed metrics;
- image-space vs feature-space generation;
- a different loss function;
- a different benchmark;
- a different implementation detail.

Those differences may matter, but they are not automatically **route differences**.

---

## 2. First major correction: E is probably not a headline route axis

### 2.1 Original assumption

The human layer treated E as a peer of R and W:

`R–W–E ⊕ L`

Representative projections included:

- World4Drive: `RB + W3 + EW`
- WorldDrive: `RB + W3 + EV`
- WoTE: `RB + W4 + EF/ED`

This suggested that future agreement, holistic value, decomposed outcomes, and behavior compatibility might define different core routes.

### 2.2 Audit pressure

The critical test was:

> Hold candidate creation, candidate identity, candidate-specific consequence construction, scorer I/O, common resolver, and commitment timing fixed. Replace only the criterion semantics.

For example:

`candidate -> consequence -> score -> resolver -> action`

with score semantics changed among:

- world/future agreement;
- holistic planning value;
- decomposed safety/comfort/progress outcomes;
- behavior compatibility.

If the world-to-decision mechanism remains the same, then the changed criterion is not sufficient to define a new headline route.

### 2.3 Current judgment

Current judgment:

**E contains important information, but its natural role is closer to `ResolverProfile` than to a global route axis.**

This is supported by a structural fact already visible in the formal backend: resolver semantics only become meaningful when a resolver exists. Thus E/V is conditional on the existence and form of a resolver; it is not obviously an independent global axis.

### 2.4 EF strict lifecycle rule

Expert supervision must not automatically imply behavior-compatibility resolver semantics.

`EF`-like semantics are justified only when all are true:

1. an explicit candidate resolver exists;
2. expert/factual behavior supervision trains a behavior-compatibility scorer;
3. that scorer is retained and called during deployment;
4. its output causally participates in final candidate selection.

If expert trajectories only train a direct policy and no compatibility scorer exists online, then the information belongs to learning/provenance, not deployment resolver semantics.

### 2.5 Consequence

A more faithful temporary representation became:

`R–W ⊕ L + ResolverProfile`

But this was only an intermediate improvement, **not** accepted as the final ontology.

---

## 3. Second major correction: `R–W ⊕ L + ResolverProfile` is still probably not the right final structure

After E was demoted, a new problem became visible: R, W, and L themselves may also mix distinct conceptual levels.

Examples:

- `RJ` already says world and action are generated jointly, while `W5` also says joint world-action carrier. These are strongly dependent rather than cleanly orthogonal.
- `RR` already embeds world-policy reciprocal refinement; adding a W code often describes the object moving through that loop rather than an independent route dimension.
- `RH` describes hierarchical policy organization, which may be important but does not directly answer how a world model changes planning.
- L describes how capability is learned and transferred. This can be essential to the paper's idea, but it is not automatically a deployment route coordinate.

The deeper concern is therefore not “which code should E become?” but:

> **Were we asking for the wrong mathematical object by insisting on a flat orthogonal axis system?**

Current suspicion: the field may be better represented by a mechanism map with a core world-to-planning bridge plus conditional profiles, rather than a fixed Cartesian product of peer axes.

---

## 4. Third major correction: deployment DAG alone is insufficient

### 4.1 Tempting simplification

A proposed reset was:

> Ignore R/W/E/L, draw each paper's deployment DAG, then cluster papers by `world information -> final decision` interface.

This was an improvement over projecting old codes, but it was still too coarse.

### 4.2 Why it fails

LAW, Drive-JEPA, Metis, DynFlowDrive, and some Epona planning modes may all reduce at deployment to something that superficially looks like:

`current input -> planner -> trajectory`

Yet their research mechanisms are fundamentally different:

- LAW uses action-conditioned future-latent prediction as an end-to-end self-supervised learning signal.
- Drive-JEPA uses scalable predictive video pretraining and then transfers the learned encoder.
- Metis uses joint world/action training with asymmetric information flow so future video generation can be bypassed online.
- DynFlowDrive uses a trajectory-conditioned dynamic world model to create supervision for a scorer, then removes the world model at inference.
- Epona learns shared temporal latent structure through joint video/trajectory modeling, while allowing planning-only inference.

If we look only at the final deployment DAG, these distinct routes collapse incorrectly.

### 4.3 Revised comparison object

The more faithful object is the **complete world-to-planning causal program**:

> How does world-model capability travel from learning world dynamics to changing the final planning behavior, across both training and deployment, while keeping training and deployment explicitly separated?

This includes:

- what world-related capability is learned;
- where it is learned;
- whether action conditions the world model;
- whether the planner reads a world state, generated future, surrogate future, score, or only modified parameters;
- whether world-model computation remains online;
- whether the world and policy are parallel, chained, reciprocal, jointly generated, or compiled into another component;
- what is removed at deployment;
- what survives and carries the learned world knowledge into the final action.

This object is richer than a deployment DAG but narrower than “everything the paper does.”

---

## 5. Important unit-of-analysis correction

A paper can contain multiple modes:

- world generation;
- planning;
- joint world-policy training;
- simulator mode;
- counterfactual evaluation;
- auxiliary pretraining.

The project previously learned to split artifacts correctly, but the route-reconstruction task needs an additional rule:

> **When reconstructing a planning route, compare the program that produces the final driving decision. Other modes are retained only insofar as they causally explain how that planning program acquired or uses world-model capability.**

This prevents errors such as classifying an entire paper by a world-generation mode that is not actually used to produce the deployed action.

---

## 6. Current first-principles route criterion: the Core-Bridge Deletion Test

A useful candidate test has emerged:

> **If we remove the paper's claimed world-to-planning bridge, does the paper's main mechanism idea collapse or reduce to an ordinary baseline?**

If yes, that bridge is a strong candidate for route-defining status.

Examples:

- WoTE without `candidate -> world rollout -> reward` loses the central method.
- DriveLaW without `video-generator latent -> Action DiT` loses the claimed chained unification.
- SeerDrive without iterative world↔planning feedback reduces toward one-shot future-aware planning.
- Metis without controlled asymmetric decoupling loses the mechanism it claims resolves the coupling/latency problem.

In contrast, changing RGB to BEV or replacing one reward decomposition with another often does not destroy the core bridge; such changes are less likely to define a top-level route.

This test is provisional but currently more informative than asking whether a paper changes a single old ontology code.

---

## 7. Canonical-paper relationship reconstruction: current state

The following are **relationship observations**, not final route labels.

### 7.1 LAW — predictive self-supervision as planning representation shaping

Core problem statement:

> End-to-end planning needs better scene representations; static representation learning underuses temporal data and ego-action-conditioned future structure.

Core mechanism:

- current visual latent -> planner predicts ego trajectory;
- current latent + predicted ego trajectory -> latent world model predicts future latent;
- future frame latent supervises predicted future latent;
- this self-supervised future-prediction task jointly improves current representation and trajectory prediction.

Important interpretation:

LAW is not primarily “online imagination for action selection.” Its central contribution is using action-aware future prediction to shape representations and the planner during learning.

Closest conceptual relative at present: Drive-JEPA, but not identical.

### 7.2 Drive-JEPA — scalable predictive representation pretraining + separate multimodal planner distillation

Primary source: `papers/raw_md/P0049_DriveJEPA/P0049_DriveJEPA.raw.md`

Core problem statement:

1. pixel-generative world-model pretraining is expensive and may waste capacity on planning-irrelevant visual detail;
2. one expert trajectory per scene under-supervises multimodal planning.

Core mechanism:

- large-scale driving video -> V-JEPA predictive representation pretraining;
- pretrained encoder -> planner;
- simulator-generated pseudo-trajectories supplement human demonstrations;
- proposal-centric planner produces multiple candidates;
- learned safety/rule/comfort scoring plus momentum term selects final trajectory.

Important interpretation:

The world-model/predictive component is mainly a **representation-learning route**. Candidate diversity and final selection are separately improved through simulator distillation and selection design.

Relation to LAW:

Common idea: predictive learning can improve planning without explicit online future simulation.

Difference:

- LAW tightly couples action-conditioned future prediction into end-to-end training;
- Drive-JEPA emphasizes scalable predictive pretraining and later transfer, while multimodal planning improvements come from another supervision route.

Thus “both are W0 at runtime” is far too coarse to explain their relationship.

### 7.3 Epona — shared temporal world latent with parallel multimodal generation

Primary source: `papers/raw_md/P0001_Epona/P0001_Epona.raw.md`

Core problem statement:

Existing diffusion world models struggle with long variable-horizon generation, while autoregressive token approaches sacrifice continuous fidelity and planning precision.

Core design:

- causal temporal transformer models temporal dynamics in compressed latent space;
- separate diffusion decoders generate next video frame and future trajectory;
- video and trajectory streams share temporal latent / joint training context;
- planning-only inference can deactivate video generation for efficiency.

Important interpretation:

Epona's planning benefit is not “score several imagined futures.” It is closer to:

> jointly learning temporal world structure so that a shared latent supports both world generation and action generation, while allowing the expensive video output branch to be disabled for planning.

This becomes critical when compared with DriveLaW and Metis.

### 7.4 DriveLaW — chained generator representation into planner

Core claim:

> Internal latent representations learned by the video generator should directly become the planning state.

Core mechanism:

- video generator learns spatiotemporal generative representation;
- intermediate/mid-denoising video latent is extracted;
- Action DiT is directly conditioned on that latent;
- planner therefore consumes the generator's internal world representation rather than only sharing supervision or a parallel trunk.

Important relation:

DriveLaW treats Epona-like parallel generation/planning as insufficiently coupled.

This is evidence that **coupling topology between world model and planner may itself be a real route-defining question**.

### 7.5 Metis — controlled decoupling and asymmetric information flow

Core problem statement:

Existing WAMs suffer from:

- high inference latency when future observations must be generated before action;
- representational interference when high-dimensional video generation and low-dimensional action prediction are tightly coupled.

Core mechanism:

- separate video-generation expert and action expert;
- shared latent interaction during training;
- asymmetric attention mask: future video can see future action, but action is prevented from depending on future video tokens;
- future video prediction therefore trains useful dynamics while action inference can bypass future video generation.

Important relation:

Epona / DriveLaW / Metis form a highly informative conceptual triangle:

- Epona: shared latent + parallel generation/planning;
- DriveLaW: tighter chained coupling, generator latent directly drives planner;
- Metis: deliberate controlled decoupling to avoid interference and latency.

This relationship is almost invisible in the old R/W/E/L compression, yet it may represent a genuine research branch in the field.

### 7.6 World4Drive — intention-conditioned latent future plausibility for multimodal planning

Core problem statement:

A single latent future is insufficient to represent multimodal driving intentions; planning should reason over multiple possible intentions and corresponding world evolutions.

Core mechanism:

- trajectory vocabulary -> multimodal intention queries;
- current physical world latent + intention -> predicted intention-specific future latent;
- training uses factual future latent to identify the best-matching future mode;
- ScoreNet learns to predict which future/intention mode is most plausible;
- inference selects the trajectory associated with the highest world-model score.

Important interpretation:

Although superficially similar to `candidate -> future -> score -> select`, its central idea is not the same as WoTE's explicit reward-based rollout evaluation.

World4Drive is strongly tied to **multimodal intention-conditioned future plausibility / mode selection**.

### 7.7 WoTE — explicit online model-based trajectory evaluation

Primary source: `papers/raw_md/P0045_WOTE/P0045_WoTE.raw.md`

Core problem statement:

Evaluating a trajectory from the current state alone is inadequate. A planner should know the future caused by each candidate before deciding.

Core mechanism:

- planner proposes multiple trajectories;
- each trajectory forms a state-action pair with current BEV state;
- BEV world model recurrently predicts future states for each candidate;
- reward model evaluates candidates using predicted future states;
- highest-reward candidate is selected.

Important interpretation:

WoTE is a strong example of explicit **online model-based trajectory evaluation**.

Its world model is not merely a representation learner or training teacher; it participates directly in online candidate consequence evaluation.

### 7.8 WorldDrive — representation unification plus distilled online foresight

Primary source: `papers/raw_md/P0042_WorldDrive/P0042_WorldDrive.raw.md`

Core problem statement:

Scene generation and planning are representation-misaligned: world models learn visual dynamics while planners learn motion separately.

Core mechanism contains at least two distinct bridges:

1. **representation inheritance**: trajectory-aware world model organizes visual and motion representation, then transfers/fixes those encoders for planning;
2. **distilled future consequence evaluation**: heavy candidate-specific world generation is distilled into a lightweight online future surrogate / rewarder.

Important interpretation:

WorldDrive is not simply “another WoTE.” It explicitly studies how to retain world-model foresight after removing expensive world generation.

It occupies an important position in a possible continuum:

`full online world rollout -> distilled online future surrogate -> world-derived scorer only`

but the existence of a continuum does **not** imply these methods belong to the same final route.

### 7.9 DynFlowDrive — world model as a teacher of trajectory evaluation, removed at inference

Core problem statement:

Endpoint regression misses the dynamics of how a trajectory changes the scene. Two trajectories can reach similar endpoints while inducing very different transition stability and safety.

Core mechanism:

- candidate trajectory conditions a latent flow-based world model;
- world model models continuous state-transition dynamics;
- transition stability plus reconstruction / trajectory criteria define an optimal candidate during training;
- this selected target supervises the planner's score head;
- **during inference, the world model is not involved**;
- planner directly chooses the candidate with highest learned score.

Important interpretation:

DynFlowDrive **compiles world-model evaluation into a deployment scorer**.

This is a strong example showing why deployment-only DAG and training-only DAG are each insufficient by themselves.

### 7.10 SeerDrive — reciprocal world-planning refinement

Core problem statement:

One-shot planning underuses future dynamics because future scene and ego trajectory are mutually dependent.

Core claim:

> Future scene evolution and ego planning should interact bidirectionally rather than through a one-way prediction-to-planning pipeline.

Core mechanism:

- current state/ego feature -> future BEV prediction;
- future BEV conditions planning;
- updated plan/ego feature feeds back into scene modeling;
- repeated interaction progressively refines both future scene and trajectory.

Important interpretation:

The route-defining idea is the **reciprocal loop**, not merely that a future BEV exists.

Paper/code divergence remains important and must be tracked separately.

### 7.11 GraphWorld — future-aware relational world state without explicit rollout

Core problem statement:

Long-horizon planning requires interaction-aware future reasoning, but explicit future scene generation / rollout is expensive and prone to accumulation.

Core mechanism:

- construct ego-centric interaction graph over relevant agents;
- derive a compact latent world state encoding relational dynamics and safety-relevant semantics;
- future/target world-state information is used as supervision for learning dynamics;
- deployment planning is conditioned on the interaction-aware world state and mode-wise importance reweighting;
- no explicit multi-step rollout is required online.

Important interpretation:

GraphWorld demonstrates that world-model-assisted planning need not equal explicit future generation.

### 7.12 Discrete-WAM — unified representation/task formulation plus hierarchical policy generation

Core problem statement:

World prediction and policy generation are weakly aligned when they operate in separate representations and objectives.

Core mechanism:

- observations, future visual states, decisions, and actions share a discrete token space;
- one Transformer supports world modeling, world-policy modeling, and policy modeling through task-specific token editing / masks;
- world-policy training couples action prediction and action-conditioned world prediction;
- downstream policy generation predicts a high-level decision skeleton then refines/generates low-level action tokens.

Important interpretation:

The paper's main innovation spans three conceptual levels:

- representation alignment;
- world-policy training alignment;
- hierarchical policy construction.

Therefore “joint world-action generation” alone is an incomplete summary of its planning idea.

---

## 8. Important relationship structures currently emerging

These are **provisional relationship structures**, not final taxonomy classes.

### 8.1 Predictive-representation lineage

LAW <-> Drive-JEPA

Shared thesis: predictive/world learning can improve planning mainly by producing a better representation, without requiring expensive online world simulation.

Potential internal split:

- end-to-end action-conditioned auxiliary prediction (LAW);
- scalable pretraining then transfer (Drive-JEPA).

Question still open: distinct routes, or one route with different learning programs?

### 8.2 World-generation / planning coupling triangle

Epona <-> DriveLaW <-> Metis

- Epona: shared latent, parallel specialized generation heads;
- DriveLaW: generator latent directly conditions planner;
- Metis: separate experts and asymmetric information flow.

Potential key question:

> **What information path from world-generation computation is allowed to enter action generation, and at what stage?**

### 8.3 Action-consequence planning family — common thesis, uncertain internal route structure

World4Drive <-> WoTE <-> WorldDrive

Shared high-level thesis:

> action choice should depend on the future consequences associated with alternative behaviors.

But do not merge from the outer skeleton alone.

Possible distinctions:

- future plausibility / mode agreement;
- explicit recurrent rollout + reward evaluation;
- distilled online future surrogate + reward.

### 8.4 Progressive compilation of world reasoning

Possible spectrum:

- WoTE: full online world rollout;
- WorldDrive: distilled online future surrogate;
- DynFlowDrive: world model removed online; only world-derived scoring capability remains.

Candidate research question:

> **How much of the world-model reasoning process survives at deployment?**

### 8.5 Reciprocal refinement

SeerDrive-paper:

`plan -> world -> revised plan -> world -> ...`

Potentially independent mechanism family unless later evidence shows it is one instance of a broader search/optimization pattern.

### 8.6 Future-aware state without explicit imagination

GraphWorld:

> compress future-relevant interaction dynamics into an online world state rather than explicitly rollout future observations.

Potential relation to DriveLaW remains unresolved.

### 8.7 Representation/task unification paradigm

Discrete-WAM asks:

> Should world and action be represented and optimized in one common generative language?

This may cut across planning routes rather than define one route itself.

---

## 9. Key negative results: ideas currently rejected

### 9.1 Rejected: “same outer DAG => same route”

World4Drive, WoTE, and WorldDrive can share candidate/future/score/select while differing in indispensable mechanisms.

### 9.2 Rejected: “deployment DAG alone determines route”

Training-only world mechanisms can fundamentally change planning through representation shaping, distillation, asymmetric joint learning, or scorer supervision.

### 9.3 Rejected: “headline route must be a Cartesian product of independent axes”

R/W/E/L show dependency, overlap, and mixed conceptual levels.

### 9.4 Rejected: “paper-level capability list equals planning route”

A paper can support generation, counterfactual evaluation, and planning while using only one path for actual action commitment.

### 9.5 Rejected: “different resolver objective = different planning route”

Criterion semantics often changes what the scorer prefers without changing the world-to-decision bridge.

---

## 10. New working decomposition: route vs profiles vs paradigms

This is a **working decomposition only**.

### CoreRoute

What indispensable causal bridge carries world-model capability into final planning behavior?

### World/State Profile

What world-related object is used: current relational state, generative latent, endpoint future, horizon rollout, distilled future surrogate, etc.?

### Decision / Resolver Profile

How are actions proposed, revised, compared, edited, or committed?

### ResolverProfile

What does a resolver prefer: plausibility, behavior compatibility, safety/comfort/progress, utility, confidence, physical validity, etc.?

### Learning / Transfer Profile

How was world capability acquired and transmitted: auxiliary future prediction, predictive pretraining, representation inheritance, shared latent multi-task learning, teacher->surrogate distillation, world-derived scorer supervision, simulator-derived labels, reward-based post-training, etc.?

### Representation Paradigm

Continuous latent, BEV, relational graph state, unified discrete world-action tokens, generative-video latent, etc.

Important rule:

> A profile/paradigm should only become a headline route axis if removing or changing it consistently creates a different world-to-planning causal program across multiple target-domain papers.

---

## 11. Proposed first-principles comparison protocol for the canonical set

For each planning artifact, answer without using old ontology labels:

1. **Author's core dissatisfaction** — what does the paper claim previous systems fundamentally get wrong?
2. **World capability learned** — what predictive/dynamic/world knowledge is actually learned?
3. **Planning bridge** — through what exact mechanism does that knowledge alter the planner?
4. **Training path** — what causal path during training transfers world knowledge into deployed components?
5. **Deployment path** — what world-related computation/object remains online?
6. **Removed/bypassed computation** — what world-model components disappear at inference?
7. **Core-Bridge Deletion Test** — if the bridge is removed, does the main paper idea collapse?
8. **Closest predecessor / sibling** — which paper is it naturally compared with mechanistically?
9. **Non-equivalence reason** — why is it not merely the same route with another implementation?
10. **Potential abstraction level** — planning route, representation paradigm, learning-transfer program, or combination?

Only after these questions are answered should papers be clustered.

---

## 12. What “natural route emergence” should mean

A route candidate becomes credible when multiple pieces of evidence converge:

1. several papers share the same indispensable world-to-planning bridge;
2. implementation details vary while the bridge remains stable;
3. a clear counterexample changes the bridge and creates a qualitatively different mechanism;
4. the distinction survives implementation-invariance tests;
5. it explains why one paper was proposed in response to another;
6. it predicts meaningful relationships in held-out target-domain work;
7. deleting the distinction causes false collisions that erase a real scientific disagreement.

Conversely, a distinction should be demoted to a profile if swapping it does not alter the core world-to-planning program.

---

## 13. High-priority unresolved questions

### Q1. Is world-generation/planning coupling topology a genuine major route dimension?

Evidence: Epona vs DriveLaW vs Metis.

### Q2. Are World4Drive, WoTE, and WorldDrive one broad route with meaningful subtypes, or genuinely different routes?

Do not answer from the shared candidate/future/score/select skeleton.

### Q3. Does the WoTE -> WorldDrive -> DynFlowDrive sequence reveal a route family or a “degree of compilation” profile?

### Q4. Is SeerDrive's reciprocal loop a unique route or an instance of a broader online iterative search/optimization family?

### Q5. Should GraphWorld and DriveLaW share a higher-order family “world representation directly conditions planning”?

### Q6. Is predictive-representation learning (LAW / Drive-JEPA) itself a planning route or only a learning-transfer family?

### Q7. Where should unified world-action representation paradigms such as Discrete-WAM live?

---

## 14. Current meta-hypothesis

The field may not be best described by a flat ontology such as:

`R x W x E x L`

A more faithful structure may look like:

**A. Core world-to-planning bridge / route**  
What causal mechanism makes world modeling change the action?

**B. Deployment realization profile**  
What world-related object/computation remains online?

**C. Learning-transfer program**  
How was world capability learned and transferred?

**D. Decision/resolver profile**  
How are alternatives represented, compared, or committed?

**E. Representation paradigm**  
What shared representational language couples world and policy?

This is only a hypothesis. It must not be turned into a new ontology before canonical and broad-corpus regression.

---

## 15. Immediate next research step

Do **not** modify the existing ontology yet.

Next work should be:

1. reconstruct canonical planning artifacts using the protocol in Section 11;
2. build a paper relationship graph rather than a code table;
3. explicitly mark relations such as inherits idea from, tightens coupling of, decouples/bypasses, distills/compiles, changes one-way to reciprocal, replaces explicit future with latent state, or unifies representation/task space;
4. identify natural clusters from these relations;
5. only then propose provisional CoreRoute names;
6. attack those route candidates using D01, D01.3, and D02-W1 target-domain papers.

The goal is not to maximize the number of route classes.

The goal is:

> **minimum sufficient set of genuinely distinct world-model planning ideas that explains the field without erasing important scientific disagreements or promoting replaceable implementation choices into fake route differences.**

---

## 16. Living-log policy

This file is intentionally append-oriented.

Future high-value reasoning should be added with dated entries rather than silently rewriting history.

Each important update should record:

- observation;
- evidence/paper paths;
- prior assumption challenged;
- new hypothesis;
- confidence level;
- unresolved counterexample;
- whether the previous statement is retained, refined, or superseded.

Old reasoning should remain visible even when later rejected. Mark it `SUPERSEDED`, do not erase it.

This allows the repository to preserve not only conclusions, but the research path that produced them.

---

## 17. Snapshot verdict at creation time

Current confidence-weighted judgments:

- **High confidence:** E is more naturally a resolver semantic/profile than a universal headline route axis.
- **High confidence:** deployment DAG alone is insufficient for WAM route reconstruction.
- **High confidence:** shared outer skeleton is insufficient to establish route equivalence.
- **High confidence:** training/deployment lifecycle must be reconstructed together but kept explicitly separated.
- **High confidence:** Epona / DriveLaW / Metis expose a scientifically meaningful coupling disagreement that old R/W/E/L compresses poorly.
- **High confidence:** WoTE / WorldDrive / DynFlowDrive differ materially in how much world reasoning survives deployment.
- **Medium confidence:** the field is better represented as CoreRoute + conditional profiles/paradigms than a flat orthogonal axis system.
- **Medium confidence:** Core-Bridge Deletion Test is a useful route-legitimacy criterion.
- **Low/medium confidence:** the exact set and number of CoreRoutes. This remains deliberately unresolved.

**No new ontology is accepted by this document.**

The current task is field reconstruction, not taxonomy closure.

---

## 18. 2026-09-17 — New audit principle: preserve paper-family identity before splitting by visible mechanism differences

### Observation

Drive-JEPA creates a serious warning case for the current ontology strategy.

The paper presents Driving Video Pretraining, proposal generation / multimodal trajectory distillation, and momentum-aware trajectory selection as parts of one coherent framework. Its perception-free setting (PF) and proposal-based setting (PB) are not introduced as two unrelated scientific paradigms. They are better understood as different realizations / evaluation paths within the same broader Drive-JEPA research program: scalable predictive representation learning for planning, with the complete framework further addressing multimodal trajectory supervision and selection.

However, the old route projection can make:

- Drive-JEPA PF appear close to LAW / Epona-like direct-output systems;
- Drive-JEPA PB appear close to proposal-selection / candidate-resolver systems;

and therefore split PF and PB farther apart than the paper's own scientific framing, while potentially placing PF near papers whose central research question is quite different.

This is a **major audit alarm**.

It does not prove PF and PB must be one route. A paper can genuinely instantiate more than one mechanism route. But if an ontology repeatedly destroys strong paper-family coherence, we must ask whether the ontology is separating on secondary implementation structure instead of the scientific mechanism that the authors are actually advancing.

### Prior assumption challenged

Previous work implicitly assumed:

> If two modes have materially different commitment topology or runtime causal graphs, they may be assigned different route identities even when they come from one paper.

This remains useful for artifact bookkeeping, but it is insufficient for reconstructing **research routes**.

A research route is not necessarily identical to a runtime artifact topology.

### New distinction: artifact difference vs research-route difference

We need to separate two questions:

1. **Artifact question:** How does this exact mode/path produce its output? PF and PB can legitimately differ here.
2. **Research-route question:** What core scientific idea is the paper advancing about how world modeling should improve one-stage planning? PF and PB may still belong to the same higher-level research route if they are two instantiations of the same central thesis.

Therefore:

> Different artifacts inside one paper are evidence of mechanism variation, but they are **not automatically evidence of different research routes**.

This is an important correction to the project's earlier artifact-first classification practice.

### Drive-JEPA as a stress test

For Drive-JEPA, a plausible paper-level core thesis is:

> Learn planning-useful predictive representations efficiently at scale, then build a planner that can exploit those representations under realistic multimodal supervision.

PF tests whether the predictive representation alone transfers to a simple planner.

PB adds a richer planner, simulator-distilled multimodal proposals, and a selection mechanism.

The difference between PF and PB is real and should be preserved. But the difference may be best represented as **internal specialization within one larger route/family**, rather than as evidence that PF and PB belong to unrelated top-level routes.

This must be audited against the paper's ablations and framing before any conclusion is accepted.

### Why Epona is an important contrast

Epona's central thesis is different in kind:

> Learn a shared temporal world latent through autoregressive-diffusion world modeling so that world generation and trajectory generation are jointly supported by the same learned temporal structure, with planning-only inference available when video output is disabled.

Even if a Drive-JEPA PF deployment graph and an Epona planning graph both end in a direct trajectory, their **scientific bridge from world modeling to planning** is different.

Therefore an ontology that places Drive-JEPA PF and Epona close merely because both eventually produce a trajectory without an online candidate resolver is probably grouping on the wrong abstraction level.

This is stronger evidence that old R-like commitment topology cannot by itself define the main research route.

---

## 19. New candidate audit model: common ancestor -> major branch -> paper-specific innovation

A useful conceptual model was proposed:

- Paper 1: `a + b + e`
- Paper 2: `a + c + g`
- Paper 3: `a + c + f`
- Paper 4: `a + c + h`
- Paper 5: `a + b + j`

This should **not** be turned into a formula or imposed taxonomy.

Its value is methodological.

### Interpretation

`a` represents a common research foundation shared across the target domain, for example:

> world-model capability is deliberately connected to one-stage/end-to-end planning.

`b` and `c` represent possible **major scientific branches**: different answers to a central field-level question.

`e/f/g/h/j` represent more local innovations that distinguish individual papers or subfamilies without necessarily defining top-level routes.

The important idea is hierarchical rather than algebraic:

> Papers may share a deep common ancestor, split at one major scientific decision, then diverge again through paper-specific mechanisms.

This may fit the literature better than a flat Cartesian code.

### Critical warning

Do not assume every paper has exactly `a + one major branch + one unique point`.

Real papers may combine two major branches, introduce a bridge between existing branches, operate at a different abstraction level, contain multiple planning programs, mainly innovate representation rather than planning route, mainly compress or distill an existing route, or challenge the premise of an earlier branch.

Therefore this model is an **audit lens**, not a schema.

---

## 20. Route reconstruction should become relational and hierarchical, not coordinate-first

The new working question is no longer:

> Which values does this paper take on R, W, E, and L?

Instead ask, in order:

### Step 1 — Common scientific ancestor

What central WAM+one-stage premise does the paper share with its nearest relatives?

Candidate examples include predictive/world learning for planning representations, action-conditioned consequence reasoning, coupling world generation with action generation, or world-policy alignment in a shared representation/task space. These are hypotheses, not accepted families.

### Step 2 — Main scientific fork

What key question does the paper answer differently from its closest relatives?

Candidate examples:

- Should future/world computation remain online or be compiled into the planner?
- Should world generation and action planning be parallel, chained, reciprocal, or deliberately decoupled?
- Should candidate choice depend on explicit rollout, distilled future surrogate, or learned evaluation residue?
- Should world-policy alignment happen through auxiliary prediction, representation transfer, shared latent, or unified token modeling?

Again: these are candidate forks discovered from papers, not axes to impose.

### Step 3 — Paper-specific innovation

What is distinctive to this paper but may not justify a new route?

Examples include momentum penalty, reward decomposition, BEV vs latent realization, specific temporal objectives, trajectory vocabularies, distillation targets, and flow/diffusion implementation.

Some may later prove route-defining. They should start as local innovations, not headline classes.

### Step 4 — Core-Bridge Deletion Test

Delete the suspected major bridge.

Ask:

> Does the paper collapse into its nearest sibling / baseline, or does its main scientific identity remain intact?

If deleting feature X leaves the central thesis intact, X is unlikely to define a top-level route.

If deleting X turns the method into a different neighboring paper family or destroys the claimed contribution, X is a strong route candidate.

### Step 5 — Family-Coherence Test

Before accepting a split, ask:

> Does this split make papers/modes that the literature itself treats as one coherent research program look artificially unrelated?

Drive-JEPA PF/PB is the first explicit stress test.

A split can still be valid, but it must earn that split with strong mechanism evidence.

### Step 6 — Cross-Paper Contrast Test

Before accepting a merge, ask:

> Does this merge erase a scientific disagreement that the papers themselves explicitly motivate?

Examples include DriveLaW vs Epona-like parallel coupling, Metis vs tightly coupled world/action generation, and SeerDrive vs one-shot future-aware planning.

This protects against over-merging from superficial commonality.

---

## 21. Two complementary deletion tests are now required

The earlier Core-Bridge Deletion Test should be retained, but expanded into two levels.

### 21.1 Within-paper deletion test

For paper P, remove mechanism X.

Ask:

> Does P lose the central contribution claimed by its authors?

This identifies what is indispensable **inside the paper**.

### 21.2 Between-paper collapse test

For paper P, remove mechanism X.

Ask:

> Which neighboring paper / baseline does P become most similar to after removal?

This identifies whether X actually defines a **branch point in the literature**.

Examples:

- Removing reciprocal feedback from SeerDrive may collapse it toward one-shot future-aware planning.
- Removing a particular reward term from WoTE leaves explicit candidate-conditioned world rollout + reward selection intact, so that reward term is not branch-defining.
- Removing proposal-based PB components from Drive-JEPA may leave the same predictive-pretraining thesis tested in PF, suggesting PB could be a specialization of the Drive-JEPA family rather than an unrelated top-level route.

This between-paper collapse test is potentially more powerful than simple feature deletion because it reconstructs **where the paper sits in the research genealogy**.

---

## 22. New negative rule: do not reward an ontology for splitting things

Previous ontology work sometimes treated collision avoidance as inherently good: if two papers can be separated by another axis, the ontology appears to gain explanatory power.

This is unsafe.

A taxonomy can be wrong by **over-separating** just as easily as by over-merging.

Therefore every proposed split now needs to answer:

1. What scientifically important disagreement does the split preserve?
2. Would the papers' own problem statements recognize this disagreement?
3. Does the Core-Bridge Deletion Test support it?
4. Does the between-paper collapse test support it?
5. Does the split survive implementation substitution?
6. Does it preserve reasonable family coherence?

If not, the distinction should remain a profile/local innovation rather than a route boundary.

---

## 23. Current audit stance after the Drive-JEPA warning

High-confidence update:

> **The old ontology should no longer be used as the primary lens for discovering routes.**

It remains useful as a structured record of mechanism facts and as a source of hypotheses, but not as the discovery engine.

High-confidence update:

> **Runtime commitment topology is not sufficient to determine research-route identity.**

Drive-JEPA PF/PB provides a strong stress case; Epona provides an important contrast.

Medium/high-confidence update:

> **Research routes are likely hierarchical and genealogical: shared thesis -> major scientific fork -> local realization.**

But the exact hierarchy is deliberately unresolved.

High-confidence update:

> **Paper-family coherence is now an explicit audit signal, not a cosmetic consideration.**

Low-confidence / unresolved:

- whether Drive-JEPA PF and PB should ultimately share one CoreRoute;
- what the actual major branch containing Drive-JEPA should be called;
- whether the `a/b/c/...` intuition will survive broader corpus pressure;
- how many hierarchy levels the field genuinely needs.

No ontology changes follow automatically from this section.

The immediate task remains reconstruction of paper relationships and branch points, not code assignment.
