# WAM 路线模块抽象样板（供审阅）

> 样板模块：未来信息如何进入规划决策
> 对象：LAW / Epona / DriveLaW / World4Drive / WorldDrive / WoTE
> 状态：DRAFT — 用于确认分类粒度，不替换完整证据审计

---

## 1. 这次分类要回答什么

本模块只回答一个路线级问题：

> 在实际部署时，模型是否计算某种未来信息；如果计算，它以什么方式影响最终轨迹？

这决定了论文位于完整规划链的哪个位置：

```text
历史观测 → 当前状态 S → 轨迹提议 {Ak}
                         ↓
                  候选后果 O(Ak)
                         ↓
                     评分 V(Ak)
                         ↓
                    最终轨迹 A*
```

本模块不试图回答“哪种编码器更好”“哪种扩散噪声更合理”或“哪个 latent 更丰富”。这些问题可以单独研究，但不会自动改变论文在上述决策链中的位置。

---

## 2. 分类规则：什么时候可以认为两篇论文在做同一件事

若两篇论文对下面三个问题给出相同答案，本模块就把它们归为同一类：

1. 部署时是否计算 future-derived object？
2. 该 future object 是否针对多条 prospective candidate actions 分叉？
3. 该 future object 是否直接参与最终轨迹选择？

形式化地说，本模块使用下面的等价关系：

```text
paper_i ~ paper_j

当且仅当二者具有相同的部署接口：

(future online?, candidate-conditioned?, selection-coupled?)
```

因此，两个模型即使采用不同 backbone、token、loss 或 diffusion 实现，只要部署接口相同，就可以先放入同一路线类。反过来，两个模型即使都声称“预测未来”，只要一个未来分支仅用于训练、另一个未来结果直接决定选哪条轨迹，就不能归成同一类。

---

## 3. 一级路线分类

### A 类：未来只负责训练，部署时不读取预测未来

统一计算图：

```text
训练：
历史观测 → S → planner → A
             └→ future task → T_hat ← factual future T

部署：
历史观测 → S → planner → A*
```

判定条件：

```text
future online?          NO
candidate-conditioned?  NO / 不构成候选池
selection-coupled?      NO
```

归入论文：

```text
LAW
Epona
```

它们的共同路线意义是：

> 未来观测在训练时塑造参数或当前状态 `S`，但部署时 planner 不读取预测 future object。

LAW 与 Epona 的具体梯度路径不同：LAW 把自身预测的单条轨迹送入辅助 future predictor；Epona 的视觉生成和轨迹生成主要通过共享 `S` 发生联系。这个差异应保留在证据账中，但在当前路线问题下，它不需要把 A 类再拆成两条路线，因为两者部署图相同：`S → planner → A*`。[LAW 原文][LAW-P] [LAW 接口审计][LAW-S] [Epona 源码审计][EPONA-S]

### B 类：在线读取未来生成过程，但不做候选后果比较

统一计算图：

```text
历史观测 + future-noise canvas
              ↓
        future generator internal state U
              ↓
          direct planner
              ↓
             A*
```

判定条件：

```text
future online?          YES
candidate-conditioned?  NO
selection-coupled?      NO explicit candidate selection
```

归入论文：

```text
DriveLaW
```

它的路线意义不是“也用未来视频监督”，而是：

> 部署时保留 Video-DiT 的一次在线计算，Action-DiT直接读取生成过程内部状态 `U`；但系统没有先提出 K 条轨迹、再分别预测 K 个后果并打分。

噪声如何注入、Video-DiT 有多少层、是否完整解码 RGB，不是本模块的一级分类依据。只有当这些细节改变 `U` 是否在线、是否位于 planner 输入路径时，才升级为路线差异。[DriveLaW 原文][DRIVELAW-P] [DriveLaW 源码审计][DRIVELAW-S]

### C 类：为显式候选预测后果，并用后果选择轨迹

统一计算图：

```text
当前状态 S → proposal → {A1, A2, ..., AK}
                         ↓
                  O(A1), ..., O(AK)
                         ↓
                  V(A1), ..., V(AK)
                         ↓
                    argmax → A*
```

判定条件：

```text
future online?          YES
candidate-conditioned?  YES
selection-coupled?      YES
```

归入论文：

```text
World4Drive
WorldDrive
WoTE
```

它们的共同路线意义是：

> future object不再只是训练教师，而是候选轨迹的在线决策证据；如果改变 `O(Ak)` 或 `V(Ak)`，最终选择 `A*` 可能随之改变。

三篇的后果载体不同——compact latent、teacher-distilled latent、recurrent BEV——但这些差异不改变 `Ak → O(Ak) → V(Ak) → A*` 这一部署接口，因此先归入同一 C 类。[World4Drive 原文][WORLD4DRIVE-P] [WorldDrive 源码审计][WORLDDRIVE-S] [WoTE 原文][WOTE-P]

---

## 4. 六篇论文的一级归类

| Paper | 一级路线类 | 部署时真正保留的 future 接口 | 本模块不据此拆类的实现差异 |
|---|---|---|---|
| LAW | A | 无；future branch只留下参数影响 | visual/BEV latent、MSE、action-aware auxiliary path |
| Epona | A | 无；planning mode读取共享 `S` | MST、VisDiT、TrajDiT、rectified flow细节 |
| DriveLaW | B | Video-DiT first-pass internal state `U` | noise reinjection、block数量、RGB decoder |
| World4Drive | C | candidate future latent → ScoreNet（论文图） | depth/semantic prior、K=6、latent维度 |
| WorldDrive | C | lightweight FAR candidate consequence/reward | heavy teacher结构、distillation实现、top-K大小 |
| WoTE | C | candidate future-BEV sequence → reward | BEV尺寸、recurrent rollout步数、N=256 |

注意：World4Drive 的论文路线属于 C，但锁定公开源码的 `simple_test_pts` 没有复现论文规定的 `argmax(ScoreNet)`，而是使用已观测当前特征计算 reconstruction/KL/cosine 最小索引。因此“论文路线归 C”与“公开部署实现已完整验证”是两件事；后者必须保留为 `UNKNOWN/partial`。[World4Drive 推理源码][WORLD4DRIVE-CODE]

---

## 5. 什么应当折叠，什么绝对不能折叠

### 5.1 在当前模块中可以折叠的差异

以下差异通常不改变 A/B/C 归类：

| Difference | 为什么暂时不关心 |
|---|---|
| CNN / Transformer / DiT / BEV encoder | 不直接决定 future 是否在线进入选择 |
| latent、token、feature、BEV 的命名 | 名称不决定决策因果位置 |
| 噪声调度、采样步数、注入位置 | 除非改变部署接口，否则属于实现层 |
| 是否能把 latent 解码成 RGB | 可视化能力不等于规划器消费完成 future |
| latent维度、query数量、block数量 | 主要影响容量和成本，不直接定义路线 |
| 单篇论文自己的模块名 | 不适合作为跨论文分类标准 |

### 5.2 必须保留的差异

以下差异一旦被折叠，就会产生错误结论：

| Difference | 为什么必须保留 |
|---|---|
| future只训练还是在线计算 | 区分 A 与 B/C |
| planner读取 `S`、内部 `U` 还是候选后果 `O(Ak)` | 决定 future information access point |
| prospective action是否在预测后果之前进入 | 区分一般条件信息与候选干预 |
| 是否存在显式 K 候选及共同 scorer | 区分随机采样与真正候选选择 |
| future-derived quantity是否改变 `A*` | 判定是否真正 selection-coupled |
| target来自事实 future、teacher还是 simulator | 决定证据含义和偏差来源 |
| 其他交通参与者是否随 ego candidate反应 | 决定是否能声称 reactive counterfactual reasoning |

### 5.3 需要按研究问题决定是否保留的差异

| Difference | 研究路线位置时 | 研究机制归因/可信度时 |
|---|---|---|
| LAW 与 Epona 的梯度拓扑 | 可作为 A 类内部注释 | 必须保留，因为决定 future loss如何影响 planner |
| C 类三篇的 scorer target | 不必拆成三条主路线 | 必须保留：mode matching、PDMS preference、explicit reward不是同一种价值 |
| candidate count | 不决定是否属于 C 类 | 必须控制，否则 coverage 与 evaluator质量混杂 |
| representation substrate | 可以统一记为 `S/O(Ak)` | 讨论计算成本、可解释性和信息瓶颈时必须恢复 |

---

## 6. 为什么 C 类既应该合并，又不能“全部说成一样”

C 类共享同一个路线接口：

```text
Ak → O(Ak) → V(Ak) → A*
```

所以讨论“未来是否直接参与候选选择”时，World4Drive、WorldDrive、WoTE 应归为一类。

但如果问题改成“`V(Ak)` 是否代表真实安全价值”，分类轴就变了，C 类内部必须恢复三个证据标签：

| Paper | `O(Ak)` / `V(Ak)` 的监督来源 | 能支持的最强解释 | 不能支持的解释 |
|---|---|---|---|
| World4Drive | K 个预测输出竞争匹配一条 factual future；nearest mode训练 ScoreNet | 事实模式匹配 | K 个真实反事实后果、安全价值 |
| WorldDrive | frozen TA-DWM teacher latent + PDMS/oracle preference | teacher定义的候选后果与偏好 | 真实环境的干预结果 |
| WoTE | candidate ego rollout + simulator/reward targets；已审计路径中他车 future固定 | 固定日志他车条件下的候选评价 | 他车会响应 ego 的真实 reactive counterfactual |

这说明正确做法不是永远保留所有细节，也不是永远丢掉所有细节，而是：

> 先确定要回答的问题，再保留足以改变该问题答案的最小信息。

---

## 7. 建议用于整篇重写的固定样板

以后每个路线模块只保留下面七项：

```text
1. 模块问题
   我们到底要用这个模块回答什么？

2. 等价判据
   哪几个接口相同，就认为论文在做同一件事？

3. 一级类别
   A/B/C... 每类只写统一计算图和必要条件。

4. 论文归类
   每篇只给类别、关键证据和边界，不逐篇复述完整架构。

5. 可折叠差异
   明确本模块主动忽略什么。

6. 不可折叠差异
   明确哪些差异会改变路线、证据语义或因果解释。

7. 分类失效条件
   如果研究问题改变，何时必须把某一类重新拆开？
```

这个样板的核心不是减少事实，而是把事实分成两层：

```text
主文：决定路线位置的最小充分信息
证据账：防止错误归类所需的实现、梯度和监督边界
```

---

[LAW-P]: raw_md/P0048_LAW/P0048_LAW.raw.md
[LAW-S]: ../audits/literature/PHASE_B_WAVE2_INTERFACE_CODE_AUDIT.md
[EPONA-S]: ../audits/literature/PHASE_C5_EPONA_SOURCE_AUDIT.md
[DRIVELAW-P]: raw_md/P0009_DriveLaW/P0009_DriveLaW.raw.md
[DRIVELAW-S]: ../audits/literature/PHASE_C6_DRIVELAW_AUDIT.md
[WORLD4DRIVE-P]: raw_md/P0046_World4Drive/P0046_World4Drive.raw.md
[WORLD4DRIVE-CODE]: ../repos/World4Drive/projects/mmdet3d_plugin/W4D/W4D.py
[WORLDDRIVE-S]: ../audits/literature/PHASE_C5_WORLDDRIVE_AUDIT.md
[WOTE-P]: raw_md/P0045_WoTE/P0045_WoTE.raw.md
