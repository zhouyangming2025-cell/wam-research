# Canonical 12 Research-Lineage Audit

Status: **FIRST-PRINCIPLES AUDIT — NOT AN ONTOLOGY SPEC**  
Branch: `research/core-route-reconstruction`  
Baseline ancestry: `codex/domain-map-d02-w1e-rerun@368c9a848e241bfb7bf2e2d61242269d5e438af6`  
Scope: canonical 12 WAM + one-stage / end-to-end autonomous-driving papers  
Purpose: reconstruct paper relationships before proposing any new route taxonomy.

---

## 0. Why this audit exists

The project previously represented mechanisms with flat signatures such as `R–W–E ⊕ L`. That work remains useful as an evidence ledger, but it risks turning observable differences into artificial route differences.

The current research target is different:

> **Which papers are genuinely pursuing the same world-model-planning idea, where do they make a scientifically meaningful fork, and which differences are only implementation, operating mode, or paper-specific innovations?**

This audit therefore does **not** ask “which code does this paper receive?” It asks:

1. What problem does the paper inherit?
2. Which prior approach does it regard as insufficient?
3. What world-to-planning bridge does it change?
4. If that bridge is removed, what does the method collapse into?
5. Which papers remain its nearest scientific relatives after architecture details are ignored?

The goal is a research genealogy, not a code table.

---

## 1. Unit-of-analysis correction

### 1.1 Paper lineage is not the same as artifact topology

A paper can expose multiple operating modes or evaluation settings. Those modes are useful for causal auditing, but they do not automatically define separate research lineages.

The strongest current warning is Drive-JEPA.

The previous artifact map separates:

- Drive-JEPA PF: predictive representation -> direct trajectory decoder;
- Drive-JEPA PB: predictive representation + proposal-centric planner + simulator distillation + candidate selection.

This split is mechanically real. However, the paper presents both inside one coherent program: scalable planning-aligned predictive pretraining plus improved multimodal planning supervision. Treating PF as one top-level route and PB as a distant route can destroy the paper's own research identity.

Therefore:

> **Artifact split remains an evidence tool; paper-lineage split requires an additional scientific-identity test.**

### 1.2 A paper may have more than one parent lineage

The genealogy should be a directed idea graph, not necessarily a strict tree.

Examples:

- WorldDrive combines a generative-world-model representation lineage with a candidate-consequence evaluation lineage.
- Drive-JEPA combines predictive representation learning with an orthogonal multimodal planner/distillation program.
- Discrete-WAM combines representation alignment, world-policy joint training, and hierarchical policy generation.

Forcing each paper to have exactly one parent would recreate the same failure as forcing every paper into one Cartesian signature.

### 1.3 Not every major innovation is a planning-route innovation

A paper can contribute at different conceptual levels:

- world/planning bridge;
- representation paradigm;
- learning-transfer mechanism;
- decision architecture;
- solver/refinement mechanism;
- paper-specific engineering.

Only the first of these is automatically a candidate for a top-level WAM planning route. The others can become route-defining only after cross-paper evidence shows that changing them consistently changes the scientific mechanism.

---

## 2. Audit tests

### 2.1 Author-Framing Test

What does the paper itself claim previous work gets wrong?

Author framing is not accepted uncritically, but it is evidence about the intended scientific fork. A taxonomy that makes two papers close even when one explicitly argues that the other's mechanism is insufficient requires strong justification.

### 2.2 Core-Bridge Deletion Test

Remove the proposed world-to-planning bridge.

Ask:

> Does the WAM-specific contribution collapse into an ordinary planner, an earlier WAM family, or merely lose a minor enhancement?

The stronger the collapse, the more likely that bridge is route-defining.

### 2.3 Between-Paper Collapse Test

A stronger form of the deletion test:

> After deleting the distinguishing mechanism, which other paper/family does this method become closest to?

Examples to test:

- DriveLaW without `video-generator latent -> Action DiT` should move toward parallel/shared-latent generation-planning rather than remain a distinct chained paradigm.
- SeerDrive without reciprocal world↔planning iteration should move toward one-shot future-aware planning.
- DynFlowDrive without world-derived stability supervision should move toward an ordinary multimodal proposal/scoring planner.

### 2.4 Family-Coherence Test

If a paper's own modes are intended as parts of one coherent method family, a route system should not scatter them far apart merely because downstream output topology differs.

This test does **not** prohibit genuine multi-route papers. It creates a burden of proof for strong separation.

### 2.5 Common-Ancestor / Main-Fork / Unique-Residue Test

The user's useful `a + b/c + unique` intuition is retained only as an audit question, not as a formula.

For a set of related papers, ask:

- **Common ancestor:** what scientific thesis do they genuinely share?
- **Main fork:** what different answer do they give to the same central question?
- **Unique residue:** what remains paper-specific after the shared thesis and main fork are accounted for?

A paper need not have exactly one main fork, and multiple parent lineages are allowed.

---

## 3. Paper-level lineage reconstruction

## 3.1 LAW — action-aware predictive self-supervision for planning representation

Primary source: `papers/raw_md/P0048_LAW/P0048_LAW.raw.md`

### Inherited problem

LAW starts from a representation-learning question: end-to-end planners receive raw sensor data, but how should they learn stronger scene representations without expensive perception annotation?

It explicitly argues that static self-supervision underuses driving video and that future prediction must account for ego action because ego motion changes the future.

### Core bridge

`current visual latent + planner-predicted trajectory -> future latent prediction -> future-frame latent supervision -> improved representation/planner`

The world model is primarily a **learning bridge**. Its value is not online candidate search; its future-prediction loss shapes the representation and action path during training.

### Deletion/collapse test

Remove the action-conditioned future-latent task and LAW collapses to its underlying end-to-end planner with trajectory/perception supervision.

Therefore the WAM-specific identity is strongly tied to predictive self-supervision.

### Nearest lineage relations

- Strong conceptual ancestor/sibling for Drive-JEPA's predictive-representation program.
- Explicit predecessor challenged by World4Drive, which argues LAW's single-modal latent lacks rich physical/spatial-semantic structure and multimodal intention modeling.
- Mechanistically distinct from Epona despite both being able to deploy without explicit online future generation.

### Current lineage judgment

**High-confidence lineage node:** predictive world learning used to shape planning representation.

Whether this becomes a top-level route or a learning-transfer family remains unresolved.

---

## 3.2 Epona — shared temporal world model with parallel modular world/action generation

Primary source: `papers/raw_md/P0001_Epona/P0001_Epona.raw.md`

### Inherited problem

Epona starts from generative-world-model limitations:

- video diffusion has strong fidelity but weak flexible long-horizon autoregression;
- GPT-style autoregression has temporal flexibility but tokenization harms continuous visual/planning precision;
- existing world models do not integrate long-horizon world generation and accurate trajectory planning well.

### Core bridge

Epona factorizes temporal dynamics from modality-specific generation:

- causal temporal transformer models compressed temporal dynamics;
- one diffusion branch generates future video;
- another diffusion branch generates trajectory;
- both are conditioned on the same temporal latent;
- planning can run while video output generation is deactivated.

The key scientific idea is **shared temporal world structure with parallel specialized generation**.

### Deletion/collapse test

If the shared temporal world model / modular multimodal generation is removed, Epona separates into a video generator plus an ordinary trajectory planner. The “world model itself serves as real-time planner” thesis collapses.

### Nearest lineage relations

- Direct conceptual predecessor criticized by DriveLaW: DriveLaW argues Epona-like parallel video/planning outputs do not directly use generator internal latents as planning state.
- Broad family target criticized by Metis: Metis argues tightly coupled joint video/action WAMs can create representation mismatch and inference cost.
- Different scientific starting point from LAW/Drive-JEPA: Epona is generative world-action modeling, not primarily predictive representation pretraining.

### Current lineage judgment

**High-confidence node:** world generation and planning share temporal world structure but retain parallel output branches.

---

## 3.3 DriveLaW — from parallel unification to chained generator-latent planning

Primary source: `papers/raw_md/P0009_DriveLaW/P0009_DriveLaW.raw.md`

### Inherited problem

DriveLaW explicitly surveys three roles for world models in planning and argues that even “unified” world models such as Epona still leave generation and planning insufficiently coupled.

Its specific criticism is unusually informative for genealogy:

> Epona-like approaches co-generate video and trajectory but do not directly use the video generator's internal representation as the planning state.

### Core bridge

`video generator mid-level latent -> Action DiT -> trajectory`

This is not merely shared training. The generator's internal latent becomes an online conditioning state for the planner.

### Deletion/collapse test

Remove this chained latent path and DriveLaW loses the mechanism it claims differentiates itself from parallel unified models. It moves back toward:

- shared-pretraining/representation transfer, or
- Epona-like parallel generation/planning.

### Main scientific fork relative to Epona

Shared ancestor thesis:

> world-generation learning should help planning.

Main fork:

- Epona: shared temporal latent, parallel specialized generators;
- DriveLaW: planner should directly consume the generator's internal latent.

This is a strong candidate for a genuine field-level fork because the paper explicitly motivates itself by this distinction.

### Current lineage judgment

**High confidence:** DriveLaW is a descendant/critique of parallel unified gen-plan systems and tightens the coupling into a chained representation path.

---

## 3.4 World4Drive — LAW lineage extended into multimodal intention-conditioned latent futures and selection

Primary source: `papers/raw_md/P0046_World4Drive/P0046_World4Drive.raw.md`

### Inherited problem

World4Drive explicitly positions LAW as a predecessor:

- LAW reduces annotation dependence through latent future self-supervision;
- but its single-modal image latent is argued to lack rich spatial-semantic understanding and multimodal driving intention structure.

### Core bridge

World4Drive adds two things to the LAW-style latent-world premise:

1. a physically enriched world latent with spatial/semantic/temporal priors;
2. multiple driving intentions, each producing an intention-specific future latent and trajectory.

A selector is trained from factual-future latent agreement and later ranks trajectory/intention modes at inference.

### Deletion/collapse tests

- Remove multimodal intention-conditioned future branches and selector: the method moves substantially toward LAW-style single-future latent self-supervision plus a planner.
- Remove physical/spatial-semantic latent enrichment but retain multimodal selector: the paper loses another central claimed contribution but still retains the action-consequence selection idea.

This indicates World4Drive is **compound**: it is both a richer latent-representation descendant of LAW and an early candidate-future selection mechanism.

### Nearest lineage relations

- Strong explicit edge from LAW.
- Shares “alternative action/intention -> different future -> choose” thesis with WoTE and WorldDrive, but the future is used primarily for mode plausibility/agreement rather than explicit recurrent reward rollout.

### Current lineage judgment

**High confidence:** descendant of LAW with a major fork toward multimodal intention-conditioned future selection.

Do not reduce it to a generic `candidate -> future -> score -> select` family without preserving this ancestry.

---

## 3.5 WoTE — explicit online model-based trajectory evaluation

Primary source: `papers/raw_md/P0045_WoTE/P0045_WoTE.raw.md`

### Inherited problem

WoTE starts from trajectory evaluation, not representation learning.

Its thesis is explicit:

> Evaluating a candidate only from the current state is inadequate because the quality of an action depends on the future state induced by that action.

It frames the problem using model-based policy evaluation ideas.

### Core bridge

`trajectory candidate -> state-action pair -> recurrent future BEV rollout -> reward model -> final trajectory`

Unlike LAW, world prediction is not merely a training regularizer. Unlike World4Drive, the central framing is not “which intention mode matches the future?” It is **evaluate a candidate by explicitly predicting its consequences**.

### Deletion/collapse test

Remove candidate-conditioned world rollout and the reward model becomes a current-state/model-free scorer. WoTE collapses toward a conventional proposal-selection planner.

This is a very strong deletion result: the core paper idea disappears.

### Nearest lineage relations

- Natural sibling/ancestor for WorldDrive's candidate re-scoring component; WorldDrive explicitly adopts the scoring paradigm of the relevant prior work and then adds a distilled future surrogate.
- Direct comparator for DynFlowDrive, which keeps world-based evaluation during training but removes world-model computation from inference.
- One-shot consequence-evaluation baseline from which SeerDrive conceptually departs by adding reciprocal world↔planning interaction.

### Current lineage judgment

**High confidence:** explicit online model-based candidate consequence evaluation is a genuine scientific program.

Whether World4Drive and WorldDrive are the same route or neighboring sublineages remains open.

---

## 3.6 WorldDrive — synthesis of generative representation unification and distilled future-aware candidate evaluation

Primary source: `papers/raw_md/P0042_WorldDrive/P0042_WorldDrive.raw.md`

### Inherited problem

WorldDrive identifies a different systemic gap:

> world models learn visual representation for scene generation while planners learn motion representation separately; this representation/task disconnect prevents the planner from fully inheriting world-model dynamics.

It also recognizes that explicit candidate-wise world generation is too expensive for real-time planning.

### Core bridges

WorldDrive contains **two distinct world-to-planning bridges**:

1. **Representation inheritance**
   - trajectory-aware generative world model learns vision + motion representations;
   - visual and trajectory encoders are transferred/frozen into the downstream planner.

2. **Distilled online foresight**
   - heavy candidate-conditioned future generation is available during training;
   - Future-aware Rewarder distills candidate-specific future latents;
   - inference keeps a lightweight candidate-conditioned future surrogate and rewarder rather than full diffusion generation.

### Deletion/collapse tests

This paper is especially informative because different deletions produce different ancestors:

- Remove FAR but keep representation inheritance -> WorldDrive becomes much closer to predictive/generative representation-transfer approaches.
- Remove representation inheritance but keep candidate-future rewarder -> the remaining planner becomes much closer to WoTE-like model-based candidate evaluation, though with a learned surrogate rather than recurrent BEV rollout.
- Remove both -> ordinary multimodal proposal planner.

Therefore WorldDrive should not be forced into a single-parent lineage.

### Nearest lineage relations

- Generative representation lineage: Epona/other generative WMs provide the broader “scene generation should support planning” context.
- Latent planning lineage: LAW/World4Drive show latent world knowledge can support planning without full pixel rollout.
- Candidate evaluation lineage: WoTE provides a clear nearby scoring paradigm.

### Current lineage judgment

**High confidence:** WorldDrive is a synthesis/bridge paper. A strict tree will misrepresent it.

---

## 3.7 SeerDrive — from one-shot future assistance to reciprocal world-planning refinement

Primary source: `papers/raw_md/P0061_SeerDrive/P0061_SeerDrive.raw.md`

### Inherited problem

SeerDrive explicitly attacks the **one-shot paradigm**:

- current observations directly determine a several-second trajectory;
- future scene evolution is underused;
- ego future actions and scene evolution are mutually dependent.

The paper also distinguishes prior world-assisted planning that either adds world-model supervision or uses world modeling to select among candidates.

### Core bridge

`world prediction -> planning -> updated ego/action state -> revised world prediction -> revised planning -> ...`

The scientific fork is the bidirectional/iterative relationship, not merely the presence of future BEV.

### Deletion/collapse test

Remove iterative mutual feedback while retaining future BEV conditioning and the paper collapses toward a one-shot future-aware planner.

That is a strong route-defining deletion.

### Nearest lineage relations

- Conceptually downstream from one-shot future-aware planning/evaluation families such as World4Drive/WoTE-like methods, but not reducible to a candidate-scoring variant.
- Paper/code divergence must remain separate: released code may implement a simpler candidate evaluation/refinement topology, but research-lineage audit should preserve the paper's claimed scientific fork and note implementation divergence as evidence pressure.

### Current lineage judgment

**High confidence:** reciprocal world↔planning refinement is a distinct claimed paradigm within the canonical set.

Whether it later merges into a broader search/optimization family requires larger corpus evidence.

---

## 3.8 Drive-JEPA — one paper family with two orthogonal research components, not two distant lineages

Primary source: `papers/raw_md/P0049_DriveJEPA/P0049_DriveJEPA.raw.md`

### Inherited problems

Drive-JEPA identifies two bottlenecks:

1. world-model pretraining has not scaled effectively for planning; pixel generation is expensive and latent predictive methods have not clearly benefited from scale;
2. one expert trajectory per scene creates a multimodal supervision bottleneck.

The paper explicitly presents these as two complementary problems.

### Core program

**Component A — predictive representation learning**

`large-scale driving video -> V-JEPA latent prediction -> planning-aligned encoder -> downstream planner`

**Component B — multimodal planning distillation**

`human + simulator pseudo-teacher trajectories -> proposal-centric planner -> learned safety/rule/comfort scoring + momentum selection`

### PF/PB family-coherence audit

The previous artifact map makes PF and PB look far apart:

- PF: direct policy, no runtime candidate resolver;
- PB: candidate proposals + scorer/resolver.

Mechanically this is true. Genealogically, however, it is dangerous to treat these as separate top-level research families.

The paper uses the simple perception-free decoder to isolate and demonstrate the value of predictive pretraining. The full proposal-centric planner then adds multimodal distillation and momentum-aware selection. Both are presented as manifestations of one Drive-JEPA research program, not competing world-model paradigms.

### Core-bridge deletion results

This paper produces an important negative result for our methodology:

- Remove V-JEPA pretraining: the PB planner still exists as a multimodal proposal/distillation system, though the WAM-specific contribution is weakened.
- Remove multimodal distillation/selection: the predictive representation program still exists and is demonstrated by the simple PF planner.

Therefore there is **no single bridge whose deletion destroys the entire paper**.

The correct interpretation is not “the deletion test failed.” It is:

> Drive-JEPA is a compound paper with at least two partly orthogonal contribution lineages.

### Nearest lineage relations

- Predictive world-representation lineage: LAW is the closest canonical relative; Drive-JEPA changes the learning regime from end-to-end action-conditioned auxiliary prediction toward scalable JEPA-style video pretraining/transfer.
- Epona is deliberately a different contrast class in the paper: pixel-generative world-model pretraining is treated as computationally heavy and potentially focused on planning-irrelevant visual detail.
- PB's proposal/distillation mechanisms are closer to multimodal end-to-end planning literature than to a distinct online-world-reasoning lineage.

### Current lineage judgment

**Very high confidence:** PF/PB should not be used as evidence that Drive-JEPA belongs to two distant WAM research routes. Artifact topology and paper genealogy are different abstraction levels.

This is one of the strongest falsification cases against the old flat route map.

---

## 3.9 Metis — deliberate decoupling of world generation and action inference

Primary source: `papers/raw_md/P0062_Metis/P0062_Metis.raw.md`

### Inherited problem

Metis starts from recent WAMs that jointly model future observations and actions. It argues they suffer from:

1. inference latency if future observations must be explicitly generated;
2. representational mismatch/interference when high-dimensional video and low-dimensional action are tightly coupled.

### Core bridge

Metis uses separate video and action experts with a shared latent interaction and an asymmetric attention mask:

- future video may attend to future action;
- action may not depend on future video tokens;
- joint training transfers dynamics knowledge;
- explicit video generation is bypassed at deployment.

### Deletion/collapse test

Remove the asymmetric visibility/decoupled expert design and Metis collapses toward the tightly coupled joint video-action WAM family it criticizes.

This is a strong collapse relation.

### Relation to Epona / DriveLaW

These three papers expose a coherent scientific disagreement:

- Epona: shared temporal world model + parallel modality generators;
- DriveLaW: make coupling tighter by chaining video-generator latent into planner;
- Metis: make coupling deliberately asymmetric/looser to avoid interference and latency.

This is not a minor architecture variation. Each paper motivates its contribution using a different answer to the same world-generation/planning coupling question.

### Current lineage judgment

**High confidence:** coupling direction/strength is a real genealogy fork in this subset.

Whether it becomes a top-level route dimension remains to be tested outside the canonical set.

---

## 3.10 DynFlowDrive — world dynamics as a training-time evaluator/teacher, compiled into the planner

Primary source: `papers/raw_md/P0063_DynFlowDrive/P0063_DynFlowDrive.raw.md`

### Inherited problem

DynFlowDrive explicitly criticizes static one-step latent regression:

> endpoint prediction can miss the process by which a trajectory induces scene evolution; trajectories with similar endpoints can have very different dynamic safety/stability.

It directly positions itself against prior latent world models such as LAW/World4Drive and compares strongly with WoTE.

### Core bridge

During training:

`candidate trajectory -> flow-based latent world dynamics -> reconstruction/stability criteria -> select/label preferred mode -> supervise planner score head`

During inference:

`candidate proposals -> learned score head -> final choice`

The paper explicitly states the flow world model is training-only and adds no inference burden.

### Deletion/collapse test

Remove flow-based world evaluation/stability supervision and the deployment system becomes an ordinary multimodal proposal-and-score planner.

The WAM contribution is therefore **compiled into the scorer** rather than retained as online world reasoning.

### Nearest lineage relations

- Mechanistic cousin of WoTE: both ask whether world dynamics can improve candidate evaluation.
- Main fork from WoTE: WoTE retains explicit online future rollout/reward evaluation; DynFlowDrive uses world dynamics to create training supervision and removes the world model at inference.
- Related to WorldDrive on “compress/remove expensive world reasoning,” but WorldDrive retains an online candidate-conditioned future surrogate whereas DynFlowDrive does not.

### Current lineage judgment

**High confidence:** training-time world evaluator -> deployed scorer is a distinct transfer mechanism from full online model-based evaluation.

Whether it is a separate route or a “degree of compilation” subtype remains open.

---

## 3.11 Discrete-WAM — unified representation/task language rather than a single simple planning route

Primary source: `papers/raw_md/P0064_Discrete-WAM/P0064_Discrete-WAM.raw.md`

### Inherited problem

Discrete-WAM argues that world prediction and policy generation are weakly aligned when they use separate representations/objectives. It also argues that driving policy itself has hierarchical structure.

### Core program

Three levels are deliberately unified:

1. **representation:** visual states, actions, decisions share a discrete token interface;
2. **training:** world modeling, joint world-policy modeling, and policy modeling share one Transformer/task framework;
3. **planning:** high-level decision skeleton -> parallel low-level action-token editing/refinement.

### Deletion/collapse tests

- Remove shared discrete world-action representation: the central “unified physical-AI language” thesis collapses.
- Remove world-policy joint task but keep hierarchical action policy: a substantial planner remains, but world-policy alignment claim collapses.
- Remove hierarchical decision token but retain unified world/action training: WAM remains, but the downstream planning construction changes.

This again shows one paper contains several important mechanisms at different abstraction levels.

### Nearest lineage relations

- Broadly related to generative/joint world-action works such as Epona, but its main claimed novelty is not simply “joint output.”
- More accurately viewed as a representation/training unification paradigm that can support several task modes.

### Current lineage judgment

**High confidence:** old `RJ/W5` compression was too narrow to represent the paper's scientific identity.

Do not infer a top-level planning route directly from its joint world-action training mode.

---

## 3.12 GraphWorld — replace explicit imagination with relational future-aware world state for long-horizon planning

Primary source: `papers/raw_md/P0065_GraphWorld/P0065_GraphWorld.raw.md`

### Inherited problem

GraphWorld starts from long-horizon planning:

- ordinary E2E planners are short-sighted;
- world models can support imagination but explicit diffusion/rollout is expensive;
- existing latent world-model planning still leaves long-horizon interaction reasoning underdeveloped.

### Core bridge

`ego-centric interaction graph -> compact latent world state encoding future-relevant interaction dynamics -> world-state-conditioned multi-modal planning / importance reweighting`

The paper explicitly rejects the assumption that long-horizon reasoning requires explicit multi-step rollout.

### Deletion/collapse test

Remove the learned relational world state and WSCP conditioning path and GraphWorld collapses toward a conventional interaction-aware multimodal planner.

### Nearest lineage relations

- It is downstream of latent-world planning broadly, and compares directly with World4Drive/LAW/WoTE-like approaches.
- It is only superficially similar to DriveLaW at the interface “world representation conditions planner.” The world object and scientific purpose differ sharply:
  - DriveLaW: generative-video internal latent as planning state;
  - GraphWorld: relational interaction state deliberately replacing explicit rollout for long-horizon reasoning.

### Current lineage judgment

**High confidence:** future-aware relational state is a genuine scientific idea, but whether it is a distinct route or a state-realization subtype requires broader evidence.

---

## 4. High-confidence lineage edges

The following edges are not intended as a complete chronology. They record strong conceptual inheritance/critique supported by the papers' framing.

| From | To | Relation | Confidence | Why it matters |
|---|---|---|---|---|
| LAW | World4Drive | **EXTENDS + FORKS** | High | World4Drive explicitly treats LAW's latent as too single-modal/semantically weak and adds physical priors, multimodal intentions and future-mode selection. |
| LAW | Drive-JEPA | **REFORMULATES / SCALES** | High | Both use predictive latent learning for planning representation; Drive-JEPA explicitly contrasts LAW-style auxiliary latent prediction with scalable JEPA pretraining. |
| Epona-like parallel gen-plan | DriveLaW | **CRITIQUES + TIGHTENS COUPLING** | Very high | DriveLaW explicitly names Epona-like separate output streams as insufficient and injects generator internal latents into planner. |
| tightly coupled WAMs | Metis | **CRITIQUES + DECOUPLES** | Very high | Metis explicitly targets representation interference and inference latency of tightly coupled future-video/action modeling. |
| WoTE-like model-based evaluation | WorldDrive FAR | **COMPRESSES / DISTILLS** | High | WorldDrive retains candidate-specific foresight but distills heavy future generation into an online surrogate/rewarder and adopts a related scoring paradigm. |
| WoTE / static latent WM | DynFlowDrive | **CHANGES DYNAMICS + COMPILES TO SCORER** | High | DynFlowDrive replaces static endpoint prediction with flow dynamics and removes world model from inference. |
| one-shot future-aware planning | SeerDrive | **CHANGES ONE-WAY TO RECIPROCAL** | Very high | SeerDrive explicitly frames bidirectional iterative interaction as a paradigm shift beyond one-shot planning. |
| explicit rollout/generation WM | GraphWorld | **REPLACES EXPLICIT IMAGINATION WITH RELATIONAL STATE** | High | GraphWorld explicitly avoids explicit multi-step rollout and conditions planning on a compact relational world state. |

---

## 5. Important multi-parent / synthesis nodes

### 5.1 WorldDrive

WorldDrive cannot be represented faithfully with one parent edge.

It combines:

- generative world-model representation learning;
- motion/vision representation unification;
- candidate-consequence evaluation;
- teacher-to-surrogate distillation for real-time inference.

This is a **synthesis node**.

### 5.2 Drive-JEPA

Drive-JEPA combines:

- predictive representation pretraining (WAM lineage);
- simulator-guided multimodal trajectory distillation (planning-supervision lineage);
- momentum-aware proposal selection (decision-layer innovation).

PF and PB expose different subsets of this program. They should not automatically become distant research lineages.

### 5.3 Discrete-WAM

Discrete-WAM combines:

- shared world/action representation;
- multi-task world-policy training;
- hierarchical decision-conditioned planning;
- parallel token editing.

Treating “joint world-action generation” as the whole paper is a severe compression error.

---

## 6. Provisional relationship clusters — not route classes

These are only working neighborhoods in the research graph.

### Cluster A — predictive representation / world knowledge internalization

Strong members:

- LAW
- Drive-JEPA predictive-pretraining component

Nearby but not equivalent:

- Epona planning benefit through shared temporal latent
- Metis joint training with deployment bypass

Open question:

> Is “world knowledge compiled into representation/parameters” a route, or a cross-cutting learning-transfer family?

### Cluster B — world-generation/planning coupling debate

Strong members:

- Epona: shared temporal latent + parallel modality generators
- DriveLaW: chained generator-latent -> planner
- Metis: separate experts + asymmetric information flow / bypass

This is currently one of the strongest natural scientific forks in the canonical set.

### Cluster C — action-consequence-based planning/evaluation

Members with materially different mechanisms:

- World4Drive: intention-specific latent future plausibility / mode selection
- WoTE: explicit recurrent candidate world rollout + reward
- WorldDrive: distilled candidate-specific future surrogate + reward
- DynFlowDrive: training-time flow-dynamics evaluation -> scorer supervision

Shared ancestor thesis:

> alternative actions should be informed by their induced world consequences.

Do **not** yet decide whether this is one route with subtypes or several routes.

### Cluster D — reciprocal world-planning reasoning

- SeerDrive paper

Potentially a child/fork of Cluster C, but the iterative bidirectional loop may justify a new major branch.

### Cluster E — future-aware latent state conditioning without explicit rollout

- GraphWorld

Potentially connects to latent-state planning and long-horizon interaction modeling rather than candidate consequence evaluation.

### Cluster F — unified world-policy representation/task paradigm

- Discrete-WAM

This may overlay several planning routes rather than be one route itself.

---

## 7. The Drive-JEPA PF/PB alarm — formal audit verdict

### Observation

Old projection:

- PF looked close to LAW/Epona/Metis because it deployed a direct action path with no online future carrier.
- PB looked close to generic candidate-resolver systems because it deployed proposals and a scorer.

This creates a genealogy distortion: two modes of one paper are pushed far apart, while PF may appear artificially close to Epona.

### Evidence from the paper

Drive-JEPA's introduction explicitly defines one integrated framework around two bottlenecks:

1. scalable planning-aligned predictive video pretraining;
2. multimodal behavior supervision beyond one human trajectory.

Its contributions and ablations treat:

- V-JEPA initialization;
- driving-domain JEPA pretraining;
- multimodal trajectory distillation;
- momentum selection

as cumulative components of one system.

### Verdict

> **PF/PB artifact distinction is valid for causal topology, but invalid as an automatic top-level research-lineage split.**

More strongly:

> **A taxonomy that makes Drive-JEPA PF genealogically closer to Epona than to Drive-JEPA PB is presumptively wrong unless it can explain why the paper's predictive-pretraining program is less fundamental than its downstream action-commitment form.**

Current evidence does not support that explanation.

### Consequence for future route reconstruction

We need at least two linked views:

- **paper-family genealogy:** what scientific program the paper advances;
- **artifact/mechanism realization:** which causal path a specific mode actually executes.

Neither view can replace the other.

---

## 8. Major false-separation risks exposed in the old ontology

### 8.1 Output topology can overpower paper identity

Drive-JEPA PF/PB is the strongest example.

`direct` vs `candidate resolver` is a real deployment difference, but it may be below the level of the paper's WAM research family.

### 8.2 Runtime presence can overpower learning lineage

LAW, Drive-JEPA, Metis and some Epona planning modes all lack explicit online future rollout, but they transfer world knowledge by very different mechanisms.

Conversely, simply grouping all of them as “W0” hides their genealogy.

### 8.3 Resolver semantics can create fake route splits

World4Drive / WorldDrive / WoTE differ in what the evaluator means, but scorer target semantics alone should not decide research lineage.

### 8.4 Paper capability modes can be mistaken for planning routes

Epona rollout and Discrete-WAM world-generation/joint modes are scientifically meaningful capabilities, but their presence should not automatically define the paper's deployed planning lineage.

---

## 9. Major false-merge risks

### 9.1 Shared outer DAG is insufficient

World4Drive, WoTE and WorldDrive can all be sketched as:

`candidate -> future representation -> score -> select`

Yet their indispensable mechanisms differ:

- mode plausibility/alignment;
- recurrent explicit model-based evaluation;
- distillation of heavy generative foresight into a surrogate.

### 9.2 “World representation -> planner” is too coarse

DriveLaW and GraphWorld both condition planning on a world-related latent, but:

- DriveLaW's claim is generator-internal latent chaining;
- GraphWorld's claim is compact relational interaction-state reasoning without explicit rollout.

Merging them from interface shape alone would erase the scientific fork.

---

## 10. Current genealogy graph — conceptual, not final taxonomy

```text
                         WAM + one-stage planning
                                 |
       ---------------------------------------------------------
       |                         |                             |
 predictive/world        generative world-action       action-consequence
 representation          coupling debate               reasoning/evaluation
       |                         |                             |
      LAW                    Epona                     World4Drive
       |                     /   \                         |
       |             tighter     decouple                  |
       |               |            |                      |
 Drive-JEPA(A)      DriveLaW      Metis                  WoTE
       |                                                /   \
       |                                   distill/retain   compile/drop
 multimodal planner                                  |          |
 distillation(B)                                  WorldDrive  DynFlowDrive
                                                        |
                                                synthesis with generative
                                                representation lineage

 One-shot future-aware reasoning ------------------------------> SeerDrive
                         (make world<->planning reciprocal)

 Explicit future imagination / short-horizon WM --------------> GraphWorld
                         (replace rollout with relational world state)

 Joint/generative world-action paradigms ----------------------> Discrete-WAM
                         (unify representation + tasks + hierarchical policy)
```

Important: this diagram is intentionally **not a tree**. WorldDrive, Drive-JEPA and Discrete-WAM are multi-component/synthesis nodes. Future evidence may add cross-edges.

---

## 11. What currently looks like a real “main fork” versus a profile

### Strong main-fork candidates

These have direct author-level scientific disagreement plus strong deletion/collapse behavior:

1. **parallel/shared vs chained vs deliberately decoupled world-generation/planning coupling**  
   Evidence: Epona ↔ DriveLaW ↔ Metis.

2. **one-shot future assistance vs reciprocal world-planning refinement**  
   Evidence: SeerDrive.

3. **online explicit model-based evaluation vs world reasoning compiled/distilled away**  
   Evidence: WoTE ↔ WorldDrive ↔ DynFlowDrive, although the exact discrete boundary is not settled.

### Likely lower-level/profile candidates

Current evidence says these should not by themselves define major lineage splits:

- resolver objective semantics;
- BEV vs RGB vs latent representation;
- diffusion vs Transformer vs flow as architecture names;
- number of candidates;
- expert vs simulator target provenance;
- PF vs PB operating setting by itself.

### Still unresolved

- predictive representation learning as a route versus a learning-transfer lineage;
- GraphWorld's relational-state conditioning as a major route versus one state-realization branch;
- unified world-action token language as route versus representation/training paradigm;
- whether World4Drive/WoTE/WorldDrive are one broad consequence-reasoning family with subbranches or several top-level routes.

---

## 12. Methodological conclusions from the audit

### 12.1 The target object is probably not a flat ontology

The canonical set naturally produces:

- ancestry;
- critique;
- synthesis;
- compilation/distillation;
- tightening/loosening of coupling;
- multi-parent inheritance.

A Cartesian product of peer axes poorly expresses these relations.

### 12.2 The target may be a layered research graph

A more faithful future representation may include:

1. **research-family lineage** — which scientific thesis/fork the paper advances;
2. **core world-to-planning bridge** — the indispensable causal mechanism;
3. **artifact realization** — exact train/deploy topology of each mode;
4. **profiles** — representation, resolver semantics, learning provenance, solver details.

This is only a meta-structure hypothesis, not an accepted ontology.

### 12.3 “Same paper” is evidence, not a guarantee

A paper can genuinely contain multiple routes. But splitting modes into distant families now requires explicit proof from:

- author framing;
- core-bridge deletion;
- collapse-to analysis;
- family coherence.

### 12.4 “No collision” is not a quality goal

Related papers **should collide at some abstraction level**.

A taxonomy that distinguishes every paper can be worse than one that groups genuine siblings. The question is not “can we separate them?” but:

> **Is the separation the scientific distinction the field itself is making?**

---

## 13. Audit verdict

This audit does **not** produce final CoreRoute labels.

It produces the following high-confidence corrections:

1. **Drive-JEPA PF/PB must remain genealogically linked.** Their artifact topologies differ, but current evidence does not justify treating them as distant WAM research routes.
2. **Epona and Drive-JEPA should not be considered close merely because some deployed modes both lack online future rollout.** Their research theses are materially different.
3. **Epona → DriveLaW → Metis exposes a genuine coupling debate** that the old R/W/E/L compression largely hides.
4. **LAW → World4Drive and LAW → Drive-JEPA are meaningful but different descendant relations:** World4Drive extends toward multimodal intention-conditioned online future selection; Drive-JEPA extends toward scalable predictive pretraining/transfer.
5. **WoTE → WorldDrive → DynFlowDrive exposes a meaningful spectrum of how world reasoning is retained, compressed, or compiled**, but it is not yet known whether this is one route with profiles or several routes.
6. **SeerDrive's reciprocal loop is a strong candidate for a major lineage fork.**
7. **GraphWorld's implicit relational world state and Discrete-WAM's unified token paradigm cannot be faithfully summarized by the old route codes alone.**
8. **Canonical 12 should be represented as a research graph with multi-parent nodes before any new taxonomy is proposed.**

---

## 14. Next audit step

Do not name final routes yet.

Next:

1. turn the high-confidence edges above into a canonical relationship matrix;
2. for every proposed edge, record explicit textual evidence and a counterfactual collapse statement;
3. test whether the same edge types recur in D01, D01.3 and D02-W1 target-domain papers;
4. only promote a relation into a CoreRoute split when multiple independent papers instantiate the same scientific fork;
5. keep profiles/implementation details below route level unless changing them repeatedly changes the core bridge.

The next question is no longer:

> “Which R/W/E/L code belongs to each paper?”

It is:

> **“Which scientific disagreements and inheritance relations recur often enough across the WAM + one-stage field to deserve becoming the field's actual planning routes?”**
