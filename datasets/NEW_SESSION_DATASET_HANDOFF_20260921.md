# WAM 数据集下载：新会话接手单页（2026-09-21）

> 这是当前状态入口。新会话先读本文件，再读 `HANDOVER.md` 的历史细节和 `manifests/resource_inventory_20260921.md` 的现场盘点。旧文档中的数字和状态若与本文件冲突，以本文件和现场文件为准；历史经验不删除，但不得当作当前状态。

## 30 秒结论

- 210：`zhouyangming@10.199.4.210`；控制根：`/mnt/nas/planning/zhouyangming/wam`；正式数据根：`/mnt/nas/planning/zhouyangming/wam_datasets`。
- 正式数据池四个一级目录合计 **5,640,966,287,240 B ≈ 5.13 TiB**：OpenScene/NAVSIM 2.77 TiB、nuPlan 1.62 TiB、nuScenes 0.36 TiB、Bench2Drive 0.38 TiB。
- 当前没有 WAM 下载、监督器、验收、inventory 或 watcher 进程；没有活动锁。历史 lock、`.part`、sidecar、queue、日志和 evidence 必须保留。
- 正式数据根无 `.part`。控制根深度盘点仍有 69 个 `.part`（约 362.37 GiB）和 5 个 `.parts_*` 目录（约 5.31 GiB），不能凭目录名删除。
- nuScenes Core Full：13/13 已独立 tar/inventory 验收并以 no-clobber 方式进入正式根；官方 legacy MD5 字段未改。
- OpenScene：610/610 落地，1 个对象只有 size-only 证据；不要写成 610 个官方 hash 全通过。
- nuPlan：现有 test 24/24 仅通过尺寸 + tar 结构验收（队列无 upstream hash）；有 mini DB、mini LiDAR、maps 和一个 CAM_F0 解包日志，**没有 raw trainval camera/LiDAR**，不能称为 nuPlan Full。
- Bench2Drive v0.0.4 no-depth + map：1112/1112 SHA256/容器验收通过。

## 必读文件顺序

1. 本文件：`NEW_SESSION_DATASET_HANDOFF_20260921.md`
2. 历史完整交接：`HANDOVER.md`
3. 现场资源盘点：`manifests/resource_inventory_20260921.md`、`.tsv`、`.json`
4. 网络/下载唯一手册：`文档/下载通道测速实验报告_20260911.md`（当前有效经验看 v5.52–v5.54 和 §S；更早结论可能已废弃）
5. 控制根远端 inventory：`/mnt/nas/planning/zhouyangming/wam/cache/p2/wam_inventory_20260921.{json,tsv}`

## 当前数据与证据路径

| 数据集 | 正式数据路径 | 当前证据 |
|---|---|---|
| OpenScene/NAVSIM | `/mnt/nas/planning/zhouyangming/wam_datasets/openscene` | `/mnt/nas/planning/zhouyangming/wam/queue/soak_full_b_audit.json` |
| nuPlan | `/mnt/nas/planning/zhouyangming/wam_datasets/nuplan` | `/mnt/nas/planning/zhouyangming/wam/queue/nuplan_v1.1_test_20260917_acceptance_corrected.txt` |
| nuScenes | `/mnt/nas/planning/zhouyangming/wam_datasets/nuscenes` | `/mnt/nas/planning/zhouyangming/wam/queue/nuscenes_v1.0_core_current_20260917_resume_nopromote_acceptance.progress.json`；扩展包为 `nuscenes_extensions_20260918_acceptance.txt` |
| Bench2Drive | `/mnt/nas/planning/zhouyangming/wam_datasets/bench2drive` | `/mnt/nas/planning/zhouyangming/wam/queue/b2d_v004_20260919_resume_acceptance.txt` |

## 已验证的关键经验（以后必须复用）

### 1. 先读现场，不能读记忆

每次“现在怎么样”都必须现场检查：进程、锁、queue、JSONL、sidecar、目标文件、磁盘空间和最近日志。历史报告只能解释原因，不能代替当前状态。

### 2. Windows 只做发牌和 mint，210/NAS 才搬字节

- 本机工作根：`D:\zym_information\ZYM\wam`；负责 API、清单、签名 URL、CloudFront 边缘 IP、队列生成和代码部署。
- 210：负责实际 HTTP 字节流、分块续传、写 NAS、sidecar、监督器、验收。
- 210 不能直接访问某些 HF API/GCS/S3；不能因为 210 API 不通就断言字节路径不可用。
- 210 禁止写 `/tmp`、`/home`、`/`；所有控制产物写控制根下的既有目录。
- 不打印签名 URL、Cookie、Token；队列和日志中应脱敏。

### 3. 清单必须防截断、防路径错误

- 有 `TotalCount` 的接口：显式扩大分页并断言 `len(items) == TotalCount`，不一致就拒绝建队列。
- 没有总数的分卷枚举：连续多次缺失后才停止，并记录停止下标；不能遇到第一个缺失就停。
- Windows 生成 Linux 队列必须用 POSIX `/` 路径和绝对路径；运行前用 `queue_path_check.py`。字面反斜杠曾把 1.58 TiB 目标写成错误文件名。
- 队列是声明，不是事实：建队列后必须做尺寸、Range、路径、磁盘和认证预检；`--dry-run` 先于正式启动。

### 4. 源站和速度必须按对象、方法、时间窗记录

- ModelScope、CloudFront、HF/Xet 是不同源族；“210 API 不通”不等于 210 不能搬字节。
- CloudFront 边缘 IP 会轮换，签名 URL 会过期；每次启动前重新 mint/解析/验证，不能复用旧队列中的地址或签名。
- 60 MiB/s 是 limiter 上限，不是源站保证速度。历史 25.9–68.3 MiB/s 只适用于对应对象、Range 方法和时间窗，不能跨对象套用。
- 测速至少固定对象、请求方法、并发、分块大小和墙钟窗口；不要以一次短请求宣称全程速度。
- 同时变慢时先排查 210→CloudFront 路径/边缘状态，不要先归因单个 archive。

### 5. 一个作业一个 owner，下载不能和验收并发

- 同一 queue 只能有一个 downloader/supervisor；lock 是互斥，不是删除目标。
- 长跑挂监督器，使用 TERM 停止并记录 `process_stop`；不要 `kill -9`，不要把“进程退出”自动当成功。
- 单个作业 403 不应取消整条健康队列；无效签名作业隔离，其他作业继续。
- 下载、tar/inventory、重型验收不能并发；实测会争用入站和磁盘，导致吞吐显著下降。

### 6. 状态字段和验收必须分层

- sidecar 是断点/进度权威；JSONL、supervisor log、progress、sidecar 必须一起保留。
- 官方 legacy MD5、当前对象 MD5、本地 SHA256、ETag、尺寸是不同字段，不能互相覆盖或推断等价。
- 十六进制 MD5 不能直接当 Base64 verifier 输入。
- “下载完成”≠“tar/inventory 通过”≠“promote”。`--no-promote` 后仍必须独立验收。
- 文件名叫 `.zip` 不代表一定是 ZIP；nuPlan test 对象实际为 POSIX tar，必须按 magic/container 实测判断。
- upstream hash 缺失时只能报告 size+结构验收，不能升级成官方 checksum PASS。
- no-promote 模式下不要用 final 数量判断进度；以 queue JSONL 的 `verify ok`/`skip_exists`、sidecar 和实际 `.part` 状态为准。
- promote 只允许用户明确确认后执行，并采用 atomic no-clobber；保留源文件和完整证据。

### 7. 目录与清理纪律

- 正式数据、控制证据、历史 backup、研究仓库是不同类别；不要按目录名猜用途。
- 不移动、不删除、不重命名历史证据；候选重复必须先 hash、建 manifest、用户确认。
- `du`、文件 walk、硬链接/重复文件是不同统计口径；资源总账要明确口径，不能把混合统计当物理唯一占用。
- 0 字节 lock/test fixture、`.parts_*`、失败队列和 sidecar 不是自动垃圾。
- 不修改非 WAM 目录；不创建 Git commit/push，除非用户明确要求。本次用户已明确要求同步报告时才推送仓库。

## 新数据集的安全 SOP

1. 只读核对目标、授权、官方清单、Content-Length、ETag/Last-Modified、checksum 来源和更新日期。
2. 判断 Windows mint / 210 搬运路线，发起小 Range 探针；记录 HTTP 206、Content-Range、实际速率和边缘。
3. 生成队列：POSIX 绝对路径、尺寸、分块、并发、上游校验字段、源类型、run tag；断言清单完整。
4. 上传脚本到 210 后逐位核对远端 SHA256；先跑 path check、preflight、dry-run。
5. 用户明确授权后启动唯一 downloader + supervisor；保存 queue、JSONL、sidecar、progress、日志和锁。
6. 停止下载后再做独立 size/hash/container/tar/inventory 验收；形成 acceptance report。
7. 用户明确确认后才 no-clobber promote；post-promote 再核对 inode/size/manifest。
8. 任何 checksum、尺寸、容器、权限或路径证据缺失，都停在只读状态，不降低验收标准。

## 目前不要自动做的事

- 不自动恢复任何旧 queue；
- 不启动 nuPlan trainval/raw 下载；现场没有 raw trainval 清单和可靠总量；
- 不把 nuPlan 现有 1.62 TiB 称为 Full；
- 不重新生成 nuScenes Core 队列；
- 不删除控制根 `.part`、sidecar、历史 lock、日志、backup/evidence；
- 不把本地/远端报告数字写回官方 checksum 字段；
- 不在下载并发时做深度验收或 inventory；
- 不凭“大小正常”宣布完整。

## 交接结束条件

新会话在采取任何动作前，应先回答：

1. 现场进程/锁是否为空；
2. 目标数据属于正式 final、控制 `.part`、archive、sidecar 还是 evidence；
3. source adapter、mint 位置、210 字节路线和当前边缘是否重新验证；
4. queue 清单是否完整且 POSIX 路径正确；
5. 验收证据是 upstream hash、size-only、tar/container，还是尚未验收；
6. 用户本轮是否明确授权下载、验收或 promote。

回答不完整时，保持只读，不启动任务。
