# wam-research

Cross-session knowledge base for the **planning-centric WAM failure landscape** project.
Text and figures only — no PDFs.

## What this repository is for

A new session (or ChatGPT) should be able to reconstruct the current research state, and
read the full text of every ingested paper, from this repo alone — without the PDFs and
without re-reading a local corpus.

## Read order

```text
1. state/CURRENT_STATE.md      hypothesis status + current stage + architecture in force
2. state/DECISION_LOG.md       decisions and their basis
3. state/NEXT_TASK.md          the single next task and its stop condition
4. handoff/LATEST.md           where everything is, what is blocked
then, as needed:
   hypotheses/<current>.md     e.g. hypotheses/P2R_PRIMARY.md
   papers/cards/<relevant>.md  per-paper skeletons
   papers/raw_md/<PXXXX>/<PXXXX>.raw.md   full paper text = primary reading layer
```

## Layout

```text
manifests/CORPUS_MANIFEST.csv     registry of all 12 ingested papers (25 columns)
manifests/batch_0a_*.json         Batch 0A evidence: downloads, front-page checks,
                                  raw-MD QC, code-URL probes, hyphen fidelity
papers/raw_md/<PXXXX_Short>/      MinerU raw Markdown + its images/  <-- primary text layer
papers/cards/*.md                 per-paper research cards (skeletons)
state/                            CURRENT_STATE, DECISION_LOG, NEXT_TASK, RESEARCH_LEDGER
hypotheses/                       P1_RETIRED, P2R_PRIMARY, P3_HOLD
handoff/LATEST.md                 session handoff
scripts/                          the ingestion/verification scripts that built this corpus
experiment_logs/                  MinerU conversion logs, one per paper
WAM_Corpus_Bootstrap_Pack/        the corpus operating contract (schema, naming, policies)
BATCH_0A_*.md                     ingest reports
INTEGRATION_GATE_0_STAGING_REPORT.md   gate record (see its header note on layout)
```

## What is deliberately NOT here

- **No PDFs.** Canonical PDFs live only on local/NAS and are never uploaded here or to any
  ChatGPT Library. This repo carries the text layer and the extracted figures.
- **No MinerU intermediates.** The `quarantine/` tree (per-paper `_origin.pdf`,
  `_layout.pdf`, `_span.pdf`, `_content_list.json`, `_middle.json`, `_model.json`) is
  regenerable and is never canonical — 307 MB of the local corpus that is intentionally
  excluded here.
- **No scientific verdicts.** All card verdict fields are `PENDING SCIENTIFIC REVIEW`.
  The agent produces source extraction; scientific judgement is the owner's.

## Current state (2026-09-13)

| slot | hypothesis | status |
|---|---|---|
| Primary candidate | P2R_PRIMARY — Reactive Action-Ordering Gap in Planning-centric WAMs | PRIMARY CANDIDATE, NOT CONFIRMED GAP |
| Backup | P3_HOLD — Decision Sufficiency of World Representations | HOLD AS BACKUP |
| Retired | P1_RETIRED — Planner-Induced Model Exploitation / Search-Support Gap | RETIRED AS MAIN PROBLEM |

Current stage: **Targeted Failure Deep Read** (not started).

## Corpus state

12 papers registered. 11 have a canonical PDF (local only) and a raw MD (here);
**P0008 (NPPC) is blocked** — paywalled, no open version, so no PDF and no raw MD exist.
Its manifest row is `library_status=NONE`, `reading_status=DISCOVERED`.

## Integrity

`pdf_sha256` / `raw_md_sha256` are SHA256 over the logical document bytes as read by the
canonical Python corpus I/O path. `.gitattributes` sets `* -text` so a Windows clone with
`core.autocrlf=true` cannot rewrite LF to CRLF and invalidate those hashes.

On the Windows host that built this corpus, native tooling (PowerShell / .NET / `certutil`)
sees a **+1024 framed representation** of the same files. That is a recorded
`KNOWN_HOST_QUIRK`, not corruption. Do not "correct" hashes with native tools.
