# P0237｜Conditional Artificial Potential Field-Based Autonomous Vehicle Safety Control with Interference of Lane Changing

本地风险场 MD 库编号（与 WAM 编号独立）。用户 `all_md.zip`；源 MD SHA-256 `f33f77bd480659656f48aeb69c56fac7a466658afaf07a12a7ae09981523591d`。本卡是 **METHOD_CHAIN_SPOT_AUDIT**（非 PDF 视觉验收或全式穷尽）；完整原始公式链和行号参见本次会话 `BATCH3_MATH_AUDIT.zip`。

### 条件激活的一维安全势
先预测邻车变道意图，满足触发条件后使用纵向安全距离 Eq.(2) L186–188：
```latex
\rho_ {o r} = l = d _ {0} + h v _ {t}\tag{2}
```
在安全距离以内启用排斥势 Eq.(3) L192–194：
```latex
U _ {r e p} = \frac {1}{2} \eta (\frac {1}{\rho_ {r}} - \frac {1}{(d _ {0} + h v _ {t})}) ^ {2}\tag{3}
```
其梯度力 Eq.(4) L196–198；距离较大时切到吸引势 Eq.(5),(6) L204–210。

**数学信息：** 纵向时距 h 与速度 v_t 增加安全阈值；这是条件控制而不是新事故概率。
**DERIVED：** 排斥分支在 ρ_r=l 时趋于0，但未显示吸引分支中心处恰在此点，整体切换光滑性未被证明。Eq.(6) 写 +∇U_att，其符号需根据纵向控制正方向查证。
