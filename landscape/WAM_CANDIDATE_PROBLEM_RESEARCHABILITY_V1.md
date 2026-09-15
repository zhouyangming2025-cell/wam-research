# WAM Candidate Problem Researchability V1

Last updated: 2026-09-15

Purpose: rank candidate research problems by scientific value, falsifiability, novelty pressure and execution burden. This is **not** a method-ranking document.

Scale:

```text
5 = very favorable / very strong
1 = very unfavorable / very weak
```

For burden/risk columns, a higher number means **heavier burden / higher risk**.

---

# Summary matrix

| Candidate | Scientific importance | Prior-art overlap risk | Falsifiability | Data burden | Simulator burden | Compute burden | Source/code availability | Matched-control feasibility | Benchmark-artifact risk | Current verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **CP-T2 conditional value of online branching** | 5 | 3 | 5 | 3 | 4 | 4 | 3 | 4 | 3 | **SURVIVES — CANDIDATE RESEARCH PROBLEM** |
| **CP-T3 non-amortizable reasoning after distillation** | 4 | **5** | 4 | 3 | 3 | 4 | 3 | 4 | 3 | **REJECT — PRIOR ART standalone** |
| **CP-T5 episode-specific reactive counterfactual consequence** | **5** | 3 | **5** | **4** | **5** | 4 | 4 | **5** | 4 | **SURVIVES — CANDIDATE RESEARCH PROBLEM** |
| **CP-T6 reaction distributions beyond structured representation** | 4 | **5** | 4 | 3 | 4 | 3 | 3 | 4 | 3 | **REJECT — PRIOR ART standalone** |

---

# CP-T2 assessment

## Why it matters

It asks a first-principles WAM design question:

```text
When is online consequence computation genuinely information-bearing,
rather than just an expensive implementation choice?
```

This question can unify apparently conflicting evidence from GraphWorld/Epona versus WoTE/World4Drive/WorldDrive.

## Main strength

The falsification design is clean if one can hold training information and candidate/value supervision fixed while varying only the deployed mechanism.

## Main weakness

Compute matching is difficult. A compact direct policy, endpoint evaluator and recurrent rollout do not naturally consume equal FLOPs or have equal candidate support. Poor matching would reduce the study to another architecture comparison.

## Infrastructure path

Most feasible route:

```text
existing NAVSIM/nuPlan planner backbone
+ one candidate generator
+ one utility/evaluator target
+ three deployment interfaces
+ interaction-difficulty stratification
```

A reactive simulator is strongly preferred for the highest-value claims.

## Researchability judgment

```text
HIGH scientific value
MEDIUM novelty risk
MEDIUM-HIGH engineering burden
```

Keep as candidate #2.

---

# CP-T3 assessment

## Why it matters

The residual teacher-student gap remains scientifically interesting.

## Why it is rejected standalone

The obvious framing and method space are crowded by:

```text
WPT
Fast-WAM
Metis / DynFlowDrive lifecycle controls
CF-VLA adaptive reasoning
UTMR uncertainty-triggered extra reasoning
```

A new paper whose main claim is:

```text
distill a world model into a policy
+
run world reasoning only when uncertain
```

would face severe novelty risk.

## Retained value

Use teacher-student gap / disagreement as one explanatory axis in CP-T2 rather than as a standalone direction.

---

# CP-T5 assessment

## Why it matters

This candidate attacks the strongest evidence boundary exposed by the 11 anchors:

```text
action-conditioned predicted futures are common,
but intervention-correct reactive consequence truth is not established.
```

2026 counterfactual-WM work shows the episode-specific problem is real even before reactivity is introduced. ReactSim-Bench separately shows that reactive capability needs its own protocol. CausalDrive shows real-time reactive visual world simulation is becoming feasible.

The unresolved intersection therefore has both scientific and practical relevance.

## Main strength

The hypotheses are unusually falsifiable because a controlled simulator can produce paired interventions from the same underlying initial world.

A negative result is publishable/scientifically useful:

```text
if factual action-conditioned WAMs already recover reactive counterfactual consequences,
then the causal concern is empirically weaker than expected.
```

## Main weakness

The infrastructure is heavy. Proper validation requires:

```text
repeatable simulator state / seed
reactive surrounding-agent mechanism
multiple ego interventions
paired consequence truth
planning/evaluator integration
scenario response-dependence labels
```

Pure nuScenes/NAVSIM logs are insufficient for the strongest claim.

## Available infrastructure

Encouragingly, several pieces already exist:

```text
CARLA — repeatable controlled interventions
ReactSim-Bench — 2,636 nuPlan reactive-pressure scenarios + open benchmark code/data
CausalDrive — evidence that reactive neural world rendering is feasible in real time
InterPlan / Bench2Drive / nuPlan-family interactive scenarios — candidate planning evaluation sources
```

ReactSim-Bench lowers the behavior-simulation burden, but it does not itself provide unique matched counterfactual ground truth for every altered AV behavior. A simulator-controlled paired protocol is still needed.

## Key benchmark-artifact risk

One must not build a result that only reflects a particular scripted NPC controller. Required controls should vary the reactive-agent mechanism and interaction type.

## Researchability judgment

```text
VERY HIGH scientific value
MEDIUM-LOW current novelty overlap
VERY HIGH falsifiability
HIGH infrastructure burden
FAST-MOVING novelty window
```

Keep as candidate #1.

---

# CP-T6 assessment

## Why it matters

Response uncertainty clearly matters for interaction-heavy planning.

## Why it is rejected standalone

2026 Reaction-Uncertainty-Aware Motion Planning already directly compares multimodal conditional response modeling against a unimodal conditional baseline and reports large planning gains, especially in interactive scenes. Additional 2026 ego-conditioned prediction-planning work occupies the same mechanism family.

The remaining `structured representation only` matched control is a good ablation question but too narrow to support a standalone novelty story by itself.

## Retained value

Fold these variables into CP-T5/T2:

```text
response dependence
reaction multimodality / entropy
negotiation type
```

They become scenario strata and mechanistic probes rather than the main research claim.

---

# Candidate ranking

## Rank 1 — CP-T5

```text
Episode-specific reactive counterfactual consequences for planning
```

Why first:

```text
strongest unresolved evidence boundary
nearest prior art covers pieces but not conjunction
clean causal falsification possible
reactive benchmark/code already emerging
planning relevance direct
```

Main concern:

```text
simulator/data engineering + rapidly moving 2026 literature
```

## Rank 2 — CP-T2

```text
Conditional value of online consequence branching
```

Why second:

```text
fundamental WAM design question
strong anchor tension
very clean scientific payoff if matched well
```

Main concern:

```text
hard to ensure fair compute/data/candidate matching;
adaptive reasoning itself already prior art
```

## Rejected as standalone

```text
CP-T3 → merge into T2
CP-T6 → merge into T5/T2
```

---

# Promotion gate

Neither surviving candidate is yet a final `research gap`.

Before promotion, CP-T5 must pass:

```text
1. deep nearest-neighbor audit of 2026 counterfactual-WM paper
2. ReactSim-Bench protocol/source audit
3. CausalDrive reactive-truth audit
4. check for any 2026 paper already combining matched counterfactual truth + reactive agents + planning utility
5. concrete paired-intervention data protocol feasible with available simulator resources
```

CP-T2 must pass:

```text
1. nearest-neighbor audit of ProDrive / ForeSight / UTMR / CF-VLA
2. demonstrate that no paper already provides matched direct-vs-endpoint-vs-rollout ladder
3. define fair compute/candidate/value matching
4. identify reactive/interaction-stratified benchmark
```

Until then:

```text
NO final method design
NO novelty claim
NO risk-field insertion
```
