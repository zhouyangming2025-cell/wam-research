# P0121｜An Integrating Comprehensive Trajectory Prediction with Risk Potential Field Method for Autonomous Driving

**证据等级：METHOD_CHAIN_SPOT_AUDIT。** 原式来自用户 `all_md.zip` 中 MinerU Markdown；保留公式、所在行号、源 SHA。不是 PDF 版式复核，也不是全文公式穷尽。局部 `Pxxxx` 不等于仓库 WAM paper ID。

**MinerU 原文 SHA-256：** `b30ce23e449f1a40ae32dd840685a583cf3e6de5e1624e06b81f5ed37ee9f023`

**本批与目标最相关的机制：** 周车多模态*逐未来时刻*构建旋转各向异性高斯风险核，ego 的 MPCC 候选按相应时刻查询，和将整段未来压为二维风险带不同。

原文 Eq.(7)，MD L114–L116：

\[\Theta_i^t(x,y)=\sum_{j=0}^{k}p_j\exp\!\left[-\left(\frac{\Delta x_j^2}{a^2}+\frac{\Delta y_j^2}{b^2}\right)\right].\]

\(\Delta x_j,\Delta y_j\) 为将 ego 查询点与第 j 模态预测位置差转至目标车朝向坐标系后的分量，转动矩阵 Eq.(8) 见 L120–L122。周车聚合 Eq.(9)，L126–L128：

\[\Theta^t(x,y)=\gamma^t\sum_{i=1}^{m}\Theta_i^t(x,y).\]

MPCC Eq.(15)，MD L169–L171，将 \(q_r\gamma^k\Theta(\boldsymbol x_k)^t\) 放入预测时域逐步代价。

**核查保留：** 已有 \(\gamma^t\) 和目标中的 \(\gamma^k\)，若索引一致将双重衰减；式(15) 的 \(\Theta(\boldsymbol x_k)^t\) 是否应当对应未来 \(t+k\) 未经源码/原 PDF 校验，标 INDEX_AMBIGUITY。权重 p_j 是模态概率而非输出场为碰撞概率；核对车体 OBB 接触仍属独立问题。

更多关联原文公式与上下文：本轮 `BATCH2_MATH_AUDIT.zip`，相同 paper_id 的 `cards/*.md`（此文件只登记已经核对的关键公式，不假装包含全部 57 式）。
