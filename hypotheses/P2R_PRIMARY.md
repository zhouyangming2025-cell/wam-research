# P2R_PRIMARY — Reactive Action-Ordering Gap in Planning-centric WAMs

**Status:** `PRIMARY CANDIDATE, NOT CONFIRMED GAP`
**Current stage:** `Targeted Failure Deep Read — Round 1 complete`
**Last scientific review:** 2026-09-13

## Definition

For the same current state `s` and the same ego candidate set `A = {a_i}`, ask whether the candidate ordering induced by factual / non-reactive futures differs from the ordering under reactive counterfactual futures:

```text
rank_factual/nonreactive(A) ?= rank_reactive(A)
```

The scientific mechanism of interest is deliberately narrow:

```text
ego action
→ surrounding-agent response changes
→ candidate action ordering reverses
→ non-trivial planning regret
```

This is **not** a generic open-loop / closed-loop gap and is **not** equivalent to saying that a world model should be reactive.

## Scope exclusions

The following do not establish P2-R on their own:

- closed-loop performance is worse than open-loop;
- interaction modeling improves planning;
- an action-conditioned world model exists;
- a reactive simulator is more realistic than log replay;
- prediction quality and planning quality are imperfectly correlated;
- candidate-specific futures improve a non-reactive benchmark;
- the candidate set itself changes across evaluation regimes.

A convincing P2-R result must isolate `other-agent reaction to ego intervention` from observation shift, low-level control error, generic temporal compounding, and candidate-coverage changes.

## Current evidence

Round-1 review of the existing repo corpus is recorded in:

`audits/literature/P2R_TARGETED_FAILURE_DEEP_READ_ROUND1.md`

Current findings:

- **SafeDrive:** candidate-conditioned sparse worlds and explicit safety scoring are already occupied; this weakens broad "condition on ego candidates" novelty but does not directly measure factual-vs-reactive ordering inversion.
- **BeTop:** reactive closed-loop gains and interaction-aware planning are already established; this kills generic "reactivity matters" framing, but it does not hold the state and candidate set fixed and measure reaction-induced preference reversal.
- **GraphAD:** explicit future interaction structure improves planning, but there is no reactive matched-action evaluation.
- **RiskWorld:** relation-aware future rollout can preserve planning-relevant risk information, but it is history-only and not candidate-action-conditioned.
- **DA-WAM:** strongest current nearest prior. It already performs candidate-specific future prediction and candidate-specific scoring. However, offline logs directly supervise future prediction only for the expert-matched candidate; reviewed evaluation is NAVSIM-v1/v2, not a matched reactive closed-loop ordering test.

## What is already occupied

Do not use any of the following as the research problem or novelty claim:

```text
Planning should model interactions.
Reactive / closed-loop evaluation matters.
World models should be conditioned on ego actions.
Each candidate should receive its own predicted future.
Future information can improve candidate scoring.
```

## What still survives

The precise variable still not established in the five reviewed papers is:

```text
P[ rank_F(A) != rank_R(A)
   | fixed state, fixed candidate set, interaction-critical regime ]
```

with the causal attribution restricted to surrounding-agent response to ego intervention.

## Evidence verdict after Round 1

```text
NO DIRECT OBSERVED P2-R FAILURE HAS YET BEEN ESTABLISHED.
```

The current corpus shows strong nearest-prior pressure and architectural relevance, but does not yet establish the existence, prevalence, or planning regret of reaction-induced action-order inversion.

Therefore:

```text
P2-R SURVIVES ROUND 1 AS A QUESTION, NOT AS A CONFIRMED GAP.
```

## Hard kill criteria

Kill P2-R rather than broaden it if any of the following is found:

1. Strong prior art already measures matched-state, matched-candidate factual-vs-reactive ordering and substantially resolves the problem.
2. Ordering inversions are rare or induce negligible planning regret in interaction-critical scenes.
3. Apparent inversions are mainly explained by observation shift, control error, temporal compounding, or changed candidate coverage rather than surrounding-agent response.
4. Existing candidate-conditioned methods such as DA-WAM / SafeDrive already preserve reactive ordering under a direct controlled test.
5. The remaining contribution is only a new metric or naming for an already-established interactive-planning phenomenon.

## Next targeted literature set

Priority:

1. BridgeSim
2. ReactSim-Bench
3. CausalDrive
4. How Can Driving World Models Do Counterfactual Prediction?
5. CRAFT

Secondary only if needed:

- What Truly Matters
- Policy World Model
- BeyondDrive
- ELF-VLA

## Current rule

No method design is authorized yet.

The next stage is to attack P2-R with the direct reactive / counterfactual literature above. If the precise ordering variable is already occupied, or if direct failure evidence does not emerge, return `NONE` rather than widening the problem.