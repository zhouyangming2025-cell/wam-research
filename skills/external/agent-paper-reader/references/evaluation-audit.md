# Evaluation Audit

Use this reference when judging whether an agent paper's experiments actually support its claims.

## Claim-Evidence Check

For every important claim, ask:

- What exact metric or experiment supports it?
- Is the benchmark aligned with the claimed real-world capability?
- Is the improvement large enough to matter?
- Does the paper report variance, confidence intervals, or multiple runs?
- Does the paper include failure cases, not only success examples?
- Does the conclusion depend on a single benchmark or a single backbone model?

## Baseline Fairness

Check whether baselines use comparable:

- Backbone model strength.
- Context length and prompt detail.
- Number of tool calls or environment interactions.
- Access to tools, retrievers, memory, or feedback.
- Search budget, retry budget, and inference cost.
- Human-written hints, demonstrations, or templates.
- Training data and benchmark exposure.

If the proposed method gets more budget or better tools, report the comparison as conditional.

## Agent Benchmark Risks

- Leakage: benchmark tasks may appear in model pretraining, public examples, tutorials, or prior benchmark reports.
- Shortcut: task can be solved without the claimed agent capability.
- Brittle evaluator: exact-match or heuristic scoring misses semantically correct outputs or accepts flawed outputs.
- Environment drift: websites, APIs, packages, or GUIs change over time.
- Hidden human intervention: manual resets, retries, prompt tuning, or task filtering.
- Weak baseline: compared against outdated agents, weak prompts, or underconfigured systems.
- Cost blindness: no reporting of tokens, tool calls, wall-clock time, failures, or retries.

## Ablation Questions

- What happens without planning?
- What happens without memory?
- What happens without reflection or verifier?
- What happens with fewer tool calls or retries?
- What happens with a weaker or different backbone model?
- Which module contributes most to the final gain?
- Are prompts, tool schemas, and hyperparameters held fixed?

## Agent-Specific Metrics

Prefer metrics that expose tradeoffs:

- Success rate or pass rate.
- Task completion quality.
- Number of steps or actions.
- Token cost and API cost.
- Wall-clock latency.
- Tool-call failure rate.
- Recovery rate after wrong actions.
- Human intervention count.
- Safety violations or invalid actions.

## Reading Verdicts

Use precise verdict language:

- Strongly supported: multiple fair experiments and ablations support the claim.
- Partially supported: results are positive but scope, baselines, or ablations are limited.
- Weakly supported: evidence exists but could be explained by model strength, budget, prompt tuning, or benchmark artifacts.
- Not established: the paper claims it but does not provide relevant evidence.
