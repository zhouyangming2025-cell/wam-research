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
- `landscape/CENSUS_PHASE_A_ROUND1.md`

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
| 2026-09-14 | Round 2 targeted ingest (historical subqueue; F7/F8/F11 branch of the field atlas) | 8 registered (P0013–P0020) | 7 `RAW_MD_READY` (canonical local PDF + raw MD, `DOCUMENT_VERIFIED`); P0020 Bahram 2016 blocked `PAYWALLED_NO_OPEN_SOURCE`; cards are skeletons, every scientific section `PENDING SCIENTIFIC REVIEW`; no gap or novelty verdict; report: `ROUND2_TARGETED_INGEST_REPORT.md` |

Important interpretation: Batch 0A is scientifically useful but **not representative of the whole field** because selection was partly hypothesis-driven.

## Scientific / methodology gates

| date | gate | material | result |
|---|---|---|---|
| 2026-09-13 | P2-R Targeted Failure Deep Read — Round 1 | SafeDrive, BeTop, GraphAD, RiskWorld, DA-WAM | no direct observed reaction-induced action-order inversion established; retained as historical audit |
| 2026-09-13 | Targeted Expansion Freeze | BridgeSim/ReactSim/CausalDrive/Counterfactual/CRAFT + GameFormer/M2I/Bahram | **SUPERSEDED AS ACTIVE PROGRAM** on 2026-09-14; retained as F7/F8/F11 subqueue |
| 2026-09-14 | Field-Reconstruction Reset | research methodology | gap-first search suspended; begin neutral planning-centric WAM census + anchor deep reads |
| 2026-09-14 | Phase-A Census Round 1 | broad cross-family placement from surveys + primary paper/project sources + existing repo evidence | ~45 unique works/benchmarks/controls provisionally placed across F1–F11; no gap verdict; Round 2 coverage holes identified |

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

## Phase-A Round-1 census facts

Round-1 record:

`landscape/CENSUS_PHASE_A_ROUND1.md`

Representative works now placed include:

```text
GAIA-1, DriveDreamer, Drive-WM, Vista, Epona, DrivingGPT, Policy World Model,
WorldDrive, OccWorld, Drive-OccWorld, WoTE, World4Drive, DriveWorld, LAW,
DriveLaW, Drive-JEPA, WorldRFT, Auto-JEPA, ReWorld, WA-JEPA, DA-WAM,
M2I, GameFormer, What Truly Matters, BeTop, GraphAD, SLEDGE, NAVSIM,
Bench2Drive, HUGSIM, DriveArena, BridgeSim, ReactSim-Bench, CausalDrive,
CRAFT, SafeDrive, Gen-Drive, DriveReward, RiskWorld, NPPC, TOAD/DrivoR,
UniAD, VAD, DiffusionDrive
```

Current provisional anchor pool is ~25 works; it is **not final** and should be reduced only after Round 2 fills missing coverage.

Round-2 holes:

- Hydra-MDP / DriveSuprim / iPad / VLA controls;
- Think2Drive / WM-RL lineage;
- ViDAR / GenAD representation-pretraining bridges where planning-relevant;
- benchmark evolution and deployment properties;
- uncertainty / multimodality treatment;
- any credible real-vehicle closed-loop evidence.

## Existing interactive/reactive subqueue

See `state/TARGETED_READING_QUEUE.md`.

It contains:

- BridgeSim
- ReactSim-Bench
- CausalDrive
- How Can Driving World Models Do Counterfactual Prediction?
- CRAFT
- GameFormer
- M2I
- Bahram et al. 2016

These papers now populate F7/F8/F11 rather than define the whole agenda.

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
