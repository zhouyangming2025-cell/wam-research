# Directory Structure

## A. Local / NAS — Raw Assets

推荐：

```text
D:\zym_information\ZYM\wam\research_assets\
├── papers\
│   ├── pdf\
│   ├── raw_md\
│   ├── supplements\
│   └── quarantine\
├── repos\
├── checkpoints\
├── datasets\
├── experiment_logs\
├── manifests\
│   ├── CORPUS_MANIFEST.csv
│   └── CODE_REPO_MANIFEST.csv
├── scripts\
└── backups\
```

### quarantine

下载成功但 metadata / identity 尚未确认的文件先放：

```text
papers/quarantine/
```

不要直接混进 canonical corpus。

---

## B. GitHub — `wam-research`

推荐：

```text
wam-research/
├── README.md
│
├── state/
│   ├── CURRENT_STATE.md
│   ├── DECISION_LOG.md
│   ├── NEXT_TASK.md
│   └── RESEARCH_LEDGER.md
│
├── corpus/
│   ├── CORPUS_MANIFEST.csv
│   └── CODE_REPO_MANIFEST.csv
│
├── hypotheses/
│   ├── P1_RETIRED.md
│   ├── P2R_PRIMARY.md
│   └── P3_HOLD.md
│
├── papers/
│   └── cards/
│       ├── P0001_*.md
│       └── ...
│
├── evidence/
│   ├── OBSERVED_FAILURES.md
│   ├── COUNTEREVIDENCE.md
│   ├── PRIOR_ART_OCCUPANCY.md
│   └── EVALUATION_REGIMES.md
│
├── audits/
│   ├── literature/
│   ├── source_code/
│   └── experiments/
│
├── code/
│   ├── repos/
│   └── audits/
│
├── experiments/
│   ├── planned/
│   ├── completed/
│   └── INDEX.md
│
├── agent/
│   ├── prompts/
│   ├── reports/
│   └── worklogs/
│
└── handoff/
    └── LATEST.md
```

不要把 datasets / checkpoints / 整个第三方 repo 放进这里。

---

## C. ChatGPT Library

推荐逻辑分组：

```text
WAM Corpus — Core
WAM Corpus — P2R
WAM Corpus — P3
WAM Corpus — Archive
```

上传优先级：

1. canonical PDF；
2. raw MD；
3. 不需要上传 GitHub research card 的重复副本，GitHub 已经是权威来源。

---

# 同步原则

## Local → GitHub

同步：

- manifests；
- research cards；
- audits；
- decisions；
- handoff。

不自动同步：

- PDF；
- large raw files；
- repos；
- checkpoints。

## Local → Library

只上传：

- PDF；
- raw MD。

Library 不是唯一备份。
