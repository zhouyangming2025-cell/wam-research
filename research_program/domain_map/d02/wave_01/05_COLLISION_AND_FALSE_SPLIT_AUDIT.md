# D02-W1 Collision and False-Split Audit

The audit is performed at three levels. A collision is not automatically a problem: papers that implement the same causal interface are expected to share a human route. A collision becomes false only when a retained causal distinction is erased. Conversely, a split is false when it is caused only by representation, architecture, or solver implementation.

## 1. Human runtime collisions: `R–W–E`

| Group | Members | Judgment | Reason |
|---|---|---|---|
| H1 | P0004 BeTop, P0057 UniAD, P0058 VAD: `R0 + W4 + E0` | EXPECTED_FUNCTIONAL_EQUIVALENCE, provisional | All three are direct ego trajectory routes whose planning path consumes structured future-horizon information. BeTop topology, UniAD queries, and VAD vectors are realization differences. P0058 remains evidence-limited at the carrier gate. |
| H2 | P0010 TOAD `RB + W0 + EV`; P0021 Hydra-MDP `RB + W0 + (EF+ED)` | BACKEND_SEPARATED | Both preserve candidates through a resolver, but holistic reward search is not the same resolver semantics as mixed factual compatibility/decomposed driving outcomes. The `E` composition is meaningful and must not be normalized away. |
| H3 | P0024 DriveVLM, P0026 ORION: `RH + W0 + E0` | EXPECTED_FUNCTIONAL_EQUIVALENCE, provisional | Both have an independent semantic decision/reasoning stage before numeric trajectory generation. VLM/LLM realization and token format are below the route layer. |
| H4 | P0029 GenAD `RJ + W5 + E0`; existing Discrete-WAM joint mode | EXPECTED_FUNCTIONAL_EQUIVALENCE, provisional | Both describe joint world/action generation without a downstream common resolver. Their generative carrier and token/trajectory realization differ, but the terminal topology is the same. |
| H5 | P0038/P0039/P0055 generation/simulation works | NOT A PLANNING COLLISION | These are retained as boundary records rather than collapsed into the deployed planner map. A generated future or simulator output is not equivalent to a policy commitment. |
| H6 | P0017 CRAFT and P0025 OmniDrive: `R0 + W0 + E0` | EXPECTED_FUNCTIONAL_EQUIVALENCE at runtime; L_SEPARATED | Both leave a direct policy at deployment while counterfactual/predictive material is training-side. CRAFT uses counterfactual policy-gradient proxy plus closed-loop residual correction; OmniDrive uses counterfactual data/QA supervision. |

## 2. Normative runtime collisions: `C–X–D–P–V–T`

Only pressure cases are expanded to the backend; ordinary rows remain at the human layer.

| Group | Backend distinction | Judgment |
|---|---|---|
| N1 | P0010: no qualifying `C`, `P` candidate bank, `V` holistic reward, solver clock; P0021: no qualifying `C`, `P` candidate bank, `V` composed factual/decomposed criteria, teacher/scorer learning | BACKEND_SEPARATED |
| N2 | P0029: joint `C5` world-action carrier, `X4`, direct `D4`, no downstream `PB`; existing Discrete-WAM joint mode has the same topology but different carrier realization | EXPECTED_FUNCTIONAL_EQUIVALENCE; `L` separates |
| N3 | P0004/P0057/P0058: future-horizon carrier and direct policy path; exact carrier identity, action binding, and online clock remain to be closed | PROVISIONAL COLLISION, not false |
| N4 | P0038: controllable future world carrier is evidenced, but `D/P/V` final selection topology is not; forcing `RB` would be an unsupported backend split | EVIDENCE_GAP |

## 3. Full mechanism collisions: backend plus ordered `L`

| Group | Learning distinction | Judgment |
|---|---|---|
| L1 | P0017 `LC→LR→retain{policy}/drop{counterfactual world}` versus P0025 `LP→retain{VLM/planner}/drop{counterfactual data generator}` | L_SEPARATED |
| L2 | P0010 `LC→retain{scorer}` with runtime CEM versus P0021 `LT→LC→retain{proposal/scorer}/drop{teachers}` | L_SEPARATED |
| L3 | P0004/P0057/P0058 sibling/shared-state future prediction and planning routes | EXPECTED_FUNCTIONAL_EQUIVALENCE at this granularity; exact losses and heads are modifiers |
| L4 | P0029 `LQ→retain{joint generator}` versus the existing Discrete-WAM joint mode `LQ→retain{joint token model}` | L_SEPARATED in realization, same mechanism family |

## False-collision tests

1. P0010 and P0021 are not collapsed merely because both have `RB`; `EV` versus `(EF+ED)` is retained.
2. P0038 is not assigned `EV` until action reward is shown to determine a final selected action; generation/evaluation capability alone is insufficient.
3. P0034 is not assigned a simulator route from its title alone.
4. P0004/P0057/P0058 remain a provisional group, not a final assertion that every vectorized or predictive feature is a WAM carrier.

Result: false collision = 0 on the sealed shallow evidence; four groups remain evidence-limited or provisional and are explicitly named. No false split is found after ignoring architecture, representation, and solver implementation. New axis/code/modifier = 0.
