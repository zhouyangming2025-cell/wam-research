# CURRENT_STATE

Last updated: 2026-09-14 — Wave 2 CLOSED; Wave 3 ACTIVE

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
FIELD RECONSTRUCTION — PHASE B: WAVE 3 ACTIVE
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

Stable controls carried forward:

1. conditional future response is not automatically causal/interventional response;
2. final planner score must be decomposed into representation, scorer, refinement, optimizer and rules;
3. matched controls dominate headline SOTA tables;
4. multimodal/diffusion action generation is not automatically world modeling;
5. candidate ranking is an independent planning bottleneck;
6. E2/E3/E4/E5/E6/E7 evaluation regimes are different claims;
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

Wave-2 closeout gate:

```text
comparative first pass       = COMPLETE
planning-interface audit     = COMPLETE
comparability/attribution    = COMPLETE
supervision-source audit     = COMPLETE
Wave 2                       = CLOSED
```

### Stable Wave-2 field understanding

“World model helps planning” decomposes into different mechanisms:

```text
GAIA-1   = controllable world generation; no operational planner interface
Drive-WM = candidate → visual future → perception/reward → selection
OccWorld = joint future occupancy + ego generation
WoTE     = candidate → future BEV → learned reward → selection
ViDAR    = future prediction as representation pretraining
LAW      = action-aware future-latent auxiliary supervision
```

Strongest evidence/boundaries:

1. **GAIA-1:** controllable generation is capability evidence, not direct planning evidence.
2. **Drive-WM:** generated futures are operationally useful for choosing among candidate commands, but generation fidelity is not cleanly isolated from detector/map quality, reward design or the candidate set. Better FID/FVD/KPM → better planning is **not established**.
3. **OccWorld:** headline SOTA comparisons are heterogeneous in input, auxiliary supervision and metric implementation. Internal ablations are much cleaner. A higher-resolution tokenizer reconstructs better but forecasts/plans worse; spatial/temporal dynamics ablations materially degrade both forecasting and planning.
4. **WoTE:** matched NAVSIM ablation `81.0 → 83.2 → 85.6 PDMS` separates trajectory-only, evaluator-only, and evaluator+future-state gains. Future-state input adds value beyond scorer-only in that setup. Source audit shows surrounding-agent target futures are fixed logged/GT tracks across ego candidates in the audited PDM path, so reactive oracle supervision is not established.
5. **ViDAR:** future point-cloud forecasting is a pretraining objective. The pretrained history/BEV encoder is transferred; the future decoder is not the deployed planner interface. Same downstream UniAD improves, but future temporal learning is still entangled with LiDAR/geometric supervision and latent-rendering design.
6. **LAW:** source code verifies that the current waypoint is produced before the WM future latent. Training uses future-latent reconstruction; test-time planning discards latent outputs. LAW is representation shaping, not online rollout-based action selection. Its 1.5 s target outperforms 3 s/10 s, so longer horizon is not monotonic.

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

These are field-understanding results, not gap claims.

## Wave 3 — ACTIVE

Canonical plan:

`landscape/PHASE_B_WAVE3_PLAN.md`

Anchors and order:

```text
1. Epona
2. DrivingGPT
3. DriveLaW
4. Auto-JEPA
5. DA-WAM
6. Think2Drive
```

Wave-3 purpose: compare what “world-action unification” actually means across shared latent/joint training, interleaved token generation, hidden-WM-feature action generation, compressed predictive representation, candidate-specific future evaluation, and WM-based imagined policy learning.

Immediate comparative questions:

- What exactly is unified: weights, conditioning, tokens, latent states, objectives, or decision process?
- What future/world representation survives at inference?
- Does planning consume a predicted future, a hidden WM feature, a candidate-specific future, or no explicit future?
- Which matched ablation isolates world/action coupling from stronger action modeling, representation learning, scorer/reward, extra data or RL?
- How are unexecuted alternative actions supervised?
- Which evaluation regime actually supports the planning claim?

## Immediate next task

See `state/NEXT_TASK.md`.

Begin Wave-3 comparative deep read with Epona → DrivingGPT, then continue through DriveLaW → Auto-JEPA → DA-WAM → Think2Drive. Build one cross-paper mechanism map rather than six isolated summaries.

## Still forbidden

```text
no gap declaration
no method design
no broad paper accumulation
no P2-R/P3 rescue program
no forced risk-field insertion
```

## Research Brain architecture

GitHub raw MD + figures are the persistent GPT-readable primary-text layer; canonical PDFs remain source authority where archived/available. Public source repositories may be audited only when a planning-interface ambiguity is decision-critical; source facts must record repo + commit + file + symbol.

A fresh session should read:

```text
START_HERE.md
state/CURRENT_STATE.md
state/NEXT_TASK.md
landscape/FIELD_ATLAS.md
landscape/PHASE_B_ANCHORS.md
landscape/PHASE_B_WAVE2_COMPARABILITY_AUDIT.md
landscape/PHASE_B_WAVE3_PLAN.md
```
