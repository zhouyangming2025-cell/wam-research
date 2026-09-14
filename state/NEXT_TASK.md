# NEXT_TASK

## 唯一下一任务

> Continue the **Phase-B Wave-3 comparative deep read** by adding **DriveLaW** to the completed Epona ↔ DrivingGPT comparison block.

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
Epona ↔ DrivingGPT comparison       = COMPLETE
DriveLaW                            = NEXT
Auto-JEPA                           = PENDING
DA-WAM                              = PENDING
Think2Drive                         = PENDING
Wave 3                              = OPEN
```

## First-block result that must be preserved

“World-action unification” already splits into two mechanisms:

```text
Epona:
shared historical latent F
→ separate TrajDiT and VisDiT
→ joint training, modular generation
→ planning can disable visual generation

DrivingGPT:
interleaved z1,q1,z2,q2,... tokens
→ one causal autoregressive Transformer
→ one next-token objective
→ world/action unified at sequence level
```

Important attribution result:

```text
stronger architectural unification
!= stronger causal evidence that world modeling caused planning gains
```

Epona contains a trajectory-only vs joint video+trajectory training ablation, supporting shared visual-future supervision benefit. DrivingGPT has stronger token-level unification but no same-model action-only vs joint visual/action matched planning ablation identified in the first pass.

Do not compare Epona `86.2` and DrivingGPT `82.4` PDMS as a clean ranking: their reported NAVSIM setups/splits are not a matched experiment.

## Immediate DriveLaW audit

Trace from primary text:

```text
1. input/history visual representation
2. video/world-model architecture and training target
3. exact hidden Video-DiT representation exposed to the Action DiT
4. which denoising timestep/layer supplies planning features
5. whether a completed generated future video is needed for planning
6. action/trajectory representation and flow-matching supervision
7. inference-time data flow
8. which WM components execute at planning time
9. video-pretraining/data-scale ablations
10. denoising-step ablation and its interpretation
11. planning evaluation regime
12. matched evidence that hidden WM features add value beyond a strong action model
13. strongest alternative explanation / confound
```

Then update `landscape/PHASE_B_WAVE3_SYNTHESIS.md` with a three-way interface comparison:

```text
Epona     = shared latent → modular trajectory generator
DrivingGPT= interleaved world/action tokens
DriveLaW  = hidden world-model feature → action generator
```

## Binding controls from Waves 1–2

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

## Subsequent Wave-3 order

After DriveLaW:

```text
Auto-JEPA
→ DA-WAM
→ Think2Drive
```

The wave must eventually answer whether hidden/compressed predictive representations can be more planning-useful than explicit future reconstruction, how candidate-specific alternatives are supervised, and how WM-based RL differs from online model-based planning.

## Stop condition

Wave 3 closes when all six anchors can be placed on one inference-interface map and their planning gains can be discussed without the generic explanation “they use a world model.”

After Wave 3, proceed to Wave 4 before any gap or method selection.

Do not declare a research gap. Do not design a method. Do not broaden the corpus. Do not reactivate P2-R/P3. Do not force risk-field knowledge into the interpretation.