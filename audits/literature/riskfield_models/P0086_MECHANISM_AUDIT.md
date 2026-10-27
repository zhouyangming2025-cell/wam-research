# P0086｜Anisotropy safety potential field model under intelligent and connected vehicle environment and its application in car-following modeling

**证据等级：METHOD_CHAIN_SPOT_AUDIT。** 原式来自用户 `all_md.zip` 中 MinerU Markdown；保留公式、所在行号、源 SHA。不是 PDF 版式复核，也不是全文公式穷尽。局部 `Pxxxx` 不等于仓库 WAM paper ID。

**MinerU 原文 SHA-256：** `7e90bae3b55f9c295571de21deb08a4906ca3b61e17c8b68eef61def5f8c9011`

**核心创新：** 不同于单纯椭圆高斯，采用前/后分段的速度相关等效距离，以及加速度方向指数项，合成受场者虚拟力。

原文 Eq.(4)，L88–L90：

\[|k|=\begin{cases}\sqrt{[(x-x_0)\delta_1/(\nu_m-|\nu|)]^2+(y-y_0)^4},&x<x_0,\\\sqrt{[(x-x_0)\delta_2/|\nu|]^2+(y-y_0)^4},&x\ge x_0.\end{cases}\]

Eq.(5)，L94–L96：

\[|\boldsymbol E_V|=r_1\varsigma\frac{\exp(r_2 a\cos\theta)}{|k|^2}.\]

Eq.(6)，L107–L109：\(\boldsymbol F_0=\sum\boldsymbol E_V\times|\tau|\)。\(\varsigma\) 是场源车的虚拟惯量，\(\tau\) 是受场车的风险质量；各自受速度及面积/质量近似影响（Eq.(1),(2)）。

**时间：** 速度/加速度修正二维风险强度，非未来同步占用。**可推导边界：** Eq.(4) 在 \(|\nu|=0\) 或 \(|\nu|=\nu_m\) 无一般定义；四次横向项加平方纵向项的尺度/单位需核实，不能把输出当碰撞概率。实验主要用跟驰轨迹误差评估。

更多关联原文公式与上下文：本轮 `BATCH2_MATH_AUDIT.zip`，相同 paper_id 的 `cards/*.md`（此文件只登记已经核对的关键公式，不假装包含全部 57 式）。
