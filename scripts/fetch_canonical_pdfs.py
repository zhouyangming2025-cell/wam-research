"""Batch 0A canonical PDF acquisition (Step 4).

Compliance with the approved policy:
  - TLS certificate verification ON, using an explicit certifi CA bundle
    (the host's OpenSSL default trust store is missing entirely; see report).
  - verify=False is NEVER used.
  - redirects followed, timeout enforced, bounded retry with backoff.
  - download to <target>.part, HTTP status validated, PDF magic validated.
  - SHA256 computed after validation, atomic rename only after validation.
  - no silent fallback to a third-party mirror: on failure the entry is
    recorded as DOWNLOAD_BLOCKED with the real reason.

Usage:  python fetch_canonical_pdfs.py [--only P0001,P0005] [--dry-run]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import ssl
import sys
import time
import urllib.error
import urllib.request

BASE = r"D:\zym_information\ZYM\wam\research_assets"
PDF_DIR = os.path.join(BASE, "papers", "pdf")
RESULTS = os.path.join(BASE, "manifests", "batch_0a_download_results.json")

TIMEOUT = 90
ATTEMPTS = 3
BACKOFF = (3, 8, 20)          # seconds between attempts
USER_AGENT = "wam-corpus-ingest/1.0 (research asset acquisition)"
ARXIV_DELAY = 3.0             # be polite to arXiv between requests
MIN_PDF_BYTES = 20_000        # anything smaller is an error page, not a paper

# Canonical source policy (§5): venue camera-ready > selected official arXiv
# version > official project-hosted PDF. One canonical PDF per paper.
# `alternate_official` is RECORDED for provenance but is never auto-fetched.
SOURCES = [
    dict(paper_id="P0001", short="Epona",
         url="https://openaccess.thecvf.com/content/ICCV2025/papers/"
             "Zhang_Epona_Autoregressive_Diffusion_World_Model_for_Autonomous_Driving_"
             "ICCV_2025_paper.pdf",
         source_version="ICCV2025_camera_ready",
         basis="venue camera-ready (CVF Open Access)"),
    dict(paper_id="P0002", short="SafeDrive",
         url="https://openaccess.thecvf.com/content/CVPR2026/papers/"
             "Kim_SafeDrive_Fine-Grained_Safety_Reasoning_for_End-to-End_Driving_in_a_Sparse_"
             "CVPR_2026_paper.pdf",
         source_version="CVPR2026_camera_ready",
         basis="venue camera-ready (CVF Open Access)"),
    dict(paper_id="P0003", short="GraphAD",
         url="https://arxiv.org/pdf/2403.19098",
         source_version="arXiv_v1",
         basis="IJCAI 2024 camera-ready URL not verified -> official arXiv version",
         alternate_official="https://www.ijcai.org/proceedings/2024/0270.pdf (PATTERN-DERIVED, unverified)"),
    dict(paper_id="P0004", short="BeTop",
         url="https://proceedings.neurips.cc/paper_files/paper/2024/file/"
             "a862f5788fd09bb6843c694d8120d50c-Paper-Conference.pdf",
         source_version="NeurIPS2024_camera_ready",
         basis="venue camera-ready (NeurIPS proceedings)"),
    dict(paper_id="P0005", short="RiskWorld",
         url="https://arxiv.org/pdf/2608.21414",
         source_version="arXiv_v1",
         basis="official arXiv version (preprint, no venue version)"),
    dict(paper_id="P0006", short="GenDrive",
         url="https://arxiv.org/pdf/2410.05582",
         source_version="arXiv_v1",
         basis="ICRA 2025 camera-ready is IEEE-paywalled -> official arXiv version"),
    dict(paper_id="P0007", short="DriveReward",
         url="https://arxiv.org/pdf/2606.08525",
         source_version="arXiv_v1",
         basis="official arXiv version (preprint, no venue version)"),
    dict(paper_id="P0008", short="NPPC",
         url=None,
         source_version="none_available",
         basis="no open canonical source: IEEE RA-L 2026, paywalled, no arXiv version",
         blocked_reason="PAYWALLED_NO_OPEN_SOURCE (IEEE Xplore doc 11393633, DOI 10.1109/LRA.2026.3663819)"),
    dict(paper_id="P0009", short="DriveLaW",
         url="https://openaccess.thecvf.com/content/CVPR2026/papers/"
             "Xia_DriveLaW_Unifying_Planning_and_Video_Generation_in_a_Latent_Driving_"
             "CVPR_2026_paper.pdf",
         source_version="CVPR2026_camera_ready",
         basis="venue camera-ready (CVF Open Access)"),
    dict(paper_id="P0010", short="TOAD",
         url="https://arxiv.org/pdf/2606.07170",
         source_version="arXiv_v1",
         basis="official arXiv version (preprint, no venue version)"),
    dict(paper_id="P0011", short="SensitivityShaping",
         url="https://arxiv.org/pdf/2606.14585",
         source_version="arXiv_v1",
         basis="official arXiv version (venue unresolved)"),
    dict(paper_id="P0012", short="DAWAM",
         url="https://arxiv.org/pdf/2608.19085",
         source_version="arXiv_v1",
         basis="official arXiv version (preprint, no venue version)"),
]


def tls_context() -> ssl.SSLContext:
    """Verification ON. Prefer certifi; fail loudly if no CA bundle exists."""
    try:
        import certifi
        ctx = ssl.create_default_context(cafile=certifi.where())
        ctx.check_hostname = True
        ctx.verify_mode = ssl.CERT_REQUIRED
        return ctx
    except ImportError:
        ctx = ssl.create_default_context()
        if ctx.cert_store_stats().get("x509_ca", 0) == 0:
            raise SystemExit(
                "FATAL: no CA bundle available (certifi missing and the system "
                "OpenSSL store is empty). Refusing to disable verification.")
        return ctx


def sha256_of(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch(entry: dict, ctx: ssl.SSLContext) -> dict:
    pid, short, url = entry["paper_id"], entry["short"], entry["url"]
    name = f"{pid}_{short}.pdf"
    target = os.path.join(PDF_DIR, name)
    part = target + ".part"
    rec = dict(paper_id=pid, short_name=short, canonical_url=url,
               source_version=entry["source_version"], basis=entry["basis"],
               local_path=target, status=None, http=None, content_type=None,
               bytes=None, sha256=None, attempts=0, error=None,
               alternate_official=entry.get("alternate_official"))

    if url is None:
        rec["status"] = "DOWNLOAD_BLOCKED"
        rec["error"] = entry.get("blocked_reason", "no canonical source")
        return rec

    last_err = None
    for i in range(ATTEMPTS):
        rec["attempts"] = i + 1
        if os.path.exists(part):
            os.remove(part)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=TIMEOUT, context=ctx) as r:
                rec["http"] = r.status
                rec["content_type"] = r.headers.get("Content-Type")
                final = r.geturl()
                rec["final_url"] = final if final != url else None
                if r.status != 200:
                    raise RuntimeError(f"unexpected HTTP status {r.status}")
                total = 0
                with open(part, "wb") as f:
                    while True:
                        chunk = r.read(1 << 20)
                        if not chunk:
                            break
                        f.write(chunk)
                        total += len(chunk)
            rec["bytes"] = total
            if total < MIN_PDF_BYTES:
                raise RuntimeError(f"body too small ({total} bytes) - not a paper PDF")
            with open(part, "rb") as f:
                magic = f.read(1024)
            if b"%PDF-" not in magic:
                raise RuntimeError(f"PDF magic missing; first bytes={magic[:16]!r}")
            rec["sha256"] = sha256_of(part)
            os.replace(part, target)          # atomic rename after validation
            rec["status"] = "DOWNLOADED"
            rec["error"] = None
            return rec
        except urllib.error.HTTPError as e:
            last_err = f"HTTPError {e.code} {e.reason}"
        except Exception as e:
            last_err = f"{type(e).__name__}: {e}"
        if os.path.exists(part):
            os.remove(part)
        if i < ATTEMPTS - 1:
            time.sleep(BACKOFF[i])

    rec["status"] = "DOWNLOAD_BLOCKED"
    rec["error"] = last_err
    return rec


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="comma-separated paper ids")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    todo = SOURCES
    if args.only:
        keep = {s.strip() for s in args.only.split(",")}
        todo = [s for s in SOURCES if s["paper_id"] in keep]

    os.makedirs(PDF_DIR, exist_ok=True)
    ctx = tls_context()
    print(f"TLS: verification ON, CA bundle in use", flush=True)

    results = []
    for entry in todo:
        url = entry["url"] or ""
        print(f"[{entry['paper_id']}] {entry['short']} <- {url or '(none)'}", flush=True)
        if args.dry_run:
            results.append(dict(paper_id=entry["paper_id"], status="DRY_RUN"))
            continue
        rec = fetch(entry, ctx)
        results.append(rec)
        if rec["status"] == "DOWNLOADED":
            print(f"    OK {rec['bytes']} bytes  sha256={rec['sha256'][:32]}...", flush=True)
        else:
            print(f"    {rec['status']}: {rec['error']}", flush=True)
        if url.startswith("https://arxiv.org"):
            time.sleep(ARXIV_DELAY)

    with open(RESULTS, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    ok = sum(1 for r in results if r["status"] == "DOWNLOADED")
    blocked = [r["paper_id"] for r in results if r["status"] == "DOWNLOAD_BLOCKED"]
    print(f"\nsummary: downloaded={ok}/{len(results)} blocked={blocked or 'none'}", flush=True)
    print(f"results -> {RESULTS}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
