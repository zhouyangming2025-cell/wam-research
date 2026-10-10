<!-- 用户原有复盘文档之独立归档副本；此文包含静态审计、历史调研与未证实构想，不代表本专题检索已完成。GitHub 保存日期：2026-10-10；来源：ChatGPT Library, 原名 riskfield_e2e_wam_research_recap_CN.md。新专项结论以相邻 riskfield 专题审计为准。 -->

# 风险场与端到端驾驶 / WAM：调研与讨论完整复盘

整理日期：2026-10-10  
项目：zhouyangming2025-cell/wam-research  
用途：把指标研究、传统风险场文献、端到端 / WAM 评分方法，以及近期跨架构迁移构想串成一份可复查记录。

## 0. 先给结论

目前的工作由两条相邻问题线汇合而来：

1. **评价指标线**：NAVSIM 的部分指标较硬，促使我们讨论“已有指标怎样完善、还可增加什么评价信息”，并区分训练奖励与 benchmark 指标。
2. **风险场迁移线**：我们手上已有一套基于高斯 RiskField 的交通状态分析脚本，于是提出把风险场思想迁到多个端到端 / WAM 模型中，探索其是否能作为可复用的评分或训练模块。

截至本报告：

- 我们已完成传统连续轨迹代价、驾驶风险场、概率风险 / CVaR、IRL、安全约束等**相邻基础文献**的专题核读；也精读了 15 篇与 WAM / 学习型评价、奖励或候选评分相关的论文，并对 NAVSIM 指标与部分实现做了静态审计。
- **尚未完成**“风险场与端到端自动驾驶 / WAM 的直接应用论文”系统检索。因此不能说风险场已在 WAM 中普遍验证，也不能根据现有资料断言我们的组合已新颖或有效。
- 现有风险场脚本是一个**离线分析 / 可视化原型**，用于逐帧算风险并与 TTC gate 样本对照；它不是已接入任一 WAM 的可训练模块，不是官方 benchmark 指标，也没有经当前记录证明其值是校准碰撞概率。
- “做成可插拔模块并接入多个模型，期望多篇模型都提升”是一个有潜力但尚未验证的研究设想。可复用的接口值得探索；每个模型都能提升、无需重训、计算代价很低等均不能预先保证。
- 风险场本身、势场、距离代价、概率风险地图都已有先例。潜在贡献要落在**评价对象、场的定义、与规划模型连接的机制、训练 / 推理边界、跨架构验证或评测诊断能力**上；既可以是对现有方法的完善，也可以是向 WAM 迁移，不要求凭空创造一个无人研究过的概念。
- 到目前没有选定最终方法，也没有在 WAM 上完成接入、训练、性能对比或运行时测试。

建议把这项工作的当前定位写成：**从 NAVSIM 指标与已有 RiskField 工具出发，调研风险信息怎样更有效地参与端到端规划的训练或评价；通过直接文献盘点和小规模验证，再判断应该做训练信号、模型内评价器、补充 benchmark 诊断量，还是几者组合。**

## 1. 问题是怎样形成的

### 1.1 最初的入口是评价指标，不是预先决定的“风险场方案”

最初观察到 NAVSIM 的若干评分项基于阈值或门控，某些接近边界或违规程度不同的轨迹，最后可能得到相同或相近的分项 / 总分。由此提出的问题是：有没有工作改善自动驾驶评价指标或评测体系，以及评价本身能否成为论文贡献。

讨论后把“指标”按用途分开：

| 用途 | 评价对象 | 主要要求 | 改进证据 |
|---|---|---|---|
| 训练信号 | 单条样本、候选轨迹、策略回报或监督标签 | 对学习有区分度，统计稳定，和目标行为一致，难以被策略钻空子 | 控制数据、算力和模型后，训练效率或最终驾驶行为改善 |
| Benchmark 指标 / 协议 | 固定模型在确定数据、场景、仿真协议下的表现 | 可复现、公平、可解释、排名有意义、覆盖重要失败类型 | 对受控轨迹差异有响应，与独立评测或人工判断有支持关系 |

同一 NAVSIM 分项可以既出现在 benchmark，又被论文取作 RL reward；但两种用途的目标不同。训练信号更细或更平滑，不等于应当修改公共排行榜；一个评价标准作为 benchmark 公平可用，也不代表它已是最好的逐样本学习信号。

讨论进一步澄清：NAVSIM 的硬边界只是**研究入口**，并没有证据证明它导致 WAM-Flow 或其他模型训练失败。策略梯度方法如 GRPO 可以用采样奖励做相对更新，不要求奖励对轨迹坐标可微。更具体的待查问题是信号是否区分候选、是否在特定采样分布下太稀疏、改进后能否迁移到独立评测。

### 1.2 Benchmark 不是本轮唯一目标

组会讨论认为 NAVSIM、Bench2Drive 等现有评测系统整体比较固定、合理且公平，短期没有必要把“另造一套 benchmark”设为默认目标。风险场若进入评价，较自然的起点是保留官方分数作为共同基准，同时增加诊断项；是否进一步改官方评分，再由研究问题决定。创新可分两类：

- **沿用基准、调整评价方法或计算方式**：保留 NAVSIM 的数据 / 仿真 / 大部分指标定义，只修改一部分评价口径、信息表达或聚合方式。
- **提出不同的评价量**：增加或替换评价对象，例如安全裕量、风险暴露、概率风险、尾部损失等。

StyleDrive 被拿来作为“保留 NAVSIM 底座、改变评价 / 风格表达并跨多个规划基线验证”的案例与类比。讨论中列出的四个模型结果是 AD-MLP 63.72→60.02、TransFuser 78.12→81.09、WoTE 79.56→81.38、DiffusionDrive 79.33→84.10（论文报告的 SM-PDMS）。它支持“对既有框架作有针对性的扩展也可研究”，但它做的是风格条件 / 风格评价设计，**并不证明高斯风险场可以直接以同样方式接入多个模型**。

### 1.3 风险场构想从已有脚本和 SimWAM 讨论自然引出

随后用户提供了风险场评估与渲染脚本，并提出：高斯只是熟悉的一种风险场形式；还可以考虑碰撞概率、势能 / 引力类构造或其他风险表示。是否能把风险场迁移到多个端到端 / WAM 论文，而不仅是在某个 base 上简单加一项？能否像模块一样在不同模型中接入，并观察是否普遍有益？

具体待解决点被列为：

1. 风险场应接入 WAM 的哪个环节？
2. 逐候选、逐时刻计算的运行效率怎样？
3. 是否能迁移到多篇论文？每个模型是否都会提升？
4. 哪些接法需要重新训练，哪些可以推理时直接插入？
5. 训练资源、实验时间和可复现成本如何？

这些是问题清单，不是已得出的答案。风险场是从指标研究生长出的候选方向之一，不能反过来把全部研究收窄成“必须做风险场 + WAM”。

## 2. 已有高斯 RiskField 脚本做了什么

审阅了两个已有文件：**ly05_eval_riskfield.py** 与 **ly05_v8_render.py**。本节是对文件内容的静态阅读记录，不代表本轮重新运行了脚本。

### 2.1 单障碍物风险的计算形式

评估脚本在每帧取 ego 位置作为查询点，对每个障碍车算一次风险，再取本帧所有障碍物中的**最大值**。先把 ego 相对障碍物的位置变换到障碍物航向坐标系：

\[
x'=(x_{\rm ego}-x_{\rm obs})\cos\theta_{\rm obs}
 +(y_{\rm ego}-y_{\rm obs})\sin\theta_{\rm obs}
\]

\[
y'=-(x_{\rm ego}-x_{\rm obs})\sin\theta_{\rm obs}
 +(y_{\rm ego}-y_{\rm obs})\cos\theta_{\rm obs}.
\]

脚本使用的尺度为：

\[
\sigma_x=l_x(L+\epsilon)+\epsilon,\quad
\sigma_y=l_y(W+\epsilon)+\epsilon,\quad
\sigma_v=k_v|v_{\rm obs}-v_{\rm ego}|+\epsilon.
\]

并按障碍物速度与 ego 速度的大小关系确定方向因子 \(r_l\)。静态椭圆高斯项、速度调制动态项与 sigmoid 方向门控相加：

\[
R_{\rm static}=A\exp[-((x'/\sigma_x)^2+(y'/\sigma_y)^2)]
\]

\[
R_{\rm dyn}=A\exp[-((x')^2/\sigma_v^2+(y')^2/\sigma_y^2)]
\]

\[
g_{\rm dir}=\frac{1}{1+\exp(r_l[x'-\alpha(L+\epsilon)r_l])},\qquad
R_{\rm actor}=R_{\rm static}+R_{\rm dyn}g_{\rm dir}.
\]

默认参数是 \(A=1,k_v=6,l_x=1.5,l_y=0.5,\alpha=0.9,\epsilon=10^{-3}\)。ego 尺寸常量为 \(4.5 \times 2.0\)。代码还提供低速圆化分支：若启用低速阈值，则把动态纵向尺度压到 \(\epsilon\)、方向因子设为 0；但当前评估调用没有传入该阈值，按默认值该分支不启用。

以上是该脚本的实现表达；不能自动把它解释成真实碰撞概率。两个非负项相加后也可能超过 1，所以风险值大于 1 不等于概率大于 100%。

### 2.2 如何聚合，以及怎样与 TTC 对照

- 根据时间戳和 ego 的 \(v_x,v_y\) 积分，重建每帧 ego 世界位置。
- 对每帧的障碍车辆计算 \(R_{\rm actor}\)，取所有障碍车中的最大值作为该帧风险。
- 对一个窗口输出全程 max risk、risk > 0.5 帧比例、risk > 1.0 帧比例、risk 均值、帧数。
- 读取已有 gate CSV：L1 按 min TTC 从小到大抽样；L2 和 OK 按 CSV 原有顺序抽样。默认各抽 10 个窗口。将 RiskField 汇总量与 min TTC 及 gate 等级并列输出为 CSV。
- 输出的是**统计与对照数据**；脚本本身没有计算 AUC、校准误差、与碰撞概率的相关性，也没有从这些指标推出模型应如何更新。

### 2.3 可视化脚本的作用

ly05_v8_render.py 将物理目标跨帧追踪并标注物理 ID 与持续时间，生成三面板动画：俯视图与物理轨迹线、风险曲线、TTC 曲线。它调用既有 RiskField 热图与物理轨迹跟踪函数，可用于查看单段场景中高风险位置、对象运动和 TTC gate 是否一致。

可视化有助于发现方向、坐标和目标关联错误，但目视一致不等于量化有效性证明。

### 2.4 从静态代码审阅能提出的核查项

当前脚本提供了清晰的起点，但若要把数值用于论文指标、训练奖励或 WAM 部署，至少还要核实：

- **尺寸参数的语义**：单车函数的参数名是 obs_l / obs_w，调用处却传入 EGO_L / EGO_W。可能是有意用 ego footprint，也可能是尺寸来源与注释不一致；需对照 RiskField 原始定义、坐标系及目标框尺寸后判定。
- **速度语义**：调用使用障碍物 \(v_x\) 的绝对值及 ego \(v_x\)，未直接使用完整二维相对速度向量。应检查数据坐标定义，评估横向速度、逆向行驶、转弯及道路坐标旋转场景是否表达正确。
- **障碍物覆盖与漏检**：每帧遍历脚本实际读取到的 agent，需查明静态目标、行人、自行车、遮挡目标和跟踪 ID 切换是否进入数据。
- **分数含义与参数**：高斯宽度、速度调制和 sigmoid 方向门控由参数设定；默认值是否沿用其他文件、如何估计、跨场景是否稳定，均待验证。风险值不是概率校准结果。
- **公式实现的一致性**：评估脚本自行实现单车风险计算；渲染脚本另外调用 RiskField 热图函数。虽然注释称参数与公式保持一致，当前记录没有逐点对照两套实现的数值，需避免调参或改公式后两边悄悄分叉。
- **聚合损失信息**：逐帧取最大障碍物，适合强调最危险对象，但会忽略第二个危险对象；窗口 max 对峰值敏感，均值会稀释短时峰值，阈值占比又依赖阈值。应保留原始序列和多种聚合统计。
- **单位与离散采样**：时间戳、位置、速度、角度、车辆尺寸必须一致；缺帧时脚本把异常 dt 设为 0.1 秒，可能影响积分。需要审计输入采样与时间单位。
- **对象维度**：当前输出属于每个 ego 查询点对交通参与者的风险，不等同于沿候选自车轨迹的时空积分，也不覆盖完整未来交通响应。

## 3. 前期文献调研已经覆盖什么

### 3.1 传统连续轨迹代价与风险场

| 文献 | 本轮核读所得 | 与端到端 / WAM 的关系及边界 |
|---|---|---|
| Khatib, 1986，人工势场 | 障碍物排斥势与目标吸引势形成局部连续控制方向；基于空间接近程度 | “风险场 / 势场”思想很早已有，不应把场这个名字本身当作创新；局部极小值、参数和场景适用性仍是问题 |
| CHOMP, 2009 / IJRR 2013 版本 | 轨迹平滑先验 + 沿轨迹 / 车体点积分的障碍代价，以轨迹优化改进候选 | 可借鉴轨迹级累计 cost；其静态几何代价不能原样代替有速度和交互的交通风险 |
| TrajOpt, 2013 | signed-distance hinge 碰撞惩罚、顺序凸优化、信赖域和连续时间碰撞处理 | 说明连续、可优化、可行、安全保证是不同性质；有限次求解和惩罚项本身不自动认证安全 |
| Kolekar 等，Driver’s Risk Field, 2020 | 将驾驶者主观位置 / 事件不确定性与环境后果 cost 地图结合，以期望风险约束解释人类驾驶行为 | “主观驾驶风险”“经验场强”“客观校准碰撞概率”要分开；人类相似不等同规范安全 |

### 3.2 概率风险、CVaR 与风险地图

| 文献 | 风险对象 | 可借鉴之处 | 迁移限制 |
|---|---|---|---|
| Ono–Blackmore–Williams, 2010 | 有随机扰动下的有限时域联合约束满足概率 | 区分逐时刻安全与整段至少一次失败；风险预算和相关性重要 | 原论文是有限时域 open-loop 控制，不是 WAM 风险头 |
| Hakobyan & Yang, 2020，Wasserstein DR-CVaR | 到安全集合距离 / 穿入深度作为随机损失，再以 CVaR 与分布模糊集约束 | 风险可考虑尾部和样本分布不确定性 | 原文损失单位是距离，不是事故伤害；保证依赖样本和分布假设 |
| Hakobyan & Yang, 2021，distributionally robust risk map | 由障碍运动预测、DR-CVaR 构造风险图，再以 NN 代理供 MPC 使用 | “解析风险构造 + 学习代理 + 规划使用”已有相邻先例，是风险图迁移到学习控制最直接的传统桥梁之一 | 代理拟合误差、风险图保守性和闭环执行保证必须分层审计；MSE 小不代表边界上安全 |

用户还提过基于碰撞概率、万有引力 / 吸引排斥势能等不同路线。**概率 / 势场类原理在传统文献中有覆盖，但重力式风险场的具体公式与其在当前 WAM 上的直接应用尚未完成专项核查。**

### 3.3 IRL 与硬安全约束

| 文献 / 路线 | 相关性 |
|---|---|
| Abbeel & Ng, 2004，Apprenticeship Learning | 通过特征期望匹配逼近专家策略表现；不是恢复唯一真实奖励，也不能控制未表达的安全事件 |
| Ziebart 等，2008，Maximum Entropy IRL | 以最大熵轨迹分布拟合示范偏好；概率是行为模型概率，不是事故概率 |
| Levine & Koltun, 2012，Continuous IOC | 在局部最优轨迹附近用连续 reward 导数 / Hessian 解释示范；人类偏好可以包含激进风格，不自动符合规范安全 |
| CBF-QP, 2017 | 连续 safety margin 定义安全集，并在动力学和可行控制假设下保持前向不变；把 margin 当惩罚项不等于保留硬约束 |
| HJ reachability, 2017 | 值函数界定规定时域和扰动下的可达 / 安全集；计算复杂度高，不是学习出来的碰撞概率 |
| RSS, 2017/2018 | 以反应距离、制动能力、责任规则定义安全距离和 proper response；结论受参数、模型和参与者行为条件约束 |

第三轮传统方法审计共核读 13 篇，另登记 6 篇待补读入口。尚未全文核读的方向包括 Werling Frenét 轨迹生成、Blackmore 机会约束路径规划、Maximum Margin Planning、Kuderer 驾驶风格学习、另一版本 CVaR 风险规划及 Driving Safety Field 2015。它们不能按“已精读”引用。

### 3.4 端到端 / WAM 的奖励、评价器和 benchmark 相关文献

第二轮专题共精读 15 篇。它们提供了“训练 / 规划中如何用分数”的参照；绝大多数不是新 benchmark 论文，也不能都叫风险场方法。

| 论文 | 与评价 / 风险场构想的关系 | 审计边界 |
|---|---|---|
| NAVSIM | 以驾驶规则分项和聚合分数评价规划；PDM 规则也可用于候选筛选 | 本轮分析了指标定义与静态实现，未据此证明阈值化导致任何模型训练失败 |
| WAM-Flow | 用 NAVSIM 相关 reward 做 GRPO 训练；连续 token 几何与硬评价 reward 是不同环节 | GRPO 不需要 reward 对轨迹求导；全组同分可能使相对 reward 优势变弱，但属于需看采样分布验证的问题 |
| DriveSuprim | EMA teacher 软标签自蒸馏，保留硬规则监督；针对硬评价边界的学习稳定性 | 软标签不是物理风险概率，不是新官方指标 |
| ReWorld | 用低分候选近邻的排斥目标，修改生成模型 | 不是将 NAVSIM 指标平滑化，也不保证排斥方向等于安全方向 |
| DA-WAM | 当前场景 + 候选 + 候选条件 future latent → 子分数与 utility → 选轨迹 | 已有在线候选评价器；反事实 future 的真实性监督有限 |
| Hydra-MDP | 将 oracle 子项学习进学生评分器，再组合规则与模仿成本 | 是规则代理评分器；网络拟合与官方规则、部署选择是不同环节 |
| DrivoR | 显式把解码轨迹几何送入 scoring decoder，预测多个评价组件并组合 | 评分器设计能影响泛化；分数不是校准概率或安全证明 |
| TOAD | 用冻结 learned scorer 驱动 CEM 在控制空间搜轨迹 | 直接展示“排序正确”不保证“被优化器搜索时仍可靠”；会出现 scorer exploitation / 优化退化 |
| Gen-Drive | 偏好 reward 用于候选选择及策略更新 | reward 可能被更新后的策略利用；偏好模型与真实驾驶评价仍需验证 |
| WoTE | 候选轨迹驱动 BEV future rollout，再预测奖励组件并选轨迹 | 在线候选未来与 reward 已有先例；不等同物理 RiskField |
| WorldDrive | world teacher、PDM oracle 和 FAR learned reward 分工 | learned scalar scorer 可部署，但不因使用 world model 就自然成为风险概率场 |
| Think2Drive | privileged 训练信息下的模型内 reward / 长期 value | 需区分训练可见信息、在线输入和最终安全语义 |
| RiskWorld | 研究风险来源 / 风险预测等信息 | 它关注的任务不能直接当成候选 ego 轨迹风险评价器 |
| Vista | 以视频生成不确定性 / 方差作为行为代理之一 | 不确定性信号不等于碰撞风险校准 |
| CRAFT | 分析并修正反事实 proxy reward 偏差 | 说明代理奖励可能有结构偏差，不是具体场函数 |

与 benchmark / 评测创新直接相关的先例另有：

- **NAVSIM v1 / v2**：benchmark 内容、仿真与分数设计；v2 pseudo-simulation 通过两阶段协议补充部分闭环一致性分析。
- **Bench2Drive**：CARLA 场景化反应式闭环、多能力覆盖及统一评测协议。
- **nuPlan**：闭环规划 benchmark、场景挖掘和分类。
- **StyleDrive**：在 NAVSIM 指标底座上引入风格条件 / 风格化评分，是近期组会提到的“修改已有评价体系并在多个模型上验证”的直接启发。

风险场专项检索还未补齐，因此这张表是**相邻研究地图**，不是所有驾驶 risk-field 论文的穷尽表。

## 4. 风险场若迁到端到端 / WAM，可以接在哪

先明确输入输出：风险场模块至少需要一个场景 \(s\)、一个 ego 候选轨迹 \(\tau\)，以及交通参与者的状态或未来假设；返回的可以是沿轨迹的风险序列 \(r_t\)，再汇总成 peak、积分、超限时长、裕量或风险概率等。若只根据当前状态查询一处场值，它还不是完整的轨迹评分器。

### 4.1 五种连接位置

| 接入位置 | 实现思路 | 是否要重训 | 适用条件与主要风险 |
|---|---|---|---|
| 评价 / 诊断层 | 固定模型输出不变，离线计算 RiskField 指标，与 PDMS、TTC、碰撞和人工标注并列报告 | 不需要 | 最容易启动；只改评价，不会让模型行为变好。要证明新增量能区分或解释真实有意义的轨迹差异 |
| 候选 reranking / scorer | 对一组已生成候选逐条算风险，与原分数加权或分层排序后选一条 | 解析式直接打分可不重训 | 要有多条候选；官方 future 可用于离线 oracle 分析，但部署必须用可获得的预测 / 反应式环境，不能偷看未来 |
| 训练 reward / cost | 把场值或轨迹聚合风险加入 imitation、偏好排序或 GRPO reward | 通常需要重训 / 再训练 | 能影响输出行为；权重、量纲、奖励冲突与 reward hacking 都要处理；奖励上升不等于独立 benchmark 改善 |
| 模型输入 / 中间特征 | 生成风险热图、对象级风险 token 或候选条件风险特征，送入 encoder、waypoint query 或 scorer | 通常需训练或微调 | 更像模型机制创新，但与不同骨干绑定，数据接口及表征适配工作较多 |
| 轨迹优化指导 / 安全层 | 用解析梯度、采样搜索、CEM、CBF / RSS 约束调整候选或做输出过滤 | 取决于方案 | 需要可微 / 可优化接口或额外优化器；风险评分不等于安全证明，运行时与 fallback 需要专门评估 |

可从最便宜的一端开始：先把风险场当**固定模型的补充评价量**，再尝试对模型现有候选做**无训练 reranking**。只有确认它确实捕捉到当前指标遗漏的轨迹差异，且 reranking 有收益，再决定是否进入 reward 或网络结构。

### 4.2 对不同 WAM 结构的初步匹配

- **天然包含候选评分 / 选择链条的模型**：WoTE、World4Drive、WorldDrive、DA-WAM、DrivoR、Hydra-MDP，以及用搜索器优化 scorer 的 TOAD。可以在 scorer 输入或分数融合处做原型，也可先用固定场做外部 reranking。主要风险是与原 reward 重复计分、候选 future 可信度不足、评分器分布外被利用。
- **主要直接生成轨迹 / action 的模型**：WAM-Flow、SimWAM、LAW、Epona、DriveLaW、Metis 等。可能接在 RL reward、候选采样后处理、辅助 trajectory loss 或生成过程 guidance；若部署只输出一条轨迹且没有候选采样，单纯 reranking 无入口。reward / loss 接法大多需要重新训练。
- **候选或 waypoint 与未来表征耦合的模型**：Drive-JEPA、DynFlowDrive 等可探索把风险量作为候选条件信号、waypoint 周围局部特征，或 future latent 的辅助评价；但不能仅因模型已预测未来，就认为它已掌握正确的安全风险。具体是否适合必须看其实现和部署链路。
- **SimWAM 的关联**：近期读了 SimWAM，并完成官方 RL checkpoint 的 NAVSIM v1 评价，PDMS 91.9036，与论文报告 91.9 一致。这个结果说明团队已具备一个可用的 WAM + RL 评测参照；它不是 RiskField 接入的证据，也没有证明风险场会提升 SimWAM。

这只是按机制结构作的**接入点假设**，不是对上述模型代码逐篇完成集成审计。尤其“模块在不同架构中热插拔”需要定义统一输入输出与模型侧 adapter；不能默认只把同一段代码拷入就等价。

## 5. 关键技术问题与当前判断

### 5.1 未来信息：训练、离线评价和在线部署必须区分

离线数据集通常提供记录的其他交通参与者轨迹。评估一条 ego 轨迹时，用真实未来 agent 轨迹计算风险，可作为**oracle 后验诊断量**；但模型在线决策时不可预先知道该未来。把真实未来场直接提供给部署评分器，会产生未来信息泄漏。

合理的实验至少区分：

1. **Oracle / 记录未来风险**：用于离线评测、标签构造或上限诊断，明确标为 oracle。
2. **预测未来风险**：以模型可获得的 agent prediction / world model 情景作为未来输入，同时评估预测误差与风险偏差。
3. **反应式闭环风险**：在其他 agent 会对 ego 行为作出响应的环境中测试长期影响；仅记录未来轨迹的开环风险不能替代。

概率版本还需要说清随机性来自环境行为、感知误差还是 world model，多情景概率是否校准，场与严重程度分别是什么。否则高斯热度只能称为 risk score / risk cost，不能写成 probability of collision。

### 5.2 是否跨模型提升

不能预设“每篇论文都提升”。同一个附加项可能：

- 在原评分器忽略近距离风险时，改善保守安全；
- 与既有 NC / TTC / collision cost 重复，带来过度保守或降低进度；
- 模型没有多候选输出时，无法无训练接入；
- 在某一数据 / 模型上有效，但对另一个输出分布不匹配；
- 提升新增风险分数，却使官方 PDMS、反应式闭环或通行效率变差。

因此跨模型验证要报告各模型分项结果和失败案例；允许“某些模型有效、某些不适配”，并分析差异。跨架构结果如果一致，能支持可复用性；若不一致，也能揭示接入机制的边界。

### 5.3 计算效率和资源估算

在有 \(N\) 个候选轨迹、每条采样 \(T\) 个时刻、每时刻 \(M\) 个交通对象时，朴素轨迹评分大致与 \(N\times T\times M\) 成正比。实际代价取决于场是解析点查询还是栅格热图、是否预测多个未来情景、候选是否共享对象状态、实现是否向量化 / GPU 化。

可能的省时方法包括：一次性缓存每帧 agent 状态、批量算多候选、只在轨迹采样点查询解析场、共享静态场，及先用低成本筛选再对少数候选精算。若每个候选还 rollout 一套 agent future，成本会进一步增大。

**当前没有任何可信的实际毫秒数、显存 / GPU 需求、重新训练时长或跨模型工时估计。** 这些要先在现有脚本与一个代表性基线上 profile；不能在文档中给出推测数值冒充测量结果。

### 5.4 “平滑”不是充分条件

连续场可能仍有饱和、梯度很小 / 很大、方向不连续、局部极小值或参数敏感性。一个标量排序器也可能被优化器找到漏洞。硬约束、事件概率、裕量 cost、尾部风险、IRL 偏好回答不同问题，不能用“更连续”笼统代替“更合理”。

前期讨论的重要边界：

- CHOMP / TrajOpt 的连续几何 cost 不能自动变成动态交通事故概率。
- CVaR 必须先定义随机损失及其单位；对二值 collision 做 CVaR 不会凭空获得事故严重程度。
- IRL 学的是能解释示范的偏好，不会自动知道规范安全。
- CBF / HJ / RSS 的硬安全结论依赖模型、初始状态、动力学、控制可行与响应条件；把这些量加入 WAM reward 不会保留同样的保证。
- “连续 cost 可优化”“模型评分准确”“最终控制安全”是三项不同主张，需各自验证。

## 6. 推荐的验证路径：从指标审计到架构迁移

这是根据现有讨论整理的推进顺序，不表示实验已经执行。

### 阶段 A：固定模型，先验证指标是否提供新信息

1. 固定场景、候选轨迹、参考协议与官方 NAVSIM scorer。
2. 设计成对轨迹：都未碰撞但 clearance 不同；最大距离近似但暴露时长不同；同类违规但程度不同；前向与横向接近；单一危险对象与多个中风险对象。
3. 逐对比较 PDMS / EPDMS 原始分项、RiskField 时间序列、peak、积分 / 暴露率、TTC、碰撞标签。
4. 检查单调性、阈值敏感性、时域与采样变化、场参数敏感性、重复场景稳定性。
5. 对新增指标明确“它期望奖励哪种行为，以及在什么场景下不应该奖励”；由此判断它是 benchmark 诊断量、训练目标，还是二者都有候选价值。

这一步不训练模型，可以快速排除“数值更丝滑但没有新增判别信息”的场定义。

### 阶段 B：固定候选，做离线风险评分与 reranking

1. 用同一模型生成候选池，先比较官方 scorer 排序与 RiskField 排序 / 融合排序。
2. 将真实 agent 未来仅作为 oracle 上界诊断；另做可部署 agent prediction 版本。
3. 对 reranking 前后在 NAVSIM 官方总分 / 分项、安全裕量、进度、舒适度上做配对比较。
4. 报告场景类型、失败案例、推理额外时延。只在一个评分 / 候选基线完成上述测试后，再扩展第二个架构。

### 阶段 C：再进入训练信号或网络结构

仅在 A/B 证明存在明确缺口后，选择一个训练接口：

- RL：把场值 / 沿轨迹 risk 积分作为额外 reward，固定原 reward 与 KL / sampling 设置，对权重和组内区分做消融。
- imitation / ranking：将风险用于成对偏好、硬例标签或辅助损失，检查风险标签质量及与专家行为冲突。
- 结构输入：加入对象风险 token / 热图 / candidate risk embedding，分别看其是否需要特定骨干改动。
- safety shield / constrained optimization：把硬约束与软偏好拆开，单独验证可行性和 fallback。

需要保留官方 benchmark，报告训练成本、样本效率、重复种子、各分项变化和独立反应式闭环结果；避免只在被优化的单项上自证。

### 阶段 D：跨架构验证“可复用”

若目标是跨多个 WAM 的通用模块，先约定统一的风险接口与 adapter，再选机制差异较大的两个模型：
- 一个含显式候选评分 / selection，例如 WoTE、DA-WAM 或 DrivoR；
- 一个直接 action / trajectory policy，例如 SimWAM 或 WAM-Flow。

先测无训练后处理能否复用，再测训练信号能否复用。报告每个 adapter 改了哪些模块、是否冻结、额外参数量、训练步骤、推理耗时，不能把“理念相同”说成“热插拔实现相同”。

## 7. 候选研究贡献如何表达

在直接文献检索补齐之前，可以保留以下候选表达，不把其中任何一个写成既定创新：

1. **补充型评价指标**：对官方 PDMS / EPDMS 附加可解释的风险裕量、峰值和暴露时长，改善对细粒度差异的诊断；公共 benchmark 主分数保持可比。
2. **训练奖励完善**：在原奖励或硬门控旁加入具有明确语义的风险程度信号，验证对学习效率与独立驾驶质量的作用。
3. **候选轨迹评价 / 排序**：用风险场辅助多个候选的选优，区分 oracle 风险分析与在线可用评分。
4. **跨架构可复用模块**：为多种候选评分 / 直接生成模型定义风险输入输出接口和轻量 adapter，分析为何在不同模型上效果不同。
5. **风险表示迁移或改进**：比较椭圆高斯、距离 / 势场、概率风险与不确定性风险，说明所选择的表示表达了什么风险、依赖什么假设。

这些方向可以各自独立，也可以分阶段组合。“风险场 + 某个 WAM”不是唯一选项。仅仅把一个已有 Gaussian field 加进网络，若没有清晰研究问题和有效对照，贡献会偏弱；反过来，在已有场或指标上作扎实完善、揭示模型间适配规律，也可能形成有价值的创新。

## 8. 当前决策、未决项与范围边界

### 已经有据可查

- 对 NAVSIM v1 / v2 的评分组成及部分代码实现做过指标审计，构造过算术反例来说明分项阈值、gate、归一化和跨阶段聚合可能压缩或改变差异。那些反例是定义上的 toy arithmetic，不是仿真结果。
- 第二轮精读 15 篇 WAM / 学习型奖励、评价器与候选选择论文。
- 第三轮传统专题核读 13 篇，另有 6 篇待补读入口。
- 读过用户提供的风险场计算与渲染脚本，并整理出计算方式、输出统计和待核假设。
- 团队已用 SimWAM 官方 RL checkpoint 得到 NAVSIM v1 PDMS 91.9036，与报告值 91.9 一致；该验证为风险场实验提供了一个可能的基线条件，不是风险场实验结果。

### 尚未做完

- 没有完成 E2E / WAM × risk field 论文的系统检索、去重与机制分类。
- 没有在 NAVSIM 轨迹上运行当前 RiskField 脚本并给出实测相关性或有效性结论。
- 没有将风险场接入任何 WAM，没有重训或做推理侧 reranking。
- 没有比较 Gaussian、碰撞概率、引力 / 排斥势、风险预测分布等版本。
- 没有完成 runtime / 显存 / 训练资源测量。
- 没有决定是否把主论文定位为 benchmark 指标、训练奖励、网络模块或跨模型统一接口。
- 没有证明风险场在所有模型上提升，也没有证明 NAVSIM 的硬评分是任何已知训练退化的原因。

### 后续调研最该回答的问题

1. 端到端规划和 WAM 论文里，有哪些直接把风险场、势场、安全距离场、碰撞概率场或风险地图用于监督、候选排序、planning cost、RL reward、在线控制？
2. 它们各自用什么风险源、未来假设、聚合方式？部署是否使用真值未来、预测未来或反应式 simulator？
3. 它们验证的是指标区分度、离线规划质量、闭环性能、事故概率校准，还是仅 benchmark 分数？有什么共同缺口？
4. 我们现有 Gaussian RiskField 与这些工作具体重合在哪里，哪些改动是实质改进 / 合理迁移？
5. 在现有数据、GPU 与官方模型复现基础上，最低成本的验证应从固定轨迹评价还是一个模型的 reward/reranker 开始？

## 9. 复盘后的总判断

这项工作已经积累了两类可用资产：一是对 NAVSIM 指标结构和评价信号文献的审计；二是一个可计算、可视化的高斯风险分析原型。二者之间目前还隔着一段关键证据链：

**风险定义是否适合 → 它补充了现有评价没有保留的哪种差异 → 哪个模型接口能使用它 → 使用后的行为是否在官方及独立评测中更好。**

现在最稳妥的研究动作不是预先承诺“所有模型提升”，而是先补齐直接应用文献地图，并用固定轨迹 / 固定候选验证 RiskField 是否确实带来新增且方向合理的信息。若成立，再选最易接入的模型做低成本原型，随后才讨论跨架构通用模块。此推进顺序保留了风险场想法的开放性，也使得后续即使最后选择的是另一个指标或评价机制，前面的调研和验证仍然有复用价值。

## 参考资料与复查入口

### 已形成的审计底稿

- trajectory_evaluation_round2_deep_read_CN.md：15 篇相关论文的机制精读、训练 / 部署边界和证据限制。
- trajectory_evaluation_round3_traditional_CN.md：13 篇传统路线专题核读及 6 个未完成全文核读的补充条目。
- trajectory_evaluation_round4_optimization_audit_CN.md：评分器 / 搜索的一次有限静态代码审计。
- trajectory_evaluation_round5_metric_audit_CN.md：NAVSIM 指标语义、区分能力、聚合与 toy counterexample 审计。
- ly05_eval_riskfield.py、ly05_v8_render.py：本复盘所述风险场离线分析与可视化工具。

### 主要原始文献

- Khatib, Real-Time Obstacle Avoidance for Manipulators and Mobile Robots (1986): https://khatib.stanford.edu/publications/pdfs/Khatib_1986_IJRR.pdf
- CHOMP (2009): https://www.cs.cmu.edu/~mzucker/icra09-chomp.pdf
- CHOMP, IJRR version (2013): https://publications.ri.cmu.edu/storage/publications/pub_files/2013/5/CHOMP_IJRR.pdf
- TrajOpt (2013): https://www.roboticsproceedings.org/rss09/p31.pdf
- Human-like driving behaviour emerges from a risk-based driver model / DRF (2020): https://www.nature.com/articles/s41467-020-18353-4
- Chance Constrained Finite Horizon Optimal Control with Nonconvex Constraints (2010): https://groups.csail.mit.edu/mers/old-site/papers/ono_acc10.pdf
- Wasserstein Distributionally Robust Motion Control with CVaR (2020): https://arxiv.org/abs/2001.04727
- Distributionally Robust Risk Map (2021): https://arxiv.org/abs/2105.00657
- Apprenticeship Learning via IRL (2004): https://ai.stanford.edu/~ang/papers/icml04-apprentice.pdf
- Maximum Entropy IRL (2008): https://www.cs.cmu.edu/~bziebart/publications/maximum-entropy-inverse-reinforcement-learning.pdf
- Continuous Inverse Optimal Control (2012): https://arxiv.org/abs/1206.4617
- Control Barrier Function QP (2017): https://arxiv.org/abs/1609.06408
- HJ reachability tutorial (2017): https://arxiv.org/abs/1709.07523
- RSS (version 6, 2017/2018): https://arxiv.org/abs/1708.06374
- NAVSIM official metric code, frozen SHA: https://github.com/autonomousvision/navsim/tree/0a380a9063d7162ec93d0f51e9990ebac585f720
- WAM-Flow source note, frozen research-repo SHA: https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md/P0074_WAM-Flow/P0074_WAM-Flow.raw.md
- 第二轮 15 篇论文的仓库原文入口（冻结 SHA cb05048dfb822e95d44e52dd85b830c750411e2c）：
  - NAVSIM： https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md/P0032_NAVSIM/P0032_NAVSIM.raw.md
  - WAM-Flow： https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md/P0074_WAM-Flow/P0074_WAM-Flow.raw.md
  - DriveSuprim： https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md/P0022_DriveSuprim/P0022_DriveSuprim.raw.md
  - ReWorld： https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md/P0052_ReWorld/P0052_ReWorld.raw.md
  - DA-WAM： https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md/P0012_DAWAM/P0012_DAWAM.raw.md
  - Hydra-MDP： https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md/P0021_HydraMDP/P0021_HydraMDP.raw.md
  - DrivoR： https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md/P0060_DrivoR/P0060_DrivoR.raw.md
  - TOAD： https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md/P0010_TOAD/P0010_TOAD.raw.md
  - Gen-Drive： https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md/P0006_GenDrive/P0006_GenDrive.raw.md
  - WoTE： https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md/P0045_WoTE/P0045_WoTE.raw.md
  - WorldDrive： https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md/P0042_WorldDrive/P0042_WorldDrive.raw.md
  - Think2Drive： https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md/P0027_Think2Drive/P0027_Think2Drive.raw.md
  - RiskWorld： https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md/P0005_RiskWorld/P0005_RiskWorld.raw.md
  - Vista： https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md/P0038_Vista/P0038_Vista.raw.md
  - CRAFT： https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md/P0017_CRAFT/P0017_CRAFT.raw.md
- DriveSuprim: https://arxiv.org/abs/2506.06659
- NAVSIM v2 pseudo-simulation: https://arxiv.org/abs/2506.04218
- Bench2Drive: https://arxiv.org/abs/2406.03877
- nuPlan learning-based planning benchmark: https://arxiv.org/abs/2403.04133
- WoTE: https://arxiv.org/abs/2504.01941
- StyleDrive: 组会讨论中所用 SM-PDMS 对照数据见本轮对话中用户提供的实验摘录；后续正式引用前应补齐论文准确版本和原始表格链接。

## 证据口径说明

本报告把内容分成四类：原论文 / 代码中可直接核对的机制；脚本静态阅读所得；从已有研究抽取的迁移推论；尚未验证的构想。凡涉及“性能会提高”“某字段足以校准概率”“所有 WAM 可热插拔”等内容，目前均属于待检验假设。报告没有宣称新增文献已穷尽，没有把 toy arithmetic 当场景实验，也没有把公开 checkpoint 的 NAVSIM 成绩当风险场效果。
