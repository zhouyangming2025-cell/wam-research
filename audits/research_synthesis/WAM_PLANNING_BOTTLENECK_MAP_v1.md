# WAM Planning Bottleneck Map v1

## Purpose

This document records the current cross-paper research synthesis. The unit of analysis is not the paper module, but the role of future information inside planning.

## Core question

Traditional end-to-end driving learns:

`Observation -> Action`

However planning requires reasoning about consequences:

`Observation + Action -> Future consequence -> Decision`

Therefore the key question for WAM is not only "what future is predicted", but "how future information changes planning".

## Evolution axis

```
Future as training signal
        |
        v
Future as decision evidence
        |
        v
Future as generated world
        |
        v
Future as planning state
        |
        v
Future as interactive environment
```

## Current bottleneck hypotheses

### 1. Counterfactual future

Real datasets mainly provide:

`(history, expert action, observed future)`

Planning requires:

`(history, candidate action, corresponding future consequence)`

The missing mapping is:

`P(Future | History, Action)`

rather than only:

`P(Future | History)`.

### 2. Future representation versus decision relevance

A better future representation does not automatically mean a better planner. The field still needs clearer understanding of:

`future state -> planning relevance -> action quality`

### 3. Agent interaction

Many approaches model ego-conditioned futures but may simplify other agents. A realistic WAM needs:

`ego action + other agent response -> future evolution`

### 4. Evaluation gap

Higher prediction quality or rollout quality does not necessarily prove better decision making. Evaluation should connect world prediction to planning outcomes.

## Research direction tracking

Risk-related ideas should be treated as a possible interface, not an assumption. The current hypothesis is:

`future world representation -> importance/relevance representation -> planning`

This requires validation against existing WAM methods.

## Status

Version: v1
Scope: LAW, WoTE, Epona, WorldDrive and future WAM audits.
