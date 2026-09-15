# NEXT_TASK

## 唯一下一任务

> **Perform WAM 11-anchor Design Space Consolidation + comparability/evidence QA before any research-gap declaration or method design.**

GraphWorld is now the final completed planned Phase C.5 core-WAM stress test.

Completed anchor set:

```text
P0048 LAW
P0045 WoTE
P0001 Epona
P0042 WorldDrive
P0046 World4Drive
P0061 SeerDrive
P0049 Drive-JEPA
P0062 Metis
P0063 DynFlowDrive
P0064 Discrete-WAM
P0065 GraphWorld
```

Canonical coordinate system remains:

```text
landscape/WAM_DIMENSION_ONTOLOGY_V1.md
landscape/WAM_DIMENSION_ONTOLOGY_V1_1_AMENDMENT.md
landscape/WAM_DIMENSION_ONTOLOGY_V1_2_AMENDMENT.md
landscape/WAM_DIMENSION_ONTOLOGY_V1_3_AMENDMENT.md
```

Latest comparison layer:

```text
landscape/WAM_COMPARISON_MATRIX_V1_3_GRAPHWORLD_EXTENSION.md
```

GraphWorld artifacts:

```text
papers/deep_analysis/P0065_GRAPHWORLD_DEEP_ANALYSIS_V2.md
audits/literature/PHASE_C5_GRAPHWORLD_AUDIT.md
landscape/P0065_GRAPHWORLD_ONTOLOGY_PROJECTION.md
```

---

# Why consolidation is now higher value than reading paper 12

The eleven anchors now span the main planning-centric WAM mechanisms:

```text
predictive auxiliary representation
predictive pretraining / transfer
shared world representation + direct policy
world-loss-shaped action policy
training-only consequence teacher
shared discrete world-policy model
online structured world-state conditioning
online distilled consequence representation
online compact future-mode selection
online recurrent consequence + explicit utility
online future/planner co-refinement
```

Continuing paper accumulation before consolidating would increase coverage but decrease coordinate clarity.

The next phase must answer:

> **Which papers are actually comparable on the same scientific axis, and which apparent disagreements are artifacts of different representation, supervision, deployment or evaluation regimes?**

---

# Required outputs

Create at minimum:

```text
landscape/WAM_DESIGN_SPACE_MAP_V2.md
audits/research_synthesis/WAM_11_ANCHOR_COMPARABILITY_QA.md
landscape/WAM_EVIDENCE_STRENGTH_MATRIX.md
landscape/WAM_MECHANISM_FAMILIES_V2.md
```

Optional if justified:

```text
landscape/WAM_RESEARCH_TENSIONS_V1.md
```

Do **not** yet create final research gaps/method proposals. `RESEARCH_TENSIONS` may state contradictions or unresolved scientific tensions only.

---

# Task 1 — Rebuild the design space from mechanisms, not substrates

Do not organize mainly as:

```text
RGB / BEV / latent / token / graph
```

Those are representation substrates, not the highest-level planning mechanism.

Primary mechanism families should be derived from planning interface, e.g.:

```text
A. future-as-training signal
B. predictive representation pretraining / inheritance
C. shared world representation + direct policy
D. training-only world consequence teacher / label generator
E. online world-state-conditioned direct policy
F. online distilled future consequence evaluator
G. online compact future-mode selector
H. online recurrent consequence model + explicit utility
I. online world/planner internal co-refinement
J. shared world-policy generative backbone with planning-only deployment
```

Then place every anchor with evidence.

---

# Task 2 — Separate six forms of `world helps planning`

Force every paper into explicit answers:

```text
1. representation shaping?
2. parameter/gradient sharing?
3. online world state conditioning?
4. online candidate consequence prediction?
5. explicit utility/value over consequence?
6. search/selection over alternative actions?
```

No paper may be summarized simply as:

```text
world model improves planning
```

---

# Task 3 — Build a future-truth taxonomy

For each anchor separate:

```text
future object predicted
future target provenance
one factual future vs alternative futures
candidate-specific output?
candidate-specific supervision?
reactive other-agent truth?
external intervention validation?
```

Mandatory control:

```text
multiple predicted futures
!=
multiple counterfactual truths
```

---

# Task 4 — Build the deployment lifecycle map

For each paper draw:

```text
TRAINING GRAPH
→ knowledge transformation / distillation / transfer
→ DEPLOYMENT GRAPH
```

Key families already exposed:

```text
LAW: auxiliary predictor → discarded output
Drive-JEPA: JEPA predictor → encoder transfer
Epona: joint visual/trajectory training → planning can skip visual generator
Metis: world co-training → action-only deployment
DynFlowDrive: flow WM teacher → score head deployment
Discrete-WAM: shared world-policy pretraining → action-only planning task
WorldDrive: heavy generative teacher → lightweight online future surrogate
GraphWorld: compact online structured world state retained
World4Drive: compact future predictor retained
WoTE: recurrent transition retained
SeerDrive: internal world/planner loop retained
```

---

# Task 5 — Temporal-coordinate QA

Use F07/F08/J08 to distinguish:

```text
physical future time
history time
world-rollout step
flow/diffusion transport time
policy denoising/editing time
planner/world refinement iteration
```

Create a cross-paper table.

Mandatory rule:

```text
more solver/refinement steps
!=
longer physical prediction horizon
```

GraphWorld and DynFlowDrive are especially important controls here.

---

# Task 6 — Long-horizon taxonomy

Separate:

```text
longer trajectory output
longer history context
persistent latent memory
multi-step world prediction
longer consequence rollout
reactive closed-loop execution horizon
```

Use GraphWorld as the key negative control:

```text
6s long-horizon planning
without 6s explicit world rollout
```

---

# Task 7 — Safety / risk / value separation

For every anchor distinguish:

```text
explicit risk state / field
explicit collision probability
explicit utility/value head
simulator/PDM reward supervision
implicit safety in representation
safety only measured in evaluation
```

Do not equate:

```text
lower collision rate
with
explicit learned risk representation
```

This is especially important before later considering any risk-aware WAM direction.

---

# Task 8 — Evaluation-regime normalization

Every benchmark/result must be normalized as:

```text
open-loop offline
non-reactive pseudo-simulation
reactive simulator closed-loop
real-world closed-loop
visual autoregressive rollout only
```

Binding examples:

```text
NAVSIM ≠ reactive closed loop
Bench2Drive/CARLA = reactive simulator closed loop
visual rollout ≠ policy-environment closed loop
```

Then identify which scientific claims each regime can and cannot support.

---

# Task 9 — Evidence-strength matrix

For each central mechanism claim, grade evidence by:

```text
A. direct matched ablation
B. source-code verified mechanism
C. paper equation/architecture only
D. headline cross-paper comparison
E. author interpretation only
```

Track source status separately:

```text
SOURCE-COMPLETE
SOURCE-PARTIAL
SOURCE-BLOCKED
```

Current source-blocked/monitor examples include:

```text
Metis implementation
DynFlowDrive implementation
Discrete-WAM implementation
GraphWorld implementation
```

Do not penalize a scientific mechanism merely because code is unreleased; instead lower implementation-certainty separately.

---

# Task 10 — Strongest matched controls per paper

For each anchor record only the most decision-relevant matched controls, e.g.:

```text
LAW           ± latent future auxiliary
WoTE          evaluator no-future → + predicted future
Epona         trajectory-only → joint visual/trajectory
WorldDrive    trajectory rewarder → + distilled future feature
World4Drive   same priors/intentions, no-WM → + WM
SeerDrive     future-aware × iterative 2×2
Drive-JEPA    representation pretrain / proposal-selection decomposition
Metis         no video co-train → video co-train; joint/isolated/asymmetric
DynFlowDrive  static WM → flow WM; selection-factor decomposition
Discrete-WAM  scratch/FT/pretrain + decision/RL controls
GraphWorld    baseline→ECIG→WSCP; Stage I→II; diffusion→flow; dense→ego-star
```

Do not use best headline SOTA result as the primary evidence if a matched internal control exists.

---

# Task 11 — Produce scientific tensions, not gaps

Only after the matrices are clean, extract tensions such as:

```text
better world fidelity vs better planning relevance
explicit consequence rollout vs compact representation conditioning
training-time world modeling vs online model-basedness
stronger jointness vs stronger deployment dependence
more future detail vs decision relevance
more candidate diversity vs selection quality
more solver steps vs planning quality
factual-future prediction vs intervention consequence validity
structured interaction semantics vs true reactive dynamics
```

Each tension must contain:

```text
supporting anchors
contradicting/control anchors
evidence strength
what is genuinely unresolved
what experiment would falsify each interpretation
```

Do not call a tension a `research gap` yet.

---

# Stop condition

Phase D may only be unpaused after:

```text
11-anchor comparability QA complete
+
evidence-strength matrix complete
+
mechanism families stable
+
major terminology/evaluation mismatches normalized
+
source-status caveats recorded
```

Until then:

```text
NO final research-gap declaration
NO method design
NO forced risk-field proposal
```
