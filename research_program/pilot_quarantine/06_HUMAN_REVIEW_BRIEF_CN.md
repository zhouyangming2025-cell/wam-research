# LAW / Epona / DriveLaW：中文人工审查简报

状态：前三篇 source-first 机制审查：`人工确认通过`；五问投影与测试：`READY-FOR-REVIEW`

你不需要阅读仓库中的英文文件。只需要审查本页的中文概括是否准确、边界是否夸大，以及三篇论文是否确实存在下面的机制差异。

本页不是最终路线结论，也不要求你判断作者提出的问题是否真的成立。

## 0. 三篇论文的五问测试实际结果（审查入口）

状态：`READY-FOR-REVIEW`。五问已经完成对 LAW、Epona、DriveLaW 的第一轮投影、区分性检查、轴碰撞检查和最小删除测试；这不是最终人工通过，也没有扩展到 12 篇论文。

五问是对现有 source-first 事实的统一审查投影，不是新 ontology、路线 taxonomy 或矩阵。完整的逐问证据表和删除测试见第 6 节。

| 论文 | 五问实际答案摘要 | 暂定判定 |
|---|---|---|
| LAW | Q1：训练期 action-conditioned future-latent prediction 分支；Q2：未来 visual latent；Q3：不进入部署动作链；Q4：训练期表示塑造/辅助预测；Q5：部署保留直接 waypoint/trajectory path，future 输出不被消费 | 训练期 future supervision；未发现在线候选后果评估 |
| Epona | Q1：共享历史时空表示、TrajDiT 与 VisDiT 的相应计算分支；Q2：未来 ego trajectory 与下一帧 visual latent/frame；Q3：没有证据表明 visual future 反馈到轨迹生成或选择；Q4：联合训练、单路径轨迹生成和视觉 rollout；Q5：按模式决定是否保留 VisDiT | 多模式联合系统；不能简化成“未来视频给 planner 打分” |
| DriveLaW | Q1：Video-DiT 去噪过程及其 video-to-action hidden-state 接口；Q2：视频生成过程的中间 hidden representation，不是已被证明的显式 future state/target；Q3：该 hidden signal 前向进入 Action-DiT，但未发现 candidate-specific feedback；Q4：在线单路径动作条件；Q5：保留部分 Video-DiT hidden computation 与 Action-DiT，不保留完整 RGB 生成 | 在线 future-related representation conditioning；不是候选后果评估 |

这张表是人工审查的直接入口；如果只想确认五问测试是否产生了可区分结果，先看这里即可。`UNKNOWN`、模式依赖和证据边界仍以第 6 节及三份 source-first record 为准。

## 1. 我们现在只确认四件事

1. 论文作者批评了什么问题？
2. 模型训练时到底做了什么？
3. 部署时 planner 到底读取什么？
4. future 是否真的参与了候选动作的比较和选择？

## 2. 三篇论文的中文概括

### LAW

作者问题：端到端驾驶模型的视觉场景表示不够好；只做单帧自监督没有充分利用视频时间信息；普通未来预测没有考虑自车动作；像素级未来图像生成太慢。作者因此提出用“当前视觉特征 + 预测的自车轨迹”预测未来视觉 latent，作为自监督训练信号。

机制：

```text
当前图像 → 当前视觉 latent → 预测自车轨迹
                              ↓
                 与当前 latent 融合
                              ↓
                    预测未来 visual latent
                              ↓
              与真实未来帧提取的 latent 对齐
```

部署：根据锁定的官方代码审计，planner 先产生轨迹；future latent 分支的输出在测试时没有被拿回来重新选择或评分。也就是说，future latent 主要在训练阶段塑造表示和规划器，而不是部署时让 planner 观察一个未来再决定动作。

不能据此声称：LAW 能够针对多个候选动作分别模拟未来，或者拥有真实反事实世界模型。它训练时主要只有日志中的一条事实未来。

### Epona

作者问题：传统视频扩散模型通常固定长度、整体生成，难以做灵活的长时域自回归预测；GPT/token 方法又可能损失视觉细节和轨迹精度；现有方法还存在规划模块缺失、视频短、计算量大的问题。

机制：历史图像和历史自车运动先进入一个共享的时空表示，然后分成两个分支：

```text
历史图像 + 历史运动 → 共享历史 latent
                              ├→ TrajDiT → 未来自车轨迹
                              └→ VisDiT  → 下一帧视觉 latent / 图像
```

部署必须拆成不同模式：

- 规划模式：使用共享历史 latent 直接生成轨迹；官方代码审计显示视觉生成分支可以跳过。
- 世界生成模式：生成下一帧视觉结果，再把它用于下一轮自回归 rollout。
- 轨迹控制视频模式：给定外部轨迹，生成受其控制的视频。

不能据此声称：Epona 在规划时一定先为多个候选轨迹生成未来，再通过 scorer 选择最佳轨迹。当前证据更支持“直接生成轨迹 + 独立视觉 rollout 模式”。

### DriveLaW

作者问题：现有 world model 对规划的作用常常只是间接辅助，或者视频生成和规划只是并列的两个输出；视频生成器内部已经学到的场景动态和语义没有直接成为 planner 的输入；同时高质量视频生成和实时规划存在计算矛盾。

机制：

```text
历史驾驶视频 → Video-DiT 的视频生成过程
                         ↓
                中间 hidden state
                         ↓
                    Action-DiT
                         ↓
                    未来轨迹
```

部署：planner 读取的是视频生成过程中的内部 hidden state，而不是完整生成并解码后的 future RGB 视频。锁定的官方代码审计显示，在 canonical planning path 中只运行早期 Video-DiT 计算，完整视频去噪和 RGB 解码不必执行。

不能据此声称：DriveLaW 对每一个候选动作分别生成未来并评分。当前审计没有发现独立 candidate scorer，也没有发现完整的 candidate → future consequence → argmax 选择链。

## 3. 当前最小横向差异

| 关键问题 | LAW | Epona | DriveLaW |
|---|---|---|---|
| future 计算的主要作用 | 训练期辅助表示/规划学习 | 共享历史表示，并可独立做视觉 rollout | 在线提供 planner 使用的内部视频 hidden state |
| planner 是否读取完整 future | 否 | 规划模式不需要 | 否，读取中间 hidden state |
| 是否存在多个候选未来逐一评估 | 当前未发现 | 当前未发现 | 当前未发现 |
| 未来分支是否必须在线运行 | 否 | 规划模式可关闭，世界生成模式需要 | 规划路径需要部分 Video-DiT hidden computation |
| 最终动作如何产生 | 直接轨迹/waypoint 预测 | TrajDiT 直接生成轨迹 | Action-DiT 直接生成轨迹 |

## 4. 只需要你确认的 5 个问题

请不要审查英文细节，只判断下面的中文是否符合你对论文的理解：

1. **LAW**：future latent 主要是训练信号，部署时不用于重新选择轨迹。是否同意？
2. **Epona**：规划模式和视觉 rollout 模式必须分开，不能把 Epona 简化成“用未来视频给 planner 打分”。是否同意？
3. **DriveLaW**：planner 使用的是 Video-DiT 内部 hidden state，不是完整 future RGB，也不是 candidate scorer。是否同意？
4. 三篇论文的作者问题可以先单独记录，但暂时不判断作者批评是否客观成立。是否同意？
5. 现在只保留这三个机制差异，不立即命名路线、不建全量矩阵。是否同意？

## 5. 回复方式

你只需要回复类似下面的一句话：

```text
1同意，2同意，3同意，4同意，5同意。
```

如果有问题，只指出编号和修改意见，例如：

```text
第3条不同意：我认为 DriveLaW 的 xxx 仍然需要改成 xxx。
```

确认后，才进入下一步：把三篇论文的“作者问题维度”与上面的机制差异做一个小规模横向对照；仍然不扩展到 12 篇、不修改 ontology。

## 6. 五问验证草案

状态：`FIVE-QUESTION-VALIDATION-READY-FOR-REVIEW`

这一节把已经确认的 source-first 事实投影到五问，不新增路线、不修改 ontology。`UNKNOWN` 和“模式依赖”被保留，不强行压成单一答案。

| 五问 | LAW | Epona | DriveLaW |
|---|---|---|---|
| 1. 未来相关计算位于哪里？ | 训练期 action-conditioned future-latent prediction 分支 | 共享历史时空表示、TrajDiT 与 VisDiT 的相应计算分支 | Video-DiT 去噪过程及其 video-to-action hidden-state 接口 |
| 2. 未来对象、目标或中间表征是什么？ | 未来 visual latent | 未来 ego trajectory + 下一帧 visual latent/frame | 视频生成过程的中间 hidden representation；不是已被证明的显式 future state/target |
| 3. 未来相关信号是否进入动作链？ | 部署路径中没有；只进入训练图 | 没有证据表明生成 visual future 反向进入轨迹生成/选择 | 是，hidden signal 前向条件化 Action-DiT |
| 4. 未来机制承担什么角色？ | 训练期表示塑造/辅助预测 | 联合训练、单路径轨迹生成和视觉 rollout | 在线单路径动作条件，同时由分阶段训练支撑 |
| 5. 部署时保留什么？ | 直接 waypoint/trajectory path；future 输出不被消费 | 规划模式可跳过 VisDiT；世界生成模式保留视觉 rollout | 保留部分 Video-DiT hidden computation 与 Action-DiT，不保留完整 RGB 视频生成 |

### 6.1 验证结果（暂定）

1. **区分性通过：**五问能够区分三篇论文的训练期 future supervision、共享双分支、在线 hidden-state conditioning；不需要引入路线标签。
2. **没有被共同接口压平：**三篇都没有被错误归入“候选 future → score → select”，因为 Q3–Q5 能明确显示它们没有被证据确认存在 candidate-specific consequence resolver。
3. **模式分裂可处理：**Epona 的规划模式与视觉 rollout 模式需要在 Q1/Q4/Q5 中并列记录，说明五问能够表达模式依赖，而不是迫使论文只有一个部署答案。
4. **未知项仍可保留：**DriveLaW 的精确 denoising cadence、Epona 视觉 future 的因果含义、LAW future loss 的独立因果贡献仍然保留为未决问题。
5. **发现并收紧一个答案级重叠：**旧写法中 Q1 混入了训练/rollout 生命周期，导致 Q1 与 Q5 的答案部分重叠；这属于操作化措辞问题，暂不足以证明两轴应合并。收紧后，Q1 只记录计算位置，Q5 只记录部署残留；Q1/Q2、Q3/Q4、Q4/Q5 的职责仍可分开。

本节仍待人工审查；下方最小删除测试是基于现有 source-first 证据进行的内部验证，不代表已经通过人工审查。

### 6.2 最小桥接删除测试（内部验证草案）

| 论文 | 删除的五问中识别出的桥接 | 能否构造不含该 bridge 的规划主干 | 是否仍是原论文的方法 | 判断 |
|---|---|---|---|---|
| LAW | 删除 waypoint-conditioned future visual-latent prediction/loss | 可以保留或重新构造不含该分支的直接 planner 主干；未执行原始 checkpoint 的删改重跑 | 否；失去 LAW 用 action-conditioned future latent 塑造规划表示的核心回答 | 五问能识别训练期核心桥接 |
| Epona | 删除共享历史表示与 TrajDiT/VisDiT 的统一关系 | 可以分别保留或重建轨迹生成主干、视觉生成主干；可能需要替代输入或重训 | 否；失去统一轨迹—视觉生成系统，但必须保留模式差异 | 五问能识别多模式统一桥接 |
| DriveLaW | 删除 Video-DiT hidden signal → Action-DiT 的前向连接 | 可以概念上保留或重建独立 Action-DiT 主干，但需要替代输入或重训 | 否；失去“视频生成过程表征直接进入 planner”的核心回答 | 五问能识别在线 hidden-state bridge |

删除测试说明：这里是基于机制图的结构/身份测试，不是对原始 checkpoint 的可运行性重跑，也不是性能消融。它只支持“删除该 bridge 后，不能再声称复现原论文机制”；不支持“该 bridge 对性能提升具有因果必要性”。
