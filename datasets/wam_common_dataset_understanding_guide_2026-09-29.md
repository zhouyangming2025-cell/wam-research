# WAM 常用数据集理解指南（2026-09-29）

## 目的与范围

领域数据集目录已经完成第一轮归并。本指南转向“理解数据本身”：解释常见数据集的数据单元、模态与监督、在 WAM 中解决的问题，以及容易混淆的母体、派生包和评测器。它不再扩展论文逐篇统计，也不重复逐对象容量审计。

优先级按仓库已收录论文语料中的重复出现和项目的规划型 WAM 方向确定：在 22 篇核心论文中，NAVSIM 为 19/22、nuScenes 为 15/22、直接 nuPlan 为 7/22、旧版 Bench2Drive 为 7/22；75 篇发现来源池中，相应家族为 nuScenes 38/75、NAVSIM 37/75、直接 nuPlan 20/75、Bench2Drive 14/75。nuScenes、nuPlan/OpenScene/NAVSIM、Bench2Drive 是共同核心；Waymo Open Motion 和大规模驾驶视频是有明确研究价值、但更依赖具体任务的路线。75 篇论文只是数据集发现来源池，22 篇核心论文仍有独立深度账本。频次表示“论文涉及”，不等于复现时下载整包；统计口径见[领域数据集目录](../audits/datasets/wam_field_dataset_census_20260921.md)和[22 篇资产账本](../audits/datasets/WAM_22_dataset_asset_register_2026-09-28.md)。

读任何数据集时，先分清四层：

1. **观测母体**：真实道路或仿真中采集的图像、点云、轨迹等。
2. **标注与索引**：目标框、轨迹、地图、语言问答、占用标签，以及指向媒体的路径。
3. **派生/重组发布包**：从母体筛选、降采样或重新组织出的研究数据。
4. **基准与评测器**：split、场景筛选规则、仿真/评分协议。评测器可以依赖前三层，但不是新采集的一套原始数据。

下文用【原文事实】标记论文发布时的描述，用【官方/作者事实】标记当前项目页或数据文档，用【分析判断】标记这些属性对 WAM 研究和复现的含义。本文没有新增现场 inventory 事实；容量值仍回到已有逐文件清单核验。

这一区分直接对应 WAM 的不同能力：连续图像与动作状态支持动态/视频预测；多传感器和三维标签支持空间表征；规划场景与评分器支持轨迹比较；闭环模拟器用于测交互行为。一个数据集可以覆盖其中一部分，不能因名称或论文频次高就认为它能覆盖全部能力。

## 主干数据的对照

| 数据资产 | 本质与数据单元 | 主要可学/可测内容 | 在 WAM 中的主要价值 | 关键边界 |
|---|---|---|---|---|
| **nuScenes** | 真实道路多传感器日志；以 scene、sample 和 sample_data 组织同步关键帧 | 图像、雷达、激光雷达、3D 框、类别/属性、地图扩展及时间关系 | 场景理解、跨模态融合、占用/问答标注对齐、常见离线规划输入 | 感知数据集属性强；2 Hz 关键帧不能替代高频连续视频，也不是闭环交互评测 |
| **nuPlan** | 真实道路规划日志；数据库索引/状态与外部传感器文件分层 | ego/agent 状态与轨迹、场景/地图关系；公开 raw sensor 子集另含高频图像和点云 | 规划学习、行为分布、具备时间连续性的传感器世界建模 | DB 不含图像/点云本体；“nuPlan”可能指 DB、map 或 sensor blobs，必须问清是哪层 |
| **OpenScene** | nuPlan 的紧凑重组与降采样版本；按 log 提供 metadata 和 sensor blobs | 2 Hz 相机、激光雷达及 occupancy/flow 等三维监督 | 常用的规划/WAM 研究数据层，便于统一日志、训练和评测 | 与 nuPlan 是父子血缘；降低频率和重新组织会改变可学习的时间尺度，不等于 raw nuPlan |
| **NAVSIM** | 基于 OpenScene/nuPlan 的规划 benchmark、split、指标与评估代码 | 传感器输入到 ego 轨迹输出；按规划相关指标评分 | 可重复比较规划模型，提供比单纯轨迹 L2 更贴近驾驶目标的离线评测 | v1 非反应式；v2 增加两阶段 pseudo-simulation/reactive traffic 支持，但仍不能取代图形仿真闭环 |
| **Bench2Drive** | CARLA 生成的专家训练 clip 与闭环 route/scenario benchmark | 受控天气、城镇和交互场景中的多帧传感器、3D/语义标注与专家示范 | 压力测试交互、稀有场景、完成率和闭环能力 | CARLA 是模拟器；Bench2Drive clip、route 评测、地图和模拟器安装是不同资产。新旧版本的数据分布也不同 |

### nuScenes：多模态场景理解底座，不是规划闭环本身

【原文事实】nuScenes 原始论文描述 1,000 段、每段约 20 秒的真实道路场景，传感器包含环视 6 相机、5 个雷达和 1 个激光雷达，并提供 3D 目标框（23 类、8 种属性）等监督。【官方事实】官方数据说明以 2 Hz 发布同步关键帧。其数据 schema 的基本阅读路径是 `scene → sample → sample_data`：`sample` 是对齐的关键时刻，`sample_data` 指向具体传感器文件及时间戳/标定关系。地图通常通过单独的 map expansion 包配合使用；官方 devkit 教程适合从一个 sample 沿 token 找到多传感器观测和标注。

【分析判断】nuScenes 特别适合研究相机与几何/运动信号如何互补、驾驶 QA 如何落到真实图像，以及 occupancy 或对象级表征如何连接到规划。它在 WAM 论文中出现很多，但这并不意味着它是大规模视频世界模型预训练的最佳来源：关键帧/标注结构与连续高频驾驶视频不是一回事；基于 logged trajectory 的离线结果也不能证明模型在交互中安全。

nuScenes 派生的 Occupancy、nuScenes-C、DriveLM/OmniDrive 等应分别理解为**新监督/评测/问答层**。若标注只含 JSON/索引而图像仍引用 nuScenes 原媒体，标注包不会自动包含所需图像；反过来，已有 nuScenes 图像也不代表已拥有这些衍生标注。

### nuPlan → OpenScene → NAVSIM：一个来源体系里的三种研究对象

这条链最容易被误读成三份彼此独立的数据集。更准确的理解是：nuPlan 是真实道路规划日志母体；OpenScene 将适用的 nuPlan 标注和传感器数据重组并降到 2 Hz，另提供 occupancy/flow 等监督；NAVSIM 再从这类场景构建标准化 split、规划输入输出与评分流程。

**nuPlan 需要先拆成数据库层和 sensor 层。**【官方事实】当前官方页面称总体约 1,200 小时驾驶日志，其中公开 raw sensors 约 120 小时，含 8 路相机（10 Hz）、5 路 LiDAR（20 Hz）、IMU/GPS。【原文事实】2021 年论文曾写 1,500 小时和 200+ TB，那是论文阶段口径，不应当作当前发布规格。DB 保存日志、状态/轨迹、传感器索引、场景和地图关系；相机图像和点云保存在外部文件中。只做向量化规划/轨迹学习，可能只需要 DB、maps 和指定 split；要做高频图像条件动态建模，才需要对应 sensor blobs。

**OpenScene 是常用的研究交换层。**【官方/作者事实】项目将其称为 nuPlan 的 compact redistribution，保留相关标注和 2 Hz 传感器数据，覆盖 120 小时以上，并提供 occupancy/flow 监督。相对 raw nuPlan，它降低时间分辨率并重组数据。**【分析判断】**要学 2 Hz 规划或预测模型，OpenScene 往往更直接；要学 10 Hz 视频动力学，不能把 OpenScene 当作等价替代。

**NAVSIM 主要贡献在评测问题定义，而不是另造观测母体。**【原文事实】NAVSIM v1 把真实场景中的传感器输入与非反应式短时仿真指标结合，减少纯 L2 位移误差对合理规划的误导。**【分析判断】**它适合标准化比较“给定记录场景，模型输出的规划是否安全、合规并有进展”；但环境不随模型动作反应，也不积累完整闭环中的误差，因此结果应与 CARLA/HUGSIM 等闭环评测互补。【官方/作者事实】NAVSIM v2 增加两阶段 pseudo-simulation 和 reactive traffic agent 支持；做复现时必须锁定论文所用 v1/v2、devkit revision、split 和指标版本。

容量审计中的关系要这样读：OpenScene 与 NAVSIM 的场景/来源存在父子重叠；独立 archive 可以物理并存，逻辑场景却不能重复解释成新增原始驾驶信息。精确 bytes、发布分卷、private test 边界及各版本差异见 [OpenScene 文件 manifest](../audits/datasets/openscene_v1_1_official_file_manifest_2026-09-28.md)、[nuPlan 文件 manifest](../audits/datasets/nuplan_v1_1_official_file_manifest_2026-09-28.md) 和 [22 篇资产账本](../audits/datasets/WAM_22_dataset_asset_register_2026-09-28.md)；本指南不复算这些数字。

### Bench2Drive：合成多样性和闭环评测

【原文事实】2024 论文描述 44 类交互场景、23 种天气、12 个 CARLA 城镇、13,638 个训练 clip 和 220 条评测路线；clip 按 10 Hz 采样，提供 6 路环视相机、1 路 64 线 LiDAR、5 路 radar、IMU/GNSS，以及 3D 框、depth、语义/实例分割、HD map 和专家估值/特征等监督。【官方/作者事实】项目页在 2026 年的 v0.0.4 调整了训练数据分布：44 类场景各 25 条、共 1,100 条训练 routes，另有 220 条 validation routes，并增加 3D occupancy。**论文数字与当前 release 数字不能混成一个版本。**

把它用于 WAM 时，要分别回答两个问题：训练数据是否提供了模型所需的传感器、动作和时间序列；评测协议是否真的启动仿真闭环并与其他交通参与者交互。若只下载训练 clip，不等于已具备 route benchmark；若安装 CARLA，也不等于已经有 Bench2Drive 训练集。CARLA 的城市场景可控、容易做稀有事件和动作干预，但仿真纹理/动力学分布与真实道路仍有差距，所以适合作为闭环补充，不宜单独代表真实道路泛化。

复现旧论文须使用与其匹配的 Base/Full/旧评测版；当前项目的 v0.0.4 no-depth/map 是另一版资产。depth/occupancy 大包也不应在模型不读取这些模态时默认纳入。当前 release 的身份、文件范围和 bytes 已在 22 篇证据记录中与旧版分开。

## 条件路线：有用，但解决不同问题

| 数据体系 | 它补上的能力 | 不应当误认为 |
|---|---|---|
| **Waymo Open Motion Dataset (WOMD)** | 多主体未来轨迹、交互场景和 3D map；适合 motion forecasting、联合行为预测及轨迹规划 | Waymo 全部相机/LiDAR 原始视频。Waymo 官方仓库把 Perception、Motion、End-to-End Driving 分为不同数据集；论文写 WOMD 时通常应按 Motion 层理解 |
| **OpenDV-YouTube** | 互联网驾驶视频的广域视觉变化，可用于视频预测/视觉先验预训练 | 有同步多相机、精细地图或逐帧车辆动作标签的驾驶日志。作者页面给出的原视频约 3 TB、处理后连续图像约 24 TB 是发布方约数，且二者是不同处理形态 |
| [**CoVLA**](https://huggingface.co/datasets/turing-motors/CoVLA-Dataset) | 前视视频与 CAN/ego 状态、轨迹和语言监督；适合视频表征与驾驶动作/指令对齐 | 可直接替代 nuPlan/OpenScene 的统一规划 benchmark；需按发行版确认许可、split 和论文实际子集 |
| [**DrivingDojo**](https://huggingface.co/datasets/Yuqi1997/DrivingDojo) | 面向交互式 world model 的驾驶视频/动作数据；适合动作条件视频预测 | 与 CoVLA 完全同构或可直接合并；需核对各自序列定义、动作接口及数据协议 |
| [**HUGSIM**](https://huggingface.co/datasets/XDimLab/HUGSIM) | 从选定真实场景构建的可渲染 3D 重建与闭环 replay 环境 | 原始 nuScenes、Waymo、KITTI-360 或 PandaSet 的全量母库；重建 scene 本身是另一个派生资产 |
| **VLA/QA 数据（DriveLM、OmniDrive、ReCogDrive、SGDrive 等）** | 语言问答、指令、推理或动作解释监督 | 原始相机/视频本体。每个标注清单需要沿路径追溯其媒体来源；同一图像也可能通过不同 QA 包重复引用。路径扫描见[媒体路径审计](../audits/datasets/WAM_VLA_MEDIA_PATH_AUDIT_2026-09-29.json) |

这些条件路线仍属于领域数据地图的一部分，但不应和主干混成同一种“数据集”。尤其 VLA 标注集：它的样本数表示标注条目数，不等于唯一图像/视频数；要评估训练能力或容量，须同时知道 annotation、唯一媒体路径、上游母体以及访问许可。

## 从数据集特征到复现实验的判断方法

对目标模型逐项填写下列问题，就能决定应从哪个资产层开始，而不用先下载所有父体：

| 研究问题 | 需要核对的数据字段/资产 | 适合先看的数据体系 |
|---|---|---|
| 模型能否理解周围对象与空间关系？ | 图像/点云同步、坐标标定、3D 框/语义/occupancy | nuScenes；需要长日志时再看 OpenScene |
| 模型能否从连续图像学到未来动态？ | 原始时间戳、帧率、连续片段、ego pose/action、缺帧与相机内外参 | nuPlan raw sensors；OpenDV 作视觉先验；OpenScene 只适合其 2 Hz 时间尺度 |
| 规划输出是否合理？ | 历史输入、场景筛选、轨迹坐标系、指标定义、同版本 split | NAVSIM；同时记录版本和 evaluator |
| 规划遇到动作后果和交互时是否稳定？ | 可控制的参与体、仿真路线、事件触发、闭环失败统计 | Bench2Drive/CARLA；必要时 HUGSIM 场景 |
| 模型能否把语言和驾驶行为联系起来？ | QA/instruction 与准确媒体 URI、轨迹/动作标签、训练/评测隔离 | VLA annotation + 其上游图像/视频；不可只看 JSONL 大小 |

每个具体复现实验最终要从论文/代码抽取的最小规格为：`版本与 revision、split、输入模态、采样频率/时间窗、监督目标、数据坐标系、loader 路径、评测器/指标、媒体是否独立依赖、许可`。缺一项，就将相应资产记为未闭合，不能由家族名称推断。

**对当前项目的学习顺序：**先从 OpenScene/NAVSIM 走通“场景与传感器 → 数据 loader → 规划输出 → 指标”的完整链路，掌握项目规划主干；再用 nuScenes 理解多模态对象/场景标注和 VLA 媒体血缘；然后用 Bench2Drive 认识离线训练数据与模拟器闭环评测的分界；只有研究确实需要高频视频动力学时，再下钻 nuPlan raw sensor 层。WOMD 和 OpenDV 分别作为交互轨迹、广域视频预训练的专项补充。

## 可复核来源

- 本仓库原文（论文事实）：[nuScenes](../papers/raw_md/P0030_nuScenes/P0030_nuScenes.raw.md)、[nuPlan](../papers/raw_md/P0031_nuPlan/P0031_nuPlan.raw.md)、[NAVSIM](../papers/raw_md/P0032_NAVSIM/P0032_NAVSIM.raw.md)、[Bench2Drive](../papers/raw_md/P0033_Bench2Drive/P0033_Bench2Drive.raw.md)。
- nuScenes 官方：[数据集介绍](https://www.nuscenes.org/nuscenes)、[devkit tutorial](https://www.nuscenes.org/tutorials/nuscenes_tutorial.html)。
- nuPlan 官方：[nuPlan 数据页](https://www.nuplan.org/)、[nuPlan devkit](https://github.com/motional/nuplan-devkit)。
- OpenScene 作者发布：[项目主页/README](https://github.com/OpenDriveLab/OpenScene)、[v1.1 下载与数据结构说明](https://github.com/OpenDriveLab/OpenScene/blob/main/docs/getting_started.md)。
- NAVSIM 作者发布：[代码、版本记录、split 与评测文档](https://github.com/autonomousvision/navsim)。
- Bench2Drive 作者发布：[数据版本与 benchmark](https://github.com/Thinklab-SJTU/Bench2Drive)。
- Waymo 官方：[数据集格式与 Perception/Motion/End-to-End 划分](https://github.com/waymo-research/waymo-open-dataset)、[官方数据入口及条款](https://waymo.com/open/)。
- OpenDV 作者发布：[DriveAGI/OpenDV 项目与处理说明](https://github.com/OpenDriveLab/DriveAGI)。
- 容量、版本和资产状态仍以 [22 篇资产账本](../audits/datasets/WAM_22_dataset_asset_register_2026-09-28.md)、[nuPlan manifest](../audits/datasets/nuplan_v1_1_official_file_manifest_2026-09-28.md)、[OpenScene manifest](../audits/datasets/openscene_v1_1_official_file_manifest_2026-09-28.md) 为准。

外部页面于 2026-09-29 核对；页面可能继续更新。涉及发行版本或许可时，以下载/实验当天的对应 release 与 license 为准。
