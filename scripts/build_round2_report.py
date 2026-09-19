"""Compose ROUND2_TARGETED_INGEST_REPORT.md from the Round 2 ledgers.

The report is generated rather than hand-written so that every hash, byte count and
QC number is copied straight out of manifests/batch_round2_*.json, and no identifier
is ever retyped. Scientific sections of this work are deliberately absent: the
ingest records infrastructure facts only.
"""
from __future__ import annotations

import json
import os
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_manifest import META, load_all  # noqa: E402

BASE = r"D:\zym_information\ZYM\wam\research_assets"
OUT = os.path.join(BASE, "ROUND2_TARGETED_INGEST_REPORT.md")
STAMP = date.today().isoformat()

ROLE = {
    "P0013": "A1 core P2-R attack set",
    "P0014": "A2 core P2-R attack set",
    "P0015": "A3 core P2-R attack set",
    "P0016": "A4 core P2-R attack set",
    "P0017": "A5 core P2-R attack set",
    "P0018": "H1 historical novelty control",
    "P0019": "H2 historical novelty control",
    "P0020": "H3 historical novelty control",
}
CODE_BASIS = {
    "P0013": "UNKNOWN. The paper prints a PROJECT PAGE, https://vail-ucla.github.io/BridgeSim/ (p.1), not a repository URL; the discovery hint named a repo, but the paper does not state one, so officiality is not established.",
    "P0014": "YES. The paper prints the repository URL https://github.com/Thinklab-SJTU/ReactSim-Bench on page 1, which is paper-source support for officiality. Reachability of the repository was NOT independently verified in this pass.",
    "P0015": "UNKNOWN. No repository or project URL appears anywhere in the extracted PDF text; absence of a printed URL is not evidence that no code exists.",
    "P0016": "UNKNOWN. No repository or project URL appears in the extracted PDF text.",
    "P0017": "UNKNOWN. The paper prints a PROJECT PAGE, https://currychen77.github.io/CRAFT (p.1), not a repository URL.",
    "P0018": "UNKNOWN. The paper prints a PROJECT PAGE, https://mczhi.github.io/GameFormer/ (p.1), not a repository URL.",
    "P0019": "UNKNOWN. No repository or project URL appears in the extracted PDF text.",
    "P0020": "UNKNOWN. No canonical PDF was acquired, so no document-level code statement could be read.",
}
SOURCE_NOTE = {
    "P0013": "Official arXiv preprint; no venue version verified.",
    "P0014": "Official arXiv preprint; no venue version verified.",
    "P0015": "Official arXiv preprint; no venue version verified.",
    "P0016": "Official arXiv preprint; no venue version verified.",
    "P0017": "Official arXiv preprint; no venue version verified.",
    "P0018": "Venue camera-ready, chosen over the arXiv preprint per the corpus canonical priority. Located by scanning the ICCV2023 Open Access index because CVF truncates the title inside its slug.",
    "P0019": "Venue camera-ready, chosen over the arXiv preprint per the corpus canonical priority.",
    "P0020": "No lawful open source. Paywall, not an acquisition oversight.",
}
SUPERSEDED = {
    "P0018": ("arXiv:2303.05760", "https://arxiv.org/pdf/2303.05760", 2348946,
              "e7f71bda870dcf1e58ba5ffcecb013b01dcd2c6bc4cdaf726ce97ba9141a8db6"),
}


def fmt(n):
    return f"{n:,}" if isinstance(n, int) else "n/a"


def main() -> int:
    dl = {r["paper_id"]: r for r in load_all("download_results")}
    fp = {r["paper_id"]: r for r in load_all("frontpage_verification")}
    raw = {r["paper_id"]: r for r in load_all("rawmd_results")}
    ids = [f"P{i:04d}" for i in range(13, 21)]

    L = []
    a = L.append
    a("# Round 2 Targeted Ingest Report")
    a("")
    a(f"Generated {STAMP} from `manifests/batch_round2_*.json` by `scripts/build_round2_report.py`;")
    a("every hash and count below is copied out of those ledgers, never retyped.")
    a("")
    a("**Scope.** The eight records frozen in `state/TARGETED_READING_QUEUE.md` and requested by")
    a("`agent/prompts/ROUND2_TARGETED_INGEST.md`: acquisition, canonical PDF, MinerU raw-MD text")
    a("layer and provenance/QC facts. The historical card skeletons were never a scientific")
    a("evidence layer and are not retained in the current tree.")
    a("")
    a("**Explicitly not in scope, and absent from every artifact produced here.** No scientific")
    a("reading was performed: no observed-failure verdict, no hypothesis impact, no prior-art")
    a("occupancy judgement and no research verdict is recorded. Every scientific section of the")
    a("historical card skeletons was `PENDING SCIENTIFIC REVIEW` (deep-read / GPT-5.6 Sol work). No")
    a("risk-field idea was produced.")
    a("")
    a("**Stop condition.** Reached: 7 records are `RAW_MD_READY`; 1 record (P0020) carries a")
    a("specific lawful acquisition blocker.")
    a("")
    a("**Status note (2026-09-14).** The ingest prompt `agent/prompts/ROUND2_TARGETED_INGEST.md`")
    a("is now marked `PAUSED / HISTORICAL SUBQUEUE` by the 2026-09-14 field-reconstruction reset,")
    a("which keeps these eight papers as the interactive/reactive/counterfactual branch of the")
    a("field atlas and explicitly allows them to be ingested when convenient. This report is")
    a("therefore the completed execution of that subqueue rather than an active gate: it asserts")
    a("nothing about P2-R, and no reading order or scientific verdict is implied by it.")
    a("")
    a("**Date span.** Acquisition, conversion and verification ran across the 2026-09-13 →")
    a("2026-09-14 boundary (downloads late on 09-13, conversions and verification after midnight),")
    a("so the batch ledgers and the manifest carry the label 2026-09-13 while this report is")
    a("stamped with the completion date.")
    a("")
    a("---")
    a("")
    a("## 1. ID allocation")
    a("")
    a("| paper_id | short name | role | title | year | first author | venue |")
    a("|---|---|---|---|---|---|---|")
    for pid in ids:
        m = META[pid]
        a(f"| {pid} | {m['short']} | {ROLE[pid]} | {m['title']} | {m['year']} | {m['first_author']} | {m['venue']} |")
    a("")
    a("IDs were allocated in the exact order of the prompt's target list, using the next unused")
    a("stable IDs; the highest pre-existing ID was P0012, so P0013-P0020 are new. No ID was")
    a("recycled or renumbered, and no short name collides with an existing record.")
    a("")
    a("## 2. Canonical source and source_version")
    a("")
    a("| paper_id | source_version | canonical URL | basis |")
    a("|---|---|---|---|")
    for pid in ids:
        r = dl.get(pid, {})
        a(f"| {pid} | {r.get('source_version', 'n/a')} | {r.get('canonical_url') or '(none)'} | {SOURCE_NOTE[pid]} |")
    a("")
    a("Source-version vocabulary used as defined by the corpus standard. Venue camera-ready outranks")
    a("an official arXiv version, which outranks a project-hosted copy; no project-hosted copy was")
    a("used. For A1-A5 no venue version could be verified in this pass, so the official arXiv")
    a("preprint is canonical and recorded as `arXiv_v1` rather than as a camera-ready claim.")
    a("")
    a("## 3. PDF hash / raw-MD hash")
    a("")
    a("| paper_id | PDF bytes | pdf_sha256 | raw_md_sha256 |")
    a("|---|---|---|---|")
    for pid in ids:
        r, w = dl.get(pid, {}), raw.get(pid, {})
        a(f"| {pid} | {fmt(r.get('bytes'))} | `{r.get('sha256') or 'NOT ACQUIRED'}` | `{w.get('raw_md_sha256') or 'NOT CREATED'}` |")
    a("")
    a("Hashes are SHA256 over logical document bytes read through the canonical Python corpus I/O")
    a("path. One canonical PDF per paper; PDFs and MinerU intermediates stay on local/NAS and are")
    a("never uploaded. The known native/.NET +1024 framing quirk was not re-investigated.")
    a("")
    a("## 4. Front-page verification")
    a("")
    a("| paper_id | pages | title_match | first-author surname found | verdict |")
    a("|---|---|---|---|---|")
    for pid in ids:
        r = fp.get(pid, {})
        a(f"| {pid} | {r.get('pages') or 'n/a'} | {r.get('title_match') or 'n/a'} | "
          f"{r.get('first_author_found')} ({r.get('expected_first_author_surname')}) | {r.get('verdict')} |")
    a("")
    a("Verification reads page 1 of the stored canonical PDF and requires both an exact title match")
    a("and the declared first-author surname to be present. Seven of eight records are")
    a("`DOCUMENT_VERIFIED`. P0020 has no document, so it stays `INDEX_BACKED` in this ingest record.")
    a("")
    a("## 5. Raw-MD QC")
    a("")
    a("| paper_id | chars | headings | images copied/refs | mojibake | MinerU rc | seconds | qc |")
    a("|---|---|---|---|---|---|---|---|")
    for pid in ids:
        r = raw.get(pid, {})
        if not r:
            a(f"| {pid} | - | - | - | - | - | - | NOT CREATED (no canonical PDF) |")
            continue
        a(f"| {pid} | {fmt(r.get('length_chars'))} | {r.get('heading_count')} | "
          f"{r.get('images_copied')}/{r.get('image_refs_in_md')} | {r.get('mojibake_total')} | "
          f"{r.get('mineru_returncode')} | {r.get('seconds')} | {r.get('qc')} |")
    a("")
    a("Gates applied to every conversion: title heading present, abstract present, headings present,")
    a("references present, length above the floor, mojibake ratio within tolerance, and every image")
    a("referenced by the raw MD present on disk. All seven conversions passed with zero mojibake and")
    a("no missing images; no record needed a second attempt in this batch. Raw MD is raw by design")
    a("and is not edited to improve scientific content, including the known MinerU hyphen-drop at")
    a("line breaks (\"end-to-end\" -> \"endtoend\"); the PDF remains the exact source authority.")
    a("")
    a("## 6. Official code status and evidence basis")
    a("")
    a("| paper_id | code_available | official_code_url | evidence basis |")
    a("|---|---|---|---|")
    for pid in ids:
        m = META[pid]
        a(f"| {pid} | {m['code_available']} | {m['official_code_url'] or '(none stated)'} | {CODE_BASIS[pid]} |")
    a("")
    a("Rule applied: `code_available=YES` only when the paper/project/author source itself supports")
    a("officiality. Repository-name pattern matching was not treated as evidence, no repository was")
    a("cloned, and repository reachability was not probed in this pass. A printed project page is")
    a("recorded in this ingest report but leaves the field `UNKNOWN` rather than `YES`.")
    a("")
    a("## 7. Download / conversion failures")
    a("")
    a("1. **P0020 Bahram et al. 2016 - acquisition blocked (specific and lawful).** Status recorded")
    a("   verbatim as `DOWNLOAD_BLOCKED`, `source_version=none_available`: the DOI")
    a("   (`10.1109/TVT.2015.2508009`) resolves to the IEEE Xplore landing page (HTTP 202, HTML, not")
    a("   a PDF) and no lawful open version was found. Unofficial mirrors are excluded by the ingest")
    a("   prompt, so no PDF is stored and no raw MD could be produced.")
    a("2. **P0018 GameFormer - camera-ready URL not guessable.** Three pattern-derived full-title CVF")
    a("   slugs returned HTTP 404. Cause: CVF truncates the title inside its slug. Resolved by")
    a("   scanning the ICCV2023 Open Access index page for `GameFormer`, which yielded the working")
    a("   camera-ready PDF and its landing page.")
    a("3. **Web search was unavailable** for this session (the provider returned `Insufficient")
    a("   Balance`), so no URL was confirmed by a search engine. Every source decision above rests on")
    a("   direct HTTPS probes of the candidate URLs (status code plus `%PDF-` magic, TLS verified")
    a("   with the certifi bundle) or on an official index page. The delegated URL-verification")
    a("   subagent was stopped once these questions had been resolved locally, to avoid duplicated")
    a("   spend; its report therefore contributes nothing to this ingest.")
    a("4. **Conversions: none failed.** 7/7 acquired PDFs converted and passed QC. The two runs used")
    a("   reduced MinerU thread counts (render 2, max 4) and were executed sequentially rather than")
    a("   concurrently, because Batch 0A showed a resource peak that can kill the local MinerU API")
    a("   service; no such failure occurred here.")
    a("5. **Host filesystem-view flapping (environmental, not a data defect).** During this session")
    a("   the workspace intermittently reported existing files as missing to native/.NET and")
    a("   Python file APIs (for example a script that had just been patched). Every affected step")
    a("   was retried and re-verified; no artifact was written twice with different content and no")
    a("   ledger lost records. This is recorded because it explains why some steps were repeated.")
    a("")
    a("## 8. Provenance conflicts")
    a("")
    a("1. **P0018 canonical source changed mid-ingest.** The paper was first downloaded from arXiv")
    for pid, vals in SUPERSEDED.items():
        tag, url, nbytes, sha = vals
        a(f"   (`{tag}`, {url}, {fmt(nbytes)} bytes, sha256 `{sha}`) and then superseded by the venue")
    a("   camera-ready, because venue camera-ready outranks a preprint under the corpus priority.")
    a("   The stored canonical PDF and every derived artifact come from the camera-ready; the")
    a("   superseded download is recorded here as the audit trail. Only one canonical PDF exists.")
    a("2. **BridgeSim repository hint vs paper text (unresolved, not denied).** The discovery index")
    a("   named a GitHub repository, but the paper itself prints only a project page. Under the")
    a("   official-code rule the record stays `UNKNOWN`; a later verification pass may upgrade it.")
    a("3. **A1-A5 venue status.** All five are arXiv preprints with no venue version verified in")
    a("   this pass. Their `source_version` is therefore `arXiv_v1`, and no camera-ready claim is")
    a("   made. If a venue version appears later, the canonical source must be re-acquired and the")
    a("   record re-verified rather than edited in place.")
    a("4. **Affiliation facts read from page 1 only.** First-author affiliations noted in this report")
    a("   (Purdue / Bosch Center for AI for P0016; Tsinghua University / Li Auto for P0017) come")
    a("   from the papers' own front matter. Nothing was inferred from external sources.")
    a("5. **No title, author or acronym conflict was found** for A1-A5, H1 or H2: titles matched")
    a("   exactly and the declared first author was present in all seven documents.")
    a("")
    a("## 9. Exact list of GitHub files added/updated")
    a("")
    a("**Added**")
    a("")
    for pid in ids:
        m = META[pid]
        r = raw.get(pid, {})
        if r:
            a(f"- `papers/raw_md/{pid}_{m['short']}/{pid}_{m['short']}.raw.md`")
            a(f"- `papers/raw_md/{pid}_{m['short']}/images/` ({r.get('images_copied')} files)")
    for pid in ids:
        if raw.get(pid):
            a(f"- `experiment_logs/mineru_{pid}.log`")
    a("- `manifests/batch_round2_download_results.json`")
    a("- `manifests/batch_round2_frontpage_verification.json`")
    a("- `manifests/batch_round2_rawmd_results.json`")
    a("- `scripts/build_round2_report.py`")
    a("- `ROUND2_TARGETED_INGEST_REPORT.md` (this file)")
    a("")
    a("**Updated**")
    a("")
    a("- `manifests/CORPUS_MANIFEST.csv` (regenerated: 20 rows, 25 columns; the 12 Batch 0A rows are")
    a("  unchanged, and the batch ledgers are now merged rather than replaced)")
    a("- `scripts/fetch_canonical_pdfs.py` (Round 2 sources; batch-aware ledger path; merge-on-write)")
    a("- `scripts/verify_frontpage.py` (Round 2 expectations; batch-aware ledger; `--only` filter;")
    a("  merge-on-write)")
    a("- `scripts/build_raw_md.py` (Round 2 papers; batch-aware ledger; merge-on-write)")
    a("- `scripts/build_manifest.py` (Round 2 metadata; `ORDER` extended to 20; ledgers are now")
    a("  merged across batches so a targeted re-run cannot truncate another batch's provenance)")
    a("")
    a("**Never pushed, by rule and by verification:** `papers/pdf/*.pdf` (gitignored, local/NAS")
    a("authority), `papers/quarantine/**` (MinerU intermediates), any checkpoint or dataset.")
    a("")
    a("## Decision points for the owner")
    a("")
    a("1. **`decision_relevance` is `MEDIUM` for all eight new records.** The schema reserves `HIGH`")
    a("   for adjudicated evidence (a kill/weaken, a direct observed failure, novelty occupation, a")
    a("   key counterexample, or a changed research decision). Nothing here has been deep-read, so")
    a("   marking any of them `HIGH` would assert relevance that has not been adjudicated. If the")
    a("   owner wants a different convention for the frozen target set, this is a one-line change")
    a("   plus a manifest regeneration.")
    a("2. **P0020 is unreadable as stored.** It stays `INDEX_BACKED` / `DISCOVERED` with no PDF and")
    a("   no raw MD, exactly like P0008 NPPC. Options are an authorised copy through the owner's")
    a("   institutional access, or accepting the record as permanently index-level.")
    a("3. **Historical card skeletons were infrastructure only.** Filling sections 1-12 and 14")
    a("   was the deep-read task; that layer is retired and the reading queue order was not changed")
    a("   by this ingest.")
    a("")
    return _write(L)


def _write(L):
    text = "\n".join(L) + "\n"
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print(f"wrote {OUT}")
    print(f"  {len(text)} chars, {len(L)} lines")
    print(f"  PENDING SCIENTIFIC REVIEW occurrences in report: {text.count('PENDING SCIENTIFIC REVIEW')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
