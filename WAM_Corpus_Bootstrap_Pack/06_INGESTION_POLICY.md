# Corpus Ingestion Policy

## 下载前

对每篇 paper：

1. 确认 identity；
2. 查 official paper URL；
3. 查 official code；
4. 查是否已有本地副本；
5. 分配 `paper_id`。

## 下载后

至少做：

```text
PDF exists
PDF size > 0
title matches
raw MD conversion succeeds
manifest row created
```

建议生成 SHA256：

```text
pdf_sha256
raw_md_sha256
```

如果要长期严格审计，可把这两个字段自行追加到 manifest。

## MD 转换 QC

自动转换后快速检测：

- 标题存在；
- Abstract 存在；
- Method/Experiment 至少能识别主要 heading；
- References 存在；
- 文件没有异常短；
- 乱码比例不过高；
- 表格是否至少保留文本；
- 图像路径是否存在。

失败则：

```text
RAW_MD_QC_FAIL
```

不要让坏 MD 进入主检索 corpus。

## 图片

raw MD 中图像可保留为：

```markdown
`![](images/<verified-image-file>.jpg)`（这里只是路径模式示例，不是仓库内的图片链接。）
```

但不要因此认为 MD 等价于 PDF。

## Paper Card 生成策略（历史规则，已停用）

当前不再生成 paper cards。仅在 raw/source evidence 已审计后更新现有 deep analysis；不要恢复平行 card/template 层。

### 自动生成允许

Agent 可生成：

- metadata；
- section index；
- architecture/data-flow 初稿；
- evaluation regime 初稿；
- code URL；
- 关键词。

### 自动生成后必须人工/GPT审核

- observed failure；
- counterevidence；
- hypothesis impact；
- prior-art occupancy；
- research verdict。

这些直接影响科研方向，不允许批量无审计自动写死。

## 源码 clone 策略

不是每篇有 code 就 clone。

优先 clone：

```text
decision_relevance = HIGH
```

或：

```text
当前 targeted hypothesis 直接相关
```

上百篇论文可能只需要 20–40 个 repo。

## GitHub push 策略

批次 commit：

```text
ingest(batch-01): add 25 core WAM papers to corpus index
deep-analysis(batch-01): update reviewed evidence in the canonical per-paper analysis
audit(P2R): update reactive counterfactual evidence
```

不要每个微小自动生成文件都制造一个 commit。

## Library 上传策略

每批 20–40 篇。

先验证：

- 文件可检索；
- 新会话可找到；
- PDF 与 raw MD 命名一致。

再扩大批量。
