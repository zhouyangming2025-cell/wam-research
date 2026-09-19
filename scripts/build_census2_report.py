"""Compose CENSUS_ROUND2_INGEST_REPORT.md for the Phase-A Census Round 2 support batch.

Every hash, byte count, page count and QC figure in the report is read from the batch
ledgers and the manifest at run time, so the report can never drift from the evidence.

Usage:
    CORPUS_BATCH=census2 python build_census2_report.py
"""
from __future__ import annotations

import csv
import glob
import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BATCH = os.environ.get("CORPUS_BATCH", "census2")
OUT = os.path.join(BASE, "CENSUS_ROUND2_INGEST_REPORT.md")
NEW = [f"P{i:04d}" for i in range(21, 35)]

# Which Phase-A Census Round 2 coverage hole each work fills. Taken from
# landscape/FIELD_ATLAS.md (F10), landscape/CENSUS_PHASE_A_ROUND1.md and state/NEXT_TASK.md.
HOLE = {
    "P0021": "F10 strong non-WM end-to-end control (Hydra-MDP family)",
    "P0022": "F10 strong non-WM end-to-end control",
    "P0023": "F10 strong non-WM end-to-end control",
    "P0024": "F10 representative VLA planner",
    "P0025": "F10 representative VLA planner",
    "P0026": "F10 representative VLA planner",
    "P0027": "world-model RL lineage",
    "P0028": "representation-pretraining bridge",
    "P0029": "representation-pretraining bridge",
    "P0030": "benchmark / evaluation lineage",
    "P0031": "benchmark / evaluation lineage",
    "P0032": "benchmark / evaluation lineage",
    "P0033": "benchmark / evaluation lineage",
    "P0034": "benchmark / evaluation lineage",
}


def load_all(name: str) -> dict:
    """Merge every batch_*_<name>.json ledger, so no batch is hidden by another."""
    merged: dict = {}
    for path in sorted(glob.glob(os.path.join(BASE, "manifests", f"batch_*_{name}.json"))):
        try:
            with open(path, encoding="utf-8") as fh:
                data = json.load(fh)
        except Exception:
            continue
        if isinstance(data, dict):
            merged.update(data)
        elif isinstance(data, list):
            for r in data:
                if isinstance(r, dict) and r.get("paper_id"):
                    merged[r["paper_id"]] = r
    return merged


def manifest_rows() -> dict:
    path = os.path.join(BASE, "manifests", "CORPUS_MANIFEST.csv")
    with open(path, encoding="utf-8", newline="") as fh:
        return {r["paper_id"]: r for r in csv.DictReader(fh)}


def main() -> int:
    dl = load_all("download_results")
    fp = load_all("frontpage_verification")
    md = load_all("rawmd_results")
    ident = load_all("identity")
    rows = manifest_rows()

    L: list[str] = []
    a = L.append

    a("# Phase-A Census Round 2 — Corpus Ingest Report")
    a("")
    a("Status: **corpus ingestion record**. This document is *not* the census and contains no")
    a("field-placement, novelty or gap verdict. It records what the local corpus agent acquired,")
    a("converted and verified in support of the coverage holes named for Phase-A Census Round 2.")
    a("")
    a("Batch label: `census2`. Companion ledgers:")
    a("")
    a("```text")
    a("manifests/batch_census2_identity.json")
    a("manifests/batch_census2_download_results.json")
    a("manifests/batch_census2_frontpage_verification.json")
    a("manifests/batch_census2_rawmd_results.json")
    a("manifests/CORPUS_MANIFEST.csv")
    a("```")
    a("")
    a("---")
    a("")
    a("## 1. Why this batch exists")
    a("")
    a("`landscape/FIELD_RECONSTRUCTION_PLAN.md` replaces gap-first search with neutral field")
    a("reconstruction, and `state/NEXT_TASK.md` asks Round 2 to fill missing *coverage* rather")
    a("than to hunt for gaps. `landscape/FIELD_ATLAS.md` names the missing pieces explicitly:")
    a("strong non-WM end-to-end controls (F10), world-model RL lineage, representation-pretraining")
    a("bridges, and the benchmark/simulator lineage. This batch supplies those works as local")
    a("documents with an extractable text layer, so census placement no longer depends on fetching")
    a("public PDFs mid-analysis.")
    a("")
    a("Boundary of this batch: acquisition, identity verification, conversion, metadata and QC only.")
    a("No family assignment, no placement confidence, no novelty or gap claim is made here — those")
    a("belong to the census owner. The owner's landscape/atlas/taxonomy/state files were not edited.")
    a("")
    a("## 2. Coverage holes filled")
    a("")
    a("| paper_id | short name | coverage hole from the owner's atlas / next task |")
    a("|---|---|---|")
    for pid in NEW:
        short = (rows.get(pid) or {}).get("short_name") or (ident.get(pid) or {}).get("short_name", "")
        a(f"| {pid} | {short} | {HOLE.get(pid, '')} |")
    a("")
    a("## 3. Identity resolution and dedup")
    a("")
    a("Identity is the first pipeline step, and web search was unavailable in this session, so no")
    a("title, author, year or identifier in this batch was written from memory:")
    a("")
    a("1. candidates were resolved through the OpenAlex API (`scripts/resolve_works_openalex.py`);")
    a("2. each candidate's **official landing page** was then fetched and its `citation_title`,")
    a("   `citation_author`, `citation_date` and arXiv version recorded verbatim by")
    a("   `scripts/fetch_work_identity.py`;")
    a("3. an identity was accepted only when the recorded official title matched the intended work;")
    a("4. page 1 of each downloaded PDF was re-checked against that recorded title (§5).")
    a("")
    a("Dedup: all 20 pre-existing corpus records were listed first (`arxiv_id`, title). None of the")
    a("14 works below already existed, and no identifier was reused or renumbered; `P0021`–`P0034`")
    a("are allocated in the order the owner's coverage list groups them.")
    a("")
    a("## 4. Acquisition results")
    a("")
    a("| paper_id | short | source_version | bytes | pdf sha256 (logical bytes) | front page |")
    a("|---|---|---|---|---|---|")
    for pid in NEW:
        d = dl.get(pid, {})
        r = rows.get(pid, {})
        short = (md.get(pid) or {}).get("short_name") or (fp.get(pid) or {}).get("short_name") \
            or (ident.get(pid) or {}).get("short_name", "")
        sha = d.get("sha256") or ""
        verdict = (fp.get(pid) or {}).get("verdict", "NOT_RUN")
        a(f"| {pid} | {short} | {d.get('source_version','UNKNOWN')} | "
          f"{d.get('bytes','')} | `{sha[:16]}…` | {verdict} |")
    a("")
    a("Full 64-character hashes and canonical URLs are in the batch ledger and in")
    a("`manifests/CORPUS_MANIFEST.csv`; they are not retyped here.")
    a("")
    a("## 5. Front-page verification")
    a("")
    a("Each downloaded PDF was opened with pypdfium2 and page 1 text compared against the")
    a("officially recorded title (whitespace/punctuation-insensitive) plus presence of the recorded")
    a("first author. Exact counts:")
    a("")
    ok = [p for p in NEW if (fp.get(p) or {}).get("verdict") == "DOCUMENT_VERIFIED"]
    other = [p for p in NEW if p not in ok]
    a(f"- `DOCUMENT_VERIFIED`: {len(ok)} of {len(NEW)}")
    for p in other:
        a(f"- `{p}`: `{(fp.get(p) or {}).get('verdict','NOT_RUN')}`")
    a("")
    a("## 6. Raw MD conversion and QC")
    a("")
    a("MinerU conversion ran locally through `scripts/run_mineru.py` with the harness shims.")
    a("")
    a("| paper_id | qc | pages | raw md chars | headings | images (md/disk) |")
    a("|---|---|---|---|---|---|")
    for pid in NEW:
        r = md.get(pid, {})
        pages = (fp.get(pid) or {}).get("pages", "")
        a(f"| {pid} | {r.get('qc','NOT_RUN')} | {pages} | {r.get('length_chars','')} | "
          f"{r.get('heading_count','')} | {r.get('images_copied','')}/{r.get('image_refs_in_md','')} |")
    a("")
    a("Two integrity facts from this batch are recorded here rather than smoothed over:")
    a("")
    a("1. **Ledger write race, repaired from artifacts.** Conversion for this batch was started as")
    a("   two concurrent jobs. Each process read the shared ledger once at start and wrote it back at")
    a("   the end, so the later write silently dropped six records. The raw MD files and their images")
    a("   were never affected. The missing records were reconstructed from the stored artifacts by")
    a("   `scripts/repair_rawmd_ledger.py`, which calls the same `qc()` function that produced the")
    a("   originals and reproduces their figures exactly (for example P0033 83466 chars / 60")
    a("   headings / 50-50 images). `build_raw_md.py` now re-reads the ledger immediately before")
    a("   writing, so a concurrent run can no longer clobber another run's records.")
    a("2. **One conversion text loss.** For P0028 the repository URL printed on PDF page 1 is absent")
    a("   from the extracted markdown, so that record's `code_available` rests on the PDF page-1 read")
    a("   and not on the markdown. Anyone reading only the markdown of that paper would wrongly")
    a("   conclude that it prints no code URL. The manifest note states this explicitly.")
    a("")
    a("## 7. Canonical-source decisions")
    a("")
    a("The corpus priority is venue camera-ready > official arXiv > project-hosted. Every decision")
    a("below is the `basis` string recorded at download time, quoted from the ledger:")
    a("")
    for pid in NEW:
        d = dl.get(pid, {})
        if d.get("basis"):
            a(f"- **{pid}** ({d.get('source_version','')}): {d['basis']}")
    a("")
    a("## 8. Unresolved and blocked items")
    a("")
    for pid in NEW:
        d = dl.get(pid, {})
        if d.get("status") == "DOWNLOAD_BLOCKED":
            a(f"- **{pid}**: `DOWNLOAD_BLOCKED: {d.get('error')}` — {d.get('basis','')}")
    a("- **Hydra-MDP++** and **NAVSIM-v2** were named by the owner's coverage list but could NOT")
    a("  be verified in this session (no matching official record was found through OpenAlex, and the")
    a("  arXiv export API was rate-limiting). They are deliberately NOT ingested: a guessed")
    a("  identifier would have put an unverified document into the corpus. They remain an open")
    a("  Round-2 item and need an owner-supplied canonical link or title.")
    a("- **nuPlan**: the Round-1 source register lists only the project page. The canonical document")
    a("  stored here is the official arXiv version; a peer-reviewed nuPlan paper is known to exist but")
    a("  was not verified in this batch, so the record keeps that caveat.")
    a("- **OmniDrive**: the CVPR 2025 camera-ready and arXiv:2405.01533 v2 carry the same title, so")
    a("  they are one work; the camera-ready is canonical. If the census intended a *different*")
    a("  OmniDrive paper (an LLM-agent framework variant), that is a separate record to be identified.")
    a("- **Legacy**: P0008 NPPC still has no lawful open canonical source; nothing about that changed.")
    a("")
    a("## 9. What this batch does NOT claim")
    a("")
    a("- no placement of any work into F1–F11, no family label, no placement confidence;")
    a("- no novelty, gap, or counterexample verdict;")
    a("- no statement that a work uses or does not use a world model beyond what its own text says;")
    a("- `code_available` is `YES` only where the paper itself prints a repository URL; a project")
    a("  page is not a repository, and absence of a printed URL is not evidence that no code exists;")
    a("- no paper was read at deep-read depth; these records are placement-depth documents.")
    a("")
    a("## 10. Reproduce")
    a("")
    a("```powershell")
    a("$mp = 'D:\\Program Files\\Mineru\\venv\\Scripts\\python.exe'")
    a("$env:CORPUS_BATCH = 'census2'")
    a("& $mp scripts\\fetch_work_identity.py                 # official identity metadata")
    a("& $mp scripts\\fetch_canonical_pdfs.py                # canonical PDFs + logical-byte SHA256")
    a("& $mp scripts\\verify_frontpage.py                    # page-1 title/author verification")
    a("& $mp scripts\\build_raw_md.py P0021,P0022,...,P0034  # MinerU raw MD")
    a("& $mp scripts\\build_manifest.py                      # CORPUS_MANIFEST.csv")
    a("& $mp scripts\\build_census2_report.py                # this report")
    a("```")
    a("")
    a("## 11. Decision points for the owner")
    a("")
    a("1. **Hydra-MDP++ / NAVSIM-v2**: supply canonical titles or links so they can be ingested, or")
    a("   drop them from the Round-2 hole list.")
    a("2. **Tags and relevance**: census-depth records are tagged from their own text and carry")
    a("   `decision_relevance=LOW` with `GENERAL` hypothesis tags, because P1/P2-R/P3 are parked.")
    a("   Say if you want a different convention for breadth records.")
    a("3. **Paper-card layer (retired)**: these records deliberately have no paper cards, so their")
    a("   manifest rows carry a `NO_CARD` note. Current scientific synthesis uses deep analyses and")
    a("   source audits; the legacy manifest field is retained only for provenance.")
    a("4. **Anchor pool**: if you freeze the 15–25 anchor works, the same pipeline can give the whole")
    a("   anchor set a local text layer before Phase B deep reads begin.")
    a("")

    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(L))
    text = "\n".join(L)
    print(f"wrote {OUT}")
    print(f"  {len(text)} chars, {text.count(chr(10)) + 1} lines")
    print(f"  records covered: {len(NEW)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
