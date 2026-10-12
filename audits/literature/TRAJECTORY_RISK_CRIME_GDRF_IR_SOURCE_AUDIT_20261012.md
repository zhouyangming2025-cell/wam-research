# 候选轨迹风险评价：第二轮源码级机制审计与反例核验

日期：2026-10-12。**状态：专项证据记录，非路线结论、非最终模型、非新增主程序入口。** 交接依据：`Gaussian_Risk_Field_Research_Full_Handoff_2026-10-12_CN(1).md` 和本会话第一轮 `Trajectory_Risk_Literature_Survey_R1_2026-10-12_CN.md`。其中旧 SimWAM 结果仅为交接记录，本轮**没有**重跑 NAVSIM、SimWAM、Gaussian V0/V1/V2，也没有读取用户之前审计的31仓本地包。

## 0. 本轮可确认的决策相关增量

1. **CommonRoad-CriMe 不只是 README 上的指标名录。** 已在官方 GitHub `develop` 读取 DCE、TTCE、TTC、TTCStar、ALongReq、BTN、TTM/TTR、P_MC 的实际计算函数，留存单文件 blob SHA 与逐文件 URL。既有库可作为原理/复用参考，但需要场景格式适配、指标语义核查，不能把所有 `Criticality` 视为可直接接 NAVSIM K 条轨迹的统一安全分数。
2. **同步几何距离是相对于原 Gaussian V0 的独立信息来源**：DCE 按同一时间步查询**完整多边形**间距离；TTCE 从最近距离时间读出时间。它直接补全原 V0 后轴单点漏检，但不说明名义无碰撞时的制动危险或主观不安。
3. **`TTC` 与 `TTCStar` 是两条实现路线**。普通 `TTC` 使用车道/纵向间距、加速度公式；`TTCStar` 用给定 Ego 轨迹、旋转矩形和 collision checker 做时间步检测。且 `TTCStar` 的 collision checker 还装有 road-boundary obstacle：**需要区分撞周车与触碰道路边界，不能盲目叫纯周车 TTC**。
4. **`TTR` 并非神奇通用风险概率**：它调用 `TTB`（BRAKE）、`TTK`（KICKDOWN/加速）、`TTS`（转向），由 TTM 的候选机动模拟与二分搜索求最迟启动时刻，再取 max。动作集、Ego动力学、预测 horizon、collision checker 均会改变值。
5. **`P_MC` 当前代码不等于“给定 Ego 轨迹上的周车多模态碰撞概率”**：它对 Ego 的 STOP/TURN/LANECHANGE/OVERTAKE/RANDOM 等机动做 Monte Carlo，调用 TTCStar 判断，并对碰撞样本的 pdf 结果 `np.average`。是否有合法归一化需核实其 `simulator.pdf` 定义；不能直接拿返回值当作已校准 `P(collision | candidate, multimodal actors)`。
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
| [`measure/probability/p_mc.py`](https://github.com/CommonRoad/commonroad-crime/blob/develop/commonroad_crime/measure/probability/p_mc.py) | 对 Ego 模拟多种动作，收集碰撞模拟的 `pdf_bundle[j]`，`np.average(colliding_prob_list)`；无碰撞样本返回0 | **不能直接当作固定 Ego candidate + 周车联合未来的经验碰撞比例**；必须核合法性、概率归一化与目标事件 | `3cf3787a9a01012187b985a4a743f0baf27b5e28` |
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

其中 \(z\) 是**周围交通的联合时序未来假设**，而不是“Ego 如果随机转向、制动、变道的样本”；真实项目还需预测器与校准证据，不能凭式子称真实概率。`P_MC` 是采样 Ego 行为的另一种关键性定义，其在本轮读到的代码中 `np.average(colliding_prob_list)` 无法仅凭名字证明满足上述归一化。反例：若各碰撞样本 `pdf=0.2`，碰撞样本数量1和9都给 `0.2`；**只有在补充特殊密度权重语义后才可能解释，必须从 `Simulation*.pdf` 追到底层**。这是待查风险，不是给项目整体判错。

### 2.3 纵向 BTN 的控制算例（解析示意，不是运行 CriMe 的结果）

假定直线同车道、间隙 20m、前车恒速，Ego 纵向速度分别为 20m/s 和 30m/s，前车为 20m/s 或 10m/s；可用最大制动 6m/s²。理想化闭合速度为0时，当前维持速度无需额外减速；闭合速度20m/s时，避免追近所需等效制动 \(a_{req}=20^2/(2\times20)=10\,\mathrm{m/s^2}\)，BTN=10/6≈1.67，已超出设定制动能力（忽略反应时延将更乐观）。同样20m几何间隙，**制动可控性的信息不是几何距离单独提供的**。此式只用于一维且恒速前车；不能推广为路口全方向 BTN。

## 3. GDRF 2024 与 IR 2025：继续追索后的具体进展及限制

| 项目 | 确认的论文原文/出版社信息 | 尚未确认的决策关键问题 |
|---|---|---|
| [GDRF，Xia 等，TR-C 2024](https://www.sciencedirect.com/science/article/pii/S0968090X23004606)，DOI `10.1016/j.trc.2023.104470` | 原文出版社预览明确两组几何集合：`GDRF-D` 表示主观对未来车辆状态的担忧；`GDRF-E` 表示环境后果风险；作者称使用人类主观风险评价校准参数，处理多类目标/区域/相对运动，并通过多场景轨迹规划比较 THW/TTC/TLC | 两组集合的准确表达、形状交/并组合、风险归一化、是否同刻同步、校准对象/样本量/泛化及可开源复现情况：本轮没有全文章节与参数，**均不能擅自写公式** |
| [IR，Jiang 等，A&A Prevention 2025](https://www.sciencedirect.com/science/article/abs/pii/S0001457525003161)，DOI `10.1016/j.aap.2025.108228` | 出版社明确对比 2024 先前 DRP，承认先前没有 risk direction；2025提出 `IDRF` 引入方向性、`IR` 将不确定意图及事故概率/严重度关联，报告模拟+真实数据、四类应用 | 2025 完整 IR 的精确式子、方向项具体形状、时间轴是否显式同步、事故“probability”标定、是否独立于预测器更换、真实数据错误率：无全文不能判定 |
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
| `2025 IR已解决 EDRF 的全部时间问题` | 已确认方向性补充，但未知是否同刻同步；需原文 | 未见全文公式，不下结论 |
| `所有 Gaussian 得分都是概率` | 核是否归一化、随机事件和校准是额外条件 | V0, DRF, EDRF, Frenetix 都分别核 |

## 7. 下轮最小有效核验（只排序，不启动大型工程）

**最优先：两类来源证据**。第一是已核源码基础上查看 CriMe `P_MC` 的 Monte Carlo simulator `pdf` 怎样计算，尤其验证其碰撞概率含义；查 `TTCStar` road-boundary 与 collision 类型能否区分，验证 `ALongReq` 的零朝向 `if not` 条件及 DCE 在不同起始 time_step 下的坐标。第二是取得 **GDRF 2024 §2/§4、IR 2025 §3/§4** 的原文公式与实验（可接受仅有关章节），不偷填未知。其次才是 Frenetix C++ 的 probability cost 实现。

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

**证据等级**：CriMe 各指标为“真实源码正文已读，未跑测试”；Frenetix 为“官方 API 已读，C++实现未核”；GDRF/IR 为“出版社原文摘要与章节片段，公式未核”；错时案例为“本研究独立解析+CPU核算”；用户V0/SimWAM 数据为“交接史料，本轮未重跑”。