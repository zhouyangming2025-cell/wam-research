# WAM / 一段式自动驾驶数据集领域盘点（2026-09-21）

## 0. 目的与边界

本文件只回答一个问题：

> **WAM（World / World-Action Model）与 planning-centric 一段式 / 端到端自动驾驶论文，实际在使用哪些公开数据集、benchmark 与数据扩展？我们 210 开发机当前已经有哪些？**

本文件用于后续数据准备，不承担论文复现工程。以下内容**不把**作者自行生成的 feature cache、latent cache、trajectory anchors、pseudo labels、teacher trajectories、reward cache、VAD pickle、metric cache、模型 checkpoint 等普通中间资产当作“基础数据集”。

本文件也**不提出下一步下载优先级**。下载源、版本、许可、实际体量、网络可达性、是否需要全量下载，下一步应另做全网检索后再决定。

### 统计范围

1. **核心 12 篇**：仓库当前用于 WAM 机制分析的 12 篇核心论文，逐篇以 `papers/raw_md/` 原文 Markdown 为主。
2. **扩展样本**：补充查看与 WAM、world-model-enhanced planning、一段式端到端规划高度相关的代表性论文 / 官方项目，包括 DriveDreamer、Drive-WM、OccWorld、Drive-OccWorld、DrivingGPT、ReSim、DriveVLA-W0、PWM、ResWorld、WorldRFT、Latent-WAM、SparseWorld、DriveWAM、SimWAM、PLAN-S、Vista。
3. **机器现状**：以提交 `ea2f5f9330e8591080e56b4da293f7c0e18739ef` 中的 `datasets/resource_inventory_20260921.md` 为现场事实。
4. 扩展样本用于发现领域数据趋势，**不是声称穷尽整个领域**。文中的频次统计只表示本次“核心 12 + 代表性扩展样本”的出现次数。

---

## 1. 先把数据关系理清楚

这个领域最容易混淆的是：原始数据集、再分发数据层、规划 benchmark、模拟器不是同一种东西。

```text
真实道路数据
├── nuScenes
│   ├── Occ3D-nuScenes
│   ├── nuScenes-Occupancy
│   ├── Turning-nuScenes
│   ├── Adv-nuSc
│   └── nuScenes-C
│
└── nuPlan
    └── OpenScene（nuPlan 的 2 Hz compact redistribution）
        ├── NAVSIM v1
        └── NAVSIM v2

CARLA（模拟器）
└── Bench2Drive（标准化训练数据 + 220-route 闭环 benchmark）

大规模驾驶视频 / 新一代预训练数据
├── OpenDV-YouTube
├── PhysicalAI-Autonomous-Vehicles
├── CoVLA
└── DrivingDojo

真实场景重建闭环 benchmark
└── HUGSIM
    └── 由 KITTI-360 / Waymo / nuScenes / PandaSet 场景重建而来
```

最重要的口径：

- **nuScenes 与 nuPlan 是两个独立真实驾驶数据集。**
- **OpenScene 不是第三套独立采集数据**，而是 nuPlan 的紧凑再分发 / 重组织版本，主要保留 2 Hz 相关传感器和标注。
- **NAVSIM 是建立在 OpenScene / nuPlan 数据体系上的 planning benchmark**。它定义标准 split、planner 输入输出、仿真评分和指标。
- **Bench2Drive 是 CARLA 生态中的标准化 E2E 训练 / 闭环评测 benchmark**；CARLA 本身是模拟器，不应和 Bench2Drive 数据包混为一谈。
- **Occ3D、nuScenes-Occupancy、Turning-nuScenes、Adv-nuSc、nuScenes-C** 是对基础数据的标注或测试扩展，不是重新采集的一整套驾驶传感器数据。

---

## 2. 核心 12 篇：数据集使用矩阵

“使用”包括训练、微调或论文实际报告的主要 / 补充评测；括号中注明特殊情况。

| 论文 | 直接使用的主要公开数据 / benchmark |
|---|---|
| **Epona** | nuPlan、nuScenes、NAVSIM v1 |
| **WoTE** | NAVSIM v1、Bench2Drive |
| **WorldDrive** | nuPlan、nuScenes、NAVSIM v1、NAVSIM v2 |
| **LAW** | nuScenes、NAVSIM v1、CARLA/Roach 专家采集数据 |
| **World4Drive** | nuScenes、NAVSIM v1 |
| **DriveLaW** | nuPlan、nuScenes、NAVSIM v1 |
| **SeerDrive** | NAVSIM v1、nuScenes；Bench2Drive（附录补充） |
| **Drive-JEPA** | CoVLA、DrivingDojo、OpenScene、NAVSIM v1、NAVSIM v2、Bench2Drive |
| **Metis** | NAVSIM v2、CityWalker；NAVSIM v1（补充对比） |
| **DynFlowDrive** | nuScenes、NAVSIM v1 |
| **Discrete-WAM** | nuPlan、NAVSIM v1、NAVSIM v2 |
| **GraphWorld** | nuScenes、NAVSIM v1、NAVSIM v2、Bench2Drive；Turning-nuScenes / Adv-nuSc / nuScenes-C（鲁棒性扩展） |

### 核心 12 的出现频次

| 数据体系 | 核心 12 中出现 | 说明 |
|---|---:|---|
| **NAVSIM v1** | **12 / 12（任意使用）** | 11 篇是主训练/主评测体系；Metis 主要用 v2，但附加报告 v1 |
| **nuScenes** | **8 / 12** | 仍是最常见的开环规划 / world representation / 视频生成基础数据 |
| **NAVSIM v2** | **5 / 12** | WorldDrive、Drive-JEPA、Metis、Discrete-WAM、GraphWorld |
| **nuPlan（直接使用）** | **4 / 12** | Epona、WorldDrive、DriveLaW、Discrete-WAM；不把“经 OpenScene 间接继承 nuPlan”重复计入 |
| **Bench2Drive** | **4 / 12** | WoTE、SeerDrive、Drive-JEPA、GraphWorld |
| **CoVLA** | 1 | Drive-JEPA 的驾驶视频预训练数据 |
| **DrivingDojo** | 1 | Drive-JEPA 的驾驶视频预训练数据 |
| **CityWalker** | 1 | Metis 城市机器人导航 |
| **CARLA/Roach 专家数据** | 1 | LAW 的 CARLA 版本 |

这个结果说明，核心 12 的公共数据底座高度集中：**nuPlan → OpenScene → NAVSIM** 是最强主干，**nuScenes** 是第二主干，**Bench2Drive/CARLA** 提供更强的反应式闭环验证。

---

## 3. 扩展论文样本：领域正在使用什么

下面不是新的“核心论文名单”，而是为了扩大数据集视野而加入的代表性 WAM / world-model-enhanced / E2E planning 论文。

| 论文 | 年份/定位 | 主要数据集 / benchmark |
|---|---|---|
| **DriveDreamer** | ECCV 2024，早期真实驾驶 world model | nuScenes |
| **Drive-WM** | CVPR 2024，多视角世界生成 + planning | nuScenes |
| **OccWorld** | ECCV 2024，3D occupancy world model | nuScenes + Occ3D occupancy GT |
| **Drive-OccWorld** | AAAI 2025，4D occupancy forecasting + planning | nuScenes、nuScenes-Occupancy、Lyft-Level5 |
| **DrivingGPT** | ICCV 2025，统一 world modeling + planning | nuPlan、NAVSIM |
| **ReSim** | NeurIPS 2025，可靠 action-conditioned world simulation | OpenDV-YouTube、NAVSIM、CARLA 非专家数据 |
| **DriveVLA-W0** | ICLR 2026，world modeling 扩展 VLA 数据规模 | nuPlan 预训练、NAVSIM v1/v2；另有 680× in-house 数据（非公开） |
| **PWM / Policy World Model** | NeurIPS 2025，forecasting→planning | OpenDV-YouTube、nuScenes、NAVSIM；另用 CC12M / FineWeb 保持通用图文/文本能力 |
| **ResWorld** | ICLR 2026，latent residual world model | nuScenes、NAVSIM |
| **WorldRFT** | AAAI 2026，latent world model + RFT | nuScenes、NAVSIM |
| **Latent-WAM** | 2026，latent world-action modeling | NAVSIM v2、HUGSIM |
| **SparseWorld** | 2026，稀疏 scene world model | nuScenes、Bench2Drive |
| **DriveWAM** | 2026，video prior + world-action modeling | NAVSIM、PhysicalAI-Autonomous-Vehicles |
| **SimWAM** | 2026，训练期未来视频监督 | NAVSIM / NAVSIM v2、PhysicalAI-Autonomous-Vehicles；另报告 nuScenes 迁移 |
| **PLAN-S** | 2026，planner-facing latent dynamics bridge | ResWorld/nuScenes、WoTE/NAVSIM |
| **Vista** | NeurIPS 2024，上游 driving world model | OpenDV-YouTube、nuScenes |

### “核心 12 + 16 篇扩展样本”中的出现频次

该表只表示本次 **28 篇代表性样本**，不等于领域论文总数。

| 数据体系 | 28 篇中出现次数 | 观察 |
|---|---:|---|
| **NAVSIM v1** | **21** | 当前 planning-centric WAM 最集中的统一评测 / 微调底座 |
| **nuScenes** | **19** | 经典开环规划、world representation、occupancy 与生成实验仍高度依赖 |
| **NAVSIM v2** | **8** | 2025–2026 明显增加 |
| **nuPlan（直接使用）** | **6** | 主要承担大规模真实视频 / world-model 预训练 |
| **Bench2Drive** | **5** | 作为真正 CARLA 闭环验证的重要补充 |
| **OpenDV-YouTube** | **3** | 大规模无标注/弱标注驾驶视频预训练开始进入 WAM |
| **PhysicalAI-Autonomous-Vehicles** | **2** | 2026 新一代大规模 world-action 预训练数据趋势 |
| **CoVLA** | 1 | 带 CAN / trajectory / language 的真实驾驶视频 |
| **DrivingDojo** | 1 | 交互行为 / open-world 驾驶视频 |
| **CityWalker** | 1 | 跨 embodiment 城市导航 |
| **HUGSIM** | 1 | photorealistic reactive closed-loop benchmark |
| **Lyft-Level5** | 1 | occupancy world-model 分支 |
| **Occ3D / nuScenes-Occupancy** | 各 1 | nuScenes 上的 occupancy 标注扩展 |

**趋势判断（仅基于本次样本）：**

1. 2024–2025 的 planning-centric WAM 主要围绕 **nuScenes + nuPlan/OpenScene/NAVSIM**。
2. 2025–2026 开始出现明显的“**大规模驾驶视频预训练 → NAVSIM / E2E planning 适配**”路线，代表数据是 **OpenDV-YouTube、CoVLA、DrivingDojo**。
3. 2026 又出现更大规模的 **PhysicalAI-Autonomous-Vehicles**，DriveWAM / SimWAM 已直接使用。
4. 对闭环可信度更高的评测，数据形态从 **NAVSIM 非反应式 log replay** 扩展到 **NAVSIM v2 two-stage / reactive traffic、Bench2Drive/CARLA、HUGSIM**。

---

## 4. 领域数据集详细登记

### 4.1 nuPlan

**类型**：大规模真实道路驾驶日志 / planning 数据基础。

**论文里的规模口径**：
- DriveLaW 将其描述为约 **1,200 h** 人类驾驶数据；
- DrivingGPT 论文写为 **1,282 h**、四座城市，并指出公开完整传感器数据只覆盖约 **128 h**。
- 因论文版本与统计口径不同，本盘点不把 1,200 与 1,282 当作冲突，而记为：**总日志为千小时级，公开 full-sensor 子集远小于总时长**。

**主要数据形态**：多相机、LiDAR、ego 状态 / 轨迹、地图等。不同 WAM 论文经常只抽取前视 camera 视频用于 world-model pretraining。

**在本领域的用途**：
- 大规模真实视频 / world model 预训练：Epona、WorldDrive、DriveLaW、Discrete-WAM、DrivingGPT、DriveVLA-W0。
- 上游还构成 OpenScene / NAVSIM 的数据来源。

**210 当前状态**：**部分覆盖**。
- 已有约 **1.62 TiB**；
- 主要是 test sensor blobs、mini DB、mini LiDAR、maps、单个已解包 CAM_F0 日志；
- **未发现 raw trainval camera/LiDAR archive**；
- 因此当前不能称为 “nuPlan Full”。

---

### 4.2 OpenScene

**类型**：nuPlan 的 compact redistribution / 再组织数据层，不是重新采集的独立数据集。

**官方特征**：
- 保留与研究相关的传感器和标注并降到 **2 Hz**；
- 覆盖 **120+ h**；
- OpenScene v1.1 的 trainval + test sensor data 约 **2 TB**；
- 额外提供 3D box、occupancy、flow 等标注。

**用途**：
- E2E planning；
- occupancy；
- visual / world-model pretraining；
- NAVSIM 的数据基础。
- Drive-JEPA 明确把 OpenScene trainval 与 CoVLA、DrivingDojo 一起用于驾驶视频预训练。

**210 当前状态**：**已覆盖**。
- `openscene-v1.1` 约 **2.37 TiB**；
- 属于当前正式数据池中最大的单项组成。

---

### 4.3 NAVSIM v1

**类型**：基于 OpenScene / nuPlan 的 planning benchmark，而非独立采集数据。

**标准数据口径**：
- OpenScene 原始 log / scenario 层常写作 **1,192 navtrain scenarios / 136 navtest scenarios**；
- NAVSIM 标准过滤后，学习 / 评测层常写作约 **103k navtrain samples / 12k navtest samples**。
- “scenario 数”和“filtered planning sample 数”是两个层级，不能互换。

**测试机制**：
- planner 在一个 decision point 只调用一次；
- 输出未来约 4 s ego trajectory；
- ego 由 LQR + vehicle model rollout；
- 其他 traffic actor replay logged future，不响应 ego；
- 用 NC / DAC / TTC / Ego Progress / Comfort 汇总为 PDMS；
- 不需要生成未来相机画面，也不执行“新 observation → 再规划”的连续策略闭环。

**用途**：本次核心 12 几乎全覆盖，是 planning-centric WAM 最集中统一的训练 / 评测底座。

**210 当前状态**：**已覆盖**。
- `openscene/navsim` 约 **418.22 GiB**。

---

### 4.4 NAVSIM v2

**类型**：NAVSIM 的升级 planning benchmark，仍属于 OpenScene / nuPlan 数据谱系。

**相对 v1 的关键扩展**：
- EPDMS 扩展规则 / 舒适性等评分；
- 支持 reactive traffic policy；
- `navhard_two_stage` 引入 synthetic follow-up observation，用于两阶段 pseudo-closed-loop；
- 不能把“使用 NAVSIM v2”自动等同于“使用 two-stage”：`navtest` 与 `navhard` 要分开。

**代表规模**（Metis / v2 论文常见口径）：
- `navtest`：约 **12,146** real-world scenarios；
- `navhard` Stage 1：**244** real safety-critical scenarios；
- Stage 2：**4,164** 3DGS-generated synthetic follow-up scenarios。

**用途**：WorldDrive、Drive-JEPA、Metis、Discrete-WAM、GraphWorld、DriveVLA-W0、Latent-WAM、SimWAM 等较新工作。

**210 当前状态**：**已覆盖**。
- `openscene/navsim-v2` 约 **46.79 GiB**；
- 盘点中明确包含 navhard two-stage current/history、scene pickles、private-test-hard、warmup。

---

### 4.5 nuScenes

**类型**：独立真实自动驾驶多传感器数据集，与 nuPlan 无父子关系。

**规模**：
- **1,000 scenes**；
- 标准 split 常用 **700 train / 150 val / 150 test**；
- 每个 scene 约 20 s，总量约 5.5 h；
- 6 cameras + LiDAR + radar + ego / map / 3D annotations。

**在 WAM / E2E planning 中的典型用途**：
- 3 s 开环 trajectory planning；
- future latent / BEV / occupancy supervision；
- world-model / video generation；
- 长时规划与鲁棒性测试。

**代表论文**：Epona、WorldDrive、LAW、World4Drive、DriveLaW、SeerDrive、DynFlowDrive、GraphWorld，以及 DriveDreamer、Drive-WM、OccWorld、Drive-OccWorld、PWM、ResWorld、WorldRFT、SparseWorld、PLAN-S、Vista 等。

**210 当前状态**：**基本完整覆盖**。
- Core Full 13 archives；
- CAN bus；
- Map Expansion v1.3；
- camera supplement；
- 合计约 **0.356 TiB**。

---

### 4.6 Bench2Drive

**类型**：CARLA 生成的标准化 E2E-AD 训练数据 + 反应式闭环 benchmark。

**旧版 / 论文常见口径**：
- 原始论文官方训练数据约 **2M annotated frames / 13,638 clips**；
- Base 子集常用 **1,000 clips（950 train + 50 open-loop val）**；
- 闭环评测为 **220 routes**。

**2026 年 v0.0.4**：
- 新训练集：**44 scenarios × 25 routes = 1,100 routes**；
- 新 validation：**44 × 5 = 220 routes**；
- w/o depth 约 **400 GB**；
- depth 部分约 **7.3 TB**。

**用途**：WoTE、SeerDrive（附录）、Drive-JEPA、GraphWorld、SparseWorld 等。

**210 当前状态**：**已覆盖 v0.0.4 no-depth + map**。
- no-depth 约 **415.36 GB**；
- maps 约 **3.15 GB**；
- **当前盘点未见 v0.0.4 depth 数据**。
- 需要注意：部分论文报告的是旧版 Base / v0.0.3 协议，机器上现存 v0.0.4，论文复现时需另核对版本，但这属于后续复现工作。

---

### 4.7 OpenDV-YouTube

**类型**：超大规模互联网驾驶视频预训练数据。

**官方规模**：
- **1,700+ h**（PWM 论文使用口径为 **1,747 h**）；
- 244+ cities、40 countries；
- 主要是真实前视驾驶视频；
- 官方说明 raw videos 约 **3 TB**，预处理连续图像约 **24 TB**；
- OpenDV-mini raw 约 **44 GB**、processed images 约 **390 GB**。

**用途**：
- GenAD / Vista 等 driving world model；
- ReSim；
- PWM；
- 代表了 WAM 从“小规模高标注数据”转向“大规模弱标注视频预训练”的数据路线。

**210 当前状态**：**正式数据根盘点未见**。

---

### 4.8 PhysicalAI-Autonomous-Vehicles

**类型**：NVIDIA 2026 大规模多传感器真实驾驶数据。

**官方规模**：
- **1,700 h**；
- **306,152 × 20 s clips**；
- **25 countries、2,500+ cities**；
- 所有 clips 有 7 cameras；
- 298,326 clips 有 LiDAR；
- 160,761 clips 有 radar；
- 含 ego-motion、calibration、machine labels；
- 总体量约 **133 TB**。

**在当前 WAM 论文中的用法**：
- DriveWAM 直接训练 / 评测；其实现只取 `camera_front_wide_120fov` + egomotion + calibration；
- SimWAM 跟随 DriveWAM 的 PhysicalAI 数据处理与 split。

**意义**：这是 2026 WAM 数据扩展里非常重要的新信号：研究开始从 NAVSIM 的几十 / 百小时级转向真正千小时级、跨国家的大规模真实驾驶数据。

**210 当前状态**：**正式数据根盘点未见**。

---

### 4.9 CoVLA

**类型**：真实驾驶视频 + vehicle/CAN action + trajectory + language。

**官方规模**：
- **80+ h**；
- **10,000 个 30 s clips**；
- front camera + CAN-derived trajectories / vehicle states；
- 带细粒度语言描述；
- Hugging Face 为 gated access。

**用途**：Drive-JEPA 将 CoVLA 与 DrivingDojo、OpenScene 一起用于 V-JEPA 驾驶视频自监督预训练。

**210 当前状态**：**正式数据根盘点未见**。

---

### 4.10 DrivingDojo

**类型**：专门面向 interactive driving world model 的视频数据集。

**官方规模**：
- **18.2k videos**；
- Action：**7.9k**；
- Interplay：**6.4k**；
- Open：**3.9k**；
- 提供 camera、ego trajectory，Open 子集还提供文本描述；
- 官方发布结构中约 **45 个 tar.gz**，每个约 400 videos。

**用途**：Drive-JEPA 的驾驶域视频预训练；同时也是 driving world-model 预训练的重要独立数据源。

**210 当前状态**：**正式数据根盘点未见**。

---

### 4.11 CityWalker

**类型**：城市第一视角 / 机器人导航数据体系。

**Metis 实际使用口径**：
- **15 h teleoperation data**；
- **6 h fine-tuning + 9 h testing**；
- front-view observation + teleoperation trajectory；
- 用于验证 WAM 从汽车规划向城市机器人导航跨 embodiment 泛化。

**注意**：CityWalker 项目本身还涉及规模更大的网络城市行走 / 驾驶视频，但不能把这些全部自动等同于 Metis 实验所用的 15 h benchmark split。

**210 当前状态**：**正式数据根盘点未见**。

---

### 4.12 Occ3D

**类型**：3D occupancy annotation benchmark，而非新的原始 sensor corpus。

**基础数据**：
- Occ3D-nuScenes 基于 nuScenes；
- Occ3D-Waymo 基于 Waymo。

**用途**：OccWorld 明确要求 nuScenes + Occ3D semantic occupancy GT。对于 occupancy-world-model 分支，只有 nuScenes 原始 sensor 并不等价于拥有 Occ3D label。

**210 当前状态**：**正式数据根盘点未单列 / 未确认 Occ3D label 包**。

---

### 4.13 nuScenes-Occupancy

**类型**：nuScenes 上的 fine-grained occupancy annotation 扩展。

**用途**：Drive-OccWorld 使用该标注体系进行细粒度 occupancy forecasting；其代码也支持由 Cam4DOcc 生成 inflated occupancy annotations。

**210 当前状态**：**正式数据根盘点未单列 / 未确认**。

---

### 4.14 Lyft-Level5

**类型**：独立真实自动驾驶数据集。

**本次样本中的用途**：Drive-OccWorld 在 nuScenes、nuScenes-Occupancy 与 Lyft-Level5 上验证 4D occupancy forecasting / world modeling。

**210 当前状态**：**正式数据根盘点未见**。

---

### 4.15 HUGSIM

**类型**：真实场景 3DGS 重建形成的 photorealistic、real-time、closed-loop simulator benchmark；不是普通 log-replay 数据集。

**官方规模**：
- **70+ reconstructed sequences**；
- 来源包括 KITTI-360、Waymo、nuScenes、PandaSet；
- **400+ varying scenarios**；
- 运行中会根据控制更新 ego / actors / observation，属于真正的 photorealistic closed-loop 测试体系。

**用途**：Latent-WAM 直接在 NAVSIM v2 + HUGSIM 上实验。

**210 当前状态**：**正式数据根盘点未见 HUGSIM 发布场景包**。机器已有 nuScenes 并不自动等于已有 HUGSIM 的重建 scene / scenario 资产。

---

### 4.16 CARLA / Roach 采集数据

**CARLA 本质**：交互式模拟器，而不是固定的真实数据集。

**与本领域的关系**：
- Bench2Drive 是 CARLA 上标准化采集并发布的数据 + benchmark；
- LAW 使用 Roach expert 采集约 **189K frames** 训练其 CARLA 版本；
- ReSim 额外使用 CARLA 产生的非专家 / 危险行为数据补足真实 expert data 的行为分布。

**210 当前状态**：
- 已有 Bench2Drive v0.0.4 no-depth / maps；
- 本盘点不把“是否安装指定 CARLA 版本、是否已有 Roach 189K 自采数据”纳入基础数据集下载状态。

---

## 5. nuScenes 的派生 benchmark / annotation：不要和原始 nuScenes 重复计数

| 名称 | 来源 | 实质 | 本次代表论文 |
|---|---|---|---|
| **Occ3D-nuScenes** | nuScenes | 3D semantic occupancy GT | OccWorld |
| **nuScenes-Occupancy** | nuScenes | fine-grained occupancy labels | Drive-OccWorld |
| **Turning-nuScenes** | nuScenes val | 高曲率 / 转弯困难子集，GraphWorld 论文给出 680 samples / 17 scenes | GraphWorld |
| **Adv-nuSc** | nuScenes val | 加入 adversarial traffic participant trajectory 的鲁棒性 benchmark | GraphWorld |
| **nuScenes-C** | nuScenes val | 27 类 corruption × 5 severity 的感知鲁棒性 benchmark | GraphWorld |

从“你的数据下载职责”角度，这些应标成 **annotation / derived benchmark extension**，而不是重复下载一份 nuScenes raw sensor 数据。

---

## 6. 不计入“基础数据集下载清单”的论文复现资产

以下资源可能对复现某篇论文是必要的，但本文件故意不把它们计为领域基础数据集：

- VAD / UniAD / 作者生成的 `*.pkl` 元信息；
- trajectory anchors / K-Means centers；
- WoTE imitation / simulation reward cache；
- Drive-JEPA pseudo-teacher trajectories；
- metric cache；
- future BEV / latent cache；
- Grounded-SAM / Metric3D 产生的 pseudo semantic / depth；
- tokenizer VQ code / latent code；
- teacher checkpoint / pretrained backbone；
- 由代码在线生成的 Cam4DOcc inflated occupancy；
- 单篇论文作者自己生成但没有形成独立公开数据集的 expert / synthetic intermediates。

唯一例外是：如果某类衍生资产已经形成**有正式名称、独立发布、被多篇论文复用的公共 benchmark / annotation dataset**（例如 Occ3D、nuScenes-Occupancy、HUGSIM scenes），则单独列入本盘点。

---

## 7. 210 开发机：按“领域数据底座”重新看覆盖情况

依据 `datasets/resource_inventory_20260921.md`：

| 数据体系 | 210 状态 | 现场事实 |
|---|---|---|
| **nuScenes** | **已覆盖** | Core Full + CAN bus + Map Expansion + camera supplement，约 0.356 TiB |
| **OpenScene v1.1** | **已覆盖** | 约 2.37 TiB |
| **NAVSIM v1** | **已覆盖** | 约 418.22 GiB |
| **NAVSIM v2** | **已覆盖** | 约 46.79 GiB，含 navhard two-stage 等 |
| **Bench2Drive v0.0.4** | **部分模态完整** | no-depth + maps 已有；depth 未在正式盘点中出现 |
| **nuPlan** | **部分覆盖** | 1.62 TiB 主要是 test / mini / maps；**缺 raw trainval sensor data** |
| **OpenDV-YouTube** | **盘点未见** | 正式数据根未出现 |
| **PhysicalAI-Autonomous-Vehicles** | **盘点未见** | 正式数据根未出现 |
| **CoVLA** | **盘点未见** | 正式数据根未出现 |
| **DrivingDojo** | **盘点未见** | 正式数据根未出现 |
| **CityWalker** | **盘点未见** | 正式数据根未出现 |
| **Occ3D labels** | **未确认** | inventory 未作为独立项列出 |
| **nuScenes-Occupancy** | **未确认** | inventory 未作为独立项列出 |
| **Lyft-Level5** | **盘点未见** | 正式数据根未出现 |
| **HUGSIM released scenes/scenarios** | **盘点未见** | 正式数据根未出现 |

这里的“盘点未见”只表示 **2026-09-21 正式数据根 inventory 中没有该数据集条目**，不扩张为“机器任何路径绝对不存在”。

### 当前覆盖的结构性特点

开发机已经很好地覆盖了**传统 planning benchmark 主干**：

`nuScenes + OpenScene + NAVSIM v1/v2 + Bench2Drive`

真正没有覆盖的是两类：

1. **直接大规模 world-model / WAM 预训练语料**：nuPlan raw trainval、OpenDV-YouTube、PhysicalAI-AV、CoVLA、DrivingDojo。
2. **特定分支的公共扩展数据**：CityWalker、Occ3D / nuScenes-Occupancy、Lyft-Level5、HUGSIM released scenes 等。

这只是事实分类，**不等于下载优先级**。

---

## 8. 论文 → 基础数据源快速索引

### 核心 12

| 论文 | 基础训练数据 | 主要 benchmark / 评测数据 |
|---|---|---|
| Epona | nuPlan + nuScenes | NuPlan test、nuScenes、NAVSIM |
| WoTE | NAVSIM/OpenScene；Bench2Drive 独立版本 | NAVSIM、Bench2Drive |
| WorldDrive | nuPlan → nuScenes → NAVSIM | nuScenes、NAVSIM v1/v2 |
| LAW | nuScenes；NAVSIM/OpenScene；CARLA expert data | nuScenes、NAVSIM、CARLA |
| World4Drive | nuScenes；NAVSIM/OpenScene | nuScenes、NAVSIM |
| DriveLaW | nuScenes + nuPlan video；NAVSIM planning | nuScenes、NAVSIM |
| SeerDrive | NAVSIM/OpenScene + nuScenes | NAVSIM、nuScenes、Bench2Drive（补充） |
| Drive-JEPA | CoVLA + DrivingDojo + OpenScene；NAVSIM | NAVSIM v1/v2、Bench2Drive |
| Metis | NAVSIM-v2；CityWalker | NAVSIM-v2、NAVSIM-v1（补充）、CityWalker、Go2 实机 |
| DynFlowDrive | nuScenes；NAVSIM/OpenScene | nuScenes、NAVSIM |
| Discrete-WAM | nuPlan；NAVSIM | NAVSIM v1/v2 |
| GraphWorld | nuScenes；NAVSIM；Bench2Drive | nuScenes 系列扩展、NAVSIM v1/v2、Bench2Drive |

### 扩展样本

| 论文 | 基础数据 / benchmark |
|---|---|
| DriveDreamer | nuScenes |
| Drive-WM | nuScenes |
| OccWorld | nuScenes + Occ3D |
| Drive-OccWorld | nuScenes + nuScenes-Occupancy + Lyft-Level5 |
| DrivingGPT | nuPlan + NAVSIM |
| ReSim | OpenDV-YouTube + NAVSIM + CARLA |
| DriveVLA-W0 | nuPlan + NAVSIM v1/v2 + in-house（非公开） |
| PWM | OpenDV-YouTube + nuScenes + NAVSIM；CC12M/FineWeb 是通用辅助语料 |
| ResWorld | nuScenes + NAVSIM |
| WorldRFT | nuScenes + NAVSIM |
| Latent-WAM | NAVSIM v2 + HUGSIM |
| SparseWorld | nuScenes + Bench2Drive |
| DriveWAM | NAVSIM + PhysicalAI-Autonomous-Vehicles |
| SimWAM | NAVSIM / v2 + PhysicalAI-Autonomous-Vehicles；nuScenes 迁移 |
| PLAN-S | nuScenes + NAVSIM（依托 ResWorld / WoTE host） |
| Vista | OpenDV-YouTube + nuScenes |

---

## 9. 目前可以得到的领域结论

1. **NAVSIM 已经成为 planning-centric WAM 最集中的统一训练 / 评测语言。** 核心 12 几乎全部与 NAVSIM v1/v2 有直接关系。
2. **nuScenes 仍然不可替代**：它在开环规划、latent world model、occupancy、world generation、鲁棒性等方向同时出现。
3. **nuPlan 的角色和 NAVSIM 不同**：论文更常把 nuPlan 当作大规模真实视频 / world-model 预训练源，而 NAVSIM 更常承担 standardized planning 训练 / 评测。
4. **OpenScene 应作为 nuPlan→NAVSIM 的中间数据层理解**，而不是与 nuPlan、NAVSIM 并列成三个完全独立的数据采集项目。
5. **WAM 正在明显进入“大数据预训练”阶段**：OpenDV-YouTube、CoVLA、DrivingDojo、PhysicalAI-AV 的出现说明，仅准备 nuScenes/NAVSIM 已经不足以覆盖新一代 world-action model 的数据谱系。
6. **闭环评测数据也在分化**：Bench2Drive/CARLA 是标准反应式模拟闭环；HUGSIM 是真实场景重建的 photorealistic closed-loop；NAVSIM v2 则位于 log-based benchmark 向更强交互评测扩展的中间位置。
7. 对当前数据准备工作而言，应坚持区分：
   - **基础公开数据集 / benchmark：需要盘点与下载；**
   - **论文作者衍生资产：留给后续复现工程处理。**

---

## 10. 下一步边界

本次工作到此为止，只完成“**领域到底用什么数据 + 210 已有什么**”的事实盘点。

下一步若要决定“具体下载什么”，应另开一轮全网检索，对每个候选数据逐项核对：

- 官方下载源 / 镜像；
- 许可证和 gated access；
- 当前可下载版本；
- raw / processed / modality 分包；
- 真正需要的 split；
- 压缩体量与解压体量；
- 是否与 210 已有 OpenScene / nuPlan / nuScenes 内容重复；
- checksum / manifest；
- 是否值得全量下载，还是只下论文实际使用的模态 / subset。

**在完成上述检索前，本文件不输出下载优先级。**

---

## 11. 主要来源

### 本仓库核心论文原文

- [Epona](../papers/raw_md/P0001_Epona/P0001_Epona.raw.md)
- [WoTE](../papers/raw_md/P0045_WoTE/P0045_WoTE.raw.md)
- [WorldDrive](../papers/raw_md/P0042_WorldDrive/P0042_WorldDrive.raw.md)
- [LAW](../papers/raw_md/P0048_LAW/P0048_LAW.raw.md)
- [World4Drive](../papers/raw_md/P0046_World4Drive/P0046_World4Drive.raw.md)
- [DriveLaW](../papers/raw_md/P0009_DriveLaW/P0009_DriveLaW.raw.md)
- [SeerDrive](../papers/raw_md/P0061_SeerDrive/P0061_SeerDrive.raw.md)
- [Drive-JEPA](../papers/raw_md/P0049_DriveJEPA/P0049_DriveJEPA.raw.md)
- [Metis](../papers/raw_md/P0062_Metis/P0062_Metis.raw.md)
- [DynFlowDrive](../papers/raw_md/P0063_DynFlowDrive/P0063_DynFlowDrive.raw.md)
- [Discrete-WAM](../papers/raw_md/P0064_Discrete-WAM/P0064_Discrete-WAM.raw.md)
- [GraphWorld](../papers/raw_md/P0065_GraphWorld/P0065_GraphWorld.raw.md)

### 当前机器盘点

- [2026-09-21 资源盘点](./resource_inventory_20260921.md)
- Inventory commit: `ea2f5f9330e8591080e56b4da293f7c0e18739ef`

### 官方 / 原论文外部资料

- OpenScene: https://github.com/OpenDriveLab/OpenScene
- NAVSIM: https://github.com/autonomousvision/navsim
- Bench2Drive: https://github.com/Thinklab-SJTU/Bench2Drive
- OpenDV / DriveAGI: https://github.com/OpenDriveLab/DriveAGI
- PhysicalAI-Autonomous-Vehicles: https://huggingface.co/datasets/nvidia/PhysicalAI-Autonomous-Vehicles
- CoVLA: https://huggingface.co/datasets/turing-motors/CoVLA-Dataset
- DrivingDojo: https://drivingdojo.github.io/
- Metis: https://github.com/LogosRoboticsGroup/Metis
- Occ3D: https://github.com/Tsinghua-MARS-Lab/Occ3D
- Drive-OccWorld: https://github.com/yuyang-cloud/Drive-OccWorld
- HUGSIM: https://github.com/hyzhou404/HUGSIM
- ReSim: https://github.com/OpenDriveLab/ReSim
- DriveVLA-W0: https://github.com/BraveGroup/DriveVLA-W0
- PWM: https://github.com/6550Zhao/Policy-World-Model
- ResWorld: https://github.com/mengtan00/ResWorld
- DriveWAM: https://github.com/chenshi3/DriveWAM
- SimWAM: https://github.com/H-EmbodVis/SimWAM

### 代表论文

- DriveDreamer: https://arxiv.org/abs/2309.09777
- Drive-WM: https://arxiv.org/abs/2311.17918
- DrivingGPT: https://openaccess.thecvf.com/content/ICCV2025/html/Chen_DrivingGPT_Unifying_Driving_World_Modeling_and_Planning_with_Multi-modal_Autoregressive_ICCV_2025_paper.html
- ReSim: https://proceedings.neurips.cc/paper_files/paper/2025/hash/f502981cbe221d857ad409450a7917c3-Abstract-Conference.html
- DriveVLA-W0: https://proceedings.iclr.cc/paper_files/paper/2026/hash/0d70423f59c5fdd24f0dd3fa52e34623-Abstract-Conference.html
- WorldRFT: https://ojs.aaai.org/index.php/AAAI/article/view/38149
- Latent-WAM: https://arxiv.org/abs/2603.24581
- SparseWorld: https://arxiv.org/abs/2605.24354
- PLAN-S: https://arxiv.org/abs/2606.06014
