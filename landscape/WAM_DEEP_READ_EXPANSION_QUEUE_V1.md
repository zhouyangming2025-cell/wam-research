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

## 1. P0009 DriveLaW — NEXT

Why it matters:

```text
video world model internal latent
→ directly conditions diffusion planner
```

This is not Epona's sibling visual/trajectory branches and not WorldDrive's teacher→distilled-future path. It directly tests whether a generative video model's internal denoising representation can serve as the planning state.

Mandatory comparisons:

```text
DriveLaW vs Epona
DriveLaW vs WorldDrive
DriveLaW vs Metis
DriveLaW vs Discrete-WAM
DriveLaW vs LAW
```

Key questions:

```text
what exact Video-DiT latent is exported?
is the latent current/history, denoising-state, or predicted-future information?
which denoising timestep(s) are used?
video→planner forward dependence at inference?
planner→video coupling?
three-stage freezing/fine-tuning topology?
generation fidelity→planning evidence?
physical future time vs diffusion/flow solver time?
```

## 2. P0012 DA-WAM

Why it matters:

```text
N candidate trajectories
→ N action-conditioned future latents
→ per-candidate factorized scorer
```

It directly pressure-tests World4Drive/WoTE/WorldDrive distinctions and explicitly acknowledges the one-factual-future limitation.

Mandatory questions:

```text
one-to-one trajectory↔future latent correspondence
expert-matched future supervision only
hard-negative supervision semantics
factorized safety/value heads
EMA target / online encoder adaptation
candidate-specific prediction vs candidate-specific truth
```

## 3. P0002 SafeDrive

Why it matters:

```text
trajectory-conditioned sparse world
→ agent/timestep-level future interaction states
→ explicit collision + drivable-area safety reasoning
```

This adds a major safety/world-planning anchor missing from the first 11.

Mandatory comparisons:

```text
SafeDrive vs WoTE explicit utility
SafeDrive vs GraphWorld structured interaction state
SafeDrive vs World4Drive candidate future
SafeDrive vs RiskWorld object-level risk
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

Important: these are not to be read merely because prior candidate problem CP-T5 mentioned reactivity. They are required independently because the first 11 anchors under-cover simulation/evaluation semantics.

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
P0009 DriveLaW
```

Reason: it is a central planning-centric WAM paper with a world→planner interface materially different from the 11-anchor set, and it has paper text plus an attributable official code repository for later source audit.
