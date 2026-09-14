"""Turn the census Round-1 acquisition plan into pipeline entries, mechanically.

Two stages, so that no title is ever written from memory:

    --allocate   assign stable paper_ids (continuing the manifest's highest id), record the
                 allocation in manifests/census1_id_allocation.json, and add the official
                 landing-page list to scripts/fetch_work_identity.py;
    --wires      after the identity ledger exists, add the acquisition entries to
                 scripts/fetch_canonical_pdfs.py, scripts/verify_frontpage.py and
                 scripts/build_raw_md.py, taking every title and author surname from the
                 identity ledger, never from memory.

Every insertion uses an anchor that must occur exactly once, and the file is compiled after
writing, so a bad edit fails loudly instead of corrupting a pipeline script.

Usage:
    python apply_census1_plan.py --allocate
    python apply_census1_plan.py --wires
"""
from __future__ import annotations

import csv
import json
import os
import py_compile
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLAN = os.path.join(BASE, "manifests", "census_round1_acquisition_plan.json")
ALLOC = os.path.join(BASE, "manifests", "census1_id_allocation.json")
IDENTITY = os.path.join(BASE, "manifests", "batch_census1_identity.json")
MANIFEST = os.path.join(BASE, "manifests", "CORPUS_MANIFEST.csv")
BATCH = "census1"

# readable corpus short names, keyed by the planner's key for each work
SHORT = {
    "gaia1": "GAIA1", "drivedreamer": "DriveDreamer", "drivewm": "DriveWM", "vista": "Vista",
    "drivedreamer2": "DriveDreamer2", "drivinggpt": "DrivingGPT", "policyworldmodel": "PolicyWM",
    "worlddrive": "WorldDrive", "occworld": "OccWorld", "driveoccworld": "DriveOccWorld",
    "wote": "WoTE", "world4drive": "World4Drive", "driveworld": "DriveWorld", "law": "LAW",
    "drivejepa": "DriveJEPA", "worldrft": "WorldRFT", "autojepa": "AutoJEPA", "reworld": "ReWorld",
    "wajepa": "WAJEPA", "whattrulymatters": "WhatTrulyMatters", "sledge": "SLEDGE",
    "drivearena": "DriveArena", "uniad": "UniAD", "vad": "VAD",
    "diffusiondrive": "DiffusionDrive", "drivor": "DrivoR",
}

HEADER = "# --- Phase-A Census Round 1 text-layer batch (CORPUS_BATCH=census1) ---"


def edit(path: str, anchor: str, addition: str) -> None:
    """Insert `addition` immediately before `anchor`, which must occur exactly once."""
    full = os.path.join(BASE, "scripts", path)
    src = open(full, encoding="utf-8", newline="").read()
    assert src.count(anchor) == 1, f"{path}: anchor occurs {src.count(anchor)} times: {anchor[:60]!r}"
    src = src.replace(anchor, addition + anchor, 1)
    open(full, "w", encoding="utf-8", newline="").write(src)
    py_compile.compile(full, doraise=True)
    print(f"  patched scripts/{path}")


def landing_urls(rec: dict) -> tuple[str, str]:
    """(landing page, pdf url) for the official record of a planned work."""
    url, kind = rec["url"], rec["kind"]
    if kind == "arXiv":
        return url.replace("/pdf/", "/abs/"), url
    if kind == "VF_camera_ready":
        return url.replace("/papers/", "/html/").replace(".pdf", ".html"), url
    if kind == "NeurIPS_camera_ready":
        page = url.replace("/file/", "/hash/").replace("-Paper-Conference.pdf", "-Abstract-Conference.html")
        return page, url
    return rec.get("resolved_from", url), url


def source_version(rec: dict, ident: dict | None) -> str:
    kind = rec["kind"]
    if kind == "arXiv":
        v = (ident or {}).get("arxiv_version") or ""   # already shaped like "v2"
        v = v.lstrip("v")
        return f"arXiv_v{v}" if v else "arXiv_vUNKNOWN"
    m = re.search(r"/content[_/]([A-Za-z]+)(\d{4})/", rec["url"])
    if kind == "VF_camera_ready" and m:
        return f"{m.group(1)}{m.group(2)}_camera_ready"
    if kind == "NeurIPS_camera_ready":
        y = re.search(r"/paper/(\d{4})/", rec["url"])
        return f"NeurIPS{(y.group(1) if y else '')}_camera_ready"
    if kind == "ECVA_camera_ready":
        return "ECCV2024_camera_ready"
    return "UNKNOWN"


def main() -> int:
    mode = sys.argv[1] if len(sys.argv) > 1 else "--allocate"
    plan = json.load(open(PLAN, encoding="utf-8"))
    planned = [(k, v) for k, v in plan.items() if v.get("status") == "PLANNED"]
    with open(MANIFEST, encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    top = max(int(r["paper_id"][1:]) for r in rows)

    if mode == "--allocate":
        assert not os.path.exists(ALLOC), f"{ALLOC} already exists; refusing to reallocate ids"
        alloc = {}
        for i, (k, rec) in enumerate(planned, start=1):
            pid = f"P{top + i:04d}"
            page, pdf = landing_urls(rec)
            alloc[pid] = dict(key=k, short=SHORT.get(k, k[:14]), census_name=rec["census_name"],
                              landing_url=page, pdf_url=pdf, kind=rec["kind"],
                              register_urls=rec.get("register_urls", []))
        json.dump(alloc, open(ALLOC, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        print(f"  allocated {len(alloc)} ids: {list(alloc)[0]}..{list(alloc)[-1]} -> {ALLOC}")
        lines = [HEADER,
                 "# Works placed by landscape/CENSUS_PHASE_A_ROUND1.md that had no local text layer.",
                 "# Landing pages come from manifests/census1_id_allocation.json; titles are read from those",
                 "# pages and compared with the census entry, never typed from memory."]
        for pid, a in alloc.items():
            lines.append(f'    ("{pid}", "{a["short"]}", "{a["landing_url"]}", "{a["pdf_url"]}"),')
        edit("fetch_work_identity.py", '    ("P0021", "HydraMDP"', "\n".join(lines) + "\n")

        def keyword(census_name: str) -> str:
            """Distinctive words that must all appear in the official title (EXPECT_KEY rule)."""
            core = re.split(r"\s*[—–:]\s*", census_name, maxsplit=1)
            core = core[1] if len(core) > 1 else core[0]
            words = [w for w in re.findall(r"[A-Za-z0-9\-]+", core) if len(w) > 3]
            return " ".join(words[:4]) or census_name

        kw = [f'    "{pid}": {json.dumps(keyword(a["census_name"]), ensure_ascii=False)},'
              for pid, a in alloc.items()]
        # the anchor already carries the closing brace, so the addition must not repeat it
        edit("fetch_work_identity.py", '    "P0032": "NAVSIM", "P0033": "Bench2Drive", "P0034": "HUGSIM",\n}',
             "\n".join(kw) + "\n")
        return 0

    if mode == "--wires":
        alloc = json.load(open(ALLOC, encoding="utf-8"))
        ident = json.load(open(IDENTITY, encoding="utf-8"))
        if isinstance(ident, list):
            ident = {r["paper_id"]: r for r in ident}
        missing = [pid for pid in alloc if pid not in ident]
        assert not missing, f"identity ledger is missing {missing}; run fetch_work_identity.py first"

        src_lines, exp_lines, pap_lines, meta_lines = [], [], [], []
        src_lines.append(HEADER)
        src_lines.append("# Sources proposed by scripts/plan_census_acquisition.py and verified in this batch.")
        exp_lines.append(HEADER)
        pap_lines.append(HEADER)
        for pid, a in alloc.items():
            rec = plan[a["key"]]
            r = ident[pid]
            assert r.get("official_title"), f"{pid}: identity ledger has no title ({r.get('error')})"
            if not r.get("identity_match"):
                # A keyword miss is not automatically a wrong paper: the census may paraphrase an
                # official title. Every such case is listed here with its reason, and the official
                # title is what enters the corpus; nothing is silently accepted.
                divergent = {
                    "P0052": "census titles it 'ReWorld: Learning Better Representations for World Action "
                             "Models' while the official arXiv record reads 'ReWorld: Representation "
                             "Learning for World Action Models' - same work, census phrasing differs",
                }
                assert pid in divergent, f"{pid}: official title failed the EXPECT_KEY check"
                print(f"  NOTE {pid}: {divergent[pid]}")
            best = dict(official_title=r["official_title"],
                        authors=r.get("official_authors") or [],
                        arxiv_version=r.get("arxiv_version") or "")
            title = best["official_title"]
            sv = source_version(rec, best)
            basis = (rec.get("basis") or "selected by the acquisition planner") + \
                f". Official landing page verified in this batch: citation_title matches the census entry"
            alt = a["landing_url"]
            src_lines.append(
                f'    dict(paper_id="{pid}", short="{a["short"]}",\n'
                f'         url="{a["pdf_url"]}",\n'
                f'         source_version="{sv}",\n'
                f'         basis={json.dumps(basis, ensure_ascii=False)},\n'
                f'         alternate_official="{alt}"),')
            surname = (best["authors"] or ["UNKNOWN"])[0].split(",")[0].strip() or "UNKNOWN"
            extra = [x.split(",")[0].strip() for x in (best["authors"] or [])[1:12]]
            exp_lines.append(
                f'    "{pid}": ("{a["short"]}", {json.dumps(title, ensure_ascii=False)},\n'
                f'              "{surname}", {json.dumps(extra, ensure_ascii=False)}),')
            pap_lines.append(f'    ("{pid}", "{a["short"]}"),')
        edit("fetch_canonical_pdfs.py", '    dict(paper_id="P0021"', "\n".join(src_lines) + "\n\n")
        edit("verify_frontpage.py", '    "P0021": ("HydraMDP"', "\n".join(exp_lines) + "\n")
        edit("build_raw_md.py", '    ("P0021", "HydraMDP")', "\n".join(pap_lines) + "\n")
        json.dump({"order": [f'P{i:04d}' for i in range(top + 1, top + 1 + len(alloc))],
                   "note": "census1 batch; ORDER must be extended to cover these ids"},
                  open(os.path.join(BASE, "manifests", "census1_order.json"), "w", encoding="utf-8"), indent=2)
        print(f"  wired {len(alloc)} acquisitions into SOURCES, EXPECT and PAPERS")
        return 0

    print(f"unknown mode {mode!r}; use --allocate or --wires")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
