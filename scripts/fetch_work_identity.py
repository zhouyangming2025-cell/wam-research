"""Record official identity metadata for a batch of candidate works.

Identity -> dedup -> ID allocation is the first pipeline step, and the expected title
used later by front-page verification must come from an official landing page rather
than from memory. This tool fetches each candidate's landing page (arXiv abs page or
venue proceedings page), extracts citation_title / citation_author / citation_date and,
for arXiv, the exact version number, then writes a merge-on-write ledger at
manifests/batch_<batch>_identity.json.

Usage:
    python fetch_work_identity.py            # built-in census candidates
"""
from __future__ import annotations

import html as htmllib
import json
import os
import re
import ssl
import time
import urllib.request

import certifi

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BATCH = os.environ.get("CORPUS_BATCH", "census2")
OUT = os.path.join(BASE, "manifests", f"batch_{BATCH}_identity.json")

# Phase-A Census Round 2 coverage holes. NOTE: candidate arXiv IDs for ViDAR, GenAD,
# nuScenes, nuPlan and Think2Drive are hypotheses to be confirmed by the landing page;
# a mismatch is recorded as such and never silently accepted.
CANDIDATES = [
    # paper_id, short, landing_url, pdf_url
# --- Phase-A Census Round 1 text-layer batch (CORPUS_BATCH=census1) ---
# Works placed by landscape/CENSUS_PHASE_A_ROUND1.md that had no local text layer.
# Landing pages come from manifests/census1_id_allocation.json; titles are read from those
# pages and compared with the census entry, never typed from memory.
    ("P0035", "GAIA1", "https://arxiv.org/abs/2309.17080", "https://arxiv.org/pdf/2309.17080"),
    ("P0036", "DriveDreamer", "https://arxiv.org/abs/2309.09777", "https://arxiv.org/pdf/2309.09777"),
    ("P0037", "DriveWM", "https://openaccess.thecvf.com/content/CVPR2024/html/Wang_Driving_into_the_Future_Multiview_Visual_Forecasting_and_Planning_with_CVPR_2024_paper.html", "https://openaccess.thecvf.com/content/CVPR2024/papers/Wang_Driving_into_the_Future_Multiview_Visual_Forecasting_and_Planning_with_CVPR_2024_paper.pdf"),
    ("P0038", "Vista", "https://arxiv.org/abs/2405.17398", "https://arxiv.org/pdf/2405.17398"),
    ("P0039", "DriveDreamer2", "https://arxiv.org/abs/2403.06845", "https://arxiv.org/pdf/2403.06845"),
    ("P0040", "DrivingGPT", "https://openaccess.thecvf.com/content/ICCV2025/html/Chen_DrivingGPT_Unifying_Driving_World_Modeling_and_Planning_with_Multi-modal_Autoregressive_ICCV_2025_paper.html", "https://openaccess.thecvf.com/content/ICCV2025/papers/Chen_DrivingGPT_Unifying_Driving_World_Modeling_and_Planning_with_Multi-modal_Autoregressive_ICCV_2025_paper.pdf"),
    ("P0041", "PolicyWM", "https://arxiv.org/abs/2510.19654", "https://arxiv.org/pdf/2510.19654"),
    ("P0042", "WorldDrive", "https://arxiv.org/abs/2603.14948", "https://arxiv.org/pdf/2603.14948"),
    ("P0043", "OccWorld", "https://arxiv.org/abs/2311.16038", "https://arxiv.org/pdf/2311.16038"),
    ("P0044", "DriveOccWorld", "https://arxiv.org/abs/2408.14197", "https://arxiv.org/pdf/2408.14197"),
    ("P0045", "WoTE", "https://openaccess.thecvf.com/content/ICCV2025/html/Li_End-to-End_Driving_with_Online_Trajectory_Evaluation_via_BEV_World_Model_ICCV_2025_paper.html", "https://openaccess.thecvf.com/content/ICCV2025/papers/Li_End-to-End_Driving_with_Online_Trajectory_Evaluation_via_BEV_World_Model_ICCV_2025_paper.pdf"),
    ("P0046", "World4Drive", "https://openaccess.thecvf.com/content/ICCV2025/html/Zheng_World4Drive_End-to-End_Autonomous_Driving_via_Intention-aware_Physical_Latent_World_Model_ICCV_2025_paper.html", "https://openaccess.thecvf.com/content/ICCV2025/papers/Zheng_World4Drive_End-to-End_Autonomous_Driving_via_Intention-aware_Physical_Latent_World_Model_ICCV_2025_paper.pdf"),
    ("P0047", "DriveWorld", "https://openaccess.thecvf.com/content/CVPR2024/html/Min_DriveWorld_4D_Pre-trained_Scene_Understanding_via_World_Models_for_Autonomous_CVPR_2024_paper.html", "https://openaccess.thecvf.com/content/CVPR2024/papers/Min_DriveWorld_4D_Pre-trained_Scene_Understanding_via_World_Models_for_Autonomous_CVPR_2024_paper.pdf"),
    ("P0048", "LAW", "https://arxiv.org/abs/2406.08481", "https://arxiv.org/pdf/2406.08481"),
    ("P0049", "DriveJEPA", "https://arxiv.org/abs/2601.22032", "https://arxiv.org/pdf/2601.22032"),
    ("P0050", "WorldRFT", "https://arxiv.org/abs/2512.19133", "https://arxiv.org/pdf/2512.19133"),
    ("P0051", "AutoJEPA", "https://arxiv.org/abs/2607.29031", "https://arxiv.org/pdf/2607.29031"),
    ("P0052", "ReWorld", "https://arxiv.org/abs/2606.27504", "https://arxiv.org/pdf/2606.27504"),
    ("P0053", "WAJEPA", "https://arxiv.org/abs/2608.20974", "https://arxiv.org/pdf/2608.20974"),
    ("P0054", "WhatTrulyMatters", "https://papers.neurips.cc/paper_files/paper/2023/hash/e197fe307eb3467035f892dc100d570a-Abstract-Conference.html", "https://papers.neurips.cc/paper_files/paper/2023/file/e197fe307eb3467035f892dc100d570a-Paper-Conference.pdf"),
    ("P0055", "SLEDGE", "https://arxiv.org/abs/2403.17933", "https://arxiv.org/pdf/2403.17933"),
    ("P0056", "DriveArena", "https://arxiv.org/abs/2408.00415", "https://arxiv.org/pdf/2408.00415"),
    ("P0057", "UniAD", "https://openaccess.thecvf.com/content/CVPR2023/html/Hu_Planning-Oriented_Autonomous_Driving_CVPR_2023_paper.html", "https://openaccess.thecvf.com/content/CVPR2023/papers/Hu_Planning-Oriented_Autonomous_Driving_CVPR_2023_paper.pdf"),
    ("P0058", "VAD", "https://openaccess.thecvf.com/content/ICCV2023/html/Jiang_VAD_Vectorized_Scene_Representation_for_Efficient_Autonomous_Driving_ICCV_2023_paper.html", "https://openaccess.thecvf.com/content/ICCV2023/papers/Jiang_VAD_Vectorized_Scene_Representation_for_Efficient_Autonomous_Driving_ICCV_2023_paper.pdf"),
    ("P0059", "DiffusionDrive", "https://openaccess.thecvf.com/content/CVPR2025/html/Liao_DiffusionDrive_Truncated_Diffusion_Model_for_End-to-End_Autonomous_Driving_CVPR_2025_paper.html", "https://openaccess.thecvf.com/content/CVPR2025/papers/Liao_DiffusionDrive_Truncated_Diffusion_Model_for_End-to-End_Autonomous_Driving_CVPR_2025_paper.pdf"),
    ("P0060", "DrivoR", "https://openaccess.thecvf.com/content/CVPR2026/html/Kirby_Driving_on_Registers_CVPR_2026_paper.html", "https://openaccess.thecvf.com/content/CVPR2026/papers/Kirby_Driving_on_Registers_CVPR_2026_paper.pdf"),
    ("P0021", "HydraMDP", "https://arxiv.org/abs/2406.06978", "https://arxiv.org/pdf/2406.06978"),
    ("P0022", "DriveSuprim", "https://arxiv.org/abs/2506.06659", "https://arxiv.org/pdf/2506.06659"),
    ("P0023", "iPad", "https://arxiv.org/abs/2505.15111", "https://arxiv.org/pdf/2505.15111"),
    ("P0024", "DriveVLM", "https://arxiv.org/abs/2402.12289", "https://arxiv.org/pdf/2402.12289"),
    ("P0025", "OmniDrive", "https://arxiv.org/abs/2405.01533", "https://arxiv.org/pdf/2405.01533"),
    ("P0026", "ORION",
     "https://openaccess.thecvf.com/content/ICCV2025/html/Fu_ORION_A_Holistic_End-to-End_Autonomous_Driving_Framework_by_Vision-Language_Instructed_ICCV_2025_paper.html",
     "https://openaccess.thecvf.com/content/ICCV2025/papers/Fu_ORION_A_Holistic_End-to-End_Autonomous_Driving_Framework_by_Vision-Language_Instructed_ICCV_2025_paper.pdf"),
    ("P0027", "Think2Drive", "https://arxiv.org/abs/2402.16720", "https://arxiv.org/pdf/2402.16720"),
    ("P0028", "ViDAR",
     "https://openaccess.thecvf.com/content/CVPR2024/html/Yang_Visual_Point_Cloud_Forecasting_enables_Scalable_Autonomous_Driving_CVPR_2024_paper.html",
     "https://openaccess.thecvf.com/content/CVPR2024/papers/Yang_Visual_Point_Cloud_Forecasting_enables_Scalable_Autonomous_Driving_CVPR_2024_paper.pdf"),
    ("P0029", "GenAD", "https://arxiv.org/abs/2402.11502", "https://arxiv.org/pdf/2402.11502"),
    ("P0030", "nuScenes",
     "https://openaccess.thecvf.com/content_CVPR_2020/html/Caesar_nuScenes_A_Multimodal_Dataset_for_Autonomous_Driving_CVPR_2020_paper.html",
     "https://openaccess.thecvf.com/content_CVPR_2020/papers/Caesar_nuScenes_A_Multimodal_Dataset_for_Autonomous_Driving_CVPR_2020_paper.pdf"),
    ("P0031", "nuPlan", "https://arxiv.org/abs/2106.11810", "https://arxiv.org/pdf/2106.11810"),
    ("P0032", "NAVSIM", "https://arxiv.org/abs/2406.15349", "https://arxiv.org/pdf/2406.15349"),
    ("P0033", "Bench2Drive", "https://arxiv.org/abs/2406.03877", "https://arxiv.org/pdf/2406.03877"),
    ("P0034", "HUGSIM", "https://arxiv.org/abs/2412.01718", "https://arxiv.org/pdf/2412.01718"),
]

# What each candidate is expected to be, so a wrong DOI/arXiv ID cannot pass silently.
EXPECT_KEY = {
    "P0021": "Hydra-MDP", "P0022": "DriveSuprim", "P0023": "iPad",
    "P0024": "DriveVLM", "P0025": "OmniDrive", "P0026": "ORION",
    "P0027": "Think2Drive", "P0028": "Visual Point Cloud Forecasting",
    "P0029": "GenAD", "P0030": "nuScenes", "P0031": "nuPlan",
    "P0035": "Generative World Model Autonomous",
    "P0036": "Towards Real-world-driven World Models",
    "P0037": "Driving into Future Multiview",
    "P0038": "Generalizable Driving World Model",
    "P0039": "LLM-Enhanced World Models Diverse",
    "P0040": "Unifying Driving World Modeling",
    "P0041": "From Forecasting Planning Collaborative",
    "P0042": "Bridging Scene Generation Planning",
    "P0043": "Learning Occupancy World Model",
    "P0044": "Driving Occupancy World",
    "P0045": "End-to-End Driving with Online",
    "P0046": "End-to-End Autonomous Driving Intention-aware",
    "P0047": "Pre-trained Scene Understanding World",
    "P0048": "Enhancing End-to-End Autonomous Driving",
    "P0049": "Video JEPA Meets Multimodal",
    "P0050": "Latent World Model Planning",
    "P0051": "Latent World Model Continuous",
    "P0052": "Learning Better Representations World",
    "P0053": "Rethinking Video JEPA Paradigm",
    "P0054": "What Truly Matters Trajectory",
    "P0055": "Synthesizing Driving Environments with",
    "P0056": "DriveArena",
    "P0057": "Planning-Oriented Autonomous Driving",
    "P0058": "Vectorized Scene Representation Efficient",
    "P0059": "DiffusionDrive",
    "P0060": "Driving Registers",
    "P0032": "NAVSIM", "P0033": "Bench2Drive", "P0034": "HUGSIM",
}


def meta(html: str, name: str):
    m = re.search(rf'<meta name="{name}" content="([^"]*)"', html)
    return htmllib.unescape(m.group(1)).strip() if m else ""


def fetch(url: str, ctx) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "wam-corpus-ingest/1.0"})
    return urllib.request.urlopen(req, timeout=90, context=ctx).read().decode("utf-8", "replace")


def main() -> int:
    ctx = ssl.create_default_context(cafile=certifi.where())
    ledger = {}
    if os.path.exists(OUT):
        with open(OUT, encoding="utf-8") as fh:
            ledger = json.load(fh)
    for pid, short, landing, pdf in CANDIDATES:
        print(f"--- {pid} {short}", flush=True)
        rec = dict(paper_id=pid, short_name=short, landing_url=landing, pdf_url=pdf)
        try:
            html = fetch(landing, ctx)
            title = meta(html, "citation_title")
            authors = re.findall(r'<meta name="citation_author" content="([^"]*)"', html)
            date = meta(html, "citation_date") or meta(html, "citation_publication_date")
            ver = re.search(r"arXiv:\d{4}\.\d{4,5}v(\d+)", html)
            rec.update(
                official_title=htmllib.unescape(title).replace("\n", " ").strip(),
                official_authors=[htmllib.unescape(a).strip() for a in authors],
                official_date=date,
                arxiv_version=(f"v{ver.group(1)}" if ver else ""),
            )
        except Exception as ex:
            rec.update(error=f"{type(ex).__name__}: {ex}")
        exp = EXPECT_KEY.get(pid, "")
        got = rec.get("official_title", "")
        rec["expected_key"] = exp
        rec["identity_match"] = bool(got) and all(
            w.lower() in got.lower() for w in exp.split() if len(w) > 3
        )
        ledger[pid] = rec
        print(f"      title : {got[:88] or '(none)'}", flush=True)
        print(f"      auth  : {', '.join(rec.get('official_authors', [])[:3]) or '(none)'}", flush=True)
        print(f"      date  : {rec.get('official_date') or '-'}  arxiv={rec.get('arxiv_version') or '-'}"
              f"  match={rec['identity_match']}", flush=True)
        if rec.get("error"):
            print(f"      ERROR : {rec['error']}", flush=True)
        time.sleep(2)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(ledger, fh, indent=2, ensure_ascii=False)
    print(f"\nidentity ledger -> {OUT}  ({len(ledger)} records)", flush=True)
    bad = [k for k, v in ledger.items() if not v.get("identity_match")]
    print("identity mismatches to review:", bad or "none", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
