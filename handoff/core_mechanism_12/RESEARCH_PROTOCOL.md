# 12 篇核心机制本体研究协议

## 1. 研究问题

目标不是回答“每篇用了什么模块”，而是回答：

```text
在一段式自动驾驶中，world/future information
通过什么训练与部署因果机制改变最终驾驶决策？
```

本体需要同时做到压缩和区分：

- 压缩：同功能、异实现的论文落入同一机制类；
- 区分：不同因果作用、不同生命周期或不同决策语义不能被相似术语掩盖；
- 留空：论文没有该机制时明确为 `∅`；
- 守界：证据不足时为 `UNKNOWN`，不得用常识补齐。

## 2. 分类对象

最小对象固定为：

```text
Artifact = (paper/code, exact version, task mode, planning inference path)
```

禁止以论文标题作为不可拆分对象。一个标题下可以有多个 Artifact，例如：

- 原论文机制与公开代码机制；
- perception-free 与 perception-based planner；
- train-time teacher path 与 deployed student path；
- planning、generation、simulation 等不同模式。

如果版本信息未闭合，签名必须带边界，而不是合并成一个虚构系统。

## 3. 先画图，后定轴

### 3.1 Deployment DAG 最小字段

每个 Artifact 都要显式标出：

```text
O  observation/history
S  current decision state
I  semantic intent/decision（如存在）
A  action/trajectory proposal
W  current-world carrier（如存在）
F  future/consequence carrier（如存在）
V  criterion/value/reward/compatibility（如存在）
R  resolver/selector（如存在）
A* final action/trajectory
```

这些字母只是画图时的观察词汇，不是预设分类轴，也不要求每篇都具有全部节点。

边必须说明：

```text
source → target
语义输入 / 语义输出
是否按 candidate 分叉
是否实际影响 A*
是否在线执行
```

仅在线计算但不影响 `A*` 的支路，不算 runtime decision mechanism。

### 3.2 Learning DAG 最小字段

至少标出：

```text
监督 target 的来源
world/future loss
policy/action loss
teacher / simulator / planner criterion
共享参数
梯度方向
detach / freeze
预训练 → 蒸馏 → 联合训练等阶段顺序
最终部署保留/删除哪些节点
```

学习机制必须是有向、可排序的图。`{L1,L4,L5}` 这类无序集合只能当索引，不能代替机制描述。

## 4. 何时允许建立一个机制轴

候选轴必须通过以下门槛：

1. **单一问题**：该轴回答一个清楚、可复述的问题；
2. **可观测判据**：能从论文/源码判断类别，而不是凭作者命名；
3. **功能相关**：类别差异改变语义 I/O、因果路径、生命周期或决策作用；
4. **实现不变性**：替换 backbone、表示基底或生成算法而保持功能时，类别不变；
5. **空类明确**：能证明何时为 `∅`；
6. **未知明确**：能证明何时只能为 `UNKNOWN`；
7. **组合规则明确**：若一个对象可同时有多个值，必须有组合语法，不能假装互斥；
8. **可复用**：类别定义不含论文名，且理论上可被新论文复用。

若两个候选轴在 12 篇上总是共变，仍不能据此断言它们是同一轴；要用反事实问题检查它们能否独立变化。

最终表示不必强行是固定数量的平面轴。如果层级类型、参数化边或局部组合语法更忠实，可以采用它们；但必须输出一套人能快速比较的短签名，并证明短签名没有丢失核心机制。

## 5. 类别等价判据

两种实现归为同一类，至少要求：

```text
相同语义输入
+ 相同语义输出
+ 相同生命周期位置
+ 相同决策因果作用
+ 相同候选身份语义（若涉及候选）
```

下列差异通常不拆类：

```text
regression / diffusion / flow
RGB / BEV / latent / token / hidden feature
CNN / Transformer / DiT
query 数量、latent 维度、采样步数
```

但如果这些差异进一步改变在线可用对象、分叉结构、resolver 或梯度路径，就应按改变后的机制拆类，而不是机械地忽略。

## 6. `∅`、`UNKNOWN` 与 `N/A`

```text
∅       有充分证据表明该 Artifact 不存在此机制
UNKNOWN 机制可能存在，但论文/源码证据不足
N/A     上游类型约束使该轴不适用
```

三者必须分开。例如：

- 部署时 world branch 被删除，有证据时 runtime carrier=`∅`；
- 源码未公开、论文未说明 scorer 细节时是 `UNKNOWN`；
- 没有候选池时，候选 resolver 细分可能是 `N/A`，也可能由总轴设计统一记为 `∅`，但规范必须固定一种写法。

## 7. 必须处理的困难边界

### 7.1 候选池

多个随机输出或多模态预测不自动构成显式候选选择。只有当：

```text
候选身份产生
→ 身份在中间计算中保持
→ 多候选进入共同 resolver
→ resolver 决定 A*
```

才可认定存在候选选择拓扑。

### 7.2 World carrier

不能把任意时序 hidden state 称为 world state。至少提出硬门槛，例如：

- 独立可定位的 carrier；
- 明确的 world/temporal transition、prediction 或 refinement operator；
- 明确回到 planning 的接口；
- 直接 world/temporal supervision 或其他足够证据。

门槛本身要由 12 篇反例检验，不能只写概念性描述。

### 7.3 时间与迭代

必须区分：

```text
网络深度/扩散求解步
同一决策内 world↔policy 互馈轮次
物理未来时间步 rollout
跨控制周期的闭环更新
```

### 7.4 Resolver 语义

不得把所有 score 合并成“评价”。至少检查：

```text
事实/示范模式兼容性
模态概率
轨迹误差
规划效用或偏好
分解式安全/舒适/进度 reward
world reconstruction / dynamics stability / consistency
混合加权或词典序规则
```

若目标是混合的，应给 `primary semantics + composition expression`，不能硬塞进一个纯类。

### 7.5 学习边

至少区分：

```text
预测预训练后迁移
world loss 通过预测 action 条件反传到 policy
world/policy sibling heads 仅共享 state
共享 world-action sequence/backbone 的多任务训练
heavy teacher → deployed surrogate
world/simulator criterion → label/proposal/runtime scorer
runtime world-policy 联合端到端训练
```

这些只是检查清单，不是预授权类别。最终类别要从图中重新归纳，并保留方向、阶段和参数作用域。

## 8. 证据规则

证据优先级：

```text
论文公式/正文/算法/图注
> 官方源码固定版本
> 官方 README
> 仓库 audit
> deep analysis
> 当前草案或聊天记忆
```

当论文与源码冲突时，不按优先级覆盖，而是拆分 Artifact。每个分类结论标注：

```text
PAPER FACT
CODE FACT
OUR INFERENCE
UNKNOWN
```

## 9. 必做压力测试

### Collision test

完整签名相同的对象，是否真的可以画出同构的核心训练/部署图？若不能，说明轴或学习表示丢信息。

### Split test

同一类别中的论文，差异是否只是实现；若差异改变语义 I/O 或因果作用，应拆类。

### Invariance test

把 regression 换成 diffusion、BEV 换成 latent，而保持接口不变，签名应不变。

### Lifecycle test

训练期 future branch 被删除时，runtime 不得出现在线 future carrier。

### Candidate identity test

候选必须保持身份并经过共同 resolver；随机多样性不够。

### Hybrid-objective test

混合评价不能因单值编码而丢失关键目标构成。

### Version/mode test

同标题不同 paper/code/mode 必须能分开。

### Completeness test

只看签名和参数化机制图，是否能重建决定论文核心思路的训练图和部署图？

### Anti-marketing test

隐藏论文名和作者术语后，分类是否仍可判定？

## 10. 稳定性等级

最终不要只宣布“完成”。给本体评级：

```text
S0  描述性表格，不能稳定编码新论文
S1  初步机制轴，可覆盖 12 篇但存在未解释碰撞/单例类
S2  通过全部内部压力测试，可用于这 12 篇的领域地图
S3  经外部新论文盲测仍无需改轴，仅新增已有类实例
```

本轮最多能直接证明到 `S2`。不能用 12 篇内部测试声称 `S3`。
