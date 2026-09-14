"""Parse the owner's Phase-A Census Round 1 files into a candidate work list.

The census is the owner's artifact and must not be edited or re-interpreted here. This tool
only extracts, mechanically, the two things the corpus pipeline needs:

* every work the census placed (bolded first cell of each markdown table row);
* every source entry in the source register (`- Name — URL` lines), which is where the
  official or primary link for a work is recorded.

The two are then joined by name so the pipeline can ingest works that have a registered
source and report works that do not. Nothing is inferred from memory: a work without a
registered URL is listed as needing resolution rather than guessed.

Usage:
    python parse_census_works.py
"""
from __future__ import annotations

import csv
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CENSUS = os.path.join(BASE, "landscape", "CENSUS_PHASE_A_ROUND1.md")
SOURCES = os.path.join(BASE, "landscape", "CENSUS_PHASE_A_ROUND1_SOURCES.md")
MANIFEST = os.path.join(BASE, "manifests", "CORPUS_MANIFEST.csv")


def placed_works() -> list[str]:
    """Bolded first cell of every census table row, in file order."""
    works, seen = [], set()
    with open(CENSUS, encoding="utf-8") as fh:
        for line in fh:
            if not line.startswith("|"):
                continue
            cell = line.split("|")[1].strip() if len(line.split("|")) > 1 else ""
            m = re.match(r"\*\*(.+?)\*\*", cell)
            if not m:
                continue
            name = " ".join(m.group(1).split())
            if name.lower() in ("work", "paper", "title", "") or set(name) <= {"-", " "}:
                continue
            if name not in seen:
                seen.add(name)
                works.append(name)
    return works


def register_entries() -> list[tuple[str, str]]:
    """(name, url) pairs from the source register, preserving order."""
    out = []
    with open(SOURCES, encoding="utf-8") as fh:
        for line in fh:
            m = re.match(r"-\s+(.+?)\s+[—-]\s+(https?://\S+)", line.strip())
            if m:
                out.append((" ".join(m.group(1).split()), m.group(2).rstrip(".,;")))
    return out


def key(name: str) -> str:
    n = name.lower()
    n = re.sub(r"\(.*?\)", " ", n)
    n = re.split(r"\s+[—:]\s+|\s*/\s*", n)[0]
    n = re.sub(r"[^a-z0-9]+", "", n)
    return n[:18]


def main() -> int:
    works = placed_works()
    register = register_entries()
    reg_by_key: dict[str, tuple[str, str]] = {}
    for name, url in register:
        reg_by_key.setdefault(key(name), (name, url))

    with open(MANIFEST, encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    have_titles = " || ".join(
        (r["title"] + " " + (r["official_url"] or "")).lower() for r in rows
    )

    print(f"census placed works: {len(works)}")
    print(f"source register entries: {len(register)}")
    print(f"corpus records: {len(rows)}")
    print()
    print(f"{'work':52} {'registry match':30} {'in corpus?':10}")
    print("-" * 100)
    unmatched = []
    for w in works:
        k = key(w)
        name, url = reg_by_key.get(k, ("", ""))
        if not name:
            # second attempt: any register name that starts with the same key, or vice versa
            for rk, (rn, ru) in reg_by_key.items():
                if rk.startswith(k[:8]) or k.startswith(rk[:8]):
                    name, url = rn, ru
                    break
        in_corpus = ""
        if name:
            token = name.lower().split()[0].strip(",.:")
            in_corpus = "yes" if (token in have_titles and len(token) > 4) else ""
        print(f"{w[:52]:52} {(name or '(no registered source)')[:30]:30} {in_corpus:10}")
        if not name:
            unmatched.append(w)

    print()
    print(f"works with no registered source: {len(unmatched)}")
    for w in unmatched:
        print(f"  - {w}")
    print()
    print("register entries not matched to a placed work:")
    for name, url in register:
        print(f"  {name[:60]:60} {url[:60]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
