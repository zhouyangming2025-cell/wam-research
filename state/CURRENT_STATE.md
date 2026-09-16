# CURRENT_STATE

Last updated: **2026-09-16 — DRIVEREWARD COMPLETE; 16 NORMALIZED ANCHORS; WAVE C.7 ACTIVE; STATE/ID INTEGRITY REPAIRED**

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

Binding status:

```text
research-direction convergence      PAUSED
candidate-problem promotion         PAUSED
method design                       FORBIDDEN
broad literature expansion          ACTIVE
```

The working maturity gate remains:

```text
~24–30 deeply normalized papers
+
multiple independent anchors across major mechanism families
+
ontology saturation / diminishing new residues
```

Diversity and saturation matter more than raw count.

---

# Canonical normalized anchors — 16

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
P0007 DriveReward   COMPLETE v2 + reward/value boundary audit
```

These anchors are a growing comparison set, not the field boundary.

Canonical ontology remains:

```text
landscape/WAM_DIMENSION_ONTOLOGY_V1.md
landscape/WAM_DIMENSION_ONTOLOGY_V1_1_AMENDMENT.md
landscape/WAM_DIMENSION_ONTOLOGY_V1_2_AMENDMENT.md
landscape/WAM_DIMENSION_ONTOLOGY_V1_3_AMENDMENT.md
```

Current ontology:

```text
V1.3 ACTIVE
NO V1.4 authorized by DriveLaW / DA-WAM / SafeDrive / RiskWorld / DriveReward
```

Residue watchlist:

```text
GENERATIVE-STATE TAP LOCATION / SOLVER-DEPTH OF POLICY CONDITION
SAFETY-LOCALIZATION GRANULARITY
DISCRETE REPRESENTATION ALIGNMENT TOPOLOGY
```

---

# Latest scientific correction — P0007 DriveReward

Canonical files:

```text
papers/deep_analysis/P0007_DRIVEREWARD_DEEP_ANALYSIS_V2.md
audits/literature/PHASE_C6_DRIVEREWARD_AUDIT.md
landscape/P0007_DRIVEREWARD_ONTOLOGY_PROJECTION.md
landscape/WAM_COMPARISON_MATRIX_V1_3_DRIVEREWARD_EXTENSION.md
```

Canonical subtype:

```text
VLM-BASED CANDIDATE VALUE / REWARD MODEL
```

Core mechanism:

```text
visual/current-or-short-history context
+ navigation / ego state
+ candidate trajectory
→ InternVL3-1B semantic evaluator
+ VGGT geometry grounding during training
→ reasoning + factorized reward
→ RL reward teacher OR test-time candidate scorer
```

Critical boundary:

```text
candidate-specific value/reward             YES
explicit predicted future world             NO
candidate-specific future-world truth       NO
reactive intervention truth                 NO
```

Planning evidence decomposition:

```text
training-time RL reward interface   STRONGER EVIDENCE
online test-time reranking          POSITIVE BUT SMALL REPORTED GAIN
```

AdaThinkDrive selection result:

```text
Original       90.3 PDMS
Best-of-4      93.0
DriveReward    90.5
```

Thus DriveReward strengthens a project-wide causal distinction:

```text
future/world modeling
!=
value/reward modeling
```

A planner can absorb useful consequence/value information without deploying an explicit future-world state.

---

# Wave C.6 status

```text
P0009 DriveLaW      COMPLETE
P0012 DA-WAM        COMPLETE
P0002 SafeDrive     COMPLETE
P0005 RiskWorld     COMPLETE
P0007 DriveReward   COMPLETE
```

Wave C.6 is now **CLOSED**.

Its strongest collective lesson is not one architecture winner, but a separation of roles:

```text
representation shaping
future consequence prediction
explicit safety/risk prediction
direct value/reward learning
candidate scoring
training-time teacher knowledge
online deployed world knowledge
```

These must remain independent causal axes.

---

# Wave C.7 — ACTIVE

Purpose:

```text
simulation / reactivity / evaluation controls
```

Correct queue after stable-ID audit:

```text
P0066 SAFE-SIM       RESERVED / INGEST NEXT
P0067 ProSim         RESERVED / INGEST PENDING
P0013 BridgeSim      RAW_MD_READY / DEEP READ PENDING
P0014 ReactSimBench  RAW_MD_READY / DEEP READ PENDING
P0015 CausalDrive    RAW_MD_READY / DEEP READ PENDING
```

Critical questions:

```text
what actually closes the loop?
which feedback channels exist?
which agents respond endogenously to ego intervention?
what is replayed vs generated vs regenerated?
what counts as reactive behavioral evidence?
how does simulator realism relate to planner-quality evidence?
```

Project feedback coordinate system remains:

```text
F_e = ego-state / dynamics feedback
F_s = sensor / viewpoint feedback
F_a = surrounding-agent state feedback
F_b = surrounding-agent behavioral-response feedback
```

---

# Stable-ID integrity correction

Audit:

```text
audits/research_synthesis/REPO_STATE_INTEGRITY_AUDIT_20260916.md
```

Existing IDs are immutable. The old expansion queue incorrectly attempted to reuse occupied IDs.

Verified existing identities include:

```text
P0003 GraphAD
P0004 BeTop
P0006 GenDrive
P0010 TOAD
P0011 SensitivityShaping
```

Reserved new targets:

```text
P0066 SAFE-SIM
P0067 ProSim
P0068 AutoVLA
P0069 ReCogDrive
P0070 LINGO-2
P0071 DriveGPT4
```

Reserved means **not yet ingested**. Registration into `CORPUS_MANIFEST.csv` must occur with source ingestion.

---

# Current source / evidence priority

For every next paper:

```text
canonical paper/version
→ attributable official repo/source if available
→ readable raw primary text
→ source/code audit where mechanism-critical
→ normalized deep read
→ ontology projection
→ comparison extension
```

Never infer source implementation details from paper prose when code is unavailable.

---

# Parked provisional synthesis

These remain historical/provisional and must not determine paper selection during expansion:

```text
landscape/WAM_RESEARCH_TENSIONS_V1.md
landscape/WAM_RESEARCH_TENSIONS_V2_VALIDATED.md
audits/research_synthesis/WAM_TIER1_TENSION_ADVERSARIAL_VALIDATION_V1.md
landscape/WAM_CANDIDATE_PROBLEMS_V1.md
landscape/WAM_CANDIDATE_PROBLEM_OVERLAP_MATRIX_V1.md
landscape/WAM_CANDIDATE_PROBLEM_RESEARCHABILITY_V1.md
```

---

# Canonical next task

Read:

```text
state/NEXT_TASK.md
```

Current target:

```text
P0066 SAFE-SIM
```

First perform source/ingestion gate, then normalized deep read. Do not reopen Phase D.
