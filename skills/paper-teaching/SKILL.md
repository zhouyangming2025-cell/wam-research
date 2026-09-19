---
name: paper-teaching
description: "Teach a technical research paper progressively and interactively, from the semantic mainline through mechanism, computation, mathematics, and evidence. Use when explaining or continuing to explain a paper, designing a paper-learning sequence, or repairing a learner's partial understanding. Do not use for a one-shot abstract summary that needs no teaching progression."
---

# Paper Teaching

Build an understanding the learner can reconstruct, not merely recognize while reading.

## Before teaching

1. Establish the source boundary: paper text, supplement, code, related papers, and what has not been checked.
2. Translate different papers' terminology into common technical language before comparing them.
3. Infer the learner's current layer from their questions. Never treat semantic understanding as proof of computational or mathematical understanding.
4. For multi-round teaching, confusion repair, mathematics, or cross-paper comparison, read [the teaching protocol](references/teaching-protocol.md).

## Track six understanding layers

| Layer | Learner can answer |
|---|---|
| S — Semantics | What problem is being solved, and what is the high-level idea? |
| M — Mechanism | What enters each module, what operation happens, and what exits? |
| C — Computation | What are the tensors, shapes, targets, probabilities, losses, updates, and decoding steps? |
| F — Foundations | Why does the mathematical operation work, and where does its formula come from? |
| E — Evidence | Which statements are paper facts, author claims, measured results, or interpretation? |
| T — Transfer | How does this choice differ from relevant alternative mechanism families, and when would it fail? |

Maintain a small internal state for every important concept: `unintroduced`, `semantic`, `mechanistic`, `computational`, or `reconstructable`. If the learner says “the meaning is clear, but I cannot describe the actual process,” mark S as established and C/F as unresolved. Do not repeat S with new wording.

## Default teaching progression

Teach in this order, but stop at the learner's current gate instead of forcing all stages into one answer.

1. **Orientation** — One concrete scenario, the paper's task, inputs, outputs, and one-sentence contribution.
2. **Mechanism** — Trace one sample through the system. Name modules only after explaining their jobs.
3. **Lifecycle** — Separate data preparation, training modes or stages, parameter updates, and inference. State what is shared, frozen, newly added, or discarded.
4. **Representation** — Explain what each representation preserves, makes easy, and loses. Use a concrete counterfactual: “If this paper used the alternative representation, which operations would change?”
5. **Computation** — Walk through one realistic training or inference case with stable notation, shapes, selected values, target construction, output, and update destination.
6. **Foundations** — When a prerequisite gap appears, pause the paper and teach only the shortest dependency chain needed to remove it.
7. **Evidence and comparison** — Audit claims and compare only relevant mechanism families.
8. **Consolidation** — Ask the learner to reconstruct one bounded path; repair the first missing link rather than introducing more content.

## Use a fixed round contract

Each teaching round must:

1. State the exact question being resolved.
2. Reuse one stable scenario and notation ledger.
3. Explain every step as: **current problem → why the next operation is needed → operation → result → boundary**.
4. Define every symbol next to the formula where it first appears in that round.
5. Separate training from inference and distinguish teaching examples from paper-reported facts.
6. End with `now established` and `still unresolved` in concise prose.

When the learner challenges a step, stop onward expansion. Repair that exact dependency first.

## Preserve real structure in examples

- Use realistic vocabulary sizes, tensor ranks, sequence lengths, or module structure when they matter.
- Show only a few selected or top-k entries from a large vector; do not shrink a 16,384-class problem into four classes if that changes what the learner thinks an index means.
- Keep these namespaces visibly distinct: time position, spatial position, token ID, vector index, class candidate, and iterative editing round.
- Do not replace a soft target with one-hot merely to simplify arithmetic. If a simplified teaching construction is used, say exactly what was simplified and what remains unchanged.
- Keep the same example across adjacent rounds so new detail attaches to an existing mental model.

## Enforce formula discipline

Never drop a compact formula as though it were an explanation.

- Distinguish a function such as `L(theta)` from its current evaluated value such as `L(theta_current) = 2.00`.
- Distinguish learned parameters, intermediate variables, constants, targets, and observed values.
- Before connecting one scalar loss to many parameters, establish multivariable functions, partial derivatives, the computation graph, and the chain rule or automatic differentiation.
- If a result such as `dL/ds = p - q` is needed, either derive it from already established prerequisites or label it as a result being temporarily used without derivation. Do not blur those two states.
- For soft-target cross-entropy, do not claim the minimum is zero. Explain its decomposition `H(q,p) = H(q) + KL(q || p)` when relevant: matching `p` to `q` minimizes the loss, whose minimum is `H(q)`.

If the required prerequisite is too large, open a bounded foundation detour and record where the paper explanation is paused.

## Compare papers selectively

Do not march through every paper or force comparisons with unrelated work.

1. Group relevant papers into a small number of mechanism families.
2. State whether a point is field consensus, used by a subset, or a paper-specific contribution.
3. Compare against the nearest meaningful alternatives on the same axis.
4. Normalize synonymous terminology into one shared description, while preserving important implementation differences.
5. Use calibrated scope: “several compared works,” “within the checked set,” or “this paper appears unique on this axis.” Never turn an unchecked subset into “all prior work.”

## Use explicit evidence grammar

Classify material claims as one of:

- **Paper fact** — directly stated architecture, objective, data, or procedure.
- **Author claim** — the authors' interpretation or novelty claim.
- **Direct evidence** — supported by an experiment, table, figure, ablation, or theorem.
- **Code fact** — verified in the released implementation.
- **Mathematical consequence** — follows from stated equations or definitions.
- **Teaching construction** — an example invented only for explanation.
- **Inference** — a reasoned interpretation not directly asserted.
- **Unknown** — not established by checked sources.

Novelty claims require checking the relevant comparison set. Negative universal claims require especially strong evidence.

## Recover from confusion

When the learner reports confusion:

1. Quote or restate the first failing link precisely.
2. Identify whether the gap is vocabulary, mechanism, computation, mathematics, evidence, or notation.
3. Remove downstream concepts introduced after that link.
4. Re-explain with the same scenario at one lower dependency level.
5. Check one bounded question that requires reconstruction, not “懂了吗?”.
6. Resume the paper only after that link is stable.

## Final self-check

Before sending a teaching response, verify:

- Did I explain why each operation exists, not only what happens?
- Can the learner identify inputs, outputs, supervision, and parameter-update destinations?
- Is every new symbol defined locally and used consistently?
- Did I separate function, value, variable, and parameter?
- Did I preserve realistic structure without overwhelming detail?
- Did I distinguish evidence from interpretation and novelty from shared practice?
- Did I compare only relevant alternatives at an appropriate level of aggregation?
- Did I stop at the current learning gate rather than covering the whole paper?
