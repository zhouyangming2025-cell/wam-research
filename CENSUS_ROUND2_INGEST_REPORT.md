# Phase-A Census Round 2 — Corpus Ingest Report

Status: **corpus ingestion record**. This document is *not* the census and contains no
field-placement, novelty or gap verdict. It records what the local corpus agent acquired,
converted and verified in support of the coverage holes named for Phase-A Census Round 2.

Batch label: `census2`. Companion ledgers:

```text
manifests/batch_census2_identity.json
manifests/batch_census2_download_results.json
manifests/batch_census2_frontpage_verification.json
manifests/batch_census2_rawmd_results.json
manifests/CORPUS_MANIFEST.csv
```

---

## 1. Why this batch exists

`landscape/FIELD_RECONSTRUCTION_PLAN.md` replaces gap-first search with neutral field
reconstruction, and `state/NEXT_TASK.md` asks Round 2 to fill missing *coverage* rather
than to hunt for gaps. `landscape/FIELD_ATLAS.md` names the missing pieces explicitly:
strong non-WM end-to-end controls (F10), world-model RL lineage, representation-pretraining
bridges, and the benchmark/simulator lineage. This batch supplies those works as local
documents with an extractable text layer, so census placement no longer depends on fetching
public PDFs mid-analysis.

Boundary of this batch: acquisition, identity verification, conversion, metadata and QC only.
No family assignment, no placement confidence, no novelty or gap claim is made here — those
belong to the census owner. The owner's landscape/atlas/taxonomy/state files were not edited.

## 2. Coverage holes filled

| paper_id | short name | coverage hole from the owner's atlas / next task |
|---|---|---|
| P0021 | HydraMDP | F10 strong non-WM end-to-end control (Hydra-MDP family) |
| P0022 | DriveSuprim | F10 strong non-WM end-to-end control |
| P0023 | iPad | F10 strong non-WM end-to-end control |
| P0024 | DriveVLM | F10 representative VLA planner |
| P0025 | OmniDrive | F10 representative VLA planner |
| P0026 | ORION | F10 representative VLA planner |
| P0027 | Think2Drive | world-model RL lineage |
| P0028 | ViDAR | representation-pretraining bridge |
| P0029 | GenAD | representation-pretraining bridge |
| P0030 | nuScenes | benchmark / evaluation lineage |
| P0031 | nuPlan | benchmark / evaluation lineage |
| P0032 | NAVSIM | benchmark / evaluation lineage |
| P0033 | Bench2Drive | benchmark / evaluation lineage |
| P0034 | HUGSIM | benchmark / evaluation lineage |

## 3. Identity resolution and dedup

Identity is the first pipeline step, and web search was unavailable in this session, so no
title, author, year or identifier in this batch was written from memory:

1. candidates were resolved through the OpenAlex API (`scripts/resolve_works_openalex.py`);
2. each candidate's **official landing page** was then fetched and its `citation_title`,
   `citation_author`, `citation_date` and arXiv version recorded verbatim by
   `scripts/fetch_work_identity.py`;
3. an identity was accepted only when the recorded official title matched the intended work;
4. page 1 of each downloaded PDF was re-checked against that recorded title (§5).

Dedup: all 20 pre-existing corpus records were listed first (`arxiv_id`, title). None of the
14 works below already existed, and no identifier was reused or renumbered; `P0021`–`P0034`
are allocated in the order the owner's coverage list groups them.

## 4. Acquisition results

| paper_id | short | source_version | bytes | pdf sha256 (logical bytes) | front page |
|---|---|---|---|---|---|
| P0021 | HydraMDP | arXiv_v4 | 1596072 | `8927b0ffbfb0d9d5…` | DOCUMENT_VERIFIED |
| P0022 | DriveSuprim | arXiv_v3 | 28120013 | `33cf828e4a5cb7e9…` | DOCUMENT_VERIFIED |
| P0023 | iPad | arXiv_v1 | 17467751 | `0ed2da26ea19224a…` | DOCUMENT_VERIFIED |
| P0024 | DriveVLM | arXiv_v5 | 9180928 | `cac938d314337c84…` | DOCUMENT_VERIFIED |
| P0025 | OmniDrive | CVPR2025_camera_ready | 1862726 | `4a4f24a1192ecdaf…` | DOCUMENT_VERIFIED |
| P0026 | ORION | ICCV2025_camera_ready | 1161821 | `77d261a2dcfaaba2…` | DOCUMENT_VERIFIED |
| P0027 | Think2Drive | arXiv_v2 | 4053167 | `8ad50c498512580b…` | DOCUMENT_VERIFIED |
| P0028 | ViDAR | CVPR2024_camera_ready | 4913394 | `8160000193aeed74…` | DOCUMENT_VERIFIED |
| P0029 | GenAD | arXiv_v3 | 27391543 | `a12f2865bd6a6a81…` | DOCUMENT_VERIFIED |
| P0030 | nuScenes | CVPR2020_camera_ready | 1744945 | `4a2822800db7e570…` | DOCUMENT_VERIFIED |
| P0031 | nuPlan | arXiv_v4 | 153984 | `86de4fad72fa27d1…` | DOCUMENT_VERIFIED |
| P0032 | NAVSIM | arXiv_v2 | 3505835 | `d3bc66d321cfcecc…` | DOCUMENT_VERIFIED |
| P0033 | Bench2Drive | arXiv_v3 | 7789861 | `c4b3514da643b7e5…` | DOCUMENT_VERIFIED |
| P0034 | HUGSIM | arXiv_v1 | 50128067 | `7b8534cb59af740b…` | DOCUMENT_VERIFIED |

Full 64-character hashes and canonical URLs are in the batch ledger and in
`manifests/CORPUS_MANIFEST.csv`; they are not retyped here.

## 5. Front-page verification

Each downloaded PDF was opened with pypdfium2 and page 1 text compared against the
officially recorded title (whitespace/punctuation-insensitive) plus presence of the recorded
first author. Exact counts:

- `DOCUMENT_VERIFIED`: 14 of 14

## 6. Raw MD conversion and QC

MinerU conversion ran locally through `scripts/run_mineru.py` with the harness shims.

| paper_id | qc | pages | raw md chars | headings | images (md/disk) |
|---|---|---|---|---|---|
| P0021 | RAW_MD_READY | 5 | 25109 | 16 | 2/2 |
| P0022 | RAW_MD_READY | 12 | 62503 | 26 | 6/6 |
| P0023 | RAW_MD_READY | 25 | 79719 | 49 | 16/16 |
| P0024 | RAW_MD_READY | 30 | 98651 | 30 | 98/98 |
| P0025 | RAW_MD_READY | 11 | 48603 | 25 | 4/4 |
| P0026 | RAW_MD_READY | 12 | 60126 | 21 | 5/5 |
| P0027 | RAW_MD_READY | 24 | 66883 | 55 | 40/40 |
| P0028 | RAW_MD_READY | 12 | 63320 | 14 | 6/6 |
| P0029 | RAW_MD_READY | 10 | 52715 | 16 | 5/5 |
| P0030 | RAW_MD_READY | 11 | 65112 | 14 | 7/7 |
| P0031 | RAW_MD_READY | 5 | 23084 | 12 | 1/1 |
| P0032 | RAW_MD_READY | 14 | 57561 | 12 | 13/13 |
| P0033 | RAW_MD_READY | 26 | 83466 | 60 | 50/50 |
| P0034 | RAW_MD_READY | 24 | 135771 | 45 | 47/47 |

Two integrity facts from this batch are recorded here rather than smoothed over:

1. **Ledger write race, repaired from artifacts.** Conversion for this batch was started as
   two concurrent jobs. Each process read the shared ledger once at start and wrote it back at
   the end, so the later write silently dropped six records. The raw MD files and their images
   were never affected. The missing records were reconstructed from the stored artifacts by
   `scripts/repair_rawmd_ledger.py`, which calls the same `qc()` function that produced the
   originals and reproduces their figures exactly (for example P0033 83466 chars / 60
   headings / 50-50 images). `build_raw_md.py` now re-reads the ledger immediately before
   writing, so a concurrent run can no longer clobber another run's records.
2. **One conversion text loss.** For P0028 the repository URL printed on PDF page 1 is absent
   from the extracted markdown, so that record's `code_available` rests on the PDF page-1 read
   and not on the markdown. Anyone reading only the markdown of that paper would wrongly
   conclude that it prints no code URL. The manifest note states this explicitly.

## 7. Canonical-source decisions

The corpus priority is venue camera-ready > official arXiv > project-hosted. Every decision
below is the `basis` string recorded at download time, quoted from the ledger:

- **P0021** (arXiv_v4): official arXiv version v4 (arXiv abs page citation_title matches exactly); no venue camera-ready verified in this batch
- **P0022** (arXiv_v3): official arXiv version v3. An AAAI 2026 version exists (DOI 10.1609/aaai.v40i14.38178, seen in OpenAlex), but the AAAI OJS article page returned no galley PDF link in this batch, so it could not be verified and the arXiv version stays canonical
- **P0023** (arXiv_v1): official arXiv version v1; the IEEE Robotics and Automation Letters version (DOI 10.1109/lra.2026.3723334) is not open, so the preprint is canonical
- **P0024** (arXiv_v5): official arXiv version v5 (arXiv abs page citation_title matches exactly)
- **P0025** (CVPR2025_camera_ready): venue camera-ready (CVF Open Access). arXiv:2405.01533 v2 carries the same title on its official abs page, so the CVPR 2025 camera-ready supersedes the preprint per corpus canonical-source priority
- **P0026** (ICCV2025_camera_ready): venue camera-ready (CVF Open Access); located by scanning the ICCV2025 Open Access index page, because CVF truncates titles inside slugs and full-title guesses return 404
- **P0027** (arXiv_v2): official arXiv version v2; the ECCV 2024 Springer version is not open, so the preprint is canonical
- **P0028** (CVPR2024_camera_ready): venue camera-ready (CVF Open Access). NOTE: the camera-ready title is Visual Point Cloud Forecasting enables Scalable Autonomous Driving and does not contain the method name ViDAR used by the census; located by scanning the CVPR2024 Open Access index page
- **P0029** (arXiv_v3): official arXiv version v3; the ECCV 2024 Springer version is not open, so the preprint is canonical
- **P0030** (CVPR2020_camera_ready): venue camera-ready (CVF Open Access). CVPR 2020 uses the older CVF path layout (/content_CVPR_2020/), so the modern (CVPR20xx?day=all) index does not list it; the URL was verified as HTTP 206 with %PDF- magic before download
- **P0031** (arXiv_v4): official arXiv version v4, titled NuPlan: A closed-loop ML-based planning benchmark for autonomous vehicles. The Round-1 source register listed only the project page https://nuplan.org/nuplan, which is not a document; a peer-reviewed nuPlan paper is known to exist but was NOT verified in this batch, so the canonical preprint is used and this remains an open census item
- **P0032** (arXiv_v2): official arXiv version v2 (title and version confirmed twice: arXiv export API and the arXiv abs page). The NeurIPS 2024 Datasets and Benchmarks abstract page listed in the Round-1 source register was not fetched for a camera-ready in this batch
- **P0033** (arXiv_v3): official arXiv version v3 (arXiv abs page citation_title matches exactly). A NeurIPS 2024 Datasets and Benchmarks version indexed under DOI 10.52202/079017-0025 was seen in OpenAlex, but no open PDF for it was verified in this batch
- **P0034** (arXiv_v1): official arXiv version v1. The IEEE TPAMI version (DOI 10.1109/tpami.2025.3647952, listed in the Round-1 source register and seen in OpenAlex) is not open, so the preprint is canonical

## 8. Unresolved and blocked items

- **Hydra-MDP++** and **NAVSIM-v2** were named by the owner's coverage list but could NOT
  be verified in this session (no matching official record was found through OpenAlex, and the
  arXiv export API was rate-limiting). They are deliberately NOT ingested: a guessed
  identifier would have put an unverified document into the corpus. They remain an open
  Round-2 item and need an owner-supplied canonical link or title.
- **nuPlan**: the Round-1 source register lists only the project page. The canonical document
  stored here is the official arXiv version; a peer-reviewed nuPlan paper is known to exist but
  was not verified in this batch, so the record keeps that caveat.
- **OmniDrive**: the CVPR 2025 camera-ready and arXiv:2405.01533 v2 carry the same title, so
  they are one work; the camera-ready is canonical. If the census intended a *different*
  OmniDrive paper (an LLM-agent framework variant), that is a separate record to be identified.
- **Legacy**: P0008 NPPC still has no lawful open canonical source; nothing about that changed.

## 9. What this batch does NOT claim

- no placement of any work into F1–F11, no family label, no placement confidence;
- no novelty, gap, or counterexample verdict;
- no statement that a work uses or does not use a world model beyond what its own text says;
- `code_available` is `YES` only where the paper itself prints a repository URL; a project
  page is not a repository, and absence of a printed URL is not evidence that no code exists;
- no paper was read at deep-read depth; these records are placement-depth documents.

## 10. Reproduce

```powershell
$mp = 'D:\Program Files\Mineru\venv\Scripts\python.exe'
$env:CORPUS_BATCH = 'census2'
& $mp scripts\fetch_work_identity.py                 # official identity metadata
& $mp scripts\fetch_canonical_pdfs.py                # canonical PDFs + logical-byte SHA256
& $mp scripts\verify_frontpage.py                    # page-1 title/author verification
& $mp scripts\build_raw_md.py P0021,P0022,...,P0034  # MinerU raw MD
& $mp scripts\build_manifest.py                      # CORPUS_MANIFEST.csv
& $mp scripts\build_census2_report.py                # this report
```

## 11. Decision points for the owner

1. **Hydra-MDP++ / NAVSIM-v2**: supply canonical titles or links so they can be ingested, or
   drop them from the Round-2 hole list.
2. **Tags and relevance**: census-depth records are tagged from their own text and carry
   `decision_relevance=LOW` with `GENERAL` hypothesis tags, because P1/P2-R/P3 are parked.
   Say if you want a different convention for breadth records.
3. **Paper-card layer (retired)**: these records deliberately have no paper cards, so their
   manifest rows carry a `NO_CARD` note. Current scientific synthesis uses deep analyses and
   source audits; the legacy manifest field is retained only for provenance.
4. **Anchor pool**: if you freeze the 15–25 anchor works, the same pipeline can give the whole
   anchor set a local text layer before Phase B deep reads begin.
