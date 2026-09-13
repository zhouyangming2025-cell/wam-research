# RESEARCH_PRINCIPLES

Canonical scientific operating rules for this project.

Last updated: 2026-09-13

## 1. Scope

Primary research scope:

```text
World Model + End-to-End + Planning-centric autonomous driving
```

The project is not perception-centric and is not a generic world-generation project. A paper can be technically impressive yet peripheral if its contribution does not materially affect planning, decision making, interaction reasoning, evaluation of planning, or the coupling between future modeling and action selection.

## 2. Prior expertise is an asset, not a destination

The owner has strong prior expertise in driving risk, predictive risk fields, safety representation, future interaction compression and trajectory-based risk analysis.

This expertise may become useful, but **risk field is not a required component of the final research direction**.

Forbidden workflow:

```text
we know risk fields
→ search for a place to insert a risk field into WAM
```

Required workflow:

```text
observed planning failure
→ failure cause
→ missing capability
→ why existing methods do not already solve it
→ research question
→ test / falsification
→ only then inspect whether prior risk knowledge helps
```

A final contribution that uses none of the legacy risk-field machinery is acceptable if the problem is stronger.

## 3. Problem-first evidence chain

A legitimate research gap should approximately satisfy:

```text
Observed Failure
→ Failure Cause
→ Missing Capability
→ Why Existing Method Cannot Easily Handle It
→ Research Question
→ Possible Method
```

A missing module is not a gap. A new representation is not a gap. A fashionable architecture is not a gap.

## 4. Symmetric treatment of every paper

Every paper has strengths, limitations, assumptions and evaluation boundaries. Do not read papers as "supporters" or "opponents" of our current hypothesis.

For every core paper, explicitly record:

```text
Strongest evidence in favor of the paper's claim
Strongest limitation / alternative explanation
What the paper proves
What the paper does NOT prove
Which broad claims it already occupies
Which residual question remains
```

Do not attack papers merely because they threaten our hypothesis; do not excuse weaknesses merely because they support it.

## 5. Evidence taxonomy

Keep separate:

```text
AUTHOR CLAIM
DIRECT EXPERIMENTAL EVIDENCE
OUR INFERENCE
```

If the paper does not report a failure, say:

```text
NO DIRECT OBSERVED FAILURE REPORTED
```

If a mechanism is plausible but untested, label it inference. If a metric is only a proxy, do not silently upgrade it into the target property.

## 6. Evaluation regimes must remain distinct

Never collapse the following into one category:

```text
open-loop offline trajectory evaluation
non-reactive closed-loop / log-replay simulation
reactive closed-loop simulation
world-model visual rollout
real-vehicle closed-loop testing
```

A multi-step rollout is not automatically closed-loop. A candidate-conditioned predictor is not automatically reactive. A reactive simulator is not proof that the policy has learned the correct counterfactual model.

## 7. Planning coupling must be traced concretely

For planning-centric WAM papers, always ask:

```text
What is the input?
What numerical representation is produced?
What is predicted about the future?
What is directly supervised?
What is only latent / inferred?
How does the planner consume it?
Does it change candidate generation, scoring, refinement, or direct trajectory decoding?
What remains at inference time?
```

Do not infer decision usefulness from visual fidelity or representation richness alone.

## 8. Prior-art occupancy vocabulary

Use:

```text
CONCEPT_PRECEDENT
STRONG_NEIGHBOR
DIRECT_OCCUPATION
EFFECTIVELY_SOLVED
NOT_RELEVANT
```

A paper containing a similar component is not automatically direct occupation. Conversely, a paper need not use our terminology to occupy the same scientific question.

## 9. Counterexamples matter

One strong counterexample can kill a universal claim.

Examples already learned in this project:

- DriveLaW weakens any claim that an explicit risk/value interface is always necessary.
- NPPC weakens any universal claim that optimization over a learned cost necessarily produces harmful exploitation.
- BeTop weakens broad claims that logged-data learning cannot yield useful reactive planning behavior.
- DA-WAM weakens broad claims that per-candidate action-conditioned futures are missing from planning-centric WAMs.

Use counterexamples to narrow or kill hypotheses rather than adding exceptions until the claim becomes unfalsifiable.

## 10. Reading-depth policy

Not all papers deserve equal effort.

### Tier A — hypothesis-deciding
Deep read method, supervision, inference, evaluation, ablations, failures and limitations. Source-code audit only if the scientific question requires it.

### Tier B — planning-centric landscape anchors
Understand architecture, planning coupling, training/evaluation and major evidence; deep-dive only where they bear on the active hypothesis.

### Tier C — boundary / counterexample / historical controls
Read the portions needed to test a specific claim. Do not perform exhaustive reproduction without a decision-relevant reason.

## 11. Corpus expansion policy

Expand by **problem**, not by keywords.

Current policy: freeze broad expansion after the targeted direct P2-R set plus a small historical interactive-planning control set. Only add further papers if a concrete unresolved scientific question points to them.

Avoid building a large archive faster than it can be scientifically digested.

## 12. Method-design gate

No method design until a problem survives:

1. direct prior-art attack;
2. strongest alternative explanations;
3. realistic evaluation relevance;
4. counterexamples;
5. a falsifiable test showing the failure exists and matters.

`NONE / EVIDENCE INSUFFICIENT` is an acceptable research outcome.

## 13. P2-R-specific discipline

Current P2-R candidate must remain narrow:

```text
fixed state + fixed action set
factual/non-reactive ordering vs reactive counterfactual ordering
reaction-induced ordering reversal
non-trivial planning regret
```

Do not widen it to generic OL→CL mismatch, reactive simulation, interaction modeling, or action conditioning if the narrow question fails.

## 14. Research-state authority

Scientific decisions live in this repo, especially:

```text
START_HERE.md
state/CURRENT_STATE.md
state/DECISION_LOG.md
state/NEXT_TASK.md
state/RESEARCH_LEDGER.md
hypotheses/
audits/
papers/cards/
handoff/LATEST.md
```

Conversation summaries are temporary. The repo is canonical.
