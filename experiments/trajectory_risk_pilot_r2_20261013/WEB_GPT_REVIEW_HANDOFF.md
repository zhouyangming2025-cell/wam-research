# R2 视觉审计交接（给网页版 GPT / 人工验收）

本文件只汇报本轮交付状态与待审清单，不含文献综述，也不对任何风险模型宣布优劣结论。

## 1. 分支、提交与直接可打开的图片索引

| 项目 | 值 |
|---|---|
| 仓库 | `zhouyangming2025-cell/wam-research` |
| 分支 | `experiment/trajectory-risk-pilot-r2-20261013` |
| 审计前提交（上轮） | `21b6ee76456fd54f5930ce9831e9e55849a706d1` |
| **本轮证据提交** | **`1852e7a5c9eb06996ee73f952a18e68aa29a03ef`** |
| 实验目录 | `experiments/trajectory_risk_pilot_r2_20261013/` |

**图片索引（Markdown 内嵌，打开即可逐张看图）：**

- 索引文件：<https://github.com/zhouyangming2025-cell/wam-research/blob/experiment/trajectory-risk-pilot-r2-20261013/experiments/trajectory_risk_pilot_r2_20261013/VISUAL_REVIEW.md>
- 图件目录：<https://github.com/zhouyangming2025-cell/wam-research/tree/experiment/trajectory-risk-pilot-r2-20261013/experiments/trajectory_risk_pilot_r2_20261013/figures>
- 单图直链示例（Actor72 分量图）：
  <https://github.com/zhouyangming2025-cell/wam-research/blob/experiment/trajectory-risk-pilot-r2-20261013/experiments/trajectory_risk_pilot_r2_20261013/figures/v0star_2p5_vs_4p5_components.png>
- 原始字节直链（Base64/raw 读取用）：
  `https://raw.githubusercontent.com/zhouyangming2025-cell/wam-research/experiment/trajectory-risk-pilot-r2-20261013/experiments/trajectory_risk_pilot_r2_20261013/figures/<name>.png`

本轮提交了 9 张精选 PNG + 1 张总览缩略图，单图 80 KB–684 KB（均 < 1 MB），已目视核对比例、车身矩形、速度箭头、时间标注与色标。另有 `SHA256SUMS.txt`（36 条）覆盖全部图件、输入与脚本。

## 2. 复现命令与干净检出结果

```bash
git clone --branch experiment/trajectory-risk-pilot-r2-20261013 \
  https://github.com/zhouyangming2025-cell/wam-research.git
cd wam-research/experiments/trajectory_risk_pilot_r2_20261013
python run_all.py
```

依赖：`numpy pandas matplotlib shapely`。`run_all.py` 现在会先建立 `figures/ results/ data/`，
八个实验脚本跑完后自动执行 `visual_archive.py` 生成图件、`index.html`、缩略图与 SHA256 清单。

**干净检出验证：通过。** 方法：从本地仓库克隆该分支到独立目录，删除全部生成物
（`figures/`、`index.html`、`overview_thumbnail.png`、`SHA256SUMS.txt` 与 5 个结果文件），
再执行 `python run_all.py`：

- 退出码 `0`，8 个脚本 + `visual_archive.py` 全部成功，无缺目录报错；
- 重新生成的 36 项中 **33 项与已提交哈希逐字节一致**（含全部 9 张 PNG 与 1 张缩略图）；
- 仅 3 个数值文件存在**末位浮点表示差异**（`controlled_summary.csv`、
  `sampling_comparison.json`、`v0star_anomaly_attribution.json`）。差异为 numpy/pandas
  版本导致的 float64 repr 末位（如 `1.0649032986221179` ↔ `1.064903298622118`），
  **审计关注的量级与数值不变**（Actor72 Dynamic 均为 `0.45613144079076157/8`，
  几何间隙、门控、径向速度一致）。为保持上轮已审基线不被噪声污染，这 3 个文件保留原提交版本。

## 3. V0* 4.5 秒异常的关键数学证据

数据：INTERACTION EP0 真实记录，Ego #70 与 Actor #72（`V0*`，查询点为 **Ego 中心**，未冻结端口）。

| 量 | t=2.5 s | t=4.5 s |
|---|---:|---:|
| 最近车身间隙 | 1.621 m | 9.297 m |
| Actor72 局部纵向 x | +1.846 m | −14.474 m |
| Actor72 局部横向 y | +4.790 m | +0.940 m |
| σ_lateral | 1.791 m | 1.791 m |
| σ_dynamic_long = 6·\|v_e−v_a\|+0.001 | 8.779 m | **20.281 m** |
| 方向门控 | ≈0 | **0.999999989** |
| Actor72 Dynamic | 0.000663 | **0.456131** |
| Actor72 Total | 0.001384 | **0.461311** |
| 径向距离变化率（正=远离） | −3.742 m/s | **+9.104 m/s** |

- Actor71/73 在 t=4.5 s 的贡献约 `1e-94` / `1e-87`，**Actor72 近乎 100%**，故排除
  「SUM 误加远处对象」与「多 Actor 叠加」。
- Actor72 记录 yaw 与实际速度方向差约 `0.00046 rad`，排除 yaw 数据异常。
- 机制：横向归一化距离变小（0.940 m vs σ_y 1.791 m）＋动态纵向被 σ_v 拉到 20.281 m
  ＋门控饱和到 ≈1，使 `dynamic` 达 0.456；**车身越远、分数越高**。
- 结论边界：这是当前 `V0*` 公式的**数学响应**（可在人工验收中作为「持续主观关注」解释），
  但**不能**据此宣称冻结 V0 存在同样行为——冻结源码 `mcts_planner/risk_field.py`
  仍未获得，`V0*` 未通过源码一致性认证。

## 4. 两种风险场已确认的响应（合理 vs 异常）

**`V0*`（手工端口，未冻结）**

- 合理：随几何接近单调升高；前车急刹、后车加速、路口同刻碰撞分支峰值同步上升。
- 异常：①4.5 s 远离时 Dynamic 反升（见上）；②静止障碍 yaw=90° 时查询点降至 0，
  即对**静态小物体的朝向极度敏感**；③Ego 前缘小物体**车身已重叠（gap=0）**
  而中心点查询仅 `9.15e-52`，单点查询漏检；④同模长对向运动 `|Δspeed|`=0，
  无法表达 20 m/s 的真实闭合速度。

**Wu Eq7-9（单模态，离线 Oracle）**

- 合理：按同一时间采样给出时空连续的风险；错时 2 s 的路口场景给出区别响应。
- 异常：①静止锥桶 yaw=0 时初始风险 `0.01832`，yaw=90° 时 ≈`2.3e-16`，
  但对任意 yaw 的**整段峰值完全相同（均 0.857375）**——只比 Peak 会**掩盖** yaw 各向异性；
  ②前缘小物体上仍有 0.846 的非零值，但**不构成车身碰撞保证**。
- 注意：Wu 的未来取自数据集已记录轨迹，是离线 Oracle，**不是部署预测器**。

**Shapely 同步车身几何**：三组真实最小间隙 + 0.01 s 插值复核，未发现插值中间接触；
11 组合成给出碰撞判据。这是物理验收基础，但单独缺速度/可避免性/主观感知。

## 5. 仍需网页版 GPT 审计与人工判断的场景

1. `figures/v0star_2p5_vs_4p5_components.png`：Actor72 远离后高风险条带，应视为合理
   注意区域还是反直觉危险？（人工风险直觉）
2. `figures/cone_yaw_and_front_edge_fields.png`：静止障碍 yaw 各向异性与「车身重叠但
   中心点分数≈0」的漏检，是否要求改为多查询点/车身包络判据。
3. `figures/v0star_actor_risk_by_time.png` + `sampling_0p1_vs_0p5_real.png`：
   0.5 s 采样错过真实最近帧与峰值（低估约 19.9%），旧结论是否需全部按 0.1 s 重述。
4. `figures/extra_real_pair_comparison.png`：26/27 场景「越接近分数越低」的非单调性。
5. `figures/controlled_page_1.png` / `controlled_page_2.png`：标量速率口径与方向门控
   是否需要改为带符号投影；急刹/加速属构造 Oracle，如何界定其证据效力。
6. `figures/longitudinal_safety_margin.png`：纵向 RSS-style 裕度能否作为独立选轨闸门
   （仅一维同车道，非官方库实现）。

本轮的判断边界：源码与数值证据基本可信，`V0*` 4.5 s 归因扎实，Wu 时空机制值得继续；
但视觉验收尚未完成，且缺少独立危险标签与合法的多候选规划集合，**因此尚不能对方法优劣排序**。
