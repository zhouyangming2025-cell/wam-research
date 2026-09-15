# NEXT_TASK

## 唯一下一任务

> **Convert the adversarially validated Tier-1 WAM tensions into narrow falsifiable candidate research problems, then attack novelty overlap against the nearest 2025–2026 autonomous-driving literature before any method design.**

Completed prerequisite:

```text
audits/research_synthesis/WAM_TIER1_TENSION_ADVERSARIAL_VALIDATION_V1.md
landscape/WAM_RESEARCH_TENSIONS_V2_VALIDATED.md
```

Validated statuses:

```text
T2  SURVIVES — NARROWED
T3  PARTIALLY RESOLVED
T5  PARTIALLY RESOLVED — H2 strengthened
T6  SURVIVES — NARROWED
```

---

# Task 1 — Write one minimal problem statement per surviving tension

Each statement must contain exactly:

```text
1. observable failure
2. causal/mechanistic hypothesis
3. negative control
4. intervention variable
5. measurable outcome
6. falsification criterion
```

Do not start from a desired architecture.

---

# T2 candidate-problem formulation

Narrow question:

> When does online action-conditioned branching provide decision information that cannot be amortized into a compact world state or policy under matched compute/data?

Required experimental axis:

```text
A compact world state → direct policy
B candidate → endpoint future → selection
C candidate → recurrent future rollout → selection
```

Control:

```text
same perception
same candidate support where applicable
same data
matched deployment latency/FLOPs
same utility/evaluator target
```

Stratify by:

```text
interaction-response dependence
candidate ambiguity
OOD/rarity
```

---

# T3 candidate-problem formulation

Narrow question:

> Which future/consequence computations can be amortized into a distilled policy, and which require online recomputation?

Required teacher/student test:

```text
online world/consequence teacher
vs
matched distilled/action-only student
```

Measure teacher-student gap against:

```text
scene rarity
OOD distance
interaction difficulty
uncertainty
candidate disagreement
```

Nearest-neighbor novelty checks must include at minimum:

```text
WPT (CVPR 2026)
Dreamer-style policy learning from imagination
WAM distillation / Fast-WAM / related transfer methods
```

Any candidate problem that reduces to `distill WM into policy` is already too broad / too close to prior art.

---

# T5 candidate-problem formulation

Narrow question:

> How can a planning-centric WAM learn and validate intervention-correct consequences when alternative ego actions change both episode-specific outcomes and surrounding-agent responses?

Mandatory distinction:

```text
conditional prediction
interventional prediction
episode-specific counterfactual
reactive counterfactual
```

Nearest-neighbor novelty checks must include:

```text
How Can Driving World Models Do Counterfactual Prediction? (2026-08)
causal confusion / intervention learning
TrafficBots / reactive data-driven simulation
WOSAC / Waymax
recent counterfactual driving models
```

Do not claim novelty for merely adding alternative ego actions.

---

# T6 candidate-problem formulation

Narrow question:

> What marginal planning value does explicit ego-conditioned reaction-distribution modeling add beyond a strong structured interaction representation?

Required matched contrast:

```text
A structured interaction representation only
B A + ego-conditioned mean response
C A + ego-conditioned multi-modal reaction distribution
```

Evaluation must stratify:

```text
low response dependence
high response dependence:
merge / yield / negotiation / cut-in / unprotected interaction
```

Nearest-neighbor checks:

```text
M2I
GameFormer
DIPP / GET-DIPP
TrafficBots
Reaction-Uncertainty-Aware Motion Planning (2026)
other 2025–2026 ego-conditioned prediction-planning papers
```

Any proposal that is simply `predict surrounding reactions conditioned on ego plan` is not novel.

---

# Task 2 — Build nearest-neighbor overlap matrix

Create:

```text
landscape/WAM_CANDIDATE_PROBLEM_OVERLAP_MATRIX_V1.md
```

For each candidate problem record:

```text
nearest paper
same problem?
same supervision?
same intervention?
same planner interface?
same evaluation regime?
what remains different?
novelty risk: HIGH / MEDIUM / LOW
```

Search recency emphasis:

```text
2025–2026 first
then older foundational work
```

---

# Task 3 — Researchability / falsifiability matrix

Create:

```text
landscape/WAM_CANDIDATE_PROBLEM_RESEARCHABILITY_V1.md
```

Score each candidate on:

```text
scientific importance
prior-art overlap
falsifiability
required data burden
required simulator burden
required compute
source-code availability
ability to build matched controls
risk of benchmark artifact
```

Do not optimize for ease alone.

---

# Task 4 — Determine whether any candidate can become a research gap

A candidate can be promoted only if:

```text
1. survives nearest-neighbor attack;
2. unresolved variable is explicit;
3. matched negative control is feasible;
4. evaluation can distinguish competing explanations;
5. not already answered by a different research community;
6. planning relevance is evidenced, not assumed.
```

Allowed labels after this task:

```text
REJECT — PRIOR ART
REJECT — NOT FALSIFIABLE
HOLD — INFRA TOO HEAVY
SURVIVES — CANDIDATE RESEARCH PROBLEM
```

Still do not design the final method in this round.

---

# Specific warning for risk-aware direction

The user's prior risk/risk-field expertise can become relevant only AFTER the problem survives.

Do not formulate:

```text
we know risk field, therefore add risk field to WAM
```

Instead test whether a surviving problem truly requires an explicit representation of:

```text
risk
reaction uncertainty
future utility
hazard sensitivity
```

GraphWorld is the required negative control because it improves collision behavior without an explicit risk state.

---

# Stop condition

This phase is complete only when:

```text
candidate problem statements complete
+
nearest-neighbor overlap matrix complete
+
researchability matrix complete
+
at least one candidate either rejected or survives with a precise novelty boundary
```

Until then:

```text
NO final method architecture
NO paper-title brainstorming
NO novelty claim
```
