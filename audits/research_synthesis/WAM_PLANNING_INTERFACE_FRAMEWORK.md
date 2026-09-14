# WAM Planning Interface Framework

## Purpose

This document defines a cross-paper analysis framework for world-model-based autonomous driving planning. The goal is not to summarize papers by their own section structure, but to analyze where future modeling is placed inside the planning system.

## Central Question

The key question is:

> Why does a method predict the future, and where does that future enter the planning loop?

A unified abstraction is:

`Current World + Action -> Future World Representation -> Planning`

## Dimension 1: World Model Role

| Method type | Role |
|---|---|
| Future as training signal | Future prediction improves representation/planner learning |
| Future as evaluator | Future prediction scores candidate decisions |
| Future as generator | Future generation models possible world evolution |
| Future as decision representation | Future-aware latent becomes planning state |

## Dimension 2: Planner Relationship

Important distinction:

- Training-only world model: future prediction affects gradients but not inference.
- Decision-time world model: future prediction directly influences action selection.

## Dimension 3: Action Role

Trajectory may be:

1. output of planner;
2. condition of world model;
3. candidate variable evaluated by world model;
4. part of joint future generation.

## Dimension 4: Future Supervision

Important audit questions:

- What is the future target?
- Is it RGB, BEV, latent representation, trajectory, or reward-related state?
- Is the supervision observational or counterfactual?

## Dimension 5: Main Research Bottleneck

The key unresolved problem is not future prediction alone:

`P(Future | History)`

but:

`P(Future | History, Candidate Action)`

because autonomous driving requires evaluating alternative futures.

## Final Analysis Principle

Future prediction should be evaluated by its position in the decision pipeline, not only by the prediction modality.
