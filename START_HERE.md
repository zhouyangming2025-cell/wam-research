# START_HERE — WAM Research Brain

**Purpose:** a fresh GPT-5.6 Sol session should recover the project direction and current stage in under a minute without reconstructing old chats.

Last updated: 2026-09-14

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
FIELD RECONSTRUCTION — PHASE B: ANCHOR DEEP READS
```

Phase A is complete at census depth.

Corpus:

```text
60 stable IDs: P0001–P0060
58 RAW_MD_READY
2 lawful-source blockers: P0008 NPPC, P0020 Bahram 2016
```

Scientific artifacts:

- `landscape/CENSUS_PHASE_A_ROUND1.md`
- `landscape/CENSUS_PHASE_A_ROUND2.md`
- `landscape/FIELD_ATLAS.md`
- `landscape/PHASE_B_ANCHORS.md`

F1–F11 coverage passes for anchor selection. Broad ingestion is **frozen**.

## 4. Core field structure established by Phase A

Do not collapse the following distinctions:

```text
WM for data generation
!= WM for predictive pretraining
!= WM as auxiliary future supervision
!= inference-time future representation
!= per-candidate future evaluator
!= joint world-action model
!= WM as RL training simulator
```

Also:

```text
VLA/VLM planner != automatically a world model
multimodal trajectory planner != automatically a world model
candidate scorer != automatically a world model
visual simulator realism != behavioral-agent realism
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

A key historical correction: the original nuScenes paper is a multimodal scene/perception benchmark, not an end-to-end planning benchmark; later literature retrofits planning protocols onto its logs.

## 5. Phase-B anchor strategy

Canonical set:

`landscape/PHASE_B_ANCHORS.md`

25 anchors were selected to explain the field across historical interaction roots, strong non-WM controls, visual/occupancy/latent WMs, world-action models, WM-RL, VLA, reactive simulation and benchmark evolution.

Secondary papers remain in the corpus and are promoted only if an anchor comparison exposes a concrete missing link.

## 6. Immediate task — Wave 1

Read comparatively:

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

Required output:

`landscape/PHASE_B_WAVE1_SYNTHESIS.md`

Wave 1 must establish the historical/non-WM/evaluation baseline before modern WAM gains are interpreted.

Do **not** produce eight isolated summaries. For each paper trace problem, numerical representation, supervision, inference/planner interface, evaluation evidence, strongest strength, strongest limitation, what is and is not established, then synthesize across papers.

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
What survives at inference?
How does planning consume it?
What alternative mechanism could explain the reported gain?
What evaluation regime supports the claim?
```

Every anchor must receive both its strongest evidence and strongest limitation. No paper is a “supporter” or “opponent” of our research direction.

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
6. state/RESEARCH_PRINCIPLES.md
```

Then read only the primary texts required for the current Phase-B wave.

## 10. Source hierarchy

```text
Official/canonical PDF       = exact source authority
GitHub raw MD + figures      = GPT-readable primary-text layer
Paper Card                   = curated paper understanding
Field Atlas / wave synthesis = cross-paper understanding
State files                  = canonical project decisions
Chat                         = temporary reasoning workspace
```

If raw MD is ambiguous, verify against the official/canonical PDF rather than guessing.

## 11. Division of labor

**GPT-5.6 Sol:** comparative anchor deep reads, cross-paper synthesis, atlas/cards/state maintenance, scientific judgement.

**Local corpus agent:** on-demand acquisition/extraction, MinerU/QC, local code execution, datasets/checkpoints/experiments.

The repo — not conversation memory — is the research authority.