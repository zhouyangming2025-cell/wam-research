# 02 — Canonical 12 来源优先路线工作簿

**状态：WORKING BASELINE — 不是路线分类，也不是论文摘要。**  
本表把已经可复用的跨论文观察放到相同接口下。`暂定机制位置` 只是下一轮反例比较的起点；任何空缺均保留为 `UNKNOWN`。

## 记录约定

- `PF / PB`：同一论文中必须区分的 artifact / mode。
- `PAPER`：已由 raw paper 支持；`INFERENCE`：目前是跨材料解释；`UNKNOWN`：尚不能由可用资料确认。
- “进入动作链”只问该论文的主张或可复核实现，不把训练监督、可视化解码或离线评测自动视作部署闭环。

|ID / artifact|Q1：未来计算位置|Q2：未来对象|Q3：进入动作链？|Q4：作用|Q5：部署状态|暂定机制位置（待反例）|最关键边界 / 下一核验|
|---|---|---|---|---|---|---|---|
|P0001 Epona — planning-only / video-assisted|PAPER：多模态规划与视频生成支路；需按模式拆分|PAPER：视频/生成空间相关表征|PAPER：planning-only 可关闭视频支路；视频未来是否回到规划器不能据此断言|INFERENCE：共享或辅助世界相关表征，不等同候选选择|PAPER：模式依赖|直接策略中的世界知识；视频模式另列|锁定两个模式各自的实际 planner 输入与代码路径。|
|P0009 DriveLaW|PAPER：视频 DiT 及 Action-DiT 接口|PAPER：所选生成器的 hidden state|PAPER：hidden state 条件化 Action-DiT|PAPER：在线单路径条件，而非已证实的候选后果评估|PAPER：生成/隐藏状态接口保留|保留在线生成器状态 → 直接动作|不要把 hidden state 写成“已解码视频 rollout”或候选评分器。|
|P0042 WorldDrive|PAPER：teacher world model 与 FAR / rewarder|PAPER：世界前瞻被蒸馏为 future-aware 评分能力|PAPER：候选经评分重排/选择；显式视频 rollout 在推理被避免|PAPER：候选后果的评分/选择|PAPER：部署保留蒸馏后的评分能力|候选后果 → 评估/选择|核验候选生成器、评分接口与 teacher/student 版本。|
|P0045 WoTE|PAPER：候选轨迹、未来 BEV 及 reward model|PAPER：候选对应的未来 BEV 后果|PAPER：候选 → 未来 → reward → 选择|PAPER：在线轨迹评估|PAPER：评估/选择链保留|候选后果 → 评估/选择|区分自车候选后果和环境反应；非反应式边界不可省略。|
|P0046 World4Drive|PAPER：意图/未来查询与模型选择相关模块|PAPER：候选相关未来表征|PAPER：存在候选/评估结构；准确推理接口待原文定位复核|INFERENCE：候选后果或模型选择|UNKNOWN：最终部署对象与是否显式保留未来预测器|候选后果 → 评估/选择（暂定）|补齐真实 inference target、candidate commitment 与 selector。|
|P0048 LAW|PAPER：训练中的 latent/action/world 预测任务|PAPER：训练目标中的未来 latent / 表征|PAPER：主部署动作路径使用未来表征，未获证实|PAPER：训练期世界相关监督|PAPER：未来预测分支应视为训练期，除非代码反证|世界监督编译进直接策略|禁止把“预测 future latent”写为在线推演。|
|P0049 Drive-JEPA — PF / PB|PAPER：预训练 predictor；另有规划相关候选/评分路径|PAPER：JEPA 预测表征；PB 的伪轨迹/评分对象|PAPER：PF 与 PB 必须分开；共同结论尚不足|PAPER：表征预训练与规划评分不可混写|UNKNOWN：每个 artifact 的保留/删除路径需分别锁定|PF：世界监督直接策略；PB：评分器路径（均暂定）|先补齐 PF/PB 的源码、候选、监督与部署开关。|
|P0061 SeerDrive — paper / release|PAPER：世界与规划的双向建模图|PAPER：场景演化与规划轨迹|PAPER：论文叙述存在双向接口；发布实现是否同构为 UNKNOWN|PAPER：世界—规划迭代/互相约束|UNKNOWN：固定 release 的实际保留模块|世界—规划双向修正（论文个案）|论文图和代码版本不可合并；先固定 release commit。|
|P0062 Metis|PAPER：训练期未来帧/未来观测监督|PAPER：未来帧或未来观测|PAPER：推理依赖当前观测；未来帧不进入主部署链|PAPER：训练期监督|PAPER：未来帧分支不保留为推理输入|世界监督编译进直接策略|核验所有推理输入，避免把实验可视化当部署。|
|P0063 DynFlowDrive|PAPER：候选条件 flow 与稳定性/评分相关训练结构|PAPER：候选条件的未来/稳定性信号|PAPER：部署是否保留独立世界分支证据不足|PAPER：训练准则或评分教师（暂定）|PAPER：论文称无额外测试推理成本；具体删留仍需源码|训练期准则 → 部署评分/策略（暂定）|源码与最终 score/teacher 关系为高优先级 UNKNOWN。|
|P0064 Discrete-WAM|PAPER：world prediction、policy、joint training 任务|PAPER：离散世界/视觉 token|PAPER：政策路径为 decision → action token；未来视觉是否为主部署输入未证实|PAPER：联合训练 / 语义决策|UNKNOWN：各 token 生成器部署保留情况|语义决策 → 动作 token（个案）|拆训练任务与实际 decode/decision/action 路径。|
|P0065 GraphWorld|PAPER：在线 ego-centric relational world representation|PAPER：关系世界状态，不是显式多步场景生成|PAPER：世界状态条件化/支持规划；最终 commitment 接口待核验|PAPER：在线结构化状态|UNKNOWN：最终行动模块和代码可用性|保留在线关系状态 → 动作（暂定）|不得写成视频未来 rollout；补齐 planner/action 的可复核接口。|

## 目前允许提出、但尚未定名的跨论文分叉

1. 未来对象是**训练目标**，还是部署中保留的**状态/条件**，还是候选的**后果**？
2. 若它进入部署，作用是**单路径条件化**、**候选评分选择**，还是**世界—规划双向修正**？
3. 世界相关模块被删除后，动作链是否仍成立（Core-Bridge deletion）？
4. 一个相同外观的“future latent”是否在对象、接口和选择权上实际不同？

只有当以上分叉有跨论文重复、来源可核验且能承受反例时，才在后续文件提出路线名称。