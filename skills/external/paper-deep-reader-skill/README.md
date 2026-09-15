# Paper Deep Reader

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-4.0.0-blue.svg)](CHANGELOG.md)

一个用于单篇学术论文深度解读的 Agent Skill。它把论文写成来源可追溯、图文交错、零背景可进入且具博士级技术深度的完整报告。

默认报告严格采用六部分：

```text
一句话总结 → 背景与动机 → 核心方法 → 实验与结果 → 贡献与影响 → 结论
```

它不是摘要扩写器，也不是图表画廊。目标是让不懂目标学科的人能够一路读懂，同时让研究者能复核方法、公式、实验与证据边界。

## v4 的核心变化

v3 将默认交付压缩为四问结构，虽然减少了冗余，却在真实使用中暴露出三类问题：

- 术语入口过高，报告事实正确但零背景读者读不进去；
- 关键图只被引用或集中贴出，没有和推理过程交错；
- 实验被并列罗列，没有讲出“观察如何支持主张”的证据阶梯。

v4 以完整六部分教学报告为默认，同时保留 v3 的去账本化优点：

- **零背景入口 + 博士技术上限**：先解释概念，再进入精确定义、公式和证据。
- **关键术语首次解释**：不允许孤立缩写、循环定义或用陌生术语解释陌生术语。
- **一个例子走通机制**：例子必须产生中间状态并走到输出，不只是表面类比。
- **所有关键图表进入主文**：不再默认限制 2–4 张；删除后会破坏理解的图表必须全部嵌入并详解。
- **图文邻接**：图前给阅读任务，图后写观察、推理桥、边界和下一步。
- **六部分完整成稿**：背景、研究现状、创新、可靠性、贡献、影响与具体未来方向稳定出现。
- **证据可追溯**：作者主张、直接证据、报告推断和外部背景彼此分开。
- **有视觉与纯文本双路由**：无视觉能力时明确降级，不假装看图。

## 适合什么任务

```text
精读这篇 PDF，写成完整图文报告。

向完全不懂这个方向的人讲清楚，但保留博士级技术细节。

逐一解释所有关键图表，并说明每张图如何支持结论。

只解释式(7)怎样对应图3中的模块。

快速看懂这篇论文，告诉我是否值得继续读。

按审稿或复现目标深读，并附完整证据账本。
```

不用于全文逐句翻译或多论文综述。

## 默认读者模型

默认配置把“从哪里讲起”和“讲到哪里”分开：

```yaml
audience: broad-to-expert

reader_background:
  entry_level: novice
  technical_ceiling: doctoral
```

- `entry_level: novice`：不假设目标学科知识；关键术语、缩写和指标首次出现时解释。
- `technical_ceiling: doctoral`：保留方法接口、关键公式、创新差分、公平比较、证据强度和失败边界。

因此默认并不是“大众科普”，而是：

```text
白话定义 → 本文作用 → 最小例子 → 精确含义 → 技术机制 → 证据边界
```

## 交付模式

| 模式 | 常见触发 | 交付 |
|---|---|---|
| `brief` | 快速看懂、速览、值不值得读 | 一屏主线，最多一个必要图表，明确未完成深读 |
| `explain` | 解读、精读、详细讲解、讲清楚 | 默认；完整六部分，覆盖所有关键机制、公式与图表 |
| `audit` | 逐个编号图表、审稿、复现、完整审计 | 六部分主文 + 全量视觉/证据/复现/审稿附录 |
| `targeted` | 只问某个公式、图表或结论 | 直接回答局部问题，仍补术语、来源和边界 |

“逐关键图表”属于 `explain`，因为默认就要求覆盖全部关键对象；“逐个编号图表”才使用 `audit` 的全量账本。

## 阅读与写作工作流

### 第一遍：建立故事与概念地图

读取标题、摘要、引言、结论、限制、章节结构和全部图表标题，先重建：

```text
旧方法依赖什么 → 在什么条件下失败 → 作者改变什么
→ 用什么证据验证 → 结论边界
```

同时列出读懂论文前必须知道的概念，以及这些概念之间的依赖关系。

### 第二遍：重建机制

读取全部承重方法、理论或研究设计，重建输入、步骤、中间状态、输出、假设和代价。必须找到一个与论文同构的最小例子并走完整条链。

### 第三遍：核对证据与图表

读取主结果、证明、对照、消融、稳健性、负例、失败案例和影响结论的附录。为每项核心主张确定最强证据、支持等级、替代解释和适用边界。

### 教学重构

不按论文段落机械改写，而是按人理解的顺序组织：

```text
具体问题 → 必要术语 → 旧方法痛点 → 作者洞见 → 最小例子
→ 精确方法/公式 → 关键证据阶梯 → 贡献、影响与边界
```

## 默认报告结构

### 1. 核心思想一句话总结

中文不超过 50 字，同时说明解决什么、做了什么和最关键成立依据。

### 2. 论文背景与动机

包含必要概念、具体问题、重要性、研究现状、旧方法痛点和作者洞见。

### 3. 核心方法/模型详解

包含总体框架、贯穿例子、承重组件、关键公式、与旧方法的最小差分和创新判断。

### 4. 实验与结果分析

包含数据/样本、基线、公平条件、指标含义、证据阶梯、对照/消融/失败案例、支持等级与可靠性。

### 5. 论文的贡献与影响

包含问题/方法/证据层贡献、近期与长期影响、实践价值，以及由具体缺口推出的可检验未来方向。

### 6. 结论

收束核心机制、最强证据、边界和是否值得精读、引用、复现或迁移的判断。

完整骨架见 [`references/report-template.md`](references/report-template.md)。

## 关键图表如何写

所有编号视觉对象先进入 manifest，再判断 `key: true|false`，并填写 `classification_reason`，防止通过批量标记“非关键”规避覆盖。

`key: true` 表示删除后会导致读者误解问题、机制、主要证据、创新差分或边界。默认 `explain` 要求所有关键对象都设置：

```json
{
  "key": true,
  "classification_reason": "删除该图会失去对核心主张的直接证据",
  "selected_for_report": true,
  "report_role": "evidence",
  "selection_reason": "该图直接建立主结果与核心主张之间的证据关系"
}
```

每个关键图表都按以下顺序放进正文：

```text
它回答什么问题、先看哪里、怎么读
→ 已核验截图
→ 图中元素与比较关系
→ 关键数值/观察
→ 为什么支持正文主张
→ 不能推出什么
→ 下一项证据为何必要
```

这能避免两种常见失败：只写“如图 4 所示”而不展示图片，以及一次贴出多张图片后只写简短图注。

## 安装

### Codex

```bash
git clone https://github.com/Linwei-Chen/paper-deep-reader-skill.git \
  ~/.codex/skills/paper-deep-reader
```

### Claude Code

```bash
git clone https://github.com/Linwei-Chen/paper-deep-reader-skill.git \
  ~/.claude/skills/paper-deep-reader
```

### Cursor

```bash
git clone https://github.com/Linwei-Chen/paper-deep-reader-skill.git \
  ~/.cursor/skills/paper-deep-reader
```

更新已有安装：

```bash
git -C ~/.codex/skills/paper-deep-reader pull --ff-only
```

将路径替换为实际安装位置。

## 项目配置

项目根目录可放置 `.paper-reader.yaml`：

```yaml
domain: auto
audience: broad-to-expert
goal: understand
depth: deep
delivery: explain
language: zh-CN
visual_mode: auto

reader_background:
  primary_field: ""
  familiar_topics: []
  unfamiliar_topics: []
  entry_level: novice
  technical_ceiling: doctoral

preferences:
  explanation_layers: intuitive-then-technical
  define_terms_on_first_use: true
  equation_detail: teaching
  statistics_detail: teaching
  key_visual_coverage: all
  embed_key_visuals: true
```

继续兼容旧 `research-generalist`、`equation_detail: selective` 和 `embed_key_visuals` 配置；缺少新字段时使用默认双层讲解策略。

## 输出文件

只需聊天回答时不强制创建文件。需要保存报告、提取图表或执行审计时生成：

```text
<paper-slug>-deep-read/
├── report.md
├── source_map.json
└── assets/
    ├── visual_manifest.json
    ├── pages/
    ├── crops/
    └── text/
```

- `report.md`：六部分图文报告和可选附录。
- `source_map.json`：版本、来源、读者入口/技术上限、主张—证据和视觉覆盖。
- `visual_manifest.json`：全量视觉账本、核验状态和正文选择理由。
- `crops/`：经过视觉核查的图表截图。
- `text/`：纯文本路线使用的逐页文字与图表证据卡。

保存的 Markdown 使用相对资产路径，便于跨目录和跨平台迁移；在只支持绝对本地路径的聊天界面展示时使用仍然存在的绝对路径。

## PDF 图表提取

报告校验器只使用 Python 标准库。PDF 图表提取器额外需要 PyMuPDF；推荐使用隔离环境：

```bash
uv run --isolated --with pymupdf \
  python scripts/extract_pdf_assets.py inventory paper.pdf output/assets --dpi 180
```

已安装依赖时：

```bash
python3 scripts/extract_pdf_assets.py inventory \
  paper.pdf output/assets --dpi 180
```

无视觉模型使用：

```bash
python3 scripts/extract_pdf_assets.py inventory \
  paper.pdf output/assets --text-only
```

自动裁图只是候选。视觉模式必须打开核查；纯文本模式不得把文字推断写成视觉观察。自动检测漏图或重复时，按 PDF 实际编号人工修正 manifest。

需要精确重裁时：

```bash
python3 scripts/extract_pdf_assets.py crop \
  paper.pdf output/assets/crops/figure-3.png \
  --page 7 --bbox 120,180,1120,1030 --dpi 180
```

## 报告校验

```bash
python3 scripts/validate_report.py output/report.md \
  --mode explain \
  --manifest output/assets/visual_manifest.json \
  --source-map output/source_map.json \
  --strict
```

无视觉模式增加 `--text-only`。聊天回答或缩减交付可增加：

```text
--allow-missing-manifest --allow-missing-source-map
```

校验器检查：

- 六部分结构与 50 字一句话；
- 术语入门、最小例子、证据推理桥、未来方向和边界；
- 图片路径和 alt 文本；
- 所有关键视觉是否入选、核验、嵌入并与详细解释相邻；
- 纯文本模式是否错误嵌入未核验图片；
- source-map v5 的读者入口、技术上限和视觉覆盖一致性；
- 占位符、公式分隔符和来源锚点。

运行测试：

```bash
python3 -m unittest discover -s tests -v
```

## 仓库结构

```text
.
├── agents/openai.yaml
├── .paper-reader.example.yaml
├── SKILL.md
├── README.md
├── DESIGN_NOTES.md
├── CHANGELOG.md
├── references/
├── scripts/
└── tests/
```

## 限制

- 本 Skill 默认不运行论文代码或声称完成实际复现。
- 扫描 PDF 可能需要外部 OCR；本仓库不自动上传论文到第三方服务。
- 纯文本路线不能独立确认颜色、曲线、面板、布局、挑样和裁图完整性。
- “首个”和“SOTA”需要额外文献检索，不能只依据论文自述。
- 领域 Lens 不替代临床、法律、安全或伦理专业判断。

## License

[MIT](LICENSE)
