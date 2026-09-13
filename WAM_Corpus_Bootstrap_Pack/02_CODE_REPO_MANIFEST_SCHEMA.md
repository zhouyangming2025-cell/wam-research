# CODE_REPO_MANIFEST Schema

源码仓库不要复制进 `wam-research`。

本地 clone，GitHub research repo 只记录 provenance。

## Fields

| Field | Meaning |
|---|---|
| `repo_id` | `R0001` |
| `project_name` | 项目名 |
| `official_url` | 官方 GitHub |
| `local_path` | 本地 clone 路径 |
| `default_branch` | main/master |
| `pinned_commit` | 审计/实验使用 commit |
| `tag` | 若有 |
| `license` | license |
| `paper_ids` | 关联 `Pxxxx` |
| `checkpoint_status` | NONE/AVAILABLE/DOWNLOADED |
| `checkpoint_local_path` | 本地位置 |
| `audit_status` | NOT_STARTED/MAPPED/AUDITED/USED_IN_EXPERIMENT |
| `github_audit_path` | GitHub 研究审计文件 |
| `last_checked` | date |
| `notes` | notes |

任何 CODE FACT 必须能回到：

```text
repo_id + pinned_commit + file + symbol
```
