# WAM Research Tensions V1

Last updated: 2026-09-15

Status: **SCIENTIFIC TENSIONS — NOT RESEARCH GAPS, NOT METHOD PROPOSALS**

Source basis:

```text
11-anchor mechanism families
+ design-space consolidation
+ comparability QA
+ evidence-strength matrix
```

A tension is included only when:

```text
1. at least two anchors support materially different design interpretations;
2. the difference survives terminology/evaluation normalization;
3. current evidence cannot cleanly decide between the interpretations;
4. a falsifying experiment can be stated.
```

---

# T1 — Generic world fidelity vs decision-relevant future information

## Observation

Several papers show that world/future-related training improves planning:

```text
LAW
Epona
WorldDrive
World4Drive
WoTE
Metis
GraphWorld
```

But the anchor set does **not** establish a clean monotonic relation:

```text
better generic world fidelity
→ better planning
```

Controls:

```text
Epona      strong visual generation + planning gain, but no fidelity→planning ladder
Discrete-WAM strong FID/FVD + strong planning, but no matched causal relation
GraphWorld  no pixel/world fidelity objective needed for strong planning gains
WoTE        explicit decision-relevant consequence improves evaluator
```

## Competing interpretations

### H1

Better environmental prediction fidelity is intrinsically useful; current papers simply measure it poorly.

### H2

Only task-relevant future information matters; generic reconstruction/generation fidelity can be mostly orthogonal to planning.

## Evidence strength

```text
H2 support: MODERATE-STRONG
H1 support: plausible but weakly isolated
```

## Falsifying experiment

Hold planner, data, compute and representation size fixed. Train multiple WMs spanning a controlled fidelity range while separately measuring:

```text
generic future fidelity
planning-relevant state accuracy
planning score
```

If planning tracks generic fidelity after controlling task-relevant state quality, H2 weakens. If generic fidelity varies while planning remains tied to task-relevant state quality, H1 weakens.

---

# T2 — Explicit consequence rollout vs compact world-state conditioning

## Observation

Two strong online paradigms coexist:

```text
WoTE:
candidate → recurrent future → utility → select

GraphWorld:
interaction/history → compact W → direct policy
```

World4Drive/WorldDrive occupy intermediate positions.

## Competing interpretations

### H1

Explicit action-conditioned rollout is necessary for hard interactive decisions because the planner must compare future consequences.

### H2

A compact, decision-relevant world state can encode enough foresight to avoid expensive explicit rollouts in most cases.

## Evidence strength

```text
both paradigms have strong within-paper evidence
cross-paradigm causal comparison = absent
```

## Falsifying experiment

Use one backbone/data/evaluator and compare under matched latency/FLOPs:

```text
A. direct policy conditioned on compact W
B. endpoint future per candidate
C. recurrent rollout per candidate
```

Stratify by interaction difficulty. If B/C only help in high-interaction cases, the tension may resolve into a conditional design rule rather than a universal winner.

---

# T3 — Training-time world modeling vs deployment-time model-basedness

## Observation

Anchors demonstrate strong decoupling:

```text
Metis / Discrete-WAM
= strong world-policy joint training, action-only deployment

WoTE / World4Drive
= less parameter unification, strong online future dependence
```

Epona and DynFlowDrive provide additional intermediate controls.

## Competing interpretations

### H1

The main value of a world model is to shape policy parameters/representations during training; online world inference is often unnecessary.

### H2

Training-time compression loses precisely the conditional consequence information needed for rare/hard decisions; online models remain necessary.

## Evidence strength

```text
H1: STRONG existence proof
H2: plausible, supported by online-future gains but not matched against equally trained action-only policies
```

## Falsifying experiment

Train one world-aware system, then compare:

```text
full online WM
vs distilled/action-only policy
```

with identical training data and capacity budgets, stratified by distribution shift and interaction rarity.

---

# T4 — More world detail vs more decision relevance

## Observation

```text
Epona        rich visual future
WoTE         structured future consequence
GraphWorld   compact relational latent
World4Drive  compact endpoint latent
LAW          auxiliary latent
```

All can improve planning.

GraphWorld additionally shows that a highly structured, non-pixel world state can outperform richer representations on its tested planning tasks.

## Competing interpretations

### H1

Richer world state is safer because it preserves information that may become relevant later.

### H2

Excess world detail wastes capacity and introduces nuisance variation; aggressive decision-relevant abstraction is preferable.

## Evidence strength

```text
H2: MODERATE cross-anchor support
H1: theoretical plausibility + generative generality, weak matched planning evidence
```

## Falsifying experiment

Construct nested representations from the same encoder:

```text
rich scene latent
→ agent/object latent
→ interaction/risk/value latent
```

Match planner capacity and test both in-distribution and novel hazards. If compact representations fail only under novel relevance shifts, representation richness may act as robustness reserve.

---

# T5 — Factual-future learning vs intervention-correct consequence modeling

## Observation

Most anchors learn from one realized/logged future while making action-conditioned or multi-branch predictions:

```text
World4Drive
Metis
DynFlowDrive
Discrete-WAM
Epona
```

WoTE provides candidate-specific targets but the audited NAVSIM/PDM path still lacks reactive surrounding-agent truth.

## Competing interpretations

### H1

Large factual datasets plus action conditioning are sufficient to learn useful intervention consequences by generalization.

### H2

Without intervention-diverse/reactive supervision, candidate-specific future predictions may be plausible but systematically wrong exactly when ego action changes other agents' behavior.

## Evidence strength

```text
H2 boundary: STRONG — intervention validity is not established
which hypothesis is correct in practice: UNRESOLVED
```

## Falsifying experiment

Create matched scenes with controlled ego interventions and reactive agents in simulation or real-world repeated natural experiments. Evaluate:

```text
factual prediction accuracy
counterfactual response accuracy
planning utility
```

A model can then be tested for whether factual accuracy predicts intervention accuracy.

---

# T6 — Structured interaction semantics vs true reactive dynamics

## Observation

GraphWorld demonstrates strong planning/collision gains from explicit ego-agent structure without per-action reactive world prediction.

WoTE represents future consequences but lacks reactive surrounding-agent truth in the audited path.

SeerDrive provides internal world/planner interaction but not environmental response.

## Competing interpretations

### H1

Most practical safety gains come from better interaction representation; explicit game/reactive dynamics provide diminishing returns.

### H2

Interaction representations fail in negotiation-heavy scenarios unless they model how other agents respond to ego alternatives.

## Evidence strength

```text
H1: MODERATE-STRONG on current benchmarks
H2: insufficiently tested rather than contradicted
```

## Falsifying experiment

Partition evaluation by response dependence:

```text
low: other agents approximately independent of ego
high: merge/yield/negotiation where response changes with ego action
```

Compare structured-representation-only and reactive-consequence models under matched perception/planner capacity.

---

# T7 — Explicit value/utility vs learned mode/representation selection

## Observation

Decision semantics span:

```text
WoTE        explicit utility decomposition
WorldDrive  ranking/preference supervision
Drive-JEPA  simulator-distilled scorer
DynFlowDrive world-derived score head
World4Drive factual-mode consistency
GraphWorld  no explicit utility; direct conditioned policy
```

All can produce strong planning scores.

## Competing interpretations

### H1

Explicit interpretable value decomposition is necessary for reliable safety trade-offs and controllability.

### H2

Strong end-to-end representations and mode scores can internalize these trade-offs without an explicit utility layer.

## Evidence strength

```text
both viable; no matched architecture-level comparison
```

## Falsifying experiment

With the same future representation and candidates, compare:

```text
A. explicit decomposed utility heads
B. scalar learned ranker
C. direct conditioned policy
```

Probe calibration, controllability, distribution shift, and failure diagnosis—not only average planning score.

---

# T8 — Longer world rollout vs long-horizon planning competence

## Observation

GraphWorld is a decisive negative control:

```text
6s planning improvement
without 6s explicit world rollout
```

WoTE and Epona show useful recurrent/visual rollout capability.

## Competing interpretations

### H1

Long-horizon planning ultimately requires explicit long-horizon prediction to reason over delayed consequences.

### H2

Long-horizon competence can often emerge from history, latent memory, structured interaction and direct long-horizon policy conditioning without explicit long rollout.

## Evidence strength

```text
H2 existence proof: STRONG
H1 necessity claim: falsified in universal form, may remain conditional for delayed-causal tasks
```

## Falsifying experiment

Build scenarios with identical immediate observations but outcomes diverging only after delayed interactions. Compare performance while varying world rollout horizon independently from trajectory output horizon.

---

# T9 — More candidates/diversity vs better decisions

## Observation

Across anchors, more alternatives are not monotonically beneficial:

```text
WorldDrive Top-K peaks then drops
Drive-JEPA MTD diversity can rise while EPDMS/EC worsen
Discrete-WAM more decision support can increase optimization difficulty
```

## Competing interpretations

### H1

More diverse candidates increase oracle coverage and should improve planning if the scorer is strong enough.

### H2

Candidate expansion creates a harder selection/calibration problem; quality is determined by generator–scorer co-design, not diversity alone.

## Evidence strength

```text
H2: STRONG across multiple anchors
```

## Falsifying experiment

Measure separately as candidate count/diversity increases:

```text
oracle best-of-N
selected performance
ranking regret
calibration
```

If oracle improves while selected performance falls, selection rather than support is the bottleneck.

---

# T10 — More solver/refinement steps vs better planning

## Observation

Non-monotonic compute-quality behavior appears repeatedly:

```text
WorldDrive Top-K / selection depth
Metis flow steps saturate
GraphWorld >2 flow steps do not improve PDMS
Discrete-WAM edit rounds trade quality/compute
SeerDrive hidden refinement is not physical horizon
```

## Competing interpretations

### H1

Iterative refinement approximates a better solution and should improve with enough well-trained steps.

### H2

Internal iterations introduce distribution shift, over-refinement or optimization mismatch; step count is an architectural hyperparameter rather than a monotonic reasoning-depth axis.

## Evidence strength

```text
H2: STRONG empirical control
```

## Falsifying experiment

Train explicitly for variable-step inference and evaluate the same checkpoint across steps while measuring representation drift, calibration and physical planning quality.

---

# 11. Tension priority for adversarial problem discovery

Priority here means `scientifically discriminative`, not `recommended project idea`.

```text
Tier 1
T2 explicit rollout vs compact conditioning
T3 training-time world knowledge vs online model-basedness
T5 factual future vs intervention consequence validity
T6 structured interaction vs reactive dynamics

Tier 2
T1 generic fidelity vs decision relevance
T7 explicit utility vs implicit/direct decision
T8 rollout horizon vs long-horizon competence

Tier 3
T4 representation richness vs abstraction
T9 candidate diversity vs selection quality
T10 solver depth vs decision quality
```

Tier 1 tensions most directly distinguish competing WAM scientific paradigms and can potentially be falsified with controlled experiments.

---

# 12. Guardrail

This document does **not** claim:

```text
these tensions are novel research gaps;
no prior paper has studied them;
a specific method should be built;
risk fields are the answer.
```

Next phase should attack these tensions adversarially against broader literature and existing methods before any novelty or method decision.
