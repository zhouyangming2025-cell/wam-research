# NEXT_TASK

## 唯一下一任务

> Ingest and scientifically audit the **direct P2-R literature set** before any method design or experiment.

Priority papers:

1. BridgeSim
2. ReactSim-Bench
3. CausalDrive
4. How Can Driving World Models Do Counterfactual Prediction?
5. CRAFT

Secondary only if needed:

- What Truly Matters
- Policy World Model
- BeyondDrive
- ELF-VLA

## Scientific question

For fixed current state `s` and fixed ego candidate set `A`, is there direct evidence that allowing surrounding agents to respond to alternative ego interventions changes the ego-action ordering and causes non-trivial planning regret?

```text
rank_factual/nonreactive(A) ?= rank_reactive(A)
```

The mechanism must be attributable to:

```text
ego action
→ surrounding-agent response changes
→ candidate ordering reversal
→ planning regret
```

not merely to generic OL/CL mismatch, observation shift, control error, temporal compounding, or changed candidate coverage.

## Required outputs

For each direct paper:

- exact problem and evaluation regime;
- whether candidate ego actions are explicitly conditioned;
- whether other-agent response changes with ego intervention;
- whether the same candidate set is compared;
- whether any action-order reversal is directly measured;
- whether planning regret from that reversal is reported;
- strongest evidence **against** P2-R;
- prior-art occupancy level.

Then produce one adversarial verdict:

```text
P2-R SURVIVES
P2-R KILLED
NONE / EVIDENCE INSUFFICIENT
```

## Stop condition

Stop after the direct-paper adjudication. Do **not** design a model, run full reproduction, restart P1 engineering, or widen P2-R to generic reactive planning.

Batch 0B broad expansion remains paused except insofar as these direct P2-R papers need to be ingested into the corpus.