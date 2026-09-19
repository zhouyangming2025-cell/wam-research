# wam-research

Persistent research workspace for **World Model + one-stage End-to-End + planning-centric autonomous driving**.

## 唯一恢复入口

~~~
1. state/CURRENT_STATE.md
2. state/NEXT_TASK.md
3. manifests / raw paper / source-code audit / deep analysis required by that task
~~~

不从旧 taxonomy、route map、handoff、状态标题或聊天记忆推断当前任务。

远端旧分支只作为审计历史，不是平行工作入口；工作树与当前状态只认 `main`。旧分支中的 route / ontology / matrix 草稿未被恢复为当前结论。

## 当前主程序与边界

~~~
FIELD RECONSTRUCTION — Planning-centric WAM Atlas
18 normalized anchors; Wave C.7 (simulation / reactivity / evaluation) remains active.
SAFE-SIM and ProSim are complete; P0013 BridgeSim is next.
~~~

固定 12 篇（Epona、DriveLaW、WorldDrive、WoTE、World4Drive、LAW、Drive-JEPA、SeerDrive、Metis、DynFlowDrive、Discrete-WAM、GraphWorld）是当前机制证据收口子任务：它用于核验跨论文技术路线，不取代更广的 field reconstruction，也不授权最终 taxonomy、研究问题或方法设计。

固定 12 篇的唯一横向复核接口（仍属临时雏形）是 `audits/research_synthesis/WAM_PLANNING_INTERFACE_FRAMEWORK.md`。它只回答 Q1–Q5：未来计算位于哪里、未来对象是什么、是否前向进入动作链、承担什么角色、部署保留什么；完整证据仍回到 raw/deep/source 文件。

## 证据顺序

~~~
论文原文 / 固定代码 / 数据与评测配置
→ source-code audit 与 deep analysis（保留其范围与版本边界）
→ 跨论文比较
→ 历史 taxonomy、路线图、状态快照、handoff
~~~

训练期未来监督、在线世界状态、候选后果评估、世界—规划迭代和外部反应式仿真必须分开；缺证据时保留 UNKNOWN。

## ProSim 当前证据

~~~
papers/raw_md/P0067_ProSim/P0067_ProSim.source_note.md
papers/deep_analysis/P0067_PROSIM_DEEP_ANALYSIS_V2.md
audits/literature/PHASE_C7_PROSIM_AUDIT.md
~~~

ProSim 是 promptable closed-loop traffic behavior simulator：有共享 scene-token 反馈与生成代理之间的下一 chunk 反应，但没有 paired real intervention-response truth；发布默认配置也不证明完整 BPTT 或完整训练管线可复现。manifest 注册因 CSV 非 UTF-8 暂挂，见 manifests/P0067_PROSIM_REGISTRATION_PENDING.md。

SAFE-SIM 的完整 raw Markdown 与图像也已恢复到 `papers/raw_md/P0066_SafeSim/`；只有 CSV 登记仍待本地编码安全复核，见 `manifests/P0066_SAFESIM_REGISTRATION_PENDING.md`。

## 当前清理规则

不删除 raw Markdown、来源/代码审计、带独立定位的 deep analysis、manifest、实验记录和决策历史。派生 matrix、ontology amendment、paper-card、路线图和导航文档必须先完成“独有证据是否已有存活来源”的核对，才可合并、归档或删除；paper-card 层目前已退役。

研究问题发现、候选问题提升和方法设计仍暂停。
