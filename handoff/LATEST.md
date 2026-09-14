# LATEST — Handoff

Session: 2026-09-14 — Wave 1 and Wave 2 closed; Wave 3 active through DriveLaW.

## New-session fast path

```text
1. START_HERE.md
2. state/CURRENT_STATE.md
3. state/NEXT_TASK.md
4. landscape/PHASE_B_WAVE2_COMPARABILITY_AUDIT.md
5. landscape/PHASE_B_WAVE3_PLAN.md
6. landscape/PHASE_B_WAVE3_SYNTHESIS.md
```

Do not default to P2-R/P3. Do not reload the whole corpus or old chats by default.

## Research identity

```text
World Model + End-to-End + Planning-centric autonomous driving
```

Risk-field / predictive-risk expertise is optional prior knowledge, not a required destination.

Active methodology:

```text
UNDERSTAND FIELD FIRST
→ comparative deep reads
→ cross-family synthesis
→ only then research-problem discovery
```

No gap/method selection is authorized yet.

## Phase-A / corpus status

```text
P0001–P0060 = 60 registered
58 RAW_MD_READY
F1–F11 coverage = PASS
broad acquisition = FROZEN
25 Phase-B anchors = FIXED
```

## Wave 1 — CLOSED

Historical/non-WM/evaluation baseline is stable. Key controls: conditional future ≠ intervention; candidate ranking is an independent bottleneck; multimodal action generation ≠ WM; prediction accuracy ≠ planning evidence; benchmark regime changes claim semantics.

Artifacts:

- `landscape/PHASE_B_WAVE1_SYNTHESIS.md`
- `landscape/PHASE_B_WAVE1_COMPARABILITY_AUDIT.md`

## Wave 2 — CLOSED

Artifacts:

- `landscape/PHASE_B_WAVE2_SYNTHESIS.md`
- `landscape/PHASE_B_WAVE2_COMPARABILITY_AUDIT.md`
- `audits/literature/PHASE_B_WAVE2_INTERFACE_CODE_AUDIT.md`

Stable distinctions:

```text
CONTROLLABLE GENERATION != PLANNING INTERFACE
JOINT WORLD-ACTION GENERATION != CANDIDATE CONSEQUENCE EVALUATION
ACTION-CONDITIONED != REACTIVELY SUPERVISED
WM-ASSISTED PLANNING != ONLINE MODEL-BASED PLANNING
WORLD FIDELITY != DECISION UTILITY
LONGER HORIZON != BETTER PLANNING
CANDIDATE-SPECIFIC OUTPUT != CANDIDATE-SPECIFIC ORACLE SUPERVISION
```

Important evidence: OccWorld reconstruction/planning counterexample; WoTE `81.0→83.2→85.6` future-state ablation plus fixed-log PDM supervision semantics; ViDAR predictive-pretraining transfer; LAW source-verified training-only future-latent role.

## Wave 3 — ACTIVE

Canonical files:

```text
landscape/PHASE_B_WAVE3_PLAN.md
landscape/PHASE_B_WAVE3_SYNTHESIS.md
```

Status:

```text
Epona       = COMPLETE first pass
DrivingGPT  = COMPLETE first pass
DriveLaW    = COMPLETE first pass
Auto-JEPA   = NEXT
DA-WAM      = PENDING
Think2Drive = PENDING
```

### Stable Wave-3 result so far

`world-action unification` already has three distinct meanings:

```text
Epona
= shared historical latent F
→ separate TrajDiT / VisDiT
→ visual generation can be disabled for planning

DrivingGPT
= interleaved image/action token language
→ one causal autoregressive Transformer
→ one next-token objective

DriveLaW
= Video-DiT denoising latent
→ direct conditioning of Action DiT
→ online generator hidden state becomes planner representation
```

Do not numerically rank their headline PDMS as a matched progression. DrivingGPT reports navmini while Epona/DriveLaW report different NAVSIM test/Navtest conditions; inputs/training also differ.

### DriveLaW evidence to preserve

```text
video-pretraining scale:
0 / 76k / 3.8M / 7.6M samples
PDMS 85.9 / 87.0 / 87.8 / 89.1

representation condition:
BEV 84.1
VLM hidden 86.5
Video latent 89.1

denoising state:
t=1 89.1
t=5 86.9
t=10 23.2
```

Interpret the denoising ablation conservatively: planning depends sharply on which internal generative state is used; it does not alone prove a universal `lower visual fidelity = better planning` rule.

NAVSIM remains non-reactive pseudo-simulation even when papers call PDMS a closed-loop metric.

## Immediate next task

Read `state/NEXT_TASK.md`.

Deep-read **Auto-JEPA** against OccWorld, LAW and DriveLaW to determine whether deliberately compressed predictive representations provide planning value beyond dense reconstruction/generation or generic auxiliary supervision.

Then continue:

```text
DA-WAM → Think2Drive
```

## Still forbidden

```text
no gap declaration
no method design
no broad paper accumulation
no P2-R/P3 rescue
no forced risk-field insertion
```

The repo, not conversation memory, is the canonical research authority.