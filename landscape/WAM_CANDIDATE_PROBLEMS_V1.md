# WAM Candidate Research Problems V1

Last updated: 2026-09-15

Status: **POST-TIER-1 VALIDATION — MINIMAL FALSIFIABLE PROBLEMS, NOT METHOD PROPOSALS**

Source basis:

```text
11-anchor WAM normalization
+ WAM_RESEARCH_TENSIONS_V2_VALIDATED.md
+ WAM_TIER1_TENSION_ADVERSARIAL_VALIDATION_V1.md
+ 2025–2026 nearest-neighbor overlap attack
```

Allowed outcome labels in this round:

```text
REJECT — PRIOR ART
REJECT — NOT FALSIFIABLE
HOLD — INFRA TOO HEAVY
SURVIVES — CANDIDATE RESEARCH PROBLEM
```

No architecture is proposed here.

---

# CP-T2 — Conditional value of online consequence branching

## Minimal problem statement

### 1. Observable failure

Compact world-state/direct-policy approaches can perform strongly on average, but it is not established whether they lose information specifically in scenes where multiple ego alternatives induce materially different downstream consequences.

### 2. Mechanistic hypothesis

```text
Online action-conditioned branching has marginal value
only when the current scene has high consequence ambiguity / response dependence.
```

The claimed mechanism is not `more compute is better`; it is that scene-specific alternative consequences cannot always be amortized into one compact state/policy representation.

### 3. Negative control

```text
A. compact decision-relevant W → direct policy
```

trained with the same observations, future supervision and planning/value targets as the online variants.

### 4. Intervention variable

Under one perception/backbone/data budget, change only the online decision mechanism:

```text
A. compact W → direct policy
B. candidate → endpoint future latent → selection
C. candidate → recurrent consequence rollout → selection
```

Match deployment latency/FLOPs as closely as possible and separately report an unconstrained-compute oracle.

### 5. Measurable outcome

At minimum:

```text
planning score / success
collision / TTC-like safety
candidate-selection regret
latency / FLOPs
performance as a function of:
  interaction-response dependence
  candidate ambiguity
  OOD / rarity
```

### 6. Falsification criterion

The hypothesis is weakened/falsified if, after matching training information and compute:

```text
B/C do not outperform A in high-response/high-ambiguity scenes,
OR any gain is uniform across easy and hard scenes,
OR the gain is explained by larger candidate support / evaluator supervision rather than online consequence information.
```

## Nearest-neighbor pressure

Relevant 2026 work already includes explicit future-centric planning (ProDrive, ForeSight), adaptive hard-scene reasoning (CF-VLA), and uncertainty-triggered extra world-model reranking (UTMR). Therefore novelty cannot be `use world rollouts on hard scenes` or `adapt compute to uncertainty`.

## Current verdict

```text
SURVIVES — CANDIDATE RESEARCH PROBLEM
NOVELTY RISK: MEDIUM
```

Novelty boundary:

> The surviving scientific contribution would have to be the **matched causal decomposition of when branching adds information beyond compact conditioning**, not a new rollout module or trigger alone.

---

# CP-T3 — Non-amortizable world reasoning after distillation

## Minimal problem statement

### 1. Observable failure

World-model teachers can be distilled into fast policies, but a teacher-student gap may remain on rare/OOD/interactive scenes.

### 2. Mechanistic hypothesis

Some scene-specific consequence computations depend on alternatives/uncertainty available only at test time and cannot be fully compressed into fixed policy weights.

### 3. Negative control

A WPT/Fast-WAM-style policy-only student trained from the same world-aware teacher/data.

### 4. Intervention variable

```text
action-only distilled student
vs
student + online world/consequence fallback
```

with trigger variables such as disagreement, uncertainty or OOD score.

### 5. Measurable outcome

Teacher-student gap as a function of rarity, OOD distance, interaction difficulty, candidate disagreement and runtime.

### 6. Falsification criterion

If a matched distilled student closes the gap across hard/OOD strata, the hypothesis that online recomputation is necessary is falsified.

## Nearest-neighbor pressure

This formulation is now heavily occupied:

```text
WPT (CVPR 2026): online WM teacher → policy/world-reward distillation
Fast-WAM (2026, robotics): world/video co-training → future-imagination-free inference
CF-VLA (CVPR 2026): adaptive reasoning only on difficult scenes
UTMR (IV Workshops 2026): uncertainty-triggered extra world-model reranking
```

The combination `distill most reasoning + invoke extra reasoning when uncertain/hard` is therefore no longer a clean standalone novelty claim.

## Current verdict

```text
REJECT — PRIOR ART as an independent research direction
```

Residual scientific variable retained:

```text
amortizable vs scene-specific consequence information
```

This variable is folded into CP-T2 rather than pursued as a separate method problem.

---

# CP-T5 — Episode-specific reactive counterfactual consequences for planning

## Minimal problem statement

### 1. Observable failure

Direct action-conditioned driving world models can generate plausible alternative futures but can fail to recover the matched counterfactual outcome of the same episode. Existing matched-counterfactual driving-WM evidence intentionally removes the harder case where surrounding agents react to the ego intervention.

Meanwhile, reactive simulation work evaluates whether agents respond to AV deviations, but does not by itself establish episode-specific counterfactual identification for planning-centric WAMs.

### 2. Mechanistic hypothesis

```text
A planning-centric WAM trained mainly on factual trajectories is systematically unreliable
for alternative ego actions when BOTH:
  a) episode-specific latent causes must be preserved (abduction problem), and
  b) surrounding-agent responses change under the intervention (reactivity problem).
```

Correct consequence estimation requires more than adding an alternative ego action token/trajectory.

### 3. Negative control

```text
Direct factual/action-conditioned WAM:
history + alternative ego action → future
```

without explicit episode-specific evidence transfer and without reactive/intervention-diverse supervision.

Required secondary controls:

```text
factual prediction only
matched-counterfactual but non-reactive setting
reactive simulation without episode-specific counterfactual target
```

### 4. Intervention variable

Use a controlled simulator or repeatable reactive world where the same initial latent world/seed is replayed under multiple ego interventions.

For each initial episode:

```text
factual ego action a
alternative action a'
reactive surrounding-agent policy fixed as the environment mechanism
→ matched Y(a), Y(a')
```

Vary response dependence from low to high.

### 5. Measurable outcome

Separate metrics for:

```text
factual future accuracy
matched counterfactual state/trajectory accuracy
surrounding-agent response accuracy
counterfactual collision / interaction outcome accuracy
planning regret when consequences are used for selection
calibration / ranking consistency across ego alternatives
```

### 6. Falsification criterion

The hypothesis is weakened/falsified if a standard direct action-conditioned model trained on factual data:

```text
matches the episode-specific reactive counterfactual targets,
maintains accuracy as response dependence increases,
and yields no planning-regret gap against models using stronger counterfactual/reactive information.
```

## Nearest-neighbor pressure

Three 2026 lines cover different pieces but not the full intersection:

```text
How Can Driving World Models Do Counterfactual Prediction?
→ matched episode-specific counterfactual ground truth
→ deliberately non-reactive surrounding agents

ReactSim-Bench
→ standardized reactive agent response to AV deviations
→ not a matched episode-specific counterfactual planning benchmark

CausalDrive
→ real-time reactive visual world renderer / driving sociology
→ reactive simulation, but not the same matched factual-vs-reactive-counterfactual identification question
```

Additional overlap: AWM uses world models/adversarial multi-agent self-play for hard interactions; it increases long-tail pressure but asks a different robustness-training question.

## Current verdict

```text
SURVIVES — CANDIDATE RESEARCH PROBLEM
NOVELTY RISK: MEDIUM-LOW, BUT FAST-MOVING
```

Novelty boundary:

> The candidate is **not** `make a reactive world model` and not `make a counterfactual world model`. It is the measurable intersection of **episode-specific counterfactual identification + ego-intervention-dependent surrounding-agent response + planning utility**.

---

# CP-T6 — Marginal value of reaction distributions beyond structured interaction representations

## Minimal problem statement

### 1. Observable failure

A strong structured interaction representation can improve safety without explicit reactive prediction, yet negotiation-heavy scenes may remain ambiguous because surrounding-agent response is multi-modal and ego-dependent.

### 2. Mechanistic hypothesis

Explicit ego-conditioned reaction distributions add planning value mainly in high-response-dependence scenes beyond what a strong structured interaction representation already captures.

### 3. Negative control

GraphWorld-like structured interaction/world representation with no explicit per-ego-plan reaction distribution.

### 4. Intervention variable

```text
A. structured interaction representation only
B. A + ego-conditioned mean/unimodal response
C. A + ego-conditioned multimodal reaction distribution
```

### 5. Measurable outcome

Planning score, collision, yielding/merge success, calibration and regret stratified by response dependence.

### 6. Falsification criterion

If B/C do not add selective gains over A in negotiation-heavy scenes, explicit reactive distribution modeling is unnecessary for the tested regime.

## Nearest-neighbor pressure

The core mechanism is already close to established prior art:

```text
M2I / GameFormer: conditional/interactive prediction
Reaction-Uncertainty-Aware Motion Planning (2026): conditional multimodal response + tree planner, up to 32.39% gain vs unimodal conditional baseline
2026 ego-conditioned prediction + gap-driven planning: candidate ego plans → surrounding responses
ProDrive: ego-environment co-evolution in end-to-end planning
ReactSim-Bench: direct reactive-capability evaluation
```

The exact `strong structured representation only` negative control remains scientifically useful, but that alone is too thin a novelty boundary for a standalone direction.

## Current verdict

```text
REJECT — PRIOR ART as an independent research direction
```

Residual variable retained:

```text
response dependence / reaction uncertainty
```

This becomes a required stratification/intervention axis inside CP-T5 and CP-T2.

---

# Round result

After nearest-neighbor attack:

```text
CP-T2  SURVIVES — CANDIDATE RESEARCH PROBLEM
CP-T3  REJECT — PRIOR ART (merge scientific variable into T2)
CP-T5  SURVIVES — CANDIDATE RESEARCH PROBLEM
CP-T6  REJECT — PRIOR ART (merge reaction axis into T5/T2)
```

Priority for the next round:

```text
1. CP-T5 — strongest novelty boundary, strongest causal falsifiability, heaviest simulator/data burden
2. CP-T2 — strong scientific value, moderate novelty boundary, difficult compute-matching design
```

No final research gap or method architecture is authorized yet.
