# 评价指标专题：仓库现有资产基线审计（2026-10-10）

> 状态：**仓库资产基线审计完成；评价指标论文系统普查尚未启动。**  
> 工作分支：`codex/evaluation-metrics-baseline-audit-20261010`；审计基线：`main@cb05048dfb822e95d44e52dd85b830c750411e2c`。  
> 本记录只确认“仓库有哪些材料、如何复用、当前缺口在哪里”。它**不是**评价指标文献已查全、创新点已确认或新研究方向已正式替代现有研究状态的声明。  
> 核对方式：GitHub `main` 的递归文件树、仓库 README/state 文件、选择性原文与审计报告，以及四个现存历史分支文件树。所有历史判断须回到其来源核验。

## 1. 本轮需求与研究边界

用户在 2026-10-09 组会后调整研究优先级：优先全面调研**端到端自动驾驶/WAM 的 Benchmark 评价指标创新**，并扩展到**传统规划/控制/机器人领域可迁移的轨迹评价思想**。数据集创新暂列低优先级，训练损失、候选评分器作为关联材料，不与正式 Benchmark 指标贡献混为一谈。

文献按“**论文实际主要贡献**”而非标题关键词分类：

- **B1｜Benchmark/最终评价指标本身**：新指标、原指标计算/阈值/聚合改造、评价协议及评测体系创新；进一步区分 **B1a 指标公式** 与 **B1b 仿真/场景/评测协议**，防止把评测平台工作算成纯评分公式创新。
- **B2｜模型内部评价**：训练 reward/loss、候选 trajectory scorer、ranking/value/reward model；只能作为相邻研究或向 B1 迁移的线索，不累计进 B1 核心数量。
- **B3｜传统可迁移评价理论**：连续 trajectory cost、风险场、概率与尾部风险、IOC/IRL、硬约束/安全余量、交互/鲁棒性评价；记录已有端到端驾驶适配情况，不能把“传统已有”直接记为新颖。
- **D｜数据集与标注**：本轮保留索引但低优先级，必要时作为 B1 的配套构件。

## 2. 仓库直接核实的现有资产

GitHub 默认分支 `main` 的完整递归树：**1,587 个对象**，返回 `truncated=false`；其中 `papers/raw_md/` 下通过 `Pxxxx_*/*.raw.md` 路径核实 **74 篇原始论文 Markdown**。**74 是仓库材料量，不是 74 篇“评价指标创新论文”**。

| 可复用资产 | 具体入口 | 现有作用与局限 |
|---|---|---|
| NAVSIM v1 | [P0032 原文](../../papers/raw_md/P0032_NAVSIM/P0032_NAVSIM.raw.md) | PDMS、非反应式仿真、评价构成；属于 Benchmark 基线 |
| nuPlan | [P0031 原文](../../papers/raw_md/P0031_nuPlan/P0031_nuPlan.raw.md) | 规划任务、闭环与评价背景；注意此原文题名为 `nuPlan: A closed-loop ML-based planning benchmark for autonomous vehicles`，与用户提到的另一篇 nuPlan benchmark 论文不可不核对就视为同一原文 |
| Bench2Drive | [P0033 原文](../../papers/raw_md/P0033_Bench2Drive/P0033_Bench2Drive.raw.md)、[Wave4 审计](../literature/PHASE_B_WAVE4_BENCH2DRIVE_HUGSIM_AUDIT.md) | 场景化、短路线、多能力评测，主要是体系/协议贡献，不只是指标公式 |
| ReactSim-Bench | [P0014 原文](../../papers/raw_md/P0014_ReactSimBench/P0014_ReactSimBench.raw.md)、[Wave4 审计](../literature/PHASE_B_WAVE4_REACTSIMBENCH_AUDIT.md) | 反应式模拟行为评测，须区别于自车规划 PDMS |
| 既有横向可比性审计 | [Wave1](../../landscape/PHASE_B_WAVE1_COMPARABILITY_AUDIT.md)、[Wave2](../../landscape/PHASE_B_WAVE2_COMPARABILITY_AUDIT.md) | 已记录 NAVSIM v1/v2 指标与协议不能混比、WoTE 候选评分和训练/评测归因等 |
| 评价器和模型内部得分 | [DriveReward 审计](../literature/PHASE_C6_DRIVEREWARD_AUDIT.md)、[RiskWorld 审计](../literature/PHASE_C6_RISKWORLD_AUDIT.md)、[WoTE 原文](../../papers/raw_md/P0045_WoTE/P0045_WoTE.raw.md)、[DriveSuprim 原文](../../papers/raw_md/P0022_DriveSuprim/P0022_DriveSuprim.raw.md)、[Hydra-MDP 原文](../../papers/raw_md/P0021_HydraMDP/P0021_HydraMDP.raw.md)、[DrivoR 原文](../../papers/raw_md/P0060_DrivoR/P0060_DrivoR.raw.md) | 对 B2 有用；**不能充当新 Benchmark 论文计数** |
| 仿真评价边界 | [ProSim 审计](../literature/PHASE_C7_PROSIM_AUDIT.md) | 反事实真值/反应性评价边界，可作为新指标的验证约束 |

在 `main` **路径清单**中未发现 `research_program/evaluation_metrics`、`audits/evaluation_metrics`（本提交前）、StyleDrive 原文、NAVSIM v2 / Pseudo-Simulation 原文的独立 `raw.md`。这表示 **仓库现有索引缺失**，不表示这些研究在线不存在。旧文档提到 NAVSIM v2，但这不同于已 ingest/核读其权威原文。

## 3. 历史分支与文档治理边界

2026-10-10 通过 GitHub 分支列表确认远端当前可见：`main`、`codex/canonical12-mechanism-reconstruction`、`codex/pilot-quarantine-law-epona-drivelaw`、`codex/preserve-research-foundation`、`codex/wam-vla-22-dataset-audit-20260928`。后四支递归文件树已检查。

- 旧 `codex/canonical12-mechanism-reconstruction` 等分支含大型 `research_program/`、`outputs/` 历史层；这主要是**机制路线/ontology**工作，并非现成的指标专题账本。
- [主分支 README](../../README.md) 和 [DECISION_LOG](../../state/DECISION_LOG.md) 指出旧分支不能直接恢复为当前规范依据；`main` 是现存研究状态的权威入口。
- [CURRENT_STATE](../../state/CURRENT_STATE.md)、[NEXT_TASK](../../state/NEXT_TASK.md) 在审计基线仍将 C.7/BridgeSim 作为既定任务，并暂停研究方向收敛。**用户近期组会的评价指标新优先级尚未同步到这些状态文档**。
- README 禁止冗余的 summary、map、queue、handoff 或第二投影层。因此本轮仅新增这份有独立核查范围的**审计原始记录**，暂不另建重复的任务入口或综述；后续若要正式更改主线，应在获得明确授权后更新已有状态文件而不是悄悄改变。

## 4. 近期专题调研的“仓库外资产”

用户提供的前期调研记录包含三类：① NAVSIM v1/v2、Bench2Drive、nuPlan、StyleDrive；② 评价器/reward/候选打分代表论文 15 篇专题阅读（含 NAVSIM）；③ 传统轨迹评价方法 13 篇专题核读、另有六项补读。ChatGPT Library 可找到 `NAVSIM_metrics_group_meeting_report_CN.md`（2026-10-07），其中登记 74 篇材料普查、37 篇相关材料等。

**证据状态必须分清：**
- 这些是“用户提供的历史调研与独立 Library 报告线索”，并不等于完整原文/代码/审计成果已经全部位于此 GitHub 仓库。
- 已在 `main` 找到的论文必须复用原路径；未在仓库找到的 StyleDrive、NAVSIM v2 等需登记 `NOT-INGESTED`，后续按权威原文逐一核验。
- 15、13、37 和 74 的**口径不同**，不能相加形成“已核读 100+ 评价指标论文”的结论。

## 5. 审计结论与下一步工作入口

**结论：ASSET-BASELINE-PASS / BENCHMARK-METRIC-LITERATURE-INCOMPLETE。**

1. 可用资产充足：已存在 NAVSIM v1、nuPlan、Bench2Drive、ReactSim-Bench、WoTE 等一手原文与部分分项/协议审计，前期工作不能丢失或重复 ingest。
2. 主要缺口不是“没有阅读 WAM 论文”，而是**缺少 B1a（直接修改/新增最终评分指标）论文的系统识别、创新机制对照和覆盖证据**；B1b 与 B2 不能混算。
3. 旧分支 `research_program/` 为历史研究层，不应直接复制成新专题入口。当前专题记录放在 `audits/evaluation_metrics/`，新文件必须提供独立证据用途。
4. 此轮未进行网上新论文全面搜索、源码重审、指标实验或创新性定案；不能据此声称文献已找全或存在尚无人使用的指标。

**建议下一轮执行步骤（尚未执行）：**

- 从用户现有清单和仓库原文去重，建立 **B1a/B1b/B2/B3 论文证据登记**：论文身份、来源 URL、贡献性质、指标定义、评测协议、实验验证、审计状态、是否已有本地 raw md。
- 首先追踪并核对 StyleDrive、NAVSIM v2/Pseudo-Simulation、近期直接提出新评分的论文，然后通过引用链和相关会议论文扩展 B1a。
- 在完成 B1a 覆盖后，再与 B3 传统评价思想交叉比对；对创新机会只标记 `CANDIDATE / UNVERIFIED`，不直接下结论。
- 形成评价方法对照时特别检查阈值/分辨率、权重、聚合、仿真反应性、原版兼容性和实验所能支持的最强结论。

## 6. 固定审计基线

- 仓库：<https://github.com/zhouyangming2025-cell/wam-research>
- 固定 `main`：<https://github.com/zhouyangming2025-cell/wam-research/tree/cb05048dfb822e95d44e52dd85b830c750411e2c>
- 仓库 README：<https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/README.md>
- 历史状态：<https://github.com/zhouyangming2025-cell/wam-research/blob/cb05048dfb822e95d44e52dd85b830c750411e2c/state/NEXT_TASK.md>

**本审计范围：仓库现有资产和文档治理，非全面新文献普查。**
