# P0092｜Extension and Application of Driving Risk Field Model Considering Vehicle Motion Constraints

**证据等级：METHOD_CHAIN_SPOT_AUDIT。** 原式来自用户 `all_md.zip` 中 MinerU Markdown；保留公式、所在行号、源 SHA。不是 PDF 版式复核，也不是全文公式穷尽。局部 `Pxxxx` 不等于仓库 WAM paper ID。

**MinerU 原文 SHA-256：** `a92f4ff6a79b95468935b56da5667826847e8516db75a1a9609516c8b8038b1d`

**公式链：** 车道势 + 根据障碍物尺寸构造的空间椭圆高斯 + 动能/驾驶行为项 + 轨迹动态约束。

原文静障 Eq.(5)，MD L85–L87：

\[E_{R2}=\beta\exp\!\left\{-\frac12\left[\delta_1\frac{(x-x_o)^2}{L^2}+\delta_2\frac{(y-y_o)^2}{W^2}\right]\right\}-E(0).\]

静态源求和 Eq.(9)，L120–L122：\(E_R=E_{R1}+\sum_{i=1}^n E_{R2}^{i}\)。移动体动能 Eq.(10)，L140–L142：

\[E_v=\begin{cases}\tfrac12k_vv^2\cos^2\theta,&\theta\in(-\pi/2,\pi/2),\\0,&\text{otherwise}.\end{cases}\]

行为项 Eq.(11)，L150–L152：\(E_D=K_DE_v\)。

**场源：** 道路/静障/移动体；ego 查询并后接运动约束。**时间：** 动能项是当前速度条件，不能直接当未来同刻交互。**反例：** Eq.(10) 单独不依赖 ego–周车距离，相同速度方位、相距 2m 或 50m 数值相同；不是声称最终多源总场无距离依赖。Eq.(4) 解析中的零/字母下标仍需回 PDF。

更多关联原文公式与上下文：本轮 `BATCH2_MATH_AUDIT.zip`，相同 paper_id 的 `cards/*.md`（此文件只登记已经核对的关键公式，不假装包含全部 57 式）。
