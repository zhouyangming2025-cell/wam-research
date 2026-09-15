# Reproduction Checklist

Use this reference when the user asks whether an agent paper can be implemented, reproduced, or turned into a project.

## Required Details

Check whether the paper provides:

- Code repository and license.
- Model names, versions, temperatures, decoding parameters, and context lengths.
- Full prompts, system messages, tool schemas, and examples.
- Agent loop pseudocode or algorithm.
- Memory format and retrieval/update rules.
- Tool execution environment and sandbox assumptions.
- Dataset, benchmark split, task list, and evaluation harness.
- Baseline configurations.
- Cost, number of calls, retries, and stopping conditions.
- Failure-handling rules.

Missing prompts, tool schemas, or evaluator details are serious reproducibility gaps for agent papers.

## MVP Reproduction Plan

When proposing a reproduction, keep it small:

1. Select one representative task or benchmark subset.
2. Implement the minimal agent loop.
3. Use one backbone model and one baseline.
4. Reproduce one main table row or one ablation.
5. Log every prompt, tool call, observation, retry, cost, and failure.
6. Compare against the paper's reported result and explain mismatches.

## Engineering Risk

Rate risk as low, medium, or high:

- Low: open code, open data, explicit prompts, deterministic evaluation, small compute/API cost.
- Medium: partial code or prompts, moderate environment setup, some closed models, manageable cost.
- High: no code, hidden prompts, closed environments, high API cost, web/GUI drift, vague evaluator, or many moving parts.

## Implementation Decomposition

Break the method into files or modules:

- `agent_loop`: orchestrates state, action, observation, and termination.
- `prompts`: system prompts, action prompts, reflection prompts, verifier prompts.
- `tools`: tool schemas and execution wrappers.
- `memory`: storage, retrieval, summarization, update rules.
- `evaluator`: benchmark runner and scoring.
- `logging`: trajectory, cost, and failure trace capture.
- `baselines`: simple baseline agents for fair comparison.

## First Experiment

Recommend the smallest experiment that tests the paper's core claim:

- If the claim is planning, compare with and without planner under equal tool-call budget.
- If the claim is memory, compare no-memory, summary-memory, and retrieval-memory.
- If the claim is reflection, compare no-reflection vs reflection with equal retries.
- If the claim is multi-agent, compare against a single agent with equal context and call budget.
- If the claim is benchmark quality, manually inspect a sample for validity and evaluator errors.
