# CURRENT_STATE

Last updated: 2026-09-14 — Wave 3 CLOSED; Research QA Gate ACTIVE

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
RESEARCH QA GATE — WAVES 1–3
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

Stable Wave-2 distinctions:

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
WoTE candidate target-generation uses fixed logged surrounding futures = CODE VERIFIED
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

### Stable six-way interface map

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

### Stable Wave-3 conclusions

1. `world-action unification` is not one architecture; the planning-relevant variable is where predictive/world information enters the decision process.
2. Architectural coupling strength does not equal planning effect size or causal evidence strength.
3. Future information has no universal positive sign; representation, horizon, conditioning, planner interface and supervision jointly determine value.
4. Planning-oriented compression is a real branch of world modeling: Auto-JEPA predicts future ego-motion intent rather than reconstructing a full future scene.
5. DA-WAM predicts per-candidate future latents but direct observed-future supervision exists only for the expert-matched candidate.
6. Think2Drive establishes a distinct role: the WM can act primarily as a latent imagination environment for RL policy learning rather than an online candidate evaluator.
7. Think2Drive official ECCV 2024 PDF was directly checked for RSSM/imagination mechanism, privileged input and CARLA-v2 test results.

These are field-understanding results, not gap claims.

## Research QA Gate — ACTIVE

Canonical artifacts:

```text
audits/literature/RESEARCH_QA_GATE_WAVES1_3.md
audits/literature/PDF_VERIFICATION_QUEUE.md
```

Current rule:

```text
Do not begin Wave 4 until Priority-A evidence is either
VERIFIED / CORRECTED / explicitly UNRESOLVED.
```

Highest-priority checks:

```text
Epona      joint-vs-trajectory-only ablation
OccWorld   tokenizer + temporal/spatial ablations + metric footnote
WoTE       future-state-on/off table
LAW        action-aware/no-WM + horizon tables
DriveLaW   pretraining/representation/denoising tables + freeze semantics
Auto-JEPA  component/K/occlusion evidence
DA-WAM     future-config ablation + expert-matched future supervision
DrivingGPT optimized planning decode path
```

The assistant should use public official PDFs/source code first. User/local PDF help is required only for inaccessible canonical evidence.

## Immediate next task

See `state/NEXT_TASK.md`.

Execute the Priority-A verification queue, correct any earlier synthesis if needed, then create:

```text
audits/literature/RESEARCH_QA_GATE_CLOSEOUT.md
```

Only after QA closeout may Wave 4 begin:

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

## Research Brain architecture

GitHub raw MD + figures are the persistent GPT-readable primary-text layer; canonical PDFs remain source authority where archived/available. Public official PDFs and source repositories should be used directly for decision-critical verification whenever available.

A fresh session should read:

```text
START_HERE.md
state/CURRENT_STATE.md
state/NEXT_TASK.md
landscape/PHASE_B_WAVE3_CLOSEOUT.md
audits/literature/RESEARCH_QA_GATE_WAVES1_3.md
audits/literature/PDF_VERIFICATION_QUEUE.md
```
