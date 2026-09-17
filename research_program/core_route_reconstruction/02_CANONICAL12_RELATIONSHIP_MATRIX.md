# Canonical 12 Relationship Matrix

Status: **AUDIT AID — NOT TAXONOMY**  
Companion to: `01_CANONICAL12_RESEARCH_LINEAGE_AUDIT.md`

This file records the strongest currently supported paper-to-paper relations. It intentionally avoids route codes.

## 1. Relation vocabulary

- `EXTENDS`: keeps a predecessor thesis and adds a substantive mechanism.
- `FORKS`: answers a shared scientific question differently.
- `CRITIQUES`: paper explicitly identifies the other family/mechanism as insufficient.
- `TIGHTENS`: increases direct causal coupling between world modeling and planning.
- `DECOUPLES`: deliberately reduces/directs coupling while retaining shared learning.
- `DISTILLS`: retains knowledge from a heavier world process through a surrogate.
- `COMPILES`: world-model reasoning affects training targets/parameters but disappears online.
- `RECIPROCALIZES`: turns a one-way world->planning relation into iterative mutual feedback.
- `REPLACES-ROLLOUT`: replaces explicit future rollout with a compact future-aware state.
- `SYNTHESIZES`: combines multiple previously separate lineages.
- `ORTHOGONAL-COMPONENT`: important paper component that belongs to another mechanism lineage and should not automatically split the paper family.

## 2. Strong pairwise relations

| Source / ancestor | Target | Relation | Core inherited thesis | Main fork introduced by target | Deletion / collapse statement | Confidence |
|---|---|---|---|---|---|---|
| LAW | World4Drive | EXTENDS + FORKS | predictive latent world learning can improve planning without manual perception labels | single future latent -> physically enriched multimodal intention-conditioned futures + selector | remove multimodal intention/future selection and World4Drive moves substantially toward LAW-style latent self-supervision | High |
| LAW | Drive-JEPA predictive component | REFORMULATES + SCALES | predictive latent learning can produce planning-useful representation | in-task auxiliary action-conditioned prediction -> large-scale JEPA pretraining and transfer | remove JEPA pretraining and Drive-JEPA loses its WAM representation contribution, but its multimodal planner remains | High |
| Epona-like parallel gen-plan | DriveLaW | CRITIQUES + TIGHTENS | world generation should support planning through shared learned dynamics | parallel/shared latent outputs -> generator internal latent directly conditions planner | remove video-latent->Action-DiT chain and DriveLaW collapses toward parallel/shared representation designs | Very high |
| tightly coupled/joint WAMs | Metis | CRITIQUES + DECOUPLES | future prediction and action learning can be jointly trained | tight bidirectional coupling -> separate experts + asymmetric visibility, video bypass online | remove asymmetric decoupling and Metis collapses toward the tightly coupled WAM family it criticizes | Very high |
| WoTE-like candidate consequence evaluation | WorldDrive FAR | DISTILLS | candidate choice should depend on candidate-specific future consequences | full/expensive future modeling -> distilled lightweight online future surrogate | remove FAR and WorldDrive retains representation inheritance but loses online candidate-specific foresight | High |
| WoTE / static latent candidate evaluation | DynFlowDrive | FORKS + COMPILES | world dynamics can improve trajectory evaluation | online/static future evaluation -> flow-dynamics-derived training selection; WM removed online | remove world-derived stability/selection supervision and deployment becomes ordinary proposal+score planning | High |
| one-shot future-aware planning | SeerDrive | RECIPROCALIZES | predicted future scene should inform planning | one-way future->plan -> iterative world<->plan mutual refinement | remove reciprocal loop and SeerDrive collapses toward one-shot future-aware planning | Very high |
| explicit imagination / rollout WM family | GraphWorld | REPLACES-ROLLOUT | long-horizon planning needs future-aware dynamics | explicit future generation/rollout -> compact relational world state conditioning | remove ECIG/WSCP world-state bridge and system collapses toward conventional interaction-aware multimodal planning | High |

## 3. Multi-parent / synthesis nodes

| Paper | Parent lineage 1 | Parent lineage 2 | Additional component | Why strict tree fails |
|---|---|---|---|---|
| WorldDrive | generative world-model representation learning | candidate-consequence evaluation | teacher->surrogate distillation | representation inheritance and online future-aware ranking are independently meaningful bridges |
| Drive-JEPA | predictive representation learning (LAW-adjacent) | multimodal end-to-end planning supervision | simulator pseudo-teachers + momentum selection | PF and PB expose different subsets of one compound paper program |
| Discrete-WAM | world/action representation alignment | world-policy joint training | hierarchical decision-conditioned action editing | representation, learning program and policy construction are three conceptual levels, not one route edge |
| World4Drive | LAW-style latent self-supervision ancestry | candidate/intention consequence selection | physical semantic/spatial prior enrichment | it is simultaneously a LAW descendant and a move toward multimodal consequence reasoning |

## 4. Family-coherence stress tests

| Stress case | Superficial split/merge | Current audit judgment |
|---|---|---|
| Drive-JEPA PF vs PB | direct output vs proposal+resolver | **Do not promote to distant research routes.** Artifact distinction is real, but both belong to one paper program unless stronger evidence proves two separate WAM theses. |
| Drive-JEPA PF vs Epona planning | both may deploy without online future rollout | **Do not treat as close lineage from this fact.** JEPA predictive pretraining and Epona shared generative temporal modeling solve different scientific problems. |
| World4Drive vs WoTE | both can be drawn candidate->future->score | **Outer DAG is insufficient.** World4Drive emphasizes intention-conditioned future plausibility/mode selection; WoTE explicitly evaluates action consequences through recurrent future rollout and rewards. |
| WoTE vs WorldDrive | both use candidate-specific future information | **Likely close lineage but not identical.** WorldDrive additionally unifies representation and distills heavy foresight into an online surrogate. |
| WorldDrive vs DynFlowDrive | both compress world-model reasoning | **Different residual online mechanism.** WorldDrive retains candidate-specific future surrogate; DynFlowDrive compiles world reasoning into score supervision and drops WM online. |
| DriveLaW vs GraphWorld | both use world-related latent to condition planner | **Do not merge from interface alone.** Generator-internal representation chaining and relational long-horizon world-state reasoning have different scientific claims. |
| Epona vs DriveLaW vs Metis | all combine world/video and action learning | **Strong genuine fork candidate.** They explicitly disagree on correct coupling structure: parallel/shared, chained, or deliberately asymmetric/decoupled. |

## 5. Per-paper nearest relatives after genealogy audit

| Paper | Nearest current relatives | Why | Main caution |
|---|---|---|---|
| LAW | Drive-JEPA(A), World4Drive | predictive latent learning ancestry | LAW->Drive-JEPA and LAW->World4Drive fork in different directions |
| Epona | DriveLaW, Metis | world-generation/action coupling debate | do not group with JEPA merely because video branch can be disabled online |
| DriveLaW | Epona, Metis | explicit answer to coupling question | generator latent itself is central, not generic latent-state conditioning |
| World4Drive | LAW, WoTE, WorldDrive | LAW descendant plus multimodal future selection | has two ancestries; generic candidate-score sketch is too coarse |
| WorldDrive | WoTE, generative WM lineage, World4Drive | representation inheritance + candidate future surrogate | synthesis node; one-label genealogy is misleading |
| WoTE | WorldDrive, DynFlowDrive | world dynamics for candidate evaluation | distinguish full online rollout from surrogate/compiled evaluation |
| SeerDrive | one-shot future-aware planners, WoTE/World4Drive neighborhood | turns one-way future assistance into reciprocal loop | paper/code divergence must not silently rewrite research lineage |
| Drive-JEPA | LAW, multimodal planner/distillation literature | predictive representation + orthogonal multimodal planning component | PF/PB split must not destroy family identity |
| Metis | Epona/DriveLaW/tightly coupled WAMs | explicit coupling/efficiency critique | deployment bypass alone is not the full mechanism |
| DynFlowDrive | WoTE, WorldDrive | consequence evaluation with world reasoning progressively compiled | flow architecture itself may be lower-level than compilation role |
| Discrete-WAM | joint/generative WAM lineage | unified world/action token language and training | old joint-output label captures only part of paper identity |
| GraphWorld | latent-world planning neighborhood | compact relational future-aware world state | unclear whether separate route or state-realization branch |

## 6. Current high-value unresolved branch points

1. **Predictive representation:** Is LAW/Drive-JEPA a planning route or a learning-transfer lineage that can attach to multiple planning routes?
2. **Coupling topology:** Does Epona/DriveLaW/Metis generalize into a stable field-level branch family beyond these papers?
3. **Consequence reasoning:** Are World4Drive/WoTE/WorldDrive/DynFlowDrive one broad family with subbranches, or several top-level routes?
4. **Compilation degree:** Is `full online world reasoning -> online surrogate -> compiled scorer` a route distinction or a deployment-realization profile?
5. **Reciprocity/search:** Is SeerDrive a unique reciprocal family or one instance of a broader iterative search/optimization family?
6. **Relational world state:** Is GraphWorld a genuinely different route from future rollout, or a compact realization of a broader future-aware-state route?
7. **Unified token paradigm:** Does Discrete-WAM define a planning route, or a representation/training substrate that can host several routes?

## 7. Promotion rule for the next phase

A relation above may become a candidate CoreRoute split only if broader target-domain evidence shows that:

- multiple independent papers instantiate the same fork;
- changing the fork changes the indispensable world->planning bridge;
- implementation substitutions do not erase the distinction;
- the split explains paper-to-paper scientific disagreement;
- the split does not destroy strong family coherence without evidence;
- held-out papers can be placed naturally without inventing new ad hoc coordinates.

Until then, this matrix is a **genealogy audit artifact**, not a taxonomy.