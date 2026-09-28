# 22 篇 WAM / WAM+VLA 数据集与容量审计：过程、修正及当前结论

审计日期：2026-09-28。范围是仓库固定 12 篇 planning-centric WAM / 一段式论文，加 10 篇 WAM+VLA 论文；论文源固定在 `wam-research` 提交 [`cb05048dfb822e95d44e52dd85b830c750411e2c`](https://github.com/zhouyangming2025-cell/wam-research/tree/cb05048dfb822e95d44e52dd85b830c750411e2c/papers/raw_md)。本记录补充仓库已有的 65 篇领域 census 与 2026-09-21 数据资产 inventory，范围更窄、目标是把这 22 篇论文的数据依赖及容量缺口查清；它不替代仓库当前正式资产 inventory、下载 plan 或 `state/NEXT_TASK.md`。

## 交付文件与定位

- [22 篇论文逐篇数据资产账本](WAM_22_dataset_asset_register_2026-09-28.md)：逐篇训练/预训练、微调、评测数据；父数据/派生包/annotation 与独立媒体的关系；当前已知容量、证据和未闭合项；高概率与可定价组合的算术。
- [nuPlan v1.1 官方对象 byte manifest](nuplan_v1_1_official_file_manifest_2026-09-28.md)：从官方 S3 对象 `Size` 字段得到的 169 项精确压缩容量。
- [OpenScene v1.1 官方文件级 manifest](openscene_v1_1_official_file_manifest_2026-09-28.md)：官方固定 revision 下 540 个对象，另附 [逐文件 TSV](openscene_v1_1_official_file_manifest_2026-09-28.tsv)；用于消解官方页面与历史目录 inventory 的口径差。
- 已有背景资产不重复抄写：[65 篇数据集 census](../../audits/datasets/wam_field_dataset_census_20260921.md)、[2026-09-21 资产 inventory](../../datasets/resource_inventory_20260921.md)、[nuPlan/OpenScene/NAVSIM 血缘审计](../../audits/datasets/NUPLAN_DATASET_AUDIT.md)。

## 用户目标和审计口径如何收敛

用户的目标不是总结论文，而是为 planning-centric WAM 与 WAM+VLA 建立可核验的数据底账，并最终给出两个集合：① 22 篇论文实际涉及的全部数据资产；② 研究上高概率会用到的数据资产。用户指出“高概率”是理论上的复用优先级，不代表马上下载，不能因为 nuPlan 超过 20 TB 就把它排除；也不能只写 nuPlan、OpenScene/NAVSIM、nuScenes、CARLA/Bench2Drive 四个大类而省掉 VLA 的专有视频、QA、指令、通用视觉数据。

因此本文按以下字段审计：论文 ID 与角色（training / pretraining / finetuning / evaluation）；数据集名、版本、split、模态；论文是否明确实际使用；它是原始观测、benchmark protocol、重标注/QA 还是可复用重建场景；上游母体及可确定的重复关系；官方/作者发布容量；容量是精确 byte、网页取整、估算还是 UNKNOWN；压缩包、解压目录和峰值占用分别是什么。

标签：**【原文事实】**表示论文原文、作者发布或官方资料明确支持；**【inventory事实】**表示已有项目 byte-level asset inventory；**【分析判断】**表示跨论文复用、去重、容量场景的推断；**UNKNOWN**表示源清单/字节或精确映射缺失。提及 Related Work 不算“论文使用”；作者生成的普通 cache、checkpoint 或 feature 不自动等同新原始数据集；如果作者将其命名并公开为可复用 benchmark，则单独登记。

## 本轮全过程记录

### 阶段 0：研究底座已存在（2026-09-19 至 2026-09-21）

**【已有仓库事实】**仓库已经有 nuPlan/OpenScene/NAVSIM 的分层血缘审计，说明 nuPlan 是原始规划日志与传感器母体，OpenScene 按约 2 Hz 重组/下采样，NAVSIM 再按 scene filter 选样并提供 PDMS/EPDMS benchmark。已有 65 篇论文 census 也强调不能只看四个主干数据集：WOMD、HUGSIM、OpenDV、CoVLA、DrivingDojo、语言/QA、地图/占用、仿真与私有数据都可能构成不同的复现资产。仓库还有一份 2026-09-21 资产 inventory，其中列出 OpenScene/NAVSIM、nuScenes、Bench2Drive、nuPlan 的已核验数据包 byte；它是数据大小的历史证据，不是本轮对 NAS 的重新检查。

### 阶段 1：范围确定为 22 篇（2026-09-28）

**【原文范围】**固定 WAM 12 篇：Epona、DriveLaW、WorldDrive、WoTE、World4Drive、LAW、Drive-JEPA、SeerDrive、Metis、DynFlowDrive、Discrete-WAM、GraphWorld。WAM+VLA 10 篇：DriveWorld-VLA、Uni-World VLA、SGDrive、FutureSightDrive、DriveVLA-W0、CoT4AD、WAM-Flow、ExploreVLA、UniDriveVLA、UniDrive-WM。逐篇入口、训练/评测项和行级原文链接见资产账本。

这不是仓库全部 65 个论文条目的新统计；频次也只对上述 22 篇计算。仓库主分支 `main` 当前停在源论文导入提交 `cb05048...`。仓库 `state/NEXT_TASK.md` 仍把 BridgeSim 标为当前下一任务；本审计是用户明确要求的数据专项证据，不更改科学工作流状态。

### 阶段 2：纠正前几轮审计的问题

此前的初步答复把“常见数据集”过快收敛成四个家族，未完成逐篇清单，尤其没有覆盖 WAM+VLA 的 ReCogDrive、多源驾驶 QA、LingoQA、DriveLM、OmniDrive、SGDrive、FineVision、CoVLA、DrivingDojo、HUGSIM、DriveBench、Chat-B2D 等；也没有把“论文提到”“论文实际训练/评测”“完整发布包大小”“论文真实抽样量”区分开。nuPlan 虽然昂贵且不一定近期下载，却被遗漏在高概率理论清单之外。旧估算又把网页标称、GB/GiB、当地 inventory、不同 Bench2Drive 版本和派生 NAVSIM 包混在一起，造成小数很多而证据精度不足的总数。

这些问题的实质不是“少找了几个数字”，而是没有逐论文回到原文、没有以具体版本/分卷列资产、没有沿数据 lineage 去重，也没有单独跟踪 annotation 对原始媒体的依赖。后续步骤据此重做，而非把旧总数当成基线。

### 阶段 3：逐篇复核 22 篇论文并区分数据角色

**【原文事实】**论文依据是版本固定的 `papers/raw_md/`，逐篇把训练、视频/世界模型预训练、planner finetune、open-loop/closed-loop 验证、消融集和私有数据拆开。结果显示常见规划基准仍然是 NAVSIM 与 nuScenes，但存在显著独立分支：nuPlan 高时频视频/日志、旧版 Bench2Drive、Drive-JEPA 的 CoVLA 与 DrivingDojo、CityWalker teleoperation、HUGSIM 重建场景、多个 VLM/QA/语言数据和私有驾驶视频。不是“所有论文都只用四个原始传感器集”。

**【分析统计】**在限定的 22 篇中，NAVSIM 出现 19/22、nuScenes 15/22、直接 nuPlan 7/22、旧 Bench2Drive 7/22；LAW 独立 CARLA 专家数据为 1/22。这里的“直接 nuPlan 7 篇”不包含通过 OpenScene/NAVSIM 间接继承的 nuPlan 场景。频次不等于应重复下载次数，也不等于每篇读取全 split。

VLA 侧不能把“有语言”简化成多一种语义输入。容量审计单独追问：语言样本来自何处、JSONL 是否包含图片、路径依赖哪一套上游媒体、数据是否是图片级还是视频级、某个论文是否实际使用完整发布语料。比如 ReCogDrive 的 3.79 GB 是重写 QA/轨迹 annotation 包，不等于 12 个来源的所有原图；WAM-Flow 披露的 3.4M 通用 VQA 图像也不等于作者约 414 MB SFT 子目录；FineVision 的整库体量不等于 UniDriveVLA 实际抽取体量。

### 阶段 4：拆数据血缘、版本和重复包

**【原文/官方事实】**OpenScene 是 nuPlan 派生传感器母体；NAVSIM v1 `navtrain` 是 OpenScene trainval 的 scene filter，NAVSIM `navtest` 在 OpenScene test 上过滤；NAVSIM v2 navhard two-stage 又增加 synthetic candidate state/传感器资产。因此选择完整 OpenScene 父体时，不把 navtrain 445 GB 的相同逻辑场景内容再次当“必需新增信息”；若要同时保留官方 navtrain archive，压缩文件实际重叠尚未 hash 验证，需另计一个交付包场景。

Bench2Drive 按版本拆开：早期论文中的 Base/v0.0.3 不等于现行 v0.0.4 no-depth。Full 4 TB 和 7.3 TB depth 包没有足够的 22 篇论文证据，不会仅因 benchmark 名相同而混入主总量。CARLA 闭环评测的 route/scenario XML 是协议，运行中观测由 simulator 产生；它不等于有一个同体量预录“测试视频集”。LAW 的 189K 帧 CARLA/Roach 是独立采集，不能由 Bench2Drive Base 替代。

nuScenes Core Full 与 QA/benchmark 子集也采用母体依赖思路；DriveLM/OmniDrive/ReCogDrive annotation 可能伴随图片，也可能要求从 nuScenes 根读取同一图像。没有文件级哈希/路径映射就不声明它们完全重复或完全独立。

### 阶段 5：逐项核发布体量、而不是把样本数换算成 TB

按作者/官方 dataset 页面、Hugging Face、Zenodo、CARLA/Bench2Drive、项目 source 等逐条核可见发布包；逐篇具体值和 URL 已放在资产账本。关键区别：

- 论文披露“hours / frames / QA rows / clips”是使用量信息，不足以推断压缩字节；分辨率、频率、图像格式、是否多视角、音视频 codec 和 cache 均会改变体量。
- JSONL/Parquet annotation 容量不含未嵌入的图片/视频；数据路径可引用其他母体。
- 官网列“dataset size”可能是格式化取整数；公开模型仓库的总 size 还可能包含 checkpoint，不能直接作为数据集大小。
- 下载 archive bytes、展开后的文件 bytes、解压临时目录/重复 cache 的峰值不是同一个需求。当前容量账本主项以 archive/公开托管 package 为主；没有把未验证的展开系数乘进总量。

### 阶段 6：单独关闭最大不确定项 nuPlan（2026-09-28）

旧调查从 S3 Explorer 逐 split 记录了 169 个对象名，页面只显示取整 GB/MB。先前因此把容量写成十进制 18.886 TB 或 GiB 解释约 20.279 TB 两种假设，不能据此做盘决策。

本轮从 Motional 官方 S3 的公开 `ListObjectsV2` 获取固定前缀 `public/nuplan-v1.1/`，响应 `IsTruncated=false`，共 170 个 key。排除历史 v1.0 map 后，对其余 169 个对象逐个读取 XML `Size` 的整数 byte。并对测试 DB 对象发出 HTTP HEAD，`Content-Length=95,919,476,643`，与 list size 相等。由此确定：

- **169 个 v1.1 发布对象总压缩体积：20,280,630,002,024 B =20.280630002024 TB =18.445125535 TiB。**
- 含 mini debug split；排除 mini 的其他 149 个对象共 **19,187,050,050,161 B =19.187050050161 TB**。
- 这解决了发布压缩对象 GB/GiB 语义猜测；以前的 18.886–20.279 TB 区间已作废。按官方对象字节而不是 UI 取整值计。
- 该数是公开 v1.1 package 清单合计，不是展开后的 sensor bytes、不经过 scene/hash 去重的“独立内容字节”，也不是 22 篇每篇都需要的最小 nuPlan 子集。

逐对象表和 exact sum 在 [nuPlan 文件清单](nuplan_v1_1_official_file_manifest_2026-09-28.md)。OpenScene 官方文档也把 nuPlan sensor data 描述为超过 20 TB，并列出 OpenScene v1.1 trainval/test sensors 约 2 TB、trainval camera 1.1 TB 与 LiDAR 822 GB；这支持“OpenScene 不是 raw nuPlan 等价物”的版本边界，但 publisher displayed units 和我们的对象 `Size` 不应混算。见 [OpenScene 官方数据表](https://github.com/OpenDriveLab/OpenScene/blob/main/docs/getting_started.md#download-data)。

### 阶段 7：重算 high / all 的条件容量和

以下数字保留首次提交时的历史计算过程；**现行口径见阶段 8 与资产账本**，不可将本段当最终容量表。

高概率资产定义为频次高或明确支撑多个 WAM/WAM+VLA 复现路线的组合，而非近期下载队列。主情景保留完整 nuPlan、OpenScene 父体、NAVSIM v2 synthetic 包、nuScenes、旧 Bench2Drive Base 与现行 v0.0.4，再加 VLA 的多个小 annotation 包。基于当前可核容量，资产账本给出：

- **high 条件组合：nuPlan 20.280630002024 TB + 其余 3.816689510071 TB =24.097319512095 TB。**
- **更广的已定价 package 组合：nuPlan +其余 9.346248010071 TB =29.626878012095 TB。** 这个情景把 CoVLA、DrivingDojo、FineVision 整库、HUGSIM、Adv-nuSc、CityWalker、Chat-B2D、LingoQA 等加入；FineVision 整库可能明显高估论文所取子集。
- **ThinkTwice 同为 189K CARLA 帧的约 8 TB**仅为 LAW 体量敏感性参照：若加到第二情景，算术和为约 37.626878012095 TB；绝不是 LAW 的实测数或合理上限。
- 若另存一份 NAVSIM v1 navtrain 压缩包，项目历史 inventory 是 449,007,425,603 B（约0.449007425603 TB）；主组合按 OpenScene 父体逻辑去重未另加。若 OpenScene 官方标称 2.28056 TB 取代历史 archive inventory 2.545682394232 TB，则组合需减去约0.265122394232 TB；两者冲突待复核。

这些是**已标价发布包的条件和**，不是“全部数据 exact 总量”，不构成有证明的下界或上限。公开/私有媒体尚有 UNKNOWN；包与包之间图片重复未校验；某些完整仓库大小是论文子采样的上界而非论文实际读取量。故目前不能据此宣称 32 TB / 40 TB / 64 TB 中任何一个容量已足以覆盖全部路线，也不能把 37.63 TB 当完整场景上限。

## 当前资产地图：纳入/排除原则

**已纳入或单独显式列出**：nuPlan v1.1；OpenScene v1.1 的六类 sensor 与 metadata；NAVSIM v1/v2；nuScenes 主体及扩展；旧 Bench2Drive Base 与当前 v0.0.4 no-depth；LAW CARLA 独立集；CoVLA、DrivingDojo、ReCogDrive；DriveLM、OmniDrive、SGDrive、UniDriveVLA 标注；FineVision、HUGSIM、CityWalker、Adv-nuSc、LingoQA、Chat-B2D；DriveBench 全量、nuScenes-C、DRAMA、SUTD、WAM-Flow 通用 VQA 等 UNKNOWN 项；DriveVLA-W0 私有数据另标不可公开定价。逐篇核对请看资产账本，不以本段名单代替逐项表。

**没有作为 22 篇数据需要直接计入**：只在 Related Work/引用中出现的项目；用户当前 22 篇论文没有明确使用的 OpenScene private-test wm/e2e 包；Bench2Drive Full 与 depth mega package；HUGSIM 依赖的 KITTI-360、Waymo、PandaSet 原始全库（论文使用 HUGSIM 四域并不能推出要下载源域全量）；WAM 模型训练产生的 checkpoint、latent/cache、常规临时文件。一个更广的 65 篇领域 census 会另外登记部分此类数据，那是不同范围。

## 当前结论与后续 closure gate

**【当前可确认】**已完成 22 篇范围内逐篇数据入口表、父/子 lineage 区分，以及 nuPlan 官方对象逐项 byte；后续已取 OpenScene 官方固定 revision 的 540 项文件级 `size`，见阶段 8。**【仍未确认】**全量 22 篇数据盘需求不是闭合数字：LAW CARLA 原始资产、VLA QA 源媒体映射、WAM-Flow 3.4M 图像、GraphWorld/DriveBench corruption、部分 benchmark 子集和私有 W0 仍缺可匹配的文件级 bytes。完整资产目录是现在的可复核产物，不等于容量审计已全部关闭。

要把容量审计关闭，下一轮必须按账本 UNKNOWN 行逐个获取官方文件 manifest / API `Size` / `Content-Length`，并把每个 paper 的路径抽取到源媒体 ID；一项一行记录 `asset_id, paper_id, role, version, split, modality, shard, exact_bytes, source, duplicate_of, public/private, compressed/unpacked`。接着分别计算：（a）高概率最小可复现组合，（b）22 篇全部公开原始数据/标注/评测协议组合，（c）私有数据的独立 UNKNOWN，不允许以公开替代。对于父体和派生 archive，用相同文件 SHA 或上游 object ID 去重；对无 hash 的重叠只给独立下载包情景与逻辑去重情景两列。最后由 zip/tar central directory 或公开解包 byte 数计算展开与峰值需求。

本轮只读公共项目论文文件、公开网站与官方 object metadata；没有检查 NAS 现场、没有下载数据包、没有解压/搬移/删除数据、没有修改资产 inventory 或当前 scientific state。仓库提交本审计材料后仍须以文档所列 UNKNOWN 为未决事项继续审计。

## 阶段 8：官方 OpenScene 清单与专项缺口推进（2026-09-28，后续提交）

【官方文件事实】固定 `OpenDriveLab/OpenScene` HF revision `a76f840b65e972bc45e56c2adced897498e9a026`，分页读取 620 个条目，筛出 `openscene-v1.1/` 540 个文件；常规 mini/trainval/test 534 项共 **2,506,457,646,127 B**，private test 6 项共 **39,224,624,432 B**，全部共 **2,545,682,270,559 B**。项目旧目录 inventory **2,545,682,394,232 B** 比官方对象和大 123,673 B，目录含 sidecar。旧差额 0.265 TB 主要是拿官网取整九项与**含 private** 的目录比较；不得再称同范围未解冲突。官方明细和文件 URL 已在新 manifest，未下载 payload。NAVSIM v1 独立 archive 在同一官方 revision 为 **449,007,410,406 B**，v2 五包为 **50,241,882,946 B**；历史目录对应多 15,197 B、4,655 B，疑为 sidecar（未逐 sidecar 独立验算）。逻辑父子关系已知，archive 内容同一性没有 SHA 证明。

【原文/作者事实】LAW 明确 CARLA **0.9.10.1**、Roach 教师、189K 帧；论文的 CARLA 输入 resize 900×256 属于训练预处理，不提供原图分辨率。检查作者公开 `BraveGroup/LAW` 代码后仅发现 nuScenes 数据准备/训练说明，没有该 CARLA 采集包及文件 manifest；因此无法公开定价。ReCogDrive 作者公开 17 个 JSONL 对象，固定 HF revision `f55bb18e0aca846bbedfb516760a1b9b7cfe3ebf` 的 `size` 合计 **3,789,771,567 B**，仍仅是标注；全量唯一路径归属和独立媒体字节未完成。WAM-Flow 作者模型仓 `data/navsim_668k.jsonl` 为 **414,319,989 B** 的 NAVSIM 标注，并非 3.4M 通用 VQA 的图像包。

【官方 Zenodo 事实】`records/7431011` 九个文件 `size` 合计 **20,534,486,181 B**：四个 `.h5` 分别是 motion、ResNet101、ResNet18、MobileNetV2 预计算特征，其余是 JSONL 与视频 ID 映射；record 没有原始视频文件。SUTD 源媒体与 ReCogDrive 样本路径的对应及原始视频发布字节保持 UNKNOWN。

【修订算术】原 high/all 条件和均减去 `2,545,682,394,232 − 2,506,457,646,127 = 39,224,748,105 B`，对应 **约 24.058 TB / 约 29.588 TB**；加 ThinkTwice 同规模参考为 **约 37.588 TB**。旧约 24.097/29.627/37.627 TB 不再是当前口径。这些组合混有网页约数、整库对论文子集的替代及未计价媒体，既不是完整下界也不是上界。高概率 nuPlan 仍保留完整 v1.1；NAVSIM 采用父体逻辑覆盖场景，若另存 navtrain archive 再单列包留存。压缩包、解压后、预处理峰值三列中后两列仍 UNKNOWN。私有 70M 帧独立标 PRIVATE/UNKNOWN，公开资料下全量上限**无法确定**。
