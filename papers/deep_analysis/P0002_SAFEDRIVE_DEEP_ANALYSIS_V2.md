# P0002 SafeDrive — Dimension-first Deep Analysis V2

Last updated: 2026-09-15

Status: **COMPLETE FIRST PASS — PAPER + OFFICIAL NAVSIM SOURCE AUDITED**

Paper: **SafeDrive: Fine-Grained Safety Reasoning for End-to-End Driving in a Sparse World**

Canonical research role in this repository:

```text
ONLINE TRAJECTORY-CONDITIONED SPARSE INTERACTION WORLD
→ AGENT×TIME SAFETY REASONING
→ EXPLICIT SAFETY/VALUE SCORING
→ TRAJECTORY SELECTION
```

Do **not** summarize SafeDrive as either:

```text
"a sparse world model that gives true counterfactual futures for every ego plan"
```

or:

```text
"just another scene-level trajectory scorer"
```

The source-audited picture is more precise: each selected ego candidate receives its own sparse interaction world and its own simulator-derived safety labels, while the surrounding-agent motion targets used to train the world branches remain the same logged future across different ego candidates. SafeDrive therefore has strong candidate-specific **consequence/safety supervision** without candidate-specific reactive **environment-future truth**.

---

# 0. Source and version contract

Primary paper source:

```text
papers/raw_md/P0002_SafeDrive/P0002_SafeDrive.raw.md
SafeDrive: Fine-Grained Safety Reasoning for End-to-End Driving in a Sparse World
CVPR 2026 Highlight
arXiv:2602.18887
```

Official implementation:

```text
SPA-junghokim/SafeDrive
commit audited: ea7791d6c2ebdeedfb6ed514f080cdfa1675b76f
commit date: 2026-09-08
```

Decision-critical source paths:

```text
README.md
docs/train_eval.md
navsim/agents/safedrive/safedrive_model.py
navsim/agents/safedrive/safedrive_agent.py
navsim/agents/safedrive/safedrive_loss.py
navsim/agents/safedrive/safedrive_config.py
navsim/agents/safedrive/modules/transformer_motion.py
navsim/agents/safedrive/score_module/compute_navsim_score.py
navsim/planning/script/config/common/agent/SafeDrive_Phase2_Planner_FreezePerception.yaml
navsim/planning/script/config/common/agent/SafeDrive_Phase3_Planner_FullTrain.yaml
train.sh
test.sh
```

Source boundary:

```text
NAVSIM training / scoring / released checkpoint path  SOURCE-VERIFIED
Bench2Drive paper result                              PAPER-VERIFIED
Bench2Drive implementation branch                     NOT IDENTIFIED in audited public repo
```

---

# 1. Executive mechanism verdict

SafeDrive is a three-stage planner:

```text
CAMERA + LIDAR + HISTORY
→ ProposalNet
   BEV + objects + 256 trajectory anchors
   → refined proposals + coarse scene-level safety
   → prune candidate set

FOR EACH SURVIVING EGO CANDIDATE
→ SWNet
   candidate planning query + copied surrounding-agent queries
   → one sparse world
   → intra-world self-attention
   → trajectory-guided future feature sampling
   → joint ego/agent motion refinement

→ FRNet
   scene-level safety
   + Pair-wise No Collision (agent × future time)
   + Time-wise Drivable Area Compliance (future time / ego footprint)
   → weighted safety score
   → select final trajectory
```

Canonical subtype:

```text
TRAJECTORY-CONDITIONED SPARSE-WORLD SAFETY EVALUATOR
```

Its scientific novelty is not merely `sparse representation`. The strongest matched evidence says the important combination is:

```text
SPARSE INTERACTION REPRESENTATION
×
FINE-GRAINED SAFETY LOCALIZATION
```

rather than sparse representation alone.

---

# 2. ProposalNet — world reasoning starts after a strong candidate planner

## 2.1 Current representation

ProposalNet fuses camera and LiDAR into spatiotemporal BEV features `F_BEV`, then extracts object/instance queries. The official Phase-3 configuration uses a 4 s trajectory horizon with 0.5 s spacing.

The planner starts from K-means trajectory anchors. The released implementation ships:

```text
num_plan_anchor = 256
trajectory_anchors_256_GTRS.npy
```

A two-stage proposal path is active in the released Phase-3 config:

```text
256 anchors
→ ProposalNet trajectory refinement / coarse scoring
→ top 128 proposals
→ SWNet
```

The model also filters surrounding instances before sparse-world reasoning; the released config uses `num_filtering_instance=25`.

Important attribution control:

```text
SafeDrive final performance
!=
world model added to a weak trivial planner
```

Candidate generation, refinement and coarse safety filtering are independent sources of planning strength and must be separated from the world/safety modules.

---

# 3. SWNet — what exactly is a “Sparse World”?

## 3.1 One ego candidate creates one world branch

For each surviving planning query, SafeDrive replicates surrounding-agent queries and combines them with that ego planning query. Thus the branch identity is:

```text
world j
=
{ ego-plan query j, surrounding-agent queries }
```

This creates candidate-specific world representations:

```text
trajectory candidate 1 → sparse world 1
trajectory candidate 2 → sparse world 2
...
```

This is stronger architectural alignment than a single pooled future representation shared across candidates.

## 3.2 World Interaction Module

Inside each world, SWNet performs:

```text
intra-world self-attention
→ ego / agent relational exchange
→ trajectory-guided deformable attention along predicted future paths
→ refined world queries
→ refined ego and surrounding-agent motion
```

Therefore the world object is not RGB/video, occupancy or one compact global latent. It is an **instance-centric structured query set** whose elements carry predicted future motion and interaction information.

## 3.3 Physical-time semantics

SafeDrive predicts explicit future poses over the planning horizon. These pose indices correspond to physical future timesteps. This is different from:

```text
DriveLaW diffusion/flow denoising steps
GraphWorld flow transport coordinate
DynFlowDrive rectified-flow coordinate
```

which are internal solver/transport coordinates rather than physical time.

---

# 4. FRNet — explicit fine-grained safety semantics

SafeDrive is one of the strongest current anchors for distinguishing:

```text
future/world representation
from
explicit safety semantics
```

## 4.1 Pair-wise No Collision (PwNC)

For every ego candidate, surrounding agent and future timestep, FRNet predicts a collision-free probability. Conceptually:

```text
candidate j × agent i × future step h
→ p(no collision)
```

This is much more localized than a single scene-level NC score. The network can identify **which agent** and **when** the danger emerges.

## 4.2 Time-wise Drivable Area Compliance (TwDAC)

FRNet also predicts whether the ego trajectory remains within the drivable region over future timesteps. The released implementation can combine ego-world features with BEV road features and evaluates off-road pose/timestep supervision.

## 4.3 Final decision

At deployment, SafeDrive combines multiple learned safety/quality terms in log space. The released `test.sh` uses explicit weights for:

```text
imitation
NC
DAC
EP
TTC
PwNC
TwDAC
aggregate PDM score
DDC / TLC / LK
```

Thus SafeDrive is not merely `world → latent → opaque score`; it is an explicit multi-factor safety/value selector.

Important boundary:

```text
PwNC/TwDAC = learned safety proxies / evaluators
!= formal safety guarantee
```

The paper itself treats them as learned reasoning signals, not proof of collision impossibility.

---

# 5. The most important source-level supervision audit

This section is the central result of the deep read.

## 5.1 Candidate-specific safety consequence labels — YES

In the released training path, the model's own final candidate trajectories are detached and sent through the NAVSIM PDM simulator/scorer. The source then injects per-candidate targets:

```text
safety_target_scores
pair_collision_gt
twdac_gt
```

The PDM scorer evaluates every proposal using NC, DAC, EP, TTC, comfort, DDC and, in EPDMS mode, TLC/LK. It also exposes:

```text
which agent token caused an at-fault collision
at which future timestep
which future ego pose is off-road
```

Therefore:

```text
candidate-specific safety / value supervision = YES
agent×time collision labels                 = YES
time-wise drivable-area labels              = YES
```

This is substantially richer decision supervision than simply assigning an imitation label.

## 5.2 Candidate-specific alternative-world truth — NO

However, the surrounding-agent motion prediction loss uses the logged future motion trajectories. In the active `all_motion_predidction_loss=true` path, the same logged agent-future targets are expanded/reused over the ego-anchor/world dimension.

Hence:

```text
ego candidate A → predicted agent future A
                         \ target = logged agent future

ego candidate B → predicted agent future B
                         \ target = same logged agent future
```

The architecture may produce different branch representations, but the training data do not provide a different observed/reactive surrounding-agent future for every ego intervention.

Binding conclusion:

```text
candidate-specific sparse-world output              YES
candidate-specific safety/value consequence labels  YES
candidate-specific alternative-agent future truth   NO
reactive ego→other-agent intervention truth          NO in audited NAVSIM path
```

This is a critical distinction:

> **Consequence supervision can be candidate-specific even when environment-dynamics truth is not.**

---

# 6. Training topology

Official release uses three stages:

```text
Phase 1: perception pretraining
Phase 2: planner + safety heads with perception frozen
Phase 3: end-to-end full fine-tuning
```

The public docs give the shipped training schedule approximately as:

```text
Phase 1  90 epochs
Phase 2   5 epochs
Phase 3  10 epochs
```

Phase 2 and Phase 3 both use live simulator-scored safety targets (`use_target_scores=True`). Phase 2 freezes perception modules; Phase 3 removes that freeze and trains the full model end-to-end.

Loss families include:

```text
perception / BEV semantic losses
trajectory imitation classification + regression
surrounding-agent motion prediction
scene-level safety losses
PwNC loss
pair-wise displacement/motion losses
TwDAC loss
```

So final SafeDrive performance is a bundle of perception, proposal quality, world interaction, motion prediction and explicit safety/value learning.

---

# 7. Inference graph

NAVSIM deployment is:

```text
sensor history
→ ProposalNet
→ coarse proposals / coarse safety
→ candidate pruning
→ SWNet candidate-specific sparse worlds
→ FRNet safety heads
→ weighted learned safety score
→ argmax / final trajectory
```

The external PDM simulator used to generate training safety targets is **not** needed online for the deployed planner. It is a teacher/label generator during training and a benchmark evaluator after trajectory generation.

This separates:

```text
training-time simulator teacher
from
online learned safety evaluator
```

which is analogous in lifecycle to other teacher→student decision systems, but SafeDrive preserves an explicit online world + safety model rather than distilling everything into a plain policy score head.

---

# 8. Strongest matched evidence

## 8.1 Sparse representation alone is not the main result

The cleanest reported representation/safety-granularity control is approximately:

```text
baseline / no world representation            90.1 PDMS
BEV representation + coarse safety            90.3
BEV + scene-level safety                      90.9
Sparse world + scene-level safety             90.9
Sparse world + fine-grained safety             91.6
```

The key observation is:

```text
BEV + scene-level      ≈ 90.9
Sparse + scene-level   ≈ 90.9
```

so the paper does **not** show that sparse representation by itself dominates BEV.

The strongest evidence is the interaction:

```text
Sparse world
+
agent/time localized safety reasoning
→ 91.6
```

Thus the scientifically defensible statement is:

> Sparse structure becomes useful when the evaluator can exploit its agent- and timestep-level semantics.

## 8.2 PwNC and TwDAC

Reported fine-grained-head ablation is approximately:

```text
coarse/scene-level baseline   90.9
+ PwNC                        91.5
+ TwDAC                       91.4
+ PwNC + TwDAC                91.6
```

Both help, but their gains are not additive. PwNC contributes slightly more in the reported PDMS control.

## 8.3 Main benchmark result

Paper reports roughly:

```text
NAVSIM-v1 PDMS    91.6
NAVSIM-v2 EPDMS   87.5
NAVSIM collisions 61 / 12,146 scenarios (~0.5%)
Bench2Drive DS    66.8
```

The official release README reports a reproduced NAVSIM result (`SafeDrive*`) of 91.6 PDMS with the released checkpoint/scoring path.

---

# 9. Evaluation semantics

## NAVSIM

Project-standard label:

```text
NON-REACTIVE DATA-DRIVEN / PSEUDO-SIMULATION PLANNING
```

PDM can score different ego trajectories against map/logged-world semantics, so SafeDrive obtains candidate-specific safety labels. This does **not** imply that surrounding agents were reactively resimulated under each alternative ego action.

Therefore:

```text
high NC/TTC/PwNC/PDMS
!= validated reactive counterfactual dynamics
```

## Bench2Drive

Paper reports reactive CARLA closed-loop performance. That supports the final policy's competence during interactive execution.

But:

```text
reactive final-policy benchmark
!= direct validation that SWNet's candidate branches predict intervention-correct surrounding-agent futures
```

The audited public repository did not expose a clearly attributable Bench2Drive execution branch, so implementation-level verification remains partial for that benchmark.

---

# 10. Immediate cross-paper comparison

## SafeDrive vs WoTE

```text
WoTE:
candidate → recurrent BEV future → explicit utility → select

SafeDrive:
candidate → sparse ego/agent world → agent×time safety + scene utility → select
```

Both use explicit consequence/value semantics online. WoTE is stronger on recurrent world-sequence modeling; SafeDrive is stronger on localized safety semantics. Neither audited NAVSIM target path establishes reactive branch-specific surrounding-agent truth.

## SafeDrive vs DA-WAM

```text
DA-WAM:
candidate → 0.5s implicit latent → factorized utility
only expert branch has direct future-latent truth

SafeDrive:
candidate → explicit sparse interaction world → localized safety evaluator
all candidates have simulator-derived safety labels
but agent-motion truth is still shared/logged across candidate worlds
```

Thus SafeDrive has stronger candidate-specific **decision consequence** supervision, not stronger reactive environment truth.

## SafeDrive vs GraphWorld

```text
GraphWorld:
structured interaction world → condition direct planner
explicit utility scorer absent

SafeDrive:
structured candidate-specific sparse world
→ explicit safety/value reasoning
→ selection
```

GraphWorld is representation-conditioned direct policy; SafeDrive is structured consequence evaluation.

## SafeDrive vs World4Drive

```text
World4Drive score = factual-future / mode consistency
SafeDrive score   = explicit safety / compliance / progress semantics
```

Similar multi-branch diagrams therefore implement different decision objects.

## SafeDrive vs DriveLaW

```text
DriveLaW:
one common generative hidden representation → direct policy

SafeDrive:
multiple ego candidates → multiple sparse interaction worlds
→ explicit evaluator → select
```

They sit on opposite sides of direct-policy vs candidate-evaluation planning.

---

# 11. What SafeDrive proves / does not prove

## Strongly supported

```text
candidate-specific sparse interaction representation is deployable online;
agent/time safety decomposition can improve planning over coarse scene-level scoring;
PDM-derived candidate-specific safety supervision can train fine-grained learned evaluators;
explicit safety semantics can coexist with an end-to-end planner;
the released NAVSIM code reproduces the main PDMS level.
```

## Not established

```text
each ego candidate has its own factual/reactive surrounding-agent future truth;
PwNC/TwDAC are calibrated physical risk probabilities;
SafeDrive provides formal safety guarantees;
sparse representation alone is superior to dense BEV;
Bench2Drive final-policy success validates SWNet counterfactual dynamics;
better agent motion prediction fidelity is the causal source of the full PDMS gain.
```

---

# 12. Ontology stress-test result

SafeDrive exposes a useful residue:

```text
SAFETY LOCALIZATION GRANULARITY
scene-level
vs agent-level
vs agent×time
vs ego-footprint/time spatial localization
```

However this is already expressible through existing dimensions:

```text
B04 state semantics/granularity
K02 scorer semantics
K04 factorization
K05 target provenance
P01/P02 explicit risk/safety state and scorer
P04 interaction semantics
G04 consequence/value teacher truth
```

Decision:

```text
ONTOLOGY V1.3 RETAINED
NO V1.4 FROM SAFEDRIVE
```

Keep `safety-localization granularity` on the residue watchlist until an independent anchor demonstrates cross-paper explanatory value beyond the existing dimensions.

---

# 13. Final normalized identity

```text
SafeDrive
=
multimodal temporal BEV
→ objects + 256 trajectory anchors
→ coarse proposal/safety pruning
→ one sparse ego-agent world per surviving ego candidate
→ world self-attention + trajectory-guided feature sampling
→ joint ego/agent future refinement
→ scene-level + pairwise-agent/time + drivable-area/time safety heads
→ learned weighted safety selection

TRAINING TRUTH:
model-generated ego candidates receive candidate-specific PDM safety labels;
surrounding-agent motion supervision remains based on logged futures and is reused across ego branches.
```

Primary binding lesson:

```text
candidate-specific safety consequence supervision
!=
candidate-specific reactive world truth
```
