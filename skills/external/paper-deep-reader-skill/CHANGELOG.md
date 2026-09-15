# Changelog

## 4.0.0 — 2026-08-15

- 恢复六部分论文解读结构作为默认 `explain` 契约：一句话总结、背景与动机、核心方法、实验与结果、贡献与影响、结论。
- 将单轴受众默认值改为双轴模型：零背景入口 `entry_level: novice` 与博士级技术上限 `technical_ceiling: doctoral`。
- 要求每个承重术语、缩写、指标和前置概念首次出现时先做白话解释，再给精确定义与类比边界。
- 要求至少一个最小例子在形式化细节之前走完整条核心机制。
- 将 `key: true` 视觉对象定义为 `explain` 与 `audit` 中必须进入报告的内容，取消原先 2–4 张的默认数量。
- 要求每个编号视觉对象填写 `classification_reason`，防止通过批量标记“非关键”规避覆盖。
- 新增图文邻接：每个关键图表附近必须有阅读指导、具体观察、观察到主张的推理桥，以及不能由该图推出的内容。
- 恢复实验设计、可靠性、贡献、影响和基于证据缺口的未来方向，同时不恢复 v2 的固定字段账本式正文。
- 将视觉 manifest 升级至 schema v4，将 source map 升级至 schema v5。
- 扩展确定性校验与单元测试，覆盖六部分结构、术语入门、贯穿例子、推理桥、关键视觉全覆盖、图文交错和分层读者元数据。
- 新增 `agents/openai.yaml`，用于 Codex 技能发现与界面展示。

## 3.0.0 — 2026-08-15

- Separated reading depth from delivery density with `brief`, `explain`, `audit`, and `targeted` modes.
- Made `explain` the default for both “解读” and “精读”: deep internal reading now produces a compact four-question explanation instead of a mandatory six-section audit.
- Required a worked minimal example before formal terminology and equations.
- Moved full visual ledgers, claim audits, reproduction details, and review checklists into optional audit appendices.
- Added understanding-driven visual selection through `selected_for_report`, `report_role`, and `selection_reason`; helpful figures and tables are included without a rigid count cap.
- Added mode-aware length budgets and validator checks for structure, examples, evidence grades, boundaries, visual selection, and source-map delivery consistency.
- Upgraded visual manifests to schema v3 and source maps to schema v4.

## 2.1.0 — 2026-08-01

- Added explicit `visual` and `text-only` execution routes for models without image understanding.
- Added `inventory --text-only`, which emits page text, per-visual text cards, body-reference contexts, and a text evidence ledger without rendering PNG assets.
- Added A/B/C/D text evidence grades and strict rules against presenting caption/OCR inference as direct visual observation.
- Added `validate_report.py --text-only` checks for disclosure, text-review completion, source recording, unverified-crop handling, and source-map execution metadata.
- Upgraded the source-map template to schema v3 with visual capability and verification fields.
- Documented structured-source, PDF-text, OCR, user-description, and human/vision-model handoff paths.

## 2.0.0 — 2026-08-01

- Broadened the default audience from computer-vision Ph.D. readers to research-trained readers across disciplines.
- Added structured routing for domain, audience, goal, depth, and language.
- Added project-level `.paper-reader.yaml` preferences and an example configuration.
- Separated method, theory, empirical/observational, dataset, system, and review paper types from domain-specific evidence norms.
- Added domain lenses for AI/CS, biomedicine, physics/mathematics, chemistry/materials, engineering, social science, earth/environment, and humanities/qualitative research.
- Kept computer vision as a deeply supported optional lens.
- Generalized report, reading, quality, and source-map protocols from model/experiment language to methods, theory, observation, qualitative evidence, and other research designs.
- Extended PDF caption detection to Scheme, Plate, Box, Chart, supplementary visuals, and Extended Data visuals.
- Added multilingual elevator-pitch validation and reader-profile validation for source-map schema v2.

## 1.0.0 — 2026-07-31

- Initial open-source release with source-grounded deep reading, visual extraction, report validation, and computer-vision-focused review guidance.
