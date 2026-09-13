# LATEST — Handoff

Session: 2026-09-14 — field-reconstruction reset.

## New-session fast path

```text
1. START_HERE.md
2. state/CURRENT_STATE.md
3. state/NEXT_TASK.md
4. state/RESEARCH_PRINCIPLES.md
5. landscape/FIELD_RECONSTRUCTION_PLAN.md
6. landscape/FIELD_ATLAS.md
```

Copy-ready fresh-session prompt:

`handoff/NEW_SESSION_PROMPT.md`

Do not default to P2-R. Do not reload the whole corpus or old chats by default.

## Research identity

```text
World Model + End-to-End + Planning-centric autonomous driving
```

Planning is the center of gravity.

Risk field / predictive risk field expertise is optional prior knowledge, not a required destination.

## Critical methodological change

The project recognized that prior work was too gap-driven too early. The active program is no longer:

```text
pick a candidate gap
→ search around it
→ try to keep/refute it
```

It is now:

```text
reconstruct the field
→ understand major families and why they emerged
→ understand representations, supervision, planning interfaces and evaluation
→ synthesize recurring trade-offs / contradictions / counterexamples
→ only then formulate research problems
```

## Current hypothesis status

```text
P1 = retired historical hypothesis
P2-R = parked probe, not active search target
P3 = parked backup probe
```

The prior P2-R audit remains valid as historical evidence but does not organize the reading program.

## Current active task

Build the first neutral planning-centric WAM census.

Target:

```text
~50–80 papers at census/placement depth
~15–25 representative anchors for full deep reading
```

Field families are provisionally defined in:

`landscape/FIELD_ATLAS.md`

Common placement taxonomy:

`landscape/PLANNING_WAM_TAXONOMY.md`

## What the census must include

Not only WAM papers. It must also include:

- strong end-to-end planning baselines without explicit WM;
- interactive prediction/planning predecessors;
- reactive simulator / closed-loop training papers;
- benchmark/evaluation papers that change how planning results should be interpreted;
- strong counterexamples to common claims.

The existing Batch 0A set is valuable but hypothesis-biased and is not a representative sample of the field.

## Existing P2-R branch

Round-1 audit:

`audits/literature/P2R_TARGETED_FAILURE_DEEP_READ_ROUND1.md`

Historical result:

```text
NO DIRECT OBSERVED P2-R FAILURE HAS YET BEEN ESTABLISHED.
```

The previously prepared Round-2 set — BridgeSim, ReactSim-Bench, CausalDrive, Counterfactual Prediction, CRAFT, GameFormer, M2I, Bahram et al. — now fills interactive/reactive/counterfactual atlas families instead of acting as the entire research gate.

## Scientific discipline

During field reconstruction:

- no per-paper gap/novelty verdict during census placement;
- every anchor paper gets strongest evidence + strongest limitation;
- distinguish `AUTHOR CLAIM / DIRECT EXPERIMENTAL EVIDENCE / OUR INFERENCE`;
- trace exact observation→future→planner flow;
- record what receives real future supervision vs inferred/counterfactual supervision;
- keep evaluation regimes distinct;
- check historical continuity so new WAM language does not hide old planning ideas;
- treat strong non-WM planners as necessary controls.

## Corpus / infrastructure

- Batch 0A: 12 registered; 11 readable as raw MD in this repo; P0008 NPPC remains paywalled.
- Canonical local PDFs remain local/NAS when archived.
- Public official PDFs/pages can be read directly for active field research before local ingestion.
- Raw MD + figures remain the cross-session primary-text layer once ingested.
- Windows native/.NET +1024 file framing is a known host quirk; canonical local hashes use Python logical bytes.

## Division of labor

**GPT-5.6 Sol:** field census, survey/primary-paper research, anchor deep reads, cross-family synthesis, atlas/taxonomy maintenance, scientific judgement, direct GitHub write-back.

**Local corpus agent:** bulk acquisition, local archival, MinerU conversion, metadata/QC, source extraction, local code work, datasets/checkpoints/experiments.

The repo, not conversation memory, is the canonical research authority.
