# D01.2-R2 R1 Audit Corrections

Status: **R1 corrections applied; R2 closeout in progress**

Baseline: `codex/ontology-stabilization-d01-2-r1` at `61494f61bb152dce8388baff0c49998b1a5e3eea`

R2 preserves `d01_2/` and `d01_2_r1/` as historical records. Only the approved normative files `09_ONTOLOGY_SPEC_S1_PLUS.md`, `12_HUMAN_ROUTE_SIGNATURE_PROPOSAL.md`, and the new amendment record `15_D01_2_COMPOSITION_AMENDMENT.md` are changed outside the new R2 directory.

## Corrections applied

### 1. Realization modifiers

The only legal realization modifiers are:

```text
direct | surrogate | generative_internal | unknown
```

R1 used undefined modifiers in four groups:

| R1 expression | R2 expression | Reason |
|---|---|---|
| A02/A06/A21/A22 `generative` | `generative_internal` | The generator/process is the carrier realization; `generative` is not a legal modifier. |
| A13/A17 `joint` | `direct` | C5 already carries joint world/action semantics; realization must not duplicate that semantic word. |

No new modifier was introduced.

### 2. Online clock topology

T records online progression only. A training-only future sequence does not create an online physical-horizon clock. R2 sets `Th=A` for:

```text
A04, A08, A09, A12, A18, A22
```

Their training horizon remains visible in `C@T`, the ordered L route, and the evidence sentence. The corrected training-only rows use `T=(A,A,A,U)` unless another online clock is independently evidenced.

### 3. A11 X binding

A11 is a current structured world carrier without evidence that an action/control variable indexes or changes that carrier. Its corrected binding is:

```text
C1@R{direct}; X=N/A; D1; P=∅; V=N/A
```

This is not the same as the general future-carrier rule `X=∅`. N/A is correct here because the current carrier type/lifecycle is not action/control-indexable in the scoped artifact.

### 4. A16 X binding and composition

The approved A16 projection removes the rejected `X3@resolver`:

```text
C5@R{direct}[k]
X=X4
D=D2⟨C5{k} -> V{k} -> resolver -> A*⟩
P=PB
V=VU
T=(P,A,P,U)
L=LC->LR
```

Gen-Drive candidates are born from independent noise in the joint world/action generation process. Candidate identity is preserved through P/D and the common resolver. X3 is recorded only when an external or upstream candidate action actually conditions the carrier.

## R2 schema pass criteria

Every final row is checked against:

1. legal C code, lifecycle, and realization;
2. one X binding for each applicable carrier;
3. D global constraints, including the approved C5[k] D2 form;
4. P/V constraints and declared A*;
5. online-only T fields;
6. ordered L macros and deployment fate;
7. explicit retain/drop or UNKNOWN boundaries.

## Expected R2 result

The R1 errors are projection-level corrections. The A16 amendment is a composition clarification using existing values. The expected closeout is:

```text
new axis = 0
deleted axis = 0
new R/W/E code = 0
canonical core-12 headline changes = 0
```

The full acceptance result is recorded only after the 23-artifact, collision, core-12, canonical-21, and DA-WAM regressions in the following files.
