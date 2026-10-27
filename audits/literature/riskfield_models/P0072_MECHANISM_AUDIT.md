# P0072｜Rationale-aware Autonomous Driving Policy utilizing Safety Force Field implemented on CARLA Simulator

本地风险场 MD 库编号（与 WAM 编号独立）。来源：用户 `all_md.zip`；原 MD SHA-256 `bef241666785bd38b13448e0827d2994bc540ec326c6865f0f929435b744d397`。审计级别 **METHOD_CHAIN_SPOT_AUDIT**；PDF 未视觉核验；主文原始公式全量与上下文见本次 `BATCH3_MATH_AUDIT.zip` 的同名 card。

### SFF 公式语义（Appendix B MD L160–175）
- State x_A(t)：车辆位置、朝向与速度。
- Safety Procedure S_A：控制 policy 家族；Claimed Set C_A(x_A)：对应程序可能产生的轨迹集合。
- 两车的安全潜势 ρ_AB：claimed sets 交叠的**非负度量**，无交叠为 0；安全力 F_AB=−∂ρ_AB/∂x_A。该 PDF 转写 MD 对上述仅保留行内表达与文字，没有整块原始 LaTeX 方程，**这里不重构 NVIDIA 原文 SFF 公式**。

**研究贡献：** CARLA 中监督学习 claimed-set predictor，并尝试把预测集合的 safety potential 用于策略，实现上的来源和形式来自已有 NVIDIA SFF。

**理论边界：** SFF 的安全性依赖安全程序和可信的 claimed set 覆盖；预测误差可能使理论保证失效。属于控制安全机制对照，不是 2D Gaussian 场。
