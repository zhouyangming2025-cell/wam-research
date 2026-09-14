"""Batch 0A raw MD layer: MinerU conversion -> migration -> QC.

Phase 2 of Step 4-8. Per paper:
  1. run MinerU (pipeline backend, auto method) with output into
     papers/quarantine/mineru_artifacts/PXXXX_Short/   (kept, never deleted)
  2. migrate ONLY the final raw MD + the images it actually references into
     papers/raw_md/PXXXX_Short/PXXXX_Short.raw.md + images/
  3. QC the MD (title / abstract / headings / references / length / encoding)
  4. record result to manifests/batch_0a_rawmd_results.json

_origin.pdf / _layout.pdf / _span.pdf / content_list.json stay in quarantine and
are never treated as canonical. No piped stdio: child output goes to log files.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time

BASE = r"D:\zym_information\ZYM\wam\research_assets"
PDF_DIR = os.path.join(BASE, "papers", "pdf")
RAW_DIR = os.path.join(BASE, "papers", "raw_md")
STAGE = os.path.join(BASE, "papers", "quarantine", "mineru_artifacts")
LOG_DIR = os.path.join(BASE, "experiment_logs")
MAN = os.path.join(BASE, "manifests")
# Batch label selects the results ledger. The default reproduces the Batch 0A
# file exactly; CORPUS_BATCH=round2 writes the Round 2 targeted-ingest ledger, so
# a targeted re-run can never truncate another batch's provenance.
BATCH = os.environ.get("CORPUS_BATCH", "0a")
OUT = os.path.join(MAN, f"batch_{BATCH}_rawmd_results.json")

MINERU = r"D:\Program Files\Mineru\venv\Scripts\mineru.exe"
MINERU_PY = r"D:\Program Files\Mineru\venv\Scripts\python.exe"
# documented entry point (mineru = mineru.cli.client:main) behind a launcher that
# activates scripts/_mineru_site/sitecustomize.py in this process AND in MinerU's
# mineru-api subprocess. See that file for the two sandbox defects it works around.
MINERU_RUNNER = os.path.join(BASE, "scripts", "run_mineru.py")
MINERU_SITE = os.path.join(BASE, "scripts", "_mineru_site")
MINERU_CONFIG = r"D:\Program Files\Mineru\mineru.json"
TIMEOUT = 5400

PAPERS = [
    ("P0001", "Epona"), ("P0002", "SafeDrive"), ("P0003", "GraphAD"),
    ("P0004", "BeTop"), ("P0005", "RiskWorld"), ("P0006", "GenDrive"),
    ("P0007", "DriveReward"), ("P0009", "DriveLaW"), ("P0010", "TOAD"),
    ("P0011", "SensitivityShaping"), ("P0012", "DAWAM"),
    # Round 2 targeted ingest: the frozen set from
    # agent/prompts/ROUND2_TARGETED_INGEST.md, in the prompt's list order. IDs were
    # allocated after confirming the live manifest's highest ID was still P0012 and
    # that none of these eight titles already existed in the corpus.
    # --- Phase-A Census Round 2 support batch (CORPUS_BATCH=census2) ---
    ("P0021", "HydraMDP"),        # F10 strong non-WM control
    ("P0022", "DriveSuprim"),     # F10 strong non-WM control
    ("P0023", "iPad"),            # F10 strong non-WM control
    ("P0024", "DriveVLM"),        # F10 representative VLA planner
    ("P0025", "OmniDrive"),       # F10 representative VLA planner
    ("P0026", "ORION"),           # F10 representative VLA planner
    ("P0027", "Think2Drive"),     # WM-RL lineage
    ("P0028", "ViDAR"),           # representation-pretraining bridge
    ("P0029", "GenAD"),           # representation-pretraining bridge
    ("P0030", "nuScenes"),        # benchmark lineage
    ("P0031", "nuPlan"),          # benchmark lineage
    ("P0032", "NAVSIM"),          # benchmark lineage
    ("P0033", "Bench2Drive"),     # benchmark lineage
    ("P0034", "HUGSIM"),          # benchmark lineage
    ("P0013", "BridgeSim"),            # A1
    ("P0014", "ReactSimBench"),        # A2
    ("P0015", "CausalDrive"),          # A3
    ("P0016", "CounterfactualPred"),   # A4
    ("P0017", "CRAFT"),                # A5
    ("P0018", "GameFormer"),           # H1
    ("P0019", "M2I"),                  # H2
    ("P0020", "Bahram2016"),           # H3
]

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

IMG_RE = re.compile(r"!\[[^\]]*\]\((?:\./)?(images/[^)\s]+)\)")
MOJIBAKE = ("\ufffd", "锟", "鈥", "搂", "脗", "â€", "Ã")


def sha256_of(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def find_md(stage_dir):
    hits = []
    for root, _dirs, files in os.walk(stage_dir):
        for fn in files:
            if fn.endswith(".md"):
                hits.append(os.path.join(root, fn))
    if not hits:
        return None
    return max(hits, key=os.path.getsize)


def qc(md_text, md_path, img_dir):
    res = {}
    low = md_text.lower()
    res["length_chars"] = len(md_text)
    res["has_title_heading"] = bool(re.search(r"^#\s+\S", md_text, re.M))
    res["has_abstract"] = "abstract" in low
    headings = re.findall(r"^#{1,4}\s+\S", md_text, re.M)
    res["heading_count"] = len(headings)
    res["has_references"] = ("references" in low or "bibliography" in low)
    bad = {m: md_text.count(m) for m in MOJIBAKE if md_text.count(m)}
    res["mojibake_marks"] = bad
    res["mojibake_total"] = sum(bad.values())
    res["mojibake_ratio"] = round(res["mojibake_total"] / max(len(md_text), 1), 6)
    refs = sorted(set(IMG_RE.findall(md_text)))
    res["image_refs_in_md"] = len(refs)
    res["images_present"] = sum(
        1 for r in refs if os.path.exists(os.path.join(img_dir, os.path.basename(r))))
    res["images_missing"] = [r for r in refs
                             if not os.path.exists(os.path.join(img_dir, os.path.basename(r)))]
    problems = []
    if res["length_chars"] < 5000:
        problems.append(f"too short ({res['length_chars']} chars)")
    if not res["has_title_heading"]:
        problems.append("no title heading")
    if not res["has_abstract"]:
        problems.append("no abstract")
    if res["heading_count"] < 3:
        problems.append(f"too few headings ({res['heading_count']})")
    if not res["has_references"]:
        problems.append("no references section")
    if res["mojibake_ratio"] > 0.002:
        problems.append(f"mojibake ratio {res['mojibake_ratio']}")
    if res["images_missing"]:
        problems.append(f"{len(res['images_missing'])} missing image files")
    res["problems"] = problems
    res["qc"] = "RAW_MD_READY" if not problems else "RAW_MD_QC_FAIL"
    return res


def convert(pid, short):
    pdf = os.path.join(PDF_DIR, f"{pid}_{short}.pdf")
    stage = os.path.join(STAGE, f"{pid}_{short}")
    log = os.path.join(LOG_DIR, f"mineru_{pid}.log")
    os.makedirs(stage, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)
    cmd = [MINERU_PY, MINERU_RUNNER, "-p", pdf, "-o", stage, "-b", "pipeline", "-m", "auto"]
    # MinerU's orchestrated CLI starts a local mineru-api and creates its
    # output_root under %TEMP%. The default temp lives outside the writable
    # root, so it must be redirected into the workspace.
    tmp = os.path.join(BASE, "papers", "quarantine", "_tmp")
    os.makedirs(tmp, exist_ok=True)
    env = dict(os.environ)
    env["TEMP"] = env["TMP"] = env["TMPDIR"] = tmp
    env["PYTHONIOENCODING"] = "utf-8"
    # activates the sandbox shims in this process and in MinerU's subprocesses
    env["MINERU_SANDBOX_SHIMS"] = "1"
    env["PYTHONPATH"] = MINERU_SITE + os.pathsep + env.get("PYTHONPATH", "")
    # bounds the render pool; the pool is thread-backed in this sandbox.
    # Overridable so a single heavy paper can be retried with less concurrency.
    env["MINERU_PDF_RENDER_THREADS"] = os.environ.get("CORPUS_PDF_RENDER_THREADS", "4")
    env["MINERU_SANDBOX_MAX_THREADS"] = os.environ.get("CORPUS_MAX_THREADS", "8")
    # MinerU resolves mineru.json relative to the CWD. Running from the corpus
    # directory would otherwise fall back to the empty %USERPROFILE%\mineru.json
    # (models-dir.pipeline = ""), which makes MinerU try to snapshot_download
    # PDF-Extract-Kit from the HuggingFace cache - unwritable here. Point it at
    # the installation config whose models-dir holds the local pipeline models
    # (2.5 GB incl. MFR/unimernet), so nothing is downloaded and no HF lock is
    # needed.
    if os.path.exists(MINERU_CONFIG):
        env["MINERU_TOOLS_CONFIG_JSON"] = MINERU_CONFIG
    t0 = time.time()
    with open(log, "w", encoding="utf-8", errors="replace") as lf:
        lf.write("CMD: " + " ".join(cmd) + "\n")
        lf.flush()
        try:
            proc = subprocess.run(cmd, stdout=lf, stderr=subprocess.STDOUT,
                                  timeout=TIMEOUT, env=env)
            rc = proc.returncode
        except subprocess.TimeoutExpired:
            rc = -9
            lf.write("\nTIMEOUT\n")
    return stage, log, rc, round(time.time() - t0, 1)


def main():
    only = None
    if len(sys.argv) > 1:
        only = {s.strip() for s in sys.argv[1].split(",")}
    # resume: keep results already achieved, skip papers that are RAW_MD_READY
    prev = {}
    if os.path.exists(OUT):
        try:
            with open(OUT, encoding="utf-8") as f:
                prev = {r["paper_id"]: r for r in json.load(f)}
        except Exception:
            prev = {}
    results = []
    for pid, short in PAPERS:
        if only and pid not in only:
            continue
        if not only and prev.get(pid, {}).get("qc") == "RAW_MD_READY":
            results.append(prev[pid])
            print(f"=== {pid} {short} : already RAW_MD_READY, skipped", flush=True)
            continue
        print(f"=== {pid} {short}", flush=True)
        rec = dict(paper_id=pid, short_name=short)
        pdf = os.path.join(PDF_DIR, f"{pid}_{short}.pdf")
        if not os.path.exists(pdf):
            rec.update(qc="RAW_MD_QC_FAIL", qc_detail="canonical PDF missing")
            results.append(rec)
            print("    PDF missing", flush=True)
            continue

        stage, log, rc, secs = convert(pid, short)
        rec.update(mineru_returncode=rc, seconds=secs, log=log, stage_dir=stage)
        if rc != 0:
            rec.update(qc="RAW_MD_QC_FAIL", qc_detail=f"MinerU exit {rc} (see {log})")
            results.append(rec)
            print(f"    MinerU failed rc={rc} ({secs}s)", flush=True)
            continue

        md = find_md(stage)
        if not md:
            rec.update(qc="RAW_MD_QC_FAIL", qc_detail="no .md produced")
            results.append(rec)
            print("    no md produced", flush=True)
            continue

        dest_dir = os.path.join(RAW_DIR, f"{pid}_{short}")
        os.makedirs(dest_dir, exist_ok=True)
        dest_md = os.path.join(dest_dir, f"{pid}_{short}.raw.md")
        with open(md, encoding="utf-8", errors="replace") as f:
            text = f.read()

        img_dir = os.path.join(dest_dir, "images")
        os.makedirs(img_dir, exist_ok=True)
        # copy only images the markdown actually references
        refs = sorted(set(IMG_RE.findall(text)))
        src_img_dir = os.path.join(os.path.dirname(md), "images")
        copied = 0
        for r in refs:
            base = os.path.basename(r)
            for cand in (os.path.join(src_img_dir, base),
                         os.path.join(os.path.dirname(md), r),
                         os.path.join(stage, r)):
                if os.path.exists(cand):
                    shutil.copy2(cand, os.path.join(img_dir, base))
                    copied += 1
                    break
        with open(dest_md, "w", encoding="utf-8") as f:
            f.write(text)

        q = qc(text, dest_md, img_dir)
        rec.update(q)
        rec["raw_md_local_path"] = dest_md
        rec["raw_md_sha256"] = sha256_of(dest_md) if q["qc"] == "RAW_MD_READY" else None
        rec["images_copied"] = copied
        rec["source_md"] = md
        results.append(rec)
        print(f"    {q['qc']} chars={q['length_chars']} headings={q['heading_count']} "
              f"imgs={copied}/{q['image_refs_in_md']} mojibake={q['mojibake_total']} "
              f"({secs}s)", flush=True)
        if q["problems"]:
            print(f"    problems: {q['problems']}", flush=True)

    # merge, never drop records: a targeted re-run must not truncate the file.
    # The ledger is re-read here, immediately before writing, because two concurrent runs
    # would otherwise each write back the snapshot they read at process start and silently
    # drop the other's records. That happened once for the census2 batch; the lost records
    # were reconstructed from the stored artifacts by scripts/repair_rawmd_ledger.py.
    latest = {}
    if os.path.exists(OUT):
        try:
            with open(OUT, encoding="utf-8") as f:
                latest = {r["paper_id"]: r for r in json.load(f)}
        except Exception:
            latest = {}
    merged = dict(latest)
    for pid, rec in prev.items():
        merged.setdefault(pid, rec)
    for r in results:
        merged[r["paper_id"]] = r
    ordered = [merged[pid] for pid, _s in PAPERS if pid in merged]

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(ordered, f, indent=2, ensure_ascii=False)
    ok = sum(1 for r in ordered if r.get("qc") == "RAW_MD_READY")
    print(f"\nsummary: RAW_MD_READY={ok}/{len(ordered)}")
    print(f"results -> {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
