# D01.2 Composition Amendment

Status: **approved and applied in D01.2-R2**

Scope: minimal stabilization of the existing `C–X–D–P–V–T–L` backend and the derived `R–W–E ⊕ L` human layer.

```text
new axis = 0
deleted axis = 0
new R/W/E code = 0
canonical headline changes = 0
D02 = not started
```

## 1. Triggering counterexample

Gen-Drive A16 generates multiple independent joint ego/agent futures. Each future is a single semantic world/action carrier, candidate identity is preserved, and a common scene evaluator chooses the final ego trajectory:

```text
S + noise_k
  → C5[k] = (world[k], action[k])
  → V[k]
  → common resolver
  → A*
```

The former `C3+C5` encoding duplicated the same generated scenario. The former D4-only encoding lost the downstream candidate resolver. This was a composition gap, not a need for a new axis.

## 2. Approved decisions

Approved:

- candidate-indexed `C5[k]` may be the consequence object consumed by D2;
- `C5[k]` may be jointly born with world and action variables;
- `W5` may coexist with `RB`;
- D2/PB represent the downstream common resolver;
- D4/RJ remain for direct joint emission with no downstream common resolver.

Rejected:

- `X3@resolver` is not added to A16.

Reason: X describes the control/generation interface of a carrier. Gen-Drive candidates are born from independent diffusion noise and joint world/action generation; candidate identity is maintained by P/D through the resolver, not by an additional carrier-conditioning edge. X3 is allowed only when an external or upstream candidate action actually conditions `C5[k]`.

## 3. Normative amendment

### C5

`C5` may be candidate-indexed as `C5[k]` when each jointly born world/action sample retains its identity through a downstream resolver. The key does not itself imply action-conditioned input.

### D2

D2 now admits two forms:

```text
A{k} → C2/C3{k} → V{k} → resolver → A*

C5{k} = (world{k}, action{k}) → V{k} → resolver → A*
```

The first normally uses X3 on the candidate consequence. The second uses X4 on the joint carrier. Both require identity preservation, PB, non-N/A V, and a declared A*.

### D4

D4 means one joint world/action process directly emits the committed world/action output. If multiple joint candidates enter a common resolver, the final route is D2, not D4. No D6 is introduced.

### W5

W5 is the primary online joint world/action carrier role. It may map from runtime C5 through D4 or through candidate-resolution D2. Therefore `RB+W5` is legal, while `RJ+W5` remains direct joint emission without a downstream resolver.

## 4. Exact normative file changes

### `09_ONTOLOGY_SPEC_S1_PLUS.md`

1. Added candidate indexing `C5[k]` to the C5 semantics.
2. Replaced the single D2 route with the two admissible forms above.
3. Updated global constraint 1 to admit either C2/C3 with X3 or C5[k] with X4, both with identity preservation, PB, V, and A*.
4. Clarified D4 as direct committed joint emission and routed multi-candidate joint cases to D2.
5. Added no new D code.

### `12_HUMAN_ROUTE_SIGNATURE_PROPOSAL.md`

1. W5 now maps from C5 through D4 or candidate-resolution D2.
2. Added the legal `RB+W5` combination.
3. Kept `RJ+W5` for direct joint emission without a resolver.
4. Kept R determined by final commitment topology.

## 5. Canonical A16 projection after amendment

```text
C = C5@R{direct}[k]
X = X4
D = D2⟨C5{k} → V{k} → resolver → A*⟩
P = PB
V = VU
T = (P,A,P,U)
L = LC→LR
```

Human layer:

```text
RB + W5 + EV ⊕ LC→LR
```

## 6. Impact review

### Core-12

No core-12 headline changes. Existing `RJ+W5` entries, including the Discrete-WAM joint mode, remain direct joint emission. The amendment only adds the previously missing `RB+W5` composition for candidate-resolved joint carriers.

### DA-WAM

DA-WAM remains `RB+W3+(ED→EV)` because its candidate-specific carrier is an endpoint consequence, not a jointly born C5 carrier. It does not inherit X4 or W5.

### A16/A17

- A16: `RB+W5+EV`, C5[k] enters a common resolver.
- A17: `RJ+W5+E0`, one joint sample emits action without a common resolver.

The distinction remains real after amendment.

### Other artifacts

No other artifact is reclassified solely because the composition rule was added. A13 remains RJ+W5; A19 remains RR+W3; SeerDrive paper/code and Drive-JEPA PF/PB remain separate.
