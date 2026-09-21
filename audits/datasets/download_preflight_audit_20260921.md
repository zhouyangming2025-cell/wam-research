# WAM 数据下载前置深度审计（2026-09-21）

## 结论先行

本轮审计完成了“能不能安全开始准备队列”的判断，但**没有启动下载、没有生成新 queue、没有修改正式数据根**。

当前可以确认：

- 210 正式数据池为 `5,640,966,287,240 B`，约 `5.130 TiB`；
- 正式数据根已有 OpenScene/NAVSIM、nuPlan test/mini/maps、nuScenes Core/扩展、Bench2Drive v0.0.4 no-depth + maps；
- 210 当前无 WAM 下载、监督、验收、inventory 或 watcher 进程；
- 正式数据根没有 `.part`；6 个零字节历史锁保留为证据；
- OpenScene 正式目录中未发现 v1.0 occupancy/label 目录，inventory 中也没有对应条目；
- 当前下一批最值得准备的是“薄层标注/QA/重建资产”，不是 raw nuPlan trainval，也不是 Bench2Drive depth；
- 由于 210 对 Hugging Face、GitHub、Google Drive、Waymo 的直接 HEAD 探测均为 HTTP `000`，**当前还不能声称候选下载路径已具备可用字节通道**。必须先针对实际对象/签名 CDN 做 source probe，再建 queue。

因此本轮状态为：

> **研究和空间层面的候选已收敛；传输层和对象 manifest 仍未完全放行。继续只读准备，不启动下载。**

## 1. 现场基线

来源：

- 本机 `manifests/resource_inventory_20260921.json/.md/.tsv`；
- 210 `/mnt/nas/planning/zhouyangming/wam/cache/p2/wam_inventory_20260921.json`；
- 2026-09-21 17:24（Asia/Shanghai）SSH 现场检查。

| 正式数据集 | 逻辑字节 | 当前状态 |
|---|---:|---|
| OpenScene / NAVSIM | 3,044,931,711,532 B | 610/610 落地；609 个有上游 hash，1 个 size-only |
| nuPlan | 1,786,201,342,956 B | test 24/24 size+tar PASS；没有 raw trainval |
| nuScenes | 391,324,385,149 B | Core 13/13 tar/inventory PASS；扩展包 PASS |
| Bench2Drive | 418,508,847,603 B | v0.0.4 no-depth + maps，1112/1112 PASS |
| **合计** | **5,640,966,287,240 B** | **约 5.130 TiB** |

远端空间：`/mnt/nas` 现场显示总容量 10P、可用约 9.5P；空间不是当前阻塞。控制根仍有 69 个历史 `.part`、5 个 `.parts_*` 目录及 sidecar/evidence，不能凭目录名清理。

远端锁：以下 6 个零字节 `.lock` 均保留，现场没有对应 WAM 进程，不能把它们当活动锁或垃圾删除：

- `nuplan_v1.1_test_20260917.lock`
- `nuscenes_v1.0_core_current_20260916_nopromote.lock`
- `nuscenes_v1.0_core_current_20260917_resume_nopromote.lock`
- `soak_full_b.lock`
- `sup_s1.lock`
- `sup_s2.lock`

## 2. P0 现场复用审计

### 2.1 OpenScene v1.0 occupancy

OpenScene 官方说明 v1.0 trainval occupancy label 约 95.4 GB，并明确表示 v1.1 使用 occupancy 时仍需要 v1.0 label；v1.1 camera/LiDAR 不能替代该 label。

现场检查：

- `openscene` 下只有 `openscene-v1.1`、`navsim`、`navsim-v2`；
- `openscene-v1.1` 下只有 mini/test/trainval camera 和 LiDAR 目录；
- 对正式根目录和远端 inventory 搜索 `occupancy|label|v1.0` 未找到候选条目。

**P0 结论：目前按“缺失”处理，但仍需在实际源 listing 阶段确认具体 label 分卷和 MD5；不重复下载任何 v1.1 sensor。**

### 2.2 nuPlan trainval DB

当前 nuPlan 只有 test sensor blobs、mini DB/LiDAR、maps 和少量解包日志；没有 raw trainval DB。第三方统计不能替代 Motional 官方对象清单，因此：

- 不把约 1 TB 的第三方 DB 统计写成官方 manifest；
- 不因 ReactSim-Bench 的需求直接拉 >20 TB raw sensor；
- 先核对 ReactSim/论文实际需要的 trainval DB split，再决定是否只补 DB/metadata。

**P0 结论：nuPlan trainval 仍是待核 manifest，不进入本轮自动下载。**

## 3. 候选源审计与放行状态

### 3.1 建议进入 Phase 1 的低重复资产

| 候选 | 官方/作者证据 | 体量口径 | 许可/访问 | 与现有资产关系 | 前置状态 |
|---|---|---:|---|---|---|
| HUGSIM | HF `XDimLab/HUGSIM` | 60.7 GB；`scenes`、`3DRealCar`、`nusc_map_cache.zip`、`scenarios.zip` | HF 标 MIT，非 gated | 重建场景是新资产，不等于 raw nuScenes | **候选放行；需逐文件 listing、HEAD、hash** |
| OpenScene v1.0 occupancy | OpenScene 官方 getting-started | trainval label 约 95.4 GB | OpenScene CC BY-NC-SA + nuPlan Dataset Agreement | 只补 label，不重复 sensor | **现场缺失；需锁分卷/MD5/路径** |
| nuScenes-Occupancy | OpenOccupancy 官方 `prepare_data.md` | v0.1 约 5 GB 压缩、约 130 GB 解压；v0.0 deprecated | 官方 Google Drive/Baidu 链接；原始 nuScenes 条款仍适用 | 只补 occupancy label | **候选；下载链接和校验需现场探测** |
| Occ3D-nuScenes | Occ3D 官方 GitHub | train 600、val 150、test 250；官方页面未给 archive 总字节 | 代码/生成数据许可与 nuScenes 条款需分开核对 | 只补 occupancy GT，不重复 nuScenes raw | **条件候选；总字节和对象清单未锁** |
| OpenLane-V2 subset_A info | OpenDriveLab 官方 `data/README.md` | info 约 8.8 GB，MD5 `95bf28...` | CC BY-NC-SA 4.0；须同意 nuScenes/Argoverse 2 上游条款 | 先不下约 28.3 GB重复 images | **适合先做 manifest** |
| OpenLane-V2 Map Element Bucket | 同上 | 约 240 MB，MD5 `1c1f9d...` | 同上 | OmniDrive/topology 新标注 | **适合先做 manifest** |
| OmniDrive-nuScenes | NVlabs 官方 v1.0 release，2024-05-02 发布 | `data_nusc.zip` 约 885 MB（需以 release HEAD 为准）；社区 HF 镜像完整集合约 4.48 GB，含多个 pkl | NVIDIA research/non-commercial 口径需保留 | QA/反事实标注新；nuScenes raw 已有 | **先确认只下 QA 还是含 planning pkl** |
| DriveLM-nuScenes | OpenDriveLab 官方 docs | 训练 QA `v1_0_train_nus.json`；HF 全集合页面约 4.86 GB，含 subset images | 官方要求先填 form；CC BY-NC-SA 4.0 | annotation 新，subset image 可复用现有 nuScenes | **需账号/form 状态和 JSON 精确字节** |
| ReCogDrive_Pretraining | 作者 GitHub + HF `owl10/ReCogDrive_Pretraining` | 3.79 GB | HF 标 Apache-2.0，但各源数据条款仍适用 | 多源 rewritten QA 新，底层图像可能重复 | **候选；需确认文件组成和 license notice** |
| Talk2Car Slim | 官方 Talk2Car GitHub | `<2 GB` | 软件 MIT；数据/上游 nuScenes 条款需分开记录 | Slim 可独立使用，不需再拉 300GB+ nuScenes | **适合小批量；需下载链接 HEAD/MD5** |
| CityWalker teleportation subset | 官方 repo 指向 HF；HF 页面约 6.82 GB | 6.82 GB | 代码 Apache-2.0；dataset card 未充分说明原始视频/数据条款 | Metis 导航支线的新资产 | **候选但许可证需补证** |
| Adv-nuSc | HF `Pixtella/Adv-nuSc` dataset card | 15.6 GB；156 scenes/6115 samples；6 cameras | CC-BY-SA-4.0 | adversarial rendered video/轨迹是新资产 | **候选；需确认 revision、文件级 hash** |

### 3.2 P2 新分布资产

| 候选 | 官方现状 | 决策 |
|---|---|---|
| WOMD / Waymo Open Motion v1.3.1 | Waymo 当前下载页列出 v1.3.1；103,354 个 20s、10Hz segments、约 574h；官方不提供单一总字节；需登录并接受 Waymo non-commercial terms | **高价值但先做账号/条款/官方 GCS manifest；不先下载** |
| ProSim-Instruct-520k | 官方 ProSim repo 明确发布 raw prompts/motion tags，覆盖 WOMD train/val；需同时有 WOMD；总字节未锁 | **WOMD 落地后再做** |
| OpenDV-mini | 计划账给出 raw 44 GB，但本轮尚未完成官方对象 listing/许可重核 | **保留候选，不作为已放行 queue** |
| DrivingDojo | HF 283 GB；需要同意共享联系方式，页面标 Apache-2.0 | **P2；需 gated access 和对象 manifest** |
| CoVLA | HF 452 GB；>80h、10,000 个 30s clips；视频/CAN 受 CoVLA 条款，语言受 VideoLLaMA 2 条款；需同意共享联系方式 | **P2；不进入第一批** |

### 3.3 明确暂缓或不下载

- nuPlan native full raw trainval：20 TB 级，当前没有 exact reproduction 的最小模态证明；
- Bench2Drive v0.0.4 depth：约 7.35 TB，已有同版本 no-depth + maps；当前 WAM 主线不需要 depth/3D occupancy；
- OpenDV 全量 raw/processed frames：约 3 TB/24 TB，先做 mini；
- Waymo Perception raw：与 WOMD 不等价，当前论文主线先满足 motion/scenario；
- full nuScenes-C、KITTI-360、PandaSet、Lyft Level5、RiskBench：用途窄或重复高，等待具体论文任务。

## 4. 传输层和队列前置阻塞

### 4.1 210 直连探测

2026-09-21 在 210 对以下公共入口只做 HTTP HEAD/连接探测，没有请求大文件正文：

- `https://huggingface.co`
- `https://github.com`
- `https://drive.google.com`
- `https://waymo.com`

均返回 HTTP `000`/连接失败或超时。这个结果只证明“210 直接访问这些站点当前不可用”，不能推导镜像或签名字节域名一定不可用。后续必须对实际下载对象做：

1. Windows/API 取得当前 revision、对象列表和短命 URL；
2. 解析实际字节域名/CDN/edge；
3. 从 210 对同一对象做 HEAD 和有限 Range；
4. 记录 `Content-Length`、`ETag`、`Last-Modified`、HTTP 状态和实际返回字节；
5. 只有所有对象通过，才能生成 POSIX queue。

### 4.2 当前尚未满足的 queue gate

- HUGSIM、Occ3D、OmniDrive、DriveLM、Talk2Car、CityWalker、Adv-nuSc 尚未形成完整对象 manifest；
- 多个来源只有总量展示，没有逐对象 `Content-Length`/hash；
- Google Drive/Baidu/HF gated 对象可能需要登录或短期确认，不能把页面 URL 当稳定下载 URL；
- 目标路径、文件名冲突、压缩包实际容器和解压空间还未逐项冻结；
- 当前没有用户对某一批次的正式下载授权。

## 5. 建议的安全执行顺序

### Gate A：只读 manifest 探针

优先核查并生成候选 manifest，不下载正文：

1. OpenScene v1.0 occupancy label；
2. OpenLane-V2 subset_A info + Map Element Bucket；
3. OmniDrive `data_nusc.zip` 与 planning pkl 分开；
4. DriveLM 仅 `v1_0_train_nus.json`；
5. ReCogDrive annotation bundle；
6. Talk2Car Slim；
7. HUGSIM file listing；
8. nuScenes-Occupancy v0.1。

### Gate B：小批量下载候选

若 Gate A 全部满足对象、许可、路径和 210 字节通道要求，建议先做低风险小批量：

- OpenLane-V2 info + Map Element Bucket；
- OmniDrive QA；
- DriveLM JSON；
- ReCogDrive QA；
- Talk2Car Slim。

随后再决定 HUGSIM 60.7 GB 和 occupancy label 95.4 GB/nuScenes-Occupancy v0.1 5 GB。这样即使某个 HF/Drive 源失效，也不会影响整批任务。

### Gate C：WOMD

只有 Waymo 登录、条款、GCS listing、train/val 对象总数和精确字节冻结后，才建立 WOMD scenario queue；不把可选 LiDAR/camera embeddings 混进第一批。

### Gate D：下载后的串行验收

严格遵循本机 `文档/DOWNLOAD_SOP.md`：下载 → 独立 tar/hash/inventory → acceptance report → 用户确认 → no-clobber promote。任何“页面显示大小”“HTTP 200”“容器可读”都不能冒充 upstream checksum PASS。

## 6. 本轮阻塞与下一动作

当前阻塞不是磁盘空间，而是：

1. 210 直连公共站点不可用，实际 CDN/签名字节通道尚未验证；
2. 关键候选仍缺逐对象 manifest 和稳定 hash 证据；
3. Waymo/DriveLM/CoVLA/DrivingDojo 有账号、表单或 gated/license gate；
4. nuPlan trainval DB 是否需要，尚未被具体论文代码裁剪到最小 split；
5. 当前没有新下载授权。

本审计不启动下载。下一步应先在 Windows 侧建立**候选对象 manifest 探针**，再逐对象从 210 做 HEAD/Range；探针通过后再由用户明确选择 Gate B 的具体批次。

## 7. 官方/作者来源

- OpenScene: <https://github.com/OpenDriveLab/OpenScene/blob/main/docs/getting_started.md>
- OpenOccupancy / nuScenes-Occupancy: <https://github.com/JeffWang987/OpenOccupancy/blob/main/docs/prepare_data.md>
- Occ3D: <https://github.com/Tsinghua-MARS-Lab/Occ3D>
- OpenLane-V2 data: <https://github.com/OpenDriveLab/OpenLane-V2/blob/master/data/README.md>
- HUGSIM: <https://huggingface.co/datasets/XDimLab/HUGSIM>
- OmniDrive official release: <https://github.com/NVlabs/OmniDrive/releases/tag/v1.0>
- DriveLM data prep: <https://github.com/OpenDriveLab/DriveLM/blob/main/docs/data_prep_nus.md>
- ReCogDrive: <https://huggingface.co/datasets/owl10/ReCogDrive_Pretraining>
- Talk2Car: <https://github.com/talk2car/Talk2Car>
- CityWalker: <https://github.com/ai4ce/CityWalker>
- Adv-nuSc: <https://huggingface.co/datasets/Pixtella/Adv-nuSc>
- ReactSim-Bench: <https://github.com/Thinklab-SJTU/ReactSim-Bench>
- Waymo download: <https://waymo.com/open/download/>
- Waymo terms: <https://waymo.com/open/terms/>
- ProSim: <https://github.com/Ariostgx/ProSim>
