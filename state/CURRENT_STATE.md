# CURRENT_STATE

Last updated: 2026-09-14 — Wave 1 closed; Wave-2 comparative first pass + interface code audit complete

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
→ only then research-problem / gap discovery
```

P1/P2-R/P3 remain parked historical probes and do not organize the reading program.

## Current active stage

```text
FIELD RECONSTRUCTION — PHASE B: WAVE 2 CLOSEOUT
```

Phase A is closed:

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

Stable control rules carried forward:

1. conditional future response is not automatically causal/interventional response;
2. final planner score must be decomposed into learned representation, scorer, refinement, optimizer and rules;
3. matched controls dominate headline SOTA tables;
4. multimodal/diffusion action generation is not automatically world modeling;
5. candidate ranking is an independent planning bottleneck;
6. E2/E3/E4/E5/E6/E7 evaluation regimes are different claims;
7. world-prediction accuracy alone is not planning evidence.

## Wave 2 — comparative first pass complete

Anchors:

```text
GAIA-1
Drive-WM
OccWorld
WoTE
ViDAR
LAW
```

Canonical synthesis:

`landscape/PHASE_B_WAVE2_SYNTHESIS.md`

Decision-critical source audit:

`audits/literature/PHASE_B_WAVE2_INTERFACE_CODE_AUDIT.md`

### Main structural result

“World model helps planning” decomposes into different mechanisms:

```text
GAIA-1   = controllable world generation; no operational planner interface
Drive-WM = candidate → visual future → perception/reward → selection
OccWorld = joint future occupancy + ego generation
WoTE     = candidate → future BEV → learned reward → selection
ViDAR    = future prediction as representation pretraining
LAW      = action-aware future-latent auxiliary supervision
```

These are not interchangeable planning paradigms.

### Strongest Wave-2 evidence/corrections

1. **GAIA-1 establishes controllable generative capability, not planning value.** It does not provide an operational imagined-future planner or planning benchmark.
2. **Drive-WM makes imagined visual futures an explicit decision object.** But its planning gain is entangled with generated-image perception, reward design and candidate quality; evaluation is not reactive closed loop.
3. **OccWorld supplies a direct counterexample to “higher reconstruction fidelity → better planning.”** Its higher-resolution tokenizer reconstructs better but forecasts/plans worse than the default representation.
4. **WoTE contains an unusually useful future-state ablation.** Trajectory-only `81.0 PDMS` → evaluator without future `83.2` → evaluator with future states `85.6`; future state adds value beyond scorer-only in that matched setup.
5. **WoTE target-generation code uses NAVSIM/PDM non-reactive semantics.** Candidate ego trajectories are separately simulated/scored, but surrounding-agent observations come from one cached interpolated logged/GT future shared across candidates. Candidate-specific prediction therefore does not imply reactively supervised response.
6. **ViDAR improves planning through predictive pretraining rather than deployed online imagination.** Future LiDAR/geometry forecasting shapes the encoder reused by downstream tasks.
7. **LAW source code resolves the inference-path ambiguity.** The current waypoint is computed before the WM future latent; training uses future-latent reconstruction loss; test-time planning discards the returned latent outputs. LAW is therefore an action-aware future-prediction representation-shaping method, not online rollout-based action selection in the audited implementation.
8. **Longer horizon is not monotonic.** LAW's 1.5 s target is better than 3 s and 10 s variants in the shown planning results.

### Field-level distinctions now established

```text
CONTROLLABLE GENERATION != PLANNING INTERFACE
JOINT WORLD-ACTION GENERATION != CANDIDATE CONSEQUENCE EVALUATION
ACTION-CONDITIONED != REACTIVELY SUPERVISED
WM-ASSISTED PLANNING != ONLINE MODEL-BASED PLANNING
WORLD FIDELITY != DECISION UTILITY
LONGER HORIZON != BETTER PLANNING
```

These are field-understanding results, not gap claims.

## Immediate next task

See `state/NEXT_TASK.md`.

Perform a short Wave-2 comparability closeout on four remaining issues:

- Drive-WM: separate generation quality from detector/map/reward/candidate-selection contribution as far as paper evidence permits;
- OccWorld: normalize planning table/metric variants and identify the cleanest matched world-state comparisons;
- ViDAR: lock exactly what pretrained components survive downstream and which matched pretraining controls support planning claims;
- WoTE: fold the now-verified non-reactive supervision semantics into final evidence-strength grading.

Then close Wave 2 and start Wave 3 from the established interface taxonomy rather than from generic “WM” labels.

## Still forbidden

```text
no gap declaration
no method design
no broad paper accumulation
no P2-R/P3 rescue program
no forced risk-field insertion
```

## Research Brain architecture

GitHub raw MD + figures are the persistent GPT-readable primary-text layer; canonical PDFs remain source authority where archived/available. Public source repositories may be audited when a planning-interface ambiguity is decision-critical; source facts must record repo + commit + file + symbol.

A fresh session should read:

```text
START_HERE.md
state/CURRENT_STATE.md
state/NEXT_TASK.md
landscape/FIELD_ATLAS.md
landscape/PHASE_B_WAVE1_SYNTHESIS.md
landscape/PHASE_B_WAVE1_COMPARABILITY_AUDIT.md
landscape/PHASE_B_WAVE2_SYNTHESIS.md
```
