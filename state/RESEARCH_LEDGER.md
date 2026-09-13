# RESEARCH_LEDGER

Running factual ledger of assets, research-state transitions and scientific gates.

## Current research stage

```text
FIELD RECONSTRUCTION — Planning-centric WAM Atlas
```

Canonical documents:

- `landscape/FIELD_RECONSTRUCTION_PLAN.md`
- `landscape/PLANNING_WAM_TAXONOMY.md`
- `landscape/FIELD_ATLAS.md`

## Hypotheses

| hypothesis | status | role | file |
|---|---|---|---|
| P1_RETIRED — Planner-Induced Model Exploitation / Search-Support Gap | RETIRED | historical hypothesis / robustness evidence | `hypotheses/P1_RETIRED.md` |
| P2R_PRIMARY — Reactive Action-Ordering Gap | PARKED PROBE | one diagnostic lens inside broader field reconstruction; not active target | `hypotheses/P2R_PRIMARY.md` |
| P3_HOLD — Decision Sufficiency of World Representations | PARKED BACKUP PROBE | possible later synthesis question | `hypotheses/P3_HOLD.md` |

## Research scope rule

```text
World Model + End-to-End + Planning-centric
```

Risk / predictive risk field is optional prior knowledge, not a required destination.

As of 2026-09-14, **field understanding precedes gap hunting**. Canonical rules: `state/RESEARCH_PRINCIPLES.md`.

## Corpus

| date | batch | papers | state |
|---|---|---|---|
| 2026-09-13 | Batch 0A | 12 registered (P0001–P0012) | 11 `RAW_MD_READY` (canonical local PDF + raw MD, DOCUMENT_VERIFIED); P0008 NPPC blocked `PAYWALLED_NO_OPEN_SOURCE` |

Important interpretation: Batch 0A is scientifically useful but **not representative of the whole field** because selection was partly hypothesis-driven.

## Scientific / methodology gates

| date | gate | material | result |
|---|---|---|---|
| 2026-09-13 | P2-R Targeted Failure Deep Read — Round 1 | SafeDrive, BeTop, GraphAD, RiskWorld, DA-WAM | no direct observed reaction-induced action-order inversion established; retained as historical audit |
| 2026-09-13 | Targeted Expansion Freeze | BridgeSim/ReactSim/CausalDrive/Counterfactual/CRAFT + GameFormer/M2I/Bahram | **SUPERSEDED AS ACTIVE PROGRAM** on 2026-09-14; retained as F7/F8/F11 subqueue |
| 2026-09-14 | Field-Reconstruction Reset | research methodology | gap-first search suspended; begin neutral planning-centric WAM census + anchor deep reads |

## Field reconstruction targets

```text
Phase A: ~50–80 paper census at placement/overview depth
Phase B: ~15–25 representative anchor deep reads
Phase C: historical + architectural + supervision + evaluation + trade-off/counterexample synthesis
Phase D: only then reopen research-problem discovery
```

Provisional field families:

```text
F1  visual/video generative driving world models
F2  BEV / occupancy / geometric predictive world models
F3  latent / JEPA / predictive-representation world models
F4  world-model-assisted direct end-to-end planning
F5  candidate-conditioned / action-conditioned future evaluation
F6  unified world-action / trajectory-and-world generation
F7  interactive prediction + planning predecessors
F8  reactive world simulation / closed-loop policy training
F9  reward / value / safety / cost interfaces
F10 strong end-to-end planners without explicit world models
F11 evaluation / benchmark / simulator papers
```

## Existing interactive/reactive subqueue

See `state/TARGETED_READING_QUEUE.md`.

It currently contains:

- BridgeSim
- ReactSim-Bench
- CausalDrive
- How Can Driving World Models Do Counterfactual Prediction?
- CRAFT
- GameFormer
- M2I
- Bahram et al. 2016

No Paper IDs have been assigned to these entries yet unless later ingestion updates the manifest.

## Existing cross-session evidence

- `evidence/CORE_EVIDENCE_SNAPSHOT.md`
- `evidence/LEGACY_EXPERTISE_ASSETS.md`
- `audits/literature/P2R_TARGETED_FAILURE_DEEP_READ_ROUND1.md`

Use them as prior evidence, not as a substitute for field reconstruction.

## Integration gates

| date | gate | status |
|---|---|---|
| 2026-09-13 | Integration Gate 0 | PASSED — private repo directly readable/writable by GPT-5.6 Sol |
| 2026-09-13 | New-session Bootstrap Hardening | PASSED structurally |
| 2026-09-14 | New-session Field-Reconstruction Update | state/start/handoff updated so fresh sessions should not default to P2-R |

## Known host quirks

| quirk | status |
|---|---|
| Windows native/.NET reads expose a +1024 framed representation while canonical Python corpus I/O reads logical document bytes | `KNOWN_HOST_QUIRK`; no further investigation planned |
| `tempfile.mkdtemp`/named-pipe/MinerU config issues on local host | worked around in corpus scripts |
| git schannel TLS broken on local host | local git HTTPS uses OpenSSL backend |

## Division of labor

- **GPT-5.6 Sol:** field census, primary-paper/survey research, anchor deep reads, cross-paper synthesis, atlas/taxonomy/cards/state updates.
- **Local corpus agent:** acquisition, MinerU conversion, metadata/QC, local PDF archival/extraction, source-code execution, datasets/checkpoints/experiments.
