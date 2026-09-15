# CURRENT_STATE

Last updated: **2026-09-15 — RESEARCH-DIRECTION CONVERGENCE PAUSED; BROAD WAM DEEP-READ EXPANSION ACTIVE; RISKWORLD COMPLETE**

## Research north star

```text
WAM / World Model + one-stage End-to-End + Planning-centric autonomous driving
```

Core WAM remains primary. Risk/safety/reward/simulation/VLA papers are included when they expose mechanisms required to understand planning-centric WAM; they are not selected to support a preferred future method.

---

# Methodology in force

```text
FIELD UNDERSTANDING FIRST
→ broad core-WAM coverage
→ comparative anchor deep reads
→ dimension-first normalization
→ periodic consolidation
→ evidence/source QA
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
research-direction convergence      PAUSED
candidate-problem promotion         PAUSED
method design                       FORBIDDEN
broad literature expansion          ACTIVE
```

Previously created tension/candidate-problem artifacts remain parked historical observations and MUST NOT determine paper selection during this phase.

---

# Normalized anchors — expansion now at 15

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
P0005 RiskWorld     COMPLETE v2 + paper/source-status audit
```

These anchors are a growing comparison set, not the field boundary.

Canonical ontology remains:

```text
landscape/WAM_DIMENSION_ONTOLOGY_V1.md
landscape/WAM_DIMENSION_ONTOLOGY_V1_1_AMENDMENT.md
landscape/WAM_DIMENSION_ONTOLOGY_V1_2_AMENDMENT.md
landscape/WAM_DIMENSION_ONTOLOGY_V1_3_AMENDMENT.md
```

Ontology V1.3 remains active. No V1.4 is authorized by DriveLaW, DA-WAM, SafeDrive or RiskWorld.

Residue watchlist:

```text
GENERATIVE-STATE TAP LOCATION / SOLVER-DEPTH OF POLICY CONDITION
SAFETY-LOCALIZATION GRANULARITY
```

RiskWorld did not add an irreducible residue; it strongly exercised existing risk/planning/counterfactual axes.

---

# Latest expansion anchors

## P0009 DriveLaW

Subtype:

```text
ONLINE GENERATIVE-LATENT DIRECT-POLICY WAM
```

Core result:

```text
history frames
→ first Video-DiT denoising pass
→ cached blockwise generative hidden states
→ Action-DiT cross-attention / flow refinement
→ trajectory

full future-video rollout / RGB decode NOT REQUIRED
```

Key correction:

```text
forward:  WORLD/VIDEO HIDDEN → ACTION
backward: ACTION LOSS → VIDEO DIT in action_full stage
```

## P0012 DA-WAM

Subtype:

```text
ONLINE CANDIDATE-SPECIFIC FUTURE-LATENT UTILITY SCORING WAM
```

Critical supervision boundary:

```text
candidate-specific future output              YES
candidate-specific direct future truth        NO except expert-matched branch
all-branch factor/value/ranking supervision   YES
reactive alternative-world truth              NO / NOT ESTABLISHED
```

Strong matched control:

```text
No Future 93.31
Action-Conditioned Future 93.46
+ Hard Negatives 93.68 PDMS
```

Official implementation remains SOURCE-BLOCKED.

## P0002 SafeDrive

Subtype:

```text
ONLINE TRAJECTORY-CONDITIONED SPARSE-WORLD SAFETY EVALUATOR
```

Core supervision decomposition:

```text
candidate-specific sparse world               YES
candidate-specific PDM safety/value labels    YES
candidate-specific pair collision/TwDAC       YES
candidate-specific reactive-agent future GT   NO
```

Binding interpretation:

```text
candidate-specific safety consequence supervision
!= candidate-specific reactive world truth
```

Source status:

```text
NAVSIM core      SOURCE-COMPLETE
Bench2Drive      PAPER-VERIFIED / SOURCE-PARTIAL
```

## P0005 RiskWorld

Canonical files:

```text
papers/deep_analysis/P0005_RISKWORLD_DEEP_ANALYSIS_V2.md
audits/literature/PHASE_C6_RISKWORLD_AUDIT.md
landscape/P0005_RISKWORLD_ONTOLOGY_PROJECTION.md
landscape/WAM_COMPARISON_MATRIX_V1_3_RISKWORLD_EXTENSION.md
```

Subtype:

```text
OBJECT-CENTRIC FACTUAL-RELATION ROLLOUT RISK WORLD MODEL
```

Core inference graph:

```text
16-frame front RGB + object tracks + ego motion
→ frozen V-JEPA2 global/object features
→ structured object/ego state + relation attention
→ one relation-aware latent token per object
→ RSSM-style 60-step / 3 s physical future rollout
→ future relative position / distance / temporal-risk curve
→ pooled object-risk probability
→ risk-source identification
```

Critical boundary:

```text
explicit learned risk state                  YES
recurrent physical future rollout            YES
hypothetical ego-action conditioning         NO
online world→planner consumption             NO
trajectory selection                         NO
reactive intervention truth                  NO
```

Supervision:

```text
logged future ego/object tracks
→ future relative geometry targets

RiskBench risk-object/event annotations
→ final object-risk label + shaped temporal-risk curve
```

Strongest matched future-model evidence:

```text
w/o future rollout      60.2 F1 / 5.9 FA
w/o future supervision  61.6 / 4.4
Deterministic GRU       62.0 / 6.0
RiskWorld               63.0 / 2.1
```

Representation effects are larger (`w/o world features` = 50.6 F1), but those bundle the imported V-JEPA2 prior and must not be narrated as pure RSSM dynamics gain.

Planning-aware LBC masking shows that selected objects can preserve planning-relevant information, but the paper explicitly does **not** demonstrate an integrated RiskWorld→planner performance gain.

Source status:

```text
arXiv:2608.21414v1                  PAPER-VERIFIED
official implementation             NOT IDENTIFIED
KevinWjk/RiskWorld                   FALSE POSITIVE (Alpamayo 1.5 README)
```

Therefore:

```text
P0005 RiskWorld = PAPER-COMPLETE / SOURCE-BLOCKED-MONITOR
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
P0005 RiskWorld     COMPLETE
P0007 DriveReward   NEXT
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

# Next coverage target — DriveReward

DriveReward is a value/reward control anchor:

```text
visual/current context + trajectory
→ learned semantic reward/value
→ RL / trajectory selection or reranking
```

It is needed to distinguish:

```text
future-world modeling
vs
trajectory valuation / reward learning
```

Immediate comparisons:

```text
DriveReward vs WoTE
DriveReward vs DA-WAM
DriveReward vs SafeDrive
DriveReward vs RiskWorld
DriveReward vs Drive-JEPA / WorldDrive
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

These remain historical/provisional only during expansion.

---

# Source completeness

Authority:

```text
audits/research_synthesis/CORE_ANCHOR_SOURCE_COMPLETENESS_AUDIT.md
```

Source certainty and scientific coverage remain separate axes.
