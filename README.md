# wam-research

Persistent research workspace for **planning-centric World-Action Models (WAM) in autonomous driving**.

## 唯一入口

每次恢复工作只按这个顺序读取：

```text
1. state/CURRENT_STATE.md    当前目标、边界和已确认事实
2. state/NEXT_TASK.md        唯一正在执行的任务
3. manifests/CORPUS_MANIFEST.csv → 对应 papers/raw_md / audits
```

`START_HERE.md`、`handoff/LATEST.md` 和旧的 field/taxonomy/route 文档不再独立声明“当前状态”；它们只保存历史上下文或证据线索。

## 当前工作边界

固定核心集为 12 篇：Epona、DriveLaW、WorldDrive、WoTE、World4Drive、LAW、Drive-JEPA、SeerDrive、Metis、DynFlowDrive、Discrete-WAM、GraphWorld。

当前任务是：在不丢失原文、代码审计与有效比较观察的前提下，清理重复入口和历史性总结，并从可追溯证据重建这 12 篇的规划技术路线。不得把旧 taxonomy、D01/D02、路线图或状态标题自动当作当前结论。

## 证据顺序

```text
论文原文 / 固定代码 / 数据与评测配置
→ 单篇 source/code audit 与 deep analysis（保留其边界）
→ 跨论文比较
→ 历史 taxonomy、路线图、hand-off 与状态快照
```

缺证据时保留 `UNKNOWN`。训练期未来监督、在线状态条件、候选后果评估与世界—规划迭代不得混为一种“world model benefit”。

## 目录职责

```text
manifests/          语料索引
papers/raw_md/      可读原始文本层
papers/deep_analysis/ 与 audits/   受证据边界约束的解释与核验
state/              当前决策、当前任务与历史决策记录
landscape/          历史性比较/地图；非当前状态入口
hypotheses/         历史或暂停的研究问题
handoff/            会话辅助；非当前状态入口
```

研究问题发现与方法设计仍暂停；仓库首先服务于可核验的领域理解与 12 篇机制比较。