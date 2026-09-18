# P0045 WoTE — Source-First Record

Status: `SOURCE-FIRST-DRAFT`

Primary source: `papers/raw_md/P0045_WoTE/P0045_WoTE.raw.md`

Pinned source audit: `audits/literature/PHASE_B_WAVE2_INTERFACE_CODE_AUDIT.md`

Audited repository commit: `liyingyanUCAS/WoTE@298957c128a91d41a1c6075bd0bb6e7e845e093f`

Historical route labels are intentionally absent.

## A. Author problem / gap ledger

| ID | Author-stated problem or gap | Evidence location | Status |
|---|---|---|---|
| WOTE-P1 | 端到端驾驶方法通常重点是预测一条高质量轨迹；当驾驶本身具有多模态性时，同时产生多条候选轨迹并可靠评估它们更重要。 | Abstract; Introduction | `AUTHOR CLAIM` |
| WOTE-P2 | 传统轨迹评估依赖感知结果和规则，容易受感知误差影响，也不容易直接进行端到端优化。 | Introduction; Related Works | `AUTHOR CLAIM` |
| WOTE-P3 | 只根据当前状态评价候选轨迹，没有利用“这条候选轨迹会带来的未来”信息。 | Introduction | `AUTHOR CLAIM` |
| WOTE-P4 | 图像级未来世界模型使用扩散生成，作者认为速度和计算量不适合实时轨迹评估。 | Introduction | `AUTHOR CLAIM` |
| WOTE-P5 | 真实驾驶日志通常只有一条未来轨迹/未来状态，但多候选评估需要为多条候选想象多个未来，未来状态监督不足。 | Introduction; Sec. 3.4 | `AUTHOR CLAIM` |
| WOTE-G1 | 作者提出的缺口是：把候选轨迹输入 BEV world model，预测各候选对应的未来 BEV 状态，再用 reward model 评价并选择轨迹。 | Abstract; Introduction; Sec. 3 | `AUTHOR CLAIM` |

这些条目只记录 WoTE 作者如何定义问题；本记录不判断这些批评是否客观成立，也不把它们直接升级为领域共识。

## B. Neutral mechanism record

### B1. 输入与候选轨迹

- 当前多模态观测（相机和 LiDAR）经过 BEV encoder，得到当前 BEV state `B_t`。
- 轨迹预测器先产生多条轨迹候选；论文使用 KMeans trajectory anchors，再根据当前 BEV state 对候选进行 refinement。
- 每条 refined trajectory 与后续 future 分支保持对应索引 `i`，形成 state-action pair `(B_t, a_t^i)`；这不暗示代码中存在独立的 candidate-ID 数据结构。

证据：`PAPER FACT`，raw paper Sec. 3.1；候选数量和配置见 Sec. 4.2。

### B2. 候选特定的未来展开

对每个候选 `i`，BEV world model 接收 `(B_t, a_t^i)`，递归地产生该候选对应的未来 BEV states 和 future actions：

```text
(B_t, a_t^i)
      ↓
recurrent BEV world model
      ↓
B_{t+1}^i, ..., B_{t+K}^i
```

论文明确描述这些 state-action pairs 是并行处理的；未来状态在 BEV 空间而非完整 RGB 图像空间中预测。代码审计也确认 learned model 是 action-conditioned，并不据此断言所有候选的未来都相同。

证据：`PAPER FACT` + `CODE FACT`。

### B3. Future 如何进入最终动作

Reward Model 对每个候选分别汇总当前 BEV state、该候选的未来 BEV states 和对应 actions，预测：

- imitation reward；
- simulation rewards，包括碰撞、可行驶区域、TTC、舒适性和 ego progress 等指标。

这些 reward 按论文设定组合成 final reward。最终选择 final reward 最高的 refined trajectory：

```text
多个 trajectory candidates
        ↓
每个候选自己的 BEV future
        ↓
每个候选自己的 reward
        ↓
argmax / highest-reward selection
        ↓
最终轨迹
```

这条链在 WoTE 中是论文明确声称的部署机制；未来 BEV 不是只用于训练辅助，也不是仅供独立视觉生成，而是进入候选评价并影响最终选择。

证据：`PAPER FACT`，raw paper Sec. 3.2–3.3；`CODE FACT`，pinned audit 的 inference/target-generation interpretation。

### B4. 训练图与部署图分开记录

**训练图**

- BEV future state target 和 simulation reward target 由 BEV-space traffic simulator 产生。
- imitation reward 仍通过与一条 expert trajectory 的距离构造监督；trajectory predictor 也使用 winner-take-all 等与专家轨迹相关的训练信号。
- NAVSIM 配置中，论文提到会预计算基于 anchors 的 simulation results 以加快训练；测试时再评价 refined trajectories。

**部署图**

- 输入当前观测，产生多条 refined candidates。
- 对每个 candidate 进行 candidate-conditioned BEV future prediction。
- Reward Model 读取这些 candidate-specific futures，计算 reward。
- 选择最高 reward 的 candidate。

因此，WoTE 是当前试点中第一个被证据确认的“future 在线参与候选选择”的正对照；不能把它退化成普通的多轨迹直接生成器。

### B5. Surrounding agents 的反应性边界

这里必须区分论文中的世界模型机制和官方代码中的监督/目标生成语义。

官方代码审计锁定的 NAVSIM/PDM target-generation path 显示：

```text
candidate-specific ego trajectory       = YES
candidate-specific simulated ego state  = YES
candidate-dependent other-agent future  = NO in this cached target path
other-agent future source               = interpolated logged/GT tracks
```

也就是说，每个候选的自车轨迹和自车模拟状态会变化，但审计到的 cached environment 中，周围车辆未来来自同一条记录/GT 场景未来，并不是每个自车干预都触发一次新的反应式交通重规划。

这不等于 learned BEV world model 必然对所有候选输出相同未来；它只说明当前已审计的监督路径没有为每个自车干预提供一份匹配的、反应式的周围车辆未来 oracle。

证据：`CODE FACT`，`PHASE_B_WAVE2_INTERFACE_CODE_AUDIT.md` 的 WoTE supervision-reactivity audit。

### B6. Candidate、future、resolver 状态

| 项目 | 当前证据 |
|---|---|
| 明确的多候选轨迹 | `YES` |
| 候选与 future 的索引/对应关系保持可追踪 | `YES`，以 `(B_t, a_t^i)` 和 `B_{t+k}^i` 表示 |
| 每候选独立 future representation | `YES`，论文机制与代码审计一致支持 candidate-conditioned BEV prediction |
| future 在线进入候选评价 | `YES` |
| 明确 reward/scorer | `YES`，Reward Model |
| 最终 resolver | `YES`，选择最高 final reward |
| 反应式周围车辆 counterfactual | `NO in the audited NAVSIM/PDM target path` |
| 完整 RGB future 是否必需 | `NO`，未来主要在 BEV 表示中预测 |

### B7. 证据状态与不可越界结论

- 可以确认：WoTE 的规划机制是“候选轨迹 → 候选特定 BEV future → reward → 选择”。`PAPER FACT` / `CODE FACT`。
- 可以确认：future 在部署时参与 candidate evaluation，而不是只在训练时提供辅助 loss。`PAPER FACT`。
- 可以确认：官方代码审计到的 NAVSIM/PDM 目标生成使用固定 logged/GT surrounding-agent future。`CODE FACT`。
- 因此可以把它作为“候选后果评估”的正对照，但不能进一步写成“已经证明了行为正确的反事实交通仿真”。`OUR INFERENCE`。
- 论文报告的性能提升说明该模块有实验收益，不单独证明 learned future 对每个指标的因果贡献。`EVIDENCE BOUNDARY`。

## C. 与前三篇试点的最小差异

| 论文 | future/world-related computation 在规划系统中的位置 | 是否在线逐候选评价并选择 |
|---|---|---|
| LAW | 未来 latent 主要作为训练期辅助目标；审计路径中不回读 future 重新选轨迹。 | 当前未确认 |
| Epona | 共享历史 latent 支撑轨迹分支；视觉 future 可在独立运行模式中 rollout，规划模式可跳过。 | 当前未确认 |
| DriveLaW | Video-DiT 内部 hidden state 在线条件化 Action-DiT；直接生成轨迹。 | 当前未确认 |
| WoTE | 每条候选进入自己的 BEV future，再进入 Reward Model 和最高 reward 选择。 | 已确认，但带 NAVSIM 非反应式监督边界 |

这张表只用于本次人工审查，不是路线命名，也不是全量分类矩阵。

## D. Unresolved

- 论文描述的所有 simulator supervision 与官方公开代码各配置之间是否完全一致，当前没有逐配置重建。
- 当前审计结论主要针对 NAVSIM/PDM target-generation path；不能无条件外推到论文所有 benchmark/configuration。
- WoTE 的 BEV world model 预测是否在每个部署配置中都由同一套 reward/resolver 使用，需要继续保留配置边界。
- raw Markdown 的个别实验叙述存在数值/排版不一致；这不影响当前机制判定，但不应在本记录中自行修正。
- learned candidate-specific future 是否学到了真实交通参与者对自车干预的反应，当前证据不足。

## E. Five-question pilot projection

Status: `READY-FOR-REVIEW`

This section projects the repaired five-question frame onto the already accepted source-first record. It does not add a route label, ontology axis, or matrix entry.

| Question | Provisional answer | Evidence status |
|---|---|---|
| Q1. Where does future-related computation occur? | In a candidate-conditioned recurrent BEV world-model rollout between the refined candidate action and the Reward Model. | `PAPER FACT` + `CODE FACT` |
| Q2. What is the future object, target, or intermediate representation? | Multi-step candidate-specific future BEV states paired with the candidate actions; not RGB video. | `PAPER FACT` + `CODE FACT` |
| Q3. Does the future-related signal enter the action chain? | Yes. Each candidate's predicted BEV future is consumed by the Reward Model and changes the final highest-reward selection. | `PAPER FACT` + `CODE FACT` |
| Q4. What role does the future mechanism play? | Online candidate-consequence evaluation and selection; training also uses simulator-derived future/reward supervision and imitation-related signals. | `PAPER FACT` + `CODE FACT` |
| Q5. What remains at deployment? | Candidate generation/refinement, recurrent BEV rollout, Reward Model, and the highest-reward resolver remain. In the audited NAVSIM/PDM target path, surrounding-agent future targets remain shared logged/GT tracks rather than reactive per-ego-intervention futures. | `CODE FACT` + `EVIDENCE BOUNDARY` |

Parallel provenance annotation: candidate-specific ego future prediction is supported; reactive counterfactual future supervision for surrounding agents is not established in the audited target path.

The five questions therefore identify WoTE as an online candidate-evaluation mechanism without treating its BEV rollout as proof of a fully reactive counterfactual traffic simulator.
