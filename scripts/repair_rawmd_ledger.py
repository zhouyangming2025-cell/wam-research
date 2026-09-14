"""Rebuild missing raw-MD ledger records from the artifacts already on disk.

Context: two `build_raw_md.py` processes ran concurrently for the census2 batch. Each read
the shared ledger once at start and wrote it back at the end, so the later finishing
process silently dropped the earlier one's six records. The raw MD files and their images
were never affected.

This tool reconstructs only the missing records, by calling the very same `qc()` function
from `build_raw_md` against the stored artifacts, and leaves existing records untouched.
Nothing is inferred: every field is recomputed from the file that is actually on disk.

Usage:
    CORPUS_BATCH=census2 python repair_rawmd_ledger.py
"""
from __future__ import annotations

import glob
import json
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "scripts"))

import build_raw_md as brm  # noqa: E402  (same qc() that produced the original records)

BATCH = os.environ.get("CORPUS_BATCH", "census2")
OUT = os.path.join(BASE, "manifests", f"batch_{BATCH}_rawmd_results.json")
NEW = [f"P{i:04d}" for i in range(21, 35)]
SHORT = dict((p, s) for p, s in brm.PAPERS)


def rebuild(pid: str) -> dict | None:
    short = SHORT.get(pid)
    if not short:
        return None
    hits = glob.glob(os.path.join(BASE, "papers", "raw_md", f"{pid}_*", f"{pid}_*.raw.md"))
    if not hits:
        return None
    dest_md = max(hits, key=os.path.getsize)
    dest_dir = os.path.dirname(dest_md)
    img_dir = os.path.join(dest_dir, "images")
    text = open(dest_md, encoding="utf-8", errors="replace").read()

    rec = dict(paper_id=pid, short_name=short)
    rec.update(brm.qc(text, dest_md, img_dir))
    rec["raw_md_local_path"] = dest_md
    rec["raw_md_sha256"] = brm.sha256_of(dest_md) if rec["qc"] == "RAW_MD_READY" else None
    rec["images_copied"] = len([f for f in os.listdir(img_dir)]) if os.path.isdir(img_dir) else 0
    stage = os.path.join(BASE, "papers", "quarantine", "mineru_artifacts", f"{pid}_{short}")
    rec["source_md"] = brm.find_md(stage) if os.path.isdir(stage) else None
    rec["rebuilt_from_artifacts"] = True
    return rec


def main() -> int:
    existing = []
    if os.path.exists(OUT):
        with open(OUT, encoding="utf-8") as fh:
            existing = json.load(fh)
    have = {r["paper_id"] for r in existing}
    print(f"ledger records before: {len(existing)}  -> {sorted(have)}")

    added = []
    for pid in NEW:
        if pid in have:
            continue
        rec = rebuild(pid)
        if rec:
            added.append(rec)
            print(f"  rebuilt {pid} {rec['short_name']}: {rec['qc']} "
                  f"chars={rec['length_chars']} headings={rec['heading_count']} "
                  f"imgs={rec['images_copied']}/{rec['image_refs_in_md']} "
                  f"mojibake={rec['mojibake_total']}")
        else:
            print(f"  {pid}: no artifact found, record NOT rebuilt")

    merged = {r["paper_id"]: r for r in existing}
    for rec in added:
        merged[rec["paper_id"]] = rec
    ordered = [merged[pid] for pid, _s in brm.PAPERS if pid in merged]

    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(ordered, fh, indent=2, ensure_ascii=False)

    census2 = [r for r in ordered if r["paper_id"] >= "P0021"]
    bad = [r["paper_id"] for r in census2 if r.get("qc") != "RAW_MD_READY"]
    print(f"\nledger records after: {len(ordered)}  census2={len(census2)}  not-ready={bad or 'none'}")
    print(f"-> {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
