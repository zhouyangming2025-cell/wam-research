# 22 篇数据资产：TCP、VLA 媒体与训练缓存补充证据

2026-09-28；接续 [逐论文资产账本](WAM_22_dataset_asset_register_2026-09-28.md) 与 [审计流程](WAM_WAMVLA_22_DATASET_AUDIT_PROCESS_20260928.md)。本文件只保存本轮独立证据、受限媒体路径核查口径及状态；不替代两个既有总表。TB 为十进制 `10^12 B`，`bytes=UNKNOWN` 不参与加总。官方对象尺寸指分发文件，未测展开后的文件系统占用。`duplicate_of` 只在能确认来源时标逻辑母体，不能据此作 archive SHA 去重。

## TCP/CARLA：可定价候选，LAW 同一性未证实

TCP [作者 README](https://github.com/OpenDriveLab/TCP/blob/main/README.md#dataset) 指向 [HF 发布仓](https://huggingface.co/datasets/craigwu/tcp_carla_data)，要求将三段顺序合并为 ZIP，称约 115G；CARLA 为 0.9.10.1。下列 `size` 取官方 HF [固定 revision `acf13f86b50eb924e3ec76966c5123de0874e6ff` 的 API](https://huggingface.co/api/datasets/craigwu/tcp_carla_data/tree/main?recursive=false&expand=true)（2026-09-28 元信息核查），sha256 为各 LFS 对象 ID；只读取元信息，未下载分包或合并 ZIP。

| asset_id | paper_id / role | version / split / modality | file / shard | bytes | source URL / revision或日期 | duplicate_of | 压缩/公开 | status |
|---|---|---|---|---:|---|---|---|---|
| TCP-CARLA-AA | P0048 候选／CARLA 训练 | TCP release／train+val／打包的 CARLA 帧及标注，ZIP 内 member 未验 | `tcp_carla_data_part_aa` | **42,949,672,960** | [HF 文件](https://huggingface.co/datasets/craigwu/tcp_carla_data/blob/acf13f86b50eb924e3ec76966c5123de0874e6ff/tcp_carla_data_part_aa)，LFS SHA256 `9f5e0adfe3a27e231a655a2503e1c5e28fb165d27484b896a6e5ce8f3147952b` | UNKNOWN | ZIP 分卷／PUBLIC | VERIFIED（TCP 对象）；CANDIDATE（LAW） |
| TCP-CARLA-AB | P0048 候选／CARLA 训练 | 同上 | `tcp_carla_data_part_ab` | **42,949,672,960** | [HF 文件](https://huggingface.co/datasets/craigwu/tcp_carla_data/blob/acf13f86b50eb924e3ec76966c5123de0874e6ff/tcp_carla_data_part_ab)，LFS SHA256 `ce79c6ad299d78884c37467125ba0413a0451b95e808afd365732bbb43fbdfdd` | UNKNOWN | ZIP 分卷／PUBLIC | VERIFIED（TCP 对象）；CANDIDATE（LAW） |
| TCP-CARLA-AC | P0048 候选／CARLA 训练 | 同上 | `tcp_carla_data_part_ac` | **37,549,639,870** | [HF 文件](https://huggingface.co/datasets/craigwu/tcp_carla_data/blob/acf13f86b50eb924e3ec76966c5123de0874e6ff/tcp_carla_data_part_ac)，LFS SHA256 `09295b608791cde259f0d0bcc0fe812116382a0a039334e38461a209187af146` | UNKNOWN | ZIP 分卷／PUBLIC | VERIFIED（TCP 对象）；CANDIDATE（LAW） |
| LAW-CARLA | P0048／训练 | CARLA 0.9.10.1、Roach、189K 帧／原采集模态与 split UNKNOWN | 作者实际使用的对象 UNKNOWN | **UNKNOWN** | [LAW 原文 §5.1](https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md/P0048_LAW/P0048_LAW.raw.md#L165) | 与 TCP-CARLA 同一性 UNKNOWN | UNKNOWN／公开状态 UNKNOWN | UNKNOWN |

复算 `42,949,672,960 + 42,949,672,960 + 37,549,639,870 = 123,448,985,790 B = 0.123448985790 TB`，约 114.97 GiB。LAW 明确说跟随 TCP、DriveAdapter、用同版 CARLA/Roach、189K 帧；[ThinkTwice 数据准备](https://github.com/OpenDriveLab/ThinkTwice/blob/main/docs/DATA_PREP.md) 还写 TCP 有 189K 训练帧及后续验证帧，但没有给 LAW 训练路径、TCP ZIP 的 member ID 或校验和。**匹配采集路线不等于文件相同**；ThinkTwice 的 189K 帧约 8 TB 采用多模态高分辨率采集设置，只作独立敏感性参照，不与 TCP 候选包相加，也不是 LAW 上限。

## Bench2Drive：按版本与来源分账

| asset_id | paper_id / role | version / split / modality | file / shard | bytes | source URL / revision或日期 | duplicate_of | 压缩/公开 | status |
|---|---|---|---|---:|---|---|---|---|
| B2D-BASE-OLD | P0045/P0049/P0061/P0065/P0073/P0076/P0077 等／训练评测 | 旧 Base／1,000 clips／预录传感器 | 官方 HF 1,000 个 `.tar.gz` 聚合 | **334,866,900,094** | [官方 HF tree](https://huggingface.co/datasets/rethinklab/Bench2Drive/tree/ce56cfbc26edf7796586e26fd44644f0ac2f6bcc) `size` 汇总；[官方 0.0.3 说明](https://github.com/Thinklab-SJTU/Bench2Drive/blob/0.0.3/README.md)，2026-09-28 | 与 v0.0.4 不宣称同一内容 | 压缩／PUBLIC | VERIFIED（官方对象汇总；逐对象表未留存） |
| B2D-004-NODEPTH | 22 篇直接 0 篇／可选项目版本 | v0.0.4／1,100 routes／无 depth | 官方 HF 1,100 个 `.tar.gz` 聚合 | **415,362,197,807** | [官方 HF tree](https://huggingface.co/datasets/rethinklab/Bench2Drive-V0.0.4/tree/d84ae18cf20a88b9220df1bc15c073d8824b7ac1) `size` 汇总；[官方 0.0.4 说明](https://github.com/Thinklab-SJTU/Bench2Drive/blob/0.0.4/README.md)，2026-09-28 | 旧 Base 不作版本替代 | 压缩／PUBLIC | VERIFIED（官方对象汇总；逐对象表未留存） |
| B2D-004-MAP | 同上／地图 | v0.0.4 map／12 Town HD map | 历史 inventory 的 12 个 `.npz` 与 12 个 sidecar 目录 | **3,146,330,646** | [项目 2026-09-21 inventory](../../datasets/resource_inventory_20260921.md#4-bench2drive)；map 未见于上述 no-depth HF tree | B2D-004-NODEPTH 的配套目录，非同一文件 | NPZ+sidecar／项目历史记录 | VERIFIED（inventory；非纯 payload object size） |
| B2D-004-INVENTORY | 同上／历史目录对照 | v0.0.4／no-depth + map，各带 sidecar | 1,100+12 个 payload 及对应 sidecar | **418,508,847,603** | [项目历史 inventory](../../datasets/resource_inventory_20260921.md#4-bench2drive) | 上两行的目录计量，不另加入情景 | 目录／项目记录 | VERIFIED（inventory） |

新版本官方 no-depth 对象加历史 map **目录**为 `415,362,197,807 + 3,146,330,646 = 418,508,528,453 B`，这是混合来源的压缩发布/目录口径。历史两个子目录之和为 **418,508,843,507 B**；历史汇总行 `418,508,847,603 B` 还多 **4,096 B**（未定位到具体文件）。汇总行与混合口径相差 **319,150 B = 315,054 + 4,096 B**；其中 315,054 B 是历史 no-depth 子目录比官方对象和多的量。map `.npz` 与 sidecar 未逐文件拆分，不能称 `3,146,330,646 B` 为纯地图 payload。路线 XML 是 CARLA 仿真协议，不计入离线传感器包。Full 约 4 TB、v0.0.4 depth 约 7.3 TB 属不同模态/版本，22 篇没有整包使用证据。

## VLA 原媒体：有界路径核查与未闭合的唯一数

ReCogDrive 作者 [来源表](https://github.com/xiaomi-research/recogdrive#driving-pretraining-datasets) 列 12 个外部驾驶 QA 源及 NAVSIM/Bench2Drive 派生。固定 [HF revision `f55bb18e0aca846bbedfb516760a1b9b7cfe3ebf`](https://huggingface.co/datasets/owl10/ReCogDrive_Pretraining/tree/f55bb18e0aca846bbedfb516760a1b9b7cfe3ebf) 的 **17 个 JSONL 对象合计 3,789,771,567 B**，只是 annotation。前一轮对 17/17 个文件各读取首 4,096 B（共至多 69,632 B），对 `image`/`images` 及视频路径字段做前缀观察；对 SGDrive 的 [作者 `sgdrive.jsonl`](https://huggingface.co/SII-Whaleice/SGDrive/blob/c6379bea8aaf635883b33fcc99499b59d42aad1e/sgdrive.jsonl) 首 1 MiB 做过有界读取，官方对象 932,449,828 B。**这些临时前缀未保存在仓库，不能据此宣称全量扫描、唯一 URI 数或跨源 SHA 去重**。本次没有再下载 JSONL 或原媒体。路径形态观察如下；这是可追溯的字段/母体分类，不是完整行数统计。

| annotation 来源 | 前缀中出现的媒体字段/路径形态（省略动态文件名） | 候选母体与状态 |
|---|---|---|
| `Bench2drive_QA`, `Bench2drive_Traj` | `./Bench2drive/v1/<route>/camera/rgb_front/...jpg` | Bench2Drive；`v1` 与旧 Base 的 archive 成员对应尚未证明，PARTIAL |
| `Navsim_ReCogDrive`, `Navsim_Traj` | `./NAVSIM/dataset/sensor_blobs/trainval/.../CAM_F0/...jpg`、`./dataset/sensor_blobs/trainval/...` | NAVSIM/OpenScene trainval 逻辑母体，PARTIAL；独立 archive hash 未比 |
| `DriveLM` 两变体、`Nuinstruct`, `Nuscenes-QA`, `Omnidrive`, `Senna` | `/mnt/evad_fs/opensource-data/nuscenes/samples/CAM_FRONT/...jpg` 或 `samples/CAM_.../...jpg` | nuScenes 路径规范；个别前缀样本重复文件名，未计唯一数，PARTIAL |
| `LingoQA` | `./LingoQA/Scenery/images/train/<id>/<frame>.jpg` | LingoQA 独立图像源，实际子集 UNKNOWN |
| `Drama` | `./Drama/combined/titan/clip_.../movie.gif` | DRAMA 源媒体，申请受限，RESTRICTED |
| `SUTD` | `./SUTD/compressed_videos/<id>.mp4` | **需要视频**；Zenodo 的 20,534,486,181 B `.h5`/annotation 包不能代替，RESTRICTED/UNKNOWN |
| `CODA-LM`, `Maplm` | `./CODA-LM/images/0001.jpg`、`./MAPLM/maplm_v0.1/train/<id>/photo_forward.jpg` | 各自发布资产与 nuScenes 父体的逐图关系 UNKNOWN |
| `Drivegpt4`, `Talk2Car` | `training_<id>_...png`、`img_train_0.jpg` | 平铺文件名不足以归属原始媒体，UNKNOWN |
| SGDrive `sgdrive.jsonl` | `"image": ["navsim_data/sensor_blobs/trainval/.../CAM_F0/...jpg", ...]`，样本中四个时序前视帧 | NAVSIM/OpenScene trainval 逻辑母体，PARTIAL |

**统计边界：**覆盖的 annotation 对象数是 ReCogDrive 17、SGDrive 1；实际逐行扫描数、媒体 URI 读取总数、规范化后唯一数、未归属唯一数均为 **UNKNOWN**，绝不可把 17 或四帧当唯一媒体总数。全量闭合需按每条 JSONL 的 `image/images/video/image_path`（包括字符串、数组、字典）抽 URI，去掉本地挂载前缀，规范大小写与分隔符，以 `(source_dataset, canonical_relative_path)` 去重；父体内再用官方文件 ID/散列核对，不能只按 basename 跨数据集去重。路径或 annotation count 均不等于压缩包 byte。ReCogDrive 原图依赖 nuScenes/OpenScene/B2D 时先作为父体覆盖情景；LingoQA、DRAMA、SUTD 等独立媒体并集仍 UNKNOWN。

## 其他状态行与峰值

| asset_id | paper_id / role | version / split / modality | file / shard | bytes | source URL / revision或日期 | duplicate_of | 压缩/公开 | status |
|---|---|---|---|---:|---|---|---|---|
| WAMFLOW-GENERAL-VQA | P0074／VLM 预训练 | 论文称 LLaVA-v1.5 来源 3.4M；split 与图像模态清单 UNKNOWN | 图像 URI 集合 UNKNOWN | UNKNOWN | [原文 §3.4](https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md/P0074_WAM-Flow/P0074_WAM-Flow.raw.md#L157)；[作者配置 `747dad9`](https://github.com/fudan-generative-vision/WAM-Flow/blob/747dad929a419e11c7fb2fcbd57fec90e9e31a55/config/pretrain.yaml) 引 `llava_v1_5_mix665k_2.jsonl`，2026-09-28 | LLaVA/其他 VQA 重复 UNKNOWN | 原图／PUBLIC 可得性不明 | PARTIAL |
| WAMFLOW-NAVSIM-ANN | P0074／NAVSIM 标注 | `navsim_668k.jsonl`／NAVSIM | 单个 JSONL | **414,319,989** | [作者模型仓 data](https://huggingface.co/fudan-generative-ai/WAM-Flow/tree/main/data)，2026-09-28；[LLaVA 标准 README](https://github.com/haotian-liu/LLaVA#visual-instruction-tuning)另说 665K 标注须从组成数据集取得图片 | NAVSIM/OpenScene 逻辑母体 | 直接文本／PUBLIC | VERIFIED（标注）；不可充当上行图片 |
| GRAPHWORLD-NUSC-C | P0065／Snow、Rain、Fog 开环验证 | nuScenes val，三天气；severity 未披露 | 预生成图像包或运行时函数 UNKNOWN | UNKNOWN | [原文 §5.1/附录](https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md/P0065_GraphWorld/P0065_GraphWorld.raw.md#L358)；[nuScenes-C 原作者函数](https://github.com/thu-ml/3D_Corruptions_AD#how-to-use)可对 camera/LiDAR 在 test-time 生成，2026-09-28 | nuScenes val；派生图像不可未经检验去重 | 模态/包 UNKNOWN／PUBLIC | PARTIAL |
| UNIDRIVE-DRIVEBENCH | P0076／驾驶理解评测 | DriveBench；实际 corruption 子集 UNKNOWN | [作者另列 image bundle](https://drive.google.com/file/d/1_MqbX1oXH9S55eC0r_rZvvaoAD5GVOyW/view?usp=share_link)、HF text 与 `data/corruption/` | UNKNOWN | [官方 DATA_PREPAER.md](https://github.com/worldbench/DriveBench/blob/main/docs/DATA_PREPAER.md)，2026-09-28 | nuScenes samples 为母体，额外腐蚀图像未比对 | 预生成媒体／PUBLIC 页面可见 | PARTIAL |
| W0-INHOUSE | P0072／训练与百场景测试 | in-house 70M frames、>1M clips、100 test scenes；模态/编码 UNKNOWN | 私有存储清单不公开 | UNKNOWN | [原文 §4.1](https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md/P0072_DriveVLA-W0/P0072_DriveVLA-W0.raw.md#L133) | 不以 nuPlan/NAVSIM 替换 | UNKNOWN／PRIVATE | PRIVATE/RESTRICTED |
| SGDRIVE-HIDDEN-CACHE | P0070／Diffusion Planner IL 加速 | 作者代码 `fcda385`；navtrain/navtest/navmini 可选 | VLM hidden states cache；非原始媒体 | **约 1–2 TB，发布方估计** | [作者 Train_Eval.md](https://github.com/LogosRoboticsGroup/SGDrive/blob/fcda385371f8f40af5b8969ca5090be06f421358/docs/Train_Eval.md)；[缓存脚本](https://github.com/LogosRoboticsGroup/SGDrive/blob/fcda385371f8f40af5b8969ca5090be06f421358/scripts/cache_dataset/run_caching_sgdrive_hidden_state.sh)，2026-09-28 | 从 VLM/NAVSIM 生成，不与原图按 byte 去重 | 生成目录／非发布包 | PARTIAL（作者估计；可跳过） |

SGDrive 文档明确说先缓存 **VLM 输出的 hidden states** 以加速 DiT 模仿学习；也允许不缓存、直接联合训练 VLM + DiT，代价是更慢。缓存脚本设置 `agent.cache_hidden_state=True`、`cache_path`，默认示例为 `navmini`，可改 navtrain/navtest；**1–2 TB 不是每个 split、每个硬件/策略的可证峰值**。缓存是否与独立 metric cache、archive 解包目录同时存在、能否训练后删除、各盘是否同盘，作者没有给总 byte 清单，峰值仍 UNKNOWN；盘规划仅在选择该缓存流程时增加条件性空间项。
