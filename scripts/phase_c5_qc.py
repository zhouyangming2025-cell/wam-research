"""Infrastructure-only QC for the Phase C.5 raw Markdown layer.

This deliberately reports extraction observations rather than interpreting a
paper's method or evidence. It is safe to re-run and writes one batch ledger.
"""
from __future__ import annotations

import hashlib
import json
import os
import re

BASE = r"D:\zym_information\ZYM\wam\research_assets"
RAW = os.path.join(BASE, "papers", "raw_md")
MAN = os.path.join(BASE, "manifests")
OUT = os.path.join(MAN, "batch_phase_c5_qc.json")

PAPERS = [
    ("P0042", "WorldDrive"),
    ("P0046", "World4Drive"),
    ("P0049", "DriveJEPA"),
    ("P0061", "SeerDrive"),
    ("P0062", "Metis"),
    ("P0063", "DynFlowDrive"),
    ("P0064", "Discrete-WAM"),
    ("P0065", "GraphWorld"),
]

IMG_RE = re.compile(r"!\[[^\]]*\]\((?:\./)?(images/[^)\s]+)\)")
HEADING_RE = re.compile(r"^#{1,6}\s+\S", re.M)
MOJIBAKE = ("\ufffd", "锟", "鈥", "搂", "脗", "â€", "Ã")


def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def count_patterns(text: str, patterns: list[str]) -> int:
    return sum(len(re.findall(p, text, re.I | re.M)) for p in patterns)


def qc(pid: str, short: str) -> dict:
    key = f"{pid}_{short}"
    md_path = os.path.join(RAW, key, f"{key}.raw.md")
    rec = {"paper_id": pid, "short_name": short, "raw_md_path": md_path}
    if not os.path.exists(md_path):
        rec.update(qc="RAW_MD_BLOCKED", blocker="raw Markdown missing")
        return rec
    with open(md_path, encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    low = text.lower()
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    refs = sorted(set(IMG_RE.findall(text)))
    img_dir = os.path.join(os.path.dirname(md_path), "images")
    missing = [r for r in refs if not os.path.exists(os.path.join(img_dir, os.path.basename(r)))]
    line_counts = {}
    for line in lines:
        if len(line) >= 24:
            line_counts[line] = line_counts.get(line, 0) + 1
    repeated = sorted((n, line[:140]) for line, n in line_counts.items() if n >= 5)
    bad = {mark: text.count(mark) for mark in MOJIBAKE if text.count(mark)}
    body = IMG_RE.sub("", text)
    table_caps = count_patterns(text, [r"^(?:table|tab\.)\s*[0-9]"])
    figure_caps = count_patterns(text, [r"^(?:figure|fig\.)\s*[0-9]"])
    equation_like = count_patterns(text, [r"\$\$", r"\\begin\{(?:equation|aligned|array)", r"\\tag\{"])
    checks = {
        "has_abstract": "abstract" in low,
        "has_method_or_approach": bool(re.search(r"\b(method|methodology|approach|framework)\b", low)),
        "has_experiments_or_results": bool(re.search(r"\b(experiments?|results?|evaluation)\b", low)),
        "has_conclusion": "conclusion" in low,
        "has_references": bool(re.search(r"\b(references|bibliography)\b", low)),
    }
    warnings = []
    if not checks["has_method_or_approach"]:
        warnings.append("MISSING_METHOD_SECTION_MARKER")
    if not checks["has_experiments_or_results"]:
        warnings.append("MISSING_EXPERIMENTS_SECTION_MARKER")
    if not checks["has_conclusion"]:
        warnings.append("MISSING_CONCLUSION_MARKER")
    if not checks["has_references"]:
        warnings.append("MISSING_REFERENCES_MARKER")
    if bad:
        warnings.append("MOJIBAKE")
    if missing:
        warnings.append("MISSING_REFERENCED_IMAGES")
    if len(body.strip()) < 2000:
        warnings.append("BODY_EMPTY_OR_IMAGE_ONLY")
    if len(repeated) >= 4:
        warnings.append("REPEATED_TEXT_BLOCKS")
    # Only flag image-only tables when the extracted text itself explicitly
    # presents a table caption next to an image and no table text marker.
    if table_caps and not re.search(r"\|[^\n]+\|", text) and "<table" not in low:
        warnings.append("TABLE_IMAGE_ONLY")
    rec.update({
        "char_count": len(text),
        "heading_count": len(HEADING_RE.findall(text)),
        "table_caption_count": table_caps,
        "figure_caption_count": figure_caps,
        "equation_like_line_count": equation_like,
        "image_ref_count": len(refs),
        "image_present_count": len(refs) - len(missing),
        "missing_images": missing,
        "mojibake_total": sum(bad.values()),
        "repeated_text_blocks": repeated,
        "body_char_count_without_image_links": len(body.strip()),
        "checks": checks,
        "warnings": warnings,
        "raw_md_sha256": sha256(md_path),
        "qc": "RAW_MD_READY" if not warnings else "RAW_MD_READY_WITH_WARNINGS",
    })
    return rec


def main() -> None:
    rows = [qc(pid, short) for pid, short in PAPERS]
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(rows, fh, indent=2, ensure_ascii=False)
    for r in rows:
        print(f"{r['paper_id']} {r['short_name']}: {r['qc']} chars={r.get('char_count', 0)} "
              f"headings={r.get('heading_count', 0)} tables={r.get('table_caption_count', 0)} "
              f"figures={r.get('figure_caption_count', 0)} equations={r.get('equation_like_line_count', 0)} "
              f"warnings={','.join(r.get('warnings', [])) or '-'}")
    print(f"results -> {OUT}")


if __name__ == "__main__":
    main()
