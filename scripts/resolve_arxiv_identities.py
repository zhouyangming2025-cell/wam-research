"""Resolve candidate works to verified arXiv identities via the arXiv API.

Identity is the first pipeline step (identity -> dedup -> ID allocation). This tool
exists because web search is not always available in the agent session, while the
arXiv API is: it returns exact titles, arXiv IDs, submission dates and authors, so a
candidate is never taken from memory or from a search snippet.

Usage:
    python resolve_arxiv_identities.py                 # built-in census candidate list
    python resolve_arxiv_identities.py "ti:\"Some Title\""
"""
from __future__ import annotations

import ssl
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

import certifi

NS = {"a": "http://www.w3.org/2005/Atom"}
API = "https://export.arxiv.org/api/query?search_query={q}&max_results={n}&sortBy=relevance"

# Phase-A Census Round 2 coverage holes named in landscape/FIELD_ATLAS.md (F10),
# landscape/CENSUS_PHASE_A_ROUND1.md and state/NEXT_TASK.md (F3, F11, WM-RL lineage).
QUERIES = [
    ("F10 Hydra-MDP", 'ti:"Hydra-MDP"'),
    ("F10 Hydra-MDP++", 'ti:"Hydra-MDP++"'),
    ("F10 DriveSuprim", 'ti:"DriveSuprim"'),
    ("F10 iPad", 'ti:"iPad" AND abs:"planning"'),
    ("F10 VLA DriveVLM", 'ti:"DriveVLM"'),
    ("F10 VLA OmniDrive", 'ti:"OmniDrive" AND abs:"autonomous driving"'),
    ("F10 VLA ORION", 'ti:"ORION" AND abs:"autonomous driving"'),
    ("WM-RL Think2Drive", 'ti:"Think2Drive"'),
    ("F3 ViDAR", 'ti:"ViDAR"'),
    ("F3 GenAD", 'ti:"GenAD"'),
    ("F11 nuScenes", 'ti:"nuScenes"'),
    ("F11 nuPlan", 'ti:"nuPlan"'),
    ("F11 NAVSIM", 'ti:"NAVSIM"'),
    ("F11 NAVSIM-v2", 'ti:"NAVSIM-v2" OR abs:"NAVSIM-v2"'),
    ("F11 Bench2Drive", 'ti:"Bench2Drive"'),
    ("F11 HUGSIM", 'ti:"HUGSIM"'),
]


def query(q: str, n: int = 3, ctx=None):
    url = API.format(q=urllib.parse.quote(q), n=n)
    req = urllib.request.Request(url, headers={"User-Agent": "wam-corpus-ingest/1.0 (local research corpus; contact: repo owner)"})
    raw = urllib.request.urlopen(req, timeout=60, context=ctx).read().decode("utf-8", "replace")
    return ET.fromstring(raw).findall("a:entry", NS)


def query_with_backoff(q: str, n: int = 3, ctx=None, tries: int = 4):
    """arXiv rate-limits bursts (HTTP 429); back off instead of losing a candidate."""
    delay = 10
    last = None
    for attempt in range(tries):
        try:
            return query(q, n, ctx)
        except Exception as ex:
            last = ex
            if attempt < tries - 1:
                print(f"      retry in {delay}s after {type(ex).__name__}", flush=True)
                time.sleep(delay)
                delay *= 2
    raise last


def main() -> int:
    ctx = ssl.create_default_context(cafile=certifi.where())
    pairs = QUERIES
    if len(sys.argv) > 1:
        pairs = [("cli", sys.argv[1])]
    for label, q in pairs:
        print(f"--- {label}", flush=True)
        try:
            entries = query_with_backoff(q, ctx=ctx)
        except Exception as ex:  # network/parse failure is reported, never hidden
            print(f"      ERROR {type(ex).__name__}: {ex}", flush=True)
            time.sleep(2)
            continue
        if not entries:
            print("      (no arXiv match)", flush=True)
        for e in entries:
            title = " ".join(e.find("a:title", NS).text.split())
            aid = e.find("a:id", NS).text.rsplit("/", 1)[-1]
            published = e.find("a:published", NS).text[:10]
            authors = ", ".join(a.find("a:name", NS).text for a in e.findall("a:author", NS)[:3])
            print(f"      {aid:16s} {published}  {title[:80]}   [{authors}]", flush=True)
        time.sleep(12)
    return 0


if __name__ == "__main__":
    sys.exit(main())
