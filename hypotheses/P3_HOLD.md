# P3_HOLD — Decision Sufficiency of World Representations

**Status:** `HOLD AS BACKUP`
**Last updated:** 2026-09-13

## Definition

Broad phenomenon:

```text
prediction / reconstruction fidelity != planning / decision sufficiency
```

The scientifically interesting form is narrower than "learn a better planning representation":

> What future information must a world representation preserve so that downstream action preferences are preserved?

A useful conceptual form is:

```text
z1 ~ z2
iff
for the relevant candidate actions, the induced utility / preference ordering is preserved.
```

The emphasis is on **decision-relevant distinctions**, not photorealistic reconstruction or generic task-oriented feature learning.

## Why it is only backup

P3 is highly WAM-native, but the broad problem statement is heavily occupied by 2025–2026 work on:

- planning-oriented latents;
- action-oriented / world-action representations;
- future-intent latents;
- JEPA-style predictive representations;
- representation alignment for planning.

Therefore the following is **not** sufficient novelty:

```text
"world-model representations should be more planning-oriented than reconstruction-oriented"
```

The remaining potentially valuable question is whether specific future distinctions can be tied causally and operationally to action-preference preservation or reversal.

## Current evidence status

`PENDING SCIENTIFIC REVIEW` for the dedicated P3 corpus.

Existing evidence from prior research state suggests the broad framing is under strong prior-art pressure, but this file does not treat that as a final literature verdict until the relevant primary texts are ingested and audited in this repo.

## Promotion condition

P3 should be reconsidered as a primary candidate only if evidence supports a problem deeper than generic representation engineering, for example:

```text
specific future distinction
→ action preference changes
→ measurable planning regret
```

under a controlled comparison that separates representation content from backbone, data, planner, and supervision confounds.

## Current rule

No active P3 method work is scheduled while P2-R remains under targeted falsification.