# RESEARCH_LEDGER

Running factual ledger of assets, research-state transitions and scientific gates.

## Hypotheses

| hypothesis | status | definition | file |
|---|---|---|---|
| P1_RETIRED — Planner-Induced Model Exploitation / Search-Support Gap | RETIRED AS MAIN PROBLEM | prior formulation retained for provenance | `hypotheses/P1_RETIRED.md` |
| P2R_PRIMARY — Reactive Action-Ordering Gap in Planning-centric WAMs | PRIMARY CANDIDATE, NOT CONFIRMED GAP | fixed-state / fixed-candidate factual-vs-reactive action-ordering question | `hypotheses/P2R_PRIMARY.md` |
| P3_HOLD — Decision Sufficiency of World Representations | HOLD AS BACKUP | what future distinctions must be preserved to preserve action preference | `hypotheses/P3_HOLD.md` |

## Research scope rule

```text
World Model + End-to-End + Planning-centric
```

Risk / predictive risk field is an optional knowledge asset, not a required destination. Scientific process is problem-first; every paper is reviewed symmetrically for strengths, limitations, evidence and counterevidence. Canonical rules: `state/RESEARCH_PRINCIPLES.md`.

## Corpus

| date | batch | papers | state |
|---|---|---|---|
| 2026-09-13 | Batch 0A | 12 registered (P0001–P0012) | 11 `RAW_MD_READY` (canonical local PDF + raw MD, DOCUMENT_VERIFIED); P0008 NPPC blocked `PAYWALLED_NO_OPEN_SOURCE`; reports: `BATCH_0A_METADATA_REPORT.md`, `BATCH_0A_INGEST_REPORT.md` |

## Scientific review gates

| date | gate | material | result |
|---|---|---|---|
| 2026-09-13 | P2-R Targeted Failure Deep Read — Round 1 | SafeDrive, BeTop, GraphAD, RiskWorld, DA-WAM | `P2-R SURVIVES ROUND 1 AS A QUESTION, NOT AS A CONFIRMED GAP`; no direct observed reaction-induced action-order inversion established |
| 2026-09-13 | Targeted Expansion Freeze | A1–A5 direct P2-R + H1–H3 historical controls | queue fixed; broad expansion paused until adjudication |

Round-1 audit:

`audits/literature/P2R_TARGETED_FAILURE_DEEP_READ_ROUND1.md`

### Broad formulations rejected as novelty after Round 1

```text
Planning should model interactions.
Reactive / closed-loop evaluation matters.
World models should be conditioned on ego actions.
Each candidate should receive its own predicted future.
Future information can improve candidate scoring.
```

### Strongest current nearest priors

- **DA-WAM:** candidate-specific future latent + candidate-specific scoring; offline observed-future supervision only for expert-matched candidate.
- **SafeDrive:** candidate-conditioned sparse worlds + fine-grained safety selection.
- **BeTop:** explicit future-interaction supervision + reactive closed-loop evaluation.

## Frozen targeted reading queue

Full queue and acquisition metadata:

`state/TARGETED_READING_QUEUE.md`

### A — direct P2-R attack set

| key | paper | discovery status |
|---|---|---|
| A1 | BridgeSim: Unveiling the OL-CL Gap in End-to-End Autonomous Driving | `DISCOVERED_NOT_INGESTED`, arXiv:2604.10856 |
| A2 | ReactSim-Bench: Benchmarking Reactive Behavior World Model Simulation in Autonomous Driving | `DISCOVERED_NOT_INGESTED`, arXiv:2606.14058 |
| A3 | CausalDrive: Real-time Causal World Models for Autonomous Driving | `DISCOVERED_NOT_INGESTED`, arXiv:2606.15341 |
| A4 | How Can Driving World Models Do Counterfactual Prediction? | `DISCOVERED_NOT_INGESTED`, arXiv:2608.11601 |
| A5 | CRAFT: Counterfactual-to-Interactive Reinforcement Fine-Tuning for Driving Policies | `DISCOVERED_NOT_INGESTED`, arXiv:2605.04470 |

### H — historical novelty controls

| key | paper | discovery status |
|---|---|---|
| H1 | GameFormer | `DISCOVERED_NOT_INGESTED`, arXiv:2303.05760 / ICCV 2023 |
| H2 | M2I | `DISCOVERED_NOT_INGESTED`, arXiv:2202.11884 / CVPR 2022 |
| H3 | Bahram et al., A Game-Theoretic Approach to Replanning-Aware Interactive Scene Prediction and Planning | `DISCOVERED_NOT_INGESTED`, DOI 10.1109/TVT.2015.2508009; open-copy status unresolved |

No Paper IDs have been assigned to A/H entries yet.

## Deferred, not authorized for automatic ingestion

```text
What Truly Matters
Policy World Model
BeyondDrive
ELF-VLA
WorldRFT / ReWorld / Auto-JEPA / WA-JEPA / Drive-JEPA
```

Activate only if a specific unresolved question survives the targeted gate.

## Other discovered, not ingested

| item | state |
|---|---|
| `论文\2602.06521v1.pdf` (DriveWorld-VLA) | `DISCOVERED_NOT_INGESTED`, target batch = Batch 1, no Paper ID; remains deferred while targeted gate is active |

## Integration gates

| date | gate | content | status |
|---|---|---|---|
| 2026-09-13 | Integration Gate 0 | Full corpus text layer: manifest + 11 raw MD + figures + scripts + logs + reports; initial cards; Research Brain state/hypotheses/handoff | **PASSED for GitHub access** — private repo is live and directly readable/writable by GPT-5.6 Sol through the GitHub connector |
| 2026-09-13 | New-session Bootstrap Hardening | `START_HERE.md` + principles + targeted queue + state/read-order cleanup | **PASSED structurally**; fresh-session behavioral test still recommended after next handoff |

## Known host quirks

| quirk | status |
|---|---|
| Windows native/.NET reads of workspace files expose a +1024 framed representation while the canonical Python corpus I/O path reads logical document bytes | `KNOWN_HOST_QUIRK`; content hashes use Python logical bytes; no further investigation planned |
| `tempfile.mkdtemp` directories become inaccessible/undeletable; named pipes denied; MinerU config depends on CWD | worked around in corpus scripts; MinerU installation unmodified |
| git schannel TLS broken on the local host | local git HTTPS operations require OpenSSL backend; not a blocker for GPT direct GitHub access |

## Division of labor

- **GPT-5.6 Sol:** scientific interpretation, cross-paper reasoning, adversarial review, hypothesis adjudication, research cards, audits, state/ledger/handoff updates.
- **Local corpus agent:** acquisition, MinerU conversion, metadata/QC, local PDF source extraction, source-code execution, datasets/checkpoints/experiments.
