# Round 2 Targeted Ingest Report

Generated 2026-09-14 from `manifests/batch_round2_*.json` by `scripts/build_round2_report.py`;
every hash and count below is copied out of those ledgers, never retyped.

**Scope.** The eight records frozen in `state/TARGETED_READING_QUEUE.md` and requested by
`agent/prompts/ROUND2_TARGETED_INGEST.md`: acquisition, canonical PDF, MinerU raw-MD text
layer, provenance/QC facts and card skeletons.

**Explicitly not in scope, and absent from every artifact produced here.** No scientific
reading was performed: no observed-failure verdict, no hypothesis impact, no prior-art
occupancy judgement and no research verdict is recorded. Every scientific section of every
card is `PENDING SCIENTIFIC REVIEW` (deep-read / GPT-5.6 Sol work). No method design and no
risk-field idea was produced.

**Stop condition.** Reached: 7 records are `RAW_MD_READY`; 1 record (P0020) carries a
specific lawful acquisition blocker.

---

## 1. ID allocation

| paper_id | short name | role | title | year | first author | venue |
|---|---|---|---|---|---|---|
| P0013 | BridgeSim | A1 core P2-R attack set | BridgeSim: Unveiling the OL-CL Gap in End-to-End Autonomous Driving | 2026 | Seth Z. Zhao | arXiv preprint |
| P0014 | ReactSimBench | A2 core P2-R attack set | ReactSim-Bench: Benchmarking Reactive Behavior World Model Simulation in Autonomous Driving | 2026 | Zhiyuan Zhang | arXiv preprint |
| P0015 | CausalDrive | A3 core P2-R attack set | CausalDrive: Real-time Causal World Models for Autonomous Driving | 2026 | Tianyi Yan | arXiv preprint |
| P0016 | CounterfactualPred | A4 core P2-R attack set | How Can Driving World Models Do Counterfactual Prediction? | 2026 | Jiaru Zhang | arXiv preprint |
| P0017 | CRAFT | A5 core P2-R attack set | CRAFT: Counterfactual-to-Interactive Reinforcement Fine-Tuning for Driving Policies | 2026 | Keyu Chen | arXiv preprint |
| P0018 | GameFormer | H1 historical novelty control | GameFormer: Game-theoretic Modeling and Learning of Transformer-based Interactive Prediction and Planning for Autonomous Driving | 2023 | Zhiyu Huang | ICCV 2023 |
| P0019 | M2I | H2 historical novelty control | M2I: From Factored Marginal Trajectory Prediction to Interactive Prediction | 2022 | Qiao Sun | CVPR 2022 |
| P0020 | Bahram2016 | H3 historical novelty control | A Game-Theoretic Approach to Replanning-Aware Interactive Scene Prediction and Planning | 2016 | Mohammad Bahram | IEEE Transactions on Vehicular Technology 65(6), 3981-3992 |

IDs were allocated in the exact order of the prompt's target list, using the next unused
stable IDs; the highest pre-existing ID was P0012, so P0013-P0020 are new. No ID was
recycled or renumbered, and no short name collides with an existing record.

## 2. Canonical source and source_version

| paper_id | source_version | canonical URL | basis |
|---|---|---|---|
| P0013 | arXiv_v1 | https://arxiv.org/pdf/2604.10856 | Official arXiv preprint; no venue version verified. |
| P0014 | arXiv_v1 | https://arxiv.org/pdf/2606.14058 | Official arXiv preprint; no venue version verified. |
| P0015 | arXiv_v1 | https://arxiv.org/pdf/2606.15341 | Official arXiv preprint; no venue version verified. |
| P0016 | arXiv_v1 | https://arxiv.org/pdf/2608.11601 | Official arXiv preprint; no venue version verified. |
| P0017 | arXiv_v1 | https://arxiv.org/pdf/2605.04470 | Official arXiv preprint; no venue version verified. |
| P0018 | ICCV2023_camera_ready | https://openaccess.thecvf.com/content/ICCV2023/papers/Huang_GameFormer_Game-theoretic_Modeling_and_Learning_of_Transformer-based_Interactive_Prediction_and_ICCV_2023_paper.pdf | Venue camera-ready, chosen over the arXiv preprint per the corpus canonical priority. Located by scanning the ICCV2023 Open Access index because CVF truncates the title inside its slug. |
| P0019 | CVPR2022_camera_ready | https://openaccess.thecvf.com/content/CVPR2022/papers/Sun_M2I_From_Factored_Marginal_Trajectory_Prediction_to_Interactive_Prediction_CVPR_2022_paper.pdf | Venue camera-ready, chosen over the arXiv preprint per the corpus canonical priority. |
| P0020 | none_available | (none) | No lawful open source. Paywall, not an acquisition oversight. |

Source-version vocabulary used as defined by the corpus standard. Venue camera-ready outranks
an official arXiv version, which outranks a project-hosted copy; no project-hosted copy was
used. For A1-A5 no venue version could be verified in this pass, so the official arXiv
preprint is canonical and recorded as `arXiv_v1` rather than as a camera-ready claim.

## 3. PDF hash / raw-MD hash

| paper_id | PDF bytes | pdf_sha256 | raw_md_sha256 |
|---|---|---|---|
| P0013 | 14,142,381 | `0761960bc4ccecfafceeb9de91e86c4802cac72de3a3db5c0ff86104b0c2f9db` | `40292b954d4b287eeed35996ef2057f5d3535d60588a83235e2f6aa7748e251b` |
| P0014 | 3,527,069 | `6cc8a9c29b04502a5a66621c3e3e645ff98ea977db0a9d7cc57bab1734e74bb7` | `d6a84f926349d31d1f294645f7e2f1b8daf8b577f11ff67327f46fac3040143c` |
| P0015 | 2,859,614 | `122f70ce0788be2207a2a8119c60077e33bc7c869139af39ac665c14af647215` | `2ed84911f1db9683c6363b1b2a199cf0e6ead04122e52227a94346be8fd46b6c` |
| P0016 | 2,871,125 | `f8c89128cd5ec24c435e0ff128b6152a638ea4ba90c2089b415a4e251eb3f898` | `4274e4dedfaf23ade590a8a422fa700edb20ceb9bd989689231da2dc2a3e1a94` |
| P0017 | 2,973,002 | `6530ffb316ec827f3f875523388a4d5b48c1f76c20759b69d3ed4db8ce5a2db8` | `b1bfece5ad0968fa6c3222ac998b63d7d70f6524a96f90afdc3bb37955b09829` |
| P0018 | 1,355,533 | `f70b54c4f9232fb666b746769e183f1764c2ed6757b0326ccb078257d01a656a` | `866a5617e23785af2b7795927804ae0c4f04c5e534f7fe66a30580f7d582bc1d` |
| P0019 | 1,848,721 | `9344a1364a225d8befcc46d6e6e0f0eda1d9d9c16ad60a42e09437f846f87718` | `9dc0ecf9faae49efde8a2ae3109f1edd0b743eef85378e6d3540c06db9a02886` |
| P0020 | n/a | `NOT ACQUIRED` | `NOT CREATED` |

Hashes are SHA256 over logical document bytes read through the canonical Python corpus I/O
path. One canonical PDF per paper; PDFs and MinerU intermediates stay on local/NAS and are
never uploaded. The known native/.NET +1024 framing quirk was not re-investigated.

## 4. Front-page verification

| paper_id | pages | title_match | first-author surname found | verdict |
|---|---|---|---|---|
| P0013 | 26 | EXACT | True (Zhao) | DOCUMENT_VERIFIED |
| P0014 | 19 | EXACT | True (Zhang) | DOCUMENT_VERIFIED |
| P0015 | 18 | EXACT | True (Yan) | DOCUMENT_VERIFIED |
| P0016 | 18 | EXACT | True (Zhang) | DOCUMENT_VERIFIED |
| P0017 | 22 | EXACT | True (Chen) | DOCUMENT_VERIFIED |
| P0018 | 11 | EXACT | True (Huang) | DOCUMENT_VERIFIED |
| P0019 | 10 | EXACT | True (Sun) | DOCUMENT_VERIFIED |
| P0020 | n/a | n/a | None (Bahram) | PDF_MISSING |

Verification reads page 1 of the stored canonical PDF and requires both an exact title match
and the declared first-author surname to be present. Seven of eight records are
`DOCUMENT_VERIFIED`. P0020 has no document, so it stays `INDEX_BACKED` and its card says so.

## 5. Raw-MD QC

| paper_id | chars | headings | images copied/refs | mojibake | MinerU rc | seconds | qc |
|---|---|---|---|---|---|---|---|
| P0013 | 101,854 | 41 | 17/17 | 0 | 0 | 299.4 | RAW_MD_READY |
| P0014 | 65,924 | 26 | 11/11 | 0 | 0 | 181.1 | RAW_MD_READY |
| P0015 | 52,124 | 22 | 2/2 | 0 | 0 | 175.1 | RAW_MD_READY |
| P0016 | 64,659 | 38 | 4/4 | 0 | 0 | 184.3 | RAW_MD_READY |
| P0017 | 94,931 | 34 | 14/14 | 0 | 0 | 394.6 | RAW_MD_READY |
| P0018 | 61,809 | 22 | 9/9 | 0 | 0 | 214.0 | RAW_MD_READY |
| P0019 | 53,401 | 32 | 6/6 | 0 | 0 | 144.1 | RAW_MD_READY |
| P0020 | - | - | - | - | - | - | NOT CREATED (no canonical PDF) |

Gates applied to every conversion: title heading present, abstract present, headings present,
references present, length above the floor, mojibake ratio within tolerance, and every image
referenced by the raw MD present on disk. All seven conversions passed with zero mojibake and
no missing images; no record needed a second attempt in this batch. Raw MD is raw by design
and is not edited to improve scientific content, including the known MinerU hyphen-drop at
line breaks ("end-to-end" -> "endtoend"); the PDF remains the exact source authority.

## 6. Official code status and evidence basis

| paper_id | code_available | official_code_url | evidence basis |
|---|---|---|---|
| P0013 | UNKNOWN | (none stated) | UNKNOWN. The paper prints a PROJECT PAGE, https://vail-ucla.github.io/BridgeSim/ (p.1), not a repository URL; the discovery hint named a repo, but the paper does not state one, so officiality is not established. |
| P0014 | YES | https://github.com/Thinklab-SJTU/ReactSim-Bench | YES. The paper prints the repository URL https://github.com/Thinklab-SJTU/ReactSim-Bench on page 1, which is paper-source support for officiality. Reachability of the repository was NOT independently verified in this pass. |
| P0015 | UNKNOWN | (none stated) | UNKNOWN. No repository or project URL appears anywhere in the extracted PDF text; absence of a printed URL is not evidence that no code exists. |
| P0016 | UNKNOWN | (none stated) | UNKNOWN. No repository or project URL appears in the extracted PDF text. |
| P0017 | UNKNOWN | (none stated) | UNKNOWN. The paper prints a PROJECT PAGE, https://currychen77.github.io/CRAFT (p.1), not a repository URL. |
| P0018 | UNKNOWN | (none stated) | UNKNOWN. The paper prints a PROJECT PAGE, https://mczhi.github.io/GameFormer/ (p.1), not a repository URL. |
| P0019 | UNKNOWN | (none stated) | UNKNOWN. No repository or project URL appears in the extracted PDF text. |
| P0020 | UNKNOWN | (none stated) | UNKNOWN. No canonical PDF was acquired, so no document-level code statement could be read. |

Rule applied: `code_available=YES` only when the paper/project/author source itself supports
officiality. Repository-name pattern matching was not treated as evidence, no repository was
cloned, and repository reachability was not probed in this pass. A printed project page is
recorded in the card but leaves the field `UNKNOWN` rather than `YES`.

## 7. Download / conversion failures

1. **P0020 Bahram et al. 2016 - acquisition blocked (specific and lawful).** Status recorded
   verbatim as `DOWNLOAD_BLOCKED`, `source_version=none_available`: the DOI
   (`10.1109/TVT.2015.2508009`) resolves to the IEEE Xplore landing page (HTTP 202, HTML, not
   a PDF) and no lawful open version was found. Unofficial mirrors are excluded by the ingest
   prompt, so no PDF is stored and no raw MD could be produced.
2. **P0018 GameFormer - camera-ready URL not guessable.** Three pattern-derived full-title CVF
   slugs returned HTTP 404. Cause: CVF truncates the title inside its slug. Resolved by
   scanning the ICCV2023 Open Access index page for `GameFormer`, which yielded the working
   camera-ready PDF and its landing page.
3. **Web search was unavailable** for this session (the provider returned `Insufficient
   Balance`), so no URL was confirmed by a search engine. Every source decision above rests on
   direct HTTPS probes of the candidate URLs (status code plus `%PDF-` magic, TLS verified
   with the certifi bundle) or on an official index page. The delegated URL-verification
   subagent was stopped once these questions had been resolved locally, to avoid duplicated
   spend; its report therefore contributes nothing to this ingest.
4. **Conversions: none failed.** 7/7 acquired PDFs converted and passed QC. The two runs used
   reduced MinerU thread counts (render 2, max 4) and were executed sequentially rather than
   concurrently, because Batch 0A showed a resource peak that can kill the local MinerU API
   service; no such failure occurred here.
5. **Host filesystem-view flapping (environmental, not a data defect).** During this session
   the workspace intermittently reported existing files as missing to native/.NET and
   Python file APIs (for example a script that had just been patched). Every affected step
   was retried and re-verified; no artifact was written twice with different content and no
   ledger lost records. This is recorded because it explains why some steps were repeated.

## 8. Provenance conflicts

1. **P0018 canonical source changed mid-ingest.** The paper was first downloaded from arXiv
   (`arXiv:2303.05760`, https://arxiv.org/pdf/2303.05760, 2,348,946 bytes, sha256 `e7f71bda870dcf1e58ba5ffcecb013b01dcd2c6bc4cdaf726ce97ba9141a8db6`) and then superseded by the venue
   camera-ready, because venue camera-ready outranks a preprint under the corpus priority.
   The stored canonical PDF and every derived artifact come from the camera-ready; the
   superseded download is recorded here as the audit trail. Only one canonical PDF exists.
2. **BridgeSim repository hint vs paper text (unresolved, not denied).** The discovery index
   named a GitHub repository, but the paper itself prints only a project page. Under the
   official-code rule the record stays `UNKNOWN`; a later verification pass may upgrade it.
3. **A1-A5 venue status.** All five are arXiv preprints with no venue version verified in
   this pass. Their `source_version` is therefore `arXiv_v1`, and no camera-ready claim is
   made. If a venue version appears later, the canonical source must be re-acquired and the
   record re-verified rather than edited in place.
4. **Affiliation facts read from page 1 only.** First-author affiliations noted in the cards
   (Purdue / Bosch Center for AI for P0016; Tsinghua University / Li Auto for P0017) come
   from the papers' own front matter. Nothing was inferred from external sources.
5. **No title, author or acronym conflict was found** for A1-A5, H1 or H2: titles matched
   exactly and the declared first author was present in all seven documents.

## 9. Exact list of GitHub files added/updated

**Added**

- `papers/raw_md/P0013_BridgeSim/P0013_BridgeSim.raw.md`
- `papers/raw_md/P0013_BridgeSim/images/` (17 files)
- `papers/cards/P0013_BridgeSim.md`
- `papers/raw_md/P0014_ReactSimBench/P0014_ReactSimBench.raw.md`
- `papers/raw_md/P0014_ReactSimBench/images/` (11 files)
- `papers/cards/P0014_ReactSimBench.md`
- `papers/raw_md/P0015_CausalDrive/P0015_CausalDrive.raw.md`
- `papers/raw_md/P0015_CausalDrive/images/` (2 files)
- `papers/cards/P0015_CausalDrive.md`
- `papers/raw_md/P0016_CounterfactualPred/P0016_CounterfactualPred.raw.md`
- `papers/raw_md/P0016_CounterfactualPred/images/` (4 files)
- `papers/cards/P0016_CounterfactualPred.md`
- `papers/raw_md/P0017_CRAFT/P0017_CRAFT.raw.md`
- `papers/raw_md/P0017_CRAFT/images/` (14 files)
- `papers/cards/P0017_CRAFT.md`
- `papers/raw_md/P0018_GameFormer/P0018_GameFormer.raw.md`
- `papers/raw_md/P0018_GameFormer/images/` (9 files)
- `papers/cards/P0018_GameFormer.md`
- `papers/raw_md/P0019_M2I/P0019_M2I.raw.md`
- `papers/raw_md/P0019_M2I/images/` (6 files)
- `papers/cards/P0019_M2I.md`
- `papers/cards/P0020_Bahram2016.md`
- `experiment_logs/mineru_P0013.log`
- `experiment_logs/mineru_P0014.log`
- `experiment_logs/mineru_P0015.log`
- `experiment_logs/mineru_P0016.log`
- `experiment_logs/mineru_P0017.log`
- `experiment_logs/mineru_P0018.log`
- `experiment_logs/mineru_P0019.log`
- `manifests/batch_round2_download_results.json`
- `manifests/batch_round2_frontpage_verification.json`
- `manifests/batch_round2_rawmd_results.json`
- `scripts/build_round2_cards.py`
- `scripts/build_round2_report.py`
- `ROUND2_TARGETED_INGEST_REPORT.md` (this file)

**Updated**

- `manifests/CORPUS_MANIFEST.csv` (regenerated: 20 rows, 25 columns; the 12 Batch 0A rows are
  unchanged, and the batch ledgers are now merged rather than replaced)
- `scripts/fetch_canonical_pdfs.py` (Round 2 sources; batch-aware ledger path; merge-on-write)
- `scripts/verify_frontpage.py` (Round 2 expectations; batch-aware ledger; `--only` filter;
  merge-on-write)
- `scripts/build_raw_md.py` (Round 2 papers; batch-aware ledger; merge-on-write)
- `scripts/build_manifest.py` (Round 2 metadata; `ORDER` extended to 20; ledgers are now
  merged across batches so a targeted re-run cannot truncate another batch's provenance)

**Never pushed, by rule and by verification:** `papers/pdf/*.pdf` (gitignored, local/NAS
authority), `papers/quarantine/**` (MinerU intermediates), any checkpoint or dataset.

## Decision points for the owner

1. **`decision_relevance` is `MEDIUM` for all eight new records.** The schema reserves `HIGH`
   for adjudicated evidence (a kill/weaken, a direct observed failure, novelty occupation, a
   key counterexample, or a changed research decision). Nothing here has been deep-read, so
   marking any of them `HIGH` would assert relevance that has not been adjudicated. If the
   owner wants a different convention for the frozen target set, this is a one-line change
   plus a manifest regeneration.
2. **P0020 is unreadable as stored.** It stays `INDEX_BACKED` / `DISCOVERED` with no PDF and
   no raw MD, exactly like P0008 NPPC. Options are an authorised copy through the owner's
   institutional access, or accepting the record as permanently index-level.
3. **Card skeletons are infrastructure only.** Filling sections 1-12 and 14 is the deep-read
   task; the reading queue order was not changed by this ingest.

