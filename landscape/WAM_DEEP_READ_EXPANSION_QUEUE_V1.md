# WAM Deep-Read Expansion Queue V1

Last updated: 2026-09-15

Status: **ACTIVE — LITERATURE EXPANSION BEFORE RESEARCH-DIRECTION CONVERGENCE**

## Binding rule

```text
11 deep anchors
= preliminary coordinate system
!= mature field understanding
!= authorization to promote research direction
```

Paper selection remains coverage-driven, not hypothesis-driven.

Current normalized count:

```text
15 papers
```

Latest completed expansion anchors:

```text
P0009 DriveLaW  — COMPLETE
P0012 DA-WAM    — COMPLETE
P0002 SafeDrive — COMPLETE
P0005 RiskWorld — COMPLETE
```

---

# Working gate before another research-direction discussion

```text
~24–30 deeply normalized papers total
+
multiple independent anchors across major mechanism families
+
new papers mostly map into the coordinate system without repeatedly exposing major blind spots
```

Required diversity:

```text
planning-centric online WAM interfaces
world→policy latent interfaces
candidate-specific future/scoring
explicit safety/risk/value reasoning
reactive behavior simulation / world simulation
evaluation-regime controls
WAM+VLA boundary methods
alternative world representations
training-only vs deployment-time world knowledge
```

---

# Wave C.6 — Core planning-centric WAM expansion

## P0009 DriveLaW — COMPLETE

```text
history → early Video-DiT hidden states → Action-DiT → direct trajectory
```

## P0012 DA-WAM — COMPLETE

```text
32 ego candidates → candidate-specific 0.5s future latents → explicit factor/utility scorer → argmax
```

Direct future truth exists only for the expert-matched branch; all branches receive value/ranking supervision.

## P0002 SafeDrive — COMPLETE

```text
ego candidate → sparse ego-agent world → fine-grained agent×time safety → trajectory selection
```

Candidate-specific safety consequence labels exist; candidate-specific reactive agent futures do not.

## P0005 RiskWorld — COMPLETE

Canonical subtype:

```text
OBJECT-CENTRIC FACTUAL-RELATION ROLLOUT RISK WORLD MODEL
```

Mechanism:

```text
observed history
→ object-centric relation-aware current state
→ RSSM-style 60-step / 3s physical future rollout
→ future relative position / distance / temporal-risk sequence
→ object risk source
```

Critical boundaries:

```text
explicit predicted risk state           YES
future physical rollout                 YES
ego action-candidate conditioning        NO
online planning consumption             NO
reactive intervention truth             NO
```

RiskWorld is therefore a boundary/control anchor: it demonstrates risk-as-prediction inside a world-model pipeline without demonstrating world-model-based planning.

Strongest future-model controls:

```text
w/o future rollout      60.2 F1
w/o future supervision  61.6
Deterministic GRU       62.0
RiskWorld               63.0
```

Representation prior effects are larger and must be attributed separately.

## P0007 DriveReward — NEXT

Value/reward control anchor:

```text
visual/current context + trajectory
→ learned semantic reward/value
→ RL / candidate ranking / test-time selection
```

Scientific purpose:

```text
separate consequence/world prediction
from
value/reward modeling
```

Mandatory comparisons:

```text
DriveReward vs WoTE
DriveReward vs DA-WAM
DriveReward vs SafeDrive
DriveReward vs RiskWorld
DriveReward vs Drive-JEPA / WorldDrive
```

---

# Wave C.7 — Simulation / reactivity / evaluation controls

```text
P0003 Safe-Sim
P0004 PROSIM
P0013 BridgeSim
P0014 ReactSimBench
P0015 CausalDrive
```

Purpose:

```text
reactive environment modeling
behavior simulation
log-replay vs endogenous reaction
generative simulator vs planning WAM
open-loop vs non-reactive pseudo-sim vs reactive closed loop
simulation/evaluation truth
```

---

# Wave C.8 — WAM+VLA / reasoning boundary controls

```text
P0008 AutoVLA
P0011 ReCogDrive
P0010 LINGO-2
P0006 DriveGPT4
```

Purpose:

```text
separate world-model benefit from language/reasoning prior
separate generative planning from VLM/VLA semantic reasoning
understand reward/post-training/reasoning interfaces
avoid calling every future-aware VLA a world model
```

---

# Reading protocol

```text
paper-deep-reader reconstruction
→ source/version gate
→ architecture/training/inference graph
→ strongest matched ablations
→ immediate cross-paper comparison
→ force-fill Ontology V1.3
→ residue/back-projection test
```

Every paper must answer:

```text
what exactly the module does
what prior anchors do the same scientific job
whether supervision/deployment role is truly comparable
strongest matched evidence
what the paper does NOT prove
```

---

# Parked work

All research-tension / candidate-problem artifacts remain historical/provisional until the expanded corpus is reconsolidated.

---

# Next paper

```text
P0007 DriveReward
```
