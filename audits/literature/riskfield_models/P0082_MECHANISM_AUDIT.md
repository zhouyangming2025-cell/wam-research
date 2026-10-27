# P0082｜A Dynamic Path-Planning Method for Obstacle Avoidance Based on the Driving Safety Field

**证据等级：METHOD_CHAIN_SPOT_AUDIT。** 原式来自用户 `all_md.zip` 中 MinerU Markdown；保留公式、所在行号、源 SHA。不是 PDF 版式复核，也不是全文公式穷尽。局部 `Pxxxx` 不等于仓库 WAM paper ID。

**MinerU 原文 SHA-256：** `dab12a2166c1958a2a421af712ca2af07386ead40ffa2cb22f87acd077220bec`

**场源与受体：** 车道、静态/动态障碍产生虚拟场强，自车规划质心读取并由虚拟力更新轨迹；另以覆盖车身的圆做碰撞检测。

原文动态障碍场 Eq.(5)，MD L108–L110：

\[\boldsymbol{E}_{\mathrm{V},cj}=\frac{K R_c M_c}{|\boldsymbol r_{cj}|^{k_2}}\frac{\boldsymbol r_{cj}}{|\boldsymbol r_{cj}|}\exp(k_3 v_c\cos\theta_c).\]

静态障碍 Eq.(4)，L91–L93 为相近的距离幂衰减、无指数速度因子。ego 受场转换 Eq.(9)，L150–L152：\(\boldsymbol F=\boldsymbol E M_j R_j\)。规划状态更新与覆盖圆碰撞约束在 L225–L248。

**时间：** 基础场为当前状态参数化的二维函数；按规划步迭代 ≠ 给定双方全部未来的同步 OBB 查询。**数学边界：** 场用质心距离，零距离有奇异性；L112 原文距离向量第二分量为 `X_j-Y_c`，和二维位移定义冲突，须核原 PDF（不可私自改式）。车辆几何检查是另一模块。

更多关联原文公式与上下文：本轮 `BATCH2_MATH_AUDIT.zip`，相同 paper_id 的 `cards/*.md`（此文件只登记已经核对的关键公式，不假装包含全部 57 式）。
