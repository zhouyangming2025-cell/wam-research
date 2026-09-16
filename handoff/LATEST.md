# LATEST — Handoff

Session: **2026-09-16 — DriveReward normalized; 16 anchors; repository state/ID integrity repaired; Wave C.7 SAFE-SIM next.**

## New-session fast path

```text
1. START_HERE.md
2. state/CURRENT_STATE.md
3. state/NEXT_TASK.md
4. landscape/WAM_DEEP_READ_EXPANSION_QUEUE_V1.md
5. audits/research_synthesis/REPO_STATE_INTEGRITY_AUDIT_20260916.md
```

Do not default to old Phase-D, P2-R/P3, or pre-expansion handoffs. Do not reload old chats by default.

---

## Research identity

```text
World Model + End-to-End + Planning-centric autonomous driving
```

Risk/safety/reward/simulation/VLA are comparison/control families when they illuminate planning-centric WAM; none is a required research destination.

Active methodology:

```text
UNDERSTAND FIELD FIRST
→ broad comparative deep reads
→ dimension-first normalization
→ cross-family synthesis
→ ONLY AFTER maturity gate: adversarial problem discovery
→ falsification
→ method design
```

Current guardrails:

```text
research-direction convergence   PAUSED
candidate-problem promotion      PAUSED
method design                    FORBIDDEN
literature expansion             ACTIVE
```

---

## Current normalized state

```text
16 anchors complete
Ontology V1.3 active
Wave C.6 closed
Wave C.7 active
```

Latest C.6 bundle:

```text
P0009 DriveLaW
P0012 DA-WAM
P0002 SafeDrive
P0005 RiskWorld
P0007 DriveReward
```

DriveReward canonical artifacts:

```text
papers/deep_analysis/P0007_DRIVEREWARD_DEEP_ANALYSIS_V2.md
audits/literature/PHASE_C6_DRIVEREWARD_AUDIT.md
landscape/P0007_DRIVEREWARD_ONTOLOGY_PROJECTION.md
landscape/WAM_COMPARISON_MATRIX_V1_3_DRIVEREWARD_EXTENSION.md
```

---

## Latest scientific correction

DriveReward provides the current clean control for:

```text
candidate-specific learned value/reward
!=
explicit candidate-specific future-world prediction
```

Mechanism:

```text
visual/current-or-short-history context
+ route / ego state
+ candidate trajectory
→ VLM semantic evaluator
→ factorized reward + reasoning
→ RL reward teacher OR test-time scorer
```

Evidence balance:

```text
training-time RL reward use       strong positive evidence
online test-time reranking        positive but small reported gain
```

AdaThinkDrive:

```text
Original      90.3 PDMS
Best-of-4     93.0
DriveReward   90.5
```

Therefore planning gains must be decomposed across:

```text
representation
candidate support
future consequence prediction
risk/safety prediction
value/reward modeling
post-training
online inference-time selection
```

rather than called one generic `world-model gain`.

---

## Stable-ID integrity repair

The 2026-09-15 expansion queue had accidentally reused occupied paper IDs.

Existing identities are immutable:

```text
P0003 GraphAD
P0004 BeTop
P0006 GenDrive
P0010 TOAD
P0011 SensitivityShaping
```

Corrected new reservations:

```text
P0066 SAFE-SIM
P0067 ProSim
P0068 AutoVLA
P0069 ReCogDrive
P0070 LINGO-2
P0071 DriveGPT4
```

BridgeSim / ReactSimBench / CausalDrive remain correctly registered as:

```text
P0013 BridgeSim
P0014 ReactSimBench
P0015 CausalDrive
```

Audit:

```text
audits/research_synthesis/REPO_STATE_INTEGRITY_AUDIT_20260916.md
```

Reserved IDs are not yet ingested; register them in the corpus manifest when primary sources are ingested.

---

## Current Wave C.7 queue

```text
P0066 SAFE-SIM       RESERVED / INGEST NEXT
P0067 ProSim         RESERVED / INGEST PENDING
P0013 BridgeSim      RAW_MD_READY / DEEP READ PENDING
P0014 ReactSimBench  RAW_MD_READY / DEEP READ PENDING
P0015 CausalDrive    RAW_MD_READY / DEEP READ PENDING
```

Wave C.7 purpose:

```text
reactive environment modeling
behavior simulation
log replay vs endogenous reaction
generative simulator vs planning WAM
simulation / intervention truth
evaluation-regime semantics
```

Feedback coordinates:

```text
F_e = ego-state / dynamics feedback
F_s = sensor / viewpoint feedback
F_a = surrounding-agent state feedback
F_b = surrounding-agent behavioral-response feedback
```

Binding warning:

```text
closed-loop generation
!=
causally identified counterfactual behavioral truth
```

---

## Immediate next task

Read `state/NEXT_TASK.md`.

Execute:

```text
P0066 SAFE-SIM source gate
→ register / ingest readable primary source
→ verify official code attribution
→ normalized deep read
→ full Ontology V1.3 projection
→ compare against ProSim / RiskWorld / SafeDrive / WoTE / DA-WAM
```

Target paper:

```text
SAFE-SIM: Safety-Critical Closed-Loop Traffic Simulation with Diffusion-Controllable Adversaries
ECCV 2024
arXiv:2401.00391
```

Do not reopen research-direction convergence after SAFE-SIM. Continue Wave C.7 unless the ontology exposes a genuinely irreducible residue requiring consolidation.

---

## Evidence discipline

Always separate:

```text
AUTHOR CLAIM
DIRECT EXPERIMENTAL EVIDENCE
OUR INFERENCE
```

For reactive/simulator papers ask:

```text
what closes the loop?
which feedback carrier is updated?
which agents react to ego?
what is generated once vs regenerated?
what truth supervises behavior under changed ego action?
what proves realism?
what proves planning relevance?
what remains only conditional generation rather than intervention truth?
```

---

The repo, not conversation memory, is the canonical research authority.
