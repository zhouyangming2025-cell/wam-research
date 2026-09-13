# LATEST — Handoff

Session: 2026-09-13 — Research Brain hardening + targeted reading freeze.

## New-session fast path

```text
1. START_HERE.md
2. state/CURRENT_STATE.md
3. state/NEXT_TASK.md
4. hypotheses/P2R_PRIMARY.md
5. latest relevant audit/card only
```

Do not reload the whole corpus or old chats by default. `START_HERE.md` is the canonical one-file bootstrap.

## Research identity

```text
World Model + End-to-End + Planning-centric autonomous driving
```

Planning is the center of gravity.

**Risk field is optional, not required.** The owner's legacy expertise in risk / predictive risk fields / safety representation is a possible asset only after a real planning problem survives prior-art and falsification pressure. Never search for a problem merely to justify that expertise.

Canonical operating rules:

`state/RESEARCH_PRINCIPLES.md`

## Current research state

```text
P1_RETIRED  = RETIRED AS MAIN PROBLEM
P2R_PRIMARY = PRIMARY CANDIDATE, NOT CONFIRMED GAP
P3_HOLD     = HOLD AS BACKUP
```

P2-R asks whether, under the same state and same ego candidate set, factual/non-reactive and reactive counterfactual futures induce different ego-action orderings because surrounding agents respond differently to ego intervention.

Mechanism of interest:

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

Audit:

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

## New decision this session

Do not keep expanding the literature broadly. Freeze the next corpus growth to:

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

These metadata have been web-verified at discovery level; they are not `DOCUMENT_VERIFIED` until canonical PDFs are ingested and front pages checked.

After these eight are adjudicated, stop expansion and issue:

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

A paper can be strong overall yet fail to prove a specific mechanism. A threatening paper can still contain real limitations. Missing modules are not gaps; action conditioning is not proof of correct reactive counterfactual response.

## Immediate task

Phase 1: local corpus agent ingests only the eight targeted papers above, following the existing canonical PDF → hash → front-page verify → MinerU → QC → manifest → GitHub text-layer pipeline.

Phase 2: GPT-5.6 Sol deep-reads them adversarially in the order specified by `state/TARGETED_READING_QUEUE.md` and writes cards/audits directly here.

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
