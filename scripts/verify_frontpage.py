"""Document front-page metadata verification (Batch 0A).

Extracts page-1 text from each canonical PDF and checks it against the manifest
expectation. This is what promotes a row from INDEX_BACKED to DOCUMENT_VERIFIED.

Read-only: nothing is written except the JSON result file.
"""
from __future__ import annotations

import json
import os
import re
import sys
import unicodedata

BASE = r"D:\zym_information\ZYM\wam\research_assets"
PDF_DIR = os.path.join(BASE, "papers", "pdf")
# Batch label selects the ledger; the default reproduces the Batch 0A file exactly
# and CORPUS_BATCH=round2 writes the Round 2 ledger (see scripts/build_raw_md.py).
BATCH = os.environ.get("CORPUS_BATCH", "0a")
OUT = os.path.join(BASE, "manifests", f"batch_{BATCH}_frontpage_verification.json")

try:  # console below is GBK; paper front pages contain symbols like U+2020
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# paper_id -> (short_name, expected_title, expected_first_author_surname, extra_author_surnames)
EXPECT = {
    "P0001": ("Epona", "Epona: Autoregressive Diffusion World Model for Autonomous Driving",
              "Zhang", ["Tang", "Hu", "Pan", "Guo", "Liu", "Huang", "Yuan", "Zhang", "Long", "Cao", "Yin"]),
    "P0002": ("SafeDrive", "SafeDrive: Fine-Grained Safety Reasoning for End-to-End Driving in a Sparse World",
              "Kim", ["Oh", "Yu", "Shin", "Kwak", "Choi"]),
    "P0003": ("GraphAD", "GraphAD: Interaction Scene Graph for End-to-end Autonomous Driving",
              "Zhang", []),
    "P0004": ("BeTop", "Reasoning Multi-Agent Behavioral Topology for Interactive Autonomous Driving",
              "Liu", []),
    "P0005": ("RiskWorld", "RiskWorld: Object-Centric Latent World Modeling for Autonomous Driving Risk Identification",
              "Li", []),
    "P0006": ("GenDrive", "Gen-Drive: Enhancing Diffusion Generative Driving Policies with Reward Modeling and Reinforcement Learning Fine-Tuning",
              "Huang", []),
    "P0007": ("DriveReward", "DriveReward: A Comprehensive Dataset and Generative Vision-Language Reward Model for Autonomous Driving",
              "Chen", []),
    "P0009": ("DriveLaW", "DriveLaW: Unifying Planning and Video Generation in a Latent Driving World",
              "Xia", []),
    "P0010": ("TOAD", "Test-Time Trajectory Optimization for Autonomous Driving",
              "Xu", ["Zablocki", "Yin", "Ramzi", "Kirby", "Boulch", "Cord"]),
    "P0011": ("SensitivityShaping", "Sensitivity Shaping for Latent Modeling",
              "Yu", []),
    "P0012": ("DAWAM", "DA-WAM: Decision-Aligned Future Latents for Driving World Models",
              "Zhong", []),
    # Round 2 targeted ingest. These expectations are the DECLARED discovery
    # metadata from state/TARGETED_READING_QUEUE.md (WEB-VERIFIED DISCOVERY). The
    # check promotes a record to DOCUMENT_VERIFIED only if the PDF's own front page
    # confirms title and first author; anything else is recorded as CONFLICT with
    # the page-1 head kept for adjudication.
    # --- Phase-A Census Round 2 support batch (titles copied from the official landing
    # pages recorded in manifests/batch_census2_identity.json) ---
    "P0021": ("HydraMDP", "Hydra-MDP: End-to-end Multimodal Planning with Multi-target Hydra-Distillation", "Li", []),
    "P0022": ("DriveSuprim", "DriveSuprim: Towards Precise Trajectory Selection for End-to-End Planning", "Yao", []),
    "P0023": ("iPad", "iPad: Iterative Proposal-centric End-to-End Autonomous Driving", "Guo", []),
    "P0024": ("DriveVLM", "DriveVLM: The Convergence of Autonomous Driving and Large Vision-Language Models", "Tian", []),
    "P0025": ("OmniDrive", "OmniDrive: A Holistic Vision-Language Dataset for Autonomous Driving with Counterfactual Reasoning", "Wang", []),
    "P0026": ("ORION", "ORION: A Holistic End-to-End Autonomous Driving Framework by Vision-Language Instructed Action Generation", "Fu", []),
    "P0027": ("Think2Drive", "Think2Drive: Efficient Reinforcement Learning by Thinking in Latent World Model for Quasi-Realistic Autonomous Driving", "Li", []),
    "P0028": ("ViDAR", "Visual Point Cloud Forecasting enables Scalable Autonomous Driving", "Yang", []),
    "P0029": ("GenAD", "GenAD: Generative End-to-End Autonomous Driving", "Zheng", []),
    "P0030": ("nuScenes", "nuScenes: A Multimodal Dataset for Autonomous Driving", "Caesar", []),
    "P0031": ("nuPlan", "nuPlan: A closed-loop ML-based planning benchmark for autonomous vehicles", "Caesar", []),
    "P0032": ("NAVSIM", "NAVSIM: Data-Driven Non-Reactive Autonomous Vehicle Simulation and Benchmarking", "Dauner", []),
    "P0033": ("Bench2Drive", "Bench2Drive: Towards Multi-Ability Benchmarking of Closed-Loop End-To-End Autonomous Driving", "Jia", []),
    "P0034": ("HUGSIM", "HUGSIM: A Real-Time, Photo-Realistic and Closed-Loop Simulator for Autonomous Driving", "Zhou", []),
    "P0013": ("BridgeSim", "BridgeSim: Unveiling the OL-CL Gap in End-to-End Autonomous Driving",
              "Zhao", []),
    "P0014": ("ReactSimBench", "ReactSim-Bench: Benchmarking Reactive Behavior World Model Simulation in Autonomous Driving",
              "Zhang", []),
    "P0015": ("CausalDrive", "CausalDrive: Real-time Causal World Models for Autonomous Driving",
              "Yan", []),
    "P0016": ("CounterfactualPred", "How Can Driving World Models Do Counterfactual Prediction?",
              "Zhang", []),
    "P0017": ("CRAFT", "CRAFT: Counterfactual-to-Interactive Reinforcement Fine-Tuning for Driving Policies",
              "Chen", []),
    "P0018": ("GameFormer", "GameFormer: Game-theoretic Modeling and Learning of Transformer-based Interactive Prediction and Planning for Autonomous Driving",
              "Huang", ["Liu", "Lv"]),
    "P0019": ("M2I", "M2I: From Factored Marginal Trajectory Prediction to Interactive Prediction",
              "Sun", []),
    "P0020": ("Bahram2016", "A Game-Theoretic Approach to Replanning-Aware Interactive Scene Prediction and Planning",
              "Bahram", []),
}


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    s = s.replace("\u2010", "-").replace("\u2011", "-").replace("\u2013", "-").replace("\u2014", "-")
    return re.sub(r"[^a-z0-9]+", "", s.lower())


def page_text(pdf, idx: int) -> str:
    try:
        return pdf[idx].get_textpage().get_text_range()
    except Exception as e:
        return f"<text extraction failed: {type(e).__name__}: {e}>"


def main() -> int:
    # optional CLI filter: verify only these paper ids (comma-separated), so a
    # targeted batch never mixes other batches into its own ledger.
    only = None
    if len(sys.argv) > 1 and not sys.argv[1].startswith("-"):
        only = {s.strip() for s in sys.argv[1].split(",")}
    try:
        import pypdfium2 as pdfium
    except ImportError:
        print("pypdfium2 not available in this interpreter", file=sys.stderr)
        return 2
    try:
        ver = getattr(pdfium, "V_PYPDFIUM2", None) or getattr(
            __import__("pypdfium2.version", fromlist=["x"]), "V_PYPDFIUM2", "unknown")
    except Exception:
        ver = "unknown"
    print(f"pypdfium2={ver}")
    results = []
    for pid, (short, exp_title, exp_sur, extra) in EXPECT.items():
        if only and pid not in only:
            continue
        path = os.path.join(PDF_DIR, f"{pid}_{short}.pdf")
        rec = dict(paper_id=pid, short_name=short, path=path, exists=os.path.exists(path),
                   expected_title=exp_title, expected_first_author_surname=exp_sur,
                   title_match=None, first_author_found=None, extra_authors_found=[],
                   pdf_meta_title=None, page1_head=[], verdict=None)
        if not rec["exists"]:
            rec["verdict"] = "PDF_MISSING"
            results.append(rec)
            print(f"\n=== {pid} {short}: PDF MISSING")
            continue
        pdf = pdfium.PdfDocument(path)
        rec["pages"] = len(pdf)
        try:
            md = pdf.get_metadata_dict() or {}
            rec["pdf_meta_title"] = (md.get("Title") or "").strip() or None
        except Exception:
            pass
        head = page_text(pdf, 0)[:4000]
        lines = [l.strip() for l in head.splitlines() if l.strip()]
        rec["page1_head"] = lines[:22]
        n_head = norm(head)
        rec["title_match"] = "EXACT" if norm(exp_title) in n_head else None
        if rec["title_match"] is None:
            # tolerate a dropped subtitle after ':'
            stem = norm(exp_title.split(":")[0])
            rec["title_match"] = "PARTIAL" if stem and stem in n_head else "NONE"
        rec["first_author_found"] = norm(exp_sur) in n_head
        rec["extra_authors_found"] = [a for a in extra if norm(a) in n_head]
        rec["verdict"] = ("DOCUMENT_VERIFIED"
                          if rec["title_match"] in ("EXACT", "PARTIAL") and rec["first_author_found"]
                          else "CONFLICT")
        results.append(rec)
        print(f"\n=== {pid} {short}  pages={rec['pages']}  title_match={rec['title_match']}  "
              f"first_author({exp_sur})_found={rec['first_author_found']}  -> {rec['verdict']}")
        print(f"    pdf_meta_title: {rec['pdf_meta_title']!r}")
        for l in rec["page1_head"][:14]:
            print(f"    | {l[:150]}")
    # merge, never drop records: a targeted --only re-run must not truncate the
    # batch's front-page verification ledger.
    try:
        with open(OUT, encoding="utf-8") as f:
            merged = {r["paper_id"]: r for r in json.load(f)}
    except (OSError, ValueError):
        merged = {}
    for r in results:
        merged[r["paper_id"]] = r
    ordered = [merged[k] for k in sorted(merged)]

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(ordered, f, indent=2, ensure_ascii=False)
    print(f"\nrecords in ledger: {len(ordered)} (this run: {len(results)})")
    print(f"results -> {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
