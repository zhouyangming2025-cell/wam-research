# CURRENT_STATE

Last updated: **2026-09-15 — Discrete-WAM stress test COMPLETE; Ontology V1.3 RETAINED; GraphWorld NEXT**

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
P0048 LAW           COMPLETE v2
P0045 WoTE          COMPLETE v2
P0001 Epona         COMPLETE v2
P0042 WorldDrive    COMPLETE v2
P0046 World4Drive   COMPLETE v2
P0061 SeerDrive     COMPLETE v2 first pass
P0049 Drive-JEPA    COMPLETE v2 first pass + source audit
P0062 Metis         COMPLETE v2 first pass + paper/repo audit
P0063 DynFlowDrive  COMPLETE v2 first pass + paper/repo audit
P0064 Discrete-WAM  COMPLETE v2 first pass + paper/source-status audit
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
landscape/WAM_COMPARISON_MATRIX_V1_3_DISCRETE_WAM_EXTENSION.md
```

Discrete-WAM artifacts:

```text
papers/deep_analysis/P0064_DISCRETE_WAM_DEEP_ANALYSIS_V2.md
audits/literature/PHASE_C5_DISCRETE_WAM_AUDIT.md
landscape/P0064_DISCRETE_WAM_ONTOLOGY_PROJECTION.md
```

---

# Discrete-WAM stable result

## Source/version boundary

```text
paper: Discrete-WAM: Unified Discrete Vision-Action Token Editing for World-Policy Learning
arXiv:2606.05645v2
v2: 2026-06-09
```

As of 2026-09-15 no official implementation repository attributable to the paper/authors was identified in the audit.

Therefore:

```text
paper architecture / appendix / ablations   PAPER-VERIFIED
exact code implementation                   SOURCE-UNVERIFIED
```

## Canonical mechanism

```text
SHARED-BACKBONE MULTI-TASK DISCRETE WORLD-POLICY PRETRAINING
→ HIERARCHICAL DECISION-CONDITIONED ACTION TOKEN EDITING
→ POLICY-ONLY PLANNING INFERENCE
```

Training/capability graph:

```text
visual VQ tokens            action acceleration tokens
(separate vocabulary)       (separate vocabulary)
          \                  /
           shared decoder-only Transformer
                    ↓
world modeling / policy modeling / interleaved world-policy modeling
```

Primary NAVSIM planning graph:

```text
current context
→ decision token
→ parallel / iterative action-token editing
→ trajectory

future visual-token generation = NOT REQUIRED
```

Thus Discrete-WAM is **not** an online `generate future world → score consequence → choose action` planner.

---

# `Unified` correction

The audited paper does **not** use one literal world/action codebook.

```text
visual vocabulary      ≈ 16,384 VQ entries
action vocabulary      = 60×60 ≈ 3,600 acceleration prototypes
decision vocabulary    ≈ 400 high-level behavior candidates
```

What is shared:

```text
common Transformer hidden interface
shared decoder/backbone parameters
shared/mixed token sequence capability
joint multitask losses/gradients
world-policy generative task
```

What is not shared:

```text
visual/action codebook
visual/action physical semantics
mandatory world-generation path at planning deployment
```

Binding rule:

```text
shared discrete framework != shared codebook
```

---

# World-action coupling

World task:

```text
current/history context + future action tokens
→ future visual tokens
```

World-policy task conceptually interleaves:

```text
A_{t+1}, V_{t+1}, A_{t+2}, V_{t+2}, ...
```

Thus:

```text
same-step action → world           YES
prior world → later action context YES in joint world-policy generation
```

But primary planning inference is:

```text
current context → decision → action tokens
```

so:

```text
training/model jointness
!= deployment online world dependence
```

---

# Counterfactual boundary

The paper perturbs actions and obtains different generated futures / surprise signals.

```text
action-specific generated world output        YES
per-action observed alternative future truth  NO
reactive surrounding-agent truth              NO / NOT ESTABLISHED
external intervention-validity evidence       ABSENT
```

Therefore:

```text
action-conditioned alternative generation
!= intervention-correct counterfactual dynamics
```

Surprise can be a useful model-sensitivity / safety proxy without being ground-truth causal validation.

---

# Strongest evidence decomposition

## World/pretraining control

```text
From scratch   89.8 EPDMS
FT             89.7
LoRA-SFT       90.0
```

Critical qualifier: the LoRA-SFT pretraining row is described as vision-oriented world-policy pretraining with teacher-forced future actions and only vision prediction losses before LoRA policy finetuning.

Therefore this table does **not** cleanly isolate the full joint world+action pretraining objective.

## Decision-modeling control

```text
Base       84.7 EPDMS
Base-D_t   87.2
```

This +2.5 control is a much stronger isolated contributor than the cleanest world-pretraining delta.

## Post-training ladder

```text
SFT       89.1
SFT-D_t   90.0
RL        90.4
```

Final performance is therefore a bundle of:

```text
world/vision-oriented pretraining
+ high-level decision prior
+ action discretization
+ token editing
+ LoRA adaptation
+ RL/post-training
+ shared Transformer capacity
```

Do not report 90.4 as a monolithic world-model gain.

---

# World-generation evidence

Reported short-horizon generation includes approximately:

```text
FID 6.6
FVD 80.0
4 s / 8-frame setting
```

This establishes strong visual-generation capability.

It does **not** establish:

```text
better visual-generation fidelity
→ better planning
```

because no matched monotonic fidelity→EPDMS relation is demonstrated.

---

# Temporal correction

Discrete-WAM contains two separate axes:

```text
physical future index h
→ interleaved A_h / V_h sequence

editing round r
→ discrete-diffusion / token-refinement iteration
```

Binding rule:

```text
more token-edit rounds
!= longer physical future horizon
```

F07:

```text
current/history + action → chronologically unseen future visual tokens
```

F08:

```text
physical future positions are distinct from internal token-edit solver rounds
```

---

# Ontology stress-test result

Discrete-WAM exposes a genuine residue:

```text
shared codebook
vs
separate modality vocabularies embedded in one shared hidden/sequence space
```

But prior core anchors are overwhelmingly continuous-latent, so back-projection would mostly be `NOT APPLICABLE` and currently lacks sufficient cross-paper discriminatory value.

Decision:

```text
Ontology V1.3 RETAINED
NO V1.4 AMENDMENT
```

Residue watchlist:

```text
Discrete representation alignment topology
(shared codebook / disjoint vocabularies / common hidden interface)
```

Re-test after another discrete-token anchor.

World/action generation order does not justify a new axis because it is already represented by:

```text
F04 + E02 + J04 + F08
```

---

# Ten-anchor mechanism map

```text
LAW
future-latent auxiliary shaping
→ no future online

Drive-JEPA
masked predictive pretraining → encoder transfer
→ no predictor online

Metis
action-conditioned future-video co-training
→ world-loss-shaped policy
→ no future online

DynFlowDrive
candidate flow consequence teacher
→ world-derived score supervision
→ no future online

Discrete-WAM
shared discrete world/policy multitask pretraining
→ shared backbone + decision/action token policy
→ no future visual required in primary planning

Epona
joint visual+trajectory generation
→ shared F
→ visual future optional online

WorldDrive
heavy future teacher → distilled lightweight future
→ future online

World4Drive
candidate endpoint future → factual-mode selector
→ future online

WoTE
candidate recurrent future → explicit utility
→ future online

SeerDrive
future BEV ↔ planner hidden state co-refinement
→ future online
```

Key new synthesis:

```text
training-time unification strength
and
deployment-time model-basedness
are orthogonal axes
```

---

# Evaluation regime

```text
NAVSIM v1/v2
= NON-REACTIVE DATA-DRIVEN / PSEUDO-SIMULATION PLANNING
```

Reported 92.2 PDMS / 90.4 EPDMS support strong planning performance under that regime, not reactive surrounding-agent world validity.

---

# Phase C.5 coverage queue

```text
WorldDrive       COMPLETE
World4Drive      COMPLETE
SeerDrive        COMPLETE
Drive-JEPA       COMPLETE
Metis            COMPLETE
DynFlowDrive     COMPLETE
Discrete-WAM     COMPLETE
GraphWorld       NEXT
```

## Immediate next task

See `state/NEXT_TASK.md`.

Deep-read **GraphWorld** next under the same skill stack + Ontology V1.3.

## Still forbidden

```text
no research-gap declaration
no method design
no broad VLA expansion
no forced risk-field insertion
no novelty conclusion from empty ontology cells
```

Phase D remains **PAUSED** until GraphWorld normalization and WAM-only comparability QA are complete.
