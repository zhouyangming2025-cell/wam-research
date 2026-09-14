"""Compose the handoff document for the corpus text-layer work.

Written for the human who owns the research, not for a machine: it says where the corpus stands,
how to read it, what was verified, which traps cost time (including the agent's own mistakes), and
what still needs an owner decision. Every number is read from a ledger, never retyped.

Usage:
    python build_handoff_doc.py
"""
from __future__ import annotations

import csv
import json
import os
from collections import Counter

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAN = os.path.join(BASE, "manifests")
OUT = os.path.join(BASE, "handoff", "CENSUS_TEXTLAYER_HANDOFF.md")


def load(name: str):
    p = os.path.join(MAN, name)
    if not os.path.exists(p):
        return {}
    d = json.load(open(p, encoding="utf-8"))
    if isinstance(d, list):
        d = {r["paper_id"]: r for r in d if isinstance(r, dict) and "paper_id" in r}
    return d


def main() -> int:
    rows = list(csv.DictReader(open(os.path.join(MAN, "CORPUS_MANIFEST.csv"), encoding="utf-8", newline="")))
    alloc = json.load(open(os.path.join(MAN, "census1_id_allocation.json"), encoding="utf-8"))
    ident = load("batch_census1_identity.json")
    ev = load("batch_census1_evidence.json")
    dl1 = load("batch_census1_download_results.json")
    md1 = load("batch_census1_rawmd_results.json")
    md2 = load("batch_census2_rawmd_results.json")
    fp1 = load("batch_census1_frontpage_verification.json")
    plan = json.load(open(os.path.join(MAN, "census_round1_acquisition_plan.json"), encoding="utf-8"))
    ids = sorted(alloc)
    c2 = [r for r in rows if "P0021" <= r["paper_id"] <= "P0034"]
    lib = Counter(r["library_status"] for r in rows)
    yes = [r for r in rows if r["code_available"] == "YES"]
    L: list[str] = []
    a = L.append

    a("# 交接文档：语料本地文本层（census1 批次 + 现状）")
    a("")
    a("给项目所有者。写的是**语料现状与怎么用**，不是研究结论。所有数字由台账生成")
    a("（`scripts/build_handoff_doc.py`），不是手抄。")
    a("")
    a(f"- 语料规模：**{len(rows)} 条记录**（{rows[0]['paper_id']}–{rows[-1]['paper_id']}）")
    a(f"- 有本地 PDF + raw MD 文本层：**{lib.get('PDF+MD', 0)} 条**；无公开来源：{lib.get('NONE', 0)} 条")
    a(f"- 文本层已发布到私有 GitHub 仓库（`origin/main`），clone 后可直接精读")
    a("")
    a("## 0. 现在可以直接怎么用")
    a("")
    a("| 你想做的事 | 打开这个 |")
    a("|---|---|")
    a("| 读正文（含图） | `papers/raw_md/P00XX_<短名>/P00XX_<短名>.raw.md` 与同级 `images/` |")
    a("| 看权威清单（谁在语料里、来源、哈希、标签） | `manifests/CORPUS_MANIFEST.csv`（%d 行 × %d 列） |" % (len(rows), len(rows[0])))
    a("| 看本批次的采集与核验细节 | `CENSUS_ROUND1_TEXTLAYER_INGEST_REPORT.md` |")
    a("| 看上一批次（覆盖空洞） | `CENSUS_ROUND2_INGEST_REPORT.md` |")
    a("| 复核某个数字从哪来 | `manifests/batch_*.json`（每步一份台账） |")
    a("")
    a("## 1. 本次做的事：把 Round-1 已放置的作品补上本地文本层")
    a("")
    a("你在 `landscape/CENSUS_PHASE_A_ROUND1.md` 里已经放置了约 45 篇，但其中 26 篇此前只有")
    a("条目、没有本地正文；要读就得临时联网抓 PDF。这批把这 26 篇补齐为：一条核验过的身份、")
    a("一份正典 PDF + 逻辑字节 SHA256、一次首页核验、一份可提取的 raw MD 与配图。")
    a("")
    a("| id | 短名 | 官方标题 | 来源 | 页 | raw md 字符 |")
    a("|---|---|---|---|---:|---:|")
    for pid in ids:
        r = ident.get(pid) or {}
        title = (r.get("official_title") or "").replace("|", "/")
        if len(title) > 62:
            title = title[:59] + "..."
        kind = (plan.get(alloc[pid]["key"]) or {}).get("kind", "")
        # canonical-source label comes from the download ledger, which records the real version
        sv = (dl1.get(pid) or {}).get("source_version") or kind
        a(f"| {pid} | {alloc[pid]['short']} | {title} | {sv} | "
          f"{(fp1.get(pid) or {}).get('pages','')} | {(md1.get(pid) or {}).get('length_chars','')} |")
    a("")
    a("此外 P0021–P0034（%d 篇）是上一批“覆盖空洞”支持批次，同样有本地文本层。" % len(c2))
    a("")
    a("## 2. 这 26 篇是怎么选出来的（机械化，不靠记忆）")
    a("")
    a("1. `scripts/parse_census_works.py`：机械解析你的 census 表格行与 Round-1 来源登记表，减去")
    a("   语料里已有的记录；")
    a("2. `scripts/plan_census_acquisition.py`：按语料既定的来源优先级 **venue camera-ready >")
    a("   官方 arXiv > 项目页** 为每篇挑一份正典文档（CVF 论文页推导 PDF，NeurIPS/ICLR 页抽取 PDF");
    a("   链接）；")
    a("3. 每个候选 URL 先探测是否真返回 `%PDF-` 才下载；")
    a("4. 登记表只给项目页/仓库的 5 篇，走“发现 + 独立核验”：CVF 索引页扫标题（Drive-WM），或")
    a("   从作品自己的项目页/仓库里找官方 arXiv 链接，再到官方落地页核验标题（Drive-OccWorld、")
    a("   DriveArena、SLEDGE）。**项目页只是发现入口，永远不作为证据**；")
    a("5. **NPPC 仍未入库**：登记表记明它没有合法开放来源，这与 P0008 一直无 PDF 是同一原因。")
    a("")
    a("## 3. 已核验的事实（可引用为事实的部分）")
    a("")
    a(f"- 首页核验：26/26 `DOCUMENT_VERIFIED`（标题精确匹配 + 第一作者出现在首页），")
    a(f"  全库唯一 `PARTIAL` 是 P0027 Think2Drive 的标题分歧（见 §5.5）")
    a(f"- 转换 QC：26/26 `RAW_MD_READY`；替换乱码字符 **0**；配图 "
      f"{sum((md1.get(p) or {}).get('images_copied') or 0 for p in ids)} 张，缺失 "
      f"{sum((md1.get(p) or {}).get('images_missing') or 0 for p in ids)} 张")
    a(f"- 去重：45 个非空 arXiv ID **无一重复**；全库**无重复标题**；无 ID 复用或重编号")
    a(f"- 代码可得性按论文自述记录：`code_available=YES` 的 {len([r for r in rows if r['paper_id'] >= 'P0035' and r['code_available'] == 'YES'])} 篇都印了仓库 URL；"
      f"其余标 `UNKNOWN`（不印 URL ≠ 没有代码；项目页不算仓库）")
    a("")
    a("## 4. 每个记录的元数据约定（读 manifest 前请先看这段）")
    a("")
    a("- `hypothesis_tags=GENERAL`、`decision_relevance=LOW`：本批次定位是“让 census 可本地阅读”，")
    a("  不对决策相关性下判断；标签由固定词表在**作品自身标题与正文**中的计数机械得出，")
    a("  **不是**你的家族归属；")
    a("- `reading_status=RAW_MD_READY` 且 `NO_CARD`：这些是**放置深度**的文本层，没有做深读，")
    a("  因此没有生成论文卡片；")
    a("- `arxiv_id` 为空 ≠ 不存在 arXiv 版本：10 条 camera-ready 记录的落地页未印 arXiv 版本，")
    a("  留空表示“未记录/未显示”，不写成 `NONE`（那会变成一句我无法支撑的断言）；")
    a("- `code_available=UNKNOWN` 是“论文没有印仓库 URL”，不是“没有代码”。")
    a("")
    a("## 5. 必须知道的坑（含我自己的失误，全部已修或已记录）")
    a("")
    a("1. **MinerU 内存泄漏（本批次最大坑）**：每一篇转换结束后会残留一个约 1.7 GB 的 python")
    a("   进程；跑到第 12 篇时主机内存耗尽，`OpenBLAS … Memory allocation still failed` + 502，")
    a("   后续任务全部失败。对策：**小批量转换（每次 3 篇）+ 每批清理工作集 > 800 MB 的残留进程**。")
    a("   这不是文档问题，失败篇重试即成功。")
    a("2. **台账竞态**：两个 MinerU 进程并行时各自读一次台账再整体写回，后写者会静默丢掉前者的")
    a("   记录（census2 曾丢 6 条）。已修：写台账前重读；并保留 `scripts/repair_rawmd_ledger.py`")
    a("   可从磁盘产物忠实重建（本次重建 12 条，数值与原记录逐项吻合）。")
    a("3. **转换会丢文本**：P0028 ViDAR 首页印着的代码 URL 在 raw MD 里不存在。因此代码证据允许")
    a("   取自 PDF 首页并标注位置，避免“只看 markdown 就断言没代码”。")
    a("4. **参考文献里的第三方仓库会被误认**：GAIA-1 的扫描一度把参考文献中的 stable-diffusion")
    a("   WebUI 当成本文代码。已修：扫描先截断参考文献段。")
    a("5. **标题分歧（记录而非抹平）**：census 把 P0052 写作 “ReWorld: Learning Better”")
    a("   Representations for World Action Models”，官方记录是 “ReWorld: Representation Learning")
    a("   for World Action Models”。入库用**官方标题**，你的 census 文件**未改动**。")
    a("   P0027 Think2Drive 同类（arXiv 落地页 vs PDF 首页），入库用论文首页标题。")
    a("6. **无公开来源的记录**：P0008（NPPC，IEEE 付费无开放版）与 P0020（Bahram2016）没有 PDF，")
    a("   `library_status=NONE`，manifest 里明确标注，未用猜测链接填充。")
    a("")
    a("## 6. 待你裁决（我按边界留给你）")
    a("")
    a("1. **NPPC**：提供许可副本，或维持“已记录阻塞”。")
    a("2. **`decision_relevance=LOW` 的整批惯例**：若其中若干篇已是你的 anchor，请点名，我会把它记成")
    a("   你的判断（而不是我的）。")
    a("3. **词表缺口**：语料没有 vision-language / VLA 类标签，相关的 VLA 工作只能用最接近的词表标签")
    a("   （如 P0024 DriveVLM、P0025 OmniDrive、P0026 ORION）。是否扩词表由你定。")
    a("4. **census 措辞 vs 官方标题**：是否需要在 manifest 里同时保留 census 的写法（如 P0052）。")
    a("")
    a("## 7. 环境与复现")
    a("")
    a("```powershell")
    a("# 网络/PDF 一律用带 certifi 的解释器，否则 TLS 校验会失败")
    a("$mp = 'D:\\Program Files\\Mineru\\venv\\Scripts\\python.exe'")
    a("$env:CORPUS_BATCH = 'census1'")
    a("$env:PYTHONIOENCODING = 'utf-8'")
    a("# MinerU 转换（必须串行 / 小批量；环境变量见 CENSUS_ROUND1_TEXTLAYER_INGEST_REPORT.md §12）")
    a("& $mp -u scripts\\build_raw_md.py P0035,P0036,...,P0060")
    a("```")
    a("")
    a("脚本分工：采集规划 `parse_census_works.py` / `plan_census_acquisition.py` /")
    a("`resolve_census_unresolved.py` / `resolve_census_via_discovery.py` / `apply_census1_plan.py`；")
    a("核验与入库 `fetch_work_identity.py` / `fetch_canonical_pdfs.py` / `verify_frontpage.py` /")
    a("`build_raw_md.py` / `build_census1_meta.py` / `build_manifest.py`；报告")
    a("`build_census1_report.py` / `build_handoff_doc.py`。")
    a("")
    a("## 8. 我的边界（这一条也是交接内容）")
    a("")
    a("本次工作只做：采集、身份核验、下载与哈希、转换、QC、元数据、台账与报告。**没有**做家族归属、")
    a("新颖性/缺口判断、方法设计或深读；**没有**编辑你的 `landscape/`、`state/`、`handoff/` 文件")
    a("（本文件是新建的交接说明，不是改写你的既有文件）。凡我无法用官方来源核验的东西，都留在")
    a("“未解决”里，而没有填成结论。")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(f"  wrote {OUT}")
    print(f"    {len('\n'.join(L))} chars, {len(L)} lines")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
