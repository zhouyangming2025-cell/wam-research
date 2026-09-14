# RESEARCH_QA_PRIORITY_A_PROGRESS

Last updated: 2026-09-14

Status: **ACTIVE — Priority-A verification in progress**

Purpose: record decision-critical verification work performed after Wave 3 closeout. This file supplements `RESEARCH_QA_GATE_WAVES1_3.md` and should be merged into the final QA closeout.

## A1 — Epona

**Target claim:** joint visual+trajectory training improves planning over trajectory-only training.

**Current verdict:** `VERIFIED IN PRIMARY PUBLIC PDF TEXT / exact canonical table extraction still to be mirrored into final register`.

Public ICCV 2025 open-access paper confirms Epona as the venue-final source. The public PDF/searchable text exposes Table 5 as the planning comparison between the full model and `Ours w/o Joint Training`; the reported values are:

```text
Ours w/o Joint Training: NC 94.5 / DAC 89.7 / TTC 88.1 / Comfort 99.9 / EP 74.7 / PDMS 78.1
Ours:                    NC 97.9 / DAC 95.1 / TTC 93.8 / Comfort 99.9 / EP 80.4 / PDMS 86.2
```

Interpretation allowed:

```text
within Epona's own setup, removing joint visual prediction materially reduces planning performance.
```

Interpretation NOT allowed:

```text
the +8.1 PDMS difference proves that online imagined visual rollout causes the planning gain.
```

The deployed planner can operate without visual generation, so this remains evidence for joint predictive representation shaping / multi-task coupling rather than online future-video evaluation.

## A2 — OccWorld

**Target claims:**

1. higher-resolution tokenizer reconstructs better but forecasts/plans worse;
2. removing temporal/spatial modeling degrades forecasting and planning.

**Verdict:** `PDF VERIFIED` using official arXiv PDF `2311.16038`, p.7, tokenizer table + Table 4.

Verified tokenizer rows:

```text
default (50^2,128,512): reconstruction 66.38/62.29; forecast mIoU 17.14; planning L2 1.17
higher-res (100^2,128,512): reconstruction 78.12/71.63; forecast mIoU 12.38; planning L2 1.36
```

Verified spatial/temporal ablation:

```text
OccWorld-O             forecast mIoU 17.14 / IoU 26.63 / planning L2 1.17 / Col 0.60
w/o spatial attention  10.07 / 21.44 / 1.42 / 1.21
w/o temporal attention  8.98 / 20.10 / 2.06 / 2.56
```

Stable conclusion:

```text
better reconstruction fidelity is not monotonic with forecast/planning utility in this matched representation ablation.
```

This is a paper-specific counterexample, not a universal theorem.

## A3 — WoTE

**Target claim:** future-state input adds value beyond evaluator-only under the matched NAVSIM setup.

**Verdict:** `PDF VERIFIED` using arXiv PDF `2504.01941`, Table 3, p.6.

Verified rows:

```text
Traj Eval × / Future × : 81.0 PDMS
Traj Eval ✓ / Future × : 83.2 PDMS
Traj Eval ✓ / Future ✓ : 85.6 PDMS
```

Paper text explicitly states that the second row uses trajectory evaluation without predicted future states and the third row integrates the BEV world model, improving multiple metrics.

Stable conclusion:

```text
within this NAVSIM setup, learned trajectory evaluation contributes +2.2 PDMS over trajectory-only, and adding predicted future BEV states contributes another +2.4 PDMS over evaluator-only.
```

Boundary retained from source-code audit:

```text
this does not establish candidate-specific reactive oracle supervision for surrounding agents.
```

## A4 — LAW

**Target claims:**

1. action-aware future-latent auxiliary prediction improves planning within the matched model family;
2. future-target horizon is non-monotonic.

**Verdict:** `PDF VERIFIED` using official ICLR 2025 / arXiv PDF `2406.08481`, Table 4 and horizon table on p.8.

Verified Table 4, perception-free branch:

```text
no WM inputs                    avg L2 0.71 / collision 0.41
visual latent only              avg L2 0.68 / collision 0.37
visual latent + predicted traj  avg L2 0.61 / collision 0.30
```

Verified perception-based branch:

```text
0.54 / 0.25
0.52 / 0.21
0.49 / 0.19
```

Verified horizon rows:

```text
0.5 s   avg L2 0.61 / collision 0.30
1.5 s   avg L2 0.58 / collision 0.25
3.0 s   avg L2 0.63 / collision 0.27
10.0 s  avg L2 0.72 / collision 0.43
```

Stable conclusion:

```text
action-aware future-latent supervision improves the matched planner family, while longer prediction horizon is not monotonically better.
```

This remains compatible with the code-verified inference fact that the predicted future latent is not consumed for current trajectory selection at test time.

## Current QA status

```text
A1 Epona      = evidence confirmed; final canonical provenance formatting pending
A2 OccWorld   = PDF VERIFIED
A3 WoTE       = PDF VERIFIED + prior CODE VERIFIED supervision boundary
A4 LAW        = PDF VERIFIED + prior CODE VERIFIED inference boundary
A5 DriveLaW   = NEXT
A6 Auto-JEPA  = pending
A7 DA-WAM     = pending
A8 DrivingGPT = pending source/runtime decode audit
```

No contradiction requiring correction of existing Wave-2/Wave-3 synthesis has been found in A1–A4 so far.
