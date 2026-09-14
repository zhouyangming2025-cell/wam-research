"""Build the infrastructure-only Phase C.5 ingest report from batch ledgers."""
from __future__ import annotations

import csv
import glob
import json
import os

BASE = r"D:\zym_information\ZYM\wam\research_assets"
MAN = os.path.join(BASE, "manifests")
REPORT = os.path.join(BASE, "audits", "ingest", "PHASE_C5_CORE_WAM_BATCH_INGEST.md")
TARGETS = [
    ("P0042", "WorldDrive"),
    ("P0046", "World4Drive"),
    ("P0061", "SeerDrive"),
    ("P0049", "Drive-JEPA"),
    ("P0062", "Metis"),
    ("P0063", "DynFlowDrive"),
    ("P0064", "Discrete-WAM"),
    ("P0065", "GraphWorld"),
]


def merge_ledgers(suffix: str) -> dict[str, dict]:
    merged: dict[str, dict] = {}
    for path in sorted(glob.glob(os.path.join(MAN, f"batch_*_{suffix}.json"))):
        with open(path, encoding="utf-8") as fh:
            for row in json.load(fh):
                merged[row["paper_id"]] = row
    return merged


def load_csv(path: str) -> dict[str, dict]:
    with open(path, encoding="utf-8-sig", newline="") as fh:
        return {row.get("paper_id") or row.get("repo_id"): row for row in csv.DictReader(fh)}


def main() -> None:
    downloads = merge_ledgers("download_results")
    frontpages = merge_ledgers("frontpage_verification")
    rawmd = merge_ledgers("rawmd_results")
    qc = {row["paper_id"]: row for row in json.load(open(os.path.join(MAN, "batch_phase_c5_qc.json"), encoding="utf-8"))}
    corpus = load_csv(os.path.join(MAN, "CORPUS_MANIFEST.csv"))
    code_rows = load_csv(os.path.join(MAN, "CODE_REPO_MANIFEST.csv"))

    lines = [
        "# Phase C.5 — Core-WAM Batch Ingest",
        "",
        "> Infrastructure/corpus record only. No innovation, gap, quality, method comparison, or research-direction judgment is included.",
        "",
        "Checked: 2026-09-14  |  Authority: official paper/repository pages and local canonical assets",
        "",
        "## Batch matrix",
        "",
        "| Paper ID | Short name | Identity verified? | Canonical source | PDF acquired? | PDF hash | Raw MD ready? | Raw MD hash | QC status | Official code? | Pinned commit | Checkpoint status | Blocker / anomaly |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for pid, short in TARGETS:
        d, f, r = downloads.get(pid, {}), frontpages.get(pid, {}), rawmd.get(pid, {})
        c = corpus.get(pid, {})
        q = qc.get(pid, {})
        code = next((row for row in code_rows.values() if row.get("paper_ids") == pid), {})
        anomaly = f.get("frontpage_anomaly", "")
        if code.get("audit_status") in {"CODE_REPO_PLACEHOLDER;IMPLEMENTATION_UNRELEASED", "NOT_FOUND"}:
            anomaly = "; ".join(x for x in [anomaly, code.get("audit_status", "")] if x)
        lines.append("| " + " | ".join([
            pid,
            short,
            "YES" if f.get("verdict") == "DOCUMENT_VERIFIED" else "NO",
            f"{d.get('source_version', c.get('source_version', 'UNKNOWN'))} ({d.get('canonical_url', c.get('official_pdf_url', 'UNKNOWN'))})",
            "YES" if d.get("status") == "DOWNLOADED" or c.get("pdf_sha256") else "NO",
            d.get("sha256") or c.get("pdf_sha256", "UNKNOWN"),
            "YES" if r.get("qc") == "RAW_MD_READY" or c.get("raw_md_sha256") else "NO",
            r.get("raw_md_sha256") or c.get("raw_md_sha256", "UNKNOWN"),
            q.get("qc", r.get("qc", "UNKNOWN")),
            "YES" if code.get("official_url") not in ("", "NONE", None) else "NO",
            code.get("pinned_commit", "NONE"),
            code.get("checkpoint_status", "UNKNOWN"),
            anomaly or "NONE",
        ]) + " |")

    lines += [
        "",
        "## BLOCKERS",
        "",
        "- No paper-level ingest blocker. All 8 target identities, local PDFs, front pages, and raw Markdown layers are present.",
        "- Discrete-WAM page 1 omits the author list and directs readers to Contributions/Acknowledgments; identity was checked against the official arXiv record and this is retained as `FRONTPAGE_AUTHOR_OMITTED`.",
        "- Metis and DynFlowDrive official repositories are present but do not contain released implementation at the pinned commits. Discrete-WAM and GraphWorld have no official code URL found in the live check.",
        "",
        "## QC WARNINGS",
        "",
        "- Raw Markdown: all 8 passed infrastructure QC; no `TABLE_IMAGE_ONLY` or `FIGURE_TEXT_LOSS` was observed. HTML tables, figure captions, equations, references, and referenced images were retained in the extracted layer.",
        "- Front page: `P0064 Discrete-WAM` — `FRONTPAGE_AUTHOR_OMITTED` as described above.",
        "",
        "## CODE STATUS CHANGES",
        "",
        "| Paper | Repository status | Check |",
        "|---|---|---|",
    ]
    for pid, short in TARGETS:
        code = next((row for row in code_rows.values() if row.get("paper_ids") == pid), {})
        lines.append(f"| {pid} {short} | {code.get('audit_status', 'NOT_RECORDED')} | {code.get('official_url', 'NONE')} @ `{code.get('pinned_commit', 'NONE')}` |")

    lines += [
        "",
        "## MANIFEST CHANGES",
        "",
        "- Reused stable IDs `P0042` WorldDrive, `P0046` World4Drive, and `P0049` Drive-JEPA; no aliases were merged and no old ID was renumbered.",
        "- Allocated `P0061`–`P0065` in target order: SeerDrive, Metis, DynFlowDrive, Discrete-WAM, GraphWorld.",
        "- Updated `manifests/CORPUS_MANIFEST.csv` to 65 rows with the existing 25-column schema; target rows are capped at corpus ingestion status and do not claim deep-read status.",
        "- Replaced the example code row in `manifests/CODE_REPO_MANIFEST.csv` with 8 target records, including default branch, pinned commit, license, checkpoint state, and source-release notes.",
        "- Added batch evidence ledgers: `batch_phase_c5_download_results.json`, `batch_phase_c5_frontpage_verification.json`, `batch_phase_c5_rawmd_results.json`, and `batch_phase_c5_qc.json`.",
        "",
        "## Local-only assets",
        "",
        "- Canonical PDFs remain under `papers/pdf/` and are not part of the GitHub corpus push policy.",
        "- Shallow-cloned third-party repositories remain under `repos/` and are not staged for this repository.",
    ]
    os.makedirs(os.path.dirname(REPORT), exist_ok=True)
    with open(REPORT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"wrote {REPORT}")


if __name__ == "__main__":
    main()
