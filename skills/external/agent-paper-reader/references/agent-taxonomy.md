# Agent Taxonomy

Use this reference when classifying an AI agent paper or naming its components.

## Common Agent Paper Topics

- Planning: decomposes goals into steps, subgoals, plans, programs, or search trees.
- Tool use: selects and calls APIs, functions, search engines, browsers, code interpreters, databases, or domain tools.
- Memory: stores and retrieves observations, summaries, user preferences, trajectories, reflections, or documents.
- Reflection and critique: evaluates intermediate outputs, diagnoses failure, revises plans, or verifies answers.
- RAG agent: combines retrieval with iterative reasoning, tool calls, or long-horizon task execution.
- Web agent: interacts with websites through DOM, screenshots, browser actions, or web APIs.
- GUI agent: operates desktop or mobile UI through screenshots, accessibility trees, or coordinate actions.
- Coding agent: edits repositories, runs tests, debugs failures, and creates patches.
- Multi-agent system: coordinates multiple role-specialized or debate-style agents.
- Workflow agent: uses a fixed or semi-fixed graph of steps, often with LLM calls at nodes.
- Agent benchmark: defines tasks, environments, metrics, and evaluation harnesses.

## Component Vocabulary

- Backbone model: the LLM or VLM used for reasoning and action generation.
- State: the information currently available to the agent.
- Memory: information persisted across steps, tasks, or sessions.
- Planner: module that creates or updates plans.
- Executor: module that performs actions or tool calls.
- Tool interface: schema, API, function signature, browser action, or environment action space.
- Observation: result returned by tools or environment after an action.
- Critic/verifier: module that judges correctness, detects errors, or decides whether to continue.
- Retriever: module that selects documents, memories, examples, or prior trajectories.
- Policy: rule or model that maps state to action.
- Controller/orchestrator: code or prompt that manages the agent loop.
- Stopping rule: condition for returning a final answer or ending execution.

## Agent Loop Template

```text
Task/Input
-> State construction
-> Planning or reasoning
-> Action/tool selection
-> Tool/environment execution
-> Observation parsing
-> Memory update or reflection
-> Continue, revise, or stop
```

## Classification Questions

- Is the main novelty in reasoning, tool use, memory, evaluation, training, or orchestration?
- Is the agent loop dynamic, or is it mostly a fixed workflow?
- Is the method inference-only, or does it require training/fine-tuning/RL?
- Does the agent interact with a real environment or only simulate actions in text?
- Does the method depend on closed-source models, proprietary tools, or hidden prompts?
- Does the paper evaluate the agent system or just the underlying model?
