# 专项方向：风险场 × 端到端驾驶 / WAM 的规划评价指标（2026-10-10）

> **研究定位：重点跟踪的 Benchmark / 外部评价指标候选方向；先做文献和有效性诊断，不宣布创新点。**  
> 工作分支：`codex/evaluation-metrics-baseline-audit-20261010`；基线：`main@cb05048dfb822e95d44e52dd85b830c750411e2c`。  
> **原有完整复盘已保留于** [source_materials/riskfield_e2e_wam_research_recap_CN.md](source_materials/riskfield_e2e_wam_research_recap_CN.md)；此处**只追踪风险场在端到端 / WAM 上的直接先例及作为最终评价指标的价值**，不复制所有传统方法分析。  
> 本轮检索日期：2026-10-10；完成首轮定向搜寻 + 选定原文/正式摘要检查，不代表系统综述穷尽；“风险场”泛称包含 driving safety/risk field、energy/potential field、risk map、continuous risk cost，不能据同义词自动认定实现等价。  
> 标签：`PRIMARY-FULL` = 核对论文方法与实验正文；`PRIMARY-ABSTRACT` = 核对论文官方摘要；`ADJACENT` = 非典型端到端/WAM 或主要是控制/预测；`METRIC-PRIMARY` = 原创贡献为公开评测指标；`MODEL-PRIMARY` = 风险表示用于模型内部训练/推理。**没有完成代码/实验验证的工作不要标作 REPRODUCED。**

## 1. 本方向究竟要研究什么

**主问题（M1）**：在不改变现有 NAVSIM / Bench2Drive 的数据和主要仿真语义的前提下，能否从经典或学习式风险场构建**有解释力、稳定、能跨多个 E2E/WAM 模型比较的轨迹级风险评价指标**，作为现有 TTC、NC、EP 等分项的补充，或者在合适条件下形成指标计算改进？

**次问题（M2）**：如果指标具有可复查的增量信息，风险场能否再用于候选选择、奖励或 WAM 表示？这属于**模型侧研究**，不计成新 Benchmark 指标论文。用户本轮的正式优先级是 M1，而非抢先把风险场集成进任何模型。

核心数据接口（尚未落地）：

`E(s, τ, A, H) -> {r(t), peak, integral/time-mean, exposure, maybe robustness}`

- `s` = 固定场景地图/ego 初始状态；`τ` = 待评价自车轨迹；`A` = 他车/行人的时序状态**或**明确标示的未来假设；`H` = 时域、采样、车辆占用几何。
- 输出应优先为**连续风险代价、峰值、时间暴露/裕量**；**不能未经概率标定称其为“碰撞概率”**。风险场只定义场值，沿轨迹的采样、车辆 footprint、时间聚合、严重性归一化仍是待设计的评价环节。
- 现有用户脚本 `ly05_eval_riskfield.py` 是**每一帧在记录 ego 位置查询，并对障碍物取 max**，再对窗口汇总；这不是针对任意生成 ego 轨迹的时间一致风险指标，也不是已经接入 NAVSIM 官方 scorer。

## 2. “风险场直接接到 E2E/WAM”已出现明确论文，必须更新新颖性假设

| 论文及来源 | 主要机制（**风险场到底起什么作用**） | 实验/实际评价指标 | 与本专项的关系及状态 |
|---|---|---|---|
| **FlowDrive: Energy Flow Field for End-to-End Autonomous Driving**，2025，[arXiv:2509.14303](https://arxiv.org/abs/2509.14303)、[官方项目](https://github.com/AstrixDrive/FlowDrive) | 规则驱动 risk-potential 与 lane-attraction/energy-flow field 作为 BEV 先验，修正 trajectory anchors 并指导 diffusion trajectory 生成；**模型内部可解释引导** | 作者报告 NAVSIM v2 `EPDMS=86.3`；并不是提出名为 RiskField 的公共新评分标准 | `MODEL-PRIMARY`；`PRIMARY-ABSTRACT`+官方项目；该项目页面仍将模型/训练代码列为待发布，**未确认完整代码可复现** |
| **DRiF: Data-Driven Risk Fields for Safer End-to-End Autonomous Driving**，2026-09，[arXiv:2609.10377](https://arxiv.org/abs/2609.10377)、[正文镜像](https://rt.http3.lol/index.php?q=aHR0cHM6Ly9hcnhpdi5vcmcvaHRtbC8yNjA5LjEwMzc3djE) | 静态 BEV map 监督 + 动态 ego-conditioned risk 场；训练时用规则构建 overlap/corridor/occupancy **成对风险排序**，不用拟合绝对数值；风险场通过 BEV 表示影响规划，部署不保留训练标签生成器 | 作者报告 Bench2Drive 220 路线：DS 88.78、SR 75.91；采用已有闭环指标验证模型，不提出官方新指标 | `MODEL-PRIMARY`；`PRIMARY-FULL`（镜像的 arXiv v1 正文）+官方摘要；**代码/数据标为将来公开，未核实实际发布** |
| **READ: Learning Risk-Informed Fields for End-to-End Autonomous Driving**，2026-09，[arXiv:2609.12371 正文](https://arxiv.org/html/2609.12371) | 可学习、随时间变化的**各向异性高斯场**，地图/未来 occupancy/示范轨迹/运动学残差等部分约束；作为 E2E 辅助训练与 VLA risk tokens；还可以对轨迹计算平均风险并选择性做 waypoint refinement | NAVSIM v1：TransFuser 84.0→84.6 PDMS、Drive-JEPA matched 89.1→90.0；NAVSIM v2 还报告 EPDMS；**仍按官方评测** | `MODEL-PRIMARY`；`PRIMARY-FULL`；与现有高斯 RiskField/跨架构构想**最直接重叠** |
| **Risk Map As Middleware (RiskMM): Toward Interpretable Cooperative End-to-End Autonomous Driving for Risk-Aware Planning**，RA-L 2026，[IEEE 正式发表](https://ieeexplore.ieee.org/document/11266912/)、[arXiv:2508.07686](https://arxiv.org/abs/2508.07686) | V2X 协同感知 → 学习时空风险地图 → 学习式 MPC；**网络+规划器使用风险表征** | V2XPnP-Seq 等规划验证，**不是 NAVSIM 指标创新** | `MODEL-PRIMARY`、`PRIMARY-ABSTRACT`；协同输入与我们单车 NAVSIM 条件不同 |
| **RiskMap: A Unified Driving Context Representation for Autonomous Motion Planning in Urban Driving Environment**，2024，[arXiv:2406.04451](https://arxiv.org/abs/2406.04451) | **可微风险场**作为交通环境的统一上下文与规划代价，采样式 planner 使用 | 传统/学习式混合规划的安全与平顺性，不直接定义 E2E 公共分数 | `ADJACENT`、`PRIMARY-ABSTRACT`；更早直接的**风险场→规划 cost**前例 |
| **Enhance Planning with Physics-informed Safety Controller for End-to-end Autonomous Driving**，2024，[arXiv:2405.00316](https://arxiv.org/abs/2405.00316) | FusionAssurance：Potential Field 进入 MPC 安全控制，与端到端轨迹预测模型结合 | CARLA 结果；评测的是系统的风险规避，不是新公共风险指标 | `MODEL-PRIMARY`/安全层，`PRIMARY-ABSTRACT`；风险场仅为控制器的一部分 |
| **Vehicle Safety Planning Control Method Based on Variable Gauss Safety Field**，2022，[正式全文](https://www.mdpi.com/2032-6653/13/11/203) | 变参数高斯安全场分别用于 RL 轨迹规划的**奖励**和跟踪控制的**评价**，输入有时序 BEV | 高速场景仿真；不是现代 WAM/NAVSIM 最终指标，但已覆盖“高斯场+学习式规划/奖励” | `ADJACENT`、`PRIMARY-ABSTRACT`+文章正文入口；**重要历史反例，勿称高斯安全场首次接学习式规划** |
| **Integrating spatial-temporal risk maps with candidate trajectory trees for explainable autonomous driving planning**，Communications in Transportation Research 2025，[期刊原文](https://doi.org/10.1016/j.commtr.2025.100161) | 传统/学习式混合规划：先构建时空风险地图，再对**多候选轨迹累积风险做过滤和选择** | 离线安全与效率、运行时；候选级风险累积先例，未证实是 WAM 公共 Benchmark | `ADJACENT`、`PRIMARY-ABSTRACT` |
| **Risk Occupancy: A New and Efficient Paradigm through Vehicle-Road-Cloud Collaboration**，T-ITS 2026，[arXiv:2408.07367](https://arxiv.org/abs/2408.07367)、[期刊 DOI](https://doi.org/10.1109/TITS.2026.3707600) | 4D 风险占用表征（空间/时间/风险）+ 局部规划，V2X 数据 | DAIR-V2X 等；并非标准 E2E/WAM risk scorer | `ADJACENT`、`PRIMARY-ABSTRACT` |

**新增关注但不计入 E2E/WAM 模型实证总数：**
- [A consequence-aware driving risk field framework with data-driven calibration for high-risk scenario identification](https://doi.org/10.1016/j.aap.2026.108704)，Accident Analysis & Prevention 2026：**事故后果校准的 risk-field 场景危险程度评分**，重点在场景风险识别而非 WAM 训练，反而对“新评价指标”路线可能更直接。当前仅核到出版商摘要，全文公式、使用数据和数值校准质量待补。  
- [Driver's Risk Field](https://www.nature.com/articles/s41467-020-18353-4)、[Driving Safety Field 2015](https://doi.org/10.1109/TITS.2014.2359430) 等是场建模理论起点，不自动成为 E2E 指标论文。

### 2.1 DRiF 与 READ 不能误当完全独立复现实验

两篇均来自**2026 年 9 月，同一清华大学车辆团队，作者高度重叠（Yuanxin Tian、Zhiyuan Liu、Jinhao Li、Zhenhua Xu、Wenhao Yu、Jianqiang Wang 等）**，研究方法和验证平台却不同：

- DRiF：规则三风险类产生**相对监督**；实证场景 Bench2Drive；场预测不是直接一个新的 benchmark。
- READ：可学习高斯时空场 + **部分几何/示范/残差监督**；实证 NAVSIM，并额外试验 E2E/VLA 多架构。

应按 **两个不同 arXiv ID/方法** 登记，但**不能把它们说成两个独立实验室互相验证**；是否共享训练代码、技术沿革或数据资产，仍未知。READ 正文未能凭本轮阅读确认与 DRiF 的互引关系，不能猜是先后版本或独立复现。

### 2.2 第一轮覆盖结论

**DIRECT-PRIOR-ART-FOUND / BENCHMARK-METRIC-GAP-UNVERIFIED。**  
“风险场/高斯场刚引入 E2E/WAM 可能有创新”已经被 FlowDrive/DRiF/READ/RiskMM 等**直接先例显著削弱**。风险场作为训练、模型内表征、在线选择/控制评价已存在广泛相邻工作。

本轮搜索中**尚未确认**有论文将某一种风险场直接标准化为 **NAVSIM 公共主评分/官方 leaderboard 替代指标**；但是**未确认≠从未有人做过**，不能据此宣布创新空白。应继续搜索 risk-field-based evaluation benchmark、planning safety metric、risk-map scoring 以及传统安全 surrogate measures，并按阅读证据等级记录排除项。

## 3. 我们的现有 Gaussian RiskField 与先例的重合、差别

原始报告所述当前单 actor 静态高斯 + 速度动态项 + sigmoid gate（旧脚本审计，不是本轮重新执行），通过 max-over-actors 与窗口 max/mean/超过阈值比例生成统计量：

- **与 READ 的重叠**：均为 BEV 的连续/高斯风险表示。**差别**：现有脚本是固定手设参数的逐时刻已记录 ego 位置查询；READ 是以神经网络预测高斯分量权重/空间尺度，随时刻变化，并在训练中以多种部分约束学习场。不能仅改为“沿生成轨迹求积分”就宣称超过 READ。
- **与 FlowDrive 的重叠**：把风险势场作为场景引导。**差别**：FlowDrive 直接影响扩散规划；我们当前没有任何接入/规划性能实验。
- **与 DRiF 的重叠**：通过周车/路线关系表达风险。**差别**：DRiF 从风险类别优先级生成监督，优化的是相对风险排序，不直接学习现有脚本的绝对高斯值。
- **与 RiskMap/传统 trajectory cost 的重叠**：可微场/沿路 cost、候选累积值已有人做；若仅加一个新风险 mean 或 peak 数值，其思想也不是新颖的。
- **审计仍需核查的实现点**：`ly05_eval_riskfield.py` 里给 `obs_l/obs_w` 传的是 EGO_L/EGO_W？速度使用 `abs(vx)` 而非沿目标 heading 的完整相对速度？异常 dt 回填 0.1s？逐帧 max 忽略第二危险 actor？脚本和渲染端场函数是否逐点一致？这些都只记为用户原有复盘提出的**静态待核项**，不伪称本轮有执行脚本复核。**源脚本本身未在本次 GitHub 仓库检索里得到可运行版本**。

## 4. 作为新评价指标，真正需要核查的“场/轨迹/总分”三层

| 层 | 研究对象 | 当前可操作的问题 | 常见误区 |
|---|---|---|---|
| **F1：场函数** | `R(x,y,t | s,A)` 的几何、交互与不确定性语义 | 高斯/距离/相对速度场能否捕捉不同空间危险程度？有无有意义的尺度？ | 把经验热力值解释为**校准事故概率** |
| **F2：轨迹聚合** | 对每条 ego `τ` 查询并聚合场值，考虑 vehicle footprint、风险峰值、暴露时长、场景采样 | 两条 NC=TTC 同分的轨迹，是否具有不同的暴露、车距、相对速度和冲突持续时间？场值是否仅重复已有 TTC？ | 只把现有逐帧 ego risk 做 mean 就认为建立了全新规划评分 |
| **F3：Benchmark 兼容性** | 多模型/多场景打分、评价排序与误罚类型 | 能否在固定 NAVSIM 轨迹/采样/他车回放协议上加 **独立 risk diagnostic**，保留原 PDMS 不变并报告分项变化？ | 单纯 Std/Range 增大等同评测“更准确”；无对照直接修改官方主分数 |

**推荐优先从 F2–F3 做专项研究，F1 先用现有手设场作为受控基线。** DRiF/READ 已在 F1 + 模型侧证明不同风险表示和训练监督路径，继续从零学习整张场不一定是当前最省时的指标创新路径。

## 5. 未来信息的研究设计（不可跳过）

区分至少三种互不等价的版本：

1. **LOGGED-ORACLE-DIAGNOSTIC**：固定 ego 候选（历史上未实际执行）和日志重放的 other-agent 轨迹计算场值，可同 NAVSIM v1 的非反应式假设做**后验对比**，但不是其他人对候选行动的真实反应。
2. **DEPLOYABLE-PREDICTIVE-SCORER**：用当前可获得的其他 agent 状态或预测未来代替 oracle，不能偷看将来轨迹。需要报告预测不确定性。
3. **REACTIVE-CLOSED-LOOP**：将 ego 执行/重规划反馈给会反应的他车仿真。需要将响应模型假设、场值目标、规划策略实际安全结果分开。

本轮**以 1 为低成本研究入口**；它是离线 benchmark 语义的一部分，**不是在线可部署机制**。若长期目标仍是正式公共 Benchmark 指标，可定义统一他车重放协议，但应说明此协议限制；如果要验证交互效度，再转 3。M1 不能默默切换 1/2/3 的评价对象。

## 6. 首轮最小可行审计与证伪计划（不启动训练）

**目标不是先凑一个风险公式**，而是判断风险场是否提供 PDMS 分项之外的、跨模型可重复的规划质量信息。

| 门槛 | 最小工作 | 要检查的结果/失败条件 |
|---|---|---|
| **G0 数据和接口** | 从现有 NAVSIM scorer/输出/scene cache 核对轨迹与 agent 时间、坐标、尺寸和速度字段；对齐用户 RiskField 脚本与渲染函数 | 真实脚本无法正确映射坐标、仅有非时序未来、成本异常高 → 优先修数据接口 |
| **G1 场本身** | 手设 3–5 个受控 toy 场景：前车/侧车、快/慢接近、短时擦肩/长时贴近、多个同时危险对象、停车等；查是否符合**场构造时宣称的单调性** | 与相对速度/时间/尺寸变化呈反直觉结果；对横向/转向不稳定 |
| **G2 轨迹级新增信息** | 固定模型输出/官方 PDMS，计算风险 peak、time-weighted integral、exposure；对 **PDMS/NC/TTC 同分轨迹**做成对分析 | 大多数有效样本新增量只是 TTC 或距离单调变换；不对应任何可解释质量差异 |
| **G3 排名/稳健性** | 在多个已有不同架构（有固定输出轨迹）的 baseline 上报告模型/场景排序、bootstrap CI、参数扰动、采样频率敏感性；若能找到独立事件/人工偏好，只测明确定义的目标 | 换一个高斯参数/抽样 seed 就大幅改排名；总分被严重场景选择偏置 |
| **G4 可选择性进入决策** | 若 G1–G3 有信息价值，在一个现成多候选 WAM 上做固定候选 reranking 试验，检查 PDMS 分项及过度保守/进度损失 | 无候选、多候选集合不可比、利用 logged future 泄漏、仅新评分涨而官方结果降 |

G0–G3 是**评价指标专项**；G4 才是可选的**WAM 内部使用**。不必为了证明一个外部指标能诊断问题就先去做大规模训练。

**用户已有可用规划基线线索：**SimWAM 官方 RL checkpoint 曾测得 NAVSIM v1 PDMS=91.9036（原复盘记录），但那是一个模型的官方分数复现，**并不是 RiskField 的任何改进效果**。有待确认是否可导出统一格式的固定轨迹与足够数量的不同架构基线，不能默认全套数据已在 GitHub。

## 7. 后续直接文献检索的约束和优先级

**下轮检索必须完成，不能把本轮结果当作找全：**

- 沿 DRiF/READ/FlowDrive/RiskMM 的 Related Work 与被引链，找 **explicit risk field in E2E planner**、risk occupancy / risk map scoring / cost maps、trajectory risk aggregation、surrogate safety metrics（包括首次发表时间早于 2024 的工作）。
- 针对 **benchmark risk-field metric** 与 **evaluation of learned planners** 寻找直接先例，按“最终榜单评分 / 离线诊断 / planner cost / 训练 reward / 监督表征”分别编码。
- 正式精读 FlowDrive energy-field 的具体数学定义、DRiF 样本对/排序阈值、READ 高斯场及选择性 refinement 的数据需求；**尤其核查其使用的是训练时 GT future 还是部署预测**。
- 核验 2026 后果校准场论文的“事故严重性”标签来源，确认它能否作为外部危险度/风险场的**有效性验证参考**；不把事故后果校准模型误称为完美事故概率。
- 检查实际代码发布状态及许可证，不从作者口头“即将公开”推断代码已有。

### 推荐继续精读的三篇（与原 StyleDrive 衔接）

1. **READ（首选）**：直接同高斯场、NAVSIM、跨 E2E/VLA 框架吻合；**重点剖析 F1/F2 与它的训练创新边界**。[全文](https://arxiv.org/html/2609.12371)。
2. **FlowDrive**：早于 READ，在 NAVSIM v2 使用规则风险势场引导；用于回答“风险场 + E2E 这一想法此前做到哪里”。[论文](https://arxiv.org/abs/2509.14303)。
3. **DRiF**：相对风险排序而非绝对风险值监督，并使用 Bench2Drive 闭环作为独立训练收益验证；注意作者与 READ 重叠。[论文](https://arxiv.org/abs/2609.10377)。

**本专题阶段性结论：风险场接入 E2E 已有多个强相关先例，不可再用泛化组合宣称新颖。评价指标侧的研究机会尚在于“究竟评价何种风险、如何沿轨迹聚合、与既有分项差别何在、离线非反应式得分能反映什么”，必须先验证 G1–G3，才可判断是否构成独立论文贡献。**
