# WAM Comparison Matrix V1.3 — RiskWorld Extension

Last updated: 2026-09-15

Status: **15-ANCHOR EXTENSION — RISKWORLD NORMALIZED**

This file adds P0005 RiskWorld to the active comparison set without changing Ontology V1.3.

Canonical analysis:

```text
papers/deep_analysis/P0005_RISKWORLD_DEEP_ANALYSIS_V2.md
audits/literature/PHASE_C6_RISKWORLD_AUDIT.md
landscape/P0005_RISKWORLD_ONTOLOGY_PROJECTION.md
```

---

# 1. RiskWorld row

| Dimension | RiskWorld |
|---|---|
| Primary role | object-level risk-source identification / anticipation |
| World object | one relation-aware latent state per observed object |
| Current representation | frozen V-JEPA2 global/object visual features + structured ego/object histories + relation attention |
| Future dynamics | object-wise RSSM-style recurrent deterministic/stochastic latent rollout |
| Physical horizon | 60 future steps = 3 s at 20 FPS |
| Future decoded state | ego-relative position, distance, temporal-risk probability |
| Final output | object-risk probability / risky-object selection |
| Ego action candidate input | **NO** |
| Action→world coupling | **ABSENT for hypothetical future action** |
| Online world rollout | **YES** |
| Online world consumed by planner | **NO** |
| Explicit risk semantics | **YES — object risk + time-indexed risk curve** |
| Explicit utility/value semantics | **NO** |
| Factual future supervision | logged future ego/object tracks |
| Risk supervision | RiskBench risk-object annotation + event-timing-derived curve |
| Alternative-action future truth | **NO** |
| Reactive other-agent intervention truth | **NO** |
| Planning evidence | filtered-observation LBC diagnostic only; no integrated planning improvement |
| Foundation prior | frozen V-JEPA2 ViT-L |
| Source status | paper verified; official implementation not identified |

Canonical subtype:

```text
OBJECT-CENTRIC FACTUAL-RELATION ROLLOUT RISK WORLD MODEL
```

---

# 2. Safety / risk / utility comparison

| Method | What is explicitly predicted? | Is it ego-action conditioned? | Does it directly choose an ego trajectory? |
|---|---|---:|---:|
| RiskWorld | object risk + time-indexed risk + future relative geometry | **NO** | **NO** |
| SafeDrive | scene safety + pairwise collision + time-wise DAC + PDM-like factors | **YES, per ego candidate** | **YES** |
| DA-WAM | NC/DAC/EP/TTC/Comfort + learned utility over candidate future latent | **YES** | **YES** |
| WoTE | learned future consequence sequence + explicit utility/value | **YES** | **YES** |
| World4Drive | factual-future/mode consistency score | **YES** | **YES**, but score is not explicit safety utility |
| GraphWorld | structured future-aware interaction latent | not candidate-consequence branching | direct planner conditioning |

Binding interpretation:

```text
explicit risk prediction
!=
trajectory value modeling
!=
candidate-specific consequence modeling
```

RiskWorld is the cleanest current anchor for the first category.

---

# 3. RiskWorld vs SafeDrive

## Shared feature

Both make safety/risk semantics explicit rather than judging success only through downstream benchmark collision metrics.

## Structural difference

```text
RiskWorld
history
→ factual-distribution object future
→ risk object

SafeDrive
ego plan candidate
→ sparse candidate world
→ safety consequence
→ score / select
```

Thus:

```text
RiskWorld = predictive risk monitor
SafeDrive = candidate-conditioned safety evaluator/planner
```

## Supervision difference

RiskWorld:

```text
future geometry = logged future ego/object tracks
risk = object/event annotations
```

SafeDrive:

```text
future agent motion = logged future
candidate safety = simulator/PDM labels per ego proposal
```

This exposes a three-way separation:

```text
factual world truth
candidate-specific safety consequence truth
reactive alternative-world truth
```

They are not interchangeable.

---

# 4. RiskWorld vs DA-WAM

The word `candidate` must not be used without type annotation.

```text
RiskWorld candidate = observed environment object
DA-WAM candidate    = hypothetical ego trajectory
```

RiskWorld branches by **who may be risky**.
DA-WAM branches by **what ego may do**.

Both produce future latent features, but the decision semantics are orthogonal:

```text
RiskWorld: future relation → classify object
DA-WAM: action future → evaluate trajectory
```

---

# 5. RiskWorld vs WoTE

Shared:

```text
explicit recurrent/multi-step future reasoning
```

Different:

```text
WoTE:
action_i → future_i → utility_i → argmax action

RiskWorld:
object_i → future relation_i → risk_i → identify object
```

This is direct evidence that:

```text
multi-step world rollout
!=
model-based planning by itself
```

The planner interface is an independent dimension.

---

# 6. RiskWorld vs GraphWorld

A useful inversion:

```text
GraphWorld:
weak/no explicit physical multi-step rollout
strong online world→planning coupling

RiskWorld:
strong explicit 60-step physical rollout
no online world→planning coupling
```

Therefore:

```text
rollout depth ⟂ planning dependence
```

This relationship should remain explicit in future taxonomy work.

---

# 7. World-model contribution attribution

RiskWorld's ablation table should be read in two blocks.

## Representation block

```text
w/o world features        50.6 F1
w/o object visual token   54.6
w/o relation attention    54.3
full                      63.0
```

These are large effects but bundle imported V-JEPA context and relational representation.

## Future-model block

```text
w/o future rollout      60.2
w/o future supervision  61.6
Deterministic GRU       62.0
full                    63.0
```

The strongest matched incremental rollout evidence is therefore closer to:

```text
60.2 → 63.0
```

rather than:

```text
50.6 → 63.0
```

when asking specifically about recurrent latent future modeling.

---

# 8. Counterfactual vector

RiskWorld must be entered carefully because branches correspond to objects, not actions.

| Question | RiskWorld |
|---|---|
| object-specific future output? | YES |
| ego-action-specific future output? | NO |
| alternative-action factual future supervision? | NO |
| reactive other-agent intervention truth? | NO |
| intervention-response validation? | NO |

Do not interpret its 64 object candidates as 64 counterfactual world branches.

---

# 9. Evaluation comparability

RiskWorld headline `63.0 F1` is not comparable numerically with NAVSIM PDMS/EPDMS or Bench2Drive driving score.

Evaluation regime:

```text
RiskBench CARLA scenario corpus
→ frame-wise object risk identification
```

Planning-aware evaluation:

```text
RiskWorld selects/masks observations
→ fixed LBC planner diagnostic
```

It establishes planning relevance of selected evidence, not planning-policy improvement.

---

# 10. Scientific role in the growing atlas

RiskWorld fills an important under-covered mechanism family:

```text
explicit risk as a learned prediction from latent world dynamics
```

Previous anchors mostly used safety as:

```text
benchmark outcome
external teacher/value
candidate evaluator
```

RiskWorld shows a different design:

```text
future world relation
→ risk representation itself
```

But because risk is not fed back into an online planner, it remains a **boundary anchor**, not evidence that this representation improves end-to-end planning.

---

# Ontology decision

```text
V1.3 RETAINED
NO V1.4
```

RiskWorld strongly exercises existing axes rather than exposing a new irreducible one:

```text
P01 explicit risk state
P02 risk monitor vs safety/value evaluator
F04/F05 recurrent physical future
G03 factual future provenance
I01–I05 counterfactuality/reactivity
J02/J03 world computation vs planner consumption
O01/O07 evaluation semantics
```
