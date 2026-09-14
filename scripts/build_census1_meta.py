"""Build evidence-backed manifest metadata for the Census Round 1 text-layer batch.

Two stages, both reading only artifacts that already exist on disk:

    --scan        read each paper's raw markdown and record, per record:
                  * repository URLs the paper itself prints (project pages are flagged as
                    such, because a project page is not a repository);
                  * counts for the fixed corpus tag vocabulary, so tags can be assigned from
                    the paper's own wording instead of from any field placement;
                  * size and encoding quality facts used in the report.
                  Output: manifests/batch_census1_evidence.json

    --write-meta  emit manifest META entries for the batch into scripts/build_manifest.py and
                  extend ORDER to cover every allocated id. Titles, authors, years and arXiv
                  versions come from the identity ledger; tags come from the scan; the front-page
                  verdict comes from the verification ledger. Nothing here is typed from memory.

Usage:
    python build_census1_meta.py --scan
    python build_census1_meta.py --write-meta
"""
from __future__ import annotations

import json
import os
import py_compile
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAN = os.path.join(BASE, "manifests")
ALLOC = os.path.join(MAN, "census1_id_allocation.json")
PLAN = os.path.join(MAN, "census_round1_acquisition_plan.json")
IDENTITY = os.path.join(MAN, "batch_census1_identity.json")
EVIDENCE = os.path.join(MAN, "batch_census1_evidence.json")
FRONTPAGE = os.path.join(MAN, "batch_census1_frontpage_verification.json")
RAWMD = os.path.join(MAN, "batch_census1_rawmd_results.json")
PAPERS_DIR = os.path.join(BASE, "papers", "raw_md")

TAGS = ["planning", "world-model", "interactive", "reactive", "trajectory-prediction",
        "trajectory-scorer", "closed-loop", "counterfactual", "end-to-end", "evaluation",
        "action-conditioned", "diffusion", "reward-model", "OOD", "autoregressive",
        "benchmark", "latent-world-model", "open-loop", "representation", "risk", "safety"]

REPO_HOSTS = ("github.com", "gitlab.com", "bitbucket.org", "huggingface.co")
PROJECT_HOSTS = ("github.io", "sites.google.com", "drive.google.com")


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (s or "").lower())


def source_version(kind: str, url: str, arxiv_version: str) -> str:
    if kind == "arXiv":
        v = (arxiv_version or "").lstrip("v")
        return f"arXiv_v{v}" if v else "arXiv_vUNKNOWN"
    m = re.search(r"/content[_/]([A-Za-z]+)(\d{4})/", url)
    if kind == "VF_camera_ready" and m:
        return f"{m.group(1)}{m.group(2)}_camera_ready"
    if kind == "NeurIPS_camera_ready":
        y = re.search(r"/paper/(\d{4})/", url)
        return f"NeurIPS{(y.group(1) if y else '')}_camera_ready"
    return "UNKNOWN"


def pdf_front_text(pid: str, short: str, pages: int = 3) -> list[tuple[int, str]]:
    """Text of the first PDF pages, used when the markdown lost a line the PDF prints.

    The stored PDF is the paper itself; MinerU has been observed to drop a repository line from
    the extracted markdown (ViDAR), so a paper's own printed URL is taken from the PDF when the
    markdown does not show it. The page number is recorded so the claim stays checkable.
    """
    path = os.path.join(BASE, "papers", "pdf", f"{pid}_{short}.pdf")
    if not os.path.exists(path):
        return []
    try:
        import pypdfium2 as pdfium
    except Exception:
        return []
    out: list[tuple[int, str]] = []
    doc = pdfium.PdfDocument(path)
    try:
        for i in range(min(pages, len(doc))):
            out.append((i + 1, doc[i].get_textpage().get_text_range()))
    finally:
        doc.close()
    return out


def repo_pattern(hosts=REPO_HOSTS) -> str:
    return (r"(?:https?://)?(?:www\.)?(?:" + "|".join(re.escape(h) for h in hosts)
            + r")/[A-Za-z0-9_.\-]+/[A-Za-z0-9_.\-]+")


def scan_one(pid: str, short: str, title: str) -> dict:
    path = os.path.join(PAPERS_DIR, f"{pid}_{short}", f"{pid}_{short}.raw.md")
    rec: dict = {"paper_id": pid, "short": short, "raw_md": os.path.relpath(path, BASE).replace(os.sep, "/"),
                 "exists": os.path.exists(path)}
    if not rec["exists"]:
        return rec
    text = open(path, encoding="utf-8", errors="replace").read()
    rec["chars"] = len(text)
    low = text.lower()

    # Repository evidence: only what the paper's own body prints. The reference list is cut off
    # first, because a bibliography is full of third-party repository URLs and taking one of those
    # for the paper's own code would be a false claim. A scheme-less `github.com/owner/repo` counts
    # too, because MinerU often drops the scheme, and the surrounding line is kept so a human can
    # see the sentence the URL came from.
    body = text
    ref = re.search(r"(?m)^#{1,6}\s*(references|bibliography)\s*$", text, re.I)
    if ref:
        body = text[:ref.start()]
    code_words = re.compile(r"code|repo|repositor|implement|release|available|open.?source|github", re.I)
    repos, projects = [], []
    repo_pat = repo_pattern()
    for m in re.finditer(repo_pat, body):
        url = m.group(0).rstrip(".")
        if not url.startswith("http"):
            url = "https://" + url
        line = body[:m.start()].count("\n") + 1
        ctx = body.splitlines()[line - 1].strip()[:200] if line - 1 < len(body.splitlines()) else ""
        item = {"url": url, "line": line, "context": ctx, "source": "raw markdown",
                "code_context": bool(code_words.search(ctx))}
        if item["url"] not in [r["url"] for r in repos]:
            repos.append(item)

    # if the markdown shows no repository, ask the PDF's own first pages before concluding UNKNOWN
    if not repos:
        for page_no, ptxt in pdf_front_text(pid, short):
            for m in re.finditer(repo_pat, ptxt):
                url = m.group(0).rstrip(".")
                if not url.startswith("http"):
                    url = "https://" + url
                ctx = ptxt[max(0, m.start() - 90):m.end() + 90].replace("\n", " ").strip()
                item = {"url": url, "line": page_no, "context": ctx, "source": f"PDF page {page_no}",
                        "code_context": bool(code_words.search(ctx))}
                if item["url"] not in [r["url"] for r in repos]:
                    repos.append(item)
    for host in PROJECT_HOSTS:
        for m in re.finditer(rf"https?://[^\s\)\]\>,;\"']*{re.escape(host)}[^\s\)\]\>,;\"']*", text):
            url = m.group(0).rstrip(".")
            if url not in projects:
                projects.append(url)
    rec["repo_urls"] = repos[:6]
    rec["project_pages"] = projects[:4]

    # tag vocabulary counts over the paper's own text
    counts = {}
    for tag in TAGS:
        pat = tag.replace("-", "[- ]")
        counts[tag] = len(re.findall(rf"\b{pat}\w*", low))
    rec["tag_counts"] = counts
    title_low = title.lower()
    proposed = [t for t in TAGS if t.replace("-", " ") in title_low or t.replace("-", "-") in title_low]
    body = [t for t, c in sorted(counts.items(), key=lambda kv: -kv[1]) if c >= 5]
    tags: list[str] = []
    for t in proposed + body:
        if t not in tags:
            tags.append(t)
    if "planning" in counts and "planning" not in tags and counts["planning"] >= 5:
        tags.insert(0, "planning")
    rec["proposed_tags"] = tags[:4] or ["planning"]
    rec["mojibake"] = text.count("\ufffd")
    rec["image_refs"] = len(re.findall(r"!\[\]\(", text))
    return rec


def load(name: str) -> dict:
    p = os.path.join(MAN, name)
    if not os.path.exists(p):
        return {}
    d = json.load(open(p, encoding="utf-8"))
    if isinstance(d, list):
        d = {r["paper_id"]: r for r in d}
    return d


def main() -> int:
    mode = sys.argv[1] if len(sys.argv) > 1 else "--scan"
    alloc = json.load(open(ALLOC, encoding="utf-8"))
    plan = json.load(open(PLAN, encoding="utf-8"))
    ident = load("batch_census1_identity.json")

    if mode == "--scan":
        out = {}
        print(f"  {'id':6} {'short':17} {'chars':8} {'tags (from the paper\'s own wording)':44} code evidence")
        for pid, a in alloc.items():
            rec = scan_one(pid, a["short"], (ident.get(pid) or {}).get("official_title", ""))
            out[pid] = rec
            repo = (rec.get("repo_urls") or [{}])[0].get("url", "") if rec.get("repo_urls") else ""
            print(f"  {pid:6} {a['short'][:17]:17} {rec.get('chars', 0):8} "
                  f"{','.join(rec.get('proposed_tags', []))[:44]:44} {repo[:40]}")
        json.dump(out, open(EVIDENCE, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        have = sum(1 for r in out.values() if r["exists"])
        print(f"\n  raw MD present: {have}/{len(out)}   evidence -> {EVIDENCE}")
        return 0

    if mode == "--write-meta":
        ev = load("batch_census1_evidence.json")
        fp = load("batch_census1_frontpage_verification.json")
        md = load("batch_census1_rawmd_results.json")
        missing = [pid for pid in alloc if pid not in ev or not ev[pid].get("exists")]
        assert not missing, f"raw MD missing for {missing}; run the conversion first"
        entries = []
        for pid, a in alloc.items():
            r = ident.get(pid) or {}
            assert r.get("official_title"), f"{pid}: no verified official title"
            title = r["official_title"]
            authors = r.get("official_authors") or []
            first = authors[0] if authors else "UNKNOWN"
            year = (r.get("official_date") or "")[:4] or "UNKNOWN"
            e = ev[pid]
            kind = (plan.get(a["key"]) or {}).get("kind", "")
            sv = source_version(kind, a["pdf_url"], r.get("arxiv_version", ""))
            verdict = (fp.get(pid) or {}).get("verdict", "NOT_RUN")
            qc = (md.get(pid) or {}).get("qc", "NOT_RUN")
            repos = e.get("repo_urls") or []
            if repos:
                code, curl = "YES", repos[0]["url"]
                src_kind = repos[0].get("source", "text")
                code_ev = (f"Code: the paper itself prints {curl} (seen in the {src_kind}, "
                           f"position {repos[0]['line']}), so code_available=YES")
            else:
                code, curl = "UNKNOWN", ""
                if e.get("project_pages"):
                    code_ev = (f"The text prints a PROJECT PAGE only ({e['project_pages'][0]}); a project "
                               f"page is not a repository, and absence of a printed URL is not evidence "
                               f"that no code exists, so code_available stays UNKNOWN")
                else:
                    code_ev = ("No repository URL is printed in the extracted text; absence of a printed URL "
                               "is not evidence that no code exists, so code_available stays UNKNOWN")
            tags = ";".join(e.get("proposed_tags", ["planning"]))
            note = (
                f"Phase-A Census Round 1 text-layer batch (CORPUS_BATCH=census1), record created so that "
                f"this work placed by landscape/CENSUS_PHASE_A_ROUND1.md has a local text layer. "
                f"Official title, first author and date come from the official landing page "
                f"({a['landing_url']}), copied from manifests/batch_census1_identity.json; front-page "
                f"verification of the stored PDF returned {verdict}. Canonical source: {sv}. {code_ev}. "
                f"Tags are assigned mechanically from the fixed corpus vocabulary by counting the work's own "
                f"title and text ('{tags}'), not from any field placement. Conversion QC: {qc}. "
                f"decision_relevance=LOW: this batch exists to make the census readable locally, and it makes "
                f"no claim about whether the work is decision-relevant. Census-depth record: no deep read, no "
                f"field placement, no novelty or gap verdict. EVIDENCE_LEVEL=DOCUMENT_VERIFIED"
            )
            def lit(s: str) -> str:
                return json.dumps(s, ensure_ascii=False)
            entries.append(
                f'    "{pid}": dict(short={lit(a["short"])},\n'
                f'                  title={lit(title)},\n'
                f'                  year={lit(year)}, first_author={lit(first)}, venue={lit(kind.replace("_camera_ready", " camera-ready").replace("arXiv", "arXiv preprint"))},\n'
                f'                  arxiv_id={lit(r.get("arxiv_version") and a["pdf_url"].split("/")[-1] or "")}, doi="NONE",\n'
                f'                  official_url={lit(a["landing_url"])},\n'
                f'                  code_available={lit(code)}, official_code_url={lit(curl)},\n'
                f'                  tags={lit(tags)}, hyp="GENERAL", rel="LOW", reviewed="2026-09-14",\n'
                f'                  note={lit(note)}),'
            )
        full = os.path.join(BASE, "scripts", "build_manifest.py")
        src = open(full, encoding="utf-8", newline="").read()
        anchor = 'EVIDENCE_LEVEL=DOCUMENT_VERIFIED"),\n}'
        assert src.count(anchor) == 1, f"META anchor occurs {src.count(anchor)} times"
        header = ("    # --- Phase-A Census Round 1 text-layer batch (CORPUS_BATCH=census1) ---\n"
                  "    # Generated by scripts/build_census1_meta.py from the identity, front-page and raw-MD\n"
                  "    # ledgers: titles are the official ones, tags come from the works' own wording, and code\n"
                  "    # availability is asserted only where the paper prints a repository URL.\n")
        src = src.replace(anchor, 'EVIDENCE_LEVEL=DOCUMENT_VERIFIED"),\n' + header + "\n".join(entries) + "\n}", 1)
        lo, hi = min(int(p[1:]) for p in alloc), max(int(p[1:]) for p in alloc)
        src = re.sub(r'ORDER = \[f"P\{i:04d\}" for i in range\(1, \d+\)\]',
                     f'ORDER = [f"P{{i:04d}}" for i in range(1, {hi + 1})]', src)
        assert f"range(1, {hi + 1})" in src, "ORDER was not extended"
        open(full, "w", encoding="utf-8", newline="").write(src)
        py_compile.compile(full, doraise=True)
        print(f"  wrote {len(entries)} META entries ({lo}..{hi}) into scripts/build_manifest.py; ORDER -> range(1, {hi+1})")
        return 0

    print(f"unknown mode {mode!r}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
