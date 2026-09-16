# WAM Comparison Matrix V1.3 — DriveReward Extension

Last updated: 2026-09-16

Status: **16-ANCHOR EXTENSION — DRIVEREWARD NORMALIZED**

This file adds P0007 DriveReward to the active comparison set without changing Ontology V1.3.

Canonical analysis:

```text
papers/deep_analysis/P0007_DRIVEREWARD_DEEP_ANALYSIS_V2.md
audits/literature/PHASE_C6_DRIVEREWARD_AUDIT.md
landscape/P0007_DRIVEREWARD_ONTOLOGY_PROJECTION.md
```

---

# 1. DriveReward row

| Dimension | DriveReward |
|---|---|
| Primary role | semantic trajectory reward/value modeling for RL and candidate selection |
| World object | **NONE — no explicit predicted future world** |
| Current representation | InternVL3-1B visual-language hidden state + route/ego/candidate context |
| Future dynamics | **ABSENT** |
| Candidate input | **YES — ego trajectory** |
| Candidate-specific reward | **YES** |
| Candidate-specific future world | **NO** |
| Output | reasoning + NC/DAC/TTC/EP/Comfort/CF/Legality |
| Value semantics | explicit hybrid safety/progress/comfort/rule/command reward |
| Reward supervision | PDM/NAVSIM metrics + deterministic CF + Qwen3.5 legality/reasoning teacher |
| Alternative-action future truth | **NO** |
| Reactive other-agent truth | **NO** |
| RL use | **YES — training-time reward teacher** |
| Test-time use | **YES — optional candidate scorer** |
| World model required online | **NO** |
| Planning evidence | RL gains across multiple policies; small +0.2 PDMS online selection gain on AdaThinkDrive |
| Source status | paper verified; official implementation not identified |

Canonical subtype:

```text
VLM-BASED CANDIDATE VALUE / REWARD MODEL
```

---

# 2. Consequence prediction vs value modeling

| Method | Explicit future state? | Direct candidate value? | Candidate-specific world branch? | Main planning interface |
|---|---:|---:|---:|---|
| **DriveReward** | **NO** | **YES** | **NO** | RL reward / direct scorer |
| WoTE | YES, recurrent BEV/state | YES | YES | future → utility → argmax |
| DA-WAM | YES, short latent | YES | YES | future latent → factors/value |
| SafeDrive | YES, sparse future/safety world | YES | YES | fine-grained safety → select |
| World4Drive | YES, endpoint latent | score is mode/factual consistency rather than explicit utility | YES | future latent → ScoreNet |
| RiskWorld | YES, factual object rollout | object-risk, not ego candidate value | NO ego-action branch | risk monitoring |

Binding distinction:

```text
learned value/reward
!=
explicit consequence prediction
!=
world model
```

DriveReward is the clean control for the first category.

---

# 3. DriveReward vs WoTE

Shared scientific problem:

```text
which ego trajectory should be preferred?
```

Mechanism split:

```text
WoTE
candidate_i
→ recurrent future state_i
→ learned utility_i
→ argmax

DriveReward
current visual-semantic context + candidate_i
→ direct reward_i
→ RL or argmax
```

Scientific consequence:

```text
future-state mediation is one route to value estimation,
not the definition of value estimation itself.
```

WoTE's future-state ablation can test whether explicit future features add value inside its own architecture; DriveReward prevents generalizing that result into a universal requirement for trajectory evaluation.

---

# 4. DriveReward vs DA-WAM

DA-WAM matched planning control:

```text
No Future                  93.31 PDMS
Action-Conditioned Future  93.46
+ Hard Negatives           93.68
```

DriveReward has no explicit future latent at all yet provides useful reward supervision and some ranking capability.

Therefore DA-WAM should be decomposed as:

```text
strong candidate valuation base
+ small matched future-latent increment
+ hard-negative / ranking improvement
```

rather than described as one monolithic world-model gain.

---

# 5. DriveReward vs SafeDrive

```text
SafeDrive
candidate trajectory
→ sparse candidate-conditioned world
→ agent×time safety / PDM factors
→ select

DriveReward
candidate trajectory + visual-semantic context
→ direct factorized reward
→ train/select
```

Shared:

```text
explicit safety/value semantics
candidate-specific decision supervision
```

Different:

```text
SafeDrive explicitly represents predicted consequence structure.
DriveReward compresses consequence judgment directly into a VLM evaluator.
```

Thus explicit safety semantics does not imply an explicit future-world state.

---

# 6. DriveReward vs RiskWorld

The two are useful structural opposites:

```text
RiskWorld
history → 60-step factual object/world relation rollout → explicit risk
future-model depth = strong
planner coupling = absent

DriveReward
candidate action + current semantic context → direct explicit value/reward
future-model depth = absent
planner coupling = strong through RL/scoring
```

Therefore:

```text
world rollout depth ⟂ decision-interface strength
```

This is now supported by independent anchors rather than only a taxonomy argument.

---

# 7. Supervision truth comparison

| Method | Factual future truth | Candidate-specific value/safety truth | Reactive alternative-world truth |
|---|---:|---:|---:|
| DriveReward | NO explicit future target | **YES** — metric/rule/VLM labels | NO |
| WoTE | YES logged future structure | YES learned reward/value | NO in audited PDM target path |
| DA-WAM | expert-matched branch only for direct future truth | **YES all branches** factor/value/rank | NO / not established |
| SafeDrive | logged surrounding futures / sparse state components | **YES** PDM safety labels | NO reactive-agent GT |
| RiskWorld | **YES** logged future object relations | risk-object/event label, not ego action value | NO |

Key separation:

```text
factual future truth
candidate-specific decision truth
reactive intervention truth
```

are three independent supervision objects.

DriveReward has the second without the first or third.

---

# 8. Training-time vs deployment-time value knowledge

DriveReward has two lifecycles:

```text
A. RL teacher
reward model online during post-training
→ policy absorbs value knowledge
→ reward model may disappear at deployment

B. Online scorer
reward model retained
→ evaluate N candidate trajectories
→ choose candidate
```

This extends the existing future-knowledge lifecycle lesson into value models:

```text
training-time decision supervision strength
and
deployment-time evaluator dependence
are orthogonal axes
```

This parallels the WM lifecycle distinction already seen in Drive-JEPA, Metis and DynFlowDrive.

---

# 9. Planning evidence decomposition

## Reward-model quality

```text
InternVL3-1B SFT → DriveReward-1B
Safety 72.2 → 80.6
DAC    75.6 → 81.2
CF     95.5 → 99.9
LG     92.2 → 97.6
EP-MAE .34  → .23
```

## Policy RL

```text
InternVL3-2B       80.8 → 82.2 PDMS
InternVL3-8B       85.6 → 86.8
DiffusionDriveV2   89.1 → 90.7
```

## Closed-loop Bench2Drive

```text
Base SFT                    40.2 DS
RM-predicted PDMS RL        51.4
Rule-PDMS RL                55.0
Rule-PDMS + RM CF/LG RL     57.1
```

## Test-time selection

```text
Original       90.3 PDMS
Best-of-4      93.0
DriveReward    90.5
```

Canonical attribution:

```text
strongest evidence = training-time reward / RL interface
weaker evidence    = online candidate reranking interface
```

Do not infer a strong deployed scorer from the RL results.

---

# 10. Reward-teacher provenance as a confound

DriveReward reward knowledge is not learned from one homogeneous source.

It distills:

```text
simulator / PDM metrics
+ deterministic command rule
+ VLM legality labels
+ VLM reasoning traces
+ foundation VLM prior
+ geometry foundation prior
```

Therefore comparisons against explicit WAMs must ask:

```text
Is the gain from modeling future consequences?
or
from importing richer target semantics / teacher knowledge?
```

DriveReward is a particularly strong control for this attribution question.

---

# 11. Evaluation boundary

Keep regimes separate:

```text
DriveReward-Bench
= evaluator accuracy

NAVSIM-v1
= non-reactive data-driven / pseudo-simulation planning

Bench2Drive
= interactive CARLA closed loop

AdaThinkDrive Best-of-N
= candidate-selection experiment
```

The reported Bench2Drive gains are evidence for a policy **trained using** DriveReward, not evidence that DriveReward itself simulates a reactive world.

---

# 12. Scientific role in the growing atlas

DriveReward fills the control family:

```text
DIRECT LEARNED VALUE / REWARD WITHOUT EXPLICIT FUTURE-WORLD STATE
```

It sharpens a central design-space question:

```text
When does a planner need an explicit predicted world state,
and when can the relevant consequence information be compressed directly into value/reward?
```

This is a field question, not yet a research gap.

---

# Ontology decision

```text
V1.3 RETAINED
NO V1.4
```

DriveReward maps cleanly onto existing dimensions, especially:

```text
A01/A02 role
G04 reward truth
J03/J05/J07 planning interface/lifecycle
K01–K05 scorer semantics
M01–M03 lifecycle
O05/O06 attribution
P01/P02 explicit safety/value semantics
```
