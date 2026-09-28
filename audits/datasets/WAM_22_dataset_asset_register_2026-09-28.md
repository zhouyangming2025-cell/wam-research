# WAM 12 + WAM+VLA 10：数据资产逐项账本（2026-09-28）

口径：只计 22 篇**自身**的训练、预训练、微调、验证需求；单纯出现在相关工作的数据不计。论文原文固定为仓库 `cb05048dfb822e95d44e52dd85b830c750411e2c` 的 [papers/raw_md](https://github.com/zhouyangming2025-cell/wam-research/tree/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md)。`官网标称` 是发布方显示的取整量，`字节` 才是可审计的准确量。因可访问的站点未提供公开 `Content-Length` 列表，**不得把前者改写为精确字节**。不查看、不扣减用户存储。单独的 [nuPlan 169 文件清单](nuplan_v1_1_official_file_manifest_2026-09-28.md) 给出每个文件名、页面容量和官方直链。

## 22 篇论文的资产入口（原文事实；`?` 表示论文未给精确训练列表）

| 原文 ID | 训练/预训练资产 | 评测资产 | 易误算之处 |
|---|---|---|---|
| [P0001 Epona](https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md/P0001_Epona/P0001_Epona.raw.md#L183) | nuPlan、nuScenes | nuPlan test、nuScenes val、NAVSIM | nuPlan test 仅论文特定视频子集。 |
| [P0009 DriveLaW](https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md/P0009_DriveLaW/P0009_DriveLaW.raw.md#L151) | nuPlan、nuScenes、NAVSIM 规划适配 | nuScenes、NAVSIM | 预训练与规划数据应分阶段记录。 |
| [P0042 WorldDrive](https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md/P0042_WorldDrive/P0042_WorldDrive.raw.md#L142) | nuPlan+nuScenes 视频，NAVSIM 规划 | nuScenes、NAVSIM v1/v2 | NAVSIM 继承 OpenScene，不重复计算原始 nuPlan。 |
| [P0045 WoTE](https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md/P0045_WoTE/P0045_WoTE.raw.md) | NAVSIM、旧 Bench2Drive | NAVSIM、旧 Bench2Drive | CARLA 仿真运行时观测不是离线测试视频包。 |
| [P0046 World4Drive](https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md/P0046_World4Drive/P0046_World4Drive.raw.md) | nuScenes、NAVSIM | nuScenes、NAVSIM | — |
| [P0048 LAW](https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md/P0048_LAW/P0048_LAW.raw.md#L165) | nuScenes、NAVSIM、独立 CARLA/Roach 189K 帧 | nuScenes、NAVSIM、CARLA | 189K 帧不是 Bench2Drive Base；LAW 官方代码仅给 nuScenes 准备说明。 |
| [P0049 Drive-JEPA](https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md/P0049_DriveJEPA/P0049_DriveJEPA.raw.md) | CoVLA、DrivingDojo、OpenScene 视频；NAVSIM/B2D 规划 | NAVSIM v1/v2、旧 B2D | 三份视频来源不可合并为 NAVSIM。 |
| [P0061 SeerDrive](https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md/P0061_SeerDrive/P0061_SeerDrive.raw.md) | NAVSIM、nuScenes、B2D 实验 | NAVSIM、nuScenes、旧 B2D | — |
| [P0062 Metis](https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md/P0062_Metis/P0062_Metis.raw.md#L126-L130) | NAVSIM、CityWalker 15h（6h 微调） | NAVSIM、CityWalker 9h | CityWalker HF 公开包与这 15h 精确映射未证实。 |
| [P0063 DynFlowDrive](https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md/P0063_DynFlowDrive/P0063_DynFlowDrive.raw.md) | nuScenes、NAVSIM | nuScenes、NAVSIM | — |
| [P0064 Discrete-WAM](https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md/P0064_Discrete-WAM/P0064_Discrete-WAM.raw.md) | nuPlan、NAVSIM | NAVSIM | — |
| [P0065 GraphWorld](https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md/P0065_GraphWorld/P0065_GraphWorld.raw.md#L251-L263) | 旧 B2D v0.0.3 Base、NAVSIM、nuScenes | 以上 + Turning-nuScenes、Adv-nuSc、nuScenes-C 三种天气 | Turning 只需 nuScenes 子集；天气 corruption 像素可能另存。 |
| [P0068 DriveWorld-VLA](https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md/P0068_DriveWorld-VLA/P0068_DriveWorld-VLA.raw.md#L179-L193) | NAVSIM、nuScenes；ReCogDrive 式 VLM 预训练? | NAVSIM、nuScenes | 论文未提供完整 12 源图像 manifest。 |
| [P0069 Uni-World VLA](https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md/P0069_UniWorldVLA/P0069_UniWorldVLA.raw.md#L134) | NAVSIM，nuPlan 轨迹消融 | NAVSIM，nuPlan 消融 | nuPlan 轨迹消融不能推断读取 nuPlan 所有相机和 LiDAR。 |
| [P0070 SGDrive](https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md/P0070_SGDrive/P0070_SGDrive.raw.md#L117-L136) | NAVSIM；>3.1M 驾驶 QA +85K 轨迹 QA | NAVSIM | 作者 JSONL 已发布，原图映射待核。 |
| [P0071 FSDrive](https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md/P0071_FSDrive/P0071_FSDrive.raw.md#L107-L111) | OmniDrive-nuScenes QA、nuScenes 图像和标注、DriveLM GVQA | nuScenes、NAVSIM、DriveLM | OmniDrive 885MB 是附加包，原图仍来自 nuScenes。 |
| [P0072 DriveVLA-W0](https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md/P0072_DriveVLA-W0/P0072_DriveVLA-W0.raw.md#L124-L145) | nuPlan 8k steps + NAVSIM 4k steps；另有私有 70M 帧 | NAVSIM、私有 100 难例 | 私有资产无公开字节数，不准以公开 nuPlan 替代。 |
| [P0073 CoT4AD](https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md/P0073_CoT4AD/P0073_CoT4AD.raw.md#L117) | nuScenes、旧 B2D | nuScenes、旧 B2D | 提及语言数据集不证明整包直接训练。 |
| [P0074 WAM-Flow](https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md/P0074_WAM-Flow/P0074_WAM-Flow.raw.md#L157) | nuPlan 668K、LLaVA-v1.5 来源通用 VQA 3.4M、ReCogDrive 来源驾驶 QA 3.1M、NAVSIM 103K | NAVSIM、附录 nuScenes | 官方小型 SFT 文件不等于 6.5M 图片。 |
| [P0075 ExploreVLA](https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md/P0075_ExploreVLA/P0075_ExploreVLA.raw.md#L145) | NAVSIM、nuScenes | NAVSIM、nuScenes、HUGSIM 四域 | HUGSIM 四域不证明需要原始 Waymo/KITTI-360/PandaSet 全量。 |
| [P0076 UniDriveVLA](https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md/P0076_UniDriveVLA/P0076_UniDriveVLA.raw.md#L148) | 驾驶 VQA + FineVision 为主的通用数据（混采3:7）；nuScenes、旧 B2D | nuScenes、旧 B2D、DriveBench、七通用 VQA | FineVision 实际使用分卷 UNKNOWN。 |
| [P0077 UniDrive-WM](https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md/P0077_UniDrive-WM/P0077_UniDrive-WM.raw.md#L184-L194) | 旧 B2D Base、nuScenes、混合 VQA? | 旧 B2D、nuScenes、DriveLM、Chat-B2D | Chat-B2D 对应 ORION 原版 zip；不是 B2D-VL 的后续版本。 |

## 逐数据资产账本：容量、证据与重复关系

| 资产／版本 | 发布方可核容量 | 计量状态 | 母体/依赖；计盘决定 | 一手来源 |
|---|---:|---|---|---|
| nuPlan v1.1 原版 152 camera/LiDAR 分卷 +12 DB zip +v1.1 地图 +4 清单 | **20,280,630,002,024 B =20.280630002024 TB =18.445125535 TiB**；不含 mini debug 包为 **19,187,050,050,161 B =19.187050050161 TB** | **2026-09-28 官方 S3 `ListObjectsV2 Size` 精确核验169个对象；旧地图 v1.0 排除；页面显示取整量只作交叉检查** | 和 2Hz OpenScene 有场景/图像继承；压缩对象并非同一 archive，未按内容 hash 去重 | [Motional S3 Explorer](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/index.html#public/nuplan-v1.1/)；[官方 S3 对象列表](https://motional-nuplan.s3.ap-northeast-1.amazonaws.com/?list-type=2&prefix=public%2Fnuplan-v1.1%2F)；见逐文件清单 |
| OpenScene v1.1 trainval/test/mini camera/LiDAR 与 metadata | 官方表标称九项合计 **2.28056 TB（按显示数加总）**；项目 2026-09-21 archive inventory 为 **2,545,682,394,232 B =2.545682394232 TB** | **官方表数字经过取整；项目历史逐包 inventory 有 archive bytes，见 `datasets/resource_inventory_20260921.md`。两者不是可相加的两份数据** | NAVSIM 数据母体；navtrain sensor 是 trainval scene filter。高频情景按父体计一次，不另加 navtrain 下载包；如同时保留独立 navtrain archive，容量情景另加约449.007GB | [OpenScene 下载表](https://github.com/OpenDriveLab/OpenScene/blob/main/docs/getting_started.md#download-data)；[项目逐资产字节清单](../../datasets/resource_inventory_20260921.md) |
| OpenScene 额外 private test wm/e2e/hard | 15GB、23.6GB、636MB 传感器，另少量 metadata | **官方可见；22 篇直接使用证据不足，排除** | 这些是独立 benchmark private 项，不凭名称并入 NAVSIM navtest | [同上](https://github.com/OpenDriveLab/OpenScene/blob/main/docs/getting_started.md#download-data) |
| NAVSIM v1 navtrain 精简传感器 | 445GB | **官方取整；高频选择整份 OpenScene 时额外为 0** | OpenScene trainval 的 scene filter 再分发，不属于新采集 | [NAVSIM splits](https://github.com/autonomousvision/navsim/blob/main/docs/splits.md#overview) |
| NAVSIM v2 navhard two-stage、warmup、private hard | 官方分项 31GB、1.2GB、11GB（含现有路径历史约50.2GB另一口径） | **分项官方近似；完整文件精确字节 UNKNOWN** | Stage1 真实传感器继承 OpenScene test；Stage2 另有 synthetic | [NAVSIM splits](https://github.com/autonomousvision/navsim/blob/main/docs/splits.md#overview) |
| nuScenes Core Full + camera supplement + Map Expansion v1.3 + CAN bus | Core Full **372,554,105,065 B**；加项目已登记 camera supplement、map、CAN payload 后合计 **391,324,380,635 B =0.391324380635 TB** | **2026-09-21 项目逐资产 inventory 的 archive bytes；不同于官网网页容量报价；camera supplement 是否每篇都需用，按具体复现配置确认** | DriveLM、OmniDrive、Turning、部分 ReCogDrive 子源依赖 nuScenes 图像/标注；QA 包中的图片可能与 Core 重复，未 hash 去重 | [nuScenes 数据页](https://www.nuscenes.org/download)；[项目逐资产字节清单](../../datasets/resource_inventory_20260921.md) |
| 旧 Bench2Drive Base（用于多篇旧论文） | 官方400GB | **发布方约数** | 与 0.0.4 无 depth 不同版本，分开计 | [Bench2Drive 官方](https://github.com/Thinklab-SJTU/Bench2Drive#dataset) |
| Bench2Drive v0.0.4 无 depth | 官方400GB；用户此前记录415GB | **官方/用户口径不一致，主情景用415GB** | 新版基建情景，旧论文不能据此直接替换 Base | [同上](https://github.com/Thinklab-SJTU/Bench2Drive#dataset) |
| 旧 Bench2Drive Full／新版 depth | 4TB／7.3TB | **可定价，但 22 篇没有使用整包的明确证据，排除** | 若方案改为 Full/depth，分别较 Base 增约3.6TB／7.3TB | [同上](https://github.com/Thinklab-SJTU/Bench2Drive#dataset) |
| LAW 独立 CARLA 189K 帧 | **LAW 原版 UNKNOWN**；ThinkTwice 同规模采集约8TB | **同规模情景，不是 LAW 实测/上限** | LAW 官方仓库未发布对应 CARLA 文件级清单；不得用另一个 Roach 150GB 包替代 | [LAW 原文](https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md/P0048_LAW/P0048_LAW.raw.md#L165)；[ThinkTwice 采集](https://github.com/OpenDriveLab/ThinkTwice/blob/main/docs/DATA_PREP.md)；[LAW 仓库](https://github.com/BraveGroup/LAW) |
| CoVLA-Dataset；DrivingDojo | 452GB；283GB | **作者 HF 整库近似** | Drive-JEPA 视频预训练，独立于 OpenScene | [CoVLA](https://huggingface.co/datasets/turing-motors/CoVLA-Dataset)；[DrivingDojo](https://huggingface.co/datasets/Yuqi1997/DrivingDojo) |
| CityWalker 公开 teleportation 包 | 6.82GB | **作者 HF 整库** | Metis 的 15h teleoperation 与发布包对应关系未证实 | [作者说明](https://github.com/ai4ce/CityWalker/blob/main/dataset/README.md#teleportation-dataset)；[HF](https://huggingface.co/datasets/ai4ce/CityWalker) |
| FineVision 整库 | 4.65TB | **HF 整库，论文实际选取分卷 UNKNOWN** | 3:7 是抽样比例，不能推回使用了4.65TB | [HF](https://huggingface.co/datasets/HuggingFaceM4/FineVision) |
| HUGSIM 预建四域 scenes；Adv-nuSc | 60.7GB；15.6GB | **作者 HF 整库** | 四域场景不自动追加 Waymo/KITTI-360/PandaSet 原始全集；Adv-nuSc 依赖 nuScenes | [HUGSIM](https://huggingface.co/datasets/XDimLab/HUGSIM)；[Adv](https://huggingface.co/datasets/Pixtella/Adv-nuSc) |
| nuScenes-C 图像（GraphWorld 三天气）；Turning-nuScenes | **前者 UNKNOWN；后者仅母体筛选** | **论文评测包含，但大小未闭合** | 别将 benchmark 全量27×5或另一严重度配置误认三天气子集 | [GraphWorld 原文](https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md/P0065_GraphWorld/P0065_GraphWorld.raw.md#L263) |
| ReCogDrive_Pretraining 重写 QA+轨迹标注 | 3.79GB | **作者 HF 整库，仅标注** | 12 源所指独立媒体另核，不能称为驾驶 VQA 全量 | [作者 12 源清单](https://github.com/xiaomi-research/recogdrive#driving-pretraining-datasets)；[标注包](https://huggingface.co/datasets/owl10/ReCogDrive_Pretraining) |
| LingoQA 独立媒体（ReCogDrive 子源） | **作者公开云盘逐文件页面和约61.1135GB**：scenery `images.zip` 7.71GB+`train.parquet` 11.6MB；action `images.zip` 53.15GB+`train.parquet` 20.5MB；evaluation `images.zip` 221.3MB+`val.parquet` 72KB | **整包可定价，页面取整，精确字节 UNKNOWN；ReCog 实际引用范围 UNKNOWN** | ReCogDrive LingoQA JSONL 92.7MB 不含作者原图；LingoQA 完整媒体不能当作只用该 JSONL 的实际选择量 | [Wayve 作者下载页](https://github.com/wayveai/LingoQA#download-data-and-annotations)；[公开云盘](https://drive.google.com/drive/folders/1ivYF2AYHxDQkX5h7-vo7AUDNkKuQz_fL)；[ReCog 子目录](https://huggingface.co/datasets/owl10/ReCogDrive_Pretraining/tree/main/LingoQA) |
| DRAMA 独立视频（ReCogDrive 子源） | UNKNOWN | **独立视频字节 UNKNOWN** | ReCogDrive Drama JSONL 21.4MB 不含视频 | [ReCog 子目录](https://huggingface.co/datasets/owl10/ReCogDrive_Pretraining/tree/main/Drama)；[作者来源链](https://github.com/xiaomi-research/recogdrive#driving-pretraining-datasets) |
| SUTD TrafficQA（ReCogDrive 子源） | Zenodo 发布的 feature+annotation 包约 **20.5GB**；原始视频体积 UNKNOWN | **可计价的是预计算 MobileNet/ResNet/motion feature 与标注；不等于 ReCogDrive 训练所需的原视频，未计入媒体总量** | 逐视频路径映射未完成；是否能用官方 features 代替视频取决于复现输入接口 | [ReCog 作者来源链](https://github.com/xiaomi-research/recogdrive#driving-pretraining-datasets)；[SUTD TrafficQA Zenodo](https://zenodo.org/records/7431011) |
| ReCogDrive 余下 DriveLM、NuInstruct、nuScenesQA、OmniDrive、Senna、MapLM、Talk2Car、DriveGPT4、CODA-LM 等原图 | UNKNOWN 增量 | **逐源路径待核** | 不可把全部笼统归到 nuScenes；已确认属于 nuScenes 的条目不重复计母体 | [ReCog 12 源表](https://github.com/xiaomi-research/recogdrive#driving-pretraining-datasets) |
| WAM-Flow 通用 VQA 3.4M 原图 | UNKNOWN | **论文披露样本数，不披露训练 manifest** | 作者发布的约414MB SFT 文件不等于3.4M图像 | [原文](https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md/P0074_WAM-Flow/P0074_WAM-Flow.raw.md#L157)；[作者数据目录](https://huggingface.co/fudan-generative-ai/WAM-Flow/tree/main/data) |
| DriveLM 整包、OmniDrive nuScenes 附加、UniDriveVLA 作者 JSON | 4.86GB；885MB；465MB | **HF/发布方标称；可能有部分 nuScenes 重复图像** | 需文件级去重；增加包容量≠增加独立媒体同量 | [DriveLM](https://huggingface.co/datasets/OpenDriveLab/DriveLM)；[OmniDrive](https://github.com/NVlabs/OmniDrive/releases)；[UniDrive](https://huggingface.co/datasets/owl10/UniDriveVLA_Data) |
| SGDrive 作者 `sgdrive.jsonl` | 932MB | **作者文件，图片依赖 UNKNOWN** | 同一模型仓库 11.5GB 含模型权重，不能全加 | [作者文件清单](https://huggingface.co/SII-Whaleice/SGDrive/tree/main) |
| ORION 原版 Chat-B2D `chat-B2D.zip` | **325MB** | **作者 HF 单文件标称，原图依赖 Bench2Drive** | 同库 `ChatB2D-plus.zip` 332MB 为后续扩展版，不能代入 UniDrive-WM | [ORION 原版链接](https://github.com/xiaomi-mlab/Orion#preperation)；[作者发布库](https://huggingface.co/datasets/poleyzdk/Chat-B2D/tree/main) |
| DriveBench 完整 corruption + QA | UNKNOWN；HF `arena` 31.8MB/1461 行仅子集 | **不能以小子集报价完整评测** | Benchmark 19,200 帧/20,498 QA，腐蚀图像另需核 | [作者数据准备](https://github.com/worldbench/DriveBench/blob/main/docs/DATA_PREPAER.md)；[HF 子集](https://huggingface.co/datasets/drive-bench/arena) |
| UniDriveVLA 其余七种通用 VQA **评测集** | UNKNOWN（论文未逐包给 manifest） | **未闭合，仅评测；不自动并为训练 FineVision** | MMStar、MMMU、RealWorldQA、AI2D、MME、VLMsAreBlind、ChartQA | [原文表8](https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md/P0076_UniDriveVLA/P0076_UniDriveVLA.raw.md#L192) |
| DriveVLA-W0 私有 70M 帧／>1M clips | UNKNOWN 且不可公开获取 | **从公开采购总量剥离** | 论文完全相同训练数据无法按公开包复现 | [原文](https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md/P0072_DriveVLA-W0/P0072_DriveVLA-W0.raw.md#L133) |

## 本轮容量核算（2026-09-28 修订；组合口径，不是全部需求闭合）

nuPlan 项 `N` 已从“页面显示 GB 单位不明”升级为官方对象级 byte 总和：**20,280,630,002,024 B =20.280630002024 TB =18.445125535 TiB**，含 169 个 v1.1 发布对象及 mini；排除 mini 后 **19,187,050,050,161 B =19.187050050161 TB**。逐对象证据见 [nuPlan v1.1 文件清单](nuplan_v1_1_official_file_manifest_2026-09-28.md)。

高概率组合按“完整 OpenScene 父体覆盖 NAVSIM v1 的过滤场景，因此不再把独立 navtrain 传感器包重复算入”计算。优先用可找到的逐包 byte 账本：OpenScene 历史 archive inventory 2.545682394232 TB；NAVSIM v2 50,241,887,601 B；nuScenes 全部已登记 archive payload 391,324,380,635 B；Bench2Drive v0.0.4 no-depth+map 418,508,847,603 B；旧 Bench2Drive Base 仍只能按发布方约 400 GB。其余小包用发布页取整容量。因此合计虽显示多位小数，整体**不是 byte-exact**。OpenScene 官方页面标称九项合计约 2.28056 TB，与历史 archive inventory 2.545682394232 TB 不一致，须保留此冲突；下表高概率情景暂用逐包 byte inventory 值，不把两种口径相加。

| 集合 | 不含 nuPlan 的已知包合计 | 加 nuPlan 后的容量和 | 尚未计入/解释 |
|---|---:|---:|---|
| 高频父系 + ReCogDrive、DriveLM、OmniDrive、SGDrive、UniDriveVLA 标注包 | **3.816689510071 TB** | **24.097319512095 TB** | OpenScene 标称值与历史 archive byte 数有 0.265122394232 TB 冲突；完整 WAM/VLA 源媒体未闭合 |
| 上行 + CoVLA、DrivingDojo、FineVision 全库、HUGSIM、Adv-nuSc、CityWalker、ORION 原版 Chat-B2D、LingoQA 作者公开整库 | **9.346248010071 TB** | **29.626878012095 TB** | 这是“每个已知可定价包按此组合取用”的加总，不是 22 篇真实使用字节，也非完整集上限或下限 |
| 上行 + ThinkTwice 同规模 CARLA 189K 帧参考 | **17.346248010071 TB** | **37.626878012095 TB** | 额外约 8 TB 是 ThinkTwice 采集案例，不是 LAW 实测值、LAW 上限或实际可复现包 |

以上 `TB` 均为十进制。精确 nuPlan 加数相同；其他组件可能是精确 archive inventory、网页标称整数/小数或整库大小混合。数字小数位只是算术结果，**不得据此解释为总容量精确到 byte**。

敏感项：① 若为代码复现保留独立 NAVSIM v1 navtrain archive，而不从 OpenScene 父体筛选生成，则在 high/all 组合上另加项目 inventory 的 **449,007,425,603 B（0.449007425603 TB）**；传感器内容逻辑重叠，但没有做跨 archive hash 去重。② SUTD TrafficQA 预计算 feature+annotation 官方包约 20.5 GB；因不是原始视频且 ReCogDrive 实际读入映射未知，未加主合计。③ DriveBench `arena` 31.8 MB 只是评测子集，不可代替完整腐蚀图像。

`FineVision 4.65 TB` 是整库包量；UniDriveVLA 实际抽取/缓存的子集仍 UNKNOWN。LAW 189K CARLA frames、WAM-Flow 通用 VQA 图片、ReCogDrive 多源原视频、nuScenes-C、DriveBench 完整腐蚀数据和私有 DriveVLA-W0 均未计入可定价主和。故目前可以报告**已列资产的条件总和**，不能报告“完整数据盘准确需求”或一个有证明的上限；压缩 archive、展开后的 payload、训练缓存和 archive+unpack 同时存在的峰值是四种不同数字。

## 截止本轮的未闭合项与终止标准

1. **nuPlan 已闭合。** 169 个官方对象的精确 `Size` 已抓取；历史“GB/GiB 单位猜测”作废。要估算展开体积或只下载 paper-specific shards，仍需按实际 member/scene 集合另算。
2. **OpenScene 容量冲突待复核。** 官方 getting-started 表的九项加总为 2.28056 TB；项目 2026-09-21 archive inventory 为 2.545682394232 TB。需要官方逐分卷 `Content-Length`/仓库文件 `size` 或复核原 inventory 每个 payload 的归属后，才能选择统一值。
3. **LAW CARLA 189K frames**：作者未公开和该论文对应的 modality/resolution/codec/file manifest/bytes；ThinkTwice 约 8 TB 只能作同规模参照。
4. **VLA 源媒体**：ReCogDrive/SGDrive 发布 JSONL 需要逐唯一路径映射到 nuScenes/OpenScene/NAVSIM/B2D 或独立源视频；LingoQA 整包已列但 ReCog 实际子集 UNKNOWN；DRAMA、SUTD 原视频文件体积未知。WAM-Flow 3.4M 通用 VQA 的确切 LLaVA-v1.5 来源 split、图像资产与去重 manifest 未公开。
5. **专用验证资产**：GraphWorld 三天气 nuScenes-C 原始 corruption 图像、DriveBench 完整 corruption 图像、UniDriveVLA 七种通用 VQA benchmark 的实际 split/文件大小仍未知。不能用 QA 行数或一个小评测子集估成全包大小。
6. **私有/训练量边界**：DriveVLA-W0 的私有 70M frames / >1M clips 不公开；公开 nuPlan/NAVSIM 小样本不能替代。CityWalker 发布整库与 Metis 15h 子集映射、FineVision 实际分卷也需要作者配置确认。
7. 输出完整、可复核的最终盘需求前，每一项需有 `dataset_id, paper_id, role, version, split, modality, shard, exact_bytes, source, duplicate_of, compressed/unpacked status, public/private`；所有 required 行不能有 UNKNOWN。之后分别计算高概率组合与全部组合，并把 archive 持有、解压后和下载/预处理峰值分开。

## 截止本轮的硬性阻塞及可判定终止标准

1. nuPlan 169 文件需要 `Content-Length` 或等价对象 `Size` 精确整数，才能确定 GB 的单位和逐包取整；OpenScene/FineVision 等同理需所选文件 manifest。当前动态官网只显示格式化取整量。
2. LAW 作者尚未公布其 189K 帧的模态、分辨率、压缩方式、文件目录及字节；不能从其他论文 8TB 类比得出实际总量。
3. ReCogDrive/SGDrive 需从发布 JSONL 抽取唯一路径并归属独立视频/nuScenes/NAVSIM/B2D；LingoQA 整包已获取整规模，但 DRAMA、SUTD 等仍需与实际路径匹配的发布文件字节。WAM-Flow 3.4M 与 UniDrive-WM 混合 VQA 需作者 manifest。
4. GraphWorld 三天气 nuScenes-C、DriveBench 全量 corruption、七通用 VQA 评测实际 split 需要选定具体发布文件和字节。
5. 只有以上全部公开数据 `asset_id, version, shard, bytes, role, evidence, duplicate_of` 均非 UNKNOWN，才可输出**公开可复现**的“高概率”和“全部”两个精确数；私有 70M 单独报不可复现。另将 archive 留存、解压后留存、运行峰值分别核算，不得互代。
