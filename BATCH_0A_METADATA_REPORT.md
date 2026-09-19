# BATCH_0A_METADATA_REPORT

Status: **HISTORICAL INGEST PROVENANCE — the paper-card target mentioned below was never a
scientific evidence layer and is retired from the current tree.**

Scope: Batch 0A = Ledger entries 1–12 (Epona … DA-WAM).
Objective of this batch: metadata resolution + dedup + Paper ID allocation ONLY.
**No PDF was downloaded. No file was moved. No upstream asset was modified.**

Date: 2026-09-13
Agent role: research librarian / corpus engineer (no scientific verdicts issued).

---

## 1. Rulings applied (from user adjudication)

| Ruling | Applied |
|---|---|
| A1 per-paper raw_md subdir | `papers/raw_md/PXXXX_ShortName/{*.raw.md, images/}` adopted as target layout. Isolated staging dir created: `papers/quarantine/mineru_artifacts/`. `_origin.pdf` / `_layout.pdf` / `_span.pdf` / `content_list.json` are never canonical. |
| A2 Paper Cards in GitHub repo | Target `D:\zym_information\ZYM\wam\wam-research\papers\cards\PXXXX_ShortName.md`. **NOT CLONED — blocked, see §7.** No second cards tree was created under `research_assets` (complied). |
| A3 template rows | `P0001 EXAMPLE` row **removed**; P0001 = first real paper. `R0001 EXAMPLE` row **kept** — no repo registered yet (Step 10 not reached). |

Deliverables: `manifests/CORPUS_MANIFEST.csv` (12 real rows, structurally validated) and this report.
`CODE_REPO_MANIFEST.csv` untouched.

---

## 2. Resolved

11 of 12 entries have their identity and core bibliographic fields resolved.

| ID | Short name | Exact title | Year | Venue | First author | arXiv | DOI |
|---|---|---|---|---|---|---|---|
| P0001 | Epona | Epona: Autoregressive Diffusion World Model for Autonomous Driving | 2025 | ICCV 2025 | Kaiwen Zhang | 2506.24113 | 10.1109/ICCV.2025.02527 |
| P0003 | GraphAD | GraphAD: Interaction Scene Graph for End-to-end Autonomous Driving | 2024 | IJCAI 2024 | Yunpeng Zhang | 2403.19098 | 10.24963/ijcai.2024/270 |
| P0004 | BeTop | Reasoning Multi-Agent Behavioral Topology for Interactive Autonomous Driving | 2024 | NeurIPS 2024 | Haochen Liu | 2409.18031 | NONE |
| P0005 | RiskWorld | RiskWorld: Object-Centric Latent World Modeling for Autonomous Driving Risk Identification | 2026 | arXiv preprint | Jingzheng Li | 2608.21414 | NONE |
| P0006 | Gen-Drive | Gen-Drive: Enhancing Diffusion Generative Driving Policies with Reward Modeling and Reinforcement Learning Fine-Tuning | 2025 | ICRA 2025 | Zhiyu Huang | 2410.05582 | 10.1109/ICRA55743.2025.11127286 |
| P0007 | DriveReward | DriveReward: A Comprehensive Dataset and Generative Vision-Language Reward Model for Autonomous Driving | 2026 | arXiv preprint | Qimao Chen | 2606.08525 | NONE |
| P0008 | NPPC | NPPC: Neural Parametric Planning Cost for End-to-End Autonomous Driving | 2026 | IEEE RA-L 2026 | Abi Rahman Syamil | **NONE** (no arXiv version) | 10.1109/LRA.2026.3663819 |
| P0009 | DriveLaW | DriveLaW: Unifying Planning and Video Generation in a Latent Driving World | 2026 | CVPR 2026 | Tianze Xia | 2512.23421 | NONE |
| P0010 | TOAD | Test-Time Trajectory Optimization for Autonomous Driving | 2026 | arXiv preprint | Yihong Xu | 2606.07170 | NONE |
| P0011 | Sensitivity Shaping | Sensitivity Shaping for Latent Modeling | 2026 | arXiv preprint (venue unresolved) | Hongzhan Yu | 2606.14585 | NONE |
| P0012 | DA-WAM | DA-WAM: Decision-Aligned Future Latents for Driving World Models | 2026 | arXiv preprint | Ruiguo Zhong | 2608.19085 | NONE |

### Evidence grade — read this before trusting §2

**No PDF was read and no publisher byline was inspected.** Author/title/year/DOI come from
**OpenAlex** (a bibliographic index, reached over plain HTTP) plus, for two entries, from
official artifacts already on this host. So the correct label is **index-backed**, not
**document-verified**. Before a Paper Card is written for any entry, title and author order must
be re-checked against the paper's own first page.

Two entries are stronger, because the source was the project's own artifact:

- **P0001 Epona** — author list read directly from the official repo README author block.
  ⚠ The upstream enriched file `workspace/Epona/Epona.md` lists the eighth author as **"Li Yuan"**
  while the official README lists **"Yuan Li"**. Do not trust that enriched file's author list.
- **P0010 TOAD** — author order confirmed **twice**: the official repo citation block lists
  `Xu, Yihong` first (bibkey `xu2026toad`), and OpenAlex independently agrees. A caveat raised
  during resolution (that valeo.ai sometimes leads with a lab-lead author) is therefore closed:
  the repo's own BibTeX is the authority.

---

## 3. Ambiguous

| ID | Short name | Status | Candidates |
|---|---|---|---|
| P0002 | SafeDrive | **METADATA_AMBIGUOUS** | see below — the problem is larger than first reported |
| P0003 | GraphAD | identity resolved; **same-name collision** must be excluded | see below |
| P0005 | RiskWorld | identity resolved; mild collision | see below |
| P0008 | NPPC | identity resolved; acronym collision | disambiguate by DOI, never by acronym |

### P0002 SafeDrive — 13 same-name works, not 2

An OpenAlex title search for `SafeDrive` returns **13 works**. Driving/safety-relevant ones:

| Candidate | First author | Year | Venue | ID |
|---|---|---|---|---|
| (a) SafeDrive: Fine-Grained Safety Reasoning for End-to-End Driving in a Sparse World | Jungho Kim | 2026 | CVPR 2026 | arXiv 2602.18887 |
| (b) SafeDrive: Knowledge- and Data-Driven Risk-Sensitive Decision-Making for AVs with LLMs | Zhiyuan Zhou | 2025 | Accident Analysis & Prevention | DOI 10.1016/j.aap.2025.108299 |
| (c) SafeDrive Dreamer: Navigating Safety-Critical Scenarios in Autonomous Driving with World Models | Haitao Li | 2024 | AEJ | DOI 10.1016/j.aej.2024.10.039 |
| — SafeDrive: A New Model for Driving Risk Analysis Based on Crash Avoidance | Yibo Wang | 2020 | IEEE T-ITS | DOI 10.1109/TITS.2020.3033276 |
| — SafeDrive: Online Driving Anomaly Detection From Large-Scale Vehicle Data | Mingming Zhang | 2017 | IEEE T-II | DOI 10.1109/TII.2017.2674661 |

Non-driving collisions also exist (OSDI 2006 language-based extensions; lane-tracking; pothole
detection; IoT). **Why this cannot be adjudicated here:** a full-content search of the entire
upstream `D:\zym_information\ZYM\wam` tree for `SafeDrive` returned **zero** local references, so
there is no local Ledger entry to disambiguate against. Per Batch 0 rule 3 → **no download, no
identity guess.** P0002 keeps the Ledger slot so the ID stays stable; its bibliographic fields
stay `UNKNOWN`.

Resolution input for you (not treated as a verdict): candidate **(a)** is the only one that
operates on the ego trajectory space where trajectory scoring and planner exploitation live, and
it matches the tags `planning;safety;trajectory-scorer` + `P1_RETIRED;P2R_PRIMARY`. Candidate (b)
makes discrete LLM-driven risk decisions, not candidate-trajectory ranking. Candidate **(c)** was
not in your original list and is thematically a world-model paper — it deserves explicit
consideration rather than being silently dropped.

### P0003 GraphAD — competing non-driving works

`GraphAD` is also used by: graph anomaly detection over multivariate time series (arXiv
2205.11139), a SIGIR 2022 paper (DOI 10.1145/3477495.3531848), microservice anomaly detection
(2025), and Alzheimer's early diagnosis (2026). The driving match (2403.19098 / IJCAI 2024) fits
the tags exactly and is treated as resolved, **but the collision must be excluded at download
time by matching title + abstract, not the short name.**

Also flagged: OpenAlex holds **two** IJCAI-keyed records for the driving GraphAD —
`10.24963/ijcai.2024/270` (2024, no author list resolved) and `10.24963/ijcai.2025/270` (2025,
full authors) — both pages 2422–2430, with differing author lists. One is almost certainly an
indexing artifact of the same paper; which one is **UNKNOWN**. We cite the 2024 DOI and must
verify the author list against the IJCAI proceedings before first print.

### P0005 RiskWorld — milder

Only unrelated sociological/corporate "Riskworld" uses and a "RiskWebWorld" benchmark were
found. **No competing driving RiskWorld exists.** Treated as resolved.

### P0008 NPPC — disambiguate by DOI

"NPPC" in the literature is dominated by the **C-type natriuretic peptide gene**, plus an
unrelated cancer-classification classifier and a seismic-engineering building. The reliable key is
**DOI 10.1109/LRA.2026.3663819** (IEEE RA-L 2026), not the acronym.

### P0012 DA-WAM — NOT ambiguous

A title search on "WAM" returns only unrelated works (ocean-wave model, WAMS phasor measurement,
Web Acceptance Model, antibody modelling); "Decision-Aligned" returns no second DA-WAM.

---

## 4. Duplicate

**None.** All 12 Ledger entries are bibliographically distinct: no shared arXiv ID, no shared DOI,
no normalized-title collision.

Thematically adjacent but distinct (not duplicates): P0006 Gen-Drive (reward-model RL fine-tuning)
vs P0007 DriveReward (reward dataset + VLM reward model); P0004 BeTop vs P0003 GraphAD (both
interactive prediction). The corpus contained only the `P0001 EXAMPLE` template row before this
batch, so there was no pre-existing row to collide with.

### Pre-existing external copies found (provenance items, not duplicates)

| Asset | Location | Evidence | Consequence |
|---|---|---|---|
| Epona PDF (candidate canonical) | `workspace\Epona\Epona.pdf` | 21,696,844 B · SHA256 `5AD061982813C667…` | not migrated; version unverified |
| Epona MinerU origin PDF | `workspace\Epona\Epona_mineru\Epona\txt\Epona_origin.pdf` | 21,664,903 B · SHA256 `731D0633001DF878…` | **byte-different from the above** |
| Epona raw MD | `workspace\Epona\Epona_mineru\Epona\txt\Epona.md` | 62,520 B · SHA256 `75622A1753D3ED54…` | true MinerU output |
| Epona enriched MD | `workspace\Epona\Epona.md` | 55,303 B · SHA256 `E78001C069AE4F00…` | **derived, not raw**; mojibake (`✝`→`鈥?`, `§`→`搂`) + author discrepancy → must not become `.raw.md` |
| Epona repo | `workspace\Epona` | `https://github.com/Kevin-thu/Epona.git` @ `69b24c55f5ab8b3ffde8fa55e9f833bfe64d2c68` (3 dirty entries) | unregistered |
| TOAD repo | `论文调研\repos\toad` | `https://github.com/valeoai/TOAD.git` @ `cfa88e008080d0799b2859b5935c257048ec0adf` (Apache-2.0) | unregistered; matches P0010 |
| WorldDrive / WoTE repos | `workspace\WorldDrive`, `workspace\WoTE` | WorldDrive @ `c375ee1e…`, WoTE @ `298957c1…`, both with `*_mineru` output | not in Batch 0A; for later batches |
| Out-of-batch PDF | `论文\2602.06521v1.pdf` | arXiv 2602.06521 = *DriveWorld-VLA: Unified Latent-Space World Modeling with Vision-Language-Action for Autonomous Driving* | **not in Batch 0A or the Batch 0 list** — flagged for the Ledger owner, not ingested |

Two Epona PDFs with different SHA256 means **at most one is the canonical arXiv v1**. PDF
`/Producer` and `/CreationDate` could not be extracted (both files use object streams; an ASCII
scan returned nothing) → **UNKNOWN**. Canonical status must be established by re-fetching arXiv
v1 and comparing hashes, not by assuming the larger file wins.

---

## 5. Official PDF source / official code source (proposed, NOT fetched)

⚠ **Resolvability is UNVERIFIED for every row below.** No HTTP request was issued by me, and the
resolver could not open any page. These are proposals for the download step.

| ID | Proposed official PDF source | Proposed official code source | code_available | evidence basis for code |
|---|---|---|---|---|
| P0001 Epona | https://arxiv.org/pdf/2506.24113 · CVF: `ICCV2025/papers/Zhang_Epona_...pdf` | https://github.com/Kevin-thu/Epona | **YES** | repo README read locally |
| P0002 SafeDrive | UNRESOLVED (blocked) | UNKNOWN | UNKNOWN | — |
| P0003 GraphAD | https://arxiv.org/pdf/2403.19098 | (candidate only) | UNKNOWN | `OpenDriveLab/GraphAD` was **pattern-inferred**, not verified |
| P0004 BeTop | https://arxiv.org/pdf/2409.18031 · NeurIPS proceedings PDF | https://github.com/OpenDriveLab/BeTop | **YES** | search-result listing; page not fetched |
| P0005 RiskWorld | https://arxiv.org/pdf/2608.21414 | UNKNOWN | UNKNOWN | — |
| P0006 Gen-Drive | https://arxiv.org/pdf/2410.05582 | (candidate only) | UNKNOWN | `Chengyuan-Zhang/Gen-Drive` unverified candidate |
| P0007 DriveReward | https://arxiv.org/pdf/2606.08525 | UNKNOWN | UNKNOWN | no dataset page located (unresolved, not "no") |
| P0008 NPPC | **no open source located** — IEEE Xplore doc 11393633 (paywalled) | UNKNOWN | UNKNOWN | — |
| P0009 DriveLaW | https://arxiv.org/pdf/2512.23421 · CVF CVPR 2026 PDF | https://github.com/xiaomi-research/drivelaw | **YES** | search-result listing; page not fetched |
| P0010 TOAD | https://arxiv.org/pdf/2606.07170 | https://github.com/valeoai/TOAD | **YES** | local clone + repo README citation |
| P0011 Sensitivity Shaping | https://arxiv.org/pdf/2606.14585 | UNKNOWN | UNKNOWN | — |
| P0012 DA-WAM | https://arxiv.org/pdf/2608.19085 | UNKNOWN | UNKNOWN | — |

`code_available` counts 4 YES / 8 UNKNOWN. **UNKNOWN is used deliberately** — a plausible-looking
GitHub path is not evidence that a repo exists, and two of the YES verdicts rest only on
search-result listings rather than a fetched repository page.

### Schema gap discovered

`01_CORPUS_MANIFEST_SCHEMA.md` has **no `official_pdf_url` field** — only `official_url`. The
"official PDF source" you asked for therefore has nowhere to live in the manifest and exists only
in this report. Not silently changed; awaiting your decision (§9).

---

## 6. Proposed Paper ID allocation

Allocated in the order you supplied. No reordering, no reuse.

| ID | Short name | reading_status | decision_relevance | Rationale |
|---|---|---|---|---|
| P0001 | Epona | DISCOVERED | MEDIUM | `GENERAL;P3_HOLD`; not in your likely-HIGH list |
| P0002 | SafeDrive | DISCOVERED | MEDIUM | blocked by ambiguity; no local evidence of decision impact |
| P0003 | GraphAD | DISCOVERED | MEDIUM | `P2R_PRIMARY`; not in your likely-HIGH list |
| P0004 | BeTop | DISCOVERED | HIGH | in your likely-HIGH list; interactive behavioural topology |
| P0005 | RiskWorld | DISCOVERED | MEDIUM | `P2R_PRIMARY;P3_HOLD`; not in your likely-HIGH list |
| P0006 | Gen-Drive | DISCOVERED | HIGH | upstream context: learned-reward RL improve-then-degrade |
| P0007 | DriveReward | DISCOVERED | **MEDIUM** (downgraded) | in your likely-HIGH list, but no local evidence it changed a decision → applied your "优先 MEDIUM" rule |
| P0008 | NPPC | DISCOVERED | HIGH | upstream context: key **counterexample** (no cost hacking; planning improved) |
| P0009 | DriveLaW | DISCOVERED | HIGH | upstream context: explicit reward/cost/risk not necessary |
| P0010 | TOAD | DISCOVERED | HIGH | upstream context: occupies much of the scorer-engineering solution space |
| P0011 | Sensitivity Shaping | DISCOVERED | HIGH | upstream context: ∂F/∂u ≈ 0 mechanism evidence |
| P0012 | DA-WAM | DISCOVERED | HIGH | upstream context: supervision blind spot for unexecuted candidate futures |

`decision_relevance` is **not** all-HIGH (6 HIGH / 6 MEDIUM). Every HIGH is backed by the upstream
local document `论文调研\P1_Agent_Bootstrap_Pack\01_RESEARCH_CONTEXT.md`, not by my own judgement.

`primary_tags` / `hypothesis_tags` were taken **verbatim** from your list; all fall inside the
controlled vocabularies of `01_CORPUS_MANIFEST_SCHEMA.md` — **no vocabulary extension needed**. No
hypothesis-support claim is implied by these tags.

### Interpretation recorded (needs confirmation)

`03_FILE_NAMING_STANDARD.md` uses `P0001_Epona` and **`P0002_DriveLaW`** as illustrative examples.
Taken literally that would make DriveLaW = P0002, contradicting Batch 0A order (SafeDrive is entry
2, DriveLaW is entry 9). I treated the naming-doc examples as non-binding and allocated DriveLaW =
**P0009**. Flagged because the two authorities conflict on their face.

---

## 7. Blockers (real, not research blockers)

### 7a. A2 clone of the private research repo — BLOCKED

```
git ls-remote (default schannel) -> fatal: schannel: AcquireCredentialsHandle failed: SEC_E_NO_CREDENTIALS (0x8009030E)
git -c http.sslBackend=openssl   -> fatal: could not read Username for 'https://github.com'
                                    (private repo → credential prompt)
                                    + sh.exe "couldn't create signal pipe, Win32 error 5"
```

1. **Credentials:** the repo is private; git needs a PAT or SSH key. None is available to me.
2. **Sandbox boundary:** `D:\zym_information\ZYM\wam\wam-research` is **outside** this session's
   writable root (`…\wam\research_assets`). A clone there would be denied even with credentials.
3. `PortableGit`'s `sh.exe`/`bash.exe` cannot create signal pipes under this confinement — the
   documented sandbox boundary, so git credential-prompt helpers that spawn a shell fail here
   regardless. Not retried another way.

### 7b. Tool availability changed mid-batch (material for the download step)

| Channel | Status | Consequence |
|---|---|---|
| `web_search` | **DOWN** — provider returned "Insufficient Balance" | cannot resolve code URLs or verify pages |
| HTTPS via .NET/schannel (PowerShell, `curl.exe`, `git`, `Invoke-WebRequest`) | **BROKEN** — `SEC_E_NO_CREDENTIALS` | plain HTTPS downloads from PowerShell will fail |
| `github.com` from the sandbox | TLS rejected (`000`) | repo existence cannot be confirmed by probe |
| **OpenAlex REST API over plain HTTP** | **WORKS** | this is how §2 was resolved |
| Python TLS (OpenSSL) | **WORKS** (per upstream evidence: the nuPlan/nuScenes downloads succeeded earlier via `scripts/download_url_resume.py`) | **the download step should use Python, not PowerShell/curl/git** |

This is the most actionable finding of the batch: **HTTPS through the OS TLS stack is broken on
this host, but Python's OpenSSL stack works.** The PDF-download step must therefore be implemented
in Python (e.g. `urllib`/`requests`), and the one-shot `git -c http.sslBackend=openssl` workaround
applies only to git. This should be captured before Step 4 is attempted.

---

## 8. Self-audit record (defect found and fixed in this batch)

A structural QC pass was run on the manifest after writing it. It caught a real defect introduced
by this agent:

```
defect : P0002 and P0008 rows had a field-count error (extra empty separator),
         shifting library_status..reading_status by one and truncating the notes field.
detect : Import-Csv row/column count + enum validation against 01_CORPUS_MANIFEST_SCHEMA.md
fix    : separator corrected in both rows (first attempt under-corrected → re-checked → fixed)
verify : rows=12, columns=21, unique paper_id=12,
         invalid reading_status=0, invalid decision_relevance=0, invalid library_status=0,
         empty notes=0, legacy github_card_path matching papers/cards/P*=12
re-verify after metadata merge: same checks, all 0; first_author resolved 11/12
```

---

## 9. Verification status and remaining gaps

**Verified (source-cited):** 11/12 exact titles, first authors, years, venues where a publisher
record exists; 4 DOIs; 4 `code_available=YES` with the evidence basis stated per row.

**Still UNKNOWN — deliberately:**

1. Every `code_available=UNKNOWN` (8 entries) — `github.com` is unreachable and `web_search` is down.
2. **P0002 SafeDrive** — the whole row, pending your adjudication.
3. **P0011 venue** — CoRL 2026 NOT confirmed; the arXiv DOI `10.48550/arxiv.2606.14585` carries no publisher venue.
4. **P0008 arXiv status** — no arXiv version found; stated as NONE, not guessed.
5. **P0007 dataset page** — no official dataset/HuggingFace page located. Unresolved, not answered "no".
6. **P0003 IJCAI duplicate record** — which of the 2024/2025 DOIs is canonical.
7. **Epona canonical PDF version** — two byte-different local PDFs; which is arXiv v1.
8. **DOIs for the 2026 arXiv-only preprints** (P0004, P0005, P0007, P0009–P0012) — none exists
   yet. Expected for very recent preprints, not a gap I can close.

Nothing was upgraded from `UNKNOWN` without a source, and no `RESOLVED` field rests on my own
judgement rather than a cited record.

---

## 10. Next smallest action

> Confirm the **SafeDrive** adjudication (§3) and the **private `wam-research` repo landing
> mechanism** (§7a) — both block Batch 0A's download step. A third decision now matters for the
> download itself: approve implementing Step 4 in **Python** (the only working HTTPS path, §7b).

Secondary decisions (non-blocking): add `official_pdf_url` to the schema; choose the canonical
Epona PDF; assign `论文\2602.06521v1.pdf` (DriveWorld-VLA) to a batch.
