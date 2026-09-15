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

The candidate-problem/tension artifacts produced after the 11-anchor synthesis are retained only as **parked provisional observations**. They MUST NOT drive paper selection or method design during this expansion phase.

The immediate objective is to broaden and stress-test the coordinate system with additional papers selected by **coverage diversity**, not by whether they support a preferred hypothesis.

Current normalized count:

```text
13 papers
```

Latest completed expansion anchors:

```text
P0009 DriveLaW — COMPLETE
P0012 DA-WAM   — COMPLETE
```

---

# Working gate before another research-direction discussion

Use both a count gate and a diversity gate.

Working count target:

```text
~24–30 deeply normalized papers total
```

This is not a magic threshold. The real stop condition is that the major mechanism families below have multiple independent anchors and new papers mostly map into existing dimensions without repeatedly exposing major blind spots.

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

No final research gap or method design before the next consolidation gate.

---

# Wave C.6 — Core planning-centric WAM expansion

## 1. P0009 DriveLaW — COMPLETE

Canonical result:

```text
ONLINE GENERATIVE-LATENT DIRECT-POLICY WAM
```

Stable mechanism:

```text
history frames
→ first-pass Video-DiT internal block states
→ blockwise Action-DiT conditioning
→ direct trajectory flow policy

full video rollout / RGB future decode not required
```

Key findings added to the coordinate system:

```text
forward world→action can coexist with backward action-loss→world gradient flow;
online world-model use does not imply completed future rollout;
planning-optimal generative state can be an EARLY denoising state;
more complete denoising is not monotonically better for planning.
```

No Ontology V1.4 amendment; candidate residue retained:

```text
GENERATIVE-STATE TAP LOCATION / SOLVER-DEPTH OF POLICY CONDITION
```

## 2. P0012 DA-WAM — COMPLETE

Canonical result:

```text
ONLINE CANDIDATE-SPECIFIC FUTURE-LATENT UTILITY SCORING WAM
```

Stable mechanism:

```text
2 historical front-camera frames
→ V-JEPA 2.1 online encoder + LoRA
→ 32 trajectory candidates
→ one 0.5s future latent per candidate
→ factorized NC/DAC/EP/TTC/Comfort + utility scorer
→ argmax
```

Critical supervision boundary:

```text
candidate-specific future output               YES
candidate-specific direct future truth         NO except expert-matched branch
all-branch factor/value/ranking supervision    YES
reactive alternative-world truth               NO / NOT ESTABLISHED
```

Strongest matched control:

```text
No Future Prediction          93.31 PDMS
Shared Global Future          92.81
Current-Latent Conditioning   93.25
Action-Conditioned Future     93.46
+ Hard Negatives              93.68
```

No Ontology V1.4 amendment. Official `LeapWM/da-wam` repository currently contains only a placeholder README, so implementation remains source-unverified.

## 3. P0002 SafeDrive — NEXT

Why it matters:

```text
trajectory-conditioned sparse world
→ agent/timestep-level future interaction states
→ explicit collision + drivable-area safety reasoning
```

This adds a major safety/world-planning anchor missing from the existing 13-paper normalized set.

Mandatory comparisons:

```text
SafeDrive vs WoTE explicit utility
SafeDrive vs DA-WAM factorized utility
SafeDrive vs GraphWorld structured interaction state
SafeDrive vs World4Drive candidate future
SafeDrive vs RiskWorld object-level risk
```

Mandatory questions:

```text
what is the sparse world state?
which agent/timestep objects are predicted?
how ego trajectory conditions future interaction?
what future truth exists for alternative ego candidates?
what is predicted state vs rule evaluator vs learned safety/value?
how safety information changes final planning?
```

## 4. P0005 RiskWorld

Boundary anchor rather than pure planner paper.

Why it matters:

```text
object-centric RSSM-style latent rollout
→ future ego-object relation
→ object-level risk identification
```

Use it to distinguish:

```text
risk as explicit predicted state
vs safety as evaluator/reward
vs safety only observed in benchmark metrics
```

Do not force it into the planning-core family if the planning interface is absent.

## 5. P0007 DriveReward

Value/reward control anchor.

Why it matters:

```text
trajectory + visual context
→ generative VLM reward reasoning
→ RL / test-time trajectory selection
```

It broadens the value/utility side beyond world-state prediction and prevents us from assuming that future-world modeling is the only way to improve trajectory evaluation.

---

# Wave C.7 — Simulation / reactivity / evaluation controls

Deep-read after core C.6, unless a C.6 paper requires one as immediate context.

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

Important: these are not to be read merely because prior candidate problem CP-T5 mentioned reactivity. They are required independently because the first-wave anchors under-cover simulation/evaluation semantics.

BridgeSim is especially valuable as an evaluation/control paper because it decomposes open-loop→closed-loop failure into observational shift and objective mismatch rather than treating benchmark score as interchangeable evidence.

ReactSim-Bench is especially valuable as a benchmark anchor because it explicitly evaluates world-agent reactions when the AV deviates from the log.

CausalDrive is valuable as a world-simulator anchor because it removes oracle future-NPC layouts and targets real-time reactive visual generation.

---

# Wave C.8 — WAM+VLA / reasoning boundary controls

Secondary to core WAM, but necessary before claiming full field understanding.

Initial queue:

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

Add more WAM+VLA papers only when they expose a mechanism not covered by these controls.

---

# Reading protocol for every added paper

Use the same WAM reading stack:

```text
paper-deep-reader reconstruction
→ source/version gate
→ architecture/training/inference graph
→ strongest matched ablations
→ immediate cross-paper comparison
→ force-fill Ontology V1.3
→ residue/back-projection test
```

Every important mechanism must immediately trigger:

```text
1. What exactly does this module do?
2. Which prior anchors perform the same scientific function?
3. Is the implementation/supervision/deployment role actually the same?
4. What is the strongest matched evidence that this module matters?
5. What does the paper NOT establish?
```

---

# Parked work

The following files remain in the repo as historical/provisional synthesis, but are **NOT ACTIVE RESEARCH-DIRECTION AUTHORITY** during literature expansion:

```text
landscape/WAM_RESEARCH_TENSIONS_V1.md
landscape/WAM_RESEARCH_TENSIONS_V2_VALIDATED.md
audits/research_synthesis/WAM_TIER1_TENSION_ADVERSARIAL_VALIDATION_V1.md
landscape/WAM_CANDIDATE_PROBLEMS_V1.md
landscape/WAM_CANDIDATE_PROBLEM_OVERLAP_MATRIX_V1.md
landscape/WAM_CANDIDATE_PROBLEM_RESEARCHABILITY_V1.md
```

They may be revisited only after the expanded deep-read corpus is re-consolidated.

---

# Next paper

```text
P0002 SafeDrive
```

Reason: after DriveLaW covered online generative representation→direct policy and DA-WAM covered online candidate-specific future→explicit utility scoring, SafeDrive extends the map toward structured future interaction and explicit safety reasoning.
