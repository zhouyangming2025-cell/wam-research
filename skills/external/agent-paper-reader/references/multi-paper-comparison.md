# Multi-Paper Comparison

Use this reference when the user provides multiple AI agent papers, asks which paper is more important, or wants to understand a research cluster.

For Chinese users, write the main analysis in Chinese. Keep paper titles, method names, benchmarks, datasets, and model names in English when needed.

## Start With the Comparison Goal

Choose one primary goal unless the user specifies otherwise:

- Field map: build a mental model of the topic.
- Method choice: decide which mechanism is most useful.
- Reproduction choice: decide what to implement first.
- Research gap discovery: find publishable next steps.
- Evaluation audit: judge whose evidence is strongest.
- System design: extract ideas for a practical agent architecture.

## Depth Modes

Choose a depth mode before writing:

- `balanced` default: first write a compact mini-review for each paper, then compare them. Use this for most paper-reading and research-planning requests.
- `deep-per-paper`: write near full single-paper analysis for each paper before comparison. Use by default when there are only 2-3 papers, or whenever the user asks for detailed reading.
- `quick-scan`: skip mini-reviews and only produce one-line verdicts plus a comparison table. Use only when the user asks for a quick overview, triage, or reading order.

Do not let cross-paper comparison erase individual paper analysis. In `deep-per-paper` mode, every paper should use the full six-question paper-reading structure. In `balanced` mode, every paper must keep at least:

```text
问题：
缺口：
方法：
证据：
可延展点：
```

## Deep-Per-Paper Structure

For 2-3 papers, prefer this structure before the comparison:

```text
### Paper A

1. 这篇论文解决什么问题
- 用 1-2 段解释问题背景、任务设定和为什么重要。

2. 已有方法为什么不够
- 区分作者声称的不足、真实成立的不足、可能被夸大的不足。

3. 作者怎么解决
- 先用直白语言讲核心 idea。
- 再拆 agent loop 和关键组件。
- 最后说明哪个机制是最小必要机制。

4. 优势与证据
- 按 claim -> evidence -> interpretation 写。
- 说明实验支持了什么，也说明没有支持什么。

5. 缺点与隐含假设
- 模型依赖、prompt 依赖、工具/环境依赖、成本、复现细节、benchmark 风险。

6. 我们能在它基础上做什么
- 复现 MVP。
- 一个直接改进。
- 一个更严格评测。
- 一个可和其他论文组合的想法。
```

Then write the cross-paper synthesis. The synthesis should not repeat every detail; it should explain relationships, conflicts, and next actions.

## Contribution Types

Label each paper by contribution type:

- Framework: general infrastructure for building agents.
- Workflow/SOP: structured process or role design for collaboration.
- Mechanism: specific planning, memory, tool-use, reflection, verifier, or training method.
- Benchmark: task suite, dataset, environment, metric, or evaluation protocol.
- Analysis: failure taxonomy, behavior study, scaling analysis, or diagnostic method.
- Survey: taxonomy and literature organization.
- Position: agenda or argument with limited direct evidence.

This prevents treating framework, benchmark, and analysis papers as if they were competing algorithms.

## Comparison Table Fields

Use a compact table when comparing three or more papers:

```text
Paper | Type | Problem | Core mechanism | Agent loop | Evaluation | Main strength | Main weakness | Best use
```

For Chinese output:

```text
论文 | 类型 | 解决的问题 | 核心机制 | Agent loop | 评测证据 | 主要优势 | 主要弱点 | 最适合用途
```

For deeper comparison, add:

```text
Backbone model | Planning | Memory | Tools | Verifier | Multi-agent role design | Cost reporting | Reproducibility
```

## Method Comparison Questions

- Are the papers solving the same task or only using similar terminology?
- Is the novelty in agent orchestration, prompt design, training, memory, tools, benchmark, or analysis?
- Is the agent loop dynamic or fixed?
- Does multi-agent collaboration outperform a single agent under equal budget?
- Does the method require closed-source models or hidden prompts?
- Can the method survive weaker models, fewer tool calls, and different tasks?
- What part of the method could be reused independently?

## Evidence Comparison Questions

- Which paper has the fairest baselines?
- Which reports ablations that isolate the claimed mechanism?
- Which reports cost, latency, retries, and tool-call budget?
- Which evaluates across multiple models or tasks?
- Which includes failure cases or trajectory analysis?
- Which claims are not established by the evidence?

## Complementarity Patterns

Look for combinations:

- Framework paper + failure analysis paper: use the analysis taxonomy to debug the framework.
- SOP/workflow paper + benchmark paper: test whether structured roles actually improve task success.
- Memory paper + tool-use paper: preserve useful observations across tool calls.
- Multi-agent paper + single-agent baseline paper: verify whether collaboration is worth the budget.
- Coding agent paper + verifier paper: combine patch generation with test or static-analysis feedback.

## Research Gap Patterns

Classify gaps as:

- Method gap: missing mechanism, weak planner, shallow memory, poor verifier, brittle tool use.
- Evaluation gap: weak baselines, missing budget controls, benchmark leakage, no failure analysis.
- Reproduction gap: hidden prompts, no code, missing tool schemas, closed environments.
- Engineering gap: high latency, high cost, fragile browser/API dependencies.
- Theory gap: unclear why the agent loop works or when multi-agent helps.

## Ranking Follow-Up Ideas

Rank ideas by:

- Feasibility: can be done quickly with available tools and data.
- Evidence value: produces a clear answer, not just another demo.
- Novelty: more than applying an existing framework unchanged.
- Transfer value: likely useful across tasks or agent systems.
- Cost: model, token, environment, annotation, and engineering cost.

## Final Synthesis Pattern

End with a synthesis, not only a table:

```text
综合来看，这组论文说明 ...
证据最扎实的结论是 ...
最有意思但证据还不足的 claim 是 ...
下一步最值得做的实验是 ...
```
