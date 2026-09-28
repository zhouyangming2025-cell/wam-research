# WAM 12 + WAM+VLA 10：数据资产逐项账本（2026-09-28）

口径：只计 22 篇**自身**的训练、预训练、微调、验证需求；单纯出现在相关工作的数据不计。论文原文固定为仓库 `cb05048dfb822e95d44e52dd85b830c750411e2c` 的 [papers/raw_md](https://github.com/zhouyangming2025-cell/wam-research/tree/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md)。`官网标称` 是发布方显示的取整量，`字节` 只在官方 `Size`/`Content-Length` 或已审计 archive inventory 明确返回整数时才写精确；其余保留发布方近似值或 UNKNOWN。2026-09-28 已从 Motional S3 listing 取得 nuPlan 169 个对象的精确 byte，其他逐篇资产不因此自动变成精确。**不把取整标称数伪装成精确字节。**本轮不检查或扣减 NAS 当前占用。单独的 [nuPlan 169 文件清单](nuplan_v1_1_official_file_manifest_2026-09-28.md) 给出每个对象名、显示容量、精确 byte 和官方直链。

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
| OpenScene v1.1 常规 mini/trainval/test camera/LiDAR、metadata 与三份 JSON 清单 | **2,506,457,646,127 B**；另有 private test **39,224,624,432 B**；全仓 540 个 OpenScene 文件 **2,545,682,270,559 B** | **2026-09-28 官方 HF 固定 revision 文件 `size`；常规 534 项、private 6 项，见逐文件 manifest。历史 inventory 2,545,682,394,232 B 计入 private 和 sidecar，较官方文件总和多 123,673 B。原 0.265 TB“冲突”是比较范围及页面单位/取整混合所致** | NAVSIM 数据母体；navtrain 是 trainval scene filter。高概率/全部情景均仅选常规 534 项；private test 缺 22 篇使用证据，不加入。独立 navtrain archive 须另计包留存 | [官方 HF 固定 revision](https://huggingface.co/datasets/OpenDriveLab/OpenScene/tree/a76f840b65e972bc45e56c2adced897498e9a026/openscene-v1.1)；[逐文件清单](openscene_v1_1_official_file_manifest_2026-09-28.md)；[历史 inventory](../../datasets/resource_inventory_20260921.md) |
| OpenScene 额外 private test wm/e2e/hard | 15GB、23.6GB、636MB 传感器，另少量 metadata | **官方可见；22 篇直接使用证据不足，排除** | 这些是独立 benchmark private 项，不凭名称并入 NAVSIM navtest | [同上](https://github.com/OpenDriveLab/OpenScene/blob/main/docs/getting_started.md#download-data) |
| NAVSIM v1 navtrain 精简传感器 | 445GB | **官方取整；高频选择整份 OpenScene 时额外为 0** | OpenScene trainval 的 scene filter 再分发，不属于新采集 | [NAVSIM splits](https://github.com/autonomousvision/navsim/blob/main/docs/splits.md#overview) |
| NAVSIM v2 navhard two-stage、warmup、private hard | 官方分项 31GB、1.2GB、11GB（含现有路径历史约50.2GB另一口径） | **分项官方近似；完整文件精确字节 UNKNOWN** | Stage1 真实传感器继承 OpenScene test；Stage2 另有 synthetic | [NAVSIM splits](https://github.com/autonomousvision/navsim/blob/main/docs/splits.md#overview) |
| nuScenes Core Full + camera supplement + Map Expansion v1.3 + CAN bus | Core Full **372,554,105,065 B**；加项目已登记 camera supplement、map、CAN payload 后合计 **391,324,380,635 B =0.391324380635 TB** | **2026-09-21 项目逐资产 inventory 的 archive bytes；不同于官网网页容量报价；camera supplement 是否每篇都需用，按具体复现配置确认** | DriveLM、OmniDrive、Turning、部分 ReCogDrive 子源依赖 nuScenes 图像/标注；QA 包中的图片可能与 Core 重复，未 hash 去重 | [nuScenes 数据页](https://www.nuscenes.org/download)；[项目逐资产字节清单](../../datasets/resource_inventory_20260921.md) |
| 旧 Bench2Drive Base（用于多篇旧论文） | 官方400GB | **发布方约数** | 与 0.0.4 无 depth 不同版本，分开计 | [Bench2Drive 官方](https://github.com/Thinklab-SJTU/Bench2Drive#dataset) |
| Bench2Drive v0.0.4 无 depth | 官方400GB；用户此前记录415GB | **官方/用户口径不一致，主情景用415GB** | 新版基建情景，旧论文不能据此直接替换 Base | [同上](https://github.com/Thinklab-SJTU/Bench2Drive#dataset) |
| 旧 Bench2Drive Full／新版 depth | 4TB／7.3TB | **可定价，但 22 篇没有使用整包的明确证据，排除** | 若方案改为 Full/depth，分别较 Base 增约3.6TB／7.3TB | [同上](https://github.com/Thinklab-SJTU/Bench2Drive#dataset) |
| LAW 独立 CARLA 189K 帧 | **LAW 原版 UNKNOWN**；ThinkTwice 同规模采集约8TB | **论文明确 CARLA 0.9.10.1、Roach 教师、189K 帧；CARLA 网络输入 resize 900×256 是训练变换，不是采集原图分辨率。作者公开仓库只有 nuScenes 数据准备/训练入口，未给对应 CARLA 发布对象、模态/采集帧率/格式/原分辨率/字节** | 与 B2D archive 不同；未公开原包则无法公开定价。8TB 仅敏感性参照，Roach 其他采集包也不能代换 | [LAW 原文 §5.1–5.2](https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md/P0048_LAW/P0048_LAW.raw.md#L165)；[ThinkTwice 采集](https://github.com/OpenDriveLab/ThinkTwice/blob/main/docs/DATA_PREP.md)；[LAW 官方仓库](https://github.com/BraveGroup/LAW) |
| CoVLA-Dataset；DrivingDojo | 452GB；283GB | **作者 HF 整库近似** | Drive-JEPA 视频预训练，独立于 OpenScene | [CoVLA](https://huggingface.co/datasets/turing-motors/CoVLA-Dataset)；[DrivingDojo](https://huggingface.co/datasets/Yuqi1997/DrivingDojo) |
| CityWalker 公开 teleportation 包 | 6.82GB | **作者 HF 整库** | Metis 的 15h teleoperation 与发布包对应关系未证实 | [作者说明](https://github.com/ai4ce/CityWalker/blob/main/dataset/README.md#teleportation-dataset)；[HF](https://huggingface.co/datasets/ai4ce/CityWalker) |
| FineVision 整库 | 4.65TB | **HF 整库，论文实际选取分卷 UNKNOWN** | 3:7 是抽样比例，不能推回使用了4.65TB | [HF](https://huggingface.co/datasets/HuggingFaceM4/FineVision) |
| HUGSIM 预建四域 scenes；Adv-nuSc | 60.7GB；15.6GB | **作者 HF 整库** | 四域场景不自动追加 Waymo/KITTI-360/PandaSet 原始全集；Adv-nuSc 依赖 nuScenes | [HUGSIM](https://huggingface.co/datasets/XDimLab/HUGSIM)；[Adv](https://huggingface.co/datasets/Pixtella/Adv-nuSc) |
| nuScenes-C 图像（GraphWorld 雨/雪/雾）；Turning-nuScenes | **前者 UNKNOWN；后者仅 nuScenes val 场景筛选** | **论文明确三种 Rain/Snow/Fog，nuScenes-C 全 benchmark 为 27 类×5 强度；未指定本实验选用强度的可下载文件清单/bytes** | Turning 为 17 scenes/680 val samples，不是独立影像包；不能把 nuScenes-C 全量或任一小子集报价成 GraphWorld 所用三天气 | [GraphWorld 原文 §5.1](https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md/P0065_GraphWorld/P0065_GraphWorld.raw.md#L263)；[Robo3D 官方准备说明](https://github.com/worldbench/Robo3D/blob/main/docs/DATA_PREPARE.md) |
| ReCogDrive_Pretraining 重写 QA+轨迹标注 | **17 个 JSONL 文件 `size` 合计 3,789,771,567 B**（HF revision `f55bb18e0aca846bbedfb516760a1b9b7cfe3ebf`） | **官方 HF 文件元信息精确到各对象；不含源图像/视频**。作者页面列 12 个外部驾驶 QA 源，另有 NAVSIM/B2D 派生项；单仓 JSONL 文件数不是独立媒体数 | NAVSIM 两项、Bench2Drive 两项依赖各自母体；DriveLM、Nuscenes-QA、Omnidrive 等须按样本路径归属 nuScenes；LingoQA、Drama、SUTD 等可能需独立媒体。尚未完成 17 文件全量唯一路径抽取/逐图去重 | [作者源清单](https://github.com/xiaomi-research/recogdrive#driving-pretraining-datasets)；[固定 revision 文件清单](https://huggingface.co/datasets/owl10/ReCogDrive_Pretraining/tree/f55bb18e0aca846bbedfb516760a1b9b7cfe3ebf) |
| LingoQA 独立媒体（ReCogDrive 子源） | **作者公开云盘逐文件页面和约61.1135GB**：scenery `images.zip` 7.71GB+`train.parquet` 11.6MB；action `images.zip` 53.15GB+`train.parquet` 20.5MB；evaluation `images.zip` 221.3MB+`val.parquet` 72KB | **整包可定价，页面取整，精确字节 UNKNOWN；ReCog 实际引用范围 UNKNOWN** | ReCogDrive LingoQA JSONL 92.7MB 不含作者原图；LingoQA 完整媒体不能当作只用该 JSONL 的实际选择量 | [Wayve 作者下载页](https://github.com/wayveai/LingoQA#download-data-and-annotations)；[公开云盘](https://drive.google.com/drive/folders/1ivYF2AYHxDQkX5h7-vo7AUDNkKuQz_fL)；[ReCog 子目录](https://huggingface.co/datasets/owl10/ReCogDrive_Pretraining/tree/main/LingoQA) |
| DRAMA 独立视频（ReCogDrive 子源） | UNKNOWN | **独立视频字节 UNKNOWN** | ReCogDrive Drama JSONL 21.4MB 不含视频 | [ReCog 子目录](https://huggingface.co/datasets/owl10/ReCogDrive_Pretraining/tree/main/Drama)；[作者来源链](https://github.com/xiaomi-research/recogdrive#driving-pretraining-datasets) |
| SUTD TrafficQA（ReCogDrive 子源） | Zenodo record 7431011 九个对象 **20,534,486,181 B**；其中四个 `.h5` 为 motion/ResNet101/ResNet18/MobileNetV2 features，余下 JSONL/映射文件；**原始 10,080 视频未在该 record 文件列表中，视频字节 UNKNOWN** | **官方 Zenodo API `files[].size` 精确到发布对象**；约 20.5GB 不是原视频 | ReCogDrive 的 SUTD JSONL 为 30,424,175 B；逐视频引用路径及 VLM 图像输入是否可由原始视频公开取得尚未核实；feature 不能替代像素输入 | [Zenodo record/API](https://zenodo.org/api/records/7431011)；[ReCog 子文件](https://huggingface.co/datasets/owl10/ReCogDrive_Pretraining/tree/main/SUTD) |
| ReCogDrive 余下 DriveLM、NuInstruct、nuScenesQA、OmniDrive、Senna、MapLM、Talk2Car、DriveGPT4、CODA-LM 等原图 | UNKNOWN 增量 | **逐源路径待核** | 不可把全部笼统归到 nuScenes；已确认属于 nuScenes 的条目不重复计母体 | [ReCog 12 源表](https://github.com/xiaomi-research/recogdrive#driving-pretraining-datasets) |
| WAM-Flow 通用 VQA 3.4M 原图 | UNKNOWN | **论文称 LLaVA-v1.5 来源；未给具体版本/split/3.4M 样本路径清单。作者模型仓 `data/navsim_668k.jsonl` 官方 `size` 414,319,989 B，文件名指 NAVSIM 标注，不能代替 3.4M 通用图像** | 通用视觉上游与 FineVision/其他 VQA 是否有重叠未经路径或 hash 核实 | [原文](https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md/P0074_WAM-Flow/P0074_WAM-Flow.raw.md#L157)；[作者文件目录](https://huggingface.co/fudan-generative-ai/WAM-Flow/tree/main/data) |
| DriveLM 整包、OmniDrive nuScenes 附加、UniDriveVLA 作者 JSON | 4.86GB；885MB；465MB | **HF/发布方标称；可能有部分 nuScenes 重复图像** | 需文件级去重；增加包容量≠增加独立媒体同量 | [DriveLM](https://huggingface.co/datasets/OpenDriveLab/DriveLM)；[OmniDrive](https://github.com/NVlabs/OmniDrive/releases)；[UniDrive](https://huggingface.co/datasets/owl10/UniDriveVLA_Data) |
| SGDrive 作者 `sgdrive.jsonl` | 932MB | **作者文件，图片依赖 UNKNOWN** | 同一模型仓库 11.5GB 含模型权重，不能全加 | [作者文件清单](https://huggingface.co/SII-Whaleice/SGDrive/tree/main) |
| ORION 原版 Chat-B2D `chat-B2D.zip` | **325MB** | **作者 HF 单文件标称，原图依赖 Bench2Drive** | 同库 `ChatB2D-plus.zip` 332MB 为后续扩展版，不能代入 UniDrive-WM | [ORION 原版链接](https://github.com/xiaomi-mlab/Orion#preperation)；[作者发布库](https://huggingface.co/datasets/poleyzdk/Chat-B2D/tree/main) |
| DriveBench 完整 corruption + QA | UNKNOWN；HF `arena` 31.8MB/1461 行仅子集 | **不能以小子集报价完整评测** | Benchmark 19,200 帧/20,498 QA，腐蚀图像另需核 | [作者数据准备](https://github.com/worldbench/DriveBench/blob/main/docs/DATA_PREPAER.md)；[HF 子集](https://huggingface.co/datasets/drive-bench/arena) |
| UniDriveVLA 其余七种通用 VQA **评测集** | UNKNOWN（论文未逐包给 manifest） | **未闭合，仅评测；不自动并为训练 FineVision** | MMStar、MMMU、RealWorldQA、AI2D、MME、VLMsAreBlind、ChartQA | [原文表8](https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md/P0076_UniDriveVLA/P0076_UniDriveVLA.raw.md#L192) |
| DriveVLA-W0 私有 70M 帧／>1M clips | UNKNOWN 且不可公开获取 | **从公开采购总量剥离** | 论文完全相同训练数据无法按公开包复现 | [原文](https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md/P0072_DriveVLA-W0/P0072_DriveVLA-W0.raw.md#L133) |

## ReCogDrive 发布标注逐源对象（官方文件 API，2026-09-28）

固定 revision [`f55bb18e0aca846bbedfb516760a1b9b7cfe3ebf`](https://huggingface.co/datasets/owl10/ReCogDrive_Pretraining/tree/f55bb18e0aca846bbedfb516760a1b9b7cfe3ebf) 下仅列 `.jsonl` 的 `size`；17 文件 **3,789,771,567 B**。这是 annotation 对象的精确包留存，**不是源像素或视频容量**。下表“候选母体”取自作者 [来源表](https://github.com/xiaomi-research/recogdrive#driving-pretraining-datasets) 的项目名和明确派生项；尚未读取整份 JSONL 提取所有唯一路径，所以没有将 nuScenes 可能关联的条目无条件去重。

| 作者 JSONL 对象 | 官方 bytes | 候选源媒体/父体（逐样本路径待证） |
|---|---:|---|
| [Bench2drive_QA/Bench2drive_QA.jsonl](https://huggingface.co/datasets/owl10/ReCogDrive_Pretraining/blob/f55bb18e0aca846bbedfb516760a1b9b7cfe3ebf/Bench2drive_QA/Bench2drive_QA.jsonl) | 1,007,343,319 | Bench2Drive；具体版本/路径 UNKNOWN |
| [Bench2drive_Traj/Bench2drive_Traj.jsonl](https://huggingface.co/datasets/owl10/ReCogDrive_Pretraining/blob/f55bb18e0aca846bbedfb516760a1b9b7cfe3ebf/Bench2drive_Traj/Bench2drive_Traj.jsonl) | 409,885,730 | Bench2Drive；具体版本/路径 UNKNOWN |
| [CODA-LM/dataset_coda_lm.jsonl](https://huggingface.co/datasets/owl10/ReCogDrive_Pretraining/blob/f55bb18e0aca846bbedfb516760a1b9b7cfe3ebf/CODA-LM/dataset_coda_lm.jsonl) | 24,557,896 | 作者所列 coda-lm 来源；与 nuScenes 等父体的逐样本关系 UNKNOWN |
| [Drama/dataset_drama.jsonl](https://huggingface.co/datasets/owl10/ReCogDrive_Pretraining/blob/f55bb18e0aca846bbedfb516760a1b9b7cfe3ebf/Drama/dataset_drama.jsonl) | 21,437,538 | 独立媒体候选 drama；原始图像/视频路径 UNKNOWN |
| [DriveLM/drivelm_change_box_type.jsonl](https://huggingface.co/datasets/owl10/ReCogDrive_Pretraining/blob/f55bb18e0aca846bbedfb516760a1b9b7cfe3ebf/DriveLM/drivelm_change_box_type.jsonl) | 84,501,306 | 作者所列 drivelm 来源；与 nuScenes 等父体的逐样本关系 UNKNOWN |
| [DriveLM/drivelm_original_box.jsonl](https://huggingface.co/datasets/owl10/ReCogDrive_Pretraining/blob/f55bb18e0aca846bbedfb516760a1b9b7cfe3ebf/DriveLM/drivelm_original_box.jsonl) | 77,619,323 | 作者所列 drivelm 来源；与 nuScenes 等父体的逐样本关系 UNKNOWN |
| [Drivegpt4/dataset_drivegpt4.jsonl](https://huggingface.co/datasets/owl10/ReCogDrive_Pretraining/blob/f55bb18e0aca846bbedfb516760a1b9b7cfe3ebf/Drivegpt4/dataset_drivegpt4.jsonl) | 48,949,414 | 作者所列 drivegpt4 来源；与 nuScenes 等父体的逐样本关系 UNKNOWN |
| [LingoQA/dataset_lingoqa.jsonl](https://huggingface.co/datasets/owl10/ReCogDrive_Pretraining/blob/f55bb18e0aca846bbedfb516760a1b9b7cfe3ebf/LingoQA/dataset_lingoqa.jsonl) | 92,711,709 | 独立媒体候选 lingoqa；原始图像/视频路径 UNKNOWN |
| [Maplm/dataset_maplm.jsonl](https://huggingface.co/datasets/owl10/ReCogDrive_Pretraining/blob/f55bb18e0aca846bbedfb516760a1b9b7cfe3ebf/Maplm/dataset_maplm.jsonl) | 25,223,737 | 作者所列 maplm 来源；与 nuScenes 等父体的逐样本关系 UNKNOWN |
| [Navsim_ReCogDrive/dataset_navsim_recogdrive.jsonl](https://huggingface.co/datasets/owl10/ReCogDrive_Pretraining/blob/f55bb18e0aca846bbedfb516760a1b9b7cfe3ebf/Navsim_ReCogDrive/dataset_navsim_recogdrive.jsonl) | 737,567,360 | NAVSIM/OpenScene 派生；具体 token 路径 UNKNOWN |
| [Navsim_Traj/dataset_navsim_traj.jsonl](https://huggingface.co/datasets/owl10/ReCogDrive_Pretraining/blob/f55bb18e0aca846bbedfb516760a1b9b7cfe3ebf/Navsim_Traj/dataset_navsim_traj.jsonl) | 191,907,292 | NAVSIM/OpenScene 派生；具体 token 路径 UNKNOWN |
| [Nuinstruct/dataset_nuinstruct.jsonl](https://huggingface.co/datasets/owl10/ReCogDrive_Pretraining/blob/f55bb18e0aca846bbedfb516760a1b9b7cfe3ebf/Nuinstruct/dataset_nuinstruct.jsonl) | 246,273,130 | 作者所列 nuinstruct 来源；与 nuScenes 等父体的逐样本关系 UNKNOWN |
| [Nuscenes-QA/dataset_nuscenes_qa.jsonl](https://huggingface.co/datasets/owl10/ReCogDrive_Pretraining/blob/f55bb18e0aca846bbedfb516760a1b9b7cfe3ebf/Nuscenes-QA/dataset_nuscenes_qa.jsonl) | 189,749,118 | 作者所列 nuscenes-qa 来源；与 nuScenes 等父体的逐样本关系 UNKNOWN |
| [Omnidrive/dataset_omnidrive.jsonl](https://huggingface.co/datasets/owl10/ReCogDrive_Pretraining/blob/f55bb18e0aca846bbedfb516760a1b9b7cfe3ebf/Omnidrive/dataset_omnidrive.jsonl) | 195,598,167 | 作者所列 omnidrive 来源；与 nuScenes 等父体的逐样本关系 UNKNOWN |
| [SUTD/dataset_sutd.jsonl](https://huggingface.co/datasets/owl10/ReCogDrive_Pretraining/blob/f55bb18e0aca846bbedfb516760a1b9b7cfe3ebf/SUTD/dataset_sutd.jsonl) | 30,424,175 | 独立媒体候选 sutd；原始图像/视频路径 UNKNOWN |
| [Senna/dataset_senna.jsonl](https://huggingface.co/datasets/owl10/ReCogDrive_Pretraining/blob/f55bb18e0aca846bbedfb516760a1b9b7cfe3ebf/Senna/dataset_senna.jsonl) | 402,490,225 | 作者所列 senna 来源；与 nuScenes 等父体的逐样本关系 UNKNOWN |
| [Talk2Car/dataset_talk2car.jsonl](https://huggingface.co/datasets/owl10/ReCogDrive_Pretraining/blob/f55bb18e0aca846bbedfb516760a1b9b7cfe3ebf/Talk2Car/dataset_talk2car.jsonl) | 3,532,128 | 作者所列 talk2car 来源；与 nuScenes 等父体的逐样本关系 UNKNOWN |

【分析判断】SGDrive 的 932 MB JSONL 也不能代替这些文件或它们引用的图片；论文的“3.1M QA”与 ReCogDrive 全仓文件数量、具体采样集合之间尚无可证明的一一对应。下载/读取全量 annotation 后应以去重后的 media URI+原始 dataset ID 核验，不能只按文件名宣称 nuScenes 同源。

## 本轮容量核算（2026-09-28 修订；组合口径，不是全部需求闭合）

nuPlan 项 `N` 已从“页面显示 GB 单位不明”升级为官方对象级 byte 总和：**20,280,630,002,024 B =20.280630002024 TB =18.445125535 TiB**，含 169 个 v1.1 发布对象及 mini；排除 mini 后 **19,187,050,050,161 B =19.187050050161 TB**。逐对象证据见 [nuPlan v1.1 文件清单](nuplan_v1_1_official_file_manifest_2026-09-28.md)。

高概率组合按完整 OpenScene 父体覆盖 NAVSIM v1 过滤场景计算。现改用官方固定 revision 的常规 OpenScene **534 个文件、2,506,457,646,127 B**，不含 private test 6 包；NAVSIM v2 暂沿用历史 inventory 50,241,887,601 B（官方五包为 50,241,882,946 B）；nuScenes 391,324,380,635 B；Bench2Drive v0.0.4 no-depth+map 418,508,847,603 B。旧 Bench2Drive Base 仍为发布方约 400 GB，其他小包也有网页取整数，整体不是 byte-exact。

| 集合 | 不含 nuPlan 的已列包 | 加 nuPlan 后条件和 | 限制 |
|---|---:|---:|---|
| 高概率：父系 + ReCogDrive、DriveLM、OmniDrive、SGDrive、UniDriveVLA 标注 | **约 3.777 TB** | **约 24.058 TB** | 源媒体及按论文读取量未闭合 |
| 全 22 篇更广已定价包：上行 + CoVLA、DrivingDojo、FineVision 整库、HUGSIM、Adv-nuSc、CityWalker、Chat-B2D、LingoQA 整库 | **约 9.307 TB** | **约 29.588 TB** | FineVision 整库不是论文实际取用量；多个独立媒体仍 UNKNOWN |
| 上行 + ThinkTwice 同规模 CARLA 参照 | **约 17.307 TB** | **约 37.588 TB** | 额外约 8 TB 非 LAW 实测或上限 |

十进制 TB。修正算式为旧条件和 `24.097319512095 − (2.545682394232 − 2.506457646127) = 24.058094763990 TB`；更广组合 `29.626878012095 − 0.039224748105 = 29.587653263990 TB`。这些小数只是对旧**混合精度输入**的算术，呈报仅保留约三位小数。ReCogDrive 17 个 JSONL 官方 size 总数比旧取整 3.79 GB 小 228,433 B，未将这一微小修订冒充全组合字节精确。

敏感项：① 若为代码复现保留独立 NAVSIM v1 navtrain archive，而不从 OpenScene 父体筛选生成，则在 high/all 组合上另加项目 inventory 的 **449,007,425,603 B（0.449007425603 TB）**；传感器内容逻辑重叠，但没有做跨 archive hash 去重。② SUTD TrafficQA 预计算 feature+annotation 九个 Zenodo 对象为 20,534,486,181 B；因不是原始视频且 ReCogDrive 实际读入映射未知，未加主合计。③ DriveBench `arena` 31.8 MB 只是评测子集，不可代替完整腐蚀图像。

`FineVision 4.65 TB` 是整库包量；UniDriveVLA 实际抽取/缓存的子集仍 UNKNOWN。LAW 189K CARLA frames、WAM-Flow 通用 VQA 图片、ReCogDrive 多源原视频、nuScenes-C、DriveBench 完整腐蚀数据和私有 DriveVLA-W0 均未计入可定价主和。故目前可以报告**已列资产的条件总和**，不能报告“完整数据盘准确需求”或一个有证明的上限；压缩 archive、展开后的 payload、训练缓存和 archive+unpack 同时存在的峰值是四种不同数字。

## 留存、展开与峰值的独立账本口径

| 资产集合 | 压缩发布对象同时留存 | 展开后留存 | 下载/预处理峰值 |
|---|---|---|---|
| nuPlan v1.1 官方 169 包 | **20,280,630,002,024 B**（含 mini；不含 mini 19,187,050,050,161 B） | UNKNOWN（未取得逐包 member uncompressed bytes） | UNKNOWN（与流式/同盘解包及中间缓存策略有关） |
| OpenScene v1.1 常规 534 文件 | **2,506,457,646,127 B**（其中三份 JSON 清单为直接文件） | UNKNOWN | UNKNOWN |
| OpenScene 全 540 文件（仅作为发布仓库全量情景） | **2,545,682,270,559 B**；private 6 包未在 22 篇常规情景计入 | UNKNOWN | UNKNOWN |
| NAVSIM v1 独立包额外留存 | **449,007,410,406 B**（HF 对象）；若以历史目录含 sidecar 计为 449,007,425,603 B | UNKNOWN | UNKNOWN |
| SUTD TrafficQA Zenodo 9 对象 | **20,534,486,181 B**（特征/annotation，不含原视频） | 该 record 是 `.h5`/JSONL 直接对象；原始视频 UNKNOWN | UNKNOWN |

“压缩发布对象同时留存”是指定包集合的算术，不能直接除以压缩比得到展开量；峰值还取决于下载暂存、archive 与展开目录是否并存、训练缓存是否保留。若要作设备盘容量决策，需先选择可复现目标论文、媒体模式与保留策略；对缺少原始发布对象的 LAW、私有 W0 则无可核上限。

## 截止本轮的未闭合项与终止标准

1. **nuPlan 已闭合。** 169 个官方对象的精确 `Size` 已抓取；历史“GB/GiB 单位猜测”作废。要估算展开体积或只下载 paper-specific shards，仍需按实际 member/scene 集合另算。
2. **OpenScene 官方压缩对象容量已闭合，展开未闭合。**常规 534 项 2,506,457,646,127 B，private 6 项 39,224,624,432 B；全部 540 项 2,545,682,270,559 B。历史目录 inventory 多 123,673 B，包含 sidecar。旧的 0.265 TB“冲突”来自官网取整/单位口径与含 private 的 inventory 相比；不能再作为同范围未解释差额。
3. **LAW CARLA 189K frames**：作者未公开和该论文对应的 modality/resolution/codec/file manifest/bytes；ThinkTwice 约 8 TB 只能作同规模参照。
4. **VLA 源媒体**：ReCogDrive/SGDrive 发布 JSONL 需要逐唯一路径映射到 nuScenes/OpenScene/NAVSIM/B2D 或独立源视频；LingoQA 整包已列但 ReCog 实际子集 UNKNOWN；DRAMA、SUTD 原视频文件体积未知。WAM-Flow 3.4M 通用 VQA 的确切 LLaVA-v1.5 来源 split、图像资产与去重 manifest 未公开。
5. **专用验证资产**：GraphWorld 三天气 nuScenes-C 原始 corruption 图像、DriveBench 完整 corruption 图像、UniDriveVLA 七种通用 VQA benchmark 的实际 split/文件大小仍未知。不能用 QA 行数或一个小评测子集估成全包大小。
6. **私有/训练量边界**：DriveVLA-W0 的私有 70M frames / >1M clips 不公开；公开 nuPlan/NAVSIM 小样本不能替代。CityWalker 发布整库与 Metis 15h 子集映射、FineVision 实际分卷也需要作者配置确认。
7. 输出完整、可复核的最终盘需求前，每一项需有 `dataset_id, paper_id, role, version, split, modality, shard, exact_bytes, source, duplicate_of, compressed/unpacked status, public/private`；所有 required 行不能有 UNKNOWN。之后分别计算高概率组合与全部组合，并把 archive 持有、解压后和下载/预处理峰值分开。

## 截止本轮的硬性阻塞及可判定终止标准

1. nuPlan 169 文件和 OpenScene 540 文件官方 `Size` 已取得；FineVision 仍需确认论文实际使用分卷，整库报价不能替代子集。
2. LAW 作者尚未公布其 189K 帧的模态、分辨率、压缩方式、文件目录及字节；不能从其他论文 8TB 类比得出实际总量。
3. ReCogDrive/SGDrive 需从发布 JSONL 抽取唯一路径并归属独立视频/nuScenes/NAVSIM/B2D；LingoQA 整包已获取整规模，但 DRAMA、SUTD 等仍需与实际路径匹配的发布文件字节。WAM-Flow 3.4M 与 UniDrive-WM 混合 VQA 需作者 manifest。
4. GraphWorld 三天气 nuScenes-C、DriveBench 全量 corruption、七通用 VQA 评测实际 split 需要选定具体发布文件和字节。
5. 只有以上全部公开数据 `asset_id, version, shard, bytes, role, evidence, duplicate_of` 均非 UNKNOWN，才可输出**公开可复现**的“高概率”和“全部”两个精确数；私有 70M 单独报不可复现。另将 archive 留存、解压后留存、运行峰值分别核算，不得互代。
