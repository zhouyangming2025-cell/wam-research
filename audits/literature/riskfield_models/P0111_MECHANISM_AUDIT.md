# P0111｜Time-to-Collision-Aware Lane-Change Strategy Based on Potential Field and Cubic Polynomial for Autonomous Vehicles

**证据等级：METHOD_CHAIN_SPOT_AUDIT。** 原式来自用户 `all_md.zip` 中 MinerU Markdown；保留公式、所在行号、源 SHA。不是 PDF 版式复核，也不是全文公式穷尽。局部 `Pxxxx` 不等于仓库 WAM paper ID。

**MinerU 原文 SHA-256：** `82ee31e9cb3bf3f44d59a7b3f94d4e5c5193af37d7beeec101a3699a3f0b2e0b`

**真正作用：** 沿用道路/障碍人工势场，加入纵向停车距离确定高斯范围，以 TTC 来调整多项式换道开始位置，而不是构建校准碰撞概率。

原文障碍势 Eq.(3)，MD L79–L81：

\[P_o=A_{obs}\exp\left[-\frac{C_1}{2}\left(\frac{(X-X_o)^2}{\sigma_x}+\frac{(Y-Y_o)^2}{\sigma_y}-C_2\right)\right].\]

参数 \(C_1,C_2,\sigma_x,\sigma_y,D_{min}\) 及其停车距离/相对速度定义见 MD L85–L89，完整原样多行式保存在本次交付包。纵向 TTC 分段式见 L121–L135；换道起点 Eq.(8) 后附式 L157–L159：

\[X_{start}=X_{obs}-v(TTC+T_{LC}),\quad X_{end}=X_{obs}+\sigma_x.\]

**时空边界：** 以一维纵向 TTC 调时机，不等于在双车任意转向轨迹上逐时检查几何占用。**反例：** 源 Eq.(7) 定义 \(v_{rela}=|v_1-v_2|\) 会把速度差同幅、但一个追近一个远离的情形混合；另外 Eq.(7) 有重复 `\\tag{7}`，且判别根需 PDF 回查。

更多关联原文公式与上下文：本轮 `BATCH2_MATH_AUDIT.zip`，相同 paper_id 的 `cards/*.md`（此文件只登记已经核对的关键公式，不假装包含全部 57 式）。
