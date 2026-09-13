"""Generate CORPUS_MANIFEST.csv for Batch 0A from the acquisition artifacts.

Single source of truth: the download results JSON (canonical URL, source_version,
byte size, SHA256) + the front-page verification JSON (DOCUMENT_VERIFIED verdict).
Hashes are never retyped by hand.

Optional: if manifests/batch_0a_rawmd_results.json exists it is merged in
(raw_md_local_path, raw_md_sha256, library_status, reading_status).

Idempotent: safe to re-run.
"""
from __future__ import annotations

import csv
import json
import os

BASE = r"D:\zym_information\ZYM\wam\research_assets"
MAN = os.path.join(BASE, "manifests")
PDF_DIR = os.path.join(BASE, "papers", "pdf")
RAW_DIR = os.path.join(BASE, "papers", "raw_md")
OUT_CSV = os.path.join(MAN, "CORPUS_MANIFEST.csv")

HEADER = [
    "paper_id", "title", "year", "first_author", "venue", "arxiv_id", "doi",
    "official_url", "official_pdf_url", "source_version", "pdf_sha256",
    "raw_md_sha256", "pdf_local_path", "raw_md_local_path", "library_status",
    "github_card_path", "code_available", "official_code_url", "code_repo_id",
    "reading_status", "primary_tags", "hypothesis_tags", "decision_relevance",
    "last_reviewed", "notes",
]

DATE = "2026-09-13"

# paper_id -> bibliographic + policy fields. Titles follow the paper's own front
# page where it differs from the index (evidence hierarchy: paper > index).
META = {
    "P0001": dict(short="Epona", title="Epona: Autoregressive Diffusion World Model for Autonomous Driving",
                  year="2025", first_author="Kaiwen Zhang", venue="ICCV 2025",
                  arxiv_id="2506.24113", doi="10.1109/ICCV.2025.02527",
                  official_url="https://arxiv.org/abs/2506.24113",
                  code_available="YES", official_code_url="https://github.com/Kevin-thu/Epona",
                  tags="world-model;planning;diffusion;autoregressive",
                  hyp="GENERAL;P3_HOLD", rel="MEDIUM",
                  note="Camera-ready front page confirms author 8 = Li Yuan, overruling the 'Yuan Li' spelling in arXiv/OpenAlex and the GitHub README. Canonical PDF differs from BOTH pre-existing local copies (Epona.pdf 5AD06198..., Epona_origin.pdf 731D0633...), so per ruling neither may serve as canonical. EVIDENCE_LEVEL=DOCUMENT_VERIFIED"),
    "P0002": dict(short="SafeDrive", title="SafeDrive: Fine-Grained Safety Reasoning for End-to-End Driving in a Sparse World",
                  year="2026", first_author="Jungho Kim", venue="CVPR 2026",
                  arxiv_id="2602.18887", doi="NONE",
                  official_url="https://openaccess.thecvf.com/content/CVPR2026/html/Kim_SafeDrive_Fine-Grained_Safety_Reasoning_for_End-to-End_Driving_in_a_Sparse_CVPR_2026_paper.html",
                  code_available="UNKNOWN", official_code_url="",
                  tags="planning;safety;trajectory-scorer", hyp="P1_RETIRED;P2R_PRIMARY", rel="MEDIUM",
                  note="RESOLVED per user adjudication (mechanism anchors: trajectory-conditioned Sparse World, SWNet, FRNet, PwNC, TwDAC). Front page confirms all six authors Jungho Kim, Jiyong Oh, Seunghoon Yu, Hongjae Shin, Donghyuk Kwak, Jun Won Choi (Seoul National University). Project page found on the paper itself: https://spa-junghokim.github.io/SafeDrive-Page/ (repo existence NOT verified). SafeDrive Dreamer and other same-name works do NOT occupy P0002. EVIDENCE_LEVEL=DOCUMENT_VERIFIED"),
    "P0003": dict(short="GraphAD", title="GraphAD: Interaction Scene Graph for End-to-end Autonomous Driving",
                  year="2024", first_author="Yunpeng Zhang", venue="IJCAI 2024",
                  arxiv_id="2403.19098", doi="10.24963/ijcai.2024/270",
                  official_url="https://arxiv.org/abs/2403.19098",
                  code_available="UNKNOWN", official_code_url="",
                  tags="planning;interactive;trajectory-prediction", hyp="P2R_PRIMARY", rel="MEDIUM",
                  note="Front page author list begins Yunpeng Zhang, Deheng Qian, Ding Li, Yifeng Pan, Yong Chen, Zhenbao Liang. Canonical source is arXiv because a verified IJCAI camera-ready URL was not located; IJCAI pattern URL remains unverified. OpenAlex holds two IJCAI records (2024/2025, same pages 2422-2430). EVIDENCE_LEVEL=DOCUMENT_VERIFIED (title/authors) / venue INDEX_BACKED"),
    "P0004": dict(short="BeTop", title="Reasoning Multi-Agent Behavioral Topology for Interactive Autonomous Driving",
                  year="2024", first_author="Haochen Liu", venue="NeurIPS 2024",
                  arxiv_id="2409.18031", doi="NONE",
                  official_url="https://arxiv.org/abs/2409.18031",
                  code_available="YES", official_code_url="https://github.com/OpenDriveLab/BeTop",
                  tags="planning;interactive;trajectory-prediction;closed-loop",
                  hyp="P2R_PRIMARY", rel="HIGH",
                  note="Front page confirms Haochen Liu, Li Chen, Yu Qiao, Chen Lv, Hongyang Li and that BeTop/BeTopNet are this paper's own terms. Downloaded NeurIPS 2024 camera-ready. Code URL evidence = search-result listing only; repo not verified. EVIDENCE_LEVEL=DOCUMENT_VERIFIED"),
    "P0005": dict(short="RiskWorld", title="RiskWorld: Object-Centric Latent World Modeling for Autonomous Driving Risk Identification",
                  year="2026", first_author="Jingzheng Li", venue="arXiv preprint",
                  arxiv_id="2608.21414", doi="NONE",
                  official_url="https://arxiv.org/abs/2608.21414",
                  code_available="UNKNOWN", official_code_url="",
                  tags="world-model;risk;planning", hyp="P2R_PRIMARY;P3_HOLD", rel="MEDIUM",
                  note="Front page confirms Jingzheng Li, Yufei Ge, Qianren Mao, Zhijun Chen, Bing Li, Xingyu Peng, Baochang Zhang, Xianglong Liu. No competing driving RiskWorld exists. EVIDENCE_LEVEL=DOCUMENT_VERIFIED"),
    "P0006": dict(short="GenDrive", title="Gen-Drive: Enhancing Diffusion Generative Driving Policies with Reward Modeling and Reinforcement Learning Fine-tuning",
                  year="2025", first_author="Zhiyu Huang", venue="ICRA 2025",
                  arxiv_id="2410.05582", doi="10.1109/ICRA55743.2025.11127286",
                  official_url="https://arxiv.org/abs/2410.05582",
                  code_available="UNKNOWN", official_code_url="",
                  tags="planning;reward-model;diffusion", hyp="P1_RETIRED", rel="HIGH",
                  note="TITLE CONFLICT RESOLVED: paper front page reads 'Fine-tuning', OpenAlex read 'Fine-Tuning'; paper wins. Front page confirms Zhiyu Huang, Xinshuo Weng, Maximilian Igl, Yuxiao Chen, Yulong Cao, Boris Ivanovic, Marco Pavone, Chen Lv. ICRA camera-ready is IEEE-paywalled -> arXiv used. HIGH per upstream context (learned-reward RL improve-then-degrade). EVIDENCE_LEVEL=DOCUMENT_VERIFIED"),
    "P0007": dict(short="DriveReward", title="DriveReward: A Comprehensive Dataset and Generative Vision-Language Reward Model for Autonomous Driving",
                  year="2026", first_author="Qimao Chen", venue="arXiv preprint",
                  arxiv_id="2606.08525", doi="NONE",
                  official_url="https://arxiv.org/abs/2606.08525",
                  code_available="UNKNOWN", official_code_url="",
                  tags="reward-model;trajectory-scorer;planning", hyp="P1_RETIRED", rel="MEDIUM",
                  note="Front page confirms Qimao Chen, Fang Li, Yuechen Luo, Zehan Zhang, Haiyang Sun, ... No official dataset page located (unresolved, not 'no'). EVIDENCE_LEVEL=DOCUMENT_VERIFIED"),
    "P0008": dict(short="NPPC", title="NPPC: Neural Parametric Planning Cost for End-to-End Autonomous Driving",
                  year="2026", first_author="Abi Rahman Syamil", venue="IEEE RA-L 2026",
                  arxiv_id="NONE", doi="10.1109/LRA.2026.3663819",
                  official_url="https://doi.org/10.1109/LRA.2026.3663819",
                  code_available="UNKNOWN", official_code_url="",
                  tags="planning;trajectory-scorer;end-to-end", hyp="P1_RETIRED", rel="HIGH",
                  note="DOWNLOAD_BLOCKED: PAYWALLED_NO_OPEN_SOURCE (IEEE Xplore doc 11393633, DOI 10.1109/LRA.2026.3663819). No arXiv version exists. PDF NOT acquired, so metadata stays INDEX_BACKED - no front-page verification possible. HIGH per upstream context (key counterexample: no cost hacking). Disambiguate by DOI, never by the acronym (NPPC also denotes the natriuretic peptide gene). EVIDENCE_LEVEL=INDEX_BACKED"),
    "P0009": dict(short="DriveLaW", title="DriveLaW: Unifying Planning and Video Generation in a Latent Driving World",
                  year="2026", first_author="Tianze Xia", venue="CVPR 2026",
                  arxiv_id="2512.23421", doi="NONE",
                  official_url="https://openaccess.thecvf.com/content/CVPR2026/html/Xia_DriveLaW_Unifying_Planning_and_Video_Generation_in_a_Latent_Driving_CVPR_2026_paper.html",
                  code_available="YES", official_code_url="https://github.com/xiaomi-research/drivelaw",
                  tags="world-model;planning;end-to-end;representation", hyp="P3_HOLD", rel="HIGH",
                  note="Front page confirms Tianze Xia, Yongkang Li, Lijun Zhou, Jingfeng Yao, ... (Huazhong UST / Xiaomi EV). ID conflict recorded earlier: naming-standard example P0002_DriveLaW corrected to PXXXX_DriveLaW; DriveLaW stays P0009. Code URL evidence = search-result listing only. EVIDENCE_LEVEL=DOCUMENT_VERIFIED"),
    "P0010": dict(short="TOAD", title="Test-Time Trajectory Optimization for Autonomous Driving",
                  year="2026", first_author="Yihong Xu", venue="arXiv preprint",
                  arxiv_id="2606.07170", doi="NONE",
                  official_url="https://arxiv.org/abs/2606.07170",
                  code_available="YES", official_code_url="https://github.com/valeoai/TOAD",
                  tags="planning;trajectory-scorer", hyp="P1_RETIRED", rel="HIGH",
                  note="PROVENANCE CONFLICT RECORDED: official repo README advertises 94.9 PDMS on NAVSIM-v1, while the paper abstract states 94.7 PDMS. Author order confirmed by both the repo citation block and the front page (Yihong Xu first). Existing EXTERNAL clone: 论文调研/repos/toad @ cfa88e008080d0799b2859b5935c257048ec0adf, Apache-2.0. EVIDENCE_LEVEL=DOCUMENT_VERIFIED"),
    "P0011": dict(short="SensitivityShaping", title="Sensitivity Shaping for Latent Modeling",
                  year="2026", first_author="Hongzhan Yu", venue="arXiv preprint",
                  arxiv_id="2606.14585", doi="NONE",
                  official_url="https://arxiv.org/abs/2606.14585",
                  code_available="UNKNOWN", official_code_url="",
                  tags="latent-world-model;OOD;planning", hyp="P1_RETIRED;P3_HOLD", rel="HIGH",
                  note="VENUE UNRESOLVED (CoRL 2026 not confirmed). Front page confirms Hongzhan Yu, Chenghao Li, Ruipeng Zhang, Henrik Christensen, Sicun Gao (UC San Diego). HIGH per upstream context (policy-induced OOD detection failure mechanism). EVIDENCE_LEVEL=DOCUMENT_VERIFIED"),
    "P0012": dict(short="DAWAM", title="DA-WAM: Decision-Aligned Future Latents for Driving World Models",
                  year="2026", first_author="Ruiguo Zhong", venue="arXiv preprint",
                  arxiv_id="2608.19085", doi="NONE",
                  official_url="https://arxiv.org/abs/2608.19085",
                  code_available="UNKNOWN", official_code_url="",
                  tags="world-model;planning;action-conditioned", hyp="P1_RETIRED;P2R_PRIMARY", rel="HIGH",
                  note="Front page confirms Ruiguo Zhong, Benshan Ma, Xiaolong Chen, Lang Zhang, Mingyue Feng, Yaonong Wang, Pei Liu, Jun Ma (HKUST-GZ / Leapmotor). Acronym checked and NOT ambiguous. EVIDENCE_LEVEL=DOCUMENT_VERIFIED"),
}

ORDER = [f"P{i:04d}" for i in range(1, 13)]


def load(name):
    p = os.path.join(MAN, name)
    if not os.path.exists(p):
        return None
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def main():
    dl = {r["paper_id"]: r for r in load("batch_0a_download_results.json") or []}
    fp = {r["paper_id"]: r for r in load("batch_0a_frontpage_verification.json") or []}
    raw = {r["paper_id"]: r for r in load("batch_0a_rawmd_results.json") or []}

    rows = []
    for pid in ORDER:
        m = META[pid]
        short = m["short"]
        d = dl.get(pid, {})
        f = fp.get(pid, {})
        r = raw.get(pid, {})

        downloaded = d.get("status") == "DOWNLOADED"
        raw_ok = r.get("qc") == "RAW_MD_READY"

        pdf_rel = os.path.join(BASE, "papers", "pdf", f"{pid}_{short}.pdf") if downloaded else ""
        raw_rel = r.get("raw_md_local_path", "") if raw_ok else ""

        if raw_ok:
            lib, reading = "PDF+MD", "RAW_MD_READY"
        elif downloaded:
            lib, reading = "PDF", "DOWNLOADED"
        else:
            lib, reading = "NONE", "DISCOVERED"

        notes = m["note"]
        if d.get("status") == "DOWNLOAD_BLOCKED":
            notes = f"DOWNLOAD_BLOCKED: {d.get('error')}. " + notes
        if f and f.get("verdict") and f["verdict"] != "DOCUMENT_VERIFIED" and downloaded:
            notes += f" FRONTPAGE_VERDICT={f['verdict']}."
        if r.get("qc") == "RAW_MD_QC_FAIL":
            notes += f" RAW_MD_QC_FAIL: {r.get('qc_detail')}."

        rows.append([
            pid, m["title"], m["year"], m["first_author"], m["venue"],
            m["arxiv_id"], m["doi"], m["official_url"],
            d.get("canonical_url") or "", d.get("source_version", "UNKNOWN"),
            d.get("sha256") if downloaded else "",
            (r.get("raw_md_sha256") if raw_ok else "UNKNOWN"),
            pdf_rel, raw_rel, lib,
            f"papers/cards/{pid}_{short}.md",
            m["code_available"], m["official_code_url"], "",
            reading, m["tags"], m["hyp"], m["rel"], DATE, notes,
        ])

    os.makedirs(MAN, exist_ok=True)
    with open(OUT_CSV, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, quoting=csv.QUOTE_MINIMAL)
        w.writerow(HEADER)
        w.writerows(rows)

    print(f"wrote {OUT_CSV}")
    print(f"rows={len(rows)} columns={len(HEADER)}")
    got = sum(1 for x in rows if x[10])
    print(f"pdf_sha256 filled={got}  raw_md filled={sum(1 for x in rows if x[12])}")
    print(f"library_status: " + ", ".join(f"{a}={b}" for a, b in
          {s: sum(1 for x in rows if x[14] == s) for s in {x[14] for x in rows}}.items()))


if __name__ == "__main__":
    main()
