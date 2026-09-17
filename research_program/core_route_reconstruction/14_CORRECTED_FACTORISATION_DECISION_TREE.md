# Corrected Factorisation Decision Tree for Future Route Audits

Status: **AUDIT INSTRUMENT — NOT AN ACCEPTED ONTOLOGY**  
Branch: `research/core-route-reconstruction`  
Date: 2026-09-17  
Purpose: freeze the current first-principles decision procedure before additional held-out papers are inspected.

## 0. Why freeze a decision procedure now

The route reconstruction has reached a point where new papers can easily bias the definitions if rules are changed after seeing each case.

This document therefore freezes a **test procedure**, not final route names.

A new paper should first be analyzed ontology-free, then passed through these gates. If it does not fit, record a counterexample. Do not quietly stretch a gate.

---

## 1. Gate A — target planning program

Identify the exact scoped mode that produces the ego planning/control output.

Do not classify an entire paper from:

- a generation demo;
- a simulator mode;
- a pretraining task;
- a joint mode not used for policy deployment;
- a reward/evaluation model attached only externally.

Record supporting modes only if they causally explain how world capability reaches the scoped planner.

---

## 2. Gate B — qualifying world/dynamics object or process

Before route assignment, require a separately traceable predictive/dynamics/world process.

Positive semantic roles include:

- environment/world state;
- temporal transition state;
- predicted future environment consequence;
- joint ego-environment future;
- generative world/model process state;
- learned simulator rollouts used to optimize the deployed policy.

Insufficient by themselves:

- generic current visual feature;
- future ego trajectory / ego-intent latent only;
- action proposal;
- semantic decision token;
- trajectory score or reward scalar;
- perception output with no stateful world/dynamics operation.

A latent is allowed, but its operational semantics must be world/dynamics predictive rather than merely action encoding.

### If Gate B fails

Return:

`NOT-WAM-BRIDGE / ADJACENT CONTROL`.

Do not invent a route.

Current pressure example:

- Auto-JEPA — future ego-intent latent currently pressures this gate rather than proving a new route.

---

## 3. Gate C — does world computation survive on the deployed action path?

### If NO

Enter `M0 compiled world knowledge` and ask **what was compiled**.

#### M0-R — representation/action-feature shaping

Predictive/world objective shapes deployed representation/action model.

Strong anchors:

- LAW;
- Drive-JEPA PF/PB WAM bridge;
- ViDAR;
- ReWorld / WA-JEPA;
- Metis / SimWAM as joint-training + future-bypass realizations.

#### M0-P — policy preference through imagined/simulated consequences

World/simulator rollouts produce returns/advantages for policy optimization.

Strong anchors:

- Think2Drive;
- CRAFT;
- CausalDrive policy post-training.

#### M0-S — world-derived evaluator supervision

World consequence analysis produces target labels/scores for a deployed evaluator.

Strong anchor:

- DynFlowDrive.

Status: early / replication-limited.

If none fits, return `M0-UNKNOWN-COMPILED` and record the new survivor object. Do not force into M0-R/P/S.

### If YES

Proceed to Gate D.

---

## 4. Gate D — implemented online world/action dependency

### D1. Does a qualifying world/model state exist before the final action process and directly condition action?

Pattern:

`O -> Z -> A`.

If yes and no more specific M2/M3/M4 structure dominates:

`M1 WORLD-FIRST MEDIATION`.

Strong anchors:

- DriveLaW — generator internal latent -> Action DiT;
- GraphWorld — relational world state -> planning;
- Policy World Model — explicit future forecast -> action;
- Epona planning — probable shared temporal state -> trajectory generator.

Sublineage note:

- explicit forecast (`M1-F`);
- internal model/world state (`M1-S`).

Do not promote these to separate routes yet.

### D2. Does a provisional ego alternative exist first and instantiate its own world consequence?

Pattern:

`O -> A~_k -> Z(A~_k) -> commitment/refinement`.

If yes:

`M2 ACTION-CONDITIONED CONSEQUENCE`.

Strong M2-EVAL anchors:

- WoTE;
- DA-WAM;
- World4Drive;
- WorldDrive;
- Drive-WM;
- SafeDrive;
- RaWMPC.

Early M2-REFINE anchor:

- DriveFuture.

Negative controls:

- DrivoR;
- TOAD;
- Hydra-MDP;
- Drive-JEPA PB downstream proposal system.

These have candidate selection without candidate-specific predicted world consequence.

### D3. Are world/future and ego-action variables generated as one coupled future process?

Pattern:

`(Z, A) <- G(O)`.

If yes:

`M3 JOINT WORLD-ACTION FUTURE GENERATION`.

Strong anchors:

- DrivingGPT;
- GenAD;
- Gen-Drive;
- Discrete-WAM joint mode;
- OccWorld (full-paper correction).

Strict negative controls:

- Epona: shared state + parallel specialized heads is not sufficient;
- Metis: joint training with future bypass is not sufficient.

Downstream ranking of jointly generated futures does not convert M3 into M2.

### D4. Do world and action update each other repeatedly before/through the planned rollout?

Pattern:

`Z^1 -> A^1 -> Z^2 -> A^2 -> ...`

or equivalent alternating conditionals.

If yes:

`M4 RECIPROCAL / ALTERNATING WORLD-ACTION REFINEMENT`.

Strong independent anchors:

- SeerDrive — iterative mutual future-scene / planning refinement;
- Drive-OccWorld — continuous occupancy forecasting -> planning -> action-conditioned next forecasting -> planning.

Negative controls:

- GraphAD iterative prediction graph without confirmed plan->world->plan alternation;
- DriveFuture future-guided action refinement without independently updated world state loop at current evidence depth.

---

## 5. Dominance / composition rules

A paper may satisfy more than one mechanism.

### Rule 1 — prefer the full higher-order dependency when it genuinely subsumes substeps

Example:

SeerDrive has world->action and action->world steps, but full reciprocal loop is M4.

### Rule 2 — retain independent secondary bridges

Example:

WorldDrive:

- M0-R representation inheritance;
- M2-EVAL online future-surrogate selection.

Both are independently traceable contributions.

### Rule 3 — downstream ordinary planner mechanisms are profiles, not secondary WAM motifs

Drive-JEPA PB:

- WAM bridge = M0-R;
- proposal generation/scoring = downstream planner specialization, not M2.

### Rule 4 — joint future + resolver remains M3 plus ResolverProfile

Gen-Drive:

- joint ego/agent future generation = M3;
- scene evaluator = downstream resolver;
- do not rewrite as M2 unless ego proposal existed before the world consequence branch.

---

## 6. Evidence hierarchy for route adjudication

### Level R3 — full paper + code/implementation path

Best evidence when paper semantics are ambiguous.

### Level R2 — full paper method/formula/dataflow

Sufficient for most route adjudication.

### Level R1 — abstract / mechanism skeleton / secondary summary

Use only for candidate screening and pressure selection.

**New rule after OccWorld / Drive-OccWorld corrections:**

> R1 skeletons cannot establish a new CoreRoute assignment when factorisation is ambiguous.

They may suggest M1/M2/M3/M4, but final route status requires R2 or R3.

---

## 7. Strong-anchor evidence table

| Method/mode | Current motif | Evidence depth | Why it is a strong anchor |
|---|---|---|---|
| LAW | M0-R | full paper | future prediction explicitly used for self-supervised scene/planning representation shaping |
| Drive-JEPA PF/PB WAM bridge | M0-R | full paper | paper separates predictive pretraining from orthogonal multimodal planner program |
| Think2Drive | M0-P | full paper | learned world model is neural simulator for actor/critic imagined rollout training |
| DynFlowDrive | M0-S | full paper | world-dynamics-derived supervision trains scorer; WM explicitly absent at inference |
| DriveLaW | M1-S | full paper | generator internal latent explicitly conditions Action DiT |
| GraphWorld | M1-S | full paper | separately identified relational world state conditions planning without rollout |
| Policy World Model | M1-F | full paper | future states are generated first and explicitly used as planning rationales |
| WoTE | M2-EVAL | full paper | per-trajectory recurrent BEV future -> reward -> selection |
| DA-WAM | M2-EVAL | full paper | explicit one-to-one candidate -> future latent -> scorer |
| World4Drive | M2-EVAL | full paper | intention/candidate-specific future latent -> selector |
| GenAD | M3 | full paper | simultaneous ego/other-agent future generation in one structural latent process |
| DrivingGPT | M3 | full paper | interleaved world/action tokens in one autoregressive driving language |
| Gen-Drive | M3 | full paper | diffusion generates joint ego/agent future scene before evaluation |
| OccWorld | M3 | full paper | autoregressive model jointly predicts scene evolution and ego future |
| SeerDrive | M4 | full paper | paper explicitly proposes bidirectional iterative scene/planning refinement |
| Drive-OccWorld | M4 | full paper | forecast->plan->feed action back->forecast next state continuous loop |

---

## 8. Explicit unresolved cases

### Auto-JEPA

`WORLD-GATE-PRESSURE`: predicted future ego intent may be action representation rather than world state.

### WorldRFT

Current best WAM bridge: M0-R. Current latent naming does not prove online world mediator.

### Epona

M1-S probable; exact runtime temporal-state semantics worth code/path recheck before normative freeze.

### Discrete-WAM policy mode

Do not inherit M3 from joint training mode automatically.

### DriveFuture

M2-REFINE probable; check whether repeated world recomputation upgrades it toward M4.

### M0-S

Mechanism distinct but field replication still thin.

---

## 9. Failure protocol for future held-out papers

When a held-out paper does not fit:

1. do not add a class immediately;
2. write its full world-action computation graph;
3. verify Gate B world qualification;
4. identify exactly which conditional dependency is absent from M0-M4;
5. perform Core-Bridge Deletion Test;
6. search existing corpus for at least one independent analogue;
7. only then propose spine expansion.

A new representation, objective, or architecture without a new dependency structure is **not** a new route.

---

## 10. Freeze statement

For the next held-out audit, the decision rules in this file are frozen.

Allowed outcomes:

- existing motif fits;
- composition of existing motifs fits;
- world/domain gate failure;
- evidence unresolved;
- genuine factorisation counterexample.

Do not revise gates until the held-out case has first been recorded under the frozen rules.
