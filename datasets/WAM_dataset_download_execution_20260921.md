# WAM 数据集下载与落地执行底稿（Windows → SSH → 210）

**版本日期：2026-09-21**  
**用途：交给本地 Agent 进行下载链路、manifest、批次、验收、传输与落盘准备。**  
**目标：在“新增数据总量原则上不超过 10 TB（十进制）”的条件下，为 planning-centric WAM / driving world model 研究建立一套可复用、可审计、可恢复的数据基础资产。**

---

## 0. 本文的证据口径

本文严格区分四类体积/事实状态，后续 Agent 不允许混写：

- **VERIFIED（现场已验证）**：已经在 210 上实测或由当前官方文件页直接给出。
- **OFFICIAL-REPORTED（官方报告）**：官方项目页 / 论文 / 官方 HF repo 明确给出的总量或规模。
- **ESTIMATE（预算估算）**：基于局部文件大小、历史 manifest 或外推得到，只能用于空间预留。
- **PENDING-MANIFEST（待冻结）**：必须在真正下载前通过当前官方对象列表 / `hf download --dry-run` / S3 HEAD 或 listing 重新锁定。

### 0.1 固定执行约束

本轮采用：

> **Windows 机器负责公网下载与第一阶段验收 → 通过 SSH 系列工具上传到 210 → 210 做第二阶段验收、正式入库与必要解包。**

**210 不作为主要公网下载节点。**

原因：

1. Windows 侧互联网环境通常更稳定，浏览器、HF gated access、YouTube/yt-dlp、AWS CLI 登录与调试更方便。
2. TB 级下载失败时，应在本地 staging 恢复，而不是让 210 同时承担外网不稳定、下载中间态和正式数据根污染。
3. 210 只接收已经有 manifest、文件大小和来源记录的数据，更容易做到正式数据根可审计。
4. SSH 链路可以独立重试，不把“公网下载失败”和“内网上传失败”混成一个问题。

### 0.2 10 TB 预算怎么解释

“10 TB 可接受”不等于可以把所有归档、解包副本、HF cache、临时文件同时长期保存。

建议预算：

| 项目 | 规划量 |
|---|---:|
| raw nuPlan：DB + 43 train camera | **约 6.2 TB，PENDING-MANIFEST** |
| DrivingDojo 全量公开 repo | **约 1.689 TB，官方 HF 当前文件量级** |
| CoVLA | **452 GB** |
| HUGSIM | **60.7 GB** |
| OpenDV-mini raw | **44 GB** |
| CityWalker | **6.82 GB** |
| Adv-nuSc | **15.6 GB** |
| **合计（按当前 nuPlan 预算）** | **约 8.47 TB** |

因此本轮推荐把**正式新增目标控制在约 8.5–8.9 TB**，留约 1 TB 以上缓冲给：

- nuPlan 精确 manifest 与旧预算的偏差；
- Hugging Face metadata/cache；
- Windows staging 中间态；
- 210 上传 `.part`；
- 少量选择性解包；
- 校验清单、日志与 sidecar。

**重要：如果以后同时保留约 5 TB nuPlan camera 原 archive + 完整 4 路相机解包副本，很可能把整个方案推过 10 TB。默认不要做“原 archive + 四路全量解包”双份长期保存。**

---

# 1. 210 当前正式数据基线

仓库现场底账：

- `datasets/resource_inventory_20260921.md`
- `datasets/resource_inventory_20260921.json`
- `datasets/NUPLAN_210_INVENTORY_2026-09-19.md`

截至 2026-09-21，210 正式数据根：

```text
/mnt/nas/planning/zhouyangming/wam_datasets
```

总逻辑占用：

```text
5,640,966,287,240 B
≈ 5.641 TB decimal
≈ 5.13 TiB
```

已存在：

| 数据 | 210 状态 | 逻辑占用 |
|---|---|---:|
| OpenScene / NAVSIM | OpenScene v1.1 + NAVSIM v1 + NAVSIM v2 | ~3.045 TB |
| nuPlan | test sensor blobs + mini DB + mini LiDAR + maps + 少量已解 CAM_F0 | ~1.786 TB |
| nuScenes | Core Full + CAN + Map Expansion + camera supplement | ~0.391 TB |
| Bench2Drive | v0.0.4 no-depth + maps | ~0.419 TB |

OpenScene trainval 已现场确认：

```text
trainval camera archives: 1,242,213,272,326 B
trainval LiDAR archives :   882,141,233,382 B
trainval metadata       :     7,052,210,642 B
```

这意味着：

- **不需要再次下载 NAVSIM navtrain 精简 sensor 包。**
- raw nuPlan 的价值不是“补一个 nuPlan 名字”，而是补 **高频原始时序 + 完整 DB/log + 更高的预处理自由度**。

---

# 2. 本轮最终下载范围

## 2.1 主线数据：下载

1. **nuPlan v1.1 raw train DB + val/test DB + 43 个 train camera archive**
2. **DrivingDojo Main + Extra1–Extra5**
3. **CoVLA 全量公开 HF repo**
4. **HUGSIM 全量公开 release**
5. **OpenDV-mini raw video（不提前转 frame cache）**
6. **CityWalker**
7. **Adv-nuSc**

## 2.2 明确不在本轮下载

- nuPlan train/val LiDAR
- nuPlan val camera × 12
- Bench2Drive v0.0.4 depth（官方 HF 约 7.35 TB）
- OpenDV full raw（官方约 3 TB）
- OpenDV full processed frames（官方约 24–25 TB）
- OpenDV-mini 全量 frame cache（官方约 390 GB）
- Waymo Perception raw
- KITTI-360 raw
- PandaSet raw
- full nuScenes-C

这些不是“没价值”，而是本轮 10 TB 预算下收益/成本不如上述主线。

---

# 3. raw nuPlan v1.1

## 3.1 为什么值得下载

raw nuPlan 对当前研究的价值主要有四个：

### A. 高频驾驶视频

OpenScene 是基于 nuPlan 的 compact redistribution，当前主流 planning/NAVSIM 研究使用它非常合适，但它并不能完全替代 raw nuPlan 的高频视觉时序。

WAM / world model 研究关心：

```text
历史连续视频
+ ego motion / trajectory / command
→ future video / future latent / world dynamics
→ planning
```

2 Hz 对普通 planner 往往够用，但对 5–10 Hz 级时序动态、视频预测、latent dynamics、action-conditioned prediction，高频 raw camera 更有价值。

### B. Epona from-scratch 数据链明确依赖 raw nuPlan

Epona 官方 data preparation 明确要求：

```text
splits/trainval/*.db
sensor_blobs/<log>/CAM_*
```

训练 meta 由 `create_nuplan_json.py` 自行生成。

Epona 官方文档：
- https://github.com/Kevin-thu/Epona/blob/main/data_preparation/README.md
- https://github.com/Kevin-thu/Epona

Epona 官方写法甚至是 “download all the splits in NuPlan”，并使用 NuPlan-Download-CLI 作为参考流程。

**因此：raw nuPlan 对 Epona exact/from-scratch reproduction 是真实依赖，不是推测。**

### C. 数据预处理自由度

有 raw data 后可以自行决定：

- 2 / 5 / 10 Hz；
- history 长度；
- future horizon；
- 单前视 / 四视角 / 八视角；
- ego state 对齐方式；
- clip 切分；
- candidate/action conditioning；
- world-model 预训练 corpus 的过滤策略。

这些自由度是 compact redistribution 无法完全恢复的。

### D. 长期研究资产价值

对于实验室长期 WAM 数据池，raw nuPlan 的“未来选择权”很高。当前不训练不等于未来不用。

---

## 3.2 官方基础信息

官方 AWS Open Data：

- Registry：
  https://registry.opendata.aws/motional-nuplan/
- S3 bucket：
  `s3://motional-nuplan/`
- Region：
  `ap-northeast-1`
- AWS CLI 匿名访问：
  ```powershell
  aws s3 ls --no-sign-request s3://motional-nuplan/
  ```
- CloudFront：
  https://d1qinkmu0ju04f.cloudfront.net

官方 nuPlan devkit：

- https://github.com/motional/nuplan-devkit
- Dataset setup：
  https://github.com/motional/nuplan-devkit/blob/master/docs/dataset_setup.md
- nuPlan 下载页：
  https://www.nuscenes.org/nuplan#download

官方 dataset setup 明确说明下载需接受 nuPlan Terms of Use；即使 AWS bucket 可以匿名访问，**数据使用仍要遵守 nuPlan 条款，不能把“无需 AWS 账号”误解成“无许可限制”。**

nuPlan devkit 描述的大规模数据：

- v1.0 / v1.1 系列为约 1,300+ / 1,500 h 级；
- 15,000+ logs；
- Boston / Pittsburgh / Singapore / Las Vegas 等城市。

不同论文对小时数写法不完全一致，本文**不使用某一个小时数字判断“是否完整”**，完整性只按对象 manifest + split 结构判断。

---

## 3.3 本轮 nuPlan 精确对象范围

### Train DB：9 个 archive

```text
nuplan-v1.1_train_boston.zip
nuplan-v1.1_train_pittsburgh.zip
nuplan-v1.1_train_singapore.zip
nuplan-v1.1_train_vegas_1.zip
nuplan-v1.1_train_vegas_2.zip
nuplan-v1.1_train_vegas_3.zip
nuplan-v1.1_train_vegas_4.zip
nuplan-v1.1_train_vegas_5.zip
nuplan-v1.1_train_vegas_6.zip
```

### 其他 DB

```text
nuplan-v1.1_val.zip
nuplan-v1.1_test.zip
```

### Train camera

```text
sensor_blobs/train_set/nuplan-v1.1_train_camera_0.zip
...
sensor_blobs/train_set/nuplan-v1.1_train_camera_42.zip
```

共 **43 个**。

### 本轮不取

```text
train lidar 0..42
val camera 0..11
val lidar 0..11
```

test camera / LiDAR 当前 210 已有，不重复。

---

## 3.4 体积：当前真实状态

### 已知

历史公开信息和旧审计可支持：

```text
train + val DB ≈ 1.04 TB 量级
train + val + test DB ≈ 1.1 TB 量级
```

**但这不是本轮 final byte manifest。**

旧会话曾用：

```text
train_camera_0 ≈ 118.26 GB
× 43
≈ 5.085 TB
```

推导 camera 总量。

这个数字只能标记：

```text
ESTIMATE
```

不能再写成 VERIFIED。

### 当前下载预算

为了容量规划，可临时使用：

```text
43 train camera + train/val/test DB
≈ 6.2 TB
```

状态：

```text
PENDING-MANIFEST
```

### 强制 gate

正式下载前必须生成当前 S3 manifest。

仓库已有脚本：

```text
scripts/datasets/nuplan_public_manifest.py
scripts/datasets/nuplan_archive_head_probe.py
```

Windows 上建议先运行：

```powershell
python scripts/datasets/nuplan_public_manifest.py `
  --prefix public/nuplan-v1.1/ `
  --out manifests/nuplan_v1_1_objects.csv `
  --summary manifests/nuplan_v1_1_objects.summary.json
```

需要冻结字段：

```text
key
size_bytes
last_modified
etag
category
```

对下载范围再生成一份专用 frozen manifest：

```text
nuplan_wam_download_manifest_YYYYMMDD.csv
```

至少包括：

```text
object_key
filename
split
kind
size_bytes
etag
last_modified
source_url
download_status
local_sha256
remote_size_after_ssh
archive_scan_status
```

**如果 54 个目标对象精确总量导致整个新增计划超过 10 TB，应暂停并重新审批，不允许继续用旧 6.2 TB 预算硬跑。**

---

## 3.5 Windows 下载方式

### 推荐：AWS CLI v2

官方 AWS CLI 支持：

```text
aws s3 cp
aws s3 sync
--no-sign-request
```

文档：

- https://docs.aws.amazon.com/cli/latest/reference/s3/cp.html
- https://docs.aws.amazon.com/cli/latest/reference/s3/sync.html

建议不用一个巨大 `sync` 把所有数据一次拉完，而是**按 frozen manifest 逐对象/逐批下载**。

示意：

```powershell
$DEST="D:\wam_stage\nuplan\camera_batch_01"

aws s3 cp `
  s3://motional-nuplan/public/nuplan-v1.1/sensor_blobs/train_set/nuplan-v1.1_train_camera_0.zip `
  "$DEST\nuplan-v1.1_train_camera_0.zip" `
  --no-sign-request `
  --region ap-northeast-1
```

### 批次原则

**不要固定“每 7 个 shard 一批”。**

最终应根据精确 manifest 自动组批：

```text
单批目标：400–700 GB
单批硬上限：800 GB
```

理由：

- Windows staging 不需要同时容纳 6 TB；
- SSH 失败只需重传当前批；
- 每批可以独立验收；
- 210 不会同时出现大量 `.part` 和正式文件。

---

## 3.6 nuPlan archive 格式坑

官方/论文经常把文件写成 `.zip`，但社区已经有明确 issue：

https://github.com/motional/nuplan-devkit/issues/334

Issue #334 中用户下载的 sensor `.zip` 字节数与官方一致，但 `unzip` 报：

```text
End-of-central-directory signature not found
```

你们 210 现场也已经验证过：

> 部分 nuPlan `.zip` 实际为 POSIX tar / 可被 tar 工具读取。

因此本地 Agent 必须：

```powershell
# Windows 若有 bsdtar（Windows 自带 tar/bsdtar 体系可用）
tar -tf .\nuplan-v1.1_train_camera_0.zip > $null
```

210 上再次：

```bash
file nuplan-v1.1_train_camera_0.zip
bsdtar -tf nuplan-v1.1_train_camera_0.zip >/dev/null
```

**禁止：**

```bash
unzip *.zip
```

直接批量执行。

---

## 3.7 nuPlan 长期保存策略

10 TB 预算下，默认建议：

```text
formal raw archive = canonical
```

先长期保存官方 archive，不要立刻把 43 个 camera 全量拆成八路目录。

原因：

- 原 archive 本身约 5 TB 量级；
- 若再完整解四路相机，可能新增 2–3 TB；
- 加上 DrivingDojo/CoVLA 等后容易超过 10 TB。

建议：

```text
/mnt/nas/planning/zhouyangming/wam_datasets/nuplan/
├── raw_archives/
│   ├── db/
│   └── train_camera/
├── manifests/
└── extracted/
    └── 按实验或按 batch 选择性生成
```

优先相机：

```text
CAM_F0
CAM_L0
CAM_R0
CAM_B0
```

但**四路占 camera archive 的真实字节比例目前未知**，不能机械按 50% 算。

第一批 archive 落地后应统计八路 member byte：

```text
CAM_F0
CAM_B0
CAM_L0
CAM_L1
CAM_L2
CAM_R0
CAM_R1
CAM_R2
```

再决定：

- 只保留 archive；
- archive + CAM_F0 hot cache；
- archive + 四路 camera。

---

# 4. DrivingDojo

## 4.1 论文和项目事实

官方项目：

https://drivingdojo.github.io/

论文：

- NeurIPS 2024
- arXiv: https://arxiv.org/abs/2410.10738
- 官方代码：https://github.com/Robertwyq/Drivingdojo

论文/项目报告：

```text
总视频：约 18.2k
总时长：约 150 h
DrivingDojo-Action：约 7.9k
DrivingDojo-Interplay：约 6.4k
DrivingDojo-Open：约 3.9k
```

论文中描述的视频典型设置：

```text
1920×1080
5 fps
front-view camera
ego trajectory / camera pose
部分 Open subset 有文本描述
```

数据目标不是普通随机驾驶视频，而是特别强调：

- 完整 ego maneuvers；
- multi-agent interaction；
- open-world rare knowledge。

---

## 4.2 为什么对我们的 WAM 数据池重要

Drive-JEPA 原文明确写：

```text
CoVLA
+ DrivingDojo
+ OpenScene (trainval)
→ curated driving video dataset
→ V-JEPA driving-domain pretraining
```

Drive-JEPA 报告最终预训练规模约：

```text
330 h
```

处理成：

```text
front-view
8-frame clips
512×256
2 Hz
```

我们已经有 OpenScene；因此 CoVLA + DrivingDojo 是 Drive-JEPA 数据链的关键缺口。

**注意：Drive-JEPA 论文没有公开给出 DrivingDojo 的精确 shard 白名单。**

因此：

> 只下载 Main 283 GB 不能声称“具备完整 Drive-JEPA DrivingDojo source”。

为了公共研究数据池，下载全 45 shard 更稳妥。

---

## 4.3 官方 HF 分发

Main：

https://huggingface.co/datasets/Yuqi1997/DrivingDojo

Extra：

- https://huggingface.co/datasets/Yuqi1997/DrivingDojo-Extra1
- https://huggingface.co/datasets/Yuqi1997/DrivingDojo-Extra2
- https://huggingface.co/datasets/Yuqi1997/DrivingDojo-Extra3
- https://huggingface.co/datasets/Yuqi1997/DrivingDojo-Extra4
- https://huggingface.co/datasets/Yuqi1997/DrivingDojo-Extra5

官方/作者代码数据说明：

https://github.com/zyy721/Drivingdojo-occ/blob/main/docs/DATASET.md

其中明确说明：

```text
Due to size limitations, videos are split across multiple repositories.
Totally there are 45 tar.gz files, each containing about 400 videos.
```

---

## 4.4 当前 HF 体积

当前 HF 页面显示：

| Repo | 当前页面体积 |
|---|---:|
| Main | **283 GB** |
| Extra1 | **283 GB** |
| Extra2 | **291 GB** |
| Extra3 | **310 GB** |
| Extra4 | **291 GB** |
| Extra5 | 文件列表合计约 **231 GB** |
| **合计** | **约 1.689 TB** |

Main 额外包含：

```text
action_info.tar.gz   ~61.2 MB
camera_info.tar.gz   ~197 MB
meta.json            ~490 MB
```

Main `videos/` 当前可见：

```text
videos_1.tar.gz   35.7 GB
videos_2.tar.gz   38.0 GB
videos_3.tar.gz   33.4 GB
videos_4.tar.gz   33.6 GB
videos_5.tar.gz   35.8 GB
videos_6.tar.gz   33.7 GB
videos_7.tar.gz   35.8 GB
videos_8.tar.gz   35.8 GB
```

Extra5 当前公开文件列表包含：

```text
videos_35.zip
videos_40.tar.gz
...
videos_45.tar.gz
```

因此 **videos_35.zip 不是重复垃圾**；它补的是编号 35。

### 体积状态

HF 页面总体积是当前官方服务给出的信息，可视为：

```text
OFFICIAL-REPORTED
```

但真正开跑前仍应执行 `hf download --dry-run` 冻结当前 revision 和精确 Bytes。

---

## 4.5 Gate 与 license

这些 repo 是 gated：

> 需要登录 HF，并接受“分享联系信息”等访问条件后才能读取数据文件。

Main 页面 metadata：

```text
Apache-2.0
```

Extra1–Extra5 页面：

```text
CC-BY-NC-SA-4.0
```

因此内部 inventory **禁止把整个 DrivingDojo 粗暴标成统一 Apache-2.0**。

建议每 repo 单独保存：

```text
repo_id
revision
license_displayed
access_date
accepted_gate
```

---

## 4.6 Windows 下载

HF 官方当前推荐使用 `hf download` / Hugging Face Hub。

官方文档：

- https://huggingface.co/docs/huggingface_hub/guides/download
- https://huggingface.co/docs/hub/datasets-downloading

安装：

```powershell
py -m pip install -U huggingface_hub
hf auth login
```

建议设置独立缓存/下载盘：

```powershell
$env:HF_HOME="D:\wam_stage\hf_cache"
$env:HF_XET_HIGH_PERFORMANCE="1"
```

每个 repo 先：

```powershell
hf download Yuqi1997/DrivingDojo `
  --repo-type dataset `
  --dry-run
```

保存 stdout 到：

```text
manifests/DrivingDojo_Main_dryrun_YYYYMMDD.txt
```

正式：

```powershell
hf download Yuqi1997/DrivingDojo `
  --repo-type dataset `
  --local-dir "D:\wam_stage\DrivingDojo"
```

Extra1–Extra5 **一个 repo 一批**。

### 不建议

```text
一个巨大 git clone
```

作为 1.7 TB 长任务。

HF 官方 `local_dir` 会在目标目录建立 `.cache/huggingface/` metadata，从而避免重复下载已是最新版本的文件。

---

## 4.7 是否解包

HF 把数据标成 `webdataset`；45 个 `.tar.gz` 本身就是适合长期存放和流式训练的发布形式。

因此默认：

> **保留原 shard，不全量解包。**

只需要：

- `tar -tzf` 结构扫描；
- 少量视频抽检；
- 训练 pipeline 需要时直接读取 WebDataset 或按需生成 index/cache。

`videos_35.zip` 单独用 ZIP 工具检查。

---

# 5. CoVLA

## 5.1 官方事实

HF：

https://huggingface.co/datasets/turing-motors/CoVLA-Dataset

论文：

https://arxiv.org/abs/2408.10845

WACV 2025：

> CoVLA: Comprehensive Vision-Language-Action Dataset for Autonomous Driving

官方报告：

```text
>80 h
约 10,000 个真实驾驶 clips
视频 + vehicle state/CAN + trajectory + natural-language description
```

HF 当前：

```text
Total file size: 452 GB
```

状态：

```text
OFFICIAL-REPORTED / HF current
```

---

## 5.2 对 WAM 的价值

Drive-JEPA 直接将 CoVLA 纳入 driving video pretraining corpus。

它相比普通前视视频额外有：

- CAN / ego state；
- trajectory/action；
- language description。

所以它既可做 JEPA/video pretraining，也保留未来 VLA/action-conditioned world-model 的价值。

---

## 5.3 Gate / license

HF 页面显示：

- 数据访问需 gate / contact sharing；
- video clips 和 CAN data 受 **CoVLA-Dataset Licensing Terms and Conditions**；
- natural-language descriptions 受 VideoLLaMA 2 license；
- 论文明确数据以 academic purpose 发布。

因此：

1. 下载前必须人工接受当前页面条款；
2. 本地 Agent 不得把 CoVLA 重新公开分发；
3. inventory 保存 access date + revision + license snapshot。

---

## 5.4 Windows 下载

```powershell
hf auth login

hf download turing-motors/CoVLA-Dataset `
  --repo-type dataset `
  --dry-run

hf download turing-motors/CoVLA-Dataset `
  --repo-type dataset `
  --local-dir "D:\wam_stage\CoVLA-Dataset"
```

建议完整下载，不做 452 GB 以内的微型裁剪，因为附加 state/language metadata 相对视频成本低，未来研究价值高。

---

# 6. HUGSIM

## 6.1 官方事实

官方代码：

https://github.com/hyzhou404/HUGSIM

官方 HF：

https://huggingface.co/datasets/XDimLab/HUGSIM

论文：

https://arxiv.org/abs/2412.01718

HF 当前：

```text
60.7 GB
license: MIT
非 gated
```

主要内容：

```text
3DRealCar/
scenes/
nusc_map_cache.zip   ~198 MB
scenarios.zip
```

论文报告：

- 基于 KITTI-360、Waymo、nuScenes、PandaSet 等真实场景进行重建；
- 70+ sequences；
- 400+ scenarios；
- 目标是 real-time / photorealistic / closed-loop simulation。

---

## 6.2 为什么要单独下载

即使 210 已有 nuScenes，也**不等于已有 HUGSIM**。

HUGSIM 的价值是：

```text
raw source scene
→ 3D reconstructed assets
→ 可产生 novel-view / closed-loop observation
```

它是派生后的独立 simulator assets。

对于 TOAD / WA-JEPA / DrivoR 等路线和 future closed-loop 对照，非常值得。

---

## 6.3 Windows 下载

```powershell
hf download XDimLab/HUGSIM `
  --repo-type dataset `
  --dry-run

hf download XDimLab/HUGSIM `
  --repo-type dataset `
  --local-dir "D:\wam_stage\HUGSIM"
```

因为只有 60.7 GB，可以作为整个链路的第一个 HF smoke test。

---

# 7. OpenDV-mini

## 7.1 官方入口

官方代码：

https://github.com/OpenDriveLab/DriveAGI

OpenDV 目录：

https://github.com/OpenDriveLab/DriveAGI/tree/main/opendv

官方 README：

https://github.com/OpenDriveLab/DriveAGI/blob/main/opendv/README.md

---

## 7.2 官方规模

完整 OpenDV-YouTube：

```text
>1700 h
raw video: ~3 TB
processed images: ~24–25 TB
mostly 1080p
244+ cities / 40 countries（项目页描述）
```

OpenDV-mini：

详细 README 写：

```text
约 28 h total
25 h mini-train
3 h mini-val
raw ~44 GB
processed images ~390 GB
```

顶层项目 news 有时简写成 “25 hours mini”，应理解为 train 部分/简化宣传口径；**详细 opendv README 的 25h train + 3h val 更具体。**

---

## 7.3 本轮为什么只下 raw mini

OpenDV 是 Vista / PWM / CausalDrive 这条大规模 video world-model 路线的重要资源，但不是当前核心 12 中每篇都需要。

44 GB raw 足以验证：

- YouTube metadata pipeline；
- yt-dlp 稳定性；
- clip slicing；
- world-model data loader；
- 后续是否值得上 3 TB full。

暂时禁止：

```powershell
python scripts/video2img.py --mini
```

因为会从约 44 GB 膨胀到约 390 GB。

---

## 7.4 官方下载流程

官方要求：

1. 从官方 Google Sheet 导出：
   ```text
   OpenDV-YouTube.csv
   ```
2. 运行：
   ```bash
   python scripts/meta_preprocess.py -i CSV_PATH -o JSON_PATH
   ```
3. 配置：
   ```text
   opendv/configs/download.json
   ```
4. mini：
   ```bash
   python scripts/youtube_download.py --mini >> download_output.txt
   ```

当前官方 `configs/download.json` 已经使用：

```json
"method": "yt-dlp"
```

并选择 720–1080p 范围。

官方默认：

```text
num_workers = 90
```

我们不采用这个并发。

Windows 初始：

```text
num_workers = 8
```

稳定后最大建议先尝试：

```text
16
```

避免触发本地磁盘、网络、YouTube 限速/封禁问题。

---

## 7.5 社区下载风险

DriveAGI issue #9：

https://github.com/OpenDriveLab/DriveAGI/issues/9

已有用户报告旧 `youtube-dl`：

```text
Unable to extract uploader id
```

并提出使用 `yt-dlp`。

当前官方 config 已经转向 `yt-dlp`，说明这个问题已被工程上吸收。

但是 YouTube 下载仍天然有：

- 视频被删除/设为 private；
- 403；
- bot/rate-limit；
- 地区限制；
- cookie / JS player 变化。

yt-dlp 2026 仍有 YouTube 403 社区 issue，因此不能把失败 URL 全部判断成“本地配置坏”。

必须保留：

```text
download_output.txt
download_exceptions.txt
```

OpenDV 的验收不是“历史 URL 100% 成功”，而是：

```text
manifest frozen
+ success list
+ exception list
+ downloaded duration / file size check
```

---

# 8. CityWalker

官方 HF：

https://huggingface.co/datasets/ai4ce/CityWalker

当前：

```text
6.82 GB
obs/
pose_label.zip
```

论文入口由 HF dataset card 链到：

```text
arXiv 2411.17820
```

Metis 的城市机器人/urban navigation 分支使用 CityWalker。

它对 10 TB 预算几乎没有压力，所以建议顺手补齐。

Windows：

```powershell
hf download ai4ce/CityWalker `
  --repo-type dataset `
  --dry-run

hf download ai4ce/CityWalker `
  --repo-type dataset `
  --local-dir "D:\wam_stage\CityWalker"
```

**License 注意：dataset card 当前没有像 Main DrivingDojo 那样非常清晰地单列 data license。**
代码/模型 license 不能自动等价为 dataset license。

因此 inventory 标：

```text
data_license = CHECK_BEFORE_REDISTRIBUTION
```

但研究内部下载使用可按当前官方页面条款执行。

---

# 9. Adv-nuSc

官方 HF：

https://huggingface.co/datasets/Pixtella/Adv-nuSc

当前 HF：

```text
15.6 GB
CC-BY-SA-4.0
156 scenes
6,115 samples
6-camera rendered video
3D bounding boxes
```

其 foundation 是 nuScenes validation，但 adversarial trajectories + rendered videos 是新的派生资产，因此不是“已有 nuScenes 就等价拥有”。

GraphWorld robustness 支线会用到这类数据，因此成本很低、研究价值明确。

Windows：

```powershell
hf download Pixtella/Adv-nuSc `
  --repo-type dataset `
  --dry-run

hf download Pixtella/Adv-nuSc `
  --repo-type dataset `
  --local-dir "D:\wam_stage\Adv-nuSc"
```

---

# 10. Windows 下载工作根

建议统一：

```text
D:\wam_stage\
├── manifests\
├── logs\
├── nuplan\
├── DrivingDojo\
├── DrivingDojo-Extra1\
├── DrivingDojo-Extra2\
├── DrivingDojo-Extra3\
├── DrivingDojo-Extra4\
├── DrivingDojo-Extra5\
├── CoVLA-Dataset\
├── HUGSIM\
├── OpenDV-mini\
├── CityWalker\
├── Adv-nuSc\
└── hf_cache\
```

要求 Windows staging 盘：

- NTFS；
- 避免 FAT32；
- 预留单批至少 1 TB 空闲；
- 不把浏览器临时下载目录作为正式 staging。

---

# 11. Windows → 210 传输

## 11.1 首选：WSL + rsync over SSH

对于 TB 级多批次传输，比单纯 `scp` 更适合：

- 可增量；
- 可重跑；
- 已存在相同文件可跳过；
- 有成熟 partial transfer 支持。

rsync 官方：

https://rsync.samba.org/

当前官方 rsync 已到 3.5.0（2026-08 发布）。

Windows 侧推荐在 WSL 中访问：

```text
/mnt/d/wam_stage/
```

示意：

```bash
rsync -avhP --partial \
  /mnt/d/wam_stage/HUGSIM/ \
  USER@10.199.4.210:/mnt/nas/planning/zhouyangming/wam/staging/HUGSIM/
```

**不要无脑使用 `--append-verify` 作为所有文件的通用恢复参数。**
rsync 官方 man page明确说明 append/append-verify 是针对“已知为增长文件”的特殊模式，普通 immutable dataset archive 使用正常 partial/resume 语义更稳妥。

---

## 11.2 备选：Windows OpenSSH `scp` / `sftp`

Windows 10/11 自带/可选安装 OpenSSH Client，Microsoft 官方说明包含：

```text
ssh
sftp
scp
ssh-keygen
```

Microsoft 文档：

https://learn.microsoft.com/windows-server/administration/openssh/openssh-overview

示意：

```powershell
scp "D:\wam_stage\HUGSIM\*" `
  USER@10.199.4.210:/mnt/nas/planning/zhouyangming/wam/staging/HUGSIM/
```

但 TB 级长传输更推荐：

```text
rsync over SSH
```

因为目录级重跑和跳过已完成文件更方便。

---

# 12. 两阶段验收

## 12.1 Windows 下载后第一验收

每个文件记录：

```text
source
repo/object
revision / ETag
expected bytes
local bytes
local SHA256
download time
```

PowerShell SHA256：

```powershell
Get-FileHash "D:\wam_stage\...\file" -Algorithm SHA256
```

建议统一输出：

```text
manifest_local_sha256.csv
```

HF 文件：

- 以 `hf download --dry-run` 的 Bytes + revision 为下载前冻结基线；
- 下载后保存本地 SHA256。

nuPlan：

- 以 S3 `size_bytes` + ETag + Last-Modified 为 source manifest；
- **ETag 不默认当 MD5**，尤其 multipart object；
- 另外计算本地 SHA256。

---

## 12.2 传到 210 后第二验收

210 对每个文件再次：

```bash
stat -c '%s %n' FILE
sha256sum FILE
```

必须满足：

```text
local Windows SHA256 == 210 SHA256
```

然后 archive structure scan。

tar / tar.gz：

```bash
tar -tf FILE >/dev/null
```

ZIP：

```bash
unzip -t FILE
```

nuPlan `.zip`：

```bash
file FILE
bsdtar -tf FILE >/dev/null
```

**按实际 container 判断，不按扩展名判断。**

---

# 13. 210 staging 与正式目录

禁止 Windows 直接传到正式数据根。

先：

```text
/mnt/nas/planning/zhouyangming/wam/staging/<dataset>/
```

验收完整后再 promote 到：

```text
/mnt/nas/planning/zhouyangming/wam_datasets/<dataset>/
```

建议每个数据集正式根保留：

```text
SOURCE.md
MANIFEST.csv
CHECKSUMS.sha256
LICENSE_OR_TERMS.txt / URL
DOWNLOAD_LOG.txt
```

这样以后研究人员能知道：

- 来源；
- 下载日期；
- revision；
- 是否 gated；
- 当时体积；
- 本地是否被修改过。

---

# 14. 推荐执行顺序

## Batch 0 — 只读 manifest / gate

Windows 完成：

```text
HF 登录
DrivingDojo 6 repo gate
CoVLA gate
AWS CLI
Python
yt-dlp
WSL / rsync
SSH key
```

生成：

- nuPlan S3 object manifest；
- DrivingDojo 6× `hf download --dry-run`；
- CoVLA dry-run；
- HUGSIM dry-run；
- CityWalker dry-run；
- Adv-nuSc dry-run。

**Batch 0 不下载 TB 级 payload。**

---

## Batch 1 — 小数据 + 传输链 smoke

```text
HUGSIM       60.7 GB
CityWalker    6.82 GB
Adv-nuSc     15.6 GB
```

合计约：

```text
83 GB
```

目标：

验证：

```text
Windows download
→ SHA256
→ SSH/rsync
→ 210 SHA256
→ archive scan
→ formal promote
```

整条链。

---

## Batch 2 — OpenDV-mini

```text
~44 GB raw
```

重点不是体积，而是验证：

- YouTube availability；
- yt-dlp；
- exception ledger；
- duration consistency。

不做 frame extraction。

---

## Batch 3 — CoVLA

```text
452 GB
```

单 repo 完整处理。

---

## Batch 4 — DrivingDojo

顺序：

```text
Main
Extra1
Extra2
Extra3
Extra4
Extra5
```

约：

```text
1.689 TB
```

每 repo：

```text
dry-run frozen
→ download
→ SHA256
→ transfer
→ 210 verify
→ promote
```

不要一次把六 repo 混成一个不可恢复任务。

---

## Batch 5 — nuPlan DB

以精确 S3 manifest 为准。

先 DB 而不是 camera，原因：

- 对象较少；
- 容易验证 AWS 路线；
- DB/log 层以后 ReactSim / scenario mining / raw sensor 对齐都有价值。

---

## Batch 6+ — nuPlan camera

由 `size_bytes` 自动组批：

```text
目标 400–700 GB / batch
硬上限 800 GB / batch
```

每批：

```text
AWS download on Windows
→ size + local SHA256
→ file/container smoke
→ rsync/scp to 210 staging
→ remote size + SHA256
→ bsdtar structure scan
→ promote raw archive
→ 清理 Windows batch
→ next
```

Windows staging 不要求同时容纳全部 5–6 TB。

---

# 15. 10 TB 硬门限

本地 Agent 在 Batch 0 完成后重新计算：

```text
TOTAL_PLANNED_BYTES =
nuPlan exact target objects
+ HF dry-run DrivingDojo exact bytes
+ HF CoVLA exact bytes
+ HF HUGSIM exact bytes
+ OpenDV-mini planning bytes
+ CityWalker
+ Adv-nuSc
```

门限：

```text
TOTAL_PLANNED_BYTES <= 9.0 TB
    → 可按当前方案继续，保留 ≥1 TB 缓冲

9.0 TB < TOTAL_PLANNED_BYTES <= 10 TB
    → 必须减少 eager extraction / cache，下载 payload 可继续但需要重新算峰值

TOTAL_PLANNED_BYTES > 10 TB
    → 停止，重新审批；优先裁 nuPlan 非必要相机或延期部分数据
```

这里使用十进制：

```text
1 TB = 1,000,000,000,000 B
```

同时 inventory 可额外显示 TiB，但决策口径不要混。

---

# 16. 本地 Agent 的最低交付物

在真正开始大下载前，本地 Agent 应产生以下文件：

```text
download_control/
├── 00_ENV_CHECK.md
├── 01_SOURCE_REGISTRY.csv
├── 02_LICENSE_GATE_LEDGER.csv
├── 03_NUPLAN_S3_MANIFEST.csv
├── 04_HF_DRYRUN_MANIFEST.csv
├── 05_DOWNLOAD_BATCH_PLAN.csv
├── 06_SPACE_BUDGET.md
├── 07_TRANSFER_PLAN.md
└── 08_ACCEPTANCE_PROTOCOL.md
```

`05_DOWNLOAD_BATCH_PLAN.csv` 至少：

```text
batch_id
dataset
source_type
source_object
expected_bytes
windows_path
remote_staging_path
remote_formal_path
download_tool
download_status
local_sha256
transfer_status
remote_sha256
archive_scan
promote_status
notes
```

---

# 17. 当前推荐最终结论

在“新增 10 TB 以内可接受”的前提下，本轮数据建设不应再走极端保守路线。

建议正式准备：

```text
raw nuPlan
  ├─ train DB ×9
  ├─ val DB
  ├─ test DB
  └─ train camera ×43
     （LiDAR / val camera 不下）

DrivingDojo
  ├─ Main
  └─ Extra1–5
     → 45 video shards + metadata

CoVLA
  → full HF release

HUGSIM
  → full HF release

OpenDV-mini
  → raw video only

CityWalker
  → full HF release

Adv-nuSc
  → full HF release
```

按当前预算：

```text
约 8.5 TB 新下载
```

但其中 raw nuPlan 的 camera 仍是：

```text
PENDING-MANIFEST
```

因此本地 Agent 的第一任务不是启动 6 TB 下载，而是：

> **在 Windows 上把 nuPlan S3 54 个目标对象的当前精确 byte、DrivingDojo 六 repo 当前 dry-run byte、CoVLA/HUGSIM revision 全部冻结，再自动生成不超过 10 TB 的最终批次计划。**

---

# 18. 官方 / 论文 / 社区来源索引

## nuPlan

官方：

- AWS Open Data Registry  
  https://registry.opendata.aws/motional-nuplan/
- Motional nuPlan devkit  
  https://github.com/motional/nuplan-devkit
- Dataset setup  
  https://github.com/motional/nuplan-devkit/blob/master/docs/dataset_setup.md
- nuPlan download  
  https://www.nuscenes.org/nuplan#download

论文/实际 WAM 使用：

- Epona data preparation  
  https://github.com/Kevin-thu/Epona/blob/main/data_preparation/README.md
- Epona repo  
  https://github.com/Kevin-thu/Epona

社区/坑：

- nuPlan sensor zip cannot be unzipped, issue #334  
  https://github.com/motional/nuplan-devkit/issues/334

本仓库：

```text
datasets/NUPLAN_210_INVENTORY_2026-09-19.md
datasets/NUPLAN_DOWNLOAD_DECISION.md
datasets/NUPLAN_DATASET_AUDIT.md
scripts/datasets/nuplan_public_manifest.py
scripts/datasets/nuplan_archive_head_probe.py
```

---

## DrivingDojo

官方：

- Project  
  https://drivingdojo.github.io/
- Paper  
  https://arxiv.org/abs/2410.10738
- Code  
  https://github.com/Robertwyq/Drivingdojo
- Main HF  
  https://huggingface.co/datasets/Yuqi1997/DrivingDojo
- Extra1  
  https://huggingface.co/datasets/Yuqi1997/DrivingDojo-Extra1
- Extra2  
  https://huggingface.co/datasets/Yuqi1997/DrivingDojo-Extra2
- Extra3  
  https://huggingface.co/datasets/Yuqi1997/DrivingDojo-Extra3
- Extra4  
  https://huggingface.co/datasets/Yuqi1997/DrivingDojo-Extra4
- Extra5  
  https://huggingface.co/datasets/Yuqi1997/DrivingDojo-Extra5

作者相关数据准备说明：

- https://github.com/zyy721/Drivingdojo-occ/blob/main/docs/DATASET.md

---

## CoVLA

- HF  
  https://huggingface.co/datasets/turing-motors/CoVLA-Dataset
- Paper  
  https://arxiv.org/abs/2408.10845

---

## HUGSIM

- Code  
  https://github.com/hyzhou404/HUGSIM
- HF  
  https://huggingface.co/datasets/XDimLab/HUGSIM
- Paper  
  https://arxiv.org/abs/2412.01718

---

## OpenDV

- DriveAGI  
  https://github.com/OpenDriveLab/DriveAGI
- OpenDV instructions  
  https://github.com/OpenDriveLab/DriveAGI/blob/main/opendv/README.md
- OpenDV directory  
  https://github.com/OpenDriveLab/DriveAGI/tree/main/opendv
- Historical/community download issue  
  https://github.com/OpenDriveLab/DriveAGI/issues/9

---

## CityWalker

- Dataset  
  https://huggingface.co/datasets/ai4ce/CityWalker
- Paper ID  
  arXiv:2411.17820

---

## Adv-nuSc

- Dataset  
  https://huggingface.co/datasets/Pixtella/Adv-nuSc

---

## 下载/传输工具官方文档

Hugging Face：

- Download from Hub  
  https://huggingface.co/docs/huggingface_hub/guides/download
- Dataset downloading  
  https://huggingface.co/docs/hub/datasets-downloading

AWS：

- `aws s3 cp`  
  https://docs.aws.amazon.com/cli/latest/reference/s3/cp.html
- `aws s3 sync`  
  https://docs.aws.amazon.com/cli/latest/reference/s3/sync.html

Windows OpenSSH：

- https://learn.microsoft.com/windows-server/administration/openssh/openssh-overview

rsync：

- https://rsync.samba.org/
- https://download.samba.org/pub/rsync/rsync.1

---

# 19. 不确定项清单（必须保留，不允许 Agent 自行脑补）

1. **nuPlan 43 个 train camera 当前精确总字节**：尚未冻结，必须当前 S3 manifest。
2. **nuPlan train/val/test DB 当前精确总字节**：必须同 manifest 冻结；历史约 1.1 TB 只作预算。
3. **nuPlan 四路 F0/L0/R0/B0 解包后真实长期占用**：未知，必须至少对首批 archive 统计 member bytes。
4. **Drive-JEPA 实际从 DrivingDojo 45 shards 中用了哪些具体 clips/shards**：论文未发布精确 shard whitelist；因此公共数据池按全量 DrivingDojo 获取。
5. **OpenDV-mini 当前可成功下载比例**：受 YouTube 视频存活、地区限制、403 等影响；只能运行时得到。
6. **CityWalker dataset-specific redistribution terms**：当前 HF 页面未给出像 CoVLA/DrivingDojo 那样非常清晰的独立数据 license 字段；内部研究使用与再分发必须分开处理。

---

**本文件原则：所有 TB 级任务必须先 manifest，再下载；所有 Windows 下载必须先 staging，再 SSH；所有 210 数据必须先 staging 验收，再进入 formal root。**
