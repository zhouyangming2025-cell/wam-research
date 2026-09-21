# WAM 数据集资源盘点（2026-09-21）

## 结论

本盘点是 2026-09-21 对 Windows 工作根和 210（`10.199.4.210`）的只读现场盘点。没有启动下载、验收、inventory watcher，也没有删除、移动、重命名或 promote 任何文件。

210 正式数据根 `/mnt/nas/planning/zhouyangming/wam_datasets` 当前有四个一级数据集目录。按四个目录最新 `du -sb` 的字节相加，逻辑占用为 **5,640,966,287,240 B（约 5.13 TiB）**。这比 `wam_inventory.py` 的 `5.66 TiB` 混合汇总更适合作为总账；后者同时混用了文件 walk 和目录 `du`，可能把目录树重复计入，本报告不采用它作为总量。

| 数据集 | 逻辑字节 | 约 TiB | 当前内容 | 现场状态 |
|---|---:|---:|---|---|
| OpenScene / NAVSIM | 3,044,931,711,532 | 2.77 | OpenScene v1.1、NAVSIM、NAVSIM v2 | 610/610 落地；609 个有上游 hash，1 个仅 size-only |
| nuPlan | 1,786,201,342,956 | 1.62 | test sensor blobs、mini DB、mini LiDAR、maps、1 个已解包 CAM_F0 日志 | test 24/24 size+tar PASS；无上游 hash 验证；没有 raw trainval |
| nuScenes | 391,324,385,149 | 0.36 | Core Full 13 archive、CAN bus、Map Expansion v1.3、camera supplement | Core 13 项 tar/inventory PASS；扩展包 ZIP PASS；正式根无 `.part` |
| Bench2Drive | 418,508,847,603 | 0.38 | v0.0.4 no-depth、v0.0.4 map | 1112/1112 SHA256/容器验收 PASS |
| **合计** | **5,640,966,287,240** | **5.13** | 只统计正式数据根四个一级目录 | 无活动下载/验收/inventory 进程 |

## 1. OpenScene / NAVSIM

根目录：`/mnt/nas/planning/zhouyangming/wam_datasets/openscene`

| 子集 | 字节 | 约 GiB/TiB | 说明 |
|---|---:|---:|---|
| `openscene-v1.1` | 2,545,682,394,232 | 2.37 TiB | trainval/test/mini metadata、camera、LiDAR 及清单；610 个 payload/sidecar 对应长跑队列 |
| `navsim` | 449,007,425,603 | 418.22 GiB | NAVSIM 当前/历史 sensor 包及 sidecar |
| `navsim-v2` | 50,241,887,601 | 46.79 GiB | navhard two-stage current/history、scene pickles、private-test-hard、warmup |

文件统计（正式目录）：1218 个文件，其中 609 个 payload/archive、609 个 sidecar；`.part` 为 0。

验收证据：`/mnt/nas/planning/zhouyangming/wam/queue/soak_full_b_audit.json`。610/610 文件落地、缺失 0、size_bad 0、sha_bad 0、tar_bad 0、zip_bad 0；其中 `v1.0-trainval01_blobs_camera.tgz` 没有上游 hash，只能标记为 size-only。因此该证据的精确表述是“全量落地且结构/尺寸通过，1 个 size-only”，不能写成 610 个上游 hash 全通过。

## 2. nuPlan

根目录：`/mnt/nas/planning/zhouyangming/wam_datasets/nuplan`

| 子集 | 字节 | 说明 |
|---|---:|---|
| `v1.1/sensor_blobs` | 1,696,354,370,715 | `test_set` 24 个归档 + sidecar，以及 1 个已解包 CAM_F0 日志 |
| `v1.1/splits` | 14,351,192,064 | mini split 的 64 个 DB 文件 |
| `nuplan-v1.1_mini_lidar_0.zip` | 74,069,152,445 | mini LiDAR archive |
| `maps` | 1,426,619,540 | maps/v1.0 地图包 |

`sensor_blobs/test_set` 为 1,695,274,394,424 B，24 个归档和 24 个 sidecar；已解包单日志 `2021.05.12.22.00.38_veh-35_01008_01518` 为 1,079,972,195 B，只有 `CAM_F0` JPG。当前正式根没有发现 raw trainval camera/LiDAR archive；因此不能把现有 1.62 TiB 叫作 nuPlan Full。

验收证据：`/mnt/nas/planning/zhouyangming/wam/queue/nuplan_v1.1_test_20260917_acceptance_corrected.txt`。24/24 文件尺寸一致、24/24 tar 扫描返回 0、缺失 0；队列没有 upstream checksum，所以这是 **PASS_TAR_STRUCTURE_SIZE**，不是 upstream-hash acceptance。原先 ZIP 解析失败是对象实际为 POSIX tar、文件名却以 `.zip` 结尾导致的格式误报。

## 3. nuScenes

根目录：`/mnt/nas/planning/zhouyangming/wam_datasets/nuscenes`

| 子集 | 字节 | 说明 |
|---|---:|---|
| `v1.0` Core Full | 372,554,105,065 | 13 个 Core archive |
| `v1.0-trainval01_blobs_camera.tgz` | 17,590,765,342 | 独立 camera supplement |
| `nuScenes-map-expansion-v1.3.zip` | 398,535,531 | 13 个 zip member |
| `can_bus.zip` | 780,974,697 | 7,834 个 member |
| 三个 sidecar | 418 | 不计入 payload |

扩展包证据：`/mnt/nas/planning/zhouyangming/wam/queue/nuscenes_extensions_20260918_acceptance.txt`，CAN bus 和 Map Expansion 均 PASS；分别为 7,834 和 13 个 member，CRC 未报错。

Core Full 的独立验收进度：`/mnt/nas/planning/zhouyangming/wam/queue/nuscenes_v1.0_core_current_20260917_resume_nopromote_acceptance.progress.json`。13/13 对象 size 一致、tar return code 0、路径安全检查通过、member inventory 已生成。正式数据根中的 13 个 payload 是 final；控制根仍保留对应 `.part`/queue/sidecar/日志作为运行证据，不能混为正式数据或直接删除。

## 4. Bench2Drive

根目录：`/mnt/nas/planning/zhouyangming/wam_datasets/bench2drive`

| 子集 | 字节 | 文件结构 |
|---|---:|---|
| `v0.0.4_no_depth` | 415,362,512,861 | 1100 个 tar.gz payload + 1100 个 sidecar |
| `v0.0.4_map` | 3,146,330,646 | 12 个 Town HD map `.npz` + 12 个 sidecar |

验收证据：`/mnt/nas/planning/zhouyangming/wam/queue/b2d_v004_20260919_resume_acceptance.txt`。1112/1112 文件落地，缺失 0、size_bad 0、sha_bad 0、tar_bad 0、zip_bad 0；结论 `ALL_LANDED_FILES_OK`。

## 5. 210 控制根与证据

控制根：`/mnt/nas/planning/zhouyangming/wam`。本次深度 inventory 产物：

- `/mnt/nas/planning/zhouyangming/wam/cache/p2/wam_inventory_20260921.json`
- `/mnt/nas/planning/zhouyangming/wam/cache/p2/wam_inventory_20260921.tsv`

控制根主要占用：`archives` 约 404.48 GiB、`backup` 约 79.79 GiB、`cache` 约 12.15 GiB、`checkpoints` 约 20.54 GiB、`queue` 约 9.59 GiB；这些不是正式数据根，不应并入 5.13 TiB 数据池。

深度扫描发现 5 个 `.parts_*` 目录（约 5.31 GiB）和 69 个 `.part` 文件（约 362.37 GiB，包含历史 backup/evidence）。它们是控制面残留、失败/恢复证据或未 promote 中间产物；本轮没有删除、移动、重命名或覆盖它们。历史 lock 文件也继续保留，但现场没有活动进程。

深度扫描还发现 5 组“同 basename+同 size”的候选重复文件。这只是候选重复，不等于内容 hash 相同，不能据此删除。

另有 2028 个 0 字节文件，主要位于 backup/evidence、锁和测试夹具路径；0 字节本身不是删除依据，均保留原位。

## 6. 本机工作根（不计入数据池）

`D:\zym_information\ZYM\wam` 共约 40,486 个文件、8,521,551,341 B。主要目录：

| 目录 | 文件数 | 字节 | 定性 |
|---|---:|---:|---|
| `research_assets` | 8,981 | 2,976,066,533 | Git 研究仓库、脚本、清单和论文资产；不是正式 payload |
| `论文调研` | 26,959 | 2,012,376,505 | 历史调研资料；不属于下载数据 |
| `workspace` | 4,062 | 1,308,686,763 | 历史项目工作区；不属于下载数据 |
| `backup` | 23 | 2,201,930,278 | 本地备份/证据；不属于正式数据 |

这些目录按 `AGENTS.md` 要求保留原位，不纳入 210 正式数据总账，也没有在本轮整理。

## 7. 当前可用结论

1. 已有正式数据池约 **5.13 TiB**，不是 5.66 TiB；后者是混合统计口径。
2. OpenScene 是最大组成部分（约 2.77 TiB）；nuPlan 现有的是 test/mini/maps，**缺 raw trainval**。
3. nuScenes Core、扩展包和 Bench2Drive 已有独立证据；nuPlan test 只有尺寸+tar 结构验收；OpenScene 有 1 个 size-only 文件。
4. 正式数据根无 `.part`；控制根 `.part`、sidecar、queue、日志和历史锁证据完整保留。
5. 当前无下载、验收、inventory、watcher 进程；本盘点完成后不应自动恢复任何下载。

## 8. 证据和口径限制

- 本报告统计的是路径逻辑占用，不是去重后的物理块占用；尚未进行全树内容 hash 去重。
- 报告不把“尺寸一致”写成“官方 checksum 通过”。各数据集的 checksum/结构验收范围已在对应章节单独标明。
- 本报告只记录现场事实，不改变 manifest、官方 MD5 字段、队列或正式数据文件。
