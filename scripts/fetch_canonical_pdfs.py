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
# Batch label selects the results ledger. The default reproduces the Batch 0A
# file exactly; CORPUS_BATCH=round2 writes the Round 2 targeted-ingest ledger, so
# a targeted re-run can never truncate another batch's provenance.
BATCH = os.environ.get("CORPUS_BATCH", "0a")
RESULTS = os.path.join(BASE, "manifests", f"batch_{BATCH}_download_results.json")

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

    # --- Phase-A Census Round 2 support batch (CORPUS_BATCH=census2) ---
    # Coverage holes named in landscape/FIELD_ATLAS.md (F10), landscape/CENSUS_PHASE_A_ROUND1.md
    # and state/NEXT_TASK.md: strong non-WM E2E controls, WM-RL lineage, representation
    # pretraining bridges, benchmark/simulator lineage. Identities were resolved against
    # official landing pages (scripts/fetch_work_identity.py -> manifests/batch_census2_identity.json);
    # every title, first author and arXiv version below is copied from that ledger, never typed
    # from memory.
    dict(paper_id="P0021", short="HydraMDP",
         url="https://arxiv.org/pdf/2406.06978",
         source_version="arXiv_v4",
         basis="official arXiv version v4 (arXiv abs page citation_title matches exactly); no venue camera-ready verified in this batch",
         alternate_official="https://arxiv.org/abs/2406.06978"),
    dict(paper_id="P0022", short="DriveSuprim",
         url="https://arxiv.org/pdf/2506.06659",
         source_version="arXiv_v3",
         basis="official arXiv version v3. An AAAI 2026 version exists (DOI 10.1609/aaai.v40i14.38178, seen in OpenAlex), but the AAAI OJS article page returned no galley PDF link in this batch, so it could not be verified and the arXiv version stays canonical",
         alternate_official="https://arxiv.org/abs/2506.06659"),
    dict(paper_id="P0023", short="iPad",
         url="https://arxiv.org/pdf/2505.15111",
         source_version="arXiv_v1",
         basis="official arXiv version v1; the IEEE Robotics and Automation Letters version (DOI 10.1109/lra.2026.3723334) is not open, so the preprint is canonical",
         alternate_official="https://arxiv.org/abs/2505.15111"),
    dict(paper_id="P0024", short="DriveVLM",
         url="https://arxiv.org/pdf/2402.12289",
         source_version="arXiv_v5",
         basis="official arXiv version v5 (arXiv abs page citation_title matches exactly)",
         alternate_official="https://arxiv.org/abs/2402.12289"),
    dict(paper_id="P0025", short="OmniDrive",
         url="https://openaccess.thecvf.com/content/CVPR2025/papers/"
             "Wang_OmniDrive_A_Holistic_Vision-Language_Dataset_for_Autonomous_Driving_with_Counterfactual_"
             "CVPR_2025_paper.pdf",
         source_version="CVPR2025_camera_ready",
         basis="venue camera-ready (CVF Open Access). arXiv:2405.01533 v2 carries the same title on its official abs page, so the CVPR 2025 camera-ready supersedes the preprint per corpus canonical-source priority",
         alternate_official="https://openaccess.thecvf.com/content/CVPR2025/html/"
                            "Wang_OmniDrive_A_Holistic_Vision-Language_Dataset_for_Autonomous_Driving_with_Counterfactual_"
                            "CVPR_2025_paper.html"),
    dict(paper_id="P0026", short="ORION",
         url="https://openaccess.thecvf.com/content/ICCV2025/papers/"
             "Fu_ORION_A_Holistic_End-to-End_Autonomous_Driving_Framework_by_Vision-Language_Instructed_"
             "ICCV_2025_paper.pdf",
         source_version="ICCV2025_camera_ready",
         basis="venue camera-ready (CVF Open Access); located by scanning the ICCV2025 Open Access index page, because CVF truncates titles inside slugs and full-title guesses return 404",
         alternate_official="https://openaccess.thecvf.com/content/ICCV2025/html/"
                            "Fu_ORION_A_Holistic_End-to-End_Autonomous_Driving_Framework_by_Vision-Language_Instructed_"
                            "ICCV_2025_paper.html"),
    dict(paper_id="P0027", short="Think2Drive",
         url="https://arxiv.org/pdf/2402.16720",
         source_version="arXiv_v2",
         basis="official arXiv version v2; the ECCV 2024 Springer version is not open, so the preprint is canonical",
         alternate_official="https://arxiv.org/abs/2402.16720"),
    dict(paper_id="P0028", short="ViDAR",
         url="https://openaccess.thecvf.com/content/CVPR2024/papers/"
             "Yang_Visual_Point_Cloud_Forecasting_enables_Scalable_Autonomous_Driving_"
             "CVPR_2024_paper.pdf",
         source_version="CVPR2024_camera_ready",
         basis="venue camera-ready (CVF Open Access). NOTE: the camera-ready title is Visual Point Cloud Forecasting enables Scalable Autonomous Driving and does not contain the method name ViDAR used by the census; located by scanning the CVPR2024 Open Access index page",
         alternate_official="https://openaccess.thecvf.com/content/CVPR2024/html/"
                            "Yang_Visual_Point_Cloud_Forecasting_enables_Scalable_Autonomous_Driving_"
                            "CVPR_2024_paper.html"),
    dict(paper_id="P0029", short="GenAD",
         url="https://arxiv.org/pdf/2402.11502",
         source_version="arXiv_v3",
         basis="official arXiv version v3; the ECCV 2024 Springer version is not open, so the preprint is canonical",
         alternate_official="https://arxiv.org/abs/2402.11502"),
    dict(paper_id="P0030", short="nuScenes",
         url="https://openaccess.thecvf.com/content_CVPR_2020/papers/"
             "Caesar_nuScenes_A_Multimodal_Dataset_for_Autonomous_Driving_"
             "CVPR_2020_paper.pdf",
         source_version="CVPR2020_camera_ready",
         basis="venue camera-ready (CVF Open Access). CVPR 2020 uses the older CVF path layout (/content_CVPR_2020/), so the modern (CVPR20xx?day=all) index does not list it; the URL was verified as HTTP 206 with %PDF- magic before download",
         alternate_official="https://openaccess.thecvf.com/content_CVPR_2020/html/"
                            "Caesar_nuScenes_A_Multimodal_Dataset_for_Autonomous_Driving_"
                            "CVPR_2020_paper.html"),
    dict(paper_id="P0031", short="nuPlan",
         url="https://arxiv.org/pdf/2106.11810",
         source_version="arXiv_v4",
         basis="official arXiv version v4, titled NuPlan: A closed-loop ML-based planning benchmark for autonomous vehicles. The Round-1 source register listed only the project page https://nuplan.org/nuplan, which is not a document; a peer-reviewed nuPlan paper is known to exist but was NOT verified in this batch, so the canonical preprint is used and this remains an open census item",
         alternate_official="https://arxiv.org/abs/2106.11810"),
    dict(paper_id="P0032", short="NAVSIM",
         url="https://arxiv.org/pdf/2406.15349",
         source_version="arXiv_v2",
         basis="official arXiv version v2 (title and version confirmed twice: arXiv export API and the arXiv abs page). The NeurIPS 2024 Datasets and Benchmarks abstract page listed in the Round-1 source register was not fetched for a camera-ready in this batch",
         alternate_official="https://arxiv.org/abs/2406.15349"),
    dict(paper_id="P0033", short="Bench2Drive",
         url="https://arxiv.org/pdf/2406.03877",
         source_version="arXiv_v3",
         basis="official arXiv version v3 (arXiv abs page citation_title matches exactly). A NeurIPS 2024 Datasets and Benchmarks version indexed under DOI 10.52202/079017-0025 was seen in OpenAlex, but no open PDF for it was verified in this batch",
         alternate_official="https://arxiv.org/abs/2406.03877"),
    dict(paper_id="P0034", short="HUGSIM",
         url="https://arxiv.org/pdf/2412.01718",
         source_version="arXiv_v1",
         basis="official arXiv version v1. The IEEE TPAMI version (DOI 10.1109/tpami.2025.3647952, listed in the Round-1 source register and seen in OpenAlex) is not open, so the preprint is canonical",
         alternate_official="https://arxiv.org/abs/2412.01718"),
    # --- Round 2 targeted ingest: H1-H3 historical novelty controls ---
    dict(paper_id="P0018", short="GameFormer",
         url="https://openaccess.thecvf.com/content/ICCV2023/papers/Huang_GameFormer_Game-theoretic_Modeling_and_Learning_of_Transformer-based_Interactive_Prediction_and_ICCV_2023_paper.pdf",
         source_version="ICCV2023_camera_ready",
         basis="venue camera-ready (CVF Open Access); the URL was located by scanning the ICCV2023 Open Access index page, because CVF truncates the title inside its slug and full-title guesses therefore return 404. This supersedes an earlier arXiv download of the same paper (arXiv:2303.05760): venue camera-ready outranks a preprint in the corpus canonical-source priority, and the superseded hash is recorded in ROUND2_TARGETED_INGEST_REPORT.md",
         alternate_official="https://openaccess.thecvf.com/content/ICCV2023/html/Huang_GameFormer_Game-theoretic_Modeling_and_Learning_of_Transformer-based_Interactive_Prediction_and_ICCV_2023_paper.html"),
    dict(paper_id="P0019", short="M2I",
         url="https://openaccess.thecvf.com/content/CVPR2022/papers/Sun_M2I_From_Factored_Marginal_Trajectory_Prediction_to_Interactive_Prediction_CVPR_2022_paper.pdf",
         source_version="CVPR2022_camera_ready",
         basis="venue camera-ready (CVF Open Access); URL verified 2026-09-13 as HTTP 206 + %PDF- before download"),
    dict(paper_id="P0020", short="Bahram2016",
         url=None,
         source_version="none_available",
         basis="no lawful open canonical source: IEEE Transactions on Vehicular Technology 65(6), 3981-3992, DOI 10.1109/TVT.2015.2508009; the DOI resolves to the IEEE Xplore landing page (HTML, not a PDF). Unofficial mirrors are excluded by the ingest prompt."),
    # --- Round 2 targeted ingest (agent/prompts/ROUND2_TARGETED_INGEST.md) ---
    # A1-A5 core P2-R attack set: 2026 arXiv preprints with no verified venue
    # camera-ready, so the official arXiv version is canonical.
    dict(paper_id="P0013", short="BridgeSim",
         url="https://arxiv.org/pdf/2604.10856",
         source_version="arXiv_v1",
         basis="official arXiv version (preprint, no verified venue version)"),
    dict(paper_id="P0014", short="ReactSimBench",
         url="https://arxiv.org/pdf/2606.14058",
         source_version="arXiv_v1",
         basis="official arXiv version (preprint, no verified venue version)"),
    dict(paper_id="P0015", short="CausalDrive",
         url="https://arxiv.org/pdf/2606.15341",
         source_version="arXiv_v1",
         basis="official arXiv version (preprint, no verified venue version)"),
    dict(paper_id="P0016", short="CounterfactualPred",
         url="https://arxiv.org/pdf/2608.11601",
         source_version="arXiv_v1",
         basis="official arXiv version (preprint, no verified venue version)"),
    dict(paper_id="P0017", short="CRAFT",
         url="https://arxiv.org/pdf/2605.04470",
         source_version="arXiv_v1",
         basis="official arXiv version (preprint, no verified venue version)"),
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

    # merge, never drop records: a targeted re-run must not truncate the ledger.
    # The run-local `results` list still drives the summary below.
    try:
        with open(RESULTS, encoding="utf-8") as f:
            merged = {r["paper_id"]: r for r in json.load(f)}
    except (OSError, ValueError):
        merged = {}
    for r in results:
        merged[r["paper_id"]] = r
    ordered = [merged[k] for k in sorted(merged)]

    with open(RESULTS, "w", encoding="utf-8") as f:
        json.dump(ordered, f, indent=2, ensure_ascii=False)

    ok = sum(1 for r in results if r["status"] == "DOWNLOADED")
    blocked = [r["paper_id"] for r in results if r["status"] == "DOWNLOAD_BLOCKED"]
    print(f"\nsummary: downloaded={ok}/{len(results)} blocked={blocked or 'none'}", flush=True)
    print(f"results -> {RESULTS}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
