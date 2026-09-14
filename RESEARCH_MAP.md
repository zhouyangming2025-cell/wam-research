# Research Map — Planning-centric WAM

## Mission

Build a systematic understanding of how World Models transform autonomous driving planning, and identify future research opportunities at the intersection of World Model, End-to-End driving, planning, safety and risk reasoning.

## Current Stage

FIELD RECONSTRUCTION — Planning-centric WAM Atlas

The immediate goal is not to design a model. The goal is to reconstruct the field:

field understanding → taxonomy → contradictions → research question → method

## Evolution of World Model + Planning

```
Traditional E2E:
Image → Planner → Trajectory

LAW:
World Model as training teacher
Future latent prediction improves planner representation

WoTE:
World Model as online evaluator
Candidate action → future prediction → trajectory selection

Epona:
World Model as generative world
Shared latent → trajectory generation + visual future generation

WorldDrive:
Future-aware representation learning
Future world understanding serves planning
```

## Core Research Questions

1. What should a driving world model represent?
2. How should future world knowledge enter planning?
3. Can safety/risk become an explicit part of world representation?
4. How should planners reason over uncertain futures?

## Future Direction

Potential research direction:

Risk-aware World Model Planning

Observation → Future latent world → Risk evolution representation → Planning decision
