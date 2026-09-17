# Minimal-Branch Reconstruction — From Candidate Axes to Causal Bridge Motifs

Status: **FIRST-PRINCIPLES RECONSTRUCTION — NOT AN ONTOLOGY SPEC**  
Branch: `research/core-route-reconstruction`  
Date: 2026-09-17  
Input: canonical-12 lineage audit + D01 / D01.3 / D02-W1 pressure test + branch-point ledger  
Purpose: determine whether `BP-02`, `BP-03`, and `BP-07` are independent route questions, hierarchical questions, or redundant descriptions of one deeper causal structure.

---

## 0. Executive result

The three promoted branch questions should **not** be treated as three peer axes.

Current judgment:

1. `BP-03` and `BP-07` are largely two views of the **same deeper causal fork**.
2. `BP-02` is real, but as currently written it is **too broad**: it mixes a route-level question (“what causal bridge connects world modeling to planning?”) with lower-level coupling realizations (“parallel, chained, isolated, shared-token, etc.”).
3. The most compact structure currently supported by evidence is not a Cartesian axis system. It is a small set of **causal bridge motifs** describing the direction and locus by which world-model capability changes planning.
4. Research genealogy and mechanism-route identity must be kept separate. Closely related papers may deliberately choose different bridge motifs, while one paper may synthesize multiple motifs.

The strongest first-principles abstraction now appears to be:

> **What is the indispensable causal path by which learned world dynamics / future structure reaches the final planning behavior?**

A provisional causal grammar is introduced below only for reconstruction. It is **not yet a final taxonomy**.

---

## 1. Why the three promoted branch points cannot remain peer axes

The branch-point ledger promoted:

- `BP-02`: how world generation / prediction and action generation are coupled;
- `BP-03`: whether action choice depends on explicit/provisional action consequences;
- `BP-07`: direct future-aware state conditioning vs candidate-specific consequence evaluation.

At first glance these look independent. Under causal reconstruction, they are not.

### 1.1 `BP-03` and `BP-07` collapse toward one directional fork

Consider two mechanism skeletons.

### World-first / state-conditioned form

```text
observation/history
    -> world/future state Z
    -> planner/action A
```

or more compactly:

`O -> Z -> A`

Examples include:

- GraphWorld: ego-centric relational world state -> planning;
- OccWorld / Drive-OccWorld: predicted occupancy future -> planning;
- UniAD / BeTop / VAD: future-aware structured prediction -> direct planner;
- Policy World Model: autoregressive future tokens -> trajectory decoder;
- DriveLaW: video-generator latent -> Action DiT.

The defining fact is not whether `Z` is BEV, occupancy, latent, graph, or video-generator hidden state. It is that a world/future representation is formed and **then conditions one planning computation**.

### Action-indexed consequence form

```text
observation/history
    -> provisional/candidate action Ã_k
    -> consequence Z(Ã_k)
    -> evaluate / compare / refine
    -> committed action A*
```

or:

`O -> Ã -> Z(Ã) -> A*`

Examples include:

- WoTE;
- Drive-WM planning;
- DA-WAM;
- SafeDrive;
- RaWMPC;
- World4Drive;
- WorldDrive;
- DriveFuture, where `Z(Ã)` guides solver refinement instead of only external ranking.

The important difference is **causal direction**:

- world-first: `world -> action`;
- consequence reasoning: `action -> world -> action`.

Therefore `BP-07` (“direct state vs candidate consequence”) is not an independent peer of `BP-03`; it is essentially the clearest operational manifestation of `BP-03` within online future-aware planning.

### Current adjudication

`BP-03` and `BP-07` should be **merged for route discovery** into a deeper question:

> **Does planning consume a world/future state formed independently of a particular ego alternative, or does a provisional ego action index the world consequence that then changes commitment?**

This is a much cleaner scientific fork than keeping both old branch questions.

---

## 2. `BP-02` is real, but currently mixes two abstraction levels

The Epona / DriveLaW / Metis triangle correctly exposed a real disagreement:

> How tightly should world modeling and planning be coupled?

But “coupling topology” currently combines at least two different things.

### 2.1 Route-level causal mediation

Examples:

- world computation only changes learned parameters / representation;
- online world state directly conditions action;
- provisional action conditions world consequence, which changes action;
- world and action are generated jointly;
- world and action repeatedly update each other.

These are changes in the **causal bridge itself**.

### 2.2 Realization-level coupling design

Examples:

- shared latent with parallel heads;
- generator latent chained into planner;
- separate experts;
- asymmetric attention;
- isolated attention;
- shared autoregressive token backbone;
- diffusion vs flow vs autoregression.

These can be scientifically important, but not all deserve equal route status.

### 2.3 Consequence

`BP-02` should not be promoted wholesale as a single “coupling axis.”

Instead, it should be decomposed:

- **bridge topology** = potential route-defining object;
- **coupling realization** = profile/sub-branch unless deletion evidence shows it changes the bridge.

DriveLaW is a useful example. “Video latent directly conditions Action DiT” changes the online information path, so it is route-relevant.

Changing the exact diffusion block, latent resolution, or noise schedule does not.

---

## 3. Major correction: research genealogy is not the same object as mechanism-route hierarchy

This distinction is now necessary.

### 3.1 Research genealogy asks

- Which paper responds to which previous limitation?
- Which paper tightens, relaxes, distills, reverses, or criticizes another design?
- Which papers share a scientific ancestor?

### 3.2 Mechanism-route hierarchy asks

- Through what causal bridge does world-model capability change planning?

These graphs are related but not identical.

### Example: Epona / DriveLaW / Metis

Genealogically they are close.

DriveLaW explicitly argues that Epona-like parallel generation/planning does not sufficiently exploit the generator’s internal representation and proposes a chained latent-to-planner bridge.

Metis/SimWAM-like designs push in the opposite direction: they seek world-model training benefit while avoiding future-video dependence on the deployed action path.

Thus the papers may be close **because they disagree about the bridge**.

A route system is allowed to separate them if that separation corresponds to the scientific decision they are debating.

### Example: Drive-JEPA PF / PB

PF and PB are both descendants of the same predictive-representation program.

PB adds proposal generation, simulator-derived multimodal supervision, and a candidate selector. But the world-model contribution itself still reaches planning primarily through the pretrained predictive representation.

Therefore an artifact-level difference in planner topology does not automatically imply a different WAM research route.

This resolves the earlier Drive-JEPA alarm more cleanly:

> classify the **world-to-planning bridge**, not every downstream planner operation as if it were a world-model route difference.

---

## 4. Provisional causal grammar

The following motifs are introduced as a reconstruction language, not final class names.

Let:

- `O` = current/history observation or encoded context;
- `Z` = qualifying world/future state, representation, consequence, or world-model computation;
- `Ã` = provisional/candidate action or trajectory;
- `A*` = committed action/trajectory;
- `θ_A` = deployed planner/policy/scorer parameters changed by learning.

### M0 — Compiled world knowledge

Training:

`world/predictive process -> loss/reward/teacher signal -> θ_A`

Deployment:

`O -> θ_A -> A*`

No separately traceable world/future mediator needs to remain on the deployed causal path.

Representative mechanisms:

- LAW — action-conditioned future prediction shapes representation/planner;
- Drive-JEPA — predictive pretraining transfers encoder to PF/PB planners;
- ViDAR / DriveWorld / ReWorld / WA-JEPA — predictive pretraining / representation transfer;
- DynFlowDrive — world dynamics create scorer supervision; world model disappears online;
- Think2Drive — imagined return trains actor/critic;
- CRAFT — counterfactual advantages train policy;
- CausalDrive policy post-training — simulator/reward trains policy;
- SimWAM / Metis-like bypass — world/video branch contributes during learning but action deployment bypasses future generation.

Important warning:

`M0` is **too broad to be a final leaf route**. It is a high-level ancestor containing several different transfer mechanisms.

Likely sub-branches include at least:

- predictive representation shaping/transfer;
- world-derived evaluator/scorer supervision;
- world/simulator-derived policy optimization;
- joint world/action training with future branch bypass.

### M1 — Online world-first mediation

`O -> Z -> A*`

A world/future state or generative representation is formed online and directly conditions action formation, without first requiring an ego candidate to index a distinct consequence branch.

Representative mechanisms:

- GraphWorld — relational world state -> planner;
- OccWorld / Drive-OccWorld — future occupancy -> planning;
- UniAD / BeTop / VAD — predicted future structure -> direct planner;
- Policy World Model — future state tokens -> trajectory decoder;
- DriveLaW — video-generator latent -> Action DiT;
- Epona planning path — shared temporal world state supports trajectory generation while video output may be disabled.

Internal scientific distinctions remain:

- current relational state vs explicit future forecast;
- shared temporal latent vs generator internal latent;
- structured occupancy/agent forecast vs learned generative latent.

Those differences are not yet proven to require separate top-level routes.

### M2 — Action-conditioned consequence mediation

`O -> Ã_k -> Z(Ã_k) -> evaluate/refine -> A*`

A provisional ego action, intention, trajectory, or candidate indexes a distinct predicted consequence. That consequence then changes which action is committed or how the action is refined.

Representative mechanisms:

- World4Drive — intention-specific future latent -> plausibility / mode selection;
- WoTE — candidate -> recurrent future rollout -> reward -> selection;
- WorldDrive — candidate -> distilled future latent -> future-aware reward -> selection;
- Drive-WM — candidate -> generated future views -> planning cost -> selection;
- DA-WAM — candidate -> future latent -> score;
- SafeDrive — proposal -> sparse future world -> safety reasoning;
- RaWMPC — candidate sequence -> horizon rollout -> risk/progress cost;
- DriveFuture — provisional trajectory -> future latent -> solver guidance/refinement.

This motif survives implementation substitution across:

- video;
- BEV;
- occupancy / sparse world;
- latent state;
- diffusion solver;
- cost, reward, plausibility, or safety criteria.

Therefore the causal order `action -> consequence -> changed action` is currently one of the strongest field-level route signals.

### M3 — Joint world-action generation

`O -> G -> (Z, A)`

World/future variables and action variables are born within one generative process rather than one clearly mediating the other.

Representative evidence:

- DrivingGPT shared autoregressive world/action process;
- GenAD joint ego/agent future generation;
- Gen-Drive joint ego/agent future scene generation;
- Discrete-WAM joint world-policy mode.

Important caution:

Shared representation is not enough. `M3` requires real generative jointness / co-birth of world and action variables, not merely two heads attached to one encoder.

This is why Epona should not be automatically collapsed into `M3`: parallel heads sharing a temporal latent are not the same as a single joint world-action sample/process.

### M4 — Reciprocal world-action refinement

`O -> A^(0) -> Z^(1) -> A^(1) -> Z^(2) -> ... -> A*`

World and planning states repeatedly modify each other before final commitment.

Confirmed anchor:

- SeerDrive paper.

Near-neighbors not yet admitted:

- DriveFuture — solver-internal future guidance, but full alternating world/action update not established;
- GraphAD — iterative predictive graph updates, but ego-plan-to-world-to-revised-plan loop not established;
- joint generators — simultaneous co-generation is not reciprocal refinement.

Current status remains singleton / provisional extension.

---

## 5. Why this grammar is better than the old promoted branch set

### 5.1 It resolves `BP-03` vs `BP-07` redundancy

`M1` and `M2` capture the causal fork directly:

- `M1`: `world -> action`;
- `M2`: `action -> world -> action`.

No separate “direct future state” axis is required.

### 5.2 It explains Drive-JEPA PF/PB without artificial route splitting

PF:

`predictive pretraining -> encoder parameters -> direct planner`

PB:

`predictive pretraining -> same encoder family -> proposal planner / scorer`

From the WAM bridge perspective both remain primarily `M0` predictive-representation descendants.

PB adds a candidate-planning mechanism, but because that candidate scorer does not itself run a world consequence model, it does not become `M2` merely because multiple proposals exist.

This is exactly the distinction the old `R` layer obscured.

### 5.3 It explains DrivoR / TOAD / Hydra-MDP as negative controls

All may have candidates and resolvers.

But:

`proposal -> score -> choose`

is not equivalent to:

`proposal -> predicted world consequence -> choose`.

Therefore they are not `M2` WAM routes solely because they perform candidate selection.

### 5.4 It preserves Epona / DriveLaW / Metis scientific disagreement

The genealogy remains close, but their bridge choices can differ:

- Epona: shared temporal world state supports both generation and planning; planning output can run without video rendering;
- DriveLaW: generator internal latent explicitly becomes the planning state (`M1`, chained realization);
- Metis/SimWAM-like design: future-generation computation is deliberately prevented from becoming an online action dependency, pushing the deployed bridge toward `M0`-style compiled/shared-training benefit.

Thus the new structure does not force genealogical siblings into one route simply to preserve “family coherence.”

Family coherence is a **warning test**, not a no-split rule.

### 5.5 It preserves World4Drive / WoTE / WorldDrive commonality without erasing their real differences

All three plausibly sit under `M2` because an intention/candidate indexes future-related information that then changes final selection.

But their sub-branches remain different:

- World4Drive — intention-conditioned future plausibility / factual-mode agreement;
- WoTE — explicit recurrent rollout + driving reward;
- WorldDrive — representation inheritance + distilled online future surrogate + reward.

This is a better expression of the user's “common ancestor -> major branch -> unique innovation” intuition than either full merging or flat code separation.

### 5.6 It gives WorldDrive a legitimate multi-parent structure

WorldDrive contains at least two bridges:

1. world-generation pretraining -> transferred visual/motion encoders (`M0`-like representation inheritance);
2. candidate -> distilled future latent -> reward -> selected trajectory (`M2`).

A one-label-per-paper ontology would hide this synthesis.

The research graph should allow:

`predictive/generative representation lineage + action-consequence lineage -> WorldDrive`.

### 5.7 It does not force Discrete-WAM into one misleading route

Discrete-WAM spans:

- representation paradigm: unified discrete world/action token space;
- training program: world, world-policy, and policy objectives;
- possible joint world-action generative mode (`M3`);
- deployed hierarchical policy generation.

Therefore the paper can be genealogically linked to `M3` without claiming that every deployment mode is “joint world-action generation.”

---

## 6. Canonical-12 provisional reconstruction

This table is deliberately **not a final classification**. It asks which causal motif(s) are indispensable to the paper's WAM planning thesis.

| Paper | Provisional indispensable bridge motif(s) | Why this is more faithful than old route code |
|---|---|---|
| LAW | `M0: predictive representation shaping` | World prediction changes planner through learning, not online candidate/world evaluation. |
| Epona | `M1: shared temporal world state -> trajectory generation` + joint-training context | Captures the shared world state that supports planning while video rendering can be disabled; avoids calling it merely “direct action.” |
| DriveLaW | `M1: generator latent -> planner` | The generator's internal latent is explicitly the planning state; deletion destroys the paper's chained thesis. |
| World4Drive | `M2: intention -> future latent -> mode commitment` | Its core is intention-conditioned future reasoning, not generic candidate scoring. |
| WorldDrive | `M0 + M2` synthesis | Representation inheritance and distilled consequence evaluation are both central contributions. |
| WoTE | `M2: candidate -> recurrent world rollout -> reward -> select` | Explicit online model-based trajectory evaluation. |
| SeerDrive | `M4: reciprocal world<->planning refinement` | Feedback loop, not merely presence of future BEV, is the paper's claimed paradigm shift. |
| Drive-JEPA PF | `M0: predictive pretraining -> planner` | Keeps PF with the paper's predictive-representation thesis. |
| Drive-JEPA PB | `M0: predictive pretraining -> planner` + non-WM candidate/resolver specialization | PB's candidate resolver does not by itself create an `M2` WAM route. |
| Metis | `M0: world/action joint training with online future bypass` (provisional) | Captures deliberate removal of future-video dependency from action inference. |
| DynFlowDrive | `M0: world-dynamics-derived scorer supervision` | World model teaches the scorer and disappears at inference. |
| Discrete-WAM | `M3` evidence in joint mode + unified-representation/training paradigm; deployed policy route remains multi-level | Avoids reducing the entire paper to “joint emission.” |
| GraphWorld | `M1: relational world state -> planning` | Future-relevant interaction state directly conditions planning without candidate-specific rollout. |

Note: the canonical program historically contains 12 paper families but multiple artifacts/modes; therefore the table intentionally preserves mode-aware qualifications rather than forcing a one-row-one-code interpretation.

---

## 7. Broader-corpus adversarial checks

### 7.1 `M0` is real but internally heterogeneous

Independent descendants:

- ViDAR — predictive geometry pretraining transfer;
- DriveWorld — world representation pretraining transfer;
- ReWorld / WA-JEPA — predictive representation learning;
- Think2Drive — imagined rollout -> actor/critic;
- CRAFT — counterfactual advantage -> policy update;
- CausalDrive policy post-training — simulator reward -> policy;
- SimWAM — video/action joint training -> action-only deployment;
- DynFlowDrive — world dynamics -> scorer target.

Conclusion:

`M0` is likely a major **ancestor branch** (“compiled world knowledge”), but not a final leaf route.

### 7.2 `M1` independently recurs

- OccWorld;
- Drive-OccWorld;
- Policy World Model;
- UniAD;
- BeTop;
- VAD;
- GraphAD;
- DriveDreamer action path.

The substrate changes radically, but `world/future state -> direct planning` recurs.

### 7.3 `M2` independently recurs with clean negatives

Positive:

- Drive-WM;
- DA-WAM;
- SafeDrive;
- RaWMPC;
- DriveFuture;
- Gen-Drive multi-sample mode.

Negative controls:

- DrivoR;
- TOAD;
- Hydra-MDP;
- Drive-JEPA PB.

This is strong evidence that candidate count / resolver topology is not the route-defining object. The qualifying difference is whether the **candidate/provisional action changes a predicted world consequence that then changes commitment**.

### 7.4 `M3` recurs independently

- DrivingGPT;
- GenAD;
- Gen-Drive;
- Discrete-WAM joint mode.

But shared latent or shared encoder alone is not enough.

### 7.5 `M4` remains under-replicated

SeerDrive remains the strongest confirmed case.

Do not promote `M4` to a mature field family until another independent target-domain paper shows genuine alternating world-update/action-update before commitment.

---

## 8. Independence and hierarchy tests

### Test A — Can `M1` and `M2` vary while training method stays fixed?

Yes in principle. Both can use diffusion, transformers, BEV, latent states, shared pretraining, or supervised future prediction. Therefore the causal direction is not reducible to implementation.

### Test B — Can the same paper combine motifs?

Yes.

WorldDrive combines `M0 + M2`.

Gen-Drive can combine `M3` joint future generation with a downstream ranking stage, depending on mode.

Discrete-WAM combines a representation/training paradigm with `M3`-like joint modeling and a separate policy mode.

Therefore the final research map must permit **composition**, not only mutually exclusive labels.

### Test C — Is online-vs-compiled sufficient as the top split?

No.

It is useful but too coarse:

- `M1`, `M2`, `M3`, `M4` can all retain online world-related computation but are mechanistically different;
- `M0` contains predictive representation, scorer distillation, policy RL, and asymmetric joint training.

Thus lifecycle is necessary context, not the full route identity.

### Test D — Is “world/action coupling topology” itself a sufficient single axis?

No.

If defined too broadly it simply renames the whole problem.

A useful route system needs **specific recurrent bridge motifs**, not an abstract axis whose values reproduce every paper architecture.

### Test E — Is `M1` vs `M2` scientifically meaningful?

Current answer: yes, high confidence.

The distinction changes causal direction:

- `M1`: world/future representation exists before the planner's final action reasoning;
- `M2`: a provisional ego action is necessary to instantiate the relevant world consequence.

Deleting that action-indexed world branch from WoTE / Drive-WM / DA-WAM / SafeDrive / RaWMPC collapses them toward direct-state planning or ordinary candidate scoring.

This passes both deletion and negative-control tests.

---

## 9. New understanding of the user's `a + b/c + unique` intuition

The strongest surviving interpretation is not:

`paper = a + exactly one b/c + exactly one unique feature`.

It is closer to:

```text
shared field premise
    -> recurrent causal bridge motif
        -> sub-branch / coupling realization
            -> paper-specific innovation
```

with optional synthesis:

```text
motif A -----\
             -> synthesis paper
motif B -----/
```

For example:

```text
WAM improves one-stage planning
    -> action-conditioned consequence reasoning
        -> explicit rollout (WoTE)
        -> distilled future surrogate (WorldDrive)
        -> plausibility matching (World4Drive)
        -> solver-internal foresight (DriveFuture)
```

while WorldDrive also receives a second parent from representation inheritance.

This structure is much closer to an **idea DAG** than a flat taxonomy.

---

## 10. What is now superseded

The following assumptions should be marked `SUPERSEDED` for route discovery:

1. `R–W–E⊕L` as the primary discovery coordinate system.
2. “No collision” as a positive ontology objective by itself.
3. Deployment commitment topology as the main route identity.
4. Three independent promoted branch questions `BP-02 / BP-03 / BP-07`.
5. `BP-07` as a separate top-level branch from `BP-03`.
6. Treating genealogy proximity as proof of route equivalence.
7. Treating one paper as necessarily one route.

Still retained:

- old ontology as a structured evidence ledger;
- artifact splitting for exact causal-path auditing;
- lifecycle tracking;
- resolver semantics as a profile;
- deletion/collapse tests;
- family-coherence warning;
- implementation-invariance tests.

---

## 11. Current confidence-weighted verdict

### High confidence

- `BP-03` and `BP-07` should not survive as independent route questions.
- The causal direction `world -> action` vs `action -> world consequence -> action` is a real recurring mechanism distinction.
- Drive-JEPA PF/PB should not be separated into different WAM routes merely because PB uses proposal selection.
- Candidate resolver existence alone is not evidence of action-consequence world reasoning.
- Research genealogy and mechanism-route hierarchy are different objects.
- Papers can synthesize multiple bridge motifs.

### Medium/high confidence

- A compact causal grammar roughly resembling `M0 / M1 / M2 / M3 / M4` is a better reconstruction language than the old flat axes.
- `M1` and `M2` are mature recurring bridge motifs.
- `M0` is a real high-level ancestor but requires internal subdivision before becoming a useful leaf route.
- `M3` is recurrent enough to keep as a strong route candidate, though exact jointness gates need tightening.

### Medium confidence

- Epona belongs primarily under an online shared-world-state planning motif rather than a compiled-only motif. Planning-only inference disables video rendering, but the shared temporal world representation remains central; exact runtime carrier semantics should be rechecked if this distinction becomes normative.
- Metis belongs primarily on the compiled / bypass side; exact retained shared-state path should be rechecked before normative classification.

### Low/medium confidence

- `M4` as a field-level route rather than a SeerDrive-specific branch.
- exact number of leaf routes needed under `M0`, `M1`, and `M2`.

---

## 12. Next gate: adversarial motif regression before naming

Do **not** name final CoreRoutes yet.

The next audit should attack the provisional motifs with hard pairs:

1. Drive-JEPA PF vs PB — family coherence under `M0`;
2. Epona vs DriveLaW vs Metis — does the bridge grammar preserve the scientific coupling dispute without over-splitting?
3. GraphWorld / OccWorld / UniAD vs WoTE / Drive-WM / SafeDrive — does `M1` vs `M2` survive detailed mechanism reading?
4. World4Drive vs WoTE vs WorldDrive vs DA-WAM — are all truly `M2` descendants, and what internal fork is indispensable?
5. DrivingGPT / GenAD / Gen-Drive / Discrete-WAM — define strict `M3` jointness gate;
6. SeerDrive vs DriveFuture / GraphAD — determine whether `M4` is independent or an iterative subtype of `M2`/`M1`.
7. LAW / Drive-JEPA / ViDAR / DynFlowDrive / Think2Drive / SimWAM — determine how many genuine `M0` sub-branches exist.

Only after these tests should provisional route names be proposed.

The research goal remains:

> **minimum sufficient hierarchy of genuine world-model-to-planning causal ideas, with paper-specific innovations preserved but not promoted into fake top-level routes.**
