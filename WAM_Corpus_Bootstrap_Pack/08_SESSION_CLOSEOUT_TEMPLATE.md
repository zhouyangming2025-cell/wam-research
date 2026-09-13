# Session Close-out Template

每次长会话结束前，把最终状态写入 GitHub。

## CURRENT_STATE delta

- Primary candidate:
- Backup:
- Retired:
- Current evidence status:
- Current stage:

## DECISION_LOG entry

### YYYY-MM-DD — <Decision title>

**Decision**

...

**Why**

...

**Evidence**

- Paper IDs:
- Code audits:
- Experiments:

**Counterevidence considered**

...

**What would reverse this decision**

...

## NEXT_TASK

唯一下一任务：

> ...

Stop condition:

> ...

## Handoff

新会话首先读取：

```text
state/CURRENT_STATE.md
state/DECISION_LOG.md
state/NEXT_TASK.md
handoff/LATEST.md
```

然后按需读取：

```text
hypotheses/<current>.md
papers/cards/<relevant IDs>.md
audits/<relevant>.md
```

禁止新会话默认重读全部 corpus。
