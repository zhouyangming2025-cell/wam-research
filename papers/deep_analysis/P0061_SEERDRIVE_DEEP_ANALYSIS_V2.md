# P0061 SeerDrive — Dimension-first Deep Analysis v2

> Paper: **Future-Aware End-to-End Driving: Bidirectional Modeling of Trajectory Planning and Scene Evolution** (NeurIPS 2025)  
> Purpose: read SeerDrive under the shared WAM scientific coordinate system, not inside the paper's own “bidirectional/closed-loop” narrative.  
> Primary source: `papers/raw_md/P0061_SeerDrive/P0061_SeerDrive.raw.md`.  
> Official repo: `LogosRoboticsGroup/SeerDrive`; public release code is a **post-paper WoTE-integrated variant** and is not used to overwrite the paper mechanism.  
> Reading stack used: `paper-deep-reader` for mainline/mechanism/formula/evidence reconstruction; `literature-reading-and-synthesis` for immediate cross-paper projection; `academic-research-agent` source/claim discipline for version and evidence boundaries.

---

# 0. Executive verdict

SeerDrive is best understood as **future-BEV-guided multimodal planning with intra-decision iterative world↔planner feature co-refinement**, not as a standard candidate-consequence-value planner and not as a temporally recurrent world rollout.

The paper's original mechanism is approximately:

```text
multi-view image + LiDAR
→ TransFuser
→ current BEV F_bev^curr

trajectory anchors + ego status
→ M current ego/mode features F_ego^curr

repeat current BEV across M modes
+ concatenate each mode's ego feature
→ M current scene features
→ shared BEV World Model
→ M future BEV features F_bev^fut
→ future BEV semantic supervision

planning branch A:
F_ego^curr ↔ F_bev^curr
→ T_a

planning branch B:
anchor endpoint initializes F_ego^fut
F_ego^fut ↔ F_bev^fut
→ T_b

MLN(F_ego^curr, F_ego^fut)
→ T_final

refined F_ego^curr
→ fed back into BEV World Model
→ update F_bev^fut
→ repeat planning refinement N times
```

This creates real **world→planning feedback** because predicted future BEV is consumed by the deployed planner, and a real **planning-feature→world feedback** because the refined ego feature is fed back into the world model during the same decision computation.

However, the paper's phrase “closed-loop” must be interpreted narrowly. The loop is an **internal neural refinement loop inside one planning decision**, not demonstrated environment feedback after executing an action. It is not equivalent to:

```text
execute ego action
→ other agents react
→ observe new world
→ re-plan
```

and it is not equivalent to WoTE's temporal recurrent rollout:

```text
state_t + action
→ state_t+1
→ state_t+2
→ reward
```

The strongest new ontology insight from SeerDrive is therefore:

> **Iteration depth in a WAM must be separated into temporal rollout depth and intra-decision world↔planner refinement depth.**

---

# 1. Source/version map — mandatory before interpreting the mechanism

## 1.1 Paper authority

Canonical paper text in this repo:

```text
P0061_SeerDrive.raw.md
```

The paper describes the NeurIPS method as:

```text
future-aware planning
+
iterative scene modeling and vehicle planning
```

where future BEV and ego/planning features interact iteratively.

## 1.2 Public code is not the same method snapshot

The official repository README explicitly says that the released code was updated by integrating the **online trajectory evaluation and selection process proposed in WoTE**, reporting 88.88 PDMS **without the iterative interaction between planning and scene modeling**.

The official repository's `initial release` commit (`1cfb7ec...`, 2025-10-25) already contains:

```text
trajectory anchors
latent_world_model
RewardConvNet
reward_head
five simulator reward heads
```

Thus the public code is scientifically useful, but it verifies a **later released variant**, not the exact original paper's iterative mechanism.

### Binding source rule

For P0061:

```text
paper architecture / original ablations
→ paper is primary authority

released WoTE-integrated deployment implementation
→ official source code is authority

never merge the two into one undocumented architecture
```

This is a direct application of the source/version discipline from the external research skills.

---

# 2. What problem does SeerDrive actually attack?

The paper frames conventional E2E planning as one-shot:

```text
current scene
→ trajectory
```

and argues that two dependencies are underused:

```text
future scene → ego planning
planned ego state → predicted future scene
```

The important scientific object is therefore not merely “future prediction,” but **coupling topology between world prediction and planning**.

Immediate cross-paper contrast:

```text
LAW
planner action → future latent
but future latent does not feed back into current action selection

Epona
action → visual future
but visual future is not required to re-score/refine same-step trajectory

WoTE
candidate → future BEV sequence → reward → select
one-way consequence-to-value chain after candidate generation

WorldDrive
candidate → distilled future representation → reward → select
again mainly one-way future-to-ranking at deployment

World4Drive
candidate → compact future latent → mode score → select
again future-to-selection

SeerDrive (paper)
planning feature → future BEV → planning feature → future BEV → ...
repeated within one inference computation
```

So the distinct axis is not simply `future online = YES`; it is **whether world and planner mutually refine each other before the final action is emitted**.

---

# 3. Current-state and candidate construction

## 3.1 Current BEV

Sensor inputs are encoded by TransFuser:

```text
multi-view images I + LiDAR P
→ F_bev^curr ∈ R^{H×W×C}
```

A lightweight decoder predicts current semantic BEV for auxiliary supervision.

## 3.2 Multimodal ego feature

Trajectory anchors and ego status are encoded into:

```text
F_ego^curr ∈ R^{M×C}
```

where each row corresponds to one trajectory mode.

Reported default modes:

```text
NAVSIM    M = 256
nuScenes  M = 6
```

This matters immediately: SeerDrive's future worlds are multimodal largely because **the current scene is replicated across an existing multimodal trajectory-mode dimension**.

It does not first generate a single world future and then create trajectories. Nor does it construct independent causal simulators per candidate.

---

# 4. Future BEV World Model

The current BEV is flattened and repeated across the mode dimension:

```text
F_bev^curr
→ repeat M times
→ R^{M×HW×C}
```

Each mode's current ego feature is concatenated:

```text
F_scene^curr ∈ R^{M×(HW+1)×C}
```

A shared Transformer encoder predicts:

```text
F_scene^fut = BEVWorldModel(F_scene^curr)
```

from which mode-specific future BEV features are extracted.

A BEV decoder predicts future semantic maps for supervision.

## 4.1 What is action conditioning here?

It is more accurate to say:

```text
trajectory-mode / ego-feature conditioned world prediction
```

than to claim fully intervention-identified action-conditioned dynamics.

The mode representation contains anchored-trajectory and ego-status information, and the future BEV branch varies across modes. But the dataset still contains one realized future.

## 4.2 Multi-modal future supervision

The supplement clarifies that future BEV prediction is multimodal and shares the ego mode structure. Supervision uses winner-takes-all:

```text
mode probability from current ego feature
→ choose best trajectory/mode
→ choose corresponding future BEV
→ compute loss on selected mode
```

Therefore:

```text
M future BEV outputs = YES
M separately observed alternative-action future BEV GT = NO
```

This places SeerDrive in the same broad structural warning class as World4Drive:

> branch multiplicity is not alternative-intervention ground truth.

But the assignment mechanism differs:

```text
World4Drive:
nearest predicted future latent to factual future → branch j

SeerDrive:
trajectory/mode probability winner → same mode used for trajectory and future-BEV WTA supervision
```

This is a useful new comparison point under multimodal branch assignment.

---

# 5. Future-aware planning: future is consumed, but not through a scalar reward

SeerDrive deliberately decouples current-scene planning from future-scene planning.

## 5.1 Current branch

```text
F_ego^curr
cross-attend F_bev^curr
→ updated current ego feature
→ EgoDecoder
→ T_a
```

## 5.2 Future branch

The future ego feature is initialized using trajectory-anchor endpoints, then interacts with predicted future BEV:

```text
anchor endpoints
→ F_ego^fut init

F_ego^fut
cross-attend F_bev^fut
→ updated future ego feature
→ EgoDecoder
→ T_b
```

## 5.3 Fusion

Motion-aware LayerNorm (MLN) fuses future ego information into current ego information:

```text
F_ego^curr ← MLN(F_ego^curr, F_ego^fut)
→ T_final
```

This is a fundamentally different world→planning interface from WoTE / WorldDrive / World4Drive.

```text
WoTE / WorldDrive / World4Drive:
future object
→ scorer/reward/mode score
→ choose candidate

SeerDrive:
future BEV
→ future-side planning feature
→ feature fusion/refinement
→ final trajectory
```

So **future consumption location** must distinguish at least:

```text
candidate scoring/ranking
trajectory feature refinement
trajectory generation/decoding
policy hidden-state update
```

SeerDrive primarily uses future world information as a **planner feature-refinement signal**, not as an explicit scalar utility.

---

# 6. Iterative scene modeling and vehicle planning — the main new mechanism

After one future-aware planning pass, the refined `F_ego^curr` is fed back into the BEV world model. The world model then predicts a revised future BEV, which again refines planning.

Conceptually:

```text
iteration 0:
current BEV + initial ego/mode feature
→ future BEV^(0)
→ planner
→ refined ego feature^(0)

iteration 1:
current BEV + refined ego feature^(0)
→ future BEV^(1)
→ planner
→ refined ego feature^(1)

...
```

Each iteration's future semantic map and trajectories are supervised during training.

## 6.1 What the iteration IS

- repeated neural computation inside the same decision;
- alternating refinement of world representation and planning representation;
- same planning horizon reconsidered multiple times;
- a form of iterative/co-refinement inference.

## 6.2 What the iteration IS NOT

It is **not** automatically:

- a 2-step or 3-step physical-time world rollout;
- execution-feedback closed loop;
- reactive surrounding-agent simulation;
- model predictive control over observed environment feedback.

This distinction is empirically reinforced by Table 6: predicting intermediate temporal BEVs at `1s-2s-3s-4s` does not improve over predicting only the `4s` future endpoint.

So:

```text
planning/world refinement iterations N
!=
future temporal prediction steps
```

This distinction was not explicit enough in Ontology V1 and is a genuine SeerDrive-driven ontology residue.

---

# 7. Evidence ladder — what actually isolates SeerDrive's contribution?

## 7.1 Core 2×2 component ablation (NAVSIM)

```text
Future-aware planning   Iterative S&V   PDMS
NO                      NO              87.1
NO                      YES             87.9
YES                     NO              88.1
YES                     YES             88.9
```

This is the strongest evidence in the paper because it separately tests both proposed mechanisms.

Interpretation:

```text
future-aware planning alone   ≈ +1.0
iterative refinement alone    ≈ +0.8
both together                 ≈ +1.8 over baseline
```

Within this matched setup, the two mechanisms are roughly complementary.

### Boundary

This does not prove that the learned future BEV is physically correct under alternative interventions. It proves that **using the predicted future representation and iterating the model/planner computation improves NAVSIM planning score**.

## 7.2 Future-BEV interface ablation

Reported PDMS:

```text
without future BEV        87.9
without decoupled design  87.3
MLN → concat              88.3
MLN → add                 88.5
full MLN                  88.9
```

This supports two claims:

1. predicted future context itself helps;
2. **how** current/future features are coupled matters materially.

Thus `future available = YES` is too coarse. Fusion architecture is a decision mechanism.

## 7.3 Iteration count

```text
1 iteration   88.1
2 iterations  88.9
3 iterations  88.7
```

More refinement is not monotonically better. Two iterations are best in the reported setup.

This exposes an iteration-depth / convergence-quality / latency trade-off.

## 7.4 Temporal prediction steps

```text
1s-2s-3s-4s  88.8
2s-4s         88.9
4s only       88.9
```

This is especially important for WAM research:

> richer temporal world prediction did not yield a meaningful planning gain here.

The paper's best design predicts only the endpoint future BEV.

This strongly reinforces the project-wide principle:

```text
world completeness != decision relevance
```

## 7.5 Two planning branches

```text
T_a current branch   88.3
T_b future branch    88.2
T_final fused        88.9
```

Neither branch alone explains the final performance. The gain lies partly in **combining present-scene and future-scene planning views**.

## 7.6 Future ego initialization

```text
random                 88.6
full anchored trajectory 88.7
anchor endpoint         88.9
```

This is a modest effect, not the main source of gain.

---

# 8. Prediction quality vs planning value

The paper reports future BEV semantic prediction quality (e.g. NAVSIM mIoU around 38.87 in the inspected material), but the key planning evidence does not establish a monotonic relationship:

```text
better future-BEV mIoU
→ better PDMS
```

Indeed, Table 6 shows that adding more intermediate future states does not improve planning despite providing more world-model temporal content.

Therefore SeerDrive should not be narrated as evidence that “more accurate/richer scene evolution modeling automatically improves planning.”

The stronger conclusion is narrower:

> **A compact final-horizon future BEV, when coupled through a good planner interface and iterative feature refinement, is useful in this architecture.**

---

# 9. Candidate generation and selection remain independent bottlenecks

The supplement reports a failure case where a good candidate trajectory is already present but receives an insufficient classification score and is not selected. It also reports a right-turn case where candidate modes mostly favor left/straight motion, motivating stronger high-level intention information.

These failures are unusually useful because they explicitly show two independent bottlenecks:

```text
candidate support / intention coverage
vs
candidate ranking / mode probability
```

Therefore the final SeerDrive PDMS cannot be attributed solely to the world model.

This also connects directly to:

- WoTE: candidate bank + evaluator are separate bottlenecks;
- WorldDrive: best-of-N oracle exposes ranking gap;
- World4Drive: only six intention modes constrain support.

---

# 10. Counterfactual / reactivity profile

Under Ontology V1's vector semantics:

```text
candidate/mode-specific future output:
YES — M mode-specific future BEV features

alternative-action observed/simulated future supervision:
NO direct K-way alternative GT established; WTA uses one demonstrated future/mode target

other-agent reactive response truth:
NOT ESTABLISHED for each candidate/mode

external intervention-validity evidence:
NOT ESTABLISHED
```

NAVSIM remains non-reactive data-driven planning evaluation under the project taxonomy.

The supplement adds Bench2Drive closed-loop policy evaluation, which is stronger deployment evidence for the planner, but it still does not identify the correctness of every internally imagined candidate future under matched interventions.

---

# 11. Evaluation regime

## NAVSIM

Treat as:

```text
non-reactive data-driven planning evaluation
```

not true policy-environment reactive closed loop.

## nuScenes

```text
open-loop planning
```

## Bench2Drive supplement

Reports:

```text
Avg L2        0.66
Driving Score 58.32
Success Rate  30.17%
```

This provides reactive closed-loop simulator evidence for the deployed policy/system. It does **not** by itself prove intervention-correct candidate-specific world dynamics.

---

# 12. Compute and architecture economy

The supplement reports approximately:

```text
66M parameters
24 ms average inference on NAVSIM configuration
```

The paper's finding that only final-horizon BEV is needed is therefore also a compute result:

```text
more temporal future states
→ more model/input complexity
→ almost no PDMS gain
```

Again, planning-relevant compression appears more important than world completeness.

---

# 13. Relation to the five ontology anchors

| Scientific axis | LAW | WoTE | Epona | WorldDrive | World4Drive | SeerDrive |
|---|---|---|---|---|---|---|
| future consumed in deployed planning | no | yes | visual future not required | yes, distilled | yes, compact latent | **yes, future BEV feature** |
| planner interface | representation shaping | consequence→utility→select | direct generative policy from shared latent | future feature→preference rank | future mode→factual consistency score | **future feature→dual-branch refinement/fusion** |
| action/world coupling | action→future only | candidate→future rollout | action→visual future | candidate→teacher/student future | candidate→future latent | **ego/planning feature↔future BEV iterative co-refinement** |
| temporal object | training endpoint | recurrent future sequence | AR visual future, optional for planning | distilled summary | endpoint future latent | **endpoint future BEV by default** |
| scorer semantics | N/A | explicit utility | N/A | preference/value | factual-mode matching | **mode/classification remains a candidate-selection factor, but core future use is feature refinement** |
| counterfactual truth | single factual | multi ego / non-reactive others | not candidate evaluator | teacher-generated alternatives | one factual target for K branches | **multimodal WTA, no K intervention GT** |

The most important difference is SeerDrive's **iterative world↔planner feature topology**. No previous ontology-discovery anchor used the future object primarily through repeated bidirectional feature refinement.

---

# 14. Ontology residue exposed by SeerDrive

Ontology V1 can describe most of SeerDrive, but it does not cleanly separate the following concepts. These are proposed V1.1 additions, not free-form paper-specific fields.

## SD-R01 — Inference iteration semantics

Scientific question:

> What does one “iteration” advance?

Values:

```text
physical future time
candidate-search depth
world↔planner feature refinement depth
optimization/denoising step
environment execution-feedback step
```

SeerDrive = **world↔planner feature refinement depth**.

## SD-R02 — Feedback carrier

What object is passed from planner back into world prediction?

```text
executed action/control
candidate trajectory
planner hidden feature
ego mode feature
reward/value
environment observation
```

SeerDrive = **refined current ego/planning feature**.

This is scientifically distinct from true action execution.

## SD-R03 — Mutual-refinement topology

```text
one-way world→planner
one-way planner/action→world
single-pass bidirectional branches
alternating world↔planner co-refinement
external closed-loop feedback
```

SeerDrive = **alternating internal world↔planner co-refinement**.

## SD-R04 — Per-iteration supervision

Are intermediate refinement states supervised?

```text
final only
all iterations
selected iterations
self-consistency only
```

SeerDrive = **all iterations' future semantic maps and trajectories are supervised**.

## SD-R05 — Refinement-depth saturation

Record whether added refinement iterations improve monotonically and where saturation/reversal occurs.

SeerDrive:

```text
1 → 2 improves
2 → 3 declines slightly
```

This should live under compute/evidence rather than be mistaken for temporal horizon scaling.

These additions should be backfilled for LAW / WoTE / Epona / WorldDrive / World4Drive before they become fully canonical V1.1 dimensions.

---

# 15. Claim–evidence ledger

| Claim | Direct evidence | Strength | What remains unproven |
|---|---|---|---|
| Future BEV helps planning | Table 3 and Table 4 matched ablations | **Strong within architecture** | physical/counterfactual correctness of future BEV |
| Iterative world/planner interaction helps | Table 3; iterations 1/2/3 in Table 5 | **Strong within architecture** | that benefit specifically reflects environment reaction rather than feature refinement capacity |
| Rich temporal future sequence is needed | Table 6 | **Not supported** | endpoint future already matches best PDMS |
| Both current- and future-side planner branches matter | Table 7 | **Moderate/strong** | exact semantic contribution of each representation |
| Bidirectional loop models causal ego↔environment interaction | architectural motivation + internal feedback | **Weak as causal claim** | no matched reactive alternative futures / intervention identification |
| Public code verifies paper's original iterative architecture | official README + initial-release source | **Contradicted for direct equivalence** | released implementation is WoTE-integrated variant |

---

# 16. Final scientific placement

SeerDrive expands the WAM interface map with a distinct subtype:

```text
ITERATIVE LATENT CO-REFINEMENT

current world + ego modes
→ future world hypothesis
→ future-aware planner feature
→ refined ego/planner feature
→ feed back to world predictor
→ repeat
→ final trajectory
```

It should not be collapsed into:

```text
WoTE-style online reward evaluation
World4Drive-style future mode scoring
LAW-style training-only future shaping
Epona-style sibling world generation
WorldDrive-style distilled foresight
```

Its strongest scientific lesson is not “closed-loop world model planning.” It is more precise:

> **Prediction and planning can be iteratively co-refined inside a single E2E inference graph, and a compact final-horizon future representation may be sufficient; richer temporal prediction is not automatically more useful.**

That statement is supported by the paper's component, iteration-count, and temporal-step ablations without upgrading internal feature feedback into externally validated causal interaction.
