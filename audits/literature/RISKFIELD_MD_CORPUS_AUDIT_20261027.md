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
