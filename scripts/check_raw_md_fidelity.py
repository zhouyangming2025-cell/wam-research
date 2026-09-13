"""Fidelity scan for Batch 0A raw MD: quantify line-break hyphen loss.

MinerU's text-extraction path joins words that were hyphenated across a line
break without restoring the hyphen ("end-to-end" -> "endtoend"). This measures
how often that happened, per paper, for a fixed list of expected hyphenated
terms. It is an observation metric, not a pass/fail gate: the raw MD is meant to
be raw.

Writes manifests/batch_0a_rawmd_fidelity.json and prints a table.
"""
from __future__ import annotations

import json
import os
import re
import sys

BASE = r"D:\zym_information\ZYM\wam\research_assets"
MAN = os.path.join(BASE, "manifests")
RAW = os.path.join(BASE, "papers", "raw_md")
OUT = os.path.join(MAN, "batch_0a_rawmd_fidelity.json")

TERMS = [
    "end-to-end", "trajectory-conditioned", "fine-grained", "grid-centric",
    "closed-loop", "open-loop", "pair-wise", "self-attention",
    "state-of-the-art", "real-world", "decision-making", "world-model",
    "cross-module", "well-defined", "long-tail", "time-step", "ego-vehicle",
]

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def scan(text: str) -> dict:
    low = text.lower()
    rows = []
    merged_total = 0
    hyphen_total = 0
    for t in TERMS:
        merged = t.replace("-", "")
        h = len(re.findall(r"\b" + re.escape(t) + r"\b", low))
        m = len(re.findall(r"\b" + re.escape(merged) + r"\b", low))
        hyphen_total += h
        merged_total += m
        if m:
            rows.append(dict(term=t, hyphenated=h, merged=m))
    return dict(merged_forms=merged_total, hyphenated_forms=hyphen_total,
                examples=sorted(rows, key=lambda r: -r["merged"]))


def main():
    res_path = os.path.join(MAN, "batch_0a_rawmd_results.json")
    with open(res_path, encoding="utf-8") as f:
        results = json.load(f)
    out = []
    for r in results:
        pid = r["paper_id"]
        if r.get("qc") != "RAW_MD_READY":
            continue
        key = f"{pid}_{r['short_name']}"
        md = os.path.join(RAW, key, f"{key}.raw.md")
        if not os.path.exists(md):
            continue
        with open(md, encoding="utf-8") as fh:
            text = fh.read()
        s = scan(text)
        s.update(paper_id=pid, short_name=r["short_name"], chars=len(text))
        out.append(s)
        ex = ", ".join(f"{e['term']}:{e['merged']}" for e in s["examples"][:5]) or "-"
        print(f"{pid} {r['short_name']:20s} merged={s['merged_forms']:4d} "
              f"hyphenated={s['hyphenated_forms']:4d}  {ex}")

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    tm = sum(x["merged_forms"] for x in out)
    th = sum(x["hyphenated_forms"] for x in out)
    print(f"\ntotal merged={tm} hyphenated={th} "
          f"(hyphen loss {tm / max(tm + th, 1):.1%} of these terms)")
    print(f"results -> {OUT}")


if __name__ == "__main__":
    main()
