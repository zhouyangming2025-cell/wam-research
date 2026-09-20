# Claim-First Teaching and Evidence-Grounded Note Protocol

Use this reference for first-pass teaching, paper synthesis, novelty positioning, selective cross-paper comparison, experiment review, and final research notes.

## 1. Establish the source and artifact boundary

Record what was checked:

- paper version and supplement;
- official code or absence of verified code;
- evaluation artifact and task mode;
- related-paper comparison set;
- unresolved implementation details.

Preserve distinctions among paper facts, code facts, author claims, direct evidence, mathematical consequences, literature synthesis, inference, teaching constructions, and unknowns.

## 2. Build a ranked claim map

Extract the smallest useful set of primary claims—usually two to four—using the introduction, contribution list, method structure, deployment graph, and experiments together. Do not use the contribution list alone.

Classify method elements into:

| Level | Test |
|---|---|
| Primary claim | Removing it changes the paper's scientific identity. |
| Supporting mechanism | It solves a technical obstacle created by a primary claim. |
| Generic component | It is a routine tool used to implement the method. |

For each primary claim, record:

```text
problem addressed
→ proposed change
→ minimum mechanism
→ intended benefit
→ deployment role
→ evidence
→ strongest remaining alternative explanation
```

An ablated component is not automatically novel, and an unablated component is not automatically unimportant.

## 3. Audit the problem statement

Separate:

- **field-level fact** — supported across relevant literature;
- **subset pattern** — true for some checked approaches;
- **author framing** — motivation that may compress or exaggerate prior work;
- **paper-specific target** — the precise limitation this method actually changes.

Do not repeat “most prior work” or “existing methods all…” without checking the relevant comparison set. Translate different papers' terminology into a common functional description before judging similarity.

## 4. Explain the minimum viable mechanism

For each primary claim, state only what is required to understand it:

- input and condition;
- predicted or edited object;
- supervision source;
- shared versus separate modules/parameters;
- training-only versus deployment-time role;
- representation advantage and cost.

Defer internal projections, tensor arithmetic, gradient derivations, and optimizer details unless the detail-value gate passes.

## 5. Use an evidence ladder

Match conclusions to the strongest demonstrated level:

1. **Responsiveness** — model output changes when the condition or component changes.
2. **Task relevance** — the change correlates with or improves a task metric.
3. **Matched attribution** — a controlled ablation isolates the component's contribution.
4. **Intervention validity** — predicted alternatives match real or externally validated consequences.
5. **Deployment utility** — the mechanism improves the actual online/closed-loop system under the claimed regime.

A lower-level result can still be valuable. State what it establishes instead of dismissing it for not reaching a stronger level. Conversely, do not upgrade correlation, internal self-consistency, or non-reactive evaluation into causal or reactive validation.

For each experiment, ask:

- Which claim is this intended to test?
- What changed between rows or conditions?
- What else changed at the same time?
- Is the metric matched to the claimed capability?
- Is the evaluation open-loop, pseudo-simulation, non-reactive, reactive simulation, or real-world?
- What conclusion is supported, and what stronger conclusion remains unproven?

## 6. Compare papers by mechanism family

Choose the comparison axis before choosing papers. Group only relevant works into families such as:

- continuous latent prediction;
- discrete token prediction/editing;
- auxiliary future supervision;
- online future-conditioned policy;
- candidate consequence evaluation;
- shared world-policy generation;
- direct action or trajectory generation.

Use three labels:

- **Common foundation** — broadly shared idea or routine practice.
- **Route choice** — one of multiple established design families.
- **Paper-specific design** — a distinctive mechanism or combination within the checked evidence.

Summarize prevalence and differences at the family level. Do not march through every paper, force irrelevant comparisons, or infer uniqueness from absence in a small list.

## 7. Separate lifecycle from architectural jointness

For every world/policy or multi-task paper, record:

```text
training-time future/world computation
→ gradient or representation bridge
→ downstream adaptation
→ mandatory deployment graph
```

Strong parameter sharing does not imply online future simulation. A paper with separate modules may use future consequences explicitly at deployment, while a highly unified model may retain only a policy path.

Also separate physical future time from diffusion, flow, token-edit, or refinement iterations.

## 8. Research-note template

Adapt the length to the request; do not populate sections with filler.

```markdown
# Paper title and one-sentence position

## Problem addressed
- Field-level problem
- Precise paper target

## Core claims and contributions
| Primary claim | Minimal mechanism | Common foundation / route choice / paper-specific design | Evidence | Judgment |

## Implementation mainline
- Representation choices
- Training tasks/stages
- Inference/deployment path
- Key supervision

## Evidence audit
- Headline capability results
- Matched ablations
- Counterfactual or qualitative evidence
- Evaluation regime

## Relation to relevant mechanism families
- Aggregated comparison only

## Limitations and unproven claims

## Final assessment
- Well supported
- Promising but under-isolated
- Conclusions not licensed by the evidence
- One-sentence memory anchor
```

The core table is the organizing surface. Avoid repeating the same claim in prose, another table, a flow, and the conclusion unless each occurrence adds a new relationship.

## 9. Synthesis check

Before delivering a first explanation or note, verify:

- Is the primary-claim set as small as the paper permits, without hiding a scientifically distinct claim?
- Are supporting mechanisms and generic components visibly subordinate?
- Did experiments help identify the paper's intended claims without being mistaken for novelty proof?
- Is every novelty statement scoped to checked literature?
- Is the deployment graph explicit?
- Are strong scores separated from causal attribution?
- Are limitations calibrated to the paper's actual claim level and field maturity?
- Have low-value computation details been deferred rather than silently expanded?
