"""Probe official code URLs for existence (evidence upgrade for Step 4-8 section E).

This does NOT establish officiality - it only records whether the URL resolves
and what the page claims. Nothing is cloned. TLS verification is ON with an
explicit CA bundle (the host has no system CA store; see ASSET_PROVENANCE notes).
"""
from __future__ import annotations

import json
import os
import re
import ssl
import sys
import urllib.request

import certifi

BASE = r"D:\zym_information\ZYM\wam\research_assets"
OUT = os.path.join(BASE, "manifests", "batch_0a_code_probe.json")

TARGETS = [
    ("P0001", "Epona", "YES", "https://github.com/Kevin-thu/Epona"),
    ("P0004", "BeTop", "YES", "https://github.com/OpenDriveLab/BeTop"),
    ("P0009", "DriveLaW", "YES", "https://github.com/xiaomi-research/drivelaw"),
    ("P0010", "TOAD", "YES", "https://github.com/valeoai/TOAD"),
    ("P0003", "GraphAD", "CANDIDATE", "https://github.com/OpenDriveLab/GraphAD"),
    ("P0006", "GenDrive", "CANDIDATE", "https://github.com/Chengyuan-Zhang/Gen-Drive"),
]

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ctx = ssl.create_default_context(cafile=certifi.where())
UA = "Mozilla/5.0 (compatible; corpus-librarian/1.0)"


def probe(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=45, context=ctx) as r:
            body = r.read(400_000).decode("utf-8", "replace")
            return dict(status=r.status, final_url=r.geturl(), body=body)
    except urllib.error.HTTPError as e:
        return dict(status=e.code, final_url=url, body="", error=f"HTTP {e.code}")
    except Exception as e:
        return dict(status=None, final_url=url, body="", error=f"{type(e).__name__}: {e}")


def main():
    out = []
    for pid, short, claim, url in TARGETS:
        r = probe(url)
        body = r.pop("body", "")
        title = ""
        m = re.search(r"<title>(.*?)</title>", body, re.S | re.I)
        if m:
            title = re.sub(r"\s+", " ", m.group(1)).strip()[:160]
        mentions = bool(re.search(re.escape(short), body, re.I)) if body else False
        rec = dict(paper_id=pid, short_name=short, manifest_claim=claim, url=url,
                   http_status=r.get("status"), final_url=r.get("final_url"),
                   error=r.get("error"), page_title=title,
                   page_mentions_short_name=mentions,
                   verdict=("REPO_URL_REACHABLE" if r.get("status") == 200 else
                            "REPO_URL_NOT_REACHABLE"))
        out.append(rec)
        print(f"{pid} {short:10s} claim={claim:9s} http={rec['http_status']} "
              f"mentions={mentions} {rec['verdict']}")
        if title:
            print(f"    title: {title}")

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"\nresults -> {OUT}")
    print("NOTE: reachability is NOT proof of officiality.")


if __name__ == "__main__":
    main()
