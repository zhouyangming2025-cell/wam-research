# 12 篇论文证据索引

## 使用规则

- `raw paper` 是本任务的主要论文文本层；若公式/图像转换含糊，应回到本地 canonical PDF 核验并记录，但不要凭二手总结补齐。
- `audit` 主要处理源码、版本和 paper/code 边界。
- `deep analysis` 是已有解释，必须晚于独立机制重建读取，以降低锚定偏差。
- 表中没有单篇 audit 不代表缺少论文证据；raw paper 仍可支持 paper-level 分类。

## 第一组：最终人工验收六篇

| ID | Paper | Raw paper | Source/code audit | Secondary deep analysis | 必查边界 |
|---|---|---|---|---|---|
| P0048 | LAW — *Enhancing End-to-End Autonomous Driving with Latent World Model* | `papers/raw_md/P0048_LAW/P0048_LAW.raw.md` | `audits/literature/PHASE_B_WAVE2_INTERFACE_CODE_AUDIT.md` | `papers/deep_analysis/P0048_LAW_DEEP_ANALYSIS_V2.md` | future/world branch 是否只在训练塑形；predicted action 到 world loss 的梯度路径 |
| P0001 | Epona — *Autoregressive Diffusion World Model for Autonomous Driving* | `papers/raw_md/P0001_Epona/P0001_Epona.raw.md` | `audits/literature/PHASE_C5_EPONA_SOURCE_AUDIT.md` | `papers/deep_analysis/P0001_EPONA_DEEP_ANALYSIS_V2.md` | planning mode 与 rollout/user-control mode 分开；shared state 与 action-conditioned future 不要混写 |
| P0009 | DriveLaW — *Unifying Planning and Video Generation in a Latent Driving World* | `papers/raw_md/P0009_DriveLaW/P0009_DriveLaW.raw.md` | `audits/literature/PHASE_C6_DRIVELAW_AUDIT.md` | `papers/deep_analysis/P0009_DRIVELAW_DEEP_ANALYSIS_V2.md` | 在线消费的是生成过程 hidden carrier 还是完整 future video；paper/source 公式与 action-step 差异 |
| P0046 | World4Drive — *End-to-End Autonomous Driving via Intention-aware Physical Latent World Model* | `papers/raw_md/P0046_World4Drive/P0046_World4Drive.raw.md` | `audits/literature/PHASE_C5_WORLD4DRIVE_AUDIT.md` | `papers/deep_analysis/P0046_WORLD4DRIVE_DEEP_ANALYSIS_V2.md` | K 个候选对应的 future latent；selector 的事实模式匹配语义；反事实真实性边界 |
| P0042 | WorldDrive — *Bridging Scene Generation and Planning* | `papers/raw_md/P0042_WorldDrive/P0042_WorldDrive.raw.md` | `audits/literature/PHASE_C5_WORLDDRIVE_AUDIT.md` | `papers/deep_analysis/P0042_WORLDDRIVE_DEEP_ANALYSIS_V2.md` | 预训练表示继承、heavy future teacher、deployed rewarder 与候选排序的阶段关系 |
| P0045 | WoTE — *End-to-End Driving with Online Trajectory Evaluation via BEV World Model* | `papers/raw_md/P0045_WoTE/P0045_WoTE.raw.md` | `audits/literature/PHASE_B_WAVE2_INTERFACE_CODE_AUDIT.md` | `papers/deep_analysis/P0045_WOTE_DEEP_ANALYSIS_V2.md` | candidate-conditioned 多步 future BEV；分解 reward；在线 evaluator 是否进入最终选择 |

## 第二组：维度发现与压力测试六篇

| ID | Paper | Raw paper | Source/code audit | Secondary deep analysis | 必查边界 |
|---|---|---|---|---|---|
| P0061 | SeerDrive — *Future-Aware End-to-End Driving: Bidirectional Modeling of Trajectory Planning and Scene Evolution* | `papers/raw_md/P0061_SeerDrive/P0061_SeerDrive.raw.md` | `audits/literature/PHASE_C5_SEERDRIVE_AUDIT.md`; `audits/research_synthesis/SEERDRIVE_DEEP_AUDIT.md` | `papers/deep_analysis/P0061_SEERDRIVE_DEEP_ANALYSIS_V2.md` | 原论文 iterative world↔planner 与公开 WoTE-integrated code 必须拆分 |
| P0049 | Drive-JEPA — *Video JEPA Meets Multimodal Trajectory Distillation for End-to-End Driving* | `papers/raw_md/P0049_DriveJEPA/P0049_DriveJEPA.raw.md` | `audits/literature/PHASE_C5_DRIVEJEPA_AUDIT.md` | `papers/deep_analysis/P0049_DRIVEJEPA_DEEP_ANALYSIS_V2.md` | predictive pretraining 与 planner 解耦；perception-free / perception-based 部署路径拆分；proposal distillation |
| P0062 | Metis — *A Generalizable and Efficient World-Action Model for Autonomous Driving and Urban Navigation* | `papers/raw_md/P0062_Metis/P0062_Metis.raw.md` | `audits/literature/PHASE_C5_METIS_AUDIT.md` | `papers/deep_analysis/P0062_METIS_DEEP_ANALYSIS_V2.md` | asymmetric attention；future video loss 如何塑造 action expert；部署 action-only；源码不可用 |
| P0063 | DynFlowDrive — *Flow-Based Dynamic World Modeling for Autonomous Driving* | `papers/raw_md/P0063_DynFlowDrive/P0063_DynFlowDrive.raw.md` | `audits/literature/PHASE_C5_DYNFLOWDRIVE_AUDIT.md` | `papers/deep_analysis/P0063_DYNFLOWDRIVE_DEEP_ANALYSIS_V2.md` | world model 训练期给候选标签/score、部署删除；hybrid criterion；flow time 与物理时间 |
| P0064 | Discrete-WAM — *Unified Discrete Vision-Action Token Editing for World-Policy Learning* | `papers/raw_md/P0064_Discrete-WAM/P0064_Discrete-WAM.raw.md` | `audits/literature/PHASE_C5_DISCRETE_WAM_AUDIT.md` | `papers/deep_analysis/P0064_DISCRETE_WAM_DEEP_ANALYSIS_V2.md` | shared world-action token backbone；高层 decision token→action；400 decisions 是监督词表还是在线候选池；源码未识别 |
| P0065 | GraphWorld — *Long-Horizon Planning with World Models for End-to-End Autonomous Driving* | `papers/raw_md/P0065_GraphWorld/P0065_GraphWorld.raw.md` | `audits/literature/PHASE_C5_GRAPHWORLD_AUDIT.md` | `papers/deep_analysis/P0065_GRAPHWORLD_DEEP_ANALYSIS_V2.md` | current world-state refinement 而非显式 future rollout；flow coordinate；多模态 planner/selector 路由源码未验证 |

## 历史与竞争性草案

按以下顺序读，且只在 12 篇独立重建完成后读取：

1. `papers/WAM_SIX_PAPER_UNIFIED_MODULE_AUDIT.md` — 最早的逐论文/逐维度整理，作为失败样本；
2. `papers/WAM_ROUTE_MODULE_ABSTRACTION_SAMPLE.md` — 从论文比较转向功能接口组合的重要转折；
3. `papers/WAM_CORE_MECHANISM_SIGNATURE_V1_PROPOSAL.md` — 双层签名候选，不是 canonical；
4. `papers/WAM_CORE_MECHANISM_SIGNATURE_V1_STRESS_TEST.md` — 12 篇 shadow projection，不是正式结论；
5. `handoff/core_mechanism_12/DRAFTS_TO_ATTACK.md` — 当前已知漏洞和需证伪点。

## 证据完整性现状

```text
12/12 raw paper Markdown present and tracked
12/12 deep analyses present and tracked
official-source implementation unavailable or unidentified:
  Metis / DynFlowDrive / Discrete-WAM / GraphWorld
paper/code version split required:
  SeerDrive
mode split required:
  Epona / Drive-JEPA（至少）
```

源码缺失只限制 code-level 结论，不妨碍 paper-level 机制分类；相应字段必须标记 `SOURCE-UNVERIFIED` 或 `UNKNOWN`。
