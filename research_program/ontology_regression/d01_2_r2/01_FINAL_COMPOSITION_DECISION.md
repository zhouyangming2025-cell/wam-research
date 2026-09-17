# D01.2-R2 Final Composition Decision

## Decision

The A16 composition amendment is **approved and applied**.

## Gen-Drive A16 mechanism

```text
S + noise_k
  -> C5[k] = (world[k], action[k])
  -> V[k]
  -> common resolver
  -> A*
```

There is one carrier per sampled candidate. The carrier is jointly born from world/action variables, and its identity survives to a common evaluator. There is no second independent C3 carrier.

## A16 final audit signature

```text
C = C5@R{direct}[k]
X = X4
D = D2⟨C5{k} -> V{k} -> resolver -> A*⟩
P = PB
V = VU
T = (P,A,P,U)
L = LC->LR
```

Human signature:

```text
RB + W5 + EV ⊕ LC->LR
```

## Why X3@resolver is rejected

X answers what action/control variable indexes or generates the carrier. A16's joint sample is generated from noise and joint world/action variables, so `X4` is complete. Candidate identity is a P/D property:

```text
candidate birth -> identity preservation -> common resolver -> A*
```

Adding `X3@resolver` would incorrectly claim a second carrier-conditioning edge. If an upstream candidate action `A{k}` actually conditions `C5{k}`, an audit record may additionally record X3 for that carrier. Gen-Drive does not establish that condition.

## H1/H2/H3 resolution

| Hypothesis | Result | Reason |
|---|---|---|
| H1: independent C3 and C5 carriers | REJECTED | The scored object is one joint future; C3+C5 duplicates it. |
| H2: candidate-indexed C5 with common resolver | ACCEPTED | Independent samples keep identity through one evaluator and produce A*. |
| H3: D4 alone | REJECTED for A16 | D4 remains correct only for direct joint emission without a downstream common resolver. |

## A16 versus A17

| Artifact | Final route | Resolver |
|---|---|---|
| A16 | `RB+W5+EV` | Multiple C5[k] samples enter a common evaluator. |
| A17 | `RJ+W5+E0` | One joint C5 sample directly emits action; no common runtime resolver. |

## Normative consequences

- C5 accepts candidate key `[k]` for jointly born candidates.
- D2 accepts C2/C3 action-conditioned consequences and C5[k] joint-born consequences.
- D2/PB require identity preservation, non-N/A V, and A* in both forms.
- D4/RJ remains direct joint emission without downstream common resolver.
- W5 is legal with RB as well as RJ.
- No D6, no new X code, and no new R/W/E code are introduced.
