# LATEST — Handoff

Session: 2026-09-14 — Phase-A census closeout completed.

## New-session fast path

```text
1. START_HERE.md
2. state/CURRENT_STATE.md
3. state/NEXT_TASK.md
4. landscape/FIELD_ATLAS.md
5. landscape/PHASE_B_ANCHORS.md
6. state/RESEARCH_PRINCIPLES.md
```

Do not default to P2-R. Do not reload the whole corpus or old chats by default.

## Research identity

```text
World Model + End-to-End + Planning-centric autonomous driving
```

Planning is the center of gravity. Risk-field / predictive-risk expertise is optional prior knowledge, not a required destination.

## Methodology in force

```text
FIELD UNDERSTANDING FIRST
→ representative comparative deep reads
→ cross-family synthesis
→ only then research-problem discovery
```

P1/P2-R/P3 are parked provenance probes, not active search targets.

## Phase A is closed

Corpus:

```text
P0001–P0060 registered
58 RAW_MD_READY
2 lawful-source blockers: P0008 NPPC, P0020 Bahram 2016
```

Scientific closeout artifacts:

- `landscape/CENSUS_PHASE_A_ROUND1.md`
- `landscape/CENSUS_PHASE_A_ROUND2.md`
- `landscape/FIELD_ATLAS.md`
- `landscape/PHASE_B_ANCHORS.md`

The F1–F11 coverage audit passes at census depth. Broad paper acquisition is **frozen**.

## What Round 2 clarified

- Hydra-MDP / DriveSuprim / iPad are strong non-WM planning controls; scoring, hard-negative selection and proposal-centric representation can improve planning without future-world rollout.
- DriveVLM / OmniDrive / ORION show VLM/VLA reasoning and generative action are adjacent to WAM but not synonymous with a learned environment transition model.
- Think2Drive represents a distinct WM lineage: latent world dynamics as a neural simulator for RL policy learning.
- ViDAR is a clean pretraining-only world-prediction case.
- GenAD is a trajectory-level joint ego/agent future-generation precursor to later world-action models.
- Benchmark evolution is technically decisive: original nuScenes is not a planning benchmark; nuPlan formalizes planning OL/CL-NR/CL-R; NAVSIM is explicitly non-reactive; Bench2Drive is CARLA interactive closed loop; HUGSIM adds photorealistic reconstructed closed loop.

These are field distinctions, not research gaps.

## Phase-B anchor set

25 anchors are fixed in:

`landscape/PHASE_B_ANCHORS.md`

Secondary papers stay in the corpus and are promoted only when a concrete anchor comparison needs them.

## Immediate next task — Wave 1

Comparative deep-read set:

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

Required synthesis artifact:

`landscape/PHASE_B_WAVE1_SYNTHESIS.md`

Goal: establish what interaction, planning, multimodality and evaluation already looked like before modern WAMs, and what strong non-WM planners can already achieve. Later WM gains must be interpreted against this baseline.

Do not create eight disconnected summaries. Build one comparative account with source-backed per-paper evidence.

## Still forbidden

```text
no gap declaration
no method design
no broad literature accumulation
no P2-R/P3 optimization
no forced risk-field insertion
```

## Corpus / infrastructure

- Canonical local PDFs remain local/NAS when archived.
- GitHub raw MD + figures are the persistent GPT-readable text layer.
- The agent is now on-demand infrastructure support rather than a broad-ingestion worker.
- Integrity notes remain: repaired raw-MD ledger race; ViDAR Markdown omitted a code URL visible on PDF page 1; canonical hashes use Python logical bytes.

The repo, not conversation memory, is the canonical research authority.