# CURRENT_STATE

Last updated: **2026-09-15 — 11-anchor WAM consolidation COMPLETE; Phase D adversarial problem discovery UNPAUSED**

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
→ adversarial problem discovery
→ falsification
→ only then method design
```

Current phase:

```text
Phase C.5 core-anchor stress tests     COMPLETE
11-anchor Design Space Consolidation   COMPLETE
Comparability QA                       COMPLETE
Evidence-strength QA                   COMPLETE
Mechanism-family stabilization         COMPLETE
Phase D adversarial problem discovery  UNPAUSED
Final research-gap declaration         NOT YET AUTHORIZED
Method design                          NOT YET AUTHORIZED
```

---

# 1. Eleven normalized anchors

```text
P0048 LAW           COMPLETE v2
P0045 WoTE          COMPLETE v2
P0001 Epona         COMPLETE v2 + source audit
P0042 WorldDrive    COMPLETE v2 + source audit
P0046 World4Drive   COMPLETE v2 + core source audit
P0061 SeerDrive     COMPLETE v2 + version/source audit
P0049 Drive-JEPA    COMPLETE v2 + source audit
P0062 Metis         COMPLETE v2 + paper/repo audit
P0063 DynFlowDrive  COMPLETE v2 + paper/repo audit
P0064 Discrete-WAM  COMPLETE v2 + paper/source-status audit
P0065 GraphWorld    COMPLETE v2 + paper/source-status audit
```

Canonical coordinate system:

```text
landscape/WAM_DIMENSION_ONTOLOGY_V1.md
landscape/WAM_DIMENSION_ONTOLOGY_V1_1_AMENDMENT.md
landscape/WAM_DIMENSION_ONTOLOGY_V1_2_AMENDMENT.md
landscape/WAM_DIMENSION_ONTOLOGY_V1_3_AMENDMENT.md
```

Ontology decision after all 11 anchors:

```text
V1.3 RETAINED
NO V1.4
```

The ontology now absorbs new papers without paper-specific dimension inflation.

---

# 2. Consolidation artifacts

Canonical eleven-anchor synthesis:

```text
landscape/WAM_MECHANISM_FAMILIES_V2.md
landscape/WAM_DESIGN_SPACE_MAP_V2.md
audits/research_synthesis/WAM_11_ANCHOR_COMPARABILITY_QA.md
landscape/WAM_EVIDENCE_STRENGTH_MATRIX.md
landscape/WAM_RESEARCH_TENSIONS_V1.md
```

Latest per-paper comparison extension remains:

```text
landscape/WAM_COMPARISON_MATRIX_V1_3_GRAPHWORLD_EXTENSION.md
```

Source completeness authority:

```text
audits/research_synthesis/CORE_ANCHOR_SOURCE_COMPLETENESS_AUDIT.md
```

---

# 3. Stable mechanism-family map

```text
LAW
= future as predictive training signal

Drive-JEPA
= predictive representation pretraining / transfer

Epona
= shared world representation + direct generative policy

Metis
= asymmetric world-action co-training + action-only deployment

Discrete-WAM
= shared discrete world-policy backbone + policy-only primary planning

DynFlowDrive
= training-only candidate consequence teacher / score supervision

GraphWorld
= online structured world-state conditioning + direct multimodal planning

WorldDrive
= heavy future teacher → distilled lightweight online future evaluator

World4Drive
= online compact future latent + factual-mode selection

WoTE
= online recurrent consequence model + explicit utility

SeerDrive
= online world/planner hidden co-refinement
```

---

# 4. Core design-space conclusion

The field cannot be organized by a scalar notion of `world-model strength`.

At minimum, four orthogonal axes must remain separate:

```text
A. environmental/predictive modeling strength
B. decision-relevance of world representation
C. training-time jointness / gradient coupling
D. deployment-time dependence on online world computation
```

Canonical control:

```text
Discrete-WAM / Metis
= strong training jointness, low mandatory online future dependence

WoTE / World4Drive
= less parameter unification, high online future dependence
```

Therefore:

```text
training-time unification
!=
deployment-time model-basedness
```

---

# 5. Six distinct forms of `world helps planning`

Every future paper must answer independently:

```text
1. representation shaping?
2. parameter / gradient sharing?
3. online world-state conditioning?
4. online candidate consequence prediction?
5. explicit consequence utility/value?
6. search/selection over alternative actions?
```

The phrase `world model improves planning` is no longer accepted without this decomposition.

---

# 6. Future-truth / counterfactual boundary

Across the 11 anchors:

```text
candidate/action-specific predicted output       common
candidate-specific factual alternative truth    rare/absent
reactive surrounding-agent intervention truth   NOT ESTABLISHED
external intervention-validity proof             NOT ESTABLISHED
```

Binding rule:

```text
multiple predicted futures
!=
multiple counterfactual truths
```

This is currently an evidence boundary, not yet a final research-gap claim.

---

# 7. Temporal semantics stabilized

Never conflate:

```text
physical future time
history time
world rollout step
flow/diffusion transport coordinate
policy denoising/editing round
planner/world refinement iteration
```

F07/F08/J08 remain sufficient after GraphWorld.

Canonical negative controls:

```text
DynFlowDrive flow s          != physical time
GraphWorld flow coordinate   != physical time
Discrete-WAM edit round      != physical time
SeerDrive iteration          != physical time
Epona diffusion step         != future frame time
```

---

# 8. Long-horizon correction

Long-horizon must specify which object is long:

```text
trajectory output
history context
latent memory
world rollout
consequence rollout
reactive execution horizon
```

GraphWorld provides the key negative control:

```text
6s long-horizon planning
without
6s explicit world rollout
```

Therefore long-horizon planning competence does not universally require long-horizon world simulation.

---

# 9. Safety / risk / value correction

Keep separate:

```text
explicit risk state / field
explicit collision probability
explicit utility/value head
simulator/PDM reward supervision
implicit safety in representation
safety only measured at evaluation
```

GraphWorld is an important control:

```text
collision reduction
without
explicit risk representation or deployed utility head
```

Therefore later risk-aware hypotheses must prove value beyond better interaction modeling alone.

---

# 10. Evaluation regime normalization

Project labels:

```text
nuScenes and robustness subsets
= OPEN LOOP

NAVSIM v1/v2
= NON-REACTIVE DATA-DRIVEN / PSEUDO-SIMULATION PLANNING

Bench2Drive / CARLA
= REACTIVE SIMULATOR CLOSED LOOP

visual autoregressive generation
= GENERATIVE ROLLOUT, not policy-environment closed loop
```

Reactive final-policy performance does not automatically validate intervention-correct internal world dynamics.

---

# 11. Evidence-strength conclusion

High-confidence findings:

```text
1. future/world knowledge can help planning without online future generation;
2. online predicted future can improve candidate selection/ranking;
3. training jointness and online model-basedness are independent;
4. multiple future branches do not imply counterfactual truth;
5. internal solver/refinement depth is not physical horizon;
6. long-horizon planning does not require explicit long world rollout;
7. lower collision does not imply explicit risk-state learning.
```

Still unresolved at field level:

```text
generic world fidelity → planning causality
explicit rollout vs compact state under matched compute/data
training-only world knowledge vs online model-basedness on hard/OOD cases
factual-future learning vs intervention-correct consequence prediction
structured interaction representation vs true reactive dynamics
explicit utility/risk vs implicit/direct decision under matched architecture
```

---

# 12. Scientific tensions now authorized for adversarial validation

Canonical file:

```text
landscape/WAM_RESEARCH_TENSIONS_V1.md
```

Tier-1 tensions:

```text
T2 explicit consequence rollout vs compact world-state conditioning
T3 training-time world modeling vs deployment-time model-basedness
T5 factual-future learning vs intervention-correct consequence modeling
T6 structured interaction semantics vs true reactive dynamics
```

These are **not research gaps yet**.

Next phase must search broader literature/prior art and design falsification tests before novelty claims.

---

# 13. Source certainty

High source completeness:

```text
LAW
WoTE decision-critical path
Epona core mechanism
WorldDrive core mechanism
World4Drive core mechanism
Drive-JEPA first-pass paths
```

Partial/by-design:

```text
SeerDrive — public code is a later WoTE-integrated variant
World4Drive — NAVSIM branch equivalence remains partial
```

Source-blocked/monitor:

```text
Metis
DynFlowDrive
Discrete-WAM
GraphWorld
```

Do not replace absent official implementations with unofficial reimplementations as mechanism evidence.

---

# Immediate next task

See:

```text
state/NEXT_TASK.md
```

The next task is **adversarial validation of Tier-1 scientific tensions against broader literature and falsification logic**.

Still forbidden:

```text
NO final research-gap declaration
NO method architecture proposal
NO forced risk-field insertion
NO novelty claim from empty ontology cells
```
