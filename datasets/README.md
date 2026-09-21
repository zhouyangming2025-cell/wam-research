# WAM 数据集文档入口

本目录只保留当前决策和当前资产，不保存过程性调研长文。

| 文件 | 权威职责 |
|---|---|
| `resource_inventory_20260921.md` | 210 正式数据池的人类可读资产账 |
| `resource_inventory_20260921.tsv` | 表格化资产账 |
| `resource_inventory_20260921.json` | 机器可读资产账 |
| `wam_dataset_download_plan_20260921.md` | 后续数据集选择、版本、许可、体量和优先级 |

研究依据位于 `../audits/datasets/`，只用于解释结论，不是执行入口。

下载、监督、验收与 promote 的实际工程 SOP 位于本地 WAM 工作根 `文档/DOWNLOAD_SOP.md`。本目录不存在“所有数据必须先下载到 Windows 再 SSH 上传 210”的固定路线；具体传输路线必须按源站和 210 可达性现场决定。

实际数据落地后，应更新 resource inventory；不能把计划下载提前写成已经拥有。
