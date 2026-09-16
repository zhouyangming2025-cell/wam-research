# 前六篇人工验收模板

> 使用时机：GPT‑6 完成 12 篇机制发现、投影与自我攻击之后。
> 目的：人工检查分类是否真的表达功能机制，而不是检查它是否符合预设答案。

## 1. 单格验收

对前六篇的每个机制轴逐格填写：

| 字段 | 内容 |
|---|---|
| Paper artifact / mode |  |
| Axis |  |
| Assigned class | `∅` / class / `UNKNOWN` / `N/A` |
| 一句话机制定义 |  |
| Semantic input |  |
| Semantic output |  |
| Lifecycle | TRAIN / RUNTIME / BOTH |
| 对最终决策的因果作用 |  |
| Primary evidence | 文件 + 章节/行号/公式 |
| Nearest alternative class |  |
| Why not alternative |  |
| Confidence | HIGH / MEDIUM / LOW |
| Human verdict | PASS / REVISE / EVIDENCE GAP |

### 必问问题

1. 若标 `∅`，证据是否真的表明不存在，而非只是没看到？
2. 若标 `UNKNOWN`，是否明确写出缺什么证据？
3. 类别定义能否在不提论文名的情况下复述？
4. 换成另一种 backbone/表示/生成算法，类别是否仍成立？
5. 此类别是否改变语义 I/O、因果路径、生命周期或决策作用？
6. 只看该格是否会误以为训练期模块在线运行？

## 2. 同类验收

对所有落入同一类的前六篇论文，逐对检查：

| Pair | 相同的语义 I/O | 相同的生命周期 | 相同的决策作用 | 仅实现不同？ | Verdict |
|---|---|---|---|---|---|
|  |  |  |  |  | PASS / SPLIT |

只有前三项都成立，且剩余差异确属实现层，才允许维持同类。

## 3. 异类验收

对相邻类别逐对检查：

| Class pair | 最小区别 | 改变了什么 | 有无反例 | Verdict |
|---|---|---|---|---|
|  |  | input / output / causal role / lifecycle / decision semantics |  | PASS / MERGE / REDEFINE |

若只能说“用了不同网络”或“作者叫法不同”，应合并。

## 4. 前六篇重点成对问题

### LAW ↔ Epona

- 部署规划路径是否功能等价？
- 两者训练图的 world/action 关系是机制家族相同，还是仅有宽泛相似性？
- 若完整签名不同，差异是否重要到足以表达论文核心？
- 若完整签名相同，能否从签名重建两者关键学习边？

### LAW / Epona ↔ DriveLaW

- DriveLaW 是否在部署期真正消费 future-generation carrier？
- 这条在线边是否足以形成明确的机制分界？
- 完整 future video 与内部生成 hidden state 是否被正确区分？

### World4Drive ↔ WorldDrive ↔ WoTE

- 三者是否都满足显式候选身份持续到共同 resolver？
- candidate-specific consequence 是终点摘要、时间展开，还是 deployed surrogate？
- resolver 分别优化事实模式兼容、整体规划价值、分解 planning reward，还是存在混合？
- teacher 生成的 future 与部署时实际消费的 carrier 是否被混淆？

## 5. 体系级评分

每项 0–2 分：

```text
0 = 失败或不可审计
1 = 部分成立/仍有边界问题
2 = 清楚、证据充分、可复用
```

| 检查项 | 分数 | 备注 |
|---|---:|---|
| 每轴问题单一且定义清晰 |  |  |
| `∅` / UNKNOWN / N/A 区分清晰 |  |  |
| 同功能异实现成功合并 |  |  |
| 不同因果机制成功拆分 |  |  |
| Runtime / Learning 生命周期无泄漏 |  |  |
| Learning 顺序、方向和参数作用域可重建 |  |  |
| 候选身份与 resolver 语义清晰 |  |  |
| 混合 objective 未被单标签抹平 |  |  |
| paper/code/mode 版本边界清晰 |  |  |
| 完整签名碰撞都有合理解释 |  |  |
| 单例类别不是论文专属命名 |  |  |
| 只看签名能重建核心训练/部署图 |  |  |

总分 24：

```text
22–24  可接受为 12 篇内部稳定地图（S2）
18–21  有价值但需局部修订（S1+）
12–17  轴或类别存在结构性问题（S1）
0–11   退回机制图阶段重做（S0）
```

任何一项出现“训练模块误记为在线机制”“paper/code 混合成虚构系统”“以实现差异冒充机制差异”，即使总分达标也不得通过。
