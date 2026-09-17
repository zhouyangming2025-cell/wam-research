# Domain Lineage Pressure Test — Canonical 12 vs D01 / D01.3 / D02-W1

Status: **PRESSURE TEST — NOT AN ONTOLOGY SPEC**  
Branch: `research/core-route-reconstruction`  
Date: 2026-09-17  
Scope: test whether research-lineage relations reconstructed from the canonical 12 recur in broader target-domain evidence.

## 0. Purpose

The canonical-12 audit produced a research-idea graph rather than a flat route code table. This document tests whether those relationships survive contact with three independent evidence pools:

- D01 domain census;
- D01.3 blind set;
- D02-W1 / W1e broader-domain wave.

The test does **not** project these papers back into R/W/E/L. It asks whether the scientific forks observed in the canonical 12 recur under different papers and mechanisms.

Four hypotheses are under pressure:

1. world-generation / planning coupling topology is a real recurring scientific fork;
2. online world reasoning -> distilled surrogate -> compiled residue is a recurring lifecycle pattern;
3. reciprocal world↔planning refinement is a stable family rather than a SeerDrive-specific idea;
4. predictive-representation learning forms a stable lineage, and whether that lineage is a CoreRoute or a learning-transfer family.

A fifth question is tracked throughout:

> when two papers share a deployment skeleton, do they also share the same scientific world-to-planning bridge?

## 1. Evidence pools used

### D01

Mechanism skeletons provide artifact-level causal descriptions for Drive-WM, OccWorld, Think2Drive, DrivingGPT, Drive-OccWorld, ViDAR, DriveWorld, Auto-JEPA, WorldRFT, ReWorld, WA-JEPA, DA-WAM, SafeDrive, Gen-Drive, SimWAM, DriveFuture, Policy World Model, CausalDrive, and RaWMPC.

This pool is especially useful because it contains multiple mechanisms that were not part of the canonical 12 derivation set.

### D01.3 blind set

The ontology-free blind cards provide independent cases:

- GraphAD planning;
- DriveDreamer video-generation mode;
- DriveDreamer action path;
- DrivoR candidate/scorer planning.

These were described before ontology projection and therefore serve as useful checks against retrospective fitting.

### D02-W1 / W1e

The breadth wave contributes BeTop, TOAD, CRAFT, Hydra-MDP, DRIVEVLM, OmniDrive, ORION, GenAD, UniAD, VAD and multiple simulator / prediction boundaries.

The old D02 route-family labels are **not** treated as evidence for the new lineage model. Only their mechanism descriptions and source-backed causal facts are used.

---

## 2. Hypothesis A — world-generation / planning coupling topology

### Canonical-12 seed

The strongest canonical relation was the Epona / DriveLaW / Metis triangle:

- Epona: shared temporal representation with parallel specialized video and trajectory generation;
- DriveLaW: video-generator internal latent directly conditions the planner;
- Metis: separate experts with asymmetric information flow so future-video computation can train the system but be bypassed for action inference.

The question was whether this is a genuine field-level scientific fork or merely three paper-specific implementations.

### Broader-domain evidence

#### DrivingGPT

D01 describes a shared autoregressive world/action backbone in which future/world and action tokens are learned by one generative model and the planning mode autoregressively emits action tokens. This is neither Epona-style parallel specialized diffusion heads nor Metis-style explicit action-side blocking. It supports the existence of a broader design question about how world and action generation inhabit one computational process.

#### SimWAM

D01 describes joint video/action training but an action-only deployed path. The video expert is a training object; isolated attention prevents action inference from depending on generated future frames. This independently reproduces the **deliberate decoupling / bypass** idea seen in Metis.

This is important: Metis is therefore not a one-off architectural curiosity. The broader corpus contains another mechanism whose scientific goal is to extract world-model training benefit without forcing expensive future generation onto the deployed action path.

#### Policy World Model

D01 records an online autoregressive future-token horizon fused into trajectory decoding. This supports another coupling form: world/future state is explicitly generated first or alongside planning and remains on the deployed causal path.

#### Gen-Drive

D01 contains both a generate-then-evaluate mode and a single-sample policy mode. Joint ego/agent futures are generated as one object. In the multi-sample mode, the generated joint futures are ranked; in the single-sample mode, preference is compiled into generator parameters and the evaluator can disappear.

This provides an important warning: **joint generation topology and final decision topology can vary inside one paper family.** Therefore coupling topology must be reconstructed at both paper-thesis and artifact levels.

#### DriveFuture

D01 describes provisional ego action / trajectory -> predicted future latent -> foresight guidance inside diffusion planning. This is neither a simple chained `world latent -> planner` feed-forward path nor an external candidate evaluator. World prediction participates inside the action solver itself.

#### DriveDreamer blind case

D01.3 independently finds an action path where recurrent predicted structural evolution and multi-scale world-model features feed an action decoder while future video is jointly trained/generated. The exact semantic jointness is unresolved, but the case clearly supports the broader question of **how internal world-generation features enter action formation**.

#### GenAD in D02-W1

GenAD jointly emits world-agent and ego trajectories from one generative process. This independently supports the existence of a joint world/action generation paradigm distinct from a candidate-conditioned external consequence evaluator.

### Pressure-test verdict

**SUPPORTED — HIGH confidence.**

The canonical Epona / DriveLaW / Metis disagreement is not confined to those papers. The broader domain repeatedly revisits the same scientific decision:

> What information from world modeling is allowed to enter action generation, and through what coupling topology?

Observed answers include:

- shared backbone / parallel heads;
- generator representation directly conditioning planner;
- explicit future state feeding action decoder;
- one joint world-action generative process;
- world prediction embedded inside action refinement / diffusion solving;
- deliberate asymmetric or isolated training coupling with future generation bypassed online.

### Important restraint

This does **not** yet justify a flat “coupling axis.” Some of these differences may form separate routes, while others may be profiles inside a higher-order family. But coupling topology has now passed the basic recurrence test required of a serious route-defining question.

---

## 3. Hypothesis B — online world reasoning -> surrogate -> compiled residue

### Canonical-12 seed

The canonical set suggested a possible progression:

- WoTE: explicit candidate-conditioned online world rollout;
- WorldDrive: expensive world generation distilled into a lightweight candidate-specific future surrogate;
- DynFlowDrive: world model removed at inference, leaving a scorer trained by world-derived supervision.

The question was whether this represents a route family, a deployment profile, or an accidental three-paper sequence.

### Broader-domain evidence

#### Drive-WM

D01 provides a clear full-online endpoint: candidate ego trajectories condition future multiview scene generation, a planning cost is computed per branch, and the minimum-cost trajectory is committed. The world-consequence computation remains online.

#### DA-WAM

D01 gives a compact online-surrogate form: candidate trajectories index predicted future latents; a common scorer ranks them online. The target future branch is training-only, but the candidate-specific future predictor survives.

This strongly resembles the **surrogate future consequence** position in the canonical WorldDrive story, but without requiring the same representation or teacher architecture.

#### SafeDrive

Proposal-specific sparse future worlds over agents/road remain online and are used by safety reasoning. This is another explicit online candidate-consequence mechanism, implemented with sparse structured worlds rather than video or BEV rollout.

#### RaWMPC

Candidate action sequences are rolled out through an action-conditioned world model; semantic/risk/ego predictions feed a shared cost and the minimum-cost action sequence is selected. This independently supports the full-online planning-through-consequence end.

#### Think2Drive

Action-conditioned imagined latent rollouts and returns train actor/critic updates, but the rollout machinery is not the final online candidate resolver. World reasoning is transferred into the deployed policy through policy optimization.

#### CRAFT

Counterfactual world-derived group advantages and closed-loop corrections train the policy; deployment drops the counterfactual world machinery. Again, world reasoning survives only through changed policy parameters.

#### CausalDrive policy post-training

The simulator produces intervention-conditioned rollout/reward signals for reinforcement updates and is absent from the final deployed policy. This is another compiled-training case.

#### SimWAM

Future video is used during joint training; deployment runs the action expert without future-video generation. This is compilation through shared/joint training rather than scorer supervision or RL.

### Pressure-test verdict

**RECURRENCE SUPPORTED, BUT ROUTE STATUS REJECTED FOR NOW — HIGH confidence.**

The online -> surrogate -> compiled pattern is unquestionably real across the domain. However, it does **not** behave like one scientific route.

Why:

- Think2Drive compiles imagined return optimization into a policy;
- CRAFT compiles counterfactual advantages into a policy;
- CausalDrive compiles simulator rewards through RL;
- SimWAM compiles predictive/video supervision through joint training;
- DynFlowDrive compiles world-dynamic evaluation into a scorer;
- WorldDrive distills a candidate-specific future representation that still remains online.

The shared property is **deployment residue**, not the same world-to-planning causal program.

Therefore:

> `how much world reasoning survives deployment` is strongly supported as a lifecycle / compilation profile, but currently fails the test for a standalone CoreRoute.

This is a direct correction to any taxonomy that would merge all training-only world-model methods because their runtime graph becomes action-only.

---

## 4. Hypothesis C — reciprocal world↔planning refinement

### Canonical-12 seed

SeerDrive paper proposes repeated mutual refinement:

`world prediction -> planning -> updated world prediction -> revised planning -> ...`

The route-defining hypothesis is reciprocal causal interaction, not merely iterative neural computation.

### Search for independent relatives

#### GraphAD blind case

D01.3 shows iterative graph updates over predicted multi-agent motions before a direct ego planning output. This initially looks like a possible reciprocal relative.

But the blind card explicitly leaves unresolved whether the repeated graph layers constitute policy/world reciprocity or merely internal predictive feature refinement. No evidence establishes that a committed/provisional ego plan alters a world prediction and is then revised by that changed world prediction in the SeerDrive sense.

Therefore GraphAD is **not** accepted as a reciprocal match.

#### DriveFuture

World latent prediction guides diffusion planning during solving. This creates interaction between future prediction and action refinement, but the available mechanism skeleton does not establish a full alternating bidirectional world-update/action-update loop. It is a promising near-neighbor, not confirmed evidence of the same branch.

#### BeTop

Future multi-agent trajectory topology guides planning and interactive prediction, but D02 evidence supports structured future-aware conditioning rather than an evidenced ego-plan -> world -> revised-ego-plan reciprocal loop.

#### Joint generators

DrivingGPT, GenAD, Gen-Drive and Discrete-WAM couple world and action variables, but joint generation is not equivalent to reciprocal refinement. Simultaneous/co-generated variables should not be promoted to the SeerDrive lineage merely because both modalities interact.

### Pressure-test verdict

**NOT YET REPLICATED — MEDIUM/HIGH confidence.**

SeerDrive's reciprocal loop remains scientifically meaningful, but in the inspected independent corpus it is still close to a singleton.

This matters methodologically:

> A mechanism can be real and important without yet deserving a broad field-level route class.

Current status should therefore be:

- retain reciprocal refinement as a strong candidate branch;
- do not promote it to a stable CoreRoute solely from SeerDrive;
- actively search later waves for independent implementations where provisional action changes predicted world consequences and those changed consequences revise the action within one decision process.

---

## 5. Hypothesis D — predictive representation lineage

### Canonical-12 seed

LAW and Drive-JEPA share the idea that predictive/world learning can improve planning without requiring expensive online world simulation, but differ in learning program:

- LAW: action-conditioned future-latent prediction integrated into end-to-end training;
- Drive-JEPA: scalable predictive video pretraining followed by transfer, plus an orthogonal multimodal-planning program.

### Broader-domain evidence

#### ViDAR

Future point-cloud / occupancy prediction is used during pretraining; the forecasting decoder can disappear while the transferred encoder supports downstream planning. This is a clean independent example of predictive pretraining -> representation transfer -> planner.

#### DriveWorld

Spatiotemporal world-model pretraining transfers a world representation into downstream planning. Predictive heads may be removed. Again, the central bridge is learned representation rather than online future evaluation.

#### ReWorld

D01 describes predictive representation learning -> world-action representation -> direct trajectory generator, with predictive targets/heads removable at deployment.

#### WA-JEPA

Future/action predictive targets shape a shared representation; target/teacher machinery is training-side while the context representation and action decoder survive.

#### OmniDrive / counterfactual VLM supervision

D02-W1 supplies a weaker but useful boundary case: counterfactual data/reasoning can shape a deployed planner even when no predictive future object survives online. This demonstrates why “training-time future knowledge” is broader than predictive-representation WAM and should not all be merged.

### Pressure-test verdict

**LINEAGE STRONGLY SUPPORTED; CORE-ROUTE STATUS UNRESOLVED — HIGH confidence.**

There is clearly a recurring research lineage in which future/world prediction is used to create planning-useful representations and the expensive predictive task can disappear at deployment.

However, evidence currently suggests that the stable commonality is primarily **how world capability is learned and transferred**, not necessarily a unique deployment decision mechanism.

Therefore the best current interpretation is:

> predictive-representation learning is a strong Learning/Transfer lineage that may cut across multiple planning routes.

It should only become a CoreRoute if later evidence shows that these papers share an indispensable planning bridge beyond “better predictive representation transferred into the planner.”

---

## 6. New pressure result — action-consequence reasoning is much broader than the canonical trio

The canonical set made World4Drive / WoTE / WorldDrive look like a difficult local cluster. D01 shows that their shared ancestor is much broader.

Independent examples include:

- Drive-WM: candidate -> generated future views -> cost -> select;
- DA-WAM: candidate -> future latent -> score -> select;
- SafeDrive: proposal -> sparse future world -> safety reasoning -> commit/refine;
- RaWMPC: candidate sequence -> horizon rollout -> risk/progress cost -> select;
- Gen-Drive multi-sample: sampled joint future scenes -> learned value -> select;
- Auto-JEPA: predicted future intent -> trajectory-memory alternatives -> refine/rank;
- DriveFuture: provisional action -> predicted future latent -> guidance inside action solving.

### Interpretation

A robust common ancestor now exists:

> **Planning should depend on consequences/future structure associated with alternative or provisional actions, rather than only the current observation.**

But the descendants differ in a way that the old `candidate -> future -> score` skeleton cannot capture:

1. external candidate evaluation by explicit simulated consequences;
2. compact candidate-specific future surrogate;
3. joint future-scene generation and ranking;
4. future intent retrieval rather than environmental consequence prediction;
5. future prediction embedded inside trajectory optimization / denoising;
6. plausibility matching against factual future rather than downstream utility.

This is strong evidence for a **large research lineage with internal scientific forks**, not one flat route.

---

## 7. New pressure result — direct future-aware state conditioning also recurs

GraphWorld's core idea was future-aware planning without explicit online rollout: encode interaction-relevant world state and use it directly for planning.

Broader relatives include:

- OccWorld: recurrent future occupancy horizon directly informs planning;
- Drive-OccWorld: online 4D occupancy forecast conditions planning;
- UniAD: predicted agent motion / occupancy exposed through unified queries to planner;
- BeTop: future multi-agent behavioral topology guides a direct trajectory generator;
- VAD: predicted vectorized agent motion guides direct trajectory output;
- GraphAD blind case: future motion predictions organize interaction graph structure before direct ego planning.

### Interpretation

There is a real family of **future-aware structured state -> direct planning** mechanisms that does not require a candidate consequence bank.

But the exact role of GraphWorld remains special: it explicitly argues for a compact current relational world state carrying future-relevant semantics instead of explicit multistep rollout.

Current evidence supports a higher-order relationship, not equivalence.

---

## 8. D01.3 blind-set lessons

The blind set is particularly important because it was not built to support the new lineage model.

### GraphAD

Shows that iterative predictive computation is not automatically reciprocal world-policy refinement. This protects SeerDrive from false relatives.

### DriveDreamer

Shows that one paper can contain a world-generation terminal and a world-conditioned action path. Artifact splitting remains necessary, but lineage reconstruction must still ask for the paper-level scientific thesis connecting those modes.

### DrivoR

Shows a strong candidate/scorer mechanism with **no separately predicted future consequence state**. This is a clean negative control against overextending the action-consequence lineage to every candidate resolver.

Thus:

> candidate selection alone is not evidence of world-model consequence reasoning.

This negative control is essential when comparing Drive-JEPA PB, TOAD, Hydra-MDP, WoTE, DA-WAM, and WorldDrive.

---

## 9. D02-W1 methodological re-interpretation

The old D02-W1 family map grouped papers through the frozen R/W/E/L layer. That was appropriate for its historical task, but it must not be reused as proof of research lineage.

The new audit extracts a different lesson from the same papers:

- CRAFT supports training-time compilation of world/counterfactual knowledge;
- GenAD supports joint world-action generation;
- BeTop / UniAD / VAD support future-aware structured-state planning;
- TOAD / Hydra-MDP provide negative controls showing candidate resolution without a world consequence carrier;
- OmniDrive shows that counterfactual supervision alone does not establish online world reasoning;
- DRIVEVLM / ORION show semantic hierarchy before action, but this may be orthogonal to WAM route identity.

This re-use of the corpus is important because it prevents the previous ontology from becoming self-confirming evidence.

---

## 10. Updated genealogy hypotheses

After domain pressure, the following structures have different evidentiary status.

### A. Coupling topology between world modeling and action generation

Status: **strong recurring scientific fork**.

Evidence now spans Epona, DriveLaW, Metis, DrivingGPT, SimWAM, Policy World Model, DriveDreamer, GenAD, DriveFuture, Gen-Drive, and Discrete-WAM.

### B. Action-consequence reasoning

Status: **strong recurring research lineage with unresolved internal branches**.

Evidence now spans World4Drive, WoTE, WorldDrive, Drive-WM, DA-WAM, SafeDrive, RaWMPC, Gen-Drive, Auto-JEPA, and DriveFuture.

Do not collapse all members into one route.

### C. Predictive representation / world-pretraining transfer

Status: **strong recurring learning-transfer lineage**.

Evidence spans LAW, Drive-JEPA, ViDAR, DriveWorld, ReWorld, WA-JEPA and related training-only predictive methods.

Not yet proven to be a standalone planning CoreRoute.

### D. Deployment compilation / residue

Status: **strong cross-cutting lifecycle profile, not a route**.

Evidence spans WorldDrive, DynFlowDrive, Think2Drive, CRAFT, CausalDrive-policy, SimWAM, Metis and other training-only world branches.

### E. Reciprocal world↔planning refinement

Status: **scientifically meaningful but currently singleton / near-singleton**.

SeerDrive remains the strongest case. DriveFuture and GraphAD are near-neighbors but not equivalent on current evidence.

### F. Future-aware structured world state -> direct planning

Status: **recurring higher-order family**.

Evidence spans GraphWorld, OccWorld, Drive-OccWorld, UniAD, BeTop, VAD and GraphAD, but the precise world-model qualification and future-state semantics vary.

### G. Unified representation/task language for world and action

Status: **recurring paradigm, likely cross-cutting rather than a route**.

Discrete-WAM, DrivingGPT, GenAD and some joint generative models provide supporting examples. Shared token/latent language alone does not determine how final planning commitment occurs.

---

## 11. Major correction to the original tree intuition

The domain evidence strengthens the claim that the final scientific object is a **directed idea graph (DAG)** rather than a strict tree.

Examples:

- WorldDrive combines representation inheritance with action-consequence evaluation and distillation;
- Drive-JEPA combines predictive-representation pretraining with a separate multimodal planning/distillation program;
- Gen-Drive combines joint world/ego future generation with learned reward evaluation and optional reward compilation into the generator;
- Discrete-WAM combines unified representation, joint world-policy learning, and hierarchical policy construction.

Therefore a faithful genealogy must support:

- inheritance;
- forks;
- convergence / synthesis;
- compression / distillation;
- bypass / decoupling;
- specialization;
- cross-cutting paradigms.

A strict single-parent hierarchy will lose information.

---

## 12. Current first-principles verdict

### High-confidence conclusions

1. The canonical-12 lineage audit generalizes: broader target-domain papers repeatedly expose the same kinds of scientific disagreements.
2. World/action coupling topology is a serious route-defining candidate and has independent support beyond the canonical 12.
3. Action-consequence reasoning is a real broad lineage, but its internal forks matter and cannot be flattened to `candidate -> future -> score`.
4. Predictive-representation learning is a real recurring lineage, but currently looks more like a learning-transfer family than a unique decision route.
5. Deployment residue / degree of world-model removal is important but cross-cutting; it should not define route identity by itself.
6. Reciprocal world↔planning refinement remains under-replicated and must not be promoted solely because SeerDrive is distinctive.
7. Candidate/resolver topology without a world consequence object is an important negative control; DrivoR, TOAD and Hydra-MDP prevent over-merging candidate planners into WAM consequence planning.
8. The field is better represented as an idea DAG with major forks and synthesis nodes than as a Cartesian product or strict tree.

### Still unresolved

- exact number of CoreRoutes;
- whether coupling topology should itself become the top split or sit below a broader route family;
- how to split the large action-consequence lineage without reproducing implementation-level fake classes;
- whether future-aware structured-state planning and chained generator-latent planning share a common parent;
- whether reciprocal refinement gains independent support in later waves;
- whether predictive-representation lineage should remain purely under Learning/Transfer or participate in top-level route identity.

## 13. Next required step

Do **not** name final routes yet.

The next audit should build a **branch-point ledger**. For each candidate scientific fork, record:

- common ancestor thesis;
- papers on each side;
- the exact bridge that changes;
- within-paper deletion evidence;
- between-paper collapse target;
- negative-control paper;
- whether the distinction survives representation / architecture substitution;
- current status: `PROMOTE-CANDIDATE`, `PROFILE`, `PARADIGM`, `SINGLETON`, or `REJECT`.

Only after that ledger should provisional CoreRoute names be introduced.
