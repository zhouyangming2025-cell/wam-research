# P0097｜Learning from Demonstrations of Critical Driving Behaviours Using Driver’s Risk Field

本地风险场 MD 库编号（与 WAM 编号独立）。来源：用户 `all_md.zip`；原 MD SHA-256 `cef61185a6352de8ebff5b688b684bebf6037eda47548eb6e18937449e611e97`。审计级别 **METHOD_CHAIN_SPOT_AUDIT**；PDF 未视觉核验；主文原始公式全量与上下文见本次 `BATCH3_MATH_AUDIT.zip` 的同名 card。

### DRF 在本论文中的角色
原始二维 DRF Gaussian 沿预测路径作为 *behavior policy*；该论文 §3.2 MD L86–88 仅以行内 P_risk(v,δ) 引用已有 DRF，**没有重新提出核的原始数学定义**。作者调节多个周车 agent 的谨慎/激进参数 Φ，寻找诱发交通冲突的联合仿真场景。

Eq.(3),(4) 原式，MD L96–104：
```latex
\Phi^ {*} = \arg \min _ {\Phi} J (\theta , \Phi)  ,\tag{3}
```
```latex
J (\theta , \Phi) = \mathbb {E} _ {s _ {t}, Z _ {t}} \sum_ {t = 0} ^ {T} L 1 (s _ {t}, Z _ {t}) - L _ {a c c i d e n t s}.\tag{4}
```
M 个周车两种策略导致 2^M 个联合参数组合（L106）。**模型属于行为反事实情景生成，不是固定周车未来的候选打分场**；亦未证明新 DRF 空间核性能。
