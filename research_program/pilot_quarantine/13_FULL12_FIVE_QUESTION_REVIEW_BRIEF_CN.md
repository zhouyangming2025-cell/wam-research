# canonical-12：五问全量投影中文审查简报

状态：`FULL12-FIVE-QUESTION-PROJECTION-READY-FOR-REVIEW`

日期：2026-09-18

本文件是对原三篇五问试点、WoTE/World4Drive 扩展试点的范围延伸。它只做 Q1–Q5 的全量证据投影，不创建路线标签、不修改 ontology、不建立新的矩阵，也不覆盖原有历史文档。

## 1. 冻结的 canonical-12 与证据位置

| ID | 论文 | 原始 Markdown | source-first 记录 |
|---|---|---|---|
| P0001 | Epona | `papers/raw_md/P0001_Epona/P0001_Epona.raw.md` | `reconstruction/P0001_EPONA_SOURCE_FIRST_RECORD.md` |
| P0009 | DriveLaW | `papers/raw_md/P0009_DriveLaW/P0009_DriveLaW.raw.md` | `reconstruction/P0009_DRIVELAW_SOURCE_FIRST_RECORD.md` |
| P0042 | WorldDrive | `papers/raw_md/P0042_WorldDrive/P0042_WorldDrive.raw.md` | `reconstruction/P0042_WORLDDRIVE_SOURCE_FIRST_RECORD.md` |
| P0045 | WoTE | `papers/raw_md/P0045_WoTE/P0045_WoTE.raw.md` | `reconstruction/P0045_WOTE_SOURCE_FIRST_RECORD.md` |
| P0046 | World4Drive | `papers/raw_md/P0046_World4Drive/P0046_World4Drive.raw.md` | `reconstruction/P0046_WORLD4DRIVE_SOURCE_FIRST_RECORD.md` |
| P0048 | LAW | `papers/raw_md/P0048_LAW/P0048_LAW.raw.md` | `reconstruction/P0048_LAW_SOURCE_FIRST_RECORD.md` |
| P0049 | Drive-JEPA | `papers/raw_md/P0049_DriveJEPA/P0049_DriveJEPA.raw.md` | `reconstruction/P0049_DRIVEJEPA_SOURCE_FIRST_RECORD.md` |
| P0061 | SeerDrive | `papers/raw_md/P0061_SeerDrive/P0061_SeerDrive.raw.md` | `reconstruction/P0061_SEERDRIVE_SOURCE_FIRST_RECORD.md` |
| P0062 | Metis | `papers/raw_md/P0062_Metis/P0062_Metis.raw.md` | `reconstruction/P0062_METIS_SOURCE_FIRST_RECORD.md` |
| P0063 | DynFlowDrive | `papers/raw_md/P0063_DynFlowDrive/P0063_DynFlowDrive.raw.md` | `reconstruction/P0063_DYNFLOWDRIVE_SOURCE_FIRST_RECORD.md` |
| P0064 | Discrete-WAM | `papers/raw_md/P0064_Discrete-WAM/P0064_Discrete-WAM.raw.md` | `reconstruction/P0064_DISCRETE_WAM_SOURCE_FIRST_RECORD.md` |
| P0065 | GraphWorld | `papers/raw_md/P0065_GraphWorld/P0065_GraphWorld.raw.md` | `reconstruction/P0065_GRAPHWORLD_SOURCE_FIRST_RECORD.md` |

原文是主要证据；官方代码审计只用于确认部署路径、版本差异和源码边界。Metis、DynFlowDrive、Discrete-WAM、GraphWorld 的代码级结论仍受源码不可用/未识别限制；SeerDrive 必须拆分论文 artifact 与公开 release artifact。

## 2. 五问的固定含义

| 问题 | 只回答什么 | 不吸收什么 |
|---|---|---|
| Q1. 未来相关计算位于哪里？ | 模块、分支、接口或过程位置 | 是否训练期/在线、是否部署保留 |
| Q2. 未来对象、目标或中间表征是什么？ | 预测对象、监督目标或未来生成过程中的中间表征 | 证据不足时把它升级为物理未来状态 |
| Q3. 未来相关信号是否进入动作链？ | 是否被动作生成或候选选择前向消费 | 仅因模块存在就判定部署使用 |
| Q4. 未来机制承担什么角色？ | 训练塑形、在线单路径条件、在线候选后果评估/选择等功能角色 | 具体部署模块清单 |
| Q5. 部署时保留什么？ | 哪些模块、模式和 future-related computation 保留/绕过/删除 | 重新定义机制所在位置 |

每个答案保留 `PAPER FACT`、`CODE FACT`、`OUR INFERENCE`、`UNKNOWN`、`NOT REPORTED`、`EVIDENCE BOUNDARY` 等状态；不把源码未知强行改成“没有”。

## 3. 12 篇论文的 Q1–Q5 实际结果

### 3.1 Q1–Q2：未来计算位置与未来对象

| 论文 | Q1：未来相关计算位于哪里？ | Q2：未来对象/目标/中间表征是什么？ |
|---|---|---|
| LAW | 训练期 action-conditioned future-latent prediction 分支。 | 由当前视觉 latent + 预测 waypoint 条件化的未来 visual latent；不是已确认的完整 world model。 |
| Epona | 共享历史时空表示，以及 TrajDiT/VisDiT 两个对应分支。 | 未来 ego trajectory 与下一帧 visual latent/frame；视觉分支可自回归 rollout。 |
| DriveLaW | Video-DiT 去噪过程及其 video-to-action hidden-state 接口。 | 中间视频生成 hidden representation；不是已证明的显式 future-time state/endpoint。 |
| World4Drive | action token 与 World Model Selector/ScoreNet 之间的 candidate-conditioned future-query/world-model 分支。 | 固定时刻 t+n 的候选 future latent；不是 WoTE 式多步 BEV rollout。 |
| WorldDrive | 训练期重型 TA-DWM/TA-DiT teacher；部署期轻量 FAR future-scene surrogate。 | trajectory-conditioned teacher future latent/scene representation，以及部署期 candidate-conditioned surrogate。 |
| WoTE | 候选动作与 Reward Model 之间的 candidate-conditioned recurrent BEV world-model rollout。 | 每个候选对应的多步 BEV future states 与 actions；不是 RGB future。 |
| SeerDrive | **论文：** BEV world model 与 future-aware planner 的交互/反馈分支；**release：** WoTE-like latent-world/reward evaluation path。 | **论文：** mode-specific final-horizon future BEV + future ego feature；**release：** candidate reward-related future representation，不能等同原论文 loop。 |
| Drive-JEPA | V-JEPA masked video-latent pretraining 分支；部署时只使用迁移后的 encoder/proposal planner。 | 随机 masked spatiotemporal latent target；不是已确认的 chronological physical future。 |
| Metis | 训练期 future-video expert 与 action expert 的 asymmetric token interface。 | action-conditioned future video latent tokens；目标是 logged factual future video latent。 |
| DynFlowDrive | 训练期 candidate-conditioned rectified-flow latent world model 与 stability criterion。 | 候选条件化 latent endpoint/flow path，目标为单一 factual next-step latent；flow time 不等于物理时间。 |
| Discrete-WAM | 共享 Transformer 中的 world/world-policy token-editing 任务；规划路径另有 decision/action token editing。 | future visual tokens、future action tokens、decision tokens；视觉/动作词表分开。 |
| GraphWorld | ECIG/GRU interaction encoder 与 flow-refined latent world-state branch。 | current structured `W_cur`、future-oriented `W_tgt` 及其内部 flow-refined latent；不是直接编码的 future observation。 |

### 3.2 Q3–Q5：是否进入动作链、功能角色与部署残留

| 论文 | Q3：future-related signal 前向进入动作链？ | Q4：机制角色 | Q5：部署保留什么？ |
|---|---|---|---|
| LAW | 否；future latent 只进入训练图，不进入测试时 waypoint selection/resolver。 | 训练期 action-aware representation shaping。 | 直接 waypoint/trajectory path；future output 不被消费。 |
| Epona | 没有证据表明生成 visual future 反馈轨迹生成或选择。 | 联合训练；规划模式的单路径轨迹生成；独立视觉 rollout/user-control 模式。 | 规划模式可跳过 VisDiT；world-rollout 模式保留视觉生成。 |
| DriveLaW | 是，但仅为 hidden signal → Action-DiT 的单路径条件；没有 candidate-specific feedback。 | 在线单路径动作条件；完整视频生成不是 planner 的输入。 | 部分 Video-DiT hidden computation + Action-DiT；不保留完整 RGB generation。 |
| World4Drive | 是；candidate future latents 进入 ScoreNet 并改变 argmax trajectory selection。 | 在线候选评分/选择；主要是 factual-future consistency/mode matching，不等于一般反事实价值函数。 | candidate generator、future-latent predictor、ScoreNet、resolver 保留；factual future target 不可用。 |
| WorldDrive | 是；FAR surrogate 进入 future-aware reward 并改变候选 argmax。 | 重型 TA-DWM teacher → FAR surrogate 蒸馏；部署期候选 future-surrogate 评分。 | planner/FAR/surrogate/reward/resolver；完整 TA-DiT teacher off。 |
| WoTE | 是；每候选 BEV future 进入 Reward Model 并改变最高 reward 选择。 | 在线候选后果评估与选择；但周围车辆 logged/GT future 在审计路径中非反应式。 | candidate generation/refinement、recurrent BEV rollout、Reward Model、resolver。 |
| SeerDrive | **论文：** 是，future BEV 进入轨迹生成，refined ego feature 再反馈 world model；**release：** 是，future-related reward path 参与候选选择，但原始 iterative loop 不确认。 | **论文：** world↔planner 内部迭代共精炼；**release：** WoTE-like candidate evaluation/refinement。 | **论文：** future BEV + iterative feedback；**release：** reward/evaluator path，明确不保留原论文 iterative interaction。 |
| Drive-JEPA | 否；JEPA predictor 不在线，proposal scorer 读取 proposal features 与 simulator utility，不是 future predictor。 | predictive representation pretraining + simulator-distilled proposal utility selection。 | encoder、WADA/refinement、scorer、版本相关 momentum selection；JEPA predictor off。 |
| Metis | 否；future video 由 action 条件化，但 action token 不读取 future video；影响主要通过训练梯度。 | asymmetric world-loss-shaped action policy；训练联合、部署 action-only。 | current-context/action expert + action-flow denoising；future video generation bypassed。 |
| DynFlowDrive | 部署时否；world-derived criterion 只用于 score-head supervision。 | 训练期 world-derived candidate-label/selector teacher；不是在线 candidate evaluator。 | candidates + learned score head + argmax；world model/future latent/stability off。 |
| Discrete-WAM | mandatory planning path 中否；decision → action-token editing，不要求 future visual generation 或 future utility scorer。 | shared world/world-policy multi-task pretraining + hierarchical action-token editing。 | decision prediction、confidence/schedule-guided action editing、trajectory decoding；future visual mode非必需。 |
| GraphWorld | 是；refined world state 在线调制 motion queries 和 ego planning queries，但没有 candidate-specific future resolver。 | online structured world-state-conditioned planning；训练含 temporal world-state consistency。 | ECIG、history/map world state、短 flow refinement、importance/residual modulation、planning heads。 |

证据状态不是“论文是否强”，而是“该条判断由什么支撑”：LAW/Epona/World4Drive/WoTE/WorldDrive 具有论文+既有源码审计；SeerDrive 是论文/代码双 artifact；Drive-JEPA 具有 paper+source audit；Metis/DynFlowDrive/Discrete-WAM/GraphWorld 的部署细节主要为 paper-level，源码部分保持 `UNKNOWN` 或 `NOT REPORTED`。

## 4. 全量投影的效果

### 4.1 五问确实产生了第一层横向区分

五问能够稳定区分以下事实，而不需要路线命名：

1. **future predictor 是否在部署动作链中被消费。** LAW、Drive-JEPA、Metis、DynFlowDrive、Discrete-WAM 的主要规划路径没有被证据确认需要在线 future prediction；DriveLaW、GraphWorld、World4Drive、WorldDrive、WoTE 和 SeerDrive 的相应部署 artifact 中，future-related representation/compute 被前向使用，但使用位置不同。
2. **进入动作链的方式不同。** DriveLaW 是生成过程 hidden state 直接条件化 Action-DiT；GraphWorld 是结构化 world state 调制 planning queries；World4Drive/WorldDrive/WoTE 是 candidate-specific future 进入 resolver；SeerDrive 论文是 future-aware planner + world↔planner 反馈。
3. **部署生命周期不同。** Metis 是 future-video loss 通过训练梯度塑造 action expert；DynFlowDrive 是 world-derived candidate criterion 蒸馏到 score head；WorldDrive 是 heavy teacher 蒸馏成在线 surrogate；Drive-JEPA 是 predictive encoder transfer；这些不能被同一句“未来辅助训练”替代。
4. **模式/版本依赖是可表达的。** Epona 的 planning/world-rollout/user-control 模式，以及 SeerDrive 的 paper/release 差异，都不能被强行压成一个 Q5 答案。

### 4.2 五问单独仍然不充分

全量压力测试确认：五问不是完整技术路线描述。至少有三组论文会在只看 Q3 的情况下过度接近：

- **World4Drive / WorldDrive / WoTE：** 都是 candidate future representation → score/reward → select，但分别是 fixed-time latent matching、teacher-distilled future surrogate、recurrent BEV rollout + reward。
- **LAW / Metis / DynFlowDrive：** 都可被粗略写成“future 在训练期帮助 planner”，但分别是 action-conditioned latent prediction loss、asymmetric future-video gradient coupling、world-derived candidate selector teacher。
- **DriveLaW / GraphWorld / SeerDrive：** 都有在线 future-related representation 进入规划，但分别是 hidden-state conditioning、current structured world-state modulation、future-BEV/world↔planner iterative refinement。

因此，五问必须与每篇 source-first 记录中的三类桥接信息同时阅读：

```text
Q1–Q5：定位 future-related computation 的部署因果位置
core bridge：说明删除后论文为何不再是该方法
future semantics：说明“future”究竟是什么
provenance/boundary：说明监督是否是 factual、simulator-derived、teacher-distilled 或 reactive counterfactual
```

这不是新增第六问，而是防止五问被共同末端接口压平的证据要求。

### 4.3 碰撞与失败测试

| 测试 | 结果 | 结论 |
|---|---|---|
| Q1 与 Q5 是否重新碰撞？ | 暂未发现。 | Q1 记录位置，Q5 记录部署残留；两者职责可分。 |
| Q2 是否把 hidden/process representation 误写成物理 future state？ | 在 DriveLaW、Drive-JEPA、DynFlowDrive、GraphWorld 中可明确避免。 | Q2 的“对象/目标/中间表征”措辞必要。 |
| Q3 是否把所有在线 future use 都误判为候选后果评估？ | 若不结合候选身份和 resolver，会误判 DriveLaW、GraphWorld、SeerDrive。 | Q3 必须与 Q4 及 candidate/resolver 证据联读。 |
| Q4 是否把训练作用和部署作用混在一起？ | Metis、DynFlowDrive、WorldDrive 压力测试通过分离。 | Q4 负责功能角色，Q5 负责部署残留。 |
| Q5 是否能表达模式/版本差异？ | Epona、SeerDrive 可以；需保留多 artifact/模式列。 | 单一论文单一答案不是强制要求。 |
| 五问能否独立保留不可替代核心？ | 不能完全独立完成。 | 必须保留 source-first core bridge，而非只留五问表。 |

## 5. 当前暂定结论

`PASS-WITH-BOUNDARY`：五问已经可以推广到 canonical-12，作为统一的离线审查接口是有效的；它能稳定回答“未来计算在哪里、未来是什么、是否前向进入动作链、承担什么角色、部署保留什么”。但它不能单独承担最终技术路线分类，也不能替代每篇论文的 core bridge、future semantics、provenance 和 paper/code boundary。

因此本轮只确认：

- 12 篇均已完成 Q1–Q5 初步投影；
- 五问没有被新增论文直接击穿；
- 五问不能压平三组关键机制差异；
- 未新增 ontology、路线标签或矩阵；
- 所有源码缺口、反事实边界、模式差异和 `UNKNOWN` 均保留。

本文件仍等待人工审查；在审查通过前，不把表中相似项升级为技术路线，也不据此比较哪条路线“更优”。
