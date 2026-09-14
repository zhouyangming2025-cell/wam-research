# CURRENT_STATE

Last updated: 2026-09-14 — post-agent census ingest sync

## Research north star

```text
World Model + End-to-End + Planning-centric autonomous driving
```

Planning is the center of gravity. Perception, video generation, JEPA/latent prediction, VLA, safety/risk modeling and simulation are supporting means, not the project identity.

**Risk field is optional, not required.** Prior risk/predictive-risk expertise is an asset, not a destination.

Canonical rules: `state/RESEARCH_PRINCIPLES.md`.

## Methodological rule in force

```text
FIELD UNDERSTANDING FIRST
→ reconstruct the planning-centric WAM landscape
→ understand method families, historical transitions, planner interfaces, supervision, evaluation and trade-offs
→ only then reopen problem/gap discovery
```

P1/P2-R/P3 are parked historical probes. They do not organize the current reading program.

## Current active stage

```text
FIELD RECONSTRUCTION — Phase-A closeout
```

Phase-A breadth acquisition has now reached the planned scale. The active task is no longer bulk paper acquisition; it is to finish **scientific placement and coverage audit**, freeze breadth expansion, and select the representative Phase-B anchor set.

## Latest repository / corpus status

Latest observed head:

```text
e0f4507  Complete Phase-A census round 1 text-layer ingest
```

The local corpus agent has now pushed three major supporting ingests:

1. `P0013–P0020`: prior interactive/reactive/counterfactual branch; 7 `RAW_MD_READY`, P0020 Bahram 2016 blocked `PAYWALLED_NO_OPEN_SOURCE`.
2. `P0021–P0034`: 14 coverage-hole works; all 14 `DOCUMENT_VERIFIED` + `RAW_MD_READY`.
3. `P0035–P0060`: 26 works from the existing Phase-A Round-1 census; all 26 `DOCUMENT_VERIFIED` + `RAW_MD_READY`.

Together with Batch 0A:

```text
60 stable paper IDs registered: P0001–P0060
58 RAW_MD_READY
2 lawful-source blockers:
  P0008 NPPC
  P0020 Bahram 2016
```

The corpus now has enough breadth for Phase-A closeout. Further broad ingestion is **paused** unless the coverage audit exposes a specific missing family/transition.

## Important distinction: corpus coverage != scientific placement

The agent correctly performed infrastructure work only. It did **not** assign F1–F11 scientific placement, novelty, gap, or research verdicts.

Current scientific map:

- `landscape/CENSUS_PHASE_A_ROUND1.md` provisionally places roughly 45 works/benchmarks/controls.
- The newly ingested `P0021–P0034` were chosen to fill Round-2 coverage holes but still need owner/GPT scientific placement in the common taxonomy.
- `P0035–P0060` mostly correspond to works already placed in Round 1; their new value is that full raw-MD text is now persistent in the repo.

## Immediate next task

See `state/NEXT_TASK.md`.

In order:

1. Read `P0021–P0034` at **census depth**, not deep-read depth.
2. Create `landscape/CENSUS_PHASE_A_ROUND2.md` with neutral taxonomy placement.
3. Update `FIELD_ATLAS.md` and perform an F1–F11 coverage audit.
4. Decide whether any truly essential family/transition remains missing. `Hydra-MDP++` and `NAVSIM-v2` remain unresolved optional follow-ups, not automatic blockers.
5. Freeze Phase-A breadth expansion.
6. Select roughly **15–25 representative anchor papers** for Phase-B deep reading, justified by field coverage and historical/architectural diversity rather than prior hypotheses.

No method design and no gap declaration before Phase B/C synthesis.

## Integrity notes from latest agent pushes

- A concurrent raw-MD ledger write race was detected and repaired from stored artifacts; the write path was changed so later processes re-read before writing.
- `P0028 ViDAR` has one known raw-MD extraction omission: the repository URL printed on PDF page 1 is absent from Markdown; the manifest note preserves this provenance fact.
- Canonical PDF/raw-MD hashes continue to use logical bytes through the Python corpus I/O path.

## New-session bootstrap

A fresh session should begin with:

```text
START_HERE.md
state/CURRENT_STATE.md
state/NEXT_TASK.md
landscape/FIELD_ATLAS.md
landscape/CENSUS_PHASE_A_ROUND1.md
```

Then read only the raw MD needed for the active census-placement or anchor-deep-read task.
