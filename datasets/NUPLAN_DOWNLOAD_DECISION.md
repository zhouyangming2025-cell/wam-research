# nuPlan / OpenScene / NAVSIM 下载决策：WAM 代码级审计

> 状态：2026-09-19  
> 目标：把 `datasets/NUPLAN_DATASET_AUDIT.md` 的数据集认知进一步落到“现在究竟应该下载什么、暂时不要下载什么”。  
> 原则：**论文写了 nuPlan，不等于需要完整 raw nuPlan；README 写了 download all splits，也不等于模型实际读取全部传感器。以 dataloader / preprocessing / config 为最高工程证据。**

---

## 0. 当前结论

### 0.1 现在不批准的下载

在当前证据下，**不建议立刻启动以下大规模下载**：

- 完整 raw nuPlan camera；
- 完整 raw nuPlan LiDAR；
- 约 1.04 TB 的 nuPlan train+val DB；
- 为了 NAVSIM 再重复下载一份完整 OpenScene trainval。

原因不是这些资产“没用”，而是目前主线 WAM 复现并不要求它们全部存在，而且 3 个最重要的高频 nuPlan 工作中有 2 个公开训练链路并不足以支撑 exact-from-scratch reproduction。

### 0.2 当前真正应该做的事情

按优先级：

1. **核对 210 现有 OpenScene / NAVSIM 是否完整**；
2. 缺什么就只补什么；
3. 优先使用论文作者公开的 world-model / planner checkpoints；
4. 如果确定要从零重训高频 nuPlan world model，**Epona 是第一优先候选**；
5. 在下载 raw nuPlan 前先生成官方 S3 object manifest，得到精确大小；
6. 同时评估 123D 的 10 Hz nuPlan 派生版本作为“研究型高频数据源”，但不把它当 exact paper reproduction 的等价物。

当前默认策略因此从：

```text
先下载 nuPlan DB → 再考虑 camera
```

修正为：

```text
先确认 OpenScene/NAVSIM 已有资产
→ 用公开 checkpoint 推进 WAM
→ 明确需要从零高频预训练时
→ 再按模型实际输入最小化 raw nuPlan 下载
```

---

# 1. 四篇高优先级论文：代码级结论

## 1.1 Epona：唯一目前值得优先保留“raw nuPlan from-scratch”路线的项目

官方仓库：

`Kevin-thu/Epona`

关键文件：

- `data_preparation/create_nuplan_json.py`
- `dataset/dataset_nuplan.py`
- `configs/dit_config_dcae_nuplan.py`

### README 怎么写

README 要求：

> download all the splits in NuPlan

并展示完整 8-camera + merged LiDAR 目录结构。

**但模型代码实际并不读取全部这些传感器。**

### 数据准备脚本实际做什么

`create_nuplan_json.py` 扫描 DB 时确实定义了：

- CAM_F0
- CAM_B0
- CAM_L0/L1/L2
- CAM_R0/R1/R2

但最终写入训练 sequence meta 的只有：

```python
new_seq_meta = {
    'CAM_F0': cameras['CAM_F0'][i]['seq'],
    'scene': cameras['CAM_F0'][i]['scene'],
    'data_root': cameras['data_root'],
    'pose': ...
}
```

### Dataset 实际读什么

`dataset/dataset_nuplan.py`：

```python
rgb_front_dir = f"{seq_root}/CAM_F0"
```

训练图像只来自 **CAM_F0**。

LiDAR 没有进入 Epona 的 NuPlan training sample。

### 实际频率

代码明确：

```python
self.ori_fps = 10
self.downsample = self.ori_fps // downsample_fps
```

配置：

```python
downsample_fps = 5
condition_frames = 10
image_size = (512, 1024)
```

因此公开代码的 Epona NuPlan recipe 是：

```text
raw nuPlan CAM_F0 @ 10 Hz
          ↓
代码下采样
          ↓
CAM_F0 @ 5 Hz
          ↓
10 history frames + next-frame / autoregressive training
```

### Epona 对下载策略的意义

**模型级最小需求：**

- train/val 中有 sensor 的相关 DB/log metadata；
- CAM_F0；
- camera/ego pose 对齐信息；
- 不需要其他 7 路 camera；
- 不需要 LiDAR。

但注意：

**官方 Motional 下载页面把 camera 按 train/val camera archive 分片，而不是按 CAM_F0 单独打包。**

所以：

- “模型只需要 CAM_F0”
- 与
- “官方 ZIP 下载能否只取 CAM_F0”

是两个不同问题。

在拿到 S3 object manifest 前，不能把模型级节省量直接等同为官方下载量节省。

### 当前决策

| 目标 | 是否需要 raw nuPlan |
|---|---|
| 阅读/分析 Epona | 否 |
| 使用公开 checkpoint | 否 |
| 只跑自定义 demo | 否，可自己准备 front video + pose |
| exact NuPlan video benchmark | 需要对应 NuPlan CAM_F0 test sensor |
| 从零重训 Epona | **需要，且目前四篇中最值得优先支持** |

---

## 1.2 DriveLaW：论文明确 8 Hz nuPlan，但公开 raw→video 数据链不完整

官方仓库：

`xiaomi-research/drivelaw`

论文明确：

- DriveLaW-Video 在 nuPlan + nuScenes 上预训练；
- driving video 使用 **8 Hz**；
- 两阶段视频 curriculum：
  - low-res long clip；
  - high-res shorter clip；
- planning 后续在 NAVSIM。

### 公开代码目前能确认什么

`DriveLaW-Video/Train/docs/Data-preparation.md` 仍然写：

> download all the splits in NuPlan

但真正的训练 preprocessing 接受的是：

```text
CSV / JSON / JSONL
  ├─ media_path -> 已组织好的 video
  └─ caption
```

`preprocess_dataset.py` 负责：

- 读 video；
- 转 VAE latent；
- 转 caption embedding。

**官方仓库没有发布从原始 NuPlan DB + sensor_blobs 直接构造论文 8 Hz video corpus 的 NuPlan-specific converter。**

代码搜索也没有发现 Epona 那样的 `NuPlanDBWrapper` preprocessing 链路。

### 这意味着什么

论文的数据条件是真实存在的：

```text
nuPlan / nuScenes @ 8 Hz
→ DriveLaW-Video pretraining
```

但目前公开代码不足以从 Motional 原始文件一键重建作者训练集。

与此同时，官方已经发布：

- DriveLaW-Video 权重；
- DriveLaW-Act 权重；
- NAVSIM planning 代码。

### 当前决策

**不为了 DriveLaW 立即下载 raw nuPlan。**

当前最合理路线：

```text
released DriveLaW-Video weights
+
OpenScene/NAVSIM
→ planning / representation / downstream research
```

只有当研究目标明确变成：

> 重做 DriveLaW 的 8 Hz driving-video pretraining

时，再反向构建 NuPlan video preprocessing pipeline。

---

## 1.3 WorldDrive：论文 raw nuPlan pretrain 很明确，但公开仓库没有对应 NuPlan dataloader

官方仓库：

`TabGuigui/WorldDrive`

论文 / supplement 报告的 Stage 1：

```text
nuPlan training
200k iterations
10 Hz
8 history frames
→ 17 future frames
256×512
```

随后 nuScenes，再迁移到 NAVSIM planner。

这是强有力的“高频 nuPlan 对 WAM 有价值”的论文证据。

### 但当前公开代码发生了什么

`docs/Train_Eval.md` 明确把：

> Stage 1: Trajectory-aware Driving World Model pretrain

标记为：

> **Optional**

并建议直接下载作者发布的：

> pretrained WM checkpoint training on nuPlan

当前 `ta_dwm/dataset/create_dataset.py` 实际实现的 dataset branch 只有：

```python
if data_name == "navsim":
    ...
```

没有可用的：

```python
if data_name == "nuplan":
```

raw NuPlan dataloader。

当前 NAVSIM TA-DWM dataset 则明确只读：

```python
f0 = cameras.cam_f0.image
```

也就是 OpenScene/NAVSIM 的 CAM_F0。

### 代码与 paper config 还存在版本痕迹

当前 config 中出现：

- `train_data_list=['nuplan']`
- `downsample_fps=2`
- `condition_frames=4`
- `predict_frames=9`

但 dataset factory 并没有 NuPlan branch。

因此这套公开代码不能被当作论文 Stage-1 raw NuPlan training 的完整可复现实现。

### 当前决策

为了 WorldDrive：

**当前不下载 raw nuPlan。**

优先：

```text
作者发布的 TA-DWM checkpoint
+
现有 OpenScene/NAVSIM
→ planner
→ FAR
→ 研究与复现
```

只有在明确决定重建其缺失的 raw NuPlan training pipeline 时，才重新评估 raw data。

---

## 1.4 Discrete-WAM：论文说明 full nuPlan，但传感器配置没有公开到可批准下载的程度

本仓库原论文：

`papers/raw_md/P0064_Discrete-WAM/P0064_Discrete-WAM.raw.md`

明确：

```text
full nuPlan training set
→ unified world-policy pretraining
→ 200k steps
→ navtrain SFT
→ navtrain RL
```

### Camera 证据并不完全一致

Vision Tokenization 一节明确写：

> VQ-VAE tokenizer encodes **front-view camera images**

但其 attention analysis 又明确展示：

- left-view
- front-view
- right-view

三路 camera。

因此我们可以确认：

> 模型体系中存在多视角视觉输入。

但不能仅凭论文确定：

- full nuPlan pretraining 到底是 CAM_F0 only；
- 还是 L/F/R 三路；
- 各阶段是否使用不同 camera 配置；
- 原始 nuPlan 频率如何重采样。

截至本次审计，没有找到可用于验证这些细节的官方公开训练代码。

### 当前决策

**不因为一句 “full nuPlan training set” 启动 raw nuPlan 下载。**

Discrete-WAM 当前应标记为：

```text
论文价值：高
raw nuPlan 需求：真实
可执行数据 recipe：未闭合
下载状态：DEFER
```

---


## 1.5 ReWorld：进一步支持“先用 checkpoint，不为论文名盲下 raw data”

DriveLaW 团队在 2026-08 开源的 ReWorld 同样报告了基于 driving videos 的 world-model representation learning，并在统一实验里使用 nuPlan + nuScenes。

但当前公开 Stage-1 数据入口仍然是通用的：

```yaml
video_root: /path/to/training/videos
total_source_frames: 33
condition_source_frames: 9
video_width: 1024
video_height: 512
```

`OnlineVideoFolderDataset` 直接递归读取 mp4/webm/avi/mkv，并没有公开 raw NuPlan DB + sensor_blobs → training clips 的 NuPlan-specific converter。

同时作者已发布 ReWorld 权重。

因此 ReWorld 不改变当前下载结论：

- 它再次证明 high-frequency driving video 对 WAM 有研究价值；
- 但它没有提供足以要求我们现在下载完整 raw nuPlan 的公开转换链；
- 对当前研究推进，应先用 released weights + OpenScene/NAVSIM；
- 如果未来构建自研 driving-video corpus，再把 raw NuPlan / 123D 作为候选数据源。

---

# 2. 四篇论文的最终下载判定

| 方法 | raw nuPlan 对论文是否有用 | 公开代码能否闭合 raw 数据链 | 当前是否为它下载 raw |
|---|---:|---:|---:|
| **Epona** | 是 | **基本能** | **条件性 YES，第一候选** |
| DriveLaW | 是 | 不完整 | NO / defer |
| WorldDrive | 是 | 当前公开 repo 不完整 | NO / use checkpoint |
| Discrete-WAM | 是 | 未找到公开代码闭环 | NO / defer |

因此：

> **如果我们未来真的要下载第一批 raw nuPlan，不应面向“四篇一起用”的模糊目标，而应该以 Epona 的 CAM_F0 pipeline 作为第一个明确目标。**

---

# 3. NAVSIM / OpenScene：现在真正的主力资产

NAVSIM 官方当前 split 文档给出：

| 资产 | Logs | Sensors |
|---|---:|---:|
| OpenScene trainval | 14 GB | >2000 GB |
| OpenScene test | 1 GB | 217 GB |
| OpenScene mini | 1 GB | 151 GB |
| **NAVSIM navtrain** | 14 GB | **445 GB（含历史）** |
| NAVSIM navtrain without history | 同 logs | **300 GB** |
| navtest | 983 MB | 223 GB |
| navhard_two_stage | 892 MB | 31 GB |

官方特别说明：

> 如果已经有完整 trainval sensor data，则**不需要再次下载 navtrain sensor frames**。

这对当前 210 很重要。

> **工程风险提示：** NAVSIM 官方提供的 navtrain-only sensor 包是节省存储的正式路线，但公开 issue 中已有用户报告：即使下载包 MD5 全部通过，按 navtrain scene filter 加载时仍出现大量历史 sensor frame 缺失。该报告不能证明官方包普遍损坏，但在我们已经拥有约 2.8T OpenScene 的前提下，没有理由为了节省空间主动删除完整 trainval、退回精简 navtrain。现有完整数据应优先保留。

已知现场：

```text
OpenScene formal root ≈ 2.8T
```

从容量上看，它很可能已经覆盖完整或接近完整：

- trainval；
- test；
- metadata；
- 其他 NAVSIM assets。

但“2.8T”本身不能证明目录完整。

### 因此当前第一动作不是下载，而是 inventory

核对至少：

```text
OpenScene metadata trainval
OpenScene sensor_blobs trainval
OpenScene metadata test
OpenScene sensor_blobs test
nuPlan maps
NAVSIM v1 split/filter
NAVSIM v2 navhard_two_stage（若做 v2）
metric / trajectory caches（可重建，不属于原始数据）
```

仓库脚本：

`scripts/datasets/audit_dataset_roots.sh`

用于做这一轮盘点。

---

# 4. 对 nuPlan DB 的新判断：不再默认优先下载 1.04 TB

上一阶段我们曾把：

```text
nuPlan train+val DB ≈ 1.04 TB
```

视作“下一项明确值得补的资产”。

经过代码审计后，这个结论需要继续收紧。

### 对当前 NAVSIM WAM

以下工作并不需要这套 raw nuPlan trainval DB 才能按公开 recipe 训练：

- WoTE
- World4Drive
- LAW
- Drive-JEPA
- SeerDrive
- Metis
- DynFlowDrive
- GraphWorld
- WorldDrive planner stage
- DriveLaW-Act

它们走 OpenScene/NAVSIM。

### 对高频 pretrain WAM

raw DB 有用，但：

- Epona from-scratch：有明确用途；
- DriveLaW：公开 raw preprocessing 未闭合；
- WorldDrive：公开 raw dataloader 缺失；
- Discrete-WAM：公开 recipe 未闭合。

因此：

> **1.04 TB DB 是“条件资产”，不是当前 P1 必下资产。**

新的下载优先级应该是：

```text
P0 核实现有 OpenScene
P1 补 OpenScene/NAVSIM 真正缺失部分
P2 保证论文 checkpoint / model assets
P3 明确要 Epona from-scratch 时，再补 raw NuPlan DB + camera
```

---

# 5. Official Motional archive：模型最小需求 ≠ ZIP 最小下载

公开 NuPlan-Download-CLI 反映了官方归档方式：

### Train sensors

- camera archives：43 个，编号 0–42
- LiDAR archives：43 个

### Validation sensors

- camera archives：12 个
- LiDAR archives：12 个

### Test sensors

- camera archives：12 个
- LiDAR archives：12 个

### Train DB

9 个 package：

- Boston
- Pittsburgh
- Singapore
- Vegas 1–6

另有：

- val DB archive
- test DB archive
- map archive。

这些 camera archive 是：

```text
train_camera_0.zip
...
train_camera_42.zip
```

而不是：

```text
CAM_F0.zip
CAM_L0.zip
...
```

因此即使 Epona 模型只读 CAM_F0，若使用官方 archive 下载方式，仍可能被迫下载一个 archive 中的其他 camera 数据。

### 所以 raw download 前必须过一个 gate

先生成官方 S3 object manifest：

```text
object_key
size_bytes
last_modified
```

再判断 bucket 是否允许直接按对象路径：

```text
.../CAM_F0/...
```

选择性抓取。

仓库提供：

`scripts/datasets/nuplan_public_manifest.py`

它不依赖 AWS CLI，用 Python 标准库直接尝试列 public S3 bucket。

如果 210 外网策略阻断 S3，则在能访问 AWS 的机器运行；manifest 本身很小，生成后可以带回 210。

---

# 6. 新发现：123D 可能是“高频研究数据”的更合理中间层

2026 年发布的 **123D** 已经把 nuPlan v1.1 转成统一 Apache Arrow 数据。

其当前 Hugging Face 数据卡给出的 nuPlan 版本：

- 15910 logs；
- 1457 sensor logs；
- 14453 sensorless logs；
- 所有 modality 总体约 **7.8 TiB / 8.55 TB**；
- metadata 在 **10 Hz sync clock**；
- camera 仍为 native resolution；
- camera 图像重新编码成 JPEG quality 75；
- 每个 camera 每个 log 是独立 Arrow 文件，例如：

```text
camera.pcam_f0.arrow
camera.pcam_l0.arrow
camera.pcam_r0.arrow
...
```

这和 Motional 官方 archive 有一个非常重要的差异：

> **123D 是按 modality 文件组织，因此天然可以只下载 front camera。**

Hugging Face CLI 还支持 `--include` 与 `--dry-run`。

因此可以在真正下载前先算：

```bash
hf download kesai-labs/nuplan \
  --repo-type dataset \
  --include "logs/nuplan_train/*/camera.pcam_f0.arrow" \
  --dry-run
```

用同样方法估算：

```text
ego_state_se3.arrow
sync.arrow
route_position.arrow
```

的大小。

### 123D 不能直接替代官方 raw nuPlan 的地方

它不是 bit-exact raw data：

- images 被 JPEG quality 75 重编码；
- 目录/API 已变成 Arrow；
- 原论文 dataloader 不能直接读取；
- exact reproduction 需要额外 adapter；
- LiDAR 也被转换为 LAZ。

所以：

| 目标 | 123D 是否合适 |
|---|---|
| exact Epona paper reproduction | 不作为首选 |
| exact DriveLaW raw preprocessing | 不作为首选 |
| 自研 10 Hz/5 Hz front-camera WAM | **很有吸引力** |
| 大规模高频 world-model pretraining | **值得评估** |
| 只想减少 storage / 按相机下载 | **优势明显** |
| 当前 NAVSIM planning | 没必要，OpenScene 更直接 |

### 123D 当前定位

**研究替代方案，不是论文复现替代方案。**

在 raw Motional 下载前，强烈建议先用 HF `--dry-run` 算出：

```text
NuPlan 123D:
CAM_F0 train sensor logs
+
ego state
+
sync
+
必要 metadata
= ? TB
```

如果这个量显著低于官方 camera archives，并且我们的目标是自研 WAM 而不是 exact reproduction，它可能比下载 >20 TB raw sensor 更合理。

---

# 7. 当前“三类下载清单”

## A. 必须保有 / 缺失就补

### OpenScene / NAVSIM

- OpenScene trainval logs / metadata
- OpenScene trainval sensors：**已有完整 trainval 时不重复下 navtrain**
- OpenScene test / navtest 所需数据
- nuPlan maps
- NAVSIM v2 navhard_two_stage（仅当做 v2）
- 对应 benchmark split/config

### 模型资产

优先使用官方已发布：

- Epona checkpoint
- DriveLaW-Video / DriveLaW-Act weights
- WorldDrive TA-DWM / planner checkpoint

这能把大量 raw-data 下载从“前置条件”变成“以后想重训时再决定”。

---

## B. 条件性下载

### nuPlan raw DB

只有当：

- Epona from-scratch；
- 自研原始 nuPlan scenario mining；
- 需要原始高频 sensor↔ego/agent metadata 对齐；
- 重建缺失的 high-frequency pretrain pipeline；

再下。

### nuPlan raw camera

第一个合理目标：

```text
Epona → CAM_F0
```

不是：

```text
8 cameras + LiDAR 全量
```

但要先确认 S3 object-level 是否能真正做到 channel-selective 下载。

---

## C. 暂时不下载

- raw nuPlan LiDAR：当前四个高频 WAM 没有形成必须下载理由；
- DriveLaW 专用 raw corpus：公开 raw preprocessing 不闭合；
- WorldDrive raw pretraining corpus：公开 dataloader 不闭合，已有 checkpoint；
- Discrete-WAM raw corpus：没有足够公开实现证据确认 sensor recipe；
- 重复的 NAVSIM navtrain sensor：已有完整 OpenScene trainval 时不需要。

---

# 8. 下一次“允许 raw 下载”的审批条件

只有同时满足下面四条，才建议正式启动 raw nuPlan 大规模下载：

1. **目标模型明确**  
   例如 Epona，而不是泛泛“WAM”。

2. **输入通道明确**  
   CAM_F0 / L0 / R0 / LiDAR 等已经从代码确认。

3. **采样频率明确**  
   例如 Epona raw 10 Hz → training 5 Hz。

4. **下载粒度和大小明确**  
   已生成 S3 / HF manifest，知道实际将传输多少 TB。

如果四条中有任意一条未知：

> **不启动 TB 级下载。**

---

# 9. 目前最合理的总体路线

```text
210 当前 OpenScene ≈ 2.8T
        │
        ▼
[1] 盘点完整性
        │
        ├─ 完整 → 不重复下载
        │
        └─ 缺失 → 只补对应 split
        │
        ▼
[2] NAVSIM/WAM 主线
    使用现有 OpenScene + 作者 checkpoint
        │
        ▼
[3] 需要 high-frequency world model 吗？
        │
        ├─ 否 → raw nuPlan = 不下载
        │
        └─ 是
            │
            ▼
       首先选择 Epona / 自研目标
            │
            ├─ exact reproduction
            │   → official Motional manifest
            │   → DB + 必要 camera archives/objects
            │
            └─ research pretraining
                → 先 dry-run 123D CAM_F0-only
                → 比较 storage / adaptation cost
```

---

# 10. 当前结论一句话

> **我们现在已经不缺“一个叫 nuPlan 的 20TB 数据集”；我们缺的是对目标 WAM 真正有用的那一小部分高频数据。短期主线应继续使用现有 OpenScene/NAVSIM 和作者 checkpoints，不批准全量 raw nuPlan 下载；若未来进入高频 world-model 从零预训练，首先围绕 Epona 的 CAM_F0 需求做官方 S3 manifest 和 123D front-only dry-run，再决定最终 Y TB。**
