# P0007 DriveReward — Dimension-first Deep Analysis v2

Last updated: 2026-09-16

Paper: **DriveReward: A Comprehensive Dataset and Generative Vision-Language Reward Model for Autonomous Driving**  
Public record: **arXiv:2606.08525v2** (current public version observed 2026-09-16; v2 dated 2026-06-09)  
Primary in-repo evidence: `papers/raw_md/P0007_DriveReward/P0007_DriveReward.raw.md`  
Implementation status: **NO attributable official GitHub implementation identified in project ingest or live search as of 2026-09-16.**

Reading protocol: paper-deep-reader reconstruction + source/version gate + reward/supervision decomposition + immediate cross-paper comparison + Ontology V1/V1.1/V1.2/V1.3 force-fill.

---

# 0. Executive verdict

DriveReward is best understood as a **VISION-LANGUAGE TRAJECTORY VALUE / REWARD MODEL**, not as a future-world predictor.

Its core deployed mapping is approximately:

```text
current / short-history front-view visual context
+ navigation instruction
+ ego state
+ candidate ego trajectory
        ↓
InternVL3-1B reward model
+ geometry grounding from VGGT during training
        ↓
reasoning tokens
+ seven reward dimensions
        ↓
(a) RL reward for policy post-training
or
(b) test-time candidate trajectory scoring / selection
```

The decisive boundary is:

```text
candidate trajectory → reward/value
!=
candidate trajectory → predicted future world → reward/value
```

DriveReward does not explicitly predict future RGB, BEV, occupancy, object trajectories, world latent states, or reactive surrounding-agent futures. It learns a direct semantic evaluation function from current visual context and a proposed ego trajectory.

Canonical subtype:

```text
VLM-BASED CANDIDATE VALUE / REWARD MODEL
+ RL REWARD TEACHER
+ OPTIONAL TEST-TIME TRAJECTORY SCORER
```

Scientific role in this project:

> **Control anchor separating future-world modeling from learned trajectory valuation.**

---

# 1. What problem does DriveReward actually solve?

The paper targets a specific bottleneck in modern multimodal planning and VLA post-training:

```text
multiple candidate trajectories exist
→ which candidate is good?
→ how can we provide a scalable reward for RL / selection?
```

The paper argues that common trajectory evaluation methods depend heavily on:

```text
hand-crafted rules
explicit perception annotations
GT trajectory similarity
PDM / PDMS-style simulator infrastructure
```

and that these sources scale poorly or miss high-level semantic violations such as red-light or command-following errors.

DriveReward therefore shifts the main learned object from a future world state to an explicit **trajectory quality function**.

This is important for the WAM atlas because a planner can gain consequence-sensitive supervision without retaining any future-world state at inference.

---

# 2. Dataset: what is actually supervised?

## 2.1 Candidate trajectory sources

For each driving frame, candidate ego trajectories come from three sources:

```text
1. original dataset / GT trajectory
2. ego-state-based retrieval from an offline kinematic bank
3. planner-generated trajectories
```

This broadens the action support beyond the single logged expert trajectory.

However:

```text
many ego candidates
!=
many observed alternative-world futures
```

The dataset contains diverse hypothetical ego behaviors, but it does not provide one experimentally observed surrounding-world response for every candidate.

## 2.2 Reward labels

Each trajectory receives multi-dimensional labels.

Five NAVSIM/PDM-style dimensions:

```text
NC   No Collision
DAC  Drivable Area Compliance
TTC  Time-to-Collision
EP   Ego Progress
C    Comfort
```

Two added dimensions:

```text
CF   Command Following
LG   Legality
```

Label provenance is heterogeneous and must remain separated:

```text
NC/DAC/TTC/EP/C
→ PDM-Closed / NAVSIM-style simulator or rule-derived metric pipeline

CF
→ deterministic rule based on endpoint lateral deviation relative to GT intent

LG
→ Qwen3.5-35B-A3B semantic judging of red-light / solid-line violations

reasoning CoT
→ Qwen3.5 explanation conditioned on visual prompts + metric context
```

The teacher annotation pipeline receives additional deterministic visual overlays such as the candidate trajectory, collision points, off-road points and highlighted objects/boundaries. These overlays are annotation-time aids only; the paper states that the final reward model is trained on the original, unmodified visual input.

## 2.3 What `counterfactual` means here

The paper describes counterfactual augmentation because it creates diverse erroneous or suboptimal ego behaviors.

Canonical project interpretation:

```text
counterfactual ego-action proposals                 YES
candidate-specific reward / consequence labels     YES
candidate-specific observed future world truth     NO
reactive other-agent intervention truth             NO
```

Thus DriveReward provides **counterfactual action valuation**, not experimentally identified counterfactual world dynamics.

---

# 3. Reward model input and representation

The model is built on InternVL3-1B.

Paper-level input is:

```text
front-view visual context I_t
+ navigation instruction
+ ego velocity / acceleration
+ candidate future ego trajectory h_fut ∈ R^(T×3)
```

The textual prompt carries navigation, ego-state and trajectory information.

Temporal-input wording is not perfectly consistent:

```text
architecture equation/prose:
"current front-view image"

training/dataset prose and visual example:
"historical video frames" / 3-frame historical sequence
```

Without released code, the exact deployed temporal packing should be retained as **PAPER-AMBIGUOUS** rather than silently normalized.

---

# 4. Geometry grounding

DriveReward adds a geometric auxiliary path:

```text
reward-model hidden geometry feature f_geo
→ Geometry Adapter (MLP)
→ VGGT latent space
→ L2 alignment to pretrained VGGT dense representation
```

Scientific function:

```text
inject spatial/geometric prior
→ improve trajectory–road / trajectory–scene judgment
```

This is not future-world supervision. It is **representation grounding** for the evaluator.

The paper reports consistent but smaller improvements from the 3D/geometry adapter relative to removing reasoning supervision.

---

# 5. Reward generation

The model does not use a conventional scalar regression head as its main output. It autoregressively emits text tokens:

```text
<think> ... trajectory evaluation reasoning ... </think>
<answer> ... numerical reward dimensions ... </answer>
```

Seven reward dimensions are generated directly.

Therefore DriveReward combines:

```text
semantic reasoning
+
explicit factorized reward prediction
```

but the output object is still a **value/reward description**, not a simulated future state.

---

# 6. Training graph

## Stage 1 — domain-specific pretraining

The paper aggregates 10 autonomous-driving QA / reasoning datasets to adapt the VLM toward driving semantics, spatial-temporal understanding and action reasoning.

Reported training scale in the appendix:

```text
~800k domain-specific QA
6 epochs
```

## Stage 2 — DriveReward SFT

The reward model is then supervised on DriveReward QA/reward samples:

```text
visual / textual context + candidate trajectory
→ reasoning tokens
→ seven reward values
```

The paper reports 8 epochs in this stage.

## Trainability ambiguity

Two statements are not perfectly aligned:

```text
§5.1:
vision backbone frozen;
LLM layers fine-tuned

appendix training description:
"full parameter fine-tuning" in both stages
```

The most conservative interpretation is:

```text
vision encoder freeze is explicitly stated in main experimental setup;
exact meaning of "full parameter" in appendix is unresolved without code.
```

Do not invent a more precise gradient graph.

## Dataset-size reporting ambiguity

The appendix dataset analysis states:

```text
200K samples
```

while the training-parameter paragraph states:

```text
300K DriveReward dataset
```

Possible explanations include sample-vs-QA counting or revision mismatch, but the paper does not resolve it in the audited text.

Record as:

```text
DATASET SCALE = 200K / 300K REPORTING INCONSISTENCY
```

---

# 7. RL use: reward model as a training-time teacher

One main deployment mode is **not deployment at all**: the trained reward model supplies scalar reward during policy RL post-training.

Three reward formulations are evaluated:

```text
1. rule-based PDMS
2. DriveReward-predicted PDMS
3. rule-based PDMS + DriveReward-predicted CF + LG
```

The standard PDMS form uses:

```text
NC × DAC × weighted(EP, TTC, Comfort)
```

The hybrid adds learned CF and LG terms.

Scientific lifecycle:

```text
DriveReward evaluates generated policy trajectories during RL
→ reward signal shapes policy parameters
→ final policy can execute without DriveReward online
```

No evidence was identified that policy loss backpropagates through the reward model itself. Treat DriveReward as a fixed external reward teacher unless future source code establishes joint optimization.

This creates an important control for WAM comparison:

```text
planning can absorb consequence/value knowledge through post-training
without deploying a future model at inference.
```

---

# 8. Test-time trajectory selection

DriveReward is also used online as a scorer.

On AdaThinkDrive, four trajectories are generated from independent inference passes:

```text
Original        90.3 PDMS
Best-of-4       93.0 PDMS   (+2.7 oracle headroom)
DriveReward     90.5 PDMS   (+0.2)
```

This is the strongest direct evidence for the online-scoring path and also its strongest limitation.

Canonical interpretation:

```text
DriveReward can recover some candidate-selection value
BUT
current test-time ranking captures only a small fraction of available oracle headroom.
```

The paper itself acknowledges this gap.

Do not narrate the online scorer as a large planning gain.

---

# 9. RL evidence

## NAVSIM-v1 / non-reactive data-driven evaluation

Reported SFT → RL-RM improvements:

```text
InternVL3-2B     80.8 → 82.2 PDMS
InternVL3-8B     85.6 → 86.8
DiffusionDriveV2 89.1 → 90.7
```

This is positive evidence that model-predicted reward can train stronger policies than the corresponding SFT checkpoints.

Project-standard evaluation label remains:

```text
NAVSIM-v1
= NON-REACTIVE DATA-DRIVEN / PSEUDO-SIMULATION PLANNING
```

The paper table calls this `Open-Loop Evaluation`; do not let that naming override the project benchmark ontology.

## Reward-model enhancement of rule reward

Adding DriveReward CF/LG to rule PDMS yields:

```text
InternVL3-2B     83.3 → 83.3 PDMS
InternVL3-8B     87.9 → 88.4
AdaThinkDrive-8B 89.3 → 89.9
```

The gains are modest and not uniformly positive on efficiency/progress.

This supports the narrower claim that semantic reward dimensions can add information not captured by base PDMS.

---

# 10. Bench2Drive closed-loop evidence

DriveReward is transferred zero-shot as an RL reward teacher on Bench2Drive / CARLA.

Reported policy results:

```text
Base SFT                        DS 40.2 / Success 14.5
RL (RM-predicted PDMS)          DS 51.4 / Success 20.8
RL (rule-based PDMS)            DS 55.0 / Success 25.0
RL (rule-PDMS + RM CF/LG)       DS 57.1 / Success 27.2
```

This is stronger evidence for the **training-time reward interface** than the test-time scorer interface.

Important trade-off / reporting signal:

```text
Comfort↑ column:
Base SFT                  42.9
RM-predicted PDMS RL      19.2
Rule-PDMS RL              14.8
Rule-PDMS + RM CF/LG      11.4
```

Therefore the overall driving-score improvement should not be described as uniform improvement across all behavioral qualities. Either a genuine reward trade-off or a benchmark/reporting semantic issue exists; the paper does not resolve it in the audited text.

---

# 11. Reward-model benchmark evidence

Task-specific training is clearly effective for reward prediction.

Representative benchmark comparison:

```text
InternVL3-1B SFT
Safety 72.2 / DAC 75.6 / CF 95.5 / LG 92.2 / EP-MAE 0.34

DriveReward-1B
Safety 80.6 / DAC 81.2 / CF 99.9 / LG 97.6 / EP-MAE 0.23
```

Ablation signals:

```text
full DriveReward-1B
NC 80.58 / DAC 81.24 / CF 99.86 / LG 97.64 / EP-MAE 0.2308

w/o pre-training
80.52 / 81.06 / 99.84 / 97.48 / 0.2355

w/o reasoning CoT
71.26 / 73.60 / 100.00 / [LG not reported in extracted table] / 0.4161

w/o 3d adapter
79.04 / 80.88 / 99.86 / 97.20 / 0.2518
```

The biggest matched degradation is from removing reasoning CoT, not from removing domain pretraining or geometry grounding.

Thus the final reward-model gain is a bundle of:

```text
task-specific reward labels
+ teacher-generated semantic reasoning
+ InternVL/VLM prior
+ geometry alignment
+ domain-specific pretraining
```

Do not attribute the entire improvement to the 3D adapter or pretraining.

---

# 12. World-model boundary

DriveReward gives a clean negative control for the claim that trajectory evaluation requires an explicit future world model.

At inference, it consumes:

```text
current / short-history visual context
+ candidate ego trajectory
```

and emits:

```text
reward factors / reasoning
```

There is no explicit intermediate:

```text
future scene
future BEV
future occupancy
future object set
future latent world trajectory
```

Therefore:

```text
candidate consequence/value approximation     YES
explicit future-world prediction              NO
world rollout                                 NO
world→value decomposition                     NO
```

The model may implicitly encode expected consequences inside VLM hidden states, but hidden semantic competence is not sufficient to label it a world model.

Canonical boundary:

> **A learned trajectory evaluator is not automatically a WAM merely because its reward depends on the consequences of the trajectory.**

---

# 13. Immediate cross-paper comparison

## DriveReward vs WoTE

```text
WoTE:
candidate action
→ recurrent future BEV/state sequence
→ learned utility
→ argmax

DriveReward:
current visual context + candidate trajectory
→ direct semantic reward/value
→ RL reward or argmax
```

Shared scientific job:

```text
rank / train actions using learned decision utility
```

Different mechanism:

```text
explicit future-state mediator vs direct value approximation
```

WoTE's matched scorer-only controls show that future state can add value inside that architecture; DriveReward demonstrates that useful trajectory valuation is nevertheless possible without an explicit future-state object.

## DriveReward vs DA-WAM

```text
DA-WAM:
candidate → short future latent → factor/value score

DriveReward:
candidate + visual context → factorized reward directly
```

DA-WAM's matched control is especially relevant:

```text
No Future                  93.31 PDMS
Action-Conditioned Future  93.46
+ Hard Negatives           93.68
```

The incremental future-latent gain is much smaller than the total strength of the scoring system. DriveReward is therefore an important control against narrating all high-performing candidate valuation as `world-model benefit`.

## DriveReward vs SafeDrive

```text
SafeDrive:
candidate → sparse candidate-conditioned world → fine-grained safety consequence → select

DriveReward:
candidate + current VLM context → direct semantic reward dimensions → train/select
```

Both have explicit safety semantics, but SafeDrive constructs an explicit sparse consequence representation whereas DriveReward directly predicts the value factors.

## DriveReward vs RiskWorld

```text
RiskWorld:
observed history → factual physical future rollout → risk object
no action selection

DriveReward:
hypothetical ego action → direct value/risk factors
no physical future rollout
```

This is nearly an inversion:

```text
RiskWorld = strong future modeling, weak/no planner interface
DriveReward = strong decision interface, no explicit future modeling
```

## DriveReward vs WorldDrive / Drive-JEPA

WorldDrive and Drive-JEPA show how predictive/world knowledge can shape a planner representation or candidate system. DriveReward shows an orthogonal route:

```text
learn the decision utility itself
```

This strengthens the project-wide attribution rule:

```text
planning improvement
must be decomposed into
representation + candidate support + future consequence + value/reward + post-training
rather than collapsed into one "WM gain".
```

---

# 14. Historical boundary / Gen-Drive control

The paper itself identifies Gen-Drive as a nearby reward-model predecessor.

Gen-Drive uses preference modeling / DPO-style reward learning inside a generation-then-evaluation planning pipeline, whereas DriveReward emphasizes explicit metric factors + semantic legality/command reasoning.

Therefore DriveReward's novelty should not be stated as `first learned driving reward model`.

More defensible distinction:

```text
factorized explicit driving reward supervision
+ VLM semantic reasoning
+ geometry grounding
+ use as both RL reward and test-time scorer
```

P0006 GenDrive should remain a targeted historical comparator if reward/value interfaces become decision-critical later.

---

# 15. What DriveReward proves

Direct paper evidence supports:

1. A small task-specific VLM can predict structured driving reward dimensions substantially better than the tested zero-shot VLM baselines.
2. A learned reward model can provide useful RL supervision across multiple planners.
3. The learned reward transfers as an RL teacher from nuPlan/NAVSIM-style training data to Bench2Drive/CARLA in the reported setup.
4. Semantic CF/LG reward factors can add incremental value to rule-based PDMS.
5. Direct test-time reward scoring can produce a small improvement over the original AdaThinkDrive selection.

---

# 16. What DriveReward does NOT prove

It does not establish:

1. an explicit future-world model;
2. accurate alternative-action world-state prediction;
3. reactive surrounding-agent responses under changed ego behavior;
4. that VLM hidden reasoning is a causally valid dynamics model;
5. that model-predicted reward matches rule/simulator reward in all regimes;
6. that online reward scoring captures most of the available candidate-selection headroom;
7. that gains arise primarily from domain pretraining or geometry grounding;
8. real-vehicle closed-loop improvement;
9. calibrated uncertainty over reward prediction;
10. a uniform improvement in comfort/efficiency alongside overall driving score.

---

# 17. Residue test against Ontology V1.3

DriveReward strongly exercises existing axes:

```text
A01/A02  planning bottleneck / role of learned knowledge
D04–D06  candidate construction and support
G04/K01–K05 reward/value supervision and semantics
J01/J03/J05 world/planner interface and action selection
L01–L06 training topology and losses
M01–M03 training-teacher vs online-scorer lifecycle
O01–O07 evaluation and attribution
P01/P02 explicit safety/value semantics
```

No irreducible new dimension survives back-projection.

Potential residue considered:

```text
semantic-reward factor provenance / teacher heterogeneity
```

but this is already representable through G04/G05, K02/K05 and O03/O06.

Ontology decision:

```text
V1.3 RETAINED
NO V1.4
```

---

# Final normalized identity

```text
DriveReward
=
current / short-history front visual context
+ route command
+ ego state
+ candidate trajectory
→ InternVL3-1B semantic evaluator
+ VGGT geometry-alignment prior
→ reasoning tokens
→ NC / DAC / TTC / EP / Comfort / CF / Legality
→ (training) RL reward teacher
   OR
→ (deployment) candidate trajectory scorer

FUTURE WORLD STATE             ABSENT
CANDIDATE-SPECIFIC VALUE       YES
CANDIDATE-SPECIFIC WORLD GT    NO
REACTIVE INTERVENTION TRUTH    NO
RL POLICY SUPERVISION          YES
ONLINE TEST-TIME SCORING       OPTIONAL / YES
```

Best role in the WAM atlas:

> **A decisive value/reward control demonstrating that trajectory consequence knowledge can be compressed directly into a semantic evaluator without an explicit deployed future-world state.**
