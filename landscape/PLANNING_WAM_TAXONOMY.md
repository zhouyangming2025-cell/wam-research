# PLANNING_WAM_TAXONOMY

Last updated: 2026-09-14

Purpose: provide a neutral coordinate system for understanding planning-centric driving world models before gap hunting.

## A. World-state representation

Use one or more labels:

```text
VIDEO_RGB
BEV_FEATURE
OCCUPANCY_FLOW
POINTCLOUD_3D
GAUSSIAN_3D_SCENE
VECTOR_OBJECT_RELATION
TRAJECTORY_BEHAVIOR
LATENT_PREDICTIVE_STATE
REWARD_VALUE_COST
MULTIMODAL_HYBRID
```

## B. Predictive / generative mechanism

```text
AUTOREGRESSIVE_TOKEN
DIFFUSION_FLOW
JEPA_LATENT_PREDICTION
RSSM_LATENT_DYNAMICS
TRANSFORMER_TRAJECTORY_PREDICTION
OCCUPANCY_FORECASTING
GAME_THEORETIC / CONDITIONAL_INTERACTION
HYBRID
```

## C. World-model role in the driving stack

```text
SIMULATOR_ONLY
DATA_GENERATOR
PRETRAINING_REPRESENTATION
AUXILIARY_TRAINING_OBJECTIVE
FUTURE_FEATURE_FOR_DIRECT_PLANNER
CANDIDATE_CONDITIONED_FUTURE
CANDIDATE_SCORER / EVALUATOR
MPC_ROLLOUT_MODEL
REWARD_VALUE_SAFETY_MODEL
RL_ENVIRONMENT / POLICY_IMPROVER
UNIFIED_WORLD_ACTION_MODEL
```

## D. Action / intent conditioning

```text
NONE / HISTORY_ONLY
ROUTE_COMMAND
EGO_STATE
DISCRETE_ACTION
CONTROL_SEQUENCE
EGO_TRAJECTORY
GOAL_INTENTION
MULTI_AGENT_ACTION
POLICY_CONDITIONED
```

Record the exact numerical form, not only yes/no.

## E. Interaction / reactivity level

```text
I0  no explicit interaction model
I1  marginal agent prediction
I2  joint multi-agent prediction
I3  conditional influencer→reactor prediction
I4  ego-action-conditioned surrounding-agent future
I5  branching / contingency planning
I6  game-theoretic / strategic interaction
I7  reactive closed-loop simulator/world agents
```

These levels describe mechanism, not guaranteed correctness.

## F. Planning interface

```text
P0  no planner consumption
P1  world prediction used only during training
P2  future representation conditions direct trajectory decoder
P3  predicted occupancy/geometry enters explicit cost
P4  candidate future enters learned scorer
P5  per-action rollout used for selection / MPC
P6  learned cost/reward optimized by planner
P7  world model used for RL / policy improvement
P8  trajectory/action and world generated jointly
```

## G. Planning output

```text
DIRECT_TRAJECTORY
TRAJECTORY_DISTRIBUTION
CANDIDATE_SET_AND_SCORE
CONTINUOUS_OPTIMIZATION
CONTROL_SEQUENCE
POLICY_ACTION
HIERARCHICAL_INTENT_TRAJECTORY
```

## H. Supervision

```text
FUTURE_PIXEL / VIDEO
FUTURE_BEV / OCCUPANCY / GEOMETRY
FUTURE_LATENT_SELF_SUPERVISION
AGENT_TRAJECTORY
EXPERT_EGO_TRAJECTORY
PLANNING_METRIC / RULE
RANKING / HARD_NEGATIVE
PREFERENCE
RISK / SAFETY_LABEL
COUNTERFACTUAL_PROXY
CLOSED_LOOP_REWARD
SYNTHETIC_SIMULATOR
```

For each supervision source, record whether it exists for all candidate actions or only the executed/logged action.

## I. Evaluation regime

```text
E0  generation quality only
E1  prediction quality only
E2  open-loop ego trajectory matching
E3  non-reactive data-driven planning evaluation
E4  closed-loop non-reactive simulation
E5  reactive closed-loop simulation
E6  CARLA / Bench2Drive style interactive simulation
E7  real-vehicle closed loop
```

Multiple labels allowed. Never treat E0/E1 as evidence of planning competence.

## J. Decision evidence strength

For planning claims, annotate:

```text
D0  no planning evidence
D1  auxiliary correlation / proxy
D2  end-to-end planning benchmark improvement
D3  matched ablation showing future-model contribution
D4  direct candidate/action consequence comparison
D5  reactive closed-loop causal evidence
D6  real-world closed-loop evidence
```

This is an evidence hierarchy, not a model-quality ranking.

## K. Operational properties

Record where reported:

- input sensors;
- history horizon;
- prediction horizon;
- planning horizon;
- candidate count;
- spatial/temporal resolution;
- model size;
- training data scale;
- inference FLOPs / latency / FPS;
- autoregressive rollout length;
- uncertainty/multimodality representation;
- whether deployment removes training-time WM branches.

## L. Per-paper census record

Use this compact template for breadth mapping:

```text
Paper:
Year / venue:
Family labels:
World state:
WM mechanism:
WM role:
Action conditioning:
Interaction/reactivity:
Planning interface:
Planning output:
Supervision:
Evaluation regime:
Decision evidence strength:
Main contribution:
Main limitation stated by authors:
Why historically important:
Confidence in placement: HIGH / MEDIUM / LOW
```

No gap verdict in census records.
