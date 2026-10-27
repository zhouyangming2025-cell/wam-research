# P0091｜Considering Human Factors in Risk Maps for Robust and Foresighted Driver Warning

**证据等级：METHOD_CHAIN_SPOT_AUDIT。** 原式来自用户 `all_md.zip` 中 MinerU Markdown；保留公式、所在行号、源 SHA。不是 PDF 版式复核，也不是全文公式穷尽。局部 `Pxxxx` 不等于仓库 WAM paper ID。

**MinerU 原文 SHA-256：** `7e000595f2ae769d86178e87f61d3f0958ad4a19c99faffeead5d821e26a9bbb`

**机制原创位置：** 改造驾驶员对外部风险的*认知输入*，不是重新定义风险场核。分别构造注意失误、速度估计误差和路径推断错误，形成 perceived vs objective Risk Map。

原文 Eq.(2)，MD L52–L54：\(v_{\rm per}=v_{\rm obj}+\mathrm{FE}\,v_{\rm off}\)，其中 FE ∈[−1,1]；Eq.(3)，L60–L62：

\[\boldsymbol p_{\rm per}=\begin{cases}\boldsymbol p_{\rm obj},&\mathrm{IE}\in[0,0.5),\\\boldsymbol p_{\rm pred},&\mathrm{IE}\in[0.5,1].\end{cases}\]

采样速度的规划接口 MD L89–L95：\(C(v^h)=R(v^h)-U(v^h)+O(v^h)\)，选 \(v_{\rm tar}=\arg\min_h C(v^h)\)。

**ego/周车：** ego 驾驶员错误观测周车状态/路径；预警比较主观风险与客观风险。**时间：** 预测路径影响主观地图，但该方法段未给出原创同步时空风险核。**反例：** 物理状态相同时，是否注意到周车可改变感知风险与警报，不改变物理碰撞概率。类别为 B（应用与认知风险建模），不可按风险场原创 A 统计。

更多关联原文公式与上下文：本轮 `BATCH2_MATH_AUDIT.zip`，相同 paper_id 的 `cards/*.md`（此文件只登记已经核对的关键公式，不假装包含全部 57 式）。
