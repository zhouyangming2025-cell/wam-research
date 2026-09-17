# D01.2-R2 Final Collision Audit

The audit keeps three layers separate:

1. human runtime: `R-W-E`;
2. normative runtime: `C-X-D-P-V-T`;
3. full mechanism: runtime backend plus ordered `L`.

The labels used below are deliberately explicit:

- `EXPECTED_FUNCTIONAL_EQUIVALENCE`: same semantic function at the layer being tested;
- `BACKEND_SEPARATED`: human route may collide, but typed runtime fields separate the mechanisms;
- `L_SEPARATED`: runtime may collide, but ordered learning/deployment program separates the mechanisms;
- `FALSE_COLLISION`: a grouping that erases a mechanism-defining distinction and is therefore prohibited.

## 1. Human-runtime groups

| Human signature | Members | Classification | Judgment |
|---|---|---|---|
| `R0+W0+E0` | A04, A08, A09, A12, A18, A22 | `EXPECTED_FUNCTIONAL_EQUIVALENCE` | Direct deployment with no online qualifying world carrier. Training world use remains in L and retain/drop notes. |
| `R0+W4+E0` | A03, A07, A20 | `EXPECTED_FUNCTIONAL_EQUIVALENCE` | Direct action conditioned by an online future-horizon carrier without a candidate resolver. |
| `RB+W4+ED` | A01, A15, A23 | `EXPECTED_FUNCTIONAL_EQUIVALENCE` | Candidate-specific future horizons and common resolvers use decomposed driving outcomes. |
| `RJ+W5+E0` | A13, A17 | `EXPECTED_FUNCTIONAL_EQUIVALENCE` | One joint world/action process directly emits action without a downstream common resolver. Their learning routes remain separate below. |
| `RG+W4+E0` | A02, A06, A21 | `EXPECTED_FUNCTIONAL_EQUIVALENCE` | Generated future world is the terminal output; target and simulator provenance are attributes. |
| `RB+W3+ED` | A10 | singleton | A10 has candidate retrieval/scoring but no candidate-specific world consequence. |
| `RB+W3+(ED->EV)` | A14 | singleton | A14 combines decomposed candidate evidence into holistic preference. |
| `RB+W5+EV` | A16 | singleton | Candidate-indexed C5 enters a common resolver; this is the newly legalized composition. |
| `R0+W1+E0` | A11 | singleton | Current structured world conditions direct action. |
| `RR+W3+E0` | A19 | singleton | Reciprocal action/future endpoint refinement within one decision. |
| `RU+WU+E?` | A05 | singleton | Runtime planning fate remains UNKNOWN. |

No human-runtime group contains a false collision.

## 2. Normative-runtime groups

| Exact/near runtime backend | Members | Classification | Why |
|---|---|---|---|
| `C3@R{direct};X=∅;D1;P=∅;V=N/A;T=(A,A,P,U)` | A03, A07 | `EXPECTED_FUNCTIONAL_EQUIVALENCE` | Same direct online future-horizon interface; occupancy realization differences are below the chosen semantic granularity. |
| `C3@T{direct};X=∅@T;D∅;P=∅;V=N/A;T=(A,A,A,U)` | A08, A09, A12 | `EXPECTED_FUNCTIONAL_EQUIVALENCE` | Same training-only predictive-transfer deployment role. |
| `C3@T{direct};X2@T;D∅;P=∅;V=N/A;T=(A,A,A,U)` | A04, A18 | `EXPECTED_FUNCTIONAL_EQUIVALENCE` | Same training-only predicted-action-to-world interface with direct action-only deployment. |
| `C5@R{direct};X4;D4;P=∅;V=N/A;T=(P,A,P,U)` | A13, A17 | `EXPECTED_FUNCTIONAL_EQUIVALENCE` | Same direct joint-emission runtime topology. L separates the learning programs. |
| `C3@R{generative_internal};X1;D5;P=N/A;V=N/A;T=(P,A,P,U)` | A02, A06, A21 | `EXPECTED_FUNCTIONAL_EQUIVALENCE` | Same generation-only controlled-world output topology. Simulator/reactivity and target provenance remain attributes. |
| A01/A15/A23 | A01, A15, A23 | `BACKEND_SEPARATED` | All are `RB+W4+ED`, but their Ts/solver and evidence boundaries are not asserted identical. Human collision is expected; typed backend identity is not claimed. |
| A10 versus A14 | A10, A14 | `BACKEND_SEPARATED` | A10 is C2 surrogate + X∅ + D1; A14 is C2 direct + X3 + D2. Their E compositions are also different. |
| A16 versus A17 | A16, A17 | `BACKEND_SEPARATED` | A16 is C5[k] + D2 + PB; A17 is one C5 + D4 + P∅. The amendment preserves this split. |

## 3. Full-mechanism groups

| Full signature relation | Members | Classification | Learning judgment |
|---|---|---|---|
| Same normalized runtime and `L=LS` | A03, A07 | `EXPECTED_FUNCTIONAL_EQUIVALENCE` | Same macro learning family; paper-specific losses remain evidence attributes. |
| Same normalized runtime and `L=LP` | A08, A09, A12 | `EXPECTED_FUNCTIONAL_EQUIVALENCE` | Predictive representation transfer is the intended equivalence class. |
| Same normalized runtime and `L=LG` | A02, A06, A21 | `EXPECTED_FUNCTIONAL_EQUIVALENCE` | Generative-carrier adaptation is the shared macro route; target/simulator provenance does not create a new core mechanism. |
| Same runtime, `L=LC->LR` versus `L=LS->LR` | A04, A18 | `L_SEPARATED` | Both are action-only at deployment, but the world/action co-training and reward paths differ. |
| Same runtime, `L=LP->LQ` versus `L=LC->LR` | A13, A17 | `L_SEPARATED` | Joint world/action sequence learning differs from reward-fine-tuned joint generation. |
| `RB+W4+ED` group | A01, A15, A23 | `BACKEND_SEPARATED` + `L_SEPARATED` | Resolver family collides intentionally; carrier realization, clock evidence, and ordered L remain distinct. |
| A10 versus A14 | A10, A14 | `BACKEND_SEPARATED` | They cannot be merged by writing both as RB+W3+ED; A14's ED->EV composition and D2/X3 path are mechanism-defining. |

## 4. Explicit false-collision tests

| Tempting grouping | Classification if performed | Required outcome |
|---|---|---|
| A10 and A14 after erasing the complete E expression | `FALSE_COLLISION` | Keep `RB+W3+ED` and `RB+W3+(ED->EV)` separate. |
| A16 and A17 after erasing P/D | `FALSE_COLLISION` | Keep `RB+W5+EV` and `RJ+W5+E0` separate. |
| A13 and A16 because both contain C5 | `FALSE_COLLISION` | D4 direct emission and D2/PB candidate resolution are different final topologies. |
| A04/A18 and A22 after erasing X and realization | `FALSE_COLLISION` | X2 training world branch and X1 simulator/control branch remain separate audit facts. |
| A05 promoted to RJ solely from shared visual/action architecture | `FALSE_COLLISION` | Preserve C5@U, DU, PU, and the runtime UNKNOWN boundary. |

These are prohibited hypothetical merges, not collisions in the final map. Therefore:

```text
false collisions in final accepted grouping = 0
```

## 5. Amendment-specific tests

- A16 uses `C5[k]`, `X4`, D2, PB, VU, and W5+RB.
- A16 does not use X3@resolver.
- A17 remains `C5`, X4, D4, P∅, and RJ+W5.
- A13 remains direct joint emission and is not converted to a candidate resolver.
- W5 is no longer incorrectly restricted to D4.
- D4 is not broadened to cover downstream common resolution.

## Collision verdict

```text
expected human collisions: accepted
backend-separated groups: explicit
L-separated groups: explicit
false collision in final grouping: 0
```
