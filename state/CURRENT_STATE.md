# CURRENT_STATE

Last updated: **2026-09-15 — RESEARCH-DIRECTION CONVERGENCE PAUSED; BROAD WAM DEEP-READ EXPANSION ACTIVE**

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

## Correction after the first 11 anchors

The first eleven normalized anchors were sufficient to build a useful preliminary ontology and mechanism map, but **not sufficient to converge on research problems or method directions**.

Binding correction:

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

The previously created tension/candidate-problem artifacts are retained only as **parked provisional observations**. They must not determine paper selection during this phase.

---

# First normalized anchor set — preliminary, not final

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
```

These eleven remain canonical comparison anchors, but they no longer define the boundary of the field.

Canonical ontology remains:

```text
landscape/WAM_DIMENSION_ONTOLOGY_V1.md
landscape/WAM_DIMENSION_ONTOLOGY_V1_1_AMENDMENT.md
landscape/WAM_DIMENSION_ONTOLOGY_V1_2_AMENDMENT.md
landscape/WAM_DIMENSION_ONTOLOGY_V1_3_AMENDMENT.md
```

Ontology V1.3 remains a working coordinate system, not a final taxonomy.

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
multiple independent anchors across the major mechanism families
+
new papers mostly map into the coordinate system without exposing major coverage blind spots
```

The numerical target is a working gate, not a scientific claim. Diversity and saturation matter more than raw count.

## Wave C.6 — core planning-centric WAM expansion

```text
P0009 DriveLaW      NEXT
P0012 DA-WAM
P0002 SafeDrive
P0005 RiskWorld
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

Queue order may change only for evidence/source dependencies or if a paper is found to be out of scope—not because it supports a preferred hypothesis.

---

# Why the next core papers materially extend coverage

## DriveLaW

```text
video generator internal latent
→ directly conditions Action DiT planner
```

This is different from Epona's sibling branches and WorldDrive's teacher/distillation lifecycle.

## DA-WAM

```text
N candidate trajectories
→ N action-conditioned future latents
→ one-to-one future-latent-conditioned scoring
```

This directly pressures candidate-specific consequence / factual-supervision dimensions.

## SafeDrive

```text
trajectory-conditioned sparse world
→ agent/timestep future states
→ explicit fine-grained safety reasoning
```

This provides a missing explicit safety/world/planning anchor.

## RiskWorld

```text
object-centric latent rollout
→ future ego-object relation
→ object-level risk
```

Boundary anchor for explicit risk-state semantics.

## DriveReward

```text
visual context + trajectory
→ learned semantic reward/value
→ RL / trajectory selection
```

Control anchor showing that decision quality can be improved through value/reward modeling without requiring a conventional future-world rollout.

---

# Parked provisional synthesis

The following are retained for history but are not active research-direction authority:

```text
landscape/WAM_RESEARCH_TENSIONS_V1.md
landscape/WAM_RESEARCH_TENSIONS_V2_VALIDATED.md
audits/research_synthesis/WAM_TIER1_TENSION_ADVERSARIAL_VALIDATION_V1.md
landscape/WAM_CANDIDATE_PROBLEMS_V1.md
landscape/WAM_CANDIDATE_PROBLEM_OVERLAP_MATRIX_V1.md
landscape/WAM_CANDIDATE_PROBLEM_RESEARCHABILITY_V1.md
```

No candidate from those files may be called a project research direction until after expanded literature coverage and a second consolidation.

---

# Source completeness

Authority remains:

```text
audits/research_synthesis/CORE_ANCHOR_SOURCE_COMPLETENESS_AUDIT.md
```

Source certainty and scientific coverage are separate axes. New papers should be paper-normalized even when official implementation is not yet available, with source uncertainty stated explicitly.

---

# Immediate next task

Deep-read:

```text
P0009 DriveLaW
```

under the same WAM reading stack, with immediate cross-paper comparison against Epona, WorldDrive, Metis, Discrete-WAM and LAW.

Still forbidden:

```text
NO final research-gap declaration
NO research-direction ranking
NO method architecture proposal
NO forced risk-field insertion
NO paper selection driven by parked candidate problems
```
