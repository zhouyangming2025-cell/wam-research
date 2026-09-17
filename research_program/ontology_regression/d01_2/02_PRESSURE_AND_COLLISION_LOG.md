# D01.2 Pressure and Collision Log

## 1. Test interpretation

The question is not whether every artifact receives a unique string. The question is whether the existing ontology separates mechanisms when the difference changes a semantic interface, lifecycle, commitment topology, resolver meaning, or ordered learning edge, while allowing implementation variants to remain in one functional family.

Two collision levels are therefore distinguished:

1. **expected compression collision** — the human route is equal, but the audit backend or modifiers preserve the meaningful difference;
2. **false collision** — two mechanisms that should be separated at the chosen granularity receive the same complete projection.

Only the second is a failure.

## 2. Required non-collisions

| Pair or group | Observed separation | Result |
|---|---|---|
| A14 vs A15 vs A23 | `C2` endpoint versus `C3` horizon, and `VD→VU` versus `VD`, with different ordered-L programs | PASS |
| A16 vs A17 | A16 keeps identity-preserving candidates and a common `D2/PB` resolver; A17 emits one joint sample with `D4/P∅` | PASS |
| A19 vs A03/A07/A20 | A19 has action→future→revised-action feedback (`D3/RR`, `Tr=P`); the others are direct one-way future-conditioned policy paths (`D1/R0`) | PASS |
| A08/A09/A12/A13/A18/A22 vs A03/A07/A20 | Training-only carriers map to `C@T/D∅/W0`; runtime carriers map to `C@R/D1/W4` or related online W values | PASS |
| A02/A06/A21 vs planning artifacts | Generation-only terminal output maps to `D5/P=N/A/RG`; it is not incorrectly treated as a planner resolver | PASS |
| A04 vs A22 | Both drop the world artifact before deployment, but ordered learning provenance differs (`LR` imagined latent environment versus `LC→LR` simulator criterion) | PASS |
| A05/A17 vs A16 | Joint-generation route is separated from generate-then-evaluate route by `D4/P∅/V=N/A` versus `D2/PB/V=VU` | PASS |

No required non-collision collapsed to an identical complete normative signature.

## 3. Expected human-layer collisions

The following equalities are intentional and do not indicate an ontology defect:

- A03, A07, and A20 are all direct policies whose deployed online carrier is a future sequence and whose output is not selected from an explicit candidate bank. Occupancy/latent/token realization is below the human route layer.
- A08, A09, A12, and A13 are predictive-transfer or shared predictive-learning systems whose world branch is training-only. Their learning macros and target/drop modifiers remain in the audit layer.
- A02, A06, and A21 are world-generation/simulation outputs rather than action resolvers. Their exact control provenance and realization are modifiers.
- A04 and A22 are direct action policies trained with a world/simulator branch that is absent at deployment. Their learning DAGs are not identical even though their headline deployment route is close.

This is the intended meaning of `R–W–E ⊕ L`: it exposes a route family while retaining the ordered backend for non-identical learning programs.

## 4. Pressure cases

### 4.1 A05: shared autoregressive world–action tokens

The existing representation is `C5@R + X4 + D4 + P∅ + V=N/A`, with `RJ+W5+E0` at the human layer. The unresolved point is evidentiary: the frozen D01 skeleton does not fully prove whether the planning mode emits a genuinely joint world–action carrier at deployment or merely shares a sequence backbone before action decoding.

This is an `EVIDENCE_GAP`, not a `STRUCTURAL_MISS`. If the causal interface is later disproven, the artifact can be remapped to a direct route without adding an axis.

### 4.2 A16: generate-then-evaluate with joint futures

A16 combines two semantic facts that are easy to confuse: each sample is a joint ego/agent future (`C5`-like realization), but candidates are identity-preserving and go through a common evaluator. The legal existing expression is a multi-carrier/composed projection:

```text
C={C3@R, C5@R}; X=X4; D=D2; P=PB; V=VU
```

The decisive resolver carrier is the candidate future sequence, so the human projection is `RB+W4+EV` with a joint-generation modifier. No new “joint candidate” axis is needed.

### 4.3 A19: reciprocal guidance versus mere solver iteration

A19 is a useful attack on the `D3/RR` boundary. The process is not classified as reciprocal merely because it uses diffusion steps. Its qualification comes from the semantic loop:

```text
current action hypothesis → predicted future latent → revised denoising action hypothesis
```

The future latent is computed from a trajectory intent derived from the current noisy action sample and is fed back into the same planning process. Therefore `Tr=P` and `D3/RR` are justified. A diffusion implementation with no action-indexed future branch would remain `Ts=P, Tr=A` and would not qualify.

### 4.4 A04 and A22: world model as training environment

Both are common sources of false `W` assignments. The world/simulator can be computationally substantial and still be `C@T`, `D∅`, and `W0` if the deployed planner does not consume it. The ordered-L field carries the difference between imagined actor–critic learning and simulator-criterion policy optimization.

### 4.5 A10 and A11: unresolved commitment/resolver

`PU`, `DU`, `UNKNOWN`, and `WU` are used to prevent evidence gaps from becoming invented candidate routes. Neither artifact is allowed to become `PB` or `RB` until a common resolver and final commitment path are actually evidenced.

### 4.6 A18: branch coupling without online carrier

A video expert jointly trained with an action expert does not automatically create a runtime carrier. Existing ordered-L modifiers can record interface-only coupling and branch drop. This is a wording/verification issue, not a missing axis.

## 5. D01.1 diagnostic-probe audit

| Probe | Regression finding |
|---|---|
| `runtime role` | Correctly exposes `training improvement`, `representation transfer`, `simulation`, and `generation only` cases that must not be called online planning world carriers. It is a lifecycle label, not a new route axis. |
| `world dependency type` | Correctly separates `training-only predictive`, `online predictive state`, `online rollout`, `candidate-conditioned consequence`, and `joint generation`. Existing `C` plus lifecycle/realization modifiers already express these semantics. |
| `action commitment relation` | Correctly diagnoses `before world`, `after world`, `through world`, and `independent`; existing `D/P/R` plus `X` and `T` represent the causal distinction. |

The probes find boundary questions but do not produce a false collision that requires a fourth headline axis.

## 6. Counterexample checks

- Ordinary BEV/RGB/latent encoding without a qualifying stateful world operation remains below `C` and maps to `W0`.
- Multiple random samples without identity persistence and a common resolver remain direct sampling, not `PB/RB`.
- A training future predictor removed before deployment remains `C@T/D∅/W0`, with its contribution recorded in `L`.
- A runtime scorer based on a world-derived criterion but without an online carrier may be `RB+W0`, as long as `D2/PB/V` are evidenced.
- Diffusion/flow/AR iterations alone create `Ts`, not `D3/RR`.
- An endpoint carrier and a physical horizon carrier remain separated by `C2/W3` versus `C3/W4`.

## 7. Collision verdict

```text
false collisions: 0
required separations passed: 7/7
pressure cases needing human wording/evidence review: A04, A05, A10, A11, A16, A18
new axis required: no
```

The pressure cases are retained in the backend as modifiers, compositions, or UNKNOWN states. None justifies automatic ontology expansion.
