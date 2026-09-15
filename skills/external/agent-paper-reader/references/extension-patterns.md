# Extension Patterns

Use this reference when proposing what to do after reading an agent paper.

## Method Improvements

- Replace a fixed prompt step with a learned or adaptive policy.
- Add a verifier that checks tool outputs, constraints, or final answers.
- Reduce cost with early stopping, smaller models, caching, or selective tool use.
- Improve memory with structured state, retrieval filters, forgetting rules, or provenance.
- Add uncertainty estimation or confidence-based fallback.
- Make the agent loop observable with trajectory logs and error taxonomy.

## Evaluation Improvements

- Re-run on a harder or less contaminated benchmark.
- Add cost, latency, tool-call count, and invalid-action metrics.
- Compare under equal model, context, tool, and retry budgets.
- Add human evaluation only where automatic metrics are unreliable.
- Test model transfer across open and closed models.
- Stress-test with environment drift, noisy observations, or adversarial tool outputs.

## Domain Transfers

- Move a general agent method to coding, research, web navigation, GUI control, data analysis, or enterprise workflow automation.
- Replace toy tools with real APIs and measure reliability.
- Convert a benchmark task into a realistic workflow with partial observability and changing state.
- Use domain-specific memory, retrieval, or validators.

## Combination Ideas

- Planning method + stronger verifier.
- Tool-use method + structured memory.
- Multi-agent debate + single-agent self-consistency baseline.
- RAG agent + trajectory-level reflection.
- Coding agent + test-generation loop.
- Web/GUI agent + accessibility tree plus screenshot grounding.

## Research Direction Ranking

Rank follow-up ideas by:

- Feasibility: can it be implemented in days or weeks?
- Novelty: is it more than applying the paper unchanged?
- Evidence value: will the experiment clearly prove or disprove something?
- Cost: token, compute, data labeling, and environment maintenance.
- Relevance: does it connect to the user's own project or research goal?

## Output Format for Follow-Up Ideas

```text
Idea:
What changes:
Why it may work:
Smallest experiment:
Expected evidence:
Main risk:
```
