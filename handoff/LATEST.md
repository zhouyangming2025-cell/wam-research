# LATEST — Handoff

Session: 2026-09-13 — Batch 0A ingestion + Integration Gate 0 staging.
Prepared by the corpus-librarian agent. This file states where things are and what is
blocked; it contains no scientific verdicts.

## New session read order

```text
1. state/CURRENT_STATE.md
2. state/DECISION_LOG.md
3. state/NEXT_TASK.md
4. handoff/LATEST.md          (this file)
then, as needed:
   hypotheses/<current>.md
   papers/cards/<relevant IDs>.md
```

Do not re-read the whole corpus by default.

## What exists now

- **Local/NAS corpus** (`D:\zym_information\ZYM\wam\research_assets\`): 12 papers
  registered in `manifests/CORPUS_MANIFEST.csv` (25 columns); 11 canonical PDFs in
  `papers/pdf/`; 11 MinerU raw MD + referenced images in
  `papers/raw_md/PXXXX_ShortName/`; all MinerU intermediates quarantined in
  `papers/quarantine/mineru_artifacts/`. Reports: `BATCH_0A_METADATA_REPORT.md`,
  `BATCH_0A_INGEST_REPORT.md`.
- **This repo** (`wam-research`, private): the text layer of the whole corpus — full
  manifest, all 11 raw MD + their figures, card skeletons (P0001/P0002/P0010), the
  Research Brain skeleton (`state/`, `hypotheses/`, `handoff/`), the ingest scripts,
  conversion logs and reports. Canonical PDFs and the 307 MB MinerU `quarantine/` tree
  are deliberately excluded (see `README.md`).

## Non-negotiable boundaries

- PDFs never leave local/NAS. The GitHub repo carries raw MD, cards, state — text only.
- All card verdict fields are `PENDING SCIENTIFIC REVIEW`. The agent does source
  extraction only; scientific judgement is the owner's.
- `pdf_sha256` / `raw_md_sha256` are SHA256 over logical document bytes via the
  canonical Python corpus I/O path. The Windows native/.NET +1024 framed view is a
  `KNOWN_HOST_QUIRK` — do not re-investigate, do not "fix" hashes with PowerShell.

## Open items (blockers on the owner)

1. **GitHub push decision** — target private repo URL + auth method. No credentials
   have been requested, stored or used. Push not attempted.
2. **P0008 NPPC** — unreadable from the corpus (paywalled). If a lawfully obtained PDF
   appears, hash it, verify the front page, convert it.
3. **Two confirmations from the Batch 0A ingest report** still stand: hash read-path
   authority is now fixed by ruling, but the "open the PDF in a Windows viewer" check
   was never performed; and the TOAD README-vs-abstract PDMS discrepancy (94.9 vs 94.7)
   is recorded, unadjudicated.

## Known host quirks to respect

- MinerU on this host must be launched through `scripts/run_mineru.py` with
  `MINERU_SANDBOX_SHIMS=1` and `PYTHONPATH` pointing at `scripts/_mineru_site/`
  (see `sitecustomize.py` for the four defects it works around); point
  `MINERU_TOOLS_CONFIG_JSON` at `D:\Program Files\Mineru\mineru.json` or it will try to
  download models and fail on HuggingFace locks.
- Any git HTTPS operation needs `-c http.sslBackend=openssl` (schannel is broken here).

## What is deliberately NOT started

Batch 0B (paused). Targeted Failure Deep Read (awaits owner scope). Any new scientific
analysis. Any hypothesis verdict.
