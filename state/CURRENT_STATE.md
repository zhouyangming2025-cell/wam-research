# CURRENT_STATE

Last updated: 2026-09-14 — Research QA Gate CLOSED; Wave 4 ACTIVE

## Research north star

```text
World Model + End-to-End + Planning-centric autonomous driving
```

Planning is the center of gravity. Risk/predictive-risk expertise is optional prior knowledge, not a required destination.

Canonical rules: `state/RESEARCH_PRINCIPLES.md`.

## Methodological rule in force

```text
FIELD UNDERSTANDING FIRST
→ comparative anchor deep reads
→ cross-family synthesis
→ evidence QA
→ only then research-problem / gap discovery
```

P1/P2-R/P3 remain parked historical probes and do not organize the reading program.

## Current active stage

```text
FIELD RECONSTRUCTION — PHASE B: WAVE 4 ACTIVE
```

Phase A remains closed:

```text
P0001–P0060 registered
58 RAW_MD_READY
F1–F11 census coverage PASS
broad acquisition FROZEN
25 representative Phase-B anchors selected
```

## Wave 1 — CLOSED

Anchors:

```text
M2I
GameFormer
What Truly Matters in Trajectory Prediction?
UniAD
nuPlan
NAVSIM
DiffusionDrive
DriveSuprim
```

Canonical artifacts:

- `landscape/PHASE_B_WAVE1_SYNTHESIS.md`
- `landscape/PHASE_B_WAVE1_COMPARABILITY_AUDIT.md`

Stable controls:

1. conditional future response is not automatically causal/interventional response;
2. final planner score must be decomposed into representation, scorer, refinement, optimizer and rules;
3. matched controls dominate headline SOTA tables;
4. multimodal/diffusion action generation is not automatically world modeling;
5. candidate ranking is an independent planning bottleneck;
6. evaluation regimes are different claims;
7. world-prediction accuracy alone is not planning evidence.

## Wave 2 — CLOSED

Anchors:

```text
GAIA-1
Drive-WM
OccWorld
WoTE
ViDAR
LAW
```

Canonical artifacts:

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

High-confidence source facts:

```text
LAW test-time path discards predicted future latent  = CODE VERIFIED
WoTE audited target path uses fixed logged surrounding futures = CODE VERIFIED
```

## Wave 3 — CLOSED

Anchors:

```text
Epona
DrivingGPT
DriveLaW
Auto-JEPA
DA-WAM
Think2Drive
```

Canonical artifacts:

- `landscape/PHASE_B_WAVE3_SYNTHESIS.md`
- `landscape/PHASE_B_WAVE3_CLOSEOUT.md`
- `audits/literature/PHASE_B_WAVE3_AUTOJEPA_AUDIT.md`
- `audits/literature/PHASE_B_WAVE3_DAWAM_AUDIT.md`
- `audits/literature/PHASE_B_WAVE3_THINK2DRIVE_AUDIT.md`

Stable six-way interface map:

```text
Epona
= shared historical predictive representation
→ separate trajectory / visual generation heads

DrivingGPT
= interleaved image/action tokens
→ one causal world-action language

DriveLaW
= online Video-DiT hidden state
→ Action DiT

Auto-JEPA
= predicted future ego-intent latent
→ trajectory-memory retrieval
→ scorer/gate

DA-WAM
= candidate_i
→ candidate-specific future latent_i
→ score_i

Think2Drive
= learned latent transition/reward model
→ imagined actor/critic rollouts
→ learned closed-loop policy
```

Stable Wave-3 conclusions:

1. `world-action unification` is not one architecture; the planning-relevant variable is where predictive/world information enters the decision process.
2. Architectural coupling strength does not equal planning effect size or causal evidence strength.
3. Future information has no universal positive sign; representation, horizon, conditioning, planner interface and supervision jointly determine value.
4. Planning-oriented compression is a real branch: Auto-JEPA predicts future ego-motion intent rather than reconstructing a full future scene.
5. DA-WAM predicts per-candidate future latents but direct observed-future supervision exists only for the expert-matched candidate.
6. Think2Drive establishes a distinct role: the WM can act primarily as a latent imagination environment for RL policy learning rather than an online candidate evaluator.

QA correction carried forward:

```text
DriveLaW Stage 3 does NOT freeze the Video DiT.
Paper + official code show trajectory fine-tuning updates both Video DiT and Planning/Action DiT;
o future synthesis may describe DriveLaW as fixed-video-features + separately trained planner.
```

DrivingGPT runtime boundary:

```text
shared interleaved world/action causal sequence = VERIFIED
exact optimized NAVSIM decode path              = UNRESOLVED
```

## Research QA Gate — CLOSED

Canonical artifacts:

```text
audits/literature/RESEARCH_QA_GATE_WAVES1_3.md
audits/literature/RESEARCH_QA_PRIORITY_A_PROGRESS.md
audits/literature/RESEARCH_QA_GATE_CLOSEOUT.md
```

Priority-A outcome:

```text
A1 Epona      VERIFIED
A2 OccWorld   VERIFIED
A3 WoTE       VERIFIED + code boundary
A4 LAW        VERIFIED + code boundary
A5 DriveLaW   VERIFIED + CORRECTED Stage-3 semantics
A6 Auto-JEPA  VERIFIED
A7 DA-WAM     VERIFIED
A8 DrivingGPT paper-level VERIFIED / exact runtime UNRESOLVED after public-source exhaustion
```

Hardened field claims:

```text
F-01 world-prediction quality != planning evidence                         STRONGLY SUPPORTED
F-02 future information is not automatically beneficial                    STRONGLY SUPPORTED
F-03 candidate-specific output != candidate-specific oracle supervision     STRONGLY SUPPORTED
F-04 WM-assisted planning != online model-based planning                    STRONGLY SUPPORTED
F-05 architectural coupling strength != causal-evidence strength            SUPPORTED INFERENCE
F-06 decision relevance != world completeness                              SUPPORTED FIELD TENSION
```

These remain field-understanding results, not research gaps.

## Wave 4 — ACTIVE

Anchors:

```text
1. Bench2Drive
2. HUGSIM
3. ORION
4. ReactSim-Bench
5. CausalDrive
```

Wave-4 purpose: reconstruct the distinctions among:

```text
sensor / visual realism
physical scene evolution
other-agent behavior realism
ego-action feedback
reactivity
closed-loop policy evaluation
VLA / semantic reasoning
world-model behavioral validity
```

The central question is not “which benchmark is best?” but:

```text
what causal/behavioral claim does each evaluation setup actually support?
```

## Immediate next task

See `state/NEXT_TASK.md`.

Begin with Bench2Drive → HUGSIM as the evaluation/simulator baseline pair before reading ORION / ReactSim-Bench / CausalDrive.

## Still forbidden

```text
no gap declaration
no method design
no broad paper accumulation
no P2-R/P3 rescue program
no forced risk-field insertion
```

## Research Brain architecture

GitHub raw MD + figures are the persistent GPT-readable primary-text layer; canonical PDFs remain source authority where archived/available. Public official PDFs and source repositories should be used directly for decision-critical verification whenever available.

A fresh session should read:

```text
START_HERE.md
state/CURRENT_STATE.md
state/NEXT_TASK.md
audits/literature/RESEARCH_QA_GATE_CLOSEOUT.md
landscape/PHASE_B_WAVE3_CLOSEOUT.md
```
