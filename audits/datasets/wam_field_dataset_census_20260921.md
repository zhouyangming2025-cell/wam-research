# WAM / WAM+VLA 领域数据集目录（来源语料交叉补录 2026-09-29）

## 0. 本轮结论

上一版“核心 12 + 16 篇代表性扩展论文”**不足以作为后续下载决策的数据集底账**。本目录的目标是尽量找全仓库 WAM / WAM+VLA 相关论文涉及的数据集和数据资产，并按资产家族归并；不是把扩展论文逐篇做成与核心论文同等深度的审计。

已有的 65 篇广义 census 与 22 篇专项账本提供发现来源和出处。其中既有逐篇记录仅作追溯与频次交叉检查，本轮不继续扩写 75 篇逐篇分析。目录主体按数据资产组织：原始驾驶数据、派生数据与 benchmark、语言/QA/奖励标注、通用视觉数据、仿真与作者私有资产分别登记。

此前的广义 census 曾对仓库 `papers/raw_md/` 中的 **65 个论文条目做逐项核对**：

- **64 个条目**：直接读取 `<ID>_<Name>.raw.md` 原文；
- **P0067 ProSim**：仓库当前只有 verified source note，没有 full raw Markdown；因此只使用 source note，并额外核对官方 ProSim 发布页确认其底层使用 **Waymo Open Dataset / WOMD** 与 **ProSim-Instruct-520k**；
- 统计只记录论文**实际训练、微调、主/补充评测、明确构建 benchmark 的数据**；
- **不把 Related Work / reference list 中“提到过”的数据集算作论文使用数据**；
- 这 65 条是仓库当时的**广义领域语料**，不等于 65 篇纯 WAM 论文；包含 E2E、预测、occupancy、仿真/benchmark 等相邻工作，也包含 P0030–P0033 数据集/benchmark 论文自身；频次是语料内唯一 paper ID 数，不是全领域抽样比例；
- 作者自行生成的 feature cache、latent cache、trajectory anchors、pseudo labels、reward cache、teacher trajectories、checkpoint 等普通复现中间资产，不纳入“基础数据集下载”盘点；
- 如果作者生成的数据在论文中被**独立命名，或明确作为训练集/benchmark 使用**，则纳入资产目录并标注公开状态；公开、私有、发布状态未知分开登记。例如 Occ3D、DriveReward、OmniDrive、ProSim-Instruct-520k、CornerCaseRepo 与作者构建的场景集。

本目录的主要任务是：

> **先把这个研究域实际涉及的数据集和资产家族找全、统一名称并厘清来源关系；容量与下载决策后置。**

本目录的范围是仓库当前收录的论文语料，不声称等于整个领域文献全集。频次只作“哪些数据集反复出现”的辅助信息，不要求对扩展论文逐篇复核全部版本、样本和文件。**本阶段不输出下载优先级或总容量。**

**2026-09-29 数据集查漏调整：**批量筛查 raw Markdown 中的数据集/benchmark 标题后，补登记 CornerCaseRepo、CARLA Leaderboard v1/v2、Think2Drive 专家帧，以及 CounterfactualPred 的作者构建场景集。只对新出现资产回看相关段落确认身份；不扩展成对所有论文逐篇重挖。未核公开包状态或字节的资产保留 UNKNOWN。

---

## 0.1 当前仓库论文语料的统一覆盖（2026-09-29）

本次统一发现来源池为此前 65 篇广义领域 census 与 22 篇 WAM / WAM+VLA 专项账本的去重并集：65 + 22 − 12 篇重叠核心 WAM = **75 个唯一论文 ID**。其中 65 篇底账为 64 篇 full raw Markdown 加 P0067 ProSim source note；22 篇专项账本包含同一批核心 12 篇及 P0068–P0077 十篇 WAM+VLA。该范围覆盖**仓库当前收录的论文**，不等于整个领域文献全集。

阅读顺序以数据集为中心：先看 §3–§6 的数据资产目录；§1 频次及 §13 重复/单篇资产表用于快速识别高频与长尾；附录 A 保留已有论文到数据集的出处映射，但不再作为扩展论文逐篇深挖任务。22 篇核心证据见 [逐论文资产账本](WAM_22_dataset_asset_register_2026-09-28.md) 与 [媒体/缺口补充证据](WAM_22_OPEN_ITEMS_EVIDENCE_20260928.md)。

## 1. 高频数据家族：仓库来源语料频次（辅助索引）

按“论文直接使用或明确作为其 benchmark/source”的口径，仓库 65 个条目中最集中的数据体系如下。每个 paper ID 对同一数据家族最多计 1 次；同一论文可同时出现在 v1、v2 两行。来源数据、数据集/benchmark 自身论文也按 ledger 中的角色计入，因此这些是**文献条目频次**，不能直接解释成独立下载包数或项目复现概率。

| 数据体系 | 65 条目中涉及条目数 | 说明 |
|---|---:|---|
| **nuScenes** | **31** | 含 P0030 数据集论文及 P0034 的 HUGSIM 来源记录；频次不代表每篇都需下载原始 nuScenes 全量 |
| **NAVSIM 家族（版本合并）** | **30** | v1/v2/未标版本合并后的唯一条目数；见下方版本拆分 |
| **nuPlan（含 mini）** | **17** | 含 P0031 数据集论文及 NAVSIM/OpenScene 上游关系记录；不代表需要全时段 raw sensor |
| **NAVSIM v1（明确标版本）** | **20** | 与 v2 有交集；另有记录只写 NAVSIM，需按 split 信息拆分 |
| **NAVSIM v1 典型 split（论文未写版本号）** | **6** | 报告 `navtrain/navtest` 的 1,192/136 scenarios 或约 103k/12k samples；能识别为 v1 典型 split profile，但不证明具体 archive revision |
| **NAVSIM v2（明确标版本）** | **13** | 其中 12 条也明确涉及 v1；版本频次不能相加成家族频次 |
| **NAVSIM 版本仍未能判定** | **3** | 只称 NAVSIM/使用 NAVSIM 评测 protocol，未给版本或足以识别 split 的信息 |
| **Bench2Drive 家族** | **11** | 含 P0033 benchmark 论文；多版本/子包需另核，不能等同于 11 次下载 |
| **CARLA 原生/仿真侧资产** | **8** | 计 RiskBench、Roach、SUMMIT 等明确 CARLA 实验；仅使用 Bench2Drive 的论文另按 Bench2Drive 计，BridgeSim 的 CARLA 支持能力不算实际使用 |
| **WOMD / Waymo** | **6** | 含 WOMD 与 HUGSIM 来源记录；不能混同 Waymo Perception 全量原始传感器 |
| **HUGSIM** | **4** | 含 HUGSIM 自身场景/benchmark 发布论文 |
| **OpenScene（论文直接写明使用）** | **3** | NAVSIM 上游关系不重复当作直接 OpenScene 使用 |
| **OpenDV** | **3** | 大规模驾驶视频预训练数据，Vista/PWM/CausalDrive 等使用 |

**75 篇去重并集的已复核高频家族：**nuScenes **38/75**、NAVSIM（版本合并）**37/75**、nuPlan（含 mini，直接使用口径）**20/75**、Bench2Drive **14/75**、HUGSIM **5/75**；论文直接点名 OpenScene 为 **3/75**。这些频次已按 paper ID 去重并与 22 篇逐篇表复算。NAVSIM/OpenScene/nuPlan 的上游血缘不自动转成直接使用频次；不同角色统计见[交叉复核表](WAM_22_dataset_asset_register_2026-09-28.md#与-65-篇领域盘点的频次交叉复核)。频次只回答论文是否涉及该家族，不回答资产包是否相同或是否要下载整包。



**NAVSIM 版本复核：**逐篇原文复核后，明确写出 v1 的条目为 20（包括 census 原表漏标的 P0007 DriveReward 与 P0052 ReWorld）；明确写出 v2 的为 13，其中 12 篇也明确写出 v1。另有 6 篇虽未写版本号，但报告 `navtrain/navtest` 的 1,192/136 scenarios 或约 103k/12k samples，按 NAVSIM v1 典型 split profile 单列；这不能替代版本/文件修订号。剩余 3 篇 P0015、P0048、P0059 未给足以判定版本的 split 信息。因此唯一家族频次仍是 30，不能用重叠的 v1/v2 两行直接相加。旧“v1 29”实为“20 条明确 v1 + 9 条原先未标版本、但排除仅 v2 的 P0013”；其中 6 条有 v1 典型 split 佐证，3 条仍未判版本，不应作为纯 v1 精确计数。

若只为观察基础数据集/benchmark owner paper 对总数的影响，剔除 P0030–P0033 四篇后分母为 61，nuScenes 为 30、NAVSIM 家族为 29、nuPlan 为 15、Bench2Drive 为 10。这个敏感性仍包含 E2E、预测、仿真等相邻方向；它不是“纯 WAM 方法论文”频次，也不改变原始 65 条 census 的主表口径。

**CARLA 口径复核：**[P0013 BridgeSim 原文 Table 1](../../papers/raw_md/P0013_BridgeSim/P0013_BridgeSim.raw.md#L31) 把 CARLA 列为平台支持地图，但[实验段落](../../papers/raw_md/P0013_BridgeSim/P0013_BridgeSim.raw.md#L164)报告的是 NavHard log-replay、nuScenes/WOMD unseen-scene 及替换交通策略的测试；没有证据将 CARLA 场景列为该论文实际读取的数据。因此逐篇表将 CARLA 从 P0013 的“实际使用数据”列移到能力备注，CARLA 原生/仿真侧 8 条统计保持不变。

**与 22 篇专项范围的关系：**本 census 截止 P0067，覆盖 12 篇核心 WAM；后续 22 篇账本另含 P0068–P0077 共 10 篇 WAM+VLA。两套范围重叠 12 篇，合并时应去重，当前两账本的并集为 75 个条目，而不是 87 篇。详见 [22 篇账本中的交叉复核表](WAM_22_dataset_asset_register_2026-09-28.md#与-65-篇领域盘点的频次交叉复核)。

这比上一版多暴露出几条不能忽略的数据支线：

1. **Waymo Open Motion Dataset（WOMD）**：BeTop、GameFormer、M2I、BridgeSim、ProSim 等；
2. **仿真/闭环数据资产**：RiskBench、ReactSim-Bench、BridgeSim、SocioDrive-Bench、ProSim-Instruct-520k；
3. **语言/奖励数据支线**：DriveReward、OmniDrive、DriveLM、NuScenes-QA、LingoQA、NuInstruct 等；
4. **地图/占用扩展**：OpenLane-v2、Occ3D、nuScenes-Occupancy；
5. **公开大视频预训练数据**：OpenDV、CoVLA、DrivingDojo；
6. **非公开/作者内部数据**：GAIA-1 4,700 h、DriveVLM 的 SUP-AD，不能误放进“可下载公开数据集”。

因此，后续数据下载决策不能只盯着 `nuScenes + nuPlan + NAVSIM + Bench2Drive`。

---

## 2. 数据层级关系：不要把所有名字都当成独立原始数据集

```text
真实道路传感器 / 日志
├── nuScenes
│   ├── Occ3D-nuScenes
│   ├── nuScenes-Occupancy
│   ├── Turning-nuScenes
│   ├── Adv-nuSc
│   ├── nuScenes-C
│   ├── OmniDrive（QA / counterfactual annotation）
│   └── 部分 HUGSIM 重建场景
│
├── nuPlan
│   ├── OpenScene（nuPlan compact redistribution，常用 2 Hz）
│   │   ├── NAVSIM v1
│   │   └── NAVSIM v2
│   ├── ReactSim-Bench
│   ├── SocioDrive-Bench 的主要真实数据来源
│   └── 多篇 world model / WAM 直接视频预训练
│
├── Waymo Open Dataset / WOMD
│   ├── BeTop / GameFormer / M2I
│   ├── ProSim + ProSim-Instruct-520k
│   ├── BridgeSim 场景源
│   └── 部分 HUGSIM 重建场景
│
├── Lyft-Level5
├── KITTI-360
├── PandaSet
├── CoVLA
├── DrivingDojo
├── OpenDV
└── CityWalker

模拟器 / 交互环境
├── CARLA
│   ├── Bench2Drive
│   ├── CARLA Leaderboard v1/v2 routes/scenarios
│   ├── CornerCaseRepo（Think2Drive）
│   ├── RiskBench
│   ├── Think2Drive expert frames
│   ├── CounterfactualPred case set
│   ├── LAW 的 Roach expert data
│   ├── CausalDrive 的 safety-critical / SocioDrive 数据组成
│   └── SUMMIT（基于 CARLA）
├── HUGSIM（真实场景 3DGS 重建闭环）
└── BridgeSim（跨 simulator / 多地图闭环平台）
```

最重要的几个口径：

- **nuScenes 与 nuPlan 是独立采集的数据集**。
- **OpenScene 是 nuPlan 的再分发/重组织数据层，不是第三套独立采集数据**。
- **NAVSIM 是 planning benchmark，不是重新采集的数据源**。
- **WOMD 是 Waymo Open Dataset 的 motion/scenario 数据分支**；不要和 Waymo perception raw sensor dataset 混写。
- **Bench2Drive 是 CARLA 上的标准化 E2E 数据/benchmark；CARLA 本身是 simulator**。
- **HUGSIM 的可下载对象是重建后的 scene/scenario 资产，不等于“机器上有 nuScenes/Waymo/KITTI-360/PandaSet 就已经有 HUGSIM”**。

---

## 3. 数据资产目录：类别与阅读入口

本目录按资产实体归档，不按论文逐篇展开。相同上游数据可同时出现在母体、筛选子集、标注层或 benchmark 中；这些层次要分开登记，不能因名称相似就视为同一包或可相互替代。

| 资产层 | 数据集目录位置 | 典型内容 |
|---|---|---|
| 原始驾驶传感器、motion、视频 | §4.1、§6 | nuScenes、nuPlan、WOMD、OpenDV、CoVLA、DrivingDojo 等 |
| 规划、闭环、仿真与 benchmark | §4.2 | NAVSIM、Bench2Drive、HUGSIM、RiskBench、ReactSim-Bench；CARLA/SUMMIT 等模拟器另标为软件/环境 |
| 派生标注、占用/拓扑与驾驶 QA | §4.3、§4.4、§5 | Occ3D、OpenLane-v2、DriveLM、OmniDrive、ReCogDrive、SUTD 等；标注与其引用的图像/视频分层 |
| 通用视觉/VQA 训练与评测资产 | §4.4 | FineVision、LLaVA-v1.5 来源、通用 VQA benchmark；复合数据集未公开组成时按家族登记并标明 UNKNOWN |
| 作者自采、私有或仅特定论文所需资产 | §8、§13.2 | LAW/Roach 候选、W0、GAIA-1、SUP-AD、作者生成 benchmark |

§4–§6 与 §13.2 是数据集/资产目录主体；§1 的论文频次只辅助判断哪些家族反复出现。逐篇来源表放在[附录 A](#附录-a-已有论文到数据集出处映射来源索引)，不要求读者逐篇核对后才能使用本目录。

---

## 4. 领域基础数据源总表

本节按类别登记仓库来源语料中出现的具名基础数据、benchmark 与衍生资产；软件环境、原始母体和标注/派生层分开记。是否下载、下载全量还是子集留到容量与复现阶段判断。

### 4.1 真实驾驶 / motion / video 基础数据

| 数据集 | 数据类型 | 本仓库直接使用代表 | 210 当前状态 |
|---|---|---|---|
| **nuScenes** | 6-camera + LiDAR + radar + map + 3D labels | 31 个条目涉及 | **已有，基本完整** |
| **nuPlan** | 千小时级真实驾驶日志 / planning | Epona、DriveLaW、WA-JEPA、GenDrive、SLEDGE 等 | **部分：缺 raw trainval** |
| **OpenScene** | nuPlan compact redistribution / 2 Hz research layer | NAVSIM、DriveWorld、Drive-JEPA | **已有** |
| **WOMD / Waymo Open Motion** | 轨迹 + map 的大规模 motion/scenario data | BeTop、GameFormer、M2I、ProSim、BridgeSim | **正式数据根盘点未见** |
| **Waymo sensor data** | 高分辨率真实传感器数据 | HUGSIM 场景来源等 | **正式数据根盘点未见** |
| **OpenDV** | 千小时级互联网 / worldwide driving video | Vista、PWM、CausalDrive | **正式数据根盘点未见** |
| **CoVLA** | front video + CAN/action/trajectory + language | Drive-JEPA | **正式数据根盘点未见** |
| **DrivingDojo** | interactive driving video / trajectory | Drive-JEPA | **正式数据根盘点未见** |
| **CityWalker** | 城市第一视角 / teleoperation navigation | Metis | **正式数据根盘点未见** |
| **Lyft-Level5** | 独立真实自动驾驶数据集 | DriveOccWorld | **正式数据根盘点未见** |
| **KITTI-360** | 城市多传感器 / 3D scene | HUGSIM source | **正式数据根盘点未见** |
| **PandaSet** | 多传感器自动驾驶 | HUGSIM source | **正式数据根盘点未见** |

### 4.2 Planning / simulation benchmark

| 名称 | 本质 | 主要使用论文 | 210 当前状态 |
|---|---|---|---|
| **NAVSIM v1 / 未标版本 NAVSIM** | OpenScene/nuPlan 上的非反应式 planning benchmark | **20 条明确 v1；另 6 条符合 v1 典型 split；3 条未能判版本；NAVSIM 家族 30 条，v2 13 条（与 v1 重叠 12 条）** | **已有** |
| **NAVSIM v2** | EPDMS + reactive traffic support + two-stage pseudo-simulation | 13 个条目 | **已有** |
| **Bench2Drive** | CARLA E2E train/eval benchmark | 11 个条目 | **已有 v0.0.4 no-depth + maps；depth 未见** |
| **CARLA Leaderboard v1/v2** | CARLA 闭环 route/scenario benchmark；与 Bench2Drive 分开 | [P0027 原文](../../papers/raw_md/P0027_Think2Drive/P0027_Think2Drive.raw.md#L7)直接报告官方 v1/v2 route 评测；v2 含 39 类场景 | 论文确认使用；独立 route asset 文件清单未在本轮核对 |
| **CornerCaseRepo** | Think2Drive 提出的 CARLA 场景解耦 route benchmark；1,600 train + 390 eval routes | [P0027 原文 §4.2](../../papers/raw_md/P0027_Think2Drive/P0027_Think2Drive.raw.md#L153) | 名称、规模和作用有论文依据；公开 route 包状态 UNKNOWN |
| **Think2Drive expert frames** | CARLA 不同天气下采集的 TCP 模仿学习输入；论文称 200K frames | [P0027 原文](../../papers/raw_md/P0027_Think2Drive/P0027_Think2Drive.raw.md#L181) | 作者生成资产；frame bytes 与公开包状态 UNKNOWN，不从帧数推算容量 |
| **CounterfactualPred CARLA case set** | 作者构建的 186 个反事实案例、72 个初始 placements 的 RGB 序列 benchmark | [P0016 原文 §5.1](../../papers/raw_md/P0016_CounterfactualPred/P0016_CounterfactualPred.raw.md#L121) | 原文描述了采集与模态；独立公开发布状态 UNKNOWN，不从分辨率/帧数推算容量 |
| **HUGSIM** | 真实场景重建 photorealistic closed-loop | TOAD、WA-JEPA、DrivoR 等 | **未见 released scene/scenario 资产** |
| **RiskBench** | CARLA 风险场景数据/benchmark | RiskWorld | **未见** |
| **ReactSim-Bench** | nuPlan 上构建的 reactive traffic test benchmark | ReactSimBench | **未作为独立资产确认** |
| **BridgeSim** | 跨 simulator / 多地图闭环平台 | BridgeSim | **未作为独立资产确认** |
| **SUMMIT** | 基于 CARLA 的交互式城市 simulator | What Truly Matters | **未盘点** |
| **CARLA** | simulator，不是固定真实数据集 | RiskWorld、LAW、CausalDrive、CRAFT 等 | **本次 dataset inventory 未盘点软件安装状态** |

### 4.3 独立发布的 annotation / derived dataset

| 名称 | 上游 | 主要作用 | 210 当前状态 |
|---|---|---|---|
| **Occ3D** | nuScenes / Waymo | semantic occupancy GT | **未确认** |
| **nuScenes-Occupancy** | nuScenes | fine-grained occupancy labels | **未确认** |
| **Turning-nuScenes** | nuScenes val | 转弯困难子集 | **未确认独立文件/索引** |
| **Adv-nuSc** | nuScenes val | adversarial traffic robustness | **未确认** |
| **nuScenes-C** | nuScenes val | corruption robustness | **未确认** |
| **OpenLane-v2** | 独立道路拓扑标注体系 | OmniDrive counterfactual checklist | **未见** |
| **OmniDrive** | nuScenes | 3D / counterfactual driving QA | **未见** |
| **DriveReward** | NAVSIM | trajectory reward / reasoning dataset | **未见** |
| **DriveLM** | nuScenes-based driving QA | VLM reasoning benchmark | **未见** |
| **ProSim-Instruct-520k** | WOMD train/val | 520k scenarios 上的 prompt / motion tags | **未见** |
| **SocioDrive-Bench** | 80% nuPlan + 20% CARLA | driving sociology / reactive world-model benchmark | **未见；公开状态待下一轮核** |

---

### 4.4 WAM+VLA 新增的通用视觉、VQA 与腐蚀评测资产

以下资产身份纳入 75 篇统一登记；“标注集”与“原始媒体”分开，具体文件版本和字节数不在本阶段处理。论文/代码给出名称但未给足源清单的，保留 PARTIAL/UNKNOWN。

| 数据资产 | 论文/角色 | 母体或类型 | 登记状态 |
|---|---|---|---|
| ReCogDrive_Pretraining | P0074 论文明确使用 3.1M 驾驶 QA；P0068 仅有 ReCogDrive 式预训练关联线索 | 多源驾驶 QA / 轨迹标注；17 个 JSONL 与源媒体分层 | **PARTIAL**：17/17 JSONL 全量路径扫描，681,733 rows、4,158,072 URI refs、1,832,283 source-family unique paths；实际论文章节取用子集、媒体 byte/hash 未闭合。 |
| SGDrive 标注集 | P0070 训练 | 驾驶 QA + 轨迹 QA；JSONL 引用 NAVSIM/OpenScene 路径 | **PARTIAL**：全量 85,109 rows、340,436 refs、126,032 unique paths 已核；原图 byte、OpenScene archive/member hash 与 loader root 仍 UNKNOWN。 |
| UniDriveVLA 作者 JSON/标注 | P0076 训练 | 驾驶 VQA 标注 | **PARTIAL**：与原始图片包的包含关系需按路径核验。 |
| FineVision | P0076 通用视觉/VQA 混合训练 | 通用视觉数据家族 | **PARTIAL**：论文/代码提示抽样清单，实际 shards 与样本媒体集合未确认。 |
| LLaVA-v1.5 general VQA mix | P0074 通用 VQA 训练 | 通用图像 + VQA 标注 | **UNKNOWN**：论文 3.4M 与公开配置 665K 不一致，具体发布版本、split 和图像路径未确认。 |
| navsim_668k.jsonl | P0074 作者 SFT 配置中的 NAVSIM 标注 | NAVSIM 派生标注；不是原图包 | **PARTIAL**：文件内容身份为 NAVSIM 标注；它与论文所称 nuPlan 668K 训练阶段的对应关系未证实，且不能代替 3.4M 通用 VQA 原图。 |
| DriveBench | P0076 腐蚀鲁棒性评测 | 驾驶图像 corruption benchmark + QA | **PARTIAL**：评测名与任务已知，完整 corruption image 清单及运行时生成/预生成边界未知。 |
| ReCogDrive 上游配置源：NAVSIM / Bench2Drive QA 与轨迹项 | P0074 作者固定配置/17 个标注 JSONL | NAVSIM/OpenScene 与 Bench2Drive 的派生 QA/轨迹标注 | **PARTIAL**：完整 canonical path 数及标注间相交已核；对应 archive bytes/member hash 未核。 |
| DriveLM | P0007 recipe、P0025 OmniDrive 数据链、P0071 FSDrive、P0077 UniDrive-WM 评测；P0074 作者配置列为源 | nuScenes 图像上的驾驶 QA | **PARTIAL**：标注来源已命名；每篇实际 split 与原图重用关系未统一。 |
| NuScenes-QA | P0007 recipe；P0074 作者配置列为源 | nuScenes QA 标注 | **PARTIAL**：与 nuScenes 母体相关；逐样本对应未统一。 |
| OmniDrive QA | P0007 recipe、P0025、P0071；P0074 作者配置列为源 | nuScenes 派生驾驶/反事实 QA | **PARTIAL**：区分 QA 标注包与 nuScenes 原图。 |
| NuInstruct | P0007 recipe；P0074 作者配置列为源 | 驾驶指令/QA 标注，图像路径可能指向 nuScenes | **PARTIAL**：source path 中可识别 nuScenes 根；样本级映射未统一。 |
| Senna | P0007 recipe；P0074 作者配置列为源 | 驾驶 QA 标注，图像路径可能指向 nuScenes | **PARTIAL**：source path 中可识别 nuScenes 根；样本级映射未统一。 |
| CODA-LM | P0074 作者配置及 ReCogDrive 标注源 | 独立驾驶 QA 图像来源候选 | **PARTIAL**：15,516 unique paths（`images/` 和 `images_w_boxes/`）；与 nuScenes 的内容 hash/官方文件映射未核。 |
| LingoQA | P0007 recipe；P0074 作者配置/标注源 | 驾驶视频帧 + QA；Scenery/Action split | **PARTIAL**：134,120 unique paths：Action 116,770、Scenery 17,350；配置根/loader path join 与实际媒体包仍需核。 |
| MAPLM v0.1 | P0074 作者配置/标注源 | 驾驶多视角图像及地图/问答标注 | **PARTIAL**：31,836 unique `maplm_v0.1/train` paths；主 archive 大小是包近似值，不代表子集精确字节。 |
| SUTD TrafficQA | P0007 recipe；P0074 作者配置/标注源 | 视频 QA；标注/features 与原视频分层 | **PARTIAL/RESTRICTED**：9,916 unique `.mp4` paths；Zenodo features/annotation 不含这些像素视频，原始包 byte UNKNOWN。 |
| Talk2Car | P0007 recipe；P0074 作者配置/标注源 | nuScenes 相关语言导航/指令数据 | **PARTIAL**：8,079 unique paths 按标注来源/配置 root 归属；平铺 basename 不能独立证明母体。 |
| DriveGPT4 / BDD-X selected images | P0007 recipe；P0074 作者配置/标注源 | BDD-X 图像/对话标注候选 | **PARTIAL**：113,320 unique relative paths 按文件与 config root 推断；同名候选包未逐路径/hash 绑定，不等同完整 BDD-X 视频。 |
| DRAMA | P0074 作者配置/标注源 | 多摄像头驾驶视频、GIF、光流与标注 | **RESTRICTED/UNKNOWN**：全量标注引用 16,401 unique GIF paths，原始发布包 byte 未找到且申请受限。 |
| MMStar | P0076 通用视觉问答评测 | 通用 VQA benchmark | **PARTIAL**：名称已知，论文对应版本/split 清单待核。 |
| MMMU | P0076 通用视觉问答评测 | 通用 VQA benchmark | **PARTIAL**：名称已知，论文对应版本/split 清单待核。 |
| RealWorldQA | P0076 通用视觉问答评测 | 通用 VQA benchmark | **PARTIAL**：名称已知，论文对应版本/split 清单待核。 |
| AI2D | P0076 通用视觉问答评测 | 通用图表/科学图像问答 | **PARTIAL**：名称已知，论文对应版本/split 清单待核。 |
| MME | P0076 通用视觉问答评测 | 通用 VLM benchmark | **PARTIAL**：名称已知，论文对应版本/split 清单待核。 |
| VLMsAreBlind | P0076 通用视觉问答评测 | 通用 VLM benchmark | **PARTIAL**：名称已知，论文对应版本/split 清单待核。 |
| ChartQA | P0076 通用视觉问答评测 | 图表问答 benchmark | **PARTIAL**：名称已知，论文对应版本/split 清单待核。 |
| Chat-B2D（ORION 原版） | P0077 通用/驾驶 VQA 评测 | Bench2Drive 图像上的 QA 标注 | **PARTIAL**：按原版与后续扩展版区分；样本路径映射单列核查。 |

DriveReward 的 10 项域内 QA 预训练来源仍按 §5 登记；ReCogDrive 源目录中出现的 CODA-LM、DRAMA、SUTD、Talk2Car、LingoQA 等保留为**上游候选/标注来源记录**。只有论文 recipe 或配置确认实际加载时才增加直接使用频次，不把“目录中存在”推成“每篇都用”。逐源媒体和包证据见 [22 篇开放项证据](WAM_22_OPEN_ITEMS_EVIDENCE_20260928.md)。

## 5. 一段式 / WAM 的语言与奖励数据支线

65 篇全量审计以后，发现仅盘点 sensor/log 数据还不够。仓库已经出现一条明确的 **VLM / reward / reasoning 数据支线**。

### DriveReward 明确使用的域内 QA 数据

DriveReward 原文给出的两阶段 recipe 中，第一阶段整合：

- **DriveLM**
- **ReCogDrive**
- **NuScenes-QA**
- **SUTD**
- **Talk2Car**
- **LingoQA**
- **NuInstruct**
- **Senna**
- **OmniDrive**
- **DriveGPT4**

第二阶段再用作者构建的 **DriveReward Dataset** 微调。

这些数据的角色和 nuScenes/NAVSIM 不同：它们不是基础多传感器驾驶日志，而是**基于驾驶数据构建的 QA / reasoning / instruction / reward annotations**。后续下载决策时应单独作为“语言数据层”处理，不能和 raw sensor dataset 混成一张体量表。

### OmniDrive 数据链

```text
nuScenes raw sensor / 3D annotations
+ OpenLane-v2 topology
+ simulated counterfactual trajectories
→ OmniDrive QA
→ DriveLM / nuScenes planning / VLM experiments
```

因此，“我们已有 nuScenes”并不等于“我们已有 OmniDrive / DriveLM / OpenLane-v2”。

---

## 6. 大规模 world-model / WAM 视频预训练数据

全 65 篇后，这一类的重要性比上一版更清楚。

### OpenDV

仓库中直接落到 OpenDV 的代表：

- **Vista**
- **PolicyWM / PWM**
- **CausalDrive**

它承担的不是常规 3 秒 planning supervision，而是**大规模真实驾驶视频世界模型预训练**。

### CoVLA + DrivingDojo

Drive-JEPA 明确把：

```text
CoVLA
+ DrivingDojo
+ OpenScene trainval
→ 约 330 h driving-domain V-JEPA pretraining
```

然后才进入 NAVSIM planning。

这意味着 Drive-JEPA 的数据路线和“直接在 navtrain 上训练 planner”的论文不同。

### GAIA-1 proprietary corpus

GAIA-1 使用约 **4,700 h** proprietary London driving data。它说明领域上限已经远超公开小数据集，但该数据**不是公开可下载数据**，因此只作为领域规模参照，不进入公开下载候选。

### repo 外补充观察

上一版外部调研还发现 2026 新 WAM 已开始使用 **PhysicalAI-Autonomous-Vehicles** 等更大规模公开数据。该项不计入本次“仓库 65 篇频次”，但保留为领域外延观察；是否纳入下一轮下载候选，应在下载调研阶段重新核查。

---

## 7. 210 开发机现状：用完整 65 篇视角重新评价

依据提交 `ea2f5f9330e8591080e56b4da293f7c0e18739ef`：

### 已经覆盖的主干

| 数据 | 当前正式数据 |
|---|---|
| **nuScenes** | Core Full + CAN bus + Map Expansion + camera supplement，约 0.356 TiB |
| **OpenScene v1.1** | 约 2.37 TiB |
| **NAVSIM v1** | 约 418.22 GiB |
| **NAVSIM v2** | 约 46.79 GiB，含 navhard two-stage 等 |
| **Bench2Drive** | v0.0.4 no-depth + map，约 0.381 TiB |

### 部分覆盖

| 数据 | 当前缺口 |
|---|---|
| **nuPlan** | 现有约 1.62 TiB 主要是 test / mini / maps；**没有 raw trainval sensor data** |
| **Bench2Drive** | no-depth + maps 已有；**depth 不在正式 inventory 中** |

### 65 篇审计后明确暴露、但当前正式 inventory 未见的公共数据家族

- **WOMD / Waymo Open Motion Dataset**
- **HUGSIM released scenes / scenarios**
- **OpenDV**
- **CoVLA**
- **DrivingDojo**
- **CityWalker**
- **Lyft-Level5**
- **KITTI-360**
- **PandaSet**
- **Occ3D**
- **nuScenes-Occupancy**
- **OpenLane-v2**
- **OmniDrive / DriveLM / NuScenes-QA / LingoQA / NuInstruct 等语言数据**
- **DriveReward**
- **ProSim-Instruct-520k**
- **RiskBench**
- 以及若公开可得的 **ReactSim-Bench / SocioDrive-Bench** 等命名 benchmark 资产

这里的“未见”严格表示：

> **2026-09-21 的 210 正式数据根 inventory 没有该条目。**

它不等于“整台机器所有路径绝对不存在”，也不等于“下一步一定要下载”。

---

## 8. 哪些东西不是独立公开基础数据包

以下常规训练产物或软件环境不按独立基础数据集包计；若其在论文中被明确命名为数据资产或 benchmark，仍登记在 §13.2，并将发布状态和容量保持为 UNKNOWN：

- 作者训练产生的 latent / feature cache；
- trajectory anchor / K-Means centers；
- reward cache / metric cache；
- pseudo-teacher trajectories；
- future BEV cache；
- Grounded-SAM / Metric3D 临时 pseudo labels；
- author checkpoint / backbone weights；
- 单篇代码运行时重新生成的 `*.pkl`；
- LAW 的 Roach 189K expert frames、WhatTrulyMatters 的 Alignment-59,944、Think2Drive 的 200K CARLA expert frames、CounterfactualPred 的 186-case RGB benchmark 等**作者自采/自生成实验资产**均予登记；它们不因此成为可公开采购的数据包，也不推定有独立下载源；
- CARLA / SUMMIT 的软件安装、版本、route config、evaluation server：这是复现环境准备，不是“公开基础数据集下载”。

但如果作者把衍生内容正式发布成独立 dataset / benchmark，例如：

- Occ3D
- OmniDrive
- DriveReward
- ProSim-Instruct-520k

则作为公开数据资源单独登记。

---

## 9. 论文原文中的版本/口径差异：下载阶段必须再核

本轮只做“用了什么数据”的 source-first census，已经发现几个后续下载调查必须注意的口径问题：

1. **nuPlan 总时长**在不同论文版本中有 1,200 h、1,282 h、1,500 h 等写法；后续不能只按一个数字判断“full”。
2. **NAVSIM**同时存在“1,192/136 scenarios”和“约 103k/12k filtered samples”两种层级，不能混为一谈。
3. **Bench2Drive**仓库里不同论文使用 v0.0.3 / Base / 新版协议，而 210 当前是 **v0.0.4 no-depth + map**。
4. **Waymo**至少要区分：
   - perception raw sensor dataset；
   - **WOMD / Motion Dataset**；
   - End-to-End Driving Dataset；
   这三者体量和用途完全不同。
5. **HUGSIM**用到了 KITTI-360 / Waymo / nuScenes / PandaSet 的重建场景，但最终评测所需的是 HUGSIM 发布资产和 simulator，不应简单理解成“下载四个 raw dataset 就完成”。
6. **DriveReward 原文不同位置对 dataset sample 数存在版本/表述差异**；当前只确认其 data source 为 NAVSIM，以及其 QA pretrain 数据组成，不在本轮强行统一数字。

---

## 10. 已有底账的来源与审计强度（历史记录）

此前形成逐篇底账时采用了以下核验方式；这说明现有证据从何而来，不代表后续需要对每篇扩展论文重复同一深度：

1. 枚举 `papers/raw_md/` **65 个目录**；
2. 对 **64 个 full raw Markdown** 读取 Abstract、Experiments / Dataset / Benchmark / Implementation 等相关段落；
3. 将“直接训练/评测”与“Related Work 提及”分离；
4. 对易混项进行二次核查，例如：
   - ViDAR：主实验确认为 **nuScenes**，没有因为 references 出现其他数据就误计；
   - DrivoR：确认 **NAVSIM-v1 train + NAVSIM-v2 navhard-two-stage + HUGSIM zero-shot**；
   - Safe-Sim：确认 **nuScenes train → nuScenes val / nuPlan mini val**；
   - What Truly Matters：确认其 59,944 Alignment scenarios 是 **SUMMIT/CARLA 自采**，不是 Argoverse/nuScenes 下载数据；
   - CausalDrive：确认 **OpenDV → nuPlan / SocioDrive-Bench + Bench2Drive/CARLA** 的直接训练链；
5. P0067 ProSim 因仓库没有 full raw，只用 source note，并额外核官方发布确认：
   - 基于 **Waymo Open Dataset / WOMD**；
   - ProSim-Instruct-520k 覆盖 Waymo train/val，提供 prompt 与 motion tags。

因此，现有底账可以作为数据集名称发现与来源追溯的输入；本轮后续增量按数据集家族处理，不重复构造逐篇报告。

---

## 11. 后续工作边界

数据集全集清理与容量审计分成两个阶段。先完成数据集目录，再决定哪些项目进入容量核验；不得从未定价直接推导为不重要或不需要。

数据集目录阶段按以下边界推进：

- 合并本 census、22 篇核心账本及已有下载调研里出现的 canonical 数据集/资产名称；
- 统一别名、版本家族和父子/派生关系，分开原始数据、benchmark、annotation、通用视觉数据、仿真软件、作者自采或私有数据；
- 对仓库论文材料做批量候选名查漏；仅对新出现或身份/血缘不清的名字回看相关来源，不再逐篇挖掘全部论文；
- 对未能确认身份或实际参与方式的条目保留 `PARTIAL` / `UNKNOWN`，并明确目录只覆盖仓库语料。

容量阶段再按资产优先级核验官方下载源、版本、许可、模态、split、文件清单、压缩/解压大小、重复关系与峰值空间。核心 22 篇已有账本的闭合项目不重做，容量未知也不从小时数、帧数或 QA 数量外推。

在目录与容量证据闭合以前，不把任何“论文出现”自动变成“必须下载整包”，也不把任何未公开/私有数据用公共数据替代。

---

## 12. Source index

### 仓库 source of truth

原文路径统一为：

`papers/raw_md/<paper_id_name>/<paper_id_name>.raw.md`

例外：

`papers/raw_md/P0067_ProSim/P0067_ProSim.source_note.md`

当前机器数据事实：

- [resource_inventory_20260921.md](../../datasets/resource_inventory_20260921.md)
- inventory commit: `ea2f5f9330e8591080e56b4da293f7c0e18739ef`

### 关键数据/benchmark 原文条目

- [P0030 nuScenes](../../papers/raw_md/P0030_nuScenes/P0030_nuScenes.raw.md)
- [P0031 nuPlan](../../papers/raw_md/P0031_nuPlan/P0031_nuPlan.raw.md)
- [P0032 NAVSIM](../../papers/raw_md/P0032_NAVSIM/P0032_NAVSIM.raw.md)
- [P0033 Bench2Drive](../../papers/raw_md/P0033_Bench2Drive/P0033_Bench2Drive.raw.md)
- [P0034 HUGSIM](../../papers/raw_md/P0034_HUGSIM/P0034_HUGSIM.raw.md)

### 本轮额外核验

- ProSim official repository: https://github.com/Ariostgx/ProSim
- ProSim paper: https://arxiv.org/abs/2409.05863

## 13. 统一登记状态与闭合边界（2026-09-29）

**本文件以 75 个在库论文 ID 作为发现来源池**：65 篇广义 census 与 22 篇专项账本按 12 篇重叠去重。高频资产频次见 §1；本节补充驾驶 QA 等重复资产及只在一篇论文出现的具名资产。VLA 通用视觉、驾驶 QA、腐蚀评测等新资产逐项见 §4.4，逐篇论文关联见附录 A.1–A.5。频次按论文 ID 计，不代表包数、样本数或整包下载量。当前登记先闭合名称、角色与血缘，不做容量决策。

### 13.1 已复核的重复数据家族

| 数据家族 / 资产 | 论文频次（去重） | 说明 |
|---|---:|---|
| nuScenes | 38/75 | 含数据集自身论文及 HUGSIM 来源记录；不是 38 次完整包下载。 |
| NAVSIM（合并版本） | 37/75 | v1/v2 等版本重叠；见 §1 与 22 篇交叉表。 |
| nuPlan（直接使用，含 mini） | 20/75 | 不把 NAVSIM/OpenScene 上游血缘重复计作直接使用。 |
| Bench2Drive | 14/75 | 旧论文版与项目新版分开登记。 |
| WOMD / Waymo Open Motion | 6/75 | 与 Waymo 原始 sensor/perception 数据分开。 |
| HUGSIM | 5/75 | 计 HUGSIM 场景/benchmark 使用，不推导出原始来源数据全库需求。 |
| CARLA 原生/仿真侧资产 | 8/75 | simulator/场景路线；与 Bench2Drive 家族分别记账。 |
| OpenScene（论文直接点名） | 3/75 | NAVSIM 上游关系不作为直接 OpenScene 使用频次。 |
| OpenDV | 3/75 | 驾驶视频预训练数据。 |
| DriveLM | 4/75 | P0007、P0025、P0071、P0077 的 recipe/训练/评测表有明确记录。P0074 配置亦列出，但未作为额外确认使用次数。 |
| OmniDrive QA | 3/75 | P0007、P0025、P0071 明确记录；P0074 配置候选不重复计频。 |
| ReCogDrive QA | 2/75 | P0007 recipe 与 P0074 论文均明确使用；P0068 的关系仍是候选。 |

P0074 作者配置列出的 NuScenes-QA、NuInstruct、LingoQA、SUTD、Talk2Car、Senna、DriveGPT4、CODA-LM、MAPLM、DRAMA 等，在 §4.4 保留为“代码配置/上游来源”状态；在逐样本映射或训练配置与论文对应关系闭合前，不把配置中的每个子源都当作已确认的独立论文使用频次。

### 13.2 单篇出现的具名资产（长尾目录）

下表按数据资产列出当前来源语料中只出现于一个 paper ID 的具名长尾项。“1/75”只描述语料频次，不代表复现优先级或下载建议。HUGSIM 源数据只表示作者用于重建的来源，不表示下游论文需下载完整母库；私人或作者生成资产保留在目录中，但与公开可采购项分开。

| 数据资产 | 论文频次 | 类型 / 关系 | 状态 |
|---|---:|---|---|
| RiskBench | 1/75：P0005 | CARLA 风险场景 / benchmark | 名称与用途已登记；发布包/版本仍需核。 |
| ReactSim-Bench | 1/75：P0014 | nuPlan 派生的 reactive traffic benchmark | 数据身份已知；单独发布资产状态待核。 |
| BridgeSim / NavHard | 1/75：P0013 | 跨模拟器评测平台及场景/协议 | 平台、benchmark 与日志数据分层；CARLA 支持能力不等于该论文使用 CARLA 场景。 |
| SocioDrive-Bench | 1/75：P0015 | 交互式 world-model benchmark；论文称 nuPlan/CARLA 混合来源 | benchmark 身份已知；公开包与媒体清单待核。 |
| [CARLA Leaderboard v1/v2 routes/scenarios](../../papers/raw_md/P0027_Think2Drive/P0027_Think2Drive.raw.md#L7) | 1/75：P0027 直接使用 | CARLA 官方 route/scenario 闭环评测；v2 为 39 类场景 | 论文确认评测协议；单独 route 文件清单未核，勿与 Bench2Drive 训练包合并。 |
| [CornerCaseRepo](../../papers/raw_md/P0027_Think2Drive/P0027_Think2Drive.raw.md#L153) | 1/75：P0027 | Think2Drive CARLA route benchmark；1,600 train + 390 eval | 论文声称 benchmark；公开 route 包/复现方式仍 UNKNOWN。 |
| [Think2Drive expert TCP frames](../../papers/raw_md/P0027_Think2Drive/P0027_Think2Drive.raw.md#L181) | 1/75：P0027 | CARLA expert 在不同天气下采集的 200K 模仿学习帧 | 论文记载帧数；是否单独发布及实际字节 UNKNOWN。 |
| [CounterfactualPred CARLA case set](../../papers/raw_md/P0016_CounterfactualPred/P0016_CounterfactualPred.raw.md#L121) | 1/75：P0016 | 186 个反事实案例 / 72 个 placements；每案例包含 factual、counterfactual、null 三路 RGB 序列 | 作者构建 benchmark；公开独立包 UNKNOWN。 |
| SUP-AD | 1/75：P0024 | DriveVLM 私有驾驶数据 | PRIVATE/UNKNOWN；不计公开数据需求。 |
| OpenLane-v2 | 1/75：P0025 | 道路拓扑标注；OmniDrive counterfactual checklist 的来源 | 与 nuScenes 传感器数据分开登记。 |
| COCO | 1/75：P0028 | ViDAR 通用视觉初始化 | 论文记录为通用初始化，不是自动驾驶主训练数据。 |
| ImageNet | 1/75：P0028 | ViDAR 通用视觉初始化 | 同上；按其实际初始化角色保留。 |
| KITTI-360 | 1/75：P0034 | HUGSIM 重建场景来源 | 来源资产；HUGSIM 下游场景使用不推出整库需求。 |
| PandaSet | 1/75：P0034 | HUGSIM 重建场景来源 | 来源资产；HUGSIM 下游场景使用不推出整库需求。 |
| GAIA-1 London corpus | 1/75：P0035 | 约 4,700 h proprietary driving corpus | PRIVATE/RESTRICTED；非公开采购项。 |
| Occ3D | 1/75：P0043 | nuScenes/Waymo occupancy 标签扩展 | 派生标签与 raw sensor 分开登记。 |
| nuScenes-Occupancy | 1/75：P0044 | nuScenes occupancy 标签扩展 | 派生标签与 raw sensor 分开登记。 |
| Lyft-Level5 | 1/75：P0044 | 独立真实驾驶数据集 | 名称已知；论文所需 split/模态待核。 |
| CoVLA | 1/75：P0049 | driving video + CAN/action/trajectory/language | 与 OpenScene/NAVSIM 分开；整库与论文子集待核。 |
| DrivingDojo | 1/75：P0049 | interactive driving video / trajectory | 与 CoVLA、OpenScene 分开登记。 |
| UCF-101 | 1/75：P0052 | ReWorld 辅助线性 probe 数据 | 辅助表征评测，不并入驾驶主训练集。 |
| SUMMIT Alignment dataset | 1/75：P0054 | SUMMIT/CARLA 上作者构建的 59,944 场景集 | 作者生成 benchmark 数据；不是公开真实道路母库。 |
| OpenStreetMap | 1/75：P0056 | DriveArena 的地图来源 | 地图资产，不与 nuScenes/nuPlan 传感器包合并。 |
| CityWalker | 1/75：P0062 | 城市导航 / teleoperation 数据；Metis 使用 15 h | 与公开分卷的映射未确认，详见专项账本。 |
| Turning-nuScenes | 1/75：P0065 | nuScenes val 场景筛选集 | 派生场景列表；不按独立完整图像库计。 |
| Adv-nuSc | 1/75：P0065 | nuScenes val adversarial 子集 | 与 nuScenes 母体分层。 |
| nuScenes-C | 1/75：P0065 | nuScenes corruption benchmark | GraphWorld 所用三天气 corruption 文件清单 UNKNOWN。 |
| DriveReward Dataset / DriveReward-Bench | 1/75：P0007 | NAVSIM 派生 reward / reasoning 标注与 benchmark | 与 NAVSIM 原始场景和训练标注分层。 |
| ProSim-Instruct-520k | 1/75：P0067 | 基于 WOMD 的 prompt / motion-tag 标注 | 与 WOMD 母体分层；该篇依据 source note 与官方发布信息。 |
| LAW Roach / TCP-CARLA candidate | 1/75：P0048 | CARLA expert frames；TCP 三分包仅候选 | LAW 实际采集包身份仍 UNKNOWN，不能以 TCP 候选代替。 |
| DriveVLA-W0 in-house corpus | 1/75：P0072 | 私有 70M 帧 / 百万级 clips 与 100 难例 | PRIVATE/UNKNOWN；不以公开 nuPlan/NAVSIM 替代。 |

VLA / 通用视觉部分同样保留单篇资产：P0074 的 LLaVA-v1.5 通用 VQA 与 NAVSIM 标注文件、P0076 的 FineVision / DriveBench / 七项通用 VQA 评测、P0077 的 Chat-B2D，以及 P0072 的私有 W0 语料，分别见 §4.4 和附录 A.5；不会因这些资产目前没有确定容量而从“数据集全集”中删除。

“统一登记”按**数据资产层级**区分四类：①原始驾驶传感器/视频/轨迹母体；②从母体筛选或重组织的派生包与 benchmark（如 OpenScene/NAVSIM、Bench2Drive、HUGSIM）；③QA/指令/奖励标注；④benchmark 的额外媒体、corruption 图像或私有/作者自采资产。同一名称出现多次按 paper ID 去重计频；上游来源只作 lineage 关联，不自动视为每篇都直接读取母体全量。Related Work 中纯引用且未参与训练、微调、评测或构建的数据不计入使用频次。

仍需保持显式未闭合行，不把它们折成容量估值：

- **源媒体 package identity/容量未闭合：**ReCogDrive/SGDrive 18 份 JSONL 的路径已全量映射及计数，但源包成员、论文实际子集、媒体 byte 与跨 family SHA 去重未闭；LingoQA root resolution、DRAMA/SUTD 限制媒体字节仍 UNKNOWN。
- **通用视觉数据身份未闭合：**WAM-Flow 的 3.4M VQA 图像版本/split/样本清单；论文所称 nuPlan 668K 与公开 navsim_668k.jsonl 的阶段关系；UniDriveVLA 的 FineVision 实际取样与七项通用评测集对应 split。
- **评测资源粒度未闭合：**GraphWorld nuScenes-C 三天气实际 corruption 文件；DriveBench 完整 corruption 资源及生成方式。
- **非公开/作者资产：**LAW 的 189K CARLA/Roach 数据具体发布对象仍 UNKNOWN；DriveVLA-W0 的 70M 帧/百万级 clips 为 PRIVATE/UNKNOWN；GAIA-1、SUP-AD 与自建 Alignment 数据分别保留私有或作者生成属性。
- **派生包/母体边界：**NAVSIM v1 navtrain 与 OpenScene trainval、HUGSIM scenes 与原始来源、CityWalker 15h 子集与公开包、Bench2Drive 旧版/新版都必须保持分行；不能只靠名称推断内容相同。

因此，当前可表述为：**75 个仓库论文 ID 已作为发现来源池合并；高频数据家族和已命名单篇资产已有数据集中心的分组目录；若干长尾资产的正式名称、父体关系或实际依赖仍为 PARTIAL/UNKNOWN，所以还不能宣布仓库语料涉及的数据集目录完全闭合。**后续先按数据集家族做候选查漏与身份归并，不扩写逐篇分析；目录冻结后再衔接容量汇总。本节不提供盘容量建议。

---

## 附录 A. 已有论文到数据集出处映射（来源索引）

本附录保留此前完成的逐篇记录，作为数据集名称的来源追溯和频次交叉检查。它不是后续扩展工作的审计模板；增量按数据集家族做别名、血缘和类别核对，只在身份有歧义时回看相关原文。

### A.1 P0001–P0019

| ID | 论文 | 定位 | 实际训练 / 评测 / 构建数据 | 盘点备注 |
|---|---|---|---|---|
| P0001 | Epona | 核心 WAM | **nuPlan、nuScenes、NAVSIM v1** | nuPlan + 700 nuScenes scenes 训练；NuPlan test / nuScenes / NAVSIM 评测 |
| P0002 | SafeDrive | WAM / 安全规划 | **NAVSIM v1、NAVSIM v2、Bench2Drive** | 同时覆盖 PDMS、EPDMS 与 CARLA 闭环 |
| P0003 | GraphAD | 图式 E2E | **nuScenes** | 主数据集 |
| P0004 | BeTop | 交互预测 / 规划 | **nuPlan、WOMD** | nuPlan planning + Waymo Open Motion prediction |
| P0005 | RiskWorld | 风险 world model / simulation | **RiskBench（CARLA）** | RiskBench 由 CARLA 风险场景构成 |
| P0006 | GenDrive | 生成式规划 | **nuPlan** | 训练和 closed-loop planning test 都在 nuPlan |
| P0007 | DriveReward | 奖励模型 / 数据集 | **NAVSIM v1 → DriveReward / DriveReward-Bench** | 原文报告 NAVSIM-V1 RL 评测及 train-set 衍生（[原文](../../papers/raw_md/P0007_DriveReward/P0007_DriveReward.raw.md#L92)）；另有 QA 预训练混合，见 §6 |
| P0009 | DriveLaW | 核心 WAM | **nuPlan、nuScenes、NAVSIM v1** | 大规模视频预训练 + NAVSIM planning |
| P0010 | TOAD | E2E planning | **NAVSIM v1、NAVSIM v2、HUGSIM** | 同时覆盖 log-based 与 photorealistic closed-loop |
| P0011 | SensitivityShaping | 外围：通用动力学 / OOD | **无统一 AD 基础数据集可列** | 不是本次自动驾驶数据下载主线，避免强行计数 |
| P0012 | DAWAM | WAM | **NAVSIM v1、NAVSIM v2** | planning benchmark 主线 |
| P0013 | BridgeSim | 闭环 simulator / benchmark | **NAVSIM v2、nuPlan、nuScenes、WOMD、BridgeSim/NavHard** | CARLA 是论文列出的支持能力；实验报告未证明实际读取 CARLA 场景，不计 CARLA 使用频次 |
| P0014 | ReactSimBench | reactive traffic benchmark | **nuPlan → ReactSim-Bench** | 基于 nuPlan 构建 2,636 个 test scenarios |
| P0015 | CausalDrive | 交互式 world renderer | **OpenDV、nuPlan、SocioDrive-Bench、Bench2Drive/CARLA、NAVSIM** | OpenDV 1,700 h 预训练；SocioDrive-Bench 20K clips，80% nuPlan / 20% CARLA |
| P0016 | CounterfactualPred | 反事实预测 benchmark | **CARLA；作者构建的 186-case RGB counterfactual benchmark** | controlled counterfactual GT 来自 simulator；公开独立包状态 UNKNOWN |
| P0017 | CRAFT | 闭环 E2E | **Bench2Drive / CARLA** | 闭环 benchmark |
| P0018 | GameFormer | 交互预测 / 规划 | **WOMD、nuPlan** | 两条真实行为数据线 |
| P0019 | M2I | 交互运动预测 | **WOMD** | Waymo motion benchmark |

### A.2 P0021–P0039

| ID | 论文 | 定位 | 实际训练 / 评测 / 构建数据 | 盘点备注 |
|---|---|---|---|---|
| P0021 | HydraMDP | E2E planning | **NAVSIM v1** | NAVSIM 主线 |
| P0022 | DriveSuprim | E2E planning | **NAVSIM v1、NAVSIM v2、Bench2Drive** | 论文强调不引入额外训练数据 |
| P0023 | iPad | E2E planning | **NAVSIM v1 split profile、Bench2Drive** | 原文使用 103k/12k 的官方 navtrain/navtest（[原文](../../papers/raw_md/P0023_iPad/P0023_iPad.raw.md#L152)）；未写 archive revision |
| P0024 | DriveVLM | VLM / E2E | **nuScenes、SUP-AD（内部）** | SUP-AD 为非公开自有数据，不能作为公共下载候选 |
| P0025 | OmniDrive | VLM 数据 / 规划 | **nuScenes、OpenLane-v2、OmniDrive、DriveLM** | OmniDrive QA 基于 nuScenes；counterfactual checklist 还用 OpenLane-v2 topology |
| P0026 | ORION | VLM / E2E | **Bench2Drive** | 主要 CARLA E2E benchmark |
| P0027 | Think2Drive | world-model RL | **CARLA Leaderboard v1/v2、CornerCaseRepo、200K expert TCP frames** | CARLA v2 39 场景；CornerCaseRepo 1,600/390 train/eval routes；expert frame 公布帧数但包体 UNKNOWN |
| P0028 | ViDAR | world representation pretrain | **nuScenes** | 主实验全部在 nuScenes；COCO/ImageNet 只属通用初始化 |
| P0029 | GenAD | E2E / generative | **nuScenes** | 主数据集 |
| P0030 | nuScenes | 数据集论文 | **nuScenes** | 基础数据源 |
| P0031 | nuPlan | 数据集 / planning benchmark 论文 | **nuPlan** | 基础数据源 |
| P0032 | NAVSIM | benchmark 论文 | **OpenScene / nuPlan → NAVSIM v1** | 非反应式 planning benchmark |
| P0033 | Bench2Drive | benchmark 论文 | **Bench2Drive / CARLA** | E2E 多能力闭环 |
| P0034 | HUGSIM | photorealistic closed-loop | **HUGSIM；来源 KITTI-360、Waymo、nuScenes、PandaSet** | 重建场景资产需要单独看待 |
| P0035 | GAIA-1 | driving world model | **4,700 h proprietary London driving data** | 非公开基础数据，记录但不列公开下载 |
| P0036 | DriveDreamer | driving world model | **nuScenes** | 主数据集 |
| P0037 | Drive-WM | driving world model | **nuScenes** | 主数据集 |
| P0038 | Vista | large-scale driving world model | **OpenDV；nuScenes 等跨域评测** | 关键训练源是约 1,740 h worldwide driving video |
| P0039 | DriveDreamer-2 | driving world model | **nuScenes** | 主数据集 |

### A.3 P0040–P0059

| ID | 论文 | 定位 | 实际训练 / 评测 / 构建数据 | 盘点备注 |
|---|---|---|---|---|
| P0040 | DrivingGPT | WAM | **nuPlan、NAVSIM v1 split profile** | 原文列 navtrain/navtest 1,192/136 scenarios（[原文](../../papers/raw_md/P0040_DrivingGPT/P0040_DrivingGPT.raw.md#L106)）；world modeling + planning |
| P0041 | PolicyWM / PWM | WAM | **OpenDV、nuScenes、NAVSIM v1 split profile** | 原文列约 103k/12k train/test samples（[原文](../../papers/raw_md/P0041_PolicyWM/P0041_PolicyWM.raw.md#L100)）；大视频预训练 → 下游 planning |
| P0042 | WorldDrive | 核心 WAM | **nuPlan、nuScenes、NAVSIM v1/v2** | 多阶段数据链 |
| P0043 | OccWorld | occupancy world model | **nuScenes + Occ3D** | Occ3D 是额外 occupancy GT，不能等同于 raw nuScenes |
| P0044 | DriveOccWorld | occupancy world model | **nuScenes、nuScenes-Occupancy、Lyft-Level5** | 独立 occupancy 扩展 + 独立 Lyft 数据 |
| P0045 | WoTE | 核心 WAM | **NAVSIM v1、Bench2Drive** | BEV world model trajectory evaluation |
| P0046 | World4Drive | 核心 WAM | **nuScenes、NAVSIM v1** | 主实验两套 |
| P0047 | DriveWorld | world-model pretraining | **OpenScene、nuScenes** | OpenScene 大规模 4D pretrain → nuScenes downstream |
| P0048 | LAW | 核心 WAM | **nuScenes、NAVSIM、CARLA/Roach expert** | Roach 189K frames 属作者 CARLA expert 采集 |
| P0049 | Drive-JEPA | 核心 WAM | **CoVLA、DrivingDojo、OpenScene、NAVSIM v1/v2、Bench2Drive** | 本仓库中最明显的多源驾驶视频预训练之一 |
| P0050 | WorldRFT | WAM | **nuScenes、NAVSIM v1 split profile** | 原文列 1,192/136 train/test sequences（[原文](../../papers/raw_md/P0050_WorldRFT/P0050_WorldRFT.raw.md#L443)）；open-loop + NAVSIM |
| P0051 | Auto-JEPA | WAM | **NAVSIM v1、NAVSIM v2** | action-oriented latent world model |
| P0052 | ReWorld | WAM | **nuScenes、NAVSIM v1；UCF-101（辅助 probe）** | 原文明写 NAVSIM v1（[原文](../../papers/raw_md/P0052_ReWorld/P0052_ReWorld.raw.md#L244)）；UCF-101 仅表示学习线性探针，不是驾驶训练主数据 |
| P0053 | WA-JEPA | WAM | **nuPlan、NAVSIM v1/v2、HUGSIM** | Stage 1 明确 nuPlan multi-view pretrain |
| P0054 | What Truly Matters | 外围：prediction evaluation | **SUMMIT/CARLA 自建 Alignment dataset** | 59,944 自采 simulation scenarios；不是公开驾驶 sensor corpus 主线 |
| P0055 | SLEDGE | generative scene / simulation | **nuPlan** | 生成式驾驶环境主数据源 |
| P0056 | DriveArena | generative closed-loop simulator | **nuScenes；OpenStreetMap；nuPlan 零样本测试** | World Dreamer 700/150 nuScenes；OSM 是地图源 |
| P0057 | UniAD | E2E | **nuScenes** | 标准 E2E 基线 |
| P0058 | VAD | E2E | **nuScenes** | 标准 E2E 基线 |
| P0059 | DiffusionDrive | E2E planning | **NAVSIM、nuScenes** | 使用 NAVSIM navtest；未找到能单独识别版本的 split 规模，NAVSIM v1/v2 UNKNOWN |

### A.4 P0060–P0067

| ID | 论文 | 定位 | 实际训练 / 评测 / 构建数据 | 盘点备注 |
|---|---|---|---|---|
| P0060 | DrivoR | E2E planning | **NAVSIM v1、NAVSIM v2、HUGSIM** | navtrain 训练；navhard-two-stage；HUGSIM zero-shot |
| P0061 | SeerDrive | 核心 WAM | **NAVSIM v1 split profile、nuScenes；Bench2Drive（补充）** | 原文列 1,192/136 navtrain/navtest scenarios（[原文](../../papers/raw_md/P0061_SeerDrive/P0061_SeerDrive.raw.md#L107)）；future-aware planning |
| P0062 | Metis | 核心 WAM | **NAVSIM v2、CityWalker；NAVSIM v1（补充）** | 自动驾驶 + 城市机器人导航 |
| P0063 | DynFlowDrive | 核心 WAM | **nuScenes、NAVSIM v1 split profile** | 原文列 1,192/136 train/test scenarios（[原文](../../papers/raw_md/P0063_DynFlowDrive/P0063_DynFlowDrive.raw.md#L223)）；两套独立实验 |
| P0064 | Discrete-WAM | 核心 WAM | **nuPlan、NAVSIM v1/v2** | nuPlan pretraining + NAVSIM post-training |
| P0065 | GraphWorld | 核心 WAM | **nuScenes、NAVSIM v1/v2、Bench2Drive** | 另有 Turning-nuScenes、Adv-nuSc、nuScenes-C robustness |
| P0066 | Safe-Sim | safety-critical traffic simulation | **nuScenes、nuPlan mini** | nuScenes train；nuScenes val + nuPlan mini val |
| P0067 | ProSim | promptable closed-loop traffic simulation | **WOMD + ProSim-Instruct-520k** | 仓库无 raw paper；官方发布确认 prompts/tags 覆盖 WOMD train/val |

---

### A.5 P0068–P0077：WAM+VLA 补录

以下十篇是 65 篇底账之后新纳入的 VLA 论文；资产角色沿用 22 篇专项账本的原文核对。问号表示数据池身份或源媒体依赖仍未完全确认，不把标注 JSONL 当作原图/视频。

| ID | 论文 | 实际训练 / 预训练 / 评测数据 | 资产层说明与未确认项 |
|---|---|---|---|
| P0068 | DriveWorld-VLA | **NAVSIM、nuScenes；ReCogDrive 式 VLM 预训练池（候选）** | 论文未给完整 12 源图像清单；与 ReCogDrive 的具体同一性及实际媒体清单未闭合。 |
| P0069 | Uni-World VLA | **NAVSIM；nuPlan 轨迹消融** | nuPlan 轨迹消融不等于使用 nuPlan 全部相机、LiDAR 或数据库。 |
| P0070 | SGDrive | **NAVSIM；SGDrive 驾驶 QA 与轨迹 QA 标注** | 公开 JSONL 全量扫描：85,109 rows、340,436 image path refs、126,032 个 NAVSIM/OpenScene family-scoped unique paths；原媒体 byte 与 archive hash 未核。 |
| P0071 | FSDrive | **nuScenes 图像/标注、OmniDrive-nuScenes QA、DriveLM GVQA；NAVSIM / DriveLM 评测** | QA 标注与 nuScenes 原始图像分层登记；评测包不替代原图。 |
| P0072 | DriveVLA-W0 | **nuPlan、NAVSIM；私有 70M 帧 / 百万级 clips** | 私有数据单独记为 PRIVATE/UNKNOWN；不得用公开数据包替代。 |
| P0073 | CoT4AD | **nuScenes、旧版 Bench2Drive** | 按论文实际版本登记，不以新版包替换旧版。 |
| P0074 | WAM-Flow | **nuPlan（论文称 668K）、NAVSIM 103K RL、ReCogDrive 驾驶 QA、LLaVA-v1.5 通用 VQA（论文称 3.4M）；公开的 navsim_668k.jsonl 与论文各阶段映射未确认** | pretrain.yaml 的 665K 配置与论文 3.4M 来源映射未知；公开的 navsim_668k.jsonl 是 NAVSIM 标注，不能替代该通用 VQA 图像；各阶段映射、图像路径与 split 未确认。 |
| P0075 | ExploreVLA | **NAVSIM、nuScenes、HUGSIM 四域场景** | 记录论文使用的 HUGSIM 重建场景；不自动追加 KITTI-360、Waymo、PandaSet 原始全集。 |
| P0076 | UniDriveVLA | **FineVision + 驾驶 VQA 混合训练、nuScenes、旧版 Bench2Drive；DriveBench 与七项通用 VQA 评测** | FineVision 实际分卷/抽样及 DriveBench 完整 corruption 文件清单未知。七项通用 VQA 集在 §13 单列。 |
| P0077 | UniDrive-WM | **旧版 Bench2Drive、nuScenes、混合 VQA；DriveLM 与 Chat-B2D 评测** | 混合 VQA 的组成未完整命名；Chat-B2D 与 Bench2Drive 的标注/原图依赖分开记。 |

逐篇原文链接见[WAM+VLA 原文清单](../../papers/WAM_VLA_PAPER_LIST.md)及[22 篇专项账本](WAM_22_dataset_asset_register_2026-09-28.md)。容量和官方包证据不在此重复。
