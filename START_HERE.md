# START_HERE — WAM Research Brain

**Purpose:** a new GPT-5.6 Sol session should be able to resume the project from this file in under a minute without reconstructing prior chats.

Last updated: 2026-09-13

## 1. Research north star

```text
World Model + End-to-End + Planning-centric autonomous driving
```

Planning is the center of gravity. Perception, video generation, JEPA/latent prediction, VLA, safety/risk modeling and simulation matter only insofar as they affect planning capability, decision quality, closed-loop behavior, or scientific understanding of planning failures.

**Risk field is NOT a required destination.** The owner's prior expertise in risk / predictive risk fields / safety representation is an optional asset. Never force a research problem to fit that expertise.

Correct order:

```text
observed planning failure
→ cause / missing capability
→ why existing methods do not already solve it
→ research question
→ only then ask whether prior risk / interaction / safety expertise helps
→ possible method
```

## 2. Current hypothesis state

| slot | hypothesis | status |
|---|---|---|
| Primary | `P2R_PRIMARY` — Reactive Action-Ordering Gap in Planning-centric WAMs | **PRIMARY CANDIDATE, NOT CONFIRMED GAP** |
| Backup | `P3_HOLD` — Decision Sufficiency of World Representations | **HOLD AS BACKUP** |
| Retired | `P1_RETIRED` — Planner-Induced Model Exploitation / Search-Support Gap | **RETIRED AS MAIN PROBLEM** |

P2-R currently asks, for a fixed state and fixed ego candidate set:

```text
rank_factual/nonreactive(A) ?= rank_reactive(A)
```

The only mechanism of interest is:

```text
ego action
→ surrounding-agent response changes
→ candidate action ordering reverses
→ non-trivial planning regret
```

This is deliberately narrower than generic OL→CL mismatch, generic reactive planning, action-conditioned world modeling, or candidate-specific future prediction.

## 3. Current scientific verdict

Round 1 is complete on SafeDrive, BeTop, GraphAD, RiskWorld and DA-WAM.

```text
NO DIRECT OBSERVED P2-R FAILURE HAS YET BEEN ESTABLISHED.
P2-R SURVIVES ROUND 1 AS A QUESTION, NOT AS A CONFIRMED GAP.
```

Broad framings already considered occupied:

```text
Planning should model interactions.
Reactive / closed-loop evaluation matters.
World models should be conditioned on ego actions.
Each candidate should receive its own predicted future.
Future information can improve candidate scoring.
```

Strongest nearest-prior pressure:

- **DA-WAM:** candidate-specific future latent + candidate-specific scorer.
- **SafeDrive:** candidate-conditioned sparse worlds + fine-grained safety selection.
- **BeTop:** explicit future-interaction structure + reactive closed-loop evaluation.

Do not design a method yet.

## 4. Immediate task

Freeze broad corpus expansion. Add only the high-discrimination set in `state/TARGETED_READING_QUEUE.md`, then deep-read it adversarially.

Core P2-R attack set:

1. BridgeSim
2. ReactSim-Bench
3. CausalDrive
4. How Can Driving World Models Do Counterfactual Prediction?
5. CRAFT

Historical controls to prevent renaming old interactive-planning ideas as WAM novelty:

6. GameFormer
7. M2I
8. Bahram et al. 2016 — replanning-aware interactive scene prediction and planning

After these are ingested, **stop expanding** unless a concrete unresolved question requires a specific additional paper.

## 5. How every core paper must be read

Do not produce a generic summary. For each paper determine:

```text
Exact problem
Input → numerical representation → intermediate future representation → planner consumption
Training supervision: what has real future supervision? what is inferred/counterfactual?
Inference / planning coupling
Evaluation regime: open-loop / non-reactive / reactive / real closed-loop
Strongest direct evidence
Strongest limitation / alternative explanation
Observed failure (if any) vs our inference
What it proves
What it does NOT prove
Prior-art pressure on P2-R / P3
Residual question after reading
```

Every paper must be treated symmetrically: record both the strongest case **for** the method and the strongest case **against** over-interpreting it.

Use three evidence labels:

```text
AUTHOR CLAIM
DIRECT EXPERIMENTAL EVIDENCE
OUR INFERENCE
```

Never convert a missing module into a research gap. Never convert a rollout into closed-loop evidence. Never convert action conditioning into proof of correct intervention response.

## 6. Fast new-session read order

For an ordinary continuation, read only:

```text
1. START_HERE.md                       ← this file
2. state/CURRENT_STATE.md
3. state/NEXT_TASK.md
4. hypotheses/P2R_PRIMARY.md
5. latest relevant audit/card only
```

Read `state/DECISION_LOG.md` only when provenance/rationale is needed. Do **not** reload all raw papers or all old chats.

Current latest audit:

`audits/literature/P2R_TARGETED_FAILURE_DEEP_READ_ROUND1.md`

## 7. Source hierarchy

```text
Local/NAS canonical PDF = exact source authority
GitHub raw MD + figures  = GPT-readable primary-text layer
Paper Card               = curated scientific knowledge
State / hypothesis files = canonical research decisions
Chat                      = temporary reasoning workspace
```

If raw MD is ambiguous or a formula/figure is damaged, request a source extract from the local canonical PDF rather than guessing.

## 8. Division of labor

**GPT-5.6 Sol:** deep reading, adversarial scientific review, cross-paper synthesis, hypothesis adjudication, cards/audits/state updates, direct GitHub write-back.

**Local corpus agent:** acquisition, canonical PDF, MinerU conversion, metadata/QC, local-PDF source extraction, local code execution, datasets/checkpoints/experiments.

## 9. Session closeout rule

Any session that materially changes the research must update, before ending:

```text
state/CURRENT_STATE.md
state/DECISION_LOG.md        (only if a decision changed)
state/NEXT_TASK.md
state/RESEARCH_LEDGER.md     (if corpus/gate changed)
handoff/LATEST.md
relevant hypothesis/card/audit
```

The repo — not conversation memory — is the research authority.
