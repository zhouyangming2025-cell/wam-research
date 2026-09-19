# WAM Research Corpus — Operating System

> Historical corpus-process template. It governs asset provenance only; it does not set the current scientific task or authorize a new research direction. For the live entry order, use `README.md` → `state/CURRENT_STATE.md` → `state/NEXT_TASK.md` → `manifests/CORPUS_MANIFEST.csv`.

## 目标

建立一个长期可持续的 WAM / Planning-centric 自动驾驶研究语料系统，使：

- 原始论文不会因会话结束而丢失；
- GPT-5.6 Sol 可以跨会话按需读取；
- 论文结论、反证、假设和决策有明确 provenance；
- 源码、论文、实验结果可以互相引用；
- 新会话无需重新“吃”全部历史。

核心分层：

\[
\boxed{\text{Local/NAS = Raw Asset Authority}}
\]

\[
\boxed{\text{GitHub = Research Knowledge Authority}}
\]

\[
\boxed{\text{ChatGPT Library = AI Access / Retrieval Layer}}
\]

---

## 1. 三类文件

### A. Canonical PDF

原始论文 PDF。

作用：

- 最终事实核查；
- Figure / Table / Appendix / Footnote；
- 防止 PDF→MD 转换错误。

保存位置：

```text
local/NAS/papers/pdf/
ChatGPT Library/
```

不要依赖 GitHub 保存大量 PDF。

### B. Raw Markdown

PDF 转换得到的全文 Markdown。

作用：

- 全文检索；
- semantic retrieval；
- cross-paper synthesis；
- Agent 批处理；
- LLM 阅读。

保存位置：

```text
local/NAS/papers/raw_md/
可选：ChatGPT Library/
```

如果文件体积合理，也可以放 GitHub 的 `raw_text/`，但不是必须。

### C. Research synthesis (current) / historical card policy

旧 Research Card 层曾用于承载研究知识，但它与 deep analysis/source audit 重复，已从工作树退役。当前 canonical synthesis 只保留每篇论文一个 deep analysis；只有存在独立版本/源码证据时才保留 source/code audit。

作用：

- 记录该论文真正影响研究决策的内容；
- 把 Author Claim / Direct Evidence / Our Inference 分开；
- 记录它攻击哪个 hypothesis；
- 记录 observed failure / counterevidence / evaluation regime。

保存位置：

```text
GitHub wam-research/papers/deep_analysis/ 与 audits/literature/
```

---

## 2. 单篇论文标准资产

每篇重要论文最终对应：

```text
P0042/
├── Canonical PDF      -> local/NAS + Library
├── Raw MD             -> local/NAS (+ Library)
└── Deep analysis      -> GitHub；必要时再加 source/code audit
```

通过 `paper_id` 串联，而不是靠文件名猜。

---

## 3. 最重要的纪律

### 不要把 100+ 篇论文全部当“精读”

Corpus 中允许存在不同阅读状态：

```text
DISCOVERED
DOWNLOADED
RAW_MD_READY
SCREENED
DEEP_READ
AUDITED
DECISION_RELEVANT
RETIRED
```

### 不要让 Agent 自动产生“研究结论”

Agent 可以：

- 下载；
- 校验；
- 转 Markdown；
- 抽 metadata；
- 建索引；
- 生成初始结构化摘要。

但以下任务交给 GPT-5.6 Sol / 人工审查：

- 这篇论文是否真正支持某个 gap；
- observed failure 是否成立；
- 是否与其他工作冲突；
- 是否杀掉 hypothesis；
- 是否形成 innovation。

---

## 4. Corpus ingestion 推荐节奏

### Batch 0 — 已经影响过研究决策的核心论文

先处理 20–30 篇：

- 已精读；
- 已进入 Research Ledger；
- 对 P1/P2/P3 产生过实质影响。

### Batch 1 — P2-R targeted corpus

约 20–40 篇：

- reactive prediction；
- interactive planning；
- counterfactual world models；
- closed-loop evaluation；
- contingency / game-theoretic planning。

### Batch 2 — P3 backup corpus

约 20–40 篇。

### Batch 3 — broad archive

过去 100+ broad-read papers 逐步补齐。

不要第一天就让 Agent 对 150 篇全部生成深度结论。

---

## 5. 新会话恢复协议

任何新 ChatGPT 会话先读 GitHub：

```text
state/CURRENT_STATE.md
state/DECISION_LOG.md
state/NEXT_TASK.md
```

然后按当前任务读取：

```text
hypotheses/<CURRENT>.md
evidence/<relevant>.md
papers/deep_analysis/<relevant>_DEEP_ANALYSIS_V2.md
audits/literature/<relevant>_AUDIT.md (only when independently needed)
```

只有证据不足时才回 Library 的 raw MD / PDF。

这叫：

\[
\boxed{\text{Selective Retrieval, not Full Reload}}
\]

---

## 6. 数据主权原则

任何 Library 中的重要 PDF / MD 必须已有 local/NAS 副本。

任何聊天中形成的重要研究结论必须写回 GitHub。

任何源码研究必须记录：

```text
official repo URL
commit SHA
local path
license
audit file
```

任何实验必须记录：

```text
code commit
config
dataset/split
seed
checkpoint SHA
result path
```
