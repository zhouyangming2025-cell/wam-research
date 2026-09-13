# INTEGRATION GATE 0 — STAGING REPORT

> **AMENDMENT 2026-09-13 - repository root relocated.** The push target is now the corpus
> root itself (`D:\zym_information\ZYM\wam\research_assets`), with `.gitignore` excluding
> `papers/pdf/`, `papers/quarantine/`, `github_staging/` and `_diag/`. References below to
> `github_staging/gate_0/` as "the repository" describe the earlier staging layout and are
> kept as history. Current state: single commit, 191 tracked files, working tree clean, no
> PDFs and no MinerU intermediates tracked. All 11 raw MD were re-verified natively against
> `manifests/CORPUS_MANIFEST.csv` (11/11 SHA256 match). The 11 `experiment_logs/*.log` files
> are force-included because the host global gitignore (`*.log`) silently drops them.

> **LAYOUT NOTE — added 2026-09-13 after this report was written.** Gate 0 was
> subsequently expanded to the **full corpus text layer** (owner decision: text layer
> only, private repo), so the repo now mirrors the local corpus's text structure:
> `manifests/`, `papers/raw_md/<PXXXX_Short>/`, `papers/cards/`, `scripts/`,
> `experiment_logs/`, `WAM_Corpus_Bootstrap_Pack/`, `state/`, `hypotheses/`, `handoff/`.
> The `corpus/` staging layout described below no longer exists: `CORPUS_MANIFEST.csv`
> now lives at `manifests/CORPUS_MANIFEST.csv`, and each raw MD keeps its per-paper
> directory together with its `images/` (which also fixes the unresolvable figure
> references noted in §4 below).
>
> Consequence for §2: the **manifest and raw-MD hashes remain valid** (same bytes), and
> the same files are now at the new paths. The hashes of the *documentation* files
> (README, cards, `state/`, `hypotheses/`, `handoff/`) are from the moment of the
> original staging and have since changed, because those files were revised to describe
> the new layout. Current hashes for every file in this repo are recorded in
> `manifests/repo_file_inventory.json`. See `README.md` for the live layout.

**Scope executed**: Integration Gate 0 only — P0001 (Epona), P0002 (SafeDrive), P0010 (TOAD).
Batch 0B: **paused, not started**. New scientific analysis: **none**.
**Date**: 2026-09-13.
**Rulings in force**: the nine-point long-term architecture ruling of 2026-09-13 (PDF locality,
raw MD as GPT-readable text layer, GitHub private repo as cross-session layer, ChatGPT Library
as optional convenience copy only, hash authority = canonical Python corpus I/O,
+1024 framed view = KNOWN_HOST_QUIRK, on-demand source extracts, agent = source extraction
not scientific judgement) plus the hypothesis status reset
(P1_RETIRED / P2R_PRIMARY / P3_HOLD as stated by the owner).

---

## 1. Staging location and layout

Staging root (local, mirrors the intended GitHub private repo root):

```
D:\zym_information\ZYM\wam\research_assets\github_staging\gate_0\   <-- local git repo, branch main
├── .gitattributes                 (EOL pinning so recorded hashes reproduce)
├── README.md                      (orientation + read order for a new session / ChatGPT)
├── corpus\
│   ├── CORPUS_MANIFEST.csv
│   └── raw_md\
│       ├── P0001_Epona.raw.md
│       ├── P0002_SafeDrive.raw.md
│       └── P0010_TOAD.raw.md
├── papers\cards\
│   ├── P0001_Epona.md
│   ├── P0002_SafeDrive.md
│   └── P0010_TOAD.md
├── state\
│   ├── CURRENT_STATE.md
│   ├── DECISION_LOG.md
│   ├── NEXT_TASK.md
│   └── RESEARCH_LEDGER.md
├── hypotheses\
│   ├── P1_RETIRED.md
│   ├── P2R_PRIMARY.md
│   └── P3_HOLD.md
└── handoff\
    └── LATEST.md
```

17 tracked files, all text (`.csv` / `.md`, plus `.gitattributes`). **No PDF is staged** —
consistent with the ruling that canonical PDFs stay on local/NAS and never cross to GitHub
or ChatGPT Library. Total repo size 337 KB (the local corpus is 402 MB, of which 89 MB is
PDF that must never be uploaded).

`README.md` and `.gitattributes` were added after the initial staging spec, to serve the
stated purpose (ChatGPT reading this repo) and to protect the recorded hashes. Both are
text, neither carries a scientific claim. `.gitattributes` sets `* -text` so a Windows
clone with `core.autocrlf=true` cannot rewrite LF to CRLF and invalidate every hash in
§2.

---

## 2. Staging files, sizes, hashes

All hashes are SHA256 over logical file bytes via the canonical Python corpus I/O path
(ruling #6). The Windows native/.NET view of these files differs by the +1024 framed
representation; that is the recorded `KNOWN_HOST_QUIRK` and is not a defect of these files.

| path (repo-relative) | bytes | sha256 |
|---|---|---|
| `corpus/CORPUS_MANIFEST.csv` | 14,635 | `9779f1a110dad0df4f43e4dcf1928c8477d667029fef748ca128d65e715d7dfd` |
| `corpus/raw_md/P0001_Epona.raw.md` | 56,690 | `f7593ab5881b11446ba6d90bb6e48ffc0c2c17375a775039d7d7442ec059e8e6` |
| `corpus/raw_md/P0002_SafeDrive.raw.md` | 49,745 | `99a404b8d541484c28a515f9dd63997baf664fa00bb6f29b5c339ad61d074b99` |
| `corpus/raw_md/P0010_TOAD.raw.md` | 70,491 | `d15e5a52a3f7bdb13ef745aa39522521227b33fd3449675c0857fb1cdf0dd25c` |
| `papers/cards/P0001_Epona.md` | 2,364 | `0e837bf6529577e7b0e894eda01178e570a1bc5282382a6ad9af44699e5fdea2` |
| `papers/cards/P0002_SafeDrive.md` | 2,418 | `6226039795a3a6c6f7f7471a26cdf644d6a5eb4991d68b37cc1d3df045d08027` |
| `papers/cards/P0010_TOAD.md` | 2,571 | `bf49d3ca0d1c7d111cda3d2d8f012df241e0ce09623242dc95fe22d96cbe22d2` |
| `state/CURRENT_STATE.md` | 2,518 | `8c8d7dd6a15a082b8df0102cea4562096a528486bc3b19b5ede847c84be4f5f5` |
| `state/DECISION_LOG.md` | 2,688 | `874d06b075b152391b4ba9699fe27e306e52a9a2b55c38f777b8158430a82cb0` |
| `state/NEXT_TASK.md` | 789 | `526999e1096ce86162906a5fc390f7ab92c7f40e18a13419bfaac29b70804721` |
| `state/RESEARCH_LEDGER.md` | 2,076 | `2c944d3ee7c0f39c8d1285693537348704dce5656cfb898559c7203161146333` |
| `hypotheses/P1_RETIRED.md` | 1,586 | `24f491232f9a81766fe98fc51e8797c03f5b8e169208990cdae69c67bd290e8e` |
| `hypotheses/P2R_PRIMARY.md` | 1,018 | `5cdadc85ace69f2ec0435bb783244b2e050d65f3e30417c4d599e12a69f0a393` |
| `hypotheses/P3_HOLD.md` | 792 | `bf9c50b0a68ad1538889060f53e41e679f74f8ed90df5dda2e9488e3254f3d2b` |
| `handoff/LATEST.md` | 2,930 | `2c42f4a7c47388c81c05b365bdbe4fbb65eb000caac2a95983499a1516fff465` |
| `README.md` | 2,655 | `7a1d9eb0e51f9bfb4ad1830beefe78dd5d26e25a18ff0bcf00f1e910af20aa04` |
| `.gitattributes` | 358 | `f64014f8e6e7dd983f0bf9e145afc243a4c0810542c0e4328d116cad7dd2b2fb` |

(The last two rows were added after the initial staging spec; see §1.)

### Integrity cross-checks (all performed, all pass)

1. **Staged raw MD = corpus raw MD.** Each staged `.raw.md` hash equals the
   `raw_md_sha256` recorded in `CORPUS_MANIFEST.csv` (3/3 exact match).
2. **Staged manifest = corpus manifest.** `corpus/CORPUS_MANIFEST.csv` is byte-identical
   to `manifests/CORPUS_MANIFEST.csv` (same SHA256, 14,635 B, 12 rows × 25 columns).
3. **Cards embed the right hashes.** Each card's Section 13 contains the same
   `pdf_sha256` and `raw_md_sha256` as the manifest row (3/3 verified for both fields).

---

## 3. What each staged artifact is

- **`corpus/CORPUS_MANIFEST.csv`** — the full corpus registry, all 12 papers
  (11 `RAW_MD_READY`, P0008 blocked). Staged whole rather than as a 3-row subset so the
  repo carries one registry, not a second truncated truth. Its `pdf_local_path` /
  `raw_md_local_path` fields are local/NAS paths by design; the repo's
  `corpus/raw_md/` is the cross-session copy for the three gated papers.
- **`corpus/raw_md/*.raw.md`** — MinerU raw Markdown, byte-identical to the local corpus
  files, renamed only. These are the GPT-readable primary-text layer (ruling #3/#4).
- **`papers/cards/*.md`** — NEW skeletons built on
  `WAM_Corpus_Bootstrap_Pack/05_PAPER_CARD_TEMPLATE.md`. Metadata + Section 13
  (source locations, hashes) are filled; **every analytical section carries
  `PENDING SCIENTIFIC REVIEW`**. None of the five forbidden verdicts
  (observed failure / counterevidence / hypothesis impact / prior-art occupancy /
  research verdict) was generated.
- **`state/`, `hypotheses/`, `handoff/`** — NEW Research Brain skeletons. The three
  hypothesis statuses are written **verbatim** from the owner ruling:
  P1_RETIRED `RETIRED AS MAIN PROBLEM`;
  P2R_PRIMARY `PRIMARY CANDIDATE, NOT CONFIRMED GAP`, stage `Targeted Failure Deep Read`;
  P3_HOLD `HOLD AS BACKUP`.
  P1's prior formulation is quoted for provenance only, explicitly labelled superseded;
  P2R/P3 definitions are `PENDING OWNER SUPPLY` because only names were given — the agent
  does not invent definitions.
  A provenance note records that
  `论文调研/P1_Agent_Bootstrap_Pack/01_RESEARCH_CONTEXT.md` (P1 as primary, "P1 — SURVIVES")
  is superseded by the 2026-09-13 ruling.

---

## 4. Missing items

| item | status | why |
|---|---|---|
| Raw MD of the other 9 papers | not staged | Gate 0 scope is P0001/P0002/P0010 only. All 9 exist locally and are one copy command away when a later gate asks. |
| `images/` for the staged raw MDs | not staged | Not in the specified staging layout. Measured consequence: the 3 staged raw MDs contain 27 image references (11 + 5 + 11), **0 resolvable inside the flat staging tree**. Acceptable under ruling #8: figures/exact content are obtained as on-demand source extracts from the local canonical PDF. If you want figures readable in-repo, the alternative is `corpus/raw_md/<stem>/images/` per paper — say so and I will restage. |
| P0008 NPPC | not in Gate 0, and unreadable | Paywalled (IEEE Xplore 11393633), no open version; no canonical PDF exists locally. |
| P2R_PRIMARY / P3_HOLD definition bodies | `PENDING OWNER SUPPLY` | Only hypothesis names were provided; inventing definitions would be scientific judgement, which is excluded. |
| LICENSE / .gitignore | absent | A private research repo needs neither yet. `README.md` and `.gitattributes` were added after the spec — see §1. |
| The two Batch 0A reports (`BATCH_0A_METADATA_REPORT.md`, `BATCH_0A_INGEST_REPORT.md`) | not staged | Kept the repo lean; `state/` and `handoff/LATEST.md` carry the operative summary. Stage on request. |

---

## 5. GitHub write readiness

**Content: READY. Local repository: prepared and committed. Write path: blocked on
authentication only. No push attempted.**

Target designated by the owner: `https://github.com/zhouyangming2025-cell/wam-research`.

Verified facts:

- Staging tree is complete, hashed, and cross-checked (§2). Nothing in it is a PDF.
- `github_staging/gate_0/` **is now a local git repository**: branch `main`, two commits
  (`3868565` initial gate content, `85529e8` EOL pinning), remote `origin` set to the
  target URL above, 17 tracked files, working tree clean, **0 PDF tracked** (checked).
  (`D:\zym_information\ZYM\wam\research_assets` itself remains a non-repo; only the
  staging directory is a repo, which is correct — the corpus folder holds the PDFs.)
- **TLS transport verified working**: `git -c http.sslBackend=openssl ls-remote
  https://github.com/git/git HEAD` returned `47ce80527c56f462cb97db4ca8125342204d3783`.
  The host's default schannel backend is broken, so the `openssl` backend is mandatory
  for every HTTPS remote operation.
- **Target repo state undetermined**: unauthenticated `https://github.com/.../wam-research`
  returns **HTTP 404** while the account page returns 200. GitHub returns 404 for private
  repos to unauthenticated callers, so this is "not created yet" **or** "already private" —
  indistinguishable without credentials.
- **No credentials available in this environment**: `gh` CLI is not installed; Git
  Credential Manager is configured
  (`D:\PortableGit\mingw64\bin\git-credential-manager.exe`) but Windows Credential Manager
  holds **no** `github.com` entry (`cmdkey /list` shows none). No GitHub credential has
  been requested, stored or used at any point.
- git 2.47.1.windows.1; global identity already set (`zhouyangming` /
  `h-zhouyangming@voyah.com.cn`), so the commits carry a real author.

Remaining step is **authentication only** — the content and the local repo are done. Two
owner-side options:

1. **Owner pushes (recommended, no secret ever enters this session).** Run in a normal
   terminal on this machine, from the staging directory:
   ```
   cd D:\zym_information\ZYM\wam\research_assets\github_staging\gate_0
   git -c http.sslBackend=openssl push -u origin main
   ```
   Git Credential Manager opens a browser sign-in on first use; nothing must be pasted
   into chat. If the remote repo was created *with* a README, run
   `git -c http.sslBackend=openssl pull --rebase origin main` first.
2. **Agent pushes** — requires a credential to reach this session. This means pasting a
   token into the conversation, where it becomes part of the transcript; that is a real
   exposure and I do not recommend it. If chosen, use a fine-grained token scoped to this
   one repository with `Contents: Read and write`, and revoke it immediately after.

Post-push verification (the gate's acceptance check): read the repo tree back and re-hash
the **17** files; all must match §2 exactly. Note that `.gitattributes` now guarantees
byte-identical checkouts, so the recorded hashes reproduce on any platform.

---

## 6. Boundaries respected in this gate

- Batch 0B: not started.
- New scientific analysis: none. No hypothesis verdict, no evidence weighing, no
  carry-over of P1's historical evidence into P2R_PRIMARY.
- All five verdict fields in all three cards: `PENDING SCIENTIFIC REVIEW`.
- PDFs: none uploaded, none staged, none hashed into any cloud-bound artifact.
- Upstream trees (`论文调研`, `workspace`, MinerU installation): read-only, untouched.
- Undeletable quarantine leftovers from Batch 0A remain recorded as-is; nothing was
  force-deleted.

**Stopping here as instructed.**
