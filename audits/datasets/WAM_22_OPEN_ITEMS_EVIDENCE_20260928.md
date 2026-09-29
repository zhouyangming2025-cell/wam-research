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

## VLA 标注媒体路径：全量扫描完成，媒体字节仍未闭合

2026-09-29 对 ReCogDrive 固定 [HF revision `f55bb18e0aca846bbedfb516760a1b9b7cfe3ebf`](https://huggingface.co/datasets/owl10/ReCogDrive_Pretraining/tree/f55bb18e0aca846bbedfb516760a1b9b7cfe3ebf) 的 17 个 JSONL 与 SGDrive 固定 [commit `c6379bea8aaf635883b33fcc99499b59d42aad1e`](https://huggingface.co/SII-Whaleice/SGDrive/tree/c6379bea8aaf635883b33fcc99499b59d42aad1e) 的 `sgdrive.jsonl` 做了完整流式扫描。官方 HF tree API `size` 合计 `3,789,771,567 + 932,449,828 = 4,722,221,395 B`；实际读入字节逐对象与该值一致。共解析 **766,842 行、4,498,508 个媒体路径引用**（4,472,191 image、26,317 video/GIF），无 JSON 解析错误；18 个对象中 17 个实际 SHA-256 与官方 LFS OID 相符，Talk2Car 对象未提供 LFS OID。没有请求任何图像或视频。`4,722,221,395 B` 是 JSONL 标注文本，不是媒体体积。

规范化规则和逐对象 URL、版本、size、实际 SHA-256、行数、引用数、逐来源唯一路径数保存在[机器可读扫描结果](WAM_VLA_MEDIA_PATH_AUDIT_2026-09-29.json)；可用[扫描脚本](../../scripts/datasets/audit_vla_media_paths.py)按相同固定 revision 复核。扫描递归读取 `image/images/video/videos/image_path(s)/video_path(s)/frame_path(s)/clip_path(s)/media_path(s)` 字段；规范斜杠和 URL 转义，按数据集标记剥离挂载根，以 `(source family, canonical relative path)` 计路径级唯一值。**不按 basename 去重、不跨源媒体 hash 去重**；因此下表是媒体路径引用/路径并集，不是经内容哈希验证的独立文件数或字节数。

| 注释来源 | JSONL 行数 | URI 引用数 | 本文件唯一路径 | 归属依据与主要路径 | 文件/媒体状态 |
|---|---:|---:|---:|---|---|
| Bench2drive QA | 49,942 | 299,652 | 299,652 | `Bench2drive/v1/...`；Bench2Drive | 路径直接标识；与旧 Base archive 的内容 hash 未比 |
| Bench2drive Traj | 196,761 | 1,180,566 | 1,180,566 | `Bench2drive/v1/...`；Bench2Drive | 与 QA 文件共享 238,104 条规范路径，不是内容 hash 去重 |
| CODA-LM | 20,318 | 20,318 | 15,516 | `images/` 与 `images_w_boxes/`；CODA-LM | 两目录共 4,883 与 10,633 条唯一路径；原图包与 nuScenes 重复关系未知 |
| DRAMA | 16,401 | 16,401 | 16,401 | `combined/<clip>/...movie.gif`；DRAMA | 39 个 `combined/` 下 clip 目录；原始视频/帧/光流包字节仍 UNKNOWN/RESTRICTED |
| DriveLM change-box / original-box | 各 4,072 | 各 24,432 | 各 24,432 | `samples/CAM_*`；nuScenes 六相机 | 两 JSONL 共享 24,432 条规范路径；不代表独立 annotation 的内容字节 |
| DriveGPT4 | 26,319 | 210,552 | 113,320 | 载荷为平铺相对路径；依据来源文件及配置 root `/Drivegpt4/BDD_X_imgs_select` 归属 BDD-X | **上下文推断**；第三方同名 tar 仍未与这些文件逐项/hash 证明相同 |
| LingoQA | 26,824 | 134,120 | 134,120 | `Action/images/train` 116,770；`Scenery/images/train` 17,350 | 两个 split 都在 annotation 中出现；训练配置仅列 Action root，实际路径解析/分包字节仍需核 |
| MAPLM | 10,612 | 31,836 | 31,836 | `maplm_v0.1/train/...`；MAPLM | 路径直接标识；约 18.92 GB 主分卷不是该子集的实测字节 |
| NAVSIM ReCogDrive / NAVSIM Traj | 各 85,109 | 各 85,109 | 各 85,109 | `sensor_blobs/trainval/...`；NAVSIM/OpenScene | 两文件规范路径集合完全重合；与 OpenScene 官方 archive 未做文件 hash |
| NuInstruct | 57,317 | 1,542,258 | 49,074 | `samples/CAM_*`；nuScenes | 路径模式直接识别；大量引用在同文件内重复 |
| nuScenes-QA | 24,988 | 149,928 | 149,928 | `samples/CAM_*`；nuScenes | 六相机图像路径 |
| OmniDrive | 28,009 | 168,054 | 168,054 | `samples/CAM_*`；nuScenes | 六相机图像路径；公开配置 length 为 28,010，与实有行数差 1 |
| SUTD TrafficQA | 9,916 | 9,916 | 9,916 | `compressed_videos/*.mp4`；SUTD TrafficQA | annotation 明确引用 MP4；Zenodo 20,534,486,181 B features/annotation 不能代替原视频 |
| Senna | 27,885 | 167,310 | 167,310 | `samples/CAM_*`；nuScenes | 配置 length 27,813，比对象实际行数少 72 |
| Talk2Car | 8,079 | 8,079 | 8,079 | 平铺图片名；依据 annotation 源与配置 root `/Talk2Car/imgs` 归属 | **上下文推断**；不能仅凭 basename 证明媒体母体 |
| SGDrive `sgdrive.jsonl` | 85,109 | 340,436 | 126,032 | `navsim_data/sensor_blobs/trainval/.../CAM_F0/...`；NAVSIM/OpenScene | 每行四个前视时序 image 路径；与两份 ReCogDrive NAVSIM JSONL 各共享 85,109 条规范路径 |

来源家族并集为 **1,873,206 个规范路径**：Bench2Drive 1,242,114；nuScenes 175,872（六个 `CAM_*` 目录各 29,312）；NAVSIM/OpenScene 126,032；DriveGPT4/BDD-X 113,320；LingoQA 134,120；MAPLM 31,836；DRAMA 16,401；CODA-LM 15,516；SUTD 9,916；Talk2Car 8,079。路径标记或 annotation 上下文 fallback 后未归类路径为 0；但 **DriveGPT4 与 Talk2Car 的 121,399 个唯一路径来自文件/配置上下文，不是路径字符串自行证明**。

可直接复核的跨 JSONL 路径重用：Bench2Drive QA/Traj 共享 238,104 路径；两份 ReCogDrive NAVSIM 文件各 85,109 路径完全相同，SGDrive 也分别共享这 85,109 条，三者并集 126,032；nuScenes 六份 annotation 合计 583,230 个“每文件唯一路径出现”，合并后 175,872 个路径，重复出现超出并集 407,358 次，逐文件 pairwise 交集见 JSON。跨不同 source family 的媒体内容未读、未计算 SHA；不能据此排除 CODA-LM 等源包与 nuScenes 的内容重合。

**容量结论不因路径计数改变：**这些 URI 数不是压缩包 byte。LingoQA 同时出现 Action 与 Scenery，但包页面约数只说明可见整包，不给这两组引用的精确子集字节；DRAMA、SUTD 原媒体体积仍 UNKNOWN/RESTRICTED；DriveGPT4 同名候选包没有逐 URI/hash 绑定。容量情景不得将 4.72 GB annotation 字节当媒体容量，也未据帧数/路径数推算媒体 byte。ReCogDrive 代码对本地图片调用 `os.path.join(root, image_path)`，LingoQA 与部分带前缀的相对路径仍须与训练配置根一起验证实际可解析性：[固定代码](https://github.com/xiaomi-research/recogdrive/blob/6b8d8f5e01346c71094651c81dcaf66405dbc04e/internvl_chat/internvl/train/internvl_chat_pretrain.py#L450-L455)。


## ReCogDrive 训练配置：root/记录数不是媒体容量

作者固定提交 `6b8d8f5e01346c71094651c81dcaf66405dbc04e` 的 [`recogdrive_pretrain.json`](https://github.com/xiaomi-research/recogdrive/blob/6b8d8f5e01346c71094651c81dcaf66405dbc04e/internvl_chat/shell/data_info/recogdrive_pretrain.json) 明确给出下列本地根目录和配置 `length`。它证明训练配置期望读取这些来源，但 `length` 是配置样本计数，不是独立文件数、唯一媒体数或 byte；不能直接相加为资产容量。NAVSIM 两个来源各 85,109 条，其中 `Navsim` 的 `repeat_time=2`；LLaVA 行 `repeat_time=0.2`。

| 配置源 | root（去掉 `/path/to`） | length | repeat_time |
|---|---|---:|---:|
| Navsim | `/NAVSIM/dataset` | 85,109 | 2 |
| Navsim_QA | `/NAVSIM/dataset` | 85,109 | 1 |
| CODA-LM | `/CODA-LM/Val` | 20,318 | 1 |
| DriveLM | `/nuscenes` | 4,072 | 1 |
| LingoQA | `/LingoQA/Action/images` | 26,824 | 1 |
| MAPLM | `/MAPLM/maplm_v0.1` | 10,612 | 1 |
| Nuinstruct | `/nuscenes` | 57,317 | 1 |
| Omnidrive | `/nuscenes` | 28,010 | 1 |
| SUTD | `/SUTD/compressed_videos` | 9,916 | 1 |
| Talk2Car | `/Talk2Car/imgs` | 8,079 | 1 |
| NuScenes-QA | `/nuscenes` | 24,988 | 1 |
| Drivegpt4 | `/Drivegpt4/BDD_X_imgs_select` | 26,319 | 1 |
| Senna | `/nuscenes` | 27,813 | 1 |
| Drama | `/Drama/drama_data/combined` | 16,404 | 1 |
| llava | `/llava` | 665,298 | 0.2 |

最接近的可定价项是 DriveGPT4：第三方 [HF 仓](https://huggingface.co/datasets/owl10/Drivegpt4-BDD/tree/main) 有 `BDD_X_imgs_select.tar`，页面显示 21.9 GB（非精确 byte、非论文作者发布仓）；与配置 root 同名，故作为**候选包**，未 hash/逐路径证明完全相同，也不代表论文用了完整包。LingoQA 配置指向 `Action/images`，而本次以前缀读到的标注路径是 `Scenery/images/train`；在全量样本路径核查完成前，不判断哪个 split 真正被读取。MAPLM 配置锁定 `maplm_v0.1`；官方 README 指向的 [Google Drive 文件夹](https://drive.google.com/drive/folders/1cqFjBH8MLeP6nKFM0l7oV-Srfke-Mx1R?usp=sharing) 页面于 2026-09-28 显示：四个主 split archive 分卷 `.z01/.z02/.z03/.zip` 分别为 5/5/5/3.92 GB，标称合计约 **18.92 GB**（Google Drive UI 显示值、非精确 byte；README 的合并命令恰好只使用这四个分卷）。同目录另有 `maplm_v0.1_small.zip` 230.5 MB、`pid_splits.json` 191 KB、`problems.json` 31.5 MB；这些对象的替代/附属关系未确认，不加到主 archive 总和；若按 Google Drive UI 把文件夹内所有可见对象都留存，名义合计约 **19.18 GB**，仍为显示标签加总。README 还提到 2024 年 2M 点云/HD map 发布，但未给这版可识别分卷或字节清单，故不能以 v0.1 的 18.92 GB 代替，也不相加。

DRAMA 配置指向 `drama_data/combined`。Honda [官方说明](https://usa.honda-ri.com/drama) 确认 17,785 个约 2 秒片段、SEKONIX 与 GoPro 双摄及 CAN/IMU；raw 包结构同时含 `frame_*.png`、`flow_*.png` 和 `movie.gif`。官方没有给下载字节/分卷 manifest，且数据申请限大学身份和非商业研究，因此容量继续为 UNKNOWN。SUTD root 则明确是压缩视频目录；已列 Zenodo 特征+标注 20.534 GB 不是这批视频。

## WAM-Flow：论文 3.4M 与可见配置/公开文件未闭合

【原文事实】P0074 报告 6.5M VQA：3.4M LLaVA-v1.5 来源通用多模态 VQA + 3.1M ReCogDrive 驾驶 QA。

【代码事实】固定作者 [`config/pretrain.yaml`](https://github.com/fudan-generative-vision/WAM-Flow/blob/747dad929a419e11c7fb2fcbd57fec90e9e31a55/config/pretrain.yaml) 的 `data_list` 共 16 项，首项是占位路径 `path/to/llava_v1_5_mix665k_2.jsonl`；另列 CODA-LM、DriveGPT4、LingoQA、MAPLM、nuScenes QA、OmniDrive、Senna、Talk2Car、DriveLM、nuPlan/NAVSIM ReCogDrive、NAVSIM 668K/103K、nuScenes train，其中 `navsim_recogdrive.jsonl` 被列两次。作者 [`SupervisedDataset` loader](https://github.com/fudan-generative-vision/WAM-Flow/blob/747dad929a419e11c7fb2fcbd57fec90e9e31a55/flow_matching/data/navsim.py) 将各 JSONL 行并入数据集并用 PIL 按 `image` 路径打开本地原图；所以若该预训练配置实际运行，图像媒体是硬依赖。

公开的 WAM-Flow [SFT launcher](https://github.com/fudan-generative-vision/WAM-Flow/blob/747dad929a419e11c7fb2fcbd57fec90e9e31a55/scripts/sft_navsim.sh) 只指向 `sft_navsim.yaml`，其 `data_list` 仅 `data/navsim_668k.jsonl`；作者 HF data 页也只列这一 NAVSIM 标注文件（414,319,989 B），没有 3.4M general VQA manifest/图像包。配置中的 `mix665k_2` 文件名与论文 3.4M 不能因名字相近而等同于标准 LLaVA 665K，也不能假设这 665K 覆盖 3.4M 训练样本。标准 LLaVA v1.5 所需的 COCO、GQA、OCR-VQA、TextVQA、Visual Genome 图像只是**可能上游候选**，在作者样本级映射确认前不加入本账本或任何容量总和。

**判断：**现有公开配置不足以复原论文所报 3.4M 通用数据的确切组成；可能是配置不完整、过期或仅为子集，现有证据无法区分。故图像 URI、独立来源包、去重关系、字节和是否超过 0.1 TB 均保留 UNKNOWN。NAVSIM 668K 标注包与此项无替代关系。

## 其他状态行与峰值

| asset_id | paper_id / role | version / split / modality | file / shard | bytes | source URL / revision或日期 | duplicate_of | 压缩/公开 | status |
|---|---|---|---|---:|---|---|---|---|
| WAMFLOW-GENERAL-VQA | P0074／VLM 预训练 | 原文 3.4M 通用 VQA；代码占位配置列 `llava_v1_5_mix665k_2.jsonl`，二者映射 UNKNOWN | 图像 URI 与独立发布 shard UNKNOWN | UNKNOWN | [原文 §3.4](https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md/P0074_WAM-Flow/P0074_WAM-Flow.raw.md#L157)；[固定 pretrain.yaml](https://github.com/fudan-generative-vision/WAM-Flow/blob/747dad929a419e11c7fb2fcbd57fec90e9e31a55/config/pretrain.yaml)；[loader](https://github.com/fudan-generative-vision/WAM-Flow/blob/747dad929a419e11c7fb2fcbd57fec90e9e31a55/flow_matching/data/navsim.py) | 标准 LLaVA 上游源/其他 VQA 重复 UNKNOWN | 原图可用性不等于标注公开 | PARTIAL |
| WAMFLOW-NAVSIM-ANN | P0074／NAVSIM 标注 | `navsim_668k.jsonl`／NAVSIM | 单个 JSONL | **414,319,989** | [作者模型仓 data](https://huggingface.co/fudan-generative-ai/WAM-Flow/tree/main/data)，2026-09-28；[LLaVA 标准 README](https://github.com/haotian-liu/LLaVA#visual-instruction-tuning)另说 665K 标注须从组成数据集取得图片 | NAVSIM/OpenScene 逻辑母体 | 直接文本／PUBLIC | VERIFIED（标注）；不可充当上行图片 |
| GRAPHWORLD-NUSC-C | P0065／Snow、Rain、Fog 开环验证 | nuScenes val，三天气；severity 未披露 | 预生成图像包或运行时函数 UNKNOWN | UNKNOWN | [原文 §5.1/附录](https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md/P0065_GraphWorld/P0065_GraphWorld.raw.md#L358)；[nuScenes-C 原作者函数](https://github.com/thu-ml/3D_Corruptions_AD#how-to-use)可对 camera/LiDAR 在 test-time 生成，2026-09-28 | nuScenes val；派生图像不可未经检验去重 | 模态/包 UNKNOWN／PUBLIC | PARTIAL |
| UNIDRIVE-DRIVEBENCH | P0076／驾驶理解评测 | DriveBench：官方页面称 17 settings / 19,200 frames；具体 corruption 文件集合与样本选择 UNKNOWN | [图像 bundle](https://drive.google.com/file/d/1_MqbX1oXH9S55eC0r_rZvvaoAD5GVOyW/view?usp=share_link)、HF text 与 `data/corruption/`；Google Drive viewer 显示“文件太大而无法预览”，未显示 byte/size | UNKNOWN | [官方 README](https://github.com/worldbench/DriveBench)；[官方 DATA_PREPAER.md](https://github.com/worldbench/DriveBench/blob/main/docs/DATA_PREPAER.md)，2026-09-28 | nuScenes samples 为母体，额外腐蚀图像未比对 | 预生成媒体／PUBLIC 页面可见 | PARTIAL |
| MAPLM-2024-2M | ReCogDrive 上游版本边界候选／训练 | README 描述 2024/01 release：2M 3D point clouds + BEV + 多张全景图 + HD map annotation；确切 version ID、分卷及 ReCogDrive 是否涉及 UNKNOWN | 2M 版公开包清单未从 README/linked v0.1 folder 锁定 | UNKNOWN | [官方 MAPLM README](https://github.com/LLVM-AD/MAPLM)；[ReCogDrive 固定配置](https://github.com/xiaomi-research/recogdrive/blob/6b8d8f5e01346c71094651c81dcaf66405dbc04e/internvl_chat/shell/data_info/recogdrive_pretrain.json)，2026-09-28 | 不与 `maplm_v0.1` 主 archive 自动合并 | 公开状态部分可见／容量 UNKNOWN | OPEN; 计盘仍待版本确认 |
| W0-INHOUSE | P0072／训练与百场景测试 | in-house 70M frames、>1M clips、100 test scenes；模态/编码 UNKNOWN | 私有存储清单不公开 | UNKNOWN | [原文 §4.1](https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md/P0072_DriveVLA-W0/P0072_DriveVLA-W0.raw.md#L133) | 不以 nuPlan/NAVSIM 替换 | UNKNOWN／PRIVATE | PRIVATE/RESTRICTED |
| SGDRIVE-HIDDEN-CACHE | P0070／Diffusion Planner IL 加速 | 作者代码 `fcda385`；navtrain/navtest/navmini 可选 | VLM hidden states cache；非原始媒体 | **约 1–2 TB，发布方估计** | [作者 Train_Eval.md](https://github.com/LogosRoboticsGroup/SGDrive/blob/fcda385371f8f40af5b8969ca5090be06f421358/docs/Train_Eval.md)；[缓存脚本](https://github.com/LogosRoboticsGroup/SGDrive/blob/fcda385371f8f40af5b8969ca5090be06f421358/scripts/cache_dataset/run_caching_sgdrive_hidden_state.sh)，2026-09-28 | 从 VLM/NAVSIM 生成，不与原图按 byte 去重 | 生成目录／非发布包 | PARTIAL（作者估计；可跳过） |

SGDrive 文档明确说先缓存 **VLM 输出的 hidden states** 以加速 DiT 模仿学习；也允许不缓存、直接联合训练 VLM + DiT，代价是更慢。缓存脚本设置 `agent.cache_hidden_state=True`、`cache_path`，默认示例为 `navmini`，可改 navtrain/navtest；**1–2 TB 不是每个 split、每个硬件/策略的可证峰值**。缓存是否与独立 metric cache、archive 解包目录同时存在、能否训练后删除、各盘是否同盘，作者没有给总 byte 清单，峰值仍 UNKNOWN；盘规划仅在选择该缓存流程时增加条件性空间项。
