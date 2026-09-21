# WAM / 一段式自动驾驶数据集领域盘点（2026-09-21）

## 0. 本轮结论

上一版“核心 12 + 16 篇代表性扩展论文”**不足以作为后续下载决策的最终数据底账**。本版已改为对仓库 `papers/raw_md/` 的 **65 个论文条目逐项审计**：

- **64 个条目**：直接读取 `<ID>_<Name>.raw.md` 原文；
- **P0067 ProSim**：仓库当前只有 verified source note，没有 full raw Markdown；因此只使用 source note，并额外核对官方 ProSim 发布页确认其底层使用 **Waymo Open Dataset / WOMD** 与 **ProSim-Instruct-520k**；
- 统计只记录论文**实际训练、微调、主/补充评测、明确构建 benchmark 的数据**；
- **不把 Related Work / reference list 中“提到过”的数据集算作论文使用数据**；
- 作者自行生成的 feature cache、latent cache、trajectory anchors、pseudo labels、reward cache、teacher trajectories、checkpoint 等普通复现中间资产，不纳入“基础数据集下载”盘点；
- 如果作者生成的数据已经成为**独立命名、公开发布或可复用的 dataset / benchmark**，则单独登记，例如 Occ3D、DriveReward、OmniDrive、ProSim-Instruct-520k。

本文件的任务仍然只是：

> **先把这个研究域实际使用的数据集搞清楚，并和 210 当前数据池对齐。**

**本轮不输出下载优先级。** 下载源、版本、许可、gated access、压缩/解压体量、模态选择、重复数据等，下一轮再全网调查。

---

## 1. 65 篇审计后的总体图景

按“论文直接使用或明确作为其 benchmark/source”的口径，仓库 65 个条目中最集中的数据体系如下。

| 数据体系 | 65 条目中直接出现次数 | 说明 |
|---|---:|---|
| **nuScenes** | **31** | 仍是最广泛的真实多传感器基础：E2E、world model、occupancy、生成、鲁棒性都在用 |
| **NAVSIM v1** | **29** | planning-centric WAM / 一段式规划最集中的统一训练与评测体系 |
| **nuPlan（含 mini）** | **17** | 大规模规划/行为数据与 world-model 视频预训练的重要源头；同时是 OpenScene/NAVSIM 上游 |
| **NAVSIM v2** | **13** | 2025–2026 明显增加，尤其用于 navhard / two-stage / EPDMS |
| **Bench2Drive** | **11** | CARLA 反应式闭环的重要标准 benchmark |
| **CARLA 系** | **8** | 包括直接 CARLA、CARLA-v2、RiskBench、Roach 专家采集、SUMMIT 等 |
| **WOMD / Waymo** | **6** | 交互预测、traffic simulation、HUGSIM/BridgeSim/ProSim 的重要数据源 |
| **HUGSIM** | **4** | 真实场景重建的 photorealistic closed-loop benchmark |
| **OpenScene（论文直接写明使用）** | **3** | 注意：NAVSIM 本身建立在 OpenScene/nuPlan 之上，不能把所有 NAVSIM 论文重复计为“直接使用 OpenScene” |
| **OpenDV** | **3** | 大规模驾驶视频 world-model 预训练数据，Vista/PWM/CausalDrive 等使用 |

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
│   ├── RiskBench
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

## 3. 仓库 65 篇论文：逐篇数据审计 ledger

### 3.1 P0001–P0019

| ID | 论文 | 定位 | 实际训练 / 评测 / 构建数据 | 盘点备注 |
|---|---|---|---|---|
| P0001 | Epona | 核心 WAM | **nuPlan、nuScenes、NAVSIM v1** | nuPlan + 700 nuScenes scenes 训练；NuPlan test / nuScenes / NAVSIM 评测 |
| P0002 | SafeDrive | WAM / 安全规划 | **NAVSIM v1、NAVSIM v2、Bench2Drive** | 同时覆盖 PDMS、EPDMS 与 CARLA 闭环 |
| P0003 | GraphAD | 图式 E2E | **nuScenes** | 主数据集 |
| P0004 | BeTop | 交互预测 / 规划 | **nuPlan、WOMD** | nuPlan planning + Waymo Open Motion prediction |
| P0005 | RiskWorld | 风险 world model / simulation | **RiskBench（CARLA）** | RiskBench 由 CARLA 风险场景构成 |
| P0006 | GenDrive | 生成式规划 | **nuPlan** | 训练和 closed-loop planning test 都在 nuPlan |
| P0007 | DriveReward | 奖励模型 / 数据集 | **NAVSIM → DriveReward / DriveReward-Bench** | DriveReward 从 NAVSIM train 构建；另有 QA 预训练混合，见 §6 |
| P0009 | DriveLaW | 核心 WAM | **nuPlan、nuScenes、NAVSIM v1** | 大规模视频预训练 + NAVSIM planning |
| P0010 | TOAD | E2E planning | **NAVSIM v1、NAVSIM v2、HUGSIM** | 同时覆盖 log-based 与 photorealistic closed-loop |
| P0011 | SensitivityShaping | 外围：通用动力学 / OOD | **无统一 AD 基础数据集可列** | 不是本次自动驾驶数据下载主线，避免强行计数 |
| P0012 | DAWAM | WAM | **NAVSIM v1、NAVSIM v2** | planning benchmark 主线 |
| P0013 | BridgeSim | 闭环 simulator / benchmark | **NAVSIM v2、nuPlan、nuScenes、WOMD、CARLA / BridgeSim** | 平台支持多地图/多场景源；不是单一原始数据集 |
| P0014 | ReactSimBench | reactive traffic benchmark | **nuPlan → ReactSim-Bench** | 基于 nuPlan 构建 2,636 个 test scenarios |
| P0015 | CausalDrive | 交互式 world renderer | **OpenDV、nuPlan、SocioDrive-Bench、Bench2Drive/CARLA、NAVSIM** | OpenDV 1,700 h 预训练；SocioDrive-Bench 20K clips，80% nuPlan / 20% CARLA |
| P0016 | CounterfactualPred | 反事实预测 benchmark | **CARLA** | controlled counterfactual GT 来自 simulator |
| P0017 | CRAFT | 闭环 E2E | **Bench2Drive / CARLA** | 闭环 benchmark |
| P0018 | GameFormer | 交互预测 / 规划 | **WOMD、nuPlan** | 两条真实行为数据线 |
| P0019 | M2I | 交互运动预测 | **WOMD** | Waymo motion benchmark |

### 3.2 P0021–P0039

| ID | 论文 | 定位 | 实际训练 / 评测 / 构建数据 | 盘点备注 |
|---|---|---|---|---|
| P0021 | HydraMDP | E2E planning | **NAVSIM v1** | NAVSIM 主线 |
| P0022 | DriveSuprim | E2E planning | **NAVSIM v1、NAVSIM v2、Bench2Drive** | 论文强调不引入额外训练数据 |
| P0023 | iPad | E2E planning | **NAVSIM、Bench2Drive** | 非反应式 + CARLA 闭环 |
| P0024 | DriveVLM | VLM / E2E | **nuScenes、SUP-AD（内部）** | SUP-AD 为非公开自有数据，不能作为公共下载候选 |
| P0025 | OmniDrive | VLM 数据 / 规划 | **nuScenes、OpenLane-v2、OmniDrive、DriveLM** | OmniDrive QA 基于 nuScenes；counterfactual checklist 还用 OpenLane-v2 topology |
| P0026 | ORION | VLM / E2E | **Bench2Drive** | 主要 CARLA E2E benchmark |
| P0027 | Think2Drive | world-model RL | **CARLA-v2** | simulator-generated RL 数据体系 |
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

### 3.3 P0040–P0059

| ID | 论文 | 定位 | 实际训练 / 评测 / 构建数据 | 盘点备注 |
|---|---|---|---|---|
| P0040 | DrivingGPT | WAM | **nuPlan、NAVSIM** | world modeling + planning |
| P0041 | PolicyWM / PWM | WAM | **OpenDV、nuScenes、NAVSIM** | 大视频预训练 → 下游 planning |
| P0042 | WorldDrive | 核心 WAM | **nuPlan、nuScenes、NAVSIM v1/v2** | 多阶段数据链 |
| P0043 | OccWorld | occupancy world model | **nuScenes + Occ3D** | Occ3D 是额外 occupancy GT，不能等同于 raw nuScenes |
| P0044 | DriveOccWorld | occupancy world model | **nuScenes、nuScenes-Occupancy、Lyft-Level5** | 独立 occupancy 扩展 + 独立 Lyft 数据 |
| P0045 | WoTE | 核心 WAM | **NAVSIM v1、Bench2Drive** | BEV world model trajectory evaluation |
| P0046 | World4Drive | 核心 WAM | **nuScenes、NAVSIM v1** | 主实验两套 |
| P0047 | DriveWorld | world-model pretraining | **OpenScene、nuScenes** | OpenScene 大规模 4D pretrain → nuScenes downstream |
| P0048 | LAW | 核心 WAM | **nuScenes、NAVSIM、CARLA/Roach expert** | Roach 189K frames 属作者 CARLA expert 采集 |
| P0049 | Drive-JEPA | 核心 WAM | **CoVLA、DrivingDojo、OpenScene、NAVSIM v1/v2、Bench2Drive** | 本仓库中最明显的多源驾驶视频预训练之一 |
| P0050 | WorldRFT | WAM | **nuScenes、NAVSIM** | open-loop + NAVSIM |
| P0051 | Auto-JEPA | WAM | **NAVSIM v1、NAVSIM v2** | action-oriented latent world model |
| P0052 | ReWorld | WAM | **nuScenes、NAVSIM；UCF-101（辅助 probe）** | UCF-101 仅表示学习线性探针，不是驾驶训练主数据 |
| P0053 | WA-JEPA | WAM | **nuPlan、NAVSIM v1/v2、HUGSIM** | Stage 1 明确 nuPlan multi-view pretrain |
| P0054 | What Truly Matters | 外围：prediction evaluation | **SUMMIT/CARLA 自建 Alignment dataset** | 59,944 自采 simulation scenarios；不是公开驾驶 sensor corpus 主线 |
| P0055 | SLEDGE | generative scene / simulation | **nuPlan** | 生成式驾驶环境主数据源 |
| P0056 | DriveArena | generative closed-loop simulator | **nuScenes；OpenStreetMap；nuPlan 零样本测试** | World Dreamer 700/150 nuScenes；OSM 是地图源 |
| P0057 | UniAD | E2E | **nuScenes** | 标准 E2E 基线 |
| P0058 | VAD | E2E | **nuScenes** | 标准 E2E 基线 |
| P0059 | DiffusionDrive | E2E planning | **NAVSIM、nuScenes** | NAVSIM 主结果 + nuScenes open-loop |

### 3.4 P0060–P0067

| ID | 论文 | 定位 | 实际训练 / 评测 / 构建数据 | 盘点备注 |
|---|---|---|---|---|
| P0060 | DrivoR | E2E planning | **NAVSIM v1、NAVSIM v2、HUGSIM** | navtrain 训练；navhard-two-stage；HUGSIM zero-shot |
| P0061 | SeerDrive | 核心 WAM | **NAVSIM、nuScenes；Bench2Drive（补充）** | future-aware planning |
| P0062 | Metis | 核心 WAM | **NAVSIM v2、CityWalker；NAVSIM v1（补充）** | 自动驾驶 + 城市机器人导航 |
| P0063 | DynFlowDrive | 核心 WAM | **nuScenes、NAVSIM** | 两套独立实验 |
| P0064 | Discrete-WAM | 核心 WAM | **nuPlan、NAVSIM v1/v2** | nuPlan pretraining + NAVSIM post-training |
| P0065 | GraphWorld | 核心 WAM | **nuScenes、NAVSIM v1/v2、Bench2Drive** | 另有 Turning-nuScenes、Adv-nuSc、nuScenes-C robustness |
| P0066 | Safe-Sim | safety-critical traffic simulation | **nuScenes、nuPlan mini** | nuScenes train；nuScenes val + nuPlan mini val |
| P0067 | ProSim | promptable closed-loop traffic simulation | **WOMD + ProSim-Instruct-520k** | 仓库无 raw paper；官方发布确认 prompts/tags 覆盖 WOMD train/val |

---

## 4. 领域基础数据源总表

这一节只保留对后续“是否需要下载”真正有意义的数据实体。

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
| **NAVSIM v1** | OpenScene/nuPlan 上的非反应式 planning benchmark | 29 个条目 | **已有** |
| **NAVSIM v2** | EPDMS + reactive traffic support + two-stage pseudo-simulation | 13 个条目 | **已有** |
| **Bench2Drive** | CARLA E2E train/eval benchmark | 11 个条目 | **已有 v0.0.4 no-depth + maps；depth 未见** |
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

## 8. 哪些东西不要误列成你的“基础数据下载职责”

即使复现时可能需要，也先不纳入基础数据集下载盘点：

- 作者训练产生的 latent / feature cache；
- trajectory anchor / K-Means centers；
- reward cache / metric cache；
- pseudo-teacher trajectories；
- future BEV cache；
- Grounded-SAM / Metric3D 临时 pseudo labels；
- author checkpoint / backbone weights；
- 单篇代码运行时重新生成的 `*.pkl`；
- LAW 的 Roach 189K expert frames、WhatTrulyMatters 的 Alignment-59,944 等**作者自采/自生成实验数据**，除非后续确认作者提供独立公开下载包；
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

## 10. 本轮方法与审计强度

本轮不是关键词扫一遍 references，而是：

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

因此，本版比“核心 12 + 16”更适合作为下一轮下载调查的输入底账。

---

## 11. 下一步边界

**本次到此为止，不做下载推荐。**

下一轮若开始决定“具体下载什么”，应对本文件中的**缺失/部分覆盖项**逐一全网核查：

- 官方 source / mirror；
- dataset version；
- license / gated access；
- raw vs processed；
- train / val / test；
- camera / LiDAR / map / motion / text 等模态；
- 压缩与解压体量；
- checksum / manifest；
- 是否能只下论文真正需要的 subset；
- 是否和 210 的 nuPlan / OpenScene / NAVSIM 数据发生内容重复；
- 是否是独立发布资产，还是必须由代码从已有数据生成。

在上述核查完成以前，不把任何“inventory 未见”自动变成“必须下载”。

---

## 12. Source index

### 仓库 source of truth

原文路径统一为：

`papers/raw_md/<paper_id_name>/<paper_id_name>.raw.md`

例外：

`papers/raw_md/P0067_ProSim/P0067_ProSim.source_note.md`

当前机器数据事实：

- [resource_inventory_20260921.md](./resource_inventory_20260921.md)
- inventory commit: `ea2f5f9330e8591080e56b4da293f7c0e18739ef`

### 关键数据/benchmark 原文条目

- [P0030 nuScenes](../papers/raw_md/P0030_nuScenes/P0030_nuScenes.raw.md)
- [P0031 nuPlan](../papers/raw_md/P0031_nuPlan/P0031_nuPlan.raw.md)
- [P0032 NAVSIM](../papers/raw_md/P0032_NAVSIM/P0032_NAVSIM.raw.md)
- [P0033 Bench2Drive](../papers/raw_md/P0033_Bench2Drive/P0033_Bench2Drive.raw.md)
- [P0034 HUGSIM](../papers/raw_md/P0034_HUGSIM/P0034_HUGSIM.raw.md)

### 本轮额外核验

- ProSim official repository: https://github.com/Ariostgx/ProSim
- ProSim paper: https://arxiv.org/abs/2409.05863

