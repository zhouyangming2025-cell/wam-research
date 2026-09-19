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
                  code_repo_id="R0009",
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
    # --- Round 2 targeted ingest (agent/prompts/ROUND2_TARGETED_INGEST.md) ---
    # decision_relevance stays MEDIUM for every Round 2 record: the schema reserves
    # HIGH for adjudicated evidence (kills/weakens a hypothesis, a direct observed
    # failure, novelty occupation, a key counterexample, or a changed research
    # decision), and none of these has been deep-read yet. hypothesis_tags record
    # the batch's owner-declared purpose, not an adjudication.
    # Official-code rule: YES only when the paper itself prints a repository URL;
    # a printed project page is recorded in notes and left UNKNOWN.
    "P0013": dict(short="BridgeSim", title="BridgeSim: Unveiling the OL-CL Gap in End-to-End Autonomous Driving",
                  year="2026", first_author="Seth Z. Zhao", venue="arXiv preprint",
                  arxiv_id="2604.10856", doi="NONE",
                  official_url="https://arxiv.org/abs/2604.10856",
                  code_available="UNKNOWN", official_code_url="",
                  tags="open-loop;closed-loop;end-to-end;evaluation", hyp="P2R_PRIMARY", rel="MEDIUM",
                  note="Round 2 A1, core P2-R attack set. Front page confirms title and first author Seth Z. Zhao (26 pages). The paper prints a PROJECT PAGE, https://vail-ucla.github.io/BridgeSim/ (p.1), not a repository URL, so code_available stays UNKNOWN pending verification. EVIDENCE_LEVEL=DOCUMENT_VERIFIED"),
    "P0014": dict(short="ReactSimBench", title="ReactSim-Bench: Benchmarking Reactive Behavior World Model Simulation in Autonomous Driving",
                  year="2026", first_author="Zhiyuan Zhang", venue="arXiv preprint",
                  arxiv_id="2606.14058", doi="NONE",
                  official_url="https://arxiv.org/abs/2606.14058",
                  code_available="YES", official_code_url="https://github.com/Thinklab-SJTU/ReactSim-Bench",
                  tags="benchmark;reactive;world-model;evaluation", hyp="P2R_PRIMARY", rel="MEDIUM",
                  note="Round 2 A2, core P2-R attack set. Front page confirms title and first author Zhiyuan Zhang (19 pages) and prints the repository URL https://github.com/Thinklab-SJTU/ReactSim-Bench on page 1, which is paper-source support for code_available=YES (repo reachability NOT independently verified). EVIDENCE_LEVEL=DOCUMENT_VERIFIED"),
    "P0015": dict(short="CausalDrive", title="CausalDrive: Real-time Causal World Models for Autonomous Driving",
                  year="2026", first_author="Tianyi Yan", venue="arXiv preprint",
                  arxiv_id="2606.15341", doi="NONE",
                  official_url="https://arxiv.org/abs/2606.15341",
                  code_available="UNKNOWN", official_code_url="",
                  tags="world-model;reactive;counterfactual;planning", hyp="P2R_PRIMARY", rel="MEDIUM",
                  note="Round 2 A3, core P2-R attack set. Front page confirms title and first author Tianyi Yan (18 pages). No repository or project URL appears anywhere in the extracted PDF text, so code_available stays UNKNOWN: absence of a printed URL is not evidence that no code exists. EVIDENCE_LEVEL=DOCUMENT_VERIFIED"),
    "P0016": dict(short="CounterfactualPred", title="How Can Driving World Models Do Counterfactual Prediction?",
                  year="2026", first_author="Jiaru Zhang", venue="arXiv preprint",
                  arxiv_id="2608.11601", doi="NONE",
                  official_url="https://arxiv.org/abs/2608.11601",
                  code_available="UNKNOWN", official_code_url="",
                  tags="world-model;counterfactual;action-conditioned;evaluation", hyp="P2R_PRIMARY", rel="MEDIUM",
                  note="Round 2 A4, core P2-R attack set. Front page confirms title and first author Jiaru Zhang (Purdue University / Bosch Center for Artificial Intelligence), 18 pages. No repository or project URL found in the extracted text. EVIDENCE_LEVEL=DOCUMENT_VERIFIED"),
    "P0017": dict(short="CRAFT", title="CRAFT: Counterfactual-to-Interactive Reinforcement Fine-Tuning for Driving Policies",
                  year="2026", first_author="Keyu Chen", venue="arXiv preprint",
                  arxiv_id="2605.04470", doi="NONE",
                  official_url="https://arxiv.org/abs/2605.04470",
                  code_available="UNKNOWN", official_code_url="",
                  tags="counterfactual;closed-loop;planning;interactive", hyp="P2R_PRIMARY", rel="MEDIUM",
                  note="Round 2 A5, core P2-R attack set. Front page confirms title and first author Keyu Chen (Tsinghua University / Li Auto), 22 pages. The paper prints a PROJECT PAGE, https://currychen77.github.io/CRAFT (p.1), not a repository URL, so code_available stays UNKNOWN pending verification. EVIDENCE_LEVEL=DOCUMENT_VERIFIED"),
    "P0018": dict(short="GameFormer", title="GameFormer: Game-theoretic Modeling and Learning of Transformer-based Interactive Prediction and Planning for Autonomous Driving",
                  year="2023", first_author="Zhiyu Huang", venue="ICCV 2023",
                  arxiv_id="2303.05760", doi="NONE",
                  official_url="https://openaccess.thecvf.com/content/ICCV2023/html/Huang_GameFormer_Game-theoretic_Modeling_and_Learning_of_Transformer-based_Interactive_Prediction_and_ICCV_2023_paper.html",
                  code_available="UNKNOWN", official_code_url="",
                  tags="trajectory-prediction;interactive;reactive;planning", hyp="P2R_PRIMARY", rel="MEDIUM",
                  note="Round 2 H1, historical novelty control for the P2-R occupancy question. Canonical source is the ICCV 2023 camera-ready (CVF Open Access), which SUPERSEDED an earlier arXiv download of the same paper (arXiv:2303.05760, 2348946 bytes, sha256 e7f71bda870dcf1e58ba5ffcecb013b01dcd2c6bc4cdaf726ce97ba9141a8db6) because venue camera-ready outranks a preprint. The CVF URL was located by scanning the ICCV2023 Open Access index: CVF truncates the title inside its slug, so three full-title guesses had returned HTTP 404. Front page confirms title and first author Zhiyu Huang (11 pages). The paper prints a PROJECT PAGE, https://mczhi.github.io/GameFormer/ (p.1), not a repository URL, so code_available stays UNKNOWN. EVIDENCE_LEVEL=DOCUMENT_VERIFIED"),
    "P0019": dict(short="M2I", title="M2I: From Factored Marginal Trajectory Prediction to Interactive Prediction",
                  year="2022", first_author="Qiao Sun", venue="CVPR 2022",
                  arxiv_id="2202.11884", doi="NONE",
                  official_url="https://openaccess.thecvf.com/content/CVPR2022/html/Sun_M2I_From_Factored_Marginal_Trajectory_Prediction_to_Interactive_Prediction_CVPR_2022_paper.html",
                  code_available="UNKNOWN", official_code_url="",
                  tags="trajectory-prediction;interactive;reactive", hyp="P2R_PRIMARY", rel="MEDIUM",
                  note="Round 2 H2, historical novelty control for the P2-R occupancy question. Canonical source is the CVPR 2022 camera-ready (CVF Open Access), verified as HTTP 206 + %PDF- before download, which outranks the arXiv preprint. Front page confirms the title and first author Qiao Sun (10 pages). No repository or project URL appears anywhere in the extracted PDF text, so code_available stays UNKNOWN: absence of a printed URL is not evidence that no code exists. EVIDENCE_LEVEL=DOCUMENT_VERIFIED"),
    "P0020": dict(short="Bahram2016", title="A Game-Theoretic Approach to Replanning-Aware Interactive Scene Prediction and Planning",
                  year="2016", first_author="Mohammad Bahram", venue="IEEE Transactions on Vehicular Technology 65(6), 3981-3992",
                  arxiv_id="NONE", doi="10.1109/TVT.2015.2508009",
                  official_url="https://doi.org/10.1109/TVT.2015.2508009",
                  code_available="UNKNOWN", official_code_url="",
                  tags="trajectory-prediction;interactive;reactive;planning", hyp="P2R_PRIMARY", rel="MEDIUM",
                  note="Round 2 H3, historical novelty control for the P2-R occupancy question. BLOCKED: no lawful open canonical source. The DOI resolves to the IEEE Xplore landing page (HTTP 202, HTML, not a PDF); unofficial mirrors are excluded by the ingest prompt, so no PDF is stored and the record carries DOWNLOAD_BLOCKED: PAYWALLED_NO_OPEN_SOURCE. Title, year, venue and author are index-level discovery metadata and NOT document-verified. EVIDENCE_LEVEL=INDEX_BACKED"),
    # --- Phase-A Census Round 2 support batch (CORPUS_BATCH=census2) ---
    # Coverage holes named in landscape/FIELD_ATLAS.md (F10), landscape/CENSUS_PHASE_A_ROUND1.md
    # and state/NEXT_TASK.md. Titles, years, first authors and arXiv versions are copied from
    # manifests/batch_census2_identity.json (official landing pages); tags come from the corpus
    # vocabulary and every assignment is backed by the paper's own text; code_available is YES
    # only where the paper itself prints a repository URL. These are census-depth records: no
    # deep read, no field placement, no novelty or gap verdict.
    "P0021": dict(short="HydraMDP", title="Hydra-MDP: End-to-end Multimodal Planning with Multi-target Hydra-Distillation",
                  year="2024", first_author="Zhenxin Li", venue="arXiv preprint",
                  arxiv_id="2406.06978", doi="NONE",
                  official_url="https://arxiv.org/abs/2406.06978",
                  code_available="YES", official_code_url="https://github.com/NVlabs/Hydra-MDP",
                  tags="planning;end-to-end", hyp="GENERAL", rel="LOW", reviewed="2026-09-14",
                  note="Phase-A Census Round 2 support batch (CORPUS_BATCH=census2), coverage hole: F10 strong non-WM end-to-end control from the Hydra-MDP family. Canonical source is the official arXiv version v4; no venue camera-ready was verified. Front page confirms the title and first author Zhenxin Li (5 pages). Code: the abstract's closing line reads 'More details by visiting https://github.com/NVlabs/Hydra-MDP', so code_available=YES. Tags are assigned from the paper's own title/abstract vocabulary only. decision_relevance=LOW: breadth/context record at placement depth, not tied to a live decision. Census-depth record: not deep-read, no field-placement or novelty verdict. EVIDENCE_LEVEL=DOCUMENT_VERIFIED"),
    "P0022": dict(short="DriveSuprim", title="DriveSuprim: Towards Precise Trajectory Selection for End-to-End Planning",
                  year="2025", first_author="Wenhao Yao", venue="arXiv preprint",
                  arxiv_id="2506.06659", doi="NONE",
                  official_url="https://arxiv.org/abs/2506.06659",
                  code_available="YES", official_code_url="https://github.com/William-Yao-2000/DriveSuprim",
                  tags="planning;end-to-end;trajectory-scorer", hyp="GENERAL", rel="LOW", reviewed="2026-09-14",
                  note="Phase-A Census Round 2 support batch, coverage hole: F10 strong non-WM end-to-end control. Canonical source is the official arXiv version v3. An AAAI 2026 version exists (DOI 10.1609/aaai.v40i14.38178, seen through OpenAlex) but the AAAI OJS article page returned no galley PDF link, so the camera-ready could not be verified and the preprint stays canonical. Front page confirms the title and first author Wenhao Yao (12 pages). Code: page 1 reads 'Code - https://github.com/William-Yao-2000/DriveSuprim', so code_available=YES. decision_relevance=LOW (breadth/context record). Census-depth record: no deep read, no placement or novelty verdict. EVIDENCE_LEVEL=DOCUMENT_VERIFIED"),
    "P0023": dict(short="iPad", title="iPad: Iterative Proposal-centric End-to-End Autonomous Driving",
                  year="2025", first_author="Ke Guo", venue="arXiv preprint",
                  arxiv_id="2505.15111", doi="NONE",
                  official_url="https://arxiv.org/abs/2505.15111",
                  code_available="YES", official_code_url="https://github.com/Kguo-cs/iPad",
                  tags="planning;end-to-end", hyp="GENERAL", rel="LOW", reviewed="2026-09-14",
                  note="Phase-A Census Round 2 support batch, coverage hole: F10 strong non-WM end-to-end control. Canonical source is the official arXiv version v1 (the PDF carries the arXiv stamp 'arXiv:2505.15111v1 [cs.CV] 21 May 2025'); the IEEE Robotics and Automation Letters version (DOI 10.1109/lra.2026.3723334) is not open. Front page confirms the title and first author Ke Guo (25 pages). Code: the abstract's closing line reads 'Code is available at https://github.com/Kguo-cs/iPad'. decision_relevance=LOW (breadth/context record). Census-depth record: no deep read, no placement or novelty verdict. EVIDENCE_LEVEL=DOCUMENT_VERIFIED"),
    "P0024": dict(short="DriveVLM", title="DriveVLM: The Convergence of Autonomous Driving and Large Vision-Language Models",
                  year="2024", first_author="Xiaoyu Tian", venue="arXiv preprint",
                  arxiv_id="2402.12289", doi="NONE",
                  official_url="https://arxiv.org/abs/2402.12289",
                  code_available="UNKNOWN", official_code_url="",
                  tags="planning;end-to-end", hyp="GENERAL", rel="LOW", reviewed="2026-09-14",
                  note="Phase-A Census Round 2 support batch, coverage hole: F10 representative VLA planner. Canonical source is the official arXiv version v5. Front page confirms the title and first author Xiaoyu Tian (30 pages). No repository URL is printed anywhere in the extracted text (the paper does mention a deployment video), so code_available stays UNKNOWN: absence of a printed URL is not evidence that no code exists. NOTE for the corpus tag vocabulary: there is no vision-language tag, so this VLA work carries only the closest available tags; a vocabulary extension is an owner decision. decision_relevance=LOW (breadth/context record). Census-depth record: no deep read, no placement or novelty verdict. EVIDENCE_LEVEL=DOCUMENT_VERIFIED"),
    "P0025": dict(short="OmniDrive", title="OmniDrive: A Holistic Vision-Language Dataset for Autonomous Driving with Counterfactual Reasoning",
                  year="2024", first_author="Shihao Wang", venue="CVPR 2025",
                  arxiv_id="2405.01533", doi="NONE",
                  official_url="https://openaccess.thecvf.com/content/CVPR2025/html/Wang_OmniDrive_A_Holistic_Vision-Language_Dataset_for_Autonomous_Driving_with_Counterfactual_CVPR_2025_paper.html",
                  code_available="YES", official_code_url="https://github.com/NVlabs/OmniDrive",
                  tags="planning;end-to-end;counterfactual", hyp="GENERAL", rel="LOW", reviewed="2026-09-14",
                  note="Phase-A Census Round 2 support batch, coverage hole: F10 representative VLA planner. Canonical source is the CVPR 2025 camera-ready (CVF Open Access), which supersedes arXiv:2405.01533 v2 because the official abs page carries the same title; venue camera-ready outranks a preprint. Front page confirms the title and first author Shihao Wang (11 pages). Code: the camera-ready prints https://github.com/NVlabs/OmniDrive in its page-1 affiliation block, so code_available=YES. decision_relevance=LOW (breadth/context record). Census-depth record: no deep read, no placement or novelty verdict. EVIDENCE_LEVEL=DOCUMENT_VERIFIED"),
    "P0026": dict(short="ORION", title="ORION: A Holistic End-to-End Autonomous Driving Framework by Vision-Language Instructed Action Generation",
                  year="2025", first_author="Haoyu Fu", venue="ICCV 2025",
                  arxiv_id="NONE", doi="NONE",
                  official_url="https://openaccess.thecvf.com/content/ICCV2025/html/Fu_ORION_A_Holistic_End-to-End_Autonomous_Driving_Framework_by_Vision-Language_Instructed_ICCV_2025_paper.html",
                  code_available="UNKNOWN", official_code_url="",
                  tags="planning;end-to-end", hyp="GENERAL", rel="LOW", reviewed="2026-09-14",
                  note="Phase-A Census Round 2 support batch, coverage hole: F10 representative VLA planner. Canonical source is the ICCV 2025 camera-ready (CVF Open Access); the URL was found by scanning the ICCV2025 Open Access index page because CVF truncates titles inside slugs. Front page confirms the title and first author Haoyu Fu (12 pages). The paper prints only a PROJECT PAGE, https://xiaomi-mlab.github.io/Orion/, and no repository URL, so code_available stays UNKNOWN. decision_relevance=LOW (breadth/context record). Census-depth record: no deep read, no placement or novelty verdict. EVIDENCE_LEVEL=DOCUMENT_VERIFIED"),
    "P0027": dict(short="Think2Drive", title="Think2Drive: Efficient Reinforcement Learning by Thinking with Latent World Model for Autonomous Driving (in CARLA-v2)",
                  year="2024", first_author="Qifeng Li", venue="arXiv preprint",
                  arxiv_id="2402.16720", doi="NONE",
                  official_url="https://arxiv.org/abs/2402.16720",
                  code_available="UNKNOWN", official_code_url="",
                  tags="world-model;latent-world-model;planning", hyp="GENERAL", rel="LOW", reviewed="2026-09-14",
                  note="Phase-A Census Round 2 support batch, coverage hole: world-model RL lineage. Canonical source is the official arXiv version v2. TITLE DIVERGENCE, recorded rather than smoothed over: the arXiv landing page gives 'Think2Drive: Efficient Reinforcement Learning by Thinking in Latent World Model for Quasi-Realistic Autonomous Driving', while the stored PDF's first page reads 'by Thinking with Latent World Model for Autonomous Driving (in CARLA-v2)' (front-page verdict PARTIAL for that reason); the manifest title follows the paper's own front page. First author Qifeng Li confirmed (24 pages). The paper prints a related project page (https://thinklab-sjtu.github.io/CornerCaseRepo/) and no repository URL, so code_available stays UNKNOWN. decision_relevance=LOW (breadth/context record). Census-depth record: no deep read, no placement or novelty verdict. EVIDENCE_LEVEL=DOCUMENT_VERIFIED"),
    "P0028": dict(short="ViDAR", title="Visual Point Cloud Forecasting enables Scalable Autonomous Driving",
                  year="2024", first_author="Zetong Yang", venue="CVPR 2024",
                  arxiv_id="NONE", doi="NONE",
                  official_url="https://openaccess.thecvf.com/content/CVPR2024/html/Yang_Visual_Point_Cloud_Forecasting_enables_Scalable_Autonomous_Driving_CVPR_2024_paper.html",
                  code_available="YES", official_code_url="https://github.com/OpenDriveLab/ViDAR",
                  tags="representation;trajectory-prediction;planning", hyp="GENERAL", rel="LOW", reviewed="2026-09-14",
                  note="Phase-A Census Round 2 support batch, coverage hole: representation-pretraining bridge. Canonical source is the CVPR 2024 camera-ready (CVF Open Access). NOTE: the camera-ready title does not contain the method name ViDAR used by the census atlas; the paper introduces ViDAR inside that title. Front page confirms the title and first author Zetong Yang (12 pages). Code: page 1 of the PDF prints https://github.com/OpenDriveLab/ViDAR, so code_available=YES. CONVERSION DEFECT worth knowing: that page-1 line is absent from the extracted raw MD (the MD's only repository mention is a reference to MMDetection3D), so this record's code field rests on the PDF page-1 read, not on the markdown. decision_relevance=LOW (breadth/context record). Census-depth record: no deep read, no placement or novelty verdict. EVIDENCE_LEVEL=DOCUMENT_VERIFIED"),
    "P0029": dict(short="GenAD", title="GenAD: Generative End-to-End Autonomous Driving",
                  year="2024", first_author="Wenzhao Zheng", venue="arXiv preprint",
                  arxiv_id="2402.11502", doi="NONE",
                  official_url="https://arxiv.org/abs/2402.11502",
                  code_available="YES", official_code_url="https://github.com/wzzheng/GenAD",
                  tags="planning;end-to-end;trajectory-prediction", hyp="GENERAL", rel="LOW", reviewed="2026-09-14",
                  note="Phase-A Census Round 2 support batch, coverage hole: representation-pretraining bridge. Canonical source is the official arXiv version v3; the ECCV 2024 Springer version is not open. Front page confirms the title and first author Wenzhao Zheng (10 pages). Code: the abstract ends with 'Code: https://github.com/wzzheng/GenAD'. decision_relevance=LOW (breadth/context record). Census-depth record: no deep read, no placement or novelty verdict. EVIDENCE_LEVEL=DOCUMENT_VERIFIED"),
    "P0030": dict(short="nuScenes", title="nuScenes: A Multimodal Dataset for Autonomous Driving",
                  year="2020", first_author="Holger Caesar", venue="CVPR 2020",
                  arxiv_id="NONE", doi="NONE",
                  official_url="https://openaccess.thecvf.com/content_CVPR_2020/html/Caesar_nuScenes_A_Multimodal_Dataset_for_Autonomous_Driving_CVPR_2020_paper.html",
                  code_available="UNKNOWN", official_code_url="",
                  tags="evaluation;benchmark", hyp="GENERAL", rel="LOW", reviewed="2026-09-14",
                  note="Phase-A Census Round 2 support batch, coverage hole: benchmark/evaluation lineage (the open-loop nuScenes planning legacy the atlas recalls). Canonical source is the CVPR 2020 camera-ready; CVPR 2020 uses the older CVF path layout (/content_CVPR_2020/), so the modern (CVPR20xx?day=all) index does not list it, and the URL was verified as HTTP 206 with %PDF- magic before download. Front page confirms the title and first author Holger Caesar (11 pages). The paper prints dataset-site and citation links but no repository URL, so code_available stays UNKNOWN. decision_relevance=LOW (breadth/context record). Census-depth record: no deep read, no placement or novelty verdict. EVIDENCE_LEVEL=DOCUMENT_VERIFIED"),
    "P0031": dict(short="nuPlan", title="nuPlan: A closed-loop ML-based planning benchmark for autonomous vehicles",
                  year="2021", first_author="Holger Caesar", venue="arXiv preprint",
                  arxiv_id="2106.11810", doi="NONE",
                  official_url="https://arxiv.org/abs/2106.11810",
                  code_available="UNKNOWN", official_code_url="",
                  tags="planning;closed-loop;benchmark;evaluation", hyp="GENERAL", rel="LOW", reviewed="2026-09-14",
                  note="Phase-A Census Round 2 support batch, coverage hole: benchmark/evaluation lineage (closed-loop planning benchmark). Canonical source is the official arXiv version v4. The Round-1 source register listed only the project page https://nuplan.org/nuplan, which is not a document; a peer-reviewed nuPlan paper is known to exist but was NOT verified in this batch, so this remains an open census item. Front page confirms the title and first author Holger Caesar (5 pages). No URL is printed in the extracted text, so code_available stays UNKNOWN. decision_relevance=LOW (breadth/context record). Census-depth record: no deep read, no placement or novelty verdict. EVIDENCE_LEVEL=DOCUMENT_VERIFIED"),
    "P0032": dict(short="NAVSIM", title="NAVSIM: Data-Driven Non-Reactive Autonomous Vehicle Simulation and Benchmarking",
                  year="2024", first_author="Daniel Dauner", venue="NeurIPS 2024 Datasets and Benchmarks",
                  arxiv_id="2406.15349", doi="NONE",
                  official_url="https://arxiv.org/abs/2406.15349",
                  code_available="YES", official_code_url="https://github.com/autonomousvision/navsim",
                  tags="benchmark;evaluation;planning", hyp="GENERAL", rel="LOW", reviewed="2026-09-14",
                  note="Phase-A Census Round 2 support batch, coverage hole: benchmark/evaluation lineage. Canonical source is the official arXiv version v2; the venue is recorded from the Round-1 source register, which lists the NeurIPS 2024 Datasets and Benchmarks abstract page for NAVSIM, while no camera-ready PDF was fetched in this batch. The paper's own framing is data-driven NON-REACTIVE pseudo-simulation; that distinction is recorded here rather than collapsed into a closed-loop label, and no reactive tag is applied. Front page confirms the title and first author Daniel Dauner (14 pages). Code: the abstract ends with 'Our code is available at https://github.com/autonomousvision/navsim'. decision_relevance=LOW (breadth/context record). Census-depth record: no deep read, no placement or novelty verdict. EVIDENCE_LEVEL=DOCUMENT_VERIFIED"),
    "P0033": dict(short="Bench2Drive", title="Bench2Drive: Towards Multi-Ability Benchmarking of Closed-Loop End-To-End Autonomous Driving",
                  year="2024", first_author="Xiaosong Jia", venue="arXiv preprint",
                  arxiv_id="2406.03877", doi="NONE",
                  official_url="https://arxiv.org/abs/2406.03877",
                  code_available="YES", official_code_url="https://github.com/Thinklab-SJTU/Bench2Drive",
                  tags="benchmark;closed-loop;end-to-end;evaluation", hyp="GENERAL", rel="LOW", reviewed="2026-09-14",
                  note="Phase-A Census Round 2 support batch, coverage hole: benchmark/evaluation lineage (interactive CARLA closed-loop evaluation). Canonical source is the official arXiv version v3. A NeurIPS 2024 Datasets and Benchmarks version indexed under DOI 10.52202/079017-0025 was seen in OpenAlex, but no open PDF for it was verified in this batch, so the venue is left as arXiv preprint rather than asserted. Front page confirms the title and first author Xiaosong Jia (26 pages). Code: the dataset checklist states 'All data, codes, and checkpoints are in GitHub (https://github.com/Thinklab-SJTU/Bench2Drive)', and the title page prints the project page https://thinklab-sjtu.github.io/Bench2Drive/. decision_relevance=LOW (breadth/context record). Census-depth record: no deep read, no placement or novelty verdict. EVIDENCE_LEVEL=DOCUMENT_VERIFIED"),
    "P0034": dict(short="HUGSIM", title="HUGSIM: A Real-Time, Photo-Realistic and Closed-Loop Simulator for Autonomous Driving",
                  year="2024", first_author="Hongyu Zhou", venue="arXiv preprint",
                  arxiv_id="2412.01718", doi="NONE",
                  official_url="https://arxiv.org/abs/2412.01718",
                  code_available="UNKNOWN", official_code_url="",
                  tags="closed-loop;benchmark;evaluation", hyp="GENERAL", rel="LOW", reviewed="2026-09-14",
                  note="Phase-A Census Round 2 support batch, coverage hole: benchmark/evaluation lineage (photorealistic closed-loop simulation). Canonical source is the official arXiv version v1; the IEEE TPAMI version (DOI 10.1109/tpami.2025.3647952, listed in the Round-1 source register and seen in OpenAlex) is not open. Front page confirms the title and first author Hongyu Zhou (24 pages). The extracted text contains no repository URL at all, so code_available stays UNKNOWN. First conversion attempt failed with a local MinerU service error (502 Bad Gateway while two conversion jobs ran concurrently); the paper converted cleanly when retried serially - this is a host/resource artifact, not a document problem. decision_relevance=LOW (breadth/context record). Census-depth record: no deep read, no placement or novelty verdict. EVIDENCE_LEVEL=DOCUMENT_VERIFIED"),
    # --- Phase-A Census Round 1 text-layer batch (CORPUS_BATCH=census1) ---
    # Generated by scripts/build_census1_meta.py from the identity, front-page and raw-MD
    # ledgers: titles are the official ones, tags come from the works' own wording, and code
    # availability is asserted only where the paper prints a repository URL.
    "P0035": dict(short="GAIA1",
                  title="GAIA-1: A Generative World Model for Autonomous Driving",
                  year="2023", first_author="Hu, Anthony", venue="arXiv preprint",
                  arxiv_id="2309.17080", doi="NONE",
                  official_url="https://arxiv.org/abs/2309.17080",
                  code_available="UNKNOWN", official_code_url="",
                  tags="world-model;diffusion;representation;autoregressive", hyp="GENERAL", rel="LOW", reviewed="2026-09-14",
                  note="Phase-A Census Round 1 text-layer batch (CORPUS_BATCH=census1), record created so that this work placed by landscape/CENSUS_PHASE_A_ROUND1.md has a local text layer. Official title, first author and date come from the official landing page (https://arxiv.org/abs/2309.17080), copied from manifests/batch_census1_identity.json; front-page verification of the stored PDF returned DOCUMENT_VERIFIED. Canonical source: arXiv_v1. No repository URL is printed in the extracted text; absence of a printed URL is not evidence that no code exists, so code_available stays UNKNOWN. Tags are assigned mechanically from the fixed corpus vocabulary by counting the work's own title and text ('world-model;diffusion;representation;autoregressive'), not from any field placement. Conversion QC: RAW_MD_READY. decision_relevance=LOW: this batch exists to make the census readable locally, and it makes no claim about whether the work is decision-relevant. Census-depth record: no deep read, no field placement, no novelty or gap verdict. EVIDENCE_LEVEL=DOCUMENT_VERIFIED"),
    "P0036": dict(short="DriveDreamer",
                  title="DriveDreamer: Towards Real-world-driven World Models for Autonomous Driving",
                  year="2023", first_author="Wang, Xiaofeng", venue="arXiv preprint",
                  arxiv_id="2309.09777", doi="NONE",
                  official_url="https://arxiv.org/abs/2309.09777",
                  code_available="UNKNOWN", official_code_url="",
                  tags="world-model;diffusion;representation;evaluation", hyp="GENERAL", rel="LOW", reviewed="2026-09-14",
                  note="Phase-A Census Round 1 text-layer batch (CORPUS_BATCH=census1), record created so that this work placed by landscape/CENSUS_PHASE_A_ROUND1.md has a local text layer. Official title, first author and date come from the official landing page (https://arxiv.org/abs/2309.09777), copied from manifests/batch_census1_identity.json; front-page verification of the stored PDF returned DOCUMENT_VERIFIED. Canonical source: arXiv_v2. The text prints a PROJECT PAGE only (https://drivedreamer.github.io); a project page is not a repository, and absence of a printed URL is not evidence that no code exists, so code_available stays UNKNOWN. Tags are assigned mechanically from the fixed corpus vocabulary by counting the work's own title and text ('world-model;diffusion;representation;evaluation'), not from any field placement. Conversion QC: RAW_MD_READY. decision_relevance=LOW: this batch exists to make the census readable locally, and it makes no claim about whether the work is decision-relevant. Census-depth record: no deep read, no field placement, no novelty or gap verdict. EVIDENCE_LEVEL=DOCUMENT_VERIFIED"),
    "P0037": dict(short="DriveWM",
                  title="Driving into the Future: Multiview Visual Forecasting and Planning with World Model for Autonomous Driving",
                  year="2024", first_author="Wang, Yuqi", venue="CVPR 2024",
                  arxiv_id="", doi="NONE",
                  official_url="https://openaccess.thecvf.com/content/CVPR2024/html/Wang_Driving_into_the_Future_Multiview_Visual_Forecasting_and_Planning_with_CVPR_2024_paper.html",
                  code_available="YES", official_code_url="https://github.com/BraveGroup/Drive-WM",
                  tags="planning;world-model;diffusion;end-to-end", hyp="GENERAL", rel="LOW", reviewed="2026-09-14",
                  note="Phase-A Census Round 1 text-layer batch (CORPUS_BATCH=census1), record created so that this work placed by landscape/CENSUS_PHASE_A_ROUND1.md has a local text layer. Official title, first author and date come from the official landing page (https://openaccess.thecvf.com/content/CVPR2024/html/Wang_Driving_into_the_Future_Multiview_Visual_Forecasting_and_Planning_with_CVPR_2024_paper.html), copied from manifests/batch_census1_identity.json; front-page verification of the stored PDF returned DOCUMENT_VERIFIED. Canonical source: CVPR2024_camera_ready. Code: the paper itself prints https://github.com/BraveGroup/Drive-WM (seen in the raw markdown, position 9), so code_available=YES. Tags are assigned mechanically from the fixed corpus vocabulary by counting the work's own title and text ('planning;world-model;diffusion;end-to-end'), not from any field placement. Conversion QC: RAW_MD_READY. decision_relevance=LOW: this batch exists to make the census readable locally, and it makes no claim about whether the work is decision-relevant. Census-depth record: no deep read, no field placement, no novelty or gap verdict. EVIDENCE_LEVEL=DOCUMENT_VERIFIED"),
    "P0038": dict(short="Vista",
                  title="Vista: A Generalizable Driving World Model with High Fidelity and Versatile Controllability",
                  year="2024", first_author="Gao, Shenyuan", venue="arXiv preprint",
                  arxiv_id="2405.17398", doi="NONE",
                  official_url="https://arxiv.org/abs/2405.17398",
                  code_available="YES", official_code_url="https://github.com/OpenDriveLab/Vista",
                  tags="world-model;diffusion;evaluation;planning", hyp="GENERAL", rel="LOW", reviewed="2026-09-14",
                  note="Phase-A Census Round 1 text-layer batch (CORPUS_BATCH=census1), record created so that this work placed by landscape/CENSUS_PHASE_A_ROUND1.md has a local text layer. Official title, first author and date come from the official landing page (https://arxiv.org/abs/2405.17398), copied from manifests/batch_census1_identity.json; front-page verification of the stored PDF returned DOCUMENT_VERIFIED. Canonical source: arXiv_v5. Code: the paper itself prints https://github.com/OpenDriveLab/Vista (seen in the raw markdown, position 7), so code_available=YES. Tags are assigned mechanically from the fixed corpus vocabulary by counting the work's own title and text ('world-model;diffusion;evaluation;planning'), not from any field placement. Conversion QC: RAW_MD_READY. decision_relevance=LOW: this batch exists to make the census readable locally, and it makes no claim about whether the work is decision-relevant. Census-depth record: no deep read, no field placement, no novelty or gap verdict. EVIDENCE_LEVEL=DOCUMENT_VERIFIED"),
    "P0039": dict(short="DriveDreamer2",
                  title="DriveDreamer-2: LLM-Enhanced World Models for Diverse Driving Video Generation",
                  year="2024", first_author="Zhao, Guosheng", venue="arXiv preprint",
                  arxiv_id="2403.06845", doi="NONE",
                  official_url="https://arxiv.org/abs/2403.06845",
                  code_available="UNKNOWN", official_code_url="",
                  tags="world-model;evaluation", hyp="GENERAL", rel="LOW", reviewed="2026-09-14",
                  note="Phase-A Census Round 1 text-layer batch (CORPUS_BATCH=census1), record created so that this work placed by landscape/CENSUS_PHASE_A_ROUND1.md has a local text layer. Official title, first author and date come from the official landing page (https://arxiv.org/abs/2403.06845), copied from manifests/batch_census1_identity.json; front-page verification of the stored PDF returned DOCUMENT_VERIFIED. Canonical source: arXiv_v2. The text prints a PROJECT PAGE only (https://drivedreamer2.github.io); a project page is not a repository, and absence of a printed URL is not evidence that no code exists, so code_available stays UNKNOWN. Tags are assigned mechanically from the fixed corpus vocabulary by counting the work's own title and text ('world-model;evaluation'), not from any field placement. Conversion QC: RAW_MD_READY. decision_relevance=LOW: this batch exists to make the census readable locally, and it makes no claim about whether the work is decision-relevant. Census-depth record: no deep read, no field placement, no novelty or gap verdict. EVIDENCE_LEVEL=DOCUMENT_VERIFIED"),
    "P0040": dict(short="DrivingGPT",
                  title="DrivingGPT: Unifying Driving World Modeling and Planning with Multi-modal Autoregressive Transformers",
                  year="2025", first_author="Chen, Yuntao", venue="ICCV 2025",
                  arxiv_id="", doi="NONE",
                  official_url="https://openaccess.thecvf.com/content/ICCV2025/html/Chen_DrivingGPT_Unifying_Driving_World_Modeling_and_Planning_with_Multi-modal_Autoregressive_ICCV_2025_paper.html",
                  code_available="UNKNOWN", official_code_url="",
                  tags="planning;world-model;autoregressive;end-to-end", hyp="GENERAL", rel="LOW", reviewed="2026-09-14",
                  note="Phase-A Census Round 1 text-layer batch (CORPUS_BATCH=census1), record created so that this work placed by landscape/CENSUS_PHASE_A_ROUND1.md has a local text layer. Official title, first author and date come from the official landing page (https://openaccess.thecvf.com/content/ICCV2025/html/Chen_DrivingGPT_Unifying_Driving_World_Modeling_and_Planning_with_Multi-modal_Autoregressive_ICCV_2025_paper.html), copied from manifests/batch_census1_identity.json; front-page verification of the stored PDF returned DOCUMENT_VERIFIED. Canonical source: ICCV2025_camera_ready. The text prints a PROJECT PAGE only (https://rogerchern.github.io/DrivingGPT); a project page is not a repository, and absence of a printed URL is not evidence that no code exists, so code_available stays UNKNOWN. Tags are assigned mechanically from the fixed corpus vocabulary by counting the work's own title and text ('planning;world-model;autoregressive;end-to-end'), not from any field placement. Conversion QC: RAW_MD_READY. decision_relevance=LOW: this batch exists to make the census readable locally, and it makes no claim about whether the work is decision-relevant. Census-depth record: no deep read, no field placement, no novelty or gap verdict. EVIDENCE_LEVEL=DOCUMENT_VERIFIED"),
    "P0041": dict(short="PolicyWM",
                  title="From Forecasting to Planning: Policy World Model for Collaborative State-Action Prediction",
                  year="2025", first_author="Zhao, Zhida", venue="arXiv preprint",
                  arxiv_id="2510.19654", doi="NONE",
                  official_url="https://arxiv.org/abs/2510.19654",
                  code_available="YES", official_code_url="https://github.com/6550Zhao/Policy-World-Model",
                  tags="planning;world-model;end-to-end;representation", hyp="GENERAL", rel="LOW", reviewed="2026-09-14",
                  note="Phase-A Census Round 1 text-layer batch (CORPUS_BATCH=census1), record created so that this work placed by landscape/CENSUS_PHASE_A_ROUND1.md has a local text layer. Official title, first author and date come from the official landing page (https://arxiv.org/abs/2510.19654), copied from manifests/batch_census1_identity.json; front-page verification of the stored PDF returned DOCUMENT_VERIFIED. Canonical source: arXiv_v2. Code: the paper itself prints https://github.com/6550Zhao/Policy-World-Model (seen in the raw markdown, position 7), so code_available=YES. Tags are assigned mechanically from the fixed corpus vocabulary by counting the work's own title and text ('planning;world-model;end-to-end;representation'), not from any field placement. Conversion QC: RAW_MD_READY. decision_relevance=LOW: this batch exists to make the census readable locally, and it makes no claim about whether the work is decision-relevant. Census-depth record: no deep read, no field placement, no novelty or gap verdict. EVIDENCE_LEVEL=DOCUMENT_VERIFIED"),
    "P0042": dict(short="WorldDrive",
                  title="Bridging Scene Generation and Planning: Driving with World Model via Unifying Vision and Motion Representation",
                  year="2026", first_author="Gui, Xingtai", venue="arXiv preprint",
                  arxiv_id="2603.14948", doi="NONE",
                  official_url="https://arxiv.org/abs/2603.14948",
                  code_available="YES", official_code_url="https://github.com/TabGuigui/WorldDrive",
                  tags="planning;world-model;representation;diffusion", hyp="GENERAL", rel="LOW", reviewed="2026-09-14",
                  note="Phase-A Census Round 1 text-layer batch (CORPUS_BATCH=census1), record created so that this work placed by landscape/CENSUS_PHASE_A_ROUND1.md has a local text layer. Official title, first author and date come from the official landing page (https://arxiv.org/abs/2603.14948), copied from manifests/batch_census1_identity.json; front-page verification of the stored PDF returned DOCUMENT_VERIFIED. Canonical source: arXiv_v1. Code: the paper itself prints https://github.com/TabGuigui/WorldDrive (seen in the raw markdown, position 7), so code_available=YES. Tags are assigned mechanically from the fixed corpus vocabulary by counting the work's own title and text ('planning;world-model;representation;diffusion'), not from any field placement. Conversion QC: RAW_MD_READY. decision_relevance=LOW: this batch exists to make the census readable locally, and it makes no claim about whether the work is decision-relevant. Census-depth record: no deep read, no field placement, no novelty or gap verdict. EVIDENCE_LEVEL=DOCUMENT_VERIFIED"),
    "P0043": dict(short="OccWorld",
                  title="OccWorld: Learning a 3D Occupancy World Model for Autonomous Driving",
                  year="2023", first_author="Zheng, Wenzhao", venue="arXiv preprint",
                  arxiv_id="2311.16038", doi="NONE",
                  official_url="https://arxiv.org/abs/2311.16038",
                  code_available="YES", official_code_url="https://github.com/wzzheng/OccWorld",
                  tags="world-model;planning;representation;end-to-end", hyp="GENERAL", rel="LOW", reviewed="2026-09-14",
                  note="Phase-A Census Round 1 text-layer batch (CORPUS_BATCH=census1), record created so that this work placed by landscape/CENSUS_PHASE_A_ROUND1.md has a local text layer. Official title, first author and date come from the official landing page (https://arxiv.org/abs/2311.16038), copied from manifests/batch_census1_identity.json; front-page verification of the stored PDF returned DOCUMENT_VERIFIED. Canonical source: arXiv_v1. Code: the paper itself prints https://github.com/wzzheng/OccWorld (seen in the raw markdown, position 19), so code_available=YES. Tags are assigned mechanically from the fixed corpus vocabulary by counting the work's own title and text ('world-model;planning;representation;end-to-end'), not from any field placement. Conversion QC: RAW_MD_READY. decision_relevance=LOW: this batch exists to make the census readable locally, and it makes no claim about whether the work is decision-relevant. Census-depth record: no deep read, no field placement, no novelty or gap verdict. EVIDENCE_LEVEL=DOCUMENT_VERIFIED"),
    "P0044": dict(short="DriveOccWorld",
                  title="Driving in the Occupancy World: Vision-Centric 4D Occupancy Forecasting and Planning via World Models for Autonomous Driving",
                  year="2024", first_author="Yang, Yu", venue="arXiv preprint",
                  arxiv_id="2408.14197", doi="NONE",
                  official_url="https://arxiv.org/abs/2408.14197",
                  code_available="UNKNOWN", official_code_url="",
                  tags="planning;world-model;end-to-end;representation", hyp="GENERAL", rel="LOW", reviewed="2026-09-14",
                  note="Phase-A Census Round 1 text-layer batch (CORPUS_BATCH=census1), record created so that this work placed by landscape/CENSUS_PHASE_A_ROUND1.md has a local text layer. Official title, first author and date come from the official landing page (https://arxiv.org/abs/2408.14197), copied from manifests/batch_census1_identity.json; front-page verification of the stored PDF returned DOCUMENT_VERIFIED. Canonical source: arXiv_v3. The text prints a PROJECT PAGE only (https://drive-occworld.github.io/); a project page is not a repository, and absence of a printed URL is not evidence that no code exists, so code_available stays UNKNOWN. Tags are assigned mechanically from the fixed corpus vocabulary by counting the work's own title and text ('planning;world-model;end-to-end;representation'), not from any field placement. Conversion QC: RAW_MD_READY. decision_relevance=LOW: this batch exists to make the census readable locally, and it makes no claim about whether the work is decision-relevant. Census-depth record: no deep read, no field placement, no novelty or gap verdict. EVIDENCE_LEVEL=DOCUMENT_VERIFIED"),
    "P0045": dict(short="WoTE",
                  title="End-to-End Driving with Online Trajectory Evaluation via BEV World Model",
                  year="2025", first_author="Li, Yingyan", venue="ICCV 2025",
                  arxiv_id="", doi="NONE",
                  official_url="https://openaccess.thecvf.com/content/ICCV2025/html/Li_End-to-End_Driving_with_Online_Trajectory_Evaluation_via_BEV_World_Model_ICCV_2025_paper.html",
                  code_available="UNKNOWN", official_code_url="",
                  tags="world-model;end-to-end;evaluation;benchmark", hyp="GENERAL", rel="LOW", reviewed="2026-09-14",
                  note="Phase-A Census Round 1 text-layer batch (CORPUS_BATCH=census1), record created so that this work placed by landscape/CENSUS_PHASE_A_ROUND1.md has a local text layer. Official title, first author and date come from the official landing page (https://openaccess.thecvf.com/content/ICCV2025/html/Li_End-to-End_Driving_with_Online_Trajectory_Evaluation_via_BEV_World_Model_ICCV_2025_paper.html), copied from manifests/batch_census1_identity.json; front-page verification of the stored PDF returned DOCUMENT_VERIFIED. Canonical source: ICCV2025_camera_ready. No repository URL is printed in the extracted text; absence of a printed URL is not evidence that no code exists, so code_available stays UNKNOWN. Tags are assigned mechanically from the fixed corpus vocabulary by counting the work's own title and text ('world-model;end-to-end;evaluation;benchmark'), not from any field placement. Conversion QC: RAW_MD_READY. decision_relevance=LOW: this batch exists to make the census readable locally, and it makes no claim about whether the work is decision-relevant. Census-depth record: no deep read, no field placement, no novelty or gap verdict. EVIDENCE_LEVEL=DOCUMENT_VERIFIED"),
    "P0046": dict(short="World4Drive",
                  title="World4Drive: End-to-End Autonomous Driving via Intention-aware Physical Latent World Model",
                  year="2025", first_author="Zheng, Yupeng", venue="ICCV 2025",
                  arxiv_id="", doi="NONE",
                  official_url="https://openaccess.thecvf.com/content/ICCV2025/html/Zheng_World4Drive_End-to-End_Autonomous_Driving_via_Intention-aware_Physical_Latent_World_Model_ICCV_2025_paper.html",
                  code_available="YES", official_code_url="https://github.com/ucaszyp/World4Drive",
                  tags="world-model;end-to-end;latent-world-model;planning", hyp="GENERAL", rel="LOW", reviewed="2026-09-14",
                  note="Phase-A Census Round 1 text-layer batch (CORPUS_BATCH=census1), record created so that this work placed by landscape/CENSUS_PHASE_A_ROUND1.md has a local text layer. Official title, first author and date come from the official landing page (https://openaccess.thecvf.com/content/ICCV2025/html/Zheng_World4Drive_End-to-End_Autonomous_Driving_via_Intention-aware_Physical_Latent_World_Model_ICCV_2025_paper.html), copied from manifests/batch_census1_identity.json; front-page verification of the stored PDF returned DOCUMENT_VERIFIED. Canonical source: ICCV2025_camera_ready. Code: the paper itself prints https://github.com/ucaszyp/World4Drive (seen in the raw markdown, position 8), so code_available=YES. Tags are assigned mechanically from the fixed corpus vocabulary by counting the work's own title and text ('world-model;end-to-end;latent-world-model;planning'), not from any field placement. Conversion QC: RAW_MD_READY. decision_relevance=LOW: this batch exists to make the census readable locally, and it makes no claim about whether the work is decision-relevant. Census-depth record: no deep read, no field placement, no novelty or gap verdict. EVIDENCE_LEVEL=DOCUMENT_VERIFIED"),
    "P0047": dict(short="DriveWorld",
                  title="DriveWorld: 4D Pre-trained Scene Understanding via World Models for Autonomous Driving",
                  year="2024", first_author="Min, Chen", venue="CVPR 2024",
                  arxiv_id="", doi="NONE",
                  official_url="https://openaccess.thecvf.com/content/CVPR2024/html/Min_DriveWorld_4D_Pre-trained_Scene_Understanding_via_World_Models_for_Autonomous_CVPR_2024_paper.html",
                  code_available="UNKNOWN", official_code_url="",
                  tags="world-model;representation;planning;end-to-end", hyp="GENERAL", rel="LOW", reviewed="2026-09-14",
                  note="Phase-A Census Round 1 text-layer batch (CORPUS_BATCH=census1), record created so that this work placed by landscape/CENSUS_PHASE_A_ROUND1.md has a local text layer. Official title, first author and date come from the official landing page (https://openaccess.thecvf.com/content/CVPR2024/html/Min_DriveWorld_4D_Pre-trained_Scene_Understanding_via_World_Models_for_Autonomous_CVPR_2024_paper.html), copied from manifests/batch_census1_identity.json; front-page verification of the stored PDF returned DOCUMENT_VERIFIED. Canonical source: CVPR2024_camera_ready. No repository URL is printed in the extracted text; absence of a printed URL is not evidence that no code exists, so code_available stays UNKNOWN. Tags are assigned mechanically from the fixed corpus vocabulary by counting the work's own title and text ('world-model;representation;planning;end-to-end'), not from any field placement. Conversion QC: RAW_MD_READY. decision_relevance=LOW: this batch exists to make the census readable locally, and it makes no claim about whether the work is decision-relevant. Census-depth record: no deep read, no field placement, no novelty or gap verdict. EVIDENCE_LEVEL=DOCUMENT_VERIFIED"),
    "P0048": dict(short="LAW",
                  title="Enhancing End-to-End Autonomous Driving with Latent World Model",
                  year="2024", first_author="Li, Yingyan", venue="arXiv preprint",
                  arxiv_id="2406.08481", doi="NONE",
                  official_url="https://arxiv.org/abs/2406.08481",
                  code_available="YES", official_code_url="https://github.com/BraveGroup/LAW",
                  tags="world-model;end-to-end;latent-world-model;benchmark", hyp="GENERAL", rel="LOW", reviewed="2026-09-14",
                  note="Phase-A Census Round 1 text-layer batch (CORPUS_BATCH=census1), record created so that this work placed by landscape/CENSUS_PHASE_A_ROUND1.md has a local text layer. Official title, first author and date come from the official landing page (https://arxiv.org/abs/2406.08481), copied from manifests/batch_census1_identity.json; front-page verification of the stored PDF returned DOCUMENT_VERIFIED. Canonical source: arXiv_v2. Code: the paper itself prints https://github.com/BraveGroup/LAW (seen in the raw markdown, position 17), so code_available=YES. Tags are assigned mechanically from the fixed corpus vocabulary by counting the work's own title and text ('world-model;end-to-end;latent-world-model;benchmark'), not from any field placement. Conversion QC: RAW_MD_READY. decision_relevance=LOW: this batch exists to make the census readable locally, and it makes no claim about whether the work is decision-relevant. Census-depth record: no deep read, no field placement, no novelty or gap verdict. EVIDENCE_LEVEL=DOCUMENT_VERIFIED"),
    "P0049": dict(short="DriveJEPA",
                  title="Drive-JEPA: Video JEPA Meets Multimodal Trajectory Distillation for End-to-End Driving",
                  year="2026", first_author="Wang, Linhan", venue="arXiv preprint",
                  arxiv_id="2601.22032", doi="NONE",
                  official_url="https://arxiv.org/abs/2601.22032",
                  code_available="YES", official_code_url="https://github.com/linhanwang/Drive-JEPA",
                  tags="end-to-end;representation;planning;world-model", hyp="GENERAL", rel="LOW", reviewed="2026-09-14",
                  note="Phase-A Census Round 1 text-layer batch (CORPUS_BATCH=census1), record created so that this work placed by landscape/CENSUS_PHASE_A_ROUND1.md has a local text layer. Official title, first author and date come from the official landing page (https://arxiv.org/abs/2601.22032), copied from manifests/batch_census1_identity.json; front-page verification of the stored PDF returned DOCUMENT_VERIFIED. Canonical source: arXiv_v2. Code: the paper itself prints https://github.com/linhanwang/Drive-JEPA (seen in the raw markdown, position 15), so code_available=YES. Tags are assigned mechanically from the fixed corpus vocabulary by counting the work's own title and text ('end-to-end;representation;planning;world-model'), not from any field placement. Conversion QC: RAW_MD_READY. decision_relevance=LOW: this batch exists to make the census readable locally, and it makes no claim about whether the work is decision-relevant. Census-depth record: no deep read, no field placement, no novelty or gap verdict. EVIDENCE_LEVEL=DOCUMENT_VERIFIED"),
    "P0050": dict(short="WorldRFT",
                  title="WorldRFT: Latent World Model Planning with Reinforcement Fine-Tuning for Autonomous Driving",
                  year="2025", first_author="Yang, Pengxuan", venue="arXiv preprint",
                  arxiv_id="2512.19133", doi="NONE",
                  official_url="https://arxiv.org/abs/2512.19133",
                  code_available="YES", official_code_url="https://github.com/pengxuanyang/WorldRFT",
                  tags="planning;world-model;latent-world-model;representation", hyp="GENERAL", rel="LOW", reviewed="2026-09-14",
                  note="Phase-A Census Round 1 text-layer batch (CORPUS_BATCH=census1), record created so that this work placed by landscape/CENSUS_PHASE_A_ROUND1.md has a local text layer. Official title, first author and date come from the official landing page (https://arxiv.org/abs/2512.19133), copied from manifests/batch_census1_identity.json; front-page verification of the stored PDF returned DOCUMENT_VERIFIED. Canonical source: arXiv_v1. Code: the paper itself prints https://github.com/pengxuanyang/WorldRFT (seen in the raw markdown, position 11), so code_available=YES. Tags are assigned mechanically from the fixed corpus vocabulary by counting the work's own title and text ('planning;world-model;latent-world-model;representation'), not from any field placement. Conversion QC: RAW_MD_READY. decision_relevance=LOW: this batch exists to make the census readable locally, and it makes no claim about whether the work is decision-relevant. Census-depth record: no deep read, no field placement, no novelty or gap verdict. EVIDENCE_LEVEL=DOCUMENT_VERIFIED"),
    "P0051": dict(short="AutoJEPA",
                  title="Auto-JEPA: A Latent World Model of Continuous Intent for End-to-End Autonomous Driving",
                  year="2026", first_author="Yang, Jiwei", venue="arXiv preprint",
                  arxiv_id="2607.29031", doi="NONE",
                  official_url="https://arxiv.org/abs/2607.29031",
                  code_available="YES", official_code_url="https://github.com/NoctYang/Auto-JEPA",
                  tags="world-model;end-to-end;latent-world-model;planning", hyp="GENERAL", rel="LOW", reviewed="2026-09-14",
                  note="Phase-A Census Round 1 text-layer batch (CORPUS_BATCH=census1), record created so that this work placed by landscape/CENSUS_PHASE_A_ROUND1.md has a local text layer. Official title, first author and date come from the official landing page (https://arxiv.org/abs/2607.29031), copied from manifests/batch_census1_identity.json; front-page verification of the stored PDF returned DOCUMENT_VERIFIED. Canonical source: arXiv_v1. Code: the paper itself prints https://github.com/NoctYang/Auto-JEPA (seen in the raw markdown, position 11), so code_available=YES. Tags are assigned mechanically from the fixed corpus vocabulary by counting the work's own title and text ('world-model;end-to-end;latent-world-model;planning'), not from any field placement. Conversion QC: RAW_MD_READY. decision_relevance=LOW: this batch exists to make the census readable locally, and it makes no claim about whether the work is decision-relevant. Census-depth record: no deep read, no field placement, no novelty or gap verdict. EVIDENCE_LEVEL=DOCUMENT_VERIFIED"),
    "P0052": dict(short="ReWorld",
                  title="ReWorld: Representation Learning for World Action Models",
                  year="2026", first_author="Xia, Tianze", venue="arXiv preprint",
                  arxiv_id="2606.27504", doi="NONE",
                  official_url="https://arxiv.org/abs/2606.27504",
                  code_available="YES", official_code_url="https://github.com/xiaomi-research/ReWorld",
                  tags="representation;planning;world-model;diffusion", hyp="GENERAL", rel="LOW", reviewed="2026-09-14",
                  note="Phase-A Census Round 1 text-layer batch (CORPUS_BATCH=census1), record created so that this work placed by landscape/CENSUS_PHASE_A_ROUND1.md has a local text layer. Official title, first author and date come from the official landing page (https://arxiv.org/abs/2606.27504), copied from manifests/batch_census1_identity.json; front-page verification of the stored PDF returned DOCUMENT_VERIFIED. Canonical source: arXiv_v2. Code: the paper itself prints https://github.com/xiaomi-research/ReWorld (seen in the raw markdown, position 5), so code_available=YES. Tags are assigned mechanically from the fixed corpus vocabulary by counting the work's own title and text ('representation;planning;world-model;diffusion'), not from any field placement. Conversion QC: RAW_MD_READY. decision_relevance=LOW: this batch exists to make the census readable locally, and it makes no claim about whether the work is decision-relevant. Census-depth record: no deep read, no field placement, no novelty or gap verdict. EVIDENCE_LEVEL=DOCUMENT_VERIFIED"),
    "P0053": dict(short="WAJEPA",
                  title="WA-JEPA: Rethinking the Video JEPA Paradigm for World-Action Modeling in Autonomous Driving",
                  year="2026", first_author="Wang, Xinlin", venue="arXiv preprint",
                  arxiv_id="2608.20974", doi="NONE",
                  official_url="https://arxiv.org/abs/2608.20974",
                  code_available="YES", official_code_url="https://github.com/AFARI-Research/WA-JEPA",
                  tags="representation;planning;end-to-end;world-model", hyp="GENERAL", rel="LOW", reviewed="2026-09-14",
                  note="Phase-A Census Round 1 text-layer batch (CORPUS_BATCH=census1), record created so that this work placed by landscape/CENSUS_PHASE_A_ROUND1.md has a local text layer. Official title, first author and date come from the official landing page (https://arxiv.org/abs/2608.20974), copied from manifests/batch_census1_identity.json; front-page verification of the stored PDF returned DOCUMENT_VERIFIED. Canonical source: arXiv_v2. Code: the paper itself prints https://github.com/AFARI-Research/WA-JEPA (seen in the raw markdown, position 13), so code_available=YES. Tags are assigned mechanically from the fixed corpus vocabulary by counting the work's own title and text ('representation;planning;end-to-end;world-model'), not from any field placement. Conversion QC: RAW_MD_READY. decision_relevance=LOW: this batch exists to make the census readable locally, and it makes no claim about whether the work is decision-relevant. Census-depth record: no deep read, no field placement, no novelty or gap verdict. EVIDENCE_LEVEL=DOCUMENT_VERIFIED"),
    "P0054": dict(short="WhatTrulyMatters",
                  title="What Truly Matters in Trajectory Prediction for Autonomous Driving?",
                  year="2023", first_author="Phong, Tran", venue="NeurIPS 2023",
                  arxiv_id="", doi="NONE",
                  official_url="https://papers.neurips.cc/paper_files/paper/2023/hash/e197fe307eb3467035f892dc100d570a-Abstract-Conference.html",
                  code_available="UNKNOWN", official_code_url="",
                  tags="trajectory-prediction;evaluation;planning;interactive", hyp="GENERAL", rel="LOW", reviewed="2026-09-14",
                  note="Phase-A Census Round 1 text-layer batch (CORPUS_BATCH=census1), record created so that this work placed by landscape/CENSUS_PHASE_A_ROUND1.md has a local text layer. Official title, first author and date come from the official landing page (https://papers.neurips.cc/paper_files/paper/2023/hash/e197fe307eb3467035f892dc100d570a-Abstract-Conference.html), copied from manifests/batch_census1_identity.json; front-page verification of the stored PDF returned DOCUMENT_VERIFIED. Canonical source: NeurIPS2023_camera_ready. No repository URL is printed in the extracted text; absence of a printed URL is not evidence that no code exists, so code_available stays UNKNOWN. Tags are assigned mechanically from the fixed corpus vocabulary by counting the work's own title and text ('trajectory-prediction;evaluation;planning;interactive'), not from any field placement. Conversion QC: RAW_MD_READY. decision_relevance=LOW: this batch exists to make the census readable locally, and it makes no claim about whether the work is decision-relevant. Census-depth record: no deep read, no field placement, no novelty or gap verdict. EVIDENCE_LEVEL=DOCUMENT_VERIFIED"),
    "P0055": dict(short="SLEDGE",
                  title="SLEDGE: Synthesizing Driving Environments with Generative Models and Rule-Based Traffic",
                  year="2024", first_author="Chitta, Kashyap", venue="arXiv preprint",
                  arxiv_id="2403.17933", doi="NONE",
                  official_url="https://arxiv.org/abs/2403.17933",
                  code_available="YES", official_code_url="https://github.com/autonomousvision/sledge",
                  tags="representation;planning;benchmark;evaluation", hyp="GENERAL", rel="LOW", reviewed="2026-09-14",
                  note="Phase-A Census Round 1 text-layer batch (CORPUS_BATCH=census1), record created so that this work placed by landscape/CENSUS_PHASE_A_ROUND1.md has a local text layer. Official title, first author and date come from the official landing page (https://arxiv.org/abs/2403.17933), copied from manifests/batch_census1_identity.json; front-page verification of the stored PDF returned DOCUMENT_VERIFIED. Canonical source: arXiv_v2. Code: the paper itself prints https://github.com/autonomousvision/sledge (seen in the raw markdown, position 5), so code_available=YES. Tags are assigned mechanically from the fixed corpus vocabulary by counting the work's own title and text ('representation;planning;benchmark;evaluation'), not from any field placement. Conversion QC: RAW_MD_READY. decision_relevance=LOW: this batch exists to make the census readable locally, and it makes no claim about whether the work is decision-relevant. Census-depth record: no deep read, no field placement, no novelty or gap verdict. EVIDENCE_LEVEL=DOCUMENT_VERIFIED"),
    "P0056": dict(short="DriveArena",
                  title="DriveArena: A Closed-loop Generative Simulation Platform for Autonomous Driving",
                  year="2024", first_author="Yang, Xuemeng", venue="arXiv preprint",
                  arxiv_id="2408.00415", doi="NONE",
                  official_url="https://arxiv.org/abs/2408.00415",
                  code_available="YES", official_code_url="https://github.com/PJLab-ADG/DriveArena",
                  tags="closed-loop;diffusion;open-loop;evaluation", hyp="GENERAL", rel="LOW", reviewed="2026-09-14",
                  note="Phase-A Census Round 1 text-layer batch (CORPUS_BATCH=census1), record created so that this work placed by landscape/CENSUS_PHASE_A_ROUND1.md has a local text layer. Official title, first author and date come from the official landing page (https://arxiv.org/abs/2408.00415), copied from manifests/batch_census1_identity.json; front-page verification of the stored PDF returned DOCUMENT_VERIFIED. Canonical source: arXiv_v1. Code: the paper itself prints https://github.com/PJLab-ADG/DriveArena (seen in the raw markdown, position 19), so code_available=YES. Tags are assigned mechanically from the fixed corpus vocabulary by counting the work's own title and text ('closed-loop;diffusion;open-loop;evaluation'), not from any field placement. Conversion QC: RAW_MD_READY. decision_relevance=LOW: this batch exists to make the census readable locally, and it makes no claim about whether the work is decision-relevant. Census-depth record: no deep read, no field placement, no novelty or gap verdict. EVIDENCE_LEVEL=DOCUMENT_VERIFIED"),
    "P0057": dict(short="UniAD",
                  title="Planning-Oriented Autonomous Driving",
                  year="2023", first_author="Hu, Yihan", venue="CVPR 2023",
                  arxiv_id="", doi="NONE",
                  official_url="https://openaccess.thecvf.com/content/CVPR2023/html/Hu_Planning-Oriented_Autonomous_Driving_CVPR_2023_paper.html",
                  code_available="YES", official_code_url="https://github.com/OpenDriveLab/UniAD",
                  tags="planning;end-to-end;representation", hyp="GENERAL", rel="LOW", reviewed="2026-09-14",
                  note="Phase-A Census Round 1 text-layer batch (CORPUS_BATCH=census1), record created so that this work placed by landscape/CENSUS_PHASE_A_ROUND1.md has a local text layer. Official title, first author and date come from the official landing page (https://openaccess.thecvf.com/content/CVPR2023/html/Hu_Planning-Oriented_Autonomous_Driving_CVPR_2023_paper.html), copied from manifests/batch_census1_identity.json; front-page verification of the stored PDF returned DOCUMENT_VERIFIED. Canonical source: CVPR2023_camera_ready. Code: the paper itself prints https://github.com/OpenDriveLab/UniAD (seen in the raw markdown, position 5), so code_available=YES. Tags are assigned mechanically from the fixed corpus vocabulary by counting the work's own title and text ('planning;end-to-end;representation'), not from any field placement. Conversion QC: RAW_MD_READY. decision_relevance=LOW: this batch exists to make the census readable locally, and it makes no claim about whether the work is decision-relevant. Census-depth record: no deep read, no field placement, no novelty or gap verdict. EVIDENCE_LEVEL=DOCUMENT_VERIFIED"),
    "P0058": dict(short="VAD",
                  title="VAD: Vectorized Scene Representation for Efficient Autonomous Driving",
                  year="2023", first_author="Jiang, Bo", venue="ICCV 2023",
                  arxiv_id="", doi="NONE",
                  official_url="https://openaccess.thecvf.com/content/ICCV2023/html/Jiang_VAD_Vectorized_Scene_Representation_for_Efficient_Autonomous_Driving_ICCV_2023_paper.html",
                  code_available="YES", official_code_url="https://github.com/hustvl/VAD",
                  tags="representation;planning;end-to-end;safety", hyp="GENERAL", rel="LOW", reviewed="2026-09-14",
                  note="Phase-A Census Round 1 text-layer batch (CORPUS_BATCH=census1), record created so that this work placed by landscape/CENSUS_PHASE_A_ROUND1.md has a local text layer. Official title, first author and date come from the official landing page (https://openaccess.thecvf.com/content/ICCV2023/html/Jiang_VAD_Vectorized_Scene_Representation_for_Efficient_Autonomous_Driving_ICCV_2023_paper.html), copied from manifests/batch_census1_identity.json; front-page verification of the stored PDF returned DOCUMENT_VERIFIED. Canonical source: ICCV2023_camera_ready. Code: the paper itself prints https://github.com/hustvl/VAD (seen in the raw markdown, position 13), so code_available=YES. Tags are assigned mechanically from the fixed corpus vocabulary by counting the work's own title and text ('representation;planning;end-to-end;safety'), not from any field placement. Conversion QC: RAW_MD_READY. decision_relevance=LOW: this batch exists to make the census readable locally, and it makes no claim about whether the work is decision-relevant. Census-depth record: no deep read, no field placement, no novelty or gap verdict. EVIDENCE_LEVEL=DOCUMENT_VERIFIED"),
    "P0059": dict(short="DiffusionDrive",
                  title="DiffusionDrive: Truncated Diffusion Model for End-to-End Autonomous Driving",
                  year="2025", first_author="Liao, Bencheng", venue="CVPR 2025",
                  arxiv_id="", doi="NONE",
                  official_url="https://openaccess.thecvf.com/content/CVPR2025/html/Liao_DiffusionDrive_Truncated_Diffusion_Model_for_End-to-End_Autonomous_Driving_CVPR_2025_paper.html",
                  code_available="UNKNOWN", official_code_url="",
                  tags="end-to-end;diffusion;planning;evaluation", hyp="GENERAL", rel="LOW", reviewed="2026-09-14",
                  note="Phase-A Census Round 1 text-layer batch (CORPUS_BATCH=census1), record created so that this work placed by landscape/CENSUS_PHASE_A_ROUND1.md has a local text layer. Official title, first author and date come from the official landing page (https://openaccess.thecvf.com/content/CVPR2025/html/Liao_DiffusionDrive_Truncated_Diffusion_Model_for_End-to-End_Autonomous_Driving_CVPR_2025_paper.html), copied from manifests/batch_census1_identity.json; front-page verification of the stored PDF returned DOCUMENT_VERIFIED. Canonical source: CVPR2025_camera_ready. No repository URL is printed in the extracted text; absence of a printed URL is not evidence that no code exists, so code_available stays UNKNOWN. Tags are assigned mechanically from the fixed corpus vocabulary by counting the work's own title and text ('end-to-end;diffusion;planning;evaluation'), not from any field placement. Conversion QC: RAW_MD_READY. decision_relevance=LOW: this batch exists to make the census readable locally, and it makes no claim about whether the work is decision-relevant. Census-depth record: no deep read, no field placement, no novelty or gap verdict. EVIDENCE_LEVEL=DOCUMENT_VERIFIED"),
    "P0060": dict(short="DrivoR",
                  title="Driving on Registers",
                  year="2026", first_author="Kirby, Ellington", venue="CVPR 2026",
                  arxiv_id="", doi="NONE",
                  official_url="https://openaccess.thecvf.com/content/CVPR2026/html/Kirby_Driving_on_Registers_CVPR_2026_paper.html",
                  code_available="UNKNOWN", official_code_url="",
                  tags="end-to-end;planning;benchmark;representation", hyp="GENERAL", rel="LOW", reviewed="2026-09-14",
                  note="Phase-A Census Round 1 text-layer batch (CORPUS_BATCH=census1), record created so that this work placed by landscape/CENSUS_PHASE_A_ROUND1.md has a local text layer. Official title, first author and date come from the official landing page (https://openaccess.thecvf.com/content/CVPR2026/html/Kirby_Driving_on_Registers_CVPR_2026_paper.html), copied from manifests/batch_census1_identity.json; front-page verification of the stored PDF returned DOCUMENT_VERIFIED. Canonical source: CVPR2026_camera_ready. No repository URL is printed in the extracted text; absence of a printed URL is not evidence that no code exists, so code_available stays UNKNOWN. Tags are assigned mechanically from the fixed corpus vocabulary by counting the work's own title and text ('end-to-end;planning;benchmark;representation'), not from any field placement. Conversion QC: RAW_MD_READY. decision_relevance=LOW: this batch exists to make the census readable locally, and it makes no claim about whether the work is decision-relevant. Census-depth record: no deep read, no field placement, no novelty or gap verdict. EVIDENCE_LEVEL=DOCUMENT_VERIFIED"),
    # --- Phase C.5 Core-WAM batch ---
    "P0061": dict(short="SeerDrive",
                  title="Future-Aware End-to-End Driving: Bidirectional Modeling of Trajectory Planning and Scene Evolution",
                  year="2025", first_author="Zhang, Bozhou", venue="NeurIPS 2025",
                  arxiv_id="2510.11092", doi="NONE",
                  official_url="https://arxiv.org/abs/2510.11092",
                  code_available="YES", official_code_url="https://github.com/LogosRoboticsGroup/SeerDrive",
                  tags="world-model;planning;end-to-end;representation", hyp="GENERAL", rel="LOW", reviewed="2026-09-14",
                  note="Phase C.5 Core-WAM batch. Official arXiv identity and NeurIPS 2025 status verified; canonical source arXiv_v1. Official code repository live-checked and pinned in CODE_REPO_MANIFEST.csv. Raw Markdown conversion/QC is infrastructure-only; no scientific synthesis."),
    "P0062": dict(short="Metis",
                  title="Metis: A Generalizable and Efficient World-Action Model for Autonomous Driving and Urban Navigation",
                  year="2026", first_author="Li, Jingyu", venue="arXiv preprint",
                  arxiv_id="2606.15869", doi="NONE",
                  official_url="https://arxiv.org/abs/2606.15869",
                  code_available="YES", official_code_url="https://github.com/LogosRoboticsGroup/Metis",
                  tags="world-model;planning;end-to-end", hyp="GENERAL", rel="LOW", reviewed="2026-09-14",
                  note="Phase C.5 Core-WAM batch. Official arXiv identity verified; canonical source arXiv_v1. Official repository exists but contains project assets/README only at the checked commit; implementation and checkpoints are not released. Raw Markdown conversion/QC is infrastructure-only; no scientific synthesis."),
    "P0063": dict(short="DynFlowDrive",
                  title="DynFlowDrive: Flow-Based Dynamic World Modeling for Autonomous Driving",
                  year="2026", first_author="Liu, Xiaolu", venue="arXiv preprint",
                  arxiv_id="2603.19675", doi="NONE",
                  official_url="https://arxiv.org/abs/2603.19675",
                  code_available="YES", official_code_url="https://github.com/xiaolul2/DynFlowDrive",
                  tags="world-model;planning;end-to-end", hyp="GENERAL", rel="LOW", reviewed="2026-09-14",
                  note="Phase C.5 Core-WAM batch. Official arXiv v2 identity verified; canonical source arXiv_v2. Official repository exists but contains README only at the checked commit and states code will be released once accepted; implementation is unreleased. Raw Markdown conversion/QC is infrastructure-only; no scientific synthesis."),
    "P0064": dict(short="Discrete-WAM",
                  title="Discrete-WAM: Unified Discrete Vision-Action Token Editing for World-Policy Learning",
                  year="2026", first_author="Yao, Ziyang", venue="arXiv preprint",
                  arxiv_id="2606.05645", doi="NONE",
                  official_url="https://arxiv.org/abs/2606.05645",
                  code_available="UNKNOWN", official_code_url="",
                  tags="world-model;planning;end-to-end;representation", hyp="GENERAL", rel="LOW", reviewed="2026-09-14",
                  note="Phase C.5 Core-WAM batch. Official arXiv v2 identity verified; canonical source arXiv_v2. No official code repository was found in the paper record or live GitHub search at the check date. Raw Markdown conversion/QC is infrastructure-only; no scientific synthesis."),
    "P0065": dict(short="GraphWorld",
                  title="GraphWorld: Long-Horizon Planning with World Models for End-to-End Autonomous Driving",
                  year="2026", first_author="Song, Ziying", venue="arXiv preprint",
                  arxiv_id="2606.16274", doi="NONE",
                  official_url="https://arxiv.org/abs/2606.16274",
                  code_available="UNKNOWN", official_code_url="",
                  tags="world-model;planning;end-to-end;interactive", hyp="GENERAL", rel="LOW", reviewed="2026-09-14",
                  note="Phase C.5 Core-WAM batch. Official arXiv identity verified; canonical source arXiv_v1. No official code repository was found in the paper record or live GitHub search at the check date. Raw Markdown conversion/QC is infrastructure-only; no scientific synthesis."),
}


# P0021-P0034 come from the Phase-A Census Round 2 support batch (census2).
ORDER = [f"P{i:04d}" for i in range(1, 66)]


def load_all(name):
    """Merge every batch ledger for one artifact, e.g. load_all("download_results").

    The CSV is a single corpus-wide index, so it must never lose another
    batch's rows: every manifests/batch_*_<name>.json is read and later batches
    win per paper_id. Batch 0A and Round 2 therefore coexist, and a targeted
    re-run cannot truncate the other batch's provenance.
    """
    merged = {}
    suffix = f"_{name}.json"
    for fn in sorted(os.listdir(MAN)):
        if fn.startswith("batch_") and fn.endswith(suffix):
            with open(os.path.join(MAN, fn), encoding="utf-8") as f:
                for r in json.load(f):
                    merged[r["paper_id"]] = r
    return list(merged.values())


def main():
    dl = {r["paper_id"]: r for r in load_all("download_results")}
    fp = {r["paper_id"]: r for r in load_all("frontpage_verification")}
    raw = {r["paper_id"]: r for r in load_all("rawmd_results")}

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

        # Keep the legacy schema column blank. The former paper-card layer is retired;
        # current scientific synthesis lives in deep analyses and source/code audits.
        card_rel = ""
        notes += " NO_CARD: legacy github_card_path field is blank because the paper-card layer is retired."

        rows.append([
            pid, m["title"], m["year"], m["first_author"], m["venue"],
            m["arxiv_id"], m["doi"], m["official_url"],
            d.get("canonical_url") or "", d.get("source_version", "UNKNOWN"),
            d.get("sha256") if downloaded else "",
            (r.get("raw_md_sha256") if raw_ok else "UNKNOWN"),
            pdf_rel, raw_rel, lib,
            card_rel,

            m["code_available"], m["official_code_url"], m.get("code_repo_id", ""),
            reading, m["tags"], m["hyp"], m["rel"], m.get("reviewed", DATE), notes,
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
