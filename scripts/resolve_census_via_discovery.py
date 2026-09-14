"""Resolve the last census works through discovery pages, then verify the official record.

Three Round-1 works are registered only by a project page or a repository, and OpenAlex was
rate-limiting. A project page or repository is a *discovery* source here, never the document:

* the CVF Open Access index for the paper's year is scanned for the census title, and the
  camera-ready is verified through that page's own ``citation_title`` meta tag;
* a project page or README is scanned for an arXiv link, and the arXiv abs page is then
  fetched and its ``citation_title`` compared with the census title.

Only a verified record is written into the plan. Anything unverified is left unresolved.

Usage:
    python resolve_census_via_discovery.py [--apply]
"""
from __future__ import annotations

import json
import os
import re
import ssl
import sys
import time

import certifi

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from resolve_census_unresolved import BASE, get, landing_meta, norm, title_match  # noqa: E402

PLAN = os.path.join(BASE, "manifests", "census_round1_acquisition_plan.json")

# discovery source per unresolved work key: CVF index for a year, or a page to mine for links
DISCOVERY: dict[str, dict] = {
    "drivewm": {"cvf_index": "https://openaccess.thecvf.com/CVPR2024?day=all",
                "title_hint": "driving into the future"},
    "driveoccworld": {"mine": "https://drive-occworld.github.io/",
                      "title_hint": "driving in the occupancy world"},
    "drivearena": {"mine": "https://github.com/PJLab-ADG/DriveArena",
                   "title_hint": "drivearena"},
    # ECVA hosts only an abstract stub for this ECCV 2024 paper (its page carries no PDF link),
    # so the official record is discovered through the paper's own project repository instead.
    "sledge": {"mine": "https://github.com/autonomousvision/sledge",
               "title_hint": "sledge"},
}


def cvf_candidates(index_url: str, hint: str, ctx) -> list[tuple[str, str]]:
    """(html_url, pdf_url) pairs from a CVF index page whose slug matches the hint words."""
    try:
        html = get(index_url, ctx)
    except Exception as exc:
        print(f"    CVF index fetch failed: {exc}")
        return []
    words = [w for w in re.findall(r"[a-z]+", hint.lower()) if len(w) > 3]
    out = []
    for href in re.findall(r'href="(/content/[^"]+_paper\.html)"', html):
        slug = href.lower()
        if all(w in slug or w[:5] in slug for w in words[:3]):
            pdf = href.replace("/html/", "/papers/").replace(".html", ".pdf")
            out.append(("https://openaccess.thecvf.com" + href, "https://openaccess.thecvf.com" + pdf))
    return out[:6]


def arxiv_candidates(page_url: str, ctx) -> list[str]:
    try:
        html = get(page_url, ctx)
    except Exception as exc:
        print(f"    discovery page fetch failed: {exc}")
        return []
    ids = re.findall(r"arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})", html)
    seen, out = set(), []
    for aid in ids:
        if aid not in seen:
            seen.add(aid)
            out.append(f"https://arxiv.org/abs/{aid}")
    return out[:4]


def main() -> int:
    apply_ = "--apply" in sys.argv
    ctx = ssl.create_default_context(cafile=certifi.where())
    plan = json.load(open(PLAN, encoding="utf-8"))
    changed = 0
    for k, spec in DISCOVERY.items():
        rec = plan.get(k)
        if not rec or rec.get("status") == "PLANNED":
            continue
        census_title = rec["census_name"]
        print()
        print(f"  {census_title[:86]}")
        accepted = None
        if "cvf_index" in spec:
            for html_url, pdf_url in cvf_candidates(spec["cvf_index"], spec["title_hint"], ctx):
                meta = landing_meta(html_url, ctx)
                title = (meta.get("title") or [""])[0]
                if title_match(census_title, title):
                    accepted = dict(kind="VF_camera_ready", url=pdf_url, source=html_url,
                                    title=title, authors=(meta.get("authors") or [])[:3],
                                    date=(meta.get("date") or ["-"])[0], venue="CVF Open Access")
                    print(f"    VERIFIED camera-ready: {title[:76]}")
                    break
                print(f"    candidate rejected (title mismatch): {title[:70]!r}")
        if not accepted and "mine" in spec:
            for abs_url in arxiv_candidates(spec["mine"], ctx):
                meta = landing_meta(abs_url, ctx)
                title = (meta.get("title") or [""])[0]
                if title_match(census_title, title):
                    accepted = dict(kind="arXiv", url=abs_url.replace("/abs/", "/pdf/"),
                                    source=abs_url, title=title,
                                    authors=(meta.get("authors") or [])[:3],
                                    date=(meta.get("date") or ["-"])[0],
                                    venue=f"arXiv:{meta.get('arxiv','?')}v{meta.get('version','?')}")
                    print(f"    VERIFIED arXiv record: {title[:76]}")
                    print(f"      {accepted['venue']}  authors={accepted['authors']}  date={accepted['date']}")
                    break
                print(f"    arXiv candidate rejected on title: {title[:70]!r}")
        if accepted:
            rec.update(status="PLANNED", kind=accepted["kind"], url=accepted["url"],
                       resolved_from=accepted["source"],
                       basis="resolved in this batch by discovery then verification: the document was "
                             f"located through {spec.get('cvf_index') or spec.get('mine')}, and the official "
                             f"record was verified independently (title '{accepted['title'][:70]}', "
                             f"{accepted['venue']})")
            changed += 1
            print(f"    -> PDF {accepted['url'][:100]}")
        else:
            rec["reason"] = ("no official record with a matching title could be verified through the "
                             "available discovery sources")
            print("    -> still UNRESOLVED")
        time.sleep(1)

    if apply_:
        json.dump(plan, open(PLAN, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        print(f"\n{changed} newly planned; plan -> {PLAN}")
    else:
        print("\nreport only (pass --apply to write)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
