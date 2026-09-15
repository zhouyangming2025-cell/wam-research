# WAM Dimension Discovery Addendum — World4Drive

Last updated: 2026-09-15

Status: **FIFTH-ANCHOR DISCOVERY COMPLETE — ready for ontology merge/split pass**

Source:

```text
papers/deep_analysis/P0046_WORLD4DRIVE_DEEP_ANALYSIS_V2.md
audits/literature/PHASE_C5_WORLD4DRIVE_AUDIT.md
papers/raw_md/P0046_World4Drive/P0046_World4Drive.raw.md
```

This file records only the dimensions/refinements exposed most clearly by World4Drive. It supplements:

```text
landscape/WAM_DIMENSION_DISCOVERY_LOG.md
landscape/WAM_DIMENSION_DISCOVERY_ADDENDUM_EPONA_WORLDDRIVE.md
```

---

# 1. World4Drive forces scorer semantics to split

Earlier analyses often used a broad chain:

```text
candidate → future → score → select
```

World4Drive shows that `score` is not one scientific object.

Stable candidate dimension:

## Scorer semantics

Possible values:

```text
utility / value
risk / safety
imitation / expert-likeness
factual-future consistency
mode posterior / likelihood
hybrid
```

World4Drive position:

```text
training target:
which predicted future latent is nearest to the one factual observed future latent?

therefore:
primary semantics = factual-future consistency / mode classification
```

Contrast:

```text
WoTE
= explicit imitation + NC/DAC/TTC/comfort/progress utility heads

WorldDrive FAR
= future representation + PDMS/oracle preference ranking

World4Drive
= nearest-factual-future mode index → focal classification
```

This distinction should survive ontology v1.

---

# 2. Mode-assignment mechanism becomes an independent dimension

World4Drive predicts K future hypotheses but has no externally observed mode ID.

It creates one through:

```text
d_k = distance(predicted future latent k, factual future latent)
j = argmin_k d_k
```

Then `j` controls:

```text
reconstruction target
ScoreNet class target
expert trajectory supervision
```

New stable candidate dimension:

## Multimodal branch assignment / mode identity

Possible mechanisms:

```text
fixed semantic label
nearest expert trajectory
nearest factual future representation
simulator value ranking
oracle best-of-N
learned latent assignment
```

World4Drive:

```text
nearest factual future latent
```

---

# 3. Counterfactuality must be represented as a vector, not one level

World4Drive makes a single ordinal counterfactual score insufficient.

Minimum three fields:

```text
A. output branching
B. alternative-future supervision
C. reactive response evidence
```

World4Drive:

```text
A. output branching
   YES — K candidate-conditioned future latents

B. alternative-future supervision
   NO — only one factual observed future latent

C. reactive response evidence
   NOT ESTABLISHED — no matched intervention-specific other-agent futures
```

Therefore:

> branch multiplicity is architectural counterfactuality, not causal identification.

The provisional CF ladder can remain as shorthand, but ontology v1 should store these three fields separately.

---

# 4. Endpoint future vs rollout sequence is a real design axis

World4Drive uses:

```text
current latent + candidate action
→ compact future latent at selected offset t+n
→ selector
```

Compare:

```text
LAW
single future target latent for auxiliary learning

WoTE
recurrent sequence of future BEV states consumed by reward model

Epona
frame-autoregressive visual rollout capability, but not required by planning

WorldDrive
teacher-generated future representation distilled to lightweight surrogate

World4Drive
single compact candidate future endpoint per intention
```

Stable candidate dimension:

## Future temporal object consumed by planning

Values may include:

```text
none
single future endpoint
multi-step sequence
recurrent rollout
full generated trajectory/world episode
distilled summary of future
```

---

# 5. Branch parameterization / parameter sharing

World4Drive's six future modes are not six independent WMs.

They are produced by one shared conditioned predictor:

```text
Q_future + L_t + A^k
→ shared cross-attention predictor
→ L^k_{t+n}
```

New/refined dimension:

## Alternative-future branch parameterization

```text
shared model + different condition
shared trunk + mode heads
independent per-mode models
search tree through shared transition
```

World4Drive:

```text
shared model + different action/intention condition
```

---

# 6. Representation origin stack is confirmed as mandatory

World4Drive's current world latent includes:

```text
image feature
+ metric-depth prior
+ semantic/VLM pseudo-supervision/prior
+ previous-frame temporal feature
```

Thus planning gains need separate attribution for:

```text
imported foundation knowledge
current-state temporal representation
future prediction
mode selector
```

This reinforces WorldDrive's earlier lesson:

```text
foundation prior gain != WM-specific dynamics gain
```

Stable ontology requirement:

## Representation origin / prior stack

Record each imported prior and whether it is frozen, pseudo-labeling, pretrained initialization, or jointly learned.

---

# 7. Strongest matched control for World4Drive

Do not use LAW→World4Drive headline delta as the primary WM effect.

Most informative control:

```text
physical priors + intentions, no WM
0.61 L2 / 0.36 collision

physical priors + intentions + WM selector
0.50 L2 / 0.16 collision
```

Interpretation:

```text
future-latent predictor + mode assignment + ScoreNet
adds planning value beyond intention-based multimodal candidates
```

What remains unproven:

```text
pure future dynamics accuracy contribution
vs
mode separation / factual matching
vs
extra training regularization
```

This confirms a stable evidence field:

> strongest matched control immediately before the claimed WAM mechanism is added.

---

# 8. Five-anchor future-knowledge lifecycle is now stable enough for v1

```text
LAW
predictive auxiliary task
→ future output not consumed by deployed selection

Epona
visual future jointly shapes shared latent
→ planning uses direct generative trajectory policy
→ visual future optional/off in planning

WoTE
compact learned transition model remains online
→ recurrent future states → explicit reward → selection

WorldDrive
heavy generative WM
→ frozen future teacher
→ distilled lightweight future surrogate
→ online ranking

World4Drive
compact candidate-conditioned future predictor remains online directly
→ factual-mode ScoreNet
→ selection
```

Stable dimension name recommendation:

## Future-knowledge lifecycle / deployment path

Record:

```text
where future knowledge is learned
what object carries it
whether it changes model class through transfer/distillation
whether future prediction remains active online
how it enters final action selection
```

---

# 9. Five-anchor mechanism map before ontology freeze

| Axis | LAW | WoTE | Epona | WorldDrive | World4Drive |
|---|---|---|---|---|---|
| future role | representation teacher | consequence model | cross-modal representation shaping + visual simulator | representation inheritance + distilled consequence | online compact future hypothesis |
| action mechanism | single waypoint policy | candidate bank + selection | direct flow/diffusion policy | candidate bank + coarse score + re-rank | 6 intention candidates + selector |
| future online in selection | no | yes | visual future no | yes, distilled surrogate | yes, direct compact latent |
| temporal future object | single target latent | recurrent BEV sequence | visual next-frame autoregression | distilled summary | one endpoint latent/mode |
| scorer type | N/A | explicit utility | N/A | preference/value ranking | factual-mode classification |
| consequence truth source | factual future latent | simulator/semantic targets | factual future image/trajectory | learned TA-DWM teacher | one factual future latent for branch assignment |
| value truth source | N/A | expert + simulator rules | trajectory demonstrations | PDMS preference/oracle | derived mode index from factual latent distance |
| representation prior | host planner | camera+LiDAR BEV | visual tokenizer + history | CogVideoX + TA-DWM | depth + semantic foundation priors |
| candidate count | 1 | 256 | no scored bank | 256 → top-K | 6 |
| reactive alternative truth | no | no in audited NAVSIM path | no candidate evaluator | no real matched alternatives | no real matched alternatives |

---

# 10. Dimensions now ready to merge/split

The next synthesis should no longer preserve discovery IDs. Merge them into stable families such as:

```text
A. Problem / role of world knowledge
B. Observation and current-state representation
C. Representation provenance and priors
D. Action / candidate space
E. Action→world coupling
F. Dynamics / future modeling
G. Future supervision and truth sources
H. Multimodal branch assignment
I. Counterfactuality / reactivity
J. World→planning interface
K. Scorer / value semantics
L. Training topology and gradient coupling
M. Future-knowledge lifecycle / deployment
N. Compute / latency / pruning
O. Evaluation regime and evidence strength
P. Safety / uncertainty / risk semantics
```

These are family headings only, not yet the final dimension list.

Next task:

```text
all discovery logs
→ merge/split pass
→ WAM_DIMENSION_ONTOLOGY_V1.md
→ WAM_COMPARISON_MATRIX_V1.md
```
