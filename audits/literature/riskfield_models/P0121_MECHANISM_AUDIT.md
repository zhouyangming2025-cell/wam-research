# P0121｜An Integrating Comprehensive Trajectory Prediction with Risk Potential Field Method for Autonomous Driving

> **本文件由“4 个公式的 spot 摘录”升级为“全部 20 个展示公式的源 MD 机制链核对”。** 完整 20 个原样 LaTeX 块及单式解释另保留于本次会话文件 `P0121_FULL_MATH_MODEL_AUDIT.md`（19KB；尚未原样镜像到 GitHub）。本文件保留可供继续研究的公式输入输出、数学关系与明确阻塞。**审计状态：`MD_FORMULA_CHAIN_MAPPED_WITH_BLOCKERS`；不是 PDF_VISUAL_VERIFIED / FULL_FORMULA_VERIFIED。**

源：用户 `all_md.zip/all_md/2024_An_Integrating_Comprehensive_Trajectory_Prediction_with_Risk_Potential_Field_Method_for_Autonom_dbb70ca8.md`。
原文 SHA-256：`b30ce23e449f1a40ae32dd840685a583cf3e6de5e1624e06b81f5ed37ee9f023`；源 330 行；**20 个展示式全部回放吻合**。原 ZIP 缺图片，PDF 页码不作猜测。作者：Kailu Wu、Xing Liu、Feiyu Bian、Yizhai Zhang、Panfeng Huang；文件名标 2024，DOI/正式出版仍待核。

## 1. 不是摘要：从输入到轨迹评价的完整公式链

| 运算节点 | 原文 Eq.／MD 行号 | 本式在模型中的真实作用 |
|---|---|---|
| 预测模态与概率 | (1) L65–67；未编号的第2展示式 L69–71 | 从车道目标区域、目标/周车历史和 GRU/Attention 输出每个未来路径 `τ_j` 与权重 `p_j`；源缺显式 softmax/归一化式 |
| 预测器监督 | (3)(4)(5) L79–93 | 轨迹回归损失、GT 对应模态负对数似然、加权训练损失；**不是风险场本体** |
| ego 动力学 | (6) L106–108 | 自车运动学单轨模型；控制符号 `dot a` / `a` 不一致 |
| 单周车风险场 | **(7) L114–116** | 在**未来时刻 t** 以预测多模态中心建立旋转局部坐标的各向异性指数平方势，按 p_j 求和 |
| 局部坐标变换 | **(8) L120–122** | 用预测车朝向，将 `(x−x_j,y−y_j)` 转到车辆局部纵横分量；φ_j^t 下标未写出 |
| 多周车聚合 | **(9) L126–128** | 叠加所有周车的空间势，再乘未来折扣 γ^t；是线性强度和，不是联合事件概率 |
| 参考线几何与 MPCC 跟踪 | (10)–(14) L139–164 | 参考线切向、contouring/lag error 及参考线进度；(13) 的三角括号疑似转写损坏 |
| 轨迹规划目标 | **(15) L169–171** | 每个预测步的风险代价与路径跟踪、控制平滑和进度奖励联合优化；时间索引和 γ 双重出现需要核 |
| 优化约束 | (16)–(20) L173–190 | 初始条件、离散车辆动力学、参考进度与状态/控制范围；**无硬碰撞不等式** |

## 2. 保留原文关键场公式与逐项变量

Eq.(7)：
```latex
\Theta (x, y) _ {i} ^ {t} = \sum_ {j = 0} ^ {k} p _ {j} e ^ {- (\frac {\Delta x _ {j} ^ {2}}{a ^ {2}} + \frac {\Delta y _ {j} ^ {2}}{b ^ {2}})}\tag{7}
```

Eq.(8)：
```latex
\left[ \begin{array}{c} \Delta x _ {j} \\ \Delta y _ {j} \end{array} \right] = \left[ \begin{array}{c c} \cos \varphi & \sin \varphi \\ - \sin \varphi & \cos \varphi \end{array} \right] \left[ \begin{array}{c} x - x _ {j} \\ y - y _ {j} \end{array} \right]\tag{8}
```

Eq.(9)：
```latex
\Theta (x, y) ^ {t} = \gamma^ {t} \sum_ {i = 1} ^ {m} \Theta (x, y) _ {i} ^ {t}\tag{9}
```

Eq.(15) 在源 MD L169–171 的关键项为 `q_r γ^k Θ(x_k)^t`，完整原样式包含路径偏差、控制惩罚和进度奖励，但 MinerU 重复生成 `\tag{1}\tag{15}`。在找到 PDF 前保持原式，不私自更正为 Θ^k 或删去一个 γ。

**变量和对象：** `i` 为周车，`m` 是周车数；`j` 为该车预测模态；`p_j` 为模态权重，源未直接展示其规范化操作；`(x,y)` 是被查询的 ego 空间位置；`(x_j,y_j,φ)` 是预测模态的周车中心和朝向；`a,b` 为纵横高斯形状尺度而非经过 OBB 认证的实际车身轮廓或估计协方差；`γ` 为未来折扣；`t` 是周车未来预测时刻，`k` 在不同公式里重载为模态上界与 ego 控制步；`q_r` 为规划中的风险权重。ego 状态 `(x,y,φ,δ,v)` 属轨迹控制，不是周车风险源。

**风险输出语义：** 位置到预测周车中心在局部坐标中的高斯型非负势。不是几何净距、碰撞指示函数或归一化事故概率。多模态内部是求和、不同周车之间是求和，**没有**对周车多主体联合预测模式相关性的显式联合分布操作。

## 3. 时间与真实几何（不得用‘考虑时空’四字替代）

Eq.(7) 对每个未来时刻 `t` 建立一张 Θ_i^t(x,y)。论文 §IV 和 Fig.1 文字确实声称规划每个未来时刻的风险场；Eq.(15) 却写 `Θ(x_k)^t`，**在用户给出的转写版中，不能严谨证明 t 与 ego k 实际实现按同一时刻配对**。这点应该回原 PDF 或实现查，而不是先断言已同步或未同步。

风险几何对 ego 使用位置点查询、对周车使用中心加朝向旋转；没有直接把两个时刻 t 的整车 OBB 作相交或净距检查。预测历史可含速度/加速度，但 Eq.(7) 并没有单独出现相对接近速度、双方响应时间/制动能力等变量。

## 4. 数学推导与反例（DERIVED；不是作者原文声称）

1. 当 `a=b`，单模态核对中心等距的两个位置给相同数值；实际车辆形状/朝向可能导致净距不同。因此从本式不能推出真实车身安全距离。
2. 即便两个预测模态均与 ego 的 OBB 不接触，它们在 ego 处高斯尾部仍给正势；`Σ p_j exp(−...)` 不是 `P(collision)`，平滑代价与事故事件概率不能互换。
3. **双折扣条件推导：** Eq.(9) 写 `γ^t`，Eq.(15) 也写 `γ^k`。若在实际规划中 t=k，则输入 Eq.(15) 的原式风险项等于 `q_r γ^(2k) Σ_i Θ_i^k(x_k)`；这是代数条件结论，不代表已定位真实代码 bug。
4. **时间错位的判断是条件性的：** 若未来步 k 错取不同时刻 t 的 Θ，会失去同步接近判据；若运行时正确选择 t=k，则该问题不发生。当前仅凭源 MD 为 UNKNOWN。
5. Eq.(16)–(20) 没有写碰撞不等式，风险是 soft planning penalty。其设计在数值上不自动提供任意场景的严格无碰撞保证。

## 5. 原创性与机制去重

- 本文作者声称贡献是 TRTP 预测方式以及把预测结果构成未来风险场后结合 MPCC；**没有证据证明该 Gaussian 核本身为首次提出。**
- 与风险场库 `P0092` 的单车各向异性 Gaussian 在相同坐标和单模态情况下存在特定尺度/幅值重参数化的**局部核同构**。机制表中可标 `SHARED_GAUSSIAN_PRIMITIVE`。
- **不能整篇并入 P0092：** 本文另有预测模态 p_j、未来时刻 t、周车聚合和 ego 预测时域优化等独立输入和计算位置。应标为 `REUSED_PRIMITIVE_WITH_DISTINCT_TIME_INTERFACE`，保留论文身份，但不重复把 Gaussian 核算一个“新物理公式”。

## 6. 影响模型闭合的原始证据缺口

| 原式 | 具体问题 | 状态 |
|---|---|---|
| (2), L69–75 | 概率分数未直接展示 softmax/规范化形式，原文编号游离 | `PDF_OR_CODE_REQUIRED` |
| (3), L79–81 | 原文称 average displacement，式中没有除样本步数；位置/完整状态范围不明 | `PDF_OR_CODE_REQUIRED` |
| (6), L104–108 | 控制输入描述 `dot a`，公式 `a` | `PDF_OR_CODE_REQUIRED` |
| (7), L114–116 | `k` 同时用作模态上界和规划时间步 | `INDEX_COLLISION` |
| (8), L120–122 | 旋转角 `φ` 未明确标 j,t | `YAW_INDEX_AMBIGUITY` |
| (9)+(15) | 折扣 `γ^t` 和 `γ^k`、时间 t/k 对应未说明 | `TIME_ALIGNMENT_BLOCKED` |
| (13), L157–159 | 三角函数括号疑似错乱 | `PDF_VISUAL_REQUIRED` |
| (15), L169–171 | MinerU 保留重复 `\tag{1}\tag{15}` | `PARSE_NOISE` |
| Fig.1/3/4 | 用户 ZIP 无图片 | `FIGURE_NOT_AVAILABLE` |

## 7. 论文实验能证明的范围

Table II (MD L248–256) 两个 CARLA 场景本方法和 GPIR 都报告 0% 碰撞，本方法用时更短；Table III (MD L252–258) CSP+MPCC 的碰撞率 5%，TRTP+MPCC 为 0%。它主要支持本文“预测方法替换”在给定场景中的作用，并不构成高斯核原创性、低中风险语义或事故概率校准的独立验证。

**本轮验收结论：** `SOURCE_MD_ALL_20_EQUATIONS_REPLAYED = YES`；`FULL_RISK_MODEL_SEMANTICS_UNAMBIGUOUS = NO`；`PDF_VERIFIED = NO`。应先核实上述时间映射、Eq.(13) 和预测归一化，再提升状态。完整 20 个原始 LaTeX 块及逐式角色在会话交付 `P0121_FULL_MATH_MODEL_AUDIT.md`，未完整镜像 GitHub。
