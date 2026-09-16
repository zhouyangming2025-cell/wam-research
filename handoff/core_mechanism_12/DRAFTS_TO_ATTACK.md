# 现有草案的已知漏洞：必须攻击，不得继承

## 0. 定位

现有双层签名 V1 提出：

```text
Runtime = A? + B? + C? + D?
Learning = L{...}
FullMechanism = Runtime ⊕ Learning
```

它比“12 个维度 × 论文填表”前进了一步，但尚未达到 canonical ontology 的稳定程度。下面是交接前反复自审得到的失败点。新会话需要从证据重新判断，不得把本文件当成修订答案。

## 1. 完整机制等价定义过强

旧说法：

```text
Runtime 相同                    → 部署路线等价
Runtime 和 Learning 标签相同    → 核心机制等价
```

反例风险：LAW 与 Metis 可能都被压成 `A1+B0+C0+D0 ⊕ L2a`，但两者只共享“训练期 world loss 可塑造 action policy”的高层家族；具体 action 条件、mask、共享参数、生成对象和梯度路径并不同。

需要检验是否至少分为：

```text
Runtime 同构                         → deployment-route equivalence
Runtime + learning family 相同        → mechanism-family equivalence
参数化 learning DAG 也同构            → core-mechanism equivalence
```

这只是待验证方案。

## 2. Learning 不能是无序集合

`L{L1,L4,L5}` 丢失：

- 先预训练后迁移，还是共同训练；
- teacher 和 student 谁产生什么；
- 哪条 loss 反传到哪些参数；
- 哪些节点 freeze/detach；
- 部署保留什么。

新体系必须保留方向、阶段和并行关系。标签可以作为索引，但不能替代 DAG。

## 3. Resolver 可能不是单值语义

DynFlowDrive 的候选 criterion 包含轨迹误差、重建误差与 dynamics/stability score 的混合。若强制只取一个 D 类，会丢掉论文核心。

新体系要检验：

```text
primary resolver semantics
+ composition expression
+ component provenance
```

是否比单值类更合理。

## 4. “当前 world state”容易退化成任意 hidden state

如果只凭“有时序 latent/graph/BEV”就归入在线 world carrier，普通 encoder 会全部被包装成 world model。GraphWorld 是关键压力点。

新体系必须给出可执行门槛与负例，而不是靠作者自称。

## 5. “联合训练”信息量太低

旧 `L7 runtime world 与 policy 端到端联合训练` 过宽，容易重演早期 `joint=yes` 的无意义整理。必须回答是哪条 supervision/gradient edge、何时训练、哪些参数共享。

## 6. 轴之间可能不独立

旧 A（最终决策拓扑）、B（world carrier）、C（world-policy coupling）、D（resolver semantics）可能存在：

- A 与 D 的类型依赖被误当成两个自由轴；
- B 与 C 重复编码同一条在线边；
- 直接策略/层级策略/候选选择混合了拓扑与语义层级；
- “未来 carrier 类型”与“是否按候选分叉”可能应拆成两个问题。

新会话需要做最小充分性测试：删掉任一轴是否丢信息；合并任意两轴是否造成非法组合或重复。

## 7. 12 篇覆盖不等于领域完备

12 篇足以形成一个高质量内部机制地图，并检验明显漏洞；不足以证明对所有未来 WAM 论文闭包。最终最多宣称内部 `S2`，外部盲测后才能宣称 `S3`。

## 8. 已知容易误判的论文

```text
LAW vs Epona
  部署路径可能同族，但学习机制不能只写“实现不同”就跳过；要判断差异是否改变核心学习因果图。

SeerDrive
  paper 的 iterative co-refinement 与 released code 不同。

Drive-JEPA
  predictive pretraining、proposal distillation、perception-free 与 perception-based 路径不能揉成一个签名。

Metis
  训练期 action→world 条件与 world loss→policy，不代表部署在线生成 future。

DynFlowDrive
  world criterion 在训练期压缩到 runtime scorer，不是在线 candidate rollout。

Discrete-WAM
  decision vocabulary 不自动等于 runtime candidate bank；共享 token backbone 也不自动等于在线 world carrier。

GraphWorld
  flow refinement 不是物理时间 rollout；current world state 与普通 planner hidden state 的边界必须证成。
```

## 9. 旧草案的合理保留点也必须重新证明

旧草案中较有价值、但仍需证据复核的原则：

- Runtime 与 Learning 分离；
- 分类单位版本化、模式化；
- 表示基底通常是属性而非核心机制；
- 候选身份与共同 resolver 是显式候选路线的必要条件；
- 训练期 future branch 不可冒充部署期 online imagination；
- 同功能异实现应合并。

新会话若保留它们，要给出 12 篇上的证据和反例测试，不能因为它们“听起来合理”就直接继承。
