# Detailed Reading

Use this reference when the user wants a detailed explanation, when analyzing 1-3 important papers, or when prior output feels too shallow.

## What "Detailed" Means

Detailed paper reading is not longer summary. It must make the paper understandable and judgeable.

For each major section, include:

- Explanation: what the paper is saying in plain language.
- Mechanism: how the method actually works.
- Evidence: where the paper supports the claim.
- Interpretation: what the evidence means and what it does not prove.
- Research use: how the idea could be reused, tested, or extended.

## Required Depth Blocks

### Background Bridge

Before method details, explain the minimum background needed:

- What problem family this paper belongs to.
- What the standard/simple baseline would do.
- Why the paper's setting is harder than the baseline setting.
- Which terms must be understood before reading the method.

### Mechanism Decomposition

For agent papers, decompose the method into:

```text
Input/task
-> state/context construction
-> planning or role assignment
-> action/tool/message generation
-> observation or peer response
-> memory/reflection/verification
-> stopping or final output
```

For each component, explain:

- What enters this component.
- What it outputs.
- Whether it is prompt-only, learned, retrieved, rule-based, tool-based, or human-provided.
- What can go wrong inside it.

### Claim-Evidence-Interpretation

Use this pattern for experiments:

```text
Claim:
Evidence:
Interpretation:
What remains unproven:
```

Do not just list table numbers. Explain what the metric means, why the baseline matters, and whether the comparison is fair.

### Figure and Table Reading

When figures/tables are central:

- State what the figure/table is trying to prove.
- Explain the axes, rows, or columns in plain language.
- Identify the key trend.
- Say what conclusion is justified.
- Say what conclusion would be overclaiming.

### Limitation Reading

Separate limitations into:

- Author-stated limitations.
- Evidence limitations.
- Reproducibility limitations.
- Engineering limitations.
- Generalization limitations.
- Safety or misuse limitations, if relevant.

### Extension Reading

Convert "future work" into concrete next steps:

```text
Idea:
What changes:
Why it may work:
Smallest experiment:
Needed implementation:
Expected evidence:
Main risk:
```

## Depth Calibration

- 1 paper: full detailed reading is expected.
- 2-3 papers: detailed per-paper reading plus concise synthesis.
- 4-6 papers: compact per-paper mini-review plus stronger comparison.
- More than 6 papers: cluster the papers first, then deep-read the most important ones.

If the user says "还是不够详细", expand the per-paper sections before adding more cross-paper comparison.
