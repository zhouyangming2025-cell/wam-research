# CURRENT_STATE

Last updated: **2026-09-15 — RESEARCH-DIRECTION CONVERGENCE PAUSED; BROAD WAM DEEP-READ EXPANSION ACTIVE; SAFEDRIVE COMPLETE**

## Research north star

```text
WAM / World Model + one-stage End-to-End + Planning-centric autonomous driving
```

Core WAM remains primary. WAM+VLA is secondary/control. Risk/safety/reward/simulation papers are included when they expose mechanisms needed to understand planning-centric WAM rather than because they fit a preferred future direction.

---

# Methodology in force

```text
FIELD UNDERSTANDING FIRST
→ broad core-WAM coverage
→ comparative anchor deep reads
→ dimension-first normalization
→ periodic consolidation
→ evidence / source QA
→ ONLY AFTER sufficient field maturity: adversarial problem discovery
→ falsification
→ method design
```

Binding correction after the first 11 anchors:

```text
11 deep anchors
= preliminary scientific coordinate system
!= mature field coverage
!= authorization to promote research directions
```

Therefore:

```text
Phase D research-direction convergence      PAUSED
candidate-problem promotion                 PAUSED
method design                               FORBIDDEN
broad literature expansion                  ACTIVE
```

Previously created tension/candidate-problem artifacts remain parked historical observations and MUST NOT determine paper selection during this phase.

---

# Normalized anchors — expansion now at 14

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
P0009 DriveLaW      COMPLETE v2 + official-source audit
P0012 DA-WAM        COMPLETE v2 + official-repo-status audit
P0002 SafeDrive     COMPLETE v2 + NAVSIM source audit
```

These anchors are a growing comparison set, not the field boundary.

Canonical ontology:

```text
landscape/WAM_DIMENSION_ONTOLOGY_V1.md
landscape/WAM_DIMENSION_ONTOLOGY_V1_1_AMENDMENT.md
landscape/WAM_DIMENSION_ONTOLOGY_V1_2_AMENDMENT.md
landscape/WAM_DIMENSION_ONTOLOGY_V1_3_AMENDMENT.md
```

Ontology V1.3 remains active as a working coordinate system.

No V1.4 was authorized by DriveLaW, DA-WAM or SafeDrive.

Residue watchlist:

```text
GENERATIVE-STATE TAP LOCATION / SOLVER-DEPTH OF POLICY CONDITION
SAFETY-LOCALIZATION GRANULARITY
```

Both remain unpromoted until independent anchors show explanatory value beyond existing dimensions.

---

# DriveLaW stable normalized result

Canonical files:

```text
papers/deep_analysis/P0009_DRIVELAW_DEEP_ANALYSIS_V2.md
audits/literature/PHASE_C6_DRIVELAW_AUDIT.md
landscape/P0009_DRIVELAW_ONTOLOGY_PROJECTION.md
landscape/WAM_COMPARISON_MATRIX_V1_3_DRIVELAW_EXTENSION.md
```

Subtype:

```text
ONLINE GENERATIVE-LATENT DIRECT-POLICY WAM
```

Core deployment graph:

```text
history frames
→ FIRST Video-DiT denoising pass
→ cached blockwise Video-DiT hidden states
→ Action-DiT cross-attention / flow refinement
→ trajectory

full future-video rollout / RGB decode NOT REQUIRED
```

Key correction:

```text
forward:  WORLD/VIDEO HIDDEN → ACTION
backward: ACTION LOSS → VIDEO DIT in action_full stage
```

Planning-optimal video representation occurs early in denoising; more complete generation is not monotonically better for planning.

---

# DA-WAM stable normalized result

Canonical files:

```text
papers/deep_analysis/P0012_DAWAM_DEEP_ANALYSIS_V2.md
audits/literature/PHASE_C6_DAWAM_AUDIT.md
landscape/P0012_DAWAM_ONTOLOGY_PROJECTION.md
landscape/WAM_COMPARISON_MATRIX_V1_3_DAWAM_EXTENSION.md
```

Subtype:

```text
ONLINE CANDIDATE-SPECIFIC FUTURE-LATENT UTILITY SCORING WAM
```

Core deployment:

```text
2 front-camera frames
→ V-JEPA 2.1 online encoder + LoRA
→ 32 trajectory candidates
→ 32 short-horizon future latents
→ NC/DAC/EP/TTC/Comfort + utility scorer
→ argmax
```

Binding supervision boundary:

```text
candidate-specific future outputs                         YES
candidate-specific direct future truths                  NO
expert-matched future-latent truth                       YES
other branches direct future-latent truth                NO
all branches factor/value/ranking supervision            YES
```

Matched control:

```text
No Future 93.31
Shared Global Future 92.81
Current Latent 93.25
Action-Conditioned Future 93.46
+ Hard Negatives 93.68 PDMS
```

Official implementation remains SOURCE-BLOCKED (`LeapWM/da-wam` placeholder README only in audited state).

---

# SafeDrive stable normalized result

Canonical files:

```text
papers/deep_analysis/P0002_SAFEDRIVE_DEEP_ANALYSIS_V2.md
audits/literature/PHASE_C6_SAFEDRIVE_AUDIT.md
landscape/P0002_SAFEDRIVE_ONTOLOGY_PROJECTION.md
landscape/WAM_COMPARISON_MATRIX_V1_3_SAFEDRIVE_EXTENSION.md
```

Official source:

```text
SPA-junghokim/SafeDrive@ea7791d6c2ebdeedfb6ed514f080cdfa1675b76f
```

Subtype:

```text
ONLINE TRAJECTORY-CONDITIONED SPARSE-WORLD SAFETY EVALUATOR
```

Core deployment graph:

```text
camera + LiDAR + history
→ ProposalNet: BEV / objects / 256 anchors / coarse safety
→ candidate pruning
→ one sparse ego-agent world per surviving ego candidate
→ SWNet interaction + future-motion refinement
→ FRNet
   scene safety
   + PwNC(agent × future time)
   + TwDAC(future time)
→ weighted learned safety score
→ select trajectory
```

Critical source-verified supervision decomposition:

```text
candidate-specific sparse-world output               YES
candidate-specific PDM safety/value labels           YES
candidate-specific pair-collision / TwDAC labels     YES
candidate-specific alternative-agent future GT       NO
reactive other-agent intervention truth              NO in audited NAVSIM path
```

The released loss code reuses the same logged surrounding-agent future targets across ego-anchor/world branches while PDM safety targets are computed separately for each ego candidate.

Binding interpretation:

```text
candidate-specific safety consequence supervision
!=
candidate-specific reactive world truth
```

Strongest matched attribution:

```text
BEV + scene-level safety       ~90.9 PDMS
Sparse + scene-level safety    ~90.9
Sparse + fine-grained safety    91.6

scene baseline                 ~90.9
+ PwNC                          91.5
+ TwDAC                         91.4
+ both                          91.6
```

Thus the best-supported contribution is:

```text
structured sparse interaction representation
×
fine-grained safety localization
```

not sparse representation alone.

Source status:

```text
NAVSIM core implementation   SOURCE-COMPLETE
Bench2Drive result           PAPER-VERIFIED
Bench2Drive code path        SOURCE-PARTIAL / NOT IDENTIFIED
```

---

# Active expansion plan

Canonical queue:

```text
landscape/WAM_DEEP_READ_EXPANSION_QUEUE_V1.md
```

Working maturity gate before another research-direction discussion:

```text
~24–30 deeply normalized papers total
+
multiple independent anchors across major mechanism families
+
new papers mostly map into the coordinate system without repeatedly exposing major blind spots
```

Diversity/saturation matter more than raw count.

## Wave C.6 — core planning-centric WAM expansion

```text
P0009 DriveLaW      COMPLETE
P0012 DA-WAM        COMPLETE
P0002 SafeDrive     COMPLETE
P0005 RiskWorld     NEXT
P0007 DriveReward
```

## Wave C.7 — simulation / reactivity / evaluation controls

```text
P0003 Safe-Sim
P0004 PROSIM
P0013 BridgeSim
P0014 ReactSimBench
P0015 CausalDrive
```

## Wave C.8 — WAM+VLA / reasoning boundary controls

```text
P0008 AutoVLA
P0011 ReCogDrive
P0010 LINGO-2
P0006 DriveGPT4
```

Queue order may change only for source/evidence dependencies or scope correction, not because a paper supports a preferred hypothesis.

---

# Next coverage target — RiskWorld

```text
object-centric latent rollout
→ future ego-object relation
→ object-level risk identification
```

RiskWorld is a boundary anchor: read it to understand explicit predicted risk state, not to force it into the planning-core family if the planning interface is absent.

Immediate comparison targets:

```text
RiskWorld vs SafeDrive
RiskWorld vs GraphWorld
RiskWorld vs WoTE
RiskWorld vs LAW / World4Drive
```

Primary distinction to lock:

```text
risk as predicted world state
vs
safety/value as candidate evaluator
vs
safety only as benchmark outcome
```

---

# Parked provisional synthesis

```text
landscape/WAM_RESEARCH_TENSIONS_V1.md
landscape/WAM_RESEARCH_TENSIONS_V2_VALIDATED.md
audits/research_synthesis/WAM_TIER1_TENSION_ADVERSARIAL_VALIDATION_V1.md
landscape/WAM_CANDIDATE_PROBLEMS_V1.md
landscape/WAM_CANDIDATE_PROBLEM_OVERLAP_MATRIX_V1.md
landscape/WAM_CANDIDATE_PROBLEM_RESEARCHABILITY_V1.md
```

These are historical/provisional only during expansion.

---

# Source completeness

Authority:

```text
audits/research_synthesis/CORE_ANCHOR_SOURCE_COMPLETENESS_AUDIT.md
```

Source certainty and scientific coverage remain separate axes.
