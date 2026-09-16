# Core Mechanism 12 — Phase 3 Collision and Counterexample Audit

Status: ontology attack completed before reading the old V1 drafts, then corrected after the independent first-six human review. The semantic decision→action correction and later evidence corrections are traced in `05_ONTOLOGY_REVISION_VERDICT.md` and `08_FIRST_SIX_HUMAN_REVIEW_VERDICT.md`.

## 1. Executive audit result

The seven research questions remain useful, but the Phase 2 encoding does not survive unchanged.

Passes:

- C and D are separately necessary.
- X and P are not duplicates.
- D1/D2/D3/D4/D5 are causally distinct.
- the four clock domains are necessary.
- L must remain an ordered directed program.

Required revisions:

- tighten the C gate so ordinary perception states cannot qualify;
- lifecycle-qualify X;
- merge P2/P3/P4 into PB plus ordered audit attributes, while expanding P to encode semantic action hierarchy;
- restructure V into semantic target atoms plus provenance/measure/composition;
- remove geometric error and cross-cycle reference as standalone V atoms;
- make T core topology-only and move counts to audit parameters;
- add generative-carrier transfer as an L family macro;
- define graded equivalence relations so shared short signatures do not overclaim full-DAG equivalence.

Overall result: S1+, not S2. The ontology is now internally sharper, but unresolved final resolvers and unavailable source for four works still block a full completeness claim.

## 2. C-axis carrier attack

### 2.1 Failure found in the Phase 2 G1–G4 wording

The original G2 allowed a state produced by an operator with “scene/world semantics,” and G3 allowed attached detection/map supervision. Taken literally, an ordinary BEV perception feature consumed by planning could pass G1, G3, and G4, while a loose reading of “scene operator” could pass G2. That would falsely turn standard perception into a world carrier. [OUR INFERENCE]

### 2.2 Revised carrier gate

A carrier must pass all four revised tests:

1. Localizable identity: a separately traceable state exists.
2. Stateful world operation: beyond encoding, the state participates in at least one explicit transition, temporal prediction/consistency, structured entity-relation update with temporal identity, generative dynamics operation, or world-state transport.
3. Carrier-level grounding: supervision/teacher evidence targets the carrier’s world/temporal semantics itself; losses merely attached to a shared feature do not suffice.
4. Mechanism interface: the carrier reaches planning/output, or its loss/criterion updates a deployed planning component.

Additional exclusion:

    detection/map supervision + planner consumption
    without a stateful world operation
    = ordinary perception state, not C1

### 2.3 Mandatory counterexamples

| Case | G1 | Revised G2 | Revised G3 | G4 | Result | Why |
|---|---:|---:|---:|---:|---|---|
| ordinary perception/BEV state | yes | no | no at carrier level | yes | excluded | encoding plus attached perception heads is not a world transition |
| GraphWorld structured current world | yes | yes | yes | yes | C1 | ECIG/GRU relational state, flow transport, stopped temporal target, planning interface [PAPER FACT] |
| DriveLaW future-generative hidden state | yes | yes | yes | yes | C4 | internal Video-DiT future process, video training, Action-DiT consumption [PAPER FACT + CODE FACT] |
| World4Drive candidate future latent | yes | yes | yes | yes | C2 | A{k}-conditioned future state, factual-future alignment, selector input [PAPER FACT + CODE FACT] |

Additional tests:

- World4Drive needs two C records: C1 for its physical current latent and C2 for F{k}. Merging them would erase transition direction. [OUR INFERENCE]
- WorldDrive’s deployed surrogate remains C2 with realization=surrogate. A new carrier class is unnecessary because semantic input/output and temporal referent remain a candidate future endpoint. [OUR INFERENCE]
- Factual future targets are C@TRAIN_ONLY and cannot support runtime D. [OUR INFERENCE]
- Drive-JEPA’s deployed encoder feature is not C_runtime. Its future predictive target is C2@TRAIN, while predictor/target encoder are dropped. [PAPER FACT + CODE FACT]

Verdict: C=MODIFY gate; keep carrier categories.

## 3. X-axis control/branching attack

### 3.1 Mutual exclusivity

X1/X2/X3/X4 are mutually exclusive per incoming carrier edge in one lifecycle and training stage:

- X1: fixed external/factual control;
- X2: one policy-predicted control;
- X3: candidate-keyed control with preserved k;
- X4: joint/interleaved variables.

They are not necessarily exclusive across lifecycle or training stage. Epona is the decisive counterexample: base training uses factual motion X1, periodic chain-of-forward training uses detached predicted motion X2, and runtime may use predicted X2 or external X1 depending on mode. [PAPER FACT + CODE FACT]

Required syntax:

    X(C2@T,base)=X1
    X(C3@T,chain)=X2
    X(C3@R,self)=X2

If multiple carriers exist, bind X to the carrier record:

    X(C2@T)=X1
    X(C3@R)=X2

Lifecycle-only shorthand is invalid when two carriers share a lifecycle. For example, W4D must record `X(C1@B)=N/A` and `X(C2@B)=X3`; writing only `@B:X3` falsely suggests that the current-state carrier itself is candidate-indexed.

Stage-only shorthand is also invalid when one carrier architecture receives different controls in different training stages. WorldDrive requires `X(C2_teacher@T,pretrain)=X1` and `X(C2_teacher@T,FAR)=X3`.

### 3.2 X versus P

No duplication was found:

- DFD has X3@TRAIN but its runtime world carrier is removed; PB still exists at runtime through the distilled scorer.
- Drive-JEPA PB has PB but X_runtime=N/A because no runtime consequence carrier exists.
- W4D has both X3 and PB because candidate actions index consequences and later reach a resolver.

Thus X describes an incoming edge to C; P describes commitment among actions.

### 3.3 Route/command exclusion

A route command that conditions only the policy is not X. X is assigned only if the route/intent/control directly indexes a qualifying consequence/joint carrier.

Verdict: X=MODIFY syntax, otherwise KEEP.

## 4. D/P deployment-topology attack

### 4.1 D mutual-exclusivity tests

| Pair | Separating condition | Result |
|---|---|---|
| D1 vs D2 | D2 requires A{k}→F{k} plus a common resolver; D1 has carrier→one action path without candidate consequence commitment | distinct |
| D2 vs D3 | D3 feeds consequence/refined action back into another world–policy round before commitment; D2 resolves candidates once | distinct |
| D3 vs D4 | D3 alternates typed action/world updates; D4 jointly generates/edits one shared sequence | distinct |
| D1 vs D5 | D1 ends in planning A*; D5 ends in generated consequence and may have A*=N/A | distinct |

Required examples:

- Epona self-rollout: D5, nested Ts+Th. [PAPER FACT + CODE FACT]
- DriveLaW: D1 with C4 future-generative hidden conditioning. [PAPER FACT + CODE FACT]
- GraphWorld: D1 with C1 current structured world modulation. [PAPER FACT]
- SeerDrive paper: D3 because A{r}→F{r}→A{r+1} repeats. [PAPER FACT]
- SeerDrive code: D2; score/select precedes one selected-trajectory refinement and k* is not rescored. [CODE FACT]

### 4.2 Candidate identity test

PB is admitted only when all four are proven:

    candidate birth
    → identity preservation
    → common resolver
    → resolver determines A*

Rejected as PB:

- random diffusion samples without a common resolver;
- token-edit iterations;
- flow solver states;
- proposal-refinement layers;
- 400 supervised decision labels;
- winner-take-all training assignment without runtime commitment.

### 4.3 P2/P3/P4 deletion counterfactuals

| Phase 2 category | Remove tested step | Does semantic resolver change? | Does criterion target change? | Core verdict |
|---|---|---:|---:|---|
| P2 bank→filter→commit | remove WorldDrive top-K filter while keeping same reward and argmax | no; search support/compute changes | no | merge into PB; record prefilter attribute |
| P3 bank→commit→refine | remove released SeerDrive selected-path refinement | final geometry may change, but k* and resolver semantics do not | no | merge into PB; record postselect_refine |
| P4 filter+commit+refine | remove either engineering step while preserving resolver | commitment semantics unchanged unless evidence shows rescore/re-entry | no in current set | merge into PB; keep ordered attributes |

Rescore rule:

- if refinement is followed by a new shared resolver, it creates another commitment stage and must be represented in the core P graph;
- if no rescore occurs, refinement is an audit suffix.

### 4.4 Semantic hierarchy completeness correction

The first-pass P only distinguished no bank from bank→resolver. That loses Discrete-WAM’s independently semantic path×speed decision token:

    context → semantic decision token → action-token editing → A*

The token is not a candidate bank, but it is also not an ordinary hidden layer. Final P therefore becomes:

- P∅ direct/implicit action formation;
- PH semantic decision/intent→action;
- PB explicit bank→resolver;
- PU unknown;
- N/A no action commitment task.

This correction was noticed during the second-pass historical comparison, then accepted only because the primary DWAM-POLICY DAG already contained the missing semantic edge.

Verdict: D=KEEP; P=MODIFY, expand with PH, and MERGE P2/P3/P4 into PB+attributes.

## 5. V-axis semantic attack

### 5.1 Failure of the Phase 2 atom list

Demonstration compatibility and geometric trajectory error are not mutually exclusive semantic peers.

Example:

    compare candidate trajectory to factual expert trajectory
    using L2/ADE/FDE

The semantic target is expert/factual compatibility. Geometry is the measure. Treating both VM and VG as coequal atoms double-encodes one fact. [OUR INFERENCE]

Likewise, previous-cycle reference is a temporal provenance attribute. In Drive-JEPA PB2, the semantic criterion is comfort, while the referent comes from a previous cycle. VC as a standalone atom would duplicate VD[comfort] and Tc.

### 5.2 Revised V record

    V = composition(
          semantic atoms,
          target provenance,
          compared objects,
          measure,
          weights/order/filter
        )

Retained semantic atoms:

- VM expert/factual behavior compatibility;
- VU holistic task utility/preference;
- VD decomposed driving outcomes;
- VW world/future fidelity;
- VY dynamics/physical validity;
- VP model confidence/likelihood;
- VX known resolver with unknown criterion semantics.
- UNKNOWN resolver applicability and/or criterion not established.

Demoted attributes:

- geometric error → measure;
- cross-cycle continuity → temporal_reference/provenance, while Tc records clock dependency.

### 5.3 Required artifact tests

| Artifact | Compared objects | Semantic atoms | Measure/provenance | Composition | Information preserved? |
|---|---|---|---|---|---|
| World4Drive | candidate future latent vs factual future latent | VW | latent MSE creates target class j; separate trajectory L1 shapes T{j} | single learned score | yes; ScoreNet's label is future-world agreement, not nearest trajectory geometry |
| WorldDrive | candidates vs simulator/oracle planning outcomes | VU | PDMS ordering; pairwise preference | pairwise_preference(VU) | yes |
| WoTE | candidate rollout/outcome vs imitation and simulator component labels | VM + VD | logged expert plus safety/comfort/progress-related labels | learned/weighted fusion; exact formula bounded | yes |
| Drive-JEPA PB2 | current candidate vs EPDMS, and candidate vs previous-cycle trajectory comfort | VU + VD[comfort] | EPDMS plus previous-cycle temporal reference | (14·VU+2·comfort)/16 | yes |
| DynFlowDrive | candidate future vs factual future; candidate trajectory vs factual; flow path stability | VW + VM + VY | reconstruction, geometric expert-match measure, angular stability | hybrid winner criterion; exact sign/weights UNKNOWN | yes with UNKNOWN composition |

### 5.4 Scalar-output invariance

Two learned scalar heads remain different if their target provenance differs. Conversely, a decomposed vector later summed remains VD with a recorded composition; vector dimensionality alone does not create a class.

Verdict: V=MODIFY; delete VG and VC as standalone atoms, retain them as typed attributes.

## 6. T-axis clock and implementation-invariance attack

### 6.1 Core versus audit parameter

The Phase 2 values 1/N risk making solver count part of the core signature. This fails implementation invariance.

Revised core:

    Ts,Tr,Th,Tc ∈ {absent,present,UNKNOWN}

Audit parameters:

    solver_steps
    refinement_rounds
    model_horizon_steps
    previous_cycle_lag

### 6.2 Mandatory invariance replacements

| Replacement | Semantic I/O unchanged? | Causal topology unchanged? | Core T change? | Audit change? |
|---|---:|---:|---:|---:|
| diffusion 10→20 steps | yes | yes | no; Ts remains present | yes |
| flow solver 5→10 steps | yes | yes | no | yes |
| token editing 3→6 rounds | yes | yes | no | yes |

### 6.3 Clock separation

| Repetition | Core field | Not equivalent to |
|---|---|---|
| network depth | none by default | solver or semantic loop |
| diffusion/flow/token solver | Ts | physical horizon |
| world↔policy reciprocal update | Tr | generic solver |
| predicted physical future sequence | Th | environment interaction |
| state from previous control tick | Tc | model horizon |

Verdict: T=MODIFY value grammar; keep four clock fields.

## 7. L-axis directed-program attack

### 7.1 Required program comparisons

| Artifact | Ordered program | Gradient/retention distinction |
|---|---|---|
| LAW-PF | joint action/future training → deploy planner | predicted waypoint conditions future latent; target detached; future branch dropped |
| EPO-PLAN | sibling action and visual losses on shared MST + detached chain-of-forward curriculum → deploy action path | factual motion conditions the base visual loss; predicted motion/context appears only in the detached chain curriculum; visual path is bypassed at planning deployment |
| METIS-PLAN | joint action/video training → deploy action-only | predicted action tokens condition visual expert; paper asserts video-loss gradient to action expert; visual expert bypassed |
| DJEPA-PF | predictive video pretrain → downstream planner training → deploy encoder/planner | EMA target and predictor dropped; encoder frozen/no-grad by default |
| WD-PLAN | TA-DWM pretraining → frozen representation transfer/planner training → joint FAR distillation and preference ranking → deploy surrogate/reward | LP precedes FAR; LT and LC are parallel FAR objectives; teacher generator is dropped |
| DFD-PLAN | candidate world-flow training → hybrid winner labels → score supervision → deploy scorer | LC compresses train-time world criterion; world model dropped |
| DWAM-JOINT | world pretrain → shared world-action sequence learning → joint generation deployment | action/world tokens share one coupled sequence; not sibling heads |

### 7.2 LAW versus Metis

They share the family LA because predicted action conditions a future branch and future loss reaches the action path. They are not automatically core-mechanism-equivalent:

- LAW predicts one future latent from a waypoint, detaches the target branch, and drops the predictor.
- Metis uses asymmetric action→video attention inside coupled experts, combines action/video flow losses, and bypasses the visual expert at deployment.
- Their runtime Ts also differs in the projected modes.

Conclusion: same learning family, different canonical L program.

### 7.3 Epona versus LAW

Epona standard visual training uses factual motion and shares MST parameters; LAW uses predicted waypoint as the future predictor condition. Therefore LS versus LA remains a real directed-edge distinction.

### 7.4 Missing macro found

DriveLaW does not fit LP exactly: the generative trunk itself remains online as C4, while full decoding is skipped. Add:

    LG generative-carrier pretraining and retained-trunk adaptation

The raw program remains authoritative.

### 7.5 Equivalence levels

Short signatures cannot alone assert full mechanism identity. Adopt:

1. Runtime-equivalent: C/X/D/P/V/T runtime projections are equal after audit-parameter erasure.
2. Mechanism-family-equivalent: runtime-equivalent and ordered L macro families match.
3. Core-mechanism-equivalent: full typed deployment and learning DAGs are isomorphic after renaming representation/backbone/generator implementations and erasing noncausal numeric parameters.

A collision at level 1 or 2 is not automatically level 3.

Verdict: L=MODIFY with LG and mandatory canonical program; equivalence relation=SPLIT into three levels.

## 8. Twelve type-constraint audit

| # | Constraint | Test result | Revision |
|---:|---|---|---|
| 1 | D2 requires C_runtime, X3, P, V | pass | allow V=VX when resolver exists but semantics unknown; never N/A |
| 2 | D3 requires action→carrier and carrier→action | pass | also require Tr=present |
| 3 | D4 requires joint world–action sequence | pass | require C5 and X4 |
| 4 | D5 permits A*=N/A | pass | for externally controlled/generation-only modes use P=N/A |
| 5 | TRAIN_ONLY carrier cannot support D1–D4 | pass | retain |
| 6 | P may exist without world carrier | pass via DJEPA-PB/DFD | retain |
| 7 | no candidate commitment constrains V | wording needed | P=P∅, PH, or N/A ⇒ V=N/A; V∅ reserved for an actual resolver without evaluative evidence |
| 8 | no future/joint carrier constrains X | pass with lifecycle syntax | C may contain TRAIN future while X@R=N/A |
| 9 | Th does not imply Tr/Tc | pass via WoTE/Epona | retain |
| 10 | Ts does not imply physical future | pass via DriveLaW/Metis/DWAM-POLICY | retain |
| 11 | L cannot be inferred from D | pass via D∅ group and D2 group | retain |
| 12 | dropped node cannot appear in runtime path | pass | mismatch requires a new artifact/version |

Additional constraints required:

13. D1 requires at least one C@R ancestor of A* and excludes the D2 candidate-consequence resolver pattern.
14. PB requires A* to exist; generation-only D5 uses P=N/A.
15. PU implies `V=UNKNOWN` when resolver applicability is itself unresolved. VX is legal only when a resolver is known to exist but its criterion semantics are unknown; N/A is legal only when the mode type rules out a resolver.
16. A current-only C1 makes X@R=N/A unless a separate future/joint carrier is present.

No semantically false signature remains legal under these additions in the 21-artifact projection.

## 9. Collision-test matrix

### 9.1 Required groups

| Group | Shared fields | Different fields | Mechanism or implementation difference? | Collision verdict |
|---|---|---|---|---|
| LAW-PF ↔ DJEPA-PF ↔ METIS-PLAN | D∅,P∅,V=N/A | X: predicted-action vs unconditioned; T: Metis Ts; L: LA vs LP; detailed C/L | mechanism differences | no complete collision |
| LAW-PF ↔ EPO-PLAN | C2@T,D∅,P∅,V=N/A | Epona additionally has C3@T chain context; X2 action-mediated loss vs Epona X1 base/X2 detached curriculum; T; LA vs LS | mechanism difference in gradient/control edge and training carrier | correctly split |
| W4D ↔ WD ↔ WoTE | candidate-bound X3,D2,PB | C endpoint/current vs surrogate vs horizon; V VW vs VU vs VM+VD; Th; L | mechanism differences | correctly split |
| SEER-PAPER ↔ SEER-CODE | C1+C2,X3 | D3 vs D2; Tr; P/V known only in code | paper/code mechanism difference | correctly split |
| DLAW-PAPER ↔ GW-PLAN | D1,P no verified consequence resolver | C4 vs C1(+train C2); X; Ts audit; P unknown in GW; L | mechanism difference, not representation | correctly split |
| DFD ↔ DJEPA-PB1/PB2 | D∅,PB,LC family | V hybrid world/expert/dynamics vs utility vs utility+comfort; C/X training; Tc | mechanism difference | correctly split |
| EPO-PLAN ↔ EPO-SELF ↔ EPO-CTRL | shared model/L family | D∅ vs D5; C runtime; X runtime; Th; task output | mode-level mechanism difference | correctly split |
| DWAM-POLICY ↔ DWAM-WORLD ↔ DWAM-JOINT | token-edit family/Ts | C lifecycle/type, X, D∅/D5/D4, Th, A* applicability | mode-level mechanism difference | correctly split |

### 9.2 Complete-signature collisions

#### DLAW-PAPER ↔ DLAW-CODE

- Core short signatures collide.
- Runtime DAGs are isomorphic after erasing exact solver count and formula-sign notation.
- Learning DAG family is also aligned, though source proves an action_full gradient detail more strongly.
- Verdict: reasonable mechanism-family collision; core-mechanism equivalence is HIGH for topology but exact numeric/formula reproduction remains unresolved.

No other pair has a fully identical revised signature with equally resolved fields.

### 9.3 Near-collisions that would have failed under a coarser ontology

- LAW-PF and Metis would collide under “training-only future branch” unless X, T, and full L are retained.
- W4D and WorldDrive would collide under “candidate future scoring” unless direct versus surrogate C, VW versus VU, and LP→joint(LT,LC) are retained.
- W4D and WoTE would collide unless endpoint versus horizon C/Th and VW versus VM+VD are retained.
- Seer paper/code would collide under paper title or “future-aware planner” labels.
- DFD and Drive-JEPA PB would collide under “world/simulator trains scorer” unless V provenance and C/X training records are retained.

## 10. Split test

Within every retained category, differences based only on representation or generator implementation were ignored:

- C2 accepts latent/BEV/token endpoint consequences.
- D1 accepts current structured or future-generative carriers only because C separately records the object.
- PB accepts proposal-bank construction by queries, anchors, or decoded trajectories.
- PH accepts a semantic decision variable only when its meaning is independently defined and it conditions action formation.
- Ts accepts diffusion, flow, or token editing.

Splits were retained only where semantic inputs/outputs, lifecycle, candidate identity, resolver target, or gradient direction changed.

Result: pass after revisions.

## 11. Implementation-invariance test

### 11.1 Replacements that must not change the signature

| Replacement | Preserved conditions | Expected result |
|---|---|---|
| RGB↔BEV↔latent↔token | same carrier semantics and lifecycle | no C–L change |
| regression↔diffusion↔flow | same semantic I/O and causal path | no change except audit algorithm |
| CNN↔Transformer/DiT | same typed edges | no change |
| 10↔20 solver steps | same solver clock and outputs | T core unchanged; parameter changes |

Result: revised ontology passes by construction.

### 11.2 Mechanism changes that must change the signature

| Change | Required signature change |
|---|---|
| training-only future→runtime future | C lifecycle and D |
| single predicted control→candidate-preserving control | X2→X3; often P/D |
| endpoint→physical-horizon rollout | C2→C3 and Th absent→present |
| utility ranking→factual compatibility | VU→VM |
| shared-state loss→action-mediated loss | LS→LA plus detailed L edge |
| teacher removed with deployed surrogate retained | C realization and LT retain/drop |

Result: pass.

## 12. Lifecycle test

Checked train-only future branches:

- LAW-PF/PB;
- EPO-PLAN;
- Drive-JEPA PF/PB;
- Metis;
- DynFlowDrive;
- DWAM-POLICY.

All have D∅ and no C@R future record. WorldDrive is the contrasting case: heavy teacher is dropped, but a surrogate C2@R is explicitly retained, so D2 remains valid.

Result: pass.

## 13. Candidate-identity test

Accepted runtime banks:

- W4D, WorldDrive, WoTE, released SeerDrive, Drive-JEPA PB1/PB2, DynFlowDrive.

Unresolved:

- SeerDrive paper and GraphWorld final mode resolution.

Rejected:

- LAW outputs;
- Epona action-flow samples;
- DriveLaW diffusion states;
- Metis flow states;
- Discrete-WAM decision vocabulary/token edits;
- winner-take-all training labels without runtime resolver.

Result: pass with PU retained for two artifacts.

## 14. Hybrid-objective test

The revised V record preserves atoms, target provenance, measures, and composition. It avoids both failure modes:

- collapsing all scalars into one “score”;
- multiplying categories because different papers use L2, BCE, ranking loss, or a learned head.

Known UNKNOWN composition/sign details in WoTE and DynFlowDrive remain unresolved rather than guessed.

Result: pass with bounded unknowns.

## 15. Version/mode test

Required splits remain visible:

- LAW PF/PB;
- Epona planning/self/external control;
- DriveLaW paper/code;
- SeerDrive paper/code;
- Drive-JEPA PF/PB1/PB2;
- Discrete-WAM policy/world/joint.

Result: pass.

## 16. Completeness test

The revised short signature reconstructs:

- carrier type/lifecycle;
- control branching;
- runtime carrier path;
- candidate commitment;
- resolver semantics;
- clock topology;
- ordered learning family.

It does not reconstruct every gradient edge or stage scope by itself. That information remains in the canonical L program and full DAG.

Therefore completeness is conditional:

    short signature + canonical L program + evidence boundary
    can reconstruct the core graph

    short signature alone
    cannot

This is intentional and is the reason for graded equivalence.

Result: partial pass; sufficient for S1+, not enough for S2 without blind external use and resolution of key UNKNOWN edges.

## 17. Anti-marketing test

All paper/module names were hidden and replaced by typed inputs, outputs, paths, targets, and clocks. No retained class contains a paper name, representation substrate, backbone name, or branded module.

Result: pass.

## 18. Preserved failure cases

These failures are not repaired by invention:

1. SEER-PAPER final resolver remains PU with V=UNKNOWN.
2. GW-PLAN final resolver remains PU with V=UNKNOWN.
3. LAW-PB exact detach topology remains UNKNOWN.
4. W4D exact future-loss gradient into proposal path remains UNKNOWN by config.
5. Metis, DynFlowDrive, Discrete-WAM, and GraphWorld lack executable source verification.
6. DynFlowDrive flow sign/anchor and hybrid composition remain ambiguous.
7. WoTE paper reward sign/ordering wording remains bounded by source behavior.
8. Discrete-WAM headline metric mode remains uncertain between policy-only and joint capability.

These unresolved edges block an S2 declaration.

## 19. Phase 3 audit conclusion

The ontology covers all 21 artifacts without leaking train-only futures into runtime, promoting random samples to candidate banks, or accepting ordinary perception states as world carriers.

However, Phase 2’s exact coding required material revisions. The resulting status is S1+:

- stronger than a descriptive table;
- internally typed and counterexample-tested;
- not yet S2 because key resolver/source/gradient boundaries remain UNKNOWN and the short signature requires the canonical L program for full reconstruction.
