# D01.3 Freeze Manifest

Status: **frozen before source/method inspection**

## 1. Validation boundary

This branch is the D01.3 blind-validation worktree:

\`\`\`text
repository = zhouyangming2025-cell/wam-research
base branch = codex/ontology-stabilization-d01-2-r2
base commit = 28f6c7da48e692a6a81c7a522e191c97420f875f
working branch = codex/ontology-blind-validation-d01-3
\`\`\`

The frozen mechanism is the existing two-layer system:

\`\`\`text
human route layer:      R–W–E ⊕ L
normative audit backend: C–X–D–P–V–T–L
\`\`\`

This round is a generalization test. It is not an ontology-design round. No code, modifier, axis, composition rule, or canonical route may be added or changed after the blind pool is opened.

## 2. Immutable source blobs

The following files are the normative sources at the base commit. Their Git blob identifiers are recorded so that later working-tree changes cannot silently redefine the test.

| file | blob SHA |
|---|---|
| \`outputs/core_mechanism_12_v1/09_ONTOLOGY_SPEC_S1_PLUS.md\` | \`1fd712c8337fbf4323b48a8acd9ec419949274b5\` |
| \`outputs/core_mechanism_12_v1/12_HUMAN_ROUTE_SIGNATURE_PROPOSAL.md\` | \`5877aff6a7c1867e8b2b4a42f00be25cb64e7e91\` |
| \`outputs/core_mechanism_12_v1/15_D01_2_COMPOSITION_AMENDMENT.md\` | \`3b920165834d7a0677d5d2b7959e9ff1b7261c08\` |

Supporting R2 closeout records and \`handoff/core_mechanism_12/RESEARCH_PROTOCOL.md\` were read before candidate selection. They are evidence for the freeze, not editable schema inputs.

## 3. Frozen normative vocabulary

### C — world/consequence carrier

\`\`\`text
C1 current structured world state
C2 future endpoint consequence
C3 future-horizon consequence sequence
C4 internal future-generative process state
C5 joint world–action sequence/carrier
C∅ no qualifying carrier in the scoped lifecycle
CU carrier type unknown
\`\`\`

Lifecycle modifiers:

\`\`\`text
@T train-only | @R runtime-only | @B both | @U unknown
\`\`\`

Realization modifiers:

\`\`\`text
direct | surrogate | generative_internal | unknown
\`\`\`

The carrier gate requires localizable identity, stateful world operation, carrier-level world/temporal grounding, and a mechanism interface to planning/output or a deployed planning component. Ordinary encoder, BEV, map, detection, or shared-feature states do not become C merely because a planner consumes them.

### X — control/branching interface bound to a carrier

\`\`\`text
X∅ no action/control conditions the applicable carrier
X1 factual, supplied, or external control
X2 one policy-predicted control
X3 candidate-preserving control keyed by k
X4 joint/interleaved world–action variables
XU control edge unknown
N/A carrier type is not action/control-indexable in this lifecycle
\`\`\`

X must be bound to the carrier, lifecycle, and—when needed—the training stage. Candidate identity by itself is not X3; resolver identity belongs to P/D.

### D — deployment carrier-to-output route

\`\`\`text
D∅ no runtime C carrier influences A*
D1 runtime carrier → one policy/action path → A*
D2 candidate consequence → resolver → A*
D3 action → consequence → revised action within one decision before commitment
D4 direct joint world–action emission of the committed output
D5 consequence generation is the terminal mode output
DU route unknown
\`\`\`

The only legal D2 forms are:

\`\`\`text
A{k} → C2/C3{k} → V{k} → resolver → A*
C5{k}=(world{k}, action{k}) → V{k} → resolver → A*
\`\`\`

The first normally binds X3 to the candidate consequence. The second binds X4 to C5[k]. Both require candidate identity preservation, PB, a non-N/A resolver criterion, and a declared A*. A multi-candidate C5 resolver is D2, not D4.

### P — action formation and commitment

\`\`\`text
P∅ direct/implicit action formation
PH semantic decision/intent → action
PB identity-preserving candidate bank → common resolver → A*
PU final commitment topology unresolved
N/A generation-only or external-control mode has no action commitment
\`\`\`

PB requires candidate birth, identity preservation, a common resolver, and a resolver that determines A*. Random samples, multimodality, solver states, or token edits do not suffice.

### V — resolver semantics

\`\`\`text
VM expert/factual behavior compatibility
VU holistic planning utility/preference
VD decomposed driving outcomes
VW world/future fidelity or predictive agreement
VY dynamics/physical validity
VP model confidence/likelihood
VX resolver known, criterion semantics unknown
V∅ resolver exists but no criterion evidenced
N/A no resolver by task/topology
UNKNOWN resolver applicability and/or criterion cannot be established
\`\`\`

Composition, compared objects, target provenance, measure, and ordering remain audit attributes. A metric name or scalar head does not determine V.

### T — online clock topology

\`\`\`text
T=(Ts, Tr, Th, Tc)
Ts solver/denoising/flow/token-edit coordinate
Tr reciprocal world↔policy update within one decision
Th physical-future horizon progression
Tc dependency across real control cycles
\`\`\`

Each clock field is \`absent\`, \`present\`, or \`UNKNOWN\`. Training-only future targets cannot create runtime Th. Numerical iteration count is an audit parameter, not a new clock type.

### L — ordered learning-to-deployment route

\`\`\`text
LP predictive/generative pretraining → encoder/backbone transfer
LS sibling world and policy objectives through shared state/parameters
LA predicted action → world/future branch whose loss reaches action path
LG generative-carrier pretraining with retained online trunk adaptation
LN factual next-state/temporal consistency with stopped target
LT heavy consequence teacher → deployed surrogate distillation
LC world/simulator criterion → proposal, label, reward, or runtime scorer
LQ shared world–action sequence learning
LR reward-based policy optimization
LU learning route unresolved
\`\`\`

L is an ordered, directed program. Stage order, gradient direction, detach/freeze/stopgrad boundaries, and retain/drop/bypass fate are evidence fields, not optional prose.

## 4. Frozen human route vocabulary

\`\`\`text
R0 direct/implicit action
RH semantic decision/intent → action
RB explicit candidate bank → common resolver
RR world↔policy reciprocal refinement before commitment
RJ direct joint world–action emission
RG world/consequence generation is terminal output
RU final action commitment unresolved
\`\`\`

\`\`\`text
W0 no qualifying online world carrier
W1 current structured world state
W2 internal future-generative state
W3 future endpoint consequence
W4 future-horizon consequence sequence
W5 joint world–action carrier
WU online world role unknown
\`\`\`

\`\`\`text
E0 no resolver criterion
EF expert/factual compatibility
EV holistic planning value/preference
ED decomposed driving outcomes
EW world/future fidelity
EY dynamics/physical validity
EP confidence/likelihood
EØ resolver known but no criterion evidenced
E? resolver/criterion unresolved
\`\`\`

R/W/E are a compression layer. The backend remains authoritative for disputes. Training-only carriers are represented in L, not W. \`RB+W5\` is legal for candidate-indexed C5 entering a common resolver; \`RJ+W5\` is direct joint emission without that resolver.

## 5. Frozen evidence and absence rules

\`\`\`text
∅        positive scoped evidence of absence
N/A      upstream type makes the field inapplicable
UNKNOWN  available evidence cannot determine value/applicability
\`\`\`

Evidence must be labeled \`PAPER FACT\`, \`CODE FACT\`, \`OUR INFERENCE\`, or \`UNKNOWN\`. Paper, code, and mode boundaries must be split when they disagree. Online calculation that does not causally affect the declared terminal output is not a runtime decision mechanism.

## 6. Protected paths and prohibited actions

The following paths are read-only for D01.3:

\`\`\`text
outputs/core_mechanism_12_v1/
handoff/core_mechanism_12/
research_program/domain_corpus/d01/
research_program/ontology_regression/d01_2/
research_program/ontology_regression/d01_2_r1/
research_program/ontology_regression/d01_2_r2/
research_program/ONTOLOGY_FREE_CARD_V2.md
\`\`\`

The D01.3 work may add files only under \`research_program/ontology_blind_test/d01_3/\`. It may not modify the frozen ontology, create new codes, create paper-named categories, start D02, or replace a selected paper because its methods, source, or code are incomplete. Evidence difficulty is recorded as UNKNOWN or an evidence-limited verdict.

## 7. Blindness barrier

Before the preregistration file is written, the candidate pool is constructed from local identifiers, exact titles, years, source metadata, abstracts, and explicit exclusion checks only. No method section, formula, code path, mechanism diagram, or existing ontology projection is used to choose a selected paper. After the pool and selection are sealed, source inspection may begin.


