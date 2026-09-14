"""Resolve candidate works to verified identities via the OpenAlex API.

Why OpenAlex: the arXiv export API rate-limits bursts (HTTP 429) and web search is not
always available in the agent session, while OpenAlex is a free metadata index that
returns title, year, venue, DOI and known arXiv/landing-page locations. Identity is
still finally confirmed against page 1 of the downloaded canonical PDF, so this tool
narrows candidates and never stands in for document verification.

Usage:
    python resolve_works_openalex.py            # built-in census candidate list
    python resolve_works_openalex.py "some title"
"""
from __future__ import annotations

import json
import ssl
import sys
import time
import urllib.parse
import urllib.request

import certifi

API = "https://api.openalex.org/works?search={q}&per-page=3"

# Phase-A Census Round 2 coverage holes (FIELD_ATLAS.md F10; CENSUS_PHASE_A_ROUND1.md;
# state/NEXT_TASK.md F3 / F11 / WM-RL lineage).
CANDIDATES = [
    ("F10 Hydra-MDP", "Hydra-MDP End-to-end Multimodal Planning with Multi-target Hydra-Distillation"),
    ("F10 Hydra-MDP++", "Hydra-MDP++ Advancing End-to-End Driving via Expert-Guided Hydra-Distillation"),
    ("F10 DriveSuprim", "DriveSuprim Towards Precise Trajectory Selection for End-to-End Planning"),
    ("F10 iPad", "iPad Iterative Proposal-centric End-to-End Autonomous Driving"),
    ("F10 VLA DriveVLM", "DriveVLM The Convergence of Autonomous Driving and Large Vision-Language Models"),
    ("F10 VLA OmniDrive", "OmniDrive A Holistic LLM-Agent Framework for Autonomous Driving"),
    ("F10 VLA ORION", "ORION A Holistic End-to-End Autonomous Driving Framework by Vision-Language Instructed Action Generation"),
    ("WM-RL Think2Drive", "Think2Drive Efficient Reinforcement Learning by Thinking in Latent World Model for Quasi-Realistic Autonomous Driving"),
    ("F3 ViDAR", "ViDAR Visual Point Cloud Forecasting enables Scalable Autonomous Driving"),
    ("F3 GenAD", "GenAD Generative End-to-End Autonomous Driving"),
    ("F11 nuScenes", "nuScenes A multimodal dataset for autonomous driving"),
    ("F11 nuPlan", "nuPlan A closed-loop ML-based planning benchmark for autonomous vehicles"),
    ("F11 NAVSIM", "NAVSIM Data-Driven Non-Reactive Autonomous Vehicle Simulation and Benchmarking"),
    ("F11 NAVSIM-v2", "NAVSIM v2 benchmark autonomous driving"),
    ("F11 Bench2Drive", "Bench2Drive Towards Multi-Ability Benchmarking of Closed-Loop End-To-End Autonomous Driving"),
    ("F11 HUGSIM", "HUGSIM A Real-Time Photo-Realistic and Closed-Loop Simulator for Autonomous Driving"),
]


def search(title: str, ctx=None):
    url = API.format(q=urllib.parse.quote(title))
    req = urllib.request.Request(url, headers={"User-Agent": "wam-corpus-ingest/1.0"})
    return json.loads(urllib.request.urlopen(req, timeout=60, context=ctx).read().decode("utf-8"))


def summarize(w: dict) -> str:
    venue = ((w.get("primary_location") or {}).get("source") or {}).get("display_name") or "-"
    arxiv = ""
    for loc in w.get("locations") or []:
        for key in ("landing_page_url", "pdf_url"):
            u = loc.get(key) or ""
            if "arxiv.org/abs/" in u or "arxiv.org/pdf/" in u:
                arxiv = u.replace("/pdf/", "/abs/").replace(".pdf", "")
    doi = (w.get("doi") or "").replace("https://doi.org/", "") or "-"
    first = ""
    auths = w.get("authorships") or []
    if auths:
        first = (auths[0].get("author") or {}).get("display_name") or ""
    return (f"{(w.get('display_name') or '')[:74]} | {w.get('publication_year')} | "
            f"{venue[:28]} | DOI {doi} | {arxiv or 'no arXiv location'} | 1st {first}")


def main() -> int:
    ctx = ssl.create_default_context(cafile=certifi.where())
    pairs = CANDIDATES
    if len(sys.argv) > 1:
        pairs = [("cli", sys.argv[1])]
    for label, title in pairs:
        print(f"--- {label}", flush=True)
        try:
            data = search(title, ctx)
        except Exception as ex:
            print(f"      ERROR {type(ex).__name__}: {ex}", flush=True)
            time.sleep(1)
            continue
        results = data.get("results") or []
        if not results:
            print("      (no OpenAlex match)", flush=True)
        for w in results[:3]:
            print(f"      {summarize(w)}", flush=True)
        time.sleep(1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
