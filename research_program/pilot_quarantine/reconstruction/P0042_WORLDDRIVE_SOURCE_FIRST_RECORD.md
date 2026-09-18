# P0042 WorldDrive — Source-First Record

Status: `READY-FOR-REVIEW`

Primary source: `papers/raw_md/P0042_WorldDrive/P0042_WorldDrive.raw.md`

Pinned official-code audit: `audits/literature/PHASE_C5_WORLDDRIVE_AUDIT.md`

Official repository and audited commit recorded by the audit: `TabGuigui/WorldDrive@c375ee1e1fe86ace175609db1ed90fd6db89673b`

Historical route labels are intentionally absent.

## A. Scope and artifact boundary

WorldDrive contains two related but operationally different artifacts:

1. **TA-DWM / TA-DiT scene-generation mode**: trajectory-conditioned future-latent/video generation. The paper also invokes this mode for qualitative future-scene visualization.
2. **Planning mode**: a frozen/inherited representation, a multimodal trajectory planner, and a Future-aware Rewarder (FAR) that selects among candidates.

The two modes must not be collapsed. The full TA-DiT future-generation path is a training teacher and an optional scene-generation path; the planning deployment path uses the distilled FAR representation rather than running full diffusion for every candidate.

## B. Author problem / gap ledger

| ID | Author-stated problem or gap | Evidence location | Status |
|---|---|---|---|
| WD-P1 | 将高保真未来场景生成接入规划会带来过高的计算成本和延迟。 | Introduction; Sec. 3.3 | `AUTHOR CLAIM` |
| WD-P2 | latent world model 虽然更高效，但作者认为它牺牲了可解释的场景模拟和显式视觉验证。 | Introduction | `AUTHOR CLAIM` |
| WD-P3 | 场景生成器侧重视觉/感知重建，规划器侧重动作回归，二者存在 representation misalignment 和 task disconnection。 | Abstract; Introduction | `AUTHOR CLAIM` |
| WD-P4 | 现有 world model 的 motion representation 没有被明确设计成可与 planner 共享、继承的表示，因而规划器不能充分利用 world model 学到的动态和 motion priors。 | Abstract; Introduction | `AUTHOR CLAIM` |
| WD-P5 | 需要在不运行每个候选的完整视频扩散生成的前提下，利用 future-aware 信息进行实时候选轨迹评价和选择。 | Introduction; Sec. 3.3 | `AUTHOR CLAIM` |

这些内容只记录作者如何定义问题和 gap，不判断这些问题是否已经构成客观领域共识，也不接受作者对效果的因果解释。

## C. Neutral mechanism record

### C1. Training-time TA-DWM

原文给出的主要训练链条是：

```text
historical frames
→ pretrained 3D causal VAE + visual adapter
→ historical visual latent f

trajectory vocabulary / anchor + residual
→ motion embedding c

(f, c, future-frame latent target)
→ TA-DiT
→ trajectory-conditioned future latent / future scene
```

TA-DWM 的 future target 来自实际视频的未来帧编码；trajectory condition 使生成 latent 与 motion intention 关联。这里的 `future scene` 可以进一步用于视频生成，但这不等于部署时规划器会对所有候选运行完整扩散。

证据：原文 Sec. 3.1、Appendix Sec. 6.1，`PAPER FACT`。

### C2. Candidate generation and first-stage planner

规划阶段继承 TA-DWM 的 visual encoder 和 trajectory encoder，并将预定义 trajectory anchors 作为 query，与历史 visual latent 和 ego status 交互。planner 对 anchor 预测 imitation/simulation scores 和 offset，选出 top-K refined trajectories，作为 FAR 的候选集。

```text
current visual representation + ego status + motion anchors
→ multimodal planner
→ candidate trajectories T^1, ..., T^K
```

候选集本身已经经过 planner 的第一阶段评分；FAR 是后续的 future-aware reranking/selection，不应把全部规划收益无条件归因给 TA-DWM。

证据：原文 Sec. 3.2、Appendix Sec. 6.2；官方代码审计中的 planner/anchor/offset 事实，分别为 `PAPER FACT` 与 `CODE FACT`。

### C3. FAR training graph

对候选 `k`，训练期有两条分支：

```text
candidate T^k / motion embedding c^k + current visual latent f
        ├─ frozen TA-DWM / TA-DiT
        │    → teacher future latent z^k
        └─ lightweight FAR future-scene decoder
             → predicted future surrogate z_hat^k

z_hat^k ↔ z^k
→ future-latent alignment/distillation

candidate preference pairs
→ Bradley–Terry ranking loss
```

原文的 preference-pair 构造是：先由 planner 生成 top-16 candidates，取 planner score 最高的 top-1，选 simulation score 最低的 hard negatives，再从剩余候选中随机采样；FAR 以 Bradley–Terry loss 学习偏好。

所以 FAR 不是只有一个监督来源：

```text
frozen TA-DWM → future representation distillation
planner/simulation preference setup → candidate ranking
```

证据：原文 Figure 3、Sec. 3.3、Appendix Sec. 6.3；官方代码审计，`PAPER FACT + CODE FACT`。

### C4. Deployment graph

部署时的候选选择链条是：

```text
observation
→ current visual representation
→ planner candidate set
→ FAR: current representation + candidate embedding
→ candidate-conditioned future-scene surrogate
→ scalar future-aware reward
→ argmax
→ selected trajectory
```

官方代码审计确认，FAR/refiner 在推理路径中直接预测 future-scene embedding；该路径没有调用完整 TA-DiT diffusion denoising。TA-DWM 的完整 future generation 可以被单独调用来生成/可视化未来场景，但不属于 FAR 的在线候选选择链条。

证据：原文 Sec. 3.3、Appendix Sec. 6.3/8；`worlddrive_refiner.py::TrajWorldRefiner.forward` 和 `worlddrive_agent.py::forward_wm` 的 pinned audit，`PAPER FACT + CODE FACT`。

### C5. Candidate correspondence and resolver

- `T^k`、`c^k`、`z^k`/`z_hat^k` 和 reward `r_k` 按候选索引 `k` 保持对应关系。
- 这里的“对应”表示同一候选分支的输入与输出一一关联，不暗示代码中存在独立的 candidate-ID 数据结构。
- FAR 的终端 resolver 是对候选 reward 做 `argmax`，输出最高 reward 对应的轨迹。
- planner 的第一阶段 top-K 选择与 FAR 的最终选择是两个连续决策，不能合并为一个无中间阶段的单一 scorer。

证据：原文 Sec. 3.2–3.3、Appendix Sec. 6.3；官方代码审计，`PAPER FACT + CODE FACT`。

## D. Training/deployment separation

| 阶段 | 使用的 future 相关对象 | TA-DiT / teacher path 状态 | 作用 |
|---|---|---:|---|
| TA-DWM 训练 | 实际未来帧编码的 future latent target | 使用扩散训练任务 | 学习 trajectory-aware visual/motion representation |
| FAR 训练 | 冻结 TA-DWM 对候选生成的 teacher future latent | 使用 teacher path | 对齐 FAR 的 candidate-conditioned future surrogate |
| 规划部署 | FAR 直接预测的 candidate-conditioned future surrogate | 不调用完整 TA-DiT path | 为候选计算 future-aware reward 并选择 |
| 单独场景生成/可视化 | TA-DWM/TA-DiT 生成的 future scene/video | 可选调用 | 展示或分析 motion-conditioned scene generation，不是 FAR resolver |

这张表只描述生命周期，不把“future latent 在训练期由 teacher 产生”和“future surrogate 在部署期被 planner 使用”混成同一个执行路径。

## E. Future supervision boundary

可以确认：

- candidate-specific future output：`YES`；每个候选有对应的 teacher/surrogate future representation。
- future-related representation online enters candidate selection：`YES`；部署 FAR 用 surrogate 计算 reward 并 `argmax`。
- full generative world-model rollout online for every candidate：`NO`；部署使用 distillation 后的轻量 FAR。
- each candidate has a real observed alternative-action future target：`NO`。
- reactive, behaviorally correct counterfactual traffic response：`NOT ESTABLISHED`。

关键边界是：TA-DWM 为未执行候选生成的 `z^k` 是模型 teacher output；FAR 的 reward 还受到 planner/simulation preference supervision 影响。它不是“每个自车干预都有一条真实记录 future”的监督，也不能仅凭 candidate-conditioned video 生成宣称已验证真实反事实交通后果。

官方评测包含 NAVSIM/NAVSIM-v2 和 nuScenes；已有审计特别保留 benchmark、代码配置和反应式交通语义之间的边界，不能把这些结果自动升级为真实闭环反事实验证。

## F. Minimal cross-paper comparison

WorldDrive、WoTE 和 World4Drive 可以共享一个粗粒度部署骨架：

```text
candidate
→ candidate-corresponding future representation
→ score / reward
→ select
```

但它们的 future 语义和生命周期不同：

| 项目 | WorldDrive | WoTE | World4Drive |
|---|---|---|---|
| 部署时 future 对象 | FAR 直接预测的 distilled future surrogate | candidate-conditioned recurrent BEV future | candidate-conditioned fixed-time future latent |
| 完整 world model 的位置 | TA-DWM 主要作为训练 teacher；完整生成可单独调用 | online future evaluator/world-model path | future latent predictor 与 ScoreNet 在部署链中 |
| 选择信号 | FAR future-aware reward + preference ranking | imitation/safety/progress 等 reward | ScoreNet 对 future latent 的评分/匹配 |
| 关键监督边界 | teacher latent + planner/simulation preference，不是真实 alternative future | logged/benchmark future 与 reward 监督，不等于反应式交通反事实 | 多候选预测对一条 factual future latent 的匹配，不是 K 条真实反事实 future |

因此当前最小结论是：WorldDrive 与 WoTE、World4Drive 共享“候选 future 相关表示进入选择”的粗粒度方向；WorldDrive 的特殊点是把重型 candidate-conditioned future generation 从部署期卸载到训练期 teacher，再把其 planning-relevant representation 蒸馏给在线 FAR。这是生命周期/实现差异，不应单独升级为新路线或 ontology。

## G. Evidence status

- `PAPER FACT`：原文明确给出 TA-DWM、representation inheritance、top-K candidate、FAR distillation，以及推理时最高 reward 选择。
- `CODE FACT`：Pinned audit 在 `TabGuigui/WorldDrive@c375ee1e1fe86ace175609db1ed90fd6db89673b` 上确认 planner/FAR 的 candidate-conditioned future surrogate、teacher path 和 `argmax` selection；确认 FAR 推理不调用完整 TA-DiT diffusion。
- `AUTHOR CLAIM`：统一 vision/motion representation 会弥合 scene generation 与 planning 的 representation schism，并提升规划与生成能力。
- `OUR INFERENCE`：WorldDrive 与 WoTE、World4Drive 可在部署因果骨架上横向比较，但应把“teacher future”“deployed surrogate”“future supervision”作为语义修饰，而不是另建路线分类。
- `EVIDENCE BOUNDARY`：candidate-specific generated future 不等于 candidate-specific observed counterfactual truth；FAR 同时受 future-latent distillation 与 preference/ranking supervision 影响。

## H. Unresolved / evidence debt

- 论文描述的全部 benchmark/configuration 是否与公开代码的 FAR path 逐配置完全一致，当前没有逐配置重建。
- FAR 的性能增益中，TA-DWM future dynamics、通用 CogVideoX visual prior、planner/simulation preference supervision 各自的独立贡献没有完全隔离。
- candidate-conditioned TA-DWM future latent 对未执行自车动作及周围交通行为的物理/行为正确性，当前没有真实多干预 ground truth 证明。
- 部署 FAR 输出更准确的名称应是“candidate-conditioned future-scene representation/surrogate”，不能无条件称为真实 future state 或完整 world rollout。
- 论文中的 scene-generation mode 与 planning deployment mode 已被分开记录；若未来发现代码存在额外部署分支，需要新增 artifact boundary，而不是覆盖当前结论。

## I. Five-question pilot projection

Status: `READY-FOR-REVIEW`

| Question | Provisional answer | Evidence status |
|---|---|---|
| Q1. Where does future-related computation occur? | The heavy TA-DWM/TA-DiT branch constructs candidate-conditioned teacher futures during training; the deployed FAR branch predicts a lightweight candidate-conditioned future-scene surrogate between planner candidates and the final reward resolver. | `PAPER FACT` + `CODE FACT` |
| Q2. What is the future object, target, or intermediate representation? | Training uses trajectory-conditioned future latent/scene representations from actual future-frame targets and the frozen TA-DWM teacher; deployment uses FAR-predicted future-scene surrogates. These are not established as observed alternative-action futures. | `PAPER FACT` + `CODE FACT` + `EVIDENCE BOUNDARY` |
| Q3. Does the future-related signal enter the forward action chain? | Yes. The deployed FAR surrogate is consumed by the future-aware rewarder and changes the candidate argmax selection. The full TA-DiT teacher is not run for every candidate at deployment. | `PAPER FACT` + `CODE FACT` |
| Q4. What role does the future mechanism play? | Training-time representation inheritance and heavy-teacher distillation, followed by online candidate-specific future-surrogate scoring/selection. Scene-generation mode remains a separate optional artifact. | `PAPER FACT` + `CODE FACT` |
| Q5. What remains at deployment? | The inherited planner representation, candidate generator, lightweight FAR surrogate, future-aware reward, and resolver remain; full TA-DiT diffusion teacher computation is removed from the canonical planning path. | `CODE FACT` |

Parallel provenance annotation: candidate-specific surrogate futures and online selection are supported; each candidate's real alternative-action future and reactive traffic response are not established.
