# D01.3 Blind Counterexample Review

This is the adversarial pass performed after the ontology-free cards and frozen projections. It treats every projection as potentially wrong and does not change the ontology in response.

Reviewer choices:

\`\`\`text
ACCEPT
REMAP_WITH_EXISTING_CODES
NEED_EVIDENCE
STRUCTURAL_CHALLENGE
\`\`\`

## 1. Per-artifact attack

| artifact | attack question | adversarial finding | reviewer choice |
|---|---|---|---|
| GAD-PLAN | Is the future trajectory object merely an ordinary feature or a qualifying world/consequence carrier? | It is separately represented, temporally sequenced, motion-supervised, used to construct interaction edges, and reaches planning. The carrier gate is met. | ACCEPT |
| GAD-PLAN | Do iterative graph layers force reciprocal world/policy refinement? | The paper shows predicted trajectories refining graph features and new trajectories, but does not show a committed action entering a separate future transition and returning to policy. Internal iterative prediction alone does not force reciprocal topology. | ACCEPT |
| DD-VIS | Is terminal future video being confused with an internal generative hidden state? | The terminal semantic object is the generated future video sequence; hidden diffusion states were not promoted to a separate carrier. This preserves the direct-terminal versus internal-state distinction. | ACCEPT |
| DD-ACT | Does the paper prove direct joint world/action emission, or only a world-conditioned action head? | The paper gives a joint future-video/future-action factorization, but exact action-only deployment and code boundary are unresolved. Existing direct-joint and internal-carrier forms both remain available; the main projection must retain UNKNOWN. | NEED_EVIDENCE |
| DRV-PLAN | Are trajectory time points being mistaken for future world consequences? | No environment transition, agent response, occupancy rollout, or predicted world state is described. The proposal bank is action output, so no online world carrier is admitted. | ACCEPT |
| DRV-PLAN | Does a common resolver really determine the final action? | Proposals retain identity, each is scored, weighted sub-scores form the final score, and argmax selects the committed trajectory. PB is satisfied. | ACCEPT |

## 2. Twelve frozen-ontology checks

| # | check | result | rationale |
|---:|---|---|---|
| 1 | carrier gate versus ordinary representation | PASS | GraphAD future motion, DriveDreamer generated future structure/video, and DrivoR scene tokens/proposals are separated correctly. Only the first two pass the carrier gate. |
| 2 | training/runtime mixing | PASS with evidence limit | DriveDreamer's staged training is separated from runtime generation/action use; exact video-decoder fate in action-only inference remains UNKNOWN. |
| 3 | candidate identity preservation | PASS | DrivoR has explicit proposal identity through the scorer; GraphAD modalities and DriveDreamer samples are not promoted to PB without a common final resolver. |
| 4 | resolver determines final action | PASS | DrivoR's weighted maximum determines the final trajectory; no such resolver is asserted for GraphAD or DriveDreamer. |
| 5 | D1/D2/D3/D4/D5 discrimination | PASS with one UNKNOWN | GraphAD is kept at direct carrier-to-action because the evidence lacks a committed-action-to-world transition; DriveDreamer video is terminal generation; DriveDreamer joint action/video is direct joint emission; DrivoR has no runtime carrier. |
| 6 | X3 versus X4 | PASS with one UNKNOWN | No X3 is invented for GraphAD or DrivoR. DriveDreamer joint mode uses X4 only under the joint-emission reading; the paper/code boundary is explicitly unresolved rather than silently asserted. |
| 7 | endpoint, horizon, and joint object | PASS | GraphAD is a future sequence, DriveDreamer video is a future sequence, DriveDreamer action/video is a joint object, and DrivoR proposals are not a world object. |
| 8 | semantic target versus loss/head | PASS | DrivoR's decomposed safety/comfort/progress supervision is treated as driving-outcome semantics, not as a generic scalar-head category. |
| 9 | learning direction/order/deployment fate | PASS with evidence limit | GraphAD staged freezing and DriveDreamer two-stage learning are ordered; DrivoR's scorer-to-perception and scorer-stop-to-proposal edges are retained. |
| 10 | same human signature false collision | PASS | GraphAD's R0+W4+E0 is a functional collision with the existing direct future-horizon family, not a false collision. DriveDreamer DD-VIS and DD-ACT remain separate terminal mechanisms despite related learning. |
| 11 | different signature false split | PASS | The split between DriveDreamer video generation and action/joint mode changes terminal semantics; the split between DrivoR's W0 resolver and future-carrier routes is necessary. |
| 12 | hidden-title stability | PASS | Each result can be reconstructed from input/output/causal role without the paper title or author terminology. |

## 3. Collision review

### Human runtime layer

| signature | blind member | nearest prior members | judgment |
|---|---|---|---|
| R0+W4+E0 | GAD-PLAN | A03, A07, A20 | EXPECTED_FUNCTIONAL_EQUIVALENCE |
| RG+W4+E0 | DD-VIS | A02, A06, A21 | EXPECTED_FUNCTIONAL_EQUIVALENCE at human layer |
| RJ+W5+E0 | DD-ACT | A13, A17, Discrete-WAM joint | EXPECTED_FUNCTIONAL_EQUIVALENCE at human layer; action/video fate remains an attribute |
| RB+W0+ED | DRV-PLAN | Drive-JEPA PB2 family at W0, with different criterion/training details | EXPECTED_FUNCTIONAL_EQUIVALENCE at human layer |

### Normative backend

- GAD-PLAN is close to the direct future-horizon rows but its explicit graph construction and training evidence are retained in the carrier and learning record.
- DD-VIS is separated from prior generation rows if their internal realization differs; the terminal human route remains equivalent.
- DD-ACT is separated from direct joint-emission rows only at the learning/deployment evidence boundary if the action-only path drops the video decoder. This is an evidence boundary, not a new type.
- DRV-PLAN has no runtime carrier, but PB and VD remain explicit. It does not collide with a future-consequence candidate route.

### Full mechanism layer

- GAD-PLAN may be macro-equivalent to the direct future-horizon/shared-training family; graph architecture is an implementation or supporting-branch attribute unless it changes the carrier/output topology.
- DD-VIS has generative-carrier learning and terminal generation.
- DD-ACT has an ordered generative-to-joint world/action program; the unresolved decoder fate is recorded as UNKNOWN.
- DRV-PLAN has a known proposal/scorer learning DAG with gradient separation and no world-linked learning edge. Its detailed learning DAG is not erased by the human W0 compression.

No final grouping produces a false collision. The only unresolved item is the DD-ACT deployment interpretation.

## 4. Structural challenge decision

The strongest apparent challenge is that DriveDreamer uses one model to predict future video and future actions, while the paper also evaluates an action-only planning path. The existing ontology already distinguishes:

1. direct joint world/action emission without a resolver; and
2. an internal future-generative state conditioning a direct action path.

The paper evidence does not force a new semantic axis. It only fails to determine which deployment boundary the official implementation uses. Therefore this is NEED_EVIDENCE, not STRUCTURAL_CHALLENGE.

The strongest apparent challenge from GraphAD is iterative future-trajectory refinement. The frozen D3/RR rule requires an action-to-consequence-to-revised-action causal loop, not merely repeated graph prediction. The available paper does not establish that stronger loop, so D1 is retained.

## 5. Attack verdict

\`\`\`text
structural challenge = 0
false collision = 0
existing-code remap = 0
evidence-limited artifacts = DD-ACT and code boundaries
ontology modified = no
\`\`\`


