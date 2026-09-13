# CURRENT_STATE

Last updated: 2026-09-14 — field-reconstruction reset

## Research north star

```text
World Model + End-to-End + Planning-centric autonomous driving
```

Planning is the center of gravity. Perception, video generation, JEPA/latent prediction, VLA, safety/risk modeling and simulation are supporting means, not the project identity.

**Risk field is optional, not required.** Prior risk/predictive-risk expertise is an asset, not a destination.

Canonical rules: `state/RESEARCH_PRINCIPLES.md`.

## Major methodological reset

The previous workflow moved too quickly from a small, hypothesis-biased paper set to candidate gaps (P1/P2-R/P3). That is now considered an insufficient basis for research-problem selection.

New active rule:

```text
FIELD UNDERSTANDING FIRST
→ reconstruct the planning-centric WAM landscape
→ understand method families, historical transitions, planner interfaces, supervision, evaluation and trade-offs
→ only then reopen problem/gap discovery
```

Canonical plan:

`landscape/FIELD_RECONSTRUCTION_PLAN.md`

Canonical taxonomy:

`landscape/PLANNING_WAM_TAXONOMY.md`

Living map:

`landscape/FIELD_ATLAS.md`

## Hypothesis status during reconstruction

| item | status |
|---|---|
| **P1_RETIRED — Planner-Induced Model Exploitation / Search-Support Gap** | RETIRED HISTORICAL HYPOTHESIS |
| **P2R_PRIMARY — Reactive Action-Ordering Gap** | **PARKED PROBE — NOT ACTIVE SEARCH TARGET** |
| **P3_HOLD — Decision Sufficiency of World Representations** | PARKED BACKUP PROBE |

`P2R_PRIMARY.md` retains the prior formulation for provenance, but the reading program must no longer be optimized around proving/killing P2-R.

## Current active stage

```text
FIELD RECONSTRUCTION — Planning-centric WAM Atlas
```

The goal is not to find a gap quickly. The goal is to be able to explain the field coherently:

- what major world-model families exist;
- why each family emerged;
- what world state each predicts;
- how future information reaches the planner;
- what supervision is actually available;
- how action conditioning / interaction / reactivity differ;
- what benchmark regimes really prove;
- what strong non-WM end-to-end planners reveal;
- what trade-offs recur across independent papers;
- what common claims have counterexamples.

## Field-reconstruction depth

Planned structure:

```text
Phase A: ~50–80 paper census at placement/overview depth
Phase B: ~15–25 representative anchor deep reads
Phase C: cross-family synthesis + historical evolution + evaluation map + trade-off map
Phase D: only then reopen research-problem discovery
```

This is deliberately different from both blind gap hunting and indiscriminate 100+ paper accumulation.

## Existing P2-R work — retained, not driving the program

Round-1 P2-R audit remains useful historical evidence:

`audits/literature/P2R_TARGETED_FAILURE_DEEP_READ_ROUND1.md`

Its result remains:

```text
NO DIRECT OBSERVED P2-R FAILURE HAS YET BEEN ESTABLISHED.
P2-R SURVIVES ROUND 1 AS A QUESTION, NOT AS A CONFIRMED GAP.
```

But this is no longer the project's active scientific target.

The previously prepared targeted Round-2 queue (BridgeSim, ReactSim-Bench, CausalDrive, Counterfactual Prediction, CRAFT + historical controls) is still valuable and should be integrated as part of the broader field atlas, especially families F7/F8/F11. It is no longer a gate that must be completed before looking elsewhere.

## Existing corpus status

- Batch 0A: 12 papers registered.
- 11 have canonical local PDF + MinerU raw MD; P0008 NPPC is paywalled and not readable from the corpus.
- The private GitHub repo contains the full text layer for the readable papers plus figures, manifest, reports, scripts, state, hypotheses and selected scientific cards/audits.
- Existing Batch 0A papers were selected partly to test earlier hypotheses and therefore are **not a representative sample of the whole field**.

## Immediate scientific need

Build a neutral census across the field families defined in `landscape/FIELD_ATLAS.md`, seeded by recent DWM surveys, planning-oriented end-to-end surveys, foundational WAM papers, strong non-WM planning baselines, interactive prediction/planning predecessors, and benchmark/evaluation papers.

No novelty/gap verdicts during census placement.

## Architecture / infrastructure in force

1. Canonical PDFs live only on local/NAS when locally archived.
2. GPT-readable primary-text layer = raw Markdown in the private repo when ingested.
3. Public official PDFs/pages may also be read directly for active research before local ingestion.
4. Exact wording / damaged formulas / missing visual evidence should be verified against official PDF/canonical local PDF.
5. Local corpus agent handles acquisition, conversion, metadata/QC, local assets and local code execution.
6. GPT-5.6 Sol handles field reconstruction, deep reading, synthesis, scientific interpretation and direct GitHub state updates.

## New-session bootstrap

A fresh session should start at `START_HERE.md`. During this phase it must understand that **field reconstruction, not P2-R gap hunting, is the active task**.
