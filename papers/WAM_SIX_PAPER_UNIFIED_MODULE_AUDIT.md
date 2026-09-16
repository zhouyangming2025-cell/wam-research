# 六篇 WAM 论文：一条共同路线，三种“使用未来”的方式

> LAW / Epona / DriveLaW / World4Drive / WorldDrive / WoTE 统一理解稿
> 目标：帮助理解论文之间的关系，而不是罗列论文模块
> 更新时间：2026-09-16

---

## 0. 先给结论：这不是六种路线

六篇论文都可以放进同一条完整规划链：

```text
历史观测
   ↓
当前世界状态 S
   ↓
生成轨迹提议 A
   ↓
预测执行 A 后的世界后果 O(A)
   ↓
评价 V(A)
   ↓
选择最终轨迹 A*
```

论文之间真正的区别，不是各自发明了一套完全不同的路线，而是：

1. 做到了这条链的哪一段；
2. “未来信息”在哪个位置进入；
3. 未来只在训练时教模型，还是在推理时真的参与决策。

六篇论文中的未来信息只有三种基本用法：

```text
用法 A：未来作为训练教师
       用未来观测监督模型，使当前状态 S 更具有未来可预测性

用法 B：未来生成过程作为在线表示
       规划器在推理时读取未来生成模型的内部计算状态 U

用法 C：未来作为候选轨迹的预测后果
       对每条候选 Ak 预测 O(Ak)，再根据 V(Ak) 选择
```

对应关系是重叠的，而不是六选一：

```text
用法 A：LAW、Epona、DriveLaW 的视频预训练、World4Drive、WorldDrive
用法 B：DriveLaW
用法 C：World4Drive、WorldDrive、WoTE
```

WoTE 也有未来状态监督，但它的主要意义在用法 C，即“轨迹生成之后如何评价”，而不是重新发明历史图像编码方式。

因此，最适合阅读这六篇论文的结构是：

```text
LAW / Epona              研究未来怎样教会当前表示
DriveLaW                 研究能否直接读取未来生成过程
World4Drive / WorldDrive 研究怎样用候选未来选择轨迹
WoTE                      把候选展开、评价和选择做成主要系统
```

这不是能力等级，也不是按时间排列的技术演进；它是同一条计算链上的位置关系。

---

## 1. 先统一语言：全文只使用五个核心对象

不同论文分别使用 latent、feature、token、BEV、hidden state、world representation 等词。为了比较，正文统一翻译成下面五个对象。

### 1.1 当前状态 `S`（current state）

由历史图像、历史运动、导航信息等编码得到。无论论文称它为 visual latent、`F`、physical latent 还是 BEV feature，只要它表示“作出当前决策前，模型对当前场景的压缩”，本文都叫 `S`。

### 1.2 未来目标 `T`（future target）

训练数据中实际发生的未来观测，经编码后得到的监督目标。它通常只有一条，因为日志中只发生了一种未来。

### 1.3 在线内部状态 `U`（online internal state）

未来生成模型在完成预测之前产生的中间计算状态。`U` 不是已经预测完成的未来，只是生成过程中的信息载体。

### 1.4 轨迹 `A`（action / trajectory）

可以是一条直接输出的轨迹，也可以是同时存在的候选集合：

```text
{A1, A2, ..., AK}
```

### 1.5 候选后果 `O(Ak)` 与价值 `V(Ak)`

`O(Ak)` 表示：“如果执行第 k 条轨迹，模型认为世界会变成什么样。”

`V(Ak)` 表示：“根据这个后果，第 k 条轨迹有多值得选择。”

论文原始术语只在需要定位源码或公式时保留：

- LAW 的 `V_t` 统一视为 `S`，`V_{t+1}` 视为 `T`。
- Epona 的共享历史表示 `F` 统一视为 `S`。
- DriveLaW 的 Video-DiT block hidden states 统一视为 `U`。
- World4Drive 的 `L_t` 视为 `S`，每个 `L_{t+n}^k` 视为 `O(Ak)`。
- WorldDrive 的 teacher/student future scene latent 视为 `O_teacher(Ak)` / `O(Ak)`。
- WoTE 的当前 BEV 视为 `S`，候选未来 BEV sequence 视为 `O(Ak)`。

后文不再因为各论文命名不同，就把同一种计算功能写成六种东西。

---

## 2. 共同起点：未来图像究竟教会了什么？

你的原始理解可以写成：

```text
历史观测 → 当前表示 S
未来观测 → 未来目标 T

模型从 S 预测 T
预测误差反向传播
于是 S 更有能力表达与未来演化有关的信息
```

这个理解作为第一层抽象是正确的，但“学好的 latent 充分表达未来”说得太强。

训练真正保证的是：

> `S` 对训练目标 `T` 更具有可预测性（future-predictive），而不是 `S` 已经包含唯一、完整、真实的未来。

原因有三点：

1. 同一个当前场景本来就可能有多种未来；
2. 日志通常只提供其中实际发生的一条；
3. 模型还可能依靠纹理、路线先验、数据偏差等捷径降低 future loss。

因此，后面比较论文时，不问“谁的 latent 更聪明”，而问：

```text
future loss 更新了谁？
规划器推理时读取谁？
动作是否在预测未来之前进入？
预测的未来是否参与最终选轨迹？
```

编码器结构、噪声调度和 token 形状只有在改变这四个问题的答案时，才是路线级差异；否则它们主要属于实现细节。

---

## 3. 用法 A：未来作为训练教师

这一类方法的共同计算是：

```text
未来观测 ─────────────→ 目标 T
                         ↑ loss
历史观测 → 当前状态 S → 未来预测器 → T_hat
              │
              └────────→ 规划器 → 轨迹 A
```

未来观测只在训练时出现。实际开车时没有未来图像，系统依靠被 future loss 塑造过的参数作出当前规划。

### 3.1 LAW：未来 loss 会经过模型自己预测的动作

LAW 的统一计算图是：

```text
历史图像 → S → 规划器 → 一条预测轨迹 A
              │              │
              └──── S + A ───┘
                         ↓
                   预测未来 T_hat
                         ↓
                与事实未来 T 对齐
```

这里最重要的不是 latent 用什么编码器，而是 `A` 的位置：

> LAW 先预测当前轨迹，再把这条轨迹放进未来预测器。

所以 future loss 不仅训练未来预测器和 `S`，还可以沿 `A` 这条路径约束轨迹预测。这是 LAW 所谓 action-aware 的实质。

部署时则是：

```text
历史图像 → S → 规划器 → A
```

预测出来的 `T_hat` 不参与当前轨迹选择。锁定源码审计还确认，事实 future target 分支被 detach；它是监督目标，不是另一个可被共同优化的输入。[论文原文][LAW-P] [接口审计][LAW-S]

一句话：

> LAW 用“我预测的这条轨迹能否解释接下来的事实世界”来训练当前规划器，但实际部署不在线预测未来。

### 3.2 Epona：未来任务和轨迹任务共享 `S`，但互为并列分支

Epona 的统一计算图是：

```text
历史图像与历史运动 → S
                     ├→ 轨迹生成器 → A          → trajectory loss
                     └→ 视觉未来生成器 → T_hat  → future visual loss
```

两条分支共享 `S`，所以视觉 future loss 会训练 `S`，而轨迹生成器也读取同一个 `S`。

但它与 LAW 有一个决定性区别：

```text
LAW： 预测轨迹 A → 进入 future predictor → future loss 可以沿 A 约束规划路径

Epona：轨迹生成器和视觉生成器并列
       视觉分支训练时使用事实 ego motion
       不使用 TrajDiT 刚预测出的 A
```

因此，Epona 的 visual loss 影响规划的主要通路是：

```text
visual loss → 共享状态 S → 轨迹生成器的输入质量
```

而不是：

```text
visual loss → TrajDiT 的预测轨迹 → 直接修正这条轨迹
```

部署做规划时，源码调用 `traj_only=True`，视觉未来分支可以完全不运行。[论文原文][EPONA-P] [源码审计][EPONA-S] [核心 forward][EPONA-CODE]

一句话：

> Epona 用视觉未来生成和轨迹生成共同训练一个历史状态 `S`，规划时只保留“`S` → 轨迹”这条分支。

### 3.3 LAW 与 Epona 到底是不是同一件事？

是，同一层面上它们都在做：

> 用未来观测提供辅助监督，使当前规划表示更有预测性。

但它们的耦合方式不同：

```text
LAW：   future loss 与“模型自己预测的动作”相连
Epona： future loss 与 trajectory head 只通过共享状态 S 相连
```

这比“LAW 是 latent prediction，Epona 是双任务”更有比较价值，因为它直接说明 future loss 怎样影响 planner。

### 3.4 另外三篇也包含用法 A，但不止于此

- DriveLaW 先通过视频生成学习未来演化表示，但推理时还会在线运行生成模型，因此不能只归入训练辅助。
- World4Drive 用事实 future target 训练候选未来预测器和 selector，并让候选未来在线参与选择。
- WorldDrive 用 future video generation 预训练视觉/运动表示，再把这些表示继承给 planner；随后还增加候选评价器。

所以 LAW/Epona 是最纯粹的“未来作为教师”；后三篇在这条基础上继续向后走。

---

## 4. 用法 B：未来生成过程本身成为在线规划表示

### 4.1 DriveLaW 的关键不是“也预测未来视频”

DriveLaW 的统一计算图是：

```text
历史图像 + future-noise slots + 历史运动/导航
                    ↓
          Video-DiT 第一次去噪计算
                    ↓
       每一层产生内部状态 U1, U2, ...
                    ↓
       Action-DiT 逐层读取对应的 Ui
                    ↓
                输出轨迹 A
```

规划器读取的是 `U`，不是解码完成的未来视频，也不是最终预测好的未来 latent。

这使 DriveLaW 与 LAW/Epona 有本质区别：

```text
LAW / Epona：future branch 训练模型，部署时可以不运行

DriveLaW：Video-DiT 的第一次 future-generation computation
          是部署时 Action-DiT 的必要输入
```

DriveLaW 在 action training 阶段只优化 action flow loss；Action-DiT 对 `U` 的 cross-attention 没有 detach，因此该 loss 也可以继续调整 Video-DiT。[论文原文][DRIVELAW-P] [源码审计][DRIVELAW-S]

### 4.2 为什么它仍然不是候选未来评价？

因为 prospective trajectory 是在 `U` 产生之后，才由 Action-DiT 生成：

```text
Video-DiT → U → Action-DiT → A
```

而候选评价要求：

```text
A1 → O(A1)
A2 → O(A2)
...
AK → O(AK)
```

DriveLaW 没有把多条待比较轨迹回灌给 Video-DiT，也没有对不同后果打分。因此它是“在线未来计算辅助直接策略”，不是“用未来比较候选”。

### 4.3 还需不需要继续研究噪声怎么注入？

如果目标是理解六篇论文的路线关系，目前不需要把精力放在噪声 schedule、VAE token 排布等细节上。现在真正需要掌握的是：

1. future-noise slots 使 Video-DiT 启动一个面向未来的生成计算；
2. planner 在第一次去噪后就读取内部状态；
3. planner 不等待最终视频；
4. prospective trajectory 没有反过来生成 candidate-specific future。

只有准备复现 DriveLaW、研究为什么第一步优于后续 denoising steps，或准备改造它的接口时，噪声和编码细节才成为下一层重点。

---

## 5. 用法 C：为每条候选预测后果，再做选择

这一类论文共享同一条后半段：

```text
当前状态 S
   ↓
候选生成器 → {A1, A2, ..., AK}
                   ↓
      O(A1), O(A2), ..., O(AK)
                   ↓
      V(A1), V(A2), ..., V(AK)
                   ↓
                选择 A*
```

World4Drive、WorldDrive、WoTE 的共同点不是都使用某种 latent，而是它们都让 prospective candidate action 在未来预测之前进入，并让预测后果影响最终选择。

三篇真正不同的地方只有两个：

1. `O(Ak)` 怎样得到；
2. `V(Ak)` 到底在评价什么。

### 5.1 World4Drive：评价“哪种未来最像事实 future”

统一计算图：

```text
S → 6 条意图候选 {Ak}

S + Ak → 候选未来 O(Ak)

训练日志只提供一个事实未来 T

j = 与 T 最接近的 O(Ak)

用 j 训练 mode scorer
```

因此，World4Drive虽然为 6 条轨迹生成 6 个未来，但它没有 6 条真实反事实 future 作为监督。它只有一个事实 future，让 6 个 mode 竞争谁最接近这条事实。

它的 scorer 更准确的语义是：

> 哪个候选 future 最像训练数据中实际发生的模式？

而不是：

> 哪条轨迹在安全、舒适、进度等方面具有最高真实价值？

论文规定推理时选择 ScoreNet 最高分的候选。[论文原文][WORLD4DRIVE-P]

但锁定公开源码存在重要不一致：源码确认了 6 个 future features、`wm_cls_head` 和 focal loss；公开 `simple_test_pts` 却没有使用 `pred_img_cls` 做最终 argmax，而是根据已观测当前特征计算上一时刻候选的 reconstruction/KL/cosine 最小索引。[future/head 源码][WORLD4DRIVE-HEAD] [推理源码][WORLD4DRIVE-INFER] [源码审计][WORLD4DRIVE-S]

所以当前最严格的表述是：

> “候选 future + ScoreNet selection”是论文明确机制；公开仓库确认了 head 和训练 loss，但没有完整确认论文所述的在线 final selection。

### 5.2 WorldDrive：用重型 world model 当离线教师，在线只留轻量评价器

WorldDrive有前后两段。

第一段先学习表示：

```text
历史视频 + 轨迹条件
        ↓
重型视频 world model
        ↓
学习视觉表示和运动表示
        ↓
把这些表示继承给 base planner
```

第二段评价候选：

```text
base planner：256 anchors → 初步筛选 → top-K（默认 5）

训练：
S + Ak → 重型 teacher world model → O_teacher(Ak)
S + Ak → 轻量 student FAR       → O(Ak)

student 对齐 teacher future
同时学习 PDMS/oracle candidate preference

推理：
只运行 student FAR → V(Ak) → 选择 A*
```

这里必须分开两种监督：

```text
future latent alignment：教 student 模仿 teacher 认为的候选后果

PDMS preference：教 scorer 哪个候选在 benchmark 规则下更好
```

因此，WorldDrive并不是“预测 future 越准就自然知道选谁”。它把 world-model teacher 和外部 value supervision 组合在一起。[论文原文][WORLDDRIVE-P] [源码审计][WORLDDRIVE-S] [FAR 源码][WORLDDRIVE-CODE]

一句话：

> WorldDrive把昂贵的候选未来生成放到训练期，再把候选后果和 PDMS 排序能力蒸馏进在线轻量评价器。

### 5.3 WoTE：直接在线展开大量候选，并预测明确规划 reward

WoTE从当前 BEV 状态开始：

```text
当前 BEV 状态 S
       ↓
生成并修正 256 条候选 {Ak}
       ↓
对每条 Ak 递归预测未来 BEV 序列 O(Ak)
       ↓
根据当前/未来 BEV 和 Ak 预测：
碰撞、可行驶区域、TTC、舒适性、进度、模仿等 reward
       ↓
选择综合 reward 最高的轨迹
```

这正是完整路线的后半段：proposal → rollout → reward → selection。

WoTE与 World4Drive 的差别，不是 BEV 和图像 latent 的表面差别，而是 scorer 的含义：

```text
World4Drive：哪一个 mode 最接近唯一事实 future

WoTE：每条候选在多个规划指标上会得到什么结果
```

WoTE与 WorldDrive 的差别是：

```text
WorldDrive：重型生成 teacher 离线产生候选后果知识，轻量 student 在线评价

WoTE：紧凑 BEV world model 直接在线递归展开 256 条候选
```

WoTE的关键边界也很清楚：在已审计的 target-generation path 中，每条 ego 候选会得到不同的 ego rollout 和 reward，但周围交通参与者使用同一条缓存的日志 future，不会针对不同 ego 候选重新反应。[论文原文][WOTE-P] [接口审计][LAW-S]

所以 WoTE实现的是：

> 固定周围车辆未来条件下的 ego candidate evaluation。

它还不是行为正确的多智能体反事实模拟。

### 5.4 三篇候选评价方法的统一差异

可以只记住三句话：

```text
World4Drive：用唯一事实 future 教模型“哪个候选模式最像发生过的未来”

WorldDrive：用生成 teacher 教候选后果，再用 PDMS 教候选偏好

WoTE：用 simulator-derived targets 教每条候选的显式规划 reward
```

这三句话已经比记住 ScoreNet、FAR、BEV reward head 等论文专有名词更接近真正的算法区别。

---

## 6. 六篇论文在共同路线上的位置

现在可以把六篇放回一条链，而不是画成六条路线：

```text
                 未来信息怎样进入规划
                          │
          ┌───────────────┼────────────────┐
          │               │                │
     训练时塑造 S      在线读取 U       在线比较 O(Ak)
          │               │                │
     LAW / Epona       DriveLaW      World4Drive
          │                               WorldDrive
          │                                  WoTE
          └──── World4Drive / WorldDrive 也包含表示学习 ────┘
```

更精确地说：

- LAW、Epona主要完成“历史状态怎样接受未来监督”。
- DriveLaW把读取点推进到在线 future-generation process 内部，但仍直接输出单条策略。
- World4Drive、WorldDrive把表示学习和候选未来评价接在一起。
- WoTE主要实现后半段，并用低成本 BEV 支撑大量候选展开。

因此 WoTE不是应该排除的异类。它补上的是大路线中的后半段，只是没有把视觉 future representation learning 当作主要叙事。

---

## 7. 回答五个真正决定路线的问题

### 7.1 未来信息在哪里产生？

- LAW：在辅助未来预测器中产生 `T_hat`；planner部署时不读取它。
- Epona：在视觉未来生成器中产生 `T_hat`；轨迹分支读取的是生成之前的共享 `S`。
- DriveLaW：在 Video-DiT 第一次去噪过程中产生 `U`；planner在线读取 `U`。
- World4Drive：在候选轨迹之后产生 6 个 `O(Ak)`。
- WorldDrive：训练时由重型 teacher 产生候选后果，部署时由轻量 student 产生。
- WoTE：对每条候选在线递归产生 future-BEV sequence。

### 7.2 动作在哪里进入？

- LAW：模型自己的单条预测轨迹进入辅助未来预测器。
- Epona：视觉分支训练时使用事实 ego motion；预测轨迹分支与它并列。
- DriveLaW：Video-DiT先产生 `U`，Action-DiT随后生成轨迹；不存在 candidate action → candidate future 回路。
- World4Drive、WorldDrive、WoTE：候选轨迹先产生，再分别进入未来/后果模型。

所以“模型使用了 action condition”仍然不够。真正的分界是 action 是历史运动、单条自预测动作，还是待比较的 K 条 prospective candidates。

### 7.3 未来是否在线消费？

```text
LAW / Epona：否，主要留下训练后的参数影响
DriveLaW：是，消费未来生成过程内部状态 U
World4Drive / WorldDrive / WoTE：论文机制上是，消费候选后果 O(Ak)
```

World4Drive的公开推理代码等价性除外，当前保持 partial。

### 7.4 未来是否直接参与选择？

- LAW、Epona：不参与，没有 future-based candidate selector。
- DriveLaW：影响直接策略生成，但没有候选间选择。
- World4Drive、WorldDrive、WoTE：参与，因为不同 `O(Ak)` 会进入可比较的分数。

### 7.5 监督是否是真实反事实？

六篇都没有获得这样的真实监督：

```text
在完全相同的初始世界中，
真实执行 A1、A2、...、AK，
并分别观测所有交通参与者如何响应。
```

它们拥有的是：

- LAW/Epona：一条事实 future；
- World4Drive：一个事实 target 对多个模型输出；
- WorldDrive：teacher 生成的候选 future；
- WoTE：不同 ego 候选面对固定的 logged-agent future；
- DriveLaW：没有候选专属 future branch。

所以这些论文可以学习有用的 prospective planning evidence，但不能直接宣称已经学到真实、可干预、具有交通参与者反应性的反事实世界模型。

---

## 8. 重新精读时，每篇只抓一个接口

现在继续读论文时，不需要平均用力。

### LAW

只追踪：

```text
预测轨迹 A → future predictor → future loss → 梯度回到哪里？
```

不要把主要精力放在 future latent 的具体维度上。

### Epona

只追踪：

```text
共享状态 S → TrajDiT
共享状态 S → VisDiT
两条 loss 在哪里相遇？哪里没有相遇？
```

视频能否漂亮解码不是规划机制的核心。

### DriveLaW

只追踪：

```text
Video-DiT 的哪个时刻产生 U？
Action-DiT怎样逐层读取 U？
action loss 是否更新 Video-DiT？
```

噪声注入和编码细节先放到复现阶段。

### World4Drive

只追踪：

```text
Ak → O(Ak)
唯一事实 T 怎样给 K 个 mode 分配标签？
训练时的 mode label 与推理时的选择是否一致？
```

尤其要保留论文 ScoreNet 与公开 `simple_test_pts` 的实现差异。

### WorldDrive

只追踪：

```text
teacher future 教了什么？
PDMS preference 又教了什么？
部署时到底留下哪些 student 模块？
```

不要把 latent distillation 与 value learning 混成一个 loss。

### WoTE

只追踪：

```text
候选怎样生成？
future BEV 怎样按候选展开？
reward 的监督来源是什么？
周围车辆是否会随 ego candidate 改变？
```

这四个问题就是 WoTE的主体。

---

## 9. 对原始直觉的最终修正

原始直觉是：

> 用未来图片监督，把编码器训练得更聪明；推理时这个 latent包含未来信息，再帮助 planner规划。

修正后的统一说法是：

> 六篇都用未来数据或未来计算改善规划，但未来与 planner 的接口不同。
>
> LAW/Epona主要把未来知识写进当前状态的参数；DriveLaW在线读取未来生成过程的内部状态；World4Drive/WorldDrive/WoTE则为候选轨迹构造未来后果，并让这些后果影响选择。

这一区分不能再简化，否则就会把三个不同机制混为一谈：

```text
future-supervised current representation
≠ online future-generation hidden state
≠ candidate-conditioned future consequence
```

同时，三者也不是彼此排斥的路线。World4Drive和WorldDrive正是把表示学习与候选评价组合起来的例子。

---

## 10. 下一步真正值得横向研究什么？

不建议继续用大量篇幅比较各论文怎样把图片编码成 latent。更有价值的是在同一实验框架中隔离以下问题。

### 10.1 future supervision 是否真的学习了动态？

保持数据、模型、参数量和训练步数不变，只打乱 future target 与历史样本的对应关系。如果规划收益仍存在，说明一部分收益可能来自正则化或额外训练，而不是真实时序结构。

### 10.2 `S`、`U`、`O(A)` 哪个接口真正有用？

在同一 backbone 下分别让 planner 读取：

```text
当前状态 S
生成过程内部 U
完成的候选后果 O(A)
```

这样才能比较 LAW/Epona、DriveLaW、candidate evaluator 三种接口，而不是比较六套不同 backbone。

### 10.3 候选质量和评价质量分别贡献多少？

固定完全相同的候选池，再替换：

```text
无 future evaluator
mode-matching evaluator
teacher-distilled evaluator
explicit reward evaluator
```

否则 WorldDrive/WoTE增加候选数后变好，可能只是 proposal coverage提高。

### 10.4 如何获得真正的 reactive counterfactual supervision？

需要交互式环境为同一初始状态生成不同 ego action 下的多智能体响应，而不是让所有 ego candidates 共用一条 logged-agent future。这是六篇共同没有解决的研究缺口。

---

## 11. 证据范围与版本边界

正文中的机制结论以本地论文原文为主，以锁定源码或源码审计确认关键接口。深度分析稿只用于定位，不作为最终事实来源。

- LAW：`BraveGroup/LAW@b2f6a784247072923c477ab92324d3aa5a9759bf`
- Epona：`Kevin-thu/Epona@69b24c55f5ab8b3ffde8fa55e9f833bfe64d2c68`
- DriveLaW：`xiaomi-research/drivelaw@243e0e41148bdb1ae39ce1adf17d026e7cbd4348`
- World4Drive：`ucaszyp/World4Drive@cffb51adeb1f7d02b49c4b74d7262ded62a33ac8`
- WorldDrive：`TabGuigui/WorldDrive@c375ee1e1fe86ace175609db1ed90fd6db89673b`
- WoTE：`liyingyanUCAS/WoTE@298957c128a91d41a1c6075bd0bb6e7e845e093f`

保留两项版本边界：

1. DriveLaW当前公开代码晚于论文提交，精确 benchmark reproduction仍为 partial。
2. World4Drive公开 nuScenes推理路径与论文 ScoreNet selection不一致，NAVSIM分支的实现等价性也未闭合。

---

[LAW-P]: raw_md/P0048_LAW/P0048_LAW.raw.md
[EPONA-P]: raw_md/P0001_Epona/P0001_Epona.raw.md
[DRIVELAW-P]: raw_md/P0009_DriveLaW/P0009_DriveLaW.raw.md
[WORLD4DRIVE-P]: raw_md/P0046_World4Drive/P0046_World4Drive.raw.md
[WORLDDRIVE-P]: raw_md/P0042_WorldDrive/P0042_WorldDrive.raw.md
[WOTE-P]: raw_md/P0045_WoTE/P0045_WoTE.raw.md

[LAW-S]: ../audits/literature/PHASE_B_WAVE2_INTERFACE_CODE_AUDIT.md
[EPONA-S]: ../audits/literature/PHASE_C5_EPONA_SOURCE_AUDIT.md
[DRIVELAW-S]: ../audits/literature/PHASE_C6_DRIVELAW_AUDIT.md
[WORLD4DRIVE-S]: ../audits/literature/PHASE_C5_WORLD4DRIVE_AUDIT.md
[WORLDDRIVE-S]: ../audits/literature/PHASE_C5_WORLDDRIVE_AUDIT.md

[EPONA-CODE]: ../repos/Epona/models/model.py
[WORLD4DRIVE-HEAD]: ../repos/World4Drive/projects/mmdet3d_plugin/W4D/dense_heads/waypoint_query_decoder_simple.py
[WORLD4DRIVE-INFER]: ../repos/World4Drive/projects/mmdet3d_plugin/W4D/W4D.py
[WORLDDRIVE-CODE]: ../repos/WorldDrive/navsim/agents/worlddrive/worlddrive_refiner.py
