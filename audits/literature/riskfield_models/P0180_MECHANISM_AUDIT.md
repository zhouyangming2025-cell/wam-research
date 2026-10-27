# P0180｜Space Based Longitudinal Car Following Safety Field Model for Vehicles and its Auxiliary Decision-Making and

本地风险场 MD 库编号（与 WAM 编号独立）。来源：用户 `all_md.zip`；原 MD SHA-256 `277b4fc5fc2ad5dc989e7fd202c38f4980c7daecc2163f3a5aad430a0fde8370`。审计级别 **METHOD_CHAIN_SPOT_AUDIT**；PDF 未视觉核验；主文原始公式全量与上下文见本次 `BATCH3_MATH_AUDIT.zip` 的同名 card。

### 数学对象
首先用 ΔV(t) 的积分表示相对间距变化：Eq.(5) MD L107–109，Eq.(7) L121–123；再按前车/后车的相对加速度贡献分配安全域。初始对称条件 Eq. L177–179 为 L_a=L_f=L/2，后在 L201–203 给出非对称动态分配：
```latex
\begin{array}{l} \Delta \mathrm{L} = (\mathrm{L} / 2) \cdot \mathrm{e} ^ {- 1 / \mathrm{v}} \\ \mathrm{L} _ {\mathrm{a}} = (\mathrm{L} / 2) \cdot (1 - \mathrm{e} ^ {- 1 / \mathrm{v}}) \\ \mathrm{L} _ {\mathrm{f}} = (\mathrm{L} / 2) \cdot (1 + \mathrm{e} ^ {- 1 / \mathrm{v}}) \end{array}
```
风险波形在 L324–332。

**DERIVED：** v=0 时 e^{−1/v} 未定义；v→0+ 才有有限右极限，不代表原式自动覆盖停车状态。更多正文数学式仅剩编号，故 **PDF_REQUIRED_HIGH**。当前可以核实“一维跟驰安全域和相对运动贡献”的想法，不能声明原始数学机制已闭合。
