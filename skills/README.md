# External research skills

本目录保存外部 GitHub research skill 的源码快照，供 `wam-research` 设计和对照使用。

## 使用边界

- `external/` 下的内容是参考材料，不是当前会话自动启用的 Codex skill。
- 不直接复制外部 skill 的整套规则；先提炼接口、证据要求和输出契约，再写成 WAM 专用版本。
- `RAW_MD`、manifest、证据 ledger 与研究判断分层保存；文献摄取阶段不触发 novelty、gap 或 reviewer 判断。
- 本轮只下载和整理，未提交或 push 这些外部源码。

## 已下载来源

| 来源 | 本地目录 | 角色 | 建议处理 |
|---|---|---|---|
| [Academic Research Agent Skill](https://github.com/ngtiendong/Academic-Research-Agent-Skill) | `external/academic-research-agent-skill/SKILL.md` + `references/{source_grounding,workflow}.md` | source/claim gate 与反重复 artifact discipline | 只保留当前证据链需要的三个参考文件，不整包启用 |
| [Paper Deep Reader Skill](https://github.com/Linwei-Chen/paper-deep-reader-skill) | `external/paper-deep-reader-skill/` | 单篇论文精读、图表和公式讲解 | 作为 `paper-reader` 的主要参考 |
| [Agent Paper Reader](https://github.com/chuyanchu/agent-paper-reader) | `external/agent-paper-reader/` | claim-evidence、复现性、反证实验 | 作为 `evidence-audit` 的主要参考 |
| [Agent Skills for Academic Research](https://github.com/jjfroehlich/agent-skills-for-academic-research) | `external/literature-reading-and-synthesis/` | claim-evidence 与文献综合 | 作为跨论文证据综合参考 |

当前只保留与论文精读和证据审计直接相关的 4 个参考 bundle。原先下载的 career、grant、publishing、communication、feedback、writing、visualization、mentoring 与 project-design 快照不属于当前证据链，已从工作树移除；Git 历史仍保留其来源，不把它们当作研究入口。

## 建议的 WAM 融合方案

不要把四个来源并列挂载为 13 个长期运行 skill，建议收敛为 5 个 WAM 原生层：

1. `paper-reader`：单篇精读；输出必须带 page / section / figure / table locator。
2. `evidence-audit`：逐条 claim → evidence → limitation → reproduction check。
3. `literature-ledger`：把精读结果写入现有 paper ID、raw MD、deep analysis 和 manifest；不再创建平行矩阵层。
4. `research-analysis`：仅在用户明确要求研究方向判断时执行；当前保持暂停。

## 分阶段落地

1. **兼容性审计**：检查各来源的触发条件、输出格式、引用方式、许可证和规则冲突。
2. **契约提炼**：只抽取 locator、claim ledger、图表解读、复现风险和 gate 字段，形成 WAM schema。
3. **小样本试跑**：用已完成的 P0042 / P0046 / P0061 做单篇精读和 claim audit，对比是否能回指 raw MD 与 PDF 页码。
4. **跨论文试跑**：用 WorldDrive → World4Drive → SeerDrive 做统一矩阵，验证 stable ID、证据定位和版本边界。
5. **固化与验收**：把通过试跑的规则写入正式 `skills/`，补测试和示例，再单独提交；外部快照保留为参考，不参与运行时默认路由。

## 当前推荐优先级

`agent-paper-reader`（证据审查） → `paper-deep-reader-skill`（单篇精读） → `academic-research-agent-skill`（总流程 gates） → academic-research 集合中的 literature / strategy / feedback 子 skill。
