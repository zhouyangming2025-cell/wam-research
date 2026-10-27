# P0143｜Risk Occupancy: A New and Efficient Paradigm through Vehicle-Road-Cloud Collaboration

**证据等级：METHOD_CHAIN_SPOT_AUDIT。** 原式来自用户 `all_md.zip` 中 MinerU Markdown；保留公式、所在行号、源 SHA。不是 PDF 版式复核，也不是全文公式穷尽。局部 `Pxxxx` 不等于仓库 WAM paper ID。

**MinerU 原文 SHA-256：** `050861a0238217cf341b3391ee534c5bd024a802f7f671ba14f71f5cccd00da4`

**机制：** 静态危险物体按距离阈值赋固定权重；动态物体通过 ETA 经验函数打分；投影到道路锚节点、用于 A* 类路径启发式。不要把 4D 命名直接当作未来双方 OBB 同步碰撞概率。

原文 Eq.(1)–(3)，MD L73–L83：

\[ETA=Distance_{so}/Speed,\]

\[Risk_{dyn}=\begin{cases}0.0667 ETA^3-0.3 ETA^2+0.0333 ETA+1,&ETA\le3.0,\\0.5,&ETA>3.0,\end{cases}\]

\[Risk_{sta}=\begin{cases}Constant,&Distance_{so}\le1.0,\\0,&Distance_{so}>1.0.\end{cases}\]

路径代价 Eq.(4)，MD L170–L172：风险权重项 + 节点距终点与自车距终点的比值（完整原式见本轮 57 式 ZIP）。

**源式数学检验：** 左段 \(f(3)=0.0667·27-0.3·9+0.0333·3+1=0.2008\)；3s 右侧为 0.5，存在 **0.2992 数值跳变**。多项式被称为与 ETA 负相关，但在分界整体非连续、非全局单调。\(Speed=0\) 未定义。**解释边界：** 平滑/归一化启发代价不等于经过真实事故统计标定的概率。

更多关联原文公式与上下文：本轮 `BATCH2_MATH_AUDIT.zip`，相同 paper_id 的 `cards/*.md`（此文件只登记已经核对的关键公式，不假装包含全部 57 式）。
