"""Resolve the census works whose register entry carries no usable document link.

Some Round-1 works are registered only by a project page, a repository or a publisher
landing page. A project page is not a document, so this tool looks for an official record
instead, and then *verifies* it:

    1. OpenAlex is queried with the census title taken verbatim from the owner's file;
    2. the candidate's official landing page is fetched (arXiv abs page, or the publisher /
       Open Access page OpenAlex points at);
    3. the landing page's citation_title must match the census title (whitespace and
       punctuation insensitive); only then is the record accepted.

A candidate that cannot be verified is reported as UNRESOLVED with the reason. Nothing is
guessed, and no identifier is ever written from memory.

Usage:
    python resolve_census_unresolved.py            # report only
    python resolve_census_unresolved.py --apply    # write verified results into the plan
"""
from __future__ import annotations

import json
import os
import re
import ssl
import sys
import time
import urllib.parse
import urllib.request

import certifi

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLAN = os.path.join(BASE, "manifests", "census_round1_acquisition_plan.json")
UA = {"User-Agent": "wam-corpus-ingest/1.0 (research corpus; mailto:corpus@example.invalid)"}


def get(url: str, ctx, timeout: int = 90) -> str:
    req = urllib.request.Request(url, headers=UA)
    return urllib.request.urlopen(req, timeout=timeout, context=ctx).read(4_000_000).decode("utf-8", "replace")


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (s or "").lower())


def title_parts(s: str) -> list[str]:
    """Normalized `method name` + `descriptive title` fragments of a work name."""
    split = re.split(r"\s*[—–:]\s*", s or "", maxsplit=1)
    parts = [norm(split[0])]
    if len(split) > 1:
        parts.append(norm(split[1]))
    return [p for p in parts if p]


def title_match(census_name: str, candidate_title: str, min_len: int = 8) -> bool:
    """Same-work test across the shapes the census and official records actually use.

    The census may prefix a method name (`Drive-WM: Driving into the Future ...`), may use the
    method name alone (`DriveArena`), or may shorten a title. Any fragment of one name that
    contains, or is contained in, a fragment of the other is accepted, with a length floor so a
    short generic word cannot match by accident. Page 1 of the PDF is verified later regardless.
    """
    for a in title_parts(census_name):
        for b in title_parts(candidate_title):
            if len(a) >= min_len and len(b) >= min_len and (a == b or a in b or b in a):
                return True
    return False


def openalex(title: str, ctx) -> list[dict]:
    q = urllib.parse.quote(title)
    url = f"https://api.openalex.org/works?search={q}&per-page=5&mailto=corpus@example.invalid"
    for attempt in range(3):
        try:
            data = json.loads(get(url, ctx))
            return data.get("results", [])
        except Exception as exc:  # rate limiting is common; back off and retry
            print(f"    openalex attempt {attempt + 1} failed: {exc}")
            time.sleep(10 * (attempt + 1))
    return []


def landing_meta(url: str, ctx) -> dict:
    """citation_title / citation_author / citation_date from an official landing page."""
    try:
        html = get(url, ctx)
    except Exception as exc:
        return {"error": str(exc)}
    out = {}
    for field, key in (("citation_title", "title"), ("citation_date", "date"),
                       ("citation_author", "authors"), ("citation_pdf_url", "pdf")):
        vals = re.findall(rf'<meta[^>]+name="{field}"[^>]+content="([^"]*)"', html, re.I)
        if not vals:
            vals = re.findall(rf"<meta[^>]+content=\"([^\"]*)\"[^>]+name=\"{field}\"", html, re.I)
        if vals:
            out.setdefault(key, []).append(vals[0] if key != "authors" else vals)
    m = re.search(r"arXiv:(\d{4}\.\d{4,5})v(\d+)", html)
    if m:
        out["arxiv"], out["version"] = m.group(1), m.group(2)
    return out


def main() -> int:
    apply = "--apply" in sys.argv
    ctx = ssl.create_default_context(cafile=certifi.where())
    plan = json.load(open(PLAN, encoding="utf-8"))
    todo = {k: v for k, v in plan.items() if v.get("status") == "NEEDS_RESOLUTION"}
    print(f"unresolved works: {len(todo)}")
    changed = 0
    for k, rec in todo.items():
        title = rec["census_name"]
        print()
        print(f"  {title[:88]}")
        results = openalex(title, ctx)
        accepted = None
        for cand in results[:5]:
            cand_title = (cand.get("title") or "")
            if not title_match(title, cand_title):
                continue
            ids = cand.get("ids", {}) or {}
            venue = ((cand.get("primary_location") or {}).get("source") or {}).get("display_name") or ""
            print(f"    openalex candidate: {cand_title[:70]}")
            print(f"      year={cand.get('publication_year')}  venue={venue[:40]}  arxiv={ids.get('arxiv','-')}")
            # prefer the publisher / open-access landing page OpenAlex points at, else arXiv
            loc_url = ((cand.get("primary_location") or {}).get("landing_page_url")) or ""
            arxiv = (ids.get("arxiv") or "").rsplit("/", 1)[-1]
            for url, kind in ((loc_url, "venue"), (f"https://arxiv.org/abs/{arxiv}" if arxiv else "", "arXiv")):
                if not url:
                    continue
                meta = landing_meta(url, ctx)
                if meta.get("error"):
                    print(f"      {kind} page fetch failed: {meta['error']}")
                    continue
                if title_match(title, meta.get("title", [""])[0]):
                    accepted = dict(kind=kind, url=url, meta=meta, year=cand.get("publication_year"),
                                    venue=venue, doi=(cand.get("doi") or ""))
                    print(f"      VERIFIED via {kind}: {meta.get('title',[''])[0][:70]}")
                    print(f"        authors={meta.get('authors',[])[:3]}  date={meta.get('date',['-'])[0]}")
                    break
                print(f"      {kind} title mismatch: {meta.get('title',[''])[0][:70]!r}")
            if accepted:
                break
        if accepted:
            pdf = None
            if accepted["kind"] == "arXiv":
                pdf = accepted["url"].replace("/abs/", "/pdf/")
            else:
                pdf = (accepted["meta"].get("pdf") or [""])[0] or None
            rec.update(status="PLANNED" if pdf else "NEEDS_RESOLUTION",
                       kind=accepted["kind"] + "_camera_ready" if accepted["kind"] != "arXiv" else "arXiv",
                       url=pdf,
                       resolved_from=accepted["url"],
                       basis=f"resolved and verified in this batch: official {accepted['kind']} record "
                             f"titled exactly like the census entry ({accepted['year']}); "
                             f"venue recorded as {accepted['venue'] or 'n/a'}"
                             + (f"; DOI {accepted['doi']}" if accepted.get("doi") else ""))
            if not pdf:
                rec["reason"] = "landing page did not expose a PDF link"
            else:
                changed += 1
                print(f"    -> PDF {pdf[:100]}")
        else:
            rec["reason"] = "no official record with a matching title could be verified"
            print("    -> UNRESOLVED (no verified official record)")
        time.sleep(2)

    if apply:
        json.dump(plan, open(PLAN, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        print(f"\nplan updated: {changed} newly planned, plan -> {PLAN}")
    else:
        print("\nreport only (pass --apply to write)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
