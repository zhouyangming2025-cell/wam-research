# LATEST — Handoff

Session: 2026-09-13 — GPT-5.6 Sol scientific takeover.

## New-session read order

```text
1. state/CURRENT_STATE.md
2. state/DECISION_LOG.md
3. state/NEXT_TASK.md
4. handoff/LATEST.md
5. hypotheses/P2R_PRIMARY.md
```

Then read only the paper cards / raw MD / audits relevant to the current task. Do not reload the whole corpus by default.

## Current research state

```text
P1_RETIRED  = RETIRED AS MAIN PROBLEM
P2R_PRIMARY = PRIMARY CANDIDATE, NOT CONFIRMED GAP
P3_HOLD     = HOLD AS BACKUP
```

P2-R is precisely defined as the possible mismatch between factual/non-reactive and reactive counterfactual **ego-action ordering** under a fixed state and fixed candidate set.

Mechanism of interest:

```text
ego action
→ surrounding-agent response changes
→ candidate action ordering reverses
→ non-trivial planning regret
```

## What has changed since Integration Gate 0

- The private repo is **live and readable directly by ChatGPT through the GitHub connection**. GitHub push/authentication is no longer a blocker.
- GPT-5.6 Sol has taken over scientific interpretation and research-state maintenance.
- `hypotheses/P2R_PRIMARY.md` now contains the full definition, exclusions, kill criteria and Round-1 status.
- `hypotheses/P3_HOLD.md` now contains the actual backup-problem definition and prior-art risk.
- `audits/literature/P2R_TARGETED_FAILURE_DEEP_READ_ROUND1.md` records the first direct scientific audit using repo-hosted primary texts.

## Round-1 P2-R result

Reviewed from the existing corpus:

- P0002 SafeDrive
- P0004 BeTop
- P0003 GraphAD
- P0005 RiskWorld
- P0012 DA-WAM

Result:

```text
P2-R SURVIVES ROUND 1 AS A QUESTION, NOT AS A CONFIRMED GAP.
```

Important negative result:

```text
NO DIRECT OBSERVED P2-R FAILURE HAS YET BEEN ESTABLISHED.
```

Broad claims already considered occupied:

```text
interaction modeling matters
reactive / closed-loop evaluation matters
action-conditioned world modeling matters
candidate-specific future prediction matters
future information can improve trajectory scoring
```

DA-WAM is the strongest current nearest prior because it already maps each candidate trajectory to a distinct imagined future latent and scores the candidate with that latent. SafeDrive and BeTop strongly occupy generic candidate-conditioned interaction / reactive-planning framings.

## Next task

Ingest and attack P2-R with the direct literature set:

1. BridgeSim
2. ReactSim-Bench
3. CausalDrive
4. How Can Driving World Models Do Counterfactual Prediction?
5. CRAFT

Only if necessary, expand to What Truly Matters, Policy World Model, BeyondDrive, ELF-VLA.

Do not design a method yet.

## Corpus and infrastructure

- Batch 0A: 12 papers registered; 11 readable as raw MD in this repo; P0008 NPPC remains paywalled.
- Canonical PDFs stay local/NAS only.
- Raw MD + figures are the cross-session primary-text layer in this private repo.
- Exact wording / broken formula / visual evidence is extracted from local PDFs on demand.
- Windows native/.NET +1024 file framing is a known host quirk; canonical content hashes use the Python logical-byte view. The user has confirmed the Epona PDF can render in a normal Windows viewer after refresh; no further host-forensics work is planned.

## Division of labor

**GPT-5.6 Sol:** scientific deep read, adversarial review, hypothesis adjudication, paper cards, evidence synthesis, direct GitHub write-back.

**Local agent:** download, MinerU conversion, metadata/QC, source extraction from local PDFs, local source-code work, datasets/checkpoints/experiments.

The repo, not any one chat, is the canonical research memory.