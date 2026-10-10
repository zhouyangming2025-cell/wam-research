# 评价指标论文登记账本｜Wave 1（2026-10-10）

> **阶段性质：有来源的第一轮发现与分类，不是穷尽性系统综述、不是所有论文的全文精读。**
>
> 审计起点：[`00_REPOSITORY_BASELINE_AUDIT_20261010.md`](00_REPOSITORY_BASELINE_AUDIT_20261010.md)；主仓库 `main@cb05048dfb822e95d44e52dd85b830c750411e2c`。  
> 研究目的：寻找 **以规划质量的评价指标/Benchmark 机制创新为贡献** 的论文，再与传统方法交叉对照。重点不是 WAM 模型“使用哪个 benchmark”。
>
> 状态：`METHOD-READ` = 阅读了可定位方法/实验段落；`PRIMARY-ABSTRACT` = 仅经作者/期刊/会议正式摘要核实身份与主要贡献；`REPO-SOURCE` = 仓库已有原文或证据审计，**不自动意味着本轮逐行精读**；`FOLLOW-UP` = 待补代码、全文或细节。  
> 分类：`B1a` 直接评价量/公式/评分器；`B1b` 评测环境/协议/聚合；`B1p` **运动预测评价**（相邻领域，不能并入自车规划指标总数）；`B1d` 对官方指标的效度/对照研究（不直接提新 benchmark）；`B2` 模型内部训练/候选评分；`B3` 传统评价理论与迁移来源。一个工作可有次级标签，以主贡献归类，**每篇只登记一次**。

## A. 核心：自车规划质量的评分指标/评价器（B1a）

| 论文、原始来源 | 评价对象与具体改变 | 如何验证（本轮能确认的范围） | 证据状态与存量 |
|---|---|---|---|
| **StyleDrive: Towards Driving-Style Aware Benchmarking of End-To-End Autonomous Driving**；AAAI 2026，[期刊/会议 DOI](https://ojs.aaai.org/index.php/AAAI/article/view/42463)、[原文](https://arxiv.org/abs/2506.23982)、[官方代码](https://github.com/AIR-THU/StyleDrive) | NAVSIM v1 基座的风格条件化指标 **SM-PDMS**：TTC 风格阈值、Comfort 阈值比例、与示范进度对应的 EP；还提供风格标注数据集。属于**现有公式/规则微调**路线 | 作者比较模型风格注入收益及新旧指标对模型分数的分散程度；不能把 Std/Range 增大自动等同于人类偏好一致性 | `METHOD-READ`（已有对话核过正文/源码，**尚未在 GitHub ingest**）；`FOLLOW-UP` 需在专题分支固化全文、代码版本及实验验证 |
| **WOD-E2E: Waymo Open Dataset for End-to-End Driving in Challenging Long-tail Scenarios**；CVPR 2026，[CVF 原文](https://openaccess.thecvf.com/content/CVPR2026/html/Xu_WOD-E2E_Waymo_Open_Dataset_for_End-to-End_Driving_in_Challenging_Long-tail_CVPR_2026_paper.html) | 真实长尾场景下的自车轨迹开放环评价，提出 **Rater Feedback Score (RFS)**；围绕人工标注的轨迹偏好判断，区别于纯距离误差 | 原文摘要确认偏好标注、验证集与独立 held-out 测试集；具体 RFS 算法与信度实验还需全文审计 | `PRIMARY-ABSTRACT`、`NOT-INGESTED`；`FOLLOW-UP` |
| **DriveCritic: Towards Context-Aware, Human-Aligned Evaluation for Autonomous Driving with Vision-Language Models**；ICRA 2026（[作者项目页](https://song-jingyu.github.io/DriveCritic/)），[arXiv 正文](https://arxiv.org/html/2510.13108v2) | 发现 EPDMS 在特定复杂驾驶场景与专家偏好不一致；构建成对人类偏好数据，训练 **VLM 轨迹对评价器**。属**学习式评价器**，不只是更换 PDMS 权重 | 方法正文报告人类偏好配对验证，并给出模型偏好匹配结果；本轮核到作者在论文中报告 76% 配对准确率；评测集独立性与人工标注细节待精读 | `METHOD-READ`、`NOT-INGESTED`；`FOLLOW-UP` |
| **DriveJudge: Rethinking Autonomous Driving Evaluation with Vision-Language Models**；2026-06 预印本，[arXiv 正文](https://arxiv.org/html/2606.17362v1) | **VLM 理解场景 + 选择性调用物理规则函数**，不是纯 VLM 打分或统一硬规则；建立驾驶质量分类和轨迹偏好选择两种评价指标测试 | 正文 Sec.3/4/5：33,577 个 2s 窗口来自 10,732 段标注；DQC 使用人类合理性标签与 AUC/AP，TPS 使用成对偏好匹配准确率；作者报告对 EPDMS 的 DQC AUC 优势及对 DriveCritic 的 TPS 准确率优势；局限：未验证闭环效果 | `METHOD-READ`、`NOT-INGESTED`；**未核实正式会议接收**，不得记为顶会论文 |
| **S2O: An Integrated driving decision-making performance evaluation method bridging subjective feeling to objective evaluation**；Accident Analysis & Prevention 2025，[期刊 DOI](https://doi.org/10.1016/j.aap.2025.108026) | 将安全、时间效率、舒适、能耗等客观因素映射到人的主观质量分；传统自动驾驶综合评价与**人类标注拟合**路线，可迁移到 E2E 指标 | 官方摘要：D2E 约 1000 案例、4 万个人工评分；报告评分 MAE 与 SUMO/规划算法验证，**不是 NAVSIM 新 benchmark** | `PRIMARY-ABSTRACT`、`NOT-INGESTED`；`B3` 次级标签，全文/可用数据待审计 |
| **Scalable evaluation methods for autonomous vehicles**；Expert Systems with Applications 2024，[期刊 DOI](https://doi.org/10.1016/j.eswa.2024.123603) | **场景复杂度校正 + 多目标聚合**，增加其他交通参与者受影响的“altruism”评价维度；将场景难度和能力表现同时纳入总分 | 官方摘要介绍仿真与实车测试；指标数学形式、权重法 MEREC 与 MARCOS、有效性需全文审计 | `PRIMARY-ABSTRACT`、`NOT-INGESTED`；`B3` 次级标签，全文获取可能受出版商限制 |
| **Don't Shake the Wheel: Momentum-Aware Planning in End-to-End Autonomous Driving (MomAD)**；**CVPR 2025**，[CVPR 正式论文](https://openaccess.thecvf.com/content/CVPR2025/html/Song_Dont_Shake_the_Wheel_Momentum-Aware_Planning_in_End-to-End_Autonomous_Driving_CVPR_2025_paper.html)、[官方代码](https://github.com/adept-thu/MomAD) | **TPC (Trajectory Prediction Consistency)**：前后两次规划先转换到相同坐标系，仅在实际未来时间的重合区间比较计划轨迹差异；属于**模型论文附带提出的规划时间稳定性新评价维度**，不是改 PDMS，也不是评测方向为主贡献 | Turning-nuScenes 6s：SparseDrive TPC **2.90m** → MomAD **1.93m**，减少 0.97m；同场景 Collision 2.57%→2.31%（**0.26 个百分点，非相对下降 26%**）。还用 nuScenes 和 Bench2Drive 评测。注意 TPC 小不自动等于安全/正确 | `PAPER-EQ6-READ` + `OFFICIAL-CODE-STATIC-READ`，源码 **3s/6s 公开评价函数中没看到按时间重合与 ego 坐标对齐的变换、跨场景重置**； `CRITICAL-IMPLEMENTATION-FOLLOWUP`，须对照实际评测 pipeline 与复算，不能直接拿源码评估跨场景稳定性 |
| **FluidTest / Is Your Trajectory Displacement Safe in Long-tail?**；2026-06 预印本，[arXiv](https://arxiv.org/abs/2606.16313) | 将规划评价重表述为：相对于专家轨迹，规划轨迹是否产生**额外的安全威胁**；采用 32 类语义风险、成对 WebUI 人工标注及三代理反思验证流程；属于**评价任务/风险验证管线**而非简单新标量 PDMS | 摘要报告 WOD-E2E 场景上 Poutine、RAP 轨迹新增威胁比例分别 65%、51%；缺全文方法/可重复标注一致性细节 | `PRIMARY-ABSTRACT`、`NOT-INGESTED`、`FOLLOW-UP`，**不记为正式会议论文** |

**本表扩展为 8 篇是“直接指标/评分器/评价任务”的初始代表样本，**不是 B1a 全领域总数；其中 StyleDrive 与 WOD-E2E 的评价公式路线和 DriveJudge/DriveCritic 的学习评价路线不应混写成同一种机制。

**MomAD/TPC 单独审计提醒**：论文 §4.1 Eq.(6) 明确强调“coordinate transformation + overlapping prediction times + validation-set aggregation”；官方 [3s](https://github.com/adept-thu/MomAD/blob/7d2247605364e1aba8d7ba4e99f57d01fc452f8c/open_loop/projects/mmdet3d_plugin/datasets/evaluation/planning/planning_eval_roboAD.py) 和 [6s](https://github.com/adept-thu/MomAD/blob/7d2247605364e1aba8d7ba4e99f57d01fc452f8c/open_loop/projects/mmdet3d_plugin/datasets/evaluation/planning/planning_eval_roboAD_6s.py) 的 `compute_Consist` 直接用当前轨迹减 `last_final_planning`，后者是循环上一个 **valid sample** 的轨迹，并在首个样本初始化为零；在此实现段中未见根据 timestamp、scene_token、ego pose 进行坐标转换、时间偏移、scene 边界复位。**需要审计上游是否已等价对齐，不能未经验证照搬这段代码或直接断言发表结果错误。** TPC 评价的是规划输出跨时刻一致性，不是车辆 jerk/方向盘振荡的直接测量，也可能偏好坚持错误的旧计划；须和安全、碰撞与正确性指标联合使用。

## B. 评价协议、平台、聚合及情境评测（B1b）

| 论文、来源 | 主要改变与边界 | 现有证据状态 |
|---|---|---|
| **NAVSIM v1**；[仓库原文](../../papers/raw_md/P0032_NAVSIM/P0032_NAVSIM.raw.md) | 非反应式的自车规划质量仿真 + PDMS；本轮指标改造的基础坐标系 | `REPO-SOURCE` |
| **Pseudo-Simulation for Autonomous Driving / NAVSIM v2**；CoRL 2025，[PMLR 正式论文](https://proceedings.mlr.press/v305/cao25a.html)、[官方指标定义](https://github.com/autonomousvision/navsim/blob/main/docs/metrics.md) | EPDMS 增加分项与误罚过滤；通过预先生成扰动后续观察、按与模型行为接近程度加权的两阶段评测，改善与闭环的联系。要区分 **指标定义变化** 与 **pseudo-simulation 协议变化** | `PRIMARY-ABSTRACT` + `OFFICIAL-DOC`；`NOT-INGESTED`，旧比较审计可用 |
| **Bench2Drive**；[仓库原文](../../papers/raw_md/P0033_Bench2Drive/P0033_Bench2Drive.raw.md)、[相关源审计](../literature/PHASE_B_WAVE4_BENCH2DRIVE_HUGSIM_AUDIT.md) | CARLA 反应式闭环 + 场景化短路线、多能力分项评价；不只是调整 Driving Score 权重 | `REPO-SOURCE` |
| **Towards learning-based planning: The nuPlan benchmark for real-world autonomous driving**；2024，[arXiv 原文](https://arxiv.org/abs/2403.04133) | 闭环、挖掘场景分类、规划专用评价等；**区别于**仓库 `P0031` 的 2021 版 `nuPlan: A closed-loop ML-based planning benchmark...`，不能当作同一篇原文已收录 | `PRIMARY-ABSTRACT`、`NOT-INGESTED`（新版文章） |
| **ReactSim-Bench: Benchmarking Reactive Behavior World Model Simulation in Autonomous Driving**；[仓库原文](../../papers/raw_md/P0014_ReactSimBench/P0014_ReactSimBench.raw.md)、[审计](../literature/PHASE_B_WAVE4_REACTSIMBENCH_AUDIT.md) | 以自车偏离行为测试周边 agent 的反应质量；评价对象主要是**反应式世界模拟器**，不是直接替换自车 PDMS | `REPO-SOURCE`，`B1b-ADJACENT` |
| **nuPlan-R: A Closed-Loop Planning Benchmark for Autonomous Driving via Reactive Multi-Agent Simulation**；IEEE IV 2026，[IEEE DOI](https://doi.org/10.1109/IV66570.2026.11623929)、[arXiv](https://arxiv.org/abs/2511.10403) | 用学习式反应交通代理扩展 nuPlan，并增加两个评价量；首先是**评测环境/交互协议创新**，新增指标细节待核验 | `PRIMARY-ABSTRACT`、`NOT-INGESTED` |
| **Getting SMARTER for Motion Planning in Autonomous Driving Systems**；IEEE IV 2025，[IEEE DOI](https://doi.org/10.1109/IV64158.2025.11097471)、[arXiv](https://arxiv.org/abs/2502.15824) | SMARTS 2.0 模拟器与交互规划评测，提出通用和任务特定指标；主要贡献为平台 + Benchmark | `PRIMARY-ABSTRACT`、`NOT-INGESTED` |
| **When Planners Meet Reality: How Learned, Reactive Traffic Agents Shift nuPlan Benchmarks**；2025 预印本，[arXiv](https://arxiv.org/abs/2510.14677) | 用学习式反应车辆替换 IDM，分析仿真设置改变后的规划器排名变化；主要是**评测有效性/交互假设**，不是新得分公式 | `PRIMARY-ABSTRACT`、`NOT-INGESTED` |

**本表 8 篇，其中已有仓库原文 3 篇；这里的 B1b 不等于 B1a。**

## C. 邻域：运动预测的评价指标（B1p，不计入自车规划 B1a）

| 论文、来源 | 新指标思路 | 适用边界 |
|---|---|---|
| **Measuring What Matters: Scenario-Driven Evaluation for Trajectory Predictors in Autonomous Driving**；AAAI 2026，[官方出版页](https://ojs.aaai.org/index.php/AAAI/article/view/36978) | 按场景 criticality 自适应组合**周围交通参与者轨迹预测**的 accuracy 与 diversity，并比较与下游驾驶性能的关联 | **评价对象是 trajectory predictor（预测器），不是 ego planner。** `PRIMARY-ABSTRACT`，可以借鉴“场景条件化聚合/下游关联验证”，禁止虚计入规划指标创新论文数。 |

## C2. 指标效度对照研究（B1d；与新指标论文分开登记）

| 论文、原始来源 | 贡献性质 | 验证边界 |
|---|---|---|
| **Do Open-Loop Metrics Predict Closed-Loop Driving? A Cross-Benchmark Correlation Study of NAVSIM and Bench2Drive**；2026-04 预印本，[arXiv](https://arxiv.org/abs/2605.00066) | 对已有 NAVSIM 规划分项与 Bench2Drive 闭环 Driving Score 做跨指标相关性研究，并比较一个简化的 3 分项组合；属于**指标效度及指标组合诊断**，不是大规模正式新 benchmark | 从 15 个方法搜集公开结果，仅 **8** 个模型有可配对数据；作者报告简化版与原版相关性均约 Spearman ρ=0.90。**同一小样本选方案并验证，不能推论普适新评分已被证明更优**；`PRIMARY-ABSTRACT`，预印本 |

## D. 模型内评分与传统方法（关联索引，不混算）

- **B2：** [WoTE](../../papers/raw_md/P0045_WoTE/P0045_WoTE.raw.md)、[Hydra-MDP](../../papers/raw_md/P0021_HydraMDP/P0021_HydraMDP.raw.md)、[DriveSuprim](../../papers/raw_md/P0022_DriveSuprim/P0022_DriveSuprim.raw.md)、[DrivoR](../../papers/raw_md/P0060_DrivoR/P0060_DrivoR.raw.md)、[WAM-Flow](../../papers/raw_md/P0074_WAM-Flow/P0074_WAM-Flow.raw.md)、[DriveReward 审计](../literature/PHASE_C6_DRIVEREWARD_AUDIT.md) 等；仅供指标评价侧方法迁移，不充当新 Benchmark 论文。
- **B3：** 前期已检索 Khatib 势场、CHOMP/TrajOpt、Driver's Risk Field、CVaR/风险地图、Maximum Entropy IRL、RSS/CBF/HJ reachability 等；本轮**仅继承用户前期清单，未重新全文核实**。重点研究是否已经进入端到端规划的正式评价标准，而不是重复它们的训练损失用途。

## E. Wave 1 的验证方式线索（只记录论文已有验证，不强加统一标准）

| 研究工作 | 与新指标性质匹配的验证 |
|---|---|
| StyleDrive | 新旧指标对几个风格模型的评分分散程度 + 风格条件模型表现 |
| WOD-E2E / RFS | 独立 rater 的轨迹偏好标签与 held-out 测试集；公式、标注信度待核 |
| DriveCritic | 对候选轨迹的成对偏好一致性 |
| DriveJudge | (i) 行为质量合理性分类 AUC/AP；(ii) 成对轨迹偏好命中率；论文还讨论部署收益和闭环相关性是评价指标验证的不同范式 |
| S2O | 用人类主观评分拟合误差与场景/规划方法实证验证 |
| Scalable evaluation methods | 不同难度场景下的多目标评价、仿真与实车实验 |
| Pseudo-Simulation | 同闭环测试结果的相关性（不是实车安全保证） |

## F. 尚未完成、不得夸大的内容

- **截至 2026-10-10 补录共 18 篇**：B1a 8、B1b 8、B1p 1、B1d 1；不是“全领域只有 18 篇”，也不是“18 篇全文已精读”。B2 与 B3 只列关联线索，**不计在 18 篇之内**。
- 尚未完成逐论文 PDF/代码精读、按关键词和引文链的系统去重、2024–2026 会议全量扫描或 citation saturation 判断。
- Wave 2 已核到 WOD RFS 官方代码计算、DriveCritic 数据拆分、DriveJudge 验证协议；参见 [`03_WAVE2_PRIMARY_SOURCE_METRIC_AUDIT_20261010.md`](03_WAVE2_PRIMARY_SOURCE_METRIC_AUDIT_20261010.md)。尚待补核：StyleDrive 代码版本、WOD 标注信度、DriveCritic 跨标注者一致性、DriveJudge 标注协议与训练开销、S2O/Scalable 公式全文、nuPlan-R 两项新增指标，以及新增 FluidTest 的完整流程。
- Wave 2 可重点寻找：**独立于新增感知模态的低成本 B1a 改造**、**场景复杂度/交互影响校正**、**传统轨迹 risk/cost 到公开 Benchmarks 的适配前例**；在完整检索前不得将其标记为科研空白或创新点。
