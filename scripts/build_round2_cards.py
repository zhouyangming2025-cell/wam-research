"""Generate paper-card SKELETONS for the Round 2 targeted ingest.

Infrastructure only. Bibliographic fields come from build_manifest.META (single
source of truth) and provenance/QC facts come from the batch ledgers, so no hash
is ever retyped by hand. EVERY scientific section is left as
`PENDING SCIENTIFIC REVIEW`: observed-failure verdicts, hypothesis impact,
prior-art occupancy and research verdicts are deep-read (GPT-5.6 Sol) tasks, not
corpus-agent tasks.

Inputs, all under manifests/ and merged across batches:
  batch_*_download_results.json        canonical URL, source_version, bytes, sha256
  batch_*_frontpage_verification.json  DOCUMENT_VERIFIED verdict, pages, page-1 head
  batch_*_rawmd_results.json           raw-MD QC facts, raw_md_sha256, image counts

Usage:  python build_round2_cards.py [P0013,P0014,...]
Idempotent: rewrites the card for each requested id.
"""
from __future__ import annotations

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_manifest import META, load_all  # noqa: E402

BASE = r"D:\zym_information\ZYM\wam\research_assets"
CARDS = os.path.join(BASE, "papers", "cards")
DATE = "2026-09-14"
PENDING = "PENDING SCIENTIFIC REVIEW"
ROUND2 = [f"P{i:04d}" for i in range(13, 21)]

# Full author lists, restricted to what an ingestion record actually shows:
#   "page 1"  = observed in the front-page verification record for the canonical PDF
#   "index"   = discovery metadata only (state/TARGETED_READING_QUEUE.md), not yet
#               confirmed against a document, and therefore labelled as such.
# Names are NEVER completed from memory; a truncated list says so.
AUTHORS = {
    # Only used when no document exists: the blocked record. Every other card takes
    # its author list from the document itself, so nothing is completed from memory.
    "P0020": "Mohammad Bahram, et al. (index-level discovery metadata only; no canonical PDF acquired)",
}

SCIENTIFIC_SECTIONS = [
    ("1. Role in our research", "这篇论文为什么进入我们的 corpus？"),
    ("2. Exact problem", "作者究竟解决什么问题？"),
    ("3. System / data flow", "input → representation → model → output → planner / evaluator"),
    ("4. Training", "Data / supervision / objective / joint or staged / alternative-action supervision / reactive supervision"),
    ("5. Inference / planning coupling", "Planner consumes what? Candidate-conditioned? Action-conditioned? Replanning? Explicit scorer? Reactive world response?"),
    ("6. Evaluation regime", "open-loop / non-reactive / pseudo closed-loop / reactive closed-loop / real-world closed-loop"),
    ("7. Observed failures", "Only genuinely observed failures. If none: NO DIRECT OBSERVED FAILURE REPORTED"),
    ("8. Direct evidence relevant to current hypotheses", "P1_RETIRED / P2R_PRIMARY / P3_HOLD: strengthens, weakens, or not relevant"),
    ("9. Counterevidence", "What could this paper kill in our hypotheses?"),
    ("10. Author Claim vs Evidence vs Our Inference", "AUTHOR CLAIM / DIRECT EXPERIMENTAL EVIDENCE / OUR INFERENCE kept strictly separate"),
    ("11. Prior-art occupancy", "CONCEPT_PRECEDENT / STRONG_NEIGHBOR / DIRECT_OCCUPATION / EFFECTIVELY_SOLVED / NOT_RELEVANT"),
    ("12. Research verdict", "DECISION_RELEVANT / SUPPORTING / COUNTEREVIDENCE / ARCHIVE"),
]


SUP = re.compile(r"<sup>.*?</sup>", re.S)
MARK = re.compile(r"[\u2217\u2020\u2021*\u00b0\u00a7]+")
# A front-matter line stops being an author line as soon as one of these occurs:
# MinerU frequently prints affiliations on the same line as the author list.
AFFIL = re.compile(
    r"universit|institute|school|college|laborator|\blabs?\b|\binc\b|\bltd\b|corp|"
    r"academy|department|\bcenter\b|\bcentre\b|\bIIIS\b|CASIA|"
    r"http|www\.|@|\bPurdue\b|\bTsinghua\b|\bNanyang\b|\bMacau\b|\bXiaomi\b",
    re.I,
)
NAME_CHARS = re.compile(r"^[A-Za-z.,\-' ]+$")


def _person_segment(seg: str) -> bool:
    """True when a comma-separated fragment looks like one person's name."""
    toks = seg.split()
    if not 2 <= len(toks) <= 4:
        return False
    for t in toks:
        if not re.match(r"^[A-Z][A-Za-z.'\-]*$", t):
            return False
        if len(t) >= 3 and t.isupper():      # UCLA, UCSD, IIIS are not names
            return False
    return True


def _salvage_name(seg: str):
    """Keep the leading name of a segment that ends in an institution marker.

    "Bolei Zhou UCLA UCSD Qualcomm" -> "Bolei Zhou": tokens are taken while they
    look like name words and the run stops at the first all-caps token, so an
    author is not lost merely because the affiliation shares the segment.
    """
    keep = []
    for t in seg.split():
        if (len(t) >= 3 and t.isupper()) or not re.match(r"^[A-Z][A-Za-z.'\-]*$", t):
            break
        keep.append(t)
        if len(keep) == 3:
            break
    return " ".join(keep) if 2 <= len(keep) <= 3 else None


def _author_fragments(path: str) -> list:
    """Collect page-1 author fragments from the raw MD front matter, verbatim.

    Only <sup> markers are stripped and the run is cut at the first affiliation
    marker, so no name is invented and none is completed from memory. Author
    lists that MinerU spreads over several lines are concatenated; space-separated
    lists are kept as printed rather than being split (splitting would break
    multi-word names such as "Brian C. Williams").
    """
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            lines = [l.strip() for l in fh.read().splitlines()[:24]]
    except OSError:
        return []
    frags = []
    for line in lines:
        if not line or line.startswith("#") or line.startswith("!") or line.startswith("|"):
            continue
        low = line.lower()
        if low.startswith("abstract") or "abstract:" in low:
            break
        # MinerU sometimes splits a <sup> tag across lines, leaving a dangling tag that
        # would otherwise look like a digit and stop the author scan.
        clean = SUP.sub("", line)
        clean = re.sub(r"<sup>.*$", "", clean).replace("</sup>", "")
        clean = re.sub(r"\s{2,}", " ", MARK.sub("", clean)).strip(" ,;")
        if not clean:
            continue
        m = AFFIL.search(clean)
        head = clean[:m.start()].strip(" ,;") if m else ""
        if m and not frags and head:
            # author list glued to its affiliation on one line
            if "," in head:
                kept = []
                for seg in head.split(","):
                    seg = seg.strip()
                    if _person_segment(seg):
                        kept.append(seg)
                        continue
                    salv = _salvage_name(seg)
                    if salv:
                        kept.append(salv)
                    break
                frags.append(", ".join(kept) if kept else head)
            elif NAME_CHARS.match(head) and not re.search(r"\d", head):
                frags.append(head)
        if m:
            break
        if not NAME_CHARS.match(clean) or re.search(r"\d", clean):
            break
        frags.append(clean)
        if len(frags) >= 6:
            break
    return frags


def authors_from_raw_md(path: str):
    frags = [f for f in _author_fragments(path) if f]
    if not frags:
        return None
    if len(frags) == 1:
        body, note = frags[0], "verbatim page-1 front matter"
    else:
        body, note = "; ".join(frags), "verbatim page-1 front matter, author lines joined in order"
    return f"{body} ({note} of the canonical PDF, via the raw MD; superscript markers stripped)"


def num(v, fmt="{:,}"):
    return fmt.format(v) if isinstance(v, (int, float)) else "n/a"


def card(pid: str, meta: dict, dl: dict, fp: dict, raw: dict) -> str:
    short = meta["short"]
    pdf_rel = f"papers/pdf/{pid}_{short}.pdf"
    raw_rel = f"papers/raw_md/{pid}_{short}/{pid}_{short}.raw.md"
    raw_ok = raw.get("qc") == "RAW_MD_READY"

    code = meta["code_available"]
    code_line = meta["official_code_url"] or "—"
    if code == "UNKNOWN" and meta["official_code_url"]:
        code_line = f"{meta['official_code_url']} (status UNKNOWN)"

    ident = f"arXiv:{meta['arxiv_id']}" if meta["arxiv_id"] != "NONE" else f"DOI {meta['doi']}"

    L = []
    L.append(f"# {pid} — {short}")
    L.append("")
    L.append("> **SKELETON CARD — INFRASTRUCTURE ONLY.** Created by the local corpus agent during the")
    L.append("> Round 2 targeted ingest (`agent/prompts/ROUND2_TARGETED_INGEST.md`). It records metadata,")
    L.append("> provenance and ingestion/QC facts. **Every scientific section is")
    L.append(f"> `{PENDING}`**: no observed-failure verdict, no hypothesis impact, no prior-art")
    L.append("> occupancy and no research verdict is recorded here. Those are deep-read tasks")
    L.append("> (GPT-5.6 Sol), not corpus-agent tasks.")
    L.append("")
    L.append("## Metadata")
    L.append("")
    L.append(f"- **Title:** {meta['title']}")
    L.append(f"- **Year:** {meta['year']}")
    raw_md_path = os.path.join(BASE, raw_rel.replace("/", os.sep))
    authors = authors_from_raw_md(raw_md_path) or AUTHORS.get(pid, "not recorded")
    L.append(f"- **Authors:** {authors}")
    L.append(f"- **Venue:** {meta['venue']}")
    L.append(f"- **arXiv / DOI:** {ident}")
    if dl.get("sha256"):
        L.append(f"- **Canonical PDF:** `{pdf_rel}` — {num(dl.get('bytes'))} bytes, "
                 f"sha256 `{dl.get('sha256')}`")
    else:
        L.append(f"- **Canonical PDF:** NOT ACQUIRED — `{dl.get('status') or 'UNKNOWN'}`"
                 + (f" ({dl.get('error')})" if dl.get("error") else ""))
    L.append("  (SHA256 over the logical document bytes read by the canonical Python corpus I/O")
    L.append("  path. The PDF lives on local/NAS only and is never uploaded anywhere.)")
    L.append(f"- **Raw MD:** `{raw_rel}`" if raw_ok
             else "- **Raw MD:** not created (no canonical PDF)")
    L.append(f"- **Official code:** {code_line}")
    L.append("- **Repo ID:**")
    L.append("- **Last reviewed:** — (not yet reviewed)")
    if raw.get("qc"):
        reading = raw["qc"]
    elif dl.get("sha256"):
        reading = "DOWNLOADED"
    else:
        reading = "DISCOVERED"
    L.append(f"- **Reading status:** {reading}")
    verdict = fp.get("verdict")
    if verdict == "DOCUMENT_VERIFIED":
        evidence = "DOCUMENT_VERIFIED (title and first author checked against page 1 of the canonical PDF)"
    elif verdict:
        evidence = f"{verdict} (the front-page check did not confirm title and first author)"
    else:
        evidence = "INDEX_BACKED (no canonical PDF acquired, so nothing could be document-verified)"
    L.append(f"- **Evidence level:** {evidence}")
    L.append("")
    L.append("### Ingestion / QC facts (agent-recorded, not scientific)")
    L.append("")
    L.append(f"- `source_version`: {dl.get('source_version', 'UNKNOWN')}")
    L.append(f"- `canonical_url`: {dl.get('canonical_url') or '—'}")
    L.append(f"- download status: {dl.get('status', 'n/a')}"
             + (f" — {dl.get('error')}" if dl.get("error") else ""))
    if fp:
        L.append(f"- front-page verification: verdict={fp.get('verdict')}, pages={fp.get('pages')}, "
                 f"title_match={fp.get('title_match')}, "
                 f"first_author({fp.get('expected_first_author_surname')})_found={fp.get('first_author_found')}")
    if raw:
        L.append(f"- MinerU: returncode={raw.get('mineru_returncode')}, {raw.get('seconds')}s, "
                 f"backend `pipeline`, method `auto`; log `experiment_logs/mineru_{pid}.log`")
        L.append(f"- raw MD QC: {raw.get('qc')} — chars={num(raw.get('length_chars'))}, "
                 f"headings={raw.get('heading_count')}, "
                 f"images={raw.get('images_copied')}/{raw.get('image_refs_in_md')}, "
                 f"mojibake={raw.get('mojibake_total')}"
                 + (f", problems={raw.get('problems')}" if raw.get("problems") else ""))
        L.append(f"- `raw_md_sha256`: {raw.get('raw_md_sha256') or 'UNKNOWN'}")
        L.append(f"- MinerU intermediates (never canonical): "
                 f"`papers/quarantine/mineru_artifacts/{pid}_{short}/`")
    L.append("- Known extraction artifact: MinerU drops a hyphen at a line break "
             "(\"end-to-end\" → \"endtoend\"). The raw MD is raw by design; the local canonical "
             "PDF remains the exact source authority for wording, formulas and figures.")
    L.append("")
    for title, hint in SCIENTIFIC_SECTIONS:
        L.append(f"## {title}")
        L.append("")
        L.append(PENDING)
        L.append("")
    L.append("## 13. Source locations")
    L.append("")
    L.append("```text")
    L.append(f"canonical PDF : {pdf_rel}" if dl.get("sha256") else "canonical PDF : (not acquired)")
    L.append(f"raw MD        : {raw_rel}" if raw_ok else "raw MD        : (not created)")
    L.append(f"images        : papers/raw_md/{pid}_{short}/images/")
    L.append(f"official entry: {meta['official_url']}")
    L.append(f"venue page    : {meta['official_url']}")
    L.append("```")
    L.append("")
    L.append("## 14. Open questions")
    L.append("")
    L.append(PENDING)
    L.append("")
    L.append("## 15. Change log")
    L.append("")
    L.append("```text")
    L.append(f"{DATE} — skeleton card created by the local corpus agent during the Round 2")
    L.append("           targeted ingest: metadata, provenance and ingestion/QC facts only.")
    L.append("           Scientific sections deliberately left unreviewed.")
    L.append("```")
    L.append("")
    return "\n".join(L)


def main() -> int:
    ids = ROUND2
    if len(sys.argv) > 1 and not sys.argv[1].startswith("-"):
        ids = [s.strip() for s in sys.argv[1].split(",")]
    dl = {r["paper_id"]: r for r in load_all("download_results")}
    fp = {r["paper_id"]: r for r in load_all("frontpage_verification")}
    raw = {r["paper_id"]: r for r in load_all("rawmd_results")}
    os.makedirs(CARDS, exist_ok=True)
    for pid in ids:
        meta = META.get(pid)
        if not meta:
            print(f"{pid}: no META entry, skipped")
            continue
        d, f, r = dl.get(pid, {}), fp.get(pid, {}), raw.get(pid, {})
        text = card(pid, meta, d, f, r)
        path = os.path.join(CARDS, f"{pid}_{meta['short']}.md")
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
        print(f"{pid} {meta['short']:20s} -> {os.path.relpath(path, BASE)}  "
              f"({len(text)} chars, qc={r.get('qc') or d.get('status') or 'n/a'})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
