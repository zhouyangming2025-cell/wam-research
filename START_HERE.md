# START_HERE — WAM Research Brain

**Purpose:** a fresh GPT-5.6 Sol session should recover the project direction and current stage in under a minute without reconstructing old chats.

Last updated: 2026-09-14 — Wave 3 active

## 1. Research north star

```text
World Model + End-to-End + Planning-centric autonomous driving
```

Planning is the center of gravity. Perception, video generation, JEPA/latent prediction, VLA, safety/risk modeling and simulation matter only insofar as they affect planning capability, decision quality, closed-loop behavior, or scientific understanding of planning.

**Risk field is NOT a required destination.** Prior risk/predictive-risk expertise is an optional capability pool, not a research commitment.

## 2. Methodological reset

The project previously moved too quickly from a small paper set to candidate gaps. That workflow is suspended.

Active rule:

```text
UNDERSTAND THE FIELD FIRST
→ representative comparative deep reads
→ cross-family synthesis
→ only then research-problem / gap discovery
```

P1/P2-R/P3 are parked historical probes and do not organize the reading program.

## 3. Current stage

```text
FIELD RECONSTRUCTION — PHASE B: WAVE 3 ACTIVE
```

Phase A is complete at census depth:

```text
60 stable IDs: P0001–P0060
58 RAW_MD_READY
2 lawful-source blockers: P0008 NPPC, P0020 Bahram 2016
F1–F11 coverage PASS
broad ingestion FROZEN
25 representative anchors FIXED
```

Wave 1 and Wave 2 are closed. Their evidence is now a binding baseline for Wave 3.

## 4. What must not be collapsed

The planning-centric taxonomy distinguishes:

```text
WM for controllable generation
!= predictive pretraining
!= auxiliary future supervision
!= online hidden future representation
!= candidate-specific future evaluator
!= joint world-action generation
!= WM as an RL imagination environment
```

Also:

```text
VLA/VLM planner != automatically a world model
multimodal trajectory planner != automatically a world model
candidate scorer != automatically a world model
visual simulator realism != behavioral-agent realism
action-conditioned != reactively supervised
candidate-specific output != candidate-specific oracle supervision
```

Evaluation regimes remain distinct:

```text
nuScenes-style open-loop logs
nuPlan OL / CL-NR / CL-R
NAVSIM non-reactive pseudo-simulation
Bench2Drive CARLA interactive closed loop
HUGSIM photorealistic reconstructed closed loop
standardized real-vehicle closed loop (currently sparse)
```

## 5. Closed-wave baseline

### Wave 1 — historical/non-WM/evaluation controls

Artifacts:

- `landscape/PHASE_B_WAVE1_SYNTHESIS.md`
- `landscape/PHASE_B_WAVE1_COMPARABILITY_AUDIT.md`

Stable controls include: conditional prediction is not intervention; candidate ranking is an independent bottleneck; multimodal action generation is not automatically WM; prediction accuracy is not planning evidence; final planner gains must be decomposed; benchmark regime changes claim semantics.

### Wave 2 — world representation and planning interfaces

Artifacts:

- `landscape/PHASE_B_WAVE2_SYNTHESIS.md`
- `landscape/PHASE_B_WAVE2_COMPARABILITY_AUDIT.md`
- `audits/literature/PHASE_B_WAVE2_INTERFACE_CODE_AUDIT.md`

Stable result:

```text
GAIA-1   = controllable generation; no operational planner interface
Drive-WM = candidate → visual future → perception/reward → selection
OccWorld = joint future occupancy + ego generation
WoTE     = candidate → future BEV → learned reward → selection
ViDAR    = future prediction as representation pretraining
LAW      = action-aware future-latent auxiliary representation shaping
```

Key corrections:

- better generation/reconstruction quality is not automatically better planning;
- longer future horizon is not automatically better planning;
- an online candidate-conditioned model may still lack reactive per-action oracle supervision;
- a world-model loss can improve planning while the predicted future is absent from the deployed decision path.

## 6. Immediate task — Wave 3

Canonical plan:

`landscape/PHASE_B_WAVE3_PLAN.md`

Read comparatively in this order:

```text
Epona
→ DrivingGPT
→ DriveLaW
→ Auto-JEPA
→ DA-WAM
→ Think2Drive
```

Wave-3 goal: understand what “world-action unification” actually means across:

```text
shared latent / joint training
interleaved world-action token generation
hidden WM feature → action generation
compressed planning-oriented predictive target
candidate-specific future latent → scoring
Dreamer-style WM → imagined RL policy learning
```

Start with **Epona ↔ DrivingGPT**, then use DriveLaW as the next bridge. Build one comparison matrix; do not create six isolated summaries.

## 7. Deep-read evidence discipline

Use separately:

```text
AUTHOR CLAIM
DIRECT EXPERIMENTAL EVIDENCE
OUR INFERENCE
```

Always ask:

```text
What exactly is predicted?
What gets direct supervision?
What future target source exists for alternative actions?
What survives at inference?
How does planning consume it?
What alternative mechanism could explain the gain?
What evaluation regime supports the claim?
```

Every anchor must receive both its strongest evidence and strongest limitation.

## 8. Still forbidden

```text
no gap declaration yet
no method design yet
no broad paper accumulation
no P2-R/P3 rescue program
no forced risk-field insertion
```

## 9. Fast new-session read order

```text
1. START_HERE.md
2. state/CURRENT_STATE.md
3. state/NEXT_TASK.md
4. landscape/FIELD_ATLAS.md
5. landscape/PHASE_B_ANCHORS.md
6. landscape/PHASE_B_WAVE2_COMPARABILITY_AUDIT.md
7. landscape/PHASE_B_WAVE3_PLAN.md
```

Then read only the primary texts required for the active Wave-3 comparison.

## 10. Source hierarchy

```text
Official/canonical PDF       = exact source authority
GitHub raw MD + figures      = GPT-readable primary-text layer
Paper Card                   = curated paper understanding
Wave synthesis / Field Atlas = cross-paper understanding
State files                  = canonical project decisions
Chat                         = temporary reasoning workspace
```

If raw MD is ambiguous, verify against the official/canonical PDF rather than guessing.

## 11. Division of labor

**GPT-5.6 Sol:** comparative anchor deep reads, cross-paper synthesis, atlas/cards/state maintenance, scientific judgement.

**Local corpus agent:** on-demand acquisition/extraction, MinerU/QC, local code execution, datasets/checkpoints/experiments.

The repo — not conversation memory — is the research authority.