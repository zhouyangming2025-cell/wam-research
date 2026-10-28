# P0240｜Driving Style Recognition Method Based on Risk Field and Masked Learning Techniques



证据：本会话 all_md.zip 内原始 MinerU Markdown，SHA-256：3d92758f5240d79ef8e3cd0c6132a4882603b5aaf0cea969788dd23fc2581cca。已核全部展示公式在 MD 内的位置与内容，未经 PDF 视觉/代码验收；以下是重点公式链，全部原样 LaTeX 在独立交付 ZIP。



模型角色：每辆周车作场源，二维查询点接收虚拟风险场强矢量；车场 + 道路边界场按时序生成风险图像供 MAE 驾驶风格识别，不是固定 ego 候选风险排序。

**逐式主链**

- Eq.(1) L57–59：引用 Tian 的原始运动风险场 E_i = λ1 M_eq-i exp(λ2 m_j Δv/|k|) exp(−βa cosθ) k/|k|，k 是车心到查询点的空间向量。

- Eq.(2) L67–69：引用 Wu 等高速事故数据的等效质量经验式，含 m_i v_i^6.687 项；Eq.(3) L71–73 将等效质量代入旧风险场；Eq.(4) L77–79 将两指数部分记为 A、B。

- Eq.(5) L85–87：A=c1 sigmoid[−c2(|k|−c_reaction v−v²/(2a_max))]，将反应距离与理想制动距离作为距离阈值，属于本文新增的主要数学结构。

- Eq.(6) L91–93：等效质量 × sigmoid 幅值 × 运动方向指数 × k/|k|；Eq.(7) L99–101：c3 exp[−s²/(2γ²)]，其中 s 是路边线的法向空间距离，非时间。

**关键语义**：c_reaction 是反应时间参数，不意味着建立真实时间维 R(x,y,t)。Eq.(6) 用中心向量，不具备 OBB 全车身接触或同步 ego/周车未来匹配。输出是虚拟势场而非事故概率。

**数学阻塞**：Eq.(1)→Eq.(3) 指数中 m_j 改成 m_i，非纯代数代入；Eq.(1),(3) 的 exp(−β a cosθ) 到 Eq.(6) 变成 exp(+βa cosθ)；a_max 文字称最大加速度，却用于制动距离分母；|k|=0 时方向向量不可定义；L141 的向量模量合成只以文字出现，未给精确算子。

**DERIVED**：在 c1,c2,a_max>0 下 sigmoid 距离单调下降、反应时间上升使风险幅值增加，但这不是模型安全性证明。状态 MD_EQUATION_CHAIN_MAPPED_WITH_BLOCKERS。完整七式和上下文见会话交付 P0240_FULL_MATH_MODEL_AUDIT.md。
