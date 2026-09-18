# P0046 World4Drive — Source-First Record

Status: `REVIEW-PASSED`

Primary source: `papers/raw_md/P0046_World4Drive/P0046_World4Drive.raw.md`

Pinned official-code audit: `audits/literature/PHASE_C5_WORLD4DRIVE_AUDIT.md`

Official repository commit recorded by the audit: `ucaszyp/World4Drive@cffb51adeb1f7d02b49c4b74d7262ded62a33ac8`

Historical route labels are intentionally absent.

## A. Author problem / gap ledger

| ID | Author-stated problem or gap | Evidence location | Status |
|---|---|---|---|
| W4D-P1 | 端到端规划需要从原始传感器中获得更有信息量的场景表示，但现有方法往往依赖昂贵的 3D 框、HD map 等感知标注。 | Abstract; Introduction | `AUTHOR CLAIM` |
| W4D-P2 | 现有单模态 latent 表示难以同时捕捉驾驶场景的空间、语义信息以及多模态驾驶意图。 | Introduction; Related Works | `AUTHOR CLAIM` |
| W4D-P3 | 仅从当前场景直接规划，不能充分表达不同驾驶意图下的多模态轨迹及其未来差异。 | Introduction; Sec. 3.1–3.3 | `AUTHOR CLAIM` |
| W4D-P4 | 作者希望利用 latent world model 预测不同驾驶意图对应的未来状态，并用 world model selector 评价和选择多模态轨迹。 | Abstract; Introduction; Sec. 3.3 | `AUTHOR CLAIM` |
| W4D-G1 | 作者提出的 gap 是：用空间—语义—时间增强的 current world latent，加上 intention-conditioned future latent prediction，支持无感知标注的多模态轨迹选择。 | Abstract; Introduction; Conclusion | `AUTHOR CLAIM` |

这些内容只记录作者如何定义问题，不判断其是否已经构成客观领域 gap。

## B. Neutral mechanism record

### B1. Current scene/world representation

World4Drive 的 current latent 不是只由一个普通图像 encoder 产生：

```text
multi-view image features
+ metric-depth spatial prior
+ open-vocabulary semantic prior
+ previous-frame temporal feature
→ current physical world latent L_t
```

其中，时间聚合通过当前视觉特征与上一时刻特征的 cross-attention 得到 `L_t`。这些 spatial/semantic priors 是 current representation 的组成部分；不能把所有规划提升都直接归因于 future predictor 或 selector。

证据：`PAPER FACT`，raw paper Sec. 3.2；foundation-prior 与 future-selector 的独立贡献边界见 pinned audit。

### B2. Intention and candidate generation

- 论文从 logged trajectory vocabulary 中得到 intention points；默认每个 driving command 有 `K=6` 个 intention modes。
- `Q_ego` 与 intention query 经过 self-attention，形成 multimodal planning query `Q_plan`。
- `Q_plan` 对 current world latent `L_t` 做 cross-attention，直接生成 `K` 条 ego trajectory candidates `T^1,...,T^K`。
- 每条候选再经 action encoder 得到对应 action token `A^k`。

关键顺序是：候选轨迹先产生，candidate-conditioned future latent 后产生。

```text
intention query + current L_t
        ↓
K trajectory candidates T^k
        ↓
K action tokens A^k
```

证据：`PAPER FACT`，raw paper Sec. 3.2.1 和 Sec. 3.3.1；`CODE FACT`，审计记录的 `num_mode=6`、`num_proposals=6` 及 K-means planning-mode reference。

### B3. Candidate-specific future latent

对每个候选，future query 读取共享的 current latent 和该候选 action token：

```text
(L_t, A^k)
      ↓
future-query cross-attention predictor
      ↓
L_{t+n}^k
```

默认设置是固定时间间隔 `n=3` 的 future latent。原文没有描述 WoTE 那种多步 recurrent BEV rollout；更准确的说法是“每个候选对应一个固定时刻的 future latent prediction”。

候选与 future 通过索引 `k` 保持对应关系。这里不暗示代码中存在独立的 candidate-ID 数据结构，而是指每个 action-conditioned branch 的输出与其输入候选一一对应。

证据：`PAPER FACT`，raw paper Eq. 6；`CODE FACT`，审计记录的 per-mode future features 与 stacked predictions。

### B4. World Model Selector / resolver

训练时，模型从真实未来帧提取一个 factual future latent `L_hat_{t+n}`，计算每个预测 latent 与它的距离：

```text
d_k = distance(L_{t+n}^k, L_hat_{t+n})
j = argmin_k d_k
```

索引 `j` 被用于：

1. 对最接近 factual future 的分支施加 latent reconstruction/alignment loss；
2. 将 `j` 作为 ScoreNet 的分类目标；
3. 对对应的 trajectory `T^j` 施加 expert trajectory supervision。

部署时不再拥有真实未来 latent，而是由 ScoreNet 对各候选预测 future latent 给出分数，并选择最高分对应的轨迹：

```text
K candidates
→ K candidate-conditioned future latents
→ ScoreNet
→ argmax score
→ final trajectory
```

因此，World4Drive 的未来 latent 确实位于部署时的候选选择路径上。

### B5. Training graph / deployment graph

**训练图**

```text
historical images + trajectory vocabulary
→ current L_t + K trajectory candidates
→ K predicted future latents
future frame
→ one factual future latent L_hat
predicted/factual latent matching
→ selected index j
→ reconstruction loss + ScoreNet focal loss + selected-trajectory loss
```

**部署图**

```text
current images + command/intention vocabulary
→ K trajectory candidates
→ K action-conditioned future latents
→ ScoreNet scores
→ choose highest-score trajectory
```

所以它不同于 LAW：future prediction 不只是训练期辅助；也不同于 Epona planning：future visual branch 不是可独立绕开的旁路；它与 WoTE 一样，future-related representation 在部署时参与候选选择。

### B6. Future supervision boundary

World4Drive 的关键监督不是：

```text
每个候选 T^k 都有一个由真实反事实驾驶产生的 future target
```

而是：

```text
K 个预测 future latents
vs
1 个实际发生的 factual future latent
```

因此可以确认：

- candidate-specific future output：`YES`；
- future latent 在线进入 selector：`YES`；
- 每个候选都有真实 alternative-action future supervision：`NO`；
- 已证明对每个自车干预都学到了真实周围交通响应：`NO / NOT ESTABLISHED`。

这不是说 K 个 latent 必然相同，而是说它们的训练目标主要是围绕一条 factual future 进行匹配和模式选择。

### B7. Official-code boundary

官方代码审计记录了以下核心事实：

- 官方仓库：`ucaszyp/World4Drive`；审计 commit：`cffb51adeb1f7d02b49c4b74d7262ded62a33ac8`。
- released W4D head 使用多个 planning modes，并存在 world-model branch、per-mode future feature、world-model classification head。
- 代码包含 reconstruction loss、world-model classification/focal loss，并将最佳 world-model index 与 ego trajectory supervision 连接起来。
- 当前审计明确闭合的是公开 W4D 实现的核心机制；论文报告的 NAVSIM 路径没有被单独重建，不能把论文和所有 benchmark/configuration 无条件视为完全相同。

### B8. 与 WoTE 的最小横向比较

两者可以共享同一个粗粒度部署骨架：

```text
candidate
→ candidate-corresponding future representation
→ learned score/reward
→ select
```

但 future 和 scorer 的语义不同：

| 项目 | World4Drive | WoTE |
|---|---|---|
| candidate future | 每候选一个固定时刻 latent | 每候选 recurrent multi-step BEV future |
| 主要部署模块 | World Model Selector / ScoreNet | Reward Model |
| 训练 future target | 一条 factual future latent | BEV simulator future states，并配合 simulation/imitation rewards |
| 选择信号 | 与 factual future latent 的模式匹配 proxy | imitation + safety/progress 等 reward 组合 |
| 共同点 | future representation 在线影响最终选择 | future representation 在线影响最终选择 |

当前更安全的结论是：二者属于同一个“候选后果评估”粗粒度方向，但不能把它们的 future semantics、监督方式和反事实含义混成相同机制。

## C. Evidence status

- `PAPER FACT`：World4Drive 原文明确给出多意图候选、candidate-conditioned future latent、world model selector，以及 inference-time highest-score selection。
- `CODE FACT`：已锁定官方仓库和 commit 的审计记录支持多 mode future features、selector head、reconstruction/classification losses 及最佳分支索引连接。
- `OUR INFERENCE`：World4Drive 与 WoTE 在部署因果骨架上同属候选后果评估，但 World4Drive 更接近 fixed-time future-latent matching，不应等同于 WoTE 的多步 BEV reward evaluation。
- `EVIDENCE BOUNDARY`：candidate-specific output 不等于 candidate-specific observed counterfactual truth；NAVSIM 报告也不自动证明反应式交通仿真。

## D. Unresolved

- 论文描述的 NAVSIM implementation 与公开代码核心路径之间的完整对应关系尚未逐配置重建。
- World4Drive 的 future latent 是否在所有场景中具有可解释的物理 consequence 语义，当前证据不足。
- foundation depth/semantic priors、intention vocabulary、future selector 三者对性能提升的独立因果贡献没有被完全隔离。
- K=6 intention modes 的覆盖能力与候选质量可能显著影响 selector 结果。
- ScoreNet 的最稳妥解释是 factual-future consistency / demonstrated-mode matching；不能直接升级为一般 safety utility 或真实反事实价值函数。

## E. Five-question pilot projection

Status: `READY-FOR-REVIEW`

This section projects the repaired five-question frame onto the already accepted source-first record. It does not add a route label, ontology axis, or matrix entry.

| Question | Provisional answer | Evidence status |
|---|---|---|
| Q1. Where does future-related computation occur? | In the candidate-conditioned future-query/world-model branch between each action token and the World Model Selector/ScoreNet. | `PAPER FACT` + `CODE FACT` |
| Q2. What is the future object, target, or intermediate representation? | A fixed-time candidate-specific future latent at t+n (default n=3); it is a latent representation, not established as a multi-step BEV rollout or a physical future state. | `PAPER FACT` + `CODE FACT` + `EVIDENCE BOUNDARY` |
| Q3. Does the future-related signal enter the action chain? | Yes. The candidate-specific future latents are scored by ScoreNet and the score changes the final argmax trajectory selection. | `PAPER FACT` + `CODE FACT` |
| Q4. What role does the future mechanism play? | Online candidate scoring/selection, trained mainly through matching candidate predictions to one factual future latent plus ScoreNet and trajectory supervision; not established as reactive counterfactual evaluation. | `PAPER FACT` + `CODE FACT` + `EVIDENCE BOUNDARY` |
| Q5. What remains at deployment? | Candidate generation, action tokens, the candidate-conditioned future-latent predictor, ScoreNet, and the resolver remain. The factual future target is a training signal and is not available at deployment. | `PAPER FACT` + `CODE FACT` |

Parallel provenance annotation: candidate-specific predicted future output is supported; one factual future latent supervises the alternatives; real alternative-action future ground truth and reactive traffic response are not established.

The five questions therefore distinguish World4Drive from training-only future supervision, while preserving the boundary that its selector is safest to describe as factual-future consistency/mode matching rather than a general counterfactual value function.
