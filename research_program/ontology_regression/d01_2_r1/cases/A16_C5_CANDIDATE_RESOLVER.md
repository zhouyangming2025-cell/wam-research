# A16 Pressure Case — Candidate-Indexed Joint Future with Resolver

Artifact: A16, Gen-Drive multiple-sample planning mode.

## Observed graph

```text
S + noise_k
  → joint ego/agent future C5{k}
  → common scene evaluator
  → selected ego trajectory A*
```

The same candidate-indexed joint future is both the generated world/action carrier and the object consumed by the common resolver.

## Failure of the first-round encoding

The first-round C3+C5 projection duplicates one semantic object. The D4-only projection loses the distinction between one joint sample and a candidate bank resolved by a common evaluator.

## Proposed existing-axis composition

```text
C5@R[k]
X4@birth + X3@resolver
D2⟨C5{k}⟩
P=PB
V=VU
```

This is a composition clarification, not a new axis. It remains held until the global D2 admissibility rule is approved for candidate-indexed C5 consequences.
