# NEXT_TASK

## 唯一下一任务

> Complete the frozen **targeted reading gate** before any method design, experiment, broad corpus expansion, or return to risk-field engineering.

Canonical queue:

`state/TARGETED_READING_QUEUE.md`

## Phase 1 — local corpus ingestion

Ingest only these papers, in this order of acquisition priority:

### Core P2-R set

1. BridgeSim — arXiv:2604.10856
2. ReactSim-Bench — arXiv:2606.14058
3. CausalDrive — arXiv:2606.15341
4. How Can Driving World Models Do Counterfactual Prediction? — arXiv:2608.11601
5. CRAFT — arXiv:2605.04470

### Historical controls

6. GameFormer — arXiv:2303.05760 / ICCV 2023
7. M2I — arXiv:2202.11884 / CVPR 2022
8. Bahram et al. 2016 — DOI 10.1109/TVT.2015.2508009

For each actual ingestion: allocate next stable Paper ID, acquire canonical PDF from venue/arXiv/official source, hash, front-page verify, MinerU-convert, QC raw MD + figures, update manifest, push text layer to this repo. If H3 has no lawful open PDF, record `PAYWALLED_NO_OPEN_SOURCE` rather than using an unofficial mirror.

Do not ingest the deferred set automatically.

## Phase 2 — GPT-5.6 Sol adversarial deep read

After raw MD is present, deep-read in scientific order:

```text
A4 Counterfactual Prediction
A2 ReactSim-Bench
A1 BridgeSim
A5 CRAFT
A3 CausalDrive
H3 Bahram 2016
H1 GameFormer
H2 M2I
```

For each paper answer:

- exact problem and scope;
- input → numerical representation → future representation → planner consumption;
- what receives direct supervision vs inferred/counterfactual supervision;
- evaluation regime;
- whether ego intervention is explicit;
- whether surrounding-agent response changes with intervention;
- whether state and candidate/action set are held fixed;
- whether factual-vs-reactive action ordering is actually compared;
- whether ordering reversal is directly measured;
- whether planning regret from that reversal is measured;
- strongest evidence supporting the paper;
- strongest limitation / alternative explanation;
- strongest evidence against P2-R;
- prior-art occupancy level;
- residual scientific question.

Use `AUTHOR CLAIM`, `DIRECT EXPERIMENTAL EVIDENCE`, `OUR INFERENCE` separately.

## Scientific question

For fixed current state `s` and fixed ego candidate/action set `A`, is there direct evidence that surrounding-agent response to alternative ego interventions changes ego-action ordering and causes non-trivial planning regret?

```text
rank_factual/nonreactive(A) ?= rank_reactive(A)
```

The causal chain must be:

```text
ego action
→ surrounding-agent response changes
→ candidate ordering reversal
→ planning regret
```

not merely generic OL/CL mismatch, observation shift, control error, temporal compounding, representation shift, or changed candidate coverage.

## Stop condition

After A1–A5 + H1–H3 are scientifically adjudicated, **stop corpus expansion** and issue one of:

```text
P2-R SURVIVES
P2-R KILLED
NONE / EVIDENCE INSUFFICIENT
```

Do not widen P2-R to protect it. Do not design a method yet. Do not force risk-field knowledge into the solution.
