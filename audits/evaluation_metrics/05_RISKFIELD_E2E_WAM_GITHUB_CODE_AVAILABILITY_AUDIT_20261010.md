# 风险场 × 端到端驾驶 / WAM：严格筛选的开源 GitHub 实现（2026-10-10，修订）

> **修订原因：上一版错误地把一般风险场/传统规划算法仓库列为优先对象。用户明确：只关心“风险场真正接入端到端驾驶或 WAM 模型”的 GitHub 实现。** 本版替换旧的项目推荐，不新增分支。  
> **证据状态：GITHUB-SOURCE-READ / RUNTIME-UNTESTED。** 已核对仓库文件树及关键调用链，未 clone、下载模型、安装依赖或运行任何实验。  
> **准入规则：必须同时满足**（1）端到端驾驶模型或学习式驾驶策略有公开实现；（2）仓库中能找到风险场生成/预测代码；（3）能找到风险场在模型训练、在线决策、候选评价或安全控制中的实际接入点。只有论文、README 或独立 Field 计算函数的项目**不算已开源 E2E+RiskField 系统**。
>
> 参考专项：[04 风险场 × E2E/WAM 指标方向](04_RISKFIELD_E2E_WAM_METRIC_SPECIAL_STUDY_20261010.md)。

## 1. 符合条件、实际有源码的项目

| 项目 | 模型端 | 风险场端 | 接入链条 | 复现状态与边界 |
|---|---|---|---|---|
| **[METEOR](https://github.com/tier4/METEOR)**（TIER IV；`main@dc193a81e9959de57b751e269127ae9b67e3f300`） | 八相机多任务端到端驾驶网络，输出 E2E 轨迹模式与置信度；`bevlane/model.py`、`train.py` 等代码 | `bevlane/risk_field.py` 生成连续 BEV 风险标签；`DepthSegIPMNetV28.risk_head` 预测场，`risk_loss` 监督 | 风险标签→网络 risk head→`guardrail.py:risk_pick` 沿各候选轨迹采样平均风险，用 `confidence - λ*risk` 比较；演示路径 `demo_rgbd_bev.py` 包含函数调用 | **有源代码、训练脚本、部署脚本、声称已发布的 PyTorch checkpoint/ONNX 与 demo 数据**。但已发现演示推理路径的风险排序**可能失效（见下文代码问题）**；不等于已证明 risk_pick 实际改变最终轨迹或在 NAVSIM 上有效 |
| **[Safe-Human-in-the-Loop-RL](https://github.com/OscarHuangWind/Safe-Human-in-the-Loop-RL)**（IEEE T-ITS 2024；`master@d6c1fd21c5f18a84c1eba49be5edfd917a2306f7`） | SMARTS 内端到端深度强化学习驾驶策略：`Network.py`、`drl_agent.py`、`main.py` | `dynamic_potential_field.py:FDPF`，Frenet 空间动态势场风险强度 | `authority_allocation.py:Arbitrator.authority` 获取场值，分别估计 RL 动作、人类动作导致的风险变化，决定双方的控制权分配；**只在 shared-control 开启时该路径使用场** | 有真实 DPF 与 RL/共享控制融合源码和仿真说明；并非传感器到轨迹的现代 WAM，亦不是 NAVSIM/Bench2Drive 实现；尚未实际跑通 |

### 1.1 METEOR 值得阅读的官方文件

- [风险场 GT](https://github.com/tier4/METEOR/blob/dc193a81e9959de57b751e269127ae9b67e3f300/bevlane/risk_field.py)：动态目标椭圆高斯（速度前导）、静态占用衰减，聚合为 `1-exp(-1.6*sum(intensity))`，带自车距离调制。这里输出经验风险量 **[0,1]**，不能未经标定说成真实碰撞概率。
- [网络风险预测头](https://github.com/tier4/METEOR/blob/dc193a81e9959de57b751e269127ae9b67e3f300/bevlane/model.py)：`DepthSegIPMNetV28` 在 BEV feature 上预测 risk logits，使用高风险加权 L1 监督。
- [候选风险评分](https://github.com/tier4/METEOR/blob/dc193a81e9959de57b751e269127ae9b67e3f300/bevlane/guardrail.py)：`risk_pick` 对每个 6 点候选计算沿轨迹平均 risk，组合模型置信度 `confidence - λ*mean_risk`。
- [演示调用路径](https://github.com/tier4/METEOR/blob/dc193a81e9959de57b751e269127ae9b67e3f300/bevlane/demo_rgbd_bev.py)：**注意潜在实质性问题**：在 `if args.guard: risk_pick(...)` 后，代码重新从 `_pr` 生成 `_k2`，考虑 prev-mode、直行偏置并以 `if _k2 != _k: _k = _k2` 覆盖。就**此段代码而言**，最终 `_k` 总等于不依赖 risk 的 `_k2`；因此不能声称此演示已经有效使用 risk_pick 来决定最终轨迹。这是**源码静态逻辑结论，未运行验证**。其他实际部署路径有无独立风险选择逻辑尚待查。
- [模型与示例数据发布说明](https://github.com/tier4/METEOR/blob/dc193a81e9959de57b751e269127ae9b67e3f300/README.md)：列出 [AutowareFoundation/meteor](https://huggingface.co/AutowareFoundation/meteor) 中的 ONNX/PyTorch 和示例数据，**本轮未逐文件下载核对模型权重与加载测试**。

**评价**：目前找到的项目中，与“高斯风险场 + learned E2E planning + 轨迹级风险评价”接口最直接贴近。但训练/推理实际选轨效果存在代码审计疑点；在拿来做研究 baseline 前必须先证明 risk head 的计算与 final action 的因果连接，最好固定候选对 `λ=0` 与 `λ>0` 做最小对照，不能预先称其完整复现。

### 1.2 SafeHiL-RL 的代码证据

- [FDPF 数学代码](https://github.com/OscarHuangWind/Safe-Human-in-the-Loop-RL/blob/d6c1fd21c5f18a84c1eba49be5edfd917a2306f7/dynamic_potential_field.py)：`FDPF.getIntensityAt(...)` 用 Frenet 坐标、相对速度和障碍车场强求风险。
- [风险参与决策](https://github.com/OscarHuangWind/Safe-Human-in-the-Loop-RL/blob/d6c1fd21c5f18a84c1eba49be5edfd917a2306f7/authority_allocation.py)：`self.field = FDPF()`、`field.update`、`current_dpf`、`rl_pred_dpf`、`human_pred_dpf`，对两种动作的风险变化做 `coupled_normalize` 后返回控制权系数。
- **限制**：该算法的场是共享控制仲裁，不是对一组 WAM 候选做统一 PDMS 风险评分；不能因为作者使用“end-to-end RL”就当成现代 world-model action-based planner。

## 2. 相关论文有 GitHub 项目页，但当前不符合“实际 E2E+RiskField 代码公开”

| 论文 | GitHub 状态核查 | 结论 |
|---|---|---|
| **FlowDrive: Energy Flow Field for End-to-End Autonomous Driving** | [AstrixDrive/FlowDrive](https://github.com/AstrixDrive/FlowDrive) `main@d063b0fb94998993369e88306894ec1ce8dc2e2a` 树中仅 6 blobs，LICENSE/README/docs/assets；**无训练/模型推理/risk field 模块代码**；README 仍“coming soon” | **PLACEHOLDER，不能称已开源模型** |
| **READ: Learning Risk-Informed Fields for E2E Driving** | [arXiv:2609.12371](https://arxiv.org/abs/2609.12371)，论文确实做了 E2E+learned risk field；本轮未找到可确认官方源码 | **PAPER-ONLY/NO-VERIFIED-OFFICIAL-REPO** |
| **DRiF: Data-Driven Risk Fields for Safer E2E Driving** | [arXiv:2609.10377](https://arxiv.org/abs/2609.10377)，作者称后续开源；本轮未核实官方 risk field+BEV planner 代码 | **PAPER-ONLY/COMING-SOON**，**绝不能拿 `SAS-HKU/DRIFT` 冒充 DRiF** |
| **RiskMM: Risk Map as Middleware** | [arXiv:2508.07686](https://arxiv.org/abs/2508.07686)，论文报告 V2X end-to-end risk map planning；本轮未确认官方源码 | **PAPER-ONLY/NO-VERIFIED-OFFICIAL-REPO** |
| **FusionAssurance** | [arXiv:2405.00316](https://arxiv.org/abs/2405.00316)，论文将 potential field 加 MPC safety layer 以辅助 E2E planner；检索未核实作者官方 E2E+potential-field 集成 GitHub | **PAPER-ONLY/NO-VERIFIED-OFFICIAL-REPO** |

“没找到”只意味着本轮没有经核验可访问的官方集成源码；不能断言永远不会开源或不存在任何私有实现。

## 3. 明确排除（不是本次用户要的开源项目）

- [SAS-HKU/DREAM](https://github.com/SAS-HKU/DREAM)、[SAS-HKU/DRIFT](https://github.com/SAS-HKU/DRIFT)、[gisgrid/RESPOND](https://github.com/gisgrid/RESPOND)、[PeterWANGHK/Benchmark-RiskField](https://github.com/PeterWANGHK/Benchmark-RiskField)、[Dispacher/driving-risk-field-01](https://github.com/Dispacher/driving-risk-field-01) 等：有风险场/传统混合规划/决策或场本身评价的实现，**但本次没有验证它们包含一个正式 E2E/WAM 模型的完整风险场接入代码**。因此不纳入“风险场+E2E/WAM 已开源”结果，也不再推荐用户优先下载。
- `SAS-HKU/DRIFT` 是 PDE 风险场传播项目，和 Tsinghua `DRiF` **名称相似但不同论文**。
- [FARPlan](https://github.com/WUTAD-Wjy/FARPlan)：GitHub 树仅 LICENSE/README，不具备实际模型源码，排除。

## 4. 我们下一步怎样用这些发现

**若要马上找一个“风险场+端到端”确有公开代码的研究实现：**
1. 首先源码审计 **METEOR**，明确风险 head、reward/trajectory selection、模型 checkpoint 与运行路径。静态检查发现 `risk_pick` 的最终选择可能被覆盖，应先核验和修复调用链。
2. 再研究 **SafeHiL-RL** 的风险场对不同控制动作的强度评估与权力分配，属于与 WAM/Benchmark 有距离的学习式控制先例，不建议作为 NAVSIM 直接 baseline。
3. 对 **READ/DRiF/FlowDrive** 应继续监测官方代码发布，**尚不能启动官方模型复现**；可用论文机制与现有 E2E 模型做独立实现，但不可宣称复现了官方系统。

当前没有找到一个**“开箱即用的 NAVSIM/WAM + 风险场完整官方源码”**，因此结论是：**确有 E2E+RiskField 开源实例，最具体可查的是 METEOR；现代 WAM/NAVSIM 论文中直接对应 READ/DRiF/FlowDrive 的完整官方开源代码仍未核验到。**

**本文件修订只改变第三方项目评价的聚焦口径；不改 main，不开新分支，不执行第三方代码。**
