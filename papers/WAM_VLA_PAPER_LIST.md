# WAM + VLA 论文候选清单

更新时间：2026-09-28

定位：本文件记录当前新扩展的 **WAM + VLA** 论文候选集合。它与现有 canonical-12 planning-centric WAM 主线分开维护，现阶段仅作为后续论文摄取、数据集盘点和机制对比的入口，不代表已完成原文核验或纳入核心论文集合。

## 有代码

| 序号 | 论文 | 当前状态 |
| --- | --- | --- |
| 1 | DriveWorld-VLA | TO-VERIFY / TO-INGEST |
| 2 | Uni-World VLA | TO-VERIFY / TO-INGEST |
| 3 | SGDrive | TO-VERIFY / TO-INGEST |
| 4 | FSDrive | TO-VERIFY / TO-INGEST |
| 5 | DriveVLA-W0 | TO-VERIFY / TO-INGEST |
| 6 | CoT4AD | TO-VERIFY / TO-INGEST |
| 7 | WAM-Flow | TO-VERIFY / TO-INGEST |
| 8 | ExploreVLA: Dense World Modeling and Exploration for E... | TITLE-TO-VERIFY / TO-INGEST |
| 9 | UniDriveVLA | TO-VERIFY / TO-INGEST |

## 暂无代码

| 序号 | 论文 | 当前状态 |
| --- | --- | --- |
| 1 | UniDrive-WM | TO-VERIFY / NO-CODE |

## 后续处理规则

1. 先核验论文正式标题、年份、作者/机构、论文链接与代码仓库。
2. 有公开原文后再分配 `Pxxxx` 编号并进入 `papers/raw_md/`；不要仅凭当前名单创建空论文目录。
3. 后续重点补充两类信息：
   - 训练数据：基础驾驶数据、语言/QA/instruction 数据、私有数据、预训练来源；
   - 验证体系：nuScenes、NAVSIM v1/v2、Bench2Drive，以及世界/未来生成验证。
4. 该集合暂不改变 canonical-12，也不触发既有机制 ontology 修改；完成原文核验后再决定哪些论文进入扩展研究集。

来源说明：初始名单来自 2026-09-28 用户提供的 WAM+VLA 分类截图；截图中部分长标题被截断，因此当前文件刻意保留 `TO-VERIFY` 状态，避免未核实信息进入正式语料。