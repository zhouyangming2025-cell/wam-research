# NEXT_TASK

## 唯一下一任务

> **Deep-read SeerDrive under `WAM_DIMENSION_ONTOLOGY_V1` and use it as the first post-ontology stress test.**

## Current normalization status

```text
P0048 LAW          COMPLETE v2 + matrix projection
P0045 WoTE         COMPLETE v2 + matrix projection
P0001 Epona        COMPLETE v2 + matrix projection
P0042 WorldDrive   COMPLETE v2 + matrix projection
P0046 World4Drive  COMPLETE v2 + matrix projection

WAM_DIMENSION_ONTOLOGY_V1   COMPLETE
WAM_COMPARISON_MATRIX_V1    COMPLETE FIRST PROJECTION
```

Canonical comparison system:

```text
landscape/WAM_DIMENSION_ONTOLOGY_V1.md
landscape/WAM_COMPARISON_MATRIX_V1.md
```

## Why SeerDrive is next

SeerDrive appears to introduce bidirectional coupling between future-scene modeling and planning. It is therefore a strong stress test for dimensions that the first five anchors only partially exercised:

```text
J04 causal coupling direction
J07 task-mode inference graph
L02–L04 representation/parameter/gradient jointness
F04–F06 iterative future modeling and rollout
I01–I05 counterfactuality/reactivity
M01–M06 future-knowledge lifecycle
```

The main scientific question is:

> Is SeerDrive genuinely a new **online bidirectional world↔planning co-refinement interface**, or is it mainly an older iterative prediction-planning refinement pattern expressed in future-scene latent space?

## Mandatory workflow

Do not write a conventional SeerDrive summary first.

Use:

```text
paper/source facts
→ fill Ontology A–P
→ identify mechanism residue not expressible by V1
→ compare every important module to prior anchors and historical predecessors
→ only then write narrative synthesis
```

Every ontology dimension must receive a value or explicit:

```text
ABSENT
NOT REPORTED
NOT EVALUATED
NOT APPLICABLE
UNCLEAR / NEEDS SOURCE AUDIT
```

## SeerDrive audit targets

At minimum resolve:

```text
1. exact observation/history representation
2. current world state vs predicted future state
3. first trajectory/proposal generation
4. first future-scene prediction
5. exact world→trajectory refinement arrow
6. exact trajectory→world refinement arrow
7. number of iterations and weight sharing
8. whether planning/world branches share representation, parameters and gradients
9. future target and truth source
10. whether future supervision is factual, candidate-specific, teacher-generated or simulated
11. whether multiple candidates persist across iterations
12. scorer semantics if a scorer exists
13. whether predicted future directly changes deployed action
14. inference-time modules and compute
15. matched ablations for each coupling direction
16. iteration-count ablation
17. evaluation regime / reactivity
18. counterfactual output vs counterfactual supervision
19. relation to LAW / WoTE / Epona / WorldDrive / World4Drive
20. relation to PPAD / GameFormer / earlier iterative prediction-planning methods
```

## Required output

Create a dimension-first deep analysis and update the matrix:

```text
papers/deep_analysis/<SeerDrive>_DEEP_ANALYSIS_V2.md
landscape/WAM_COMPARISON_MATRIX_V1.md
```

If SeerDrive reveals a mechanism that cannot be represented by Ontology V1, do **not** force-fit it. Instead:

```text
fill existing dimensions first
→ document the residue
→ propose exact new/split dimension
→ back-project that dimension onto all five existing anchors
→ version ontology only after the back-projection succeeds
```

## Stop condition

Do not move to Drive-JEPA until we can state without ambiguity:

```text
what object is iterated
what arrows are genuinely bidirectional
what is supervised at each round
what remains online
what is world modeling vs generic iterative decoder refinement
what matched evidence isolates the claimed world↔planning coupling
```

## After SeerDrive

Unless new evidence changes priority:

```text
Drive-JEPA
Metis
DynFlowDrive
Discrete-WAM
GraphWorld
```

## Still forbidden

```text
no research-gap declaration
no method design
no broad VLA expansion
no forced risk-field insertion
no novelty conclusion from missing ontology cells
```
