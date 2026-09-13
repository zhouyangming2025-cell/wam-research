# RESEARCH_LEDGER

Running factual ledger of assets and state transitions. No verdicts live here.

## Hypotheses

| hypothesis | status | definition | file |
|---|---|---|---|
| P1_RETIRED — Planner-Induced Model Exploitation / Search-Support Gap | RETIRED AS MAIN PROBLEM | prior formulation recorded for provenance | `hypotheses/P1_RETIRED.md` |
| P2R_PRIMARY — Reactive Action-Ordering Gap in Planning-centric WAMs | PRIMARY CANDIDATE, NOT CONFIRMED GAP | PENDING OWNER SUPPLY (name only) | `hypotheses/P2R_PRIMARY.md` |
| P3_HOLD — Decision Sufficiency of World Representations | HOLD AS BACKUP | PENDING OWNER SUPPLY (name only) | `hypotheses/P3_HOLD.md` |

## Corpus

| date | batch | papers | state |
|---|---|---|---|
| 2026-09-13 | Batch 0A | 12 registered (P0001–P0012) | 11 `RAW_MD_READY` (canonical PDF + raw MD, DOCUMENT_VERIFIED); P0008 blocked `PAYWALLED_NO_OPEN_SOURCE`; reports: `BATCH_0A_METADATA_REPORT.md`, `BATCH_0A_INGEST_REPORT.md` |

## Discovered, not ingested

| item | state |
|---|---|
| `论文\2602.06521v1.pdf` (DriveWorld-VLA) | `DISCOVERED_NOT_INGESTED`, target batch = Batch 1, **no Paper ID** (owner ruling) |

## Gates

| date | gate | content | status |
|---|---|---|---|
| 2026-09-13 | Integration Gate 0 | Full corpus text layer: manifest + all 11 raw MD + figures + scripts + logs + reports; card skeletons for P0001/P0002/P0010; Research Brain skeleton | local git repo prepared (190 files, 5.76 MB, 0 PDF, 0 quarantine artifacts); private target repo designated; awaiting authentication to push |

## Known host quirks

| quirk | status |
|---|---|
| Windows native/.NET reads of workspace files show a +1024 framed representation; the canonical Python corpus I/O path reads logical document bytes | `KNOWN_HOST_QUIRK` — hash authority fixed to the Python path; no further investigation (owner ruling 2026-09-13) |
| `tempfile.mkdtemp` directories become inaccessible/undeletable; named pipes denied (ProcessPoolExecutor unusable); MinerU resolves `mineru.json` by CWD | worked around in `scripts/_mineru_site/sitecustomize.py`; MinerU installation unmodified |
| git schannel TLS broken on this host | any GitHub HTTPS operation needs `-c http.sslBackend=openssl` |
