# OpenScene v1.1 官方文件级容量清单（2026-09-28）

来源：[OpenDriveLab/OpenScene 官方 Hugging Face 仓库](https://huggingface.co/datasets/OpenDriveLab/OpenScene/tree/a76f840b65e972bc45e56c2adced897498e9a026/openscene-v1.1)，固定 revision `a76f840b65e972bc45e56c2adced897498e9a026`；通过 `api/datasets/OpenDriveLab/OpenScene/tree/main?recursive=true&expand=true&limit=100` 的七页 `size` 字段列取，完整 620 条仓库条目中筛出 OpenScene v1.1 文件 540 条。此处只读文件元信息，未下载数据对象。每条完整路径及官方字节链接见 [TSV](openscene_v1_1_official_file_manifest_2026-09-28.tsv)。

| split | 对象数 | 压缩对象/JSON 字节 |
|---|---:|---:|
| mini | 66 | 153,999,775,596 |
| trainval | 402 | 2,131,406,784,702 |
| test | 66 | 221,051,085,829 |
| private_test | 6 | 39,224,624,432 |
| **常规 mini/trainval/test** | **534** | **2,506,457,646,127** |
| **全部（含 private test）** | **540** | **2,545,682,270,559** |

【官方对象事实】常规九项传感器/metadata 加三份极小 JSON 清单 = 2,506,457,646,127 B（2.506457646127 TB）；private test 的 metadata/sensors = 39,224,624,432 B；合计 2,545,682,270,559 B。2026-09-21 历史 inventory 的 `openscene-v1.1` 目录为 2,545,682,394,232 B，比官方发布对象和大 123,673 B；目录计数含 sidecar，不能误当发布包 payload。旧的“官网九项约 2.28056 TB 对比 inventory 2.54568 TB 相差 0.26512 TB”将**官网取整/单位口径与含 private test/sidecar 的目录值相比较**，不得再视为同范围的未解释 0.265 TB。

【分析判断】NAVSIM v1 navtrain 为 OpenScene trainval 场景过滤；官方 HF 发布的独立 navsim 两类 archive 合计 449,007,410,406 B，项目目录 inventory 449,007,425,603 B，差 15,197 B；v2 五包为 50,241,882,946 B，与历史目录差 4,655 B。两者差额同样符合 sidecar 范围，但未以每个 sidecar 的逐项清单独立验算。父子数据仅有逻辑血缘证据，没有跨 archive 内容 SHA 去重。

本表的 `exact_bytes` 是官方仓库该 revision 的文件对象 `size`，只对这些对象的压缩留存有效。`duplicate_of` 是上游血缘提示，不是二进制同一性证明；解压字节、下载/预处理峰值仍为 UNKNOWN。API 分页结果须在变更 revision 后重新采样。
