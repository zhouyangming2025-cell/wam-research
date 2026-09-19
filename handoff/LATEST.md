# LATEST — 已退役的状态快照

本文件不再发布“latest”研究状态，避免 handoff、README、START_HERE 和 state 文件互相覆盖。

恢复会话时只读取：

```text
README.md
state/CURRENT_STATE.md
state/NEXT_TASK.md
manifests/CORPUS_MANIFEST.csv
```

历史 handoff 的科学观察仍可通过 Git 历史和对应论文/审计文件追溯；它们不应覆盖当前状态。