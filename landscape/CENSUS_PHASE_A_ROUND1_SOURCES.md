# Phase-A Census Round 1 — Source Register

Last updated: 2026-09-14

Purpose: auditable discovery/source register for `CENSUS_PHASE_A_ROUND1.md`. This file records primary or official sources used for Round-1 placement. It is not a bibliography for final publication and does not replace canonical PDF verification during deep read.

Source priority during census:

```text
venue open-access / proceedings page
> official arXiv
> official project page / official repository
> survey navigation source
```

## Surveys / navigation

- Tu et al., **The Role of World Models in Shaping Autonomous Driving: A Comprehensive Survey** — Frontiers of Computer Science, 2026: https://journal.hep.com.cn/fcs/EN/10.1007/s11704-026-60102-1
- **Planning-Oriented End-to-End Autonomous Driving: Architectures, Evaluation, and Emerging Paradigms**, arXiv:2608.20111: https://arxiv.org/abs/2608.20111
- **World Models for Autonomous Driving: An Initial Survey**, IEEE T-IV 2024: https://ieeexplore.ieee.org/document/10522953/

## Visual / video WM

- GAIA-1 — https://arxiv.org/abs/2309.17080
- DriveDreamer — https://arxiv.org/abs/2309.09777 ; project: https://drivedreamer.github.io/
- DriveDreamer-2 — https://arxiv.org/abs/2403.06845 ; AAAI: https://ojs.aaai.org/index.php/AAAI/article/view/33130
- Drive-WM — project: https://drive-wm.github.io/ ; code: https://github.com/BraveGroup/Drive-WM
- Vista — https://arxiv.org/abs/2405.17398 ; official repo: https://github.com/OpenDriveLab/Vista
- Epona — https://arxiv.org/abs/2506.24113 ; ICCV: https://openaccess.thecvf.com/content/ICCV2025/html/Zhang_Epona_Autoregressive_Diffusion_World_Model_for_Autonomous_Driving_ICCV_2025_paper.html
- DrivingGPT — ICCV: https://openaccess.thecvf.com/content/ICCV2025/html/Chen_DrivingGPT_Unifying_Driving_World_Modeling_and_Planning_with_Multi-modal_Autoregressive_ICCV_2025_paper.html
- Policy World Model — https://arxiv.org/abs/2510.19654 ; project: https://6550zhao.github.io/Policy-World-Model/
- WorldDrive — https://arxiv.org/abs/2603.14948 ; official repo: https://github.com/TabGuigui/WorldDrive

## Occupancy / BEV / geometric

- OccWorld — https://arxiv.org/abs/2311.16038 ; official repo: https://github.com/wzzheng/OccWorld
- Drive-OccWorld — AAAI: https://ojs.aaai.org/index.php/AAAI/article/view/33010 ; project: https://drive-occworld.github.io/
- WoTE — ICCV: https://openaccess.thecvf.com/content/ICCV2025/html/Li_End-to-End_Driving_with_Online_Trajectory_Evaluation_via_BEV_World_Model_ICCV_2025_paper.html
- World4Drive — https://arxiv.org/abs/2507.00603 ; ICCV: https://openaccess.thecvf.com/content/ICCV2025/html/Zheng_World4Drive_End-to-End_Autonomous_Driving_via_Intention-aware_Physical_Latent_World_Model_ICCV_2025_paper.html

## Latent / JEPA / WAM

- DriveWorld — https://arxiv.org/abs/2405.04390 ; CVPR: https://openaccess.thecvf.com/content/CVPR2024/html/Min_DriveWorld_4D_Pre-trained_Scene_Understanding_via_World_Models_for_Autonomous_CVPR_2024_paper.html
- LAW — ICLR 2025: https://proceedings.iclr.cc/paper_files/paper/2025/hash/6aa4967920e495e90aeeaa3acf18d019-Abstract-Conference.html ; arXiv:2406.08481
- Drive-JEPA — https://arxiv.org/abs/2601.22032 ; official repo: https://github.com/linhanwang/Drive-JEPA
- WorldRFT — https://arxiv.org/abs/2512.19133 ; AAAI: https://ojs.aaai.org/index.php/AAAI/article/view/38149
- Auto-JEPA — https://arxiv.org/abs/2607.29031
- ReWorld: Learning Better Representations for World Action Models — https://arxiv.org/abs/2606.27504 ; official repo: https://github.com/xiaomi-research/reworld
- WA-JEPA — https://arxiv.org/abs/2608.20974 ; official repo: https://github.com/AFARI-Research/WA-JEPA
- DA-WAM — https://arxiv.org/abs/2608.19085
- DriveLaW — primary text already stored in this repo at `papers/raw_md/P0009_DriveLaW/`; use canonical local PDF/card for exact source metadata.

## Interactive prediction / planning

- M2I — CVPR 2022: https://openaccess.thecvf.com/content/CVPR2022/html/Sun_M2I_From_Factored_Marginal_Trajectory_Prediction_to_Interactive_Prediction_CVPR_2022_paper.html
- GameFormer — ICCV 2023: https://openaccess.thecvf.com/content/ICCV2023/html/Huang_GameFormer_Game-theoretic_Modeling_and_Learning_of_Transformer-based_Interactive_Prediction_and_ICCV_2023_paper.html
- What Truly Matters in Trajectory Prediction for Autonomous Driving? — NeurIPS 2023: https://papers.neurips.cc/paper_files/paper/2023/hash/e197fe307eb3467035f892dc100d570a-Abstract-Conference.html
- BeTop — primary text already stored in this repo at `papers/raw_md/P0004_BeTop/`.
- GraphAD — primary text already stored in this repo at `papers/raw_md/P0003_GraphAD/`.

## Simulation / benchmark

- nuPlan — official: https://nuplan.org/nuplan
- SLEDGE — ECCV: https://www.ecva.net/papers/eccv_2024/papers_ECCV/html/490_ECCV_2024_paper.php ; official repo: https://github.com/autonomousvision/sledge
- NAVSIM — https://arxiv.org/abs/2406.15349 ; NeurIPS: https://proceedings.nips.cc/paper_files/paper/2024/hash/32768f7faf1995026ef9821c696f3404-Abstract-Datasets_and_Benchmarks_Track.html
- Bench2Drive — https://arxiv.org/abs/2406.03877
- HUGSIM — DOI 10.1109/TPAMI.2025.3647952 ; PubMed record: https://pubmed.ncbi.nlm.nih.gov/41442300/
- DriveArena — official repo: https://github.com/PJLab-ADG/DriveArena
- BridgeSim / ReactSim-Bench / CausalDrive / CRAFT — see `state/TARGETED_READING_QUEUE.md`; full-paper verification remains pending under field-reconstruction work.

## Strong non-WM controls

- UniAD / Planning-Oriented Autonomous Driving — CVPR 2023: https://openaccess.thecvf.com/content/CVPR2023/html/Hu_Planning-Oriented_Autonomous_Driving_CVPR_2023_paper.html
- VAD — ICCV 2023: https://openaccess.thecvf.com/content/ICCV2023/html/Jiang_VAD_Vectorized_Scene_Representation_for_Efficient_Autonomous_Driving_ICCV_2023_paper.html
- DiffusionDrive — CVPR 2025: https://openaccess.thecvf.com/content/CVPR2025/html/Liao_DiffusionDrive_Truncated_Diffusion_Model_for_End-to-End_Autonomous_Driving_CVPR_2025_paper.html
- DrivoR / Driving on Registers — CVPR 2026: https://openaccess.thecvf.com/content/CVPR2026/html/Kirby_Driving_on_Registers_CVPR_2026_paper.html

## Existing repo evidence used

Primary/raw paper text already in the Research Brain was used for placement of:

```text
Epona
SafeDrive
GraphAD
BeTop
RiskWorld
Gen-Drive
DriveReward
DriveLaW
TOAD
Sensitivity Shaping
DA-WAM
```

NPPC remains a legacy deep-read/counterexample with no current readable canonical PDF in the corpus. Fine-grained NPPC claims must be reverified if a lawful source becomes available.
