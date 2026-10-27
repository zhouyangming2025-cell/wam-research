# P0046｜A NOVEL ROAD USER SAFETY FIELD THEORY FOR TRAFFIC SAFETY ASSESSMENT APPLYING VIDEO ANALYTICS

本地风险场 MD 库编号（与 WAM 编号独立）。来源：用户 `all_md.zip`；原 MD SHA-256 `99fa4e1eb5091f057aa8551c94bf67510e70177c13ae27ae86db8f37d1998448`。审计级别 **METHOD_CHAIN_SPOT_AUDIT**；PDF 未视觉核验；主文原始公式全量与上下文见本次 `BATCH3_MATH_AUDIT.zip` 的同名 card。

### 物理含义与原式
Road User Safety Field 理论，Eq.(3.3) MD L855–857 以速度、风险潜势 q、环境 ε_R、距离 d 构造场；Eq.(3.4) MD L863–865 将第二主体 q₂ 引入 Risk Force，使用相对速度及 d+d_crash：
```latex
| F _ {c o l l} | = \big | E _ {c o l l, 1} \big | q _ {2} \propto \frac {v _ {r} \cos (\theta - K \alpha_ {r , 1})}{\epsilon_ {R}} \frac {q _ {1} q _ {2}}{d + d _ {c r a s h}}\tag{3.4),}
```
Eq.(4.2) L958–960 的风险潜势原式：
```latex
q = \left(e ^ {\left(\frac {\beta_ {r} T _ {r}}{\beta_ {v} b _ {m a x}}\right)}\right) ^ {- \xi}\tag{4.2),}
```
Eq.(4.3) L966–968 定义环境 ε_R；完整 rear-end Eq.(4.17),(4.18) 在 MD L1185–1193。风险强度和后果严重度 F_sev (Eq3.5) 分开建模，再通过极值方法关联事故频数（Chapter8），**不能将 F_coll 直接写成校准事故概率**。

**DERIVED：** 若 \(\xi,\beta_r,\beta_v,b_{max}>0\)，\(\partial q/\partial T_r<0\)，与原文“更长反应时间→更高风险势”的散文描述相反；最终符号取决于经验参数标定，不宜在未确认参数正负时下结论。实际车辆几何和未来同步碰撞判据没有被该静态势本体保证。
