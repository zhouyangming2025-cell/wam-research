# 候选轨迹风险评价：源码证据与全领域机制覆盖审计（R2→R3 累积）

日期：2026-10-12。**状态：R2源码证据与R3跨机制覆盖的同一份累计审计；不是路线结论、最终模型或新的工作入口。** 交接依据：`Gaussian_Risk_Field_Research_Full_Handoff_2026-10-12_CN(1).md` 和本会话第一轮 `Trajectory_Risk_Literature_Survey_R1_2026-10-12_CN.md`。其中旧 SimWAM 结果仅为交接记录，本轮**没有**重跑 NAVSIM、SimWAM、Gaussian V0/V1/V2，也没有读取用户之前审计的31仓本地包。

## 0. 本轮可确认的决策相关增量

1. **CommonRoad-CriMe 不只是 README 上的指标名录。** 已在官方 GitHub `develop` 读取 DCE、TTCE、TTC、TTCStar、ALongReq、BTN、TTM/TTR、P_MC 的实际计算函数，留存单文件 blob SHA 与逐文件 URL。既有库可作为原理/复用参考，但需要场景格式适配、指标语义核查，不能把所有 `Criticality` 视为可直接接 NAVSIM K 条轨迹的统一安全分数。
2. **同步几何距离是相对于原 Gaussian V0 的独立信息来源**：DCE 按同一时间步查询**完整多边形**间距离；TTCE 从最近距离时间读出时间。它直接补全原 V0 后轴单点漏检，但不说明名义无碰撞时的制动危险或主观不安。
3. **`TTC` 与 `TTCStar` 是两条实现路线**。普通 `TTC` 使用车道/纵向间距、加速度公式；`TTCStar` 用给定 Ego 轨迹、旋转矩形和 collision checker 做时间步检测。且 `TTCStar` 的 collision checker 还装有 road-boundary obstacle：**需要区分撞周车与触碰道路边界，不能盲目叫纯周车 TTC**。
4. **`TTR` 并非神奇通用风险概率**：它调用 `TTB`（BRAKE）、`TTK`（KICKDOWN/加速）、`TTS`（转向），由 TTM 的候选机动模拟与二分搜索求最迟启动时刻，再取 max。动作集、Ego动力学、预测 horizon、collision checker 均会改变值。
5. **`P_MC` 当前代码不等于“给定 Ego 轨迹上的周车多模态碰撞概率”**：它对 Ego 的 STOP/TURN/LANECHANGE/OVERTAKE/RANDOM 等机动做 Monte Carlo，调用 TTCStar 判断，并对碰撞样本的 pdf 结果 `np.average`。已继续追查 `utility/simulation.py`：`simulator.pdf` 对 STOP/TURN/RANDOM 等样本取 `scipy.stats.norm(...).pdf(...)`（正态**概率密度**，不是单次碰撞事件概率）。再对**仅碰撞样本的密度**取 `np.average`，不是常规 Monte Carlo 的“全部样本碰撞指示变量求均值”，也没有显式概率归一化；因此该函数返回值不可直接当作已校准 `P(collision | candidate, multimodal actors)`。
6. **GDRF 2024 与 IR 2025 依然是论文公式证据缺口，不可凭摘要补全。** 官方出版社文字证实 GDRF 的两类几何集合 `GDRF-D`（主观未来状态担忧）与 `GDRF-E`（环境损害后果）和主观评分参数校准；IR 2025 自述 IDRF 的方向性改进及模拟/真实验证。但这次仍未取得可核对的全文式子/默认参数、概率归一化及时间同步证明。
7. **冻结 V0 不变**：此前空间风险条带、单点漏检、K4 负收益都是真实课题，不能由其他代码库存在而宣告 V0 全面失败；也不能把 V0 的经验强度当碰撞概率。

## 1. 证据边界、仓库状态

- 用户研究库 `zhouyangming2025-cell/wam-research` 的 `main` 可访问和写入。2026-10-12读取 `README.md`, `state/CURRENT_STATE.md`, `state/NEXT_TASK.md`：主项目唯一下一任务仍为 P0013 BridgeSim，研究方向收敛/方法设计仍暂停。因此本文仅作为**用户新发起的风险评价文献专项证据**，不修改原 `state` 文件、不引入第二主入口、不虚构其已经取代 BridgeSim。
- 源码均通过 GitHub 连接读取，下面给出每个文件在本轮读到的 **blob SHA**（比“某天查看 develop”更容易复核具体文本）；并未执行仓库依赖、单元测试，也未验证其运行环境和所有默认参数。`develop` 是阅读时的分支，后续可能变化。具体函数问题列为 **源码观察/待做单测**，不冒充已运行的程序错误。

## 2. CommonRoad-CriMe：直接源码审计

官方源入口：https://github.com/CommonRoad/commonroad-crime ，审计分支 `develop`。

| 指标/源码 | 本轮实际逻辑 | 对 K 候选评价的边界 | blob SHA |
|---|---|---|---|
| [`measure/distance/dce.py`](https://github.com/CommonRoad/commonroad-crime/blob/develop/commonroad_crime/measure/distance/dce.py) | `ego_vehicle.occupancy_at_time(i).shape.shapely_object` 与同刻 `other_vehicle.occupancy_at_time(i)` 的 shape 距离，遍历时间，保存 `time_dce`；0提前停止 | 完整轮廓+同刻，适于物理近距比较；无制动/意图；代码将距离 `int_round(...,2)`，精细排序需验证原始未四舍五入值 | `c6ccbd6c7b3767cafb1e5580e573008c2b8f4963` |
| [`measure/time/ttce.py`](https://github.com/CommonRoad/commonroad-crime/blob/develop/commonroad_crime/measure/time/ttce.py) | 调 `DCE.compute`，返回 `time_dce - start` 乘 dt | 只报告最近接近时间，风险高低必须配合 DCE；孤立使用 TTCE 可误导 | `170f71c63dd9578d23c1b8063279d5d3f6055e30` |
| [`measure/time/ttc.py`](https://github.com/CommonRoad/commonroad-crime/blob/develop/commonroad_crime/measure/time/ttc.py) | 调纵向 `HW` 和 lanelet orientation，再解常加速度相对运动碰撞时间 | **不是通用二维绕行/路口同刻全车身算法**；对向与切入需单独看边界 | `6a5c2faf158323e4c04ae469f045692b2e5daf9c` |
| [`measure/time/ttc_star.py`](https://github.com/CommonRoad/commonroad-crime/blob/develop/commonroad_crime/measure/time/ttc_star.py) | 创建 road-boundary obstacle 加入 checker；按 Ego 给定轨迹每步 `RectOBB(length/2,width/2,yaw,x,y)` 检测障碍，碰撞则返回首个时刻 | **候选相关几何冲突可用**；但 checker 含道路边界，不能将所有命中解释为周车碰撞。0.5s间隔仍可能漏峰 | `41a47a1e0eae4da466b1cabafa57a5f5f8dd38df` |
| [`measure/acceleration/a_long_req.py`](https://github.com/CommonRoad/commonroad-crime/blob/develop/commonroad_crime/measure/acceleration/a_long_req.py) | 沿 lanelet 投影速度/加速度 + HW；一模式有 `a_obj - v_rel**2/(2*x_rel)` | 清晰制动需求，但带 lanelet 和纵向假设；`if not ego_orientation or not other_orientation` 对合法数值 0.0 也为真，**存在需单测的真值判断问题** | `3401fa79df4a5aafbb6cb7931bc3423d27b9578e` |
| [`measure/index/btn.py`](https://github.com/CommonRoad/commonroad-crime/blob/develop/commonroad_crime/measure/index/btn.py) | `ALongReq.compute` / `-configuration.vehicle.curvilinear.a_lon_max` | 相对制动能力比值；继承 ALongReq 所有输入/异常条件 | `df67e44d4b0a58f1d4469391ff130c817c2c10ef` |
| [`measure/time/ttm.py`](https://github.com/CommonRoad/commonroad-crime/blob/develop/commonroad_crime/measure/time/ttm.py) | Simulate B/K/STEER 动作，然后二分“最迟还能避免碰撞的时刻”；`detect_collision` 用 TTCStar | 不是简单数学闭式：受机动仿真集及候选基线轨迹影响 | `bc2f1a4979136c74c799eb072bc92aa8efc1293f` |
| [`measure/time/ttr.py`](https://github.com/CommonRoad/commonroad-crime/blob/develop/commonroad_crime/measure/time/ttr.py) | 实际 `self._evaluator=[TTB,TTK,TTS]`，求各个 TTM，取 max 并记录 winning maneuver | 能比较避险余量；“max”表示存在一种较晚仍可施行的逃生动作，不能直接替代多模态碰撞概率 | `401ede44c45deb0b491b64de0a945a16e59a6379` |
| [`measure/probability/p_mc.py`](https://github.com/CommonRoad/commonroad-crime/blob/develop/commonroad_crime/measure/probability/p_mc.py) | 对 Ego 模拟多种动作，收集碰撞模拟的 `pdf_bundle[j]`，`np.average(colliding_prob_list)`；无碰撞样本返回0 | **不能直接当作固定 Ego candidate + 周车联合未来的经验碰撞比例**；追查 simulator 得知 `pdf` 为正态密度（非单次事件概率） | `3cf3787a9a01012187b985a4a743f0baf27b5e28` |
| [`measure/probability/p_smh.py`](https://github.com/CommonRoad/commonroad-crime/blob/develop/commonroad_crime/measure/probability/p_smh.py) | `compute` 仅打印 `coming soon` | **仓库导出了类不代表实现已完成**；勿称该项已有可用实现 | `7208a1c87f22f15aebb8e6cd6c7ebbea8c9fcaac` |
| [`measure/__init__.py`](https://github.com/CommonRoad/commonroad-crime/blob/develop/commonroad_crime/measure/__init__.py) | 导出上述及其他指标 | 可追踪模块真实位置 | `8916ec89a4db5a0e45c41477ef2e023e52152961` |

### 2.1 DCE vs Gaussian 原核：不应只理解为“一个平滑，一个不平滑”

DCE 测量同刻预测的两块**占用形状**之间的最短几何间隙：

\[
d_{\min}(\tau^k)=\min_{i,t}\operatorname{dist}\big(B_e^k(t),B_i(t)\big).
\]

这是为横向比较写的**统一式**，不是源代码逐字数学表达。若用 \(\exp[-d_{\min}^2/\sigma^2]\) 做单调映射，在固定 \(\sigma\)、无其他项且按同一 min 距离排序的条件下，**不会产生额外候选排序信息**：仅改变数值曲线。Gaussian V0 的速度方向、类别尺度和动态门则确实包含 DCE 没有的属性，但这些属性**是否物理正确**需独立验证。一个模型平滑不代表具备更多物理信息。

### 2.2 必须审计“碰撞概率”到底在哪个随机变量上取期望

真正适用于固定候选 \(\tau^k\) 的多模态 Actor 概率应具备如下逻辑（**我们的目标定义，不是 CriMe `P_MC` 原函数**）：

\[
\hat P_{\rm col}(\tau^k)=\sum_{z=1}^Z p_z\,\mathbf1\!\left[\exists i,t:\ B_e^k(t)\cap B_i^z(t)\ne\varnothing\right],\quad\sum_zp_z=1.
\]

其中 \(z\) 是**周围交通的联合时序未来假设**，而不是“Ego 如果随机转向、制动、变道的样本”；真实项目还需预测器与校准证据，不能凭式子称真实概率。`P_MC` 是采样 Ego 行为的另一种关键性定义，其在本轮读到的代码中 `np.average(colliding_prob_list)` 现已追到底层：`SimulationRandoMonteCarlo` 使用两个正态密度相乘，`SimulationLongMonteCarlo` 与 `SimulationLatMonteCarlo` 使用 `scipy.stats.norm(...).pdf(...)`。密度值可大于1，具有连续变量的单位倒数语义，**不是归一化碰撞概率**；更关键的是代码只收集碰撞样本，再对这些密度取平均，而非对所有采样结果的碰撞指示变量取期望。因此不能把 `P_MC.compute()` 视为标准 Monte Carlo 事件频率估计。反例：若各碰撞样本 `pdf=0.2`，碰撞样本数量1和9都给 `0.2`。这种结论仅针对本次读取的 `develop` 代码逻辑；并不证明仓库其他概率模块或论文整体错误。

### 2.3 纵向 BTN 的控制算例（解析示意，不是运行 CriMe 的结果）

假定直线同车道、间隙 20m、前车恒速，Ego 纵向速度分别为 20m/s 和 30m/s，前车为 20m/s 或 10m/s；可用最大制动 6m/s²。理想化闭合速度为0时，当前维持速度无需额外减速；闭合速度20m/s时，避免追近所需等效制动 \(a_{req}=20^2/(2\times20)=10\,\mathrm{m/s^2}\)，BTN=10/6≈1.67，已超出设定制动能力（忽略反应时延将更乐观）。同样20m几何间隙，**制动可控性的信息不是几何距离单独提供的**。此式只用于一维且恒速前车；不能推广为路口全方向 BTN。


### 2.4 新增底层证据：Monte Carlo 权重到底是什么（源码已核）

读取 [`commonroad_crime/utility/simulation.py`](https://github.com/CommonRoad/commonroad-crime/blob/develop/commonroad_crime/utility/simulation.py)，本轮 blob SHA 为 `6c86edeee97b968e3db8edb7825021dac03918ea`；其约第181–215、358–387、865–894行显示：

- `SimulationRandoMonteCarlo.set_inputs`：`self.pdf = a_lat_norm.pdf(self.a_lat) * a_long_norm.pdf(self.a_long)`。
- `SimulationLongMonteCarlo.set_inputs`：`self.pdf = a_long_norm.pdf(self.a_long)`。
- `SimulationLatMonteCarlo.set_inputs`：`self.pdf = a_lat_norm.pdf(self.a_lat)`。

这里的 `norm.pdf` 是连续正态分布**概率密度函数**，即使数值可能小于1也并非“发生事故的概率”，且在标准差足够小时可大于1。对碰撞样本的密度值作均值并不是蒙特卡洛估计碰撞事件概率的标准式 `np.mean(collision_indicator_over_all_samples)`。对于重要性采样也应使用合适的完整样本权重和归一化，而代码未显示该式。**本轮结论由“仅怀疑权重合法性”推进到“已确认其返回公式不是标准事件概率估计”**，但依旧没有运行数值测试，不给出具体对外结果误差大小。

## 3. GDRF 2024 与 IR 2025：继续追索后的具体进展及限制

| 项目 | 确认的论文原文/出版社信息 | 尚未确认的决策关键问题 |
|---|---|---|
| [GDRF，Xia 等，TR-C 2024](https://www.sciencedirect.com/science/article/pii/S0968090X23004606)，DOI `10.1016/j.trc.2023.104470` | 原文出版社预览明确两组几何集合：`GDRF-D` 表示主观对未来车辆状态的担忧；`GDRF-E` 表示环境后果风险；作者称使用人类主观风险评价校准参数，处理多类目标/区域/相对运动，并通过多场景轨迹规划比较 THW/TTC/TLC | 两组集合的准确表达、形状交/并组合、风险归一化、是否同刻同步、校准对象/样本量/泛化及可开源复现情况：本轮没有全文章节与参数，**均不能擅自写公式** |
| [IR，Jiang 等，A&A Prevention 2025](https://www.sciencedirect.com/science/article/abs/pii/S0001457525003161)，DOI `10.1016/j.aap.2025.108228` | **R3纠偏**：据用户既有 §3.2–3.4 全文核查记录（本次未独立取得原始 `main.md`），方向 `r=∇IDRF/||∇IDRF||`、交互 `IR_ij=IDRF_i IDRF_j n^{-r_i·r_j}` 已知；最终场写在二维 `(x,y)`，作者将时间对齐列未来工作。出版商另证研究采用 IDRF/多模态意图。 | **不再将公式和是否显式同刻对齐标 UNKNOWN**；底数 `n` 标定、梯度零点处理、事故概率校准、消融归因和跨场景泛化仍需核正式全文/源码。证据为“用户已有原文核对结论”，不同于“本轮重读原文”。 |
| [EDRF，Jiang 等 2024](https://arxiv.org/abs/2410.14996) | 第一轮已按公开稿核其二维预测路径场与交互风险场的空间乘积 | 路径经过**时间不同**可能产生正空间风险是一个理论边界；本轮的数学反例不是对作者全部实验的独立复现，更不能将 2024 缺点直接归到 2025 IR |

**纠偏**：`GDRF` 中 `D` 与 `E` 不可随手解释为 Gaussian 的 Static/Dynamic；该论文的 `D/E` 是**主观未来状态担忧与环境后果**。`IDRF` 也不能与 `EDRF` 的风险场交互乘积视为同一模型。即便作者称“probability”，仍需核事件空间、归一化和校准。

## 4. 自主核算：同一几何路径、不同通过时刻，可完全改变实际碰撞

构造二维路口、时间 `t∈[0,6]` 秒、半径均0.2m的**圆形占用简化模型**（非真实车辆矩形，目的只隔离时间）：

\[
x_e(t)=\operatorname{clip}(t-2,-2,2),\ y_e(t)=0,\qquad x_a(t)=0.
\]

- **同步案例**：Actor \(y_a(t)=\operatorname{clip}(t-2,-2,2)\)；Ego在 \(t=2\) 穿过原点，Actor 也同时在原点，中心距0，圆形占用相交。
- **错时案例**：Actor \(y_a(t)=\operatorname{clip}(t-4,-2,2)\)；Actor在 \(t=4\) 才穿过原点，而Ego已到(2,0)。
- 二者 Ego 空间运动线段都是 \([-2,2]\times\{0\}\)，Actor空间运动线段都是 \(\{0\}\times[-2,2]\)。所以**纯粹对经过区域的二维空间场求重叠**，两案的空间交叉结构完全一致。
- 但错时案例的**同时刻中心最短距离**为 \(\sqrt 2\approx1.4142\,\mathrm m\)，发生在 \(t=3\)；扣除两圆半径之和0.4m后，最短表面距离约 **1.0142m**，全程无碰撞。已用独立0.001s等间隔数值扫查确认 `0.0` 与 `1.41421356237`（本质是解析几何结论，不是论文复现实验）。

这**严格否定了“空间扫过路径重叠必然等于时空碰撞”的通用命题**。但它**没有**证明 EDRF 两案数值必定相同：EDRF 某些权重会因速度、延时、有限未来轨迹及参数产生变化；正确的结论是其二维空间乘积本身并不构成时刻相同的显式判据。下一步应按 EDRF 原算法生成两案、固定其他输入、查看是否有错时高风险。

## 5. Frenetix：真实 API 已核，公式级概率仍 UNKNOWN

官方 [Frenetix](https://github.com/TUM-AVS/Frenetix) README 提供：

```python
cf.CalculateCollisionProbabilityFast(name, weight, predictions,
                                     vehicle_length, vehicle_width,
                                     wb_rear_axle)
```

每个 `PredictedObject(id, predicted_path, length, width)` 的 `predicted_path` 是按时间组织的 `PoseWithCovariance(position, orientation, covariance_matrix)`。这些是**直接源自官方使用示例的 API**，证实它至少接受未来位姿/协方差与车身尺寸，也支持候选轨迹 cost 回传。但是否真的严格积分两车多边形高斯占用、协方差在什么坐标系、各个时间步/Actor 如何合并、返回值是否概率（还是加权规划代价）——**尚未读到 C++ 核，标为 UNKNOWN**。不能以函数名结束源码审计。源码许可为 LGPL-3.0，项目若复用应确认许可边界。

## 6. 横向归纳：现在可以排除哪些错误等价

| 常见误读 | 源码或反例支持的纠正 | 适用边界 |
|---|---|---|
| `TTC == 全方向未来车身碰撞检测` | CriMe `TTC` 实际是车道/纵向公式；`TTCStar` 才使用给定轨迹/矩形 checker | 实现版本限定 `develop` |
| `DCE 与 Gaussian 单调映射是全新两类信息` | 只对相同距离做固定单调变换不改变候选顺序；V0 另有速度/方向输入则另论 | 固定尺度与同一查询/聚合条件 |
| `TTR只是TTC加权` | 代码对制动/加速/转向逐个做避险 simulation 并取最迟可行时刻 | 动作可行集受模型决定 |
| `P_MC 是每条 Ego 候选下对所有 Actor 随机未来取概率` | 当前实现采样 Ego 机动，`np.average` 碰撞样本 pdf，无直接联合 Actor 模态输入 | 必须追模拟器pdf语义 |
| `有完整预测路径就能安全评估未来冲突` | 路径重叠不保证同刻交叠；见可计算错时反例 | 不否定主观暴露风险存在 |
| `GDRF-D=原Gaussian Dynamic` | GDRF-D 是主观未来状态担忧的形状集合 | 以出版商预览为证据 |
| `2025 IR已解决 EDRF 的全部时间问题` | **R3纠偏**：用户已核完整公式显示输出为二维 `(x,y)`，未显式共同未来时刻；作者将时间对齐列未来方向 | 原 `main.md` 未于本轮取回；按“用户既有原文核验”记录，不再称时间同步 UNKNOWN |
| `所有 Gaussian 得分都是概率` | 核是否归一化、随机事件和校准是额外条件 | V0, DRF, EDRF, Frenetix 都分别核 |

## 7. 下轮最小有效核验（只排序，不启动大型工程）

**本段为 R2 当时的历史待办，R3已调整优先级**：P_MC 的 simulator.pdf 已追到正态密度并收口；IR 核心公式及二维时间语义已从用户已有全文证据恢复，不再为此反复检索；当前重点是机制族全覆盖、同场景横向评价与选型，GDRF 完整几何构造/Frenetix C++ 概率核只在实际进入候选验证时按需继续核查。

**最小验证矩阵（尚未实际运行）**：V0冻结风险、CriMe DCE/TTCE、TTCStar、BTN/TTR、真正条件化 Actor 模态的概率指标、EDRF路径场，在一组匹配坐标/时间/车身/未来信息条件下测试：静止锥桶任意 yaw、高速接近静物、同速正常跟车 vs 高闭合追近、后车逼近、正面会车、路口同刻/错时、前保险杠小物体接触、多个对象同时逼近。若方案只要速度/车道等额外输入就应明确申明，不为了强行同一输入剥夺其本来机制；按“共同可用输入”“合法额外输入”两组对比。

**停止与边界**：当前不训练、不中途调整 V0 参数、不改 NAVSIM PDMS、不把官方 scorer 的不连续当成风险场必须替代的证据；风险方法是否适合**训练时连续监督、候选筛选、离线安全诊断**还需后续证据。

## 8. 可追溯外部来源

- 原 GDRF 出版社页：https://www.sciencedirect.com/science/article/pii/S0968090X23004606
- 原 IR 出版社页：https://www.sciencedirect.com/science/article/abs/pii/S0001457525003161
- IR PubMed 条目：https://pubmed.ncbi.nlm.nih.gov/40929823/
- 原 EDRF：https://arxiv.org/abs/2410.14996
- CriMe 官方仓库（逐文件正文及 SHA见上）：https://github.com/CommonRoad/commonroad-crime
- CriMe 官方实用教程（列出各指标）：https://github.com/CommonRoad/commonroad-crime/blob/develop/tutorials/evaluate_scene_I_II.py
- Frenetix 官方 API：https://github.com/TUM-AVS/Frenetix
- Westhofen, *Criticality Metrics for Automated Driving: A Review and Suitability Analysis*：https://doi.org/10.1007/s11831-022-09788-7

**证据等级**：CriMe 各指标为“真实源码正文已读，未跑测试”；Frenetix 为“官方 API 已读，C++实现未核”；GDRF 为“出版社预览，公式未核”；IR 为“出版社元信息+用户既有 §3 公式全文核查结论，原始 main.md 本轮尚未取回”；错时案例为“本研究独立解析+CPU核算”；用户V0/SimWAM 数据为“交接史料，本轮未重跑”。

---

## 9. 第三轮：全领域机制覆盖审计（2026-10-12）

**研究边界**：本节是对 R1 文献账本、R2 源码、两份交接材料与本轮新检索的**同一审计文件增量**。不新增 summary / taxonomy / route-map / GitHub 状态入口，不更改主程序 `NEXT_TASK 的 BridgeSim 任务；本节回答的是独立候选轨迹风险研究的证据需求，而不是 WAM 大程序已经收敛到风险模型。用户本次评审已明确授权跨机制覆盖和公平选型审查，**并未授权模型开发或训练**。P0/P1/P2/P3/P4 的推进等级分别标明，不把部分完成伪称完全完成。

### 9.1 P0 原始材料回收与去重：取回了什么，缺什么

| 原资产 | 本轮是否实际取得正文 | 可继承的独有内容 | 证据等级和处理 |
|---|---|---|---|
| 2026-10-12 Gaussian 全过程交接约486行 | 是（当前会话上传） | 64场景K4、96场景行为实验负结果、V0/V1/V2待证伪状态、31仓项目目录和关键路径、时空错时反例 | **H：交接记录**，未独立重跑实验或读取本地原始报告 |
| 第一轮 `Trajectory_Risk_Literature_Survey_R1_2026-10-12_CN.md` | 是（文件库） | 26条文献/项目记录、7组危险机制初稿、主要公式/链接、案例族 | **R1：既有调研**；去重合入以下索引，不把其中同篇的出版社镜像当另一篇 |
| 第二轮本文件原`0–8 | 是（GitHub主分支正文） | CriMe DCE、TTCE、TTC、TTCStar、BTN、TTR、P_MC 实现、源 blob SHA、可复核错时算例 | **C：实际读过源码**；P_MC 已收口，重复代码细节不再算新增模型 |
| 31仓 `PROJECT_CENSUS.csv` / `SOURCE_EVIDENCE_REGISTER.csv` / `DEEP_MECHANISM_AUDIT_CN.md` / `CROSS_PROJECT_MECHANISM_MATRIX.md` / `UNIFIED_RISK_FIELD_RESEARCH_CN.md` | **否**；GitHub现有目录/文件库未找到这些原始审计本体 | 已知约31仓、13仓深审、E001–E073编号、5空间机制（见交接`9） | **H：仅有交接摘录**；不能说已重新核对73处代码行号与HEAD |
| IR 2025 原 `main.md` 全文 | **否**；用户提供了此前精确阅读的 `3.2–3.4 公式与结论 | 梯度方向、二维 IDRF 交互项、显式共同 t 缺失及作者未来工作 | **U：用户已完成的全文核验结果**；纠正 R2 错误 UNKNOWN；尚非本轮独立取得原文 |
| GDRF 2024 出版商全文 | **否**，只得出版商可公开预览 | GDRF-D 未来状态担忧 / GDRF-E 环境后果和主观风险校准主张 | **A：摘要与节选**，不擅自补形状公式、训练数据规模 |
| Westhofen 2023、DRF 2020、2026 主观风险 IRL | **是**，本轮读取可开放的论文 HTML 正文 | 从应用要求选择危险指标；风险阈值≠最低风险；主观偏好可以从示范学习 | **F：全文可见**；尚未执行论文复现实验 |

**31仓清点与去重边界**：交接给出的首批15仓是 METEOR、SAFE-AD、SafeRL-metaDrive-SEU-AMC、R2D_SEU_Test、Safe-Human-in-the-Loop-RL、Benchmark-RiskField、DRIFT、DREAM、RESPOND、udmc_carla、K-Risk、RiskDiffuser、GA2AD、RAP、Structure_Road_Motion_Planning；第二批16仓是 idslab-autosec/risk、GeoffreyWang1117/risk-field-model-python、CommonRoad/commonroad-crime、nav2_social_costmap_plugin、social_nav2、social_costmap_layer、navigation_layers、PySocialForce、socialforce、Autonomous-mobile-robot-navigation-in-enviroment-with-humans、Frenetix-Occlusion、PedestrianAwareMotionPlanning、Frenetix-Motion-Planner、APF-Autonomous-Driving、Artificial-Potential-Field-for-autonomous-vehicle、RVO2-python。**31是仓库，不是31个独立风险模型**。交接记录源码提示：METEOR `bevlane/risk_field.py`；SEU `safe_metadrive_adapter/risk_field.py`；Social Costmap `src/social_layer.cpp`；RESPOND `respond/risk_pattern/risk_calculator.py`；Structure-Road `src/risk_assessment/scripts/risk_field.py`。这些是**历史审计路径索引**，在原压缩包未恢复前不记本轮“源码再次复核”。

### 9.2 P1 领域谱系：按真正不同的风险信息，而不是按论文个数

| 机制代号 | 研究机制 | 数学对象/危险来源 | 代表论文或项目（实证状态） | 路线与重复边界 |
|---|---|---|---|---|
| M1 当前状态空间势/场 | `R_i(q;s_i,s_e)`、空间权重、方向、相对速度 | 原 Gaussian V0、2015/16 Driving Safety Field、METEOR、SEU、Social Costmap（H/A） | 改 Gaussian 核宽与类别、保持同输入，通常仍是一个家族；不能按不同仓库数量统计方法 |
| M2 驾驶者感知不确定性 × 后果 | `C=∫P_{\mathrm{belief}}(x)D_{\mathrm{env}}(x)dx` | Kolekar DRF 2020（F）；Xia GDRF 2024（A）；2026主观风险IRL（F） | DRF 的高斯沿**驾驶者预期路径**形成，而非原 V0 对每个 Actor 的影响核；2026 IRL 将风险参数学习/偏好阈值加入 |
| M3 预测路径/方向交互场 | 未来多模态路线投影为场，再取场重叠/方向调制 | EDRF 2024（公开 arXiv）；IR 2025（U+A） | 多模态预测器≠风险场公式；IR方向性修正≠时间同步；仍是空间场家族，不应按每个模式另算方法 |
| M4 同步几何占用/相遇 | `d_t=dist(B_e(t),O_i(t)); d_*=\min_t d_t`，同刻碰撞 | CriMe DCE、TTCStar、TTCE（C）；PET/PrET等（综述F）；几何SDF（H） | DCE与`exp[-(d_*/ρ)^2]`在固定ρ、同样时间归约下可能同排序；平滑核不必算新信息 |
| M5 相对运动与操作余量 | 纵向相对速度、必要减速度、RSS安全距离、TTR，速度障碍 | CriMe BTN/TTR（C），RSS 2017（P）、Velocity Obstacles 1998（A/F） | VO速度空间的冲突集合区别于只看速度“大小差”；BTN/RSS内含动作能力，不能仅靠空间距离替代；但现成纵向BTN不是全向模型 |
| M6 同时刻多模态危险概率 | `P(\bigcup_{t,i}{B_e(t)\cap O_i(t)\ne\emptyset}\mid \tau_e,\mathcal I)`（事件定义示例） | Frenetix（API/C++核待核）、2024概率可达框架（F）、chance constraints（RADIUS） | 模态权重、时间相关性和校准决定概率含义；逐时最大概率≠全时碰撞事件概率。CriMe P_MC **不作为合格概率基线** |
| M7 可达性与可避免性 | `\min_u\max_w safety-margin`、可达/安全集或违反约束上界 | Li等 ICRA 2021 HJ预测可达性（A），RADIUS 2023论文+代码（P+C），2025不确定可达性（F） | 回答“是否有可行避险动作”，而不是单纯“路径离物体远吗”；直接候选逐条调用可能昂贵 |
| M8 学习型风险、偏好与反应交互 | `P(\tau\mid s)\propto\exp R(\tau)`、感知风险约束、周车条件响应 | Sadigh等 RSS 2016（F）；Liang等 2026 主观风险阈值 MaxEnt IRL（F） | 从人类选择学到的不等同于安全真值；响应型预测应与非反应式固定未来区分；这是新增的重要机制，不要仅挂“DRF小变体” |

**过去研究覆盖缺口的具体变化**：31仓审计已大量触及 M1/M3 的空间机制、部分 M4 与 M6 的软件入口；本轮一手公开文献重点补 M2 的主观风险阈值学习、M5 的 RSS/VO 可操作安全逻辑、M7 的 RADIUS 和预测可达性、M8 的 Ego-Actor 反应条件化。不是8套必须融合的模块，也不是互斥的8种模型。交叉点若输出不同风险语义应分层记录。

### 9.3 文献/项目一体化去重账本（精简但保留证据）

证据等级：**F=本轮可见论文正文；C=本轮读过计算源码；U=用户已核全文且提供公式（本轮原文件未恢复）；A=正式摘要/出版社节选；P=官方仓库/论文入口、未核核心源码；H=仅交接史料**。同篇预印/期刊/项目页只算一条，交叉覆盖只记在机制列，不重复计数。以下是**跨机制高价值子集**，不是“已重新检查31仓每个原始文件”的宣称。

| ID | 来源/年份 | 机制 | 本轮事实与等级 | 直接性/最关键缺口 |
|---|---|---|---|---|
| R01 | 用户 Gaussian V0（冻结核） | M1 | H：Static+Dynamic+速度差+方向sigmoid | 有候选query接口；真实场景低速与车身漏检须验 |
| R02 | Wang 等，The Driving Safety Field，IEEE T-ITS 2015，DOI:10.1109/TITS.2015.2401837 | M1 | A：环境势、运动与驾驶者行为场 | 是候选危险建模源流，非直接已实现K条评分器 |
| R03 | Wang 等，Driving Safety Field Theory Modeling，TR-C 2016，DOI:10.1016/j.trc.2016.10.003 | M1 | A：`E_S=E_R+E_V+E_D`，道路/车辆/驾驶因素，实车碰撞预警 | 不是“通用候选risk函数已验证” |
| R04 | METEOR / SEU / Social Costmap（3子群） | M1 | H：交接中报告的类别、yaw与速度核修正 | 等原31仓索引才可确认各源码HEAD；不当3种物理新信息 |
| R05 | Kolekar 等，DRF，Nature Communications 2020，DOI:10.1038/s41467-020-18353-4 | M2 | F：驾驶者位置感知不确定性×环境后果，曲线高斯与阈值控制，7情境 | 可做主观暴露基线；缺候选轨迹适配与参数跨域校准 |
| R06 | Xia 等，GDRF，TR-C 2024，DOI:10.1016/j.trc.2023.104470 | M2 | A：GDRF-D/E几何风险、主观评价校准主张 | 论文精确构造/数据/可运行源码尚待核；不编造 |
| R07 | Liang 等，Subjective Risk-Driven IRL，Advanced Intelligent Systems，2026，DOI:10.1002/aisy.70412 | M2/M8 | **F：完整公开正文**，主观高斯重叠、风险阈值和MaxEnt IRL、自然驾驶与HiL验证 | 有直接候选轨迹风险约束定义；未核可复现代码/跨域预测安全 |
| R08 | Jiang 等，EDRF，arXiv:2410.14996，2024 | M3 | R1已有开放全文公式阅读，R3未再次读所有附录 | 多模态空间场、交互项；需同刻/错时专门测试 |
| R09 | Jiang 等，IR，Accident Analysis & Prevention 2025，DOI:10.1016/j.aap.2025.108228 | M3 | U+A：核心`r=∇IDRF/||∇IDRF||, IR_ij=IDRF_i IDRF_j n^{-r_i·r_j}`；二维场未显式共同时刻 | 时间同步不能当已解决；概率/后果语义需核剩余部分 |
| R10 | Fiorini & Shiller，Velocity Obstacles，IJRR 1998，DOI:10.1177/027836499801700706 | M5 | A：相对速度空间内定义将导致碰撞的速度集合、交加速度可行动作 | 适于检测相对运动方向，但原方法本质是速度避碰，不是多候选连续感知风险 |
| R11 | Westhofen 等，Criticality Metrics，ACME 2023，DOI:10.1007/s11831-022-09788-7 | M4/M5 | F：综述、PET/PrET/TTC/制动/概率/可避免性，强调适用性选择 | 理论索引，不是单独新算法 |
| R12 | CommonRoad-CriMe DCE/TTCE/TTCStar | M4 | C：同步完整多边形/旋转车身与车道边界 | 可适配候选；需障碍/道路归因与时间采样 |
| R13 | CriMe ALongReq/BTN/TTM/TTR | M5 | C：车道纵向必要加速度和避险机动二分搜索 | 近跟车/减速有用；不能视作全向街区统一风险 |
| R14 | Shalev-Shwartz 等，RSS，arXiv:1708.06374（2017） | M5 | A/P：形式化纵横安全距离及正确响应定义 | 物理安全裕度很重要，正式代码版/参数政策尚未固定 |
| R15 | Ortiz 等，TTC with motion orientation，A&A Prevention 2023，DOI:10.1016/j.aap.2023.107172 | M4/M5 | A：有yaw方向的TTC扩展 | 横向安全指标对照；未核全文几何公式/代码 |
| R16 | TUM-AVS Frenetix 与 Frenetix-Motion-Planner，2024论文 arXiv:2402.01443 | M6 | P+R2核API：Gaussian位置/协方差、车身尺寸、候选代价调用 | 核心 C++ 概率/校准仍未知；不能按名字认为返回绝对碰撞概率 |
| R17 | Reachability-Based Confidence-Aware Probabilistic Collision Detection，Engineering 2024，DOI:10.1016/j.eng.2023.10.010 | M6/M7 | F：BRS保障区+随机FRS按时估危险，验证主要为**高速公路** | 组合框架的独立证据；跨路口通用性未证明 |
| R18 | Li 等，Prediction-Based Reachability，ICRA 2021，DOI:10.1109/ICRA48506.2021.9560790 | M7 | A：预测左/右转意图后按模态使用HJ安全控制，T路口/环岛仿真 | 预测减保守，但仍是安全控制器，不是可直接代入K4的标量 |
| R19 | Liu 等，RADIUS，2023，arXiv:2302.07933，官方 `roahmlab/RADIUS` | M6/M7 | A+P：离线参数化可达集、在线风险上界优化、概率阈值 | 有代码入口但尚未跑；需检查车辆模型/城市VRU适配 |
| R20 | Zhou 等，Environment and Uncertainty-Aware Reachability Planning，Control Eng Practice 2025，DOI:10.1016/j.conengprac.2025.106319 | M7 | F：道路几何约束+在线意图控制集；环岛仿真和硬件验证 | 证明此族仍有实质发展，但不等于轻量候选打分器 |
| R21 | Sadigh 等，Planning for Autonomous Cars That Leverage Effects on Human Actions，RSS 2016，DOI:10.15607/RSS.2016.XII.029 | M8 | F：Ego动作影响人的反应，使用IRL学到的驾驶者奖励建反应模型 | 候选专属周车未来，不能与同一固定未来预测器不加区分比较 |
| R22 | FHWA Surrogate Safety Assessment Model（SSAM） | M4/M5 | A：TTC/PET等历史交通冲突指标；R1已列 | 更适合事后冲突诊断，不能自动当在线主观安全代价 |
| R23 | RADIUS之外的 SocialForce/RVO2 社交避碰开源簇 | M1/M5 | H：31仓审计记录其机制位置 | 作为行人相对运动/空间回避的移植性对照；非汽车正式风险评分实证 |

**本轮高价值新增**：R07 的 2026 主观风险阈值 IRL、R17 的“保证安全区域与概率可达区域分离”、R19 的概率约束可达性、R21 的反应条件化交互。按机制计量是四种研究能力，而不是新增仓库数。R17的试验主要是高速公路，不能写为通用城市道路验证；R07的“human-likeness”不等于真实事故风险校准。

### 9.4 P2 代表机制的真实计算链及相互非等价

**(A) 原 Gaussian V0**：输入 Actor 的`(p,\theta,L,W,v)`和 Ego 的查询位置/速度，先旋转 Actor 局部坐标，算`R_s+R_d`，再经 Actor Sum/Max、同步轨迹时间归约变成候选分数。`σ_v=6|v_a-v_e|`在低速Actor且高速Ego时会将无可信 yaw 的细目标拉成长条；在正常有向车辆上可能有提前危险提示。**V0单Actor公式不是概率**；交接报告已经记录其对正常车的主观肯定与对低速类型的实景异常，两者都应保留。

**(B) DRF 2020：风险不是 Actor 向外发射的核。** 论文公开的驾驶者感知风险形式可概括为`C=\sum_{q}P_{\mathrm{DRF}}(q\mid s_e,\delta)\,D_{\mathrm{scene}}(q)`（离散网格对应论文图示；不是对所有Actor都使用Gaussian）。DRF沿**驾驶者预期车辆路径**弯曲，前瞻时间、速度、方向盘与形状宽度影响其形状；2020论文正式正文`σ_i=(m+k_i|\delta|)s+c`，控制器保持`C`在风险阈值附近而非绝对最低。候选适配：每条给定候选必须从轨迹获得局部转向/预期路径并合法校准`P_DRF`；若只用单一当前δ，无法代表任意给定K条复杂未来。验证：论文报告7种道路/交通情境的拟人驾驶规律，而非跨类别同刻碰撞概率校准。

**(C) IR 2025：方向增强的二维交互。** 用户之前核得`r_i(x,y)=∇IDRF_i/||∇IDRF_i||`、`IR_ij=IDRF_i IDRF_j n^{-r_i·r_j}`。输入每参与者多模态路线/方向/风险场，输出二维空间交互强度；`r_i·r_j`是两个单位方向的余弦，指数修正会改变方向不同的交互权重。**公式没有共同时间`t`和同刻车身占用判据**，因此不能从“用了未来轨迹”推出“不会把错时过路口误判危险”。本轮没有原始main.md，不补未公开参数，不擅称“全文独立重读”。

**(D) 同步完整几何：** 输入`B_e^k(t)`（第k候选车身多边形）和`O_i(t)`（Actor未来占用），输出`d_i^k(t)=dist(B_e^k(t),O_i(t))`，最后`d_*^k=\min_{i,t}d_i^k(t)`。这是**统一建模对照的定义**；CriMe DCE源码实现按同刻多边形距离，TTCStar做同刻碰撞并含道路边界。`d`是间隙而非心理危险；`d=0`同时覆盖刚接触和深度交叠，若要区分严重碰撞需交叠深度/相对速度。转换`e^{-(d/\rho)^2}`可更平滑，但固定单调变换不产生额外风险信息。

**(E) Brake/RSS 操作安全：** 在**同车道纵向接近、恒相对速度简化**条件下，物理必要减速度可写`b_{\mathrm{req}}\approx(\max(v_e-v_f,0))^2/(2g)`（`g>0`为可用纵向净间隙；这是解析示例，**非逐字CriMe公式**）。BTN把需要的刹车强度与车辆可用最大减速度相比；RSS还考虑反应延迟、反应期加速、前车/后车制动与正确响应。对路口、后车和横向对象不得硬套同一道路中心线公式。TTR对制动/加速/转向的行为可行性重模拟，计算成本和动作集都更大。

**(F) 多模态概率（本研究统一事件定义，不冒充某论文）：** 固定Ego候选`τ_k`，周车联合未来模式`Z`和传感/预测信息`\mathcal I`，定义`P_k=\sum_z P(Z=z\mid\mathcal I,\tau_k)\mathbf1\{\exists t,i:\,B_e^k(t)\cap O_i^z(t)\ne\emptyset\}`。若使用离散加权采样，这才是“轨迹周期内至少发生一次碰撞”的联合事件概率的标准骨架；逐时概率简单相加可能重复计数，模式独立假设需说明，概率质量可能失准。Frenetix提供候选与协方差接口，**但本轮未核是否实现此式**。CriMe P_MC已明确不是同一条件事件。

**(G) 可达性：** 给定动力学`\dot x=f(x,u,w)`、可控输入`u`、周车扰动`w`，计算安全/危险可达集合或风险上界；RADIUS用离线参数化FRS和运行时风险上界设计动作。它回答在安全约束下是否仍存在避险轨迹，不与“某点的Gaussian值”同义。现成优化器的输入动作参数化可能不同于离散K条Ego轨迹，轻量适配并未验证。

**(H) 主观风险阈值 MaxEnt IRL 2026：** 作者真实正文给`\mathcal T_{\rm safe}=\{\tau:C(\tau)\le\delta\}`，风险接受集合内`\pi(\tau)=e^{R(\tau)}/Z`，`C`从主观高斯场与环境危险场重叠建模，并通过驾驶示范学习风险参数。**论文通过naturalistic/HiL支撑“行为拟人程度和个性化”的结论，而不能推断同刻碰撞判别最优**。如果目前没有风险标注/偏好数据，直接在NAVSIM部署需额外适配、训练和泛化验证；暂不作为低成本第一个实现。

### 9.5 P3 典型场景 × 机制证据矩阵

符号等级（**非模型强弱评分**）：`[P]`论文实验证实与该场景相近（注意实验任务/数据限定）；`[C]`源码运算支持此机制（尚未同条件真实测试）；`[T]`数学机制理论上能表达，但尚无匹配场景验证；`[N]`原始定义明确不足/无法单独完成；`[?]`证据不足。每个单元含关键限制语，不能按字母数计算模型排行。`G`=原Gaussian V0；`D`=DRF/GDRF；`I`=EDRF/IR；`O`=同步占用几何；`B`=BTN/RSS/制动；`P`=同步多模态碰撞概率；`R`=可达性/避险；`L`=主观风险学习/反应式。

| 场景/物理问题 | G | D | I | O | B | P | R | L |
|---|---|---|---|---|---|---|---|---|
| 稳定正常跟车 | [T]相对速度核/几何 | [P]DRF论文含跟车 | [T]道路方向场 | [N]间隙本身无制动含义 | [C]RSS/BTN可度量纵向余量 | [T]若预测不碰撞趋0 | [T]可控刹车空间 | [P]拟人行为而非安全真值 |
| 高速追近 | [T]纵向扩散，未校准 | [P]DRF驾驶响应 | [T]路径场可能提前关注 | [C]未来间隙衰减 | [C]制动需求随闭合增 | [T]模式权重依赖预测 | [T]动作是否仍可避让 | [T]需风险偏好标签 |
| 前车突然减速 | [N]仅当前无先验难预警 | [?]未来后果须给预测 | [T]须预测到急刹模式 | [C]给定未来则可同刻判别 | [C]当前制动余量；突发前车行为仍需假设 | [T]急刹模态须有质量 | [T]将前车减速纳扰动集 | [T]响应模型学习不可保证涵盖急刹 |
| 后车高速逼近 | [T]原核有方向门控需反例 | [T]看后方权重设定 | [?]全向主张，未独立核后车实验 | [C]同步几何可检测尾撞 | [T]RSS纵向后方危险，现成BTN方向需改 | [T]包含后车意图才有效 | [T]可避免性由后车反应能力决定 | [?]训练覆盖与响应条件未知 |
| Cut-in/窄距换道 | [T]横向核可响应但yaw/宽度受限 | [P]DRF含超车/绕障，非直接cut-in真值 | [T]交互场；时间混淆需测 | [C]同刻车身宽度与间隙 | [N]纯纵向BTN不够 | [T]需周车横向多模态 | [P]HJ预测可达性有交互转向示例 | [P]Sadigh展示响应式并线 |
| 对向交通 | [T]标量速度差可能失真 | [P]DRF含对向情境 | [T]梯度方向增强但非相遇保证 | [C]相向几何相遇时间 | [N]直接套跟车制动错误 | [T]依赖方向轨迹预测 | [T]相对速度/可达集合可表述 | [T]行为预测参与方向判断 |
| 路口同刻相交 | [N]仅当前空间核不保证同刻 | [T]需要前瞻/道路后果 | [N]二维场不保证同刻判别 | [C]同步车身接触 | [N]纯纵向公式不支持 | [T]联合时空事件概率 | [P]HJ在T路口仿真 | [P]反应式人车研究含路口交互 |
| 路口错时通过 | [N]潜在“路径重叠=危险”误报 | [T]暴露风险可非零，不等于碰撞 | [N]二维乘积单独不识别时差 | [C]相同位置不同t不碰撞 | [N]纯纵向指标不充分；PET可测 | [T]同步事件概率应识别 | [T]时变占用可避免不必要约束 | [T]依赖响应预测正确 |
| 行人横穿/骑行者 | [N]低速yaw与细长核既有异常 | [T]后果场可分类型；待校准 | [T]多模态路线+方向不保证几何 | [C]类别占用合法即可同刻查 | [N]车辆纵向制动比不可直接复用 | [T]横穿/停下多模态、需概率校准 | [T]可达集复杂且费用较高 | [?]低频危险数据泛化弱 |
| 停车汽车/锥桶任意yaw | [N]已发现低速斜长条 | [T]场朝向应由可观测运动/环境定 | [?]静态目标表示细节待核 | [C]真实形状不依赖运动yaw | [T]Ego制动紧迫性独立于物体yaw | [T]静态占用为确定模式即可 | [T]固定障碍避险可达性 | [?]训练域与分类/尺寸误差 |
| 弯道/无车道线 | [T]Actor真实朝向仍有稳定性问题 | [P]DRF论文有曲率情境 | [T]空间路径结构可曲 | [C]全局坐标任意车身 | [N]需改写纵向车道模型 | [T]世界坐标的占用有效 | [T]可达性可以不强依赖固定车道 | [?]训练地图依赖待证 |
| 多车+不确定未来 | [T]Max/Sum主导与饱和问题 | [T]场成本可累加但量纲须校准 | [T]多模态场有重叠，跨Actor同步待核 | [C]min间隙能找主导对象但无联合概率 | [T]逐对约束不自然变联合风险 | [T]需保留joint modes/事件相关 | [T]多对象最坏扰动保守 | [T]数据驱动交互需有匹配训练 |

**如何读矩阵**：例如“路口同刻/错时”的 [C] 只表示读取CriMe源码证实存在**同步多边形检查机制**，不是已对原 NAVSIM 日志验证性能；DRF 的 [P] 只表示对应论文有类似**驾驶行为情境实验**，不代表作者验证的安全与我们候选排序标签相同。绝不进行“加总评分”。

### 9.6 以“前车突然减速”为共同主线，做机制级对比

统一条件：Ego 20m/s，前车 18m/s，初始车身间隙20m，给定Ego候选`τ`不变。若前车继续18m/s，当前相对闭合速度2m/s，简化恒速 TTC≈10s；若前车在1s后开始减速，未来风险可能很快上升。下面是**机制解释而非已跑实验**：

- **原V0**只根据当前Actor状态及相对速度形成方向核，若不给未来急刹，无法凭空获知加速度突变。即便高速逼近时风险带合理，也不是“预测未来”的证据。
- **DRF/GDRF**可以让驾驶者前瞻位置的不确定性/潜在伤害产生非零担忧，但具体是否敏感前车急刹，取决于其感知模型是否把该后果与风险权重计入；不能从“主观”二字直接推断。
- **IR/EDRF**若预测器有“继续/急刹”模态，可把新模态注入未来路径交互；如果只给连续行驶模态，就无法凭公式恢复漏掉的行为。二维交互仍需测试时序误报。
- **DCE/同步占用**：若输入真实急刹future，Ego-Actor同步几何间隙可以准确衰减到接触；若只给当前CV，仍只能得到CV下的几何结果。对已知未来，它解决“哪里/何时碰到”，但不测制动余量。
- **BTN/RSS**：用当前速度、间隙、假设的最大前车制动力、Ego反应时间与可用制动量，能回答在突发急刹条件下是否仍保持安全，**不需要已知具体实测急刹未来**，但依赖明确的物理行为约束。
- **多模态概率**：关键不只是有预测轨迹，还要对急刹概率赋值并保持事件一致的全轨迹计算；当前行为先验漏掉急刹时概率可错误很小。
- **可达性**：将允许的前车制动行为视为扰动、Ego允许操作视为控制动作，判断安全可操作空间。最坏情况集合大时易保守，依靠真实预测意图减保守则面临预测偏差。
- **学习型主观/反应风险**：可通过示范学习“感觉危险时更早减速”的选择模式，亦可能学到驾驶者的不安全跟车习惯。主观一致≠硬碰撞保证。

**该场景的研究判断**：要同时解释“稳定近车距依旧存在风险”和“前车急刹前可操作余量”，仅有名义future碰撞概率可能不足；运动安全/反应余量提供额外信息。但这仍不证明一定要把BTN/RSS和DRF数值线性相加；不同分量可能在相同接近事件上重复惩罚。

### 9.7 技术传承与补充：哪些不是新的危险信息

- **空间场历史**：Wang等驾驶安全场（环境/运动/驾驶员）与用户V0有相似空间影响视角，但并非“DRF 2020全领域首创”或“V0必错”。
- **DRF→GDRF→2026感知IRL**：共同关注驾驶者主观担忧，但数学域/是否学习阈值不同；不能把GDRF精确公式在没全文时写成已核。DRF偏`ego预期位置概率×后果`，V0偏`Actor空间危险势`，方向正好不同。
- **EDRF→IR**：未来多模态路径空间场引入方向项；新增方向不等于同刻占用；几何重叠与时间同步是不同信息。
- **DCE→平滑足迹核**：若只是`g(d)`固定单调变换，在固定聚合条件下同一排序；与制动需求、路径不确定性、主观风险不是同一信息。
- **TTC→BTN/RSS→TTR/可达性**：从“多久撞”逐渐进入“需要多大操控、是否还来得及/仍可安全”层面；但不是每个版本都满足城市路口。
- **确定性同步占用→联合多模态概率**：相同时空几何上，对不同未来加权求事件概率，是新信息源；“ Gaussian 模型名称”不能说明是否概率。
- **固定周车future→Ego条件化反应**：预测条件信息变了，可能获得新能力；必须固定同一预测协议对比风险算子的贡献。

### 9.8 P4 进入小规模真实验收的8个代表（筛选而非最终采用）

优先级为**验证价值/机制独立性**，不是实验胜负榜。输入要求：统一世界坐标和物理时刻；固定`K`条Ego候选和同步完整占用；划分 “当前+CV” / “合法预测未来” / “GT未来Oracle离线” 三个证据层次，绝不混用。

| 候选 | 实际最小表达/来源 | 为什么要比 | 输入和代价边界 | 最强反例与状态 |
|---|---|---|---|---|
| V0 冻结原 Gaussian | 旧单Actor Static+Dynamic+方向sigmoid；原 `mcts_planner/risk_field.py`（H） | 保留正常车方向性优势假设，作为连续空间风险起点 | 当前Actor/Ego pose、速度、类别尺寸；空间查询便宜；原源码需对哈希 | 低速锥桶长斜线、后轴漏小障碍；**冻结基线，不调参** |
| DRF 2020 代表主观场 | 作者 Nature 2020 `C≈∑P_DRF·D_env` + 风险阈值控制 | 检验“人类感知风险”是否真正提供更适合的连续信号 | 需给定候选转成预期路径和行为状态；校准参数；Matlab作者代码可追索 | 急刹模态缺失/行人多意图、不同司机偏好；**F，有方法但未适配** |
| IR 2025 方向化交互场 | 用户已核`IDRF_i IDRF_j n^{-r_i·r_j}` | 代表未来路径场/方向交互而非另选EDRF重复实现 | 需多模态预测/空间风险场；原`main.md`和运行代码待取回 | 同刻/错时、梯度为零、低速向量；**U+A，完整原文需归档复核** |
| 同步车身 DCE/TTCStar | CriMe `measure/distance/dce.py`、`measure/time/ttc_star.py` | 物理几何锚点；直接验证小障碍与错时 | 多边形、同刻轨迹；可用现成源码，TTCStar需排除道路边界混合事件 | 高速近距同速且不碰撞未必高风险；**C，低成本第一批** |
| 制动安全余量 BTN/RSS | CriMe `index/btn.py` 和`acceleration/a_long_req.py`；RSS 2017 | 区分几何距离、闭合速度、制动能力；补静态高速逼近 | 车辆动力学/制动/反应参数；纵向适配可靠区域，非城市路口通用 | Cut-in与对向几何难直接通用；**C+A，先做合法纵向测试** |
| Frenetix多模态概率 | `CalculateCollisionProbabilityFast`（官方API） | 检验校准后联合未来不确定性是否优于仅确定距离 | 需预测协方差/模态、相关性与事件归一化；C++实现未核 | 预测遗漏突然横穿/过度自信；**P，公式源门未过暂勿直接用“概率”绝对值** |
| RADIUS可达风险上界 | Liu等2023 + `roahmlab/RADIUS` | 回答“还能否避免风险”的新信息，不重复投影Gaussian | 要有车辆模型、控制参数集、FRS离线资产和运行时优化；集成成本高 | 多车VRU实时场景/动作集合不完备；**A+P，第二批高成本对照** |
| 2026主观风险阈值IRL | Liang等 2026 `C(τ)≤δ` + MaxEnt 偏好分布 | 检验学习风险约束能否比手写核更符合主观偏好 | 必须有驾驶示范/训练参数及跨域验证；论文正文已取、官方可运行权重未核 | 危险示范偏好、长尾OOD、“拟人”不等于安全；**F，研究对照不立即训练** |

**值得明确暂时不单立验证项**：GDRF需等原始几何公式证据门通过后，决定能否替换DRF代表；EDRF与IR重复预测路径场，不应两者都算8种独立信息；PET/PrET可作为路口诊断而非单独候选；RVO/VO是速度空间安全域对照，不一定要另做热力图；CriMe `P_MC`因事件语义问题禁止作标准碰撞概率基线；仿真安全的RSS与从人类示范学到的风险不直接合并为同一量纲。

### 9.9 验收而非大工程：同输入控制变量与失败归因

1. **场景先固定**：正常跟车（不同车距/速度）、急刹、后方追近、cut-in、对向、路口同时/错时、横穿、静止锥桶0～4m/s+yaw扰动、停车汽车、弯道、小障碍Ego前中部交叠、多车联合。
2. **输入四组必须分列**：S0仅当前真实状态（用于几何机理离线）；S1当前+CV；S2同一预测器给每种方法的合法多模态future；S3GT future只用于离线Oracle。这是**观测协议划分**，不能误说S0可以部署（它可含GT当前标注）。
3. **监督/评价目标分列**：①同刻全车身碰撞/距离与事件时刻（物理几何）；②可用制动/操作余量（独立动力学参数）；③有评判者时的主观配对风险偏好（不能由几何距离自动替代）；④CPU/GPU计算延迟和Actor数扩展。各指标只对其自称风险语义负责。
4. **匹配比较**：几何评价对齐车身和时间步；主观场不强制成0–1碰撞概率；概率值须先检查事件空间/校准；训练依赖比较报告总成本；不要把“用了更强预测器”误当“风险函数更好”。
5. **结果分类不主观打分**：[已有论文实验]/[本轮源码证实]/[仅数学机制支持]/[现有定义不支持]/[原文或源代码未读]。真正在同一独立场景跑过才可新增“本项目实证”。
6. **可视化**：对有空间场的用共享Jet与同场景相同色标；不同量纲应同时给“绝对原值”和**仅为形状**的独立规范化图；对RSS、TTR、RADIUS用安全裕度/时域风险/可达集，不强行伪装热力图。
7. **停止规则**：暂不改V0、NAVSIM benchmark、SimWAM训练或K4选择器，不启动大数据下载；先确认哪些算法现成可运行且物理定义吻合，不为制造创新合并8分量。V1/V2是用户历史已提出但未有新实验结果的假设，不能提前宣称胜出。

### 9.10 当前能与不能下的研究结论

**已经可以下的**：①完整占用几何与原点Gaussian存在真实查询差异；②纵向制动/可操作余量含有单纯几何间隙之外的信息；③二维未来路径相交本身不保证同刻碰撞；④原IR 2025 的方向化交互没有显式共同未来`t`；⑤概率预测依赖校准和联合事件定义，CriMe `P_MC`不可默认适用；⑥DRF与2026主观风险IRL提供主观阈值和从示范学习的实在文献证据；⑦可达性可提供“是否仍可规避”的附加答案。这些是机制层的证据支持，不等于最终选轨实测比较胜负。

**尚不能下的**：①“V1/V2优于V0”；②“DRF/GDRF/IR在人类主观评价和城市全场景一定优于Gaussian”；③“Frenetix函数返回校准的全轨迹碰撞概率”；④“RADIUS可直接低开销替换多候选风险评价”；⑤“2026学习风险已适合NAVSIM泛化”；⑥“现有8个机制必须合成统一模型”；⑦“已复核完31仓E001-E073所有行号”。要得这些结论需要相应场景数据、源码和独立同输入实验。

### 9.11 本轮新增一手来源索引（去重，以正式论文/官方仓库为准）

- Westhofen et al. 2023 Criticality Metrics（期刊全文）：https://link.springer.com/article/10.1007/s11831-022-09788-7
- Kolekar et al. 2020 DRF（期刊全文）：https://www.nature.com/articles/s41467-020-18353-4
- Xia et al. 2024 GDRF（出版社节选，非全文）：https://www.sciencedirect.com/science/article/pii/S0968090X23004606
- Jiang et al. 2025 IR（出版商信息；公式证据另来自用户既有全文核验）：https://www.sciencedirect.com/science/article/abs/pii/S0001457525003161
- Liang et al. 2026 主观风险学习（开放期刊全文）：https://advanced.onlinelibrary.wiley.com/doi/10.1002/aisy.70412
- Shalev-Shwartz et al. RSS（原论文）：https://arxiv.org/abs/1708.06374
- Fiorini & Shiller 1998 Velocity Obstacles（出版页）：https://journals.sagepub.com/doi/abs/10.1177/027836499801700706
- Li et al. 2021 Prediction-Based Reachability（IEEE）：https://ieeexplore.ieee.org/document/9560790/
- Liu et al. 2023 RADIUS：https://arxiv.org/abs/2302.07933 ；作者代码：https://github.com/roahmlab/RADIUS
- Reachability-Based Confidence-Aware Probabilistic Collision Detection 2024：https://www.sciencedirect.com/science/article/pii/S2095809923004915
- Zhou et al. 2025 Environment/Uncertainty-Aware Reachability：https://www.sciencedirect.com/science/article/pii/S0967066125000826
- Sadigh et al. 2016 反应式交互（RSS正式论文页）：https://www.roboticsproceedings.org/rss12/p29.html
- Ortiz et al. 2023 TTC with motion orientation：https://www.sciencedirect.com/science/article/pii/S0001457523002191
- Wang et al. 2016 Driving Safety Field：https://doi.org/10.1016/j.trc.2016.10.003
- CriMe真实源码与官方接口：https://github.com/CommonRoad/commonroad-crime ；https://cps.pages.gitlab.lrz.de/commonroad/commonroad-criticality-measures/user/getting_started.html
- Frenetix 官方规划论文：https://arxiv.org/abs/2402.01443 ；代码：https://github.com/TUM-AVS/Frenetix-Motion-Planner

**限制与下一次只需补最小源**：31仓审计五份CSV/MD与IR完整`main.md`目前没有可访问本体，已知的关键信息已按H/U恢复；若要完成“全量逐源去重”的最高等级核验，仍需那份本地压缩包/文件，不能用网络搜索凭空补其E001–E073编号。其余当前研究阶段所需的**机制全景和候选筛选已形成第一版**。未启动模型运行或大规模训练。

---

## 10. 第四轮：由文献全景进入实际场景最小验收（2026-10-12）


**性质**：小规模运行证据，继承 R3 机制清单，**不是最终模型选型**；无训练、无官方 NAVSIM 评分、不改 SimWAM。原始内容来源为 [SCP-CN-001/trajectory_dataset_support 的 INTERACTION 路口录制样例](https://github.com/SCP-CN-001/trajectory_dataset_support)；`trajectory_sample/INTERACTION/recorded_trackfiles/DR_USA_Intersection_EP0/vehicle_tracks_000.csv` 的 Git blob SHA 为 `f15a96fd2000b198e4719c38054098abf577c917`。该仓提供第三方的**样本**，不是原创记录方。原始 INTERACTION 数据集的正式出处为 [INTERACTION Dataset](https://interaction-dataset.com/)。本轮只使用少量数值，未取得整套数据集，也未声称训练或预测已经部署。

## 1. 时间分层风险场的一手公式核验

Wu 等，2024，*An Integrating Comprehensive Trajectory Prediction with Risk Potential Field Method for Autonomous Driving*，arXiv:2404.00893v1，论文正式可读 [HTML](https://arxiv.org/html/2404.00893v1) 的 §IV-B 式(7)(8)(9)以及 §IV-C 式(15)；[PDF 第4页](https://arxiv.org/pdf/2404.00893)。完整单 Actor、多模态逐时风险场：

\[
\Theta_i^t(x,y)=\sum_j p_{ij}\exp[-(\Delta x_{ij}^2/a^2+\Delta y_{ij}^2/b^2)],\quad
[\Delta x_{ij},\Delta y_{ij}]^T=R(-\varphi_{ij}^t)[x-x_{ij}^t,y-y_{ij}^t]^T.
\]
\[
\Theta^t(x,y)=\gamma^t\sum_i\Theta_i^t(x,y).
\]

**源论文事实**：TRTP按候选目标区域预测多条轨迹及其概率，逐未来时刻叠加风险，结合 MPCC 轨迹优化，论文在 CARLA 仿真中验证。**本轮实现边界**：没有 TRTP 预测器与 MPCC；只取真实 Actor 记录轨迹的单模式 `p=1`（**GT-future Oracle，不可部署**），选定演示核 `a=6m, b=2m, gamma=0.95/0.5s`，每时刻采样记录中的同刻 Ego 位置。`a/b/gamma` 为**本次演示选值**而非声称论文默认。使用 Eq(9) 折扣一次；论文 Eq(15) 又出现 `gamma^k Theta`，有可能构成额外折扣，故不将本轮候选均值冒充论文完整 MPCC 成本。数学形式吻合 Eq7-9，预测、时间步长、参数和优化器**不等价于论文复现**。

## 2. 三条可计算方法的明确边界

| 代号 | 实际输入与输出 | 实现真值等级 | 原方法未覆盖的部分 |
|---|---|---|---|
| V0*（重新实现的公式） | Actor的长宽/速度模长/yaw；Ego中心点位置与速度模长，Static+Dynamic Gaussian，逐时空间强度，再做Mean/Peak | 已本地运行；从历史交接所述核写成；**未获取原 `mcts_planner/risk_field.py` 验证bitwise parity**，且当前点位为**车辆中心而非原风险后轴接口** | 不能称真实 V0 精确复现；无法把结果直接与历史 SimWAM PDMS 对齐 |
| WU-TS（Wu逐时核最小版） | 单个记录未来模式 `p=1`，以 Eq7-9 建立同一未来时刻字段，给Ego对应时刻中心采样，Mean/Peak | 原论文公式已PDF核实+本地运行；作者预测与MPCC**均未运行** | 无概率预测校准；漏掉TRTP真实性能；不解决单点Ego footprint 与低速yaw的全部问题 |
| GEOM（同步完整占用） | Ego和周车同刻的有向矩形多边形；精确 Shapely minimum polygon gap [m] | 本地运行，数学定义与CriMe DCE类机制一致，**没有直接调用CriMe库** | 距离没有制动/人体感知语义；值0不区分点触碰与大面积穿透 |

**运动安全裕度**：受控纵向案例另用 `b_req=(max(v_e-v_f,0))²/(2 gap)`（解析简化公式），**不是 CriMe BTN/RSS 的同调用复现**；并且不能直接用于路口横向接近。DRF/GDRF 未在本轮实现：缺确证的可转入任意 Ego 候选的源实现和参数，绝不用自造Gaussian冒充DRF。文献候选实施优先级已调整为 V0、DRF/GDRF、Wu时间分层、几何+合法纵向制动四组，实际第一批**计算到三组+制动解析**。

## 3. 真实 INTERACTION 片段：数值已运行

采样：源文件四车 `ID=70,71,72,73`，记录帧 `2820..2880`，按5帧取一次，即13点×0.5秒，共6秒；原始字段 `track_id/frame_id/timestamp_ms/x/y/vx/vy/psi_rad/length/width`。车70作Ego，余3车Actor。全部 Actor `t>0` 状态来自**已记录未来**。另对Ego原记录几何横向偏移 `-1m/0m/+1m` 得到**人为构造的三个几何候选**：只作为同参数敏感性试验，不保证与原环境一致的动力学/道路可行，也绝不称来自SimWAM。

| Ego 横移 | V0* Mean | V0* Peak | Wu-TS Mean | Wu-TS Peak | 最小几何间隙[m] |
|---|---:|---:|---:|---:|---:|
| -1m | 0.036313 | 0.270529 | 0.000284 | 0.001056 | 2.487141 |
| 0m (原记录) | 0.048650 | 0.461311 | 0.001984 | 0.008685 | 1.621020 |
| +1m | 0.083529 | 0.620454 | 0.009929 | 0.046444 | 0.754899 |

在**这一条**实测片段和**这三个**人工横移候选里，三种方法的偏好方向一致（-1m 较远、+1m 较近），故**没有证据显示 Wu 比 V0 选轨更优秀**。三列风险绝对数不校准，不可直接比较数值大小。

原记录 Ego(0m)关键时间点：

| t[s] | 同刻完整车身最小距离[m] | V0* Total |
|---|---:|---:|
| 2.0 | 2.10567 | 0.00008 |
| 2.5 | **1.62102**（最近时刻） | 0.00138 |
| 3.5 | 2.60462 | 0.01468 |
| 4.5 | **9.29654**（已远离） | **0.46131**（最大风险） |
| 5.0 | 13.96256 | 0.08865 |

**本轮新异常证据**：V0*峰值落在双方间隙扩大的阶段，而不是本轮最近几何接触时。该结果可能来自Actor纵轴动态伸长+sigmoid门控+速度差变化，不能简单定性为不安全模型；但它是明确的**风险与物理相遇时刻偏离**，须核原类参数/参考点、其他 Actor 主导权与本模型预期风险语义。Wu-TS原记录最高约0.00869发生在t=3.5s，仍晚于最近距离2.5s；说明“逐时高斯”也不是“真实最小间隙函数”，只是缓解两者时间失配机制。所有比较仅该13时间点，无真实事故标签。

图件：`trajectory_risk_pilot_R1/real_interaction_six_panels.png`（上V0*、下Wu-TS，每行在t=0/2/4秒采用各自行内固定Jet颜色标尺，**不跨模型强制相同数值范围**）；`real_risk_vs_gap.png`（同刻风险与车身间隙双纵轴）；不强迫几何法画成风险热力图。

## 4. 独立受控单因素试验（已运行数值）

| 对照 | 固定条件、改变因素 | 可观测结果 | 解释/证据级别 |
|---|---|---|---|
| 静止锥桶 yaw | 椭圆近似小物体长0.4、宽0.3m，Actor速度0、Ego速度8m/s，固定查询(-10,0)、只改 Actor yaw 0→90度 | V0*查询约 **0.957497→数值下溢到0** | 静物任意方向触发伪风险条带的机制反例；**合成、已执行**。真实锥桶应按无向物理占用处理 |
| 小物体碰车头 | Ego全车身5×2m，锥桶中心(2.45,0)，长度/宽度0.15m，Ego和目标都静止，V0中心查询 | 多边形距离 **0m**；V0*中心点风险约 **1.33e-90** | 单参考点并非车身碰撞判据；**合成、已执行** |
| 同路径的路口同/错时 | 两车同样横竖线轨迹，Actor过冲突点推迟2秒，各以半径0.2m圆形表示，占用判定同步 | 同时通过最近中心距离 **0m**，错时约 **1.4142m**，边界最短距离 **1.0142m** | 仅路径覆盖不含真实相遇时间；**合成、已执行** |
| 同/错时的 Wu 切片 | 同上一测试的两种时序，示意 `a=2,b=0.75,gamma=1`，仅Actor t对应场（非真实预测） | 最大查询强度同时 **1.000**，错时 **0.4161**（仍有非零） | 时间分层可以区分同/错时，**但错时接近仍有Gaussian风险**，不等于概率或碰撞正确率 |
| 相同逼近速度，更短间隙 | 纯纵向同车道，闭合速度2m/s，间隙20→10m | 简化必要减速度 **0.1→0.2m/s²** | 确认运动安全对距离的单因素响应；不等于RSS完备响应模型 |
| 同速对向 | 两车速度模长均10m/s，方向相反 | 模长差=**0**，相对速度向量模=**20m/s** | 当前模长差不代表真正关闭速度，特别对向车辆 |

图件：`controlled_yaw_and_time.png`（上：同色标锥桶 yaw=0与90风险图；下左：两案同步物理距离，下右：Wu按未来相同时间查询风险）。**响应规则不应无条件要求单调**：只在固定相遇几何、动力学与信息协议后讨论闭合速度、距离、制动能力变化；当速度变化同时改接触时间时须按真实运动方程分析。

## 5. 第一批实施可行性（区分研究价值与工程成本）

| 方案 | 直接计算必要输入 | 算法核相对易用性 | 本轮真实情况 | 下一步最小约束 |
|---|---|---|---|---|
| V0 | 当前状态/yaw/尺寸/Ego查询/速度 | 很低（标量算子） | 仅公式复刻已跑，**严格原源码对齐待办** | 仅核单Actor函数hash、坐标点/速度语义；不重跑SimWAM |
| 同刻全车身 DCE | 车辆尺寸/yaw/未来同步位姿 | 低（Shapely几何） | **已跑** | 检查0.1/0.5s离散时间漏峰；真实多样本对照 |
| Wu-TS | 各Actor未来时刻位置/航向、模态及权重 | 场核低，真实预测器高 | Eq7–9单GT模式已跑 | 替换为**同一CV输入**、多模态预测另分列；禁止GT未来当部署优势 |
| BTN/RSS 纵向 | 同车道、有效间隙、当前速度、反应期、可用刹车 | 纵向解析低、正式接口中等 | 只跑制动简式 | 必须引入合法车道对齐及真正RSS/BTN实现才能做算法级评价 |
| DRF 2020/GDRF 2024 | 候选前瞻路径、风险后果、作者校准 | 方法研究高、复刻中高 | **没有实际实现** | 获得原作者MATLAB/GDRF公式与参数，先验证一条候选映射后再并排比较 |
| IR 2025 | 多模态轨迹的方向场和二维重叠 | 实施中高 | 没跑 | 时间混淆已证结构风险；非近期首选 |
| Frenetix 概率 | 可校准未来分布和车身 + native成本接口 | 中高 | 未核 C++ | 无需近期建成，只保留备选 |
| RADIUS/2026主观IRL | FRS资产/优化器或示范训练权重 | 高 | 没跑 | 暂不实现 |

**运行开销边界**：在当前 Python+Shapely 非矢量化实现中，对同一13时间步、3个人为候选、3个Actor，总计117个候选-Actor-时刻查询，反复计时得到单轮约 **0.034–0.038秒**；这是脚本端到端计算时间（包含DataFrame操作、Polygon创建），**不是三个算法分别测速、更不是车载部署时延**。Wu二维热图额外使用131×145网格，可视化与轨迹查询成本也不能混计。

## 6. 执行命令及可复现源

本轮交付 `trajectory_risk_pilot_r1.py`、脚本生成3幅PNG、`real_candidate_summary.csv`、`real_trajectory_time_series.csv`、`controlled_diagnostics.json`；输入样本子集文件为 `interaction_sample_70_73_2820_2880.csv`。安装依赖本环境已有 `numpy,pandas,shapely,matplotlib`，本轮没有新安装。复现命令：

```bash
python trajectory_risk_pilot_r1.py --csv interaction_sample_70_73_2820_2880.csv --out trajectory_risk_pilot_R1
```

脚本也能接收上游完整 `vehicle_tracks_000.csv`，运行时自动选取上述帧和车辆；样本来源 GitHub 的确切路径/Blob见开头；**只对该原始CSV格式与本固定场景做测试，尚非通用场景加载器**。如需完整复现 Wu TRTP/CARLA、原Gaussian Bitwise、DRF原作、真实大规模样本，仍需相应独立证据，不可将这一批可视化当作最终优效评价。

## 7. 验收建议与研究停止条件

本轮暂不认定胜者。请先人工查看：A 实测 t=2.5s车身最近 vs t=4.5s V0*的风险峰值是否体现合理预警；B Wu 时间场错时通过依然非零是否符合“近距离但不碰撞仍有主观风险”的目标；C 静止障碍物的yaw旋转是否必须具有风险不变性；D 三种横移候选只反映间隙大小，没有体现不同驾驶意图，是否值得再补**一条**真实急刹或 Cut-in 案例。

此后才判断是否进入更大真实样本：**优先原始V0源码逐值校验、独立风险语义、同预测输入的比较**；不要把 GT未来较好、调Gaussian参数、改PDMS或造大候选集合等混进这批结论。31仓审计原包和IR `main.md` 的未复得状态保持不变。