# wam-research

Cross-session Research Brain for **World Model + End-to-End + Planning-centric autonomous driving**.

Text and extracted figures only — canonical PDFs remain local/NAS.

## New session: start here

```text
1. START_HERE.md
2. state/CURRENT_STATE.md
3. state/NEXT_TASK.md
4. hypotheses/P2R_PRIMARY.md
5. latest relevant audit/card only
```

`START_HERE.md` is intentionally self-contained so a fresh GPT-5.6 Sol session can recover the research direction, current hypothesis, scientific discipline and immediate task without re-reading old chats or the whole corpus.

A copy-ready prompt for a totally fresh session lives at:

`handoff/NEW_SESSION_PROMPT.md`

Read `state/DECISION_LOG.md` only when decision provenance is needed. If older cross-paper evidence is needed, prefer `evidence/CORE_EVIDENCE_SNAPSHOT.md` over old conversations.

## Research scope

```text
World Model + End-to-End + Planning-centric
```

Planning is the center of gravity. Risk/safety modeling, perception, generation, VLA and representation learning matter only insofar as they contribute to planning capability or explain planning failures.

**Risk field is optional, not a required destination.** Prior expertise is used only if the surviving problem genuinely benefits from it. See `state/RESEARCH_PRINCIPLES.md` and `evidence/LEGACY_EXPERTISE_ASSETS.md`.

## Current state

| slot | hypothesis | status |
|---|---|---|
| Primary | P2R_PRIMARY — Reactive Action-Ordering Gap in Planning-centric WAMs | PRIMARY CANDIDATE, NOT CONFIRMED GAP |
| Backup | P3_HOLD — Decision Sufficiency of World Representations | HOLD AS BACKUP |
| Retired | P1_RETIRED — Planner-Induced Model Exploitation / Search-Support Gap | RETIRED AS MAIN PROBLEM |

Current stage: **P2-R Targeted Failure Deep Read**.

Round 1 has been completed on SafeDrive, BeTop, GraphAD, RiskWorld and DA-WAM. Result:

```text
NO DIRECT OBSERVED P2-R FAILURE HAS YET BEEN ESTABLISHED.
P2-R SURVIVES ROUND 1 AS A QUESTION, NOT AS A CONFIRMED GAP.
```

Latest full primary-text audit:

`audits/literature/P2R_TARGETED_FAILURE_DEEP_READ_ROUND1.md`

Abstract/project-page reconnaissance for Round 2:

`audits/literature/P2R_ROUND2_PREINGEST_RECON.md`

## Immediate reading gate

Broad corpus expansion is paused. The frozen high-discrimination queue is:

`state/TARGETED_READING_QUEUE.md`

Core direct set: BridgeSim, ReactSim-Bench, CausalDrive, *How Can Driving World Models Do Counterfactual Prediction?*, CRAFT.

Historical controls: GameFormer, M2I, Bahram et al. 2016 replanning-aware interactive prediction/planning.

After these are adjudicated, stop expanding unless a concrete unresolved question requires another paper.

## Repository layout

```text
START_HERE.md                         one-file new-session bootstrap
state/CURRENT_STATE.md               current hypothesis/stage/verdict
state/NEXT_TASK.md                   single next task + stop condition
state/RESEARCH_PRINCIPLES.md         canonical scientific operating rules
state/TARGETED_READING_QUEUE.md      frozen targeted expansion set
state/DECISION_LOG.md                decision provenance
state/RESEARCH_LEDGER.md             factual corpus/gate ledger
hypotheses/                          P1_RETIRED, P2R_PRIMARY, P3_HOLD
evidence/CORE_EVIDENCE_SNAPSHOT.md   compact legacy/current cross-paper evidence
evidence/LEGACY_EXPERTISE_ASSETS.md  optional prior risk/safety capabilities
audits/literature/                   cross-paper adversarial audits
papers/cards/                        curated per-paper scientific cards
papers/raw_md/<PXXXX_Short>/         MinerU raw Markdown + images
manifests/CORPUS_MANIFEST.csv        corpus registry
handoff/LATEST.md                    latest session handoff
handoff/NEW_SESSION_PROMPT.md        copy-ready fresh-session bootstrap prompt
scripts/                             ingestion/verification scripts
experiment_logs/                     conversion logs
BATCH_0A_*.md                        ingest reports
```

## Source hierarchy

```text
Local/NAS canonical PDF = exact source authority
GitHub raw MD + figures  = GPT-readable primary-text layer
Paper Card               = curated scientific knowledge
State / hypothesis files = canonical research decisions
Chat                      = temporary reasoning workspace
```

If raw MD is ambiguous, request a source extract from the local canonical PDF rather than guessing.

## Corpus state

Batch 0A: 12 papers registered; 11 have canonical local PDFs and raw MD here. P0008 NPPC is blocked by paywall/no verified open version.

The targeted Round-2 papers have not yet been assigned Paper IDs or ingested; see `state/TARGETED_READING_QUEUE.md`.

## Scientific discipline

Every core paper must be assessed symmetrically:

```text
strongest evidence for the paper
strongest limitation / alternative explanation
what it proves
what it does NOT prove
observed failure vs our inference
prior-art pressure
residual question
```

Use `AUTHOR CLAIM`, `DIRECT EXPERIMENTAL EVIDENCE`, and `OUR INFERENCE` separately. Missing modules are not automatically gaps; rollout is not automatically closed-loop; action conditioning is not proof of correct reactive counterfactual behavior.

## Division of labor

**GPT-5.6 Sol:** scientific deep read, adversarial review, cross-paper synthesis, hypothesis adjudication, cards/audits/state updates, direct GitHub write-back.

**Local corpus agent:** acquisition, MinerU conversion, metadata/QC, local-PDF source extraction, source-code execution, datasets/checkpoints/experiments.

## Integrity / host note

`pdf_sha256` / `raw_md_sha256` use logical bytes read through the canonical Python corpus I/O path. The Windows host exposes a recorded +1024 native/.NET framed view; this is a known host quirk, not a scientific blocker.

The repo — not conversation history — is the canonical research memory.
