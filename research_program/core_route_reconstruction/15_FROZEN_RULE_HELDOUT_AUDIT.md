# Frozen-Rule Adversarial Held-Out Audit

Status: **PREDICTION-THEN-INSPECTION AUDIT — NOT AN ONTOLOGY SPEC**  
Branch: `research/core-route-reconstruction`  
Date: 2026-09-17  
Frozen rule source: `14_CORRECTED_FACTORISATION_DECISION_TREE.md`

## 0. Purpose

This audit tests whether the factorisation decision tree has predictive value when its rules are frozen **before** detailed full-paper inspection of selected stress cases.

The goal is not a formal statistical blind test. The goal is methodological honesty:

> Predict the expected route outcome under frozen rules, inspect the full paper, record success or failure, and do not rewrite the rule afterward merely to save the prediction.

Selected stress cases:

1. ReWorld — predicted `M0-R` from prior census summary;
2. SafeDrive — predicted `M2`;
3. DriveSuprim — predicted `NOT-WAM-BRIDGE`;
4. iPad — predicted `NOT-WAM-BRIDGE`, with specific pressure on the “iterative != M4” rule;
5. CausalDrive policy post-training — predicted `M0-P`;
6. DriveDreamer action path — predicted `M1`, with M3 as the main alternative risk.

---

## 1. ReWorld — PREDICTION FAILURE

Primary source: `papers/raw_md/P0052_ReWorld/P0052_ReWorld.raw.md`.

### Frozen prediction

`M0-R predictive representation transfer/shaping`.

This prediction followed the earlier D01 summary, which emphasized predictive representation learning transferred into trajectory generation.

### Full-paper finding

The prediction is wrong.

ReWorld explicitly instantiates a **chained latent WAM** following DriveLaW:

- a Video DiT models future scene evolution;
- mid-denoising Video DiT states `F` are retained in the current forward pass;
- Action DiT directly attends to / is conditioned on those video states;
- ReWorld's contribution is to optimize this world-to-action representation pathway more explicitly.

The paper even contrasts this chained path with parallel/shared-output designs.

### Corrected factorisation

`M1-S internal online model/world state -> action`.

The representation-learning objectives are not evidence that the world state is compiled away. They improve an online world-to-action mediator that remains active.

### Why the failure matters

This is the most important result of the held-out audit.

It proves:

1. old census summaries can be too coarse for CoreRoute adjudication;
2. “representation learning” does not imply M0;
3. lifecycle must be reconstructed from the actual forward path;
4. the frozen rule can falsify our prior expectation instead of being stretched to protect it.

### Verdict

**FAIL — useful failure.**

Update required in future projection snapshots:

`ReWorld: M0-R` -> **SUPERSEDED by `M1-S`**.

---

## 2. SafeDrive — PREDICTION PASS, WITH A DOMINANCE LESSON

Primary source: `papers/raw_md/P0002_SafeDrive/P0002_SafeDrive.raw.md`.

### Frozen prediction

`M2 action-conditioned consequence mediation`.

### Full-paper finding

Confirmed strongly.

SafeDrive performs:

1. ProposalNet generates / filters ego trajectory candidates;
2. for each retained candidate, SWNet constructs a separate trajectory-conditioned Sparse World;
3. within each sparse world, ego and surrounding-agent future motions are jointly refined for interaction consistency;
4. FRNet evaluates pair-wise collision risk and time-wise drivable-area compliance;
5. candidate-specific safety results determine final trajectory selection.

Implemented outer factorisation:

`candidate A_k -> sparse world Z(A_k) -> fine-grained safety reasoning -> final commitment`.

### M2 vs M3 dominance test

SafeDrive contains **internal joint ego/agent refinement** inside each candidate-conditioned sparse world.

This does not make the overall route M3.

Why:

- an ego candidate already exists before sparse-world construction;
- that candidate indexes a distinct world branch;
- joint ego/agent refinement happens *inside* `Z(A_k)`;
- final commitment compares/evaluates the candidate-indexed worlds.

Thus the outer bridge is M2.

This yields an important dominance rule:

> Internal joint prediction inside a candidate-conditioned consequence does not override the externally implemented `A_k -> Z(A_k)` factorisation.

### Verdict

**PASS — strong M2 confirmation.**

---

## 3. DriveSuprim — PREDICTION PASS

Primary source: `papers/raw_md/P0022_DriveSuprim/P0022_DriveSuprim.raw.md`.

### Frozen prediction

`NOT-WAM-BRIDGE`.

### Full-paper finding

Confirmed.

DriveSuprim is explicitly a selection-based planner:

- fixed trajectory vocabulary;
- coarse scoring/filtering;
- fine-grained rescoring of hard candidates;
- rotation augmentation;
- self-distillation;
- select highest-scoring trajectory.

There is no separately traceable predictive world/dynamics process producing a future consequence for each candidate.

The safety metrics / teacher labels do not create a world state.

### Why it matters

DriveSuprim is a very strong negative control against the old tendency to treat:

`candidate -> score -> selection`

as inherently close to WoTE / DA-WAM / SafeDrive.

The missing bridge is exactly:

`candidate -> predicted world consequence`.

### Verdict

**PASS — clean NOT-WAM-BRIDGE control.**

---

## 4. iPad — PREDICTION PASS AND M4 NEGATIVE CONTROL

Primary source: `papers/raw_md/P0023_iPad/P0023_iPad.raw.md`.

### Frozen prediction

`NOT-WAM-BRIDGE / adjacent proposal-centric planner`.

Specific stress hypothesis:

> The word “iterative” and proposal-centric prediction must not cause accidental M4 promotion.

### Full-paper finding

Confirmed.

iPad's deployed core is:

- initialize proposal queries;
- repeatedly predict proposals;
- use proposal locations as anchors to gather image features;
- refine proposal queries;
- score final proposals;
- select best trajectory.

It also contains proposal-centric mapping and future-agent/collision-related prediction tasks, but the paper explicitly describes those as **auxiliary tasks during training**.

There is no deployed alternating loop:

`plan -> world state -> revised plan -> revised world state`.

The iteration is internal proposal/feature refinement.

### Why it matters

This is a clean negative control for M4:

- iterative planner != reciprocal world-action route;
- future-agent auxiliary prediction != online world mediator;
- proposal-centric auxiliary tasks != candidate-specific world consequence unless their predicted state is actually consumed in the deployed decision path.

### Verdict

**PASS — strong M4 negative control.**

---

## 5. CausalDrive policy post-training — PREDICTION PASS

Primary source: `papers/raw_md/P0015_CausalDrive/P0015_CausalDrive.raw.md`.

### Frozen prediction

`M0-P imagined/simulated consequences -> policy optimization`.

### Full-paper finding

Confirmed.

CausalDrive is a real-time reactive world renderer / neural simulator conditioned by ego trajectory and sociology prompt. It is used for:

- closed-loop policy evaluation;
- RL post-training through a Video2Reward module;
- human-in-the-loop simulation.

For the policy artifact:

- policy actions are executed inside CausalDrive;
- the simulator generates action-dependent reactive world outcomes;
- Video2Reward / RL turns those outcomes into policy-learning signal;
- the final deployed policy is improved through this simulated interaction program.

The world renderer itself is training / evaluation infrastructure for the policy artifact; it is not required as the final deployed action mediator.

### Correct factorisation

`policy action -> reactive world rollout -> reward/return -> policy update -> deployed policy`.

This is canonical M0-P.

### Mode warning

CausalDrive's simulator mode itself is a **world/simulation terminal**, not an ego planning route.

The M0-P assignment applies specifically to the **policy post-training artifact**.

### Verdict

**PASS — strong independent M0-P replication.**

---

## 6. DriveDreamer action path — PREDICTION PASS, M1/M3 BOUNDARY CLARIFIED

Primary source: `papers/raw_md/P0036_DriveDreamer/P0036_DriveDreamer.raw.md`.

### Frozen prediction

Primary expectation: `M1 world-first / model-state mediation`.

Main alternative risk: the paper's joint video/action training might reveal an M3 co-generation process.

### Full-paper finding

The primary expectation is more faithful.

DriveDreamer second-stage training predicts future video and future action, but the action path is not implemented as one interleaved/co-born world-action sample in the sense of DrivingGPT / GenAD / OccWorld.

The action decoder uses:

- historical actions;
- hidden/world states produced through ActionFormer / video-prediction program;
- pooled multi-scale Auto-DM features;

to generate future driving actions.

Thus the action model causally reads internal world/video-model state.

The variational objective trains video and action prediction together, but joint loss / simultaneous target prediction alone is not sufficient for M3.

### Correct factorisation

`world/video predictive hidden state / Auto-DM features -> future action decoder`.

Best current assignment:

`M1-S internal model-state mediation`.

### Why not M3

- future video and future action are not evidenced as one inseparable joint future sample/process;
- action prediction is explicitly conditioned on world-model internal features;
- there is a mediator direction from world/video computation into action decoding.

### Verdict

**PASS — supports strict M1 vs M3 gate.**

---

## 7. Held-out scorecard

| Case | Frozen prediction | Full-paper result | Outcome |
|---|---|---|---|
| ReWorld | M0-R | M1-S | **FAIL** |
| SafeDrive | M2 | M2 | **PASS** |
| DriveSuprim | NOT-WAM | NOT-WAM | **PASS** |
| iPad | NOT-WAM / not M4 | NOT-WAM / not M4 | **PASS** |
| CausalDrive-policy | M0-P | M0-P | **PASS** |
| DriveDreamer-action | M1, M3 risk | M1-S | **PASS** |

Raw predictive accuracy is not the main goal, but the pattern is useful:

- 5/6 expectations survive full-paper inspection;
- the one failure is scientifically informative and corrects an R1-level census simplification;
- no case requires a sixth world-action causal factorisation.

---

## 8. What was learned from the failure

The ReWorld error exposes a hierarchy of evidence importance:

### Weak clue

“representation learning for WAM” / “predictive representation transfer”.

### Strong route evidence

Actual deployed forward dataflow:

`Video DiT state -> Action DiT`.

Therefore future route reconstruction should privilege the causal forward path over paper-level task labels and secondary summaries.

This rule also explains why:

- Metis remains M0-R: future-video state is deliberately blocked from action inference;
- ReWorld is M1-S: Video DiT state explicitly remains on action inference path.

They can be close genealogically but different mechanistically.

---

## 9. New dominance rule from SafeDrive

A method can contain local sub-computations resembling another motif.

SafeDrive contains joint ego/agent future refinement inside each sparse world.

But the outer implemented program is:

`ego candidate -> its sparse world -> evaluation -> choice`.

Therefore route adjudication should follow the **highest-level causal factorisation that determines how world computation reaches commitment**, while retaining internal submechanisms as profiles/secondary notes.

This prevents nested components from causing uncontrolled multi-label explosion.

---

## 10. Current verdict on the frozen decision tree

The tree survives this adversarial audit with one meaningful correction case and no new factorisation class.

High confidence:

- full forward dataflow must outrank summary labels;
- candidate selection without world consequence remains a clean negative family;
- iterative proposal refinement without world/action alternation is not M4;
- joint training without co-generated world/action future is not M3;
- simulator-based policy optimization is distinct from predictive representation shaping;
- nested joint prediction inside `Z(A_k)` does not erase an M2 outer bridge.

Most important unresolved risk:

> The current five-way spine may still be incomplete because the stress cases were drawn from the known corpus. It now needs a **small, deliberately held-out external/unused target-domain paper set** selected before mechanism inspection, with the frozen decision tree applied unchanged.

Do not broadly expand literature yet. A handful of adversarial cases is more valuable than another shallow census wave.
