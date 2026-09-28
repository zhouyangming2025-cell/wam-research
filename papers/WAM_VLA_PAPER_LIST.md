# WAM + VLA 论文清单

更新时间：2026-09-28

定位：本文件记录扩展的 WAM + VLA / autonomous-driving VLA 原文资产。该集合与现有 canonical-12 planning-centric WAM 主线分开维护；本轮不修改 canonical-12，也不代表已完成论文分析或技术路线分类。

## 已核验并完成原文 ingest

| Seed name | P-ID | 正式标题 | 年份 | Paper | Code / project | raw_md | ingest 状态 |
|---|---|---|---:|---|---|---|---|
| DriveWorld-VLA | P0068 | DriveWorld-VLA: Unified Latent-Space World Modeling with Vision-Language-Action for Autonomous Driving | 2026 | [arXiv:2602.06521](https://arxiv.org/abs/2602.06521) | [GitHub](https://github.com/liulin815/DriveWorld-VLA) | `papers/raw_md/P0068_DriveWorld-VLA/P0068_DriveWorld-VLA.raw.md` | PASS |
| Uni-World VLA | P0069 | Uni-World VLA: Interleaved World Modeling and Planning for Autonomous Driving | 2026 | [arXiv:2603.27287](https://arxiv.org/abs/2603.27287) | [GitHub](https://github.com/LogosRoboticsGroup/UniWorldVLA) | `papers/raw_md/P0069_UniWorldVLA/P0069_UniWorldVLA.raw.md` | PASS |
| SGDrive | P0070 | SGDrive: Scene-to-Goal Hierarchical World Cognition for Autonomous Driving | 2026 | [arXiv:2601.05640](https://arxiv.org/abs/2601.05640) | [GitHub](https://github.com/LogosRoboticsGroup/SGDrive) | `papers/raw_md/P0070_SGDrive/P0070_SGDrive.raw.md` | PASS |
| FSDrive | P0071 | FutureSightDrive: Thinking Visually with Spatio-Temporal CoT for Autonomous Driving | 2025 | [arXiv:2505.17685](https://arxiv.org/abs/2505.17685) | [GitHub](https://github.com/MIV-XJTU/FSDrive) | `papers/raw_md/P0071_FSDrive/P0071_FSDrive.raw.md` | PASS |
| DriveVLA-W0 | P0072 | DriveVLA-W0: World Models Amplify Data Scaling Law in Autonomous Driving | 2025 | [arXiv:2510.12796](https://arxiv.org/abs/2510.12796) | [GitHub](https://github.com/BraveGroup/DriveVLA-W0) | `papers/raw_md/P0072_DriveVLA-W0/P0072_DriveVLA-W0.raw.md` | PASS |
| CoT4AD | P0073 | CoT4AD: A Vision-Language-Action Model with Explicit Chain-of-Thought Reasoning for Autonomous Driving | 2025 | [arXiv:2511.22532](https://arxiv.org/abs/2511.22532) | Paper states code will be released; no official repository verified | `papers/raw_md/P0073_CoT4AD/P0073_CoT4AD.raw.md` | PASS |
| WAM-Flow | P0074 | WAM-Flow: Parallel Coarse-to-Fine Motion Planning via Discrete Flow Matching for Autonomous Driving | 2025 | [arXiv:2512.06112](https://arxiv.org/abs/2512.06112) | [GitHub](https://github.com/fudan-generative-vision/WAM-Flow) | `papers/raw_md/P0074_WAM-Flow/P0074_WAM-Flow.raw.md` | PASS |
| ExploreVLA | P0075 | ExploreVLA: Dense World Modeling and Exploration for End-to-End Autonomous Driving | 2026 | [arXiv:2604.02714](https://arxiv.org/abs/2604.02714) | [Project page](https://zihaosheng.github.io/ExploreVLA/) | `papers/raw_md/P0075_ExploreVLA/P0075_ExploreVLA.raw.md` | PASS |
| UniDriveVLA | P0076 | UniDriveVLA: Unifying Understanding, Perception, and Action Planning for Autonomous Driving | 2026 | [arXiv:2604.02190](https://arxiv.org/abs/2604.02190) | [GitHub](https://github.com/xiaomi-research/unidrivevla) | `papers/raw_md/P0076_UniDriveVLA/P0076_UniDriveVLA.raw.md` | PASS-WITH-MINOR-PARSE-ISSUES |
| UniDrive-WM | P0077 | UniDrive-WM: Unified Understanding, Planning and Generation World Model for Autonomous Driving | 2026 | [arXiv:2601.04453](https://arxiv.org/abs/2601.04453) | [Project page](https://unidrive-wm.github.io/UniDrive-WM/)；paper says code will be released | `papers/raw_md/P0077_UniDrive-WM/P0077_UniDrive-WM.raw.md` | PASS-WITH-MINOR-PARSE-ISSUES |

## 处理说明

- P0068–P0077 属于扩展 corpus，不属于 canonical-12。
- PDF 原文保存在本机 `papers/pdf/`，按仓库 `.gitignore` 不进入 Git；来源、页数、SHA256 和解析证据见 `audits/ingest/WAM_VLA_SOURCE_INGEST_20260928.md`。
- MinerU 基础 QC 对 P0076 报告缺少 Abstract heading，但 PDF 和 raw Markdown 均含 Abstract 正文；对 P0077 报告缺少 References heading，但 raw Markdown 含完整编号 bibliography，且已用 `txt` 方法独立重试确认。两者均保留轻微解析问题状态，不手工改写原文。
