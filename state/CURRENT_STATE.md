# CURRENT_STATE

Last updated: **2026-09-15 — DynFlowDrive stress test COMPLETE; Ontology V1.3 ACTIVE; Discrete-WAM NEXT**

## Research north star

```text
WAM / World Model + one-stage End-to-End + Planning-centric autonomous driving
```

Core 2.2 WAM remains primary. WAM+VLA is secondary/control. Risk/predictive-risk remains optional prior knowledge, not a required destination.

## Methodology in force

```text
FIELD UNDERSTANDING FIRST
→ complete core-WAM coverage
→ comparative anchor deep reads
→ dimension-first normalization
→ evidence QA
→ only then adversarial problem discovery
→ falsification
→ method design
```

Phase D remains **PAUSED**.

Canonical reading stack:

```text
paper-deep-reader
→ mechanism / formula / figure reconstruction

academic-research-agent source/claim gate
→ source/version discipline + claim/evidence separation

literature-reading-and-synthesis
→ immediate cross-paper scientific comparison

WAM Ontology
→ full projection + residue/back-projection gate
```

Authority:

```text
landscape/WAM_READING_SKILL_STACK.md
```

---

# Dimension-first normalization status

```text
P0048 LAW          COMPLETE v2
P0045 WoTE         COMPLETE v2
P0001 Epona        COMPLETE v2
P0042 WorldDrive   COMPLETE v2
P0046 World4Drive  COMPLETE v2
P0061 SeerDrive    COMPLETE v2 first pass
P0049 Drive-JEPA   COMPLETE v2 first pass + source audit
P0062 Metis        COMPLETE v2 first pass + paper/official-repo audit
P0063 DynFlowDrive COMPLETE v2 first pass + paper/official-repo audit
```

Canonical coordinate system:

```text
landscape/WAM_DIMENSION_ONTOLOGY_V1.md
landscape/WAM_DIMENSION_ONTOLOGY_V1_1_AMENDMENT.md
landscape/WAM_DIMENSION_ONTOLOGY_V1_2_AMENDMENT.md
landscape/WAM_DIMENSION_ONTOLOGY_V1_3_AMENDMENT.md
```

Comparison layer:

```text
landscape/WAM_COMPARISON_MATRIX_V1.md
landscape/WAM_COMPARISON_MATRIX_V1_1_SEERDRIVE_EXTENSION.md
landscape/WAM_COMPARISON_MATRIX_V1_2_DRIVEJEPA_EXTENSION.md
landscape/WAM_COMPARISON_MATRIX_V1_2_METIS_EXTENSION.md
landscape/WAM_COMPARISON_MATRIX_V1_3_DYNFLOWDRIVE_EXTENSION.md
```

DynFlowDrive artifacts:

```text
papers/deep_analysis/P0063_DYNFLOWDRIVE_DEEP_ANALYSIS_V2.md
audits/literature/PHASE_C5_DYNFLOWDRIVE_AUDIT.md
landscape/P0063_DYNFLOWDRIVE_ONTOLOGY_PROJECTION.md
```

---

# DynFlowDrive stable result

## Source/version boundary

```text
paper: arXiv:2603.19675v2, 2026-05-03
official repo: xiaolul2/DynFlowDrive
latest observed public commit: c665dc577a0939543fa7abe64d28eadaec28283c
```

As of 2026-09-15 the official repo still exposes only README/teaser and states that code will be released once accepted.

Therefore:

```text
paper architecture/equations/ablations  PAPER-VERIFIED
implementation details                 SOURCE-UNVERIFIED
```

Two paper-level ambiguities remain unresolved until code release:

```text
Eq.7:  x_s=(1-s)a+s z_{t+1}
→ mathematically dx_s/ds=z_{t+1}-a

Eq.10 target written as:
(1-s)(z_{t+1}-a)

and:
training interpolation starts from stochastic anchor a,
while sampling prose says integration starts from current latent z_t.
```

Do not silently repair these by inference.

## Canonical mechanism

```text
TRAINING-ONLY FLOW-DYNAMICS MODE-SUPERVISION WAM
```

Training:

```text
current observation
→ multimodal planner
→ candidate trajectories + score head

current factual world latent + candidate trajectory
→ rectified-flow latent world model
→ predicted transport path / endpoint
→ reconstruction + flow objectives
→ flow-direction stability

GT trajectory error
+ factual-latent reconstruction
+ flow stability
→ hybrid criterion C_n
→ n* positive candidate
→ supervise planner score head
```

Deployment:

```text
current observation
→ candidate trajectories + learned scores
→ argmax

world model       = OFF
future latent      = NOT COMPUTED
flow integration   = NOT COMPUTED
flow stability     = NOT COMPUTED
```

Thus DynFlowDrive is **not** an online candidate→future→score planner.

---

# DynFlowDrive strongest scientific correction

Three time axes are distinct:

```text
physical scene time τ
!= rectified-flow transport coordinate s
!= planner/query refinement iteration k
```

Only physical endpoints `t` and `t+1` are observed as world-state targets. Intermediate `s` states are internal transport/solver states.

Binding control:

```text
smooth latent path over s
!= validated smooth physical evolution over τ

dz/ds
!= dz/dτ
unless physical-time identity is explicitly established
```

This motivated Ontology V1.3:

```text
F08  Internal transition-coordinate / physical-time alignment
```

DynFlowDrive value:

```text
RECTIFIED-FLOW TRANSPORT COORDINATE BETWEEN PHYSICAL ENDPOINTS;
INTERMEDIATE s STATES ARE NOT PHYSICALLY TIME-SUPERVISED
```

F08 back-projects meaningfully onto Epona, WorldDrive, Metis, WoTE, SeerDrive and other anchors and therefore passes the ontology extension gate.

---

# DynFlowDrive supervision and counterfactual boundary

```text
N candidate trajectories
→ N candidate-conditioned flow fields / outputs

but factual world target from logs
= ONE next world latent z_{t+1}
```

Therefore:

```text
candidate-specific world output                    YES
candidate-specific observed alternative future GT NO
reactive surrounding-agent truth                  NO / NOT ESTABLISHED
external intervention-validity evidence           ABSENT
```

Continuous candidate-conditioned flow does not solve the alternative-action supervision problem.

---

# DynFlowDrive strongest matched evidence

## Static WM → Flow WM

```text
Static WM   0.61 Avg L2 / 0.30 Avg CR
Flow WM     0.59        / 0.26
```

This reasonably isolates a benefit from the rectified-flow parameterization inside the authors' framework.

## Representation prior

```text
Flow WM                    0.59 / 0.26
+ pretrained World Feature 0.57 / 0.22
```

Thus foundation representation quality remains an independent contribution.

## Selection criterion ladder

```text
none              0.61 / 0.30
L2 only           0.59 / 0.24
+ reconstruction  0.58 / 0.22
+ flow stability  0.57 / 0.22
```

The full selection teacher matters substantially, but the final angular flow-stability term itself has only a modest incremental effect.

## Flow integration steps

```text
steps   Avg L2   Avg CR
1       0.60     0.28
3       0.59     0.23
5       0.57     0.22
10      0.59     0.24
```

This is a **solver/teacher-resolution curve**, not a future-horizon curve.

---

# Headline-comparison correction

The highlighted SSR delta is not fully matched:

```text
SSR*                             0.39 L2 / 0.15 CR
DynFlowDrive(SSR)                0.35    / 0.14
DynFlowDrive(SSR) + ego status   0.31    / 0.11
```

The 0.31/0.11 row includes extra ego-status input. The more defensible matched WM comparison is approximately:

```text
0.39 → 0.35 L2
0.15 → 0.14 CR
```

This strengthens:

```text
matched controls > headline SOTA deltas
```

---

# Evaluation-regime correction

The paper calls NAVSIM `closed-loop`.

Project-standard classification remains:

```text
NAVSIM v1
= NON-REACTIVE DATA-DRIVEN / PSEUDO-SIMULATION PLANNING
```

Therefore DynFlowDrive's 88.7 PDMS supports strong planning performance under NAVSIM's non-reactive regime, but does **not** validate reactive surrounding-agent responses or intervention-correct world dynamics.

---

# Nine-anchor mechanism map

```text
LAW
= action-aware future-latent auxiliary shaping
→ no future online

Drive-JEPA
= masked predictive pretraining → encoder transfer
→ no predictor online

Metis
= action-conditioned future-video co-training
→ world-loss-shaped action expert
→ no future online

DynFlowDrive
= candidate-conditioned flow consequence teacher
→ world-derived score/mode supervision
→ no future online

Epona
= shared history latent → trajectory + visual generative branches
→ visual future optional online

WorldDrive
= heavy future teacher → distilled lightweight future surrogate
→ future summary online

World4Drive
= candidate/intention endpoint future → factual-mode selector
→ future online

WoTE
= candidate recurrent future BEV → explicit utility
→ future online

SeerDrive
= future BEV ↔ planner hidden-feature co-refinement
→ future online
```

---

# Stable controls retained / strengthened

```text
rectified-flow time != physical time
continuous latent transport != continuous physical dynamics
smooth dz/ds != smooth dz/dτ
solver-step depth != future-horizon depth
world-derived score supervision != online world evaluation
training-time consequence model may disappear entirely at deployment
candidate-conditioned future != counterfactual truth
foundation latent gain != flow-dynamics gain
selection-teacher gain != consequence-model gain
prediction fidelity != planning evidence
NAVSIM non-reactive != reactive closed loop
matched controls > headline SOTA
```

---

# Phase C.5 coverage queue

```text
WorldDrive      COMPLETE
World4Drive     COMPLETE
SeerDrive       COMPLETE
Drive-JEPA      COMPLETE
Metis           COMPLETE
DynFlowDrive    COMPLETE
Discrete-WAM    NEXT
GraphWorld      PENDING
```

## Immediate next task

See `state/NEXT_TASK.md`.

Deep-read **Discrete-WAM** next, focusing on what `unified discrete world-policy learning` means at the token, parameter, loss, autoregressive process and deployment levels.

## Still forbidden

```text
no research-gap declaration
no method design
no broad VLA expansion
no forced risk-field insertion
no novelty conclusion from missing ontology cells
```

GitHub remains the Research Knowledge Authority; official papers/repos remain primary evidence for decision-critical claims.
