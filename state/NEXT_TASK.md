# NEXT_TASK

## 唯一下一任务

> Execute the **Phase-B Wave-3 comparative deep read** and build a stable map of unified / compressed / candidate-specific / RL world-action interfaces.

Wave 1 and Wave 2 are closed. Broad corpus acquisition remains frozen.

Canonical Wave-3 plan:

`landscape/PHASE_B_WAVE3_PLAN.md`

## Wave-3 anchors and order

```text
1. Epona
2. DrivingGPT
3. DriveLaW
4. Auto-JEPA
5. DA-WAM
6. Think2Drive
```

## Why this wave exists

Wave 2 established that “world model helps planning” is not one mechanism. Wave 3 now asks what happens when world knowledge and action generation become more tightly coupled.

Do not use the generic label `world-action model` as explanation. Distinguish:

```text
shared latent + joint training
interleaved world/action tokens
hidden WM features consumed by action generator
compressed planning-oriented predictive state
candidate-specific future latent used for scoring
latent WM used as an RL imagination environment
```

## Required per-paper audit

For each anchor, record compactly but precisely:

```text
1. historical problem / motivation
2. exact observation representation
3. exact future/world representation
4. action representation
5. training supervision and future-target source
6. whether unexecuted alternative actions have direct future supervision
7. inference-time data flow
8. whether the WM/future branch survives deployment
9. exact planner interface
10. multimodality/uncertainty and whether planning consumes it
11. evaluation regime
12. strongest matched planning evidence
13. strongest limitation / competing explanation
14. what the paper proves and does not prove
15. historical transition role
```

Maintain `AUTHOR CLAIM / DIRECT EXPERIMENTAL EVIDENCE / OUR INFERENCE` separately.

## Wave-3 comparison questions

The synthesis must answer:

1. What is actually unified — parameters, conditioning, token sequence, latent state, loss, or decision process?
2. Which methods use a predicted future online, and which only use predictive learning to shape a representation/policy?
3. Is explicit/high-fidelity reconstruction necessary, or do hidden/compressed predictive states carry equal or stronger planning value?
4. Does joint world-action modeling improve planning beyond shared representation or stronger action modeling?
5. For candidate-specific futures, what supervision exists for non-executed alternatives?
6. How does model-based RL differ from an online model-based planner in this literature?
7. Which evaluation regime supports each planning claim?

## Binding controls from Waves 1–2

Do not forget:

```text
conditional != causal
candidate ranking != world modeling
world fidelity != decision utility
longer horizon != better planning
generation quality != planning value
candidate-specific output != candidate-specific oracle supervision
WM-assisted planning != online model-based planning
```

Strong non-WM controls remain active: UniAD, DiffusionDrive, DriveSuprim.

## Required output

Primary artifact:

`landscape/PHASE_B_WAVE3_SYNTHESIS.md`

Create a code audit only if a decision-critical inference-path ambiguity cannot be resolved from paper text:

`audits/literature/PHASE_B_WAVE3_INTERFACE_CODE_AUDIT.md`

Do not audit code by default.

## First execution block

Start with:

```text
Epona ↔ DrivingGPT
```

Compare them directly on:

```text
shared latent vs shared sequence
trajectory/world branch separation vs token interleaving
whether generated world output feeds action selection
training coupling vs inference coupling
planning evidence vs generation evidence
```

Then add DriveLaW as the next bridge: hidden world-model features directly condition action generation without requiring fully rendered future output.

## Stop condition

Wave 3 closes when all six papers can be placed on one inference-interface map and we can explain their planning gains without saying merely “they use a world model.”

After Wave 3, proceed to Wave 4 before any gap or method selection.

Do not declare a research gap. Do not design a method. Do not broaden the corpus. Do not reactivate P2-R/P3. Do not force risk-field knowledge into the interpretation.