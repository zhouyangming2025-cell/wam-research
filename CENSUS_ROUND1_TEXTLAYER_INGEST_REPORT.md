# Phase-A Census Round 1 — Local Text-Layer Batch Report

Status: **corpus acquisition record**. This document is not the census. It records what the
local corpus agent acquired and verified so that the works the owner already placed in
`landscape/CENSUS_PHASE_A_ROUND1.md` can be read locally, without repeating that
placement, adding a family label, or making any novelty or gap claim.

Batch label: `census1`. Companion ledgers:

```text
manifests/census_round1_acquisition_plan.json
manifests/census1_id_allocation.json
manifests/batch_census1_identity.json
manifests/batch_census1_download_results.json
manifests/batch_census1_frontpage_verification.json
manifests/batch_census1_rawmd_results.json
manifests/batch_census1_evidence.json
manifests/CORPUS_MANIFEST.csv
```

---

## 1. Why this batch exists

The Round-1 census places roughly 45 works, but only 20 of them existed locally. Reading
the rest meant fetching public PDFs mid-analysis, which makes every later claim depend on
the network and on whatever the publisher served that day. The owner chose to close that
gap, so this batch gives the remaining Round-1 works the same treatment the corpus already
gives its other records: a verified identity, one canonical PDF with a logical-byte hash, a
front-page check, and an extractable raw markdown text layer with images.

Boundary: acquisition, identity verification, conversion, metadata and QC only. No family
assignment, no placement confidence and no novelty verdict is made here; the owner's
landscape, atlas, taxonomy and state files were not edited.

## 2. What was ingested

| paper_id | short | official title | source | pages | raw md chars |
|---|---|---|---|---:|---:|
| P0035 | GAIA1 | GAIA-1: A Generative World Model for Autonomous Driving | arXiv_v1 | 25 | 73066 |
| P0036 | DriveDreamer | DriveDreamer: Towards Real-world-driven World Models for Autonomous Dri... | arXiv_v2 | 15 | 61812 |
| P0037 | DriveWM | Driving into the Future: Multiview Visual Forecasting and Planning with... | CVPR2024_camera_ready | 11 | 53322 |
| P0038 | Vista | Vista: A Generalizable Driving World Model with High Fidelity and Versa... | arXiv_v5 | 31 | 102786 |
| P0039 | DriveDreamer2 | DriveDreamer-2: LLM-Enhanced World Models for Diverse Driving Video Gen... | arXiv_v2 | 24 | 60354 |
| P0040 | DrivingGPT | DrivingGPT: Unifying Driving World Modeling and Planning with Multi-mod... | ICCV2025_camera_ready | 11 | 54571 |
| P0041 | PolicyWM | From Forecasting to Planning: Policy World Model for Collaborative Stat... | arXiv_v2 | 20 | 69593 |
| P0042 | WorldDrive | Bridging Scene Generation and Planning: Driving with World Model via Un... | arXiv_v1 | 16 | 66254 |
| P0043 | OccWorld | OccWorld: Learning a 3D Occupancy World Model for Autonomous Driving | arXiv_v1 | 11 | 57359 |
| P0044 | DriveOccWorld | Driving in the Occupancy World: Vision-Centric 4D Occupancy Forecasting... | arXiv_v3 | 18 | 87400 |
| P0045 | WoTE | End-to-End Driving with Online Trajectory Evaluation via BEV World Model | ICCV2025_camera_ready | 10 | 53006 |
| P0046 | World4Drive | World4Drive: End-to-End Autonomous Driving via Intention-aware Physical... | ICCV2025_camera_ready | 11 | 51081 |
| P0047 | DriveWorld | DriveWorld: 4D Pre-trained Scene Understanding via World Models for Aut... | CVPR2024_camera_ready | 12 | 63648 |
| P0048 | LAW | Enhancing End-to-End Autonomous Driving with Latent World Model | arXiv_v2 | 18 | 58787 |
| P0049 | DriveJEPA | Drive-JEPA: Video JEPA Meets Multimodal Trajectory Distillation for End... | arXiv_v2 | 21 | 81841 |
| P0050 | WorldRFT | WorldRFT: Latent World Model Planning with Reinforcement Fine-Tuning fo... | arXiv_v1 | 15 | 73734 |
| P0051 | AutoJEPA | Auto-JEPA: A Latent World Model of Continuous Intent for End-to-End Aut... | arXiv_v1 | 12 | 62825 |
| P0052 | ReWorld | ReWorld: Representation Learning for World Action Models | arXiv_v2 | 15 | 83432 |
| P0053 | WAJEPA | WA-JEPA: Rethinking the Video JEPA Paradigm for World-Action Modeling i... | arXiv_v2 | 14 | 70274 |
| P0054 | WhatTrulyMatters | What Truly Matters in Trajectory Prediction for Autonomous Driving? | NeurIPS2023_camera_ready | 13 | 53244 |
| P0055 | SLEDGE | SLEDGE: Synthesizing Driving Environments with Generative Models and Ru... | arXiv_v2 | 18 | 53064 |
| P0056 | DriveArena | DriveArena: A Closed-loop Generative Simulation Platform for Autonomous... | arXiv_v1 | 19 | 73497 |
| P0057 | UniAD | Planning-Oriented Autonomous Driving | CVPR2023_camera_ready | 10 | 59418 |
| P0058 | VAD | VAD: Vectorized Scene Representation for Efficient Autonomous Driving | ICCV2023_camera_ready | 11 | 52017 |
| P0059 | DiffusionDrive | DiffusionDrive: Truncated Diffusion Model for End-to-End Autonomous Dri... | CVPR2025_camera_ready | 11 | 53783 |
| P0060 | DrivoR | Driving on Registers | CVPR2026_camera_ready | 12 | 55801 |

Total: **26 works**, P0035–P0060. Full 64-character hashes and canonical URLs
are in `manifests/batch_census1_download_results.json` and `manifests/CORPUS_MANIFEST.csv`.

## 3. How the set was chosen, mechanically

No work was selected from memory or from a search engine result:

1. `scripts/parse_census_works.py` parsed the owner's census table rows and the Round-1 source
   register, mechanically, and subtracted the works the corpus already holds;
2. `scripts/plan_census_acquisition.py` then chose one canonical source per remaining work in
   the corpus priority order — venue camera-ready, then official arXiv, then project-hosted —
   deriving CVF camera-ready PDFs from the paper pages, and extracting the PDF link from
   NeurIPS/ICLR pages;
3. every candidate URL was probed for a real `%PDF-` body before any download was attempted.

Source mix: NeurIPS_camera_ready=1, VF_camera_ready=9, arXiv=16.

## 4. Works whose register entry carried no document link

Five works were registered only by a project page, a repository or a publisher landing page.
A project page is not a document, so each was resolved through a discovery step and then
verified independently — the discovery page is never the evidence:

- **P0037 Drive-WM**: the CVPR 2024 Open Access index was scanned for the census title and the
  camera-ready page's own `citation_title` was checked before its PDF was used;
- **P0044 Drive-OccWorld**, **P0056 DriveArena**, **P0055 SLEDGE**: an arXiv link was found on
  the work's own project page or repository, and the official arXiv record was then fetched and
  its `citation_title` compared with the census entry;
- **NPPC** stays unresolved: the register records no lawful open canonical source for it, the
  same reason its record P0008 has never had a PDF. Nothing about that changed here, and it was
  not replaced with a guessed link.

## 5. Identity verification

Each work's official landing page was fetched (`scripts/fetch_work_identity.py`) and its
`citation_title`, `citation_author`, `citation_date` and arXiv version recorded verbatim in
`manifests/batch_census1_identity.json`. A keyword test derived from the census entry had to be
satisfied by the official title; the result:

- matched on the first pass: 25 of 26
- **P0052 divergence**: the census records this work as “ReWorld: Learning Better Representations for World Action Models”, while the official record reads “ReWorld: Representation Learning for World Action Models”. Same work, different phrasing; the
  official title is what entered the corpus, and the census file was left untouched.

## 6. Acquisition result

- downloaded: **26 of 26**
- total logical bytes: 242,036,669
- one canonical PDF per work, hashed on logical bytes (Python is the hash authority; the
  known .NET/local-read offset quirk in this environment does not affect these values)
- duplicate work check: no arXiv id, DOI or official URL in this batch repeats an existing
  corpus record, and no identifier was reused or renumbered

## 7. Front-page verification

Page 1 of every stored PDF was read and compared with the officially recorded title and first
author:

- `DOCUMENT_VERIFIED`: 26
- first author found on page 1 for every record in this batch

## 8. Conversion and QC

MinerU ran locally through `scripts/run_mineru.py`. Conversion for this batch ran **serially**:
an earlier batch showed that concurrent conversion on this host can hit service-side 502s and,
before the write path was fixed, could make two processes race on the shared ledger.

- `RAW_MD_READY`: 26
- images copied: 261; images referenced but missing: 0
- replacement/mojibake characters across the batch: 0

## 9. Code availability, as printed by the papers themselves

`code_available=YES` is asserted only where the paper's own text prints a repository URL. A
project page is not a repository, and the absence of a printed URL is not evidence that no code
exists. What the extracted text actually shows:

- papers printing a repository URL: 16 of 26
  - P0037 DriveWM: `https://github.com/BraveGroup/Drive-WM` (line 9)
  - P0038 Vista: `https://github.com/OpenDriveLab/Vista` (line 7)
  - P0041 PolicyWM: `https://github.com/6550Zhao/Policy-World-Model` (line 7)
  - P0042 WorldDrive: `https://github.com/TabGuigui/WorldDrive` (line 7)
  - P0043 OccWorld: `https://github.com/wzzheng/OccWorld` (line 19)
  - P0046 World4Drive: `https://github.com/ucaszyp/World4Drive` (line 8)
  - P0048 LAW: `https://github.com/BraveGroup/LAW` (line 17)
  - P0049 DriveJEPA: `https://github.com/linhanwang/Drive-JEPA` (line 15)
  - P0050 WorldRFT: `https://github.com/pengxuanyang/WorldRFT` (line 11)
  - P0051 AutoJEPA: `https://github.com/NoctYang/Auto-JEPA` (line 11)
  - P0052 ReWorld: `https://github.com/xiaomi-research/ReWorld` (line 5)
  - P0053 WAJEPA: `https://github.com/AFARI-Research/WA-JEPA` (line 13)
  - P0055 SLEDGE: `https://github.com/autonomousvision/sledge` (line 5)
  - P0056 DriveArena: `https://github.com/PJLab-ADG/DriveArena` (line 19)
  - P0057 UniAD: `https://github.com/OpenDriveLab/UniAD` (line 5)
  - P0058 VAD: `https://github.com/hustvl/VAD` (line 13)
- papers printing a project page but no repository: P0036, P0039, P0040, P0044
- papers printing neither (recorded as UNKNOWN, not as “no code”): P0035, P0045, P0047, P0054, P0059, P0060

## 10. Tag provenance

Tags for these 26 records were assigned mechanically (`scripts/build_census1_meta.py`) by
counting the fixed corpus vocabulary in each work's own title and extracted text. They are
**not** taken from the census family labels, so a reader must not treat them as the owner's
placement. Every record in this batch carries `decision_relevance=LOW` and `GENERAL` hypothesis
tags, because the batch exists to make the census readable locally and makes no claim about
decision relevance; both are owner decision points.

## 11. What this batch does NOT claim

- no placement of any work into a family, no family label, no placement confidence;
- no novelty, gap or counterexample verdict, and no statement about which limitations were
  genuinely resolved in the field's history;
- no claim that a work does or does not use a world model beyond what its own text says;
- no deep reading: these are placement-depth text layers, and the manifest marks them `NO_CARD`;
- no edit to the owner's `landscape/` or `state/` files; the retired handoff area was not touched.

## 12. Reproduce

```powershell
$mp = 'D:\Program Files\Mineru\venv\Scripts\python.exe'
$env:CORPUS_BATCH = 'census1'
& $mp scripts\parse_census_works.py                     # census works vs source register
& $mp scripts\plan_census_acquisition.py               # canonical source per work
& $mp scripts\resolve_census_unresolved.py             # OpenAlex path (title-verified)
& $mp scripts\resolve_census_via_discovery.py          # discovery-page path (title-verified)
& $mp scripts\apply_census1_plan.py --allocate         # ids + landing pages
& $mp scripts\fetch_work_identity.py                   # official identity ledger
& $mp scripts\apply_census1_plan.py --wires            # SOURCES / EXPECT / PAPERS
& $mp scripts\fetch_canonical_pdfs.py                  # canonical PDFs + sha256
& $mp scripts\verify_frontpage.py                      # page-1 verification
& $mp scripts\build_raw_md.py P0035,...,P0060          # MinerU raw MD (run serially)
& $mp scripts\build_census1_meta.py --scan             # text evidence + tags
& $mp scripts\build_census1_meta.py --write-meta       # manifest metadata
& $mp scripts\build_manifest.py                        # CORPUS_MANIFEST.csv
& $mp scripts\build_census1_report.py                  # this report
```

## 13. Decision points for the owner

1. **NPPC**: still no lawful open canonical source; keep it documented as blocked, or supply a
   permitted copy.
2. **`decision_relevance=LOW` for the whole batch**: if some of these works are already
   decision-relevant anchors for you, say which and the corpus will record that as your
   judgement rather than the agent's.
3. **Tag vocabulary**: no vision-language/VLA tag exists, so VLA works carry the closest
   available terms; extending the vocabulary is a corpus decision.
4. **Census titles vs official titles**: where the census paraphrases a title (P0052 here), the
   corpus stores the official one. Tell me if you want the census phrasing recorded too.
