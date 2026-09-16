# GPT-6 可直接复制提示词：WAM 一段式核心机制本体

```text
接管 private GitHub repo：zhouyangming2025-cell/wam-research。

先切换到分支 `codex/gpt6-mechanism-handoff`；除非该分支已被合并，否则不要从默认 `main` 读取本任务。

本次只执行一个隔离任务：基于指定 12 篇论文，建立“World Model + 一段式端到端自动驾驶”的核心机制本体。不要继续仓库原有的文献扩展队列，不做 gap hunting，不设计新方法，也不要把现有 A/B/C/D 当作答案。

先依次完整读取：
1. handoff/core_mechanism_12/README.md
2. handoff/core_mechanism_12/RESEARCH_PROTOCOL.md
3. handoff/core_mechanism_12/PAPER_EVIDENCE_INDEX.md

然后按 PAPER_EVIDENCE_INDEX 读取 12 篇 raw paper Markdown。raw paper 是首要证据；source/code audit 用于版本和实现边界；deep analysis 只是二手线索。必须先独立重建机制，之后才读取：
4. handoff/core_mechanism_12/DRAFTS_TO_ATTACK.md
5. papers/WAM_ROUTE_MODULE_ABSTRACTION_SAMPLE.md
6. papers/WAM_CORE_MECHANISM_SIGNATURE_V1_PROPOSAL.md
7. papers/WAM_CORE_MECHANISM_SIGNATURE_V1_STRESS_TEST.md

用户要的不是“12 篇 × 若干描述维度”的表，而是功能机制等价类。理想分类应出现这样的现象：

论文1 = A∅
论文2 = A1
论文3 = A1
论文4 = A2

其中：论文1有证据证明没有该机制；论文2与论文3具有相同语义输入、相同语义输出和相同系统作用，即便用 regression/diffusion/flow/BEV/latent 等不同实现，也必须同类；论文4只有在因果路径、语义接口、生命周期或决策作用实质不同时才分为 A2。

这里的 A/1/2 只是用户期望的编码行为示例，不预设最终轴名、轴数或平面结构。若独立轴无法无损表达机制，可以提出带类型约束的层级语法或参数化机制图；但必须同时给出简洁、可比较的论文签名。

硬约束：
- 分类单位是 (paper/code artifact, version, task mode, planning inference path)，不是论文标题。
- 12 篇论文可以产生多于 12 个 Artifact 投影；不得为了表格“一篇一行”重新合并模式。
- 同一论文的不同部署模式必须可拥有不同签名。
- 论文机制与公开代码不一致时必须拆开记录。
- 每个轴必须有明确的 ∅（ABSENT）和 UNKNOWN；二者不可混淆。
- 训练期存在但部署删除的 world/future 分支，不得记成在线 world carrier。
- 多个随机样本不自动等于显式候选选择；候选身份必须持续到共同 resolver。
- 普通 encoder hidden state 不自动等于 world state；必须给出可检验门槛。
- diffusion step、网络层迭代、物理时间 rollout、同一决策内 world↔policy 互馈不得混淆。
- 不能按 RGB/BEV/token/latent、CNN/Transformer/DiT、regression/diffusion/flow 建核心类别，除非它改变语义接口或因果作用。
- scorer 的模式匹配、事实一致性、规划效用、安全/舒适/进度 reward、world/dynamics consistency 不得因“都是分数”而合并；混合目标允许组合表达。
- 学习机制若存在先后、并行、detach/freeze、teacher→student 或梯度方向，必须用有向/分阶段图表达，不能用无序标签集合冒充机制。
- 不允许为了让 12 篇都唯一而制造论文专属类别；完整签名碰撞可能合理，但必须解释碰撞是否表示真正等价。
- 不允许为保持现有 A/B/C/D 而扭曲论文；必要时改轴、拆轴、合轴或完全废弃。
- 不要求所有轴彼此绝对独立；允许显式类型依赖，但禁止用两个轴重复编码同一事实。

执行顺序：

Phase 0 — 固定对象与证据
- 为每篇列出 paper version、code version、规划模式、证据层级。
- 标出 SeerDrive paper/released code、Drive-JEPA perception-free/perception-based 等必须拆分的对象。

Phase 1 — 盲重建，不先分类
- 对每个对象画 deployment DAG：观测/状态/提议/世界载体/后果/评价/选择/动作。
- 对每个对象画 learning DAG：监督目标、teacher、world branch、policy branch、共享参数、梯度去向、阶段顺序、部署保留项。
- 每条边注明 TRAIN、RUNTIME 或 BOTH；不确定写 UNKNOWN。

Phase 2 — 从 12 个图中发现机制轴
- 只有一个问题能独立改变、且类别互斥或有明确组合语法时，才建立一个轴。
- 对每轴定义：研究问题、纳入门槛、∅ 条件、类别、判别算法、类型约束、非例、边界例。
- 类别命名先用中性语义名称，再分配代码；不要从论文名和模块名造类。

Phase 3 — 投影与反例攻击
- 投影全部 12 篇的每个 artifact/mode，并为每格引用原文或源码审计。
- 做 collision test、split test、invariance test、lifecycle test、candidate identity test、hybrid objective test、version/mode test、completeness test。
- 主动寻找“同类但其实机制不同”和“异类但只是实现不同”的错误。
- 若一个类别只有一篇，必须证明它是可复用机制类别而非论文专属标签。

Phase 4 — 与旧草案对抗
- 此时才审查现有双层签名 V1。
- 对每个旧轴/类别给 KEEP / MODIFY / SPLIT / MERGE / DELETE，并说明证据。
- 特别攻击：Runtime 相同 + Learning 标签相同是否真等于核心机制相同；Learning 能否是无序集合；resolver 是否需要组合语义；B1 是否会吸收所有 hidden state；L7 是否信息量过低。

Phase 5 — 前六篇人工验收准备
- 对 LAW、Epona、DriveLaW、World4Drive、WorldDrive、WoTE 生成逐轴验收表。
- 每格包含：类别、1句机制定义、语义 I/O、因果作用、关键证据、最近替代类、为何不属于替代类、置信度。
- 另外生成成对检查：LAW↔Epona、LAW/Epona↔DriveLaW、World4Drive↔WorldDrive↔WoTE。
- 不得用人工预期倒推分类；人工验收用于发现你的分类错误。

输出到新目录：outputs/core_mechanism_12_v1/。至少包含：
00_SCOPE_AND_ARTIFACTS.md
01_PAPER_MECHANISM_GRAPHS.md
02_ONTOLOGY_SPEC.md
03_TWELVE_PAPER_PROJECTIONS.md
04_COLLISION_AND_COUNTEREXAMPLE_AUDIT.md
05_V1_DRAFT_VERDICT.md
06_FIRST_SIX_HUMAN_VALIDATION.md
07_UNRESOLVED_EVIDENCE.md
08_EXECUTIVE_ROUTE_MAP.md

最后不要只给一张签名表。先给结论：这个 ontology 是否已达到“可用于领域理解”的稳定程度；若没有，明确阻塞在哪个机制边界。所有结论都要区分 PAPER FACT / CODE FACT / OUR INFERENCE / UNKNOWN。

完成后更新 GitHub，但不要覆盖 handoff/LATEST.md、state/CURRENT_STATE.md 或 state/NEXT_TASK.md；本任务保持独立。
```
