# Core Mechanism 12 — Phase 3 Ontology Revision Verdict

Status: second-pass verdict. The 21-artifact projection and counterexample audit were completed before the three historical V1 documents were read.

Historical competitors reviewed:

- papers/WAM_ROUTE_MODULE_ABSTRACTION_SAMPLE.md
- papers/WAM_CORE_MECHANISM_SIGNATURE_V1_PROPOSAL.md
- papers/WAM_CORE_MECHANISM_SIGNATURE_V1_STRESS_TEST.md

They are treated as competing hypotheses, not ground truth.

## 1. Final Phase 3 verdict

Retain the seven research questions, but revise five encodings and one comparison relation:

    C – X – D – P – V – T – L

Final Phase 3 status:

| Field | Verdict | Material change |
|---|---|---|
| C carrier | MODIFY | tighten gate; ordinary perception excluded; lifecycle and realization remain modifiers |
| X control interface | MODIFY | bind values to carrier and lifecycle |
| D runtime carrier route | KEEP | categories survive; retain D2/D3 distinction and D4/D5 generation cases |
| P action formation/commitment | MODIFY + MERGE | expand to direct/hierarchical/bank; merge old P2/P3/P4 into bank plus attributes |
| V resolver semantics | MODIFY + SPLIT | semantic target separated from provenance, measure, temporal reference, and composition |
| T clock topology | MODIFY | core stores presence/type; counts become audit parameters |
| L learning program | MODIFY | full ordered graph mandatory; add LG/LN; delete low-information joint-training shortcut |
| equivalence relation | SPLIT | runtime, family, and full core-DAG equivalence |

No entire C–X–D–P–V–T–L question is deleted. None can be merged without recreating a demonstrated collision.

## 2. Revised P after the second-pass completeness test

### 2.1 Failure found

The first-pass P asked only whether an explicit candidate bank reached a resolver. It therefore recorded both an ordinary direct policy and Discrete-WAM’s semantic decision-token→action path as P∅.

The primary Discrete-WAM DAG contains an independently meaningful path×speed decision token that conditions later action-token editing. [PAPER FACT]

This is a semantic action-formation difference, not a hidden-layer implementation detail. The short signature would lose it unless P is widened.

### 2.2 Final P question

How is the action semantically formed and, when alternatives exist, committed to A*?

| Neutral category | Code | Required topology |
|---|---|---|
| Direct/implicit action formation | P∅ | context→action; no independently semantic intermediate decision and no explicit bank/resolver |
| Semantic hierarchical action formation | PH | context→semantic decision/intent→action; the intermediate variable has independently defined semantics |
| Explicit candidate commitment | PB | identity-preserving A{k}→common resolver→A* |
| Unknown action commitment | PU | multimodal/action outputs visible, but final commitment topology is unresolved |
| Not applicable | N/A | generation-only mode has no action commitment task |

Candidate audit attributes:

    prefilter
    postselect_refine
    rescore={yes,no,UNKNOWN}
    candidate_count

They become core only if they add another resolver/commitment stage or change semantic target.

### 2.3 Why this is not old-V1 anchoring

The semantic decision token was already present in the Phase 1 DWAM-POLICY graph and the first-pass projection. The historical A2 category merely exposed that the provisional P signature failed to encode a primary-paper edge. The revision is therefore validated against the pre-existing primary DAG.

## 3. Current-axis verdicts

### 3.1 C — MODIFY

Keep:

- current structured world;
- future endpoint;
- future horizon;
- future generative-process state;
- joint world–action sequence;
- lifecycle and realization modifiers.

Modify:

- require a stateful transition/prediction/relational-update/generative/transport operation;
- require carrier-level temporal/world grounding;
- explicitly exclude ordinary BEV/perception features with only attached detection/map losses.

Do not split WorldDrive’s surrogate into a new temporal class; retain C2 with realization=surrogate.

### 3.2 X — MODIFY

Keep X1–X4 semantics. Require:

    X(carrier@lifecycle)=value

This represents Epona’s @T:X1 and @R:X2 without inventing a hybrid class.

Do not merge with P:

- X describes what indexes a consequence carrier;
- P describes how actions are formed/committed.

### 3.3 D — KEEP

The D templates survive:

- D∅ no runtime carrier influence;
- D1 carrier-conditioned action;
- D2 candidate consequence selection;
- D3 reciprocal within-decision refinement;
- D4 joint world–action generation;
- D5 consequence-generation output.

SeerDrive paper/code and Epona/DriveLaW/GraphWorld jointly prove these are causal-topology distinctions.

### 3.4 P — MODIFY + MERGE

Modify to include semantic hierarchical action formation.

Merge the Phase 2 P2/P3/P4 categories into PB plus ordered attributes. Top-K filtering and non-rescored post-selection refinement fail the semantic-deletion test.

### 3.5 V — MODIFY + SPLIT

Retain semantic atoms:

- VM expert/factual compatibility;
- VU holistic task utility/preference;
- VD decomposed driving outcomes;
- VW world/future fidelity;
- VY dynamics/physical validity;
- VP model confidence.

Delete as standalone atoms:

- geometric trajectory error;
- cross-cycle continuity.

Move them to:

    measure=geometry(...)
    temporal_reference=previous_cycle

Every V record must include:

    compared objects
    semantic atoms
    target provenance
    measure
    composition/weights/order/filter

### 3.6 T — MODIFY

Keep Ts/Tr/Th/Tc. Core values are:

    absent | present | UNKNOWN

Move numerical counts to audit attributes. This makes 5→10 solver steps invariant while endpoint→horizon still changes C and Th.

### 3.7 L — MODIFY

Keep an ordered program:

    stage1 ; stage2 ; … => retain{…}/drop{…}

Keep family macros:

- LP predictive representation transfer;
- LS shared-state sibling multitask;
- LA action-mediated future supervision;
- LT teacher-to-surrogate;
- LC criterion-to-proposal/resolver;
- LQ shared world–action sequence;
- LR reward-based policy optimization.

Add:

- LG generative-carrier pretraining and retained-trunk adaptation;
- LN factual next-state/temporal consistency with explicit stop-gradient target.

Delete any macro that merely says “runtime world and policy were jointly trained” without edge direction. Joint training is a stage/operator plus parameter scope, not a sufficient learning mechanism class.

## 4. Historical route-module verdict

The old A/B/C route narrative is useful as a teaching compression:

- training-only future;
- online future-generative conditioning;
- candidate consequence selection.

Verdict: KEEP as an explanatory view, DELETE as a complete ontology.

Why:

- it correctly foregrounds deployment causality;
- it intentionally suppresses learning, resolver semantics, generation modes, clocks, and paper/code splits;
- SeerDrive D3, Discrete-WAM D4, GraphWorld C1/D1, and direct candidate scorers cannot be fully encoded.

## 5. Historical V1 runtime-axis verdict

### 5.1 Old A final-decision topology

Verdict: MODIFY and MERGE into revised P.

Keep:

- direct action;
- semantic hierarchy;
- explicit candidate bank.

Strength:

- old A2 correctly identifies Discrete-WAM’s semantic decision token;
- old A3 candidate gate is sound.

Modify:

- bind generation-only modes to N/A;
- retain candidate filtering/refinement as attributes unless they introduce another commitment stage.

### 5.2 Old B deployment world carrier

Verdict: MODIFY and MERGE into C.

Mapping:

| Old V1 | Revised field |
|---|---|
| B0 no online carrier | no C@R record; train-only C may still be recorded |
| B1 current world | C1 |
| B2 direct future-derived carrier | C4, with D1 recorded separately |
| B3 endpoint consequence | C2 |
| B4 horizon consequence | C3 |

Add C5 joint world–action sequence and realization modifiers.

Main improvement: old B0 erases training-only carriers, whereas lifecycle-qualified C records preserve them without leaking them into runtime.

### 5.3 Old C world-policy coupling

Verdict: MODIFY and MERGE into D.

Mapping:

| Old V1 | Revised field |
|---|---|
| C0 | D∅ |
| C1 | D1 |
| C2 | D2 |
| C3 | D3 |

Add:

- D4 joint world–action generation;
- D5 consequence-generation output.

### 5.4 Old D resolver semantics

Verdict: MODIFY and MERGE into V.

Mapping:

| Old V1 | Revised V |
|---|---|
| D0 no resolver | V=N/A under P∅/PH/N/A |
| D1 fact/mode compatibility | VM |
| D2a holistic utility | VU |
| D2b decomposed reward | VD |
| D3 world/dynamics consistency | VW and/or VY, with explicit composition |

Historical D was directionally correct, but a single main value cannot faithfully encode DynFlowDrive hybrids or Drive-JEPA PB2’s utility-plus-comfort composition.

## 6. Historical V1 Learning verdict

| Old code | Verdict | Revised treatment |
|---|---|---|
| L1 predictive transfer | KEEP/MODIFY | LP with stage, EMA/freeze, retain/drop |
| L2a action-conditioned auxiliary | KEEP/MODIFY | LA with exact action→carrier→loss gradient |
| L2b sibling co-training | KEEP/MODIFY | LS with shared parameter scope |
| L3 shared world-action backbone | KEEP/MODIFY | LQ; distinguish shared sequence from sibling heads |
| L4 teacher→surrogate | KEEP/MODIFY | LT; require stopgrad/freeze and deployed surrogate |
| L5 criterion→proposal/scorer | KEEP/MODIFY | LC with target provenance |
| L6 next-state consistency | KEEP/MODIFY | LN with stopped target and retained current state |
| L7 runtime joint training | DELETE as standalone class | encode actual edges/stage and retain set |

Add LG and LR.

Why the old unordered Learning set fails:

- WorldDrive requires LT→LC order;
- LP→LC differs from LC→finetune;
- LAW and Metis share LA family but have non-isomorphic parameter/attention/target graphs;
- retain/drop cannot be recovered from a set.

## 7. Historical two-level equivalence verdict

Old V1 used:

- deployment-route equivalence;
- core-mechanism equivalence from Runtime + Learning-set equality.

Verdict: SPLIT.

Final comparison relations:

1. Runtime-equivalent: equal runtime C/X/D/P/V/T after erasing noncausal audit parameters.
2. Mechanism-family-equivalent: runtime-equivalent plus the same ordered L macro family.
3. Core-mechanism-equivalent: full deployment and learning DAGs are typed-graph isomorphic after implementation renaming and erasing noncausal numeric parameters.

The short signature supports levels 1–2. Level 3 always requires canonical DAG comparison.

## 8. Final short-signature form

    Artifact@version/mode
      C = carrier-records(kind@life{realization})
      X = {carrier@life : control-interface}
      D = carrier-to-output route
      P = P∅ | PH | PB{attributes} | PU | N/A
      V = composition(atoms; provenance; compared objects; measure)
      T = (Ts,Tr,Th,Tc) + audit parameters
      L = ordered stages and edges => retain{…}/drop{…}

Compact code:

    C[…]·X[…]·D…·P…·V[…]·T[s…,r…,h…,c…]·L[…]

The compact form is an index. The canonical DAG and evidence boundary remain part of the mechanism record.

## 9. What was retained, merged, demoted, and renamed

Retained:

- seven independent mechanism questions;
- candidate identity gate;
- C carrier temporal types;
- D causal routes;
- four clock domains;
- directed learning families.

Merged:

- P2/P3/P4 into PB plus attributes;
- old A into revised P;
- old B into C;
- old C into D;
- old D into V.

Demoted to attribute/suffix:

- top-K filtering;
- post-selection refinement without rescore;
- candidate count;
- exact solver/horizon/refinement counts;
- geometric distance metric;
- previous-cycle reference;
- representation/backbone/generator family.

Renamed:

- P from “proposal identity and commitment” to “action formation and commitment topology”;
- V from a flat atom choice to a typed resolver-criterion record.

Added:

- PH semantic hierarchy;
- C5 joint world–action sequence;
- D4/D5 generation routes;
- LG and LN learning macros;
- three-level equivalence relation.

## 10. Stability judgment

Current rating: S1+.

Reasons it exceeds bare S1:

- all 21 artifacts are projected;
- mandated internal collisions and invariance tests were run;
- known false encodings were revised rather than hidden;
- old V1 was tested after independent reconstruction and contributed only one primary-DAG-validated completeness fix.

Reasons it does not reach S2:

- SEER-PAPER and GW-PLAN final commitment/resolver remain UNKNOWN;
- four recent works remain source-unverified;
- several gradient/detach boundaries remain unresolved;
- complete equivalence still requires canonical DAGs beyond the short signature;
- no external new-paper blind test exists.

Phase 3 verdict: retain the revised ontology as an S1+ research instrument, not a stable S2 domain map.
