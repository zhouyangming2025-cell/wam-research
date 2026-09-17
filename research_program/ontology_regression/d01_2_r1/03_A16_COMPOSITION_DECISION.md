# A16 Composition Decision — Gen-Drive

## Question

Can Gen-Drive be represented by the frozen ontology without inventing a paper-specific category?

## Evidence-grounded mechanism

The audited paper describes a generation-then-evaluation planner:

```text
S + independent noise_k
    → joint ego/agent future scenario C5{k}
    → common scene evaluator
    → selected ego trajectory A*
```

`C5{k}` is the single semantic object that contains the joint world/action future for candidate `k`. The evaluator compares several such objects. No separate endpoint consequence and no independent horizon carrier are needed.

## Hypothesis tests

### H1 — Two independent carriers

```text
C3{k} + C5{k} → resolver
```

Rejected. The paper does not expose an independently scored endpoint/horizon consequence in addition to the joint scenario. Treating the same generated scenario as both C3 and C5 duplicates the object and creates a false complexity.

### H2 — One candidate-indexed C5 carrier with a resolver

```text
C5{k} → common evaluator → A*
```

Supported. Candidate identity is created by independent samples, preserved through evaluation, and resolved to a final ego trajectory. The action/control relation has two stages:

```text
X4@birth       joint world/action generation
X3@resolver    candidate identity bound to the common selection interface
```

### H3 — D4 alone is the whole route

Rejected. D4 correctly captures the joint world/action generation process, but it does not say whether the generated object is one terminal sample or one of several candidates sent to a common resolver. A16 needs D4-like birth plus PB/D2-like resolution; A17 needs D4 without the resolver.

## Recommended composition notation

The corrected projection is:

```text
C = C5@R{direct}[k]
X = X4@birth + X3@resolver
D = D2⟨C5{k}⟩
P = PB
V = VU[learned scene preference; joint futures; pairwise VLM provenance; score; argmax]
T = (P,A,P,U)
L = LC→LR
```

Human layer:

```text
RB + W5 + EV ⊕ L[LC→LR]
```

This preserves the semantic distinction:

- `RB` describes final commitment topology;
- `W5` describes the carrier;
- `EV` describes the evaluator’s preference semantics;
- `D4` is the joint-generation birth process, not the complete final decision topology.

## Minimum amendment proposal — not applied

The frozen specification should be clarified in three places:

1. D2’s admissible consequence set should include a candidate-indexed C5 joint consequence when identity is preserved to a common resolver.
2. X binding should explicitly permit stage-qualified composition (`X4@birth + X3@resolver`) without collapsing joint generation and candidate identity.
3. W5 should be explicitly allowed to coexist with `RB`; W5 is a carrier semantic, while RB is the final commitment topology.

No new axis, code, or headline signature is needed. The amendment is held for human approval because it changes a global type constraint, even though it does not create a second taxonomy.

## Comparison with A17

| Artifact | Carrier | Resolver | Human route |
|---|---|---|---|
| A16 | candidate-indexed joint future `C5{k}` | common evaluator selects `A*` | `RB+W5+EV` |
| A17 | one joint future `C5` | absent in the deployed single-sample mode | `RJ+W5+E0` |

The split is real and is not an implementation detail.
