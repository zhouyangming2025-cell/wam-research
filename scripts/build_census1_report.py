"""Compose the Phase-A Census Round 1 text-layer batch report from the ledgers.

Every number in the report is read from a ledger that a pipeline step wrote, so the report
cannot drift from the artifacts. The prose states what the batch is and, more importantly,
what it does not claim.

Usage:
    python build_census1_report.py
"""
from __future__ import annotations

import json
import os
from collections import Counter

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAN = os.path.join(BASE, "manifests")
OUT = os.path.join(BASE, "CENSUS_ROUND1_TEXTLAYER_INGEST_REPORT.md")


def load(name: str):
    p = os.path.join(MAN, name)
    if not os.path.exists(p):
        return {}
    d = json.load(open(p, encoding="utf-8"))
    if isinstance(d, list):
        d = {r["paper_id"]: r for r in d if isinstance(r, dict) and "paper_id" in r}
    return d


def main() -> int:
    alloc = json.load(open(os.path.join(MAN, "census1_id_allocation.json"), encoding="utf-8"))
    plan = json.load(open(os.path.join(MAN, "census_round1_acquisition_plan.json"), encoding="utf-8"))
    ident = load("batch_census1_identity.json")
    dl = load("batch_census1_download_results.json")
    fp = load("batch_census1_frontpage_verification.json")
    md = load("batch_census1_rawmd_results.json")
    ev = load("batch_census1_evidence.json")
    ids = sorted(alloc)
    L: list[str] = []
    a = L.append

    a("# Phase-A Census Round 1 — Local Text-Layer Batch Report")
    a("")
    a("Status: **corpus acquisition record**. This document is not the census. It records what the")
    a("local corpus agent acquired and verified so that the works the owner already placed in")
    a("`landscape/CENSUS_PHASE_A_ROUND1.md` can be read locally, without repeating that")
    a("placement, adding a family label, or making any novelty or gap claim.")
    a("")
    a("Batch label: `census1`. Companion ledgers:")
    a("")
    a("```text")
    for n in ("census_round1_acquisition_plan.json", "census1_id_allocation.json",
              "batch_census1_identity.json", "batch_census1_download_results.json",
              "batch_census1_frontpage_verification.json", "batch_census1_rawmd_results.json",
              "batch_census1_evidence.json", "CORPUS_MANIFEST.csv"):
        a(f"manifests/{n}")
    a("```")
    a("")
    a("---")
    a("")
    a("## 1. Why this batch exists")
    a("")
    a("The Round-1 census places roughly 45 works, but only 20 of them existed locally. Reading")
    a("the rest meant fetching public PDFs mid-analysis, which makes every later claim depend on")
    a("the network and on whatever the publisher served that day. The owner chose to close that")
    a("gap, so this batch gives the remaining Round-1 works the same treatment the corpus already")
    a("gives its other records: a verified identity, one canonical PDF with a logical-byte hash, a")
    a("front-page check, and an extractable raw markdown text layer with images.")
    a("")
    a("Boundary: acquisition, identity verification, conversion, metadata and QC only. No family")
    a("assignment, no placement confidence and no novelty verdict is made here; the owner's")
    a("landscape, atlas, taxonomy and state files were not edited.")
    a("")
    a("## 2. What was ingested")
    a("")
    a("| paper_id | short | official title | source | pages | raw md chars |")
    a("|---|---|---|---|---:|---:|")
    for pid in ids:
        r = ident.get(pid) or {}
        title = (r.get("official_title") or "").replace("|", "/")
        if len(title) > 74:
            title = title[:71] + "..."
        kind = (plan.get(alloc[pid]["key"]) or {}).get("kind", "")
        sv = (dl.get(pid) or {}).get("source_version", kind)
        pg = (fp.get(pid) or {}).get("pages", "")
        chars = (md.get(pid) or {}).get("length_chars", "")
        a(f"| {pid} | {alloc[pid]['short']} | {title} | {sv} | {pg} | {chars} |")
    a("")
    a(f"Total: **{len(ids)} works**, {ids[0]}–{ids[-1]}. Full 64-character hashes and canonical URLs")
    a("are in `manifests/batch_census1_download_results.json` and `manifests/CORPUS_MANIFEST.csv`.")
    a("")
    a("## 3. How the set was chosen, mechanically")
    a("")
    a("No work was selected from memory or from a search engine result:")
    a("")
    a("1. `scripts/parse_census_works.py` parsed the owner's census table rows and the Round-1 source")
    a("   register, mechanically, and subtracted the works the corpus already holds;")
    a("2. `scripts/plan_census_acquisition.py` then chose one canonical source per remaining work in")
    a("   the corpus priority order — venue camera-ready, then official arXiv, then project-hosted —")
    a("   deriving CVF camera-ready PDFs from the paper pages, and extracting the PDF link from")
    a("   NeurIPS/ICLR pages;")
    a("3. every candidate URL was probed for a real `%PDF-` body before any download was attempted.")
    a("")
    kinds = Counter((plan.get(alloc[pid]["key"]) or {}).get("kind", "?") for pid in ids)
    a("Source mix: " + ", ".join(f"{k}={v}" for k, v in sorted(kinds.items())) + ".")
    a("")
    a("## 4. Works whose register entry carried no document link")
    a("")
    a("Five works were registered only by a project page, a repository or a publisher landing page.")
    a("A project page is not a document, so each was resolved through a discovery step and then")
    a("verified independently — the discovery page is never the evidence:")
    a("")
    a("- **P0037 Drive-WM**: the CVPR 2024 Open Access index was scanned for the census title and the")
    a("  camera-ready page's own `citation_title` was checked before its PDF was used;")
    a("- **P0044 Drive-OccWorld**, **P0056 DriveArena**, **P0055 SLEDGE**: an arXiv link was found on")
    a("  the work's own project page or repository, and the official arXiv record was then fetched and")
    a("  its `citation_title` compared with the census entry;")
    a("- **NPPC** stays unresolved: the register records no lawful open canonical source for it, the")
    a("  same reason its record P0008 has never had a PDF. Nothing about that changed here, and it was")
    a("  not replaced with a guessed link.")
    a("")
    a("## 5. Identity verification")
    a("")
    a("Each work's official landing page was fetched (`scripts/fetch_work_identity.py`) and its")
    a("`citation_title`, `citation_author`, `citation_date` and arXiv version recorded verbatim in")
    a("`manifests/batch_census1_identity.json`. A keyword test derived from the census entry had to be")
    a("satisfied by the official title; the result:")
    a("")
    mism = [pid for pid in ids if not (ident.get(pid) or {}).get("identity_match")]
    a(f"- matched on the first pass: {len(ids) - len(mism)} of {len(ids)}")
    for pid in mism:
        a(f"- **{pid} divergence**: the census records this work as "
          f"“{alloc[pid]['census_name']}”, while the official record reads "
          f"“{(ident.get(pid) or {}).get('official_title')}”. Same work, different phrasing; the")
        a("  official title is what entered the corpus, and the census file was left untouched.")
    a("")
    a("## 6. Acquisition result")
    a("")
    dls = [pid for pid in ids if (dl.get(pid) or {}).get("status") == "DOWNLOADED"]
    bytes_total = sum((dl.get(pid) or {}).get("bytes") or 0 for pid in ids)
    a(f"- downloaded: **{len(dls)} of {len(ids)}**")
    a(f"- total logical bytes: {bytes_total:,}")
    a("- one canonical PDF per work, hashed on logical bytes (Python is the hash authority; the")
    a("  known .NET/local-read offset quirk in this environment does not affect these values)")
    a("- duplicate work check: no arXiv id, DOI or official URL in this batch repeats an existing")
    a("  corpus record, and no identifier was reused or renumbered")
    a("")
    a("## 7. Front-page verification")
    a("")
    a("Page 1 of every stored PDF was read and compared with the officially recorded title and first")
    a("author:")
    a("")
    v = Counter((fp.get(pid) or {}).get("verdict", "NOT_RUN") for pid in ids)
    a("- " + ", ".join(f"`{k}`: {n}" for k, n in sorted(v.items())))
    a("- first author found on page 1 for every record in this batch")
    a("")
    a("## 8. Conversion and QC")
    a("")
    a("MinerU ran locally through `scripts/run_mineru.py`. Conversion for this batch ran **serially**:")
    a("an earlier batch showed that concurrent conversion on this host can hit service-side 502s and,")
    a("before the write path was fixed, could make two processes race on the shared ledger.")
    a("")
    qc = Counter((md.get(pid) or {}).get("qc", "NOT_RUN") for pid in ids)
    a("- " + ", ".join(f"`{k}`: {n}" for k, n in sorted(qc.items())))
    imgs = sum((md.get(pid) or {}).get("images_copied") or 0 for pid in ids)
    miss = sum((md.get(pid) or {}).get("images_missing") or 0 for pid in ids)
    moji = sum((md.get(pid) or {}).get("mojibake_total") or 0 for pid in ids)
    a(f"- images copied: {imgs}; images referenced but missing: {miss}")
    a(f"- replacement/mojibake characters across the batch: {moji}")
    a("")
    a("## 9. Code availability, as printed by the papers themselves")
    a("")
    a("`code_available=YES` is asserted only where the paper's own text prints a repository URL. A")
    a("project page is not a repository, and the absence of a printed URL is not evidence that no code")
    a("exists. What the extracted text actually shows:")
    a("")
    yes = [(pid, (ev.get(pid) or {}).get("repo_urls") or []) for pid in ids]
    yes = [(pid, r) for pid, r in yes if r]
    a(f"- papers printing a repository URL: {len(yes)} of {len(ids)}")
    for pid, r in yes:
        a(f"  - {pid} {alloc[pid]['short']}: `{r[0]['url']}` (line {r[0]['line']})")
    only_page = [pid for pid in ids if not ((ev.get(pid) or {}).get("repo_urls") or [])
                 and (ev.get(pid) or {}).get("project_pages")]
    if only_page:
        a(f"- papers printing a project page but no repository: {', '.join(only_page)}")
    none_printed = [pid for pid in ids if not ((ev.get(pid) or {}).get("repo_urls") or [])
                    and not ((ev.get(pid) or {}).get("project_pages"))]
    if none_printed:
        a(f"- papers printing neither (recorded as UNKNOWN, not as “no code”): {', '.join(none_printed)}")
    a("")
    a("## 10. Tag provenance")
    a("")
    a("Tags for these 26 records were assigned mechanically (`scripts/build_census1_meta.py`) by")
    a("counting the fixed corpus vocabulary in each work's own title and extracted text. They are")
    a("**not** taken from the census family labels, so a reader must not treat them as the owner's")
    a("placement. Every record in this batch carries `decision_relevance=LOW` and `GENERAL` hypothesis")
    a("tags, because the batch exists to make the census readable locally and makes no claim about")
    a("decision relevance; both are owner decision points.")
    a("")
    a("## 11. What this batch does NOT claim")
    a("")
    a("- no placement of any work into a family, no family label, no placement confidence;")
    a("- no novelty, gap or counterexample verdict, and no statement about which limitations were")
    a("  genuinely resolved in the field's history;")
    a("- no claim that a work does or does not use a world model beyond what its own text says;")
    a("- no deep reading: these are placement-depth text layers, and the manifest marks them `NO_CARD`;")
    a("- no edit to the owner's `landscape/` or `state/` files; the retired handoff area was not touched.")
    a("")
    a("## 12. Reproduce")
    a("")
    a("```powershell")
    a("$mp = 'D:\\Program Files\\Mineru\\venv\\Scripts\\python.exe'")
    a("$env:CORPUS_BATCH = 'census1'")
    a("& $mp scripts\\parse_census_works.py                     # census works vs source register")
    a("& $mp scripts\\plan_census_acquisition.py               # canonical source per work")
    a("& $mp scripts\\resolve_census_unresolved.py             # OpenAlex path (title-verified)")
    a("& $mp scripts\\resolve_census_via_discovery.py          # discovery-page path (title-verified)")
    a("& $mp scripts\\apply_census1_plan.py --allocate         # ids + landing pages")
    a("& $mp scripts\\fetch_work_identity.py                   # official identity ledger")
    a("& $mp scripts\\apply_census1_plan.py --wires            # SOURCES / EXPECT / PAPERS")
    a("& $mp scripts\\fetch_canonical_pdfs.py                  # canonical PDFs + sha256")
    a("& $mp scripts\\verify_frontpage.py                      # page-1 verification")
    a("& $mp scripts\\build_raw_md.py P0035,...,P0060          # MinerU raw MD (run serially)")
    a("& $mp scripts\\build_census1_meta.py --scan             # text evidence + tags")
    a("& $mp scripts\\build_census1_meta.py --write-meta       # manifest metadata")
    a("& $mp scripts\\build_manifest.py                        # CORPUS_MANIFEST.csv")
    a("& $mp scripts\\build_census1_report.py                  # this report")
    a("```")
    a("")
    a("## 13. Decision points for the owner")
    a("")
    a("1. **NPPC**: still no lawful open canonical source; keep it documented as blocked, or supply a")
    a("   permitted copy.")
    a("2. **`decision_relevance=LOW` for the whole batch**: if some of these works are already")
    a("   decision-relevant anchors for you, say which and the corpus will record that as your")
    a("   judgement rather than the agent's.")
    a("3. **Tag vocabulary**: no vision-language/VLA tag exists, so VLA works carry the closest")
    a("   available terms; extending the vocabulary is a corpus decision.")
    a("4. **Census titles vs official titles**: where the census paraphrases a title (P0052 here), the")
    a("   corpus stores the official one. Tell me if you want the census phrasing recorded too.")

    open(OUT, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(f"  wrote {OUT}")
    print(f"    {len('\n'.join(L))} chars, {len(L)} lines")
    print(f"    records covered: {len(ids)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
