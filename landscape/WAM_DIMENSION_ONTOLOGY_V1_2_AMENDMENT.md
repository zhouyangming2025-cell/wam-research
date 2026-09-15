# WAM Dimension Ontology V1.2 Amendment — Drive-JEPA

Last updated: 2026-09-15

Status: **STABLE MINOR AMENDMENT — one dimension survives back-projection**

Base coordinate system:

```text
landscape/WAM_DIMENSION_ONTOLOGY_V1.md
landscape/WAM_DIMENSION_ONTOLOGY_V1_1_AMENDMENT.md
```

Trigger paper:

```text
P0049 Drive-JEPA
```

This amendment follows the same extension gate as V1.1:

```text
fill existing ontology first
→ isolate residue
→ merge anything already expressible
→ back-project surviving distinction
→ add only if cross-paper comparison changes
```

---

# 1. Residue exposed by Drive-JEPA

The existing ontology already captures:

```text
F04  temporal factorization
F05  horizon / intermediate-state use
G01  target truth source
G02  target encoder / stop-gradient treatment
E01  action conditioning
M01  future-knowledge lifecycle
```

But none of these explicitly records a crucial property:

> **What temporal information is visible to the predictor when its target is hidden?**

That omission allows fundamentally different objectives to collapse into the same label `predictive representation learning`.

Examples:

```text
Drive-JEPA / V-JEPA
randomly hide spatiotemporal patches inside a video clip
→ predict masked latent from remaining visible context

ViDAR
historical images only
→ predict chronologically future point clouds

LAW
current scene + ego action
→ predict a later factual future latent

WoTE
current predicted state + candidate action
→ predict next future state recurrently
```

These objectives impose different causal/temporal learning obligations even if they all predict a latent or future-related representation.

---

# 2. F07 — Prediction temporal / observability geometry

**Scientific question**

When the model predicts a target representation/state during training or deployment, which temporal parts of the sample are visible and which are held out?

**Why it matters**

The term `prediction` can describe:

```text
same-window masked completion
past-only→unseen-future forecasting
current→future endpoint prediction
recurrent next-state transition
future prediction with partial future context
bidirectional imputation
```

Only some of these require a model to extrapolate forward in time from past/current information alone.

**Typical values**

```text
NOT APPLICABLE
RANDOM-MASK SAME-WINDOW SPATIOTEMPORAL COMPLETION
PAST/HISTORY-ONLY → UNSEEN FUTURE
CURRENT → FUTURE ENDPOINT
RECURRENT NEXT-STATE / AUTOREGRESSIVE FUTURE
PARTIAL-FUTURE-CONTEXT COMPLETION
HYBRID FUTURE MASKING
FULL-EPISODE / TRAJECTORY JOINT GENERATION
UNCLEAR / NOT REPORTED
```

Modifiers that remain in other dimensions:

```text
action condition         → E01/E02
future substrate         → F01/F02
model class              → F03
factorization            → F04
horizon                   → F05
uncertainty               → F06
target-network treatment → G02
```

Do not overload F07 with those properties.

**Evidence required**

Trace the information set available to the predictor at the moment a target is predicted:

```text
visible frames/tokens
masked frames/tokens
whether any future tokens are visible
whether only history/current information is available
whether prediction is recursively fed forward
```

**Common trap**

```text
uses video temporal masking
!=
causal future forecasting
```

and:

```text
predictive representation
!=
online world transition model
```

---

# 3. Drive-JEPA value

Drive-JEPA inherits the paper-described V-JEPA objective:

```text
RANDOM-MASK SAME-WINDOW SPATIOTEMPORAL COMPLETION
```

The target is the EMA target-encoder representation at randomly masked spatiotemporal positions. The stated objective does not require history-only context and is not action-conditioned.

This does not make the representation non-predictive; it limits the stronger claim that the pretext task itself establishes causal future-world dynamics.

---

# 4. Back-projection onto existing anchors

| Paper | F07 Prediction temporal / observability geometry | Consequence for interpretation |
|---|---|---|
| **LAW** | **CURRENT → FUTURE ENDPOINT** (with current predicted ego waypoint/action as condition) | explicit later factual latent prediction; stronger chronological-future obligation than random-mask completion |
| **WoTE** | **RECURRENT NEXT-STATE / AUTOREGRESSIVE FUTURE** | each learned state-action transition advances predicted future time |
| **Epona** | **PAST/HISTORY-ONLY → UNSEEN FUTURE** for visual generation; trajectory branch generates future ego motion from history/shared latent | predictive generative task is chronologically forward |
| **WorldDrive** | **PAST/HISTORY + TRAJECTORY CONDITION → UNSEEN FUTURE** | TA-DWM is trained to generate future scene conditioned on history and ego trajectory |
| **World4Drive** | **CURRENT → FUTURE ENDPOINT** | intention/action-conditioned compact future latent |
| **SeerDrive** | **CURRENT → FUTURE ENDPOINT** | predicts final-horizon future BEV, then internally co-refines world/planner representations |
| **Drive-JEPA** | **RANDOM-MASK SAME-WINDOW SPATIOTEMPORAL COMPLETION** | predictive video representation pretraining; does not itself enforce causal history-only future modeling |

The distinction therefore changes scientific comparison for every prior anchor and survives the V1 extension rule.

---

# 5. Historical/control back-projection

Two nearby predictive-pretraining controls make the distinction especially visible.

## ViDAR

```text
PAST/HISTORY-ONLY → UNSEEN FUTURE
+
RECURRENT/AUTOREGRESSIVE FUTURE
```

Historical images are encoded and an autoregressive decoder forecasts future point clouds. The future decoder is not the deployed downstream planner interface, but the pretext task is explicitly chronological future forecasting.

## Auto-JEPA

```text
CURRENT/HISTORY → FUTURE EGO-MOTION LATENT
```

The future target is a frozen representation of the actual future ego trajectory; the predicted intent remains online as a retrieval key.

## WA-JEPA

```text
HYBRID FUTURE MASKING
```

Its full-mask branch exposes history only and predicts all future tokens; its patch-mask branch retains partial future context. WA-JEPA explicitly motivates this change by distinguishing V-JEPA random-mask completion from future-directed prediction.

These controls reinforce the stability of F07.

---

# 6. What was NOT added

Drive-JEPA exposed several tempting new labels that are already covered:

```text
JEPA target EMA / stop-gradient
→ G02 already covers target-network treatment

pretraining predictor removed at deployment
→ M01–M03 already cover lifecycle/model-class transformation

frozen vs fine-tuned transferred encoder
→ C03 + L05 already cover trainability/transfer

proposal refinement repeated four times
→ J08 already covers iteration semantics

simulator pseudo-teacher trajectory supervision
→ G04/G05 + D04–D06 already cover utility/policy supervision and candidate construction
```

No duplicate dimensions are added for these.

---

# 7. Canonical rule after V1.2

Any paper described as `predictive`, `JEPA`, `latent world model`, `future representation`, or `world-action pretraining` must now answer both:

```text
WHAT is predicted?        → F01/F02/G01/G02
WHAT WAS VISIBLE?         → F07
```

Only after those are explicit should we ask whether the predictive knowledge enters planning online (`J02/J03`, `M01–M03`).

Until a consolidated ontology is generated, canonical use is:

```text
WAM_DIMENSION_ONTOLOGY_V1.md
+
WAM_DIMENSION_ONTOLOGY_V1_1_AMENDMENT.md
+
WAM_DIMENSION_ONTOLOGY_V1_2_AMENDMENT.md
```
