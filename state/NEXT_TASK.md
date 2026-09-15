# NEXT_TASK

## 唯一下一任务

> **Merge/split the dimensions discovered from LAW + WoTE + Epona + WorldDrive + World4Drive and build the first stable WAM comparison ontology + matrix.**

## Current status

```text
P0048 LAW          COMPLETE v2
P0045 WoTE         COMPLETE v2
P0001 Epona        COMPLETE v2
P0042 WorldDrive   COMPLETE v2
P0046 World4Drive  COMPLETE v2
```

Canonical deep analyses:

```text
papers/deep_analysis/P0048_LAW_DEEP_ANALYSIS_V2.md
papers/deep_analysis/P0045_WOTE_DEEP_ANALYSIS_V2.md
papers/deep_analysis/P0001_EPONA_DEEP_ANALYSIS_V2.md
papers/deep_analysis/P0042_WORLDDRIVE_DEEP_ANALYSIS_V2.md
papers/deep_analysis/P0046_WORLD4DRIVE_DEEP_ANALYSIS_V2.md
```

Dimension-discovery sources:

```text
landscape/WAM_DIMENSION_DISCOVERY_LOG.md
landscape/WAM_DIMENSION_DISCOVERY_ADDENDUM_EPONA_WORLDDRIVE.md
landscape/WAM_DIMENSION_DISCOVERY_ADDENDUM_WORLD4DRIVE.md
```

## Why synthesis is mandatory now

The five anchors expose fundamentally different ways future/world knowledge enters planning:

```text
LAW
= future prediction as auxiliary representation shaping

WoTE
= online candidate consequence rollout → explicit utility/reward → selection

Epona
= shared world representation + direct generative trajectory policy;
  visual future is a sibling branch, not required by planning inference

WorldDrive
= generative-WM representation inheritance
  + heavy future teacher → distilled lightweight future surrogate → online ranking

World4Drive
= direct online compact candidate future latent
  → factual-future/mode ScoreNet → selection
```

Continuing to add papers before consolidating these discoveries would reproduce the original repository problem: many paper notes but no stable comparison coordinates.

## Required outputs

Create:

```text
landscape/WAM_DIMENSION_ONTOLOGY_V1.md
landscape/WAM_COMPARISON_MATRIX_V1.md
```

### Output 1 — WAM_DIMENSION_ONTOLOGY_V1.md

Do not simply concatenate the >60 provisional discovery dimensions. Perform an explicit merge/split pass.

Each stable dimension must contain:

```text
Dimension name
Scientific question
Why it matters
Allowed / typical values
How to distinguish similar values
Evidence required
Common misclassification traps
Anchor examples
```

Recommended high-level families to pressure-test, not blindly accept:

```text
A. problem / role of world knowledge
B. observation and current-state representation
C. representation provenance / foundation priors
D. action and candidate space
E. action→world conditioning
F. dynamics / future temporal modeling
G. future supervision / truth sources
H. multimodal branch assignment
I. counterfactuality / reactivity
J. world→planning interface
K. scorer / utility semantics
L. training topology / gradient coupling
M. future-knowledge lifecycle / deployment path
N. compute / pruning / latency
O. evaluation regime / evidence attribution
P. safety / uncertainty / risk semantics
```

Do not force every family to survive if dimensions can be merged more cleanly.

### Output 2 — WAM_COMPARISON_MATRIX_V1.md

Project all five anchors into the same ontology.

Rules:

```text
1. Every stable dimension must be filled for every anchor.
2. Use ABSENT / NOT REPORTED / NOT EVALUATED / NOT APPLICABLE explicitly.
3. A paper cannot stay inside its own preferred narrative.
4. Separate AUTHOR CLAIM / DIRECT EVIDENCE / OUR INFERENCE where interpretation is disputed.
5. Counterfactuality must at least separate:
   - candidate-specific output
   - alternative-action supervision
   - reactive other-agent response evidence
6. Scorer semantics must distinguish utility/value from factual-consistency/mode matching.
7. Representation gains must separate imported foundation priors from WM-specific future-model learning.
8. Planning gains must use strongest matched controls, not headline SOTA deltas.
```

## Mandatory merge/split tests

Before freezing ontology v1, explicitly test these discoveries:

```text
1. `action-conditioned` is too coarse:
   provenance / representation / multiplicity / injection / support need separation.

2. `joint world-action modeling` is too coarse:
   shared representation / parameters / gradients / online causal feedback need separation.

3. `counterfactual` is too coarse:
   output branching / supervision branching / behavioral reactivity need separation.

4. `future→score` is too coarse:
   utility / risk / imitation / factual consistency / mode posterior need separation.

5. `world-model gain` is too coarse:
   foundation prior / predictive representation / candidate generator / evaluator / future state contribution need attribution.

6. `online vs offline WM` is too coarse:
   future-knowledge lifecycle must represent discard, sibling branch, direct online transition, and teacher→student distillation.

7. `future representation` is too coarse:
   endpoint / sequence / recurrent rollout / distilled summary and current-vs-future state must be separated.
```

## Stop condition

Do not resume new-paper reading until we can take an arbitrary new WAM paper and systematically answer, under one shared coordinate system:

```text
what world/current state it represents
where that representation came from
what actions/candidates it considers
how actions condition future prediction
what future object it predicts
how that future is supervised
whether alternatives have real/simulated/reactive truth
how world information changes the final action
what the scorer actually means
where future knowledge lives at deployment
what computation is paid online
what experiment truly isolates the claimed mechanism
```

## After ontology + matrix

Resume core-WAM coverage correction in this order unless new evidence changes priority:

```text
SeerDrive
Drive-JEPA
Metis
DynFlowDrive
Discrete-WAM
GraphWorld
```

Every new anchor must be projected into ontology v1 and is allowed to add/split dimensions if genuinely necessary.

## Still forbidden

```text
no research-gap declaration
no method design
no forced risk-field insertion
no novelty conclusion from missing cells
```
