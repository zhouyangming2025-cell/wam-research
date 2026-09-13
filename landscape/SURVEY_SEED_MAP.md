# SURVEY_SEED_MAP

Last updated: 2026-09-14

Purpose: seed the field census from multiple recent surveys without allowing any single survey taxonomy to define the project.

This is a **navigation artifact**, not scientific authority. Representative primary papers must still be read directly.

## 1. Why multiple surveys are needed

A single taxonomy is not enough for a planning-centric WAM map because the field can be organized along different, non-equivalent axes:

```text
what future state is predicted
what role the world model plays
how prediction and planning interact
what the planner outputs
what supervision is available
how interaction/reactivity is modeled
how planning is evaluated
```

Recent surveys emphasize different subsets of these axes. The atlas should combine them rather than choose one.

## 2. Seed surveys

### S1 — Tu et al., “The Role of World Models in Shaping Autonomous Driving: A Comprehensive Survey”

Publication: Frontiers of Computer Science, accepted/published online 2026.

Public source:

`https://journal.hep.com.cn/fcs/EN/10.1007/s11704-026-60102-1`

Useful taxonomy signal:

- organizes driving world models primarily by **predicted scene modality/state**;
- includes video, point cloud, occupancy, latent feature and traffic-map style representations;
- connects generation and driving applications;
- reviews datasets/metrics and limitations.

Atlas use:

Strong seed for **world-state representation** and DWM ecosystem coverage, but insufficient by itself for planning-interface analysis.

### S2 — Feng, Wang, Yang, “A Survey of World Models for Autonomous Driving”

arXiv:2501.11260.

Public source:

`https://arxiv.org/abs/2501.11260`

Useful taxonomy signal:

Three broad tiers:

```text
generation of future physical world
behavior planning for intelligent agents
interaction between prediction and planning
```

Atlas use:

Useful bridge between pure future generation and planning/interaction. Helps prevent the atlas from becoming only a modality catalog.

### S3 — Li, Zhang, Zhao, “Ranging from prediction to planning via machine learning approaches for autonomous driving: a survey”

Artificial Intelligence Review, 2026.

Public source:

`https://link.springer.com/article/10.1007/s10462-026-11604-8`

Useful taxonomy signal:

- traces progression from marginal prediction to conditional prediction to integrated/interactive prediction and planning;
- discusses scene comprehension, trajectory decoding, safety, robustness, generalization and deployment;
- explicitly distinguishes open-loop and closed-loop experimental platforms/evaluation.

Atlas use:

Critical historical/control source for **F7 interactive prediction + planning predecessors** and for understanding which WAM ideas have older prediction/planning roots.

### S4 — Guan et al., “Planning-Oriented End-to-End Autonomous Driving: Architectures, Evaluation, and Emerging Paradigms”

arXiv:2608.20111.

Public source:

`https://arxiv.org/abs/2608.20111`

Useful taxonomy signal:

Organizes planning-oriented E2E driving around axes such as:

```text
input representation
planning output
supervision signal
evaluation protocol
```

and situates world-model-based planners and VLA systems inside the broader E2E planning landscape.

Atlas use:

Critical for **F10 strong non-WM end-to-end planner controls** and for preventing WAM-only tunnel vision.

### S5 — Yin & Tian, “World models in autonomous driving: A review and outlook”

Journal of Harbin Institute of Technology, 2025.

Public source:

`https://hit.alljournals.cn/hitxb_cn/article/html/20251211`

Useful taxonomy signal:

Highlights three application directions:

```text
future scene generation and understanding
end-to-end driving policy learning
data-driven closed-loop simulation
```

Atlas use:

Useful high-level application-role split and a reminder that closed-loop simulation is a distinct world-model role, not simply another generation benchmark.

## 3. Combined lesson for our taxonomy

No single organizing axis is sufficient.

The project therefore uses a **multi-axis placement**:

```text
A. world-state representation
B. predictive/generative mechanism
C. world-model role
D. action/intent conditioning
E. interaction/reactivity level
F. planning interface
G. planning output
H. supervision
I. evaluation regime
J. decision-evidence strength
K. operational properties
```

See:

`landscape/PLANNING_WAM_TAXONOMY.md`

## 4. First census construction rule

Use surveys to discover candidate papers, but every paper that becomes an atlas anchor must be verified from its own primary source.

During census placement:

```text
NO GAP VERDICT
NO NOVELTY VERDICT
NO P2-R SCORE
```

Only record its field position, technical interface, evidence regime and historical role.

## 5. Immediate census coverage targets

First pass should deliberately sample across:

```text
visual/video WMs
occupancy/BEV/geometric WMs
latent/JEPA WMs
planning-coupled WMs
candidate/action-conditioned WMs
unified world-action models
interactive prediction/planning predecessors
reactive simulation / closed-loop training
reward/value/safety interfaces
strong non-WM E2E planners
benchmarks/evaluation
```

The current Batch 0A papers will be reclassified into these axes but will not be treated as a representative sample.
