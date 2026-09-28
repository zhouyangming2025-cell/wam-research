# 22 篇 WAM / WAM+VLA：可能超过 1 TB 的数据资产专项审计

审计日期：2026-09-28。范围锁定于仓库源论文提交 [cb05048dfb822e95d44e52dd85b830c750411e2c](https://github.com/zhouyangming2025-cell/wam-research/tree/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md) 的 12 篇 planning-centric WAM + 10 篇 WAM+VLA；论文实际训练、预训练、微调、验证资产见[逐篇账本](WAM_22_dataset_asset_register_2026-09-28.md)。此文件只回答：哪些实际使用或可能需要的资产会跨过 1 TB；不检查 NAS，不决定下载。

## 判定口径与结论

- TB 按十进制 10^12 byte。官方网页的 TB/GB 是发布方近似标注时保留原精度；精确容量只认文件 listing 的 Size/Content-Length。
- 逐项分为：**确认 >1 TB 的公开包**、**容量 >1 TB 但论文未证实采用该版本/整包**、**论文确实涉及但能否 >1 TB 为 UNKNOWN**。论文说用了某数据集，不等于用了它的完整公开包；行数/帧数/小时数不能直接换算 byte。
- 在 22 篇论文直接相关的发布物中，确认跨过 1 TB 的是 **nuPlan v1.1 公共发布包、OpenScene v1.1 常规包、FineVision 全库**。其中 FineVision 是 UniDriveVLA 使用的上游全集容量，论文代码显示其采样子集，故 4.65 TB **不能当成论文实际读取量**。
- 另有两个官方已标为 TB 级、但不是目标论文已证实使用版本/完整度的 CARLA 包：Bench2Drive Full（约 4 TB）与 v0.0.4 depth（约 7.3 TB）。它们列为版本情景，不加入 22 篇论文实际需求主项。
- 仍有高风险 UNKNOWN：W0 私有 70M 帧、LAW 独立 CARLA 189K 帧、WAM-Flow/VLA 多源 VQA 原图，以及 corruption/私有源媒体。它们使完整上限**无法闭合**。因此“只有三个 TB 级包”只对当前已核实发布包成立，不代表全部潜在资产只有三个或总盘有上限。

## A. 已确认 >1 TB 的发布包

| 数据资产 | 官方/作者发布容量 | 与论文的关系 | 去重与容量解释 |
|---|---:|---|---|
| nuPlan v1.1 当前公开发布 | **20,280,630,002,024 B = 20.280630002024 TB**，169 个官方 S3 对象，含 mini；排除 mini 为 **19.187050050161 TB**。其中 camera/LiDAR 对象 **19.060954001531 TB** | 多篇 WAM/WAM+VLA 将 nuPlan 用作视频/世界模型训练、轨迹或规划数据；实际论文通常读指定 split/场景，不等同整包 | 数字是当前公开 v1.1 对象清单的压缩发布字节，不是解压后大小或各论文所需最小子集。见[逐对象 byte manifest](nuplan_v1_1_official_file_manifest_2026-09-28.md)。 |
| OpenScene v1.1 常规传感器/metadata | **2,506,457,646,127 B = 2.506457646127 TB**，固定 HF revision 的 534 个常规对象；另外 private test 39,224,624,432 B 未并入 | 多篇论文通过 NAVSIM/OpenScene 使用其场景/视频 | OpenScene 是 nuPlan 衍生、约 2 Hz 的传感器母体，和 nuPlan 有场景/内容重叠；两个独立发布包若都保留仍占两份 archive 空间，逻辑独立数据量不可把两包直接相加。详见[逐文件 manifest](openscene_v1_1_official_file_manifest_2026-09-28.md)。 |
| FineVision 全库 | Hugging Face 页面显示 **4.65 TB**、约 24.2M rows | UniDriveVLA 论文/代码使用 FineVision 派生的通用视觉训练样本；作者脚本含 641,439 / 1,141,184 选择记录，联合训练 config 指向 finevision_subset_90k.jsonl | 页面整库大小是完整上游发布包；选样索引不是图像 byte manifest。论文实际图像去重字节、cache 形式与不同训练阶段的并集仍 UNKNOWN。不能直接把 4.65 TB 写成论文必需量。 |

nuPlan 的关键边界：Motional 官方称公开的 raw sensor 是 120 小时、约为 full nuPlan 的 10%，并称这部分约 16 TB；官方 devkit 对完整数据集描述为超过 1,300 小时，Motional 较早页面又给 1,500 小时。当前 S3 清单中 camera/LiDAR 发布对象总和为 19.061 TB。故可作的**分析外推**是：以 120 小时为 10% 线性放大，按官方历史约数得到约 160 TB，按当前对象清单得到约 191 TB；若采用较早 1,500h 全集口径则约 200–238 TB。小时口径、传感器覆盖范围与发布版本并不完全一致，这些是量级敏感性估算，**不是官方全量文件清单、精确值或硬上限**。公开 v1.1 对象清单已闭合；全时段 raw sensor 总量没有闭合。

## B. 已知 >1 TB、但不证明 22 篇论文需要该版本/整包

| 资产/版本 | 发布方容量 | 22 篇论文已核使用范围 | 处理 |
|---|---:|---|---|
| Bench2Drive Full | 约 **4 TB** | 相关论文使用旧 Bench2Drive Base/指定 clips，公开论文材料没有证明读取 Full 全集 | 可选历史版本情景，主需求排除。 |
| Bench2Drive v0.0.4 depth | 约 **7.3 TB** | 该 2026 新版含 depth/3D occupancy；22 篇论文锁定的旧版 Bench2Drive 实验不等于 v0.0.4 depth | 新版 modality 扩展情景，主需求排除。 |
| nuPlan 全时段 raw sensor | 官方资料只给局部 released sensor 与小时比例，未提供完整 raw sensor object manifest | 多篇论文会用 nuPlan，但其论文代码/实验划分不等于下载全部 1,300–1,500h | 量级可能约百 TB；精确值与最大值 UNKNOWN，见 A 节。 |

Bench2Drive 官方 README 同时列 Base 1000 clips 约 400 GB、Full 约 4 TB；新版 v0.0.4 分为 no-depth 约 400 GB 与 depth 约 7.3 TB。版本与模态不同，不能把三个数同时计入同一篇论文，也不能以“论文用 Bench2Drive”推导它需要 4–7.3 TB。

## C. 实际涉及、潜在 >1 TB，但公开容量/子集尚 UNKNOWN

| 资产候选 | 论文原文/作者侧已知信息 | 为什么跨 1 TB 尚不能确认 | 风险 |
|---|---|---|---|
| DriveVLA-W0 私有驾驶集 | 原文称 in-house 约 **70M frames、>1M clips**；含 100 个难例测试场景 | 私有，不提供公开包、模态/分辨率/压缩率及 byte manifest；无法从论文训练步数或公开 nuPlan 代替 | **很高**：帧量极大，最可能显著抬高总量；容量上限 UNKNOWN。 |
| LAW 独立 CARLA/Roach 集 | 原文称 CARLA 0.9.10.1、Roach 教师采集 **189K 帧**；与 Bench2Drive Base 是不同资产 | LAW 作者没有公布该训练集的原始分辨率、模态、编码、帧率或文件 manifest。论文 resize 到 900×256 是模型预处理，不能据此压缩估算原始采集。ThinkTwice 同量级 189K 帧约 8 TB 只可作敏感性参照，绝非 LAW 实测或上限 | **高**：可大于 1 TB，但 UNKNOWN。 |
| WAM-Flow 通用 VQA 原图 | 论文称约 **3.4M** 通用 VQA 样本来自 LLaVA v1.5 系；另用约 3.1M driving QA | 没有论文样本到图像 URI、原始数据源 split 和压缩文件的 manifest。作者仓约 414 MB navsim_668k.jsonl 是 NAVSIM annotation，不能代表 3.4M 通用图像 | **高**：图像源并集未知，不能按样本数换算。 |
| ReCogDrive / SGDrive / DriveWorld-VLA 多源 QA 原媒体 | ReCogDrive 作者发布 17 个 JSONL 共 **3,789,771,567 B**；源表覆盖多个驾驶 QA 数据集。JSONL 是标注，不包含所有原图/视频。已单独发现 LingoQA 媒体包约 61 GB、SUTD Zenodo 20.534 GB（主要为 feature/annotation）；DRAMA 原视频 byte 未公开 | 多个来源可能复用 nuScenes、OpenScene、NAVSIM、Bench2Drive，也有独立视频。全量唯一路径/媒体 ID、逐源 archive bytes 与跨包重复未核清；不能把父包大小相加后当 unique bytes，也不能认为 JSONL 已包含媒体 | **高**：联合源媒体并集是否 >1 TB 为 UNKNOWN。 |
| UniDrive-WM mixed VQA | 论文说使用混合 VQA/driving 数据 | 数据源、样本量、图片/视频打包方式未给完整 manifest | **中高**：名称无法定价，可能和其他 VQA 复用。 |
| GraphWorld 的 nuScenes-C corruption 与 DriveBench 完整腐蚀图像 | GraphWorld 使用 Rain/Snow/Fog 三类天气；nuScenes-C 全 benchmark 有多类 corruption 与 severity。DriveBench 发布评测集包含 corruption images 与 QA | 22 篇具体实验只指向子集；被论文使用的 severity、预生成图像/运行时生成方式、全量文件 manifest/bytes 未被锁定 | **中**：全量派生包可能大，但论文子集不等于 full benchmark；UNKNOWN。 |
| HUGSIM 所用源数据父集（Waymo、KITTI-360、PandaSet、nuScenes） | ExploreVLA 使用 HUGSIM 四域预建重建场景；HUGSIM 场景发布包约 60.7 GB | 要运行发布的 HUGSIM 场景不等于需要完整下载其原始父数据全集。若重做全部 scene reconstruction，具体选段/父集文件清单未知 | **条件项**：完整 Waymo raw 等父体可能跨 TB，但不是论文已证实的下载需求；主清单只计 HUGSIM 发布资产。 |

上述 C 类不允许用“与某个 8 TB 数据规模相似”、帧数×猜测的平均文件大小、数据行数×JPEG 常数补出容量。必须拿到与论文实际 split 对应的源媒体 URI、作者 manifest 或正式 archive byte 才能升级为“确认 >1 TB”。

## D. 明确筛查过、当前公开单包未跨 1 TB

nuScenes 项目资产约 **0.391 TB**；NAVSIM v1 navtrain 官方包约 **0.449 TB**；Bench2Drive Base 与 v0.0.4 no-depth 各约 **0.4 TB**；CoVLA 约 **452 GB**；DrivingDojo 约 **283 GB**。它们单包未过 1 TB；互相组合或附加媒体的总量另算。HUGSIM 约 60.7 GB、CityWalker teleportation 包 6.82 GB、ReCogDrive annotation 3.79 GB，也不是 TB 级媒体包。

## 范围外但容易造成漏项的 TB 级数据（不计入上述 22 篇）

OpenDriveLab 官方 DriveAGI / GenAD 页面称 OpenDV-YouTube 原始视频约 **3 TB**，处理后连续帧约 **24 TB**，mini raw 约 44 GB。当前 22 篇逐篇账本没有将 OpenDV-YouTube 记为实际训练/评测输入，因此这两个大包**不应偷偷加进 22 篇合计**；若后续把 WAM 研究范围扩到 GenAD/OpenDV 路线，必须单独加入审计。此处列出是为了明确它不是被忽略，而是按当前研究范围排除。

## 结论

按“22 篇直接相关的已发布整包”计，有 3 个确认 >1 TB 的公开包；按已知替代版本再算，Bench2Drive Full 和 depth 两种额外 package form 也超过 1 TB。对真实论文子集和原始媒体联合量，仍有至少 W0、LAW、WAM-Flow、ReCogDrive 系、UniDrive-WM、corruption、HUGSIM parent 七类 UNKNOWN 风险。nuPlan 的全时段 raw sensor 也远大于已公开对象清单可能对应的 20.28 TB release；公开证据允许估到百 TB 量级，不能给“准确全量上限”。

所以目前能严谨确认的是：**三份已量化直接大包 + 两种未证实被论文采用的 Bench2Drive TB 级版本 + 多个无法封顶的实际数据源。**这比“只有三个 TB 数据集”准确；也意味着现在不能用约 27.44 TB（20.28+2.506+4.65 的算术和）作为全部论文需求或最大盘容量：它同时忽略 nuPlan 未发布时段、私有 W0、多源图像，并把 OpenScene 与 nuPlan 的重叠、FineVision 整库与子集差异混在一起。

### 核心一手来源

- [nuPlan Motional：120h raw sensor = full dataset 10%，约 16TB](https://motional.com/news/motionals-nuplan-dataset-will-advance-av-planning-research)
- [nuPlan 官方 devkit：完整 v1.0 >1,300h，sensor v1.1 分阶段发布](https://github.com/motional/nuplan-devkit)
- [Motional 早期 nuPlan 总记录 1,500h](https://motional.com/news/motionals-nuplan-dataset-set-usher-next-generation-autonomous-vehicles)
- [OpenScene 官方 v1.1 数据说明](https://github.com/OpenDriveLab/OpenScene/blob/main/docs/getting_started.md#download-data)
- [FineVision 作者数据集页](https://huggingface.co/datasets/HuggingFaceM4/FineVision)
- [Bench2Drive 官方 README](https://github.com/Thinklab-SJTU/Bench2Drive/blob/0.0.4/README.md)
- [LAW 原文](https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md/P0048_LAW/P0048_LAW.raw.md#L165)；[ThinkTwice 采集信息（仅比较参照）](https://github.com/OpenDriveLab/ThinkTwice/blob/main/docs/DATA_PREP.md)
- [DriveVLA-W0 原文](https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md/P0072_DriveVLA-W0/P0072_DriveVLA-W0.raw.md#L133)
- [WAM-Flow 原文](https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md/P0074_WAM-Flow/P0074_WAM-Flow.raw.md#L157)；[ReCogDrive 官方数据源表](https://github.com/xiaomi-research/recogdrive#driving-pretraining-datasets)
- [ExploreVLA 原文](https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md/P0075_ExploreVLA/P0075_ExploreVLA.raw.md#L145)；[HUGSIM 包](https://huggingface.co/datasets/XDimLab/HUGSIM)
- [OpenDV 官方 DriveAGI 页面（范围外边界校验）](https://github.com/OpenDriveLab/DriveAGI)
