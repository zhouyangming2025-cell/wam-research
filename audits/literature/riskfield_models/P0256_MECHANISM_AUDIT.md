# P0256｜Predictive Risk-Aware Reinforcement Learning for Autonomous Vehicles Using Safety Potential



证据：本会话 all_md.zip 内原始 MinerU Markdown，SHA-256：86461e5ad08d34d22bcf73e86858c9414c33f9c39dc7e8ea8a050dc1e8da5312。已核全部展示公式在 MD 内的位置与内容，未经 PDF 视觉/代码验收；以下是重点公式链，全部原样 LaTeX 在独立交付 ZIP。



**定义对象**：ego 局部规划路线与 NPC 规则预测路线均被转为沿路径定向的宽2.8m、长1m多边形单元。安全势是所有空间 cell 交面积的索引衰减和，最后跨 NPC 取 max；并非逐时刻完整车身碰撞概率。

**逐式主链**

- Eq.(1)–(4) L77–95：49维观察状态和 throttle/brake 行动接口；与 SP 场本体区分。

- §2.4.1–2.4.2 L101–112：1m 路径采样、车身前 J_body=5 个单元、规则式 NPC 预测。Eq.(5) L117–119：u_e,i=i/(N_e−1)，NPC u_o,k,j 以 j−J_body 归一。

- Eq.(6) L121–123：w_i=exp(−ηu_e,i)、v_k,j=1（车身）或 exp(−ηu_o,k,j)，η=0.5。

- Eq.(7) L134–136：SP_t=max_k sum_i sum_j min(w_i,v_k,j) Area(p_i ∩ q_k,j)。对单个 NPC 所有 ego 与 NPC 路线 polygon 的**双重求和**，再选最大 NPC。

- Eq.(8) L155–157：r_sp=−λ_sp SP_t−λ_sp,a 1[SP_t>σ_sp] a_t SP_t；制动 a_t<0 可抵消一部分惩罚。Eq.(9)–(11) L165–187：碰撞、目标、速度奖励合成。Eq.(12)–(14) 为 SAC 训练损失；Eq.(15)–(16) 为 distance/TTC 基线奖励。

**时间审计**：SP_t 每个控制时刻重新计算，但单个 Eq.(7) 内没有 t_e(i)=t_o(j) 的相同时刻配对。分别衰减两条路径的前视索引不等于时间同步。错时通过空间交叉点仍可能给正面积风险（DERIVED）。

**性质**：权重无量纲时 SP 单位为 m²；空间 cell 密度和重复重叠可改变总值。矩形是扫掠路线片段而非同一未来时刻两车完整 OBB。NPC 未来按规则车道跟随，并非固定给定的全时序真实未来。

**实验边界**：Table 5 同一训练环境 400 episode 报告 No-SP 碰撞21.75%、SP reward-only 3.00%、state+reward 1.75%，证明该环境的学习效果，不能证明空间势的碰撞概率校准或时间同步。状态 MD_EQUATION_CHAIN_MAPPED_WITH_BLOCKERS。完整22式与上下文见 P0256_FULL_MATH_MODEL_AUDIT.md。
