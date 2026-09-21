# WAM 数据缺口全网核查与下载计划（2026-09-21）

## 0. 任务与口径

本文件承接两份已有底账：

- `datasets/wam_field_dataset_census_20260921.md`：65 篇论文逐篇核实“实际用了什么数据”；
- `datasets/resource_inventory_20260921.md`：210 开发机正式数据根的现场事实。

本轮只回答一个问题：缺失/部分覆盖的数据，到底哪些应该下载、下载什么、哪些应该复用已有 raw data、哪些应该等待或按需生成。

对每项尽量核查：官方/作者发布源、当前版本、体量、模态、许可、是否 gated、与 210 的重复关系。官方没有给出统一字节数或 dataset-specific license 的，保留 UNKNOWN，不用第三方估算冒充官方数字。

> 重要：210 的“未见”仅表示 2026-09-21 正式数据根 inventory 未记录。真正开跑下载前，还应做目标路径 existence / manifest / hash 检查。

---

## 1. 下载策略结论

210 已经有约 5.13 TiB 的核心 planning 主干：nuScenes、OpenScene v1.1、NAVSIM v1/v2、Bench2Drive v0.0.4 no-depth + maps，以及 nuPlan test/mini/maps。最大的缺口不是“再复制一套 raw sensor”，而是三类东西：

1. 薄层监督/派生 benchmark：occupancy、topology、QA、robustness labels；
2. 独立闭环/重建资产：HUGSIM、ReactSim custom behavior；
3. 真正新的行为/视频分布：WOMD、CoVLA、DrivingDojo、OpenDV。

因此采用四级策略：

- **P0 审计/复用**：先确认 210 是否已有薄层数据，避免重复；
- **P1 立即补**：体量小、重复少、直接提高论文覆盖；
- **P2 账号/许可就绪后补**：WOMD、CoVLA、DrivingDojo 等新分布；
- **P3 暂缓**：TB～20TB 级 raw 数据，只有明确复现实验才激活；
- **WAIT**：论文存在，但当前没有稳定官方独立数据包。

---

## 2. P0：下载前必须先审计的现有数据

### 2.1 OpenScene v1.0 occupancy labels

OpenScene 官方说明：v1.1 trainval camera 约 1.1 TB、LiDAR 约 822 GB；如果做 occupancy，仍需从 v1.0 获取 occupancy label，trainval label 约 95.4 GB。210 inventory 只明确列出 v1.1 metadata/camera/LiDAR，没有明确写 occupancy labels。

**动作：**先检查正式根是否已经存在 v1.0 occupancy label。若缺，再下载约 95.4 GB label-only；不要重复 v1.1 sensor。

### 2.2 nuPlan trainval DB metadata

ReactSim-Bench 的官方预处理结构要求 `nuplan-v1.1/splits/trainval/*.db` + maps + custom behaviors。它不要求先把 >20 TB native sensor blobs 全部拉下来。

210 当前 inventory 只有 mini DB，未见 trainval DB。

**动作：**先补 trainval DB metadata；native raw trainval sensors 暂缓。

### 2.3 Turning-nuScenes

Turning-nuScenes 完全建立在 nuScenes validation 上。GraphWorld 原文给出 17 scenes / 680 samples；MomAD repo 还提供对应 planning-info pkl。

**动作：**只取索引/pkl，或按规则本地生成；不复制任何 nuScenes 图像。

---

## 3. 真实驾驶 / motion / 大视频数据

| 数据 | 当前官方/作者版本与规模 | 模态 | 许可 / Gate | 与 210 重复 | 决策 |
|---|---|---|---|---|---|
| **WOMD / Waymo Open Motion** | Motion **v1.3.1 (2025-10)**；103,354 个 20s segments、574h；官方未给单一总字节数 | agent tracks、3D map；可选 LiDAR；8 cameras 为 embedding，不是 raw RGB | Waymo Dataset License Agreement for Non-Commercial Use；**需登录并接受条款** | 210 未见 Waymo/WOMD，属于真正新分布 | **P2 高优先级**：先下 scenario train+val + map；先不下可选 LiDAR/camera embedding |
| **Waymo Perception raw** | v1.4.3 / modular v2.0.1；官方按 shard 提供 | raw cameras、LiDAR、labels | Waymo non-commercial license；gated | 与 WOMD 不等价，210 未见 | **P3**：目前不下；ProSim/BeTop/M2I 主线先满足 WOMD |
| **OpenDV-YouTube** | >1700h；raw mostly-1080p ~**3 TB**；processed frames ~**24 TB** | 单目驾驶视频；另有 language annotation | 原视频受 YouTube/source 条款；language 数据 CC BY-NC-SA 4.0 | 新视频分布 | **P3 full**；先走 mini |
| **OpenDV-mini** | 官方 25h；raw **44 GB**；processed ~390 GB | driving video | 同 OpenDV | 新 | **P1.5**：先下 raw 44 GB，训练时按需抽帧，不长期复制 390 GB 全量帧 |
| **OpenDV-YouTube-Language** | HF **14.3 GB** | JSON text annotations | CC BY-NC-SA 4.0；非 gate | 新 annotation | **P2**：PWM/CausalDrive/语言 world-model 激活时下 |
| **CoVLA** | HF **452 GB**；>80h、10k×30s clips | front video、CAN/ego signals、60-point trajectory、language | CoVLA custom academic/non-commercial + VideoLLaMA2；**HF gated/contact sharing** | 新 | **P2**：Drive-JEPA 预训练激活时下载 |
| **DrivingDojo** | HF **283 GB** | image-to-video driving data + action/camera metadata | HF 标记 Apache-2.0；**HF gated/contact sharing** | 新 | **P2**：与 CoVLA 成对补；二者已知 payload 约 735 GB |
| **CityWalker** | HF **6.82 GB** | urban navigation images + pose labels | dataset card 未显式给 data license；项目代码 Apache-2.0，下载前再确认 data terms | 新 | **P1**：体量小，直接补 |
| **KITTI-360** | perspective train/val 约 128 GB、fisheye 约 355 GB，另有 LiDAR/labels | cameras、LiDAR、poses、2D/3D semantics | CC BY-NC-SA 3.0；机构邮箱注册/用途声明 | 主要是 HUGSIM 上游之一 | **P3**：不为 HUGSIM 单独下 raw |
| **PandaSet** | 官方未给单一总包字节数 | 6 cameras、2 LiDAR、GPS/IMU、3D cuboid、semantic segmentation | 官网允许 academic/commercial use；下载前按官方最新条款确认 | 主要是 HUGSIM 上游之一 | **P3**：HUGSIM public reconstruction 足够时不下 raw |
| **Lyft Level5 Perception** | legacy release；官方 legacy 页未给稳定统一体量 | camera、LiDAR、maps、3D labels | Perception 数据公开文档为 CC BY-NC-SA 4.0；legacy source | 210 未见；只少数 occupancy 工作使用 | **P3**：先锁死 DriveOccWorld/Cam4DOcc 所需 release，再决定 |

---

## 4. Planning / closed-loop / reconstructed benchmark

| 数据 | 版本/规模 | 模态 | 许可 / Gate | 与 210 重复 | 决策 |
|---|---|---|---|---|---|
| **HUGSIM** | 官方 HF reconstructed assets **60.7 GB** | 3D reconstructed scenes、3DRealCar、nuScenes map cache、scenario definitions | MIT；非 gated | 源场景与 nuScenes/Waymo/KITTI/PandaSet有重叠，但 reconstruction 本身全新 | **P1：下载** |
| **Bench2Drive v0.0.4 depth** | HF **7.35 TB**；no-depth 官方包 415 GB | depth npz；新版另支持 3D occupancy | Apache-2.0；非 gated | 210 已有同版本 no-depth + maps | **P3：不下 depth**，只有明确 depth/3D-occ 任务才激活 |
| **RiskBench** | CARLA 0.9.14；官方 repo 提供完整数据与分块下载，但未给稳定总字节 | front camera、depth、instance segmentation、scenario labels | repo code GPL-3.0；**dataset-specific license 未明确** | 新但用途窄 | **P3**：RiskWorld/RiskBench 专题开始时只下需要 subset |
| **ReactSim-Bench** | 2,636 scenarios；作者提供 custom AV behaviors / checkpoints；总字节未可靠核到 | nuPlan vector-state scenarios + custom AV behaviors | repo/data 链接公开；dataset-specific license 需下载前再核 | 210 maps 已有，但 trainval DB 未见；不需要 native sensors | **P1.5**：custom behaviors + nuPlan trainval DB；不拉 >20TB raw sensors |
| **BridgeSim** | 跨 simulator 平台，没有 monolithic dataset | 转换/replay NAVSIM/OpenScene、nuScenes、WOMD、CARLA 等 | project/code 按作者 repo 许可 | 210 已覆盖大部分主支 | **REUSE**：装代码+转换已有数据；Waymo branch 等 WOMD |
| **SocioDrive-Bench** | CausalDrive paper：20K clips，80% nuPlan + 20% CARLA；未发现稳定官方 standalone release | sociology/reactive clips + interaction labels | UNKNOWN | 上游与 nuPlan/CARLA 重叠 | **WAIT** |
| **CARLA / SUMMIT** | simulator/software，不是固定基础数据包 | interactive simulation | 各软件项目许可 | 不属于 210 dataset inventory | **环境任务，不计基础数据下载** |

---

## 5. Occupancy / topology / robustness 薄层数据

| 数据 | 版本/规模 | 模态 | 许可 / Gate | 与 210 重复 | 决策 |
|---|---|---|---|---|---|
| **OpenScene v1.0 occupancy** | trainval labels **95.4 GB** | 3D occupancy/flow labels | OpenScene CC BY-NC-SA + nuPlan Dataset Agreement | sensor 100%复用现有 OpenScene | **P0 audit；缺失则 P1 label-only** |
| **nuScenes-Occupancy / OpenOccupancy** | 推荐 **v0.1**：~5 GB compressed / ~130 GB extracted；v0.0 deprecated | 0.2m voxel semantic occupancy，6 cameras对应 | project/code Apache-2.0；raw nuScenes遵守上游条款 | raw nuScenes 已有 | **P1：只补 v0.1 labels** |
| **Occ3D-nuScenes** | official release；官方 repo **未给 archive 总字节** | 3D voxel occupancy GT + visibility | generated data/code MIT，同时必须同意 nuScenes terms | raw nuScenes 已有 | **P1：只补 nuScenes labels；不下 Occ3D-Waymo** |
| **OpenLane-V2 subset_A** | info ~**8.8 GB** + Map Element Bucket ~**240 MB**；train images另约 28.3 GB | lane centerline、traffic elements、topology | CC BY-NC-SA 4.0 + nuScenes/Argoverse2 upstream terms | OmniDrive 主要要 topology；210 已有 nuScenes image | **P1：先下 ~9.04 GB info/Map Bucket，跳过重复 image** |
| **Turning-nuScenes** | 17 scenes / 680 samples；MomAD repo 提供 pkl | sample selection / planning infos | inherits nuScenes terms | 100%基于现有 nuScenes | **REUSE/GENERATE** |
| **Adv-nuSc** | HF **15.6 GB**；156 scenes、6115 samples | 6-camera adversarial rendered video + 3D boxes | HF CC-BY-SA-4.0；同时基于 nuScenes source | source scene 重叠，但 adversarial render 新 | **P1：下载** |
| **nuScenes-C** | 27 corruption types × 5 severity；full benchmark很大，官方论文未给单一当前总字节 | camera/LiDAR corruptions | 依赖 nuScenes terms | clean nuScenes 已有；corrupted data为派生冗余 | **P3：不下 full；GraphWorld只用 Rain/Snow/Fog，按需生成/取 subset** |

---

## 6. Language / reasoning / reward 数据

| 数据 | 版本/规模 | 模态 | 许可 / Gate | 与 210 重复 | 决策 |
|---|---|---|---|---|---|
| **OmniDrive-nuScenes** | v1.0 `data_nusc.zip` **885 MB** | counterfactual / 3D driving QA、planning reasoning | NVIDIA License：non-commercial research/evaluation | raw nuScenes 已有；QA新 | **P1：下载** |
| **DriveLM** | HF total **4.86 GB** | graph-VQA / language；包内还含部分 nuScenes images | language data CC BY-NC-SA 4.0；base data沿用上游条款 | image重复 | **P1：annotation JSON优先；不必复制 image subset** |
| **ReCogDrive_Pretraining** | 作者已发布完整 driving QA；HF bundle约 3.8 GB 量级，下载前以 listing 为准 | 12 source datasets rewritten QA + NAVSIM QA | 各源数据必须继续遵守原 license | annotations新，底层 images可能重复 | **P1：下 annotation bundle** |
| **NuScenes-QA** | v1.0；官方未给统一 annotation archive 字节 | QA annotations；可选 CenterPoint features | project MIT；visual data受 nuScenes terms | raw nuScenes已有 | **P1：annotation-only，不下 feature archive** |
| **NuInstruct** | 91K multi-view video-QA；官方未给统一字节 | perception/prediction/risk/planning reasoning QA | repo 未见独立 data license；nuScenes upstream applies | raw image已有 | **P1：annotation-only；license标记 unresolved** |
| **Talk2Car v1.1 / Slim** | Slim **<2 GB** | natural-language commands、referred objects、subset images | software MIT；商业 dataset use需联系作者；full mode受 nuScenes terms | raw nuScenes已有 | **P1：Slim/commands only** |
| **LingoQA** | official video-QA release；官方页未给统一总字节 | driving video + QA | Wayve Dataset Licence Agreement for Non-Commercial Use；限制较强 | 新 video分布 | **P2：只有 reward/VLM 分支激活才下** |
| **SUTD-TrafficQA** | Zenodo v1.0；files约 **20.5 GB** | 10,080 videos + QA / features | Zenodo公开；独立 license字段需开跑前再核 | 新 | **P2 optional** |
| **Senna** | ReCogDrive/DriveReward source之一 | driving QA / trajectory reasoning | 按原始 Senna terms | 可先由 ReCogDrive rewritten QA覆盖 | **REUSE：当前不单建 raw download** |
| **DriveGPT4 / BDD-X** | BDD-X 6970 videos、>77h；官方当前未给统一字节 | driving video + action/reason explanations | academic/research free；commercial需另授权 | 新 | **P3：DriveReward/DriveGPT4专题再下** |
| **DriveReward** | paper已定义 dataset/benchmark；截至本轮**未发现稳定官方 dataset release** | NAVSIM-based reward reasoning、7维评分 | UNKNOWN | underlying NAVSIM已在210 | **WAIT**：不自行拼“伪官方包” |

---

## 7. Prompt / traffic simulation annotation

| 数据 | 版本/规模 | 模态 | 许可 / Gate | 与 210 重复 | 决策 |
|---|---|---|---|---|---|
| **ProSim-Instruct-520k** | official raw release；覆盖 WOMD train/val 约 520K scenarios；>10M prompts；官方未给总字节 | Goal Point、Route Sketch、Action Tags、20 text instructions/scenario | 必须同时遵守 WOMD；standalone data license 在 README 未单独明确 | annotation新；底层 WOMD 当前缺 | **P2：WOMD落地后再下** |

---

## 8. 210 与候选数据的重复关系

### 8.1 不应重复拉 raw sensor

- Turning-nuScenes → 直接复用现有 nuScenes；
- OpenLane-V2 的 nuScenes image → 先只拿 topology info；
- OmniDrive / DriveLM / NuScenes-QA / NuInstruct / Talk2Car → 先拿 annotation；
- Occ3D-nuScenes / nuScenes-Occupancy → 只拿 labels；
- ReactSim-Bench → trainval DB/maps + custom behavior，不需要 native sensor；
- BridgeSim → 转换现有 OpenScene/NAVSIM/nuScenes/Bench2Drive。

### 8.2 上游重叠，但派生资产值得单独保存

- HUGSIM：重建后的 3D scenes/scenarios 是独立资产；
- Adv-nuSc：adversarial trajectories/rendered video 是新增内容；
- ProSim-Instruct：WOMD 上新增 prompts/tags；
- ReCogDrive：多来源 rewritten QA 是新增 annotation。

### 8.3 真正的新数据分布

- WOMD；
- OpenDV；
- CoVLA；
- DrivingDojo；
- CityWalker；
- LingoQA；
- KITTI-360 / PandaSet / Lyft（当前优先级低）。

---

## 9. 实际下载计划

### Phase 0 — 零/小流量审计

1. 检查 OpenScene v1.0 occupancy labels 是否已在 210；
2. 检查/补 nuPlan trainval DB metadata；
3. 建立现有 nuScenes 的共享映射/manifest，给 OmniDrive、DriveLM、NuScenes-QA、NuInstruct、Talk2Car、OpenLane-V2 共用；
4. Turning-nuScenes 只取 pkl/索引；
5. nuScenes-C 不下载全量，先记录 GraphWorld只需要 Rain/Snow/Fog。

### Phase 1 — 建议现在补：低重复、高覆盖

| 项目 | 已知新增网络量 | 备注 |
|---|---:|---|
| HUGSIM | 60.7 GB | 独立 photorealistic closed-loop 资产 |
| OpenScene occupancy label | 95.4 GB（仅若 P0 确认缺） | label-only |
| nuScenes-Occupancy v0.1 | 5 GB | 解压约 130 GB |
| Occ3D-nuScenes | UNKNOWN | 官方没给 archive 总字节；只取 labels |
| OpenLane-V2 subset_A info + Map Bucket | ~9.04 GB | 不下重复 images |
| OmniDrive | 0.885 GB | QA/CF reasoning |
| DriveLM | ≤4.86 GB | 实际建议 annotation-only |
| ReCogDrive QA | ~3.8 GB 量级 | 下载前 listing 锁字节 |
| Talk2CarSlim | <2 GB | commands/slim |
| CityWalker | 6.82 GB | Metis navigation branch |
| Adv-nuSc | 15.6 GB | GraphWorld robustness |
| NuScenes-QA | UNKNOWN | annotation-only |
| NuInstruct | UNKNOWN | annotation-only |
| ReactSim custom behaviors + nuPlan trainval DB | UNKNOWN | 不需要 native sensor |

已知且不把 Occ3D/UNKNOWN 项强行估算时：若 OpenScene occupancy 确认缺失，Phase 1 的明确网络量约 **0.20 TB 起步**；若它已经存在，则约 **0.10 TB 起步**。额外注意 nuScenes-Occupancy 解压需要约 130 GB。

### Phase 1.5 — world-model 小规模预训练试水

- OpenDV-mini raw：**44 GB**；
- 不长期保留约 390 GB 的全量 processed-frame 副本，先按训练代码按需抽帧/cache。

### Phase 2 — 真正的新行为数据主干

顺序建议：

1. **WOMD v1.3.1** scenario format train + validation：先 enumerate 官方 bucket 得到精确 manifest/bytes；不先下 Motion LiDAR/camera embeddings；
2. **ProSim-Instruct-520k**：WOMD 落地后再配套；
3. **DrivingDojo 283 GB**；
4. **CoVLA 452 GB**；
5. 如果进入语言/reward branch，再加 OpenDV-language 14.3 GB、LingoQA、SUTD-TrafficQA。

### Phase 3 — 明确不现在自动下载

- nuPlan native full raw trainval：>20 TB；
- Bench2Drive v0.0.4 depth：7.35 TB；
- OpenDV full raw：约 3 TB；
- OpenDV fully processed frames：约 24 TB；
- Waymo Perception raw；
- KITTI-360 raw；
- PandaSet raw；
- Lyft Level5 raw；
- full RiskBench；
- full nuScenes-C；
- BDD-X / DriveGPT4 visual corpus。

### WAIT — 监控发布

- DriveReward official dataset；
- SocioDrive-Bench standalone release。

---

## 10. 最终决策

对当前 210，最合理的扩容方向不是“把所有相关公开数据都完整下载”，而是：

> **先补薄层 annotation / HUGSIM / robustness → 再补 WOMD → 再按明确论文任务激活 CoVLA + DrivingDojo；TB 级 raw video/sensor 全部延后。**

这条路线能最大化复用现有 nuScenes + OpenScene/NAVSIM + Bench2Drive，把新增存储集中到真正带来新监督或新交互分布的数据。

---

## 11. 仍保留 UNKNOWN 的项目

没有足够官方证据就不填假数字：

- WOMD v1.3.1 scenario train+val 精确总字节；
- Occ3D-nuScenes 官方 archive 精确总字节；
- PandaSet 官方当前全包精确字节；
- Lyft Level5 中 DriveOccWorld 所需具体 release / archive；
- ReactSim custom behavior 总字节与独立 data license；
- NuInstruct annotation archive 总字节与独立 data license；
- NuScenes-QA annotation archive 总字节；
- LingoQA 总字节；
- RiskBench full data 总字节与 dataset-specific license；
- ProSim-Instruct-520k 总字节；
- DriveReward / SocioDrive-Bench standalone release。

这些项真正下载前必须做 listing / manifest / license gate audit。

---

## 12. 官方/作者源索引

- Waymo Open Dataset: https://waymo.com/open/download/ ; https://waymo.com/open/terms/
- OpenScene: https://github.com/OpenDriveLab/OpenScene/blob/main/docs/getting_started.md
- Bench2Drive: https://huggingface.co/datasets/rethinklab/Bench2Drive-V0.0.4 ; https://huggingface.co/datasets/Bench2DriveData/Bench2Drive-V0.0.4-depth
- HUGSIM: https://huggingface.co/datasets/XDimLab/HUGSIM
- OpenDV: https://github.com/OpenDriveLab/DriveAGI
- CoVLA: https://huggingface.co/datasets/turing-motors/CoVLA-Dataset
- DrivingDojo: https://huggingface.co/datasets/Yuqi1997/DrivingDojo
- CityWalker: https://huggingface.co/datasets/ai4ce/CityWalker
- Occ3D: https://github.com/Tsinghua-MARS-Lab/Occ3D
- nuScenes-Occupancy: https://github.com/JeffWang987/OpenOccupancy/blob/main/docs/prepare_data.md
- OpenLane-V2: https://github.com/OpenDriveLab/OpenLane-V2
- OmniDrive: https://github.com/NVlabs/OmniDrive/releases
- DriveLM: https://huggingface.co/datasets/OpenDriveLab/DriveLM
- ReCogDrive: https://github.com/xiaomi-research/recogdrive
- ReactSim-Bench: https://github.com/Thinklab-SJTU/ReactSim-Bench
- ProSim: https://github.com/Ariostgx/ProSim
- Adv-nuSc: https://huggingface.co/datasets/Pixtella/Adv-nuSc
- MomAD / Turning-nuScenes: https://github.com/adept-thu/MomAD

---

## 13. 与现有文档的职责分工

- 论文→数据使用事实：`wam_field_dataset_census_20260921.md`；
- 210 当前磁盘事实：`resource_inventory_20260921.md`；
- 本文件：官方源/版本/体量/许可/gate/重复关系 → 下载决策。

实际数据落地后，应新建/更新后继 resource inventory；不能把“计划下载”提前写成“已经拥有”。