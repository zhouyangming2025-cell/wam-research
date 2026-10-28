# 风险场文献库 Markdown 普查、建模证据与 GitHub 既有研究交叉核对

日期：2026-10-27 | 状态：**阶段性研究证据，不是最终分类或新主任务**

## 0. 范围与来源

- 来源：用户在 ChatGPT 会话上传的 `all_md.zip`，为独立本地风险场文献库 MinerU 转写稿。
- 原始本地工作区：`D:\zym_information\ZYM\wam\workspace\风险场\mineru`；工作成果原计划目录：`D:\zym_information\ZYM\wam\workspace\风险场\audits`。
- ZIP SHA-256：`8f4030ced23eb68de7b55396fbe66369b3009944b28011fd936f4ab318f501dd`，大小 6,264,174 字节。
- 本次从 ZIP 实读 Markdown，未取得其中引用的图片文件，也未为所有论文重新查原始 PDF。
- 本文是独立专题历史证据；不更改 WAM 项目 `state/CURRENT_STATE.md` 或 `state/NEXT_TASK.md`，不替代其 P0013 BridgeSim 当前工作入口。

## 1. 实际盘点数据与审计层次

| 项目 | 当前数量 | 证据程度 |
|---|---:|---|
| Markdown 文件 | 299 | ZIP 文件清点 |
| 内容 SHA-256 不同 | 277 | 字节级去重 |
| 规范化主标题归组 | 264 | 暂定论文身份；并非严格 DOI/作者去重 |
| 多个 MD 共享同标题 | 34 组 | 有 13 组同标题不同字节内容；保留版本区别 |
| A 类（原创或改进风险场） | 61 | **初步相关性**，非逐篇全文人工验证 |
| B 类（风险场应用） | 29 | **初步相关性** |
| C 类（相邻风险/通用 APF） | 100 | 尚待可迁移模型甄别 |
| D 类（外围或误收） | 74 | 可能存在需复核的误排除 |
| A/B 方法原文证据档案 | 90 | 来源行号、公式、场源/时间/聚合/下游候选片段 |
| A/B 正文展示公式块 | 1,978 | 机械抽取，非全都是场本体公式 |
| 入选自动建模候选公式 | 1,014 | 自动筛选，非已全部审核核心式 |
| 关键方法来源核读卡 | 34 | 核读有限核心公式及机制，不是全公式穷尽审计 |

质量限制：`P0156` 在重点卡中未找到计划核验的核心原始公式，应标记 `NEEDS_REVIEW`；原始图缺失，一些 MinerU LaTeX 存在重复 `\tag` 等噪声。版本合并基于标题而非全面 DOI/作者辨识，264 不可对外写成“264 篇独立论文已确认”。

## 2. 已核读方法的关键分界

| 论文库局部 ID | 代表模型 | 风险场/时间语义 |
|---|---|---|
| `P0028` | Driver's Risk Field (DRF) | 自车驾驶者沿预期路径的二维主观风险分布；使用 look-ahead 并不等价于 ego–周车同刻未来占用 |
| `P0126` | EDRF | 多模态预测路径投影为二维风险带，未来路径信息与碰撞时刻一致性必须分开讨论 |
| `P0071` | P-PDRF | 预测碰撞可能性/后果严重度随未来时刻聚合，不应等同普通空间势能 |
| `P0181` | STRF | 编织区时空等效距离风险场，显式处理时间差，但等效时距的物理接触语义需另证 |
| `P0199` | DRIFT | 对流/扩散/源项/衰减形成时间演化 PDE 风险场；不是自带轨迹碰撞概率 |
| `P0216` | READ | 高斯基函数叠加构成可微的 `R(x,y,t)`；连续场查询不自动保证时域采样无漏峰 |
| `P0213` | MC-Risk | 预测路径机动车场 + VRU 场 + 道路惩罚场，供 ego 轨迹/MPC 查询 |
| `P0194` | 双阶段换道动态场 | `R(s,d,t)` 随未来周车位置变化；轨迹聚合和连续时间安全仍需单独核对 |
| `P0198` | DRiF | 数据驱动、ego-conditioned 的风险表征，需区别于手工高斯势场及校准碰撞概率 |
| `P0145` | RiskMap | 可微的规划成本/风险图与多模态预测耦合，须区分预测时间与代价时序 |
| `P0219` | RiskWorld（Flow-Guided Occupancy 版） | 风险核 + 未来占用 + 候选轨迹筛选，须查清实际进入候选排序的是哪个模块 |
| `P0171` | 预测离散时空风险图 | 按未来离散时刻分别建立风险图，不等于连续时间接触保证 |

全部 34 个局部 ID 的机制核读文件和完整原始公式行号保存在会话交付包 `风险场全库建模审计_阶段交付_20261027.zip` 中，**本分支仅归档阶段结果和交叉核对依据**。该文件不是公开外链，未来迁移请依据上面的源 ZIP 哈希及本地工作目录。

## 3. 与此前 wam-research 证据的关系

本次实际读过以下已有文献，禁止将其中可信的旧证据当作新发现重新计数：

1. [`audits/literature/TRAJECTORY_RISK_CRIME_GDRF_IR_SOURCE_AUDIT_20261012.md`](../../audits/literature/TRAJECTORY_RISK_CRIME_GDRF_IR_SOURCE_AUDIT_20261012.md)：此前已有 IR/EDRF/GDRF 对照、当前状态二维场与时间同步的边界，以及 CommonRoad-CriMe 的实现级语义审计。
2. [`papers/deep_analysis/P0005_RISKWORLD_DEEP_ANALYSIS_V2.md`](../../papers/deep_analysis/P0005_RISKWORLD_DEEP_ANALYSIS_V2.md)：已有历史条件对象风险识别的 RiskWorld 深度审计，其未来关系预测不接受 ego 候选行动条件。

**特别注意两篇不同 RiskWorld：**

- 此次本地库 `P0219`：*RiskWorld: Risk-Aware World Modeling with Flow-Guided Occupancy Evolution for Selective Trajectory Planning in Automated Driving*。
- 仓库旧 `P0005`：*RiskWorld: Object-Centric Latent World Modeling for Autonomous Driving Risk Identification*。
- 二者题名/模型/任务均不同；**本地 Pxxxx 与仓库 Pxxxx 属于不同编号命名空间，绝不能将两者的 P 编号直接联接**。

针对 IR/GDRF，本次 ZIP 的正文未找到 `IDRF`/`GDRF` 关键词，因此不要误称本次全库覆盖了 IR 与 GDRF 完整原式；继续沿用仓库旧审计的来源限制，待找回原文再提升证据等级。

## 4. 未完成的审计任务（历史事实，不修改主状态）

- 90 篇 A/B 中，56 篇目前只有自动筛选证据，没有来源核读的语义卡；34 篇核读卡也只覆盖重点式子。
- 所有 A/B 需进一步核验模型本体与下游规划目标之间的公式接口，避免错把速度条件的二维场当作可校准的未来碰撞概率。
- C 类共 100 组尚未针对“有实质风险建模迁移价值但无 risk field 关键词”进行二次召回检查。
- 对缺图、公式断裂、场源/评价对象含混的论文，应按最小原 PDF 页回查，而非猜补 LaTeX。
- 独立二次盲审、完整公式闭合验证、全部论文 DOI/版本归并均未完成。

## 5. 可复用的数据结构

会话生成的压缩包含以下文件，迁回本地研究目录时保留原名与 CSV 编码：

- `PAPER_IDENTITY_AND_RELEVANCE.csv`：264 个候选论文组、初步相关性与主 Markdown SHA。
- `ALL_MARKDOWN_VERSIONS.csv` / `DUPLICATES_AND_VARIANTS.csv`：版本与去重证据。
- `FORMULA_EVIDENCE_INDEX.csv`：所有 A/B 展示公式的原文行号与上下文。
- `MODEL_AUDIT_INDEX.csv`：90 份原文证据档案的状态。
- `evidence_audits/Pxxxx.md`：源行可回查的原样公式摘录。
- `reviewed_model_cards/Pxxxx.md` / `REVIEWED_MODEL_SEMANTICS.csv`：34 份有限范围机制审计。
- `REVIEW_QA.csv` / `GITHUB_PRIOR_WORK_CROSSWALK.csv`：阶段 QA 与跨仓库身份纠错。

最终原则：严格区分 `SOURCE_EXTRACTED`、`CORE_METHOD_SPOT_REVIEW`、`FULL_FORMULA_VERIFIED`，本轮没有任何依据声称已经完成 264 篇的完整数学复核。

## 6. 数学机制核读批次 B2（2026-10-27；8 篇 / 57 个原始公式块）

原始证据：用户提交 `all_md.zip` 中相应 MinerU Markdown；57 个公式块均已精确定位、原样抽取并确认在源 Markdown 出现，无行号定位失败。**这只表示 MD 来源一致性，不等于 PDF 视觉验收、完整模型参数验证或独立实验复现。**

| paper_id | 原始机制 | 对固定候选风险评价的边界 | 逐篇证据 |
|---|---|---|---|
| P0082 | 逆距离静态场 + 指数相对方向速度动态场 + 分离车身圆碰撞检查 | 势场引导与真实几何接触是不同模块；源距离向量疑误 | [卡](riskfield_models/P0082_MECHANISM_AUDIT.md) |
| P0086 | 前后分段伪距离、四次横向量、虚拟风险质量与 co-force | ν=0 / ν=νm 下分母需退化处理；非未来同刻风险概率 | [卡](riskfield_models/P0086_MECHANISM_AUDIT.md) |
| P0091 | 认知失误→主观风险图、和客观图比较警报 | 并未提出独立风险场本体；B 类应用而非 A 类原创 | [卡](riskfield_models/P0091_MECHANISM_AUDIT.md) |
| P0092 | 尺寸各向异性静态高斯 + 动能/驾驶风格场 + 控制约束 | 单独动能项不区分车间距离，动态约束并非风险核的时空同步 | [卡](riskfield_models/P0092_MECHANISM_AUDIT.md) |
| P0111 | 高斯障碍核的停车距离尺度 + 纵向 TTC 提前换道 | `abs(v_rel)` 丢失追近方向；是控制程序增强，不是新概率场 | [卡](riskfield_models/P0111_MECHANISM_AUDIT.md) |
| P0121 | **每个未来时刻**的多模态周车旋转高斯场 + ego MPCC 查询 | 时间步对应关系和两层 γ 折扣需查原始符号/代码 | [卡](riskfield_models/P0121_MECHANISM_AUDIT.md) |
| P0140 | 车身伪距离类库仑场、环岛 DENCLUE 聚类风险 | 反距离奇异；MD Eq.(12) 失真、下标角色存疑 | [卡](riskfield_models/P0140_MECHANISM_AUDIT.md) |
| P0143 | 经验 ETA 分段风险映射 + 4D 锚节点风险占用图 | **Eq.(2) ETA=3s 左0.2008、右0.5，不连续**；非碰撞概率 | [卡](riskfield_models/P0143_MECHANISM_AUDIT.md) |

本批可直接证实的结构性区别：风险核为状态条件空间场、逐未来时刻预测场、主观驾驶员错误场、系统级宏观风险场，不能根据“potential/risk”同名合并。B2 的完整 57 个源公式、邻近文字、行号和候选衍生反例以会话交付 `BATCH2_MATH_AUDIT.zip` 保存；GitHub 8 张卡已保留核心公式但**未镜像所有 57 个完整公式块**。

**尚未完成：** 以前列出的56篇是旧阶段基线而非本轮剩余数（中间已有额外核读）；继续按 `PAPER_IDENTITY_AND_RELEVANCE.csv`、`AUDITED_MODEL_SEMANTICS_NEW.csv` 与新增卡共同去重判定当前状态。当前 B2 不改变其余论文的质量等级，也未完成剩余 C 类全库复核。

此文仍是风险场独立专项记录，不修改 `main` WAM 工作状态或混入非风险场 WAM 论文。

### B2-1. 可证明的同核特例：P0092 静态障碍高斯 ≈ P0121 单时刻单模态高斯

这是**本研究的符号代换推导（DERIVED）**，不是任何论文自己的等价性声明。

- P0092 原文 Eq.(5)，MD L85–L87：\(E_{R2}+E(0)=\beta\exp[-\tfrac12(\delta_1\Delta x^2/L^2+\delta_2\Delta y^2/W^2)]\)。
- P0121 原文 Eq.(7)，MD L114–L116：\(\Theta_i^t=\sum_j p_j\exp[-(\Delta x_j^2/a^2+\Delta y_j^2/b^2)]\)。

取 P0121 只有一个模态且 \(p_1=1\)，朝向坐标与 P0092 一致，且 \(a^2=2L^2/\delta_1\)、\(b^2=2W^2/\delta_2\)，则

\[
\boxed{\ E_{R2}(x,y)+E(0)=\beta\,\Theta_i^t(x,y)\ }.
\]

**意义：** 在此受限条件下，二者的单个空间核只差幅值与常数平移，不能仅用“不同高斯公式”声称新的风险信息。然而 P0121 在真实完整算法中具有**时刻索引、周车未来预测模态权重、局部朝向旋转和 ego 预测时域查询**，这些新增输入/计算位置使完整系统**不等价于** P0092 静态障碍场。式子是否原样进入 MPCC 时刻 t+k 仍需查 Eq.(15) 时间下标。

### B2-2. 明确不能做的等价归纳

- P0086 的分段逆伪距离场和 P0140 的类库仑反距离场，不是简单换宽度的高斯核。近零距离的奇异性与 Gaussian 有本质差别。
- P0091 的主观识别错误不等于车辆真实可达性、制动裕量或客观事故概率。
- P0143 的 ETA 分段函数数值跳变，不具有可据以定义“动态安全余量”的全域连续单调性质。

## 7. 统一账本实时快照（2026-10-27 B2 合并）

本次已把旧的 34 张核心机制卡、后续 38 张局部公式核读卡、9 篇 C 类范围复核、本批 8 张数学主链卡按**同一源论文 ID**合并为一个 `MASTER_WORKS_LIVE_20261027.csv`（会话 ZIP 内），**不是将卡片数量简单相加当作独立文献数**。

- 候选独立论文组：264（按题名暂定，未完全 DOI/作者核验）。
- 当前工作分类：A 65、B 39、C 85、D 75；**仍是工作分类，可继续纠偏**。
- 审计层级分别为：8 篇 `METHOD_CHAIN_SPOT_AUDIT`、34 篇 `CORE_METHOD_SPOT_REVIEW`、38 篇 `CORE_FORMULA_SPOT_REVIEW`、9 篇 `C_METHOD_SCOPE_REVIEW`、19 篇 `AUTOMATIC_SOURCE_EXTRACTION_ONLY`、156 篇 `PRELIMINARY_RELEVANCE_ONLY`。这些状态按每篇论文取单一当前最高可用阶段，仍非全文穷尽核验。
- 主账本 264 行；A/B 侧的已有机械公式索引 1,978 行，其中本批 57 个公式块补充了原文精读证据。**1,978 行不等于 1,978 个有独立物理意义的风险公式。**
- 目前**没有**论文可以仅因这些局部卡被标记 `FULL_FORMULA_VERIFIED` 或 `PDF_VISUALLY_VERIFIED`。

后续应继续对工作分类中未完成方法审计的论文做证据升级，不得直接沿用历史的“剩余 56/91”作为实时计数。

**最新可下载源数据：** 本轮会话交付 `BATCH2_MATH_AUDIT.zip` 含统一账本、A/B 公式索引、57 个校验后的原始公式块、8 张逐篇深入卡。上述 ZIP 并未整包同步至 GitHub；GitHub 已长期保存 8 张重点方法卡与本主账本。

## 8. Batch3：11 篇数学机制增量与统一身份分类修正（2026-10-28）

本轮由用户 `all_md.zip` 选取 11 篇未深审风险场/相邻数学机制原文，**确切对比源 Markdown 原样公式 73 个**，ZIP 原文 SHA-256 全部 11/11 通过；**无 PDF 视觉复核或全文穷尽验证**。完整逐篇 formula→roles→time→aggregation→counterexample 在会话生成 `mechanism_batch3_20261028/BATCH3_MATH_AUDIT.zip`，GitHub 已另存 11 张精简重点数学审计卡：`audits/literature/riskfield_models/Pxxxx_MECHANISM_AUDIT.md`。精简卡保留关键公式，其余公式目前仅在 ZIP 中，不能冒称 73 式已逐字镜像 GitHub。

| 局部编号 | 分类 | 核心方法与发现 | GitHub 卡 |
|---|---|---|---|
| P0046 | A | Road User Safety Field：q(T_r,b_max)、ε_R、交互 Risk Force 及后果强度；不是事故概率 | [卡](riskfield_models/P0046_MECHANISM_AUDIT.md) |
| P0113 | **A→B** | 论文明确引用已有风险场；Eq.(16)–(17) 是**候选序号上的碰撞标签高斯平滑**，重排候选可改变分数 | [卡](riskfield_models/P0113_MECHANISM_AUDIT.md) |
| P0138 | A | 车辆场×虚拟质量 + 行人各向异性核 + 道路指数场；若干 MD 式需视觉确认 | [卡](riskfield_models/P0138_MECHANISM_AUDIT.md) |
| P0180 | A（阻塞） | 跟驰相对速度积分和纵向安全域；MD 缺关键原式、e^(−1/v) 在 v=0 未定义 | [卡](riskfield_models/P0180_MECHANISM_AUDIT.md) |
| P0072 | B | SFF claimed-set 安全程序与集合交叠势；不能混为高斯危险密度 | [卡](riskfield_models/P0072_MECHANISM_AUDIT.md) |
| P0097 | B | 已有 DRF 调参数模拟周车干预，生成 critical scenarios，非新的风险核 | [卡](riskfield_models/P0097_MECHANISM_AUDIT.md) |
| P0103 | B | RSS 安全距离尺度 + 遮挡出现的纵/横虚拟力修正；原式有量纲/下标疑点 | [卡](riskfield_models/P0103_MECHANISM_AUDIT.md) |
| P0237 | B | 预测变道意图触发 1D APF，安全时距 l=d0+hv 与换力控制 | [卡](riskfield_models/P0237_MECHANISM_AUDIT.md) |
| P0096 | C 对照 | **每个真实未来时刻** GMM 等值轮廓→轴对齐占用→车辆 Minkowski 膨胀；峰值归一核并非概率密度 | [卡](riskfield_models/P0096_MECHANISM_AUDIT.md) |
| P0124 | C 对照 | 同刻车辆几何碰撞 Monte Carlo；`max_t P(col at t)` **不是** `P(∪_t collision_t)` | [卡](riskfield_models/P0124_MECHANISM_AUDIT.md) |
| P0163 | **C→B** | FlowDrive 真实构建 BEV Gaussian 风险/车道吸引场，嵌入 end-to-end 特征，不是原创新风险核 | [卡](riskfield_models/P0163_MECHANISM_AUDIT.md) |

**当前合库工作分类更新**：A 64、B 41、C 84、D 75（合计 264 标题候选组；**不是已 DOI 核定的 264 篇独立论文**）。上一版 A65/B39/C85/D75 已被上述两项有原文证据的分类改判取代。

### Batch3 实质性数学结论

1. *索引空间 vs 物理空间*：P0113 `g(u-k)` 的 `u,k` 是候选列表编号，P0163 `U_risk(u,v)` 的 `u,v` 是 BEV 位置。二者即使用 Gaussian 核，也不是同一空间运算。
2. *峰值归一 ≠ 概率密度*：P0096 的 GMM 每分量除其最大值后，累计积分一般不等于1；阈值 ε 控制等势轮廓保守性，不是自动事故概率保证。
3. *逐时刻事件概率最大值 ≠ 时域并集概率*：P0124 对两个独立各 0.2 的碰撞事件返回 max=0.2，而并集 P=0.36。已明确数值反例，不能改写作者原始 max 公式。
4. *响应能力作为物理输入*：P0046 q(T_r,b_max) 提供纯距离势没有的人员/车辆能力变量，但经验参数会决定 q 随 T_r 的方向；需要在确定参数号及原 PDF 后才可声称严格单调。
5. *安全程序潜势 vs 经验危险分数*：P0072 SFF 取安全控制程序可达集合的交叠，不可与高斯风险幅度在物理解释或保证层面等价。

本批未新增研究代码或训练，不修改 WAM 主项目状态。此账本是唯一专题总览入口，链接到局部详细机制卡；未经 PDF 核实的 MinerU 疑点保留 `PDF_REQUIRED`。

## 9. Bulk50：50 篇 / 48 篇有原始展示公式 / 1,273 个公式块（2026-10-28）

**[转入本轮唯一增量公式索引](RISKFIELD_BULK50_FORMULA_AUDIT_INDEX_20261028.md)**。基于 `all_md.zip` 与既有规范化身份及哈希，50 篇源 MD SHA 与账本一致；48 篇有展示数学公式，**重点抽查与分析 496 个原样公式块**，同时保存全部 1,273 个源展示式及上下文。所有 1,273 个原始 MD 起止行号回放一致，无错位；2 篇 P0135/P0142 无可提取展示式，标记 `BLOCKED_NO_DISPLAY_MATH`，不填造公式。原始图片未归档，PDF 视觉校验为 0。

本次属于 `FORMULA_CHAIN_SPOT_REVIEW`，**不是 A 类逐篇完整公式验收、不是新增 50 篇 A 类论文，也未更新 264 工作组的 A64/B41/C84/D75 临时分类**。C 类只作为数学机制对照，若经原始贡献核对证明新增机制才晋升；前期主任务 WAM 原文均未导入。

存档分工：GitHub 长期保留本索引与数学差异结论；完整的每篇源公式、公式上下文、50 篇逐篇卡和 264 行新版账本在当前会话压缩包 `RISKFIELD_BULK50_FORMULA_AUDIT_20261028.zip`，**尚未整包推入 GitHub**。

## 10. Batch4 数学机制增量（2026-10-28；61 篇、1,450 原式）

**[公式分级审计、独立数学反例与 61 篇统一入口](RISKFIELD_BATCH4_61_PAPER_FORMULA_AUDIT_20261028.md)**

本批从 `all_md.zip` 拣选原 Bulk50 未覆盖的 61 篇论文组（A26/B20/C15），已完成源文件哈希核验 61/61、展示公式精确行号回放 1,450/1,450。54 篇关键公式及其原文上下文做有限方法主链判读，183 处关键原式直接引用；另 7 篇仅源公式提取，**不能冒充完整机制审计**。原 PDF 视觉/全公式闭合仍均未完成。

与本研究高度相关的新增结论是 P0256 的「双路径多边形空间交叠 × 分别递减时间权重」并无 `t_i=t_j` 同刻条件；P0240 的反应时间与制动距离 sigmoid 门，P0154 的 ST 安全集合，P0191 的未来风险场经 TTA 时间过滤后降维，以及 P0115 对连续 Gaussian 加速度密度使用的概率语义，都有独立数学边界。均按 SOURCE 与 DERIVED 两种证据等级在上述链接中分别标记。

会话端已生成 `RISKFIELD_BATCH4_61_PAPER_MATH_AUDIT_20261028.zip`（含 61 张独立论文审计卡、1,450 个展示公式原文与行号、54 篇人工要点审核、统一 264 行审计状态、数学机制对照和数值检查；ZIP SHA-256 `01b510a736534b008f9a29319a17616959ac01847bc8c6b8cedc2e20e4e2cc83`）。**该 ZIP 尚未完整上传 GitHub，本仓库目前保留归档索引和摘要证据**。旧 264 候选组和 A/B/C/D 工作分类仍暂定，不能因为处理 61 篇就直接累加出 325 篇。

## 11. 公式建模闭合验收门槛（2026-10-28，替换此前“数量优先”的研究方法）

本轮用户再次明确：**不再把批量扫描、公式定位、粗分类当作完成逐篇审计；优先弄清每篇完整数学建模，暂不急于写大范围跨论文总结。** 既有 Bulk50、Batch4 中的公式数只表示已建立可追溯**原文基础设施**，不代表这些论文的风险模型已经闭合。

严格将文献结果分成三类：`OUT_OF_SCOPE`（研究的不是可用于驾驶安全建模的风险/安全机制，不需要深读）、`MODEL_REUSE_ONLY`（完整引用成熟核而没有实质新增风险定义，可与原始来源建立公式复用边，只深审新增的接口）、`INDEPENDENT_MECHANISM`（风险数学对象/输入/时间/几何/交互/响应能力/聚合方式或风险评分的作用链发生实质变化，保留独立机制审计）。**同核不等于同方法，同名不等于同一论文。**

每篇判定“公式机制可以理解”必须同时：① 确认风险量的定义域、单位、非概率/概率语义；② 找齐风险源→局部几何或相对运动→时间处理→多周车/模态聚合→ego 候选评分/控制的全部已有环节；③ 对每个式子的变量、参数、同名变量重载和 Eq. 依赖关系逐一核对；④ 说明作者沿用的原始模型和该论文的新增机制；⑤ 识别闭合所需关键公式如已损坏则标 `PDF_REQUIRED/BLOCKED`；⑥ 记录原文 MD SHA/行号和具体可算反例；⑦ **只把符合证据的部分标为已核，禁止未验证公式参与研究模型设计。**

详细示范已实际落地：**[P0121 完整公式机制链核读](riskfield_models/P0121_MECHANISM_AUDIT.md)**。源论文 20 个展示式已精确逐个回放，连通 Eq.(1)–(20) 的预测、风险场和 MPCC，但发现 Eq.(13) 括号、Eq.(15) 时间索引及双 γ、概率归一化等关键不闭合点，因此**未**标 `FULL_FORMULA_VERIFIED`。会话端另保存全 20 式原样附录 `P0121_FULL_MATH_MODEL_AUDIT.md`，尚未完整镜像到 GitHub。

**后续使用原则：** 与其一年产出上百张不完整公式卡，不如按照上述验收门槛逐篇达到 `MODEL_SEMANTICS_CLOSED`。跨论文等价整理只做最必要的重复阅读减免，不应取代逐篇计算链理解。此前分类/批次统计保留历史，不作为完成度 KPI。

## 12. Full-chain 模式第二批：4 篇逐篇数学链闭合排查（2026-10-28）

这批不再追求新论文数；选取 P0240、P0256、P0076、P0238 四篇公式机制不同的论文，对每篇原文**所有展示公式块**重新定位并区分场本体/输入/下游/训练：共 7+22+21+17=**67 式**。原始 MD SHA-256 四份全部确认，成稿附件 67/67 公式与源文件逐字符对齐；**未作 PDF 视觉检查，不声称完整数学闭合**。

| 论文 | 公式建模主链 | 当前最重要不闭合点 | GitHub 逐篇卡 |
|---|---|---|---|
| P0240 | 经验等效质量→反应/制动距离 sigmoid 源场→路边界场→驾驶风格图像 | 动态方向指数正负号反转、源/受体质量下标、矢量聚合未写式 | [P0240](riskfield_models/P0240_MECHANISM_AUDIT.md) |
| P0256 | 确定性规则未来路径→全对路径矩形交面积→分别前视索引衰减→最坏 NPC SP→SAC reward | 没有同步未来时刻匹配，不能作为真正时空碰撞风险 | [P0256](riskfield_models/P0256_MECHANISM_AUDIT.md) |
| P0076 | 人工空间风险标签→非负张量 B 样条拟合→速度加权风险积分→词典序两阶段 OCP | 经验标签非概率、动态 actor 不存在、Eq.(21) 字符污染 | [P0076](riskfield_models/P0076_MECHANISM_AUDIT.md) |
| P0238 | 同时刻两车椭圆安全 h→动态 CBF H→delta-method 风险分布→尾部 CVaR→最坏周车→MPC 硬软约束 | Eq.(10) 梯度变量维度、Theorem3 上界/全时域概率条件 | [P0238](riskfield_models/P0238_MECHANISM_AUDIT.md) |

**完全原式备份**：用户会话生成 `FOUR_PAPER_FULL_MATH_AUDIT_20261028.zip`，包括四篇完整逐式 MD、67 式全量表、4 份原始 MinerU MD、源路径与 SHA 映射、独立逐式回放验收。GitHub 当前提交的是四篇重点公式链与歧义，不是全部 67 式的原样镜像。所有四篇状态为 `MD_EQUATION_CHAIN_MAPPED_WITH_BLOCKERS`，不是 `FULL_FORMULA_VERIFIED`。

**去重策略**：P0240 含引用既有 Tian/Wu 风险核但新增制动 sigmoid；P0256 是路径扫掠交面积风险，不应与同步占用安全势混并；P0076 新在 B 样条数值表示、不提供新事故物理量；P0238 以成熟 CBF/CVaR 提供安全约束机制对照，不因为名称“risk map”而计为原创 Gaussian 场。
