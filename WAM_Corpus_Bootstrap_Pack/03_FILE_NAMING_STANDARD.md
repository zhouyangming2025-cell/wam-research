# File Naming Standard

## 1. Paper ID

固定 4 位流水号：

```text
P0001
P0002
...
P0127
```

ID 一旦分配，不因标题修改而改变。

## 2. PDF

```text
P0001_Epona.pdf
PXXXX_DriveLaW.pdf
```

标题部分使用短名，不用完整论文标题。

## 3. Raw Markdown

```text
P0001_Epona.raw.md
PXXXX_DriveLaW.raw.md
```

用 `.raw.md` 明确表示：

> 这是自动转换全文，不是研究卡片。

## 4. Research Card（历史规则，已退役）

当前不再生成 `papers/cards/`。使用：

```text
papers/deep_analysis/P0001_EPONA_DEEP_ANALYSIS_V2.md
audits/literature/<phase>_EPONA_AUDIT.md
```

不要写 `.raw`。

## 5. Deep-read / Audit

```text
audits/literature/P0001_Epona_DEEP_READ.md
audits/literature/P0001_Epona_ADVERSARIAL_AUDIT.md
```

## 6. Source-code audit

```text
code/audits/R0003_TOAD_CEM_AUDIT.md
```

## 7. Paper supplements

```text
papers/supplements/P0001_Epona_supp.pdf
```

## 8. 文件名字符规则

建议仅使用：

```text
A-Z a-z 0-9 _ -
```

避免：

```text
: ? * < > | " /
```

Windows 路径更稳定。

## 9. 同名论文

ID 是唯一主键，因此无需在文件名里堆作者/年份来防冲突。

## 10. 版本论文

如果 arXiv 更新：

```text
P0042_xxx_v1.pdf
P0042_xxx_v2.pdf
```

manifest 的 canonical source 指向当前审计版本。
