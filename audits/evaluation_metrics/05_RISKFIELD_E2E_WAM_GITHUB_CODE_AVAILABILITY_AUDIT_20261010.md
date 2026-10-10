# 2023–2026 风险场 Python 开源项目：GitHub 专项普查（2026-10-10 第三版）

> **目的**：回应“把风险场 Python 开源项目最近几年尽可能找全”的要求，且保留用户先前明确的核心筛选标准：**优先风险场已经集成进端到端驾驶/WAM/学习式 ego 驾驶策略的项目**。传统、混合规划与纯场库单列，不与核心数量混算。  
> **证据等级：STATIC-SOURCE-VERIFIED / NOT-REPRODUCED**。本次横向检索 Google/Bing GitHub 搜索 + GitHub repository/代码检索，并读取仓库文件树及关键 Python 源码；**未安装、跑测试、加载权重或复现论文数字**。  
> 研究分支不变：`codex/evaluation-metrics-baseline-audit-20261010`，`main` 不改。相连文献审计：[04 风险场 × E2E/WAM 评价专项](04_RISKFIELD_E2E_WAM_METRIC_SPECIAL_STUDY_20261010.md)。  
> **注意**：本文 2023–2026 指重点检索的论文/代码活动年代，不代表每个 GitHub 仓库都核实为在 2023 年之后创建；不能保证穷尽未索引、私有、改名或后续发布项目。本表“有代码”含静态源码，不等于已跑通；项目简介宣称的性能未被本轮独立确认。

## A. 严格核心：Python 源码同时覆盖风险场 + ego 学习式驾驶策略 / 端到端模型

| 优先级 | GitHub 项目 | 具体 Python 证据：场如何进入策略 | 研究定位/限制 |
|---|---|---|---|
| **A0** | **[tier4/METEOR](https://github.com/tier4/METEOR)**，2026；固定 `main@dc193a81` | [场 GT](https://github.com/tier4/METEOR/blob/dc193a81e9959de57b751e269127ae9b67e3f300/bevlane/risk_field.py) 以各向异性高斯+占用生成 BEV risk；[模型](https://github.com/tier4/METEOR/blob/dc193a81e9959de57b751e269127ae9b67e3f300/bevlane/model.py) 的 `risk_head` 预测风险；[guardrail](https://github.com/tier4/METEOR/blob/dc193a81e9959de57b751e269127ae9b67e3f300/bevlane/guardrail.py) `risk_pick` 计算 `confidence - λ*mean_risk(path)`；含训练、ONNX/PyTorch 权重发布说明 | **真正多相机 E2E 表征+风险监督代码**。但 `demo_rgbd_bev.py` 中 risk_pick 得到的选择之后又被不依赖 risk 的 `_k2` 覆盖；在该演示路径风险是否改变最终动作有**明确源码疑点**，其他推理路径未全面核查；不是 NAVSIM 模型 |
| **A0** | **[SAS-HKU/SAFE-AD](https://github.com/SAS-HKU/SAFE-AD)**，2026；`main@f8b53b2f` | [field backend](https://github.com/SAS-HKU/SAFE-AD/blob/main/rl/risk/field_backend.py) 数值 PDE/PINN 可切换；[HighwayEnv wrapper](https://github.com/SAS-HKU/SAFE-AD/blob/main/rl/env/highwayenv_drift_wrapper.py) 将场注入 reward/可选状态；[MetaDrive wrapper](https://github.com/SAS-HKU/SAFE-AD/blob/main/rl/env/metadrive_drift_wrapper.py) 增添 8 维场特征/奖励成本；[训练](https://github.com/SAS-HKU/SAFE-AD/blob/main/rl/train_highwayenv_social_sb3.py) 涉及 PPO/SAC | **真实“空间场→学习策略 observation/reward”接入，可与 WAM 指标/训练思想对照**。作者 README 自标 partial release；属于状态/特征 RL，**不是 NAVSIM 图像→规划的现代 WAM**。仓库含大体量复制/内嵌仿真器，独立代码需从 `rl/` 等筛选 |
| **A0** | **[lumen2023/SafeRL-metaDrive-SEU-AMC](https://github.com/lumen2023/SafeRL-metaDrive-SEU-AMC)**，2026 前后版本；`main@e1550056` | [风险计算器](https://github.com/lumen2023/SafeRL-metaDrive-SEU-AMC/blob/main/safe_metadrive_adapter/risk_field.py)、[reward](https://github.com/lumen2023/SafeRL-metaDrive-SEU-AMC/blob/main/safe_metadrive_adapter/reward.py) 的 `aggregate_risk_field_reward_penalty`、[config](https://github.com/lumen2023/SafeRL-metaDrive-SEU-AMC/blob/main/safe_metadrive_adapter/config.py) 默认 `use_risk_field_reward=True`；[训练](https://github.com/lumen2023/SafeRL-metaDrive-SEU-AMC/blob/main/train_sacl.py) / PPO-Lag / SAC-Lag；[风险 cost 语义审计](https://github.com/lumen2023/SafeRL-metaDrive-SEU-AMC/blob/main/docs/risk_field/RISK_FIELD_TRAINING_SEMANTICS.md) | **连续风险场真正接入安全 RL 训练 reward，cost 可选**；对“密集安全信号与 episode cost_limit 单位冲突”的讨论尤为有用。非 WAM，训练/性能结果未独立核 |
| **A1 / WAM** | **[lumen2023/R2D_SEU_Test](https://github.com/lumen2023/R2D_SEU_Test)**，2026；`main@db2c46b9` | [R2-Dreamer/DreamerV3](https://github.com/lumen2023/R2D_SEU_Test/blob/main/README.md) + [MetaDrive RiskFieldCalculator](https://github.com/lumen2023/R2D_SEU_Test/blob/main/r2dreamer_metadrive/risk_field.py) + [SafeMetaDrive cost wrapper](https://github.com/lumen2023/R2D_SEU_Test/blob/main/r2dreamer_metadrive/safe_env.py)。`cost_function` 在 `use_risk_field_cost=True` 时计算场风险、转事件等价 cost、组合进 episode cost；[环境 wrapper](https://github.com/lumen2023/R2D_SEU_Test/blob/main/r2dreamer_metadrive/env.py) 供 Dreamer 训练使用 | **六个核心项目中与 world model/RSSM 最近**，但场主要作为**环境侧可选 cost/记录**，并不等于风险已经送入 world model latent；`use_risk_field_cost=False` 时返回零风险日志，仓库某些现有 eval JSON 中风险均为零。**必须明确启用配置后再判定有效实验**；和 SafeRL-metaDrive 同一维护者，非独立研究复现 |
| **A1** | **[OscarHuangWind/Safe-Human-in-the-Loop-RL](https://github.com/OscarHuangWind/Safe-Human-in-the-Loop-RL)**，2024 发表；`master@d6c1fd21` | [Frenet 动态势场](https://github.com/OscarHuangWind/Safe-Human-in-the-Loop-RL/blob/master/dynamic_potential_field.py) `FDPF.getIntensityAt`; [控制权仲裁](https://github.com/OscarHuangWind/Safe-Human-in-the-Loop-RL/blob/master/authority_allocation.py) 比较 RL/human 动作预测后的 DPF 变化，并生成 shared-control authority；[DRL policy](https://github.com/OscarHuangWind/Safe-Human-in-the-Loop-RL/blob/master/drl_agent.py) | 已证明真实源码连接到 RL 决策系统；但势场用于**人机共享控制权**，不是 WAM 对多条候选轨迹选优；SMARTS 仿真 |
| **A1 / 研究原型** | **[SetasAditya/material-aware-grl-snam](https://github.com/SetasAditya/material-aware-grl-snam)**，2026 仓库内容；`main@10b4506e` | [风险场构造器](https://github.com/SetasAditya/material-aware-grl-snam/blob/main/full_code/exp-highway-env/risk_field.py) `RiskFieldConstructor`；[highway-env 策略观察构造](https://github.com/SetasAditya/material-aware-grl-snam/blob/main/full_code/exp-highway-env/env_wrapper.py) 把 field 转成 `risk_patch` 与 `rollout_patch`，并接 Stage2 train/eval 代码 | 属于 HighwayEnv 学习式导航/风险场输入原型，不是 NAVSIM/WAM；`env_wrapper` 自称 pure observer，不是完整 Gym wrapper，需逐训练脚本核实 Stage2 实验实际所用路径；不能把本仓库含其他仿真器源码当独立贡献 |

**A 类当前找到 6 个去重 GitHub 仓库；不表示全领域只有 6 个。** 其中真正**多相机 E2E 模型 + 风险空间 head**的可核实例子以 METEOR 最明确；真正 WAM/RSSM 基线工程以 R2D 最贴近但 risk cost 是可选环境侧功能；其余主要 RL 代理/共享控制/Stage2 特征。这种机制差异不能只凭“risk field + Python”忽略。

## B. Python 风险场 / 风险地图源码真实存在，但不是 E2E/WAM 直接开源基线

| 仓库 | Python 实现核查 | 为什么不列入 A |
|---|---|---|
| [PeterWANGHK/Benchmark-RiskField](https://github.com/PeterWANGHK/Benchmark-RiskField) | [risk_field_metrics.py](https://github.com/PeterWANGHK/Benchmark-RiskField/blob/main/metrics_evaluation/risk_field_metrics.py)、[behavioral_alignment_metrics.py](https://github.com/PeterWANGHK/Benchmark-RiskField/blob/main/metrics_evaluation/behavioral_alignment_metrics.py)、[unified_metrics_integration.py](https://github.com/PeterWANGHK/Benchmark-RiskField/blob/main/metrics_evaluation/unified_metrics_integration.py)；GVF/EDRF/APF/ADA、场结构/驾驶行为一致性等指标 | 场本身评价与传统交互模型，**没有核实学习式 ego E2E 规划骨干与场的集成**；不是官方 NAVSIM 指标。代码研究价值高 |
| [SAS-HKU/DRIFT](https://github.com/SAS-HKU/DRIFT) | [src/pde_solver.py](https://github.com/SAS-HKU/DRIFT/blob/main/src/pde_solver.py) PDE 高斯车辆源、遮挡源、汇入源及可视化/测试 | 风险传播核心库，**不是 2026 DRiF 端到端论文的官方实现**；在主分支未见 solver import 的 `config.py`，独立运行有疑问 |
| [SAS-HKU/DREAM](https://github.com/SAS-HKU/DREAM) | [PDE 场](https://github.com/SAS-HKU/DREAM/blob/main/src/dream_limo/dream_limo/core/risk_field.py)、[物理安全指标](https://github.com/SAS-HKU/DREAM/blob/main/src/Carla/physical_safety_metrics.py)、[paired evaluation](https://github.com/SAS-HKU/DREAM/blob/main/src/evaluation/README.md) | 风险场 + 传统/混合 MPC-CBF 安全规划，不是现代学习式 E2E/WAM 模型；尽管有测试和 CARLA |
| [gisgrid/RESPOND](https://github.com/gisgrid/RESPOND) | [risk_torch.py](https://github.com/gisgrid/RESPOND/blob/main/respond/risk_pattern/risk_torch.py)、[risk_calculator.py](https://github.com/gisgrid/RESPOND/blob/main/respond/risk_pattern/risk_calculator.py)；Driver Risk Field 与 LLM/HighD 驾驶代理 | 通过风险模式推理和 agent 决策，不是 NAVSIM/WAM sensor→ego planner；可借鉴 Torch 场计算 |
| [henryhcliu/udmc_carla](https://github.com/henryhcliu/udmc_carla) | Python/CasADi CARLA 统一优化框架，引入 APF 交通规则/动态规划成本 | 传统优化决策/控制，不是学习式 E2E 网络 |
| [CGoodin/nature-lite](https://github.com/CGoodin/nature-lite) | [potential_field.py](https://github.com/CGoodin/nature-lite/blob/main/src/autonomy/planning/potential_field.py)；NumPy 独立端到端**软件栈**的 APF path planner | “end-to-end stack”仅指传感器→规划→控制的传统模块流水线，**不是端到端可学习策略** |
| [wzjoriv/Larp](https://github.com/wzjoriv/Larp) | `larp/field`、risk/potential fields、quadtree、轨迹 SQP 等 Python 组件 | 通用地面/UAM 路线规划库，不是 E2E 学习驾驶 |
| [benmagnifico/K-Risk](https://github.com/benmagnifico/K-Risk) | Python 各交通数据集处理、危险驾驶事件抽取与风险标注脚本 | 主要是场景筛选/风险事件数据，不是风险场 E2E 规划 |
| [hb-datag/xfc-controller](https://github.com/hb-datag/xfc-controller) | `risk_field.py` 与 CasADi/Fuzzy MPC 控制 Python | 有风险场计算与传统控制器，非 E2E 学习；论文对应关系待核 |

另一些相关资源不计入 A/B：`SH-Tan/AV_risk_model` 主体为 MATLAB/C++（不是 Python 实现）；`CORE-SNU/DR-Risk-Map` README 虽写 Python，但实验及主要脚本是 MATLAB，按源文件决定；`Makabaka0000/4WIS_Vehicle_Trajectory_planning` 当前文件树 Python 数为零；`CVC-Lab/GRL-SNAM` 面向通用移动机器人不是驾驶数据的直接 risk-field+WAM 贡献，不能直接代替上方实验分支。

## C. 名字近似却非“空间/时空风险场 + ego E2E/WAM”集成

| 项目 | 真实状态 | 排除或次级用途 |
|---|---|---|
| [YQ-097/RiskDiffuser](https://github.com/YQ-097/RiskDiffuser)（2026） | **有 43 个 .py 文件**：nuPlan 扩散 planner、`riskdiffuser/model/risknet.py`、训练、风险教师与仿真 runner。RiskAssessmentHead 输出 **单个场景级 `risk_score`**（加 TTC/距离代理），属于**连续风险条件化** | **有完整学习式规划和风险条件化代码，但不是二维/时空 RiskField map**；值得作为近邻对照，不能混数为风险场 |
| [MoMingQimio/GA2AD](https://github.com/MoMingQimio/GA2AD) | SUMO adversarial background vehicle RL；`sumo_env.py:risk_assessment` 使用安全代理 SSM 转分级风险概率 | 主要是**背景车对抗场景生成**，不是 ego E2E 规划的空间风险场 |
| [TRI-ML/RAP](https://github.com/TRI-ML/RAP)（2022 原论文） | PyTorch 风险偏置预测 + MPC planner + 完整 eval，风险属于风险敏感场景预测与 planner cost | 邻域重要但不是显式 BEV 风险场；且正式年代更早 |
| [wenqing-2021/Structure_Road_Motion_Planning](https://github.com/wenqing-2021/Structure_Road_Motion_Planning) | Python PPO/RL+CommonRoad，风险可达集实现核心是 `risk_field.cpp/.h` | Python 策略 + C++ 风险场的**混合语言**，不满足“Python 风险场函数”严格口径；可做技术对照 |
| [Basar-mte/Paper-recreate--He-et-al.](https://github.com/Basar-mte/Paper-recreate--He-et-al.) | Python 高斯场场景复杂度 + adaptive reward patch | 应用领域是**机器人拥挤人群导航**，非自动驾驶 E2E/WAM |

## D. 直接相关但核心模型/风险场官方代码尚未核实开放

- [FlowDrive（2025）](https://github.com/AstrixDrive/FlowDrive)：项目存在但根文件树仅 README/LICENSE/docs/assets **6 个文件**，暂无 Python 训练/规划 risk-field 核心源码；**placeholder**。
- [READ（2026）](https://arxiv.org/abs/2609.12371)：高斯可学习时空风险场 + NAVSIM + E2E/VLA，多架构；**未发现核验通过的作者官方 GitHub Python 实现**。
- [DRiF（2026）](https://arxiv.org/abs/2609.10377)：Bench2Drive 数据驱动动态风险场；**未确认官方实现**。特别注意 **DRiF != DRIFT**。
- [RiskMM（2025–2026）](https://arxiv.org/abs/2508.07686)：协同风险地图+学习规划，**未确认公开的官方完整源码**。
- [FusionAssurance（2024）](https://arxiv.org/abs/2405.00316)：Potential Field + MPC 安全层辅助 E2E，**未确认作者官方完整实现**。
- [FARPlan](https://github.com/WUTAD-Wjy/FARPlan)：当前 GitHub 文件树仅 LICENSE/README，不作为代码已开源。
- [RiskMap（2024）](https://arxiv.org/abs/2406.04451) 作者过去的 Velocity-Field 链接当前 GitHub 访问 404，不能计入可用代码。

## E. 本轮检索口径、遗漏风险和核验重点

- 组合关键词：`risk field`、`potential field`、`Gaussian risk field`、`risk map`、`energy flow field`、`risk-aware reinforcement learning`、`risk_field.py`、`BEV`、`MetaDrive`、`highway-env`、`NAVSIM`、`Bench2Drive`、`world model` 等；从论文页/正式代码链接反查 GitHub，又从仓库 README/具体 Python 文件顺藤摸瓜。
- 静态证据标注：**具体 Python 文件可读**、**策略调用路径可见**、**是否可选开关/默认值**、**模型/benchmark 类型**、**代码完整度**。只包含场代码或声称“code coming soon”不累计到 A。
- **未做到的项目**：GitHub 代码搜索索引不能覆盖私有、近期未索引和嵌套大仓库；未做平台级穷尽扫描，也未检查所有 2023–2026 论文作者列表；因此只能说**现阶段的高置信候选集合**，不能说“全领域所有已找全”。大量同名别名和 fork 需要审计来源；同一团队的多个仓库不能当成跨机构独立复现。
- 研发价值排序：**(1) R2D 的 WAM/RSSM 环境侧 cost**；**(2) METEOR 真正从 BEV 预测 risk map 并对候选轨迹评分**；**(3) SAFE-AD 场时序传播 + 可切换 numerical/PINN + policy observation/reward**；**(4) SafeRL-metaDrive 密集风险 cost/reward 的单位冲突与可选组合**。
- 关键未决问题：R2D 在真实训练配置是否开风险？METEOR 风险排序是否被最终规则覆盖？SAFE-AD 的 PINN 代理是否提供足够稳定实时评估？SafeRL 源码中的 dense cost 是否在官方 cost_limit 下带来 overconservatism？这些都需要实际运行，不可从 README 自证。

**第三版结论**：发现 **A类6个、B类9个、C类5个**经 GitHub 文件树/源码核实的不同用途仓库线索（总计20个，不代表20篇独立论文），加若干论文/项目主页未完整开源项。A 类中真正进入现代多相机 E2E 的以 METEOR 最直接；贴近世界模型工程的是 R2D，但它的场是可选环境 cost，不能等同在 WAM 内实现了风险预测。**目前尚未核实到 READ、DRiF 或 FlowDrive 的官方完整训练/推理代码。**
