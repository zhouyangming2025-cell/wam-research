# RESEARCH_QA_PRIORITY_A_PROGRESS

Last updated: 2026-09-14

Status: **COMPLETE — A1–A8 adjudicated**

Purpose: record decision-critical verification work performed after Wave 3 closeout. This file supplements `RESEARCH_QA_GATE_WAVES1_3.md` and is consolidated by `RESEARCH_QA_GATE_CLOSEOUT.md`.

## A1 — Epona

**Target claim:** joint visual+trajectory training improves planning over trajectory-only training.

**Verdict:** `PDF VERIFIED` from the public ICCV 2025 venue paper, Table 5.

```text
Ours w/o Joint Training: NC 94.5 / DAC 89.7 / TTC 88.1 / Comfort 99.9 / EP 74.7 / PDMS 78.1
Ours:                    NC 97.9 / DAC 95.1 / TTC 93.8 / Comfort 99.9 / EP 80.4 / PDMS 86.2
```

Allowed interpretation:

```text
within Epona's own setup, removing joint visual-future training materially reduces planning performance.
```

Not allowed:

```text
the +8.1 PDMS difference proves that online imagined visual rollout causes the planning gain.
```

The visual generator can be disabled on the deployed planning path, so this is evidence for joint predictive representation shaping / multi-task coupling rather than online future-video evaluation.

## A2 — OccWorld

**Target claims:**

1. higher-resolution tokenizer reconstructs better but forecasts/plans worse;
2. removing temporal/spatial modeling degrades forecasting and planning.

**Verdict:** `PDF VERIFIED` using official arXiv PDF `2311.16038`, p.7, tokenizer table + Table 4.

```text
default (50^2,128,512): reconstruction 66.38/62.29; forecast mIoU 17.14; planning L2 1.17
higher-res (100^2,128,512): reconstruction 78.12/71.63; forecast mIoU 12.38; planning L2 1.36

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

```text
Traj Eval × / Future × : 81.0 PDMS
Traj Eval ✓ / Future × : 83.2 PDMS
Traj Eval ✓ / Future ✓ : 85.6 PDMS
```

Stable conclusion:

```text
learned trajectory evaluation contributes +2.2 PDMS over trajectory-only,
and adding predicted future BEV states contributes another +2.4 PDMS over evaluator-only.
```

Boundary retained from source-code audit:

```text
this does not establish candidate-specific reactive oracle supervision for surrounding agents.
```

## A4 — LAW

**Target claims:**

1. action-aware future-latent auxiliary prediction improves planning within the matched model family;
2. future-target horizon is non-monotonic.

**Verdict:** `PDF VERIFIED` using official ICLR 2025 / arXiv PDF `2406.08481`, Table 4 and horizon table.

Perception-free:

```text
no WM inputs                    avg L2 0.71 / collision 0.41
visual latent only              avg L2 0.68 / collision 0.37
visual latent + predicted traj  avg L2 0.61 / collision 0.30
```

Perception-based:

```text
0.54 / 0.25
0.52 / 0.21
0.49 / 0.19
```

Horizon:

```text
0.5 s   avg L2 0.61 / collision 0.30
1.5 s   avg L2 0.58 / collision 0.25
3.0 s   avg L2 0.63 / collision 0.27
10.0 s  avg L2 0.72 / collision 0.43
```

Stable conclusion:

```text
action-aware future-latent supervision improves the matched planner family,
while longer prediction horizon is not monotonically better.
```

This remains compatible with the code-verified inference fact that the predicted future latent is not consumed for current trajectory selection at test time.

## A5 — DriveLaW

**Target claims:**

1. video-pretraining scale correlates with planning improvement;
2. Video-DiT latent outperforms BEV/VLM representations in the authors' planner setup;
3. planning is highly sensitive to denoising state;
4. resolve whether Stage-3 planning training freezes or updates the Video DiT.

**Verdict:** `PRIMARY PAPER VERIFIED + CODE VERIFIED TRAINING SEMANTICS`.

Canonical public paper / repository evidence confirms the matched planning results:

```text
Video pretraining size → PDMS
0 (scratch)  85.9
76k          87.0
3.8M         87.8
7.6M         89.1

Representation under the paper planner:
BEV features       84.1
VLM hidden state   86.5
Video latents      89.1

Denoising state:
t=1   89.1
t=5   86.9
t=10  23.2
```

A previous ambiguity is now **CORRECTED**. The paper implementation section explicitly states that trajectory fine-tuning updates **both the Video DiT and Planning DiT**. The official repository at commit/tree `243e0e41148bdb1ae39ce1adf17d026e7cbd4348` further shows:

```text
DriveLaW-Act/.../video_model_infer_navsim.yaml
return_action: true
return_video: false
train_mode: 'action_full'
```

and the training implementation makes all unified diffusion-model parameters trainable for `action_full`, while the trajectory stage optimizes the action loss.

Therefore future synthesis must use:

```text
Stage 3 jointly adapts the Video-DiT / Action-DiT planning stack under trajectory/action training.
```

It must NOT state or imply:

```text
DriveLaW Stage 3 simply freezes a video generator and trains a separate planner on fixed features.
```

Boundary:

```text
the scaling table establishes monotonic planning improvement with more video pretraining in this pipeline,
but it does not isolate physical-world understanding as the unique cause; representation scale/data/curriculum and subsequent joint adaptation co-vary.
```

The denoising-step table establishes representation-state sensitivity, not a universal inverse relation between visual fidelity and planning value.

## A6 — Auto-JEPA

**Target claims:** component attribution, candidate-pool sensitivity, semantic occlusion evidence.

**Verdict:** `PUBLIC PRIMARY-TEXT VERIFIED` from arXiv `2607.29031` and the canonical paper text in the corpus.

Component ablation:

```text
fixed codebook-medoid intent          52.6 PDMS
intent retrieval + gate, no scorer   87.6
intent + scorer, no gate              91.0
full                                  91.3
```

Candidate pool:

```text
K=1     87.6
K=200   91.1
K=300   91.3
```

Semantic occlusion over 15,364 validation samples:

```text
dynamic-agent mask mean intent change  0.080
equal-area random mask                  0.027
ratio                                   2.97×
dynamic-agent intervention larger       71.1% of samples
```

Stable conclusion:

```text
future-ego-trajectory latent prediction is a decision-oriented compression mechanism,
and final system quality materially depends on trajectory-memory coverage and candidate ranking.
```

Not established:

```text
universal decision sufficiency;
reactive/counterfactual causal understanding of other agents;
full environment-transition modeling.
```

## A7 — DA-WAM

**Target claims:** matched future-configuration ablation and source of supervision for unexecuted candidate futures.

**Verdict:** `PUBLIC PRIMARY-TEXT VERIFIED` from arXiv `2608.19085` and the canonical paper text in the corpus.

Matched future configuration:

```text
No Future Prediction                  93.31 PDMS
Shared Global Future                  92.81
Current-Latent Conditioning           93.25
Action-Conditioned Future             93.46
Action-Conditioned Future + hard neg  93.68
```

Therefore:

```text
candidate-specific future vs no-future = +0.15 PDMS
hard-negative addition                = +0.22 PDMS
shared global future vs no-future     = -0.50 PDMS
```

The method explicitly acknowledges the offline counterfactual supervision limit:

```text
N candidate-specific future latents are predicted,
but direct observed-future latent prediction loss is applied only to the expert-matched candidate.
```

Other candidates receive factor / utility / ranking supervision; hard-negative labels are planning targets rather than observed alternative future representations.

Stable conclusion:

```text
candidate-specific future OUTPUT != candidate-specific observed-future GROUND TRUTH.
```

Do not describe all DA-WAM candidates as having counterfactual future oracle supervision.

## A8 — DrivingGPT

**Target claim:** resolve the optimized planning decode path — specifically whether NAVSIM planning must autoregressively generate every intervening visual token or can bypass visual generation.

**Verdict:** `PAPER-LEVEL COUPLING VERIFIED / OPTIMIZED RUNTIME PATH UNRESOLVED`.

The ICCV 2025 venue paper and supplement verify:

```text
image tokens + framewise action tokens are interleaved in one causal sequence;
one autoregressive Transformer uses standard next-token prediction;
image-token sampling is part of the documented generative inference path;
the SVD decoder consumes predicted DrivingGPT image tokens during video inference.
```

The authors' project page exposes a `Code` link to:

```text
https://github.com/RogerChern/DrivingGPT
```

but that official link currently returns `404 Not Found`, and no accessible official repository was found through GitHub repository search. Therefore the implementation-level question cannot lawfully be resolved further from current public sources.

Allowed:

```text
DrivingGPT has genuine paper-level shared-sequence world/action coupling.
```

Not allowed:

```text
the NAVSIM deployment path is proven to generate every future image token before every action token;
or, conversely, that it is proven to bypass them.
```

This remains an explicit implementation-level unresolved item and does not block field reconstruction.

## Priority-A final status

```text
A1 Epona      = VERIFIED
A2 OccWorld   = VERIFIED
A3 WoTE       = VERIFIED + prior CODE VERIFIED boundary
A4 LAW        = VERIFIED + prior CODE VERIFIED inference boundary
A5 DriveLaW   = VERIFIED + CORRECTED Stage-3 training semantics
A6 Auto-JEPA  = VERIFIED
A7 DA-WAM     = VERIFIED
A8 DrivingGPT = PAPER-LEVEL VERIFIED / runtime detail UNRESOLVED after public-source exhaustion
```

No Priority-A item now depends on an unmarked OCR/table ambiguity. The only unresolved item is deliberately scoped to DrivingGPT's unavailable optimized runtime implementation.
