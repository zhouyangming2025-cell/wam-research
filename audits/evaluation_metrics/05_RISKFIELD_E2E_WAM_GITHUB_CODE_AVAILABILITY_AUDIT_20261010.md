# 风险场 × E2E/WAM｜GitHub 开源实现与复用价值审计（2026-10-10）

> **状态：REPOSITORY-AND-SOURCE-PATH-VERIFIED / RUNTIME-UNTESTED。**  
> 研究分支：`codex/evaluation-metrics-baseline-audit-20261010`；在 [风险场评价指标专项](04_RISKFIELD_E2E_WAM_METRIC_SPECIAL_STUDY_20261010.md) 之下。  
> **此次只读审计第三方 GitHub 仓库实际文件树及精选源码，未 git clone、安装依赖、执行测试、下载 checkpoint 或集成 NAVSIM/WAM。** “有源码”不等于“论文端到端复现成功”，也不等于“已发布模型权重”。  
> 目的：优先寻找**确实可复用的风险场/风险评价模块**，不是只收集论文 README 的 Code 链接。因仓库不断更新，结果只代表本日观察状态。

## 1. 结果总览：论文相近程度与代码可用性必须分开

| 优先级 | 仓库 / 来源 | 核查到的实际状态 | 与本研究的关系 | 重要限制 |
|---|---|---|---|---|
| **P0 / 指标研究首选** | [PeterWANGHK/Benchmark-RiskField](https://github.com/PeterWANGHK/Benchmark-RiskField) | **有指标实现代码**，含 `metrics_evaluation/risk_field_metrics.py`、`behavioral_alignment_metrics.py`、`unified_metrics_integration.py`。约 68 个 blob | 多类风险场 GVF/EDRF/APF/ADA 的**场平滑、边界、遮挡和驾驶行为对齐评价**；有 `--demo` 描述 | **并非 NAVSIM 官方 benchmark 或自车轨迹 PDMS 替代评分器**；偏重 exiD 高速交互；未见根许可证、依赖清单或测试；不得宣称一键复现 |
| **P0 / 风险场 + 评价代码首选** | [SAS-HKU/DREAM](https://github.com/SAS-HKU/DREAM) | **大规模真实代码**，风险场 `src/dream_limo/dream_limo/core/risk_field.py`，评价 `src/evaluation/` 和 `src/Carla/physical_safety_metrics.py`，有 test 文件和依赖 | **PDE risk field、footprint-aware safety metrics、二维 TTC、clearance、风险源消融、paired scenarios**；部分实现有完整测试入口 | 主要是传统/混合规划与 CARLA、机器人 LIMO，不是现成 WAM 或 NAVSIM 插件；实验数据与依赖待核 |
| **P1 / PDE 场表示** | [SAS-HKU/DRIFT](https://github.com/SAS-HKU/DRIFT) | `src/pde_solver.py`、`src/drift_pde_visualization.py`、`src/test_pde_fixes.py` 等 7 个 Python 文件（24 blobs 总量） | 显式车辆高斯风险源、遮挡源、汇入风险源、对流扩散/电报方程；可借鉴场随时间传播的实现 | **源码可读但不宜断言可直接运行**：`pde_solver.py` 引用 `from config import Config`，当前主分支树未发现 `config.py`；README clone 路径亦指向另一账号；根未见许可证 |
| **P1 / PyTorch Gaussian 场** | [gisgrid/RESPOND](https://github.com/gisgrid/RESPOND) | `respond/risk_pattern/risk.py`、`risk_torch.py`、`risk_calculator.py` 等真实实现，`run_highD_experiment.sh`；65 个 blob | **连续 Driver Risk Field→5×3 风险模式→LLM agent 决策**。尤其是 Torch 批量高斯计算与 overlap/risk 值，可当评价函数借鉴 | README 仍提示完整版本后续发布；外部 highway-env/LLM 依赖及数据路径需核；**不是端到端 WAM 模型，也没有证明可直接接 NAVSIM** |
| **P2 / 传统场模型** | [Dispacher/driving-risk-field-01](https://github.com/Dispacher/driving-risk-field-01) | `src/model/car_risk_model.cpp`、`road_risk_model.cpp`、MATLAB 风险场脚本，34 个 blobs | 车辆、行人、道路风险的手工数学实现，适合对照已有 Gaussian 脚本 | README 简短，无明显自动化验证/依赖文档及许可证；移植 Python 有工程成本 |
| **P2 / 标注与风险场外部验证** | [benmagnifico/K-Risk](https://github.com/benmagnifico/K-Risk) | 数据提取/风险事件筛选/标注脚本；数据单独发布 [Figshare](https://doi.org/10.6084/m9.figshare.32896772) | 以 DRF+机动阈值+短时冲突过滤事件，适合做危险场景/外部风险分级测试 | **不是 NAVSIM 评分器**；数据底座与 NAVSIM/OpenScene 不同；是否迁移需核对字段、标签质量与授权 |
| **P3 / 理论算法参考** | [jasour/Risk-Contours](https://github.com/jasour/Risk-Contours)、[jasour/Non-Gaussian_Risk-Bounded_TrajOpt](https://github.com/jasour/Non-Gaussian_Risk-Bounded_TrajOpt) | 风险轮廓、概率约束/非高斯风险有公式和示例源码（语言/环境需查） | 若研究概率风险、机会约束和尾部风险，可借鉴风险对象定义 | 是**传统随机规划**理论，不是 E2E/WAM 现成训练、评分实现 |

## 2. 最相关 E2E/WAM 原论文：项目存在≠代码开放

| 论文 / 已知入口 | 本次所见仓库状态 | 执行判断 |
|---|---|---|
| **FlowDrive**，[AstrixDrive/FlowDrive](https://github.com/AstrixDrive/FlowDrive) | 核对 `main` 完整树仅 **6 个 blob**：LICENSE、README、assets/docs 等，**无 .py 训练/推理/评分核心代码**。README 仍写 code/models coming soon。分支列表目前只有 `main`；对应 [Hugging Face model card](https://huggingface.co/AstrixDrive/Flowdrive) 不是已证实的可加载 checkpoint | **PAPER+REPO-PLACEHOLDER**。可精读机制，暂不可按官方源码复现。 |
| **READ**，[论文](https://arxiv.org/abs/2609.12371) | 论文和相关网络检索均未定位到**经确认的官方 GitHub 实现**；CatalyzeX 仍显示 Request Code | **OFFICIAL-CODE-NOT-CONFIRMED**。不是“完全无代码存在”的证明。 |
| **DRiF**，[论文](https://arxiv.org/abs/2609.10377) | 摘要称数据和代码将公开；未检索到可核验的官方 GitHub 实现 | **OFFICIAL-CODE-NOT-CONFIRMED**。注意名称 **DRiF ≠ DRIFT**：后者是 SAS-HKU 的另一项 PDE 风险传播研究。 |
| **RiskMap（2024）**，[原文](https://arxiv.org/abs/2406.04451) | 作者[公开论文列表](https://xinren.website/publications/)的 Code 链接指向 `Rex-sys-hk/Velocity-Field/tree/recover`；GitHub 工具当前访问该仓库返回 404 | **CODE-LINK-NOT-ACCESSIBLE**；不得说 RiskMap 官方实现已核实可用；链接可能变更或不可见。 |
| **RiskMM**，[论文](https://arxiv.org/abs/2508.07686) | 本次未确认官方可执行代码；第三方相关列表曾标记 code 未发布 | **OFFICIAL-CODE-NOT-CONFIRMED**。不宜据非官方列表断言永远不开源。 |

## 3. 对 P0 仓库源码的具体核查（避免只看 README）

### 3.1 Benchmark-RiskField

- [field metrics](https://github.com/PeterWANGHK/Benchmark-RiskField/blob/main/metrics_evaluation/risk_field_metrics.py)：`SmoothnessAnalyzer`、`BoundaryAnalyzer`、`OcclusionAnalyzer`；能计算梯度/平滑、阈值区域边界、遮挡风险低估等**场本身的质量**。
- [behavioral alignment](https://github.com/PeterWANGHK/Benchmark-RiskField/blob/main/metrics_evaluation/behavioral_alignment_metrics.py)：`SpatialAlignmentAnalyzer`、`TemporalCoherenceAnalyzer`、`BehavioralValidityAnalyzer`、`DecisionSensitivityAnalyzer`；强调风险场阈值/梯度变化与真实驾驶操作时刻/空间是否一致。
- [unified metrics](https://github.com/PeterWANGHK/Benchmark-RiskField/blob/main/metrics_evaluation/unified_metrics_integration.py)：`FieldMethod` = GVF、EDRF、ADA、APF，`UnifiedRiskFieldEvaluator`；头部提供 `--demo` 和真实 `--data_dir` 用法。**代码存在不代表命令本次实际测试通过。**
- **科学边界：风险场 smoothness 高不是规划更安全；场结构与人类驾驶反应对齐也不是碰撞概率经过校准。** 这是 G1（场验证）和 G2（轨迹评分）之间的好对照，但不是原封不动复制到 NAVSIM 的新指标。

### 3.2 DREAM

- [核心风险场](https://github.com/SAS-HKU/DREAM/blob/main/src/dream_limo/dream_limo/core/risk_field.py)：类 `DREAMRiskField` 包含 `compute_sources`、`step`、`risk_at`、`risk_gradient_at`、`lane_change_risk`，记录计算时延与 PDE 数值稳定性等。
- [物理安全指标](https://github.com/SAS-HKU/DREAM/blob/main/src/Carla/physical_safety_metrics.py)：`signed_oriented_box_clearance`、`constant_velocity_ttc`、`evaluate_swept_pair_safety`、`summarize_episode_safety`；以**车辆旋转矩形 footprint + 二维相对速度**替代简单中心距/纵向 TTC。包括连续时间 swept 检查的近似边界。
- [paired evaluation 指南](https://github.com/SAS-HKU/DREAM/blob/main/src/evaluation/README.md)：matched scenario、component/channel ablations、配对随机化/自助法及多重比较调整，且源码树存在对应 runner/metric/tests。**可为我们未来设计 risk metric 的有效性测试提供模板**；目前未证明可直接运行或移植到 NAVSIM。
- 仓库根含 LICENSE 和依赖/单元测试，相较只有论文页的项目更适合实作试验。

### 3.3 DRIFT、RESPOND 与传统场实现

- [DRIFT PDE 核心](https://github.com/SAS-HKU/DRIFT/blob/main/src/pde_solver.py)：`compute_Q_vehicle` 的车辆源是相对速度加权的各向异性高斯，还含遮挡/汇入源和 PDE；不是 READ、DRiF 的代码替代品。
- [RESPOND DRF Torch 代码](https://github.com/gisgrid/RESPOND/blob/main/respond/risk_pattern/risk_torch.py)、[风险计算器](https://github.com/gisgrid/RESPOND/blob/main/respond/risk_pattern/risk_calculator.py)：提供 Tensor 化复杂 Gaussian、risks/overlap，属于更容易从 Python/PyTorch 迁移到自己的 scorer 的代码素材。
- [传统场 C++/MATLAB](https://github.com/Dispacher/driving-risk-field-01)：适合核对车/路风险函数，但缺现成 NAVSIM 集成层和完善文档。

## 4. 能否直接用于 WAM / NAVSIM 的结论

**本轮没有发现“官方可运行 READ/DRiF/FlowDrive WAM 模型 + 风险场 + 评测环境的一体化开源包”。**

能够做的是**复用风险场评价素材**，自己适配统一轨迹/场景接口：

`NAVSIM output (ego τ, map, tracked-agent states) → time-aligned field inputs → sampled risk along τ → risk peak/integral/exposure → compare with unchanged official PDMS`

建议第一步只做静态代码接口检查：
1. **DREAM** 的 footprint/TTC/episode risk 和 paired evaluation，理解基础验证；
2. **Benchmark-RiskField** 的 field/behavioral quality metrics，判断哪些指标有新增语义；
3. **RESPOND** 的 PyTorch risk functions，确认 GPU 批量处理候选的可移植性；
4. 可选 **DRIFT** PDE 动态风险扩散；它更复杂，不应预设比解析高斯场在 NAVSIM 更合理。

**尚未执行**：安装项目、单元测试、许可确认/源代码拷贝、NAVSIM 接口实现、实际轨迹重评分、模型训练、跨模型结果。对无 LICENSE 仓库先做代码阅读和思想研究，**不能默认可复制、分发或商业复用源代码**。

## 5. 下一步操作与失败条件

- **源码首轮不需下载整库**：先核对 `DREAM src/Carla/physical_safety_metrics.py` 的输入输出与已有 NAVSIM states 能否对齐；再看 `Benchmark-RiskField` 中哪些 metrics 是可转成**trajectory-level**量的，避免场评分/轨迹评分混淆。
- **下一阶段本地最小可运行实验**（尚未授权/执行）：可选 Python 小型 toy 场景对比 Gaussian / PDE / footprint-aware TTC，保存可重复 seed，先评价是否与物理危险方向一致，再接 NAVSIM.
- **样本/协议风险**：DRIFT 缺 `config.py`、多个仓库依赖外部 exiD/HighD/CARLA、无训练 checkpoint、不少无根许可证；全部需在真正引入源码前解决。
- **分支纪律**：持续沿用 `codex/evaluation-metrics-baseline-audit-20261010`，不创建额外分支、不修改主分支；该记录与 [04 专项研究](04_RISKFIELD_E2E_WAM_METRIC_SPECIAL_STUDY_20261010.md) 互补而不是取代。

**阶段最终判断：有真正有价值的开源风险场/评价源码，但目前能确认的主要是“传统/混合规划、风险场分析和评测模块”；最贴近 WAM 的 READ/DRiF/FlowDrive 官方完整实现尚不能依赖。**
