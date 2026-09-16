# Phase C.6 DriveReward Audit

Last updated: 2026-09-16

Status: **COMPLETE FIRST PASS — PAPER VERIFIED; OFFICIAL IMPLEMENTATION NOT IDENTIFIED**

Paper:

```text
DriveReward: A Comprehensive Dataset and Generative Vision-Language Reward Model for Autonomous Driving
arXiv:2606.08525v2
```

Canonical deep read:

```text
papers/deep_analysis/P0007_DRIVEREWARD_DEEP_ANALYSIS_V2.md
```

---

# 1. Stable mechanism judgment

DriveReward is a **trajectory reward/value model**, not a future-world model.

Core mapping:

```text
front-view visual context
+ navigation instruction
+ ego state
+ candidate ego trajectory
→ InternVL3-1B semantic evaluator
→ reasoning tokens
+ NC / DAC / TTC / EP / Comfort / CF / Legality
→ RL reward teacher
  OR
→ test-time trajectory scorer
```

Canonical subtype:

```text
VLM-BASED CANDIDATE VALUE / REWARD MODEL
```

Binding boundary:

```text
candidate → learned reward/value
!=
candidate → explicit future world → learned reward/value
```

No explicit future RGB, BEV, occupancy, object future or world latent is generated.

---

# 2. Source/version boundary

In-repo primary text:

```text
papers/raw_md/P0007_DriveReward/P0007_DriveReward.raw.md
```

The PDF was document-verified during corpus ingestion.

No attributable official GitHub implementation was identified in the project ingest or live repository search as of 2026-09-16.

Final source label:

```text
PAPER-COMPLETE
SOURCE-BLOCKED / MONITOR
```

Two paper-level ambiguities remain unresolved without source code:

```text
A. temporal input wording
current front-view image
vs
historical video / 3-frame examples

B. trainability wording
§5.1: vision backbone frozen, LLM layers fine-tuned
vs
appendix: "full parameter fine-tuning"
```

A reporting inconsistency also exists for DriveReward dataset scale:

```text
~200K samples in dataset analysis
vs
300K DriveReward dataset in training-parameter description
```

Do not repair these by inference.

---

# 3. Candidate and label provenance

Candidate ego trajectories are drawn from:

```text
GT / logged trajectory
+ offline kinematic retrieval
+ planner-generated proposals
```

Reward target provenance must be separated:

```text
NC / DAC / TTC / EP / Comfort
→ NAVSIM / PDM-Closed style simulator or rule metrics

CF
→ deterministic endpoint-deviation rule relative to intended/GT maneuver

LG
→ Qwen3.5-35B-A3B semantic legality judgment

reasoning CoT
→ Qwen3.5 annotation aided by deterministic visual overlays
```

The overlays expose collision/off-road locations to the annotation teacher; the final reward model is stated to train on unmodified visual inputs.

Therefore the reward model distills a heterogeneous teacher stack rather than learning reward from raw human preference alone.

---

# 4. Counterfactual / intervention boundary

DriveReward enriches training with alternative/suboptimal ego trajectories.

Correct vector:

```text
alternative ego-action proposals                 YES
candidate-specific reward labels                 YES
candidate-specific observed future-world truth   NO
reactive other-agent intervention truth           NO
intervention-response validation                  NO
```

Thus:

```text
counterfactual action valuation
!=
counterfactual world dynamics identification
```

---

# 5. Training lifecycle

Two-stage reward-model training:

```text
Stage 1
~800K driving-domain QA / reasoning data
→ domain adaptation

Stage 2
DriveReward SFT
→ reasoning + factorized reward prediction
```

Geometry grounding adds:

```text
reward hidden geometry tokens
→ MLP adapter
→ VGGT latent alignment
→ L2 supervision
```

This is representation grounding, not future-state supervision.

The reward model subsequently has two distinct planning roles:

```text
TRAINING-TIME:
policy trajectories → DriveReward → scalar/factorized reward → RL policy update

TEST-TIME:
multiple policy trajectories → DriveReward → score → selection
```

These roles must not be collapsed.

---

# 6. Strongest reward-model ablation evidence

Reward benchmark:

```text
InternVL3-1B SFT
Safety 72.2 / DAC 75.6 / CF 95.5 / LG 92.2 / EP-MAE 0.34

DriveReward-1B
Safety 80.6 / DAC 81.2 / CF 99.9 / LG 97.6 / EP-MAE 0.23
```

Component ablation:

```text
full                 NC 80.58 / DAC 81.24 / CF 99.86 / LG 97.64 / EP-MAE .2308
w/o pre-training        80.52 /     81.06 /    99.84 /    97.48 /        .2355
w/o reasoning CoT       71.26 /     73.60 /   100.00 /   [NR]  /        .4161
w/o 3D adapter          79.04 /     80.88 /    99.86 /    97.20 /        .2518
```

The largest matched degradation is removing reasoning CoT. Domain pretraining and geometry alignment are positive but much smaller in the reported table.

Canonical attribution:

```text
final evaluator quality
=
foundation VLM prior
+ task-specific reward labels
+ teacher reasoning
+ geometry alignment
+ domain adaptation
```

Do not narrate it as one module's gain.

---

# 7. RL planning evidence

NAVSIM-v1 policy SFT → RL using DriveReward-predicted reward:

```text
InternVL3-2B       80.8 → 82.2 PDMS
InternVL3-8B       85.6 → 86.8
DiffusionDriveV2   89.1 → 90.7
```

Project-standard regime:

```text
NAVSIM-v1 = NON-REACTIVE DATA-DRIVEN / PSEUDO-SIMULATION PLANNING
```

Adding DriveReward CF/LG to rule PDMS:

```text
InternVL3-2B       83.3 → 83.3
InternVL3-8B       87.9 → 88.4
AdaThinkDrive-8B   89.3 → 89.9
```

This is evidence that learned semantic reward dimensions can complement rule metrics, but the incremental gain is modest.

---

# 8. Bench2Drive closed-loop evidence

Reported CARLA / Bench2Drive results:

```text
Base SFT                    DS 40.2 / Success 14.5
RL: RM-predicted PDMS       DS 51.4 / Success 20.8
RL: rule PDMS               DS 55.0 / Success 25.0
RL: rule PDMS + RM CF/LG    DS 57.1 / Success 27.2
```

This is the strongest planning evidence for DriveReward's **training-time reward-teacher** role.

However, the reported Comfort↑ column decreases:

```text
42.9 → 19.2 → 14.8 → 11.4
```

Therefore the overall driving-score improvement is not evidence of uniform improvement across all behavior qualities. Preserve this trade-off/reporting issue rather than smoothing it away.

---

# 9. Test-time scorer evidence

AdaThinkDrive with N=4 proposals:

```text
Original       90.3 PDMS
Best-of-N      93.0   (+2.7 oracle headroom)
DriveReward    90.5   (+0.2)
```

Binding interpretation:

```text
online learned reward scoring has positive evidence
BUT
reported gain is small and captures little of available oracle selection headroom
```

The training-time RL role currently has materially stronger evidence than the online reranking role.

---

# 10. Immediate cross-paper controls

## vs WoTE

```text
WoTE:
candidate → recurrent future state → utility → argmax

DriveReward:
candidate + current visual context → direct reward/value → train/select
```

DriveReward is the no-explicit-future value control.

## vs DA-WAM

```text
DA-WAM:
No Future                  93.31
Action-Conditioned Future  93.46
+ Hard Negatives           93.68 PDMS
```

Future latent adds a small matched increment inside an already strong valuation system. DriveReward strengthens the requirement to separate **future consequence modeling** from **value learning**.

## vs SafeDrive

```text
SafeDrive:
candidate → sparse future/consequence representation → explicit safety → select

DriveReward:
candidate + current semantic context → direct reward factors → train/select
```

## vs RiskWorld

```text
RiskWorld:
strong factual future rollout + explicit risk
but no action-selection interface

DriveReward:
strong action-value interface
but no explicit future rollout
```

Future modeling depth and decision coupling are orthogonal.

---

# 11. Historical boundary

Gen-Drive is a clear learned reward-model predecessor and uses preference-oriented reward learning within generation/evaluation and RL.

Therefore DriveReward must not be treated as the first learned reward model for autonomous driving.

Its more defensible distinguishing bundle is:

```text
explicit factorized driving reward targets
+ VLM semantic reasoning
+ geometry grounding
+ RL reward-teacher use
+ test-time scorer use
```

---

# 12. What DriveReward proves

- task-specific VLM reward learning can strongly improve reward-factor prediction;
- learned semantic reward can provide useful policy RL supervision;
- reward-teacher transfer to Bench2Drive improves the reported policy outcomes;
- CF/LG can add information beyond base rule PDMS;
- online learned trajectory reranking can provide a small positive gain.

# 13. What DriveReward does not prove

- an explicit world model or future-state transition;
- alternative-action future-world truth;
- reactive other-agent behavior under ego intervention;
- causal validity of latent VLM reasoning as dynamics;
- online scorer superiority over explicit future-state evaluators;
- real-vehicle closed-loop gain;
- calibrated reward uncertainty;
- uniform safety/comfort/efficiency improvement.

---

# Final audit verdict

```text
DriveReward is a high-value control anchor because it improves planning through learned semantic value/reward,
without explicitly predicting a future world.

explicit future world         NO
candidate-specific value      YES
RL reward supervision         YES
online candidate scoring      YES, modest reported gain
reactive intervention truth   NO
```

Ontology result:

```text
V1.3 RETAINED
NO V1.4
```
