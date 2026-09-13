# NEW_SESSION_PROMPT

Copy/paste this into a fresh GPT-5.6 Sol session:

```text
接管我的 private GitHub repo：zhouyangming2025-cell/wam-research。

不要让我重复旧聊天，也不要从记忆猜当前状态。先通过 GitHub 连接依次读取：
1. START_HERE.md
2. state/CURRENT_STATE.md
3. state/NEXT_TASK.md
4. hypotheses/P2R_PRIMARY.md
5. handoff/LATEST.md

如果需要理解此前跨论文证据，再读 evidence/CORE_EVIDENCE_SNAPSHOT.md；如果需要决策历史，再读 state/DECISION_LOG.md。不要默认把整个 corpus 全部读进上下文。

读完后先用不超过 10 行告诉我：
- 当前研究 north star；
- P1/P2-R/P3 状态；
- 当前最重要的科学结论；
- 唯一下一任务；
- 目前禁止做什么。

然后直接继续当前任务，不要重新做 broad literature survey，不要提前设计方法，不要强行把 risk field 塞进方案。科研判断必须遵守 state/RESEARCH_PRINCIPLES.md，并在本轮产生实质性进展后直接更新 GitHub Research Brain。
```

Expected recovered state at the time this prompt was created:

```text
North star = World Model + End-to-End + Planning-centric
P1 = RETIRED AS MAIN
P2-R = PRIMARY CANDIDATE, NOT CONFIRMED GAP
P3 = HOLD AS BACKUP
Round 1 = no direct observed P2-R failure established
Next = ingest + deep-read frozen targeted set A1–A5 + H1–H3
No method design yet
Risk field = optional asset, not destination
```

If the repo state later conflicts with the expected snapshot above, the repo state wins; this file's snapshot is only a sanity check.
