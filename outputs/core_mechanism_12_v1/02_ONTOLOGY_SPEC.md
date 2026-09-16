# Core Mechanism 12 — Phase 2 Ontology Specification

Status: Phase 2 candidate ontology derived from the Phase 1 DAGs. It has not yet undergone the Phase 3 full projection and counterexample audit.

Evidence convention:

- definitions and ontology design choices are OUR INFERENCE;
- supporting observations retain PAPER FACT or CODE FACT;
- unresolved assignments remain UNKNOWN;
- ∅ means verified absence, while N/A means a type constraint makes a field inapplicable.

## 1. Phase boundary

This document performs only Phase 2:

- discover mechanism questions from the 21 frozen artifact/mode DAGs;
- retain a question only when it can vary independently;
- define inclusion gates, neutral semantic categories, codes, decision algorithms, type constraints, nonexamples, and boundary cases;
- define a compact signature that does not replace the underlying DAG.

Not performed here:

- full artifact projection or per-cell evidence citation;
- collision, split, or completeness tests;
- comparison with the old V1 draft;
- first-six human validation.

Those remain Phase 3–5 work.

## 2. Result: a typed seven-field ontology

The smallest candidate representation that preserved the causal distinctions in the 21 graphs is:

    C — qualifying world/consequence carrier
    X — consequence control and branching interface
    D — deployment carrier-to-output causal route
    P — proposal identity and commitment topology
    V — resolver criterion semantics
    T — online clock and iteration signature
    L — directed learning-to-deployment program

Compact signature:

    SIG = C | X | D | P | V | T | L

This is not seven independent dropdowns. C establishes types consumed by X and D; P controls applicability of V; T annotates repeated online edges; L is an ordered graph program rather than an unordered label set. [OUR INFERENCE]

## 3. Why these questions remain separate

| Contrast observed in Phase 1 | Graph facts | Required distinction |
|---|---|---|
| DriveLaW and GraphWorld can both feed an online carrier directly into planning, but one consumes an internal future-generative feature and the other a current structured world state | PAPER FACT; DriveLaW also CODE FACT for the released path | C must be separate from D |
| World4Drive, WorldDrive, WoTE, and released SeerDrive all retain candidate identity and select an action, but use endpoint prediction, a distilled surrogate, or a recurrent horizon and different criteria | PAPER FACT + available CODE FACT | C, P, V, and T cannot be collapsed into “candidate scoring” |
| DynFlowDrive and World4Drive both produce and resolve trajectory candidates; the former deletes its flow world model at runtime while the latter retains candidate-conditioned future prediction | PAPER FACT | P must be separate from D and lifecycle |
| LAW and Epona planning can both lack runtime future influence, while LAW routes future loss through a predicted action and Epona standard visual training uses factual motion with a shared state | PAPER FACT + CODE FACT | L cannot be inferred from D |
| SeerDrive paper and initial code use repeated reciprocal refinement versus score-select-then-refine | PAPER FACT versus CODE FACT | D and P need explicit directed topology |
| Epona controlled rollout and self-generated rollout can emit similar future visuals while being indexed by external versus predicted motion | PAPER FACT + CODE FACT | X must be separate from C |
| Drive-JEPA perception-based v1 and v2 share a proposal bank, but v2 composes current learned score with previous-trajectory comfort | CODE FACT | V and cross-cycle T can vary while P remains fixed |

Counterfactual independence checks:

1. Hold C fixed and change D: an endpoint future state can be a terminal generation output, a candidate evaluator, or an action-refinement input.
2. Hold D fixed and change C: direct conditioning can consume a current structured world or an internal future-generative state.
3. Hold P fixed and change V: the same bank→argmax topology can resolve demonstration compatibility, task utility, decomposed reward, or a hybrid criterion.
4. Hold runtime D at ∅ and change L: future learning may be predictive pretraining, shared-state auxiliary learning, action-mediated supervision, or criterion distillation.
5. Hold D fixed and change T: candidate consequences may be a single endpoint or a multi-step model rollout.

Each field therefore answers a distinct mechanism question. [OUR INFERENCE]

## 4. Common qualification gate: what counts as a world/consequence carrier

A state is admitted to C only if all four tests below pass. [OUR INFERENCE]

| Gate | Required evidence |
|---|---|
| G1 — localizable identity | a separately identifiable tensor, token set, state, query set, or generative-process state exists |
| G2 — world/temporal operator | it is produced, predicted, transitioned, refined, or transported by an operator with explicit scene/world or temporal semantics |
| G3 — semantic grounding | direct world/temporal supervision, a factual future target, a teacher target, or equally explicit algorithmic evidence grounds the state |
| G4 — mechanism interface | it is consumed by planning/generation, or its loss/criterion updates a deployed planning component |

For a RUNTIME carrier, G4 additionally requires that the carrier lie on a causal path to A* or to the declared terminal output of a generation mode. A branch that executes but is not consumed does not qualify as a runtime decision carrier. [OUR INFERENCE]

Verified nonexamples:

- an ordinary encoder hidden state with no explicit world/temporal operator fails G2/G3;
- Drive-JEPA’s deployed V-JEPA feature is not automatically a runtime future carrier merely because its encoder was predictively pretrained; its predictor and target encoder are discarded downstream. [PAPER FACT + CODE FACT]
- multiple trajectory queries do not become world carriers merely because they are called modes or tokens;
- a scalar reward or score is V, not C.

Boundary examples:

- DriveLaW’s early Video-DiT hidden state passes because it is a localizable state inside a future-video generative process, is grounded by video training, and is consumed by Action DiT; decoding pixels is not required. [PAPER FACT + CODE FACT]
- GraphWorld’s structured ego/agent state passes because it is explicitly refined by a world-flow operator, temporally supervised, and injected into motion/planning. [PAPER FACT]
- LAW’s predicted future latent passes at TRAIN but not at RUNTIME because it shapes learning and is not consumed by deployed A*. [PAPER FACT + CODE FACT]

## 5. Axis C — qualifying carrier semantics

### 5.1 Research question

What temporally meaningful world/consequence object exists, and during which lifecycle is it available? [OUR INFERENCE]

### 5.2 Neutral semantic categories

| Neutral category | Semantic input → output | Inclusion threshold |
|---|---|---|
| Absent | no qualifying carrier | the common carrier gate fails, or verified evidence shows no carrier in the specified lifecycle |
| Current structured world | current observations/interactions → explicit current scene/world state | current-time carrier passes G1–G4 and has explicit world structure/refinement or supervision |
| Future endpoint consequence | current context, optionally control → one future/consequence state | output represents a future endpoint or fixed future summary |
| Future horizon consequence | current context, optionally control → ordered future states | carrier preserves at least two modelled physical-horizon positions or recurrent states |
| Future generative-process state | current context/noise → internal state of a future generative process | temporal generative state is consumed before a decoded future is completed |
| Joint world–action sequence | shared context → temporally coupled world and action sequence | world and action elements coexist in one generated/edited sequence with explicit cross-conditioning |
| Unknown | evidence cannot determine carrier type | the carrier may pass the gate, but temporal semantics are not recoverable |

Carrier modifiers:

    life ∈ {TRAIN_ONLY, RUNTIME_ONLY, BOTH, UNKNOWN}
    realization ∈ {DIRECT, DISTILLED_SURROGATE, GENERATIVE_INTERNAL, UNKNOWN}

Multiple carrier records are legal:

    C = carrier_record + carrier_record + …

For example, a current structured world plus candidate future endpoints is represented as two records rather than a new fused class. [OUR INFERENCE]

### 5.3 Code assignment

Codes are assigned only after the semantic names above:

| Semantic category | Code |
|---|---|
| Absent | C∅ |
| Current structured world | C1 |
| Future endpoint consequence | C2 |
| Future horizon consequence | C3 |
| Future generative-process state | C4 |
| Joint world–action sequence | C5 |
| Unknown | CU |

Lifecycle modifiers use @T, @R, @B, and @U. Realization modifiers use {direct}, {surrogate}, {internal}, and {unknown}. These modifiers deliberately avoid the L-axis macro namespace.

### 5.4 Decision algorithm

1. Apply G1–G4 to every candidate state.
2. Reject representation-only hidden states that lack world/temporal grounding.
3. Determine temporal referent: current, one future summary, ordered horizon, internal future process, or joint sequence.
4. Determine lifecycle separately from temporal type.
5. Record direct versus distilled-surrogate realization without changing the temporal category.
6. If evidence proves no carrier, assign C∅; if evidence is insufficient, assign CU.

### 5.5 Nonexamples and boundary rules

- RGB versus BEV versus token versus latent never changes C by itself.
- Regression versus diffusion versus flow never changes C unless the online semantic object changes.
- A distilled future embedding remains the same temporal carrier category as its teacher target, with realization=RS; it is not falsely promoted to a fully simulated world.
- A factual future target used only for loss is TRAIN_ONLY, not runtime foresight.

## 6. Axis X — consequence control and branching interface

### 6.1 Research question

Which semantic variable, if any, controls or indexes the consequence carrier? [OUR INFERENCE]

This field concerns the incoming control edge to a future/joint carrier, not how final actions are selected.

### 6.2 Neutral semantic categories

| Neutral category | Definition |
|---|---|
| No control conditioning | applicable consequence carrier depends on observation/context but no action, intent, or control variable is an input |
| Factual or external control | logged future motion, user-supplied pose/yaw, or another externally fixed control conditions the carrier |
| Predicted single control | one policy-produced action/trajectory conditions the carrier, without a preserved alternative bank |
| Candidate-preserving control | each A{k} conditions F{k} while identity k is preserved |
| Joint/interleaved control | action and world variables are generated or edited together, so neither is merely a fixed upstream condition |
| Unknown | a control edge may exist but source evidence cannot identify it |

### 6.3 Code assignment

| Semantic category | Code |
|---|---|
| No control conditioning | X∅ |
| Factual or external control | X1 |
| Predicted single control | X2 |
| Candidate-preserving control | X3 |
| Joint/interleaved control | X4 |
| Unknown | XU |

If C contains no future or joint carrier to which control could apply, X=N/A. This differs from X∅: X∅ says a relevant carrier exists and is observation-only.

### 6.4 Decision algorithm

1. Locate each incoming edge to the consequence carrier.
2. Classify the source as factual/external control, predicted single control, candidate-indexed control, joint variable, or no control.
3. For candidate-preserving control, verify the same identity k reaches downstream consequence use.
4. If the paper uses factual action during training and predicted action at runtime, record lifecycle-qualified X values rather than merging them.

### 6.5 Nonexamples and boundaries

- A route command that conditions only the policy but not F is not X.
- Random noise seeds are not candidate-preserving control unless sample identity survives to a common resolver.
- Epona factual-pose visual training and self-generated predicted-motion rollout require different X records by lifecycle/mode. [PAPER FACT + CODE FACT]
- Discrete-WAM’s interleaved world-policy generation is joint/interleaved; its policy-only mode has X=N/A if no future carrier is generated. [PAPER FACT]

## 7. Axis D — deployment carrier-to-output causal route

### 7.1 Research question

At deployment, through what directed causal topology does a qualifying carrier change A* or the declared generation output? [OUR INFERENCE]

### 7.2 Neutral topology templates

| Neutral category | Canonical directed path |
|---|---|
| No runtime carrier influence | no qualifying runtime carrier lies on a path to A* |
| Carrier-conditioned action | C_runtime → action generator/decoder → A* |
| Candidate consequence selection | A{k} → F{k} → V{k} → R(k*) → A{k*} |
| Reciprocal within-decision refinement | repeated A{r} → F{r} → A{r+1}, then A* |
| Joint world–action generation | shared/joint process emits coupled A and F, with A becoming A* |
| Consequence generation output | C/F is the terminal generation/simulation output; A* is N/A or externally supplied |
| Unknown | source evidence does not fix the carrier-to-output path |

Legal suffixes:

    + postselect_refine
    + preselect_filter
    × N within-decision rounds

Suffixes are used only when they alter the directed path. [OUR INFERENCE]

### 7.3 Code assignment

| Semantic category | Code |
|---|---|
| No runtime carrier influence | D∅ |
| Carrier-conditioned action | D1 |
| Candidate consequence selection | D2 |
| Reciprocal within-decision refinement | D3 |
| Joint world–action generation | D4 |
| Consequence generation output | D5 |
| Unknown | DU |

### 7.4 Decision algorithm

1. Start at A*; for a generation mode, start at its declared terminal output.
2. Trace ancestors through runtime edges only.
3. If no qualifying C ancestor exists, assign D∅ even if a future branch ran elsewhere.
4. If C feeds one action path without action-indexed consequence selection, assign carrier-conditioned action.
5. If preserved candidates condition F{k} and a resolver commits k*, assign candidate consequence selection.
6. If action and consequence update one another before commitment, assign reciprocal refinement.
7. If world/action variables are jointly generated, assign joint generation.
8. If only a future artifact is emitted and no action is selected, assign consequence generation output.

### 7.5 Nonexamples and boundaries

- Training-time future prediction never creates D1–D4 by itself.
- An ordinary proposal refiner with no qualifying world/consequence carrier is D∅.
- Running a world branch whose output is ignored by A* remains D∅.
- Released SeerDrive is candidate consequence selection plus postselect refinement, not reciprocal refinement, because k* is fixed before refinement and is not rescored. [CODE FACT]
- SeerDrive paper is reciprocal refinement because refined planning features/actions feed the world model again within one decision. [PAPER FACT]

## 8. Axis P — proposal identity and commitment topology

### 8.1 Research question

How are explicit action alternatives created, identity-preserved, reduced, and committed to A*? [OUR INFERENCE]

### 8.2 Candidate admission gate

An explicit candidate bank exists only if:

    alternatives are produced
    → each identity is preserved through relevant computation
    → alternatives reach a common resolver
    → the resolver determines A*

Failure of any step means no verified bank-and-resolve topology. [OUR INFERENCE]

### 8.3 Neutral semantic categories

| Neutral category | Directed topology |
|---|---|
| No explicit bank/resolver | single/implicit output, or multiple samples without a common identity-preserving resolver |
| Bank then commit | A{1…K} → R → A* |
| Bank, filter, then commit | A{1…K} → filter → A{1…K′} → R → A* |
| Bank, commit, then refine | A{1…K} → R(k*) → refine A{k*} → A* |
| Bank, filter, commit, then refine | combines the preceding two ordered operations |
| Unknown | multimodal alternatives are visible but commitment topology is not established |

### 8.4 Code assignment

| Semantic category | Code |
|---|---|
| No explicit bank/resolver | P∅ |
| Bank then commit | P1 |
| Bank, filter, then commit | P2 |
| Bank, commit, then refine | P3 |
| Bank, filter, commit, then refine | P4 |
| Unknown | PU |

### 8.5 Decision algorithm

1. Identify the candidate birth point and candidate key k.
2. Trace k through features, consequences, and scores.
3. Locate the common resolver and prove its output selects A*.
4. Record any hard filtering before resolution and refinement after resolution.
5. If multiple outputs exist but resolver evidence is missing, use PU rather than P1.

### 8.6 Nonexamples and boundaries

- Diffusion samples, flow iterations, or token edits are not a candidate bank unless identity survives to a common resolver.
- Discrete-WAM’s 400 decision labels are a vocabulary/classification interface, not 400 verified trajectory candidates. [PAPER FACT]
- Drive-JEPA’s iterative proposal refinement is not a physical rollout. [CODE FACT]
- A winner-take-all training match does not establish a runtime resolver.

## 9. Axis V — resolver criterion semantics

### 9.1 Research question

What semantic evidence makes one preserved candidate win, and how are multiple criterion semantics composed? [OUR INFERENCE]

V is applicable only when P establishes a runtime resolver.

### 9.2 Neutral criterion atoms

| Neutral atom | Meaning |
|---|---|
| No evaluative criterion | commitment uses a fixed/deterministic rule without candidate evidence |
| Demonstration or mode compatibility | closeness/probability relative to expert/factual behavior or a learned mode label |
| Holistic task utility or preference | scalar task-level quality, simulator score, or pairwise preference |
| Decomposed driving utility | explicit safety, comfort, progress, rule, collision, or related components retained as components |
| World fidelity or dynamics consistency | reconstruction, predictive agreement, stability, or world-dynamics quality |
| Geometric trajectory error | displacement, heading, endpoint, or other direct trajectory discrepancy |
| Cross-cycle continuity | evidence based on a previous executed/simulated/planned trajectory |
| Model confidence or likelihood | probability/confidence not reducible to the atoms above |
| Unknown criterion | resolver exists but semantic target is not established |

Composition is recorded explicitly:

    single(atom)
    weighted_sum(atom:weight, …)
    learned_fusion(atom, …)
    hard_filter(atom) >> score(atom)
    lexicographic(atom, …)
    pairwise_preference(atom)
    UNKNOWN_COMPOSITION

A learned scalar may still encode multiple semantic atoms; dimensionality does not determine semantic purity. [OUR INFERENCE]

### 9.3 Code assignment

| Semantic atom | Code |
|---|---|
| No evaluative criterion | V∅ |
| Demonstration or mode compatibility | VM |
| Holistic task utility or preference | VU |
| Decomposed driving utility | VD |
| World fidelity or dynamics consistency | VW |
| Geometric trajectory error | VG |
| Cross-cycle continuity | VC |
| Model confidence or likelihood | VP |
| Unknown criterion | VX |

If P=P∅, V=N/A. If P=PU and a criterion head is visible but its role in A* is unclear, V may be VX.

### 9.4 Decision algorithm

1. Confirm P contains a runtime resolver.
2. Trace runtime V back to its training targets, simulator outputs, ranking labels, or explicit formulas.
3. Identify semantic atoms from target origin, not from module names such as score head or reward head.
4. Preserve decomposed terms and the composition operator.
5. Distinguish a carrier used as evidence from the criterion target itself.
6. Use VX when a scalar exists but its semantic supervision is unresolved.

### 9.5 Nonexamples and boundaries

- All scalar scores are not one class.
- A world-predicted feature input to a utility head does not automatically make the criterion world fidelity.
- A hybrid training criterion that selects labels for a runtime scorer transfers its semantic atoms to V even if the world model is removed at deployment.
- Previous-trajectory comfort is recorded as cross-cycle continuity plus comfort semantics, not as a future-world rollout.

## 10. Axis T — online clock and iteration signature

### 10.1 Research question

Which distinct update clocks are executed online, and what state does each repeated step advance? [OUR INFERENCE]

### 10.2 Typed product grammar

T is a four-field product rather than a single ordinal class:

    T = (s, r, h, c)

| Field | Neutral clock | State advanced |
|---|---|---|
| s | numerical solver/edit iteration | noise/sample/token estimate; no physical time implied |
| r | within-decision world↔policy refinement | semantic action/world estimate before one commitment |
| h | modelled physical-horizon rollout | predicted world/action state across future horizon positions |
| c | cross-control-cycle dependency | state/evidence carried from a previous control cycle |

Each field takes:

    ∅        verified absent
    1        a single non-repeated update where recording presence matters
    N        repeated; exact count may be parameterized
    UNKNOWN  evidence insufficient

### 10.3 Code assignment

The short codes are Ts, Tr, Th, and Tc. Example syntax:

    T=(Ts:N, Tr:∅, Th:3, Tc:∅)

This states numerical solver repetition and a three-position model horizon; it does not claim three environment interactions.

### 10.4 Decision algorithm

For every loop or repeated block:

1. identify the mutable state;
2. identify the loop termination condition;
3. ask whether the index advances numerical estimation, semantic co-refinement, modelled physical horizon, or actual control cycle;
4. place it in exactly one field unless the implementation contains genuinely nested clocks;
5. record nested clocks independently.

### 10.5 Nonexamples and boundaries

- Transformer depth is not Ts unless layers implement an explicit iterative state-update procedure exposed by the algorithm.
- Diffusion/flow steps are Ts, never Th solely because the model predicts the future.
- SeerDrive paper’s repeated world–planner feedback is Tr. [PAPER FACT]
- WoTE’s recurrent candidate future states are Th. [PAPER FACT + CODE FACT]
- Epona self-rollout can contain nested Ts inside each outer Th step. [PAPER FACT + CODE FACT]
- Drive-JEPA PB2’s previous-trajectory comfort introduces Tc without creating Th. [CODE FACT]

## 11. Axis L — directed learning-to-deployment program

### 11.1 Research question

Through what ordered supervision, gradient, teacher, and deployment-retention program does world/future information alter the deployed planner? [OUR INFERENCE]

L is a program, not a bag of labels.

### 11.2 Program grammar

    Program := Stage (; Stage)* => retain{nodes} / drop{nodes}
    Stage   := pretrain(Edges)
             | joint_train(Edges)
             | distill(Edges)
             | finetune(Edges)
             | policy_optimize(Edges)
    Edges   := Edge
             | Edge || Edge
             | Edge -> Edge

Every edge records:

    source target or loss
    destination parameter scope
    gradient direction
    stopgrad/freeze/EMA if present
    PAPER FACT / CODE FACT / UNKNOWN

### 11.3 Neutral reusable learning patterns

| Neutral pattern | Directed semantics |
|---|---|
| No world/future learning route | no world/future target, teacher, or criterion updates any deployed planning component |
| Predictive representation transfer | future/temporal prediction updates an encoder; predictor/target branch is later dropped and encoder transfers |
| Shared-state sibling multitask | world/future loss and action loss update shared state parameters through sibling heads; no predicted-action→world edge |
| Action-mediated future supervision | predicted action conditions future/world prediction and future loss backpropagates into the action-producing path |
| Teacher-to-surrogate distillation | frozen/heavy teacher produces future/consequence target; deployed surrogate learns it and teacher is dropped |
| Criterion-to-proposal/resolver supervision | world model or simulator produces labels/preferences/selected indices that train deployed proposals or V/R |
| Shared world–action sequence learning | world and action elements are optimized in one coupled sequence/objective with explicit cross-conditioning |
| Reward-based policy optimization | task reward produces advantages/updates for policy after or alongside supervised stages |
| Unknown learning route | a relation is claimed but gradient, stage, or retained scope cannot be established |

### 11.4 Code assignment

| Neutral pattern | Code |
|---|---|
| No world/future learning route | L∅ |
| Predictive representation transfer | LP |
| Shared-state sibling multitask | LS |
| Action-mediated future supervision | LA |
| Teacher-to-surrogate distillation | LT |
| Criterion-to-proposal/resolver supervision | LC |
| Shared world–action sequence learning | LQ |
| Reward-based policy optimization | LR |
| Unknown learning route | LU |

Codes are macros inside an ordered program. They are not mutually exclusive whole-artifact labels.

### 11.5 Decision algorithm

1. Order all training stages chronologically.
2. In each stage, identify target origin: factual future, expert action, simulator, teacher, self-generated context, or reward.
3. Trace gradients to named parameter scopes.
4. Record detach, freeze, no-grad, EMA, and unknown edges explicitly.
5. Determine whether action predicted by the policy conditions the world branch; do not infer this from a shared encoder.
6. At deployment, list retained and dropped nodes.
7. Replace recurring subgraphs with the neutral macro codes only after the full edge graph is recoverable.

### 11.6 Nonexamples and boundaries

- The unordered set {LP, LC} is invalid without stage order and retention.
- Sharing an encoder does not prove action-mediated supervision.
- A world model used only to choose training labels is LC, not runtime D2.
- A frozen teacher and a deployed future surrogate require LT; dropping both teacher and future branch after label creation is LC.
- LAW’s inspected path is an action-mediated boundary example because its predicted waypoint conditions future-latent prediction and the future target is detached. [CODE FACT]
- Epona standard visual training is a sibling-multitask boundary example because factual motion conditions the visual branch while action and visual losses share the MST. [PAPER FACT + CODE FACT]
- Metis is paper-level action-mediated supervision because visual loss is stated to backpropagate through predicted action conditioning; implementation detach details remain UNKNOWN. [PAPER FACT]

## 12. Global type constraints

These constraints prevent legal-looking but causally impossible signatures. [OUR INFERENCE]

1. D2 requires:

       C contains a RUNTIME future/consequence carrier
       X = candidate-preserving control
       P contains a verified bank and resolver
       V ≠ N/A

2. D3 requires at least one runtime action→carrier edge and one carrier→action edge repeated under Tr.
3. D4 requires C to contain a joint world–action sequence and X=joint/interleaved control.
4. D5 permits A*=N/A; P and V are normally N/A unless the generation mode also commits an action.
5. C records marked TRAIN_ONLY cannot justify D1–D4.
6. P1–P4 do not imply a world carrier; direct candidate scoring remains possible with C_runtime=∅ and D∅.
7. V is N/A when P=P∅. V∅ is reserved for an actual resolver with no evaluative evidence, not for no resolver.
8. X is N/A when no future/joint carrier exists. X∅ means an applicable carrier exists but is not control-conditioned.
9. Th does not imply Tr or Tc. A model rollout can occur wholly inside one control decision.
10. Ts never implies physical future progression.
11. L is not derivable from D. The same deployment route may result from different learning programs.
12. A lifecycle conflict is invalid: a node listed in drop{…} cannot appear in a runtime D path unless a separately versioned artifact is created.

## 13. Unified classification procedure

For a new artifact/mode:

1. Freeze paper/code version, task mode, and A* or terminal output.
2. Reconstruct deployment and learning DAGs before assigning codes.
3. Apply the carrier gate and create C records with lifecycle/realization.
4. Inspect incoming control edges and assign X.
5. Trace runtime ancestors of A* and assign D.
6. Run the candidate identity test and assign P.
7. If P has a resolver, trace target semantics and composition to assign V.
8. Classify every online repeated update into T=(s,r,h,c).
9. Serialize the ordered learning graph as L and record retain/drop sets.
10. Run global type constraints.
11. If a fact is absent by evidence, use ∅; if unresolved, use UNKNOWN; if ruled out by type, use N/A.
12. Retain the underlying DAG and evidence citations; the signature is an index, not a replacement.

## 14. Short-signature grammar

Canonical human-readable form:

    Artifact@version/mode
      C = kind@life{realization} [+ …]
      X = control-interface
      D = runtime-route [suffix]
      P = commitment-topology
      V = composition(semantic-atoms)
      T = (Ts, Tr, Th, Tc)
      L = stage(pattern-edges); … => retain{…}/drop{…}

Canonical compact form:

    C[…]·X…·D…·P…·V[…]·T[s=…,r=…,h=…,c=…]·L[…]

Implementation details excluded from the short signature unless they change a typed edge:

- RGB/BEV/token/latent representation;
- CNN/Transformer/DiT backbone;
- regression/diffusion/flow implementation;
- latent dimension, query count, or solver step count.

Those details may remain parameters in an engineering appendix but cannot create core mechanism classes by themselves. [OUR INFERENCE]

## 15. Implementation-invariance thought experiment

Two systems remain equivalent under this ontology if both have:

    candidate-indexed future endpoint carrier at runtime
    candidate-preserving action conditioning
    candidate consequence selection
    bank→resolver commitment
    the same criterion semantics/composition
    the same typed clocks
    isomorphic directed learning and retention program

One may use BEV regression and the other token diffusion. The implementation substitution does not change C–L. [OUR INFERENCE]

They cease to be equivalent if, for example:

- the future branch is dropped and only its labels train a scorer;
- a single action is refined instead of candidates being resolved;
- an endpoint becomes a recurrent physical-horizon rollout;
- utility ranking is replaced by demonstration compatibility;
- world loss changes from shared-state supervision to an action-mediated gradient path.

These are graph changes, not naming changes. [OUR INFERENCE]

## 16. Rejected candidate axes

The following were considered and rejected as core axes at Phase 2:

| Rejected axis | Reason |
|---|---|
| representation substrate | RGB/BEV/token/latent does not independently determine semantic I/O or causal role |
| generator family | regression/diffusion/flow is usually implementation; solver behavior is retained only in Ts |
| backbone family | CNN/Transformer/DiT fails functional relevance and implementation invariance |
| number of candidates | parameter of P, not a new mechanism class |
| number of denoising steps | parameter of Ts, not physical-horizon semantics |
| paper-reported module name | violates anti-marketing and reuse requirements |
| generic “has a world model” boolean | collapses lifecycle, carrier semantics, causal route, and learning transfer |
| generic “has a score” boolean | collapses incompatible resolver semantics and hybrid objectives |

## 17. Phase 2 boundary risks

The ontology deliberately leaves the following for Phase 3 evidence projection and attack:

- whether every C category is needed after all 21 exact projections;
- whether future endpoint and future generative-process state produce any false collision;
- whether criterion atoms are sufficient for every hybrid supervision path;
- whether P3/P4 post-selection refinement should remain a topology category or become a suffix only;
- whether any complete signatures collide while their full DAGs are non-isomorphic;
- whether singleton categories survive the reusable-class test;
- how UNKNOWN final resolvers in SEER-PAPER and GW-PLAN affect P/V projection.

These are testable ontology risks, not facts to fill by intuition.

## 18. Provisional stability and stop gate

The ontology is a Phase 2 candidate only. It has passed internal question-separation and type-consistency reasoning, but it has not passed mandatory artifact projection, collision, split, invariance, lifecycle, candidate-identity, hybrid-objective, version/mode, completeness, or anti-marketing tests.

Therefore:

- it is not yet justified as S2;
- no final domain-understanding claim is made;
- Phase 3 is required before stability can be rated above a provisional S1 ceiling.

Work stops here pending explicit approval for Phase 3.
