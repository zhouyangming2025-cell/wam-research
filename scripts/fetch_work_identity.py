"""Record official identity metadata for a batch of candidate works.

Identity -> dedup -> ID allocation is the first pipeline step, and the expected title
used later by front-page verification must come from an official landing page rather
than from memory. This tool fetches each candidate's landing page (arXiv abs page or
venue proceedings page), extracts citation_title / citation_author / citation_date and,
for arXiv, the exact version number, then writes a merge-on-write ledger at
manifests/batch_<batch>_identity.json.

Usage:
    python fetch_work_identity.py            # built-in census candidates
"""
from __future__ import annotations

import html as htmllib
import json
import os
import re
import ssl
import time
import urllib.request

import certifi

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BATCH = os.environ.get("CORPUS_BATCH", "census2")
OUT = os.path.join(BASE, "manifests", f"batch_{BATCH}_identity.json")

# Phase-A Census Round 2 coverage holes. NOTE: candidate arXiv IDs for ViDAR, GenAD,
# nuScenes, nuPlan and Think2Drive are hypotheses to be confirmed by the landing page;
# a mismatch is recorded as such and never silently accepted.
CANDIDATES = [
    # paper_id, short, landing_url, pdf_url
    ("P0021", "HydraMDP", "https://arxiv.org/abs/2406.06978", "https://arxiv.org/pdf/2406.06978"),
    ("P0022", "DriveSuprim", "https://arxiv.org/abs/2506.06659", "https://arxiv.org/pdf/2506.06659"),
    ("P0023", "iPad", "https://arxiv.org/abs/2505.15111", "https://arxiv.org/pdf/2505.15111"),
    ("P0024", "DriveVLM", "https://arxiv.org/abs/2402.12289", "https://arxiv.org/pdf/2402.12289"),
    ("P0025", "OmniDrive", "https://arxiv.org/abs/2405.01533", "https://arxiv.org/pdf/2405.01533"),
    ("P0026", "ORION",
     "https://openaccess.thecvf.com/content/ICCV2025/html/Fu_ORION_A_Holistic_End-to-End_Autonomous_Driving_Framework_by_Vision-Language_Instructed_ICCV_2025_paper.html",
     "https://openaccess.thecvf.com/content/ICCV2025/papers/Fu_ORION_A_Holistic_End-to-End_Autonomous_Driving_Framework_by_Vision-Language_Instructed_ICCV_2025_paper.pdf"),
    ("P0027", "Think2Drive", "https://arxiv.org/abs/2402.16720", "https://arxiv.org/pdf/2402.16720"),
    ("P0028", "ViDAR",
     "https://openaccess.thecvf.com/content/CVPR2024/html/Yang_Visual_Point_Cloud_Forecasting_enables_Scalable_Autonomous_Driving_CVPR_2024_paper.html",
     "https://openaccess.thecvf.com/content/CVPR2024/papers/Yang_Visual_Point_Cloud_Forecasting_enables_Scalable_Autonomous_Driving_CVPR_2024_paper.pdf"),
    ("P0029", "GenAD", "https://arxiv.org/abs/2402.11502", "https://arxiv.org/pdf/2402.11502"),
    ("P0030", "nuScenes",
     "https://openaccess.thecvf.com/content_CVPR_2020/html/Caesar_nuScenes_A_Multimodal_Dataset_for_Autonomous_Driving_CVPR_2020_paper.html",
     "https://openaccess.thecvf.com/content_CVPR_2020/papers/Caesar_nuScenes_A_Multimodal_Dataset_for_Autonomous_Driving_CVPR_2020_paper.pdf"),
    ("P0031", "nuPlan", "https://arxiv.org/abs/2106.11810", "https://arxiv.org/pdf/2106.11810"),
    ("P0032", "NAVSIM", "https://arxiv.org/abs/2406.15349", "https://arxiv.org/pdf/2406.15349"),
    ("P0033", "Bench2Drive", "https://arxiv.org/abs/2406.03877", "https://arxiv.org/pdf/2406.03877"),
    ("P0034", "HUGSIM", "https://arxiv.org/abs/2412.01718", "https://arxiv.org/pdf/2412.01718"),
]

# What each candidate is expected to be, so a wrong DOI/arXiv ID cannot pass silently.
EXPECT_KEY = {
    "P0021": "Hydra-MDP", "P0022": "DriveSuprim", "P0023": "iPad",
    "P0024": "DriveVLM", "P0025": "OmniDrive", "P0026": "ORION",
    "P0027": "Think2Drive", "P0028": "Visual Point Cloud Forecasting",
    "P0029": "GenAD", "P0030": "nuScenes", "P0031": "nuPlan",
    "P0032": "NAVSIM", "P0033": "Bench2Drive", "P0034": "HUGSIM",
}


def meta(html: str, name: str):
    m = re.search(rf'<meta name="{name}" content="([^"]*)"', html)
    return htmllib.unescape(m.group(1)).strip() if m else ""


def fetch(url: str, ctx) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "wam-corpus-ingest/1.0"})
    return urllib.request.urlopen(req, timeout=90, context=ctx).read().decode("utf-8", "replace")


def main() -> int:
    ctx = ssl.create_default_context(cafile=certifi.where())
    ledger = {}
    if os.path.exists(OUT):
        with open(OUT, encoding="utf-8") as fh:
            ledger = json.load(fh)
    for pid, short, landing, pdf in CANDIDATES:
        print(f"--- {pid} {short}", flush=True)
        rec = dict(paper_id=pid, short_name=short, landing_url=landing, pdf_url=pdf)
        try:
            html = fetch(landing, ctx)
            title = meta(html, "citation_title")
            authors = re.findall(r'<meta name="citation_author" content="([^"]*)"', html)
            date = meta(html, "citation_date") or meta(html, "citation_publication_date")
            ver = re.search(r"arXiv:\d{4}\.\d{4,5}v(\d+)", html)
            rec.update(
                official_title=htmllib.unescape(title).replace("\n", " ").strip(),
                official_authors=[htmllib.unescape(a).strip() for a in authors],
                official_date=date,
                arxiv_version=(f"v{ver.group(1)}" if ver else ""),
            )
        except Exception as ex:
            rec.update(error=f"{type(ex).__name__}: {ex}")
        exp = EXPECT_KEY.get(pid, "")
        got = rec.get("official_title", "")
        rec["expected_key"] = exp
        rec["identity_match"] = bool(got) and all(
            w.lower() in got.lower() for w in exp.split() if len(w) > 3
        )
        ledger[pid] = rec
        print(f"      title : {got[:88] or '(none)'}", flush=True)
        print(f"      auth  : {', '.join(rec.get('official_authors', [])[:3]) or '(none)'}", flush=True)
        print(f"      date  : {rec.get('official_date') or '-'}  arxiv={rec.get('arxiv_version') or '-'}"
              f"  match={rec['identity_match']}", flush=True)
        if rec.get("error"):
            print(f"      ERROR : {rec['error']}", flush=True)
        time.sleep(2)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(ledger, fh, indent=2, ensure_ascii=False)
    print(f"\nidentity ledger -> {OUT}  ({len(ledger)} records)", flush=True)
    bad = [k for k, v in ledger.items() if not v.get("identity_match")]
    print("identity mismatches to review:", bad or "none", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
