# 01 — 既有研究资产处置账本

**状态：ACTIVE — 可追加。**  
本账本不删除、不重写历史材料；它限定它们在新的 12 篇技术路线重建中能够承担的角色。

## A. 直接保留为证据底座

|资产|处置|原因与使用规则|
|---|---|---|
|`papers/raw_md/P0001, P0009, P0042, P0045, P0046, P0048, P0049, P0061–P0065`|保留，最高优先级|12 篇论文的可复核文字底座；所有路线性主张必须能回指到此处或固定代码。|
|`audits/literature/` 中的单篇 paper/source/code audit|保留，二级解释|其中关于输入、未来对象、训练/部署、版本差异的定位可复用；未经原文复核的句子不升级为事实。|
|`papers/deep_analysis/`|保留，二级解释|作为深读和反例材料；以文档中的证据边界为准。|
|`evidence/`、manifests、来源/代码可得性审计|保留，证据元数据|保留 `UNKNOWN`、版本、获取限制与冲突，不静默补全。|

## B. 采用其方法，不继承其结论

|资产|保留的有效成分|禁止继承的成分|
|---|---|---|
|`research_program/pilot_quarantine/`（提交 `f47e2ca`）|来源优先记录、Q1–Q5、mode split、PAPER/CODE/INFERENCE/UNKNOWN 分栏、停止条件|把五问行直接提升为技术路线，或把 `READY-FOR-REVIEW` 当作人工批准。|
|`research_program/core_route_reconstruction/`（提交 `b942c82`）|训练/部署双图、world-object lifecycle、candidate/commitment、Core-Bridge Deletion Test、反例日志|六个最小机制程序或任何 route name 已被正式接受的说法。|
|`outputs/core_mechanism_12_v1/`|盲 DAG、碰撞/压力测试、论文 artifact 拆分|S1+/normative、唯一代码、路线压缩结果的权威性。|
|`landscape/`、外部综述与 comparability QA|论文定位、术语核对、外部反例候选|将广域综述当成核心 12 的直接证据，或让它替代原文核验。|

## C. 降级为历史性组织尝试

|资产簇|处置|理由|
|---|---|---|
|V1/V1.3 taxonomy、WAM mechanism families、design space、comparison matrix 的标签层|归档引用，不作为新的分类键|存在跨版本重复、维度混合、单篇唯一标签和状态不同步。|
|`codex/domain-census-*`、`codex/domain-map-*` 的 D01/D02、R1/R2|保留其论文阅读与反例，冻结其代码体系|D01.1 暂停交接已明示不得将其推广为最终签名；后续“stable”文字不足以撤销该边界。|
|旧 12-paper route map / route signature / ontology spec|仅作待攻击的历史假说|它们可帮助发现遗漏分叉，但不可直接成为最终图。|
|`papers/cards/`|不作为 canonical-12 事实输入|覆盖对象与 canonical 12 不一致，且存在 skeleton / pending 卡片。|
|`state/`、`START_HERE`、`NEXT_TASK`、旧 handoff|保留时间线线索，不作为当前事实来源|main 与分支状态互相滞后；需由提交、原文和本账本裁决。|

## D. 已知高价值、不可丢失的具体观察

- **训练与部署必须分图。** LAW、Metis 一类未来监督不等于部署时显式未来推演。
- **未来对象不能同名合并。** DriveLaW 的生成器 hidden state、WorldDrive 的蒸馏评分能力、WoTE 的候选 BEV 后果并不是同一个“future latent”。
- **候选—评估—选择是单独的决策因果结构。** World4Drive、WorldDrive、WoTE 必须比较候选承诺、评分器与选择器，而非只标作“在线未来”。
- **artifact / mode 必须显式。** Epona 的 planning-only 与视频参与模式、Drive-JEPA 的 PF/PB、SeerDrive 的论文图与发布实现都不可压成一行。
- **来源缺口本身是结果。** DynFlowDrive、Discrete-WAM、GraphWorld 等的代码或部署细节不可得时，应写 `UNKNOWN`，不能用邻近论文补齐。

## E. 重建期间的处置规则

1. 原始资料、既有审计和历史分支均不删除、不搬迁。
2. 新结论只写入 `research_program/route_rebuild/`；旧文件只通过链接引用。
3. 每次引用历史综合，都必须标明它属于“方法”还是“假说”。
4. 任何要进入最终路线图的条目，先在 `02_CANONICAL12_SOURCE_FIRST_ROUTE_WORKBOOK.md` 中补齐证据与反例。
