# WAM 数据集缺口：官方下载调研与 210 下载计划（2026-09-21）

## 0. 结论先行

本文件基于：

- `audits/datasets/wam_field_dataset_census_20260921.md`：65 个论文条目的 source-first 数据使用底账；
- `datasets/resource_inventory_20260921.md`：210 当前正式数据池约 5.13 TiB；
- 2026-09-21 对官方项目页、官方 GitHub、官方 Hugging Face / Google Cloud 下载页的逐项核查。

本轮**没有启动任何下载**。先把“缺什么、是否真的需要、是否和已有数据重复”定清楚。

核心结论：

1. **不要按“缺失名单”全量补齐。** 里面混有原始数据、衍生 annotation、benchmark、simulator、自建数据和非公开数据。
2. 210 已经覆盖最重要主干：**nuScenes + OpenScene/NAVSIM v1/v2 + Bench2Drive no-depth**。
3. 当前最有价值的新增数据不是 7–20TB 级大包，而是：
   - **HUGSIM released scenes：60.7 GB**
   - **OmniDrive annotations：885 MB**
   - **nuScenes-Occupancy v0.1 annotations：约 5 GB 压缩 / 130 GB 解压**
   - **OpenLane-v2 annotation/info 层：约 9 GB 量级，避免重复下载 images**
   - **CityWalker：6.82 GB**
   - 若做 Drive-JEPA 预训练：**CoVLA 452 GB + DrivingDojo 283 GB**
   - 若扩展 traffic-simulation 线：**WOMD Motion v1.3.1 + ProSim-Instruct**
4. **Bench2Drive depth 7.35 TB 暂不下**；210 已有 415 GB no-depth 和 maps，而核心 WAM 复现没有足够证据需要完整 depth。
5. **OpenDV full 暂不下**：原视频约 3 TB、处理后 frames 约 24 TB；先用官方 25h mini（raw ~44 GB）验证 world-model 数据链。
6. **nuPlan 不建议现在盲下 full raw >20 TB。** 210 已有 OpenScene 2.55 TB 的 2 Hz nuPlan 重分发；应先补 **nuPlan trainval DB/log 层**，再按核心论文是否真的需要高频原始 camera 决定 camera-only raw，而不是默认全传感器。
7. **Waymo Perception / KITTI-360 / PandaSet raw 暂缓**。如果目的只是 HUGSIM closed-loop，直接下载 HUGSIM 60.7 GB 重建资产远比补齐其四套原始数据合理。
8. DriveReward、SocioDrive-Bench 当前没有找到可确认的官方独立公开 dataset 下载包，**不碰非官方镜像**。

---

## 1. 当前 210 基线

| 数据 | 210 当前状态 | 逻辑占用 |
|---|---|---:|
| nuScenes | Core Full + CAN + map expansion + camera supplement | ~0.36 TiB |
| OpenScene v1.1 | trainval/test/mini，nuPlan 2 Hz 重分发 | ~2.37 TiB |
| NAVSIM v1 | 已有 | ~418.22 GiB |
| NAVSIM v2 | 含 navhard two-stage 等 | ~46.79 GiB |
| nuPlan | test sensor + mini DB/LiDAR + maps；**无 trainval DB/raw trainval** | ~1.62 TiB |
| Bench2Drive | v0.0.4 **no-depth** + maps | ~0.38 TiB |

因此后续每个候选都必须先问：

> 它提供的是已有数据的重复 sensor payload，还是新的 supervision / benchmark / modality？

---

## 2. 下载优先级定义

- **P0：现在值得补。** 小/中体量、高复用、低重复，直接填补验证或 annotation 缺口。
- **P1：研究方向明确后补。** 价值高，但体量较大、需要账号/协议，或只服务特定 WAM 路线。
- **P2：条件下载。** 单篇/外围路线、可由已有数据生成、或明显高重复。
- **P3：暂缓。** TB 级高成本但当前复现收益低，或有更小的替代资产。
- **HOLD：官方发布未确认。** 不使用非官方副本。

---

## 3. 主干缺口

### 3.1 nuPlan v1.1：拆成 DB/log 与 raw sensor 两层

**官方源**

- nuPlan devkit: https://github.com/motional/nuplan-devkit
- official download: https://www.nuscenes.org/nuplan
- dataset setup: https://github.com/motional/nuplan-devkit/blob/master/docs/dataset_setup.md

**版本**：nuPlan dataset v1.1；官方 devkit 当前 1.2.x 仍以 v1.1 dataset 为主。

**许可 / gated**

- 下载需要创建账户并同意 Terms of Use；
- devkit 本身 Apache-2.0，但 dataset 不能用代码 license 替代数据 Terms。

**模态**

- trainval SQLite `.db`：轨迹、agent state、scenario annotations 等；
- raw sensor blobs：8 cameras + merged LiDAR；
- maps。

**大小**

- 官方公开页没有在未登录状态给出完整 raw trainval 分包总字节；
- OpenScene 官方说明：完整 nuPlan sensor data **over 20 TB**；
- OpenScene 2 Hz 重分发的 trainval sensor 已缩到 >2 TB。

**与 210 重复**

- 210 已有 maps；
- 已有 OpenScene 2 Hz trainval sensor，是 nuPlan 的下采样/重组织版本；
- 已有 nuPlan test raw sensor；
- **缺 nuPlan trainval DB**；
- **缺原始高频 trainval sensor**。

**决定**

- **P0：先补 trainval DB/log，不碰 full raw sensor。**
- **P1/P2：之后按论文需求补 raw camera，而不是一口气下 >20 TB 全传感器。**
- Epona / DriveLaW / WorldDrive / WA-JEPA 等若明确需要高于 2 Hz 的原始 nuPlan video，再评估 camera-only 分包。
- ReactSim-Bench 只要求 `nuplan-v1.1/splits/trainval` + maps，并不要求为此先下载 20TB sensor。

---

### 3.2 Bench2Drive v0.0.4 depth

**官方源**

- https://github.com/Thinklab-SJTU/Bench2Drive/tree/0.0.4
- https://huggingface.co/datasets/Bench2DriveData/Bench2Drive-V0.0.4-depth

**版本**：v0.0.4。

**大小**

- no-depth：约 400 GB；210 已有 415 GB；
- depth repo：**7.35 TB**；
- v0.0.4 depth 使用 `.npz`，并加入 3D occupancy 相关数据。

**许可**：官方 HF 标记 Apache-2.0。

**gated**：HF 页面公开，不属于强制申请型 gated dataset。

**与 210 重复**

- route/scenario 主体和 no-depth 数据已经有；
- depth 是新增 modality，但绝大多数 scene/route identity 与当前数据相同。

**决定：P3 暂缓。**

除非后续要复现依赖 depth / occupancy supervision 的具体方法，否则为新增单一 modality 增加 7.35 TB 不划算。

---

## 4. Closed-loop / simulation 数据

### 4.1 HUGSIM

**官方源**

- https://github.com/hyzhou404/HUGSIM
- https://huggingface.co/datasets/XDimLab/HUGSIM

**版本**：官方当前 release tree。

**大小**：**60.7 GB**。

**内容 / 模态**

- photorealistic 3D reconstructed scenes；
- `3DRealCar`；
- scenes；
- scenarios；
- nuScenes map cache；
- source scenes 来自 KITTI-360 / Waymo / nuScenes / PandaSet。

**许可**：HF dataset card 标记 **MIT**。

**gated**：否。

**与 210 重复**

- 有“内容来源”重叠，例如 nuScenes；
- 但 HUGSIM 文件是重建后的 3D/scene assets，不是重复的 nuScenes JPG/LiDAR。

**服务论文**：TOAD、WA-JEPA、DrivoR，以及 photorealistic closed-loop 对照。

**决定：P0，建议直接下载完整 60.7 GB。**

这是当前最清晰的“低体量、高验证价值”缺口。

---

### 4.2 RiskBench

**官方源**

- https://github.com/HCIS-Lab/RiskBench

**本质**：CARLA safety-critical/risk benchmark，不是自然道路 raw dataset。

**内容**：interactive / collision / obstacle / non-interactive scenario groups，官方提供完整数据下载和分卷方案。

**大小**：官方 GitHub 可确认有完整包与 2GB 分卷，但公开 README 未给出可信的总下载字节；下载前应以官方链接 manifest 实测。

**许可**

- repo code 为 GPL-3.0；
- 数据文件本身未在当前公开页上单独给出一份可明确区分的 dataset license，不能直接把代码 GPL 当数据许可。

**gated**：未发现账户审批型 gate。

**与 210 重复**：无；它是 CARLA 合成数据。

**决定：P3。** 主要服务 RiskWorld/风险支线，不是当前 12 核心 WAM 的基础。

---

### 4.3 ReactSim-Bench

**官方源**

- https://github.com/Thinklab-SJTU/ReactSim-Bench

**本质**：基于 nuPlan 的 reactive traffic simulation benchmark。

**规模**：官方论文/README 给出 **2,636** 个 test scenarios：
- longitudinal 937
- directional 799
- lateral 900

**依赖**

- `nuPlan maps`
- `nuplan-v1.1/splits/trainval`
- 官方 custom AV behaviors（HF）
- 预处理后再生成 train/val cache。

**模态**：vector/map/agent behavior；重点不是相机视频。

**许可 / gated**

- custom behavior / checkpoint 由官方 HF 提供；
- 是否有单独 dataset license 应以 HF 页面进入下载时显示的 terms 为准；
- 不需要为它下载 nuPlan full raw sensor。

**与 210 重复**

- maps 已有；
- OpenScene sensor 不替代 nuPlan trainval DB；
- 当前最大缺口是 **trainval DB**。

**决定：P1。**

先完成 nuPlan trainval DB，再取 custom behaviors。它不应成为下载 full nuPlan sensor 的理由。

---

### 4.4 SocioDrive-Bench / CausalDrive

**论文原文确认**

- 20K clips；
- 80% 从 nuPlan 真实日志挖掘；
- 20% CARLA safety-critical data；
- CausalDrive 另以 OpenDV 1,700 h 预训练并使用 Bench2Drive OOD augmentation。

**官方下载状态（2026-09-21）**

当前检索未找到能够确认归属于作者的独立 SocioDrive-Bench dataset release。

**决定：HOLD。**

不下载第三方镜像；保留 release watcher。底层 OpenDV / nuPlan / Bench2Drive 分别处理。

---

### 4.5 BridgeSim / SUMMIT

它们首先是 simulator / platform，而不是必须先下载的一份统一“dataset archive”。

- BridgeSim 可承载 nuPlan / nuScenes / WOMD / CARLA 等 scene source；
- SUMMIT 基于 CARLA，用于交互闭环 simulation。

**决定：P2（软件/环境任务），不列入本轮基础 dataset payload 队列。**

---

## 5. Waymo / motion simulation 数据线

### 5.1 WOMD — Waymo Open Motion Dataset

**官方源**

- https://waymo.com/open/download/
- GCS bucket：官方 download 页跳转
- Waymax config 可直接读取 official WOMD shards。

**当前版本**：**Motion Dataset v1.3.1（2025-10）**，新增 `sdc_paths`；v1.3.0 / v1.2.x 仍可从 version history 获取。

**规模 / 模态**

- 103,354 个原始 driving segments；
- motion/scenario 数据包含 agent histories/futures、HD map、traffic-light state；
- 不是 Waymo Perception raw camera/LiDAR corpus；
- v1.2+ 还存在 lidar/camera related extensions，但若目标是 GameFormer / M2I / ProSim，首先需要的是 scenario/motion layer。

**大小**

官方公开 download landing page没有直接给整套 v1.3.1 aggregate byte size。为避免拿第三方估算冒充官方数字，本报告暂不写虚假的“官方 TB 数”。

下载实施前应直接对官方 GCS `scenario/{training,validation,testing}` 做 bucket listing，记录 object count + content-length，生成我们的 manifest 后再入队。

**许可**：Waymo Open Dataset Terms，**Non-Commercial Use**。

**gated**：需要账号/登录并接受 Waymo terms。

**与 210 重复**：无。它是独立 Waymo motion corpus。

**服务论文**：BeTop、GameFormer、M2I、ProSim、BridgeSim 等。

**决定：P1。**

优先下载 **Motion/scenario**，不下载 Waymo full Perception。

---

### 5.2 Waymo Perception raw dataset

**官方源**同 Waymo Open Dataset download page。

**模态**：camera + LiDAR + perception annotations。

**用途**：在本仓库主要作为 HUGSIM/重建来源，而不是核心 planning WAM 的训练主干。

**与 210 重复**：无。

**决定：P3。**

如果目标是 HUGSIM closed-loop，60.7GB 的官方 HUGSIM reconstructed scenes 已能直接满足 benchmark；没必要为此补 full Waymo sensor corpus。

---

### 5.3 ProSim-Instruct-520k

**官方源**

- https://github.com/Ariostgx/ProSim
- official project: https://ariostgx.github.io/ProSim/

**规模**

- 520K WOMD scenarios；
- >10M agent-prompt pairs；
- 基于 WOMD train/val 添加 route sketch / goal / action tag / text instruction 等 prompt annotations。

**模态**：WOMD vector states/maps + prompt / instruction annotations。

**大小**：作者官方 README 已给 download entry，但当前公开索引没有稳定暴露总字节；下载前应对官方 asset 列表做 manifest。

**许可**

- 必须先满足 WOMD non-commercial terms；
- ProSim annotation 独立 license 在当前 README 摘要中未明确到可以安全替代 WOMD terms 的程度，因此下载前再记录 asset 自带 LICENSE。

**gated**：底层 WOMD gated。

**与 210 重复**：annotation 是新数据；底层 WOMD 当前不存在。

**决定：P2。**

先完成 WOMD；只有继续交通行为/闭环 simulation 研究时再补 ProSim-Instruct。

---

## 6. 大规模驾驶视频预训练数据

### 6.1 OpenDV-YouTube

**官方源**

- https://github.com/OpenDriveLab/DriveAGI

**规模**

- >1,700 h；
- >244 cities / 40 countries；
- 原视频大多 1080p。

**官方体量**

- full raw videos：**约 3 TB**
- full processed consecutive frames：**约 24 TB**
- official mini：25 h
  - raw：**约 44 GB**
  - processed：**约 390 GB**

**模态**：front driving video；另有 language annotations。

**许可**

- video list / raw source 受 YouTube source/license/availability 约束；
- language annotation 是独立发布资产，不能把它的 license 自动套给原 YouTube 视频。

**gated**：不是统一账户审批型 dataset；实际下载依赖公开视频是否仍可访问。

**与 210 重复**：无。

**服务论文**：Vista、PolicyWM/PWM、CausalDrive 等。

**决定**

- **P1：先下载 OpenDV-mini raw 44 GB，验证数据 pipeline。**
- **P3：full 3TB raw / 24TB processed 暂缓。**
- 如果后续真的做规模化 video pretraining，再升级，不要先把 24TB frame cache 塞进 210。

---

### 6.2 CoVLA

**官方源**

- https://huggingface.co/datasets/turing-motors/CoVLA-Dataset

**大小**：**452 GB**。

**规模 / 模态**

- >80 h real-world driving；
- 10,000 × 30s clips；
- front camera；
- CAN/state/action；
- driving trajectory；
- natural-language descriptions。

**许可**

- video + CAN：CoVLA-Dataset Licensing Terms；
- language descriptions：VideoLLaMA 2 license；
- 必须分别遵守，不能简化成统一 Apache。

**gated**：**是**。HF 要求同意条件并分享 contact info。

**与 210 重复**：无。

**服务论文**：Drive-JEPA 的 driving-domain V-JEPA pretraining。

**决定：P1。**

若要复现 Drive-JEPA 的 330h pretraining 数据链，CoVLA 是高优先级，但需要用户账号手动接受 gate。

---

### 6.3 DrivingDojo

**官方源**

- https://huggingface.co/datasets/Yuqi1997/DrivingDojo

**主 repo 大小**：**283 GB**。

官方 main video shards 可见 8 个约 33–38 GB 的 tar.gz。

**模态**：driving video + action / camera metadata，服务 world-model / interactive driving representation training。

**许可**：main repo 标记 **Apache-2.0**。

**gated**：**是**，需要 HF 登录并同意 share contact。

**Extra repos**

官方还有 `DrivingDojo-Extra1` 等扩展，Extra1 本身又是 283 GB 且标记 CC-BY-NC-SA-4.0。**不能默认把所有 Extra 一起下。**

**与 210 重复**：无。

**服务论文**：Drive-JEPA。

**决定：P1，只先下 main 283 GB。**

只有 Drive-JEPA paper/code 明确要求某个 Extra 时再补对应扩展。

---

## 7. Occupancy / topology 衍生监督

### 7.1 Occ3D-nuScenes

**官方源**

- https://github.com/Tsinghua-MARS-Lab/Occ3D

**模态**

- nuScenes 上的 3D semantic occupancy labels；
- 0.4m voxel；
- volume [200, 200, 16]；
- 18 类；
- 基于 6 cameras 对齐。

**许可**

- Occ3D generated data：MIT；
- 同时必须遵守底层 nuScenes terms。

**gated**：底层 nuScenes 需要账号/terms；annotation 本身作者公开。

**大小**

官方 repo 当前页面没有给出单一 archive 的可靠总字节。第三方 repack 显示 train ~41.2GB、val ~9.1GB，可作为**容量估算**，不能写成官方 checksum-size。

**与 210 重复**

- raw nuScenes 完全已有；
- 只需要新 occupancy annotation，不需要再下载 images。

**决定：P1/P2。**

如果进入 occupancy-world-model 支线，下载 labels；否则不是 12 核心规划 WAM 的必需项。

---

### 7.2 nuScenes-Occupancy（OpenOccupancy）

这里必须纠正一个潜在混淆：

DriveOccWorld 原文引用的是 **Wang et al. 2023 OpenOccupancy-C**，对应：

- https://github.com/JeffWang987/OpenOccupancy

而不是另一个 `occupancy-for-nuscenes` 项目。

**官方当前推荐版本**：**nuScenes-Occupancy v0.1**。

**官方大小**

- v0.0：~24 GB 压缩 / ~270 GB 解压，已 deprecated；
- **v0.1：~5 GB 压缩 / ~130 GB 解压**。

**规模 / 模态**

- train 28,130 frames；
- val 6,019；
- 6 cameras；
- voxel 0.2m；
- volume [512,512,40]；
- 17 semantic labels（含 noise/empty 定义）。

**许可**：OpenOccupancy repo **Apache-2.0**；底层 nuScenes terms 仍适用。

**gated**：annotation 本身 Google Drive/Baidu；底层 nuScenes已有。

**与 210 重复**

- raw nuScenes 已有；
- 新增仅 occupancy annotation / derived depth cache。

**决定：P0/P1，建议下 v0.1 annotation，不下 v0.0。**

压缩只 5GB，是很低成本的监督扩展；depth_gt 可在 210 从现有 nuScenes 生成。

---

### 7.3 OpenLane-v2

**官方源**

- https://github.com/OpenDriveLab/OpenLane-V2

**许可**

- dataset：**CC BY-NC-SA 4.0**
- 还必须分别同意 nuScenes 与 Argoverse 2 terms；
- code：Apache-2.0。

**官方体量（关键部分）**

subset_A：
- info：~8.8 GB
- Map Element Bucket：~240 MB
- train images：7 × ~14GB ≈ 99GB
- val image：~21GB
- test image：~21.2GB

subset_B：
- info：~7.7GB
- images 另计。

**模态**：3D lane centerline、traffic elements、topology relationships、images、SD map。

**与 210 重复**

- OmniDrive 主要使用其 topology/centerline information；
- subset_A 的 image source 与 nuScenes 关系紧密，下载整套 images 会产生明显 sensor-level 重复；
- 210 已有 nuScenes。

**决定：P0，先下 `subset_A info + Map Element Bucket`，不下 images。**

约 9 GB 就能补主要 topology annotation；需要时再做 path mapping 到现有 nuScenes。

---

## 8. VLM / QA / reward annotation 支线

这一类原则是：

> 210 已有 nuScenes/NAVSIM sensor，就优先只下载 JSON/QA/annotation，不重复下图片。

### 8.1 OmniDrive

**官方源**

- https://github.com/NVlabs/OmniDrive
- GitHub Release v1.0

**主要 data asset**：`data_nusc.zip` **885 MB**。

**上游**：nuScenes + OpenLane-v2 topology + counterfactual trajectory annotation。

**许可**：repo 根 LICENSE 为 **NVIDIA non-commercial research/evaluation license**。

**gated**：GitHub Release 公开。

**与 210 重复**：raw nuScenes 已有；885MB 基本是新的 annotation/data package。

**决定：P0。**

---

### 8.2 DriveLM

**官方源**

- https://huggingface.co/datasets/OpenDriveLab/DriveLM

**大小**：official HF repo **4.86 GB**。

**内容**：DriveLM-nuScenes / DriveLM-CARLA 的 graph VQA / reasoning data；repo 中包含部分 nuScenes-subset images 和 JSON。

**许可**：**CC-BY-NC-SA-4.0**。

**gated**：是，需要 HF contact-info gate。

**与 210 重复**

- nuScenes images 不必再下；
- 应优先下载 QA JSON / annotation files。

**决定：P1（annotation-only）。**

---

### 8.3 NuScenes-QA

**官方源**

- https://github.com/qiantianwen/NuScenes-QA

**版本**：v1.0 release line。

**内容**：基于 nuScenes 的 visual QA，官方提供 QA annotations；visual side 可用原始 nuScenes 或 pre-extracted features。

**大小**：官方项目页未给 annotation bundle 的稳定总字节；下载前对 Google Drive assets 做 manifest。

**许可 / gated**：项目公开；底层 nuScenes terms 继续适用。数据包若有单独条款，以下载资产为准。

**与 210 重复**：只需要 QA annotation，不需 nuScenes sensor。

**决定：P1 annotation-only。**

---

### 8.4 NuInstruct

**官方源**

- https://github.com/xmed-lab/nuinstruct

**规模**：约 **91K multi-view video-QA pairs / 17 subtasks**。

**内容**：Perception / Prediction / Risk / Planning with Reasoning；annotation 指向 nuScenes sample tokens。

**官方说明**：images 直接从 nuScenes 获取，annotations 另从 Google Drive 下载。

**大小**：官方 README 未给 annotation zip 总字节。

**许可**：仓库公开页当前没有足够明确的数据许可字段，不能自行补成 Apache/MIT；底层 nuScenes terms 仍适用。

**与 210 重复**：images 100% 可复用现有 nuScenes；只下 annotation。

**决定：P1/P2 annotation-only。**

---

### 8.5 Talk2Car

**官方源**

- https://github.com/talk2car/Talk2Car

**上游**：nuScenes。

**大小**

- 官方提供 `Talk2CarSlim`，**<2 GB**；
- 若用全 nuScenes version，原始 nuScenes 由我们现有数据复用。

**模态**：natural-language commands + referred objects / image context；另有 trajectory/destination extensions。

**许可**：官方 repo 表述 software MIT；商业用途需联系作者。底层 nuScenes terms 仍适用。

**gated**：Slim 通过 Google Drive，未见申请型 gate。

**与 210 重复**：只需 Slim/commands，不重复下载 nuScenes。

**决定：P2。**

---

### 8.6 ReCogDrive processed pretraining annotations

**官方/作者发布 HF**

- `owl10/ReCogDrive_Pretraining`

**大小**：约 **3.79 GB**。

**许可**：HF card 标记 Apache-2.0。

**内容**：已经汇总/预处理多类驾驶 reasoning 数据，其中含 LingoQA / NAVSIM_ReCogDrive 等 JSONL。

**与 210 重复**

- sensor 层和 NAVSIM/其他源有重叠；
- 作为 annotation aggregate 反而可以避免我们重复整理多个原始 QA 数据。

**决定：P1。**

如果目标是复现 DriveReward 第一阶段，优先评估这个 annotation aggregate，比重复搬所有 raw visual assets 更合理。

---

### 8.7 LingoQA

**官方源**

- https://github.com/wayveai/LingoQA

**规模**

- 28K driving scenarios；
- 约 419K QA annotations；
- Scenery / Action 两类 training data + official eval。

**许可**：Wayve Dataset Licence Agreement，**Non-Commercial Use**。

**gated**：下载链接走官方 Drive；法律上下载即接受协议。

**大小**：官方 GitHub 未公布完整 Google Drive 文件总字节，因此下载前需先列 asset manifest。

**与 210 重复**：无直接 sensor duplicate。

**决定：P2。**

如果 ReCogDrive aggregate 已覆盖 DriveReward 所需 LingoQA annotations，先不重复拉 full LingoQA videos。

---

### 8.8 Senna

Senna 官方仓库当前提供的是：

- 代码；
- weights；
- **用 nuScenes 自行生成 QA data 的 converter**。

并没有一套必须单独下载的大型“Senna raw dataset”。

**官方源**：https://github.com/hustvl/Senna

**license**：code Apache-2.0。

**与 210 重复**：底层 nuScenes 已有。

**决定：P2 / generate locally。**

不要把“Senna”误列成一份独立 sensor archive。

---

### 8.9 DriveGPT4 / SUTD 等

它们在 DriveReward paper 中作为 domain QA pretraining mix 出现，但对当前 WAM 数据池而言属于**语言 annotation 辅助支线**，并非 65 篇中重复出现的基础 sensor corpus。

**决定：P2。**

只有真的复现 DriveReward 两阶段 VLM reward model 时，才逐个补其 annotation；不把它们加入近期大数据下载队列。

---

### 8.10 DriveReward

**论文**：arXiv:2606.08525。

仓库 paper raw 明确：

- source = NAVSIM train；
- DriveReward-Bench = NAVSIM test 中抽样；
- 作者从 trajectories + PDMS + rule/VLM annotation 构造 reward QA。

**官方独立 dataset release 状态**

截至 2026-09-21，本轮未找到能够确认是作者官方发布的 DriveReward dataset repository / downloadable archive。

**与 210 重复**：底层 NAVSIM 已完整在 210。

**决定：HOLD。**

等作者 release；如要提前复现，应基于现有 NAVSIM 按论文 pipeline 生成，而不是下载未知第三方包。

---

## 9. 其他真实驾驶数据：只因单篇/重建来源出现

### 9.1 CityWalker

**官方源**

- https://huggingface.co/datasets/ai4ce/CityWalker
- https://github.com/ai4ce/CityWalker

**大小**：**6.82 GB**。

**模态**：urban navigation image trajectories / pose labels。

**许可**：upstream GitHub code Apache-2.0；HF dataset card未单独写 license 字段，使用数据前保留 upstream terms 证据。

**gated**：否。

**与 210 重复**：无。

**服务论文**：Metis urban navigation branch。

**决定：P0/P1。**

体量很小；如果希望完整复现 Metis 的跨任务验证，值得直接补。

---

### 9.2 KITTI-360

**官方源**

- https://www.cvlibs.net/datasets/kitti-360/
- official scripts: https://github.com/autonomousvision/kitti360Scripts

**模态**：camera、LiDAR、3D/semantic scene data。

**gated**：官方下载需要 registration/account。

**大小**：官方按组件分包；仅某些 perspective/semantic components 已到百 GB 级，完整多模态不能用一个未经核验的第三方“总 GB”替代官方 manifest。

**与 210 重复**：无。

**主要用途**：HUGSIM source。

**决定：P3。**

先下载 HUGSIM reconstructed scenes，不因 HUGSIM 反向补 full KITTI-360。

---

### 9.3 PandaSet

**官方源**

- https://pandaset.org/
- https://github.com/scaleapi/pandaset-devkit

**模态**：6 cameras + 2 LiDAR + GPS/IMU + cuboid/semantic annotations。

**gated**：官方需要 signup form / download access。

**大小**：公开镜像对总量给出不同数字；本轮没有找到官方页面直接给可信 aggregate byte size，因此不采用镜像数字当官方值。

**与 210 重复**：无。

**主要用途**：HUGSIM source。

**决定：P3。**

同样直接用 HUGSIM release。

---

### 9.4 Lyft-Level5

**官方源 / 状态**

历史官方 Level5 / Lyft nuscenes-style devkit 仍可查，但数据分发已经不是当前研究生态最稳定的一条下载线。

**模态**：camera / LiDAR / map / trajectories 等。

**用途**：DriveOccWorld 单篇的 occupancy forecasting。

**大小 / license**：当前官方入口未给出足够稳定的统一 current download manifest；不采用 Kaggle/HF mirror 的体量替代官方数据事实。

**与 210 重复**：无。

**决定：P3。**

单篇、非核心，且当前 official distribution 不如其他数据稳定。

---

## 10. 推荐下载计划

### Phase A — 低成本高收益，先补齐

目标：增加 closed-loop benchmark + annotations，不重复搬 sensor。

| 项 | 预计新增 |
|---|---:|
| HUGSIM full | 60.7 GB |
| OmniDrive data_nusc | 0.885 GB |
| nuScenes-Occupancy v0.1 compressed | ~5 GB |
| OpenLane-v2 subset_A info + Map Element Bucket | ~9.0 GB |
| CityWalker | 6.82 GB |
| **小计（压缩下载口径）** | **约 82–85 GB** |

附加：
- nuPlan trainval DB：官方登录后获取，大小先以官方对象 manifest 为准；
- NuScenes-QA / NuInstruct 等 annotation-only：体量预计远小于 raw sensor，但先生成每个官方 asset manifest 再入队。

**建议先做 Phase A。**

---

### Phase B — Drive-JEPA 数据链

需要手动完成 HF gated acceptance：

| 项 | 大小 |
|---|---:|
| CoVLA | 452 GB |
| DrivingDojo main | 283 GB |
| OpenDV-mini raw | ~44 GB |
| **小计** | **约 779 GB** |

注意：

- OpenScene 已有，不再重复；
- DrivingDojo Extra 不自动下载；
- OpenDV 不生成 390GB mini frames，先保留 44GB raw，训练前再按需要局部处理。

**Phase B 只在确定要复现 Drive-JEPA / driving-video pretraining 时执行。**

---

### Phase C — Waymo behavior / simulation 线

1. 手动登录 Waymo、接受 Non-Commercial Terms；
2. 只列举 WOMD v1.3.1 `scenario` shards；
3. 在下载前生成 object count / byte size / checksum manifest；
4. 先下 training + validation motion/scenario；
5. 再决定 ProSim-Instruct-520k。

**不带 Waymo Perception raw。**

---

### Phase D — 暂缓的大体量项

| 项 | 原因 |
|---|---|
| Bench2Drive depth 7.35TB | 单一新增 modality，当前核心 WAM 复现收益不足 |
| OpenDV full 3TB raw | 先用 44GB mini 验证 |
| OpenDV processed 24TB | 不能把预处理 cache 当基础数据先占满 NAS |
| nuPlan full raw sensor >20TB | 210 已有 2Hz OpenScene；先按高频 camera 真实需求拆分 |
| Waymo Perception full | HUGSIM eval 无需它 |
| KITTI-360 raw | HUGSIM release 可替代当前目的 |
| PandaSet raw | 同上 |
| Lyft-Level5 | 单篇、官方分发稳定性低 |
| RiskBench full | 风险外围支线 |
| DrivingDojo Extra* | 主 repo 足够先验证 |

---

## 11. Gated / 手工授权清单

这些不能由后台脚本替用户“自动同意协议”：

| 数据 | 人工动作 |
|---|---|
| nuPlan | 注册 / 登录 / 接受 Terms |
| WOMD | Waymo 登录 / 接受 Non-Commercial Terms |
| CoVLA | HF 登录 + share contact + 接受 CoVLA terms |
| DrivingDojo | HF 登录 + share contact |
| DriveLM | HF gated access |
| KITTI-360 | registration |
| PandaSet | signup/download access |
| OpenLane-v2 | 需遵守 nuScenes + Argoverse 2 terms |

因此真正执行下载时，先解决这些授权，再写自动下载脚本。

---

## 12. 去重策略

### 12.1 nuScenes 系

210 已有完整 nuScenes，所以以下资源只取 annotation：

```text
Occ3D              → labels only
nuScenes-Occupancy → v0.1 annotation only
OpenLane-v2        → info / topology only
OmniDrive          → data_nusc annotation package
DriveLM            → QA JSON / annotation only
NuScenes-QA        → QA only
NuInstruct         → QA only
Talk2Car           → Slim/commands only
Senna              → locally generate QA from existing nuScenes
```

### 12.2 nuPlan 系

```text
210 current:
nuPlan test raw
+ mini DB/LiDAR
+ maps
+ OpenScene v1.1 2Hz trainval/test
+ NAVSIM v1/v2

next:
trainval DB  ← 新增且关键

do NOT automatically:
full raw trainval >20TB
```

只有论文要求高频 video/sensor 且 OpenScene 2Hz 不够，才补对应 raw camera。

### 12.3 HUGSIM

HUGSIM scenes 是**derived reconstruction**，不是 raw-source duplication。下载 HUGSIM 后，不要为了“数据完整性”又把 Waymo/KITTI/PandaSet 全搬进来。

---

## 13. 当前建议的最终下载顺序

```text
A0  nuPlan trainval DB/log
A1  HUGSIM 60.7GB
A2  OmniDrive 885MB
A3  nuScenes-Occupancy v0.1 ~5GB compressed
A4  OpenLane-v2 subset_A info + Map Element Bucket ~9GB
A5  CityWalker 6.82GB

B0  完成人工 gated 授权
B1  CoVLA 452GB
B2  DrivingDojo main 283GB
B3  OpenDV-mini raw ~44GB

C0  WOMD v1.3.1 manifest
C1  WOMD scenario training/validation
C2  ProSim-Instruct-520k

D   QA annotations按 DriveReward 复现需求补：
    DriveLM / ReCogDrive / NuScenes-QA / NuInstruct / Talk2Car / LingoQA ...

HOLD:
    DriveReward official release
    SocioDrive-Bench official release

SKIP FOR NOW:
    Bench2Drive depth 7.35TB
    OpenDV 24TB processed
    nuPlan >20TB full raw
    Waymo Perception
    KITTI-360 raw
    PandaSet raw
    Lyft-Level5
    RiskBench
```

如果目标仍然是“先把 WAM 12 核心 + 代表性扩展论文做扎实”，这是比“看到缺失就全下”更合理的数据路线。

---

## 14. 关键官方 source index

### 已有主干 / nuPlan

- nuPlan devkit: https://github.com/motional/nuplan-devkit
- nuPlan dataset setup: https://github.com/motional/nuplan-devkit/blob/master/docs/dataset_setup.md
- OpenScene: https://github.com/OpenDriveLab/OpenScene

### closed-loop / benchmark

- Bench2Drive: https://github.com/Thinklab-SJTU/Bench2Drive
- Bench2Drive v0.0.4 depth: https://huggingface.co/datasets/Bench2DriveData/Bench2Drive-V0.0.4-depth
- HUGSIM: https://github.com/hyzhou404/HUGSIM
- HUGSIM assets: https://huggingface.co/datasets/XDimLab/HUGSIM
- ReactSim-Bench: https://github.com/Thinklab-SJTU/ReactSim-Bench
- RiskBench: https://github.com/HCIS-Lab/RiskBench

### motion / simulation

- Waymo Open Dataset: https://waymo.com/open/download/
- ProSim: https://github.com/Ariostgx/ProSim

### video pretraining

- OpenDV / DriveAGI: https://github.com/OpenDriveLab/DriveAGI
- CoVLA: https://huggingface.co/datasets/turing-motors/CoVLA-Dataset
- DrivingDojo: https://huggingface.co/datasets/Yuqi1997/DrivingDojo

### occupancy / topology

- Occ3D: https://github.com/Tsinghua-MARS-Lab/Occ3D
- OpenOccupancy / nuScenes-Occupancy: https://github.com/JeffWang987/OpenOccupancy
- OpenLane-v2: https://github.com/OpenDriveLab/OpenLane-V2

### language / reasoning

- OmniDrive: https://github.com/NVlabs/OmniDrive
- DriveLM: https://huggingface.co/datasets/OpenDriveLab/DriveLM
- NuScenes-QA: https://github.com/qiantianwen/NuScenes-QA
- NuInstruct: https://github.com/xmed-lab/nuinstruct
- Talk2Car: https://github.com/talk2car/Talk2Car
- Senna: https://github.com/hustvl/Senna
- LingoQA: https://github.com/wayveai/LingoQA
- CityWalker: https://huggingface.co/datasets/ai4ce/CityWalker

---

## 15. 仍需在真正下载前做的 manifest gate

本报告已经足够用于确定**下载路线**，但在任何大包入队前仍必须通过同一 gate：

1. 官方下载 URL；
2. exact version；
3. object/file list；
4. upstream byte size；
5. checksum / ETag / hash 能否作为验收依据；
6. license snapshot；
7. 是否 gated；
8. 210 destination path；
9. 与现有数据的 path/hash overlap；
10. 压缩后 + 解压后磁盘预算；
11. 是否能只下载 annotation / selected modality；
12. acceptance script。

尤其是：

- nuPlan trainval DB / raw camera；
- WOMD；
- ReactSim custom behaviors；
- ProSim-Instruct；
- NuScenes-QA / NuInstruct / LingoQA；

这些官方入口存在，但网页并未全部公开“总字节 + checksum”，必须在授权后先生成 manifest，**不能直接开长跑下载**。
