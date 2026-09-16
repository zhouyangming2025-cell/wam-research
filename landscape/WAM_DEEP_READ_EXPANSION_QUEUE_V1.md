# WAM Deep-Read Expansion Queue V1

Last updated: 2026-09-16

Status: **ACTIVE — LITERATURE EXPANSION BEFORE RESEARCH-DIRECTION CONVERGENCE**

## Binding rule

```text
16 normalized anchors
= stronger coordinate system
!= mature field understanding
!= authorization to promote research direction
```

Paper selection remains coverage-driven, not hypothesis-driven.

Current normalized count:

```text
16 papers
```

Latest completed expansion anchors:

```text
P0009 DriveLaW     — COMPLETE
P0012 DA-WAM       — COMPLETE
P0002 SafeDrive    — COMPLETE
P0005 RiskWorld    — COMPLETE
P0007 DriveReward  — COMPLETE
```

Stable-ID integrity rule:

```text
existing corpus IDs are immutable
new not-yet-ingested targets receive IDs after P0065
```

See:

```text
audits/research_synthesis/REPO_STATE_INTEGRITY_AUDIT_20260916.md
```

---

# Working gate before another research-direction discussion

```text
~24–30 deeply normalized papers total
+
multiple independent anchors across major mechanism families
+
new papers mostly map into the coordinate system without repeatedly exposing major blind spots
```

Required diversity:

```text
planning-centric online WAM interfaces
world→policy latent interfaces
candidate-specific future/scoring
explicit safety/risk/value reasoning
reactive behavior simulation / world simulation
evaluation-regime controls
WAM+VLA boundary methods
alternative world representations
training-only vs deployment-time world knowledge
```

---

# Wave C.6 — Core planning-centric WAM expansion — CLOSED

## P0009 DriveLaW — COMPLETE

```text
history → early Video-DiT hidden states → Action-DiT → direct trajectory
```

## P0012 DA-WAM — COMPLETE

```text
32 ego candidates → candidate-specific 0.5s future latents → explicit factor/utility scorer → argmax
```

Direct future truth exists only for the expert-matched branch; all branches receive value/ranking supervision.

## P0002 SafeDrive — COMPLETE

```text
ego candidate → sparse ego-agent world → fine-grained agent×time safety → trajectory selection
```

Candidate-specific safety consequence labels exist; candidate-specific reactive agent futures do not.

## P0005 RiskWorld — COMPLETE

```text
observed history
→ object-centric relation-aware current state
→ RSSM-style 60-step / 3s physical future rollout
→ future relative position / distance / temporal-risk sequence
→ object risk source
```

Boundary:

```text
explicit risk prediction             YES
future physical rollout              YES
ego action-candidate conditioning     NO
online planning consumption           NO
reactive intervention truth           NO
```

## P0007 DriveReward — COMPLETE

Canonical subtype:

```text
VLM-BASED CANDIDATE VALUE / REWARD MODEL
```

Mechanism:

```text
visual/current context + trajectory
→ learned semantic factorized reward/value
→ RL reward teacher OR test-time candidate scorer
```

Critical boundary:

```text
candidate-specific value              YES
explicit predicted future world       NO
alternative-action world truth        NO
reactive intervention truth           NO
```

Strongest planning evidence is the training-time RL reward interface; the reported AdaThinkDrive online scoring gain is only +0.2 PDMS versus +2.7 Best-of-N oracle headroom.

C.6 synthesis consequence:

```text
future/world modeling
and
value/reward modeling
must remain separate causal axes
```

---

# Wave C.7 — Simulation / reactivity / evaluation controls — ACTIVE

Existing corpus anchors:

```text
P0013 BridgeSim       — RAW_MD_READY / DEEP READ PENDING
P0014 ReactSimBench   — RAW_MD_READY / DEEP READ PENDING
P0015 CausalDrive     — RAW_MD_READY / DEEP READ PENDING
```

New targets requiring ingestion:

```text
P0066 SAFE-SIM       — RESERVED / INGEST NEXT
P0067 ProSim         — RESERVED / INGEST PENDING
```

Important correction from the 2026-09-15 queue:

```text
P0003 is GraphAD, not SAFE-SIM
P0004 is BeTop, not ProSim
```

Purpose:

```text
reactive environment modeling
behavior simulation
log-replay vs endogenous reaction
generative simulator vs planning WAM
open-loop vs non-reactive pseudo-sim vs reactive closed loop
simulation/evaluation truth
```

Recommended order:

```text
P0066 SAFE-SIM
→ P0067 ProSim
→ P0013 BridgeSim
→ P0014 ReactSimBench
→ P0015 CausalDrive
```

This ordering moves from controllable closed-loop traffic generation toward increasingly explicit learned reactivity / behavioral-validity questions.

---

# Wave C.8 — WAM+VLA / reasoning boundary controls

Targets not yet in raw corpus; IDs reserved sequentially:

```text
P0068 AutoVLA       — RESERVED / INGEST PENDING
P0069 ReCogDrive    — RESERVED / INGEST PENDING
P0070 LINGO-2       — RESERVED / INGEST PENDING
P0071 DriveGPT4     — RESERVED / INGEST PENDING
```

Important correction from the 2026-09-15 queue:

```text
P0006 = GenDrive
P0010 = TOAD
P0011 = SensitivityShaping
those IDs must not be reused
```

Purpose:

```text
separate world-model benefit from language/reasoning prior
separate generative planning from VLM/VLA semantic reasoning
understand reward/post-training/reasoning interfaces
avoid calling every future-aware VLA a world model
```

---

# Reading protocol

```text
paper-deep-reader reconstruction
→ source/version gate
→ architecture/training/inference graph
→ strongest matched ablations
→ immediate cross-paper comparison
→ force-fill Ontology V1.3
→ residue/back-projection test
```

Every paper must answer:

```text
what exactly the module does
what prior anchors do the same scientific job
whether supervision/deployment role is truly comparable
strongest matched evidence
what the paper does NOT prove
```

---

# Parked work

All research-tension / candidate-problem artifacts remain historical/provisional until the expanded corpus is reconsolidated.

```text
research-direction convergence = PAUSED
problem promotion              = PAUSED
method design                  = FORBIDDEN
```

---

# Next task

```text
P0066 SAFE-SIM
```

Required pre-read gate:

```text
register stable ID
verify canonical paper/version
verify attributable official source/code
create raw readable source layer
then deep-read
```
