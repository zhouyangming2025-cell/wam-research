# P2R_PRIMARY — Reactive Action-Ordering Gap in Planning-centric WAMs

> **Historical filename retained for provenance. P2-R is no longer the active research target.**

**Status:** `PARKED PROBE — NOT ACTIVE SEARCH TARGET`
**Last active hypothesis review:** 2026-09-13
**Parked:** 2026-09-14 during field-reconstruction reset

## Why it is parked

The project recognized that it had started gap hunting too early: a small, hypothesis-biased paper set was being used to invent and then falsify candidate gaps before the planning-centric WAM field had been reconstructed as a whole.

P2-R remains a useful scientific question, but the reading program must not be organized around proving or killing it.

Active program:

`landscape/FIELD_RECONSTRUCTION_PLAN.md`

## Historical definition

For the same current state `s` and the same ego candidate set `A = {a_i}`, ask whether the candidate ordering induced by factual / non-reactive futures differs from the ordering under reactive counterfactual futures:

```text
rank_factual/nonreactive(A) ?= rank_reactive(A)
```

Historical mechanism of interest:

```text
ego action
→ surrounding-agent response changes
→ candidate action ordering reverses
→ non-trivial planning regret
```

This is narrower than a generic open-loop / closed-loop gap and is not equivalent to saying that a world model should be reactive.

## Historical Round-1 result

Audit:

`audits/literature/P2R_TARGETED_FAILURE_DEEP_READ_ROUND1.md`

Result:

```text
NO DIRECT OBSERVED P2-R FAILURE HAS YET BEEN ESTABLISHED.
P2-R SURVIVES ROUND 1 AS A QUESTION, NOT AS A CONFIRMED GAP.
```

The earlier review also established that broad claims around interaction-aware planning, reactive evaluation, action-conditioned world modeling, candidate-specific future prediction, and future-conditioned scoring are already heavily occupied.

## How to use P2-R now

P2-R may be used as **one diagnostic lens** when reading papers about:

- interactive prediction/planning;
- candidate-conditioned futures;
- reactive simulation;
- counterfactual prediction;
- world-model-based candidate scoring.

It must not determine which papers count as important to the field.

## Reactivation condition

Reopen P2-R only after the field atlas is mature enough to show that this question emerges naturally as a recurrent unresolved planning issue across multiple independent method families and evaluation regimes.

If the broader field reconstruction points elsewhere, leave P2-R parked or retire it.

## Historical hard kill criteria

If P2-R is ever reactivated, kill it rather than broaden it if:

1. matched-state / matched-candidate factual-vs-reactive ordering is already substantially solved;
2. ordering inversions are rare or induce negligible planning regret;
3. apparent inversions are mostly caused by observation shift, control error, temporal compounding, or candidate-set change rather than surrounding-agent response;
4. existing candidate-conditioned methods preserve reactive ordering under direct controlled evaluation;
5. the remaining contribution is only a new name/metric for an established interactive-planning phenomenon.
