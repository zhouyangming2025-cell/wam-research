# nuPlan 数据集与 WAM 使用方式审计留痕

> 日期：2026-09-19  
> 目的：建立 nuPlan / OpenScene / NAVSIM 的统一数据口径，并核对 WAM 论文实际使用的数据资产，避免将“nuPlan 母数据”“OpenScene 派生传感器”“NAVSIM benchmark/split”混为一谈。  
> 证据优先级：① 本仓库论文原文 `papers/raw_md`；② 官方 nuPlan / OpenScene / NAVSIM 文档与 devkit；③ 公开代码仓库；④ 社区工具统计。  
> 重要原则：凡是官方网页未公开精确字节数的数据，不将社区估算写成“官方大小”。

---

## 0. 结论先行

### 0.1 最重要的三个概念

**nuPlan、OpenScene、NAVSIM 不是三个彼此独立的数据集。**

更准确的数据血缘关系是：

```text
nuPlan
├─ 约 1200 h 的规划/轨迹数据库（全量日志层）
│  ├─ ego pose / vehicle state
│  ├─ agent tracks / 3D boxes
│  ├─ traffic light / scenario / route / map relation
│  └─ HD maps
│
└─ 其中约 120 h 公开 raw sensors（高频传感器层）
   ├─ 8 cameras，原始约 10 Hz
   ├─ 5 LiDAR，原始约 20 Hz
   ├─ IMU
   └─ GPS
        │
        │ OpenScene 重新组织 + 下采样到 2 Hz
        ▼
OpenScene
├─ metadata / annotations
├─ 8-camera images，2 Hz
├─ merged LiDAR，2 Hz
└─ occupancy / flow 等附加标注
        │
        │ NAVSIM 场景筛选 + split + simulator/metric
        ▼
NAVSIM
├─ navtrain / navtest / navmini / navhard ...
├─ PDMS / EPDMS
└─ non-reactive / pseudo-closed-loop planning evaluation
```

因此，“论文使用了 nuPlan”必须继续追问：

1. 是直接读取原始 nuPlan DB？
2. 是直接读取原始 nuPlan 10 Hz camera？
3. 是读取 OpenScene 的 2 Hz camera/LiDAR？
4. 只是使用 nuPlan map？
5. 还是只在 NAVSIM 的 split/evaluator 上训练评测？

这五种情况的存储需求完全不同。

### 0.2 对当前数据下载决策的核心结论

- **OpenScene/NAVSIM 路线**已经覆盖大量当前 WAM：WoTE、World4Drive、LAW(NAVSIM部分)、Drive-JEPA、SeerDrive、Metis、DynFlowDrive、GraphWorld 等。对于这些工作，**不需要为了复现论文而补齐原始 nuPlan 10 Hz camera**。
- **直接 nuPlan 高时频视频预训练路线**也真实存在，并且越来越重要：Epona、DriveLaW、WorldDrive、Discrete-WAM 等明确在原始/高频 nuPlan training data 上做 world-model 或 world-policy pretraining。
- 因此，“WAM 只需要 OpenScene”也是错误的；是否需要原始 nuPlan camera，要由目标论文决定。
- 原始 nuPlan `train + val` DB 的公开第三方统计约 **1037.72 GB（十进制）≈ 1.04 TB ≈ 0.944 TiB**。这是 NVLabs `trajdata` 的公开统计，不应标成 Motional 官方静态 catalog。
- OpenScene v1.1 官方明确列出 `trainval camera = 1.1 TB`、`trainval LiDAR = 822 GB`、`metadata = 6.6 GB`。
- **原始 Motional nuPlan trainval camera 的精确总字节数，本次仍未找到公开官方静态表可确认。** 因此正式预算仍应写作：
  `原始 nuPlan trainval DB ≈ 1.04 TB（第三方公开统计） + 原始 camera X（待官方对象清单确认）`。
- OpenScene 文档明确说明：完整 nuPlan sensor data **over 20 TB**，而 OpenScene 只是对 nuPlan sensors 进行下采样以改善可访问性。因此 OpenScene 的 `1.1 TB camera` 不能拿来代表原始 nuPlan camera。

---

# 1. nuPlan 到底是什么

## 1.1 数据集定位

nuPlan 最初就是为 **motion planning / ML planning** 而设计，而不是以 perception benchmark 为第一目标。

本仓库原论文：

`papers/raw_md/P0031_nuPlan/P0031_nuPlan.raw.md`

原始 2021 论文给出的目标口径是：

- 计划发布 **1500 h** 人类驾驶；
- Boston / Pittsburgh / Las Vegas / Singapore 四城；
- 全数据提供 autolabeled agent trajectories；
- camera、LiDAR、localization、steering 等 sensor data 只公开一个子集；
- 原始采集总体量级被描述为 **200+ TB**。

注意：这是**论文发布前/早期规划口径**，不能直接等同于最终公开数据。

当前 nuPlan 官方网页的实际发布口径则是：

- **1200 h** driving data；
- 4 cities；
- **120 h sensor data**；
- 5×LiDAR、8×camera、IMU、GPS；
- 5B autolabeled 3D boxes；
- HD maps；
- open-loop + closed-loop planning simulation。

因此必须保留两个时间口径：

| 口径 | 驾驶时长 | sensor 描述 | 含义 |
|---|---:|---|---|
| 2021 nuPlan 论文 | 1500 h（planned） | subset；全原始规模 200+ TB | 早期计划/论文描述 |
| 当前官方公开版本 | 1200 h | 120 h raw sensors | 实际公开版本应采用的主口径 |

后续工程预算应以**当前官方公开版本**为准。

---

# 2. nuPlan 数据的两层结构

理解 nuPlan 最关键的一点是：

> **SQLite `.db` 和 camera/LiDAR 文件不是同一个东西。**

## 2.1 Database / metadata / planning layer

nuPlan devkit schema 表明数据库包含或索引：

- `log`
- `ego_pose`
- camera calibration
- LiDAR calibration
- `image` metadata
- `lidar_pc` metadata
- tracked objects / categories
- scenes
- scenario / route / map relation
- vehicle state
- traffic-light related信息等

其中 `image` 表保存的是**图像索引与元数据**，包括图像文件路径、时间戳、ego pose、camera token 等，**不存 JPEG 图像本体**。

同理，LiDAR 数据库表保存点云文件的索引/元信息，并不是点云 blob 本体。

典型结构：

```text
nuplan/
├─ maps/
│
└─ nuplan-v1.1/
   ├─ splits/
   │  ├─ mini/
   │  │  └─ *.db
   │  ├─ trainval/
   │  │  └─ *.db
   │  └─ test/
   │     └─ *.db
   │
   └─ sensor_blobs/
      └─ <log>/
         ├─ CAM_F0/
         ├─ CAM_B0/
         ├─ CAM_L0/
         ├─ CAM_L1/
         ├─ CAM_L2/
         ├─ CAM_R0/
         ├─ CAM_R1/
         ├─ CAM_R2/
         └─ MergedPointCloud/
```

所以：

```text
*.db ≠ images
*.db ≠ point clouds
```

DB 可以非常大，因为它承载了大规模全量日志里的轨迹和自动标注，但仍不等于 raw sensor blobs。

## 2.2 Raw sensor layer

当前官方口径：

- 8 cameras
- 5 LiDAR
- IMU
- GPS
- 公开 sensor data 时长约 120 h

公开资料与后续论文一致表明：

- 原始 camera 典型频率：**10 Hz**
- LiDAR：**20 Hz**
- OpenScene 后续将关键传感器数据降至 **2 Hz**

这正是“原始 nuPlan sensor >20 TB”与“OpenScene 约 2 TB”之间数量级差异的主要来源之一。

---

# 3. nuPlan DB 大小：目前能证明到什么程度

NVLabs `trajdata` 对其支持的 nuPlan 数据给出：

| split | 公开统计大小 |
|---|---:|
| Train | 947.42 GB |
| Validation | 90.30 GB |
| Test | 89.33 GB |
| Mini | 7.96 GB |

因此：

```text
Train + Val
= 947.42 + 90.30
= 1037.72 GB
≈ 1.038 TB (decimal)
≈ 0.944 TiB
```

如果再加 Test：

```text
Train + Val + Test
= 1127.05 GB
≈ 1.127 TB
```

### 证据等级

这是一项**可信的社区/开源工具统计**，不是 Motional 当前公开下载网页提供的静态官方 size catalog。

因此推荐正式写法：

> nuPlan v1.1 train+val DB 按公开工具统计约 1.04 TB；最终下载预算应以官方 S3 对象实际 Content-Length 汇总为准。

不要写：

> “nuPlan 官方确认 trainval DB = 1.04 TB”。

---

# 4. 原始 camera / LiDAR：目前为什么不能给出精确总量

## 4.1 已经可以确认

OpenScene 官方明确写：

> 如果已经拥有完整 nuPlan sensor data（**over 20TB**），可直接链接到 OpenScene；OpenScene 对 nuPlan sensor data 做了 downsampling。

NAVSIM 原论文也写：

> OpenScene 将 nuPlan sensor 数据降至 2 Hz，并把存储从 **over 20 TB** 降到约 **2 TB**。

因此：

```text
原始 nuPlan sensor ≫ OpenScene sensor
```

且：

```text
OpenScene 1.1 TB camera
≠ 原始 nuPlan camera
```

## 4.2 本次仍无法公开确认的数

没有找到 Motional 官方公开静态网页列出：

```text
nuPlan train camera shard 0 = ?
...
nuPlan train camera shard N = ?
nuPlan val camera shard 0 = ?
...
camera total = ?
```

NuPlanQA 等项目只能确认官方页面确实按 camera 分片发布，例如其研究使用：

- `nuPlan Train Camera 32–42`
- `nuPlan Val Camera 0–1`

但这些说明并没有给出所有原始 camera shard 的总字节数。

因此当前最严谨的写法仍是：

```text
原始 nuPlan trainval DB ≈ 1.04 TB
+
原始 nuPlan trainval camera = X（未由公开官方 catalog 定死）
```

### 要彻底定死 X 的方法

只接受下面两种办法作为最终工程证据：

1. 已登录 Motional 下载页，导出全部 camera shard 的 `Size`；
2. 对 AWS Open Data bucket / CloudFront 对象逐项列举并汇总 `Content-Length`。

AWS Registry 已确认公开 bucket：

```text
s3://motional-nuplan/
region: ap-northeast-1
```

并允许：

```bash
aws s3 ls --no-sign-request s3://motional-nuplan/
```

因此最终最可靠的方法是直接做 S3 manifest，而不是继续从网页二手估算。

---

# 5. OpenScene 到底做了什么

OpenScene 不是一个与 nuPlan 无关的新采集数据集，它是一个以 nuPlan 为基础的**紧凑再分发/派生版本**。

OpenScene 官方 v1.1 文档明确：

- based on nuPlan；
- folder structure 与 nuPlan 对齐；
- sensor data 是从 nuPlan 下采样得到；
- 完整 trainval + test sensors 约 2 TB；
- 如果已经拥有原始 nuPlan `over 20TB` sensor，可链接复用。

## 5.1 OpenScene v1.1 官方大小

| subset | metadata | camera | LiDAR |
|---|---:|---:|---:|
| mini | 509.6 MB | 84 GB | 60 GB |
| trainval | **6.6 GB** | **1.1 TB** | **822 GB** |
| test | 454 MB | **120 GB** | **87 GB** |

因此：

```text
OpenScene trainval camera + metadata
≈ 1.1066 TB
```

如果包含 LiDAR：

```text
≈ 1.9286 TB
```

这里只是按官网标称下载包大小做预算加和，不宣称精确字节值。

## 5.2 下采样意味着什么

NAVSIM 原论文写得非常明确：

```text
nuPlan high-frequency sensors
        ↓
OpenScene 2 Hz
120 h
```

因此“120 h 没变”不表示所有原始 frame 都保留。

例如 camera：

```text
原始 10 Hz：
0.0, 0.1, 0.2, 0.3, 0.4, 0.5, ...

OpenScene 2 Hz：
0.0,                0.5, ...
```

本质上保留的是**时间覆盖范围**，不是**原始时间分辨率**。

这就是：

> “OpenScene 仍然覆盖约 120 h，但数据已经不完整地保留原始逐帧信息。”

---

# 6. NAVSIM 和 OpenScene 的关系

NAVSIM 是：

> **benchmark / scenario curation / simulator / metrics + 基于 OpenScene 的标准化数据 split。**

NAVSIM 论文：

`papers/raw_md/P0032_NAVSIM/P0032_NAVSIM.raw.md`

其原文明确：

- 选择 OpenScene 作为数据基础；
- OpenScene 是 nuPlan redistribution；
- 120 h；
- 2 Hz；
- 8 cameras，1920×1080；
- 5 个 LiDAR 融合后的 merged point cloud；
- 当前 frame + 最多 3 个过去 frames，总历史窗口 1.5 s；
- 对 OpenScene 进一步筛选困难场景；
- 获得 100k+ challenging scenarios。

所以 NAVSIM 并不是把 raw nuPlan 重新完整复制一份，而是：

```text
OpenScene 2 Hz sensor
+
nuPlan/OpenScene annotations
+
nuPlan map
+
scenario filtering
+
planning evaluator
```

## 6.1 为什么 navtrain 不是 1192 个训练样本

这是一个很常见的误读。

很多论文写：

```text
1192 training scenarios
136 testing scenarios
```

同时另一些论文写：

```text
navtrain ≈ 103k scenes/keyframes
navtest ≈ 12k scenes
```

这两个数字指向不同层级：

- `1192 / 136`：更接近 source logs / scenario groups 的计数口径；
- `103k / 12k`：具体可用于训练/测试的 sampled planning scenes / keyframes。

Drive-JEPA 原文明确写：

- navtrain：**103k**
- navtest：**12k**

Discrete-WAM 也明确写 navtest 约 12k、2 Hz。

因此以后文档中不要把：

> 1192 scenarios = 1192 training samples

二者混为一谈。

---

# 7. nuPlan 与 NAVSIM 的“闭环”也不能混用

nuPlan 原生提供真正的 planning simulator，并支持：

- open-loop
- closed-loop non-reactive
- closed-loop reactive

NAVSIM v1 的核心设计却是：

> 用真实 sensor input，但不重新渲染 ego 偏离记录轨迹后的新视觉；在短时 BEV abstraction 中 unroll candidate trajectory，并用 simulation-based metrics 打分。

因此 NAVSIM v1 常被论文口语化叫“closed-loop metric”，但更严谨地说：

- 它比 L2 imitation 更接近闭环安全指标；
- 但环境不响应 ego action；
- 原论文自己定义为 **non-reactive simulation**。

不能把 NAVSIM v1 当 CARLA/reactive nuPlan 那种完整交互式闭环。

NAVSIM v2 则进一步引入 reactive traffic / pseudo-closed-loop 等扩展，应与 v1 分开记录。

---

# 8. WAM 论文到底怎么使用 nuPlan：逐篇原文审计

以下结论优先来自本仓库 `papers/raw_md` 的论文原文，而不是只看 README。

---

## 8.1 Epona — 直接 nuPlan video 路线

来源：

`papers/raw_md/P0001_Epona/P0001_Epona.raw.md`

原文关键证据：

- 模型 **from scratch** 训练；
- 使用公开 **NuPlan videos**；
- 同时使用 nuScenes 700 scenes；
- image resize 512×1024；
- nuPlan test 使用 1628 video clips 做视频生成评测；
- 生成时以 10 个连续过去 frames 为条件；
- NAVSIM planning 用过去 2s observations 预测未来 4s trajectory。

**结论：**

```text
Epona WM pretrain:
direct nuPlan videos

Epona planning evaluation:
NAVSIM
```

所以完整复现 Epona world model，OpenScene 2 Hz 不应默认视为与原 nuPlan video recipe 等价。

---

## 8.2 DriveLaW — nuPlan + nuScenes 8 Hz video pretraining → NAVSIM planner

来源：

`papers/raw_md/P0009_DriveLaW/P0009_DriveLaW.raw.md`

原文关键证据：

- Video DiT 在 **nuScenes + NuPlan 的 8 Hz frames** 上预训练；
- 先 low-resolution long-duration clips，再 high-resolution shorter clips；
- video generation 在 nuScenes 评测；
- trajectory planning 在 NAVSIM 评测；
- NAVSIM planning 是后续 action fine-tuning。

**结论：**

```text
DriveLaW-Video:
nuPlan + nuScenes @ 8 Hz

DriveLaW-Act:
NAVSIM
```

这是一条非常典型的：

```text
高频大规模 driving video pretraining
→ NAVSIM planning adaptation
```

路线。

---

## 8.3 WorldDrive — 直接 nuPlan 10 Hz，数据依赖最明确之一

来源：

`papers/raw_md/P0042_WorldDrive/P0042_WorldDrive.raw.md`

论文正文：

- Phase 1：TA-DWM 使用 **nuPlan + nuScenes driving videos**
- Phase 2：freeze encoders，在 **NAVSIM navtrain** 训练 planner。

补充材料进一步明确：

### Stage 1 — nuPlan

- nuPlan training dataset；
- **200k iterations**
- resolution：**256×512**
- **8 historical frames**
- **17 future frames**
- **10 Hz video clips**

### Stage 2 — nuScenes

- 100k iterations；
- 同 resolution / frame rate。

之后才进入 NAVSIM planner training。

**结论：**

这是目前最强的“原始高频 nuPlan video 对 WAM 有直接复现价值”的论文证据之一。

```text
nuPlan 10Hz:
8 history → 17 future
        ↓
TA-DWM
        ↓
nuScenes finetune
        ↓
NAVSIM planner
```

如果目标是完整复现 WorldDrive pretraining，OpenScene 2 Hz 无法按原配置直接替代。

---

## 8.4 Discrete-WAM — full nuPlan pretraining → NAVSIM SFT/RL

来源：

`papers/raw_md/P0064_Discrete-WAM/P0064_Discrete-WAM.raw.md`

原文：

- unified world-policy pretraining：
  **full nuPlan training set**
- 200k steps；
- 然后：
  - navtrain SFT 10 epochs；
  - navtrain RL post-training 2 epochs；
- NAVSIM v1/v2 navtest；
- navtest 约 12k scenes，2 Hz；
- 模型视觉输入包括 side/front views。

**结论：**

```text
full nuPlan
→ unified world-policy pretraining
→ NAVSIM navtrain SFT
→ NAVSIM navtrain RL
→ navtest
```

这说明原始 nuPlan 对新一代 unified world-policy WAM 并非“历史包袱”，而是大规模预训练资产。

---

## 8.5 WoTE — NAVSIM/OpenScene + nuPlan simulator，不是原始 camera 路线

来源：

`papers/raw_md/P0045_WoTE/P0045_WoTE.raw.md`

原文明确解释：

- OpenScene 将 nuPlan 从 10 Hz 下采样到 2 Hz；
- 形成 120 h driving logs；
- NAVSIM 再从 OpenScene 重采样困难场景；
- navtrain/navtest；
- input：
  - front + cropped front-left + front-right
  - stitched 256×1024
  - 64m×64m LiDAR
- Navtrain 50 epochs；
- BEV world model future states at t+2s / t+4s；
- nuPlan simulator 用于生成 trajectory-conditioned BEV semantic maps/rewards。

这里有一个必须区分的点：

> WoTE “使用 nuPlan simulator”不等于“训练输入需要原始 nuPlan camera”。

**结论：**

主要数据路线是：

```text
OpenScene/NAVSIM sensor
+
nuPlan simulator-generated BEV supervision
```

---

## 8.6 World4Drive — NAVSIM/OpenScene 路线

来源：

`papers/raw_md/P0046_World4Drive/P0046_World4Drive.raw.md`

原文：

- NAVSIM built upon OpenScene；
- >100k keyframes；
- 1192 training scenario groups / 136 test scenario groups；
- 4s horizon，2 Hz；
- input 是 front/front-left/front-right stitching；
- resize 256×1024；
- NAVSIM model train 60 epochs。

**结论：**

NAVSIM 部分不需要原始 nuPlan 10 Hz sensor。

---

## 8.7 LAW — nuScenes + NAVSIM/OpenScene，不做原始 nuPlan video pretrain

来源：

`papers/raw_md/P0048_LAW/P0048_LAW.raw.md`

原文：

- nuScenes benchmark；
- NAVSIM benchmark；
- NAVSIM built on OpenScene；
- OpenScene 提供从 nuPlan condensed 的 120 h logs；
- NAVSIM input resize 640×320，ResNet34，20 epochs。

**结论：**

LAW 在 NAVSIM 上使用的是 OpenScene/NAVSIM 路线，不能因为论文引用了 nuPlan，就写成“LAW 需要原始 nuPlan”。

---

## 8.8 Drive-JEPA — OpenScene 本身就是视频预训练数据之一

来源：

`papers/raw_md/P0049_DriveJEPA/P0049_DriveJEPA.raw.md`

原文：

- 大规模 driving-video corpus 来自：
  - CoVLA
  - DrivingDojo
  - **OpenScene trainval**
- 都使用 front-view camera；
- NAVSIM v1：
  - navtrain ≈ 103k scenes
  - navtest ≈ 12k scenes。

**结论：**

Drive-JEPA 的公开 recipe 直接证明：

> 2 Hz OpenScene camera 本身也可以作为 driving video representation pretraining 数据，并非所有 video pretraining 都必须回到 raw nuPlan 10 Hz。

---

## 8.9 SeerDrive — NAVSIM/OpenScene

来源：

`papers/raw_md/P0061_SeerDrive/P0061_SeerDrive.raw.md`

原文：

- NAVSIM built upon nuPlan；
- 1192 train/val + 136 test scenario groups；
- 8-camera + LiDAR，2 Hz；
- 模型实际 NAVSIM input：
  - images + LiDAR
  - 3 camera views
  - 1024×256。

**结论：**

OpenScene/NAVSIM 路线。

---

## 8.10 Metis — NAVSIM-v2，front-camera-only

来源：

`papers/raw_md/P0062_Metis/P0062_Metis.raw.md`

原文：

- train on navtrain；
- navtrain：1192 source scenario groups；
- navtest：12,146 scenarios；
- navhard：244 real safety-critical + 4,164 3DGS synthetic counterparts；
- only **front-facing camera**；
- input resolution **640×768**；
- action horizon 8 = 4 s，0.5 s interval；
- NAVSIM-v2 train 60 epochs。

**结论：**

不需要原始完整 8-camera nuPlan；论文公开训练直接基于 NAVSIM-v2。

---

## 8.11 DynFlowDrive — NAVSIM/OpenScene

来源：

`papers/raw_md/P0063_DynFlowDrive/P0063_DynFlowDrive.raw.md`

原文：

- NavSim built on OpenScene；
- 103K keyframes；
- 1192 train scenario groups +136 test groups；
- trajectory 2 Hz / 4 s；
- front + left/right crop stitched 256×1024；
- LiDAR 64m×64m；
- train 30 epochs。

**结论：**

OpenScene/NAVSIM。

---

## 8.12 GraphWorld — NAVSIM/OpenScene

来源：

`papers/raw_md/P0065_GraphWorld/P0065_GraphWorld.raw.md`

原文：

- NAVSIMv1 built upon OpenScene；
- OpenScene 是 compact redistribution of nuPlan；
- 8 cameras 360°；
- merged LiDAR from 5 sensors；
- annotations 2 Hz；
- HD maps + boxes；
- official Navtrain split training；
- ResNet34 / TransFuser setup。

**结论：**

NAVSIM/OpenScene。

---

## 8.13 DriveWorld（早期 4D representation pretraining）— OpenScene 路线

来源：

`papers/raw_md/P0047_DriveWorld/P0047_DriveWorld.raw.md`

注意与 **WorldDrive** 名称容易混淆。

DriveWorld 原文：

- pretrain on nuScenes + **OpenScene**
- multi-camera videos
- 3D occupancy labels from LiDAR + pose
- fine-tune on nuScenes

**结论：**

这是 OpenScene pretraining，不是 raw nuPlan pretraining。

---

# 9. WAM 数据路线总表

| 方法 | 原始/高频 nuPlan | OpenScene/NAVSIM | 关键数据用法 | 对原始 nuPlan sensor 的依赖 |
|---|---|---|---|---|
| Epona | **是** | 是 | nuPlan videos + nuScenes WM；NAVSIM planning | **高** |
| DriveLaW | **是，8 Hz** | 是 | nuPlan+nuScenes video pretrain → NAVSIM Act | **高** |
| WorldDrive | **是，10 Hz** | 是 | nuPlan 8 hist→17 future WM → NAVSIM planner | **高** |
| Discrete-WAM | **是，full train** | 是 | nuPlan world-policy pretrain → NAVSIM SFT/RL | **高** |
| WoTE | 否（raw sensor） | **是** | OpenScene/NAVSIM input；nuPlan simulator给BEV/reward | 低 |
| World4Drive | 否 | **是** | NAVSIM/OpenScene 2 Hz | 低 |
| LAW | 否（NAVSIM部分） | **是** | NAVSIM/OpenScene + nuScenes | 低 |
| Drive-JEPA | 否 | **是** | OpenScene trainval 也是 video pretrain corpus | 低 |
| SeerDrive | 否 | **是** | NAVSIM 3 cams + LiDAR | 低 |
| Metis | 否 | **是** | NAVSIM-v2 front camera only | 低 |
| DynFlowDrive | 否 | **是** | NAVSIM 3-view stitched + LiDAR | 低 |
| GraphWorld | 否 | **是** | NAVSIM/OpenScene 2 Hz | 低 |
| DriveWorld | 否 | **OpenScene** | OpenScene 4D pretrain | 低 |

这里的“低”不是说完全与 nuPlan 无关，而是：

> **不需要单独拥有原始 nuPlan 高频 sensor_blobs 即可遵循论文所述的公开训练路线。**

---

# 10. WAM 为什么会形成两条数据路线

## 路线 A：高频 raw nuPlan 做 world model pretraining

典型：

```text
Epona
DriveLaW
WorldDrive
Discrete-WAM
```

特点：

- 更长 driving-video corpus；
- 8–10 Hz 时序；
- world dynamics / video dynamics pretraining；
- 之后迁移到 NAVSIM planning；
- 更像“大规模预训练 → 下游规划对齐”。

这类研究的需求是：

```text
高时间分辨率
连续视频
ego motion/action
大量 driving hours
```

因此 raw nuPlan 的高频 camera 很有价值。

## 路线 B：直接 OpenScene/NAVSIM

典型：

```text
WoTE
World4Drive
LAW
Drive-JEPA
SeerDrive
Metis
DynFlowDrive
GraphWorld
```

特点：

- 2 Hz；
- 标准 navtrain/navtest；
- 训练成本更低；
- 直接针对 planning；
- 很多模型只吃 1–3 个 camera；
- 有些需要 LiDAR，有些纯 camera。

这类研究没有必要为了“nuPlan 名字”去补完整原始 camera。

---

# 11. 对当前数据资产的工程含义

如果机器上已经有较完整 OpenScene：

## 11.1 已覆盖的大类

通常已经能够支持或接近支持：

- NAVSIM v1/v2 planning
- WoTE
- World4Drive
- LAW NAVSIM
- Drive-JEPA 的 OpenScene 部分
- SeerDrive
- Metis
- DynFlowDrive
- GraphWorld
- 多数 TransFuser/NAVSIM baseline

前提还要确认：

```text
metadata
camera
LiDAR（对需要 LiDAR 的论文）
nuPlan maps
navsim split/cache
```

是否完整。

## 11.2 仍值得补的资产

### A. 原始 nuPlan train/val DB

预算：

```text
≈ 1.04 TB
```

用途：

- 完整日志索引；
- high-frequency ego/agent trajectories；
- scenario mining；
- 原始 sensor 时间对齐；
- 自定义 nuPlan planning；
- Epona/WorldDrive/Discrete-WAM 等原始 nuPlan pipeline 数据准备。

这个资产与 OpenScene metadata 不等价。

### B. 原始 nuPlan camera

只有在明确开展：

- Epona full pretraining
- DriveLaW Video pretraining
- WorldDrive TA-DWM pretraining
- Discrete-WAM full nuPlan world-policy pretraining
- 自研高频 world model

时，再优先补。

不应因为“做 WAM”三个字就无条件下载全部 >20TB sensors。

---

# 12. 推荐的数据资产分层

建议以后 210 上按资产语义而不是论文名组织认知：

```text
DATA/
├─ nuplan/
│  ├─ maps/
│  ├─ db/
│  │  ├─ train/
│  │  ├─ val/
│  │  └─ test/
│  └─ raw_sensor/
│     ├─ camera_10hz/
│     └─ lidar_20hz/
│
├─ openscene/
│  ├─ metadata/
│  ├─ camera_2hz/
│  ├─ lidar_2hz/
│  └─ occupancy/
│
└─ navsim/
   ├─ splits/
   ├─ metric_cache/
   ├─ trajectory_cache/
   └─ benchmark_configs/
```

即使物理目录不做迁移，也应在资产账本里按照这个逻辑登记。

---

# 13. 正式容量口径表

| 资产 | 当前建议口径 | 证据等级 | 备注 |
|---|---:|---|---|
| nuPlan current public driving logs | 1200 h | 官方 | 四城 |
| nuPlan raw sensor coverage | 120 h | 官方 | 约10% |
| nuPlan original total sensor | >20 TB | OpenScene/NAVSIM官方项目 | 公开文档量级 |
| nuPlan Train DB | 947.42 GB | 第三方公开工具 | NVLabs trajdata |
| nuPlan Val DB | 90.30 GB | 第三方公开工具 | 同上 |
| nuPlan Train+Val DB | **1037.72 GB ≈1.04 TB** | 计算 | 非Motional静态catalog |
| nuPlan Test DB | 89.33 GB | 第三方公开工具 | 同上 |
| raw nuPlan trainval camera | **未知 X** | 未闭合 | 需S3 manifest |
| OpenScene v1.1 trainval metadata | 6.6 GB | 官方 OpenScene | |
| OpenScene v1.1 trainval camera | **1.1 TB** | 官方 OpenScene | 2 Hz派生 |
| OpenScene v1.1 trainval LiDAR | **822 GB** | 官方 OpenScene | 2 Hz派生 |
| OpenScene v1.1 test camera | 120 GB | 官方 OpenScene | |
| OpenScene v1.1 test LiDAR | 87 GB | 官方 OpenScene | |

---

# 14. 目前仍未闭合的问题

## Q1. 原始 nuPlan trainval camera 到底多少 TB？

**未闭合。**

公开网页能确认 shards 存在，却没有找到官方静态 size table。

下一步应生成：

```text
object_key,size_bytes,etag,last_modified
```

的 S3 manifest，再分类汇总：

```text
train_camera
val_camera
train_lidar
val_lidar
DB
maps
```

这是唯一值得作为“最终容量真值”留档的办法。

## Q2. Epona / Discrete-WAM 所谓 full nuPlan 是否需要全部 8 路 camera？

论文仅凭一句 `full nuPlan training set` 还不足以推出“8 路全部 camera 都必须下载”。

例如 Epona 规划结果明确是 front-camera-only；不同代码的数据预处理可能只抽特定 camera channel。

因此：

> “需要 raw nuPlan”与“需要 raw nuPlan 的全部 sensor”不是同一结论。

真正制定下载队列前，应继续对这些项目的 dataloader/config 做代码级审计。

## Q3. 原始 sensor >20TB 中 camera 与 LiDAR 各占多少？

本次公开官方资料仍不能可靠拆分。

不能通过 OpenScene camera:LiDAR 比例反推原始数据，因为编码格式、采样频率、压缩方式不同。

---

# 15. 推荐后续下载决策

### P0 — 先核对现有 OpenScene 完整性

应核验：

- trainval metadata
- trainval camera
- trainval LiDAR
- test
- nuPlan maps
- NAVSIM split/cache

如果完整，当前主流 NAVSIM WAM 已有较好的数据基础。

### P1 — 补 nuPlan DB

目标：

```text
train + val ≈ 1.04 TB
```

价值高、容量明确、可支撑日志/trajectory/scenario/sensor alignment。

### P2 — 在选定目标论文后再补原始 camera

优先候选：

1. WorldDrive
2. DriveLaW
3. Epona
4. Discrete-WAM

先对代码确认具体 camera channel / sampling / log subset，再下载相应 shards。

### P3 — 暂不做“全量 raw sensor >20TB”式盲下

除非研究目标明确需要：

- 原始 10Hz multi-camera
- 原始 20Hz LiDAR
- 自己重建 OpenScene-like preprocessing
- 多传感器 foundation pretraining

否则投入产出比偏低。

---

# 16. 以后论文审计必须新增的数据字段

以后项目中的论文数据集记录，建议禁止只写：

```text
Dataset: nuPlan / NAVSIM
```

至少记录：

| 字段 | 示例 |
|---|---|
| mother dataset | nuPlan |
| actual distribution | OpenScene v1.1 |
| benchmark | NAVSIM v1 |
| split | navtrain |
| camera source | OpenScene sensor_blobs |
| camera views | F0 + cropped L/R |
| input resolution | 256×1024 |
| sampling rate | 2 Hz |
| history | current + 3 past |
| future horizon | 4 s |
| LiDAR | yes/no |
| nuPlan DB directly used | yes/no |
| raw nuPlan sensor directly used | yes/no |
| nuPlan map | yes/no |
| simulator | NAVSIM / nuPlan |
| purpose | pretrain / SFT / RL / eval |

这能彻底避免“同一篇论文被一句 dataset=nuPlan 误导”的问题。

---

# 17. 证据来源

## 17.1 本仓库论文原文

仓库：

https://github.com/zhouyangming2025-cell/wam-research

重点：

- `papers/raw_md/P0031_nuPlan/P0031_nuPlan.raw.md`
- `papers/raw_md/P0032_NAVSIM/P0032_NAVSIM.raw.md`
- `papers/raw_md/P0001_Epona/P0001_Epona.raw.md`
- `papers/raw_md/P0009_DriveLaW/P0009_DriveLaW.raw.md`
- `papers/raw_md/P0042_WorldDrive/P0042_WorldDrive.raw.md`
- `papers/raw_md/P0045_WoTE/P0045_WoTE.raw.md`
- `papers/raw_md/P0046_World4Drive/P0046_World4Drive.raw.md`
- `papers/raw_md/P0047_DriveWorld/P0047_DriveWorld.raw.md`
- `papers/raw_md/P0048_LAW/P0048_LAW.raw.md`
- `papers/raw_md/P0049_DriveJEPA/P0049_DriveJEPA.raw.md`
- `papers/raw_md/P0061_SeerDrive/P0061_SeerDrive.raw.md`
- `papers/raw_md/P0062_Metis/P0062_Metis.raw.md`
- `papers/raw_md/P0063_DynFlowDrive/P0063_DynFlowDrive.raw.md`
- `papers/raw_md/P0064_Discrete-WAM/P0064_Discrete-WAM.raw.md`
- `papers/raw_md/P0065_GraphWorld/P0065_GraphWorld.raw.md`

## 17.2 nuPlan 官方与 devkit

nuPlan official:
https://www.nuscenes.org/nuplan

AWS Registry of Open Data:
https://registry.opendata.aws/motional-nuplan/

nuPlan devkit:
https://github.com/motional/nuplan-devkit

Database schema:
https://github.com/motional/nuplan-devkit/blob/master/docs/nuplan_schema.md

Dataset setup:
https://github.com/motional/nuplan-devkit/blob/master/docs/dataset_setup.md

## 17.3 OpenScene

OpenScene:
https://github.com/OpenDriveLab/OpenScene

Getting Started / size table:
https://github.com/OpenDriveLab/OpenScene/blob/main/docs/getting_started.md

## 17.4 NAVSIM

NAVSIM:
https://github.com/autonomousvision/navsim

NAVSIM paper:
https://arxiv.org/abs/2406.15349

## 17.5 DB 大小的第三方统计

NVLabs trajdata:
https://github.com/NVlabs/trajdata

## 17.6 camera shard 存在性的旁证

NuPlanQA:
https://github.com/sungyeonparkk/NuPlanQA

其 README 明确要求下载官方：
`Train Camera 32–42`、`Val Camera 0–1`，
但未给出原始 camera 全部分片的总字节数。

---

# 18. 最终固定口径

以后项目中涉及 nuPlan 容量时，建议统一使用下面这段：

> **nuPlan 当前公开版本包含约 1200 h 驾驶日志，其中约 120 h 提供 raw sensor。完整 raw sensor 数据公开资料显示超过 20 TB。nuPlan 的规划 DB 与 raw sensor blobs 是两类独立资产：公开第三方工具统计 train+val DB 约 1.04 TB，而原始 Motional trainval camera 的精确总字节数目前没有从公开官方静态 catalog 中确认。OpenScene 是 nuPlan 120 h sensor 的 2 Hz 紧凑再分发版本，官方 v1.1 trainval camera 为 1.1 TB、LiDAR 822 GB、metadata 6.6 GB；该 1.1 TB 不应被当作原始 nuPlan camera 大小。NAVSIM 在 OpenScene 之上进一步定义困难场景 split、planning simulator 与 PDMS/EPDMS 评测协议。WAM 文献同时存在两类路线：Epona、DriveLaW、WorldDrive、Discrete-WAM 等直接使用高频/full nuPlan 做 world-model/world-policy pretraining；WoTE、World4Drive、LAW、Drive-JEPA、SeerDrive、Metis、DynFlowDrive、GraphWorld 等则主要使用 OpenScene/NAVSIM。是否需要下载原始 nuPlan sensor，必须按目标论文的数据读取代码决定，不能仅凭论文写有“nuPlan”或“NAVSIM”判断。**

---

## 19. 下一项应做的审计

在生成正式原始 camera 下载队列以前，应继续执行：

```text
Epona
DriveLaW
WorldDrive
Discrete-WAM
```

四个项目的 dataloader/config 级审计，逐个确认：

- 使用几个 cameras；
- camera channel 名称；
- 是否真的读取 10 Hz 全帧；
- 是否自行抽成 8 Hz / 其他频率；
- 是否使用 train 全量 logs；
- 是否依赖 LiDAR；
- 是否依赖原始 DB；
- 可以最小化下载到哪些 official shards。

完成这一层后，才能从“数据集理解”进入“精确下载 manifest”。
