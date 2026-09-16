# WAM 核心机制双层签名 V1：十二篇历史压力测试（待证伪）

> 状态：HISTORICAL SHADOW PROJECTION — 非正式分类结论；下一轮以 `handoff/core_mechanism_12/` 为任务入口，从原始机制图重新判断
> 基础规范：[WAM_CORE_MECHANISM_SIGNATURE_V1_PROPOSAL.md](WAM_CORE_MECHANISM_SIGNATURE_V1_PROPOSAL.md)
> 测试对象：正式六篇 + SeerDrive / Drive-JEPA / Metis / DynFlowDrive / Discrete-WAM / GraphWorld

---

## 1. 压力测试目的

后续六篇不用于扩大论文清单，而用于攻击签名结构：

```text
它们是否迫使我们把训练机制和部署机制重新混在一起？
它们是否暴露A/B/C/D的漏项或层级冲突？
它们能否在不引入论文专属类别的前提下表达核心机制？
```

本文件中的签名均为 shadow projection：

- 可以证明某个轴能否承载该机制；
- 不等于完成这些论文的最终正式归类；
- 论文/源码不一致时必须拆开；
- SOURCE-UNVERIFIED 的实现细节不得补全。

---

## 2. 基线：六篇正式签名

| Artifact / mode | Runtime | Learning | 核心机制 |
|---|---|---|---|
| LAW planning | `A1+B0+C0+D0` | `L{L2a}` | predicted action进入辅助future预测，world loss塑造直接策略 |
| Epona `traj_only` planning | `A1+B0+C0+D0` | `L{L2b}` | world/action sibling heads通过shared state共同训练 |
| DriveLaW planning | `A1+B2+C1+D0` | `L{L1,L7}` | 在线future-generation carrier单向进入直接策略 |
| World4Drive paper mechanism | `A3+B3+C2+D1` | `L{L7}` | candidate endpoint future用于事实模式选择 |
| WorldDrive planning | `A3+B3+C2+D2a` | `L{L4,L5}` | heavy consequence teacher蒸馏 + preference ranking |
| WoTE planning | `A3+B4+C2+D2b` | `L{L7}` | candidate temporal rollout + decomposed planning reward |

这六篇覆盖：

```text
A1 / A3
B0 / B2 / B3 / B4
C0 / C1 / C2
D0 / D1 / D2a / D2b
L1 / L2a / L2b / L4 / L5 / L7
```

后续压力测试重点攻击尚未充分覆盖的 A2、B1、C3、D3、L3、L6，以及多版本分类规则。

---

## 3. SeerDrive：C3与版本单位测试

### 3.1 论文机制

论文图：

```text
current BEV + candidate/mode ego features
→ mode-specific future BEV
→ future-aware planner refinement
→ refined ego feature反馈给world model
→ 更新future BEV
→ 重复内部互馈
→ mode score选择最终trajectory
```

shadow signature：

```text
Runtime  = A3 + B3 + C3 + D1
Learning = L{L7}
```

判定：

- A3：多模态trajectory identity持续到classification selection；
- B3：每个mode对应终点式future BEV，默认不需要多步物理时间展开；
- C3：future BEV影响planner，refined ego feature再反馈给world model；
- D1：winner-takes-all的事实/示范mode supervision，不是显式规划效用；
- L7：runtime world/planner模块端到端、逐迭代监督。

压力测试结论：C3能够表达“同一决策内迭代互馈”，无需把 iteration count、Transformer depth 或 physical rollout另建主轴。

### 3.2 公开代码版本

官方README明确说明公开版本整合了 WoTE在线轨迹评价，并且**不包含论文所述 planning/scene iterative interaction**。源码包含trajectory anchors、latent world model、RewardConvNet与多个sim reward heads。

因此只能给出边界化 shadow：

```text
Runtime  = A3 + B? + C2 + D2b
Learning = L{L7}

B? = B3或B4，等待对released-code world rollout时间结构的独立闭合
```

不得把论文的 `C3` 与公开代码的 `C2` 合并。

证据：[SeerDrive审计](../audits/literature/PHASE_C5_SEERDRIVE_AUDIT.md)、[原文](raw_md/P0061_SeerDrive/P0061_SeerDrive.raw.md)

---

## 4. Drive-JEPA：同一论文多规划模式测试

### 4.1 Perception-free部署路径

```text
two front images
→ transferred/frozen JEPA encoder
→ trajectory head
```

shadow signature：

```text
Runtime  = A1 + B0 + C0 + D0
Learning = L{L1}
```

JEPA predictor、EMA target encoder、masked prediction和future object均不进入规划推理。

### 4.2 Perception-based候选路径

```text
context
→ proposal set + iterative planner-side refinement
→ PDM-like utility score
→ optional momentum/comfort recalibration
→ argmax
```

shadow signature：

```text
Runtime  = A3 + B0 + C0 + D2b
Learning = L{L1, L5}
```

判定：

- planner-side proposal refinement不是world carrier；
- pseudo teachers和score targets来自simulator/rule criterion，属于 L5；
- 最终score是分解式规划质量而不是future reconstruction；
- NAVSIM-v2 momentum calibration作为 D2b 的决策属性记录，不另建主轴。

压力测试结论：同一论文必须按 task mode分开签名；“使用JEPA”不能把两条Runtime强行写成一类。

证据：[Drive-JEPA审计](../audits/literature/PHASE_C5_DRIVEJEPA_AUDIT.md)、[原文](raw_md/P0049_DriveJEPA/P0049_DriveJEPA.raw.md)

---

## 5. Metis：训练图核心、部署图简单测试

训练机制：

```text
action expert → predicted/noisy future action representation
future action → condition video-generation expert
video flow loss → backpropagate into action expert
```

部署机制：

```text
current context → action expert → action chunk
future-video branch bypassed
```

shadow signature：

```text
Runtime  = A1 + B0 + C0 + D0
Learning = L{L2a}
```

Metis与 LAW在功能级学习边上可以同属 L2a：模型自己的action进入world branch，world loss训练policy。二者使用video还是latent、flow还是其他loss属于实现/属性差异。

压力测试结论：双层签名能够表达“Runtime完全相同，但论文核心位于Learning”的情形；无需为Metis建立部署期world类别。

边界：公开仓库尚无训练/推理源码，attention和gradient routing为paper-verified、source-unverified。

证据：[Metis审计](../audits/literature/PHASE_C5_METIS_AUDIT.md)、[原文](raw_md/P0062_Metis/P0062_Metis.raw.md)

---

## 6. DynFlowDrive：world-derived selector teacher测试

训练机制：

```text
candidate trajectory
→ training-only flow world model
→ reconstruction + flow stability + trajectory criterion
→ winner label / score supervision
```

部署机制：

```text
observation → candidate trajectories + learned scores → argmax
world model OFF
```

shadow signature：

```text
Runtime  = A3 + B0 + C0 + D3
Learning = L{L5}
```

判定：

- world model删除，因此必须 B0+C0；
- runtime score head仍在预测由world reconstruction/stability参与构造的criterion，因此 D3；
- world criterion被压缩成selector target，因此 L5；
- flow solver coordinate不是physical future time，不影响 B0。

压力测试结论：D必须编码 resolver语义，而 B/C只编码在线对象与因果边；否则 DynFlowDrive会被错误归入在线candidate consequence。

边界：官方实现未发布，方程与采样初值仍有paper-level ambiguity。

证据：[DynFlowDrive审计](../audits/literature/PHASE_C5_DYNFLOWDRIVE_AUDIT.md)、[原文](raw_md/P0063_DynFlowDrive/P0063_DynFlowDrive.raw.md)

---

## 7. Discrete-WAM：A2与L3测试

训练能力：

```text
separate visual/action vocabularies
→ shared Transformer hidden space/backbone
→ world / policy / joint world-policy tasks
```

主要规划部署：

```text
current context
→ high-level decision token
→ iterative action-token editing
→ trajectory
```

shadow signature：

```text
Runtime  = A2 + B0 + C0 + D0
Learning = L{L3}
```

判定：

- decision token具有path×speed语义并条件化action generation，因此 A2；
- primary planning graph不要求future visual token generation，因此 B0+C0；
- action-token editing rounds是policy refinement compute，不是candidate resolver或physical rollout；
- world/action共享序列接口、主干和多任务梯度，因此 L3。

压力测试结论：A2捕获语义层级，而不按continuous/discrete、diffusion/token editing拆类；L3捕获统一world-policy学习但不虚构在线world imagination。

边界：未识别官方实现仓库，代码级token routing与planning forward保持source-unverified。

证据：[Discrete-WAM审计](../audits/literature/PHASE_C5_DISCRETE_WAM_AUDIT.md)、[原文](raw_md/P0064_Discrete-WAM/P0064_Discrete-WAM.raw.md)

---

## 8. GraphWorld：B1而非future rollout测试

论文部署图：

```text
current/history observation + interaction graph + map
→ current ego-centric latent world state
→ flow-based world-state refinement
→ reweight agent motion modes + modulate ego planning queries
→ multimodal trajectory probabilities and trajectories
```

shadow signature：

```text
Runtime  = A3 + B1 + C1 + D1
Learning = L{L6, L7}
```

判定：

- multi-modal ego trajectories具有概率并进入最终mode selection，因此shadow为 A3；
- online world object是interaction/history/current planning state，不是每个ego candidate的future environment，因此 B1；
- world state单向调制motion/planning queries，没有candidate→future consequence回路，因此 C1；
- final mode probability属于示范/模式兼容性语义，暂记 D1；
- Stage-II `W_t`对stop-gradient `W_{t+1}`的一致性属于 L6；
- world-state与planning模块仍在Runtime并联合训练，记 L7。

压力测试结论：B1阻止所有“world state”都被叫作future consequence；A3与 B3/B4没有强绑定，候选系统可以只读取共享当前world state。

边界：`W_tgt`由motion/planning hypotheses和map构造，不是直接编码事实future observation；官方实现未找到，D1与精确selector routing保持paper-level shadow。

证据：[GraphWorld审计](../audits/literature/PHASE_C5_GRAPHWORLD_AUDIT.md)、[原文](raw_md/P0065_GraphWorld/P0065_GraphWorld.raw.md)

---

## 9. 逐轴压力测试结论

| 轴/规则 | 攻击论文 | 结果 | 原因 |
|---|---|---|---|
| A1直接策略 | Metis | PASS | action-only部署不因训练期video branch升级 |
| A2层级策略 | Discrete-WAM | PASS | semantic decision→action与普通hidden layer可区分 |
| A3候选选择 | Drive-JEPA / GraphWorld | PASS | 候选身份与共同resolver是稳定判据 |
| B0无在线carrier | Drive-JEPA / Metis / DynFlow / Discrete-WAM | PASS | 训练期world能力不会污染部署分类 |
| B1当前world state | GraphWorld | PASS | current relational state与future consequence分离 |
| B3候选endpoint | SeerDrive paper | PASS | mode-specific endpoint future无需误写成rollout |
| C3迭代互馈 | SeerDrive paper | PASS | 与network iteration、physical rollout分开 |
| D2规划效用 | Drive-JEPA | PASS | utility selection不要求在线future object |
| D3 dynamics consistency | DynFlowDrive | PASS | runtime scorer语义与online carrier正交 |
| L2a action-conditioned auxiliary learning | Metis | PASS | 与LAW形成可复用功能等价类 |
| L3共享world-policy学习 | Discrete-WAM | PASS | 共享主干不等于部署联合生成 |
| L5world/simulator→decision target | Drive-JEPA / DynFlow | PASS | 离线知识压缩进runtime selector可统一表达 |
| L6next-state consistency | GraphWorld | PASS | factual t+1监督不被误写成action-conditioned transition |
| 版本/模式单位 | SeerDrive / Drive-JEPA | PASS | 同一标题允许多个签名 |

---

## 10. 未升级为主轴的 residue

压力测试中出现但暂不应升级为核心主轴的差异：

```text
flow interpolation time vs physical time
denoising/editing rounds vs planning refinement rounds
endpoint future vs多时间点训练辅助监督
momentum/comfort score calibration
single shared codebook vs separate vocabularies映射到shared hidden space
per-iteration deep supervision
ego-star graph vs fully connected graph
future target来自事实、teacher、simulator或规划hypothesis
```

它们分别进入 temporal、representation、training 或 evidence 属性。只有未来论文证明某项差异改变语义接口或核心因果图，才启动扩展规则。

---

## 11. 验收结果

### 重建测试

通过。十二篇的核心部署图和学习知识流都能由 Runtime + Learning恢复，不需要阅读论文专属模块名。

### 碰撞测试

通过。关键碰撞被双层等价关系正确处理：

```text
LAW vs Epona
Runtime相同，Learning不同

LAW vs Metis
Runtime与功能级L2a相同
具体表示、专家结构和loss parameterization属于属性差异

World4Drive vs WorldDrive vs WoTE
A3/C2共享
B与D明确分离其核心机制
```

### 不变性测试

通过。flow、diffusion、token editing、BEV和latent不会仅凭实现名称改变类别。

### 生命周期测试

通过。Drive-JEPA、Metis、DynFlowDrive、Discrete-WAM均可具有丰富world learning但保持 B0+C0。

### 版本测试

通过。SeerDrive论文机制与公开实现、Drive-JEPA两种部署路径能够分别记录。

### 当前总判定

```text
V1主轴在十二篇压力测试下无需新增维度。

但V1仍为PROPOSAL：
后续正式收录六篇shadow论文时，必须逐篇锁定版本、task mode和源码边界，
不得直接复制本文件中的shadow签名为最终结论。
```
