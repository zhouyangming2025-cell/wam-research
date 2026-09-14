# NEXT_TASK

## 唯一下一任务

> Continue the **Phase-B Wave-3 comparative deep read** with **Auto-JEPA**, using the completed Epona ↔ DrivingGPT ↔ DriveLaW interface comparison as the baseline.

Wave 1 and Wave 2 are closed. Broad corpus acquisition remains frozen.

Canonical Wave-3 artifacts:

```text
landscape/PHASE_B_WAVE3_PLAN.md
landscape/PHASE_B_WAVE3_SYNTHESIS.md
```

## Wave-3 status

```text
Epona primary-text first pass       = COMPLETE
DrivingGPT primary-text first pass  = COMPLETE
DriveLaW primary-text first pass    = COMPLETE
three-way interface synthesis       = COMPLETE
Auto-JEPA                           = NEXT
DA-WAM                              = PENDING
Think2Drive                         = PENDING
Wave 3                              = OPEN
```

## Stable first-half result

“World-action unification” already splits into three mechanisms:

```text
Epona:
shared historical latent F
→ separate TrajDiT / VisDiT
→ joint training, modular generation
→ visual generation can be disabled for planning

DrivingGPT:
interleaved image/action tokens
→ one causal Transformer
→ world/action unified as one driving language

DriveLaW:
Video-DiT denoising latent
→ direct condition for Action DiT
→ online generative hidden state becomes planner state
```

Important evidence correction:

```text
architectural coupling strength
!= causal evidence strength for planning gain
```

Epona has a useful joint-vs-trajectory-only ablation. DrivingGPT lacks a same-model action-only vs joint world/action control in the reviewed paper. DriveLaW supplies stronger representation-side evidence through video-pretraining scale, representation comparisons, and denoising-step ablations.

DriveLaW key matched results to carry forward:

```text
video pretraining size:
0 → 76k → 3.8M → 7.6M
85.9 → 87.0 → 87.8 → 89.1 PDMS

representation under diffusion planner:
BEV 84.1
VLM hidden 86.5
video latent 89.1

video denoise state used by Action DiT:
t=1 89.1
t=5 86.9
t=10 23.2
```

Interpret conservatively: the exact internal world-model representation matters greatly for planning; the denoising-step table does not by itself prove a universal inverse relationship between visual fidelity and planning utility.

NAVSIM remains non-reactive pseudo-simulation even where a paper calls PDMS “closed-loop metrics.”

## Immediate Auto-JEPA audit

Auto-JEPA must be read against three established results:

```text
OccWorld: better reconstruction can coexist with worse forecasting/planning
LAW: longer predictive horizon is not monotonically better
DriveLaW: planner quality is highly sensitive to which generative latent is exposed
```

Trace:

```text
1. exact observation/context encoder
2. exact JEPA target representation
3. predictor input and output tensors
4. what future information is intentionally preserved or discarded
5. how ego action/planning intent enters the objective
6. target encoder / stop-gradient mechanics
7. whether predictive target/predictor survives at inference
8. exact deployed planner path
9. matched controls against reconstruction/generative objectives
10. matched controls against ordinary auxiliary losses / pretraining
11. planning metrics and evaluation regime
12. strongest evidence that compression is decision-oriented
13. strongest alternative explanation
```

Then update `landscape/PHASE_B_WAVE3_SYNTHESIS.md` with a four-way interface comparison:

```text
Epona     = shared latent / modular generation
DrivingGPT= interleaved world-action language
DriveLaW  = world-generator hidden state → action generator
Auto-JEPA = deliberately compressed predictive representation (to verify precisely)
```

## Subsequent order

```text
Auto-JEPA
→ DA-WAM
→ Think2Drive
```

DA-WAM will test per-candidate future-latent evaluation and alternative-action supervision. Think2Drive will separate a learned world used for policy training from a world model used directly by the deployed planner.

## Stop condition

Wave 3 closes when all six anchors can be placed on one inference-interface map and their planning gains can be discussed without the generic explanation “they use a world model.” After Wave 3, proceed to Wave 4 before any gap or method selection.

Do not declare a research gap. Do not design a method. Do not broaden the corpus. Do not reactivate P2-R/P3. Do not force risk-field knowledge into the interpretation.