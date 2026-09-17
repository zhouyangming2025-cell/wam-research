# D01.2-R1 Review Findings

Status: **closed-set regression complete; ontology amendment not applied**

Base: `codex/ontology-stabilization-d01-2` at `c13653f4c2af54f96f159079ed6a9e0ce077792c`

Scope: the 23 frozen D01 artifacts (`A01–A23`). This review preserves the two-layer mechanism map:

```text
human route:       R–W–E ⊕ L
normative backend: C–X–D–P–V–T–L
```

The D01.1 three-field probe is used only as diagnostic evidence. It is not converted into a parallel taxonomy or a new signature.

## Freeze

- `research_program/domain_corpus/d01/` is treated as frozen input.
- `research_program/ontology_regression/d01_2/` is treated as a frozen first-round audit record.
- `outputs/core_mechanism_12_v1/` and `handoff/core_mechanism_12/` are protected.
- No new axis, deleted axis, or canonical headline signature is introduced in R1.
- All 23 artifacts are projected in one closed set before any repair is proposed.
- `UNKNOWN` is used where the artifact or version boundary cannot be established; `N/A` is used only where a field is semantically inapplicable.

## Review findings

### 1. The ontology survives the broad regression

The first-round mechanism distinctions remain useful:

- direct action versus candidate-bank commitment;
- current/future/joint carrier roles;
- resolver semantics separate from carrier type;
- decision-internal reciprocal refinement separate from ordinary solver steps;
- ordered learning and deployment fate separate from runtime topology.

No collision was found that requires a new top-level axis.

### 2. Several first-round values were schema errors, not ontology failures

The most repeated error was using `X=N/A` for an applicable future carrier that simply had no action/control condition. Under the specification this is `X=∅`, not `N/A`. The affected boundary cases are A03, A07, A08, A09, A10, A12, A13, A18, and A20; A13 is additionally corrected to `X4` because its runtime carrier is joint world/action generation rather than an unconditioned forecast.

The second repeated error was allowing a physical future-horizon clock on a carrier that is only a future endpoint. A19 therefore changes from `Th=present` to `Th=absent`; its real distinction is `Tr=present` because a provisional action is fed back into future prediction during the same diffusion decision.

### 3. Evidence closure changes labels without changing the route ontology

- A01 has a known decomposed planning resolver, so its `V` is `VD`, not unresolved.
- A10 has a real candidate retrieval/scoring/gating path; its `P` is `PB`, `D` is `D1` rather than candidate-consequence `D2`, and its resolver semantics are `VD`.
- A11 is a current structured world carrier with direct policy use; the remaining uncertainty is learning/deployment detail, not the existence of a candidate resolver.
- A20 predicts an online future token horizon used by a direct action decoder; it is `X=∅`, not `N/A`.

### 4. A16 is a genuine composition pressure case

Gen-Drive does not provide two independent carriers. The scored object is one candidate-indexed joint world–action future, `C5{k}`. Its identity survives to a common evaluator, which then commits the selected ego trajectory. The first-round `{C3,C5}` projection duplicated one semantic object and incorrectly forced `D4` to serve as the complete route.

The existing axes can express the mechanism if composition is made explicit:

```text
C5@R[k]
X4@birth + X3@resolver
D2⟨C5{k}⟩
P=PB
V=VU
```

However, the current global constraint says that D2 consumes a C2/C3-like consequence. Accepting a candidate-indexed C5 joint consequence therefore requires a small normative clarification. The proposal is recorded, but deliberately held for human approval.

### 5. A05 remains an evidence boundary

DrivingGPT clearly unifies visual and action tokens at paper/objective level, but the inspected evidence does not prove that the NAVSIM planning path emits and consumes every future visual token before producing the deployed action. It must remain a version/mode-specific `UNKNOWN` runtime projection rather than being promoted to `RJ` or `D4` by architectural language alone.

## R1 disposition counts

The detailed matrix records one primary result per artifact:

| Result | Count | Meaning |
|---|---:|---|
| `PASS` | 9 | Existing projection is legal under the frozen schema; remaining uncertainty is an audit attribute. |
| `SYNTAX_ERROR` | 0 | No malformed signature grammar was found. |
| `TYPE_CONSTRAINT_ERROR` | 9 | A value violates a frozen type/lifecycle constraint and is remapped in the corrected projection. |
| `EVIDENCE_REQUIRED` | 4 | The structure is legal but a stronger value needs targeted evidence or version scoping. |
| `POSSIBLE_COMPOSITION_GAP` | 1 | A16 needs an explicit composition clarification before it can be accepted as a fully legal canonical projection. |

The count is about the first-round projections, not about paper quality. A `TYPE_CONSTRAINT_ERROR` is usually repairable by a value correction; a `POSSIBLE_COMPOSITION_GAP` is the only item that creates structural pressure.

## Review conclusion

The two-layer ontology is preserved. R1 does **not** justify a new axis or a second taxonomy. It does justify a held, minimal composition clarification for A16 and a set of projection corrections. The formal verdict is therefore deferred to `08_REVISED_VERDICT.md` and is not silently upgraded by this document.
