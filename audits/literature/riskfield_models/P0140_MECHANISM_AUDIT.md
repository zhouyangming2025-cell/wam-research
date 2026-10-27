# P0140｜Risk Assessment of Roundabout Scenarios in Virtual Testing Based on an Improved Driving Safety Field

**证据等级：METHOD_CHAIN_SPOT_AUDIT。** 原式来自用户 `all_md.zip` 中 MinerU Markdown；保留公式、所在行号、源 SHA。不是 PDF 版式复核，也不是全文公式穷尽。局部 `Pxxxx` 不等于仓库 WAM paper ID。

**MinerU 原文 SHA-256：** `fb28a96614bd9796054c97c129722ba2a781b776a82a131e50c52775da2769c9`

**机制：** 环岛坐标旋转 + 以主车长宽归一的伪距离 + 速度/车体面积/转向偏差构成源强度 Q + 类库仑反距离风险势；随后 DENCLUE 聚集高势区域，评价车群风险。

原文伪距离 Eq.(3)，MD L101–L103：

\[|d'|=\sqrt{\delta_1\left(\frac{x_e^*-x_o^*}{l_e}\right)^2+\delta_2\left(\frac{y_e^*-y_o^*}{w_e}\right)^2}.\]

原文 Eq.(4)，L111–L113：

\[Q=(k_\alpha|\alpha_e|+k_vv_e+k_{se}l_ew_e)T_e.\]

互动场强 Eq.(5)，L122–L124：\(E_{coll}=k_wQ/(|d'|^2)\,(d'/|d'|)\)；对应势 Eq.(9)，L178–L180：\(V_{coll}=k_wQ/d'\)。群体风险 Eq.(11)，L214–L216：\(R_{cs}=\phi_{max}S\)。

**时间：** 按帧更新车辆状态的二维场，不是未来 ego 候选/周车的逐时 OBB 接触积分。**数值问题：** \(d'=0\) 使场强奇异；Eq.(1) 的 \(x_l/|x_l|\) 在 0 不定义。**MD 解析缺陷：** Eq.(12) 仅两个空求和符号，无法复原完整公式，PDF_REQUIRED。Eq.(4) 将源量 Q 赋予下标 e，源/受体角色需核原文图表。

更多关联原文公式与上下文：本轮 `BATCH2_MATH_AUDIT.zip`，相同 paper_id 的 `cards/*.md`（此文件只登记已经核对的关键公式，不假装包含全部 57 式）。
