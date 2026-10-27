# P0103｜Occlusion-Aware Path Planning for Collision Avoidance: Leveraging Potential Field Method with Responsibility

本地风险场 MD 库编号（与 WAM 编号独立）。用户 `all_md.zip`；源 MD SHA-256 `381b8e49919827771c50a5253a1ec2a7bfa7bcafe3ffd5b23b26345b59bb23b1`。本卡是 **METHOD_CHAIN_SPOT_AUDIT**（非 PDF 视觉验收或全式穷尽）；完整原始公式链和行号参见本次会话 `BATCH3_MATH_AUDIT.zip`。

### 机制：RSS 距离尺度 + 高斯型 APF + 遮挡时调整方向力
来源 MD Eq.(4) L60–62 以纵横差值及 RSS 安全距离参数构造障碍势：
```latex
U _ {O B} ^ {j} = \frac {\left| e ^ {- \sigma_ {y} ^ {j} (X - X _ {O B} ^ {j}) ^ {2} - \sigma_ {x} ^ {j} (Y - Y _ {O B} ^ {j}) ^ {2}} - \epsilon \right|}{1 - \epsilon}\tag{4}
```
RSS 纵横距离/响应时间系数见 MD L66–70；总场 U_N 和虚拟力 −∇U_N Eq.(5) L77–85；遮挡引入 α_1,α_2 的纵横力梯度 Eq.(7),(8) L106–118；转期望速度/加速度 Eq.(9),(10) L122–143。

**语义：** ego 向周车/道路势受场；遮挡处增加对于未能早期感知物体的控制补偿。不是事故概率。

**DERIVED / PDF_REQUIRED：** Eq.(4) 下标 σ_x 与 Y²、σ_y 与 X²交叉，Eq.(6) RSS 制动距离项存在量纲疑点；不经 PDF 核查不应直接运行此式。此创新主要在感知遮挡和控制力修正，并非完整同步未来两车 OBB 判据。
