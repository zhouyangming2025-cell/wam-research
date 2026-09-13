# NEW_SESSION_PROMPT

Copy/paste this into a fresh GPT-5.6 Sol session:

```text
接管我的 private GitHub repo：zhouyangming2025-cell/wam-research。

不要让我重复旧聊天，也不要从记忆猜当前状态。先通过 GitHub 连接依次读取：
1. START_HERE.md
2. state/CURRENT_STATE.md
3. state/NEXT_TASK.md
4. state/RESEARCH_PRINCIPLES.md
5. landscape/FIELD_RECONSTRUCTION_PLAN.md
6. landscape/FIELD_ATLAS.md

读完后先用不超过 10 行告诉我：
- 当前研究 north star；
- 当前 active stage；
- P1/P2-R/P3 现在是什么地位；
- 当前唯一下一任务；
- 目前禁止做什么。

然后直接继续当前任务。

非常重要：当前阶段不是 gap hunting。不要围绕 P2-R 搜论文，不要提前设计方法，不要强行把 risk field 塞进方案。当前任务是先彻底重建 World Model + End-to-End + Planning-centric 自动驾驶领域的技术版图：方法家族、历史演化、world representation、future supervision、action conditioning、interaction/reactivity、planner coupling、planning output、evaluation regime、strong non-WM baselines、benchmark effects、trade-offs 和 counterexamples。

先做 50–80 篇左右的 field census（只需要 placement/overview depth），再选 15–25 篇 representative anchors 深读。只有 field atlas 稳定后才允许重新讨论研究问题/gap。

科研判断必须遵守 state/RESEARCH_PRINCIPLES.md，并在本轮产生实质性进展后直接更新 GitHub Research Brain。
```

Expected recovered state when this prompt was created:

```text
North star = World Model + End-to-End + Planning-centric
Active stage = FIELD RECONSTRUCTION — Planning-centric WAM Atlas
P1 = retired historical hypothesis
P2-R = parked probe, not active target
P3 = parked backup probe
Next = build neutral field census, then select anchor deep reads
No method design / no formal gap declaration yet
Risk field = optional asset, not destination
```

If the repo later changes, the live repo state wins; this snapshot is only a sanity check.
