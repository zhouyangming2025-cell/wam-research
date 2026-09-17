# D02-W1 Escalated Cases

This is a compact escalation ledger, not a set of full ontology cards. Six cases are elevated because a shallow `R–W–E ⊕ L` row could hide a carrier-gate, candidate-identity, joint-emission, or evidence-closure error. No new code is introduced by an escalation.

| Case | Why escalation is justified | Shallow hypothesis | Backend fields to inspect next | Current route / disposition |
|---|---|---|---|---|
| P0004 BeTop | Future multi-agent topology and trajectory predictions clearly influence planning, but the local text does not fully isolate the ego commitment path from the multi-agent prediction path. | `context → future topology/trajectory carrier → direct ego trajectory` | `C` carrier gate; `X` whether ego action indexes the carrier; `D` direct condition versus reciprocal refinement; `T` online horizon; ordered `L`. | `R0 + W4 + E0`; retain as provisional direct future-horizon family. |
| P0010 TOAD | Test-time CEM creates and updates an explicit candidate population, but the scorer is not a world model. The case tests whether `RB + W0 + EV` is legal without manufacturing a `W`. | `proposal distribution → candidates → learned trajectory reward → selected candidate` | `P` identity preservation; `V` holistic value; `T` solver loop; `C=∅/W0`; confirm no hidden consequence carrier. | `RB + W0 + EV`; expected candidate-resolver family. |
| P0021 Hydra-MDP | Multiple heads, human teacher, rule/simulation teacher, and metric-specific scores can be conflated into one vague “multi-target” label. | `context → candidate trajectories → human/rule-derived metric vector → common choice` | `P` common resolver; `V=EF+ED`; `L` teacher-to-student and scorer retention; target provenance as modifier. | `RB + W0 + (EF+ED)`; no new `E` code. |
| P0029 GenAD | The paper’s joint generation can be mistaken for direct future-conditioned action or for an explicit candidate bank. | `joint latent future process → world/agent trajectories and ego trajectory` | `C5` joint carrier; `D4` direct joint emission; `P` absence of downstream common resolver; `X4`; `LQ`. | `RJ + W5 + E0`; retain as existing joint-emission route. |
| P0034 HUGSIM | The local raw artifact contains the title/metadata but insufficient method evidence. Any route would be an inference from the name. | `simulator only` is plausible but not auditable from the selected local source. | All backend fields remain `UNKNOWN`; first close source/evidence boundary, then decide whether it is `RG`, boundary N/A, or another terminal role. | `UNKNOWN`; no route assignment until evidence closure. |
| P0038 Vista | Vista exposes controllable world rollouts and a model-derived action reward, but the shallow abstract does not establish whether that reward is a final online resolver for a one-stage policy. | `action/control → future rollout → reward/evaluation` | `D` terminal generation versus candidate selection; `P` candidate identity/common resolver; `V=EV` only if final selection is shown; `T` future rollout. | `RG + W4 + E0` boundary; do not promote to candidate route yet. |

## Escalation policy

The cases above are not evidence that the ontology is wrong. They are the smallest set where a false collision or false split could change the route-family map. Deeper inspection may refine a modifier, scope, or ordered learning edge. It may not create a new axis/code in Wave 1.

P0058 VAD is recorded as an evidence-limited audit flag in the census rather than a seventh escalation case. Its question is narrow: whether vectorized predicted motion is a qualifying carrier under the existing four-part gate. If later evidence shows that it is only an ordinary representation, its route changes to `W0`; this is a planned `REMAP`, not a new category.

No separate `cases/` files are created in Wave 1. The selected works remain one-row shallow artifacts, and the six pressure cases are fully named here for a later evidence pass.
