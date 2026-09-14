# LATEST — Handoff

Session: 2026-09-14 — Wave 1 and Wave 2 closed; Phase-B Wave 3 active.

## New-session fast path

```text
1. START_HERE.md
2. state/CURRENT_STATE.md
3. state/NEXT_TASK.md
4. landscape/FIELD_ATLAS.md
5. landscape/PHASE_B_ANCHORS.md
6. landscape/PHASE_B_WAVE2_COMPARABILITY_AUDIT.md
7. landscape/PHASE_B_WAVE3_PLAN.md
```

Do not default to P2-R/P3. Do not reload the whole corpus or old chats by default.

## Research identity

```text
World Model + End-to-End + Planning-centric autonomous driving
```

Risk-field / predictive-risk expertise is optional prior knowledge, not a required destination.

## Methodology

```text
UNDERSTAND FIELD FIRST
→ representative comparative deep reads
→ cross-family synthesis
→ only then research-problem discovery
```

No gap/method selection is authorized yet.

## Corpus / Phase-A status

```text
P0001–P0060 = 60 registered
58 RAW_MD_READY
F1–F11 census coverage = PASS
broad acquisition = FROZEN
25 Phase-B anchors = FIXED
```

## Wave 1 — CLOSED

Anchors: M2I, GameFormer, What Truly Matters, UniAD, nuPlan, NAVSIM, DiffusionDrive, DriveSuprim.

Artifacts:

- `landscape/PHASE_B_WAVE1_SYNTHESIS.md`
- `landscape/PHASE_B_WAVE1_COMPARABILITY_AUDIT.md`

Carry-forward controls:

```text
conditional future != intervention
matched controls > headline SOTA
candidate ranking is independent bottleneck
multimodal action generation != WM
prediction accuracy != planning evidence
evaluation regime is part of the claim
```

## Wave 2 — CLOSED

Anchors: GAIA-1, Drive-WM, OccWorld, WoTE, ViDAR, LAW.

Artifacts:

- `landscape/PHASE_B_WAVE2_SYNTHESIS.md`
- `landscape/PHASE_B_WAVE2_COMPARABILITY_AUDIT.md`
- `audits/literature/PHASE_B_WAVE2_INTERFACE_CODE_AUDIT.md`

Stable interpretation:

```text
GAIA-1   = controllable generation, no operational planner
Drive-WM = candidate visual future → perception/reward → select
OccWorld = joint future occupancy + ego generation
WoTE     = candidate future BEV → reward → select
ViDAR    = predictive pretraining
LAW      = action-aware future-latent representation shaping
```

Important Wave-2 evidence boundaries:

1. Drive-WM proves an operational future-as-evaluator interface, not that better FID/FVD/KPM causes better planning.
2. OccWorld's high-resolution tokenizer reconstructs better but forecasts/plans worse; main SOTA rows are heterogeneous, internal ablations are more causal.
3. WoTE has strong matched future-state evidence (`81.0 → 83.2 → 85.6 PDMS`) but the audited NAVSIM/PDM target pipeline uses fixed logged surrounding-agent futures across ego candidates.
4. ViDAR transfers a pretrained History/BEV encoder into the standard downstream stack; the Future Decoder is not the deployed planning interface.
5. LAW's current waypoint is computed before future-latent prediction; training uses the prediction loss, while test-time planning discards latent outputs.
6. Longer prediction horizon and higher reconstruction fidelity are not monotonic proxies for planning value.

Stable distinctions:

```text
CONTROLLABLE GENERATION != PLANNING INTERFACE
JOINT WORLD-ACTION GENERATION != CANDIDATE CONSEQUENCE EVALUATION
ACTION-CONDITIONED != REACTIVELY SUPERVISED
WM-ASSISTED PLANNING != ONLINE MODEL-BASED PLANNING
WORLD FIDELITY != DECISION UTILITY
CANDIDATE-SPECIFIC OUTPUT != CANDIDATE-SPECIFIC ORACLE SUPERVISION
```

## Wave 3 — ACTIVE

Plan:

`landscape/PHASE_B_WAVE3_PLAN.md`

Order:

```text
Epona
→ DrivingGPT
→ DriveLaW
→ Auto-JEPA
→ DA-WAM
→ Think2Drive
```

Purpose: map the transition from shared-latent/joint training through interleaved world-action tokens, hidden WM features, compressed predictive states, candidate-specific future latents, and Dreamer-style imagined policy learning.

Immediate task: start comparative deep read with **Epona ↔ DrivingGPT**, then add DriveLaW. Do not produce six disconnected summaries.

## Still forbidden

```text
no gap declaration
no method design
no broad paper accumulation
no P2-R/P3 rescue
no forced risk-field insertion
```

The repo, not conversation memory, is the canonical research authority.