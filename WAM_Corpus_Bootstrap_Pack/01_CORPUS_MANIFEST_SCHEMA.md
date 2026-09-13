# CORPUS_MANIFEST Schema

`CORPUS_MANIFEST.csv` 是整个论文资产层的主索引。

一篇论文一行。

## 必填字段

| Field | Meaning |
|---|---|
| `paper_id` | 稳定 ID，例如 `P0001` |
| `title` | 正式标题 |
| `year` | 年份 |
| `first_author` | 第一作者 |
| `venue` | arXiv / CVPR / NeurIPS / etc. |
| `arxiv_id` | 若有 |
| `doi` | 若有 |
| `official_url` | 论文官方入口（论文页面） |
| `official_pdf_url` | canonical PDF 的官方下载入口；可与 `official_url` 不同。未确认时留空 |
| `source_version` | canonical PDF 的版本标识，见下方枚举。未确认时填 `UNKNOWN` |
| `pdf_sha256` | canonical PDF 的 SHA256。未获取填 `UNKNOWN`；获取失败留空并在 notes 记 `DOWNLOAD_BLOCKED` |
| `raw_md_sha256` | raw MD 的 SHA256。未转码填 `UNKNOWN` |
| `pdf_local_path` | 本地/NAS PDF 路径 |
| `raw_md_local_path` | PDF→MD 路径 |
| `library_status` | `NONE/PDF/MD/PDF+MD` |
| `github_card_path` | Research Card 路径 |
| `code_available` | `YES/NO/UNKNOWN` |
| `official_code_url` | 官方源码 |
| `code_repo_id` | 对应 CODE_REPO_MANIFEST 的 ID |
| `reading_status` | 见状态枚举 |
| `primary_tags` | 主标签，用 `;` 分隔 |
| `hypothesis_tags` | `P1;P2R;P3` 等 |
| `decision_relevance` | `HIGH/MEDIUM/LOW/NONE` |
| `last_reviewed` | `YYYY-MM-DD` |
| `notes` | 简短备注 |

## source_version 枚举

canonical PDF 采用的版本。一篇论文只有一个 canonical。

```text
<VENUE><YEAR>_camera_ready    例如 ICCV2025_camera_ready, NeurIPS2024_camera_ready
arXiv_v<N>                    例如 arXiv_v1
project_hosted
none_available                没有任何可获取的开放官方来源
UNKNOWN
```

## Canonical PDF 优先级

```text
venue camera-ready
> explicitly selected official arXiv version
> official project-hosted PDF
```

其他版本只能作为 archive / quarantine 保存，**不得同时充当 canonical**。

## Metadata 证据层级

metadata 冲突时按以下顺序裁决：

```text
venue camera-ready paper
> arXiv paper
> official project/repository
> OpenAlex / bibliographic index
> secondary source
```

证据等级标签（记录在该行 `notes` 内，形如 `EVIDENCE_LEVEL=<值>`）：

```text
INDEX_BACKED       来源为文献索引（OpenAlex 等），尚未对照论文本身
DOCUMENT_VERIFIED  已对照 PDF 首页（title / authors）核验
```

只有 `DOCUMENT_VERIFIED` 才可视为最终 metadata。`INDEX_BACKED` 字段不得用于对外引用。

## reading_status

推荐固定枚举：

```text
DISCOVERED
DOWNLOADED
RAW_MD_READY
SCREENED
DEEP_READ
AUDITED
DECISION_RELEVANT
RETIRED
```

定义：

- `DISCOVERED`: 只知道论文存在。
- `DOWNLOADED`: PDF 已落本地。
- `RAW_MD_READY`: 已转全文 MD。
- `SCREENED`: 已完成快速判断。
- `DEEP_READ`: 完整精读。
- `AUDITED`: 已进行 adversarial audit。
- `DECISION_RELEVANT`: 已真正改变研究问题/方向。
- `RETIRED`: 当前主线不再需要，但保留归档。

## primary_tags 推荐词表

不要让 tag 无限自由增长。优先复用：

```text
world-model
planning
end-to-end
video-generation
latent-world-model
action-conditioned
counterfactual
reactive
interactive
closed-loop
open-loop
trajectory-prediction
reward-model
trajectory-scorer
representation
JEPA
diffusion
autoregressive
uncertainty
multimodal
OOD
long-tail
evaluation
benchmark
safety
risk
```

## hypothesis_tags

当前：

```text
P1_RETIRED
P2R_PRIMARY
P3_HOLD
GENERAL
```

未来新增 hypothesis 时再扩。

## decision_relevance

`HIGH` 只有当论文满足至少一项：

- 杀掉 / 强烈削弱一个 hypothesis；
- 提供主问题的直接 observed failure；
- 直接占据 novelty；
- 形成关键反例；
- 改变实验设计或 research decision。

不要把“看起来相关”标 HIGH。
