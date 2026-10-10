# Wave 2：直接评价指标论文的公式、验证与成本审计（2026-10-10）

> **阶段判定：PRIMARY-EVIDENCE-PARTIAL-PASS / FORMULAS-AND-VALIDATION-IN-PROGRESS。**  
> 唯一工作分支：`codex/evaluation-metrics-baseline-audit-20261010`（本轮不创建新分支）；关联 [论文账本](01_BENCHMARK_METRIC_LITERATURE_REGISTER_W1_20261010.md)。  
> 本轮聚焦真正的**自车规划评价指标**。区分：论文的明示贡献（PAPER）、公开代码可验证行为（CODE）、我们的推论（ANALYSIS）、未确认（UNKNOWN）。**不新建候选创新点，不做任何论文外的指标实验。**

## 1. 已核实的直接指标创新案例

### 1.1 StyleDrive（AAAI 2026）：底座基本保留，局部评分函数修改

- **问题/对象（PAPER）**：NAVSIM v1 PDMS 没有区分驾驶风格；作者在已有 OpenScene 数据上增加 A/N/C 标注，并提出 SM-PDMS。
- **公式（PAPER + CODE）**：保留 NC、DAC 乘法约束与 (5 EP + 5 TTC + 2 Comfort)/12 聚合；Comfort 随风格调整阈值 ±20%；TTC 检测后根据 A/N/C 的 0.8/1.0/1.2 秒阈值做 **0/1 判断**；EP 改成 `max(1 - 1.2*((d_model-d_human)/Ref)^2, 0)`（Ref 根据真人进度 3/5/6/7 分段）。
- **代码级特殊性（CODE）**：TTC 预测检查点是 `np.arange(0,15,3)`，0.1s 默认采样时仅含 **0、0.3、0.6、0.9、1.2s**，因此 A 与 N/C 的边界可不同，但 **N 1.0 秒和 C 1.2 秒在这个离散实现下产生相同的 TTC 二值判定**。不是作者论文明确强调的结论。
- **EP 的额外分支（CODE）**：只在 `max(raw_progress) > progress_distance_threshold` 时执行与真人进度匹配的二次函数，否则 `normalized_progress = 1`；读公式时不能漏掉这一实现分支。
- **验证（PAPER）**：三种 style 模型下，EP Std 1.657→4.339，Comfort 0→0.312，TTC 0.643→0.575，总分 1.614→1.660；对模型分数敏感性有一定支持，**TTC 与总分变化有限**；模型条件化实验是另一个问题。
- **额外实验/数据成本（ANALYSIS）**：已有原始标签、评分器和 OpenScene 环境时，改指标不必重训 WAM；但 StyleDrive 的数据标注/风格模型实验本身有额外数据和模型工作。不能只按改评分器的代码行数估算整篇论文成本。

权威来源：[AAAI 2026](https://ojs.aaai.org/index.php/AAAI/article/view/42463)｜[论文 §4.1/4.3、补充 §1](https://arxiv.org/html/2506.23982)｜[作者官方评分器](https://github.com/AIR-THU/StyleDrive/blob/main/navsim/planning/simulation/planner/pdm_planner/scoring/pdm_scorer.py)（本轮 GitHub fetch 得到该文件 blob SHA `0d2b4bfd65bd1cd7c6a9c6b75df5d410f070a966`）。

### 1.2 WOD-E2E / RFS（CVPR 2026）：多参考人工评价 + 容忍区域 + 衰减

- **评价对象（PAPER）**：Waymo Long-tail E2E 的开环规划轨迹，打分反映多条人工评分参考轨迹，而不局限一条 logged expert 或 ADE。
- **官方函数（CODE）**：`get_rater_feedback_score` 接收预测轨迹（可多候选及概率）、`rater_specified_trajectories`、0~10 的 `rater_feedback_labels`、初始速度。默认参考条数 3（不足复制最后一条）；采样频率 4 Hz，5 秒。
- **时间与空间（CODE）**：**只在 t=3s 和 t=5s** 评价偏差。基本横向容忍半宽分别 1.0m/1.8m；纵向为四倍（4.0m/7.2m），均再乘 `clip(0.5+0.5*(v-1.4)/(11-1.4),0.5,1)` 的初速比例。
- **逐时刻参考匹配（CODE）**：对候选 i、人工参考 p、时刻 t，计算沿参考轨迹方向的绝对纵向/横向差 `D_lng, D_lat`，定义 `q=max(D_lng/T_lng,D_lat/T_lat)`，局部匹配评分 `s[p]*0.1^max(q-1,0)`。**每个时刻分别选最高参考分**，再平均 3s/5s；对于**不在任何参考的两个时间点同时落入容忍区域的候选**，结果设最低 4 分（`max(4,score)`），因此并非所有偏移都被无限降分。多条预测轨迹还按给定推理概率加权。
- **不能误说（CODE）**：“对三条参考分别算完整轨迹得分，然后取最大”与**代码实际顺序**不同；实际是 `max over rater` 在两个评测时刻分别进行，再平均两个时刻，**不同时间可匹配不同参考**。
- **验证代价（ANALYSIS）**：官方 NumPy 实现可运行，**不要求新训练 WAM**；但在别的数据（尤其 NAVSIM）使用 RFS，需要配套多条 reference 及人工 0–10 标签，不能无成本复制 RFS。注意其 reference-可得性限制和对中间时刻运动的忽视。
- **状态**：`CODE-READ`，对官方评测代码核实；完整 CVPR 论文消融和 rater 间一致性**尚未审计**。

权威来源：[CVPR 2026 论文页](https://openaccess.thecvf.com/content/CVPR2026/html/Xu_WOD-E2E_Waymo_Open_Dataset_for_End-to-End_Driving_in_Challenging_Long-tail_CVPR_2026_paper.html)｜[Waymo 官方实现（固定提交）](https://github.com/waymo-research/waymo-open-dataset/blob/99a4cb3ff07e2fe06c2ce73da001f850f628e45a/src/waymo_open_dataset/metrics/python/rater_feedback_utils.py)｜[对应单元测试](https://github.com/waymo-research/waymo-open-dataset/blob/99a4cb3ff07e2fe06c2ce73da001f850f628e45a/src/waymo_open_dataset/metrics/python/rater_feedback_utils_test.py)。

### 1.3 DriveCritic（ICRA 2026）：直接学习轨迹对人类偏好，重点在验证样本可靠性

- **任务（PAPER）**：对同一场景两条候选轨迹选出更符合上下文和人类偏好的一条，而非提出单一 PDMS 公式。以 EPDMS 的 LK/EP 在特殊情境可能误罚为切入点。
- **构造（PAPER）**：NAVSIM 里从人类 trajectory 与离散 vocabulary 提取 **5,730 对**；`navtrain` 4,564 对用于训练，`navtest` 1,166 对测试。两种情况：LK 与 EP 权衡、EP 进度权衡。
- **人工标签边界（PAPER）**：测试集 **由主要作者一人进行人工偏好标注及核对**；训练 Case 1 采用 human-preferred 伪标签，Case 2 使用 GPT-5 标注。**不能把“expert human annotations”误读为多人独立盲评或已经测得跨评审一致性。**
- **模型与验证（PAPER）**：Qwen2.5-VL-7B，SFT + DAPO；作者测试集报告 76.0% preference accuracy。根据项目页 EPDMS 约 46.6%，但应注意其测试集被专门筛选为规则指标困难场景，不能解释为 EPDMS 在一般场景准确率仅有 46.6%。
- **成本（ANALYSIS）**：不仅需要人类偏好数据，还要训练大 VLM 评价器；与 StyleDrive 式的低成本 scorer 改造不是一类项目。
- **状态**：`METHOD-READ`；人工标签多评审验证未见报告，不能以此直接认为全领域偏好真值已解决。

权威来源：[ICRA 2026 作者页](https://song-jingyu.github.io/DriveCritic/)｜[arXiv v2 正文 III–V 节](https://arxiv.org/html/2510.13108)。

### 1.4 DriveJudge（2026-06 预印本）：语义规则选择 + 评价器的评价任务

- **算法（PAPER）**：VLM 选择性调用物理规则函数，不是纯 LLM 主观打分；规则调用集合与条件化评分是算法贡献。区别于单一子项阈值优化。
- **数据（PAPER）**：人工评估 **10,732 段**，提取 **33,577 个 2s 片段**，15.3% 失败；测试 1,083 例，其中 23.3% 失败。
- **评价新机制的两个任务（PAPER）**：DQC 判断行为是否合理，报告 AUC / failure AP；TPS 判断成对轨迹的人工偏好，报告准确率。作者 8B 模型 DQC AUC **78.90** vs EPDMS **57.67**（差 **21.23 个百分点**）；TPS **82.83%** vs DriveCritic **76.33%**（差 **6.50 个百分点**）；TPS 数据来自针对偏好困难样本的再筛选，**不与 DriveCritic 原始测试集 76.0% 直接混合比较**。
- **成本/范围（PAPER）**：作者正文训练报告使用 **8 张 A100**，因此不属于低成本无需训练的简单指标修改。
- **研究意义（ANALYSIS）**：这篇文章将“指标效度”转成可操作的 DQC、TPS 任务，为我们提供除 Std/Range 外的另一套验证范式；但它是预印本，目前未确认顶会接收。
- **状态**：`METHOD-READ`，尚未完成附录/训练代码复现。

权威来源：[arXiv v1 论文 §3–5](https://arxiv.org/html/2606.17362v1)。

### 1.5 S2O（Accident Analysis & Prevention 2025）：传统规划评价中的主客观映射

- **方法（PAPER 官方正文/摘要）**：分项为安全、时间效率、舒适、能耗；通过分段线性拟合 + SVM 段分类器来映射人类主观评分，并有碰撞惩罚修正。这是**学习综合权重/聚合关系**而不只是改子项阈值。
- **证据（PAPER）**：D2E 约 **1000 个驾驶案例、40,000 个人工评价分**；作者报告总体百分制 MAE **4.58**、相对基线误差降低 **32.55%**；另在 SUMO 与三种规划算法上验证。
- **限制**：这些指标是特定主观驾驶质量的拟合，不意味着可以无监督接到 NAVSIM 的最终分项计算；原公式全文与数据权限尚需核实。
- **状态**：`JOURNAL-FULLPAGE-SUMMARY`，可读到出版商网页正文节选和摘要，**未完成所有公式精读**。

权威来源：[期刊 DOI 文章](https://www.sciencedirect.com/science/article/pii/S0001457525001125)｜[PubMed](https://pubmed.ncbi.nlm.nih.gov/40233569/)。

### 1.6 Scalable evaluation methods for autonomous vehicles（Expert Systems with Applications 2024）

- **方法（PAPER 官方摘要）**：构建 `scenario complexity` 对不同难度场景缩放评分，除了自车安全/舒适/驾驶性能/法规，增加**对其他交通参与者影响的 altruism** 分项；MEREC 决定权重，MARCOS 做综合排序。
- **验证（PAPER 摘要）**：作者声称仿真及真实车辆测试验证该方法；没有原文全文公式与样本详情之前，**不能判定不同复杂度校正是否真的带来更公平的模型排名**。
- **迁移价值（ANALYSIS）**：证明传统规划评价中已存在**场景复杂度缩放 + 外部交通参与者影响 + 多指标综合排序**；若迁移 NAVSIM，不能宣称首次提出其中任何一个一般概念。
- **状态**：`PRIMARY-ABSTRACT`，全文需机构访问或合法公开副本。

权威来源：[期刊全文信息与官方摘要](https://www.sciencedirect.com/science/article/pii/S0957417424004688)。

## 2. 发现两篇补充研究（新增到账本）

- **FluidTest: Is Your Trajectory Displacement Safe in Long-tail?**（[2026-06 预印本](https://arxiv.org/abs/2606.16313)）：以规划轨迹相对专家的**新增安全威胁**为目标；32 类风险语义、人工成对标注和三代理验证。摘要报告 WOD-E2E 里 Poutine、RAP 分别 65%/51% 的轨迹有新增威胁。**非简单改 PDMS 公式**；需要核实威胁标签可信度、时间/行为颗粒度、原理与评审可靠性。
- **Do Open-Loop Metrics Predict Closed-Loop Driving? A Cross-Benchmark Correlation Study of NAVSIM and Bench2Drive**（[2026-04 预印本](https://arxiv.org/abs/2605.00066)）：从 15 个模型搜集公开结果，只有 **n=8** 可完整配对；作者报告整体指标对 Bench2Drive 闭环分数的 Spearman **ρ≈0.90**，简化 3 项也达到同样相关系数。属于**指标效度与聚合诊断**，但样本很小，且“用同一样本选出简化公式再验证”需要谨慎。不能直接得出“EP 是全领域最客观的单项指标”。

这两篇说明评价研究不只是“定义一个新标量”——也可以从**有效性检验/错误暴露/评价对照**出发，但应与指标公式论文分开计数。

## 3. 对我们项目的实际可行性筛选（尚未试验）

| 实现路线 | 现有证据代表 | 所需条件 | 研发成本判断 |
|---|---|---|---|
| 修改 NAVSIM 子项/权重/聚合 | StyleDrive、NAVSIM v2 | 官方 scoring 环境、轨迹及场景缓存；可能需要原有传感器或地图资产 | **相对低**：可先固定模型输出，无需新 WAM 训练 |
| 引入传统多目标/复杂度校正 | Scalable、S2O | 场景难度、行为影响或人工评分，取决于公式 | **中～高**：若所有量从已有场景可算成本低，若需要标注则明显增大 |
| RFS 型人工多参考评价 | WOD-E2E | 多条参考及人类质量标签；官方 scorer 已公开 | **指标计算低，建立数据/标注高** |
| VLM 场景语义评价 | DriveCritic、DriveJudge | VLM 训练/推理、标注与可重复测试协议 | **较高**：至少更复杂，DriveJudge 作者报告 8×A100 训练 |
| 新的安全威胁验证任务 | FluidTest | 风险词表、人工/自动验证协议、跨场景一致性 | **中～高**，验证可信度是主要难点 |
| 跨 benchmark 效度分析 | 2026 Cross-Benchmark study | 成对模型结果和设置控制、足够样本量 | **较低算力**，但更难保证统计结论稳健 |

**目前更建议下一轮先调查两个“可低成本复核的评价问题”而非立刻发明公式：**
1. 不改底层仿真，单独改变聚合/阈值/误罚过滤，究竟会改变哪些模型或场景的分数、排名、置信区间？
2. 各个子指标是否因分数饱和、不同场景比例或乘法门控，使不同规划能力难以被观察？先量化再决定研究哪个性质。

这只是可行性诊断任务；如果得不到稳定可观察的现象，就不升格为论文创新点。

## 4. 尚未解决的核查事项

- WOD-E2E：需要审查 CVPR 全文的人工参考标注协议/标注一致性及 RFS 验证实验（本轮最强证据来自 Waymo **官方评分代码**）。
- DriveCritic：测试集仅主要作者独立标注；是否有额外独立评审、不同专家一致性未知，不能凭“专家偏好”暗示多人的统计共识。
- DriveJudge：进一步核查人工标签协议、TPS 重过滤过程与模型公用数据风险。
- S2O/Scalable：需要读取可合法获取全文，核对分项公式和多指标聚合的完整数学细节。
- FluidTest/Cross-Benchmark：目前仅官方摘要已核实，必须标为 `PRIMARY-ABSTRACT` 而非 `METHOD-READ`。
- **传统迁移路线仍未完整精读**，应从“旧法作为训练 loss / 候选评价 / 最终 Benchmark 哪种角色”继续核查，避免把已有数学表达误当新的 Benchmark 首创。
- 本轮未运行任何模型训练、NAVSIM 轨迹重评、RFS 评分计算；**不能宣称已经证明某种指标比 PDMS 更优**。

**Wave 2 结论：指标创新确有多种已发表路径，但“低计算成本 ≠ 低研究验证成本”。重点候选是可在固定 NAVSIM 轨迹上再评分的轻量改进；人类偏好/VLM 新指标属于另一种更重的实验条件。**
