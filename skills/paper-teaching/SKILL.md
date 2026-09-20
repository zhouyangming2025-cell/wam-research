---
name: paper-teaching
description: "Teach and synthesize technical research papers by identifying their core claims, minimal mechanisms, evidence, novelty boundaries, and deployment lifecycle, with computation or mathematics taught only when needed. Use for progressive explanation, confusion repair, cross-paper comparison, or research-note creation; not for a one-shot abstract summary with no teaching or evidence analysis."
---

# Paper Teaching

Help the learner reconstruct what a paper claims, how it works, what evidence supports it, and what remains unproven. Do not turn paper reading into a compulsory tour through every tensor operation or mathematical prerequisite.

## Choose the teaching mode

Use the narrowest mode that fits the request.

1. **Claim-and-evidence orientation (default)** — Identify the problem, a small set of primary claims, minimal implementation, evidence, comparison scope, and limits. Use this for first explanations, framework understanding, paper synthesis, and deciding what deserves deeper study. Read [claim-evidence-note.md](references/claim-evidence-note.md).
2. **Mechanism deep dive** — Trace one requested mechanism through data, operations, targets, losses, parameter updates, or decoding. Use only when the detail affects understanding, evaluation, or reproduction. Read [teaching-protocol.md](references/teaching-protocol.md).
3. **Confusion repair** — Stop expansion, locate the first broken dependency, and repair it at one lower level. Read [teaching-protocol.md](references/teaching-protocol.md).
4. **Evidence-grounded research note** — Produce a compact problem → claim → mechanism → evidence → boundary record. Read [claim-evidence-note.md](references/claim-evidence-note.md).

When modes overlap, begin with claim-and-evidence orientation and enter a deep dive only at a justified gate.

## Start with a claim map

Before teaching, establish the source boundary and internally record:

- the paper's stated problem and whether the framing itself has been checked;
- the smallest useful set of **primary claims** that define the paper, usually two to four;
- **supporting mechanisms** that solve difficulties created by those claims;
- **generic components** such as standard attention, losses, optimizers, LoRA, or known tokenizers;
- the minimum training and inference lifecycle needed to understand the claims;
- the experiment, theorem, code fact, or comparison that supports each claim;
- the nearest relevant alternatives and the checked comparison set.

Do not flatten primary claims, supporting mechanisms, and generic components into one list of equal “innovations.” An experiment can reveal what the authors intend to validate, but an ablation does not by itself establish novelty.

## Apply the detail-value gate

Before explaining a technical detail, ask whether it is needed to do at least one of the following:

- identify or distinguish a core contribution;
- understand the paper's essential data flow or lifecycle;
- evaluate an experimental or mathematical claim;
- compare against the nearest mechanism family;
- reproduce the requested part of the method;
- repair a dependency the learner has explicitly exposed.

If none applies, defer the detail. State its functional role in one sentence if needed. Hidden dimensions, projection matrices, softmax derivatives, and optimizer mechanics are not default teaching goals merely because they appear in the implementation.

## Default claim-first workflow

1. **Position the paper** — One concrete task, inputs, outputs, deployment graph, and one-sentence technical identity.
2. **Separate the problem from the rhetoric** — Distinguish a field-level problem, an author framing, and an unchecked historical claim.
3. **Rank the contributions** — Primary claims, supporting mechanisms, and generic components.
4. **Give the minimum mechanism** — Explain only the data flow required to make the claims meaningful, including what is shared, predicted, supervised, retained, or removed.
5. **Audit the evidence** — For each primary claim, state what supports it, what alternative explanation remains, and how far the conclusion can extend.
6. **Compare selectively** — Normalize terminology and compare only relevant mechanism families within the checked set.
7. **Choose the next depth** — Continue to experiments, consolidate into a note, or open one bounded mechanism/foundation deep dive.

Do not postpone evidence until after an exhaustive architecture or mathematics tutorial.

## Use understanding layers as diagnostics, not a curriculum

| Layer | Diagnostic question |
|---|---|
| S — Semantics | Can the learner state the problem and proposal? |
| M — Mechanism | Can the learner trace the essential data flow? |
| C — Computation | Can the learner reconstruct shapes, targets, probabilities, losses, and decoding? |
| F — Foundations | Can the learner justify the required mathematical operation? |
| E — Evidence | Can the learner distinguish claim, result, inference, and limitation? |
| T — Transfer | Can the learner compare the nearest alternatives and failure conditions? |

For ordinary paper understanding, prioritize `S → essential M → E → T`. Enter C or F only when the detail-value gate passes. Semantic understanding is not proof of computational understanding, but computational mastery is also not required for every paper judgment.

## Preserve continuity without repetition

Maintain an internal established-knowledge ledger for multi-round teaching:

- `established` — reference briefly; do not redefine, re-table, re-example, or re-summarize;
- `new this round` — emphasize only the relationships being added;
- `deferred` — exclude explicitly when adjacent detail would distract;
- `blocked` — record the earliest missing prerequisite.

Repeat only to correct an error, connect to a genuinely new relationship, or answer an explicit request. Do not make every round independently self-contained. When stability is uncertain, use one bounded reconstruction check instead of preventive reteaching.

## Preserve evidence and comparison discipline

Classify material claims as **paper fact**, **author claim**, **direct evidence**, **code fact**, **mathematical consequence**, **literature synthesis**, **teaching construction**, **inference**, or **unknown**.

- Novelty claims require a relevant comparison set; negative universal claims require especially strong evidence.
- Translate synonymous terminology into shared technical language before comparing papers.
- Group relevant works into mechanism families; omit papers unrelated to the current axis.
- Use calibrated scope such as “within the checked set” or “several compared works.”
- Match the required evidence to the strength of the claim. Failure to prove reactive closed-loop validity does not erase evidence for action-conditioned sensitivity; it limits the conclusion to the lower evidence level.
- Separate training-time knowledge shaping from deployment-time computation. Shared training does not imply that a predicted future remains on the online action path.

## Final check

Before responding, verify:

- Are the paper's primary claims visible before low-level details?
- Did I distinguish a field foundation, a route choice, and a paper-specific design?
- Is the mechanism explanation the minimum needed for the current goal?
- Does every major conclusion have an evidence status and scope boundary?
- Did I avoid forcing irrelevant paper-by-paper comparisons?
- Did I separate training, inference, data time, and solver/refinement time?
- Did I avoid reteaching established knowledge?
- If I used formulas or numerical examples, did they expose a real dependency rather than imitate concreteness?
