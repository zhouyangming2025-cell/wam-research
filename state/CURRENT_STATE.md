# CURRENT_STATE

Last updated: 2026-09-13 — GPT-5.6 Sol scientific takeover

## Hypothesis status

| slot | hypothesis | status |
|---|---|---|
| Primary candidate | **P2R_PRIMARY — Reactive Action-Ordering Gap in Planning-centric WAMs** | PRIMARY CANDIDATE, NOT CONFIRMED GAP |
| Backup | **P3_HOLD — Decision Sufficiency of World Representations** | HOLD AS BACKUP |
| Retired | **P1_RETIRED — Planner-Induced Model Exploitation / Search-Support Gap** | RETIRED AS MAIN PROBLEM |

## Current stage

**P2-R Targeted Failure Deep Read**

Round 1 is complete on the existing Batch 0A corpus. Scientific review has now moved from the corpus-librarian agent to GPT-5.6 Sol using this private repo directly.

Round-1 audit:

`audits/literature/P2R_TARGETED_FAILURE_DEEP_READ_ROUND1.md`

## Current P2-R definition

For the same current state `s` and the same ego candidate set `A = {a_i}`:

```text
rank_factual/nonreactive(A) ?= rank_reactive(A)
```

The mechanism of interest is:

```text
ego action
→ surrounding-agent response changes
→ candidate action ordering reverses
→ non-trivial planning regret
```

This is narrower than a generic OL→CL gap, reactive planning, action-conditioned world modeling, or candidate-specific future prediction.

## Round-1 scientific verdict

The existing repo corpus is already sufficient to reject several broad formulations as novelty:

```text
Planning should model interactions.                    OCCUPIED
Reactive / closed-loop evaluation matters.             OCCUPIED
World models should be conditioned on ego actions.     OCCUPIED
Each candidate should receive its own future.          OCCUPIED
Future information can improve candidate scoring.      OCCUPIED
```

Key nearest-prior pressure:

- SafeDrive: candidate-conditioned sparse worlds + safety-based candidate selection.
- BeTop: explicit future interaction structure + reactive closed-loop evaluation.
- DA-WAM: candidate-specific future latent + candidate-specific scoring.

However, the five reviewed papers do **not** directly establish the precise matched-state / matched-candidate factual-vs-reactive ordering variable.

Therefore:

```text
NO DIRECT OBSERVED P2-R FAILURE HAS YET BEEN ESTABLISHED.
P2-R SURVIVES ROUND 1 AS A QUESTION, NOT AS A CONFIRMED GAP.
```

No method design is authorized.

## Next scientific task

Attack P2-R with the direct reactive / counterfactual literature:

1. BridgeSim
2. ReactSim-Bench
3. CausalDrive
4. How Can Driving World Models Do Counterfactual Prediction?
5. CRAFT

Secondary only if needed: What Truly Matters, Policy World Model, BeyondDrive, ELF-VLA.

The next decision is not "how to solve P2-R" but whether P2-R should survive at all.

## Corpus status

- Batch 0A: 12 papers registered.
- 11 have canonical local PDF + MinerU raw MD; P0008 NPPC is paywalled and not readable from the corpus.
- The private GitHub repo contains the full text layer for the 11 readable papers plus figures, manifest, reports, scripts, state, hypotheses and selected paper cards.
- Canonical PDFs remain local/NAS only.

## Architecture in force

1. Canonical PDFs live only on local/NAS.
2. GPT-readable primary-text layer = MinerU raw Markdown in this private repo.
3. ChatGPT Library is optional and not required.
4. Exact wording / damaged formulas / missing visual evidence are extracted on demand from the local canonical PDF.
5. The corpus-librarian agent handles downloading, conversion, local assets and code execution; GPT-5.6 Sol handles scientific interpretation, adversarial review, hypothesis decisions and direct GitHub research-state updates.
6. `pdf_sha256` is based on the logical document bytes read through the canonical Python corpus I/O path.
7. Windows native/.NET +1024 framed view is a known host quirk and is not a scientific blocker.

## Superseded states

Historical files that record P1 as the primary hypothesis are provenance only and are superseded by the current status above.