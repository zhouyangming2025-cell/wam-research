# D02-W1E Full-Text Collision and Constraint Audit

## Purpose

This audit compares the twenty full-text projections at three levels. A shared
headline route is not treated as a false collision unless the shared signature
would make the mechanism sentence materially false.

## 1. Human runtime route collisions

| Human group | Members in the twenty-artifact set | Judgment | Reason |
|---|---|---|---|
| `RB + W4 + ED` | P0004 BeTop, P0057 UniAD | EXPECTED_FUNCTIONAL_EQUIVALENCE at coarse layer; BACKEND_SEPARATED | Both preserve ego candidate identity to a common resolver using a future-horizon signal and decomposed driving-oriented cost. BeTop uses topology/contingency prediction; UniAD uses predicted occupancy and Newton/multiple-shooting optimization. |
| `RH + W0 + E0` | P0024 DriveVLM, P0026 ORION | EXPECTED_FUNCTIONAL_EQUIVALENCE; BACKEND_SEPARATED | Both expose an independently semantic planning stage before trajectory generation. Their tokenization, VLM architecture, and planner implementation differ. |
| `R0 + W0 + E0` | P0017 CRAFT, P0025 OmniDrive | EXPECTED_FUNCTIONAL_EQUIVALENCE; L_SEPARATED | Both deploy a direct action/planning path with future/counterfactual material confined to learning or data generation. CRAFT uses counterfactual reinforcement fine-tuning; OmniDrive uses VLM/Q&A training. |
| `RG + W4 + E0` | P0039 DriveDreamer-2, P0038 Vista | EXPECTED_BOUNDARY_EQUIVALENCE, not an in-domain planner collision | Both are generation/evaluation terminal modes. Their generated objects and controls differ, and both remain outside the one-stage decision route. |

Boundary nearest routes are deliberately not merged with in-domain planner
routes. In particular, P0013, P0019, P0054, and P0055 are useful negative
controls: candidate selection, interactive prediction, evaluation loops, or
simulation does not automatically become an ego action commitment.

## 2. Normative runtime collision and separation

### BeTop / UniAD pressure group

Both can be conservatively represented as:

```text
C3@B(shared future-horizon carrier)
· X=N/A
· D1
· P=PB
· V=VD
```

This is not a false collision at the normative runtime level. The shared carrier
is distinct from a candidate-indexed consequence, so `D2` and `X3` must not be
invented. `PB` still records the independent candidate-commitment topology.
The collision is therefore a valid compression collision to investigate, not a
reason to duplicate `W4` or create a new code.

### Direct training-only group

CRAFT and OmniDrive remain runtime-equivalent at the coarse level:

```text
C∅ · X=N/A · D∅ · P=P∅ · V=N/A
```

Their learning DAGs separate them: CRAFT has counterfactual criterion plus
policy optimization (`LC→LR`), while OmniDrive has predictive/representation
pretraining and retained VLM/planner (`LP`). This is an intentional `L`
separation, not a false collision.

### Semantic hierarchy group

DriveVLM and ORION share `PH`/`RH`, but their intermediate semantics remain
independently identifiable. DriveVLM uses a sequence of meta-actions and a
decision description before waypoints; ORION uses an LLM planning token before a
generative planner. The human collision is expected; the backend is separated
by the semantic carrier and learning path. No `RB` is justified merely because
the planner can produce multiple modes.

## 3. Candidate gate checks

| Artifact | Candidate birth | Identity preserved | Common resolver determines final output | Candidate resolver admitted? |
|---|---|---|---|---|
| P0004 BeTop | multimodal/branched ego trajectories | yes | yes | yes, `PB`; shared future carrier remains a pressure |
| P0010 TOAD | CEM control population | yes | yes | yes, `RB + W0 + EV` |
| P0021 Hydra-MDP | fixed candidate vocabulary | yes | yes | yes, `RB + W0 + (EF+ED)` |
| P0013 BridgeSim | candidate trajectory actions in TTA/planner loop | evidence sufficient for nearest boundary comparison | yes for nearest route, but not a WAM planner artifact | boundary-only `RB + W0 + EV` |
| P0019 M2I | `N²` joint agent samples | yes | yes, likelihood selector | boundary prediction selector; not ego `R` |
| P0057 UniAD | multiple-shooting trajectories around initial plan | yes | yes, occupancy/cost optimizer | yes, `PB`; shared future carrier remains a pressure |
| P0024 DriveVLM | meta-action/decision sequence | semantic intermediate, not candidate bank | no common candidate resolver shown | `RH`, not `RB` |
| P0026 ORION | multimodal generative trajectories | not shown to enter common resolver | no | `RH`, not `RB` |
| P0029 GenAD | joint world/ego samples | joint identity does not reach downstream resolver | no | `RJ`, not `RB` |

## 4. Constraint results

| Check | Result |
|---|---:|
| Illegal new human route code | 0 |
| Illegal new world code | 0 |
| Candidate bank admitted without identity/common resolver | 0 |
| Training-only future branch leaked into W | 0 |
| Joint emission incorrectly promoted to candidate resolver | 0 |
| `D4` used where a downstream common resolver exists | 0 |
| False collision established | 0 |
| Existing `W4 + RB → X3` rule independently pressured | 2 cases |

## Verdict of this audit

The new UniAD case strengthens, rather than invalidates, the earlier BeTop
finding. The framework can describe both papers without a new axis, but the
human compression rule is narrower than the backend causal graph for the
shared-carrier-plus-resolver pattern. This remains a HOLD-level structural
question for a later human decision. It is not changed automatically in this
evidence pass.
