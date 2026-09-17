# Living First-Principles Audit — Continuation

Status: **APPEND-ONLY RESEARCH MEMORY — NOT AN ONTOLOGY SPEC**  
Parent log: `00_LIVING_FIRST_PRINCIPLES_AUDIT.md`  
Continuation starts: 2026-09-17  
Scope: preserve high-value reasoning changes after Section 23 of the parent log.

This continuation exists because the detailed reconstruction work expanded into dedicated audit files. The detailed files remain the evidentiary record; this file records the **evolution of judgment** so later work can recover why the project changed direction.

Future major route/ontology judgments should be appended here (or a subsequent continuation chunk if this file becomes operationally unwieldy), while detailed case evidence belongs in the numbered audit files.

---

## 24. Major shift: from paper genealogy to implemented world-action causal factorisation

### Observation

Canonical-12 genealogy and broader-corpus pressure showed that research lineage alone cannot define mechanism routes.

Examples:

- Epona, DriveLaW, and Metis are close intellectual siblings because they debate world/action coupling, yet they deliberately choose different deployed information paths.
- Drive-JEPA PF and PB have different downstream planner topology but preserve the same predictive-representation WAM bridge.
- WorldDrive combines more than one bridge and cannot be faithfully represented by one mutually exclusive label.

### Prior assumption challenged

> A hierarchical research genealogy itself may become the route taxonomy.

### New hypothesis

A major route should primarily be defined by the **implemented causal factorisation** through which world-model computation changes planning.

Working motifs emerged:

- `M0`: world knowledge is compiled into deployed components through learning;
- `M1`: online world/model state is formed first and conditions action (`O -> Z -> A`);
- `M2`: provisional ego action indexes a consequence that changes commitment (`O -> A~ -> Z(A~) -> A*`);
- `M3`: world and ego action are generated as coupled variables of one future process (`(Z,A) <- G(O)`);
- `M4`: world and action alternately revise one another before/through planning (`Z -> A -> Z -> A ...`).

These are reconstruction motifs, not accepted CoreRoute names.

### Confidence

High that causal factorisation is a better discovery object than flat R/W/E/L axes.

Detailed records:

- `05_MINIMAL_BRANCH_RECONSTRUCTION.md`
- `06_ADVERSARIAL_MOTIF_REGRESSION.md`
- `11_M3_JOINT_GENERATION_AND_FACTORISATION_AUDIT.md`
- `12_REVISED_MINIMAL_CAUSAL_SPINE_SYNTHESIS.md`

---

## 25. BP-03 and BP-07 were redundant views of one deeper fork

Earlier branch-point work separately considered:

- action-consequence reasoning;
- direct world/future-state conditioning vs candidate-specific consequence evaluation.

Deeper reconstruction showed these are largely the same causal fork:

### World-first

`O -> Z -> A`

### Action-indexed consequence

`O -> A~ -> Z(A~) -> A*`

The key question is not merely whether the system has candidates or future states. It is **which variable must exist first to instantiate the decision-relevant world state**.

This correction substantially simplifies the branch structure.

Status: **SUPERSEDES treating BP-03 and BP-07 as independent peer axes.**

---

## 26. M0 cannot repeat the old W0 mistake

### Observation

Many papers remove explicit world computation before deployment, but the surviving learned object differs materially.

### Reconstruction

#### M0-R — predictive representation / action-feature shaping

World prediction shapes the representation or action model.

Strong examples:

- LAW;
- Drive-JEPA;
- ViDAR;
- WA-JEPA;
- Metis / SimWAM as future-bypass realizations.

#### M0-P — simulated/imaged consequence policy optimization

World/simulator interaction produces returns/advantages that optimize policy preference.

Examples:

- Think2Drive;
- CRAFT;
- CausalDrive policy post-training.

#### M0-S — world-derived evaluator supervision

World consequence analysis teaches a deployed scorer/evaluator.

Strong anchor:

- DynFlowDrive.

### Important reversal

A previous idea treated “joint world/action training + future branch bypass” as an independent M0 route. This was degraded to a Learning/Coupling Profile: Metis/SimWAM still primarily transmit world knowledge by shaping the deployed representation/action model.

Detailed record: `08_M0_COMPILED_WORLD_SUBBRANCH_AUDIT.md`.

---

## 27. M2 became the strongest mature field-level ancestor

### Shared indispensable bridge

`candidate / intention / provisional action -> candidate-specific consequence -> final selection/refinement`.

Independent strong anchors include:

- World4Drive;
- WoTE;
- WorldDrive;
- DA-WAM;
- Drive-WM;
- SafeDrive;
- RaWMPC.

### Clean negative controls

- DrivoR;
- TOAD;
- Hydra-MDP;
- Drive-JEPA PB;
- DriveSuprim;
- iPad (for its deployed route).

These controls may have candidates and scorers but do not instantiate a deployed candidate-specific world consequence.

### Internal branch result

`M2-EVAL` is mature: consequence evaluates already identifiable alternatives.

`M2-REFINE` is plausible but under-replicated: consequence participates inside the action solver/refinement process (DriveFuture anchor).

### Important non-route distinctions

The following failed to justify top-level route splits at current evidence:

- endpoint vs horizon;
- explicit BEV/video rollout vs compact latent vs distilled surrogate;
- plausibility vs reward vs safety criterion;
- candidate generator type.

These remain profiles/sublineages unless later evidence changes the causal bridge.

Detailed record: `09_M2_ACTION_CONSEQUENCE_SUBBRANCH_AUDIT.md`.

---

## 28. Strict M1 gate: “world-pretrained feature” is not an online world state

M1 risks swallowing every predictive representation method.

A strict online mediator gate was therefore introduced:

- runtime-localizable state;
- stateful predictive/dynamics/generative operation beyond ordinary encoding;
- planner causally reads the state;
- online mediator is indispensable to the WAM bridge;
- if only parameters/features survive after prediction training, prefer M0;
- if ego candidate indexes the state, prefer M2;
- if world/action are co-generated, test M3 first.

Strong M1 examples:

- DriveLaW — Video DiT internal state -> Action DiT;
- GraphWorld — relational world state -> planning;
- Policy World Model — explicit future forecast -> action;
- Epona — probable shared temporal world state -> trajectory generation.

Sublineages:

- `M1-F`: explicit forecast as planning intermediate;
- `M1-S`: internal online model/world state as planning state.

Current judgment: real distinction, not yet proven to require separate top-level CoreRoutes.

Detailed record: `10_M1_WORLD_FIRST_MEDIATION_AUDIT.md`.

---

## 29. Major evidence correction: OccWorld is M3-like, not clean M1

### Previous shallow interpretation

D01 skeleton compressed OccWorld as future occupancy supporting planning, suggesting M1.

### Full-paper finding

OccWorld's GPT-like world model jointly predicts:

- future scene/occupancy tokens;
- ego movement / ego tokens.

The paper explicitly formulates simultaneous surrounding-scene evolution and ego-motion forecasting.

### New judgment

OccWorld is stronger evidence for `M3 joint world-action/world-ego future generation`.

### Methodological lesson

> R1 mechanism skeletons may select pressure cases, but cannot establish a CoreRoute factorisation when the full generative structure is ambiguous.

This correction is deliberately preserved rather than rewriting the historical D01 artifact.

Detailed records:

- `10_M1_WORLD_FIRST_MEDIATION_AUDIT.md`
- `11_M3_JOINT_GENERATION_AND_FACTORISATION_AUDIT.md`

---

## 30. Strict M3: joint training is not joint future generation

M3 is now defined by co-generation / co-birth of world and ego-action variables inside one coupled future process.

Strong anchors:

- DrivingGPT — interleaved visual/action autoregressive driving language;
- GenAD — ego and surrounding-agent futures generated together;
- Gen-Drive — joint multi-agent including ego future scenes generated before evaluation;
- Discrete-WAM joint world-policy mode;
- OccWorld — joint future scene + ego generation.

Important negatives:

- Epona: shared temporal latent + parallel specialized heads is insufficient;
- Metis: joint training with action masked from future-video tokens is insufficient.

### Key M2 vs M3 distinction

M2 asks:

> “If ego does this candidate action, what world consequence follows?”

M3 asks:

> “What coherent joint future, including ego behavior and world/agents, is generated together?”

Downstream ranking of an M3 joint sample does not turn it into M2.

Detailed record: `11_M3_JOINT_GENERATION_AND_FACTORISATION_AUDIT.md`.

---

## 31. Major evidence correction: Drive-OccWorld independently replicates M4

### Previous shallow interpretation

D01 compressed Drive-OccWorld to occupancy forecast -> planner, suggesting M1.

### Full-paper finding

Drive-OccWorld explicitly performs continuous alternation:

1. world model forecasts next occupancy/flow state;
2. planner selects next trajectory using that predicted state;
3. selected trajectory is fed back as action condition;
4. world model predicts the following state;
5. planning repeats.

### Consequence

M4 is no longer a SeerDrive-only singleton.

Strong anchors now include:

- SeerDrive — iterative mutual future-scene/planning refinement;
- Drive-OccWorld — continuous forecasting/planning alternation.

The implementations differ, but both instantiate repeated world/action conditional updates.

### Current status

M4 upgraded from singleton extension to **major branch candidate**.

Detailed record: `13_COUNTEREXAMPLE_HUNT_AND_SPINE_CORRECTIONS.md`.

---

## 32. Auto-JEPA exposed a domain/world-object gate problem, not a sixth route

Auto-JEPA predicts a continuous **future ego-motion intent latent** and uses it to retrieve trajectories.

This is dangerous for scope:

If future action/trajectory latents automatically count as “world state,” almost any advanced action predictor can become a world model.

Current judgment:

`WORLD-GATE-PRESSURE / ACTION-LATENT PREDICTIVE PLANNER`.

Before M0-M4 projection, require a qualifying world/dynamics object/process such as:

- environment/world state;
- transition/dynamics state;
- predicted world consequence;
- joint ego-environment future;
- generative world process state.

Action intent, generic visual feature, decision token, or scalar reward alone are insufficient.

This recovers the useful gate discipline of the earlier C-carrier work without restoring R-W-E-L as the discovery ontology.

Detailed record: `13_COUNTEREXAMPLE_HUNT_AND_SPINE_CORRECTIONS.md`.

---

## 33. Frozen decision tree and evidence hierarchy

To prevent definitions drifting after each new paper, the route audit procedure was frozen before adversarial test cases.

Decision order:

1. scope exact planning mode;
2. pass world/dynamics object gate;
3. determine whether relevant world computation remains online;
4. if compiled -> M0 subbranch;
5. if online, inspect implemented world/action conditioning order:
   - world-first -> M1;
   - ego alternative -> consequence -> action -> M2;
   - coupled joint future -> M3;
   - repeated alternation -> M4.

Evidence depth:

- R3: full paper + code path;
- R2: full paper method/formula/dataflow;
- R1: abstract / skeleton / secondary summary.

New rule:

> R1 cannot establish a new CoreRoute assignment where factorisation is ambiguous.

Detailed record: `14_CORRECTED_FACTORISATION_DECISION_TREE.md`.

---

## 34. Frozen-rule audit produced an intentional prediction failure: ReWorld

### Frozen prediction

Based on D01 summary: `ReWorld -> M0-R predictive representation transfer`.

### Full-paper result

Prediction failed.

ReWorld directly follows a DriveLaW-like chained WAM:

- Video DiT mid-denoising states are retained in the current forward pass;
- Action DiT directly conditions on those states;
- ReWorld explicitly optimizes this online world-to-action latent pathway.

### Corrected judgment

`ReWorld -> M1-S`, with representation learning improving the mediator rather than compiling it away.

### Why this failure is valuable

The frozen method allowed the evidence to falsify our expectation instead of changing the rule to preserve a clean score.

It sharply distinguishes ReWorld from Metis:

- ReWorld keeps Video-DiT state on action path -> M1;
- Metis blocks future-video dependency at action inference -> M0-R.

Detailed record: `15_FROZEN_RULE_HELDOUT_AUDIT.md`.

---

## 35. SafeDrive established an important motif-dominance rule

SafeDrive:

- ego proposals exist first;
- one separate sparse world is constructed for each proposal;
- within each sparse world, ego and surrounding-agent futures are jointly refined;
- fine-grained safety reasoning selects the final trajectory.

The internal joint ego/agent prediction resembles M3 locally.

But the outer implemented factorisation is:

`A_k -> Z(A_k) -> evaluate -> A*`.

Therefore M2 dominates.

### New rule

> Classify by the highest-level causal factorisation that determines how world computation reaches commitment; retain nested submechanisms as secondary notes unless they are independent bridges.

This prevents uncontrolled multi-label explosion.

Detailed record: `15_FROZEN_RULE_HELDOUT_AUDIT.md`.

---

## 36. Iterative planning is not M4: iPad as a clean negative control

iPad repeatedly predicts/refines trajectory proposals and uses proposal-centric future-agent/collision auxiliary prediction.

However:

- future-agent/collision prediction is described as an auxiliary training task;
- deployment iterates proposal/feature refinement;
- no deployed plan->world-update->revised-plan->world-update loop exists.

Therefore iPad is not M4 and currently does not establish a qualifying WAM bridge.

This is a strong negative control against keyword-based route assignment.

Detailed record: `15_FROZEN_RULE_HELDOUT_AUDIT.md`.

---

## 37. Current route hypothesis snapshot after frozen-rule audit

Current working causal spine:

```text
World-model contribution to one-stage planning
|
|-- M0  compiled into deployed decision system
|     |-- M0-R representation/action-feature shaping
|     |-- M0-P imagined/simulated return -> policy preference
|     |-- M0-S world-derived evaluator supervision [replication-limited]
|
|-- M1  world/model state first -> action
|     |-- explicit forecast mediator [profile/sublineage]
|     |-- internal model/world state mediator [profile/sublineage]
|
|-- M2  ego alternative first -> candidate-specific consequence -> action
|     |-- M2-EVAL [mature]
|     |-- M2-REFINE [early]
|
|-- M3  world + action generated as one coupled future process
|
|-- M4  repeated world/action alternation
```

This is **not an accepted ontology**.

It is the first causal spine that has so far survived:

- canonical genealogy reconstruction;
- broader-corpus pressure;
- false-merge / false-split audits;
- full-paper corrections;
- a frozen-rule adversarial test including a genuine failed prediction.

### What remains unresolved

- external/unused held-out validation against papers not already involved in route discovery;
- M0-S replication;
- M1 leaf structure;
- M2-REFINE replication;
- exact M3 world-object gate;
- whether M4 has additional independent examples;
- whether the final human representation should expose this as a tree/DAG, route names, or factorisation notation.

### Current discipline

Do not rename these motifs into polished CoreRoute labels yet.

Next high-value step:

> select a small adversarial held-out target-domain set **before method inspection**, freeze it, and apply `14_CORRECTED_FACTORISATION_DECISION_TREE.md` unchanged. A sixth route may only be introduced if one held-out paper demonstrates a genuinely new implemented world-action dependency that cannot be represented as M0–M4 or their composition.
