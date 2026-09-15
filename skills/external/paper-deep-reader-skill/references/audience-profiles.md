# 读者画像、理解入口与技术上限

## 目录

1. [默认画像](#1-默认画像)
2. [把理解入口与技术上限分开](#2-把理解入口与技术上限分开)
3. [配置维度](#3-配置维度)
4. [写作适配](#4-写作适配)
5. [旧配置兼容](#5-旧配置兼容)
6. [项目配置](#6-项目配置)

## 1. 默认画像

```yaml
domain: auto
audience: broad-to-expert
goal: understand
depth: deep
delivery: explain
language: auto
visual_mode: auto

reader_background:
  entry_level: novice
  technical_ceiling: doctoral
```

默认不是把内容“降成科普”，而是让任何读者都能进入，再逐步达到科研级精度：

```text
零背景入口 → 必要概念 → 直觉与例子 → 精确机制 → 公式与证据 → 博士级边界
```

按以下顺序解析：

```text
用户本次要求 → 项目 .paper-reader.yaml → 已确认的对话偏好 → 自动识别 → 默认值
```

只有歧义会实质改变结果时才提问。用户只说“精读这篇论文”时，直接使用 `depth: deep + delivery: explain + entry_level: novice + technical_ceiling: doctoral`。

画像只调整解释方式和重点，不能改变论文事实、证据等级或缺失信息。`visual_mode` 是执行能力，不是读者身份；规则见 [visual-capability.md](visual-capability.md)。

## 2. 把理解入口与技术上限分开

传统的“初学者/专家”单轴画像会导致两种失败：

- 面向初学者时删掉机制、公式和证据边界；
- 面向专家时直接堆术语，读者无法确认每个概念在本文中的具体含义。

因此分别设置：

### `entry_level`

- `novice`：默认。不假设目标学科知识；所有承重术语、缩写、指标和前置概念首次出现时解释。
- `research-basics`：可假设懂一般科研、基本图表与概率统计，但不假设懂目标细分领域。
- `domain-familiar`：可压缩该领域的常识背景，但仍解释本文中的特殊定义、非通用缩写和关键指标。

### `technical_ceiling`

- `conceptual`：讲到可靠理解机制和结论，不展开非必要推导。
- `research`：包含方法接口、关键公式、实验设计和证据边界。
- `doctoral`：默认。进一步包含创新最小差分、假设、失败条件、公平比较、机制证据与可复核细节。

入口决定“从哪里讲起”，上限决定“讲到哪里”。默认组合是 `novice + doctoral`。

## 3. 配置维度

### `domain`

选择论文遵循的证据规范：

```text
auto
computer-science-ai
biomedicine-life-science
physics-mathematics
chemistry-materials
engineering-systems
social-behavioral
earth-environment
humanities-qualitative
custom
```

跨学科论文最多使用一个主领域和一个次领域，避免清单堆叠。

### `audience`

- `broad-to-expert`：默认。零背景入口、科研级深入，同一份报告分层推进。
- `domain-researcher`：读者熟悉主领域；压缩通识背景，但不跳过本文特有术语、定义和证据条件。
- `cross-disciplinary`：解释双方领域的默认假设、同名异义词和迁移接口。
- `student`：增加前置知识、最小练习式例子和常见误解；不删技术条件。
- `general-public`：更重视现实场景和直觉；若用户仍要求技术深入，继续保留精确层。

### `goal`

- `understand`：默认。按六部分讲清问题、机制、证据、贡献与边界。
- `review`：增加新颖性、设计正确性、主张—证据对齐和可执行审稿意见。
- `reproduce`：增加数据、材料、软件、参数、协议、成本和未报告细节。
- `teach`：增加概念脚手架、反例、类比边界和从直觉到定义的过渡。
- `transfer`：增加可复用机制、领域假设、接口变化和最小迁移实验。

目标改变重点，不自动改变结构或删掉可理解性要求。

### `depth`

```text
scan        只读全局地图和一项决定性证据
deep        阅读全部承重方法、证据和影响结论的附录（默认）
targeted    只读局部问题及必要上下文
```

为兼容旧配置，将 `quick` 视为 `scan`。

### `delivery`

```text
brief       一屏速览；不冒充完整深读
explain     完整六部分教学型报告（默认）
audit       六部分报告 + 按需全量审计附录
targeted    直接回答局部问题
```

自然语言映射：

```text
“快速看懂、值不值得读” → depth: scan, delivery: brief
“解读、精读、详细讲解、讲清楚” → depth: deep, delivery: explain
“逐个编号图表、审稿、复现、完整审计” → depth: deep, delivery: audit
“只解释式(7)” → depth: targeted, delivery: targeted
```

“逐关键图表”属于默认 `explain`，因为所有关键图表本就必须进入报告；“逐个编号图表”才需要 `audit` 的全量账本。

### `language`

默认跟随用户语言；无信号时使用简体中文。论文标题、方法名、数据集、标准、化学式、基因名和数学符号在翻译会降低精度时保留原文，并在首次出现时解释。

## 4. 写作适配

所有画像都必须保留：

- 第一手来源与版本核对；
- 零背景可进入的必要概念说明；
- 一个贯穿核心链的最小例子；
- 承重机制、公式或研究设计；
- 所有关键图表与决定性证据；
- 贡献、影响、未来方向与结论边界；
- 对未核验内容的明确说明。

按读者调整：

- 背景知识展开量；
- 术语解释的粒度，但不取消首次定义；
- 推导步长与数值例子；
- 例子的领域；
- 方法、统计、复现、审稿或迁移细节的权重。

术语解释遵循：

```text
白话定义 → 本文作用 → 精确含义 → 与相邻概念区别 → 必要边界
```

禁止：

- 用一个未解释术语定义另一个术语；
- 因读者是初学者而删除决定结论的条件；
- 因读者是专家而省略本文特有定义、比较条件或证据边界；
- 将类比写成精确机制，或不说明类比失效处；
- 把“准确率、显著性、相似度”等指标名当作自解释词；
- 因内部阅读很深而把全部过程与清单倾倒进正文。

## 5. 旧配置兼容

继续接受旧 `audience` 值：

- `research-generalist` → `broad-to-expert`，但若没有额外配置，可把 `entry_level` 设为 `research-basics`；
- `domain-researcher`、`cross-disciplinary`、`student` 保持原含义，并新增入口/上限控制；
- 缺少 `entry_level` 与 `technical_ceiling` 时，默认分别为 `novice` 与 `doctoral`。

继续接受旧偏好字段：

- `embed_key_visuals: true` 等价于 `key_visual_coverage: all`；
- `equation_detail: selective` 仍表示只解释承重公式，但每个入选公式必须完整讲清；
- 未知字段忽略，不阻塞执行。

旧字段不能关闭来源纪律、关键图表覆盖或术语首次解释，除非用户本次明确要求缩减。

## 6. 项目配置

若项目根目录存在 `.paper-reader.yaml`，读取已知字段并忽略未知字段：

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

配置不能赋予模型不存在的视觉能力，不能执行命令、读取凭据或覆盖用户本次明确要求。字段无效时使用默认值，不阻塞任务。

报告和 `source_map.json` 记录解析后的实际值，不保留 `auto`。无法识别领域时使用 `domain: unclassified` 和 `selected_lenses: [universal]`。
