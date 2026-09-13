# Agent Prompt — Round 2 Targeted Corpus Ingestion

Copy this task into the local corpus agent. This is an **infrastructure task only**, not scientific analysis.

---

You are the corpus-librarian / local-source worker for `wam-research`.

Read first:

```text
START_HERE.md
state/CURRENT_STATE.md
state/NEXT_TASK.md
state/TARGETED_READING_QUEUE.md
state/RESEARCH_PRINCIPLES.md
01_CORPUS_MANIFEST_SCHEMA.md or the canonical schema copy in the repo
manifests/CORPUS_MANIFEST.csv
```

## Scope

Ingest **only** the frozen targeted reading set below. Do not broaden the search and do not perform scientific gap analysis.

### Core P2-R set

1. BridgeSim: Unveiling the OL-CL Gap in End-to-End Autonomous Driving — arXiv:2604.10856
2. ReactSim-Bench: Benchmarking Reactive Behavior World Model Simulation in Autonomous Driving — arXiv:2606.14058
3. CausalDrive: Real-time Causal World Models for Autonomous Driving — arXiv:2606.15341
4. How Can Driving World Models Do Counterfactual Prediction? — arXiv:2608.11601
5. CRAFT: Counterfactual-to-Interactive Reinforcement Fine-Tuning for Driving Policies — arXiv:2605.04470

### Historical novelty controls

6. GameFormer: Game-theoretic Modeling and Learning of Transformer-based Interactive Prediction and Planning for Autonomous Driving — arXiv:2303.05760 / ICCV 2023
7. M2I: From Factored Marginal Trajectory Prediction to Interactive Prediction — arXiv:2202.11884 / CVPR 2022
8. A Game-Theoretic Approach to Replanning-Aware Interactive Scene Prediction and Planning — Mohammad Bahram et al., IEEE TVT 2016, DOI 10.1109/TVT.2015.2508009

## ID policy

Read the live manifest first and allocate the next unused stable Paper IDs in the exact list order above. Never recycle or renumber an existing ID.

If the current highest ID is still P0012, the expected allocation is P0013–P0020, but verify rather than assume.

A selected paper may retain its allocated ID even if acquisition is lawfully blocked; record the failure honestly.

## Source priority

```text
published venue camera-ready
> official arXiv version
> official project-hosted PDF
```

For arXiv-only 2026 papers, use official arXiv PDF as canonical unless a verified venue camera-ready exists.

For GameFormer and M2I, prefer CVF camera-ready PDFs if reachable.

For Bahram et al. 2016, do not use unofficial mirrors. If no lawful open full text is available, record:

```text
DOWNLOAD_BLOCKED: PAYWALLED_NO_OPEN_SOURCE
```

and keep metadata/evidence level appropriately limited.

## Known official discovery sources

```text
BridgeSim
  https://arxiv.org/abs/2604.10856
  https://github.com/VAIL-UCLA/BridgeSim

ReactSim-Bench
  https://arxiv.org/abs/2606.14058
  https://github.com/Thinklab-SJTU/ReactSim-Bench

CausalDrive
  https://arxiv.org/abs/2606.15341

Counterfactual Prediction
  https://arxiv.org/abs/2608.11601

CRAFT
  https://arxiv.org/abs/2605.04470
  https://github.com/CurryChen77/CraftPolicy

GameFormer
  https://arxiv.org/abs/2303.05760
  CVF ICCV 2023 official paper page preferred

M2I
  https://arxiv.org/abs/2202.11884
  CVF CVPR 2022 official paper page preferred

Bahram et al. 2016
  DOI 10.1109/TVT.2015.2508009
```

Treat these as discovery hints, not substitutes for source verification.

## Pipeline

For every successfully acquired paper:

```text
identity resolution
→ deduplication against live manifest
→ stable ID allocation
→ canonical PDF acquisition
→ logical-byte SHA256
→ front-page title / first-author verification
→ MinerU raw Markdown conversion
→ raw-MD QC + image-reference QC
→ raw_md_sha256
→ manifest update
→ GitHub text-layer staging/push
```

Use the existing proven Python/OpenSSL downloader and MinerU wrapper; respect the known host shims documented in the repo. Do not re-investigate the Windows +1024 native/.NET framing issue.

## Raw MD layout

```text
papers/raw_md/PXXXX_ShortName/
  PXXXX_ShortName.raw.md
  images/
```

Do not edit raw MD to "improve" scientific content. PDF remains exact source authority.

## Paper Card creation

Create one card skeleton per ingested paper under:

```text
papers/cards/PXXXX_ShortName.md
```

Fill only:

- metadata;
- source locations;
- evidence level;
- ingestion/QC facts;
- official code source if genuinely verified.

Leave scientific sections as:

```text
PENDING SCIENTIFIC REVIEW
```

Do not infer:

- observed failure verdict;
- hypothesis impact;
- prior-art occupancy;
- research verdict.

Those are GPT-5.6 Sol tasks.

## Official code

Only set `code_available=YES` when officiality is directly supported by the paper/project/author source. Repository-name pattern matching is not evidence.

Do not clone source repositories in this ingestion pass unless required to verify identity or explicitly requested later.

## GitHub write-back

Push text-layer artifacts only:

```text
raw MD + images
manifest updates
paper-card skeletons
ingestion report
```

Never push PDFs, checkpoints, datasets, or MinerU quarantine artifacts.

## Required report

Create:

```text
ROUND2_TARGETED_INGEST_REPORT.md
```

with:

1. ID allocation table
2. canonical source + source_version
3. PDF hash / raw-MD hash
4. front-page verification result
5. raw-MD QC result
6. official code status + evidence basis
7. download/conversion failures
8. provenance conflicts
9. exact list of GitHub files added/updated

## Stop condition

Stop when all eight selected records have either:

```text
RAW_MD_READY
```

or a specific lawful acquisition blocker recorded.

Do not start scientific deep reading. Do not ingest deferred papers. Do not start method design. Do not re-open P1 engineering. Do not introduce risk-field ideas.
