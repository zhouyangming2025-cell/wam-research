"""Collect per-paper metadata evidence from converted raw MD text.

Two fields in the manifest must be evidence-backed rather than guessed:

* ``code_available`` may only be YES when the paper itself prints a repository URL
  (a project page is not a repository), so this tool lists every printed URL with its
  surrounding line and which page of the markdown it appeared on;
* ``primary_tags`` must come from the corpus tag vocabulary, so this tool shows how often
  each vocabulary keyword actually occurs, leaving the assignment to a reviewer.

Usage:
    CORPUS_BATCH=census2 python scan_raw_md_evidence.py P0021,P0022,...
"""
from __future__ import annotations

import os
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(BASE, "papers", "raw_md")

SHORT = {}
for _d in os.listdir(RAW) if os.path.isdir(RAW) else []:
    m = re.match(r"(P\d{4})_(.+)$", _d)
    if m:
        SHORT[m.group(1)] = m.group(2)

REPO_HOSTS = ("github.com", "gitlab.com", "bitbucket.org", "huggingface.co", "codeberg.org")
VOCAB = {
    "world-model": r"world[- ]model",
    "latent-world-model": r"latent world model",
    "planning": r"\bplan(?:ning|ner)\b",
    "end-to-end": r"end-to-end|\bE2E\b",
    "closed-loop": r"closed[- ]loop",
    "open-loop": r"open[- ]loop",
    "benchmark": r"\bbenchmark",
    "evaluation": r"\bevaluat|\bmetric",
    "diffusion": r"\bdiffusion\b",
    "autoregressive": r"auto-?regressive",
    "reward-model": r"reward model|\breward\b",
    "safety": r"\bsafety\b",
    "risk": r"\brisk\b",
    "representation": r"representation|pre-?train",
    "interactive": r"interactive|interaction",
    "reactive": r"reactive|reactivity",
    "counterfactual": r"counterfactual",
    "action-conditioned": r"action[- ]conditioned",
    "trajectory-prediction": r"trajectory prediction|motion prediction|forecasting",
    "trajectory-scorer": r"scorer|scoring|trajectory selection|candidate selection",
    "OOD": r"out-of-distribution|\bOOD\b",
}


def main() -> int:
    ids = sys.argv[1].split(",") if len(sys.argv) > 1 else sorted(SHORT)
    for pid in ids:
        pid = pid.strip()
        short = SHORT.get(pid)
        if not short:
            print(f"--- {pid}: no raw_md directory")
            continue
        path = os.path.join(RAW, f"{pid}_{short}", f"{pid}_{short}.raw.md")
        if not os.path.exists(path):
            print(f"--- {pid} {short}: raw md not found ({path})")
            continue
        text = open(path, encoding="utf-8", errors="replace").read()
        lines = text.splitlines()
        print(f"--- {pid} {short}  ({len(text)} chars, {len(lines)} lines)")

        # printed URLs, with the line they appeared on
        urls: list[tuple[int, str, str]] = []
        for i, ln in enumerate(lines, 1):
            for u in re.findall(r"https?://[^\s\)\]\"'>,]+", ln):
                urls.append((i, u.rstrip(".,;"), ln.strip()))
        repos = [(i, u, ctx) for i, u, ctx in urls if any(h in u for h in REPO_HOSTS)]
        other = [(i, u, ctx) for i, u, ctx in urls if (i, u, ctx) not in repos]
        print(f"      printed URLs: {len(urls)}  repository URLs: {len(repos)}")
        for i, u, ctx in repos[:6]:
            print(f"        REPO  L{i}: {u}      | {ctx[:70]}")
        for i, u, ctx in other[:6]:
            print(f"        other L{i}: {u}      | {ctx[:60]}")

        # abstract opening, so tags can be assigned from the paper's own words
        m = re.search(r"(?is)\babstract\b[.:\s]*(.{120,700}?)(?:\n\n|\n#)", text)
        if m:
            snippet = " ".join(m.group(1).split())[:420]
            print(f"      abstract: {snippet}")

        # vocabulary evidence
        low = text.lower()
        counts = {tag: len(re.findall(pat, low, re.I)) for tag, pat in VOCAB.items()}
        nonzero = {t: c for t, c in sorted(counts.items(), key=lambda kv: -kv[1]) if c}
        print("      tag evidence: " + ", ".join(f"{t}={c}" for t, c in list(nonzero.items())[:10]))
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
