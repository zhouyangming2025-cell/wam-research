# BATCH 0A INGEST REPORT

**Scope executed**: Batch 0A only — `P0001`–`P0012` (12 papers).
**Pipeline stages**: Step 4 canonical PDF acquisition → Step 5–7 MinerU raw MD → Step 8 provenance reconciliation.
**Date**: 2026-09-13.
**Rulings in force**: #3–#11 of the Batch 0A metadata gate (see `BATCH_0A_METADATA_REPORT.md`).

This report distinguishes four kinds of statement throughout:
**[FACT]** verified from a primary artifact, **[DECISION]** yours or a documented ruling,
**[ASSUMPTION]** mine and explicitly labelled, **[UNKNOWN]** unresolved and left unresolved.

---

## A. Canonical PDF acquisition (Step 4)

### A.1 Method

A single Python downloader (`scripts/fetch_canonical_pdfs.py`) was used, per ruling #6:

- TLS verification **ON**, with an explicit CA bundle (`certifi`). The host has no
  usable system CA store, so `verify=False` was never an option and never used.
- redirects followed, `TIMEOUT=90 s`, `ATTEMPTS=3` with backoff `3/8/20 s`,
  3 s spacing between arXiv requests.
- every download written to `<target>.part`, validated as HTTP 200, validated to
  contain `%PDF-` in the first 1024 bytes and to exceed 20 000 bytes, then
  SHA256'd, then atomically `os.replace`d onto the final name.
- a failure is recorded as `DOWNLOAD_BLOCKED` **with the real reason**; the
  canonical URL is never silently swapped for a third-party mirror.

**[FACT]** Result: **11 of 12 acquired**, 0 leftover `.part` files.

### A.2 Acquired canonical PDFs

| paper_id | short name | source_version | bytes | sha256 (first 12) |
|---|---|---|---|---|
| P0001 | Epona | `ICCV2025_camera_ready` | 18,718,629 | `bab0acb08dfa` |
| P0002 | SafeDrive | `CVPR2026_camera_ready` | 1,941,523 | `77b057a6687a` |
| P0003 | GraphAD | `arXiv_v1` | 8,469,624 | `36667d2cddcd` |
| P0004 | BeTop | `NeurIPS2024_camera_ready` | 6,841,853 | `ddd710d8c508` |
| P0005 | RiskWorld | `arXiv_v1` | 4,097,446 | `8241e4d40e34` |
| P0006 | Gen-Drive | `arXiv_v1` | 1,859,743 | `5b3377cf3c94` |
| P0007 | DriveReward | `arXiv_v1` | 14,330,221 | `16fdf0c22d51` |
| P0008 | NPPC | `none_available` | — | — (**blocked**) |
| P0009 | DriveLaW | `CVPR2026_camera_ready` | 5,729,791 | `74c3b1f2a642` |
| P0010 | TOAD | `arXiv_v1` | 3,007,062 | `552116bd4076` |
| P0011 | Sensitivity Shaping | `arXiv_v1` | 27,041,471 | `2da902b22d57` |
| P0012 | DA-WAM | `arXiv_v1` | 1,493,052 | `9c942d4a7c5a` |

Files: `papers\pdf\PXXXX_ShortName.pdf`. Exactly one canonical PDF per paper (ruling #5).

Camera-ready was available and used for **4 of 11**: P0001 and P0002 (CVF Open Access),
P0004 (NeurIPS proceedings), P0009 (CVF Open Access).
**[FACT]** For P0006 the ICRA 2025 camera-ready is IEEE-paywalled, so the official
arXiv version is canonical. For P0003 no IJCAI camera-ready URL could be verified, so
arXiv is canonical and the venue stays index-backed.

### A.3 The one failure

**[FACT] P0008 NPPC — `DOWNLOAD_BLOCKED: PAYWALLED_NO_OPEN_SOURCE`**
(IEEE Xplore document 11393633, DOI `10.1109/LRA.2026.3663819`). There is no arXiv
version. Consequences: no canonical PDF, no raw MD, no front-page verification, and
its metadata stays `INDEX_BACKED`. It is the only row with `library_status = NONE` and
`reading_status = DISCOVERED`.

---

## B. Document front-page metadata verification (Step 4 gate)

### B.1 Outcome

`scripts/verify_frontpage.py` opened each canonical PDF with an independent PDF parser
(`pypdfium2`), extracted page 1, and tested the expected title and first-author surname.

**[FACT] 11 of 11 acquired PDFs → `DOCUMENT_VERIFIED`.**
Title match `EXACT` for all 11; first-author surname found on the front page for all 11.

| paper_id | pages | document title as printed | metadata Title field |
|---|---|---|---|
| P0001 | 11 | Epona: Autoregressive Diffusion World Model for Autonomous Driving | present |
| P0002 | 11 | SafeDrive: Fine-Grained Safety Reasoning for End-to-End Driving in a Sparse World | present |
| P0003 | 17 | GraphAD: Interaction Scene Graph for End-to-end Autonomous Driving | absent |
| P0004 | 33 | Reasoning Multi-Agent Behavioral Topology for Interactive Autonomous Driving | absent |
| P0005 | 9 | RiskWorld: Object-Centric Latent World Modeling for Autonomous Driving Risk Identification | present |
| P0006 | 7 | Gen-Drive: Enhancing Diffusion Generative Driving Policies with Reward Modeling and Reinforcement Learning Fine-tuning | absent |
| P0007 | 16 | DriveReward: A Comprehensive Dataset and Generative Vision-Language Reward Model for Autonomous Driving | present |
| P0009 | 12 | DriveLaW: Unifying Planning and Video Generation in a Latent Driving World | present |
| P0010 | 15 | Test-Time Trajectory Optimization for Autonomous Driving | present |
| P0011 | 18 | Sensitivity Shaping for Latent Modeling | present |
| P0012 | 15 | DA-WAM: Decision-Aligned Future Latents for Driving World Models | present |

164 pages total. 8 of 11 carry a PDF `Title` metadata field; 3 do not (P0003, P0004,
P0006). That is a property of the publisher's PDF, not a defect in the acquisition.

### B.2 Conflicts the front page resolved

1. **P0001 Epona — author 8 is `Li Yuan`.** The camera-ready prints
   `Kaiwen Zhang … Jingwei Huang, Li Yuan, Qian Zhang, Xiao-Xiao Long, Xun Cao, Wei Yin`.
   This **confirms ruling #3** and overrules the `Yuan Li` spelling that OpenAlex and
   the GitHub README carry. The paper is the higher authority; no metadata is taken
   from the README.
2. **P0006 Gen-Drive — title is `Fine-tuning`, not `Fine-Tuning`.** The front page
   prints the lowercase form; OpenAlex carried the capitalised variant. The paper wins.
   **[DECISION]** recorded as such in the manifest.
3. **P0002 SafeDrive — all six authors confirmed verbatim**
   (Jungho Kim, Jiyong Oh, Seunghoon Yu, Hongjae Shin, Donghyuk Kwak, Jun Won Choi,
   Seoul National University), matching the list you adjudicated on. `METADATA_AMBIGUOUS`
   is withdrawn. The paper itself prints the project page
   `https://spa-junghokim.github.io/SafeDrive-Page/`; repository existence was **not**
   verified, so `code_available` stays `UNKNOWN`.
4. **P0010 TOAD — first author `Yihong Xu` confirmed twice**, by the repo citation block
   and by the camera-ready front page.
5. **P0012 DA-WAM — author list confirmed** (Ruiguo Zhong, Benshan Ma, Xiaolong Chen,
   Lang Zhang, Mingyue Feng, Yaonong Wang, Pei Liu, Jun Ma; HKUST-GZ / Leapmotor).

### B.3 Conflicts the front page exposed but did NOT resolve

| item | detail | status |
|---|---|---|
| P0010 TOAD metric | repo README advertises **94.9 PDMS** on NAVSIM-v1; the paper abstract states **94.7 PDMS** | **[UNKNOWN] recorded, not resolved.** I do not adjudicate which number is correct. |
| P0003 GraphAD venue | OpenAlex holds **two** IJCAI records (2024 and 2025) with the same pages 2422–2430 | **[UNKNOWN]** venue remains `INDEX_BACKED` |
| P0011 venue | CoRL 2026 **not confirmed**; no publisher venue in the DOI | **[UNKNOWN]** |
| P0008 | no PDF ⇒ no verification possible | stays `INDEX_BACKED` |
| P0001 name spelling | front page prints `Xiao-Xiao Long` and `Shenzhen Gruaduate School` | **[FACT]** typographical variants inside the publisher's own PDF; left as printed |

### B.4 Evidence levels now in the manifest

Every `notes` field carries an explicit token: `EVIDENCE_LEVEL=DOCUMENT_VERIFIED`
(11 rows) or `EVIDENCE_LEVEL=INDEX_BACKED` (P0008 only).

---

## C. Raw MD layer (Steps 5–7)

### C.1 Conversion

**[FACT]** MinerU 3.4.5, `pipeline` backend, `-m auto`, per paper, one process at a time:

```
<venv>\Scripts\python.exe scripts\run_mineru.py -p papers\pdf\PXXXX_Short.pdf \
    -o papers\quarantine\mineru_artifacts\PXXXX_Short -b pipeline -m auto
```

`pipeline` is not the CLI default; the default `hybrid-engine` needs VLM weights that
are not installed here (`models-dir.vlm` is empty), so it was set explicitly.
`-m auto` was chosen so each PDF gets text extraction or OCR by its own nature rather
than by my assumption.

### C.2 Result

**[FACT] 11 of 11 converted and QC-passed: `RAW_MD_READY`.** 702,126 characters total.
Compute time: 2,346.8 s for the eleven successful conversions, plus 609.0 s for P0012's
failed first attempt — 2,955.8 s of CPU work in total.

| paper_id | chars | headings | images | mojibake | seconds | QC |
|---|---|---|---|---|---|---|
| P0001 | 56,223 | 19 | 11/11 | 0 | 196.5 | READY |
| P0002 | 49,328 | 21 | 5/5 | 0 | 164.6 | READY |
| P0003 | 47,393 | 19 | 4/4 | 0 | 193.4 | READY |
| P0004 | 129,551 | 49 | 35/35 | 0 | 420.0 | READY |
| P0005 | 48,913 | 22 | 14/14 | 0 | 191.0 | READY |
| P0006 | 42,505 | 18 | 14/14 | 0 | 194.9 | READY |
| P0007 | 59,082 | 23 | 8/8 | 0 | 131.4 | READY |
| P0009 | 63,498 | 19 | 3/3 | 0 | 171.4 | READY |
| P0010 | 69,928 | 20 | 11/11 | 0 | 183.0 | READY |
| P0011 | 76,865 | 24 | 10/10 | 0 | 313.0 | READY |
| P0012 | 58,840 | 21 | 9/9 | 0 | 187.6 | READY (2nd attempt) |

QC applied to every file: title heading present, abstract present, ≥3 headings,
references section present, length ≥5 000 chars, mojibake ratio measured, and **every
image the markdown references is present on disk**. The columns above are the measured
values, not assertions.

### C.3 Output shape

Canonical-adjacent output, per paper (ruling #8):

```
papers\raw_md\PXXXX_ShortName\
    PXXXX_ShortName.raw.md      the MinerU markdown, verbatim, renamed only
    images\                     only the images that markdown actually references
```

Markdown keeps MinerU's relative `![](images/<sha>.jpg)` references, so the pair is
self-contained and no global shared image directory exists.

Everything else MinerU emitted stays in quarantine and is **never** canonical:

```
papers\quarantine\mineru_artifacts\PXXXX_ShortName\auto\
    PXXXX_ShortName.md                  (the pre-rename copy)
    PXXXX_ShortName_content_list.json
    PXXXX_ShortName_content_list_v2.json
    PXXXX_ShortName_middle.json
    PXXXX_ShortName_model.json
    PXXXX_ShortName_origin.pdf          (MinerU's re-render of the source)
    PXXXX_ShortName_layout.pdf
    PXXXX_ShortName_span.pdf
```

An `auto\images\` copy is also retained there. The `.raw.md` file was **not** edited
after conversion: it is raw by design.

### C.4 The one conversion failure, and its cause

**[FACT]** P0012 DA-WAM failed on its first attempt after 609 s. The log shows layout
inference completing over all 15 pages, then, at the start of MFR formula recognition
(132 formulas, the largest formula load in the batch):

```
MFR Predict:   0%|          | 0/132 [00:00<?, ?it/s]
Error: 1 task(s) failed … : All connection attempts failed
```

`All connection attempts failed` means the client lost its local `mineru-api` service:
the service process was terminated with no traceback, i.e. killed, not raised. The
document itself is fine — layout inference had already succeeded on it.

**[FACT] Retry with reduced parallelism succeeded**: the same command with the
thread-pool ceiling lowered from 8 to 2 and the render pool from 4 to 1 produced a
clean `RAW_MD_READY` in 187.6 s. That confirms a concurrency-related resource peak,
not a defect in the PDF or in the conversion settings. The reduced setting was applied
only to this retry.

### C.5 Fidelity observation: line-break hyphen loss

**[FACT]** MinerU's text-extraction path joins words that were hyphenated across a line
break without restoring the hyphen. Measured over 17 tracked terms
(`scripts/check_raw_md_fidelity.py`):

**41 merged forms vs 452 correctly hyphenated forms — 8.3 % of these occurrences lost
their hyphen.** Worst case: P0006 Gen-Drive, 14 merged, of which **11 are
`pair-wise` → `pairwise`**, which is a legitimate alternative spelling rather than a
loss. `endtoend`, `trajectoryconditioned` and `gridcentric` do occur (visible in the
P0002 abstract). Discarding that false-positive class, the real loss is concentrated
and small.

**[ASSUMPTION]** I treat this as an acceptable characteristic of raw MD, because the
corpus spec asks for *raw* output and the source PDF remains canonical for exact
wording. If exact hyphenation mattered for downstream extraction, the fix would be a
de-hyphenation pass at the card stage, not a repair of the raw layer. **I have not
modified the raw markdown.**

Zero mojibake was found across all 11 files; the earlier `✝`/`§` corruption in the
pre-existing derived `Epona.md` does not appear in this batch's output.

### C.6 Integrity check

**[FACT]** Re-reading the corpus with the mediated read path confirmed: 11 PDFs present,
no stray `.part` files, every file starts with `%PDF-`, and all 11 SHA256 values match
the download records exactly (11 match, 0 mismatch). Manifest validation:
12 rows × 25 columns, 11 populated `pdf_sha256`, 11 populated `raw_md_sha256`,
0 empty `notes`, 12 card paths, and **every `pdf_local_path` / `raw_md_local_path`
resolves to an existing file**.

---

## D. Provenance conflicts

### D.1 Epona canonical version (ruling #7 discharged)

**[FACT] The ICCV 2025 camera-ready is a third, distinct file.** Comparing within a
single consistent read path, all three hash differently:

| artifact | sha256 (native read path) |
|---|---|
| canonical `papers\pdf\P0001_Epona.pdf` (ICCV 2025 camera-ready) | `CBFC52B2D2D0FA37449295E04CC789EB50BD7C9FF371FAC5A211E956483A3127` |
| pre-existing `workspace\Epona\Epona.pdf` | `5AD06198…` |
| pre-existing MinerU `Epona_origin.pdf` | `731D0633…` |

Ruling #7's condition ("if either matches, reuse") is **not** met, so **neither
pre-existing file may serve as canonical**, and `P0001_Epona.pdf` is the only canonical
Epona PDF. Both pre-existing files remain untouched where they were (upstream tree is
read-only for me); they are not registered anywhere.

### D.2 The pre-existing Epona markdown must not be reused

**[FACT]** `workspace\Epona\Epona.md` (55,303 B) is a *derived, enriched* file, not
MinerU raw output. It shows mojibake (`✝` → `鈥?`, `§` → `搂`) and an author-name
discrepancy. The true MinerU raw output of that run is
`Epona_mineru\Epona\txt\Epona.md` (62,520 B). **Neither is used**: `P0001`'s raw MD was
regenerated from the new canonical PDF.

### D.3 Environment defect: two different views of the same file

This is the most consequential unresolved environment item and it affects how any
recorded hash may be re-checked.

**[FACT]** For files on this workspace the two read paths disagree:

| artifact | mediated Python read | native Windows read (PowerShell / cmd / certutil) |
|---|---|---|
| `P0010_TOAD.pdf` | 3,007,062 B, starts `%PDF-`, parses | 3,008,086 B (**+1024**), no `%PDF` anywhere |
| `P0001_Epona.pdf` | 18,718,629 B, valid PDF | 18,719,653 B (+1024), sha256 `CBFC52B2…` |
| `CORPUS_MANIFEST.csv` (Python-written) | valid CSV, 12×25 | unparseable text |
| 10-byte text file (Python-written) | `hello-pwsh` | `hello-pwsh` (agree) |
| `hosts` (outside workspace) | 956 B | 956 B (agree) |

**[FACT]** The +1024 relation also holds for files this session never wrote: the
pre-existing `Epona.pdf` reads 21,695,820 B in Python and 21,696,844 B natively;
`Epona_origin.pdf` reads 21,663,879 B and 21,664,903 B. So this is a property of the
host environment, not of my downloads, and not of any single writer.

**[FACT]** Which view is the real document: the Python view is a complete, valid PDF
(`%PDF-1.6` header, `%%EOF` trailer, self-consistent xref, correct page count, correct
printed title and authors on page 1). A non-PDF view cannot produce that. The previous
session's MinerU run — also a Python process — successfully parsed `Epona.pdf`, which is
only possible from the valid view.

**Consequences recorded, not papered over:**

1. **Hash provenance is now part of the hash.** The `pdf_sha256` / `raw_md_sha256`
   values in `CORPUS_MANIFEST.csv` were computed by the **mediated Python read path**,
   i.e. over the actual PDF/MD content. A verification performed with PowerShell,
   `Get-FileHash`, `certutil` or Explorer on this host **will not reproduce them**;
   it will see the framed view instead. Any future verification step must use the same
   read path or it will report false corruption.
2. **[ASSUMPTION]** I take the Python view as authoritative *because it is the view the
   pipeline and any PDF consumer actually parse*. I could not determine the physical
   storage form, and I did not guess further. If you can open `papers\pdf\P0001_Epona.pdf`
   in a normal Windows PDF viewer, that settles it in one glance and I would like to know
   the result.
3. **[FACT]** Directories created via `tempfile.mkdtemp` become **undeletable**:
   `papers\quarantine\_tmp2`, `_tmp3` and three `mineru-api-client-*` directories inside
   `_tmp` remain. `cmd /c rmdir /s /q`, `Remove-Item -Recurse -Force` and `icacls`-free
   deletion all return `Access is denied`. They contain no corpus asset, only failed
   MinerU scratch, and they live inside `quarantine` where non-canonical material belongs.

### D.4 Hash comparison for the remaining papers

**[FACT]** For the 10 other acquired PDFs there is no competing local copy, so no
comparison was possible or needed. Hash authority for those rows is the Python read path,
same as D.3.

---

## E. Official code — conservative status

`code_available = YES` is written only where an official source was actually observed.
Reachability is **not** officiality, and the evidence basis is stated per row.

**[FACT]** Probed over HTTPS with TLS verification on (`scripts/probe_code_urls.py`);
GitHub's repository search API was used to hunt the two inferred candidates. Nothing was
cloned.

| paper_id | URL | HTTP | observed | verdict |
|---|---|---|---|---|
| P0001 | `github.com/Kevin-thu/Epona` | 200 | page self-describes as "Official Code for Epona … (ICCV 2025)" | **YES** |
| P0004 | `github.com/OpenDriveLab/BeTop` | 200 | "[NeurIPS 2024] Behavioral Topology (BeTop) …" | **YES** |
| P0009 | `github.com/xiaomi-research/drivelaw` | 200 | "[CVPR2026] DriveLaW: Unifying Planning and Video Generation …" | **YES** |
| P0010 | `github.com/valeoai/TOAD` | 200 | "Official implementation for TOAD …" | **YES** |
| P0003 | `github.com/zhangyp15/GraphAD` | 200 | owner handle matches first author Yunpeng Zhang; page mentions GraphAD, scene graph, autonomous driving | **YES** |
| P0003 | `github.com/OpenDriveLab/GraphAD` | **404** | — | candidate was **wrong** (mine) |
| P0006 | `github.com/Chengyuan-Zhang/Gen-Drive` | **404** | — | candidate was **wrong** (mine) |
| P0006 | Gen-Drive / GenDrive search | — | no matching project | **no repo located** ⇒ stays `UNKNOWN` |
| P0007 | DriveReward search | — | **0 results** | **no repo** ⇒ stays `UNKNOWN` |
| P0008 | NPPC search | — | only unrelated projects (Notepad++ plugins etc.) | **no repo**; acronym confirmed unsafe |

**[FACT] My two earlier pattern-inferred candidates were both 404.** They were
presented in the metadata report as candidates, not as facts, and they are now killed:
`OpenDriveLab/GraphAD` and `Chengyuan-Zhang/Gen-Drive` do not exist. The real GraphAD
repository is under the first author's account. This is exactly why the ruling said to
be conservative, and I am flagging my own inference error rather than quietly fixing it.

**[ASSUMPTION]** `P0004` and `P0009` rest on a repository title/description match and a
lab/company account; `P0003` on owner-handle-plus-topic match. I would call these strong
but not proof of officiality. Only a paper's own link or an author statement would make
them airtight, and web search was unavailable (section F).

---

## F. Failures, unknowns, and things I could not do

Nothing below is hidden or softened.

1. **P0008 NPPC — no PDF obtainable** (paywall, no open version). Consequence: this HIGH
   relevance paper cannot be read from the corpus at all. Only its DOI-verified metadata
   is available.
2. **`web_search` is down** — the provider returns "Insufficient Balance". All discovery
   in this batch therefore rested on the OpenAlex REST API plus direct HTTPS probes.
   Anything that needed a search engine (venue confirmations, code repos, dataset pages)
   is correspondingly weaker, and I have said so per row.
3. **GitHub repository work is decoupled** (ruling #9): no PAT requested, stored or used;
   no clone attempted. Step 9 (Paper Cards) has no local home yet because the
   `wam-research` worktree does not exist.
4. **Four sandbox/environment defects blocked the unmodified toolchain.** All four were
   diagnosed from evidence and worked around **without** weakening any validation:
   - `tempfile.mkdtemp` directories are inaccessible afterwards (`WinError 5`), which
     kills MinerU's local API server → replaced `mkdtemp` with a plain `os.makedirs`
     creation.
   - `ProcessPoolExecutor` cannot start (it needs `multiprocessing.Pipe` → named pipe,
     denied) → process pools are thread-backed. Parallelism is preserved; workers are
     GIL-releasing render/inference loops.
   - HuggingFace locking under `C:\Users\...\.cache\huggingface\hub\.locks` is denied.
     Root cause found: MinerU resolves `mineru.json` **relative to the CWD**, so running
     from the corpus directory fell back to `%USERPROFILE%\mineru.json` whose
     `models-dir.pipeline` is **empty**, which triggered a model download. Pointing
     `MINERU_TOOLS_CONFIG_JSON` at the installation config (`D:\Program Files\Mineru\mineru.json`,
     `models-dir` holding the local 2.5 GB pipeline models including MFR/unimernet) makes
     the run fully offline — nothing is downloaded and no lock is needed.
   - The shims must apply inside MinerU's own subprocesses, so they are delivered via a
     `PYTHONPATH` `sitecustomize.py` gated by an env var rather than by patching the
     launcher. **No file inside the MinerU installation was modified.**
   All four are documented in `scripts/_mineru_site/sitecustomize.py`.
5. **No mechanism exists for ID-less discovery records.** `2602.06521v1.pdf`
   (DriveWorld-VLA, parked in `论文\`) is currently recorded only as
   `DISCOVERED_NOT_INGESTED`, `target_batch = Batch 1`, with **no Paper ID** (ruling #11).
   The manifest schema has no ingest queue, so the record lives in the report, not in
   the manifest.
6. **Schema amendment recommended, not applied.** `pdf_sha256` and `raw_md_sha256` are
   only meaningful together with the read path that produced them (section D.3). I did
   **not** edit `01_CORPUS_MANIFEST_SCHEMA.md` for this, because rulings #4/#11 authorised
   the four new fields themselves, not a change to what they mean. Proposed wording:
   *"Hashes are computed over file content as read by the mediated process; native Windows
   tooling on this host sees a differently framed representation and will not reproduce
   them. Record the computing tool alongside any hash."*
7. **Left-behind undeletable directories** in `papers\quarantine\` (section D.3.3).
8. **`BATCH_0A_METADATA_REPORT.md` self-correction**: its two code-repository entries
   marked as pattern-inferred candidates are both wrong (section E). The metadata report
   is not rewritten; this report supersedes them.
9. **P0012 needed two attempts.** The first crashed the local MinerU service during
   formula recognition; the retry at lower concurrency succeeded (section C.4). No
   content was lost — the retry produced the complete 58,840-character markdown — but
   the successful run used a lower-parallelism setting than the other ten, so P0012's
   conversion is not byte-identical in provenance to the rest.
10. **Raw MD is raw.** 8.3 % hyphen loss on tracked terms and no de-hyphenation pass
    (section C.5). The PDF stays canonical for exact wording.

---

## Self-audit

- No PDF was read for scientific content in this step, no hypothesis verdict was upgraded
  or downgraded, and no novelty or gap judgement was made. Hypothesis tags in the manifest
  are copied from the definitions you supplied.
- 11 of 12 acquisitions succeeded and the 12th failed for an external reason (paywall),
  reported with the exact DOI and document id.
- Every metadata conflict found is listed with the authority chosen and the reason; the
  three conflicts I could not resolve are marked `[UNKNOWN]` and left unresolved.
- The three rows where my own earlier inference was wrong (two code repositories) are
  stated as failures, not silently corrected.
- `P0001`'s raw MD was regenerated from the new canonical PDF; no pre-existing derived
  Markdown was promoted into the corpus.

---

## Deliverable state

**Corpus layer (this step)**
`papers\pdf\` 11 canonical PDFs · `papers\raw_md\PXXXX_ShortName\` 11 raw markdown files
plus referenced images · `papers\quarantine\mineru_artifacts\` all intermediate MinerU
output · `manifests\CORPUS_MANIFEST.csv` 12 rows × 25 columns.

**Evidence layer**
`manifests\batch_0a_download_results.json` · `batch_0a_frontpage_verification.json` ·
`batch_0a_rawmd_results.json` · `batch_0a_rawmd_fidelity.json` · `batch_0a_code_probe.json`.

**Scripts** (all committed under `scripts\`, re-runnable and idempotent where possible)
`fetch_canonical_pdfs.py` · `verify_frontpage.py` · `build_manifest.py` ·
`build_raw_md.py` · `check_raw_md_fidelity.py` · `probe_code_urls.py` · `run_mineru.py` ·
`_mineru_site\sitecustomize.py`.

### Two things that need you

1. **Which filesystem read path is authoritative for hashes** (section D.3). I recorded
   the mediated-Python hashes and stated the caveat, but I did not guess which view is
   physically real. The cheapest resolution is you opening
   `papers\pdf\P0001_Epona.pdf` in a normal Windows PDF viewer and telling me whether it
   renders. If it does, the Python view is the content and my manifest hashes are correct
   as recorded.
2. **P0008 NPPC is unreadable from the corpus** (paywall). If you have institutional
   access, the only action I can take with a lawfully obtained PDF is hash it, verify the
   front page and convert it — tell me if such a copy exists.

### Not done, deliberately

Batch 0B was not started. Step 9 (Paper Cards) was not started — no `wam-research`
worktree exists to host them. Step 10 (code repository registration) was not started;
`CODE_REPO_MANIFEST.csv` still holds only its intentional `R0001 EXAMPLE` row. No
hypothesis verdict was touched. No repository was cloned. No upstream file was modified
or deleted.

**Stopping here as instructed.**
