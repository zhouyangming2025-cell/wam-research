# CURRENT_STATE

Last updated: **2026-09-15 — candidate-problem novelty attack COMPLETE; CP-T5 PRIMARY, CP-T2 SECONDARY**

## Research north star

```text
WAM / World Model + one-stage End-to-End + Planning-centric autonomous driving
```

Core WAM remains primary. WAM+VLA is secondary/control. Risk/predictive-risk remains optional prior knowledge, not a required destination.

## Methodology in force

```text
FIELD UNDERSTANDING FIRST
→ core-WAM coverage
→ comparative anchor deep reads
→ dimension-first normalization
→ comparability/evidence QA
→ adversarial prior-art attack
→ falsifiable candidate-problem formulation
→ nearest-neighbor novelty attack
→ candidate-specific falsification / feasibility audit
→ only then research-gap promotion
→ only then method design
```

Current phase:

```text
Phase C.5 core-anchor stress tests          COMPLETE
11-anchor Design Space Consolidation        COMPLETE
Comparability / evidence QA                 COMPLETE
Tier-1 broader-literature adversarial QA    COMPLETE
Candidate problem formulation               COMPLETE
2025–2026 nearest-neighbor overlap attack   COMPLETE FIRST PASS
Researchability ranking                     COMPLETE FIRST PASS
Final research-gap declaration              NOT YET AUTHORIZED
Method design                               NOT YET AUTHORIZED
```

---

# Canonical synthesis artifacts

```text
landscape/WAM_MECHANISM_FAMILIES_V2.md
landscape/WAM_DESIGN_SPACE_MAP_V2.md
audits/research_synthesis/WAM_11_ANCHOR_COMPARABILITY_QA.md
landscape/WAM_EVIDENCE_STRENGTH_MATRIX.md
landscape/WAM_RESEARCH_TENSIONS_V2_VALIDATED.md
audits/research_synthesis/WAM_TIER1_TENSION_ADVERSARIAL_VALIDATION_V1.md
```

Candidate-problem layer:

```text
landscape/WAM_CANDIDATE_PROBLEMS_V1.md
landscape/WAM_CANDIDATE_PROBLEM_OVERLAP_MATRIX_V1.md
landscape/WAM_CANDIDATE_PROBLEM_RESEARCHABILITY_V1.md
```

Ontology remains:

```text
WAM Ontology V1.3 — RETAINED
```

---

# Candidate problem decisions after nearest-neighbor attack

## CP-T2 — Conditional value of online consequence branching

```text
VERDICT: SURVIVES — CANDIDATE RESEARCH PROBLEM
PRIORITY: #2
NOVELTY RISK: MEDIUM
```

Minimal scientific question:

> **When does online action-conditioned consequence branching add decision information that cannot be amortized into a compact world state/direct policy under matched training information and deployment budget?**

Required contrast:

```text
A compact W → direct policy
B candidate → endpoint future → selection
C candidate → recurrent consequence rollout → selection
```

Required stratification:

```text
interaction-response dependence
candidate ambiguity
OOD / rarity
```

2026 novelty pressure:

```text
ProDrive / ForeSight         explicit future-centric planning
CF-VLA                      adaptive hard-scene reasoning
UTMR                        uncertainty-triggered extra WM reranking
```

Therefore the novelty cannot be `use rollouts on hard scenes` or `trigger more reasoning under uncertainty`. The surviving contribution would have to be a matched causal decomposition of **when branching itself is information-bearing**.

---

## CP-T3 — Non-amortizable world reasoning after distillation

```text
VERDICT: REJECT — PRIOR ART as standalone direction
```

Primary collision:

```text
WPT (CVPR 2026)
= online WM teacher → policy/world-reward distillation → fast student

Fast-WAM (2026, robotics)
= world/video co-training → test-time future imagination can be skipped

CF-VLA
= selective hard-scene reasoning

UTMR
= uncertainty-triggered extra world-model computation
```

Residual variable retained:

```text
what consequence information is / is not amortizable?
```

This is folded into CP-T2 rather than pursued independently.

---

## CP-T5 — Episode-specific reactive counterfactual consequences for planning

```text
VERDICT: SURVIVES — CANDIDATE RESEARCH PROBLEM
PRIORITY: #1
NOVELTY RISK: MEDIUM-LOW BUT FAST-MOVING
```

Minimal scientific question:

> **Can a planning-centric WAM trained mainly on factual trajectories recover intervention-correct consequences when an alternative ego action changes both the episode-specific outcome and surrounding-agent responses?**

Core hypothesis:

```text
history + alternative action
is insufficient in the hard case because both:

1. episode-specific latent causes must be preserved / inferred;
2. surrounding-agent response is endogenous to the ego intervention.
```

Required paired protocol:

```text
same underlying simulated world / seed
factual ego action a
alternative ego action a'
reactive environment mechanism held fixed
→ matched Y(a), Y(a')
```

Required outcomes:

```text
factual future accuracy
matched counterfactual accuracy
agent reaction accuracy
counterfactual interaction/collision outcome accuracy
planning regret / ranking consistency
```

### Why this survives the strongest 2026 nearest neighbors

`How Can Driving World Models Do Counterfactual Prediction?`:

```text
matched episode-specific counterfactual truth: YES
surrounding-agent response to changed ego action: deliberately NO
planning-centric reactive consequence test: NO
```

`ReactSim-Bench`:

```text
AV deviation → agent reactive response protocol: YES
2,636 nuPlan scenarios + open benchmark code/data: YES
matched same-episode factual/counterfactual truth: NO
planning-regret / WAM consequence validity: NO
```

`CausalDrive`:

```text
real-time reactive visual world renderer: YES
counterfactual reaction control / driving sociology: YES
matched episode-specific factual↔reactive-CF identification: NOT ESTABLISHED
```

`AWM / reactive-adversarial work`:

```text
hard interactive counterfactual pressure: YES
same scientific target as consequence-validity benchmark: NO
```

The unresolved conjunction is therefore:

```text
EPISODE-SPECIFIC COUNTERFACTUAL IDENTIFICATION
+
REACTIVE EGO→AGENT INTERVENTION RESPONSE
+
PLANNING UTILITY / REGRET
```

Important:

```text
This is NOT a claim that reactive world models are novel.
This is NOT a claim that counterfactual world models are novel.
```

---

## CP-T6 — Reaction distributions beyond structured interaction representation

```text
VERDICT: REJECT — PRIOR ART as standalone direction
```

Key collision:

```text
Reaction-Uncertainty-Aware Motion Planning (2026)
= ego-conditioned multimodal reaction prediction + tree planning
= directly shows planning gain over unimodal conditional response baseline
```

Additional prior art:

```text
M2I
GameFormer
2026 ego-conditioned prediction + planning
ProDrive
ReactSim-Bench
```

The exact GraphWorld-like structured-only negative control remains scientifically useful, but is too thin a standalone novelty boundary.

Retained variables:

```text
response dependence
reaction multimodality / entropy
negotiation type
```

These become stratification axes inside CP-T5 / CP-T2.

---

# Current candidate ranking

```text
#1 CP-T5
Episode-specific reactive counterfactual consequence validity for planning

#2 CP-T2
Conditional marginal value of online consequence branching
```

Rejected standalone:

```text
CP-T3 → merge into T2
CP-T6 → merge into T5/T2
```

---

# Why CP-T5 is currently first

Scientific value:

```text
very high
```

Falsifiability:

```text
very high — controlled repeated interventions can generate paired truth
```

Nearest-neighbor overlap:

```text
moderate: the pieces exist separately, the full conjunction has not been identified
```

Infrastructure burden:

```text
high
```

Promising available pieces:

```text
CARLA repeatable intervention
ReactSim-Bench reactive protocol + open code/data
CausalDrive evidence for real-time reactive neural simulation
Bench2Drive / InterPlan / nuPlan-family interactive scenarios
```

Main risk:

```text
fast-moving 2026 literature may close the novelty window quickly
```

---

# Counterfactual vocabulary remains mandatory

Always separate:

```text
conditional prediction
interventional prediction
episode-specific counterfactual prediction
reactive counterfactual simulation
```

And separately report:

```text
candidate-specific output?
candidate-specific paired truth?
reactive other-agent truth?
external intervention validation?
planning utility validation?
```

---

# Immediate next task

See `state/NEXT_TASK.md`.

Next phase focuses on **CP-T5 promotion attack**, not method design:

```text
deep-audit nearest neighbors
→ verify exact novelty boundary
→ verify paired-intervention infrastructure feasibility
→ decide PROMOTE / REJECT / HOLD
```

CP-T2 remains the secondary candidate and fallback.

Still forbidden:

```text
NO final architecture proposal
NO paper-title brainstorming
NO forced risk-field insertion
NO novelty claim until CP-T5 promotion gate passes
```
