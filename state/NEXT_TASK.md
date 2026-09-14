# NEXT_TASK

## 唯一下一任务

> Execute the **Research QA Gate for Waves 1–3** before starting Wave 4.

Wave 1, Wave 2 and Wave 3 are now closed. Broad corpus acquisition remains frozen.

Canonical QA artifacts:

```text
audits/literature/RESEARCH_QA_GATE_WAVES1_3.md
audits/literature/PDF_VERIFICATION_QUEUE.md
```

## Completed immediately before this task

```text
Think2Drive anchor deep read          = COMPLETE
Think2Drive official ECCV PDF check  = COMPLETE
Wave-3 six-interface synthesis       = COMPLETE
Wave 3                               = CLOSED
```

Wave-3 closeout artifact:

```text
landscape/PHASE_B_WAVE3_CLOSEOUT.md
```

Stable six-way interface map:

```text
Epona      = shared predictive representation / modular heads
DrivingGPT = shared world-action causal sequence
DriveLaW   = online world hidden state → action generator
Auto-JEPA  = predicted future ego intent → retrieval / selection
DA-WAM     = candidate action → candidate-specific future latent → score
Think2Drive= learned world → latent imagination → actor/critic policy learning
```

## QA gate — execution order

### 1. Verify all Priority-A public evidence ourselves first

Do not ask the user for PDFs unless public/canonical access fails.

Order:

```text
A1 Epona
A2 OccWorld
A3 WoTE
A4 LAW
A5 DriveLaW
A6 Auto-JEPA
A7 DA-WAM
A8 DrivingGPT source/runtime decode path
```

For each item:

```text
- retrieve official/venue/canonical PDF or public source code;
- verify only the exact decision-critical table/figure/section/path;
- record source version and page/table/symbol;
- mark VERIFIED / CORRECTED / UNRESOLVED;
- correct any downstream synthesis immediately if necessary.
```

### 2. Harden cross-wave field claims

After A1–A8, revisit:

```text
F-01 world prediction accuracy != planning evidence
F-02 future information is not automatically beneficial
F-03 candidate-specific output != candidate-specific oracle supervision
F-04 WM-assisted planning != online model-based planning
F-05 architectural coupling strength != causal evidence strength
F-06 decision relevance != world completeness
```

For each field claim, require at least two independent paper families or one code-verified mechanism + one independent experimental control.

### 3. Produce QA closeout

Required final artifact:

```text
audits/literature/RESEARCH_QA_GATE_CLOSEOUT.md
```

It must contain:

```text
- claims verified unchanged;
- claims corrected;
- unresolved claims;
- exact PDF/code verification provenance;
- statements no longer allowed in future synthesis;
- final authorization decision for Wave 4.
```

## Stop condition

QA closes when every Priority-A item is either:

```text
VERIFIED
CORRECTED
or explicitly UNRESOLVED after exhausting lawful public sources
```

and no field-level conclusion depends on an unmarked OCR/table/source-path ambiguity.

Only then start Wave 4:

```text
Bench2Drive
HUGSIM
ORION
ReactSim-Bench
CausalDrive
```

## Still forbidden

```text
no gap declaration
no method design
no broad paper accumulation
no P2-R/P3 rescue program
no forced risk-field insertion
```
