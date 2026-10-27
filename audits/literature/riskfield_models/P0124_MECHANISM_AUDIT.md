# P0124｜Collision Risk Assessment for Intelligent Vehicles Considering Multi-Dimensional Uncertainties

本地风险场 MD 库编号（与 WAM 编号独立）。用户 `all_md.zip`；源 MD SHA-256 `6a873384bc503b7a0e3c5e80d45cca436c8dc992bf7e62ad4123db282396b882`。本卡是 **METHOD_CHAIN_SPOT_AUDIT**（非 PDF 视觉验收或全式穷尽）；完整原始公式链和行号参见本次会话 `BATCH3_MATH_AUDIT.zip`。

### 成熟机制对照：截断正态 + 真实车身几何的事件频率
输入 ego/周车 EKF 状态与协方差，预测各自未来运动分布；源 Eq.(16) L239–241 尝试定义带截断区间的高斯 PDF（**分母有自引用形式，需 PDF 回查**）。算法 1 L251–285 对每个预测时刻 i 的双方车辆几何交集采样：
```text
I_coll^{i,j} = 1[S_v(x_v^{i,j},y_v^{i,j},φ_v^{i,j}) ∩ S_o(x_o^{i,j},y_o^{i,j}) ≠ ∅]
P_coll^i = (1/N_c) Σ_j I_coll^{i,j}
P_coll = max_i P_coll^i
```
此处是**算法逻辑转录（DERIVED，不是原文显示公式）**，源原始全文可在 ZIP card 的公式块 Eq.(17) L297–299 及算法行定位。P_coll^i 是单时刻碰撞样本比例，P_coll 是其峰值。

**严格不等价：** 两个时间窗口独立 P=0.2，则 max=0.2，但任一碰撞为 1−0.8²=0.36；故不要将全程 max 称为 horizon 累积事故概率。

车辆几何使用旋转矩形和包络安全间距，真实位置/朝向协方差源于 EKF；**但其 ego 也按驾驶行为采样，并非固定 ego candidate 版本**。保留为 C 类安全事件基准。
