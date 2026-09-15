# WAM Deep-Read Expansion Queue V1

Last updated: 2026-09-15

Status: **ACTIVE — LITERATURE EXPANSION BEFORE RESEARCH-DIRECTION CONVERGENCE**

## Why this queue exists

The first 11 normalized anchors established a useful preliminary coordinate system, but they are not sufficient for mature field coverage or research-direction convergence.

Binding correction:

```text
11 deep anchors
= enough to build a preliminary ontology
!= enough to declare mature field understanding
!= enough to promote a research direction
```

Parked candidate-problem/tension artifacts MUST NOT drive paper selection during this phase. Selection is based on coverage diversity and mechanism-family saturation.

Current normalized count:

```text
14 papers
```

Latest completed expansion anchors:

```text
P0009 DriveLaW  — COMPLETE
P0012 DA-WAM    — COMPLETE
P0002 SafeDrive — COMPLETE
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

The count is a working gate, not a magic threshold. Diversity and saturation matter more than raw count.

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

No final gap declaration or method design before the next consolidation gate.

---

# Wave C.6 — Core planning-centric WAM expansion

## 1. P0009 DriveLaW — COMPLETE

```text
ONLINE GENERATIVE-LATENT DIRECT-POLICY WAM
history → first Video-DiT pass → cached block states → Action-DiT → trajectory
```

Key coordinate additions:

```text
forward world→action can coexist with backward action-loss→world gradient;
full future-video rollout not required for online world use;
early tapped generative states can be more planning-relevant than later denoised states.
```

## 2. P0012 DA-WAM — COMPLETE

```text
ONLINE CANDIDATE-SPECIFIC FUTURE-LATENT UTILITY SCORING WAM
32 candidates → 32 short future latents → factorized utility → argmax
```

Critical supervision boundary:

```text
candidate-specific outputs                         YES
candidate-specific direct future truth             NO except expert-matched branch
all-branch factor/value/rank labels                YES
reactive alternative-world truth                   NO / NOT ESTABLISHED
```

## 3. P0002 SafeDrive — COMPLETE

```text
ONLINE TRAJECTORY-CONDITIONED SPARSE-WORLD SAFETY EVALUATOR
candidate → sparse ego-agent world → fine-grained safety → select
```

Critical source-verified boundary:

```text
candidate-specific sparse worlds                   YES
candidate-specific PDM safety/value labels         YES
candidate-specific pair-collision/TwDAC labels     YES
candidate-specific alternative-agent future GT     NO
reactive other-agent truth in NAVSIM path          NO
```

Strongest attribution:

```text
BEV + scene-level safety       ~90.9 PDMS
Sparse + scene-level safety    ~90.9
Sparse + fine-grained safety    91.6
```

Thus sparse representation alone is not isolated as superior; the supported contribution is sparse structure × localized safety reasoning.

No Ontology V1.4 amendment.

## 4. P0005 RiskWorld — NEXT

Boundary anchor rather than automatically a core planner paper.

Why it matters:

```text
object-centric latent rollout
→ future ego-object relation
→ object-level risk identification
```

Mandatory distinctions:

```text
risk as predicted world state
vs safety as evaluator/value
vs benchmark collision outcome
```

Mandatory questions:

```text
object state and identity persistence
RSSM/recurrent dynamics semantics
physical future horizon
whether ego action conditions dynamics
risk-label provenance
risk decoder vs analytic risk computation
whether any planner consumes the output
prediction evidence vs planning evidence
```

Mandatory comparisons:

```text
RiskWorld vs SafeDrive
RiskWorld vs GraphWorld
RiskWorld vs WoTE
RiskWorld vs DA-WAM
RiskWorld vs LAW / World4Drive
```

## 5. P0007 DriveReward

Value/reward control anchor:

```text
trajectory + visual context
→ generative VLM reward reasoning
→ RL / test-time trajectory selection
```

Purpose: prevent the atlas from assuming future-world prediction is the only route to better trajectory evaluation.

---

# Wave C.7 — Simulation / reactivity / evaluation controls

```text
P0003 Safe-Sim
P0004 PROSIM
P0013 BridgeSim
P0014 ReactSimBench
P0015 CausalDrive
```

Scientific purpose:

```text
reactive environment modeling
behavior simulation
log-replay vs endogenous reaction
generative simulator vs planning WAM
open-loop vs non-reactive pseudo-sim vs reactive closed loop
simulation truth / evaluation truth
```

These papers are required because the current anchor set still under-covers simulator/evaluation semantics, not because of a parked candidate hypothesis.

---

# Wave C.8 — WAM+VLA / reasoning boundary controls

```text
P0008 AutoVLA
P0011 ReCogDrive
P0010 LINGO-2
P0006 DriveGPT4
```

Purpose:

```text
separate world-model benefit from language/reasoning prior
separate generative planning from VLM/VLA semantic reasoning
understand reward/post-training/reasoning interfaces
avoid calling every future-aware VLA a world model
```

---

# Reading protocol for every added paper

```text
paper-deep-reader reconstruction
→ source/version gate
→ architecture/training/inference graph
→ strongest matched ablations
→ immediate cross-paper comparison
→ force-fill Ontology V1.3
→ residue/back-projection test
```

Every important mechanism must trigger:

```text
1. What exactly does this module do?
2. Which prior anchors perform the same scientific function?
3. Are implementation, supervision and deployment roles actually the same?
4. What is the strongest matched evidence it matters?
5. What does the paper NOT establish?
```

---

# Parked work

```text
landscape/WAM_RESEARCH_TENSIONS_V1.md
landscape/WAM_RESEARCH_TENSIONS_V2_VALIDATED.md
audits/research_synthesis/WAM_TIER1_TENSION_ADVERSARIAL_VALIDATION_V1.md
landscape/WAM_CANDIDATE_PROBLEMS_V1.md
landscape/WAM_CANDIDATE_PROBLEM_OVERLAP_MATRIX_V1.md
landscape/WAM_CANDIDATE_PROBLEM_RESEARCHABILITY_V1.md
```

Historical/provisional only until the expanded corpus is reconsolidated.

---

# Next paper

```text
P0005 RiskWorld
```

Reason: after SafeDrive established `candidate-specific structured world → explicit safety evaluator`, RiskWorld is the next coverage-control needed to determine what it means for **risk itself** to be part of a predicted world state rather than merely a scoring target.
