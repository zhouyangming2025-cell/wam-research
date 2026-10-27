# P0163｜FlowDrive: Energy Flow Field for End-to-End Autonomous Driving

本地风险场 MD 库编号（与 WAM 编号独立）。用户 `all_md.zip`；源 MD SHA-256 `1f4e4e3c3b71ad9c48852c99752f1c457217ffde09b6d7ca243e0bc772a1b7d7`。本卡是 **METHOD_CHAIN_SPOT_AUDIT**（非 PDF 视觉验收或全式穷尽）；完整原始公式链和行号参见本次会话 `BATCH3_MATH_AUDIT.zip`。

### C→B：明确采用风险势场，但非新核
MD Eq.(2) L77–79 将 BEV 障碍物像素中心映射为二维径向 Gaussian：
```latex
U _ {\mathrm{risk}} (u, v) = \sum_ {i} \eta \exp \left(- \frac {\| (u , v) - (u _ {i} , v _ {i}) \| ^ {2}}{2 \sigma^ {2}}\right)\tag{2}
```
Eq.(3) L88–90 车道吸引势：
```latex
U _ {\text { lane }} (u, v) = \frac {1}{2} k _ {\text { lat }} d (u, v) ^ {2} + k _ {\text { lon }} \left(L - s (u, v)\right),\tag{3}
```
学习输出 \(\hat U_{risk},\hat U_{lane}\)=MLP(F_flow) Eq.(4) L96–98，并用于 anchor refinement Eq.(5) L106–108 和扩散规划。

**时间核查：** U_risk 的 u,v 是 BEV 坐标，而扩散模型 t 是去噪时间，不是“未来两车同步时刻”，不能因此把该式称为 3D/4D 风险场。

**核心创新归属**：BEV flow 表征、learnable queries 和 anchor refinement，而非新的 Gaussian 核。适合作为 E2E 中“风险场是辅助先验”的对照，尚不足证明对固定多候选的低中风险量化。
