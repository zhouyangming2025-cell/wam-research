# P0096｜Interaction-Aware Motion Planning for Autonomous Vehicles with Multi-Modal Obstacle Uncertainty Predictions

本地风险场 MD 库编号（与 WAM 编号独立）。用户 `all_md.zip`；源 MD SHA-256 `7ed6413a8463e2a412509fa1ce0b49e86b3712252c24af8340f340a427e11ae3`。本卡是 **METHOD_CHAIN_SPOT_AUDIT**（非 PDF 视觉验收或全式穷尽）；完整原始公式链和行号参见本次会话 `BATCH3_MATH_AUDIT.zip`。

### 非势场的成熟数学对照：逐时 GMM 水平集→可避碰车辆占用
原文 Eq.(6) MD L245–247 以预测模态权重 p_m 的二维高斯函数混合得到 f_t^c(x,y)，但**每个高斯都被其最大值归一**，总体不自动满足 PDF 面积积分=1。然后 Eq.(7) MD L256–258：
```latex
\mathcal {D} _ {t} ^ {c} = \left\{(x, y) \mid f _ {t} ^ {c} (x, y) = \varepsilon_ {k} \cdot f _ {t, \max} ^ {c} \right\}\tag{7}
```
再将此轮廓连同内部封成轴对齐盒 O_t^c Eq.(8) L268–270，车辆膨胀：
```latex
\mathcal {O} _ {\mathrm{veh}, t} ^ {c} = \mathcal {O} _ {t} ^ {c} \oplus S _ {\mathrm{veh}}\tag{9a}
```
其中 S_veh 以长宽为界 Eq.(9b) L294–296。原文 L298 明说忽略周车 yaw 并统一车长宽。

**时间：** 周车 t 时刻占用与 ego MPC t 时刻避障约束对应。**风险语义：** ε 是相对峰值阈值，不等于概率置信质量，不是 calibrated P_collision。

**DERIVED：** 如果调高 ε，低概率预测模态可能完全掉出等值集，即便其是现实可达的未来；这是参数控制保守性，并非安全事件概率保证。
