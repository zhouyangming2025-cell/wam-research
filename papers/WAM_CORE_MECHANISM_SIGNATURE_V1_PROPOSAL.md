# WAM 核心机制双层签名 V1（历史提案，待证伪）

> 状态：HISTORICAL PROPOSAL — 非 canonical ontology；下一轮须按 `handoff/core_mechanism_12/` 从 12 篇机制图重新发现并攻击本提案
> 适用范围：planning-centric World-Action Model / driving world model
> 分类单位：**固定论文版本或代码版本下，一个明确的规划推理模式**
> 配套压力测试：[WAM_CORE_MECHANISM_SIGNATURE_V1_STRESS_TEST.md](WAM_CORE_MECHANISM_SIGNATURE_V1_STRESS_TEST.md)

---

## 0. 为什么需要这套新签名

早期工作先后经历了两种组织方式：

1. 按论文和审计维度填表，适合保管证据，但会把传感器、表示、训练、部署和评价混在一起；
2. 把论文放进“当前状态 → 轨迹提议 → 候选后果 → 候选评价”的共同链，能解释路线关系，但仍难以编码训练期才存在的核心机制。

对应的历史材料保留在：

- [WAM_SIX_PAPER_UNIFIED_MODULE_AUDIT.md](WAM_SIX_PAPER_UNIFIED_MODULE_AUDIT.md)
- [WAM_ROUTE_MODULE_ABSTRACTION_SAMPLE.md](WAM_ROUTE_MODULE_ABSTRACTION_SAMPLE.md)

本提案不覆盖这两份材料。它们记录了从“逐篇比较”到“功能接口分类”的思路变化。

本轮进一步确认：一篇 WAM 论文通常同时包含两个不同的因果图。

```text
部署图：实际推理时，world information怎样改变最终动作？

学习图：训练时，future/world supervision怎样进入部署模块的参数？
```

如果把二者压进一个平面维度，会发生三类错误：

- 把训练期生成器误写成部署期在线想象；
- 把相同部署路径、不同学习机制的论文说成完全相同；
- 为每种训练细节制造新的部署路线类别。

因此核心机制改用双层签名：

```text
Runtime = A? + B? + C? + D?
Learning = L{...}

FullMechanism = Runtime ⊕ Learning
```

其中 Runtime 每个轴只能取一个主值；Learning 是受控的学习边集合。

---

## 1. 分类对象与证据边界

### 1.1 签名不直接绑定论文标题

签名的最小单位是：

```text
(paper/code artifact, version, task mode, planning inference path)
```

原因包括：

- 同一论文可能有 planning、simulation、generation 等不同推理模式；
- 论文机制和公开代码可能不一致；
- 后续代码版本可能替换原始规划路径；
- perception-free 与 perception-based 实现可能具有不同 Runtime。

默认签名对象是论文声称的**主要规划部署路径**。如果公开源码不同，必须单独给源码版本签名，不能把二者拼成一个不存在的系统。

### 1.2 什么进入核心签名

只有改变以下问题答案的差异才进入 Runtime 或 Learning：

```text
最终动作怎样产生和选择？
部署时存在什么world/future object？
world information通过哪条在线边进入决策？
候选resolver实际优化什么语义？
future/world supervision通过什么学习边写入部署模块？
```

以下内容默认属于审计属性，不单独创建路线类别：

```text
传感器类型
RGB / BEV / latent / token / hidden state
CNN / Transformer / DiT
regression / diffusion / flow
latent维度、query数量、采样步数
target来源、detach/freeze状态
其他车辆是否对ego candidate反应
论文和代码的证据强度
```

如果某项属性改变了语义输入、语义输出或因果路径，它才升级为核心类别。

---

## 2. Runtime 签名

### 2.1 A：最终决策拓扑

A 描述最终动作经过什么样的决策结构产生，不描述内部网络。

### A1：直接策略

```text
context → action / trajectory
```

判定条件：

- 没有一组身份持续到共同 resolver 的显式候选；
- 可以输出分布、使用扩散/flow、进行多次采样或内部迭代；
- 只要这些样本没有作为同一候选池进入共同选择，仍属于 A1。

### A2：层级策略

```text
context → semantic decision / intent → action
```

判定条件：

- 中间 decision/intent 具有独立语义；
- 它是后续动作生成的条件；
- 系统不要求保留一组候选到最终 argmax。

“先产生一个高层决策，再编辑动作 token”属于 A2；普通隐藏层不属于 A2。

### A3：显式候选选择

```text
context → {A1, A2, ..., AK}
                  ↓
             common resolver
                  ↓
                  A*
```

判定条件：

- `Ak` 的候选身份在 proposal 之后继续存在；
- 所有候选进入可比较的共同 resolver；
- 最终通过 score、reward、mode probability 或 criterion 选出 `A*`。

多个随机样本、多个 decoder query 或多个可视化轨迹不自动构成 A3。

---

### 2.2 B：部署期 world carrier

B 描述部署时真正位于规划因果路径上的 world/future object。普通 observation encoder 输出不自动算 world carrier。

### B0：无独立在线 world/future carrier

```text
world knowledge
→ 只保留在参数、普通encoder或runtime scorer中
```

训练期 predictor、teacher 或生成器被删除，或者在线生成结果不影响动作时，必须记为 B0。

### B1：在线当前/中间世界状态

```text
current/history context
→ dedicated world-state transform/refinement W
→ planning
```

`W` 是明确的 world-state 运算结果，但不表示“执行某条候选后的未来后果”。

### B2：直接策略使用的 future-derived carrier

```text
context
→ future-oriented generation/prediction state U
→ direct or hierarchical policy
```

`U` 可以是生成过程 hidden state、预测未来特征或压缩摘要；关键是它在线进入策略，但不按候选动作分叉。

### B3：候选条件终点/摘要后果

```text
(S, Ak) → O(Ak)
```

每个候选具有专属后果，但 `O(Ak)` 只表示一个终点、摘要或非展开式 future object。

### B4：候选条件时间展开

```text
(S, Ak) → O1(Ak), O2(Ak), ..., OH(Ak)
```

候选分支沿物理未来时间持续存在。神经网络层数、diffusion steps、flow solver steps 或内部 refinement rounds 不构成 B4。

---

### 2.3 C：部署期 world-policy 耦合

C 只描述实际影响最终动作的在线边。

### C0：无在线 world→decision 边

```text
context → policy / scorer → action
```

训练期存在 world model 不改变 C0。

### C1：world/future carrier 单向进入 policy

```text
W or U → policy/proposal → action
```

policy读取 world state 或 future-derived feature，但 prospective action 不先进入该 carrier 并产生候选专属后果。

### C2：candidate → consequence → selection

```text
Ak → O(Ak) → resolver → A*
```

候选动作先进入 consequence model，候选后果再参与共同选择。

### C3：同一决策内 world ↔ policy 迭代互馈

```text
world state → policy refinement
      ↑             ↓
      └──── feedback ┘
```

必须同时存在两个方向的在线信息边，并在同一次决策中至少完成一次反馈。单纯堆叠 Transformer blocks、增加 denoising steps 或递归 world rollout 不属于 C3。

---

### 2.4 D：最终决策语义

D 回答：最终 resolver 认为“好候选”是什么意思。

### D0：无显式候选 resolver

用于 A1/A2。最终动作由直接或层级策略解码，不存在共同候选比较。

### D1：事实/示范模式兼容性

```text
high score
≈ 更像训练数据中的事实轨迹、事实future或获胜模式
```

它不等价于安全价值，也不代表所有候选都拥有真实反事实监督。

### D2：规划效用

高分表示候选在安全、舒适、进度、规则或综合驾驶质量上更值得执行。

```text
D2a  整体标量价值、偏好或排序
D2b  分解式reward/cost预测后再聚合
```

D2a/D2b 是 D2 内部子类，不与 D2并列。

### D3：world/dynamics consistency

```text
high score
≈ 更符合world reconstruction、transition stability、future plausibility
   或其组合criterion
```

D3只有在该 criterion 训练了部署期 selector，并决定最终候选时才成立。单纯拥有 world reconstruction loss 不属于 D3。

---

## 3. Learning 签名

Learning 使用受控边集合：

```text
Learning = L{Lx, Ly, ...}
```

它记录 future/world knowledge 如何写入 Runtime，而不是重复所有 loss。

### L1：predictive pretraining → encoder/backbone transfer

```text
predictive/world pretraining
→ transfer encoder/backbone
→ predictor不进入主要规划部署图
```

### L2a：predicted action-conditioned auxiliary world learning

```text
state → predicted action
(state, predicted action) → world/future prediction
world loss → state and action policy
```

要求模型自己的 action 位于 world branch 前向路径中，并能够接收 world/future loss 的训练影响。

### L2b：shared-state sibling co-training

```text
shared state S
├→ policy head
└→ world/future head
```

两个分支通过共享状态/参数接受共同训练，但 predicted action 不构成 world branch 的必要前向输入。

### L3：shared world-action sequence/backbone multi-task learning

```text
shared sequence/backbone
→ world task
→ policy task
→ joint world-policy task
```

要求世界和动作在同一主干、序列接口或共享参数体系中接受多任务学习；不要求部署时生成 future world。

### L4：heavy consequence teacher → deployed online surrogate

```text
heavy world/consequence teacher
→ future/consequence representation distillation
→ lightweight online surrogate
```

L4与 L5可以同时存在：一个教“会发生什么”，另一个教“哪个候选更好”。

### L5：world/simulator criterion → proposal、标签或 runtime scorer

```text
world model / simulator / rule criterion
→ candidate label, pseudo teacher or score target
→ deployed proposal/scorer
```

训练期 world computation可以完全消失；其决策知识被压缩进候选分布或 selector。

### L6：factual next-state consistency → online current-world state

```text
input at t   → W_t
input at t+1 → stop-gradient W_{t+1}

consistency(W_t, W_{t+1})
→ shape deployed current-world state
```

它不自动等于 action-conditioned transition learning。

### L7：runtime world与policy模块端到端联合训练

部署时保留的 world carrier、policy和 resolver 在同一训练体系中通过任务 loss 联合优化。若只转移 frozen encoder，使用 L1；若只从离线 teacher 学习，使用 L4/L5。

---

## 4. 类型约束与判定顺序

### 4.1 合法组合

```text
B0 → C0
B1/B2 → C1 或 C3
B3/B4 → C2 或 C3

A1/A2 → D0
A3 → D1 / D2 / D3
```

补充约束：

- A3并不要求 B3/B4；候选可以直接由普通 scorer 选择；
- B3/B4要求候选身份存在，因此通常与 A3共同出现；
- 在线计算但不影响最终动作的 future branch 不进入 B/C；
- 训练期 world model被删除时，Runtime必须是 B0+C0；
- `flow time`、`denoising iteration`、`planner refinement` 与物理 future horizon分别记录。

### 4.2 固定判定顺序

对任何新论文按以下顺序分类：

```text
1. 锁定paper/code版本和主要planning mode。
2. 只画部署图，删除所有training-only节点。
3. 判断最终是直接/层级策略还是显式候选选择 → A。
4. 找到实际影响动作的在线world/future object → B。
5. 沿因果边追踪world information怎样进入决策 → C。
6. 读取最终resolver的监督和score语义 → D。
7. 回到训练图，记录future/world knowledge写入Runtime的边 → Learning。
8. 最后填写表示、监督来源、梯度、反应性和证据属性。
```

---

## 5. 两级等价关系

### 5.1 部署路线等价

```text
Runtime_i = Runtime_j
```

表示两篇论文在部署时具有相同的主要决策拓扑、world carrier、在线耦合和决策语义。

### 5.2 核心机制等价

```text
Runtime_i = Runtime_j
且
Learning_i = Learning_j
```

表示部署路线和关键知识写入方式均相同。此时不同 backbone、loss parameterization 或 substrate 才被视为实现差异。

因此 LAW 与 Epona可以是**部署路线等价**，但不是**完整核心机制等价**。

---

## 6. 六篇正式投影

### 6.1 LAW

```text
Runtime  = A1 + B0 + C0 + D0
Learning = L{L2a}

FullMechanism = A1+B0+C0+D0 ⊕ L{L2a}
```

重建：planner先输出单条轨迹；预测轨迹进入辅助 future-latent predictor；future loss训练状态和规划路径；部署时 predictor/future output 不参与动作选择。

边界：事实 future target 被 detach；没有在线 candidate consequence。

证据：[LAW原文](raw_md/P0048_LAW/P0048_LAW.raw.md)、[接口源码审计](../audits/literature/PHASE_B_WAVE2_INTERFACE_CODE_AUDIT.md)

### 6.2 Epona

```text
Runtime  = A1 + B0 + C0 + D0
Learning = L{L2b}

FullMechanism = A1+B0+C0+D0 ⊕ L{L2b}
```

重建：shared historical state分别进入 trajectory generator 与 visual future generator；两类 loss共同塑造 shared state；planning mode 可只运行 trajectory branch。

边界：视觉分支训练使用事实 ego motion，不读取 TrajDiT刚预测的轨迹，因此不属于 L2a。

证据：[Epona原文](raw_md/P0001_Epona/P0001_Epona.raw.md)、[源码审计](../audits/literature/PHASE_C5_EPONA_SOURCE_AUDIT.md)

### 6.3 DriveLaW

```text
Runtime  = A1 + B2 + C1 + D0
Learning = L{L1, L7}

FullMechanism = A1+B2+C1+D0 ⊕ L{L1,L7}
```

重建：Video-DiT在线产生future-generation internal carrier；Action-DiT读取该 carrier直接生成轨迹；没有候选动作→候选后果→共同选择。

边界：planner读取的是生成过程状态，不要求完成RGB解码；future-noise、采样步数和block数量不改变签名。

证据：[DriveLaW原文](raw_md/P0009_DriveLaW/P0009_DriveLaW.raw.md)、[源码审计](../audits/literature/PHASE_C6_DRIVELAW_AUDIT.md)

### 6.4 World4Drive

```text
Runtime  = A3 + B3 + C2 + D1
Learning = L{L7}

FullMechanism = A3+B3+C2+D1 ⊕ L{L7}
```

重建：显式意图候选分别产生candidate future latent；事实 future用于定义获胜mode；ScoreNet在部署机制中选择高分候选。

边界：只有一条事实 future，不是K条干预真值。锁定公开推理源码未完整复现论文规定的 ScoreNet argmax，因此该签名首先是**论文机制签名**，源码等价性保持 partial。

证据：[World4Drive原文](raw_md/P0046_World4Drive/P0046_World4Drive.raw.md)、[源码审计](../audits/literature/PHASE_C5_WORLD4DRIVE_AUDIT.md)

### 6.5 WorldDrive

```text
Runtime  = A3 + B3 + C2 + D2a
Learning = L{L4, L5}

FullMechanism = A3+B3+C2+D2a ⊕ L{L4,L5}
```

重建：base planner提出并筛选候选；heavy TA-DWM教 lightweight FAR候选后果表示；PDMS/oracle preference教候选排序；部署保留轻量 future surrogate 和整体偏好评分。

边界：future latent distillation与value/preference learning是两条不同学习边。

证据：[WorldDrive原文](raw_md/P0042_WorldDrive/P0042_WorldDrive.raw.md)、[源码审计](../audits/literature/PHASE_C5_WORLDDRIVE_AUDIT.md)

### 6.6 WoTE

```text
Runtime  = A3 + B4 + C2 + D2b
Learning = L{L7}

FullMechanism = A3+B4+C2+D2b ⊕ L{L7}
```

重建：显式候选分别进行recurrent future-BEV rollout；当前/未来状态和轨迹进入多个规划 reward head；聚合碰撞、可行驶区域、TTC、舒适性、进度和模仿等指标后选择候选。

边界：已审计 target path 中周围车辆 future 对不同 ego candidate固定，不支持 reactive multi-agent counterfactual claim。

证据：[WoTE原文](raw_md/P0045_WoTE/P0045_WoTE.raw.md)、[接口源码审计](../audits/literature/PHASE_B_WAVE2_INTERFACE_CODE_AUDIT.md)

---

## 7. 六篇签名揭示的结构

```text
LAW / Epona
相同 Runtime：A1+B0+C0+D0
不同 Learning：L2a vs L2b

DriveLaW
仍是直接策略，但增加在线future-derived carrier：B2+C1

World4Drive / WorldDrive / WoTE
共享：A3 + candidate consequence + C2
区别：后果时间结构 B3/B4 + resolver语义 D1/D2
```

因此新的主比较问题不再是“谁使用了什么 latent”，而是：

```text
world knowledge是否只通过参数存在？
是否有独立在线carrier？
carrier是否被candidate action分叉？
后果是endpoint还是temporal rollout？
最终选的是事实模式、规划价值还是world consistency？
训练知识通过哪条边进入部署模块？
```

---

## 8. 审计属性模板

每个正式签名后附下面的属性账，但属性不自动改变类别：

```yaml
subject:
  paper_version:
  code_commit:
  task_mode:

representation:
  sensors:
  current_state_substrate:
  world_carrier_substrate:

learning_evidence:
  future_target_source:
  candidate_target_coverage:
  gradient_path:
  stop_gradient_or_freeze:

causal_boundary:
  candidate_conditioned_output:
  alternative_action_ground_truth:
  reactive_other_agent_truth:
  intervention_validation:

evidence:
  paper_status:
  source_status:
  paper_code_equivalence:
  unresolved:
```

---

## 9. 验收测试

### 9.1 重建测试

只给读者 Runtime 与 Learning，读者应能恢复：

- 动作是直接产生还是候选选择；
- 部署时是否存在future/world object；
- world information如何影响最终动作；
- resolver在优化什么；
- future/world knowledge如何写入部署模块。

### 9.2 碰撞测试

若两篇论文被认为具有不同核心机制，却得到完全相同的 FullMechanism，必须：

1. 检查差异是否真的只是实现属性；
2. 若差异改变语义输入/输出或因果边，修订类别定义；
3. 不得为了论文名称不同而直接添加新类别。

### 9.3 不变性测试

在语义接口不变时替换：

```text
regression ↔ diffusion ↔ flow
RGB ↔ BEV ↔ latent ↔ token
Transformer ↔ DiT ↔ recurrent model
```

签名必须保持不变。

### 9.4 生命周期测试

如果 world/future branch在主要规划部署时被删除或旁路，B/C不得写成在线 future类别。

### 9.5 候选测试

只有候选身份持续到共同 resolver 才能归入 A3。多模态输出、多个 query、随机采样和可视化分支都不充分。

### 9.6 版本测试

论文机制、公开源码、后续重构版本和不同 task mode必须能够拥有不同签名。

---

## 10. 扩展规则

只有满足以下条件才能增加新类别或新主轴：

```text
1. 现有签名无法重建一个重要机制；
2. 缺失差异改变部署决策图或学习知识流；
3. 差异不是论文专属模块名或实现细节；
4. 至少能反投影检查一个已有anchor；
5. 新类别具有定义、正例、反例、类型约束和证据要求。
```

遇到新论文时，先完成现有签名，再记录无法表达的 residue；不得见到新术语就扩轴。
