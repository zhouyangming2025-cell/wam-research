# LATEST — Handoff

Session: 2026-09-13 — Research Brain hardening + Round-2 targeted execution start.

## New-session fast path

```text
1. START_HERE.md
2. state/CURRENT_STATE.md
3. state/NEXT_TASK.md
4. hypotheses/P2R_PRIMARY.md
5. handoff/LATEST.md
```

Copy-ready fresh-session prompt:

`handoff/NEW_SESSION_PROMPT.md`

Do not reload the whole corpus or old chats by default. If older evidence behind P1/P3 is needed, use `evidence/CORE_EVIDENCE_SNAPSHOT.md`.

## Research identity

```text
World Model + End-to-End + Planning-centric autonomous driving
```

Planning is the center of gravity.

**Risk field is optional, not required.** Legacy risk/predictive-risk expertise is preserved in `evidence/LEGACY_EXPERTISE_ASSETS.md` as an optional capability pool, not a method commitment.

Canonical operating rules:

`state/RESEARCH_PRINCIPLES.md`

## Current research state

```text
P1_RETIRED  = RETIRED AS MAIN PROBLEM
P2R_PRIMARY = PRIMARY CANDIDATE, NOT CONFIRMED GAP
P3_HOLD     = HOLD AS BACKUP
```

P2-R asks whether, under the same state and same ego candidate set, factual/non-reactive and reactive counterfactual futures induce different ego-action orderings because surrounding agents respond differently to ego intervention.

Mechanism:

```text
ego action
→ surrounding-agent response changes
→ candidate action ordering reverses
→ non-trivial planning regret
```

## Completed scientific work

Round 1 reviewed:

- P0002 SafeDrive
- P0004 BeTop
- P0003 GraphAD
- P0005 RiskWorld
- P0012 DA-WAM

Full audit:

`audits/literature/P2R_TARGETED_FAILURE_DEEP_READ_ROUND1.md`

Result:

```text
NO DIRECT OBSERVED P2-R FAILURE HAS YET BEEN ESTABLISHED.
P2-R SURVIVES ROUND 1 AS A QUESTION, NOT AS A CONFIRMED GAP.
```

Broad novelty framings already occupied:

```text
interaction modeling matters
reactive / closed-loop evaluation matters
action-conditioned world modeling matters
candidate-specific future prediction matters
future information can improve trajectory scoring
```

DA-WAM is the strongest current WAM nearest prior; SafeDrive and BeTop strongly occupy generic candidate-conditioned interaction / reactive-planning framings.

Cross-session evidence snapshot:

`evidence/CORE_EVIDENCE_SNAPSHOT.md`

## Round-2 execution started

Broad literature expansion is frozen. Canonical queue:

`state/TARGETED_READING_QUEUE.md`

### Direct P2-R set

1. BridgeSim — arXiv:2604.10856
2. ReactSim-Bench — arXiv:2606.14058
3. CausalDrive — arXiv:2606.15341
4. How Can Driving World Models Do Counterfactual Prediction? — arXiv:2608.11601
5. CRAFT — arXiv:2605.04470

### Historical novelty controls

6. GameFormer — arXiv:2303.05760 / ICCV 2023
7. M2I — arXiv:2202.11884 / CVPR 2022
8. Bahram et al. 2016 — DOI 10.1109/TVT.2015.2508009

Pre-ingest public-source reconnaissance has already been written to:

`audits/literature/P2R_ROUND2_PREINGEST_RECON.md`

Important early boundary: *How Can Driving World Models Do Counterfactual Prediction?* is highly relevant to counterfactual correctness but, at abstract level, intentionally studies a short-horizon setting where alternative ego action does **not** change surrounding-agent evolution; therefore it must not be misread as direct P2-R evidence before full review.

Local ingestion prompt is ready at:

`agent/prompts/ROUND2_TARGETED_INGEST.md`

The corpus agent should ingest only these eight records, produce raw MD + figures + skeleton cards + manifest/report updates, and stop. GPT-5.6 Sol then performs the scientific deep reads.

After the eight-paper adjudication, stop expansion and issue:

```text
P2-R SURVIVES
P2-R KILLED
NONE / EVIDENCE INSUFFICIENT
```

Do not widen P2-R to protect it. Do not design a method yet.

## Reading discipline

Every core paper must be treated objectively, not as a supporter/opponent of our hypothesis. Record both:

```text
strongest evidence for the paper
strongest limitation / alternative explanation
```

and separately:

```text
AUTHOR CLAIM
DIRECT EXPERIMENTAL EVIDENCE
OUR INFERENCE
```

Missing modules are not gaps; action conditioning is not proof of correct reactive counterfactual response; visual/world fidelity is not automatically decision sufficiency.

## Corpus / infrastructure

- Batch 0A: 12 registered; 11 readable as raw MD in this repo; P0008 NPPC remains paywalled.
- Canonical PDFs stay local/NAS only.
- Raw MD + figures are the cross-session primary-text layer.
- Exact wording / broken formula / visual evidence is extracted from local PDFs on demand.
- Windows native/.NET +1024 file framing is a known host quirk; canonical hashes use Python logical bytes.

## Division of labor

**GPT-5.6 Sol:** scientific deep read, adversarial review, hypothesis adjudication, cards/audits/state maintenance, direct GitHub write-back.

**Local corpus agent:** acquisition, MinerU conversion, metadata/QC, local-PDF extraction, local source-code work, datasets/checkpoints/experiments.

The repo, not conversation memory, is the canonical research authority.
