"""Plan the acquisition of every Phase-A Census Round 1 work that lacks a local text layer.

This is the acquisition planner, not a note-taker. It reads the owner's census and source
register mechanically, subtracts what the corpus already has, and then proposes a canonical
source per remaining work using the corpus priority:

    venue camera-ready (CVF / ECVA / NeurIPS / ICLR page -> PDF)
    > official arXiv version
    > project-hosted

CVF PDFs are derived from the camera-ready path layout. ECVA, NeurIPS and ICLR pages are
fetched once and their PDF link is extracted. A work whose register entry offers only a
project page, a repository or a DOI is reported as NEEDS_RESOLUTION instead of being guessed.

Output:
    manifests/census_round1_acquisition_plan.json   (the plan, merge-on-write per work)
and a table on stdout for review.

Usage:
    python plan_census_acquisition.py
"""
from __future__ import annotations

import csv
import html as htmllib
import json
import os
import re
import ssl
import time
import urllib.request

import certifi

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CENSUS = os.path.join(BASE, "landscape", "CENSUS_PHASE_A_ROUND1.md")
SOURCES = os.path.join(BASE, "landscape", "CENSUS_PHASE_A_ROUND1_SOURCES.md")
MANIFEST = os.path.join(BASE, "manifests", "CORPUS_MANIFEST.csv")
OUT = os.path.join(BASE, "manifests", "census_round1_acquisition_plan.json")


def key(name: str) -> str:
    """Stable short key for a work name.

    The census writes titles as `GAIA-1: A Generative ...` (colon attached to the word) while
    the register writes the bare name `GAIA-1`, so the separator must be matched whether or
    not it is surrounded by spaces. Both sides then reduce to the same key.
    """
    n = name.lower()
    n = re.sub(r"\(.*?\)", " ", n)
    n = re.split(r"\s*[—–:/]\s*|\s+-\s+", n)[0]
    n = re.sub(r"[^a-z0-9]+", "", n)
    return n[:16]


def placed_works() -> list[str]:
    works, seen = [], set()
    with open(CENSUS, encoding="utf-8") as fh:
        for line in fh:
            if not line.startswith("|"):
                continue
            cells = line.split("|")
            if len(cells) < 2:
                continue
            m = re.match(r"\*\*(.+?)\*\*", cells[1].strip())
            if not m:
                continue
            name = " ".join(m.group(1).split())
            if name.lower() in ("work", "paper", "title") or key(name) in seen:
                continue
            seen.add(key(name))
            works.append(name)
    return works


def register_entries() -> dict[str, tuple[str, list[str]]]:
    out: dict[str, tuple[str, list[str]]] = {}
    with open(SOURCES, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line.startswith("- "):
                continue
            body = line[2:]
            name = re.split(r"\s+[—–]\s+", body, maxsplit=1)[0].strip()
            urls = [u.rstrip(".,;") for u in re.findall(r"https?://[^\s;),]+", body)]
            short_arxiv = re.findall(r"arXiv:\s*(\d{4}\.\d{4,5})", body)
            urls += [f"https://arxiv.org/abs/{aid}" for aid in short_arxiv]
            if not urls:
                continue
            k = key(name)
            if k and k not in out:
                out[k] = (name, urls)
    return out


def fetch(url: str, ctx, limit: int = 3_000_000) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "wam-corpus-ingest/1.0"})
    return urllib.request.urlopen(req, timeout=90, context=ctx).read(limit).decode("utf-8", "replace")


def cvf_pdf(url: str) -> str | None:
    m = re.match(r"(https://openaccess\.thecvf\.com/(?:content[_A-Za-z0-9]*|content/[A-Za-z0-9]+)/)(html|papers)/(.+?)\.html$", url)
    if not m:
        return None
    return f"{m.group(1)}papers/{m.group(3)}.pdf"


def page_pdf(url: str, ctx, pattern: str) -> str | None:
    try:
        html = fetch(url, ctx)
    except Exception:
        return None
    for cand in re.findall(pattern, html):
        cand = htmllib.unescape(cand)
        cand = urllib.parse.urljoin(url, cand)
        if cand.startswith("http") and cand.lower().endswith(".pdf"):
            return cand
    return None


def propose(name: str, urls: list[str], ctx) -> dict:
    """Choose one canonical document for a work, or report that it needs resolution."""
    cands = []
    for u in urls:
        if "arxiv.org/abs/" in u:
            cands.append(("arXiv", u.replace("/abs/", "/pdf/")))
        elif "arxiv.org/pdf/" in u:
            cands.append(("arXiv", u))
        elif "openaccess.thecvf.com" in u and "/html/" in u:
            p = cvf_pdf(u)
            if p:
                cands.append(("VF_camera_ready", p))
        elif "ecva.net" in u:
            # ECVA convention: .../papers_ECCV/html/490_ECCV_2024_paper.php -> .../papers_ECCV/papers/490.pdf
            m = re.search(r"(/papers/[^/]+/papers_[A-Z]+/)html/(\d+)_", u)
            p = (u.split("/papers/")[0] + m.group(1) + "papers/" + m.group(2) + ".pdf") if m else None
            if not p:
                p = page_pdf(u, ctx, r'href="([^"]+\.pdf)"')
            if p:
                cands.append(("ECVA_camera_ready", p))
        elif "neurips.cc" in u or "papers.nips.cc" in u:
            m = re.search(r"/hash/([0-9a-f]+)-Abstract", u)
            p = None
            if m:
                base = u.split("/hash/")[0]
                p = f"{base}/file/{m.group(1)}-Paper-Conference.pdf"
            if not p:
                p = page_pdf(u, ctx, r'href="([^"]+\.pdf)"')
            if p:
                cands.append(("NeurIPS_camera_ready", p))
        elif "proceedings.iclr.cc" in u or "openreview.net" in u:
            p = page_pdf(u, ctx, r'href="([^"]+\.pdf)"')
            if p:
                cands.append(("ICLR_camera_ready", p))
    order = {"VF_camera_ready": 0, "ECVA_camera_ready": 0, "NeurIPS_camera_ready": 0,
             "ICLR_camera_ready": 0, "arXiv": 1}
    cands.sort(key=lambda c: order.get(c[0], 9))
    if not cands:
        return dict(status="NEEDS_RESOLUTION", register_urls=urls,
                    reason="register entry offers only a project page, repository or DOI")
    kind, url = cands[0]
    return dict(status="PLANNED", kind=kind, url=url, register_urls=urls,
                alternates=[u for k, u in cands[1:]])


def main() -> int:
    ctx = ssl.create_default_context(cafile=certifi.where())
    works = placed_works()
    register = register_entries()
    with open(MANIFEST, encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    # corpus short names, e.g. papers/raw_md/P0004_BeTop/... -> "betop"
    corpus_short = set()
    for r in rows:
        for fld in ("raw_md_local_path", "pdf_local_path"):
            m = re.search(r"P\d{4}_([A-Za-z0-9]+)", r[fld] or "")
            if m:
                corpus_short.add(re.sub(r"[^a-z0-9]", "", m.group(1).lower()))
    corpus_titles = {re.sub(r"[^a-z0-9]", "", (r["title"] or "").lower()) for r in rows}
    # census rows that are not single works
    SKIP = {"toaddrivorcontext"}

    plan = {}
    print(f"{'work':46} {'status':18} {'source':64}")
    print("-" * 132)
    for w in works:
        ck = key(w)
        hit = register.get(ck)
        name, urls = hit if hit else (w, [])
        short = key(name)
        norm_name = re.sub(r"[^a-z0-9]", "", name.lower())
        if ck in SKIP or short in SKIP or norm_name in SKIP:
            continue
        # already covered when the census key or the register name is a corpus short name,
        # or the register name is a corpus title
        if ck in corpus_short or short in corpus_short or norm_name in corpus_short \
                or norm_name in corpus_titles:
            continue
        rec = propose(name, urls, ctx) if urls else dict(
            status="NEEDS_RESOLUTION", register_urls=[], reason="no register entry at all")
        rec.update(census_name=w, register_name=name, key=short)
        plan[short or w[:14]] = rec
        print(f"{w[:46]:46} {rec['status']:18} {(rec.get('url') or rec.get('reason',''))[:64]:64}")
        time.sleep(0.5)

    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(plan, fh, indent=2, ensure_ascii=False)
    planned = [k for k, v in plan.items() if v["status"] == "PLANNED"]
    print()
    print(f"census works parsed: {len(works)}   already in corpus: {len(works) - len(plan)}")
    print(f"to acquire: {len(planned)}   need resolution: {len(plan) - len(planned)}")
    for k, v in plan.items():
        if v["status"] != "PLANNED":
            print(f"  NEEDS_RESOLUTION {v['census_name'][:60]}  urls={v['register_urls']}")
    print(f"\nplan -> {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
