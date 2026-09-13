# NEXT_TASK

## 唯一下一任务

> Complete **Phase-A Field Census Round 2**: fill the remaining planning-centric WAM landscape gaps until the field map reaches sufficient 50–80-work coverage, then freeze breadth expansion and select representative anchor papers for deep reading.

Active plan:

`landscape/FIELD_RECONSTRUCTION_PLAN.md`

Taxonomy:

`landscape/PLANNING_WAM_TAXONOMY.md`

Living atlas:

`landscape/FIELD_ATLAS.md`

Round-1 census:

`landscape/CENSUS_PHASE_A_ROUND1.md`

## Current progress

Round 1 has provisionally placed roughly **45 unique works / benchmarks / control systems** across F1–F11.

The map now contains early coverage of:

```text
visual/video WMs
occupancy/BEV/geometric WMs
latent/JEPA/predictive representations
world-model-assisted planning
candidate/action-conditioned futures
unified world-action models
interactive prediction/planning predecessors
reactive simulation
reward/value/safety interfaces
strong non-WM E2E controls
planning benchmarks/evaluation regimes
```

No research-gap verdict has been issued.

## Round 2 — fill missing coverage, not gaps

Priority coverage holes:

1. **Strong non-WM E2E controls**
   - Hydra-MDP family
   - DriveSuprim
   - iPad
   - representative modern VLA planners

2. **World-model RL / policy-learning lineage**
   - Think2Drive and related latent-WM RL driving work
   - distinguish simulator world model from planner world model

3. **Representation-pretraining bridges**
   - ViDAR
   - GenAD
   - only include additional pretraining WMs if they help explain the transition into planning-centric WMs

4. **Benchmark / evaluation evolution**
   - nuScenes planning protocol
   - nuPlan OL / CL-NR / CL-R
   - NAVSIM v1 / v2
   - Bench2Drive
   - HUGSIM
   - reactive-world benchmarks

5. **Operational/deployment properties**
   - whether the future-model branch survives at inference
   - action/candidate count
   - rollout/planning horizon
   - latency/FPS when reported
   - real-vehicle closed-loop evidence, if any

6. **Uncertainty / multimodality**
   - determine how major families represent multiple plausible futures and whether the planner actually consumes that uncertainty

## Per-paper census output

For every new work record only field-placement facts:

```text
Paper
Year / venue
Family labels
World state representation
Predictive/generative mechanism
World-model role
Action conditioning
Interaction/reactivity level
Planning interface
Planning output
Supervision
Evaluation regime
Decision-evidence strength
Main contribution
Main stated limitation
Historical importance / transition role
Placement confidence
```

Do **not** write novelty or gap verdicts.

## Phase-A stop condition

Freeze breadth expansion when:

1. the census contains roughly 50–80 reasonably placed works;
2. F1–F11 each have enough coverage to explain why that family exists;
3. 2023–2026 historical transitions can be narrated without relying on one survey taxonomy;
4. benchmark differences are explicit enough to prevent false cross-paper comparison;
5. strong non-WM planning controls are represented;
6. a 15–25 paper deep-read anchor set can be justified by field coverage rather than by P1/P2-R/P3.

Then begin Phase B anchor deep reads.

## Parked hypotheses

P1/P2-R/P3 remain provenance and diagnostic probes only. Do not optimize Round 2 around proving, rescuing, or killing them.

Do not design methods. Do not declare a gap. Do not force risk-field knowledge into the atlas.