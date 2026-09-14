# NEXT_TASK

## 唯一下一任务

> Complete the **Phase-B Wave-2 comparability / supervision-source closeout**, then decide whether Wave 2 is stable enough to close.

Wave 1 is closed. Wave-2 comparative first pass and two source-code audits are complete.

Current artifacts:

```text
landscape/PHASE_B_WAVE2_SYNTHESIS.md
audits/literature/PHASE_B_WAVE2_INTERFACE_CODE_AUDIT.md
```

## Wave-2 anchors

```text
GAIA-1
Drive-WM
OccWorld
WoTE
ViDAR
LAW
```

## What Wave 2 has already established

The generic phrase `world model helps planning` hides multiple different mechanisms:

```text
controllable generation                    — GAIA-1
candidate visual future → reward selection — Drive-WM
joint world + ego future generation        — OccWorld
candidate future BEV → learned reward      — WoTE
future prediction as pretraining           — ViDAR
action-aware auxiliary latent prediction   — LAW
```

Source audits further establish:

- LAW's predicted future latent is an auxiliary training signal; the audited test-time planning path does not consume it to select/refine the current trajectory.
- WoTE's PDM multi-candidate target-generation path changes candidate ego trajectories but scores them against a cached surrounding-agent future interpolated from logged/GT tracks; it is non-reactive supervision with respect to other-agent response.

## Remaining closeout — no new papers

### 1. Drive-WM attribution audit

From primary paper evidence, separate as far as possible:

```text
world-generation quality
vs detector/map performance on generated future
vs reward design
vs candidate-set quality
```

Do not convert the reported planning improvement into a pure “better world model” effect unless a matched ablation supports it. Record the strongest evidence and the unresolved confound explicitly.

### 2. OccWorld metric/comparison audit

Normalize which rows use the same planning metric/protocol and which use alternate `†` metrics or different inputs. Identify the cleanest matched evidence for:

```text
temporal world modeling
representation/tokenizer choice
world forecasting ↔ planning relation
```

Preserve the already important counterexample: higher reconstruction fidelity can coexist with worse forecasting/planning.

### 3. ViDAR downstream-retention audit

Lock exactly:

```text
what is pretrained
what is discarded
what weights/features are transferred
what downstream planner remains unchanged
which matched pretraining ablations isolate the future-prediction benefit
```

The goal is to distinguish “world-model pretraining helps” from generic stronger initialization or LiDAR-supervised representation learning.

### 4. WoTE evidence-strength grading

Integrate the source-code result into the paper evidence:

```text
future-state-on/off ablation = strong evidence for future-state value under NAVSIM
candidate-specific online WM = architecturally true
reactively supervised other-agent response = not established in audited target pipeline
```

Do not downgrade WoTE merely because supervision is non-reactive; distinguish what it proves from what it does not prove.

## Required output

Create:

`landscape/PHASE_B_WAVE2_COMPARABILITY_AUDIT.md`

Then update `landscape/PHASE_B_WAVE2_SYNTHESIS.md` only where the audit changes interpretation.

## Stop condition

Wave 2 closes when we can answer, without hand-waving:

1. which future-state interfaces are actually used online by planning;
2. which planning gains are matched to future modeling rather than scorer/reward/input changes;
3. where alternative ego-action futures receive direct supervision;
4. whether surrounding-agent responses are factual, fixed-log, or truly reactive;
5. what evidence supports or contradicts `higher fidelity / longer horizon → better planning`.

If those are stable, close Wave 2 and start Wave 3.

Do not declare a research gap. Do not design a method. Do not broaden the corpus. Do not reactivate P2-R/P3. Do not force risk-field knowledge into the interpretation.