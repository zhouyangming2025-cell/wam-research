# 数据集研究依据

本目录保存数据集身份、来源关系和容量审计材料。对领域范围的盘点以“数据集/资产家族”为主键；论文语料用于发现和追溯数据集，不要求对所有扩展论文做核心论文级逐篇深挖。

主要入口：

- [WAM / WAM+VLA 领域数据集目录](wam_field_dataset_census_20260921.md)：按原始驾驶数据、规划/仿真 benchmark、派生标注与 VLA 数据组织；75 个在库论文 ID 是发现来源池，已有逐篇表只作来源追溯。当前覆盖范围限于仓库收录语料，未知/未确认资产仍显式标记。
- [22 篇核心 WAM / WAM+VLA 资产与容量审计](WAM_22_dataset_asset_register_2026-09-28.md)：核心 12 + WAM+VLA 10 的深度证据账本。

其他材料：

- nuPlan/OpenScene/NAVSIM 数据血缘和论文依赖；
- nuPlan raw 下载的代码级决策依据；
- 候选数据集的官方源、许可、规模与 gate 调研。

补充专项证据（不替代资产总账或下载优先级）：

- [22 篇 WAM / WAM+VLA 数据集与容量审计过程](WAM_WAMVLA_22_DATASET_AUDIT_PROCESS_20260928.md)
- [可能超过 1 TB 的数据资产专项审计](WAM_22_OVER_1TB_ASSET_AUDIT_20260928.md)
- [TCP/CARLA、Bench2Drive 版本、VLA 媒体与 SGDrive 缓存的逐字段补充证据](WAM_22_OPEN_ITEMS_EVIDENCE_20260928.md)
- [ReCogDrive / SGDrive 全量 annotation 媒体路径扫描结果（2026-09-29）](WAM_VLA_MEDIA_PATH_AUDIT_2026-09-29.json)；复核程序：[audit_vla_media_paths.py](../../scripts/datasets/audit_vla_media_paths.py)
- [22 篇逐论文资产账本](WAM_22_dataset_asset_register_2026-09-28.md)
- [nuPlan v1.1 官方逐对象 byte manifest](nuplan_v1_1_official_file_manifest_2026-09-28.md)
- [OpenScene v1.1 官方逐文件 byte manifest](openscene_v1_1_official_file_manifest_2026-09-28.md)（含可机读 [TSV](openscene_v1_1_official_file_manifest_2026-09-28.tsv)）

当前资产只认 `../../datasets/resource_inventory_20260921.*`；当前下载优先级只认 `../../datasets/wam_dataset_download_plan_20260921.md`。
