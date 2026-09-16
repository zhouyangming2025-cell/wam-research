# WAM 一段式核心机制研究：12 篇交接包

> 状态：`TASK PACKAGE / NOT A CONCLUDED ONTOLOGY`
> 目标：让一个新会话从 12 篇论文的一手证据出发，建立可解释、可证伪、可扩展的核心机制分类；现有 A/B/C/D 只作为待攻击草案。

## 一句话任务

不要逐篇复述论文，也不要先接受现有维度；先重建每个论文版本/规划模式的训练因果图与部署因果图，再发现功能等价类，使分类满足：

```text
未涉及某机制                         → 该维度明确记为 ∅
语义输入/输出/决策作用相同、实现不同 → 同一类
因果路径或决策作用实质不同           → 不同类
证据不足                             → UNKNOWN，不得脑补
```

## 给新会话的读取顺序

```text
1. handoff/core_mechanism_12/GPT6_TASK_PROMPT.md
2. handoff/core_mechanism_12/RESEARCH_PROTOCOL.md
3. handoff/core_mechanism_12/PAPER_EVIDENCE_INDEX.md
4. 12 篇 raw paper Markdown（索引中列出）
5. 对应 source/code audit（用于版本与实现边界）
6. deep analysis（仅作二手检查，不得覆盖原文）
7. handoff/core_mechanism_12/DRAFTS_TO_ATTACK.md
8. papers/WAM_ROUTE_MODULE_ABSTRACTION_SAMPLE.md
9. papers/WAM_CORE_MECHANISM_SIGNATURE_V1_PROPOSAL.md
10. papers/WAM_CORE_MECHANISM_SIGNATURE_V1_STRESS_TEST.md
11. handoff/core_mechanism_12/HUMAN_VALIDATION_TEMPLATE.md
```

第 8–10 项是思路演化记录和竞争性假设，不是标准答案。必须先读完 12 篇的一手机制图，才允许借鉴或反驳它们。

机器可读清单位于 `handoff/core_mechanism_12/PAPER_SET_12.tsv`；可运行 `scripts/validate_core_mechanism_12_handoff.ps1` 检查 12 篇证据和交接文件是否齐全。

## 12 篇固定样本

第一组（最终用于人工验收）：

```text
P0048 LAW
P0001 Epona
P0009 DriveLaW
P0046 World4Drive
P0042 WorldDrive
P0045 WoTE
```

第二组（用于发现维度和压力测试）：

```text
P0061 SeerDrive
P0049 Drive-JEPA
P0062 Metis
P0063 DynFlowDrive
P0064 Discrete-WAM
P0065 GraphWorld
```

这里的“第一组/第二组”不代表训练集/测试集，也不代表论文优劣。12 篇共同用于机制发现；第一组只是在最终阶段额外接受人工逐格验收。

注意：12 篇是 paper set，不是 12 个不可拆的分类对象。paper/code、版本和规划模式拆开后，最终 Artifact 投影可以多于 12 行。

## 与仓库其他任务的关系

本任务是一个隔离的 12 篇机制建模任务，不替换：

```text
handoff/LATEST.md
state/CURRENT_STATE.md
state/NEXT_TASK.md
```

这些文件仍服务于长期 field reconstruction 工作流。新会话执行本任务时，不应继续扩展文献、做 gap hunting 或设计新方法。

## 完成判据

只有同时交付以下内容才算完成：

1. 12 个版本化 artifact/mode 的训练图和部署图；
2. 从图中归纳出的机制轴、每轴 `∅`、类别定义和类型约束；
3. 12 篇投影及逐格证据；
4. 完整签名碰撞分析与“为何该碰撞合理/不合理”；
5. 对现有 V1 草案的保留、修改或废弃判决；
6. 前六篇人工验收表；
7. unresolved/UNKNOWN 清单；
8. 一份自我攻击报告，证明分类没有靠论文名、表示基底或模型结构凑类。
