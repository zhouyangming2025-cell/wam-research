# WAM Dimension Ontology V1.3 Amendment — DynFlowDrive

Last updated: 2026-09-15

Status: **STABLE MINOR AMENDMENT — one dimension survives back-projection**

Base coordinate system:

```text
landscape/WAM_DIMENSION_ONTOLOGY_V1.md
landscape/WAM_DIMENSION_ONTOLOGY_V1_1_AMENDMENT.md
landscape/WAM_DIMENSION_ONTOLOGY_V1_2_AMENDMENT.md
```

Trigger paper:

```text
P0063 DynFlowDrive
```

Extension rule:

```text
fill existing ontology
→ isolate residue
→ merge duplicate concepts
→ back-project surviving distinction
→ add only if scientific comparison changes
```

---

# 1. Residue exposed by DynFlowDrive

DynFlowDrive introduces a rectified-flow latent transition:

```text
physical observations:
z_t ........................ z_{t+1}

internal transport:
s = 0 → s = 1
```

The paper describes intermediate integration steps as progressively simulating world evolution and uses the directional consistency of flow velocities as a `stability` signal.

Existing dimensions already capture:

```text
F03 dynamics operator
F04 endpoint/recurrent/autoregressive temporal factorization
F05 physical horizon/intermediate-state consumption
F07 prediction observability geometry
J08 inference iteration semantics
N06 quality-vs-step/scale curve
```

But none asks the decisive question:

> **Is the internal coordinate of a dynamics/generative process actually identified with physical-world time?**

That distinction matters because a model can have many mathematically smooth denoising/transport steps between two physical states without any intermediate step corresponding to an observed physical time.

---

# 2. Why F04 / F05 / F07 / J08 are not enough

## F04 — Temporal factorization

F04 answers:

```text
endpoint vs sequence vs recurrent rollout vs autoregressive frame generation
```

It does not tell us whether internal solver states have physical timestamps.

## F05 — Horizon / intermediate-state use

F05 records physical horizon and whether intermediate future states are consumed. It does not determine whether an internal interpolation state is a physically supervised future state.

## F07 — Prediction temporal / observability geometry

F07 asks what temporal evidence is visible when predicting the target. It does not identify the semantics of the solver / denoising coordinate itself.

## J08 — Inference iteration semantics

J08 asks what advances during planner/model **inference iteration**. DynFlowDrive's key flow path is training-only, so silently extending J08 would alter its existing meaning.

Therefore a separate dynamics-family axis is warranted.

---

# 3. F08 — Internal transition-coordinate / physical-time alignment

**Scientific question**

When a world/dynamics model contains intermediate states indexed by an internal variable, what does that variable mean relative to physical scene time?

**Why it matters**

Terms such as:

```text
continuous evolution
velocity field
progressive dynamics
rollout step
flow step
diffusion step
```

can refer to very different objects.

A solver coordinate can be useful computationally while carrying no direct physical-time identity.

**Typical values**

```text
NOT APPLICABLE / DIRECT ENDPOINT

PHYSICALLY INDEXED FUTURE TIME
    intermediate states have explicit physical timestamps / targets

AUTOREGRESSIVE PHYSICAL FRAME TIME
    each generated step advances the observation timeline

GENERATIVE DENOISING / TRANSPORT COORDINATE
    intermediate states are solver/noise/transport states, not physical-time labels

PHYSICALLY INDEXED OUTER TIME + INTERNAL GENERATIVE TIME
    each physical future frame/state may itself require diffusion/flow iterations

INTERNAL REPRESENTATION REFINEMENT
    repeated hidden-state refinement, not scene time
    (primarily also recorded by J08)

MIXED / HIERARCHICAL

UNCLEAR / NOT REPORTED
```

**Evidence required**

For an intermediate index `r`, ask:

```text
Does r map to a real/simulator timestamp?
Is there a target observation/state at that timestamp?
Does one step execute an action/environment transition?
Or is r only a denoising / interpolation / solver coordinate?
```

**Common traps**

```text
K flow/diffusion steps
!= K future physical timesteps

smooth path in latent transport coordinate
!= validated smooth physical evolution

dz/ds
!= dz/dtau
unless s is explicitly identified with physical time tau
```

---

# 4. DynFlowDrive value

DynFlowDrive defines:

```text
x_s = (1-s)a + s z_{t+1}
s ∈ [0,1]
```

and integrates a learned velocity field over `s`.

Only endpoint observations `t` and `t+1` are used as physical scene targets. No paper evidence pairs intermediate `s` states with intermediate observed physical frames.

Therefore:

```text
F08 = GENERATIVE / RECTIFIED-FLOW TRANSPORT COORDINATE
       BETWEEN TWO PHYSICAL ENDPOINTS
```

The paper's five-step optimum:

```text
1 → 3 → 5 → 10 integration steps
```

is a solver/teacher-resolution ablation, not a future-horizon ablation.

This matters especially because the paper computes flow-direction angular consistency over `s` and interprets it as physical stability.

Canonical boundary:

```text
transport-direction consistency
!= directly validated physical-time stability
```

---

# 5. Back-projection onto prior anchors

| Paper | F08 internal-coordinate / physical-time alignment | Scientific consequence |
|---|---|---|
| **LAW** | **NOT APPLICABLE / DIRECT FUTURE ENDPOINT** | predicts a later factual latent directly; no internal generative trajectory is claimed as physical evolution |
| **WoTE** | **PHYSICALLY INDEXED FUTURE TIME** | recurrent BEV transitions advance explicit predicted scene time; internal NN layers are not treated as temporal states |
| **Epona** | **PHYSICALLY INDEXED OUTER FRAME TIME + INTERNAL GENERATIVE/DENOISING TIME** | visual future frames advance physical time, while DiT denoising iterations are solver/generative coordinates |
| **WorldDrive** | **PHYSICALLY INDEXED FUTURE VIDEO/LATENT + INTERNAL DIFFUSION TIME** in the heavy teacher | diffusion sampling step is not itself a driving timestamp |
| **World4Drive** | **NOT APPLICABLE / DIRECT ENDPOINT LATENT** | one compact future endpoint per candidate; no continuous internal path receives physical semantics |
| **SeerDrive** | **INTERNAL REPRESENTATION REFINEMENT** for the repeated world↔planner loop; final-horizon future remains fixed | reinforces J08: refinement iteration is not future-time advancement |
| **Drive-JEPA** | **NOT APPLICABLE to deployed world dynamics**; JEPA masking positions are spatiotemporal data indices, not a transport-time path | predictive representation objective does not create a physical dynamics path |
| **Metis** | **GENERATIVE FLOW/DENOISING COORDINATE + SEPARATE PHYSICAL ACTION/VIDEO HORIZON** | action/video flow time is not waypoint/video physical time |
| **DynFlowDrive** | **RECTIFIED-FLOW TRANSPORT COORDINATE BETWEEN t AND t+1; INTERMEDIATE s NOT PHYSICALLY SUPERVISED** | `continuous latent evolution` must not automatically be upgraded to continuous physical dynamics |

This back-projection changes interpretation across multiple prior anchors and therefore passes the ontology extension rule.

---

# 6. Relation to J08

Use the two axes together:

```text
F08
= what an internal WORLD/DYNAMICS transition coordinate means relative to physical time

J08
= what advances across repeated INFERENCE iterations in the decision graph
```

Examples:

```text
DynFlowDrive
F08 = flow transport coordinate
J08 = deployed planner has no world-model iteration

SeerDrive
F08 = internal representation refinement / no physical-time transport path
J08 = world↔planner co-refinement

WoTE
F08 = physically indexed world transition
J08 = physical-time latent rollout

Epona
F08 = outer physical frame time + inner denoising time
J08 = generative denoising / autoregressive observation rollout depending mode
```

Do not merge them unless a future consolidated ontology explicitly redesigns both dimensions.

---

# 7. What was NOT added

DynFlowDrive also exposed several tempting labels that are already covered:

```text
training-only world-derived candidate-label teacher
→ J01 + K05 + M01–M03

flow-stability score semantics
→ K02 + K04 + K05

candidate-conditioned world branching with one factual target
→ E03 + G01/G06/G07 + I01/I02

flow-step performance curve
→ N06

paper equation / sampling inconsistency
→ O08 source-verification / audit boundary
```

No duplicate dimensions are added for these.

---

# 8. Canonical control after V1.3

Any WAM using diffusion, flow matching, rectified flow, iterative latent dynamics or repeated hidden-state updates must now answer two separate questions:

```text
WHAT FUTURE IS PREDICTED?
→ F01–F07

WHAT DOES EACH INTERNAL STEP MEAN IN TIME?
→ F08
```

Binding scientific rule:

> **An internal path between physical endpoints is not evidence of physically correct intermediate evolution unless intermediate states are explicitly time-identified and validated.**

Until a consolidated ontology is generated, canonical use is:

```text
WAM_DIMENSION_ONTOLOGY_V1.md
+
WAM_DIMENSION_ONTOLOGY_V1_1_AMENDMENT.md
+
WAM_DIMENSION_ONTOLOGY_V1_2_AMENDMENT.md
+
WAM_DIMENSION_ONTOLOGY_V1_3_AMENDMENT.md
```
