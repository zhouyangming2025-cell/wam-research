# NEXT_TASK

## 唯一下一任务

> **Deep-read GraphWorld under the WAM reading skill stack + Ontology V1/V1.1/V1.2/V1.3, as the final planned Phase C.5 core-WAM stress test before WAM-only comparability QA.**

## Completed normalization / stress tests

```text
P0048 LAW           COMPLETE v2
P0045 WoTE          COMPLETE v2
P0001 Epona         COMPLETE v2
P0042 WorldDrive    COMPLETE v2
P0046 World4Drive   COMPLETE v2
P0061 SeerDrive     COMPLETE v2 first pass
P0049 Drive-JEPA    COMPLETE v2 first pass
P0062 Metis         COMPLETE v2 first pass
P0063 DynFlowDrive  COMPLETE v2 first pass
P0064 Discrete-WAM  COMPLETE v2 first pass
```

Canonical method stack:

```text
landscape/WAM_READING_SKILL_STACK.md
```

Canonical coordinate system:

```text
landscape/WAM_DIMENSION_ONTOLOGY_V1.md
landscape/WAM_DIMENSION_ONTOLOGY_V1_1_AMENDMENT.md
landscape/WAM_DIMENSION_ONTOLOGY_V1_2_AMENDMENT.md
landscape/WAM_DIMENSION_ONTOLOGY_V1_3_AMENDMENT.md
```

Latest comparison layer:

```text
landscape/WAM_COMPARISON_MATRIX_V1_3_DISCRETE_WAM_EXTENSION.md
```

Discrete-WAM artifacts:

```text
papers/deep_analysis/P0064_DISCRETE_WAM_DEEP_ANALYSIS_V2.md
audits/literature/PHASE_C5_DISCRETE_WAM_AUDIT.md
landscape/P0064_DISCRETE_WAM_ONTOLOGY_PROJECTION.md
```

---

# Why GraphWorld is next

GraphWorld (`arXiv:2606.16274v1`) claims to improve **long-horizon planning** through:

```text
Ego-Centric Interaction Graph
+
latent world state
+
World-State-Conditioned Planning
```

The paper's abstract further says the latent world state captures interaction dynamics and safety-relevant semantics.

These claims directly pressure-test dimensions that the prior anchors only partially cover:

```text
explicit multi-agent interaction representation
world-state semantics vs generic scene latent
long-horizon planning vs merely longer trajectory output
safety-relevant representation vs explicit risk/value modeling
reactive-agent truth vs relational feature modeling
world-state persistence / transition dynamics
```

The central question is:

> **Does GraphWorld actually learn a predictive/dynamic world state that changes long-horizon decisions, or does it mainly build a stronger interaction-aware current-scene representation and call that a world model?**

---

# Mandatory audit targets

Resolve at minimum:

```text
1. exact sensor/history inputs on nuScenes / NAVSIM / Bench2Drive
2. ego/agent node construction and graph update rules
3. how neighbors are selected / pruned / ranked
4. node and edge semantics
5. whether graph state is current-only, predictive, recurrent, or explicitly transitioned in time
6. exact object called `world state`
7. whether world state has a factual future target
8. whether there is a transition/dynamics operator
9. F07 prediction observability geometry
10. F08 internal-step / physical-time semantics
11. what `long horizon` means numerically and mechanistically
12. whether longer trajectory horizon is the only long-horizon change
13. whether the world state is predicted into the future or only conditions a longer planner
14. planner→world and world→planner forward interfaces
15. interaction graph→planning-query information path
16. whether other-agent reactions are predicted or only encoded
17. candidate/action representation and multimodality
18. action-conditioned world prediction, if any
19. counterfactual vector I01–I05
20. risk/safety semantics: explicit state, value, loss, or only interpretation
21. world-state supervision truth source
22. policy/value supervision truth source
23. training topology / shared parameters / gradient coupling
24. what world machinery remains at inference
25. matched ablations isolating interaction graph, world state, horizon and planner changes
26. strongest collision/safety matched control
27. short-horizon vs long-horizon ablation
28. prediction/world-state quality → planning evidence
29. source/version/code status
30. evaluation-regime correction across nuScenes/NAVSIM/Bench2Drive
```

---

# Required semantic attack 1 — `world state`

Do not accept:

```text
interaction-aware latent
→ world model
```

Trace:

```text
current observations
→ graph / latent state
→ transition or update operator
→ future/world target, if any
→ planner use
```

Then classify:

```text
CURRENT SCENE REPRESENTATION
PREDICTIVE FUTURE STATE
RECURRENT DYNAMICAL STATE
INTERACTION MEMORY
VALUE / SAFETY STATE
HYBRID
```

A strong current interaction encoder is scientifically different from a learned future world transition.

---

# Required semantic attack 2 — `long horizon`

Separate:

```text
longer output trajectory horizon
longer observation/history context
multi-step predicted world horizon
persistent latent memory
multi-stage planner refinement
reactive closed-loop horizon
```

Do not infer long-horizon reasoning merely from a longer waypoint vector.

Use:

```text
F04/F05/F07/F08
J08
P06
```

to record what actually becomes long.

---

# Required semantic attack 3 — interaction and safety

GraphWorld explicitly claims interaction dynamics and safety-relevant semantics.

Force separate answers:

```text
explicit graph relation?                   yes/no
other-agent future prediction?             yes/no
other-agent response to ego alternatives?  yes/no
reactive-agent ground truth?                yes/no
explicit risk variable?                    yes/no
explicit collision/value objective?        yes/no
safety improvement measured?               yes/no
```

Binding control:

```text
interaction-aware representation
!= reactive interaction dynamics

collision reduction
!= explicit learned risk representation
```

---

# Required cross-paper comparisons

Especially compare:

```text
GraphWorld vs SeerDrive
= interaction/world state vs future-BEV/planner co-refinement

GraphWorld vs WoTE
= graph relational state vs explicit recurrent future consequence + utility

GraphWorld vs World4Drive
= safety/interaction latent vs candidate-conditioned endpoint future

GraphWorld vs LAW
= current/interaction representation shaping vs explicit factual future-latent auxiliary prediction

GraphWorld vs Epona
= graph state + planner conditioning vs shared generative world latent

GraphWorld vs CausalDrive / GameFormer / M2I controls
= explicit interaction modeling without automatically granting WAM status
```

The objective is to distinguish **world-model-specific mechanism** from strong graph-based interaction modeling inherited from prediction/planning literature.

---

# Required workflow

```text
official paper / PDF / HTML / official repo if available
→ source/version gate
→ mechanism + formula + graph-flow reconstruction
→ claim/evidence extraction
→ fill all Ontology V1 + V1.1 + V1.2 + V1.3 dimensions
→ immediate horizontal comparison
→ residue test
→ back-project any proposed new dimension before ontology extension
```

## Required output

```text
papers/deep_analysis/P0065_GRAPHWORLD_DEEP_ANALYSIS_V2.md
audits/literature/PHASE_C5_GRAPHWORLD_AUDIT.md
landscape/P0065_GRAPHWORLD_ONTOLOGY_PROJECTION.md
comparison matrix extension/update
```

Add a new ontology dimension only if existing axes cannot express a scientifically important distinction and the residue survives cross-paper back-projection.

---

# Stop condition

Do not close Phase C.5 until we can state without ambiguity:

```text
what GraphWorld calls a world state;
whether that state is predictive/dynamical or current interaction representation;
what exact mechanism makes planning long-horizon;
how graph relations enter planning;
whether other agents are predicted/reactive;
where safety semantics actually live;
which ablation isolates graph/world/horizon contributions;
what survives into deployment;
what is proven vs author framing.
```

## After GraphWorld

```text
WAM-only comparability QA
→ consolidate the ten/eleven-anchor design-space map
→ only then decide whether Phase D problem discovery may reopen
```

## Still forbidden

```text
no research-gap declaration
no method design
no broad VLA expansion
no forced risk-field insertion
no novelty conclusion from empty ontology cells
```
