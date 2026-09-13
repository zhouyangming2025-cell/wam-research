# RESEARCH_LEDGER

Running factual ledger of assets, research-state transitions and scientific gates.

## Hypotheses

| hypothesis | status | definition | file |
|---|---|---|---|
| P1_RETIRED — Planner-Induced Model Exploitation / Search-Support Gap | RETIRED AS MAIN PROBLEM | prior formulation retained for provenance | `hypotheses/P1_RETIRED.md` |
| P2R_PRIMARY — Reactive Action-Ordering Gap in Planning-centric WAMs | PRIMARY CANDIDATE, NOT CONFIRMED GAP | fixed-state / fixed-candidate factual-vs-reactive action-ordering question | `hypotheses/P2R_PRIMARY.md` |
| P3_HOLD — Decision Sufficiency of World Representations | HOLD AS BACKUP | what future distinctions must be preserved to preserve action preference | `hypotheses/P3_HOLD.md` |

## Corpus

| date | batch | papers | state |
|---|---|---|---|
| 2026-09-13 | Batch 0A | 12 registered (P0001–P0012) | 11 `RAW_MD_READY` (canonical local PDF + raw MD, DOCUMENT_VERIFIED); P0008 NPPC blocked `PAYWALLED_NO_OPEN_SOURCE`; reports: `BATCH_0A_METADATA_REPORT.md`, `BATCH_0A_INGEST_REPORT.md` |

## Scientific review gates

| date | gate | material | result |
|---|---|---|---|
| 2026-09-13 | P2-R Targeted Failure Deep Read — Round 1 | SafeDrive, BeTop, GraphAD, RiskWorld, DA-WAM | `P2-R SURVIVES ROUND 1 AS A QUESTION, NOT AS A CONFIRMED GAP`; no direct observed reaction-induced action-order inversion established |

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

## Next targeted literature gate

Direct set:

1. BridgeSim
2. ReactSim-Bench
3. CausalDrive
4. How Can Driving World Models Do Counterfactual Prediction?
5. CRAFT

Goal: determine whether the precise fixed-state / fixed-candidate reaction-induced ordering variable is already measured, solved, or unsupported.

## Discovered, not ingested

| item | state |
|---|---|
| `论文\2602.06521v1.pdf` (DriveWorld-VLA) | `DISCOVERED_NOT_INGESTED`, target batch = Batch 1, no Paper ID |

## Integration gates

| date | gate | content | status |
|---|---|---|---|
| 2026-09-13 | Integration Gate 0 | Full corpus text layer: manifest + 11 raw MD + figures + scripts + logs + reports; initial cards; Research Brain state/hypotheses/handoff | **PASSED for GitHub access** — private repo is live and directly readable/writable by GPT-5.6 Sol through the GitHub connector |

## Known host quirks

| quirk | status |
|---|---|
| Windows native/.NET reads of workspace files expose a +1024 framed representation while the canonical Python corpus I/O path reads the logical document bytes | `KNOWN_HOST_QUIRK`; content hashes use Python logical bytes; no further investigation planned |
| `tempfile.mkdtemp` directories become inaccessible/undeletable; named pipes denied; MinerU config depends on CWD | worked around in corpus scripts; MinerU installation unmodified |
| git schannel TLS broken on the local host | local git HTTPS operations require OpenSSL backend; not a blocker for GPT direct GitHub access |

## Division of labor

- **GPT-5.6 Sol:** scientific interpretation, cross-paper reasoning, adversarial review, hypothesis adjudication, research cards, state/ledger/handoff updates.
- **Local agent:** acquisition, MinerU conversion, metadata/QC, local PDF source extraction, source-code execution, datasets/checkpoints/experiments.
