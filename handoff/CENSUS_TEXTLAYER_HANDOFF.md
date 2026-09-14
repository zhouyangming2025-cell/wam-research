# 交接文档：语料本地文本层（census1 批次 + 现状）

给项目所有者。写的是**语料现状与怎么用**，不是研究结论。所有数字由台账生成
（`scripts/build_handoff_doc.py`），不是手抄。

- 语料规模：**60 条记录**（P0001–P0060）
- 有本地 PDF + raw MD 文本层：**58 条**；无公开来源：2 条
- 文本层已发布到私有 GitHub 仓库（`origin/main`），clone 后可直接精读

## 0. 现在可以直接怎么用

| 你想做的事 | 打开这个 |
|---|---|
| 读正文（含图） | `papers/raw_md/P00XX_<短名>/P00XX_<短名>.raw.md` 与同级 `images/` |
| 看权威清单（谁在语料里、来源、哈希、标签） | `manifests/CORPUS_MANIFEST.csv`（60 行 × 25 列） |
| 看本批次的采集与核验细节 | `CENSUS_ROUND1_TEXTLAYER_INGEST_REPORT.md` |
| 看上一批次（覆盖空洞） | `CENSUS_ROUND2_INGEST_REPORT.md` |
| 复核某个数字从哪来 | `manifests/batch_*.json`（每步一份台账） |

## 1. 本次做的事：把 Round-1 已放置的作品补上本地文本层

你在 `landscape/CENSUS_PHASE_A_ROUND1.md` 里已经放置了约 45 篇，但其中 26 篇此前只有
条目、没有本地正文；要读就得临时联网抓 PDF。这批把这 26 篇补齐为：一条核验过的身份、
一份正典 PDF + 逻辑字节 SHA256、一次首页核验、一份可提取的 raw MD 与配图。

| id | 短名 | 官方标题 | 来源 | 页 | raw md 字符 |
|---|---|---|---|---:|---:|
| P0035 | GAIA1 | GAIA-1: A Generative World Model for Autonomous Driving | arXiv_v1 | 25 | 73066 |
| P0036 | DriveDreamer | DriveDreamer: Towards Real-world-driven World Models for Au... | arXiv_v2 | 15 | 61812 |
| P0037 | DriveWM | Driving into the Future: Multiview Visual Forecasting and P... | CVPR2024_camera_ready | 11 | 53322 |
| P0038 | Vista | Vista: A Generalizable Driving World Model with High Fideli... | arXiv_v5 | 31 | 102786 |
| P0039 | DriveDreamer2 | DriveDreamer-2: LLM-Enhanced World Models for Diverse Drivi... | arXiv_v2 | 24 | 60354 |
| P0040 | DrivingGPT | DrivingGPT: Unifying Driving World Modeling and Planning wi... | ICCV2025_camera_ready | 11 | 54571 |
| P0041 | PolicyWM | From Forecasting to Planning: Policy World Model for Collab... | arXiv_v2 | 20 | 69593 |
| P0042 | WorldDrive | Bridging Scene Generation and Planning: Driving with World ... | arXiv_v1 | 16 | 66254 |
| P0043 | OccWorld | OccWorld: Learning a 3D Occupancy World Model for Autonomou... | arXiv_v1 | 11 | 57359 |
| P0044 | DriveOccWorld | Driving in the Occupancy World: Vision-Centric 4D Occupancy... | arXiv_v3 | 18 | 87400 |
| P0045 | WoTE | End-to-End Driving with Online Trajectory Evaluation via BE... | ICCV2025_camera_ready | 10 | 53006 |
| P0046 | World4Drive | World4Drive: End-to-End Autonomous Driving via Intention-aw... | ICCV2025_camera_ready | 11 | 51081 |
| P0047 | DriveWorld | DriveWorld: 4D Pre-trained Scene Understanding via World Mo... | CVPR2024_camera_ready | 12 | 63648 |
| P0048 | LAW | Enhancing End-to-End Autonomous Driving with Latent World M... | arXiv_v2 | 18 | 58787 |
| P0049 | DriveJEPA | Drive-JEPA: Video JEPA Meets Multimodal Trajectory Distilla... | arXiv_v2 | 21 | 81841 |
| P0050 | WorldRFT | WorldRFT: Latent World Model Planning with Reinforcement Fi... | arXiv_v1 | 15 | 73734 |
| P0051 | AutoJEPA | Auto-JEPA: A Latent World Model of Continuous Intent for En... | arXiv_v1 | 12 | 62825 |
| P0052 | ReWorld | ReWorld: Representation Learning for World Action Models | arXiv_v2 | 15 | 83432 |
| P0053 | WAJEPA | WA-JEPA: Rethinking the Video JEPA Paradigm for World-Actio... | arXiv_v2 | 14 | 70274 |
| P0054 | WhatTrulyMatters | What Truly Matters in Trajectory Prediction for Autonomous ... | NeurIPS2023_camera_ready | 13 | 53244 |
| P0055 | SLEDGE | SLEDGE: Synthesizing Driving Environments with Generative M... | arXiv_v2 | 18 | 53064 |
| P0056 | DriveArena | DriveArena: A Closed-loop Generative Simulation Platform fo... | arXiv_v1 | 19 | 73497 |
| P0057 | UniAD | Planning-Oriented Autonomous Driving | CVPR2023_camera_ready | 10 | 59418 |
| P0058 | VAD | VAD: Vectorized Scene Representation for Efficient Autonomo... | ICCV2023_camera_ready | 11 | 52017 |
| P0059 | DiffusionDrive | DiffusionDrive: Truncated Diffusion Model for End-to-End Au... | CVPR2025_camera_ready | 11 | 53783 |
| P0060 | DrivoR | Driving on Registers | CVPR2026_camera_ready | 12 | 55801 |

此外 P0021–P0034（14 篇）是上一批“覆盖空洞”支持批次，同样有本地文本层。

## 2. 这 26 篇是怎么选出来的（机械化，不靠记忆）

1. `scripts/parse_census_works.py`：机械解析你的 census 表格行与 Round-1 来源登记表，减去
   语料里已有的记录；
2. `scripts/plan_census_acquisition.py`：按语料既定的来源优先级 **venue camera-ready >
   官方 arXiv > 项目页** 为每篇挑一份正典文档（CVF 论文页推导 PDF，NeurIPS/ICLR 页抽取 PDF
   链接）；
3. 每个候选 URL 先探测是否真返回 `%PDF-` 才下载；
4. 登记表只给项目页/仓库的 5 篇，走“发现 + 独立核验”：CVF 索引页扫标题（Drive-WM），或
   从作品自己的项目页/仓库里找官方 arXiv 链接，再到官方落地页核验标题（Drive-OccWorld、
   DriveArena、SLEDGE）。**项目页只是发现入口，永远不作为证据**；
5. **NPPC 仍未入库**：登记表记明它没有合法开放来源，这与 P0008 一直无 PDF 是同一原因。

## 3. 已核验的事实（可引用为事实的部分）

- 首页核验：26/26 `DOCUMENT_VERIFIED`（标题精确匹配 + 第一作者出现在首页），
  全库唯一 `PARTIAL` 是 P0027 Think2Drive 的标题分歧（见 §5.5）
- 转换 QC：26/26 `RAW_MD_READY`；替换乱码字符 **0**；配图 261 张，缺失 0 张
- 去重：45 个非空 arXiv ID **无一重复**；全库**无重复标题**；无 ID 复用或重编号
- 代码可得性按论文自述记录：`code_available=YES` 的 16 篇都印了仓库 URL；其余标 `UNKNOWN`（不印 URL ≠ 没有代码；项目页不算仓库）

## 4. 每个记录的元数据约定（读 manifest 前请先看这段）

- `hypothesis_tags=GENERAL`、`decision_relevance=LOW`：本批次定位是“让 census 可本地阅读”，
  不对决策相关性下判断；标签由固定词表在**作品自身标题与正文**中的计数机械得出，
  **不是**你的家族归属；
- `reading_status=RAW_MD_READY` 且 `NO_CARD`：这些是**放置深度**的文本层，没有做深读，
  因此没有生成论文卡片；
- `arxiv_id` 为空 ≠ 不存在 arXiv 版本：10 条 camera-ready 记录的落地页未印 arXiv 版本，
  留空表示“未记录/未显示”，不写成 `NONE`（那会变成一句我无法支撑的断言）；
- `code_available=UNKNOWN` 是“论文没有印仓库 URL”，不是“没有代码”。

## 5. 必须知道的坑（含我自己的失误，全部已修或已记录）

1. **MinerU 内存泄漏（本批次最大坑）**：每一篇转换结束后会残留一个约 1.7 GB 的 python
   进程；跑到第 12 篇时主机内存耗尽，`OpenBLAS … Memory allocation still failed` + 502，
   后续任务全部失败。对策：**小批量转换（每次 3 篇）+ 每批清理工作集 > 800 MB 的残留进程**。
   这不是文档问题，失败篇重试即成功。
2. **台账竞态**：两个 MinerU 进程并行时各自读一次台账再整体写回，后写者会静默丢掉前者的
   记录（census2 曾丢 6 条）。已修：写台账前重读；并保留 `scripts/repair_rawmd_ledger.py`
   可从磁盘产物忠实重建（本次重建 12 条，数值与原记录逐项吻合）。
3. **转换会丢文本**：P0028 ViDAR 首页印着的代码 URL 在 raw MD 里不存在。因此代码证据允许
   取自 PDF 首页并标注位置，避免“只看 markdown 就断言没代码”。
4. **参考文献里的第三方仓库会被误认**：GAIA-1 的扫描一度把参考文献中的 stable-diffusion
   WebUI 当成本文代码。已修：扫描先截断参考文献段。
5. **标题分歧（记录而非抹平）**：census 把 P0052 写作 “ReWorld: Learning Better”
   Representations for World Action Models”，官方记录是 “ReWorld: Representation Learning
   for World Action Models”。入库用**官方标题**，你的 census 文件**未改动**。
   P0027 Think2Drive 同类（arXiv 落地页 vs PDF 首页），入库用论文首页标题。
6. **无公开来源的记录**：P0008（NPPC，IEEE 付费无开放版）与 P0020（Bahram2016）没有 PDF，
   `library_status=NONE`，manifest 里明确标注，未用猜测链接填充。

## 6. 待你裁决（我按边界留给你）

1. **NPPC**：提供许可副本，或维持“已记录阻塞”。
2. **`decision_relevance=LOW` 的整批惯例**：若其中若干篇已是你的 anchor，请点名，我会把它记成
   你的判断（而不是我的）。
3. **词表缺口**：语料没有 vision-language / VLA 类标签，相关的 VLA 工作只能用最接近的词表标签
   （如 P0024 DriveVLM、P0025 OmniDrive、P0026 ORION）。是否扩词表由你定。
4. **census 措辞 vs 官方标题**：是否需要在 manifest 里同时保留 census 的写法（如 P0052）。

## 7. 环境与复现

```powershell
# 网络/PDF 一律用带 certifi 的解释器，否则 TLS 校验会失败
$mp = 'D:\Program Files\Mineru\venv\Scripts\python.exe'
$env:CORPUS_BATCH = 'census1'
$env:PYTHONIOENCODING = 'utf-8'
# MinerU 转换（必须串行 / 小批量；环境变量见 CENSUS_ROUND1_TEXTLAYER_INGEST_REPORT.md §12）
& $mp -u scripts\build_raw_md.py P0035,P0036,...,P0060
```

脚本分工：采集规划 `parse_census_works.py` / `plan_census_acquisition.py` /
`resolve_census_unresolved.py` / `resolve_census_via_discovery.py` / `apply_census1_plan.py`；
核验与入库 `fetch_work_identity.py` / `fetch_canonical_pdfs.py` / `verify_frontpage.py` /
`build_raw_md.py` / `build_census1_meta.py` / `build_manifest.py`；报告
`build_census1_report.py` / `build_handoff_doc.py`。

## 8. 我的边界（这一条也是交接内容）

本次工作只做：采集、身份核验、下载与哈希、转换、QC、元数据、台账与报告。**没有**做家族归属、
新颖性/缺口判断、方法设计或深读；**没有**编辑你的 `landscape/`、`state/`、`handoff/` 文件
（本文件是新建的交接说明，不是改写你的既有文件）。凡我无法用官方来源核验的东西，都留在
“未解决”里，而没有填成结论。
