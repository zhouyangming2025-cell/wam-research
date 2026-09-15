# PHASE_C5_SEERDRIVE_AUDIT

Last updated: 2026-09-15

Status: **COMPLETE FIRST PASS — paper deep read + official-repo version-boundary audit**

Paper:

```text
Future-Aware End-to-End Driving: Bidirectional Modeling of Trajectory Planning and Scene Evolution
NeurIPS 2025
P0061 SeerDrive
```

Official repo:

```text
LogosRoboticsGroup/SeerDrive
```

---

# 1. Executive verdict

The NeurIPS paper and the released public implementation must be treated as **two related but non-identical artifacts**.

## Paper mechanism

```text
current BEV + multimodal ego/mode features
→ candidate/mode-specific future BEV
→ future-aware dual-branch planner
→ refined ego feature
→ feed refined ego feature back to world model
→ update future BEV
→ repeat internal refinement
→ final trajectory
```

Scientific subtype:

```text
ITERATIVE LATENT WORLD↔PLANNER CO-REFINEMENT
```

## Released-code mechanism

The official README explicitly says the release was updated by integrating WoTE's online trajectory evaluation and selection process, achieving ~88.88 PDMS **without the iterative interaction between planning and scene modeling**.

The repository's `initial release` commit:

```text
1cfb7ecdbdbbe52fd598949efe4edf8f6fb12b69
2025-10-25
```

already contains in `SeerDrive_model.py`:

```text
trajectory anchors
latent_world_model
RewardConvNet
reward_head
five sim_reward_heads
```

Therefore the available public source is **not evidence that the original paper's iterative architecture was implemented exactly as described**. It is evidence for the later WoTE-integrated release path.

Binding rule:

```text
paper mechanism = verify from paper
released implementation = verify from source
never silently merge the two
```

---

# 2. Original paper data flow

## Current representation

NAVSIM input:

```text
multi-view RGB + LiDAR
→ TransFuser
→ F_bev^curr
```

Trajectory anchors + ego status:

```text
→ F_ego^curr ∈ R^{M×C}
```

Default multimodal counts:

```text
NAVSIM   M=256
nuScenes M=6
```

## Future world prediction

Current BEV is repeated over the M modes and combined with mode-specific ego features:

```text
F_scene^curr ∈ R^{M×(HW+1)×C}
→ Transformer BEV World Model
→ F_scene^fut
→ F_bev^fut
→ semantic BEV decoder
```

The paper predicts only the **final planning-horizon future BEV by default**:

```text
NAVSIM   4 s
nuScenes 3 s
```

## Future-aware planning

The planner is decoupled into two branches:

```text
current ego × current BEV
→ T_a

future ego initialized from anchor endpoints × future BEV
→ T_b
```

Motion-aware LayerNorm fuses future ego information into current ego representation:

```text
MLN(F_ego^curr, F_ego^fut)
→ T_final
```

## Iterative refinement

The refined current ego feature is fed back into the BEV world model to update future BEV. This process repeats N times; each iteration outputs future semantic map and trajectories and receives supervision.

Crucial interpretation:

```text
iteration = internal model/planner refinement
iteration != physical-time transition
iteration != environment execution-feedback loop
```

---

# 3. Multimodal supervision boundary

The supplement states:

```text
future BEV is multimodal
future BEV mode aligns with ego/planning mode
winner-takes-all supervision is used
best trajectory and corresponding future BEV are selected
using the same current-ego mode probability
```

Therefore:

```text
candidate/mode-specific future outputs = YES
K separately observed alternative futures = NO
```

No inspected evidence establishes candidate-specific reactive surrounding-agent ground truth.

This is an important boundary against the paper's broad bidirectional/closed-loop language.

---

# 4. Strongest matched evidence

## 4.1 Core mechanisms — NAVSIM Table 3

```text
Future-aware   Iterative   PDMS
NO             NO          87.1
NO             YES         87.9
YES            NO          88.1
YES            YES         88.9
```

This is the strongest causal evidence in the paper.

It supports:

```text
future-aware use of predicted BEV helps
+
internal iterative world/planner refinement helps
+
the two mechanisms are complementary in the reported setup
```

It does not prove behavioral counterfactual correctness.

## 4.2 Future-planning coupling — Table 4

```text
w/o future BEV       87.9
w/o decoupled design 87.3
MLN→Cat              88.3
MLN→Add              88.5
full MLN             88.9
```

This shows the **interface** between current/future information and planner matters, not merely the existence of a future representation.

## 4.3 Refinement iterations — Table 5

```text
1 iteration  88.1
2 iterations 88.9
3 iterations 88.7
```

Refinement depth is non-monotonic.

## 4.4 Temporal future richness — Table 6

```text
1s-2s-3s-4s  88.8
2s-4s         88.9
4s only       88.9
```

Intermediate temporal world predictions do not materially improve PDMS.

This is direct evidence against any monotonic `more future rollout = better planning` assumption.

## 4.5 Present/future planner branches — Table 7

```text
T_a       88.3
T_b       88.2
T_final   88.9
```

Fusion contributes beyond either branch alone.

## 4.6 Future-ego initialization — Table 8

```text
random             88.6
full anchor traj   88.7
anchor endpoint    88.9
```

This is a secondary effect.

---

# 5. Prediction evidence vs planning evidence

The paper reports future semantic BEV prediction quality (mIoU), but no inspected experiment establishes a monotonic relationship:

```text
future-BEV fidelity ↑
→ PDMS ↑
```

Indeed, intermediate temporal prediction adds world-model content without improving planning.

Therefore retain:

```text
world-prediction quality != planning evidence
world completeness != decision relevance
```

The paper supports the usefulness of a **planning interface to future information**, not a universal value of richer future reconstruction.

---

# 6. Counterfactual / reactive evidence vector

```text
candidate-specific output:
YES — multimodal future BEV modes

alternative-action future supervision:
NO matched K-way intervention truth established

reactive other-agent response truth:
NOT ESTABLISHED

external intervention validation:
NOT ESTABLISHED
```

NAVSIM remains non-reactive data-driven planning evaluation under the project taxonomy.

Bench2Drive supplementary results provide reactive closed-loop simulator evidence for the **deployed planner/system**, but they do not validate every internal candidate-conditioned future as a correct counterfactual environment response.

---

# 7. Candidate/ranking bottleneck evidence

The supplementary failure analysis explicitly shows:

1. a good candidate can exist but receive an insufficient classification score;
2. right-turn failure can result from candidate modes/intention distribution favoring left/straight.

This is useful direct evidence that:

```text
candidate support
candidate ranking
world prediction
```

remain separate bottlenecks.

---

# 8. Evaluation semantics

```text
NAVSIM
= non-reactive data-driven planning evaluation

nuScenes
= open-loop trajectory planning

Bench2Drive supplement
= reactive closed-loop simulator policy evaluation
```

Do not collapse these regimes.

Reported supplementary Bench2Drive result:

```text
Avg L2        0.66
Driving Score 58.32
Success Rate  30.17%
```

---

# 9. Runtime

Supplement reports approximately:

```text
66M parameters
24ms average inference time
```

The endpoint-only future BEV design is also computationally meaningful because richer temporal predictions did not improve PDMS.

---

# 10. Ontology impact

SeerDrive fits most V1 families but exposes a new distinction that should become V1.1:

```text
TEMPORAL ROLLOUT DEPTH
!=
INTRA-DECISION REFINEMENT DEPTH
```

Candidate V1.1 additions:

```text
1. inference iteration semantics
2. feedback carrier
3. mutual-refinement topology
4. per-iteration supervision
5. refinement-depth saturation / compute trade-off
```

These must be backfilled for the first five anchors before being treated as stable canonical dimensions.

---

# 11. Final scientific judgment

AUTHOR CLAIM:

> scene evolution and vehicle planning are bidirectionally modeled in a closed-loop manner.

DIRECT EVIDENCE:

- predicted future BEV is consumed by planner;
- refined ego/planning feature is fed back to the world model;
- matched ablations show both future-aware planning and iterative refinement improve PDMS;
- two refinement iterations outperform one, while three do not improve further.

OUR INTERPRETATION:

> SeerDrive demonstrates **internal iterative latent co-refinement between world prediction and planning**.

WHAT REMAINS UNPROVEN:

> That this internal bidirectional feature loop corresponds to behaviorally correct causal ego↔traffic interaction under alternative executed actions.

This narrower interpretation preserves the paper's real contribution while avoiding an unjustified upgrade from neural feedback to externally validated interactive world dynamics.
