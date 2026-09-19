# 210 现场数据资产核查：nuPlan / OpenScene

> 日期：2026-09-19  
> 性质：现场只读核查留痕。未下载数据、未安装 Hugging Face CLI、未删除/清理正式数据，也未修改正式数据目录。  
> 作用：把 `NUPLAN_DOWNLOAD_DECISION.md` 的推理落到 210 当前真实资产状态。

---

## 1. 结论

**短期 raw nuPlan 下载批准量继续保持 0 TB。**

原因已经从“推测”升级为现场证据：

1. OpenScene trainval camera / LiDAR / metadata 已经存在于正式数据根；
2. raw nuPlan trainval DB / raw trainval sensor 当前不在正式根；
3. 当前 raw trainval camera 的公开路径不能在 210 现场直接形成可信对象清单；
4. 因此不能因为论文写有 nuPlan 就生成 TB 级 raw 下载队列；
5. 当前更合理的策略是保留 OpenScene、继续用 NAVSIM 与作者 checkpoint 推进 WAM，raw nuPlan 只在具体 from-scratch 目标闭合后审批。

---

## 2. OpenScene trainval：现场实测

正式根中已确认：

| 资产 | 文件数 | 实测字节 |
|---|---:|---:|
| trainval camera archives | 200 × `.tgz` | **1,242,213,272,326 B** |
| trainval LiDAR archives | 200 × `.tgz` | **882,141,233,382 B** |
| trainval metadata | - | **7,052,210,642 B** |

对应 `.sidecar` 均存在。

换算仅用于直观理解：

```text
camera  ≈ 1.242 TB decimal
LiDAR   ≈ 0.882 TB decimal
metadata≈ 7.05 GB decimal
```

合计归档量约：

```text
2,131,406,716,350 B
≈ 2.131 TB decimal
```

这与 OpenScene / NAVSIM 官方对完整 trainval sensor “>2000 GB”的量级一致。

### 工程含义

- 不需要再次下载 NAVSIM navtrain 精简 sensor 包；
- 不应为了节省空间主动删除当前完整 trainval；
- 现有 OpenScene 已经是当前 NAVSIM/WAM 主线最有价值的基础数据资产之一。

---

## 3. nuPlan 正式根：现场状态

当前正式 nuPlan 根约：

```text
~1.7 TB
```

但现场核查没有发现：

- raw `splits/trainval` DB；
- raw trainval sensor 目录。

因此不能把“nuPlan 根约 1.7 TB”解释为：

> 已拥有 raw nuPlan trainval DB / raw trainval camera。

这两件事必须分开。

---

## 4. raw trainval camera：当前仍未闭合

现场确认：

- 当前使用的 CloudFront raw trainval camera 路径返回 **HTTP 404**；
- 既有 `nuplan_volume_inventory.json` 记录：
  - trainval camera = 0 objects；
  - trainval LiDAR = 0 objects。

因此：

> 当前不能基于路径猜测、历史 URL 或论文需求直接生成 raw trainval 下载队列。

### 但 404 不能被解释成“官方数据已经不存在”

进一步公开代码核查发现，当前 123D / py123d 文档仍明确列出 Motional 区域 S3 的 legacy archive object keys：

```text
https://motional-nuplan.s3-ap-northeast-1.amazonaws.com/public/nuplan-v1.1/
```

其中：

- train camera：`0..42`，共 43 archives；
- train LiDAR：`0..42`；
- val camera：`0..11`；
- val LiDAR：`0..11`；
- test camera / LiDAR：各 `0..11`。

所以当前需要区分：

```text
CloudFront 某路径 404
≠
已证明区域 S3 的 legacy object 不存在
```

下一步应做 **HEAD-only probe**，而不是 GET 下载。

---

## 5. 123D：保持候选，不视为 Motional raw replacement

公开数据卡当前确认：

- 15,910 logs；
- 1,457 sensor logs；
- 14,453 sensorless logs；
- all modalities 总量约 **7.8 TiB**；
- metadata 使用 **10 Hz sync clock**；
- 每个 sensor log 按 modality 单独存 Arrow 文件。

这使它尤其适合做：

```text
CAM_F0-only
+
ego state
+
sync / route metadata
```

的高频研究数据候选。

但是：

- camera 被重新编码；
- 存储/API 改为 Arrow；
- 原 Epona / DriveLaW / WorldDrive dataloader 不能直接读取；
- 因此它适合作为“自研高频 WAM 数据源”，而不是 exact paper reproduction 的 raw Motional 替代。

---

## 6. 当前下载矩阵

| 资产 | 当前状态 | 当前动作 |
|---|---|---|
| OpenScene trainval camera | 已有 200 archives | **保留，不重复下载** |
| OpenScene trainval LiDAR | 已有 200 archives | **保留，不重复下载** |
| OpenScene trainval metadata | 已有 | **保留** |
| NAVSIM navtrain 精简 sensor | 完整 trainval 已有 | **不下载** |
| raw nuPlan trainval DB | 未发现 | **暂不下载** |
| raw nuPlan train camera | 未闭合 | **暂不下载** |
| raw nuPlan LiDAR | 当前 WAM 无明确必须理由 | **不下载** |
| 123D all modalities | 未下载 | **不下载全量** |
| 123D CAM_F0-only | 候选 | **先 metadata-only size probe** |

---

## 7. 下一步只读核查

### A. Motional archive HEAD probe

目标：

- 不下载 ZIP body；
- 对已知 archive URL 发 HEAD；
- 记录：
  - HTTP status；
  - Content-Length；
  - ETag；
  - Last-Modified；
- 汇总 train/val camera 与 LiDAR 的 archive-level 总量。

脚本：

`scripts/datasets/nuplan_archive_head_probe.py`

### B. 123D repo metadata probe

目标：

- 不安装 HF CLI；
- 不下载 Arrow；
- 只调用公开 Hub tree API；
- 统计：
  - `camera.pcam_f0.arrow`
  - `ego_state_se3.arrow`
  - `sync.arrow`
  - 其他必要 metadata
  的文件数和总字节。

脚本：

`scripts/datasets/hf_dataset_size_probe.py`

### C. 只有 A/B 得到真实字节后，才做下一次下载审批

最终比较：

```text
Motional archive-level raw camera
vs.
Epona 真正所需数据的可裁剪程度
vs.
123D CAM_F0-only
```

再决定真正的 Y TB。

---

## 8. 当前固定结论

> **210 已拥有完整量级的 OpenScene trainval 核心资产；当前没有证据支持立即补 raw nuPlan。raw nuPlan trainval 的对象清单与大小尚未在现场闭合，因此短期批准下载量继续为 0 TB。下一阶段只做 HEAD / metadata 级探测，不做任何 TB 级数据传输。**
